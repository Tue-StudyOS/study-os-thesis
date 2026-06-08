"""Pydantic schemas for the researchers API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResearcherCreate(BaseModel):
    name: str
    chair_id: int | None = None
    title: str | None = None
    role: str | None = None
    email: str | None = None
    profile_url: str | None = None
    source_url: str | None = None
    orcid: str | None = None
    affiliation: str | None = None
    is_professor: bool = False


class ResearcherOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    chair_id: int | None
    title: str | None
    role: str | None
    email: str | None
    profile_url: str | None
    source_url: str | None
    orcid: str | None
    affiliation: str | None
    is_professor: bool
    created_at: datetime
