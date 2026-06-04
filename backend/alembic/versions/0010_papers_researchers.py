"""papers_researchers

Adds: papers, tags, paper_tags, researchers, researcher_papers tables
for the arXiv scraper pipeline.

Revision ID: 0010
Revises: 0009
Create Date: 2026-06-04
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0010"
down_revision: Union[str, None] = "0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ tags
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_tags_name"),
    )

    # ---------------------------------------------------------------- papers
    op.create_table(
        "papers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("arxiv_id", sa.String(length=50), nullable=True),
        sa.Column("doi", sa.String(length=100), nullable=True),
        sa.Column("title", sa.String(length=1000), nullable=False),
        sa.Column("title_normalized", sa.String(length=1000), nullable=False),
        sa.Column("abstract", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("authors", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("publication_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("source_url", sa.String(length=1000), nullable=False),
        sa.Column("recency_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("relevance_score", sa.Float(), nullable=False, server_default="0.0"),
        # pgvector column — use raw DDL so Alembic doesn't need pgvector installed
        sa.Column("enriched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("arxiv_id", name="uq_papers_arxiv_id"),
        sa.UniqueConstraint("doi", name="uq_papers_doi"),
    )
    # Add the pgvector column with raw DDL (type not known to plain SQLAlchemy)
    op.execute("ALTER TABLE papers ADD COLUMN embedding vector(2560)")

    op.create_index("ix_papers_arxiv_id", "papers", ["arxiv_id"], unique=False)
    op.create_index("ix_papers_doi", "papers", ["doi"], unique=False)
    op.create_index("ix_papers_publication_date", "papers", ["publication_date"], unique=False)

    # Dedup index for non-arxiv, non-doi papers: unique (title_normalized, first_author)
    op.execute(
        """
        CREATE UNIQUE INDEX uq_papers_title_author
            ON papers (title_normalized, (authors->>0))
            WHERE arxiv_id IS NULL AND doi IS NULL
        """
    )

    # ------------------------------------------------------------ paper_tags
    op.create_table(
        "paper_tags",
        sa.Column("paper_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["paper_id"], ["papers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("paper_id", "tag_id"),
    )

    # ----------------------------------------------------------- researchers
    op.create_table(
        "researchers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("google_scholar_id", sa.String(length=50), nullable=True),
        sa.Column("orcid", sa.String(length=50), nullable=True),
        sa.Column("affiliation", sa.String(length=500), nullable=True),
        sa.Column("chair_id", sa.Integer(), nullable=True),
        sa.Column("is_professor", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["chair_id"], ["chairs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("google_scholar_id", name="uq_researchers_scholar_id"),
        sa.UniqueConstraint("orcid", name="uq_researchers_orcid"),
    )
    op.create_index("ix_researchers_chair_id", "researchers", ["chair_id"], unique=False)

    # ------------------------------------------------------ researcher_papers
    op.create_table(
        "researcher_papers",
        sa.Column("researcher_id", sa.Integer(), nullable=False),
        sa.Column("paper_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["paper_id"], ["papers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["researcher_id"], ["researchers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("researcher_id", "paper_id"),
    )

    # --------------------------------- extend job_type enum with new values
    op.execute("ALTER TYPE job_type ADD VALUE IF NOT EXISTS 'scrape_chair'")
    op.execute("ALTER TYPE job_type ADD VALUE IF NOT EXISTS 'scrape_researcher'")
    op.execute("ALTER TYPE job_type ADD VALUE IF NOT EXISTS 'enrich_paper'")


def downgrade() -> None:
    op.drop_table("researcher_papers")
    op.drop_index("ix_researchers_chair_id", table_name="researchers")
    op.drop_table("researchers")
    op.drop_table("paper_tags")
    op.execute("DROP INDEX IF EXISTS uq_papers_title_author")
    op.drop_index("ix_papers_publication_date", table_name="papers")
    op.drop_index("ix_papers_doi", table_name="papers")
    op.drop_index("ix_papers_arxiv_id", table_name="papers")
    op.drop_table("papers")
    op.drop_table("tags")
    # Note: removing enum values from PostgreSQL requires recreating the type;
    # we leave the job_type enum additions in place on downgrade.
