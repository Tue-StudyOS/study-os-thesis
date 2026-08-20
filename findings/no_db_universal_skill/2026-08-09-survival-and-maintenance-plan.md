# Survival & maintenance plan

- **Date:** 2026-08-09
- **Task:** AO of [the final 1.0 plan](2026-08-08-final-1.0-plan.md). Explicitly invited by
  P. Gehler: *"How could the project survive, and what would it take? Realistically, not just
  hoping someone takes over a GitHub project ;)"*
- **Grading:** G5 (future development), G3 (design rationale), G1 (the architecture decision
  in hindsight).

---

## The short answer

**The survival strategy is already shipped, and it is not a plan — it is the architecture.**

On 2026-07-31 the project deleted its static backbones: the curated Tübingen faculty URI
catalog and the BW company catalog. Discovery became rules-only — the skills carry *how to
search*, and the data comes from the live web at runtime. The stated rationale on 2026-07-30
was that this "better matches the maintenance-free product goal."

That decision was made for product reasons. Its largest consequence turns out to be a
survival property: **a system with no database, no backend, no scraped catalog and no
maintained URI list has nothing that goes stale on a schedule.** There is no refresh job to
keep running, no server bill, no credential to rotate, no scraper to repair when a site
changes its markup.

The honest framing for the write-up is therefore *not* "here is how we hope someone will
maintain this." It is: **the thing that usually kills a student project — the maintenance
burden — was designed out of this one, and the remaining risks are real but different in
kind.** The rest of this document is what that claim costs in honesty.

This was not hindsight. The project's founding constraint, written in
[MASTERPLAN §1](../../MASTERPLAN.md) before any of this was built, was already: *"the system
must be maintenance-free — no one will keep a database fresh after this project."* The
2026-07-31 pivot is that constraint finally being taken seriously, two architectures late.

---

## 1. What cannot rot

| Component | Why it cannot rot |
|---|---|
| **The 10 shipped skills** | Plain Markdown. `SKILL.md` entrypoints plus `references/` files. No code to break, no dependency to update, no build step at install time. |
| **No database** | There is no runtime store, so there is nothing to go stale. Curated chair data survives *only* as evaluation ground truth, never as a runtime source. |
| **No backend, no server, no domain** | Nothing runs between sessions. Nothing needs hosting, uptime, or a paying owner. The project can be abandoned and still work. |
| **No credentials, no API keys** | Nothing to rotate, leak, or expire. The user brings their own agent client. |
| **No scraped job boards or catalogs** | The failure mode that kills scraper projects — the source site changes its markup — does not exist here, because nothing is scraped ahead of time. |
| **Distribution** | A GitHub release with two archives. GitHub could disappear and the artefact would still be a folder of Markdown files a student can copy. |

**This is enforced, not merely intended.** `skills/tests/test_skill_package.py` carries
`test_shipped_resources_are_not_static_uri_catalogs` — an invariant test that fails the build
if a static URI catalog reappears in the shipped resources. Someone who tries to "helpfully"
re-add a curated list of chair URLs is stopped by CI. That test is the single most important
piece of survival infrastructure in the repo, because it protects the property everything
else in this document rests on.

---

## 2. What can still rot

The interesting part. Four risks, honestly ranked.

### (a) The agent-skill format itself — **highest risk**

`SKILL.md` conventions are young and vendor-controlled. If Anthropic (or any client vendor)
changes how skills are discovered, named, or loaded, the package breaks through no fault of
its own — and nothing in this repo can prevent that.

- **Likelihood:** moderate-to-high over a 2–3 year horizon. This is a young format.
- **Impact if it happens:** total, but *shallow*. The content — interview structure, discovery
  rules, verification requirements — is format-independent Markdown. A port is an afternoon of
  reshaping frontmatter and folder layout, not a rewrite.
- **Mitigation already in place:** the package is deliberately portable across clients
  (Claude, Codex), and `design-agent-skill` is the meta-skill for reshaping skills to a new
  format. That is exactly the port tool, and it ships.
- **Honest residual:** it still needs *a person* to notice and do it.

### (b) University site restructuring — **medium risk, slow**

The discovery rules assume things about how university web presences are shaped — that
faculties list chairs, that `site:`-scoped queries reach them, that chair pages name their
holder and research focus.

- **Likelihood:** continuous but slow. Universities restructure sites every few years.
- **Impact:** partial and graceful — a faculty gets thinner results, the tool does not break.
- **Detectable?** Yes, but only by running the eval. This is what the per-semester faculty
  spot-check in §3 exists to catch.

### (c) The discovery rules going stale relative to how students search — **slow**

Degree programmes get renamed, new interdisciplinary centres appear, the vocabulary students
use for their own interests shifts.

- **Likelihood:** slow and steady.
- **Impact:** gradual quality decay, invisible without measurement. The most insidious of the
  four, because nothing ever visibly fails.

### (d) Underlying model drift — **real, and unmeasurable from inside the repo**

The skills steer a model. If the model's behaviour changes, the same rules produce different
output. Every number this project owns was produced by a specific model generation.

- **Likelihood:** certain. Models are replaced constantly.
- **Impact:** unknown in direction — a stronger model may well follow the rules *better*.
- **The honest problem:** the project cannot measure this from inside itself. The simulation
  suite is self-scored by the same model family that generates the turns, so it cannot
  cleanly separate "the rules stopped working" from "the grader changed too." Only the
  ground-truth evals (fixed, human-curated answer keys) can, which is why they matter beyond
  their headline percentages.

**Ranked by what would actually end the project:** (a) breaks it outright; (d) erodes it
invisibly; (b) and (c) degrade it slowly and visibly to anyone who looks. Only (a) requires a
response within weeks.

---

## 3. Minimum viable maintenance contract

The number that makes an institutional handover plausible:

> **One simulation-suite run plus one live faculty spot-check per semester.
> On the order of one to two hours of work, twice a year. Not continuous work.**

Concretely, per semester:

| Step | What | Effort |
|---|---|---|
| 1 | Run the 8-persona simulation suite (`run-thesis-simulations`) against current `main` | ~30–45 min, mostly waiting |
| 2 | Run one faculty's ground-truth eval live, rotating the faculty each time | ~30 min |
| 3 | If either regresses, read the transcript and patch the relevant rule in `references/` | 0–2 h, usually 0 |
| 4 | Re-run `pytest` and the release build; re-publish if a skill changed | ~10 min |

Everything needed for this is in the repo: the ground truth in
`skills/tests/eval_ground_truth/` (architecture-neutral, deliberately untouched by the
pivot), the simulation suite, the eval runbook, and `AGENTS.md` as the operating guide.

**Two honest caveats on this number.** It is an estimate from the maintainer's own runs, not
a measured figure from someone else doing it cold — a first-time maintainer should budget
double. And it buys *detection*, not improvement: it tells you the tool still works. Making it
better is discretionary work nobody is committing to here.

---

## 4. Ownership options, ranked with their real failure modes

### 1. Fachschaft Informatik as institutional home

- **For:** best distribution fit by a distance. They already talk to exactly the students
  this serves, they are a named channel in [MASTERPLAN §7](../../MASTERPLAN.md), and passing
  a link along costs them nothing.
- **Against:** weakest on technical upkeep. Membership turns over annually, so institutional
  memory is roughly one year deep.
- **Realistic failure mode:** it gets shared enthusiastically for two semesters, then the
  people who knew what it was graduate, and the link quietly stops being passed on. Nothing
  breaks; it just stops being mentioned.
- **Verdict:** the right *distribution* home, not a maintenance home. Do not conflate the two.

### 2. A follow-on StudyOS course project

- **For:** natural fit. The course exists, the topic is proven, and a follow-on team inherits
  a working artefact plus an unusually complete evidence trail.
- **Against:** entirely dependent on the course running again *and* on someone choosing this
  topic over a greenfield one — and students generally prefer greenfield.
- **Realistic failure mode:** nobody picks it, because inheriting someone else's architecture
  is less appealing than starting fresh.
- **Verdict:** plausible, not plannable. Worth making easy — the handover documents are the
  work that makes it possible — but it cannot be relied on.

### 3. A named chair or the Studienberatung

- **For:** by far the most durable. Institutions outlive cohorts, and Studienberatung's remit
  genuinely overlaps with what this does.
- **Against:** highest approval cost. An institution adopting a tool takes on an implicit
  quality guarantee, and this tool explicitly does not guarantee coverage.
- **Realistic failure mode:** it never gets adopted, because the approval cost exceeds the
  perceived benefit and nobody has an incentive to push it through. Alternatively, it *is*
  adopted, and then the "not an official University of Tübingen service" disclaimer in
  INSTALL.md becomes a problem someone has to resolve.
- **Verdict:** the best outcome and the least likely. Requires someone inside to actively
  want it — which is precisely what the AD channel question to Menth/Gehler is trying to find
  out, and the honest answer today is that we do not know.

### 4. Domi as unpaid maintainer

- **For:** zero coordination cost, full context, and the per-semester contract in §3 is
  genuinely small.
- **Against:** the well-documented half-life of unpaid post-graduation maintenance.
- **Realistic failure mode:** it works for two or three semesters while the project is still
  personally interesting, then a job and other commitments win. This is the normal outcome,
  not a character flaw, and planning as if it were not would be dishonest.
- **Verdict:** the realistic bridge for 1–2 years, not the answer. Worth stating as a
  time-boxed commitment rather than an open-ended one.

### 5. No owner — **the default, and the one worth taking seriously**

This is where the architecture pays off.

**Because there is no database, no backend and no scraper, "no owner" does not mean "broken."**
It means the discovery rules stop improving. The tool keeps interviewing students, keeps
searching the live web, and keeps returning verified options — against a web that has moved on
a little further each semester. Quality decays slowly along risks (b) and (c) rather than
failing on a specific date.

The one exception is risk (a): if the skill format changes incompatibly and no one ports it,
the package stops loading. That is the single scenario where "no owner" means "dead," and it
is the reason the format risk is ranked first.

**This should be stated plainly in the report rather than dressed up.** Most student projects
end here. The difference this architecture makes is not that it finds an owner — it is that
the null outcome degrades gracefully instead of failing, and that is a design achievement
worth claiming.

---

## 5. What would actually have to be true for survival

Three conditions. Two exist, one does not.

| # | Condition | Status today |
|---|---|---|
| 1 | **One named person or body who wants it** | ❌ **Does not exist.** No one has been asked directly yet. The AD channel question to Menth/Gehler is the nearest thing, and it asks about *distribution*, not ownership. This is the gap. |
| 2 | **A documented handover** | ✅ **Largely exists.** `AGENTS.md` (maintainer and agent operating guide), `INSTALL.md` (end-user install, cold-tested), the final 1.0 plan, this document, and a dense dated `findings/` trail. A competent successor could pick it up without talking to anyone. |
| 3 | **One distribution channel that keeps pointing at it** | 🟡 **Pending.** Fachschaft Informatik is identified and the recruiting/outreach texts are written, but **not yet sent** (Task AD / Z′ blocker as of 2026-08-09). Until they go out, condition 3 is aspiration. |

**Condition 1 is the honest gap, and it will not be closed by writing documents.** It requires
asking a specific person or body whether they want this — a conversation nobody has had. The
recommendation for the remaining project time is narrow and concrete: **when the AD channel
question goes to Menth/Gehler, ask a second question alongside it** — not "will you
distribute this," but "is there a body for whom owning something like this would make sense?"
A no is a useful, reportable answer. Not asking is not.

---

## 6. What this means for the report

Three claims this chapter supports, each defensible:

1. **G1 — the architecture decision in hindsight.** The rules-only pivot was made on product
   grounds and turned out to be the sustainability decision. That is a genuine finding about
   the design, and it is stronger for having been arrived at sideways rather than planned.
2. **G3 — design rationale.** "Maintenance-free" was a founding constraint from
   MASTERPLAN §1 that the first two architectures quietly violated. The third one honours it,
   and CI enforces it. The design story is a constraint being taken seriously on the third
   attempt.
3. **G5 — future development.** The maintenance contract is a number, the ownership options
   carry named failure modes, and the honest default — no owner, graceful degradation — is
   stated rather than avoided.

The one thing the report should **not** claim is that the project has a future owner. It does
not, and §5 says why.
