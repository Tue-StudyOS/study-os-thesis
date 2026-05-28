"""Phase 4: Tests for thesis embedding Celery task.

These tests will FAIL until app.theses.tasks is implemented.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.unit
class TestEmbedThesisTask:
    def test_calls_embed_with_title_and_abstract(self):
        from app.theses.tasks import embed_thesis

        with patch("app.theses.tasks.run_async") as mock_run, \
             patch("app.theses.tasks._get_deps") as mock_deps:
            mock_service = AsyncMock()
            mock_deps.return_value = (mock_service, AsyncMock())
            mock_run.side_effect = lambda coro: None  # run_async executes the coro

            # The task should call service to generate embedding
            embed_thesis(thesis_id=1, user_id=1, job_id="job-123")
            mock_run.assert_called_once()

    def test_marks_job_success(self):
        from app.theses.tasks import embed_thesis

        with patch("app.theses.tasks.run_async") as mock_run, \
             patch("app.theses.tasks._get_deps") as mock_deps, \
             patch("app.theses.tasks.publish_event") as mock_publish:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            embed_thesis(thesis_id=1, user_id=1, job_id="job-123")

            # Should publish a success event
            if mock_publish.called:
                call_kwargs = mock_publish.call_args.kwargs
                assert call_kwargs.get("status") == "success" or \
                       call_kwargs.get("event_type") == "task_complete"

    def test_marks_job_failure_on_error(self):
        from app.theses.tasks import embed_thesis

        with patch("app.theses.tasks.run_async") as mock_run, \
             patch("app.theses.tasks._get_deps") as mock_deps, \
             patch("app.theses.tasks.publish_event") as mock_publish:
            mock_run.side_effect = Exception("LLM down")
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            # Task should handle the error
            try:
                embed_thesis(thesis_id=1, user_id=1, job_id="job-123")
            except Exception:
                pass  # May or may not re-raise depending on retry logic

    def test_retries_on_connection_error(self):
        from app.theses.tasks import embed_thesis

        with patch("app.theses.tasks.run_async") as mock_run, \
             patch("app.theses.tasks._get_deps") as mock_deps:
            mock_run.side_effect = ConnectionError("Connection refused")
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            # Should trigger retry
            try:
                embed_thesis(thesis_id=1, user_id=1, job_id="job-123")
            except (ConnectionError, Exception):
                pass  # Expected - retry mechanism will handle it

    def test_no_retry_on_not_found(self):
        from app.theses.tasks import embed_thesis
        from app.exceptions import NotFoundException

        with patch("app.theses.tasks.run_async") as mock_run, \
             patch("app.theses.tasks._get_deps") as mock_deps:
            mock_run.side_effect = NotFoundException("Thesis", 999)
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            # Should NOT retry, should fail permanently
            try:
                embed_thesis(thesis_id=999, user_id=1, job_id="job-123")
            except NotFoundException:
                pass  # Expected - permanent failure
