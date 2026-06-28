---
name: thesis-finder
description: Entry-point orchestrator for thesis discovery. Routes to university chair discovery (find-university-chairs), company thesis discovery (find-company-thesis-options), or both, based on student choice. Requires a complete 6-dimension student profile from build-student-profile before routing. Use when a student is ready to look for where to write their thesis and wants to be routed to the right discovery skill(s).
---

# Thesis Finder

Single entry point for thesis-option discovery. This skill checks for a student profile and
routes to the appropriate discovery skill(s). It contains no discovery logic itself.

## Step 1 — Profile check

Check whether the current conversation contains a complete student profile from
`build-student-profile` covering all six dimensions:

1. Interests, 2. Methods, 3. Domain, 4. Thesis style, 5. Skills, 6. No-gos

**If any dimension is missing or shallow:** stop and say:

> "Run `build-student-profile` first to complete your profile, then return here."

Do not proceed until all six dimensions are present.

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
| **(a)** | Invoke `find-university-chairs` |
| **(b)** | Invoke `find-company-thesis-options` |
| **(c)** | Invoke `find-university-chairs` first; deliver its option map. Then invoke `find-company-thesis-options`; deliver its option map under a `---` separator and a `## Company Thesis Options (Baden-Württemberg)` header. No cross-ranking between the two maps. |

## Step 4 — Offer next step

After delivering the option map(s), say:

> "`draft-thesis-contact` can draft a first-contact email for any option you choose."
