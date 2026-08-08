# University Candidate Discovery Rules

## Source Axes

Use multiple axes so discovery is not limited to one faculty page structure or
one search ranking.

| Axis | Purpose | Example query shape |
|---|---|---|
| Faculty search | Find official Tübingen faculty, department, and chair pages | `site:uni-tuebingen.de {topic_de} Lehrstuhl Tübingen` |
| Institute search | Find departments, institutes, seminars, clinics, and research groups | `site:uni-tuebingen.de {domain_de} Institut Forschung Tübingen` |
| Center search | Catch cross-faculty centers and special structures | `site:uni-tuebingen.de {topic_de} Zentrum Forschung Tübingen` |
| Associated institutes | Catch Tübingen research groups outside faculty listing pages | `{topic_en} Tübingen research group MPI-IS Cyber Valley ELLIS` |
| Publication search | Confirm current research areas and people | `{person_or_group} {topic_en} {THIS_YEAR} {THIS_YEAR-1} {THIS_YEAR-2}` |
| Course catalog | Support teaching/supervision fit when research pages are thin | `{topic_de} Tübingen Vorlesungsverzeichnis Seminar` |

For AI/ML/neuroscience profiles, associated institutes and centers are
first-class axes, not optional enrichment.

Resolve `{THIS_YEAR}` to the current calendar year at run time. Never paste a
fixed set of years into a query — a hardcoded window silently stops finding new
work the year after it is written.

## Verification

A candidate can be returned only if the run verifies:

- official or authoritative page is reachable
- Tübingen affiliation is confirmed from an official or authoritative current
  public source
- topic fit is supported by page text, recent publications, projects, teaching,
  or center descriptions
- relevant person is confirmed on an official/current page or set to `unknown`
- no-go conflicts are absent or explicitly flagged
- evidence has a source URL and access date

Do not include `affiliation_status: uncertain` entries in the final candidate
table for Tübingen thesis options. Keep them in scratch notes or a separate
"uncertain / excluded" note only when they explain a no-fit or thin-field
result. Use `affiliation_status: rejected` only in scratch notes, not in the
final candidate table, unless the result is needed to explain why a plausible
source-axis hit was not a Tübingen option.

## Ranking

Rank by profile fit first, then supervision/topic plausibility, then evidence
freshness and contactability. Do not rank by faculty prestige or search position.

Prefer:

- specific method/domain evidence over broad discipline labels
- current official pages over old PDFs or stale personal pages
- candidates that match both interest and thesis style
- direct Tübingen affiliation over ambiguous association
- honest no-fit outcomes over padded weak matches

## Failure Modes

- If fewer than five verified candidates remain, broaden by adjacent departments
  or centers and explain the thin field.
- If a topic does not fit University of Tübingen structures, say so plainly and
  name adjacent routes only when verified.
- If search tools are unavailable, stop rather than relying on stale model
  memory.
