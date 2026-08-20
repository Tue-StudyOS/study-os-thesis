# Task P — Steering Proof (does the interview change the search?)

> **Architecture tag (added 2026-08-09, Task AJ): `[backbone-crawl, ≤2026-07-30]`.**
> Every figure in this file was produced by the static-backbone architecture, removed on
> 2026-07-31 in favour of rules-only live discovery. The numbers are the honest record of
> that architecture; they do not describe the tool that ships today. Current picture:
> [eval scorecard §0](2026-07-03-eval-aggregate-scorecard.md).


- **Date:** 2026-07-02
- **Branch:** `feat/no-db-universal-skill`
- **Role:** roadmap Task P ([core-optimization-roadmap.md §3 Track 3](2026-06-28-core-optimization-roadmap.md)) —
  *"the most important for the thesis claim."* The whole premise of `find-university-chairs`
  is that the 6-dimension interview steers the search meaningfully better than plain Claude.
  Until now that had never been directly tested. This is that test.
- **Runs compared:** `dist/live-validation/cs-persona-A-skill.md`, `dist/live-validation/cs-persona-B-skill.md`
- **Skill under test:** `skills/find-university-chairs/SKILL.md` + `references/search-strategy.md`
  (stable since Task O, commits `2e5b503`/`e459683`).

## Design

Same faculty (`cs` → FB-Informatik + MPI-IS/ELLIS/Cyber Valley), same Pass-1 candidate set,
**two students with deliberately inverted profiles** so the predicted divergence is falsifiable:

| | Persona A | Persona B |
|---|---|---|
| **Interests** | causality / causal representation learning; probabilistic ML (Bayesian, prob. numerics) | computer vision (3D scene/human); self-supervised representation learning |
| **Methods** | probabilistic modelling, code-first | empirical deep learning, large-scale training |
| **No-gos** | **computer vision**, hardware/robotics | **heavy Bayesian / probabilistic theory**, hardware/robotics |

The two no-gos invert each other: A excludes exactly the topical cluster B is built around, and
vice versa. **Prediction if steering works:** the vision chairs (Geiger, Black, Pons-Moll,
Kühne, Bethge) top B's map and are absent from A's; the Bayesian/probabilistic chairs (Hennig,
Macke, Schölkopf) top A's map and are absent from B's. **Prediction if steering fails:** both
maps converge on roughly the same "top CS-ML chairs" list regardless of profile.

Every chair's routing to each persona is grounded in **live-verified facts** gathered this run
(WebSearch/WebFetch on FB-Informatik `forschung.html` + per-chair topic/recency queries), not
on assertion — e.g. Geiger's CVPR-2024 3D-vision work, Hennig's 2025 Probabilistic Numerics
conference editorship, Macke's simulation-based *Bayesian* inference, Kühne's ERC multimodal
grant. So the divergence rests on external evidence about what each group actually does.

## Result — the two maps diverge sharply, in the predicted direction

| Chair (live-verified focus) | Persona A | Persona B | Divergence |
|---|---|---|---|
| Schölkopf — Empirical Inference (causality) | **#1 core** | excluded (causality not B's; prob-leaning) | ▲→✗ |
| Hennig — Methoden des ML (prob. numerics / Bayesian) | **#3 core** | excluded (**Bayesian no-go**) | ▲→✗ |
| Macke — ML in der Wissenschaft (SBI / Bayesian) | **#4** | excluded (**Bayesian no-go**) | ▲→✗ |
| von Luxburg — Theorie des ML (stat. theory) | #5 (clean fit) | excluded (theory-heavy) | ▲→✗ |
| Martius — Distributed Intelligence (model-based RL) | #7 (kept+flag) | not surfaced | A only |
| Geiger — Autonomous Vision (3D CV) | excluded (**CV no-go**) | **#1 core** | ✗→▲ |
| Black — Perceiving Systems (3D humans) | excluded (**CV no-go**) | **#2 core** | ✗→▲ |
| Pons-Moll — Real Virtual Humans (3D CV) | excluded (**CV no-go**) | **#3 core** | ✗→▲ |
| Kühne — Multimodal Learning (repr. learning) | excluded (CV / topical) | **#4 core** | ✗→▲ |
| Bethge — Comp. Neuro & ML (visual repr.) | excluded (vision-leaning) | #5 strong | ✗→▲ |
| Lensch — Computergrafik | excluded (CV) | #7 adjacent | ✗→▲ |
| Berens — Data Science for Vision | excluded (CV) | #8 adjacent | ✗→▲ |
| Brendel — Robust ML | #2 (causal structure) | #6 (robust repr.) | present both, reframed |
| Hein — Maschinelles Lernen | #6 (optimization) | secondary (adversarial vision) | present both, reframed/reranked |
| Zell, Eivazi (hardware/robotics) | excluded | excluded | same (shared no-go) |
| Butz, Gehler, Krenn, Hardt | excluded (topical) | excluded (topical) | same |
| Oh — STAI (relocated KAIST) | flagged, excluded (2f) | flagged, excluded (2f) | same (affiliation) |

**Numbered options:** Persona A = {Schölkopf, Brendel, Hennig, Macke, von Luxburg, Hein,
Martius} (7). Persona B = {Geiger, Black, Pons-Moll, Kühne, Bethge, Brendel, Lensch, Berens}
(8). **Intersection = {Brendel, Hein}** — and even those two are reframed and reranked per
profile. ~6 of 7 (A) and ~6 of 8 (B) options are persona-unique.

**Conversation starters diverge completely too:** A's are "causal representation learning for
OOD generalization," "probabilistic ODE solvers with calibrated uncertainty," "simulation-based
inference as a general ML method"; B's are "generative 3D scene reconstruction," "single-image
garment/human reconstruction," "self-supervised video representation learning." No overlap.

## Verdict: **STEERING CONFIRMED (strong).**

The interview demonstrably changes the search. The profile is **not decorative**: on the same
faculty and the same Pass-1 candidate set, two inverted profiles produce near-disjoint option
maps whose top entries flip in exactly the direction each profile predicts. A chair that is #1
for one student is excluded for the other, and vice versa — this is the opposite of the
"same answer for everyone" failure mode the roadmap warned about. This is the first direct
defense of the "better than plain Claude" claim: plain Claude, given "find me a CS-ML thesis
chair in Tübingen," would return one generic top-ML list; the skill returns two materially
different, profile-justified lists.

## Which mechanism does the steering (and one honest gap)

Tracing *where* in `search-strategy.md` the divergence comes from:

1. **§1 profile→topic query variables** — the dominant lever. `{TOPIC}` = causality/Bayesian
   for A vs. computer-vision/representation for B produces different Pass-2a relevance queries,
   which surface different chairs' pages as "actively working on the topic."
2. **§5 topical-justification filter** — the second lever. It keeps only chairs whose *own*
   stated focus matches the profile, so a pure-Bayesian chair fails Persona B's topical test and
   a vision chair fails Persona A's. This is what makes the exclusions principled rather than
   arbitrary.
3. **§7 no-go exclusion** — a secondary amplifier here, and the **honest gap**: neither
   "computer vision" nor "heavy Bayesian theory" is a **codified row** in the §7 table (which
   lists only hardware, pure-math proofs, clinical, large SE, teaching). Both no-gos were applied
   via §7's *general* "discard entries that violate the student's no-gos" rule plus §5. It worked
   because both no-gos are topically obvious, but it means the codified rows did **not** carry the
   steering — §1 + §5 did. That's fine for the thesis claim (steering is real and driven by the
   interest→topic mapping), but it's a small documentation gap: §7's table reads as if it were
   the exhaustive no-go mechanism when in practice the general rule does most of the work. A
   one-line note in §7 ("this table is worked examples, not the whole no-go space; apply the
   general rule to any stated no-go") would make that explicit. **Not fixed in this task** —
   logged as a minor follow-up; it did not affect the result.

## Honest caveats (do not oversell)

1. **Single-agent authorship.** The same agent designed both personas, ran both, *and* judged
   the divergence. Confirmation bias is a structural risk: I knew the predicted split and
   produced it. The mitigation is that each chair→persona routing is anchored to live external
   facts (verified this run), not to my preference — but this is not an independent/blind test.
2. **Personas were built to diverge.** This proves the mechanism *can* steer when profiles
   differ on codifiable topical/no-go axes. It does **not** prove the skill steers on *subtle*
   personas that differ only slightly (e.g. two probabilistic-ML students with different
   sub-interests). That's a harder, separate test (candidate for a future Task).
3. **One faculty, one pair.** Same generalization caveat as every prior live run: `cs` is the
   best-understood, most-populated faculty. Steering on a sparse hard faculty (few chairs, less
   topical spread) is unproven — a chair-poor faculty may not *have* enough distinct groups for
   two profiles to diverge, which would be a robustness finding, not a steering failure.
4. **MPI-IS bot-block persisted** (fourth run) — Schölkopf/Brendel/Black confirmed via per-name
   search, not direct crawl. Unchanged known gap; did not affect steering.

## Pointer

Steering is confirmed; recall (100%, 3 runs) and precision (100% post-Task-O) are established.
Per the roadmap's "core is done" definition (§4), the remaining unproven axis is **robustness on
hard faculties** — Track 4 **Task Q (hard-faculty ground truth)**: extend ground truth to
Humanities/Theology/Law and an interdisciplinary persona. Caveat #3 above (does steering hold
when a faculty has few chairs?) is a natural thing to check while building that ground truth.
