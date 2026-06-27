# Medicine Discovery — Skill Arm

## ID

medicine-discovery-skill

## Scenario

A neurosciences master's student wants to find a thesis supervisor at the
University of Tübingen in the area of neurodegenerative diseases (Parkinson's,
Alzheimer's). The assistant runs inside this repository and should use the
thesis-advising skills through native Codex skill discovery: first
build-student-profile to collect the full profile, then find-university-chairs
to surface relevant chairs at the Hertie Institute for Clinical Brain Research
(HIH) and associated Neurologie departments.

## Initial User Message

Hallo, ich studiere Neurowissenschaften im Master und suche eine Masterarbeit
im Bereich Neurodegeneration — Parkinson, Alzheimer. Kann mir jemand helfen?

## Expected Outcome

The assistant builds a complete student profile (interests, methods/skills,
background, constraints, no-gos) across at least 4 of the 6 profile dimensions,
then runs the discovery skill and surfaces at least 2 of the 6 chairs in the
Medicine ground truth (Gasser, Jucker, Lerche, Ziemann, Siegel, Tabatabai) with
their research areas, the HIH context, and a concrete next step.

## Assistant Start Prompt

You are the thesis-advising agent in this repository. Use the available Agent
Skills when they are relevant: first build-student-profile to collect the
student's full profile across all six dimensions, then find-university-chairs
to discover Tübingen thesis supervisors matching the profile. Do not manually
persist private student data into repository files. Treat public evidence as
potentially stale and avoid inventing papers, chair openings, supervision
capacity, quotas, or advisor commitments. Reply only as the assistant speaking
to the student.
