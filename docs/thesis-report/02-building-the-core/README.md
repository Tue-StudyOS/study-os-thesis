# 02 — Building the Core (Phases 1–3)

**No files live in this folder** — the build history is already well-organized elsewhere and
is linked, not duplicated:
- [MASTERPLAN.md](../../../MASTERPLAN.md) — the stable, structural plan (§1–§7 for
  Phases 1–3; §8 for the Phase 4 hardening track covered in [03](../03-hardening-and-evaluation/README.md)).
- [Design-Entscheidungen.md](../../../Design-Entscheidungen.md) — the detailed "why" behind
  every step of the flow (profile gate, two-pass search, output shape, session persistence).
- [findings/no_db_universal_skill/](../../../findings/no_db_universal_skill/) — the dated,
  task-by-task build log (build plan, per-task decisions, eval results) for every task named
  below.
- `STATUS.md`'s task tables ("Phase 1", "Phase 2 — Company discovery", "Phase 3 —
  Orchestration & Distribution") for the literal done/blocked status of each task.

## Synthesis

Phase 1 (2026-06-26 → 06-27, Tasks A–I) built and proved the university-discovery half of the
skill for one faculty at a time, in a strict dependency order: conversation discipline first
(Task A — one question per turn, so the interview doesn't collapse into a checklist a student
answers shallowly), then the two structural references the whole system depends on — the
**Tübingen faculty backbone** (Task B: official `uni-tuebingen.de` listing URLs for all 7
faculties + the Center for Islamic Theology, used as an anti-SEO-bias anchor) and the
**search-strategy** reference (Task C: how to turn six profile dimensions into precise
queries, plus a two-pass search: Pass 1 crawls the backbone offline for a candidate set,
Pass 2 enriches each candidate live). Only once both references existed did Task D rewrite
`find-university-chairs` to actually use them, faculty-agnostically. Task E then retired the
old scraped-database assets (`match-thesis-advisors`, `update-openalex-paper-index`), moving
the curated CS chair data to eval-only ground truth rather than deleting it outright — the
first concrete instance of "the backbone/curated data is allowed to exist only as an
evaluation baseline, never as a runtime source," a rule that holds throughout the rest of the
project. Tasks F–H built the eval ground truth, wired it into an existing multiturn eval
harness, and ran a first (later found to be **circular**, see [03](../03-hardening-and-evaluation/README.md))
comparison against a scripted baseline.

Phase 2 (2026-06-28, Tasks 2-A–2-E) repeated the same two-pass pattern for **company** thesis
discovery in Baden-Württemberg: a curated backbone of ~107 companies (Cyber Valley industry
partners + manual BW R&D additions), a parallel search-strategy reference, and a live-eval
pass. The company case is structurally harder than the university case — company org
structure is far less standardized than a faculty page, and roughly 80% of companies don't
publicly list thesis openings — which is why the skill was deliberately built to *not* scrape
concrete job postings (fragile, low yield, re-introduces the SEO-bias problem) and instead
outputs a **thesis-signal classification** (`explicit opening` / `active program` / `unclear`)
plus size-aware outreach guidance (careers portal for corporates, direct R&D-team email for
startups) — `unclear` is explicitly documented as a valid result, not a skill failure.

Phase 3 (2026-06-28, Tasks 3-A–3-D) turned the two independent discovery skills into one
product: `thesis-finder` became the single entry point, building the student profile inline
rather than deferring to a separate skill, then routing to university / company / both. It
also added **session persistence** — a `~/.claude/thesis-finder/session.md` file, deliberately
kept outside `references/` (which ships with every release) because it's mutable, user-scoped
runtime state, not bundled content — so a multi-week thesis search doesn't force a student to
re-interview from scratch each time they return. Design-Entscheidungen.md §9 explains the
reasoning in full, including why the returning-user flow asks for only a 1–2 sentence update
rather than repeating the interview (a full re-interview risks corrupting an already-good
profile).

A CI/engineering-hygiene finding from 2026-06-28 is worth naming explicitly here because it's
a genuine lesson, not just a bugfix: the project's "gate GREEN" verdicts up to that point had
only run the eval-harness tests, never the full deterministic `pytest -q` suite — which was
actually **red** (9 failures, broken release build) due to real skill bugs (malformed
reference links) and stale DB-era tests never migrated after the Phase 1 pivot. It was fixed,
but it's the first concrete instance of a recurring theme in this project: a "passing" claim is
only as good as what was actually run to produce it — the same discipline that later drives the
fixture-vs-live distinction in [03](../03-hardening-and-evaluation/README.md).
