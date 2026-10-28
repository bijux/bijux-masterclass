from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from fastapi import Request

from .problems import ApiProblem

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

CredentialRecord = tuple[str, frozenset[str], bool]

# These credentials are deterministic course fixtures, not an identity system.
# The public security contract is real; token issuance and verification are
# deliberately outside this course's boundary.
TOKEN_RECORDS: dict[str, CredentialRecord] = {
    "learner-read": ("learner", frozenset(READ_SCOPES), False),
    "learner-write": ("learner", frozenset(ALL_USER_SCOPES), False),
    "other-owner": ("other", frozenset(ALL_USER_SCOPES), False),
    "admin": ("admin", frozenset(ALL_USER_SCOPES | {"admin"}), True),
}
API_KEYS: dict[str, CredentialRecord] = {
    "demo-api-key": ("learner", frozenset(ALL_USER_SCOPES), False),
}


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    scopes: frozenset[str]
    admin: bool = False


def _bearer_value(authorization: str) -> str:
    scheme, separator, value = authorization.partition(" ")
    if separator == "" or scheme.lower() != "bearer" or value == "":
        raise ApiProblem(
            401,
            "Authentication required",
            "Malformed bearer credential.",
            "unauthorized",
        )
    return value


async def principal_from_request(request: Request) -> Principal:
    authorization = request.headers.get("authorization")
    api_key = request.headers.get("x-api-key")

    record: CredentialRecord | None
    if authorization is not None:
        record = TOKEN_RECORDS.get(_bearer_value(authorization))
        unknown_detail = "Unknown bearer credential."
    elif api_key is not None:
        record = API_KEYS.get(api_key)
        unknown_detail = "Unknown API key."
    else:
        raise ApiProblem(
            401,
            "Authentication required",
            "Supply a bearer token or X-API-Key.",
            "unauthorized",
        )

    if record is None:
        raise ApiProblem(
            401,
            "Authentication required",
            unknown_detail,
            "unauthorized",
        )

    subject, scopes, is_admin = record
    return Principal(subject=subject, scopes=scopes, admin=is_admin)


def require_scopes(
    *required: str,
) -> Callable[[Request], Awaitable[Principal]]:
    required_scopes = frozenset(required)

    async def dependency(request: Request) -> Principal:
        principal = await principal_from_request(request)
        missing = required_scopes - principal.scopes
        if missing:
            names = ", ".join(sorted(missing))
            raise ApiProblem(
                403,
                "Permission denied",
                f"Missing required scope(s): {names}.",
                "forbidden",
            )
        return principal

    return dependency
