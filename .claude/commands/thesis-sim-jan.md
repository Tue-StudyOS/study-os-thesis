---
description: Simulate Jan, a social-science thesis-finder student
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

Jan is a Political Science / Sociology / Media-and-Society student. He is
interested in misinformation, polarization, and online discourse, but wants a
social-science thesis rather than a pure NLP or CS project.

### Response Style

Engaged, critical, and evidence-sensitive. Jan asks about ethics, data access,
and whether methods really answer the social question.

### Initial User Message

```text
I study political science and I'm interested in misinformation, online
discourse, and polarization. I'd like a thesis that uses empirical methods, but
I don't want it to become just a technical text-mining project.
```

### Hidden Student Profile

- Name: Jan.
- Field: Political Science / Sociology / Media and Society.
- Interests: misinformation, polarization, political communication, platform
  governance, public opinion, democratic institutions.
- Methods: social-science theory plus empirical analysis; surveys, interviews,
  content analysis, and possibly computational text analysis.
- Domain: politics, media, social platforms, democratic discourse.
- Thesis style: empirical social-science thesis grounded in theory.
- Skills: R, statistics, survey design, qualitative coding, academic writing;
  limited programming beyond applied analysis.
- No-gos: pure NLP engineering, ethically dubious scraping, corporate marketing
  analytics, and method without theory.
- Hidden tension: attracted to computational methods but worried about research
  ethics and data availability.

### Disclosure Rules

- Do not reveal the whole profile in the first turn.
- When asked about methods, include both quantitative and qualitative options.
- If the assistant frames the thesis as CS/NLP only, push back and ask for the
  social-science theory connection.
- If asked which track to explore, choose university first. Accept company
  exploration only as a secondary track if the assistant is honest about likely
  fit limitations.

## Simulation Rules

- Use the repository's actual Agent Skills, starting from `thesis-finder`.
- Simulate both sides until the skill reaches its natural endpoint.
- When the skill asks the student questions, answer in-character from Jan's
  persona.
- Build a complete six-dimension student profile before discovery.
- Do not assume CS, ML, or company fit.
- Route through relevant Tuebingen social-science, political-science, sociology,
  media, and communication-adjacent structures.
- Treat computational text analysis as optional support, not the thesis identity.
- Use live web/source checks when the skill requires current evidence.
- Do not invent chairs, thesis openings, datasets, scraping permissions, advisor
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
6. Company thesis options only if explored
7. Recommended top option
8. Final thesis topic plus chair
9. Outreach angle or first-contact prompt
10. Skill completion assessment
11. Where the skill struggled
12. Suggested improvements to the skill

