# Skill Distribution And Maintenance

This is the minimal maintainer guide for the skill-only thesis finder.

## Local Check

Run the DB-free skill test suite from the repository root:

```bash
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

The release artifact contains only the portable skill package, scripts, tests, and docs needed after the old app runtime is removed.

Target clients:

- Codex: install or copy the skill folders into the configured skills location.
- Claude Code: install or copy the skill folders into the configured skills/plugin location.
- OpenCode-style clients: install the same `SKILL.md` folders if the client supports Agent Skills.
- Other LLM surfaces: reuse the Markdown instructions and generated references as uploaded files or retrieval documents.

Student-facing skills must use bundled Markdown data first and must not depend on the old UI, backend, database, Docker, Celery, or FastAPI runtime.
