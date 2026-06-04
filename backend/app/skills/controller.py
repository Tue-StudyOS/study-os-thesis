"""HTTP routes for the skill computation domain."""

from __future__ import annotations

from fastapi import APIRouter, status

from app.auth.deps import CurrentUserDep
from app.jobs.deps import JobServiceDep
from app.models.job import JobType
from app.skills.deps import SkillRepoDep
from app.skills.schemas import SkillEvidenceOut, UserSkillItemOut, UserSkillProfileOut

router = APIRouter(prefix="/api/students", tags=["skills"])


@router.get("/me/skills", response_model=UserSkillProfileOut)
async def get_my_skills(
    current_user: CurrentUserDep,
    skill_repo: SkillRepoDep,
) -> UserSkillProfileOut:
    """Return the current student's computed skill profile."""
    user_skills = await skill_repo.get_user_skills(current_user.id)
    run = await skill_repo.get_latest_run(current_user.id)

    skill_items: list[UserSkillItemOut] = []
    for us in user_skills:
        evidence_out = [
            SkillEvidenceOut(
                course_name=_get_course_name(ev),
                credits=float(ev.credits_used) if ev.credits_used is not None else None,
                grade=_grade_from_factor(ev),
                handbook_module=_get_handbook_title(ev),
                match_method=ev.match_method,
                match_confidence=float(ev.match_confidence),
                contribution=float(ev.raw_contribution),
            )
            for ev in (us.evidence or [])
        ]
        skill_items.append(
            UserSkillItemOut(
                skill=us.skill_tag.name,
                category=us.skill_tag.category,
                score=float(us.score),
                evidence=evidence_out,
            )
        )

    return UserSkillProfileOut(
        user_id=current_user.id,
        computation_run_id=str(run.id) if run else None,
        computed_at=run.completed_at if run else None,
        skills=skill_items,
        unmatched_courses=run.unmatched_courses or [] if run else [],
        warnings=run.warnings or [] if run else [],
    )


@router.post("/me/skills/recompute", status_code=status.HTTP_202_ACCEPTED)
async def recompute_skills(
    current_user: CurrentUserDep,
    job_service: JobServiceDep,
) -> dict:
    """Manually trigger a skill re-computation from the stored transcript."""
    from app.skills.tasks import compute_skills as _compute_skills_task

    job = await job_service.create_job(
        type=JobType.compute_skills,
        user_id=current_user.id,
    )
    task_result = _compute_skills_task.delay(
        user_id=current_user.id,
        job_id=str(job.id),
    )
    await job_service.set_celery_task_id(job.id, task_result.id)
    return {"job_id": str(job.id)}


# ---------------------------------------------------------------------------
# Private helpers to reconstruct display data from evidence rows
# ---------------------------------------------------------------------------

def _get_course_name(ev: object) -> str:
    course = getattr(ev, "_course", None)
    return getattr(course, "course_name", "") or ""


def _grade_from_factor(ev: object) -> str | None:
    """Return the raw grade from the loaded course, if available."""
    course = getattr(ev, "_course", None)
    return getattr(course, "grade", None)


def _get_handbook_title(ev: object) -> str | None:
    entry = getattr(ev, "_handbook_entry", None)
    return getattr(entry, "module_title", None)
