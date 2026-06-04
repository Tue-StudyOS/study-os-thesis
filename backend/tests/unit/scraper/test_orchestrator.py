"""Unit tests for ScraperOrchestrator.

All external adapters are mocked. Concurrency behaviour is verified by
recording call ordering and counts, not by timing.
"""

import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.papers.domain import PaperCandidate
from app.scraper.orchestrator import ScraperOrchestrator, _ARXIV_CONCURRENCY, _LLM_CONCURRENCY


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _researcher(id_=1, name="Georg Martius", chair_id=1, scholar_id="ABC123"):
    return SimpleNamespace(
        id=id_,
        name=name,
        chair_id=chair_id,
        google_scholar_id=scholar_id,
        orcid=None,
        affiliation=None,
    )


def _candidate(title="Paper A", arxiv_id=None, abstract="Abstract text", year=2023):
    return PaperCandidate(
        title=title,
        abstract=abstract,
        authors=["Alice", "Bob"],
        publication_date=datetime(year, 6, 1, tzinfo=timezone.utc),
        source="google_scholar",
        source_url="https://scholar.google.com/test",
        arxiv_id=arxiv_id,
    )


def _paper_row(id_=99, **kwargs):
    defaults = dict(arxiv_id=None, tags=[])
    defaults.update(kwargs)
    return SimpleNamespace(id=id_, **defaults)


def _build_orchestrator(**overrides):
    defaults = dict(
        source=AsyncMock(),
        arxiv_enricher=AsyncMock(),
        llm_enricher=AsyncMock(),
        ranker=MagicMock(),
        dedup=AsyncMock(),
        paper_repo=AsyncMock(),
        tag_repo=AsyncMock(),
        researcher_repo=AsyncMock(),
        max_results=20,
        since_days=365,
    )
    defaults.update(overrides)

    o = ScraperOrchestrator(**defaults)

    # Sensible defaults
    o._source.fetch_papers.return_value = []

    async def _identity(p):
        return p

    o._arxiv.enrich.side_effect = _identity
    o._llm.summarize.return_value = "A short summary."
    o._llm.generate_tags.return_value = ["machine learning"]
    o._ranker.compute_recency_score.return_value = 0.8
    o._dedup.find_duplicate.return_value = None
    o._dedup.merge_metadata.return_value = AsyncMock()
    o._paper_repo.create.return_value = _paper_row()
    o._tag_repo.get_or_create.return_value = SimpleNamespace(id=1, name="machine learning")
    o._researcher_repo.get_by_id.return_value = _researcher()
    o._researcher_repo.list_by_chair.return_value = []

    return o


# ---------------------------------------------------------------------------
# ensure_researchers_for_chair
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnsureResearchers:
    async def test_returns_existing_ids_without_creating(self):
        o = _build_orchestrator()
        r1 = SimpleNamespace(id=1, name="Prof A")
        r2 = SimpleNamespace(id=2, name="Dr B")
        o._researcher_repo.list_by_chair.return_value = [r1, r2]

        ids = await o.ensure_researchers_for_chair(chair_id=1, professor_name="A")

        assert ids == [1, 2]
        o._researcher_repo.create.assert_not_awaited()

    async def test_auto_creates_from_professor_name_when_empty(self):
        o = _build_orchestrator()
        o._researcher_repo.list_by_chair.return_value = []
        new_researcher = SimpleNamespace(id=7, name="Georg Martius")
        o._researcher_repo.create.return_value = new_researcher

        ids = await o.ensure_researchers_for_chair(chair_id=1, professor_name="Georg Martius")

        assert ids == [7]
        o._researcher_repo.create.assert_awaited_once()
        call_kwargs = o._researcher_repo.create.call_args.kwargs
        assert call_kwargs["name"] == "Georg Martius"
        assert call_kwargs["is_professor"] is True
        assert call_kwargs["chair_id"] == 1

    async def test_commits_after_auto_creation(self):
        o = _build_orchestrator()
        o._researcher_repo.list_by_chair.return_value = []
        o._researcher_repo.create.return_value = SimpleNamespace(id=3, name="P")

        await o.ensure_researchers_for_chair(1, "P")

        o._researcher_repo.commit.assert_awaited()


# ---------------------------------------------------------------------------
# scrape_for_researcher — core pipeline
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestScrapeForResearcher:
    async def test_researcher_not_found_raises(self):
        o = _build_orchestrator()
        o._researcher_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="1"):
            await o.scrape_for_researcher(1)

    async def test_two_new_papers_stored(self):
        o = _build_orchestrator()
        candidates = [_candidate("Paper A"), _candidate("Paper B")]
        o._source.fetch_papers.return_value = candidates
        paper_ids = iter([_paper_row(1), _paper_row(2)])
        o._paper_repo.create.side_effect = lambda **kw: next(paper_ids)

        result = await o.scrape_for_researcher(1)

        assert result["stored"] == 2
        assert result["skipped"] == 0
        assert result["errors"] == 0
        assert o._paper_repo.create.await_count == 2

    async def test_duplicate_paper_skipped_and_merged(self):
        o = _build_orchestrator()
        existing = _paper_row(42)
        o._source.fetch_papers.return_value = [_candidate("Paper A")]
        o._dedup.find_duplicate.return_value = existing

        result = await o.scrape_for_researcher(1)

        assert result["stored"] == 0
        assert result["skipped"] == 1
        o._paper_repo.create.assert_not_awaited()
        # merge_metadata was called with the existing paper as first arg
        assert o._dedup.merge_metadata.await_count == 1
        assert o._dedup.merge_metadata.call_args[0][0] is existing
        o._researcher_repo.link_paper.assert_awaited()

    async def test_no_abstract_skips_llm_enrichment(self):
        o = _build_orchestrator()
        candidate = _candidate(abstract=None)
        o._source.fetch_papers.return_value = [candidate]

        await o.scrape_for_researcher(1)

        o._llm.summarize.assert_not_awaited()
        o._llm.generate_tags.assert_not_awaited()
        # Verify enriched_at is None in the create call
        create_kwargs = o._paper_repo.create.call_args.kwargs
        assert create_kwargs["enriched_at"] is None

    async def test_abstract_present_triggers_llm(self):
        o = _build_orchestrator()
        o._source.fetch_papers.return_value = [_candidate(abstract="Some abstract")]

        await o.scrape_for_researcher(1)

        o._llm.summarize.assert_awaited_once()
        o._llm.generate_tags.assert_awaited_once()
        create_kwargs = o._paper_repo.create.call_args.kwargs
        assert create_kwargs["summary"] == "A short summary."
        assert create_kwargs["enriched_at"] is not None

    async def test_tags_stored_for_each_tag(self):
        o = _build_orchestrator()
        o._source.fetch_papers.return_value = [_candidate()]
        o._llm.generate_tags.return_value = ["robotics", "optimization"]
        tag1 = SimpleNamespace(id=1, name="robotics")
        tag2 = SimpleNamespace(id=2, name="optimization")
        o._tag_repo.get_or_create.side_effect = [tag1, tag2]

        await o.scrape_for_researcher(1)

        assert o._tag_repo.get_or_create.await_count == 2
        assert o._paper_repo.add_tag.await_count == 2

    async def test_candidate_exception_counted_as_error(self):
        o = _build_orchestrator()
        o._source.fetch_papers.return_value = [_candidate("Bad"), _candidate("Good")]
        # First enrich raises, second succeeds
        call_count = 0

        async def enrich_side_effect(paper):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("arXiv down")
            return paper

        o._arxiv.enrich.side_effect = enrich_side_effect

        result = await o.scrape_for_researcher(1)

        assert result["errors"] == 1
        assert result["stored"] == 1  # second paper still processed

    async def test_commit_called_once_at_end(self):
        o = _build_orchestrator()
        o._source.fetch_papers.return_value = [_candidate("A"), _candidate("B")]

        await o.scrape_for_researcher(1)

        o._paper_repo.commit.assert_awaited_once()

    async def test_researcher_linked_to_stored_paper(self):
        o = _build_orchestrator()
        o._source.fetch_papers.return_value = [_candidate()]
        o._paper_repo.create.return_value = _paper_row(id_=55)

        await o.scrape_for_researcher(researcher_id=1)

        o._researcher_repo.link_paper.assert_awaited_with(1, 55)

    async def test_result_contains_researcher_info(self):
        o = _build_orchestrator()
        o._source.fetch_papers.return_value = []

        result = await o.scrape_for_researcher(1)

        assert result["researcher_id"] == 1
        assert result["researcher_name"] == "Georg Martius"
        assert result["total"] == 0

    async def test_empty_candidate_list_returns_zeros(self):
        o = _build_orchestrator()
        o._source.fetch_papers.return_value = []

        result = await o.scrape_for_researcher(1)

        assert result == {
            "researcher_id": 1,
            "researcher_name": "Georg Martius",
            "total": 0,
            "stored": 0,
            "skipped": 0,
            "errors": 0,
        }


# ---------------------------------------------------------------------------
# Concurrency behaviour
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestConcurrency:
    async def test_all_candidates_processed(self):
        """Verify all candidates still pass through arXiv enrichment."""
        o = _build_orchestrator()
        n = 10
        candidates = [_candidate(f"Paper {i}") for i in range(n)]
        o._source.fetch_papers.return_value = candidates

        await o.scrape_for_researcher(1)

        assert o._arxiv.enrich.await_count == n

    async def test_arxiv_enrichment_is_parallel_but_bounded(self):
        """Network enrichment may overlap, up to the configured cap."""
        o = _build_orchestrator()
        n = _ARXIV_CONCURRENCY * 3
        candidates = [_candidate(f"P{i}") for i in range(n)]
        o._source.fetch_papers.return_value = candidates

        max_concurrent = 0
        current = 0

        async def counting_enrich(paper):
            nonlocal max_concurrent, current
            current += 1
            max_concurrent = max(max_concurrent, current)
            await asyncio.sleep(0)
            current -= 1
            return paper

        o._arxiv.enrich.side_effect = counting_enrich

        await o.scrape_for_researcher(1)

        assert max_concurrent <= _ARXIV_CONCURRENCY
        assert max_concurrent > 1

    async def test_llm_calls_are_sequential(self):
        """LLM calls must never overlap."""
        o = _build_orchestrator()
        n = 5
        candidates = [_candidate(f"P{i}", abstract=f"Abstract {i}") for i in range(n)]
        o._source.fetch_papers.return_value = candidates

        max_concurrent_llm = 0
        current_llm = 0

        async def counting_summarize(title, abstract):
            nonlocal max_concurrent_llm, current_llm
            current_llm += 1
            max_concurrent_llm = max(max_concurrent_llm, current_llm)
            await asyncio.sleep(0)
            current_llm -= 1
            return "summary"

        o._llm.summarize.side_effect = counting_summarize
        o._llm.generate_tags.return_value = []

        await o.scrape_for_researcher(1)

        assert max_concurrent_llm == _LLM_CONCURRENCY  # always exactly 1

    async def test_db_creates_are_sequential(self):
        """Repository writes must not overlap on the shared AsyncSession."""
        o = _build_orchestrator()
        n = 8
        candidates = [_candidate(f"P{i}", abstract=None) for i in range(n)]
        o._source.fetch_papers.return_value = candidates

        max_concurrent_create = 0
        current_create = 0
        ids = iter(range(1, n + 1))

        async def counting_create(**kwargs):
            nonlocal max_concurrent_create, current_create
            current_create += 1
            max_concurrent_create = max(max_concurrent_create, current_create)
            await asyncio.sleep(0)
            current_create -= 1
            return _paper_row(id_=next(ids))

        o._paper_repo.create.side_effect = counting_create

        result = await o.scrape_for_researcher(1)

        assert result["stored"] == n
        assert max_concurrent_create == 1

    async def test_n_papers_all_stored(self):
        """Correctness check: processing 8 papers stores exactly 8."""
        o = _build_orchestrator()
        n = 8
        candidates = [_candidate(f"P{i}") for i in range(n)]
        o._source.fetch_papers.return_value = candidates
        ids = iter(range(1, n + 1))
        o._paper_repo.create.side_effect = lambda **kw: _paper_row(id_=next(ids))

        result = await o.scrape_for_researcher(1)

        assert result["stored"] == n
        assert o._paper_repo.create.await_count == n

    async def test_errors_do_not_cancel_later_candidates(self):
        """One failing candidate must not prevent others from completing."""
        o = _build_orchestrator()
        n = 6
        candidates = [_candidate(f"P{i}") for i in range(n)]
        o._source.fetch_papers.return_value = candidates

        call_count = 0

        async def sometimes_fail(paper):
            nonlocal call_count
            call_count += 1
            if call_count % 3 == 0:  # fail every 3rd paper
                raise ConnectionError("timeout")
            return paper

        o._arxiv.enrich.side_effect = sometimes_fail

        result = await o.scrape_for_researcher(1)

        # 2 out of 6 fail (indices 3, 6), 4 succeed
        assert result["errors"] == 2
        assert result["stored"] == 4
