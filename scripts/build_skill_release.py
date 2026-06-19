"""Build the public release artifact for the thesis-advising skills."""

from __future__ import annotations

import argparse
import re
import shutil
import tarfile
import zipfile
from pathlib import Path
from tomllib import loads as load_toml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
DEFAULT_DIST_DIR = REPO_ROOT / "dist"
PACKAGE_BASENAME = "study-os-thesis-skills"
ALLOWED_RESOURCE_DIRS = {"references", "assets"}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
REFERENCE_PATTERN = re.compile(r"`(references/[^`]+)`")


class BuildError(RuntimeError):
    """Raised when the release package cannot be built safely."""


def read_project_version(pyproject_path: Path = REPO_ROOT / "pyproject.toml") -> str:
    data = load_toml(pyproject_path.read_text(encoding="utf-8"))
    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise BuildError(f"{pyproject_path} is missing [project].version")
    return version


def validate_tag(version: str, tag: str | None) -> None:
    if not tag:
        return

    expected = f"skills-v{version}"
    if tag != expected:
        raise BuildError(f"release tag {tag!r} does not match project version {version!r}; expected {expected!r}")


def skill_dirs() -> list[Path]:
    if not SKILLS_DIR.is_dir():
        raise BuildError("skills/ directory is missing")

    dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir() and path.name != "tests")
    if not dirs:
        raise BuildError("no skill directories found")
    return dirs


def validate_source_skill(skill_dir: Path) -> None:
    if not SKILL_NAME_PATTERN.fullmatch(skill_dir.name):
        raise BuildError(f"invalid skill directory name: {skill_dir.name}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise BuildError(f"{skill_dir.relative_to(REPO_ROOT)} is missing SKILL.md")

    skill_text = skill_md.read_text(encoding="utf-8")
    for relative_reference in REFERENCE_PATTERN.findall(skill_text):
        if not (skill_dir / relative_reference).exists():
            raise BuildError(f"{skill_dir.name} references missing path {relative_reference}")


def copy_skill(skill_dir: Path, package_dir: Path) -> None:
    validate_source_skill(skill_dir)

    target_dir = package_dir / skill_dir.name
    target_dir.mkdir(parents=True)
    shutil.copy2(skill_dir / "SKILL.md", target_dir / "SKILL.md")

    for resource_name in sorted(ALLOWED_RESOURCE_DIRS):
        source_resource = skill_dir / resource_name
        if source_resource.exists():
            if not source_resource.is_dir():
                raise BuildError(f"{source_resource.relative_to(REPO_ROOT)} must be a directory")
            shutil.copytree(source_resource, target_dir / resource_name)


def validate_package(package_dir: Path) -> None:
    forbidden_names = {
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
        "skills",
        "tests",
    }
    forbidden_parts = {".github", "__pycache__", "fixtures", "scripts", "tests"}

    for path in package_dir.rglob("*"):
        relative_parts = path.relative_to(package_dir).parts
        if any(part in forbidden_parts for part in relative_parts):
            raise BuildError(f"forbidden path in release package: {path.relative_to(package_dir)}")
        if path.name in forbidden_names:
            raise BuildError(f"forbidden file or directory in release package: {path.relative_to(package_dir)}")

    for skill_dir in sorted(path for path in package_dir.iterdir() if path.is_dir()):
        allowed = {"SKILL.md", "references", "assets"}
        unexpected = {path.name for path in skill_dir.iterdir()} - allowed
        if unexpected:
            raise BuildError(f"{skill_dir.name} contains unexpected release entries: {sorted(unexpected)}")
        if not (skill_dir / "SKILL.md").is_file():
            raise BuildError(f"{skill_dir.name} is missing SKILL.md in release package")


def create_archives(package_dir: Path, dist_dir: Path) -> tuple[Path, Path]:
    tar_path = dist_dir / f"{package_dir.name}.tar.gz"
    zip_path = dist_dir / f"{package_dir.name}.zip"

    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(package_dir, arcname=package_dir.name)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for path in sorted(package_dir.rglob("*")):
            zip_file.write(path, path.relative_to(package_dir.parent))

    return tar_path, zip_path


def build_release(dist_dir: Path, tag: str | None = None) -> tuple[Path, Path, Path]:
    version = read_project_version()
    validate_tag(version, tag)

    package_dir = dist_dir / f"{PACKAGE_BASENAME}-v{version}"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    for skill_dir in skill_dirs():
        copy_skill(skill_dir, package_dir)

    validate_package(package_dir)
    tar_path, zip_path = create_archives(package_dir, dist_dir)
    return package_dir, tar_path, zip_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public skill-only release artifact.")
    parser.add_argument("--dist-dir", type=Path, default=DEFAULT_DIST_DIR, help="Directory for the release package and archives.")
    parser.add_argument("--tag", help="Release tag to validate, for example skills-v0.1.0.")
    args = parser.parse_args()

    try:
        package_dir, tar_path, zip_path = build_release(args.dist_dir, args.tag)
    except BuildError as error:
        parser.exit(status=1, message=f"error: {error}\n")

    print(f"Built {package_dir}")
    print(f"Built {tar_path}")
    print(f"Built {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
