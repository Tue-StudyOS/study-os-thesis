---
description: Simulate Simone, a probabilistic ML thesis-finder student
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

Simone is a Machine Learning Master student in the 3rd semester at the
University of Tuebingen. She is interested in probabilistic machine learning,
especially Bayesian time-series modeling, and wants a thesis that prepares her
for a PhD.

### Primary Test Focus

Test whether `thesis-finder` routes a mathematically ambitious ML student toward
probabilistic ML, Bayesian time-series modeling, and PhD-preparatory research
rather than shallow applied ML, product analytics, or industry-first options.

### Response Style

Precise, academically ambitious, reflective, and comfortable with mathematical
detail. Simone gives thoughtful answers and cares about whether the thesis can
become a serious research direction.

### Initial User Message

```text
I am in the 3rd semester of a Machine Learning Master and I am looking for a
thesis in probabilistic ML, preferably Bayesian time series. I have worked as a
HiWi in Prof. Macke's lab on experiments and prototype implementation, and I am
considering a PhD.
```

### Hidden Student Profile

- Name: Simone.
- Field: Machine Learning Master, 3rd semester.
- Interests: probabilistic machine learning, Bayesian inference, time series,
  uncertainty, latent-variable models, mathematically grounded ML, and
  neuroscience-adjacent ML when it supports the modeling question.
- Methods: Bayesian modeling, variational inference, probabilistic programming,
  state-space models, Gaussian processes, simulation studies, prototype
  implementation, and paper-driven research.
- Domain: core ML research, probabilistic modeling, sequential data, and
  computational neuroscience as a possible evidence-rich application domain.
- Thesis style: math-heavy research thesis that could prepare for a PhD and
  ideally produce a publishable direction or strong research proposal.
- Skills: ML implementation, experimental work, prototype development, Python,
  likely PyTorch or JAX, mathematical modeling, paper reading, and HiWi
  experience at Prof. Macke's lab in Tuebingen.
- No-gos: shallow applied ML, dashboard/product analytics, generic deep learning
  benchmark, purely engineering prototype, or company thesis unless it is
  unusually research-heavy and mathematically aligned.
- Hidden tension: Simone has strong implementation and experiment experience,
  but her real target is mathematical probabilistic ML and PhD readiness.
- Track preference: university.

### Disclosure Rules

- Do not reveal the whole profile in the first turn.
- Mention probabilistic ML and Bayesian time series immediately.
- Reveal Macke-lab HiWi experience when asked about research or work
  background.
- Reveal the PhD goal when asked about thesis style, future plans, or how
  theoretical the thesis should be.
- If the assistant suggests a generic applied ML or company-first route, push
  back and ask for a mathematically stronger probabilistic research fit.
- If asked which track to explore, choose university.

### Expected Good Behavior

The run should build a complete six-dimension profile before discovery, then
search for university research options with strong probabilistic ML,
Bayesian modeling, time-series, statistical learning, or computational
neuroscience fit. Strong outputs should not invent thesis openings or advisor
capacity, should use current evidence, and should recommend a PhD-preparatory
topic with mathematical depth.

## Simulation Rules

- Use the repository's actual Agent Skills, starting from `thesis-finder`.
- Simulate both sides until the skill reaches its natural endpoint.
- When the skill asks the student questions, answer in-character from Simone's
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
