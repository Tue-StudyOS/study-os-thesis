"""Unit tests for DeduplicationService."""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.papers.dedup import DeduplicationService
from app.papers.domain import PaperCandidate


def _make_paper(**kwargs):
    defaults = dict(
        id=1,
        title="Some Paper",
        title_normalized="some paper",
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
        source="openalex",
        source_url="https://openalex.org/W1",
        doi=None,
        abstract=None,
        authors=[],
        publication_date=None,
    )
    defaults.update(kwargs)
    return PaperCandidate(**defaults)


@pytest.mark.unit
class TestNormalizeTitle:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("  Hello, World!  ", "hello world"),
            ("UPPER CASE", "upper case"),
            ("multiple   spaces", "multiple spaces"),
            ("Punctuation: (test) [here]", "punctuation test here"),
            ("A Learning-Based Approach", "a learningbased approach"),
            ("", ""),
            ("already normalized", "already normalized"),
        ],
    )
    def test_normalize(self, raw, expected):
        assert DeduplicationService.normalize_title(raw) == expected

    def test_en_dash_stripped(self):
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

    async def test_doi_match_returns_paper(self):
        existing = _make_paper(id=7, doi="10.1234/test")
        self.repo.get_by_doi.return_value = existing
        candidate = _make_candidate(doi="10.1234/test")

        result = await self.svc.find_duplicate(candidate)

        assert result is existing
        self.repo.get_by_doi.assert_awaited_once_with("10.1234/test")
        self.repo.get_by_title_author.assert_not_awaited()

    async def test_no_doi_skips_doi_lookup(self):
        self.repo.get_by_title_author.return_value = None
        candidate = _make_candidate(doi=None, authors=["Author A"])

        await self.svc.find_duplicate(candidate)

        self.repo.get_by_doi.assert_not_awaited()

    async def test_title_author_match_after_doi_miss(self):
        existing = _make_paper(id=3)
        self.repo.get_by_doi.return_value = None
        self.repo.get_by_title_author.return_value = existing
        candidate = _make_candidate(title="Deep Learning", authors=["Alice Smith", "Bob Jones"])

        result = await self.svc.find_duplicate(candidate)

        assert result is existing
        self.repo.get_by_title_author.assert_awaited_once_with(
            DeduplicationService.normalize_title("Deep Learning"),
            "Alice Smith",
        )

    async def test_no_authors_skips_title_author_lookup(self):
        self.repo.get_by_doi.return_value = None
        candidate = _make_candidate(authors=[])

        result = await self.svc.find_duplicate(candidate)

        assert result is None
        self.repo.get_by_title_author.assert_not_awaited()

    async def test_all_tiers_miss_returns_none(self):
        self.repo.get_by_doi.return_value = None
        self.repo.get_by_title_author.return_value = None
        candidate = _make_candidate(doi="10.0000/x", authors=["Author A"])

        result = await self.svc.find_duplicate(candidate)

        assert result is None


@pytest.mark.unit
class TestMergeMetadata:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = AsyncMock()
        self.svc = DeduplicationService(self.repo)

    async def test_fills_null_doi(self):
        existing = _make_paper(doi=None)
        self.repo.update.return_value = existing
        candidate = _make_candidate(doi="10.1234/test")

        await self.svc.merge_metadata(existing, candidate)

        assert self.repo.update.call_args.kwargs["doi"] == "10.1234/test"

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

    async def test_no_update_called_when_nothing_to_fill(self):
        date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        existing = _make_paper(
            doi="10.1234/x",
            abstract="Existing abstract",
            publication_date=date,
            authors=["Alice"],
        )
        candidate = _make_candidate(
            doi="10.9999/y",
            abstract="New abstract",
            publication_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            authors=["Bob"],
        )

        await self.svc.merge_metadata(existing, candidate)

        self.repo.update.assert_not_awaited()

    async def test_multiple_fields_filled_in_single_update_call(self):
        existing = _make_paper(doi=None, abstract=None)
        self.repo.update.return_value = existing
        candidate = _make_candidate(doi="10.1234/x", abstract="Abstract text")

        await self.svc.merge_metadata(existing, candidate)

        self.repo.update.assert_awaited_once()
        kwargs = self.repo.update.call_args.kwargs
        assert kwargs["doi"] == "10.1234/x"
        assert kwargs["abstract"] == "Abstract text"
