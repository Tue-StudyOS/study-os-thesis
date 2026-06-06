"""E2E tests for chair endpoints."""

import pytest


@pytest.mark.e2e
class TestCreateChair:
    async def test_returns_201_with_job_id(self, admin_client):
        """POST /api/chairs returns chair data + job_id for embedding."""
        response = await admin_client.post(
            "/api/chairs",
            json={
                "name": "Test Chair",
                "short_description": "A research chair focused on machine learning and AI applications.",
                "professor_title": "Prof.",
                "professor_name": "Prof. Test",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "job_id" in data

    async def test_list_chairs_returns_list(self, client):
        response = await client.get("/api/chairs")
        assert response.status_code == 200
