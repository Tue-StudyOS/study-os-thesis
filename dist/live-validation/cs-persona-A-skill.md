# CS — Persona A — Skill Arm (live)

**Date:** 2026-07-02 · **Faculty:** Science → FB Informatik (+ MPI-IS / ELLIS / Cyber Valley) ·
**Arm:** SKILL · **Role:** Roadmap Task P (steering proof) — persona A of the A/B divergence test.

> Task-P note: this is **not** the Task O persona. Persona A and Persona B are two
> different students who both plausibly route to FB-Informatik but have deliberately
> **inverted no-gos** (A excludes computer vision; B excludes heavy Bayesian/probabilistic
> theory). The test is whether the two maps diverge in the direction each profile predicts.

## Persona A (6 dimensions)

- **Interests:** Causality & causal representation learning; probabilistic machine learning
  (Bayesian inference, probabilistic numerics, uncertainty quantification).
- **Methods:** Computational + empirical; probabilistic modelling; Python. Comfortable with
  math but wants methods tied to working code / experiments, not proof-only output.
- **Domain:** General ML methodology (no fixed application domain); occasional interest in
  simulation-based scientific inference as a *methods* playground.
- **Thesis style:** Methods-development thesis — implement an inference/causal-discovery
  method and evaluate it empirically.
- **Skills:** Python, PyTorch/JAX, probabilistic-programming (Pyro/NumPyro), statistics.
- **No-gos:** **Computer vision / image-centric research** (no 3D reconstruction, no
  pose/scene/graphics, no vision-perception labs); **hardware / embedded / robotics** setup.

**Query variables extracted (search-strategy §1):**
- `{TOPIC_DE}` = "Kausalität", "kausales Repräsentationslernen", "probabilistisches maschinelles Lernen";
  `{TOPIC_EN}` = "causality / causal representation learning", "probabilistic ML / Bayesian inference"
- `{METHOD_DE}` = "probabilistische Modellierung / Bayes'sche Inferenz"; `{METHOD_EN}` = "probabilistic modelling / Bayesian inference"
- `{DOMAIN}` = none fixed (general methodology)
- `{NOGO_TERM}` = "Computer Vision / Bildverarbeitung / 3D-Rekonstruktion", "Robotik / Hardware / Embedded"

## Route (search-strategy §2)

Primary: Science → FB Informatik. Required Pass-1 legs for AI/ML: MPI for Intelligent
Systems (`is.mpg.de/departments`), ELLIS Tübingen / Cyber Valley. (Same route as Persona B —
route does **not** encode the no-go; that happens in Pass 2 filtering.)

## Pass 1 — backbone crawl (live, this run)

FB-Informatik `forschung.html` fetched live. The page now exposes **two** relevant
sections (fuller than the Task O run, which saw only "Maschinelles Lernen"):

**Maschinelles Lernen (18):** Bethge (Computational Neuroscience & ML), Michael Black
(Perceiving Systems), Butz (Kognitive Modellierung), Eivazi (Autonomous Systems), Gehler
(ML Engineering & Tech Transfer), Geiger (Autonomes maschinelles Sehen / Autonomous Vision),
Hardt (Social Foundations of Computation), Hein (Maschinelles Lernen), Hennig (Methoden des ML),
Krenn (ML in der Wissenschaft II), von Luxburg (Theorie des ML), Macke (ML in der Wissenschaft),
Martius (Distributed Intelligence), Oh (Scalable Trustworthy AI), Pons-Moll (Kontinuierliches
Lernen auf multimodalen Datenströmen), Schölkopf (Empirical Inference), Williamson (Foundations
of ML Systems), Zell (Kognitive Systeme).

**Vision & Cognition (7):** Berens (Data Science for Vision Research), Giese (Computational
Sensomotorics), Henze (Medieninformatik), Lensch (Computergrafik), Kühne (Multimodal Learning),
Zhaoping Li (Sensory and Sensorimotor Systems), Wichmann (Neuronale Informationsverarbeitung).

MPI-IS `is.mpg.de/departments` bot-blocked again (fourth run) → per-name web-search fallback.

## Relevance & no-go filtering for Persona A (search-strategy §5 + §7)

**Topical-justification filter (§5):** include only chairs whose *own* stated research
matches causality / probabilistic ML.

**No-go exclusion (§7 + general no-go rule):** Persona A's "computer vision" no-go is **not a
codified row in §7** (§7 lists hardware, pure proofs, clinical, large SE, teaching), so it is
applied via the general no-go rule + §5. The whole Vision & Cognition section and the vision
chairs in the ML section are excluded on this basis:

- **Excluded — computer vision no-go:** Geiger (Autonomous Vision, 3D scene understanding,
  CVPR 2024 best paper — live-confirmed), Michael Black (Perceiving Systems, SMPL 3D body,
  live-confirmed), Pons-Moll (3D humans/clothing, ICCV/SIGGRAPH-Asia 2025 — live-confirmed),
  Kühne (Multimodal Learning — vision+language+video; more multimodal than pure CV but
  image-centric enough to trip A's no-go and, separately, not a causality/probabilistic topical
  match), Berens (vision-research data science), Lensch (Computergrafik), Zhaoping Li (visual
  sensory systems), Giese/Wichmann (perception/psychophysics).
- **Excluded — hardware/robotics no-go:** Zell (Kognitive Systeme — embedded/FPGA/robotics,
  primary methodology), Eivazi (Autonomous Systems — robotics).
- **Excluded — topical justification / thesis-fit (not a no-go):** Butz (cognitive-science
  predictive-processing models of human cognition — uses probabilistic models but domain is
  human cognition, not ML methodology — same domain-mismatch as the §5 worked example),
  Gehler (technology-transfer/engineering, not a research thesis), Krenn (AI-for-physics,
  domain-specific), Hardt (algorithmic fairness / social-ML theory — domain mismatch to
  causality/probabilistic methods).
- **Excluded — affiliation (2f):** Oh (STAI) relocated to KAIST Feb 2026 (live-confirmed,
  same as prior runs); flagged, not silently dropped (see below).

## Option Map (grouped by interest dimension)

### Causality & causal representation learning

**1. Empirical Inference — Prof. Dr. Bernhard Schölkopf** (MPI-IS / ELLIS Institute Tübingen —
[is.mpg.de/ei](https://is.mpg.de/ei), confirmed via search; direct MPI-IS fetch bot-blocked)
- Relevance: **core match** — causal representation learning, kernel methods, causal inference
  for out-of-distribution generalization. "Toward Causal Representation Learning" is the
  defining reference of this exact interest (live-confirmed 2024–2025 activity).
- Pros/difficulties: extremely high-profile, very competitive; a director-led department, so
  day-to-day supervision is usually via a senior postdoc.
- Conversation starter: causal representation learning for OOD generalization — a
  simulation-only, code-first thesis variant (respects the CV / hardware no-gos).

**2. Robust Machine Learning — Prof. Dr. Wieland Brendel** (MPI-IS / ELLIS Institute Tübingen —
confirmed via search)
- Relevance: causal structure learning + self-supervised representation learning. Causal angle
  fits directly; robustness work is model-analysis, not image-perception.
- ⚠ note: some robustness work is evaluated on image benchmarks; confirm the specific thesis
  topic is method/analysis-oriented, not a CV-perception project (would trip A's CV no-go).

### Probabilistic methods (Bayesian inference / probabilistic numerics)

**3. Methoden des maschinellen Lernens — Prof. Dr. Philipp Hennig**
([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: **core match** — probabilistic numerics, Bayesian inference, uncertainty
  quantification (live-confirmed: co-editor of the 2025 Probabilistic Numerics conference,
  ELLIS program co-director). This is the single most on-profile chair for Persona A.
- Pros/difficulties: strong methods group with a code-first culture (probabilistic-numerics
  libraries) — matches the "methods tied to working code" style well.
- Conversation starter: probabilistic ODE/linear-algebra solvers with calibrated uncertainty —
  a concrete methods-development thesis.

**4. Maschinelles Lernen in der Wissenschaft — Prof. Dr. Jakob Macke**
- Relevance: **strong methods match** — simulation-based (Bayesian) inference, neural posterior
  estimation, `sbi` toolkit (live-confirmed: FNOPE NeurIPS 2025, tabular-foundation-model SBI
  2025). The domain framing is computational neuroscience/biophysics, but the *methods* (SBI,
  probabilistic inference) are exactly Persona A's interest and the group ships open-source code.
- ⚠ borderline on domain (application is scientific simulators, not general ML), kept because
  the probabilistic-inference methods overlap is the dominant fit.
- Conversation starter: sample-efficient simulation-based inference as a general ML method,
  benchmarked outside neuroscience simulators.

### ML theory / statistical foundations (probabilistic-leaning)

**5. Theorie des maschinellen Lernens — Prof. Dr. Ulrike von Luxburg**
- Relevance: theory of ML, statistical guarantees, clustering, explainability (live-confirmed
  AISTATS/NeurIPS 2025). Probabilistic/statistical foundations fit Persona A's methods axis.
- ⚠ possible conflict with no-go: **none** — A's no-go is CV+hardware, *not* proofs, and von
  Luxburg's group pairs theory with empirical evaluation (clustering/explanation experiments),
  so it is not proof-only. Included cleanly.
- Conversation starter: statistical guarantees for a causal-discovery or clustering method with
  an empirical evaluation component.

### Deep learning & optimization (empirical, method-oriented)

**6. Maschinelles Lernen — Prof. Dr. Matthias Hein**
- Relevance: adversarial robustness, optimization, provable robustness — empirical deep-learning
  methods. Fits A's "methods tied to code/experiments" style; the robustness angle is
  method/optimization, not image-perception per se.
- ⚠ note: robustness is often benchmarked on image data; steer the thesis toward the
  optimization/guarantee side to respect the CV no-go.

**7. Distributed Intelligence — Prof. Dr. Georg Martius**
- Relevance: model-based reinforcement learning, representation learning for control.
  Representation-learning + probabilistic-model angle is a partial fit.
- ⚠ possible conflict with no-go (ambiguous, kept per §7): ERC-funded work targets "versatile
  robots" — confirm a **simulation-only** thesis topic so it doesn't cross into the hardware
  no-go. Ranked below the pure-methods chairs for that reason.

### Excluded but surfaced honestly (per SKILL.md "do not silently drop")

> ⚠ **Scalable Trustworthy AI — Prof. Dr. Seong Joon Oh — affiliation not confirmed current.**
> Trustworthy AI / uncertainty would have been an on-profile match for Persona A, but Oh
> relocated to KAIST (Feb 2026, live-confirmed). Not a current Tübingen option. Do not contact.

> **Foundations of ML Systems — Prof. Dr. Robert C. Williamson:** statistical foundations /
> f-divergences / fairness theory. Borderline for Persona A — the statistical-foundations angle
> is adjacent to "probabilistic methods," but the group's own focus (aggregation/fairness theory)
> doesn't intersect the stated causality/Bayesian-methods interests closely enough to rank as an
> option. Excluded via §5 topical justification, same verdict as the Task O run.

> **Coverage caveat:** This map covers publicly visible chairs as of 2026-07-02. Chairs with a
> weak web presence may be missing. To catch them: visit the FB Informatik research page and the
> MPI-IS / ELLIS Tübingen / Cyber Valley pages directly, ask the Fachschaft, and check the
> official Vorlesungsverzeichnis. MPI-IS's department listing was bot-blocked this run — MPI-IS
> coverage relies on per-person web search, a narrower net than a direct crawl.
