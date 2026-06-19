# Skill Architecture Summary - Skill-Only Thesis Finder

**Date:** 2026-06-11 | **Updated:** 2026-06-13 | **Context:** Full pivot from app runtime to portable skills + generated Markdown data
**Related docs:** [detailed_analysis.md](detailed_analysis.md), [product_positioning.md](product_positioning.md), [technical_roadmap.md](technical_roadmap.md)

This note supersedes the earlier Claude-only and 3-skill MVP proposals. The long-term target is now a repository that can drop the old UI, backend, database, Docker, Celery, and FastAPI runtime. The durable product becomes:

- portable `SKILL.md` folders under `skills/`
- versioned Markdown data under skill `references/`
- a lightweight monthly GitHub Action that refreshes public OpenAlex data

Student-facing skills must work from bundled Markdown first. Live web/OpenAlex access is only a fallback when the active agent provides tools.

---

## 1. Target Architecture

Runtime for students:

- The user's coding agent loads skills from `skills/`.
- Skills read local Markdown indexes under `references/`.
- Private student data stays in the active agent session.
- No student-facing skill depends on the old DB, API, Docker, Celery, React UI, or FastAPI app.

Update runtime:

- A monthly GitHub Action runs `scripts/update_openalex_index.py`.
- The script reads known researchers and OpenAlex Author IDs from Markdown.
- It fetches recent works from OpenAlex and regenerates researcher and paper indexes.
- It runs DB-free skill tests and optionally LLM-as-judge evals.
- It opens a PR with generated Markdown changes.

The generated Markdown files are the new database.

---

## 2. Skill Suite

The target package is:

```text
skills/
+-- design-agent-skill/
+-- build-student-profile/
+-- find-recent-papers/
+-- find-university-chairs/
+-- match-thesis-advisors/
+-- generate-thesis-directions/
+-- draft-thesis-contact/
+-- update-openalex-paper-index/
```

Skill responsibilities:

- `design-agent-skill`: meta-skill for designing and reviewing portable skills.
- `build-student-profile`: extracts interests, courses, skills, constraints, and preferences into an in-session profile.
- `find-recent-papers`: reads bundled paper/researcher indexes and explains recent paper relevance.
- `find-university-chairs`: reads bundled chair/researcher indexes and identifies labs or supervisors.
- `match-thesis-advisors`: combines profile, papers, and chair data into an evidence-based ranking.
- `generate-thesis-directions`: turns matches and papers into thesis directions or conversation starters.
- `draft-thesis-contact`: writes specific first-contact emails.
- `update-openalex-paper-index`: maintenance skill for monthly Markdown data generation.

This split maps more closely to the old UI's workflows without recreating the app runtime.

---

## 3. Data Layout

OpenAlex data belongs primarily to researchers, not chairs, because OpenAlex works are author-centric. Chair files aggregate people and research areas.

```text
skills/find-university-chairs/references/
+-- chairs/
|   +-- INDEX.md
|   +-- <chair-slug>.md
+-- researchers/
    +-- INDEX.md
    +-- <person-slug>.md

skills/find-recent-papers/references/
+-- papers/
    +-- INDEX.md
    +-- by-topic/
    |   +-- INDEX.md
    |   +-- <topic-slug>.md
    +-- by-year/
        +-- INDEX.md
        +-- 2026.md
        +-- 2025.md
```

Researcher profiles store:

- name, role, chair/lab, website
- OpenAlex Author ID
- last updated date
- research areas and keywords
- selected recent papers
- DOI/OpenAlex/source URLs
- short thesis angles
- caveats for affiliation or missing data

Chair profiles store:

- chair/lab metadata
- linked researcher profiles
- aggregated research areas
- matching student skills/interests
- contact preparation notes

---

## 4. Monthly OpenAlex Update

The monthly update flow is:

```text
GitHub Action cron
-> scripts/update_openalex_index.py
-> read researchers/INDEX.md
-> fetch OpenAlex works by author id
-> deduplicate by DOI, OpenAlex ID, normalized title
-> update researcher profiles
-> update paper indexes by topic and year
-> run skill tests
-> optionally run LLM judge evals
-> open PR
```

Implementation constraints:

- no backend imports
- no DB
- no Docker
- no FastAPI
- no third-party package requirement for the fetch script
- optional OpenAlex polite-pool email via `OPENALEX_MAILTO`

---

## 5. Testing And Quality Gates

Normal skill tests are DB-free and run from the repo root:

```bash
python -m pytest
```

They verify:

- the complete skill suite exists
- every `SKILL.md` has portable frontmatter
- referenced files exist
- generated-data index templates exist
- private student data is not bundled
- student-facing skills reject old runtime dependencies

Optional LLM-as-judge evals stay gated:

```bash
RUN_DEEPEVAL=1 OPENAI_API_KEY=... python -m pytest -m eval
```

These evals check behavior for profile extraction, paper discovery, chair discovery, advisor matching, thesis direction generation, contact drafting, and OpenAlex maintenance.

---

## 6. Recommendation

Proceed with the skill-only architecture:

- Treat Markdown files as the durable data layer.
- Treat GitHub Actions as the only scheduled automation.
- Treat OpenAlex live access as a maintenance concern, not a student-facing runtime dependency.
- Keep the old backend/UI only as temporary source material until the skill package and generated Markdown data are sufficient.

The key design choice is settled: **fetch and commit Markdown data monthly, then let student-facing skills read it locally.**
