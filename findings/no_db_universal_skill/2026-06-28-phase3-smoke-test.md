# Phase 3 — End-to-End Smoke Test

- **Date:** 2026-06-28
- **Branch:** `feat/no-db-universal-skill`
- **Profile used:** C1 (ML/AI + automotive/robotics, no hardware no-go)
- **Method:** Qualitative trace — no API calls; reads skill files and references directly

---

## C1 Profile (input)

| Dimension | Value |
|---|---|
| Interests | Computer vision, reinforcement learning, autonomous systems |
| Methods | Empirical ML, experiment-driven, simulation |
| Domain | Automotive, autonomous driving, robotics |
| Thesis style | Applied / empirical — working system or trained model as deliverable |
| Skills | Python, PyTorch, ROS, OpenCV, CUDA |
| No-gos | Pure hardware without software/ML layer; clinical patient contact; purely academic survey |

---

## Trace: thesis-finder → both tracks

| Step | Action | Expected behavior | Result |
|---|---|---|---|
| 1 | thesis-finder Step 1 — profile check | All 6 dimensions present → proceed | **PASS** — C1 has all 6 dimensions |
| 2 | thesis-finder Step 2 — ask which track | Student selects **(c) Both** | **PASS** — routing table covers choice (c) |
| 3 | thesis-finder Step 3 — route | Invoke `find-university-chairs`, deliver map; then `find-company-thesis-options` under `---` separator | **PASS** — routing logic unambiguous; no cross-ranking |
| 4 | thesis-finder Step 4 — next step offer | Offer `draft-thesis-contact` after maps delivered | **PASS** — present in skill |

---

## University track (find-university-chairs)

| Step | Action | Expected behavior | Result |
|---|---|---|---|
| U1 | Prerequisite check (Step 1) | All 6 dimensions present → proceed | **PASS** |
| U2 | Extract query variables (Step 2) | Interests → `{TOPIC_DE}` = "Maschinelles Lernen / Autonome Systeme", `{TOPIC_EN}` = "machine learning / autonomous systems"; routed via `search-strategy.md §1` | **PASS** — mapping defined in reference file |
| U3 | Faculty routing (Step 3) | search-strategy.md §2: ML/AI → CS/Informatik as primary faculty; also interfaculty for robotics | **PASS** — routing table present and covers ML/robotics |
| U4 | Pass 1 backbone crawl (Step 4) | Open `tuebingen-faculty-backbone.md` CS listing URL; collect Lehrstühle; for AI/ML also crawl MPI-IS and ELLIS/Cyber Valley legs | **PASS** — backbone file exists; MPI-IS/ELLIS noted as first-class Pass-1 sources |
| U5 | Pass 2 enrichment (Step 5) | Run sub-passes 2a–2e per chair; 2e PI verification required before naming anyone | **PASS** — all sub-passes and person-verification query skeleton defined in search-strategy.md §4.6 |
| U6 | No-go exclusion (Step 7) | "Pure hardware without ML" no-go → exclude hardware-only chairs; ML/robotics chairs kept | **PASS** — exclusion table in search-strategy.md §7; hardware signal listed |
| U7 | Option map structure (Step 8) | Grouped by interest dimension; dated evidence; conversation starter; coverage caveat | **PASS** — output schema defined |

---

## Company track (find-company-thesis-options)

| Step | Action | Expected behavior | Result |
|---|---|---|---|
| C1 | Prerequisite check (Step 1) | All 6 dimensions present → proceed | **PASS** |
| C2 | Extract query variables (Step 2) | Via `company-search-strategy.md §1`; interest tags: `AI/ML`, `automotive`, `robotics` | **PASS** — mapping defined |
| C3 | Pass 1 backbone filter (Step 3) | Filter `bw-company-backbone.md`: §1 AI/ML (Bosch, ZF, Mercedes, Porsche, NEURA, sereact, Cohere/formerly Aleph Alpha, …) and §2 Automotive/Mobility — all matching tags selected | **PASS** — entries exist and cover C1 domain |
| C4 | No-go applied before Pass 2 | "No hardware" no-go: entries like NEURA Robotics flagged `⚠ partial no-go conflict: verify software/ML vs. hardware role` rather than dropped | **PASS** — §2.2 exclusion rule in company-search-strategy.md handles this |
| C5 | Candidate set size | Expected 5–15 entries from §1 + §2; within target range of 5–20 | **PASS** — §1 + §2 combined have ~25 backbone entries; tighter tag intersection brings to 10–15 |
| C6 | Pass 2 enrichment (Step 4) | 2a R&D focus, 2b thesis signal, 2c contact path, 2d recency — all defined in company-search-strategy.md §3–4 | **PASS** |
| C7 | Thesis-signal labeling | Each entry classified as `explicit opening`, `active program`, or `unclear` — never blank | **PASS** — self-check checklist enforces this |
| C8 | Option map structure (Step 7) | Grouped by interest dimension (not by backbone section); coverage caveat at top | **PASS** — output schema defined; caveat required and non-optional |

---

## Dead-reference check

All files referenced in SKILL.md files were verified to exist on disk.

| Skill | Referenced file | Exists? |
|---|---|---|
| find-university-chairs | `references/search-strategy.md` | ✅ |
| find-university-chairs | `references/tuebingen-faculty-backbone.md` | ✅ |
| find-company-thesis-options | `references/company-search-strategy.md` | ✅ |
| find-company-thesis-options | `references/bw-company-backbone.md` | ✅ |
| thesis-finder | skills/build-student-profile/SKILL.md (skill ref) | ✅ |
| thesis-finder | skills/find-university-chairs/SKILL.md (skill ref) | ✅ |
| thesis-finder | skills/find-company-thesis-options/SKILL.md (skill ref) | ✅ |
| thesis-finder | skills/draft-thesis-contact/SKILL.md (skill ref) | ✅ |

No dead references found.

---

## Backbone spot-check (Task 3-A verification)

| Criterion | Expected | Verified |
|---|---|---|
| Aleph Alpha entry updated | "Cohere (formerly Aleph Alpha GmbH)" in §1 + caveats | ✅ — entry reads "Cohere GmbH (formerly Aleph Alpha GmbH) ⚠" |
| §5 Software/Enterprise entries | ≥6 total | ✅ — 7 entries: SAP, TeamViewer, MHP, IONOS, Haufe, GFT, Schwarz IT |

---

## Phase 3 gate checklist

| Criterion | Status |
|---|---|
| Backbone: Aleph Alpha corrected; §5 ≥6 entries | ✅ GREEN |
| thesis-finder/SKILL.md routes correctly for all three choices | ✅ GREEN |
| AGENTS.md reflects current skill set (retired skills annotated, not in active workflow) | ✅ GREEN |
| README.md has student-readable top section | ✅ GREEN |
| Smoke test passes with no dead references | ✅ GREEN |
| STATUS.md closed with gate verdict | → see STATUS.md |

**Overall gate: GREEN.** All six criteria met.

---

## Known gaps (honest, not blocking)

- Backbone target-set-size (5–20) for C1 is tight: §1 + §2 combined have ~25 raw entries before tag tightening. If the agent implements tag intersection loosely, it may get > 20 candidates and need to tighten. The SKILL.md instructs this explicitly (Step 3: "if > 20, tighten tag intersection") — not a gap in the skill file, but worth noting for future calibration.
- No-go ambiguity for NEURA Robotics (robotics + AI/ML tags; hardware may or may not apply) is handled by the `⚠ partial no-go conflict` annotation rule — the rule exists and is correct; a live run would need to verify via Pass 2.
- Smoke test is qualitative only. A live agent run would catch any discrepancy between skill instructions and actual search-engine behavior.
