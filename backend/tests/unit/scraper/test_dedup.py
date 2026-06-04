"""Unit tests for DeduplicationService."""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.papers.dedup import DeduplicationService
from app.papers.domain import PaperCandidate


def _make_paper(**kwargs):
    defaults = dict(
        id=1,
        title="Some Paper",
        title_normalized="some paper",
        arxiv_id=None,
        doi=None,
        abstract=None,
        authors=[],
        publication_date=None,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def _make_candidate(**kwargs):
    defaults = dict(
        title="Some Paper",
        source="google_scholar",
        source_url="https://example.com",
        arxiv_id=None,
        doi=None,
        abstract=None,
        authors=[],
        publication_date=None,
    )
    defaults.update(kwargs)
    return PaperCandidate(**defaults)


@pytest.mark.unit
class TestNormalizeTitle:
    @pytest.mark.parametrize("raw,expected", [
        ("  Hello, World!  ", "hello world"),
        ("UPPER CASE", "upper case"),
        ("multiple   spaces", "multiple spaces"),
        ("Punctuation: (test) [here]", "punctuation test here"),
        ("A Learning-Based Approach", "a learningbased approach"),
        ("", ""),
        ("already normalized", "already normalized"),
    ])
    def test_normalize(self, raw, expected):
        assert DeduplicationService.normalize_title(raw) == expected

    def test_en_dash_stripped(self):
        # Real-world: paper titles with em/en dashes
        result = DeduplicationService.normalize_title("Model\u2013Based RL")
        assert "\u2013" not in result

    def test_idempotent(self):
        title = "Deep Learning for Robotics"
        once = DeduplicationService.normalize_title(title)
        twice = DeduplicationService.normalize_title(once)
        assert once == twice


@pytest.mark.unit
class TestFindDuplicate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = AsyncMock()
        self.svc = DeduplicationService(self.repo)

    async def test_tier1_arxiv_id_match_returns_paper(self):
        existing = _make_paper(id=42, arxiv_id="2301.07041")
        self.repo.get_by_arxiv_id.return_value = existing
        candidate = _make_candidate(arxiv_id="2301.07041")

        result = await self.svc.find_duplicate(candidate)

        assert result is existing
        self.repo.get_by_arxiv_id.assert_awaited_once_with("2301.07041")
        self.repo.get_by_doi.assert_not_awaited()
        self.repo.get_by_title_author.assert_not_awaited()

    async def test_tier1_no_arxiv_id_skips_lookup(self):
        candidate = _make_candidate(arxiv_id=None)
        self.repo.get_by_doi.return_value = None
        self.repo.get_by_title_author.return_value = None

        await self.svc.find_duplicate(candidate)

        self.repo.get_by_arxiv_id.assert_not_awaited()

    async def test_tier2_doi_match_when_arxiv_misses(self):
        existing = _make_paper(id=7, doi="10.1234/test")
        self.repo.get_by_arxiv_id.return_value = None
        self.repo.get_by_doi.return_value = existing
        candidate = _make_candidate(arxiv_id="2301.00000", doi="10.1234/test")

        result = await self.svc.find_duplicate(candidate)

        assert result is existing
        self.repo.get_by_doi.assert_awaited_once_with("10.1234/test")
        self.repo.get_by_title_author.assert_not_awaited()

    async def test_tier2_no_doi_skips_lookup(self):
        self.repo.get_by_arxiv_id.return_value = None
        self.repo.get_by_title_author.return_value = None
        candidate = _make_candidate(doi=None)

        await self.svc.find_duplicate(candidate)

        self.repo.get_by_doi.assert_not_awaited()

    async def test_tier3_title_author_match(self):
        existing = _make_paper(id=3)
        self.repo.get_by_arxiv_id.return_value = None
        self.repo.get_by_doi.return_value = None
        self.repo.get_by_title_author.return_value = existing
        candidate = _make_candidate(title="Deep Learning", authors=["Alice Smith", "Bob Jones"])

        result = await self.svc.find_duplicate(candidate)

        assert result is existing
        self.repo.get_by_title_author.assert_awaited_once_with(
            DeduplicationService.normalize_title("Deep Learning"),
            "Alice Smith",
        )

    async def test_tier3_no_authors_skips_lookup(self):
        self.repo.get_by_arxiv_id.return_value = None
        self.repo.get_by_doi.return_value = None
        candidate = _make_candidate(authors=[])

        result = await self.svc.find_duplicate(candidate)

        assert result is None
        self.repo.get_by_title_author.assert_not_awaited()

    async def test_all_tiers_miss_returns_none(self):
        self.repo.get_by_arxiv_id.return_value = None
        self.repo.get_by_doi.return_value = None
        self.repo.get_by_title_author.return_value = None
        candidate = _make_candidate(
            arxiv_id="0000.00000", doi="10.0000/x", authors=["Author A"]
        )

        result = await self.svc.find_duplicate(candidate)

        assert result is None

    async def test_whitespace_only_title_normalizes_to_empty(self):
        self.repo.get_by_arxiv_id.return_value = None
        self.repo.get_by_doi.return_value = None
        candidate = _make_candidate(title="   ", authors=["Author A"])
        self.repo.get_by_title_author.return_value = None

        result = await self.svc.find_duplicate(candidate)

        assert result is None
        self.repo.get_by_title_author.assert_awaited_once_with("", "Author A")


@pytest.mark.unit
class TestMergeMetadata:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = AsyncMock()
        self.svc = DeduplicationService(self.repo)

    async def test_fills_null_arxiv_id(self):
        existing = _make_paper(arxiv_id=None)
        self.repo.update.return_value = existing
        candidate = _make_candidate(arxiv_id="2301.07041")

        await self.svc.merge_metadata(existing, candidate)

        kwargs = self.repo.update.call_args.kwargs
        assert kwargs["arxiv_id"] == "2301.07041"

    async def test_fills_null_doi(self):
        existing = _make_paper(doi=None)
        self.repo.update.return_value = existing
        candidate = _make_candidate(doi="10.1234/test")

        await self.svc.merge_metadata(existing, candidate)

        assert "doi" in self.repo.update.call_args.kwargs

    async def test_fills_null_abstract(self):
        existing = _make_paper(abstract=None)
        self.repo.update.return_value = existing
        candidate = _make_candidate(abstract="This paper presents...")

        await self.svc.merge_metadata(existing, candidate)

        assert self.repo.update.call_args.kwargs["abstract"] == "This paper presents..."

    async def test_fills_null_publication_date(self):
        existing = _make_paper(publication_date=None)
        self.repo.update.return_value = existing
        date = datetime(2023, 1, 17, tzinfo=timezone.utc)
        candidate = _make_candidate(publication_date=date)

        await self.svc.merge_metadata(existing, candidate)

        assert self.repo.update.call_args.kwargs["publication_date"] == date

    async def test_fills_empty_authors(self):
        existing = _make_paper(authors=[])
        self.repo.update.return_value = existing
        candidate = _make_candidate(authors=["Alice", "Bob"])

        await self.svc.merge_metadata(existing, candidate)

        assert self.repo.update.call_args.kwargs["authors"] == ["Alice", "Bob"]

    async def test_does_not_overwrite_existing_arxiv_id(self):
        existing = _make_paper(arxiv_id="1111.11111")
        self.repo.update.return_value = existing
        candidate = _make_candidate(arxiv_id="2222.22222")

        await self.svc.merge_metadata(existing, candidate)

        if self.repo.update.called:
            assert "arxiv_id" not in self.repo.update.call_args.kwargs

    async def test_no_update_called_when_nothing_to_fill(self):
        date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        existing = _make_paper(
            arxiv_id="1111.11111",
            doi="10.1234/x",
            abstract="Existing abstract",
            publication_date=date,
            authors=["Alice"],
        )
        candidate = _make_candidate(
            arxiv_id="2222.22222",
            doi="10.9999/y",
            abstract="New abstract",
            publication_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            authors=["Bob"],
        )

        await self.svc.merge_metadata(existing, candidate)

        self.repo.update.assert_not_awaited()

    async def test_multiple_fields_filled_in_single_update_call(self):
        existing = _make_paper(arxiv_id=None, doi=None, abstract=None)
        self.repo.update.return_value = existing
        candidate = _make_candidate(
            arxiv_id="2301.07041", doi="10.1234/x", abstract="Abstract text"
        )

        await self.svc.merge_metadata(existing, candidate)

        self.repo.update.assert_awaited_once()
        kwargs = self.repo.update.call_args.kwargs
        assert kwargs["arxiv_id"] == "2301.07041"
        assert kwargs["doi"] == "10.1234/x"
        assert kwargs["abstract"] == "Abstract text"
