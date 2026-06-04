"""SQLAlchemy models for the module handbook domain."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.skill import SkillTag


class ModuleHandbookEntry(Base):
    """One module from a university module handbook.

    The handbook is the authoritative source for mapping transcript courses to
    skill tags. Entries are versioned so multiple handbook editions can coexist.
    """

    __tablename__ = "module_handbook_entries"
    __table_args__ = (
        UniqueConstraint(
            "university_id",
            "handbook_version",
            "module_code",
            name="uq_handbook_entry_code",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    university_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    handbook_version: Mapped[str] = mapped_column(String(50), nullable=False)
    module_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    module_title: Mapped[str] = mapped_column(String(500), nullable=False)
    module_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    learning_outcomes: Mapped[str | None] = mapped_column(Text, nullable=True)
    contents: Mapped[str | None] = mapped_column(Text, nullable=True)
    prerequisites: Mapped[str | None] = mapped_column(Text, nullable=True)
    ects: Mapped[float | None] = mapped_column(Numeric(4, 1), nullable=True)
    # "bachelor" | "master" | "phd"
    level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # "de" | "en"
    language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    skill_mappings: Mapped[list["ModuleSkillMapping"]] = relationship(
        "ModuleSkillMapping",
        back_populates="handbook_entry",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ModuleSkillMapping(Base):
    """Links a handbook entry to a skill tag with a relevance score.

    This is the cached output of LLM-based skill tag generation. Re-running with
    the same (handbook_entry_id, llm_prompt_version, llm_input_hash) is a no-op.
    """

    __tablename__ = "module_skill_mappings"
    __table_args__ = (
        UniqueConstraint(
            "handbook_entry_id",
            "skill_tag_id",
            name="uq_module_skill_mapping",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    handbook_entry_id: Mapped[int] = mapped_column(
        ForeignKey("module_handbook_entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_tag_id: Mapped[int] = mapped_column(
        ForeignKey("skill_tags.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # How central this skill is to the module (0.0-1.0).
    relevance: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    # "llm_generated" | "manual"
    source: Mapped[str] = mapped_column(String(30), nullable=False, default="llm_generated")
    llm_prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    llm_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # SHA-256 of the module text fields sent to the LLM — used for cache invalidation.
    llm_input_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    handbook_entry: Mapped["ModuleHandbookEntry"] = relationship(
        "ModuleHandbookEntry", back_populates="skill_mappings"
    )
    skill_tag: Mapped["SkillTag"] = relationship("SkillTag")  # type: ignore[name-defined]
