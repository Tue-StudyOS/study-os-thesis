---
name: generate-thesis-directions
description: Generate precise research-proposal sketches, thesis questions, and advisor-ready conversation starters from a deep student profile, recent paper evidence, and chair or supervisor matches. Use when asked for research proposals, thesis proposal ideas, proposal directions, topic hypotheses, or questions to discuss with a potential advisor.
---

# Generate Thesis Directions

Turn evidence from a deep student profile, papers, and chair matches into precise research-proposal sketches that a student can discuss with a supervisor.

## Workflow

1. Start from an in-session student profile and a small set of chair/researcher matches. If the profile is shallow, ask targeted follow-up questions before generating final proposals.
2. Use recent papers and official chair/lab pages gathered by `find-recent-papers` and `find-university-chairs` as grounding evidence.
3. Read `references/research-proposal-rubric.md` before finalizing proposals.
4. Generate 2-4 proposal sketches, each narrow enough to become a first supervisor conversation.
5. For each proposal, state the research question, motivation, method, expected evidence, feasibility assumptions, required background, advisor fit, and first validation step.
6. Label the evidence status for each proposal: external posting/snippet-derived lead, research-area conversation starter, or feasibility hypothesis requiring verification.
7. Label uncertainty and avoid presenting proposals as official open topics.

## Output

For each proposal include:

- working title
- research question
- motivation from cited evidence
- possible methods/data/evaluation
- fit to chair/person
- evidence status: external posting/snippet-derived lead, research-area conversation starter, or feasibility hypothesis
- prerequisites
- feasibility risks and how to de-risk them
- first question to ask in a meeting

## Rules

- Say "proposal sketch", "possible direction", or "conversation starter", not "available thesis topic".
- Do not invent datasets, hardware access, supervision capacity, or chair approval.
- Prefer fewer, sharper proposals over many generic ideas.
- Make the student's personal fit visible: why this proposal fits their skills, curiosity, and preferred working style.
- Do not treat old bundled chair, researcher, or paper profiles as the primary source.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
