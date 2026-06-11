"""Unit tests for AuthService."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UniversityLoginRequest
from app.auth.service import AuthService
from app.auth.university import UniversityIdentity
from app.exceptions import (
    AlreadyExistsException,
    BadRequestException,
    InvalidCredentialsException,
    UnauthorizedException,
)
from app.models import User, UserRole
from tests.conftest import _make_orm


@pytest.fixture
def auth_service(mock_user_repo, fake_settings) -> AuthService:
    return AuthService(mock_user_repo, fake_settings)


class FakeUniversityVerifier:
    def __init__(self, identity: UniversityIdentity | None = None, error: Exception | None = None) -> None:
        self.identity = identity or UniversityIdentity(username="zxabc12", display_name="Max Mustermann")
        self.error = error
        self.calls: list[tuple[str, str]] = []

    def verify(self, username: str, password: str) -> UniversityIdentity:
        self.calls.append((username, password))
        if self.error:
            raise self.error
        return self.identity


@pytest.mark.unit
class TestRegister:
    async def test_register_creates_user(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None
        fake_user = _make_orm(User, id=1, email="new@test.com", role=UserRole.student)
        mock_user_repo.create.return_value = fake_user

        with patch("app.auth.service.hash_password", new_callable=AsyncMock) as mock_hash:
            mock_hash.return_value = "hashed-pw"
            data = RegisterRequest(email="new@test.com", password="password123")
            result = await auth_service.register(data)

        mock_user_repo.create.assert_called_once()
        call_kwargs = mock_user_repo.create.call_args
        assert call_kwargs.kwargs["email"] == "new@test.com"
        assert call_kwargs.kwargs["password_hash"] == "hashed-pw"
        mock_user_repo.commit.assert_called_once()
        assert result.email == "new@test.com"

    async def test_register_hashes_password(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None
        mock_user_repo.create.return_value = _make_orm(User, id=1)

        with patch("app.auth.service.hash_password", new_callable=AsyncMock) as mock_hash:
            mock_hash.return_value = "bcrypt-hash"
            data = RegisterRequest(email="x@test.com", password="plaintext1")
            await auth_service.register(data)

        mock_user_repo.create.assert_called_once()
        assert mock_user_repo.create.call_args.kwargs["password_hash"] != "plaintext1"

    async def test_register_duplicate_email_raises(self, auth_service, mock_user_repo):
        existing = _make_orm(User, email="taken@test.com")
        mock_user_repo.get_by_email.return_value = existing

        with pytest.raises(AlreadyExistsException):
            data = RegisterRequest(email="taken@test.com", password="password123")
            await auth_service.register(data)

    async def test_register_admin_role_raises(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None
        with pytest.raises(BadRequestException, match="Admin cannot self-register"):
            data = RegisterRequest(email="a@test.com", password="password123", role=UserRole.admin)
            await auth_service.register(data)


@pytest.mark.unit
class TestLogin:
    async def test_login_valid_credentials_returns_token(self, auth_service, mock_user_repo):
        user = _make_orm(User, id=1, email="user@test.com", role=UserRole.student, password_hash="stored-hash")
        mock_user_repo.get_by_email.return_value = user

        with patch("app.auth.service.verify_password", new_callable=AsyncMock) as mock_verify, patch("app.auth.service.create_access_token") as mock_token:
            mock_verify.return_value = True
            mock_token.return_value = "jwt-token-123"
            data = LoginRequest(email="user@test.com", password="correct-pw")
            result = await auth_service.login(data)

        assert isinstance(result, TokenResponse)
        assert result.access_token == "jwt-token-123"

    async def test_login_unknown_email_raises(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None

        with pytest.raises(InvalidCredentialsException):
            data = LoginRequest(email="nobody@test.com", password="anything1")
            await auth_service.login(data)

    async def test_login_wrong_password_raises(self, auth_service, mock_user_repo):
        user = _make_orm(User, id=1, password_hash="stored-hash")
        mock_user_repo.get_by_email.return_value = user

        with patch("app.auth.service.verify_password", new_callable=AsyncMock) as mock_verify:
            mock_verify.return_value = False
            with pytest.raises(InvalidCredentialsException):
                data = LoginRequest(email="user@test.com", password="wrong-pw1")
                await auth_service.login(data)


@pytest.mark.unit
class TestUniversityLogin:
    async def test_university_login_creates_local_user_without_storing_uni_password(self, mock_user_repo, fake_settings):
        verifier = FakeUniversityVerifier()
        auth_service = AuthService(mock_user_repo, fake_settings, university_verifier=verifier)
        mock_user_repo.get_by_email.return_value = None
        created_user = _make_orm(User, id=4, email="alma-zxabc12@studyos.invalid", role=UserRole.student)
        mock_user_repo.create.return_value = created_user

        with patch("app.auth.service.hash_password", new_callable=AsyncMock) as mock_hash, patch("app.auth.service.create_access_token") as mock_token:
            mock_hash.return_value = "hashed-random-local-secret"
            mock_token.return_value = "jwt-token-uni"
            result = await auth_service.university_login(UniversityLoginRequest(username="zxabc12", password="uni-secret"))

        assert result.access_token == "jwt-token-uni"
        assert result.display_name == "Max Mustermann"
        assert verifier.calls == [("zxabc12", "uni-secret")]
        mock_user_repo.create.assert_called_once()
        assert mock_user_repo.create.call_args.kwargs["email"] == "alma-zxabc12@studyos.invalid"
        assert mock_user_repo.create.call_args.kwargs["password_hash"] == "hashed-random-local-secret"
        assert mock_user_repo.create.call_args.kwargs["password_hash"] != "uni-secret"
        mock_user_repo.commit.assert_called_once()

    async def test_university_login_reuses_existing_local_user(self, mock_user_repo, fake_settings):
        verifier = FakeUniversityVerifier()
        auth_service = AuthService(mock_user_repo, fake_settings, university_verifier=verifier)
        existing = _make_orm(User, id=5, email="alma-zxabc12@studyos.invalid", role=UserRole.student)
        mock_user_repo.get_by_email.return_value = existing

        with patch("app.auth.service.create_access_token") as mock_token:
            mock_token.return_value = "jwt-token-existing"
            result = await auth_service.university_login(UniversityLoginRequest(username="zxabc12", password="uni-secret"))

        assert result.access_token == "jwt-token-existing"
        mock_user_repo.create.assert_not_called()
        mock_user_repo.commit.assert_not_called()

    async def test_university_login_invalid_credentials_raise(self, mock_user_repo, fake_settings):
        verifier = FakeUniversityVerifier(error=InvalidCredentialsException())
        auth_service = AuthService(mock_user_repo, fake_settings, university_verifier=verifier)

        with pytest.raises(InvalidCredentialsException):
            await auth_service.university_login(UniversityLoginRequest(username="zxabc12", password="wrong"))

        mock_user_repo.get_by_email.assert_not_called()


@pytest.mark.unit
class TestGetUserById:
    async def test_get_user_by_id_returns_user(self, auth_service, mock_user_repo):
        user = _make_orm(User, id=1)
        mock_user_repo.get_by_id.return_value = user

        result = await auth_service.get_user_by_id(1)
        assert result.id == 1
        mock_user_repo.get_by_id.assert_called_once_with(1)

    async def test_get_user_by_id_not_found_raises(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = None

        with pytest.raises(UnauthorizedException):
            await auth_service.get_user_by_id(999)
