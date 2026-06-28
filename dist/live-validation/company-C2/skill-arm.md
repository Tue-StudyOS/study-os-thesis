# Skill Arm — find-company-thesis-options — Profile C2 (Medtech / Health)

**Run date:** 2026-06-28
**Skill:** find-company-thesis-options (SKILL.md, Task 2-C)
**Protocol:** No-peeking — written before opening company_seed/ ground truth

---

## Step 1 — Profile verification

All 6 dimensions present. Proceeding.

**Profile C2:**
- **Interests:** Medical imaging, biosensors, point-of-care diagnostics
- **Methods:** Signal processing, image processing, hardware-software co-design, lab experimentation, prototype validation
- **Domain:** Healthcare, medical devices, diagnostics
- **Thesis style:** Engineering / empirical — working prototype or validated algorithm as deliverable
- **Skills:** Python, MATLAB, image processing (OpenCV / ITK), signal analysis, some hardware experience
- **No-gos:** Pure clinical patient-contact work without engineering component; pharmaceutical synthesis; purely theoretical thesis without implementation; management/business focus

---

## Step 2 — Query variables extracted

| Variable | Value |
|---|---|
| `{TOPIC_EN}` | "medical imaging" OR "biosensors" OR "point-of-care diagnostics" |
| `{TOPIC_DE}` | "medizinische Bildgebung" OR "Biosensor" OR "Point-of-Care Diagnostik" |
| `{METHOD_EN}` | "signal processing" OR "image processing" OR "prototype" |
| `{DOMAIN_EN}` | "healthcare" OR "medical devices" OR "diagnostics" |
| `{DOMAIN_DE}` | "Medizintechnik" OR "Diagnostik" OR "Medizinprodukte" |
| `{NOGO_TERM}` | pharma synthesis / Arzneimittelentwicklung / clinical patient-only |
| Size preference | both SME and corporate acceptable; strong industry supervision preferred |

---

## Step 3 — Pass 1: Backbone filter (no web search)

**Backbone sections scanned:**
- §4 Medtech / Life Sciences — all entries: sector tags `[medtech]`, `[optics, medtech]`, `[pharma, medtech]`, `[medtech, imaging]`, `[IoT, sensors]`
- §1 AI / ML — entries tagged `[AI/ML, medtech]` or `[robotics, medtech]`
- §3 Industrial — entries with `[medical]` co-tag: Wittenstein AG

**Included entries after filter:**

| Company | Sector tags | Size | City |
|---|---|---|---|
| Carl Zeiss AG | optics, medtech | corporate | Oberkochen |
| Karl Storz GmbH & Co. KG | medtech | corporate | Tuttlingen |
| Paul Hartmann AG | medtech | corporate | Heidenheim |
| Roche Diagnostics GmbH | pharma, medtech | corporate | Mannheim |
| Heidelberg Engineering GmbH | medtech, imaging | SME | Heidelberg |
| Bosch Sensortec GmbH | IoT, sensors | SME | Reutlingen |
| eye2you GmbH | AI/ML, medtech | startup | Tübingen |
| Medicalvalues GmbH | AI/ML, medtech | startup | Stuttgart |
| NODE Robotics GmbH | robotics, medtech | startup | Stuttgart |
| DeepCare GmbH | AI/ML, medtech | startup | BW |
| Cytolytics GmbH | AI/ML, medtech | startup | Tübingen |
| Wittenstein AG | industrial, medical | SME | Igersheim |

**No-go check at filter stage:**
- Roche Diagnostics `[pharma, medtech]`: pharma tag triggers no-go flag review. Profile no-go is "pharmaceutical synthesis", NOT diagnostics/medical devices. Roche Diagnostics division focus is diagnostics engineering — keep, annotate.
- Wittenstein AG `[industrial, medical]`: medical is a secondary tag; primary is industrial/drive-technology — de-prioritize, keep for annotation.

**Candidate set: 12 entries → trim to ~8 best-matched for enrichment.** Removing Wittenstein (weak medtech match) and DeepCare (very small startup, unclear activity). Keeping: Carl Zeiss, Karl Storz, Paul Hartmann, Roche Diagnostics, Heidelberg Engineering, Bosch Sensortec, eye2you, NODE Robotics.

---

## Step 4 — Pass 2: Live enrichment

### Carl Zeiss AG
**2a — R&D focus:** Zeiss Meditec division (ophthalmology, surgical microscopy, OCT imaging) is the primary medtech arm. Hardware development, reliability engineering, medical optics — active Masterarbeit listings in Oberkochen (hardware development, reliability). Zeiss Research & Quality Technology division also covers imaging systems. Source: zeissgroup.wd3.myworkdayjobs.com (active 2025 listings); TUM collaboration on ML + physical modeling for Zeiss AG (2024).
**2b — Thesis signal:** `explicit opening` — Workday portal active with Masterarbeit listings at Oberkochen; confirmed topics include hardware development and reliability in medical context.
**2c — Contact path:** https://zeissgroup.wd3.myworkdayjobs.com/External — filter by "Masterarbeit"
**2d — Recency:** Active listings confirmed via Workday portal (2025 dates visible in search snippets).

### Karl Storz GmbH & Co. KG
**2a — R&D focus:** Global leader in minimally invasive surgery endoscopes; acquired Asensus Surgical (robotic surgery platform) in August 2024 — now actively expanding into robotics and AI-assisted surgery. AI for 3D organ modeling from MRI/CT, robotic endoscopy R&D. Source: karlstorz.com news (2024), career.karlstorz.com.
**2b — Thesis signal:** `explicit opening` — dedicated Masterarbeiten page with 3 current listings (Core Technology R&D, Robotic Systems, general initiativ option). All in Tuttlingen.
**2c — Contact path:** https://career.karlstorz.com/go/Bachelor-Masterarbeiten/9154101/
**2d — Recency:** 3 current listings confirmed as of 2026-06-28 backbone verification.

### Roche Diagnostics GmbH
**2a — R&D focus:** Third-largest Roche site globally (12,000+ employees in Mannheim). Point-of-care diagnostics, biosensor development, immunoassay engineering, molecular diagnostics. Active R&D focus on smartphone-based test strip evaluation, sensor technology, data analysis for POC systems. Source: roche.com/stories/science-and-the-city-mannheim (2025); wizbii.com (Roche Master-Thesis POC Diagnostics listing); roche.com/innovation/structure/rnd-locations/diagnostics-mannheim.
**2b — Thesis signal:** `active program` — roche.com/de/careers "Abschlussarbeiten" section active. Historical listings: "Master-Thesis in der Point-of-Care Diagnostik," "Masterarbeit mit Schwerpunkt Sensortechnologie." Active program confirmed.
**2c — Contact path:** https://www.roche.com/de/careers/country/germany/de_your_job/graduates/final_papers.htm
**2d — Recency:** Roche Diagnostics Day 2025 confirmed (diagnostics-day-20-05-2025.pdf); innovation center Mannheim active.

**No-go note:** Roche has a pharma tag in backbone. This entry is for Roche Diagnostics GmbH, not pharma synthesis R&D. Thesis topics are in diagnostic device development, signal processing, biosensors — consistent with profile. Flag: `confirm thesis topic is in diagnostics engineering (not pharmaceutical synthesis) before applying`.

### Paul Hartmann AG
**2a — R&D focus:** Medical wound care and infection management; R&D in wound healing (advanced dressings, proteomics of healing), incontinence and infection management products. €91.9M R&D spend (2023), 10,000+ employees. Publication record on ResearchGate. Source: medicaldesignandoutsourcing.com (2024 Medtech Big 100); hartmann.info news.
**2b — Thesis signal:** `active program` — careers.hartmann.info/go/Graduates-and-Students/4570501/ confirms thesis opportunity for Bachelor's and Master's students. No specific open listing found at time of enrichment.
**2c — Contact path:** https://careers.hartmann.info/go/Graduates-and-Students/4570501/ — search for Abschlussarbeit or contact directly.
**2d — Recency:** Company active in 2025 (acquisition of Safran Coating for advanced wound care confirmed 2024). R&D page live.

**Fit note:** Wound care and infection management R&D has some engineering overlap (testing devices, material engineering, sensor-based wound monitoring) but is less directly aligned with medical imaging/biosensor interests. Proactive inquiry needed to identify an imaging- or sensor-focused subproject.

### Heidelberg Engineering GmbH
**2a — R&D focus:** Medical imaging systems for ophthalmology (high-resolution OCT, HRA, fundus imaging). This is a direct match for medical imaging interests. Heidelberg (BW).
**2b — Thesis signal:** `unclear` — no Masterarbeit listing found at heidelbergengineering.com/de/karriere/. No live enrichment result confirmed a thesis program. SME (~400 employees); direct outreach to R&D team recommended.
**2c — Contact path:** https://www.heidelbergengineering.com/de/karriere/ — no structured portal; direct inquiry.
**2d — Recency:** Company active; fundus imaging products updated regularly. No publication trail found for 2024–2025 in enrichment run.

### Bosch Sensortec GmbH
**2a — R&D focus:** MEMS sensor development in Reutlingen — accelerometers (BMA530, BMA580 launched Jan 2024), gyroscopes, environmental sensors; applications in wearables, hearables, and health monitoring. Medical-adjacent (wearable health sensors). Bosch Sensortec is an independent subsidiary of the Bosch Group.
**2b — Thesis signal:** `active program` (inferred from Bosch Group) — Bosch Sensortec career page confirms: "opportunities … as a working student, or while completing your final thesis." Source: bosch-sensortec.com (brochure + careers page). Bosch parent runs Germany's largest industrial thesis program.
**2c — Contact path:** https://www.bosch-sensortec.com/career/ — no dedicated thesis portal; apply through Sensortec careers or via parent's portal (jobs.bosch.de, filter by "Reutlingen").
**2d — Recency:** BMA530/580 launched January 2024 confirms active MEMS R&D.

**Fit note:** MEMS sensors for health/wearables align with biosensor interest. The "medical" overlap is indirect (consumer/wearable health, not clinical diagnostics); flag for student to confirm R&D aligns with their specific interest in clinical or near-clinical biosensors.

### eye2you GmbH
**2a — R&D focus:** AI-based diabetic retinopathy screening using fundus images; medical image analysis for ophthalmology; direct intersection of medical imaging + AI. Based in Tübingen (University of Tübingen spin-off / Cyber Valley ecosystem). Source: Cyber Valley member profile; eye2you.org.
**2b — Thesis signal:** `unclear` — no Masterarbeit listing found at eye2you.org. Small startup. Given academic origins (Tübingen), thesis collaboration culture likely but unconfirmed. Proactive outreach to founders recommended.
**2c — Contact path:** https://www.eye2you.org — no careers page found; use contact page for inquiry.
**2d — Recency:** Active Cyber Valley member; academic spin-off with continuing research presence.

### NODE Robotics GmbH
**2a — R&D focus:** Medical robotics for minimally invasive procedures; surgical robotics; robotics + medtech intersection in Stuttgart. Source: node-robotics.com (careers).
**2b — Thesis signal:** `unclear` — no Masterarbeit listing found. Small startup in Stuttgart. Direct outreach to research team recommended.
**2c — Contact path:** https://www.node-robotics.com/careers — no structured portal.
**2d — Recency:** Backbone entry from 2026-06-28; company existence confirmed. No recent publications found.

---

## Step 5 — Quality filters

- Carl Zeiss, Karl Storz, Roche, Hartmann: official career pages used. ✓
- Heidelberg Engineering, Bosch Sensortec, eye2you, NODE: company own domains. ✓
- No job-board aggregator used as thesis source. ✓
- All recency evidence from 2024–2026. ✓

---

## Step 6 — No-go check

- Paul Hartmann: wound care R&D — borderline for "medical imaging/biosensor" profile. Kept with annotation to verify subproject alignment.
- Roche Diagnostics: pharma tag triggers no-go flag review — keep as diagnostics engineering (not pharma synthesis); annotated.
- All others: clear of no-go violations.

---

## Step 7 — Option map

---

> **Coverage caveat:** This map covers BW companies that publicly indicate R&D activity in your areas, based on a curated backbone (as of 2026-06-28) and live web enrichment. Most companies do NOT publicize open Masterarbeit positions — a 'thesis signal: unclear' does not mean there is no opening. For all entries marked 'unclear', proactive outreach (careers portal or direct R&D contact) is the recommended next step. The backbone is necessarily incomplete; new startups and divisions not yet in the list are a known gap.

---

### Group A — Medical Imaging / Optical Diagnostics

---

**Carl Zeiss AG — Zeiss Meditec**
- Sector tags: `[optics, medtech]` | Size: corporate | Location: Oberkochen (BW)
- **Relevance rationale:** Zeiss Meditec is one of the world's leading medical imaging companies (OCT, surgical microscopes, ophthalmic imaging). Direct match to "medical imaging" interest dimension.
- **Research focus (live):** Medical hardware development, reliability engineering for imaging systems, optical coherence tomography; active collaboration with TUM on ML + physical modeling for Zeiss components (2024). Workday portal shows active Masterarbeit listings including hardware development in Oberkochen.
- **Thesis signal:** `explicit opening` — active Masterarbeit listings on zeissgroup.wd3.myworkdayjobs.com/External (2025 dates).
- **Pros & likely difficulties:** World-class optics + medical imaging environment; structured program; excellent for optical engineering + imaging methods. Corporate pace; apply via Workday portal.
- **Contact path:** https://zeissgroup.wd3.myworkdayjobs.com/External — search "Masterarbeit"
- **Thesis coordinator / contact:** not confirmed publicly — apply via Workday portal; supervisor assigned to topic.

---

**Heidelberg Engineering GmbH — Ophthalmic Imaging**
- Sector tags: `[medtech, imaging]` | Size: SME | Location: Heidelberg (BW)
- **Relevance rationale:** High-resolution ophthalmic imaging systems (HRA, OCT, confocal scanning laser ophthalmoscopy) — one of the most direct matches to "medical imaging" in the backbone.
- **Research focus (live):** Fundus imaging; OCT for ophthalmology; diagnostic imaging devices. Products actively updated (product line confirmed current). No thesis-specific page found.
- **Thesis signal:** `unclear` — no Masterarbeit listing found. Direct outreach recommended; SME size suggests direct R&D team contact is most effective.
- **Pros & likely difficulties:** Highly specialized imaging domain; close contact with technical team likely in an SME; excellent thesis topic for imaging algorithms. No structured thesis portal; thesis opportunity depends on live R&D needs.
- **Contact path:** https://www.heidelbergengineering.com/de/karriere/ — use contact form for direct inquiry.
- **Thesis coordinator / contact:** not confirmed — direct inquiry to engineering team.

---

**eye2you GmbH — AI Medical Image Analysis**
- Sector tags: `[AI/ML, medtech]` | Size: startup | Location: Tübingen (BW)
- **Relevance rationale:** AI-based diabetic retinopathy screening from fundus images — direct intersection of medical imaging + ML interest. Tübingen location = proximity to university co-supervision opportunity.
- **Research focus (live):** Fundus image analysis for early diabetic retinopathy detection; DL for ophthalmology screening. University of Tübingen spin-off / Cyber Valley ecosystem.
- **Thesis signal:** `unclear` — no explicit listing found on eye2you.org. Academic spin-off background suggests thesis collaboration culture; confirm directly with founders.
- **Pros & likely difficulties:** Unique intersection of AI + medical imaging; proximity to Tübingen enables co-supervision. Very small team; thesis scope must align with active product pipeline; no structured program.
- **Contact path:** https://www.eye2you.org — contact page for inquiry.
- **Thesis coordinator / contact:** not confirmed — contact via website.

---

### Group B — Diagnostics / Biosensors

---

**Roche Diagnostics GmbH — Mannheim R&D**
- Sector tags: `[pharma, medtech]` | Size: corporate | Location: Mannheim (BW)
- **Relevance rationale:** Point-of-care diagnostics, biosensor development, immunoassay engineering, smartphone-based test strip evaluation — direct match to "biosensors" and "point-of-care diagnostics" interest dimensions.
- **Research focus (live):** POC diagnostics R&D; sensor technology for in-vitro diagnostics; data analysis for POC systems; molecular diagnostics. Mannheim is the primary Roche Diagnostics R&D hub (12,000+ employees). Source: roche.com/stories/science-and-the-city-mannheim (2025).
- **Thesis signal:** `active program` — roche.com/de/careers "Abschlussarbeiten" section active; confirmed thesis topics in POC diagnostics and sensor technology (wizbii.com mirrors of past listings).
- ⚠ **No-go flag:** Backbone tags include "pharma" — this entry is for Roche Diagnostics GmbH (diagnostic device engineering), NOT pharmaceutical synthesis R&D. Confirm thesis topic is in diagnostics / device engineering before applying.
- **Pros & likely difficulties:** World-class diagnostics R&D environment; access to state-of-the-art lab facilities. Large corporate; thesis topic must be confirmed in the diagnostics division (not pharma manufacturing). IP restrictions standard.
- **Contact path:** https://www.roche.com/de/careers/country/germany/de_your_job/graduates/final_papers.htm
- **Thesis coordinator / contact:** not confirmed — apply via careers page; supervisor matched to topic.

---

**Bosch Sensortec GmbH — MEMS / Health Sensors**
- Sector tags: `[IoT, sensors]` | Size: SME | Location: Reutlingen (BW)
- **Relevance rationale:** MEMS sensor R&D for wearables and health monitoring — relevant to "biosensors" interest dimension. All MEMS sensor manufacturing takes place in Reutlingen; R&D is at this site.
- **Research focus (live):** MEMS accelerometers (BMA530, BMA580 — smallest in world, Jan 2024), environmental sensors, health/wearable sensor applications. Source: bosch-sensortec.com/about-us/mems-expertise/ (2024).
- **Thesis signal:** `active program` (inferred) — Bosch Sensortec career page states opportunities "while completing your final thesis"; Bosch Group runs one of Germany's largest thesis programs.
- **Fit note:** Sensor applications are wearable/consumer health, not clinical diagnostics — relevant to biosensors interest but the clinical overlap is indirect. Verify R&D team's specific medical application focus before outreach.
- **Pros & likely difficulties:** State-of-the-art MEMS fabrication and characterization environment; strong Bosch Group infrastructure. Reutlingen is well-connected. Topic scope may lean toward consumer health (wearables) more than clinical diagnostics.
- **Contact path:** https://www.bosch-sensortec.com/career/ — or via jobs.bosch.de filtering by "Reutlingen"
- **Thesis coordinator / contact:** not confirmed — contact via careers page.

---

### Group C — Medtech Engineering / Surgical Systems

---

**Karl Storz GmbH & Co. KG — Robotic Surgery R&D**
- Sector tags: `[medtech]` | Size: corporate | Location: Tuttlingen (BW)
- **Relevance rationale:** World leader in minimally invasive endoscopy; acquired Asensus Surgical (Aug 2024) expanding into robotic surgery with AI-assisted navigation. Image processing for endoscopy and 3D organ modeling from CT/MRI data are active research areas.
- **Research focus (live):** AI for 3D organ modeling, robotic endoscopy, MIS instrumentation; recent Asensus Surgical acquisition directly adds AI-assisted robotic surgery R&D. Source: karlstorz.com news (2024).
- **Thesis signal:** `explicit opening` — career.karlstorz.com/go/Bachelor-Masterarbeiten/9154101/ shows 3 active listings: Core Technology R&D, Robotic Systems, general thesis initiativ application. All Tuttlingen.
- **Pros & likely difficulties:** Global leader in endoscopy with growing AI/robotics R&D (post-Asensus); active thesis program; Tuttlingen is the medtech capital of Germany. Strong domain expertise environment; Tuttlingen is a smaller city (possible relocation required). Family-owned company — direct contact culture.
- **Contact path:** https://career.karlstorz.com/go/Bachelor-Masterarbeiten/9154101/
- **Thesis coordinator / contact:** not confirmed — apply via careers page; initiativ listing accepts general thesis applications.

---

**Paul Hartmann AG — Wound Care / Medical Technology R&D**
- Sector tags: `[medtech]` | Size: corporate | Location: Heidenheim (BW)
- **Relevance rationale:** Medtech company with active wound care R&D (€91.9M R&D spend in 2023). Engineering thesis opportunity may be available in wound monitoring (sensor-based wound assessment), material testing, or process analysis.
- **Research focus (live):** Advanced wound care products; incontinence and infection management; proteomics-based wound healing research; acquisition of Safran Coating (2024) expands advanced wound care portfolio. Source: hartmann.info news (2024); medicaldesignandoutsourcing.com (Medtech Big 100, 2024).
- **Thesis signal:** `active program` — careers.hartmann.info/go/Graduates-and-Students/4570501/ explicitly mentions Bachelor's and Master's thesis opportunity for students.
- **Fit note:** Wound care R&D is less directly aligned with medical imaging / biosensors profile. Best fit if profile has flexibility to engineering or material aspects of wound monitoring. Recommend contacting Hartmann to identify a subproject with imaging or sensor measurement component.
- **Pros & likely difficulties:** Structured R&D program; Heidenheim BW location; access to real clinical applications. Wound care domain is niche — assess domain interest before applying.
- **Contact path:** https://careers.hartmann.info/go/Graduates-and-Students/4570501/ — search for Abschlussarbeit or contact HR.
- **Thesis coordinator / contact:** not confirmed — contact via careers page.

---

**NODE Robotics GmbH — Surgical Robotics**
- Sector tags: `[robotics, medtech]` | Size: startup | Location: Stuttgart (BW)
- **Relevance rationale:** Medical robotics for minimally invasive procedures — intersection of robotics and medical devices. Could overlap with surgical imaging if thesis involves visual guidance or image-based control.
- **Research focus (live):** Surgical robotics; medical robotics for MIS. Backbone entry confirmed.
- **Thesis signal:** `unclear` — no listing found on node-robotics.com/careers. Small startup; direct outreach required.
- **Pros & likely difficulties:** Cutting-edge surgical robotics space; close team contact. Very small; highly variable supervision; thesis scope must precisely match live product need.
- **Contact path:** https://www.node-robotics.com/careers — inquiry via contact form.
- **Thesis coordinator / contact:** not confirmed.

---

## Step 8 — Coverage caveat (restated)

> This map covers BW companies that publicly indicate R&D activity in your areas, based on the curated BW company backbone (2026-06-28) and live web enrichment. Most companies do NOT publicize open Masterarbeit positions — 'thesis signal: unclear' does not mean no opening exists. For all entries marked 'unclear', proactive outreach is recommended. Medical device companies often require NDA for thesis work. Note: Tuttlingen is Germany's "Medizintechnik Valley" — many SMEs in the Tuttlingen area not yet in the backbone may also offer thesis opportunities.

---

*Self-check: All 6 profile dimensions verified; Pass 1 backbone-read only; no web search at Step 3; contact names not invented; all thesis signals classified; recency from 2024–2026; coverage caveat present.*
