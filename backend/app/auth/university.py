from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Protocol

from app.exceptions import InvalidCredentialsException


@dataclass(frozen=True, slots=True)
class UniversityIdentity:
    username: str
    display_name: str | None = None


class UniversityCredentialVerifier(Protocol):
    def verify(self, username: str, password: str) -> UniversityIdentity: ...


class AlmaCredentialVerifier:
    """Verify ZDV credentials by completing a real Alma login."""

    def verify(self, username: str, password: str) -> UniversityIdentity:
        try:
            from tue_api_wrapper import TuebingenAuthenticatedClient
            from tue_api_wrapper.config import AlmaLoginError
        except ImportError as exc:
            raise RuntimeError("tue-api-wrapper is required for university login") from exc

        try:
            client = TuebingenAuthenticatedClient.login(username=username, password=password)
            profile = client.alma.studyservice_summary()
        except AlmaLoginError as exc:
            raise InvalidCredentialsException() from exc

        return UniversityIdentity(username=username, display_name=profile.person_name)


def university_subject_email(username: str) -> str:
    normalized = re.sub(r"[^a-z0-9._-]+", "-", username.strip().lower())
    local_part = normalized.strip(".-_") or "student"
    return f"alma-{local_part}@studyos.invalid"
