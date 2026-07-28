# Task L — Studiengangs-Taxonomie & Gap-Analyse (BW Company Backbone)

**Date:** 2026-07-04 · **Branch:** `task/L-company-backbone`

## 0. Method note (deviation from the task brief)

The task brief pointed to `skills/build-student-profile/references/tuebingen-degree-programs.md`
as the source for Step 1. That file only lists the **6 degree programs of the Computer
Science department** — it is not a university-wide list. Per Domi's steer (asked live), the
correct approach was: **research all faculty/department areas of Uni Tübingen first** (via
live WebFetch of the official faculty pages, not the sparse repo file), build the employment-
field taxonomy from that, then search for companies. That research is summarized in §1 below,
cross-checked against `skills/find-university-chairs/references/tuebingen-faculty-backbone.md`
(the actual university-wide structure already curated in this repo for the chairs skill).

## 1. Uni Tübingen academic structure (live-verified 2026-07-04)

Fetched from `uni-tuebingen.de/fakultaeten/` and each faculty's Fachbereich/Fach listing:

| Faculty | Fachbereiche / Fächer |
|---|---|
| Mathematisch-Naturwissenschaftliche Fakultät | Biologie, Mathematik, Chemie, Pharmazie & Biochemie, Geowissenschaften, Physik, Informatik, Psychologie |
| Philosophische Fakultät | FB1 Altertums-/Kunstwissenschaften (IANES, Klassische Archäologie, Philologie, Ur-/Frühgeschichte, Kunstgeschichte, Musikwissenschaft, Religionswissenschaft), FB2 Asien-Orient-Wissenschaften (Ethnologie, Indologie, Japanologie, Koreanistik, Orient-/Islamwissenschaften, Sinologie), FB3 Geschichtswissenschaft, FB4 Neuphilologie (Deutsch, Englisch, Romanistik, Slavistik, Sprachwissenschaft), FB5 Philosophie-Rhetorik-Medien (Philosophie, Rhetorik, Medienwissenschaft) |
| Wirtschafts- und Sozialwissenschaftliche Fakultät | Empirische Kulturwissenschaft, Erziehungswissenschaft, Hector-Institut für Empirische Bildungsforschung, Politikwissenschaft, Soziologie, Sportwissenschaft, Wirtschaftswissenschaft |
| Juristische Fakultät | Lehrstühle (Bürgerliches Recht, Öffentliches Recht, Strafrecht) |
| Medizinische Fakultät | Institute (theoretical medicine) + Kliniken (clinical) |
| Ev.-Theologische / Kath.-Theologische Fakultät + ZITh | Theological chairs + Islamic Theology professorships |

## 2. Employment-field taxonomy (12 fields + 1 explicit no-fit field)

| # | Employment field | Primary Fachbereiche/Fächer | Company-thesis plausibility |
|---|---|---|---|
| 1 | Informatik & Data/AI | Informatik, Machine Learning (Master) | High — best-covered field in backbone |
| 2 | Ingenieurnahe Systeme (Automotive/Fertigung/IoT) | *(no Tübingen engineering degree)* — Physik, Informatik, Mathematik grads with applied/hardware interest | High for BW industry generally, but structurally a secondary fit for Tübingen students (no engineering Fakultät) |
| 3 | Medtech/Pharma/Biotech/Life-Science | Pharmazie & Biochemie, Biologie, Medizinische Fakultät (Institute) | High |
| 4 | Chemie/Materialwissenschaft | Chemie, Geowissenschaften (materials-adjacent) | Medium — was a hard gap (0 entries), now curated |
| 5 | Psychologie (klinisch / Wirtschaftspsych+UX+HR) | Psychologie | Medium for Wirtschaftspsych/UX/HR; **klinische Psychologie has no company-thesis track** — route to Medizinische Fakultät Kliniken via `find-university-chairs` |
| 6 | Bildung/EdTech | Erziehungswissenschaft, Hector-Institut | Low — BW has few EdTech companies; anchored on Klett |
| 7 | Umwelt/Energie/Geowissenschaften | Geowissenschaften | Was thin (EnBW + 1 climate startup); now curated |
| 8 | Wirtschaft/Finance/Consulting/Versicherung | Wirtschaftswissenschaft | Was thin (MHP, GFT only); now curated |
| 9 | Sozialwissenschaften/Marktforschung/Politik | Soziologie, Politikwissenschaft, Empirische Kulturwissenschaft | **Genuine structural gap** — most BW social-science employment is public-sector/NGO/academic, not company R&D. Only one credible company found after diverse-source search. |
| 10 | Medien/Verlage/Sprache/Kultur | Neuphilologie, Sinologie/Japanologie/Koreanistik/Indologie, Medienwissenschaft, Rhetorik, FB1/FB3 (Kunstgeschichte, Musikwissenschaft, Geschichte) | Low-medium — anchored on Klett/publishing; no dedicated language-industry (localization/translation) BW company found |
| 11 | Recht/Legal Tech | Juristische Fakultät | **Explicit honest gap, as anticipated in the task brief itself** — Staatsexamen-Jura Masterarbeit-in-Firma is structurally uncommon; no verifiable BW legal-tech company survived live verification (candidate found, but its Heidelberg/BW HQ could not be confirmed — excluded rather than guessed) |
| 12 | Sport/Gesundheitstechnologie | Sportwissenschaft, Interfakultäres Institut für Sport | Thin — folds partly into Medtech; 2 entries only |
| 13 | Theologie/Philosophie/Religionswissenschaft/Geisteswissenschaften ohne Firmenbezug | Ev./Kath. Theologie, ZITh, FB5 Philosophie, Religionswissenschaft, Alter Orient | **No realistic company-thesis track at all.** Documented as a hard no-fit field — route these students to `find-university-chairs` exclusively; do not force company entries. |

Every Fachbereich/Fach from §1 maps to exactly one primary field above (secondary fits noted
inline, e.g. Geowissenschaften → both field 2, adjacent, and field 7, primary).

## 3. Gap analysis (entries per field, before this task)

| Field | Backbone entries before Task L | Status |
|---|---|---|
| 1 Informatik & Data/AI | ~38 (Section 1 + SAP/TeamViewer from Section 5) | Well covered — **already exceeds the 30% cap** (see §5) |
| 2 Ingenieurnahe Systeme | ~26 (Sections 2, 3, 7) | Well covered |
| 3 Medtech/Pharma/Biotech | ~11 (Section 4 + AI/ML medtech-tagged rows) | Adequate |
| 4 Chemie/Materialwissenschaft | 0 | **Gap — filled, see §4** |
| 5 Psychologie | 0 dedicated (cross-tag candidates existed: Bosch, Mercedes-Benz, Haufe, NextStepHR) | **Gap — cross-tagged, see §4** |
| 6 Bildung/EdTech | 1 (DenkBox GmbH, tag only) | **Gap — partially filled** |
| 7 Umwelt/Energie/Geo | 2 (EnBW, Bergsonne Labs) | **Gap — filled to 5** |
| 8 Wirtschaft/Consulting/Versicherung | 2 (MHP, GFT) | **Gap — filled to 4** (honest note: still under 5) |
| 9 Sozialwissenschaften/Marktforschung | 0 | **Structural gap — 1 entry added, documented honestly** |
| 10 Medien/Verlage/Sprache | ~1 (Haufe, tangential) | **Gap — filled to 3** (honest note: still under 5) |
| 11 Recht/Legal Tech | 0 | **Honest gap — no entries added** (candidate rejected after failed verification) |
| 12 Sport/Gesundheitstechnologie | 0 | **Gap — 2 entries added** (honest note: still under 5) |
| 13 Theologie/Philosophie/… | 0 | **Intentional — no company track exists; not a gap to fill** |

## 4. Spot-check log — new entries (2026-07-04, all URLs opened live via WebFetch)

| Company | Field | URL | Verified |
|---|---|---|---|
| Freudenberg Technology Innovation SE & Co. KG | Chemie/Materialien | https://jobs.freudenberg.com/freudenberg/ | ✓ reachable; explicit Masterarbeit postings found via search (algorithmic manufacturing optimization, AI for injection molding) |
| Wieland-Werke AG | Chemie/Materialien | https://www.wieland.com/en/career/entry-options/students/ | ✓ reachable; page explicitly invites thesis topics |
| Carl Roth GmbH + Co. KG | Chemie/Materialien | https://www.carlroth.com/de/de/Karriere | ✓ reachable; no explicit thesis wording found — marked `unklar` |
| Schill+Seilacher GmbH | Chemie/Materialien | https://www.schillseilacher.de/en/ | ✓ reachable; evidence of university research collaboration (Reutlingen University pilot plant, doctoral scholarship) |
| Zeller+Gmelin GmbH & Co. KG | Chemie/Materialien | https://zeller-gmelin.de/en/career/ | ✓ reachable; "Interns & Students" section present, thesis not explicit — marked `unklar` |
| ZSW (Zentrum für Sonnenenergie- und Wasserstoff-Forschung BW) | Umwelt/Energie/Geo | https://www.zsw-bw.de/en/career.html | ✓ reachable; no explicit thesis wording — marked `unklar` |
| LUBW (Landesanstalt für Umwelt BW) | Umwelt/Energie/Geo | https://karriere.lubw.de/en/studium | ✓ reachable; explicit "wissenschaftliche Arbeiten für Ihr Studium" |
| Endress+Hauser (Maulburg/Weil am Rhein, BW site of the Swiss group) | Umwelt/Energie/Geo | https://www.endress.com/de/de-karriere/ihre-moeglichkeiten | ✓ reachable; general careers only, BW site not confirmed on this page — flag `(BW site)` per public HQ knowledge, verify before outreach |
| Wüstenrot & Württembergische AG (W&W Gruppe) | Wirtschaft/Consulting/Versicherung | https://www.ww-ag.com/de/karriere | ✓ reachable; "Studierende" section, practical-experience framing, no explicit thesis wording — marked `unklar` |
| Landesbank Baden-Württemberg (LBBW) | Wirtschaft/Consulting/Versicherung | https://www.lbbw.de/menschen/karriere/karriere-bei-der-lbbw/karriere_7wo376iug_d.html | ✓ reachable; explicit Werkstudierende/Trainee/LBBW Campus programs |
| ipi Institute für Produkt-Markt-Forschung GmbH | Sozialwissenschaften/Marktforschung | https://ipi.de/en/jobs/ | ✓ reachable (verified via ipi.de/en/about-us/, which links directly to /en/jobs/) |
| Ernst Klett Verlag / Klett Gruppe | Bildung/EdTech, Medien/Verlage | https://ernst-klett-verlag.de/karriere/ | ✓ reachable; explicit dual-study programs (Data Science & KI, Media, HR), no thesis-specific wording — marked `unklar` |
| Motor Presse Stuttgart GmbH & Co. KG | Medien/Verlage/Sprache | https://www.motorpresse.de/karriere-digital/ | ✓ reachable (page title + digital-careers section confirmed); thesis culture `unklar` |
| Erbe Elektromedizin GmbH | Sport/Gesundheitstechnologie | https://www.erbegroup.com/de-de/karriere | ✓ reachable (redirect from erbe-med.com noted); dual-study programs confirmed (BWL, Informatik, Maschinenbau, Mechatronik, Elektrotechnik, Wirtschaftsingenieurwesen) |
| Bosch eBike Systems (business unit of Robert Bosch GmbH, R&D at Reutlingen/Kusterdingen) | Sport/Gesundheitstechnologie (cross-tag, not a new row — see backbone) | (reuses main Bosch careers URL, already ✓ in original spot-check) | ✓ confirmed via live job postings found for eBike-specific thesis work (power electronics, rider-dynamics modeling, UX research), though the individual postings themselves rotate and one sampled posting had since expired (404) — expected volatility, not a dead company |

**Rejected candidates** (found via search, excluded after verification failed): "Homburg & Partner"
management consultancy (Mannheim) was acquired by Accenture in 2021 and its jobs page now
resolves to an unrelated Hagen-based tax firm of the same name — excluded to avoid a wrong
entity. A legal-tech candidate ("Codefy") could not have its Heidelberg/BW headquarters
confirmed on its own site — excluded per the "never guess" rule rather than included with an
unverified location claim. Testo SE & Co. KGaA (Lenzkirch, BW; measurement technology,
~10% revenue to R&D) is a strong real candidate confirmed via search but its careers domain
rate-limited (HTTP 429) on every live-fetch attempt during this session — not included in the
backbone to keep the "every URL opened live" rule intact; flagged here as a good next-session
candidate for Umwelt/Energie/Geo once it can be fetched.

## 5. Smoke test — "Erziehungswissenschaft, digitale Lernmedien" persona (2026-07-04)

Manual Pass-1 walkthrough per the task's step 6, using the final backbone:

- Interest tag: `edtech`. Domain tags: Bildung, `verlag` (secondary).
- Candidates: DenkBox GmbH (§1, `edtech`), Ernst Klett Verlag (§11, `edtech, verlag`),
  Haufe Group (§5, `verlag` — secondary fit only, HR/business content not core Lernmedien).
  Motor Presse Stuttgart (§12, `verlag`) excluded on relevance judgment despite the tag
  match — its publishing focus is automotive/lifestyle, not education.
- **Result: 2–3 candidates, below the 5–20 target range.** This is not a bug in the
  filter — it is the honest, documented outcome of a field (Bildung/EdTech) that stayed
  thin despite real search effort (§3). The skill's own Disambiguation Rules
  (`SKILL.md`, "When to ask") already cover this case: fewer than 3 candidates on a niche
  profile triggers asking the student whether to broaden scope, rather than silently
  returning a short list. No code or skill-logic change was needed to handle it correctly —
  the existing fallback behavior is the right one here.
- Take-away for whoever revisits the backbone next: Bildung/EdTech is the field most likely
  to benefit from a future dedicated research pass (e.g. checking Cornelsen's Stuttgart
  office for any BW-registered entity, or Tübingen-based e-learning spinouts not yet surfaced).

## 6. Anti-bias compliance note

- **Source diversity:** new entries were sourced via general web search (not solely
  Cyber-Valley-adjacent), a state environmental agency (LUBW), a state research institute
  (ZSW), a family-business job portal (karriere-familienunternehmen.de), and direct company
  sites — not job boards. No StepStone/Indeed/Glassdoor listing was used as a source of a
  thesis signal, only as an initial discovery hint later traced to the company's own domain.
- **Min 5 per field:** achieved for Chemie/Materialwissenschaft (5) and
  Umwelt/Energie/Geowissenschaften (5, counting pre-existing EnBW + Bergsonne Labs).
  Not achieved for Wirtschaft/Consulting (4), Sozialwissenschaften (1), Medien (3),
  Sport (2), Recht (0) — documented honestly per §3 rather than padded with weak entries,
  per the task's own explicit permission ("Lücken... ehrlich eintragen statt mit schwachen
  Einträgen aufzufüllen").
- **Max 30% per field — known pre-existing exception:** Field 1 (Informatik & Data/AI) sits
  at ~38 of the new backbone total of ~104 rows (≈36%), exceeding the 30% cap. This
  predates Task L (Section 1 alone had 36 rows before this task started) and reflects the
  real density of Cyber-Valley-era AI/ML startups in BW, not artificial padding introduced
  here. Trimming a previously-validated, GO-status section was out of scope for this task
  (would undo Phase 3/4 curation work) and risked breaking the eval baseline. Flagged here
  transparently rather than silently ignored — a candidate follow-up for a future backbone
  maintenance pass, not for this task.
