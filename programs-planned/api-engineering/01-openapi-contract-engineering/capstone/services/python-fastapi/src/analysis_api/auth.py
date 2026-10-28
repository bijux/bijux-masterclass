from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Coroutine, Any

from fastapi import Request
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from .errors import ApiProblem


READ_SCOPES = {
    "projects:read",
    "datasets:read",
    "runs:read",
    "artifacts:read",
}
WRITE_SCOPES = {
    "projects:write",
    "datasets:write",
    "runs:write",
    "webhooks:write",
}
ALL_USER_SCOPES = READ_SCOPES | WRITE_SCOPES

TOKEN_RECORDS: dict[str, tuple[str, set[str], bool]] = {
    "learner-read": ("learner", READ_SCOPES, False),
    "learner-write": ("learner", ALL_USER_SCOPES, False),
    "other-owner": ("other", ALL_USER_SCOPES, False),
    "admin": ("admin", ALL_USER_SCOPES | {"admin"}, True),
}
API_KEYS: dict[str, tuple[str, set[str], bool]] = {
    "demo-api-key": ("learner", ALL_USER_SCOPES, False),
}

bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@dataclass(frozen=True)
class Principal:
    subject: str
    scopes: frozenset[str]
    admin: bool = False


async def _principal_from_request(request: Request) -> Principal:
    authorization = request.headers.get("authorization")
    api_key = request.headers.get("x-api-key")

    record: tuple[str, set[str], bool] | None = None
    if authorization:
        parts = authorization.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise ApiProblem(401, "Authentication required", "Malformed bearer credential.", "unauthorized")
        record = TOKEN_RECORDS.get(parts[1])
        if record is None:
            raise ApiProblem(401, "Authentication required", "Unknown bearer credential.", "unauthorized")
    elif api_key:
        record = API_KEYS.get(api_key)
        if record is None:
            raise ApiProblem(401, "Authentication required", "Unknown API key.", "unauthorized")
    else:
        raise ApiProblem(
            401,
            "Authentication required",
            "Supply a bearer token or X-API-Key.",
            "unauthorized",
        )

    subject, scopes, is_admin = record
    return Principal(subject=subject, scopes=frozenset(scopes), admin=is_admin)


def require_scopes(*required: str) -> Callable[[Request], Coroutine[Any, Any, Principal]]:
    async def dependency(request: Request) -> Principal:
        principal = await _principal_from_request(request)
        missing = set(required) - set(principal.scopes)
        if missing:
            raise ApiProblem(
                403,
                "Permission denied",
                f"Missing required scope(s): {', '.join(sorted(missing))}.",
                "forbidden",
            )
        return principal

    return dependency
