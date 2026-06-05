"""Unit tests for OllamaClient structured output helpers."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel, StrictStr, ValidationError

from app.llm.ollama_client import OllamaClient


class StructuredAnswer(BaseModel):
    answer: StrictStr


@pytest.mark.unit
@pytest.mark.asyncio
async def test_chat_structured_validates_json_response():
    client = OllamaClient(host="http://localhost:11434")
    client.chat = AsyncMock(return_value={"message": {"content": '{"answer": "ok"}'}})

    try:
        result = await client.chat_structured(
            "m",
            messages=[{"role": "user", "content": "hi"}],
            output_schema=StructuredAnswer,
        )
    finally:
        await client.aclose()

    assert result == StructuredAnswer(answer="ok")
    client.chat.assert_awaited_once_with(
        model="m",
        messages=[{"role": "user", "content": "hi"}],
        options=None,
        format="json",
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_chat_structured_rejects_invalid_schema():
    client = OllamaClient(host="http://localhost:11434")
    client.chat = AsyncMock(return_value={"message": {"content": '{"answer": 42}'}})

    try:
        with pytest.raises(ValidationError):
            await client.chat_structured(
                "m",
                messages=[{"role": "user", "content": "hi"}],
                output_schema=StructuredAnswer,
            )
    finally:
        await client.aclose()
