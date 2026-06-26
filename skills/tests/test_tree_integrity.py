"""Referential-integrity checks for the Prof -> researcher -> Paper Markdown tree.

These guard the bundled Tuebingen tree and prove the faculty-agnostic validator
fails on orphaned references, so a broken tree cannot pass CI.
"""

from __future__ import annotations

from pathlib import Path

from scripts.update_openalex_index import BuildConfig, validate_references


def test_bundled_tree_has_no_orphaned_references() -> None:
    assert validate_references() == []


def _make_faculty(tmp_path: Path, *, paper_person: str = "alice", chair_member: str = "alice") -> BuildConfig:
    researchers_index = tmp_path / "researchers" / "INDEX.md"
    chairs_index = tmp_path / "chairs" / "INDEX.md"
    papers_dir = tmp_path / "papers"
    researchers_index.parent.mkdir(parents=True)
    chairs_index.parent.mkdir(parents=True)
    papers_dir.mkdir(parents=True)

    researchers_index.write_text(
        "# Researcher Index\n\n"
        "| slug | name | role | chair_slug | openalex_author_id | keywords | last_updated |\n"
        "|---|---|---|---|---|---|---|\n"
        "| alice | Alice | professor | lab-x | A1 | ml | 2026-01-01 |\n",
        encoding="utf-8",
    )
    chairs_index.write_text(
        "# Chair Index\n\n"
        "| slug | name | university | department | researchers | keywords | last_updated |\n"
        "|---|---|---|---|---|---|---|\n"
        f"| lab-x | Lab X | U | CS | {chair_member} | ml | 2026-01-01 |\n",
        encoding="utf-8",
    )
    (papers_dir / "INDEX.md").write_text(
        "# Paper Index\n\n"
        "| title | year | researchers | chairs | keywords | doi | openalex | updated |\n"
        "|---|---|---|---|---|---|---|---|\n"
        f"| Paper One | 2026 | {paper_person} | lab-x | ml |  | W1 | 2026-01-01 |\n",
        encoding="utf-8",
    )
    return BuildConfig(researchers_index=researchers_index, chairs_index=chairs_index, papers_dir=papers_dir)


def test_clean_synthetic_faculty_passes(tmp_path: Path) -> None:
    assert validate_references(_make_faculty(tmp_path)) == []


def test_orphaned_paper_person_is_flagged(tmp_path: Path) -> None:
    errors = validate_references(_make_faculty(tmp_path, paper_person="ghost"))
    assert any("ghost" in error for error in errors)


def test_orphaned_chair_member_is_flagged(tmp_path: Path) -> None:
    errors = validate_references(_make_faculty(tmp_path, chair_member="ghost"))
    assert any("ghost" in error for error in errors)


def test_faculty_specific_extra_columns_do_not_break_validation(tmp_path: Path) -> None:
    config = _make_faculty(tmp_path)
    text = config.researchers_index.read_text(encoding="utf-8")
    text = text.replace("last_updated |", "last_updated | themenbereich |")
    text = text.replace("| 2026-01-01 |", "| 2026-01-01 | robotics |")
    config.researchers_index.write_text(text, encoding="utf-8")

    assert validate_references(config) == []
