"""E2E tests for scraper, papers, and researchers endpoints."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _make_job(**kwargs):
    defaults = dict(
        id=uuid.uuid4(),
        type="scrape_chair",
        status="pending",
        user_id=1,
        celery_task_id=None,
        input_data={},
        result_data=None,
        error=None,
        attempts=0,
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        started_at=None,
        completed_at=None,
    )
    return SimpleNamespace(**{**defaults, **kwargs})


def _make_paper(**kwargs):
    defaults = dict(
        id=1,
        title="Deep Learning Paper",
        abstract="We present a novel approach.",
        summary="A short summary.",
        authors=["Georg Martius", "Alice Author"],
        publication_date=datetime(2023, 6, 1, tzinfo=timezone.utc),
        source="openalex",
        source_url="https://openalex.org/W1",
        doi=None,
        recency_score=0.8,
        relevance_score=0.8,
        enriched_at=datetime(2023, 7, 1, tzinfo=timezone.utc),
        created_at=datetime(2023, 7, 1, tzinfo=timezone.utc),
        tags=[],  # PaperOut.from_orm_with_tags reads paper.tags (list of PaperTag)
    )
    return SimpleNamespace(**{**defaults, **kwargs})


def _make_researcher(**kwargs):
    defaults = dict(
        id=1,
        name="Georg Martius",
        chair_id=1,
        orcid=None,
        affiliation="University of Tübingen",
        is_professor=True,
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    return SimpleNamespace(**{**defaults, **kwargs})


def _mock_celery_result():
    r = MagicMock()
    r.id = "celery-" + uuid.uuid4().hex[:8]
    return r


# ---------------------------------------------------------------------------
# Scraper trigger endpoints
# ---------------------------------------------------------------------------


@pytest.mark.e2e
class TestRunChairScrape:
    async def test_dispatches_job_for_authenticated_user(self, client, _app):
        from app.jobs.deps import get_job_service
        from app.scraper.deps import get_chair_repository

        fake_chair = SimpleNamespace(
            id=1,
            name="Distributed Intelligence",
            short_description="",
            professor_title="Prof. Dr.",
            professor_name="Georg Martius",
            website_url=None,
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            documents=[],
        )
        chair_repo = AsyncMock()
        chair_repo.get_by_id.return_value = fake_chair

        job = _make_job(id=uuid.uuid4())
        job_svc = AsyncMock()
        job_svc.find_active_chair_scrape.return_value = None
        job_svc.create_job.return_value = job
        job_svc.set_celery_task_id.return_value = job

        _app.dependency_overrides[get_chair_repository] = lambda: chair_repo
        _app.dependency_overrides[get_job_service] = lambda: job_svc
        try:
            with patch(
                "app.scraper.tasks.scrape_chair_papers.delay",
                return_value=_mock_celery_result(),
            ) as scrape_delay:
                resp = await client.post("/api/scraper/run/1", json={"since_days": 365, "max_results": 20})
        finally:
            _app.dependency_overrides.pop(get_chair_repository, None)
            _app.dependency_overrides.pop(get_job_service, None)

        assert resp.status_code == 202
        data = resp.json()
        assert "job_id" in data
        assert data["chair_id"] == 1
        assert scrape_delay.call_args.args[-2:] == (20, 365)

    async def test_chair_not_found_returns_404(self, client, _app):
        from app.scraper.deps import get_chair_repository

        chair_repo = AsyncMock()
        chair_repo.get_by_id.return_value = None

        _app.dependency_overrides[get_chair_repository] = lambda: chair_repo
        try:
            resp = await client.post("/api/scraper/run/999", json={"since_days": 365, "max_results": 20})
        finally:
            _app.dependency_overrides.pop(get_chair_repository, None)

        assert resp.status_code == 404

    async def test_active_job_returns_409(self, client, _app):
        from app.jobs.deps import get_job_service
        from app.scraper.deps import get_chair_repository

        fake_chair = SimpleNamespace(
            id=1,
            name="Distributed Intelligence",
            short_description="",
            professor_title="Prof. Dr.",
            professor_name="Georg Martius",
            website_url=None,
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            documents=[],
        )
        chair_repo = AsyncMock()
        chair_repo.get_by_id.return_value = fake_chair

        existing_job = _make_job(id=uuid.uuid4())
        job_svc = AsyncMock()
        job_svc.find_active_chair_scrape.return_value = existing_job

        _app.dependency_overrides[get_chair_repository] = lambda: chair_repo
        _app.dependency_overrides[get_job_service] = lambda: job_svc
        try:
            resp = await client.post("/api/scraper/run/1", json={"since_days": 365, "max_results": 20})
        finally:
            _app.dependency_overrides.pop(get_chair_repository, None)
            _app.dependency_overrides.pop(get_job_service, None)

        assert resp.status_code == 409
        assert str(existing_job.id) in resp.json()["detail"]["job_id"]

    async def test_unauthenticated_returns_401(self, _app):
        from httpx import ASGITransport, AsyncClient
        from app.auth.deps import get_current_user

        orig_override = _app.dependency_overrides.get(get_current_user)
        # Remove the auth override so FastAPI evaluates the real OAuth2 scheme
        _app.dependency_overrides.pop(get_current_user, None)
        try:
            transport = ASGITransport(app=_app)
            async with AsyncClient(transport=transport, base_url="http://test") as anon:
                resp = await anon.post("/api/scraper/run/1", json={"since_days": 365, "max_results": 20})
        finally:
            if orig_override is not None:
                _app.dependency_overrides[get_current_user] = orig_override
        assert resp.status_code == 401


@pytest.mark.e2e
class TestEnrichPaper:
    async def test_admin_can_enrich_paper(self, admin_client, _app):
        from app.jobs.deps import get_job_service

        job = _make_job(type="enrich_paper")
        job_svc = AsyncMock()
        job_svc.create_job.return_value = job
        job_svc.set_celery_task_id.return_value = job
        _app.dependency_overrides[get_job_service] = lambda: job_svc

        try:
            with patch(
                "app.scraper.tasks.enrich_paper.delay",
                return_value=_mock_celery_result(),
            ):
                resp = await admin_client.post("/api/scraper/enrich/1")
        finally:
            _app.dependency_overrides.pop(get_job_service, None)

        assert resp.status_code == 202
        assert resp.json()["paper_id"] == 1

    async def test_student_cannot_enrich_paper(self, client):
        resp = await client.post("/api/scraper/enrich/1")
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Papers API
# ---------------------------------------------------------------------------


@pytest.mark.e2e
class TestListPapers:
    async def test_authenticated_user_gets_200(self, client, _app):
        from app.papers.deps import get_paper_service

        paper_svc = AsyncMock()
        paper_svc.list_papers.return_value = []
        _app.dependency_overrides[get_paper_service] = lambda: paper_svc
        try:
            resp = await client.get("/api/papers")
        finally:
            _app.dependency_overrides.pop(get_paper_service, None)

        assert resp.status_code == 200
        assert resp.json() == []

    async def test_returns_papers_from_service(self, client, _app):
        from app.papers.deps import get_paper_service
        from app.papers.schemas import PaperOut

        paper = _make_paper()
        paper_svc = AsyncMock()
        paper_svc.list_papers.return_value = [paper]
        _app.dependency_overrides[get_paper_service] = lambda: paper_svc

        # PaperOut.from_orm_with_tags reads paper.tags as list of PaperTag objects
        # We need to patch it to avoid attribute errors on SimpleNamespace
        with patch(
            "app.papers.controller.PaperOut.from_orm_with_tags",
            return_value=PaperOut(
                id=1,
                title="Deep Learning Paper",
                abstract=None,
                summary=None,
                authors=["Georg Martius"],
                publication_date=None,
                source="openalex",
                source_url="https://example.com",
                doi=None,
                recency_score=0.8,
                relevance_score=0.8,
                enriched_at=None,
                created_at=datetime(2023, 7, 1, tzinfo=timezone.utc),
                tags=[],
            ),
        ):
            try:
                resp = await client.get("/api/papers")
            finally:
                _app.dependency_overrides.pop(get_paper_service, None)

        assert resp.status_code == 200
        papers = resp.json()
        assert len(papers) == 1
        assert papers[0]["source"] == "openalex"

    async def test_chair_id_filter_forwarded_to_service(self, client, _app):
        from app.papers.deps import get_paper_service

        paper_svc = AsyncMock()
        paper_svc.list_papers.return_value = []
        _app.dependency_overrides[get_paper_service] = lambda: paper_svc
        try:
            resp = await client.get("/api/papers?chair_id=1")
        finally:
            _app.dependency_overrides.pop(get_paper_service, None)

        assert resp.status_code == 200
        paper_svc.list_papers.assert_awaited_once()
        assert paper_svc.list_papers.call_args.kwargs.get("chair_id") == 1

    async def test_tag_filter_forwarded_to_service(self, client, _app):
        from app.papers.deps import get_paper_service

        paper_svc = AsyncMock()
        paper_svc.list_papers.return_value = []
        _app.dependency_overrides[get_paper_service] = lambda: paper_svc
        try:
            resp = await client.get("/api/papers?tag=robotics")
        finally:
            _app.dependency_overrides.pop(get_paper_service, None)

        assert resp.status_code == 200
        assert paper_svc.list_papers.call_args.kwargs.get("tag_name") == "robotics"

    async def test_unauthenticated_returns_401(self, _app):
        from httpx import ASGITransport, AsyncClient
        from app.auth.deps import get_current_user

        orig_override = _app.dependency_overrides.get(get_current_user)
        _app.dependency_overrides.pop(get_current_user, None)
        try:
            transport = ASGITransport(app=_app)
            async with AsyncClient(transport=transport, base_url="http://test") as anon:
                resp = await anon.get("/api/papers")
        finally:
            if orig_override is not None:
                _app.dependency_overrides[get_current_user] = orig_override
        assert resp.status_code == 401


@pytest.mark.e2e
class TestGetPaper:
    async def test_existing_paper_returns_200(self, client, _app):
        from app.papers.deps import get_paper_service
        from app.papers.schemas import PaperOut

        paper = _make_paper(id=42)
        paper_svc = AsyncMock()
        paper_svc.get_paper.return_value = paper
        _app.dependency_overrides[get_paper_service] = lambda: paper_svc

        with patch(
            "app.papers.controller.PaperOut.from_orm_with_tags",
            return_value=PaperOut(
                id=42,
                title="T",
                abstract=None,
                summary=None,
                authors=[],
                publication_date=None,
                source="openalex",
                source_url="https://openalex.org/W42",
                doi=None,
                recency_score=0.5,
                relevance_score=0.5,
                enriched_at=None,
                created_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
                tags=[],
            ),
        ):
            try:
                resp = await client.get("/api/papers/42")
            finally:
                _app.dependency_overrides.pop(get_paper_service, None)

        assert resp.status_code == 200
        assert resp.json()["id"] == 42

    async def test_missing_paper_returns_404(self, client, _app):
        from app.exceptions import NotFoundException
        from app.papers.deps import get_paper_service

        paper_svc = AsyncMock()
        paper_svc.get_paper.side_effect = NotFoundException("Paper", 999)
        _app.dependency_overrides[get_paper_service] = lambda: paper_svc
        try:
            resp = await client.get("/api/papers/999")
        finally:
            _app.dependency_overrides.pop(get_paper_service, None)

        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Researchers API
# ---------------------------------------------------------------------------


@pytest.mark.e2e
class TestListResearchers:
    async def test_requires_chair_id_param(self, client):
        resp = await client.get("/api/researchers")
        assert resp.status_code == 422

    async def test_returns_researchers_for_chair(self, client, _app):
        from app.researchers.deps import get_researcher_service

        researcher = _make_researcher()
        svc = AsyncMock()
        svc.list_by_chair.return_value = [researcher]
        _app.dependency_overrides[get_researcher_service] = lambda: svc
        try:
            resp = await client.get("/api/researchers?chair_id=1")
        finally:
            _app.dependency_overrides.pop(get_researcher_service, None)

        assert resp.status_code == 200
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Georg Martius"

    async def test_unauthenticated_returns_401(self, _app):
        from httpx import ASGITransport, AsyncClient
        from app.auth.deps import get_current_user

        orig_override = _app.dependency_overrides.get(get_current_user)
        _app.dependency_overrides.pop(get_current_user, None)
        try:
            transport = ASGITransport(app=_app)
            async with AsyncClient(transport=transport, base_url="http://test") as anon:
                resp = await anon.get("/api/researchers?chair_id=1")
        finally:
            if orig_override is not None:
                _app.dependency_overrides[get_current_user] = orig_override
        assert resp.status_code == 401


@pytest.mark.e2e
class TestCreateResearcher:
    async def test_student_cannot_create(self, client):
        resp = await client.post(
            "/api/researchers",
            json={"name": "New Researcher", "chair_id": 1},
        )
        assert resp.status_code == 403

    async def test_admin_can_create(self, admin_client, _app):
        from app.researchers.deps import get_researcher_service

        researcher = _make_researcher(id=99, name="New Researcher")
        svc = AsyncMock()
        svc.create_researcher.return_value = researcher
        _app.dependency_overrides[get_researcher_service] = lambda: svc

        try:
            resp = await admin_client.post(
                "/api/researchers",
                json={"name": "New Researcher", "chair_id": 1},
            )
        finally:
            _app.dependency_overrides.pop(get_researcher_service, None)

        assert resp.status_code == 201
        assert resp.json()["name"] == "New Researcher"

    async def test_create_missing_name_returns_422(self, admin_client):
        resp = await admin_client.post("/api/researchers", json={"chair_id": 1})
        assert resp.status_code == 422
