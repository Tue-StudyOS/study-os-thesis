"""Add professor_title to chairs; split titles from professor_name.

Revision ID: 0011
Revises: 0010
Create Date: 2026-06-04
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0011"
down_revision: Union[str, None] = "0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("chairs", sa.Column("professor_title", sa.String(length=255), nullable=True))

    # Extract leading academic titles into professor_title and keep the remaining
    # portion as professor_name. This avoids losing the title while still
    # providing a canonical name for scraping.
    # Note: PostgreSQL uses POSIX regex; avoid PCRE-only constructs like (?:...).
    # Single backslashes in the raw string produce \s / \. for PostgreSQL's regex
    # engine, which supports \s as a whitespace shorthand (Perl extension).
    title_re = r"^\s*((Professor|Prof)\.?\s*|Dr(\.-Ing\.)?\.?\s*)+"
    op.execute(
        sa.text(
            """
            UPDATE chairs
            SET
                professor_title = NULLIF(btrim(substring(professor_name from :title_re)), ''),
                professor_name = btrim(regexp_replace(professor_name, :title_re, '', 'i'))
            """
        ).bindparams(sa.bindparam("title_re", title_re))
    )


def downgrade() -> None:
    op.drop_column("chairs", "professor_title")
