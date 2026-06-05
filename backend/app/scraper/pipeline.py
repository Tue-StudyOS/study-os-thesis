"""Factories for scraper pipeline dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.llm.factory import build_chat_client
from app.papers.dedup import DeduplicationService
from app.papers.repository import PaperRepository, TagRepository
from app.researchers.repository import ResearcherRepository
from app.scraper.adapters.llm_enricher import LLMPaperEnricher
from app.scraper.adapters.openalex_client import OpenAlexSourceClient
from app.scraper.adapters.ranker import RecencyPaperRanker
from app.scraper.orchestrator import ScraperOrchestrator


@dataclass(slots=True)
class ScraperPipeline:
    orchestrator: ScraperOrchestrator
    source: OpenAlexSourceClient


def build_scraper_pipeline(
    session: AsyncSession,
    settings: Settings,
    *,
    max_results: int | None = None,
    since_days: int | None = None,
) -> ScraperPipeline:
    source = OpenAlexSourceClient()
    paper_repo = PaperRepository(session)
    tag_repo = TagRepository(session)
    researcher_repo = ResearcherRepository(session)
    orchestrator = ScraperOrchestrator(
        source=source,
        llm_enricher=LLMPaperEnricher(build_chat_client(settings), settings.effective_enrichment_model),
        ranker=RecencyPaperRanker(half_life_days=settings.scraper_recency_half_life),
        dedup=DeduplicationService(paper_repo),
        paper_repo=paper_repo,
        tag_repo=tag_repo,
        researcher_repo=researcher_repo,
        max_results=max_results or settings.scraper_max_results,
        since_days=since_days or settings.scraper_since_days,
    )
    return ScraperPipeline(orchestrator=orchestrator, source=source)
