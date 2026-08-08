---
name: thesis-finder
description: Single entry point for thesis discovery. Helps a student sharpen what kind of thesis fits them and then find where to write it. Builds the student profile through an inline interview if not yet present, then routes to university chair discovery (find-university-chairs), company thesis discovery (find-company-thesis-options), or both, based on student choice. Records the student's own thesis self-understanding before and after the search. Supports multi-session continuity: detects prior searches and resumes without re-interviewing. Use when a student wants to find where to write their thesis — no prior skill invocation needed.
---

# Thesis Finder

Single entry point for thesis-option discovery. Routes to the appropriate discovery skill(s) and maintains a persistent session log (see **Session File Location** below) so searches can resume across weeks without starting over.

---

## Step 0 — Detect session state (do this before anything else)

Resolve the session file path (see **Session File Location** below), then attempt to read it.

- **File not found** → new user. Follow the **New User Flow** below.
- **File found** → returning user. Follow the **Returning User Flow** below.

Use the resolved path for every later read and write in this skill.

---

## New User Flow

Before starting the interview, give the student a short one-time framing message:

> "This skill helps you work out what kind of thesis actually fits you, and then find where you could write it — at a university chair, a company, or both. The questions are as much a part of that as the results: most students finish with a sharper sense of what they want than they started with. How much detail you give is entirely up to you — more detail makes the search more precise, but there's no minimum required. Once the profile is done, I'll ask whether you want to search university chairs, companies, or both."

### Step N0 — Capture the starting point (one turn, before any other question)

Ask exactly this and wait for the answer:

> "Before we start: in one or two sentences, what kind of thesis do you think you're looking for right now? A rough or uncertain answer is fine and useful — we'll come back to it at the end."

Record the answer **verbatim** — do not clean it up, summarise it, or correct it. It goes into the session file as the starting statement. If the student declines or says they have no idea, record exactly that; "no idea" is a real and useful starting point.

Do not comment on the answer, do not evaluate it, and do not start searching. Move straight to Step N1.

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

After delivering results, create the session file at the path resolved in Step 0 (create its parent directory if it does not exist). Use the session file format defined at the end of this skill.

Populate:
- **Thesis Self-Understanding log**: the verbatim starting statement from Step N0, dated, marked "before first search"
- **Student Profile section**: compact 6D snapshot from the interview
- **Active Candidates table**: all options surfaced (status: "Found")
- **Search Log — Session 1**: track chosen, key directions, candidates found, any dead-ends noted during discovery

### Step N5 — Recommend, then obey the student's branch choice

This is a two-turn gate. Do not treat the question as rhetorical.

1. From the delivered option map(s), pick 1-2 top options and give a short "why this one" line for each — grounded only in the relevance rationale already present in the map. Do not invent facts not already in the map.
2. Ask exactly: "Want to go deeper on [the recommended option(s)] before reaching out, or keep exploring other options?"
3. Stop and wait for the student's answer.

#### Step N5a — If the student wants to go deeper

The next assistant message must be the drill-down, not a contact-email offer and not only a generic outreach angle. Skipping directly to `draft-thesis-contact` after "go deeper" is a workflow failure.

1. If 1-2 recent papers from the selected person/lab/team are not already available in-session, call `find-recent-papers` for that specific option before writing the drill-down. For humanities, social-science, company, or practice-oriented options where recent papers are not the right evidence type or none are found, say that plainly and use only the verified option-map evidence plus any verified project, collection, teaching, careers, or institute pages already gathered.
2. Present a section headed `## Deeper Look: [selected option]` with:
   - **Fit in one sentence** — why this option is the top fit, grounded in the option map.
   - **Evidence anchors** — 1-2 papers, projects, official pages, collections, or job/thesis pages used for the drill-down, with dates or "not found" where appropriate.
   - **What you'd likely work on / learn** — concrete thesis work derived only from the option map and evidence anchors.
   - **Feasibility checks** — data/material access, method scope, language, prerequisites, supervision/thesis availability, and any no-go risks to verify.
   - **First meeting question** — one precise question the student can ask before drafting an email.
3. Update that option's Status to "Recommended" in the Active Candidates table in `session.md`.
4. Only after this drill-down is complete, proceed to Step N6.

#### Step N5b — If the student wants to keep exploring

Skip the drill-down and ask what adjacent direction, constraint, or track they want to explore next before running another search.

### Step N6 — Close the loop on the starting statement

Ask exactly this and wait for the answer:

> "Same question as at the start: in one or two sentences, what kind of thesis are you looking for now?"

Record the answer **verbatim** in the session file next to the starting statement, with today's date.

Then show the student both statements side by side and say what changed, in one or two sentences — narrower, wider, shifted, or unchanged. Do not editorialise and do not claim progress that is not visible in the two texts. "These are close to identical" is a legitimate and honest outcome; say it when it is true.

If the student's own words became less certain rather than more, treat that as a real result too, and say so plainly. Discovering that a direction was wrong is worth as much as confirming one.

### Step N7 — Offer next step

> "`draft-thesis-contact` can draft a first-contact email for any option you choose."

---

## Returning User Flow

### Step R1 — Load session state

Read the session file (the path resolved in Step 0) in full. Extract:
- Thesis Self-Understanding log — in particular the **first** entry, needed for the comparison in Step R7. Do not re-ask the starting question; it was already answered in an earlier session.
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

Append a new session block to the session file (the path resolved in Step 0):
- New entry in the Search Log (date, track, directions, new candidates, new dead-ends)
- Refresh the Active Candidates table: add new finds; update statuses the student mentioned
- Add newly ruled-out items to the Dead-Ends list
- Update the Student Profile section only if interests changed in Step R3

### Step R6 — Recommend, then obey the student's branch choice

Only run this step if Step R4 produced a fresh option map (a new `find-university-chairs` and/or `find-company-thesis-options` run). If the student went straight to `draft-thesis-contact` on an existing candidate in Step R3, skip ahead to Step R7 — the self-understanding check still runs.

1. From the fresh option map, pick 1-2 top options and give a short "why this one" line for each — grounded only in the relevance rationale already present in the map. Do not invent facts not already in the map.
2. Ask exactly: "Want to go deeper on [the recommended option(s)] before reaching out, or keep exploring other options?"
3. Stop and wait for the student's answer.
4. If the student wants to go deeper, follow Step N5a exactly. The next assistant message must be headed `## Deeper Look: [selected option]` and must include the required fit, evidence, likely work, feasibility, and first-meeting fields before Step R7.
6. Proceed to Step R7 once the branch is resolved.
5. If the student wants to keep exploring, follow Step N5b.

### Step R7 — Close the loop on the starting statement

Ask exactly this and wait for the answer:

> "In one or two sentences, what kind of thesis are you looking for now?"

Record the answer **verbatim** in the session file's self-understanding log with today's date, appended after the existing entries — never overwrite an earlier statement.

Then show the student their **first** statement and this one, and say what changed across the whole search, in one or two sentences. Because these are weeks apart, this is the most informative comparison the skill produces. Do not claim progress that is not visible in the two texts; "unchanged" and "less certain than before" are legitimate outcomes to report plainly.

If the session file has **no** self-understanding log — it was written by an older version of this skill — do not invent an earlier statement and do not reconstruct one from the profile. Record today's answer as the first entry, say that no earlier statement exists to compare against, and note that the comparison becomes available from the next session onward.

### Step R8 — Offer next step

> "`draft-thesis-contact` can draft a first-contact email for any option you choose."

---

## Session File Format

### Session File Location

**Preferred path:** `~/.claude/thesis-finder/session.md`

**Fallback:** if that path is unavailable — the client has no home-directory access, writes outside the working directory are refused, or the read fails for any reason other than "file does not exist" — keep the session log at `./thesis-finder-session.md` in the current working directory instead, and **say so in your first reply**: name the path you are using and that the log will be found there next time.

Check the fallback path too when detecting session state in Step 0, so a returning student is recognised regardless of which path the previous run used. If both exist, use the preferred path and mention the duplicate.

This file is runtime state — it is never bundled in skill releases. The path is a convention; the file is owned by the user.

The **Thesis Self-Understanding** log is append-only. Each entry is the student's own
wording, never a paraphrase, and earlier entries are never edited or deleted — the value
of the log is that it shows change over time in the student's own words.

```markdown
# Thesis Search Session

## Thesis Self-Understanding (append-only, student's own words)
| Date | Point in flow | Verbatim statement |
|------|---------------|--------------------|
| YYYY-MM-DD | before first search | "..." |
| YYYY-MM-DD | after session N | "..." |

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
