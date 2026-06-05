"""SQLAlchemy models for papers, tags, and the paper-tag join table."""

from datetime import datetime
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.thesis import EMBEDDING_DIM

if TYPE_CHECKING:
    from app.models.researcher import ResearcherPaper


class Tag(Base):
    """Canonical, lowercase tag (e.g. 'machine learning', 'robotics')."""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    papers: Mapped[list["PaperTag"]] = relationship("PaperTag", back_populates="tag", cascade="all, delete-orphan")


class PaperTag(Base):
    """Join table linking papers to their tags."""

    __tablename__ = "paper_tags"

    paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    paper: Mapped["Paper"] = relationship("Paper", back_populates="tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="papers")


class Paper(Base):
    """A research paper discovered and enriched by the scraper pipeline."""

    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Canonical identifiers
    arxiv_id: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True, index=True)
    doi: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True)
    # Content
    title: Mapped[str] = mapped_column(String(1000), nullable=False)
    # Lowercased, punctuation-stripped version for dedup lookups
    title_normalized: Mapped[str] = mapped_column(String(1000), nullable=False)
    abstract: Mapped[str | None] = mapped_column(Text, nullable=True)
    # LLM-generated summary
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON array of author name strings, e.g. ["Alice Smith", "Bob Jones"]
    authors: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    publication_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    # First source that discovered this paper
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    source_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    # Scoring
    recency_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    # Vector embedding of abstract (for semantic search)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM), nullable=True)
    # NULL means not yet enriched by LLM
    enriched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    tags: Mapped[list["PaperTag"]] = relationship("PaperTag", back_populates="paper", cascade="all, delete-orphan")
    researchers: Mapped[list["ResearcherPaper"]] = relationship("ResearcherPaper", back_populates="paper", cascade="all, delete-orphan")
