"""Pydantic schemas for the scraper API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScrapeChairRequest(BaseModel):
    """Optional overrides for a chair scrape run."""

    since_days: int = Field(3650, ge=30, le=3650, description="How far back to search for papers")
    max_results: int = Field(250, ge=1, le=500, description="Max papers per researcher")


class ScrapeRunResponse(BaseModel):
    job_id: str
    chair_id: int
    message: str

