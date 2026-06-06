"""LiteLLM-based adapter that satisfies LLMPort.

LiteLLM provides a unified interface to 100+ LLM providers (Azure OpenAI,
DeepSeek, Ollama, OpenAI, Anthropic, …).  This adapter wraps
``litellm.acompletion`` and ``litellm.aembedding`` and normalises their
OpenAI-format responses into the Ollama dict shape that the service layer
already expects::

    {"message": {"role": "assistant", "content": "...", "tool_calls": [...]}}

Supported providers and their litellm model name prefixes
---------------------------------------------------------
- Ollama     : ``ollama_chat/<model>``   (e.g. ``ollama_chat/gemma4:26b``)
- Azure      : ``azure/<deployment>``    (e.g. ``azure/gpt-4o``)
- DeepSeek   : ``deepseek/<model>``      (e.g. ``deepseek/deepseek-chat``)

The factory (``app.llm.factory``) constructs instances of this class with the
correct model names and provider-specific kwargs.
"""

import json
import logging
from typing import Any, TypeVar

import litellm
from pydantic import BaseModel

from app.llm.litellm_constants import LITELLM_JSON_RESPONSE_FORMAT, LITELLM_SYNTHETIC_TOOL_CALL_PREFIX
from app.llm.structured import parse_structured_content

T = TypeVar("T", bound=BaseModel)
_logger = logging.getLogger(__name__)

# Suppress litellm's verbose internal logging by default.
litellm.suppress_debug_info = True


def _normalise_tool_calls(
    tool_calls: list[Any],
) -> list[dict[str, Any]]:
    """Convert LiteLLM/OpenAI tool_call objects to Ollama's dict shape.

    LiteLLM returns ``ChatCompletionMessageToolCall`` pydantic objects with:
        .function.name  (str)
        .function.arguments  (str — JSON encoded)

    Ollama returns plain dicts with:
        {"function": {"name": str, "arguments": dict}}

    We convert to the Ollama shape so the service layer is unaffected.
    """
    result: list[dict[str, Any]] = []
    for tc in tool_calls:
        try:
            fn = tc.function
            import json

            args: Any = fn.arguments
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            result.append(
                {
                    "function": {
                        "name": fn.name,
                        "arguments": args,
                    }
                }
            )
        except Exception as exc:
            _logger.warning("Could not normalise tool call %r: %s", tc, exc)
    return result


def _to_openai_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Translate Ollama-shaped messages into OpenAI/DeepSeek-compatible shape.

    The service layer builds messages in Ollama's dict shape (tool_call
    arguments are a dict, tool results carry only a ``name``).  OpenAI-compatible
    providers require:
      - each assistant ``tool_calls`` entry to have ``id`` + ``type`` and
        ``function.arguments`` encoded as a JSON *string*;
      - each ``tool`` result message to carry the matching ``tool_call_id``.

    Tool-call ids are synthesised and matched to the following tool results by
    order (the agent loop appends tool results immediately after the assistant
    turn that requested them, in the same order).
    """
    out: list[dict[str, Any]] = []
    pending_ids: list[str] = []
    counter = 0

    for msg in messages:
        tool_calls = msg.get("tool_calls")
        if msg.get("role") == "assistant" and tool_calls:
            converted: list[dict[str, Any]] = []
            for tc in tool_calls:
                fn = tc.get("function", {}) or {}
                args = fn.get("arguments", {})
                if not isinstance(args, str):
                    args = json.dumps(args)
                call_id = tc.get("id") or f"{LITELLM_SYNTHETIC_TOOL_CALL_PREFIX}_{counter}"
                counter += 1
                pending_ids.append(call_id)
                converted.append({"id": call_id, "type": "function", "function": {"name": fn.get("name", ""), "arguments": args}})
            new_msg = dict(msg)
            new_msg["tool_calls"] = converted
            out.append(new_msg)
        elif msg.get("role") == "tool":
            new_msg = dict(msg)
            if "tool_call_id" not in new_msg and pending_ids:
                new_msg["tool_call_id"] = pending_ids.pop(0)
            out.append(new_msg)
        else:
            out.append(msg)

    return out


class LiteLLMAdapter:
    """Provider-agnostic LLM adapter built on top of LiteLLM.

    Parameters
    ----------
    chat_model:
        The fully-qualified litellm model string used for ``chat()`` calls.
        Examples: ``"ollama_chat/gemma4:26b"``, ``"azure/gpt-4o"``,
        ``"deepseek/deepseek-chat"``.
    embed_model:
        The fully-qualified litellm model string used for ``embed()`` calls.
        Examples: ``"ollama/qwen3-embedding:4b"``,
        ``"azure/text-embedding-3-small"``.
    **kwargs:
        Extra kwargs forwarded to every litellm call (``api_base``,
        ``api_key``, ``api_version``, …).  Provider-specific kwargs can be
        split via ``chat_kwargs`` / ``embed_kwargs`` if they differ between
        the two operations.
    chat_kwargs:
        Additional kwargs forwarded only to ``acompletion`` calls.
    embed_kwargs:
        Additional kwargs forwarded only to ``aembedding`` calls.
    """

    def __init__(
        self,
        chat_model: str,
        embed_model: str,
        chat_kwargs: dict[str, Any] | None = None,
        embed_kwargs: dict[str, Any] | None = None,
        **shared_kwargs: Any,
    ) -> None:
        self._chat_model = chat_model
        self._embed_model = embed_model
        self._chat_kwargs: dict[str, Any] = {**shared_kwargs, **(chat_kwargs or {})}
        self._embed_kwargs: dict[str, Any] = {**shared_kwargs, **(embed_kwargs or {})}

    async def chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        options: dict[str, Any] | None = None,
        format: str | None = None,
    ) -> dict[str, Any]:
        """Execute a single non-streamed chat turn via LiteLLM.

        The *model* parameter mirrors the OllamaClient signature (the caller
        passes the configured model name).  We use ``self._chat_model``
        internally so that the provider prefix is always correct regardless of
        what the caller passes in — this keeps Settings usage identical to the
        Ollama path.
        """
        kwargs: dict[str, Any] = dict(self._chat_kwargs)
        if tools:
            kwargs["tools"] = tools
        # Map Ollama's JSON output mode to the OpenAI-compatible response_format.
        if format == "json":
            kwargs["response_format"] = LITELLM_JSON_RESPONSE_FORMAT
        # Map Ollama-style options (num_predict, temperature, …) to OpenAI params.
        if options:
            if "temperature" in options:
                kwargs["temperature"] = options["temperature"]
            if "num_predict" in options:
                kwargs["max_tokens"] = options["num_predict"]

        response = await litellm.acompletion(
            model=self._chat_model,
            messages=_to_openai_messages(messages),
            stream=False,
            **kwargs,
        )

        # Normalise OpenAI ModelResponse → Ollama dict shape.
        msg = response.choices[0].message
        result: dict[str, Any] = {
            "role": msg.role or "assistant",
            "content": msg.content or "",
        }
        if msg.tool_calls:
            result["tool_calls"] = _normalise_tool_calls(msg.tool_calls)
        # DeepSeek thinking mode: the reasoning trace must be echoed back on the
        # assistant message within the same tool-calling turn. Surface it so the
        # caller can replay it (see _to_openai_messages).
        reasoning = getattr(msg, "reasoning_content", None)
        if reasoning:
            result["reasoning_content"] = reasoning

        return {"message": result}

    async def embed(self, model: str, text: str) -> list[float]:
        """Return one embedding vector for *text* via LiteLLM.

        Like ``chat()``, the *model* parameter is accepted for API compatibility
        but the adapter uses ``self._embed_model`` to ensure the correct provider
        prefix.
        """
        response = await litellm.aembedding(
            model=self._embed_model,
            input=[text],
            **self._embed_kwargs,
        )
        return list(response.data[0]["embedding"])

    async def aclose(self) -> None:
        """No-op — LiteLLM manages its own connection lifecycle."""
        pass

    async def chat_structured(
        self,
        model: str,
        messages: list[dict[str, Any]],
        output_schema: type[T],
        options: dict[str, Any] | None = None,
    ) -> T:
        response = await self.chat(model=model, messages=messages, options=options, format="json")
        content = (response.get("message", {}) or {}).get("content", "") or ""
        return parse_structured_content(content, output_schema)
