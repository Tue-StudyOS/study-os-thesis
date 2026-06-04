from typing import Annotated

from fastapi import Depends

from app.auth.deps import SessionDep
from app.papers.repository import PaperRepository, TagRepository
from app.papers.service import PaperService


def get_paper_repository(session: SessionDep) -> PaperRepository:
    return PaperRepository(session)


PaperRepoDep = Annotated[PaperRepository, Depends(get_paper_repository)]


def get_tag_repository(session: SessionDep) -> TagRepository:
    return TagRepository(session)


TagRepoDep = Annotated[TagRepository, Depends(get_tag_repository)]


def get_paper_service(paper_repo: PaperRepoDep) -> PaperService:
    return PaperService(paper_repo)


PaperServiceDep = Annotated[PaperService, Depends(get_paper_service)]
