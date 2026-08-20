"""Checks for the single-folder Claude-app skill bundle."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pytest

from scripts.build_app_bundle import (
    ROOT_SESSION_NOTE,
    BUNDLED_DIR,
    BUNDLED_INSTRUCTIONS,
    EXCLUDED_SKILLS,
    ROOT_SKILL,
    AppBundleError,
    build_app_bundle,
    override_session_location,
    rewrite_bundled_skill,
    rewrite_root_skill,
)
from scripts.build_skill_release import read_project_version


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
BACKTICKED_PATH_PATTERN = re.compile(r"`([a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)+\.md)`")


def test_bundle_is_one_uploadable_skill_folder(tmp_path: Path) -> None:
    package_dir, zip_path = build_app_bundle(tmp_path)

    # A client that takes one skill per upload reads the frontmatter of the SKILL.md at
    # the root. Anything else at the root, or a second root folder in the archive, makes
    # the upload ambiguous.
    assert package_dir.name == ROOT_SKILL
    assert (package_dir / "SKILL.md").is_file()
    assert {path.name for path in package_dir.iterdir()} == {"SKILL.md", BUNDLED_DIR}

    with zipfile.ZipFile(zip_path) as zip_file:
        names = zip_file.namelist()
    assert names, "archive is empty"
    assert {name.split("/")[0] for name in names} == {ROOT_SKILL}
    assert f"{ROOT_SKILL}/SKILL.md" in names

    assert zip_path.name == f"{ROOT_SKILL}-app-v{read_project_version()}.zip"


def test_bundle_carries_every_skill_the_flow_hands_off_to(tmp_path: Path) -> None:
    package_dir, _ = build_app_bundle(tmp_path)

    source_names = {path.name for path in SKILLS_DIR.iterdir() if path.is_dir() and path.name != "tests"}
    expected = source_names - EXCLUDED_SKILLS - {ROOT_SKILL}
    bundled = {path.name for path in (package_dir / BUNDLED_DIR).iterdir() if path.is_dir()}
    assert bundled == expected

    # The routing table is what replaces the client's own skill routing. A skill missing
    # from it is a hand-off the agent cannot follow.
    root_text = (package_dir / "SKILL.md").read_text(encoding="utf-8")
    for name in expected:
        assert f"`{BUNDLED_DIR}/{name}/{BUNDLED_INSTRUCTIONS}`" in root_text
        assert (package_dir / BUNDLED_DIR / name / BUNDLED_INSTRUCTIONS).is_file()


def test_every_path_in_the_bundle_resolves_inside_the_bundle(tmp_path: Path) -> None:
    package_dir, _ = build_app_bundle(tmp_path)

    for markdown in sorted(package_dir.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        location = markdown.relative_to(package_dir)

        # `../build-student-profile/...` resolves when the ten skills are siblings on a
        # filesystem. In an uploaded bundle it points outside the package and the agent
        # silently continues without the file.
        assert "`../" not in text, f"{location} reaches outside the bundle"

        for reference in BACKTICKED_PATH_PATTERN.findall(text):
            if reference.startswith(f"{BUNDLED_DIR}/"):
                assert (package_dir / reference).exists(), f"{location} points at missing {reference}"


def test_bundled_skills_lose_their_folder_relative_reference_paths(tmp_path: Path) -> None:
    package_dir, _ = build_app_bundle(tmp_path)

    for instructions in sorted((package_dir / BUNDLED_DIR).rglob(BUNDLED_INSTRUCTIONS)):
        text = instructions.read_text(encoding="utf-8")
        # `references/x.md` resolved against the skill's own folder when it was installed
        # as its own skill; inside the bundle it would resolve against the bundle root.
        # A bare `references/` naming the directory in prose is not a path and stays put.
        leftover = re.findall(r"`(references/[^`]+)`", text)
        assert not leftover, f"{instructions.relative_to(package_dir)} kept un-rewritten paths {leftover}"


def test_sources_are_left_untouched(tmp_path: Path) -> None:
    before = {
        path: path.read_bytes()
        for path in sorted(SKILLS_DIR.rglob("SKILL.md"))
    }
    build_app_bundle(tmp_path)
    after = {path: path.read_bytes() for path in sorted(SKILLS_DIR.rglob("SKILL.md"))}
    assert before == after


def test_rewrites_repoint_paths_at_the_bundle_root() -> None:
    bundled = rewrite_bundled_skill("see `references/search-strategy.md` now", "find-university-chairs")
    assert bundled == "see `skills/find-university-chairs/references/search-strategy.md` now"

    root = rewrite_root_skill("use `../build-student-profile/references/x.md`", ["build-student-profile"])
    assert root == "use `skills/build-student-profile/references/x.md`"


def test_a_handoff_to_an_unbundled_skill_fails_the_build() -> None:
    with pytest.raises(AppBundleError, match="not in the bundle"):
        rewrite_root_skill("use `../design-agent-skill/references/x.md`", ["build-student-profile"])


def test_the_filesystem_path_is_overridden_where_it_is_read(tmp_path: Path) -> None:
    package_dir, _ = build_app_bundle(tmp_path)
    root_text = (package_dir / "SKILL.md").read_text(encoding="utf-8")

    # The override has to sit at the heading, not only in the preamble: an agent
    # reading Step 0 must not try to resolve ~/.claude/thesis-finder/session.md.
    heading_at = root_text.index("Session File Location")
    note_at = root_text.index(ROOT_SESSION_NOTE)
    path_at = root_text.index("`~/.claude/thesis-finder/session.md`")
    assert heading_at < note_at < path_at


def test_a_renamed_session_section_fails_the_build_rather_than_dropping_the_override() -> None:
    with pytest.raises(AppBundleError, match="Session File Location"):
        override_session_location("# Some Skill\n\nno such heading\n", "x/SKILL.md", "note")
