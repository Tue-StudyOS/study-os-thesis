# 04 — Open Work

**Files in this folder:**
- [2026-07-02-ideen-domi.md](2026-07-02-ideen-domi.md) — raw brainstorm on six directions for
  the project (other universities, testable evaluation, backbone breadth, distribution,
  and — most importantly — the scope-vs-genericness intuition below).
- [2026-07-04-feedback-gehler.md](2026-07-04-feedback-gehler.md) — raw notes from an informal
  end-user test session, with Domi's own follow-up ideas interleaved. Not a designed eval run
  (no protocol, no ground truth, one tester) — see synthesis below for what it does and
  doesn't support.

**Related, not moved here** (already dated/organized in place):
- [findings/gesamtplan-2026-07-02.md](../../../findings/gesamtplan-2026-07-02.md) — a full
  codebase review + point-by-point discussion of the ideas above, ending in a prioritized
  implementation plan.

## What's open right now

*(Updated 2026-07-05 to match the current state after Tasks T/U/S and the independent
1.0-readiness review closed several items below; this section is a short pointer to the
review's full punch list, not a duplicate of it — see
[2026-07-05-fable-1.0-readiness-review.md](2026-07-05-fable-1.0-readiness-review.md) and
`STATUS.md` Phase 5 [Tasks V–AA] for the actionable, current version.)*

- **Theology blind live run** (was: "Law and Theology"). Law was blind-run 2026-07-03/04
  (60% → 80% recall after a skill fix); Humanities was corrected to 100% via an
  eval-protocol fix, but by a **re-score**, not a fresh blind run — the reviewing session
  was already un-blind on that faculty. Theology is now the only hard-faculty ground truth
  no eval session has ever opened mid-run, making it the last clean, uncontaminated data
  point available (`STATUS.md` Phase 5 Task V; also exercises the known N.N.-vacant-chair
  case). The interdisciplinary case was covered via Task R's routing check (100%).
- **Track 2 (backbone audit & repair, weak-web-presence fallback, query-skeleton
  iteration)** — still not started; implicitly skipped because Task I already cleared the
  recall bar that would have triggered it. **Task S (output & interview quality pass) is
  done** (2026-07-03; 4/5 criteria pass cleanly, one gap found and fixed) — see
  [03](../03-hardening-and-evaluation/README.md). Task R (edge-case behavior) is also done
  (3/3 pass).
- **The roadmap's "core is done" recall bar was declared MET on 2026-07-04** (all 6
  measured faculties ≥80%, 2 hard) — but the independent review found the evidence behind
  the two hard-faculty numbers is not clean blind measurement (see [03](../03-hardening-and-evaluation/README.md)
  and the review). Treat the GO as **provisional**, not unmet — a meaningfully different
  status than either "not yet met" or an unqualified "done."
- **Company-backbone ground-truth circularity** (named in [03](../03-hardening-and-evaluation/README.md)):
  an independent, non-backbone-derived ground truth for company discovery is still missing
  (`STATUS.md` Phase 5 Task Y).
- **Non-MINT company backbone coverage** — meaningfully improved by Task L (2026-07-04:
  all 7 faculties + ZITh now have a Studiengangs-Routing entry, even where the honest
  answer is "no company track — use `find-university-chairs` instead"), but still thin in
  absolute entry counts for Recht/Legal Tech (0), Sozialwissenschaften (1), and Sport (2) —
  documented in the backbone itself as a structural gap, not padded.
- **The project's central scientific claim is untested** (see "The scope question" below)
  — the gesamtplan's scope-erosion experiment was never run. The independent review names
  this the single highest-value remaining task (`STATUS.md` Phase 5 Task W).
- **Nobody outside the project has run the shipped release artifact** — Gehler's informal
  test (below) used a dev checkout with no protocol or ground truth. Distribution has not
  started. Design-Entscheidungen.md TODOs 1 and 2 (both "Hoch/Ja") remain open
  (`STATUS.md` Phase 5 Task Z).
- **Small, real, unfixed defects** the review found and deliberately left unpatched (it was
  a read-only pass): `find-recent-papers`' shipped paper index conflates two different
  people both named "Matthias Hein"; `tuebingen-degree-programs.md` is CS-only but used as
  if university-wide; `find-company-thesis-options`'s frontmatter claims "any discipline"
  against its own routing table's honest exceptions; the `~/.claude/` session path sits
  against a stated multi-agent portability claim. Bundled as `STATUS.md` Phase 5 Task AA.

## A first, informal data point toward independent validation

`2026-07-04-feedback-gehler.md` is the first evidence of a real person outside the project
using the tool — relevant to the still-open "independent external validation" item (Design-
Entscheidungen.md TODO 1) — but it is **informal, not a designed eval**: one tester, no
protocol, no ground truth, feedback captured as free-text quotes rather than scored against a
rubric. Treat it as a source of concrete product ideas, not as evidence for or against the
recall/precision/steering numbers in [03](../03-hardening-and-evaluation/README.md). Three
usable signals from it: (1) the tester found the interview's information-need unclear at the
start ("not clear how much detail was required at which step") — a candidate fix is an
upfront one-line explanation of what the skill does and that detail level is the student's
choice; (2) the tester wanted more concrete follow-through after the option map ("tell me
which one you would choose... walk a bit more down that road") — currently `thesis-finder`
only offers `draft-thesis-contact` as a next step, with no ranking or drill-down; (3) the
tester asked whether professors could contribute information to the skill — out of scope per
the no-DB principle ([01](../01-the-pivot/README.md)), but suggests the coverage caveat could
more clearly explain *why* the tool doesn't take professor input. **Update 2026-07-05:**
signals (1) and (2) have since been implemented — `thesis-finder` now gives an upfront
framing message (Task M1) and a recommend-and-drill-down step after the option map
(Task M2); signal (3) was considered and explicitly dropped (see the Task M plan doc, item
M4). The independent review notes these fixes have not yet been live-exercised since
landing (folded into Phase 5 Task AA) — they address the *stated* feedback, but no fresh
user has confirmed the fix actually lands.

## The scope question — the idea that matters most for the thesis claim

`2026-07-02-ideen-domi.md` raises a specific concern, credited there to the author's stats
background (SLLN/law-of-large-numbers intuition): **the broader the tool is made, the more it
converges in expectation toward plain Claude.** The reasoning: the tool's advantage over plain
Claude comes from curated, scope-specific knowledge (the faculty backbone, the MPI-IS/ELLIS
leg, the search-strategy query mapping) — a fixed asset that one person can maintain. Spread
that same curation budget across more universities or a wider company list, and curation
*density per query* drops; in the limit, the tool degrades toward "plain Claude with extra
steps." `findings/gesamtplan-2026-07-02.md` takes this seriously as the project's central
scientific claim rather than a hedge, and works through six concrete ideas against it (other
universities as a third track, making the evaluation genuinely testable, broadening the
company/university backbones, generalizing the backbone-building process to any university,
and distribution). Its recommendation, argued point by point: **narrow scope (Tübingen, all
faculties) is the stronger position, not a fallback** — and the way to make that a scientific
claim rather than an opinion is to test it directly, e.g. running the identical skill
mechanism against a university it was *not* curated for and showing the advantage over
baseline shrinks or disappears. That experiment has not been run; it is the most
consequential piece of unfinished work going into the write-up.

**Independent review (2026-07-05):** assessed this argument as directionally right but
over-claimed in its SLLN framing — a curated foreign backbone would not dilute Tübingen's
curation density; only an *uncurated* expansion (the rejected Idee 5 direction) trivially
converges to baseline by construction, which isn't a law-of-large-numbers effect. The
defensible, testable form is a **dose-response claim**: advantage is proportional to
curated local-knowledge density in the query scope — consistent with, but not proven by,
the two internal data points already cited (the MPI-IS-fix recall jump; the weak C1
company delta). The review also trims the proposed experiment to a feasible minimum: one
foreign university (TUM recommended — the harder, more honest comparison per the
gesamtplan's own §7 reasoning), one faculty, a ~6-chair ground truth curated by a second
person, estimated at 2–4 working days. Full reasoning:
[2026-07-05-fable-1.0-readiness-review.md](2026-07-05-fable-1.0-readiness-review.md) §2.

## What was deliberately decided against (not just "not done yet")

- **Generic, per-university entry-point discovery via live web search** — rejected, not
  deferred. If the skill's first move for any university were "search for the right
  organizational entry point," it would functionally *be* the plain-Claude baseline it's
  supposed to beat; the whole measured advantage comes from curated Tübingen-specific
  knowledge that a runtime search cannot reconstruct.
- **Scraping concrete job postings** (see [02](../02-building-the-core/README.md)) — rejected
  on fragility and low-yield grounds, not merely postponed.
- **A third "other universities" track as a user-facing feature** — the brainstorm's own idea
  #1; `gesamtplan-2026-07-02.md` argues this should be a controlled *experiment arm*, not a
  shipped feature, precisely because it would dilute the curated-knowledge advantage described
  above.
