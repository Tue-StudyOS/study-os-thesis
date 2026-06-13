---
name: build-student-profile
description: Build an in-session student thesis profile from user-provided interests, courses, skills, constraints, degree context, and thesis preferences. Use when asked to infer a thesis profile, summarize a student's background, prepare matching inputs, or turn course/interests text into a structured profile without storing private data.
---

# Build Student Profile

Create a private, in-session profile that downstream thesis-finder skills can use. Do not persist student data to bundled resources.

## Workflow

1. Extract the student's stated interests, courses, skills, methods, domain preferences, constraints, language preferences, thesis level, and timing.
2. Ask only for missing information that materially changes matching quality.
3. Normalize the profile into concise sections using `references/student-profile-schema.md`.
4. Mark confidence levels when information is inferred rather than explicitly stated.
5. Keep the profile in the current conversation only. Do not write it to shared skill files.

## Output

Return a compact profile with:

- thesis level and program, if known
- interests and preferred research areas
- relevant courses and skills
- methods/tools the student can use
- constraints and preferences
- matching keywords for paper and chair search
- missing information that would improve recommendations

## Privacy Rules

- Do not store transcripts, grades, GPA, or private profile data in `references/` or `assets/`.
- If GPA is needed later, use a deterministic local script only when available; do not ask an LLM to estimate grades.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
