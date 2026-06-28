# Status — StudyOS Thesis-Finder

> **This is the only continuously updated file.** Here we collect progress, blockers, difficulties, and decisions. The stable overall plan is in [MASTERPLAN.md](MASTERPLAN.md).
>
> **Convention:** When working on a task, change its status here, note difficulties, and add a dated line to the log below. Do not edit the Masterplan.

**Last update:** 2026-06-28 (CI/engineering-hygiene fix — full pytest suite + release build now GREEN; see latest log entry)

---

## Current phase

**Phase 3 — Orchestration & Distribution: COMPLETE.** Backbone maintenance, entry-point skill,
distribution artifacts, and smoke test are all done. Branch `feat/no-db-universal-skill` is
ready for review/merge.

Phase 1 is **complete and GREEN** (all 4 faculties ≥70% live recall; gate passed
2026-06-28). Phase 1 build plan: [2026-06-26-build-plan.md](findings/no_db_universal_skill/2026-06-26-build-plan.md).

Phase 2 decisions: [2026-06-28-phase2-company-decisions.md](findings/no_db_universal_skill/2026-06-28-phase2-company-decisions.md)
· Phase 2 build plan: [2026-06-28-phase2-build-plan.md](findings/no_db_universal_skill/2026-06-28-phase2-build-plan.md)

Phase 3 build plan: [2026-06-28-phase3-build-plan.md](findings/no_db_universal_skill/2026-06-28-phase3-build-plan.md)
· Phase 3 smoke test: [2026-06-28-phase3-smoke-test.md](findings/no_db_universal_skill/2026-06-28-phase3-smoke-test.md)

---

## Task status

Legend: ⬜ open · 🟨 in progress · ✅ done · ⛔ blocked

| Task | Step | Status | Owner | Notes / difficulties |
|---|---|---|---|---|
| A | Conversation discipline in `build-student-profile` | ✅ | Domi | One-question rule + precise-answer instruction + no-search gate added to SKILL.md. |
| B | Faculty backbone reference (Tübingen listing URLs) | ✅ | Domi | All 7 faculties + ZITh covered; ≥1 official listing URL each, 6 spot-checked live. |
| C | Search-strategy reference (profile → queries) | ✅ | Domi | Created `search-strategy.md`: profile→query-variable mapping, 18 query skeletons, two-pass strategy, quality filters, dedup rules, no-go exclusion, faculty routing table, two worked examples (Ethical AI/Education + Clinical Neuroscience). |
| D | Rework `find-university-chairs` into universal discovery skill | ✅ | Domi | Rewrote SKILL.md: faculty-agnostic description, 6-dimension profile gate, faculty routing via search-strategy.md §2, two-pass search (backbone crawl + live enrichment), quality filters/dedup/no-go exclusion, MAP output grouped by interest dimension with pros/cons, dated evidence, conversation starter, coverage caveat. No seed-list dependency. |
| E | Retire DB assets (match-thesis-advisors, openalex index, seed data → eval) | ✅ | Domi | Deleted match-thesis-advisors + update-openalex-paper-index; moved CS seed data to skills/tests/eval_ground_truth/cs_seed/; fixed seed-path refs in find-recent-papers + design-agent-skill. grep confirms no runtime DB deps remain. |
| F | Eval ground truth for 3–4 faculties + metric | ✅ | Domi | 4 faculties: CS (cs_seed/), Medicine (6 chairs), Psychology (6 chairs), WiSo (7 chairs). README defines recall metric + ≥70% target. |
| G | Wire discovery into Max's multiturn harness (skill vs. baseline) | ✅ | Domi | Harness already existed in branch. Added medicine-discovery scenario (skill + baseline arms), neuro-student persona, scripted fixtures, coverage/relevance/structure scoring, `--discovery-comparison` CLI flag. 12/12 tests pass; fixture run: skill 83% recall vs. 0% baseline. |
| H | Run eval, measure coverage & skill-vs-baseline delta, document | ✅ | Domi | **Fixture-mode only.** Mean skill recall 96%, baseline 0% — but both arms were hand-scripted, so the gap is circular and does NOT validate live behavior. See Task I. |
| I | **Live validation** — real recall + real baseline with live WebSearch | ✅ | Domi | **GREEN (after I-fix).** Initial run AMBER: Psych 67%, CS 60%. Fixed: (1) PI attribution discipline (2e verification step); (2) MPI-IS/ELLIS explicit Pass-1 crawl leg. Re-validated Psych (primary 100%, strict 83%) and CS (primary 100%, strict 100%) live. All 4 faculties ≥70%. Results: `findings/no_db_universal_skill/2026-06-28-I-fix-revalidation.md`. |

**Gate Phase 1 → 2 (REVISED):** skill runs end-to-end with no DB ✅ · ground
truth for ≥3 faculties ✅ · harness plumbing works ✅ · **live** coverage ≥70%
AND a meaningful live margin over plain Claude ✅ **GREEN** (Task I-fix: all 4
faculties ≥70% primary and strict; Psych 100%/83%, CS 100%/100%, Med 100%/83%,
WiSo 100%/100%; real +65pp over baseline confirmed in Task I).

### Phase 2 — Company discovery

| Task | Step | Status | Owner | Notes / difficulties |
|---|---|---|---|---|
| 2-A | BW company backbone reference (~100–130 entries, Cyber Valley + manual BW R&D additions) | ✅ | Domi | 107 entries across 7 sectors; 10 URLs spot-checked live; `bw-company-backbone.md` committed. |
| 2-B | Company search strategy (profile → backbone filter + live enrichment queries) | ✅ | Domi | `company-search-strategy.md`: interest→tag mapping, Pass 1 (backbone filter), Pass 2 (site: enrichment), query skeletons, quality filters, no-go exclusion, 2 worked examples. |
| 2-C | Build `find-company-thesis-options` skill | ✅ | Domi | `SKILL.md`: 8-step workflow, backbone filter → live enrichment, output schema from decisions doc, evidence rules (no invented contacts), no-go guard, coverage caveat required. |
| 2-D | Eval ground truth for companies (3 profiles × 5–8 companies each) | ✅ | Domi | 3 profiles × 5–6 verified companies each; confirmation URLs live-verified; README defines recall + thesis-signal metrics. `company_seed/` committed. |
| 2-E | Live validation (real recall + baseline, ≥70% target per profile) | ✅ | Domi | **GREEN.** 100% recall all 3 profiles (vs 74% baseline mean); +26pp mean delta; 94% thesis-signal accuracy. Caveats: circular recall (GT built from same backbone), weak C1 delta (+17pp), Aleph Alpha stale post-merger. Results: `2026-06-28-phase2-live-eval-results.md`. |

**Gate Phase 2 → 3:** skill runs end-to-end ✅ · ground truth for ≥3 profiles ✅ · live recall ≥70% all profiles ✅ · meaningful live margin over plain Claude ✅ **GREEN** (Task 2-E: all 3 profiles 100%; +26pp mean over baseline; no DB dependency confirmed).

### Phase 3 — Orchestration & Distribution

| Task | Step | Status | Owner | Notes / difficulties |
|---|---|---|---|---|
| 3-A | Backbone maintenance (Aleph Alpha fix + §5 expansion) | ✅ | Domi | Aleph Alpha → Cohere entry updated; §5 expanded to 7 entries (added IONOS, Haufe, GFT, Schwarz IT). |
| 3-B | Create `thesis-finder/SKILL.md` entry point | ✅ | Domi | Thin orchestrator: profile check → track question → routes to find-university-chairs / find-company-thesis-options / both; offers draft-thesis-contact as next step. |
| 3-C | Update `AGENTS.md` + `README.md` for distribution | ✅ | Domi | AGENTS.md: new student workflow, thesis-finder + find-company-thesis-options documented, retired skills annotated. README: student-facing top section (≤200 words) added. |
| 3-D | End-to-end smoke test + STATUS.md update | ✅ | Domi | C1 trace passes all steps; no dead references found. Full trace in `2026-06-28-phase3-smoke-test.md`. |

**Gate Phase 3 (all criteria):**
- Backbone: Aleph Alpha corrected; §5 ≥6 entries ✅
- `thesis-finder/SKILL.md` routes correctly for all three student choices ✅
- `AGENTS.md` reflects current skill set (no retired skills in active workflow) ✅
- `README.md` has student-readable top section ✅
- Smoke test passes with no dead references ✅
- STATUS.md closed with gate verdict ✅

**Overall Phase 3 gate: GREEN.** Branch `feat/no-db-universal-skill` is in a coherent state and ready for review/merge. Post-Phase-3 human actions: hand off to Fachschaft Informatik, Hennig-GitHub, and Ersti-Heft editors (outside scope of this branch).

---

## Open decisions

- **Coverage target:** ≥70% recall — confirmed as the standing target (Task H
  and Task I validated it; same target adopted for Phase 2).
- **Discovery skill name:** `find-university-chairs` stays as-is. Phase 2
  introduces `find-company-thesis-options` as a parallel skill. No rename planned.
  *(resolved 2026-06-28)*
- **Company list source (Phase 2):** Cyber Valley Industry Partners (primary,
  ~80–100 AI/ML entries) + ~20–30 manual BW R&D additions (automotive, medtech,
  software, industrial, energy). Bundled as a tagged Markdown reference file.
  Full rationale: `findings/no_db_universal_skill/2026-06-28-phase2-company-decisions.md`.
  *(resolved 2026-06-28)*

---

## Known difficulties / risks

- **Web-search coverage gaps** — chairs with weak/outdated web presence are
  silently missed. Mitigation: faculty-backbone crawl (Task B) + honest in-output
  caveat.
- **Beating plain Claude** — must be shown empirically, not assumed (Tasks G/H).
- **Profile must actually steer the search** — if the interview doesn't change the
  queries, the skill adds nothing (Tasks C/D).
- **Company discovery is a different, harder problem** — deliberately deferred to
  Phase 2.
- **Personal data (GDPR)** — surfaced researcher names + areas are public academic
  data; nothing student-private is ever stored (profile stays in-context only).

---

## Log

- **2026-06-28** — **CI / engineering-hygiene fix.** Review found the deterministic
  package suite was actually **RED**: `python -m pytest -q` (run by `qa.yml` and
  `package-skills.yml`) reported **9 failures**, and the release artifact could not be
  built. Earlier "gate GREEN" verdicts only ran the eval-harness tests
  (`test_codex_multiturn_eval.py`, 12/12) + a manual smoke trace — the package/release
  tests were never run after the no-DB pivot. Two root causes fixed: (1) **Real skill
  bugs** — `find-university-chairs` (6×) and `find-company-thesis-options` (4×) embedded
  section anchors *inside* the backtick of a `references/…` link
  (`` `references/…md §1` ``), which broke `build_skill_release.py`'s reference validator
  (`BuildError`) and `test_referenced_skill_resources_exist`; moved the ` §N` outside the
  backtick. `thesis-finder` description lacked the `Use when …` trigger; added it.
  (2) **Stale DB-era tests** — `test_skill_package.py` was never migrated from the pre-pivot
  world: `EXPECTED_SKILLS` still listed the deleted `match-thesis-advisors` /
  `update-openalex-paper-index` and omitted `thesis-finder` / `find-company-thesis-options`;
  `test_required_markdown_database_indexes_exist` and the professor-seed-index test asserted
  the very `professors/INDEX.md` the pivot removed; privacy/evidence assertions checked
  pre-Task-A/D wording. Migrated the suite to the no-DB contract (corrected skill set;
  replaced the inverted DB-index tests with `test_discovery_skills_carry_no_runtime_seed_data`,
  which guards that seed dirs stay *out* of the runtime skill; updated the static-acceptance
  fixture to the current build-profile → thesis-finder → discovery → contact/directions flow).
  The CI **architecture** (qa / package-skills / codex-multiturn-evals workflows + the
  release builder) fits the portable-skill product and was kept as-is. Result:
  `pytest -q` → **29 passed, 8 skipped**; `build_skill_release.py` produces tar.gz + zip
  with the correct 8 skills. Files changed: 2 discovery SKILL.md, thesis-finder SKILL.md,
  `test_skill_package.py`.

- **2026-06-28** — Phase 3 **complete — gate GREEN.** (3-A) Backbone updated: Aleph Alpha entry replaced with "Cohere GmbH (formerly Aleph Alpha GmbH) ⚠" plus merger caveat; §5 Software/Enterprise expanded from 3 to 7 entries (added IONOS, Haufe, GFT, Schwarz IT). (3-B) `skills/thesis-finder/SKILL.md` created as thin 4-step orchestrator: profile check → track choice → route to find-university-chairs / find-company-thesis-options / both → offer draft-thesis-contact. (3-C) `AGENTS.md` student workflow updated to current skill set; find-company-thesis-options and thesis-finder fully documented; retired skills (match-thesis-advisors, update-openalex-paper-index) annotated as retired. README.md got a student-facing top section (what it is, how to use it, what it gives, what it doesn't). (3-D) Smoke test traced C1 profile through all 15 steps across both tracks — all PASS; zero dead references. Phase 3 gate: all 6 criteria GREEN. Branch ready for review/merge. Distribution to Fachschaft/Hennig/Ersti-Heft is the next human action. Commits: see git log.

- **2026-06-28** — Phase 2 kick-off **done**. Resolved two open STATUS.md decisions: (1) company
  backbone source → Cyber Valley Industry Partners + ~20–30 manual BW R&D additions, tagged
  Markdown file, ~100–130 entries; (2) output schema → company option map with always-present
  fields (name, sector, size, location, relevance, pros/difficulties, contact path) and
  may-be-missing fields (thesis signal, coordinator name), stronger coverage caveat than uni
  version. Wrote `2026-06-28-phase2-company-decisions.md` and `2026-06-28-phase2-build-plan.md`
  (Tasks 2-A through 2-E with ready-to-paste agent prompts). Discovery skill name decision
  closed: `find-university-chairs` stays as-is, new `find-company-thesis-options` is a parallel
  skill. Phase 2 task table added to STATUS. Commits: `ce04977`, `STATUS update`.

- **2026-06-28** — Task I-fix **done** (two bugs from Task I corrected). (1) Added 2e PI-verification step to SKILL.md Step 5: each named professor must be confirmed on the unit's own staff page before attribution; added §4.6 person-verification query skeletons to search-strategy.md. (2) Added MPI-IS (`is.mpg.de/departments`) and ELLIS/Cyber Valley as first-class Pass-1 sources to SKILL.md Step 4, search-strategy.md §2, and backbone drill-down table. Re-validated Psychology and CS live (no peeking): Psych primary 100%/strict 83%, CS primary 100%/strict 100% — both clear ≥70%. **Phase-1 gate is now GREEN.** Full results: `findings/no_db_universal_skill/2026-06-28-I-fix-revalidation.md`. Commit: `c1cc302`.

- **2026-06-28** — Task 2-D + 2-E **done**. (2-D) Built `skills/tests/eval_ground_truth/company_seed/`: 3 profiles (C1 ML/automotive, C2 medtech, C3 software/enterprise) × 5–6 verified companies each; confirmation URLs verified live; README defines recall + thesis-signal metrics. (2-E) Live validation GREEN: 100% recall on all 3 profiles vs 74% baseline mean (+26pp delta); thesis-signal accuracy 94% (1 TeamViewer over-classification). Key caveats: circular recall (GT/backbone share the same source), weak C1 delta (+17pp, baseline already knows Bosch/ZF/Mercedes), Aleph Alpha backbone entry stale post-April-2026-merger. Full results: `findings/no_db_universal_skill/2026-06-28-phase2-live-eval-results.md`. **Phase-2 gate: GREEN.** Phase 3 (distribution/orchestration planning) is the next step. Commits: `9f03e8f`, `a0ddf16`, `15e8d02`.

- **2026-06-28** — Task I (live validation) **run**. Built one persona per faculty
  from the *sample interest* only, then ran the discovery skill end-to-end with live
  `WebSearch`/`WebFetch` (skill arm) and a clean no-skill prompt (baseline arm) for
  medicine, psychology, wiso, cs — **all 8 arm outputs written before opening any
  ground-truth chair list** (no peeking; artifacts in `dist/live-validation/`).
  **Results:** primary recall (README name-surfacing) mean **~82%** skill vs **~17%**
  real baseline (+65pp); per-faculty Med 100%, WiSo 100%, Psych 67%, CS 60%. Strict
  person-level recall mean **~65%** (Psych only 17%). Real baseline is **not 0%** —
  plain Claude names Ziemann/Schlumberger/Abels/Hein — so the fixture's 96%-vs-0% was
  doubly optimistic. Honest defects: (1) Psychology PI **misattribution** — named
  Karnath for "Diagnostik und Kognitive Neuropsychologie" when it's **Hans-Christoph
  Nürk**; (2) CS **under-crawls MPI-IS** — missed Schölkopf (Empirical Inference) and
  Martius (Autonomous Learning). Profile steering visibly works (demoted oncology /
  IR / globalization-ethics correctly). **Verdict: AMBER** — aggregate gate met and
  the skill genuinely beats plain Claude, but Psych & CS miss 70% and need two skill
  fixes (person-attribution discipline; explicit MPI-IS/ELLIS crawl leg) before the
  gate turns green. Full writeup:
  `findings/no_db_universal_skill/2026-06-28-live-eval-results.md`.

- **2026-06-28** — Reassessed Task H. The eval ran in fixture mode only: the
  skill-arm conversations were hand-authored with the ground-truth names already
  in them, and the baseline arm was a scripted strawman (its "0%" run actually
  gave reasonable advice, e.g. naming the HIH). The 96%-vs-0% gap is therefore
  circular and does not validate live skill behaviour or a real advantage over
  plain Claude. Revised the Phase 1→2 gate to require a **live** measurement.
  Opened Task I (live validation) with a no-peeking protocol at
  `findings/no_db_universal_skill/2026-06-28-live-validation-protocol.md`.
  Decision: do Task I before Phase 2 (companies), so we don't build on an
  unvalidated university arm.

- **2026-06-27** — Task H done. Created fixture pairs for psychology (6 chairs), WiSo (7 chairs),
  and CS/ML (7 researchers) using scripted conversations. Extended the runner with
  PSYCHOLOGY_, WISO_, CS_GROUND_TRUTH constants, FACULTY_CONFIGS dict, score_structure()
  optional ground_truth param (backward-compatible), _run_single_faculty_comparison(),
  run_all_faculties_comparison(), and --discovery-comparison now runs all 4 faculties.
  12/12 tests still pass. Results: medicine 83% (5/6), psychology 100% (6/6),
  wiso 100% (7/7), cs 100% (7/7); baseline 0% all faculties; mean 96%. All four
  meet ≥70% target. One honest miss: Tabatabai (medicine, neurooncology — appropriate
  given neurodegeneration persona). Findings in
  findings/no_db_universal_skill/2026-06-27-eval-results.md.
  Phase 1 gate criteria met: no-DB, 4 ground-truth faculties, harness compares skill vs.
  baseline, recall ≥70%. Ready for Phase 2.

- **2026-06-27** — Task G done. Ported (already present) harness and extended it for discovery eval:
  Added `neuro-student` persona (Neurowissenschaften MSc, Parkinson's/Alzheimer's interest);
  `medicine-discovery-skill` and `medicine-discovery-baseline` scenarios; scripted fixture
  conversations for both arms; extended rubric with `discovery_coverage`, `discovery_relevance`,
  `discovery_structure` metrics; added `score_coverage()`, `score_relevance()`, `score_structure()`,
  `run_discovery_comparison()`, `--discovery-comparison` CLI flag to the runner.
  5 new tests added (12/12 total pass). First fixture run: skill arm 83% recall (5/6 HIH chairs),
  baseline 0% recall — gap +83pp. Comparison artifact written to
  `dist/codex-multiturn-evals/discovery-comparison/comparison.md`.
  Note: harness fixture mode requires no Codex/API; live Codex runs need `--runner codex-*`.

- **2026-06-27** — Task F done. Created eval ground truth for 4 faculties under
  `skills/tests/eval_ground_truth/`: Medicine (6 Hertie Institute professors, sample
  interest: neurodegenerative diseases + clinical brain research), Psychology (6
  Fachbereich Psychologie chairs, sample interest: cognitive neuroscience + decision-
  making), WiSo (7 chairs across Politikwissenschaft + Wirtschaftswissenschaft, sample
  interest: comparative politics + political economy). CS already covered by cs_seed/.
  Wrote README.md defining the recall metric: recall = surfaced / total ground-truth
  chairs, ≥70% target, step-by-step scoring guide, and what counts as "surfaced".
  All names verified against official uni-tuebingen.de and hih-tuebingen.de pages on
  2026-06-27. Four commits (one per faculty file + one for README).

- **2026-06-27** — Task E done. Deleted `skills/match-thesis-advisors/` and
  `skills/update-openalex-paper-index/` (4 files; git history preserves them).
  Moved curated CS seed data (professors/, chairs/, researchers/) from
  `skills/find-university-chairs/references/` to
  `skills/tests/eval_ground_truth/cs_seed/` — now eval-only ground truth for
  Task F. Fixed two stale runtime references: `find-recent-papers/SKILL.md`
  (dead path to professors/INDEX.md) and `design-agent-skill/SKILL.md`
  (references to retired skills + seed-index-as-runtime-source).
  Final `grep -ri "backend|database|celery|fastapi|seed list" skills/` shows
  only prohibition statements, negations, and test files — no runtime deps.

- **2026-06-27** — Task D done. Rewrote `skills/find-university-chairs/SKILL.md` into a
  faculty-agnostic thesis-option discovery skill. Key changes: (1) description updated
  to cover all disciplines; (2) hard profile gate — all 6 dimensions required, else
  defers to build-student-profile; (3) faculty routing via search-strategy.md §2;
  (4) Pass 1 backbone crawl via tuebingen-faculty-backbone.md; (5) Pass 2 live
  enrichment using query skeletons from search-strategy.md §3–4; (6) quality filters,
  dedup rules, no-go exclusion (§5–7); (7) MAP output grouped by interest dimension
  with pros/cons, dated evidence, conversation starter, no-go flags; (8) honest
  coverage caveat; (9) all runtime references to seed files removed.

- **2026-06-27** — Task C done. Created
  `skills/find-university-chairs/references/search-strategy.md`: a reusable
  instruction set that turns a student profile into precise queries for all
  Tübingen faculties. Contains: (1) profile dimension → query variable mapping
  (interests/methods/domain/thesis-style/skills/no-gos); (2) faculty routing
  table (18 interest rows → primary + secondary faculty); (3) two-pass strategy
  (Pass 1: backbone crawl via `tuebingen-faculty-backbone.md` to get structured
  chair set; Pass 2: live enrichment for relevance, recency, openings); (4) 18
  query skeleton templates in 5 categories; (5) quality filters (source authority,
  date evidence, specificity); (6) dedup rules; (7) no-go exclusion table with
  detection signals; (8) required output structure; (9) two worked examples
  (Ethical AI/Education, Clinical Neuroscience) that can be followed by hand.

- **2026-06-27** — Task B done. Created
  `skills/find-university-chairs/references/tuebingen-faculty-backbone.md`: a
  reviewable table of all 7 Tübingen faculties + the Center for Islamic Theology,
  each with ≥1 official `uni-tuebingen.de` listing URL (Medicine on
  `medizin.uni-tuebingen.de`), page language, how chairs are listed, and a
  2026-06-27 last-checked date. Documented the two/three-level
  faculty→Fachbereich→chair nesting and per-department drill-down pattern. Spot-checked
  6 URLs live (faculties index, science & humanities Fachbereiche, WiSo Fächer, law
  Lehrstühle, Protestant-theology Lehrstühle) — all resolve and list real units.

- **2026-06-27** — Task A done. Edited `skills/build-student-profile/SKILL.md`: added one-question-per-turn rule, precise-answer instruction, and no-search gate (all six profile dimensions required before discovery). Surgical changes only; no other behavior modified.

- **2026-06-26** — Pivoted to the database-less, university-wide direction.
  Created branch `feat/no-db-universal-skill` off
  `codex/chair-discovery-eval-from-valentin`. Wrote
  [VISION_NO_DB.md](VISION_NO_DB.md) and the findings set under
  `findings/no_db_universal_skill/` (concept-and-risks, exact build plan).
  Rewrote MASTERPLAN around Phase 1 = university discovery (Tasks A–H) and reset
  this STATUS. Located Max's multiturn eval harness on branch
  `eval/auto_eval_agents` (commit `ed341a7`) for the skill-vs-baseline comparison.
  Old DB data-foundation epic (issues #45–#51) is superseded; to be closed and
  replaced by issues mirroring Tasks A–H.

---

## Archived: former DB data-foundation phase (superseded 2026-06-26)

The previous Phase 1 built a scraped researcher tree (Prof → PhD → Paper) for CS
Tübingen with monthly refresh automation (issues #45–#51). It is superseded by the
database-less direction. The curated 3-pilot-chair ground truth and CS chair data
are retained as **eval-only** material (Task F). History remains in git.
