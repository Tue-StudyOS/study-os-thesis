from fastapi import APIRouter, Request, status

from app.auth.constants import AUTH_API_PREFIX, AUTH_API_TAG, AUTH_RATE_LIMIT
from app.auth.deps import AuthServiceDep, CurrentUserDep
from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UniversityLoginRequest, UniversityTokenResponse, UserOut
from app.limiter import limiter
from app.models import User

router = APIRouter(prefix=AUTH_API_PREFIX, tags=[AUTH_API_TAG])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(AUTH_RATE_LIMIT)
async def register(request: Request, body: RegisterRequest, auth_service: AuthServiceDep) -> User:
    return await auth_service.register(body)


@router.post("/login", response_model=TokenResponse)
@limiter.limit(AUTH_RATE_LIMIT)
async def login(request: Request, body: LoginRequest, auth_service: AuthServiceDep) -> TokenResponse:
    return await auth_service.login(body)


@router.post("/university-login", response_model=UniversityTokenResponse)
@limiter.limit(AUTH_RATE_LIMIT)
async def university_login(request: Request, body: UniversityLoginRequest, auth_service: AuthServiceDep) -> UniversityTokenResponse:
    return await auth_service.university_login(body)


@router.get("/me", response_model=UserOut)
async def me(user: CurrentUserDep) -> User:
    return user
