"""REST endpoints for querying papers."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.auth.deps import CurrentUserDep
from app.papers.api_constants import (
    PAPER_LIST_DEFAULT_LIMIT,
    PAPER_LIST_DEFAULT_OFFSET,
    PAPER_LIST_MAX_LIMIT,
    PAPER_LIST_MIN_LIMIT,
    PAPER_LIST_MIN_OFFSET,
)
from app.papers.deps import PaperServiceDep
from app.papers.schemas import PaginatedPapersOut, PaperOut

router = APIRouter(prefix="/api/papers", tags=["papers"])


@router.get("", response_model=PaginatedPapersOut)
async def list_papers(
    _user: CurrentUserDep,
    paper_service: PaperServiceDep,
    chair_id: int | None = Query(None, description="Filter by chair"),
    tag: str | None = Query(None, description="Filter by canonical tag name"),
    limit: int = Query(PAPER_LIST_DEFAULT_LIMIT, ge=PAPER_LIST_MIN_LIMIT, le=PAPER_LIST_MAX_LIMIT),
    offset: int = Query(PAPER_LIST_DEFAULT_OFFSET, ge=PAPER_LIST_MIN_OFFSET),
) -> PaginatedPapersOut:
    """Return papers ordered by relevance_score DESC."""
    result = await paper_service.list_papers(
        chair_id=chair_id,
        tag_name=tag,
        limit=limit,
        offset=offset,
    )
    return PaginatedPapersOut(
        items=[PaperOut.from_orm_with_tags(p) for p in result.items],
        total=result.total,
        limit=result.limit,
        offset=result.offset,
    )


@router.get("/{paper_id}", response_model=PaperOut)
async def get_paper(
    paper_id: int,
    _user: CurrentUserDep,
    paper_service: PaperServiceDep,
) -> PaperOut:
    paper = await paper_service.get_paper(paper_id)
    return PaperOut.from_orm_with_tags(paper)
