# Eval Ground Truth — Company Seed

This directory contains hand-curated benchmarks for measuring the recall of the
`find-company-thesis-options` skill against known, findable BW companies with thesis
programs. It is the company-sector analogue of the university-chair ground truths in
the parent `eval_ground_truth/` directory.

## Files

| File | Profile | Sample interest |
|---|---|---|
| `C1-ml-automotive-robotics.md` | ML/AI + automotive/robotics | Computer vision, RL, autonomous systems at BW automotive/robotics companies |
| `C2-medtech-health.md` | Medtech + health | Medical imaging, biosensors, point-of-care diagnostics at BW medtech companies |
| `C3-software-data-enterprise.md` | Software/data + enterprise | Distributed systems, data pipelines, enterprise LLMs at BW software companies |

## What "recall" means here

**Primary recall = (ground-truth companies surfaced by the skill run) / (total ground-truth companies in the file)**

A company is counted as **surfaced** if the skill's option map:
- Names the company by name, OR
- Unambiguously names its relevant division or R&D lab (e.g. "Bosch Center for AI" → counts for Robert Bosch GmbH; "Zeiss Meditec" → counts for Carl Zeiss AG)

A company is **not counted** if it appears only in a generic sentence ("there are many automotive companies in BW") without specific identification.

## Secondary metric: thesis-signal accuracy

For each surfaced ground-truth company, check whether the skill's thesis signal classification matches the expected value in the ground truth table:

| Ground truth signal | Expected skill output | Counts as correct? |
|---|---|---|
| `explicit opening` | `explicit opening` or `active program` | ✓ |
| `active program` | `active program` | ✓ |
| `active program` | `unclear` | ✗ (skill under-classified) |
| `unclear` | `unclear` | ✓ |
| `unclear` | `explicit opening` or `active program` | ✗ (skill over-classified — hallucination risk) |

**Thesis-signal accuracy = correct classifications / total surfaced ground-truth companies.**
Over-classification (claiming `explicit opening` when the ground truth is `unclear`) is the more serious error — it can mislead students.

## Target

**≥ 70% primary recall** per profile.
This is the Phase-2 gate criterion. All three profiles must clear 70% for the gate to be GREEN.
A partial result (1 or 2 profiles < 70%) is AMBER; fix plan required.

The thesis-signal accuracy is a secondary metric — reported but not gated. A score of ≥80%
correct signal classification is aspirational; widespread over-classification is a fail.

## How to score a skill run

1. Run `find-company-thesis-options` with the student profile from the ground truth file.
2. Collect the full option map output.
3. For each row in the ground-truth table, mark it **found** (✓) or **missed** (✗).
4. Compute: `recall = count(✓) / total rows`.
5. For each found company, compare the skill's thesis signal to the expected value.
6. Compute thesis-signal accuracy: `correct_signals / count(✓)`.
7. Record per-profile recall, signal accuracy, and the overall gate verdict in the findings doc.

## What the ground truth is NOT

- **Not exhaustive.** Each file lists only companies a careful web search surfaced and verified
  on 2026-06-28. Many other BW companies with thesis programs exist; missing them is not a skill failure.
- **Not a promise of open positions.** A company appearing here means we found evidence of an
  active or inferable thesis program as of the verification date. Programs open and close. The
  skill's coverage caveat applies here too.
- **Not permanent.** Startup entries are especially volatile. Re-verify if more than 6 months
  have passed since the `Date verified` column.

## Relationship to Phase 1 eval ground truth

This directory follows the same scoring conventions as the parent `eval_ground_truth/` directory.
The key difference: university chairs are almost always publicly listed (easy ground truth);
company thesis programs are inconsistently publicized (harder ground truth). The ≥70% target
is unchanged because the skill's backbone anchoring should partially compensate for lower
web-signal quality.
