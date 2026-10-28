from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib


class SandboxError(ValueError):
    pass


@dataclass(frozen=True)
class SandboxSession:
    id: str
    tenant: str
    created_at: datetime
    expires_at: datetime
    credential_expires_at: datetime
    data_class: str

    def active(self, now: datetime) -> bool:
        return now < self.expires_at


def create_session(*, subject: str, nonce: str, now: datetime, profile: dict) -> SandboxSession:
    if profile.get("dataClass") != "synthetic-only" or profile.get("productionDataAllowed") is not False:
        raise SandboxError("unsafe-sandbox-profile")
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    digest = hashlib.sha256(f"{subject}\0{nonce}".encode()).hexdigest()[:16]
    tenant = profile["tenantPrefix"] + digest[:10]
    return SandboxSession(
        id="sbx-"+digest, tenant=tenant, created_at=now,
        expires_at=now+timedelta(seconds=int(profile["sessionTtlSeconds"])),
        credential_expires_at=now+timedelta(seconds=int(profile["credentialTtlSeconds"])),
        data_class="synthetic-only",
    )


def validate_import(session: SandboxSession, data_class: str) -> None:
    if data_class != "synthetic-only":
        raise SandboxError("production-data-forbidden")
