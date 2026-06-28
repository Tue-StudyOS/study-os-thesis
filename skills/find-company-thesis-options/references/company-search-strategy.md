# Company Search Strategy Reference

**Purpose:** Reusable instruction set that turns a fully-built student profile into
a precise, reproducible query set for discovering Masterarbeit options at BW companies —
without a runtime database and without job-board noise.

- **Depends on:** [`bw-company-backbone.md`](bw-company-backbone.md)
  (the anti-SEO-bias baseline of curated BW company entries with sector tags).
- **Used by:** `find-company-thesis-options` skill.
- **Last updated:** 2026-06-28

---

## 1. Profile dimensions → query variables

Extract these six dimensions from the student profile before running any query.
All dimensions are mandatory; if any is missing, return to `build-student-profile`.

| Profile dimension | What it captures | Query variable | Company filter |
|---|---|---|---|
| **Interests** | Core research areas / topics (e.g. "NLP", "Bildverarbeitung", "Energieoptimierung") | `{TOPIC_DE}`, `{TOPIC_EN}` | Maps to backbone sector tags (e.g. "AI/ML", "NLP", "energy") — filters which backbone sections to read |
| **Methods** | How the student wants to work (empirical ML, lab experiments, systems engineering, statistical modeling) | `{METHOD_DE}`, `{METHOD_EN}` | Used in Pass 2 relevance queries; not a backbone filter (backbone tags don't encode methods) |
| **Domain** | Application field (automotive, healthcare, manufacturing, enterprise software) | `{DOMAIN_DE}`, `{DOMAIN_EN}` | Maps directly to backbone sector tags (e.g. "automotive", "medtech", "industrial") — often the primary filter axis |
| **Thesis style** | Preferred output type (applied/empirical, theoretical, engineering, survey) | (filter in Pass 2, not a backbone slot) | Signals startup vs. corporate fit: applied/engineering → startup; structured lab-style → corporate R&D division |
| **Skills** | Concrete tools / competencies (Python, PyTorch, CAD, LabVIEW, MATLAB, NLP frameworks) | (used to assess fit after discovery) | No direct backbone filter; used to identify skill-fit during Pass 2 enrichment |
| **No-gos** | Hard exclusions (pure hardware, clinical patient work, non-technical roles, specific sectors) | `{NOGO_TERM}` (negative filter; see §6) | Maps to backbone sector tags for exclusion: e.g. no-go "robotics hardware" → exclude entries tagged `robotics` if hardware is primary focus |

**Extraction rule:** the most useful filter axes are the intersection of `{DOMAIN}` and
`{INTERESTS}`, mapped to backbone sector tags. `{METHOD}` and `{SKILLS}` drive Pass 2
queries, not Pass 1 filtering. Always prepare both German and English query variants — company
R&D pages are often bilingual, with English-first for international labs.

---

## 2. Profile → backbone filter

### 2.1 Interest-to-tag mapping

Match the student's `{INTERESTS}` and `{DOMAIN}` to backbone sector tags to determine
which backbone sections to read and which rows to keep.

| Student interest / domain | Primary backbone sector tags | Secondary tags to check |
|---|---|---|
| Machine learning, deep learning, NLP, LLMs | `AI/ML`, `NLP` | `automotive` (AI-in-car), `medtech` (AI-in-health), `industrial` (AI-in-manufacturing) |
| Computer vision, image analysis | `AI/ML`, `computer-vision` | `medtech`, `robotics`, `optics` |
| Robotics, autonomous systems | `robotics`, `AI/ML`, `automotive` | `industrial`, `logistics` |
| Automotive, mobility, autonomous driving | `automotive`, `AI/ML` | `robotics`, `simulation` |
| Medical devices, health tech | `medtech`, `AI/ML` | `optics`, `pharma`, `sensors` |
| Manufacturing, industrial automation | `industrial`, `automation` | `automotive`, `sensors`, `IoT` |
| Sensors, IoT, embedded systems | `IoT`, `sensors` | `industrial`, `automotive`, `smart-home` |
| Energy, sustainability, climate tech | `energy`, `sustainability`, `climate` | `industrial`, `AI/ML` |
| Enterprise software, ERP, business AI | `enterprise software`, `AI/ML` | `consulting` |
| Supply chain, logistics, operations | `supply-chain`, `logistics`, `AI/ML` | `industrial` |
| Cybersecurity, safe AI | `cybersecurity`, `AI/ML` | `automotive` (functional safety) |

### 2.2 Filtering logic

Apply in this order:

1. **Include:** keep all backbone entries whose sector tags include at least one tag from
   the student's interest-to-tag mapping above.
2. **Expand:** if the student's domain tag matches a backbone section heading (e.g. "Medtech /
   Life Sciences"), include the entire section as a candidate set before tag-filtering —
   then trim using the interest intersection. This prevents cross-sector tag misses.
3. **Exclude no-gos:** apply §6 exclusion rules to remove entries whose sector tags
   signal a no-go match.
4. **Size filter (optional):** if the student's thesis style is "startup" or they prefer an
   agile environment, de-prioritize `corporate` entries (still include, but rank lower);
   if structured supervision is preferred, de-prioritize `startup` entries.

**Output of backbone filter:** a filtered candidate set of 5–20 companies. If the filter
returns more than 20, tighten the tag intersection. If it returns fewer than 5, broaden by
one secondary tag or lower the size filter.

---

## 3. Two-pass strategy

### Pass 1 — Backbone filter (no web search)

**Goal:** produce a candidate company set without touching the live web. This is the
anti-SEO-bias step that ensures results are anchored to known R&D-relevant BW companies,
not to whatever happens to rank well for "Masterarbeit + topic".

**Steps:**

1. Read [`bw-company-backbone.md`](bw-company-backbone.md) in full.
2. Apply the §2 backbone filter: select entries whose sector tags intersect the student's
   interest and domain tags, then apply no-go exclusions from §6.
3. Note the `Size` column: flag whether each candidate is `startup`, `SME`, or `corporate`.
4. Collect for each selected entry: company name, sector tags, size, city, careers/research URL,
   last verified date.

**Output of Pass 1:** a flat filtered list of (company name, sector tags, size, careers URL)
pairs. This is your **candidate set** for Pass 2.

> **If the backbone URL is stale (404):** search `"{COMPANY_NAME}" Masterarbeit OR Abschlussarbeit`
> to find the current entry point, then update your working candidate list.

### Pass 2 — Live enrichment per company

**Goal:** for each candidate from Pass 1, determine what the R&D team actually works on,
whether there is a thesis signal, and how to contact them — using targeted `site:` queries
against the company's own domain.

Run the following sub-passes for each candidate company. Use the query skeletons in §4.

**2a — R&D focus (what does this team actually work on?):**

```
site:{COMPANY_DOMAIN} "{TOPIC_EN}" OR "{TOPIC_DE}" research OR Forschung
```

If the careers URL points to a third-party platform (Ashby, Personio, Workable), also query
the company's main domain directly:

```
site:{COMPANY_MAIN_DOMAIN} research OR Forschung OR R&D
```

**2b — Thesis signal (any listed Masterarbeit / Abschlussarbeit position?):**

```
site:{COMPANY_DOMAIN} (Masterarbeit OR Abschlussarbeit OR "thesis" OR "student project") "{TOPIC_EN}" OR "{TOPIC_DE}"
```

If this returns nothing, run the broader fallback:

```
"{COMPANY_NAME}" (Masterarbeit OR Abschlussarbeit OR "Abschlussarbeit schreiben") 2023 OR 2024 OR 2025
```

**2c — Contact path (careers portal URL or named contact):**

```
site:{COMPANY_DOMAIN} (Karriere OR career OR Kontakt OR contact OR team OR Ansprechpartner) Hochschule OR Studenten OR students
```

Only surface a named contact if they appear on the company's own page. Never infer or guess.

**2d — Recency evidence (has the R&D work been active recently?):**

```
site:{COMPANY_DOMAIN} "{TOPIC_EN}" 2022 OR 2023 OR 2024 OR 2025
```

or via publications / press:

```
"{COMPANY_NAME}" "{TOPIC_EN}" research 2023 OR 2024 OR 2025
```

---

## 4. Query skeleton library for Pass 2

Use these templates verbatim, substituting slot values. Not every skeleton applies to every
company — choose based on what the candidate's profile demands.

### 4.1 R&D focus queries

```
# Company's own research description
site:{COMPANY_DOMAIN} "{TOPIC_EN}" OR "{TOPIC_DE}" research OR Forschung OR innovation

# R&D team or lab page (many corporates have named labs)
site:{COMPANY_DOMAIN} "research" OR "R&D" OR "Forschung" lab OR center OR Zentrum

# For Cyber Valley members — check for any Cyber Valley affiliation page
"Cyber Valley" "{COMPANY_NAME}" "{TOPIC_EN}"

# For companies with published papers
"{COMPANY_NAME}" "{TOPIC_EN}" site:arxiv.org OR site:ieeexplore.ieee.org 2023 OR 2024 OR 2025
```

### 4.2 Thesis signal queries

```
# Explicit Masterarbeit listing on company domain
site:{COMPANY_DOMAIN} (Masterarbeit OR Abschlussarbeit OR "master thesis" OR "student thesis") "{TOPIC_EN}" OR "{TOPIC_DE}"

# Active thesis program (general mention of Abschlussarbeiten, not position-specific)
site:{COMPANY_DOMAIN} (Abschlussarbeit OR "Abschlussarbeiten" OR Studienarbeit) students OR Studenten

# Structured student programs (for corporates that run cohort programs)
site:{COMPANY_DOMAIN} ("Abschlussarbeit" OR "master's thesis" OR "Werkstudent") Programm OR Program

# Third-party recruitment platform (if careers URL is not on company domain)
site:{CAREERS_PLATFORM_DOMAIN} "{COMPANY_NAME}" Masterarbeit OR thesis OR Abschlussarbeit
```

### 4.3 Contact / team queries

```
# Named coordinator on company's student/career page
site:{COMPANY_DOMAIN} (Hochschulkontakt OR "university relations" OR Ansprechpartner) Abschlussarbeit OR thesis

# R&D team page (may include research lead contact)
site:{COMPANY_DOMAIN} "research team" OR "Forschungsteam" OR "our team" OR "unser Team"

# For startups: who to reach out to (often founders or leads)
site:{COMPANY_DOMAIN} "contact" OR "Kontakt" team OR founder OR CEO OR CTO

# Career fair / event presence (useful entry angle)
"{COMPANY_NAME}" Hochschulmesse OR career fair Stuttgart OR Karlsruhe OR Tübingen 2024 OR 2025
```

### 4.4 Recency / date evidence queries

```
# Recent activity on company's own domain
site:{COMPANY_DOMAIN} "{TOPIC_EN}" 2023 OR 2024 OR 2025

# Press release or news confirming recent R&D activity
"{COMPANY_NAME}" "{TOPIC_EN}" Forschung OR research press OR news 2024 OR 2025

# For AI/ML companies: Cyber Valley announcements
site:cybervalley.de "{COMPANY_NAME}" 2023 OR 2024 OR 2025
```

### 4.5 Fallback queries (when site: returns nothing)

Use when a company has a weak web presence or their R&D pages are not indexed.

```
# Direct name search with thesis term
"{COMPANY_NAME}" Masterarbeit OR "Masterarbeit Thema" 2023 OR 2024 OR 2025

# LinkedIn company page (read-only; acceptable as a fallback signal source)
site:linkedin.com/company "{COMPANY_NAME}" Masterarbeit OR "master thesis" OR Abschlussarbeit

# Academic paper with company affiliation
"{COMPANY_NAME}" {TOPIC_EN} site:arxiv.org OR site:dl.acm.org OR site:researchgate.net 2023 OR 2024

# Company mentioned on Cyber Valley partner page
site:cybervalley.de "{COMPANY_NAME}"
```

---

## 5. Quality filters

Apply these filters when evaluating search results and evidence gathered in Pass 2.
Do not promote a company just because it appears prominently in results.

| Filter | Rule |
|---|---|
| **Source authority** | Prefer the company's own domain (`{COMPANY_DOMAIN}`) over job-board aggregators (LinkedIn, StepStone, Indeed, Glassdoor). Accept `cybervalley.de` as a secondary authority for Cyber Valley members. Arxiv / IEEE are acceptable for publication evidence only. |
| **No job-board aggregators** | Never use StepStone, Indeed, or similar job boards as the source of a thesis listing — they re-post and strip context. Only use them as a fallback signal that a position may exist, then trace it to the official source. |
| **Date evidence required** | Mark evidence as *recent* only if it contains content from 2022 or later (listing date, page "last updated", or publication year). Evidence older than 3 years = stale; flag it. A thesis listing without a date is `thesis signal: unclear`. |
| **Specificity of R&D match** | A company whose R&D page explicitly mentions the student's topic (with dated examples) outranks one that only mentions it as a vague capability. Concrete: "we work on transformer-based NLP for CRM systems" > "we use AI". |
| **Sub-domain preference** | For large corporates with many sub-sites, prefer R&D or research sub-domains (`research.{company}.com`, `ai.{company}.com`, `labs.{company}.com`) over generic marketing pages. These sub-domains signal the existence of a research unit. |
| **Startup recency check** | For startup entries, verify the company's main domain is reachable and was last updated within 24 months. A startup with a frozen website or no social presence may no longer be active. Flag with "⚠ web presence not confirmed — verify before outreach". |

---

## 6. No-go exclusion

After producing the Pass 1 candidate set, discard or flag entries that conflict with the
student's no-gos. Apply exclusion **before** Pass 2 enrichment to avoid wasting query
budget on incompatible companies.

| Student no-go | Backbone exclusion signal | Action |
|---|---|---|
| Pure hardware / embedded systems | Sector tags include `IoT`, `sensors`, or `robotics` as the *only* tags, with no `AI/ML` or `software` co-tag | Discard unless the student's interest explicitly matches hardware |
| Automotive (sector-level) | Backbone section "Automotive / Mobility"; sector tags `automotive` | Discard entire automotive section; no per-entry check needed |
| Medtech / clinical work | Sector tags `medtech`, `pharma` | Discard medtech section; include only if student domain is healthcare-compatible |
| Non-technical / consulting | Sector tags `consulting`, `HR-tech` (without `AI/ML`) | Discard if student wants engineering/research role |
| Corporate bureaucracy | Size = `corporate` (if student preference is startup/agile) | Flag, do not hard-discard; include with note "corporate structure — long lead time" |
| Startups / unstructured supervision | Size = `startup` (if student prefers structured program) | Flag, do not hard-discard; include with note "startup — supervision structure unclear" |

**Ambiguous no-gos:** if a no-go *might* apply (e.g. a company tagged `robotics, AI/ML`
and the student's no-go is "no hardware robotics"), keep the entry and annotate:
`⚠ partial no-go conflict: verify whether the role is software/ML-side or hardware-side
before outreach`.

---

## 7. Output structure per company

After running both passes and applying filters, populate one structured entry per company.
Mirror the schema from Decision 2 in `2026-06-28-phase2-company-decisions.md`.

### Always-present fields (from backbone or live enrichment)

```
Company:           [full company name]
Division / team:   [business unit or R&D lab name, e.g. "Bosch Center for AI"; mark "unknown" if not determinable]
Sector tags:       [from backbone, e.g. AI/ML, automotive]
Size:              startup | SME | corporate
Location:          [city + (BW)]
Relevance rationale: [why this matches the student's profile dimensions — tie to specific interests, domain, method]
Pros & likely difficulties: [honest: e.g. "large structured program, requires portal application 4–6 months out";
                            "startup — supervision may be informal; IP/confidentiality constraints likely";
                            "corporate R&D lab — English work environment; competitive application"]
Contact path:      [careers portal URL from backbone; or "direct R&D team inquiry — no portal found";
                   or "contact via career fair: {event name}"]
```

### Present only when found in live web (mark `not found` if absent)

```
Research focus (live): [what the R&D team actually works on — with dated evidence (2022+) and source URL]
Thesis signal:         explicit opening | active program | unclear
                       — explicit opening: a currently listed Masterarbeit / thesis position found on the
                         company's own page, with URL and date
                       — active program: careers page mentions Abschlussarbeiten generally but no open
                         position is listed
                       — unclear: no public signal found; proactive outreach required
Thesis coordinator / contact: [named person ONLY if confirmed on the company's own public page;
                               never inferred or guessed; otherwise omit]
```

### Never included

- Unpublicized application deadlines.
- Salary or compensation information.
- Any named supervisor or contact not publicly confirmed by the company itself.

### Map-level coverage caveat (required once, at the top of the output map)

> "This map covers BW companies that publicly indicate R&D activity in your areas, based on a
> curated backbone (as of [date]) and live web enrichment. Most companies do NOT publicize
> open Masterarbeit positions — a 'thesis signal: unclear' does not mean there is no opening.
> For all entries marked 'unclear', proactive outreach (careers portal or direct R&D contact)
> is the recommended next step. The backbone is necessarily incomplete; new startups and
> divisions not yet in the list are a known gap."

### Grouping

Group the output map by the student's **interest dimension**, not by backbone sector or
company size. Example groupings:
- "NLP / Language AI" companies
- "Computer Vision in Healthcare" companies
- "Automotive AI / Autonomous Systems" companies

If a company fits multiple groups, place it in the group that best matches its primary R&D
focus and note the secondary fit in the relevance rationale.

---

## 8. Worked examples

### Example A — "NLP / Conversational AI for Enterprise"

**Condensed profile:**
- Interests: NLP, large language models, conversational AI, retrieval-augmented generation
- Methods: empirical ML, model fine-tuning, evaluation benchmarks
- Domain: enterprise software, customer communication, knowledge management
- Style: applied/empirical; prefers working with real product data
- Skills: Python, PyTorch, HuggingFace Transformers
- No-gos: pure hardware/robotics, non-technical roles, academic-only research with no applied component

---

**Step 1 — Backbone filter (Pass 1)**

Interest tags: `AI/ML`, `NLP`  
Domain tags: `enterprise software`, `AI/ML`  
No-go exclusions: entries where `robotics` or `automotive` is the *only* tag and NLP is absent; entries tagged `consulting` only; size filter: no hard exclusion, but flag `corporate` as requiring 4–6 month lead time.

```
Read bw-company-backbone.md, Section 1 (AI/ML) — include all rows tagged NLP or AI/ML.
Read bw-company-backbone.md, Section 5 (Software / Enterprise) — include SAP, TeamViewer, MHP.

Pass 1 candidate set (illustrative):
- Aleph Alpha GmbH       | AI/ML, NLP | startup | Heidelberg
- Respeak GmbH           | AI/ML, NLP | startup | BW
- SAP SE                 | enterprise software, AI/ML | corporate | Walldorf
- kausable GmbH          | AI/ML, analytics | startup | Tübingen
- Field 33 GmbH          | AI/ML, software | startup | BW
- MHP GmbH               | consulting, AI/ML | corporate | Ludwigsburg   ← flag: consulting-adjacent
- Collectu GmbH          | AI/ML, data | startup | BW
- BinDoc GmbH            | AI/ML, document | startup | BW

Excluded from no-go:
- NEURA Robotics, sereact, NODE Robotics (robotics primary, no NLP tag)
- Vialytics, DeepScenario, nuvus (mobility/automotive primary, no NLP)
```

---

**Step 2 — Pass 2 enrichment per candidate**

*Aleph Alpha GmbH (Heidelberg)*

```
# R&D focus
site:aleph-alpha.com "NLP" OR "LLM" OR "large language model" research

# Thesis signal
site:aleph-alpha.com Masterarbeit OR Abschlussarbeit OR "student thesis"
— Fallback: "Aleph Alpha" Masterarbeit 2024 OR 2025

# Contact path
site:aleph-alpha.com careers OR Karriere Studenten OR students

# Recency
"Aleph Alpha" NLP OR LLM research 2024 site:arxiv.org
```

*SAP SE (Walldorf)*

```
# R&D focus (SAP Labs Germany is the research arm)
site:labs.sap.com "NLP" OR "LLM" OR "language model" OR "conversational AI"

# Thesis signal (SAP has a structured student portal)
site:jobs.sap.com/content/Studierende Masterarbeit OR "master thesis" NLP OR language

# Contact path
site:sap.com karriere studenten Abschlussarbeit Ansprechpartner

# Recency
"SAP" "language model" OR "NLP" research 2024 site:arxiv.org OR site:sap.com
```

*Respeak GmbH (BW)*

```
# R&D focus (startup — check main site directly)
site:respeak.io research OR technology OR NLP OR "speech recognition"

# Thesis signal
"Respeak" Masterarbeit OR thesis 2023 OR 2024 OR 2025
— Fallback: site:linkedin.com/company "respeak" Masterarbeit

# Recency
site:respeak.io 2023 OR 2024
```

---

**No-go filter applied:**  
MHP GmbH is flagged "consulting-heavy — likely project work, not research thesis; verify whether R&D thesis placement exists before including in map."  
Vialytics, DeepScenario, nuvus discarded (no NLP tag).

---

**Expected output shape:**

Output map grouped as:
- **"Large Language Models / NLP AI"** — Aleph Alpha, Respeak, kausable; 3–4 entries  
- **"Enterprise AI / Knowledge Management"** — SAP SE, BinDoc, Field 33; 2–3 entries

Each entry: relevance rationale tied to "RAG" or "conversational AI" interest; thesis signal from live search; contact path (SAP portal vs. direct startup email); honest pros/difficulties note (SAP: structured, 4–6 month lead; Aleph Alpha: high bar, competitive, likely English-only).

---

### Example B — "Medical Image Analysis"

**Condensed profile:**
- Interests: computer vision, medical image segmentation, deep learning for diagnostics
- Methods: supervised deep learning, CNN/ViT architectures, model evaluation on medical datasets
- Domain: healthcare, radiology, ophthalmic imaging, endoscopy
- Style: applied/empirical, lab collaboration preferred, clinical data acceptable (no direct patient contact)
- Skills: Python, PyTorch, MONAI or similar medical imaging libraries
- No-gos: purely theoretical work (no data), pure hardware design, non-technical business roles

---

**Step 1 — Backbone filter (Pass 1)**

Interest tags: `AI/ML`, `computer-vision`, `medtech`, `optics`  
Domain tags: `medtech`, `AI/ML`  
No-go exclusions: entries where sector is purely `industrial` or `automotive` with no medtech/AI link; size filter: none — both startup and corporate can offer medical imaging theses.

```
Read bw-company-backbone.md, Section 4 (Medtech / Life Sciences) — include all rows.
Read bw-company-backbone.md, Section 1 (AI/ML) — include rows tagged medtech or computer-vision.

Pass 1 candidate set:
- Carl Zeiss AG              | optics, medtech | corporate | Oberkochen
- Karl Storz GmbH & Co. KG  | medtech | corporate | Tuttlingen
- Roche Diagnostics GmbH     | pharma, medtech | corporate | Mannheim
- Heidelberg Engineering GmbH| medtech, imaging | SME | Heidelberg
- Bosch Sensortec GmbH       | IoT, sensors | SME | Reutlingen   ← secondary; verify imaging connection
- eye2you GmbH               | AI/ML, medtech | startup | Tübingen
- Medicalvalues GmbH         | AI/ML, medtech | startup | Stuttgart
- Cytolytics GmbH            | AI/ML, medtech | startup | Tübingen
- DeepCare GmbH              | AI/ML, medtech | startup | BW
- NODE Robotics GmbH         | robotics, medtech | startup | Stuttgart   ← flag: robotics component

Excluded from no-go:
- Pure industrial/automation companies (no medtech tag): Trumpf, Festo, Kärcher, SEW-EURODRIVE, etc.
- Non-AI automotive sector.
```

---

**Step 2 — Pass 2 enrichment per candidate**

*Carl Zeiss AG (Oberkochen)*

```
# R&D focus (Zeiss has multiple divisions — target the Meditec sub-domain)
site:zeiss.com "medical imaging" OR "image segmentation" OR "deep learning" OR "AI" Meditec OR research

# Thesis signal (Zeiss has a structured student portal)
site:zeiss.com/career Masterarbeit OR "master thesis" "medical imaging" OR "computer vision" OR "deep learning"

# Contact path
site:zeiss.com/career studenten OR Hochschule Ansprechpartner OR contact

# Recency
"Carl Zeiss" "medical imaging" OR "AI" OR "deep learning" research 2023 OR 2024
```

*eye2you GmbH (Tübingen)*

```
# R&D focus (retinal imaging AI startup — small team)
site:eye2you.org research OR technology OR "retinal" OR "fundus" OR "deep learning"

# Thesis signal
"eye2you" Masterarbeit OR thesis 2023 OR 2024 OR 2025
— Fallback: site:linkedin.com/company "eye2you" Masterarbeit

# Contact path
site:eye2you.org contact OR Kontakt OR team

# Recency
"eye2you" "retinal" OR "fundus" site:arxiv.org OR site:researchgate.net 2022 OR 2023 OR 2024
```

*Heidelberg Engineering GmbH (Heidelberg)*

```
# R&D focus (ophthalmic imaging — OCT hardware + analysis software)
site:heidelbergengineering.com research OR "deep learning" OR "AI" OR "image analysis" OR "OCT"

# Thesis signal
site:heidelbergengineering.com Masterarbeit OR "student" OR career
— Fallback: "Heidelberg Engineering" Masterarbeit OR thesis 2023 OR 2024

# Recency
"Heidelberg Engineering" "OCT" OR "image analysis" OR "deep learning" 2023 OR 2024
```

*Cytolytics GmbH (Tübingen)*

```
# R&D focus (cytology AI — cell image analysis)
site:cytolytics.de technology OR research OR "cell" OR "pathology" OR "deep learning"

# Thesis signal
"Cytolytics" Masterarbeit OR thesis 2023 OR 2024 OR 2025
— Fallback: site:cybervalley.de "Cytolytics"

# Recency
site:cytolytics.de 2022 OR 2023 OR 2024
```

---

**No-go filter applied:**  
NODE Robotics flagged: `⚠ partial no-go conflict — medtech tag present but robotics is primary; verify whether thesis would be ML/software or hardware robotics`.  
Bosch Sensortec de-prioritized: IoT/sensors is primary; no imaging connection confirmed — requires Pass 2 verification before including.

---

**Expected output shape:**

Output map grouped as:
- **"Ophthalmic / Optics Imaging AI"** — Carl Zeiss (Meditec), eye2you, Heidelberg Engineering; 3 entries  
- **"Diagnostic AI / Pathology / Cell Analysis"** — Cytolytics, Medicalvalues, DeepCare; 2–3 entries  
- **"Clinical Imaging / Diagnostic Devices"** — Karl Storz (endoscopy imaging), Roche Diagnostics; 2 entries

Each entry: relevance rationale tied to "medical image segmentation" or "diagnostic AI" interest; thesis signal from live search (Karl Storz and Zeiss are expected `active program`; startups likely `unclear`); contact path (Zeiss/Storz via portal, eye2you/Cytolytics via direct team contact or Cyber Valley network); honest pros/difficulties note (startups: close supervision, IP constraints, smaller dataset; corporates: structured program, regulatory context, may require medical-domain onboarding).
