# Executive Summary — StudyOS Thesis Advisor

**Date:** 2026-06-11 · **Deadline:** 1.07.2026 · **Full analysis:** see market_analysis.md, technical_roadmap.md, product_positioning.md, detailed_analysis.md

---

## Status

Student-facing MVP is ~90% complete: transcript upload, competency profile, semantic chair matching, and proposal generation all work; i18n is in review (PR #38). 5 PRs and 16 issues are open; the critical path is **landing the chair-discovery scraping agent (PR #35 → #37)**. We are on track for 1.07.2026 **if** that pipeline merges by week 14.

## What 27 Professors Told Us

- **~35%** ("Type B"): would try a topic tool — but only if zero-friction, no reminder emails, stable for years, and exportable back to their own websites.
- **~50%** (Types A + C): don't want a central platform — either overrun with applicants already, or principled believers in co-creating topics through conversation.
- **~15%** (Type D): irrelevant to their recruiting pipeline (GTC, lab courses).

**Key insight:** a topic-listing platform was tried in this department (~2022) and failed for incentive reasons, not UI reasons (Hennig). **Build for students first; let chairs plug in optionally.** The most-endorsed feature is one we're already building: scraping existing chair websites instead of asking professors to enter data (Macke: "that would be something I am much more excited about").

## Roadmap

| Phase | Focus |
|---|---|
| **Now – week 14** | Merge schema groundwork (#35) + chair-discovery agent (#37); merge i18n (#38) |
| **Weeks 15–21** | Eval harness (deepeval, #6), RAG optimization (#7), real skill computation (#21/#16), DeepSeek dedup (#33) |
| **Weeks 22–28** | Security fix (WebSocket JWT), trust fix (ChairExplorer placeholder metrics), docs alignment, staging deployment |
| **Weeks 29 – 1.07** | Monitor early usage; quantitative survey (optional per plan) |

## Top 3 Risks

1. **Chair-discovery scope creep** — 27 heterogeneous chair websites; if #37 slips past week 14, the whole schedule slips. Mitigation: timebox to the most common page structures, manual fallback for the rest.
2. **WebSocket JWT in URL** — leaks tokens into logs/proxies; showstopper for any hosted deployment. Known fix, ~3–5 days; must land before staging.
3. **Hard-coded metrics in ChairExplorer** — fabricated team/citation numbers shown to professors whose #1 stated concern is trust. Hide before *any* demo.

## Top 3 Priorities, Next 2 Weeks

1. Review and merge **#35, then #37** (chair-discovery pipeline) — CI green via `gh pr checks`.
2. **File and schedule the security issue** (JWT → short-lived ticket or secure cookie).
3. **Audit ChairExplorer** for placeholder data; hide or mark "data unavailable."
