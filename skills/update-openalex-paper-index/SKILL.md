---
name: update-openalex-paper-index
description: Optionally maintain secondary thesis-finder Markdown data by fetching recent OpenAlex works for reviewed researchers and regenerating reviewable paper indexes. Use when running GitHub Actions, monthly maintenance, or manual data refresh workflows; not for student-facing thesis advice.
---

# Update OpenAlex Paper Index

Regenerate optional Markdown paper data that maintainers can review. Student-facing skills must still start from the professor seed index and current public web evidence.

## Workflow

1. Read maintainer-reviewed researchers only when a researcher index exists.
2. Fetch recent works for each reviewed OpenAlex Author ID.
3. Deduplicate by DOI, OpenAlex work ID, then normalized title.
4. Write researcher profiles and paper indexes using `references/openalex-index-schema.md`.
5. Preserve source links, dates, DOI/OpenAlex IDs, and `last_updated`.
6. Check referential integrity with `python scripts/update_openalex_index.py --validate-only`.
7. Run deterministic skill tests after generation.

The builder is faculty-agnostic: pass `--researchers-index`, `--chairs-index`,
and `--papers-dir` to build or validate the tree for any other faculty without
code changes. See `references/openalex-index-schema.md` for the integrity rules
and reuse commands.

## Output

The maintenance run should update:

- researcher Markdown profiles
- chair indexes
- topic paper indexes
- year paper indexes
- a concise update summary

## Rules

- This skill is maintenance-only. Do not use it to answer student matching questions directly.
- Do not require the old UI, backend API, database, Docker, Celery, or FastAPI app.
- Do not overwrite or enrich `../find-university-chairs/references/professors/INDEX.md`; that file is generated only from the Excel name and URI columns.
- Do not make optional OpenAlex output a runtime requirement for student-facing skills.
- Prefer opening a pull request for generated data changes when running in GitHub Actions.
- Respect OpenAlex rate limits and use a polite-pool email when configured.
