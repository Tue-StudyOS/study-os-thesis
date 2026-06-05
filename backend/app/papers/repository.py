"""Data-access layer for the papers, tags, and paper_tags tables."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.paper import Paper, PaperTag, Tag


class PaperRepository:
    """CRUD and lookup operations for the papers table."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        title: str,
        title_normalized: str,
        source: str,
        source_url: str,
        abstract: str | None = None,
        summary: str | None = None,
        authors: list[str] | None = None,
        publication_date: datetime | None = None,
        arxiv_id: str | None = None,
        doi: str | None = None,
        recency_score: float = 0.0,
        relevance_score: float = 0.0,
        embedding: list[float] | None = None,
        enriched_at: datetime | None = None,
    ) -> Paper:
        paper = Paper(
            title=title,
            title_normalized=title_normalized,
            source=source,
            source_url=source_url,
            abstract=abstract,
            summary=summary,
            authors=authors or [],
            publication_date=publication_date,
            arxiv_id=arxiv_id,
            doi=doi,
            recency_score=recency_score,
            relevance_score=relevance_score,
            embedding=embedding,
            enriched_at=enriched_at,
        )
        self._session.add(paper)
        await self._session.flush()
        await self._session.refresh(paper)
        return paper

    async def get_by_id(self, paper_id: int) -> Paper | None:
        return await self._session.get(Paper, paper_id)

    async def get_by_arxiv_id(self, arxiv_id: str) -> Paper | None:
        return await self._session.scalar(select(Paper).where(Paper.arxiv_id == arxiv_id))

    async def get_by_doi(self, doi: str) -> Paper | None:
        return await self._session.scalar(select(Paper).where(Paper.doi == doi))

    async def get_by_title_author(self, title_normalized: str, first_author: str) -> Paper | None:
        """Look up a paper by its normalised title and first author name."""
        return await self._session.scalar(
            select(Paper).where(
                Paper.title_normalized == title_normalized,
                Paper.arxiv_id.is_(None),
                Paper.doi.is_(None),
            )
        )

    async def list(
        self,
        *,
        chair_id: int | None = None,
        tag_name: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Paper]:
        """List papers ordered by relevance_score DESC, with optional filters."""
        from app.models.researcher import Researcher, ResearcherPaper

        stmt = (
            select(Paper)
            .options(selectinload(Paper.tags).selectinload(PaperTag.tag))
            .order_by(Paper.relevance_score.desc(), Paper.publication_date.desc())
            .limit(limit)
            .offset(offset)
        )

        if chair_id is not None:
            stmt = stmt.join(Paper.researchers).join(ResearcherPaper.researcher).where(Researcher.chair_id == chair_id)

        if tag_name is not None:
            stmt = stmt.join(Paper.tags).join(PaperTag.tag).where(Tag.name == tag_name.lower())

        rows = await self._session.scalars(stmt)
        return list(rows)

    async def update(self, paper: Paper, **fields: object) -> Paper:
        for key, value in fields.items():
            setattr(paper, key, value)
        await self._session.flush()
        await self._session.refresh(paper)
        return paper

    async def add_tag(self, paper_id: int, tag_id: int) -> None:
        existing = await self._session.scalar(select(PaperTag).where(PaperTag.paper_id == paper_id, PaperTag.tag_id == tag_id))
        if existing is None:
            self._session.add(PaperTag(paper_id=paper_id, tag_id=tag_id))
            await self._session.flush()

    async def commit(self) -> None:
        await self._session.commit()


class TagRepository:
    """CRUD for the canonical tags table."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_name(self, name: str) -> Tag | None:
        return await self._session.scalar(select(Tag).where(Tag.name == name.lower()))

    async def get_or_create(self, name: str) -> Tag:
        name = name.lower().strip()
        tag = await self.get_by_name(name)
        if tag is None:
            tag = Tag(name=name)
            self._session.add(tag)
            await self._session.flush()
            await self._session.refresh(tag)
        return tag

    async def list_all(self) -> list[Tag]:
        rows = await self._session.scalars(select(Tag).order_by(Tag.name))
        return list(rows)

    async def commit(self) -> None:
        await self._session.commit()
