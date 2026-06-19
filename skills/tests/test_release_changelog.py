"""Tests for changelog finalization used by releases."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.release_changelog import ChangelogError, finalize_changelog, finalize_changelog_text


SAMPLE_CHANGELOG = """# Changelog

## [Unreleased]

### Added

- Skill-only release artifacts.

### Changed

- Release workflow publishes GitHub Release notes.

### Fixed

- Release artifacts exclude maintainer files.

### Removed

- Removed standalone pytest config.

### Breaking Changes

- None.

## [0.1.0] - 2026-06-19

### Added

- Initial skill package.
"""


def test_finalize_changelog_creates_version_section_and_resets_unreleased() -> None:
    new_text, notes = finalize_changelog_text(SAMPLE_CHANGELOG, "0.1.1", "2026-06-20")

    assert "## [Unreleased]\n\n### Added\n\n- ..." in new_text
    assert "## [0.1.1] - 2026-06-20" in new_text
    assert "## [0.1.0] - 2026-06-19" in new_text
    assert notes.startswith("## [0.1.1] - 2026-06-20")
    assert "Skill-only release artifacts." in notes
    assert "Initial skill package." not in notes


def test_finalize_changelog_writes_release_notes_file(tmp_path: Path) -> None:
    changelog = tmp_path / "CHANGELOG.md"
    notes = tmp_path / "dist" / "release-notes.md"
    changelog.write_text(SAMPLE_CHANGELOG, encoding="utf-8")

    release_notes = finalize_changelog(changelog, notes, "0.1.1", "2026-06-20")

    assert notes.read_text(encoding="utf-8") == release_notes
    assert "## [0.1.1] - 2026-06-20" in changelog.read_text(encoding="utf-8")


def test_finalize_changelog_rejects_missing_unreleased_section() -> None:
    with pytest.raises(ChangelogError):
        finalize_changelog_text("# Changelog\n", "0.1.1", "2026-06-20")


def test_finalize_changelog_rejects_empty_unreleased_section() -> None:
    text = """# Changelog

## [Unreleased]

### Added

- ...

### Breaking Changes

- None.
"""

    with pytest.raises(ChangelogError):
        finalize_changelog_text(text, "0.1.1", "2026-06-20")
