"""Unit tests for ResearcherRepository dedup/upsert contracts."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.dialects import postgresql

from app.researchers.repository import ResearcherRepository


@pytest.mark.unit
async def test_get_by_profile_url_filters_profile_url():
    session = AsyncMock()
    repo = ResearcherRepository(session)

    await repo.get_by_profile_url("https://chair.example/team/jane")

    statement = session.scalar.await_args.args[0]
    compiled = str(statement.compile(dialect=postgresql.dialect()))
    assert "researchers.profile_url" in compiled


@pytest.mark.unit
async def test_upsert_updates_existing_matched_by_profile_url():
    session = AsyncMock()
    repo = ResearcherRepository(session)
    existing = SimpleNamespace(
        id=7, name="Old Name", title=None, role=None, email=None, profile_url="u", source_url=None, orcid=None, affiliation=None, chair_id=1, is_professor=False
    )
    repo.get_by_profile_url = AsyncMock(return_value=existing)
    repo.get_by_name_and_chair = AsyncMock()
    repo.create = AsyncMock()

    result = await repo.upsert(name="Jane Doe", chair_id=1, profile_url="u", title="Dr.", is_professor=True)

    assert result is existing
    assert existing.name == "Jane Doe"
    assert existing.title == "Dr."
    assert existing.is_professor is True
    # profile_url match short-circuits the name lookup, and we update in place.
    repo.get_by_name_and_chair.assert_not_awaited()
    repo.create.assert_not_awaited()


@pytest.mark.unit
async def test_upsert_falls_back_to_name_and_chair():
    session = AsyncMock()
    repo = ResearcherRepository(session)
    existing = SimpleNamespace(
        id=3, name="Jane", title=None, role=None, email=None, profile_url=None, source_url=None, orcid=None, affiliation=None, chair_id=2, is_professor=False
    )
    repo.get_by_profile_url = AsyncMock(return_value=None)
    repo.get_by_name_and_chair = AsyncMock(return_value=existing)
    repo.create = AsyncMock()

    result = await repo.upsert(name="Jane Doe", chair_id=2, role="PhD Student")

    assert result is existing
    assert existing.role == "PhD Student"
    repo.get_by_name_and_chair.assert_awaited_once_with("Jane Doe", 2)
    repo.create.assert_not_awaited()


@pytest.mark.unit
async def test_upsert_creates_when_no_match():
    session = AsyncMock()
    repo = ResearcherRepository(session)
    created = SimpleNamespace(id=99)
    repo.get_by_profile_url = AsyncMock(return_value=None)
    repo.get_by_name_and_chair = AsyncMock(return_value=None)
    repo.create = AsyncMock(return_value=created)

    result = await repo.upsert(name="New Person", chair_id=5, profile_url="p", email="x@y.z")

    assert result is created
    repo.create.assert_awaited_once()
    kwargs = repo.create.await_args.kwargs
    assert kwargs["name"] == "New Person"
    assert kwargs["chair_id"] == 5
    assert kwargs["profile_url"] == "p"
    assert kwargs["email"] == "x@y.z"
