# Changelog

All notable changes to the study-os-thesis skill package are documented here.

This project follows Semantic Versioning for the released skill package:

- PATCH: wording fixes, small reference/data corrections
- MINOR: new skills, new references, new optional outputs
- MAJOR: breaking changes to skill names, folder layout, triggers, or expected inputs/outputs

## [Unreleased]

### Added

- New `find-linkedin-company-theses` skill for profile-first parallel thesis discovery across university/chair matching and public LinkedIn-indexed company thesis postings, with hard exclusions, scorecards, evidence tiers, and company-thesis readiness checks.
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
