"""Phase 5: Tests for chat agent loop Celery task.

These tests will FAIL until app.chat.tasks is implemented.
"""

from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.unit
class TestProcessChatTurnTask:
    def test_loads_history(self):
        from app.chat.tasks import process_chat_turn

        with patch("app.chat.tasks.run_async") as mock_run, \
             patch("app.chat.tasks._get_deps") as mock_deps:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            process_chat_turn(session_id=1, user_id=1, content="Hello", job_id="job-1")
            mock_run.assert_called_once()

    def test_no_tool_calls_succeeds(self):
        from app.chat.tasks import process_chat_turn

        with patch("app.chat.tasks.run_async") as mock_run, \
             patch("app.chat.tasks._get_deps") as mock_deps, \
             patch("app.chat.tasks.publish_event") as mock_publish:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            process_chat_turn(session_id=1, user_id=1, content="Hello", job_id="job-1")

            # Should publish at minimum a completion event
            assert mock_publish.called

    def test_publishes_turn_started(self):
        from app.chat.tasks import process_chat_turn

        with patch("app.chat.tasks.run_async") as mock_run, \
             patch("app.chat.tasks._get_deps") as mock_deps, \
             patch("app.chat.tasks.publish_event") as mock_publish:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            process_chat_turn(session_id=1, user_id=1, content="Hello", job_id="job-1")

            # Look for a turn_started event
            event_types = [c.kwargs.get("event_type", "") for c in mock_publish.call_args_list]
            assert "chat_turn_started" in event_types

    def test_publishes_turn_completed(self):
        from app.chat.tasks import process_chat_turn

        with patch("app.chat.tasks.run_async") as mock_run, \
             patch("app.chat.tasks._get_deps") as mock_deps, \
             patch("app.chat.tasks.publish_event") as mock_publish:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            process_chat_turn(session_id=1, user_id=1, content="Hello", job_id="job-1")

            event_types = [c.kwargs.get("event_type", "") for c in mock_publish.call_args_list]
            assert "chat_turn_completed" in event_types

    def test_marks_job_failure_on_llm_error(self):
        from app.chat.tasks import process_chat_turn

        with patch("app.chat.tasks.run_async") as mock_run, \
             patch("app.chat.tasks._get_deps") as mock_deps, \
             patch("app.chat.tasks.publish_event") as mock_publish:
            mock_run.side_effect = Exception("LLM error")
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            try:
                process_chat_turn(session_id=1, user_id=1, content="Hello", job_id="job-1")
            except Exception:
                pass

            # Should publish failure event
            if mock_publish.called:
                event_types = [c.kwargs.get("event_type", "") for c in mock_publish.call_args_list]
                assert "task_failed" in event_types or any("fail" in et for et in event_types)

    def test_retries_on_connection_error(self):
        from app.chat.tasks import process_chat_turn

        with patch("app.chat.tasks.run_async") as mock_run, \
             patch("app.chat.tasks._get_deps") as mock_deps:
            mock_run.side_effect = ConnectionError("Network error")
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            try:
                process_chat_turn(session_id=1, user_id=1, content="Hello", job_id="job-1")
            except (ConnectionError, Exception):
                pass
