# Go-Deeper Branch Validation

- Date: 2026-08-04

## Context

The thesis simulation artifacts showed a recurring pattern after Step N5: the
assistant asked whether the student wanted to go deeper before outreach, the
student answered yes, and the next assistant turn skipped directly to a generic
outreach angle plus `draft-thesis-contact`.

## Finding

The `thesis-finder` workflow described the drill-down branch, but it was not
explicit enough that the branch is blocking. The simulation validation also
checked option-map evidence without checking whether the selected branch was
actually followed.

## Implication

Runs can look evidence-complete while still failing the student's immediate
request. Simulation validation must treat skipped drill-downs as workflow and
usefulness failures, even when the earlier option map is strong.

## Follow-Up

- Keep `thesis-finder` Step N5/R6 explicit that `go deeper` requires a
  `## Deeper Look` response before `draft-thesis-contact`.
- Keep simulation artifacts validating
  `Drill-down branch followed after go-deeper: yes|no|not requested`.
- Add a real runner-side validator if the harness becomes scripted rather than
  instruction-only.
