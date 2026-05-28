"""Celery tasks for thesis-related background work."""

from __future__ import annotations

import logging
import traceback
from typing import Any

from app.exceptions import NotFoundException
from app.worker.celery_app import celery_app
from app.worker.publisher import publish_event
from app.worker.utils import run_async

logger = logging.getLogger(__name__)


def _get_deps() -> tuple[Any, Any]:
    """Build service and job-service instances for use inside a task.

    Lazy imports avoid circular dependencies and ensure each forked
    worker process initialises its own DB connections.
    """
    from app.config import get_settings
    from app.db import SessionLocal
    from app.jobs.repository import JobRepository
    from app.jobs.service import JobService
    from app.llm.factory import build_embed_client
    from app.theses.repository import ThesisRepository
    from app.theses.service import ThesisService
    from app.users.repository import UserRepository

    settings = get_settings()

    async def _build():
        session = SessionLocal()
        thesis_repo = ThesisRepository(session)
        user_repo = UserRepository(session)
        embed_client = build_embed_client(settings)
        svc = ThesisService(thesis_repo, user_repo, embed_client, settings)
        job_repo = JobRepository(session)
        job_svc = JobService(job_repo)
        return svc, job_svc

    return run_async(_build())


@celery_app.task(
    bind=True,
    name="app.theses.tasks.embed_thesis",
    max_retries=3,
    default_retry_delay=60,
    soft_time_limit=120,
    time_limit=180,
)
def embed_thesis(self: Any, thesis_id: int, user_id: int, job_id: str) -> dict:
    """Generate and store the embedding for a thesis."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("embed_thesis: thesis_id=%d job_id=%s", thesis_id, job_id)

    try:
        svc, job_svc = _get_deps()
    except Exception:
        logger.exception("Failed to build dependencies for embed_thesis")
        publish_event(
            settings.redis_url,
            event_type="task_failed",
            job_id=job_id,
            user_id=user_id,
            status="failure",
            data={"error": "Internal dependency error"},
        )
        raise

    async def _inner():
        from app.db import SessionLocal
        from app.llm.factory import build_embed_client
        from app.theses.repository import ThesisRepository

        async with SessionLocal() as session:
            repo = ThesisRepository(session)
            thesis = await repo.get_by_id(thesis_id)
            if thesis is None:
                raise NotFoundException("Thesis", thesis_id)

            embed_client = build_embed_client(get_settings())
            embedding = await embed_client.embed(
                settings.ollama_embed_model,
                f"{thesis.title}\n\n{thesis.abstract}",
            )
            thesis.embedding = embedding
            await session.commit()
            return {"thesis_id": thesis_id, "dim": len(embedding)}

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
    except NotFoundException:
        publish_event(
            settings.redis_url,
            event_type="task_failed",
            job_id=job_id,
            user_id=user_id,
            status="failure",
            data={"error": f"Thesis {thesis_id} not found"},
        )
        raise
    except (ConnectionError, TimeoutError, OSError) as exc:
        publish_event(
            settings.redis_url,
            event_type="task_failed",
            job_id=job_id,
            user_id=user_id,
            status="retry",
            data={"error": str(exc)},
        )
        raise self.retry(exc=exc)
    except Exception as exc:
        publish_event(
            settings.redis_url,
            event_type="task_failed",
            job_id=job_id,
            user_id=user_id,
            status="failure",
            data={"error": traceback.format_exc()[:500]},
        )
        raise
