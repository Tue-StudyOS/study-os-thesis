# Skill Computation System — Technical Design & Implementation Plan

> **Status:** Pre-implementation
> **Branch:** `feat/skill_computation` (rebased on `architecture_refactoring`)
> **Date:** 2026-06-04

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current Dummy-Skill Replacement Strategy](#2-current-dummy-skill-replacement-strategy)
3. [System Architecture](#3-system-architecture)
4. [Core Domain Models](#4-core-domain-models)
5. [Database Schema & Migrations](#5-database-schema--migrations)
6. [Interfaces & Protocols](#6-interfaces--protocols)
7. [Transcript Parsing Pipeline](#7-transcript-parsing-pipeline)
8. [Module Handbook Ingestion & Versioning](#8-module-handbook-ingestion--versioning)
9. [Module Matching Strategy](#9-module-matching-strategy)
10. [Skill Tag Generation & Normalization](#10-skill-tag-generation--normalization)
11. [Skill Scoring Formula](#11-skill-scoring-formula)
12. [Agent Tool Design](#12-agent-tool-design)
13. [Upload-to-Computation Orchestration Flow](#13-upload-to-computation-orchestration-flow)
14. [Representative Code Snippets](#14-representative-code-snippets)
15. [Error Handling & Edge Cases](#15-error-handling--edge-cases)
16. [Testing Strategy](#16-testing-strategy)
17. [Observability & Logging](#17-observability--logging)
18. [MVP Implementation Plan](#18-mvp-implementation-plan)
19. [Future Extension Roadmap](#19-future-extension-roadmap)
20. [Risks & Tradeoffs](#20-risks--tradeoffs)
21. [Appendix: New File Structure](#21-appendix-new-file-structure)

---

## 1. Executive Summary

Replace the **frontend-only keyword heuristic** in `SkillRadar.tsx` (6 hardcoded axes, keyword
matching against course names) with a **backend-driven skill computation pipeline** that:

1. Takes parsed transcript courses already extracted by the existing LLM pipeline
2. Matches them against a **module handbook** (new data source, ingested via Docling PDF parsing)
3. Uses an LLM to **generate normalized skill tags** from handbook content
4. Computes **weighted skill scores** using ECTS, grades, relevance, level, recency, and match confidence
5. Persists results with full evidence and explainability
6. Exposes skills via a new `GET /api/students/me/skills` endpoint consumed by the frontend
7. Injects the computed skill profile into the **chat agent context** for better thesis recommendations

The pipeline runs as a **Celery task** (using the `architecture_refactoring` worker infrastructure)
triggered automatically after transcript parsing completes. The frontend becomes a pure display
layer — it fetches structured skill data from the API instead of computing it client-side.

---

## 2. Current Dummy-Skill Replacement Strategy

### What exists today

| Component | Location | Problem |
|---|---|---|
| `SkillRadar.tsx` | `frontend/src/components/SkillRadar.tsx:31-136` | 6 fixed axes, `AXIS_KEYWORDS` keyword matching, `gradeToScore()` — **all client-side heuristics** |
| `Dashboard.tsx` | `frontend/src/pages/Dashboard.tsx:71-82` | Calls `coursesToRadarData()`, derives percent bars — **no backend involvement** |
| `TARGET_DATA` | `SkillRadar.tsx:140` | `[3.5, 3.5, 3.0, 3.5, 2.5, 3.0]` — hardcoded fixed target profile |
| Backend | — | **No skill computation whatsoever.** `skills_required` on theses is a separate concept. |

### What gets replaced

| Symbol | Action |
|---|---|
| `AXIS_KEYWORDS` (SkillRadar.tsx:31-96) | **Deleted** — skill-to-course mapping moves to backend |
| `gradeToScore()` (SkillRadar.tsx:99-106) | **Deleted** — grade weighting moves to `skills/scorer.py` |
| `coursesToRadarData()` (SkillRadar.tsx:109-137) | **Deleted** — replaced by `GET /api/students/me/skills` |
| `SKILL_BAR_AXES` (Dashboard.tsx:10-17) | **Deleted** — axes are now dynamic from the API response |
| `TARGET_DATA` (SkillRadar.tsx:140) | **Replaced** — optional configurable target passed as a prop |

### What stays

| Component | Status |
|---|---|
| `SkillRadar.tsx` SVG rendering (polar coordinates, polygons, grid) | **Kept** — visualization becomes data-driven |
| `SkillBar.tsx` presentation component | **Unchanged** — receives computed data from parent |
| Transcript upload pipeline | **Extended** — triggers skill computation on success |

---

## 3. System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                          Frontend                                 │
│  Dashboard.tsx ──► GET /api/students/me/skills ──► SkillRadar    │
│                                                     SkillBar     │
└──────────────────────────┬───────────────────────────────────────┘
                           │ HTTP / WebSocket
┌──────────────────────────▼───────────────────────────────────────┐
│                      API Layer (FastAPI)                          │
│                                                                  │
│  POST /me/transcript ──► [202] dispatch parse_transcript         │
│                                       │ on success               │
│                                       ▼                          │
│                               dispatch compute_skills            │
│                                                                  │
│  GET  /me/skills         ──► SkillRepository.get_profile()       │
│  POST /me/skills/recompute ► dispatch compute_skills (manual)    │
│  POST /admin/handbook    ──► dispatch ingest_handbook            │
└──────────────────────────────────────┬───────────────────────────┘
                                       │ Celery tasks
┌──────────────────────────────────────▼───────────────────────────┐
│                    Worker Domain (Celery + Redis)                 │
│                                                                  │
│  skills/tasks.py     compute_skills                              │
│  handbook/tasks.py   ingest_handbook                             │
│                                                                  │
│  Both use execute_task() from worker/task_runner.py              │
└──────────────────────────────────────┬───────────────────────────┘
                                       │
┌──────────────────────────────────────▼───────────────────────────┐
│               Skill & Handbook Domain Services (NEW)             │
│                                                                  │
│  skills/                                                         │
│    service.py      ─ SkillComputationService (orchestrator)      │
│    scorer.py       ─ pure scoring functions                      │
│    matcher.py      ─ CascadeModuleMatcher                        │
│    tag_generator.py─ LLMSkillTagGenerator (cached per entry)     │
│    taxonomy.py     ─ SkillTaxonomy (normalize, get_or_create)    │
│    repository.py   ─ user_skills, skill_evidence, runs           │
│    controller.py   ─ /me/skills, /me/skills/recompute            │
│    ports.py        ─ Protocol interfaces                         │
│                                                                  │
│  handbook/                                                       │
│    parser.py       ─ DoclingHandbookParser                       │
│    service.py      ─ HandbookService (ingestion orchestrator)    │
│    repository.py   ─ module_handbook_entries, mappings           │
│    controller.py   ─ /admin/handbook CRUD                        │
└──────────────────────────────────────┬───────────────────────────┘
                                       │ SQLAlchemy async
┌──────────────────────────────────────▼───────────────────────────┐
│               PostgreSQL + pgvector (existing)                    │
│                                                                  │
│  NEW TABLES:                                                     │
│    module_handbook_entries   ─ authoritative module data         │
│    skill_tags               ─ normalized canonical taxonomy      │
│    module_skill_mappings    ─ entry ↔ skill tag + relevance      │
│    user_skills              ─ computed scores per user           │
│    skill_evidence           ─ per-module explanation rows        │
│    skill_computation_runs   ─ audit log                          │
└──────────────────────────────────────────────────────────────────┘
```

### Key design decisions

- **Celery-first**: all heavy computation runs as Celery tasks via the `architecture_refactoring`
  worker infrastructure. No long-running work inside FastAPI request handlers.
- **Docling for PDF parsing**: handbook PDFs are parsed with IBM Docling which preserves
  hierarchical document structure (headings, sections, tables).
- **LLM only where deterministic logic is insufficient**: module matching uses a cascade of
  deterministic methods; the LLM is only called for tag generation and ambiguous field extraction.
- **Dynamic radar axes**: the frontend shows the user's top N skills by score. Axes are not fixed.
- **Full evidence trail**: every skill score is explainable down to individual module contributions.
- **Idempotent computation**: re-running on the same transcript replaces all previous skill data
  atomically, never duplicating rows.

---

## 4. Core Domain Models

### 4.1 ModuleHandbookEntry

One module from a university module handbook (the authoritative source).

```python
class ModuleHandbookEntry(Base):
    __tablename__ = "module_handbook_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    university_id: Mapped[str] = mapped_column(String(50), nullable=False)
    handbook_version: Mapped[str] = mapped_column(String(50), nullable=False)
    module_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    module_title: Mapped[str] = mapped_column(String(500), nullable=False)
    module_title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    learning_outcomes: Mapped[str | None] = mapped_column(Text, nullable=True)
    contents: Mapped[str | None] = mapped_column(Text, nullable=True)
    prerequisites: Mapped[str | None] = mapped_column(Text, nullable=True)
    ects: Mapped[float | None] = mapped_column(Numeric(4, 1), nullable=True)
    level: Mapped[str | None] = mapped_column(String(20), nullable=True)  # bachelor/master/phd
    language: Mapped[str | None] = mapped_column(String(10), nullable=True)  # de/en
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    skill_mappings: Mapped[list["ModuleSkillMapping"]] = relationship(
        back_populates="handbook_entry", cascade="all, delete-orphan"
    )
```

UNIQUE constraint: `(university_id, handbook_version, module_code)` where `module_code IS NOT NULL`.

### 4.2 SkillTag — Canonical Taxonomy

```python
class SkillTag(Base):
    __tablename__ = "skill_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)  # canonical lowercase
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # e.g. ["ML", "maschinelles lernen", "statistical learning"]
    aliases: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

**Categories**: `programming`, `mathematics`, `theory`, `systems`, `data`, `engineering`,
`research`, `other`.

### 4.3 ModuleSkillMapping

Links a handbook entry to its skill tags with relevance scores. Cached LLM output.

```python
class ModuleSkillMapping(Base):
    __tablename__ = "module_skill_mappings"

    id: Mapped[int] = mapped_column(primary_key=True)
    handbook_entry_id: Mapped[int] = mapped_column(
        ForeignKey("module_handbook_entries.id", ondelete="CASCADE"), nullable=False
    )
    skill_tag_id: Mapped[int] = mapped_column(
        ForeignKey("skill_tags.id", ondelete="CASCADE"), nullable=False
    )
    relevance: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)  # 0.0-1.0
    source: Mapped[str] = mapped_column(String(30), nullable=False)  # "llm_generated" | "manual"
    llm_prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    llm_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    llm_input_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)  # SHA-256
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    handbook_entry: Mapped["ModuleHandbookEntry"] = relationship(back_populates="skill_mappings")
    skill_tag: Mapped["SkillTag"] = relationship()
```

UNIQUE constraint: `(handbook_entry_id, skill_tag_id)`.

### 4.4 UserSkill

A user's computed score for one canonical skill.

```python
class UserSkill(Base):
    __tablename__ = "user_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    skill_tag_id: Mapped[int] = mapped_column(
        ForeignKey("skill_tags.id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)  # 0.0-1.0
    computation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("skill_computation_runs.id"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    skill_tag: Mapped["SkillTag"] = relationship()
    evidence: Mapped[list["SkillEvidence"]] = relationship(
        back_populates="user_skill", cascade="all, delete-orphan"
    )
```

UNIQUE constraint: `(user_id, skill_tag_id)`.

### 4.5 SkillEvidence

Explains why a user received a specific skill score. One row per (user_skill, contributing course).

```python
class SkillEvidence(Base):
    __tablename__ = "skill_evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_skill_id: Mapped[int] = mapped_column(
        ForeignKey("user_skills.id", ondelete="CASCADE"), nullable=False
    )
    student_course_id: Mapped[int] = mapped_column(
        ForeignKey("student_courses.id", ondelete="CASCADE"), nullable=False
    )
    handbook_entry_id: Mapped[int | None] = mapped_column(
        ForeignKey("module_handbook_entries.id", ondelete="SET NULL"), nullable=True
    )
    match_method: Mapped[str] = mapped_column(String(30), nullable=False)
    # "exact_code" | "title_exact" | "title_fuzzy" | "semantic"
    match_confidence: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    module_skill_relevance: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    credits_used: Mapped[float | None] = mapped_column(Numeric(4, 1), nullable=True)
    grade_factor: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    level_factor: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    recency_factor: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    raw_contribution: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)
    computation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("skill_computation_runs.id"), nullable=False
    )

    user_skill: Mapped["UserSkill"] = relationship(back_populates="evidence")
```

### 4.6 SkillComputationRun — Audit Log

```python
class SkillComputationRun(Base):
    __tablename__ = "skill_computation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    handbook_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    university_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    total_courses: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    matched_courses: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    unmatched_courses: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    warnings: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # ScoringConfig snapshot
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

---

## 5. Database Schema & Migrations

One new Alembic migration (`00XX_skill_computation.py`) numbered after migration `0009` from
`architecture_refactoring`.

### Tables summary

| Table | Key indexes / constraints |
|---|---|
| `module_handbook_entries` | UNIQUE `(university_id, handbook_version, module_code)` when code not null; GIN on `module_title` for text search |
| `skill_tags` | UNIQUE on `name`; GIN on `aliases` for JSONB containment |
| `module_skill_mappings` | UNIQUE `(handbook_entry_id, skill_tag_id)`; index on `skill_tag_id` |
| `user_skills` | UNIQUE `(user_id, skill_tag_id)`; index on `computation_run_id` |
| `skill_evidence` | Index on `user_skill_id`; index on `computation_run_id` |
| `skill_computation_runs` | Index on `user_id`; index on `job_id` |

### Enum extension

```sql
ALTER TYPE job_type ADD VALUE IF NOT EXISTS 'compute_skills';
ALTER TYPE job_type ADD VALUE IF NOT EXISTS 'ingest_handbook';
```

### Taxonomy seed

The migration also inserts ~70 common CS/engineering `skill_tags` rows with canonical names,
categories, and aliases (see Section 10.3).

---

## 6. Interfaces & Protocols

Following the existing `LLMPort` pattern (structural subtyping via `typing.Protocol`, no
inheritance required):

```python
# skills/ports.py

class ModuleMatcher(Protocol):
    async def match(
        self,
        course: StudentCourse,
        handbook_entries: list[ModuleHandbookEntry],
    ) -> list[ModuleMatch]: ...

class SkillTagGenerator(Protocol):
    async def generate_tags(
        self, entry: ModuleHandbookEntry
    ) -> list[GeneratedSkillTag]: ...

class SkillScorer(Protocol):
    def compute(
        self,
        matched_modules: list[MatchedModule],
        config: ScoringConfig,
    ) -> list[ComputedSkill]: ...

class HandbookParser(Protocol):
    async def parse(
        self,
        document_bytes: bytes,
        university_id: str,
        handbook_version: str,
    ) -> list[HandbookEntryData]: ...

class SkillTaxonomyPort(Protocol):
    async def normalize(self, raw_tag: str) -> str: ...
    async def get_or_create(self, raw_tag: str, category: str | None) -> SkillTag: ...
```

### Intermediate data transfer objects

```python
@dataclass
class ModuleMatch:
    handbook_entry: ModuleHandbookEntry
    method: str        # "exact_code" | "title_exact" | "title_fuzzy" | "semantic"
    confidence: float  # 0.0-1.0

@dataclass
class GeneratedSkillTag:
    tag: str           # raw tag from LLM (will be normalized)
    relevance: float   # 0.0-1.0
    category: str      # one of the 8 categories

@dataclass
class MatchedModule:
    course: StudentCourse
    handbook_entry: ModuleHandbookEntry | None
    match: ModuleMatch | None
    skill_mappings: list[ModuleSkillMapping]

@dataclass
class ComputedSkill:
    skill_tag_id: int
    score: float
    evidence: list[EvidenceItem]

@dataclass(frozen=True)
class ScoringConfig:
    default_ects: float = 5.0
    default_grade_factor: float = 0.5
    pass_grade_factor: float = 0.6
    level_weights: dict[str, float] = field(default_factory=lambda: {
        "bachelor": 0.6, "master": 0.85, "phd": 1.0, "unknown": 0.7,
    })
    recency_decay_per_year: float = 0.05
    recency_floor: float = 0.5
    recency_default: float = 0.75
    min_match_confidence: float = 0.5
```

---

## 7. Transcript Parsing Pipeline

**No changes to the existing pipeline.** `students/service.py` already handles:

1. PDF text extraction via `pdfplumber`
2. LLM structured JSON extraction of courses
3. GPA computation
4. Profile embedding
5. DB persistence into `student_courses`

Skill computation is **chained after** this pipeline succeeds (see Section 13).

---

## 8. Module Handbook Ingestion & Versioning

### 8.1 Parsing with Docling

[IBM Docling](https://github.com/docling-project/docling) (v2.97+) is added as a dependency in
`pyproject.toml`. It parses the Modulhandbuch PDF into a hierarchical `DoclingDocument` that
preserves heading levels, sections, and tables — critical for detecting per-module boundaries.

```python
# handbook/parser.py

from docling.document_converter import DocumentConverter

class DoclingHandbookParser:
    """
    Two-phase parsing:
      Phase 1 (deterministic): Docling converts the PDF to a hierarchical document.
                               Heading patterns detect module boundaries.
      Phase 2 (LLM-assisted):  Ambiguous fields (ECTS from prose text, level
                               classification) are extracted via LLM per module chunk.
    """

    async def parse(
        self,
        document_bytes: bytes,
        university_id: str,
        handbook_version: str,
    ) -> list[HandbookEntryData]:
        # Phase 1: structural parsing (sync, run in thread pool)
        doc = await asyncio.get_event_loop().run_in_executor(
            None, self._convert_pdf, document_bytes
        )
        raw_modules = self._extract_module_sections(doc)

        # Phase 2: LLM-assisted field extraction
        entries = []
        for raw in raw_modules:
            entry = await self._extract_fields(raw)
            entry.university_id = university_id
            entry.handbook_version = handbook_version
            entries.append(entry)
        return entries

    def _convert_pdf(self, pdf_bytes: bytes):
        converter = DocumentConverter()
        return converter.convert_from_bytes(pdf_bytes).document

    def _extract_module_sections(self, doc) -> list[dict]:
        """Walk Docling's section tree to detect module boundaries.

        Module headings match patterns like:
          "IN0001 Einführung in die Informatik"
          "Module: Introduction to Computer Science"
        Sub-sections under each heading yield description, contents,
        learning outcomes, prerequisites, ECTS, etc.
        """
        ...

    async def _extract_fields(self, raw_section: dict) -> HandbookEntryData:
        """
        Structured sub-headings (Contents, Lernergebnisse, etc.) are matched
        deterministically. Remaining free-text fields use a compact LLM call
        to extract ECTS and level.
        """
        ...
```

### 8.2 Versioning

- All entries are keyed by `(university_id, handbook_version, module_code)`.
- Uploading a **new version** creates new rows; old rows remain (no deletion).
- Skill computation always uses the **latest version** for a given `university_id` by default.
- `module_skill_mappings` are per-entry, so they version naturally with their handbook.

### 8.3 LLM caching

LLM-generated skill tags are cached via `module_skill_mappings`:

- `llm_input_hash` = SHA-256 of the module content fields sent to the LLM.
- `llm_prompt_version` = a short constant (e.g. `"v1"`) bumped when the prompt changes.
- If a matching row exists for `(handbook_entry_id, llm_prompt_version, llm_input_hash)`,
  the LLM is skipped.

### 8.4 Admin ingestion flow

```
POST /api/admin/handbook (multipart: file, university_id, version)
  ↓
Create Job(type=ingest_handbook)
Store PDF bytes in Redis (same pattern as transcript pdf_store.py)
Dispatch ingest_handbook.delay()
Return {job_id} 202
  ↓
Celery worker:
  1. Docling parse → module sections
  2. LLM-assisted field extraction per module
  3. Persist ModuleHandbookEntry rows (upsert by module_code+version)
  4. For each new entry: generate skill tags via LLM
  5. Normalize tags via SkillTaxonomy.get_or_create()
  6. Persist ModuleSkillMapping rows
  7. Return {modules_ingested, tags_generated}
```

---

## 9. Module Matching Strategy

`CascadeModuleMatcher` tries methods in order, stopping at the first result that meets its
confidence threshold:

### Step 1 — Exact module code (confidence: 1.0)

```python
if course.module_code and entry.module_code:
    if course.module_code.strip().upper() == entry.module_code.strip().upper():
        return [ModuleMatch(entry, "exact_code", 1.0)]
```

> The current transcript prompt does not extract module codes. Extend
> `_TRANSCRIPT_PROMPT` in `students/service.py` to capture them when present.

### Step 2 — Normalized title exact match (confidence: 0.95)

```python
def _normalize(title: str) -> str:
    t = title.lower().strip()
    for de, en in [("ä","ae"),("ö","oe"),("ü","ue"),("ß","ss")]:
        t = t.replace(de, en)
    t = re.sub(r"\s*\([^)]*\)\s*", " ", t)  # strip "(IN0001)" etc.
    return re.sub(r"\s+", " ", t).strip()

if _normalize(course.course_name) == _normalize(entry.module_title):
    return [ModuleMatch(entry, "title_exact", 0.95)]
```

### Step 3 — Fuzzy title match via `rapidfuzz` (confidence: 0.70-0.90)

```python
from rapidfuzz import fuzz
ratio = fuzz.token_sort_ratio(_normalize(course.course_name), _normalize(entry.module_title))
if ratio >= 80:
    confidence = 0.70 + (ratio - 80) * 0.01  # 80→0.70, 100→0.90
    return [ModuleMatch(entry, "title_fuzzy", confidence)]
```

### Step 4 — Semantic match via embedding cosine similarity (confidence: 0.50-0.80)

Pre-compute and cache handbook title embeddings. At match time:

```python
sim = cosine_similarity(course_embedding, entry_title_embedding)
if sim >= 0.75:
    confidence = 0.50 + (sim - 0.75) * 1.2  # 0.75→0.50, 1.0→0.80
    return [ModuleMatch(entry, "semantic", confidence)]
```

### Unmatched courses

Courses with no match above `min_match_confidence` (default: 0.5) are:

- Excluded from scoring
- Recorded in `skill_computation_runs.unmatched_courses`
- Returned in the API response as `unmatched_courses`

---

## 10. Skill Tag Generation & Normalization

### 10.1 LLM prompt

```python
SKILL_GENERATION_PROMPT = """\
Given the following university module, extract 3-8 skill tags that describe
the competencies a student gains by completing it.

Module title: {title}
Description: {description}
Learning outcomes: {learning_outcomes}
Contents: {contents}
Prerequisites: {prerequisites}
ECTS: {ects}

Return a JSON array:
[
  {{"tag": "machine learning", "relevance": 0.9, "category": "theory"}}
]

Rules:
- Tags must be lowercase English canonical names.
- relevance is 0.0-1.0: how central this skill is to the module.
- category is one of: programming, mathematics, theory, systems, data, engineering, research.
- Prefer specific but not overly narrow tags.
  Good: "machine learning". Bad: "gradient descent for logistic regression".
- Do not include generic academic soft skills (critical thinking, teamwork, etc.).
- Return ONLY the JSON array, no markdown, no explanation.
"""
```

Output is validated with Pydantic before use:

```python
class _GeneratedTag(BaseModel):
    tag: str = Field(min_length=2, max_length=100)
    relevance: float = Field(ge=0.0, le=1.0)
    category: Literal[
        "programming","mathematics","theory","systems","data","engineering","research"
    ]
```

### 10.2 Normalization via SkillTaxonomy

```python
class SkillTaxonomy:
    async def normalize(self, raw_tag: str) -> str:
        lower = raw_tag.lower().strip()
        # 1. Exact name match in skill_tags.name
        # 2. Alias match via JSONB containment query on skill_tags.aliases
        # 3. Fuzzy match against all tag names (threshold >= 0.90 via rapidfuzz)
        # 4. No match → return as-is (new tag will be created)
        ...

    async def get_or_create(self, raw_tag: str, category: str | None = None) -> SkillTag:
        canonical = await self.normalize(raw_tag)
        tag = await self._find_by_name(canonical)
        if tag:
            return tag
        tag = SkillTag(name=canonical, category=category, aliases=[raw_tag.lower().strip()])
        self._session.add(tag)
        await self._session.flush()
        return tag
```

This resolves aliases like `"OS"` / `"operating systems"` / `"Betriebssysteme"` to one canonical
entry: `"operating systems"`.

### 10.3 Seed taxonomy

The migration seeds `skill_tags` with ~70 common CS/engineering skills, for example:

```python
SEED_SKILLS = [
    # (name, category, aliases)
    ("algorithms", "programming", ["algorithmen", "algorithm design", "algorithmik"]),
    ("data structures", "programming", ["datenstrukturen", "data structures and algorithms"]),
    ("machine learning", "theory", ["maschinelles lernen", "ml", "statistical learning"]),
    ("deep learning", "theory", ["deep learning", "neural networks", "neuronale netze"]),
    ("databases", "data", ["datenbanken", "datenbanksysteme", "sql", "nosql", "dbms"]),
    ("operating systems", "systems", ["betriebssysteme", "os", "betriebssystem"]),
    ("computer networks", "systems", ["rechnernetze", "netzwerke", "networking", "networks"]),
    ("software engineering", "engineering", ["softwaretechnik", "se", "software development"]),
    ("statistics", "mathematics", ["statistik", "statistical methods", "stochastik"]),
    ("linear algebra", "mathematics", ["lineare algebra", "la"]),
    ("calculus", "mathematics", ["analysis", "differential calculus"]),
    ("computer architecture", "systems", ["rechnerarchitektur", "computer organization"]),
    ("programming languages", "programming", ["programmiersprachen", "compilers"]),
    ("distributed systems", "systems", ["verteilte systeme", "distributed computing"]),
    ("cryptography", "systems", ["kryptographie", "it-sicherheit", "security"]),
    ("computer vision", "theory", ["bildverarbeitung", "cv", "image processing"]),
    ("natural language processing", "theory", ["nlp", "sprachverarbeitung"]),
    ("robotics", "engineering", ["robotik"]),
    ("parallel computing", "systems", ["parallele systeme", "gpu computing"]),
    ("software testing", "engineering", ["softwarequalität", "testen", "qa"]),
    ("agile methods", "engineering", ["agile", "scrum", "softwareprozess"]),
    ("optimization", "mathematics", ["optimierung", "mathematical optimization"]),
    ("information retrieval", "data", ["informationsretrieval", "ir", "search"]),
    ("data engineering", "data", ["data pipelines", "etl", "data warehouse"]),
    ("cloud computing", "systems", ["cloud", "aws", "azure"]),
    # ... ~45 more
]
```

This set grows organically as new modules are processed.

---

## 11. Skill Scoring Formula

### Formula

For each skill `S`, iterating over all completed modules `m` matched to `S`:

```
             Σ_m [ W(m) · G(m) · R(m,S) · L(m) · T(m) · C(m) ]
score(S) =  ──────────────────────────────────────────────────────
                           normalization_divisor

normalization_divisor = max( Σ_m [ W(m) · C(m) ] , 1.0 )
```

### Factor definitions

| Factor | Symbol | Formula | Range |
|---|---|---|---|
| Credits weight | `W(m)` | `ects / max_ects_in_transcript` | 0.0 – 1.0 |
| Grade factor | `G(m)` | German numeric: `(5.0 − grade) / 4.0`; "bestanden": 0.6; missing: 0.5 | 0.0 – 1.0 |
| Skill relevance | `R(m,S)` | `module_skill_mappings.relevance` | 0.0 – 1.0 |
| Level factor | `L(m)` | bachelor: 0.6, master: 0.85, phd: 1.0, unknown: 0.7 | 0.6 – 1.0 |
| Recency factor | `T(m)` | `max(0.5, 1.0 − 0.05 × years_ago)`; missing semester: 0.75 | 0.5 – 1.0 |
| Match confidence | `C(m)` | From `ModuleMatch.confidence` | 0.0 – 1.0 |

A score of **1.0** means every module mapped to skill `S` was completed with grade 1.0 at master
level recently with perfect match confidence.

### Failed/non-passed modules

- Grade `"5.0"` or `"nicht bestanden"` → `G(m) = 0.0` → zero contribution (effectively excluded).
- `"bestanden"` → `G(m) = 0.6` (partial credit for ungraded passes).

### Configuration

All weight parameters are stored in a frozen `ScoringConfig` dataclass and persisted in
`skill_computation_runs.config` so every run is reproducible and auditable.

---

## 12. Agent Tool Design

### 12.1 Inject skills into chat context

Extend `ChatService._build_student_context()` to include computed skill scores:

```python
# In chat/service.py:

async def _build_student_context(self, user_id: int) -> str | None:
    # ... existing course loading (unchanged) ...

    # NEW: append top computed skills
    if self._skill_repo is not None:
        skills = await self._skill_repo.get_top_user_skills(user_id, limit=15)
        if skills:
            lines.append("\n## Computed skill profile (score 0.0–1.0)")
            for s in skills:
                lines.append(f"  - {s.skill_tag.name} ({s.skill_tag.category}): {s.score:.0%}")

    return "\n".join(lines)
```

The agent can now reason about the student's strongest areas when running `search_chairs`,
`search_theses`, and `generate_proposal`.

### 12.2 Optional: `compute_user_skills` chat tool

For manual re-computation via conversation (e.g. "please refresh my skill profile"):

```python
{
    "type": "function",
    "function": {
        "name": "compute_user_skills",
        "description": (
            "Recompute the student's skill profile from their transcript and module handbook. "
            "Call this only when the student explicitly asks to refresh or recompute their skills."
        ),
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
}
```

The tool implementation dispatches `compute_skills.delay()` and returns the new job ID.

---

## 13. Upload-to-Computation Orchestration Flow

```
User uploads PDF transcript
        │
        ▼
POST /api/students/me/transcript
  Create Job(type=parse_transcript)
  Store PDF in Redis (pdf_store.py)
  parse_transcript.delay(user_id, job_id)
  ← 202 {job_id}
        │
        ▼ (Celery worker)
parse_transcript task
  ├─ Extract PDF text (pdfplumber)
  ├─ LLM extraction → courses
  ├─ GPA computation
  ├─ Profile embedding
  ├─ Persist to student_courses
  └─ ON SUCCESS ──────────────────────────────────────────────────┐
                                                                   │
                                                                   ▼
                                              Create Job(type=compute_skills)
                                              compute_skills.delay(user_id, skill_job_id)
                                                                   │
                                                                   ▼
                                              compute_skills task
                                                ├─ Load student_courses
                                                ├─ Load module_handbook_entries (latest)
                                                ├─ CascadeModuleMatcher per course
                                                ├─ _ensure_skill_mappings() per entry
                                                │    (load cached or generate via LLM)
                                                ├─ SkillScorer.compute()
                                                ├─ SkillRepository.replace_user_skills()
                                                │    (DELETE old + INSERT new, atomic)
                                                └─ Record SkillComputationRun
                                                                   │
                                                                   ▼
                                              WebSocket: "skills_computed" event
                                                                   │
                                                                   ▼
                                              Frontend: GET /api/students/me/skills
                                                        → render SkillRadar + SkillBars
```

### Chaining implementation

In `students/tasks.py`, at the end of `_parse_transcript_work()`:

```python
# After student is persisted, chain skill computation
from app.skills.tasks import compute_skills as _compute_skills_task

async with SessionLocal() as session:
    job_svc = JobService(JobRepository(session))
    skill_job = await job_svc.create_job(
        type=JobType.compute_skills,
        user_id=user_id,
        input_data={"triggered_by_job": job_id},
    )
    await session.commit()

_compute_skills_task.delay(user_id=user_id, job_id=str(skill_job.id))
return {"user_id": user_id, "courses": len(student.courses), "skill_job_id": str(skill_job.id)}
```

---

## 14. Representative Code Snippets

### Scoring (pure functions)

```python
# skills/scorer.py

def compute_skill_scores(
    matched_modules: list[MatchedModule],
    config: ScoringConfig,
) -> list[ComputedSkill]:
    """Pure function: no I/O, no LLM calls."""
    if not matched_modules:
        return []

    max_ects = max(
        (float(m.course.credits or config.default_ects) for m in matched_modules),
        default=config.default_ects,
    )

    skill_evidence: dict[int, list[EvidenceItem]] = defaultdict(list)

    for mm in matched_modules:
        if mm.match is None or mm.match.confidence < config.min_match_confidence:
            continue

        ects = float(mm.course.credits or config.default_ects)
        credits_w = ects / max_ects
        grade_f = _grade_factor(mm.course.grade, config)
        level = (mm.handbook_entry.level or "unknown") if mm.handbook_entry else "unknown"
        level_f = config.level_weights.get(level, config.level_weights["unknown"])
        recency_f = _recency_factor(mm.course.semester_taken, config)
        conf = mm.match.confidence

        for mapping in mm.skill_mappings:
            contribution = credits_w * grade_f * float(mapping.relevance) * level_f * recency_f * conf
            skill_evidence[mapping.skill_tag_id].append(EvidenceItem(
                student_course_id=mm.course.id,
                handbook_entry_id=mm.handbook_entry.id if mm.handbook_entry else None,
                match_method=mm.match.method,
                match_confidence=conf,
                module_skill_relevance=float(mapping.relevance),
                credits_used=ects,
                grade_factor=grade_f,
                level_factor=level_f,
                recency_factor=recency_f,
                raw_contribution=contribution,
            ))

    results = []
    for skill_tag_id, items in skill_evidence.items():
        numerator = sum(i.raw_contribution for i in items)
        denominator = max(
            sum((i.credits_used or config.default_ects) / max_ects * i.match_confidence
                for i in items),
            1.0,
        )
        score = min(1.0, numerator / denominator)
        results.append(ComputedSkill(skill_tag_id=skill_tag_id, score=score, evidence=items))

    return sorted(results, key=lambda s: s.score, reverse=True)
```

### Celery task

```python
# skills/tasks.py

@celery_app.task(
    bind=True,
    name="app.skills.tasks.compute_skills",
    max_retries=2,
    default_retry_delay=60,
    soft_time_limit=300,
    time_limit=360,
)
def compute_skills(self, user_id: int, job_id: str) -> dict:
    from app.config import get_settings
    settings = get_settings()
    logger.info("compute_skills: user_id=%d job_id=%s", user_id, job_id)
    return execute_task(
        self,
        job_id=job_id,
        user_id=user_id,
        redis_url=settings.redis_url,
        work=lambda: _compute_skills_work(user_id, job_id, settings),
        success_event="skills_computed",
        started_event="skills_computing",
    )


async def _compute_skills_work(user_id: int, job_id: str, settings) -> dict:
    from app.db import SessionLocal
    from app.llm.factory import build_chat_client, build_embed_client
    from app.skills.service import SkillComputationService
    # ... build all dependencies ...

    async with SessionLocal() as session:
        run = SkillComputationRun(user_id=user_id, job_id=uuid.UUID(job_id), status="running")
        session.add(run)
        await session.flush()

        service = SkillComputationService(...)
        result = await service.compute_skills(user_id, run.id)
        await session.commit()

    return {
        "computation_run_id": str(result.computation_run_id),
        "skills_count": len(result.skills),
        "matched_courses": result.matched_courses,
        "unmatched_courses": result.unmatched_courses,
        "warnings": result.warnings,
    }
```

### API endpoint

```python
# skills/controller.py

router = APIRouter(prefix="/api/students", tags=["skills"])

@router.get("/me/skills", response_model=UserSkillProfileOut)
async def get_my_skills(
    current_user: CurrentUserDep,
    skill_service: SkillServiceDep,
) -> object:
    """Return the current user's computed skill profile."""
    return await skill_service.get_user_skill_profile(current_user.id)


@router.post("/me/skills/recompute", status_code=status.HTTP_202_ACCEPTED)
async def recompute_skills(
    current_user: CurrentUserDep,
    job_service: JobServiceDep,
) -> dict:
    """Manually trigger skill re-computation (idempotent)."""
    job = await job_service.create_job(
        type=JobType.compute_skills,
        user_id=current_user.id,
    )
    task = compute_skills.delay(user_id=current_user.id, job_id=str(job.id))
    await job_service.set_celery_task_id(job.id, task.id)
    return {"job_id": str(job.id)}
```

### Response schema

```python
# skills/schemas.py

class SkillEvidenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    course_name: str
    credits: float | None
    grade: str | None
    handbook_module: str | None
    match_method: str
    match_confidence: float
    contribution: float

class UserSkillItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    skill: str             # canonical name, e.g. "machine learning"
    category: str | None
    score: float           # 0.0-1.0
    evidence: list[SkillEvidenceOut]

class UserSkillProfileOut(BaseModel):
    user_id: int
    computation_run_id: str | None
    computed_at: datetime | None
    skills: list[UserSkillItemOut]   # sorted by score descending
    unmatched_courses: list[str]
    warnings: list[str]
```

### Frontend: fetching skills

```typescript
// frontend/src/api/skills.ts  (NEW)

export interface SkillEvidence {
  course_name: string;
  credits: number | null;
  grade: string | null;
  handbook_module: string | null;
  match_method: string;
  match_confidence: number;
  contribution: number;
}

export interface UserSkillItem {
  skill: string;
  category: string | null;
  score: number;  // 0.0-1.0
  evidence: SkillEvidence[];
}

export interface UserSkillProfile {
  user_id: number;
  computation_run_id: string | null;
  computed_at: string | null;
  skills: UserSkillItem[];
  unmatched_courses: string[];
  warnings: string[];
}

export function getUserSkills(): Promise<UserSkillProfile> {
  return api<UserSkillProfile>("/api/students/me/skills");
}
```

### Frontend: SkillRadar refactored (key changes only)

```tsx
// frontend/src/components/SkillRadar.tsx  (MODIFIED)

// BEFORE: coursesToRadarData() keyword heuristic, 6 fixed axes, AXIS_KEYWORDS, gradeToScore()
// AFTER: receives top-N skills from API, axes are dynamic

interface SkillRadarProps {
  /** Top N skills from GET /api/students/me/skills, sorted by score desc. */
  skills?: UserSkillItem[];
  /** Optional target profile for comparison polygon. */
  targetScores?: number[];
}

export default function SkillRadar({ skills, targetScores }: SkillRadarProps) {
  const topSkills = skills?.slice(0, 6) ?? [];  // show top 6 by default
  const axes = topSkills.map(s => s.skill);
  const current = topSkills.map(s => s.score * 4);  // scale 0-1 → 0-4 for SVG
  // ... rest of SVG rendering unchanged ...
}
```

---

## 15. Error Handling & Edge Cases

| Scenario | Policy |
|---|---|
| No handbook ingested for university | Return empty skills with warning `"No module handbook available"` |
| Course has no grade | `grade_factor = 0.5` (neutral) |
| Course has no ECTS | Assume `default_ects` (5.0 ECTS); add warning to run |
| Course does not match any handbook entry | Recorded in `unmatched_courses`, excluded from scoring |
| Match confidence < `min_match_confidence` (0.5) | Excluded from scoring; recorded in `low_confidence_matches` |
| LLM returns invalid JSON for tag generation | Retry up to 2 times; on failure skip entry and add warning |
| Repeated computation (same ToR re-uploaded) | Idempotent: `DELETE user_skills WHERE user_id=X` then insert new rows |
| No semester info on any course | All `recency_factor = 0.75` (neutral); no warning |
| All modules fail matching | Return empty skills with detailed unmatched list |
| Failed modules (grade 5.0) | `grade_factor = 0.0` → zero contribution → naturally excluded |
| Docling import failure | Celery task marks failure with clear error message |
| Handbook PDF parsing yields zero modules | Task fails with `"No modules could be extracted"` |

---

## 16. Testing Strategy

### Unit tests (pure, no DB, no LLM)

| File | What to cover |
|---|---|
| `tests/test_scorer.py` | Formula correctness with known inputs; edge cases (no credits, no grade, all factors at extremes, empty input) |
| `tests/test_matcher.py` | Each matching step in isolation; cascade ordering; confidence thresholds |
| `tests/test_taxonomy.py` | Alias resolution; fuzzy dedup; new tag creation; German → canonical |
| `tests/test_handbook_parser.py` | Module boundary detection from synthetic Docling output |

### Integration tests (test DB, mock LLM via `respx`)

| File | What to cover |
|---|---|
| `tests/test_skill_service.py` | Full pipeline with sample handbook + courses; idempotent re-run |
| `tests/test_skill_repository.py` | CRUD ops; `replace_user_skills` atomicity; cascade deletes |
| `tests/test_tag_generator.py` | LLM prompt construction; response parsing; caching logic |

### End-to-end tests

| Scenario | How |
|---|---|
| `compute_skills` Celery task | `celery.contrib.pytest` or mock `execute_task`; verify DB state after run |
| `GET /me/skills` HTTP | `AsyncClient` + seeded DB; verify response schema |
| Upload → skills chain | Full flow: upload PDF → poll job → check `/me/skills` |

### Key fixtures

```
tests/fixtures/
  sample_handbook.json       ← 10-20 ModuleHandbookEntry dicts
  sample_courses.json        ← matching StudentCourse dicts
  expected_scores.json       ← golden test: known skill scores for the above
  sample_transcript.pdf      ← small synthetic PDF for parser tests
```

---

## 17. Observability & Logging

### Logging pattern

Following the existing `Step N/M — description (user_id=X)` convention:

```python
_logger.info("Step 1/5 — Loading %d student courses (user_id=%d)", n, user_id)
_logger.info("Step 2/5 — Matching courses against %d handbook entries", len(entries))
_logger.info("Step 3/5 — Ensuring skill mappings for %d untagged entries", n_untagged)
_logger.info("Step 4/5 — Computing scores: %d skills across %d matched modules", n_skills, n_matched)
_logger.info("Step 5/5 — Persisting skills and evidence (user_id=%d)", user_id)
```

Warnings for partial failures:
```python
_logger.warning("Unmatched course: %r (user_id=%d)", course.course_name, user_id)
_logger.warning("Low-confidence match: course=%r entry=%r conf=%.2f", ...)
_logger.warning("LLM tag generation failed for entry_id=%d; skipping", entry.id)
```

### Audit trail

`skill_computation_runs` records every run with:
- Scoring config snapshot
- Counts (total, matched, unmatched)
- All warnings
- Created and completed timestamps
- Link to `jobs.id` for Celery job status

### WebSocket events

| Event | When | Key payload fields |
|---|---|---|
| `skills_computing` | Task starts | `job_id`, `user_id`, `status: "started"` |
| `skills_computed` | Task succeeds | `job_id`, `skills_count`, `matched_courses` |
| `task_failed` | Task fails | `job_id`, `error` |

---

## 18. MVP Implementation Plan

### Phase 1 — Foundation: models & DB (Days 1-2)

- [ ] Create `models/skill.py` (SkillTag, UserSkill, SkillEvidence, SkillComputationRun)
- [ ] Create `models/handbook.py` (ModuleHandbookEntry, ModuleSkillMapping)
- [ ] Create `alembic/versions/00XX_skill_computation.py` with all tables, indexes, enum additions
- [ ] Seed initial taxonomy (~70 skills) in the migration
- [ ] Implement `SkillRepository` (get_profile, replace_user_skills, complete_run)
- [ ] Implement `HandbookRepository` (get_latest_entries, upsert_entry)

### Phase 2 — Handbook ingestion (Days 2-3)

- [ ] Add `docling>=2.97` and `rapidfuzz>=3.0` to `pyproject.toml`
- [ ] Implement `DoclingHandbookParser` in `handbook/parser.py`
- [ ] Implement `HandbookService` in `handbook/service.py`
- [ ] Implement `ingest_handbook` Celery task in `handbook/tasks.py`
- [ ] Add admin handbook upload endpoint (`POST /api/admin/handbook`)
- [ ] Register `"app.handbook"` and `"app.skills"` in `worker/celery_app.py`

### Phase 3 — Matching & tag generation (Days 3-4)

- [ ] Implement `CascadeModuleMatcher` (exact code → title exact → fuzzy → semantic)
- [ ] Implement `LLMSkillTagGenerator` with caching and Pydantic validation
- [ ] Implement `SkillTaxonomy` (normalize, get_or_create, alias resolution)
- [ ] Unit tests for matcher, taxonomy, tag generator

### Phase 4 — Scoring & orchestration (Day 4)

- [ ] Implement `compute_skill_scores()` in `skills/scorer.py` (pure function)
- [ ] Implement `SkillComputationService.compute_skills()` orchestrator
- [ ] Implement `compute_skills` Celery task in `skills/tasks.py`
- [ ] Chain `compute_skills` after `parse_transcript` success in `students/tasks.py`
- [ ] Unit tests for scorer, integration test for service

### Phase 5 — API & frontend (Days 5-6)

- [ ] Implement `GET /api/students/me/skills` with `UserSkillProfileOut` response
- [ ] Implement `POST /api/students/me/skills/recompute`
- [ ] Register skills router in `main.py`
- [ ] Create `frontend/src/api/skills.ts`
- [ ] Refactor `SkillRadar.tsx`: remove `AXIS_KEYWORDS`, `coursesToRadarData`, `gradeToScore`; accept `skills: UserSkillItem[]`
- [ ] Refactor `Dashboard.tsx`: fetch from `/me/skills`, pass to SkillRadar/SkillBar, remove `SKILL_BAR_AXES`

### Phase 6 — Agent integration & polish (Day 6)

- [ ] Inject computed skills into `ChatService._build_student_context()`
- [ ] Add optional `compute_user_skills` tool to `TOOLS_SPEC`
- [ ] End-to-end test with a real Modulhandbuch PDF
- [ ] Add computation status indicator in Dashboard (pending/running/done)

---

## 19. Future Extension Roadmap

| Feature | Notes |
|---|---|
| **Skill gap analysis** | Compare `user_skills.score` against thesis `skills_required` to compute per-proposal fit scores |
| **Dynamic target profile** | Replace hardcoded `TARGET_DATA` with mean scores derived from thesis requirements matching the student's program |
| **Multi-university support** | Allow users to select their university; score against the right handbook version |
| **Handbook auto-update** | Periodic ingestion job that checks for new handbook versions |
| **Skill recommendations** | Identify low-scoring skills required by matched theses; recommend courses |
| **Skill-based thesis search** | Use `user_skills` vector for a new `search_theses_by_skill_profile` tool |
| **Historical skill tracking** | Archive `skill_computation_runs` to show skill growth across transcript updates |
| **Admin curation UI** | Web UI for reviewing/editing skill tags, mappings, and aliases |
| **Confidence tuning UI** | Let admins adjust `ScoringConfig` per university |

---

## 20. Risks & Tradeoffs

| Risk | Impact | Mitigation |
|---|---|---|
| **Handbook availability** | No handbook → no skill computation | Fallback mode: LLM-only tag generation from course names (no handbook required, lower quality) |
| **Docling dependency weight** | ~200 MB+ with layout ML models | Acceptable for background worker; import is confined to `handbook/parser.py` |
| **LLM cost/latency for tag generation** | 200+ modules × 1 LLM call | One-time cost per handbook version; results cached in `module_skill_mappings` |
| **Matching false positives** | Wrong handbook entry matched | Configurable confidence threshold; all low-confidence matches exposed in API and warnings |
| **Taxonomy drift** | Proliferation of near-duplicate skill tags | Fuzzy dedup at creation time; seed taxonomy covers the most common skills |
| **Scoring weight subjectivity** | Different weight choices produce different rankings | All weights stored per-run in `config` JSONB; can be tuned without a migration |
| **German/English mixed content** | Transcript in German, handbook may be bilingual | Normalization handles umlauts; matching tests both `module_title` and `module_title_en` |
| **Branch dependency (Celery/Redis)** | Feature requires `architecture_refactoring` to be merged | Core logic (scorer, matcher, taxonomy) is fully independent; Celery is a thin wrapper layer |

---

## 21. Appendix: New File Structure

```
backend/
├── app/
│   ├── skills/                     # NEW — skill computation domain
│   │   ├── __init__.py
│   │   ├── controller.py           # GET /me/skills, POST /me/skills/recompute
│   │   ├── deps.py                 # SkillServiceDep, SkillRepoDep
│   │   ├── service.py              # SkillComputationService
│   │   ├── repository.py           # SkillRepository
│   │   ├── schemas.py              # UserSkillProfileOut, UserSkillItemOut, etc.
│   │   ├── tasks.py                # Celery: compute_skills
│   │   ├── scorer.py               # ScoringConfig, compute_skill_scores() (pure)
│   │   ├── matcher.py              # CascadeModuleMatcher
│   │   ├── tag_generator.py        # LLMSkillTagGenerator (cached per entry)
│   │   ├── taxonomy.py             # SkillTaxonomy (normalize, get_or_create)
│   │   └── ports.py                # Protocol interfaces
│   │
│   ├── handbook/                   # NEW — module handbook domain
│   │   ├── __init__.py
│   │   ├── controller.py           # POST /admin/handbook, GET /admin/handbook
│   │   ├── deps.py                 # HandbookServiceDep
│   │   ├── service.py              # HandbookService
│   │   ├── repository.py           # HandbookRepository
│   │   ├── schemas.py              # HandbookVersionOut, HandbookEntryOut
│   │   ├── parser.py               # DoclingHandbookParser
│   │   └── tasks.py                # Celery: ingest_handbook
│   │
│   ├── models/
│   │   ├── (existing files unchanged)
│   │   ├── skill.py                # NEW: SkillTag, UserSkill, SkillEvidence, SkillComputationRun
│   │   └── handbook.py             # NEW: ModuleHandbookEntry, ModuleSkillMapping
│   │
│   └── worker/
│       └── celery_app.py           # MODIFIED: add "app.handbook", "app.skills" to autodiscover
│
├── alembic/versions/
│   └── 00XX_skill_computation.py   # NEW migration
│
└── tests/
    ├── test_scorer.py              # NEW
    ├── test_matcher.py             # NEW
    ├── test_taxonomy.py            # NEW
    ├── test_skill_service.py       # NEW
    └── fixtures/
        ├── sample_handbook.json    # NEW
        ├── sample_courses.json     # NEW
        └── expected_scores.json    # NEW

frontend/
└── src/
    ├── api/
    │   └── skills.ts               # NEW: getUserSkills(), UserSkillProfile types
    ├── components/
    │   └── SkillRadar.tsx           # MODIFIED: data-driven, remove keyword heuristics
    └── pages/
        └── Dashboard.tsx            # MODIFIED: fetch skills from API, remove SKILL_BAR_AXES
```
