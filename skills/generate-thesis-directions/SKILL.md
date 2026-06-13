---
name: generate-thesis-directions
description: Generate concrete thesis directions, research questions, and conversation starters from a student profile, recent paper evidence, and chair or supervisor matches. Use when asked for thesis ideas, proposal directions, topic hypotheses, or questions to discuss with a potential advisor.
---

# Generate Thesis Directions

Turn evidence from profiles, papers, and chair matches into thesis directions that a student can discuss with a supervisor.

## Workflow

1. Start from an in-session student profile and a small set of chair/researcher matches.
2. Use recent papers and official chair/lab pages gathered by `find-recent-papers` and `find-university-chairs` as grounding evidence.
3. Generate 3-5 thesis directions, each scoped as a conversation starter.
4. For each direction, state the research question, possible method, required background, and why the suggested chair/person is relevant.
5. Label uncertainty and avoid presenting directions as official open topics.

## Output

For each direction include:

- working title
- research question
- motivation from cited evidence
- possible methods/data
- fit to chair/person
- prerequisites
- first question to ask in a meeting

## Rules

- Say "possible direction" or "conversation starter", not "available thesis topic".
- Do not invent datasets, hardware access, supervision capacity, or chair approval.
- Do not treat old bundled chair, researcher, or paper profiles as the primary source.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
