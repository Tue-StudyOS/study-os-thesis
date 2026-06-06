"""Typed LLM request and response models."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class LLMToolFunction(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class LLMToolCall(BaseModel):
    id: str | None = None
    function: LLMToolFunction


class LLMMessage(BaseModel):
    model_config = ConfigDict(extra="allow")

    role: str
    content: str | None = ""
    tool_calls: list[LLMToolCall] | None = None
    name: str | None = None
    tool_call_id: str | None = None


class LLMResponse(BaseModel):
    message: LLMMessage


T = TypeVar("T", bound=BaseModel)


class StructuredLLMOutput(BaseModel, Generic[T]):
    value: T
