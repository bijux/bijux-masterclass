from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass, field
from typing import Mapping

from .errors import SecurityControlError
from .secrets import SecretBytes


def signing_input(*, timestamp: int, delivery_id: str, key_id: str, body: bytes) -> bytes:
    digest = hashlib.sha256(body).hexdigest()
    return f"v1\n{timestamp}\n{delivery_id}\n{key_id}\n{digest}".encode("utf-8")


def sign_webhook(*, secret: SecretBytes, timestamp: int, delivery_id: str, key_id: str, body: bytes) -> str:
    digest = hmac.new(secret.reveal(), signing_input(timestamp=timestamp, delivery_id=delivery_id, key_id=key_id, body=body), hashlib.sha256).hexdigest()
    return f"sha256={digest}"


@dataclass(slots=True)
class MemoryReplayStore:
    accepted: set[tuple[str, str]] = field(default_factory=set)

    def claim(self, key_id: str, delivery_id: str) -> bool:
        item = (key_id, delivery_id)
        if item in self.accepted:
            return False
        self.accepted.add(item)
        return True


def verify_webhook(
    *,
    body: bytes,
    timestamp: int,
    delivery_id: str,
    key_id: str,
    signature: str,
    now: int,
    keys: Mapping[str, SecretBytes],
    replay: MemoryReplayStore,
    max_age_seconds: int = 300,
    future_skew_seconds: int = 30,
) -> None:
    if timestamp < now - max_age_seconds or timestamp > now + future_skew_seconds:
        raise SecurityControlError("webhook-stale", "webhook timestamp is outside the accepted window", 401)
    secret = keys.get(key_id)
    if secret is None:
        raise SecurityControlError("webhook-key", "webhook key identifier is not recognized", 401)
    expected = sign_webhook(secret=secret, timestamp=timestamp, delivery_id=delivery_id, key_id=key_id, body=body)
    if not hmac.compare_digest(expected, signature):
        raise SecurityControlError("webhook-signature", "webhook signature is invalid", 401)
    if not replay.claim(key_id, delivery_id):
        raise SecurityControlError("webhook-replay", "webhook delivery identifier was already accepted", 409)
