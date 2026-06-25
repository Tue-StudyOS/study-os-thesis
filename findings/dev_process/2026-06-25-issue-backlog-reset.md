# Issue Backlog Reset And Skill-Package Goal

## Date

2026-06-25

## Context

The repository pivoted from a hosted web app/backend/UI product to a portable
Agent Skill package for thesis advising. After reviewing the open GitHub
issues, old app/backend/UI issues were closed as superseded.

## Finding

The active backlog should focus on the skill-package data foundation and
governance work. Only issues `#45`-`#51` remain active from the preexisting
backlog:

- `#45` resolve OpenAlex author IDs for all 47 seed professors
- `#46` build hand-verified pilot ground truth
- `#47` discover PhDs/researchers per chair
- `#48` define the Prof -> Researcher/PhD -> Paper schema
- `#49` fetch papers and generate topic/description Markdown
- `#50` add validation harness
- `#51` add refresh automation

Important missing work is not represented by the old closed issues. It should be
tracked as new skill-package issues: faculty portability, Markdown filesystem
policy, monthly refresh workflow, monthly eval snapshots, privacy/public-data
policy, and the findings/dev-process log.

## Implication

Future maintainers should not reopen old web-app issues to represent the new
product. New work should be phrased in terms of portable skills, Markdown
references, evidence quality, data maintenance, release artifacts, and evals.

## Follow-Up

Create focused issues for:

- faculty-extension guidance in `AGENTS.md`
- Markdown data filesystem and update policy
- monthly data refresh workflow with review PR
- monthly eval snapshots
- privacy and public-data policy
- findings/dev-process log maintenance
