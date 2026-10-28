from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
import secrets


class StateError(ValueError):
    pass


def validate_backend_profile(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_true = {
        "versioning": "state bucket versioning is required",
        "publicAccessBlock": "state bucket public-access block is required",
        "tlsOnlyPolicy": "state bucket must reject non-TLS transport",
        "nativeLockfile": "native S3 lockfile is required by the course profile",
        "kmsEncryption": "KMS-backed server-side encryption is required",
        "recoveryVersionSelection": "a documented state-version recovery path is required",
    }
    for key, message in required_true.items():
        if profile.get(key) is not True:
            errors.append(message)
    if profile.get("bucketOwner") == profile.get("workloadOwner"):
        errors.append("state administration and workload runtime authority must differ")
    if not profile.get("keyPrefix"):
        errors.append("state key prefix is required")
    if int(profile.get("retainedVersions", 0)) < 3:
        errors.append("retain at least three state versions in the course profile")
    return errors


def validate_state_transition(current: dict[str, Any], proposed: dict[str, Any]) -> None:
    if current.get("lineage") != proposed.get("lineage"):
        raise StateError("state lineage conflict")
    current_serial = int(current.get("serial", -1))
    proposed_serial = int(proposed.get("serial", -1))
    if proposed_serial != current_serial + 1:
        raise StateError(
            f"state serial must advance by one: current={current_serial} proposed={proposed_serial}"
        )


@dataclass(frozen=True)
class LockLease:
    key: str
    owner: str
    token: str
    expires_at: datetime


class LockRegistry:
    """Deterministic course model of exclusive state mutation.

    This is not the S3 backend implementation. It demonstrates owner/token and
    expiry semantics for tests and incident exercises.
    """

    def __init__(self) -> None:
        self._locks: dict[str, LockLease] = {}

    def acquire(self, key: str, owner: str, *, ttl_seconds: int = 60,
                now: datetime | None = None) -> LockLease:
        now = now or datetime.now(timezone.utc)
        existing = self._locks.get(key)
        if existing is not None and existing.expires_at > now:
            raise StateError(f"state is locked by {existing.owner}")
        lease = LockLease(
            key=key,
            owner=owner,
            token=secrets.token_hex(16),
            expires_at=now + timedelta(seconds=ttl_seconds),
        )
        self._locks[key] = lease
        return lease

    def release(self, key: str, token: str) -> None:
        existing = self._locks.get(key)
        if existing is None:
            raise StateError("state is not locked")
        if not secrets.compare_digest(existing.token, token):
            raise StateError("lock token mismatch")
        del self._locks[key]

    def inspect(self, key: str) -> LockLease | None:
        return self._locks.get(key)
