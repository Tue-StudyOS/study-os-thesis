"""Celery task: compute_skills.

Triggered automatically after parse_transcript succeeds (chained in
students/tasks.py) or manually via POST /api/students/me/skills/recompute.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from app.exceptions import NotFoundException
from app.worker.celery_app import celery_app
from app.worker.task_runner import execute_task

logger = logging.getLogger(__name__)


async def _compute_skills_work(
    user_id: int,
    job_id: str,
    settings: Any,
) -> dict:
    from app.db import SessionLocal
    from app.handbook.repository import HandbookRepository
    from app.llm.factory import build_chat_client, build_embed_client
    from app.models.skill import SkillComputationRun
    from app.skills.repository import SkillRepository
    from app.skills.service import SkillComputationService
    from app.students.repository import StudentRepository

    async with SessionLocal() as session:
        # Create the computation run record
        run = SkillComputationRun(
            user_id=user_id,
            job_id=uuid.UUID(job_id),
            status="running",
        )
        session.add(run)
        await session.flush()

        # Build all dependencies
        skill_repo = SkillRepository(session)
        handbook_repo = HandbookRepository(session)
        student_repo = StudentRepository(session)
        embed_client = build_embed_client(settings)
        llm_client = build_chat_client(settings)

        svc = SkillComputationService(
            skill_repo=skill_repo,
            handbook_repo=handbook_repo,
            student_repo=student_repo,
            embed_client=embed_client,
            llm_client=llm_client,
            settings=settings,
        )

        result = await svc.compute_skills(user_id=user_id, run=run)
        await session.commit()

    return {
        "computation_run_id": str(result.computation_run_id),
        "skills_count": result.skills_count,
        "matched_courses": result.matched_courses,
        "unmatched_courses": result.unmatched_courses,
        "warnings": result.warnings,
        "status": result.status,
    }


@celery_app.task(
    bind=True,
    name="app.skills.tasks.compute_skills",
    max_retries=2,
    default_retry_delay=60,
    soft_time_limit=300,
    time_limit=360,
)
def compute_skills(self: Any, user_id: int, job_id: str) -> dict:
    """Compute and persist weighted skill scores for a student."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("compute_skills: user_id=%d job_id=%s", user_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _compute_skills_work(user_id, job_id, settings),
        success_event="skills_computed",
        started_event="skills_computing",
        permanent_exceptions=(NotFoundException,),
    )
