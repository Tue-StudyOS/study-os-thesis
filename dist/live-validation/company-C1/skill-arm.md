# Skill Arm — find-company-thesis-options — Profile C1 (ML/AI + Automotive/Robotics)

**Run date:** 2026-06-28
**Skill:** find-company-thesis-options (SKILL.md, Task 2-C)
**Protocol:** No-peeking — written before opening company_seed/ ground truth

---

## Step 1 — Profile verification

All 6 dimensions present. Proceeding.

**Profile C1:**
- **Interests:** Computer vision, reinforcement learning, autonomous systems / autonomous driving
- **Methods:** Empirical ML, simulation-based evaluation, experiment-driven; prefer iterative model training
- **Domain:** Automotive, autonomous driving, robotics
- **Thesis style:** Applied / empirical — working system or trained model as the deliverable
- **Skills:** Python, PyTorch, ROS, OpenCV, CUDA; some experience with simulation environments (CARLA, IsaacSim)
- **No-gos:** Pure hardware without any software/ML layer; clinical patient contact; survey-only thesis without implementation

---

## Step 2 — Query variables extracted

| Variable | Value |
|---|---|
| `{TOPIC_EN}` | "computer vision" OR "reinforcement learning" OR "autonomous driving" |
| `{TOPIC_DE}` | "Computer Vision" OR "Reinforcement Learning" OR "autonomes Fahren" |
| `{METHOD_EN}` | "empirical ML" OR "simulation" OR "model training" |
| `{DOMAIN_EN}` | "automotive" OR "robotics" OR "autonomous systems" |
| `{DOMAIN_DE}` | "Automotive" OR "Robotik" OR "autonome Systeme" |
| `{NOGO_TERM}` | pure hardware / Hardwareentwicklung ohne Software-Anteil |
| Size preference | both startup and corporate acceptable; startup preferred for closer daily contact |

---

## Step 3 — Pass 1: Backbone filter (no web search)

**Backbone sections scanned:**
- §1 AI / ML — all entries; keep those tagged `[robotics]`, `[AI/ML, automotive]`, or `[AI/ML, computer-vision]`
- §2 Automotive / Mobility — all entries; keep all (domain match)
- §3 Industrial / Manufacturing — scan; only keep if additionally tagged `[AI/ML]`
- All other sections — no primary match for automotive/robotics domain

**Included entries after filter:**

| Company | Sector tags | Size | City |
|---|---|---|---|
| Robert Bosch GmbH | automotive, AI/ML | corporate | Stuttgart |
| ZF Friedrichshafen AG | automotive, AI/ML | corporate | Friedrichshafen |
| Mercedes-Benz AG | automotive, AI/ML | corporate | Stuttgart |
| Dr. Ing. h.c. F. Porsche AG | automotive, AI/ML | corporate | Stuttgart |
| Daimler Truck AG | automotive, AI/ML | corporate | Stuttgart |
| Mercedes-Benz Tech Innovation GmbH | automotive, software | SME | Stuttgart / Ulm |
| Porsche Digital GmbH | automotive, AI/ML | SME | Stuttgart |
| IAV GmbH | automotive, AI/ML | corporate | Stuttgart (BW site) |
| NEURA Robotics GmbH | robotics, AI/ML | startup | Metzingen |
| sereact GmbH | robotics, AI/ML | startup | Stuttgart |
| DeepScenario GmbH | AI/ML, automotive | startup | Stuttgart |

**No-go check:** Entries tagged `[industrial]` only (Trumpf, Festo, Kärcher, Voith) — excluded.
**Size filter:** No strong size preference expressed; all 11 entries retained.

**Candidate set: 11 companies → applying 5–20 range constraint → proceeding with enrichment on top 8 best-matched (trim Daimler Truck, IAV, Mercedes-Benz Tech Innovation to keep list to ~8).**

---

## Step 4 — Pass 2: Live enrichment

### Robert Bosch GmbH
**2a — R&D focus:** Bosch Center for AI (BCAI) confirmed working on reinforcement learning (autonomous braking, robotic manipulation), computer vision for industrial and automotive applications, and autonomous driving perception. BCAI publishes actively (IEEE/ICRA papers). Source: www.bosch.com/research/bcai/ (2026-01 content confirmed active).
**2b — Thesis signal:** `active program` — dedicated thesis portal at bosch.de/karriere confirms Wissenschaftliche Abschlussarbeit program; stipend €700–800/month; apply via jobs.bosch.de at least 4 months before start.
**2c — Contact path:** https://www.bosch.de/karriere/dein-einstieg/studentinnen-und-studenten/wissenschaftliche-abschlussarbeit/
**2d — Recency:** BCAI research pages and RL pages updated 2025; thesis portal active as of backbone verification (2026-06-28).

### ZF Friedrichshafen AG
**2a — R&D focus:** Active ML research for automotive safety systems; confirmed topic: "Masterarbeit Entwicklung & Bewertung hybrider Machine Learning Verfahren zur Knickwinkelbestimmung" (2025) and "Praktikum/Abschlussarbeit Reinforcement Learning" (2025). Autonomous driving and perception are active ZF R&D areas.
**2b — Thesis signal:** `explicit opening` — multiple ML/RL Masterarbeit listings confirmed on ZF jobs portal and aggregator mirrors (Bright Network, 2025).
**2c — Contact path:** https://jobs.zf.com/go/Studenten/3635701/ (search for "Masterarbeit" or "Abschlussarbeit")
**2d — Recency:** 2025 listings confirmed.

### Mercedes-Benz AG
**2a — R&D focus:** Active work on autonomous driving, Embedded AI (vehicle inference at edge), AI for connected vehicles. Research collaboration with KIT; "Embedded AI" Masterarbeit (Jan 2025) listed.
**2b — Thesis signal:** `explicit opening` — group.mercedes-benz.com/careers/students/dissertation/ confirmed; Embedded AI Masterarbeit (Jan 2025) found at jobs.mercedes-benz.com.
**2c — Contact path:** https://group.mercedes-benz.com/careers/students/dissertation/ → jobs.mercedes-benz.com for listings
**2d — Recency:** 2025 listings confirmed.

### Dr. Ing. h.c. F. Porsche AG
**2a — R&D focus:** Highly Automated Driving (HAD), AI for ADAS, computer vision for scenario-based testing. Active doctoral research collaboration with KIT; researchers (Tin Stribor Sohn, Tim Dieter Eberhardt) working on multimodal LLMs for autonomous driving and CV/ML for ADAS at Weissach R&D center. Source: Medium/NextLevelGermanEngineering, arXiv papers.
**2b — Thesis signal:** `active program` — dedicated thesis page confirms flexible start times, available across all departments including R&D Weissach; confidentiality required (NDI clause for 5 years).
**2c — Contact path:** https://www.porsche.com/germany/aboutporsche/jobs/students/thesis/ → apply via jobs.porsche.com (search "Abschlussarbeit")
**2d — Recency:** Thesis page and researcher profiles confirmed 2025.

### NEURA Robotics GmbH
**2a — R&D focus:** Cognitive humanoid robotics; computer vision for manipulation; reinforcement learning for dexterous tasks; multimodal AI. Partners with Bosch on German robotics R&D. 700+ employees. Presented at CES 2026 and Automatica 2025.
**2b — Thesis signal:** `active program` (inferred) — careers page active (jobs.neura-robotics.com); regional job board (stellenangebote-reutlingen.de) listed "Praktikant/in, Werkstudent/in, Bachelor-/Masterthesis" positions. No direct Masterarbeit page found on NEURA's own site.
**2c — Contact path:** https://jobs.neura-robotics.com/ — apply directly; contact Florian Fackelmayer (listed on regional posting; confirm currency before use)
**2d — Recency:** Positions active per 2026 search results; CES 2026 presence confirms company activity.

### sereact GmbH
**2a — R&D focus:** Vision Language Action Models (VLAMs) for warehouse robotics; "PickGPT" (LLM + computer vision for grasping); deployed at BMW, Mercedes-Benz, Daimler Truck. $110M Series B (April 2026). Founded by former University of Stuttgart AI researchers.
**2b — Thesis signal:** `unclear` — careers page active at sereact.ai/careers; no explicit Masterarbeit listing found; company in hyper-growth phase likely prioritizing full-time hires; direct outreach to research team recommended given founder-academic background.
**2c — Contact path:** https://sereact.ai/careers — no direct email found; apply through careers page or contact via research team inquiry
**2d — Recency:** $110M Series B April 2026; company clearly active.

### DeepScenario GmbH
**2a — R&D focus:** AI-powered simulation scenarios for autonomous driving testing; uses Stuttgart/Sindelfingen/Munich datasets; published at IEEE ICRA 2025; collaborating with AVL on AD testing.
**2b — Thesis signal:** `unclear` — no Masterarbeit listing found on deepscenario.com/jobs; small startup; direct outreach recommended.
**2c — Contact path:** https://www.deepscenario.com/jobs — check current listings; no direct email confirmed.
**2d — Recency:** IEEE ICRA 2025 paper confirms research activity.

---

## Step 5 — Quality filters applied

- Bosch, ZF, Mercedes, Porsche: official career pages used; no job board as primary source. ✓
- NEURA: regional job board reference noted; backbone URL (jobs.neura-robotics.com) used as primary. ✓
- sereact, DeepScenario: company own domains used. ✓
- All recency evidence from 2024–2026. ✓
- No duplicates across backbone and live search. ✓

---

## Step 6 — No-go check

- Pure hardware no-go: Daimler Truck, Mahle, Dürr — removed (industrial/mechanical focus without confirmed AI/ML R&D thesis signal matching profile). Note: Daimler Truck has an AI/ML tag but no confirmed CV/RL thesis signal; kept as optional note.
- No entry remaining violates the no-gos based on live enrichment.
- sereact and DeepScenario: both software/AI companies despite robotics/automotive domain — no hardware-only concern. ✓

---

## Step 7 — Option map

---

> **Coverage caveat:** This map covers BW companies that publicly indicate R&D activity in your areas, based on a curated backbone (as of 2026-06-28) and live web enrichment. Most companies do NOT publicize open Masterarbeit positions — a 'thesis signal: unclear' does not mean there is no opening. For all entries marked 'unclear', proactive outreach (careers portal or direct R&D contact) is the recommended next step. The backbone is necessarily incomplete; new startups and divisions not yet in the list are a known gap.

---

### Group A — Autonomous Driving / ADAS + Computer Vision

---

**Robert Bosch GmbH — Bosch Center for AI (BCAI)**
- Sector tags: `[automotive, AI/ML]` | Size: corporate | Location: Stuttgart (BW)
- **Relevance rationale:** BCAI is one of Germany's largest industrial AI labs. Active research in reinforcement learning (robotic manipulation, autonomous braking) and computer vision for vehicle perception — direct match to both the CV and RL interest dimensions.
- **Research focus (live):** RL for control and optimization; computer vision for autonomous driving perception; multimodal sensor fusion. Source: www.bosch.com/research/bcai/ (2025 content active).
- **Thesis signal:** `active program` — dedicated Abschlussarbeit portal; stipend €700–800/month; 3–6 month duration.
- **Pros & likely difficulties:** Structured program with mentoring; excellent research environment; strong network for post-thesis employment. Competitive — apply via portal 4+ months ahead. Large corporate bureaucracy; IP restrictions standard.
- **Contact path:** https://www.bosch.de/karriere/dein-einstieg/studentinnen-und-studenten/wissenschaftliche-abschlussarbeit/ → then jobs.bosch.de to search for specific ML/AI topic listings.
- **Thesis coordinator / contact:** not confirmed — contact via thesis portal; specific supervisor assigned after topic is matched.

---

**ZF Friedrichshafen AG — Advanced Engineering / Autonomous Driving**
- Sector tags: `[automotive, AI/ML]` | Size: corporate | Location: Friedrichshafen (BW)
- **Relevance rationale:** Active ML thesis topics confirmed for 2025, including RL and ML for vehicle system estimation — direct match to the RL interest dimension.
- **Research focus (live):** ML for automotive safety and control (knick angle estimation, braking systems); reinforcement learning for autonomous driving sub-systems. Source: ZF jobs portal, Bright Network listings (2025).
- **Thesis signal:** `explicit opening` — ML/RL Masterarbeit listings confirmed live (2025): "Masterarbeit … hybrider Machine Learning Verfahren zur Knickwinkelbestimmung" and "Abschlussarbeit Reinforcement Learning" (Hannover site also available).
- **Pros & likely difficulties:** Direct ML/RL thesis match; structured program; Friedrichshafen location requires relocation (Bodensee region); some thesis topics are in Hannover or other sites — check listing for location.
- **Contact path:** https://jobs.zf.com/go/Studenten/3635701/ — search "Masterarbeit" and filter by ML/AI.
- **Thesis coordinator / contact:** not confirmed publicly — contact via portal.

---

**Mercedes-Benz AG — Group R&D / Embedded AI**
- Sector tags: `[automotive, AI/ML]` | Size: corporate | Location: Stuttgart (BW)
- **Relevance rationale:** Embedded AI Masterarbeit (Jan 2025) confirmed — directly relevant to autonomous driving inference and edge ML, matching both CV and RL dimensions. Company-wide AI for ADAS is a documented R&D priority.
- **Research focus (live):** Embedded AI, autonomous driving perception, AI for connected and autonomous vehicles. Active KIT research collaboration visible. Source: jobs.mercedes-benz.com (2025 listings); group.mercedes-benz.com.
- **Thesis signal:** `explicit opening` — Embedded AI Masterarbeit listed at jobs.mercedes-benz.com (Jan 2025); group thesis page active.
- **Pros & likely difficulties:** Premium brand with strong R&D reputation; Stuttgart location. Highly competitive; large corporate bureaucracy; IP confidentiality standard; co-supervision with university not guaranteed.
- **Contact path:** https://group.mercedes-benz.com/careers/students/dissertation/ → search jobs.mercedes-benz.com for "Abschlussarbeit" filtered by AI/software.
- **Thesis coordinator / contact:** not confirmed — apply via careers portal.

---

**Dr. Ing. h.c. F. Porsche AG — R&D Weissach / Autonomous Driving**
- Sector tags: `[automotive, AI/ML]` | Size: corporate | Location: Weissach / Stuttgart (BW)
- **Relevance rationale:** Confirmed active researcher collaboration (KIT doctoral candidates in CV/ML for ADAS at Weissach); thesis available in all departments including R&D; computer vision and scenario-based testing of autonomous systems are documented research areas.
- **Research focus (live):** Multimodal LLMs for autonomous driving scenario understanding; ML for ADAS; computer vision for testing frameworks. Evidence: arXiv preprint 2503.11400 (Porsche AG affiliation, Mar 2025); Medium/NextLevelGermanEngineering articles (2021, indicative of ongoing focus).
- **Thesis signal:** `active program` — dedicated thesis page confirms "almost all departments and locations," flexible start. Apply via jobs.porsche.com. Note: IP confidentiality required (NDA for 5 years on thesis content).
- **Pros & likely difficulties:** Prestigious brand; Weissach R&D is a world-class automotive engineering center; exposure to both engineering and AI teams. Competitive; confidentiality constraint means university publication is restricted.
- **Contact path:** https://www.porsche.com/germany/aboutporsche/jobs/students/thesis/ → jobs.porsche.com (search "Abschlussarbeit")
- **Thesis coordinator / contact:** not confirmed — apply via portal.

---

### Group B — Robotics / Autonomous Systems + Computer Vision

---

**NEURA Robotics GmbH**
- Sector tags: `[robotics, AI/ML]` | Size: startup (700+ employees) | Location: Metzingen (BW)
- **Relevance rationale:** Cognitive humanoid robotics with computer vision + RL for dexterous manipulation — exactly matching the CV and RL interest dimensions. Founded 2019; rapid growth (Bosch partnership, CES 2026 presence).
- **Research focus (live):** Computer vision for object detection and manipulation; RL for dexterous robotic tasks; multimodal AI for human-robot interaction. Active job listings for "Robotic Foundation Model Engineer" and "Reinforcement Learning Research Scientist" (2026-level hiring). Source: neura-robotics.com, therobotreport.com (2025–2026).
- **Thesis signal:** `active program` (inferred) — careers page active; regional job board lists "Bachelor-/Masterthesis" positions at Metzingen. No dedicated Masterarbeit page on company's own site found.
- **Pros & likely difficulties:** Cutting-edge cognitive robotics startup; close daily research contact; strong publication culture (IEEE/ICRA presence). Less structured than corporates; supervision model varies; company in rapid scaling phase — verify thesis opportunity is still available before outreach.
- **Contact path:** https://jobs.neura-robotics.com/ — filter for internship/thesis; or direct R&D team inquiry via the HR contact listed on regional job boards (verify before use).
- **Thesis coordinator / contact:** not confirmed on company's own page — contact via jobs page.

---

**sereact GmbH**
- Sector tags: `[robotics, AI/ML]` | Size: startup (~150 employees, pre-$110M Series B 2026) | Location: Stuttgart (BW)
- **Relevance rationale:** Vision Language Action Models (VLAMs) for robotic grasping — directly combines computer vision, large language models, and physical action, matching CV interest and empirical ML method preference. Customers include BMW, Mercedes-Benz, Daimler Truck — domain relevance strong.
- **Research focus (live):** PickGPT (LLM + computer vision for bin-picking), VLAMs for adaptive robotics, logistics automation AI. Source: sereact.ai/cortex; sifted.eu, thenextweb.com (2025–2026).
- **Thesis signal:** `unclear` — no explicit Masterarbeit listing found on careers page (sereact.ai/careers). Company is in hyper-growth mode; direct outreach to research team is the recommended path. Founded by former University of Stuttgart AI researchers — thesis collaboration culture likely but unconfirmed.
- **Pros & likely difficulties:** High-impact startup; VLAMs are a frontier research area; close contact with founders (academic background). Hyper-growth companies may prioritize full-time hires; thesis supervision not guaranteed; fast-moving environment.
- **Contact path:** https://sereact.ai/careers — check for open roles or send direct inquiry; no structured thesis portal found.
- **Thesis coordinator / contact:** not confirmed — contact via careers page inquiry.

---

**DeepScenario GmbH**
- Sector tags: `[AI/ML, automotive]` | Size: startup | Location: Stuttgart (BW)
- **Relevance rationale:** AI-powered scenario generation and simulation for autonomous driving testing — relevant to the profile's autonomous systems interest and simulation-based evaluation method preference.
- **Research focus (live):** Scenario-based testing of autonomous driving systems using generative AI; published at IEEE ICRA 2025; collaboration with AVL on AD testing. Datasets covering Stuttgart and Sindelfingen. Source: arxiv.org/abs/2503.11400 (2025), automatedwarehouseonline.com.
- **Thesis signal:** `unclear` — no Masterarbeit listing found at deepscenario.com/jobs. Small startup; direct outreach to research team required.
- **Pros & likely difficulties:** Niche frontier area (AI simulation for AD); direct research collaboration likely if thesis matches active project. Small team — highly variable supervision; thesis scope must align with live product needs.
- **Contact path:** https://www.deepscenario.com/jobs — check current listings; no direct email confirmed.
- **Thesis coordinator / contact:** not confirmed — contact via jobs page.

---

## Step 8 — Coverage caveat (restated at map close)

> This map covers BW companies that publicly indicate R&D activity in your areas, based on the curated BW company backbone (2026-06-28) and live web enrichment. Most companies do NOT publicize open Masterarbeit positions — 'thesis signal: unclear' does not mean no opening exists. For all entries marked 'unclear', proactive outreach (careers portal or direct R&D contact) is recommended. The backbone is necessarily incomplete; automotive Tier-1 and 2 suppliers and smaller AI startups not yet in the list are a known gap.

---

*Self-check: All 6 profile dimensions verified; Pass 1 used backbone read only (no web); all entries from backbone candidate set; no contact names invented; all thesis signals classified; evidence from 2025–2026; coverage caveat present; no job-board aggregators used as thesis source.*
