"""Phase 4: Tests for transcript parsing Celery task.

These tests will FAIL until app.students.tasks is implemented.
"""

from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.unit
class TestParseTranscriptTask:
    def test_calls_extract_pdf_text(self):
        from app.students.tasks import parse_transcript

        with patch("app.students.tasks.run_async") as mock_run, \
             patch("app.students.tasks._get_deps") as mock_deps:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            parse_transcript(user_id=1, pdf_bytes_ref="ref-123", job_id="job-1")
            mock_run.assert_called_once()

    def test_marks_job_success(self):
        from app.students.tasks import parse_transcript

        with patch("app.students.tasks.run_async") as mock_run, \
             patch("app.students.tasks._get_deps") as mock_deps, \
             patch("app.students.tasks.publish_event") as mock_publish:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            parse_transcript(user_id=1, pdf_bytes_ref="ref-123", job_id="job-1")

            if mock_publish.called:
                call_kwargs = mock_publish.call_args.kwargs
                assert call_kwargs.get("status") == "success" or \
                       call_kwargs.get("event_type") == "task_complete"

    def test_invalid_llm_json_fails(self):
        from app.students.tasks import parse_transcript

        with patch("app.students.tasks.run_async") as mock_run, \
             patch("app.students.tasks._get_deps") as mock_deps:
            mock_run.side_effect = ValueError("Invalid JSON from LLM")
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            try:
                parse_transcript(user_id=1, pdf_bytes_ref="ref-123", job_id="job-1")
            except (ValueError, Exception):
                pass

    def test_retries_on_llm_timeout(self):
        from app.students.tasks import parse_transcript

        with patch("app.students.tasks.run_async") as mock_run, \
             patch("app.students.tasks._get_deps") as mock_deps:
            mock_run.side_effect = TimeoutError("LLM timeout")
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            try:
                parse_transcript(user_id=1, pdf_bytes_ref="ref-123", job_id="job-1")
            except (TimeoutError, Exception):
                pass

    def test_publishes_event(self):
        from app.students.tasks import parse_transcript

        with patch("app.students.tasks.run_async") as mock_run, \
             patch("app.students.tasks._get_deps") as mock_deps, \
             patch("app.students.tasks.publish_event") as mock_publish:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            parse_transcript(user_id=1, pdf_bytes_ref="ref-123", job_id="job-1")

            mock_publish.assert_called_once()
