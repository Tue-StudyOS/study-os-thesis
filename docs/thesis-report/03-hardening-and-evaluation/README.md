# 03 — Hardening & Evaluation

**No files live in this folder** — the evaluation trail is dense and already dated/organized
under `findings/`; this section synthesizes and links rather than duplicates:
- [core-optimization-roadmap.md](../../../findings/no_db_universal_skill/2026-06-28-core-optimization-roadmap.md) —
  the Track 1–5 plan this whole phase follows, and its "definition of core is done" bar.
- Live-eval results: `2026-06-28-live-eval-results.md`, `2026-06-28-I-fix-revalidation.md`,
  `2026-06-28-phase2-live-eval-results.md`, `2026-07-02-live-eval-runbook.md`, `2026-07-02-task-p-steering-proof.md`
  (all under `findings/no_db_universal_skill/`).
- `STATUS.md`, section "Post-Phase-3 hardening" — the literal current status of every task
  named below (Tasks J, O, P, Q; Track 2; Tasks R/S).

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
over baseline is ~+65 percentage points, not the fixture's fictional +96. The same live run
surfaced two concrete, fixable defects: a professor **misattribution** in Psychology (the
wrong chair-holder named for a unit, because a search result described a *different* group
with a similar name) and a **coverage gap** in CS (MPI-IS-affiliated researchers, not listed
on the standard FB-Informatik page, were missed entirely). Both were fixed (Task I-fix: a
mandatory person-verification step before naming anyone; MPI-IS/ELLIS added as first-class
Pass-1 sources) and re-validated live — all four faculties then cleared ≥70% on both the
lenient ("primary") and strict ("recommended and correctly attributed") reading of recall.

The Phase-2 (company) eval followed the same live-validation discipline and also cleared its
bar (100% recall across 3 profiles, +26pp mean over baseline) — but it carries an honest,
still-open caveat: the ground truth was built from the **same** BW company backbone the skill
searches, so the eval measures "does the skill find what's in the backbone," not "does the
backbone reflect reality." This circularity is explicitly logged as unresolved (see
[04](../04-open-work/README.md)).

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
output, the answer would be "none" — Task P shows it does, sharply. Task Q then extended
ground truth to structurally harder faculties (Humanities, Law, Theology, plus an
interdisciplinary AI-ethics persona spanning three faculties) to test whether the same
mechanism holds outside the "easy," well-organized faculties Phase 1 was built and tuned on —
its blind live run is deliberately deferred to a fresh conversation (see
[04](../04-open-work/README.md)) to avoid contaminating the no-peeking protocol that gives
these results their credibility in the first place.

**Honest limitations, stated plainly for the write-up:** every live run to date has been
designed, executed, and scored by a single agent in a single session — a confirmation-bias
risk mitigated only by grounding every factual claim in a live-verified source, not by
independent review. Sample sizes per faculty are n=1–3, not enough to claim the filters
generalize. The company eval's ground-truth circularity is unresolved. These are named
explicitly rather than smoothed over, in keeping with the project's own evidence-rules
discipline (never invent, never claim completeness, flag what's uncertain).
