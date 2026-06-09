"""Integration test: migration 0013 upgrade and rollback.

Runs against a live PostgreSQL database. Skipped unless RUN_INTEGRATION=1 is set.

Usage:
    RUN_INTEGRATION=1 uv run pytest tests/integration/test_migration_0013.py -v
"""

from __future__ import annotations

import os

import pytest
from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, inspect, text

_SKIP = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="Set RUN_INTEGRATION=1 to run migration integration tests",
)

_NEW_COLUMNS = {"title", "role", "email", "profile_url", "source_url"}


def _sync_url() -> str:
    """Return a psycopg2-compatible URL from DATABASE_URL (which uses asyncpg)."""
    url = os.environ.get("DATABASE_URL", "postgresql+asyncpg://thesis:thesis@localhost:5433/thesis")
    return url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")


def _alembic_cfg() -> Config:
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", _sync_url())
    return cfg


def _current_revision(engine) -> str | None:
    with engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        return ctx.get_current_revision()


@pytest.fixture(scope="module")
def sync_engine():
    engine = create_engine(_sync_url())
    yield engine
    engine.dispose()


@_SKIP
@pytest.mark.integration
class TestMigration0013:
    def test_upgrade_adds_employee_columns(self, sync_engine) -> None:
        cfg = _alembic_cfg()

        # Ensure we start from 0012 by downgrading first if already at 0013.
        if _current_revision(sync_engine) == "0013":
            command.downgrade(cfg, "0012")

        assert _current_revision(sync_engine) == "0012"

        command.upgrade(cfg, "0013")

        cols = {col["name"] for col in inspect(sync_engine).get_columns("researchers")}
        assert _NEW_COLUMNS <= cols, f"Missing columns after upgrade: {_NEW_COLUMNS - cols}"

    def test_upgrade_creates_partial_unique_index(self, sync_engine) -> None:
        assert _current_revision(sync_engine) == "0013"

        index_names = {idx["name"] for idx in inspect(sync_engine).get_indexes("researchers")}
        assert "uq_researchers_profile_url" in index_names

    def test_partial_unique_index_enforced(self, sync_engine) -> None:
        """Two rows with the same non-NULL profile_url must be rejected."""
        assert _current_revision(sync_engine) == "0013"

        with sync_engine.begin() as conn:
            conn.execute(
                text("INSERT INTO researchers (name, profile_url, is_professor) VALUES ('A', 'https://example.com/a', false)")
            )
            with pytest.raises(Exception, match="uq_researchers_profile_url"):
                conn.execute(
                    text("INSERT INTO researchers (name, profile_url, is_professor) VALUES ('B', 'https://example.com/a', false)")
                )

    def test_null_profile_url_allows_duplicates(self, sync_engine) -> None:
        """NULL profile_url is excluded from the unique index — multiple NULLs are allowed."""
        assert _current_revision(sync_engine) == "0013"

        with sync_engine.begin() as conn:
            conn.execute(text("INSERT INTO researchers (name, is_professor) VALUES ('X', false)"))
            conn.execute(text("INSERT INTO researchers (name, is_professor) VALUES ('Y', false)"))
            # Both have NULL profile_url — should succeed without constraint violation.

    def test_downgrade_removes_employee_columns(self, sync_engine) -> None:
        cfg = _alembic_cfg()
        command.downgrade(cfg, "0012")

        assert _current_revision(sync_engine) == "0012"

        cols = {col["name"] for col in inspect(sync_engine).get_columns("researchers")}
        assert not (_NEW_COLUMNS & cols), f"Columns still present after downgrade: {_NEW_COLUMNS & cols}"

    def test_downgrade_removes_partial_unique_index(self, sync_engine) -> None:
        assert _current_revision(sync_engine) == "0012"

        index_names = {idx["name"] for idx in inspect(sync_engine).get_indexes("researchers")}
        assert "uq_researchers_profile_url" not in index_names

    def test_re_upgrade_restores_columns(self, sync_engine) -> None:
        """Re-applying the upgrade after a downgrade must be idempotent."""
        cfg = _alembic_cfg()
        command.upgrade(cfg, "0013")

        cols = {col["name"] for col in inspect(sync_engine).get_columns("researchers")}
        assert _NEW_COLUMNS <= cols
