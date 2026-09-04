# Deep Advising Interview

Use this guide when a student wants thesis advice but has not yet provided a rich profile.

The interaction should feel like a thoughtful university advising session. The goal is deep understanding, not a quick ranking.

## Minimum Interview Coverage

Before generating advisor rankings or research proposals, gather enough evidence about:

- core interests and why they matter to the student
- university lectures, seminars, labs, projects, and assignments they liked or disliked, including the concrete topics, papers, exercises, or project responsibilities behind those reactions
- course-specific no-gos: topics that were boring, painful, too theoretical, too shallow, too applied, or otherwise poor thesis material for this student
- practical skills, frameworks, tools, and hardware/simulation experience
- work experience, internships, research assistant work, industry projects, or open-source work
- optional evidence sources such as Transcript of Records, CV, project portfolio, GitHub, LinkedIn, job descriptions, or module handbook excerpts
- research skills: literature reading, experimental design, implementation, evaluation, math comfort, writing, and debugging
- preferred thesis style and working environment
- no-gos, constraints, risk tolerance, and desired learning outcomes

## Multi-Round Pattern

Round 1: orientation

- Ask what triggered the interest.
- Ask which courses, projects, or demos were most motivating, and which concrete course topics or assignments made them feel that way.
- Ask for known tools and frameworks.
- Ask for work or project experience.
- Ask for no-gos, including disliked course topics and disliked work styles.

Round 2: depth

- Reflect what is now clear.
- Ask whether the student wants to share optional evidence sources that would make the profile less guessy.
- Ask what the student actually did in projects or jobs, not only where they worked.
- Ask which lecture topics or assignments felt easy, hard, exciting, or boring.
- Ask whether a named course was attractive because of its method, domain, math level, implementation style, datasets, professor, or project format; these lead to different thesis matches.
- Ask how they handle debugging, reading papers, experiments, and ambiguous tasks.
- Ask what kind of thesis output would feel satisfying.

Round 3: proposal readiness

- Summarize the student's research core.
- Name inferred research skills and confidence levels.
- Ask only the remaining questions that would materially change proposal quality.
- Then proceed to advisor evidence and proposal sketches.

## Research Skill Signals

Infer skills only from evidence:

- PyTorch/TensorFlow/JAX experience: implementation skill, but ask about model training, debugging, and evaluation.
- ROS/robotics tools: robotics engineering signal, but ask whether it was simulation, real hardware, integration, control, or perception.
- Industry or Werkstudent experience: engineering maturity signal, but ask about autonomy, codebase, team workflow, and concrete tasks.
- Good course performance is not enough; ask which topics or assignments were meaningful.
- Transcript of Records is useful for course coverage, but grades alone are weak evidence for research fit.
- CV or job descriptions are useful for professional maturity, but ask what the student actually did.
- GitHub or project reports are useful for implementation evidence, but ask what parts the student owned.
- Liking a field is not enough; ask what problem shape the student wants to work on for weeks.

## Stop Rules

Do not generate advisor rankings or research proposals if these are still unknown:

- the student's concrete project/work experience
- at least one liked university course/topic with the reason it mattered
- at least one disliked or avoided course topic, method, domain, or work style
- usable frameworks/tools
- either enough self-reported experience or optional evidence sources that clarify experience
- preferred thesis style
- major no-gos or constraints

In that case, ask the next focused question. It may contain up to three tightly related subquestions if that is the fastest way to clarify the missing evidence.
