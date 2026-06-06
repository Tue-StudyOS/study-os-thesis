"""Business logic for researcher management."""

from __future__ import annotations

from app.exceptions import NotFoundException
from app.models.researcher import Researcher
from app.researchers.repository import ResearcherRepository
from app.researchers.schemas import ResearcherCreate


class ResearcherService:
    def __init__(self, researcher_repo: ResearcherRepository) -> None:
        self._repo = researcher_repo

    async def list_by_chair(self, chair_id: int) -> list[Researcher]:
        return await self._repo.list_by_chair(chair_id)

    async def get_researcher(self, researcher_id: int) -> Researcher:
        researcher = await self._repo.get_by_id(researcher_id)
        if researcher is None:
            raise NotFoundException("Researcher", researcher_id)
        return researcher

    async def create_researcher(self, data: ResearcherCreate) -> Researcher:
        researcher = await self._repo.create(
            name=data.name,
            chair_id=data.chair_id,
            orcid=data.orcid,
            affiliation=data.affiliation,
            is_professor=data.is_professor,
        )
        await self._repo.commit()
        return researcher
