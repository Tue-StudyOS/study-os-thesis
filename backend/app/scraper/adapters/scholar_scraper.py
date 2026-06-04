"""Google Scholar scraper using Playwright.

Navigates Google Scholar search results for a given researcher and extracts
paper candidates. The scraper is rate-limited and resilient against common
failures (missing elements, navigation timeouts).

Important: Each call to `fetch_papers` creates and destroys its own browser
context, making it safe to run from Celery prefork workers (each task gets
a fresh event loop via asyncio.run()).
"""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime, timezone
from urllib.parse import parse_qs, quote_plus, urlparse

from playwright.async_api import Browser, Page, async_playwright

from app.papers.domain import PaperCandidate, ResearcherInfo
from app.scraper.adapters.arxiv_client import extract_arxiv_id_from_url
from app.scraper.interfaces import PaperSourceClient

_logger = logging.getLogger(__name__)

# Google Scholar search URL — returns up to 10 results per page
_SCHOLAR_SEARCH = "https://scholar.google.com/scholar?q={query}&as_ylo={year}"
_SCHOLAR_PROFILE = "https://scholar.google.com/citations?user={user_id}&hl=de&sortby=pubdate&cstart={cstart}&pagesize={pagesize}"
_SCHOLAR_AUTHOR_SEARCH = "https://scholar.google.com/citations?view_op=search_authors&hl=de&mauthors={query}&btnG="
_PROFILE_PAGE_SIZE = 100
_KNOWN_SCHOLAR_PROFILE_IDS = {
    "georg martius": "b-JF-UIAAAAJ",
}


def _strip_leading_titles_for_search(name: str) -> str:
    """Return a canonical name for Scholar search (strip leading academic titles)."""

    import re

    s = (name or "").strip()
    return re.sub(r"^\s*(?:(?:Professor|Prof)\.?\s*|Dr(?:\.-Ing\.)?\.?\s*)+", "", s, flags=re.IGNORECASE).strip()


def _year_cutoff(since_days: int) -> int:
    return datetime.now(timezone.utc).year - (since_days // 365)


def _parse_year_from_meta(meta: str) -> int | None:
    """Extract a 4-digit year from Scholar's author/venue/year line."""
    m = re.search(r"\b(20\d{2}|19\d{2})\b", meta)
    return int(m.group(1)) if m else None


def _parse_authors_from_meta(meta: str) -> list[str]:
    """Extract author names from the Scholar meta line.

    The meta line has the form:  "A Author, B Author - Venue, Year - Publisher"
    We take the part before the first dash and split by comma.
    """
    parts = meta.split(" - ")
    if not parts:
        return []
    author_part = parts[0]
    # Strip trailing ellipsis ("…") that Scholar sometimes adds
    authors = [a.strip().rstrip("…") for a in author_part.split(",") if a.strip()]
    return authors


def _normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", name.lower())).strip()


def _known_profile_id_for_name(name: str) -> str | None:
    return _KNOWN_SCHOLAR_PROFILE_IDS.get(_normalize_name(_strip_leading_titles_for_search(name) or name))


class ScholarPlaywrightScraper(PaperSourceClient):
    """Scrapes Google Scholar search results using Playwright.

    Two discovery modes (tried in order):
      1. Author profile page  — if google_scholar_id is known (most reliable)
      2. Author search query  — fallback using researcher name
    """

    def __init__(
        self,
        headless: bool = True,
        request_delay: float = 3.0,
        max_pages: int = 3,
    ) -> None:
        self._headless = headless
        self._delay = request_delay
        self._max_pages = max_pages
        # Browser is created lazily and held across calls if the scraper
        # instance is long-lived; destroyed in close().
        self._browser: Browser | None = None
        self._pw: object | None = None

    async def _ensure_browser(self) -> Browser:
        if self._browser is None:
            self._pw = await async_playwright().start()
            self._browser = await self._pw.chromium.launch(  # type: ignore[union-attr]
                headless=self._headless,
                args=["--no-sandbox", "--disable-setuid-sandbox"],
            )
        return self._browser

    async def fetch_papers(
        self,
        researcher: ResearcherInfo,
        *,
        max_results: int = 20,
        since_days: int = 365,
    ) -> list[PaperCandidate]:
        browser = await self._ensure_browser()
        context = await browser.new_context(user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = await context.new_page()
        papers: list[PaperCandidate] = []

        try:
            if researcher.google_scholar_id:
                _logger.info(
                    "scholar.path profile_configured researcher=%r profile_id=%s max_results=%d since_days=%d",
                    researcher.name,
                    researcher.google_scholar_id,
                    max_results,
                    since_days,
                )
                papers = await self._scrape_profile(page, researcher.google_scholar_id, max_results, since_days)
            else:
                scholar_id = await self._discover_profile_id(page, researcher.name, researcher.affiliation)
                if scholar_id is None:
                    scholar_id = _known_profile_id_for_name(researcher.name)
                    if scholar_id:
                        _logger.info(
                            "scholar.path profile_known_alias researcher=%r profile_id=%s max_results=%d since_days=%d",
                            researcher.name,
                            scholar_id,
                            max_results,
                            since_days,
                        )
                if scholar_id:
                    researcher.google_scholar_id = scholar_id
                    _logger.info(
                        "scholar.path profile_discovered researcher=%r profile_id=%s max_results=%d since_days=%d",
                        researcher.name,
                        scholar_id,
                        max_results,
                        since_days,
                    )
                    papers = await self._scrape_profile(page, scholar_id, max_results, since_days)
                else:
                    _logger.info(
                        "scholar.path search_fallback researcher=%r max_results=%d since_days=%d",
                        researcher.name,
                        max_results,
                        since_days,
                    )
                    papers = await self._scrape_search(page, researcher.name, since_days, max_results)
        except Exception as exc:
            _logger.warning(
                "Scholar scrape failed for researcher=%r: %s",
                researcher.name,
                exc,
                exc_info=True,
            )
        finally:
            await page.close()
            await context.close()

        _logger.info(
            "Scholar returned %d candidates for researcher=%r",
            len(papers),
            researcher.name,
        )
        return papers

    # ------------------------------------------------------------------
    # Profile-based scraping (preferred — sorted by publication date)
    # ------------------------------------------------------------------

    async def _discover_profile_id(
        self,
        page: Page,
        name: str,
        affiliation: str | None = None,
    ) -> str | None:
        search_name = _strip_leading_titles_for_search(name)
        normalized_search_name = _normalize_name(search_name or name)
        query = quote_plus(search_name or name)
        url = _SCHOLAR_AUTHOR_SEARCH.format(query=query)

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
            await asyncio.sleep(self._delay)
            name_links = page.locator("h3.gs_ai_name a[href*='user='], .gs_ai_name a[href*='user='], a[href*='/citations?user='], a[href*='citations?user=']")
            link_count = await name_links.count()
            _logger.info(
                "scholar.author_lookup researcher=%r query=%r profile_link_count=%d url=%s title=%r",
                name,
                search_name or name,
                link_count,
                page.url,
                await page.title(),
            )
            candidates: list[tuple[int, str]] = []

            for i in range(link_count):
                name_link = name_links.nth(i)
                profile_name = (await name_link.inner_text()).strip()
                normalized_profile_name = _normalize_name(profile_name)
                if normalized_search_name not in normalized_profile_name and normalized_profile_name not in normalized_search_name:
                    continue

                score = 10
                if affiliation:
                    sibling_text = ""
                    card = name_link.locator("xpath=ancestor::*[contains(@class, 'gs_ai_t') or contains(@class, 'gsc_1usr') or contains(@class, 'gs_ai_chpr')][1]")
                    if await card.count() > 0:
                        sibling_text = (await card.first.inner_text()).strip().lower()
                    affiliation_tokens = [token for token in re.split(r"\W+", affiliation.lower()) if len(token) >= 4]
                    if affiliation_tokens and any(token in sibling_text for token in affiliation_tokens):
                        score += 5

                href = await name_link.get_attribute("href") or ""
                parsed = urlparse(href)
                user = parse_qs(parsed.query).get("user")
                if user and user[0]:
                    candidates.append((score, user[0]))

            if candidates:
                best = max(candidates, key=lambda item: item[0])[1]
                _logger.info(
                    "scholar.author_lookup_match researcher=%r profile_id=%s candidates=%d",
                    name,
                    best,
                    len(candidates),
                )
                return best
            _logger.info("scholar.author_lookup_no_match researcher=%r profile_link_count=%d", name, link_count)
        except Exception as exc:
            _logger.info("Scholar author profile lookup failed for researcher=%r: %s", name, exc)

        return None

    async def _scrape_profile(
        self,
        page: Page,
        scholar_id: str,
        max_results: int,
        since_days: int,
    ) -> list[PaperCandidate]:
        cutoff_year = _year_cutoff(since_days)
        papers: list[PaperCandidate] = []
        pages_visited = 0
        stop_reason = "unknown"

        for cstart in range(0, max_results, _PROFILE_PAGE_SIZE):
            url = _SCHOLAR_PROFILE.format(
                user_id=scholar_id,
                cstart=cstart,
                pagesize=min(_PROFILE_PAGE_SIZE, max_results - cstart),
            )
            await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
            await asyncio.sleep(self._delay)

            pages_visited += 1
            rows = page.locator("tr.gsc_a_tr")
            page_total = await rows.count()
            if page_total == 0:
                stop_reason = "empty_page"
                break

            reached_cutoff = False
            page_papers = 0
            for i in range(page_total):
                try:
                    candidate = await self._parse_profile_row(rows.nth(i))
                    if candidate is None:
                        continue
                    if candidate.publication_date and candidate.publication_date.year < cutoff_year:
                        reached_cutoff = True
                        stop_reason = "cutoff_year"
                        break
                    papers.append(candidate)
                    page_papers += 1
                except Exception as exc:
                    _logger.debug("Profile row parse error: %s", exc)
                if len(papers) >= max_results:
                    stop_reason = "max_results"
                    break

            if len(papers) >= max_results or reached_cutoff:
                break
            if page_total < _PROFILE_PAGE_SIZE or page_papers == 0:
                stop_reason = "last_page"
                break

        if stop_reason == "unknown":
            stop_reason = "max_results"
        _logger.info(
            "scholar.profile_complete profile_id=%s parsed=%d pages_visited=%d page_size=%d stop_reason=%s max_results=%d since_days=%d",
            scholar_id,
            len(papers),
            pages_visited,
            _PROFILE_PAGE_SIZE,
            stop_reason,
            max_results,
            since_days,
        )
        return papers[:max_results]

    async def _parse_profile_row(self, row: object) -> PaperCandidate | None:
        from playwright.async_api import Locator

        row_loc: Locator = row  # type: ignore[assignment]

        title_el = row_loc.locator("a.gsc_a_at")
        if await title_el.count() == 0:
            return None

        title = (await title_el.inner_text()).strip()
        href = await title_el.get_attribute("href") or ""
        # Scholar profile links are internal (/citations?view_op=...) — no direct paper URL
        # We'll resolve the arxiv_id later via the ArxivMetadataEnricher if available

        # Authors / venue — shown in .gs_gray spans
        meta_els = row_loc.locator(".gs_gray")
        authors: list[str] = []
        year: int | None = None

        if await meta_els.count() >= 1:
            authors_text = await meta_els.nth(0).inner_text()
            authors = [a.strip() for a in authors_text.split(",") if a.strip()]
        if await meta_els.count() >= 2:
            year_text = await meta_els.nth(1).inner_text()
            m = re.search(r"\b(20\d{2}|19\d{2})\b", year_text)
            if m:
                year = int(m.group(1))

        year_dt = datetime(year, 1, 1, tzinfo=timezone.utc) if year else None

        # Try to detect arXiv link in href
        arxiv_id = extract_arxiv_id_from_url(href) if href else None

        return PaperCandidate(
            title=title,
            authors=authors,
            publication_date=year_dt,
            source="google_scholar",
            source_url=f"https://scholar.google.com{href}" if href.startswith("/") else href,
            arxiv_id=arxiv_id,
        )

    # ------------------------------------------------------------------
    # Search-based scraping (fallback — searches by author name)
    # ------------------------------------------------------------------

    async def _scrape_search(
        self,
        page: Page,
        name: str,
        since_days: int,
        max_results: int,
    ) -> list[PaperCandidate]:
        search_name = _strip_leading_titles_for_search(name)
        if search_name and search_name != name:
            _logger.info("Scholar search: stripped titles %r -> %r", name, search_name)
        query = quote_plus(f'author:"{search_name or name}"')
        year_cutoff = _year_cutoff(since_days)
        url = _SCHOLAR_SEARCH.format(query=query, year=year_cutoff)

        await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        await asyncio.sleep(self._delay)

        papers: list[PaperCandidate] = []

        stop_reason = "max_pages"
        pages_visited = 0
        for _ in range(self._max_pages):
            pages_visited += 1
            new_papers = await self._parse_search_results(page)
            papers.extend(new_papers)

            if len(papers) >= max_results:
                stop_reason = "max_results"
                break

            # Navigate to next page
            next_btn = page.locator("td.b > a[href*='start='], a[aria-label*='Next'], a:has-text('Next')").first
            if await next_btn.count() == 0:
                stop_reason = "next_unavailable"
                break
            await next_btn.click()
            await page.wait_for_load_state("domcontentloaded", timeout=10_000)
            await asyncio.sleep(self._delay)

        if len(papers) == 10 and max_results > 10:
            _logger.warning(
                "scholar.search_fallback_returned_first_page_only researcher=%r pages_visited=%d stop_reason=%s max_results=%d",
                name,
                pages_visited,
                stop_reason,
                max_results,
            )
        _logger.info(
            "scholar.search_complete researcher=%r parsed=%d pages_visited=%d stop_reason=%s max_results=%d since_days=%d",
            name,
            min(len(papers), max_results),
            pages_visited,
            stop_reason,
            max_results,
            since_days,
        )
        return papers[:max_results]

    async def _parse_search_results(self, page: Page) -> list[PaperCandidate]:
        """Extract paper candidates from a Scholar search results page."""
        entries = page.locator("div.gs_r.gs_or.gs_scl")
        papers: list[PaperCandidate] = []

        for i in range(await entries.count()):
            entry = entries.nth(i)
            try:
                # Title and link
                title_link = entry.locator("h3.gs_rt a").first
                if await title_link.count() == 0:
                    continue

                title = (await title_link.inner_text()).strip()
                href = (await title_link.get_attribute("href")) or ""

                # Meta line: "A Author, B Author - Journal, Year - Publisher"
                meta_el = entry.locator("div.gs_a")
                meta = (await meta_el.inner_text()).strip() if await meta_el.count() > 0 else ""

                authors = _parse_authors_from_meta(meta)
                year = _parse_year_from_meta(meta)
                year_dt = datetime(year, 1, 1, tzinfo=timezone.utc) if year else None

                arxiv_id = extract_arxiv_id_from_url(href) if href else None

                papers.append(
                    PaperCandidate(
                        title=title,
                        authors=authors,
                        publication_date=year_dt,
                        source="google_scholar",
                        source_url=href,
                        arxiv_id=arxiv_id,
                    )
                )
            except Exception as exc:
                _logger.debug("Search result parse error (entry %d): %s", i, exc)
                continue

        return papers

    async def close(self) -> None:
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._pw:
            await self._pw.stop()  # type: ignore[union-attr]
            self._pw = None
