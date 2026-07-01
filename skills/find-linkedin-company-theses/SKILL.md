---
name: find-linkedin-company-theses
description: Find and rank public provider-indexed Bachelor and Master thesis opportunities at companies as a parallel lane to university chair thesis discovery, using a student's in-session profile and skills. Use when asked for Bachelorarbeit, Masterarbeit, Abschlussarbeit, company thesis, thesis at company, LinkedIn or StepStone thesis postings, industry thesis topics, external thesis opportunities, or parallel company and university thesis search.
---

# Find External Company Theses

Find public company thesis opportunities that match a student's profile, prior knowledge, and constraints. Use this as the external/company lane in a parallel thesis search alongside university chairs and supervisors. Treat LinkedIn public search, StepStone, and company career pages as providers; do not require login, authenticated scraping, provider APIs, or a bundled posting database.

## Workflow

1. Check whether a deep enough student profile already exists in the conversation.
2. If the profile is shallow, use `build-student-profile` first and follow its advising baseline. Ask evidence-seeking questions about concrete coursework, projects, tools, work experience, thesis style, constraints, or no-gos. Do not ask for a search-parameter checklist yet.
3. Expect the profile phase to be a real advising conversation, not a quick pre-search form. It may take many turns or roughly 30-60 minutes before the student's nuanced tradeoffs are clear enough for high-confidence ranking.
4. One advising turn is not enough for normal use. After each answer, reflect what became clearer, reassess which profile fields are still missing, and ask the next focused advising question or small tightly grouped prompt bundle. Continue this profile-completion loop across turns until the profile is complete enough for thesis matching.
5. Do not search, rank, or produce company thesis leads until the profile is strong enough to include at least: confirmed thesis level or target degree, concrete liked/disliked courses and assignments, project/work/HiWi/internship evidence with role and ownership, practical skills/tools, research skills, preferred thesis style, working and supervision style, career goals, nuanced tradeoffs, relevant experience when available, location/work-mode constraints, sector exclusions, and no-gos. Also do not ask a radius/work-mode/sector checklist or rank university chairs until this profile gate is met.
6. Once the profile is strong enough, summarize the profile signals that will drive matching and prepare the parallel university/company search plan. Do not ask another standalone profile question. If institution plus region/radius/work-mode are already known, move into the provisional search plan immediately. Treat thesis timeline, language, and university-company process constraints as verification items that can be asked alongside the plan or checked before applying, not as blockers.
7. After profile-building is complete, run a parallel thesis search by default: use `find-university-chairs` and `match-thesis-advisors` for the university/chair lane, and use this skill's provider-based web-search procedure for the company lane. Only skip one lane if the user explicitly asks for company-only or university-only results.
8. Finish the shared search intake for both lanes: confirmed thesis level, base location and radius in km, remote/hybrid/on-site/all, sectors or company types to exclude, and any must-have or must-avoid technologies not already clear from the profile. If the thesis level is missing or ambiguous, ask whether the student needs Bachelorarbeit, Masterarbeit, or both before searching. Once confirmed, search and rank only postings compatible with that level.
9. Read `references/ranking-rubric.md`, `references/candidate-schema.md`, and `references/provider-fetching.md`. Use the profile-first gate, query matrix, provider labels, candidate schema, parallel university/company comparison, hard exclusions, scorecard, evidence tiers, company-career mirror search, and output shape.
10. Use the active agent's normal web search tool to search public provider results. Start with LinkedIn public search, StepStone, and company-career mirrors. Do not use a Markdown database, LinkedIn account, StepStone account, authenticated browser session, or provider API for the company lane.
11. Build a query matrix from the profile: confirmed thesis level, region/radius, topic synonyms, sector/no-go terms, must-have technologies, and must-avoid technologies. Treat provider result counts as discovery evidence, not recommendations.
12. Search with German and English variants that match the confirmed thesis level. For a Bachelor profile, search Bachelorarbeit/Bachelor thesis terms and level-compatible Abschlussarbeit terms; do not include Masterarbeit-only searches. For a Master profile, search Masterarbeit/Master thesis terms and level-compatible Abschlussarbeit terms; do not include Bachelorarbeit-only searches unless the user explicitly asks for both. Query examples:
   - `site:linkedin.com/jobs Bachelorarbeit <skill> <city>`
   - `site:linkedin.com/jobs Masterarbeit <skill> <city>`
   - `site:linkedin.com/jobs Abschlussarbeit <skill> Unternehmen <city>`
   - `site:linkedin.com/jobs thesis <skill> company <city>`
   - `site:stepstone.de/jobs Bachelorarbeit <skill> <city>`
   - `site:stepstone.de/jobs Masterarbeit <skill> <city>`
   - `site:stepstone.de/jobs Abschlussarbeit <skill> <city>`
13. For promising LinkedIn or StepStone results, use normal web search to look for a public company-career mirror when browsing is available. Prefer the company page if it confirms the same thesis posting, but keep the original provider label and source URL.
14. Open public result pages when available, or use snippets when pages are inaccessible. Normalize every possible posting into the candidate schema, label its provider and evidence tier, and treat snippets as incomplete unless a public page was opened.
15. Accept only company results that visibly indicate a thesis opportunity at the student's confirmed level, such as Bachelorarbeit for a Bachelor profile or Masterarbeit for a Master profile. Generic Abschlussarbeit/thesis/final thesis is eligible only when the visible text or source can be mapped to the student's level or is explicitly open to that level.
16. Exclude ordinary jobs, internships, traineeships, Werkstudent roles, working-student roles, and student assistant roles from the company thesis lane even if they mention relevant technologies. Do not rescue them with a strong skill match; they are not thesis opportunities.
17. Split company results into an eligible ranked shortlist and an excluded or not-recommended list. Do not let a strong technology match override hard mismatches such as thesis-level mismatch, excluded sectors, topic mismatch, clearly incompatible location/work mode, must-avoid technologies, or Werkstudent/working-student role type.
18. Score eligible company postings with the rubric scorecard, including thesis contribution and company-thesis readiness. Rank by hard exclusions first, then profile fit, thesis contribution, preference fit, feasibility, and evidence quality.
19. Compare the strongest university/chair matches and company postings side by side. Distinguish university research-fit evidence from confirmed company thesis postings; do not present research areas as official open university topics.
20. For each ranked company posting, explicitly check whether preferences are fulfilled: confirmed thesis level, location/radius, remote/hybrid/on-site mode, sector/no-gos, topic fit, must-have technologies, must-avoid technologies, company-thesis readiness, and evidence quality.
21. Include the provider label, source URL, mirror URL when found, access date, and visible posting date for each result; use `date unclear` when no posting date is visible.
22. If no eligible postings remain, say `no qualifying results after searched providers`, list the providers searched, and summarize excluded or inconclusive evidence. Do not say or imply that no postings exist anywhere.
23. If subagents are available and many results need review, they may extract visible facts from batches of company results or university pages. The main agent must merge evidence and rank centrally using the full student profile.

## Output

Return a short parallel thesis-search summary, not an exhaustive scrape:

- Profile signals used for both lanes
- University/chair lane: relevant chairs, labs, or supervisors from `find-university-chairs` / `match-thesis-advisors`, with evidence and caveats
- Company lane: ranked company thesis postings from public LinkedIn, StepStone, or company-career evidence
- Cross-lane comparison: best next actions, tradeoffs, and which lane currently has stronger evidence

For each company thesis opportunity include:

- Provider
- Source URL
- Company
- Thesis title or topic
- Bachelor/Master fit, when visible
- Public result link and company-career mirror URL, when found
- Location and work mode, when visible
- Matched profile evidence, such as relevant courses, projects, skills, tools, or work experience
- Scorecard covering thesis level, profile fit, feasibility gap, location/radius, work mode, sector/no-gos, required technologies, avoided technologies, thesis contribution, company-thesis readiness, and evidence quality
- Missing or risky requirements
- Sector fit or exclusion caveat
- Visible posting date or `date unclear`
- Evidence tier, evidence source, provider label, and access date
- Ranking rationale and confidence level

After the company shortlist, include excluded or not-recommended postings with the exact reason: not a thesis, wrong thesis level, generic job/internship, Werkstudent/working-student role, topic mismatch, location or work-mode mismatch, excluded sector, must-avoid technology, weak profile match, or insufficient evidence. End with a compact checklist split into university-lane contact preparation and company-thesis readiness checks.

When proposal sketches are generated from the parallel search, label each sketch as one of:

- `external posting/snippet-derived lead`: grounded in visible company thesis evidence, with live status still requiring verification
- `university research-area conversation starter`: grounded in chair/lab evidence, not an advertised thesis
- `hybrid/external feasibility hypothesis`: requires both a company lead and university supervision verification

## Guardrails

- Act like a thesis-oriented study advisor first and a search assistant second.
- Treat company thesis search as a parallel complement to university/chair matching, not as a replacement.
- Use the full in-session student profile for processing and ranking, not only keyword matches.
- Do not turn a shallow request into a generic Google/LinkedIn/StepStone search. Build the student profile first.
- Do not treat a moderate profile such as "ML Master at Tuebingen, likes neural networks/RL/CV, has one PyTorch project, dislikes theory" as ready for company or chair search.
- Do not ask which university the student attends; assume University of Tuebingen unless the student explicitly says otherwise.
- Do not search or generate Bachelor and Master thesis results together unless the student explicitly asked for both; thesis level is a hard filter, not a soft preference.
- Do not treat one answered profile question as a complete profile. Continue the advising loop with reflective summaries until the profile is complete enough for the same quality of matching expected by the university-thesis workflow.
- Do not over-block once the profile is strong. If only minor company logistics remain, summarize the profile and move into a parallel search plan while asking the missing logistics.
- Do not ask "one last" profile refinement as a blocker after readiness. Optional refinements must travel with the plan.
- Do not ask thesis timing, language, or formal university-company rules as the next standalone turn after the student has already supplied institution, region, work mode, topic, skills, and no-gos.
- Do not present ordinary jobs as thesis opportunities.
- Do not present Werkstudent, working-student, student assistant, internship, trainee, or ordinary job roles as thesis opportunities.
- Do not invent thesis availability, supervision capacity, application deadlines, remote policy, salary, or company willingness.
- Do not bypass LinkedIn, StepStone, or company career access controls or require login.
- Do not store student-private profile data in shared skill files.
- Do not run a live search before the student profile and search intake are complete unless the user explicitly asks for a low-confidence exploratory pass; in that case, label the output as exploratory and low confidence.
- Do not skip the university/chair lane when the user asks broadly for thesis options, unless they explicitly want company-only results.
- If web search is unavailable, say that live provider-indexed discovery cannot be performed and ask the user to provide public posting links or snippets.
- Do not depend on the old UI, backend API, database, Docker, Celery, or FastAPI app.
