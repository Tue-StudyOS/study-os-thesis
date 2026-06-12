# Market Analysis: Professor Feedback Synthesis

**StudyOS Thesis Advisor — Research Package, Report 1 of 5**
**Date:** 2026-06-11 · **Source:** 27 professor responses (Tübingen CS Department outreach, May 2026)

---

## 1. Executive Summary: What We Learned from 27 Professors

The thesis-topic problem is **not what we thought it was**. We assumed professors don't list topics because no good tool exists. The feedback shows the real barriers are structural, not technical:

1. **Incentive misalignment.** Listing topics publicly *increases* a chair's workload. Menth: "I supervise 20 theses but received inquiries for 50+." Macke: "listing specific topics only results in us getting even more applications which we had to turn down." For oversubscribed chairs, visibility is a cost, not a benefit.
2. **Tool fatigue.** Macke enumerated the existing stack unprompted: "ILIAS, Alma, nextcloud, MS Teams, slack, discord, ZDV email, room booking systems, gitlab, typo 3… rather than adding one more system to the list, I would be much more attracted to taking one down."
3. **Topics are emergent, not inventory.** Berens, Luxburg, Winther (O.K.), Häufle, and Niels all describe the same workflow: a student reaches out → conversation → topic is co-created. Winther: "it is just a bad idea to advertise static MSc/BSc topics rather than talk to the students about what's possible."
4. **Maintenance is intellectual work.** Macke: keeping topics current "is really intellectual work that a tool only helps slightly with." Huson: "the hard part is coming up with viable topics, putting them on the page is little work."

What actually works today, per the professors themselves: **direct contact, co-creation, and existing group websites.** A centralized topic database has been tried before in this exact department (~2022, by Hennig's predecessor as Dean of Studies) and **"failed miserably"** — for incentive reasons, not UI reasons.

---

## 2. Chair Typology

Four distinct response patterns emerged. (Counts are approximate; several responses straddle types.)

### Type A — "No thanks" (clear, capacity-driven refusal)
**Who:** Martin Butz, Michael Menth, Mähl
**Pattern:** No interest in listing because demand already exceeds capacity. Not laziness — a deliberate demand-management strategy.

> Butz: "we have no problems getting students these days — listing projects is indeed often too much overhead."

> Menth: "Wir werden überrannt von Anfragen… Es gibt schlicht keine Themen, die ich öffentlich stellen könnte." (We're overrun with inquiries… there are simply no topics I could post publicly.) — *Yet he adds:* "Ich wäre sehr froh, wenn es ein System gäbe, mit dem Studierende leichter an Abschlussarbeiten kommen können. Dann werde ich vielleicht auch nicht so überhäuft mit Anfragen."

Note the tension inside Menth's own answer: he refuses to list topics but *wants* a system that reduces misdirected inquiries. That's a signal for the student-facing pivot (§6), not for a topic database.

### Type B — "Yes, but only if trivial" (lists exist, maintenance is the burden)
**Who:** Philipp Hennig, Andreas Zell, Kerstin, Georg, Daniel Huson, Felix Wichmann, Bob/Rabanus, Anna
**Pattern:** Already maintain lists (Overleaf decks, Google Docs, group websites) and admit they're chronically outdated. Open to a tool **if and only if** it is low-friction, transparent, and stable for years.

> Zell: "the list is never up to date… I guess that >50% of all thesis topics that I supervise never make it to the online list."

> Huson: "I usually forget to update the page and I put off doing so because it is extra work." But: "having the listings in one place that can then be imported back to the group's website and to a CS-wide website would be good."

> Wichmann: "Sounds good — I'd be willing to at least give it a try. Main points are ease of use: access rights, interface, **reminder frequency under user control**."

> Georg: wants Uni-Tübingen-only access ("many of these topics are ideas that can turn into a paper and we do not want to share them with the rest of the world").

**The Hennig warning** (the single most important response in the dataset):

> "There absolutely must be a good incentive for the research groups to list theses there… This is something you likely won't get right as student developers, because it doesn't have much to do with the interface or the frontend. It's all about the internal dynamics of the CS department."

> "The website must be stable for at least a few years (i.e., also after you are long gone)… It's very hard to write an interactive web service that stays alive without developer care." (cites courses.cs.uni-tuebingen.de decaying after its HiWi developers left)

### Type C — "Actively don't want this" (principled resistance, not laziness)
**Who:** Jakob Macke, Ulrike von Luxburg, Philipp Berens, Ole Winther (O.K.), Stephan, Niels, Bob (partially)
**Pattern:** Pre-listing contradicts how they believe theses should work. Co-creation > browsing a catalogue.

> Winther: "Students had the impression that the four or five topics we had published were the only thing we worked on and then did not talk to us." (Listing actively *harmed* matching.)

> Luxburg: "experience shows: an up-to-date platform doesn't work, profs never update the topics. We've had many attempts in the department already."

> Stephan: "I dislike the idea that bachelor/master theses are just fixed packages you can browse and choose… such a platform also sounds like bureaucratic overhead to me."

> Macke: "I do not see the added value of such a central tool… If you have a system that **reads the relevant section in our website** and posts topics (and/or instructions on how to express interest in working with us), that would be something I am much more excited about."

> Bob: aggregate "not 'projects,' or even 'thesis topics,' but **the set of problems the prof and their team are interested in**" — these "would not need revision very often."

### Type D — "Not relevant to our workflow" (niche pipelines)
**Who:** Peter (GTC pipeline), Georg Martius–adjacent specialized groups, Mario (broad standing topics)
**Pattern:** Students arrive via specific channels (graduate training centers, lab courses, lectures); a department-wide listing adds nothing.

> Peter: "most of my MSc students come from the GTC — which has other ways of advertising… I wouldn't use it routinely."

> Mario: posted broad topics once, never updates, doesn't need to ("that interest will not change soon").

> Zell (gatekeeping pattern, also seen elsewhere): "students who write a B.S./M.S. thesis must at least have passed one of my lectures or lab courses."

### Distribution (approximate)

| Type | Share | Adoption outlook |
|---|---|---|
| A — capacity-driven "no" | ~15% | Won't list; might value *fewer misdirected inquiries* |
| B — willing if trivial | ~35% | Realistic early adopters, with hard conditions |
| C — principled "no" | ~35% | Won't adopt a topic database; open to keyword/area aggregation |
| D — niche pipeline | ~15% | Irrelevant to their workflow |

Even in the best case, **a topic-listing platform addresses ~35% of chairs** — and those chairs attach conditions (stability, zero friction, access control, no reminder spam) that are expensive to meet.

---

## 3. Key Insights

1. **Overhead is real but is not the bottleneck.** Zell, Hennig, Huson, Wichmann all confirm list maintenance is a burden. But fixing the overhead does not fix the *reason* lists go stale: topics emerge dynamically (Häufle: "research moves too fast and by the time students look at the thesis topics, they are outdated") and oversubscribed chairs have no reason to advertise.
2. **There is a working precedent for failure.** The ~2022 departmental list "failed miserably" (Hennig) and "we've had many attempts in the department already" (Luxburg). Any pitch that ignores this history will be dismissed by the people who lived through it.
3. **Professors trust local workflows over central systems.** Macke can push to his own website "in a few minutes." Ostermann's reply was one line: "Your assumption is wrong: https://ps.cs.uni-tuebingen.de/teaching/thesis/" — his chair already solved this locally. Niels: "I do not think we would use it unless it is adopted by the whole department" (a chicken-and-egg problem).
4. **The abandonment fear is specific and earned.** Hennig's courses.cs.uni-tuebingen.de example is a concrete, named precedent of a student-built service decaying. We must answer "who maintains this in 2028?" before asking anyone to invest.
5. **One clever design detail worth stealing:** Hennig's group keeps listings fresh because *PhD students are the listed contact* — stale listings generate emails to them, so they self-remove. Incentive design beats reminder emails.

---

## 4. What Professors Would Actually Use

Synthesizing the conditional yeses:

- **Keywords / research areas, not concrete projects.** Häufle ("a list of research keywords and students can apply by selecting several"), Bob ("the set of problems the prof and their team are interested in" — low revision frequency), Mario (broad topics stay valid for years), Niels ("a list of general domains we are interested in").
- **Scrape, don't ask.** Macke explicitly: a system that *reads existing websites* is "something I am much more excited about." Ostermann's curt reply implies the same: the data already exists at ps.cs.uni-tuebingen.de. **This validates issue #36 / PR #37 (chair-discovery scraping agent) as the single most feedback-aligned feature in the codebase.**
- **Zero new emails.** Macke: "bombarded by a long list of reminders." Wichmann's condition: "reminder frequency under user control." Default must be *no* notifications.
- **Portable / exportable.** Huson: listings "imported back to the group's website and to a CS-wide website." The platform must not hold data hostage.
- **Access control.** Georg: Uni-Tübingen-only visibility (scoop risk). Carsten (truncated response): "Public topic listings invite excessive spam from non-Tuebingen students and increase the scoop risk."
- **Simplicity over structure.** Zell: "No 'thesis topics SQL database' or such, but rather just a web page with PDFs searchable by keywords."

---

## 5. Tension Matrix

| Stated goal | What feedback says | Verdict |
|---|---|---|
| Help students find thesis topics | Students do struggle (implied by 50+ inquiries/chair bouncing around); but a *topic list* misleads them (Winther: students thought 4 listed topics = the whole lab) | Solvable — but via discovery/guidance, not a catalogue |
| Help profs manage topic listings | ~65% of chairs don't want to manage listings at all; the 35% who do attach stability + friction conditions we may not be able to guarantee | Weak — this is the part of the original concept the market rejects |
| Reduce prof overhead | The overhead profs actually complain about is *misdirected inquiries*, not list maintenance (Menth, Macke, Butz) | Reframe — reduce inquiry noise, not listing effort |

**The centralized-platform framing does not clearly serve any of the three goals.** The student-discovery framing serves goals 1 and 3.

---

## 6. Product Pivot Recommendation

**Drop "centralized thesis topic management platform" as the lead narrative. Lead with "AI thesis advisor for students."**

What the feedback supports building:

1. **Help students ask better questions before contacting a professor.** Menth would be "sehr froh" about anything that makes inquiries better-targeted. Winther believes thesis selection "merits person-to-person interaction" — our tool should *prepare* that interaction, not replace it.
2. **Extract and aggregate existing public information** (group websites, ps.cs.uni-tuebingen.de, publication records) rather than asking chairs to enter data. Macke endorsed exactly this. PR #37 already builds it.
3. **Represent chairs by research areas/problems, not topic inventories.** Bob and Häufle handed us the data model: stable keywords + a standing disclaimer that topics are co-created starting points.
4. **Chair-side tooling becomes opt-in, not the product.** For Type B chairs only, later, with export and access control. Never reminder-driven.

Why this works where the platform doesn't: it requires **zero professor adoption to deliver student value**, it sidesteps the incentive problem Hennig says we can't solve, and it converts the 65% "no" chairs from blockers into passive data sources (their public websites).

This also matches the project's own minimum-viable goal from Plan.docx: *"After <1 hour, users have a much better idea which chair to contact."* That goal never required professors to do anything.

**Next steps:**
- Reframe README / pitch materials around student discovery (see Report 3).
- Prioritize landing PR #35 → #37 (scraping pipeline) — it is the feedback-validated core.
- Park all "reminder email" and "prof dashboard" ideas indefinitely.
- Optional: take Luxburg and Hennig up on their conversation offers — both explicitly invited follow-up, and Hennig named further interviewees (Luxburg, Grust, Martius).
