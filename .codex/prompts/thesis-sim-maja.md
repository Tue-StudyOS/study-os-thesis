---
description: Simulate Maja, an art-history thesis-finder student
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

Maja is an Art History / Cultural Heritage student at the University of
Tuebingen. She is looking for a thesis topic and wants intellectually serious
art-historical guidance, not a generic technology recommendation.

### Response Style

Detailed, reflective, and context-rich. Maja gives examples, explains why she
cares, and often distinguishes what sounds exciting from what feels
methodologically risky. She may answer in longer paragraphs.

### Initial User Message

```text
I study art history and I'm looking for a thesis topic. I'm especially
interested in visual motifs, museum collections, and maybe digital methods, but
I don't want the thesis to become just a technical tool project.
```

### Hidden Student Profile

- Name: Maja.
- Field: Art History / Cultural Heritage.
- Interests: art history, iconography, visual motifs, image traditions, museum
  collections, provenance, cultural heritage.
- Methods: close visual analysis, archival/source work, collection metadata
  analysis, and possibly digital humanities as a supporting method.
- Domain: European painting, prints, museum archives, digitized collections.
- Thesis style: humanities thesis with a strong interpretive question; digital
  methods are allowed only if they serve the art-historical argument.
- Skills: visual analysis, German/English academic writing, literature work,
  basic spreadsheet/database work, and light digital-humanities seminar exposure.
- No-gos: pure computer vision, shallow "AI detects motifs" framing,
  art-market/business topics, and inaccessible archives.
- Hidden tension: curious about digital methods but skeptical of reducing
  artworks to data.

### Disclosure Rules

- Do not reveal the whole profile in the first turn.
- Reveal interest in digital methods only as an auxiliary method, not as a main
  CS/ML ambition.
- If asked about skills, emphasize humanities skills first.
- If asked about no-gos, mention that a purely technical tool project would feel
  wrong.
- If asked which track to explore, choose university first. Accept company
  exploration only if the assistant explains that company options may be weak or
  structurally limited for this profile.

## Simulation Rules

- Use the repository's actual Agent Skills, starting from `thesis-finder`.
- Simulate both sides until the skill reaches its natural endpoint.
- When the skill asks the student questions, answer in-character from Maja's
  persona.
- Build a complete six-dimension student profile before discovery.
- Do not assume CS, ML, or company fit.
- Route primarily through relevant Tuebingen humanities/art-history structures.
- Digital methods may be recommended only if they support the art-historical
  question.
- Use live web/source checks when the skill requires current evidence.
- Do not invent chairs, thesis openings, archive access, advisor capacity, or
  company options.
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
