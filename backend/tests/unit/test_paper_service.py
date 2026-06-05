from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.papers.service import PaperService


@pytest.mark.asyncio
async def test_list_papers_returns_items_and_matching_total() -> None:
    repo = AsyncMock()
    repo.list.return_value = ["paper-a", "paper-b"]
    repo.count.return_value = 17
    service = PaperService(repo)

    result = await service.list_papers(chair_id=6, tag_name="robotics", limit=15, offset=30)

    assert result.items == ["paper-a", "paper-b"]
    assert result.total == 17
    assert result.limit == 15
    assert result.offset == 30
    repo.list.assert_awaited_once_with(chair_id=6, tag_name="robotics", limit=15, offset=30)
    repo.count.assert_awaited_once_with(chair_id=6, tag_name="robotics")
