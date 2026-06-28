# Task I — Live Validation Protocol (real recall, real baseline)

- **Date:** 2026-06-28
- **Branch:** `feat/no-db-universal-skill`
- **Why this exists:** The Task H eval ran in **fixture mode** — the skill-arm
  conversations were hand-authored and already contained the ground-truth chair
  names, and the baseline arm was a scripted strawman. So the "96% vs. 0%" result
  is **circular**: it measures fixture authoring, not live skill behavior. Nothing
  about the live skill's recall or its advantage over plain Claude is yet proven.
  This task produces the **real** measurement.

---

## Goal

Measure, with live web search, (1) the discovery skill's real recall against the
4-faculty ground truth, and (2) how it compares to real plain-Claude on the same
personas. Honest numbers, no hand-authored answers.

## Hard validity rules (read before running)

1. **No peeking.** The discovery output for a faculty MUST be produced *before*
   looking at that faculty's `eval_ground_truth` file. Search live, write the
   option map, save it, *then* open the ground truth and score. Otherwise the run
   is contaminated like the fixtures were.
2. **Skill arm = actually follow the skill.** Read
   `skills/find-university-chairs/SKILL.md` and its references, then execute the
   two-pass search with real `WebSearch`/browse calls. Do not shortcut to known
   names from memory.
3. **Baseline arm = no skill, no references, no ground truth.** A clean prompt:
   "I'm a [persona] looking for a Master's thesis in [interest] at Uni Tübingen —
   who should I contact?" Plain Claude with whatever tools it would normally use.
   Do NOT read any skill file in the baseline arm.
4. **One persona per faculty**, profile matched to that faculty's
   `sample interest` in the ground truth (so recall is a fair target).
5. **Recall = ground-truth chairs surfaced by name / total ground-truth chairs.**
   Note medium vs. high relevance separately but score recall on name-surfacing.

## Procedure (per faculty: medicine, psychology, wiso, cs)

1. Build/instantiate the persona profile (6 dimensions) matching the faculty's
   sample interest.
2. **Skill arm:** follow SKILL.md end-to-end with live search → save the option
   map to `dist/live-validation/<faculty>-skill.md`.
3. **Baseline arm:** clean conversation, no skill → save to
   `dist/live-validation/<faculty>-baseline.md`.
4. Open `skills/tests/eval_ground_truth/<faculty>*` and score both arms.
5. Record: skill recall, baseline recall, delta, and any honest misses.

## Output

`findings/no_db_universal_skill/2026-06-28-live-eval-results.md` with:

- per-faculty table (skill recall, baseline recall, delta)
- comparison to the fixture-mode numbers (did live match the fixture optimism?)
- honest notes: where the skill missed, where the baseline was actually fine,
  whether the profile genuinely steered the search
- a verdict on the real Phase-1 gate: does the live skill clear ≥70%, and does it
  beat plain Claude by a meaningful margin?

## Tooling note

This needs an environment with live `WebSearch` (Claude Code has it; no Codex
required — that was only the harness's live-runner constraint). The Python harness
is not used here; this is a manual, in-conversation protocol because that is what
actually exercises the skill.

## Done-when

- All 4 faculties run in both arms with no peeking
- Real recall + real baseline recorded in the results file
- An honest verdict on whether Phase 1 truly passes its gate
