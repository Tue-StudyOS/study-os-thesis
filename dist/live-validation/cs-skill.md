# CS — Skill Arm (live)

**Date:** 2026-07-02 (re-run 2) · **Faculty:** Science → FB Informatik (+ MPI-IS / ELLIS / Cyber Valley) ·
**Arm:** SKILL · **Role:** Roadmap-J runbook re-run after Task O (relevance/no-go/affiliation tightening)

## Persona (6 dimensions — reused verbatim for comparability)

- **Interests:** Machine learning / AI research — deep learning, probabilistic methods, causality, representation learning
- **Methods:** Computational, empirical, Python
- **Domain:** General AI/ML research (no specific application domain)
- **Thesis style:** Applied/empirical — experiments, trained models
- **Skills:** Python, PyTorch, statistics/probability
- **No-gos:** Hardware/embedded systems; pure math proofs

## Route (search-strategy §2)

Primary: Science → FB Informatik. Required Pass-1 legs for AI/ML: MPI for Intelligent
Systems (`is.mpg.de/departments`), ELLIS Tübingen / Cyber Valley.

## Pass 1 — backbone crawl (live, this run)

- **FB Informatik** `forschung.html` → fetched live, reachable. "Maschinelles Lernen"
  section lists 22 groups this run (fuller than either prior run's list — page content
  keeps growing/changing).
- **MPI-IS** `is.mpg.de/departments` → **bot-detection block again** (same known gap,
  third run in a row). Fell back to targeted web search per precedent — confirmed
  Schölkopf (Empirical Inference) and Brendel (Robust ML) active via search.
- **Cyber Valley / ELLIS** → `cyber-valley.de/en/research-groups` resolved this run
  (unlike the last run's 404); also cross-checked `institute-tue.ellis.eu/research-groups`.

## Quality-filter pass (search-strategy §5, applied live this run)

Applying the new **topical-justification filter**: a chair from the "Maschinelles
Lernen" page section is only included if its own stated research matches the profile's
interests (deep learning, probabilistic methods, causality, representation learning) —
not merely because it shares the page section. Filtered out on this basis (not listed
as numbered options below):

- **Kognitive Modellierung — Prof. Martin Butz:** cognitive science / predictive-processing
  models of human cognition, not AI/ML research. Same domain-mismatch case the filter
  was written for.
- **Climate, Energy and Machine Learning Systems — Jun.-Prof. Nicole Ludwig:** domain is
  climate/energy-specific; profile states general AI/ML, no application domain.
- **Machine Learning Engineering and Technology Transfer — Prof. Peter Gehler:**
  technology-transfer/applied-engineering focus, not a research-thesis fit.
- **Maschinelles Lernen in der Wissenschaft II — Prof. Mario Krenn:** AI-for-scientific-
  discovery in physics — domain-specific application, weaker methods-novelty fit than
  Macke below.
- **Social Foundations of Computation — Prof. Moritz Hardt:** algorithmic fairness /
  social-ML theory — domain (fairness/social) doesn't match stated interests closely
  enough to justify inclusion; noted as borderline, not a clean-cut exclusion like Butz.
- **Autonomous Systems — Dr. Shahram Eivazi:** robotics-flavored, likely hardware no-go
  conflict; weak evidence of an independent research chair.

Applying the sharpened **no-go ambiguity rule** (§7): kept-with-flag rather than excluded:

- **Foundations of Machine Learning Systems — Prof. Robert C. Williamson:** re-checked
  this run. His stated work (statistical foundations, aggregation/fairness theory,
  f-divergences) still doesn't intersect meaningfully with the profile's stated
  interests (deep learning/causality/representation learning) — **excluded via the
  topical-justification filter**, same judgment as the prior run's precision scoring,
  now backed by an explicit rule instead of ad hoc call.

## Affiliation-currency check (SKILL.md 2f, new this run)

Ran the new check on **Scalable Trustworthy AI — Prof. Dr. Seong Joon Oh** (topically a
strong match: trustworthy AI, robustness, uncertainty). Query
`"Seong Joon Oh" Tübingen "now at" OR "moved" OR "joins" KAIST 2026` confirms: **Oh
moved the STAI group from Tübingen to KAIST in February 2026**, now Associate Professor
there. The FB-Informatik listing (crawled live today, same as last run) still shows the
group under Tübingen with no relocation notice.

Per SKILL.md 2f, **not silently dropped** — flagged and ranked last, excluded from the
actionable/numbered option list:

> ⚠ **Scalable Trustworthy AI — Prof. Dr. Seong Joon Oh — affiliation not confirmed
> current.** Topically a strong match, but confirmed relocated to KAIST (Feb 2026) via
> live search. Not a current Tübingen thesis option. Do not contact this address.

This is the same relocation the prior run caught by incidental diligence; this run it's
caught by the codified 2f affiliation-currency check instead — the fix is now
systematic rather than dependent on the agent happening to notice.

## Option Map (grouped by interest dimension)

### Causality & empirical inference

**1. Empirical Inference — Prof. Dr. Bernhard Schölkopf** (MPI-IS / ELLIS Institute
Tübingen — [is.mpg.de/ei](https://is.mpg.de/ei), confirmed via search since direct
fetch was bot-blocked)
- Relevance: core match — causality, kernel methods, representation learning.
- Pros/difficulties: very high-profile group, extremely competitive.
- Conversation starter: causal representation learning for out-of-distribution
  generalization.

### Reinforcement learning / autonomous systems

**2. Distributed Intelligence — Prof. Dr. Georg Martius** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: model-based reinforcement learning, representation learning for control.
- ⚠ Possible no-go conflict (ambiguous, kept per §7): ERC-funded work targets
  "versatile robots"; primary methodology is ML/RL software, but confirm the specific
  thesis topic doesn't cross into hardware.
- Conversation starter: model-based RL for sample-efficient robot skill learning
  (simulation-only variant).

### Deep learning & representation learning

**3. Maschinelles Lernen — Prof. Dr. Matthias Hein**
- Relevance: core ML — robustness, adversarial examples, optimization.

**4. Theorie des maschinellen Lernens — Prof. Dr. Ulrike von Luxburg**
- Relevance: ML theory, clustering, graph-based learning.
- ⚠ Possible no-go conflict (ambiguous, kept per sharpened §7 wording): theory-heavy,
  but has an empirical component (clustering/embedding evaluation) — not proof-only.

**5. Computational Neuroscience and Machine Learning — Prof. Dr. Matthias Bethge**
- Relevance: representation learning, computational neuroscience + ML.

**6. Robust Machine Learning — Prof. Dr. Wieland Brendel** (MPI-IS / ELLIS Institute
Tübingen — confirmed via search, direct MPI-IS page bot-blocked)
- Relevance: robustness, self-supervised/representation learning, causal structure
  learning.

**7. Autonomes maschinelles Sehen (Autonomous Vision) — Prof. Dr.-Ing. Andreas Geiger**
- Relevance: generative 3D scene representations, computer vision ∩ deep learning.
- ⚠ Availability caveat: on leave of absence, not currently hiring new PhD/postdoc
  positions; BSc/MSc theses still offered on request.

**8. Multimodal Learning — Prof. Dr. Hilde Kühne**
- Relevance: multimodal deep learning, representation learning across modalities —
  core methods match.

### Probabilistic methods

**9. Methoden des maschinellen Lernens — Prof. Dr. Philipp Hennig**
- Relevance: direct match — probabilistic numerics, Bayesian inference, uncertainty.

### ML for science (borderline domain fit — kept, methods overlap is strong)

**10. Maschinelles Lernen in der Wissenschaft — Prof. Dr. Jakob Macke**
- Relevance: methods overlap strongly (differentiable simulation, deep learning,
  simulation-based inference — core probabilistic-methods fit), but domain is
  computational neuroscience/biophysics, not general AI/ML as stated. Kept as
  borderline, flagged.

### Excluded by no-go (not included in the map)

- **Kognitive Systeme — Prof. Dr. Andreas Zell:** hardware/embedded/FPGA/robotics is
  the primary methodology for multiple active projects — clear, non-ambiguous match
  for the hardware/embedded no-go.

> **Coverage caveat:** This map covers publicly visible chairs as of 2026-07-02.
> Chairs with a weak web presence may be missing. To catch them: visit the FB
> Informatik research page and the MPI-IS / ELLIS Tübingen / Cyber Valley pages
> directly, ask the Fachschaft, and check the official Vorlesungsverzeichnis. The
> MPI-IS department listing failed to load live during this run (bot-block, third
> run in a row) — MPI-IS coverage relies on targeted web search per person, a
> narrower net than a direct crawl would give.
