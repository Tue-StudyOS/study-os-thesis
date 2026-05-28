"""Celery tasks for the chat agent loop."""

from __future__ import annotations

import logging
import traceback
from typing import Any

from app.worker.celery_app import celery_app
from app.worker.publisher import publish_event
from app.worker.utils import run_async

logger = logging.getLogger(__name__)


def _get_deps() -> tuple[Any, Any]:
    """Build chat service and job service for use inside a task."""
    from app.config import get_settings
    from app.db import SessionLocal
    from app.chairs.repository import ChairRepository
    from app.chat.repository import ChatRepository
    from app.chat.service import ChatService
    from app.jobs.repository import JobRepository
    from app.jobs.service import JobService
    from app.llm.factory import build_chat_client, build_embed_client
    from app.students.repository import StudentRepository
    from app.theses.repository import ThesisRepository

    settings = get_settings()

    async def _build():
        session = SessionLocal()
        chat_repo = ChatRepository(session)
        chat_client = build_chat_client(settings)
        embed_client = build_embed_client(settings)
        student_repo = StudentRepository(session)
        chair_repo = ChairRepository(session)
        thesis_repo = ThesisRepository(session)
        svc = ChatService(
            chat_repo=chat_repo,
            chat_client=chat_client,
            embed_client=embed_client,
            settings=settings,
            student_repo=student_repo,
            chair_repo=chair_repo,
            thesis_repo=thesis_repo,
        )
        job_repo = JobRepository(session)
        job_svc = JobService(job_repo)
        return svc, job_svc

    return run_async(_build())


@celery_app.task(
    bind=True,
    name="app.chat.tasks.process_chat_turn",
    max_retries=2,
    default_retry_delay=30,
    soft_time_limit=600,
    time_limit=660,
)
def process_chat_turn(
    self: Any,
    session_id: int,
    user_id: int,
    content: str,
    job_id: str,
) -> dict:
    """Run the full chat agent loop (up to 6 LLM iterations) as a background task.

    Publishes WebSocket events at each stage so the client gets real-time updates.
    """
    from app.config import get_settings

    settings = get_settings()
    logger.info("process_chat_turn: session_id=%d user_id=%d job_id=%s", session_id, user_id, job_id)

    publish_event(
        settings.redis_url,
        event_type="chat_turn_started",
        job_id=job_id,
        user_id=user_id,
        status="started",
        data={"session_id": session_id},
    )

    async def _inner():
        from app.db import SessionLocal
        from app.chairs.repository import ChairRepository
        from app.chat.repository import ChatRepository
        from app.chat.service import ChatService
        from app.llm.factory import build_chat_client, build_embed_client
        from app.students.repository import StudentRepository
        from app.theses.repository import ThesisRepository

        async with SessionLocal() as session:
            chat_repo = ChatRepository(session)
            chat_client = build_chat_client(settings)
            embed_client = build_embed_client(settings)
            student_repo = StudentRepository(session)
            chair_repo = ChairRepository(session)
            thesis_repo = ThesisRepository(session)
            svc = ChatService(
                chat_repo=chat_repo,
                chat_client=chat_client,
                embed_client=embed_client,
                settings=settings,
                student_repo=student_repo,
                chair_repo=chair_repo,
                thesis_repo=thesis_repo,
            )
            messages = await svc.send_message(session_id, user_id, content)
            return {
                "session_id": session_id,
                "message_count": len(messages),
            }

    try:
        result = run_async(_inner())
        publish_event(
            settings.redis_url,
            event_type="chat_turn_completed",
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
