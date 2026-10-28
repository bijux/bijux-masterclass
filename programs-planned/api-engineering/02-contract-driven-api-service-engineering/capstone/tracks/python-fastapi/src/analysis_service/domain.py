"""Pure domain rules shared by the HTTP application and worker.

Nothing in this module imports FastAPI, PostgreSQL, or the filesystem.  Tests
can therefore prove state transitions, fingerprints, ETags, and signatures
without infrastructure.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
import hmac
import json
from typing import Any

from .failures import ServiceError


MAX_POSTGRES_BIGINT = 9_223_372_036_854_775_807


class RunState(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


TERMINAL_STATES = frozenset(
    {RunState.COMPLETED, RunState.FAILED, RunState.CANCELED}
)

TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.QUEUED: frozenset({RunState.RUNNING, RunState.CANCELED}),
    RunState.RUNNING: frozenset(
        {RunState.COMPLETED, RunState.FAILED, RunState.CANCELED}
    ),
    RunState.COMPLETED: frozenset(),
    RunState.FAILED: frozenset(),
    RunState.CANCELED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class StoredResponse:
    status: int
    headers: dict[str, str]
    body: dict[str, Any]
    replay: bool


@dataclass(frozen=True, slots=True)
class RunSnapshot:
    state: RunState
    progress: int
    cancellation_requested: bool = False


MAX_SAFE_JSON_INTEGER = 9_007_199_254_740_991


def _validate_canonical_value(value: Any) -> None:
    """Validate the deliberately small cross-language JSON profile."""

    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_JSON_INTEGER:
            raise TypeError("canonical JSON integers must be JavaScript-safe")
        return
    if isinstance(value, float):
        raise TypeError("canonical JSON profile rejects floating-point values")
    if isinstance(value, list):
        for item in value:
            _validate_canonical_value(item)
        return
    if isinstance(value, dict):
        for key, member in value.items():
            if not isinstance(key, str):
                raise TypeError("canonical JSON object keys must be strings")
            _validate_canonical_value(member)
        return
    raise TypeError(f"unsupported canonical JSON value: {type(value).__name__}")


def canonical_json(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for the course profile.

    This is not RFC 8785/JCS. The profile accepts JSON null, strings, booleans,
    JavaScript-safe integers, arrays, and string-keyed objects. It rejects
    floating-point values, sorts object names by Unicode code point, preserves
    array order, and emits no insignificant whitespace. Restricting the number
    domain is what makes Python and TypeScript byte-identical without pretending
    their general-purpose JSON number serializers are equivalent.
    """

    _validate_canonical_value(value)
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def request_fingerprint(operation_id: str, owner_id: str, body: Any) -> str:
    envelope = {
        "operationId": operation_id,
        "ownerId": owner_id,
        "body": body,
    }
    return sha256(canonical_json(envelope)).hexdigest()


def filter_fingerprint(
    operation_id: str,
    owner_id: str,
    filters: dict[str, Any],
) -> str:
    envelope = {
        "operationId": operation_id,
        "ownerId": owner_id,
        "filters": filters,
    }
    return sha256(canonical_json(envelope)).hexdigest()


def project_etag(project_id: str, version: int) -> str:
    if version < 1:
        raise ValueError("version must be positive")
    return f'"{project_id}:{version}"'


def parse_project_etag(value: str, project_id: str) -> int:
    prefix = f'"{project_id}:'
    if not value.startswith(prefix) or not value.endswith('"'):
        raise ServiceError(
            412,
            "Precondition failed",
            "The supplied entity tag does not identify this project.",
            "precondition-failed",
        )
    raw = value[len(prefix) : -1]
    if (
        not raw.isascii()
        or not raw.isdigit()
        or int(raw) < 1
        or int(raw) > 2_147_483_647
    ):
        raise ServiceError(
            412,
            "Precondition failed",
            "The supplied entity tag is malformed.",
            "precondition-failed",
        )
    return int(raw)


def parse_cursor(value: str | None) -> int | None:
    if value is None:
        return None
    if not value.isascii() or not value.isdigit():
        raise _invalid_cursor()
    handle = int(value)
    if handle < 1 or handle > MAX_POSTGRES_BIGINT:
        raise _invalid_cursor()
    return handle


def _invalid_cursor() -> ServiceError:
    return ServiceError(
        422,
        "Request validation failed",
        "cursor must be a positive signed-64-bit decimal handle.",
        "cursor-invalid",
    )


def require_transition(
    current: str | RunState,
    target: str | RunState,
) -> None:
    current_state = RunState(current)
    target_state = RunState(target)
    if target_state not in TRANSITIONS[current_state]:
        raise ServiceError(
            409,
            "Request conflict",
            (
                "analysis run cannot move from "
                f"{current_state.value} to {target_state.value}"
            ),
            "invalid-run-transition",
        )


def evolve(
    snapshot: RunSnapshot,
    command: str,
    progress: int | None = None,
) -> RunSnapshot:
    if command == "request-cancel":
        if snapshot.state in TERMINAL_STATES:
            raise ServiceError(
                409,
                "Request conflict",
                "A terminal run cannot be canceled.",
                "invalid-run-transition",
            )
        return RunSnapshot(snapshot.state, snapshot.progress, True)

    targets = {
        "claim": RunState.RUNNING,
        "complete": RunState.COMPLETED,
        "fail": RunState.FAILED,
        "observe-cancel": RunState.CANCELED,
    }
    if command not in targets:
        raise ValueError(f"unknown command: {command}")

    target = targets[command]
    require_transition(snapshot.state, target)
    next_progress = (
        10
        if target is RunState.RUNNING
        else 100
        if target is RunState.COMPLETED
        else snapshot.progress
    )
    if progress is not None:
        next_progress = progress
    if target is RunState.RUNNING and not 1 <= next_progress <= 99:
        raise ValueError("running progress must be 1..99")
    return RunSnapshot(target, next_progress, snapshot.cancellation_requested)


def webhook_signature(secret: str, timestamp: str, body: bytes) -> str:
    """Sign exactly ``timestamp + b'.' + body`` using HMAC-SHA256."""

    digest = hmac.new(
        secret.encode("utf-8"),
        timestamp.encode("ascii") + b"." + body,
        sha256,
    ).hexdigest()
    return f"sha256={digest}"


def verify_webhook_signature(
    secret: str,
    timestamp: str,
    body: bytes,
    candidate: str,
) -> bool:
    return hmac.compare_digest(
        webhook_signature(secret, timestamp, body),
        candidate,
    )


def retry_delay_seconds(attempt: int, cap: int = 300) -> int:
    if attempt < 1:
        raise ValueError("attempt is one-based")
    return min(cap, 2 ** min(attempt - 1, 12))
