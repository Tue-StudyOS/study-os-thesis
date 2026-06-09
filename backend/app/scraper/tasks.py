"""Celery tasks for the paper scraper pipeline."""

from __future__ import annotations

import logging
from typing import Any

from app.scraper.constants.tasks import (
    DISCOVER_CHAIR_EMPLOYEES_COMPLETE_EVENT,
    DISCOVER_CHAIR_EMPLOYEES_DEFAULT_RETRY_DELAY_SECONDS,
    DISCOVER_CHAIR_EMPLOYEES_MAX_RETRIES,
    DISCOVER_CHAIR_EMPLOYEES_SOFT_TIME_LIMIT_SECONDS,
    DISCOVER_CHAIR_EMPLOYEES_TASK_NAME,
    DISCOVER_CHAIR_EMPLOYEES_TIME_LIMIT_SECONDS,
    ENRICH_PAPER_COMPLETE_EVENT,
    ENRICH_PAPER_DEFAULT_RETRY_DELAY_SECONDS,
    ENRICH_PAPER_MAX_RETRIES,
    ENRICH_PAPER_SOFT_TIME_LIMIT_SECONDS,
    ENRICH_PAPER_TASK_NAME,
    ENRICH_PAPER_TIME_LIMIT_SECONDS,
    SCRAPE_ALL_CHAIRS_ADMIN_LOOKUP_LIMIT,
    SCRAPE_ALL_CHAIRS_FALLBACK_USER_ID,
    SCRAPE_ALL_CHAIRS_MAX_RETRIES,
    SCRAPE_ALL_CHAIRS_SOFT_TIME_LIMIT_SECONDS,
    SCRAPE_ALL_CHAIRS_TASK_NAME,
    SCRAPE_ALL_CHAIRS_TIME_LIMIT_SECONDS,
    SCRAPE_ALL_CHAIRS_TRIGGER,
    SCRAPE_CHAIR_COMPLETE_EVENT,
    SCRAPE_CHAIR_DEFAULT_RETRY_DELAY_SECONDS,
    SCRAPE_CHAIR_MAX_RETRIES,
    SCRAPE_CHAIR_SOFT_TIME_LIMIT_SECONDS,
    SCRAPE_CHAIR_TASK_NAME,
    SCRAPE_CHAIR_TIME_LIMIT_SECONDS,
    SCRAPE_RESEARCHER_COMPLETE_EVENT,
    SCRAPE_RESEARCHER_DEFAULT_RETRY_DELAY_SECONDS,
    SCRAPE_RESEARCHER_MAX_RETRIES,
    SCRAPE_RESEARCHER_SOFT_TIME_LIMIT_SECONDS,
    SCRAPE_RESEARCHER_TASK_NAME,
    SCRAPE_RESEARCHER_TIME_LIMIT_SECONDS,
)
from app.worker.celery_app import celery_app
from app.worker.task_runner import execute_task

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Task: scrape_chair_papers  (fan-out over researchers)
# ---------------------------------------------------------------------------


async def _scrape_chair_work(
    chair_id: int,
    user_id: int,
    settings: Any,
    max_results: int | None = None,
    since_days: int | None = None,
) -> dict:
    from app.chairs.repository import ChairRepository
    from app.db import SessionLocal
    from app.exceptions import NotFoundException
    from app.jobs.repository import JobRepository
    from app.models.job import JobType
    from app.scraper.pipeline import build_scraper_pipeline

    # Step 1: resolve researcher IDs (auto-creates from professor_name if table is empty)
    async with SessionLocal() as session:
        chair_repo = ChairRepository(session)
        chair = await chair_repo.get_by_id(chair_id)
        if chair is None:
            raise NotFoundException("Chair", chair_id)

        pipeline = build_scraper_pipeline(
            session,
            settings,
            max_results=max_results,
            since_days=since_days,
        )
        try:
            researcher_ids = await pipeline.orchestrator.ensure_researchers_for_chair(chair_id, chair.professor_name)
        finally:
            await pipeline.source.close()

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
            task_result = scrape_researcher_papers.delay(rid, user_id, str(job.id), max_results, since_days)
            job = await job_repo.update(job, celery_task_id=task_result.id)

            dispatched.append({"researcher_id": rid, "job_id": str(job.id), "celery_task_id": task_result.id})
            logger.info(
                "scrape_chair: dispatched scrape_researcher researcher_id=%d job_id=%s",
                rid,
                job.id,
            )

    return {"chair_id": chair_id, "dispatched": dispatched}


@celery_app.task(
    bind=True,
    name=SCRAPE_CHAIR_TASK_NAME,
    max_retries=SCRAPE_CHAIR_MAX_RETRIES,
    default_retry_delay=SCRAPE_CHAIR_DEFAULT_RETRY_DELAY_SECONDS,
    soft_time_limit=SCRAPE_CHAIR_SOFT_TIME_LIMIT_SECONDS,
    time_limit=SCRAPE_CHAIR_TIME_LIMIT_SECONDS,
)
def scrape_chair_papers(
    self: Any,
    chair_id: int,
    user_id: int,
    job_id: str,
    max_results: int | None = None,
    since_days: int | None = None,
) -> dict:
    """Resolve researchers for a chair and fan-out scraper tasks."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("scrape_chair_papers: chair_id=%d job_id=%s", chair_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _scrape_chair_work(chair_id, user_id, settings, max_results, since_days),
        success_event=SCRAPE_CHAIR_COMPLETE_EVENT,
    )


# ---------------------------------------------------------------------------
# Task: scrape_researcher_papers  (full pipeline for one researcher)
# ---------------------------------------------------------------------------


async def _scrape_researcher_work(
    researcher_id: int,
    settings: Any,
    max_results: int | None = None,
    since_days: int | None = None,
) -> dict:
    from app.db import SessionLocal
    from app.scraper.pipeline import build_scraper_pipeline

    async with SessionLocal() as session:
        pipeline = build_scraper_pipeline(
            session,
            settings,
            max_results=max_results,
            since_days=since_days,
        )
        try:
            return await pipeline.orchestrator.scrape_for_researcher(researcher_id)
        finally:
            await pipeline.source.close()


@celery_app.task(
    bind=True,
    name=SCRAPE_RESEARCHER_TASK_NAME,
    max_retries=SCRAPE_RESEARCHER_MAX_RETRIES,
    default_retry_delay=SCRAPE_RESEARCHER_DEFAULT_RETRY_DELAY_SECONDS,
    soft_time_limit=SCRAPE_RESEARCHER_SOFT_TIME_LIMIT_SECONDS,
    time_limit=SCRAPE_RESEARCHER_TIME_LIMIT_SECONDS,
)
def scrape_researcher_papers(
    self: Any,
    researcher_id: int,
    user_id: int,
    job_id: str,
    max_results: int | None = None,
    since_days: int | None = None,
) -> dict:
    """Run the full scrape + enrich + store pipeline for one researcher."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("scrape_researcher_papers: researcher_id=%d job_id=%s", researcher_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _scrape_researcher_work(researcher_id, settings, max_results, since_days),
        success_event=SCRAPE_RESEARCHER_COMPLETE_EVENT,
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
        admin = await session.scalar(select(User).where(User.role == UserRole.admin).limit(SCRAPE_ALL_CHAIRS_ADMIN_LOOKUP_LIMIT))
        system_user_id: int = admin.id if admin is not None else SCRAPE_ALL_CHAIRS_FALLBACK_USER_ID

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
                input_data={"chair_id": chair.id, "triggered_by": SCRAPE_ALL_CHAIRS_TRIGGER},
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
    name=SCRAPE_ALL_CHAIRS_TASK_NAME,
    # No retries — Beat will re-run on the next schedule if this fails
    max_retries=SCRAPE_ALL_CHAIRS_MAX_RETRIES,
    soft_time_limit=SCRAPE_ALL_CHAIRS_SOFT_TIME_LIMIT_SECONDS,
    time_limit=SCRAPE_ALL_CHAIRS_TIME_LIMIT_SECONDS,
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
    name=ENRICH_PAPER_TASK_NAME,
    max_retries=ENRICH_PAPER_MAX_RETRIES,
    default_retry_delay=ENRICH_PAPER_DEFAULT_RETRY_DELAY_SECONDS,
    soft_time_limit=ENRICH_PAPER_SOFT_TIME_LIMIT_SECONDS,
    time_limit=ENRICH_PAPER_TIME_LIMIT_SECONDS,
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
        success_event=ENRICH_PAPER_COMPLETE_EVENT,
    )


# ---------------------------------------------------------------------------
# Task: discover_chair_employees  (find team members on chair website)
# ---------------------------------------------------------------------------


async def _discover_chair_employees_work(
    chair_id: int,
    user_id: int,
    llm_port: Any = None,
    chair_repo: Any = None,
    researcher_service: Any = None,
    settings: Any = None,
) -> dict:
    """Discover researchers from a chair website and upsert them."""
    from app.chairs.repository import ChairRepository
    from app.db import SessionLocal
    from app.exceptions import NotFoundException
    from app.researchers.schemas import ResearcherCreate
    from app.researchers.service import ResearcherService
    from app.scraper.adapters.chair_discovery import ChairDiscoveryAdapter

    async with SessionLocal() as session:
        if chair_repo is None:
            chair_repo = ChairRepository(session)
        if researcher_service is None:
            researcher_service = ResearcherService(session)
        if llm_port is None:
            from app.llm.factory import build_chat_client

            if settings is None:
                from app.config import get_settings

                settings = get_settings()
            llm_port = build_chat_client(settings)

        chair = await chair_repo.get_by_id(chair_id)
        if chair is None:
            raise NotFoundException("Chair", chair_id)

        if not chair.website_url:
            logger.warning("discover_chair_employees: chair_id=%d has no website_url", chair_id)
            return {"chair_id": chair_id, "discovered": 0, "error": "no_website_url"}

        adapter = ChairDiscoveryAdapter(llm_port=llm_port)

        try:
            researchers = await adapter.discover_researchers(chair.website_url)
        except Exception as e:
            logger.error("discover_chair_employees: adapter failed for chair_id=%d: %s", chair_id, e)
            return {"chair_id": chair_id, "discovered": 0, "error": str(e)}

        discovered = 0
        updated = 0
        for researcher_info in researchers:
            try:
                data = ResearcherCreate(
                    name=researcher_info.name,
                    chair_id=chair_id,
                    title=researcher_info.title,
                    role=researcher_info.role,
                    email=researcher_info.email,
                    profile_url=researcher_info.profile_url,
                    source_url=researcher_info.source_url,
                )
                result = await researcher_service.upsert_researcher(data)
                if result.id is not None:
                    discovered += 1
                logger.info("discover_chair_employees: upserted researcher_id=%d chair_id=%d", result.id, chair_id)
            except Exception as e:
                logger.error("discover_chair_employees: upsert failed for %s in chair_id=%d: %s", researcher_info.name, chair_id, e)
                continue

        return {
            "chair_id": chair_id,
            "discovered": discovered,
            "updated": updated,
        }


@celery_app.task(
    bind=True,
    name=DISCOVER_CHAIR_EMPLOYEES_TASK_NAME,
    max_retries=DISCOVER_CHAIR_EMPLOYEES_MAX_RETRIES,
    default_retry_delay=DISCOVER_CHAIR_EMPLOYEES_DEFAULT_RETRY_DELAY_SECONDS,
    soft_time_limit=DISCOVER_CHAIR_EMPLOYEES_SOFT_TIME_LIMIT_SECONDS,
    time_limit=DISCOVER_CHAIR_EMPLOYEES_TIME_LIMIT_SECONDS,
)
def discover_chair_employees(self: Any, chair_id: int, user_id: int, job_id: str) -> dict:
    """Discover and upsert team members from a chair's website."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("discover_chair_employees: chair_id=%d job_id=%s", chair_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _discover_chair_employees_work(chair_id, user_id, settings=settings),
        success_event=DISCOVER_CHAIR_EMPLOYEES_COMPLETE_EVENT,
    )
