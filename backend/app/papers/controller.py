"""REST endpoints for querying papers."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.auth.deps import CurrentUserDep
from app.papers.deps import PaperServiceDep
from app.papers.schemas import PaperOut

router = APIRouter(prefix="/api/papers", tags=["papers"])


@router.get("", response_model=list[PaperOut])
async def list_papers(
    _user: CurrentUserDep,
    paper_service: PaperServiceDep,
    chair_id: int | None = Query(None, description="Filter by chair"),
    tag: str | None = Query(None, description="Filter by canonical tag name"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[PaperOut]:
    """Return papers ordered by relevance_score DESC."""
    papers = await paper_service.list_papers(
        chair_id=chair_id,
        tag_name=tag,
        limit=limit,
        offset=offset,
    )
    return [PaperOut.from_orm_with_tags(p) for p in papers]


@router.get("/{paper_id}", response_model=PaperOut)
async def get_paper(
    paper_id: int,
    _user: CurrentUserDep,
    paper_service: PaperServiceDep,
) -> PaperOut:
    paper = await paper_service.get_paper(paper_id)
    return PaperOut.from_orm_with_tags(paper)
