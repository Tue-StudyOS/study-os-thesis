# External Company Thesis Ranking Rubric

Use this rubric to filter and rank public provider-indexed Bachelor and Master thesis opportunities at companies. LinkedIn public search, StepStone, and company career pages are discovery providers, not guarantees of fit or availability. Keep the scoring qualitative and evidence-based; do not invent facts that are not visible in the result or public page.

## Profile-First Gate

Do not use this skill as a generic LinkedIn or Google search shortcut. Before searching, the agent must have a usable in-session student profile with concrete evidence about the student's confirmed thesis level or degree target, liked/disliked courses and assignments, project/work/HiWi/internship evidence with role and ownership, skills/tools, research skills, working style, thesis style, career goals, constraints, sector exclusions, and no-gos.

If the profile is shallow, stop before search and continue with `build-student-profile`. Ask one focused advising question by default. Search parameters such as radius, work mode, and sectors are collected after the profile is strong enough to make those filters meaningful.

### Profile-Completion Loop

One question and one answer are not enough for normal use. After every student reply, reflect what became clearer, reassess the profile, and continue with the next most important missing aspect until the profile supports the same quality of matching expected by the university-thesis workflow.

The target behavior is a study-advising conversation, not a narrow search script. In real use, the profile phase may take many turns or roughly 30-60 minutes before generation. The agent should summarize intermediate evidence, infer research taste carefully, and ask deeper follow-ups about project ownership, tools, evaluation style, disliked work, domain constraints, and tradeoffs.

Before any provider/company search, university/chair ranking, or search-parameter checklist, the profile should cover:

- confirmed thesis level or target degree program
- concrete motivation, interests, and research taste
- liked and disliked courses, seminars, labs, assignments, or topics
- practical projects, work experience, HiWi work, research experience, open-source work, or substantial assignments, including exact roles, responsibilities, ownership, tools, and what the student enjoyed or disliked
- technical skills, tools, frameworks, methods, implementation comfort, debugging habits, evaluation habits, and research skills
- preferred thesis style, such as empirical ML, systems/engineering, robotics experimentation, theory, or scientific analysis
- working style, supervision preferences, independence/collaboration preference, and career goals
- nuanced tradeoffs, such as safe scope vs. open-ended research, university-led vs. company-led thesis, familiar tools vs. new tools, and engineering output vs. research insight
- constraints and no-gos
- external-thesis filters: location/radius, remote/hybrid/on-site preference, sector exclusions, and must-have or must-avoid technologies

The confirmed thesis level is a hard gate. Do not mix Bachelorarbeit and Masterarbeit results unless the student explicitly asks for both. If the student says Bachelorarbeit, exclude Masterarbeit-only postings and do not generate Masterarbeit proposals. If the student says Masterarbeit, exclude Bachelorarbeit-only postings and do not generate Bachelorarbeit proposals.

If only one or two of these areas are known, ask the next focused advising question and do not search. A moderate profile with a program, a few interests, one project, tools, and one no-go is still not ready for company or chair ranking. If the student explicitly requests speed, label any exploratory result as low confidence and state which profile gaps make the ranking weak.

If the comprehensive profile is strong and only minor company logistics remain, do not keep delaying. Summarize the profile, state the parallel university/company search plan, and ask the missing logistics as a final intake before live search.

Readiness is reached once the agent knows the student's confirmed thesis level/program, motivation, course evidence, project/work evidence, tools, experience depth, research skills, thesis style, working style, supervision preferences, career goals, constraints/no-gos, Tuebingen context or explicit exception, and external thesis feasibility. After readiness, do not ask another standalone profile question. If a refinement would help, include it after the plan as an optional final check.

Timing, language, and university-company registration details are important verification checklist items, but they are not reasons to replace missing discovery about coursework, experience, skills, working style, and goals.

## Parallel University/Company Search

Use this skill as the company lane in a dual thesis-discovery workflow:

- University/chair lane: use `find-university-chairs` and `match-thesis-advisors` to identify relevant chairs, labs, supervisors, research areas, recent evidence, caveats, and proposal hooks.
- Company lane: use public provider-indexed evidence from LinkedIn public search, StepStone, and company-career pages to identify explicit Bachelor or Master thesis postings at companies.
- Shared basis: both lanes must use the same in-session student profile, constraints, no-gos, and skill evidence.
- Output: compare the best university/chair options and company postings side by side. Explain which lane has stronger evidence, which has higher feasibility risk, and which next action fits the student's profile.

Do not treat university research areas as confirmed open thesis topics. Do not treat company postings as supervision commitments beyond the visible evidence.

## Provider Fetching And Candidate Schema

Build a query matrix from the confirmed thesis level, region/radius, topic
synonyms, sector exclusions, must-have technologies, and must-avoid
technologies. Use `references/provider-fetching.md` for provider-specific query
patterns and StepStone fixture expectations.

Normalize every possible result with `references/candidate-schema.md` before
ranking or exclusion. Each candidate must carry a `provider`, `source_url`,
`title`, `company`, `location`, `thesis_level`, `job_type`, `visible_date`,
`evidence_text`, `evidence_tier`, `matched_keywords`, `exclusion_reason`,
`mirror_url`, and `access_date`.

Treat provider result counts as discovery evidence only. A StepStone or
LinkedIn count can justify more inspection, but it must not be presented as a
shortlist item or availability proof.

For Bachelor students, search only Bachelorarbeit/Bachelor thesis and
level-compatible Abschlussarbeit/final thesis queries. For Master students, search only Masterarbeit/Master thesis and level-compatible Abschlussarbeit/final
thesis queries. Do not mix Bachelorarbeit and Masterarbeit unless the student
explicitly asks for both.

## Hard Exclusion Criteria

Exclude a result from the ranked shortlist when any of these apply:

- The visible text does not indicate Bachelorarbeit, Masterarbeit, Abschlussarbeit, thesis, final thesis, or thesis project.
- The posting thesis level conflicts with the student's confirmed level, such as Masterarbeit-only for a Bachelor student or Bachelorarbeit-only for a Master student.
- It is an ordinary job, internship, trainee role, Werkstudent role, working-student role, student assistant role, or similar non-thesis employment format.
- The sector or application area conflicts with the student's excluded sectors or no-gos.
- The topic visibly conflicts with the student's target direction or explicit no-gos.
- The location and work mode clearly violate the student's constraints, such as full on-site work outside the accepted radius.
- The core stack is dominated by must-avoid technologies or blocks the student's required working style.
- The visible evidence is too thin to verify that a thesis opportunity exists.

Do not let a strong technology match override a hard exclusion.

## Scorecard

For every eligible result, produce a compact scorecard. Use `pass`, `partial`, `fail`, or `unclear` for each row:

| Criterion | What To Check |
|---|---|
| Thesis level | The posting explicitly matches the student's confirmed level, or is explicitly open to that level. |
| Profile fit | Courses, projects, skills, tools, and work experience map to the topic. |
| Feasibility gap | Missing requirements look manageable for the thesis timeline. |
| Location/radius | City, commute, and radius fit or can be verified. |
| Work mode | Remote, hybrid, or on-site terms fit the student. |
| Sector/no-gos | Sector and work style do not conflict with exclusions. |
| Required technologies | Must-have technologies or methods are visible. |
| Avoided technologies | Must-avoid tools are absent or only peripheral. |
| Thesis contribution | The topic has an implementable question, evaluation metric, or research contribution. |
| Company-thesis readiness | Start date, pay/workload, academic supervision, data access, and reportability are visible or need verification. |
| Evidence quality | Source freshness and public evidence are strong enough to rank. |

Rank by hard exclusions first, then by profile fit, thesis contribution, preference fit, feasibility, and evidence quality. When two postings are close, prefer the one with clearer evaluation metrics and fewer company-thesis readiness risks.

## Evidence Tiers

Label each result with the strongest available evidence tier:

- `A`: Opened public provider page or company career page confirms the thesis details.
- `B`: Search snippet visibly confirms a provider-indexed thesis posting, but the page was not opened.
- `C`: Indirect public result, provider count, or listing category suggests a thesis posting, but key details are missing.
- `D`: Stale, inaccessible, or ambiguous evidence; do not rank unless the user explicitly asks for a low-confidence lead.

Use absolute access dates. Use `date unclear` when no posting date is visible.

## Company-Career Mirror Search

LinkedIn and StepStone snippets can be stale or incomplete. For promising
results, use normal web search to look for public company mirrors when browsing
is available:

- `"<title>" "<company>" Abschlussarbeit`
- `"<title>" "<company>" Masterarbeit`
- `"<title>" "<company>" thesis`
- `site:<company-domain> <title>`

Prefer company career pages over search snippets when they confirm the same
opportunity. Keep the discovery provider and original source URL in the
candidate record, and add the confirming page as `mirror_url`. Do not use a
LinkedIn login, StepStone login, provider API, or authenticated scraping.

## No Qualifying Results

If no candidate survives hard exclusions, say `no qualifying results after
searched providers`, name the providers and query families searched, and list
the most important excluded or inconclusive evidence. Do not say or imply that
no postings exist anywhere.

## Output Shape

Return:

1. Shared profile signals used for both lanes.
2. University/chair lane shortlist with research-fit evidence, caveats, and proposal/contact hooks.
3. Company lane ranked shortlist with each posting's provider, source URL, mirror URL if found, scorecard, matched profile evidence, evidence tier, access date, visible posting date, rationale, and confidence.
4. Excluded or not-recommended company postings with exact reasons tied to the hard exclusion criteria, including wrong thesis level, not a thesis, generic job/internship, Werkstudent/working-student role, topic mismatch, location/work-mode mismatch, excluded sector, must-avoid technology, weak profile match, and insufficient evidence.
5. Cross-lane comparison and next actions.
6. Proposal sketches, when requested, each labeled as `external posting/snippet-derived lead`, `university research-area conversation starter`, or `hybrid/external feasibility hypothesis`.
7. Verification checklist focused on university contact preparation and company-thesis readiness: open status, start date, compensation/workload, academic supervision, university-company process, data access, confidentiality, reportability, reproducible tooling, and evaluation metric.
