# Deep Advising Interview

Use this guide when a student wants thesis advice but has not yet provided a rich profile.

The interaction should feel like a thoughtful university advising session. The goal is deep understanding, not a quick ranking.

## Conversation Rhythm

- Ask one question per turn by default.
- Ask at most two questions in a turn, and only when they clarify the same aspect.
- Stay on one aspect until the student's answer gives enough signal, then move to the next aspect with a short transition.
- Do not mix profile discovery, advisor matching, paper search, and proposal generation in the same turn.
- Prefer natural follow-ups over survey-style batches.

## Minimum Interview Coverage

Before generating advisor rankings or research proposals, gather enough evidence about:

- core interests and why they matter to the student
- university lectures, seminars, labs, projects, and assignments they liked or disliked
- practical skills, frameworks, tools, and hardware/simulation experience
- work experience, internships, research assistant work, industry projects, or open-source work
- optional evidence sources such as Transcript of Records, CV, project portfolio, GitHub, LinkedIn, job descriptions, or module handbook excerpts
- research skills: literature reading, experimental design, implementation, evaluation, math comfort, writing, and debugging
- preferred thesis style and working environment
- no-gos, constraints, risk tolerance, and desired learning outcomes

## Multi-Round Pattern

Round 1: orientation

Focus first on motivation and coursework:

- Ask what triggered the interest.
- After that is clear, ask which courses, projects, or demos were most motivating.

Round 2: depth

- Reflect what is now clear.
- Focus next on skills and experience:
  - Ask what tools or frameworks the student can use.
  - Ask what the student actually did in projects or jobs, not only where they worked.
  - Ask how they handle debugging, reading papers, experiments, and ambiguous tasks when that would change proposal fit.

Round 3: proposal readiness

- Summarize the student's research core.
- Name inferred research skills and confidence levels.
- Ask only the remaining one or two questions that would materially change proposal quality, such as thesis style, no-gos, constraints, or optional evidence sources.
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
- at least one liked or disliked university course/topic
- usable frameworks/tools
- either enough self-reported experience or optional evidence sources that clarify experience
- preferred thesis style
- major no-gos or constraints

In that case, ask the next focused question about the highest-impact missing aspect.
