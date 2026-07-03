# 00 — Problem & Research

**Files in this folder:**
- [2026-06-12-professor-research-package/](2026-06-12-professor-research-package/) — the
  full research package (English + German), produced after interviewing 27 CS-department
  professors in May 2026 and reviewing the then-current codebase. Start with its own
  [README](2026-06-12-professor-research-package/README.md) and
  [EXECUTIVE_SUMMARY.md](2026-06-12-professor-research-package/EXECUTIVE_SUMMARY.md).
- [2026-06-09-project-context-pre-pivot.md](2026-06-09-project-context-pre-pivot.md) — a
  snapshot of the hosted-web-app stack and status just before the research package landed.
- [2026-06-11-mails.docx](2026-06-11-mails.docx), [2026-06-11-plan.docx](2026-06-11-plan.docx) —
  original planning artifacts referenced by the research package as source material.

## Synthesis

Before any pivot discussion, the project was a hosted web app: FastAPI backend, Celery task
queue, Postgres + pgvector, a React frontend, Ollama for local embeddings — a full-stack
"chair matcher" that scraped professor pages into a semantic index. `2026-06-09-project-
context-pre-pivot.md` documents this stack in detail: it was ~90% feature-complete (transcript
upload, competency profile, semantic chair matching, proposal generation), with 5 open PRs and
16 open issues, on track for a 1.07.2026 deadline contingent on one blocking pipeline (the
chair-discovery scraping agent, PR #35 → #37).

The research package (May–June 2026, 27 professor interviews in the CS department) is the
pivotal input. Its headline finding was not a feature request — it was a **demand-side
warning**: roughly half of interviewed professors (segments "A" and "C") did not want a
central platform at all, either because they were already overrun with applicants or on
principle preferred co-creating topics through direct conversation. Only ~35% ("Type B") would
try a topic tool, and only under strict conditions: zero-friction, no reminder emails, stable
for years, exportable back to their own site. Crucially, a topic-listing platform had already
been tried in the department around 2022 and had **failed for incentive reasons, not UI
reasons** (per Prof. Hennig) — a fact that reframes "add more features" as the wrong lever.
The single most-endorsed idea across interviews was one already on the roadmap: scrape
existing chair websites instead of asking professors to enter data (Macke: *"that would be
something I am much more excited about"*).

Alongside the demand-side finding, the research package's "Top 3 Risks" section flagged
concrete technical debt in the hosted-app track: a WebSocket-JWT-in-URL vulnerability (tokens
leaking into logs/proxies — a showstopper for any public deployment), hard-coded/fabricated
metrics displayed in the chair-explorer UI to professors whose #1 stated concern was trust,
and general chair-discovery scope creep across 27 heterogeneous, inconsistently-structured
websites. None of these were fixed by adding code — they were symptoms of committing to a
stateful, hosted, professor-facing platform in a context where professors didn't want one.

This is the input that motivated the pivot documented in [01](../01-the-pivot/README.md): if
the value is "scrape live pages, don't ask professors for data" and the audience that wants
the tool is students (not professors), a hosted database-backed platform is solving the wrong
problem in the wrong shape.
