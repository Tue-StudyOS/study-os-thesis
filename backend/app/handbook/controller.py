"""Admin HTTP routes for module handbook management."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile, status

from app.auth.deps import require_role
from app.exceptions import BadRequestException
from app.handbook.deps import HandbookRepoDep
from app.handbook.schemas import HandbookVersionOut
from app.jobs.deps import JobServiceDep
from app.models import User, UserRole
from app.models.job import JobType

router = APIRouter(prefix="/api/admin/handbook", tags=["handbook"])

_MAX_PDF_SIZE = 50 * 1024 * 1024  # 50 MB — handbooks can be large


@router.get("", response_model=list[HandbookVersionOut])
async def list_handbook_versions(
    _admin: Annotated[User, Depends(require_role(UserRole.admin))],
    handbook_repo: HandbookRepoDep,
) -> list[HandbookVersionOut]:
    """List all ingested handbook versions."""
    rows = await handbook_repo.list_versions()
    return [HandbookVersionOut(**r) for r in rows]


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def upload_handbook(
    _admin: Annotated[User, Depends(require_role(UserRole.admin))],
    job_service: JobServiceDep,
    file: UploadFile,
    university_id: str = Form(..., min_length=1, max_length=50),
    handbook_version: str = Form(..., min_length=1, max_length=50),
) -> dict:
    """Upload a Modulhandbuch PDF.  Parsing runs asynchronously in a worker."""
    from app.config import get_settings
    from app.handbook.pdf_store import store_handbook_pdf
    from app.handbook.tasks import ingest_handbook

    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise BadRequestException("Only PDF files are accepted.")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise BadRequestException("Uploaded file is empty.")
    if len(pdf_bytes) > _MAX_PDF_SIZE:
        raise BadRequestException("PDF exceeds the 50 MB size limit.")

    job = await job_service.create_job(
        type=JobType.ingest_handbook,
        user_id=0,  # admin action; no specific user
        input_data={"university_id": university_id, "handbook_version": handbook_version},
    )

    settings = get_settings()
    await store_handbook_pdf(settings.redis_url, str(job.id), pdf_bytes)

    task_result = ingest_handbook.delay(
        job_id=str(job.id),
        university_id=university_id,
        handbook_version=handbook_version,
    )
    await job_service.set_celery_task_id(job.id, task_result.id)

    return {
        "job_id": str(job.id),
        "university_id": university_id,
        "handbook_version": handbook_version,
    }
