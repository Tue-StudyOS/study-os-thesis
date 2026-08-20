# 03 — Hardening & Evaluation

**No files live in this folder** — the evaluation trail is dense and already dated/organized
under `findings/`; this section synthesizes and links rather than duplicates:
- [core-optimization-roadmap.md](../../../findings/no_db_universal_skill/2026-06-28-core-optimization-roadmap.md) —
  the Track 1–5 plan this whole phase follows, and its "definition of core is done" bar.
- [2026-07-03-eval-aggregate-scorecard.md](../../../findings/no_db_universal_skill/2026-07-03-eval-aggregate-scorecard.md) —
  **every recall/precision/steering/robustness number to date, in one place**, with sources
  and honest caveats per number. Read this first if you just want the numbers.
- Individual write-ups the scorecard aggregates: `2026-06-28-live-eval-results.md`,
  `2026-06-28-I-fix-revalidation.md`, `2026-06-28-phase2-live-eval-results.md`,
  `2026-07-02-live-eval-runbook.md`, `2026-07-02-task-p-steering-proof.md`,
  `2026-07-03-task-r-edge-cases.md` (all under `findings/no_db_universal_skill/`).
- `STATUS.md`, section "Post-Phase-3 hardening" — the literal current status of every task
  named below (Tasks J, O, P, Q, R; Track 2; Task S).
- [2026-07-05-fable-1.0-readiness-review.md](../../../findings/no_db_universal_skill/2026-07-05-fable-1.0-readiness-review.md) —
  an independent, deliberately skeptical review of everything below, run after this
  synthesis was written. Read it alongside this section, not instead of it: it confirms
  the mechanism and design are sound but disputes the blindness of the two hard-faculty
  numbers behind the GO verdict (see the updated "Honest limitations" paragraph below).

---

> ## ⚠️ Architecture banner — added 2026-08-09 (Task AJ)
>
> **Unless a number below is explicitly marked otherwise, it is `[backbone-crawl, ≤2026-07-30]`
> — it was produced by the static-backbone architecture that was removed on 2026-07-31**
> (commit `44e7e53`, PR #71) in favour of rules-only live discovery.
>
> The only faculty measurement of the shipping architecture is **Theology, 2026-08-08 (Task V′):
> 83% recall / 100% precision, `[rules-only, ≥2026-07-31]`**, on a first blind run with no
> prior fix.
>
> This section is kept as written because it is the honest record of how the *evaluation
> method* developed — and that development, not the coverage figures, is what this chapter is
> actually about. The circularity discovery, the live-run rule, the steering proof design and
> the blindness critique are all method results, and they survive the pivot intact. The
> percentages do not describe the tool a user installs today.
>
> Per-number detail: [the scorecard's §0 standing note](../../../findings/no_db_universal_skill/2026-07-03-eval-aggregate-scorecard.md).

## Synthesis

The single most important methodological turn in this project happened right after Phase 1
"passed": **Task H's fixture-based eval was found to be circular.** The skill-arm
conversations had been hand-authored with the ground-truth names already written into them,
and the baseline arm was a scripted strawman whose "0% recall" wasn't a real measurement — a
close read showed the strawman was actually giving reasonable advice. A 96%-vs-0% gap that
looks decisive on paper measured nothing about real model behavior. This forced a hard rule
for the rest of the project: **only a live run, with a no-peeking protocol and a real
plain-Claude-plus-Websearch baseline (not a scripted strawman), counts as evidence.** Task I
re-ran all four Phase-1 faculties live under that discipline and found a materially different,
more honest picture: primary recall ~82% (not 96%), and — critically — the "0% baseline" was
actually ~17%, because plain Claude does know some correct names. The real, defensible margin
over baseline is ~+65 percentage points, not the fixture's fictional +96
— `[backbone-crawl, ≤2026-07-30]`, and worth flagging on its own: this is the strongest
comparative number the project owns, and it belongs to the deleted architecture. It has never
been re-measured post-pivot. The same live run
surfaced two concrete, fixable defects: a professor **misattribution** in Psychology (the
wrong chair-holder named for a unit, because a search result described a *different* group
with a similar name) and a **coverage gap** in CS (MPI-IS-affiliated researchers, not listed
on the standard FB-Informatik page, were missed entirely). Both were fixed (Task I-fix: a
mandatory person-verification step before naming anyone; MPI-IS/ELLIS added as first-class
Pass-1 sources) and re-validated live — all four faculties then cleared ≥70% on both the
lenient ("primary") and strict ("recommended and correctly attributed") reading of recall.

The Phase-2 (company) eval followed the same live-validation discipline and also cleared its
bar (100% recall across 3 profiles, +26pp mean over baseline) — but it carried a caveat that
has since hardened into a permanent demotion: the ground truth was built from the **same** BW
company backbone the skill searched, so the eval measured "does the skill find what's in the
backbone," not "does the backbone reflect reality." **Settled 2026-08-09 (Task AJ):** that
backbone was itself deleted on 2026-07-31, so the eval is now circular *and* measures a file
that no longer exists *and* tests an architecture that no longer ships. It is demoted to a
**plumbing check** and carries no weight as a quality claim; old Task Y (build an independent
company ground truth) is closed permanently rather than left open. Full reasoning: scorecard §2.

The post-Phase-3 "hardening" track (`core-optimization-roadmap.md`) exists because passing a
recall threshold isn't the same as being *good* — the roadmap names five independent quality
axes (recall, precision, steering, output usefulness, robustness) and Task H had only ever
touched the first. Precision was added as a metric (a live CS run went from 75% to 100%
precision after tightening a relevance filter and adding an affiliation-currency check that
catches a professor who has physically relocated — a failure mode recency-checking alone can't
catch, since a stale page can still look "recently active"). The most consequential result of
this track, and arguably of the whole project, is **Task P's steering proof**: two students
with deliberately inverted profiles (one wants causal/Bayesian ML and explicitly excludes
computer vision; the other wants computer vision and explicitly excludes heavy Bayesian
theory) were run through the identical skill, on the identical faculty, against the identical
Pass-1 candidate set — and produced **near-disjoint option maps** (only 2 of 8 top options
overlapped, and even those two were re-ranked and re-framed per profile). This is the first
direct empirical answer to the question the 2026-06-25 meeting notes asked out loud: *"what's
the difference to just using Claude without a skill?"* If the interview didn't change the
output, the answer would be "none" — Task P shows it does, sharply.

Task Q then extended ground truth to structurally harder faculties (Humanities, Law,
Theology, plus an interdisciplinary AI-ethics persona) to test whether the same mechanism
holds outside the "easy," well-organized faculties Phase 1 was built and tuned on. Its first
blind live run (Humanities) landed at 60% recall — below the roadmap's 80% robustness bar —
but the honest read is more nuanced than "the skill got worse on hard faculties": the miss was
root-caused to the **eval protocol** (an incomplete one-line persona summary), not the skill
itself, which found and correctly evaluated all 5 ground-truth chairs. Law and Theology have
ground truth but no live run yet. Task R separately exercised three robustness edge cases
(a niche topic with no Tübingen match, a shallow/resistant student, interdisciplinary routing
across three faculties) and passed all three cleanly, fixing two small spec gaps along the way.

**Honest limitations, stated plainly for the write-up (updated 2026-08-09, Task AJ):** every
live run to date has been designed, executed, and scored by a single agent in a single
session — a confirmation-bias risk mitigated only by grounding every factual claim in a
live-verified source, not by independent review. Sample sizes per faculty are n=1–3, not
enough to claim the filters generalize. The company eval is permanently demoted (see above).

**The largest limitation is now the architecture break, not any single number.** Six of the
seven faculty figures were produced by an architecture deleted on 2026-07-31; the shipping
architecture has exactly one ground-truth faculty measurement. No amount of care in the old
runs compensates for that, and the honest statement in the write-up is that current discovery
quality rests on **one faculty**, with Task AK named as the repair.

On the recall bar itself: it was declared **MET** on 2026-07-04 (Task T's eval-protocol fix +
Task U's skill fix), flipping the go/no-go to **GO** — but an independent 2026-07-05 review
found the two hard-faculty numbers behind that verdict were not clean blind measurements:
Humanities' 100% is a re-score by a session that was explicitly un-blind on that faculty,
and Law's 80% re-run's session had already read the document naming the missed chair and
the fix that flips her. Every genuinely blind hard-faculty run at that point (Humanities 60%,
Law 60%) landed below the 80% bar. **Partially repaired 2026-08-08:** Task V′ ran Theology
blind — 83% recall / 100% precision, no prior fix — which is simultaneously the first clean
blind hard-faculty run *and* the first post-pivot faculty measurement. The GO stands as
dated, provisional on the two counts recorded in the scorecard.

Output quality (Task S) is scored (4/5 criteria pass cleanly; the one repeated gap was found
and fixed), but, like everything else here, by the same single-agent process. The independent
re-scoring pass that used to be Phase 5 Task X is no longer a standalone task: it is absorbed
into **Task Z′**, where the beta testers co-score the unknown-option and factual-error
measures with us — the only genuinely independent evaluation this project will get. These are
named explicitly rather than smoothed over, in
keeping with the project's own evidence-rules discipline (never invent, never claim
completeness, flag what's uncertain). Full numbers, per-faculty, with sources:
[2026-07-03-eval-aggregate-scorecard.md](../../../findings/no_db_universal_skill/2026-07-03-eval-aggregate-scorecard.md).
Independent critical review — methodology assessment, scope-claim evaluation, and the
full Phase 5 punch list this paragraph summarizes:
[2026-07-05-fable-1.0-readiness-review.md](../../../findings/no_db_universal_skill/2026-07-05-fable-1.0-readiness-review.md).
