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
- **Compiled:** 2026-06-28 (rev. 2026-07-04, Task L — extended to all Uni Tübingen faculties). Annual review recommended — startup entries are especially
  volatile; verify `last verified` dates older than 12 months before relying on them.
- **Thesis-Kultur column:** `bekanntes Programm ✓` means a live-confirmed, thesis-specific
  page or listing was found (not just a generic careers/dual-study page); `unklar` is the
  honest default everywhere else — it does not mean no thesis program exists, only that
  none was confirmed at compile time. Never upgrade `unklar` to `✓` without a fresh URL check.

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

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Cohere GmbH (formerly Aleph Alpha GmbH) ⚠ | AI/ML, NLP, LLMs | corporate | Heidelberg | https://cohere.com/careers | 2026-06-28 | unklar |
| NEURA Robotics GmbH | robotics, AI/ML | startup | Metzingen | https://jobs.neura-robotics.com/ ✓ | 2026-06-28 | unklar |
| sereact GmbH | robotics, AI/ML | startup | Stuttgart | https://sereact.ai/careers ✓ | 2026-06-28 | unklar |
| Vialytics GmbH | AI/ML, mobility | startup | Stuttgart | https://www.vialytics.de/karriere | 2026-06-28 | unklar |
| MARKT-PILOT GmbH | AI/ML, industrial | startup | Esslingen | https://markt-pilot.com/careers | 2026-06-28 | unklar |
| Octomind GmbH | AI/ML, dev-tools | startup | BW | https://octomind.dev/careers | 2026-06-28 | unklar |
| DeepScenario GmbH | AI/ML, automotive | startup | Stuttgart | https://www.deepscenario.com/jobs | 2026-06-28 | unklar |
| tsenso GmbH | AI/ML, supply-chain | startup | Stuttgart | https://tsenso.com/careers | 2026-06-28 | unklar |
| NODE Robotics GmbH | robotics, medtech | startup | Stuttgart | https://www.node-robotics.com/careers | 2026-06-28 | unklar |
| Mojin Robotics GmbH | robotics, logistics | startup | Stuttgart | https://www.mojin-robotics.de/jobs | 2026-06-28 | unklar |
| eye2you GmbH | AI/ML, medtech | startup | Tübingen | https://www.eye2you.org | 2026-06-28 | unklar |
| Medicalvalues GmbH | AI/ML, medtech | startup | Stuttgart | https://www.medicalvalues.de/careers | 2026-06-28 | unklar |
| Cytolytics GmbH | AI/ML, medtech | startup | Tübingen | https://www.cytolytics.de | 2026-06-28 | unklar |
| DeepCare GmbH | AI/ML, medtech | startup | BW | https://deepcare.de | 2026-06-28 | unklar |
| BAUTA GmbH | robotics, AI/ML | startup | BW | https://www.bauta.de | 2026-06-28 | unklar |
| AmbiGate GmbH | AI/ML, computer-vision | startup | BW | https://www.ambigate.com | 2026-06-28 | unklar |
| Tactai GmbH | AI/ML, haptics | startup | BW | https://www.tactai.de | 2026-06-28 | unklar |
| plus10 GmbH | AI/ML, analytics | startup | BW | https://plus10.ai | 2026-06-28 | unklar |
| mlxar GmbH | AI/ML, XR | startup | BW | https://www.mlxar.com | 2026-06-28 | unklar |
| preML GmbH | AI/ML, AutoML | startup | Tübingen | https://preml.de | 2026-06-28 | unklar |
| Bergsonne Labs GmbH | AI/ML, climate | startup | BW | https://bergsonne.com | 2026-06-28 | unklar |
| Collectu GmbH | AI/ML, data | startup | BW | https://www.collectu.de | 2026-06-28 | unklar |
| Protelligence GmbH | AI/ML, industrial | startup | BW | https://www.protelligence.de | 2026-06-28 | unklar |
| Radius Dynamics GmbH | AI/ML | startup | BW | https://radiusdynamics.com | 2026-06-28 | unklar |
| Spotium GmbH | AI/ML, logistics | startup | BW | https://www.spotium.de | 2026-06-28 | unklar |
| Casculate GmbH | AI/ML, simulation | startup | Stuttgart | https://casculate.com | 2026-06-28 | unklar |
| Beyondbots GmbH | AI/ML, automation | startup | BW | https://beyondbots.com | 2026-06-28 | unklar |
| NextStepHR GmbH | AI/ML, HR-tech | startup | BW | https://nextstephr.com | 2026-06-28 | unklar |
| Ventecon Technologies GmbH | AI/ML | startup | BW | https://ventecon.de | 2026-06-28 | unklar |
| DenkBox GmbH | AI/ML, edtech | startup | BW | https://www.denkbox.de | 2026-06-28 | unklar |
| kausable GmbH | AI/ML, analytics | startup | Tübingen | https://www.kausable.com | 2026-06-28 | unklar |
| polybot GmbH | robotics, agritech | startup | Tübingen | https://polybot.eu | 2026-06-28 | unklar |
| BinDoc GmbH | AI/ML, document | startup | BW | https://www.bindoc.de | 2026-06-28 | unklar |
| Field 33 GmbH | AI/ML, software | startup | BW | https://field33.com | 2026-06-28 | unklar |
| MATVIS GmbH | AI/ML, computer-vision | startup | BW | https://www.matvis.de | 2026-06-28 | unklar |
| 43IT GmbH | AI/ML, software | startup | BW | https://43it.de | 2026-06-28 | unklar |
| mine&make GmbH | AI/ML, B2B | startup | BW | https://mineandmake.com | 2026-06-28 | unklar |
| nuvus GmbH | AI/ML, automotive | startup | BW | https://nuvus.io | 2026-06-28 | unklar |
| ISTARI AI GmbH | AI/ML, cybersecurity | startup | BW | https://istari.ai | 2026-06-28 | unklar |
| Respeak GmbH | AI/ML, NLP | startup | BW | https://respeak.io | 2026-06-28 | unklar |
| Fara.AI GmbH | AI/ML | startup | BW | https://fara.ai | 2026-06-28 | unklar |
| Earlytrace GmbH | AI/ML | startup | BW | https://earlytrace.de | 2026-06-28 | unklar |
| Yugen Space GmbH | AI/ML, space | startup | Tübingen | https://yugenspace.de | 2026-06-28 | unklar |
| NECKAR GmbH | AI/ML, manufacturing | startup | Stuttgart | https://www.neckar.io | 2026-06-28 | unklar |
| Tetractys GmbH | AI/ML | startup | BW | https://tetractys.io | 2026-06-28 | unklar |
| Quantum Gaming GmbH | AI/ML, gaming | startup | BW | https://quantumgaming.de | 2026-06-28 | unklar |

---

## 2 — Automotive / Mobility

Established BW companies with confirmed thesis programs and significant R&D headcount.
All have published student/thesis portals. Corporate entries typically require application
via an online portal 4–6 months before desired start.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Robert Bosch GmbH | automotive, AI/ML, ux-research | corporate | Stuttgart | https://www.bosch.de/karriere/dein-einstieg/studentinnen-und-studenten/wissenschaftliche-abschlussarbeit/ ✓ | 2026-06-28 | bekanntes Programm ✓ |
| ZF Friedrichshafen AG | automotive, AI/ML | corporate | Friedrichshafen | https://www.zf.com/mobile/en/careers/your_application/theses_at_zf/theses.html ✓ | 2026-06-28 | bekanntes Programm ✓ |
| Mercedes-Benz AG | automotive, AI/ML, ux-research | corporate | Stuttgart | https://career.mercedes-benz.com/en/young-talent.html | 2026-06-28 | unklar |
| Dr. Ing. h.c. F. Porsche AG | automotive, AI/ML | corporate | Stuttgart | https://jobs.porsche.com | 2026-06-28 | unklar |
| Daimler Truck AG | automotive, AI/ML | corporate | Stuttgart | https://www.daimlertruck.com/career/students | 2026-06-28 | unklar |
| Mahle GmbH | automotive | corporate | Stuttgart | https://www.mahle.com/en/careers/students/ | 2026-06-28 | unklar |
| Dürr AG | automotive, manufacturing | corporate | Bietigheim-Bissingen | https://www.durr-group.com/en/jobs | 2026-06-28 | unklar |
| Eberspächer GmbH & Co. KG | automotive, energy | corporate | Esslingen | https://www.eberspaecher.com/karriere | 2026-06-28 | unklar |
| Mann+Hummel GmbH | automotive | corporate | Ludwigsburg | https://www.mann-hummel.com/de/karriere.html | 2026-06-28 | unklar |
| IAV GmbH | automotive, AI/ML | corporate | Stuttgart (BW site) | https://www.iav.com/de/karriere/studenten/ | 2026-06-28 | unklar |
| Mercedes-Benz Tech Innovation GmbH | automotive, software | SME | Stuttgart / Ulm | https://www.mercedes-benz-techinnovation.com/en/career/ | 2026-06-28 | unklar |
| Porsche Digital GmbH | automotive, AI/ML | SME | Stuttgart | https://jobs.porsche.com | 2026-06-28 | unklar |
| Bosch eBike Systems (Robert Bosch GmbH) | sport, AI/ML, ux-research | corporate | Reutlingen / Kusterdingen | https://www.bosch.de/karriere/dein-einstieg/studentinnen-und-studenten/wissenschaftliche-abschlussarbeit/ ✓ | 2026-07-04 | bekanntes Programm ✓ |

---

## 3 — Industrial / Manufacturing

Companies with BW headquarters and active R&D in automation, laser technology, precision
mechanics, or industrial software. Many run structured thesis programs; preferred entry is
the student/internship portal, not open applications.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Trumpf GmbH & Co. KG | industrial, lasers | corporate | Ditzingen | https://trumpf.wd3.myworkdayjobs.com/TRUMPF_Students ✓ | 2026-06-28 | unklar |
| Festo SE & Co. KG | industrial, automation | corporate | Esslingen | https://www.festo.com/en/company/careers/ | 2026-06-28 | unklar |
| Alfred Kärcher SE & Co. KG | industrial | corporate | Winnenden | https://www.kaercher.com/de/karriere.html | 2026-06-28 | unklar |
| SEW-EURODRIVE GmbH & Co. KG | automation | corporate | Bruchsal | https://www.sew-eurodrive.de/karriere/schueler-studenten-absolventen.html | 2026-06-28 | unklar |
| Sick AG | sensors, IoT | corporate | Waldkirch | https://www.sick.com/de/de/career/ | 2026-06-28 | unklar |
| Voith GmbH & Co. KGaA | industrial, energy | corporate | Heidenheim | https://www.voith.com/de-de/karriere.html | 2026-06-28 | unklar |
| ebm-papst GmbH & Co. KG | industrial | SME | Mulfingen | https://www.ebmpapst.com/de/karriere/ | 2026-06-28 | unklar |
| Pilz GmbH & Co. KG | automation, safety | SME | Ostfildern | https://www.pilz.com/de-DE/karriere/ | 2026-06-28 | unklar |
| Wittenstein AG | industrial, medical | SME | Igersheim | https://www.wittenstein.de/karriere/ | 2026-06-28 | unklar |

---

## 4 — Medtech / Life Sciences

BW companies in medical devices, diagnostics, and life science imaging. Carl Zeiss and Karl
Storz have long-established thesis programs with multiple active listings. Roche Diagnostics
operates its main German R&D site in Mannheim (BW).

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Carl Zeiss AG | optics, medtech | corporate | Oberkochen | https://www.zeiss.com/career/de/stellensuche.html ✓ | 2026-06-28 | unklar |
| Karl Storz GmbH & Co. KG | medtech | corporate | Tuttlingen | https://career.karlstorz.com/go/Bachelor-Masterarbeiten/9154101/ ✓ | 2026-06-28 | bekanntes Programm ✓ |
| Paul Hartmann AG | medtech | corporate | Heidenheim | https://www.paul-hartmann.com/de/karriere/ | 2026-06-28 | unklar |
| Roche Diagnostics GmbH | pharma, medtech | corporate | Mannheim | https://www.roche.com/careers/our-locations/europe/de/ | 2026-06-28 | unklar |
| Heidelberg Engineering GmbH | medtech, imaging | SME | Heidelberg | https://www.heidelbergengineering.com/de/karriere/ | 2026-06-28 | unklar |
| Bosch Sensortec GmbH | IoT, sensors | SME | Reutlingen | https://www.bosch-sensortec.com/career/ | 2026-06-28 | unklar |

---

## 5 — Software / Enterprise

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| SAP SE | enterprise software, AI/ML | corporate | Walldorf | https://jobs.sap.com/content/Studierende/?locale=de_DE ✓ | 2026-06-28 | unklar |
| TeamViewer AG | software, cloud | corporate | Göppingen | https://www.teamviewer.com/en/company/careers/ | 2026-06-28 | unklar |
| MHP Management- und IT-Beratung GmbH | consulting, AI/ML | corporate | Ludwigsburg | https://www.mhp.com/de/karriere.html | 2026-06-28 | unklar |
| IONOS Group SE | cloud, software | corporate | Karlsruhe | https://jobs.ionos.de/career/all-jobs ✓ | 2026-06-28 | unklar |
| Haufe Group GmbH & Co. KG | software, HR-tech, verlag | SME | Freiburg | https://jobs.haufegroup.com/young-talents ✓ | 2026-06-28 | unklar |
| GFT Technologies SE | fintech, software, consulting | corporate | Stuttgart | https://jobs.gft.com/go/germany/4411601/ ✓ | 2026-06-28 | unklar |
| Schwarz IT GmbH & Co. KG | software, supply-chain | corporate | Neckarsulm | https://it.schwarz/en/karriere/einstieg ✓ | 2026-06-28 | unklar |

---

## 6 — Energy / Sustainability / Environment / Geosciences

Extended 2026-07-04 (Task L) to cover the Umwelt/Energie/Geowissenschaften employment
field — previously only EnBW (and one AI/ML-tagged climate startup) represented this space.
Two entries are state research/agency bodies rather than private companies (ZSW, LUBW);
included because they run genuine, confirmed student research programs and are the strongest
BW-based fit for Geowissenschaften/Umwelttechnik students, not because the backbone's
"companies only" framing has changed — flagged explicitly so the skill can note this to students.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| EnBW Energie Baden-Württemberg AG | energy, sustainability | corporate | Karlsruhe | https://www.enbw.com/career/career-entries-advancements/university-students/ ✓ | 2026-06-28 | unklar |
| Zentrum für Sonnenenergie- und Wasserstoff-Forschung Baden-Württemberg (ZSW) ⚠ state research institute | energy, sustainability, geo | SME | Stuttgart / Ulm | https://www.zsw-bw.de/en/career.html ✓ | 2026-07-04 | unklar |
| Landesanstalt für Umwelt Baden-Württemberg (LUBW) ⚠ state agency | umwelt, geo | SME | Karlsruhe | https://karriere.lubw.de/en/studium ✓ | 2026-07-04 | bekanntes Programm ✓ |
| Endress+Hauser (Maulburg / Weil am Rhein) (BW site) | sensors, umwelt, IoT | corporate | Maulburg | https://www.endress.com/de/de-karriere/ihre-moeglichkeiten ✓ | 2026-07-04 | unklar |

---

## 7 — IoT / Sensors / Connectivity

BW SMEs with significant sensor, connectivity, or embedded-systems R&D. Smaller than the
industrial corporates above; thesis contact is typically a direct research team inquiry,
not a formal portal.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Balluff GmbH | IoT, sensors | SME | Neuhausen a. d. F. | https://www.balluff.com/en/careers/ | 2026-06-28 | unklar |
| Lapp Group GmbH | IoT, connectivity | SME | Stuttgart | https://www.lapp.com/de/ueber-lapp/karriere.html | 2026-06-28 | unklar |
| Hansgrohe SE | IoT, smart-home | SME | Schiltach | https://www.hansgrohe.com/karriere.html | 2026-06-28 | unklar |

---

## 8 — Chemie / Materialwissenschaft

Added 2026-07-04 (Task L) — previously a hard gap (0 entries) despite Chemie and
Pharmazie & Biochemie being full Fachbereiche of the Science faculty. Sourced via
family-business job portals and direct company sites, not job boards.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Freudenberg Technology Innovation SE & Co. KG (Freudenberg Group) | chemie, materials | corporate | Weinheim | https://jobs.freudenberg.com/freudenberg/ ✓ | 2026-07-04 | bekanntes Programm ✓ |
| Wieland-Werke AG | materials | corporate | Ulm | https://www.wieland.com/en/career/entry-options/students/ ✓ | 2026-07-04 | bekanntes Programm ✓ |
| Carl Roth GmbH + Co. KG | chemie | SME | Karlsruhe | https://www.carlroth.com/de/de/Karriere ✓ | 2026-07-04 | unklar |
| Schill+Seilacher GmbH | chemie, materials | SME | Böblingen | https://www.schillseilacher.de/en/ ✓ | 2026-07-04 | unklar |
| Zeller+Gmelin GmbH & Co. KG | chemie | SME | Eislingen | https://zeller-gmelin.de/en/career/ ✓ | 2026-07-04 | unklar |

---

## 9 — Wirtschaft / Finance / Consulting / Versicherung

Added 2026-07-04 (Task L). MHP Management- und IT-Beratung GmbH and GFT Technologies SE
already cover part of this field from Section 5 (Software / Enterprise) — see the
Studiengangs-Routing table below for the cross-reference. Still under the 5-entry target
(4 total across both sections); documented honestly rather than padded — see the Task L
gap-analysis findings doc for why (structural: Wirtschaftswissenschaft graduates in BW
mostly enter corporate finance/insurance functions, not open-ended R&D thesis roles).

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Wüstenrot & Württembergische AG (W&W Gruppe) | versicherung, consulting | corporate | Stuttgart | https://www.ww-ag.com/de/karriere ✓ | 2026-07-04 | unklar |
| Landesbank Baden-Württemberg (LBBW) | finance | corporate | Stuttgart | https://www.lbbw.de/menschen/karriere/karriere-bei-der-lbbw/karriere_7wo376iug_d.html ✓ | 2026-07-04 | unklar |

---

## 10 — Sozialwissenschaften / Marktforschung / Politik

Added 2026-07-04 (Task L). **Honest structural gap:** despite a diverse-source search
(general web search, market-research-industry directories), only one credible BW-based
market/social-research company with a public careers path survived live verification.
Most Soziologie/Politikwissenschaft/Empirische-Kulturwissenschaft graduates in BW go into
public-sector, NGO, or academic research roles that this company-only backbone does not
cover — route these students to `find-university-chairs` as a complement, not a substitute.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| ipi Institute für Produkt-Markt-Forschung GmbH | marktforschung | SME | Stuttgart | https://ipi.de/en/jobs/ ✓ | 2026-07-04 | unklar |

---

## 11 — Bildung / EdTech

Added 2026-07-04 (Task L). DenkBox GmbH already carries an `edtech` tag in Section 1
(AI/ML) — cross-reference via the Studiengangs-Routing table rather than duplicating the
row. Still thin (2 entries total); BW has very few dedicated EdTech companies outside the
Klett/Cornelsen publishing houses (Cornelsen is Berlin-HQ'd, out of scope).

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Ernst Klett Verlag (Klett Gruppe) | edtech, verlag | corporate | Stuttgart | https://ernst-klett-verlag.de/karriere/ ✓ | 2026-07-04 | unklar |

---

## 12 — Medien / Verlage / Sprache / Kultur

Added 2026-07-04 (Task L). Klett (above, also Bildung/EdTech) and Haufe Group (Section 5,
software/HR-tech with publishing heritage) both cross-reference here. No dedicated
language-industry company (translation/localization) survived a diverse search — a genuine
gap for FB4 Neuphilologie / FB2 Asien-Orient-Wissenschaften graduates; note this honestly
to students rather than force a weak entry.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Motor Presse Stuttgart GmbH & Co. KG | verlag, medien | SME | Stuttgart | https://www.motorpresse.de/karriere-digital/ ✓ | 2026-07-04 | unklar |

---

## 13 — Sport / Gesundheitstechnologie

Added 2026-07-04 (Task L). Bosch eBike Systems (Section 2, tagged `sport`) is the
strongest entry and cross-references here. Thin field overall (2 entries); most
sport-adjacent R&D in BW is really medtech/wearables R&D already captured in Section 4.

| Company | Sector tags | Size | City | Careers / Research URL | Last verified | Thesis-Kultur |
|---|---|---|---|---|---|---|
| Erbe Elektromedizin GmbH | medtech, sport | SME | Tübingen | https://www.erbegroup.com/de-de/karriere ✓ | 2026-07-04 | unklar |

---

## Studiengangs-Routing

Maps each Uni Tübingen employment field (see the Task L taxonomy in
`findings/no_db_universal_skill/2026-07-04-taskL-taxonomy-and-gap-analysis.md` §2 for the
full Fachbereich-level derivation) to the backbone sections and sector tags that serve it.
Use this table as the entry point for Pass 1 instead of scanning every section by hand.

| Beschäftigungsfeld | Typische Interessen | Relevante Sektionen / Tags | Hinweise |
|---|---|---|---|
| Informatik & Data/AI | ML, NLP, Robotik, Software Engineering | §1 AI/ML; §5 Software/Enterprise (`AI/ML`) | Best-covered field; already above the 30% backbone-share target (see gap-analysis §5) — no further growth needed here |
| Ingenieurnahe Systeme (Automotive/Fertigung/IoT) | Eingebettete Systeme, Fahrzeugtechnik, Sensorik | §2 Automotive/Mobility; §3 Industrial/Manufacturing; §7 IoT/Sensors | Tübingen has no engineering Fakultät — mainly relevant for Physik/Informatik/Mathematik-Studierende mit Systemschwerpunkt |
| Medtech/Pharma/Biotech/Life-Science | Medizintechnik, Diagnostik, Bildgebung, Wirkstoffe | §4 Medtech/Life Sciences; `medtech`-tagged rows in §1 | Direkter Fit für Pharmazie & Biochemie, Biologie |
| Chemie/Materialwissenschaft | Prozess-/Werkstoffchemie, Materialentwicklung | §8 Chemie/Materialwissenschaft (`chemie`, `materials`) | Neu 2026-07-04; deckt Chemie-Fachbereich ab |
| Psychologie (Wirtschaftspsych/UX/HR) | Nutzerforschung, Organisationspsychologie, HR-Analytics | `ux-research`-tagged rows (Bosch, Bosch eBike Systems, Mercedes-Benz); `HR-tech`-tagged rows (Haufe, NextStepHR) in §1/§2/§5 | **Klinische Psychologie hat keinen Firmen-Track** — dafür `find-university-chairs` (Medizinische Fakultät Kliniken) prüfen |
| Bildung/EdTech | Lernmedien, digitale Bildung | §11 Bildung/EdTech; `edtech`-tagged DenkBox GmbH in §1 | Dünn (2 Einträge) — ehrlich kommunizieren |
| Umwelt/Energie/Geowissenschaften | Energiewende, Umweltmesstechnik, Geodaten | §6 Energy/Sustainability/Environment/Geosciences | Enthält zwei Landesinstitutionen (ZSW, LUBW) statt reiner Unternehmen — im Output kennzeichnen |
| Wirtschaft/Finance/Consulting/Versicherung | Consulting, Banking, Versicherung | §9 Wirtschaft/Finance/Consulting/Versicherung; `consulting`-tagged MHP, GFT in §5 | Unter dem 5er-Ziel (4 gesamt) — dokumentierte strukturelle Lücke |
| Sozialwissenschaften/Marktforschung/Politik | Umfrageforschung, Politikanalyse | §10 Sozialwissenschaften/Marktforschung | Größte strukturelle Lücke (1 Eintrag) — `find-university-chairs` als Ergänzung nennen |
| Medien/Verlage/Sprache/Kultur | Verlagswesen, Sprachindustrie, Kulturvermittlung | §12 Medien/Verlage/Sprache/Kultur; `verlag`-tagged Klett (§11), Haufe (§5) | Keine dedizierte Sprachindustrie-Firma gefunden — ehrliche Lücke für Neuphilologie/Asien-Orient-Wissenschaften |
| Recht/Legal Tech | Rechtsinformatik, Digitalisierung der Justiz | — (keine verifizierten Einträge) | **Explizite Lücke** — Jura-Masterarbeit in einer Firma ist strukturell unüblich (Staatsexamen); kein Kandidat hat die Live-Verifikation bestanden |
| Sport/Gesundheitstechnologie | Wearables, Reha-Technologie, Sport-Engineering | §13 Sport/Gesundheitstechnologie; `sport`-tagged Bosch eBike Systems in §2 | Dünn (2 Einträge); überschneidet sich stark mit Medtech |
| Theologie/Philosophie/Religionswissenschaft/Geisteswissenschaften ohne Firmenbezug | Systematische Theologie, Religionswissenschaft, Philosophie, Alter Orient | — (keine Einträge, absichtlich) | **Kein Firmen-Track existiert.** Diese Studierenden ausschließlich auf `find-university-chairs` verweisen, nicht auf diesen Skill |

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
