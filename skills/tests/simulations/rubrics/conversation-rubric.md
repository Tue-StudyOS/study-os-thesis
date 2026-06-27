# DeepEval Conversation Rubric

Use these criteria to evaluate the complete multi-turn conversation, not a
single answer in isolation.

## Metrics

- `workflow_compliance`: The assistant follows the thesis skill workflow:
  profile-building first, then evidence gathering and downstream suggestions
  only when enough profile context exists.
- `profile_depth`: The conversation captures interests, coursework, skills,
  methods/tools, experience, constraints, no-gos, research taste, and matching
  keywords where possible.
- `shallow_profile_guardrail`: With shallow input, the assistant asks better
  questions instead of producing premature chair rankings or confident thesis
  proposals.
- `memory_retention`: Later assistant turns correctly reuse details from
  earlier student turns without inventing missing facts.
- `question_quality`: Follow-up questions are small, relevant, and easy for
  the student to answer.
- `evidence_discipline`: The assistant avoids fabricated papers, venues,
  citation counts, openings, quotas, team sizes, capacity, and willingness to
  supervise.
- `student_usefulness`: The conversation ends with a practical next step that
  fits the student's current profile depth.
- `user_simulation_realism`: User turns behave like a realistic student
  matching the persona, without acting like an assistant, evaluator, or advisor,
  and without revealing the full hidden profile too early.

## Shared Threshold

Each metric should pass at `0.75` or higher for live LLM evals.

---

# Discovery Rubric (medicine-discovery scenarios)

These metrics apply specifically to the medicine-discovery scenario pair and are
scored deterministically (no LLM judge required) by the comparison runner.

## Metrics

- `discovery_coverage`: Recall = (ground-truth chairs mentioned by name or
  unambiguous group reference) / (total chairs in the faculty ground-truth
  file). A chair counts as surfaced if its holder's last name appears in the
  assistant turns. Target: skill arm ≥ 0.50; baseline arm expected lower.

- `discovery_relevance`: Of the chairs surfaced by the assistant, what fraction
  are genuinely relevant to the student persona's stated interests
  (neurodegeneration, Parkinson's/Alzheimer's, protein aggregation)? Scored
  per-chair against the interest-area column in the ground-truth file.
  Expected: skill arm surfaces more directly relevant chairs than baseline.

- `discovery_structure`: Does the assistant output include a structured MAP
  (grouped sections with chair name, research area, and a fit/caveat note)?
  Binary check: passes if the skill-arm transcript contains at least one
  `**[` section header and at least two named chair entries.

## Scoring Guide

Run `scripts/run_codex_multiturn_eval.py --discovery-comparison` to produce a
`dist/discovery-comparison/comparison.md` artifact with per-arm scores on all
three metrics.
