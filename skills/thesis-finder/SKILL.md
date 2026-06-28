---
name: thesis-finder
description: Single entry point for thesis discovery. Builds the student profile through an inline interview if not yet present, then routes to university chair discovery (find-university-chairs), company thesis discovery (find-company-thesis-options), or both, based on student choice. Use when a student wants to find where to write their thesis — no prior skill invocation needed.
---

# Thesis Finder

Single entry point for thesis-option discovery. This skill builds the student profile inline
if needed, then routes to the appropriate discovery skill(s). It contains no discovery logic itself.

## Step 1 — Build or check student profile

Check whether the current conversation already contains a complete 6-dimension student profile:

1. Interests, 2. Methods, 3. Domain, 4. Thesis style, 5. Skills, 6. No-gos

**If the profile is already complete:** proceed to Step 2.

**If the profile is missing or any dimension is shallow:** build it now through a short interview.
- Ask **one question per turn** (at most two when tightly coupled).
- Use `../build-student-profile/references/deep-advising-interview.md` to guide the conversation.
- Ask for optional evidence sources (transcript, CV, GitHub) once, naturally.
- **Tools and libraries are not asked as a standalone question.** Infer them from courses, projects, and experience mentioned. Only note them explicitly if the student volunteers them.
- Continue until the five core dimensions are covered: interests, methods, domain, thesis style, no-gos.

Do not proceed to Step 2 until all six dimensions are present.

## Step 2 — Ask which track

Once the profile is confirmed complete, ask exactly this:

> "Which option type do you want to explore?
> (a) University thesis at Tübingen
> (b) Company thesis in Baden-Württemberg
> (c) Both"

Wait for the student's answer before continuing.

## Step 3 — Route

| Choice | Action |
|--------|--------|
| **(a)** | Invoke `find-university-chairs`, then deliver its option map. |
| **(b)** | Invoke `find-company-thesis-options`, then deliver its option map. |
| **(c)** | Invoke `find-university-chairs` **and** `find-company-thesis-options` — complete **both** searches before delivering any output. Then deliver both option maps together: university map first, a `---` separator, then the company map under `## Company Thesis Options (Baden-Württemberg)`. No cross-ranking between the two maps. |

## Step 4 — Offer next step

After delivering the option map(s), say:

> "`draft-thesis-contact` can draft a first-contact email for any option you choose."
