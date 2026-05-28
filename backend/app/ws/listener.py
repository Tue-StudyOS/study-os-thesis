"""Redis Pub/Sub → WebSocket bridge."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from app.ws.manager import ConnectionManager

logger = logging.getLogger(__name__)


async def _handle_message(raw: dict[str, Any], manager: ConnectionManager) -> None:
    """Process a single Redis Pub/Sub message.

    Extracted as a standalone function for easy unit testing.
    """
    if raw.get("type") != "message":
        return

    data_bytes = raw.get("data")
    if data_bytes is None:
        return

    try:
        if isinstance(data_bytes, bytes):
            data = json.loads(data_bytes.decode())
        else:
            data = json.loads(data_bytes)
    except (json.JSONDecodeError, UnicodeDecodeError):
        logger.warning("Malformed JSON in Redis Pub/Sub message")
        return

    user_id = data.get("user_id")
    if user_id is None:
        logger.debug("Redis event missing user_id, skipping")
        return

    await manager.send_to_user(user_id, data)


async def redis_listener(manager: ConnectionManager, redis_url: str) -> None:
    """Subscribe to ``job_events`` and dispatch messages to WebSocket clients.

    This runs as an ``asyncio.Task`` in the FastAPI lifespan.
    """
    import redis.asyncio as aioredis

    r = aioredis.from_url(redis_url)
    pubsub = r.pubsub()
    await pubsub.subscribe("job_events")

    try:
        async for message in pubsub.listen():
            await _handle_message(message, manager)
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe("job_events")
        await r.aclose()
