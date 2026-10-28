from __future__ import annotations
import json
import grpc
from .errors import (
    RpcApplicationError, InvalidArgument, NotFound, PermissionDenied,
    Unauthenticated, FailedPrecondition, Aborted, AlreadyExists,
    ResourceExhausted,
)

_STATUS = {
    "INVALID_ARGUMENT": grpc.StatusCode.INVALID_ARGUMENT,
    "NOT_FOUND": grpc.StatusCode.NOT_FOUND,
    "PERMISSION_DENIED": grpc.StatusCode.PERMISSION_DENIED,
    "UNAUTHENTICATED": grpc.StatusCode.UNAUTHENTICATED,
    "FAILED_PRECONDITION": grpc.StatusCode.FAILED_PRECONDITION,
    "ABORTED": grpc.StatusCode.ABORTED,
    "ALREADY_EXISTS": grpc.StatusCode.ALREADY_EXISTS,
    "RESOURCE_EXHAUSTED": grpc.StatusCode.RESOURCE_EXHAUSTED,
}

def abort_for(context: grpc.ServicerContext, error: RpcApplicationError) -> None:
    detail = {"reason": error.reason}
    if error.field:
        detail["field"] = error.field
    context.set_trailing_metadata((
        ("analysis-error-bin", json.dumps(detail, sort_keys=True).encode()),
    ))
    context.abort(_STATUS.get(error.code, grpc.StatusCode.INTERNAL), error.safe_message)

def safe_error(code: grpc.StatusCode, details: str, trailing=()) -> dict[str, object]:
    reason = None
    for item in trailing or ():
        if item.key == "analysis-error-bin":
            try:
                reason = json.loads(item.value.decode())
            except Exception:
                reason = {"reason": "malformed_error_detail"}
    return {"status": code.name, "message": details, "detail": reason}
