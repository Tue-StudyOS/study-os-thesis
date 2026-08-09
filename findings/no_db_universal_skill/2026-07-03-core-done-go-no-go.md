# Go/No-Go — Does the Tübingen Core Clear Roadmap §4 ("core is done")?

- **Date:** 2026-07-03
- **Branch:** `feat/no-db-universal-skill`
- **Type:** Judgment call over existing eval evidence. **No new live run.** The
  deliverable is this decision, not a skill change.
- **Inputs:** [`2026-07-03-eval-aggregate-scorecard.md`](2026-07-03-eval-aggregate-scorecard.md),
  [`2026-07-03-task-s-output-quality.md`](2026-07-03-task-s-output-quality.md),
  [`2026-06-28-core-optimization-roadmap.md`](2026-06-28-core-optimization-roadmap.md) §4–§5,
  STATUS.md (Task Q/Q-run-1/R/S + Eval Scorecard rows).

---

> ## ⚠️ Standing caveat — added 2026-08-09 (Task AJ). Read before citing this verdict.
>
> **The GO recorded below is not retracted. It is date-stamped, and it is provisional on two
> counts.**
>
> **Every number in this document is `[backbone-crawl, ≤2026-07-30]`.** All of it was
> produced by the static-backbone architecture, which was **removed on 2026-07-31** (commit
> `44e7e53`, PR #71) in favour of rules-only live discovery. This verdict therefore certifies
> a system that no longer ships.
>
> | # | The GO is provisional because… | Status |
> |---|---|---|
> | 1 | **Blindness gap** (flagged 2026-07-05): the two hard-faculty numbers behind it are not clean blind measurements. Humanities' 100% is a re-score by a session un-blind on that faculty; Law's 80% re-run's session had already read the document naming the missed chair and the fix that flips her. Every genuinely blind hard-faculty run at the time (Humanities 60%, Law 60%) was below the bar. | **Closed for one faculty 2026-08-08** — Task V′ ran Theology blind at 83% recall / 100% precision with no prior fix |
> | 2 | **The architecture it certified was deleted** (added 2026-08-09). | **Open** — Task AK is the named repair |
>
> What this does **not** invalidate: the skill fixes found along the way. Task U's
> enrich-before-exclude rule and Task T's eval-protocol fix are real, were verified
> independently within the same evidence, and survived the pivot. The *defects found* keep
> their value; the *coverage figures* do not describe the current tool.
>
> Current picture: [`2026-07-03-eval-aggregate-scorecard.md`](2026-07-03-eval-aggregate-scorecard.md) §0.

---

> **Update — 2026-07-04, post-Task-U. VERDICT FLIPPED TO GO.** Task U (1) added an
> *enrich-before-exclude* rule to `search-strategy.md` §5 — the symmetric dual of the
> Butz over-inclusion guard: do not exclude a candidate at the topical-justification
> step from a title-only reading when the title names a core-interest field amid
> off-interest strands; enrich first. (2) Re-ran **Law** blind under the fixed skill:
> **80% recall / 100% precision** (found von Bernstorff, Nettesheim, Finck, **Remmert**;
> missed Saurer — an honest, defensible miss, not the same defect class). Remmert's
> dense multi-strand title reads economic/municipal on its face, but Pass-2 enrichment
> of her own Schwerpunkte surfaced "Allgemeine Grundrechtslehren" (fundamental-rights
> doctrine) — a core constitutional-law/human-rights match. All **6 measured faculties**
> now clear the ≥80% recall bar (CS 100%, Medicine ≥83%, Psychology ≥83%, WiSo ≥83%,
> Humanities 100%, Law 80%), with 2 of 6 being hard faculties. §4 criterion 1 is met.
> Full write-up: `2026-07-02-live-eval-runbook.md` (2026-07-04 log entry).

> **Update — 2026-07-03, post-Task-T.** Task T ran the cheap path below.
> **Outcome: the original blocker is resolved, but NO-GO still stands (transformed).**
> The eval-protocol fix landed; the Humanities 60% became **100%** under the corrected
> persona (both misses were the dropped-clause artifact — hypothesis confirmed). But the
> genuinely-blind **Law** run came in at **60% recall / 100% precision** and surfaced a
> *new, real* skill defect: the §5 topical-justification filter excluded a core-relevant
> chair (**Remmert** — actual focus *Allgemeine Grundrechtslehren*, a constitutional-law/
> human-rights match) at the title-surface level without Pass-2 enrichment. Now **5 of 6**
> measured faculties clear 80% (Law is the sole miss), so the strict per-faculty reading
> of criterion 1 is still not met. Next task is **Task U** (§5 enrich-before-exclude fix +
> Law re-run), not GO. Full write-up:
> [`2026-07-03-task-t-recall-closeout.md`](2026-07-03-task-t-recall-closeout.md).

## Verdict: **GO** (as of 2026-07-04, post-Task-U) — `[backbone-crawl, ≤2026-07-30]`, provisional on two counts (see the standing caveat above).

The core clears roadmap §4's bar. All five criteria are now met: criterion 1's
recall bar clears across all 6 measured faculties (2 of them hard), and criteria
2–5 were already met as of Task T. The path to GO ran through two sequential
fixes — an eval-protocol fix (Task T) and a genuine skill fix (Task U's §5
enrich-before-exclude rule) — both landed, both verified live. See the criteria
table below and the updated evidence for criterion 1.

**Updated criterion 1 evidence (2026-07-04):**

| Faculty | Recall | Hard? | ≥80%? |
|---|---|---|---|
| CS | 100% | – | ✅ |
| Medicine | ≥83% | – | ✅ |
| Psychology | ≥83% | – | ✅ |
| WiSo | ≥83% | – | ✅ |
| Humanities | 100% | hard | ✅ |
| Law | 80% | hard | ✅ |

All 6 of 6 measured faculties clear 80% under the strict per-faculty reading this
go/no-go adopted (§ below). Criterion 1: **MET.**

*(The remainder of this document below is preserved as the historical record of
the NO-GO analysis that led to Tasks T and U; it is no longer the live verdict.)*

---

## Scoring against §4's five criteria

§4 is deliberately stricter than the original ≥70% gate ("optimal core," not
"passes"). Scored against the aggregate scorecard:

| # | §4 criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | recall ≥80% across **≥6 faculties incl. ≥1 hard** | ❌ **NOT MET** | Only **5** faculties have any live number (Med/Psych/WiSo/CS/Humanities). The **only** hard faculty with a live number (Humanities) is **60%**, below 80%. Law/Theology have GT, no live run. |
| 2 | precision high enough (map not padded) | ⚠️ under-sampled | Strong where measured — CS 100% (post-Task-O), Humanities 100% — but only **2 of 5** faculties formally scored. |
| 3 | steering proven | ✅ MET | Task P: near-disjoint maps on inverted CS personas, correct-direction flips. |
| 4 | output honest & actionable | ✅ MET | Task S: 4/5 criteria pass; the one repeated gap (dated-evidence field) was found and fixed. |
| 5 | edge cases degrade gracefully | ✅ MET | Task R: 3/3 (niche no-match, resistant-student gate, interdisciplinary routing). |

**Criterion 1 fails twice, independently:**
- **(a) Count:** only 5 faculties measured, so "≥6 faculties" cannot be claimed at
  all — regardless of any single number.
- **(b) Hard-faculty bar:** no hard faculty has produced a clean live ≥80%.
  Humanities is 60% (caveated), Law/Theology are unrun.

Reading adopted: "recall ≥80% across ≥6 faculties" means **each** of ≥6 faculties
clears 80% (the per-faculty reading), consistent with §4's stated intent of a
stricter "optimal core" bar rather than a mean that lets one weak faculty hide.

## Why the Humanities caveat does not convert this to a GO

The 60% is genuinely root-caused to the **eval protocol, not the skill**: the live
Pass-1 crawl found and evaluated all 5 GT chairs (Faculty→FB5→Seminar drill-down
worked first try); 2 were then excluded by a reasonable no-go the *persona* implied,
because the persona was built from the README's **one-line sample-interest summary**,
which drops a clause present in `humanities.md`'s full sample interest ("...with an
interest in the history of the field"). See Task Q run 1 (STATUS.md, 2026-07-03).

That is strong evidence the **discovery machinery works on a hard faculty** — but it
is an argument for *fixing the protocol and re-running to book a clean number*, not
for declaring §4 met on a number the skill never actually produced. You cannot
credit a ≥80% hard-faculty recall that no run has yet shown.

## Why not GO anyway on "the machinery is proven"

1. **Precedent.** This project was already burned once by a premature "gate GREEN"
   declared on partial evidence — the 2026-06-28 CI-hygiene entry (verdicts that had
   only ever run the eval-harness tests, never the package/release suite). Declaring
   §4 done with its headline criterion literally unmet, when the fix is cheap, repeats
   exactly that failure mode.
2. **No schedule pressure to cut the corner.** §4 gates *moving to Phase 2
   (companies)*. But Phase 2 is **already built and GREEN** (Tasks 2-A–2-E: 100%
   recall all 3 profiles, +26pp over baseline). So the thing the gate protects has
   already happened in parallel — there is no downstream work waiting on a GO. The
   only open university-core frontier *is* this recall gap. Nothing competes with it
   for priority, so there is no reason to book it as done rather than simply close it.

## What a GO would require (the cheap path)

Two shortfalls, both closable without touching the skill's discovery logic:

1. **Fix the eval-protocol gap.** The runbook builds test personas from the README's
   lossy one-line sample-interest summaries instead of the GT files' full sample
   interest. This is the documented root cause of the Humanities 60%. Fix: build
   personas from each GT file's full sample interest (or bring the README summaries
   into sync with the GT files). This is an **eval-harness fix, not a skill change.**
2. **Two blind hard-faculty runs** to satisfy both halves of criterion 1:
   - **Re-run Humanities blind** under the corrected protocol — converts the caveated
     60% into a clean number and directly tests the central hypothesis (that the miss
     was protocol, not skill). Expect it to clear 80%, since the crawl already found
     all 5.
   - **Run one more hard faculty blind** (Law recommended — GT exists at
     `skills/tests/eval_ground_truth/law.md`, and it tests a *different* hardness axis:
     dense German public-law chair-title formulas, not tree drill-down). This lifts
     the measured-faculty count from 5 to 6.

   Together these give: 4 easy faculties (≥83% strict) + Humanities (hard, re-run) +
   Law (hard) = 6 measured, with ≥1 hard faculty ≥80% — clearing criterion 1 on both
   the count and the hard-faculty bar.

   (Optional, strengthens criterion 2: record precision on these runs, lifting formal
   precision coverage from 2/5 toward 4/5.)

## The named next task

> **Task T — Eval-protocol fix + hard-faculty recall closeout.**
> (1) Fix the runbook so personas are built from the GT files' full sample interest,
> not the README's lossy one-liners. (2) Blind-re-run **Humanities** under the fixed
> protocol. (3) Blind-run **Law**. Score recall (and precision) on both. Done-when:
> ≥6 faculties have a live recall number with ≥1 hard faculty ≥80% — at which point
> §4 criterion 1 is met and this go/no-go is revisited to a GO.

This is a concrete, actionable task, not left implicit. Until it lands, the Tübingen
core is **"strong and near-done, recall bar not yet booked on hard faculties"** —
not "done."

---

## Bottom line

NO-GO. Criteria 2–5 of §4 are met or strong; criterion 1 (the recall bar) is not,
failing on both the ≥6-faculty count and the ≥1-hard-faculty-≥80% requirement. The
gap is measurement + a cheap protocol fix, not a skill defect. Because Phase 2 is
already GREEN, there is no cost to doing this properly instead of declaring it done.
Next task: **Task T** above.
