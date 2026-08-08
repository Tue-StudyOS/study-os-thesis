# Beta test protocol — reflection-first (2026-08-08)

**Task AC′** of [the final 1.0 plan](2026-08-08-final-1.0-plan.md). Executed per tester in
Task Z′. **Recruiting texts:** [2026-08-08-beta-recruiting-message.md](2026-08-08-beta-recruiting-message.md).
**Per-session capture sheet:** [2026-08-08-session-capture-sheet.md](2026-08-08-session-capture-sheet.md) — one copy per tester, filled live.

**What this measures.** Not "did the tool name the right chairs" — that is what every
existing recall/precision number measures. This measures the variable P. Gehler named on
2026-08-05: *did the student end up with a sharper understanding of the thesis they want.*
The primary result is a **pair of verbatim self-statements**, before and after. Artifact
quality is secondary and supports it — it is the reason to trust the options that triggered
the reflection.

**The instrument already exists in the product.** The coherence sweep (`3cb208f`) put it
into `thesis-finder` itself: Step N0 asks the question before anything else and records the
answer verbatim; Steps N6/R7 ask it again at the end and show both statements side by side;
the session file keeps an append-only log so the comparison survives across weeks and
sessions. This protocol does **not** rebuild that. It defines how the pair is collected,
co-scored, and reported at n=1–3.

---

## 1. Before the run — the reflection baseline

Collected by the interviewer, **before the tester opens the tool or reads INSTALL.md**.

**(a) Two sentences: "What kind of thesis do you think you're looking for right now?"**
Written by the tester, in their own words, kept verbatim. Uncertainty is a valid answer and
must not be cleaned up.

> **Decision: the protocol collects this independently, in addition to the tool's Step N0.
> Both are kept.** Three reasons, each found by reading the shipped skill:
>
> 1. **Persistence gap.** N0's statement is written to the session file only in **Step N4**,
>    *after* results are delivered. A run that dies during installation or discovery leaves
>    no persisted baseline — and §2 declares getting stuck a measurement, so aborted runs are
>    expected. They are precisely the runs where the tool's own copy would be lost.
> 2. **Demand characteristic.** The one-time framing message shown *before* N0 tells the
>    student that "most students finish with a sharper sense of what they want than they
>    started with." The tool's own pre-statement is therefore taken under a prime that
>    announces the expected outcome. A copy taken before the tool is opened is not.
> 3. **The file is the tester's, not ours.** The session log lives at
>    `~/.claude/thesis-finder/session.md` (or `./thesis-finder-session.md` on the documented
>    fallback path). We cannot assume we receive it, and must not depend on it.
>
> The external copy does not replace N0 — it makes the tool's own instrument checkable.
> If the external statement and the N0 statement differ noticeably, that difference *is*
> the measured effect of the framing message, and is reported as such.

**(b) The 2–3 supervisors, chairs or companies the tester already knows of.** Written down
before the run. This is the personal baseline for "did it show me something new", and it
beats recall-against-ground-truth for external validity: it is this student's actual prior
state, not a list we assembled.

---

## 2. The run

- **Installation strictly from [`INSTALL.md`](../../INSTALL.md) and the
  [`skills-v2.0.0` release](https://github.com/Tue-StudyOS/study-os-thesis/releases/tag/skills-v2.0.0).
  No maintainer help.** If the tester gets stuck, the interviewer records where and stops
  helping. **Getting stuck is a measurement, not a failure** — it is G4 usability evidence
  and cannot be collected any other way.
- **Start the clock** when the tester opens INSTALL.md, **stop** when `thesis-finder` first
  responds. See §5.
- Run `thesis-finder` end to end, including the closing Step N6.
- **Save:** the full transcript, the delivered option map, and the session file (ask for
  both paths — the fallback is real and the skill announces which one it used).

## 3. After the run — the reflection delta

**Use the tool's own N6 answer as the post-statement.** Do not re-ask the same question
externally afterwards: by then the tool has already shown the tester both statements side by
side and commented on what changed, so a second answer would be contaminated by that
commentary. N6 records the answer verbatim *before* it comments — that is the clean one.

Then, immediately after N6 and **before any discussion of the results**, the interviewer asks
one open question:

> **"What, if anything, is clearer to you now than before?"**

Recorded verbatim. Note in the write-up that this answer follows the tool's own side-by-side
comment — the contamination is real, so it is stated rather than hidden.

**Reported per tester as a triple, all verbatim:** external pre-statement (§1a) → N0
statement → N6 statement.

**At n=1–3 this is not reduced to a score.** The statements are quoted. A pair that is
"nearly identical", or one that got *less* certain, is a legitimate and reportable result —
the skill says so itself, and a test names that behaviour. Do not report a null as a failure
of the tester or the run.

## 4. Secondary measures

| # | Measure | How |
|---|---|---|
| a | **≥1 credible option the tester did not already know** | Against the §1b list. **Co-scored with the tester.** |
| b | **Count of factually wrong statements in the map** — misattribution, dead URL, wrong affiliation. The trust metric. | Walk the map together, check links live. **Co-scored with the tester.** |
| c | **Finished without help (yes/no) + setup minutes** | Observed, see §5. |
| d | **Would they actually contact one of the options** | Asked directly; yes/no + which one + why not. |

**(a) and (b) are scored jointly with the tester, not by us afterwards.** This is the only
independent evaluation this project will get — it absorbs the old Task X (independent
scoring) rather than leaving it unmet. Where we and the tester disagree on whether something
counts, record **both** judgements; do not resolve it in our favour.

## 5. Setup time — read this before quoting any number

Task AB′ measured a **cold install in 48 s**. That was an **agent executing commands** with
no browsing, no reading, no decisions, no mistakes. It is a **lower bound on the mechanical
steps**, not an expected value for a human, and **must never be communicated as one** — not
to testers, not in the report, not in the release notes.

The human number is what this protocol exists to collect: wall-clock minutes from opening
INSTALL.md to `thesis-finder`'s first response, including reading, account setup problems,
and wrong turns. Report the human figures; cite the 48 s only alongside them and only with
the lower-bound caveat attached.

## 6. Feedback form

Anonymous (Google Forms or equivalent). Linked from `INSTALL.md` and from the release notes.
Fills a different role from the interview: the interview is the deep n=2–3 instrument, the
form catches people who install from the release without ever talking to us.

Questions, in this order — exact wording in [Appendix A](#appendix-a--feedback-form-questions).

1. Installation — worked / worked with effort / failed (+ where)
2. Setup duration in minutes (free number)
3. Relevance of the options shown (1–5)
4. Trustworthiness of the sources (1–5)
5. Would you contact one of them? (yes / maybe / no)
6. What was confusing? (free text)
7. Studiengang (optional, free text)
8. **The reflection question** (free text) — the one item shared with the interview protocol

## 7. Pilot

Run the whole protocol **once** with a friendly student first, to shake out ambiguities in
the wording and the timing before the real sessions.

**The pilot counts as a Z′ session only if the protocol was not changed mid-way.** If it was
changed, the pilot is discarded as data, the change is recorded here with its reason, and
the protocol is **frozen** before the first counted session. Freezing is what makes the
counted sessions comparable; note the freeze date at the top of this file when it happens.

---

## Appendix A — feedback form questions

German, verbatim, for pasting into the form. English gloss in brackets is for this document
only and is not part of the form.

1. **Hat die Installation funktioniert?** [installability]
   ☐ Ja, problemlos ☐ Ja, aber mit Mühe ☐ Nein
2. **Falls „mit Mühe" oder „nein" — wo bist du hängen geblieben?** (Freitext)
3. **Wie lange hat das Setup ungefähr gedauert (in Minuten)?** [human setup time — §5]
4. **Wie relevant waren die vorgeschlagenen Optionen für dich?** (1 = gar nicht, 5 = sehr) [relevance]
5. **Wie vertrauenswürdig fandest du die genannten Quellen und Belege?** (1 = gar nicht, 5 = sehr) [source trust]
6. **Würdest du eine der vorgeschlagenen Personen oder Firmen tatsächlich kontaktieren?**
   ☐ Ja ☐ Vielleicht ☐ Nein
7. **Was war verwirrend oder unklar?** (Freitext)
8. **Studiengang** (freiwillig, Freitext)
9. **In ein bis zwei Sätzen: Was für eine Abschlussarbeit suchst du jetzt — und hat sich das
   durch den Durchlauf verändert?** (Freitext) [the reflection question]

---

## Status of the done-when criteria

| Criterion | State |
|---|---|
| Protocol committed | ✅ this file |
| Recruiting sent | ⬜ texts ready ([recruiting message](2026-08-08-beta-recruiting-message.md)); **sending requires Domi** |
| Form live | ⬜ questions specified (Appendix A) and scripted ([`scripts/create_beta_feedback_form.gs`](../../scripts/create_beta_feedback_form.gs)); **running it requires a Google account** |
| Pilot completed, protocol frozen | ⬜ **requires a real student**; freeze date to be noted at the top of this file |

The last three cannot be completed from inside the repository. They are the first actions of
Task Z′.
