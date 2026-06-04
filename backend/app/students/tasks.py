"""Celery tasks for student-related background work."""

from __future__ import annotations

import logging
import os
from typing import Any

from app.exceptions import BadRequestException, NotFoundException
from app.worker.celery_app import celery_app
from app.worker.task_runner import execute_task

logger = logging.getLogger(__name__)

# Transcript extraction runs a large LLM and can be slow on local/CPU setups.
# Limits are read from the environment so they can be raised on slow machines.
# The soft limit is the effective ceiling: the task is interrupted with
# SoftTimeLimitExceeded and the job is marked `failure` cleanly (see task_runner).
# Keep the frontend poll budget (Dashboard) >= the hard limit below.
_SOFT_TIME_LIMIT = int(os.getenv("TRANSCRIPT_SOFT_TIME_LIMIT", "1800"))
_HARD_TIME_LIMIT = int(os.getenv("TRANSCRIPT_HARD_TIME_LIMIT", "1860"))


async def _parse_transcript_work(
    user_id: int,
    job_id: str,
    settings: Any,
    program: str | None,
    semester: int | None,
) -> dict:
    from app.db import SessionLocal
    from app.jobs.repository import JobRepository
    from app.jobs.service import JobService
    from app.llm.factory import build_chat_client, build_embed_client
    from app.models.job import JobType
    from app.students.pdf_store import delete_pdf, fetch_pdf
    from app.students.repository import StudentRepository
    from app.students.service import StudentService

    pdf_bytes = await fetch_pdf(settings.redis_url, job_id)
    if not pdf_bytes:
        raise BadRequestException("Transcript PDF was not found in temporary storage (it may have expired).")

    async with SessionLocal() as session:
        repo = StudentRepository(session)
        chat_client = build_chat_client(settings)
        embed_client = build_embed_client(settings)
        svc = StudentService(repo, chat_client, embed_client, settings)
        student = await svc.upload_transcript(user_id, pdf_bytes, program=program, semester=semester)

    await delete_pdf(settings.redis_url, job_id)

    courses_count = len(student.courses) if student.courses else 0

    # Chain: automatically compute skill scores after the transcript is persisted.
    try:
        from app.skills.tasks import compute_skills as _compute_skills_task

        async with SessionLocal() as session:
            job_svc = JobService(JobRepository(session))
            skill_job = await job_svc.create_job(
                type=JobType.compute_skills,
                user_id=user_id,
                input_data={"triggered_by_job": job_id},
            )
            await session.commit()

        task_result = _compute_skills_task.delay(
            user_id=user_id,
            job_id=str(skill_job.id),
        )
        async with SessionLocal() as session:
            job_svc = JobService(JobRepository(session))
            await job_svc.set_celery_task_id(skill_job.id, task_result.id)
            await session.commit()

        logger.info(
            "parse_transcript: chained compute_skills skill_job_id=%s celery_id=%s",
            skill_job.id,
            task_result.id,
        )
        skill_job_id = str(skill_job.id)
    except Exception as exc:
        logger.warning("parse_transcript: failed to chain compute_skills: %s", exc)
        skill_job_id = None

    return {
        "user_id": user_id,
        "courses": courses_count,
        "skill_job_id": skill_job_id,
    }


@celery_app.task(
    bind=True,
    name="app.students.tasks.parse_transcript",
    max_retries=3,
    default_retry_delay=120,
    soft_time_limit=_SOFT_TIME_LIMIT,
    time_limit=_HARD_TIME_LIMIT,
)
def parse_transcript(
    self: Any,
    user_id: int,
    job_id: str,
    program: str | None = None,
    semester: int | None = None,
) -> dict:
    """Parse a transcript PDF, extract courses via LLM, compute GPA, embed profile."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("parse_transcript: user_id=%d job_id=%s", user_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _parse_transcript_work(user_id, job_id, settings, program, semester),
        started_event="transcript_parsing",
        success_event="transcript_parsed",
        permanent_exceptions=(NotFoundException, BadRequestException),
    )
