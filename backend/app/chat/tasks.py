"""Celery tasks for the chat agent loop."""

from __future__ import annotations

import logging
from typing import Any

from app.chat.constants import (
    CHAT_MESSAGE_EVENT,
    CHAT_MESSAGE_STATUS_IN_PROGRESS,
    CHAT_TURN_COMPLETED_EVENT,
    CHAT_TURN_STARTED_EVENT,
    PROCESS_CHAT_TURN_DEFAULT_RETRY_DELAY_SECONDS,
    PROCESS_CHAT_TURN_MAX_RETRIES,
    PROCESS_CHAT_TURN_SOFT_TIME_LIMIT_SECONDS,
    PROCESS_CHAT_TURN_TASK_NAME,
    PROCESS_CHAT_TURN_TIME_LIMIT_SECONDS,
)
from app.worker.celery_app import celery_app
from app.worker.task_runner import execute_task

logger = logging.getLogger(__name__)


async def _process_chat_turn_work(session_id: int, user_id: int, content: str, job_id: str, redis_url: str, settings: Any) -> dict:
    from app.chairs.repository import ChairRepository
    from app.chat.repository import ChatRepository
    from app.chat.service import ChatService
    from app.db import SessionLocal
    from app.llm.factory import build_chat_client, build_embed_client
    from app.models import MessageRole
    from app.students.repository import StudentRepository
    from app.theses.repository import ThesisRepository
    from app.worker.publisher import publish_event

    async def on_message_created(msg: Any) -> None:
        """Publish a chat message event for real-time WebSocket streaming."""
        event_data = {
            "session_id": session_id,
            "message_id": msg.id,
            "role": msg.role.value if isinstance(msg.role, MessageRole) else msg.role,
            "content": msg.content or "",
        }
        if msg.role == MessageRole.assistant and msg.tool_calls:
            event_data["tool_calls"] = msg.tool_calls
        if msg.role == MessageRole.tool and msg.tool_name:
            event_data["tool_name"] = msg.tool_name
        publish_event(
            redis_url,
            event_type=CHAT_MESSAGE_EVENT,
            job_id=job_id,
            user_id=user_id,
            status=CHAT_MESSAGE_STATUS_IN_PROGRESS,
            data=event_data,
        )

    async with SessionLocal() as session:
        svc = ChatService(
            chat_repo=ChatRepository(session),
            chat_client=build_chat_client(settings),
            embed_client=build_embed_client(settings),
            settings=settings,
            student_repo=StudentRepository(session),
            chair_repo=ChairRepository(session),
            thesis_repo=ThesisRepository(session),
        )
        messages = await svc.send_message(session_id, user_id, content, on_message_created=on_message_created)
        return {"session_id": session_id, "message_count": len(messages)}


@celery_app.task(
    bind=True,
    name=PROCESS_CHAT_TURN_TASK_NAME,
    max_retries=PROCESS_CHAT_TURN_MAX_RETRIES,
    default_retry_delay=PROCESS_CHAT_TURN_DEFAULT_RETRY_DELAY_SECONDS,
    soft_time_limit=PROCESS_CHAT_TURN_SOFT_TIME_LIMIT_SECONDS,
    time_limit=PROCESS_CHAT_TURN_TIME_LIMIT_SECONDS,
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

    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _process_chat_turn_work(session_id, user_id, content, job_id, settings.redis_url, settings),
        success_event=CHAT_TURN_COMPLETED_EVENT,
        started_event=CHAT_TURN_STARTED_EVENT,
        started_data={"session_id": session_id},
    )
