"""REST endpoints for triggering the paper scraper."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.auth.deps import require_role
from app.exceptions import NotFoundException
from app.jobs.deps import JobServiceDep
from app.models import User, UserRole
from app.models.job import JobType
from app.scraper.deps import ChairRepoDep
from app.scraper.schemas import IngestPaperRequest, ScrapeChairRequest, ScrapeRunResponse

router = APIRouter(prefix="/api/scraper", tags=["scraper"])

AdminDep = Annotated[User, Depends(require_role(UserRole.admin))]


@router.post(
    "/run/{chair_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ScrapeRunResponse,
)
async def run_chair_scrape(
    chair_id: int,
    body: ScrapeChairRequest,
    _admin: AdminDep,
    chair_repo: ChairRepoDep,
    job_service: JobServiceDep,
) -> dict:
    """Trigger a full paper scrape for all researchers of a chair.

    Returns immediately with a job_id; poll GET /api/jobs/{job_id} for status.
    """
    from app.scraper.tasks import scrape_chair_papers

    # Validate chair exists before dispatching
    chair = await chair_repo.get_by_id(chair_id)
    if chair is None:
        raise NotFoundException("Chair", chair_id)

    job = await job_service.create_job(
        type=JobType.scrape_chair,
        user_id=_admin.id,
        input_data={
            "chair_id": chair_id,
            "since_days": body.since_days,
            "max_results": body.max_results,
        },
    )
    task_result = scrape_chair_papers.delay(chair_id, _admin.id, str(job.id))
    await job_service.set_celery_task_id(job.id, task_result.id)

    return {
        "job_id": str(job.id),
        "chair_id": chair_id,
        "message": f"Scrape job dispatched for chair '{chair.name}'",
    }


@router.post(
    "/paper",
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_paper(
    body: IngestPaperRequest,
    _admin: AdminDep,
    job_service: JobServiceDep,
) -> dict:
    """Fetch, enrich, and store a single paper by arXiv ID.

    Accepts an arXiv ID (e.g. "2301.07041") and optionally links the paper
    to a researcher. Returns immediately with a job_id; the actual fetch and
    LLM enrichment run in the background worker.

    If the paper already exists it is returned without re-enriching it
    (use POST /api/scraper/enrich/{paper_id}?force=true to force re-enrichment).
    """
    from app.scraper.tasks import ingest_single_paper

    job = await job_service.create_job(
        type=JobType.ingest_single_paper,
        user_id=_admin.id,
        input_data={"arxiv_id": body.arxiv_id, "researcher_id": body.researcher_id},
    )
    task_result = ingest_single_paper.delay(body.arxiv_id, body.researcher_id, _admin.id, str(job.id))
    await job_service.set_celery_task_id(job.id, task_result.id)

    return {"job_id": str(job.id), "arxiv_id": body.arxiv_id}


@router.post(
    "/enrich/{paper_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def enrich_paper_endpoint(
    paper_id: int,
    _admin: AdminDep,
    job_service: JobServiceDep,
    force: bool = False,
) -> dict:
    """(Re-)run LLM enrichment for a single paper.

    Pass ?force=true to re-enrich a paper that was already enriched.
    """
    from app.scraper.tasks import enrich_paper

    job = await job_service.create_job(
        type=JobType.enrich_paper,
        user_id=_admin.id,
        input_data={"paper_id": paper_id, "force": force},
    )
    task_result = enrich_paper.delay(paper_id, _admin.id, str(job.id), force)
    await job_service.set_celery_task_id(job.id, task_result.id)

    return {"job_id": str(job.id), "paper_id": paper_id}
