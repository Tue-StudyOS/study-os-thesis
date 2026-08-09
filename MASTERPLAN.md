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
- Markdown `references/` files that encode search strategy, live source axes,
  verification rules, rubrics, and schemas
- `AGENTS.md` as the maintainer and agent operating guide
- an eval harness that compares the skill against a plain-Claude baseline
- durable findings under `findings/`

The student-facing skill flow:

```text
raw input ("I like deep learning + healthcare, hate hardware setup")
   |
   v  build-student-profile      ordered interview (one question, max two per turn)
   v  find-university-chairs / find-company-thesis-options
      -> dedicated live candidate discovery -> verified candidates -> MAP of options
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

The value over "just ask Claude" lives in the discovery rules the skill package
carries:

1. **Candidate discovery rules** — reusable source axes for companies and
   university groups, including official sites, research clusters, partner lists,
   internal site search, and profile-generated queries.
2. **Enrichment strategy** — reusable checks for topic fit, recency, thesis
   signals, PI/contact verification, no-go handling, dedup, and output shape.

The discovery is **two-pass**: (1) build a temporary, profile-specific candidate
table from multiple live source axes; (2) enrich the verified candidates with
live queries for topics, recent work, people, contact paths, and openings. Output
is a **map of options** grouped by interest dimension, each with relevance
rationale, pros/cons & difficulties, dated evidence, and a conversation starter
— ending with an honest coverage caveat.

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
| B | University candidate discovery rules: source axes without static faculty URI lists | – |
| C | Search-strategy reference: profile → precise queries, two-pass, filters, routing | B |
| D | Rework `find-university-chairs` into the faculty-agnostic discovery skill (map output, no DB) | B, C |
| E | Retire DB assets (`match-thesis-advisors`, `update-openalex-paper-index`, seed data → eval-only) | D |
| F | Eval ground truth for 3–4 faculties + coverage metric | – |
| G | Wire discovery into Max's multiturn eval harness (skill vs. plain-Claude baseline) | D, F |
| H | Run the eval, measure coverage and the skill-vs-baseline delta, document | G |

Dependency graph:

```text
A (interview) ----------------------------------.
B (candidate rules) -> C (search strategy) -> D (skill) -> E (retire DB)
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

Add external-company thesis discovery only after the university arm is proven.
The current approach is rules-only: a dedicated candidate-discovery skill builds
a temporary BW company set from multiple live source axes. "Top 100" company
lists may be consulted as one minority source axis, but they are not the
backbone; they are size/brand-biased and cannot be the main path.

---

## 7. Phase 3 — Distribution & cross-platform

- **Distribution channels:** Fachschaft Informatik, Hennig-GitHub, Ersti-Heft,
  and ideally surfacing on the university site / "How to find a thesis" pages so
  students who google the problem find the skill.
- **Cross-platform:** keep the content portable across capable coding-agent
  clients (Codex, Claude, Gemini CLI). Avoid client-specific metadata without a
  documented portable fallback.

---

## 8. Phase 4 — Hardening (DONE, 2026-07-04; GO verdict flagged provisional 2026-07-05)

Phase 3 made the skill package coherent and distributable; Phase 4 made the university
core (Tübingen) not just *pass the gate* but genuinely *work well* across recall,
precision, steering, output quality, and robustness on structurally hard faculties. The
explicit go/no-go on the roadmap's "core is done" bar flipped to **GO** on 2026-07-04: all
6 measured faculties (2 of them hard) clear ≥80% recall, precision/steering/output-quality/
robustness all measured and passing — **all of it `[backbone-crawl, ≤2026-07-30]`** (Task AJ,
2026-08-09). Full task list, tracks, and the bar definition:
[findings/no_db_universal_skill/2026-06-28-core-optimization-roadmap.md](findings/no_db_universal_skill/2026-06-28-core-optimization-roadmap.md).
Verdict and evidence: [2026-07-03-core-done-go-no-go.md](findings/no_db_universal_skill/2026-07-03-core-done-go-no-go.md).
All numbers: [2026-07-03-eval-aggregate-scorecard.md](findings/no_db_universal_skill/2026-07-03-eval-aggregate-scorecard.md).
Live status per task: `STATUS.md`, section "Post-Phase-3 hardening".

**Independent-review caveat (2026-07-05):** an independent 1.0-readiness review
([2026-07-05-fable-1.0-readiness-review.md](findings/no_db_universal_skill/2026-07-05-fable-1.0-readiness-review.md))
found the two hard-faculty numbers behind the GO are not clean blind measurements —
Humanities' 100% is a transparent re-score by a session that was explicitly un-blind on
that faculty, and Law's 80% was produced by a re-run whose session had already read the
document naming the missed chair and the fix that flips her. Every genuinely blind
hard-faculty run to date (Humanities 60%, Law 60% — both `[backbone-crawl, ≤2026-07-30]`)
landed below the 80% bar. This does
**not** roll back the GO or any skill fix (Task U's enrich-before-exclude rule is real
and independently verified elsewhere in the same evidence) — it flags the verdict as
**provisional** pending one clean blind hard-faculty run. See Phase 5 Task V′ below.
**Closed for one faculty on 2026-08-08:** Task V′ ran Theology blind — 83% recall / 100%
precision, `[rules-only, ≥2026-07-31]` — the first clean blind hard-faculty run, and
simultaneously the first faculty measurement of the shipping architecture.

**Architecture caveat (2026-08-08):** every number above was produced by the
**backbone-crawl architecture**, which was removed on 2026-07-31 (commit `44e7e53`,
merged in PR #71) in favour of rules-only live candidate discovery — see §3 and
[2026-07-30-rules-only-backbone.md](findings/dev_process/2026-07-30-rules-only-backbone.md).
The Phase 4 verdict is therefore provisional on a second count: it certifies an
architecture that no longer ships. Phase 5 Tasks AJ (label every number with the
architecture that produced it), V′ and AK (re-measure post-pivot), and AL (commit
simulation evidence for the shipping architecture) are the named repair.

---

## 9. Phase 5 — 1.0: repair the evidence, ship, tell (final scoping 2026-08-08)

Phase 5 was scoped three times. 2026-07-05: the independent 1.0-readiness review (Tasks
V–AA, thesis-committee framing). 2026-07-16: re-scoped against the course grading scheme
(five components × 20%), on a branch that was never merged. **2026-08-08: final scoping**,
which folds in two things the earlier plans could not know — the rules-only architecture
pivot (2026-07-31) and P. Gehler's answers of 2026-08-05.

Two decisions drive this scoping:

1. **Gehler's outcome variable.** Asked whether the generated proposals or the students'
   own reflection matters more, he answered: *"Students that have reflected about what
   topic they would like to work on. This likely has sharpened their understanding what
   kind of thesis topic that would be the best fit."* The graded outcome is therefore user
   change, not artifact quality. Response chosen 2026-08-08: **reframe and measure, do not
   rewrite the skills** — the value proposition becomes reflection (G3), the beta protocol
   gets a pre/post reflection statement (AC′), and the simulation rubric gets a reflection
   dimension (AL).
2. **The evidence break.** Every recall/precision/steering number this project owns was
   produced by the backbone architecture removed on 2026-07-31 (see §8). The shipping
   architecture has essentially no committed evidence. Tasks AJ, V′, AK and AL repair
   this; it is the largest single block of new work in Phase 5.

Authoritative, exact task-by-task plan (steps, done-when criteria, dependencies, models):
[findings/no_db_universal_skill/2026-08-08-final-1.0-plan.md](findings/no_db_universal_skill/2026-08-08-final-1.0-plan.md).

| Task | What it is about | Grading |
|---|---|---|
| AJ | Pivot evidence audit — tag every number in the repo with the architecture and date that produced it; demote the company eval permanently | G5, G4 |
| V′ | Blind Theology run — the only untouched hard-faculty ground truth; first clean blind number *and* first post-pivot faculty number. **Run before anything else touches eval material** | G5 |
| AK | Post-pivot re-measurement of 2 faculties (CS + one hard) — the architecture before/after the repo asked for on 2026-07-30 and never ran | G5, G1 |
| AL | Reflection dimension in the simulation rubric + one committed 8-persona evidence set for the shipping architecture (`.simulations/` is gitignored today) | G5, G4 |
| AA′ | Hygiene sweep, post-pivot: 4 of the original 8 items are already resolved by the pivot; delete the last static URI catalog (paper index), fix the CS-only degree file and the hardcoded session path, add a no-static-catalog invariant test. **Release blocker** | G4 |
| AB′ | Re-release + `INSTALL.md`, cold-install tested. `skills-v1.0.0` (2026-07-06) ships the deleted architecture and must be superseded | G5, G4 |
| AC′ | Beta protocol + feedback form, **reflection-first**: verbatim pre/post "what kind of thesis am I looking for" as the primary instrument | G2, G5 |
| Z′ | Protocolled external test, 2–3 students, ≥1 non-CS, on the release artifact; testers co-score (absorbs old Task X); debriefs double as student interviews | G2, G5 |
| AD | Distribution outreach: Fachschaft Informatik + Menth/Gehler channel question. No self-sent Rundmail | G5 |
| AM | Reconstructed user-study chapter with per-entry provenance (documented vs. from memory) — explicitly invited by Gehler | G2, G5 |
| AN | Future-feedback plan: what feedback, when, by whom, how many — as a table with named responsibilities | G5 |
| AO | Survival & maintenance plan — the rules-only pivot *is* the sustainability argument; state the real maintenance hours, ownership options with failure modes, and graceful degradation | G5, G3, G1 |
| AE′ | Benchmark consolidation across both architectures; names the reflection variable as measured only qualitatively | G5, G4 |
| AF–AH | Report chapters: problem framing & evolution (now three dated steps) / user research & evidence / concept & solution design (reframed value proposition) | G1 / G2 / G3 |
| AI | Final written report assembly — five rubric sections, every claim linked to an artifact, every number architecture-tagged | all |
| W | Scope-erosion experiment — **optional stretch**; reachable in the 4+ week window, but its hypothesis needs restating post-pivot | G5, G1 |

Old Tasks X and Y no longer exist: X folds into Z′ (tester co-scoring), Y is closed by AJ
item 4 (permanent demotion, the 2026-07-05 review's own named alternative). Task L
(company-backbone taxonomy) was superseded outright by the rules-only pivot.
Execution order: V′ first and blind, then {AJ, AK, AL} and AA′ → AB′ → AC′ → {AD, Z′
recruiting}; the Gehler chapters (AM, AN, AO) and AF/AH absorb Z′'s calendar latency.
The 2026-07-05 review remains the methodological evidence base.

---

## 10. How this plan is used

- `MASTERPLAN.md` = stable structural plan. Change it only when the product goal,
  phase structure, or major workflow changes.
- `STATUS.md` = living progress document. Update status, blockers, decisions, and
  dated logs there.
- `findings/no_db_universal_skill/` = the concept, risks, exact build plan, and
  eval results for this direction — including the
  [2026-08-08 final 1.0 plan](findings/no_db_universal_skill/2026-08-08-final-1.0-plan.md),
  the current authoritative source for what's left before 1.0. It supersedes the
  [2026-07-16 grading-aligned plan](findings/no_db_universal_skill/2026-07-16-grading-aligned-1.0-plan.md)
  (written pre-pivot, never merged) and the Phase-5 scoping in the
  [2026-07-05 review](findings/no_db_universal_skill/2026-07-05-fable-1.0-readiness-review.md),
  which remains the methodological evidence base.
- `findings/dev_process/` = architecture and process decisions, including the
  [rules-only pivot](findings/dev_process/2026-07-30-rules-only-backbone.md).
- `docs/thesis-report/` = the curated, chronological account for the write-up. **Stale as
  of 2026-08-08** — sections 03 and 04 predate the pivot; Tasks AJ and AF–AI resync them.
- `AGENTS.md` = operating instructions for future agents and maintainers.
- We work without GitHub issues — progress lives in `STATUS.md` and the plan above.
