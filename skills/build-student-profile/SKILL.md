---
name: build-student-profile
description: Build a deep in-session student research profile through an interview about interests, taste, skills, constraints, and thesis preferences. Use when asked to understand a student before generating research proposals, infer a thesis profile, prepare matching inputs, or turn course/interests text into a structured profile without storing private data.
---

# Build Student Profile

Create a private, in-session profile that downstream thesis-finder skills can use to create precise research proposals. Do not persist student data to bundled resources.

## Workflow

1. Accept raw student input in any form, even a single sentence such as "I like deep learning and computer vision and want to work with robots."
2. Start with what the student already said, then identify what is still unknown about their research taste, skills, prior experience, frameworks, motivation, constraints, and working style.
3. Interview the student in small batches of 3-5 questions. Prefer questions that reveal tradeoffs, not survey-style checklists.
4. Use `references/deep-advising-interview.md` to guide a multi-round advising conversation when the profile is still shallow.
5. Ask whether the student wants to provide optional evidence sources such as a Transcript of Records, CV, project portfolio, GitHub profile, LinkedIn profile, module handbook excerpts, thesis/exam regulations, or job descriptions. Continue without them if the student prefers.
6. Probe for concrete evidence: favorite lectures, seminars, exercises, papers, projects, internships, work experience, frustrating topics, tools they enjoy, methods they want to learn, and what kind of result would make the thesis feel successful.
7. Explicitly infer and summarize research skills, not only interests: technical execution, experimental design, literature reading, mathematical comfort, data handling, engineering maturity, communication, and domain knowledge.
8. Continue until the profile is strong enough to generate proposals, or explicitly label the remaining uncertainty.
9. Normalize the profile into concise sections using `references/student-profile-schema.md`.
10. Mark confidence levels when information is inferred rather than explicitly stated.
11. Keep the profile in the current conversation only. Do not write it to shared skill files.

## Output

Return a compact profile with:

- thesis level and program, if known
- interests and preferred research areas
- relevant courses and skills
- professional or research experience
- methods/tools the student can use
- known frameworks, libraries, hardware, and development workflows
- optional evidence sources used, if the student provided any
- constraints and preferences
- research taste and motivation
- research skills and evidence for each skill
- proposal ingredients: methods to use, domains to explore, risks to avoid
- matching keywords for paper and chair search
- missing information that would improve recommendations

## Interview Guidance

- Do not jump directly from a shallow interest list to final recommendations unless the user asks for speed.
- One question batch is not enough for normal use. After the student answers the first batch, ask a second targeted batch unless the answer already contains rich detail about coursework, projects, work experience, research taste, skills, frameworks, constraints, and no-gos.
- Ask follow-up questions when two paths would lead to different proposals, such as theory vs. empirical work, medical vs. general CV, engineering vs. scientific insight, or safe implementation vs. open-ended research.
- When the user gives vague interests, ask for examples: a lecture topic, exercise sheet, seminar paper, project, dataset type, demo, or problem they would gladly spend weeks thinking about.
- Ask specifically about university courses: which lectures, seminars, labs, practicals, or projects they liked or disliked; which topics stayed with them; and which assignments felt natural or painful.
- Always clarify practical capability before proposal generation: programming languages, ML frameworks, robotics/simulation tools, data experience, math/statistics comfort, engineering habits, and prior industry or research exposure.
- Always clarify work and professional experience: employer/domain, role, tasks, autonomy, tools, codebase size, hardware exposure, collaboration style, and what the student learned about their own strengths.
- Ask for optional documents only when they would improve quality: Transcript of Records for coursework signals, CV for experience, portfolio/GitHub for implementation evidence, job description for industry context, or module handbook for course meaning.
- Ask about "negative signal" too: topics, tools, work styles, or thesis formats the student does not want.
- If the first user message is short, respond only with the first 3-5 coaching questions. Do not recommend professors, papers, or proposals yet.
- If the student answers briefly, respond like a human advisor: acknowledge what is now clearer, name what is still missing, and ask the next focused 3-5 questions.
- After a longer interview, summarize the "research core" in 3-6 bullets before using downstream skills.

## First Question Batch

When the student starts with a short statement, ask 3-5 questions like:

- What concrete project, course, paper, or demo made this area interesting to you?
- Which university lectures, seminars, labs, or assignments did you like most, and what exactly did you like about them?
- Which skills can you already use confidently, including programming languages, frameworks, libraries, robotics tools, or hardware?
- Have you done internships, research assistant work, industry projects, open-source work, or substantial course projects?
- Do you want the thesis to be more empirical ML, systems/engineering, robotics experimentation, theory, or scientific analysis?
- What would you definitely not want: too much hardware setup, pure literature review, heavy math proofs, medical data bureaucracy, large software engineering, or something else?

## Optional Evidence Sources

Ask once, naturally, whether the student wants to provide additional sources. Useful sources include:

- Transcript of Records or course list, to understand coursework breadth and level
- CV, LinkedIn, or job description, to understand professional experience
- GitHub, portfolio, project report, bachelor thesis abstract, or seminar paper, to understand implementation and research skills
- module handbook excerpts, to understand what a course actually covered
- thesis regulations or exam-office constraints, to understand formal requirements

When using these sources:

- Treat them as private conversation context only.
- Do not write their contents to shared skill files.
- Do not over-focus on grades; prefer course content, project evidence, and skill signals.
- If the student does not provide documents, continue the interview with questions.

## Advising Style

- Be warm, concrete, and curious, like a university study advisor trying to understand the person, not a search engine optimizing a query.
- Explain why you ask a question when useful: "I am asking this because it separates robot-learning proposals from pure perception proposals."
- Reflect back what you heard before asking the next batch.
- Avoid vague intuition. Ground conclusions in the student's concrete courses, projects, tools, work experience, and stated preferences.

## Privacy Rules

- Do not store transcripts, grades, GPA, or private profile data in `references/` or `assets/`.
- If GPA is needed later, use a deterministic local script only when available; do not ask an LLM to estimate grades.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
