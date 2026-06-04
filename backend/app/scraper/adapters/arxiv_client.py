"""ArXiv metadata enricher.

Fetches full title, abstract, exact publication date, and author list from the
arXiv Atom API for papers whose arxiv_id was discovered via Google Scholar.

Rate-limit policy (arXiv asks for no more than 1 req/3s from automated clients):
- A Redis-backed global limiter reserves a slot BEFORE every request.
- Google Scholar findings are enriched in arXiv ID batches.
- On 429 we read the Retry-After header (or fall back to 10 s) and wait before
  retrying once. A second 429 returns papers unenriched so the pipeline can
  continue rather than stalling indefinitely.
"""

from __future__ import annotations

import asyncio
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import httpx
import redis.asyncio as aioredis

from app.papers.domain import PaperCandidate
from app.scraper.interfaces import PaperMetadataEnricher

_logger = logging.getLogger(__name__)

_ARXIV_API = "https://export.arxiv.org/api/query"
_ARXIV_NS = "http://www.w3.org/2005/Atom"

_ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", re.I)

# arXiv's documented bulk-access guideline: <= 1 request per 3 seconds.
_DEFAULT_DELAY = 3.0
_DEFAULT_TIMEOUT = 20.0
_DEFAULT_BATCH_SIZE = 50
_MAX_RETRIES = 1

_RATE_LIMIT_KEY = "rate_limit:arxiv:next_request_ms"
_RATE_LIMIT_TTL_MS = 60 * 60 * 1000
_RESERVE_SLOT_SCRIPT = """
local key = KEYS[1]
local delay_ms = tonumber(ARGV[1])
local ttl_ms = tonumber(ARGV[2])
local now_parts = redis.call('TIME')
local now_ms = (tonumber(now_parts[1]) * 1000) + math.floor(tonumber(now_parts[2]) / 1000)
local next_ms = tonumber(redis.call('GET', key) or '0')
local reserved_ms = now_ms
if next_ms > now_ms then
    reserved_ms = next_ms
end
redis.call('SET', key, reserved_ms + delay_ms, 'PX', ttl_ms)
return reserved_ms - now_ms
"""


class ArxivRateLimitUnavailable(RuntimeError):
    """Raised when the global arXiv limiter cannot reserve a request slot."""


class RedisArxivRateLimiter:
    """Redis-backed global request scheduler for arXiv API calls."""

    def __init__(
        self,
        redis_url: str,
        *,
        delay_seconds: float = _DEFAULT_DELAY,
        key: str = _RATE_LIMIT_KEY,
        ttl_ms: int = _RATE_LIMIT_TTL_MS,
    ) -> None:
        self._redis_url = redis_url
        self._delay_ms = max(0, int(delay_seconds * 1000))
        self._key = key
        self._ttl_ms = ttl_ms

    async def wait_for_slot(self) -> None:
        client = None
        try:
            client = aioredis.from_url(self._redis_url)
            wait_ms = int(await client.eval(_RESERVE_SLOT_SCRIPT, 1, self._key, self._delay_ms, self._ttl_ms))
        except Exception as exc:
            raise ArxivRateLimitUnavailable("Unable to reserve arXiv rate-limit slot") from exc
        finally:
            if client is not None:
                await client.aclose()

        if wait_ms > 0:
            await asyncio.sleep(wait_ms / 1000)


def normalize_arxiv_id(arxiv_id: str) -> str:
    """Return an arXiv ID without a version suffix."""
    return re.sub(r"v\d+$", "", arxiv_id.strip())


def extract_arxiv_id_from_url(url: str) -> str | None:
    """Return the bare arXiv ID (no version suffix) from a URL, or None."""
    m = _ARXIV_URL_RE.search(url)
    if not m:
        return None
    return normalize_arxiv_id(m.group(1))


def _chunks(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


class ArxivMetadataEnricher(PaperMetadataEnricher):
    """Fetches full paper metadata from the arXiv Atom API.

    Only enriches papers that already have an arxiv_id set (or whose source_url
    contains an arxiv.org link that we can parse).
    """

    def __init__(
        self,
        redis_url: str,
        timeout: float = _DEFAULT_TIMEOUT,
        rate_limit_delay: float = _DEFAULT_DELAY,
        batch_size: int = _DEFAULT_BATCH_SIZE,
    ) -> None:
        self._timeout = timeout
        self._batch_size = max(1, batch_size)
        self._limiter = RedisArxivRateLimiter(redis_url, delay_seconds=rate_limit_delay)

    async def enrich(self, paper: PaperCandidate) -> PaperCandidate:
        return (await self.enrich_many([paper]))[0]

    async def enrich_many(self, papers: list[PaperCandidate]) -> list[PaperCandidate]:
        candidates_by_id: dict[str, list[PaperCandidate]] = {}
        for paper in papers:
            if not paper.arxiv_id and paper.source_url:
                paper.arxiv_id = extract_arxiv_id_from_url(paper.source_url)
            if paper.arxiv_id:
                paper.arxiv_id = normalize_arxiv_id(paper.arxiv_id)
                candidates_by_id.setdefault(paper.arxiv_id, []).append(paper)

        arxiv_ids = list(candidates_by_id)
        if not arxiv_ids:
            return papers

        for batch in _chunks(arxiv_ids, self._batch_size):
            entries = await self._fetch_batch(batch)
            if entries is None:
                continue
            for arxiv_id, entry in entries.items():
                for paper in candidates_by_id.get(arxiv_id, []):
                    self._apply_entry(paper, entry)

        return papers

    async def _fetch_batch(self, arxiv_ids: list[str]) -> dict[str, ET.Element] | None:
        for attempt in range(_MAX_RETRIES + 1):
            try:
                await self._limiter.wait_for_slot()
            except ArxivRateLimitUnavailable as exc:
                _logger.warning("arXiv rate limiter unavailable; skipping ids=%s: %s", arxiv_ids, exc)
                return None

            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(_ARXIV_API, params={"id_list": ",".join(arxiv_ids)})
            except httpx.RequestError as exc:
                _logger.warning("arXiv API unreachable for ids=%s: %s", arxiv_ids, exc)
                return None

            if resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", 10))
                if attempt < _MAX_RETRIES:
                    _logger.warning("arXiv 429 for ids=%s; waiting %.0fs before retry", arxiv_ids, retry_after)
                    await asyncio.sleep(retry_after)
                    continue
                _logger.warning("arXiv 429 for ids=%s; retries exhausted, skipping enrichment", arxiv_ids)
                return None

            if not resp.is_success:
                _logger.warning("arXiv API %s for ids=%s", resp.status_code, arxiv_ids)
                return None

            return self._parse_entries(resp.text, arxiv_ids)

        return None

    def _parse_entries(self, xml_text: str, arxiv_ids: list[str]) -> dict[str, ET.Element]:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            _logger.warning("arXiv returned invalid XML for ids=%s: %s", arxiv_ids, exc)
            return {}

        entries: dict[str, ET.Element] = {}
        for entry in root.findall(f"{{{_ARXIV_NS}}}entry"):
            id_el = entry.find(f"{{{_ARXIV_NS}}}id")
            if id_el is None or not id_el.text:
                continue
            arxiv_id = extract_arxiv_id_from_url(id_el.text)
            if arxiv_id:
                entries[arxiv_id] = entry

        missing = [arxiv_id for arxiv_id in arxiv_ids if arxiv_id not in entries]
        if missing:
            _logger.warning("arXiv entries not found for ids=%s", missing)
        return entries

    def _apply_entry(self, paper: PaperCandidate, entry: ET.Element) -> None:
        if paper.arxiv_id:
            paper.arxiv_id = normalize_arxiv_id(paper.arxiv_id)

        title_el = entry.find(f"{{{_ARXIV_NS}}}title")
        if title_el is not None and title_el.text:
            paper.title = title_el.text.strip().replace("\n", " ")

        summary_el = entry.find(f"{{{_ARXIV_NS}}}summary")
        if summary_el is not None and summary_el.text:
            paper.abstract = summary_el.text.strip()

        published_el = entry.find(f"{{{_ARXIV_NS}}}published")
        if published_el is not None and published_el.text:
            try:
                paper.publication_date = datetime.fromisoformat(published_el.text.rstrip("Z")).replace(tzinfo=timezone.utc)
            except ValueError:
                pass

        arxiv_authors = [(name_el.text or "").strip() for author in entry.findall(f"{{{_ARXIV_NS}}}author") for name_el in author.findall(f"{{{_ARXIV_NS}}}name") if name_el.text]
        if arxiv_authors:
            paper.authors = arxiv_authors

        if paper.arxiv_id:
            paper.source_url = f"https://arxiv.org/abs/{paper.arxiv_id}"

        _logger.debug(
            "arXiv enriched: id=%s title=%r authors=%d",
            paper.arxiv_id,
            paper.title[:60],
            len(paper.authors),
        )
