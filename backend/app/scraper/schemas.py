"""Pydantic schemas for the scraper API."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field, Strict

from app.scraper.api_constants import (
    SCRAPE_MAX_RESULTS_DEFAULT,
    SCRAPE_MAX_RESULTS_MAX,
    SCRAPE_MAX_RESULTS_MIN,
    SCRAPE_SINCE_DAYS_DEFAULT,
    SCRAPE_SINCE_DAYS_MAX,
    SCRAPE_SINCE_DAYS_MIN,
)

StrictInteger = Annotated[int, Strict()]


class ScrapeChairRequest(BaseModel):
    """Optional overrides for a chair scrape run."""

    since_days: StrictInteger = Field(
        SCRAPE_SINCE_DAYS_DEFAULT,
        ge=SCRAPE_SINCE_DAYS_MIN,
        le=SCRAPE_SINCE_DAYS_MAX,
        description="How far back to search for papers",
    )
    max_results: StrictInteger = Field(
        SCRAPE_MAX_RESULTS_DEFAULT,
        ge=SCRAPE_MAX_RESULTS_MIN,
        le=SCRAPE_MAX_RESULTS_MAX,
        description="Max papers per researcher",
    )


class ScrapeRunResponse(BaseModel):
    job_id: str
    chair_id: int
    message: str
