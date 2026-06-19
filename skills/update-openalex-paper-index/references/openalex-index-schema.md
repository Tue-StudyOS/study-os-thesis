# OpenAlex Index Schema

## Researcher Index

`find-university-chairs/references/researchers/INDEX.md` should contain a Markdown table:

```markdown
| slug | name | role | chair_slug | openalex_author_id | keywords | last_updated |
|---|---|---|---|---|---|---|
| example-person | Example Person | professor | example-chair | A1234567890 | robotics; reinforcement learning | 2026-06-13 |
```

## Researcher Profile

```markdown
# Person Name

## Metadata
- Role:
- Chair:
- Website:
- OpenAlex author id:
- Last updated:

## Research Areas
- Keywords:

## Selected Recent Papers
### Paper Title
- Year:
- Authors:
- Source:
- DOI:
- OpenAlex:
- URL:
- Abstract:
- Thesis angles:

## Caveats
- Affiliation uncertainty:
- Missing data:
```

## Paper Index Entry

Use compact entries in topic and year indexes:

```markdown
## Paper Title
- Year:
- Authors:
- Researcher:
- Chair:
- DOI:
- OpenAlex:
- URL:
- Keywords:
- Thesis angle:
```
