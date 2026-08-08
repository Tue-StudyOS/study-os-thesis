"""Deterministic checks for the portable thesis-finder skill package."""

from __future__ import annotations

import re
from pathlib import Path


SKILLS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILLS_DIR.parent
EXPECTED_SKILLS = {
    "build-student-profile",
    "design-agent-skill",
    "discover-company-candidates",
    "discover-university-candidates",
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
# A rules-only reference file cites a handful of anchor sources; a static catalog cites
# dozens. Every shipped reference file currently contains zero absolute URLs, so this
# threshold is pure headroom — see test_shipped_resources_are_not_static_uri_catalogs.
MAX_ABSOLUTE_URLS_PER_RESOURCE_FILE = 5
ABSOLUTE_URL_PATTERN = re.compile(r"https?://")
# `site:uni-tuebingen.de/...` query templates and source-priority prose name domains on
# purpose and are the correct shape under rules-only discovery. They carry no scheme, but
# skip their lines explicitly so the intent survives a future rewrite that adds one.
SITE_QUERY_PATTERN = re.compile(r"\bsite:")


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
    # The disclaimer states what is true now ("no runtime database, index, or bundled
    # …data"); until 2026-08-08 it instead named the UI/Celery/FastAPI stack that the
    # project had already deleted, which is project history an installing agent cannot
    # act on. Phrase the invariant, not its history.
    no_db_disclaimers = (
        "has no runtime database, index, or bundled",
        "the only authoritative source during discovery.",
        "static company or URI backbone",
        "static faculty or URI backbone",
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

    # The reference files that ARE the intelligence must be present. The two named
    # backbones deleted by the 2026-07-31 pivot are kept as explicit special cases of the
    # general rule in test_shipped_resources_are_not_static_uri_catalogs.
    assert (chair_references / "search-strategy.md").is_file()
    assert not (chair_references / "tuebingen-faculty-backbone.md").exists()
    company_references = SKILLS_DIR / "find-company-thesis-options" / "references"
    assert (company_references / "company-search-strategy.md").is_file()
    assert not (company_references / "bw-company-backbone.md").exists()

    assert (SKILLS_DIR / "discover-company-candidates" / "references" / "company-discovery-rules.md").is_file()
    assert (SKILLS_DIR / "discover-university-candidates" / "references" / "university-discovery-rules.md").is_file()


def _shipped_resource_files() -> list[Path]:
    """Every file the release bundles under a skill's references/ or assets/ directory."""
    files: list[Path] = []
    for skill_dir in _skill_dirs():
        for resource_name in ("references", "assets"):
            resource_dir = skill_dir / resource_name
            if resource_dir.is_dir():
                files.extend(sorted(path for path in resource_dir.rglob("*") if path.is_file()))
    return files


def _count_catalog_urls(text: str) -> int:
    return sum(
        len(ABSOLUTE_URL_PATTERN.findall(line))
        for line in text.splitlines()
        if not SITE_QUERY_PATTERN.search(line)
    )


def test_shipped_resources_are_not_static_uri_catalogs() -> None:
    # The no-static-catalog invariant, generalised. The named-file assertions above only
    # catch a resurrection of the two backbones deleted on 2026-07-31; they did not catch
    # find-recent-papers/references/papers/ (287 absolute URLs across 59 files, deleted
    # 2026-08-08), which was a static URI catalog by any reading. This check is about
    # shape, not filename: under rules-only discovery the intelligence is search rules,
    # so no shipped resource should read like an entity list with a URL per row.
    offenders = []
    for path in _shipped_resource_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # binary asset; nothing to count
        count = _count_catalog_urls(text)
        if count > MAX_ABSOLUTE_URLS_PER_RESOURCE_FILE:
            offenders.append(f"{path.relative_to(SKILLS_DIR)} has {count} absolute URLs")

    assert not offenders, (
        "shipped resources look like static URI catalogs "
        f"(limit {MAX_ABSOLUTE_URLS_PER_RESOURCE_FILE} absolute URLs per file): " + "; ".join(offenders)
    )


def test_company_discovery_requires_confirmed_bw_scope_for_final_options() -> None:
    discovery_skill = (SKILLS_DIR / "discover-company-candidates" / "SKILL.md").read_text(encoding="utf-8")
    discovery_rules = (
        SKILLS_DIR / "discover-company-candidates" / "references" / "company-discovery-rules.md"
    ).read_text(encoding="utf-8")
    parent_skill = (SKILLS_DIR / "find-company-thesis-options" / "SKILL.md").read_text(encoding="utf-8")

    assert "Final Baden-Württemberg company candidates must use `bw_scope: confirmed`." in discovery_skill
    assert "Baden-Württemberg presence is confirmed from an official or authoritative" in discovery_rules
    assert "Do not include `bw_scope: uncertain` companies in the final candidate table" in discovery_rules
    assert "Exclude `bw_scope: uncertain` and `bw_scope: rejected` from the final BW" in parent_skill
    assert "Enrich each confirmed-BW candidate" in parent_skill


def test_university_discovery_requires_confirmed_affiliation_for_final_options() -> None:
    discovery_skill = (SKILLS_DIR / "discover-university-candidates" / "SKILL.md").read_text(encoding="utf-8")
    discovery_rules = (
        SKILLS_DIR / "discover-university-candidates" / "references" / "university-discovery-rules.md"
    ).read_text(encoding="utf-8")
    parent_skill = (SKILLS_DIR / "find-university-chairs" / "SKILL.md").read_text(encoding="utf-8")
    parent_strategy = (SKILLS_DIR / "find-university-chairs" / "references" / "search-strategy.md").read_text(
        encoding="utf-8"
    )

    assert "affiliation_status: confirmed | uncertain | rejected" in discovery_skill
    assert "Final university candidates must use `affiliation_status: confirmed`." in discovery_skill
    assert "Tübingen affiliation is confirmed from an official or authoritative" in discovery_rules
    assert "Do not include `affiliation_status: uncertain` entries in the final candidate" in discovery_rules
    assert "table for Tübingen thesis options" in discovery_rules
    assert "Exclude `affiliation_status: uncertain` and `affiliation_status: rejected`" in parent_skill
    assert "Enrich each confirmed-affiliation candidate" in parent_skill
    assert "Final options must have `affiliation_status: confirmed`." in parent_strategy


def test_no_gos_are_local_filters_not_raw_search_terms() -> None:
    discovery_files = [
        SKILLS_DIR / "discover-company-candidates" / "SKILL.md",
        SKILLS_DIR / "discover-university-candidates" / "SKILL.md",
        SKILLS_DIR / "find-company-thesis-options" / "references" / "company-search-strategy.md",
        SKILLS_DIR / "find-university-chairs" / "references" / "search-strategy.md",
    ]

    for path in discovery_files:
        text = path.read_text(encoding="utf-8")
        normalized_text = " ".join(text.split())
        assert "{NOGO_TERM}" not in text
        assert "Do not send sensitive or personal no-go wording to search providers" in normalized_text or (
            "Keep sensitive or personal no-go" in text and "wording out of web queries" in text
        )


def test_simulation_artifact_paths_use_selected_root_and_zip_is_ignored() -> None:
    for path in (
        REPO_ROOT / ".codex" / "skills" / "run-thesis-simulations" / "SKILL.md",
        REPO_ROOT / ".claude" / "skills" / "run-thesis-simulations" / "SKILL.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "selected artifact root's" in text
        assert ".simulations/baseline/{timestamp}/rating" in text
        assert "Keep generated fictional data only in `.simulations/convo`" not in text

    assert ".simulations.zip" in (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")


def test_optional_llm_eval_fixtures_do_not_use_placeholder_urls() -> None:
    eval_text = (SKILLS_DIR / "tests" / "evals" / "test_skill_quality.py").read_text(encoding="utf-8")

    assert "https://uni-tuebingen.de/..." not in eval_text


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
    assert "live web" in chair_skill
    assert "If any dimension is missing or shallow, stop here." in chair_skill
    assert "If any dimension is missing or shallow, stop here." in company_skill
    assert "discover-university-candidates" in chair_skill
    assert "discover-company-candidates" in company_skill

    # The optional final steps stay available.
    assert "research-proposal sketches" in directions_skill
    assert "conversation starter" in directions_skill
    assert "proposal sketch" in contact_skill
    assert "first-contact" in contact_skill
