# CS — Skill Arm (live)

**Date:** 2026-07-02 · **Faculty:** Science → FB Informatik (+ MPI-IS / ELLIS / Cyber Valley) ·
**Arm:** SKILL · **Role:** Roadmap-J live-eval runbook first exercise (recall + precision)

## Persona (6 dimensions — reused from Task I-fix for comparability)

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

- **FB Informatik** `forschung.html` → fetched live. "Maschinelles Lernen" section lists
  11 groups (broader than the 2026-06-28 run's list — likely a page update): Bethge,
  Butz, Geiger, Hein, Hennig, Macke, Martius, von Luxburg, Oh, Williamson, Zell.
- **MPI-IS** `is.mpg.de/departments` → **bot-detection block again** (same known gap as
  Task I-fix). Fell back to targeted web search per that precedent.
- **Cyber Valley** `cyber-valley.de/research-groups` → **404** this run (URL likely
  drifted; `cyber-valley.de/en/research/groups` also 404'd). Fell back to web search
  for Schölkopf and Brendel individually — both confirmed active at MPI-IS/ELLIS
  Tübingen via search.

## Option Map (grouped by interest dimension)

### Causality & empirical inference

**1. Empirical Inference — Prof. Dr. Bernhard Schölkopf** (MPI-IS / ELLIS Institute Tübingen —
[is.mpg.de/ei](https://is.mpg.de/ei), confirmed via search since direct fetch was bot-blocked)
- Relevance: core match — causality, kernel methods, representation learning.
- Pros/difficulties: very high-profile group, extremely competitive; also honorary
  professor status (MPI primary appointment) — confirm current thesis-supervision
  capacity directly.
- Dated evidence: elected to UN AI Scientific Panel (Feb 2026), Fellow of the Royal
  Society (2026) — both confirm active 2026 status.
- Conversation starter: causal representation learning for out-of-distribution
  generalization.

### Reinforcement learning / autonomous systems

**2. Distributed Intelligence — Prof. Dr. Georg Martius** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: model-based reinforcement learning, representation learning for control.
- ⚠ **Possible no-go conflict:** ERC-funded work ("REAL-RL") targets "versatile robots" —
  thesis projects may include hardware-in-the-loop robot experiments. Primary
  methodology is ML/RL (software), not embedded systems engineering, but confirm the
  specific thesis topic doesn't cross into the hardware no-go.
- Conversation starter: model-based RL for sample-efficient robot skill learning
  (simulation-only variant, to sidestep the hardware no-go).

### Deep learning & representation learning

**3. Maschinelles Lernen — Prof. Dr. Matthias Hein** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: core ML — robustness, adversarial examples, optimization.
- Dated evidence: active "Theses/Vacant Positions" page confirmed live this run
  ([link](https://uni-tuebingen.de/en/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/maschinelles-lernen/thesesvacant-positions/)).
- Conversation starter: certified robustness of deep classifiers.

**4. Theorie des maschinellen Lernens — Prof. Dr. Ulrike von Luxburg** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: ML theory, clustering, graph-based learning.
- ⚠ Leans theory-heavy — confirm the specific project has an empirical component to
  avoid the "pure math proofs" no-go.
- Conversation starter: empirical evaluation of clustering/embedding methods.

**5. Computational Neuroscience and Machine Learning — Prof. Dr. Matthias Bethge** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: representation learning, computational neuroscience + ML.
- Conversation starter: comparing DNN and biological representations.

**6. Robust Machine Learning — Prof. Dr. Wieland Brendel** (MPI-IS / ELLIS Institute
Tübingen — confirmed via search; direct MPI-IS page bot-blocked)
- Relevance: direct match — robustness, self-supervised/representation learning,
  causal structure learning (arxiv 2406.14302, 2504.13101).
- Dated evidence: active 2025 talk ("Robustness and Generalisation in the Era of
  Web-Scale Data") and 2025 preprints — confirmed current.
- Conversation starter: identifiability of self-supervised representations.

**7. Autonomes maschinelles Sehen (Autonomous Vision) — Prof. Dr.-Ing. Andreas Geiger** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: generative 3D scene representations, computer vision ∩ deep learning.
- ⚠ **Availability caveat (new this run):** Geiger is on a leave of absence; the group
  is **not currently hiring new PhD/postdoc positions**. BSc/MSc theses still appear to
  be offered on request (email with background + project ideas), but confirm before
  investing in outreach.
- Conversation starter: neural implicit 3D reconstruction.

### ML for science (borderline domain fit)

**8. Maschinelles Lernen in der Wissenschaft — Prof. Dr. Jakob Macke** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: methods overlap strongly (differentiable simulation, deep learning,
  simulation-based inference — arxiv/Nature Methods 2025), but the group's domain is
  computational neuroscience/biophysics, not general AI/ML research as stated in the
  profile. Borderline — plausible fit on methods, weaker on stated domain.
- Conversation starter: simulation-based inference for a non-bio scientific model
  (to keep the domain general).

### Probabilistic methods

**9. Methoden des maschinellen Lernens — Prof. Dr. Philipp Hennig** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: direct match — probabilistic numerics, Bayesian inference, uncertainty.
- Dated evidence: active "Bachelor & Master: available Thesis topics" page confirmed
  live this run ([link](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/methoden-des-maschinellen-lernens/stellen/bachelor-master-available-thesis-topics/)).
- Conversation starter: probabilistic numerics for uncertainty quantification in
  deep models.

### Surfaced but judged weak fit (kept per no-go/relevance rules, not silently dropped)

**10. Foundations of Machine Learning Systems — Prof. Dr. Robert C. Williamson** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: weak — his stated research (aggregation/fairness, f-divergences,
  selection-bias theory) is foundational statistical theory, not deep
  learning/causality/representation learning as the profile states. ⚠ possible
  conflict with the "pure math proofs" no-go — the work is foundational/theoretical
  rather than proof-only, so kept with a flag rather than excluded.

**11. Kognitive Modellierung — Prof. Martin Butz** ([uni-tuebingen.de](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html))
- Relevance: weak — computational cognitive science / predictive-processing models
  of cognition, not AI/ML research in the profile's stated sense. Surfaced only
  because the FB-Informatik "Maschinelles Lernen" section groups it alongside core
  ML chairs.

**12. Scalable Trustworthy AI (STAI) — Prof. Dr. Seong Joon Oh**
- Relevance on paper: strong (trustworthy AI, robustness, uncertainty — direct topic
  match). **⚠ New finding this run — group has relocated:** Oh moved the STAI group
  from Tübingen to KAIST in **February 2026**. The FB-Informatik listing (crawled
  live today) still shows the group under Tübingen with no relocation notice — this
  is a **stale-backbone / silent-gap case**, not a topic mismatch. Flagged
  `⚠ PI relocated — not a current Tübingen thesis option`, ranked last, and **excluded
  from the precision-relevant count** below (it is topically relevant but no longer
  actually available, which is a distinct failure mode worth tracking separately).

### Excluded by no-go (not included in the map)

- **Kognitive Systeme — Prof. Dr. Andreas Zell:** excluded. Confirmed via search:
  operates 3 robotics labs, FPGA-based stereo-vision project, embedded-systems focus —
  hardware/embedded is the primary methodology for multiple active projects. This is a
  clear (non-ambiguous) match for the student's hardware/embedded no-go, so it is
  dropped per Step 7 rather than kept-with-flag.

> **Coverage caveat:** This map covers publicly visible chairs as of 2026-07-02.
> Chairs with a weak web presence may be missing. To catch them: visit the FB
> Informatik research page and the MPI-IS / ELLIS Tübingen / Cyber Valley pages
> directly, ask the Fachschaft, and check the official Vorlesungsverzeichnis. Note:
> the MPI-IS department listing and the Cyber Valley research-groups page both
> failed to load live during this run (bot-block / 404) — MPI-IS/ELLIS coverage here
> relies on targeted web search per person, which is a narrower net than a direct
> crawl would give.
