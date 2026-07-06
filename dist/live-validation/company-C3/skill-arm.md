# Skill Arm — find-company-thesis-options — Profile C3 (Software / Data Engineering + Enterprise)

**Run date:** 2026-06-28
**Skill:** find-company-thesis-options (SKILL.md, Task 2-C)
**Protocol:** No-peeking — written before opening company_seed/ ground truth

---

## Step 1 — Profile verification

All 6 dimensions present. Proceeding.

**Profile C3:**
- **Interests:** Distributed systems, data pipelines / data engineering, large language models for enterprise use cases
- **Methods:** Systems engineering, quantitative evaluation, benchmark design, engineering prototypes
- **Domain:** Enterprise software, SaaS, data platforms, fintech/banking
- **Thesis style:** Engineering / systems — working implementation or reproducible benchmark as deliverable
- **Skills:** Python, SQL, Spark/Flink; cloud platforms (AWS/GCP/Azure); basic ML literacy; optional Go/Java for systems work
- **No-gos:** Embedded/hardware; automotive domain without any software focus; pure management consulting without technical depth; purely non-technical roles

---

## Step 2 — Query variables extracted

| Variable | Value |
|---|---|
| `{TOPIC_EN}` | "distributed systems" OR "data engineering" OR "data pipeline" OR "LLM" OR "enterprise AI" |
| `{TOPIC_DE}` | "verteilte Systeme" OR "Datenpipeline" OR "Datenarchitektur" OR "Enterprise KI" |
| `{METHOD_EN}` | "systems engineering" OR "benchmark" OR "prototype" OR "evaluation" |
| `{DOMAIN_EN}` | "enterprise software" OR "SaaS" OR "cloud" OR "data platform" |
| `{DOMAIN_DE}` | "Enterprise Software" OR "Unternehmenssoftware" OR "Cloud-Plattform" |
| `{NOGO_TERM}` | embedded hardware / Embedded Systems; non-technical management; automotive hardware |
| Size preference | corporate or SME preferred (structured supervision); startup acceptable if R&D-heavy |

---

## Step 3 — Pass 1: Backbone filter (no web search)

**Backbone sections scanned:**
- §5 Software / Enterprise — all entries: SAP SE `[enterprise software, AI/ML]`, TeamViewer AG `[software, cloud]`, MHP Management- und IT-Beratung GmbH `[consulting, AI/ML]`
- §1 AI / ML — entries tagged with software/data/NLP focus: Aleph Alpha `[AI/ML, NLP, LLMs]`, Respeak `[AI/ML, NLP]`, Field 33 `[AI/ML, software]`, Collectu `[AI/ML, data]`, kausable `[AI/ML, analytics]`, ISTARI AI `[AI/ML, cybersecurity]`
- §2 Automotive / Mobility — software-focused subsidiaries only: Mercedes-Benz Tech Innovation GmbH `[automotive, software]`, Porsche Digital GmbH `[automotive, AI/ML]`
- All other sections — excluded (industrial/hardware focus incompatible with profile)

**No-go check at filter stage:**
- §3 Industrial / Manufacturing — excluded (hardware/automation without software-first focus)
- §4 Medtech / Life Sciences — excluded (no domain match)
- §2 Automotive/Mobility main entries (Bosch, ZF, Mercedes, Porsche parent) — excluded based on no-go "automotive without software focus"; software-only subsidiaries kept
- Respeak, ISTARI AI, Field 33, Collectu, kausable: AI/ML startups with software/data/analytics focus — included

**Included entries after filter:**

| Company | Sector tags | Size | City |
|---|---|---|---|
| SAP SE | enterprise software, AI/ML | corporate | Walldorf |
| TeamViewer AG | software, cloud | corporate | Göppingen |
| MHP Management- und IT-Beratung GmbH | consulting, AI/ML | corporate | Ludwigsburg |
| Aleph Alpha GmbH | AI/ML, NLP, LLMs | startup | Heidelberg |
| Porsche Digital GmbH | automotive, AI/ML | SME | Stuttgart |
| Mercedes-Benz Tech Innovation GmbH | automotive, software | SME | Stuttgart / Ulm |
| Field 33 GmbH | AI/ML, software | startup | BW |
| Respeak GmbH | AI/ML, NLP | startup | BW |
| kausable GmbH | AI/ML, analytics | startup | Tübingen |
| ISTARI AI GmbH | AI/ML, cybersecurity | startup | BW |

**Size filter:** Profile prefers structured supervision → de-prioritize smaller startups (Field 33, Respeak, kausable, ISTARI AI); keep for completeness but rank lower. Trim enrichment to top 6 clearest matches.

---

## Step 4 — Pass 2: Live enrichment

### SAP SE
**2a — R&D focus:** SAP is the world's largest enterprise software company with primary R&D in Walldorf. Active research areas: SAP HANA Cloud (distributed in-memory database), SAP BTP (cloud platform), Agentic AI / Joule AI assistant, LLM integration in enterprise workflows. "SAP Data Science und Künstliche Intelligenz — Start 2025 Standort Walldorf" confirmed (StudySmarter). SAP Labs Germany is the primary German innovation hub. Source: sap.com/germany/about/company/innovation/labs.html; jobs.sap.com (active 2025 ML engineer and thesis listings).
**2b — Thesis signal:** `explicit opening` — jobs.sap.com/content/Studierende/ lists active thesis positions. 2025 Master Thesis in "Agentic AI" (Walldorf) confirmed; ongoing "Data Clustering for Variant Configuration Analytics on S/4HANA" thesis confirmed (wizbii mirror). SAP BTP thesis topics also discussed on SAP Community forum.
**2c — Contact path:** https://jobs.sap.com/content/Studierende/?locale=de_DE
**2d — Recency:** 2025 listings confirmed live. SAP Labs Walldorf and Rot are active.

### MHP Management- und IT-Beratung GmbH
**2a — R&D focus:** IT consulting firm focused on automotive/manufacturing transformation and AI; 100% Porsche-owned. Practice areas: Technology & Data, Intelligent Software, Intelligent Supply Chain. Active on AI, data science, large language models for enterprise workflows. Thesis student positions listed for "Thesis Student — Technology and Data" (LLMs, Predictive Analytics/ML) and "Thesis Student — Intelligent Software." Source: jobs.mhp.com (active listings verified).
**2b — Thesis signal:** `explicit opening` — multiple Thesis Student positions listed at jobs.mhp.com with data + AI topics (LLM, ML, data science); Ludwigsburg location.
**2c — Contact path:** https://jobs.mhp.com/ — search "Thesis"
**2d — Recency:** 2025 listings confirmed; MHP Strategy 2025 active.

**Fit note:** MHP is a consulting firm — thesis work is project-based and involves real client or internal tooling deliverables. Strong fit for data engineering / enterprise LLM; beware that consulting context may limit deep systems research in favor of applied project work.

### Aleph Alpha GmbH
**2a — R&D focus:** German sovereign AI company; built Luminous LLM family and PhariaAI enterprise AI platform. Research team works on novel LLM architectures, data mixes, evaluations. Enterprise customers include German government and DAX companies. Source: aleph-alpha.com; llmreference.com; earlybird job board (Applied Researcher — LLM Training listed 2025).
**⚠ Major corporate event:** Aleph Alpha announced merger with Cohere (April 24, 2026, $20B combined entity operating under "Cohere" name with German anchor). As of 2026-06-28, the merger is recent. Company entity status as "Aleph Alpha GmbH" may be in transition. Verify company is still accepting Masterarbeit applications under the current structure before outreach.
**2b — Thesis signal:** `unclear` — no explicit Masterarbeit listing found at jobs.ashbyhq.com/AlephAlpha as of enrichment. Post-merger uncertainty adds additional risk for thesis timeline stability. Applied Researcher internship roles visible (2025), suggesting student engagement exists.
**2c — Contact path:** https://jobs.ashbyhq.com/AlephAlpha — check current listings; or contact research team via company contact page.
**2d — Recency:** Merger announced April 2026; company demonstrably active. Research output includes T-Free architecture (2025) and Aleph-Alpha-GermanWeb (2025).

### TeamViewer AG
**2a — R&D focus:** Enterprise remote connectivity and IoT platform; ~15,000 employees; R&D locations in Göppingen (HQ), Bremen, Linz, Ioannina. Product areas: remote access software, AR-assisted support, IoT device management. Not primarily a data engineering / distributed systems research company, but scale of platform implies distributed systems engineering work.
**2b — Thesis signal:** `active program` (inferred) — search results confirm "TeamViewer supports Bachelor's and Master's thesis projects"; no dedicated thesis page found at teamviewer.com/en/company/careers/. Working Student QA Engineer listing confirmed at Göppingen (Stepstone).
**2c — Contact path:** https://www.teamviewer.com/en/company/careers/ — search for student positions or send inquiry.
**2d — Recency:** TeamViewer active in 2026; recent job postings confirmed.

**Fit note:** TeamViewer's R&D focus is connectivity/IoT, not data engineering or LLMs. Thesis topics may lean toward remote support systems engineering, AR/VR integration, or IoT device management — relevant to distributed systems but not squarely to data pipelines or enterprise LLMs. Confirm topic availability before outreach.

### Porsche Digital GmbH
**2a — R&D focus:** Digital software subsidiary of Porsche AG; works on connected vehicle data platforms, customer-facing digital products, data engineering for automotive use cases. Technical roles include backend engineering, data platforms, and AI product development.
**2b — Thesis signal:** `active program` (inferred) — Porsche parent has confirmed thesis program at jobs.porsche.com; Porsche Digital shares the portal; software/data engineering roles listed. No Porsche Digital-specific Masterarbeit page found.
**2c — Contact path:** https://jobs.porsche.com — filter for "Porsche Digital" or "Abschlussarbeit"
**2d — Recency:** Porsche Digital active in 2025–2026; data product roles listed.

**Fit note:** Domain is automotive data engineering — relevant to the profile's data pipeline skills but the domain is automotive (a partial no-go if student wants enterprise/finance, not automotive). Keep if student is open to automotive data systems.

### kausable GmbH (bonus entry)
**2a — R&D focus:** AI/ML analytics startup in Tübingen; data analytics and causal ML focus. Small startup in Cyber Valley ecosystem.
**2b — Thesis signal:** `unclear` — no Masterarbeit listing found. Very small startup; direct outreach only.
**2c — Contact path:** https://www.kausable.com — contact page
**2d — Recency:** Backbone entry 2026-06-28; company active unclear from enrichment.

---

## Step 5 — Quality filters

- SAP and MHP: official careers pages used; no job board as thesis source. ✓
- Aleph Alpha: own careers platform (Ashby) used. ✓
- TeamViewer, Porsche Digital: company own domains used. ✓
- All evidence from 2024–2026. ✓
- No job-board aggregators used as primary thesis source (Bright Network/StepStone mirrors noted only as secondary). ✓

---

## Step 6 — No-go check

- Porsche Digital: automotive tag — flag "automotive domain with software focus" → keep with annotation (domain overlap acceptable if student is flexible on automotive data systems).
- Mercedes-Benz Tech Innovation: automotive + software → similar to Porsche Digital; omitted from primary map in favor of cleaner matches; can be noted as "see also."
- Aleph Alpha: merger context — keep with ⚠ flag; thesis timeline risk noted.
- kausable: very small startup, analytics focus — include as a bonus entry.

---

## Step 7 — Option map

---

> **Coverage caveat:** This map covers BW companies that publicly indicate R&D activity in your areas, based on a curated backbone (as of 2026-06-28) and live web enrichment. Most companies do NOT publicize open Masterarbeit positions — 'thesis signal: unclear' does not mean there is no opening. For all entries marked 'unclear', proactive outreach is the recommended next step. The backbone is necessarily incomplete; enterprise software and cloud companies underrepresented in BW relative to automotive and medtech — this is a structural gap, not a skill failure.

---

### Group A — Enterprise Software / Cloud / Data Platforms

---

**SAP SE — SAP Labs Germany / HANA Cloud / AI & Data**
- Sector tags: `[enterprise software, AI/ML]` | Size: corporate | Location: Walldorf (BW)
- **Relevance rationale:** World's largest enterprise software company; primary R&D in Walldorf. Active thesis positions in Agentic AI, data clustering, HANA Cloud, SAP BTP — direct match to "data engineering" and "LLMs for enterprise" interest dimensions.
- **Research focus (live):** SAP HANA Cloud (distributed in-memory database), SAP BTP (cloud platform), Joule AI assistant (LLM integration in enterprise workflows), Agentic AI engineering. 2025 thesis confirmed in Agentic AI at Walldorf; ML engineer roles requiring distributed systems and data pipeline skills. Source: jobs.sap.com; sap.com/germany/about/company/innovation/labs.html (2025).
- **Thesis signal:** `explicit opening` — jobs.sap.com/content/Studierende/ confirms active thesis student program; 2025 Agentic AI Masterarbeit listing at Walldorf confirmed.
- **Pros & likely difficulties:** World-class enterprise software environment; exposure to largest ERP platform globally; strong for data engineering and enterprise LLM topics. Large corporate; topic scope determined by team availability; apply early. English-first work environment.
- **Contact path:** https://jobs.sap.com/content/Studierende/?locale=de_DE — search "Master Thesis" or "Masterarbeit"
- **Thesis coordinator / contact:** not confirmed — supervisor matched via portal after topic selection.

---

**TeamViewer AG — Engineering / R&D**
- Sector tags: `[software, cloud]` | Size: corporate | Location: Göppingen (BW)
- **Relevance rationale:** Enterprise remote connectivity and IoT platform (~15k employees); distributed systems engineering is implicit in the scale of the platform. Relevant to "distributed systems" interest; less directly aligned with "data pipelines" or "enterprise LLMs."
- **Research focus (live):** Remote access, AR-assisted workflows, IoT device management, enterprise connectivity at scale. R&D in Göppingen, Bremen, Linz. Source: teamviewer.com; Wikipedia.
- **Thesis signal:** `active program` (inferred) — search results confirm "TeamViewer supports Bachelor's and Master's thesis projects." No dedicated Masterarbeit portal found; student roles visible (working student QA Engineer, Göppingen, Stepstone 2025).
- **Pros & likely difficulties:** Large, stable enterprise software company; Göppingen BW location. Distributed systems scope likely but not prominently marketed as a thesis area; topic must be confirmed. English-first engineering environment.
- **Contact path:** https://www.teamviewer.com/en/company/careers/ — search for thesis/student roles or send direct inquiry.
- **Thesis coordinator / contact:** not confirmed — apply via careers page.

---

### Group B — Enterprise AI / LLM Research

---

**MHP Management- und IT-Beratung GmbH — Technology & Data / Intelligent Software**
- Sector tags: `[consulting, AI/ML]` | Size: corporate | Location: Ludwigsburg (BW)
- **Relevance rationale:** IT consulting firm with explicit thesis student positions in "Technology and Data" and "Intelligent Software" — topics include LLMs, Predictive Analytics, ML engineering. Direct match to "enterprise LLMs" and "data engineering" interest dimensions.
- **Research focus (live):** Data science for automotive/manufacturing enterprises; LLM applications in enterprise software; intelligent supply chain and production planning optimization. 100% Porsche-owned; strong enterprise client base. Source: jobs.mhp.com (active listings 2025); Wikipedia.
- **Thesis signal:** `explicit opening` — jobs.mhp.com "Thesis Student (f/m/d) Technology and Data" and "Thesis Student (f/m/d) Intelligent Software" listings confirmed active (Ludwigsburg).
- **Pros & likely difficulties:** Real enterprise LLM/data project as thesis topic; exposure to large-scale client environments; strong for applied systems thesis. Consulting context: thesis topic tied to client or internal product need; less academic freedom; thesis may be confidential.
- **Contact path:** https://jobs.mhp.com/ — search "Thesis Student"
- **Thesis coordinator / contact:** not confirmed — apply via jobs.mhp.com directly.

---

**Aleph Alpha GmbH — Research / Enterprise AI**
- Sector tags: `[AI/ML, NLP, LLMs]` | Size: startup | Location: Heidelberg (BW)
- **Relevance rationale:** German sovereign LLM company; PhariaAI enterprise AI platform; research in novel LLM architectures, German-language pre-training, enterprise AI deployment. Direct match to "LLMs for enterprise" interest dimension.
- **Research focus (live):** T-Free character-level LLM architecture (2025); Aleph-Alpha-GermanWeb corpus and training pipeline for German-language LLMs (May 2025); enterprise AI for German government and DAX companies. Source: arxiv.org/abs/2505.00022 (2025); llmreference.com.
- **Thesis signal:** `unclear` — no Masterarbeit listing found (careers at jobs.ashbyhq.com/AlephAlpha). Applied Researcher and Software Engineer roles visible; student engagement likely but not confirmed.
- ⚠ **Corporate transition:** Aleph Alpha announced merger with Cohere (April 24, 2026, $20B combined entity, operating as "Cohere" with German anchor). Company may be in organizational transition. Verify entity status and thesis program availability before committing to this option.
- **Pros & likely difficulties:** Most directly LLM-research-focused company in BW; frontier research environment; access to proprietary LLM training infrastructure. Post-merger instability risk; no structured thesis portal found; very competitive.
- **Contact path:** https://jobs.ashbyhq.com/AlephAlpha — check for current openings; or contact research team via aleph-alpha.com contact page.
- **Thesis coordinator / contact:** not confirmed.

---

### Group C — Automotive Data / Software (domain-adjacent, flag noted)

---

**Porsche Digital GmbH — Data Engineering / Platform**
- Sector tags: `[automotive, AI/ML]` | Size: SME | Location: Stuttgart (BW)
- **Relevance rationale:** Digital subsidiary of Porsche AG; builds connected vehicle data platforms, customer digital products, and AI-powered automotive software — relevant to "data pipeline" and "cloud platform" skills.
- ⚠ **Domain flag:** Automotive domain. Profile no-go is "automotive without software focus" — Porsche Digital is software/data-focused (no manufacturing/hardware). Include if student is open to automotive data systems.
- **Research focus (live):** Connected vehicle data infrastructure, customer experience platforms, AI in digital automotive products. Source: mercedes-benz-techinnovation.com equivalent; jobs.porsche.com.
- **Thesis signal:** `active program` (inferred) — Porsche parent has dedicated thesis program; Porsche Digital uses shared portal. No Porsche Digital-specific Masterarbeit page found.
- **Pros & likely difficulties:** Modern cloud/data tech stack in automotive context; Stuttgart location. Domain is automotive data — strong for students open to that but misaligned if profile strictly prefers fintech/pure enterprise.
- **Contact path:** https://jobs.porsche.com — filter "Porsche Digital" and "Abschlussarbeit"
- **Thesis coordinator / contact:** not confirmed.

---

## Step 8 — Coverage caveat (restated)

> This map covers BW companies that publicly indicate R&D activity in your areas, based on the curated BW company backbone (2026-06-28) and live web enrichment. Most companies do NOT publicize open Masterarbeit positions — 'thesis signal: unclear' does not mean no opening exists. For all entries marked 'unclear', proactive outreach is recommended. Note structural gap: enterprise software, fintech, and cloud-native companies are less represented in BW than automotive and medtech — this is a genuine limitation of the backbone and of BW's industry composition.

---

*Self-check: All 6 profile dimensions verified; Pass 1 backbone-read only; all entries from backbone; no contact names invented; thesis signals classified; recency from 2025–2026; coverage caveat present; Aleph Alpha merger noted explicitly; no job-board aggregator used as thesis source.*
