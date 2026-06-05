"""Unit tests for scraper pipeline dependency factories."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.scraper.pipeline import build_scraper_pipeline


def _settings():
    return SimpleNamespace(
        effective_enrichment_model="chat-model",
        scraper_max_results=25,
        scraper_since_days=3650,
        scraper_recency_half_life=180,
    )


@pytest.mark.unit
def test_build_scraper_pipeline_wires_openalex_only_dependencies():
    session = AsyncMock()
    settings = _settings()
    source = AsyncMock()
    orchestrator = AsyncMock()

    with (
        patch("app.scraper.pipeline.OpenAlexSourceClient", return_value=source) as source_cls,
        patch("app.scraper.pipeline.build_chat_client", return_value=AsyncMock()) as chat_factory,
        patch("app.scraper.pipeline.ScraperOrchestrator", return_value=orchestrator) as orchestrator_cls,
    ):
        pipeline = build_scraper_pipeline(session, settings, max_results=250, since_days=365)

    source_cls.assert_called_once_with()
    chat_factory.assert_called_once_with(settings)
    assert pipeline.source is source
    assert pipeline.orchestrator is orchestrator
    assert orchestrator_cls.call_args.kwargs["source"] is source
    assert orchestrator_cls.call_args.kwargs["max_results"] == 250
    assert orchestrator_cls.call_args.kwargs["since_days"] == 365
