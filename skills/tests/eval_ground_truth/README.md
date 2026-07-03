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
| `humanities.md` | Philosophische Fakultät — Philosophisches Seminar | Philosophy of mind, metaphysics and cognitive science |
| `law.md` | Juristische Fakultät — Öffentliches Recht | Constitutional/international law and regulation of new technologies |
| `theology.md` | Evangelisch-Theologische Fakultät | Biblical studies and the history of early Christianity |
| `interdisciplinary.md` | Law + Humanities/IZEW + Science (MPI-IS/Cyber Valley) | Ethics, law and governance of artificial intelligence |

The first four rows are the **structurally easy, well-organized** faculties (used for
the recall/precision/steering proofs, Tasks H–P). The last four were added in
**Task Q (robustness)** to cover the **structurally harder** faculties — Humanities
(a large three-level faculty where chairs live deep in a Seminar), Law (dense German
chair-title formulas), Theology (a small faculty with several vacant chairs) — plus one
**interdisciplinary** persona spanning three faculties to test routing breadth. See
each file's Notes for the specific hardness it exercises.

## What "recall" means here

**Recall = (ground-truth chairs surfaced by the skill run) / (total ground-truth chairs in the file)**

A chair is counted as **surfaced** if the skill's output MAP mentions the chair-holder by
name OR names their group/institute in a way that unambiguously identifies them (e.g.
"Hertie Institute — Neurodegenerative Diseases" maps to Thomas Gasser even without
naming him explicitly).

A chair is **not counted** if it appears only in a generic sentence ("there are many
neuroscience labs at Tübingen") without specific identification.

**Interdisciplinary file (`interdisciplinary.md`) — routing metric.** For the
cross-faculty persona, recall is the same fraction (anchors surfaced / total anchors),
but **also report per-faculty coverage**: whether the run surfaced at least one anchor
from *each* spanned faculty (Law, Humanities/IZEW, Science-ML). Surfacing five law
chairs but nothing from the ethics centers or ML side is an interdisciplinary-routing
miss even at high raw recall — the point of that file is routing breadth, not depth in
one faculty.

## What "precision" means here

Recall alone rewards over-surfacing (list everything remotely related and recall goes
up for free). Precision catches that:

**Precision = (surfaced options judged relevant to the profile) / (total surfaced options in the MAP)**

An option counts as **relevant** if a reasonable reader would agree it plausibly fits
the profile's stated interests/methods/domain — i.e. the skill's own "Relevance
rationale" field for that option holds up on inspection, even if the option isn't in
the ground-truth list (the ground truth is not exhaustive; a correct option missing
from it is still relevant, not noise).

An option counts as **not relevant** (noise) if it's a generic/padding entry whose
rationale is weak or unrelated to the stated profile — e.g. a chair included mainly
because it's prominent, not because it fits.

Precision is scored by human judgment on the MAP output; there is no automated check.

## Target

**≥ 70% recall** per faculty on the first eval run (Task H). No fixed precision
target yet (Roadmap-K introduced the metric; a target should be set once a few live
runs establish a baseline) — treat a precision drop across a skill change as a signal
worth investigating, same as a recall drop.

This is a starting target, not a pass/fail gate — the honest result matters more than
hitting the number. If the skill consistently surfaces 5 of 6 known chairs per faculty
that is a strong signal; 2 of 6 indicates a systematic gap worth diagnosing.

## How to score a skill run

1. Run the skill with a student profile whose interests match the **sample interest**
   stated at the top of each ground-truth file.
2. Collect the full MAP output from the skill.
3. For each row in the ground-truth table, mark it **found** (✓) or **missed** (✗).
4. Compute: `recall = count(✓) / total rows`.
5. For every option actually surfaced in the MAP (not just ground-truth rows), mark it
   **relevant** or **not relevant** per the definition above.
6. Compute: `precision = count(relevant) / total surfaced options`.
7. Record per-faculty recall, precision, and the overall means in the findings doc
   (or the live-eval runbook log for a single-faculty re-check —
   [2026-07-02-live-eval-runbook.md](../../../findings/no_db_universal_skill/2026-07-02-live-eval-runbook.md)).

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
