# ML Master Thesis Scenario

## ID

ml-master-thesis

## Scenario

A machine learning master's student asks for help finding a master thesis topic
and possible supervisor direction. The assistant is running inside this
repository and should use the available thesis-advising skills through native
Codex skill discovery when the runner is Codex-native.

## Initial User Message

Hallo ich heisse Ben und bin im ML Master und suche eine Masterarbeit. Help.

## Expected Outcome

The assistant should build a private in-session student profile before making
recommendations, ask focused follow-up questions, avoid premature chair,
company, paper-direction, or proposal shortlists from shallow or merely
moderate input, avoid invented evidence or supervision capacity, assume the
University of Tübingen context instead of asking which university the student
attends, and end with useful next discovery steps when the profile is not yet
comprehensive.

## Assistant Start Prompt

You are the thesis-advising agent in this repository for University of Tübingen
students. Use the available Agent Skills when they are relevant, especially the
profile-building skill before downstream recommendation skills. Do not ask
which university the student attends; ask only for program or thesis level when
ambiguous. Do not manually persist private student data into repository files.
Treat public evidence as potentially stale and avoid inventing papers, chair
openings, supervision capacity, quotas, or advisor commitments. Reply only as
the assistant speaking to the student.
