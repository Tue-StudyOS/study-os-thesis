"""Pydantic schemas for the handbook domain."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HandbookEntryData(BaseModel):
    """Intermediate: one parsed module entry before DB persistence."""

    university_id: str = ""
    handbook_version: str = ""
    module_code: str | None = None
    module_title: str = Field(min_length=1, max_length=500)
    module_title_en: str | None = Field(default=None, max_length=500)
    description: str | None = None
    learning_outcomes: str | None = None
    contents: str | None = None
    prerequisites: str | None = None
    ects: float | None = None
    level: str | None = None  # "bachelor" | "master" | "phd"
    language: str | None = None  # "de" | "en"


class HandbookEntryOut(BaseModel):
    """API response for a single handbook entry."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    university_id: str
    handbook_version: str
    module_code: str | None
    module_title: str
    module_title_en: str | None
    ects: float | None
    level: str | None
    created_at: datetime


class HandbookVersionOut(BaseModel):
    """Summary of one ingested handbook version."""

    university_id: str
    handbook_version: str
    module_count: int


class HandbookIngestResult(BaseModel):
    """Result returned by the ingest_handbook Celery task."""

    university_id: str
    handbook_version: str
    modules_ingested: int
    modules_skipped: int
    warnings: list[str]
