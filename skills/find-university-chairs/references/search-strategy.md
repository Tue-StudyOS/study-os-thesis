# Search Strategy Reference

**Purpose:** Reusable instruction set that turns a fully-built student profile into
a precise, reproducible set of web queries for discovering thesis options across
*all* faculties of the University of Tübingen — without a runtime database.

- **Depends on:** [`tuebingen-faculty-backbone.md`](tuebingen-faculty-backbone.md)
  (the anti-SEO-bias baseline of official listing URLs).
- **Used by:** `find-university-chairs` (Task D) and any future discovery skill
  that targets Tübingen.
- **Last updated:** 2026-06-27

---

## 1. Profile dimensions → query variables

Extract these six dimensions from the student profile before running any query.
All dimensions are mandatory; if any is missing, return to `build-student-profile`.

| Profile dimension | What it captures | Query variable |
|---|---|---|
| **Interests** | Core research areas / topics (e.g. "deep learning", "Demokratisierung", "klinische Psychologie") | `{TOPIC_DE}`, `{TOPIC_EN}` |
| **Methods** | How the student wants to work (empirical ML, qualitative interviews, neuroimaging, proof-based) | `{METHOD_DE}`, `{METHOD_EN}` |
| **Domain** | Application field (healthcare, education, finance, social media, linguistics) | `{DOMAIN_DE}`, `{DOMAIN_EN}` |
| **Thesis style** | Preferred output type (experimental, theoretical, systems/engineering, analysis/survey, mixed) | (filter, not a query slot; see §5) |
| **Skills** | Concrete tools / competencies (Python, fMRI, R, lab methods, ML frameworks) | (used to assess fit after discovery) |
| **No-gos** | Hard exclusions (hardware setup, clinical rotations, heavy proofs, large software engineering) | `{NOGO_TERM}` (negative filter; see §4) |

**Extraction rule:** the most useful query slots come from the intersection of
`{TOPIC}` and `{DOMAIN}`. `{METHOD}` adds a second filter axis. Keep German and
English variants — Tübingen pages are German-first but many research groups
maintain English pages.

---

## 2. Profile → faculty routing

Run queries only against **relevant faculties**. Never start with a global keyword
search across all of `uni-tuebingen.de` — it over-returns generic news and
under-returns actual chairs.

| Student interest / domain | Primary faculty / Fachbereich | Possible secondary |
|---|---|---|
| Machine learning, AI, NLP, computer vision, data science | Science → FB Informatik **+ MPI for Intelligent Systems + ELLIS / Cyber Valley** (Pass 1 must crawl all three; FB-Informatik alone misses MPI-IS-affiliated groups) | Science → FB Mathematik (if theory-leaning) |
| Computational social science / computational linguistics | Science → FB Informatik | Humanities → FB4 Neuphilologie |
| Pure mathematics, statistics, algorithms, combinatorics | Science → FB Mathematik | Science → FB Informatik |
| Psychology, cognitive science, decision-making, learning | Science → FB Psychologie | WiSo → Erziehungswissenschaft |
| Neuroscience, neuroimaging, psychiatric disorders | Science → FB Psychologie + interfaculty (BCCN) | Medicine → Kliniken / Hertie Institute |
| Biology, genetics, biochemistry, ecology | Science → FB Biologie | Science → FB Chemie / Pharmazie & Biochemie |
| Chemistry, pharmacology, drug discovery | Science → FB Chemie | Science → FB Pharmazie & Biochemie |
| Medicine, clinical research, public health | Medicine → institutes + Kliniken | Science → FB Biologie |
| Physics, biophysics, quantum | Science → FB Physik | Science → FB Mathematik |
| Earth sciences, geosciences, climate | Science → FB Geowissenschaften | – |
| Economics, finance, management, econometrics | WiSo → Wirtschaftswissenschaft | – |
| Political science, governance, international relations | WiSo → Politikwissenschaft | – |
| Sociology, social inequality, social movements | WiSo → Soziologie | Humanities → FB3 Geschichtswissenschaft |
| Education, learning research, didactics | WiSo → Erziehungswissenschaft | Science → FB Psychologie |
| Sports science, exercise physiology | WiSo → Sportwissenschaft | Medicine |
| Empirical cultural studies, ethnography, popular culture | WiSo → Empirische Kulturwissenschaft | – |
| Law, legal theory, constitutional law, criminal law | Law | – |
| History, medieval / modern European history | Humanities → FB3 Geschichtswissenschaft | – |
| Philosophy, ethics, rhetoric, logic | Humanities → FB5 Philosophie–Rhetorik–Medien | – |
| Languages, literature, linguistics (Romance/Germanic/English) | Humanities → FB4 Neuphilologie | – |
| Classical studies, archaeology, art history | Humanities → FB1 Altertums-/Kunstwissenschaften | – |
| Asian / Middle Eastern studies | Humanities → FB2 Asien-Orient-Wissenschaften | ZITh (Islamic) |
| Protestant / Catholic theology | Evangelisch-Theologische Fakultät or Kath.-Theol. Fakultät | ZITh |
| Islamic theology, Islamic law, Koran sciences | ZITh | Humanities → FB2 |

**Routing ties:** if interest spans two areas (e.g. "ML for healthcare"),
search *both* primary faculties; the two-pass strategy handles this.

**Interfaculty institutes:** For AI / neuroscience / brain research, always add
the Science interfaculty page
(`uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/interfakultaere-institute-und-zentren.html`),
the BCCN/Tübingen-AI-Center entry points, **and the MPI for Intelligent Systems**
(`https://is.mpg.de/departments`) as explicit Pass-1 sources alongside the primary
faculty. MPI-IS hosts key ML/AI groups (Empirical Inference, Autonomous Learning,
etc.) that do not appear on FB-Informatik's `forschung.html` page.

---

## 3. Two-pass search strategy

### Pass 1 — Backbone crawl (structured, anti-SEO-bias)

**Goal:** produce a *complete* list of chairs / Arbeitsbereiche in the relevant
faculty before any topic filtering. This prevents the search from only returning
chairs that happen to rank highly on Google.

**Steps:**

1. Identify the relevant faculty(ies) from §2.
2. Visit the faculty's backbone URL from
   [`tuebingen-faculty-backbone.md`](tuebingen-faculty-backbone.md).
3. If the backbone page lists **departments** (Science, Humanities, WiSo), not
   chairs directly, drill into the relevant department's listing page. Use the
   pattern:  
   `…/fachbereiche/<name>/forschung` OR `…/forschung-arbeitsbereiche` OR
   `…/arbeitsbereiche` OR `…/abteilungen` OR `…/institute`  
   (See the drill-down examples in the backbone file for exact URLs.)
4. Collect every chair / Arbeitsbereich name and URL from the listing page.
   This is your **chair candidate set** for Pass 2.

**Output of Pass 1:** a flat list of (chair name, URL) pairs for the relevant
faculty, anchored to the official org structure.

> **Shortcut when access is read-only:** query
> `site:uni-tuebingen.de/fakultaeten/<faculty-path>/ -filetype:pdf`
> to surface the department's sub-pages and collect links from the result list.

### Pass 2 — Live enrichment per chair (topic + recency evidence)

**Goal:** determine which chairs in the candidate set are actually working on
topics relevant to the student's profile, and gather dated evidence.

For **each chair** in the Pass 1 candidate set (or the top subset if > 20), run:

**2a — Relevance check (is this chair working on the topic?):**
```
site:<chair-url-root> "{TOPIC_DE}" OR "{TOPIC_EN}"
```
or if the chair URL is not site-searchable:
```
"{CHAIR_NAME}" "Universität Tübingen" "{TOPIC_DE}" OR "{TOPIC_EN}"
```

**2b — Recent activity (date evidence):**
```
"{CHAIR_NAME}" OR "{LAB_NAME}" Tübingen "{TOPIC_DE}" 2023 OR 2024 OR 2025 OR 2026 OR 2026
```

**2c — Thesis openings:**
```
"{CHAIR_NAME}" Tübingen (Masterarbeit OR Bachelorarbeit OR "open positions" OR Abschlussarbeit)
```

**2d — Method fit (optional, use when the student has a specific method):**
```
"{CHAIR_NAME}" Tübingen "{METHOD_DE}" OR "{METHOD_EN}"
```

---

## 4. Query skeleton library

Use these templates verbatim, substituting the slot values. Choose skeletons based
on what the student's profile demands; not every skeleton applies to every search.

### 4.1 Backbone crawl queries (Pass 1)

```
# Enumerate departments in a faculty
site:uni-tuebingen.de/fakultaeten/{FACULTY_PATH}/fachbereiche/ OR faecher/ OR lehrstuehle/

# Drill into a specific department for its chairs
site:uni-tuebingen.de/fakultaeten/{FACULTY_PATH}/fachbereiche/{DEPT_NAME}/forschung

# Alternative drill-down pattern
site:uni-tuebingen.de "{DEPT_NAME}" arbeitsbereiche OR abteilungen OR institute
```

### 4.2 Topic-targeted queries (Pass 2a–b)

```
# Official page of a chair on the student's topic
site:uni-tuebingen.de "{TOPIC_DE}" Lehrstuhl OR Arbeitsbereich OR Forschungsgruppe

# Broader: topic + faculty name (for chairs with weak uni-tuebingen.de footprint)
"Universität Tübingen" "{FACULTY_DE}" "{TOPIC_DE}" Forschung

# English-first search (for research groups with English pages)
"University of Tuebingen" OR "Universität Tübingen" "{TOPIC_EN}" research group

# Topic + method pairing
site:uni-tuebingen.de "{TOPIC_DE}" "{METHOD_DE}" Forschung

# Domain-focused (when domain is distinct from topic)
"Universität Tübingen" "{DOMAIN_DE}" "{TOPIC_DE}" Arbeitsgruppe OR Lehrstuhl
```

### 4.3 Thesis-opening queries (Pass 2c)

```
# Thesis openings on the topic
site:uni-tuebingen.de "{TOPIC_DE}" (Masterarbeit OR Abschlussarbeit OR Bachelorarbeit)

# Named chair or professor
"{PROF_NAME}" Tübingen (Masterarbeit OR thesis OR "open positions")

# German-language opening announcement
"Universität Tübingen" "{TOPIC_DE}" "Abschlussarbeit" OR "Themenvorschlag" 2024 OR 2025 OR 2026
```

### 4.4 Recency-confirming queries (Pass 2b)

```
# Recent publications from a chair
"{CHAIR_NAME}" OR "{PROF_NAME}" Tübingen "{TOPIC_DE}" 2023 OR 2024 OR 2025 OR 2026 OR 2026

# Recent papers via faculty publication list
site:uni-tuebingen.de "{CHAIR_NAME}" Publikationen OR Veröffentlichungen

# Preprints (for ML/neuroscience groups)
"Universität Tübingen" "{TOPIC_EN}" site:arxiv.org OR site:biorxiv.org 2024 OR 2025 OR 2026
```

### 4.5 Interfaculty institute queries

```
# Tübingen AI Center
site:uni-tuebingen.de "KI-Zentrum" OR "AI Center" "{TOPIC_DE}" OR "{TOPIC_EN}"

# BCCN (Bernstein Center for Computational Neuroscience)
"BCCN Tübingen" OR "Bernstein Center Tübingen" "{TOPIC_EN}"

# Other cross-faculty centers
"Universität Tübingen" "Zentrum" "{TOPIC_DE}" Forschungsgruppe
```

### 4.6 Person-verification queries (required before naming a PI)

Use these **before attributing a professor to a unit** found in Pass 1 or Pass 2a.
The goal: confirm the named person appears on *that specific unit's own page*, not
just in a search result that mentions both a similar unit name and the person elsewhere.

```
# Confirm the head of a specific Arbeitsbereich (German-language page)
"{ARBEITSBEREICH_NAME}" "Leiter" OR "Leiterin" OR "Mitarbeiter" site:uni-tuebingen.de

# Name + unit co-occurrence on the official faculty page
"{PROF_NAME}" "{ARBEITSBEREICH_NAME}" site:uni-tuebingen.de

# English-language staff page
"{ARBEITSBEREICH_NAME}" Tübingen "team" OR "staff" OR "people" "{PROF_NAME}"
```

**Verification rule:** a person is confirmed for a unit only when one of these queries
returns a page from *that unit's own domain or staff listing* naming the person as
Leiter/Leiterin or group head. A result that names the person alongside a *different*
group with a similar name does not count.

---

## 5. Quality filters

Apply these filters when evaluating search results and the evidence gathered in
Pass 2. Do not promote a chair just because it appears prominently in results.

| Filter | Rule |
|---|---|
| **Source authority** | Prefer `uni-tuebingen.de` or `medizin.uni-tuebingen.de` pages over news, blogs, or alumni sites. Accept personal faculty pages and `arxiv.org`/`biorxiv.org` preprints as secondary evidence. |
| **Date evidence** | Mark evidence as *recent* only if it contains content from 2022 or later (publication date, page "last updated", or news item year). Evidence older than 3 years = stale; flag it. |
| **Specificity** | A chair that lists the student's topic as one of its *active research areas* (with dated publications) outranks one that only mentions the topic in a broad description. |
| **Thesis readiness** | Explicit mention of thesis openings or student projects is a strong positive signal; weight it above general research description. |
| **Lab activity signal** | PhD student / postdoc pages updated recently indicate an active group; dormant group pages (no updates ≥ 3 years) are a risk to flag. |

---

## 6. Dedup rules

Multiple queries and backbone levels can surface the same chair under different
names. Apply these rules before presenting results:

1. **Chair = professor = Arbeitsbereich:** if a professor's personal page and their
   Lehrstuhl/Arbeitsbereich page describe the same group, merge into one entry
   (keep the official Lehrstuhl URL as canonical).
2. **Department listing vs. chair page:** if a department lists "FB Informatik →
   Maschinelles Lernen (Prof. X)" and Pass 2 also finds Prof. X's personal page,
   these are the same entry.
3. **Interfaculty + faculty membership:** a chair that appears on both the Science
   interfaculty page and the Informatik department page is one chair; deduplicate
   and note the dual affiliation.
4. **Clinics vs. institutes (Medicine):** a Klinik entry and an Institute entry at
   `medizin.uni-tuebingen.de` are structurally distinct — only merge if they share
   the same director and research focus.

---

## 7. No-go exclusion

After collecting the candidate chair set, discard entries that violate the
student's no-gos. Apply no-go filtering **before** ranking, not after.

| Student no-go | Exclusion signal | How to detect |
|---|---|---|
| Hardware setup / embedded systems | Keywords: Robotik, Embedded, FPGA, Mikrocontroller, Hardware-in-the-Loop | Scan chair description; exclude if hardware is the *primary* methodology |
| Pure mathematical proofs | Keywords: Algebraische Topologie, Beweistheorie, rein theoretisch, proof-based | Exclude if lab output is exclusively theoretical papers with no empirical component |
| Clinical patient work | Keywords: Klinik, Patientenversorgung, klinische Studien, Notaufnahme | Exclude Medicine *Kliniken* entries unless the student explicitly accepts clinical research |
| Large software engineering | Keywords: Systemarchitektur, large-scale SE, Softwareentwicklung, DevOps | Exclude if the thesis role is primarily software engineering with no research component |
| Heavy teaching involvement | Check if the role is a "Lehrbeauftragter" or teaching-only position | Exclude if the person has no own research group |

**Rule:** if a no-go *might* apply (ambiguous), keep the chair in the candidate
set and annotate it with a "⚠ possible conflict with no-go: {NOGO}" note rather
than silently dropping it.

---

## 8. Output structure

After running both passes and applying filters, produce a **map of options**
grouped by the student's interest dimensions (not by faculty).

For each option include:
- Chair / Arbeitsbereich name and URL
- Relevant person (professor / lab head), if identifiable
- **Relevance rationale:** why this matches the profile
- **Pros & likely difficulties:** honest assessment (e.g. large group, very
  competitive, unclear thesis availability, language barrier)
- **Dated evidence:** source URL + date
- **Conversation starter:** one concrete angle for a first contact email
- **No-go flags** if any no-go partially applies

End with an **honest coverage caveat:**
> "This map covers publicly visible chairs as of [date]. Chairs with weak web
> presence may be missing. To catch them: visit the faculty backbone URLs directly,
> ask the Fachschaft, and check the official Vorlesungsverzeichnis."

---

## 9. Worked examples

### Example A — "Ethical AI in Education"

**Condensed profile:**
- Interests: ML fairness, educational technology, NLP
- Methods: empirical evaluation + qualitative user studies
- Domain: education, accessibility
- Style: applied/empirical, mixed-methods acceptable
- No-gos: hardware setup, heavy proofs, clinical settings

**Step 1 — Route to faculties:**
- Primary: Science → FB Informatik (NLP, ML fairness)
- Secondary: WiSo → Erziehungswissenschaft (educational research, Hector-Institut)
- Interfaculty: Tübingen AI Center (ML ethics groups)

**Step 2 — Pass 1 backbone crawl:**

```
# Get CS chairs
[Visit] https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html
→ Collect: NLP group, ML group, human-computer interaction group (if any)

# Get WiSo education chairs
[Visit] https://uni-tuebingen.de/fakultaeten/wirtschafts-und-sozialwissenschaftliche-fakultaet/faecher/
→ Drill into: Erziehungswissenschaft sub-page for its Arbeitsbereiche
→ Collect: Hector-Institut für Empirische Bildungsforschung and others

# Interfaculty
[Visit] https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/interfakultaere-institute-und-zentren.html
→ Note: Tübingen AI Center entry
```

**Step 3 — Pass 2 enrichment queries:**

```
# Relevance check — CS
site:uni-tuebingen.de "NLP" OR "natural language processing" Bildung OR education Forschungsgruppe

# Relevance check — ML fairness
"Universität Tübingen" Informatik "Fairness" OR "KI-Ethik" OR "responsible AI" 2023 OR 2024 OR 2025 OR 2026 OR 2026

# WiSo education
"Universität Tübingen" Erziehungswissenschaft "Lerntechnologie" OR "educational technology" Forschung

# Thesis openings
site:uni-tuebingen.de "NLP" OR "Bildungstechnologie" (Masterarbeit OR Abschlussarbeit) 2024 OR 2025 OR 2026

# Recency
"Universität Tübingen" Informatik "NLP" OR "maschinelles Lernen" 2024 site:arxiv.org OR site:uni-tuebingen.de
```

**No-go filter applied:** discard any Informatik Arbeitsbereich focused on
embedded systems, FPGA, or robotics hardware (keywords: "Eingebettete Systeme",
"Robotik-Hardware", "FPGA").

**Expected output shape:** 3–6 options across Informatik and Erziehungswissenschaft,
grouped as "NLP / Language-in-Education" and "Educational Technology / Learning
Research", each with dated evidence.

---

### Example B — "Clinical Neuroscience / Neuroimaging"

**Condensed profile:**
- Interests: fMRI, psychiatric disorders, brain connectivity
- Methods: neuroimaging, statistical modeling, computational neuroscience
- Domain: psychiatry, cognitive neuroscience
- Style: empirical, data-driven, lab collaboration preferred
- No-gos: purely theoretical (no empirical data), no teaching-heavy roles

**Step 1 — Route to faculties:**
- Primary: Science → FB Psychologie (cognitive neuroscience, neuroimaging groups)
- Secondary: Medicine → institutes (Hertie Institute for Clinical Brain Research;
  Psychiatry Klinik for clinical imaging)
- Interfaculty: BCCN (Bernstein Center for Computational Neuroscience)

**Step 2 — Pass 1 backbone crawl:**

```
# Get Psychology chairs (drill-down required)
[Visit] https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/psychologie/
→ Navigate to Forschung / Arbeitsbereiche sub-page
→ Collect: Kognitionswissenschaft, Neuropsychologie, Biologische Psychologie groups

# Medicine institutes
[Visit] https://www.medizin.uni-tuebingen.de/de/das-klinikum/einrichtungen/institute
→ Collect: Hertie Institute for Clinical Brain Research; Neurological Institute

# BCCN
[Visit] https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/interfakultaere-institute-und-zentren.html
→ Identify BCCN entry and its member groups
```

**Step 3 — Pass 2 enrichment queries:**

```
# Relevance check — Psychology
site:uni-tuebingen.de Psychologie "fMRT" OR "fMRI" OR "Neuroimaging" Forschungsgruppe

# Medicine / clinical imaging
"Universität Tübingen" Psychiatrie "fMRI" OR "Hirnkonnektivität" OR "brain connectivity" Forschung

# BCCN
"BCCN Tübingen" OR "Bernstein Center Tübingen" "fMRI" OR "computational neuroscience" 2023 OR 2024

# Thesis openings
site:uni-tuebingen.de Psychologie OR Neurologie "fMRT" (Masterarbeit OR Abschlussarbeit) 2024 OR 2025 OR 2026

# Recency via preprints
"Universität Tübingen" "fMRI" OR "neuroimaging" "psychiatric" site:biorxiv.org OR site:arxiv.org 2024
```

**No-go filter applied:** discard chairs classified as purely theoretical /
computational-only (no imaging data mentioned), and any teaching-only Lehrbeauftragte
roles. Keep clinical Kliniken-based groups with an active imaging unit (fMRI scanner
access is the positive signal).

**Expected output shape:** 4–8 options across Psychologie, Medicine institutes/Kliniken,
and BCCN, grouped as "Cognitive / Biological Psychology (imaging-based)" and
"Clinical Neuroscience / Psychiatric Imaging", each with dated evidence and a
note on scanner / data access.
