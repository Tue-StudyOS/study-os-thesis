# Changelog

All notable changes to the study-os-thesis skill package are documented here.

This project follows Semantic Versioning for the released skill package:

- PATCH: wording fixes, small reference/data corrections
- MINOR: new skills, new references, new optional outputs
- MAJOR: breaking changes to skill names, folder layout, triggers, or expected inputs/outputs

## [Unreleased]

### No-DB Universal Skill Rewrite (this branch)

- `thesis-finder` rebuilt as a single, database-less, university-wide entry-point skill covering all faculties, with inline student-profile building (no separate pre-skill call needed).
- `find-company-thesis-options` — company/R&D thesis discovery across the Baden-Württemberg company backbone.
- `draft-thesis-contact` — first-contact message drafting to potential advisors, with a paper-first gate.
- `find-university-chairs` rewritten as a faculty-agnostic discovery skill, extended from a fixed subset to all Tübingen faculties.
- Persistent session state across searches, a no-invented-URLs rule, and mandatory existence/activity verification for discovered chairs and companies.
- Breaking: `thesis-finder` is now the sole entry point; the previous flow requiring a separate profile-building skill call before search is no longer required and may not match older invocations.

### Added

- Skill-only release artifacts as `.tar.gz` and `.zip`, containing only installable skill folders.
- Automated release workflow with version bumping, release branch publishing, and GitHub App authentication.
- Human-readable changelog workflow for GitHub Release notes.

### Changed

- Moved maintainer and test configuration into `pyproject.toml`.
- Updated distribution documentation to describe release artifacts and the `release/skills` branch.

### Fixed

- Prevented release artifacts from including tests, scripts, docs, or maintainer files.
- Fixed release version bumping so SemVer values are replaced correctly.

### Removed

- Removed standalone `pytest.ini` in favor of `pyproject.toml`.

### Breaking Changes

- None.
