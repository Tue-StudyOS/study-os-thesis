"""Deterministic checks for the portable thesis-finder skill package."""

from __future__ import annotations

import re
from pathlib import Path


SKILLS_DIR = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "build-student-profile",
    "design-agent-skill",
    "draft-thesis-contact",
    "find-linkedin-company-theses",
    "find-recent-papers",
    "find-university-chairs",
    "generate-thesis-directions",
    "match-thesis-advisors",
    "update-openalex-paper-index",
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
    assert "Interview the student one aspect at a time." in profile_skill
    assert "never more than two questions in a single turn" in profile_skill
    assert "programming languages, ML frameworks, robotics/simulation tools" in profile_skill
    assert "Keep the conversation natural" in profile_skill
    assert "Explicitly infer and summarize research skills" in profile_skill
    assert "Transcript of Records" in profile_skill
    assert "optional evidence sources" in profile_skill
    assert "Do not fabricate citation counts" in paper_skill
    assert "Do not invent openings, quotas, team sizes, citation counts, or willingness to supervise." in chair_skill
    assert "do not answer with a chair shortlist" in chair_skill


def test_student_facing_skills_reject_old_runtime_dependencies() -> None:
    student_facing_skills = EXPECTED_SKILLS - {"design-agent-skill", "update-openalex-paper-index"}

    for skill_name in student_facing_skills:
        skill_text = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app." in skill_text


def test_linkedin_company_theses_skill_requires_profile_grounded_ranking() -> None:
    skill_text = (SKILLS_DIR / "find-linkedin-company-theses" / "SKILL.md").read_text(encoding="utf-8")

    assert "Use the full in-session student profile for processing and ranking, not only keyword matches." in skill_text
    assert "thesis level or target degree, concrete courses or project evidence, practical skills/tools" in skill_text
    assert "use `build-student-profile` first" in skill_text
    assert "Do not ask for a search-parameter checklist yet." in skill_text
    assert "Do not search, rank, or produce company thesis leads until the profile is strong enough" in skill_text
    assert "Once the profile is strong enough, summarize the profile signals" in skill_text
    assert "use `find-university-chairs` and `match-thesis-advisors` for the university/chair lane" in skill_text
    assert "Only skip one lane if the user explicitly asks for company-only or university-only results." in skill_text
    assert "base location and radius in km" in skill_text
    assert "sectors or company types to exclude" in skill_text
    assert "normal web search tool" in skill_text
    assert "Do not use a Markdown database" in skill_text
    assert "references/ranking-rubric.md" in skill_text
    assert "profile-first gate" in skill_text
    assert "parallel university/company comparison" in skill_text
    assert "Exclude ordinary jobs, internships, and working-student roles" in skill_text
    assert "eligible ranked shortlist and an excluded or not-recommended list" in skill_text
    assert "Do not let a strong technology match override hard mismatches" in skill_text
    assert "company-career mirror" in skill_text
    assert "Scorecard covering thesis level, profile fit, feasibility gap" in skill_text
    assert "Evidence tier, evidence source, and access date" in skill_text
    assert "not a thesis, generic job/internship, location or work-mode mismatch" in skill_text
    assert "Act like a thesis-oriented study advisor first and a search assistant second." in skill_text
    assert "Treat company thesis search as a parallel complement to university/chair matching" in skill_text
    assert "Do not turn a shallow request into a generic Google/LinkedIn search." in skill_text
    assert "Do not run a live search before the student profile and search intake are complete" in skill_text
    assert "Do not skip the university/chair lane when the user asks broadly for thesis options" in skill_text
    assert "The main agent must merge evidence and rank centrally using the full student profile." in skill_text


def test_linkedin_company_theses_rubric_covers_release_ready_ranking() -> None:
    rubric_text = (SKILLS_DIR / "find-linkedin-company-theses" / "references" / "ranking-rubric.md").read_text(
        encoding="utf-8"
    )

    assert "Profile-First Gate" in rubric_text
    assert "Do not use this skill as a generic LinkedIn or Google search shortcut." in rubric_text
    assert "Ask one focused advising question by default." in rubric_text
    assert "Parallel University/Company Search" in rubric_text
    assert "University/chair lane: use `find-university-chairs` and `match-thesis-advisors`" in rubric_text
    assert "Company lane: use public LinkedIn-indexed and company-career evidence" in rubric_text
    assert "Cross-lane comparison and next actions." in rubric_text
    assert "Hard Exclusion Criteria" in rubric_text
    assert "ordinary job, internship, trainee role, or working-student role" in rubric_text
    assert "Do not let a strong technology match override a hard exclusion." in rubric_text
    assert "Scorecard" in rubric_text
    assert "Thesis contribution" in rubric_text
    assert "Company-thesis readiness" in rubric_text
    assert "Evidence Tiers" in rubric_text
    assert "`A`: Opened public LinkedIn page or company career page confirms the thesis details." in rubric_text
    assert "Company-Career Mirror Search" in rubric_text
    assert "compensation/workload, academic supervision, university-company process" in rubric_text


def test_required_markdown_database_indexes_exist() -> None:
    required_indexes = [
        SKILLS_DIR / "find-university-chairs" / "references" / "professors" / "INDEX.md",
    ]

    for index in required_indexes:
        assert index.is_file(), f"missing generated-data index template: {index}"


def _professor_seed_rows() -> list[list[str]]:
    index = SKILLS_DIR / "find-university-chairs" / "references" / "professors" / "INDEX.md"
    rows = []
    for line in index.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line or "name" in line:
            continue
        cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
        rows.append([cell.strip().replace("\\|", "|") for cell in cells])
    return rows


def test_professor_seed_index_contains_only_name_and_uri_columns() -> None:
    index = SKILLS_DIR / "find-university-chairs" / "references" / "professors" / "INDEX.md"
    text = index.read_text(encoding="utf-8")

    assert "| name | uri |" in text
    assert "|---|---|" in text
    assert "Mail" not in text
    assert "Notizen" not in text
    assert "Antwort erhalten" not in text
    assert "Angeschrieben" not in text
    assert "Mail-Variante" not in text
    assert "Bea" not in text
    assert "OpenAlex" not in text
    assert not re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text)

    rows = _professor_seed_rows()
    assert rows
    for row in rows:
        assert len(row) == 2
        name, uri = row
        assert name
        assert uri.startswith(("http://", "https://"))


def test_static_acceptance_fixture_covers_full_student_flow() -> None:
    profile_skill = (SKILLS_DIR / "build-student-profile" / "SKILL.md").read_text(encoding="utf-8")
    professor_index = (SKILLS_DIR / "find-university-chairs" / "references" / "professors" / "INDEX.md").read_text(encoding="utf-8")
    chair_skill = (SKILLS_DIR / "find-university-chairs" / "SKILL.md").read_text(encoding="utf-8")
    advisor_skill = (SKILLS_DIR / "match-thesis-advisors" / "SKILL.md").read_text(encoding="utf-8")
    directions_skill = (SKILLS_DIR / "generate-thesis-directions" / "SKILL.md").read_text(encoding="utf-8")
    contact_skill = (SKILLS_DIR / "draft-thesis-contact" / "SKILL.md").read_text(encoding="utf-8")

    assert "matching keywords" in profile_skill
    assert "research core" in profile_skill
    assert "professional or research experience" in profile_skill
    assert "Research Skills" in (SKILLS_DIR / "build-student-profile" / "references" / "student-profile-schema.md").read_text(encoding="utf-8")
    assert "Philipp Berens" in professor_index
    assert "native websearch/browser tools" in chair_skill
    assert "Shallow Profile Guardrail" in chair_skill
    assert "proposal hooks" in advisor_skill.lower()
    assert "research-proposal sketches" in directions_skill
    assert "conversation starter" in directions_skill
    assert "proposal sketch" in contact_skill
    assert "first-contact" in contact_skill
