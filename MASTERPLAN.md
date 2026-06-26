# Masterplan — StudyOS Thesis-Finder

> **Purpose:** The zoomed-out view of the whole effort. This file is a
> **lookup** — it describes *what* we build, *in what order*, and *why*. It
> changes rarely.
>
> **For current progress, open difficulties, and notes see [STATUS.md](STATUS.md)** —
> that is the only file that is updated continuously.

---

## 1. What we build

A public, portable **Agent Skill package** for thesis advising. The package
takes a student from vague interests, coursework, skills, and constraints to
evidence-based thesis directions and advisor-ready first-contact messages —
with no required backend, database, or UI. It is driven by curated Markdown data
plus live research when an agent has web/search tools.

The durable product is:

- portable `skills/` folders with concise `SKILL.md` entrypoints
- Markdown `references/` files for rubrics, schemas, indexes, examples, and
  public source data
- `AGENTS.md` as the maintainer and agent operating guide
- lightweight scripts, tests, release tooling, and recurring data/eval
  workflows
- durable process findings under `findings/dev_process/`

The student-facing skill flow:

```text
raw input ("I like deep learning + robotics")
   |
   v  build-student-profile        deep interview -> structured profile
   v  find-recent-papers and/or
      find-university-chairs        evidence from papers and chair data
   v  match-thesis-advisors         supervisors ranked by fit + caveats
   v  generate-thesis-directions    concrete proposal sketches
   v  draft-thesis-contact          first-contact email
```

Maintenance skills and process assets:

- `design-agent-skill` is the meta-skill for creating, reviewing, or reshaping
  any skill.
- `update-openalex-paper-index` defines the paper-index maintenance workflow.
- `AGENTS.md` must explain how future agents extend the package to other
  faculties.
- `findings/dev_process/` records important repo/product/process findings so
  maintainers do not have to rediscover them.

---

## 2. Current Findings

As of 2026-06-25:

- The active GitHub issue backlog was reset to the Phase 1 data-foundation
  issues `#45`-`#51`; old app/backend/UI issues were closed as superseded by
  the skill-package pivot.
- Current bundled data is partial: 47 professor seeds exist, but only 5 curated
  chair profiles and 7 OpenAlex-linked professor/researcher rows are present.
- A 3-chair pilot ground-truth fixture exists for PhD/doctoral-researcher recall,
  but it still needs to become the measured validation anchor.
- The README describes a monthly OpenAlex refresh workflow, but no scheduled
  monthly data-refresh workflow exists yet.
- Codex multi-turn eval scaffolding exists, but monthly eval snapshots are not
  yet tied to data refreshes or baseline comparison.
- The package needs explicit faculty-extension guidance, Markdown data-layout
  policy, privacy/public-data policy, and a findings/dev-process log.

---

## 3. The Data Structure — The Tree

The core data product is a Markdown researcher tree:

```text
Professor / PI
   -> PhD, doctoral researcher, postdoc, or other relevant researcher
        -> Paper
```

Each person node should have a research area/topic description, source
provenance, update date, and uncertainty/review status where needed. Every paper
should reference a person slug and preserve traceable metadata such as DOI or
OpenAlex ID, source, year/date, and summary/abstract policy.

The tree must be:

- reviewable as plain Markdown
- internally linked with no orphaned Prof -> Researcher -> Paper references
- safe for public release
- refreshable without silently overwriting maintainer-owned corrections

---

## 4. Ordering Principle

**Get the data correct first, then optimize the advising behavior.** Downstream
matching and proposal generation cannot be trusted while chair, researcher, and
paper data are incomplete or stale.

De-risking strategy:

- prove the pipeline on 3 pilot chairs
- validate recall and integrity against ground truth
- scale to all 47 professor seeds
- only then broaden skill-behavior optimization

---

## 5. Phase 1 — Data Foundation (Current Phase)

The current executable backlog is the verified researcher-tree epic.

| # | Issue | What it is about |
|---|---|---|
| 1 | [#45](https://github.com/Tue-StudyOS/study-os-thesis/issues/45) | Resolve OpenAlex author IDs for all 47 seed professors; flag ambiguous matches instead of guessing. |
| 2 | [#46](https://github.com/Tue-StudyOS/study-os-thesis/issues/46) | Build the hand-verified ground-truth roster for 3 pilot chairs. |
| 3 | [#47](https://github.com/Tue-StudyOS/study-os-thesis/issues/47) | Discover PhDs/researchers per chair from team pages and cross-check evidence. |
| 4 | [#48](https://github.com/Tue-StudyOS/study-os-thesis/issues/48) | Define Prof -> Researcher/PhD -> Paper schema and referential integrity checks. |
| 5 | [#49](https://github.com/Tue-StudyOS/study-os-thesis/issues/49) | Fetch papers and generate topic/description fields per person as tree Markdown. |
| 6 | [#50](https://github.com/Tue-StudyOS/study-os-thesis/issues/50) | Add validation harness: structural checks, anomaly checks, sampling, golden record. |
| 7 | [#51](https://github.com/Tue-StudyOS/study-os-thesis/issues/51) | Add refresh automation: monthly/manual run, review PR, override protection, validation in loop. |

Dependency graph:

```text
1 (Prof IDs) ---------------------.
2 (ground truth) -> 3 (PhD discovery) -> 5 (papers + descriptions) -> 6 (validation) -> 7 (automation)
4 (tree schema) ------------------'
```

Gate Phase 1 -> Phase 2:

- validation harness is green
- golden record is reproducible
- pilot recall is at least 90%
- generated Markdown has no broken Prof -> Researcher -> Paper references
- refresh process does not overwrite manual corrections silently

---

## 6. Governance And Portability Track

This track can run alongside Phase 1 because it makes the package maintainable
for humans and future agents.

- **Faculty extension:** `AGENTS.md` must explain how to adapt the package to a
  new faculty or program, starting with `skills/design-agent-skill`.
- **Markdown data filesystem:** document which files are generated, curated,
  protected by manual overrides, and used as eval snapshots.
- **Public-data and privacy policy:** document what public academic data may be
  bundled and what student-private or sensitive data must never be stored.
- **Findings/dev-process log:** important architecture, process, data, eval, and
  issue-triage findings must be recorded under `findings/dev_process/`.
- **Monthly snapshots:** data refreshes and multi-turn evals should produce
  reviewable artifacts so regressions can be traced to skill changes or data
  changes.

---

## 7. Phase 2 — Skill Optimization

Only start broad skill optimization after the Phase 1 data gate.

- Measure a baseline before changing core skill behavior.
- Expand evals across happy path, shallow profile, missing info, adversarial
  prompts, and end-to-end flow.
- Add few-shot examples only where evals show repeated failure.
- Unify shallow-profile guardrails across the student-facing skills.
- Calibrate LLM-as-judge results against human review.
- Ensure degree program, thesis level, and scope constraints are respected in
  matching and proposal generation.

---

## 8. Phase 3 — Cross-Platform

The content should remain portable across capable coding-agent clients. Test the
package with Codex, Claude, Gemini CLI, and similar tools where practical. Avoid
client-specific metadata unless there is a documented portable fallback.

---

## 9. How This Plan Is Used

- `MASTERPLAN.md` = stable structural plan. Change it only when the product goal,
  phase structure, or major workflow changes.
- `STATUS.md` = living progress document. Update status, blockers, decisions,
  and dated logs there.
- `AGENTS.md` = operating instructions for future agents and maintainers.
- `findings/dev_process/` = durable discoveries about repo process, architecture,
  data maintenance, evals, or governance.
- GitHub Issues = executable work units with acceptance criteria.
