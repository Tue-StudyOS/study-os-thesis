# Eval Aggregate Scorecard — All Runs to Date

- **Date:** 2026-07-03
- **Method:** Pure aggregation. No new live run was executed for this document — every
  number below is copied from an existing dated findings file or `STATUS.md` task row and
  cited at its source. Purpose: one place to read "where do the numbers actually stand,"
  instead of reconstructing it from ~10 separate write-ups.
- **Scope:** Phase 1 (Task H/I/I-fix), Phase 2 (Task 2-E), and the Phase 4 hardening track
  (Roadmap-J run 1, Task O, Task P, Task Q run 1, Task R). Company recall is Phase 2; all
  other tables are the university-discovery skill.
- **Architecture labelling added 2026-08-09 (Task AJ).** See the standing note directly below;
  every number in this document now carries the architecture and date that produced it.

---

## 0. Standing note — the 2026-07-31 architecture pivot and what it does to these numbers

**Read this before citing any figure in this document.**

On **2026-07-31** the project removed the static backbone architecture: the curated chair and
company catalogs the skills used to search against are gone, and discovery is now delegated
to rules the agent applies live (`discover-university-candidates`). The rationale recorded on
2026-07-30 was that a database-free design better matches the maintenance-free product goal.

The consequence for evidence is blunt: **almost every hard number this project owns was
produced by an architecture that no longer ships.** Each figure below is therefore tagged:

- **`[backbone-crawl, ≤2026-07-30]`** — measured against the deleted architecture. The number
  is real and was honestly obtained; it does **not** describe what a user installs today.
- **`[rules-only, ≥2026-07-31]`** — measured against the shipping architecture.

As of 2026-08-09 exactly one faculty figure carries the second tag (Theology, Task V′), which
is why the CS + Law re-measurement (Task AK) and the committed simulation evidence set
(Task AL) are the open items that matter most.

Two things this labelling deliberately does **not** do. It does not delete the old numbers —
they remain the honest record of the architecture that produced them, and the pivot itself is
part of the project's evolution story. And it does not present the two instruments as one
series: the pre-pivot figures are recall against curated ground truth, the post-pivot
simulation evidence is a 0–3 rubric on conversation quality. *"20.0 → 20.75"* cannot answer
*"does rules-only still find Remmert."* They answer different questions and must never be
plotted together.

Full reasoning: [the final 1.0 plan](2026-08-08-final-1.0-plan.md), §2 "The evidence break".

---

## 1. University recall & precision, by faculty

**Fixture-mode numbers (Task H) are listed for historical reference only — they were
found circular (skill arm hand-authored with ground-truth names, baseline a scripted
strawman) and do not count as evidence. See `2026-06-28-live-eval-results.md`.**

| Faculty | Architecture | Fixture recall (Task H, invalid) | Live primary recall | Live strict recall | Live precision | Source |
|---|---|---|---|---|---|---|
| Medicine | `[backbone-crawl, ≤2026-07-30]` | 83% (5/6) | **100%** (6/6) | **83%** (5/6) | not measured | `2026-06-28-live-eval-results.md` (Task I; not re-run, already ≥70%) |
| Psychology | `[backbone-crawl, ≤2026-07-30]` | 100% (6/6) | 67% (4/6) → **100%** post-fix | 17% (1/6) → **83%** post-fix | not measured | `2026-06-28-live-eval-results.md` (Task I) → `2026-06-28-I-fix-revalidation.md` (Task I-fix) |
| WiSo | `[backbone-crawl, ≤2026-07-30]` | 100% (7/7) | **100%** (7/7) | **100%** (7/7) | not measured | `2026-06-28-live-eval-results.md` (Task I; not re-run, already ≥70%) |
| CS | `[backbone-crawl, ≤2026-07-30]` | 100% (7/7) | 60% (3/5) → **100%** post-fix | 60% (3/5) → **100%** post-fix | 75% (9/12) → **100%** (10/10) post-Task-O | `2026-06-28-live-eval-results.md` → `2026-06-28-I-fix-revalidation.md` → `2026-07-02-live-eval-runbook.md` (Roadmap-J run 1, Task O re-run) |
| Humanities (hard) | `[backbone-crawl, ≤2026-07-30]` | — | 60% (3/5) → **100%** (5/5) post-protocol-fix | — (recall-only, no distinct strict pass run) | **100%** (5/5) | `2026-07-02-live-eval-runbook.md`, 2026-07-03 entries (Task Q run 1 → Task T corrected re-score) — see caveat below |
| Law (hard) | `[backbone-crawl, ≤2026-07-30]` | — | 60% (3/5) → **80%** (4/5) post-§5-fix | — (recall-only, no distinct strict pass run) | 100% (3/3) → **100%** (4/4) | `2026-07-02-live-eval-runbook.md`, 2026-07-03 + 2026-07-04 entries (Task T blind run → Task U re-run after §5 enrich-before-exclude fix) |
| **Theology (hard)** | **`[rules-only, ≥2026-07-31]`** | — | **83%** (5/6) | — (recall-only, no distinct strict pass run) | **100%** (9/9) | **[full results doc](2026-08-08-theology-blind-run.md)** (Task V′ blind run) |
| Interdisciplinary | `[backbone-crawl, ≤2026-07-30]` | — | **100%** (5/5 GT anchors) | — | not scored as recall/precision | `2026-07-03-task-r-edge-cases.md` (Task R, routing-breadth check: 3/3 faculties/centers covered) |
| **Baseline (plain Claude + Websearch), Task I** | measured 2026-06-28; the baseline arm is architecture-independent by construction (no skills loaded), but it is only a valid comparator for the `[backbone-crawl, ≤2026-07-30]` rows it was run against | — | ~17% mean | ~17% mean | not measured | `2026-06-28-live-eval-results.md` |

**Seven of the eight faculty rows above are `[backbone-crawl, ≤2026-07-30]`.** Theology is the
only faculty figure measured against the architecture that currently ships. That imbalance is
the reason Task AK exists.

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

**Theology note (added 2026-08-08, Task V′)** — full account:
**[`2026-08-08-theology-blind-run.md`](2026-08-08-theology-blind-run.md)**. Summary: the
**cleanest blind run in the table** —
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
faculties incl. ≥1 hard faculty):** **declared MET on 2026-07-04 (post-Task-U), and that
verdict stands as dated — but it is provisional on two counts.** All 6 faculties measured at
the time cleared 80% (Medicine, Psychology, WiSo, CS at ≥83–100%; Humanities and Law — both
hard faculties — at 100% and 80% respectively). **Strengthened 2026-08-08 (Task V′):**
Theology now has a blind live run too — 83% recall / 100% precision — so the bar holds across
**7** faculties including **3** hard ones, and Theology is the only one that cleared it on a
first blind run with no prior fix. Precision has been formally measured for 5 of 7 faculties
(CS, Humanities, Law, Theology, plus company evals in §2) and is ≥80% everywhere it's been
measured.

> **The GO is provisional on two counts — both recorded, neither retracted:**
>
> 1. **The blindness gap (flagged 2026-07-05).** Humanities' 100% is a re-score by a session
>    explicitly un-blind on that faculty, and Law's 80% re-run's session had already read the
>    document naming the missed chair and the fix that flips her. Every *genuinely* blind
>    hard-faculty run before Task V′ (Humanities 60%, Law 60%) landed below the bar.
> 2. **The architecture it certified no longer ships (added 2026-08-09, Task AJ).** Six of the
>    seven faculties in this table are `[backbone-crawl, ≤2026-07-30]`. The GO certified a
>    system that was removed on 2026-07-31. Theology is the single faculty for which the bar
>    has been demonstrated on the shipping architecture.
>
> Task V′ resolves count 1 for one hard faculty. Task AK is what would begin to resolve
> count 2. Until then the honest reading is: **the bar was met by the old architecture, and
> has been shown once on the new one.**

See `2026-07-03-core-done-go-no-go.md` for the full go/no-go call (verdict as recorded on
2026-07-04: **GO**, now carrying both caveats above).

---

## 2. Company recall & thesis-signal accuracy (Phase 2, Task 2-E) — `[backbone-crawl, ≤2026-07-30]`

> **⚠️ Permanently demoted 2026-08-09 (Task AJ). Do not cite these figures as evidence of
> discovery quality.** The demotion the 2026-07-05 independent review already named is now
> applied in place: this eval is a **plumbing check** — it shows the skill can read and route
> against its input — and it is **circular by construction**, because its ground truth was
> built from the same `bw-company-backbone.md` the skill searched. It therefore measures
> "does the skill find what's in the backbone," never "does the backbone reflect reality."
>
> **A third defect now sits on top of the first two: that backbone was deleted on 2026-07-31.**
> The eval measures a file that no longer exists, against a ground truth derived from it, using
> an architecture that no longer ships. It is triply invalid as a quality claim.
>
> **This closes old Task Y permanently. No new company ground truth will be built** — the cost
> of an independent, non-backbone-derived company GT is not justified for a component whose
> discovery is now rules-only and covered by the same live-verification requirement as the
> university arm. The numbers stay in the record as history; they carry no weight.

| Profile | Recall | Baseline recall | Delta | Thesis-signal accuracy |
|---|---|---|---|---|
| C1 (ML/automotive/robotics) | 100% | — | +17pp (weakest — baseline already knows Bosch/ZF/Mercedes) | included in 94% mean |
| C2 (medtech/health) | 100% | — | — | included in 94% mean |
| C3 (software/data/enterprise) | 100% | — | — | included in 94% mean |
| **Mean** | **100%** | **74%** | **+26pp** | **94%** (1 miss: TeamViewer over-classified as `explicit opening`) |

Source: `2026-06-28-phase2-live-eval-results.md`. The circularity caveat that used to sit here
as "known, still open" is no longer open — it is settled as a permanent demotion in the box
above, and old Task Y is closed with it.

---

## 3. Steering (Task P) — `[backbone-crawl, ≤2026-07-30]`

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

**Post-pivot status (added 2026-08-09, Task AJ):** of all the pre-pivot results, this is the
one most likely to survive the architecture change — steering comes from the profile→query
mapping, which the pivot kept, not from the backbone, which it deleted. "Most likely to
survive" is a reasoned expectation, **not a measurement**: no steering test has been run on
the rules-only architecture. Cite it as an untested-but-plausible carry-over, never as a
current number.

---

## 4. Robustness (Task R — edge cases) — `[backbone-crawl, ≤2026-07-30]`

| Edge case | Result |
|---|---|
| Niche topic, no Tübingen match (rocket-engine/aerospace propulsion) | ✅ Honest "no strong fit" output, no padding |
| Shallow / resistant student (8-turn simulated adversarial interview) | ✅ Gate never triggered a premature `find-university-chairs` call |
| Interdisciplinary routing (AI ethics across Law/Humanities-IZEW/Science-ML) | ✅ 5/5 GT anchors surfaced, 3/3 faculties/centers covered, no collapse onto one discipline |

3/3 pass. Two small spec gaps found and fixed during this task (zero-candidates rule in
`find-university-chairs/SKILL.md`; forced-choice + honest-fallback guidance for resistant
students in `build-student-profile/SKILL.md`). Source: `2026-07-03-task-r-edge-cases.md`.

---

## 5. Output & interview quality (Task S) — `[backbone-crawl, ≤2026-07-30]`

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

**Updated 2026-08-09, post-Task-AJ.** The one-sentence version: **the old architecture was
measured thoroughly and did well; the shipping architecture has been measured once.**

**On the deleted architecture `[backbone-crawl, ≤2026-07-30]`** — recall and precision are
strong across 6 faculties (four "easy" at ≥83% strict; two "hard" — Humanities 100%, Law 80% —
each clearing only after its respective protocol/skill fix). Steering is confirmed on one
faculty. Output quality (Task S) and robustness edge cases (Task R) both pass. The company
figures are **permanently demoted** (§2) and carry no weight.

**On the shipping architecture `[rules-only, ≥2026-07-31]`** — one faculty: Theology, 83%
recall / 100% precision, on a first blind run with no prior fix, which makes it the cleanest
single run in the document. That is the entire ground-truth evidence base for what users
actually install. There is additionally an uncommitted, self-scored conversation-quality
result (PR #71: baseline mean 20.0 → rules-only 20.75, 6/6 gates) which Task AL is to bring
into the repo — and which answers a *different question* than recall, so it cannot fill this
gap, only sit beside it.

**The "core is done" recall bar** (≥80% across ≥6 faculties incl. ≥1 hard) was **declared MET
on 2026-07-04** and that dated verdict stands, carrying both caveats in §1: the 2026-07-05
blindness gap, and the fact that the architecture it certified was removed on 2026-07-31.
See `2026-07-03-core-done-go-no-go.md` for the formal **GO** call.

**Standing methodological caveats,** unchanged and tracked in
`docs/thesis-report/03-hardening-and-evaluation/README.md`: single-agent, small-n scoring
across every table here. Two substantive items remain flagged from the Theology run — whether
the GT's **Witt** row is over-inclusive for a late-antique persona, and the GT §21 vacancy
scenario for an *ethics* persona, which no run has yet exercised.

**The gap that matters:** six of seven faculty figures describe a system nobody can install.
Closing it is Task AK (ground-truth re-measurement, CS + one hard faculty) and Task AL
(committed simulation evidence). Until they land, no claim in this document about *current*
discovery quality may rest on more than one faculty.
