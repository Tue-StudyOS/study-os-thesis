# Phase 2 — Company Discovery: Decisions

- **Date:** 2026-06-28
- **Status:** Resolved — feeding into `2026-06-28-phase2-build-plan.md`
- **Context:** Phase 1 gate is GREEN (all 4 Tübingen faculties ≥70% recall live). This doc
  resolves the two open decisions from STATUS.md before Phase 2 implementation begins.

---

## Decision 1 — Company Backbone Source

**Question:** Which existing, tagged list of BW companies serves as the backbone for
Phase 2 company discovery?

### Options evaluated

| Source | Coverage | Actuality | Machine-readable | License | Notes |
|---|---|---|---|---|---|
| **Cyber Valley Industry Partners** | ~80–100 AI/ML companies, Tübingen / Stuttgart area | Actively maintained (Cyber Valley e.V.) | Yes — HTML list on cybervalley.de/ecosystem/partners | Public web, no restriction | Best fit for AI/ML profiles; exactly the companies Tübingen CS students are likely to target |
| **bw_i (BW International)** | Several hundred BW companies, export-oriented | Moderate | Partial (HTML, no structured tags) | Public web | Too broad; tags are sector-size, not R&D focus; hard to curate to a useful small set |
| **IHK member directories (Reutlingen, Stuttgart)** | 50 000+ entries | Maintained | No (requires registration or has no export) | Gated | Too coarse; no R&D filter; cannot produce a curated 100-entry list without manual scraping |
| **Startups BW Top 100** | ~100 startups, annual list from Wirtschaftsministerium BW | Annual snapshot | Yes — PDF/HTML | Public | Useful supplement; many entries too young for thesis programs; volatile year-to-year |
| **Manual curation of known BW R&D companies** | ~20–30 established companies (Bosch, SAP, ZF, Zeiss, Trumpf, etc.) | Slow-moving (large companies) | N/A — we write it | N/A | Necessary to cover automotive, medtech, manufacturing profiles not served by Cyber Valley |

### Decision

**Primary backbone: Cyber Valley Industry Partners** — curated, AI/ML-tagged, BW-anchored,
publicly accessible, maintained by Cyber Valley e.V. Provides ~80–100 entries with implicit
sector tags (AI/ML/robotics) at the right granularity.

**Secondary layer: manual curation of ~20–30 established BW R&D companies** across sectors
not covered by Cyber Valley:
- Automotive / mobility: Bosch (Stuttgart), ZF Friedrichshafen, Mercedes R&D (Sindelfingen)
- Medtech / health: Carl Zeiss (Oberkochen), Karl Storz (Tuttlingen), Hartmann Group
- Software / enterprise: SAP (Walldorf), Software AG (Darmstadt — BW-adjacent)
- Industrial / manufacturing: Trumpf (Ditzingen), Festo (Esslingen), Kärcher (Winnenden)
- Energy / sustainability: SMA Solar (Niestetal — BW-adjacent), EnBW (Karlsruhe)

Combined backbone: **~100–130 entries**, each tagged with sector, size category, location, and
a careers URL. Small enough to be a maintainable Markdown file; wide enough to serve 90%+ of
realistic student profiles.

**NOT used:**
- IHK directories (too broad, gated, not filterable by R&D focus)
- bw_i comprehensive lists (sector tags too coarse, not R&D-centric)
- Startup-BW Top 100 as the sole source (too volatile; many startups lack established thesis programs)
- Any runtime-scraped job board (LinkedIn, StepStone, Indeed) — too noisy, can't be quality-filtered

**Why this is the one acceptable static asset:** there is no live-search equivalent for
discovering *which* BW companies have active thesis programs — company career pages are
inconsistently structured, many thesis openings are invisible publicly, and SEO-optimized
job boards return noise. The backbone solves the same cold-start problem the faculty backbone
solved for universities: it gives the discovery skill an anti-SEO-bias starting set anchored
to known, relevant actors.

---

## Decision 2 — Output Schema for Company Options Map

**Question:** What fields should each company entry in the output map contain? Which are
realistically fillable from live web? Which must be flagged as "may be missing"?

### Comparison with university output schema

| Field | University skill | Company equivalent | Availability |
|---|---|---|---|
| Entity name | Chair / Arbeitsbereich name | Company name + division/lab | Backbone (name always known) |
| URL | Official listing URL | Careers page or research team URL | Backbone; may need live enrichment |
| Person | Professor / lab head | R&D lead / thesis coordinator | **Often not public** |
| Research focus | Chair's active research areas | What the company R&D team actually works on | Live web, usually findable |
| Relevance rationale | Why it matches the profile | Same — tie to profile dimensions | Derived by skill |
| Thesis signal | Explicit opening or active thesis program | Job listing / "Abschlussarbeit" mention | **Unreliable** — often absent |
| Pros & difficulties | Supervision quality, group size, language | Culture fit, structure vs. startup chaos, confidentiality constraints | Partially inferable |
| Dated evidence | Publication / page date | Job listing date or "last updated" on careers page | Variable |
| Conversation starter | Email angle to the chair | Entry point (careers portal vs. cold email vs. R&D event) | Skill-derived |
| Coverage caveat | "chairs with weak web presence may be missing" | Extended: "most companies don't publicize thesis openings; proactive contact required" | Always present |

### Resolved output schema

Each company option in the map must include:

**Always present (from backbone or live enrichment):**
- `Company` — full company name
- `Division / team` — which business unit or R&D lab is relevant (e.g. "Bosch Center for AI", "SAP Labs Germany"); mark as `unknown` if not determinable
- `Sector tags` — from backbone (e.g. `[AI/ML, automotive]`)
- `Size category` — `startup` / `SME` / `corporate` (from backbone)
- `Location` — city + `(BW)` or `(BW-adjacent)` or `(remote-friendly)`
- `Relevance rationale` — why this matches the student's profile dimensions
- `Pros & likely difficulties` — honest: startup chaos vs. corporate bureaucracy, IP/confidentiality constraints, language of work (English / German), supervision model (industry supervisor only vs. co-supervision with uni)
- `Contact path` — how to actually approach: careers portal URL, direct email pattern if public, or "contact via R&D event / career fair"
- `Coverage caveat` (at map level, not per entry)

**Present only when found in live web (mark `not found` if absent):**
- `Research focus (live)` — what the R&D team actually works on, with dated evidence (2022+)
- `Thesis signal` — one of: `explicit opening` (a listed Masterarbeit / thesis position) / `active program` (careers page mentions Abschlussarbeit generally) / `unclear` (no public signal found)
- `Thesis coordinator / contact` — named person only when confirmed on the company's public page (never infer or guess)

**Never included:**
- Unpublicized application deadlines
- Salary / compensation information (not the scope of this skill)
- Named supervisor not publicly confirmed

### Coverage caveat (stronger than university version)

The map-level caveat for companies must be:

> "This map covers BW companies that publicly indicate R&D activity in your areas, based on a
> curated backbone (as of [date]) and live web enrichment. Most companies do NOT publicize
> open Masterarbeit positions — a 'no thesis signal found' does not mean there is no opening.
> For all entries marked 'unclear', proactive outreach (careers portal or direct R&D contact)
> is the recommended next step. The backbone is necessarily incomplete; new startups and
> divisions not yet in the list are a known gap."

---

## Risks and Limits vs. University Discovery

| Dimension | University (Phase 1) | Company (Phase 2) | Implication |
|---|---|---|---|
| **Thesis openings visibility** | Many chairs publish Masterarbeit topics publicly | Rare — most companies list only full-time jobs | Recall metric must be adapted; ≥70% may need to mean "surfaced the company", not "confirmed an open position" |
| **Named supervisor** | Professor is almost always publicly listed | Rarely public; thesis coordinator often only known internally | PI-verification step has no company equivalent; skill must not hallucinate contact names |
| **Org structure stability** | Chairs change slowly (professors have tenure) | Divisions merge, restructure frequently; startups may not exist in 2 years | Backbone entries need a "last verified" date; annual review recommended |
| **Quality of web presence** | All Tübingen chairs have at least an official listing | Startups may have no careers page; some companies hide R&D work | Coverage caveat must be stronger; backbone spot-check is essential |
| **SEO noise** | Uni pages are authoritative and distinguishable | "Bosch thesis" returns noisy job boards, not just official Bosch pages | Need explicit site: filters in query skeletons (site:bosch.com, site:sap.com, etc.) |
| **Live margin over plain Claude** | Proven: +65pp recall vs. baseline | Uncertain — plain Claude may know big company names already | Phase 2 eval must measure live margin; no assumption that the backbone adds value until proven |

---

## Explicit No-Gos for Phase 2

These are behaviors the Phase 2 skill must **not** do:

1. **No runtime company database** — backbone is a Markdown file, never a database or API call.
2. **No job-board scraping** (LinkedIn, StepStone, Indeed) — too noisy, inconsistently structured, and requires accounts/auth.
3. **No named supervisor attribution without public confirmation** — equivalent to the PI-verification rule in Phase 1; stronger here because company organizational info is less structured.
4. **No companies outside BW or without a BW R&D presence** — geographic constraint is explicit; "BW-adjacent" (e.g. SAP Walldorf just across the border from KA) is acceptable only with a note.
5. **No promise of thesis availability** — "thesis signal: unclear" is valid output; never invent an opening.
6. **No cross-posting to LinkedIn or career portals** — this is a read-only discovery skill.
7. **No attempt to cover all BW companies** — the backbone is purposefully small and curated; completeness is traded for relevance and maintainability.

---

## Relationship to `find-university-chairs`

Phase 2 introduces a new, parallel skill `find-company-thesis-options`. The existing
`find-university-chairs` remains as-is; a student (or orchestrating agent) can invoke both
in sequence. No renaming of `find-university-chairs` is planned — the STATUS.md open decision
("consider a faculty-agnostic rename once companies arrive") is **closed as "no rename for
now"**: the names are already descriptive of what each skill does.

The two skills share the same student profile format (6 dimensions) and the same option-map
output structure, making it easy to combine their outputs into a single student-facing view
later (Phase 3 / orchestration).
