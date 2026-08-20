"""Checks for the single-file portable edition used by ChatGPT and Gemini."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from scripts.build_app_bundle import EXCLUDED_SKILLS, ROOT_SKILL
from scripts.build_portable_bundle import (
    INSTRUCTIONS_LIMIT,
    PortableBundleError,
    build_portable_bundle,
    demote_headings,
    reference_heading,
    rewrite_references,
    skill_heading,
)
from scripts.build_skill_release import read_project_version


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"


def _expected_skills() -> set[str]:
    names = {path.name for path in SKILLS_DIR.iterdir() if path.is_dir() and path.name != "tests"}
    return names - EXCLUDED_SKILLS


def test_portable_edition_is_one_file_with_every_skill_in_it(tmp_path: Path) -> None:
    document_path, instructions_path = build_portable_bundle(tmp_path)

    version = read_project_version()
    assert document_path.name == f"thesis-finder-portable-v{version}.md"
    assert instructions_path.name == f"thesis-finder-portable-instructions-v{version}.txt"

    document = document_path.read_text(encoding="utf-8")
    for name in _expected_skills():
        assert f"## {skill_heading(name)}\n" in document

    for excluded in EXCLUDED_SKILLS:
        assert f"## {skill_heading(excluded)}\n" not in document

    # Every reference file has to travel with the skills: ChatGPT and Gemini cap
    # knowledge at about ten files, so there is no second file to put them in.
    for reference in sorted(SKILLS_DIR.glob("*/references/*.md")):
        skill_name = reference.parent.parent.name
        if skill_name in EXCLUDED_SKILLS:
            continue
        relative = reference.relative_to(reference.parent.parent).as_posix()
        assert f"## {reference_heading(skill_name, relative)}\n" in document


def test_the_instructions_block_fits_the_smallest_instructions_box(tmp_path: Path) -> None:
    _, instructions_path = build_portable_bundle(tmp_path)
    instructions = instructions_path.read_text(encoding="utf-8")

    assert len(instructions) <= INSTRUCTIONS_LIMIT

    # The block is the only thing the assistant sees before it opens the document,
    # so it has to carry the entry point, the hand-off map, and the memory rule.
    assert skill_heading(ROOT_SKILL) in instructions
    for name in _expected_skills() - {ROOT_SKILL}:
        assert f"`{name}`" in instructions
    assert "session log" in instructions
    assert "web" in instructions.lower()


def test_every_pointer_in_the_document_names_a_section_that_exists(tmp_path: Path) -> None:
    document_path, _ = build_portable_bundle(tmp_path)
    document = document_path.read_text(encoding="utf-8")

    headings = set(re.findall(r"^## (.+)$", document, flags=re.M))
    pointers = set(re.findall(r"`((?:Skill|Reference): [^`]+)`", document))
    assert pointers, "document has no cross-section pointers at all"
    assert pointers <= headings

    # There is no filesystem behind this file. A surviving path is a dead pointer.
    assert not re.findall(r"`\.\./[^`]+`", document)
    assert not re.findall(r"`references/[^`]+`", document)


def test_section_headings_are_the_only_level_two_headings(tmp_path: Path) -> None:
    document_path, _ = build_portable_bundle(tmp_path)
    document = document_path.read_text(encoding="utf-8")

    # A skill body heading landing on `##` would look like a section a hand-off
    # could point at, and the document would have two meanings for the same level.
    for heading in re.findall(r"^## (.+)$", document, flags=re.M):
        assert heading.startswith(("Skill: ", "Reference: ", "Instructions block")), heading


def test_rewrites_turn_paths_into_section_names() -> None:
    own = rewrite_references("see `references/search-strategy.md`", "find-university-chairs", set())
    assert own == "see `Reference: find-university-chairs/references/search-strategy.md`"

    sibling = rewrite_references(
        "see `../build-student-profile/references/x.md`", "thesis-finder", {"build-student-profile"}
    )
    assert sibling == "see `Reference: build-student-profile/references/x.md`"


def test_a_pointer_to_an_unbundled_skill_fails_the_build() -> None:
    with pytest.raises(PortableBundleError, match="not in the bundle"):
        rewrite_references("see `../design-agent-skill/references/x.md`", "thesis-finder", set())


def test_headings_too_deep_to_demote_fail_the_build() -> None:
    with pytest.raises(PortableBundleError, match="too deep"):
        demote_headings("##### far too deep\n", "some-skill/SKILL.md")


def test_sources_are_left_untouched(tmp_path: Path) -> None:
    before = {path: path.read_bytes() for path in sorted(SKILLS_DIR.rglob("*.md"))}
    build_portable_bundle(tmp_path)
    assert {path: path.read_bytes() for path in sorted(SKILLS_DIR.rglob("*.md"))} == before
