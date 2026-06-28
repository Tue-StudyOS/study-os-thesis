# Thesis-Option Finder

Helps Tübingen students (and students at Baden-Württemberg universities) discover
where to write their thesis — at a Tübingen university chair or at a company in
Baden-Württemberg. No login, no database, no sign-up required.

## How to use

Open this repository in any capable coding agent — Claude Code, Codex, or Gemini
CLI — and type:

```
thesis-finder
```

The skill interviews you (a few quick questions) about your research interests,
courses, and constraints, then produces a short map of chairs or companies that
match your profile.

## What you get

- A relevant subset of Tübingen chairs or BW companies matched to your profile
- A brief research-fit rationale and conversation starters for each option
- An optional first-contact email draft (`draft-thesis-contact`)

## What this does NOT do

- Does not write your thesis
- Does not guarantee any chair or company has an open topic
- Is not an official university portal — openings and supervision capacity must
  be confirmed directly with the chair or company

---

# study-os-thesis

A set of portable **agent skills** that take a student from vague interests to a
prepared first contact with a fitting thesis supervisor — with no backend,
database, or UI. The skills are driven by curated Markdown data plus live
research.

> **Architecture note:** This project pivoted from a hosted web app
> (FastAPI + Celery + Postgres + React) to a skill-only architecture. The old
> web-app stack is archived on the [`legacy/web-app`](../../tree/legacy/web-app)
> branch. See [docs/research/skill_architecture_summary.md](docs/research/skill_architecture_summary.md)
> for why.

## Where to start

| File | What it is |
|---|---|
| [MASTERPLAN.md](MASTERPLAN.md) | The zoomed-out plan: what we build, in what order, and why. Read first. |
| [STATUS.md](STATUS.md) | The single living document: current progress, blockers, decisions. |
| [docs/research/](docs/research/) | The full research package and the rationale for the skill pivot. |

## The skills

```
skills/
├── build-student-profile/        interview → structured profile (in-session only)
├── find-university-chairs/        matching chairs from bundled data + live web search
├── match-thesis-advisors/         supervisors ranked by fit + evidence
├── find-recent-papers/            relevant papers as evidence
├── generate-thesis-directions/    concrete thesis directions + proposal hooks
├── draft-thesis-contact/          first-contact email
├── update-openalex-paper-index/   maintenance: refresh bundled OpenAlex data
└── design-agent-skill/            meta-skill for designing/reviewing skills
```

The bundled "database" is versioned Markdown under each skill's `references/`.
A monthly GitHub Action (`update-openalex-index.yml`) refreshes the OpenAlex data
and opens a PR.

## Quality gates

Skill tests are dependency-free (only `pytest`) and run from the repo root:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q        # or: make check
```

Optional LLM-as-judge evals are skipped by default; they need DeepEval and an
LLM judge configuration:

```bash
pip install deepeval
RUN_DEEPEVAL=1 OPENAI_API_KEY=... python -m pytest skills/tests/evals -m eval -q
```

CI runs the skill tests on every PR (`qa.yml`). The DeepEval checks run via the
manual **LLM Evals** workflow when judge-model credentials are configured.

## Project layout

```
study-os-thesis/
├── skills/                  the portable skills + bundled Markdown data + tests
├── scripts/
│   └── update_openalex_index.py   standalone OpenAlex refresh (no backend deps)
├── docs/research/           research package + architecture rationale
├── MASTERPLAN.md            stable plan
├── STATUS.md                living progress doc
└── .github/workflows/       CI: skill tests, evals, packaging, monthly refresh
```

## Release artifact

GitHub releases tagged as `skills-vX.Y.Z` publish a skill-only archive:

```text
study-os-thesis-skills-vX.Y.Z/
├── build-student-profile/
│   ├── SKILL.md
│   └── references/
└── ...
```

The archive intentionally excludes maintainer files such as tests, scripts,
docs, `AGENTS.md`, `CLAUDE.md`, and `pyproject.toml`. Copy the extracted skill
folders directly into a client skills directory.

Release notes are written for humans in [CHANGELOG.md](CHANGELOG.md). Maintainer
PRs should update `## [Unreleased]`; the release workflow turns that section
into the GitHub Release description.

Maintainers can publish a release from GitHub Actions by running **Package skill
artifact** manually and choosing a `patch`, `minor`, or `major` bump. The
workflow checks out the release branch, updates `pyproject.toml`, commits the
new version there, creates the `skills-vX.Y.Z` tag, and publishes the release
artifacts. The default release branch is `release/skills`; `main` is not
modified by the release workflow. The workflow authenticates as the installed
`study-os-release-bot` GitHub App via `RELEASE_APP_ID` and
`RELEASE_APP_PRIVATE_KEY` repository secrets.
