"""ArXiv metadata enricher.

Fetches full title, abstract, exact publication date, and author list from the
arXiv Atom API for papers whose arxiv_id was discovered via Google Scholar.

Rate-limit policy (arXiv asks for no more than 1 req/3s from automated clients):
- A configurable delay is applied BEFORE every request.
- On 429 we read the Retry-After header (or fall back to 10 s) and wait before
  retrying once.  A second 429 returns the paper unenriched so the pipeline
  can continue rather than stalling indefinitely.
"""

from __future__ import annotations

import asyncio
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import httpx

from app.papers.domain import PaperCandidate
from app.scraper.interfaces import PaperMetadataEnricher

_logger = logging.getLogger(__name__)

_ARXIV_API = "https://export.arxiv.org/api/query"
_ARXIV_NS = "http://www.w3.org/2005/Atom"

_ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", re.I)

# arXiv's documented bulk-access guideline: ≤ 1 request per 3 seconds.
_DEFAULT_DELAY = 3.0
_DEFAULT_TIMEOUT = 20.0
_MAX_RETRIES = 1


def extract_arxiv_id_from_url(url: str) -> str | None:
    """Return the bare arXiv ID (no version suffix) from a URL, or None."""
    m = _ARXIV_URL_RE.search(url)
    if not m:
        return None
    return re.sub(r"v\d+$", "", m.group(1))


class ArxivMetadataEnricher(PaperMetadataEnricher):
    """Fetches full paper metadata from the arXiv Atom API.

    Only enriches papers that already have an arxiv_id set (or whose
    source_url contains an arxiv.org link that we can parse).
    """

    def __init__(self, timeout: float = _DEFAULT_TIMEOUT, rate_limit_delay: float = _DEFAULT_DELAY) -> None:
        self._timeout = timeout
        self._delay = rate_limit_delay

    async def enrich(self, paper: PaperCandidate) -> PaperCandidate:
        # Try to extract arxiv_id from the URL if not already set
        if not paper.arxiv_id and paper.source_url:
            paper.arxiv_id = extract_arxiv_id_from_url(paper.source_url)

        if not paper.arxiv_id:
            return paper

        url = f"{_ARXIV_API}?id_list={paper.arxiv_id}"

        for attempt in range(_MAX_RETRIES + 1):
            # Delay BEFORE every request (not after) so consecutive calls
            # are always separated by at least `_delay` seconds.
            await asyncio.sleep(self._delay)

            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url)
            except httpx.RequestError as exc:
                _logger.warning("arXiv API unreachable for id=%s: %s", paper.arxiv_id, exc)
                return paper

            if resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", 10))
                if attempt < _MAX_RETRIES:
                    _logger.warning(
                        "arXiv 429 for id=%s — waiting %.0fs before retry",
                        paper.arxiv_id,
                        retry_after,
                    )
                    await asyncio.sleep(retry_after)
                    continue
                else:
                    _logger.warning(
                        "arXiv 429 for id=%s — retries exhausted, skipping enrichment",
                        paper.arxiv_id,
                    )
                    return paper

            if not resp.is_success:
                _logger.warning("arXiv API %s for id=%s", resp.status_code, paper.arxiv_id)
                return paper

            # Success — parse and return
            return self._parse(resp.text, paper)

        return paper  # unreachable, satisfies type checker

    def _parse(self, xml_text: str, paper: PaperCandidate) -> PaperCandidate:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            _logger.warning("arXiv returned invalid XML for id=%s: %s", paper.arxiv_id, exc)
            return paper

        entry = root.find(f"{{{_ARXIV_NS}}}entry")
        if entry is None:
            _logger.warning("arXiv entry not found for id=%s", paper.arxiv_id)
            return paper

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

        paper.source_url = f"https://arxiv.org/abs/{paper.arxiv_id}"

        _logger.debug(
            "arXiv enriched: id=%s title=%r authors=%d",
            paper.arxiv_id,
            paper.title[:60],
            len(paper.authors),
        )
        return paper
