# Detailed Analysis & Decision Log

**StudyOS Thesis Advisor — Research Package, Report 5 of 5**
**Date:** 2026-06-11 · **Audience:** internal team record
**Sources:** 27 professor responses (May 2026), StudyOS bot external review, live repo state (5 open PRs / 16 open issues, verified 2026-06-11), Plan.docx

---

## 1. Professor Feedback Deep Dive

### 1.1 Methodology note

Outreach went to chairs in two variants: chairs that already list topics publicly ("how is maintenance going?") and chairs that don't ("why not — including 'we don't want to'"). The second framing earned unusually candid answers; several professors thanked us for permission to be blunt. One response (Carsten, re: spam/scoop risk) was truncated in our records but its position is clear from the opening lines. A handful of responses are still in draft status on our side (marked "Draft geschrieben" in the source doc) — the analysis below treats received content uniformly, but we should track which threads still need a reply from us.

### 1.2 Type A — capacity-driven refusal (Butz, Menth, Mähl)

These chairs are demand-constrained in the opposite direction from what a listing platform assumes. Butz: "we have no problems getting students these days." Menth is the extreme case: 20 supervised theses against 50+ inquiries, generating topics "fast nur auf Anfrage" (almost only on request) and still not keeping up.

**Interpretation:** for these chairs, public visibility is strictly negative — it increases inbound volume they must reject. But Menth's closing paragraph is the most strategically interesting sentence in the dataset: *"Ich wäre sehr froh, wenn es ein System gäbe, mit dem Studierende leichter an Abschlussarbeiten kommen können. Dann werde ich vielleicht auch nicht so überhäuft mit Anfragen."* He rejects the mechanism (listing) while endorsing the outcome (students routed to the right place). A discovery tool that diverts students *away* from oversubscribed chairs toward chairs with capacity serves Type A without asking anything of them.

**Tension:** Menth says "there are simply no topics I could post" while also saying he generates topics on request. The topics exist — as latent capacity unlocked by the *right* student. This is the same co-creation dynamic Type C describes, arrived at from exhaustion rather than principle.

### 1.3 Type B — willing if trivial (Hennig, Zell, Kerstin, Georg, Huson, Wichmann, Bob/Rabanus, Anna)

The current state of the art among willing chairs is instructive:

- **Hennig:** a once-per-term "workshop" where PhD students each add one slide to a shared Overleaf beamer deck (8–15 topics/term). Currently outdated because the secretary coordinating it was absent. The freshness mechanism is elegant: PhD students are the listed contacts, so stale entries generate emails to them, "and that usually ensures they take the project down swiftly."
- **Zell:** estimates **>50% of supervised theses never appear on the list at all** — they emerge from PhD-student/student conversations. "I always have to run behind my Ph.D. students… now I only monitor it infrequently."
- **Kerstin:** internal Google Doc, sent to interested students on request, "hard to keep up-to-date."
- **Georg:** internal Overleaf list, "constantly moving and outdated," with a real constraint: topics are paper ideas, so visibility must be restricted to Uni Tübingen students.
- **Huson:** the cost is not the webpage edit — "the hard part is coming up with viable topics." Updates happen "ad hoc when too many students contact me asking about topics that are no longer relevant."

Even the *most cooperative* chairs describe systems that are chronically stale, and the staleness isn't tool-shaped: it's that topic generation is research work and topic lifecycle is invisible until students complain.

**Hennig's three conditions** deserve verbatim record because they are effectively our acceptance criteria for any Layer 2 work:
1. *Incentives:* "There absolutely must be a good incentive for the research groups to list theses there… This is something you likely won't get right as student developers, because it doesn't have much to do with the interface or the frontend."
2. *Friction:* "Updating the list must be easy, quick, and transparent."
3. *Stability:* "The website must be stable for at least a few years (i.e., also after you are long gone)" — citing courses.cs.uni-tuebingen.de as the cautionary precedent.

He also handed us a user-research roadmap: interview Luxburg, Grust, Martius. Luxburg independently offered a coffee chat after her SML lecture (Tue/Thu 8:15–9:45, MvL1). These invitations have a shelf life; we should use them in the next 2–3 weeks.

### 1.4 Type C — principled refusal (Macke, Luxburg, Berens, Winther, Stephan, Niels, Bob in part)

This group's objections are *experience-backed*, not hypothetical:

- **Winther ran the experiment and it failed in both directions:** "The topics that we wanted to work on urgently no student applied for. Students had the impression that the four or five topics we had published were the only thing we worked on and then did not talk to us." A static list simultaneously failed to fill urgent topics and *suppressed* organic contact. This is the strongest single argument against the catalogue model.
- **Luxburg has departmental history:** "an up-to-date platform doesn't work, profs never update the topics. We've had many attempts in the department already."
- **Macke's response is the richest in the dataset.** Three structural points: (a) maintenance "is really intellectual work that a tool only helps slightly with"; (b) topics "emerge pretty spontaneously and fluidly… not 'planned ahead of time'" and supervision is distributed across the lab, so any tool needs lab-level access management ("which group members of mine have write access") — overhead before value; (c) the systems-fatigue argument, with the memorable conclusion that he'd rather we *remove* a system than add one. His constructive counter-proposal: "If you have a system that reads the relevant section in our website and posts topics… that would be something I am much more excited about."
- **Bob** reframes the data model: aggregate "not 'projects,' or even 'thesis topics,' but the set of problems the prof and their team are interested in" — adding that such statements "would not need revision very often." He also drafted disclaimer language we should adopt nearly verbatim on chair pages: topics are "starting points only; an essential part of doing a thesis is the formulation and refinement of the problem itself."
- **Stephan** adds the pedagogy argument plainly: he dislikes theses as "fixed packages you can browse and choose."
- **Niels** adds the network-effect trap: "I do not think we would use it unless it is adopted by the whole department" — a chicken-and-egg that no student team can break by force, only route around.

### 1.5 Type D — niche pipelines (Peter, Mario, Häufle in part)

Peter's students come via the GTC; Mario posted broad standing interests once and they remain valid ("physics… that interest will not change soon"). Häufle: "for us, it works well at the moment." These chairs aren't resistant — the problem genuinely doesn't exist for them. The correct product response is to include them via scraped public data and otherwise leave them alone. Peter's one ask — occasional "bespoke advertisement" when a postdoc needs a student — is a feature to note and not build yet.

### 1.6 Cross-cutting tensions

1. **Stated vs revealed preferences.** Several "willing" chairs (Zell, Huson) describe behavior — infrequent monitoring, ad-hoc updates triggered by complaints — that predicts they would also under-maintain *our* system. Wichmann's "I'd be willing to at least give it a try" is sincere but is the same sentiment that preceded the 2022 failure. Weight behavior over politeness.
2. **The student perspective is acknowledged but unrepresented.** Macke and Menth both explicitly flag that they're arguing from the supervisor side and that students may see it differently. Our dataset is 27 professors and 0 students. The planned survey (weeks 29–1.07) is currently our only student-side evidence channel — worth pulling some lightweight student interviews earlier.
3. **Ostermann's one-liner is a data point, not a brush-off.** "Your assumption is wrong: https://ps.cs.uni-tuebingen.de/teaching/thesis/" tells us (a) our chair-coverage research had an error — audit the rest of our assumptions about who lists what; (b) machine-readable thesis info already exists in pockets and scraping it is the respectful integration path.

---

## 2. Timeline Reality Check

**Weeks 8–14 (auto-discovery).** PR #37 already exists, which is materially better than the plan's implicit "start now." The risk is breadth: 27+ chairs across Typo3, custom sites, PDF lists, and Google Docs. Realistic week-14 exit criterion: agent reliably ingests the **most common page structures covering ~20 chairs**, with manual seed data for the rest. Schema PR #35 must merge first; it's the rebase anchor for everything downstream.

**Weeks 15–21 (RAG).** "Optimize RAG" (#7) is unbounded as written. Bound it: weeks 15–16 stand up deepeval (#6) and record baseline retrieval/answer metrics; weeks 17–19 iterate (chunking, embeddings, reranking, paper tags #32) plus land skill computation (#21, closing #16) and the DeepSeek dedup (#33); weeks 20–21 retest against baseline. Without the eval harness first, "improved RAG" is an unfalsifiable claim — exactly what CLAUDE.md §4 warns against.

**Weeks 22–28 (deployment).** The hidden scope here is the security and trust work (§5 below), which is currently not in any issue. File issues now so the work is visible and estimable. Staging deployment should start week 25 at the latest to leave two weeks of real bake time.

**Weeks 29–1.07 (survey).** Plan.docx marks this "if wanted." Treat it as the schedule's pressure-release valve: if weeks 8–21 slip, this phase absorbs deployment overflow and the survey shrinks to a minimal Google Form. Where is the slack hidden overall? Almost entirely in (a) RAG scope and (b) this final phase. There is essentially **no slack in weeks 8–14** — which is why #35/#37 is the gate.

---

## 3. Technical Decisions (log)

| Decision | Status | Rationale |
|---|---|---|
| Stay with Ollama/local LLM as default | **Affirmed** | Privacy story matches professor sensitivities (Georg's scoop risk, Carsten's spam concern); aligns with local-first TOR import guidance (never route ZDV credentials through a hosted backend) |
| Keep Celery/Redis | **Affirmed** | Working; scrape jobs from #37 fit the existing queue |
| Keep PostgreSQL + pgvector | **Affirmed** | Mature, no change needed |
| WebSocket auth: JWT in URL → short-lived ticket or secure cookie | **Must change before hosting** | Tokens in URLs leak into logs/proxies/history. Estimated 3–5 days. Affects `frontend/src/api/jobEvents.ts`, `backend/app/ws/controller.py` |
| ChairExplorer hard-coded metrics | **Remove/disable before any demo** | Fabricated numbers shown to a trust-sensitive audience; mark "unavailable" until #37 supplies real data |
| README vs config drift ("no cloud accounts needed" vs Azure/DeepSeek support) | **Fix in docs pass, weeks 22–24** | Honesty in docs is part of the trust story |
| Port-adapter refactor (#5) | **Deferred indefinitely** | Architecture polish with no MVP payoff; CLAUDE.md simplicity rule applies |
| OCR engine (#4) | **Deferred** | Current LLM-based extraction works; revisit only if transcript-parsing error reports accumulate |

---

## 4. Product Strategy Decision Tree

**Branch A — accept the feedback (centralized platform is a hard sell):**
→ All energy on the student-facing chat: advisor discovery, competency profiling, context-prep for outreach. Chair management becomes an optional, later add-on. Scraping (#37) is the ingestion backbone. Professor participation required: **zero**. Risk profile: low — value delivery doesn't depend on convincing anyone.

**Branch B — fight for professor adoption anyway:**
→ Requires solving incentive alignment (which Hennig says students can't solve), guaranteeing multi-year operational stability (which we cannot honestly promise — who runs this in 2028, on whose budget?), and integrating with Typo3/group-website workflows (scope explosion). Three hard requirements, none achievable by 1.07.

**Decision: Branch A.** Recorded 2026-06-11. Branch B's prerequisites are not deliverables a Master's project can produce; Branch A delivers the Plan.docx minimum goal without them. Revisit only if the department (e.g., Dean of Studies) offers institutional ownership — that, not a better frontend, is what would change Hennig's calculus.

---

## 5. Data Quality Issues (ranked)

1. **ChairExplorer hard-coded metrics** — remove or disable before any demo. A professor seeing an invented citation count for their own chair would end the relationship. (No issue filed yet — file one.)
2. **DeepSeek duplicate papers (#33)** — duplicated publication data visibly undermines the "we represent your chair accurately" claim; fix before showcase. PR #34's dedup work is adjacent.
3. **Dummy skill computation (#16 / PR #21)** — competency profiles drive matching; a dummy model means matches are decorative. Must be real before the survey measures matching quality, i.e., land by week 19.
4. **Markdown rendering (#25)** — cosmetic; week 27–28 polish.
5. **Coverage-assumption errors** — the Ostermann incident: our "who lists topics" map had at least one false negative. Re-audit before publishing any department-wide view.

---

## 6. Known Unknowns

1. **Does the scraping agent scale across heterogeneity?** 27 chairs, wildly different sites. Test plan: run #37 against 5 structurally different chairs (Typo3 standard, ps.cs.uni-tuebingen.de, a PDF-list chair like Zell's, an MPI-hosted page, one Google-Doc/internal-only chair) and measure extraction quality before claiming generality.
2. **How often do professor research interests actually change?** Bob and Mario claim near-never (for areas, not topics). If true, re-scrape frequency can be quarterly. Test with 2–3 volunteer chairs (Wichmann, Huson, Kerstin are the friendliest candidates).
3. **Will students actually use the chat?** Zero student-side data today. Need signup + session tracking in the staging deployment (privacy-respecting, aggregate counts) and 3–5 student test sessions before the survey phase.
4. **What's the real onboarding friction?** The "<1 hour to value" MVP claim is untested end-to-end. Instrument time-to-first-match in staging.
5. **Who operates this after 1.07?** The Hennig question, unanswered. Honest options: hand off to the department, hand off to a successor student team, or publish as self-hostable open source with the department's data pipeline documented. Decide before the survey, because "what happens to my data" will be asked.

---

## 7. Recommendation to Leadership

1. **Shift the product narrative now** — from "help professors manage thesis topics" to "help students find the right thesis advisor." Update README, pitch deck, and any department-facing communication. The feedback doesn't merely permit this pivot; it demands it (Report 1 §6, Report 3).
2. **Reduce scope on the chair side.** No prof dashboards, no reminder emails, no write-workflows in the MVP. Chairs are represented via scraped public data plus an opt-in keyword layer later. Professor adoption is explicitly **not** a success metric.
3. **Hold the line on the critical path.** #35 → #37 by week 14 is the gate; everything in the RAG phase can shrink, the deployment-phase security/trust fixes cannot. Timeline is tight but doable.
4. **Fix the trust surface before any demo.** JWT-in-URL and hard-coded ChairExplorer metrics are both cheap to fix and catastrophic to be caught with. File issues for both this week.
5. **Spend the goodwill while it's warm.** Luxburg and Hennig offered conversations; Hennig named further interviewees; Wichmann/Huson/Kerstin volunteered willingness. A second round of 20-minute conversations in weeks 12–14 — this time demoing the *student-facing* tool — converts critics into informants and is the cheapest validation available before deployment.
