# Medicine Discovery — Baseline Arm

## ID

medicine-discovery-baseline

## Scenario

A neurosciences master's student wants to find a thesis supervisor at the
University of Tübingen in the area of neurodegenerative diseases (Parkinson's,
Alzheimer's). The assistant is a plain helpful assistant WITHOUT any specialized
thesis-advising skills. It may give general guidance based on general knowledge
but cannot run structured skill-driven discovery.

## Initial User Message

Hallo, ich studiere Neurowissenschaften im Master und suche eine Masterarbeit
im Bereich Neurodegeneration — Parkinson, Alzheimer. Kann mir jemand helfen?

## Expected Outcome

The assistant gives helpful but generic advice: it may mention the Hertie
Institute for Clinical Brain Research (HIH) or the Neurologie department as
institutions to explore, but it does NOT systematically surface the specific
chair-holders (Gasser, Jucker, Lerche, Ziemann, Siegel, Tabatabai) from the
ground truth through structured profile-driven discovery. This arm serves as the
coverage baseline: whatever recall it achieves without the skill is the floor
the skill arm must beat.

## Assistant Start Prompt

You are a helpful academic advisor assistant. Answer the student's question
about finding a thesis supervisor at the University of Tübingen. You do not have
access to any specialized thesis-advising tools or skills. Give your best
general advice based on your knowledge of the German university system and
neuroscience research. Reply only as the assistant speaking to the student.
