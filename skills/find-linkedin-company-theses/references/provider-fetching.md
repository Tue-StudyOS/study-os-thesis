# Provider Fetching Guide

Use this guide after the student profile and external-thesis intake are strong
enough. The goal is a small auditable shortlist, not exhaustive scraping.

## Query Matrix

Build searches from:

- confirmed thesis level: Bachelorarbeit, Masterarbeit, or both only if asked
- compatible generic terms: Abschlussarbeit, final thesis, thesis project
- region and radius: city names, nearby hubs, or country-level alternatives
- topic synonyms: methods, domains, tools, and application terms from the profile
- no-go and must-avoid terms: sectors, role types, stacks, or domains to exclude

For Bachelor profiles, search Bachelor-level and compatible Abschlussarbeit
queries only. For Master profiles, search Master-level and compatible
Abschlussarbeit queries only. Provider result counts may indicate where to look
next, but never count as a recommendation.

## Providers

### `linkedin_public`

Use public web search, not a LinkedIn login:

- `site:linkedin.com/jobs Bachelorarbeit <topic> <city>`
- `site:linkedin.com/jobs Masterarbeit <topic> <city>`
- `site:linkedin.com/jobs Abschlussarbeit <topic> <company-or-city>`
- `site:linkedin.com/jobs thesis <topic> company <city-or-country>`

LinkedIn snippets are often incomplete. Treat them as evidence tier `B` at best
unless an opened public page confirms the details.

### `stepstone`

Use public web search or public StepStone listing pages:

- `site:stepstone.de/jobs Bachelorarbeit <topic> <city>`
- `site:stepstone.de/jobs Masterarbeit <topic> <city>`
- `site:stepstone.de/jobs Abschlussarbeit <topic> <city>`
- `StepStone Bachelorarbeit <topic> <city>`
- `StepStone Masterarbeit <topic> <city>`

StepStone is useful for German Bachelorarbeit, Masterarbeit, and Abschlussarbeit
discovery, but it is noisy. Exclude ordinary jobs, internships, Werkstudent
roles, wrong-level postings, and topic-mismatch postings even when the platform
category or result count looks promising.

### `company_careers`

Use company career pages as both direct discovery surfaces and mirrors:

- `site:<company-domain> Bachelorarbeit <topic>`
- `site:<company-domain> Masterarbeit <topic>`
- `site:<company-domain> Abschlussarbeit <topic>`
- `"<title>" "<company>" Abschlussarbeit`
- `"<title>" "<company>" Masterarbeit`
- `"<title>" "<company>" thesis`

Prefer company pages when they confirm the same posting from LinkedIn or
StepStone. Do not invent open status if the company page is missing, stale, or
does not confirm the thesis.

## StepStone Fixture Expectations

These fixture-style cases define the intended filtering behavior:

| Fixture | Student Level | Visible Text | Expected Outcome |
|---|---|---|---|
| eligible bachelor | Bachelor | `Bachelorarbeit: Reinforcement Learning for automated driving simulation` | eligible if location/topic fit. |
| eligible master | Master | `Masterarbeit: Sensor Fusion fuer mobile Roboter` | eligible if location/topic fit. |
| generic Abschlussarbeit | Bachelor | `Abschlussarbeit im Bereich autonome Fahrzeuge, Bachelor oder Master moeglich` | eligible because the visible text includes Bachelor. |
| wrong-level | Bachelor | `Masterarbeit: Trajectory prediction with LiDAR` | exclude as `wrong thesis level`. |
| Werkstudent | Bachelor | `Werkstudent Robotik Software, ROS, 20h/Woche` | exclude as `Werkstudent/working-student role`. |
| internship | Master | `Praktikum / Internship Machine Learning Robotics` | exclude as `generic job/internship`. |
| topic mismatch | Master | `Masterarbeit: LLM chatbot for customer support` | exclude as `topic mismatch` when the profile excludes LLM/product support. |

## No Qualifying Results

When no candidate survives hard filters, say:

`No qualifying results after searched providers: <providers>.`

Then summarize what was searched and why the visible candidates were excluded or
too weak. Do not say that no thesis postings exist anywhere.
