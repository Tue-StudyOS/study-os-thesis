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

**Installing as a student? → [INSTALL.md](INSTALL.md)** — step-by-step setup per route, what
you need before you start, and a troubleshooting table. Grab the artifact for your route from
the [latest release](https://github.com/Tue-StudyOS/study-os-thesis/releases/latest); you do
not need this repository.

Whatever the route, the first prompt is the same:

```
thesis-finder
```

The skill interviews you, builds a structured profile of your interests and constraints,
and returns a map of matching university chairs or BW companies.

---

## Which form of the skill to use

The ten skills in [`skills/`](skills/) are the only source. Three artifacts are **generated**
from them, because the clients students actually use disagree about what a skill is. Pick by
what the target client can load, not by preference.

| Your client | Artifact | Shape | Why this one |
|---|---|---|---|
| **Claude Code, Codex, Gemini CLI** — anything that reads a skills directory | `study-os-thesis-skills-vX.Y.Z.zip` / `.tar.gz` | Ten sibling skill folders | The native form. Name-based hand-offs resolve against sibling folders, and the session log is written to disk automatically. |
| **Claude app** (Pro/Max/Team/Enterprise) | `thesis-finder-app-vX.Y.Z.zip` | One skill folder, the rest nested inside it | claude.ai installs **one skill per upload**, isolated from every other. Ten separate uploads cannot hand off to each other. |
| **ChatGPT, Gemini** — Projects, Custom GPTs, Gems | `thesis-finder-portable-vX.Y.Z.md` + `-instructions-vX.Y.Z.txt` | One document, named sections | Neither loads Agent Skills at all. Their containers hold an instructions box and a handful of files. |
| **Any chat, nothing installed** | the same portable `.md` | Attach and type `thesis-finder` | Works, but nothing is remembered after the chat ends. |

**Or install straight from this repo.** Any client that reads a skills directory can also
skip the release archive and pull `skills/` directly with the third-party
[`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add Tue-StudyOS/study-os-thesis --skill '*' --agent claude-code -g
```

It copies the same ten folders into that client's skills directory — the archive route by
other means. Two consequences: it tracks `main` unless a release tag is appended
(`…/study-os-thesis@skills-v2.1.0`), and `--skill '*'` is required, because a partial pick
breaks the name-based hand-offs. The CLI parses frontmatter with a strict YAML reader and
silently drops any skill that fails it, so `skills/*/SKILL.md` frontmatter is
`yaml.safe_load`-clean and tested as such.

### Why three and not one

Each client breaks the previous form in a specific way:

- **A skills directory** lets `thesis-finder` invoke `find-university-chairs` by name and
  reach `../build-student-profile/references/...` across folders. Both work only because the
  ten folders are siblings on a filesystem.
- **claude.ai** installs one skill per upload, and [skills cannot reference other
  skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Upload
  the ten separately and every hand-off dangles, silently — the run continues with a thinner
  interview instead of failing. Hence one bundle with a routing table.
- **ChatGPT and Gemini** cap a container at roughly ten knowledge files, and ChatGPT caps
  instructions at 8000 characters. The bundle is 21 files and its entry point alone is 17 KB.
  Hence one flat document plus a ~3 KB bootstrap block.

**Do not hand-edit the generated artifacts.** Change the skills under [`skills/`](skills/) and
rebuild — the builders rewrite every cross-skill path for the target shape and refuse to emit
an artifact whose pointers do not resolve:

```bash
make app-bundle         # dist/thesis-finder-app-vX.Y.Z.zip
make portable-bundle    # dist/thesis-finder-portable-vX.Y.Z.md
```

### Session continuity per form

`thesis-finder` keeps a session log so a search can resume weeks later without repeating the
interview. It is handed to the student **twice** per run — once the moment the profile
interview completes, before any searching, and again at the end — because the searching is
the long, abandonable part while the interview is the part that cannot cheaply be redone.

| Form | Where the log lives | Automatic? |
|---|---|---|
| Ten folders (CLI) | `~/.claude/thesis-finder/session.md`, or `./thesis-finder-session.md` if the client cannot write there | Yes |
| App bundle | The Claude **project's** knowledge base | No — the student must add the file |
| Portable | The **project / Custom GPT / Gem** the chat runs in | No — the student must add the file |

Outside the CLI form there is no durable filesystem, so both generated artifacts override the
path instructions at the heading where they are read, and search attached files and container
knowledge instead. The one manual step that remains — dropping the handed-back file into the
container — is what [INSTALL.md](INSTALL.md) is built around.

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

Tests need only `pytest` and `pyyaml`, and run from the repo root:

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
├── scripts/
│   ├── build_skill_release.py       packages skills into tar.gz + zip
│   ├── build_app_bundle.py          folds them into one Claude-app skill
│   └── build_portable_bundle.py     flattens them into one portable document
├── docs/thesis-report/               project genesis & decision history (thesis writeup)
├── INSTALL.md                       student-facing install guide (also shipped in the archive)
├── CHANGELOG.md                     release notes, SemVer policy
├── MASTERPLAN.md                    stable plan: what we build, in what order, why
├── STATUS.md                        living progress doc: current state + decisions
└── .github/workflows/               qa.yml · package-skills.yml · codex-multiturn-evals.yml
```

---

## Release artifacts

GitHub releases (`skills-vX.Y.Z`) publish **five files** — no tests, scripts, or maintainer
files. See [Which form of the skill to use](#which-form-of-the-skill-to-use) for picking one.

**1. Skill directory archive** — `study-os-thesis-skills-vX.Y.Z.zip` / `.tar.gz`

```
study-os-thesis-skills-vX.Y.Z/
├── INSTALL.md                       the install guide travels with the archive
├── build-student-profile/
│   ├── SKILL.md
│   └── references/
└── ... (10 skills total)
```

Copy the extracted skill folders — the contents, not the versioned wrapper — into any agent's
skills directory. All ten: `thesis-finder` routes into the others by name, so a partial
install dangles at the first hand-off.

**2. Claude-app bundle** — `thesis-finder-app-vX.Y.Z.zip`, built by
[`scripts/build_app_bundle.py`](scripts/build_app_bundle.py)

```
thesis-finder/
├── SKILL.md                         entry point + generated routing table
└── skills/
    ├── build-student-profile/
    │   ├── INSTRUCTIONS.md          not SKILL.md: only the root is a registered skill
    │   └── references/
    └── ... (8 skills; design-agent-skill is excluded)
```

Uploaded as-is, never unpacked. Cross-skill paths are rewritten to the bundle root.

**3. Portable edition** — `thesis-finder-portable-vX.Y.Z.md` plus
`thesis-finder-portable-instructions-vX.Y.Z.txt`, built by
[`scripts/build_portable_bundle.py`](scripts/build_portable_bundle.py)

One document whose sections (`## Skill: x`, `## Reference: x/references/y.md`) are what
hand-offs point at, since there is no filesystem to resolve a path against. The `.txt` is the
same bootstrap block that appears inside the `.md`, split out so it can be pasted into an
instructions box without opening the document.

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
