from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass, field
from typing import Any

from .secrets import SecretBytes, redact


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def pseudonym(value: str, key: SecretBytes) -> str:
    return hmac.new(key.reveal(), value.encode("utf-8"), hashlib.sha256).hexdigest()[:24]


@dataclass(frozen=True, slots=True)
class AuditEvent:
    sequence: int
    occurred_at: str
    actor: str
    action: str
    target: str | None
    decision: str
    reason: str
    correlation_id: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditChain:
    key: SecretBytes
    previous_digest: str = "0" * 64
    records: list[dict[str, Any]] = field(default_factory=list)

    def append(self, event: AuditEvent) -> dict[str, Any]:
        payload = {
            "sequence": event.sequence,
            "occurredAt": event.occurred_at,
            "actor": event.actor,
            "action": event.action,
            "target": event.target,
            "decision": event.decision,
            "reason": event.reason,
            "correlationId": event.correlation_id,
            "context": redact(event.context),
            "previousDigest": self.previous_digest,
        }
        digest = hmac.new(self.key.reveal(), canonical_json(payload), hashlib.sha256).hexdigest()
        record = {**payload, "eventDigest": digest}
        self.records.append(record)
        self.previous_digest = digest
        return record

    def verify(self) -> bool:
        previous = "0" * 64
        for record in self.records:
            payload = {k: v for k, v in record.items() if k != "eventDigest"}
            if payload.get("previousDigest") != previous:
                return False
            expected = hmac.new(self.key.reveal(), canonical_json(payload), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected, str(record.get("eventDigest"))):
                return False
            previous = expected
        return True
