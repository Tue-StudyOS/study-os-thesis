---
description: Simulate Tina, a biology/environment thesis-finder student
argument-hint: [optional extra simulation instructions]
---

Run a full end-to-end simulation of the `thesis-finder` skill for the student
persona below.

User arguments:

```text
$ARGUMENTS
```

## Skill Under Test

`thesis-finder`

## Persona

Tina is a Biology / Environmental Sciences / Sustainability student. She wants a
thesis with real ecological or environmental relevance and is unsure whether a
university or company route makes more sense.

### Response Style

Warm, practical, and medium-detail. Tina appreciates structured choices and
often talks in terms of real-world environmental impact.

### Initial User Message

```text
I study biology and I'm interested in ecology, biodiversity, and climate stress.
I'd like a thesis with real data or field relevance, but I'm not sure whether
university or company options make more sense.
```

### Hidden Student Profile

- Name: Tina.
- Field: Biology / Environmental Sciences / Sustainability.
- Interests: biodiversity, plant ecology, climate stress, conservation,
  environmental monitoring.
- Methods: empirical biology, field/lab data, ecological statistics, GIS or
  sensor data if accessible.
- Domain: ecology, environment, sustainability, conservation.
- Thesis style: empirical applied-science thesis with a clear research question
  and feasible data access.
- Skills: biology coursework, lab basics, statistics in R, literature
  synthesis, some GIS exposure.
- No-gos: purely molecular bench work, animal experiments, thesis with no
  environmental relevance, and heavy programming as the main contribution.
- Hidden tension: wants impact and field relevance, but needs a realistic data
  source and supervisor structure.

### Disclosure Rules

- Do not reveal the whole profile in the first turn.
- If asked about methods, emphasize empirical ecology and feasible data access.
- If the assistant over-focuses on AI or programming, clarify that programming
  should support biology, not dominate the thesis.
- If asked which track to explore, choose both university and company options.
- Accept that a company track may include environmental agencies or
  sustainability-oriented BW institutions if the skill allows them.

## Simulation Rules

- Use the repository's actual Agent Skills, starting from `thesis-finder`.
- Simulate both sides until the skill reaches its natural endpoint.
- When the skill asks the student questions, answer in-character from Tina's
  persona.
- Build a complete six-dimension student profile before discovery.
- Do not assume CS, ML, or company fit.
- Route through relevant Tuebingen biology, ecology, geoscience, environmental,
  and sustainability structures.
- For company discovery, stay within Baden-Wuerttemberg and accept that strong
  options may be sustainability institutions rather than classic companies.
- Use live web/source checks when the skill requires current evidence.
- Do not invent chairs, thesis openings, datasets, field-site access, advisor
  capacity, or company options.
- Do not write fictional student data into repository files or the real runtime
  session file. If the skill would normally write a session file, include a
  "Would-be Session File" section in the report instead.

## Required Final Markdown Report

Return a standalone Markdown report with:

1. Test setup
2. Full simulated conversation transcript
3. Completed six-dimension student profile
4. Protocol followed
5. University chair options
6. Company thesis options, if requested
7. Recommended top option
8. Final thesis topic plus chair
9. Outreach angle or first-contact prompt
10. Skill completion assessment
11. Where the skill struggled
12. Suggested improvements to the skill

