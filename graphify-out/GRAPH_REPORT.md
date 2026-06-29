# Graph Report - study-os-thesis  (2026-06-28)

## Corpus Check
- 116 files · ~125,039 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 930 nodes · 1102 edges · 96 communities (77 shown, 19 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ce65536f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]

## God Nodes (most connected - your core abstractions)
1. `No-DB Universal Skill — Exact Build Plan` - 13 edges
2. `main_with_args()` - 12 edges
3. `BW Company Backbone` - 12 edges
4. `build_release()` - 11 edges
5. `Skill Responsibilities` - 11 edges
6. `Kritische Sachen` - 11 edges
7. `Zusammenfassung: StudyOS Thesis Advisor als Claude Skill` - 11 edges
8. `Phase 2 — Company Discovery: Build Plan` - 11 edges
9. `read_text()` - 10 edges
10. `_run_single_faculty_comparison()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `test_minor_and_major_bumps_reset_lower_segments()` --calls--> `bump_version()`  [EXTRACTED]
  skills/tests/test_version_bump.py → scripts/bump_project_version.py
- `test_patch_bump_replaces_entire_semver()` --calls--> `bump_version()`  [EXTRACTED]
  skills/tests/test_version_bump.py → scripts/bump_project_version.py
- `test_rejects_non_semver_project_version()` --calls--> `bump_version()`  [EXTRACTED]
  skills/tests/test_version_bump.py → scripts/bump_project_version.py
- `test_finalize_changelog_creates_version_section_and_resets_unreleased()` --calls--> `finalize_changelog_text()`  [EXTRACTED]
  skills/tests/test_release_changelog.py → scripts/release_changelog.py
- `test_finalize_changelog_rejects_empty_unreleased_section()` --calls--> `finalize_changelog_text()`  [EXTRACTED]
  skills/tests/test_release_changelog.py → scripts/release_changelog.py

## Import Cycles
- None detected.

## Communities (96 total, 19 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (48): Namespace, assistant_prompt(), CodexDeepEvalLLM, deepeval_model(), deepeval_test_case_kwargs(), evaluate_with_deepeval(), load_fixture_run(), load_persona() (+40 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (39): Discover Thesis Options, Evidence Rules, Output, Prerequisites, Step 1 — Verify the profile, Step 2 — Extract query variables, Step 3 — Route to relevant faculties, Step 4 — Pass 1: backbone crawl (+31 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (34): Match, build_release(), BuildError, copy_skill(), create_archives(), main(), Path, Build the public release artifact for the thesis-advising skills. (+26 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (30): Disambiguation Rules, Discover Company Thesis Options, Evidence Rules, Map-level coverage caveat (required — append once, at the top of the map), No-Go Guard (hard stops), Output, Per-entry fields, Prerequisites (+22 more)

### Community 4 - "Community 4"
Cohesion: 0.21
Nodes (25): abstract_from_inverted_index(), dedupe_papers(), fetch_papers(), format_paper_block(), load_fixture_papers(), main(), main_with_args(), markdown_cell() (+17 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (25): 1. Profile dimensions → query variables, 2.1 Interest-to-tag mapping, 2.2 Filtering logic, 2. Profile → backbone filter, 3. Two-pass strategy, 4.1 R&D focus queries, 4.2 Thesis signal queries, 4.3 Contact / team queries (+17 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (18): `build-student-profile`, Contribution And PR Guidance, Core Rule: Use The Meta-Skill First, `design-agent-skill`, `draft-thesis-contact`, Evidence, Privacy, And Data Rules, `find-company-thesis-options`, `find-recent-papers` (+10 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (17): Added, Breaking Changes, Changed, Changelog, Fixed, Removed, [Unreleased], Architecture (+9 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (16): 1. Per-profile recall table, 2. Thesis-signal accuracy (skill arm only), 3. Honest failures: what was missed and why, 4. Comparison to Phase 1, 5. Honesty note: circular recall caveat, 6. Phase-2 gate verdict, 7. What the skill does NOT do (confirmed by this eval), C1 — Nothing missed by skill; sereact missed by baseline (+8 more)

### Community 9 - "Community 9"
Cohesion: 0.21
Nodes (12): Path, _load_runner(), Deterministic checks for Codex-native multi-turn eval scaffolding., test_coverage_scoring_detects_chair_names(), test_deepeval_kwargs_are_conversation_level(), test_discovery_comparison_writes_artifact(), test_fixture_export_writes_markdown_and_json(), test_fixture_user_runner_preserves_scripted_turns() (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (15): 10. GPA-Berechnung gibt jedes Mal etwas anderes aus, 1. Skepsis gegenüber dem Themen-Scraper der Profs, 2. Stattdessen Paper / Forschungsbeschreibungen extrahieren — exakte Lehrstuhlprofile, 3. Empfehlungen und Chat darauf stützen, 4. Empfehlungen gut balancieren, damit nicht einzelne PhDs/Profs überlaufen, 5. Erwartungshaltung der Profs & benötigte Voraussetzungen bereitstellen, 6. Wie man (im besten Fall) mit dem Prof in Kontakt tritt & wie der Thesis-Ablauf ist, 7. LaTeX-Vorlage verlinken (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.14
Nodes (13): 1. Think Before Coding, 2. Simplicity First, 3. Surgical Changes, 4. Goal-Driven Execution, 5. Issues & Pull Requests, 6. Workflow: Masterplan & Status, 7. Commits & Conversation Handoff, Branches & commits (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (14): 1.1 Methodologische Anmerkung, 1.2 Typ A — Kapazitätsbedingte Ablehnung (Butz, Menth, Mähl), 1.3 Typ B — Bereit, wenn trivial (Hennig, Zell, Kerstin, Georg, Huson, Wichmann, Bob/Rabanus, Anna), 1.4 Typ C — Prinzipielle Ablehnung (Macke, Luxburg, Berens, Winther, Stephan, Niels, Bob teils), 1.5 Typ D — Nischenpipelines (Peter, Mario, Häufle teils), 1.6 Übergreifende Spannungen, 1. Detailanalyse Professoren-Feedback, 2. Zeitplan-Realitätscheck (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (14): 10. Empfehlung & offene Entscheidung, 1. Ausgangslage — was im Meeting vorgeschlagen wurde, 2. Wie ein Skill funktioniert (Kurzüberblick), 3. Die „Datenbank" als gebündelte Dateien, 4. Empfohlene Skill-Struktur, 5. Monatliche Aktualisierung der Daten, 6. Verteilung an den Fachbereich — der eigentliche Knackpunkt, 7. Andere LLM-Plattformen (OpenAI, Gemini, DeepSeek) (+6 more)

### Community 14 - "Community 14"
Cohesion: 0.14
Nodes (13): Comparison: Task I vs. Task I-fix, CS re-validation, Honest caveats, Pass 1 backbone crawl result, Pass 1 backbone crawl result — three legs, Pass 2 enrichment highlights, Pass 2 enrichment highlights, Phase-1 gate verdict (+5 more)

### Community 15 - "Community 15"
Cohesion: 0.14
Nodes (14): 1.1 Methodology note, 1.2 Type A — capacity-driven refusal (Butz, Menth, Mähl), 1.3 Type B — willing if trivial (Hennig, Zell, Kerstin, Georg, Huson, Wichmann, Bob/Rabanus, Anna), 1.4 Type C — principled refusal (Macke, Luxburg, Berens, Winther, Stephan, Niels, Bob in part), 1.5 Type D — niche pipelines (Peter, Mario, Häufle in part), 1.6 Cross-cutting tensions, 1. Professor Feedback Deep Dive, 2. Timeline Reality Check (+6 more)

### Community 16 - "Community 16"
Cohesion: 0.23
Nodes (12): RuntimeError, bump_pyproject(), bump_version(), main(), Path, Bump the project SemVer in pyproject.toml., Raised when the project version cannot be bumped., VersionBumpError (+4 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (13): Housekeeping (not an agent task), No-DB Universal Skill — Exact Build Plan, Phase 2 (later) — Company discovery, Skill inventory: keep / rework / retire, Target skill flow (after this plan), Task A — Conversation discipline in `build-student-profile`, Task B — Faculty backbone reference (anti-SEO-bias baseline), Task C — Search-strategy reference (the core IP) (+5 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (13): Decision 1 — Orchestration: thin entry-point skill, not a wrapper pipeline, Decision 2 — Backbone fixes before distribution, Decision 3 — Distribution channels, Decision 4 — Eval strategy for Phase 3, Key decisions, Phase 3 gate criteria, Phase 3 — Orchestration & Distribution: Build Plan, Scope boundary (+5 more)

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (12): 1. Executive Summary: What We Learned from 27 Professors, 2. Chair Typology, 3. Key Insights, 4. What Professors Would Actually Use, 5. Tension Matrix, 6. Product Pivot Recommendation, Distribution (approximate), Market Analysis: Professor Feedback Synthesis (+4 more)

### Community 20 - "Community 20"
Cohesion: 0.22
Nodes (7): Path, _parse_frontmatter(), Deterministic checks for the portable thesis-finder skill package., _skill_dirs(), test_expected_portable_skills_exist(), test_referenced_skill_resources_exist(), test_skill_frontmatter_is_portable_and_trigger_rich()

### Community 21 - "Community 21"
Cohesion: 0.15
Nodes (13): Das Problem, Die neue Richtung, Die Suchanfragen — Herzstück des Skills, Externe Unternehmen, Kernfrage: Was macht diesen Skill besser als "Claude einfach fragen"?, Offene Fragen (für /grillme), Phasenplan (Vorschlag, noch zu diskutieren), Qualitäts-Filter (+5 more)

### Community 23 - "Community 23"
Cohesion: 0.17
Nodes (12): 1. Zusammenfassung: Was wir von 27 Professoren gelernt haben, 2. Lehrstuhl-Typologie, 3. Zentrale Erkenntnisse, 4. Was Professoren tatsächlich nutzen würden, 5. Spannungsmatrix, 6. Produktschwenk-Empfehlung, Marktanalyse: Synthese des Professoren-Feedbacks, Typ A — „Nein danke" (klar, kapazitätsbedingte Ablehnung) (+4 more)

### Community 24 - "Community 24"
Cohesion: 0.17
Nodes (12): 1. Web-search coverage is structurally incomplete, 2. "Better than just asking Claude" must be earned, 3. Company discovery is a different, harder problem, 4. How do we measure "works"?, 5. The honest value is the process, not a perfect output, Context, Decisions Summary, Key Open Items / Follow-up (+4 more)

### Community 25 - "Community 25"
Cohesion: 0.18
Nodes (10): API-Key, Backend, Erweitern auf andere Fachbereiche, Erweitern auf Companies:, Framing vom Tool, Key Challenges, Wie halten wir das up-to-date, sodass es wirklich funtktioniert?, Wie tragen wir die Infos von Konversation zu Konversation weiter, wenn man den Skill in einer Konversation genutzt hat, dass man "nahtlos" weiterarbeiten kann, wenn das Thema sich über mehrere Wochen zieht? (+2 more)

### Community 26 - "Community 26"
Cohesion: 0.18
Nodes (11): 1. Architektur-Bewertung, 2. Feature-Checkliste vs. MVP-Ziel, 3. Priorisierung offener PRs, 4. Priorisierung offener Issues nach Timeline, 5. Kritischer Pfad bis 01.07., 6. Risiko-Bewertung, Technischer Status & Roadmap, Wochen 15–21 (RAG-Phase) (+3 more)

### Community 27 - "Community 27"
Cohesion: 0.18
Nodes (10): 1. Medicine: one chair missed — Prof. Dr. Ghazaleh Tabatabai, 2. Fixture mode inflates the skill-vs-baseline gap, 3. CS/ML: researcher-level rather than chair-level scoring, 4. High-relevance ratio is moderate for non-CS faculties, Artifacts, Eval Results — Discovery Skill vs. Baseline (Task H), Overall Conclusion, Per-Faculty Results (+2 more)

### Community 28 - "Community 28"
Cohesion: 0.18
Nodes (11): 1. What we have today, 2. What "optimal core" actually means — the quality levers, 3. The plan — prioritized tracks, 4. Definition of "core is done", 5. Critical path / dependencies, Track 1 — Close the validation loop (highest priority), Track 2 — Optimize recall (after Task I shows the real number), Track 3 — Optimize precision & steering (+3 more)

### Community 29 - "Community 29"
Cohesion: 0.18
Nodes (11): Dependency graph, Phase 2 — Company Discovery: Build Plan, Phase-2 gate criteria (equivalent to Phase 1 gate), Skill to create, Target skill flow (Phase 2 addition), Task 2-A — BW Company Backbone Reference, Task 2-B — Company Search Strategy, Task 2-C — Build `find-company-thesis-options` Skill (+3 more)

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (11): Comparison with university output schema, Coverage caveat (stronger than university version), Decision, Decision 1 — Company Backbone Source, Decision 2 — Output Schema for Company Options Map, Explicit No-Gos for Phase 2, Options evaluated, Phase 2 — Company Discovery: Decisions (+3 more)

### Community 31 - "Community 31"
Cohesion: 0.18
Nodes (11): 1. Architecture Assessment, 2. Feature Checklist vs MVP Goal, 3. Open PR Prioritization, 4. Open Issue Prioritization vs Timeline, 5. Critical Path to 1.07, 6. Risk Assessment, Technical Status & Roadmap, Weeks 15–21 (RAG phase) (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.20
Nodes (7): Done-when, Goal, Hard validity rules (read before running), Output, Procedure (per faculty: medicine, psychology, wiso, cs), Task I — Live Validation Protocol (real recall, real baseline), Tooling note

### Community 34 - "Community 34"
Cohesion: 0.20
Nodes (9): Backbone spot-check (Task 3-A verification), C1 Profile (input), Company track (find-company-thesis-options), Dead-reference check, Known gaps (honest, not blocking), Phase 3 — End-to-End Smoke Test, Phase 3 gate checklist, Trace: thesis-finder → both tracks (+1 more)

### Community 35 - "Community 35"
Cohesion: 0.20
Nodes (9): Anti-Behavior, Behavior Rules, Deep User Persona, Disclosure Rules, Hidden Profile, ID, Response Style, Success Signal (+1 more)

### Community 36 - "Community 36"
Cohesion: 0.20
Nodes (9): Anti-Behavior, Behavior Rules, Disclosure Rules, Hidden Profile, ID, Neuro Student Persona, Response Style, Success Signal (+1 more)

### Community 37 - "Community 37"
Cohesion: 0.20
Nodes (9): Anti-Behavior, Behavior Rules, Disclosure Rules, Hidden Profile, ID, Response Style, Standard User Persona, Success Signal (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.20
Nodes (9): Anti-Behavior, Behavior Rules, Disclosure Rules, Hidden Profile, ID, Response Style, Success Signal, Terse User Persona (+1 more)

### Community 39 - "Community 39"
Cohesion: 0.22
Nodes (8): Advising Style, Build Student Profile, First Question, Interview Guidance, Optional Evidence Sources, Output, Privacy Rules, Workflow

### Community 40 - "Community 40"
Cohesion: 0.22
Nodes (8): Eval Ground Truth — Company Seed, Files, How to score a skill run, Relationship to Phase 1 eval ground truth, Secondary metric: thesis-signal accuracy, Target, What "recall" means here, What the ground truth is NOT

### Community 41 - "Community 41"
Cohesion: 0.22
Nodes (9): 1. Das Problem, das wir wirklich lösen, 2. Warum der Plattform-Ansatz schwieriger ist als er scheint, 3. Was wir tatsächlich bauen (neu gerahmt), 4. Wie das die Feedback-Punkte beantwortet, 5. Erfolgskennzahlen (nach MVP), Ebene 1 — Für Studierende (das Produkt), Ebene 2 — Für Lehrstühle (optional, später), Ebene 3 — Für den Fachbereich (nur lesend) (+1 more)

### Community 42 - "Community 42"
Cohesion: 0.22
Nodes (9): 1. What we build, 2. Why no database, 3. The core IP — how the skill searches, 4. Ordering principle, 5. Phase 1 — University discovery (current phase), 6. Phase 2 — Company discovery (later), 7. Phase 3 — Distribution & cross-platform, 8. How this plan is used (+1 more)

### Community 43 - "Community 43"
Cohesion: 0.22
Nodes (9): Comparison to the fixture-mode numbers, Did the profile actually steer the search?, Per-faculty results, Primary recall (name-surfaced, correct attribution required), Strict recall (recommended & correctly attributed as a relevant option), Task I — Live Validation Results (real recall, real baseline), Two scoring lenses (why both are reported), Verdict on the revised Phase-1 gate (+1 more)

### Community 44 - "Community 44"
Cohesion: 0.22
Nodes (9): 1. The Problem We're Actually Solving, 2. Why the Platform Approach Is Harder Than It Seems, 3. What We're Actually Building (reframed), 4. How This Answers the Feedback, 5. Success Metrics (post-MVP), Layer 1 — For students (the product), Layer 2 — For chairs (optional, later), Layer 3 — For the department (read-only) (+1 more)

### Community 45 - "Community 45"
Cohesion: 0.64
Nodes (8): _line(), main(), _rect(), render_coverage_chart(), render_recall_chart(), render_scorecard(), _svg(), _text()

### Community 46 - "Community 46"
Cohesion: 0.22
Nodes (9): Archived: former DB data-foundation phase (superseded 2026-06-26), Current phase, Known difficulties / risks, Log, Open decisions, Phase 2 — Company discovery, Phase 3 — Orchestration & Distribution, Status — StudyOS Thesis-Finder (+1 more)

### Community 47 - "Community 47"
Cohesion: 0.25
Nodes (7): CS seed data, Eval Ground Truth, Files, How to score a skill run, Target, What "recall" means here, What the ground truth is NOT

### Community 48 - "Community 48"
Cohesion: 0.29
Nodes (6): Autonomous Learning, Caveats, Metadata, People, Research Areas, Thesis Fit Notes

### Community 49 - "Community 49"
Cohesion: 0.29
Nodes (6): Caveats, Empirical Inference, Metadata, People, Research Areas, Thesis Fit Notes

### Community 50 - "Community 50"
Cohesion: 0.29
Nodes (6): Caveats, Machine Learning, Metadata, People, Research Areas, Thesis Fit Notes

### Community 51 - "Community 51"
Cohesion: 0.29
Nodes (6): Caveats, Metadata, Methods of Machine Learning, People, Research Areas, Thesis Fit Notes

### Community 52 - "Community 52"
Cohesion: 0.29
Nodes (6): Caveats, Metadata, Neural Intelligence, People, Research Areas, Thesis Fit Notes

### Community 53 - "Community 53"
Cohesion: 0.29
Nodes (6): Roadmap, Status, Top 3 Prioritäten, nächste 2 Wochen, Top 3 Risiken, Was uns 27 Professoren sagten, Zusammenfassung für Stakeholder — StudyOS Thesis Advisor

### Community 54 - "Community 54"
Cohesion: 0.29
Nodes (6): Context, Date, Finding, Follow-Up, Implication, Issue Backlog Reset And Skill-Package Goal

### Community 55 - "Community 55"
Cohesion: 0.29
Nodes (6): Executive Summary — StudyOS Thesis Advisor, Roadmap, Status, Top 3 Priorities, Next 2 Weeks, Top 3 Risks, What 27 Professors Told Us

### Community 56 - "Community 56"
Cohesion: 0.29
Nodes (7): 1. Target Architecture, 2. Skill Suite, 3. Data Layout, 4. Monthly OpenAlex Update, 5. Testing And Quality Gates, 6. Recommendation, Skill Architecture Summary - Skill-Only Thesis Finder

### Community 57 - "Community 57"
Cohesion: 0.29
Nodes (6): DeepEval Conversation Rubric, Discovery Rubric (medicine-discovery scenarios), Metrics, Metrics, Scoring Guide, Shared Threshold

### Community 58 - "Community 58"
Cohesion: 0.29
Nodes (6): Assistant Start Prompt, Expected Outcome, ID, Initial User Message, Medicine Discovery — Baseline Arm, Scenario

### Community 59 - "Community 59"
Cohesion: 0.29
Nodes (6): Assistant Start Prompt, Expected Outcome, ID, Initial User Message, Medicine Discovery — Skill Arm, Scenario

### Community 60 - "Community 60"
Cohesion: 0.29
Nodes (6): Assistant Start Prompt, Expected Outcome, ID, Initial User Message, ML Master Thesis Scenario, Scenario

### Community 61 - "Community 61"
Cohesion: 0.33
Nodes (5): Chair And Researcher Profile Schema, Chair Profile, File Naming, Index Entry, Researcher Profile

### Community 62 - "Community 62"
Cohesion: 0.33
Nodes (5): Deep Advising Interview, Minimum Interview Coverage, Multi-Round Pattern, Research Skill Signals, Stop Rules

### Community 63 - "Community 63"
Cohesion: 0.33
Nodes (5): Body, Frontmatter, Required Structure, Skill Authoring Rules, Validation Checklist

### Community 64 - "Community 64"
Cohesion: 0.33
Nodes (6): English documents (primary), German originals (`de/`), One Open Decision, Research Docs — StudyOS Thesis Advisor, The Core Finding: The Skill Approach Works, What's in Here

### Community 65 - "Community 65"
Cohesion: 0.33
Nodes (5): Step 1 — Profile check, Step 2 — Ask which track, Step 3 — Route, Step 4 — Offer next step, Thesis Finder

### Community 66 - "Community 66"
Cohesion: 0.40
Nodes (4): Design Agent Skill, Design Rules, Thesis-Finder Skill Pattern, Workflow

### Community 67 - "Community 67"
Cohesion: 0.40
Nodes (4): Dev Process Findings, Entry Shape, Filename Convention, Privacy

### Community 68 - "Community 68"
Cohesion: 0.40
Nodes (4): Draft Thesis Contact, Output, Rules, Workflow

### Community 69 - "Community 69"
Cohesion: 0.40
Nodes (4): Evidence Rules, Find Recent Papers, Output, Workflow

### Community 70 - "Community 70"
Cohesion: 0.40
Nodes (4): Generate Thesis Directions, Output, Rules, Workflow

### Community 71 - "Community 71"
Cohesion: 0.40
Nodes (5): Documents, No-DB Universal Skill — Findings, Related, The Direction in One Sentence, Why This Direction Exists

### Community 72 - "Community 72"
Cohesion: 0.40
Nodes (4): Distribution, Local Check, Monthly Data Refresh, Skill Distribution And Maintenance

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (3): Optional LLM-as-judge checks for the portable thesis-finder skills.  These tests, _skill_context(), test_skill_fixture_output_matches_skill_rubric()

### Community 74 - "Community 74"
Cohesion: 0.50
Nodes (3): How to use this, Thesis duration, University of Tübingen Degree Programs

### Community 75 - "Community 75"
Cohesion: 0.83
Nodes (3): _load_runner(), main(), run_faculty()

### Community 81 - "Community 81"
Cohesion: 0.67
Nodes (3): Kritische Sachen, Meine Ideen, Sichtbarkeit unseres Tools

## Knowledge Gaps
- **549 isolated node(s):** `study-os-thesis`, `Erweitern auf Companies:`, `Erweitern auf andere Fachbereiche`, `Backend`, `Key Challenges` (+544 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Bewertung deiner Ideen — StudyOS Thesis Advisor` connect `Community 10` to `Community 22`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Why does `Zusammenfassung: StudyOS Thesis Advisor als Claude Skill` connect `Community 13` to `Community 22`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **What connects `study-os-thesis`, `Build the public release artifact for the thesis-advising skills.`, `Raised when the release package cannot be built safely.` to the rest of the system?**
  _569 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.10666666666666667 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.112375533428165 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._