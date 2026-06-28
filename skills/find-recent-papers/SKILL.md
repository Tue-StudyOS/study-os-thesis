---
name: find-recent-papers
description: Find, rank, and summarize recent research papers for thesis discovery. Use when a student or coding agent asks for papers, publications, related work, recent research directions, literature leads, or thesis ideas based on interests, courses, skills, chairs, supervisors, or research areas.
---

# Find Recent Papers

Help a student discover recent research papers that can guide a thesis direction.

## Workflow

1. Clarify the search intent from the user's interests, courses, skills, preferred methods, constraints, or target chairs.
2. If chairs or professors are relevant, read the professor seed list for the student's faculty — a faculty-specific `../find-university-chairs/references/<faculty>/professors/INDEX.md` when one exists (e.g. `.../sociology/professors/INDEX.md`), otherwise the default `../find-university-chairs/references/professors/INDEX.md` — to find official starting URIs.
3. Use the active agent's native websearch/browser tools on official profile, lab, publication, Google Scholar, OpenAlex, DBLP, or publisher pages to find papers.
4. Prefer recent, primary, and traceable sources. Use `references/paper-search-rubric.md` for source ranking and output rules.
5. Return a short ranked list, not an exhaustive bibliography.
6. Explain why each paper matters for thesis discovery, including likely methods, prerequisites, and possible follow-up questions.
7. If the active agent has no websearch/browser tools, explain that live paper discovery is unavailable and ask the user to provide publication pages or paper metadata.

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
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
