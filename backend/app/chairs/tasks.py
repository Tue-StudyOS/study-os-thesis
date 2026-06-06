"""Celery tasks for chair-related background work."""

from __future__ import annotations

import logging
from typing import Any

from app.chairs.constants import (
    EMBED_CHAIR_DEFAULT_RETRY_DELAY_SECONDS,
    EMBED_CHAIR_MAX_RETRIES,
    EMBED_CHAIR_SOFT_TIME_LIMIT_SECONDS,
    EMBED_CHAIR_TASK_NAME,
    EMBED_CHAIR_TIME_LIMIT_SECONDS,
)
from app.exceptions import NotFoundException
from app.worker.celery_app import celery_app
from app.worker.task_runner import execute_task

logger = logging.getLogger(__name__)


async def _embed_chair_work(chair_id: int, settings: Any) -> dict:
    from app.chairs.repository import ChairRepository
    from app.db import SessionLocal
    from app.llm.factory import build_embed_client
    from app.models.chair import ChairDocumentKind

    async with SessionLocal() as session:
        repo = ChairRepository(session)
        chair = await repo.get_by_id(chair_id)
        if chair is None:
            raise NotFoundException("Chair", chair_id)
        embed_client = build_embed_client(settings)
        try:
            embedding = await embed_client.embed(settings.ollama_embed_model, chair.short_description)
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


@celery_app.task(
    bind=True,
    name=EMBED_CHAIR_TASK_NAME,
    max_retries=EMBED_CHAIR_MAX_RETRIES,
    default_retry_delay=EMBED_CHAIR_DEFAULT_RETRY_DELAY_SECONDS,
    soft_time_limit=EMBED_CHAIR_SOFT_TIME_LIMIT_SECONDS,
    time_limit=EMBED_CHAIR_TIME_LIMIT_SECONDS,
)
def embed_chair_description(self: Any, chair_id: int, user_id: int, job_id: str) -> dict:
    """Embed a chair's description and store it as a ChairDocument."""
    from app.config import get_settings

    settings = get_settings()
    logger.info("embed_chair_description: chair_id=%d job_id=%s", chair_id, job_id)

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _embed_chair_work(chair_id, settings),
    )
