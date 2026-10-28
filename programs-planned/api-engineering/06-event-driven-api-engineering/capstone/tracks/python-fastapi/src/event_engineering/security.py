from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
from typing import Any

from .envelope import EventEnvelope

SENSITIVE_KEYS = {
    "accesstoken",
    "refreshtoken",
    "password",
    "rawdataset",
    "webhooksecret",
    "authorization",
    "leasetoken",
    "stacktrace",
}


class SecurityError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ProducerGrant:
    producer_id: str
    sources: frozenset[str]
    channels: frozenset[str]
    event_types: frozenset[str]
    tenants: frozenset[str]


@dataclass(frozen=True, slots=True)
class SignedMessage:
    key_id: str
    timestamp: str
    signature: str
    body: bytes


def _walk_sensitive(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = "".join(ch for ch in key.lower() if ch.isalnum())
            if normalized in SENSITIVE_KEYS:
                found.append(f"{path}.{key}")
            found.extend(_walk_sensitive(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_walk_sensitive(item, f"{path}[{index}]"))
    return found


def authorize_message(
    grant: ProducerGrant, channel: str, event: EventEnvelope
) -> None:
    if event.source not in grant.sources:
        raise SecurityError("source not granted")
    if channel not in grant.channels:
        raise SecurityError("channel not granted")
    if event.type not in grant.event_types:
        raise SecurityError("event type not granted")
    if event.tenantid not in grant.tenants:
        raise SecurityError("tenant not granted")
    sensitive = _walk_sensitive(event.data)
    if sensitive:
        raise SecurityError(f"sensitive fields prohibited: {sensitive}")


def sign_message(
    event: EventEnvelope,
    key_id: str,
    secret: bytes,
    timestamp: datetime,
) -> SignedMessage:
    if timestamp.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    text = (
        timestamp.astimezone(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    body = event.canonical_bytes()
    mac = hmac.new(secret, text.encode("utf-8") + b"\n" + body, hashlib.sha256)
    return SignedMessage(key_id, text, "sha256=" + mac.hexdigest(), body)


def verify_message(
    message: SignedMessage,
    keys: dict[str, bytes],
    now: datetime,
    max_age_seconds: int = 300,
) -> None:
    secret = keys.get(message.key_id)
    if secret is None:
        raise SecurityError("unknown key id")
    timestamp = datetime.fromisoformat(message.timestamp.replace("Z", "+00:00"))
    age = abs(
        (
            now.astimezone(timezone.utc) - timestamp.astimezone(timezone.utc)
        ).total_seconds()
    )
    if age > max_age_seconds:
        raise SecurityError("signature timestamp outside freshness window")
    expected = "sha256=" + hmac.new(
        secret,
        message.timestamp.encode("utf-8") + b"\n" + message.body,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected, message.signature):
        raise SecurityError("invalid signature")
