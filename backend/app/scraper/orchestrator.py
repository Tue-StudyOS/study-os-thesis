"""ScraperOrchestrator: wires the five pipeline stages together.

Stage 1 - Resolve researcher from DB (auto-create from chair if needed)
Stage 2 - Discover paper candidates via PaperSourceClient (OpenAlex)
Stage 3 - LLM enrichment (summary + tags)
Stage 4 - Score, deduplicate, and persist
"""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime, timezone

from app.papers.dedup import DeduplicationService
from app.papers.domain import PaperCandidate, ResearcherInfo
from app.papers.repository import PaperRepository, TagRepository
from app.researchers.repository import ResearcherRepository
from app.scraper.interfaces import LLMEnricher, PaperRanker, PaperSourceClient

# LLM enrichment can run in parallel, but DB writes must stay sequential because
# SQLAlchemy AsyncSession is not safe for concurrent flushes.
_LLM_CONCURRENCY = 1

_logger = logging.getLogger(__name__)


class ScraperOrchestrator:
    """Coordinates paper discovery, enrichment, and persistence for one researcher."""

    def __init__(
        self,
        source: PaperSourceClient,
        llm_enricher: LLMEnricher,
        ranker: PaperRanker,
        dedup: DeduplicationService,
        paper_repo: PaperRepository,
        tag_repo: TagRepository,
        researcher_repo: ResearcherRepository,
        max_results: int = 20,
        since_days: int = 365,
    ) -> None:
        self._source = source
        self._llm = llm_enricher
        self._ranker = ranker
        self._dedup = dedup
        self._paper_repo = paper_repo
        self._tag_repo = tag_repo
        self._researcher_repo = researcher_repo
        self._max_results = max_results
        self._since_days = since_days

    async def scrape_for_researcher(self, researcher_id: int) -> dict:
        """Run the full pipeline for one researcher. Returns a summary dict."""
        researcher_row = await self._researcher_repo.get_by_id(researcher_id)
        if researcher_row is None:
            raise ValueError(f"Researcher {researcher_id} not found")

        researcher = ResearcherInfo(
            name=researcher_row.name,
            google_scholar_id=researcher_row.google_scholar_id,
            orcid=researcher_row.orcid,
            affiliation=researcher_row.affiliation,
            chair_id=researcher_row.chair_id,
        )

        _logger.info(
            "scraper.start researcher_id=%d name=%r chair_id=%s",
            researcher_id,
            researcher.name,
            researcher.chair_id,
        )

        # Stage 2: Discover papers
        candidates = await self._source.fetch_papers(
            researcher,
            max_results=self._max_results,
            since_days=self._since_days,
        )
        if researcher.google_scholar_id and researcher.google_scholar_id != researcher_row.google_scholar_id:
            await self._researcher_repo.update_google_scholar_id(researcher_id, researcher.google_scholar_id)
            _logger.info(
                "scraper.persisted_google_scholar_id researcher_id=%d profile_id=%s",
                researcher_id,
                researcher.google_scholar_id,
            )
        _logger.info("scraper.source_results count=%d researcher=%r", len(candidates), researcher.name)

        llm_sem = asyncio.Semaphore(_LLM_CONCURRENCY)

        enriched_results = await asyncio.gather(
            *[self._enrich_candidate(candidate, llm_sem) for candidate in candidates],
            return_exceptions=True,
        )

        enriched_candidates = []
        errors = 0
        for result in enriched_results:
            if isinstance(result, BaseException):
                errors += 1
                _logger.warning("scraper.candidate_error %s", result, exc_info=result)
            else:
                enriched_candidates.append(result)

        stored = 0
        skipped = 0
        for candidate, summary, tags, enriched_at, recency in enriched_candidates:
            try:
                candidate_stored, candidate_skipped = await self._persist_candidate(
                    candidate,
                    researcher_id,
                    summary,
                    tags,
                    enriched_at,
                    recency,
                )
            except Exception as exc:
                errors += 1
                _logger.warning("scraper.candidate_error %s", exc, exc_info=exc)
            else:
                stored += candidate_stored
                skipped += candidate_skipped

        await self._paper_repo.commit()
        await self._researcher_repo.commit()

        result = {
            "researcher_id": researcher_id,
            "researcher_name": researcher.name,
            "total": len(candidates),
            "stored": stored,
            "skipped": skipped,
            "errors": errors,
        }
        _logger.info("scraper.complete %s", result)
        return result

    async def _enrich_candidate(
        self,
        candidate: PaperCandidate,
        llm_sem: asyncio.Semaphore,
    ) -> tuple[PaperCandidate, str | None, list[str], datetime | None, float]:
        """Run LLM enrichment and ranking without touching the DB session."""

        # OpenAlex already provides usable metadata/abstracts; avoid hundreds of
        # synchronous local LLM calls during chair sync.
        summary: str | None = None
        tags: list[str] = []
        enriched_at: datetime | None = None

        if candidate.abstract and candidate.source != "openalex":
            async with llm_sem:
                summary = await self._llm.summarize(candidate.title, candidate.abstract)
                tags = await self._llm.generate_tags(candidate.title, candidate.abstract)
            enriched_at = datetime.now(timezone.utc)

        # Stage 5b: Compute scores
        recency = self._ranker.compute_recency_score(candidate.publication_date)
        return candidate, summary, tags, enriched_at, recency

    async def _persist_candidate(
        self,
        candidate: PaperCandidate,
        researcher_id: int,
        summary: str | None,
        tags: list[str],
        enriched_at: datetime | None,
        recency: float,
    ) -> tuple[int, int]:
        """Persist a single enriched candidate. Returns (stored, skipped)."""

        # Stage 5a: Dedup check
        existing = await self._dedup.find_duplicate(candidate)
        if existing is not None:
            await self._dedup.merge_metadata(existing, candidate)
            await self._researcher_repo.link_paper(researcher_id, existing.id)
            _logger.debug(
                "scraper.paper_skipped title=%r (duplicate paper_id=%d)",
                candidate.title[:60],
                existing.id,
            )
            return 0, 1

        # Stage 5c: Persist paper
        paper = await self._paper_repo.create(
            title=candidate.title,
            title_normalized=DeduplicationService.normalize_title(candidate.title),
            abstract=candidate.abstract,
            summary=summary,
            authors=candidate.authors,
            publication_date=candidate.publication_date,
            source=candidate.source,
            source_url=candidate.source_url,
            arxiv_id=candidate.arxiv_id,
            doi=candidate.doi,
            recency_score=recency,
            relevance_score=recency,  # MVP: relevance = recency
            enriched_at=enriched_at,
        )

        # Persist tags and link them
        for tag_name in tags:
            tag = await self._tag_repo.get_or_create(tag_name)
            await self._paper_repo.add_tag(paper.id, tag.id)

        # Link researcher ↔ paper
        await self._researcher_repo.link_paper(researcher_id, paper.id)

        _logger.info(
            "scraper.paper_stored paper_id=%d arxiv_id=%s tags=%s title=%r",
            paper.id,
            paper.arxiv_id,
            tags,
            candidate.title[:60],
        )
        return 1, 0

    # ------------------------------------------------------------------
    # Chair-level helper: ensure researchers exist before scraping
    # ------------------------------------------------------------------

    async def ensure_researchers_for_chair(self, chair_id: int, professor_name: str) -> list[int]:
        """Return researcher IDs for *chair_id*, auto-creating from professor_name if empty."""
        researchers = await self._researcher_repo.list_by_chair(chair_id)
        if researchers:
            return [r.id for r in researchers]

        # MVP: bootstrap with the chair's professor as the sole researcher.
        # Strip leading academic titles so the stored name matches Scholar profiles.
        clean_name = re.sub(
            r"^\s*(?:(?:Professor|Prof)\.?\s*|Dr(?:\.-Ing\.)?\.?\s*)+",
            "",
            professor_name,
            flags=re.IGNORECASE,
        ).strip() or professor_name
        _logger.info(
            "No researchers found for chair_id=%d — auto-creating from professor_name=%r (clean=%r)",
            chair_id,
            professor_name,
            clean_name,
        )
        researcher = await self._researcher_repo.create(
            name=clean_name,
            chair_id=chair_id,
            is_professor=True,
        )
        await self._researcher_repo.commit()
        return [researcher.id]
