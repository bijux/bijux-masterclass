from __future__ import annotations
from .errors import PermissionDenied, Unauthenticated
from .models import Principal

_FIXTURES = {
    "learner-read": Principal("user-read", "tenant-a", frozenset({"runs:read"})),
    "learner-write": Principal(
        "user-write", "tenant-a",
        frozenset({"runs:read", "runs:write", "datasets:write", "artifacts:read"})
    ),
    "tenant-b-write": Principal(
        "user-b", "tenant-b",
        frozenset({"runs:read", "runs:write", "datasets:write", "artifacts:read"})
    ),
    "worker-1": Principal("worker-1", "tenant-a", frozenset({"worker:connect"}), "worker"),
}

def authenticate(metadata) -> Principal:
    values = [m.value for m in metadata if m.key == "authorization"]
    if len(values) != 1:
        raise Unauthenticated("exactly one authorization credential is required")
    value = values[0]
    if not value.startswith("Bearer "):
        raise Unauthenticated("unsupported credential")
    token = value.removeprefix("Bearer ")
    principal = _FIXTURES.get(token)
    if principal is None:
        raise Unauthenticated("invalid credential")
    return principal

def require(principal: Principal, scope: str) -> None:
    if scope not in principal.scopes:
        raise PermissionDenied("permission denied")

def tenant_from_parent(parent: str) -> str:
    # The educational resource fixture binds projects/p-b-* to tenant-b.
    return "tenant-b" if parent.startswith("projects/p-b-") else "tenant-a"

def require_tenant(principal: Principal, resource_or_parent: str) -> None:
    if tenant_from_parent(resource_or_parent.split("/runs/")[0]) != principal.tenant:
        raise PermissionDenied("permission denied")
