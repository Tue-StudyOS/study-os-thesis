---
description: Simulate {name}, a thesis-finder student
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

{name} is a {faculty_field} student at the University of Tuebingen. This
simulation is designed to test thesis-finder routing beyond a single default
department.

### Primary Test Focus

{primary_test_focus}

### Response Style

{response_style}

### Initial User Message

```text
{initial_user_message}
```

### Hidden Student Profile

- Name: {name}.
- Field: {faculty_field}.
- Interests: {interests}
- Methods: {methods}
- Domain: {domain}
- Thesis style: {thesis_style}
- Skills: {skills}
- No-gos: {no_gos}
- Hidden tension: {hidden_tension}
- Track preference: {track_preference}

### Disclosure Rules

{disclosure_rules}

### Expected Good Behavior

{expected_good_behavior}

## Simulation Rules

- Use the repository's actual Agent Skills, starting from `thesis-finder`.
- Simulate both sides until the skill reaches its natural endpoint.
- When the skill asks the student questions, answer in-character from the
  persona.
- Build a complete six-dimension student profile before discovery.
- Do not assume CS, ML, or company fit.
- Route by the student's department, interests, methods, domain, and no-gos.
- Treat "no realistic company track" as a valid outcome when evidence supports
  it.
- Use live web/source checks when the skill requires current evidence.
- Do not invent chairs, thesis openings, datasets, contacts, application
  deadlines, advisor capacity, or company options.
- Do not write fictional student data into repository files or the real runtime
  session file. If the skill would normally write a session file, include a
  "Would-be Session File" section in the report instead.

## Required Final Markdown Report

Return a standalone Markdown report with:

1. Test setup
2. Full simulated conversation transcript
3. Completed six-dimension student profile
4. Protocol followed
5. University chair options, if explored
6. Company thesis options, if explored
7. Recommended top option or explicit no-fit result
8. Final thesis topic plus chair, if evidence supports one
9. Outreach angle or first-contact prompt
10. Skill completion assessment
11. Where the skill struggled
12. Suggested improvements to the skill

