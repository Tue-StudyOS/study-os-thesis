# Status — StudyOS Thesis-Finder

> **This is the only continuously updated file.** Here we collect progress, blockers, difficulties, and decisions. The stable overall plan is in [MASTERPLAN.md](MASTERPLAN.md).
>
> **Convention:** When working on a step, change its status here, note difficulties, and add a dated line to the log below. Do not edit the Masterplan.

**Last update:** 2026-06-24

---

## Current phase

**Phase 1 — Data Foundation.** Goal: a verified researcher tree (Prof → PhD → Paper) for the pilot chairs, then scaled to 47 profs.

---

## Step status

Legend: ⬜ open · 🟨 in progress · ✅ done · ⛔ blocked

| # | Step | Status | Owner | Notes / difficulties |
|---|---|---|---|---|
| 1 | [#45](https://github.com/Tue-StudyOS/study-os-thesis/issues/45) Resolve author IDs for all 47 profs | ⬜ | – | Only 7/47 currently in `researchers/INDEX.md`. Disambiguation is the hurdle. |
| 2 | [#46](https://github.com/Tue-StudyOS/study-os-thesis/issues/46) Ground truth for 3 pilot chairs | 🟨 | – | Fixture drafted (Martius, von Luxburg, Geiger); auto-captured rosters pending human verification. |
| 3 | [#47](https://github.com/Tue-StudyOS/study-os-thesis/issues/47) PhD discovery per chair | ⬜ | – | Hardest part: OpenAlex has no supervisor→PhD edge. |
| 4 | [#48](https://github.com/Tue-StudyOS/study-os-thesis/issues/48) Tree schema + integrity | 🟨 | – | Faculty-agnostic builder + column-name-keyed referential-integrity validator (`--validate-only`) wired into CI. PhD-level fields (role/advisor) deferred to a follow-up. |
| 5 | [#49](https://github.com/Tue-StudyOS/study-os-thesis/issues/49) Paper scrape + description per person | ⬜ | – | Description/summary = LLM step; abstract-vs-LLM decision still open. |
| 6 | [#50](https://github.com/Tue-StudyOS/study-os-thesis/issues/50) Validation harness | ⬜ | – | Anomaly checks instead of full review; golden record as anchor. |
| 7 | [#51](https://github.com/Tue-StudyOS/study-os-thesis/issues/51) Automation (cron + PR + overrides) | ⬜ | – | Override protection so the re-scrape does not destroy manual fixes. |

**Gate Phase 1 → 2:** Step 6 green · golden record reproducible · pilot recall ≥ 90%.

---

## Open decisions

- **Runtime data source:** scraper DB first or live web search first? → optimize later, does not block Phase 1.
- **Description/summary:** reuse abstract (free, deterministic) vs. LLM summary (nicer, costs more)?
- **Scrape cadence:** every 2 weeks vs. monthly?

---

## Known difficulties / risks

- **PhD discovery recall** — 47 heterogeneous team pages; not measurable without ground truth (see Step 2 → 3).
- **Name→ID disambiguation** — common names, PhDs with few papers.
- **Manual corrections** — must not be overwritten on re-scrape (Step 7).
- **30 MB upload limit** of the Skills API to watch as the tree grows.
- **Personal data (GDPR)** — PhD names + research are bundled; public academic data, but document it consciously.

---

## Log

- **2026-06-26** — Step 4 (#48) → in progress. Reframed per maintainer steer: instead of hand-adding fixed columns, generalized the builder (`scripts/update_openalex_index.py`) so a deterministic script the agent invokes can build/validate *any* faculty's Markdown tree (`--researchers-index`/`--chairs-index`/`--papers-dir`). Tables are now parsed by column name (extra faculty columns allowed). Added a column-agnostic referential-integrity validator (`validate_references`, runnable via `--validate-only`) covering researcher→chair, chair→researcher, paper→person, paper→chair; wired into CI via `skills/tests/test_tree_integrity.py` (fails on orphans). PhD-level schema fields (role/advisor edge) deliberately deferred to a follow-up PR.
- **2026-06-24** — Opened PR #57 for the ground-truth fixture. Refined the classification convention (verified against live team pages): former PhDs/alumni excluded entirely; people under a chair's "Researcher" role handled like PhDs (active); postdocs included with status `postdoc` as recall targets; research engineers, group leaders and admin excluded. Martius now 20 active (no postdoc section on page); von Luxburg adds 5 postdocs (Bhattacharjee, Bordt, König, Thiessen, Waller); Geiger 15 active (no current postdoc section). Added profile URLs for the three Martius Researchers.
- **2026-06-22** — Step 2 (#46) → in progress. Drafted `skills/tests/fixtures/ground_truth_phds.json` for the 3 pilot chairs (Martius / Autonomous Learning, von Luxburg / Theory of ML, Geiger / Autonomous Vision). Rosters auto-captured from official team pages: 17 active + 4 alumni (Martius), 3 active + 2 incoming + 1 associated (von Luxburg), 15 active (Geiger). Committed as WIP — entries still need human verification before the fixture is authoritative; no PR yet.
- **2026-06-18** — Translated Masterplan + Status to English. Reviewed teammate (Valentin) commit `688f08d`: added degree-program awareness to `build-student-profile` (`tuebingen-degree-programs.md`) — degree program → thesis level (ML = Master-only) → scope (Bachelor 4mo / Master 6mo). Logged as a Phase 2 item in the Masterplan; does not affect Phase 1.
- **2026-06-18** — Added Masterplan + Status + workflow. Defined Phase 1, created 7 issues (#45–#51). Starting point: 8 working skills, data only 7/47 profs, 0 PhDs.
