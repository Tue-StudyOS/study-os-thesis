# Skill Architecture Summary — StudyOS Thesis Advisor

**Date:** 2026-06-11 · **Context:** Post-professor-meeting evaluation + technical clarification on Agent Skills
**Related docs:** [detailed_analysis.md](detailed_analysis.md), [product_positioning.md](product_positioning.md), [technical_roadmap.md](technical_roadmap.md)

All Skill-related claims are verified against official Anthropic documentation (Agent Skills Overview, Skills API Guide, Claude Code Skills).

---

## 1. Starting Point — What the Professor Proposed

The professor suggested an **architecture pivot**:

- Deliver the entire app **not** as a hosted web app with its own UI, but as **a single Claude Skill** that the department can provide.
- For **each eligible supervisor** (professor or PhD student), create **one Markdown file** — a combination of chair info and that person's concrete research and topics.
- Based on this curated **"database"** and the student's extracted interests and prior knowledge, the tool finds **matching supervisors**.

This direction is technically sound and actually solves several existing problems (see §8). The critical question is not the Skill technology itself but **distribution to "the department"** and **monthly updates** (§5, §6).

---

## 2. How a Skill Works (Quick Overview)

A Skill is **not a single script** — it is a **directory**, like an onboarding folder for a new employee. It contains a required `SKILL.md` (YAML frontmatter with `name` + `description`, then a Markdown body with instructions) and **any number of additional files**: extra guides, executable scripts, and data/resources.

The key mechanism is **progressive disclosure** across three tiers — only what is needed lands in context:

| Tier | Loaded when | Token cost | Contents |
|---|---|---|---|
| **1: Metadata** | always (on startup) | ~100 tokens/Skill | `name` + `description` only |
| **2: Instructions** | when the Skill is triggered | < 5k tokens | the `SKILL.md` body |
| **3: Resources** | only on demand | **effectively unlimited** | bundled files, read individually via `bash` |

Three content types with different strengths:
- **Instructions** (Markdown) — flexibly interpreted, not rigid.
- **Scripts** (e.g. Python) — deterministic; the code does **not** land in context, only the result.
- **Resources** (MD / JSON / CSV) — fact retrieval, read on demand.

### We Only Need **One** Skill

There is no need for a bundle of multiple Skills. A single, well-structured Skill is sufficient: the `SKILL.md` orchestrates the entire flow and delegates to sub-files (matching logic, thesis guide, the researcher database, the GPA script) when needed. This keeps maintenance simple and the structure clear.

---

## 3. The "Database" as Bundled Files

> Question from the meeting: *Can the data already be provided as a "database" so each user doesn't have to scrape themselves?*

**Yes — exactly that.** According to the docs there is *"no practical limit on bundled content"* because files only cost tokens when they are read.

- You scrape/curate **once as a team** and store **one `.md` file per person** in the Skill (e.g. under `researchers/`).
- Individual students **scrape nothing** — the data is already in the Skill.
- On a query, Claude reads **only the few relevant researcher files**, not all of them. Even with hundreds of files the context does not explode.
- The level of detail is **effectively unlimited**. The bottleneck is not data volume but **findability** — hence the need for an index file (keywords per person) that `SKILL.md` references.

The **GPA calculation** is bundled as a deterministic script — which also fixes the floating-result bug from [de/ideen_bewertung.md](de/ideen_bewertung.md) (idea 10), because the calculation no longer depends on LLM sampling noise.

---

## 4. Recommended Skill Structure

```
thesis-advisor/
├── SKILL.md                  # Top-level instructions: flow, matching rules,
│                             #   recommendation balance, contact coaching
├── MATCHING.md               # Detailed matching heuristics (loaded on demand)
├── THESIS_GUIDE.md           # Generic thesis process + links to exam office etc.
├── researchers/
│   ├── INDEX.md              # Keyword index of all persons (findability!)
│   ├── prof-mustermann.md    # Research, supervised topics, prerequisites
│   ├── phd-xyz.md
│   └── …                     # One file per person, as detailed as needed
└── scripts/
    └── compute_gpa.py        # Deterministic GPA calculation (excludes ÜBK)
```

---

## 5. Monthly Data Updates

> Goal: re-scrape once a month so the Skill's data stays current.

**The re-scrape itself is the easy part** — a standard pipeline (most naturally a **GitHub Actions `schedule:` cron**) that monthly: scrapes → regenerates `researchers/*.md` → packages the Skill → publishes. Steps 1–3 are your existing code run as a batch job.

**Whether you need to "upload new versions" depends on the platform:**

- **Claude API (clean path):** Full versioning is supported. The **`skill_id` stays stable**; you only create a new version (`POST /v1/skills/{skill_id}/versions`). Consumers referencing `version: "latest"` **get the fresh version automatically** — no user action required. The monthly update becomes **a single automated API call** from the pipeline. (Limit: 30 MB per upload.)
- **claude.ai (painful path):** **No** central version management, no automatic "latest". Every user would have to manually download and re-upload the new ZIP — untenable at monthly cadence.
- **Claude Code:** File-based or via plugin/marketplace → update via `git pull` / plugin update. Cleanly automatable, but only reaches Claude Code users.

**Why not fetch from a server at runtime instead of bundling?** Because the runtime environment usually prohibits it: **API Skills have *no* network access**, claude.ai only variably, and external fetches are treated as a security risk. Therefore: **bundle the data + monthly version bump** is the robust approach. The scrape happens in the pipeline (with network access), not at Skill runtime.

---

## 6. Distribution to the Department — The Real Bottleneck

Distribution and updates are **the same question**; the monthly cadence makes it acute:

| Path | Distribution | Monthly update | Suitability |
|---|---|---|---|
| **API / thin backend** | centrally via your integration endpoint | fully automatic ("latest") | **Best solution** when central & always-current is the goal |
| **claude.ai (ZIP per user)** | each user uploads themselves | manual, per user → untenable | demo/fallback only |
| **Claude Code (plugin/git)** | plugin install / `git pull` | automatable | technical users only |

**Key point for the next professor conversation:** "Fresh data **every month without effort for users**" is only realistic via the **API (or a plugin)** — **not** via manually uploaded claude.ai ZIPs. The API path does, however, mean there needs to be a **small hosted component** again (through which the Messages API is called with `container.skills`). This slightly relativises "forget the UI entirely" — the large web stack becomes a thin backend, but a fully central, automatically-updated solution cannot be zero-server.

---

## 7. Other LLM Platforms (OpenAI, Gemini, DeepSeek)

**The Skill format is an Anthropic mechanism.** ChatGPT, Gemini, and DeepSeek **do not read `SKILL.md`** and have no concept of progressive disclosure or the code-execution VM. There is therefore **no** "same Skill, optimised per LLM" — you are **not** building four parallel Skill variants.

**The content is portable; the mechanism is not.** Your curated Markdown files (the researcher database) and the instruction texts are plain Markdown and can be reused. Per-platform equivalents:

- **OpenAI:** "Custom GPT" with uploaded files + File Search (RAG over the same MD collection). Closest to the Skill experience.
- **Gemini:** "Gem" or system prompt + file grounding over the same files.
- **DeepSeek:** No native Custom-GPT/Skill equivalent → needs a **custom RAG backend** (system prompt + retrieval over the MD database).
- **Generic & platform-agnostic:** System prompt + RAG over the MD collection — works with any sufficiently capable LLM, but is the most custom-built option.

**Recommendation:** Build the Skill **for Claude** (that's where the mechanism works best out of the box) and **keep data/instructions cleanly separated from the mechanism**, so the content can be re-packaged for other LLMs if needed. Do not pre-build multiple implementations speculatively.

---

## 8. Pros and Cons

### Pros

- **Security blockers disappear.** No hosted backend (or only a very thin one) → the WebSocket-JWT-in-URL problem from [technical_roadmap.md](technical_roadmap.md) largely goes away.
- **Hennig's stability concern is defused.** A Skill is a set of files, not a running web app that falls apart when the student HiWis leave. Significantly more long-lived.
- **Massive simplification.** Postgres, pgvector, Celery, Redis, Ollama hosting, and the React UI are largely gone. With a few hundred researchers, Claude reads and reasons over the MD files directly — no embedding infrastructure needed.
- **Deterministic GPA.** Executed as a bundled script → no temperature noise (fixes idea 10).
- **Low maintenance for professors.** Upkeep = periodic dev pipeline run, **no professor needs to do anything** — exactly what the product positioning calls for.

### Cons

- **Less UX control.** You ride the chat client; no custom guided interface.
- **Self-serve distribution** (on claude.ai), no true org-wide rollout.
- **Access barrier.** claude.ai Skills require a paid subscription (Pro/Max/Team/Enterprise) **with code execution enabled** — not available on the free tier.
- **Platform lock-in to Claude** for the native experience (see §7).
- **A backend is still needed** once you want it to be central and automatically updated (API path).

---

## 9. Critical Points & External Dependencies

What you need "externally" and must keep track of:

- **Anthropic API key** — for the automated Skill version uploads and (on the API path) for Messages API calls with `container.skills`. Must be stored as a **GitHub Actions secret**, never in the repo.
- **OpenAlex access for scraping** — generally usable without a key, but respect **rate limits / "polite pool"** (mail header). Uncritical for monthly batches.
- **GitHub Actions secrets management** — all tokens there, plus someone who keeps the cron job running.
- **30 MB upload limit** of the Skills API — uncritical for pure MD research descriptions, but keep an eye on it (don't bundle large binaries).
- **Beta headers / code execution** — using Skills via the API requires current beta flags (code execution, Skills, Files API); these can change.
- **Operational responsibility after 2026-07-01** — who keeps the pipeline, API key, and (possibly) the thin backend running? Exactly the unanswered Hennig question; clarify before any departmental listing.
- **Privacy.** Agent Skills are **not ZDR-capable** (Zero Data Retention) — data is stored under standard policy. **Student transcript/GPA data** should be processed locally and must **not** end up in the shared bundled database.
- **Security.** Skills from trusted sources only; external runtime fetches are explicitly risky (another reason to bundle data rather than fetch at runtime).

---

## 10. Recommendation & Open Decision

The professor's direction is good — it significantly simplifies the stack and defuses security and longevity problems. **We only need one Skill for the whole thing.**

**The single decision that determines everything else is platform/distribution:**

- For **"central + automatically updated every month"**, there is no way around an **API-based approach (or a plugin)** — with a thin backend and automated version uploads from GitHub Actions.
- The **claude.ai ZIP path** is only useful as a demo/fallback, because the monthly update affects every user manually.

**Concrete question to clarify with the professor next:** Should "provide to the department" mean central & automatically current (→ API/plugin + thin backend, some operational overhead) or is "students load the Skill themselves" good enough (→ claude.ai ZIP, but monthly updates are only practical quarterly/manually)? This answer determines architecture, distribution, and the update story simultaneously.
