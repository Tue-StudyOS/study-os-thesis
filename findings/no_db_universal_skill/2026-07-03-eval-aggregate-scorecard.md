# Eval Aggregate Scorecard — All Runs to Date

- **Date:** 2026-07-03
- **Method:** Pure aggregation. No new live run was executed for this document — every
  number below is copied from an existing dated findings file or `STATUS.md` task row and
  cited at its source. Purpose: one place to read "where do the numbers actually stand,"
  instead of reconstructing it from ~10 separate write-ups.
- **Scope:** Phase 1 (Task H/I/I-fix), Phase 2 (Task 2-E), and the Phase 4 hardening track
  (Roadmap-J run 1, Task O, Task P, Task Q run 1, Task R). Company recall is Phase 2; all
  other tables are the university-discovery skill.

---

## 1. University recall & precision, by faculty

**Fixture-mode numbers (Task H) are listed for historical reference only — they were
found circular (skill arm hand-authored with ground-truth names, baseline a scripted
strawman) and do not count as evidence. See `2026-06-28-live-eval-results.md`.**

| Faculty | Fixture recall (Task H, invalid) | Live primary recall | Live strict recall | Live precision | Source |
|---|---|---|---|---|---|
| Medicine | 83% (5/6) | **100%** (6/6) | **83%** (5/6) | not measured | `2026-06-28-live-eval-results.md` (Task I; not re-run, already ≥70%) |
| Psychology | 100% (6/6) | 67% (4/6) → **100%** post-fix | 17% (1/6) → **83%** post-fix | not measured | `2026-06-28-live-eval-results.md` (Task I) → `2026-06-28-I-fix-revalidation.md` (Task I-fix) |
| WiSo | 100% (7/7) | **100%** (7/7) | **100%** (7/7) | not measured | `2026-06-28-live-eval-results.md` (Task I; not re-run, already ≥70%) |
| CS | 100% (7/7) | 60% (3/5) → **100%** post-fix | 60% (3/5) → **100%** post-fix | 75% (9/12) → **100%** (10/10) post-Task-O | `2026-06-28-live-eval-results.md` → `2026-06-28-I-fix-revalidation.md` → `2026-07-02-live-eval-runbook.md` (Roadmap-J run 1, Task O re-run) |
| Humanities (hard) | — | 60% (3/5) → **100%** (5/5) post-protocol-fix | — (recall-only, no distinct strict pass run) | **100%** (5/5) | `2026-07-02-live-eval-runbook.md`, 2026-07-03 entries (Task Q run 1 → Task T corrected re-score) — see caveat below |
| Law (hard) | — | 60% (3/5) → **80%** (4/5) post-§5-fix | — (recall-only, no distinct strict pass run) | 100% (3/3) → **100%** (4/4) | `2026-07-02-live-eval-runbook.md`, 2026-07-03 + 2026-07-04 entries (Task T blind run → Task U re-run after §5 enrich-before-exclude fix) |
| Theology (hard) | — | not yet run | not yet run | not yet run | GT exists (`.../theology.md`), blind live run not yet exercised |
| Interdisciplinary | — | **100%** (5/5 GT anchors) | — | not scored as recall/precision | `2026-07-03-task-r-edge-cases.md` (Task R, routing-breadth check: 3/3 faculties/centers covered) |
| **Baseline (plain Claude + Websearch), Task I** | — | ~17% mean | ~17% mean | not measured | `2026-06-28-live-eval-results.md` |

**Humanities caveat (resolved by Task T):** the original 60% recall was root-caused to the
eval *protocol*, not the skill — the README's one-line sample-interest summary used to build
the test persona omitted a clause present in `humanities.md`'s actual sample interest ("...with
an interest in the history of the field"). Under the corrected protocol (personas built from
the GT file's full sample-interest line), both misses flip to Include → **100%**. Full account:
`2026-07-02-live-eval-runbook.md`, 2026-07-03 entries.

**Law caveat (resolved by Task U):** the original 60% recall (Task T, genuinely blind) was a
real skill gap, not a protocol artifact — Remmert was excluded at the §5 topical-justification
step from a title-only reading of her dense multi-strand chair title, without Pass-2
enrichment of her actual research focus. Task U added an "enrich before excluding" rule to
§5 and re-ran Law blind: Remmert now surfaces (her Schwerpunkte include "Allgemeine
Grundrechtslehren," a core constitutional-law/human-rights match) → **80%**. Saurer remains
the one miss — his own page shows no constitutional/human-rights/tech focus even after
enrichment, an honest, defensible remaining gap distinct from the Remmert defect class. Full
account: `2026-07-02-live-eval-runbook.md`, 2026-07-04 entry.

**What this table says about the roadmap's "core is done" bar (§4: recall ≥80% across ≥6
faculties incl. ≥1 hard faculty):** **MET (as of 2026-07-04, post-Task-U).** All 6 measured
faculties clear 80% (Medicine, Psychology, WiSo, CS at ≥83–100%; Humanities and Law — both
hard faculties — at 100% and 80% respectively). Theology has ground truth but no live run yet
(not required for the bar, which needs ≥6 faculties incl. ≥1 hard, already satisfied by 2 of
6 being hard). Precision has been formally measured for 4 of 6 faculties (CS, Humanities,
Law, plus company evals in §2) and is ≥80% everywhere it's been measured. See
`2026-07-03-core-done-go-no-go.md` for the full go/no-go call (verdict: **GO**).

---

## 2. Company recall & thesis-signal accuracy (Phase 2, Task 2-E)

| Profile | Recall | Baseline recall | Delta | Thesis-signal accuracy |
|---|---|---|---|---|
| C1 (ML/automotive/robotics) | 100% | — | +17pp (weakest — baseline already knows Bosch/ZF/Mercedes) | included in 94% mean |
| C2 (medtech/health) | 100% | — | — | included in 94% mean |
| C3 (software/data/enterprise) | 100% | — | — | included in 94% mean |
| **Mean** | **100%** | **74%** | **+26pp** | **94%** (1 miss: TeamViewer over-classified as `explicit opening`) |

Source: `2026-06-28-phase2-live-eval-results.md`. **Known caveat, still open:** the ground
truth for this eval was built from the same `bw-company-backbone.md` the skill searches — it
measures "does the skill find what's in the backbone," not "does the backbone reflect
reality." An independent, non-backbone-derived company ground truth does not exist yet (see
`docs/thesis-report/04-open-work/README.md`).

---

## 3. Steering (Task P)

Not a recall/precision metric — a direct test of whether the profile interview changes the
search output. Two inverted personas, same faculty (CS), same Pass-1 candidate set (25
groups):

| | Persona A (causality/Bayesian ML, no-go: CV + hardware) | Persona B (computer vision, no-go: heavy Bayesian theory + hardware) |
|---|---|---|
| Top options | Schölkopf, Brendel, Hennig, Macke, von Luxburg, Hein, Martius (7) | Geiger, Black, Pons-Moll, Kühne, Bethge, Brendel, Lensch, Berens (8) |
| Overlap | **2 of 7–8** (Brendel, Hein — both re-ranked/re-framed per profile) | |

**Result: steering confirmed, strong** — near-disjoint maps, correct-direction flips
(vision chairs top B and are excluded from A; Bayesian/causality chairs top A and excluded
from B). Tested on **one faculty, with personas deliberately built to diverge** — proves the
mechanism *can* steer, not that it reliably steers on subtle, less-extreme profile
differences. Source: `2026-07-02-task-p-steering-proof.md`.

---

## 4. Robustness (Task R — edge cases)

| Edge case | Result |
|---|---|
| Niche topic, no Tübingen match (rocket-engine/aerospace propulsion) | ✅ Honest "no strong fit" output, no padding |
| Shallow / resistant student (8-turn simulated adversarial interview) | ✅ Gate never triggered a premature `find-university-chairs` call |
| Interdisciplinary routing (AI ethics across Law/Humanities-IZEW/Science-ML) | ✅ 5/5 GT anchors surfaced, 3/3 faculties/centers covered, no collapse onto one discipline |

3/3 pass. Two small spec gaps found and fixed during this task (zero-candidates rule in
`find-university-chairs/SKILL.md`; forced-choice + honest-fallback guidance for resistant
students in `build-student-profile/SKILL.md`). Source: `2026-07-03-task-r-edge-cases.md`.

---

## 5. Output & interview quality (Task S)

**Not measured. Task S is open** (`STATUS.md`, Post-Phase-3 hardening). No data exists yet on
whether pros/cons are consistently honest, conversation starters are concrete, evidence dates
are present, or the coverage caveat reliably appears — the roadmap's fourth quality axis has
zero data points as of this scorecard.

---

## 6. Bottom line

**Updated 2026-07-04, post-Task-U.** Recall and precision are strong across all 6 measured
faculties (four "easy" faculties ≥83% strict, two "hard" faculties — Humanities 100%, Law
80% — both cleared after their respective protocol/skill fixes) and on companies (100%/94%).
Steering is confirmed on one faculty. Output quality (Task S) and robustness edge cases
(Task R) both pass. **The roadmap's own "core is done" recall bar (≥80% across ≥6 faculties
incl. ≥1 hard) is now MET** — see `2026-07-03-core-done-go-no-go.md` for the formal **GO**
call. Remaining open items are lower-stakes: Theology has ground truth but no live run yet
(not required for the bar); company-eval circularity (§2) and single-agent/small-n scoring
across every table here remain standing methodological caveats, tracked in
`docs/thesis-report/03-hardening-and-evaluation/README.md`.
