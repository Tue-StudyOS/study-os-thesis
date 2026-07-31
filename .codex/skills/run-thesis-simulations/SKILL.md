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

1. Decide the artifact root.
   - Default: `.simulations/current`.
   - For before/after architecture comparisons, use
     `.simulations/baseline/{timestamp}` for the pre-change run and
     `.simulations/rules-only/{timestamp}` for the post-change run.
2. Discover simulation commands.
   - Prefer the command directory for the active client:
     - Claude: `.claude/commands/thesis-sim-*.md`
     - Codex: `.codex/prompts/thesis-sim-*.md`
   - If the active client's directory is missing or empty, use the other one.
   - Sort commands by filename for deterministic order.
   - Exclude orchestration commands or non-student commands; run only files
     matching `thesis-sim-*.md`.
3. For each command file:
   - Read the complete file.
   - Treat the command content as the simulation specification.
   - Run the full simulated conversation in-character until the command's final
     artifact requirements are satisfied.
   - Use the repository's actual thesis skills when the command asks for them.
   - Do not write fictional student data to real runtime state such as
     `~/.claude/thesis-finder/session.md`; include any would-be session content
     in the conversation report instead.
4. Save the complete conversation.
   - Directory: `{artifact-root}/convo`
   - Filename format: `{student-slug}_conversation_dd.MM.YYYY-HH-mm-ss.md`
   - Use the lowercase student name or command slug, for example
     `maja_conversation_28.07.2026-22-10-06.md`.
   - Generate the timestamp at write time.
   - If a filename collision occurs because two files are written in the same
     second, wait until the next second and retry. Do not add student names or
     counters to the filename.
5. Evaluate the conversation using `references/evaluation-rubric.md`.
   - Directory: `{artifact-root}/rating`
   - Filename format: `{student-slug}_rating_dd.MM.YYYY-HH-mm-ss.md`
   - Use the same student slug as the conversation file.
   - Each rating file must identify the student/command inside the Markdown
     body, not in the filename.
   - Use the same collision rule as conversation files.
   - Include diagnostic fields:
     `Verified URLs: N`, `Unconfirmed claims: N`, `Wall-clock seconds: N`
     when measurable, `Company/CS misrouting: yes|no` for Jan, Simon, and
     Maja, and `Both tracks or structural company limit: yes|no` for Tina.
6. After all individual ratings are saved, write one central evaluation file.
   - Directory: `{artifact-root}/rating`
   - Filename format: `central_rating_dd.MM.YYYY-HH-mm-ss.md`
   - Title it `# Central Thesis Simulation Evaluation`.
   - Summarize pass/fail, scores, recurring skill failures, and recommended
     improvements across all students.
7. For before/after comparisons, run
   `python scripts/compare_command_simulation_performance.py --baseline-dir .simulations/baseline/{timestamp} --candidate-dir .simulations/rules-only/{timestamp}`
   and include the comparison verdict in the central summary.

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
- For rules-only backbone evaluations, judge whether live discovery found
  profile-relevant verified candidates without relying on static company or
  faculty URI lists.
- Do not assume computer science, machine learning, or company fit. Route by
  the simulated student's department and profile.
- Keep generated fictional data only under the selected artifact root's
  `convo/` and `rating/` subdirectories, for example
  `.simulations/current/convo`, `.simulations/baseline/{timestamp}/rating`, or
  `.simulations/rules-only/{timestamp}/rating`. These paths must be gitignored.
- If web access is unavailable but the command requires live evidence, mark the
  affected ratings down under evidence discipline and state the limitation.
