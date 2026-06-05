"""Abstract base classes (interfaces) for the scraper pipeline.

Each infrastructure adapter implements one of these ABCs, keeping the
orchestrator independent of any concrete scraping library or LLM provider.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from app.papers.domain import EnrichedPaper, PaperCandidate, ResearcherInfo


class PaperSourceClient(ABC):
    """Discovers and returns raw paper candidates for a researcher."""

    @abstractmethod
    async def fetch_papers(
        self,
        researcher: ResearcherInfo,
        *,
        max_results: int = 20,
        since_days: int = 365,
    ) -> list[PaperCandidate]:
        """Return recent papers for *researcher*, up to *max_results*."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Release any held resources (browsers, HTTP pools, etc.)."""
        ...


class PaperMetadataEnricher(ABC):
    """Fetches richer metadata for a candidate from an authoritative source."""

    @abstractmethod
    async def enrich(self, paper: PaperCandidate) -> PaperCandidate:
        """Return the candidate with abstract, exact date, canonical IDs filled in."""
        ...

    @abstractmethod
    async def enrich_many(self, papers: list[PaperCandidate]) -> list[PaperCandidate]:
        """Return candidates with metadata filled in where available."""
        ...


class ResearcherDiscoveryClient(ABC):
    """Discovers team members / researchers from a chair website. (Phase 2)"""

    @abstractmethod
    async def discover_researchers(self, chair_website_url: str) -> list[ResearcherInfo]:
        """Scrape the chair website and return researcher profiles."""
        ...


class LLMEnricher(ABC):
    """Generates LLM-powered summaries and tags for a paper."""

    @abstractmethod
    async def summarize(self, title: str, abstract: str) -> str:
        """Return a 2-3 sentence plain-language summary."""
        ...

    @abstractmethod
    async def generate_tags(self, title: str, abstract: str) -> list[str]:
        """Return 2-5 canonical lowercase tag strings."""
        ...


class PaperRanker(ABC):
    """Computes recency and relevance scores for a paper."""

    @abstractmethod
    def compute_recency_score(self, publication_date: datetime | None) -> float:
        """Return a [0, 1] score; 1.0 = very recent, decays over time."""
        ...

    @abstractmethod
    def compute_relevance_score(self, paper: EnrichedPaper) -> float:
        """Return a composite relevance score (MVP: mirrors recency_score)."""
        ...
