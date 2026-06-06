"""Remove stale arXiv and Scholar schema.

Revision ID: 0012
Revises: 0011
Create Date: 2026-06-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0012"
down_revision: Union[str, None] = "0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _replace_enum(table: str, column: str, enum_name: str, values: tuple[str, ...]) -> None:
    tmp_name = f"{enum_name}_new"
    quoted_values = ", ".join(f"'{value}'" for value in values)
    op.execute(f"CREATE TYPE {tmp_name} AS ENUM ({quoted_values})")
    op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE {tmp_name} USING {column}::text::{tmp_name}")
    op.execute(f"DROP TYPE {enum_name}")
    op.execute(f"ALTER TYPE {tmp_name} RENAME TO {enum_name}")


def _deduplicate_title_author_papers() -> None:
    """Collapse legacy duplicates before adding the provider-neutral index."""
    op.execute(
        """
        WITH ranked AS (
            SELECT
                id,
                first_value(id) OVER (
                    PARTITION BY title_normalized, authors->>0
                    ORDER BY publication_date DESC NULLS LAST, id ASC
                ) AS keep_id,
                row_number() OVER (
                    PARTITION BY title_normalized, authors->>0
                    ORDER BY publication_date DESC NULLS LAST, id ASC
                ) AS rn
            FROM papers
            WHERE doi IS NULL
              AND title_normalized IS NOT NULL
              AND authors->>0 IS NOT NULL
        ),
        duplicates AS (
            SELECT id, keep_id
            FROM ranked
            WHERE rn > 1
        )
        INSERT INTO researcher_papers (researcher_id, paper_id)
        SELECT rp.researcher_id, d.keep_id
        FROM researcher_papers rp
        JOIN duplicates d ON d.id = rp.paper_id
        ON CONFLICT DO NOTHING
        """
    )
    op.execute(
        """
        WITH ranked AS (
            SELECT
                id,
                first_value(id) OVER (
                    PARTITION BY title_normalized, authors->>0
                    ORDER BY publication_date DESC NULLS LAST, id ASC
                ) AS keep_id,
                row_number() OVER (
                    PARTITION BY title_normalized, authors->>0
                    ORDER BY publication_date DESC NULLS LAST, id ASC
                ) AS rn
            FROM papers
            WHERE doi IS NULL
              AND title_normalized IS NOT NULL
              AND authors->>0 IS NOT NULL
        ),
        duplicates AS (
            SELECT id, keep_id
            FROM ranked
            WHERE rn > 1
        )
        INSERT INTO paper_tags (paper_id, tag_id)
        SELECT d.keep_id, pt.tag_id
        FROM paper_tags pt
        JOIN duplicates d ON d.id = pt.paper_id
        ON CONFLICT DO NOTHING
        """
    )
    op.execute(
        """
        WITH ranked AS (
            SELECT
                id,
                row_number() OVER (
                    PARTITION BY title_normalized, authors->>0
                    ORDER BY publication_date DESC NULLS LAST, id ASC
                ) AS rn
            FROM papers
            WHERE doi IS NULL
              AND title_normalized IS NOT NULL
              AND authors->>0 IS NOT NULL
        )
        DELETE FROM papers
        WHERE id IN (SELECT id FROM ranked WHERE rn > 1)
        """
    )


def upgrade() -> None:
    # Compare via ::text so the literals are not cast to the job_type enum. One
    # of these values (ingest_single_paper) is added via ALTER TYPE ADD VALUE in
    # 0010; Postgres forbids referencing such a value in the same transaction it
    # was added, which happens when all migrations run in one transaction.
    op.execute("DELETE FROM jobs WHERE type::text IN ('ingest_arxiv', 'ingest_single_paper')")
    op.execute("DELETE FROM chair_documents WHERE kind = 'paper'")

    op.drop_index("ix_papers_arxiv_id", table_name="papers")
    op.drop_constraint("uq_papers_arxiv_id", "papers", type_="unique")
    op.execute("DROP INDEX IF EXISTS uq_papers_title_author")
    op.drop_column("papers", "arxiv_id")
    _deduplicate_title_author_papers()
    op.execute(
        """
        CREATE UNIQUE INDEX uq_papers_title_author
            ON papers (title_normalized, (authors->>0))
            WHERE doi IS NULL
        """
    )

    op.drop_constraint("uq_chair_documents_chair_arxiv", "chair_documents", type_="unique")
    op.drop_column("chair_documents", "arxiv_id")

    op.drop_constraint("uq_researchers_scholar_id", "researchers", type_="unique")
    op.drop_column("researchers", "google_scholar_id")

    _replace_enum(
        "jobs",
        "type",
        "job_type",
        (
            "embed_thesis",
            "embed_chair",
            "parse_transcript",
            "chat_turn",
            "generate_proposal",
            "scrape_chair",
            "scrape_researcher",
            "enrich_paper",
        ),
    )
    _replace_enum("chair_documents", "kind", "chair_document_kind", ("description",))


def downgrade() -> None:
    _replace_enum("chair_documents", "kind", "chair_document_kind", ("description", "paper"))
    _replace_enum(
        "jobs",
        "type",
        "job_type",
        (
            "embed_thesis",
            "embed_chair",
            "ingest_arxiv",
            "parse_transcript",
            "chat_turn",
            "generate_proposal",
            "scrape_chair",
            "scrape_researcher",
            "enrich_paper",
            "ingest_single_paper",
        ),
    )

    op.add_column("researchers", sa.Column("google_scholar_id", sa.String(length=50), nullable=True))
    op.create_unique_constraint("uq_researchers_scholar_id", "researchers", ["google_scholar_id"])

    op.add_column("chair_documents", sa.Column("arxiv_id", sa.String(length=50), nullable=True))
    op.create_unique_constraint("uq_chair_documents_chair_arxiv", "chair_documents", ["chair_id", "arxiv_id"])

    op.execute("DROP INDEX IF EXISTS uq_papers_title_author")
    op.add_column("papers", sa.Column("arxiv_id", sa.String(length=50), nullable=True))
    op.create_unique_constraint("uq_papers_arxiv_id", "papers", ["arxiv_id"])
    op.create_index("ix_papers_arxiv_id", "papers", ["arxiv_id"], unique=False)
    op.execute(
        """
        CREATE UNIQUE INDEX uq_papers_title_author
            ON papers (title_normalized, (authors->>0))
            WHERE arxiv_id IS NULL AND doi IS NULL
        """
    )
