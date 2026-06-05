"""OpenAlex paper source client."""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone

import httpx

from app.papers.domain import PaperCandidate, ResearcherInfo
from app.scraper.interfaces import PaperSourceClient

_logger = logging.getLogger(__name__)

_OPENALEX_API = "https://api.openalex.org"
_DEFAULT_TIMEOUT = 20.0
_DEFAULT_PAGE_SIZE = 100


def _strip_leading_titles_for_search(name: str) -> str:
    s = (name or "").strip()
    return re.sub(r"^\s*(?:(?:Professor|Prof)\.?\s*|Dr(?:\.-Ing\.)?\.?\s*)+", "", s, flags=re.IGNORECASE).strip()


def _normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", name.lower())).strip()


def _year_cutoff(since_days: int) -> int:
    return datetime.now(timezone.utc).year - (since_days // 365)


def _short_openalex_id(value: str) -> str:
    return value.rstrip("/").rsplit("/", 1)[-1]


def _abstract_from_inverted_index(index: dict[str, list[int]] | None) -> str | None:
    if not index:
        return None
    words: list[tuple[int, str]] = []
    for word, positions in index.items():
        for position in positions:
            words.append((position, word))
    return " ".join(word for _, word in sorted(words))


def _parse_publication_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


class OpenAlexSourceClient(PaperSourceClient):
    """Fetches recent works for a researcher from OpenAlex."""

    def __init__(
        self,
        *,
        timeout: float = _DEFAULT_TIMEOUT,
        page_size: int = _DEFAULT_PAGE_SIZE,
        mailto: str | None = None,
    ) -> None:
        self._timeout = timeout
        self._page_size = max(1, min(page_size, _DEFAULT_PAGE_SIZE))
        self._mailto = mailto

    async def fetch_papers(
        self,
        researcher: ResearcherInfo,
        *,
        max_results: int = 20,
        since_days: int = 365,
    ) -> list[PaperCandidate]:
        author_name = _strip_leading_titles_for_search(researcher.name) or researcher.name
        author_id = await self._resolve_author_id(author_name, researcher.affiliation)
        if author_id is None:
            _logger.info("openalex.author_no_match researcher=%r author_query=%r", researcher.name, author_name)
            return []

        papers = await self._fetch_author_works(author_id, researcher.name, max_results=max_results, since_days=since_days)
        _logger.info(
            "openalex.author_works_complete researcher=%r author_id=%s parsed=%d max_results=%d since_days=%d",
            researcher.name,
            author_id,
            len(papers),
            max_results,
            since_days,
        )
        return papers

    async def _resolve_author_id(self, name: str, affiliation: str | None) -> str | None:
        params = {"search": name, "per-page": 5}
        data = await self._get_json("/authors", params)
        if data is None:
            return None

        expected = _normalize_name(name)
        affiliation_tokens = [token for token in re.split(r"\W+", (affiliation or "").lower()) if len(token) >= 4]
        candidates: list[tuple[int, str]] = []
        for author in data.get("results", []):
            display_name = author.get("display_name") or ""
            normalized = _normalize_name(display_name)
            if expected not in normalized and normalized not in expected:
                continue

            score = 10
            institutions = author.get("last_known_institutions") or []
            institution_text = " ".join((institution.get("display_name") or "").lower() for institution in institutions)
            if affiliation_tokens and any(token in institution_text for token in affiliation_tokens):
                score += 5
            score += min(int(author.get("works_count") or 0), 100) // 20

            author_id = author.get("id")
            if author_id:
                candidates.append((score, _short_openalex_id(str(author_id))))

        if not candidates:
            return None
        return max(candidates, key=lambda item: item[0])[1]

    async def _fetch_author_works(
        self,
        author_id: str,
        researcher_name: str,
        *,
        max_results: int,
        since_days: int,
    ) -> list[PaperCandidate]:
        cutoff_year = _year_cutoff(since_days)
        cursor = "*"
        papers: list[PaperCandidate] = []
        pages_visited = 0
        stop_reason = "max_results"

        while len(papers) < max_results:
            data = await self._get_json(
                "/works",
                {
                    "filter": f"author.id:{author_id},from_publication_date:{cutoff_year}-01-01",
                    "sort": "publication_date:desc",
                    "per-page": min(self._page_size, max_results - len(papers)),
                    "cursor": cursor,
                },
            )
            pages_visited += 1
            if data is None:
                stop_reason = "request_failed"
                break

            results = data.get("results", [])
            if not results:
                stop_reason = "empty_page"
                break

            for work in results:
                candidate = self._work_to_candidate(work)
                if candidate is None:
                    continue
                papers.append(candidate)
                if len(papers) >= max_results:
                    break

            next_cursor = (data.get("meta") or {}).get("next_cursor")
            if not next_cursor:
                stop_reason = "last_page"
                break
            cursor = next_cursor

        _logger.info(
            "openalex.works_page_complete researcher=%r author_id=%s parsed=%d pages_visited=%d stop_reason=%s",
            researcher_name,
            author_id,
            len(papers),
            pages_visited,
            stop_reason,
        )
        return papers[:max_results]

    def _work_to_candidate(self, work: dict) -> PaperCandidate | None:
        title = work.get("display_name") or work.get("title")
        if not title:
            return None

        authors = [authorship.get("author", {}).get("display_name") for authorship in work.get("authorships", []) if authorship.get("author", {}).get("display_name")]
        ids = work.get("ids") or {}
        doi = work.get("doi") or ids.get("doi")
        source_url = self._source_url(work)

        return PaperCandidate(
            title=title,
            abstract=_abstract_from_inverted_index(work.get("abstract_inverted_index")),
            authors=authors,
            publication_date=_parse_publication_date(work.get("publication_date")),
            source="openalex",
            source_url=source_url,
            doi=doi,
        )

    def _source_url(self, work: dict) -> str:
        for location_key in ("primary_location", "best_oa_location"):
            location = work.get(location_key) or {}
            landing_page_url = location.get("landing_page_url")
            if landing_page_url:
                return landing_page_url
        return work.get("id") or ""

    async def _get_json(self, path: str, params: dict) -> dict | None:
        request_params = dict(params)
        if self._mailto:
            request_params["mailto"] = self._mailto
        url = f"{_OPENALEX_API}{path}"
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(url, params=request_params)
        except httpx.RequestError as exc:
            _logger.warning("OpenAlex request failed path=%s: %s", path, exc)
            return None

        if not resp.is_success:
            _logger.warning("OpenAlex API %s path=%s url=%s", resp.status_code, path, resp.request.url)
            return None
        return resp.json()

    async def close(self) -> None:
        return None
