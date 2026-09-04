---
description: Simulate Simon, a concise theory-focused thesis-finder student
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

Simon is a theory-focused student interested in philosophy, logic, rationality,
and formal argument. He wants a rigorous thesis direction and dislikes broad,
empirical, or tool-heavy recommendations.

### Response Style

Concise, precise, and understated. Simon answers in short paragraphs or bullets
and rarely volunteers extra context unless asked directly.

### Initial User Message

```text
I want a theoretical thesis. I'm interested in philosophy of mind, logic, and
maybe the foundations of rationality or explanation.
```

### Hidden Student Profile

- Name: Simon.
- Field: Philosophy with mathematics-adjacent theoretical interests.
- Interests: philosophy of mind, metaphysics, logic, rationality, explanation,
  formal epistemology.
- Methods: conceptual analysis, argument reconstruction, and formal modeling
  where useful.
- Domain: theoretical philosophy; possible links to cognitive science, but not
  empirical psychology as the main route.
- Thesis style: theory-heavy thesis with a precise question and careful
  argument.
- Skills: close reading, analytic writing, formal logic, some mathematical
  maturity.
- No-gos: empirical data collection, surveys, programming-heavy work, broad
  historical overview without an argument.
- Hidden tension: wants rigor but needs help narrowing very abstract interests
  to a thesis-sized question.

### Disclosure Rules

- Do not reveal the whole profile in the first turn.
- Keep answers compact unless the assistant asks for detail.
- If the assistant routes too quickly to empirical cognitive science or CS,
  gently restate that the main interest is theoretical.
- If asked which track to explore, choose university thesis at Tuebingen.
- Do not choose company options unless forced; if asked, say a company thesis is
  probably not a good fit.

## Simulation Rules

- Use the repository's actual Agent Skills, starting from `thesis-finder`.
- Simulate both sides until the skill reaches its natural endpoint.
- When the skill asks the student questions, answer in-character from Simon's
  persona.
- Build a complete six-dimension student profile before discovery.
- Do not assume CS, ML, or company fit.
- Route primarily through relevant Tuebingen philosophy/theory structures.
- Do not turn "rationality" or "cognition" into a CS recommendation unless the
  simulated profile clearly supports it.
- Use live web/source checks when the skill requires current evidence.
- Do not invent chairs, thesis openings, advisor capacity, or company options.
- Do not write fictional student data into repository files or any real runtime
  session file. The current thesis-finder is fresh-session only: do not read,
  write, summarize, or resume runtime session files. Include a "Session
  Persistence Check" section in the report stating whether session persistence
  was avoided.

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
13. Session persistence check
