"""Deterministic checks for the portable thesis-finder skill package."""

from __future__ import annotations

import re
from pathlib import Path


SKILLS_DIR = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "build-student-profile",
    "design-agent-skill",
    "draft-thesis-contact",
    "find-company-thesis-options",
    "find-recent-papers",
    "find-university-chairs",
    "generate-thesis-directions",
    "thesis-finder",
}
FORBIDDEN_PRIVATE_DATA_PATH_TERMS = {
    "gpa",
    "grade",
    "grades",
    "student-profile",
    "transcript",
}


def _parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(?P<body>.*?)\n---\n", text, flags=re.DOTALL)
    assert match, f"{skill_md} is missing YAML frontmatter"

    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        key, separator, value = line.partition(":")
        assert separator, f"{skill_md} has invalid frontmatter line: {line!r}"
        fields[key.strip()] = value.strip()
    return fields


def _skill_dirs() -> list[Path]:
    assert SKILLS_DIR.is_dir(), "skills/ package is missing"
    return sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir() and path.name != "tests")


def test_expected_portable_skills_exist() -> None:
    assert {path.name for path in _skill_dirs()} == EXPECTED_SKILLS


def test_skill_frontmatter_is_portable_and_trigger_rich() -> None:
    for skill_dir in _skill_dirs():
        fields = _parse_frontmatter(skill_dir / "SKILL.md")

        assert fields["name"] == skill_dir.name
        assert re.fullmatch(r"[a-z0-9-]+", fields["name"])
        assert fields.get("description")
        assert len(fields["description"]) <= 1024
        assert "Use when" in fields["description"]
        assert set(fields) == {"name", "description"}


def test_referenced_skill_resources_exist() -> None:
    reference_pattern = re.compile(r"`(references/[^`]+)`")

    for skill_dir in _skill_dirs():
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for relative_reference in reference_pattern.findall(skill_text):
            assert (skill_dir / relative_reference).exists(), f"{skill_dir.name} references missing path {relative_reference}"


def test_skill_package_does_not_bundle_private_student_data() -> None:
    bundled_files = [path for path in SKILLS_DIR.rglob("*") if path.is_file() and "tests" not in path.relative_to(SKILLS_DIR).parts]

    for path in bundled_files:
        relative_parts = {part.lower() for part in path.relative_to(SKILLS_DIR).parts}
        assert relative_parts.isdisjoint(FORBIDDEN_PRIVATE_DATA_PATH_TERMS), f"private student data appears to be bundled at {path}"

    shared_resource_roots = [path for path in SKILLS_DIR.rglob("*") if path.is_dir() and path.name in {"references", "assets"}]
    for root in shared_resource_roots:
        descendant_names = {part.lower() for path in root.rglob("*") for part in path.relative_to(root).parts}
        assert descendant_names.isdisjoint(FORBIDDEN_PRIVATE_DATA_PATH_TERMS), f"private student data appears under shared resource root {root}"


def test_skill_privacy_and_evidence_rules_are_explicit() -> None:
    design_skill = (SKILLS_DIR / "design-agent-skill" / "SKILL.md").read_text(encoding="utf-8")
    profile_skill = (SKILLS_DIR / "build-student-profile" / "SKILL.md").read_text(encoding="utf-8")
    paper_skill = (SKILLS_DIR / "find-recent-papers" / "SKILL.md").read_text(encoding="utf-8")
    chair_skill = (SKILLS_DIR / "find-university-chairs" / "SKILL.md").read_text(encoding="utf-8")

    assert "Keep student-private data out of shared resources." in design_skill
    assert "Do not store transcripts, grades, GPA, or private profile data" in profile_skill
    assert "Accept raw student input in any form" in profile_skill
    assert "Interview the student **one question per turn**" in profile_skill
    assert "programming languages, ML frameworks, robotics/simulation tools" in profile_skill
    assert "One question is not enough for a complete profile." in profile_skill
    assert "Explicitly infer and summarize research skills" in profile_skill
    assert "Transcript of Records" in profile_skill
    assert "optional evidence sources" in profile_skill
    assert "Do not fabricate citation counts" in paper_skill
    assert "Do not invent thesis openings, team sizes, citation counts, or willingness to supervise." in chair_skill
    assert "Do not produce a chair shortlist on a partial profile." in chair_skill


def test_student_facing_skills_reject_old_runtime_dependencies() -> None:
    # design-agent-skill is a meta-skill; thesis-finder is a thin router that does no
    # data retrieval of its own. Every other student-facing skill must explicitly
    # disclaim any runtime database/backend dependency — the no-DB product invariant.
    # The legacy carry-over skills carry the canonical disclaimer; the rewritten
    # discovery skills phrase the same stance in their own words.
    no_db_disclaimers = (
        "Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.",
        "the only authoritative source during discovery.",
        "No runtime company database",
    )
    student_facing_skills = EXPECTED_SKILLS - {"design-agent-skill", "thesis-finder"}

    for skill_name in student_facing_skills:
        skill_text = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert any(phrase in skill_text for phrase in no_db_disclaimers), f"{skill_name} does not disclaim old runtime dependencies"


def test_discovery_skills_carry_no_runtime_seed_data() -> None:
    # The no-DB pivot moved all curated chair/professor/researcher seed data out of the
    # runtime skills and into eval-only ground truth. Guard against it creeping back in.
    chair_references = SKILLS_DIR / "find-university-chairs" / "references"
    for forbidden in ("professors", "chairs", "researchers"):
        assert not (chair_references / forbidden).exists(), f"runtime seed data {forbidden}/ must not live under {chair_references}"

    # The reference files that ARE the intelligence must be present.
    assert (chair_references / "search-strategy.md").is_file()
    assert (chair_references / "tuebingen-faculty-backbone.md").is_file()
    company_references = SKILLS_DIR / "find-company-thesis-options" / "references"
    assert (company_references / "company-search-strategy.md").is_file()
    assert (company_references / "bw-company-backbone.md").is_file()


def test_static_acceptance_fixture_covers_full_student_flow() -> None:
    profile_skill = (SKILLS_DIR / "build-student-profile" / "SKILL.md").read_text(encoding="utf-8")
    chair_skill = (SKILLS_DIR / "find-university-chairs" / "SKILL.md").read_text(encoding="utf-8")
    company_skill = (SKILLS_DIR / "find-company-thesis-options" / "SKILL.md").read_text(encoding="utf-8")
    finder_skill = (SKILLS_DIR / "thesis-finder" / "SKILL.md").read_text(encoding="utf-8")
    directions_skill = (SKILLS_DIR / "generate-thesis-directions" / "SKILL.md").read_text(encoding="utf-8")
    contact_skill = (SKILLS_DIR / "draft-thesis-contact" / "SKILL.md").read_text(encoding="utf-8")

    # build-student-profile feeds the downstream flow.
    assert "matching keywords" in profile_skill
    assert "research core" in profile_skill
    assert "professional or research experience" in profile_skill
    assert "Research Skills" in (SKILLS_DIR / "build-student-profile" / "references" / "student-profile-schema.md").read_text(encoding="utf-8")

    # The entry-point orchestrator routes to both discovery skills.
    assert "find-university-chairs" in finder_skill
    assert "find-company-thesis-options" in finder_skill

    # Both discovery skills gate on a deep profile and search the live web.
    assert "using live web search" in chair_skill
    assert "If any dimension is missing or shallow, stop here." in chair_skill
    assert "If any dimension is missing or shallow, stop here." in company_skill

    # The optional final steps stay available.
    assert "research-proposal sketches" in directions_skill
    assert "conversation starter" in directions_skill
    assert "proposal sketch" in contact_skill
    assert "first-contact" in contact_skill
