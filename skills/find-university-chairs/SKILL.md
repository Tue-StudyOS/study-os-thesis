---
name: find-university-chairs
description: Find and rank university teaching chairs, research groups, professors, and possible thesis supervisors for a student's thesis interests. Use when asked which chair, lab, professor, PhD student, research group, or university supervisor fits a topic, course profile, paper list, or thesis direction.
---

# Find University Chairs

Help a student identify relevant chairs, labs, and supervisor candidates for a thesis conversation.

## Workflow

1. Extract the student's thesis interests, strongest skills, constraints, degree program, and any preferred methods or application areas.
2. Read the professor seed list at `references/professors/INDEX.md`.
3. Select likely professor/URI candidates from the seed list using the student's interests and any explicitly named chairs, professors, or topics.
4. Use the active agent's native websearch/browser tools on those URIs to identify the research group, team members, research areas, and recent publications.
5. Rank candidates by research fit, evidence quality, source freshness, and thesis-preparation value.
6. Prepare the student for a high-signal first contact rather than presenting fixed thesis topics as guaranteed openings.
7. If the active agent has no websearch/browser tools, explain that the seed list only contains names and URIs and ask the user to provide page contents or enable browsing.

## Output

For each recommended chair or supervisor include:

- Chair, lab, or group name
- Relevant person when available
- Research-fit rationale
- Evidence with source names and dates when available
- Possible thesis conversation starters
- Prerequisites or preparation suggestions
- Caveats about stale, missing, or ambiguous data

End with a concise contact-preparation checklist.

## Evidence Rules

- Prefer official university pages, lab pages, publication pages, and recent papers.
- Do not invent openings, quotas, team sizes, citation counts, or willingness to supervise.
- Distinguish research areas from concrete thesis topics.
- Treat public web data as potentially stale and date the evidence.
- Do not treat old bundled chair, researcher, or paper profiles as the primary source; the Excel-derived professor seed list plus live research is authoritative for discovery.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
