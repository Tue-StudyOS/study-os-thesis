from typing import Annotated

from fastapi import Depends

from app.auth.deps import SessionDep
from app.researchers.repository import ResearcherRepository
from app.researchers.service import ResearcherService


def get_researcher_repository(session: SessionDep) -> ResearcherRepository:
    return ResearcherRepository(session)


ResearcherRepoDep = Annotated[ResearcherRepository, Depends(get_researcher_repository)]


def get_researcher_service(researcher_repo: ResearcherRepoDep) -> ResearcherService:
    return ResearcherService(researcher_repo)


ResearcherServiceDep = Annotated[ResearcherService, Depends(get_researcher_service)]
