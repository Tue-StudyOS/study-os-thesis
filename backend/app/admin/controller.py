from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.admin.api_constants import (
    ADMIN_USER_LIST_DEFAULT_LIMIT,
    ADMIN_USER_LIST_DEFAULT_OFFSET,
    ADMIN_USER_LIST_MAX_LIMIT,
    ADMIN_USER_LIST_MIN_LIMIT,
    ADMIN_USER_LIST_MIN_OFFSET,
)
from app.admin.deps import AdminServiceDep
from app.auth.deps import require_role
from app.auth.schemas import UserOut
from app.models import User, UserRole

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
async def list_users(
    _admin: Annotated[User, Depends(require_role(UserRole.admin))],
    admin_service: AdminServiceDep,
    limit: Annotated[int, Query(ge=ADMIN_USER_LIST_MIN_LIMIT, le=ADMIN_USER_LIST_MAX_LIMIT)] = ADMIN_USER_LIST_DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=ADMIN_USER_LIST_MIN_OFFSET)] = ADMIN_USER_LIST_DEFAULT_OFFSET,
) -> list[User]:
    return await admin_service.list_users(limit=limit, offset=offset)
