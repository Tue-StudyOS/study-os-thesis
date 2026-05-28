"""Phase 3: E2E tests for WebSocket endpoints."""

import pytest

from starlette.testclient import TestClient


@pytest.mark.e2e
class TestWebSocket:
    def test_websocket_requires_auth(self, _app):
        """Connecting without a token gets accepted then immediately closed with 4001."""
        with TestClient(_app) as client:
            with client.websocket_connect("/api/ws") as ws:
                # Server accepts then closes with code 4001
                # Attempting to receive should raise because the connection is closed
                with pytest.raises(Exception):
                    ws.receive_json()

    def test_websocket_rejects_invalid_token(self, _app):
        """Connecting with an invalid JWT gets accepted then immediately closed."""
        with TestClient(_app) as client:
            with client.websocket_connect("/api/ws?token=invalid-jwt") as ws:
                with pytest.raises(Exception):
                    ws.receive_json()
