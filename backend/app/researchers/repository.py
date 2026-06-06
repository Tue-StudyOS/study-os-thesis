"""Data-access layer for the researchers and researcher_papers tables."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.researcher import Researcher, ResearcherPaper


class ResearcherRepository:
    """CRUD and lookup operations for the researchers table."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        name: str,
        chair_id: int | None = None,
        orcid: str | None = None,
        affiliation: str | None = None,
        is_professor: bool = False,
    ) -> Researcher:
        researcher = Researcher(
            name=name,
            chair_id=chair_id,
            orcid=orcid,
            affiliation=affiliation,
            is_professor=is_professor,
        )
        self._session.add(researcher)
        await self._session.flush()
        await self._session.refresh(researcher)
        return researcher

    async def get_by_id(self, researcher_id: int) -> Researcher | None:
        return await self._session.get(Researcher, researcher_id)

    async def get_by_name_and_chair(self, name: str, chair_id: int) -> Researcher | None:
        return await self._session.scalar(
            select(Researcher).where(
                Researcher.name == name,
                Researcher.chair_id == chair_id,
            )
        )

    async def list_by_chair(self, chair_id: int) -> list[Researcher]:
        rows = await self._session.scalars(select(Researcher).where(Researcher.chair_id == chair_id).order_by(Researcher.name))
        return list(rows)

    async def link_paper(self, researcher_id: int, paper_id: int) -> None:
        """Create researcher_papers row if it doesn't exist yet."""
        existing = await self._session.scalar(
            select(ResearcherPaper).where(
                ResearcherPaper.researcher_id == researcher_id,
                ResearcherPaper.paper_id == paper_id,
            )
        )
        if existing is None:
            self._session.add(ResearcherPaper(researcher_id=researcher_id, paper_id=paper_id))
            await self._session.flush()

    async def commit(self) -> None:
        await self._session.commit()
