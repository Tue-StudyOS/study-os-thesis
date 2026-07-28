# Task M — Acting on the Gehler Feedback

- **Date:** 2026-07-05
- **Branch:** `feat/no-db-universal-skill`
- **Read first:** [`docs/thesis-report/04-open-work/2026-07-04-feedback-gehler.md`](../../docs/thesis-report/04-open-work/2026-07-04-feedback-gehler.md)
  (raw feedback) and [`docs/thesis-report/04-open-work/README.md`](../../docs/thesis-report/04-open-work/README.md)
  (synthesis — three signals extracted, not yet acted on)

This plan turns the three feedback signals from the informal Gehler test session into three
concrete, independent skill-change tasks. Each task is written to be handed to a single agent
run in its own conversation. **M4 (professor-input coverage-caveat wording) was considered and
dropped by Domi — not part of this plan.**

Order: **M1 → M3 → M2** (small/independent first, then the change M2 depends on conceptually
— M2 reuses the paper-surfacing idea that M3 formalizes in `draft-thesis-contact`, so doing M3
first means M2 can point to the finished pattern instead of inventing its own).

---

## Task M1 — Upfront framing in `thesis-finder`

- **Goal:** Fix the "not clear how much detail was required at which step" signal. Add a
  one-time, upfront framing message at the start of the New User Flow, before the interview
  begins: what the skill does, that answer detail level is the student's choice, and that the
  track choice (university / company / both) comes after the interview.
- **Wording constraint (Domi, 2026-07-05):** this skill covers thesis work in general, not
  only Master's theses — use "thesis" (or the project's existing generic phrasing, see
  `build-student-profile/SKILL.md` "thesis level and program"), never "Masterarbeit" or
  "Master's thesis" in this new message. Check the rest of `thesis-finder/SKILL.md` for the
  same drift before finishing (the skill is meant to be level-agnostic).
- **Depends on:** nothing. Parallel-safe.
- **Files:** `skills/thesis-finder/SKILL.md` (New User Flow, before Step N1).
- **Steps:**
  1. Insert a short intro message (2-3 sentences) shown once, before Step N1's interview
     starts: states what the skill does, that more detail helps but isn't required, and that
     the track question comes after the profile is built.
  2. Grep `skills/thesis-finder/SKILL.md` for "Master" / "Masterarbeit" and fix any
     Master-specific wording found outside query-string contexts (query strings like
     `Masterarbeit OR Abschlussarbeit` in other skills are out of scope — only fix
     `thesis-finder/SKILL.md` itself).
  3. Do not touch Step N2 (track question) or the interview logic in `build-student-profile` —
     this task is additive framing only.
- **Done-when:** re-reading `thesis-finder/SKILL.md` New User Flow shows the framing message
  before Step N1; no "Masterarbeit"/"Master's thesis" language remains in that file; nothing
  else in the flow changed.
- **Agent prompt (paste into a fresh conversation):**

  > Branch: `feat/no-db-universal-skill` (already checked out). This is Task M1 from
  > `findings/no_db_universal_skill/2026-07-05-taskM-gehler-feedback-plan.md` — read that
  > file's Task M1 section first, plus `docs/thesis-report/04-open-work/2026-07-04-feedback-gehler.md`
  > for the original feedback context. Also skim `skills/thesis-finder/SKILL.md` in full and
  > `skills/build-student-profile/SKILL.md` for the project's existing generic "thesis"
  > wording convention (it explicitly supports Bachelor's and Master's, not just Master's).
  >
  > Task: add a one-time upfront framing message to `skills/thesis-finder/SKILL.md`'s New User
  > Flow, shown before Step N1's interview begins. It must state: (a) what the skill does, (b)
  > that the student's answer detail level is their own choice — more detail helps but isn't
  > required, (c) that the university/company/both track choice comes after the profile is
  > built. Use generic "thesis" wording throughout — this covers Bachelor's and Master's theses,
  > not only Master's ("Masterarbeit" wording is wrong here). While in the file, grep for any
  > other Master-specific phrasing in `thesis-finder/SKILL.md` and fix it too. Do not change
  > Step N2, the routing logic, or `build-student-profile`.
  >
  > Commit in small steps as you go (this repo's CLAUDE.md asks for frequent small commits with
  > descriptive messages, not one giant commit). Verify by re-reading the edited section. Update
  > `STATUS.md` with a dated log line noting Task M1 is done. Model: `claude-sonnet-4-6` is
  > sufficient (small, well-scoped text edit). At the end, emit your own next-step handoff
  > prompt for whichever of Task M2/M3 is still open, per this repo's CLAUDE.md §7 format.

---

## Task M3 — Paper-first gate in `draft-thesis-contact`

- **Goal:** Fix part of Domi's own idea (feedback file, "Meine Ideen" section): before
  drafting a first-contact email, make sure the student has been pointed to 1-2 relevant
  recent papers from the target person/lab and explicitly encouraged to skim them first —
  because arriving uninformed about what the researcher actually works on reads badly and
  undermines exactly the kind of high-signal contact this skill is trying to produce.
- **Depends on:** nothing structurally, but do this before M2 so M2 can reuse the pattern
  instead of re-deriving it.
- **Files:** `skills/draft-thesis-contact/SKILL.md`; may call `skills/find-recent-papers` if
  papers were not already surfaced upstream (check that skill's interface first — read its
  SKILL.md before wiring the call).
- **Steps:**
  1. Add a workflow step before drafting: if 1-2 relevant recent papers for the chosen
     person/lab are not already present in-session (e.g. from a prior `find-university-chairs`
     or `find-company-thesis-options` run, or a M2 drill-down), invoke `find-recent-papers` to
     get them.
  2. Explicitly recommend the student skim these before sending, and say briefly why (shows
     genuine engagement with the researcher's actual work, not a generic template).
  3. Reflect this in the Output section: add the paper pointers + the skim-first recommendation
     to the existing checklist output, rather than inventing a new output section.
  4. Keep changes surgical — do not restructure the email-drafting logic itself.
- **Done-when:** re-reading `draft-thesis-contact/SKILL.md` shows the paper-first step wired in
  before drafting, and the Output section reflects it; existing draft-quality rules (modest
  claims, no invented openings) are untouched.
- **Agent prompt (paste into a fresh conversation):**

  > Branch: `feat/no-db-universal-skill` (already checked out). This is Task M3 from
  > `findings/no_db_universal_skill/2026-07-05-taskM-gehler-feedback-plan.md` — read that
  > file's Task M3 section first, plus the "Meine Ideen" section of
  > `docs/thesis-report/04-open-work/2026-07-04-feedback-gehler.md` for the original idea. Also
  > read `skills/draft-thesis-contact/SKILL.md` in full and `skills/find-recent-papers/SKILL.md`
  > to understand its calling interface before wiring anything.
  >
  > Task: add a step to `draft-thesis-contact/SKILL.md`'s workflow, before the email is
  > drafted, that ensures 1-2 relevant recent papers from the target person/lab are surfaced
  > (call `find-recent-papers` if they aren't already available in-session) and that the
  > student is explicitly told to skim them first, with a one-line reason why (shows genuine
  > engagement, avoids reading as generic). Add this to the existing Output checklist rather
  > than inventing a new section. Do not touch the rest of the drafting logic or its existing
  > rules (modest claims, no invented openings/funding/capacity).
  >
  > Commit in small steps. Verify by re-reading the edited file. Update `STATUS.md` with a
  > dated log line noting Task M3 is done, and note whether M1 is already done (check the log)
  > so you don't duplicate a STATUS entry. Model: `claude-sonnet-4-6` is sufficient. At the end,
  > emit your own next-step handoff prompt for Task M2 (the remaining task in this plan), per
  > this repo's CLAUDE.md §7 format — mention that M2 can reuse the paper-surfacing pattern you
  > just built in `draft-thesis-contact`.

---

## Task M2 — Recommend & drill-down step in `thesis-finder`

- **Goal:** Fix the "tell me which one you would choose and walk a bit more down that road"
  signal. After `thesis-finder` delivers the option map(s) from `find-university-chairs`
  and/or `find-company-thesis-options`, add a step that (1) recommends 1-2 top candidates with
  a brief rationale, (2) asks whether the student wants to go deeper on one before drafting
  contact, and (3) if yes, drills down: surfaces what the student would concretely work on /
  learn there, using 1-2 recent papers from that group (reuse the `find-recent-papers` pattern
  from Task M3) — before offering `draft-thesis-contact`.
- **Depends on:** Task M3 (reuses its paper-surfacing pattern so the drill-down and the
  pre-email gate don't diverge in how they fetch/present papers). Read Task M3's final diff
  before starting.
- **Files:** `skills/thesis-finder/SKILL.md` (Step N4/N5 in New User Flow, R5/R6 in Returning
  User Flow — both flows currently just offer `draft-thesis-contact` with no ranking step, this
  must be fixed in both), possibly `skills/find-recent-papers/SKILL.md` if the calling
  convention needs a small addition to support a "papers for this specific chair/lab" query
  (do not change its core logic, only add a call pattern if genuinely missing).
- **Steps:**
  1. In New User Flow, insert a step between "deliver option map" (end of Step N3) and "offer
     next step" (Step N5): rank/recommend 1-2 options from the map with a short "why this one"
     line grounded in the student's profile — do not invent information not already in the map.
  2. Ask the student: continue exploring, or go deeper on the recommendation?
  3. If "go deeper": drill-down using the pattern from Task M3 — 1-2 recent papers from the
     group, plus a concrete "what you'd likely work on / learn" summary derived from the
     option's existing relevance rationale and the papers, not invented.
  4. Only after the drill-down (or if the student declines it) does Step N5's
     `draft-thesis-contact` offer apply.
  5. Apply the same insertion to the Returning User Flow (R4→R5→R6) so a returning student who
     asks for a fresh map also gets the recommendation/drill-down step, not just first-time
     users.
  6. Update the Session File Format if the recommended/chosen option should be tracked across
     sessions (optional — only add a field if it's a small, clearly justified addition; do not
     redesign the session file schema).
- **Done-when:** re-reading both flows in `thesis-finder/SKILL.md` shows recommend → ask →
  (optional) drill-down → offer-contact, in that order, in both New User and Returning User
  flows; no invented facts introduced (recommendation and drill-down must be traceable to
  the option map's own fields or to papers actually fetched).
- **Agent prompt (paste into a fresh conversation):**

  > Branch: `feat/no-db-universal-skill` (already checked out). This is Task M2 from
  > `findings/no_db_universal_skill/2026-07-05-taskM-gehler-feedback-plan.md` — read that
  > file's Task M2 section first (note it depends on Task M3, already merged — check
  > `STATUS.md`'s dated log for the M3 entry and read the current
  > `skills/draft-thesis-contact/SKILL.md` to see the paper-surfacing pattern M3 built, so you
  > reuse it instead of inventing a new one). Also read
  > `docs/thesis-report/04-open-work/2026-07-04-feedback-gehler.md` (the "What was missing for
  > you to take a real next step" section) for the original feedback this addresses, and read
  > `skills/thesis-finder/SKILL.md` in full (both New User Flow and Returning User Flow — the
  > option-map-to-next-step gap exists in both).
  >
  > Task: add a recommend-and-drill-down step to `thesis-finder/SKILL.md`, inserted after the
  > option map is delivered and before `draft-thesis-contact` is offered, in **both** flows
  > (New User Step N3→N5, Returning User R4→R6). The step must: (1) recommend 1-2 top options
  > from the map with a short rationale grounded only in information already in the map — no
  > invented facts, (2) ask the student whether they want to go deeper on the recommendation or
  > keep exploring, (3) if deeper: surface 1-2 recent papers from that group (reuse
  > `find-recent-papers` the way `draft-thesis-contact` now does) plus a concrete "what you'd
  > likely work on/learn" summary derived from the map's relevance rationale and the papers, (4)
  > only then offer `draft-thesis-contact`. Read `skills/find-recent-papers/SKILL.md` first to
  > confirm its calling interface before wiring calls into it.
  >
  > Commit in small steps. Verify by re-reading both edited flows end-to-end. Update
  > `STATUS.md` with a dated log line noting Task M2 is done and that this closes out the Task M
  > (Gehler feedback) plan — check whether M1 and M3 log entries are both present first. Model:
  > `claude-sonnet-4-6` first pass; escalate to `claude-opus-4-8` if the two-flow edit gets
  > tangled or the drill-down logic feels muddled on first read-back. At the end, emit a
  > handoff prompt only if there's a natural next task to pick up — otherwise state plainly
  > that Task M is complete and summarize what changed across M1/M2/M3.

---

## What this plan deliberately does not do

- **M4 (professor-input coverage-caveat wording)** — considered, dropped by Domi (2026-07-05).
  Not part of this plan; do not add it as a surprise scope addition in any of the three tasks
  above.
- **Round-mail to professors asking for skill-specific info** — stays out of scope per the
  no-DB principle, as already recorded in `docs/thesis-report/04-open-work/README.md`.
- **Example walkthrough / example-prompts onboarding content** — was part of the original M4
  bundle; also dropped along with it, not silently folded into M1-M3.
