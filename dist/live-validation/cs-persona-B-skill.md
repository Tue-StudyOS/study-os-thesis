# CS — Persona B — Skill Arm (live)

**Date:** 2026-07-02 · **Faculty:** Science → FB Informatik (+ MPI-IS / ELLIS / Cyber Valley) ·
**Arm:** SKILL · **Role:** Roadmap Task P (steering proof) — persona B of the A/B divergence test.

> Task-P note: Persona B is a *different* student from Persona A. Same faculty and same Pass-1
> candidate set; **inverted no-gos** — B wants computer vision and excludes heavy
> Bayesian/probabilistic theory. The steering test is whether B's map diverges from A's in the
> predicted direction.

## Persona B (6 dimensions)

- **Interests:** Computer vision (3D scene/human understanding, generative visual models) &
  self-supervised **representation learning** across modalities (image / video / multimodal).
- **Methods:** Empirical deep learning — large-scale training, benchmark-driven evaluation, GPUs.
- **Domain:** Visual perception; some interest in vision-for-robotics *applications* (but not
  building hardware).
- **Thesis style:** Experimental/systems — train and evaluate models on visual data.
- **Skills:** Python, PyTorch, CUDA, 3D/vision libraries; large-model training experience.
- **No-gos:** **Heavy Bayesian / probabilistic theory** (no probabilistic numerics, no
  simulation-based inference, no proof-heavy statistical theory); **hardware / embedded /
  robotics** setup.

**Query variables extracted (search-strategy §1):**
- `{TOPIC_DE}` = "Computer Vision / Bildverarbeitung", "3D-Szenenverständnis", "Repräsentationslernen";
  `{TOPIC_EN}` = "computer vision / 3D scene understanding", "self-supervised representation learning"
- `{METHOD_DE}` = "tiefes Lernen / großskaliges Modelltraining"; `{METHOD_EN}` = "deep learning / large-scale training"
- `{DOMAIN}` = visual perception (vision)
- `{NOGO_TERM}` = "Bayes'sche Inferenz / probabilistische Numerik / simulationsbasierte Inferenz",
  "Robotik / Hardware / Embedded"

## Route (search-strategy §2)

Primary: Science → FB Informatik. Required Pass-1 legs for AI/ML: MPI for Intelligent Systems,
ELLIS Tübingen / Cyber Valley. **Identical route to Persona A** — routing does not encode the
interest/no-go split; Pass-2 filtering does.

## Pass 1 — backbone crawl (live, this run)

Same live crawl as Persona A (same faculty). FB-Informatik `forschung.html` exposes the
**Maschinelles Lernen (18)** and **Vision & Cognition (7)** sections listed in the Persona A
file. Same candidate set of 25 groups. MPI-IS `is.mpg.de/departments` bot-blocked → per-name
web-search fallback.

## Relevance & no-go filtering for Persona B (search-strategy §5 + §7)

**Topical-justification filter (§5):** include only chairs whose *own* stated research matches
computer vision / representation learning.

**No-go exclusion (§7 + general no-go rule):** Persona B's "heavy Bayesian / probabilistic theory"
no-go is **not a codified row in §7** either — applied via the general no-go rule + §5. This
inverts Persona A's exclusions:

- **Excluded — heavy-Bayesian / probabilistic-theory no-go:** Hennig (probabilistic numerics /
  Bayesian inference — live-confirmed, the exact thing B excludes), Macke (simulation-based
  *Bayesian* inference — live-confirmed), von Luxburg (statistical-theory-heavy; B wants
  empirical vision, not statistical guarantees), Schölkopf (causality / kernel methods —
  probabilistic-leaning *and* causality is not B's interest → excluded on topical justification
  as much as on the no-go), Williamson (statistical foundations — clear exclude).
- **Excluded — hardware/robotics no-go:** Zell (Kognitive Systeme), Eivazi (Autonomous Systems).
- **Excluded — topical justification / thesis-fit (not a no-go):** Butz (cognitive-science
  models of human cognition — not CV/representation research), Gehler (tech transfer, not a
  research thesis), Krenn (AI-for-physics), Hardt (fairness/social-ML theory — no vision),
  Henze (Medieninformatik/HCI — interaction, not vision-model research), Giese/Wichmann/Zhaoping
  Li (perception/psychophysics/sensory neuroscience — visual *science*, weak fit to CV
  *engineering*; Wichmann/Li flagged as adjacent rather than surfaced as primary options).
- **Excluded — affiliation (2f):** Oh (STAI) relocated to KAIST (live-confirmed); flagged below.

## Option Map (grouped by interest dimension)

### Computer vision — 3D scene & human understanding

**1. Autonomes maschinelles Sehen (Autonomous Vision) — Prof. Dr.-Ing. Andreas Geiger**
([uni-tuebingen.de](https://uni-tuebingen.de/en/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/autonomous-vision/home/))
- Relevance: **core match** — 3D scene understanding, reconstruction, generative 3D scene
  representations, vision for autonomous systems (live-confirmed: CVPR 2024 best paper,
  Longuet-Higgins Prize). Directly on Persona B's stated interest.
- ⚠ availability caveat: Geiger is on a leave of absence — not currently hiring PhD/postdoc
  positions; BSc/MSc theses still offered on request. Rank as a strong topical fit with a
  supervision-availability flag.
- Conversation starter: generative 3D scene representations / neural reconstruction — a
  training-and-evaluation thesis on public driving/scene datasets.

**2. Perceiving Systems — Prof. Michael J. Black** (MPI-IS / Honorarprofessor Tübingen —
[is.mpg.de/ps](https://is.mpg.de/ps), confirmed via search)
- Relevance: **core match** — 3D human body/pose (SMPL family), human–scene interaction, vision
  from images/video (live-confirmed: 2025 Everingham Prize, active 2025 publications).
- Pros/difficulties: very large, prestigious MPI department — competitive; day-to-day
  supervision via senior researchers.
- Conversation starter: human–object contact reconstruction from single images (a 2025 group
  theme) as an MSc-scale project.

**3. Real Virtual Humans / Kontinuierliches Lernen auf multimodalen Datenströmen —
Prof. Dr. Gerard Pons-Moll**
- Relevance: **core match** — 3D humans, clothing/garment reconstruction, vision ∩ graphics ∩ ML
  (live-confirmed: ICCV 2025, SIGGRAPH Asia 2025). Strong CV + representation-learning fit.
- Conversation starter: single-image garment/human reconstruction — extend a 2025 group method
  to a new benchmark.

### Representation learning (multimodal / self-supervised)

**4. Multimodal Learning — Prof. Dr. Hilde Kühne**
- Relevance: **core match** — self-supervised multimodal representation learning (vision +
  language + video), learning without labels (live-confirmed: ERC Starting Grant "GraViLa",
  ICCV 2025 General Chair, core faculty Tübingen AI Center since Aug 2024). Directly on Persona
  B's representation-learning interest, with a strong code/training culture.
- Conversation starter: self-supervised video representation learning without manual labels —
  a large-scale training thesis.

**5. Computational Neuroscience and Machine Learning — Prof. Dr. Matthias Bethge**
- Relevance: strong fit on the representation-learning axis — visual representation learning,
  alignment of neural-network vs. biological visual representations, vision-model benchmarking
  (live-confirmed: ICCV 2025 saliency-bias paper, Nature Machine Intelligence 2025 on visual
  cognition in multimodal LLMs). Director of the Tübingen AI Center.
- Conversation starter: benchmarking behavioral alignment of vision-model representations.

**6. Robust Machine Learning — Prof. Dr. Wieland Brendel** (MPI-IS / ELLIS Tübingen)
- Relevance: robustness and self-supervised representation learning, much of it evaluated on
  image benchmarks — fits the empirical-vision axis (representation learning + robustness).
- Conversation starter: robustness of self-supervised visual representations under distribution
  shift.

### Vision — imaging & data-driven (adjacent, kept with a fit note)

**7. Computergrafik — Prof. Dr.-Ing. Hendrik Lensch**
- Relevance: computer graphics ∩ computational imaging ∩ learning — adjacent to CV; a good fit
  if the thesis leans toward rendering/inverse-graphics + learning.
- ⚠ fit note: graphics-leaning rather than pure vision — confirm the specific topic is
  learning-based visual modelling, not a pure-rendering systems project.

**8. Data Science for Vision Research — Prof. Dr. Philipp Berens**
- Relevance: ML/data science for visual (retinal/ophthalmic) data — vision *data* + deep learning.
- ⚠ fit note: the "vision" here is visual-neuroscience/medical-imaging data, not natural-image
  CV; kept as an adjacent option for a student open to applied medical-vision data.

### Excluded but surfaced honestly (per SKILL.md "do not silently drop")

> ⚠ **Scalable Trustworthy AI — Prof. Dr. Seong Joon Oh — affiliation not confirmed current.**
> Robustness/representation work would partially fit Persona B, but Oh relocated to KAIST
> (Feb 2026, live-confirmed). Not a current Tübingen option. Do not contact.

> **Maschinelles Lernen — Prof. Dr. Matthias Hein:** adversarial robustness on image data is
> vision-adjacent, but the group's own center of gravity is optimization / provable robustness
> (theory-leaning), so for Persona B (empirical vision) it ranks below the CV/representation
> chairs. Kept as a secondary option only if the thesis is an empirical image-robustness project;
> otherwise its theory lean is a soft mismatch with B's methods.

> **Coverage caveat:** This map covers publicly visible chairs as of 2026-07-02. Chairs with a
> weak web presence may be missing. To catch them: visit the FB Informatik research page and the
> MPI-IS / ELLIS Tübingen / Cyber Valley pages directly, ask the Fachschaft, and check the
> official Vorlesungsverzeichnis. MPI-IS's department listing was bot-blocked this run — MPI-IS
> coverage relies on per-person web search, a narrower net than a direct crawl.
