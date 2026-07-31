---
name: find-company-thesis-options
description: Discover Masterarbeit options at Baden-Württemberg companies from a complete student profile by delegating live candidate discovery to discover-company-candidates, then enriching and ranking verified companies. Use when a student asks which BW company, R&D lab, or industry team fits their interests, methods, domain, or thesis style for a company-supervised thesis.
---

# Discover Company Thesis Options

Map a student's research interests to Master's thesis opportunities at
Baden-Württemberg companies. This skill does not carry a static company or URI backbone.
It first obtains a temporary, profile-specific candidate table from
`discover-company-candidates`, then enriches those candidates with live evidence.

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

This skill requires live web/search access. If browsing or search is unavailable,
say so and do not guess from model memory.

## Workflow

1. Verify the six-dimension profile.
2. Extract German and English query terms using
   `references/company-search-strategy.md`.
3. Invoke `discover-company-candidates` with the full profile and any explicit
   dead-end exclusions from the session.
4. Require the exact temporary candidate table schema from
   `discover-company-candidates`: `entity_type`, `name`, `official_domain`,
   `relevant_uri`, `location`, `bw_scope`, `sector_tags`, `size`,
   `source_axis`, `evidence_summary`, `verified_at`, `confidence`, and
   `no_go_flags`.
5. Exclude `bw_scope: uncertain` and `bw_scope: rejected` from the final BW
   option map. Keep them only in a separate caveat or no-fit note when they
   explain a thin field.
6. If fewer than five confirmed-BW candidates return, broaden once through the candidate
   skill. If the field remains thin, continue with an honest short map or
   recommend the university track.
7. Enrich each confirmed-BW candidate using the query skeletons and filters in
   `references/company-search-strategy.md`.
8. Classify thesis signal as `explicit opening`, `active program`, or `unclear`.
9. Verify every contact/careers/R&D URL immediately before final output.
10. Apply final no-go filtering. Do not silently drop borderline entries; keep
   them with a clear warning unless a no-go is confirmed.
11. Produce the option map grouped by the student's interest dimension.

## Output

Append this map-level caveat once at the top:

> This map covers BW companies surfaced through live discovery across multiple
> public source axes and verified during this run. Most companies do not
> publicize open Masterarbeit positions, so `thesis signal: unclear` does not
> mean there is no opening. For unclear entries: use the careers portal for
> large companies and follow up, or contact the R&D/product team directly at
> startups and SMEs. Live discovery is not exhaustive; companies with weak web
> presence or non-public university contacts may be missing.

For each entry include:

- **Company** - full company name
- **Division / team** - relevant business unit or R&D lab; `unknown` if not
  determinable
- **Sector tags** - from the candidate table or live verification
- **Size** - `startup`, `SME`, `corporate`, or `unknown`
- **Location** - city/region with confirmed BW-scope evidence
- **Relevance rationale** - tied to interests, domain, methods, and thesis style
- **Pros & likely difficulties** - structure, supervision uncertainty,
  confidentiality/IP, language, or application lead time
- **Contact path** - verified URL or "direct R&D team inquiry - no portal found"
- **Research focus (live)** - source URL and content date, or `not found`
- **Thesis signal** - `explicit opening`, `active program`, or `unclear`
- **Thesis coordinator / contact** - only when confirmed on a company-owned page
- **No-go flags** - none, possible conflict, or confirmed exclusion rationale

## Evidence Rules

- Prefer company-owned pages. Accept research clusters and university partner
  pages as secondary evidence. Use job boards only as hints that must be traced
  back to official sources.
- Never invent thesis openings, contact names, team sizes, R&D topics, company
  locations, or URLs.
- Every URL in the output must have been opened or verified during this run.
- Mark evidence older than three years as stale.
- `thesis signal: unclear` is valid output, not a skill failure.
- Do not submit applications, register accounts, or post to external services.
- Keep student-private data in the active session only.

## Self-Check

Before delivering the map, confirm:

- all six profile dimensions were present
- `discover-company-candidates` returned a live-verified candidate table
- company ranking/top-company sources did not dominate the candidate pool
- every included URL was verified during this run
- every thesis signal uses one of the three allowed labels
- no-go conflicts were handled explicitly
- output is grouped by student interest, not by source axis or company size
