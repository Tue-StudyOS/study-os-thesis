---
name: find-linkedin-company-theses
description: Find and rank public LinkedIn-indexed Bachelor and Master thesis opportunities at companies as a parallel lane to university chair thesis discovery, using a student's in-session profile and skills. Use when asked for Bachelorarbeit, Masterarbeit, Abschlussarbeit, company thesis, thesis at company, LinkedIn thesis postings, industry thesis topics, external thesis opportunities, or parallel company and university thesis search.
---

# Find LinkedIn Company Theses

Find public LinkedIn-indexed company thesis opportunities that match a student's profile, prior knowledge, and constraints. Use this as the company lane in a parallel thesis search alongside university chairs and supervisors. Treat LinkedIn as a public discovery surface only; do not require login, authenticated scraping, or a bundled posting database.

## Workflow

1. Check whether a deep enough student profile already exists in the conversation.
2. If the profile is shallow, use `build-student-profile` first and follow its advising baseline. Ask evidence-seeking questions about concrete coursework, projects, tools, work experience, thesis style, constraints, or no-gos. Do not ask for a search-parameter checklist yet.
3. One advising turn is not enough for normal use. After each answer, reflect what became clearer, reassess which profile fields are still missing, and ask the next focused advising question or small tightly grouped prompt bundle. Continue this profile-completion loop across turns until the profile is complete enough for thesis matching.
4. Do not search, rank, or produce company thesis leads until the profile is strong enough to include at least: thesis level or target degree, concrete courses or project evidence, practical skills/tools, preferred thesis style, relevant experience when available, location/work-mode constraints, sector exclusions, and no-gos. Also do not ask a radius/work-mode/sector checklist or rank university chairs until this profile gate is met.
5. Once the profile is strong enough, summarize the profile signals that will drive matching and prepare the parallel university/company search plan. Do not ask another standalone profile question. If institution plus region/radius/work-mode are already known, move into the provisional search plan immediately. Treat thesis timeline, language, and university-company process constraints as verification items that can be asked alongside the plan or checked before applying, not as blockers.
6. After profile-building is complete, run a parallel thesis search by default: use `find-university-chairs` and `match-thesis-advisors` for the university/chair lane, and use this skill's web-search procedure for the company lane. Only skip one lane if the user explicitly asks for company-only or university-only results.
7. Finish the shared search intake for both lanes: Bachelor, Master, or both; base location and radius in km; remote, hybrid, on-site, or all; sectors or company types to exclude; and any must-have or must-avoid technologies not already clear from the profile.
8. Read `references/ranking-rubric.md` and use its profile-first gate, profile-completion loop, parallel university/company comparison, hard exclusions, scorecard, evidence tiers, company-career mirror search, and output shape.
9. Use the active agent's normal web search tool to search public LinkedIn-indexed company results. Do not use a Markdown database, LinkedIn account, or authenticated browser session for the company lane.
10. Search with German and English variants such as:
   - `site:linkedin.com/jobs Bachelorarbeit <skill> <city>`
   - `site:linkedin.com/jobs Masterarbeit <skill> <city>`
   - `site:linkedin.com/jobs Abschlussarbeit <skill> Unternehmen <city>`
   - `site:linkedin.com/jobs thesis <skill> company <city>`
11. For promising LinkedIn results, use normal web search to look for a public company-career mirror when browsing is available. Prefer the company page if it confirms the same thesis posting.
12. Open public result pages when available, or use snippets when pages are inaccessible. Label each result with an evidence tier from the rubric and treat snippets as incomplete unless a public page was opened.
13. Accept only company results that visibly indicate a thesis opportunity, such as Bachelorarbeit, Masterarbeit, Abschlussarbeit, thesis, final thesis, or thesis project. Exclude ordinary jobs, internships, and working-student roles unless the visible text explicitly includes an Abschlussarbeit or thesis component.
14. Split company results into an eligible ranked shortlist and an excluded or not-recommended list. Do not let a strong technology match override hard mismatches such as excluded sectors, clearly incompatible location/work mode, or must-avoid technologies.
15. Score eligible company postings with the rubric scorecard, including thesis contribution and company-thesis readiness. Rank by hard exclusions first, then profile fit, thesis contribution, preference fit, feasibility, and evidence quality.
16. Compare the strongest university/chair matches and company postings side by side. Distinguish university research-fit evidence from confirmed company thesis postings; do not present research areas as official open university topics.
17. For each ranked company posting, explicitly check whether preferences are fulfilled: thesis level, location/radius, remote/hybrid/on-site mode, sector/no-gos, must-have technologies, must-avoid technologies, company-thesis readiness, and evidence quality.
18. Include the access date and visible posting date for each result; use `date unclear` when no posting date is visible.
19. If subagents are available and many results need review, they may extract visible facts from batches of company results or university pages. The main agent must merge evidence and rank centrally using the full student profile.

## Output

Return a short parallel thesis-search summary, not an exhaustive scrape:

- Profile signals used for both lanes
- University/chair lane: relevant chairs, labs, or supervisors from `find-university-chairs` / `match-thesis-advisors`, with evidence and caveats
- Company lane: ranked company thesis postings from public LinkedIn-indexed or company-career evidence
- Cross-lane comparison: best next actions, tradeoffs, and which lane currently has stronger evidence

For each company thesis opportunity include:

- Company
- Thesis title or topic
- Bachelor/Master fit, when visible
- LinkedIn or public result link
- Location and work mode, when visible
- Matched profile evidence, such as relevant courses, projects, skills, tools, or work experience
- Scorecard covering thesis level, profile fit, feasibility gap, location/radius, work mode, sector/no-gos, required technologies, avoided technologies, thesis contribution, company-thesis readiness, and evidence quality
- Missing or risky requirements
- Sector fit or exclusion caveat
- Visible posting date or `date unclear`
- Evidence tier, evidence source, and access date
- Ranking rationale and confidence level

After the company shortlist, include excluded or not-recommended postings with the exact reason: not a thesis, generic job/internship, location or work-mode mismatch, excluded sector, must-avoid technology, weak profile match, or insufficient evidence. End with a compact checklist split into university-lane contact preparation and company-thesis readiness checks.

## Guardrails

- Act like a thesis-oriented study advisor first and a search assistant second.
- Treat company thesis search as a parallel complement to university/chair matching, not as a replacement.
- Use the full in-session student profile for processing and ranking, not only keyword matches.
- Do not turn a shallow request into a generic Google/LinkedIn search. Build the student profile first.
- Do not treat one answered profile question as a complete profile. Continue the advising loop with reflective summaries until the profile is complete enough for the same quality of matching expected by the university-thesis workflow.
- Do not over-block once the profile is strong. If only minor company logistics remain, summarize the profile and move into a parallel search plan while asking the missing logistics.
- Do not ask "one last" profile refinement as a blocker after readiness. Optional refinements must travel with the plan.
- Do not ask thesis timing, language, or formal university-company rules as the next standalone turn after the student has already supplied institution, region, work mode, topic, skills, and no-gos.
- Do not present ordinary jobs as thesis opportunities.
- Do not invent thesis availability, supervision capacity, application deadlines, remote policy, salary, or company willingness.
- Do not bypass LinkedIn access controls or require login.
- Do not store student-private profile data in shared skill files.
- Do not run a live search before the student profile and search intake are complete unless the user explicitly asks for a low-confidence exploratory pass; in that case, label the output as exploratory and low confidence.
- Do not skip the university/chair lane when the user asks broadly for thesis options, unless they explicitly want company-only results.
- If web search is unavailable, say that live LinkedIn-indexed discovery cannot be performed and ask the user to provide public posting links or snippets.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
