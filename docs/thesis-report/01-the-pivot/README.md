# 01 — The Pivot

**Files in this folder:**
- [2026-06-25-besprechung-notes.md](2026-06-25-besprechung-notes.md) — raw meeting notes,
  the day before the pivot was written up: the open questions that triggered it.
- [2026-06-26-vision-no-db.md](2026-06-26-vision-no-db.md) — the pivot document itself.

## Synthesis

The pivot from a hosted, database-backed web app to a database-less Claude Skill was decided
in a single day (2026-06-25 → 2026-06-26), but it wasn't a sudden idea — it's the direct
answer to the risks surfaced in [00](../00-problem-and-research/README.md).

The meeting notes from 2026-06-25 show the team working through the problem live, as open
questions rather than settled answers: *"Do we even need a backend? Can we design this so it
really works without one — without a database?"* / *"Then we wouldn't have to keep the whole
thing up to date so it still works in three years — we'd just have to describe how the tool
scrapes the web and leads the conversation."* / *"Where's the difference to just using Claude
without a skill?"* These three questions — do we need a DB, how do we stay current without
maintenance burden, and what's our actual edge over plain Claude — are the exact three
questions the rest of the project spends the following weeks answering empirically (see
[03](../03-hardening-and-evaluation/README.md) for the third one in particular). The notes
also already contain the seeds of later decisions made explicit in `VISION_NO_DB.md`: expand
to companies, expand to all faculties (not just CS), and — pointedly — *"maybe we need to
build the skill so it works for all faculties without needing background info, so it really
runs 'fully automatically.'"*

`VISION_NO_DB.md` (written the next day) turns those open questions into a decision. Its
core principle: **no static database foundation — the skill defines *how* to search, not
*what* is stored.** The comparison it draws is blunt and became the project's standing
rationale (repeated verbatim in `MASTERPLAN.md` §2 and `README.md`'s "Architecture rationale"):
a database goes stale within months, covers only what was curated, and needs a person or a
GitHub Actions cron to keep it alive; a live-web-search skill is always current, covers
everything publicly visible, and needs zero ongoing maintenance. The scope was set narrowly
and deliberately: Tübingen students, all faculties, university chairs primary / companies
secondary; explicitly **not** other universities or Bachelor theses (extendable later, not
now) — a scope decision that resurfaces and gets a much sharper justification in
[04-open-work](../04-open-work/README.md), where the "does breadth erode advantage"
question is finally treated as a testable claim rather than an intuition.

`VISION_NO_DB.md` also names, up front, the question a skeptical reader would ask first —
*"what makes this better than just asking Claude?"* — and answers it with a five-point
mechanism (deep profiling via interview, systematic search templates instead of ad-hoc
queries, aggregation into an interest-grouped map, active completeness pressure, concrete
next-step guidance) rather than a vague appeal to "AI." That mechanism is exactly what Phase 1
was built to implement ([02](../02-building-the-core/README.md)) and what Task P later set out
to prove empirically actually happens ([03](../03-hardening-and-evaluation/README.md)) — the
pivot document's central bet is the one piece of the whole project that most needed evidence,
not just a plausible design.

The legacy hosted-app stack (FastAPI + Celery + Postgres + React) was not deleted; it was
archived on the `legacy/web-app` git branch, and the project's continued architecture
rationale (`docs/thesis-report/00-problem-and-research/.../skill_architecture_summary.md`,
linked from the root `README.md`) explains point by point why the skill approach dissolves
each of the risks found in the professor research: no hosted backend means the WebSocket-JWT
issue is moot, a skill is a set of files rather than a running service that breaks when
student maintainers leave, and a bundled deterministic script removes the kind of
LLM-computed-metric trust problem that worried professors about `ChairExplorer`.
