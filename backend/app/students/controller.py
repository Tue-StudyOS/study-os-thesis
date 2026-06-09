from fastapi import APIRouter, Form, UploadFile, status

from app.auth.deps import CurrentUserDep
from app.exceptions import BadRequestException
from app.jobs.deps import JobServiceDep
from app.models.job import JobType
from app.students.constants import (
    STUDENT_PROGRAM_MAX_LENGTH,
    STUDENT_SEMESTER_MAX,
    STUDENT_SEMESTER_MIN,
    STUDENT_TRANSCRIPT_ACCEPTED_CONTENT_TYPES,
    STUDENT_TRANSCRIPT_MAX_PDF_SIZE_BYTES,
    STUDENT_TRANSCRIPT_MAX_PDF_SIZE_LABEL,
    STUDENTS_API_PREFIX,
    STUDENTS_API_TAG,
)
from app.students.deps import StudentServiceDep
from app.students.schemas import StudentOut, StudentProfileUpdate, StudentProfileResponse

router = APIRouter(prefix=STUDENTS_API_PREFIX, tags=[STUDENTS_API_TAG])


@router.get("/me", response_model=StudentOut)
async def get_my_profile(
    current_user: CurrentUserDep,
    student_service: StudentServiceDep,
) -> object:
    return await student_service.get_profile(current_user.id)


@router.put("/profile", response_model=StudentProfileResponse)
async def update_profile(
    current_user: CurrentUserDep,
    student_service: StudentServiceDep,
    body: StudentProfileUpdate,
) -> object:
    """Update student profile (name, education level, program)."""
    return await student_service.update_profile(
        current_user.id,
        full_name=body.full_name,
        education_level=body.education_level,
        program=body.program,
    )


@router.post("/me/transcript", status_code=status.HTTP_202_ACCEPTED)
async def upload_transcript(
    current_user: CurrentUserDep,
    job_service: JobServiceDep,
    file: UploadFile,
    program: str | None = Form(default=None, max_length=STUDENT_PROGRAM_MAX_LENGTH),
    semester: int | None = Form(default=None, ge=STUDENT_SEMESTER_MIN, le=STUDENT_SEMESTER_MAX),
) -> dict:
    """Upload a PDF transcript. Processing is dispatched to a background worker."""
    from app.config import get_settings
    from app.students.pdf_store import store_pdf
    from app.students.tasks import parse_transcript

    if file.content_type not in STUDENT_TRANSCRIPT_ACCEPTED_CONTENT_TYPES:
        raise BadRequestException("Only PDF files are accepted.")

    pdf_bytes = await file.read()
    if len(pdf_bytes) > STUDENT_TRANSCRIPT_MAX_PDF_SIZE_BYTES:
        raise BadRequestException(f"PDF exceeds the {STUDENT_TRANSCRIPT_MAX_PDF_SIZE_LABEL} size limit.")
    if not pdf_bytes:
        raise BadRequestException("Uploaded file is empty.")

    # Create the job first, stash the PDF bytes under its id, then dispatch.
    job = await job_service.create_job(
        type=JobType.parse_transcript,
        user_id=current_user.id,
        input_data={"program": program, "semester": semester},
    )
    await store_pdf(get_settings().redis_url, str(job.id), pdf_bytes)

    task_result = parse_transcript.delay(
        user_id=current_user.id,
        job_id=str(job.id),
        program=program,
        semester=semester,
    )
    await job_service.set_celery_task_id(job.id, task_result.id)

    return {"job_id": str(job.id)}
