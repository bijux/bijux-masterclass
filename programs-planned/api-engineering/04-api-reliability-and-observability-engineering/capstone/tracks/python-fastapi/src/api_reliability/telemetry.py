from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from .clock import Clock
from .context import TraceContext


SENSITIVE_KEYS = frozenset(
    {
        "authorization",
        "api_key",
        "apikey",
        "password",
        "secret",
        "token",
        "access_token",
        "refresh_token",
        "webhooksecret",
        "webhook_secret",
        "private_key",
        "pepper",
        "cookie",
        "set_cookie",
    }
)
_BEARER_RE = re.compile(r"(?i)(Bearer)\s+[A-Za-z0-9._~+/-]+={0,2}")
_EVENT_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_ALLOWED_SEVERITIES = frozenset({"TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"})


def _redact_string(value: str) -> str:
    candidate = _BEARER_RE.sub(r"\1 [REDACTED]", value)
    try:
        parsed = urlsplit(candidate)
        if parsed.scheme and parsed.hostname and (
            parsed.username is not None or parsed.password is not None
        ):
            host = parsed.hostname
            if parsed.port is not None:
                host = f"{host}:{parsed.port}"
            return urlunsplit(
                (
                    parsed.scheme,
                    f"[REDACTED]@{host}",
                    parsed.path,
                    parsed.query,
                    parsed.fragment,
                )
            )
    except ValueError:
        pass
    return candidate


def redact(value: Any, *, key: str | None = None) -> Any:
    """Recursively remove structured and embedded credential material.

    Redaction is a last-resort disclosure boundary. Callers should still avoid
    attaching sensitive values to telemetry in the first place.
    """

    normalized = key.lower().replace("-", "_") if key else None
    if normalized is not None and (
        normalized in SENSITIVE_KEYS
        or normalized.replace("_", "") in SENSITIVE_KEYS
    ):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(k): redact(v, key=str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return _redact_string(value)
    return value


@dataclass(frozen=True, slots=True)
class TelemetryEvent:
    timestamp_ms: int
    severity: str
    event_name: str
    service_name: str
    service_version: str
    deployment_environment: str
    schema_version: str
    trace_id: str | None = None
    span_id: str | None = None
    attributes: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.timestamp_ms < 0:
            raise ValueError("timestamp_ms must be non-negative")
        if self.severity not in _ALLOWED_SEVERITIES:
            raise ValueError("unsupported telemetry severity")
        if not _EVENT_NAME_RE.fullmatch(self.event_name):
            raise ValueError("event_name must be a stable dotted identifier")
        for label, value in (
            ("service_name", self.service_name),
            ("service_version", self.service_version),
            ("deployment_environment", self.deployment_environment),
            ("schema_version", self.schema_version),
        ):
            if not value or len(value) > 120:
                raise ValueError(f"{label} must contain 1..120 characters")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["attributes"] = redact(payload.get("attributes") or {})
        return payload

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )


class InMemoryEventSink:
    def __init__(self, maximum_events: int = 1_000) -> None:
        if maximum_events < 1:
            raise ValueError("maximum_events must be positive")
        self.maximum_events = maximum_events
        self.events: list[TelemetryEvent] = []
        self.dropped = 0

    def emit(self, event: TelemetryEvent) -> bool:
        if len(self.events) >= self.maximum_events:
            self.dropped += 1
            return False
        self.events.append(event)
        return True


class StructuredLogger:
    def __init__(
        self,
        *,
        clock: Clock,
        sink: InMemoryEventSink,
        service_name: str,
        service_version: str,
        deployment_environment: str = "development",
        schema_version: str = "1.0",
        maximum_attribute_bytes: int = 32_768,
    ) -> None:
        if maximum_attribute_bytes < 256:
            raise ValueError("maximum_attribute_bytes must be at least 256")
        self.clock = clock
        self.sink = sink
        self.service_name = service_name
        self.service_version = service_version
        self.deployment_environment = deployment_environment
        self.schema_version = schema_version
        self.maximum_attribute_bytes = maximum_attribute_bytes

    def emit(
        self,
        event_name: str,
        *,
        severity: str = "INFO",
        context: TraceContext | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> bool:
        clean = redact(attributes or {})
        encoded = json.dumps(clean, sort_keys=True, ensure_ascii=False).encode("utf-8")
        if len(encoded) > self.maximum_attribute_bytes:
            clean = {
                "telemetry.truncated": True,
                "telemetry.original_attribute_bytes": len(encoded),
            }
        return self.sink.emit(
            TelemetryEvent(
                timestamp_ms=self.clock.now_ms(),
                severity=severity,
                event_name=event_name,
                service_name=self.service_name,
                service_version=self.service_version,
                deployment_environment=self.deployment_environment,
                schema_version=self.schema_version,
                trace_id=context.trace_id if context else None,
                span_id=context.span_id if context else None,
                attributes=clean,
            )
        )
