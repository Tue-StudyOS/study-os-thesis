import asyncio
import json
from unittest.mock import AsyncMock

import pytest

from app.worker.constants import JOB_EVENTS_CHANNEL


@pytest.mark.unit
class TestRedisListener:
    async def test_dispatches_message_to_manager(self):
        from app.ws.listener import _handle_message

        manager = AsyncMock()
        data = {"type": "task_complete", "job_id": "abc", "user_id": 1, "status": "success"}
        raw_message = {"type": "message", "data": json.dumps(data).encode()}

        await _handle_message(raw_message, manager)

        manager.send_to_user.assert_called_once_with(1, data)

    async def test_ignores_subscribe_messages(self):
        from app.ws.listener import _handle_message

        manager = AsyncMock()
        raw_message = {"type": "subscribe", "data": None}

        await _handle_message(raw_message, manager)

        manager.send_to_user.assert_not_called()

    async def test_handles_malformed_json(self):
        from app.ws.listener import _handle_message

        manager = AsyncMock()
        raw_message = {"type": "message", "data": b"not-json"}

        # Should not raise
        await _handle_message(raw_message, manager)

        manager.send_to_user.assert_not_called()

    async def test_handles_missing_user_id(self):
        from app.ws.listener import _handle_message

        manager = AsyncMock()
        data = {"type": "task_complete", "job_id": "abc"}  # no user_id
        raw_message = {"type": "message", "data": json.dumps(data).encode()}

        # Should not raise
        await _handle_message(raw_message, manager)

        manager.send_to_user.assert_not_called()

    async def test_listener_subscribes_to_job_events_channel(self, monkeypatch):
        from app.ws.listener import redis_listener
        import redis.asyncio as aioredis

        manager = AsyncMock()
        subscribed = asyncio.Event()

        class FakePubSub:
            async def subscribe(self, channel):
                self.channel = channel
                subscribed.set()

            def listen(self):
                return self

            def __aiter__(self):
                return self

            async def __anext__(self):
                await asyncio.Event().wait()

            async def aclose(self):
                return None

        class FakeClient:
            def __init__(self):
                self.pubsub_instance = FakePubSub()

            def pubsub(self):
                return self.pubsub_instance

            async def aclose(self):
                return None

        client = FakeClient()
        monkeypatch.setattr(aioredis, "from_url", lambda _redis_url: client)

        task = asyncio.create_task(redis_listener(manager, "redis://x", retry_delay=999))
        await asyncio.wait_for(subscribed.wait(), timeout=1)
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task

        assert client.pubsub_instance.channel == JOB_EVENTS_CHANNEL
