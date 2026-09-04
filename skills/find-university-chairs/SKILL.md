---
name: find-university-chairs
description: Discover thesis options across University of Tübingen chairs, institutes, clinics, centers, and research groups from a complete student profile by delegating live candidate discovery to discover-university-candidates. Use when a student asks which chair, lab, professor, research group, or supervisor fits their interests, methods, domain, thesis style, or constraints.
---

# Discover University Thesis Options

Map a student's research interests to thesis opportunities across the University
of Tübingen and Tübingen-associated research structures. This skill does not
carry a static faculty or URI backbone. It first obtains a temporary,
profile-specific candidate table from `discover-university-candidates`, then
enriches and ranks those candidates with live evidence.

## Prerequisites

Require a deep student profile covering all six dimensions:

1. Interests
2. Methods
3. Domain
4. Thesis style
5. Skills
6. No-gos

If any dimension is missing or shallow, stop here. Invoke `build-student-profile`
before producing a shortlist.
Do not produce a chair shortlist on a partial profile.

This skill requires live web/search access. If browsing or search is unavailable,
say so and do not guess from model memory.

## Workflow

1. Verify the six-dimension profile.
2. Extract German and English query terms using `references/search-strategy.md`.
3. Invoke `discover-university-candidates` with the full profile and any explicit
   exclusions the student provided in the current conversation.
4. Require the exact temporary candidate table schema from
   `discover-university-candidates`: `entity_type`, `name`, `institution`,
   `affiliation_status`, `official_domain`, `relevant_uri`, `unit_type`,
   `relevant_person`, `topic_tags`, `source_axis`, `evidence_summary`,
   `verified_at`, `confidence`, and `no_go_flags`.
5. Exclude `affiliation_status: uncertain` and `affiliation_status: rejected`
   from the final Tübingen option map unless they appear only in a separate
   caveat or no-fit note. Do not enrich uncertain-affiliation entries as normal
   thesis options.
6. If fewer than five confirmed-affiliation candidates return, broaden once
   through the candidate skill. If the field remains thin, continue with an
   honest short map or no-fit explanation.
7. Enrich each confirmed-affiliation candidate using the query skeletons and filters in
   `references/search-strategy.md`.
8. Confirm current affiliation before naming any person as a chair-holder,
   supervisor, or lab head. If current affiliation is not confirmable, set the
   person to `unknown` or flag the entry.
9. Verify every URL immediately before final output.
10. Apply final no-go filtering. Do not silently drop borderline entries; keep
   them with a clear warning unless a no-go is confirmed.
11. Produce the option map grouped by the student's interest dimension.

## Output

Produce a map of options grouped by interest dimension, not by faculty.

If no candidate survives discovery and enrichment, say so plainly. Name adjacent
routes only when they were verified during the run.

For each option include:

- **Chair / group / institute name** and verified official URL
- **Relevant person** - professor, PI, group lead, or `unknown`
- **Unit type** - chair, institute, clinic, lab, center, or research group
- **Relevance rationale** - tied to interests, methods, domain, and thesis style
- **Possible thesis angles** - 2-4 tentative topic directions or conversation starters for strong options, each grounded in the option's verified evidence and clearly labeled as not an official opening
- **Pros & likely difficulties** - supervision uncertainty, language, workload,
  access constraints, competitive groups, or weak thesis-signal visibility
- **Dated evidence** - source URL and date
- **Conversation starter** - one concrete first-contact angle
- **No-go flags** - none, possible conflict, or confirmed exclusion rationale

End with this caveat:

> This map covers publicly visible Tübingen options found through live discovery
> across multiple source axes as of today's date. Groups with weak web presence,
> non-indexed pages, or informal supervision paths may be missing. Before
> outreach, verify the official page, current affiliation, and whether the group
> is accepting thesis students.

## Evidence Rules

- Prefer `uni-tuebingen.de` and `medizin.uni-tuebingen.de`. Accept associated
  institutes such as MPI-IS when current Tübingen affiliation is public.
- Do not invent thesis openings, team sizes, citation counts, or willingness to supervise.
- Do not invent people, capacity, or URLs.
- Every URL in the output must have been opened or verified during this run.
- Mark evidence older than three years as stale.
- Distinguish active research areas from advertised thesis openings.
- Do not collapse a strong match to a single thesis topic. Offer multiple evidence-grounded angles so the student can choose which direction to drill into.
- Keep student-private data in the active session only.

## Self-Check

Before delivering the map, confirm:

- all six profile dimensions were present
- `discover-university-candidates` returned a live-verified candidate table
- at least four source axes were attempted, unless unavailable and documented
- every named person in an included option has current affiliation evidence
- every included option has `affiliation_status: confirmed`
- every included URL was verified during this run
- no-go conflicts were handled explicitly
- output is grouped by student interest, not by source axis or faculty
