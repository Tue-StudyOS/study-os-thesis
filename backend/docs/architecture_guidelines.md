# Architecture Guidelines

## LLM Calls

Use `chat_structured()` for extraction, generation, classification, and enrichment.
The expected response shape should be a Pydantic model close to the call site.
Keep raw `chat()` for agent/tool loops where the model may return tool calls.

## Heavy Work

CPU-heavy, LLM-heavy, and network-heavy operations should run through Celery
workers. HTTP controllers should validate requests, persist lightweight job
state, dispatch tasks, and return quickly.

## Data Boundaries

Repositories own persistence details. Services and workers should pass typed
domain or schema objects instead of unvalidated dictionaries whenever the
structure is known.
