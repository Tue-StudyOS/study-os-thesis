"""Celery tasks for student-related background work."""

from __future__ import annotations

import logging
import traceback
from typing import Any

from app.worker.celery_app import celery_app
from app.worker.publisher import publish_event
from app.worker.utils import run_async

logger = logging.getLogger(__name__)


def _get_deps() -> tuple[Any, Any]:
    """Build service and job-service instances for use inside a task."""
    from app.config import get_settings
    from app.db import SessionLocal
    from app.jobs.repository import JobRepository
    from app.jobs.service import JobService
    from app.llm.factory import build_chat_client, build_embed_client
    from app.students.repository import StudentRepository
    from app.students.service import StudentService

    settings = get_settings()

    async def _build():
        session = SessionLocal()
        repo = StudentRepository(session)
        chat_client = build_chat_client(settings)
        embed_client = build_embed_client(settings)
        svc = StudentService(repo, chat_client, embed_client, settings)
        job_repo = JobRepository(session)
        job_svc = JobService(job_repo)
        return svc, job_svc

    return run_async(_build())


@celery_app.task(
    bind=True,
    name="app.students.tasks.parse_transcript",
    max_retries=3,
    default_retry_delay=120,
    soft_time_limit=300,
    time_limit=360,
)
def parse_transcript(
    self: Any,
    user_id: int,
    pdf_bytes_ref: str,
    job_id: str,
    program: str | None = None,
    semester: int | None = None,
) -> dict:
    """Parse a transcript PDF, extract courses via LLM, compute GPA, embed profile."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("parse_transcript: user_id=%d job_id=%s", user_id, job_id)

    async def _inner():
        from app.db import SessionLocal
        from app.llm.factory import build_chat_client, build_embed_client
        from app.students.repository import StudentRepository
        from app.students.service import StudentService

        # In a real implementation, pdf_bytes_ref would reference stored bytes.
        # For now we pass it through directly if it's bytes-like.
        async with SessionLocal() as session:
            repo = StudentRepository(session)
            chat_client = build_chat_client(settings)
            embed_client = build_embed_client(settings)
            svc = StudentService(repo, chat_client, embed_client, settings)
            # The PDF bytes would be retrieved from a storage backend here
            # For now this is a placeholder
            student = await svc.upload_transcript(
                user_id, b"", program=program, semester=semester
            )
            return {"user_id": user_id, "courses": len(student.courses) if student.courses else 0}

    try:
        result = run_async(_inner())
        publish_event(
            settings.redis_url,
            event_type="task_complete",
            job_id=job_id,
            user_id=user_id,
            status="success",
            data=result,
        )
        return result
    except (ConnectionError, TimeoutError, OSError) as exc:
        publish_event(
            settings.redis_url,
            event_type="task_failed",
            job_id=job_id,
            user_id=user_id,
            status="retry",
        )
        raise self.retry(exc=exc)
    except Exception:
        publish_event(
            settings.redis_url,
            event_type="task_failed",
            job_id=job_id,
            user_id=user_id,
            status="failure",
            data={"error": traceback.format_exc()[:500]},
        )
        raise
