---
name: find-company-thesis-options
description: Discover Masterarbeit options at BW companies — R&D teams, thesis programs, and contact paths — across all sectors represented in the Baden-Württemberg company backbone, for any discipline. Requires a deep student profile (all six dimensions) before searching. Use when a student asks which BW company, R&D lab, or industry team fits their interests, methods, domain, or thesis style for a company-supervised thesis. Distinct from find-university-chairs, which covers academic chairs at the University of Tübingen.
---

# Discover Company Thesis Options

Map a student's research interests to Master's thesis opportunities at **BW companies**
using a two-pass approach: (1) filter a curated backbone of ~100 BW companies by sector
tags, then (2) enrich each candidate with live web search. No runtime database —
the backbone is a Markdown file (curated, ~1x/year refresh) and the live web is the only
runtime source. Live enrichment in Pass 2 adds current context to all candidates.

## Prerequisites

This skill requires a **deep student profile** covering all six dimensions:

1. **Interests** — core research areas / topics
2. **Methods** — how the student wants to work (empirical ML, lab experiments, systems engineering, statistical modeling, …)
3. **Domain** — application field (automotive, healthcare, manufacturing, enterprise software, …)
4. **Thesis style** — preferred output type (applied/empirical, theoretical, engineering, survey, mixed)
5. **Skills** — concrete tools / competencies (Python, PyTorch, CAD, MATLAB, NLP frameworks, …)
6. **No-gos** — hard exclusions (pure hardware, clinical patient contact, non-technical roles, specific sectors, …)

**If any dimension is missing or shallow, stop here.** Call `build-student-profile` first
and complete the interview. Do not produce a company shortlist on a partial profile.

---

## Workflow

### Step 1 — Verify the profile

Check that the conversation contains profile answers for all six dimensions above.
If any is missing or the student has only given a one-liner ("I like AI"), invoke
`build-student-profile` and return here only after the profile is complete.

### Step 2 — Extract query variables

Extract the six dimensions from the profile. Using the mapping table in
[`references/company-search-strategy.md` §1](references/company-search-strategy.md),
populate these query variables:

- `{TOPIC_DE}`, `{TOPIC_EN}` — from Interests (both language forms)
- `{METHOD_DE}`, `{METHOD_EN}` — from Methods (both language forms)
- `{DOMAIN_DE}`, `{DOMAIN_EN}` — from Domain (both language forms)
- `{NOGO_TERM}` — from No-gos (one or more exclusion signals)

Note the student's thesis style and preferred company size (startup / corporate).
These inform the backbone filter and the pros/difficulties annotation.

### Step 3 — Pass 1: filter the backbone

**This step does not use the live web.** Read the backbone file and filter it.

1. Open [`references/bw-company-backbone.md`](references/bw-company-backbone.md) in full.
2. Apply the interest-to-tag mapping from
   [`references/company-search-strategy.md` §2.1](references/company-search-strategy.md):
   identify which backbone sections and rows match the student's interest and domain tags.
3. Apply the filtering logic from §2.2:
   - **Include** entries whose sector tags intersect the student's mapped tags.
   - **Expand** by including the entire relevant backbone section if the student's domain
     matches a section heading, then trim by tag intersection.
   - **Exclude (no-gos):** apply §6 exclusion rules now, before Pass 2, to avoid enriching
     incompatible companies. If a no-go is ambiguous (e.g. `robotics, AI/ML` and the
     no-go is "no hardware"), keep the entry and mark it with:
     `⚠ partial no-go conflict: verify whether role is software/ML or hardware before outreach`.
   - **Size filter (optional):** if thesis style signals startup preference, de-prioritize
     corporate entries (still include; rank lower). If structured supervision is preferred,
     de-prioritize startup entries.
4. For each selected entry record: company name, sector tags, size, city, careers/research URL,
   last-verified date.

Target candidate set size: **5–20 companies**. If > 20 result, tighten the tag intersection.
If < 5, broaden by one secondary tag or relax the size filter.

> **If a backbone URL is stale (404):** run
> `"{COMPANY_NAME}" Masterarbeit OR Abschlussarbeit` to find the current careers entry point.
> Update your working candidate list before starting Pass 2.

### Step 4 — Pass 2: live enrichment per company

For each candidate from Step 3, run the enrichment sub-passes from
[`references/company-search-strategy.md` §3](references/company-search-strategy.md)
using the query skeletons in §4:

- **2a — R&D focus:** does the company's own page confirm they work on the student's topic?
  Use `site:{COMPANY_DOMAIN} "{TOPIC_EN}" OR "{TOPIC_DE}" research OR Forschung`.
  For corporates with named labs (Bosch Center for AI, SAP Labs), target the lab sub-domain.
- **2b — Thesis signal:** is there a listed Masterarbeit / Abschlussarbeit position, a
  general thesis program, or no public signal? Use the thesis signal queries from §4.2.
  Classify as `explicit opening`, `active program`, or `unclear` (never leave blank).
- **2c — Contact path:** careers portal URL (from backbone), a named coordinator only if
  confirmed on the company's own page, or "direct R&D team inquiry — no portal found".
  Use the contact queries from §4.3. Never infer or guess a contact name.
- **2d — Recency evidence:** confirm R&D activity from 2022 or later. Use the recency
  queries from §4.4. Flag evidence older than 3 years as stale.
- **2e — Existence / activity check AND URL verification (FIRST CHECK):** open the company's main 
  domain and confirm it is still active. Check: page reachable (not 404 or parked), careers or 
  research section exists, at least one signal (news, job posting, publication, press release) from 
  2024 or later. If the company appears inactive, acquired, or renamed, mark the entry
  `⚠ existence not confirmed — verify before outreach` and rank it last. Do not silently drop it.
  **Record the status of every URL you open: reachable, 404, redirect, or parked.** This is the 
  first verification pass.

If a company's main domain is not indexed (`site:` returns nothing), use the fallback
queries from §4.5 before concluding the entry has weak web presence.

### Step 5 — Apply quality filters, dedup, and URL re-verification (SECOND CHECK)

Apply the quality filters from
[`references/company-search-strategy.md` §5](references/company-search-strategy.md):

- Prefer the company's own domain over job-board aggregators. Never use StepStone, Indeed,
  or Glassdoor as the source of a thesis signal.
- Date evidence required: accept evidence only from 2022 or later as recent.
- Prefer specificity: a page that explicitly names the student's topic outranks a page that
  says "we use AI" generically.
- For startup entries: verify the main domain is reachable and was updated within 24 months.
  If not, add `⚠ web presence not confirmed — verify before outreach`.
- Dedup: if the backbone and a live search both surface the same company unit, merge into
  one entry; do not create two entries for the same R&D team.

**URL Verification (SECOND CHECK — before final output):** Before including any contact URL, 
careers portal link, or R&D team page in the output, **open it again and verify it is still 
reachable**. Record the result (reachable / 404 / redirect / parked). Any URL that was reachable 
in Pass 2 but unreachable here must be marked with `⚠ contact URL not confirmed — verify before 
use` in the output and deprioritized (rank it lower than verified URLs). Never omit the URL — 
just annotate the problem so the student can attempt it anyway.

### Step 6 — Final no-go check

Before composing the option map, do a final pass over the enriched candidate set:

- Discard any entry that clearly violates a no-go based on what live enrichment revealed
  (e.g. a company tagged `IoT, sensors` that live enrichment confirms is hardware-only,
  and the student's no-go is "no hardware").
- For ambiguous cases flagged in Step 3, revise the annotation based on what Pass 2
  found. If the role is confirmed software/ML, clear the flag. If it confirmed hardware,
  discard.
- Do not silently drop borderline entries — if uncertain, keep and annotate.

### Step 7 — Produce the option map

Group the surviving entries by the student's **interest dimension** (not by backbone
section or company size). Example groupings:

- "Large Language Models / Enterprise NLP"
- "Computer Vision in Medical Imaging"
- "Autonomous Systems / Automotive AI"

If a company fits multiple interest groups, place it in the best-fit group and note the
secondary fit in the relevance rationale.

For each entry produce the fields described in the Output section below.

### Step 8 — Append the coverage caveat

After all entries, append the map-level caveat exactly as specified in the Output section.
Do not omit it. Company thesis discovery is structurally more opaque than university
discovery — the caveat is not optional boilerplate.

---

## Output

Produce a **map of options** grouped by interest dimension (not by company sector or size).

### Per-entry fields

**Always present** (from backbone or live enrichment):

- **Company** — full company name
- **Division / team** — which business unit or R&D lab is relevant (e.g. "Bosch Center for AI",
  "SAP Labs Germany", "Zeiss Meditec"); mark `unknown` if not determinable from live web
- **Sector tags** — from backbone (e.g. `[AI/ML, automotive]`)
- **Size** — `startup` / `SME` / `corporate`
- **Location** — city + `(BW)` or `(BW-adjacent)`
- **Relevance rationale** — why this matches the profile; tie to specific interests, domain,
  and method dimensions (not just "this company does AI")
- **Pros & likely difficulties** — honest: e.g. "structured thesis program, apply via portal
  4–6 months out; competitive"; "startup — informal supervision, IP/confidentiality
  constraints likely; close daily contact with team"; "English work environment; co-supervision
  with university not guaranteed"
- **Contact path** — careers portal URL, or "direct R&D team inquiry — no portal found",
  or "contact via career fair: {event name}"

**Present only when found in live web** (mark `not found` if absent):

- **Research focus (live)** — what the R&D team actually works on; must include a source URL
  and content date (2022 or later). If only a vague "we use AI" page was found, say so.
- **Thesis signal** — one of:
  - `explicit opening` — a listed Masterarbeit / thesis position found on the company's own
    page, with URL and date
  - `active program` — careers page mentions Abschlussarbeiten generally; no open position
    listed; program likely active
  - `unclear` — no public signal found; proactive outreach required. Include a size-aware 
    guidance: for **corporates** (Bosch, SAP, ZF, etc.), suggest checking the careers portal 
    and following up in 2 weeks if needed. For **startups and SMEs**, recommend **direct R&D 
    team inquiry** as faster and more effective (no HR queue).
- **Thesis coordinator / contact** — named person only when confirmed on the company's own
  public page; never inferred or guessed; omit if not confirmed

**Never included:**

- Unpublicized application deadlines
- Salary or compensation information
- Any named contact not publicly confirmed by the company itself

### Map-level coverage caveat (required — append once, at the top of the map)

> "This map covers BW companies that publicly indicate R&D activity in your areas, based on a
> curated backbone (as of [backbone date]) and live web enrichment. Most companies do NOT
> publicize open Masterarbeit positions — a 'thesis signal: unclear' does not mean there is
> no opening. For entries marked 'unclear': contact the careers portal for large corporates
> (follow up in 2 weeks if needed), or reach out directly to the R&D team at startups/SMEs
> (faster and more likely to get a response). The backbone is necessarily incomplete; new
> startups, emerging divisions, and niche companies not yet in the list are a known gap.
> If your profile is highly specialized, consider searching for '[your topic] BW unternehmen'
> or asking your advisor for companies they know directly."

---

## Evidence Rules

- Prefer the company's own domain as the authoritative source. Accept `cybervalley.de`
  as a secondary authority for Cyber Valley members. Accept `arxiv.org` / `ieee.org` for
  publication evidence only.
- **Never invent thesis openings, contact names, team sizes, or R&D topics.**
- **Never invent or guess URLs.** Every URL in the output must have been retrieved and
  confirmed reachable during this run. If a URL was not opened and verified, do not include it.
- **Every URL is verified twice:** (1) when first found (Pass 2 enrichment, sub-pass 2e) and 
  (2) again immediately before final output (Step 5 re-verification). A URL that was reachable 
  in Pass 2 but unreachable at Step 5 must appear in the output with a `⚠ contact URL not 
  confirmed — verify before use` flag and be ranked last (below confirmed URLs). A URL that was 
  never reachable must not appear in the output.
- **Never name a thesis coordinator or R&D contact unless they appear on the company's own
  public page.** Company organizational information is less structured than university faculty
  pages — inferring from a LinkedIn profile or a conference attendance list is not sufficient.
- Confirm the thesis coordinator on the company's own careers or team page before naming them.
  If not confirmable, write `thesis coordinator: not confirmed — contact via [careers portal URL]`.
- `thesis signal: unclear` is valid output. It does not represent a skill failure. Most
  companies do not publicize open Masterarbeit positions.
- Mark evidence older than 3 years as stale and flag it explicitly.
- For startups: if the main domain is unreachable or shows no updates for > 24 months,
  flag with `⚠ web presence not confirmed — verify company is active before outreach`.
- Do not use any bundled company, contact, or thesis seed files as a runtime source.
  The backbone + live web is the only authoritative source during discovery.

---

## No-Go Guard (hard stops)

Before producing any output, verify none of these apply:

1. **No runtime company database** — the backbone is a static Markdown file, not a database
   or API. If you find yourself constructing a database query, stop.
2. **No job-board scraping** — never use StepStone, Indeed, or Glassdoor as a thesis source.
   LinkedIn is acceptable only as a last-resort fallback signal; trace any finding to the
   official source before including.
3. **No named contact without public confirmation** — if you cannot link to the company's own
   page naming the person, do not name them.
4. **No companies outside BW** — geographic constraint is explicit. "BW-adjacent" (e.g.
   Walldorf, Mannheim, Heidelberg) is acceptable with a note only if the company is in the
   backbone. Do not expand scope.
5. **No promise of thesis availability** — never write "this company has an open thesis
   position" without a dated, on-domain URL confirming it. `thesis signal: unclear` is
   always a valid output.
6. **No cross-posting** — this is a read-only discovery skill. Do not submit applications,
   register accounts, or post to external services.
7. **No completeness claim** — the backbone is purposefully small and curated. Always append
   the coverage caveat; never claim the map is exhaustive.

---

## Disambiguation Rules

**When to proceed without asking:**

- The student profile is complete (all 6 dimensions present) → run the skill.
- A backbone URL is 404 → resolve via fallback query, document the new URL, and continue.
- A company's thesis signal is `unclear` → output it as `unclear`; do not ask for permission.
- A no-go is ambiguous → annotate with `⚠ partial no-go conflict` and keep the entry.

**When to ask:**

- A profile dimension is missing or one-liner shallow → stop and call `build-student-profile`.
- The backbone filter returns fewer than 3 candidates and the student's profile is highly
  niche (e.g. "deep tech for space") → ask whether the student wants to broaden the scope
  before continuing with a very short map.
- The student explicitly named a company not in the backbone and outside BW → ask whether
  they want BW-only discovery or want to expand scope.

---

## Self-Check Checklist

Before delivering the option map, verify:

- [ ] All 6 profile dimensions were present before starting
- [ ] Pass 1 was a backbone-file read only (no web search at Step 3)
- [ ] Every entry in the map came from the backbone candidate set (no ad-hoc SEO results)
- [ ] Every named contact or coordinator is linked to a company-owned page
- [ ] Every `thesis signal` field is one of `explicit opening`, `active program`, or `unclear`
      (never blank, never "probably", never invented)
- [ ] Date evidence for R&D focus is 2022 or later, or flagged as stale
- [ ] Startups with unverifiable web presence carry the `⚠ web presence not confirmed` flag
- [ ] No job-board aggregator was used as a thesis source
- [ ] The output is grouped by student interest dimension, not by backbone section
- [ ] The map-level coverage caveat is present at the top of the output, including guidance 
      for size-specific outreach (corporates vs. startups) and the acknowledgment of backbone gaps
- [ ] No no-go entry was silently dropped (discards are noted; ambiguous cases are annotated)
- [ ] Every URL in the output was opened and confirmed reachable twice: (1) in Pass 2 (sub-pass 2e) 
      and (2) again in Step 5 before final output. Any URL unreachable at Step 5 is marked with 
      `⚠ contact URL not confirmed` and ranked last
- [ ] URLs that were never reachable are not included in the output at all
- [ ] "Thesis signal: unclear" entries include concrete next-step guidance (e.g., "Try the careers 
      portal at [URL]" for corporates, or "Email r-and-d@company.com directly" for startups)
