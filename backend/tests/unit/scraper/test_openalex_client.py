"""Unit tests for OpenAlexSourceClient."""

import httpx
import pytest
import respx

from app.papers.domain import ResearcherInfo
from app.scraper.adapters.openalex_client import OpenAlexSourceClient


def _authors_response() -> dict:
    return {
        "results": [
            {
                "id": "https://openalex.org/A123",
                "display_name": "Georg Martius",
                "works_count": 227,
                "last_known_institutions": [{"display_name": "University of Tübingen"}],
            }
        ]
    }


def _works_response(results: list[dict], next_cursor: str | None = None) -> dict:
    return {"meta": {"next_cursor": next_cursor}, "results": results}


def _work(title: str, year: int, *, openalex_id: str = "https://openalex.org/W1") -> dict:
    return {
        "id": openalex_id,
        "display_name": title,
        "publication_date": f"{year}-01-15",
        "doi": "https://doi.org/10.123/example",
        "abstract_inverted_index": {"hello": [0], "world": [1]},
        "authorships": [{"author": {"display_name": "Georg Martius"}}],
        "primary_location": {"landing_page_url": "https://example.org/paper"},
    }


@pytest.mark.unit
class TestOpenAlexSourceClient:
    @respx.mock
    async def test_resolves_author_then_fetches_recent_works(self):
        author_route = respx.get("https://api.openalex.org/authors").mock(return_value=httpx.Response(200, json=_authors_response()))
        works_route = respx.get("https://api.openalex.org/works").mock(return_value=httpx.Response(200, json=_works_response([_work("Recent Paper", 2024)])))

        papers = await OpenAlexSourceClient().fetch_papers(
            ResearcherInfo(name="Prof. Dr. Georg Martius", affiliation="University of Tübingen"),
            max_results=10,
            since_days=3650,
        )

        assert author_route.call_count == 1
        assert works_route.call_count == 1
        author_url = str(author_route.calls[0].request.url)
        works_url = str(works_route.calls[0].request.url)
        assert "search=Georg+Martius" in author_url
        assert "author.id%3AA123" in works_url
        assert "from_publication_date" in works_url
        assert "sort=publication_date%3Adesc" in works_url
        assert papers[0].source == "openalex"
        assert papers[0].title == "Recent Paper"
        assert papers[0].abstract == "hello world"
        assert papers[0].authors == ["Georg Martius"]
        assert papers[0].doi == "https://doi.org/10.123/example"

    @respx.mock
    async def test_paginates_with_cursor_until_max_results(self):
        respx.get("https://api.openalex.org/authors").mock(return_value=httpx.Response(200, json=_authors_response()))
        works_route = respx.get("https://api.openalex.org/works").mock(
            side_effect=[
                httpx.Response(200, json=_works_response([_work("First", 2024)], next_cursor="next")),
                httpx.Response(200, json=_works_response([_work("Second", 2024, openalex_id="https://openalex.org/W2")], next_cursor=None)),
            ]
        )

        papers = await OpenAlexSourceClient(page_size=1).fetch_papers(ResearcherInfo(name="Georg Martius"), max_results=2, since_days=3650)

        assert works_route.call_count == 2
        assert "cursor=%2A" in str(works_route.calls[0].request.url)
        assert "cursor=next" in str(works_route.calls[1].request.url)
        assert [paper.title for paper in papers] == ["First", "Second"]

    @respx.mock
    async def test_no_author_match_returns_empty(self):
        respx.get("https://api.openalex.org/authors").mock(return_value=httpx.Response(200, json={"results": []}))

        papers = await OpenAlexSourceClient().fetch_papers(ResearcherInfo(name="Unknown Person"), max_results=10, since_days=3650)

        assert papers == []

    @respx.mock
    async def test_work_without_title_is_skipped(self):
        respx.get("https://api.openalex.org/authors").mock(return_value=httpx.Response(200, json=_authors_response()))
        respx.get("https://api.openalex.org/works").mock(return_value=httpx.Response(200, json=_works_response([{"id": "https://openalex.org/W1"}])))

        papers = await OpenAlexSourceClient().fetch_papers(ResearcherInfo(name="Georg Martius"), max_results=10, since_days=3650)

        assert papers == []
