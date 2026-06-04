"""Unit tests for ArxivMetadataEnricher and extract_arxiv_id_from_url."""

from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx

from app.papers.domain import PaperCandidate
from app.scraper.adapters.arxiv_client import ArxivMetadataEnricher, extract_arxiv_id_from_url

_FIXTURE_DIR = Path(__file__).parent.parent.parent / "fixtures"
_VALID_XML = (_FIXTURE_DIR / "arxiv_atom_response.xml").read_text()

_NO_ENTRY_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title type="html">ArXiv Query: unknown</title>
</feed>"""

_MINIMAL_ENTRY_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <published>2023-06-01T00:00:00Z</published>
    <title>Minimal Paper</title>
  </entry>
</feed>"""


def _candidate(**kwargs) -> PaperCandidate:
    defaults = dict(
        title="Original Title",
        source="google_scholar",
        source_url="https://scholar.google.com/test",
        arxiv_id=None,
    )
    defaults.update(kwargs)
    return PaperCandidate(**defaults)


@pytest.mark.unit
class TestExtractArxivIdFromUrl:
    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://arxiv.org/abs/2301.07041", "2301.07041"),
            ("http://arxiv.org/abs/2301.07041", "2301.07041"),
            ("https://arxiv.org/pdf/2301.07041v2", "2301.07041"),  # version stripped
            ("https://arxiv.org/pdf/2301.07041v10", "2301.07041"),  # multi-digit version
            ("https://arxiv.org/html/2301.07041v3", "2301.07041"),
            ("https://arxiv.org/abs/1234.56789", "1234.56789"),  # 5-digit ID
            ("https://example.com/paper", None),
            ("https://google.com", None),
            ("", None),
            ("not a url at all", None),
        ],
    )
    def test_extract(self, url, expected):
        assert extract_arxiv_id_from_url(url) == expected

    def test_no_version_suffix_on_canonical_id(self):
        result = extract_arxiv_id_from_url("https://arxiv.org/abs/2301.07041v99")
        assert "v" not in result


@pytest.mark.unit
class TestArxivEnricher:
    def _enricher(self, delay=0.0):
        return ArxivMetadataEnricher(timeout=5.0, rate_limit_delay=delay)

    # ---------------------------------------------------------------
    # Happy paths
    # ---------------------------------------------------------------

    @respx.mock
    async def test_happy_path_populates_all_fields(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        with patch("asyncio.sleep"):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        assert paper.title == "Causal Influence Detection for Improving Efficiency in Reinforcement Learning"
        assert "causal influences" in paper.abstract
        assert paper.authors == ["Georg Martius", "Bernhard Scholkopf", "Sebastien Lachapelle"]
        assert paper.publication_date.year == 2023
        assert paper.publication_date.month == 1
        assert paper.source_url == "https://arxiv.org/abs/2301.07041"

    @respx.mock
    async def test_extracts_arxiv_id_from_source_url_when_not_set(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        with patch("asyncio.sleep"):
            paper = await self._enricher().enrich(_candidate(arxiv_id=None, source_url="https://arxiv.org/abs/2301.07041"))

        assert paper.arxiv_id == "2301.07041"
        assert paper.title != "Original Title"  # was populated from arXiv

    @respx.mock
    async def test_request_uses_correct_arxiv_api_url(self):
        route = respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        with patch("asyncio.sleep"):
            await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        assert route.called
        assert "id_list=2301.07041" in str(route.calls[0].request.url)

    @respx.mock
    async def test_delay_applied_before_request(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        sleep_calls = []
        with patch("asyncio.sleep", new=AsyncMock(side_effect=lambda s: sleep_calls.append(s))):
            await ArxivMetadataEnricher(rate_limit_delay=1.5).enrich(_candidate(arxiv_id="2301.07041"))

        # Sleep must be called once with the configured delay
        assert len(sleep_calls) >= 1
        assert sleep_calls[0] == 1.5

    # ---------------------------------------------------------------
    # No-op paths
    # ---------------------------------------------------------------

    async def test_no_arxiv_id_and_no_arxiv_url_returns_unchanged(self):
        paper = _candidate(arxiv_id=None, source_url="https://example.com/paper")
        with patch("asyncio.sleep"):
            result = await self._enricher().enrich(paper)
        assert result.title == "Original Title"
        assert result.arxiv_id is None

    async def test_completely_no_source_url_returns_unchanged(self):
        paper = _candidate(arxiv_id=None, source_url="")
        result = await self._enricher().enrich(paper)
        assert result is paper

    # ---------------------------------------------------------------
    # Rate limiting / 429
    # ---------------------------------------------------------------

    @respx.mock
    async def test_429_retries_once_using_retry_after_header(self):
        respx.get("https://export.arxiv.org/api/query").mock(
            side_effect=[
                httpx.Response(429, headers={"Retry-After": "5"}),
                httpx.Response(200, text=_VALID_XML),
            ]
        )
        sleep_calls = []
        with patch("asyncio.sleep", new=AsyncMock(side_effect=lambda s: sleep_calls.append(s))):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        # Paper should be populated from the successful second attempt
        assert paper.abstract is not None
        # Retry-After value (5) must appear in a sleep call
        assert 5.0 in sleep_calls

    @respx.mock
    async def test_429_twice_returns_unenriched_paper(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(429, headers={"Retry-After": "1"}))
        with patch("asyncio.sleep"):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        assert paper.title == "Original Title"
        assert paper.abstract is None

    @respx.mock
    async def test_429_fallback_delay_when_no_retry_after_header(self):
        respx.get("https://export.arxiv.org/api/query").mock(
            return_value=httpx.Response(429)  # no Retry-After header
        )
        sleep_calls = []
        with patch("asyncio.sleep", new=AsyncMock(side_effect=lambda s: sleep_calls.append(s))):
            await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        # Fallback delay is 10s
        assert 10.0 in sleep_calls

    # ---------------------------------------------------------------
    # Other HTTP failure modes
    # ---------------------------------------------------------------

    @respx.mock
    async def test_500_returns_unchanged(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(500))
        with patch("asyncio.sleep"):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))
        assert paper.title == "Original Title"

    @respx.mock
    async def test_network_error_returns_unchanged(self):
        respx.get("https://export.arxiv.org/api/query").mock(side_effect=httpx.ConnectError("connection refused"))
        with patch("asyncio.sleep"):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))
        assert paper.title == "Original Title"

    # ---------------------------------------------------------------
    # XML parsing edge cases
    # ---------------------------------------------------------------

    @respx.mock
    async def test_malformed_xml_returns_unchanged(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text="<this is not valid xml<<<"))
        with patch("asyncio.sleep"):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))
        assert paper.title == "Original Title"

    @respx.mock
    async def test_missing_entry_element_returns_unchanged(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_NO_ENTRY_XML))
        with patch("asyncio.sleep"):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))
        assert paper.title == "Original Title"

    @respx.mock
    async def test_entry_missing_summary_keeps_original_abstract(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_MINIMAL_ENTRY_XML))
        paper = _candidate(arxiv_id="2301.07041", abstract="original abstract")
        with patch("asyncio.sleep"):
            result = await self._enricher().enrich(paper)
        # Title gets updated from XML, but abstract should remain since no <summary>
        assert result.title == "Minimal Paper"
        assert result.abstract == "original abstract"

    @respx.mock
    async def test_canonical_source_url_always_set_on_success(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        paper = _candidate(arxiv_id="2301.07041", source_url="https://scholar.google.com/old")
        with patch("asyncio.sleep"):
            result = await self._enricher().enrich(paper)
        assert result.source_url == "https://arxiv.org/abs/2301.07041"
