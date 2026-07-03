# Thesis Report — How StudyOS Thesis-Finder Came to Be

This folder is the curated, chronological account of how this project went from a hosted
web-app MVP to a database-less Claude Skill package — and why, at each fork, the team chose
the path it did. It exists for the thesis write-up: the goal is that someone who has never
seen the codebase can read through `00` → `04` and understand the genesis, the pivots, and
the evidence behind the final architecture, without re-deriving it from ~25 scattered files.

**What this is not:** a duplicate of the working documents. Every section below is a short
synthesis (what happened, why) that links out to the original source material — the source
stays the single point of truth; this folder is the reading path through it.

---

## The story in one paragraph

The project started (May–June 2026) as a hosted web app — FastAPI, Celery, Postgres, React —
built after interviewing 27 professors in the CS department about a chair-matching tool.
That research surfaced a hard finding: about half the professors did not want a central
platform at all, and a topic-listing platform had already failed once in the department for
incentive reasons, not UI reasons. The strongest signal was "build for students first, scrape
what already exists instead of asking professors to enter data." At the same time, the
hosted-app track was carrying real risk: a WebSocket-JWT-in-URL security hole, fabricated
placeholder metrics shown to trust-sensitive professors, and a maintenance model that assumed
student HiWis would keep a scraping pipeline alive indefinitely. On 2026-06-26 the team
pivoted: instead of a database that requires upkeep, package the whole advisor as a **Claude
Skill** — a set of Markdown instructions plus a small, curated "backbone" reference, with the
live web as the only runtime data source. Phases 1–3 (June 26 – 28) built and proved this for
university chairs, then companies, then wired it into a single entry-point skill with session
persistence. From late June into July, a "hardening" track pushed past "it passes the gate"
toward "it's good": live (not fixture) evaluation, a precision metric, a **steering proof**
that the student interview genuinely changes the search output (not just decorates a generic
answer — the empirical core of the "beats plain Claude" claim), and ground truth for
structurally harder faculties. What remains open going into the write-up is documented
honestly in `04-open-work/`.

---

## Reading table

| # | Section | Core question | Key sources |
|---|---|---|---|
| [00](00-problem-and-research/README.md) | Problem & research | What did 27 professors actually want, and what was the original plan? | professor research package, pre-pivot project context |
| [01](01-the-pivot/README.md) | The pivot | Why did the team abandon the hosted web app for a database-less skill? | `VISION_NO_DB.md`, skill architecture summary |
| [02](02-building-the-core/README.md) | Building the core | How was the two-track (university/company) discovery skill actually built? | `MASTERPLAN.md`, `findings/no_db_universal_skill/*`, `Design-Entscheidungen.md` |
| [03](03-hardening-and-evaluation/README.md) | Hardening & evaluation | Does it actually work, and how do we know? | `core-optimization-roadmap.md`, live-eval results, steering proof |
| [04](04-open-work/README.md) | Open work | What's left, and what did we deliberately decide not to do? | `Ideen_Domi_02_07.md`, `gesamtplan-2026-07-02.md` |
| — | [decision-log.md](decision-log.md) | The whole timeline as one citable table | synthesized from all of the above |

## Where the living documents are (not moved here)

`STATUS.md` (current progress) and `MASTERPLAN.md` (stable plan) at the repo root are
continuously updated and are the authoritative current state — this report narrates how they
got that way, it does not replace them. `Design-Entscheidungen.md` (repo root) is the living
architecture-rationale companion to `MASTERPLAN.md` and is linked from `02` rather than copied.
`findings/no_db_universal_skill/` already is a dated, chronological archive and was left in
place — this report links into it heavily rather than duplicating its ~15 files.
