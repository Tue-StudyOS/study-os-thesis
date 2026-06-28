# Task I — Live Validation Results (real recall, real baseline)

- **Date:** 2026-06-28
- **Branch:** `feat/no-db-universal-skill`
- **Protocol:** [2026-06-28-live-validation-protocol.md](2026-06-28-live-validation-protocol.md)
- **Method:** Manual, in-conversation. For each faculty, a persona was built from the
  ground-truth *sample interest* only (taken from STATUS / README, **not** the chair
  lists). The **skill arm** followed `find-university-chairs/SKILL.md` end-to-end with
  live `WebSearch`/`WebFetch`. The **baseline arm** was a clean plain-Claude prompt with
  one generic web search, no skill files. Ground-truth chair lists were opened **only
  after** all 8 arm outputs were written. No peeking.
- **Artifacts:** `dist/live-validation/{medicine,psychology,wiso,cs}-{skill,baseline}.md`

---

## Two scoring lenses (why both are reported)

The README metric is **name-surfacing**: a GT chair counts if the output names the
professor *or* unambiguously names their group, **correctly attributed**. I report that
as the **primary recall**. But it has a built-in optimism: the GT files were themselves
built by crawling the faculty *Arbeitsbereiche / Lehrende* pages, and the skill's Pass 1
crawls those **same pages** — so "surfacing" a unit can just mean "both the GT author and
the skill read the same org chart." To expose what the skill actually *did with* that
list, I also report **strict recall** = GT chair surfaced as a *recommended, correctly
attributed* option (not merely echoed in the Pass-1 enumeration). The gap between the two
is the real story.

---

## Per-faculty results

### Primary recall (name-surfaced, correct attribution required)

| Faculty | GT chairs | Skill recall | Baseline recall | Delta |
|---|---|---|---|---|
| Medicine | 6 | **6/6 = 100%** | 1/6 = 17% | +83pp |
| Psychology | 6 | **4/6 = 67%** | 0/6 = 0% | +67pp |
| WiSo | 7 | **7/7 = 100%** | 2/7 = 29% | +71pp |
| CS | 5 | **3/5 = 60%** | 1/5 = 20% | +40pp |
| **Mean** | | **≈ 82%** | **≈ 17%** | **+65pp** |

### Strict recall (recommended & correctly attributed as a relevant option)

| Faculty | Skill (strict) | Note |
|---|---|---|
| Medicine | 5/6 ≈ 83% | Gasser & Jucker = correct top picks; Lerche/Siegel/Tabatabai correctly listed as adjacent (off-persona); only Ziemann not carried into the option map. |
| Psychology | 1/6 ≈ 17% | Only Bartels recommended correctly. Nürk's unit **misattributed**; Huff/Svaldi/Gawrilow appear only in the Pass-1 enumeration; Friedrich missed. |
| WiSo | 7/7 = 100% | All seven named as options with correct attribution (incl. Diez/Hasenclever flagged off-core). |
| CS | 3/5 = 60% | Hein, von Luxburg, Hennig recommended; Bethge named. Schölkopf & Martius missed. |
| **Mean** | **≈ 65%** | |

Baseline strict ≈ baseline primary (≈17%): plain Claude named Ziemann (med),
Schlumberger + Abels (wiso), Hein (cs), and nothing matching the psychology GT.

---

## What was found vs. missed (honest detail)

**Medicine — strongest result.** The Pass-1 backbone crawl of the HIH research page
returned the exact 7-department structure, which *is* the GT (the GT was built from the
same HIH page). Persona-relevant top picks (Gasser, Jucker) were correct; the skill also
correctly surfaced Lerche, Siegel, Tabatabai (and flagged Tabatabai as off-topic
oncology). It additionally found genuinely relevant non-GT groups (Synofzik, Schöls,
Heutink, Deleidi) — good discovery breadth. Baseline found only Ziemann + generic HIH/DZNE
pointers.

**WiSo — strong and genuine.** Crawling the IfP *Lehrende* page + the VWL chair list
surfaced all 7 GT chairs by name, including the two pure-economics chairs (Müller, Baten)
as adjacent options and Diez/Hasenclever as flagged off-core. The persona steered the
ranking well (Schlumberger, Bieling, Abels on top). Baseline named only Schlumberger and
Abels (via program pages).

**Psychology — real weakness.** Primary recall (67%) is propped up by Pass-1 enumeration:
the skill listed the correct Arbeitsbereich names but only correctly *recommended* one GT
chair (Bartels). It **misattributed** "Diagnostik und Kognitive Neuropsychologie" to
Hans-Otto Karnath (HIH neuropsychology) when the FB-Psychologie chair is **Hans-Christoph
Nürk** — a correctness bug that would send a student to the wrong professor. It missed
Claudia Friedrich's group ("Entwicklung der Sprachverarbeitung") and never resolved
Huff / Svaldi / Gawrilow to people. Strict recall here is only 17%.

**CS — coverage gap on MPI-IS.** GT is a small, curated, MPI-IS-heavy seed (5 chairs). The
skill nailed the FB-Informatik ML chairs (Hein, von Luxburg, Hennig) and named Bethge via
the ELLIS/AI-Center leg, but **missed Bernhard Schölkopf (Empirical Inference)** and
**Georg Martius (Autonomous Learning)** — both MPI-IS-affiliated and not on the
FB-Informatik `forschung.html` page my Pass 1 crawled. The AI-Center search returned
Bethge/Akata/Berens/Geiger/Hennig but not Schölkopf/Martius/Brendel. The MPI-IS / Cyber
Valley leg was under-crawled.

---

## Comparison to the fixture-mode numbers

| | Medicine | Psychology | WiSo | CS | Mean | Baseline |
|---|---|---|---|---|---|---|
| **Fixture (Task H)** | 83% | 100% | 100% | 100% | **96%** | **0%** |
| **Live primary (Task I)** | 100% | 67% | 100% | 60% | **82%** | **17%** |
| **Live strict (Task I)** | 83% | 17% | 100% | 60% | **65%** | **17%** |

- The fixture **96%** was optimistic; live primary is **82%**, live strict **65%**.
- The fixture **0% baseline was a strawman**: real plain-Claude scores **~17%** — it does
  name some correct chairs (Ziemann, Schlumberger, Abels, Hein).
- Psychology and CS, both "100%" in fixtures, are the two live underperformers.
- The **real, defensible advantage over plain Claude is ~+65pp** (primary) — large and
  meaningful, but not the fictional +96pp.

---

## Did the profile actually steer the search?

Yes, visibly. In WiSo the persona pushed Schlumberger/Bieling/Abels to the top and pushed
IR/peace chairs (Diez, Hasenclever) and the globalization-ethics chair into off-core /
no-go buckets. In Medicine it correctly demoted oncology (Tabatabai) and elevated
Gasser/Jucker. The baseline arms, lacking the profile + backbone, defaulted to "here are
the big programs/institutes" and named far fewer specific chairs. So the skill's structure
adds real value — the steering and the org-chart anchoring both work.

---

## Verdict on the revised Phase-1 gate

**Gate:** live coverage ≥70% **AND** a meaningful live margin over plain Claude.

**Verdict: AMBER — conditionally passed.**

- ✅ **Aggregate met:** mean primary recall **82% ≥ 70%**, with a **+65pp** margin over a
  *real* (not strawman) baseline. The skill clearly and genuinely beats plain Claude.
- ⚠️ **Per-faculty gaps:** 2 of 4 faculties miss 70% on primary (Psychology 67%, CS 60%).
- ⚠️ **Inflation caveat:** part of the high medicine/WiSo recall is *circular* — the GT was
  built from the same org pages the skill crawls. The stricter "recommended the right
  person" recall is only **65% mean**, and **Psychology is 17%**. That is the honest
  ceiling on person-level identification quality today.
- ❌ **One correctness bug:** the Karnath/Nürk misattribution in Psychology.

The university arm is good enough to proceed *in principle*, but **two fixes should land
before Phase 2** so we don't build companies on top of a skill that misnames supervisors:

1. **Person-level attribution discipline (Psychology bug).** When a unit is found, resolve
   the chair-holder from *that unit's own page*, and never borrow a name from a
   same-named-but-different group (HIH "Sektion Neuropsychologie" ≠ FB-Psychologie
   "Diagnostik und Kognitive Neuropsychologie"). Add a verification step: each named
   professor must be confirmed on the unit's own staff page.
2. **Explicit MPI-IS / ELLIS / Cyber Valley crawl leg (CS gap).** The FB-Informatik page
   alone misses MPI-IS chairs (Schölkopf, Martius, Brendel). Add these as first-class
   Pass-1 backbone sources in `search-strategy.md` §2 / the backbone file for any ML/AI
   or neuroscience persona.
3. (Nice-to-have) Don't let Pass-1 enumeration alone count as a "found" option — carry a
   unit into the map only once its PI and relevance are confirmed, so primary and strict
   recall converge.

After (1) and (2), re-run Psychology and CS live; if both clear 70% on the *strict* metric,
the gate is unambiguously green.
