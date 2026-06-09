"""Unit tests for the Researcher ORM model: column presence, types, and nullability."""

from __future__ import annotations

import pytest
import sqlalchemy as sa

from app.models.researcher import Researcher, ResearcherPaper


@pytest.mark.unit
class TestResearcherColumns:
    """The columns added by migration 0013 must match the entity definition."""

    def _col(self, name: str) -> sa.Column:
        return Researcher.__table__.c[name]

    def test_title_is_nullable_string_255(self) -> None:
        col = self._col("title")
        assert isinstance(col.type, sa.String)
        assert col.type.length == 255
        assert col.nullable is True

    def test_role_is_nullable_string_255(self) -> None:
        col = self._col("role")
        assert isinstance(col.type, sa.String)
        assert col.type.length == 255
        assert col.nullable is True

    def test_email_is_nullable_string_320(self) -> None:
        col = self._col("email")
        assert isinstance(col.type, sa.String)
        assert col.type.length == 320
        assert col.nullable is True

    def test_profile_url_is_nullable_string_1000(self) -> None:
        col = self._col("profile_url")
        assert isinstance(col.type, sa.String)
        assert col.type.length == 1000
        assert col.nullable is True

    def test_source_url_is_nullable_string_1000(self) -> None:
        col = self._col("source_url")
        assert isinstance(col.type, sa.String)
        assert col.type.length == 1000
        assert col.nullable is True

    def test_name_is_required(self) -> None:
        col = self._col("name")
        assert col.nullable is False

    def test_is_professor_is_required_with_false_default(self) -> None:
        col = self._col("is_professor")
        assert col.nullable is False
        # The entity uses a Python-side default; DB-level server_default is set by migration 0010.
        assert col.default is not None
        assert col.default.arg is False

    def test_chair_id_is_nullable_with_fk(self) -> None:
        col = self._col("chair_id")
        assert col.nullable is True
        fk_targets = {fk.target_fullname for fk in col.foreign_keys}
        assert "chairs.id" in fk_targets

    def test_chair_id_is_indexed(self) -> None:
        indexed_cols = {
            frozenset(idx.columns.keys())
            for idx in Researcher.__table__.indexes
        }
        assert frozenset(["chair_id"]) in indexed_cols

    def test_profile_url_is_not_in_orm_unique_constraint(self) -> None:
        # The partial unique index (WHERE profile_url IS NOT NULL) is a DB-only
        # construct managed by migration 0013; it cannot be expressed as a standard
        # SQLAlchemy Column(unique=True). Confirm the column carries no ORM-level
        # unique flag so we don't accidentally generate a conflicting plain index.
        col = self._col("profile_url")
        assert col.unique is not True


@pytest.mark.unit
class TestResearcherPaperJoinTable:
    def test_primary_key_is_composite(self) -> None:
        pk_cols = {col.name for col in ResearcherPaper.__table__.primary_key}
        assert pk_cols == {"researcher_id", "paper_id"}

    def test_researcher_id_fk_cascades_delete(self) -> None:
        col = ResearcherPaper.__table__.c["researcher_id"]
        fk = next(iter(col.foreign_keys))
        assert fk.ondelete == "CASCADE"

    def test_paper_id_fk_cascades_delete(self) -> None:
        col = ResearcherPaper.__table__.c["paper_id"]
        fk = next(iter(col.foreign_keys))
        assert fk.ondelete == "CASCADE"
