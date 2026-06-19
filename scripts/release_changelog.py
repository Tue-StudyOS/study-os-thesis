"""Finalize CHANGELOG.md and extract release notes for a skill package release."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_skill_release import read_project_version  # noqa: E402

DEFAULT_CHANGELOG = REPO_ROOT / "CHANGELOG.md"
DEFAULT_NOTES = REPO_ROOT / "dist" / "release-notes.md"
UNRELEASED_HEADING = "## [Unreleased]"
RELEASE_HEADING_PATTERN = re.compile(r"^## \[[^\]]+\](?: - \d{4}-\d{2}-\d{2})?\s*$", re.MULTILINE)
CONTENT_LINE_PATTERN = re.compile(r"^\s*-\s+(?!(?:None\.?|\.\.\.)\s*$).+", re.MULTILINE)
DEFAULT_UNRELEASED_BODY = """### Added

- ...

### Changed

- ...

### Fixed

- ...

### Removed

- ...

### Breaking Changes

- None.
"""


class ChangelogError(RuntimeError):
    """Raised when CHANGELOG.md cannot be finalized safely."""


def _today_utc() -> str:
    return datetime.now(UTC).date().isoformat()


def _find_unreleased(text: str) -> tuple[re.Match[str], int]:
    match = re.search(rf"^{re.escape(UNRELEASED_HEADING)}\s*$", text, flags=re.MULTILINE)
    if not match:
        raise ChangelogError(f"{UNRELEASED_HEADING} section is missing")

    next_release = RELEASE_HEADING_PATTERN.search(text, match.end())
    end = next_release.start() if next_release else len(text)
    return match, end


def _validate_unreleased_body(body: str) -> None:
    if not CONTENT_LINE_PATTERN.search(body):
        raise ChangelogError(f"{UNRELEASED_HEADING} must contain at least one non-placeholder change item")
    if "### Breaking Changes" not in body:
        raise ChangelogError(f"{UNRELEASED_HEADING} must include a Breaking Changes section")


def finalize_changelog_text(text: str, version: str, release_date: str) -> tuple[str, str]:
    unreleased_match, unreleased_end = _find_unreleased(text)
    unreleased_body = text[unreleased_match.end() : unreleased_end].strip()
    _validate_unreleased_body(unreleased_body)

    release_notes = f"## [{version}] - {release_date}\n\n{unreleased_body}\n"
    replacement = f"{UNRELEASED_HEADING}\n\n{DEFAULT_UNRELEASED_BODY}\n{release_notes}"
    new_text = text[: unreleased_match.start()] + replacement + text[unreleased_end:].lstrip("\n")
    if not new_text.endswith("\n"):
        new_text += "\n"
    return new_text, release_notes


def finalize_changelog(changelog_path: Path, notes_path: Path, version: str, release_date: str) -> str:
    text = changelog_path.read_text(encoding="utf-8")
    new_text, release_notes = finalize_changelog_text(text, version, release_date)

    changelog_path.write_text(new_text, encoding="utf-8")
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text(release_notes, encoding="utf-8")
    return release_notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize CHANGELOG.md for the current project version.")
    parser.add_argument("--changelog", type=Path, default=DEFAULT_CHANGELOG)
    parser.add_argument("--notes", type=Path, default=DEFAULT_NOTES)
    parser.add_argument("--version", default=read_project_version())
    parser.add_argument("--date", default=_today_utc())
    args = parser.parse_args()

    try:
        finalize_changelog(args.changelog, args.notes, args.version, args.date)
    except ChangelogError as error:
        parser.exit(status=1, message=f"error: {error}\n")

    print(args.notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
