# ArXiv Scraper — Technical Design & Implementation Plan

## 1. Executive Summary

This document designs a **paper discovery and enrichment pipeline** for the study-os platform. The system:

1. **Discovers papers** via Google Scholar (Playwright-based browser scraping), then **enriches metadata** from arXiv when available
2. **Generates LLM summaries and tags** for each paper using a dedicated enrichment model
3. **Ranks papers** by recency and relevance
4. **Stores everything** in a normalized PostgreSQL schema with deduplication
5. **Runs as Celery background tasks** using the existing `architecture_refactoring` worker infrastructure

The architecture follows the existing codebase patterns (controller/service/repository/schemas) and introduces three new domain modules: `app/papers/`, `app/researchers/`, and `app/scraper/`.

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI / API Layer                       │
│   POST /api/scraper/run/{chair_id}    (trigger scrape)       │
│   GET  /api/papers?chair_id=&tag=     (query papers)         │
│   GET  /api/researchers?chair_id=     (list researchers)     │
└──────────────┬──────────────────────────────────────┬────────┘
               │                                      │
               ▼                                      ▼
┌──────────────────────────┐        ┌──────────────────────────┐
│    Scraper Service        │        │    Paper Service          │
│  (orchestration layer)    │        │  (query, ranking, CRUD)   │
│                          │        │                          │
│  1. Resolve researchers  │        │  - list/search papers    │
│  2. For each researcher: │        │  - compute rankings      │
│     a. Scholar scrape    │        │  - filter by tag/chair   │
│     b. ArXiv enrichment  │        └──────────────────────────┘
│     c. LLM enrichment    │
│     d. Dedup + store     │
└──────────┬───────────────┘
           │ dispatches Celery tasks
           ▼
┌──────────────────────────────────────────────────────────────┐
│                     Worker Layer (Celery)                      │
│                                                              │
│  scrape_chair_papers     (fan-out per researcher)            │
│  scrape_researcher       (Scholar + ArXiv + enrich + store)  │
│  enrich_paper            (LLM summary + tags, idempotent)    │
└──────────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                   Infrastructure Adapters                      │
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ ScholarScraper   │  │ ArxivClient     │  │ LLMEnricher  │ │
│  │ (Playwright)     │  │ (httpx + XML)   │  │ (LLMPort)    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ PaperRepository  │  │ ResearcherRepo  │                   │
│  │ (SQLAlchemy)     │  │ (SQLAlchemy)    │                   │
│  └─────────────────┘  └─────────────────┘                   │
└──────────────────────────────────────────────────────────────┘
```

**Key design decisions:**
- Each infrastructure adapter implements an **abstract base class / Protocol** so it can be swapped
- The `ScholarScraper` is the paper source adapter; later a `SemanticScholarClient`, `DBLPClient`, etc. can implement the same `PaperSourceClient` interface
- LLM enrichment uses a dedicated model config (`LLM_ENRICHMENT_MODEL`), not the chat model
- Deduplication is based on `(arxiv_id)` when available, falling back to `(doi)`, then `(title_normalized, first_author)`

---

## 3. Core Domain Model (Pydantic)

These are pure domain objects, independent of SQLAlchemy:

```python
# app/papers/domain.py
from datetime import datetime
from pydantic import BaseModel, Field

class PaperCandidate(BaseModel):
    """Raw paper data from any source, before enrichment."""
    title: str
    abstract: str | None = None
    authors: list[str] = Field(default_factory=list)
    publication_date: datetime | None = None
    source: str                      # "google_scholar", "arxiv", "semantic_scholar"
    source_url: str
    arxiv_id: str | None = None
    doi: str | None = None

class EnrichedPaper(PaperCandidate):
    """Paper after LLM enrichment."""
    summary: str | None = None
    tags: list[str] = Field(default_factory=list)
    recency_score: float = 0.0
    relevance_score: float = 0.0

class ResearcherInfo(BaseModel):
    """Researcher identity for paper lookups."""
    name: str
    google_scholar_id: str | None = None
    orcid: str | None = None
    affiliation: str | None = None
    chair_id: int | None = None
```

---

## 4. Database Schema

### New tables (Alembic migration `0010_papers_researchers.py`):

```sql
-- Researchers linked to a chair
CREATE TABLE researchers (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR(255) NOT NULL,
    google_scholar_id   VARCHAR(50) UNIQUE,
    orcid               VARCHAR(50) UNIQUE,
    affiliation         VARCHAR(500),
    chair_id            INTEGER REFERENCES chairs(id) ON DELETE SET NULL,
    is_professor        BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMPTZ DEFAULT now(),
    updated_at          TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ix_researchers_chair ON researchers(chair_id);

-- Canonical papers table
CREATE TABLE papers (
    id                  SERIAL PRIMARY KEY,
    title               VARCHAR(1000) NOT NULL,
    title_normalized    VARCHAR(1000) NOT NULL,   -- lowercase, stripped
    abstract            TEXT,
    summary             TEXT,                     -- LLM-generated
    authors             JSONB NOT NULL DEFAULT '[]',
    publication_date    TIMESTAMPTZ,
    source              VARCHAR(50) NOT NULL,      -- first source that found it
    source_url          VARCHAR(1000) NOT NULL,
    arxiv_id            VARCHAR(50) UNIQUE,        -- NULL if not on arXiv
    doi                 VARCHAR(100) UNIQUE,       -- NULL if unknown
    recency_score       FLOAT DEFAULT 0.0,
    relevance_score     FLOAT DEFAULT 0.0,
    embedding           vector(2560),              -- abstract embedding
    enriched_at         TIMESTAMPTZ,               -- NULL = not yet enriched
    created_at          TIMESTAMPTZ DEFAULT now(),
    updated_at          TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ix_papers_arxiv ON papers(arxiv_id) WHERE arxiv_id IS NOT NULL;
CREATE INDEX ix_papers_doi ON papers(doi) WHERE doi IS NOT NULL;
CREATE INDEX ix_papers_pub_date ON papers(publication_date DESC);

-- Many-to-many: which researchers authored which papers
CREATE TABLE researcher_papers (
    researcher_id   INTEGER REFERENCES researchers(id) ON DELETE CASCADE,
    paper_id        INTEGER REFERENCES papers(id) ON DELETE CASCADE,
    PRIMARY KEY (researcher_id, paper_id)
);

-- Normalized tags
CREATE TABLE tags (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) UNIQUE NOT NULL   -- lowercase, canonical
);

-- Many-to-many: paper <-> tag
CREATE TABLE paper_tags (
    paper_id    INTEGER REFERENCES papers(id) ON DELETE CASCADE,
    tag_id      INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (paper_id, tag_id)
);

-- Dedup helper: normalized title + first author for non-arxiv/non-doi papers
CREATE UNIQUE INDEX uq_papers_title_author
    ON papers (title_normalized, (authors->>0))
    WHERE arxiv_id IS NULL AND doi IS NULL;
```

### Relationship to existing tables

- `researchers.chair_id` → `chairs.id` — links a researcher to a chair
- The existing `chair_documents` table is **untouched** — it continues to serve chair description embeddings for the thesis recommendation system
- Papers found via the scraper populate the new `papers` table; they are not duplicated in `chair_documents`

---

## 5. Interfaces / Abstract Base Classes

```python
# app/scraper/interfaces.py
from abc import ABC, abstractmethod
from app.papers.domain import PaperCandidate, ResearcherInfo

class PaperSourceClient(ABC):
    """Fetches papers from an external source."""

    @abstractmethod
    async def fetch_papers(
        self,
        researcher: ResearcherInfo,
        *,
        max_results: int = 20,
        since_days: int = 365,
    ) -> list[PaperCandidate]:
        """Return recent papers for this researcher."""
        ...

    @abstractmethod
    async def close(self) -> None: ...


class PaperMetadataEnricher(ABC):
    """Enriches a paper candidate with additional metadata from an API."""

    @abstractmethod
    async def enrich(self, paper: PaperCandidate) -> PaperCandidate:
        """Fetch full abstract, dates, IDs from authoritative source."""
        ...


class ResearcherDiscoveryClient(ABC):
    """Discovers researchers from an external source (e.g., chair website)."""

    @abstractmethod
    async def discover_researchers(
        self, chair_website_url: str
    ) -> list[ResearcherInfo]:
        ...


class LLMEnricher(ABC):
    """Generates summaries and tags for papers using an LLM."""

    @abstractmethod
    async def summarize(self, title: str, abstract: str) -> str: ...

    @abstractmethod
    async def generate_tags(self, title: str, abstract: str) -> list[str]: ...


class PaperRanker(ABC):
    """Computes scores for papers."""

    @abstractmethod
    def compute_recency_score(self, publication_date: datetime | None) -> float: ...

    @abstractmethod
    def compute_relevance_score(self, paper: EnrichedPaper) -> float: ...
```

---

## 6. Pipeline Design

The scraper pipeline has 5 stages, each idempotent:

```
Stage 1: Resolve Researchers
    Input:  chair_id
    Output: list[ResearcherInfo]
    Logic:  Query researchers table for chair_id.
            For MVP: auto-create from chairs.professor_name if none exist.

Stage 2: Discover Papers (Google Scholar via Playwright)
    Input:  ResearcherInfo
    Output: list[PaperCandidate]
    Logic:  For each researcher, scrape Google Scholar profile/search.
            Extract title, authors, year, link.

Stage 3: Enrich from ArXiv
    Input:  PaperCandidate (with potential arxiv link from Scholar)
    Output: PaperCandidate (with full abstract, arxiv_id, exact date)
    Logic:  If source_url contains arxiv.org, extract arxiv_id and
            fetch full metadata via the arXiv Atom API.
            If not from arXiv, keep Scholar data as-is.

Stage 4: LLM Enrichment
    Input:  PaperCandidate with abstract
    Output: EnrichedPaper (with summary + tags)
    Logic:  Skip if paper.enriched_at is set (idempotent).
            Call LLMEnricher.summarize() and .generate_tags().
            Normalize tags against canonical tag list.

Stage 5: Score, Deduplicate, Store
    Input:  EnrichedPaper
    Output: Paper row in DB
    Logic:  Compute recency_score and relevance_score.
            Check for existing paper by arxiv_id, then doi,
            then (title_normalized, first_author).
            INSERT or UPDATE (merge new data into existing).
            Link to researcher via researcher_papers.
```

---

## 7. Concrete Adapter Implementations

### 7a. ScholarPlaywrightScraper

```python
# app/scraper/adapters/scholar_scraper.py
import asyncio
import logging
from playwright.async_api import async_playwright, Browser, Page
from app.scraper.interfaces import PaperSourceClient
from app.papers.domain import PaperCandidate, ResearcherInfo

_logger = logging.getLogger(__name__)

class ScholarPlaywrightScraper(PaperSourceClient):
    """Scrapes Google Scholar using Playwright for paper discovery."""

    def __init__(
        self,
        headless: bool = True,
        request_delay: float = 3.0,      # seconds between requests
        max_pages: int = 3,               # max Scholar result pages
    ) -> None:
        self._headless = headless
        self._delay = request_delay
        self._max_pages = max_pages
        self._browser: Browser | None = None
        self._pw = None

    async def _ensure_browser(self) -> Browser:
        if self._browser is None:
            self._pw = await async_playwright().start()
            self._browser = await self._pw.chromium.launch(headless=self._headless)
        return self._browser

    async def fetch_papers(
        self,
        researcher: ResearcherInfo,
        *,
        max_results: int = 20,
        since_days: int = 365,
    ) -> list[PaperCandidate]:
        browser = await self._ensure_browser()
        page = await browser.new_page()
        papers: list[PaperCandidate] = []

        try:
            query = f'author:"{researcher.name}"'
            url = f"https://scholar.google.com/scholar?q={query}&as_ylo={_year_cutoff(since_days)}"
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(self._delay)

            for _ in range(self._max_pages):
                results = await self._parse_results_page(page)
                papers.extend(results)
                if len(papers) >= max_results:
                    break
                next_btn = page.locator('button[aria-label="Next"]')
                if await next_btn.count() == 0:
                    break
                await next_btn.click()
                await asyncio.sleep(self._delay)

        except Exception as exc:
            _logger.warning("Scholar scrape failed for %s: %s", researcher.name, exc)
        finally:
            await page.close()

        return papers[:max_results]

    async def _parse_results_page(self, page: Page) -> list[PaperCandidate]:
        """Extract paper candidates from a Scholar results page."""
        entries = page.locator("div.gs_r.gs_or.gs_scl")
        papers = []
        for i in range(await entries.count()):
            entry = entries.nth(i)
            try:
                title_el = entry.locator("h3.gs_rt a").first
                title = await title_el.inner_text()
                href = await title_el.get_attribute("href") or ""
                meta = await entry.locator("div.gs_a").inner_text()
                authors = self._parse_authors(meta)
                year = self._parse_year(meta)
                arxiv_id = _extract_arxiv_id(href)

                papers.append(PaperCandidate(
                    title=title.strip(),
                    authors=authors,
                    publication_date=_year_to_date(year),
                    source="google_scholar",
                    source_url=href,
                    arxiv_id=arxiv_id,
                ))
            except Exception:
                continue  # skip malformed entries
        return papers

    async def close(self) -> None:
        if self._browser:
            await self._browser.close()
        if self._pw:
            await self._pw.stop()
```

### 7b. ArxivMetadataEnricher

Builds on the existing `_fetch_arxiv_metadata` logic in `app/chairs/service.py`:

```python
# app/scraper/adapters/arxiv_client.py
class ArxivMetadataEnricher(PaperMetadataEnricher):
    """Fetches full metadata from arXiv Atom API for papers with an arxiv_id."""

    def __init__(self, timeout: float = 15.0, rate_limit_delay: float = 1.0):
        self._timeout = timeout
        self._delay = rate_limit_delay

    async def enrich(self, paper: PaperCandidate) -> PaperCandidate:
        if not paper.arxiv_id:
            return paper  # nothing to enrich

        url = f"https://export.arxiv.org/api/query?id_list={paper.arxiv_id}"
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()

        root = ET.fromstring(resp.text)
        entry = root.find(f"{{{ARXIV_NS}}}entry")
        if entry is None:
            return paper

        paper.abstract = _text(entry, "summary")
        paper.publication_date = _parse_date(entry, "published")
        paper.source_url = f"https://arxiv.org/abs/{paper.arxiv_id}"
        arxiv_authors = _parse_authors(entry)
        if arxiv_authors:
            paper.authors = arxiv_authors

        await asyncio.sleep(self._delay)  # rate limit courtesy
        return paper
```

### 7c. LLMPaperEnricher

A self-contained enrichment class with its own configurable model:

```python
# app/scraper/adapters/llm_enricher.py
class LLMPaperEnricher(LLMEnricher):
    """Uses the LLMPort interface with a dedicated enrichment model."""

    # Canonical tag vocabulary — extended via DB or config
    CANONICAL_TAGS: set[str] = {
        "machine learning", "deep learning", "reinforcement learning",
        "natural language processing", "computer vision", "robotics",
        "optimization", "statistics", "mathematics", "control theory",
        "signal processing", "information theory", "graph theory",
        "neural networks", "generative models", "transformers",
        "bayesian methods", "causal inference", "federated learning",
    }

    def __init__(self, llm_client: LLMPort, model_name: str):
        self._llm = llm_client
        self._model = model_name

    async def summarize(self, title: str, abstract: str) -> str:
        prompt = (
            "Summarize this research paper in 2-3 sentences for a graduate student. "
            "Focus on the main contribution and methodology.\n\n"
            f"Title: {title}\n\nAbstract: {abstract}"
        )
        resp = await self._llm.chat(
            self._model,
            [{"role": "user", "content": prompt}],
            options={"temperature": 0.3, "num_predict": 200},
        )
        return resp["message"]["content"].strip()

    async def generate_tags(self, title: str, abstract: str) -> list[str]:
        tag_list = ", ".join(sorted(self.CANONICAL_TAGS))
        prompt = (
            "Given this research paper, select 2-5 tags from the list below. "
            "Return ONLY a JSON array of strings, nothing else.\n\n"
            f"Available tags: [{tag_list}]\n\n"
            f"Title: {title}\n\nAbstract: {abstract}"
        )
        resp = await self._llm.chat(
            self._model,
            [{"role": "user", "content": prompt}],
            options={"temperature": 0.1, "num_predict": 100},
        )
        raw = resp["message"]["content"].strip()
        return self._parse_and_normalize_tags(raw)

    def _parse_and_normalize_tags(self, raw: str) -> list[str]:
        """Parse JSON array, fuzzy-match against canonical tags."""
        import json, re
        try:
            tags = json.loads(raw)
        except json.JSONDecodeError:
            tags = re.findall(r'"([^"]+)"', raw)

        normalized = []
        for tag in tags:
            tag_lower = tag.strip().lower()
            if tag_lower in self.CANONICAL_TAGS:
                normalized.append(tag_lower)
            else:
                best = self._fuzzy_match(tag_lower)
                if best:
                    normalized.append(best)
        return list(dict.fromkeys(normalized))  # deduplicate, preserve order
```

### 7d. RecencyPaperRanker

```python
# app/scraper/adapters/ranker.py
import math
from datetime import datetime, timezone

class RecencyPaperRanker(PaperRanker):
    """Exponential decay ranker: recent papers score higher."""

    def __init__(self, half_life_days: int = 180):
        """half_life_days: days after which score decays to 0.5."""
        self._decay = math.log(2) / half_life_days

    def compute_recency_score(self, publication_date: datetime | None) -> float:
        if publication_date is None:
            return 0.1  # unknown date = low score
        now = datetime.now(timezone.utc)
        age_days = max((now - publication_date).days, 0)
        return math.exp(-self._decay * age_days)
        # Examples (half_life=180):
        #   today       → 1.0
        #   6 months    → 0.5
        #   1 year      → 0.25
        #   2 years     → 0.0625

    def compute_relevance_score(self, paper) -> float:
        # MVP: relevance = recency_score
        # Future: add citation count weighting, embedding similarity to chair description
        return paper.recency_score
```

---

## 8. Async / Concurrency Strategy

| Operation | Strategy | Concurrency | Rate Limit |
|---|---|---|---|
| Google Scholar scrape | Playwright async, single browser per task | 1 page at a time per researcher | 3s delay between requests |
| ArXiv API calls | httpx async | `asyncio.Semaphore(5)` across concurrent tasks | 1s delay between calls |
| LLM enrichment | `LLMPort` async (httpx) | `asyncio.Semaphore(3)` for local Ollama | N/A for local model |
| DB writes | SQLAlchemy async sessions | Per-task sessions (never shared across tasks) | N/A |

### Celery task structure

```python
# app/scraper/tasks.py

@celery_app.task(
    bind=True,
    soft_time_limit=600,
    time_limit=660,
    max_retries=2,
    default_retry_delay=60,
)
def scrape_chair_papers(self, job_id: str, chair_id: int) -> None:
    """Fan-out: dispatch a scrape task for each researcher of the chair."""
    execute_task(self, job_id, _scrape_chair_papers_work, chair_id=chair_id)


@celery_app.task(
    bind=True,
    soft_time_limit=300,
    time_limit=360,
    max_retries=3,
    default_retry_delay=30,
)
def scrape_researcher_papers(self, job_id: str, researcher_id: int) -> None:
    """Scrape + enrich + store papers for one researcher."""
    execute_task(self, job_id, _scrape_researcher_work, researcher_id=researcher_id)


@celery_app.task(
    bind=True,
    soft_time_limit=120,
    time_limit=180,
    max_retries=3,
    default_retry_delay=30,
)
def enrich_paper(self, job_id: str, paper_id: int) -> None:
    """LLM enrichment for a single paper (idempotent, skips enriched_at != NULL)."""
    execute_task(self, job_id, _enrich_paper_work, paper_id=paper_id)
```

> **Playwright in Celery workers:** Each task creates and destroys its own Playwright browser instance within `asyncio.run()`. This is safe because Celery prefork workers have no pre-existing event loop. Set `worker_max_tasks_per_child=10` to prevent memory accumulation from Chromium.

---

## 9. Deduplication Strategy

Three-tier lookup, falling through in order:

```python
# app/papers/dedup.py

class DeduplicationService:
    def __init__(self, paper_repo: PaperRepository):
        self._repo = paper_repo

    async def find_duplicate(self, candidate: PaperCandidate) -> Paper | None:
        # Tier 1: exact arxiv_id match (most reliable)
        if candidate.arxiv_id:
            existing = await self._repo.get_by_arxiv_id(candidate.arxiv_id)
            if existing:
                return existing

        # Tier 2: exact DOI match
        if candidate.doi:
            existing = await self._repo.get_by_doi(candidate.doi)
            if existing:
                return existing

        # Tier 3: normalized title + first author
        title_norm = self._normalize_title(candidate.title)
        first_author = candidate.authors[0] if candidate.authors else None
        if first_author:
            existing = await self._repo.get_by_title_author(title_norm, first_author)
            if existing:
                return existing

        return None

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Lowercase, strip punctuation, collapse whitespace."""
        import re
        t = title.lower().strip()
        t = re.sub(r'[^\w\s]', '', t)
        t = re.sub(r'\s+', ' ', t)
        return t
```

When a duplicate is found, the pipeline **merges** rather than skips: it fills any `NULL` fields with newly discovered data (e.g., adds `arxiv_id` if the Scholar entry had only a link, enriches the abstract from arXiv). A unique constraint in the DB (`uq_papers_title_author`) acts as a final safety net at the persistence layer.

---

## 10. Recency / Relevance Ranking Strategy

**Recency score** uses exponential decay:

```
recency_score(t) = exp(-ln(2) / half_life * age_in_days)
```

With the default `half_life = 180 days`:

| Age | Score |
|---|---|
| Today | 1.000 |
| 3 months | 0.707 |
| 6 months | 0.500 |
| 1 year | 0.250 |
| 2 years | 0.063 |

**Relevance score** is a weighted composite (MVP → production evolution):

```
# MVP
relevance_score = recency_score

# Phase 2: add citation weighting
relevance_score = 0.6 * recency_score + 0.4 * citation_score_normalized

# Phase 3: add semantic similarity to chair description
relevance_score = 0.5 * recency_score
               + 0.3 * citation_score_normalized
               + 0.2 * cosine_similarity(paper_embed, chair_embed)
```

Scores are recomputed on each scrape run. A nightly Celery Beat job (`recompute_scores`) refreshes recency scores for all papers without re-scraping.

---

## 11. LLM Summary and Tag Generation Strategy

### Summary generation
- Single prompt asking for a 2–3 sentence summary for a graduate student
- Low temperature (0.3) for deterministic output
- Output capped at 200 tokens

### Tag generation
- LLM is given a **closed vocabulary** of canonical tags (see `LLMPaperEnricher.CANONICAL_TAGS`)
- Prompted to return a JSON array of 2–5 tags from that list only
- Low temperature (0.1) for consistency
- Output validated via JSON parsing; fallback regex extracts quoted strings if parsing fails
- Each returned tag is matched against the canonical set (exact match, then fuzzy match via `thefuzz`)
- Unrecognized tags are logged and discarded

### Idempotency
- The `papers.enriched_at` timestamp is the idempotency guard
- `enrich_paper` is a no-op if `enriched_at IS NOT NULL` (unless `force=True` is passed)
- This means re-running the scraper only enriches new papers

### Canonical tag management
- Tags are seeded from a fixed list in `app/scraper/tags.py`
- Stored in the `tags` table for normalized many-to-many linking
- New tags can be added via migration or an admin endpoint — all existing papers with fuzzy-matched tags auto-link on the next enrichment pass

---

## 12. Playwright MCP Researcher Discovery (Phase 2 Extension)

For Phase 2, a `PlaywrightDiscoveryClient` implements `ResearcherDiscoveryClient` by navigating a chair's team/people page:

```python
# app/scraper/adapters/playwright_discovery.py
class PlaywrightDiscoveryClient(ResearcherDiscoveryClient):
    """Scrapes a chair's team page to discover researchers."""

    async def discover_researchers(self, chair_website_url: str) -> list[ResearcherInfo]:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(chair_website_url)

            # Heuristic: find team/people/members page links
            team_url = await self._find_team_page_url(page, chair_website_url)
            if team_url:
                await page.goto(team_url)

            researchers = await self._extract_people(page)
            await browser.close()
            return researchers
```

**Alternative via Playwright MCP:** If the Playwright MCP server is available as an agent tool, the discovery step can be delegated to an LLM agent that navigates the page and returns structured researcher data. This is the natural extension point for the existing ReAct agent in `app/chat/service.py`.

**MVP trigger for Phase 2:** A new admin endpoint `POST /api/chairs/{id}/discover-researchers` dispatches a `discover_researchers` Celery task. Discovered researchers are stored in the `researchers` table with `is_professor=False` and surface in the admin UI for review/approval before paper scraping begins.

---

## 13. Repository / File Structure

```
backend/app/
├── papers/                          # Paper domain module
│   ├── __init__.py
│   ├── domain.py                    # PaperCandidate, EnrichedPaper, ResearcherInfo (Pydantic)
│   ├── models.py                    # SQLAlchemy: Paper, Tag, PaperTag
│   ├── repository.py                # PaperRepository, TagRepository
│   ├── service.py                   # PaperService (query, list, filter by tag/chair)
│   ├── schemas.py                   # PaperOut, PaperListResponse, TagOut
│   ├── controller.py                # GET /api/papers, GET /api/papers/{id}
│   ├── deps.py                      # FastAPI dependency injection
│   └── dedup.py                     # DeduplicationService
│
├── researchers/                     # Researcher domain module
│   ├── __init__.py
│   ├── models.py                    # SQLAlchemy: Researcher, ResearcherPaper
│   ├── repository.py                # ResearcherRepository
│   ├── service.py                   # ResearcherService (CRUD + auto-create from chair)
│   ├── schemas.py                   # ResearcherOut, ResearcherCreate
│   ├── controller.py                # GET /api/researchers
│   └── deps.py
│
├── scraper/                         # Scraper orchestration + adapters
│   ├── __init__.py
│   ├── interfaces.py                # ABCs: PaperSourceClient, LLMEnricher, PaperRanker, etc.
│   ├── orchestrator.py              # ScraperOrchestrator (wires the pipeline stages)
│   ├── tags.py                      # CANONICAL_TAGS seed list
│   ├── tasks.py                     # Celery tasks (scrape_chair_papers, scrape_researcher_papers, enrich_paper)
│   ├── controller.py                # POST /api/scraper/run/{chair_id}
│   ├── schemas.py                   # ScrapeRunResponse
│   ├── deps.py
│   └── adapters/
│       ├── __init__.py
│       ├── scholar_scraper.py       # ScholarPlaywrightScraper (PaperSourceClient)
│       ├── arxiv_client.py          # ArxivMetadataEnricher (PaperMetadataEnricher)
│       ├── llm_enricher.py          # LLMPaperEnricher (LLMEnricher)
│       ├── ranker.py                # RecencyPaperRanker (PaperRanker)
│       └── playwright_discovery.py  # [Phase 2] PlaywrightDiscoveryClient
│
├── models/
│   ├── __init__.py                  # Re-export Paper, Tag, Researcher (add to existing)
│   ├── paper.py                     # [new] SQLAlchemy Paper, Tag, PaperTag models
│   ├── researcher.py                # [new] SQLAlchemy Researcher, ResearcherPaper models
│   └── ... (existing files unchanged)
│
├── alembic/versions/
│   └── 0010_papers_researchers.py   # [new] papers, researchers, tags, junction tables
│
└── ... (existing modules unchanged)
```

### Dependencies to add to `pyproject.toml`

```toml
playwright = ">=1.40"   # Playwright async API + Chromium
thefuzz = ">=0.22"      # Fuzzy string matching for tag normalization
```

```bash
# After adding, install Chromium browser binary:
playwright install chromium
```

---

## 14. Orchestration Flow (Representative Code)

```python
# app/scraper/orchestrator.py

class ScraperOrchestrator:
    """Wires all pipeline stages together for one researcher."""

    def __init__(
        self,
        source: PaperSourceClient,
        arxiv_enricher: PaperMetadataEnricher,
        llm_enricher: LLMEnricher,
        ranker: PaperRanker,
        dedup: DeduplicationService,
        paper_repo: PaperRepository,
        tag_repo: TagRepository,
        researcher_repo: ResearcherRepository,
    ):
        self._source = source
        self._arxiv = arxiv_enricher
        self._llm = llm_enricher
        self._ranker = ranker
        self._dedup = dedup
        self._paper_repo = paper_repo
        self._tag_repo = tag_repo
        self._researcher_repo = researcher_repo

    async def scrape_for_researcher(self, researcher_id: int) -> dict:
        researcher_row = await self._researcher_repo.get_by_id(researcher_id)
        researcher = ResearcherInfo(
            name=researcher_row.name,
            google_scholar_id=researcher_row.google_scholar_id,
            chair_id=researcher_row.chair_id,
        )

        # Stage 2: Discover papers via Google Scholar
        candidates = await self._source.fetch_papers(researcher)
        _logger.info("Found %d candidates for %s", len(candidates), researcher.name)

        stored = 0
        skipped = 0
        for candidate in candidates:
            # Stage 3: Enrich from ArXiv (if arxiv_id present)
            candidate = await self._arxiv.enrich(candidate)

            # Stage 5a: Dedup check
            existing = await self._dedup.find_duplicate(candidate)
            if existing:
                await self._researcher_repo.link_paper(researcher_id, existing.id)
                await self._dedup.merge_metadata(existing, candidate)
                skipped += 1
                continue

            # Stage 4: LLM enrichment (only if abstract available)
            summary = None
            tags: list[str] = []
            if candidate.abstract:
                summary = await self._llm.summarize(candidate.title, candidate.abstract)
                tags = await self._llm.generate_tags(candidate.title, candidate.abstract)

            # Stage 5b: Compute scores
            recency = self._ranker.compute_recency_score(candidate.publication_date)

            # Stage 5c: Persist
            paper = await self._paper_repo.create(
                title=candidate.title,
                title_normalized=DeduplicationService._normalize_title(candidate.title),
                abstract=candidate.abstract,
                summary=summary,
                authors=candidate.authors,
                publication_date=candidate.publication_date,
                source=candidate.source,
                source_url=candidate.source_url,
                arxiv_id=candidate.arxiv_id,
                recency_score=recency,
                relevance_score=recency,
                enriched_at=datetime.now(timezone.utc) if summary else None,
            )

            for tag_name in tags:
                tag = await self._tag_repo.get_or_create(tag_name)
                await self._paper_repo.add_tag(paper.id, tag.id)

            await self._researcher_repo.link_paper(researcher_id, paper.id)
            stored += 1

        await self._paper_repo.commit()
        _logger.info(
            "Scrape done for researcher_id=%d: stored=%d skipped=%d",
            researcher_id, stored, skipped,
        )
        return {"stored": stored, "skipped": skipped, "total": len(candidates)}
```

---

## 15. Configuration Strategy

New fields added to `app/config.py` (`Settings` class):

```python
# Scraper tuning
scraper_scholar_delay: float = Field(3.0, alias="SCRAPER_SCHOLAR_DELAY")
scraper_scholar_max_pages: int = Field(3, alias="SCRAPER_SCHOLAR_MAX_PAGES")
scraper_scholar_headless: bool = Field(True, alias="SCRAPER_SCHOLAR_HEADLESS")
scraper_arxiv_delay: float = Field(1.0, alias="SCRAPER_ARXIV_DELAY")
scraper_max_results: int = Field(20, alias="SCRAPER_MAX_RESULTS")
scraper_since_days: int = Field(365, alias="SCRAPER_SINCE_DAYS")
scraper_recency_half_life: int = Field(180, alias="SCRAPER_RECENCY_HALF_LIFE")

# Dedicated LLM enrichment model (independent of chat model)
llm_enrichment_model: str = Field("gemma4:26b", alias="LLM_ENRICHMENT_MODEL")
```

---

## 16. Error Handling, Retries, and Observability

### Error classification (extends existing `task_runner.py` pattern)

| Error | Behavior |
|---|---|
| Google Scholar CAPTCHA / block | Retry with exponential backoff (Celery `retry()`). Log warning. |
| Scholar HTML structure change | `_parse_results_page` returns empty list; logged as zero results; alert. |
| ArXiv API 429 (rate limit) | Retry after `Retry-After` header or 30s default. |
| ArXiv API 5xx | Retry up to 3 times with 60s delay. |
| ArXiv paper not found | Return original candidate unchanged; stored without full abstract. |
| LLM timeout (Ollama overloaded) | Retry up to 3 times. Paper stored with `enriched_at=NULL`; retried next run. |
| LLM returns unparseable tags | Log warning, store empty tags. Paper marked `enriched_at` set (do not retry). |
| Playwright crash / timeout | Retry entire researcher scrape. Browser recreated per task. |
| DB `IntegrityError` on duplicate | Catch, treat as dedup hit, merge metadata, link researcher. |

### Log events per task

| Event | Fields |
|---|---|
| `scraper.start` | `researcher_id`, `researcher_name`, `chair_id` |
| `scraper.scholar_results` | `count`, `researcher_name` |
| `scraper.paper_enriched` | `arxiv_id`, `abstract_len` |
| `scraper.paper_stored` | `paper_id`, `title`, `tags` |
| `scraper.paper_skipped` | `title`, `dedup_tier` (arxiv/doi/title) |
| `scraper.complete` | `stored`, `skipped`, `errors`, `duration_ms` |

The existing `jobs` table (from `architecture_refactoring`) provides full lifecycle tracking visible at `GET /api/jobs`.

---

## 17. Testing Strategy

```
backend/tests/
├── unit/
│   ├── scraper/
│   │   ├── test_dedup.py               # DeduplicationService with mock PaperRepository
│   │   ├── test_ranker.py              # RecencyPaperRanker: exact score values, edge cases
│   │   ├── test_llm_enricher.py        # Mock LLMPort: verify prompt content, tag parsing
│   │   ├── test_tag_normalization.py   # Fuzzy matching, canonical set, JSON fallback
│   │   ├── test_arxiv_client.py        # Mock httpx: parse fixture XML, missing fields
│   │   ├── test_orchestrator.py        # Full pipeline with all adapters mocked
│   │   └── test_scholar_parser.py      # Parse mock HTML fixtures, extract papers
│   ├── papers/
│   │   ├── test_paper_service.py       # List, filter by tag/chair, ordering
│   │   └── test_paper_repository.py    # SQL queries with mock session
│   └── researchers/
│       └── test_researcher_service.py  # Auto-create from chair, link paper
│
├── integration/
│   ├── conftest.py                     # Real test DB, factory fixtures
│   ├── test_scraper_pipeline.py        # Full pipeline, mocked external HTTP + Playwright
│   └── test_paper_crud.py              # Real DB: create, dedup, merge
│
└── fixtures/
    ├── arxiv_response.xml              # Sample arXiv Atom feed
    ├── scholar_results.html            # Sample Google Scholar HTML
    └── llm_responses.json              # Sample LLM outputs (good + malformed)
```

### Key test patterns

- **Ranker tests:** Parameterized with known publication dates; assert exact score within tolerance
- **Dedup tests:** Test all 3 tiers independently; test merge behavior on partial duplicate
- **LLM enricher tests:** Assert prompt contains both title and abstract; verify fallback for non-JSON output; verify fuzzy tag matching
- **Scholar parser tests:** Load fixture HTML; verify author parsing, year extraction, arxiv_id extraction from URLs
- **Integration tests:** Use a test PostgreSQL container; mock `httpx` and `Playwright`; run full orchestrator; assert DB state

---

## 18. MVP Roadmap

### Phase 1 — Foundation (Week 1)
- [ ] Rebase `feat/arxiv_scraper` onto `architecture_refactoring`
- [ ] Create migration `0010_papers_researchers.py` (papers, researchers, tags, junction tables)
- [ ] Implement `Paper`, `Tag`, `Researcher` SQLAlchemy models
- [ ] Implement `PaperRepository`, `ResearcherRepository`, `TagRepository`
- [ ] Implement `DeduplicationService`
- [ ] Implement `RecencyPaperRanker`
- [ ] Seed canonical tags

### Phase 2 — Adapters (Week 2)
- [ ] Implement `ArxivMetadataEnricher` (extend existing `_fetch_arxiv_metadata`)
- [ ] Implement `LLMPaperEnricher` with tag normalization and fuzzy matching
- [ ] Implement `ScholarPlaywrightScraper`
- [ ] Add `playwright` + `thefuzz` to `pyproject.toml`; install Chromium in dev/CI

### Phase 3 — Orchestration + Tasks (Week 3)
- [ ] Implement `ScraperOrchestrator`
- [ ] Implement Celery tasks: `scrape_chair_papers`, `scrape_researcher_papers`, `enrich_paper`
- [ ] Add scraper config fields to `Settings`
- [ ] Add API endpoints: `POST /api/scraper/run/{chair_id}`, `GET /api/papers`
- [ ] Wire dependency injection

### Phase 4 — Testing + Polish (Week 4)
- [ ] Write unit tests for all adapters and services
- [ ] Write integration tests with test DB
- [ ] Add structured logging throughout pipeline
- [ ] Frontend: replace mock papers in Chat sidebar with real `GET /api/papers` data
- [ ] Manual end-to-end test with a real chair

---

## 19. Production Roadmap

### Phase 5 — Scheduling & Scale
- [ ] Add Celery Beat schedule for periodic scraping (e.g., weekly per chair)
- [ ] Add `scrape_all_chairs` fan-out task
- [ ] Nightly `recompute_scores` task (recency decays continuously)
- [ ] Store abstract embeddings for semantic search over papers

### Phase 6 — Additional Sources
- [ ] Implement `SemanticScholarClient` (`PaperSourceClient` interface — better author disambiguation)
- [ ] Implement `DBLPClient`
- [ ] Source priority and cross-source dedup logic

### Phase 7 — Researcher Discovery
- [ ] Implement `PlaywrightDiscoveryClient` for chair team pages
- [ ] Admin UI: trigger discovery, review/approve found researchers
- [ ] ORCID integration for unambiguous author matching

### Phase 8 — Advanced Ranking
- [ ] Citation count weighting (from Scholar / Semantic Scholar)
- [ ] Embedding cosine similarity to chair description
- [ ] Student-personalized relevance (cosine similarity to student profile embedding)

---

## 20. Risks and Tradeoffs

| Risk | Impact | Mitigation |
|---|---|---|
| **Google Scholar blocking** | Cannot discover papers | 3s delay, headless browser fingerprint randomization, rotate user-agents. Fallback: manual arxiv_id entry (existing feature). Long-term: Semantic Scholar as alternative source. |
| **Scholar HTML structure changes** | Parser silently returns zero results | Fixture-based regression tests. Alert on zero-result scrape. Isolate parsing in one method for easy patching. |
| **LLM tag inconsistency** | Tags drift from canonical set | Closed-vocabulary prompt + fuzzy matching + canonical `tags` table. Admin review queue for unmapped tags. |
| **Playwright in Celery workers** | Memory accumulation over many tasks | Create and destroy browser per task. Set `worker_max_tasks_per_child=10`. Consider a dedicated scraper worker process pool. |
| **ArXiv rate limits** | Slow batch enrichment | arXiv allows ~1 req/3s. Batch up to 100 IDs per API call to amortize. Add `Retry-After` header handling. |
| **Embedding dimension (2560)** | No HNSW index; exact scan is O(n) | Acceptable at research scale (<100k papers). Future: dimensionality reduction or switch embedding model. |
| **Dedup false negatives** | Duplicate papers stored | Multi-tier matching + DB unique constraint as backstop. Periodic dedup sweep maintenance task. |
| **Playwright binary size** | ~200MB Chromium per environment | `playwright install --with-deps chromium` only. Consider a dedicated scraper Docker service. |
| **Google Scholar ToS** | Legal/policy risk | Playwright scraping is for academic research use only. Evaluate SerpApi or Semantic Scholar if ToS concerns arise. |
