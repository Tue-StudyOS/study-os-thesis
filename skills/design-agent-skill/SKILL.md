---
name: design-agent-skill
description: Design, review, or improve portable Agent Skills with SKILL.md files. Use when asked to create a new skill, split an agent workflow into skills, write skill instructions, evaluate skill portability across agents such as Codex, Claude Code, OpenCode, or similar clients, or generate a skill package for thesis-finder workflows.
---

# Design Agent Skill

Create small, portable Agent Skills that another coding agent can use without knowing the project history.

## Workflow

1. Identify the user's repeatable task, expected trigger phrases, inputs, outputs, and failure modes.
2. Decide whether the task needs one skill or several focused skills. Prefer separate skills when workflows have different triggers, resources, or outputs.
3. Write a concise `SKILL.md` with portable frontmatter:
   - `name`: lowercase letters, digits, and hyphens only.
   - `description`: include what the skill does and when to use it; this is the trigger surface.
4. Put only core procedure in `SKILL.md`. Move detailed rubrics, schemas, examples, and source lists into `references/`.
5. Add deterministic scripts only when repeated calculation or parsing would otherwise be fragile.
6. Validate the skill folder against the checklist in `references/skill-authoring-rules.md`.

## Design Rules

- Optimize for agent portability. Do not require Claude-only, Codex-only, or OpenCode-only metadata unless the user asks for a client-specific variant.
- Prefer resources over long instructions. A skill should teach the agent where to look and how to decide, not paste every possible fact into the main file.
- Make outputs evidence-based. Require dates, source names, and explicit uncertainty when data may be stale.
- Avoid hidden infrastructure assumptions. If a skill needs web search, local files, scripts, or bundled data, say so plainly.
- Keep student-private data out of shared resources.

## Thesis-Finder Skill Pattern

For thesis discovery, split the system into focused skills:

- `build-student-profile` interviews the student deeply enough to capture research taste, motivation, skills, and constraints.
- `find-recent-papers` uses native web/search tools to find recent papers and explain thesis relevance.
- `find-university-chairs` uses live web search (faculty backbone + enrichment queries) to identify labs, teams, and research areas across all faculties.
- `generate-thesis-directions` turns discovery results and papers into precise research-proposal sketches and conversation starters.
- `draft-thesis-contact` drafts concise, specific first-contact messages around one proposal sketch.
- Meta skills create or update the skill package itself.

Student-facing skills must not depend on a database, API, Docker service, FastAPI app, or the old UI. Use native web/search tools when the active agent provides them. If browsing is unavailable, say so explicitly.
