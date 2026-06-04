"""ArXiv metadata enricher.

Fetches full title, abstract, exact publication date, and author list from the
arXiv Atom API for papers whose arxiv_id was discovered via Google Scholar.

Reuses the XML-parsing approach already present in app/chairs/service.py,
but extended to also extract the complete author list and exact ISO date.
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
_ARXIV_AUTHOR_NS = "http://arxiv.org/schemas/atom"

# Regex to extract an arXiv ID from a URL like
#   https://arxiv.org/abs/2301.07041   or   http://arxiv.org/pdf/2301.07041v2
_ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", re.I)


def extract_arxiv_id_from_url(url: str) -> str | None:
    """Return the arXiv ID (without version suffix) from a URL, or None."""
    m = _ARXIV_URL_RE.search(url)
    if not m:
        return None
    # Strip version suffix (e.g. v2) for canonical dedup
    return re.sub(r"v\d+$", "", m.group(1))


class ArxivMetadataEnricher(PaperMetadataEnricher):
    """Fetches full paper metadata from the arXiv Atom API.

    Only enriches papers that already have an arxiv_id set (or whose
    source_url contains an arxiv.org link that we can parse).
    """

    def __init__(self, timeout: float = 15.0, rate_limit_delay: float = 1.0) -> None:
        self._timeout = timeout
        self._delay = rate_limit_delay

    async def enrich(self, paper: PaperCandidate) -> PaperCandidate:
        # Try to extract arxiv_id from the URL if not already set
        if not paper.arxiv_id and paper.source_url:
            paper.arxiv_id = extract_arxiv_id_from_url(paper.source_url)

        if not paper.arxiv_id:
            return paper  # not an arXiv paper — nothing to do

        url = f"{_ARXIV_API}?id_list={paper.arxiv_id}"
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            _logger.warning("arXiv API %s for id=%s", exc.response.status_code, paper.arxiv_id)
            return paper
        except httpx.RequestError as exc:
            _logger.warning("arXiv API unreachable for id=%s: %s", paper.arxiv_id, exc)
            return paper

        try:
            root = ET.fromstring(resp.text)
        except ET.ParseError as exc:
            _logger.warning("arXiv returned invalid XML for id=%s: %s", paper.arxiv_id, exc)
            return paper

        entry = root.find(f"{{{_ARXIV_NS}}}entry")
        if entry is None:
            _logger.warning("arXiv entry not found for id=%s", paper.arxiv_id)
            return paper

        # Title — prefer arXiv's canonical version
        title_el = entry.find(f"{{{_ARXIV_NS}}}title")
        if title_el is not None and title_el.text:
            paper.title = title_el.text.strip().replace("\n", " ")

        # Abstract
        summary_el = entry.find(f"{{{_ARXIV_NS}}}summary")
        if summary_el is not None and summary_el.text:
            paper.abstract = summary_el.text.strip()

        # Published date (ISO 8601, e.g. "2023-01-17T12:34:56Z")
        published_el = entry.find(f"{{{_ARXIV_NS}}}published")
        if published_el is not None and published_el.text:
            try:
                paper.publication_date = datetime.fromisoformat(published_el.text.rstrip("Z")).replace(tzinfo=timezone.utc)
            except ValueError:
                pass

        # Authors — use arXiv list if it's more complete than Scholar's
        arxiv_authors = [(name_el.text or "").strip() for author in entry.findall(f"{{{_ARXIV_NS}}}author") for name_el in author.findall(f"{{{_ARXIV_NS}}}name") if name_el.text]
        if arxiv_authors:
            paper.authors = arxiv_authors

        # Canonical source URL
        paper.source_url = f"https://arxiv.org/abs/{paper.arxiv_id}"

        # Be polite to the arXiv API
        await asyncio.sleep(self._delay)
        _logger.debug(
            "arXiv enriched: id=%s title=%r authors=%d",
            paper.arxiv_id,
            paper.title[:60],
            len(paper.authors),
        )
        return paper
