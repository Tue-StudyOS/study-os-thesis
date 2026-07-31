---
name: discover-company-candidates
description: Build a temporary, profile-specific candidate set of Baden-Württemberg company thesis options from live web discovery. Use when a thesis-discovery skill needs company candidates without relying on a static company or URI backbone.
---

# Discover Company Candidates

Find 8-12 verified company candidates for a complete student thesis profile. This
skill produces a temporary candidate table only; `find-company-thesis-options`
does the final thesis-signal enrichment, ranking, and student-facing option map.

## Prerequisites

Require a complete six-dimension profile: interests, methods, domain, thesis
style, skills, and no-gos. If any dimension is missing or shallow, return to
`build-student-profile` before searching.

This skill requires live web/search access. If browsing or search is unavailable,
stop and say that company candidate discovery cannot be run without live sources.
Do not guess candidates from model memory.

## Workflow

1. Extract German and English search terms for the student's interests, methods,
   domain, and no-gos.
2. Read `references/company-discovery-rules.md`.
3. Run at least four independent source axes before ranking candidates. Company
   ranking lists are allowed as one axis only; they must not contribute more than
   one third of the raw candidates.
4. Build a raw pool of 20-40 names. Deduplicate subsidiaries, renamed companies,
   and careers-platform duplicates.
5. Verify each surviving candidate from official or authoritative public pages:
   Baden-Württemberg presence, R&D or product-development relevance, profile
   fit, and a reachable official domain or relevant page.
6. Apply no-gos before returning candidates. Keep ambiguous conflicts only with a
   clear no-go flag.
7. Return 8-12 candidates where possible, never more than 20.

## Output

Return a Markdown table with these fields:

```yaml
entity_type: company
name: string
official_domain: string
relevant_uri: string
location: string
bw_scope: confirmed | uncertain | rejected
sector_tags: [string]
size: startup | SME | corporate | unknown
source_axis: official_site | careers_thesis | research_cluster | university_partner | industry_network | regional_search | company_ranking
evidence_summary: string
verified_at: YYYY-MM-DD
confidence: high | medium | low
no_go_flags: string
```

Do not include rejected candidates in the final table unless they explain a
no-fit result. Include a short "Search coverage" note naming which source axes
were used and which axes were thin or unavailable.

## Evidence Rules

- Prefer company-owned pages for final evidence. Use job boards only as a hint
  that must be traced back to an official source.
- Do not invent companies, URLs, thesis openings, contact names, R&D topics, or
  BW locations.
- Every included URI must be opened or verified during this run.
- Mark evidence older than three years as stale.
- Keep student-private data in the active session only; do not write profile
  details to shared resources.
