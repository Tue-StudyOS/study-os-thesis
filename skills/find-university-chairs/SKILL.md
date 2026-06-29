---
name: find-university-chairs
description: Find university teaching chairs, research groups, professors, and possible thesis supervisors only after a sufficiently deep student research profile exists. Use when asked which chair, lab, professor, PhD student, research group, or university supervisor fits a topic, course profile, paper list, thesis direction, or research proposal.
---

# Find University Chairs

Help a student identify relevant chairs, labs, and supervisor candidates for a thesis conversation. If the student's profile is shallow, first deepen the profile instead of ranking chairs.

## Workflow

1. Check whether a deep student profile already exists in the conversation and satisfies the readiness gate in `../build-student-profile/references/advising-baseline.md`.
2. If the profile is shallow, raw, based only on broad interests, or missing major dimensions, use `build-student-profile` first and ask only the next focused coaching question. Do not recommend chairs yet.
3. Continue chair research only after the profile includes at least: Tuebingen degree program/thesis level, interests and motivation, liked and disliked university courses/topics, practical skills, research skills, known frameworks/tools, prior project or work experience with role/ownership, preferred thesis style, working and supervision style, career goals, and important no-gos or constraints.
4. Read the professor seed list at `references/professors/INDEX.md`.
5. Select likely professor/URI candidates from the seed list using the student's deep profile and any explicitly named chairs, professors, or topics.
6. Use the active agent's native websearch/browser tools on those URIs to identify the research group, team members, research areas, and recent publications.
7. Rank candidates by proposal fit, research taste fit, evidence quality, source freshness, and thesis-preparation value.
8. Prepare the student for a high-signal first contact rather than presenting fixed thesis topics as guaranteed openings.
9. If the active agent has no websearch/browser tools, explain that the seed list only contains names and URIs and ask the user to provide page contents or enable browsing.

## Shallow Profile Guardrail

When the user says something like "I am interested in deep learning, computer vision, and robots; where can I write my thesis?", do not answer with a chair shortlist. Start with one focused coaching question about the highest-impact missing aspect, then continue one aspect at a time:

- concrete projects, courses, papers, demos, or robotics experiences behind the interest
- lectures, seminars, labs, assignments, or university topics the student liked or disliked
- programming languages, ML frameworks, CV libraries, robotics/simulation tools, and hardware experience
- internships, research assistant work, industry work, open-source work, or substantial course projects
- research skills such as literature reading, experimental design, debugging, evaluation, math comfort, and scientific writing
- preferred thesis style: empirical ML, robot experiments, systems/engineering, theory, or scientific analysis
- working style, supervision preferences, career goals, and what kind of thesis outcome would feel successful
- no-gos such as hardware setup, pure literature review, heavy proofs, data bureaucracy, or large software engineering

Do not jump from "ML Master at Tuebingen, likes neural networks/RL/CV, has one PyTorch project, dislikes theory" to ranked Tuebingen chairs such as AVG, ASL, Kuehne, MPI-IS, or companies. Ask about coursework details, project ownership, work/HiWi/internship experience, evaluation habits, working style, and goals first.

Do not ask which university the student attends. Treat University of Tuebingen as prior context and ask only for degree program or thesis level when it is ambiguous.

If the user explicitly asks for speed, or provides a rich imported profile/CV/transcript/project context, an exploratory shortlist is allowed only when labeled low confidence with the missing profile dimensions listed.

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
