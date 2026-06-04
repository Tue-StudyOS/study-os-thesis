"""Pydantic schemas for the skills API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SkillEvidenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=False)

    course_name: str
    credits: float | None
    grade: str | None
    handbook_module: str | None   # module_title of the matched handbook entry
    match_method: str
    match_confidence: float
    contribution: float           # raw_contribution


class UserSkillItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill: str              # canonical name, e.g. "machine learning"
    category: str | None
    score: float            # 0.0-1.0
    evidence: list[SkillEvidenceOut] = []


class UserSkillProfileOut(BaseModel):
    user_id: int
    computation_run_id: str | None
    computed_at: datetime | None
    skills: list[UserSkillItemOut]
    unmatched_courses: list[str]
    warnings: list[str]
