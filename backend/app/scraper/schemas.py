"""Pydantic schemas for the scraper API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScrapeChairRequest(BaseModel):
    """Optional overrides for a chair scrape run."""

    since_days: int = Field(365, ge=30, le=3650, description="How far back to search for papers")
    max_results: int = Field(20, ge=1, le=100, description="Max papers per researcher")


class ScrapeRunResponse(BaseModel):
    job_id: str
    chair_id: int
    message: str


class IngestPaperRequest(BaseModel):
    """Ingest a single paper by arXiv ID."""

    arxiv_id: str = Field(..., description="arXiv paper ID, e.g. '2301.07041'")
    researcher_id: int | None = Field(
        None,
        description="Link the paper to this researcher. If omitted the paper is stored without a researcher association.",
    )
