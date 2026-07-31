# Company Candidate Discovery Rules

## Source Axes

Use multiple axes so the candidate pool is not just a search-ranking or
brand-size list.

| Axis | Purpose | Example query shape |
|---|---|---|
| Official site | Confirm real company/domain and careers or research pages | `{topic} {domain} Baden-Württemberg Unternehmen Forschung` |
| Careers/thesis pages | Find student/thesis signals without trusting aggregators | `{topic} Masterarbeit Abschlussarbeit Baden-Württemberg Firma` |
| Research clusters | Catch startups and R&D-heavy teams | `{topic} Cyber Valley startup Baden-Württemberg` |
| University partners | Catch companies that collaborate with universities | `{topic} Hochschule Universität Tübingen Industriepartner` |
| Industry networks | Catch sector-specific SMEs | `{domain} Verband Baden-Württemberg Forschung Unternehmen` |
| Regional search | Catch local candidates outside famous lists | `{topic} {city_or_region} Entwicklung Forschung Unternehmen` |
| Company rankings | Add prominent employers, but only as one minority axis | `größte Unternehmen Baden-Württemberg {domain}` |

Company-ranking sources must not dominate. If a raw pool has 30 candidates, at
most 10 may come only from ranking/top-company lists.

## Verification

A candidate can be returned only if the run verifies:

- official domain or official careers/research page is reachable
- Baden-Württemberg presence is confirmed from an official or authoritative
  public source
- R&D, product development, research collaboration, or student work is plausibly
  relevant to the profile
- no-go conflicts are absent or explicitly flagged
- evidence has a source URL and access date

Do not include `bw_scope: uncertain` companies in the final candidate table for
Baden-Württemberg thesis options. Keep them in scratch notes or a separate
"uncertain / excluded" note only when they explain a no-fit or thin-field result.
Use `bw_scope: rejected` only in scratch notes, not in the final candidate table,
unless the result is needed to explain why a plausible source-axis hit was not a
BW option.

## Ranking

Rank by profile fit first, then thesis likelihood, then practical contact path.
Do not rank by company size alone.

Prefer:

- specific topic evidence over broad "innovation" language
- official pages over snippets or reposted job ads
- candidates that match both interest and domain
- candidates with a plausible thesis/student route
- diversity across company size and source axis when fit is otherwise similar

## Failure Modes

- If fewer than five verified candidates remain, broaden by one secondary domain
  or source axis and explain the thin field.
- If the profile structurally does not fit company theses, return a no-fit note
  and recommend `find-university-chairs`.
- If search tools are unavailable, stop rather than relying on stale model
  memory.
