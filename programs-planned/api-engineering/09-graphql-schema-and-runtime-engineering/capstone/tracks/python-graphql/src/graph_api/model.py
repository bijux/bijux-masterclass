from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant_id: str
    permissions: frozenset[str]


@dataclass(frozen=True)
class RequestContext:
    principal: Principal
    request_id: str
    deadline_ms: int = 1_000
    client_name: str = "course-client"
    now_epoch: int = 1_786_147_200


@dataclass(frozen=True)
class GraphError:
    message: str
    path: tuple[str | int, ...] = ()
    code: str = "INTERNAL"
    service: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "message": self.message,
            "extensions": {"code": self.code},
        }
        if self.path:
            value["path"] = list(self.path)
        if self.service:
            value["extensions"]["service"] = self.service
        value["extensions"].update(self.details)
        return value


@dataclass(frozen=True)
class ExecutionResult:
    data: dict[str, Any] | None
    errors: tuple[GraphError, ...] = ()
    extensions: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"data": self.data}
        if self.errors:
            result["errors"] = [error.as_dict() for error in self.errors]
        if self.extensions:
            result["extensions"] = self.extensions
        return result


class ValidationError(ValueError):
    """The request cannot enter execution under the released graph profile."""


class AuthorizationError(PermissionError):
    """The principal is not authorized for a graph capability."""


class DownstreamUnavailable(RuntimeError):
    def __init__(self, service: str, message: str = "downstream unavailable") -> None:
        super().__init__(message)
        self.service = service


class ConflictError(RuntimeError):
    """A durable domain command conflicts with existing state."""


class PreconditionFailed(RuntimeError):
    """An expected version no longer matches authoritative state."""
