---
name: run-thesis-simulations
description: Run and evaluate all repo-local thesis-finder simulation commands. Use when asked to run the thesis simulation suite, evaluate thesis-finder personas, execute all thesis-sim commands, or produce conversation and rating artifacts.
---

# Run Thesis Simulations

Run every repo-local `thesis-sim-*` command as an end-to-end `thesis-finder`
simulation, save the complete conversations, evaluate each run, and write a
central evaluation summary.

## Inputs

- Optional user request limiting the run to selected students or clients.
- Repo-local command files:
  - Claude: `.claude/commands/thesis-sim-*.md`
  - Codex: `.codex/prompts/thesis-sim-*.md`

## Workflow

1. Discover simulation commands.
   - Prefer the command directory for the active client:
     - Claude: `.claude/commands/thesis-sim-*.md`
     - Codex: `.codex/prompts/thesis-sim-*.md`
   - If the active client's directory is missing or empty, use the other one.
   - Sort commands by filename for deterministic order.
   - Exclude orchestration commands or non-student commands; run only files
     matching `thesis-sim-*.md`.
2. For each command file:
   - Read the complete file.
   - Treat the command content as the simulation specification.
   - Run the full simulated conversation in-character until the command's final
     artifact requirements are satisfied.
   - Use the repository's actual thesis skills when the command asks for them.
   - Do not write fictional student data to real runtime state such as
     `~/.claude/thesis-finder/session.md`; include any would-be session content
     in the conversation report instead.
3. Save the complete conversation.
   - Directory: `.simulations/convo`
   - Filename format: `student_conversation_dd.MM.YYYY-HH-mm-ss.md`
   - Generate the timestamp at write time.
   - If a filename collision occurs because two files are written in the same
     second, wait until the next second and retry. Do not add student names or
     counters to the filename.
4. Evaluate the conversation using `references/evaluation-rubric.md`.
   - Directory: `simulations/rating`
   - Filename format: `student_rating_dd.MM.YYYY-HH-mm-ss.md`
   - Each rating file must identify the student/command inside the Markdown
     body, not in the filename.
   - Use the same collision rule as conversation files.
5. After all individual ratings are saved, write one central evaluation file.
   - Directory: `simulations/rating`
   - Filename format: `student_rating_dd.MM.YYYY-HH-mm-ss.md`
   - Title it `# Central Thesis Simulation Evaluation`.
   - Summarize pass/fail, scores, recurring skill failures, and recommended
     improvements across all students.

## Conversation Artifact Requirements

Each conversation file must include:

- command filename and student name
- timestamp
- simulation setup
- full simulated conversation transcript
- completed six-dimension profile
- final thesis recommendation or explicit no-fit result
- sources used, if any
- any would-be session file content

## Rating Artifact Requirements

Each individual rating file must include:

- command filename and student name
- timestamp
- short verdict
- score table using the rubric
- evidence-grounded notes for each score
- issues, failure modes, or missing evidence
- concrete skill/package improvement suggestions

## Evidence And Safety Rules

- Do not invent chairs, companies, thesis openings, datasets, contacts,
  supervision capacity, application deadlines, or source evidence.
- Treat "no realistic company track" as a valid outcome for departments where
  company theses are structurally weak.
- Do not assume computer science, machine learning, or company fit. Route by
  the simulated student's department and profile.
- Keep generated fictional data only in `.simulations/convo` and
  `simulations/rating`, both of which must be gitignored.
- If web access is unavailable but the command requires live evidence, mark the
  affected ratings down under evidence discipline and state the limitation.

