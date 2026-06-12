# Technical Status & Roadmap

**StudyOS Thesis Advisor — Research Package, Report 2 of 5**
**Date:** 2026-06-11 · **Deadline:** 1.07.2026 production-ready
**Verified against live repo state:** 5 open PRs, 16 open issues (as of 2026-06-11)

---

## 1. Architecture Assessment

| Component | State | Notes |
|---|---|---|
| FastAPI + async SQLAlchemy | Mature | External review (StudyOS bot) confirms "real MVP, not demo" |
| Database migrations | Stable | Alembic chain 0001–0014, recent fixes landed (parent refs, down_revisions corrected in last 5 commits) |
| Frontend (React/Vite) | Feature-complete for MVP | i18n nearly done (PR #38, current branch) |
| LLM integration (Ollama / gemma4) | Working | Local-first; DeepSeek path has known duplicate bug (#33) |
| Celery/Redis job queue | Working | WebSocket job events functional, but see security item below |
| PostgreSQL + pgvector | Mature | No changes needed |

Two non-feature items from the external review must be treated as **deployment blockers**:

- **Security:** WebSocket JWT passed in URL query string (`frontend/src/api/jobEvents.ts`, `backend/app/ws/controller.py`). URLs leak into server logs, proxies, and browser history. Must move to a short-lived ticket or secure cookie before any hosted deployment.
- **Trust:** `ChairExplorer.tsx` hard-codes metrics (team sizes, citation counts). Showing fabricated numbers to the exact professors who told us trust is their main concern (Report 1, §3.4) would be self-inflicted damage. Hide or mark unavailable until backed by real scraped data.

---

## 2. Feature Checklist vs MVP Goal

MVP goal (Plan.docx): *"After <1 hour, users have a much better idea which chair to contact + infrastructure for easy chair updates."*

| Feature | Status |
|---|---|
| Transcript (TOR) upload | ✅ Working |
| Competency profile | ✅ Working (computation is dummy — #16/PR #21) |
| Semantic chair matching | ✅ Working |
| Proposal generation | ✅ Working |
| Settings + i18n (DE/EN) | 🔄 PR #38 (this branch), closes #23/#29 scope |
| Auto-discovery of chair info | 🔄 PR #35 + #37 (closes #22/#36) |

**Assessment: student-facing MVP is ~90% complete.** The "infrastructure for easy chair updates" half lives entirely in the #35→#37 pipeline — that is the critical path.

---

## 3. Open PR Prioritization

| PR | Title | Priority | Rationale |
|---|---|---|---|
| #35 | chair & university-employee schema groundwork | **P0 — merge first** | Prerequisite for #37; everything downstream rebases on this schema |
| #37 | chair-discovery scraping agent | **P0 — critical path** | The feedback-validated core feature (Macke: "reads the relevant section in our website… much more excited about"). Closes #36/#22 |
| #38 | i18n translation for all pages | **P1 — merge before deployment** | Done work, low risk; merging it clears the branch backlog |
| #21 | skill computation | **P2** | Replaces dummy competency computation (#16); needed for profile accuracy in the RAG phase, not for schema work now |
| #34 | dedup DOI-less re-scrapes | **P2** | Data-quality polish; becomes more important once #37 scrapes at scale |

Suggested merge order: **#35 → #37 → #38 → #34 → #21** (with #38 mergeable any time it doesn't conflict).

## 4. Open Issue Prioritization vs Timeline

### Weeks 8–14 (NOW — auto-discovery phase)
- **#36 / #22** — chair-discovery agent: land PRs #35 + #37. The gate for everything else.
- **#18** — startup loading icon bug: small, fix opportunistically.
- **#15** — UI formatting error: ditto.

### Weeks 15–21 (RAG phase)
- **#7** — optimize RAG capabilities (the named goal of this phase).
- **#16** — replace dummy skill computation (land PR #21 here).
- **#33** — DeepSeek duplicate papers (fix before any showcase — duplicated data is a trust issue).
- **#6** — add deepeval: do early in this phase; you can't claim RAG "improved" without an eval harness.
- **#32** — paper tags: supports better retrieval, fits here.

### Weeks 22–28 (deployment phase)
- **Security audit:** WebSocket JWT → ticket/cookie (no issue filed yet — **file one**).
- **Trust audit:** ChairExplorer hard-coded metrics (no issue filed yet — **file one**).
- **Docs alignment:** README says "no cloud accounts needed" but config supports Azure/DeepSeek — fix before external eyes see it.
- **#25** — markdown rendering (visible polish for first users).
- **#29** — help/settings page (if remainder not covered by #38).

### Weeks 29–1.07 (survey/buffer)
- Quantitative survey setup (Google Forms, per Plan.docx "nice-to-have").
- Bug reports from early users.
- **Deferred:** #14 (starting prompt), #4 (OCR engine), #5 (port-adapter pattern), #13 (DeepSeek testing). #5 in particular is an architecture refactor with no MVP payoff — explicitly out of scope per CLAUDE.md simplicity rules.

---

## 5. Critical Path to 1.07

```
Week 8–10   Merge #35, stabilize #37 (review, CI green, rebase chain)
Week 11–14  Chair-discovery agent running against real chair pages;
            merge #38, #34; fix #18/#15 opportunistically
Week 15–16  deepeval harness (#6) + baseline RAG metrics
Week 17–19  RAG optimization (#7), skill computation (#21/#16), #33
Week 20–21  Full RAG retest against baseline
Week 22–24  Security fix (JWT), trust fix (ChairExplorer), README/docs
Week 25–26  Staging deployment, smoke tests
Week 27–28  Final bugfixes, polish (#25)
Week 29–1.07 Monitor early usage; survey if time allows
```

Per CLAUDE.md §4: every phase gate is "CI green via `gh pr checks`" — no phase starts on a red main.

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Chair-discovery (#37) scope creep — 27+ chairs with heterogeneous websites (Typo3, custom, Overleaf-exported PDFs) | **High** | Schedule slip cascades | Timebox: support the 5–8 most common page structures first; manual fallback entries for the rest. "Works for 20 of 27 chairs" is a fine MVP |
| JWT-in-URL discovered at demo/hosting time | Medium | Showstopper for trust with dept | Fix in week 22 at latest; it's a 3–5 day change, schedule it explicitly |
| Hard-coded ChairExplorer metrics shown to a professor | Medium | Credibility loss with the exact audience that demands honesty | Hide/flag before *any* demo, not just before deployment |
| RAG phase eats deployment buffer | Medium | Weeks 22–28 compress | RAG improvements are non-blocking for MVP — cut #7 scope before cutting deployment tasks |
| Team capacity (Valentin Mon/Wed) | Known constraint | Throughput ceiling | Scope above already assumes this; the deferred-issue list is the pressure valve |
| Technical debt | Low | — | Nothing identified that blocks MVP |

**Bottom line: tight but doable.** The schedule holds if #35+#37 land by week 14. Everything in weeks 15–21 can shrink; the security and trust fixes in weeks 22–24 cannot.
