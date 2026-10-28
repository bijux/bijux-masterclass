from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Any, Callable
from urllib.parse import urlparse
from uuid import UUID, uuid4

from .canonical import canonical_bytes

TYPE_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*\.v[1-9][0-9]*$")
TRACEPARENT_RE = re.compile(
    r"^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$"
)


class EnvelopeError(ValueError):
    pass


def _utc_text(value: datetime) -> str:
    if value.tzinfo is None:
        raise EnvelopeError("event time must be timezone-aware")
    return (
        value.astimezone(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def _uuid_text(value: str, field: str) -> str:
    try:
        return str(UUID(value))
    except ValueError as exc:
        raise EnvelopeError(f"{field} must be a UUID") from exc


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    specversion: str
    id: str
    source: str
    type: str
    subject: str
    time: str
    datacontenttype: str
    dataschema: str
    tenantid: str
    correlationid: str
    causationid: str | None
    partitionkey: str
    data: dict[str, Any]
    traceparent: str | None = None

    def __post_init__(self) -> None:
        if self.specversion != "1.0":
            raise EnvelopeError("only CloudEvents specversion 1.0 is supported")
        _uuid_text(self.id, "id")
        _uuid_text(self.correlationid, "correlationid")
        if self.causationid is not None:
            _uuid_text(self.causationid, "causationid")
        if not urlparse(self.source).scheme:
            raise EnvelopeError("source must be an absolute URI")
        if not TYPE_RE.fullmatch(self.type):
            raise EnvelopeError("type must follow the versioned course profile")
        if not self.subject or len(self.subject) > 256:
            raise EnvelopeError("subject length is invalid")
        if self.datacontenttype != "application/json":
            raise EnvelopeError("datacontenttype must be application/json")
        if not urlparse(self.dataschema).scheme:
            raise EnvelopeError("dataschema must be an absolute URI")
        if not self.tenantid or len(self.tenantid) > 128:
            raise EnvelopeError("tenantid length is invalid")
        if not self.partitionkey or len(self.partitionkey) > 256:
            raise EnvelopeError("partitionkey length is invalid")
        if self.traceparent and not TRACEPARENT_RE.fullmatch(self.traceparent):
            raise EnvelopeError("traceparent is invalid")
        try:
            parsed = datetime.fromisoformat(self.time.replace("Z", "+00:00"))
        except ValueError as exc:
            raise EnvelopeError("time must be RFC3339-compatible") from exc
        if parsed.tzinfo is None:
            raise EnvelopeError("time must include an offset")
        canonical_bytes(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "specversion": self.specversion,
            "id": self.id,
            "source": self.source,
            "type": self.type,
            "subject": self.subject,
            "time": self.time,
            "datacontenttype": self.datacontenttype,
            "dataschema": self.dataschema,
            "tenantid": self.tenantid,
            "correlationid": self.correlationid,
            "causationid": self.causationid,
            "partitionkey": self.partitionkey,
            "data": self.data,
        }
        if self.traceparent is not None:
            value["traceparent"] = self.traceparent
        return value

    def canonical_bytes(self) -> bytes:
        return canonical_bytes(self.to_dict())


def build_event(
    *,
    source: str,
    event_type: str,
    subject: str,
    dataschema: str,
    tenant_id: str,
    correlation_id: str,
    partition_key: str,
    data: dict[str, Any],
    causation_id: str | None = None,
    traceparent: str | None = None,
    event_id_factory: Callable[[], str] = lambda: str(uuid4()),
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
) -> EventEnvelope:
    return EventEnvelope(
        specversion="1.0",
        id=event_id_factory(),
        source=source,
        type=event_type,
        subject=subject,
        time=_utc_text(clock()),
        datacontenttype="application/json",
        dataschema=dataschema,
        tenantid=tenant_id,
        correlationid=correlation_id,
        causationid=causation_id,
        partitionkey=partition_key,
        data=data,
        traceparent=traceparent,
    )
