"""Pydantic response schemas for the papers API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PaperOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    abstract: str | None
    summary: str | None
    authors: list[str]
    publication_date: datetime | None
    source: str
    source_url: str
    arxiv_id: str | None
    doi: str | None
    recency_score: float
    relevance_score: float
    enriched_at: datetime | None
    created_at: datetime
    tags: list[str] = []

    @classmethod
    def from_orm_with_tags(cls, paper: object) -> "PaperOut":
        """Build a PaperOut including the resolved tag names from joined PaperTag rows."""
        from app.models.paper import Paper

        p: Paper = paper  # type: ignore[assignment]
        tag_names = [pt.tag.name for pt in p.tags if pt.tag is not None]
        data = {
            "id": p.id,
            "title": p.title,
            "abstract": p.abstract,
            "summary": p.summary,
            "authors": p.authors,
            "publication_date": p.publication_date,
            "source": p.source,
            "source_url": p.source_url,
            "arxiv_id": p.arxiv_id,
            "doi": p.doi,
            "recency_score": p.recency_score,
            "relevance_score": p.relevance_score,
            "enriched_at": p.enriched_at,
            "created_at": p.created_at,
            "tags": tag_names,
        }
        return cls.model_validate(data)
