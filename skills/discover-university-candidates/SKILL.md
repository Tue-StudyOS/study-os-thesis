---
name: discover-university-candidates
description: Build a temporary, profile-specific candidate set of University of Tübingen chairs, institutes, clinics, centers, and research groups from live web discovery. Use when a thesis-discovery skill needs university candidates without relying on a static faculty or URI backbone.
---

# Discover University Candidates

Find 8-12 verified University of Tübingen or Tübingen-associated research
candidates for a complete student thesis profile. This skill produces a
temporary candidate table only; `find-university-chairs` does the final
PI/affiliation checks, ranking, and student-facing option map.

## Prerequisites

Require a complete six-dimension profile: interests, methods, domain, thesis
style, skills, and no-gos. If any dimension is missing or shallow, return to
`build-student-profile` before searching.

This skill requires live web/search access. If browsing or search is unavailable,
stop and say that university candidate discovery cannot be run without live
sources. Do not guess candidates from model memory.

## Workflow

1. Extract German and English terms for interests, methods, and domain. Treat
   no-gos as local filters; only convert them into broad, non-identifying query
   categories when needed to avoid an obvious mismatch.
2. Read `references/university-discovery-rules.md`.
3. Run at least four independent source axes before ranking candidates.
4. Build a raw pool of 15-30 chairs, labs, institutes, clinics, centers, or
   research groups.
5. Deduplicate faculty pages, institute pages, personal pages, center pages, and
   associated-institute pages that describe the same group.
6. Verify each surviving candidate from official or authoritative public pages:
   Tübingen affiliation, current activity, topic fit, and reachable relevant URI.
7. Apply no-gos before returning candidates. Keep sensitive or personal no-go
   wording out of web queries. Keep ambiguous conflicts only with a clear no-go
   flag.
8. Return 8-12 candidates where possible, never more than 20.

## Output

Return a Markdown table with these fields:

```yaml
entity_type: university_group
name: string
institution: University of Tübingen | associated_institute
official_domain: string
relevant_uri: string
unit_type: chair | institute | clinic | lab | center | research_group
relevant_person: string | unknown
topic_tags: [string]
source_axis: faculty_search | institute_search | center_search | associated_institutes | publication_search | course_catalog | internal_site_search
evidence_summary: string
verified_at: YYYY-MM-DD
confidence: high | medium | low
no_go_flags: string
```

Include a short "Search coverage" note naming which source axes were used and
which axes were thin or unavailable.

## Evidence Rules

- Prefer `uni-tuebingen.de` and `medizin.uni-tuebingen.de` pages. Accept
  associated institutes such as MPI-IS only when the Tübingen connection is
  current and public.
- Do not invent chairs, people, thesis openings, team sizes, capacity, or URLs.
- Every included URI must be opened or verified during this run.
- Mark evidence older than three years as stale.
- Keep student-private data in the active session only; do not write profile
  details to shared resources.
