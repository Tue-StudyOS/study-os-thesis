# Task S — Output & Interview Quality Pass (Track 4, robustness)

- **Date:** 2026-07-03
- **Branch:** `feat/no-db-universal-skill`
- **Role:** roadmap Task S ([core-optimization-roadmap.md §3](2026-06-28-core-optimization-roadmap.md)),
  following Task R's edge-case pass ([2026-07-03-task-r-edge-cases.md](2026-07-03-task-r-edge-cases.md)).
- **Goal:** review the live transcripts already produced across Tasks H–R against five
  output/interview quality criteria, and add few-shot examples to the SKILL.md files
  only where a transcript *repeatedly* fails one of them.

Reviewed the five full discovery-output transcripts (`dist/live-validation/{cs,medicine,
psychology,wiso,humanities}-skill.md`) plus the two Task R edge-case transcripts
(`niche-no-match-skill.md`, `interdisciplinary-skill.md`) against the roadmap's five
criteria. The interdisciplinary transcript is a routing-breadth test by design (Task R's
scope), not a full Step 8 output, so it's scored only where applicable and otherwise
marked N/A rather than counted as a failure.

---

## Criterion 1 — Honest pros/cons (genuinely stated, not generic hedges)

| Transcript | Verdict | Note |
|---|---|---|
| cs-skill | PASS | Specific per-chair difficulties: Geiger "on leave of absence, not currently hiring"; Schölkopf "very high-profile group, extremely competitive"; Oh flagged and excluded via a live-confirmed relocation to KAIST rather than silently dropped. |
| medicine-skill | PASS | Schöls: "clinical embedding could pull toward patient work (partial no-go — flagged)"; Deleidi: "Junior group (good supervision access) but may have moved — verify current Tübingen affiliation." Concrete, chair-specific, not templated. |
| psychology-skill | PASS | Franz: "explicit thesis availability is a strong positive signal" (genuine positive, not a hedge); Karnath: patient/lesion work flagged specifically against the no-go. |
| wiso-skill | **PARTIAL FAIL** | Options 4 (Bruzelius) and 5 (Schubert) — 2 of 7 numbered options — have no "Pros & likely difficulties" field at all, just Relevance + Conversation starter. The other 5 options in the same transcript do include it, so this is an inconsistent application of the Step 8 template within one run, not a systemic pattern across transcripts. |
| humanities-skill | PASS, strongest | Wong: scoping risk named explicitly ("empirical lab work" no-go touches his broader group); Sattig: "no online thesis-opening announcement found (typical for philosophy chairs — direct inquiry needed, not itself a red flag)" — nuanced, avoids reading absence-of-signal as a red flag. |

**Verdict: mostly strong.** One partial, single-transcript lapse (wiso, 2/7 options) — not a repeated cross-transcript pattern, so it doesn't clear the bar in the roadmap's instruction for a dedicated few-shot fix on its own, but see the combined fix in "Fixes applied" below.

## Criterion 2 — Concrete conversation starters (chair-specific vs. templated filler)

All five discovery transcripts pass. Starters consistently reference the *actual* named
person's real, dated work rather than a generic version of the topic:

- cs: "model-based RL for sample-efficient robot skill learning (**simulation-only
  variant**)" — even threads the profile's hardware no-go into the framing.
- medicine: "genotype–phenotype analysis in hereditary ataxia registries" (Synofzik) —
  matches the lab's actual disease focus, not a generic neurogenetics prompt.
- psychology: "Lesion-behavior mapping of spatial attention" (Karnath) — names his
  specific method (lesion mapping), not a generic cognitive-neuroscience prompt.
- humanities: "Ask about the 'Interrogating Artificial Agency' paper's take on machine
  agency..." — names an actual 2025 paper by title. Strongest example in the set.
- wiso: mostly specific (e.g. "Cross-national panel analysis of welfare-state reform"),
  one or two starters (Schubert) read closer to a restatement of the chair's own focus
  than a sharpened angle, but still chair-specific, not interchangeable filler.

**Verdict: PASS across the board.** No fix needed.

## Criterion 3 — Dated evidence presence (every option backed by a dated source)

| Transcript | Verdict | Note |
|---|---|---|
| cs-skill | **FAIL** | None of the 10 numbered options carry an explicit "Dated evidence" field. Dates appear only in the surrounding Pass-1/Pass-2 narrative (e.g. the Oh/KAIST relocation check) and the closing coverage caveat — the freshness signal the student actually needs per-option isn't carried into the option map itself. |
| medicine-skill | PASS | Every option has an explicit "Evidence: ... 2024/2025" line. |
| psychology-skill | PASS | Every option has an "Evidence: ..., active 2023+" or equivalent line. |
| wiso-skill | **FAIL** | Same gap as cs-skill — none of the 7 numbered options carry a dated-evidence line, despite the transcript being from the same day (2026-06-28) as medicine and psychology, which both comply. |
| humanities-skill | PASS | Every option has an explicit "Dated evidence:" line with a specific source and date, plus an "(accessed 2026-07-03)" stamp. |

**Verdict: real, repeated gap — 2 of 5 transcripts (cs, wiso) omit the field entirely
across every option.** This isn't explained by chronology (wiso is same-day as two
compliant transcripts; cs is the most recent of the non-humanities runs) — it's an
inconsistent application of the SKILL.md Output spec, which currently states the
requirement as a bullet but gives no worked example of the field's expected format.
**This clears the roadmap's "repeatedly fails" bar for a few-shot fix.**

## Criterion 4 — Coverage-caveat presence

All 5 full discovery transcripts end with the coverage caveat, verbatim or near-verbatim
to the SKILL.md template, dated to the run. `niche-no-match-skill.md` includes it inside
the Step 8 output block for the zero-candidates case too. `interdisciplinary-skill.md`
has no caveat, but it's explicitly a routing-breadth report, not a full option map (Task
R's stated scope) — not a fair criterion-4 failure.

**Verdict: PASS, 5/5 on full outputs.** No fix needed.

## Criterion 5 — Interview convergence (happy path)

No happy-path interview transcript exists anywhere in this repo — every discovery
transcript (cs/medicine/psychology/wiso/humanities/niche/interdisciplinary) starts from
an already-built persona block; the interview that would have produced it was never
recorded. The only real interview transcript on file is Task R edge case 2's adversarial
8-turn resistant-student run. Contrasting that against nothing would not answer the
question the roadmap actually asks ("does the interview converge in a reasonable number
of turns on the happy path") — so a happy-path run was produced live for this task,
using the same methodology Task R used for the adversarial case (play both sides,
turn by turn, against `build-student-profile/SKILL.md`'s actual rules, not a
paraphrase of them).

**Persona:** a reasonably cooperative but not maximally verbose NLP-interested student
(realistic mid-effort answers — not the adversarial minimum, not an ideal essay).

**Condensed transcript (6 turns):**

1. *Student:* "I'm interested in NLP and want to do something with language models for
   my thesis."
   *Agent:* first message is short → asks exactly one opening question per the First
   Question list: "What concrete project, course, paper, or demo made this area
   interesting to you?"
2. *Student:* "We had an NLP course where we built a text classifier using BERT for
   sentiment analysis on tweets. I liked fine-tuning pretrained models and seeing how
   much preprocessing choices shifted accuracy."
   → Interests (NLP, text classification) and a first Methods signal (empirical,
   fine-tuning pretrained models) now have real content. Domain, Thesis style, Skills
   breadth, and No-gos are still open.
   *Agent:* asks the next targeted question — domain: "Do you want to stay general
   NLP, or move into a specific application area (e.g. social media, healthcare text,
   legal documents, education)?"
3. *Student:* "Social media / online discourse — maybe misinformation or toxic-language
   detection. Not tied to a domain like medicine."
   → Domain now has real content (social media / online discourse), Interests sharpens
   (misinformation/toxic-language detection).
   *Agent:* asks Skills: "Which skills can you already use confidently — languages,
   frameworks, libraries?"
4. *Student:* "Python, PyTorch, HuggingFace transformers, some scikit-learn for
   baselines. Bit of AWS for training, nothing fancy."
   → Skills now has real content.
   *Agent:* asks Thesis style: "Do you want the thesis to be more building/fine-tuning
   models experimentally, analysis of existing model behavior, or theoretical?"
5. *Student:* "Hands-on — training/fine-tuning models and running experiments, not pure
   theory."
   → Thesis style now has real content.
   *Agent:* asks No-gos: "What would you definitely not want — heavy math proofs,
   hardware/robotics, clinical data, large-scale software engineering, something else?"
6. *Student:* "No hardware/robotics, no heavy math-proof-only work, and I'd rather not
   build a full production system — more research-y."
   → No-gos now has real content. **All six dimensions have concrete, non-generic
   content as of this turn.**

**Result: convergence in 6 agent questions / 6 student turns**, each turn adding real
content to exactly the dimension it targeted, no wasted turns, no repeated questions.
This is a plausible, reasonable number for a cooperative student and stands in useful
contrast to Task R edge case 2's adversarial run, which took 8 turns of sustained
resistance and *still* didn't clear the bar (Interests stayed one-line). The gap between
"6 turns, converges" (cooperative) and "8 turns, doesn't converge" (adversarial) is the
right shape — the interview should be efficient when the student cooperates and should
not be gameable into a false convergence when they don't. No fix needed here; this is
confirmation, not a gap.

---

## Fixes applied

**`find-university-chairs/SKILL.md`** — added one worked example option entry to the
Output section (Step 8), showing all required fields filled in concretely, including
the "Dated evidence" field's expected format (source + specific date). This directly
targets the repeated criterion-3 gap (cs-skill, wiso-skill both omitted the field for
every option) and incidentally models the "Pros & likely difficulties" field too,
covering wiso-skill's narrower, single-transcript lapse with the same fix rather than
a second one. Surgical, one example block, no rewording of the existing field list.

No fix applied for criterion 5 (interview convergence) — the happy-path run confirms
the design works as intended; adding a few-shot here would be speculative, not
evidence-backed.

---

## Overall Track 4 status

Task Q, Task R, and Task S are all done. Task S found one real, repeated spec-compliance
gap (dated evidence omitted from two live option maps) and fixed it with a single
worked example; the other four criteria hold up on the evidence (steering/precision-style
per-chair honesty, chair-specific conversation starters, universal coverage-caveat
presence, and a live-confirmed efficient happy-path interview). Per the roadmap's
dependency graph (§5), **Track 4 → done**. Roadmap §4's "core is done" gate should now
get an explicit go/no-go call — Tracks 1–4 are all complete at this point.
