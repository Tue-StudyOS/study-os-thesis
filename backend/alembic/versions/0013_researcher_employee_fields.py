"""Add university-employee fields to researchers.

Adds title, role, email, profile_url, source_url to the researchers table so a
chair-discovery agent can persist team members, plus a partial unique index on
profile_url to avoid duplicate employees sharing the same profile page.

Revision ID: 0013
Revises: 0012
Create Date: 2026-06-08
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0013"
down_revision: Union[str, None] = "0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("researchers", sa.Column("title", sa.String(length=255), nullable=True))
    op.add_column("researchers", sa.Column("role", sa.String(length=255), nullable=True))
    op.add_column("researchers", sa.Column("email", sa.String(length=320), nullable=True))
    op.add_column("researchers", sa.Column("profile_url", sa.String(length=1000), nullable=True))
    op.add_column("researchers", sa.Column("source_url", sa.String(length=1000), nullable=True))

    # Two discovered employees with the same profile page are the same person.
    op.create_index(
        "uq_researchers_profile_url",
        "researchers",
        ["profile_url"],
        unique=True,
        postgresql_where=sa.text("profile_url IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_researchers_profile_url", table_name="researchers")
    op.drop_column("researchers", "source_url")
    op.drop_column("researchers", "profile_url")
    op.drop_column("researchers", "email")
    op.drop_column("researchers", "role")
    op.drop_column("researchers", "title")
