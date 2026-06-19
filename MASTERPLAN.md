# Masterplan — StudyOS Thesis-Finder

> **Purpose:** The zoomed-out view of the whole effort. This file is a **lookup** — it describes *what* we build, *in what order*, and *why*. It changes rarely.
>
> **For current progress, open difficulties, and notes see [STATUS.md](STATUS.md)** — that is the only file that is updated continuously.

---

## 1. What we build

A set of portable **Claude Skills** that take a student from vague interests to a prepared first contact with a fitting thesis supervisor — with no backend, DB, or UI, driven only by curated Markdown data + live research.

The skill flow:

```
raw input ("I like deep learning + robotics")
   │
   ▼  build-student-profile        deep interview → structured profile (in-session only)
   ▼  find-university-chairs        matching chairs from the database + live web search
   ▼  match-thesis-advisors         supervisors ranked by fit + evidence
   ▼  find-recent-papers            relevant papers as evidence
   ▼  generate-thesis-directions    concrete thesis directions + proposal hooks
   ▼  draft-thesis-contact          first contact email
```

Plus maintenance skills: `update-openalex-paper-index` (data refresh) and `design-agent-skill` (meta).

---

## 2. The data structure — the tree

The core is a **tree structure** as a Markdown database:

```
Professor  (topic area + description)
   └── PhD  (topic area + description)
          └── Paper (with summary)
```

Every professor has a topic area and a description; beneath them all their PhDs with their own topic area; beneath those their papers with a summary. Everything saved as `.md` after scraping, referentially linked.

---

## 3. Ordering principle

**Get the data correct first, then everything else.** Downstream quality (matching, proposals) cannot be verified while the data is wrong or incomplete. So Phase 1 (data foundation) is a hard gate before Phase 2 (optimization).

**De-risk strategy:** Don't make "all 47 profs perfect" the gate — instead **pilot on 3 chairs → prove the pipeline + validation → scale to 47.**

---

## 4. Phase 1 — Data Foundation (current phase)

The "verified researcher tree" epic. Order = dependency.

| # | Issue | What it is about |
|---|---|---|
| 1 | [#45](https://github.com/Tue-StudyOS/study-os-thesis/issues/45) | **Resolve author IDs for all 47 profs** (name+URI → OpenAlex ID, with disambiguation) |
| 2 | [#46](https://github.com/Tue-StudyOS/study-os-thesis/issues/46) | **Ground-truth roster** for 3 pilot chairs (manual PhD list as the measuring stick) |
| 3 | [#47](https://github.com/Tue-StudyOS/study-os-thesis/issues/47) | **PhD discovery per chair** (team page + co-author graph; none forgotten) |
| 4 | [#48](https://github.com/Tue-StudyOS/study-os-thesis/issues/48) | **Tree schema** Prof→PhD→Paper + referential integrity |
| 5 | [#49](https://github.com/Tue-StudyOS/study-os-thesis/issues/49) | **Paper scrape + topic/description** per person, as tree MD |
| 6 | [#50](https://github.com/Tue-StudyOS/study-os-thesis/issues/50) | **Validation harness** (anomaly checks + sampling + golden record) |
| 7 | [#51](https://github.com/Tue-StudyOS/study-os-thesis/issues/51) | **Automation** (cron every 2 weeks, PR output, override protection, loud failure) |

Dependency graph:

```
1 (Prof IDs) ─┐
2 (ground truth) ─→ 3 (PhD discovery) ─→ 5 (papers+description) ─→ 6 (validation) ─→ 7 (automation)
4 (schema) ────────────────────────────────┘
                                                                       ↓
                                                      Gate: only once 6 is green → Phase 2
```

**Gate Phase 1 → Phase 2:** Issue 6 (validation) is green, golden record reproducible, pilot recall ≥ 90%.

---

## 5. Phase 2 — Skill optimization (after the gate)

Only sensible once the data is correct.

- **Measure a baseline** — freeze current eval scores before changing anything.
- **Expand the eval set** — several cases per core skill (happy path, shallow profile, missing info, adversarial) instead of 1.
- **Few-shot examples** in the core skills (`build-student-profile`, `find-university-chairs`, `match-thesis-advisors`).
- **Unify guardrails** (shallow-profile protection everywhere).
- **End-to-end flow eval** across the whole skill chain.
- **Calibrate the judge** against human judgement.
- **Respect degree program / thesis level / scope** — groundwork already added by a teammate in `build-student-profile` (`references/tuebingen-degree-programs.md`): degree program → thesis level (e.g. Machine Learning is Master-only) → scope (Bachelor 4 months vs. Master 6 months). Proposal generation must honor this.

## 6. Phase 3 — Cross-platform (stretch)

The content is portable, the mechanism is not. Order: OpenAI Custom GPT (closest to the skill experience) → Gemini → generic RAG. Only after Phase 2, since you port optimized content, not unfinished content.

---

## 7. How this plan is used

- **MASTERPLAN.md** (this file) = stable lookup. Only adjusted when the plan changes structurally.
- **[STATUS.md](STATUS.md)** = living document. Progress, blockers, decisions, notes land here. **Always update here, not in the Masterplan.**
- **GitHub Issues** = the executable units. Each issue linked above; details, acceptance criteria, and discussion live in the issue.
