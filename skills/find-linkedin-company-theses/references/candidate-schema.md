# External Company Thesis Candidate Schema

Normalize every possible external thesis result into this schema before ranking
or excluding it. Keep unknown fields explicit instead of guessing.

| Field | Meaning |
|---|---|
| `provider` | Discovery provider, such as `linkedin_public`, `stepstone`, or `company_careers`. |
| `source_url` | Public URL or search-result URL where the candidate was found. |
| `title` | Visible posting title or concise topic. |
| `company` | Visible company or institute name. |
| `location` | Visible city, region, country, or `unclear`. |
| `thesis_level` | `Bachelorarbeit`, `Masterarbeit`, `Abschlussarbeit`, `thesis`, or `unclear`. |
| `job_type` | Visible role type, such as thesis, internship, Werkstudent, working student, job, or unclear. |
| `visible_date` | Visible posting date, deadline, or `date unclear`. |
| `evidence_text` | Short paraphrase of the visible text that proves or weakens eligibility. |
| `evidence_tier` | Tier from `references/ranking-rubric.md`. |
| `matched_keywords` | Profile-relevant terms found in the visible evidence. |
| `exclusion_reason` | Empty for eligible candidates; otherwise one exact reason from the hard exclusions. |
| `mirror_url` | Public company-career mirror URL when found, otherwise `none found`. |
| `access_date` | Absolute date when the source was checked. |

## Normalization Rules

- Keep the original `provider` even when a company-career mirror confirms the
  posting. Use `mirror_url` for the confirming page.
- Use `company_careers` as the provider only when the company career page was
  the first source that surfaced the candidate.
- Do not infer a thesis level from a strong topic match. `Abschlussarbeit` is
  compatible only when visible evidence maps it to the student's confirmed
  level or explicitly includes that level.
- Do not infer live availability from stale snippets, result counts, or old
  cached search results.
- Use one exact `exclusion_reason` whenever a candidate fails a hard exclusion:
  `not a thesis`, `wrong thesis level`, `generic job/internship`,
  `Werkstudent/working-student role`, `topic mismatch`,
  `location/work-mode mismatch`, `excluded sector`, `must-avoid technology`,
  `weak profile match`, or `insufficient evidence`.
