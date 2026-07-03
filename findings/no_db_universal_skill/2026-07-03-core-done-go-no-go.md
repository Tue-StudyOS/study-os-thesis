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

## Verdict: **NO-GO** — narrowly, with a cheap named path to GO.

The core is *not* done against roadmap §4's own bar. Three of five criteria are
cleanly met; the headline recall criterion is not, and it fails on two independent
counts. The gap is not a skill defect — it is an unrun measurement plus a known,
cheap eval-protocol fix. Closing it is the next task.

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
