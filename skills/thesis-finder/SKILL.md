---
name: thesis-finder
description: Single entry point for thesis discovery. Builds a fresh in-session student profile through a detailed inline interview, then routes to university chair discovery (find-university-chairs), company thesis discovery (find-company-thesis-options), or both, based on student choice. Use when a student wants to find where to write a bachelor or master thesis — no prior skill invocation needed.
---

# Thesis Finder

Single entry point for thesis-option discovery. Routes to the appropriate discovery skill(s) from a fresh profile built in the current conversation.

---

## Ground Rules

- Do **not** search for, read, write, summarize, or resume old thesis-finder sessions or conversation logs.
- Treat every thesis-finder invocation as a fresh advising session unless the student explicitly includes prior profile details in the current conversation.
- Keep private student data in the active conversation only. Do not persist session files such as `~/.claude/thesis-finder/session.md` or local fallback files.
- If the student says they already have a profile or previous result, ask them to paste the relevant parts they want reused.

Before starting the interview, give the student a short one-time framing message:

> "This skill helps you find where to write your thesis — at a university chair, a company, or both. I'll first ask a few questions to build a profile of your interests, skills, and preferences; how much detail you give is up to you, but precise course, project, skill, and no-go details make the search useful. Once the profile is complete, I'll ask whether you want to search university chairs, companies, or both."

## Workflow

### Step 1 — Build student profile

Check whether the current conversation already contains a complete 6-dimension student profile:

1. Interests, 2. Methods, 3. Domain, 4. Thesis style, 5. Skills, 6. No-gos

**If the profile is already complete in the current conversation:** proceed to Step 2.

**If the profile is missing or any dimension is shallow:** build it now through a short interview.
- Ask **one primary question per turn**, but make it rich: include concrete prompts or examples when they help the student answer with useful detail. Use at most three tightly related subquestions when a single broad answer would otherwise stay too vague.
- Use `../build-student-profile/references/deep-advising-interview.md` to guide the conversation.
- Ask for optional evidence sources (transcript, CV, GitHub) once, naturally.
- Ask specifically about course content, not only course names: lectures, seminars, labs, assignments, papers, or exercises the student liked or disliked, and which topics felt exciting, painful, too theoretical, too shallow, or worth spending months on.
- Ask specifically about negative course/topic signals: no-go domains, methods, tools, thesis formats, supervision styles, and course topics the student wants to avoid.
- Ask about practical execution through projects, work experience, tools, frameworks, data/simulation/hardware exposure, debugging, evaluation, and writing.
- Continue until all six dimensions are covered with concrete evidence.
- If the student refuses more profiling before all six dimensions are present, do **not** route to `find-university-chairs` or `find-company-thesis-options`. Offer only a generic, clearly non-personalized pointer and explain that tailored discovery requires the complete profile.

Do not proceed to Step 2 until all six dimensions are present.

### Step 2 — Ask which track

Once the profile is confirmed complete, ask exactly this:

> "Which option type do you want to explore?
> (a) University thesis at Tübingen
> (b) Company thesis in **Baden-Württemberg** (BW-region only)
> (c) Both"

Wait for the student's answer before continuing.

### Step 3 — Route

| Choice | Action |
|--------|--------|
| **(a)** | Invoke `find-university-chairs`, then deliver its option map. |
| **(b)** | Invoke `find-company-thesis-options`, then deliver its option map. |
| **(c)** | Invoke `find-university-chairs` **and** `find-company-thesis-options` — complete **both** searches before delivering any output. Deliver both maps together: university first, `---` separator, then company under `## Company Thesis Options (Baden-Württemberg)`. No cross-ranking. |

### Step 4 — Recommend, then obey the student's branch choice

This is a two-turn gate. Do not treat the question as rhetorical.

1. From the delivered option map(s), pick 2-3 top options when enough viable options exist. Give a short "why this one" line for each, grounded only in the relevance rationale already present in the map.
2. Under each recommended option, include a **topic menu** with 2-4 distinct possible thesis directions or conversation starters. These are tentative proposal sketches, not official openings. Vary them by method, data/evidence, and risk profile so the student can choose a direction rather than only a single topic.
3. Ask exactly: "Want to go deeper on one of these options/topics before reaching out, or keep exploring other options?"
4. Stop and wait for the student's answer.

#### Step 4a — If the student wants to go deeper

The next assistant message must be the drill-down, not a contact-email offer and not only a generic outreach angle. Skipping directly to `draft-thesis-contact` after "go deeper" is a workflow failure.

1. If 1-2 recent papers from the selected person/lab/team are not already available in-session, call `find-recent-papers` for that specific option before writing the drill-down. For humanities, social-science, company, or practice-oriented options where recent papers are not the right evidence type or none are found, say that plainly and use only the verified option-map evidence plus any verified project, collection, teaching, careers, or institute pages already gathered.
2. Present a section headed `## Deeper Look: [selected option]` with:
   - **Fit in one sentence** — why this option is the top fit, grounded in the option map.
   - **Evidence anchors** — 1-2 papers, projects, official pages, collections, or job/thesis pages used for the drill-down, with dates or "not found" where appropriate.
   - **What you'd likely work on / learn** — concrete thesis work derived only from the option map and evidence anchors.
   - **Feasibility checks** — data/material access, method scope, language, prerequisites, supervision/thesis availability, and any no-go risks to verify.
   - **Topic variants** — 2-4 concrete thesis directions for that same option, each with a working title, research question, likely method/evidence, and main risk to validate.
   - **First meeting question** — one precise question the student can ask before drafting an email.
3. Only after this drill-down is complete, proceed to Step 5.

#### Step 4b — If the student wants to keep exploring

Skip the drill-down and ask what adjacent direction, constraint, or track they want to explore next before running another search.

### Step 5 — Offer next step

> "`draft-thesis-contact` can draft a first-contact email for any option you choose."
