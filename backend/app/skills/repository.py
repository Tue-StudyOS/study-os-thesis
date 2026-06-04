"""Data-access layer for the skill computation domain."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.skill import SkillComputationRun, SkillEvidence, UserSkill
from app.skills.scorer import ComputedSkill


class SkillRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Computation runs
    # ------------------------------------------------------------------

    async def create_run(
        self,
        user_id: int,
        job_id: uuid.UUID | None = None,
    ) -> SkillComputationRun:
        run = SkillComputationRun(user_id=user_id, job_id=job_id, status="running")
        self._session.add(run)
        await self._session.flush()
        return run

    async def complete_run(
        self,
        run: SkillComputationRun,
        *,
        total_courses: int,
        matched_courses: int,
        unmatched_courses: list[str],
        warnings: list[str],
        config: dict,
        handbook_version: str | None = None,
        university_id: str | None = None,
    ) -> None:
        run.status = "completed"
        run.total_courses = total_courses
        run.matched_courses = matched_courses
        run.unmatched_courses = unmatched_courses
        run.warnings = warnings
        run.config = config
        run.handbook_version = handbook_version
        run.university_id = university_id
        run.completed_at = datetime.now(timezone.utc)
        await self._session.flush()

    async def fail_run(self, run: SkillComputationRun, error: str) -> None:
        run.status = "failed"
        run.warnings = [error]
        run.completed_at = datetime.now(timezone.utc)
        await self._session.flush()

    # ------------------------------------------------------------------
    # User skills (idempotent upsert)
    # ------------------------------------------------------------------

    async def replace_user_skills(
        self,
        user_id: int,
        run: SkillComputationRun,
        computed_skills: list[ComputedSkill],
    ) -> list[UserSkill]:
        """Delete all existing user_skills + evidence for *user_id*, then insert new rows.

        Idempotent: re-running with the same data produces the same result.
        """
        # Cascade-delete via FK: deleting user_skills also removes skill_evidence.
        await self._session.execute(
            delete(UserSkill).where(UserSkill.user_id == user_id)
        )
        await self._session.flush()

        saved: list[UserSkill] = []
        for cs in computed_skills:
            us = UserSkill(
                user_id=user_id,
                skill_tag_id=cs.skill_tag_id,
                score=cs.score,
                computation_run_id=run.id,
                updated_at=datetime.now(timezone.utc),
            )
            self._session.add(us)
            await self._session.flush()

            for ev in cs.evidence:
                self._session.add(
                    SkillEvidence(
                        user_skill_id=us.id,
                        student_course_id=ev.student_course_id,
                        handbook_entry_id=ev.handbook_entry_id,
                        match_method=ev.match_method,
                        match_confidence=ev.match_confidence,
                        module_skill_relevance=ev.module_skill_relevance,
                        credits_used=ev.credits_used,
                        grade_factor=ev.grade_factor,
                        level_factor=ev.level_factor,
                        recency_factor=ev.recency_factor,
                        raw_contribution=ev.raw_contribution,
                        computation_run_id=run.id,
                    )
                )

            saved.append(us)

        await self._session.flush()
        return saved

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    async def get_user_skills(
        self, user_id: int, limit: int = 50
    ) -> list[UserSkill]:
        """Return user's skills sorted by score descending with evidence and related data loaded."""

        from app.models.handbook import ModuleHandbookEntry
        from app.models.student import StudentCourse

        result = await self._session.scalars(
            select(UserSkill)
            .where(UserSkill.user_id == user_id)
            .order_by(UserSkill.score.desc())
            .limit(limit)
            .options(
                selectinload(UserSkill.skill_tag),
                selectinload(UserSkill.evidence),
            )
        )
        user_skills = list(result.all())

        # Eagerly load related course and handbook entry for each evidence item.
        for us in user_skills:
            for ev in us.evidence:
                # Attach course name
                course = await self._session.get(StudentCourse, ev.student_course_id)
                ev._course = course  # type: ignore[attr-defined]
                # Attach handbook entry title
                if ev.handbook_entry_id:
                    entry = await self._session.get(ModuleHandbookEntry, ev.handbook_entry_id)
                    ev._handbook_entry = entry  # type: ignore[attr-defined]

        return user_skills

    async def get_latest_run(self, user_id: int) -> SkillComputationRun | None:
        return await self._session.scalar(
            select(SkillComputationRun)
            .where(SkillComputationRun.user_id == user_id)
            .order_by(SkillComputationRun.created_at.desc())
            .limit(1)
        )

    async def commit(self) -> None:
        await self._session.commit()
