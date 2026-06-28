# Tübingen Core — Optimization Roadmap

- **Date:** 2026-06-28
- **Branch:** `feat/no-db-universal-skill`
- **Purpose:** Make the university-discovery core (Tübingen) not just *pass the
  gate* but genuinely *work well*. This is the plan from "it runs" to "it's good."
- **Read with:** [build-plan](2026-06-26-build-plan.md) ·
  [live-validation-protocol](2026-06-28-live-validation-protocol.md) ·
  STATUS.md

---

## 1. What we have today

| Asset | State | Quality note |
|---|---|---|
| `build-student-profile` | done | One-question interview discipline + no-search gate. Not yet stress-tested live. |
| `find-university-chairs` SKILL | done | Faculty-agnostic, 6-dim gate, two-pass search, MAP output, coverage caveat, no DB. Solid design. |
| `search-strategy.md` | done | Real IP: profile→query mapping, faculty routing, ~18 skeletons, filters, dedup, no-go, 2 worked examples. |
| `tuebingen-faculty-backbone.md` | done | 19 official URLs, all 7 faculties + ZITh. **Not yet audited for drill-down depth.** |
| eval ground truth | 4 faculties | Med / Psych / WiSo / CS — the *structurally easy* faculties. Recall-only metric. |
| harness | fixture mode | Plumbing works; **fixture eval is circular** (Task H). Live runner needs Codex. |
| Task I (live validation) | in progress | First *real* recall + real baseline. Tells us where the actual gaps are. |

**Honest status:** the design is good and complete; the *empirical proof* is
pending Task I. Everything below is sequenced so it can be driven by what Task I
reveals, not by guesswork.

---

## 2. What "optimal core" actually means — the quality levers

The core is good when it scores well on five independent axes:

1. **Recall** — finds the relevant chairs (vs. silent gaps).
2. **Precision** — surfaced chairs are actually relevant (vs. noise/over-surfacing).
3. **Steering** — the profile genuinely changes the output (vs. same answer for
   everyone = no advantage over plain Claude).
4. **Output usefulness** — honest pros/cons, concrete conversation starters, dated
   evidence, the coverage caveat.
5. **Robustness** — holds up on hard faculties (humanities/theology/law),
   interdisciplinary interests, shallow profiles, and niche topics with no match.

Task H only ever (circularly) touched recall. The other four axes are untested.

---

## 3. The plan — prioritized tracks

Ordering principle: **first make "works" truly measurable, then fix whatever the
measurement exposes.** Don't optimize blind.

### Track 1 — Close the validation loop (highest priority)

- **Task I (running):** real live recall + real baseline on the 4 faculties.
  *Gate input.*
- **Task J — Lightweight live-eval runbook.** Since fixture mode is invalid and
  live manual runs are the only honest option, write a tight checklist so a single
  faculty can be re-validated cheaply after any skill change. Without this, every
  optimization is unmeasurable.
- **Task K — Add a precision metric.** Recall alone rewards over-surfacing. Add:
  precision = relevant surfaced / total surfaced, and a combined view. Update the
  ground-truth README.

### Track 2 — Optimize recall (after Task I shows the real number)

- **Task L — Backbone audit & repair.** Verify every faculty listing URL actually
  drills down to a complete chair list; fix coarse/dead ones; add sub-department
  pages where the top page is too shallow. The backbone is the anti-SEO floor — if
  it's incomplete, recall caps out no matter how good the queries are.
- **Task M — Weak-web-presence fallback.** Add the known silent-gap mitigations to
  `search-strategy.md`: Vorlesungsverzeichnis, faculty research reports / FIS,
  Fachschaft lists, institute staff directories. Target the chairs Google misses.
- **Task N — Query-skeleton iteration.** From Task I logs, drop dead queries and
  add the patterns that actually surfaced chairs.

### Track 3 — Optimize precision & steering

- **Task O — Relevance/no-go tightening.** Based on observed over-surfacing
  (Task H noted only ~33–40% high-relevance for non-CS), sharpen the relevance
  filter and no-go exclusion so the map is signal, not a long list.
- **Task P — Steering proof.** Run one faculty with two *different* personas and
  confirm the outputs diverge appropriately. If they don't, the interview adds
  nothing — fix the profile→query mapping. This directly defends the
  "better than plain Claude" claim.

### Track 4 — Robustness (hardening the core)

- **Task Q — Hard-faculty ground truth.** Extend ground truth to the structurally
  harder faculties (Humanities, Theology, Law) and one interdisciplinary persona
  spanning 2–3 faculties. The current 4 are the easy, well-structured ones.
- **Task R — Edge-case behavior.** Validate honest behavior on: a niche topic with
  no Tübingen match (does it say so?), a shallow/resistant student (does the gate
  hold?), an interdisciplinary interest (does routing pick all relevant faculties?).
- **Task S — Output & interview quality pass.** Review live transcripts for honest
  pros/cons, concrete conversation starters, dated evidence, caveat presence, and
  interview convergence. Add few-shot examples only where live runs repeatedly fail.

### Track 5 — Then, and only then

- Portability spot-check (Codex / other clients) — Phase 3 concern.
- **Phase 2 (companies)** — start only after the university core clears its
  *live* gate with good recall, precision, and proven steering.

---

## 4. Definition of "core is done"

The Tübingen core is optimal-enough to move on when, **measured live**:

- recall ≥ 80% across ≥6 faculties (incl. at least one hard faculty),
- precision is high enough that the map is not padded with noise,
- two different personas on the same faculty produce demonstrably different maps
  (steering proven),
- output is consistently honest and actionable (pros/cons, starters, dated
  evidence, caveat),
- edge cases degrade gracefully (says "no good match" when true; gate holds on
  shallow profiles).

These are stricter than the original ≥70% recall gate on purpose: the goal now is
"optimal core," not "passes."

---

## 5. Critical path / dependencies

```text
Task I (live numbers) ──► Task J (runbook) ──► everything else is measurable
        │
        ├─ recall low?     → Track 2 (backbone, fallback, queries)
        ├─ precision low?  → Track 3 (relevance/no-go)
        ├─ no steering?    → Track 3 (Task P) — most important for the thesis claim
        └─ all decent?     → Track 4 (hard faculties, edge cases) → done → Phase 2
```

Task I is the fork. Until its honest numbers land, treat Tracks 2–4 as *prepared
but not started* — we point the optimization at whatever Task I proves weakest.
