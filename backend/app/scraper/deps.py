"""Dependency injection for the scraper module."""

from typing import Annotated

from fastapi import Depends

from app.auth.deps import SessionDep
from app.chairs.repository import ChairRepository


def get_chair_repository(session: SessionDep) -> ChairRepository:
    return ChairRepository(session)


ChairRepoDep = Annotated[ChairRepository, Depends(get_chair_repository)]
