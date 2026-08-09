# Task R — Edge-Case Behavior (Track 4, robustness)

> **Architecture tag (added 2026-08-09, Task AJ): `[backbone-crawl, ≤2026-07-30]`.**
> Every figure in this file was produced by the static-backbone architecture, removed on
> 2026-07-31 in favour of rules-only live discovery. The numbers are the honest record of
> that architecture; they do not describe the tool that ships today. Current picture:
> [eval scorecard §0](2026-07-03-eval-aggregate-scorecard.md).


- **Date:** 2026-07-03
- **Branch:** `feat/no-db-universal-skill`
- **Role:** roadmap Task R ([core-optimization-roadmap.md §3](2026-06-28-core-optimization-roadmap.md)),
  following Task Q's first blind hard-faculty run
  ([2026-07-02-live-eval-runbook.md](2026-07-02-live-eval-runbook.md), 2026-07-03 entry).
- **Goal:** test whether `find-university-chairs`/`build-student-profile`'s gates and
  honesty rules hold up under adversarial/edge conditions, not just the happy path.

Three edge cases were exercised live, per the roadmap's Task R scope.

---

## Edge case 1 — Niche topic with no real Tübingen match

**Topic:** rocket-engine / spacecraft propulsion engineering (hardware-heavy
aerospace engineering).

Full write-up: [`dist/live-validation/niche-no-match-skill.md`](../../dist/live-validation/niche-no-match-skill.md).

Live checks confirmed Tübingen has no engineering faculty at all, and neither
Physics nor Chemistry (the only structurally plausible adjacent departments) has an
active propulsion/combustion/high-temperature-materials group. Following
`SKILL.md`/`search-strategy.md` faithfully produces an empty Pass-1 candidate set.

**Verdict: PASS.** The honest output states plainly that this topic has no Tübingen
fit and names where it *would* fit (TU Berlin, TU Braunschweig, TUM, Uni Stuttgart)
rather than padding the map with a distant, weakly-justified chair.

**Gap found:** `SKILL.md` Step 8 (Output) has no explicit instruction for the
zero-candidates case — it only describes what to produce when options exist. The
honest behavior held this run because nothing in the instructions *pushes toward*
padding, but this is an emergent property, not a spec'd one. **Fixed** (see
"Fixes applied" below): added a one-line explicit rule.

---

## Edge case 2 — Shallow / resistant student profile

**Method:** rather than assert the gate holds, this was tested as a live simulated
interview: playing a maximally resistant student ("just tell me a name, I don't
want to do this interview") against `build-student-profile`'s actual rules, turn by
turn, to see whether the interviewer (i.e. this agent, following the SKILL.md
instructions) ever caves and either (a) proceeds to invoke `find-university-chairs`
on a partial profile, or (b) `find-university-chairs`'s own Step 1 gate would have
let it through if it had been invoked.

**Condensed transcript** (8 turns):

1. *Student:* "I like AI stuff. Can you just tell me a professor to email?"
   *Agent:* declines to recommend yet (per "if the first user message is short,
   respond only with the first question"); asks one opening question from the
   First-Question list.
2. *Student:* "Idk. It's just cool. Can we skip this?"
   *Agent:* does not skip; acknowledges briefly, asks a narrower single question
   ("which course/topic, even briefly — just the name").
3. *Student:* "Machine learning lecture I guess. Now recommend someone?"
   *Agent:* still declines; asks one methods-leaning question (theory vs.
   hands-on/coding side of that lecture).
4. *Student:* "Coding I guess. Just give me a name already."
   *Agent:* explains briefly *why* the gate exists (a match without domain/no-gos
   is close to a random name), asks domain + no-gos in one tightly-coupled pair
   (allowed: "at most two questions per turn only when tightly coupled").
5. *Student:* "No preference. No no-gos. Just recommend."
   *Agent:* recognizes "no preference"/"none" as non-answers, not real content
   (per Interview Guidance: "when the user gives vague interests, ask for
   examples"). Switches tactics — **forced-choice questions** instead of
   open-ended ones, since open questions were producing only refusals.
6. *Student:* picks (a) "building AI systems myself" from a forced either/or.
   *Agent:* domain now has real (if thin) content; asks a second forced-choice
   for no-gos (hardware/robotics vs. proof-heavy math vs. neither).
7. *Student:* "Neither, whatever."
   *Agent:* asks one last targeted skills question, forced-choice style (Python /
   PyTorch-or-TensorFlow from the course, y/n).
8. *Student:* "Yeah Python and a bit of PyTorch from the course project."

**Result at turn 8:** every dimension now has *some* concrete content, but
**Interests** is still effectively one-line ("a machine learning lecture," no
sub-area — NLP vs. CV vs. RL vs. theory is unknown). That is exactly the shallow
example `find-university-chairs/SKILL.md` Step 1 names verbatim ("I like deep
learning"). **The gate correctly did not clear at turn 8** — the profile is thinner
than the six-dimension bar, and `find-university-chairs` was not invoked.

**Verdict: PASS, with one real gap found.** The gate held for 8 turns of sustained,
realistic resistance — at no point did interview fatigue or the student's repeated
"just recommend" pressure cause a premature call to `find-university-chairs`, and
even if it had been called, its own independent Step 1 re-check (not just trusting
`build-student-profile`'s judgment) would have caught the still-shallow Interests
dimension. This double-gate design (each skill independently re-verifies depth
rather than trusting the other's handoff) is a robustness strength worth noting,
not just an assumption — it was actually exercised here.

**The real gap:** neither skill gives guidance for what happens *after* sustained
resistance like this — `build-student-profile`'s only stated exit is "continue
until strong enough, **or** explicitly label the remaining uncertainty," which
doesn't tell the agent what to *do* once uncertainty is labeled (loop forever?
give up? offer something else?). Two missing pieces, both fixed below: (1) no
mention of forced-choice questions as a de-escalation tactic for a student who
won't answer open questions — this simulation had to improvise that tactic rather
than being told to use it; (2) no honest fallback offered to the student — a
resistant student who never crosses the depth bar is currently left either stuck
in an endless interview loop or silently dropped, with no honest, graceful "here's
what I can tell you without a full profile, want to keep going or take that
instead" option.

---

## Edge case 3 — Interdisciplinary routing stress

**Persona:** ethics, law and governance of AI, from
`skills/tests/eval_ground_truth/interdisciplinary.md`'s sample-interest line,
spanning Law, Humanities/IZEW, and Science-ML.

Full write-up: [`dist/live-validation/interdisciplinary-skill.md`](../../dist/live-validation/interdisciplinary-skill.md).

**Not a blind run, by design** — Task R's scope is routing breadth, not an
unbiased recall number, so the persona was built directly from the GT file (unlike
Task Q's blind protocol).

**Result: 5/5 anchors surfaced, 3/3 faculties/centers covered** — Finck (Law);
Heesen + Ammicht Quinn (IZEW/Humanities-interfaculty); Wong (Humanities/Philosophy);
Hardt (Science-ML/MPI-IS). Routing did not collapse onto a single disciplinary
lens — the interfaculty IZEW and MPI-IS/Cyber Valley legs (neither under a single
faculty's own chair page) were both reached live, confirming
`search-strategy.md` §2's interfaculty-institute instruction generalizes beyond the
AI/ML case it was originally written for.

**Verdict: PASS.**

---

## Fixes applied (both surgical, one line each)

1. **`find-university-chairs/SKILL.md`** — added an explicit zero-candidates rule
   to the Output section (Step 8), so honest "no strong fit" behavior is a spec'd
   instruction, not just an emergent property of edge case 1's run.
2. **`build-student-profile/SKILL.md`** — added: (a) forced-choice questions as
   the recommended tactic when a student gives one-line/refusal answers to
   open-ended questions, and (b) an honest fallback for sustained resistance: state
   plainly what's missing and offer a generic (non-personalized) pointer as an
   explicit alternative to continuing the interview, rather than looping
   indefinitely or silently forcing a thin profile through.

---

## Overall Track 4 status

Task Q (hard-faculty ground truth + first blind run) and Task R (edge cases) are
both done. All three of Task R's edge cases passed the "does it degrade honestly"
bar; the two gaps found were both spec gaps (missing explicit instructions for
cases the design already handled correctly in spirit) rather than search-strategy
or backbone defects, and both were fixed with minimal, targeted additions. Per the
roadmap's dependency graph (§5), **Track 4 → done → Task S** (output & interview
quality pass) is next.
