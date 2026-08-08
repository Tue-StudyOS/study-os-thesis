# Company Thesis Enrichment Strategy

Use this reference after `discover-company-candidates` has returned a temporary
candidate table. Do not build a static company list here.

## Profile Variables

Extract:

- `{TOPIC_DE}`, `{TOPIC_EN}` from interests
- `{METHOD_DE}`, `{METHOD_EN}` from methods
- `{DOMAIN_DE}`, `{DOMAIN_EN}` from domain

Use thesis style, skills, and no-gos for local fit assessment, not as standalone
search axes. Do not send sensitive or personal no-go wording to search
providers; if a no-go must shape discovery, convert it to a coarse,
non-identifying category such as `software role` or `non-clinical`.

## Enrichment Queries

Run only against verified candidates.

### R&D Focus

```text
site:{COMPANY_DOMAIN} "{TOPIC_EN}" OR "{TOPIC_DE}" research OR Forschung OR innovation
site:{COMPANY_DOMAIN} "{METHOD_EN}" OR "{METHOD_DE}" "{DOMAIN_EN}" OR "{DOMAIN_DE}"
```

For large companies with named labs or divisions, prefer the lab or division
domain/page over generic marketing pages.

### Thesis Signal

```text
site:{COMPANY_DOMAIN} Masterarbeit OR Abschlussarbeit OR "master thesis" OR "student thesis" "{TOPIC_EN}" OR "{TOPIC_DE}"
site:{COMPANY_DOMAIN} Abschlussarbeiten OR Studienarbeit students OR Studenten
```

If this returns no official page, classify as `unclear`; do not promote a
job-board repost to an official opening.

### Contact Path

```text
site:{COMPANY_DOMAIN} Karriere OR career OR Kontakt OR contact OR students OR Studenten
site:{COMPANY_DOMAIN} Hochschulkontakt OR "university relations" OR Ansprechpartner Abschlussarbeit OR thesis
```

Name a coordinator only if the person appears on the company's own public page.

### Recency

Resolve `{THIS_YEAR}` to the current calendar year at run time and derive the
window from it. Never paste a fixed set of years into a query — a hardcoded
window silently stops finding new work the year after it is written.

```text
site:{COMPANY_DOMAIN} "{TOPIC_EN}" {THIS_YEAR} OR {THIS_YEAR-1} OR {THIS_YEAR-2}
"{COMPANY_NAME}" "{TOPIC_EN}" Forschung OR research press OR news {THIS_YEAR} OR {THIS_YEAR-1}
```

Evidence from the last four years counts as recent. Older evidence must be
marked stale, with its actual date shown.

## Quality Filters

- Specific topic evidence outranks broad "we do AI/innovation" language.
- Official company pages outrank snippets, directories, or job boards.
- Research-cluster pages can support R&D relevance, but thesis signals must be
  traced to the company where possible.
- For startups and SMEs, no listed thesis opening is normal; recommend direct
  R&D/product-team outreach when fit is strong.
- For corporates, prefer verified student/careers portals and note slower
  application cycles.

## No-Go Handling

Discard confirmed conflicts. Keep ambiguous conflicts only with an explicit flag,
for example `possible no-go conflict: verify software vs. hardware role before
outreach`.

Do not discard a candidate from tags alone when live evidence might distinguish
between a compatible software/research role and an incompatible hardware,
clinical, sales, or consulting role.
