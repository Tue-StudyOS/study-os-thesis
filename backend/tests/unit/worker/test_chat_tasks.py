"""Tests for the chat agent loop Celery task."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.chat.constants import CHAT_MESSAGE_EVENT, CHAT_MESSAGE_STATUS_IN_PROGRESS, CHAT_TURN_COMPLETED_EVENT, CHAT_TURN_STARTED_EVENT
from app.models import MessageRole
from app.chat.tasks import _process_chat_turn_work, process_chat_turn


def _acm(session):
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=session)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


@pytest.mark.unit
class TestProcessChatTurnWiring:
    def test_uses_chat_event_names(self):
        with patch("app.chat.tasks.execute_task") as ex:
            process_chat_turn(session_id=2, user_id=1, content="Hi", job_id="j")

        kw = ex.call_args.kwargs
        assert kw["success_event"] == CHAT_TURN_COMPLETED_EVENT
        assert kw["started_event"] == CHAT_TURN_STARTED_EVENT
        assert kw["started_data"] == {"session_id": 2}


@pytest.mark.unit
class TestProcessChatTurnWork:
    async def test_runs_agent_and_counts_messages(self):
        session = AsyncMock()
        svc = AsyncMock()
        svc.send_message.return_value = ["m1", "m2", "m3"]
        settings = SimpleNamespace(ollama_embed_model="m")

        with (
            patch("app.db.SessionLocal", return_value=_acm(session)),
            patch("app.chat.repository.ChatRepository", return_value=AsyncMock()),
            patch("app.students.repository.StudentRepository", return_value=AsyncMock()),
            patch("app.chairs.repository.ChairRepository", return_value=AsyncMock()),
            patch("app.theses.repository.ThesisRepository", return_value=AsyncMock()),
            patch("app.chat.service.ChatService", return_value=svc),
            patch("app.llm.factory.build_chat_client", return_value=AsyncMock()),
            patch("app.llm.factory.build_embed_client", return_value=AsyncMock()),
            patch("app.worker.publisher.publish_event", return_value=None),
        ):
            result = await _process_chat_turn_work(
                session_id=2,
                user_id=1,
                content="Hello",
                job_id="job-123",
                redis_url="redis://localhost:6379/0",
                settings=settings,
            )

        # Check that send_message was called with the callback parameter
        assert svc.send_message.await_count == 1
        call_args = svc.send_message.call_args
        assert call_args.args == (2, 1, "Hello")
        assert "on_message_created" in call_args.kwargs
        assert call_args.kwargs["on_message_created"] is not None
        assert result == {"session_id": 2, "message_count": 3}

    async def test_message_callback_publishes_message_event_shape(self):
        session = AsyncMock()
        published = MagicMock()
        assistant_message = SimpleNamespace(
            id=10,
            role=MessageRole.assistant,
            content="Answer",
            tool_calls=[{"id": "call-1"}],
            tool_name=None,
        )

        async def send_message(*args, on_message_created):
            await on_message_created(assistant_message)
            return [assistant_message]

        svc = AsyncMock()
        svc.send_message.side_effect = send_message

        with (
            patch("app.db.SessionLocal", return_value=_acm(session)),
            patch("app.chairs.repository.ChairRepository", return_value=AsyncMock()),
            patch("app.chat.repository.ChatRepository", return_value=AsyncMock()),
            patch("app.chat.service.ChatService", return_value=svc),
            patch("app.llm.factory.build_chat_client", return_value=AsyncMock()),
            patch("app.llm.factory.build_embed_client", return_value=AsyncMock()),
            patch("app.students.repository.StudentRepository", return_value=AsyncMock()),
            patch("app.theses.repository.ThesisRepository", return_value=AsyncMock()),
            patch("app.worker.publisher.publish_event", published),
        ):
            await _process_chat_turn_work(2, 1, "Hello", "job-123", "redis://x", SimpleNamespace())

        published.assert_called_once()
        kw = published.call_args.kwargs
        assert kw["event_type"] == CHAT_MESSAGE_EVENT
        assert kw["status"] == CHAT_MESSAGE_STATUS_IN_PROGRESS
        assert kw["data"]["role"] == "assistant"
        assert kw["data"]["tool_calls"] == [{"id": "call-1"}]
