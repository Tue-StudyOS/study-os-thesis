"""Celery tasks for handbook ingestion."""

from __future__ import annotations

import logging
from typing import Any

from app.exceptions import BadRequestException
from app.worker.celery_app import celery_app
from app.worker.task_runner import execute_task

logger = logging.getLogger(__name__)


async def _ingest_handbook_work(
    job_id: str,
    university_id: str,
    handbook_version: str,
    settings: Any,
) -> dict:
    from app.db import SessionLocal
    from app.handbook.pdf_store import delete_handbook_pdf, fetch_handbook_pdf
    from app.handbook.repository import HandbookRepository
    from app.handbook.service import HandbookService
    from app.llm.factory import build_chat_client

    pdf_bytes = await fetch_handbook_pdf(settings.redis_url, job_id)
    if not pdf_bytes:
        raise BadRequestException(
            "Handbook PDF was not found in temporary storage (it may have expired)."
        )

    async with SessionLocal() as session:
        repo = HandbookRepository(session)
        llm = build_chat_client(settings)
        svc = HandbookService(repo, llm, settings)
        result = await svc.ingest_pdf(pdf_bytes, university_id, handbook_version)

    await delete_handbook_pdf(settings.redis_url, job_id)
    return result.model_dump()


@celery_app.task(
    bind=True,
    name="app.handbook.tasks.ingest_handbook",
    max_retries=2,
    default_retry_delay=60,
    soft_time_limit=1800,
    time_limit=1860,
)
def ingest_handbook(
    self: Any,
    job_id: str,
    university_id: str,
    handbook_version: str,
) -> dict:
    """Parse a Modulhandbuch PDF and persist all module entries to the DB."""
    from app.config import get_settings

    settings = get_settings()
    logger.info(
        "ingest_handbook: job_id=%s university=%s version=%s",
        job_id,
        university_id,
        handbook_version,
    )

    return execute_task(
        self,
        job_id=job_id,
        user_id=0,  # admin action, no user_id required by execute_task bookkeeping
        redis_url=settings.redis_url,
        work=lambda: _ingest_handbook_work(job_id, university_id, handbook_version, settings),
        success_event="handbook_ingested",
        permanent_exceptions=(BadRequestException,),
    )
