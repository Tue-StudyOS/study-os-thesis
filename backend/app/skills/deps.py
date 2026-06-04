"""Dependency injection wiring for the skills domain."""

from typing import Annotated

from fastapi import Depends

from app.auth.deps import SessionDep
from app.handbook.repository import HandbookRepository
from app.skills.repository import SkillRepository
from app.students.repository import StudentRepository


def get_skill_repository(session: SessionDep) -> SkillRepository:
    return SkillRepository(session)


SkillRepoDep = Annotated[SkillRepository, Depends(get_skill_repository)]


def get_handbook_repository_for_skills(session: SessionDep) -> HandbookRepository:
    return HandbookRepository(session)


def get_student_repository_for_skills(session: SessionDep) -> StudentRepository:
    return StudentRepository(session)
