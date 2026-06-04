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


async def _scrape_chair_work(chair_id: int, user_id: int, settings: Any) -> dict:
    from app.chairs.repository import ChairRepository
    from app.db import SessionLocal
    from app.exceptions import NotFoundException
    from app.jobs.repository import JobRepository
    from app.models.job import JobType
    from app.papers.dedup import DeduplicationService
    from app.papers.repository import PaperRepository, TagRepository
    from app.researchers.repository import ResearcherRepository
    from app.scraper.adapters.arxiv_client import ArxivMetadataEnricher
    from app.scraper.adapters.llm_enricher import LLMPaperEnricher
    from app.scraper.adapters.ranker import RecencyPaperRanker
    from app.scraper.adapters.scholar_scraper import ScholarPlaywrightScraper
    from app.scraper.orchestrator import ScraperOrchestrator
    from app.llm.factory import build_chat_client

    # Step 1: resolve researcher IDs (auto-creates from professor_name if table is empty)
    async with SessionLocal() as session:
        chair_repo = ChairRepository(session)
        chair = await chair_repo.get_by_id(chair_id)
        if chair is None:
            raise NotFoundException("Chair", chair_id)

        source = ScholarPlaywrightScraper(
            headless=settings.scraper_scholar_headless,
            request_delay=settings.scraper_scholar_delay,
            max_pages=settings.scraper_scholar_max_pages,
        )
        arxiv_enricher = ArxivMetadataEnricher(
            redis_url=settings.redis_url,
            rate_limit_delay=settings.scraper_arxiv_delay,
            batch_size=settings.scraper_arxiv_batch_size,
        )
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

    # Step 2: fan-out — create a Job row for each researcher task so it is
    # trackable via GET /api/jobs, then dispatch the Celery task.
    dispatched = []
    async with SessionLocal() as session:
        job_repo = JobRepository(session)
        for rid in researcher_ids:
            job = await job_repo.create(
                type=JobType.scrape_researcher,
                user_id=user_id,
                input_data={"researcher_id": rid, "chair_id": chair_id},
            )
            await session.commit()

            task_result = scrape_researcher_papers.delay(rid, user_id, str(job.id))

            # Back-patch the celery task ID onto the job row
            job = await job_repo.get_by_id(job.id)
            if job is not None:
                job.celery_task_id = task_result.id
                await session.commit()

            dispatched.append({"researcher_id": rid, "job_id": str(job.id), "celery_task_id": task_result.id})
            logger.info(
                "scrape_chair: dispatched scrape_researcher researcher_id=%d job_id=%s",
                rid,
                job.id,
            )

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
        work=lambda: _scrape_chair_work(chair_id, user_id, settings),
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
        arxiv_enricher = ArxivMetadataEnricher(
            redis_url=settings.redis_url,
            rate_limit_delay=settings.scraper_arxiv_delay,
            batch_size=settings.scraper_arxiv_batch_size,
        )
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


# ---------------------------------------------------------------------------
# Task: scrape_all_chairs  (Celery Beat periodic trigger)
# ---------------------------------------------------------------------------


async def _scrape_all_chairs_work() -> dict:
    """Dispatch scrape_chair_papers for every chair in the DB.

    Used by Celery Beat for scheduled runs. Creates Job rows attributed to the
    first admin user found in the DB (the system actor for automated runs).
    """
    from app.chairs.repository import ChairRepository
    from app.db import SessionLocal
    from app.jobs.repository import JobRepository
    from app.models.job import JobType
    from app.models.user import UserRole
    from sqlalchemy import select
    from app.models.user import User

    async with SessionLocal() as session:
        # Find a system actor — first admin user, falling back to user id=1
        admin = await session.scalar(select(User).where(User.role == UserRole.admin).limit(1))
        system_user_id: int = admin.id if admin is not None else 1

        chair_repo = ChairRepository(session)
        chairs = await chair_repo.list()

        if not chairs:
            logger.info("scrape_all_chairs: no chairs found — nothing to do")
            return {"dispatched": 0}

        job_repo = JobRepository(session)
        dispatched = 0
        for chair in chairs:
            job = await job_repo.create(
                type=JobType.scrape_chair,
                user_id=system_user_id,
                input_data={"chair_id": chair.id, "triggered_by": "beat"},
            )
            await session.commit()

            task_result = scrape_chair_papers.delay(chair.id, system_user_id, str(job.id))

            job = await job_repo.get_by_id(job.id)
            if job is not None:
                job.celery_task_id = task_result.id
                await session.commit()

            dispatched += 1
            logger.info(
                "scrape_all_chairs: dispatched chair_id=%d job_id=%s celery_task_id=%s",
                chair.id,
                job.id,
                task_result.id,
            )

    return {"dispatched": dispatched}


@celery_app.task(
    name="app.scraper.tasks.scrape_all_chairs",
    # No retries — Beat will re-run on the next schedule if this fails
    max_retries=0,
    soft_time_limit=120,
    time_limit=180,
)
def scrape_all_chairs() -> dict:
    """Celery Beat entry point: kick off paper scraping for every chair.

    Configured in celery_config.py beat_schedule. Runs weekly by default.
    """
    from app.worker.utils import run_async

    logger.info("scrape_all_chairs: periodic trigger fired")
    return run_async(_scrape_all_chairs_work())


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


# ---------------------------------------------------------------------------
# Task: ingest_single_paper  (fetch + enrich + store one arXiv paper)
# ---------------------------------------------------------------------------


async def _ingest_single_paper_work(
    arxiv_id: str,
    researcher_id: int | None,
    settings: Any,
) -> dict:
    """Fetch one arXiv paper, run LLM enrichment, dedup, and persist."""
    from datetime import datetime, timezone

    from app.db import SessionLocal
    from app.llm.factory import build_chat_client
    from app.papers.dedup import DeduplicationService
    from app.papers.domain import PaperCandidate
    from app.papers.repository import PaperRepository, TagRepository
    from app.researchers.repository import ResearcherRepository
    from app.scraper.adapters.arxiv_client import ArxivMetadataEnricher
    from app.scraper.adapters.llm_enricher import LLMPaperEnricher
    from app.scraper.adapters.ranker import RecencyPaperRanker

    arxiv_enricher = ArxivMetadataEnricher(
        redis_url=settings.redis_url,
        rate_limit_delay=settings.scraper_arxiv_delay,
        batch_size=settings.scraper_arxiv_batch_size,
    )
    ranker = RecencyPaperRanker(half_life_days=settings.scraper_recency_half_life)

    # Seed a minimal candidate so the arXiv enricher has an ID to work with
    candidate = PaperCandidate(
        title="",
        source="arxiv",
        source_url=f"https://arxiv.org/abs/{arxiv_id}",
        arxiv_id=arxiv_id,
    )
    candidate = await arxiv_enricher.enrich(candidate)

    if not candidate.title:
        raise ValueError(f"arXiv paper '{arxiv_id}' not found or returned no title")

    async with SessionLocal() as session:
        paper_repo = PaperRepository(session)
        tag_repo = TagRepository(session)
        researcher_repo = ResearcherRepository(session)
        dedup = DeduplicationService(paper_repo)

        # Dedup check — return existing paper_id if already stored
        existing = await dedup.find_duplicate(candidate)
        if existing is not None:
            await dedup.merge_metadata(existing, candidate)
            if researcher_id is not None:
                await researcher_repo.link_paper(researcher_id, existing.id)
            await paper_repo.commit()
            logger.info("ingest_single_paper: arxiv_id=%s already exists as paper_id=%d", arxiv_id, existing.id)
            return {"paper_id": existing.id, "arxiv_id": arxiv_id, "created": False}

        # LLM enrichment
        summary: str | None = None
        tags: list[str] = []
        enriched_at: datetime | None = None
        if candidate.abstract:
            llm_client = build_chat_client(settings)
            enricher = LLMPaperEnricher(llm_client, settings.effective_enrichment_model)
            summary = await enricher.summarize(candidate.title, candidate.abstract)
            tags = await enricher.generate_tags(candidate.title, candidate.abstract)
            enriched_at = datetime.now(timezone.utc)

        recency = ranker.compute_recency_score(candidate.publication_date)

        paper = await paper_repo.create(
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
            relevance_score=recency,
            enriched_at=enriched_at,
        )

        for tag_name in tags:
            tag = await tag_repo.get_or_create(tag_name)
            await paper_repo.add_tag(paper.id, tag.id)

        if researcher_id is not None:
            await researcher_repo.link_paper(researcher_id, paper.id)

        await paper_repo.commit()

    logger.info("ingest_single_paper: stored paper_id=%d arxiv_id=%s tags=%s", paper.id, arxiv_id, tags)
    return {"paper_id": paper.id, "arxiv_id": arxiv_id, "created": True}


@celery_app.task(
    bind=True,
    name="app.scraper.tasks.ingest_single_paper",
    max_retries=3,
    default_retry_delay=30,
    soft_time_limit=180,
    time_limit=240,
)
def ingest_single_paper(
    self: Any,
    arxiv_id: str,
    researcher_id: int | None,
    user_id: int,
    job_id: str,
) -> dict:
    """Fetch, enrich, and store a single arXiv paper by ID."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("ingest_single_paper: arxiv_id=%s job_id=%s", arxiv_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _ingest_single_paper_work(arxiv_id, researcher_id, settings),
        success_event="ingest_paper_complete",
    )
