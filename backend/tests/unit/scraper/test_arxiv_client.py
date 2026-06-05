"""Unit tests for ArxivMetadataEnricher and extract_arxiv_id_from_url."""

from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx

from app.papers.domain import PaperCandidate
from app.scraper.adapters.arxiv_client import (
    ArxivMetadataEnricher,
    ArxivRateLimitUnavailable,
    RedisArxivRateLimiter,
    extract_arxiv_id_from_url,
)

_FIXTURE_DIR = Path(__file__).parent.parent.parent / "fixtures"
_VALID_XML = (_FIXTURE_DIR / "arxiv_atom_response.xml").read_text()

_BATCH_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/1111.11111v2</id>
    <published>2021-01-01T00:00:00Z</published>
    <title>First Batch Paper</title>
    <summary>First abstract</summary>
    <author><name>Alice Author</name></author>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2222.22222</id>
    <published>2022-02-02T00:00:00Z</published>
    <title>Second Batch Paper</title>
    <summary>Second abstract</summary>
    <author><name>Bob Author</name></author>
  </entry>
</feed>"""

_NO_ENTRY_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title type="html">ArXiv Query: unknown</title>
</feed>"""

_MINIMAL_ENTRY_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2301.07041</id>
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
            ("https://arxiv.org/pdf/2301.07041v2", "2301.07041"),
            ("https://arxiv.org/pdf/2301.07041v10", "2301.07041"),
            ("https://arxiv.org/html/2301.07041v3", "2301.07041"),
            ("https://arxiv.org/abs/1234.56789", "1234.56789"),
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
class TestRedisArxivRateLimiter:
    async def test_first_reservation_has_zero_wait_and_sets_ttl(self):
        client = AsyncMock()
        client.eval.return_value = 0
        with patch("app.scraper.adapters.arxiv_client.aioredis.from_url", return_value=client):
            await RedisArxivRateLimiter("redis://test", delay_seconds=3.0).wait_for_slot()

        client.eval.assert_awaited_once()
        args = client.eval.await_args.args
        assert args[2] == "rate_limit:arxiv:next_request_ms"
        assert args[3] == 3000
        assert args[4] == 3600000
        client.aclose.assert_awaited_once()

    async def test_second_reservation_waits(self):
        client = AsyncMock()
        client.eval.return_value = 1500
        sleep = AsyncMock()
        with (
            patch("app.scraper.adapters.arxiv_client.aioredis.from_url", return_value=client),
            patch("app.scraper.adapters.arxiv_client.asyncio.sleep", sleep),
        ):
            await RedisArxivRateLimiter("redis://test", delay_seconds=3.0).wait_for_slot()

        sleep.assert_awaited_once_with(1.5)

    async def test_redis_failure_raises_fail_closed_signal(self):
        client = AsyncMock()
        client.eval.side_effect = ConnectionError("down")
        with patch("app.scraper.adapters.arxiv_client.aioredis.from_url", return_value=client):
            with pytest.raises(ArxivRateLimitUnavailable):
                await RedisArxivRateLimiter("redis://test").wait_for_slot()


@pytest.mark.unit
class TestArxivEnricher:
    def _enricher(self, delay=0.0, batch_size=50):
        return ArxivMetadataEnricher(
            redis_url="redis://localhost:6379/0",
            timeout=5.0,
            rate_limit_delay=delay,
            batch_size=batch_size,
        )

    def _limiter_patch(self):
        return patch("app.scraper.adapters.arxiv_client.RedisArxivRateLimiter.wait_for_slot", new=AsyncMock())

    @respx.mock
    async def test_happy_path_populates_all_fields(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        with self._limiter_patch():
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        assert paper.title == "Causal Influence Detection for Improving Efficiency in Reinforcement Learning"
        assert "causal influences" in paper.abstract
        assert paper.authors == ["Georg Martius", "Bernhard Scholkopf", "Sebastien Lachapelle"]
        assert paper.publication_date.year == 2023
        assert paper.publication_date.month == 1
        assert paper.source_url == "https://arxiv.org/abs/2301.07041"

    @respx.mock
    async def test_enrich_many_sends_one_request_for_multiple_ids(self):
        route = respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_BATCH_XML))
        papers = [_candidate(arxiv_id="1111.11111"), _candidate(arxiv_id="2222.22222")]

        with self._limiter_patch():
            result = await self._enricher().enrich_many(papers)

        assert route.call_count == 1
        assert "1111.11111" in str(route.calls[0].request.url)
        assert "2222.22222" in str(route.calls[0].request.url)
        assert result[0].title == "First Batch Paper"
        assert result[1].title == "Second Batch Paper"

    @respx.mock
    async def test_batches_split_at_configured_size(self):
        route = respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_BATCH_XML))
        papers = [_candidate(arxiv_id="1111.11111"), _candidate(arxiv_id="2222.22222")]

        with self._limiter_patch():
            await self._enricher(batch_size=1).enrich_many(papers)

        assert route.call_count == 2

    @respx.mock
    async def test_duplicate_arxiv_ids_fetched_once_and_applied_to_all(self):
        route = respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_BATCH_XML))
        papers = [_candidate(arxiv_id="1111.11111"), _candidate(arxiv_id="1111.11111v3")]

        with self._limiter_patch():
            result = await self._enricher().enrich_many(papers)

        assert route.call_count == 1
        assert result[0].title == "First Batch Paper"
        assert result[1].title == "First Batch Paper"

    @respx.mock
    async def test_extracts_arxiv_id_from_source_url_when_not_set(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        with self._limiter_patch():
            paper = await self._enricher().enrich(_candidate(arxiv_id=None, source_url="https://arxiv.org/abs/2301.07041"))

        assert paper.arxiv_id == "2301.07041"
        assert paper.title != "Original Title"

    async def test_no_arxiv_id_and_no_arxiv_url_returns_unchanged(self):
        paper = _candidate(arxiv_id=None, source_url="https://example.com/paper")
        result = await self._enricher().enrich(paper)
        assert result.title == "Original Title"
        assert result.arxiv_id is None

    @respx.mock
    async def test_429_retries_once_using_retry_after_header_and_reacquires_slot(self):
        wait_for_slot = AsyncMock()
        respx.get("https://export.arxiv.org/api/query").mock(
            side_effect=[
                httpx.Response(429, headers={"Retry-After": "5"}),
                httpx.Response(200, text=_VALID_XML),
            ]
        )
        sleep_calls = []
        with (
            patch("app.scraper.adapters.arxiv_client.RedisArxivRateLimiter.wait_for_slot", wait_for_slot),
            patch("app.scraper.adapters.arxiv_client.asyncio.sleep", new=AsyncMock(side_effect=lambda s: sleep_calls.append(s))),
        ):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        assert paper.abstract is not None
        assert wait_for_slot.await_count == 2
        assert 5.0 in sleep_calls

    @respx.mock
    async def test_429_twice_returns_unenriched_paper(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(429, headers={"Retry-After": "1"}))
        with self._limiter_patch():
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        assert paper.title == "Original Title"
        assert paper.abstract is None

    @respx.mock
    async def test_redis_failure_does_not_call_http_and_returns_unchanged(self):
        route = respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        with patch(
            "app.scraper.adapters.arxiv_client.RedisArxivRateLimiter.wait_for_slot",
            new=AsyncMock(side_effect=ArxivRateLimitUnavailable("down")),
        ):
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))

        assert route.call_count == 0
        assert paper.title == "Original Title"

    @respx.mock
    async def test_500_returns_unchanged(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(500))
        with self._limiter_patch():
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))
        assert paper.title == "Original Title"

    @respx.mock
    async def test_network_error_returns_unchanged(self):
        respx.get("https://export.arxiv.org/api/query").mock(side_effect=httpx.ConnectError("connection refused"))
        with self._limiter_patch():
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))
        assert paper.title == "Original Title"

    @respx.mock
    async def test_malformed_xml_returns_unchanged(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text="<this is not valid xml<<<"))
        with self._limiter_patch():
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))
        assert paper.title == "Original Title"

    @respx.mock
    async def test_missing_entry_element_returns_unchanged(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_NO_ENTRY_XML))
        with self._limiter_patch():
            paper = await self._enricher().enrich(_candidate(arxiv_id="2301.07041"))
        assert paper.title == "Original Title"

    @respx.mock
    async def test_entry_missing_summary_keeps_original_abstract(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_MINIMAL_ENTRY_XML))
        paper = _candidate(arxiv_id="2301.07041", abstract="original abstract")
        with self._limiter_patch():
            result = await self._enricher().enrich(paper)
        assert result.title == "Minimal Paper"
        assert result.abstract == "original abstract"

    @respx.mock
    async def test_canonical_source_url_always_set_on_success(self):
        respx.get("https://export.arxiv.org/api/query").mock(return_value=httpx.Response(200, text=_VALID_XML))
        paper = _candidate(arxiv_id="2301.07041", source_url="https://scholar.google.com/old")
        with self._limiter_patch():
            result = await self._enricher().enrich(paper)
        assert result.source_url == "https://arxiv.org/abs/2301.07041"
