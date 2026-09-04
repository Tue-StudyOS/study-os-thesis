# 2026-09-04 Thesis Finder Fresh Profile Regression

## Date

2026-09-04

## Context

Recent thesis-finder runs were compared against older high-quality user
sessions for probabilistic ML, reinforcement learning, and finance/quant thesis
discovery. The newer runs often began by checking old session state and narrowed
recommendations too quickly.

Validation note: the attempted full live black-box simulation on 2026-09-04 hung
before writing artifacts, and the bounded nested Codex runner also stalled
before first output. The completed validation for this change was therefore the
deterministic test suite plus the repo's fixture/discovery comparison artifacts,
not a full fresh live eight-persona black-box run.

## Finding

Persistent session lookup/resume behavior is a quality regression for fresh
thesis advising. It can anchor the agent to stale candidates, add awkward reset
turns, and distract from the deep profile interview that made the baseline
sessions useful. The baseline sessions performed better when the agent built a
fresh profile from current course content, project evidence, disliked topics,
no-gos, skills, and thesis-style preferences before discovery.

Recommendation quality also depends on providing multiple thesis-angle variants
per strong chair/company option. A single top topic makes the output feel
overcommitted and reduces the student's ability to choose a direction for the
drill-down.

## Implication

`thesis-finder` should remain fresh-session only unless the student explicitly
pastes prior context into the active conversation. Simulation prompts and
evaluation contracts must treat old-session reads/writes as workflow failures,
and must check that option maps and drill-downs include topic menus or thesis
variants.

## Follow-Up Or Linked Issue

- Runtime skills updated to forbid session lookup/persistence and to require
  deeper course/no-go profiling plus multiple topic angles.
- Codex/Claude simulation contracts and persona prompts updated to require a
  session-persistence check instead of would-be session content.
- Deterministic tests added for fresh-session behavior, profile-depth signals,
  topic-angle menus, and simulation-contract alignment.
- Full live simulation runner reliability remains a separate maintenance issue;
  do not treat this finding as proof that the live black-box harness is healthy.
