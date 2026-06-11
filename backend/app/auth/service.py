import secrets

from app.auth.university import AlmaCredentialVerifier, UniversityCredentialVerifier, university_subject_email
from app.auth_core.security import create_access_token, hash_password, verify_password
from app.config import Settings
from app.exceptions import (
    AlreadyExistsException,
    BadRequestException,
    InvalidCredentialsException,
    UnauthorizedException,
)
from app.models import User, UserRole
from app.users.repository import UserRepository
from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UniversityLoginRequest, UniversityTokenResponse


class AuthService:
    """Business logic for authentication and user registration."""

    def __init__(self, user_repo: UserRepository, settings: Settings, university_verifier: UniversityCredentialVerifier | None = None) -> None:
        self._user_repo = user_repo
        self._settings = settings
        self._university_verifier = university_verifier or AlmaCredentialVerifier()

    async def register(self, data: RegisterRequest) -> User:
        if data.role == UserRole.admin:
            raise BadRequestException("Admin cannot self-register")

        existing = await self._user_repo.get_by_email(data.email)
        if existing:
            raise AlreadyExistsException("User", "email", data.email)

        hashed = await hash_password(data.password)
        user = await self._user_repo.create(
            email=data.email,
            password_hash=hashed,
            role=data.role,
        )
        await self._user_repo.commit()
        return user

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self._user_repo.get_by_email(data.email)
        if not user or not await verify_password(data.password, user.password_hash):
            raise InvalidCredentialsException()

        return self._token_for_user(user)

    async def university_login(self, data: UniversityLoginRequest) -> UniversityTokenResponse:
        identity = self._university_verifier.verify(data.username, data.password)
        subject_email = university_subject_email(identity.username)

        user = await self._user_repo.get_by_email(subject_email)
        if not user:
            user = await self._user_repo.create(
                email=subject_email,
                password_hash=await hash_password(secrets.token_urlsafe(32)),
                role=UserRole.student,
            )
            await self._user_repo.commit()

        token = self._token_for_user(user)
        return UniversityTokenResponse(
            access_token=token.access_token,
            university_username=identity.username,
            display_name=identity.display_name,
        )

    def _token_for_user(self, user: User) -> TokenResponse:
        token = create_access_token(
            sub=str(user.id),
            extra={"role": user.role.value},
        )
        return TokenResponse(access_token=token)

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User not found")
        return user
