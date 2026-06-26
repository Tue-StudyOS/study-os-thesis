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

## Referential Integrity

The tree is a graph of slugs: chair -> researcher -> paper. Run the builder's
check to confirm every cross-reference resolves and to fail on any orphan:

```bash
python scripts/update_openalex_index.py --validate-only
```

It verifies that:

- every researcher `chair_slug` resolves to a chair in the chair index
- every chair `researchers` slug resolves to a researcher
- every paper `researchers` and `chairs` slug resolves to an existing node

Tables are parsed by **column name**, not position, so a faculty may add or
reorder descriptive columns without breaking the readers or this check. Only the
slug/link columns above are load-bearing.

## Reusing The Builder For Another Faculty

The same script builds or validates any faculty's tree. Point it at that
faculty's files instead of the bundled Tuebingen defaults:

```bash
python scripts/update_openalex_index.py \
  --researchers-index <faculty>/researchers/INDEX.md \
  --chairs-index <faculty>/chairs/INDEX.md \
  --papers-dir <faculty>/papers
```
