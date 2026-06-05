"""REST endpoints for researcher management."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.auth.deps import CurrentUserDep, require_role
from app.models import User, UserRole
from app.researchers.deps import ResearcherServiceDep
from app.researchers.schemas import ResearcherCreate, ResearcherOut

router = APIRouter(prefix="/api/researchers", tags=["researchers"])

AdminDep = Annotated[User, Depends(require_role(UserRole.admin))]


@router.get("", response_model=list[ResearcherOut])
async def list_researchers(
    _user: CurrentUserDep,
    researcher_service: ResearcherServiceDep,
    chair_id: int = Query(..., description="Filter by chair"),
) -> list:
    return await researcher_service.list_by_chair(chair_id)


@router.get("/{researcher_id}", response_model=ResearcherOut)
async def get_researcher(
    researcher_id: int,
    _user: CurrentUserDep,
    researcher_service: ResearcherServiceDep,
) -> object:
    return await researcher_service.get_researcher(researcher_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ResearcherOut)
async def create_researcher(
    body: ResearcherCreate,
    _admin: AdminDep,
    researcher_service: ResearcherServiceDep,
) -> object:
    return await researcher_service.create_researcher(body)
