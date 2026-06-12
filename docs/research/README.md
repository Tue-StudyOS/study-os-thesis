# Research Docs — StudyOS Thesis Advisor

**Date:** 2026-06-12 · **Deadline:** 2026-07-01

This folder contains the full research package produced after interviewing 27 professors at the CS department in Tübingen (May 2026) and reviewing the live codebase. It documents what we learned, what we decided to build, and — crucially — **why the Claude Skill architecture is the right approach**.

---

## What's in Here

### English documents (primary)

| File | What it covers |
|---|---|
| [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | One-page overview: project status, key professor findings, roadmap, top risks |
| [market_analysis.md](market_analysis.md) | Synthesis of professor feedback — what 27 professors actually want (and don't want) |
| [technical_roadmap.md](technical_roadmap.md) | Architecture assessment, open PRs/issues, week-by-week roadmap to 2026-07-01 |
| [product_positioning.md](product_positioning.md) | The pivot: why we build for students first, not professors; the new narrative |
| [detailed_analysis.md](detailed_analysis.md) | Full decision log — professor quotes, idea-by-idea evaluation, open questions |
| [skill_architecture_summary.md](skill_architecture_summary.md) | **The skill approach explained** — how a Claude Skill replaces most of the stack |

### German originals (`de/`)

The `de/` subfolder contains the same documents in German (the language they were first drafted in) plus two additional files:

| File | What it covers |
|---|---|
| [de/EXECUTIVE_SUMMARY_DE.md](de/EXECUTIVE_SUMMARY_DE.md) | German version of the executive summary |
| [de/marktanalyse.md](de/marktanalyse.md) | Market analysis (German) |
| [de/technische_roadmap.md](de/technische_roadmap.md) | Technical roadmap (German) |
| [de/produktpositionierung.md](de/produktpositionierung.md) | Product positioning (German) |
| [de/detaillierte_analyse.md](de/detaillierte_analyse.md) | Detailed analysis (German) |
| [de/skill_architektur_zusammenfassung.md](de/skill_architektur_zusammenfassung.md) | Skill architecture summary (German original) |
| [de/ideen_bewertung.md](de/ideen_bewertung.md) | Idea evaluation — each of the 10 ideas assessed against professor feedback and the codebase |
| [de/Ideen.md](de/Ideen.md) | Raw idea list (the starting point for the evaluation above) |

---

## The Core Finding: The Skill Approach Works

The professor's suggested architecture pivot — packaging the entire advisor as a **single Claude Skill** instead of a hosted web app — turns out to be technically sound and solves several pre-existing problems at once:

- **Security blocker gone.** No hosted backend means the WebSocket-JWT-in-URL issue (currently a showstopper for any public deployment) largely disappears.
- **Stability concern addressed.** A Skill is a set of files, not a running web app that falls apart when the student HiWis leave. Exactly what Prof. Hennig worried about.
- **Massive stack simplification.** Postgres, pgvector, Celery, Redis, Ollama hosting, and the React UI are no longer needed. At a few hundred researchers, Claude reads the Markdown files directly — no embedding infrastructure required.
- **Deterministic GPA.** Bundling `compute_gpa.py` as a script removes LLM temperature noise from grade calculations (fixes the floating-result bug reported in idea #10).
- **Zero maintenance for professors.** Upkeep = a periodic pipeline run. No professor needs to do anything — exactly what the product positioning calls for.

See [skill_architecture_summary.md](skill_architecture_summary.md) for the full breakdown.

---

## One Open Decision

Everything else follows from a single choice: **how is the Skill distributed to the department?**

- **Central + auto-updated** → needs an API-based approach with a thin backend and a monthly GitHub Actions cron that bumps the skill version. Zero effort for end users.
- **Self-serve** → students download and upload a ZIP to claude.ai manually. Works as a demo/fallback, but the monthly data update becomes impractical.

This needs to be clarified with the professor before committing to an architecture.
