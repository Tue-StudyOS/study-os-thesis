# LinkedIn Company Thesis Ranking Rubric

Use this rubric to filter and rank public LinkedIn-indexed Bachelor and Master thesis opportunities at companies. Keep the scoring qualitative and evidence-based; do not invent facts that are not visible in the result or public page.

## Profile-First Gate

Do not use this skill as a generic LinkedIn or Google search shortcut. Before searching, the agent must have a usable in-session student profile with concrete evidence about the student's thesis level or degree target, courses or project work, skills/tools, thesis style, constraints, sector exclusions, and no-gos.

If the profile is shallow, stop before search and continue with `build-student-profile`. Ask one focused advising question by default. Search parameters such as radius, work mode, and sectors are collected after the profile is strong enough to make those filters meaningful.

### Profile-Completion Loop

One question and one answer are not enough for normal use. After every student reply, reflect what became clearer, reassess the profile, and continue with the next most important missing aspect until the profile supports the same quality of matching expected by the university-thesis workflow.

The target behavior is a study-advising conversation, not a narrow search script. The agent should summarize intermediate evidence, infer research taste carefully, and ask deeper follow-ups about project ownership, tools, evaluation style, disliked work, and domain constraints.

Before any LinkedIn/company search, university/chair ranking, or search-parameter checklist, the profile should cover:

- thesis level or target degree program
- concrete motivation, interests, and research taste
- liked or disliked courses, seminars, labs, or topics
- practical projects, work experience, research experience, or substantial assignments
- technical skills, tools, frameworks, methods, and implementation comfort
- preferred thesis style, such as empirical ML, systems/engineering, robotics experimentation, theory, or scientific analysis
- constraints and no-gos
- external-thesis filters: location/radius, remote/hybrid/on-site preference, sector exclusions, and must-have or must-avoid technologies

If only one or two of these areas are known, ask the next focused advising question and do not search. If the student explicitly requests speed, label any exploratory result as low confidence and state which profile gaps make the ranking weak.

If the core profile is strong and only minor company logistics remain, do not keep delaying. Summarize the profile, state the parallel university/company search plan, and ask the missing logistics as a final intake before live search.

Readiness is reached once the agent knows the student's thesis level/program, motivation, project or course evidence, tools, experience depth, thesis style, constraints/no-gos, institution or region, and external thesis feasibility. After readiness, do not ask another standalone profile question. If a refinement would help, include it after the plan as an optional final check.

Timing, language, and university-company registration details are important verification checklist items, but they are not reasons to delay the first parallel university/company search plan once the student's profile, region, work mode, topic, skills, and no-gos are known.

## Parallel University/Company Search

Use this skill as the company lane in a dual thesis-discovery workflow:

- University/chair lane: use `find-university-chairs` and `match-thesis-advisors` to identify relevant chairs, labs, supervisors, research areas, recent evidence, caveats, and proposal hooks.
- Company lane: use public LinkedIn-indexed and company-career evidence to identify explicit Bachelor or Master thesis postings at companies.
- Shared basis: both lanes must use the same in-session student profile, constraints, no-gos, and skill evidence.
- Output: compare the best university/chair options and company postings side by side. Explain which lane has stronger evidence, which has higher feasibility risk, and which next action fits the student's profile.

Do not treat university research areas as confirmed open thesis topics. Do not treat company postings as supervision commitments beyond the visible evidence.

## Hard Exclusion Criteria

Exclude a result from the ranked shortlist when any of these apply:

- The visible text does not indicate Bachelorarbeit, Masterarbeit, Abschlussarbeit, thesis, final thesis, or thesis project.
- It is an ordinary job, internship, trainee role, or working-student role without an explicit thesis component.
- The sector or application area conflicts with the student's excluded sectors or no-gos.
- The location and work mode clearly violate the student's constraints, such as full on-site work outside the accepted radius.
- The core stack is dominated by must-avoid technologies or blocks the student's required working style.
- The visible evidence is too thin to verify that a thesis opportunity exists.

Do not let a strong technology match override a hard exclusion.

## Scorecard

For every eligible result, produce a compact scorecard. Use `pass`, `partial`, `fail`, or `unclear` for each row:

| Criterion | What To Check |
|---|---|
| Thesis level | Bachelor, Master, or both matches the student. |
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

- `A`: Opened public LinkedIn page or company career page confirms the thesis details.
- `B`: Search snippet visibly confirms a LinkedIn-indexed thesis posting, but the page was not opened.
- `C`: Indirect public result suggests a thesis posting, but key details are missing.
- `D`: Stale, inaccessible, or ambiguous evidence; do not rank unless the user explicitly asks for a low-confidence lead.

Use absolute access dates. Use `date unclear` when no posting date is visible.

## Company-Career Mirror Search

LinkedIn snippets can be stale or incomplete. For promising results, use normal web search to look for public company mirrors when browsing is available:

- `"<title>" "<company>" Abschlussarbeit`
- `"<title>" "<company>" Masterarbeit`
- `"<title>" "<company>" thesis`
- `site:<company-domain> <title>`

Prefer company career pages over search snippets when they confirm the same opportunity. Do not use a LinkedIn login or authenticated scraping.

## Output Shape

Return:

1. Shared profile signals used for both lanes.
2. University/chair lane shortlist with research-fit evidence, caveats, and proposal/contact hooks.
3. Company lane ranked shortlist with each posting's scorecard, matched profile evidence, evidence tier, access date, visible posting date, rationale, and confidence.
4. Excluded or not-recommended company postings with exact reasons tied to the hard exclusion criteria.
5. Cross-lane comparison and next actions.
6. Verification checklist focused on university contact preparation and company-thesis readiness: open status, start date, compensation/workload, academic supervision, university-company process, data access, confidentiality, reportability, reproducible tooling, and evaluation metric.
