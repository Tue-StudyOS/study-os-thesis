"""Business logic for querying and listing papers."""

from __future__ import annotations

from app.papers.repository import PaperRepository
from app.models.paper import Paper


class PaperService:
    def __init__(self, paper_repo: PaperRepository) -> None:
        self._repo = paper_repo

    async def list_papers(
        self,
        *,
        chair_id: int | None = None,
        tag_name: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Paper]:
        return await self._repo.list(
            chair_id=chair_id,
            tag_name=tag_name,
            limit=limit,
            offset=offset,
        )

    async def get_paper(self, paper_id: int) -> Paper:
        from app.exceptions import NotFoundException

        paper = await self._repo.get_by_id(paper_id)
        if paper is None:
            raise NotFoundException("Paper", paper_id)
        return paper
