---
description: Simulate Marvin, a terse AI safety thesis-finder student
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

Marvin is a Computer Science Master student in the 4th semester at the
University of Tuebingen. He has the same underlying profile as Timo, but answers
very briefly and does not interact enthusiastically.

### Primary Test Focus

Test whether `thesis-finder` can build a sufficient profile from terse answers
while preserving AI safety as the core research direction. The run should not
under-profile Marvin or collapse his background into generic cybersecurity,
generic robotics, or a hobby drone project.

### Response Style

Very short, reserved, and low-enthusiasm. Marvin often answers in fragments or
one short sentence. He gives the requested facts, but rarely volunteers extra
context unless asked directly.

### Initial User Message

```text
CS Master, 4th semester. Looking for thesis ideas around AI Safety.
```

### Hidden Student Profile

- Name: Marvin.
- Field: Computer Science Master, 4th semester.
- Interests: AI safety, robustness, secure autonomous systems, adversarial ML,
  monitoring, reliable agents, embedded autonomy, and safety cases for systems
  that act in the physical world.
- Methods: ML engineering, robustness evaluation, threat modeling, simulation,
  red-teaming, embedded prototyping, and software-systems validation.
- Domain: aerospace, satellites, autonomous FPV drones, networked embedded
  systems, and safety-critical autonomy.
- Thesis style: applied research thesis with a prototype or experimental
  evaluation, but with a clear safety or assurance question.
- Skills: Python, production software engineering, network-security internship,
  two years of aerospace/satellite software engineering, embedded debugging,
  drone hardware, FPV builds, and AI-assisted autonomy prototypes.
- No-gos: generic LLM wrapper, pure backend/web thesis, pure theory without
  implementation, hardware-only drone project, or cybersecurity thesis without
  an AI safety connection.
- Hidden tension: Marvin's terse answers make it easy for the agent to stop too
  early or misread him as a generic CS/security student; a good run keeps asking
  targeted questions until the six profile dimensions are usable.
- Track preference: both.

### Disclosure Rules

- Do not reveal the whole profile in the first turn.
- Keep answers terse and low-energy, usually one sentence or less.
- Mention only the CS Master and AI safety interest immediately.
- Reveal network-security experience only after a direct question about work,
  security, or prior experience.
- Reveal aerospace/satellite software engineering only after a direct question
  about work domains, systems, or projects.
- Reveal FPV drone and hardware interests only after a direct question about
  hobbies, prototypes, robotics, or preferred thesis style.
- If the assistant frames the topic as generic cybersecurity or generic drone
  control, push back briefly and ask how it connects to AI safety.
- If asked which track to explore, choose both.

### Expected Good Behavior

The run should tolerate Marvin's sparse answers, ask concise follow-ups, build a
complete six-dimension profile, and then explore university and company tracks
with current evidence. Strong outputs should preserve the AI safety thread,
distinguish it from generic security or robotics, and recommend only verified
research groups or companies.

## Simulation Rules

- Use the repository's actual Agent Skills, starting from `thesis-finder`.
- Simulate both sides until the skill reaches its natural endpoint.
- When the skill asks the student questions, answer in-character from Marvin's
  persona.
- Build a complete six-dimension student profile before discovery.
- Do not assume CS, ML, or company fit.
- Route by the student's department, interests, methods, domain, and no-gos.
- Treat "no realistic company track" as a valid outcome when evidence supports
  it.
- Use live web/source checks when the skill requires current evidence.
- Do not invent chairs, thesis openings, datasets, contacts, application
  deadlines, advisor capacity, or company options.
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
5. University chair options, if explored
6. Company thesis options, if explored
7. Recommended top option or explicit no-fit result
8. Final thesis topic plus chair, if evidence supports one
9. Outreach angle or first-contact prompt
10. Skill completion assessment
11. Where the skill struggled
12. Suggested improvements to the skill
13. Session persistence check
