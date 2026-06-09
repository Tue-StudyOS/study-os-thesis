"""Unit tests for discover_chair_employees Celery task."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.papers.domain import ResearcherInfo


@pytest.mark.unit
class TestDiscoverChairEmployeesTask:
    async def test_discover_researchers_and_upserts(self):
        """Test that task discovers researchers and upserts them."""
        from app.scraper.tasks import _discover_chair_employees_work

        mock_chair_repo = AsyncMock()
        mock_researcher_service = AsyncMock()
        mock_llm_port = AsyncMock()

        chair = MagicMock()
        chair.id = 1
        chair.website_url = "https://example.com/team"
        mock_chair_repo.get_by_id.return_value = chair

        discovered_researchers = [
            ResearcherInfo(
                name="Alice Smith",
                title="Prof. Dr.",
                role="Professor",
                email="alice@example.com",
                profile_url="https://example.com/alice",
                source_url="https://example.com/team",
                chair_id=1,
            ),
            ResearcherInfo(
                name="Bob Jones",
                role="Research Associate",
                email="bob@example.com",
                profile_url="https://example.com/bob",
                source_url="https://example.com/team",
                chair_id=1,
            ),
        ]

        with patch("app.scraper.adapters.chair_discovery.ChairDiscoveryAdapter") as mock_adapter_class:
            mock_adapter = AsyncMock()
            mock_adapter_class.return_value = mock_adapter
            mock_adapter.discover_researchers.return_value = discovered_researchers

            mock_researcher_service.upsert_researcher.side_effect = [
                MagicMock(id=10),
                MagicMock(id=11),
            ]

            result = await _discover_chair_employees_work(
                chair_id=1,
                user_id=1,
                llm_port=mock_llm_port,
                chair_repo=mock_chair_repo,
                researcher_service=mock_researcher_service,
            )

            assert result["chair_id"] == 1
            assert result["discovered"] == 2
            assert result["updated"] == 0
            assert mock_researcher_service.upsert_researcher.call_count == 2

    async def test_discover_handles_empty_researchers(self):
        """Test handling of empty researcher list."""
        from app.scraper.tasks import _discover_chair_employees_work

        mock_chair_repo = AsyncMock()
        mock_researcher_service = AsyncMock()
        mock_llm_port = AsyncMock()

        chair = MagicMock()
        chair.id = 1
        chair.website_url = "https://example.com/team"
        mock_chair_repo.get_by_id.return_value = chair

        with patch("app.scraper.adapters.chair_discovery.ChairDiscoveryAdapter") as mock_adapter_class:
            mock_adapter = AsyncMock()
            mock_adapter_class.return_value = mock_adapter
            mock_adapter.discover_researchers.return_value = []

            result = await _discover_chair_employees_work(
                chair_id=1,
                user_id=1,
                llm_port=mock_llm_port,
                chair_repo=mock_chair_repo,
                researcher_service=mock_researcher_service,
            )

            assert result["chair_id"] == 1
            assert result["discovered"] == 0
            assert mock_researcher_service.upsert_researcher.call_count == 0

    async def test_discover_fails_gracefully_on_fetch_error(self):
        """Test graceful handling of fetch errors."""
        from app.scraper.tasks import _discover_chair_employees_work

        mock_chair_repo = AsyncMock()
        mock_researcher_service = AsyncMock()
        mock_llm_port = AsyncMock()

        chair = MagicMock()
        chair.id = 1
        chair.website_url = "https://example.com/team"
        mock_chair_repo.get_by_id.return_value = chair

        with patch("app.scraper.adapters.chair_discovery.ChairDiscoveryAdapter") as mock_adapter_class:
            mock_adapter = AsyncMock()
            mock_adapter_class.return_value = mock_adapter
            mock_adapter.discover_researchers.side_effect = Exception("Network error")

            result = await _discover_chair_employees_work(
                chair_id=1,
                user_id=1,
                llm_port=mock_llm_port,
                chair_repo=mock_chair_repo,
                researcher_service=mock_researcher_service,
            )

            assert result["error"] == "Network error"
            assert result["discovered"] == 0
