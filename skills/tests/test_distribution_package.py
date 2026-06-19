"""Checks for the public skill-only release artifact."""

from __future__ import annotations

import re
import tarfile
import zipfile
from pathlib import Path

from scripts.build_skill_release import build_release, read_project_version


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
REFERENCE_PATTERN = re.compile(r"`(references/[^`]+)`")


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


def test_release_artifact_contains_only_installable_skill_folders(tmp_path: Path) -> None:
    package_dir, tar_path, zip_path = build_release(tmp_path)

    expected_skills = {path.name for path in SKILLS_DIR.iterdir() if path.is_dir() and path.name != "tests"}
    packaged_skills = {path.name for path in package_dir.iterdir() if path.is_dir()}
    assert packaged_skills == expected_skills
    assert not (package_dir / "skills").exists()
    assert not (package_dir / "tests").exists()

    forbidden_entries = {
        ".github",
        "AGENTS.md",
        "CLAUDE.md",
        "Makefile",
        "MASTERPLAN.md",
        "README.md",
        "STATUS.md",
        "docs",
        "pyproject.toml",
        "pytest.ini",
        "scripts",
    }
    for path in package_dir.rglob("*"):
        relative_parts = set(path.relative_to(package_dir).parts)
        assert relative_parts.isdisjoint(forbidden_entries), f"forbidden release path: {path.relative_to(package_dir)}"
        assert "tests" not in relative_parts
        assert "fixtures" not in relative_parts

    for skill_dir in sorted(path for path in package_dir.iterdir() if path.is_dir()):
        assert {path.name for path in skill_dir.iterdir()} <= {"SKILL.md", "references", "assets"}
        fields = _parse_frontmatter(skill_dir / "SKILL.md")
        assert fields["name"] == skill_dir.name
        assert set(fields) == {"name", "description"}

        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for relative_reference in REFERENCE_PATTERN.findall(skill_text):
            assert (skill_dir / relative_reference).exists(), f"{skill_dir.name} references missing path {relative_reference}"

    expected_name = f"study-os-thesis-skills-v{read_project_version()}"
    assert package_dir.name == expected_name
    assert tar_path.name == f"{expected_name}.tar.gz"
    assert zip_path.name == f"{expected_name}.zip"

    with tarfile.open(tar_path) as tar:
        tar_names = tar.getnames()
    assert all(name.startswith(f"{expected_name}/") or name == expected_name for name in tar_names)
    assert not any("/skills/tests/" in name or name.endswith("/pytest.ini") for name in tar_names)

    with zipfile.ZipFile(zip_path) as zip_file:
        zip_names = zip_file.namelist()
    assert all(name.startswith(f"{expected_name}/") for name in zip_names)
    assert not any("/skills/tests/" in name or name.endswith("/pytest.ini") for name in zip_names)
