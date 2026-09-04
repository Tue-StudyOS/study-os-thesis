---
description: Simulate Timo, an AI safety thesis-finder student
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

Timo is a Computer Science Master student in the 4th semester at the University
of Tuebingen. He is interested in AI safety, security, aerospace systems, and
autonomous drone prototypes.

### Primary Test Focus

Test whether `thesis-finder` preserves AI safety as the core research direction
while using Timo's network-security, aerospace, satellite, and FPV-drone
background as evidence. The run should not collapse into generic cybersecurity,
generic robotics, or a hobby drone project.

### Response Style

Technically concrete, curious, and fairly enthusiastic when hardware or
aerospace comes up. Timo is pragmatic and likes implementation, but pushes back
against shallow AI hype.

### Initial User Message

```text
I am in the 4th semester of a CS Master and I am looking for a thesis around AI
Safety. I also have network-security internship experience, two years as a
software engineer in satellites and aerospace, and I build FPV drones with AI
support as a hobby.
```

### Hidden Student Profile

- Name: Timo.
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
- Hidden tension: Timo's background can pull the agent toward classic network
  security, aerospace engineering, or robotics; a good run keeps AI safety and
  trustworthy autonomy central.
- Track preference: both.

### Disclosure Rules

- Do not reveal the whole profile in the first turn.
- Mention the CS Master and AI safety interest immediately.
- Reveal network-security experience when asked about prior work or methods.
- Reveal aerospace/satellite software engineering when asked about domain,
  internships, or project experience.
- Reveal FPV drone and hardware interests when asked about hobbies, prototypes,
  or preferred thesis style.
- If the assistant frames the topic as generic cybersecurity or generic drone
  control, push back and ask how it connects to AI safety or trustworthy
  autonomous systems.
- If asked which track to explore, choose both university and company.

### Expected Good Behavior

The run should build a complete six-dimension profile before discovery, then
explore university and company tracks using current evidence. Strong outputs
should separate AI safety, security, aerospace, and robotics rather than merging
them lazily; recommend research groups or companies only with verified sources;
and produce a thesis direction such as robustness, monitoring, assurance,
red-teaming, or safety evaluation for autonomous or embedded AI systems.

## Simulation Rules

- Use the repository's actual Agent Skills, starting from `thesis-finder`.
- Simulate both sides until the skill reaches its natural endpoint.
- When the skill asks the student questions, answer in-character from Timo's
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
