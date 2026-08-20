# User studies & user contact — full inventory with provenance

- **Date:** 2026-08-09
- **Task:** AM of [the final 1.0 plan](2026-08-08-final-1.0-plan.md). Explicitly invited by
  P. Gehler.
- **Grading:** G2 (interview summaries, insights, evidence of contact), G5 (how feedback
  influenced the project).

---

## Standing note on provenance — read first

P. Gehler wrote on 2026-08-05:

> *Not all user studies were probably documented every time. A chapter on the user studies
> and how the feedback influenced the project should simply be presented plausibly in the
> submission. If necessary, from memory, with a note to that effect.*

This document takes that invitation and draws the line it implies. **Every row carries an
explicit source marker**, and the two markers mean different things:

- **`documented`** — a dated artefact exists in this repository and is linked. The quotes are
  verbatim from that artefact.
- **`reconstructed`** — no contemporaneous record exists; the entry is written from memory,
  and says so in place.

**No row in this document is invented.** Where a detail is not recorded — how many people,
who was present, what exactly was said — the cell says *"not recorded"* rather than carrying
a plausible-looking number. An entry reading *"≈3 informal conversations, details not
recorded"* is honest evidence of contact; a fabricated interview log is not evidence of
anything, and would poison the rows that are real.

**The honest summary of this project's user contact:** one substantial documented study (27
professors, May 2026), one documented single-user product test (2026-07-04), a documented
supervisor exchange that reframed the whole final phase (2026-08-05), and — the gap — **no
documented contact with the actual end user, students, until Task Z′.** That gap is the
reason Z′ exists and is the project's critical path as of 2026-08-09.

> ### ⚠️ Section 3 is incomplete by construction
> The informal conversations — fellow students, Fachschaft contacts, advisors — are the rows
> only Domi can supply. They are listed there as explicit open slots with the questions that
> need answering. **This document is not finished until those are filled or struck.** Leaving
> them blank is better than guessing, but leaving them blank permanently understates the
> project's real user contact.

---

## 1. Documented contacts

| # | Date | Who | Format | What was asked | What was learned | What changed as a result | Source |
|---|---|---|---|---|---|---|---|
| 1 | **May 2026** | 27 professors, CS department, Uni Tübingen | Interviews (the research package's own framing; the instrument itself is **not recorded** — see §4) | Would you use / contribute to a central platform that matches students to thesis topics? | **A demand-side warning, not a feature request.** Roughly half (segments "A" and "C") did not want a central platform at all — either already overrun with applicants, or on principle preferring to co-create topics in direct conversation. Only ~35% ("Type B") would try a topic tool, and only under strict conditions: zero-friction, no reminder mails, stable for years, exportable to their own site. A topic-listing platform had **already been tried in the department around 2022 and failed for incentive reasons, not UI reasons** (per Prof. Hennig). The single most-endorsed idea was one already on the roadmap: scrape existing chair websites rather than ask professors to enter data — Macke: *"that would be something I am much more excited about."* | **The entire pivot away from the hosted platform.** The project was a ~90% feature-complete FastAPI/Postgres/pgvector/React chair-matcher; this finding reframed it as solving the wrong problem in the wrong shape for an audience that did not want it. Also redirected the audience from professors to students. | `documented` — [research package](../../docs/thesis-report/00-problem-and-research/2026-06-12-professor-research-package/), [00 README](../../docs/thesis-report/00-problem-and-research/README.md) |
| 2 | **2026-06-25** | **Not recorded** — see §4, gap G1 | Besprechung; notes taken | Do we still need a backend? Can this work without a database? How do we extend past CS? How do we distribute it? | The no-DB question was asked directly and in maintenance terms: *"Dann müssten wir auch nicht mehr das ganze up-to-date halten, dass es noch in 3 Jahren funktioniert."* Also settled the framing — the goal is **not** a research proposal but *"alle Möglichkeiten die existieren und die mit den eigenen Interessen übereinstimmen aufzeigen."* And produced the distribution list still in use: Fachschaft, Hennig-GitHub, Ersti-Heft, uni site. | Crystallised the **database-less, all-faculties** direction that became MASTERPLAN §1–§2. The distribution channel list is still the operative one in Task AD. | `documented` (notes) / participants `reconstructed` — [besprechung notes](../../docs/thesis-report/01-the-pivot/2026-06-25-besprechung-notes.md) |
| 3 | **2026-07-04** | P. Gehler, supervisor, acting as an **end user** | Hands-on product test, free-text written answers. **No protocol, no ground truth, n=1.** | Naturality of interaction; what was missing to take a real next step; would you use or recommend it | Three signals, verbatim: (1) *"It was asking a lot. It was not clear how much detail was required at which step."* (2) *"I think a bit more follow up help to be offered. Like tell me which one you would choose and then walk a bit more down that road. Eg also a bit more clarity of what I likely learn."* (3) *"Can a professor provide information for the skill? … An example walkthrough, or like 'Lisa found her thesis…' Example prompts?"* | **Three shipped fixes, fully traced.** M1: upfront framing message in `thesis-finder` (committed 2026-07-05). M2: recommend & drill-down step (2026-07-05). M3: paper-first gate in `draft-thesis-contact` (2026-07-05). M4 (professor-supplied input) and the example-walkthrough idea were **considered and explicitly dropped**, not silently folded in. | `documented` — [feedback](../../docs/thesis-report/04-open-work/2026-07-04-feedback-gehler.md), [Task M plan](2026-07-05-taskM-gehler-feedback-plan.md) |
| 4 | **2026-08-02** | Valentin Schmidt (team) → P. Gehler | Written question | *"As a professor what is more important to you? The actual proposals the skill generates or that people have used the skill to think about what they want to do?"* | — (the question itself; the answer is row 5) | Initiated the exchange that reframed the entire final phase. **Attribution matters for the report: this was Valentin's question, not Domi's.** | `documented` — [final 1.0 plan §0.3](2026-08-08-final-1.0-plan.md) |
| 5 | **2026-08-05** | P. Gehler, supervisor | Written answer, two messages | See row 4, plus submission guidance | **The outcome variable.** *"Students that have reflected about what topic they would like to work on. This likely has sharpened their understanding what kind of thesis topic that would be the best fit."* Plus three explicit invitations: document the user studies even from memory; state what future feedback should be gathered, when, by whom, from how many; and *"How could the project survive, and what would it take? Realistically, not just hoping someone takes over a GitHub project ;)"* | **The largest single reframe in the project.** Value proposition moved from artefact quality to student reflection. `thesis-finder` gained the verbatim pre/post reflection instrument (N0/N6/R7 + append-only session log). The beta protocol (AC′) was rebuilt reflection-first. The simulation rubric gained a reflection dimension (AL). Tasks AM (this document), AN, AO exist **because** of the three invitations. | `documented` — [final 1.0 plan §0.3](2026-08-08-final-1.0-plan.md) |

---

## 2. Contact that is scheduled but has not happened

Stated separately so it is never mistaken for evidence.

| Date | Who | Status as of 2026-08-09 |
|---|---|---|
| pending | 2–3 Tübingen students, ≥1 non-CS | **Task Z′.** Protocol written and frozen-pending-pilot, capture sheet built, feedback form scripted. **Recruiting texts not yet sent** — this is the project's critical path and its longest calendar clock. |
| pending | Fachschaft Informatik | **Task AD.** Text written, not sent. |
| pending | Menth / Gehler — permissible-channel question | **Task AD.** Text written, not sent. Explicitly *not* a Rundmail request. |

**The honest statement for the report: as of 2026-08-09 this project has never been observed
in the hands of a student.** Every design decision about the student experience rests on one
professor's single hands-on test, the 27-professor demand-side study, and simulated personas.

---

## 3. Informal contact — to be completed from memory ⚠️

**These rows are empty because no record exists, not because no contact happened.** The plan
explicitly invites reconstruction here, and a reconstructed entry with an honest
"details not recorded" is worth points; a blank is worth none.

Domi: fill or strike each. Rough is fine — *"≈3 conversations, June, no notes, influenced X"*
is exactly the right shape.

| Slot | Question to answer | Status |
|---|---|---|
| G2 | **Fellow students.** Roughly how many informal conversations about the thesis-search problem, in what period, and did any of them change a decision? | ⬜ open |
| G3 | **Fachschaft contacts.** Any conversation before the (unsent) Task AD mail — in person, Discord, anywhere? | ⬜ open |
| G4 | **Advisors other than Gehler.** Menth, or any chair contacted during ground-truth building who commented on the idea? | ⬜ open |
| G5 | **The 27-professor round.** Who conducted it, over what period, and did a written instrument exist? The package reports results but **not** its own method. | ⬜ open |
| G6 | **Team-internal.** Max and Valentin are excluded as Z′ testers, but did either give product feedback worth recording as contact? | ⬜ open |
| G7 | **Anyone who tried it and bounced.** Someone shown the tool informally who did not get through install. Negative contact is the most valuable kind and the least likely to be written down. | ⬜ open |

---

## 4. Known gaps in the documented rows

| # | Gap | Why it matters |
|---|---|---|
| G1 | **2026-06-25 Besprechung: participants not recorded.** The notes exist; the attendee list does not. | Determines whether row 2 is a user contact or an internal planning session. Currently it is honestly ambiguous, and the report must not imply supervisor endorsement that is not evidenced. |
| G5 | **The 27-professor study reports results but not its method.** No interview guide, no per-professor record, no date range finer than "May 2026" in the repo. | It is the project's single largest piece of user research. That its instrument is undocumented is a genuine methodological weakness and should be **stated in the report**, not smoothed over. |
| G8 | **M1–M3 were never live-exercised after landing.** Flagged by the 2026-07-05 review; folded into the AA′ hygiene sweep rather than given its own task. | The feedback→change loop in row 3 is traceable to a *commit*, not to a verified behaviour change. |

---

## 5. The feedback → change loops that are fully traceable

The chapter's strongest material: four cases where an external input is linked to a concrete
artefact change. These are what G5's *"how feedback influenced the project"* asks for.

### Loop 1 — Professors reject platforms → the entire architecture

**27 professors (May 2026) → hosted platform abandoned.** A ~90% feature-complete
FastAPI/Postgres/React application with 5 open PRs and 16 open issues was abandoned because
the user research said the demand side did not want it. The strongest version of this loop
is not that feedback changed a feature — **it is that feedback caused the team to throw away
almost-finished work.** That is expensive, verifiable, and rare.

### Loop 2 — Gehler's three signals → M1/M2/M3

**2026-07-04 test → three commits on 2026-07-05.** Each quoted signal maps to one shipped
change; two further ideas were explicitly dropped with reasons. This is the cleanest
input→artefact trace in the project. Caveat (G8): traceable to commits, not to re-verified
behaviour.

### Loop 3 — Simulation harness → the drill-down fix

**2026-08-04: the 8-persona simulation suite found a real defect** in the go-deeper /
drill-down branch, documented in
[`2026-08-04-go-deeper-branch-validation.md`](../dev_process/2026-08-04-go-deeper-branch-validation.md),
and the anti-misrouting rule now in `search-strategy.md` came out of the same harness. Not a
*user* loop, but a testing→finding→fix loop, and the two documented instances are directly
graded under G5.

### Loop 4 — Gehler's reflection answer → the reframe

**2026-08-05 → the shipping product.** The answer changed what the project claims to do:
`thesis-finder` now records the student's thesis self-understanding verbatim before and after
the search and shows both side by side. The response chosen was **reframe and measure, do not
rewrite the skills** — the value proposition became reflection, the beta protocol was rebuilt
around a verbatim pre/post pair, and the simulation rubric gained a reflection dimension.

**One property worth naming across all four:** in every case the response was to *change the
product or the measurement*, not to argue with the input. Loop 1 discarded finished code;
loop 4 changed the outcome variable the project is graded on, after most of the tool was
built. Both were cheaper to resist than to accept.

---

## 6. What this document does not claim

- It does **not** claim a user study with students. There has not been one (see §2).
- It does **not** claim the 27-professor round followed a documented protocol. It did not, as
  far as the repository records (G5).
- It does **not** claim M1–M3 were verified in use (G8).
- It does **not** fill §3 with plausible numbers. Those rows stay open until Domi fills them.
