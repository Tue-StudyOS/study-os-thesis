from app.admin.constants import ADMIN_USER_LIST_DEFAULT_LIMIT, ADMIN_USER_LIST_DEFAULT_OFFSET
from app.models import User
from app.users.repository import UserRepository


class AdminService:
    """Business logic for admin-only operations."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def list_users(self, limit: int = ADMIN_USER_LIST_DEFAULT_LIMIT, offset: int = ADMIN_USER_LIST_DEFAULT_OFFSET) -> list[User]:
        return await self._user_repo.list_all(limit=limit, offset=offset)
