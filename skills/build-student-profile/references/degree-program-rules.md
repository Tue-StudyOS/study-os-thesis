# Degree Program Resolution Rules

How to resolve a student's degree program, thesis level, and thesis duration for
**any faculty** of the University of Tübingen.

This file contains no program list. That is deliberate: the university runs far
more programs than any bundled table could stay honest about, and nobody
maintains a list here after the project ends. A stale table is worse than none,
because it is wrong silently — the run reads a plausible value and never asks.
The three facts below are cheap to obtain correctly at run time, so obtain them.

## What has to be resolved

Exactly three things, in this order. Nothing else about the program matters for
scoping a thesis proposal.

| # | Fact | Primary source | Fallback |
|---|---|---|---|
| 1 | Program name | The student, in their own words | — |
| 2 | Thesis level (Bachelor / Master / other) | The student | Verify live if they are unsure |
| 3 | Thesis duration (Bearbeitungszeit) | The student's own exam regulations | Responsible exam office page |

## 1. Program name

Accept whatever the student says, in German or English, and record it verbatim.
Do not normalize it against a list, and do not treat an unfamiliar name as
suspect — the university's program inventory is large and changes.

Only ask a follow-up when the name is genuinely ambiguous for the search, for
example when it does not reveal the faculty, or when a joint or teacher-education
program would change which chairs are relevant.

## 2. Thesis level

The student knows their own level. Ask, take the answer, move on.

Two rules constrain what you may infer when they are unsure:

- Never infer the level from the program name. Some programs exist at one level
  only — a Master-only program has no Bachelor track, and proposing a Bachelor
  scope for it is a hard error.
- Never treat "both levels exist" as the default. If it matters and the student
  is unsure, verify against the program's own page before scoping.

## 3. Thesis duration

**Do not assume a duration. There is no university-wide value.**

The Bearbeitungszeit is fixed by the Prüfungsordnung, which differs **per faculty
and per Fassung**, and is stated in weeks by some faculties and months by others.
Two students at this university can hold different, equally correct answers.

This matters because a wrong duration is invisibly wrong: it produces a proposal
that is confidently scoped to the wrong size, and nothing in the conversation
surfaces the error. Scope is the one place where a plausible guess does real
damage.

Therefore:

- Ask the student for the duration in their regulations. Many know it, because
  it is the deadline they plan around.
- If they do not know and the scope depends on it, verify live against the
  responsible exam office or the program's own regulations.
- If neither is available, say so and scope the proposal against an explicitly
  stated assumption the student can correct. Never let an unverified figure pass
  as fact.

Use the resolved duration only to size the proposal: a shorter window needs a
tighter question and less setup risk than a longer one.

## Source axes for live verification

Use these only when the student cannot answer and the fact changes the scope.

| Axis | Purpose | Example query shape |
|---|---|---|
| Program page | Confirm the program exists and which levels it offers | `site:uni-tuebingen.de {program_de} Studiengang Bachelor Master` |
| Exam office | Find the office responsible for the student's faculty | `site:uni-tuebingen.de Prüfungsamt {faculty_de}` |
| Regulations | Find the binding Bearbeitungszeit | `site:uni-tuebingen.de {program_de} Prüfungsordnung Bearbeitungszeit` |
| Faculty page | Resolve which faculty a program belongs to | `site:uni-tuebingen.de {program_de} Fakultät` |

## Verification

A level or duration may be used for scoping only if it came from the student, or
from a page the run actually opened. Record which of the two it was.

Prefer the exam office or the regulations over a faculty prose page: prose pages
paraphrase the regulations and drop the exceptions.

If the regulations name several Fassungen, the student's enrolment year decides
which applies. When that is unclear, ask rather than picking the newest.

## Failure modes

- If live verification is unavailable, ask the student and proceed on a stated
  assumption. Do not fall back on model memory for a duration or a level.
- If a program appears not to exist, assume the name is unfamiliar rather than
  invalid, and ask the student to confirm the spelling or the faculty.
- If the student is between programs or in a transition, take the regulations
  they will actually submit under.
