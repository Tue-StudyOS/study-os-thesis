"""SQLAlchemy models for researchers and the researcher-paper join table."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Researcher(Base):
    """A researcher (professor or team member) associated with a chair."""

    __tablename__ = "researchers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # Academic/job title as shown on the chair page, e.g. "Prof. Dr.", "PhD candidate".
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Position within the chair, e.g. "Professor", "Research Associate", "PhD Student".
    role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    # Personal profile page (used as a dedup key for discovered employees).
    profile_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    # The page the employee was discovered on (provenance).
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    orcid: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    affiliation: Mapped[str | None] = mapped_column(String(500), nullable=True)
    chair_id: Mapped[int | None] = mapped_column(ForeignKey("chairs.id", ondelete="SET NULL"), nullable=True, index=True)
    is_professor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    papers: Mapped[list["ResearcherPaper"]] = relationship("ResearcherPaper", back_populates="researcher", cascade="all, delete-orphan")


class ResearcherPaper(Base):
    """Join table linking researchers to papers they authored."""

    __tablename__ = "researcher_papers"

    researcher_id: Mapped[int] = mapped_column(Integer, ForeignKey("researchers.id", ondelete="CASCADE"), primary_key=True)
    paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)

    researcher: Mapped["Researcher"] = relationship("Researcher", back_populates="papers")
    paper: Mapped["Paper"] = relationship("Paper", back_populates="researchers")  # type: ignore[name-defined]  # noqa: F821
