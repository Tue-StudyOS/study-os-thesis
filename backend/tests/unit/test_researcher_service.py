"""Unit tests for ResearcherService."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.researchers.schemas import ResearcherCreate
from app.researchers.service import ResearcherService


@pytest.fixture
def mock_researcher_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def researcher_service(mock_researcher_repo) -> ResearcherService:
    return ResearcherService(mock_researcher_repo)


@pytest.mark.unit
class TestUpsertResearcher:
    async def test_delegates_to_repo_and_commits(self, researcher_service, mock_researcher_repo):
        upserted = SimpleNamespace(id=12)
        mock_researcher_repo.upsert.return_value = upserted

        data = ResearcherCreate(
            name="Jane Doe",
            chair_id=1,
            role="Research Associate",
            profile_url="https://chair.example/team/jane",
            source_url="https://chair.example/team",
        )
        result = await researcher_service.upsert_researcher(data)

        assert result is upserted
        mock_researcher_repo.upsert.assert_awaited_once()
        kwargs = mock_researcher_repo.upsert.await_args.kwargs
        assert kwargs["name"] == "Jane Doe"
        assert kwargs["chair_id"] == 1
        assert kwargs["role"] == "Research Associate"
        assert kwargs["profile_url"] == "https://chair.example/team/jane"
        assert kwargs["source_url"] == "https://chair.example/team"
        mock_researcher_repo.commit.assert_awaited_once()
