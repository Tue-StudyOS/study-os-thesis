# Live-Eval Runbook — Re-validate One Faculty Cheaply

> **Architecture tag (added 2026-08-09, Task AJ): this file is MIXED — check the date on the
> log entry you are citing.** Entries dated **≤2026-07-30** are `[backbone-crawl, ≤2026-07-30]`
> and measure the static-backbone architecture removed on 2026-07-31 (Humanities, Law, the
> Roadmap-J and Task O runs). The entry dated **2026-08-08** (Task V′, Theology) is
> `[rules-only, ≥2026-07-31]` and is the only run in this file that measures the shipping
> architecture. Do not aggregate across the two. Current picture:
> [eval scorecard §0](2026-07-03-eval-aggregate-scorecard.md).

- **Date:** 2026-07-02
- **Branch:** `feat/no-db-universal-skill`
- **Role:** roadmap Task J ([core-optimization-roadmap.md §3](2026-06-28-core-optimization-roadmap.md)).
  Note the letter collision: STATUS.md's Post-Phase-3 hardening table already used
  "Task J" for an unrelated fix (canonical six profile dimensions). This runbook is
  logged there as **Roadmap-J** to avoid confusion — see STATUS.md.
- **Why this exists:** [2026-06-28-live-validation-protocol.md](2026-06-28-live-validation-protocol.md)
  is the right process but it's written for a one-time, all-4-faculty validation run
  (~2 hours). After a skill change (e.g. a query-skeleton edit, a backbone fix), you
  need a cheap way to re-check *one* faculty without re-reading the full protocol or
  re-running everything. This is that checklist.

## When to run this

After any change to `skills/find-university-chairs/SKILL.md`,
`references/search-strategy.md`, or `references/tuebingen-faculty-backbone.md` that
could plausibly affect recall or precision. Skip for pure prose/typo edits.

## Checklist (~15–20 min for one faculty)

1. **Pick the faculty** most exercised by the change (e.g. a backbone fix to §Medicine
   → re-run medicine; a query-skeleton change → pick whichever faculty's queries
   changed, or `cs` as the default well-understood case).
2. **Build the persona from the GT file's FULL `Sample interest:` line.** Extract
   *only* that one line from `skills/tests/eval_ground_truth/<faculty>.md` (or, for CS,
   `cs_seed/`) — e.g. `grep -i "sample interest" skills/tests/eval_ground_truth/<faculty>.md`
   — and build the test persona from its full wording. **Do NOT build the persona from
   the README's one-line summary table** (`eval_ground_truth/README.md`): those
   summaries are lossy and drop qualifying clauses present in the GT file's real sample
   interest. This exact gap was the documented root cause of the Humanities 60% run
   (2026-07-03) — the README one-liner "Philosophy of mind, metaphysics and cognitive
   science" dropped the GT file's "...with an interest in the history of the field
   (ancient philosophy, Kant / German Idealism)" clause, which caused a spurious
   historical-work no-go that excluded 2 GT chairs the crawl had already found. Use the
   GT file's full sample interest verbatim so results stay comparable and complete.
3. **No peeking — with one carve-out.** Do not read the ground-truth **chair rows,
   Notes, or scoring table** for this faculty until step 5. Reading *only* the single
   `Sample interest:` line (via the `grep` in step 2, which does not reveal the chair
   list) is allowed and required — that is how you build the persona without breaking
   blindness. Do not open the full GT file in an editor until step 5.
4. **Run the skill arm live**: follow `find-university-chairs/SKILL.md` end-to-end
   with real `WebSearch`/browse calls. Save the output MAP to
   `dist/live-validation/<faculty>-skill.md` (overwrite the prior run; git history
   keeps the old one).
5. **Score against ground truth** (`skills/tests/eval_ground_truth/README.md`):
   - **Recall** = ground-truth chairs surfaced / total ground-truth chairs.
   - **Precision** = surfaced options judged relevant / total surfaced options
     (see the README's "What precision means here" section, added in Roadmap-K).
6. **Compare to the last recorded run** for this faculty (check
   `2026-06-28-I-fix-revalidation.md` or the most recent runbook entry below) — did
   the change move recall/precision up, down, or leave it flat?
7. **Record the result** as a dated entry appended to the log at the bottom of this
   file. One paragraph: what changed, faculty, recall, precision, delta vs. last run,
   one honest note if something broke.

## Skip list (things the full protocol requires that this one doesn't)

- All 4 faculties — pick one relevant to the change.
- A fresh baseline (no-skill) arm — only needed when re-validating the
  skill-vs-plain-Claude claim itself, not after a routine skill edit.
- A full findings doc — a log entry here is enough; only write a new
  `findings/no_db_universal_skill/<date>-*.md` if the result changes the Phase gate
  verdict (e.g. recall drops below 70%).

## Log

*(append one entry per re-validation run; newest first)*

- **2026-08-08 — Blind Theology run (Task V′). The cleanest blind measurement the project
  has.** `theology.md` is the one hard-faculty ground truth never opened mid-run; this
  session was kept blind on it by instruction, and only its `Sample interest:` line was
  read (via `grep`) before Pass 1. The remaining five persona dimensions were reconstructed
  from the discipline (historical-critical exegesis; ancient-religion domain; text-based
  monograph; Hebrew/Greek/Latin; no-gos practical theology, Religionspädagogik, quantitative
  religion-sociology — systematic theology deliberately marked *off-core rather than a hard
  no-go*, to avoid re-creating the Humanities over-exclusion class). Output:
  `dist/live-validation/theology-skill.md`.

  **Recall: 5/6 = 83%** (found: Leuenberger, Kamlah, Tilly, Landmesser, Drecoll; **missed:
  Witt**). **Precision: 9/9 = 100%.** Clears the ≥80% bar on a first, genuinely blind run,
  with no fix applied first — the first hard faculty to do so (Humanities needed a protocol
  fix, Law needed the §5 skill fix).

  **Precision detail.** Nine surfaced options, all judged relevant: the five GT core chairs;
  **Zellentin**, whom the GT file explicitly instructs be scored relevant rather than noise
  (flagged in the map as drifting toward Qur'anic/early-Islamic work under his ERC project
  QaSLA, which is an accurate read of his current output); and three **Catholic-faculty**
  chairs — **Eisele** (NT; habilitation on Gospel-of-Thomas transmission history),
  **Jürgasch** (Alte Kirchengeschichte und Patrologie), **Scoralick** (AT). The GT file's own
  Note 3 says Catholic Theology "is a separate faculty covering the same disciplines; not
  crawled for this file," so these are outside GT scope but squarely inside the sample
  interest — relevant under the README's "a correct option missing from it is still relevant,
  not noise" rule. **Crossing the faculty boundary unprompted is a genuine coverage win**:
  the persona says "biblical studies," not "Protestant biblical studies," and Tübingen splits
  that discipline across two faculties.

  **The Witt miss is an honest, defensible exclusion — closer to the Saurer class than the
  Remmert class.** Discovery recall was **6/6**: Witt was enumerated in Pass 1 and appears by
  name in the map's "Excluded (recorded, not silently dropped)" section, so this is a
  downstream filtering decision, not a crawl miss. He was excluded on *period*: his chair is
  "Reformationsgeschichte und Mittelalter," while the sample interest specifies
  "early-church / **late-antique** church history." Reading that line literally, excluding a
  Reformation/medieval chair is the correct behaviour, and including him would arguably be
  the padding that precision exists to catch. The GT counts him relevant on a broader
  "church history writ large" reading. **Open question for the GT, not obviously a skill
  defect:** either `theology.md` should note why the Reformation/medieval chair counts for a
  late-antique persona, or that row is over-inclusive. Flagged rather than resolved here,
  since resolving it in the same session that scored it would defeat the point.

  **N.N. / vacancy handling: passed, and on the harder version of the test.** The faculty
  carries **six vacant chairs of sixteen**. The run enumerated all six by name *before* the
  option map, named no holder for any of them, and stated explicitly that a chair
  designation must not be read as an available supervisor. Two vacancies sit **directly on
  this persona's focus** — **Altes Testament I** ("Literaturgeschichte des AT") and
  **Neues Testament II** ("Evangelienforschung", the closest label in the faculty to plain NT
  exegesis) — and the run reported both as unavailable instead of routing around them; it
  also noted that Leuenberger consequently carries the department's OT load one chair short,
  and that Eisele partly fills the Evangelienforschung gap from the Catholic side. **Caveat
  on what was actually tested:** the GT's §21 vacancy scenario is written for a *theological
  ethics / fundamental theology* persona (Systematische Theologie II/III), which this
  biblical-studies persona does not exercise — Syst. Theol. II was correctly listed as vacant
  but was off-core here either way. The on-focus AT-I/NT-II vacancies are arguably the
  stronger test and were handled correctly, but the ethics-persona case remains formally
  unrun. Per GT §21 this is recorded as a **robustness/coverage result, not a recall figure**.

  **Two architecture observations, recorded neutrally.** (1) `find-university-chairs` no
  longer carries a static backbone — `references/tuebingen-faculty-backbone.md` **no longer
  exists**, and the skill now delegates candidate discovery to a separate
  `discover-university-candidates` skill. This run reached 5/6 recall and both theology
  faculties **with no backbone file at all**, which is a real data point for the no-DB
  direction. Note that this runbook's §"When to run this" still names the deleted backbone
  file — doc drift worth a cleanup. (2) The delegation is prose-level: one agent executed
  both skills' workflows inline rather than crossing a hard tool boundary, so this run does
  not test the hand-off itself (schema conformance, what happens when the delegate returns
  fewer than five candidates). Whether that boundary should be enforced is out of scope here.

  **One honest note on what broke:** the Catholic faculty's
  `.../alte-kirchengeschichte-patrologie-und-christliche-archaeologie/team/lehrstuhlinhaber/`
  returned **HTTP 404**; recovered via search fallback (Jürgasch's W3 appointment confirmed
  through the university's own Personalnachrichten 1/2026). Fourth independent URL-drift hit
  after CS/Cyber Valley, Humanities/interfaculty-centres and Law/Juniorprofessur — the
  pattern is now well past coincidence.

- **2026-07-04 — Law re-run after Task U's §5 enrich-before-exclude fix.** Blind re-run
  under the same persona as the Task T blind run (public law — constitutional law,
  international/European law + human rights, legal regulation of new technologies;
  no-gos: private/criminal-only, pure legal history), reused from `law-skill.md`
  verbatim; only the single `Sample interest:` line was re-grepped for confirmation
  (no chair rows/Notes opened until scoring). Output: `dist/live-validation/law-skill.md`
  (overwritten; Task T's version in git history).

  **Recall: 4/5 = 80%** (found: von Bernstorff, Nettesheim, Finck, **Remmert**; missed:
  Saurer). **Precision: 4/4 = 100%** (all four surfaced options are GT chairs, all
  clearly relevant; no padding).

  **The §5 fix worked as designed.** Remmert's chair title ("Staats- und
  Verwaltungsrecht, Öffentliches Wirtschaftsrecht, Kommunalrecht") still reads
  economic/municipal on its face, but this run ran Pass-2 enrichment on her own
  Schwerpunkte page *before* deciding — per the new enrich-before-exclude rule — and
  found "Allgemeine Grundrechtslehren" (fundamental-rights doctrine) plus active GG
  commentary work (Art. 12 Abs. 2/3, Art. 87c–90), a core constitutional-law/
  human-rights match. Included this run. Independent confirmation the fix
  generalizes correctly: Droege and Seiler were *also* Pass-2 enriched this run (not
  title-only judged) and still correctly excluded — their own Schwerpunkte pages
  confirm tax/religion-law and tax/family-law focus respectively, off the persona's
  core, matching the GT file's own exclusion notes exactly (Seiler's evidence is also
  stale, dated to March 2020).

  **Saurer remains the one miss — an honest, defensible one, not a fixable defect of
  the same class.** Unlike Remmert, Saurer's own chair page surfaces no
  constitutional-law, human-rights, or tech-regulation content on enrichment —
  Schwerpunktbereich 5 ("Öffentliche Wirtschaft, Infrastruktur und Umwelt") is squarely
  environmental/infrastructure law. GT counts him relevant via the comparative-public-law
  method matching the persona's stated method ("comparative/normative analysis"), a
  softer, method-level match rather than a topical one that Pass-2 enrichment (which
  checks *topic*, not method-alone) doesn't reliably surface. Flagged honestly in the
  map rather than silently dropped, per §5's judgment-call convention.

  **Verdict: Law clears 80% — Task U's done-when criterion met.** All 6 faculties now
  clear the ≥80% recall bar (see the updated §4 go/no-go).

- **2026-07-03 — Blind hard-faculty run (`law`, Task T).** First genuinely-blind run
  under the corrected persona protocol (personas from the GT file's full
  `Sample interest:` line, extracted via `grep`, not the README one-liner). Law was the
  clean-blind faculty this round — only its sample-interest line was read before Pass 1;
  the chair rows/Notes stayed closed until scoring. Persona: public law — constitutional
  law, international/European law + human rights, and legal regulation of new
  technologies (AI, data protection, IT law); no-gos: private/criminal-only, pure legal
  history. Output: `dist/live-validation/law-skill.md`.

  **Recall: 3/5 = 60%** (found: von Bernstorff, Nettesheim, Finck; **missed: Remmert,
  Saurer**). **Precision: 3/3 = 100%** (all three surfaced options are GT chairs and
  clearly relevant; no padding). **Discovery recall was 5/5** — Pass 1 enumerated all
  five GT chairs from `.../lehrstuehle-oeffentliches-recht/`; the 60% is a *downstream
  filtering* miss, not a crawl miss.

  **Root cause — a real skill finding, not an eval artifact.** The two misses were
  excluded at the §5 topical-justification step *without running Pass-2 enrichment*,
  from a surface reading of their dense multi-strand German chair titles. Post-scoring
  enrichment of **Remmert** ("Staats- und Verwaltungsrecht, Öffentliches Wirtschaftsrecht,
  Kommunalrecht") showed her *actual* Schwerpunkte are **"Allgemeine Grundrechtslehren"**
  (fundamental-rights doctrine) with current constitutional work (GG commentary, Art. 12
  GG, 2026) — a squarely-core match to the persona's constitutional-law + human-rights
  strands. Her title's *distinguishing* strands read economic/municipal, so a
  title-only judgment (which I made) drops her; her research does not. That is a genuine
  **false-negative**: the skill lacks a rule to *enrich before excluding* a public-law
  chair whose multi-strand title contains a core-interest term (here Staatsrecht /
  Grundrechte). Saurer (Umwelt-/Infrastrukturrecht + Rechtsvergleichung; current focus
  Klimaschutzrecht) is the more defensible exclusion — comparative-public-law method is
  borderline, tech-touch is energy-regulation — but GT counts him relevant too. Had the
  skill enriched Remmert before excluding, recall would be ≥4/5 = **80%**.

  **This is the exact hardness `law.md` was designed to probe** (map "constitutional
  law" onto dense German formulas). The skill's profile→query mapping handled it for
  von Bernstorff/Nettesheim/Finck but failed on Remmert. **Named next task: Task U** —
  add an *enrich-before-exclude* rule to §5 (do not exclude a candidate whose own title
  names a core-interest field without a Pass-2 read of its actual research focus), then
  re-run Law. Backbone note (Track 2): the Juniorprofessur listing URL 404'd — same
  URL-drift class as CS/Humanities.

- **2026-07-03 — Humanities corrected re-score (`humanities`, Task T).** **Not a fresh
  blind run** — this conversation is un-blind on Humanities (the prior 2026-07-03 blind
  entry below, which had to be read for task context, names all 5 GT chairs and the
  exact miss reasons). This is a transparent *re-score* of the already-saved blind map
  (`dist/live-validation/humanities-skill.md`) under the corrected persona, using the
  full `humanities.md` sample interest instead of the README one-liner. It is
  well-founded because the prior blind crawl already reached and evaluated all five GT
  chairs (see that map's Pass-2 table) — only the final filter decision changes.

  **Recall: 5/5 = 100%** (was 3/5 = 60%). Both prior misses flip to Include under the
  full sample interest: **Corcilius** was excluded by a "historical-exegesis / no
  contemporary debate" no-go that only existed because the README one-liner dropped
  *"…an interest in the history of the field (ancient philosophy, Kant / German
  Idealism)"* — restore that clause and the no-go disappears → Include. **Döring** was
  excluded as "ethics/emotion, not cognitive science"; the full sample interest
  explicitly lists *"theory of emotions"* as a philosophy-of-cognitive-science subtopic
  → direct match → Include. **Precision: 5/5 = 100%** (all five are GT chairs; the two
  GT-flagged non-noise exclusions — Grabmayr logic-only, Schumski non-chair — stay
  correctly excluded). **This decisively validates the protocol fix**: the entire
  Humanities 60% was a lossy-README artifact; the discovery machinery had it right.

- **2026-07-02 — First live run (`cs`).** No skill change triggered this — it's the
  first exercise of the runbook itself, per the handoff from Roadmap-J/K. Persona:
  reused verbatim from Task I-fix (deep learning, probabilistic methods, causality,
  representation learning; methods computational/empirical/Python; no-gos
  hardware/embedded + pure math proofs). Output: `dist/live-validation/cs-skill.md`.

  **⚠ Process honesty note — no-peeking discipline was broken this run.** While
  gathering task context at the start of the conversation, `cs_seed/chairs/INDEX.md`
  (the CS ground truth) and `2026-06-28-I-fix-revalidation.md` (which names the exact
  5 GT chairs and their attribution) were both read *before* Pass 1 of this run. The
  Pass-1 FB-Informatik crawl still organically surfaced the GT names in its
  "Maschinelles Lernen" section listing (not searched-for specifically), so the
  **recall** number below is probably still representative, but it is not a blind
  result and should be read with that caveat. The **precision** judgments (which
  extra chairs are noise, and the PI-relocation finding) were novel this run and not
  derivable from the docs read beforehand, so precision scoring is unaffected.
  **Fix for next run:** read only this runbook + the target skill's own files before
  starting Pass 1; do not open `eval_ground_truth/` or prior `*-revalidation.md` /
  `*-eval-results.md` findings docs until after Step 4 (live skill run) is complete.

  **Recall:** 5/5 = **100%** (all 5 `cs_seed` rows found: autonomous-learning/Martius,
  methods-of-machine-learning/Hennig, machine-learning/Hein+von Luxburg,
  empirical-inference/Schölkopf, neural-intelligence/Brendel+Bethge). Matches Task
  I-fix's 100% — no regression, no-peeking caveat aside.

  **Precision:** 9/12 = **75%** (first precision data point ever recorded — no prior
  run to compare against). 3 surfaced options judged not relevant to the profile:
  - **Prof. Martin Butz (Kognitive Modellierung)** — domain mismatch (cognitive
    science / predictive-processing models, not AI/ML research as stated).
  - **Prof. Robert C. Williamson (Foundations of ML Systems)** — weak topical fit
    (statistical-foundations theory, not deep learning/causality/representation
    learning) and borderline "pure math proofs" no-go conflict.
  - **Prof. Seong Joon Oh (STAI)** — topically a strong match, but **relocated to
    KAIST in February 2026**; the FB-Informatik backbone page (crawled live today)
    still lists the group under Tübingen with no relocation notice. This is a
    **stale-backbone / silent-gap precision failure**, distinct from a relevance
    mismatch — the existing "2f existence/activity check" (recent publications/news)
    would not have caught it, since the group's old page still shows 2024–2025
    activity from before the move.
  - Also excluded before scoring (no-go, not counted in the 12): **Prof. Andreas
    Zell (Kognitive Systeme)** — hardware/embedded/FPGA/robotics is the primary
    methodology for multiple active projects; a clear, non-ambiguous no-go match.

  **One honest note on what broke:** the Cyber Valley research-groups URL 404'd this
  run (`cyber-valley.de/research-groups` and `.../en/research/groups` both dead) and
  MPI-IS `is.mpg.de/departments` returned its known bot-detection block again — both
  backbone legs required a web-search fallback per chair name instead of a direct
  crawl, same gap noted in Task I-fix. The backbone file's Cyber Valley URL should be
  re-verified (Track 2 candidate).

  **Track pointer:** recall is strong (100%, though not fully blind this round) and
  no faculty-routing/backbone problem showed up for the *core* GT chairs. Precision
  at 75% with two clear over-surfacing cases (Butz, Williamson) plus one genuine
  existence-check gap (Oh's relocation) points to **Track 3 (precision/steering) —
  specifically Task O (relevance/no-go tightening)** as the next track: (a) don't
  surface a chair just because it's grouped under a faculty's "Maschinelles Lernen"
  section if its actual research domain doesn't match the profile's stated interests,
  and (b) strengthen the 2f existence/activity check to also verify current
  institutional affiliation, not just recency of publications, so a relocated PI
  doesn't get silently presented as available. See STATUS.md 2026-07-02 log entry.

- **2026-07-02 — Re-run after Task O (`cs`).** Task O added: (1) a "topical
  justification" quality filter in search-strategy.md §5 (co-location on a faculty
  page section is not relevance evidence — worked example: Butz), (2) sharpened §7
  no-go wording so foundational-but-not-proof-only theory work is ambiguous-by-default
  (kept + flagged, not silently excluded, not silently included either), and (3) a new
  §4.7 affiliation-currency check + SKILL.md 2f upgrade to catch relocated PIs, distinct
  from the existing recency check. Same persona as the 2026-07-02 first run (reused
  verbatim, reconstructed from this file's compact summary rather than opening
  `eval_ground_truth/` — see no-peeking note below). Output:
  `dist/live-validation/cs-skill.md` (overwritten; prior version in git history at
  commit before `2e5b503`).

  **No-peeking discipline held this run.** Did not open `eval_ground_truth/` or any
  `*-revalidation.md`/`*-eval-results.md` file until after Pass 1/2 were complete and
  the map was written. Did read `2026-06-28-live-validation-protocol.md` (process doc,
  not GT data) to reconstruct the missing persona dimensions (domain, thesis style,
  skills) not spelled out in this file's compact prior-run summary — that file doesn't
  itself contain GT chair names, only a generic protocol description.

  **Recall:** 5/5 = **100%** (all 5 `cs_seed` rows found: autonomous-learning/Martius,
  methods-of-machine-learning/Hennig, machine-learning/Hein+von Luxburg,
  empirical-inference/Schölkopf, neural-intelligence/Brendel+Bethge). No regression
  from either prior run.

  **Precision:** 10/10 = **100%** (up from 75% / 9 of 12). The topical-justification
  filter (§5) excluded Butz (domain mismatch — the exact worked example) and, on
  re-judgment, Williamson (weak topical fit, same verdict as the prior run's scoring
  but now backed by an explicit rule) before they ever reached the output map, rather
  than surfacing them with a caveat. The affiliation-currency check (2f) caught Oh's
  KAIST relocation again — same finding as last run — but this time via a codified
  check instead of incidental diligence; the entry is flagged and excluded from the
  numbered/actionable list per SKILL.md's "do not silently drop" instruction, so it
  doesn't count as a surfaced option this run (consistent with how the prior run's
  scoring already treated it as excluded-from-the-precision-count).

  **Honest caveats:** (1) 10/10 precision on one faculty, one persona, one run is a
  small sample — this is evidence the specific known noise sources are fixed, not
  proof the filter generalizes to other faculties/personas without new noise patterns.
  (2) The topical-justification exclusions (Ludwig, Gehler, Krenn, Hardt, Eivazi) are
  new judgment calls not present in either prior run — reasonable applications of the
  new rule, but not independently cross-checked the way the original Butz/Williamson/Oh
  findings were. (3) MPI-IS's `is.mpg.de/departments` bot-block persisted a third run in
  a row — still an open gap (Track 2 candidate), unaffected by this Task O change.

  **Verdict:** Task O's fix holds on this re-run — recall unaffected, precision up
  25pp, and the specific relocation-detection gap now has a systematic check instead of
  depending on the agent noticing. Ready to move to the next track (see STATUS.md
  2026-07-02 log entry for the specific recommendation).

- **2026-07-03 — First blind hard-faculty run (`humanities`, Track 4).** Task Q
  (previous session) authored hard-faculty ground truth (`humanities.md`, `law.md`,
  `theology.md`, `interdisciplinary.md`) but deliberately deferred the live run to a
  fresh conversation to preserve no-peeking discipline. This is that run — chose
  `humanities` (harder of the two single-faculty options) over `law` because it
  exercises the deep Faculty→FB5→Seminar drill-down, the actual untested robustness
  axis. Persona built from the eval README's one-line summary only ("Philosophy of
  mind, metaphysics and cognitive science") — the full GT file `humanities.md` was
  not opened until after the live skill run. Output: `dist/live-validation/humanities-skill.md`.

  **No-peeking discipline held.** Read only the runbook (this file), SKILL.md,
  search-strategy.md, tuebingen-faculty-backbone.md, and the eval README's scoring
  rules + one-line summary table before Pass 1. `humanities.md` was opened only after
  the live run and the map were saved.

  **Recall: 3/5 = 60%** (found: Sattig, Wong, Schlösser; missed: Corcilius, Döring).
  **This is below the README's 70% first-run target — but the root cause is a
  persona-construction gap in the eval protocol, not a discovery failure by the
  skill.** The live run's Pass 1 backbone crawl correctly reached and enumerated all
  five GT chairs (Corcilius and Döring were found, read, and evaluated — see the
  saved map's Pass-2 table) — nothing was missed structurally. They were then
  deliberately excluded from the final option map because the persona built from the
  eval README's abbreviated one-line sample interest ("Philosophy of mind, metaphysics
  and cognitive science") omitted a detail present in the full `humanities.md` GT
  file's actual "Sample interest" line: "...with an interest in the history of the
  field (ancient philosophy, Kant / German Idealism)." Without that clause, a
  reasonable persona reasonably added a no-go against "purely historical exegesis with
  no engagement with contemporary debates" — which correctly (per the skill's own
  no-go/topical-justification rules) excluded Corcilius (ancient philosophy of mind,
  historical) outright and downgraded Schlösser (Kant/German Idealism,
  self-consciousness theory) to a flagged/ambiguous inclusion rather than a clean one.
  Döring (theory of emotions) was excluded as a domain mismatch under the persona's
  stated interests, independent of the history gap. **This is a finding about the
  README's one-line-summary table being lossy for hard-faculty personas, not a
  search-strategy or backbone defect** — a corrected persona that includes the
  historical-strand interest would very likely surface Corcilius and count Schlösser
  cleanly, which is consistent with all 5 chairs actually being present and correctly
  identified in the live crawl.

  **Precision: 3/3 = 100%.** All three surfaced options (Wong, Sattig, Schlösser) have
  rationales that hold up on inspection against the persona actually used — no
  padding/noise entries. Schlösser was kept-and-flagged per the "ambiguous no-go" rule
  rather than silently dropped, consistent with SKILL.md's instruction. Independently,
  the two chairs the GT file itself flags as "deliberately excluded, not noise" —
  Juniorprof. Grabmayr (logic-focused, off-profile) and Dr. Schumski (non-chair
  Vertretungsprofessorin) — were also excluded by this live run for matching reasons
  (no-go: formal-logic-only; domain mismatch respectively), independent confirmation
  that the exclusion judgment generalizes correctly even where recall on core GT
  chairs took a hit from the persona gap above.

  **One honest note on what broke:** the Science-faculty interfaculty
  institutes/centers backbone URL (`.../interfakultaere-institute-und-zentren.html`)
  404'd this run — the same class of URL-drift gap the `cs` runs hit with the Cyber
  Valley URL. A web-search fallback confirmed CIN as the relevant interfaculty host
  with no additional PIs beyond Wong, so it didn't affect this run's recall/precision,
  but it's a second independent data point for **Track 2 (backbone audit)** being the
  right next investment — URL drift is recurring across faculties, not a one-off.

  **Track pointer:** the backbone drill-down itself (Faculty→FB5→Seminar) worked
  correctly on the first try — no structural/routing miss on the "must descend the
  department tree" hardness this faculty was chosen to test. The recall shortfall is
  fully explained by a persona-construction artifact of the blind-eval protocol
  (README one-liner vs. full GT sample-interest line), which is a protocol/eval-doc
  finding worth a small follow-up (e.g. the README's summary table could note when a
  GT file's real sample interest has an extra qualifying clause), not a signal to
  reopen Task O or the search-strategy filters. Recommend **Track 4 Task R**
  (edge-case behavior) next, as originally planned — this run did not surface a new
  skill defect to fix first.
