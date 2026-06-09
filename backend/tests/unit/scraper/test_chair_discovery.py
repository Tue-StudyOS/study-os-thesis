"""Unit tests for chair discovery scraping adapter."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.scraper.adapters.chair_discovery import ChairDiscoveryAdapter


@pytest.fixture
def mock_llm_port() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def chair_discovery(mock_llm_port) -> ChairDiscoveryAdapter:
    return ChairDiscoveryAdapter(llm_port=mock_llm_port)


@pytest.mark.unit
class TestChairDiscoveryAdapter:
    async def test_discover_researchers_fetches_and_extracts(self, chair_discovery, mock_llm_port):
        """Test that adapter fetches URL and extracts researchers via LLM."""
        mock_llm_port.chat_structured.return_value = {
            "employees": [
                {
                    "name": "Alice Smith",
                    "title": "Prof. Dr.",
                    "role": "Professor",
                    "email": "alice@example.com",
                    "profile_url": "https://example.com/alice",
                },
                {
                    "name": "Bob Jones",
                    "title": None,
                    "role": "Research Associate",
                    "email": "bob@example.com",
                    "profile_url": "https://example.com/bob",
                },
            ]
        }

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.text = "<html>Team page</html>"
            mock_response.status_code = 200
            mock_get.return_value.__aenter__.return_value = mock_response

            researchers = await chair_discovery.discover_researchers("https://example.com/team")

            assert len(researchers) == 2
            assert researchers[0].name == "Alice Smith"
            assert researchers[0].profile_url == "https://example.com/alice"
            assert researchers[1].name == "Bob Jones"
            mock_llm_port.chat_structured.assert_awaited_once()

    async def test_discover_researchers_sets_source_url(self, chair_discovery, mock_llm_port):
        """Test that source_url is set to the fetched URL."""
        mock_llm_port.chat_structured.return_value = {
            "employees": [
                {
                    "name": "Charlie",
                    "title": None,
                    "role": "PhD Student",
                    "email": None,
                    "profile_url": None,
                }
            ]
        }

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.text = "<html></html>"
            mock_response.status_code = 200
            mock_get.return_value.__aenter__.return_value = mock_response

            researchers = await chair_discovery.discover_researchers("https://example.com/team")

            assert researchers[0].source_url == "https://example.com/team"

    async def test_discover_researchers_handles_empty_response(self, chair_discovery, mock_llm_port):
        """Test handling of empty employee list from LLM."""
        mock_llm_port.chat_structured.return_value = {"employees": []}

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.text = "<html></html>"
            mock_response.status_code = 200
            mock_get.return_value.__aenter__.return_value = mock_response

            researchers = await chair_discovery.discover_researchers("https://example.com/team")

            assert len(researchers) == 0
