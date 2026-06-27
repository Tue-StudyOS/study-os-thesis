# Eval Ground Truth

This directory contains hand-curated benchmarks for measuring the coverage of the
`find-university-chairs` discovery skill against known, findable thesis supervisors
at the University of Tübingen.

## Files

| File | Faculty | Sample interest |
|---|---|---|
| `cs_seed/` | Science — Informatik (Computer Science / ML) | Machine learning and AI research |
| `medicine.md` | Medizinische Fakultät | Neurodegenerative diseases and clinical brain research |
| `psychology.md` | Science — Psychologie (Psychology) | Cognitive neuroscience and experimental decision-making |
| `wiso.md` | Wirtschafts- und Sozialwissenschaftliche Fakultät (WiSo) | Comparative politics and political economy |

## What "recall" means here

**Recall = (ground-truth chairs surfaced by the skill run) / (total ground-truth chairs in the file)**

A chair is counted as **surfaced** if the skill's output MAP mentions the chair-holder by
name OR names their group/institute in a way that unambiguously identifies them (e.g.
"Hertie Institute — Neurodegenerative Diseases" maps to Thomas Gasser even without
naming him explicitly).

A chair is **not counted** if it appears only in a generic sentence ("there are many
neuroscience labs at Tübingen") without specific identification.

## Target

**≥ 70% recall** per faculty on the first eval run (Task H).

This is a starting target, not a pass/fail gate — the honest result matters more than
hitting the number. If the skill consistently surfaces 5 of 6 known chairs per faculty
that is a strong signal; 2 of 6 indicates a systematic gap worth diagnosing.

## How to score a skill run

1. Run the skill with a student profile whose interests match the **sample interest**
   stated at the top of each ground-truth file.
2. Collect the full MAP output from the skill.
3. For each row in the ground-truth table, mark it **found** (✓) or **missed** (✗).
4. Compute: `recall = count(✓) / total rows`.
5. Record per-faculty recall and the overall mean in the findings doc (Task H output).

## What the ground truth is NOT

- **Not exhaustive.** Each file lists only the chairs a reasonably careful web search
  surfaced and verified on 2026-06-27. There are more supervisors at each faculty;
  missing them from this list is not a skill failure.
- **Not a claim about quality.** A surfaced chair may be irrelevant to the specific
  student profile — relevance is scored separately (Task G rubric, not this metric).
- **Not permanent.** Chair-holders retire, move, or change research focus. Re-verify
  before re-running evals if more than ~6 months have passed since the `Date verified`
  column in each file.

## CS seed data

The `cs_seed/` directory was moved here from the former `find-university-chairs/references/`
runtime location in Task E. It contains curated chairs and researchers for the CS/ML
faculty (generated 2026-06-13, moved 2026-06-27). Use `cs_seed/chairs/INDEX.md` as the
ground-truth table for the CS faculty (same scoring rules as above).
