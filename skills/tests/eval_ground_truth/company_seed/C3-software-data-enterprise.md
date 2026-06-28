# Ground Truth — Profile C3: Software / Data Engineering + Enterprise

**Profile summary:**
- **Interests:** Distributed systems, data pipelines, large language models for enterprise use cases
- **Methods:** Systems engineering, quantitative evaluation, benchmark design, engineering prototypes
- **Domain:** Enterprise software, SaaS, data platforms, fintech/banking
- **Thesis style:** Engineering / systems — working implementation or reproducible benchmark as deliverable
- **Skills:** Python, SQL, Spark / Flink; cloud platforms (AWS/GCP/Azure); basic ML literacy; optional Go/Java for systems work
- **No-gos:** Embedded hardware; automotive domain without software focus; pure management consulting without technical depth; no-go on purely non-technical roles

**Scope:** BW companies in enterprise software, AI/LLM platforms, and data engineering with confirmed or strongly inferred thesis programs
**Date verified:** 2026-06-28

| Company | Division / team | Sector tags | Thesis signal | Confirmation URL | Date verified |
|---|---|---|---|---|---|
| SAP SE | SAP Labs Germany / Data & AI / HANA Cloud | `[enterprise software, AI/ML]` | explicit program — jobs.sap.com student portal active; 2025 Master Thesis listing in Agentic AI confirmed (Walldorf) | https://jobs.sap.com/content/Studierende/?locale=de_DE | 2026-06-28 |
| MHP Management- und IT-Beratung GmbH | Technology & Data / Intelligent Software | `[consulting, AI/ML]` | explicit opening — jobs.mhp.com lists active "Thesis Student (f/m/d) Technology and Data" and "Intelligent Software" positions at Ludwigsburg | https://jobs.mhp.com/?ac=jobad&id=24594&language=2 | 2026-06-28 |
| Aleph Alpha GmbH | Research / Enterprise AI | `[AI/ML, NLP, LLMs]` | unclear — active AI research startup with open positions; no explicit Masterarbeit listing found; direct outreach to research team recommended | https://jobs.ashbyhq.com/AlephAlpha | 2026-06-28 |
| TeamViewer AG | Engineering / Product R&D | `[software, cloud]` | unclear — large enterprise software company (Göppingen, ~15k employees); student/working-student positions visible; no explicit thesis listing found during verification | https://www.teamviewer.com/en/company/careers/ | 2026-06-28 |
| Porsche Digital GmbH | Data Engineering / Platform | `[automotive, AI/ML]` | active program (inferred) — independent digital subsidiary of Porsche AG; parent runs one of BW's largest thesis programs; Porsche Digital posts software and data engineering roles; careers via shared portal | https://jobs.porsche.com | 2026-06-28 |

## Notes

- **Recall rule:** a company is counted as surfaced if the skill names it or its relevant division. "SAP Labs Germany" → counts for SAP; "MHP" without division → counts.
- **Thesis signal scoring:** for SAP and MHP the correct classification is `explicit opening` or `active program`. For Aleph Alpha and TeamViewer the correct classification is `unclear`. For Porsche Digital it is `active program`.
- Field 33 GmbH (backbone: `[AI/ML, software]`) and other AI/ML startups in the backbone are in scope for this profile but not in this seed — surfacing them is a bonus, not required.
- The profile's "no-go on embedded" should cause the skill to deprioritize sensor/hardware companies; confirm the skill does not include backbone entries tagged `[IoT, sensors]` without qualification.
- Aleph Alpha and TeamViewer are included despite "unclear" thesis signal because both are in the backbone with matching tags — the skill should surface them (with correct `unclear` classification) and the ground truth counts a surfaced `unclear` entry as a recall hit.
