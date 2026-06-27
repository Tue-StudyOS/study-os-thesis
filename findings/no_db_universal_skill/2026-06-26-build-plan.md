# No-DB Universal Skill — Exact Build Plan

- **Date:** 2026-06-26
- **Branch:** `feat/no-db-universal-skill` (off `codex/chair-discovery-eval-from-valentin`)
- **Read first:** [2026-06-26-concept-and-risks.md](2026-06-26-concept-and-risks.md) and
  [VISION_NO_DB.md](../../VISION_NO_DB.md)

This plan is written so each task can be handed to a single agent run, in order.
Tasks A→H are sequential where dependencies require it; parallel-safe tasks are
marked. Each task has: **Goal · Depends on · Files · Steps · Done-when · Agent
prompt**.

---

## Target skill flow (after this plan)

```text
raw input ("I like deep learning + healthcare, hate hardware setup")
   |
   v  build-student-profile      interview, ONE question (max 2) per turn -> in-context profile
   v  discover-thesis-options    profile -> search templates -> faculty backbone + live web -> MAP of options
   v  draft-thesis-contact       (optional) first-contact message for a chosen option
```

- **No runtime database. No backend. No scraping pipeline at runtime.**
- The intelligence is the *search-strategy* and *faculty-backbone* references the
  discovery skill carries.
- Bundled chair/prof/paper data becomes **eval-only** ground truth, not a runtime
  source.

---

## Skill inventory: keep / rework / retire

| Skill | Action |
|---|---|
| `build-student-profile` | **Keep + tweak** (Task A: one-question discipline) |
| `find-university-chairs` | **Rework in place** into the universal discovery skill (Task D) |
| `find-recent-papers` | **Keep** as an optional evidence tool |
| `draft-thesis-contact` | **Keep** as the optional final step |
| `generate-thesis-directions` | **Keep but de-emphasize** — we deliver a *map*, not proposals |
| `match-thesis-advisors` | **Retire as runtime** — folds into discovery (Task E) |
| `update-openalex-paper-index` | **Retire** — DB-maintenance, not needed (Task E) |
| `design-agent-skill` | **Keep** (meta-skill) |

---

## Task A — Conversation discipline in `build-student-profile`

- **Goal:** Enforce an ordered interview: one question, max two per turn; instruct
  the user to answer precisely; build the in-context profile before any search.
- **Depends on:** nothing. Parallel-safe.
- **Files:** `skills/build-student-profile/SKILL.md`, optionally
  `skills/build-student-profile/references/deep-advising-interview.md`.
- **Steps:**
  1. In the Workflow, make explicit: ask **one** question per turn (max two when
     tightly related); never a survey batch.
  2. Add an instruction telling the user to answer precisely and concisely.
  3. State that no search/discovery happens until the profile covers interests,
     liked/disliked courses, skills, experience, preferred thesis style, no-gos.
- **Done-when:** SKILL.md explicitly states the one-question rule and the
  precise-answer instruction; no other skill behavior changed.
- **Agent prompt:**
  > Edit `skills/build-student-profile/SKILL.md` so the interview asks exactly one
  > question per turn (at most two only when tightly coupled), instructs the user
  > to answer precisely and concisely, and forbids starting any search before the
  > profile is sufficiently deep. Keep changes surgical — do not restructure the
  > rest of the skill. Verify by re-reading the file.

---

## Task B — Faculty backbone reference (anti-SEO-bias baseline)

- **Goal:** A reference listing the official University of Tübingen faculty /
  institute / chair *listing pages*, so discovery starts from the real
  org structure instead of only Google SEO winners.
- **Depends on:** nothing. Parallel-safe. Needs web access.
- **Files (new):** `skills/find-university-chairs/references/tuebingen-faculty-backbone.md`
- **Steps:**
  1. Enumerate all faculties of Uni Tübingen (e.g. Science, Medicine, Humanities,
     Economics & Social Sciences, Law, Protestant/Catholic Theology).
  2. For each faculty, record the official listing URL(s) that enumerate its
     institutes / departments / chairs (under `uni-tuebingen.de`).
  3. Note for each: language of page, how chairs are listed, last-checked date.
- **Done-when:** every faculty has ≥1 listing URL; spot-check that 3 URLs resolve
  and actually list chairs; dates recorded.
- **Agent prompt:**
  > Create `skills/find-university-chairs/references/tuebingen-faculty-backbone.md`.
  > Using web search/browse, enumerate every faculty of the University of Tübingen
  > and, per faculty, the official `uni-tuebingen.de` page(s) that list its
  > institutes/departments/chairs. Record URL, page language, how chairs are
  > listed, and a last-checked date. Verify 3 URLs resolve. Keep it as a clean,
  > reviewable Markdown table.

---

## Task C — Search-strategy reference (the core IP)

- **Goal:** The reusable instruction set for *how* Claude turns a profile into
  precise queries that find thesis options across any faculty.
- **Depends on:** Task B (references the backbone). Otherwise independent.
- **Files (new):** `skills/find-university-chairs/references/search-strategy.md`
- **Steps:**
  1. Define a mapping: profile dimensions (interests, methods, domain, thesis
     style, no-gos) → query variables.
  2. Provide query skeletons with variable slots, e.g.
     `site:uni-tuebingen.de "{topic}" (Masterarbeit OR Abschlussarbeit)`,
     `"Universität Tübingen" "{faculty}" "{topic}" Forschung`.
  3. Define the two-pass strategy: **(1) backbone crawl** from Task B to get the
     structured chair set per relevant faculty; **(2) live queries** to enrich
     with topics, recent work, openings.
  4. Define quality filters (prefer official pages, date evidence), dedup rules,
     and how no-gos *exclude* results.
  5. Define how the profile maps to the **relevant faculties** (so a psychology
     interest searches the right faculty, not CS).
- **Done-when:** a reviewer can follow the doc by hand to produce a sensible query
  set for two different sample profiles.
- **Agent prompt:**
  > Create `skills/find-university-chairs/references/search-strategy.md`: a reusable
  > instruction set that turns a student profile into precise web queries to find
  > Tübingen thesis options across ALL faculties. Include the profile→query-variable
  > mapping, concrete query skeletons with slots, a two-pass approach (first crawl
  > the faculty backbone in `tuebingen-faculty-backbone.md`, then enrich via live
  > queries), quality/dedup filters, no-go exclusion, and profile→faculty routing.
  > Make it concrete enough that a reviewer can produce queries by hand for two
  > sample profiles.

---

## Task D — Rework `find-university-chairs` into the universal discovery skill

- **Goal:** The core skill. Profile → search-strategy → backbone + live web →
  **map of options** for any faculty. No DB/seed dependency.
- **Depends on:** Task B, Task C.
- **Files:** `skills/find-university-chairs/SKILL.md`; remove runtime use of
  `references/professors/`, `references/chairs/`, `references/researchers/`.
- **Steps:**
  1. Rewrite the workflow to: confirm a deep profile exists (else call
     `build-student-profile`), route to relevant faculties, run the two-pass
     search per `search-strategy.md`, aggregate and map to interest dimensions.
  2. Output = **map of options**: per option (chair/group/person) give relevance
     rationale, **pros/cons & difficulties**, evidence with dates, and a possible
     conversation starter. Group options by interest dimension.
  3. Add the **honest coverage caveat**: "you likely see most publicly visible
     options; search the rest yourself."
  4. Remove the seed-list dependency from the workflow; the old `references/`
     chair/prof/researcher data is no longer a runtime source (handled in Task E).
  5. Update the `description:` so the skill is faculty-agnostic.
- **Done-when:** running the skill on a sample profile with live web tools yields a
  grouped map with pros/cons and the caveat; `grep` shows no runtime read of the
  seed/chair/researcher data; description is faculty-agnostic.
- **Agent prompt:**
  > Rework `skills/find-university-chairs/SKILL.md` into a faculty-agnostic thesis-
  > option discovery skill. It must: require a deep profile (else defer to
  > build-student-profile), route to relevant faculties, execute the two-pass search
  > from `references/search-strategy.md` over `references/tuebingen-faculty-backbone.md`
  > plus live web, and output a MAP of options grouped by interest dimension — each
  > with relevance rationale, pros/cons & difficulties, dated evidence, and a
  > conversation starter — ending with an honest coverage caveat. Remove all runtime
  > dependence on the bundled professor/chair/researcher seed data and update the
  > description to be faculty-agnostic. Verify end-to-end on a sample profile.

---

## Task E — Retire DB-oriented assets

- **Goal:** Remove maintenance-bound runtime assets so the package is truly
  maintenance-free; preserve curated chair/prof data as **eval-only**.
- **Depends on:** Task D (replacement must exist first).
- **Files:** `skills/match-thesis-advisors/`, `skills/update-openalex-paper-index/`,
  `skills/find-university-chairs/references/{professors,chairs,researchers}/`.
- **Steps:**
  1. Retire `match-thesis-advisors` and `update-openalex-paper-index` (delete or
     move under an `archive/` / clearly mark deprecated — recommend delete, since
     git history preserves them).
  2. Move the curated seed/chair/researcher Markdown to an eval location (see Task
     F) — it becomes ground truth, not runtime.
  3. Grep the repo to confirm no remaining runtime skill references the moved data,
     backend, DB, Docker, Celery, or FastAPI.
- **Done-when:** `grep -ri "backend\|database\|celery\|fastapi\|seed list" skills/`
  returns no runtime dependency; the two retired skills are gone from `skills/`.
- **Agent prompt:**
  > Retire the database-bound assets now that `find-university-chairs` is DB-free.
  > Delete `skills/match-thesis-advisors/` and `skills/update-openalex-paper-index/`.
  > Move the curated `professors/`, `chairs/`, `researchers/` Markdown out of the
  > runtime skill into the eval ground-truth location. Then grep `skills/` to prove
  > no runtime skill still depends on a database, backend, seed list, Docker, Celery,
  > or FastAPI. Report what you removed.

---

## Task F — Eval ground-truth sample (3–4 faculties)

- **Goal:** A hand-curated benchmark to measure discovery coverage and to compare
  skill vs. plain Claude.
- **Depends on:** can start in parallel with B–E; needs web for curation.
- **Files (new):** `skills/tests/ground_truth/<faculty>.md` (or `.json`), plus a
  short `skills/tests/ground_truth/README.md` defining the metric.
- **Steps:**
  1. Pick 3–4 faculties spanning diversity (e.g. CS/ML, Psychology, Medicine,
     Linguistics).
  2. Per faculty, manually list the real chairs/professors relevant to a defined
     sample interest (the unit we measure recall against).
  3. Reuse the existing curated CS data (moved in Task E) for the CS faculty.
  4. Define the metric: e.g. **recall = (ground-truth chairs surfaced) / (total
     ground-truth chairs)**; set a target (start at ≥70%).
- **Done-when:** ≥3 faculties each with a curated chair list and a defined sample
  interest; metric + target documented in the README.
- **Agent prompt:**
  > Build an eval ground truth under `skills/tests/ground_truth/`. For 3–4 diverse
  > Tübingen faculties (include CS/ML using the curated data moved in Task E, plus
  > e.g. Psychology, Medicine, Linguistics), manually curate the real chairs/
  > professors relevant to one defined sample interest per faculty. Write a README
  > defining the coverage metric (recall against this ground truth) and a starting
  > target of ≥70%. Verify chair names against official pages.

---

## Task G — Wire discovery into Max's multiturn eval harness

- **Goal:** Run the full profile→discovery flow automatically and compare the
  skill against a plain-Claude baseline.
- **Depends on:** Task D, Task F. Harness source: branch `eval/auto_eval_agents`
  (commit `ed341a7`).
- **Files (port from `eval/auto_eval_agents`):**
  `scripts/run_codex_multiturn_eval.py`, `skills/tests/simulations/**`,
  `skills/tests/test_codex_multiturn_eval.py`,
  `.github/workflows/codex-multiturn-evals.yml`. Add a new scenario for discovery.
- **Steps:**
  1. Cherry-pick / merge the harness files from `eval/auto_eval_agents` into this
     branch.
  2. Add a scenario that drives build-student-profile → discover-thesis-options to
     completion, plus a **baseline arm** = plain Claude with the same persona but
     no skill.
  3. Extend the rubric to score: coverage vs. ground truth (Task F), relevance,
     and structure of the option map.
- **Done-when:** the harness runs both arms (skill, baseline) on at least one
  ground-truth faculty and emits a comparison artifact.
- **Agent prompt:**
  > Port Max's multiturn eval harness from branch `eval/auto_eval_agents` (commit
  > ed341a7) into this branch: `scripts/run_codex_multiturn_eval.py`,
  > `skills/tests/simulations/**`, `skills/tests/test_codex_multiturn_eval.py`, and
  > the workflow. Add a discovery scenario that runs build-student-profile →
  > discover-thesis-options to completion AND a baseline arm using plain Claude
  > (same persona, no skill). Extend the rubric to score coverage against the Task F
  > ground truth, relevance, and option-map structure. Verify it runs both arms on
  > one faculty and writes a comparison artifact.

---

## Task H — Run the eval, measure, document

- **Goal:** Produce the empirical result: how much coverage, and does the skill
  beat plain Claude.
- **Depends on:** Task G.
- **Files (new):** `findings/no_db_universal_skill/<date>-eval-results.md`.
- **Steps:**
  1. Run the harness across the ground-truth faculties.
  2. Record per-faculty coverage and the skill-vs-baseline delta.
  3. State honestly where coverage is weak and why.
- **Done-when:** a findings doc with concrete numbers and the skill-vs-baseline
  comparison.
- **Agent prompt:**
  > Run the multiturn eval across all Task F ground-truth faculties for both arms.
  > Write `findings/no_db_universal_skill/<today>-eval-results.md` with per-faculty
  > coverage numbers, the skill-vs-plain-Claude delta, and an honest note on weak
  > spots. Do not inflate results.

---

## Phase 2 (later) — Company discovery

Out of initial scope. Approach: a **one-time** curated list (e.g. ~companies in
Baden-Württemberg) tagged by area/hashtags, bundled as the one acceptable static
asset (no clean live-search equivalent). New startups are a known later gap. Do
**not** start before the university arm is proven (Task H).

---

## Housekeeping (not an agent task)

- GitHub issues `#45`–`#51` describe the old DB data-foundation epic and are now
  **superseded**. Close them with a pointer to this plan, and open new issues
  matching Tasks A–H.
- The retired backend / web-app stack stays only in git history.
