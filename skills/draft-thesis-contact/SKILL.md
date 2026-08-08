---
name: draft-thesis-contact
description: Draft concise, high-signal first-contact messages to potential thesis advisors using a deep student profile, a concrete research-proposal sketch, relevant papers, and chair fit evidence. Use when asked to write or improve an email to a professor, PhD student, postdoc, lab, chair, or thesis supervisor.
---

# Draft Thesis Contact

Write first-contact messages that help students avoid generic cold emails.

## Workflow

1. Use the student's in-session profile, the selected chair/person, one concrete proposal sketch, and 1-2 evidence points.
2. Before drafting, make sure 1-2 relevant recent papers from the target person/lab are available. If they were not already surfaced earlier in the session (e.g. from `find-university-chairs` or `find-company-thesis-options`), call the `find-recent-papers` skill to get them.
3. Draft a short email with a clear subject, specific motivation, relevant background, a tentative research question, and a low-friction ask.
4. Keep claims modest. Do not imply the chair has an advertised topic unless a current official source explicitly says so.
5. Offer a shorter variant when the first draft is too long.

## Output

Return:

- an **AI-generated notice**, placed above the draft: state plainly that the draft is
  AI-generated, that it should not be sent as-is, and that the student should rewrite at
  least the opening and closing in their own words, cut anything they could not defend if
  asked about it in person, and verify every factual claim themselves
- subject line
- email draft
- one-sentence rationale for why the email is specific
- the 1-2 papers surfaced for this person/lab, with a recommendation that the student skim them before sending — arriving without a sense of what the researcher actually works on reads as generic and undermines the high-signal contact this skill is meant to produce
- optional checklist of details the student should verify before sending

## Rules

- Mention at most 1-2 papers or research areas unless the user asks for a longer message.
- Do not overstate skills, grades, availability, or prior relationship.
- Do not invent openings, funding, capacity, or promises from the advisor.
- Never omit the AI-generated notice, including when the user asks only for the email text
  or for a shortened variant. The notice is student-facing only — do not put a disclosure
  of AI authorship inside the email itself unless the student explicitly asks for one.
- This skill has no runtime database, index, or bundled entity data. Every fact about the person or lab must come from a live source verified during this run.
