"""Build the single-folder Claude-app bundle for the thesis-advising skills.

The public release ships ten sibling skill folders, which is what a filesystem
client (Claude Code, Codex) installs. Clients that take one uploaded skill at a
time cannot use that layout: every skill arrives isolated, so name-based
hand-offs have nothing to resolve against and `../<other-skill>/...` paths point
outside the package.

This builder folds the same sources into one uploadable skill: `thesis-finder`
stays the entry point, the skills it hands off to become bundled instruction
files underneath it, and every cross-skill path is rewritten to be relative to
the bundle root. The ten-skill sources stay the single point of truth — nothing
here is edited by hand.
"""

from __future__ import annotations

import argparse
import re
import shutil
import zipfile
from pathlib import Path

from scripts.build_skill_release import (
    ALLOWED_RESOURCE_DIRS,
    REPO_ROOT,
    BuildError,
    read_project_version,
    skill_dirs,
    validate_source_skill,
)


DEFAULT_DIST_DIR = REPO_ROOT / "dist"
ROOT_SKILL = "thesis-finder"
BUNDLED_DIR = "skills"
BUNDLED_INSTRUCTIONS = "INSTRUCTIONS.md"

# design-agent-skill authors skills; it is not reachable from the student flow and
# would only add weight to a bundle a student uploads.
EXCLUDED_SKILLS = {"design-agent-skill"}

FRONTMATTER_PATTERN = re.compile(r"^---\n.*?\n---\n", flags=re.DOTALL)
OWN_REFERENCE_PATTERN = re.compile(r"`(references/[^`]+)`")
SIBLING_REFERENCE_PATTERN = re.compile(r"`\.\./([a-z0-9-]+)/([^`]+)`")


class AppBundleError(BuildError):
    """Raised when the app bundle cannot be built safely."""


def routing_preamble(bundled_names: list[str]) -> str:
    """The one block of text that is added rather than copied.

    Everything else in the bundle is a source file with paths rewritten. This
    block is what replaces the client's own skill routing: it tells the agent
    where the skills named in the instructions actually live.
    """
    rows = "\n".join(
        f"| `{name}` | `{BUNDLED_DIR}/{name}/{BUNDLED_INSTRUCTIONS}` |" for name in bundled_names
    )
    return f"""## Bundled skills — how to follow a hand-off

This is a self-contained bundle. The instructions below name other skills
(`find-university-chairs`, `build-student-profile`, and so on). They are not
separately installed. Each one is a file inside this bundle.

Whenever these instructions say to **invoke**, **call**, or **delegate to** a
named skill, read the matching file and follow it as if it were that skill,
then return here and continue.

| Named skill | Read this file |
|---|---|
{rows}

Every path written in this bundle, in this file and in the bundled instruction
files, is relative to the bundle root — the folder holding this file.

**Session file in a client without a durable filesystem.** This bundle is often
run where written files disappear when the conversation ends. If you cannot
write to a path that will still exist next time, keep the session log in the
conversation as normal, and at the end of the run give the student the session
file as a downloadable file, telling them to attach it at the start of their
next session so the search can resume without repeating the interview.

---

"""


def rewrite_bundled_skill(text: str, skill_name: str) -> str:
    """Repoint a bundled skill's own `references/...` paths at the bundle root."""
    return OWN_REFERENCE_PATTERN.sub(
        lambda match: f"`{BUNDLED_DIR}/{skill_name}/{match.group(1)}`", text
    )


def rewrite_root_skill(text: str, bundled_names: list[str]) -> str:
    """Repoint the entry skill's `../<other-skill>/...` paths at the bundle root."""

    def replace(match: re.Match[str]) -> str:
        target, remainder = match.group(1), match.group(2)
        if target not in bundled_names:
            raise AppBundleError(
                f"{ROOT_SKILL} references `../{target}/{remainder}`, which is not in the bundle"
            )
        return f"`{BUNDLED_DIR}/{target}/{remainder}`"

    return SIBLING_REFERENCE_PATTERN.sub(replace, text)


def insert_preamble(text: str, preamble: str) -> str:
    """Put the routing block directly after the frontmatter, before any prose."""
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise AppBundleError(f"{ROOT_SKILL}/SKILL.md is missing YAML frontmatter")
    return f"{match.group(0)}\n{preamble}{text[match.end():].lstrip()}"


def copy_resources(source_dir: Path, target_dir: Path) -> None:
    for resource_name in sorted(ALLOWED_RESOURCE_DIRS):
        source_resource = source_dir / resource_name
        if source_resource.exists():
            shutil.copytree(source_resource, target_dir / resource_name)


def build_app_bundle(dist_dir: Path) -> tuple[Path, Path]:
    version = read_project_version()

    sources = {path.name: path for path in skill_dirs()}
    if ROOT_SKILL not in sources:
        raise AppBundleError(f"skills/{ROOT_SKILL} is missing; it is the bundle entry point")

    bundled_names = sorted(set(sources) - EXCLUDED_SKILLS - {ROOT_SKILL})
    if not bundled_names:
        raise AppBundleError("no skills left to bundle under the entry point")

    package_dir = dist_dir / f"{ROOT_SKILL}-app-v{version}" / ROOT_SKILL
    if package_dir.parent.exists():
        shutil.rmtree(package_dir.parent)
    package_dir.mkdir(parents=True)

    for name in bundled_names:
        source_dir = sources[name]
        validate_source_skill(source_dir)
        target_dir = package_dir / BUNDLED_DIR / name
        target_dir.mkdir(parents=True)
        skill_text = (source_dir / "SKILL.md").read_text(encoding="utf-8")
        (target_dir / BUNDLED_INSTRUCTIONS).write_text(
            rewrite_bundled_skill(skill_text, name), encoding="utf-8"
        )
        copy_resources(source_dir, target_dir)

    root_source = sources[ROOT_SKILL]
    validate_source_skill(root_source)
    root_text = (root_source / "SKILL.md").read_text(encoding="utf-8")
    root_text = rewrite_root_skill(root_text, bundled_names)
    root_text = insert_preamble(root_text, routing_preamble(bundled_names))
    (package_dir / "SKILL.md").write_text(root_text, encoding="utf-8")
    copy_resources(root_source, package_dir)

    validate_bundle(package_dir)

    zip_path = dist_dir / f"{ROOT_SKILL}-app-v{version}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for path in sorted(package_dir.rglob("*")):
            zip_file.write(path, path.relative_to(package_dir.parent))

    return package_dir, zip_path


def validate_bundle(package_dir: Path) -> None:
    """An upload is one shot; a path that does not resolve fails silently at run time."""
    if not (package_dir / "SKILL.md").is_file():
        raise AppBundleError("bundle is missing SKILL.md at its root")

    for markdown in sorted(package_dir.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        if "`../" in text:
            raise AppBundleError(
                f"{markdown.relative_to(package_dir)} still contains a path outside the bundle"
            )
        for reference in re.findall(rf"`({BUNDLED_DIR}/[^`]+)`", text):
            if not (package_dir / reference).exists():
                raise AppBundleError(
                    f"{markdown.relative_to(package_dir)} points at missing path {reference}"
                )

    for instructions in sorted((package_dir / BUNDLED_DIR).rglob(BUNDLED_INSTRUCTIONS)):
        for reference in OWN_REFERENCE_PATTERN.findall(instructions.read_text(encoding="utf-8")):
            raise AppBundleError(
                f"{instructions.relative_to(package_dir)} kept an un-rewritten path {reference}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the single-folder Claude-app skill bundle.")
    parser.add_argument("--dist-dir", type=Path, default=DEFAULT_DIST_DIR, help="Directory for the bundle and archive.")
    args = parser.parse_args()

    try:
        package_dir, zip_path = build_app_bundle(args.dist_dir)
    except BuildError as error:
        parser.exit(status=1, message=f"error: {error}\n")

    print(f"Built {package_dir}")
    print(f"Built {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
