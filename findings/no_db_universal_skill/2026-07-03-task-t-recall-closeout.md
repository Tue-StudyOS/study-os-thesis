# Task T — Eval-protocol fix + hard-faculty recall closeout

- **Date:** 2026-07-03
- **Branch:** `feat/no-db-universal-skill`
- **Type:** Eval-harness fix + two hard-faculty runs. One skill-adjacent finding
  surfaced (no skill file changed this task).
- **Inputs / reads:** [`2026-07-03-core-done-go-no-go.md`](2026-07-03-core-done-go-no-go.md),
  [`2026-07-02-live-eval-runbook.md`](2026-07-02-live-eval-runbook.md),
  `skills/tests/eval_ground_truth/README.md` + `humanities.md` + `law.md`.

---

## What was done

1. **Protocol fix (committed).** The runbook built test personas from the eval
   README's lossy one-line sample-interest summaries. Reconciled runbook steps 2–3:
   the persona is now built from each GT file's **full `Sample interest:` line**,
   extracted via `grep` (which does not reveal the chair list), with an explicit
   no-peeking carve-out for that single line. This is the documented root cause of the
   Humanities 60%. Eval-harness fix, not a skill change.
2. **Law — genuinely blind run** under the corrected protocol.
3. **Humanities — corrected re-score** (transparent; this conversation is un-blind on
   Humanities, so it is a re-score of the saved blind map, not a fresh blind run).

## Results

| Faculty | Hardness axis | Recall | Precision | Note |
|---|---|---|---|---|
| **Humanities** (corrected re-score) | deep Faculty→FB5→Seminar drill-down | **5/5 = 100%** | 5/5 = 100% | was 3/5; both misses were dropped-clause artifacts |
| **Law** (blind) | dense German public-law chair-title formulas | **3/5 = 60%** | 3/3 = 100% | discovery found all 5; downstream filter miss (Remmert, Saurer) |

### Humanities — protocol fix validated
Both prior misses flip to Include under the full sample interest:
- **Corcilius** — excluded by a "historical exegesis / no contemporary debate" no-go
  that existed only because the README one-liner dropped *"…an interest in the history
  of the field (ancient philosophy, Kant / German Idealism)."* Restore the clause → no-go
  gone → Include.
- **Döring** — excluded as "ethics/emotion, not cognitive science"; the full sample
  interest explicitly lists *"theory of emotions"* → direct match → Include.

The entire Humanities 60% was a lossy-README artifact. Discovery had it right on the
first blind pass (all 5 reached and enumerated).

### Law — a real skill finding (not a GT artifact)
Discovery recall was 5/5 — Pass 1 enumerated all five GT chairs. The 60% is a
**downstream filtering** miss: Remmert and Saurer were excluded at the §5
topical-justification step **without Pass-2 enrichment**, from a surface reading of
their dense multi-strand chair titles.

- **Remmert** — post-scoring enrichment shows her actual Schwerpunkte include
  **"Allgemeine Grundrechtslehren"** (fundamental-rights doctrine) with current
  constitutional work (GG commentary, Art. 12 GG, 2026) — a squarely-core match to the
  persona's constitutional-law + human-rights strands. Her title's *distinguishing*
  strands (Öffentliches Wirtschaftsrecht, Kommunalrecht) read economic/municipal, so a
  title-only judgment drops her; her research does not. **Genuine false-negative.**
- **Saurer** — the more defensible exclusion (Umwelt-/Infrastrukturrecht +
  Rechtsvergleichung; current focus Klimaschutzrecht; tech-touch is energy-regulation).
  Comparative-public-law method is borderline; GT counts him relevant.

Had the skill enriched Remmert before excluding, recall would be ≥4/5 = **80%**. The
gap: **§5 has no *enrich-before-exclude* rule** for a public-law chair whose multi-strand
title contains a core-interest term. This is exactly the hardness `law.md` was designed
to probe ("map constitutional law onto dense German formulas"), and the skill's
profile→query mapping partially failed it. Precision stayed 100% — the filter
under-included, it did not over-include.

## §4 criterion 1 — where we stand now

Six faculties now have a live recall number:

| Faculty | Recall | ≥80%? |
|---|---|---|
| CS | 100% | ✅ |
| Medicine | ≥83% | ✅ |
| Psychology | ≥83% | ✅ |
| WiSo | ≥83% | ✅ |
| Humanities (hard) | 100% | ✅ |
| Law (hard) | 60% | ❌ |

- **≥6 faculties measured:** ✅ now 6 (was 5).
- **≥1 hard faculty ≥80%:** ✅ Humanities 100%.
- **Strict per-faculty reading (each of ≥6 clears 80%, adopted in the go/no-go):**
  ❌ — only **5 of 6** clear 80%; Law is at 60%.

## Verdict: **NO-GO still — but transformed.**

The **original** blocker is resolved: the Humanities 60% is gone (100% under the fixed
protocol), and the go/no-go's central hypothesis (the miss was protocol, not skill) is
decisively confirmed. But the blind Law run did what a good eval should — it surfaced a
**new, genuine, narrower** recall defect (§5 enrich-before-exclude on dense multi-strand
chair titles → Remmert false-negative). Under the strict per-faculty reading the go/no-go
adopted, 5 of 6 faculties clear 80% and Law does not, so criterion 1 is not yet met.

Declaring GO now would repeat the project's prior premature-GREEN failure mode on a
freshly-measured faculty sitting at 60% with a diagnosed, fixable defect. There is still
no schedule pressure (Phase 2 is GREEN). Close the gap properly.

## Named next task — Task U

> **Task U — §5 enrich-before-exclude fix + Law re-run.**
> (1) Add a rule to `references/search-strategy.md` §5: do **not** exclude a candidate at
> the topical-justification step when its own title/listing names a core-interest field
> (even amid off-interest strands) **without first running Pass-2 enrichment** on its
> actual research focus. This is the dual of the Butz worked example: §5 currently guards
> against *over*-inclusion by co-location; it needs the symmetric guard against
> *under*-inclusion by title-surface. (2) Re-run Law blind under the fixed skill; expect
> Remmert to surface (→ ≥80%), reconsider Saurer. (3) If Law clears 80%, all 6 faculties
> clear the bar → flip the §4 go/no-go to **GO**.
> **This is a skill change** → `python3 -m pytest -q` and
> `python3 scripts/build_skill_release.py` must be green.
