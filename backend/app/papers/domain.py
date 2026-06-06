"""Pure Pydantic domain models for the scraper pipeline.

These are independent of SQLAlchemy and flow through the pipeline stages.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class PaperCandidate(BaseModel):
    """Raw paper data from any source, before LLM enrichment."""

    title: str
    abstract: str | None = None
    authors: list[str] = Field(default_factory=list)
    publication_date: datetime | None = None
    # Identifies the source adapter that discovered this paper
    source: str
    source_url: str
    doi: str | None = None


class EnrichedPaper(PaperCandidate):
    """Paper after LLM enrichment (summary + tags added)."""

    summary: str | None = None
    tags: list[str] = Field(default_factory=list)
    recency_score: float = 0.0
    relevance_score: float = 0.0


class ResearcherInfo(BaseModel):
    """Researcher identity passed to paper-source adapters."""

    name: str
    orcid: str | None = None
    affiliation: str | None = None
    chair_id: int | None = None
