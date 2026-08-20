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
4. Read the thesis level and thesis duration from the profile before drafting, and size the proposals against that budget rather than against a generic thesis. If the profile records the duration as unresolved, pick the scope you can defend, state which duration you assumed, and flag it as something to confirm — do not silently assume the longer case.
5. Generate 2-4 proposal sketches, each narrow enough to become a first supervisor conversation.
6. For each proposal, state the research question, motivation, method, expected evidence, feasibility assumptions, required background, advisor fit, and first validation step.
7. Label uncertainty and avoid presenting proposals as official open topics.

## Output

For each proposal include:

- working title
- research question
- motivation from cited evidence
- possible methods/data/evaluation
- fit to chair/person
- prerequisites
- feasibility risks and how to de-risk them, including whether the work fits the student's thesis duration
- first question to ask in a meeting

## Rules

- Say "proposal sketch", "possible direction", or "conversation starter", not "available thesis topic".
- Do not invent datasets, hardware access, supervision capacity, or chair approval.
- Prefer fewer, sharper proposals over many generic ideas.
- Scope to the recorded duration, not to the level label. "It is a master thesis" is not a time budget: the Bearbeitungszeit is set per faculty and per Fassung, so two master students can have materially different windows (see `build-student-profile/references/degree-program-rules.md`).
- Make the student's personal fit visible: why this proposal fits their skills, curiosity, and preferred working style.
- This skill has no runtime database, index, or bundled entity data. Ground every proposal in evidence gathered live during this session.
