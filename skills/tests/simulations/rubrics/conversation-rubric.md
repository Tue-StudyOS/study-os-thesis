# DeepEval Conversation Rubric

Use these criteria to evaluate the complete multi-turn conversation, not a
single answer in isolation.

## Metrics

- `workflow_compliance`: The assistant follows the thesis skill workflow:
  profile-building first, then evidence gathering and downstream suggestions
  only when enough profile context exists.
- `profile_depth`: The conversation captures interests, coursework, skills,
  methods/tools, experience, project/work ownership, research skills, working
  style, supervision preferences, career goals, constraints, no-gos, research
  taste, and matching keywords where possible.
- `shallow_profile_guardrail`: With shallow input, the assistant asks better
  questions instead of producing premature chair rankings, company leads,
  paper-based thesis directions, or confident thesis proposals. A moderate
  profile with program, a few interests, one project, tools, and one no-go is
  still not enough for recommendations.
- `memory_retention`: Later assistant turns correctly reuse details from
  earlier student turns without inventing missing facts.
- `question_quality`: Follow-up questions are small, relevant, and easy for
  the student to answer. Good turns reflect what was learned, interpret what it
  may imply, name the highest-impact gap, and ask one focused next question.
- `evidence_discipline`: The assistant avoids fabricated papers, venues,
  citation counts, openings, quotas, team sizes, capacity, and willingness to
  supervise.
- `student_usefulness`: The conversation ends with a practical next step that
  fits the student's current profile depth. For shallow or moderate profiles,
  the next step should be another high-signal discovery question, not a
  recommendation.
- `user_simulation_realism`: User turns behave like a realistic student
  matching the persona, without acting like an assistant, evaluator, or advisor,
  and without revealing the full hidden profile too early.

## Shared Threshold

Each metric should pass at `0.75` or higher for live LLM evals.
