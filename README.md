# Thesis-Option Finder

Portable AI-agent skills that take a Tübingen student from vague research interests to a
prepared first contact with a fitting thesis supervisor — no login, no database, no backend.

## Quickstart

Open this repository in any capable coding agent (Claude Code, Codex, Gemini CLI) and type:

```
thesis-finder
```

The skill interviews you, builds a structured profile of your interests and constraints,
and returns a map of matching university chairs or BW companies.

---

## What you get

A **two-track discovery** based on your profile:

| Track | What it finds |
|---|---|
| University | Tübingen chairs and research groups that match your interests, with research-fit rationale and conversation starters |
| Industry | BW companies with relevant R&D teams, thesis programs, and contact paths |

After discovery, `draft-thesis-contact` can write a first-contact email for any option you choose.

## What this does NOT do

- Does not write your thesis
- Does not guarantee an open topic — openings must be confirmed directly
- Is not an official university portal
- Does not store your data (your profile lives only in the conversation session)

---

## Architecture

**No database. No backend. No monthly update job.**

The intelligence lives in two places:

1. **Reference files** — curated Markdown under each skill's `references/` directory:
   - `tuebingen-faculty-backbone.md` — official `uni-tuebingen.de` listing URLs for every faculty, used as the anti-SEO-bias anchor for university discovery
   - `search-strategy.md` — 9 sections encoding query logic: how to translate profile dimensions into queries, faculty routing, two-pass strategy, dedup, no-go filters, 18 query skeletons, 2 worked examples
   - `bw-company-backbone.md` — ~107 BW companies across 7 sectors, tagged for first-pass filtering
   - `company-search-strategy.md` — parallel query logic for company discovery

2. **Live web search** — every discovery run enriches with current information; the backbone files are the structural anchor, not the data source

This means the skills never go stale in the way a database does. A student running the skill today gets live R&D pages, not a snapshot from months ago.

---

## Skill flow

```
build-student-profile
    │  structured interview (one question per turn)
    │  → 6-dimension profile: interests · methods · domain · thesis style · skills · no-gos
    ▼
thesis-finder
    │  checks profile completeness, asks which track
    ├──▶ find-university-chairs
    │       Pass 1: filter official faculty listing pages (backbone)
    │       Pass 2: live enrichment per chair / research group
    │       → option map grouped by interest dimension
    └──▶ find-company-thesis-options
            Pass 1: filter ~107 BW companies by sector tags (backbone)
            Pass 2: live enrichment (R&D focus, thesis signal, contact path)
            → option map grouped by interest dimension

(optional)
generate-thesis-directions   → research-proposal sketches from the chosen option
draft-thesis-contact         → first-contact email for a specific chair or company
```

Supporting skills (not part of the student flow):
- `find-recent-papers` — relevant papers as background evidence
- `design-agent-skill` — meta-skill for designing or reviewing new skills

---

## Quality gates

Tests are dependency-free (`pytest` only) and run from the repo root:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

The release builder validates skill structure and packages all 8 skills:

```bash
python scripts/build_skill_release.py
```

Fixture-based multiturn evals (no API key required):

```bash
python -m pytest skills/tests/test_codex_multiturn_eval.py -q
```

Live LLM-as-judge evals (optional, requires DeepEval + API key):

```bash
RUN_DEEPEVAL=1 OPENAI_API_KEY=... python -m pytest skills/tests/evals -m eval -q
```

CI (`qa.yml`) runs the full `pytest -q` suite on every PR. `package-skills.yml`
runs `pytest -q` + the release build as a release gate.

---

## Repository layout

```
study-os-thesis/
├── skills/
│   ├── build-student-profile/
│   │   ├── SKILL.md
│   │   └── references/student-profile-schema.md
│   ├── find-university-chairs/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── tuebingen-faculty-backbone.md
│   │       └── search-strategy.md
│   ├── find-company-thesis-options/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── bw-company-backbone.md
│   │       └── company-search-strategy.md
│   ├── thesis-finder/SKILL.md
│   ├── generate-thesis-directions/SKILL.md
│   ├── draft-thesis-contact/SKILL.md
│   ├── find-recent-papers/SKILL.md
│   ├── design-agent-skill/SKILL.md
│   └── tests/                       deterministic + eval tests
├── scripts/build_skill_release.py   packages skills into tar.gz + zip
├── docs/research/                   research package + architecture rationale
├── MASTERPLAN.md                    stable plan: what we build, in what order, why
├── STATUS.md                        living progress doc: current state + decisions
└── .github/workflows/               qa.yml · package-skills.yml · codex-multiturn-evals.yml
```

---

## Release artifact

GitHub releases (`skills-vX.Y.Z`) publish a skill-only archive — no tests, scripts,
or maintainer files:

```
study-os-thesis-skills-vX.Y.Z/
├── build-student-profile/
│   ├── SKILL.md
│   └── references/
├── find-university-chairs/
│   ├── SKILL.md
│   └── references/
└── ... (8 skills total)
```

Copy the extracted skill folders directly into any agent's skills directory.

Publish via **Package skill artifact** in GitHub Actions (choose `patch`, `minor`,
or `major`). Release notes are maintained in [CHANGELOG.md](CHANGELOG.md).

---

## Architecture rationale

This project started as a hosted web app (FastAPI + Celery + Postgres + React).
That stack is archived on the [`legacy/web-app`](../../tree/legacy/web-app) branch.
The pivot to a skill-only architecture is documented in
[docs/research/skill_architecture_summary.md](docs/research/skill_architecture_summary.md).

The core argument: a web app with a curated professor database requires a person
to keep the data fresh. A skill with a search strategy + a backbone of structural
anchors + live web access is self-refreshing and runs anywhere.
