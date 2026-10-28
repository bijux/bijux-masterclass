from __future__ import annotations

import base64
import hashlib
import hmac
from dataclasses import dataclass
from typing import Mapping

from .errors import SecurityControlError
from .models import Principal
from .secrets import SecretBytes


@dataclass(frozen=True, slots=True)
class ApiKeyRecord:
    key_id: str
    owner: str
    tenant: str
    digest: bytes
    scopes: frozenset[str]
    revoked: bool = False
    expires_at: int | None = None


def digest_api_key(raw_key: str, pepper: SecretBytes) -> bytes:
    return hmac.new(pepper.reveal(), raw_key.encode("utf-8"), hashlib.sha256).digest()


def verify_api_key(
    raw_key: str,
    *,
    records: Mapping[str, ApiKeyRecord],
    pepper: SecretBytes,
    now: int,
) -> Principal:
    if not raw_key.startswith("ak_") or "." not in raw_key:
        raise SecurityControlError("invalid-api-key", "API key format is invalid", 401)
    key_id = raw_key.split(".", 1)[0][3:]
    record = records.get(key_id)
    if record is None:
        raise SecurityControlError("invalid-api-key", "API key is invalid", 401)
    candidate = digest_api_key(raw_key, pepper)
    if not hmac.compare_digest(candidate, record.digest):
        raise SecurityControlError("invalid-api-key", "API key is invalid", 401)
    if record.revoked or (record.expires_at is not None and record.expires_at <= now):
        raise SecurityControlError("invalid-api-key", "API key is inactive", 401)
    return Principal(record.owner, record.tenant, record.scopes, client_id=f"api-key:{record.key_id}")
