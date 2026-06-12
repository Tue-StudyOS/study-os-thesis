# Product Positioning & Narrative

**StudyOS Thesis Advisor — Research Package, Report 3 of 5**
**Date:** 2026-06-11

---

## 1. The Problem We're Actually Solving

**Not:** "Professors want easier topic management."
The feedback is unambiguous — most don't (Report 1). Butz has "no problems getting students." Macke "does not see the added value." Luxburg: "profs never update the topics. We've had many attempts in the department already."

**Yes:** "Students waste weeks finding the right advisor, and professors drown in misdirected inquiries."
Evidence from the professors themselves:

- Menth supervises 20 theses, received inquiries for **50+**, regrets every rejection ("Es tut mir um jede Ablehnung leid"), and explicitly wishes for "a system with which students can more easily get to theses… then maybe I won't be so buried in inquiries."
- Macke's lab gets "a number of expressions of interest which is way larger than we can supervise."
- Winther: students saw 4–5 listed topics, assumed that was the whole lab, "and then did not talk to us" — bad information made matching *worse*.

Both sides lose to the same failure: **low-signal first contact.** Students contact the wrong chairs with generic emails; chairs spend time rejecting. The fix is better-prepared students, not more listings.

---

## 2. Why the Platform Approach Is Harder Than It Seems

Four independent failure modes, each confirmed by feedback:

1. **The incentive problem.** Listing more topics → more applications → more rejections → chairs regret listing (Macke, Menth, Hennig's 2022 precedent). Hennig: getting incentives right "doesn't have much to do with the interface or the frontend… It's all about the internal dynamics of the CS department."
2. **Tool fatigue.** Chairs already juggle 8+ systems (Macke's list: ILIAS, Alma, Nextcloud, Teams, Slack, Discord, ZDV mail, GitLab, Typo3…). A new login with new access-rights management is a cost before it delivers any value.
3. **The stability worry.** Hennig named a specific corpse: courses.cs.uni-tuebingen.de, built by "very engaged" HiWis, decayed the moment they left. "The website must be stable for at least a few years (i.e., also after you are long gone)." We cannot currently make that guarantee, and professors know it.
4. **The co-creation belief.** For a large bloc (Berens, Winther, Stephan, Bob, Luxburg), pre-listed topics aren't just impractical — they're *pedagogically wrong*. Bob: "the formulation of the question is actually the most important and difficult part of doing the thesis." No UI fixes a philosophical objection.

---

## 3. What We're Actually Building (reframed)

Three layers, in strict priority order:

### Layer 1 — For students (the product)
A chat agent that helps a student:
- **Formulate** their interests and constraints (transcript upload → competency profile),
- **Discover** which chairs actually work on relevant problems (semantic matching over scraped public data — publications, group pages, research-area statements),
- **Prepare** a high-signal first contact: a context summary of who they are, what they can do, and why this chair specifically.

This is the existing codebase. It requires **zero professor participation** to deliver value.

### Layer 2 — For chairs (optional, later)
Not a management dashboard. Three light touchpoints, each matching an explicit request:
- **Keywords/research areas, not project inventories** (Häufle, Bob, Niels, Mario) — data that "would not need revision very often" (Bob).
- **Pull from existing websites** instead of asking for input (Macke's counter-proposal; Ostermann's ps.cs.uni-tuebingen.de already has the data). This is PR #37.
- **Export back out** — listings portable to group websites (Huson's condition).
- **Hard rule: no reminder emails by default.** (Macke; Wichmann wants frequency "under user control" — default zero.)

### Layer 3 — For the department (read-only)
An aggregated, searchable view of research areas across all chairs — built from Layer 2 data and scraping, browsable by students. No chair workflow attached. Each chair page carries Bob's suggested disclaimer, roughly: *"These are starting points only. An essential part of doing a thesis is the formulation and refinement of the problem itself."*

---

## 4. How This Answers the Feedback

| Professors said | We now offer |
|---|---|
| "Don't build a system we have to use" (Macke, Stephan) | A student tool; chairs are passive data sources by default |
| "Read our existing website instead" (Macke, Ostermann) | Scraping agent (#37) is the core ingestion path |
| "Topics are co-created, not browsed" (Winther, Berens, Bob) | We surface *research areas + people*, and coach students toward conversation, not topic shopping |
| "Too many misdirected inquiries" (Menth, Macke, Butz) | Better-matched, better-prepared students → fewer cold low-signal emails |
| "Will it exist in 3 years?" (Hennig, Zell) | Layer 1 needs no chair investment, so abandonment costs chairs nothing; their websites remain the source of truth |
| "Spam / scoop risk" (Carsten, Georg) | We aggregate only already-public data; any chair-submitted content can be Uni-Tübingen-only |

The alignment story in one sentence: **students get better discovery, professors get fewer but better inquiries, the department gets visibility — and nobody is forced to maintain anything.**

---

## 5. Success Metrics (post-MVP)

- **Student:** "I contacted the right chair on my first attempt" — measure via the planned survey (Plan.docx weeks 29–1.07): time-to-first-meaningful-contact, number of chairs contacted before a match.
- **Professor:** "Inquiries I receive are better-informed" — qualitative; ask the 2–3 friendly Type B chairs (Wichmann, Huson, Kerstin offered goodwill).
- **Department:** more successful matches, fewer bounce-arounds.
- **Explicitly NOT a metric: professor adoption of the platform.** That was the old narrative; the feedback killed it. Chair opt-in (Layer 2) is a bonus signal, not a success criterion.

The MVP bar stays as written in Plan.docx: *after less than one hour with the tool, a student has a much better idea which chair to contact.* Everything above serves that sentence.
