---
name: find-recent-papers
description: Find, rank, and summarize recent research papers for thesis discovery. Use when a student or coding agent asks for papers, publications, related work, recent research directions, literature leads, or thesis ideas based on interests, courses, skills, chairs, supervisors, or research areas.
---

# Find Recent Papers

Help a student discover recent research papers that can guide a thesis direction.

## Workflow

1. Clarify the search intent from the user's deep profile: interests, concrete coursework, project/work evidence, skills, preferred methods, constraints, working style, and target chairs.
2. If the student profile is shallow and the user is asking for paper-based thesis directions, use `build-student-profile` first and ask the next focused coaching question instead of turning broad keywords into paper recommendations.
3. If chairs or professors are relevant, read the professor seed list at `../find-university-chairs/references/professors/INDEX.md` to find official starting URIs.
4. Use the active agent's native websearch/browser tools on official profile, lab, publication, Google Scholar, OpenAlex, DBLP, or publisher pages to find papers.
5. Prefer recent, primary, and traceable sources. Use `references/paper-search-rubric.md` for source ranking and output rules.
6. Return a short ranked list, not an exhaustive bibliography.
7. Explain why each paper matters for thesis discovery, including likely methods, prerequisites, and possible follow-up questions.
8. If the active agent has no websearch/browser tools, explain that live paper discovery is unavailable and ask the user to provide publication pages or paper metadata.

## Output

For each paper include:

- Title
- Year or publication date
- Authors
- Venue or source
- Link or DOI when available
- Short relevance rationale
- Thesis angle or question the student could discuss with a supervisor

End with suggested next searches or chair/supervisor connections when evidence supports them.

## Evidence Rules

- Clearly label preprints, surveys, workshop papers, and unpublished material.
- Do not fabricate citation counts, venues, acceptance status, or author affiliations.
- If sources disagree or data may be stale, say so.
- Use absolute dates for "recent" results whenever possible.
- Do not treat old bundled paper or researcher profiles as the primary source.
- Do not use papers as a shortcut to thesis directions when the student has only provided a few keywords. Build the high-fidelity profile first, unless the user explicitly asks for a low-confidence exploratory paper scan.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
