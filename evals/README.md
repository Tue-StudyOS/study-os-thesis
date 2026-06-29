# Skill Evaluations — Thesis-Finder Quality & Behavior

This directory contains SVG visualizations of the thesis-finder skill suite's quality properties and behavioral validation.

## Files Overview

### 1. **quality-matrix.svg**
Skill frontmatter and code-quality properties, verified directly from SKILL.md files without API calls.

**Columns:**
- **Frontmatter**: YAML frontmatter is valid and complete
- **Use-when**: Invocation pattern is documented and clear
- **Description**: Description is concise (≤1024 chars) for agent discovery
- **Ref Files**: Skill references external documentation files
- **No Broken Links**: All referenced files exist and are accessible
- **No-DB Rule**: Skill follows the no-database pivot (live data sourcing or static reference only)
- **Evidence Rules**: Skill documents where outputs come from (citation trail)

**Legend:**
- ✓ = Property verified
- ✗ = Property missing (blocker)
- — = Not applicable (meta/router skills exempt)

**Interpretation:** A skill is production-ready when most columns are ✓. The "Evidence rules" column ensures traceability; exempt skills don't make factual claims requiring attribution.

---

### 2. **behavior-comparison.svg**
Pre-written fixture conversations comparing skill performance vs. a naive baseline across 4 university faculties.

**What it measures:**
- **Turns**: Number of conversation steps (user input + assistant output combined)
- **Finds Chairs**: Whether the skill output contains correctly-named thesis advisors
- **Match Rate**: How many ground-truth chairs are correctly identified (last-name based matching)

**Reading the comparison:**
- Skill runs in 8 conversation turns, baseline runs in 6 turns
- Skill consistently finds chairs (✓ yes); baseline finds none (✗ no)
- Match rates show actual chair recovery: skill recovers 5-7 of 6-7 ground-truth chairs per faculty
- This validates the behavioral contract: thesis-finder enables accurate discovery

**Why fixture conversations?**
- Pre-written, deterministic, reproducible
- Tests intended behavior (not live LLM variance)
- Fast to run, no external API costs
- Focused on the single most important output: did the skill name correct chairs?

---

### 3. **skill-architecture.svg**
Architecture diagram showing the skill invocation graph and data-access strategy for the thesis-discovery journey.

**The four stages:**

1. **① PROFILE** (`build-student-profile`)
   - Entry point: interviews student to build rich profile (6 dimensions)
   - Stores: interests, constraints, thesis style, methods, domain, timeline
   - Output: structured student context for all downstream skills

2. **② ROUTE** (`thesis-finder`)
   - Router skill: decides whether to search university or industry or both
   - Reads: student profile
   - Output: routing decision + invitation to discovery skills

3. **③ DISCOVER**
   - **University track** (`find-university-chairs`): live web search of university faculty
   - **Industry track** (`find-company-thesis-options`): live web search of company R&D / thesis programs
   - Both use parameterized search strategies tuned per faculty/sector
   - Reference files: `faculty-backbone.md`, `company-backbone.md`, search strategies

4. **④ CONTACT** (`draft-thesis-contact`)
   - Drafts personalized cold-outreach emails
   - Inputs: discovered chair profiles + student profile
   - Output: concise, high-signal first contact

**Key design principle:**
- All data is sourced at runtime (live web search)
- No cached databases or pre-scraped backbones
- Always current; simpler maintenance; no staleness risk

---

## How to Interpret Results

### If you're reviewing skill quality:
1. Open **quality-matrix.svg**
2. Check each skill has ✓ on Frontmatter, Use-when, Description
3. For discovery skills, verify No-DB and Evidence rules are ✓

### If you're testing behavior:
1. Open **behavior-comparison.svg**
2. Run the fixture conversations (in `findings/no_db_universal_skill/fixtures/`)
3. Check: does your skill output match or exceed the ✓ yes results and match rates?

### If you're onboarding or understanding the architecture:
1. Open **skill-architecture.svg**
2. Trace a student's journey: profile → route → discover (uni or industry) → contact
3. Note: all external data is fetched at runtime; no databases are cached

---

## Fixture Conversations

Fixture conversations are located at:
```
findings/no_db_universal_skill/fixtures/
```

Each fixture contains:
- Pre-written student profile (6-dimensional)
- Pre-written conversation turns
- Expected behavioral output (skill should find chairs)
- Ground-truth chair names for matching

Fixtures are **not live measurements**—they test the intended behavioral contract. Use them to validate that changes to skills don't break the core discovery flow.

---

## Measurement Notes

- **Quality properties** are checked on every commit (no API call)
- **Behavioral fixtures** are pre-written, deterministic, reproducible
- **Match rates** use last-name string matching against ground-truth
- **No-DB rule** is enforced: all data flows are live-sourced or static-reference only

These evaluations measure the thesis-finder's ability to deliver on its core promise: help students find thesis advisors accurately and efficiently.
