# Chair And Researcher Profile Schema

Use this structure for bundled chair, lab, professor, PhD, or postdoc profiles.

## File Naming

Use stable, lowercase, hyphenated names:

```text
references/chairs/<chair-or-lab-slug>.md
references/researchers/<person-slug>.md
```

Create an `INDEX.md` with keywords, people, and links to profile files.

## Chair Profile

```markdown
# Chair or Lab Name

## Metadata
- University:
- Department:
- Website:
- Last updated:

## People
- Name, role, profile file or URL

## Research Areas
- Area:
- Keywords:
- Evidence:

## Recent Papers
- Title, year, authors, source/link:

## Thesis Fit Notes
- Good fit for:
- Likely prerequisites:
- Conversation starters:

## Caveats
- Stale or missing information:
```

## Researcher Profile

```markdown
# Person Name

## Metadata
- Role:
- Chair/lab:
- Website:
- Last updated:

## Research Focus
- Topics:
- Methods:
- Application areas:

## Selected Recent Papers
- Title, year, source/link:

## Thesis-Relevant Signals
- Possible directions:
- Prerequisites:
- Contact notes:

## Caveats
- Unverified or stale information:
```

## Index Entry

Each index entry should include:

- Name
- Role or chair
- Keywords
- File path
- Last updated
