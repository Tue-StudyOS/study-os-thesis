# AGENTS.md

This repository is a public, extensible Agent Skill package for thesis advising.
It helps students move from personal interests, coursework, skills, and
constraints to evidence-based thesis directions and advisor-ready contact
messages.

The durable product is the skill package itself:

- portable `skills/` folders with `SKILL.md` entrypoints
- Markdown `references/` files for rubrics, schemas, indexes, examples, and
  public source data
- lightweight maintenance scripts, tests, and documentation

Treat these files as the source of truth. Future work should make the skills
clearer, more portable, better evidenced, and easier for students and
maintainers to use.

## Core Rule: Use The Meta-Skill First

All new skills and all substantial redesigns of existing skills must start with
`skills/design-agent-skill`.

Before adding or reshaping a skill:

1. Read `skills/design-agent-skill/SKILL.md`.
2. Use it to identify the repeatable task, trigger phrases, inputs, outputs,
   evidence needs, and failure modes.
3. Validate the result against
   `skills/design-agent-skill/references/skill-authoring-rules.md`.
4. Keep the main `SKILL.md` concise and move detailed rubrics, schemas,
   examples, and source lists into `references/`.

Do not invent a new skill structure ad hoc. The meta-skill exists so future
students and maintainers can extend the package consistently after the original
authors are unavailable.

## Student Workflow

The normal student-facing workflow is:

1. `build-student-profile`
2. `find-recent-papers` and/or `find-university-chairs`
3. `match-thesis-advisors`
4. `generate-thesis-directions`
5. `draft-thesis-contact`

Do not skip directly to chair rankings, thesis proposals, or contact emails
from a shallow profile. Good thesis advice starts with understanding the
student's research taste, coursework, skills, experience, constraints, and
no-gos.

## Skill Responsibilities

### `design-agent-skill`

Intent: create, review, or improve portable Agent Skills.

Use when a user asks to create a new skill, split a workflow into skills, write
skill instructions, review portability, or change the thesis-finder skill
package itself.

Inputs:

- the repeatable task or workflow to encode
- expected users and trigger phrases
- required inputs and outputs
- known sources, scripts, references, and failure modes

Outputs:

- a focused skill design
- concise `SKILL.md` instructions
- references or validation guidance when needed

Guardrails:

- optimize for portability across capable coding agents
- avoid client-specific metadata unless explicitly requested
- keep student-private data out of shared resources
- require evidence, dates, and uncertainty labels for stale-prone facts

### `build-student-profile`

Intent: build a deep, private, in-session student research profile.

Use when a student gives interests, courses, transcript details, CV context,
project history, thesis preferences, or asks for recommendations without enough
profile depth.

Inputs:

- student statements, documents, course lists, CV details, projects, or
  preferences
- optional evidence such as transcript, portfolio, module handbook excerpts, or
  thesis constraints

Outputs:

- thesis level and program, if known
- interests, courses, skills, methods, tools, experience, constraints, no-gos,
  research taste, confidence levels, and matching keywords
- missing information that would improve downstream recommendations

Guardrails:

- keep the profile in the active conversation only
- do not write private student data into shared files
- ask targeted follow-up questions when the profile is shallow
- summarize uncertainty instead of pretending the profile is complete

### `find-recent-papers`

Intent: find, rank, and summarize recent papers that can inform thesis
directions.

Use when a student or agent asks for publications, related work, research
directions, literature leads, or paper-based thesis ideas.

Inputs:

- a student profile, interests, courses, skills, chairs, researchers, or topics
- public publication sources or native web/search access when available

Outputs:

- a short ranked paper list with title, year or date, authors, venue or source,
  link or DOI, relevance rationale, and possible thesis angle

Guardrails:

- prefer recent, primary, traceable sources
- label preprints, surveys, workshops, and uncertain publication status
- do not invent citation counts, venues, affiliations, or acceptance status
- use absolute dates for "recent" results whenever possible

### `find-university-chairs`

Intent: identify relevant university chairs, labs, groups, and possible
supervisor candidates.

Use only after a sufficiently deep student profile exists, or when the user has
already provided enough profile context.

Inputs:

- deep student profile
- named chairs, professors, topics, or paper leads
- professor seed index and current public chair/lab sources

Outputs:

- recommended chairs or supervisors with research-fit rationale, evidence,
  conversation starters, prerequisites, preparation suggestions, and caveats

Guardrails:

- do not recommend chairs from a shallow profile
- distinguish research areas from confirmed thesis topics
- do not invent openings, capacity, team sizes, quotas, or willingness to
  supervise
- date public evidence when freshness matters

### `match-thesis-advisors`

Intent: rank possible advisors by combining the student's profile with paper and
chair evidence.

Use when asked to compare advisors, rank chairs, explain fit, or prepare an
evidence-based shortlist for proposal generation.

Inputs:

- deep student profile
- professor seed index
- evidence from `find-university-chairs` and `find-recent-papers`

Outputs:

- ranked shortlist with fit summary, evidence, matching research areas or
  papers, prerequisites, risks, caveats, proposal hooks, and next actions

Guardrails:

- treat matching as preparation for proposal discussions, not as confirmation
  of available thesis topics
- include backup directions when top matches are risky or uncertain
- do not invent supervision capacity, open topics, citations, or affiliation
  details

### `generate-thesis-directions`

Intent: turn profile, paper, and chair evidence into precise research-proposal
sketches.

Use when a student asks for thesis ideas, proposal directions, research
questions, topic hypotheses, or advisor-ready conversation starters.

Inputs:

- deep student profile
- chair or advisor matches
- recent paper and public source evidence

Outputs:

- 2-4 proposal sketches with working title, research question, motivation,
  methods/data/evaluation, advisor fit, prerequisites, feasibility risks, and a
  first meeting question
- a clear "AI-generated" label on the set of sketches

Guardrails:

- say "proposal sketch", "possible direction", or "conversation starter"
- do not present proposals as official open topics
- do not invent datasets, hardware access, supervision approval, or chair
  commitments
- prefer fewer, sharper proposals over many generic ideas

### `draft-thesis-contact`

Intent: draft concise, specific first-contact messages to potential thesis
advisors.

Use when a student asks for an email, message, outreach draft, or improvement of
an existing contact note to a professor, PhD student, postdoc, lab, chair, or
supervisor.

Inputs:

- student profile
- selected chair or person
- one concrete proposal sketch
- 1-2 evidence points from papers, chair pages, or public sources

Outputs:

- a clear "AI-generated draft" label on the output
- subject line
- email draft
- short rationale for why the email is specific
- optional checklist of facts the student should verify before sending

Guardrails:

- mention at most 1-2 papers or research areas unless asked for more
- do not overstate skills, grades, availability, or prior relationships
- do not invent openings, funding, capacity, or promises from the advisor

### `update-openalex-paper-index`

Intent: maintain optional Markdown paper data from OpenAlex for reviewed
researchers.

Use for scheduled or manual maintenance workflows, not for live student
advising.

Inputs:

- maintainer-reviewed researcher profiles and OpenAlex Author IDs
- OpenAlex works data or approved fixtures

Outputs:

- updated researcher profiles and paper indexes
- preserved source links, dates, DOI/OpenAlex IDs, and `last_updated`
- concise maintenance summary

Guardrails:

- maintenance-only; never use it as a shortcut around student-facing advising
- respect OpenAlex rate limits and polite-pool configuration
- do not overwrite maintainer-owned seed indexes unless the skill explicitly
  allows it
- run deterministic skill tests after generation

## Extending To A New Faculty

The durable product is a portable skill package, not a Tuebingen machine-learning
helper. To adapt it to another faculty, program, university, or discipline, reuse
the portable core workflow and replace only the faculty-specific public reference
data. Do not invent a new structure for each faculty.

### Start With The Meta-Skill

Every new faculty package, like every substantial skill redesign, begins with
`skills/design-agent-skill` (see `## Core Rule: Use The Meta-Skill First`). Read
`skills/design-agent-skill/SKILL.md`, then validate the result against
`skills/design-agent-skill/references/skill-authoring-rules.md`.

### Minimum Inputs For A New Faculty Package

Gather these before writing or adapting any files:

- target faculty or program
- student-workflow differences (e.g. thesis levels, scope, program rules)
- seed chair/professor source (where the new seed list comes from)
- public data sources (official faculty/lab pages, OpenAlex, DBLP, publisher
  pages)
- which skills need changes vs. which core skills are reused unchanged
- privacy and evidence constraints for that faculty's data

### Reusable Core vs. Faculty-Specific Data

The student-facing core skills are faculty-agnostic and are reused as-is:
`build-student-profile`, `find-recent-papers`, `find-university-chairs`,
`match-thesis-advisors`, `generate-thesis-directions`, and
`draft-thesis-contact`, plus the maintenance skill `update-openalex-paper-index`.
What changes per faculty is the **public reference data** they read, not the
workflow. Touch a `SKILL.md` only when a faculty's workflow genuinely differs,
and keep that change as narrow as possible.

### Expected Markdown Structure For Faculty References

Mirror the existing schemas; do not reinvent them:

- professor seed index — `references/professors/INDEX.md` with `name | uri`
  columns only (no emails or extra metadata)
- chairs and labs — `references/chairs/INDEX.md` plus per-chair files following
  `skills/find-university-chairs/references/chair-profile-schema.md`
- researchers — `references/researchers/INDEX.md` plus per-person files following
  `skills/update-openalex-paper-index/references/openalex-index-schema.md`
- program or degree reference, when the faculty needs one — model it on
  `skills/build-student-profile/references/tuebingen-degree-programs.md`

### Source Of Truth And Guardrails

The durable, reviewable source-of-truth files are `skills/*/SKILL.md`, the
`references/` data, `MASTERPLAN.md`, `STATUS.md`, and `AGENTS.md`.

Keep the guidance portable: do not add client-specific instructions unless there
is a portable fallback. All faculty reference data must be public, reviewable,
and dated, with uncertainty labelled. Never request or store private student
data in shared files (see `## Evidence, Privacy, And Data Rules`).

## Evidence, Privacy, And Data Rules

- Keep student-private data in the active session only.
- Do not commit transcripts, CVs, grades, personal constraints, contact drafts,
  or private advising notes into shared resources.
- Shared `references/` should contain public, maintainable, and reviewable
  information only.
- For facts that can become stale, cite source names and absolute dates.
- Clearly label uncertainty, inference, missing data, and source disagreement.
- Do not fabricate citations, venues, affiliations, advisor availability,
  supervision capacity, or official thesis openings.
- Prefer official university pages, lab pages, publication pages, DOI records,
  OpenAlex, DBLP, Google Scholar profiles, and publisher pages when available.

## Maintainer Guidelines

- Keep each skill focused on one repeatable task.
- Keep `SKILL.md` short enough for an agent to load and follow quickly.
- Put detailed rubrics, schemas, examples, and generated indexes in
  `references/`.
- Add scripts only for deterministic maintenance tasks that would otherwise be
  fragile or repetitive.
- Prefer portable Markdown and standard files over client-specific features.
- If a client-specific instruction is unavoidable, document it explicitly and
  keep the portable path usable.
- Make every change traceable to a student workflow, maintainer workflow, or
  evidence-quality improvement.
- Do not add speculative configurability or broad abstractions before there is a
  repeated need.

## Contribution And PR Guidance

Keep changes focused and reviewable:

- one issue or PR should cover one coherent skill or maintenance change
- explain what changed and why
- mention affected skills and references
- include known gaps honestly when a change is partial
- keep public data updates separate from unrelated instruction changes when
  practical

Use clear commit subjects such as:

- `docs: clarify thesis skill workflow`
- `feat: add advisor matching rubric`
- `chore: refresh openalex paper index`
- `test: validate skill references`

Before requesting review, run the DB-free checks from the repository root:

```bash
python -m pytest
```

If CI is available for the public repository, verify that it is green before
requesting review. If `gh` is available, use it to inspect PR checks.

## Success Criteria

These instructions are working when:

- agents use `design-agent-skill` before creating or redesigning skills
- students receive profile-grounded, evidence-based thesis guidance
- shallow inputs trigger better questions instead of premature recommendations
- shared resources contain public data only
- future maintainers can extend the skill package without knowing the original
  project history
