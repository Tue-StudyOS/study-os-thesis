# Skill Distribution And Maintenance

This is the minimal maintainer guide for the skill-only thesis finder.

## Local Check

Run the DB-free skill test suite from the repository root:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Optional LLM judge evals require DeepEval and an OpenAI key:

```bash
RUN_DEEPEVAL=1 OPENAI_API_KEY=... python -m pytest -m eval
```

## Monthly Data Refresh

The scheduled workflow runs `scripts/update_openalex_index.py`, updates bundled Markdown data, runs tests, and opens a pull request.

Manual dry run:

```bash
python scripts/update_openalex_index.py --dry-run
```

Fixture-backed run without network:

```bash
python scripts/update_openalex_index.py --fixture skills/tests/fixtures/openalex_works.json
```

## Distribution

The release artifact contains only the portable skill folders needed at runtime.
It intentionally excludes maintainer scripts, tests, docs, `AGENTS.md`,
`CLAUDE.md`, and Python project configuration.

Build locally:

```bash
python scripts/build_skill_release.py
```

The output is:

```text
dist/study-os-thesis-skills-vX.Y.Z.tar.gz
dist/study-os-thesis-skills-vX.Y.Z.zip
```

Each archive expands without an outer `skills/` wrapper:

```text
study-os-thesis-skills-vX.Y.Z/
├── build-student-profile/
│   ├── SKILL.md
│   └── references/
└── ...
```

Target clients:

- Codex: extract the release archive and copy the skill folders into the configured skills location.
- Claude Code: extract the release archive and copy the skill folders into the configured skills/plugin location.
- OpenCode-style clients: install the same `SKILL.md` folders if the client supports Agent Skills.
- Other LLM surfaces: reuse the Markdown instructions and generated references as uploaded files or retrieval documents.

Student-facing skills must use bundled Markdown data first and must not depend on the old UI, backend, database, Docker, Celery, or FastAPI runtime.

Release tags must match the version in `pyproject.toml`: version `0.1.0` is
released with tag `skills-v0.1.0`.

Maintainers do not need to bump the version or create the tag locally. In GitHub
Actions, run **Package skill artifact** and choose `patch`, `minor`, or `major`.
The workflow updates `pyproject.toml`, commits the new version, creates
`skills-vX.Y.Z`, pushes the tag, and publishes the GitHub Release. If the tag
already exists, the workflow fails instead of moving or overwriting it.
