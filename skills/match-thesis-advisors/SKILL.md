---
name: match-thesis-advisors
description: Match a deep student research profile to professors, chairs, researchers, and recent papers using the professor seed index plus native web research. Use when asked to find proposal-relevant advisors, rank chairs or supervisors, compare matches, explain fit, or prepare evidence for precise research proposals without a database or UI.
---

# Match Thesis Advisors

Rank possible thesis advisors by combining the student's in-session research profile with the professor seed index and evidence gathered from official web sources. Treat the ranking as input to research-proposal generation, not as the final product.

## Workflow

1. Build or reuse a deep student profile. If the user only gave broad interests or one short answer batch, use `build-student-profile` first and ask the next 3-5 coaching questions.
2. Read `../find-university-chairs/references/professors/INDEX.md` for professor names and official starting URIs.
3. Use `find-university-chairs` and `find-recent-papers` to gather current public evidence with the active agent's native websearch/browser tools.
4. Score candidates qualitatively by proposal fit, research taste fit, evidence freshness, prerequisite fit, and risk.
5. Return a ranked shortlist with reasons, caveats, backup options, and proposal hooks.

## Output

For each match include:

- chair/lab and relevant person
- fit summary
- evidence from official pages or publication sources
- matching papers or research areas
- prerequisites and preparation
- risks or caveats
- proposal hooks that could become research questions
- suggested next action

End with 2-3 backup directions if the top matches are too competitive or uncertain.

## Rules

- Do not produce advisor rankings from a shallow profile or after only one brief question batch. Ask profile-building questions first.
- Do not invent supervision capacity, open topics, quotas, team sizes, citations, or willingness to supervise.
- Distinguish "strong research fit" from "confirmed available thesis topic".
- Do not treat old bundled chair, researcher, or paper profiles as the primary source.
- If websearch/browser tools are unavailable, say that advisor matching can only use the professor seed names and URIs until the user provides page contents or enables browsing.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
