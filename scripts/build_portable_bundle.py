"""Build the single-file portable edition of the thesis-advising skills.

Claude loads Agent Skills. ChatGPT and Gemini do not — what they offer is a
container (a Project, a Custom GPT, a Gem) that holds an instructions box and a
small number of knowledge files. Both cap knowledge at around ten files, and
ChatGPT caps instructions at 8000 characters, so neither the ten-folder release
nor the multi-file Claude bundle fits.

This builder collapses every skill and reference into one Markdown document with
named sections, and generates a short bootstrap block that goes in the
instructions box and points at those sections. One file, no filesystem, no path
resolution, no file-count limit.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_app_bundle import EXCLUDED_SKILLS, ROOT_SKILL, override_session_location
from scripts.build_skill_release import (
    REPO_ROOT,
    BuildError,
    read_project_version,
    skill_dirs,
    validate_source_skill,
)


DEFAULT_DIST_DIR = REPO_ROOT / "dist"
PORTABLE_BASENAME = "thesis-finder-portable"

# ChatGPT's Custom GPT instructions box. Gemini's is not documented; this is the
# tighter of the two known limits, so a block that fits here fits both.
INSTRUCTIONS_LIMIT = 8000

FRONTMATTER_PATTERN = re.compile(r"^---\n(?P<body>.*?)\n---\n", flags=re.DOTALL)
OWN_REFERENCE_PATTERN = re.compile(r"`(references/[^`]+)`")
SIBLING_REFERENCE_PATTERN = re.compile(r"`\.\./([a-z0-9-]+)/([^`]+)`")


class PortableBundleError(BuildError):
    """Raised when the portable edition cannot be built safely."""


def skill_heading(name: str) -> str:
    return f"Skill: {name}"


def reference_heading(skill_name: str, relative: str) -> str:
    return f"Reference: {skill_name}/{relative}"


def split_frontmatter(text: str, source: str) -> tuple[str, str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise PortableBundleError(f"{source} is missing YAML frontmatter")

    description = ""
    for line in match.group("body").splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip() == "description":
            description = value.strip()
    if not description:
        raise PortableBundleError(f"{source} has no description in its frontmatter")
    return description, text[match.end():].lstrip()


def demote_headings(body: str, source: str) -> str:
    """Push a skill's own headings below the `##` level this document navigates by.

    Section names are what a hand-off points at, so `##` has to mean "a section"
    and nothing else. Sources top out at `####`, which lands on `######` here.
    """
    if re.search(r"^#{5,} ", body, flags=re.M):
        raise PortableBundleError(f"{source} has headings too deep to demote into the document")
    return re.sub(r"^(#{1,4}) ", r"##\1 ", body, flags=re.M)


def rewrite_references(body: str, skill_name: str, known: set[str]) -> str:
    """Turn file paths into the section names this document actually uses."""

    def own(match: re.Match[str]) -> str:
        return f"`{reference_heading(skill_name, match.group(1))}`"

    def sibling(match: re.Match[str]) -> str:
        target, remainder = match.group(1), match.group(2)
        if target not in known:
            raise PortableBundleError(
                f"{skill_name} references `../{target}/{remainder}`, which is not in the bundle"
            )
        return f"`{reference_heading(target, remainder)}`"

    return SIBLING_REFERENCE_PATTERN.sub(sibling, OWN_REFERENCE_PATTERN.sub(own, body))


def bootstrap_block(bundled_names: list[str], version: str) -> str:
    rows = "\n".join(f"| `{name}` | `{skill_heading(name)}` |" for name in bundled_names)
    return f"""You are a thesis-search advisor for students at the University of Tübingen.
Your full instructions are in the attached document "Thesis-Option Finder,
portable edition {version}". Follow it exactly. Do not summarise it, do not
improvise around it, and do not answer from general knowledge where it tells you
to verify something live.

START HERE: read the section titled "{skill_heading(ROOT_SKILL)}" in that document and
follow it from its Step 0. Everything else follows from there.

FOLLOWING A HAND-OFF. Those instructions name other skills, for example
`find-university-chairs`. They are sections of the same document, not separate
tools. When told to invoke, call, or delegate to a named skill, read the matching
section, follow it, then return and continue:

| Named skill | Section to read |
|---|---|
{rows}

Paths written in backticks like `Reference: find-university-chairs/references/search-strategy.md`
are section names in that same document. Read the section.

WEB SEARCH IS REQUIRED. Every option you present must be verified against a live
official page in this conversation. If you cannot search the web, say so plainly
and stop — do not produce a list from memory. Chairs, people, and openings change,
and an unverified suggestion wastes a student's application.

MEMORY BETWEEN CONVERSATIONS. This is a search that runs over weeks, and the
interview that produces the student's profile is the expensive part. Never make a
returning student repeat it.

At the START of every conversation, before asking anything, look for an existing
session log — among the files attached to this conversation, in the knowledge or
files of this project/GPT/Gem, and in anything you remember about this student. If
you find one, say which one you are using, confirm the profile back in one short
paragraph, and continue from where it stopped. Only interview a student who has no
session log anywhere.

Produce the session log as a downloadable file TWICE: once the moment the profile
interview is complete, before any searching, and again at the end of the run with
the results added. Both times, tell the student in plain words:

> Save this file into this project's files or knowledge. Next time you start a
> chat here it will be loaded automatically, and we continue instead of starting
> over.

The session log format is defined at the end of the "{skill_heading(ROOT_SKILL)}"
section. Keep it in the student's own words where the format says so.
"""


def build_portable_bundle(dist_dir: Path) -> tuple[Path, Path]:
    version = read_project_version()
    sources = {path.name: path for path in skill_dirs()}
    if ROOT_SKILL not in sources:
        raise PortableBundleError(f"skills/{ROOT_SKILL} is missing; it is the entry point")

    bundled_names = sorted(set(sources) - EXCLUDED_SKILLS - {ROOT_SKILL})
    known = set(bundled_names) | {ROOT_SKILL}

    bootstrap = bootstrap_block(bundled_names, version)
    if len(bootstrap) > INSTRUCTIONS_LIMIT:
        raise PortableBundleError(
            f"bootstrap block is {len(bootstrap)} characters; the instructions box holds {INSTRUCTIONS_LIMIT}"
        )

    parts = [
        f"# Thesis-Option Finder — portable edition {version}\n",
        HUMAN_PREFACE,
        "## Instructions block — copy this into your assistant\n",
        "Copy everything between the lines into the instructions or custom-instructions\n"
        "field of your Project, Custom GPT, or Gem. Then attach this whole file as its\n"
        "knowledge or project file.\n",
        "-----BEGIN INSTRUCTIONS-----\n",
        bootstrap,
        "-----END INSTRUCTIONS-----\n",
        "---\n",
    ]

    for name in [ROOT_SKILL, *bundled_names]:
        skill_dir = sources[name]
        validate_source_skill(skill_dir)
        description, body = split_frontmatter(
            (skill_dir / "SKILL.md").read_text(encoding="utf-8"), f"{name}/SKILL.md"
        )
        if name == ROOT_SKILL:
            body = override_session_location(body, f"{name}/SKILL.md", PORTABLE_SESSION_NOTE)
        parts.append(f"## {skill_heading(name)}\n")
        parts.append(f"*{description}*\n")
        parts.append(demote_headings(rewrite_references(body, name, known), f"{name}/SKILL.md") + "\n")

        references_dir = skill_dir / "references"
        if references_dir.is_dir():
            for reference in sorted(references_dir.rglob("*.md")):
                relative = reference.relative_to(skill_dir).as_posix()
                parts.append(f"## {reference_heading(name, relative)}\n")
                body = reference.read_text(encoding="utf-8")
                parts.append(demote_headings(body, f"{name}/{relative}") + "\n")

    document = "\n".join(parts)
    validate_document(document, bundled_names)

    dist_dir.mkdir(parents=True, exist_ok=True)
    document_path = dist_dir / f"{PORTABLE_BASENAME}-v{version}.md"
    document_path.write_text(document, encoding="utf-8")

    instructions_path = dist_dir / f"{PORTABLE_BASENAME}-instructions-v{version}.txt"
    instructions_path.write_text(bootstrap, encoding="utf-8")
    return document_path, instructions_path


def validate_document(document: str, bundled_names: list[str]) -> None:
    """Every pointer must name a section that exists — there is no filesystem to fall back on."""
    headings = set(re.findall(r"^## (.+)$", document, flags=re.M))

    for name in [ROOT_SKILL, *bundled_names]:
        if skill_heading(name) not in headings:
            raise PortableBundleError(f"section for {name} is missing from the document")

    for pointer in set(re.findall(r"`((?:Skill|Reference): [^`]+)`", document)):
        if pointer not in headings:
            raise PortableBundleError(f"document points at missing section {pointer!r}")

    for leftover in set(re.findall(r"`(\.\./[^`]+)`", document)):
        raise PortableBundleError(f"document kept a filesystem path {leftover!r}")


PORTABLE_SESSION_NOTE = """> **In this edition, ignore the paths below.** You are running in an assistant with
> no filesystem. Read the session log from the files attached to this conversation and
> from the knowledge of this project, GPT, or Gem, and hand it back as a downloadable
> file for the student to store there. The **format** described below still applies
> exactly."""


HUMAN_PREFACE = """This one file contains everything the thesis-search advisor needs. It is meant for
assistants that do not load Agent Skills — ChatGPT and Gemini — and it also works
as a project file for Claude.

**Set it up once:**

1. Create a container that keeps files: a **Project** in ChatGPT or Claude, a
   **Gem** in Gemini, or a **Custom GPT**. A plain chat works too, but then nothing
   is remembered between conversations.
2. Attach this file to it as a knowledge or project file.
3. Copy the instructions block below into its instructions field.
4. Make sure web search is available. Without it the advisor cannot verify anything
   and is told to stop rather than guess.

**Then, in a chat inside that container, type:** `thesis-finder`

**Coming back weeks later:** the advisor gives you a session file. Put it into the
same container's files. Your next chat there picks up your profile and search
history automatically — you never redo the interview.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the single-file portable edition.")
    parser.add_argument("--dist-dir", type=Path, default=DEFAULT_DIST_DIR, help="Directory for the generated files.")
    args = parser.parse_args()

    try:
        document_path, instructions_path = build_portable_bundle(args.dist_dir)
    except BuildError as error:
        parser.exit(status=1, message=f"error: {error}\n")

    print(f"Built {document_path}")
    print(f"Built {instructions_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
