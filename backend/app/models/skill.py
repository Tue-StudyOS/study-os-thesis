"""SQLAlchemy models for the skill computation domain."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, SmallInteger, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class SkillTag(Base):
    """Canonical skill name in the normalized taxonomy.

    Raw tags from the LLM (and alternative spellings / translations) are stored
    as ``aliases``.  Normalization resolves any alias to the canonical ``name``.
    """

    __tablename__ = "skill_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Lowercase canonical name, e.g. "machine learning", "operating systems".
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # e.g. "programming" | "mathematics" | "theory" | "systems" | "data" |
    #       "engineering" | "research" | "other"
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # JSON array of alternative spellings/translations, e.g.
    # ["ML", "maschinelles lernen", "statistical learning"].
    aliases: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class UserSkill(Base):
    """Computed skill score for one user x skill pair.

    Scores are normalized to [0.0, 1.0].  Each row is linked to the
    SkillComputationRun that produced it for full auditability.
    """

    __tablename__ = "user_skills"
    __table_args__ = (
        UniqueConstraint("user_id", "skill_tag_id", name="uq_user_skill"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    skill_tag_id: Mapped[int] = mapped_column(
        ForeignKey("skill_tags.id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    computation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("skill_computation_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    skill_tag: Mapped["SkillTag"] = relationship("SkillTag", lazy="joined")
    evidence: Mapped[list["SkillEvidence"]] = relationship(
        "SkillEvidence", back_populates="user_skill", cascade="all, delete-orphan", lazy="selectin"
    )


class SkillEvidence(Base):
    """Per-module explanation for a user skill score.

    Each row records the exact factor values used to compute the contribution
    from one transcript course to one skill, making scores fully explainable.
    """

    __tablename__ = "skill_evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_skill_id: Mapped[int] = mapped_column(
        ForeignKey("user_skills.id", ondelete="CASCADE"), nullable=False, index=True
    )
    student_course_id: Mapped[int] = mapped_column(
        ForeignKey("student_courses.id", ondelete="CASCADE"), nullable=False
    )
    handbook_entry_id: Mapped[int | None] = mapped_column(
        ForeignKey("module_handbook_entries.id", ondelete="SET NULL"), nullable=True
    )
    # "exact_code" | "title_exact" | "title_fuzzy" | "semantic"
    match_method: Mapped[str] = mapped_column(String(30), nullable=False)
    match_confidence: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    module_skill_relevance: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    credits_used: Mapped[float | None] = mapped_column(Numeric(4, 1), nullable=True)
    grade_factor: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    level_factor: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    recency_factor: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    raw_contribution: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)
    computation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("skill_computation_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_skill: Mapped["UserSkill"] = relationship("UserSkill", back_populates="evidence")


class SkillComputationRun(Base):
    """Audit log of every skill computation invocation.

    Stores the configuration snapshot, match statistics, warnings, and
    timestamps for each run.  Links to the background ``jobs`` row so the
    frontend can poll status via the existing job API.
    """

    __tablename__ = "skill_computation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # "pending" | "running" | "completed" | "failed"
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    handbook_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    university_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    total_courses: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    matched_courses: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    # JSON array of course names that had no handbook match.
    unmatched_courses: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    # JSON array of human-readable warning strings.
    warnings: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    # Snapshot of the ScoringConfig used for this run.
    config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user_skills: Mapped[list["UserSkill"]] = relationship(
        "UserSkill",
        primaryjoin="SkillComputationRun.id == foreign(UserSkill.computation_run_id)",
        viewonly=True,
    )
