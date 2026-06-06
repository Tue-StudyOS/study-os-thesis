"""Business logic for querying and listing papers."""

from __future__ import annotations

from app.models.paper import Paper
from app.papers.constants import PAPER_LIST_DEFAULT_LIMIT, PAPER_LIST_DEFAULT_OFFSET
from app.papers.repository import PaperRepository


class PaginatedPapers:
    def __init__(self, *, items: list[Paper], total: int, limit: int, offset: int) -> None:
        self.items = items
        self.total = total
        self.limit = limit
        self.offset = offset


class PaperService:
    def __init__(self, paper_repo: PaperRepository) -> None:
        self._repo = paper_repo

    async def list_papers(
        self,
        *,
        chair_id: int | None = None,
        tag_name: str | None = None,
        limit: int = PAPER_LIST_DEFAULT_LIMIT,
        offset: int = PAPER_LIST_DEFAULT_OFFSET,
    ) -> PaginatedPapers:
        items = await self._repo.list(
            chair_id=chair_id,
            tag_name=tag_name,
            limit=limit,
            offset=offset,
        )
        total = await self._repo.count(chair_id=chair_id, tag_name=tag_name)
        return PaginatedPapers(items=items, total=total, limit=limit, offset=offset)

    async def get_paper(self, paper_id: int) -> Paper:
        from app.exceptions import NotFoundException

        paper = await self._repo.get_by_id(paper_id)
        if paper is None:
            raise NotFoundException("Paper", paper_id)
        return paper
