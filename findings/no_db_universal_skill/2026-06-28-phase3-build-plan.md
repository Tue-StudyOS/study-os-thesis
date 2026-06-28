# Phase 3 — Orchestration & Distribution: Build Plan

- **Date:** 2026-06-28
- **Branch:** `feat/no-db-universal-skill`
- **Read first:** [MASTERPLAN.md §7](../../MASTERPLAN.md), [STATUS.md](../../STATUS.md)
- **Phase 1 results:** [2026-06-28-live-eval-results.md](2026-06-28-live-eval-results.md) (GREEN after I-fix)
- **Phase 2 results:** [2026-06-28-phase2-live-eval-results.md](2026-06-28-phase2-live-eval-results.md) (GREEN)

Both Phase 1 (university discovery) and Phase 2 (company discovery) are GREEN. Phase 3
focuses on making the two-skill system usable and distributable — not on adding new discovery
capability.

---

## Key decisions

### Decision 1 — Orchestration: thin entry-point skill, not a wrapper pipeline

**Options considered:**
- A: No new skill — rely on prose documentation ("run build-student-profile, then pick a track")
- B: A thin `thesis-finder/SKILL.md` orchestrating entry point
- C: A heavyweight multi-agent pipeline skill

**Decision: B (thin entry point).** A single invocable entry point ("run thesis-finder") is
cleaner for distribution — students shouldn't need to know three skill names to use the system.
The entry point is intentionally thin: it checks for a profile, asks which track(s) the student
wants, and delegates to the existing skills. No duplication of discovery logic.

**What the entry point does NOT do:** It does not merge or re-format the option maps from both
tracks. Each discovery skill already produces a self-contained, student-readable map. Running
both and receiving two maps is the correct combined output — merging would require re-ranking
across very different option types (chairs vs. companies) with no principled basis.

### Decision 2 — Backbone fixes before distribution

Two known issues from the Phase 2 eval (§3 caveats) must be fixed before distributing:

1. **Aleph Alpha entry stale:** Aleph Alpha GmbH merged with Cohere in April 2026 (operating
   under the "Cohere" brand). The backbone entry must be updated to reflect this transition
   so the skill does not mislead students applying to a defunct entity.
2. **§5 Software/Enterprise gap:** Only 3 entries (SAP, TeamViewer, MHP). A C3-type profile
   (software/data/enterprise) gets a thin backbone slice. Add ≥3 more BW software/enterprise
   companies before distribution. Candidates: IONOS Group (Karlsruhe), Haufe Group (Freiburg),
   Schwarz IT (Neckarsulm), GFT Technologies (Stuttgart), Fiducia & GAD IT (Karlsruhe).

### Decision 3 — Distribution channels

MASTERPLAN §7 names: Fachschaft Informatik, Hennig-GitHub, Ersti-Heft, and ideally the
university's "How to find a thesis" pages.

**Distribution deliverables for Phase 3:**
- A clear student-facing `README.md` at repo root (already exists but written for developers;
  update for students)
- `AGENTS.md` updated to include `find-company-thesis-options` in the student workflow and
  skill responsibility table, and `thesis-finder` as the new entry point
- No PDF, no separate website — the GitHub repo *is* the distribution artifact

**What "distribution" does NOT mean for Phase 3:** We do not execute the actual handoff to
Fachschaft, Hennig, or Ersti-Heft editors. That requires human coordination outside this
conversation. Phase 3 produces the artifacts that make handoff possible; the handoff itself
is a post-Phase-3 action.

### Decision 4 — Eval strategy for Phase 3

Phase 1 and Phase 2 discovery accuracy is already measured (both GREEN). Phase 3's "eval"
is an end-to-end smoke test:
- Take one sample profile (C1: ML/automotive)
- Trace through `thesis-finder` → both tracks → confirm step sequencing is coherent
- Confirm no step produces an error condition or requires skill-file content that doesn't exist
- Document the trace result honestly

No new precision/recall measurement. The smoke test is qualitative; a pass means
"the flow works as documented."

---

## Scope boundary

Phase 3 does NOT include:

- New discovery capability (that is Phase 1/2)
- Eval harness extension or CI changes
- Coverage of universities outside Tübingen or companies outside BW
- Backbone refresh beyond the two identified stale/gap issues
- Institutional approval or actual posting to distribution channels
- Thesis write-up (separate phase, after this one)

---

## Task table

| Task | Goal | Depends on | Est. effort |
|---|---|---|---|
| 3-A | Backbone maintenance (Aleph Alpha fix + §5 expansion) | nothing | small |
| 3-B | Create `skills/thesis-finder/SKILL.md` entry point | 3-A | small |
| 3-C | Update `AGENTS.md` + `README.md` for distribution | 3-B | small |
| 3-D | End-to-end smoke test + STATUS.md update | 3-B, 3-C | small |

All tasks are sequential; no parallel-safe pairing here.

---

## Task 3-A — Backbone Maintenance

**Goal:** Fix two known backbone issues before distribution so students receive accurate
company data.

**Files to edit:**
- `skills/find-company-thesis-options/references/bw-company-backbone.md`

**Changes:**

1. **Aleph Alpha entry (§1 AI/ML):** Update the entry to note the April 2026 merger.
   - Change the entry to: `Cohere (formerly Aleph Alpha GmbH)` or mark Aleph Alpha as
     `⚠ transitioning — see note` and add a brief caveat row/footnote. The company still
     has a Heidelberg presence (now as Cohere's German entity) but the "AlephAlpha" careers
     URL is likely stale.
   - Do not delete the entry — Cohere/Aleph Alpha remains a relevant BW AI actor; update it
     so students know the correct name to contact.

2. **§5 Software/Enterprise expansion:** Add ≥3 verified BW enterprise software entries.
   Suggested additions (verify each URL resolves to R&D or careers content before adding):
   - IONOS Group SE (Karlsruhe) — cloud/hosting, student thesis program
   - Haufe Group GmbH & Co. KG (Freiburg) — HR/legal/finance software, active student program
   - GFT Technologies SE (Stuttgart) — fintech + digital banking transformation software
   - Fiducia & GAD IT AG (Karlsruhe) — banking IT for cooperative banks, large R&D arm
   - Schwarz IT GmbH & Co. KG (Neckarsulm) — retail/supply-chain IT (Lidl/Kaufland IT arm)
   - (Pick ≥3 of the above; add all if all URLs verify live.)
   - Update the spot-check log with any verified URLs.

**Done-when:**
- Aleph Alpha entry updated with accurate entity name and merger note
- §5 Software/Enterprise has ≥6 total entries
- Any new entries added have a URL spot-checked
- Preamble `Compiled:` date updated to 2026-06-28 (already correct) + a note added that this
  revision adds Phase-3 gap fills

**Commit:** `fix(backbone): update Aleph Alpha entry post-merger; expand §5 software/enterprise`

---

## Task 3-B — Create `thesis-finder/SKILL.md` Entry Point

**Goal:** A thin orchestrating skill that is the single command a student or agent invokes
to start the thesis-finding workflow.

**Files to create:**
- `skills/thesis-finder/SKILL.md`

**Behavior the skill encodes:**
1. Check whether a 6-dimension student profile (build-student-profile output) is already in
   context. If not, defer: "Run `build-student-profile` first, then return here."
2. Once a complete profile is confirmed, ask one question: "Which option type do you want to
   explore? (a) University thesis at Tübingen, (b) Company thesis in Baden-Württemberg,
   (c) Both."
3. Route accordingly:
   - (a) → invoke `find-university-chairs`
   - (b) → invoke `find-company-thesis-options`
   - (c) → invoke both in sequence; present the university option map first, then the company
     option map, separated by a clear section header. No cross-ranking between the two.
4. After either or both maps are delivered, offer the optional next step: "`draft-thesis-contact`
   can draft a first-contact email for any option you choose."

**Structure:** Single `SKILL.md` file, no `references/` subfolder needed. Keep it ≤50 lines.
This skill adds routing only — no discovery logic lives here.

**Evidence rules:** None new. The skill delegates entirely to the two discovery skills; their
evidence rules apply.

**Done-when:**
- `skills/thesis-finder/SKILL.md` exists
- A reviewer can trace the routing logic for all three student choices without ambiguity
- The file references `build-student-profile`, `find-university-chairs`,
  `find-company-thesis-options`, and `draft-thesis-contact` by their exact skill folder names
- No discovery logic duplicated from either discovery skill

**Commit:** `feat(3-B): add thesis-finder entry-point skill`

---

## Task 3-C — Update `AGENTS.md` and `README.md`

**Goal:** Bring the two maintainer/agent-facing documents up to date with the Phase 2 and
Phase 3 additions, and make the root `README.md` useful for students who find the repo.

**Files to edit:**
- `AGENTS.md` — student workflow section + skill responsibility table
- `README.md` — student-facing overview

**AGENTS.md changes:**
1. **Student Workflow section:** Replace the outdated 5-step list (which references retired
   `match-thesis-advisors`) with the current flow:
   ```
   1. thesis-finder  (entry point — or invoke skills individually)
   2. build-student-profile
   3. find-university-chairs  (university track)
      find-company-thesis-options  (company track)
      (both may be run in sequence)
   4. draft-thesis-contact  (optional final step)
   ```
2. **Skill Responsibilities section:** Add a new entry for `find-company-thesis-options`
   (intent, inputs, outputs, guardrails) and `thesis-finder` (intent, inputs, outputs).
   Remove or archive the `match-thesis-advisors` and `update-openalex-paper-index` entries
   (both skills are retired from the student-facing flow; note this explicitly).

**README.md changes:**
- Write a brief student-facing overview (≤200 words) explaining:
  - What this is (thesis-option discovery for Tübingen/BW, no login or database)
  - How to use it (run in any capable coding agent — Claude Code, Codex, Gemini CLI; invoke
    `thesis-finder` to start)
  - What it gives you (a map of university chairs or BW companies relevant to your profile)
  - What it does NOT do (write the thesis, guarantee openings, act as an official portal)
- Keep the existing technical context below a fold/separator; the student overview goes first.

**Done-when:**
- AGENTS.md student workflow matches the current skill set
- `find-company-thesis-options` and `thesis-finder` are documented in AGENTS.md skill table
- Retired skills (`match-thesis-advisors`, `update-openalex-paper-index`) are removed from the
  student-facing workflow (leave their `### match-thesis-advisors` section text with a
  *(retired)* note rather than deleting, so git history context is preserved)
- README.md has a clear student-facing top section

**Commit:** `docs(3-C): update AGENTS.md workflow + README for distribution`

---

## Task 3-D — Smoke Test + STATUS.md Update

**Goal:** Verify the full flow works end-to-end on paper; update STATUS.md to close Phase 3.

**No new files required** — document the trace in STATUS.md log and in a brief note in
`findings/no_db_universal_skill/2026-06-28-phase3-smoke-test.md`.

**Smoke test protocol:**
1. Take the C1 profile (ML/AI + automotive/robotics, no hardware no-go).
2. Trace through `thesis-finder`: profile check passes → student selects "both" → skill
   routes to `find-university-chairs` first, then `find-company-thesis-options`.
3. For the university track: confirm the skill file's prerequisite check passes; confirm
   Pass-1 (backbone crawl) would route to CS/ML faculty; confirm option map structure.
4. For the company track: confirm Pass-1 (backbone filter) would select ML/automotive entries
   from §1–§2 of bw-company-backbone.md; confirm thesis-signal labeling applies.
5. Confirm neither skill produces a dead reference (read the two SKILL.md files + check all
   referenced `references/` files exist).
6. Document: what worked, what was verified, any gap found.

**Done-when:**
- Smoke test trace documented (even a brief table of steps is enough)
- No dead references found (or any found are fixed)
- STATUS.md updated: Phase 3 task table added, gate verdict stated
- STATUS.md log entry for 2026-06-28 Phase 3 completion
- Branch is in a coherent, committable state

**Commit:** `docs(3-D): add phase3 smoke test + update STATUS`

---

## Phase 3 gate criteria

- Backbone: Aleph Alpha entry corrected; §5 has ≥6 entries ✓/✗
- `thesis-finder/SKILL.md` routes correctly for all three student choices ✓/✗
- `AGENTS.md` reflects current skill set (no retired skills in active workflow) ✓/✗
- `README.md` has a student-readable top section ✓/✗
- Smoke test passes with no dead references ✓/✗
- STATUS.md closed with a gate verdict ✓/✗

Gate verdict: GREEN when all six criteria are met; AMBER if README is weak but
functional; RED if the smoke test finds broken references or the orchestrator routes incorrectly.
