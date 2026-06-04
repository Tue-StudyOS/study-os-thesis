"""Celery tasks for the paper scraper pipeline."""

from __future__ import annotations

import logging
from typing import Any

from app.worker.celery_app import celery_app
from app.worker.task_runner import execute_task

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Task: scrape_chair_papers  (fan-out over researchers)
# ---------------------------------------------------------------------------


async def _scrape_chair_work(chair_id: int, settings: Any) -> dict:
    from app.chairs.repository import ChairRepository
    from app.db import SessionLocal
    from app.exceptions import NotFoundException
    from app.scraper.tasks import scrape_researcher_papers

    async with SessionLocal() as session:
        chair_repo = ChairRepository(session)
        chair = await chair_repo.get_by_id(chair_id)
        if chair is None:
            raise NotFoundException("Chair", chair_id)

        from app.papers.dedup import DeduplicationService
        from app.papers.repository import PaperRepository, TagRepository
        from app.researchers.repository import ResearcherRepository
        from app.scraper.adapters.arxiv_client import ArxivMetadataEnricher
        from app.scraper.adapters.llm_enricher import LLMPaperEnricher
        from app.scraper.adapters.ranker import RecencyPaperRanker
        from app.scraper.adapters.scholar_scraper import ScholarPlaywrightScraper
        from app.scraper.orchestrator import ScraperOrchestrator

        source = ScholarPlaywrightScraper(
            headless=settings.scraper_scholar_headless,
            request_delay=settings.scraper_scholar_delay,
            max_pages=settings.scraper_scholar_max_pages,
        )
        arxiv_enricher = ArxivMetadataEnricher(rate_limit_delay=settings.scraper_arxiv_delay)

        from app.llm.factory import build_chat_client

        llm_client = build_chat_client(settings)
        llm_enricher = LLMPaperEnricher(llm_client, settings.effective_enrichment_model)
        ranker = RecencyPaperRanker(half_life_days=settings.scraper_recency_half_life)

        paper_repo = PaperRepository(session)
        tag_repo = TagRepository(session)
        researcher_repo = ResearcherRepository(session)
        dedup = DeduplicationService(paper_repo)

        orchestrator = ScraperOrchestrator(
            source=source,
            arxiv_enricher=arxiv_enricher,
            llm_enricher=llm_enricher,
            ranker=ranker,
            dedup=dedup,
            paper_repo=paper_repo,
            tag_repo=tag_repo,
            researcher_repo=researcher_repo,
            max_results=settings.scraper_max_results,
            since_days=settings.scraper_since_days,
        )

        researcher_ids = await orchestrator.ensure_researchers_for_chair(chair_id, chair.professor_name)

    # Fan-out: dispatch one task per researcher
    dispatched = []
    for rid in researcher_ids:
        task_result = scrape_researcher_papers.delay(rid, chair_id, str(chair_id))
        dispatched.append({"researcher_id": rid, "celery_task_id": task_result.id})
        logger.info("scrape_chair: dispatched scrape_researcher for researcher_id=%d", rid)

    return {"chair_id": chair_id, "dispatched": dispatched}


@celery_app.task(
    bind=True,
    name="app.scraper.tasks.scrape_chair_papers",
    max_retries=2,
    default_retry_delay=60,
    soft_time_limit=120,
    time_limit=180,
)
def scrape_chair_papers(self: Any, chair_id: int, user_id: int, job_id: str) -> dict:
    """Resolve researchers for a chair and fan-out scraper tasks."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("scrape_chair_papers: chair_id=%d job_id=%s", chair_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _scrape_chair_work(chair_id, settings),
        success_event="scrape_chair_complete",
    )


# ---------------------------------------------------------------------------
# Task: scrape_researcher_papers  (full pipeline for one researcher)
# ---------------------------------------------------------------------------


async def _scrape_researcher_work(researcher_id: int, settings: Any) -> dict:
    from app.db import SessionLocal
    from app.llm.factory import build_chat_client
    from app.papers.dedup import DeduplicationService
    from app.papers.repository import PaperRepository, TagRepository
    from app.researchers.repository import ResearcherRepository
    from app.scraper.adapters.arxiv_client import ArxivMetadataEnricher
    from app.scraper.adapters.llm_enricher import LLMPaperEnricher
    from app.scraper.adapters.ranker import RecencyPaperRanker
    from app.scraper.adapters.scholar_scraper import ScholarPlaywrightScraper
    from app.scraper.orchestrator import ScraperOrchestrator

    async with SessionLocal() as session:
        source = ScholarPlaywrightScraper(
            headless=settings.scraper_scholar_headless,
            request_delay=settings.scraper_scholar_delay,
            max_pages=settings.scraper_scholar_max_pages,
        )
        arxiv_enricher = ArxivMetadataEnricher(rate_limit_delay=settings.scraper_arxiv_delay)
        llm_client = build_chat_client(settings)
        llm_enricher = LLMPaperEnricher(llm_client, settings.effective_enrichment_model)
        ranker = RecencyPaperRanker(half_life_days=settings.scraper_recency_half_life)

        paper_repo = PaperRepository(session)
        tag_repo = TagRepository(session)
        researcher_repo = ResearcherRepository(session)
        dedup = DeduplicationService(paper_repo)

        orchestrator = ScraperOrchestrator(
            source=source,
            arxiv_enricher=arxiv_enricher,
            llm_enricher=llm_enricher,
            ranker=ranker,
            dedup=dedup,
            paper_repo=paper_repo,
            tag_repo=tag_repo,
            researcher_repo=researcher_repo,
            max_results=settings.scraper_max_results,
            since_days=settings.scraper_since_days,
        )

        result = await orchestrator.scrape_for_researcher(researcher_id)
        await source.close()
        return result


@celery_app.task(
    bind=True,
    name="app.scraper.tasks.scrape_researcher_papers",
    max_retries=3,
    default_retry_delay=30,
    soft_time_limit=600,
    time_limit=660,
)
def scrape_researcher_papers(self: Any, researcher_id: int, user_id: int, job_id: str) -> dict:
    """Run the full scrape + enrich + store pipeline for one researcher."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("scrape_researcher_papers: researcher_id=%d job_id=%s", researcher_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _scrape_researcher_work(researcher_id, settings),
        success_event="scrape_researcher_complete",
    )


# ---------------------------------------------------------------------------
# Task: enrich_paper  (LLM summary + tags for a single paper, idempotent)
# ---------------------------------------------------------------------------


async def _enrich_paper_work(paper_id: int, force: bool, settings: Any) -> dict:
    from app.db import SessionLocal
    from app.exceptions import NotFoundException
    from app.llm.factory import build_chat_client
    from app.papers.repository import PaperRepository, TagRepository
    from app.scraper.adapters.llm_enricher import LLMPaperEnricher
    from datetime import datetime, timezone

    async with SessionLocal() as session:
        paper_repo = PaperRepository(session)
        tag_repo = TagRepository(session)

        paper = await paper_repo.get_by_id(paper_id)
        if paper is None:
            raise NotFoundException("Paper", paper_id)

        # Idempotency guard
        if paper.enriched_at is not None and not force:
            logger.info("enrich_paper: paper_id=%d already enriched — skipping", paper_id)
            return {"paper_id": paper_id, "skipped": True}

        if not paper.abstract:
            logger.info("enrich_paper: paper_id=%d has no abstract — cannot enrich", paper_id)
            return {"paper_id": paper_id, "skipped": True, "reason": "no_abstract"}

        llm_client = build_chat_client(settings)
        enricher = LLMPaperEnricher(llm_client, settings.effective_enrichment_model)

        summary = await enricher.summarize(paper.title, paper.abstract)
        tags = await enricher.generate_tags(paper.title, paper.abstract)

        await paper_repo.update(
            paper,
            summary=summary,
            enriched_at=datetime.now(timezone.utc),
        )

        for tag_name in tags:
            tag = await tag_repo.get_or_create(tag_name)
            await paper_repo.add_tag(paper.id, tag.id)

        await paper_repo.commit()
        logger.info("enrich_paper: paper_id=%d done tags=%s", paper_id, tags)
        return {"paper_id": paper_id, "tag_count": len(tags), "summary_len": len(summary)}


@celery_app.task(
    bind=True,
    name="app.scraper.tasks.enrich_paper",
    max_retries=3,
    default_retry_delay=30,
    soft_time_limit=120,
    time_limit=180,
)
def enrich_paper(self: Any, paper_id: int, user_id: int, job_id: str, force: bool = False) -> dict:
    """LLM-enrich a single paper (summary + tags). Idempotent unless force=True."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("enrich_paper: paper_id=%d force=%s job_id=%s", paper_id, force, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _enrich_paper_work(paper_id, force, settings),
        success_event="enrich_paper_complete",
    )
