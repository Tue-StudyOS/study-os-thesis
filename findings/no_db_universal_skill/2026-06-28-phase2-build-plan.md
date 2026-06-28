# Phase 2 — Company Discovery: Build Plan

- **Date:** 2026-06-28
- **Branch:** `feat/no-db-universal-skill`
- **Decisions:** see [`2026-06-28-phase2-company-decisions.md`](2026-06-28-phase2-company-decisions.md)
- **Read first:** [MASTERPLAN.md §6](../../MASTERPLAN.md), [STATUS.md](../../STATUS.md)

Phase 1 gate is GREEN. This plan extends the database-less discovery principle to company
thesis options in Baden-Württemberg. Each task is one agent run, ordered by dependencies.

---

## Target skill flow (Phase 2 addition)

```text
build-student-profile      (unchanged — 6-dimension interview)
      |
      v
find-university-chairs     (Phase 1 — unchanged)
      |
      v
find-company-thesis-options   (Phase 2 — new skill)
      |
      v
draft-thesis-contact       (unchanged — optional final step, works for both uni and company)
```

Both discovery skills consume the same 6-dimension student profile. Students may run either
or both, depending on whether they want a university thesis, a company thesis, or both.

---

## Skill to create

`skills/find-company-thesis-options/`  — new skill folder, with:
- `SKILL.md` — the skill entrypoint (Task 2-C)
- `references/bw-company-backbone.md` — the curated company list (Task 2-A)
- `references/company-search-strategy.md` — the profile→query mapping (Task 2-B)

---

## Task 2-A — BW Company Backbone Reference

**Goal:** A curated, tagged Markdown list of ~100–130 BW companies relevant for thesis
discovery — the anti-SEO-bias baseline that plays the same role as
`tuebingen-faculty-backbone.md` in Phase 1.

**Depends on:** nothing. Parallel-safe.

**Files (new):**
- `skills/find-company-thesis-options/references/bw-company-backbone.md`

**Steps:**
1. Retrieve the Cyber Valley Industry Partners list from `cybervalley.de/ecosystem/partners`
   (or equivalent current URL). Record each company name, sector tags, location, and any
   listed URL. This forms the AI/ML backbone (~80–100 entries).
2. Manually add ~20–30 established BW R&D companies from known sources covering:
   - Automotive / mobility: Bosch, ZF Friedrichshafen, Mercedes-Benz R&D (Sindelfingen/Stuttgart)
   - Medtech / health: Carl Zeiss (Oberkochen), Karl Storz (Tuttlingen), B. Braun (Melsungen — note: Hessen, skip unless has BW R&D)
   - Software / enterprise: SAP (Walldorf), Software AG (Darmstadt — note BW-adjacent only)
   - Industrial: Trumpf (Ditzingen), Festo (Esslingen), Kärcher (Winnenden)
   - Energy / sustainability: EnBW (Karlsruhe)
3. For each entry record: company name, sector tags (2–3), size category (startup/SME/corporate),
   BW city, careers/research URL (spot-check it resolves), and a "last verified" date.
4. Spot-check ≥10 entries (mix of Cyber Valley + manual additions): visit the careers/research
   URL and confirm the company has an R&D presence.
5. Create the `skills/find-company-thesis-options/` directory and write the file.

**Done-when:**
- ≥80 entries total; at least 5 non-AI sectors represented
- Each entry has: name, sector tags, size, location, URL, last-verified date
- 10 URLs spot-checked and confirmed to resolve to pages with R&D or careers content
- File is readable as a Markdown table with a brief preamble explaining usage

**Agent prompt:**
```
You are implementing Task 2-A of the Phase 2 company discovery build plan for StudyOS
Thesis-Finder. Branch: feat/no-db-universal-skill.

Read first (for context on what this file must do):
- findings/no_db_universal_skill/2026-06-28-phase2-company-decisions.md (§ Decision 1)
- skills/find-university-chairs/references/tuebingen-faculty-backbone.md (structural template)

Your task: Create skills/find-company-thesis-options/references/bw-company-backbone.md —
a curated Markdown table of ~100–130 BW companies tagged for thesis discovery.

Steps:
1. Fetch the Cyber Valley Industry Partners list (cybervalley.de/ecosystem/partners or similar
   current URL). Extract each company: name, sector tags, city, website.
2. Manually add ~20–30 established BW R&D companies (automotive: Bosch, ZF; medtech: Zeiss,
   Karl Storz; software: SAP; industrial: Trumpf, Festo, Kärcher; energy: EnBW).
3. For each entry record: name | sector_tags | size_category (startup/SME/corporate) | city |
   careers/research URL | last_verified (today's date).
4. Spot-check ≥10 URLs — confirm they resolve to R&D or careers content. Note any dead links.
5. Write the file as a clean Markdown table with a short preamble explaining: what this list is,
   what it is NOT (not comprehensive — intentionally curated), and how the discovery skill uses it.

Done-when: ≥80 entries; ≥5 non-AI sectors; 10 URLs verified; file has preamble + table.
Commit with message: "feat(2-A): add BW company backbone reference"
```

---

## Task 2-B — Company Search Strategy

**Goal:** The reusable profile→query-mapping for company discovery. Analog to
`search-strategy.md` in Phase 1, but adapted for the very different structure of company
career/research pages.

**Depends on:** Task 2-A (references the backbone).

**Files (new):**
- `skills/find-company-thesis-options/references/company-search-strategy.md`

**Steps:**
1. Reuse the 6-dimension profile extraction from Phase 1 (§1 of `search-strategy.md`) —
   same dimensions, same extraction rule. No changes needed.
2. Define the profile → company-filter mapping: how each profile dimension narrows the backbone
   (e.g. "interests: ML" → filter backbone by sector tags `[AI/ML]`; "domain: automotive"
   → also include entries tagged `[automotive]`; "no-gos: embedded/hardware" → exclude entries
   tagged `[hardware, robotics]`).
3. Define the two-pass strategy for companies:
   - **Pass 1 — Backbone filter:** read the backbone and select companies whose sector tags
     intersect with the student's interest + domain. This is a filter over the curated list,
     not a web search.
   - **Pass 2 — Live enrichment per company:** for each backbone-selected company, run targeted
     queries to find R&D team focus, thesis signals, and contact paths. Use `site:<company-domain>`
     queries to stay on-domain and avoid job board noise.
4. Define query skeletons for Pass 2:
   - Research focus: `site:<domain> research OR "R&D" "{TOPIC_EN}" OR "{TOPIC_DE}"`
   - Thesis signal: `site:<domain> "Masterarbeit" OR "Abschlussarbeit" OR "thesis" OR "student"`
   - Contact / team: `site:<domain> "team" OR "research team" "{TOPIC_EN}"`
   - Fallback (no site:): `"{COMPANY_NAME}" "Masterarbeit" OR "Abschlussarbeit" "{TOPIC_DE}" 2024 OR 2025`
5. Define quality filters (company version): prefer official careers/research sub-pages over
   job-board aggregators; date evidence required for thesis listings; company size affects
   interpretation (startup = direct contact more likely; corporate = use portal).
6. Define no-go exclusion: same no-go terms as Phase 1, but applied to company tags
   (e.g. "hardware" tag → exclude for hardware-averse profiles).
7. Write two worked examples (different student profiles → different backbone slices + query sets).

**Done-when:**
- A reviewer can follow the doc by hand to produce a query set for two different profiles
- Both examples cover different sectors (e.g. one ML/AI, one non-ML)
- The Pass 1 backbone filter step is concrete enough to execute without ambiguity

**Agent prompt:**
```
You are implementing Task 2-B of the Phase 2 company discovery build plan for StudyOS
Thesis-Finder. Branch: feat/no-db-universal-skill.

Read first:
- findings/no_db_universal_skill/2026-06-28-phase2-company-decisions.md (full doc)
- skills/find-university-chairs/references/search-strategy.md (structural template)
- skills/find-company-thesis-options/references/bw-company-backbone.md (the backbone you'll reference)

Your task: Create skills/find-company-thesis-options/references/company-search-strategy.md —
the reusable instruction set that turns a student profile into a company query set.

Structure it analogously to search-strategy.md but adapted for companies:
§1  Profile dimensions → query variables (same 6 dimensions as Phase 1; reuse the table,
    add a "company filter" column showing how each dimension filters the backbone)
§2  Profile → backbone filter (how sector tags map to student interest + domain + no-gos)
§3  Two-pass strategy: Pass 1 = backbone filter (no web search); Pass 2 = live enrichment
    per selected company (site: queries for R&D focus, thesis signal, contact path)
§4  Query skeleton library for Pass 2 (research focus, thesis signal, contact/team, fallback)
§5  Quality filters (company version: prefer official sub-domains, date evidence required,
    no job-board aggregators)
§6  No-go exclusion (same signals as Phase 1 §7 but applied to backbone sector tags)
§7  Output structure per company (use the schema from company-decisions.md § Decision 2)
§8  Two worked examples covering two different student profiles (e.g. ML profile → AI/ML
    backbone slice; medtech profile → Zeiss/Karl Storz backbone slice)

Done-when: a reviewer can produce a realistic query set by hand for both worked examples.
Commit: "feat(2-B): add company search strategy reference"
```

---

## Task 2-C — Build `find-company-thesis-options` Skill

**Goal:** The core Phase 2 skill. Profile → backbone filter → live enrichment → option map
of BW companies with thesis potential. No runtime database.

**Depends on:** Task 2-A, Task 2-B.

**Files (new):**
- `skills/find-company-thesis-options/SKILL.md`

**Steps:**
1. Write the SKILL.md frontmatter: `name`, `description` (company-focused, not confused with
   the uni skill).
2. Write the prerequisite block: same 6-dimension profile requirement as `find-university-chairs`;
   defer to `build-student-profile` if any dimension is missing.
3. Write the workflow (8 steps, parallel to `find-university-chairs`):
   - Step 1: Verify profile (6 dimensions complete)
   - Step 2: Extract query variables from profile
   - Step 3: Filter backbone — read `bw-company-backbone.md`, select companies by sector tags
     matching interest + domain; exclude by no-go sector tags
   - Step 4: Live enrichment per company (Pass 2 from company-search-strategy.md)
   - Step 5: Apply quality filters and dedup
   - Step 6: Apply no-go exclusion
   - Step 7: Produce option map grouped by student interest dimension
   - Step 8: Append coverage caveat (company version — stronger than uni version)
4. Write the Output section using the schema from `company-decisions.md § Decision 2`.
5. Write the Evidence Rules block (company version): never invent supervisor names; always
   confirm thesis coordinator on the company's own page before naming them; mark `thesis signal:
   unclear` when no public listing found.

**Done-when:**
- SKILL.md exists and the workflow is complete
- Running the skill mentally on one sample profile with the backbone + query strategy
  produces a sensible option map with appropriate "not found" flags
- `grep` of the new skill directory shows no runtime database dependency
- The description is company-focused and does not conflict with `find-university-chairs`

**Agent prompt:**
```
You are implementing Task 2-C of the Phase 2 company discovery build plan for StudyOS
Thesis-Finder. Branch: feat/no-db-universal-skill.

Read first:
- findings/no_db_universal_skill/2026-06-28-phase2-company-decisions.md (full doc — output schema, no-gos)
- skills/find-university-chairs/SKILL.md (structural template to mirror)
- skills/find-company-thesis-options/references/bw-company-backbone.md (Task 2-A output)
- skills/find-company-thesis-options/references/company-search-strategy.md (Task 2-B output)

Your task: Create skills/find-company-thesis-options/SKILL.md — the thesis-option discovery
skill for BW companies.

Structure it analogously to find-university-chairs/SKILL.md:
- Frontmatter: name + description (company-focused, distinct from uni skill)
- Prerequisites: same 6-dimension profile requirement; defer to build-student-profile if missing
- Workflow (8 steps):
  1. Verify profile
  2. Extract query variables
  3. Filter backbone (bw-company-backbone.md) by sector tags matching profile — this is a
     read of the backbone file, NOT a web search
  4. Live enrichment per selected company (Pass 2 from company-search-strategy.md):
     research focus, thesis signal, contact path — all on-domain (site: queries)
  5. Quality filters + dedup
  6. No-go exclusion
  7. Produce option map grouped by student interest dimension
  8. Coverage caveat (company version — stronger: "most companies don't publicize thesis
     openings; proactive outreach is the recommended next step")
- Output section: use the schema from company-decisions.md § Decision 2 (always-present fields,
  may-be-missing fields, never-included fields)
- Evidence rules: never invent contact names; confirm thesis coordinator on company's own page
  before naming; mark "thesis signal: unclear" as valid output

Verify: mentally trace through the skill on one sample profile (e.g. ML student interested
in autonomous driving → backbone filter selects Bosch + Cyber Valley AI companies → live
enrichment finds Bosch Center for AI careers page). Make sure the step sequence is executable.
Commit: "feat(2-C): add find-company-thesis-options skill"
```

---

## Task 2-D — Eval Ground Truth for Companies

**Goal:** A small, hand-curated benchmark of known BW companies with confirmed thesis programs,
analogous to the faculty ground truths in Phase 1.

**Depends on:** nothing. Parallel-safe with 2-A and 2-B.

**Files (new):**
- `skills/tests/eval_ground_truth/company_seed/` — one file per student profile
- `skills/tests/eval_ground_truth/company_seed/README.md` — metric definition

**Steps:**
1. Define 3 student profiles covering distinct sectors:
   - Profile C1: ML/AI student (interests: LLMs / computer vision; domain: automotive or robotics)
   - Profile C2: medtech/hardware student (interests: medical imaging / biosensors; domain: health)
   - Profile C3: software/enterprise student (interests: data engineering / distributed systems; domain: finance or enterprise software)
2. Per profile, manually identify 5–8 BW companies that are known to offer thesis positions in
   that area. Sources for verification:
   - Company careers pages (site:bosch.com "Masterarbeit", site:sap.com "Abschlussarbeit", etc.)
   - Cyber Valley partner pages
   - University thesis-fair records (if any are publicly listed)
   - Known large-company thesis programs (Bosch, SAP, Zeiss all have explicit "Studentenarbeiten"
     programs publicly described on their careers pages)
3. For each ground-truth company per profile, record: company name + division + sector tags +
   a URL that confirms the thesis program. Verify each URL resolves and confirms thesis
   availability.
4. Define the recall metric (adapt from Phase 1 README):
   - **Recall = companies surfaced by skill / total ground-truth companies per profile**
   - "Surfaced" = the company name + a correct sector match appears in the skill's option map
   - Target: ≥70% per profile (same target as Phase 1, same rationale)
   - Note: "thesis signal" accuracy is tracked separately as a secondary metric (what % of
     ground-truth companies did the skill correctly identify as having an active program?)

**Done-when:**
- 3 profiles, each with 5–8 verified ground-truth companies
- Each company has a URL confirming thesis program availability (checked as of today)
- README defines recall + thesis-signal accuracy metrics and targets
- Files are committed under `skills/tests/eval_ground_truth/company_seed/`

**Agent prompt:**
```
You are implementing Task 2-D of the Phase 2 company discovery build plan for StudyOS
Thesis-Finder. Branch: feat/no-db-universal-skill.

Read first:
- findings/no_db_universal_skill/2026-06-28-phase2-company-decisions.md (output schema, risks)
- skills/tests/eval_ground_truth/README.md (Phase 1 metric definition — use as template)
- skills/find-company-thesis-options/references/bw-company-backbone.md (what companies are in scope)

Your task: Build an eval ground truth for company discovery under
skills/tests/eval_ground_truth/company_seed/.

Steps:
1. Define 3 student profiles (C1: ML/AI + automotive or robotics; C2: medtech + health;
   C3: software/data + finance or enterprise). Write each as a brief 6-dimension profile
   summary (same format as Phase 1 ground truth files).
2. Per profile, manually identify 5–8 BW companies that are verifiably offering thesis positions
   in that area. Use web search: site:bosch.com "Masterarbeit", site:sap.com "Abschlussarbeit",
   site:zeiss.com "thesis", etc. Only include companies where you find a URL confirming an
   active thesis program (not just R&D presence).
3. For each ground-truth company, record: company name, division (if identifiable), sector tags,
   confirmation URL, date verified.
4. Write README.md defining the recall metric (recall = surfaced / ground-truth per profile;
   ≥70% target) and the secondary "thesis-signal accuracy" metric (did the skill correctly
   identify that the company has an active program?). Adapt from skills/tests/eval_ground_truth/README.md.

Done-when: 3 profiles × 5–8 companies each; all confirmation URLs verified live; README defines
both metrics. Commit: "feat(2-D): add company eval ground truth"
```

---

## Task 2-E — Live Validation

**Goal:** Run `find-company-thesis-options` live with real web search on all 3 ground-truth
profiles, measure recall and thesis-signal accuracy, compare to a plain-Claude baseline, and
document the results honestly.

**Depends on:** Task 2-C, Task 2-D.

**Files (new):**
- `dist/live-validation/company-C1/` (skill arm + baseline arm outputs)
- `dist/live-validation/company-C2/`
- `dist/live-validation/company-C3/`
- `findings/no_db_universal_skill/2026-06-28-phase2-live-eval-results.md` (or date of run)

**Steps:**
1. For each of the 3 profiles (C1, C2, C3):
   a. Run `find-company-thesis-options` with live WebSearch/WebFetch — write the full output
      to `dist/live-validation/company-C*/skill-arm.md` **before** opening the ground truth.
   b. Run a plain-Claude baseline (same profile, no skill, just "which BW companies could
      I write a thesis with?") — write to `dist/live-validation/company-C*/baseline-arm.md`.
2. Score both arms against the ground truth: count surfaced ground-truth companies.
   Record per-company thesis-signal accuracy (did the skill correctly label it?).
3. Write the results doc: per-profile recall (skill vs. baseline), thesis-signal accuracy,
   honest weak spots (e.g. "startup entries not found", "Karl Storz has no English careers page"),
   and a Phase-2 gate verdict (GREEN / AMBER / RED per the ≥70% criterion).
4. Note: if the gate is AMBER or RED, document the specific failures and propose targeted fixes
   (analogous to the Task I → I-fix path in Phase 1).

**Done-when:**
- All 6 arm outputs committed (3 profiles × 2 arms)
- Results doc with concrete numbers: per-profile recall, skill vs. baseline delta
- Phase-2 gate verdict stated with honest rationale
- (Optional) fix-and-revalidate loop if initial run is AMBER

**Agent prompt:**
```
You are implementing Task 2-E of the Phase 2 company discovery build plan for StudyOS
Thesis-Finder. Branch: feat/no-db-universal-skill.

Read first (in order):
- findings/no_db_universal_skill/2026-06-28-phase2-company-decisions.md (§ risks and limits)
- skills/tests/eval_ground_truth/company_seed/ (all files — your ground truth)
- skills/find-company-thesis-options/SKILL.md (the skill you will run)
- findings/no_db_universal_skill/2026-06-28-live-eval-results.md (Phase 1 live eval — for comparison format)

CRITICAL NO-PEEKING PROTOCOL: Run both arms for ALL THREE profiles BEFORE opening any
ground-truth company list to score. Write arm outputs to dist/live-validation/ first.
Only open company_seed/ files after all 6 arm outputs are written.

Steps:
1. For each profile C1, C2, C3:
   a. SKILL ARM: invoke find-company-thesis-options with the profile (live WebSearch on).
      Write full output to dist/live-validation/company-C{N}/skill-arm.md.
   b. BASELINE ARM: give a plain-Claude prompt ("You are a helpful assistant. Which companies
      in Baden-Württemberg could a student with this profile write a Master's thesis at?
      [paste profile]") with no skill, no backbone. Write to dist/live-validation/company-C{N}/baseline-arm.md.
2. ONLY AFTER all 6 outputs are written: open company_seed/ and score recall for each arm.
3. Write findings/no_db_universal_skill/<today>-phase2-live-eval-results.md:
   - Per-profile recall table (skill vs. baseline)
   - Thesis-signal accuracy (for the skill arm only: how often was signal correctly labeled?)
   - Honest failures: which ground-truth companies were missed and why?
   - Phase-2 gate verdict: ≥70% recall on all 3 profiles = GREEN; partial = AMBER (with fix plan)
4. If AMBER: propose targeted fixes (analogous to Phase 1 Task I-fix). Implement the highest-impact
   fix in the same conversation if simple enough, then revalidate the failing profiles.

Commit one commit per major step (arm outputs, scoring, results doc).
At task end, emit a handoff prompt for Phase 3 (distribution) or for the thesis.
```

---

## Dependency graph

```text
2-A (backbone)  ─────────────────────────────────────────> 2-C (skill)
                \                                          /
                 v                                        /
2-B (search strategy) ──────────────────────────────────>
                                                         \
2-D (ground truth, parallel-safe) ───────────────────────+──> 2-E (live validation)
```

---

## Phase-2 gate criteria (equivalent to Phase 1 gate)

- `find-company-thesis-options` runs end-to-end on all 3 profiles with no DB dependency
- Ground truth exists for ≥3 company profiles with a defined recall metric
- Live recall ≥70% on all 3 profiles (skill arm)
- Live skill arm meaningfully outperforms plain-Claude baseline

---

## What Phase 2 does NOT include

- No integration into a GitHub Actions / CI harness (Phase 1 harness is sufficient for discovery;
  extending it for companies is a Phase 3 / maintenance concern)
- No company coverage beyond Baden-Württemberg (or clearly noted BW-adjacent)
- No automatic backbone refresh — Task 2-A produces a point-in-time curated file; annual manual
  review is the intended maintenance model
- No Phase 3 (distribution) planning — that is deferred to a separate plan once both Phase 1
  and Phase 2 are green
