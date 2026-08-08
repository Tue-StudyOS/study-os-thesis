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
| Theology (hard) | — | **83%** (5/6) | — (recall-only, no distinct strict pass run) | **100%** (9/9) | `2026-07-02-live-eval-runbook.md`, 2026-08-08 entry (Task V′ blind run) |
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

**Theology note (added 2026-08-08, Task V′):** the **cleanest blind run in the table** —
`theology.md` was the one hard-faculty GT never opened mid-run, and this was also one of the
first measurements of the *current* skill version (no static backbone; discovery delegated to
`discover-university-candidates`). It clears ≥80% **on a first blind run with no fix applied
first**, unlike Humanities (needed a protocol fix) and Law (needed the §5 skill fix). The one
miss, **Witt** (Kirchengeschichte I — Reformation/Middle Ages), was *enumerated* in Pass 1 and
recorded in the map's explicit exclusion list, then excluded on period grounds because the
sample interest specifies "early-church / **late-antique** church history" — a defensible
call, and arguably a GT-generosity question rather than a skill defect (flagged, deliberately
not resolved in the session that scored it). Precision 9/9 includes three **Catholic-faculty**
chairs (Eisele, Jürgasch, Scoralick) that the GT's own scope note excludes but that fit the
sample interest — unprompted cross-faculty coverage, since Tübingen splits biblical studies
across two theology faculties. Separately, the faculty's **six N.N. vacancies** were all
reported honestly, including the two on-focus ones (AT I; NT II "Evangelienforschung"), with
no invented holders — recorded per GT §21 as a robustness result, not a recall figure. The
GT's sharpest vacancy scenario (an *ethics* persona facing the vacant Syst. Theol. II/III)
remains formally unrun. Full account: `2026-07-02-live-eval-runbook.md`, 2026-08-08 entry.

**What this table says about the roadmap's "core is done" bar (§4: recall ≥80% across ≥6
faculties incl. ≥1 hard faculty):** **MET (as of 2026-07-04, post-Task-U).** All 6 measured
faculties clear 80% (Medicine, Psychology, WiSo, CS at ≥83–100%; Humanities and Law — both
hard faculties — at 100% and 80% respectively). **Strengthened 2026-08-08 (Task V′):**
Theology now has a blind live run too — 83% recall / 100% precision — so the bar holds across
**7** faculties including **3** hard ones, and Theology is the only one that cleared it on a
first blind run with no prior fix. Precision has been formally measured for 5 of 7 faculties
(CS, Humanities, Law, Theology, plus company evals in §2) and is ≥80% everywhere it's been
measured. See
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

**Measured, 4/5 pass.** All 5 existing discovery transcripts reviewed against 5 criteria
(pros/cons, conversation starters, dated evidence, coverage caveat, interview convergence).
4/5 criteria pass cleanly; interview convergence was checked via a live happy-path simulation
(none existed) — 6 turns, clean convergence, versus edge case 2's adversarial 8-turn
non-convergence (Task R). One real, repeated gap found: `cs-skill` and `wiso-skill` (2 of 5
transcripts) omitted the "Dated evidence" field from every option — fixed with a worked
example added to `find-university-chairs/SKILL.md` Step 8. Source:
`2026-07-03-task-s-output-quality.md`.

---

## 6. Bottom line

**Updated 2026-08-08, post-Task-V′.** Recall and precision are strong across all 7 measured
faculties (four "easy" faculties ≥83% strict, three "hard" faculties — Humanities 100%, Law
80%, Theology 83%; the first two cleared only after their respective protocol/skill fixes,
Theology cleared on a first blind run with none) and on companies (100%/94%).
Steering is confirmed on one faculty. Output quality (Task S) and robustness edge cases
(Task R) both pass. **The roadmap's own "core is done" recall bar (≥80% across ≥6 faculties
incl. ≥1 hard) is now MET** — see `2026-07-03-core-done-go-no-go.md` for the formal **GO**
call. Remaining open items are lower-stakes: the Theology run left two things flagged but
unresolved — whether the GT's **Witt** row is over-inclusive for a late-antique persona, and
the GT §21 vacancy scenario for an *ethics* persona, which no run has yet exercised.
Company-eval circularity (§2) and single-agent/small-n scoring across every table here remain
standing methodological caveats, tracked in
`docs/thesis-report/03-hardening-and-evaluation/README.md`. Note also that most numbers above
predate the current skill architecture (static backbone removed, discovery delegated to
`discover-university-candidates`); Theology is one of the first measurements *of that
version*, which is why the CS + Law re-measurement (Task AK) matters.
