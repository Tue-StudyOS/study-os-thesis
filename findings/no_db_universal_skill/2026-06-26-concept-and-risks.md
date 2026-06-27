# No-DB Universal Skill — Concept, Grilling, and Decisions

- **Date:** 2026-06-26
- **Branch:** `feat/no-db-universal-skill` (off `codex/chair-discovery-eval-from-valentin`)
- **Status:** Direction agreed. Build plan not yet written.

---

## Context

This is a **university project**, not a scientific paper. The bar is: the
product works "well enough" to be useful, and *if* we can show empirically that
it works reasonably, that is large bonus points.

Two directions were on the table:

- **A (current):** Scrape and maintain a chair/professor database, CS Tübingen
  only, kept fresh via GitHub Actions.
- **B (new, chosen):** No database, no backend. The skill encodes *how Claude
  interviews and searches the live web*, working for all faculties of Tübingen
  immediately, and later companies.

**Decisive reason for B:** the team won't be around to maintain a database in a
few months, and no one will take it over. The system must be maintenance-free.
A "good enough" live-search result that needs no upkeep beats a precise database
that rots.

---

## The Concept (refined)

**Ordered conversation, not a free-for-all:**

1. **Interview first.** Ask the student about themselves and surface their
   interests — but **one question, max two per turn**, otherwise the
   conversation diverges. Instruct the user to answer precisely.
2. **Build an in-context user profile** from the answers (no persistence).
3. **Then search**, precisely, for the *set of possibilities* at the university
   and at companies that match the profile.
4. **Show what exists** — a map of options, not a finished proposal.
5. **Optionally show pros/cons / difficulties / good points** per option.

The agent gives **direction and clarifies options** — it does not do the whole
job for the student.

---

## The Grilling — Risks and Counter-Decisions

### 1. Web-search coverage is structurally incomplete
Many chairs have weak/outdated web presence or use terms no student would
search. The tool finds the *visible* chairs and the student may believe they see
the whole picture — the silent gaps are invisible.

**Decision:** Accept "good enough" coverage. This is the whole point — a
maintenance-free system that finds ~most options beats a rotting database.
Communicate the limitation honestly in the output ("you likely see most public
options; search the rest yourself"). Mitigation: also crawl official faculty
listing pages on `uni-tuebingen.de` as a backbone.

### 2. "Better than just asking Claude" must be earned
Claude in 2026 is already good at structured interviews and web search. The
skill's value cannot be "more structure" alone.

**Decision:** The differentiator is (a) the abstract instructions for *how* to
interview and *how* to scrape/search, encoded once and reused, and (b)
demonstrating empirically that the skill beats a plain Claude search. The core
hard problem of this project is: **how do we instruct Claude abstractly, well
enough, on how it searches and how it runs the conversation.**

### 3. Company discovery is a different, harder problem
Chairs are structured (university hierarchy, official pages). Companies are
chaotic; naive `Masterarbeit Unternehmen {topic}` mostly returns the usual
suspects (Bosch, SAP, Siemens).

**Decision:** Do companies **later**, university first. For companies, the likely
approach is a *one-time large pull* of an existing list (e.g. ~2000 companies for
Baden-Württemberg) tagged by area/hashtags (startups, etc.), bundled into the
skill. New startups joining later are a known gap to solve differently, probably
much later. This is the one place where a *bundled static list* is acceptable —
because there is no clean live-search equivalent.

### 4. How do we measure "works"?
Without a benchmark we can't claim coverage, and we'd be back to manually
maintaining chair names per faculty (the maintenance we're trying to escape).

**Decision:** Build a **small ground-truth sample**: manually curate chairs/
professors for **3–4 faculties** and verify the tool against it. Eval ≠ runtime
data — the ground truth is only for testing, not for operating the tool.

### 5. The honest value is the process, not a perfect output
The agent gives a targeted direction and clarifies options. ~70–80% coverage of
publicly visible options, stated transparently, is a feature not a bug.

**Decision:** State the coverage limitation explicitly in-conversation.

---

## Decisions Summary

| Question | Decision |
|---|---|
| University first or companies first? | **University first.** Companies are harder; prove the core first. |
| Keep any data at all? | **Only an eval ground truth** (3–4 faculties, manual), used for testing — not runtime. Plus a possible **bundled company list** later. |
| Search templates static or generated? | **Hybrid:** fixed backbone (faculty listing crawl + query skeletons) + profile-derived variables. |
| Output claim? | **Honest:** "most publicly visible options," coverage limits stated in-conversation. |
| Conversation style | **One question, max two per turn**; instruct user to answer precisely; build in-context profile before searching. |
| What proves the project? | Empirically showing the **skill beats plain Claude** search. |

---

## Key Open Items / Follow-up

1. **Eval harness (LOCATED):** Max's harness lets two agents talk to each other
   and run a conversation automatically. It lives on branch
   `eval/auto_eval_agents` (commit `ed341a7`, "test: add codex multiturn eval
   harness"):
   - `scripts/run_codex_multiturn_eval.py` — the runner
   - `skills/tests/simulations/personas/` — deep-user, standard-user, terse-user
   - `skills/tests/simulations/scenarios/ml-master-thesis.md`
   - `skills/tests/simulations/rubrics/conversation-rubric.md`
   - `skills/tests/test_codex_multiturn_eval.py`
   - `.github/workflows/codex-multiturn-evals.yml`
   → Plan: use this to evaluate the skill vs. plain Claude. Personas already model
   different answer styles (terse vs. deep), which fits our "one question per turn,
   answer precisely" design.
2. **Abstract search/interview instructions:** the core hard problem — write and
   iterate on how Claude is told to interview and to search.
3. **Ground-truth sample:** pick 3–4 faculties, curate chairs/professors,
   define the matching/coverage metric.
4. **Faculty-listing backbone:** identify the official `uni-tuebingen.de` pages
   that enumerate chairs per faculty, to reduce silent coverage gaps.
5. **Company list (later):** find an existing tagged company list for
   Baden-Württemberg; decide bundling format.

---

## Privacy

No student data is stored here or by the skill at runtime. The profile lives in
the conversation context only.
