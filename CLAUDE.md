# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"
- In this project use the gh command to insure that CI passes. Ask to install this package if it can't be found.

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Issues & Pull Requests

**One issue = one focused change. One PR = one reviewable story.**

### Issues
- **Title:** short, imperative, prefixed with an area when useful (`UI:`, `RAG:`, `backend:`). e.g. "UI: add a favicon".
- **Body:** what's wrong / what's wanted, and why. Even one or two sentences beats an empty `-`. Add reproduction steps for bugs and a rough acceptance criterion ("done when …").
- **Labels:** tag the kind (`bug`, `feature`, `docs`, `chore`) so the board is scannable.

### Branches & commits
- Branch off `main`: `feat/…`, `fix/…`, `docs/…`, `ci/…`, `chore/…`.
- Conventional-commit subjects: `feat:`, `fix:`, `ci:`, `docs:`, `chore:` — imperative, lowercase, no trailing period.
- Body explains **what and why**, not line-by-line how. Wrap at ~72 chars.

### Pull requests
Scale the template to the change — a one-liner fix needs Summary + Closes; a big refactor uses all of it. **PR #12 is the gold standard.**

```markdown
## Summary
What this PR does, in 1–3 sentences.

## Motivation        (omit for trivial changes)
Why — the problem it solves.

## What Changed
- Grouped bullets, or a before/after table for multi-endpoint changes.

## Known Issues / Not Yet Done   (only if applicable)
- Honest list of gaps, with a pointer to any tracking doc.

## How to Run / Test  (when reviewers need it)
Exact commands.
```

Rules:
- Link the issue with `Closes #N` so it auto-closes on merge.
- Keep PRs small and single-purpose; split unrelated work.
- **CI must be green before requesting review** — use `gh pr checks` and iterate until it passes (see §4).
- Be honest about what's incomplete (the "Known Issues" section in PR #12 is a good model).

---

## 6. Workflow: Masterplan & Status

This project is tracked with two central files at the repo root:

- **[MASTERPLAN.md](MASTERPLAN.md)** — the zoomed-out, stable lookup: what we build, in what order, and why. Phases and the task list (A–H). **Read it first** to understand where any task fits. Only edit when the plan structurally changes.
- **[STATUS.md](STATUS.md)** — the single living document. Progress, blockers, difficulties, decisions, and a dated log. **When you work on a task, update STATUS.md** (task status + a dated log line) — never put running progress in the Masterplan.

Rule of thumb: Masterplan answers "what's the plan?", STATUS answers "where are we right now?". The exact, agent-runnable task list lives in `findings/no_db_universal_skill/2026-06-26-build-plan.md`.

We work **without GitHub issues** — just for ourselves. Track work through STATUS.md and the build plan, not issues.

---

## 7. Commits & Conversation Handoff

We work task-by-task (Tasks A–H in the build plan), one task per conversation.

### Commit rhythm
- Make **frequent small commits** as you complete meaningful sub-steps of a task — not one giant commit at the end.
- Each commit message must reasonably describe **what was done** (conventional-commit subject + a short body when useful).
- Commit only when a sub-step is coherent and the tree is in a sane state.

### End-of-task handoff (mandatory)
When a task is **truly finished** (done-when criteria met, committed), end the conversation by producing two things:

1. **Next-step explanation** — a short, plain description of what the next task is and how this task's output feeds into it.
2. **A ready-to-paste handoff prompt** for the next conversation, inside a fenced code block, that gives the next agent everything it needs to continue seamlessly **without re-reading this whole conversation**. It must include:
   - the active branch
   - which task it is (letter + one-line goal) and its dependencies
   - the key files to read first (build plan, MASTERPLAN, STATUS, relevant references/skills)
   - what the previous task produced and where
   - the concrete done-when criteria
   - a reminder to commit in small steps and to emit its own handoff prompt at the end

The point: I can paste the prompt into a fresh conversation and the next task continues with full context.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
