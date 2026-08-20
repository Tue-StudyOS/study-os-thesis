# Student Profile Schema

Use this schema for in-session matching only. Do not write filled profiles into shared skill resources.

## Canonical Six Dimensions

`thesis-finder`, `find-university-chairs`, and `find-company-thesis-options` all gate on
these six dimensions being present before they will search. Use identical names everywhere:

1. **Interests** — core research areas / topics
2. **Methods** — how the student wants to work (empirical, qualitative, computational, …)
3. **Domain** — application field (healthcare, education, finance, automotive, …)
4. **Thesis style** — preferred output type (experimental, theoretical, systems, analysis, survey, mixed)
5. **Skills** — concrete tools / competencies (Python, fMRI, R, ML frameworks, lab methods, …)
6. **No-gos** — hard exclusions (hardware setup, clinical rotations, pure proofs, large-scale SE, …)

Courses, projects, and professional experience are not separate dimensions — they are the
evidence the interview uses to fill Methods, Domain, and Skills (see
`build-student-profile/SKILL.md`).

`Thesis duration` is the formal Bearbeitungszeit from the student's exam regulations; it is
set per faculty and per Fassung, so it is recorded with where it came from and left blank
rather than guessed (see `degree-program-rules.md`). `Time constraints` is separate — it is
the student's own situation (a job, a move, a fixed submission target), not a regulation.

```markdown
# Student Thesis Profile

## Context
- Thesis level:
- Degree program:
- Thesis duration (Bearbeitungszeit, with source: student / verified page / unresolved):
- Preferred language:
- Time constraints:
- Optional evidence sources used:

## Interests
- Research areas:
- Application domains:
- Questions the student is curious about:
- Problems the student would enjoy thinking about for weeks:
- Topics the student does not want:

## Coursework And Skills
- Relevant courses:
- Lectures/seminars/labs the student liked:
- Lectures/seminars/labs the student disliked:
- Memorable topics or assignments:
- Programming/tools:
- Frameworks/libraries:
- Robotics/simulation/hardware tools:
- Math/statistics/ML methods:
- Domain knowledge:
- Past projects or practical evidence:
- Professional or research experience:
- Development workflow:

## Research Skills
- Literature reading and paper synthesis:
- Experimental design:
- Implementation and debugging:
- Data handling and evaluation:
- Mathematical/theoretical reasoning:
- Scientific writing and communication:
- Engineering maturity:
- Evidence for each skill:

## Research Taste
- Preferred kind of contribution:
- Preferred evidence style:
- Tolerance for ambiguity:
- Methods the student wants to learn:
- Methods the student wants to avoid:
- Topics, tools, or work styles the student dislikes:

## Preferences And Constraints
- Preferred supervision style:
- Preferred chairs or excluded areas:
- Hardware/data/access constraints:
- Time budget and risk tolerance:

## Proposal Ingredients
- Promising problem shapes:
- Possible datasets or evidence sources:
- Evaluation style:
- Feasibility risks:

## Matching Keywords
- Keywords:
- Synonyms:
- Methods:

## Confidence And Missing Information
- High-confidence facts:
- Inferred facts:
- Missing information:
- Useful optional sources still missing:
```
