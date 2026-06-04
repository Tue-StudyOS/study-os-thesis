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
from urllib.parse import quote_plus

from playwright.async_api import Browser, Page, async_playwright

from app.papers.domain import PaperCandidate, ResearcherInfo
from app.scraper.adapters.arxiv_client import extract_arxiv_id_from_url
from app.scraper.interfaces import PaperSourceClient

_logger = logging.getLogger(__name__)

# Google Scholar search URL — returns up to 10 results per page
_SCHOLAR_SEARCH = "https://scholar.google.com/scholar?q={query}&as_ylo={year}"
_SCHOLAR_PROFILE = "https://scholar.google.com/citations?user={user_id}&sortby=pubdate"


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
                papers = await self._scrape_profile(page, researcher.google_scholar_id, max_results)
            else:
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

    async def _scrape_profile(
        self,
        page: Page,
        scholar_id: str,
        max_results: int,
    ) -> list[PaperCandidate]:
        url = _SCHOLAR_PROFILE.format(user_id=scholar_id)
        await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        await asyncio.sleep(self._delay)

        # Keep clicking "Show more" until all rows are loaded or max_results reached.
        # Scholar loads 20 rows at a time; the button disappears when exhausted.
        while True:
            show_more = page.locator("button#gsc_bpf_more")
            # Stop if we already have enough rows in the DOM
            current_count = await page.locator("tr.gsc_a_tr").count()
            if current_count >= max_results:
                break
            if await show_more.count() == 0 or not await show_more.is_enabled():
                break
            await show_more.click()
            # Wait for new rows to appear — Scholar adds them asynchronously
            await page.wait_for_load_state("networkidle", timeout=10_000)
            await asyncio.sleep(self._delay)

        # Parse all rows now visible in the DOM
        rows = page.locator("tr.gsc_a_tr")
        total = min(await rows.count(), max_results)
        papers: list[PaperCandidate] = []
        for i in range(total):
            try:
                candidate = await self._parse_profile_row(rows.nth(i))
                if candidate:
                    papers.append(candidate)
            except Exception as exc:
                _logger.debug("Profile row parse error: %s", exc)

        return papers

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
        query = quote_plus(f'author:"{name}"')
        year_cutoff = _year_cutoff(since_days)
        url = _SCHOLAR_SEARCH.format(query=query, year=year_cutoff)

        await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        await asyncio.sleep(self._delay)

        papers: list[PaperCandidate] = []

        for _ in range(self._max_pages):
            new_papers = await self._parse_search_results(page)
            papers.extend(new_papers)

            if len(papers) >= max_results:
                break

            # Navigate to next page
            next_btn = page.locator("td.b > a:has-text('Next')")
            if await next_btn.count() == 0:
                break
            await next_btn.first.click()
            await asyncio.sleep(self._delay)

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
