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
   - `discover-university-candidates/references/university-discovery-rules.md` — source axes, verification rules, and ranking rules for live Tübingen candidate discovery
   - `discover-company-candidates/references/company-discovery-rules.md` — source axes, verification rules, and ranking rules for live BW company candidate discovery
   - `find-university-chairs/references/search-strategy.md` — enrichment, PI/affiliation checks, no-go filters, and output rules after university candidates are found
   - `find-company-thesis-options/references/company-search-strategy.md` — thesis-signal, contact-path, recency, no-go, and output rules after company candidates are found

2. **Live web search** — every discovery run creates a temporary candidate set and then verifies current information. The backbone is now the discovery logic, not a static URI or entity catalog.

This means the skills never go stale in the way a database does. A student running the skill today gets live R&D pages, not a snapshot from months ago.

---

## Skill flow

```
thesis-finder                ← single entry point
    │  inline interview if no profile yet (one question per turn)
    │  → 6-dimension profile: interests · methods · domain · thesis style · skills · no-gos
    │  asks which track
    ├──▶ find-university-chairs
    │       Candidate pass: discover-university-candidates live source axes
    │       Enrichment pass: PI/affiliation, evidence, thesis-signal checks
    │       → option map grouped by interest dimension
    └──▶ find-company-thesis-options
            Candidate pass: discover-company-candidates live source axes
            Enrichment pass: R&D focus, thesis signal, contact path
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

The release builder validates skill structure and packages all 10 skills:

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
│   ├── discover-university-candidates/
│   │   ├── SKILL.md
│   │   └── references/university-discovery-rules.md
│   ├── discover-company-candidates/
│   │   ├── SKILL.md
│   │   └── references/company-discovery-rules.md
│   ├── find-university-chairs/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── search-strategy.md
│   ├── find-company-thesis-options/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── company-search-strategy.md
│   ├── thesis-finder/SKILL.md
│   ├── generate-thesis-directions/SKILL.md
│   ├── draft-thesis-contact/SKILL.md
│   ├── find-recent-papers/SKILL.md
│   ├── design-agent-skill/SKILL.md
│   └── tests/                       deterministic + eval tests
├── scripts/build_skill_release.py   packages skills into tar.gz + zip
├── docs/thesis-report/               project genesis & decision history (thesis writeup)
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
└── ... (10 skills total)
```

Copy the extracted skill folders directly into any agent's skills directory.

Publish via **Package skill artifact** in GitHub Actions (choose `patch`, `minor`,
or `major`). Release notes are maintained in [CHANGELOG.md](CHANGELOG.md).

---

## Architecture rationale

This project started as a hosted web app (FastAPI + Celery + Postgres + React).
That stack is archived on the [`legacy/web-app`](../../tree/legacy/web-app) branch.
The pivot to a skill-only architecture is documented in
[skill_architecture_summary.md](docs/thesis-report/00-problem-and-research/2026-06-12-professor-research-package/skill_architecture_summary.md).

The full genesis story — pre-pivot research, the pivot decision, how the skill was built
and hardened, and what's still open — is curated in
[docs/thesis-report/](docs/thesis-report/README.md), written for the thesis submission.

The core argument: a web app with a curated professor database requires a person
to keep the data fresh. A skill with live candidate discovery, explicit source
axes, verification rules, and current web access is self-refreshing and runs
anywhere.
