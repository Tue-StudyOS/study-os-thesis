# Changelog

All notable changes to the study-os-thesis skill package are documented here.

This project follows Semantic Versioning for the released skill package:

- PATCH: wording fixes, small reference/data corrections
- MINOR: new skills, new references, new optional outputs
- MAJOR: breaking changes to skill names, folder layout, triggers, or expected inputs/outputs

## [Unreleased]

### Added

- ...

### Changed

- ...

### Fixed

- ...

### Removed

- ...

### Breaking Changes

- None.

## [2.0.0] - 2026-08-08

### No-DB Universal Skill Rewrite (this branch)

- `thesis-finder` rebuilt as a single, database-less, university-wide entry-point skill covering all faculties, with inline student-profile building (no separate pre-skill call needed).
- `find-company-thesis-options` — company/R&D thesis discovery across live Baden-Württemberg candidate discovery.
- `draft-thesis-contact` — first-contact message drafting to potential advisors, with a paper-first gate.
- `find-university-chairs` rewritten as a faculty-agnostic discovery skill, extended from a fixed subset to all Tübingen faculties.
- Persistent session state across searches, a no-invented-URLs rule, and mandatory existence/activity verification for discovered chairs and companies.
- Breaking: `thesis-finder` is now the sole entry point; the previous flow requiring a separate profile-building skill call before search is no longer required and may not match older invocations.
- Breaking: runtime backbones are now rules-only. Static company and faculty URI lists were removed from the runtime package; `discover-company-candidates` and `discover-university-candidates` build temporary live candidate tables.
- Added `/commands`-based before/after performance comparison for rules-only discovery changes.

### Added

- Skill-only release artifacts as `.tar.gz` and `.zip`, containing only installable skill folders.
- `discover-company-candidates` and `discover-university-candidates` helper skills for live candidate discovery.
- `scripts/compare_command_simulation_performance.py` for comparing `.claude/commands` / `.codex/prompts` simulation ratings before and after architecture changes.
- Automated release workflow with version bumping, release branch publishing, and GitHub App authentication.
- Human-readable changelog workflow for GitHub Release notes.

### Changed

- Moved maintainer and test configuration into `pyproject.toml`.
- Updated distribution documentation to describe release artifacts and the `release/skills` branch.
- `thesis-finder` no longer hardcodes `~/.claude/thesis-finder/session.md`. It prefers that path and falls back to `./thesis-finder-session.md` in the working directory when the home-scoped path is unavailable, naming the path it used in its first reply.
- `build-student-profile/references/tuebingen-degree-programs.md` is now titled and used as what it is — a Computer Science department list, not a university-wide one. Students in other faculties are asked directly and their answer verified live.
- `INSTALL.md` added at the repo root with per-client install steps, honest prerequisites, and a troubleshooting table.

### Fixed

- Prevented release artifacts from including tests, scripts, docs, or maintainer files.
- Fixed release version bumping so SemVer values are replaced correctly.
- Fixed the release workflow's version drift: the version is read from `pyproject.toml` on the dispatched ref instead of being bumped on the release branch, which previously left `main` permanently behind the published tag.

### Removed

- Removed standalone `pytest.ini` in favor of `pyproject.toml`.
- Removed `find-recent-papers/references/papers/` — a pre-pivot static OpenAlex snapshot (59 files) that conflated two different researchers named "Matthias Hein" and was the last static URI catalog in the package. `find-recent-papers` never referenced it; the skill searches live. Its orphaned tooling (`scripts/update_openalex_index.py`) went with it.

### Breaking Changes

- Static runtime company/faculty backbones are no longer part of the discovery contract. Candidate discovery now requires live search/browsing and returns transient verified candidate tables.

### Notes

- The skills are designed to be installed **as a set**. `thesis-finder` routes into the discovery skills by name and they invoke each other, so a partial install leaves those calls unresolved.
- Release `skills-v1.0.0` (2026-07-06) is superseded: it ships the backbone architecture deleted on 2026-07-31.
