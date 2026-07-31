# University Thesis Enrichment Strategy

Use this reference after `discover-university-candidates` has returned a
temporary candidate table. Do not store or maintain faculty URL lists here.

## Profile Variables

Extract:

- `{TOPIC_DE}`, `{TOPIC_EN}` from interests
- `{METHOD_DE}`, `{METHOD_EN}` from methods
- `{DOMAIN_DE}`, `{DOMAIN_EN}` from domain

Use thesis style, skills, and no-gos for local fit assessment and first-contact
framing. Do not send sensitive or personal no-go wording to search providers;
if a no-go must shape discovery, convert it to a coarse, non-identifying
category such as `non-clinical`, `software role`, or `no animal experiments`.

## Enrichment Queries

Run only against verified candidates.

### Topic And Method Fit

```text
site:{OFFICIAL_DOMAIN} "{TOPIC_DE}" OR "{TOPIC_EN}" Forschung OR research
site:{OFFICIAL_DOMAIN} "{METHOD_DE}" OR "{METHOD_EN}" "{DOMAIN_DE}" OR "{DOMAIN_EN}"
```

Prefer specific projects, publications, teaching, or group descriptions over
broad department labels.

### Current Activity

```text
"{GROUP_OR_PERSON}" "{TOPIC_EN}" 2024 OR 2025 OR 2026
site:{OFFICIAL_DOMAIN} "{GROUP_OR_PERSON}" 2024 OR 2025 OR 2026
```

Evidence from 2022 or later can count as recent. Older evidence must be marked
stale.

### Thesis Signal

```text
site:{OFFICIAL_DOMAIN} Masterarbeit OR Abschlussarbeit OR thesis "{TOPIC_DE}" OR "{TOPIC_EN}"
site:{OFFICIAL_DOMAIN} Lehre OR teaching OR Abschlussarbeiten OR Betreuung
```

Absence of a public thesis page is normal. Do not infer supervision capacity.

### Person And Affiliation Verification

```text
site:{OFFICIAL_DOMAIN} "{PERSON_NAME}" Tübingen
"{PERSON_NAME}" Universität Tübingen OR University of Tübingen 2024 OR 2025 OR 2026
```

Name a person only when current affiliation is confirmed on an official/current
page. If a personal page or publication result conflicts with the unit page,
flag the entry and rank it lower.

## Quality Filters

- Official/current university or clinic pages outrank stale PDFs and snippets.
- Associated institutes can be first-class when the Tübingen relation is public.
- Specific method/domain evidence outranks title-only matches.
- Enrich before excluding when a title mixes compatible and incompatible areas.
- Prefer honest no-fit outcomes over padded weak matches.

## No-Go Handling

Discard confirmed conflicts. Keep ambiguous conflicts only with an explicit flag,
for example `possible no-go conflict: clinical access may be required`.

Never convert a student's humanities, social-science, theory, or biology profile
into a CS/ML recommendation unless the profile itself supports that direction.
