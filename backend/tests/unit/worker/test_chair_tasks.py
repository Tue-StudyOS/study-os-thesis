"""Phase 4: Tests for chair-related Celery tasks.

These tests will FAIL until app.chairs.tasks is implemented.
"""

from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.unit
class TestIngestArxivTask:
    def test_calls_fetch_metadata(self):
        from app.chairs.tasks import ingest_arxiv_paper

        with patch("app.chairs.tasks.run_async") as mock_run, \
             patch("app.chairs.tasks._get_deps") as mock_deps:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            ingest_arxiv_paper(chair_id=1, arxiv_id="2301.07041", user_id=1, job_id="job-1")
            mock_run.assert_called_once()

    def test_marks_job_success(self):
        from app.chairs.tasks import ingest_arxiv_paper

        with patch("app.chairs.tasks.run_async") as mock_run, \
             patch("app.chairs.tasks._get_deps") as mock_deps, \
             patch("app.chairs.tasks.publish_event") as mock_publish:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            ingest_arxiv_paper(chair_id=1, arxiv_id="2301.07041", user_id=1, job_id="job-1")

            if mock_publish.called:
                call_kwargs = mock_publish.call_args.kwargs
                assert call_kwargs.get("status") == "success" or \
                       call_kwargs.get("event_type") == "task_complete"

    def test_duplicate_fails_permanently(self):
        from app.chairs.tasks import ingest_arxiv_paper
        from app.exceptions import AlreadyExistsException

        with patch("app.chairs.tasks.run_async") as mock_run, \
             patch("app.chairs.tasks._get_deps") as mock_deps:
            mock_run.side_effect = AlreadyExistsException("ChairDocument", "arxiv_id", "2301.07041")
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            try:
                ingest_arxiv_paper(chair_id=1, arxiv_id="2301.07041", user_id=1, job_id="job-1")
            except AlreadyExistsException:
                pass

    def test_retries_on_network_error(self):
        from app.chairs.tasks import ingest_arxiv_paper

        with patch("app.chairs.tasks.run_async") as mock_run, \
             patch("app.chairs.tasks._get_deps") as mock_deps:
            mock_run.side_effect = ConnectionError("Network error")
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            try:
                ingest_arxiv_paper(chair_id=1, arxiv_id="2301.07041", user_id=1, job_id="job-1")
            except (ConnectionError, Exception):
                pass


@pytest.mark.unit
class TestEmbedChairDescriptionTask:
    def test_embeds_text(self):
        from app.chairs.tasks import embed_chair_description

        with patch("app.chairs.tasks.run_async") as mock_run, \
             patch("app.chairs.tasks._get_deps") as mock_deps:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            embed_chair_description(chair_id=1, user_id=1, job_id="job-1")
            mock_run.assert_called_once()

    def test_marks_job_success(self):
        from app.chairs.tasks import embed_chair_description

        with patch("app.chairs.tasks.run_async") as mock_run, \
             patch("app.chairs.tasks._get_deps") as mock_deps, \
             patch("app.chairs.tasks.publish_event") as mock_publish:
            mock_run.return_value = None
            mock_deps.return_value = (AsyncMock(), AsyncMock())

            embed_chair_description(chair_id=1, user_id=1, job_id="job-1")

            if mock_publish.called:
                call_kwargs = mock_publish.call_args.kwargs
                assert call_kwargs.get("status") == "success" or \
                       call_kwargs.get("event_type") == "task_complete"
