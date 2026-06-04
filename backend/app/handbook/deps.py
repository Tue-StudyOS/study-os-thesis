"""Dependency injection wiring for the handbook domain."""

from typing import Annotated

from fastapi import Depends

from app.auth.deps import LLMChatClientDep, SessionDep, SettingsDep
from app.handbook.repository import HandbookRepository
from app.handbook.service import HandbookService


def get_handbook_repository(session: SessionDep) -> HandbookRepository:
    return HandbookRepository(session)


HandbookRepoDep = Annotated[HandbookRepository, Depends(get_handbook_repository)]


def get_handbook_service(
    repo: HandbookRepoDep,
    llm_client: LLMChatClientDep,
    settings: SettingsDep,
) -> HandbookService:
    return HandbookService(repo, llm_client, settings)


HandbookServiceDep = Annotated[HandbookService, Depends(get_handbook_service)]
