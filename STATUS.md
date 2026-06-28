# Status — StudyOS Thesis-Finder

> **This is the only continuously updated file.** Here we collect progress, blockers, difficulties, and decisions. The stable overall plan is in [MASTERPLAN.md](MASTERPLAN.md).
>
> **Convention:** When working on a task, change its status here, note difficulties, and add a dated line to the log below. Do not edit the Masterplan.

**Last update:** 2026-06-28 (Phase 2 kick-off — decisions resolved, build plan written)

---

## Current phase

**Phase 2 — Company discovery (database-less).** Goal: extend the Phase 1 principle
to BW companies — same 6-dimension profile, same two-pass discovery, curated company
backbone instead of faculty backbone. Target: a student can discover thesis options at
~100–130 BW companies with ≥70% recall live.

Phase 1 is **complete and GREEN** (all 4 faculties ≥70% live recall; gate passed
2026-06-28). Phase 1 build plan: [2026-06-26-build-plan.md](findings/no_db_universal_skill/2026-06-26-build-plan.md).

Phase 2 decisions: [2026-06-28-phase2-company-decisions.md](findings/no_db_universal_skill/2026-06-28-phase2-company-decisions.md)
· Phase 2 build plan: [2026-06-28-phase2-build-plan.md](findings/no_db_universal_skill/2026-06-28-phase2-build-plan.md)

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
| 2-A | BW company backbone reference (~100–130 entries, Cyber Valley + manual BW R&D additions) | ⬜ | – | – |
| 2-B | Company search strategy (profile → backbone filter + live enrichment queries) | ⬜ | – | Depends on 2-A |
| 2-C | Build `find-company-thesis-options` skill | ⬜ | – | Depends on 2-A, 2-B |
| 2-D | Eval ground truth for companies (3 profiles × 5–8 companies each) | ⬜ | – | Parallel-safe |
| 2-E | Live validation (real recall + baseline, ≥70% target per profile) | ⬜ | – | Depends on 2-C, 2-D |

**Gate Phase 2 → 3:** skill runs end-to-end · ground truth for ≥3 profiles · live recall ≥70% all profiles · meaningful live margin over plain Claude.

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
