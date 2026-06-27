# Status — StudyOS Thesis-Finder

> **This is the only continuously updated file.** Here we collect progress, blockers, difficulties, and decisions. The stable overall plan is in [MASTERPLAN.md](MASTERPLAN.md).
>
> **Convention:** When working on a task, change its status here, note difficulties, and add a dated line to the log below. Do not edit the Masterplan.

**Last update:** 2026-06-27

---

## Current phase

**Phase 1 — University discovery (database-less).** Goal: a faculty-agnostic
discovery skill that maps a student's interests to Tübingen thesis options via
live search, measured against a small ground truth and a plain-Claude baseline.

Direction details: [findings/no_db_universal_skill/](findings/no_db_universal_skill/)
· exact build plan:
[2026-06-26-build-plan.md](findings/no_db_universal_skill/2026-06-26-build-plan.md).

---

## Task status

Legend: ⬜ open · 🟨 in progress · ✅ done · ⛔ blocked

| Task | Step | Status | Owner | Notes / difficulties |
|---|---|---|---|---|
| A | Conversation discipline in `build-student-profile` | ✅ | Domi | One-question rule + precise-answer instruction + no-search gate added to SKILL.md. |
| B | Faculty backbone reference (Tübingen listing URLs) | ✅ | Domi | All 7 faculties + ZITh covered; ≥1 official listing URL each, 6 spot-checked live. |
| C | Search-strategy reference (profile → queries) | ⬜ | – | The core IP. Depends on B. |
| D | Rework `find-university-chairs` into universal discovery skill | ⬜ | – | Map output, pros/cons, coverage caveat; drop seed-list. Depends on B, C. |
| E | Retire DB assets (match-thesis-advisors, openalex index, seed data → eval) | ⬜ | – | Do after D so replacement exists. |
| F | Eval ground truth for 3–4 faculties + metric | ⬜ | – | Recall target ≥70%; reuse CS curated data. |
| G | Wire discovery into Max's multiturn harness (skill vs. baseline) | ⬜ | – | Port from `eval/auto_eval_agents` (ed341a7). Depends on D, F. |
| H | Run eval, measure coverage & skill-vs-baseline delta, document | ⬜ | – | Depends on G. Be honest about weak spots. |

**Gate Phase 1 → 2:** skill runs end-to-end with no DB · ground truth for ≥3
faculties · harness reports coverage + baseline comparison · coverage ≥70% on the
sample.

---

## Open decisions

- **Coverage target:** start at ≥70% recall on the ground truth — revisit after
  first eval (Task H).
- **Discovery skill name:** reworking `find-university-chairs` in place for now;
  consider a faculty-agnostic rename once companies arrive (Phase 2).
- **Company list source (Phase 2):** which existing tagged list for
  Baden-Württemberg, and the bundling format — deferred until the university arm
  is proven.

---

## Known difficulties / risks

- **Web-search coverage gaps** — chairs with weak/outdated web presence are
  silently missed. Mitigation: faculty-backbone crawl (Task B) + honest in-output
  caveat.
- **Beating plain Claude** — must be shown empirically, not assumed (Tasks G/H).
- **Profile must actually steer the search** — if the interview doesn't change the
  queries, the skill adds nothing (Tasks C/D).
- **Company discovery is a different, harder problem** — deliberately deferred to
  Phase 2.
- **Personal data (GDPR)** — surfaced researcher names + areas are public academic
  data; nothing student-private is ever stored (profile stays in-context only).

---

## Log

- **2026-06-27** — Task B done. Created
  `skills/find-university-chairs/references/tuebingen-faculty-backbone.md`: a
  reviewable table of all 7 Tübingen faculties + the Center for Islamic Theology,
  each with ≥1 official `uni-tuebingen.de` listing URL (Medicine on
  `medizin.uni-tuebingen.de`), page language, how chairs are listed, and a
  2026-06-27 last-checked date. Documented the two/three-level
  faculty→Fachbereich→chair nesting and per-department drill-down pattern. Spot-checked
  6 URLs live (faculties index, science & humanities Fachbereiche, WiSo Fächer, law
  Lehrstühle, Protestant-theology Lehrstühle) — all resolve and list real units.

- **2026-06-27** — Task A done. Edited `skills/build-student-profile/SKILL.md`: added one-question-per-turn rule, precise-answer instruction, and no-search gate (all six profile dimensions required before discovery). Surgical changes only; no other behavior modified.

- **2026-06-26** — Pivoted to the database-less, university-wide direction.
  Created branch `feat/no-db-universal-skill` off
  `codex/chair-discovery-eval-from-valentin`. Wrote
  [VISION_NO_DB.md](VISION_NO_DB.md) and the findings set under
  `findings/no_db_universal_skill/` (concept-and-risks, exact build plan).
  Rewrote MASTERPLAN around Phase 1 = university discovery (Tasks A–H) and reset
  this STATUS. Located Max's multiturn eval harness on branch
  `eval/auto_eval_agents` (commit `ed341a7`) for the skill-vs-baseline comparison.
  Old DB data-foundation epic (issues #45–#51) is superseded; to be closed and
  replaced by issues mirroring Tasks A–H.

---

## Archived: former DB data-foundation phase (superseded 2026-06-26)

The previous Phase 1 built a scraped researcher tree (Prof → PhD → Paper) for CS
Tübingen with monthly refresh automation (issues #45–#51). It is superseded by the
database-less direction. The curated 3-pilot-chair ground truth and CS chair data
are retained as **eval-only** material (Task F). History remains in git.
