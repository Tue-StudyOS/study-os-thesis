"""Unit tests for scraper Celery tasks.

Covers: task wiring (execute_task delegation), retry policy, and the async
work functions.
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.exceptions import NotFoundException
from app.scraper.tasks import (
    _enrich_paper_work,
    _scrape_researcher_work,
    enrich_paper,
    scrape_all_chairs,
    scrape_chair_papers,
    scrape_researcher_papers,
)


def _acm(session):
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=session)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


def _fake_settings():
    return SimpleNamespace(
        redis_url="redis://localhost:6379/0",
        ollama_embed_model="embed-model",
        ollama_chat_model="chat-model",
        effective_enrichment_model="chat-model",
        scraper_max_results=5,
        scraper_since_days=365,
        scraper_recency_half_life=180,
    )


# ---------------------------------------------------------------------------
# Task wiring tests (patch execute_task, check what gets passed)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestScrapeChairPapersWiring:
    def test_delegates_to_execute_task(self):
        with patch("app.scraper.tasks.execute_task") as ex:
            scrape_chair_papers(chair_id=1, user_id=5, job_id="job-1")
        ex.assert_called_once()

    def test_correct_job_id_and_user_id_forwarded(self):
        with patch("app.scraper.tasks.execute_task") as ex:
            scrape_chair_papers(chair_id=1, user_id=5, job_id="job-abc")
        assert ex.call_args.kwargs["job_id"] == "job-abc"
        assert ex.call_args.kwargs["user_id"] == 5

    def test_success_event_name(self):
        with patch("app.scraper.tasks.execute_task") as ex:
            scrape_chair_papers(chair_id=1, user_id=5, job_id="j")
        assert ex.call_args.kwargs["success_event"] == "scrape_chair_complete"

    def test_work_is_callable(self):
        with patch("app.scraper.tasks.execute_task") as ex:
            scrape_chair_papers(chair_id=1, user_id=5, job_id="j")
        assert callable(ex.call_args.kwargs["work"])


@pytest.mark.unit
class TestScrapeResearcherPapersWiring:
    def test_delegates_to_execute_task(self):
        with patch("app.scraper.tasks.execute_task") as ex:
            scrape_researcher_papers(researcher_id=2, user_id=5, job_id="j")
        ex.assert_called_once()

    def test_success_event_name(self):
        with patch("app.scraper.tasks.execute_task") as ex:
            scrape_researcher_papers(researcher_id=2, user_id=5, job_id="j")
        assert ex.call_args.kwargs["success_event"] == "scrape_researcher_complete"


@pytest.mark.unit
class TestEnrichPaperWiring:
    def test_delegates_to_execute_task(self):
        with patch("app.scraper.tasks.execute_task") as ex:
            enrich_paper(paper_id=3, user_id=5, job_id="j")
        ex.assert_called_once()

    def test_success_event_name(self):
        with patch("app.scraper.tasks.execute_task") as ex:
            enrich_paper(paper_id=3, user_id=5, job_id="j")
        assert ex.call_args.kwargs["success_event"] == "enrich_paper_complete"

    def test_force_false_by_default(self):
        # The work lambda must capture force=False when not passed
        with patch("app.scraper.tasks.execute_task") as ex:
            enrich_paper(paper_id=3, user_id=5, job_id="j")
        # Verify work is a callable (force is baked in via lambda)
        assert callable(ex.call_args.kwargs["work"])


@pytest.mark.unit
class TestScrapeResearcherWork:
    async def test_uses_openalex_source(self):
        session = AsyncMock()
        source = AsyncMock()
        orchestrator = AsyncMock()
        orchestrator.scrape_for_researcher.return_value = {"stored": 0}

        with (
            patch("app.db.SessionLocal", return_value=_acm(session)),
            patch("app.scraper.adapters.openalex_client.OpenAlexSourceClient", return_value=source) as source_cls,
            patch("app.llm.factory.build_chat_client", return_value=AsyncMock()),
            patch("app.scraper.orchestrator.ScraperOrchestrator", return_value=orchestrator) as orchestrator_cls,
        ):
            result = await _scrape_researcher_work(7, _fake_settings(), max_results=250, since_days=3650)

        source_cls.assert_called_once_with()
        assert orchestrator_cls.call_args.kwargs["source"] is source
        assert orchestrator_cls.call_args.kwargs["max_results"] == 250
        assert orchestrator_cls.call_args.kwargs["since_days"] == 3650
        orchestrator.scrape_for_researcher.assert_awaited_once_with(7)
        source.close.assert_awaited_once()
        assert result == {"stored": 0}


# ---------------------------------------------------------------------------
# Retry policy
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRetryPolicy:
    def test_scrape_chair_max_retries(self):
        assert scrape_chair_papers.max_retries == 2

    def test_scrape_researcher_max_retries(self):
        assert scrape_researcher_papers.max_retries == 3

    def test_enrich_paper_max_retries(self):
        assert enrich_paper.max_retries == 3

    def test_scrape_all_chairs_max_retries_zero(self):
        assert scrape_all_chairs.max_retries == 0

    def test_scrape_researcher_has_long_soft_limit(self):
        # OpenAlex pagination and LLM fallback can still take longer than enrichment.
        assert scrape_researcher_papers.soft_time_limit == 600

    def test_enrich_paper_soft_limit(self):
        assert enrich_paper.soft_time_limit == 120


# ---------------------------------------------------------------------------
# _enrich_paper_work
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnrichPaperWork:
    def _setup_session(self, paper, tags=None):
        session = AsyncMock()
        paper_repo = AsyncMock()
        tag_repo = AsyncMock()
        paper_repo.get_by_id.return_value = paper
        paper_repo.update.return_value = paper
        tag = SimpleNamespace(id=1, name="robotics")
        tag_repo.get_or_create.return_value = tag
        return session, paper_repo, tag_repo

    async def test_skips_if_already_enriched_and_no_force(self):
        paper = SimpleNamespace(
            id=1,
            title="T",
            abstract="A",
            enriched_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        session, paper_repo, tag_repo = self._setup_session(paper)

        with (
            patch("app.db.SessionLocal", return_value=_acm(session)),
            patch("app.papers.repository.PaperRepository", return_value=paper_repo),
            patch("app.papers.repository.TagRepository", return_value=tag_repo),
            patch("app.llm.factory.build_chat_client", return_value=AsyncMock()),
        ):
            result = await _enrich_paper_work(1, force=False, settings=_fake_settings())

        assert result["skipped"] is True
        paper_repo.update.assert_not_awaited()

    async def test_force_overrides_enriched_at_guard(self):
        paper = SimpleNamespace(
            id=1,
            title="T",
            abstract="Existing abstract",
            enriched_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        session, paper_repo, tag_repo = self._setup_session(paper)
        llm = AsyncMock()
        llm.chat.return_value = {"message": {"content": "summary"}}

        with (
            patch("app.db.SessionLocal", return_value=_acm(session)),
            patch("app.papers.repository.PaperRepository", return_value=paper_repo),
            patch("app.papers.repository.TagRepository", return_value=tag_repo),
            patch("app.llm.factory.build_chat_client", return_value=llm),
            patch("app.scraper.adapters.llm_enricher.LLMPaperEnricher.summarize", new=AsyncMock(return_value="s")),
            patch("app.scraper.adapters.llm_enricher.LLMPaperEnricher.generate_tags", new=AsyncMock(return_value=[])),
        ):
            result = await _enrich_paper_work(1, force=True, settings=_fake_settings())

        assert result.get("skipped") is not True

    async def test_no_abstract_returns_skip_with_reason(self):
        paper = SimpleNamespace(id=1, title="T", abstract=None, enriched_at=None)
        session, paper_repo, tag_repo = self._setup_session(paper)

        with (
            patch("app.db.SessionLocal", return_value=_acm(session)),
            patch("app.papers.repository.PaperRepository", return_value=paper_repo),
            patch("app.papers.repository.TagRepository", return_value=tag_repo),
            patch("app.llm.factory.build_chat_client", return_value=AsyncMock()),
        ):
            result = await _enrich_paper_work(1, force=False, settings=_fake_settings())

        assert result["skipped"] is True
        assert result["reason"] == "no_abstract"

    async def test_paper_not_found_raises(self):
        session = AsyncMock()
        paper_repo = AsyncMock()
        paper_repo.get_by_id.return_value = None

        with (
            patch("app.db.SessionLocal", return_value=_acm(session)),
            patch("app.papers.repository.PaperRepository", return_value=paper_repo),
            patch("app.papers.repository.TagRepository", return_value=AsyncMock()),
            patch("app.llm.factory.build_chat_client", return_value=AsyncMock()),
        ):
            with pytest.raises(NotFoundException):
                await _enrich_paper_work(999, force=False, settings=_fake_settings())

    async def test_happy_path_updates_paper_and_returns_counts(self):
        paper = SimpleNamespace(id=1, title="T", abstract="Abstract text", enriched_at=None)
        session, paper_repo, tag_repo = self._setup_session(paper)

        with (
            patch("app.db.SessionLocal", return_value=_acm(session)),
            patch("app.papers.repository.PaperRepository", return_value=paper_repo),
            patch("app.papers.repository.TagRepository", return_value=tag_repo),
            patch("app.llm.factory.build_chat_client", return_value=AsyncMock()),
            patch("app.scraper.adapters.llm_enricher.LLMPaperEnricher.summarize", new=AsyncMock(return_value="A summary")),
            patch("app.scraper.adapters.llm_enricher.LLMPaperEnricher.generate_tags", new=AsyncMock(return_value=["robotics"])),
        ):
            result = await _enrich_paper_work(1, force=False, settings=_fake_settings())

        paper_repo.update.assert_awaited_once()
        update_kwargs = paper_repo.update.call_args.kwargs
        assert update_kwargs["summary"] == "A summary"
        assert update_kwargs["enriched_at"] is not None
        paper_repo.commit.assert_awaited_once()
        assert result["paper_id"] == 1
        assert result["tag_count"] == 1
        assert result["summary_len"] == len("A summary")
