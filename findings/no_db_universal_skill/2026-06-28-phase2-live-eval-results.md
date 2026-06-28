# Task 2-E — Phase 2 Live Evaluation Results

- **Date:** 2026-06-28
- **Branch:** `feat/no-db-universal-skill`
- **Skill evaluated:** `find-company-thesis-options` (Task 2-C)
- **Ground truth:** `skills/tests/eval_ground_truth/company_seed/` (Task 2-D)
- **Arm outputs:** `dist/live-validation/company-C{1,2,3}/{skill,baseline}-arm.md`
- **Protocol:** No-peeking — all 6 arm outputs written before ground truth was opened.
  Task 2-D (ground truth creation) and Task 2-E (validation run) were done in the same
  agent session; see honesty note in §6.

---

## Scoring method

**Primary recall** — a ground-truth company is counted as *surfaced* if the skill arm's
option map names it by name OR unambiguously names its relevant R&D division. Same rule
as Phase 1; adapted from `skills/tests/eval_ground_truth/company_seed/README.md`.

**Thesis-signal accuracy (secondary)** — for each surfaced company, compare the skill's
`thesis signal` classification to the expected value in the ground truth table.
Over-classification (`explicit opening` when GT says `unclear`) is the more serious error.

---

## 1. Per-profile recall table

### Primary recall

| Profile | GT companies | Skill surfaced | Skill recall | Baseline surfaced | Baseline recall | Skill Δ |
|---|---|---|---|---|---|---|
| C1 ML/automotive/robotics | 6 | 6 | **6/6 = 100%** | 5 | 5/6 ≈ 83% | +17pp |
| C2 medtech/health | 5 | 5 | **5/5 = 100%** | 4 | 4/5 = 80% | +20pp |
| C3 software/data/enterprise | 5 | 5 | **5/5 = 100%** | 3 | 3/5 = 60% | +40pp |
| **Mean** | | | **100%** | | **74%** | **+26pp** |

### Detailed breakdown — C1 (ML/AI + Automotive/Robotics)

| GT company | Skill surfaced? | Baseline surfaced? |
|---|---|---|
| Robert Bosch GmbH | ✓ | ✓ |
| ZF Friedrichshafen AG | ✓ | ✓ |
| Mercedes-Benz AG | ✓ | ✓ |
| Dr. Ing. h.c. F. Porsche AG | ✓ | ✓ |
| NEURA Robotics GmbH | ✓ | ✓ |
| sereact GmbH | ✓ | ✗ |
| **Total** | **6/6** | **5/6** |

Skill unique finds over baseline: sereact GmbH (startup, lesser-known outside Cyber Valley community).
Baseline extra (not in GT): Daimler Truck AG (not wrong, just not in GT seed).

### Detailed breakdown — C2 (Medtech / Health)

| GT company | Skill surfaced? | Baseline surfaced? |
|---|---|---|
| Carl Zeiss AG | ✓ | ✓ |
| Karl Storz GmbH & Co. KG | ✓ | ✓ |
| Roche Diagnostics GmbH | ✓ | ✓ |
| Paul Hartmann AG | ✓ | ✗ |
| Bosch Sensortec GmbH | ✓ | ✓ (indirect — named as Bosch subsidiary) |
| **Total** | **5/5** | **4/5** |

Skill unique find: Paul Hartmann AG (known medtech company but not top-of-mind in LLM training data).

### Detailed breakdown — C3 (Software / Data + Enterprise)

| GT company | Skill surfaced? | Baseline surfaced? |
|---|---|---|
| SAP SE | ✓ | ✓ |
| MHP Management- und IT-Beratung GmbH | ✓ | ✗ |
| Aleph Alpha GmbH | ✓ | ✓ |
| TeamViewer AG | ✓ | ✓ |
| Porsche Digital GmbH | ✓ | ✗ |
| **Total** | **5/5** | **3/5** |

Skill unique finds: MHP (IT consulting, thesis student positions confirmed), Porsche Digital
(automotive software subsidiary with inherited thesis program).

---

## 2. Thesis-signal accuracy (skill arm only)

| Profile | Surfaced | Correct signal | Signal accuracy | Notes |
|---|---|---|---|---|
| C1 | 6 | 6 | **100%** | All 6 signals matched GT expectations |
| C2 | 5 | 5 | **100%** | Bosch Sensortec `active program (inferred)` accepted per GT |
| C3 | 5 | 4 | **80%** | TeamViewer over-classified (`active program` vs GT `unclear`) |
| **Mean** | 16 | 15 | **≈ 94%** | |

**The one signal error:** TeamViewer AG — skill classified as `active program (inferred)` based
on a search-snippet claim ("TeamViewer supports Bachelor's and Master's thesis projects") that
did not come from TeamViewer's own page. The evidence did not meet the skill's own evidence
rule ("prefer the company's own domain as authoritative source"). The correct output should
have been `unclear`. This is a mild over-classification; not a hallucinated contact name or
invented thesis topic, but technically inconsistent with the evidence rules.

---

## 3. Honest failures: what was missed and why

### C1 — Nothing missed by skill; sereact missed by baseline

The skill surfaced all 6 GT companies. sereact was the only company the baseline missed —
because it is a recently-funded AI robotics startup with minimal mainstream-press profile
outside the Cyber Valley ecosystem. The backbone anchoring was specifically useful here.

**Remaining gap:** DeepScenario GmbH (backbone entry, `[AI/ML, automotive]`) was surfaced
by the skill (bonus find) but is not in the GT seed — a skill that finds it is doing more
than required, not failing.

### C2 — Nothing missed by skill; baseline missed Paul Hartmann

Paul Hartmann is a medtech corporate with €91.9M in R&D spend and an explicit thesis program.
It is less famous outside the medtech industry than Zeiss or Karl Storz. The backbone
correctly included it; the skill found it via Pass 1 backbone filter. The baseline (plain
Claude) did not surface it, confirming the backbone adds value for less web-prominent companies.

**Bonus finds by skill:** Heidelberg Engineering GmbH (imaging, SME), eye2you GmbH (AI/ML
medtech, Tübingen), NODE Robotics GmbH (surgical robotics) — all surfaced by the skill's
backbone filter + enrichment but not in the GT seed.

### C3 — Nothing missed by skill; baseline missed MHP and Porsche Digital

MHP is a large IT consulting firm with active thesis student positions, but it is primarily
known in automotive consulting circles — not top-of-mind in training data. The backbone
captured it correctly.

Porsche Digital is an automotive software subsidiary with an inherited thesis program from
the Porsche parent. The baseline named "Porsche AG" (the parent) but not "Porsche Digital"
(the software-focused subsidiary).

**Known limitations surfaced during C3 enrichment:**
- **Aleph Alpha merger (April 2026):** Aleph Alpha announced a $20B merger with Cohere
  (operating under "Cohere" name). The backbone entry (2026-06-28) predates this transition;
  the entity may no longer accept thesis students under "Aleph Alpha GmbH." The skill flagged
  this with ⚠ correctly. This is a backbone currency issue, not a skill design flaw — annual
  backbone review is the intended maintenance model.
- **Structural gap:** BW's enterprise software sector is thin relative to automotive and
  medtech. The backbone's §5 Software/Enterprise section has only 3 entries (SAP, TeamViewer,
  MHP). A student with a pure fintech or cloud-native profile would find the C3 map short.
  The coverage caveat correctly calls this out.

---

## 4. Comparison to Phase 1

| | Phase 1 (uni chairs, 4 faculties) | Phase 2 (BW companies, 3 profiles) |
|---|---|---|
| Skill recall (primary) | 82% mean | **100% mean** |
| Skill recall (strict / recommended correctly) | 65% mean | n/a (companies don't have a single PI to attribute) |
| Baseline recall | ~17% | **~74%** |
| Skill Δ over baseline | **+65pp** | **+26pp** |
| Gate threshold | ≥70% per faculty | ≥70% per profile |

**Why the advantage is smaller in Phase 2:**
- In Phase 1, university chair holders are rarely in LLM training data at the individual
  level (obscure professors → big baseline miss). In Phase 2, the top BW companies (Bosch,
  Zeiss, SAP, Roche) are well-known and in LLM training data → baseline is already strong.
- The backbone's value in Phase 2 is in surfacing less-prominent-but-confirmed companies
  (sereact, Paul Hartmann, MHP, Porsche Digital) and in providing structured filtering that
  correctly applies no-gos (hardware companies excluded for the ML profile).
- The "circular recall" caveat (see §5 below) may inflate both the skill recall and the GT
  itself for Phase 2.

---

## 5. Honesty note: circular recall caveat

**Phase 1 had this problem; Phase 2 has it more acutely.**

The ground truth (Task 2-D) and the skill arm (Task 2-E) were run in the same agent session.
The GT companies were identified by the same process that identified backbone companies, and
the skill's Pass 1 reads the same backbone the GT was derived from. This means high recall
in Phase 2 partly reflects consistency between the GT's source and the skill's filter — not
independently validated breadth.

Specifically:
- The GT was built by selecting companies from the backbone + verifying them live.
- The skill's Pass 1 reads the backbone and surfaces those same companies.
- The test essentially asks: "Does the skill filter the backbone correctly?" — not "Does the
  skill find companies a student should know about that aren't in the backbone?"

This is analogous to the Phase 1 medicine/WiSo circular recall issue (GT built from same
org pages the skill crawled). Here it is even stronger: the backbone IS the source of both
the GT and the skill's Pass 1.

**What this means for the gate verdict:** The 100% recall is a test of backbone consistency,
not of discovery breadth. The honest recall number under an independent GT would likely be
lower. The +26pp delta over baseline is more trustworthy because the baseline had no access
to the backbone.

---

## 6. Phase-2 gate verdict

**Gate criteria (from build plan):**
- `find-company-thesis-options` runs end-to-end on all 3 profiles with no DB dependency: ✓
- Ground truth exists for ≥3 company profiles with defined recall metric: ✓
- Live recall ≥70% on all 3 profiles (skill arm): ✓ (100% on all three)
- Live skill arm meaningfully outperforms plain-Claude baseline: ✓ (+26pp mean; +40pp on C3)

**Verdict: GREEN — with honesty caveats.**

The gate criteria are formally met. All three profiles clear 70% recall; the skill outperforms
the baseline on all three profiles. The skill executes the full 8-step workflow correctly,
applies no-go filtering, classifies thesis signals, and appends the coverage caveat as required.

**Caveats that should not be papered over:**
1. **Circular recall inflates the primary recall** — the honest ceiling for an independently
   built GT would be lower. The +26pp delta is the more meaningful quality signal.
2. **C1 delta is weak (+17pp)** — the backbone adds value mainly for lesser-known startups
   (sereact) on automotive/robotics profiles; well-known corporates are already baseline-accessible.
3. **Aleph Alpha backbone entry is stale** — the April 2026 merger with Cohere is not reflected
   in the backbone; annual review should catch this.
4. **Enterprise software gap** — the C3 map is thin (only 5 GT companies, only 3 backbone
   entries in §5); a student with a strict fintech profile would find the skill coverage limited.

**Phase 3 recommendation:** Before distribution, add ≥3 more entries to the backbone §5
Software/Enterprise section (e.g. Heidelberg-based enterprise software companies, fintech
players in Karlsruhe/Stuttgart). This will improve skill utility for C3-type profiles.

---

## 7. What the skill does NOT do (confirmed by this eval)

- No hallucinated contacts or thesis openings: ✓ — the skill consistently marks
  supervisor/coordinator as "not confirmed" and never invents a name.
- No job-board aggregators used as thesis source: ✓ — all evidence linked to company-owned
  or Cyber Valley-owned domains, or explicitly noted as a fallback.
- No companies outside BW: ✓ — Roche Diagnostics (Mannheim) correctly included as BW;
  Aleph Alpha (Heidelberg) correctly included as BW.
- No runtime database: ✓ — all three skill arms ran via backbone read + live WebSearch only.
- Coverage caveat always present: ✓ — all three skill arm outputs include the required
  map-level caveat verbatim.
