"""Pydantic schemas for the researchers API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResearcherCreate(BaseModel):
    name: str
    chair_id: int | None = None
    orcid: str | None = None
    affiliation: str | None = None
    is_professor: bool = False


class ResearcherOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    chair_id: int | None
    orcid: str | None
    affiliation: str | None
    is_professor: bool
    created_at: datetime
