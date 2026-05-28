"""Celery tasks for chair-related background work."""

from __future__ import annotations

import logging
import traceback
from typing import Any

from app.exceptions import AlreadyExistsException, NotFoundException
from app.worker.celery_app import celery_app
from app.worker.publisher import publish_event
from app.worker.utils import run_async

logger = logging.getLogger(__name__)


def _get_deps() -> tuple[Any, Any]:
    """Build service and job-service instances for use inside a task."""
    from app.config import get_settings
    from app.db import SessionLocal
    from app.chairs.repository import ChairRepository
    from app.chairs.service import ChairService
    from app.jobs.repository import JobRepository
    from app.jobs.service import JobService
    from app.llm.factory import build_embed_client

    settings = get_settings()

    async def _build():
        session = SessionLocal()
        chair_repo = ChairRepository(session)
        embed_client = build_embed_client(settings)
        svc = ChairService(chair_repo, embed_client, settings)
        job_repo = JobRepository(session)
        job_svc = JobService(job_repo)
        return svc, job_svc

    return run_async(_build())


@celery_app.task(
    bind=True,
    name="app.chairs.tasks.ingest_arxiv_paper",
    max_retries=3,
    default_retry_delay=60,
    soft_time_limit=120,
    time_limit=180,
)
def ingest_arxiv_paper(
    self: Any, chair_id: int, arxiv_id: str, user_id: int, job_id: str
) -> dict:
    """Fetch an ArXiv paper, embed its abstract, and store it."""
    from app.config import get_settings
    from app.chairs.schemas import ArxivIngestRequest

    settings = get_settings()
    logger.info("ingest_arxiv_paper: chair_id=%d arxiv_id=%s job_id=%s", chair_id, arxiv_id, job_id)

    async def _inner():
        from app.db import SessionLocal
        from app.chairs.repository import ChairRepository
        from app.chairs.service import ChairService
        from app.llm.factory import build_embed_client

        async with SessionLocal() as session:
            repo = ChairRepository(session)
            embed_client = build_embed_client(settings)
            svc = ChairService(repo, embed_client, settings)
            req = ArxivIngestRequest(arxiv_id=arxiv_id)
            doc = await svc.ingest_arxiv_paper(chair_id, req)
            return {"document_id": doc.id, "title": doc.title}

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
    except (NotFoundException, AlreadyExistsException):
        publish_event(
            settings.redis_url,
            event_type="task_failed",
            job_id=job_id,
            user_id=user_id,
            status="failure",
        )
        raise
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


@celery_app.task(
    bind=True,
    name="app.chairs.tasks.embed_chair_description",
    max_retries=3,
    default_retry_delay=60,
    soft_time_limit=120,
    time_limit=180,
)
def embed_chair_description(self: Any, chair_id: int, user_id: int, job_id: str) -> dict:
    """Embed a chair's description and store it as a ChairDocument."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("embed_chair_description: chair_id=%d job_id=%s", chair_id, job_id)

    async def _inner():
        from app.db import SessionLocal
        from app.chairs.repository import ChairRepository
        from app.llm.factory import build_embed_client
        from app.models.chair import ChairDocumentKind

        async with SessionLocal() as session:
            repo = ChairRepository(session)
            chair = await repo.get_by_id(chair_id)
            if chair is None:
                raise NotFoundException("Chair", chair_id)
            embed_client = build_embed_client(settings)
            try:
                embedding = await embed_client.embed(
                    settings.ollama_embed_model, chair.short_description
                )
            except Exception:
                embedding = None
            await repo.add_document(
                chair_id=chair_id,
                kind=ChairDocumentKind.description,
                content=chair.short_description,
                embedding=embedding,
            )
            await repo.commit()
            return {"chair_id": chair_id}

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
        )
        raise
    except (ConnectionError, TimeoutError, OSError) as exc:
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
