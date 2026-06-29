---
name: find-university-chairs
description: Discover thesis options — chairs, research groups, and supervisor candidates — across all faculties of the University of Tübingen, for any discipline. Requires a deep student profile (all six dimensions) before searching. Use when a student asks which chair, lab, professor, research group, or supervisor fits their interests, methods, domain, thesis style, or constraints.
---

# Discover Thesis Options

Map a student's research interests to thesis opportunities across **all faculties** of
the University of Tübingen using live web search. No database, no seed list — the search
starts from the official faculty org structure and then enriches with live topic queries.

## Prerequisites

This skill requires a **deep student profile** covering all six dimensions:

1. **Interests** — core research areas / topics
2. **Methods** — how the student wants to work (empirical, qualitative, computational, …)
3. **Domain** — application field (healthcare, education, finance, linguistics, …)
4. **Thesis style** — preferred output type (experimental, theoretical, systems, analysis, survey, mixed)
5. **Skills** — concrete tools / competencies (Python, fMRI, R, ML frameworks, lab methods, …)
6. **No-gos** — hard exclusions (hardware setup, clinical rotations, pure proofs, large-scale SE, …)

**If any dimension is missing or shallow, stop here.** Call `build-student-profile` first
and complete the interview. Do not produce a chair shortlist on a partial profile.

---

## Workflow

### Step 1 — Verify the profile

Check that the conversation contains profile answers for all six dimensions above.
If any is missing or the student has only given a one-line answer ("I like deep learning"),
invoke `build-student-profile` and return here only after the profile is complete.

### Step 2 — Extract query variables

Extract the six dimensions from the profile. For each of **Interests**, **Methods**, and
**Domain** note both a German and an English term. These populate the query slots
`{TOPIC_DE}`, `{TOPIC_EN}`, `{METHOD_DE}`, `{METHOD_EN}`, `{DOMAIN_DE}`, `{DOMAIN_EN}`,
`{NOGO_TERM}` as defined in
[`references/search-strategy.md` §1](references/search-strategy.md).

### Step 3 — Route to relevant faculties

Use the **faculty routing table** in
[`references/search-strategy.md` §2](references/search-strategy.md) to identify the
1–3 relevant faculties / departments for the student's interest+domain combination.
Do not start a global keyword search across all of `uni-tuebingen.de`.

### Step 4 — Pass 1: backbone crawl

For each relevant faculty identified in Step 3, open its official listing URL:

1. **Mathematisch-Naturwissenschaftliche Fakultät (Science):**
   https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/
   — Lists 8 departments (Informatik, Mathematik, Physik, Chemie, etc.); drill into each
   department's `forschung.html` or `arbeitsbereiche` sub-page for chairs.

2. **Philosophische Fakultät (Humanities):**
   https://uni-tuebingen.de/fakultaeten/philosophische-fakultaet/fachbereiche.html
   — Lists 5 departments; drill into each for Seminare and Institute.

3. **Wirtschafts- und Sozialwissenschaftliche Fakultät (Economics & Social Sciences):**
   https://uni-tuebingen.de/fakultaeten/wirtschafts-und-sozialwissenschaftliche-fakultaet/faecher/
   — Lists Fächer under Sozialwissenschaften and Wirtschaftswissenschaft; drill into each.

4. **Juristische Fakultät (Law):**
   https://uni-tuebingen.de/fakultaeten/juristische-fakultaet/lehrstuehle-und-personen/
   — Lists Lehrstühle directly (no drill-down needed).

5. **Evangelisch-Theologische Fakultät (Protestant Theology):**
   https://uni-tuebingen.de/fakultaeten/evangelisch-theologische-fakultaet/lehrstuehle-und-institute/
   — Lists chairs by discipline (no drill-down needed).

6. **Katholisch-Theologische Fakultät (Catholic Theology):**
   https://uni-tuebingen.de/fakultaeten/katholisch-theologische-fakultaet/lehrstuehle/
   — Lists chairs directly.

7. **Medizinische Fakultät (Medicine):**
   Institutes: https://www.medizin.uni-tuebingen.de/de/das-klinikum/einrichtungen/institute
   Clinics: https://www.medizin.uni-tuebingen.de/de/das-klinikum/einrichtungen/kliniken
   — Separate host; lists Institute and Kliniken (no traditional Lehrstühle).

8. **Zentrum für Islamische Theologie (ZITh):**
   https://uni-tuebingen.de/fakultaeten/zentrum-fuer-islamische-theologie/professuren/
   — Lists Professuren by theological specialization.

For **interfaculty institutes & centers** (AI, neuroscience, cross-faculty):
https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/interfakultaere-institute-und-zentren.html

**For AI / ML / neuroscience interests:** the Informatik page alone is insufficient — it does not
list MPI-IS-affiliated groups (Schölkopf, Martius, etc.). Before running any topic queries,
also crawl:
- **MPI for Intelligent Systems:** https://is.mpg.de/departments (Empirical Inference, Autonomous Learning, Perceiving Systems, etc.)
- **ELLIS Tübingen / Cyber Valley:** https://uni-tuebingen.de/forschung/zentren-und-institute/ki-zentrum-tuebingen/ and https://cyber-valley.de/en/research/groups

Treat these as **first-class Pass-1 sources**, not optional enrichment.

This produces your **chair candidate set** — the complete official chair list for the
relevant faculty, anchored to the real org structure rather than SEO results.

### Step 5 — Pass 2: live enrichment per chair

For each chair in the candidate set (or the top subset if > 20), run the enrichment
queries from [`references/search-strategy.md` §3](references/search-strategy.md):

- **2a** relevance check — is this chair actively working on the student's topic?
- **2b** recency — date evidence from 2022 or later
- **2c** thesis openings — explicit Masterarbeit / Abschlussarbeit signals
- **2d** method fit — optional; use when the student has a specific method requirement
- **2e** PI verification — **required before naming any person as chair-holder:** open
  the unit's own staff / team page (or run the person-verification query from
  [`references/search-strategy.md` §4.6](references/search-strategy.md)) and confirm
  the professor listed there. Never borrow a name from a search result that describes a
  *different* group with a similar name (e.g. HIH "Sektion Neuropsychologie" ≠
  FB-Psychologie "Diagnostik und Kognitive Neuropsychologie"). Link to the evidence page.
- **2f** Existence / activity check — **required for every entry:** open the chair or lab's
  own page and confirm it is still active. Check for: page reachable (not 404), at least one
  publication, event, or news item from 2024 or later, and a named PI still listed.
  If the page is gone or shows no activity since 2023, mark the entry
  `⚠ activity not confirmed — verify before outreach` and rank it last. Do not silently drop it.

Use the exact query skeletons from
[`references/search-strategy.md` §4](references/search-strategy.md).

### Step 6 — Apply filters and dedup

Apply the **quality filters** from §5 (prefer official pages, date evidence, specificity,
thesis-readiness signals). Apply **dedup rules** from §6 (merge chair page + professor
personal page; merge faculty listing + interfaculty listing for the same group).

### Step 7 — Apply no-go exclusion

Before ranking, discard chairs that violate the student's no-gos using the exclusion
table in [`references/search-strategy.md` §7](references/search-strategy.md).
If a no-go *might* apply (ambiguous), keep the chair and annotate it with a
`⚠ possible conflict with no-go: {NOGO}` note rather than silently dropping it.

### Step 8 — Produce the option map

Group the surviving chairs by the student's **interest dimension** (not by faculty).
For each option produce the fields described in the Output section below.
End with the coverage caveat.

---

## Output

Produce a **map of options** grouped by interest dimension (e.g. "NLP / Language-in-Education",
"Clinical Neuroscience"). Do not list by faculty.

For each option include:

- **Chair / Arbeitsbereich name** and official URL
- **Relevant person** (professor / lab head), if identifiable from the live web
- **Relevance rationale** — why this matches the profile (tie to specific interests/methods)
- **Pros & likely difficulties** — honest assessment: e.g. large competitive group, unclear
  thesis availability, language barrier, heavy workload, unclear supervision model
- **Dated evidence** — source URL + date (must be 2022 or later to count as recent)
- **Conversation starter** — one concrete angle for a first-contact email
- **No-go flags** — if any no-go partially applies, say so

End the map with the **coverage caveat**:

> "This map covers publicly visible chairs as of [today's date]. Chairs with a weak web
> presence may be missing. To catch them: visit the faculty backbone URLs directly,
> ask the Fachschaft, and check the official Vorlesungsverzeichnis."

---

## Evidence Rules

- Prefer `uni-tuebingen.de` or `medizin.uni-tuebingen.de` pages. Accept personal faculty
  pages and `arxiv.org` / `biorxiv.org` preprints as secondary evidence.
- Do not invent thesis openings, team sizes, citation counts, or willingness to supervise.
- **Never invent or guess URLs.** Every URL in the output must have been retrieved and
  confirmed reachable during this run. If a URL was not opened and verified, do not include it.
- **Every URL is verified twice:** once when first found (Pass 1 or Pass 2 enrichment) and
  once in the existence/activity check (sub-pass 2f). A URL that was not reachable on either
  check must not appear in the output without a `⚠ URL not confirmed` flag.
- Distinguish active research areas (with dated publications) from broad topic descriptions.
- Mark evidence older than 3 years as stale and flag it.
- Do not use any bundled professor, chair, or researcher seed files as a runtime source.
  The live web + faculty backbone is the only authoritative source during discovery.
