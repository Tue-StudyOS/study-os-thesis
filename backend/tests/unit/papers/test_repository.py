"""Unit tests for paper repository query contracts."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from sqlalchemy.dialects import postgresql

from app.papers.repository import PaperRepository


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
