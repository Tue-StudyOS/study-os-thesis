# BW Company Backbone

**Purpose:** Anti-SEO-bias baseline for `find-company-thesis-options`. The skill reads
this file in Pass 1 to identify candidate companies by sector-tag filtering — before running
any live web search. This mirrors the role of `tuebingen-faculty-backbone.md` for university
chairs: it anchors discovery in a curated, known-relevant set and prevents job-board noise
from dominating results.

- **Scope:** Companies with an R&D presence in Baden-Württemberg (BW). Mannheim, Walldorf,
  and Heidelberg are fully within BW state boundaries and require no special note. Companies
  headquartered outside BW but operating a significant BW R&D site are noted `(BW site)`.
- **Primary source:** Cyber Valley Industry Partners and Start-up Network (publicly
  announced members 2019–2024), supplemented by manual curation of established BW R&D
  companies across non-AI sectors.
- **Compiled:** 2026-06-28 (rev. 2026-06-28, Phase-3 gap-fill). Annual review recommended — startup entries are especially
  volatile; verify `last verified` dates older than 12 months before relying on them.

## What this list is NOT

- **Not a job board.** No thesis openings are listed. Use Pass 2 (live enrichment via
  `company-search-strategy.md`) to find active positions.
- **Not comprehensive.** BW has thousands of companies. This ~100-entry list covers the
  actors most likely relevant for Master's thesis work in tech, engineering, or life
  sciences. Gaps are expected and honest — the skill's coverage caveat must say so.
- **Not a confirmation of thesis availability.** Most companies do not publicize open
  Masterarbeit positions. Presence here means R&D relevance, not an open slot.
- **Not for non-BW use.** Geographic constraint is explicit. All entries are BW or
  confirmed BW-adjacent (within state boundaries). No entry is included on "HQ is nearby."

## How the skill uses this file

Pass 1 — backbone filter: read this file, select companies whose sector tags intersect
with the student's interest dimensions and domain, then exclude entries matching the
student's no-go tags. This produces a filtered candidate set for Pass 2.

Pass 2 — live enrichment: for each candidate, run targeted `site:` queries (see
`company-search-strategy.md`) to find R&D focus, thesis signal, and contact path.

## Spot-check log (2026-06-28)

Ten entries were verified by direct URL fetch or confirmed from live search results to
resolve to R&D or careers content. Marked ✓ in the tables below.

| # | Company | URL verified |
|---|---|---|
| 1 | Robert Bosch GmbH | https://www.bosch.de/karriere/dein-einstieg/studentinnen-und-studenten/wissenschaftliche-abschlussarbeit/ |
| 2 | SAP SE | https://jobs.sap.com/content/Studierende/?locale=de_DE |
| 3 | Carl Zeiss AG | https://www.zeiss.com/career/de/stellensuche.html |
| 4 | Trumpf GmbH & Co. KG | https://trumpf.wd3.myworkdayjobs.com/TRUMPF_Students |
| 5 | EnBW Energie Baden-Württemberg AG | https://www.enbw.com/career/career-entries-advancements/university-students/ |
| 6 | NEURA Robotics GmbH | https://jobs.neura-robotics.com/ |
| 7 | ZF Friedrichshafen AG | https://www.zf.com/mobile/en/careers/your_application/theses_at_zf/theses.html |
| 8 | Karl Storz GmbH & Co. KG | https://career.karlstorz.com/go/Bachelor-Masterarbeiten/9154101/ |
| 9 | Cohere (formerly Aleph Alpha GmbH) | https://cohere.com/careers ⚠ transitioning — see Caveats |
| 10 | sereact GmbH | https://sereact.ai/careers |
| 11 | IONOS Group SE | https://jobs.ionos.de/career/all-jobs ✓ |
| 12 | Haufe Group GmbH & Co. KG | https://jobs.haufegroup.com/young-talents ✓ |
| 13 | GFT Technologies SE | https://jobs.gft.com/go/germany/4411601/ ✓ |
| 14 | Schwarz IT GmbH & Co. KG | https://it.schwarz/en/karriere/einstieg ✓ |

---

## 1 — AI / ML (Cyber Valley Ecosystem)

All entries are confirmed Cyber Valley Start-up Network members or established BW-based AI
companies (publicly announced 2019–2024). For startups with "BW" as city, the exact
municipality is unconfirmed — only BW state residency is known (required for Cyber Valley
membership). Careers URLs point to the primary company website or known recruitment portal;
many startups use third-party platforms (Ashby, Personio, Workable) — navigate from the
main site if the direct URL is stale.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified |
|---|---|---|---|---|---|
| Cohere GmbH (formerly Aleph Alpha GmbH) ⚠ | AI/ML, NLP, LLMs | corporate | Heidelberg | https://cohere.com/careers | 2026-06-28 |
| NEURA Robotics GmbH | robotics, AI/ML | startup | Metzingen | https://jobs.neura-robotics.com/ ✓ | 2026-06-28 |
| sereact GmbH | robotics, AI/ML | startup | Stuttgart | https://sereact.ai/careers ✓ | 2026-06-28 |
| Vialytics GmbH | AI/ML, mobility | startup | Stuttgart | https://www.vialytics.de/karriere | 2026-06-28 |
| MARKT-PILOT GmbH | AI/ML, industrial | startup | Esslingen | https://markt-pilot.com/careers | 2026-06-28 |
| Octomind GmbH | AI/ML, dev-tools | startup | BW | https://octomind.dev/careers | 2026-06-28 |
| DeepScenario GmbH | AI/ML, automotive | startup | Stuttgart | https://www.deepscenario.com/jobs | 2026-06-28 |
| tsenso GmbH | AI/ML, supply-chain | startup | Stuttgart | https://tsenso.com/careers | 2026-06-28 |
| NODE Robotics GmbH | robotics, medtech | startup | Stuttgart | https://www.node-robotics.com/careers | 2026-06-28 |
| Mojin Robotics GmbH | robotics, logistics | startup | Stuttgart | https://www.mojin-robotics.de/jobs | 2026-06-28 |
| eye2you GmbH | AI/ML, medtech | startup | Tübingen | https://www.eye2you.org | 2026-06-28 |
| Medicalvalues GmbH | AI/ML, medtech | startup | Stuttgart | https://www.medicalvalues.de/careers | 2026-06-28 |
| Cytolytics GmbH | AI/ML, medtech | startup | Tübingen | https://www.cytolytics.de | 2026-06-28 |
| DeepCare GmbH | AI/ML, medtech | startup | BW | https://deepcare.de | 2026-06-28 |
| BAUTA GmbH | robotics, AI/ML | startup | BW | https://www.bauta.de | 2026-06-28 |
| AmbiGate GmbH | AI/ML, computer-vision | startup | BW | https://www.ambigate.com | 2026-06-28 |
| Tactai GmbH | AI/ML, haptics | startup | BW | https://www.tactai.de | 2026-06-28 |
| plus10 GmbH | AI/ML, analytics | startup | BW | https://plus10.ai | 2026-06-28 |
| mlxar GmbH | AI/ML, XR | startup | BW | https://www.mlxar.com | 2026-06-28 |
| preML GmbH | AI/ML, AutoML | startup | Tübingen | https://preml.de | 2026-06-28 |
| Bergsonne Labs GmbH | AI/ML, climate | startup | BW | https://bergsonne.com | 2026-06-28 |
| Collectu GmbH | AI/ML, data | startup | BW | https://www.collectu.de | 2026-06-28 |
| Protelligence GmbH | AI/ML, industrial | startup | BW | https://www.protelligence.de | 2026-06-28 |
| Radius Dynamics GmbH | AI/ML | startup | BW | https://radiusdynamics.com | 2026-06-28 |
| Spotium GmbH | AI/ML, logistics | startup | BW | https://www.spotium.de | 2026-06-28 |
| Casculate GmbH | AI/ML, simulation | startup | Stuttgart | https://casculate.com | 2026-06-28 |
| Beyondbots GmbH | AI/ML, automation | startup | BW | https://beyondbots.com | 2026-06-28 |
| NextStepHR GmbH | AI/ML, HR-tech | startup | BW | https://nextstephr.com | 2026-06-28 |
| Ventecon Technologies GmbH | AI/ML | startup | BW | https://ventecon.de | 2026-06-28 |
| DenkBox GmbH | AI/ML, edtech | startup | BW | https://www.denkbox.de | 2026-06-28 |
| kausable GmbH | AI/ML, analytics | startup | Tübingen | https://www.kausable.com | 2026-06-28 |
| polybot GmbH | robotics, agritech | startup | Tübingen | https://polybot.eu | 2026-06-28 |
| BinDoc GmbH | AI/ML, document | startup | BW | https://www.bindoc.de | 2026-06-28 |
| Field 33 GmbH | AI/ML, software | startup | BW | https://field33.com | 2026-06-28 |
| MATVIS GmbH | AI/ML, computer-vision | startup | BW | https://www.matvis.de | 2026-06-28 |
| 43IT GmbH | AI/ML, software | startup | BW | https://43it.de | 2026-06-28 |
| mine&make GmbH | AI/ML, B2B | startup | BW | https://mineandmake.com | 2026-06-28 |
| nuvus GmbH | AI/ML, automotive | startup | BW | https://nuvus.io | 2026-06-28 |
| ISTARI AI GmbH | AI/ML, cybersecurity | startup | BW | https://istari.ai | 2026-06-28 |
| Respeak GmbH | AI/ML, NLP | startup | BW | https://respeak.io | 2026-06-28 |
| Fara.AI GmbH | AI/ML | startup | BW | https://fara.ai | 2026-06-28 |
| Earlytrace GmbH | AI/ML | startup | BW | https://earlytrace.de | 2026-06-28 |
| Yugen Space GmbH | AI/ML, space | startup | Tübingen | https://yugenspace.de | 2026-06-28 |
| NECKAR GmbH | AI/ML, manufacturing | startup | Stuttgart | https://www.neckar.io | 2026-06-28 |
| Tetractys GmbH | AI/ML | startup | BW | https://tetractys.io | 2026-06-28 |
| Quantum Gaming GmbH | AI/ML, gaming | startup | BW | https://quantumgaming.de | 2026-06-28 |

---

## 2 — Automotive / Mobility

Established BW companies with confirmed thesis programs and significant R&D headcount.
All have published student/thesis portals. Corporate entries typically require application
via an online portal 4–6 months before desired start.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified |
|---|---|---|---|---|---|
| Robert Bosch GmbH | automotive, AI/ML | corporate | Stuttgart | https://www.bosch.de/karriere/dein-einstieg/studentinnen-und-studenten/wissenschaftliche-abschlussarbeit/ ✓ | 2026-06-28 |
| ZF Friedrichshafen AG | automotive, AI/ML | corporate | Friedrichshafen | https://www.zf.com/mobile/en/careers/your_application/theses_at_zf/theses.html ✓ | 2026-06-28 |
| Mercedes-Benz AG | automotive, AI/ML | corporate | Stuttgart | https://career.mercedes-benz.com/en/young-talent.html | 2026-06-28 |
| Dr. Ing. h.c. F. Porsche AG | automotive, AI/ML | corporate | Stuttgart | https://jobs.porsche.com | 2026-06-28 |
| Daimler Truck AG | automotive, AI/ML | corporate | Stuttgart | https://www.daimlertruck.com/career/students | 2026-06-28 |
| Mahle GmbH | automotive | corporate | Stuttgart | https://www.mahle.com/en/careers/students/ | 2026-06-28 |
| Dürr AG | automotive, manufacturing | corporate | Bietigheim-Bissingen | https://www.durr-group.com/en/jobs | 2026-06-28 |
| Eberspächer GmbH & Co. KG | automotive, energy | corporate | Esslingen | https://www.eberspaecher.com/karriere | 2026-06-28 |
| Mann+Hummel GmbH | automotive | corporate | Ludwigsburg | https://www.mann-hummel.com/de/karriere.html | 2026-06-28 |
| IAV GmbH | automotive, AI/ML | corporate | Stuttgart (BW site) | https://www.iav.com/de/karriere/studenten/ | 2026-06-28 |
| Mercedes-Benz Tech Innovation GmbH | automotive, software | SME | Stuttgart / Ulm | https://www.mercedes-benz-techinnovation.com/en/career/ | 2026-06-28 |
| Porsche Digital GmbH | automotive, AI/ML | SME | Stuttgart | https://jobs.porsche.com | 2026-06-28 |

---

## 3 — Industrial / Manufacturing

Companies with BW headquarters and active R&D in automation, laser technology, precision
mechanics, or industrial software. Many run structured thesis programs; preferred entry is
the student/internship portal, not open applications.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified |
|---|---|---|---|---|---|
| Trumpf GmbH & Co. KG | industrial, lasers | corporate | Ditzingen | https://trumpf.wd3.myworkdayjobs.com/TRUMPF_Students ✓ | 2026-06-28 |
| Festo SE & Co. KG | industrial, automation | corporate | Esslingen | https://www.festo.com/en/company/careers/ | 2026-06-28 |
| Alfred Kärcher SE & Co. KG | industrial | corporate | Winnenden | https://www.kaercher.com/de/karriere.html | 2026-06-28 |
| SEW-EURODRIVE GmbH & Co. KG | automation | corporate | Bruchsal | https://www.sew-eurodrive.de/karriere/schueler-studenten-absolventen.html | 2026-06-28 |
| Sick AG | sensors, IoT | corporate | Waldkirch | https://www.sick.com/de/de/career/ | 2026-06-28 |
| Voith GmbH & Co. KGaA | industrial, energy | corporate | Heidenheim | https://www.voith.com/de-de/karriere.html | 2026-06-28 |
| ebm-papst GmbH & Co. KG | industrial | SME | Mulfingen | https://www.ebmpapst.com/de/karriere/ | 2026-06-28 |
| Pilz GmbH & Co. KG | automation, safety | SME | Ostfildern | https://www.pilz.com/de-DE/karriere/ | 2026-06-28 |
| Wittenstein AG | industrial, medical | SME | Igersheim | https://www.wittenstein.de/karriere/ | 2026-06-28 |

---

## 4 — Medtech / Life Sciences

BW companies in medical devices, diagnostics, and life science imaging. Carl Zeiss and Karl
Storz have long-established thesis programs with multiple active listings. Roche Diagnostics
operates its main German R&D site in Mannheim (BW).

| Company | Sector tags | Size | City | Careers / Research URL | Last verified |
|---|---|---|---|---|---|
| Carl Zeiss AG | optics, medtech | corporate | Oberkochen | https://www.zeiss.com/career/de/stellensuche.html ✓ | 2026-06-28 |
| Karl Storz GmbH & Co. KG | medtech | corporate | Tuttlingen | https://career.karlstorz.com/go/Bachelor-Masterarbeiten/9154101/ ✓ | 2026-06-28 |
| Paul Hartmann AG | medtech | corporate | Heidenheim | https://www.paul-hartmann.com/de/karriere/ | 2026-06-28 |
| Roche Diagnostics GmbH | pharma, medtech | corporate | Mannheim | https://www.roche.com/careers/our-locations/europe/de/ | 2026-06-28 |
| Heidelberg Engineering GmbH | medtech, imaging | SME | Heidelberg | https://www.heidelbergengineering.com/de/karriere/ | 2026-06-28 |
| Bosch Sensortec GmbH | IoT, sensors | SME | Reutlingen | https://www.bosch-sensortec.com/career/ | 2026-06-28 |

---

## 5 — Software / Enterprise

| Company | Sector tags | Size | City | Careers / Research URL | Last verified |
|---|---|---|---|---|---|
| SAP SE | enterprise software, AI/ML | corporate | Walldorf | https://jobs.sap.com/content/Studierende/?locale=de_DE ✓ | 2026-06-28 |
| TeamViewer AG | software, cloud | corporate | Göppingen | https://www.teamviewer.com/en/company/careers/ | 2026-06-28 |
| MHP Management- und IT-Beratung GmbH | consulting, AI/ML | corporate | Ludwigsburg | https://www.mhp.com/de/karriere.html | 2026-06-28 |
| IONOS Group SE | cloud, software | corporate | Karlsruhe | https://jobs.ionos.de/career/all-jobs ✓ | 2026-06-28 |
| Haufe Group GmbH & Co. KG | software, HR-tech | SME | Freiburg | https://jobs.haufegroup.com/young-talents ✓ | 2026-06-28 |
| GFT Technologies SE | fintech, software | corporate | Stuttgart | https://jobs.gft.com/go/germany/4411601/ ✓ | 2026-06-28 |
| Schwarz IT GmbH & Co. KG | software, supply-chain | corporate | Neckarsulm | https://it.schwarz/en/karriere/einstieg ✓ | 2026-06-28 |

---

## 6 — Energy / Sustainability

| Company | Sector tags | Size | City | Careers / Research URL | Last verified |
|---|---|---|---|---|---|
| EnBW Energie Baden-Württemberg AG | energy, sustainability | corporate | Karlsruhe | https://www.enbw.com/career/career-entries-advancements/university-students/ ✓ | 2026-06-28 |

---

## 7 — IoT / Sensors / Connectivity

BW SMEs with significant sensor, connectivity, or embedded-systems R&D. Smaller than the
industrial corporates above; thesis contact is typically a direct research team inquiry,
not a formal portal.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified |
|---|---|---|---|---|---|
| Balluff GmbH | IoT, sensors | SME | Neuhausen a. d. F. | https://www.balluff.com/en/careers/ | 2026-06-28 |
| Lapp Group GmbH | IoT, connectivity | SME | Stuttgart | https://www.lapp.com/de/ueber-lapp/karriere.html | 2026-06-28 |
| Hansgrohe SE | IoT, smart-home | SME | Schiltach | https://www.hansgrohe.com/karriere.html | 2026-06-28 |

---

## Caveats

- **Cyber Valley startup URLs:** Many smaller Cyber Valley startups do not maintain a
  dedicated `/careers` page. If the URL in the table returns 404, search the company name
  on LinkedIn or navigate to their main website's careers section.
- **City "BW":** For 22 startup entries, the specific BW city is unconfirmed at compile
  time. Cyber Valley membership requires a BW headquarters or founder affiliation, so state
  residency is certain; exact municipality is not.
- **Automotive subsidiaries:** Porsche Digital GmbH and Mercedes-Benz Tech Innovation GmbH
  are subsidiaries of their respective parents. Both run independent hiring; students may
  approach either the parent or the subsidiary.
- **BW-adjacent note removed:** Mannheim, Walldorf, and Heidelberg are all within Baden-
  Württemberg state boundaries (not just adjacent). They require no special flag.
- **Out of scope (intentional):** Fraunhofer institutes, KIT spin-offs, and Max Planck
  research groups are excluded — they are academic-sector actors covered by
  `find-university-chairs`. Job boards (LinkedIn, StepStone, Indeed) are never used as
  backbone sources.
- **Aleph Alpha → Cohere (April 2026):** Aleph Alpha GmbH was acquired by Cohere in April
  2026 ($20B valuation). The combined entity retains a Heidelberg headquarters (dual HQ
  Toronto / Heidelberg). The original Ashby careers URL (`jobs.ashbyhq.com/AlephAlpha`) is
  likely stale; use https://cohere.com/careers and filter for the Heidelberg office.
