# Changelog

All notable changes to the study-os-thesis skill package are documented here.

This project follows Semantic Versioning for the released skill package:

- PATCH: wording fixes, small reference/data corrections
- MINOR: new skills, new references, new optional outputs
- MAJOR: breaking changes to skill names, folder layout, triggers, or expected inputs/outputs

## [Unreleased]

### Added

- `thesis-finder` rebuilt as a single, database-less, university-wide entry-point skill covering all faculties, with inline student-profile building (no separate pre-skill call needed).
- `find-company-thesis-options` — company/R&D thesis discovery across the Baden-Württemberg company backbone.
- `draft-thesis-contact` — first-contact message drafting to potential advisors, with a paper-first gate.
- Persistent session state across searches, a no-invented-URLs rule, and mandatory existence/activity verification for discovered chairs and companies.

### Changed

- `find-university-chairs` rewritten as a faculty-agnostic discovery skill, extended from a fixed subset to all Tübingen faculties.

### Fixed

- ...

### Removed

- ...

### Breaking Changes

- `thesis-finder` is now the sole entry point; the previous flow requiring a separate profile-building skill call before search is no longer required and may not match older invocations.
