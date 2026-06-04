"""Unit tests for LLMPaperEnricher."""

from unittest.mock import AsyncMock

import pytest

from app.scraper.adapters.llm_enricher import LLMPaperEnricher


def _make_llm(content: str = "result") -> AsyncMock:
    mock = AsyncMock()
    mock.chat.return_value = {"message": {"role": "assistant", "content": content}}
    return mock


@pytest.mark.unit
class TestSummarize:
    async def test_returns_stripped_content(self):
        llm = _make_llm("  This paper proposes a new method.  ")
        enricher = LLMPaperEnricher(llm, "test-model")
        result = await enricher.summarize("Title", "Abstract text")
        assert result == "This paper proposes a new method."

    async def test_prompt_contains_title_and_abstract(self):
        llm = _make_llm("summary")
        enricher = LLMPaperEnricher(llm, "test-model")
        await enricher.summarize("My Paper Title", "My abstract text here")

        call_args = llm.chat.call_args
        prompt = call_args[0][1][0]["content"]  # messages[0]["content"]
        assert "My Paper Title" in prompt
        assert "My abstract text here" in prompt

    async def test_uses_configured_model_name(self):
        llm = _make_llm("summary")
        enricher = LLMPaperEnricher(llm, "gemma4:26b")
        await enricher.summarize("T", "A")

        assert llm.chat.call_args[0][0] == "gemma4:26b"

    async def test_llm_exception_returns_empty_string(self):
        llm = AsyncMock()
        llm.chat.side_effect = ConnectionError("Ollama offline")
        enricher = LLMPaperEnricher(llm, "model")
        result = await enricher.summarize("Title", "Abstract")
        assert result == ""

    async def test_low_temperature_requested(self):
        llm = _make_llm("s")
        enricher = LLMPaperEnricher(llm, "m")
        await enricher.summarize("T", "A")

        options = llm.chat.call_args.kwargs.get("options") or llm.chat.call_args[1].get("options", {})
        assert options.get("temperature", 1.0) <= 0.5


@pytest.mark.unit
class TestGenerateTags:
    async def test_exact_canonical_tag_returned(self):
        llm = _make_llm('["machine learning"]')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("Title", "Abstract")
        assert tags == ["machine learning"]

    async def test_multiple_canonical_tags_returned(self):
        llm = _make_llm('["robotics", "optimization", "deep learning"]')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert set(tags) == {"robotics", "optimization", "deep learning"}

    async def test_fuzzy_match_near_canonical(self):
        # "machine-learning" should fuzzy-match "machine learning"
        llm = _make_llm('["machine-learning"]')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert "machine learning" in tags

    async def test_unrecognized_tag_discarded(self):
        # "astrophysics" has no close match in canonical tags
        llm = _make_llm('["astrophysics"]')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert tags == []

    async def test_duplicates_removed(self):
        llm = _make_llm('["deep learning", "deep learning", "robotics"]')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert tags.count("deep learning") == 1

    async def test_markdown_code_fence_stripped(self):
        llm = _make_llm('```json\n["robotics"]\n```')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert "robotics" in tags

    async def test_json_fallback_from_prose_response(self):
        # LLM ignores instructions and wraps the answer in prose
        llm = _make_llm('Sure! Here are the tags: "robotics", "optimization"')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert "robotics" in tags
        assert "optimization" in tags

    async def test_completely_unparseable_returns_empty(self):
        llm = _make_llm("I cannot determine any tags for this paper.")
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert tags == []

    async def test_non_string_items_in_array_ignored(self):
        llm = _make_llm('[1, "robotics", null, true]')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert tags == ["robotics"]

    async def test_llm_exception_returns_empty_list(self):
        llm = AsyncMock()
        llm.chat.side_effect = TimeoutError("timeout")
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert tags == []

    async def test_prompt_contains_closed_vocabulary(self):
        llm = _make_llm('["robotics"]')
        enricher = LLMPaperEnricher(llm, "model")
        await enricher.generate_tags("T", "A")

        prompt = llm.chat.call_args[0][1][0]["content"]
        # Spot-check several canonical tags appear in the prompt
        for tag in ["robotics", "machine learning", "optimization"]:
            assert tag in prompt

    async def test_case_insensitive_normalization(self):
        llm = _make_llm('["Machine Learning", "ROBOTICS"]')
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert "machine learning" in tags
        assert "robotics" in tags

    async def test_very_long_llm_response_doesnt_crash(self):
        # LLM returns a huge JSON-like string
        llm = _make_llm('["robotics"] and here is a very long explanation ' + "x" * 2000)
        enricher = LLMPaperEnricher(llm, "model")
        tags = await enricher.generate_tags("T", "A")
        assert isinstance(tags, list)
