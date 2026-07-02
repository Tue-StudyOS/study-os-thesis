# Live-Eval Runbook — Re-validate One Faculty Cheaply

- **Date:** 2026-07-02
- **Branch:** `feat/no-db-universal-skill`
- **Role:** roadmap Task J ([core-optimization-roadmap.md §3](2026-06-28-core-optimization-roadmap.md)).
  Note the letter collision: STATUS.md's Post-Phase-3 hardening table already used
  "Task J" for an unrelated fix (canonical six profile dimensions). This runbook is
  logged there as **Roadmap-J** to avoid confusion — see STATUS.md.
- **Why this exists:** [2026-06-28-live-validation-protocol.md](2026-06-28-live-validation-protocol.md)
  is the right process but it's written for a one-time, all-4-faculty validation run
  (~2 hours). After a skill change (e.g. a query-skeleton edit, a backbone fix), you
  need a cheap way to re-check *one* faculty without re-reading the full protocol or
  re-running everything. This is that checklist.

## When to run this

After any change to `skills/find-university-chairs/SKILL.md`,
`references/search-strategy.md`, or `references/tuebingen-faculty-backbone.md` that
could plausibly affect recall or precision. Skip for pure prose/typo edits.

## Checklist (~15–20 min for one faculty)

1. **Pick the faculty** most exercised by the change (e.g. a backbone fix to §Medicine
   → re-run medicine; a query-skeleton change → pick whichever faculty's queries
   changed, or `cs` as the default well-understood case).
2. **Reuse the existing persona** for that faculty from
   `skills/tests/eval_ground_truth/<faculty>.md` (or `cs_seed/`) — same sample
   interest, so results are comparable to the last live run. Do not invent a new
   persona; that breaks comparability.
3. **No peeking.** Do not open the ground-truth file for this faculty until step 5.
4. **Run the skill arm live**: follow `find-university-chairs/SKILL.md` end-to-end
   with real `WebSearch`/browse calls. Save the output MAP to
   `dist/live-validation/<faculty>-skill.md` (overwrite the prior run; git history
   keeps the old one).
5. **Score against ground truth** (`skills/tests/eval_ground_truth/README.md`):
   - **Recall** = ground-truth chairs surfaced / total ground-truth chairs.
   - **Precision** = surfaced options judged relevant / total surfaced options
     (see the README's "What precision means here" section, added in Roadmap-K).
6. **Compare to the last recorded run** for this faculty (check
   `2026-06-28-I-fix-revalidation.md` or the most recent runbook entry below) — did
   the change move recall/precision up, down, or leave it flat?
7. **Record the result** as a dated entry appended to the log at the bottom of this
   file. One paragraph: what changed, faculty, recall, precision, delta vs. last run,
   one honest note if something broke.

## Skip list (things the full protocol requires that this one doesn't)

- All 4 faculties — pick one relevant to the change.
- A fresh baseline (no-skill) arm — only needed when re-validating the
  skill-vs-plain-Claude claim itself, not after a routine skill edit.
- A full findings doc — a log entry here is enough; only write a new
  `findings/no_db_universal_skill/<date>-*.md` if the result changes the Phase gate
  verdict (e.g. recall drops below 70%).

## Log

*(append one entry per re-validation run; newest first)*

- No runs yet — this runbook was created 2026-07-02 (Roadmap-J) but not yet
  exercised. Next skill-affecting change should produce the first entry here.
