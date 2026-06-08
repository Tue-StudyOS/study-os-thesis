"""Data-access layer for the researchers and researcher_papers tables."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.researcher import Researcher, ResearcherPaper


def _normalize_name(name: str) -> str:
    """Lowercase + trim for case-insensitive employee-name dedup."""
    return name.strip().lower()


class ResearcherRepository:
    """CRUD and lookup operations for the researchers table."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        name: str,
        chair_id: int | None = None,
        title: str | None = None,
        role: str | None = None,
        email: str | None = None,
        profile_url: str | None = None,
        source_url: str | None = None,
        orcid: str | None = None,
        affiliation: str | None = None,
        is_professor: bool = False,
    ) -> Researcher:
        researcher = Researcher(
            name=name,
            chair_id=chair_id,
            title=title,
            role=role,
            email=email,
            profile_url=profile_url,
            source_url=source_url,
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
                func.lower(func.trim(Researcher.name)) == _normalize_name(name),
                Researcher.chair_id == chair_id,
            )
        )

    async def get_by_profile_url(self, profile_url: str) -> Researcher | None:
        return await self._session.scalar(select(Researcher).where(Researcher.profile_url == profile_url))

    async def upsert(
        self,
        *,
        name: str,
        chair_id: int | None = None,
        title: str | None = None,
        role: str | None = None,
        email: str | None = None,
        profile_url: str | None = None,
        source_url: str | None = None,
        orcid: str | None = None,
        affiliation: str | None = None,
        is_professor: bool = False,
    ) -> Researcher:
        """Create or update an employee, deduplicating on profile_url, then on
        (normalized name + chair_id). On a hit, only provided (non-None) fields
        overwrite existing values; ``name``/``is_professor`` always apply."""
        existing: Researcher | None = None
        if profile_url is not None:
            existing = await self.get_by_profile_url(profile_url)
        if existing is None and chair_id is not None:
            existing = await self.get_by_name_and_chair(name, chair_id)

        updates = {
            "chair_id": chair_id,
            "title": title,
            "role": role,
            "email": email,
            "profile_url": profile_url,
            "source_url": source_url,
            "orcid": orcid,
            "affiliation": affiliation,
        }
        if existing is not None:
            existing.name = name
            existing.is_professor = is_professor
            for field, value in updates.items():
                if value is not None:
                    setattr(existing, field, value)
            await self._session.flush()
            await self._session.refresh(existing)
            return existing

        return await self.create(
            name=name,
            is_professor=is_professor,
            **updates,
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
