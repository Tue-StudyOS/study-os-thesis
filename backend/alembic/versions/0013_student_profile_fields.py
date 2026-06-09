"""Add full_name and education_level to students table.

Revision ID: 0013
Revises: 0012
Create Date: 2026-06-09
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0013"
down_revision: Union[str, None] = "0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "students",
        sa.Column("full_name", sa.String(255), nullable=True),
    )
    op.add_column(
        "students",
        sa.Column("education_level", sa.String(20), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("students", "education_level")
    op.drop_column("students", "full_name")
