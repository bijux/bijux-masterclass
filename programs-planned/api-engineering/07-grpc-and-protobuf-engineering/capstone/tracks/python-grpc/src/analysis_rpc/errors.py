from __future__ import annotations

class RpcApplicationError(Exception):
    code = "INTERNAL"
    reason = "internal_error"
    def __init__(self, message: str, *, field: str | None = None) -> None:
        super().__init__(message)
        self.safe_message = message
        self.field = field

class InvalidArgument(RpcApplicationError):
    code = "INVALID_ARGUMENT"
    reason = "invalid_argument"

class NotFound(RpcApplicationError):
    code = "NOT_FOUND"
    reason = "not_found"

class PermissionDenied(RpcApplicationError):
    code = "PERMISSION_DENIED"
    reason = "permission_denied"

class Unauthenticated(RpcApplicationError):
    code = "UNAUTHENTICATED"
    reason = "unauthenticated"

class FailedPrecondition(RpcApplicationError):
    code = "FAILED_PRECONDITION"
    reason = "failed_precondition"

class Aborted(RpcApplicationError):
    code = "ABORTED"
    reason = "concurrency_conflict"

class AlreadyExists(RpcApplicationError):
    code = "ALREADY_EXISTS"
    reason = "idempotency_conflict"

class ResourceExhausted(RpcApplicationError):
    code = "RESOURCE_EXHAUSTED"
    reason = "resource_exhausted"
