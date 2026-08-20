# Blind Theology run — the shipping architecture's only ground-truth measurement

- **Date:** 2026-08-08
- **Task:** V′ of [the final 1.0 plan](2026-08-08-final-1.0-plan.md)
- **Architecture:** `[rules-only, ≥2026-07-31]`
- **Result artifact:** `dist/live-validation/theology-skill.md` (committed)
- **Ground truth:** `skills/tests/eval_ground_truth/theology.md`
- **Original record:** the dated log entry in
  [`2026-07-02-live-eval-runbook.md`](2026-07-02-live-eval-runbook.md), 2026-08-08.
  That entry remains the primary record; this document promotes it out of a runbook log
  because it is the single most-cited measurement in the project and was effectively
  unfindable there.

---

## Headline

> **Recall 5/6 = 83 %. Precision 9/9 = 100 %.**
> On a first, genuinely blind run, with **no fix applied first**.

**Two firsts in one run, which is why this measurement carries disproportionate weight:**

1. **The first clean blind hard-faculty run.** Every earlier hard-faculty number was
   contested: Humanities' 100 % is a re-score by a session already un-blind on that faculty,
   and Law's 80 % came from a session that had read the document naming the missed chair.
   Theology's ground truth had never been opened mid-run by any session.
2. **The first — and still the only — faculty measurement of the architecture that
   actually ships.** The static backbone was deleted on 2026-07-31. Six of the seven
   faculty figures in the [scorecard](2026-07-03-eval-aggregate-scorecard.md) describe the
   removed system. This one does not.

Theology is also the only hard faculty that cleared the ≥80 % bar **without** a preceding
repair — Humanities needed an eval-protocol fix, Law needed the §5 skill fix.

---

## Method and how blindness was held

Only the ground-truth file's single `Sample interest:` line was read (via `grep`) before
Pass 1. The chair rows, the Notes and the scoring table stayed closed until scoring.

The remaining five profile dimensions were **reconstructed from the discipline**, not from
the ground truth: historical-critical exegesis (methods), ancient religion (domain), a
text-based monograph (thesis style), Hebrew/Greek/Latin (skills), and as no-gos practical
theology, Religionspädagogik and quantitative religion-sociology.

One deliberate choice inside that reconstruction is worth recording: **systematic theology
was marked *off-core* rather than a hard no-go**, specifically to avoid re-creating the
over-exclusion failure class that produced the Humanities 60 %. That is a methodological
carry-over from an earlier failure, applied before the run rather than diagnosed after it.

---

## Recall — 5/6

**Found:** Leuenberger, Kamlah, Tilly, Landmesser, Drecoll.
**Missed:** Witt.

**Discovery recall was 6/6.** Witt was enumerated in Pass 1 and appears by name in the
map's *"Excluded (recorded, not silently dropped)"* section. The miss is therefore a
**downstream filtering decision, not a crawl failure** — a materially different defect
class, and only visible because the skill is required to record its exclusions.

### The Witt miss is defensible, and belongs to the Saurer class rather than the Remmert class

Witt's chair is *Reformationsgeschichte und Mittelalter*; the sample interest specifies
*"early-church / **late-antique** church history."* Read literally, excluding a
Reformation/medieval chair is **correct behaviour** — including him is arguably the padding
that precision exists to catch. The ground truth counts him relevant on a broader
"church history writ large" reading.

**This is an open question for the ground truth, not an obvious skill defect.** Either
`theology.md` should state why a Reformation/medieval chair counts for a late-antique
persona, or that row is over-inclusive. It was **flagged and deliberately not resolved** in
the session that scored it — resolving it there would have meant the scorer editing the
answer key.

---

## Precision — 9/9

Nine options surfaced, all judged relevant:

| Option | Why it counts |
|---|---|
| The five ground-truth core chairs | direct matches |
| **Zellentin** | the GT file explicitly instructs he be scored relevant, not noise. The map flagged him as drifting toward Qur'anic/early-Islamic work under his ERC project QaSLA — an accurate read of his current output |
| **Eisele** (NT, Gospel-of-Thomas transmission) | Catholic faculty |
| **Jürgasch** (Alte Kirchengeschichte und Patrologie) | Catholic faculty |
| **Scoralick** (AT) | Catholic faculty |

**The three Catholic-faculty chairs are a genuine coverage win, not scored generosity.**
The GT's own Note 3 says Catholic Theology "is a separate faculty covering the same
disciplines; not crawled for this file" — so they sit outside GT scope but squarely inside
the sample interest, and count as relevant under the eval README's rule that *a correct
option missing from the ground truth is still relevant, not noise*.

The persona says "biblical studies," not "Protestant biblical studies." Tübingen splits
that discipline across two faculties, and **the run crossed the boundary unprompted.**

---

## Vacancy handling — passed, on the harder version of the test

The faculty carries **six vacant chairs out of sixteen**. The run enumerated all six by
name *before* the option map, named **no holder for any of them**, and stated explicitly
that a chair designation must not be read as an available supervisor.

Two vacancies sit **directly on this persona's focus** — *Altes Testament I*
("Literaturgeschichte des AT") and *Neues Testament II* ("Evangelienforschung"). The run
reported both as unavailable **instead of routing around them**, and additionally noted
that Leuenberger consequently carries the department's OT load one chair short, and that
Eisele partly fills the Evangelienforschung gap from the Catholic side.

**Caveat on what was actually tested.** The GT's §21 vacancy scenario is written for a
*theological ethics / fundamental theology* persona (Systematische Theologie II/III), which
this biblical-studies persona does not exercise. Syst. Theol. II was correctly listed as
vacant but was off-core here either way. The on-focus AT-I/NT-II vacancies are arguably the
stronger test and were handled correctly, **but the ethics-persona case remains formally
unrun.**

Per GT §21 this is recorded as a **robustness/coverage result, not a recall figure.**

---

## What this run does and does not support

**Supports:**

- Rules-only discovery reaches ≥80 % recall on a structurally hard faculty, blind, first try.
- It does so **with no backbone file at all** — `references/tuebingen-faculty-backbone.md`
  no longer exists. That is a real data point for the no-DB direction.
- Honest vacancy reporting works under pressure (six of sixteen chairs vacant, two on-focus).
- Cross-faculty coverage emerges without being asked for.

**Does not support:**

- **Any claim about discovery quality in general.** This is **one faculty**, n=1, in a
  discipline with unusually well-structured web presence. Task AK exists to add CS and Law
  on the current architecture.
- **The delegation boundary.** One agent executed both skills' workflows inline rather than
  crossing a hard tool boundary, so this run does **not** test the hand-off itself — schema
  conformance, or what happens when the delegate returns fewer than five candidates.
- **Single-agent scoring.** Designed, executed and scored in one session, like every other
  eval in this project. The mitigation is live-verified sourcing, not independent review.

---

## Incidental finding: URL drift is now a pattern

The Catholic faculty's
`.../alte-kirchengeschichte-patrologie-und-christliche-archaeologie/team/lehrstuhlinhaber/`
returned **HTTP 404**. Recovered via search fallback — Jürgasch's W3 appointment confirmed
through the university's own Personalnachrichten 1/2026.

This is the **fourth independent URL-drift hit**, after CS/Cyber Valley,
Humanities/interfaculty-centres and Law/Juniorprofessur. Four out of four faculties tested.
**The pattern is well past coincidence**, and it is the strongest empirical argument in the
repo for why a maintained URI catalog was the wrong architecture: every one of those URLs
would have been a stale entry in a file someone had to notice and fix.

---

## Open items this run left behind

| Item | Status |
|---|---|
| Is the GT's **Witt** row over-inclusive for a late-antique persona? | open — needs a decision by someone other than the scoring session |
| GT §21 **ethics-persona** vacancy scenario | formally unrun |
| The `discover-university-candidates` **hand-off boundary** | untested — no run has crossed it as a real tool boundary |
| CS + Law on the current architecture | Task AK |
