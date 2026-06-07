"""Unit tests for paper repository query contracts."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError

from app.papers.repository import PaperRepository


class _FakeSavepoint:
    """Async context manager standing in for AsyncSession.begin_nested().

    Crucially, __aexit__ returns False so it does not swallow exceptions
    (unlike a bare AsyncMock), letting IntegrityError reach the caller.
    """

    async def __aenter__(self) -> "_FakeSavepoint":
        return self

    async def __aexit__(self, *exc_info: object) -> bool:
        return False


def _create_kwargs() -> dict:
    return dict(title="T", title_normalized="t", source="openalex", source_url="https://x")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_by_title_author_filters_title_first_author_and_missing_doi():
    session = AsyncMock()
    repo = PaperRepository(session)

    await repo.get_by_title_author("shared title", "Alice")

    statement = session.scalar.await_args.args[0]
    compiled = str(statement.compile(dialect=postgresql.dialect()))

    assert "papers.title_normalized" in compiled
    assert "papers.authors" in compiled
    assert "papers.doi IS NULL" in compiled


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_ignoring_conflict_returns_paper_on_success():
    session = AsyncMock()
    session.begin_nested = MagicMock(return_value=_FakeSavepoint())
    session.add = MagicMock()
    repo = PaperRepository(session)

    paper = await repo.create_ignoring_conflict(**_create_kwargs())

    assert paper is not None
    assert paper.title == "T"
    session.flush.assert_awaited()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_ignoring_conflict_returns_none_on_integrity_error():
    session = AsyncMock()
    session.begin_nested = MagicMock(return_value=_FakeSavepoint())
    session.add = MagicMock()
    # A concurrent task already inserted the same paper -> unique violation.
    session.flush.side_effect = IntegrityError("INSERT", {}, Exception("duplicate key"))
    repo = PaperRepository(session)

    paper = await repo.create_ignoring_conflict(**_create_kwargs())

    assert paper is None
