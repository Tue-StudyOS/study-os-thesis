---
name: thesis-finder
description: Single entry point for thesis discovery. Builds the student profile through an inline interview if not yet present, then routes to university chair discovery (find-university-chairs), company thesis discovery (find-company-thesis-options), or both, based on student choice. Supports multi-session continuity: detects prior searches and resumes without re-interviewing. Use when a student wants to find where to write their thesis — no prior skill invocation needed.
---

# Thesis Finder

Single entry point for thesis-option discovery. Routes to the appropriate discovery skill(s) and maintains a persistent session log at `~/.claude/thesis-finder/session.md` so searches can resume across weeks without starting over.

---

## Step 0 — Detect session state (do this before anything else)

Attempt to read `~/.claude/thesis-finder/session.md`.

- **File not found** → new user. Follow the **New User Flow** below.
- **File found** → returning user. Follow the **Returning User Flow** below.

---

## New User Flow

### Step N1 — Build student profile

Check whether the current conversation already contains a complete 6-dimension student profile:

1. Interests, 2. Methods, 3. Domain, 4. Thesis style, 5. Skills, 6. No-gos

**If the profile is already complete:** proceed to Step N2.

**If the profile is missing or any dimension is shallow:** build it now through a short interview.
- Ask **one question per turn** (at most two when tightly coupled).
- Use `../build-student-profile/references/deep-advising-interview.md` to guide the conversation.
- Ask for optional evidence sources (transcript, CV, GitHub) once, naturally.
- **Tools and libraries are not a standalone question.** Infer them from courses, projects, and experience mentioned; note explicitly only if the student volunteers them.
- Continue until all six dimensions are covered.

Do not proceed to Step N2 until all six dimensions are present.

### Step N2 — Ask which track

Once the profile is confirmed complete, ask exactly this:

> "Which option type do you want to explore?
> (a) University thesis at Tübingen
> (b) Company thesis in **Baden-Württemberg** (BW-region only)
> (c) Both"

Wait for the student's answer before continuing.

### Step N3 — Route

| Choice | Action |
|--------|--------|
| **(a)** | Invoke `find-university-chairs`, then deliver its option map. |
| **(b)** | Invoke `find-company-thesis-options`, then deliver its option map. |
| **(c)** | Invoke `find-university-chairs` **and** `find-company-thesis-options` — complete **both** searches before delivering any output. Deliver both maps together: university first, `---` separator, then company under `## Company Thesis Options (Baden-Württemberg)`. No cross-ranking. |

### Step N4 — Write session file

After delivering results, create `~/.claude/thesis-finder/session.md` (create the `~/.claude/thesis-finder/` directory if it does not exist). Use the session file format defined at the end of this skill.

Populate:
- **Student Profile section**: compact 6D snapshot from the interview
- **Active Candidates table**: all options surfaced (status: "Found")
- **Search Log — Session 1**: track chosen, key directions, candidates found, any dead-ends noted during discovery

### Step N5 — Offer next step

> "`draft-thesis-contact` can draft a first-contact email for any option you choose."

---

## Returning User Flow

### Step R1 — Load session state

Read `~/.claude/thesis-finder/session.md` in full. Extract:
- Student profile (6D snapshot)
- Active candidates and their statuses
- Dead-ends list
- Date and track of the last session

### Step R2 — Show summary and ask for brief update

Display a one-line summary:

> "Last searched [date] ([track]). [N] active candidate(s) found so far."

Then ask exactly this — nothing more:

> "In 1–2 sentences: what's your current status? Any change in direction?"

Wait for the answer. **Do not re-run the full interview.** Do not ask follow-up questions about dimensions already in the profile. A wrong re-interview produces wrong search directions.

### Step R3 — Assess direction

Based on the student's update, decide which path to take:

| Situation | Action |
|-----------|--------|
| Good candidates exist, student wants to reach out | Recommend `draft-thesis-contact`; still offer to search more if wanted |
| Profile too narrow — all directions exhausted, no good fit | Ask **1–2 targeted questions** to uncover adjacent interests; update the profile section in session.md before continuing |
| Student wants a different track (e.g., now wants companies) | Note the shift; ask which track; proceed to Step R4 |
| Student wants to continue in the same direction | Proceed to Step R4 directly |

### Step R4 — Route with dead-end exclusions

Ask which track if not already clear (same options a/b/c).

Pass the dead-ends from the session file as explicit exclusions to the discovery skill:

> "Skip the following — already ruled out: [dead-ends list from session file]."

| Choice | Action |
|--------|--------|
| **(a)** | Invoke `find-university-chairs` with exclusions, deliver option map. |
| **(b)** | Invoke `find-company-thesis-options` with exclusions, deliver option map. |
| **(c)** | Invoke both with exclusions, deliver combined map (university first, then company). |

### Step R5 — Update session file

Append a new session block to `~/.claude/thesis-finder/session.md`:
- New entry in the Search Log (date, track, directions, new candidates, new dead-ends)
- Refresh the Active Candidates table: add new finds; update statuses the student mentioned
- Add newly ruled-out items to the Dead-Ends list
- Update the Student Profile section only if interests changed in Step R3

### Step R6 — Offer next step

> "`draft-thesis-contact` can draft a first-contact email for any option you choose."

---

## Session File Format

**Location:** `~/.claude/thesis-finder/session.md`

This file is runtime state — it is never bundled in skill releases. The path is the convention; the file is owned by the user.

```markdown
# Thesis Search Session

## Student Profile (updated: YYYY-MM-DD)
Interests: ...
Methods: ...
Domain: ...
Thesis style: ...
Skills: ...
No-gos: ...

## Active Candidates
| Name | Institution / Company | Track | Status | Last Updated |
|------|-----------------------|-------|--------|--------------|

## Dead-Ends (skip in future searches)
- [Name / Department / Company]: [reason — why not a fit]

## Search Log

### Session N — YYYY-MM-DD — [university | company | both]
**Searched:** [key directions / queries]
**New candidates:** [names]
**Dead-ends added:** [what failed and why]
**Notes:** [interest shifts or decisions]
```
