"""Collapse DOI/NULL duplicate papers and guarantee the dedup unique index.

The tier-2 dedup (title_normalized, authors->>0) only matched DOI-less existing
rows, so a DOI-less re-scrape of a paper first stored *with* a DOI was treated
as new and inserted as a duplicate. The partial unique index from 0012
(``WHERE doi IS NULL``) does not cover this asymmetric pair. This migration
removes such duplicates — keeping the DOI-bearing row and re-pointing the
DOI-less twin's researcher/tag links to it — and (re)asserts the index.

Revision ID: 0013
Revises: 0012
Create Date: 2026-06-07
"""

from typing import Sequence, Union

from alembic import op

revision: str = "0013"
down_revision: Union[str, None] = "0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Shared CTE: for each (title_normalized, authors->>0) group pick a keeper —
# preferring a DOI-bearing row, else the lowest id — and list the DOI-less rows
# that should be folded into it.
_DUPLICATES_CTE = """
WITH groups AS (
    SELECT
        title_normalized,
        authors->>0 AS first_author,
        COALESCE(min(id) FILTER (WHERE doi IS NOT NULL), min(id)) AS keep_id
    FROM papers
    WHERE title_normalized IS NOT NULL
      AND authors->>0 IS NOT NULL
    GROUP BY title_normalized, authors->>0
),
duplicates AS (
    SELECT p.id AS dup_id, g.keep_id
    FROM papers p
    JOIN groups g
      ON g.title_normalized = p.title_normalized
     AND g.first_author = p.authors->>0
    WHERE p.doi IS NULL
      AND p.id <> g.keep_id
)
"""


def _collapse_doi_null_duplicates() -> None:
    op.execute(
        _DUPLICATES_CTE
        + """
        INSERT INTO researcher_papers (researcher_id, paper_id)
        SELECT rp.researcher_id, d.keep_id
        FROM researcher_papers rp
        JOIN duplicates d ON d.dup_id = rp.paper_id
        ON CONFLICT DO NOTHING
        """
    )
    op.execute(
        _DUPLICATES_CTE
        + """
        INSERT INTO paper_tags (paper_id, tag_id)
        SELECT d.keep_id, pt.tag_id
        FROM paper_tags pt
        JOIN duplicates d ON d.dup_id = pt.paper_id
        ON CONFLICT DO NOTHING
        """
    )
    # FK cascade removes the dup rows' own links once the papers are deleted.
    op.execute(
        _DUPLICATES_CTE
        + """
        DELETE FROM papers
        WHERE id IN (SELECT dup_id FROM duplicates)
        """
    )


def upgrade() -> None:
    _collapse_doi_null_duplicates()
    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS uq_papers_title_author
            ON papers (title_normalized, (authors->>0))
            WHERE doi IS NULL
        """
    )


def downgrade() -> None:
    # Data cleanup cannot be reversed; leave the index to 0012's downgrade.
    pass
