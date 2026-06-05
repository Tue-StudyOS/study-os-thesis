"""Unit tests for LiteLLMAdapter internals."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.llm.litellm_adapter import LiteLLMAdapter, _to_openai_messages


# ---------------------------------------------------------------------------
# _to_openai_messages
# ---------------------------------------------------------------------------


class TestToOpenAIMessages:
    def test_plain_messages_pass_through(self):
        msgs = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "Hello"},
        ]
        assert _to_openai_messages(msgs) == msgs

    def test_tool_call_args_serialised_to_string(self):
        msgs = [
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"function": {"name": "search", "arguments": {"q": "test"}}}],
            }
        ]
        result = _to_openai_messages(msgs)
        args = result[0]["tool_calls"][0]["function"]["arguments"]
        assert isinstance(args, str)
        assert json.loads(args) == {"q": "test"}

    def test_tool_call_already_string_args_unchanged(self):
        raw = json.dumps({"q": "test"})
        msgs = [
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"function": {"name": "search", "arguments": raw}}],
            }
        ]
        result = _to_openai_messages(msgs)
        assert result[0]["tool_calls"][0]["function"]["arguments"] == raw

    def test_tool_call_gets_id_and_type(self):
        msgs = [
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"function": {"name": "foo", "arguments": {}}}],
            }
        ]
        tc = _to_openai_messages(msgs)[0]["tool_calls"][0]
        assert "id" in tc
        assert tc["type"] == "function"

    def test_existing_tool_call_id_preserved(self):
        msgs = [
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"id": "my_id", "function": {"name": "foo", "arguments": {}}}],
            }
        ]
        tc = _to_openai_messages(msgs)[0]["tool_calls"][0]
        assert tc["id"] == "my_id"

    def test_tool_result_gets_matching_tool_call_id(self):
        msgs = [
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"function": {"name": "foo", "arguments": {}}}],
            },
            {"role": "tool", "name": "foo", "content": "result"},
        ]
        result = _to_openai_messages(msgs)
        call_id = result[0]["tool_calls"][0]["id"]
        assert result[1]["tool_call_id"] == call_id

    def test_multiple_tool_calls_matched_in_order(self):
        msgs = [
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {"function": {"name": "a", "arguments": {}}},
                    {"function": {"name": "b", "arguments": {}}},
                ],
            },
            {"role": "tool", "name": "a", "content": "result_a"},
            {"role": "tool", "name": "b", "content": "result_b"},
        ]
        result = _to_openai_messages(msgs)
        id_a = result[0]["tool_calls"][0]["id"]
        id_b = result[0]["tool_calls"][1]["id"]
        assert result[1]["tool_call_id"] == id_a
        assert result[2]["tool_call_id"] == id_b

    def test_two_sequential_tool_turns(self):
        """IDs across two back-to-back tool-calling turns stay unique and correct."""
        msgs = [
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"function": {"name": "a", "arguments": {}}}],
            },
            {"role": "tool", "name": "a", "content": "r1"},
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"function": {"name": "b", "arguments": {}}}],
            },
            {"role": "tool", "name": "b", "content": "r2"},
        ]
        result = _to_openai_messages(msgs)
        id_first = result[0]["tool_calls"][0]["id"]
        id_second = result[2]["tool_calls"][0]["id"]
        assert id_first != id_second
        assert result[1]["tool_call_id"] == id_first
        assert result[3]["tool_call_id"] == id_second

    def test_existing_tool_call_id_on_result_not_overwritten(self):
        msgs = [
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"function": {"name": "foo", "arguments": {}}}],
            },
            {"role": "tool", "name": "foo", "content": "r", "tool_call_id": "existing"},
        ]
        result = _to_openai_messages(msgs)
        assert result[1]["tool_call_id"] == "existing"


# ---------------------------------------------------------------------------
# LiteLLMAdapter.chat — reasoning_effort kwarg reaches acompletion
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_deepseek_reasoning_effort_forwarded():
    """reasoning_effort='high' must be forwarded to litellm.acompletion."""
    mock_msg = MagicMock()
    mock_msg.content = "answer"
    mock_msg.tool_calls = None
    mock_msg.reasoning_content = None

    mock_choice = MagicMock()
    mock_choice.message = mock_msg

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = mock_response

        adapter = LiteLLMAdapter(
            chat_model="deepseek/deepseek-v4-pro",
            embed_model="deepseek/deepseek-v4-pro",
            chat_kwargs={"reasoning_effort": "high"},
        )
        await adapter.chat("deepseek-v4-pro", messages=[{"role": "user", "content": "hi"}])

        _, kwargs = mock_acompletion.call_args
        assert kwargs.get("reasoning_effort") == "high"


@pytest.mark.asyncio
async def test_deepseek_no_extra_body_thinking():
    """extra_body with thinking must NOT be present — reasoning_effort is sufficient."""
    mock_msg = MagicMock()
    mock_msg.content = "answer"
    mock_msg.tool_calls = None
    mock_msg.reasoning_content = None

    mock_choice = MagicMock()
    mock_choice.message = mock_msg

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = mock_response

        adapter = LiteLLMAdapter(
            chat_model="deepseek/deepseek-v4-pro",
            embed_model="deepseek/deepseek-v4-pro",
            chat_kwargs={"reasoning_effort": "high"},
        )
        await adapter.chat("deepseek-v4-pro", messages=[{"role": "user", "content": "hi"}])

        _, kwargs = mock_acompletion.call_args
        extra_body = kwargs.get("extra_body", {})
        assert "thinking" not in extra_body, "extra_body should not contain 'thinking'; reasoning_effort handles this"
