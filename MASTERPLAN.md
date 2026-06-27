# Masterplan — StudyOS Thesis-Finder

> **Purpose:** The zoomed-out view of the whole effort. This file is a
> **lookup** — it describes *what* we build, *in what order*, and *why*. It
> changes rarely.
>
> **For current progress, open difficulties, and notes see [STATUS.md](STATUS.md)** —
> that is the only file that is updated continuously.

---

## 1. What we build

A public, portable **Agent Skill package** that simplifies the *cold start* of
the thesis search. It takes a student from vague interests, coursework, skills,
and constraints to a **clear map of the possibilities** — which chairs, groups,
people, and (later) companies fit them — so they know what exists and where to go
next.

**Core principle: no runtime database, no backend.** The skill encodes *how*
Claude interviews the student and *how* it searches the live web. It works for
**all faculties of the University of Tübingen** immediately and stays correct
because it reads the live web, not a curated store that rots. This is a deliberate
choice: the system must be **maintenance-free** — no one will keep a database
fresh after this project.

The agent gives a **targeted direction and clarifies options**. It does not do the
whole job, write the thesis, or guarantee complete coverage. "Good enough,"
honestly stated, beats a precise database that decays.

The durable product is:

- portable `skills/` folders with concise `SKILL.md` entrypoints
- Markdown `references/` files that encode search strategy, the Tübingen faculty
  backbone, rubrics, and schemas
- `AGENTS.md` as the maintainer and agent operating guide
- an eval harness that compares the skill against a plain-Claude baseline
- durable findings under `findings/`

The student-facing skill flow:

```text
raw input ("I like deep learning + healthcare, hate hardware setup")
   |
   v  build-student-profile      ordered interview (one question, max two per turn)
   v  discover-thesis-options    profile -> search templates -> faculty backbone + live web -> MAP of options
   v  draft-thesis-contact       (optional) first-contact message for a chosen option
```

Maintenance / meta assets:

- `design-agent-skill` is the meta-skill for creating, reviewing, or reshaping
  any skill.
- `find-recent-papers` is an optional evidence tool; `generate-thesis-directions`
  is optional and de-emphasized — we deliver a *map*, not finished proposals.
- `AGENTS.md` explains how future agents extend the package (e.g. companies, other
  universities).

---

## 2. Why no database

| Database approach (former direction) | Database-less approach (this plan) |
|---|---|
| Goes stale within months | Always current (live web) |
| CS Tübingen only | All faculties, immediately |
| Needs GitHub Actions to refresh | Zero ongoing maintenance |
| Only covers what is curated | Covers what is publicly visible |
| Does not scale to companies | Companies use the same principle |

The skill is the intelligence; the data comes from the world. Curated chair/prof
data is kept **only as an evaluation ground truth**, never as a runtime source.

---

## 3. The core IP — how the skill searches

The value over "just ask Claude" lives in two references the discovery skill
carries:

1. **Search strategy** — the reusable mapping from profile dimensions (interests,
   methods, domain, thesis style, no-gos) to precise web queries, plus quality
   filters, dedup rules, and profile→faculty routing.
2. **Faculty backbone** — the official `uni-tuebingen.de` listing pages per
   faculty, crawled first so discovery starts from the real org structure and not
   only from SEO-strong pages.

The discovery is **two-pass**: (1) crawl the backbone to get the structured chair
set per relevant faculty; (2) enrich with live queries for topics, recent work,
and openings. Output is a **map of options** grouped by interest dimension, each
with relevance rationale, pros/cons & difficulties, dated evidence, and a
conversation starter — ending with an honest coverage caveat.

---

## 4. Ordering principle

**Prove the university arm first, then extend.** Companies are a structurally
harder, chaotic discovery problem; they wait until the core is empirically shown
to work. Within the university arm: build the search references, then the skill,
then measure it against a small hand-curated ground truth and against a
plain-Claude baseline.

---

## 5. Phase 1 — University discovery (current phase)

The executable backlog (full detail in
[findings/no_db_universal_skill/2026-06-26-build-plan.md](findings/no_db_universal_skill/2026-06-26-build-plan.md)).
Each task is one agent run.

| Task | What it is about | Depends on |
|---|---|---|
| A | Conversation discipline in `build-student-profile` (one question, max two per turn; precise answers) | – |
| B | Faculty backbone reference: official Tübingen faculty/chair listing URLs | – |
| C | Search-strategy reference: profile → precise queries, two-pass, filters, faculty routing | B |
| D | Rework `find-university-chairs` into the faculty-agnostic discovery skill (map output, no DB) | B, C |
| E | Retire DB assets (`match-thesis-advisors`, `update-openalex-paper-index`, seed data → eval-only) | D |
| F | Eval ground truth for 3–4 faculties + coverage metric | – |
| G | Wire discovery into Max's multiturn eval harness (skill vs. plain-Claude baseline) | D, F |
| H | Run the eval, measure coverage and the skill-vs-baseline delta, document | G |

Dependency graph:

```text
A (interview) ----------------------------------.
B (backbone) -> C (search strategy) -> D (skill) -> E (retire DB)
                                          \         \
F (ground truth) --------------------------+-------- G (harness) -> H (results)
```

Gate Phase 1 → Phase 2:

- discovery skill runs end-to-end on a sample profile with no DB dependency
- ground truth exists for ≥3 faculties with a defined coverage metric
- the harness reports coverage and a skill-vs-plain-Claude comparison
- coverage meets the agreed starting target (≥70%) on the ground-truth sample

---

## 6. Phase 2 — Company discovery (later)

Add external-company thesis discovery only after the university arm is proven. The
likely approach is a **one-time** curated list (e.g. companies in
Baden-Württemberg) tagged by area/hashtags — the one acceptable static asset,
because there is no clean live-search equivalent. New startups are a known later
gap.

---

## 7. Phase 3 — Distribution & cross-platform

- **Distribution channels:** Fachschaft Informatik, Hennig-GitHub, Ersti-Heft,
  and ideally surfacing on the university site / "How to find a thesis" pages so
  students who google the problem find the skill.
- **Cross-platform:** keep the content portable across capable coding-agent
  clients (Codex, Claude, Gemini CLI). Avoid client-specific metadata without a
  documented portable fallback.

---

## 8. How this plan is used

- `MASTERPLAN.md` = stable structural plan. Change it only when the product goal,
  phase structure, or major workflow changes.
- `STATUS.md` = living progress document. Update status, blockers, decisions, and
  dated logs there.
- `findings/no_db_universal_skill/` = the concept, risks, exact build plan, and
  eval results for this direction.
- `AGENTS.md` = operating instructions for future agents and maintainers.
- GitHub Issues = executable work units mirroring Tasks A–H.
