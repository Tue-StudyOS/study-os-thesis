# Thesis-Option Finder

Portable AI-agent skills that take a Tübingen student from vague research interests to a
prepared first contact with a fitting thesis supervisor — no login, no database, no backend.

**What it is actually for.** The map of chairs and companies is the visible output, but it
is not the point. The point is that you end up with a sharper idea of what kind of thesis
fits you than you started with. The skill asks you at the outset what you think you are
looking for, and asks again at the end — in your own words, both times — and keeps both so
you can see what moved. A search that changes your mind, or convinces you a direction is
wrong, has done its job even if you contact nobody from the list.

## Quickstart

**Installing as a student? → [INSTALL.md](INSTALL.md)** — per-client setup steps, what you
need before you start, and a troubleshooting table. Grab the archive from the
[latest release](https://github.com/Tue-StudyOS/study-os-thesis/releases/latest); you do not
need this repository.

To run it from a checkout instead, open the repository in any capable coding agent
(Claude Code, Codex, Gemini CLI) and type:

```
thesis-finder
```

The skill interviews you, builds a structured profile of your interests and constraints,
and returns a map of matching university chairs or BW companies.

**Install the skills as a set.** `thesis-finder` is a router: it invokes the discovery,
paper, proposal, and contact-draft skills by name, and they invoke each other. Installing a
subset leaves those calls unresolved — install all ten. From a release archive that means
copying its *contents* (the ten skill folders), not the versioned wrapper folder; see
[INSTALL.md](INSTALL.md).

`thesis-finder` keeps a session log so a search can resume weeks later. It prefers
`~/.claude/thesis-finder/session.md`; if your client cannot write there, it falls back to
`./thesis-finder-session.md` in the working directory and tells you which path it used.

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
    │
    │  recommends 1–2 options, then asks: go deeper, or keep exploring?
    ├──▶ go deeper
    │       find-recent-papers   → 1–2 papers from that specific person or lab
    │       → "Deeper Look": fit, evidence, likely work, feasibility, first question
    └──▶ keep exploring          → next direction, then search again

(optional, on request)
draft-thesis-contact         → first-contact email for a specific chair or company
                               (also calls find-recent-papers if none surfaced yet)
```

`find-recent-papers` is invoked by the flow above, not by you. `draft-thesis-contact`
runs only when you ask for it.

Not reachable from `thesis-finder` — invoke by name if you want them:
- `generate-thesis-directions` — research-proposal sketches. Deliberately outside the
  student flow: the product is a *map of options you reflect on*, not a finished
  proposal. See [MASTERPLAN.md](MASTERPLAN.md) §1.
- `design-agent-skill` — meta-skill for designing or reviewing new skills

---

## Measured discovery quality

Honest version first: **the architecture that ships has been measured on exactly one
faculty.**

| | |
|---|---|
| **Theology, blind, 2026-08-08** | **83 % recall / 100 % precision** — [full results](findings/no_db_universal_skill/2026-08-08-theology-blind-run.md) |
| Conditions | First run, genuinely blind, no fix applied first. The only hard faculty to clear the ≥80 % bar without a preceding repair. |
| Everything else | Six further faculties were measured at ≥80 % recall between June and early July 2026 — but **against the static-backbone architecture removed on 2026-07-31**. Those numbers are real and honestly obtained; they do not describe what you install today. |

Every figure in this repository is tagged `[backbone-crawl, ≤2026-07-30]` or
`[rules-only, ≥2026-07-31]` so the two cannot be read as one series. Start at the
[scorecard's standing note](findings/no_db_universal_skill/2026-07-03-eval-aggregate-scorecard.md).

Not yet measured on the current architecture: the other six faculties, the steering proof,
and the margin over plain Claude. The company track has never been measured against an
independent reference list at all and says so to the student at run time.

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

CI (`qa.yml`) runs the full `pytest -q` suite on pull requests that touch `skills/`,
`scripts/`, `pyproject.toml`, or the workflows themselves — a docs-only PR deliberately
gets no run. `package-skills.yml` runs `pytest -q` + the release build as a release gate,
on both of its triggers.

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
├── INSTALL.md                       student-facing install guide (also shipped in the archive)
├── CHANGELOG.md                     release notes, SemVer policy
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
├── INSTALL.md                       the install guide travels with the archive
├── build-student-profile/
│   ├── SKILL.md
│   └── references/
├── find-university-chairs/
│   ├── SKILL.md
│   └── references/
└── ... (10 skills total)
```

Copy the extracted skill folders directly into any agent's skills directory.

**To publish a release**, the version is set on `main` first — it is the single source:

```bash
python scripts/bump_project_version.py minor    # or patch / major
python scripts/release_changelog.py --version X.Y.Z --notes dist/release-notes.md
```

Commit both, merge to `main`, then run **Package skill artifact** in GitHub Actions
(`workflow_dispatch`, no inputs — it reads the version from `pyproject.toml`). The workflow
tags `skills-vX.Y.Z`, points the `release/skills` publish mirror at the released commit, and
publishes the GitHub release with notes from [CHANGELOG.md](CHANGELOG.md).

Note that `skills-v*` tags can only be created by the release GitHub App: a repository
ruleset blocks tag creation for everyone else, so `gh release create` and a manual tag push
both fail. Dispatching the workflow is the only route.

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
