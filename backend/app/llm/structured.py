"""Helpers for validating structured LLM JSON output."""

from __future__ import annotations

import json
import re
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def parse_structured_content(content: str, output_schema: type[T]) -> T:
    """Parse a provider response body into a Pydantic model.

    Providers occasionally wrap JSON in markdown fences despite JSON mode. Keep
    the cleanup here so service code never owns provider quirks.
    """
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    data: Any = json.loads(text)
    return output_schema.model_validate(data)
