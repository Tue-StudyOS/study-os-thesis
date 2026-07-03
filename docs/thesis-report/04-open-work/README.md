# 04 — Open Work

**Files in this folder:**
- [2026-07-02-ideen-domi.md](2026-07-02-ideen-domi.md) — raw brainstorm on six directions for
  the project (other universities, testable evaluation, backbone breadth, distribution,
  and — most importantly — the scope-vs-genericness intuition below).

**Related, not moved here** (already dated/organized in place):
- [findings/gesamtplan-2026-07-02.md](../../../findings/gesamtplan-2026-07-02.md) — a full
  codebase review + point-by-point discussion of the ideas above, ending in a prioritized
  implementation plan.

## What's open right now

- **Law and Theology blind live runs.** Ground truth exists for all four hard-faculty/
  interdisciplinary cases; Humanities has been run (60% recall, root-caused to an eval-protocol
  gap, not a skill defect — see [03](../03-hardening-and-evaluation/README.md)) and the
  interdisciplinary case was covered via Task R's routing check (100%). Law and Theology have
  ground truth but no live run yet.
- **Track 2 (backbone audit & repair, weak-web-presence fallback, query-skeleton iteration)**
  and **Task S (output & interview quality pass)** — defined in `core-optimization-roadmap.md`
  §3, neither started. Task R (edge-case behavior) is done (3/3 edge cases pass). Track 2 was
  implicitly skipped because Task I already cleared the recall bar that would have triggered
  it; this was never formally closed and, until 2026-07-03, wasn't even visible as "open" in
  `STATUS.md`.
- **The roadmap's own "core is done" recall bar is not yet met** (≥80% recall across ≥6
  faculties incl. one hard faculty — only 5 faculties have any live number, and the one hard
  faculty tested is below bar; see the
  [aggregate scorecard](../../../findings/no_db_universal_skill/2026-07-03-eval-aggregate-scorecard.md)).
- **Company-backbone ground-truth circularity** (named in [03](../03-hardening-and-evaluation/README.md)):
  an independent, non-backbone-derived ground truth for company discovery is still missing.
- **Non-MINT company backbone coverage** — the BW company backbone is strong for AI/ML,
  robotics, medtech, and manufacturing, and thin for psychology/UX, EdTech, environmental
  science, and life-science spinouts, even though the tool claims to serve all faculties.

## The scope question — the idea that matters most for the thesis claim

`2026-07-02-ideen-domi.md` raises a specific concern, credited there to the author's stats
background (SLLN/law-of-large-numbers intuition): **the broader the tool is made, the more it
converges in expectation toward plain Claude.** The reasoning: the tool's advantage over plain
Claude comes from curated, scope-specific knowledge (the faculty backbone, the MPI-IS/ELLIS
leg, the search-strategy query mapping) — a fixed asset that one person can maintain. Spread
that same curation budget across more universities or a wider company list, and curation
*density per query* drops; in the limit, the tool degrades toward "plain Claude with extra
steps." `findings/gesamtplan-2026-07-02.md` takes this seriously as the project's central
scientific claim rather than a hedge, and works through six concrete ideas against it (other
universities as a third track, making the evaluation genuinely testable, broadening the
company/university backbones, generalizing the backbone-building process to any university,
and distribution). Its recommendation, argued point by point: **narrow scope (Tübingen, all
faculties) is the stronger position, not a fallback** — and the way to make that a scientific
claim rather than an opinion is to test it directly, e.g. running the identical skill
mechanism against a university it was *not* curated for and showing the advantage over
baseline shrinks or disappears. That experiment has not been run; it is the most
consequential piece of unfinished work going into the write-up.

## What was deliberately decided against (not just "not done yet")

- **Generic, per-university entry-point discovery via live web search** — rejected, not
  deferred. If the skill's first move for any university were "search for the right
  organizational entry point," it would functionally *be* the plain-Claude baseline it's
  supposed to beat; the whole measured advantage comes from curated Tübingen-specific
  knowledge that a runtime search cannot reconstruct.
- **Scraping concrete job postings** (see [02](../02-building-the-core/README.md)) — rejected
  on fragility and low-yield grounds, not merely postponed.
- **A third "other universities" track as a user-facing feature** — the brainstorm's own idea
  #1; `gesamtplan-2026-07-02.md` argues this should be a controlled *experiment arm*, not a
  shipped feature, precisely because it would dilute the curated-knowledge advantage described
  above.
