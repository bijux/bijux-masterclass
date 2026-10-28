from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass

from .model import Principal, ValidationError


@dataclass(frozen=True)
class CursorState:
    tenant_id: str
    audience_hash: str
    scope: str
    filter_hash: str
    after_primary: str
    after_tiebreaker: str
    high_water_primary: str
    high_water_tiebreaker: str
    expires_at: int
    version: int = 1

    @property
    def after_key(self) -> tuple[str, str]:
        return (self.after_primary, self.after_tiebreaker)

    @property
    def high_water_key(self) -> tuple[str, str]:
        return (self.high_water_primary, self.high_water_tiebreaker)


class CursorCodec:
    """Signed, query-bound keyset cursor used by the course graph profile."""

    def __init__(self, key: bytes) -> None:
        if len(key) < 32:
            raise ValueError("cursor key must be at least 32 bytes")
        self._key = key

    def encode(self, state: CursorState) -> str:
        if not state.scope or not state.tenant_id:
            raise ValidationError("cursor scope and tenant are required")
        if state.expires_at <= 0:
            raise ValidationError("cursor expiry is invalid")
        if state.after_key > state.high_water_key:
            raise ValidationError("cursor continuation exceeds high-water key")

        payload = json.dumps(
            {
                "a": state.audience_hash,
                "e": state.expires_at,
                "f": state.filter_hash,
                "ha": state.high_water_primary,
                "hb": state.high_water_tiebreaker,
                "pa": state.after_primary,
                "pb": state.after_tiebreaker,
                "s": state.scope,
                "t": state.tenant_id,
                "v": state.version,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        signature = hmac.new(self._key, payload, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(payload + signature).decode("ascii").rstrip("=")

    def decode(
        self,
        value: str,
        *,
        tenant_id: str,
        audience_hash: str,
        scope: str,
        filter_hash: str,
        now_epoch: int,
    ) -> CursorState:
        try:
            padded = value + "=" * (-len(value) % 4)
            raw = base64.urlsafe_b64decode(padded.encode("ascii"))
            if len(raw) <= 32:
                raise ValidationError("malformed cursor")
            payload, signature = raw[:-32], raw[-32:]
            expected = hmac.new(self._key, payload, hashlib.sha256).digest()
            if not hmac.compare_digest(signature, expected):
                raise ValidationError("invalid cursor signature")
            data = json.loads(payload)
            state = CursorState(
                tenant_id=str(data["t"]),
                audience_hash=str(data["a"]),
                scope=str(data["s"]),
                filter_hash=str(data["f"]),
                after_primary=str(data["pa"]),
                after_tiebreaker=str(data["pb"]),
                high_water_primary=str(data["ha"]),
                high_water_tiebreaker=str(data["hb"]),
                expires_at=int(data["e"]),
                version=int(data["v"]),
            )
        except ValidationError:
            raise
        except Exception as exc:
            raise ValidationError("malformed cursor") from exc

        if state.version != 1:
            raise ValidationError("unsupported cursor version")
        if state.tenant_id != tenant_id:
            raise ValidationError("cursor tenant mismatch")
        if state.audience_hash != audience_hash:
            raise ValidationError("cursor audience mismatch")
        if state.scope != scope:
            raise ValidationError("cursor scope mismatch")
        if state.filter_hash != filter_hash:
            raise ValidationError("cursor filter mismatch")
        if state.expires_at < now_epoch:
            raise ValidationError("cursor expired")
        if state.after_key > state.high_water_key:
            raise ValidationError("invalid cursor key order")
        return state


def _stable_json(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def normalized_filter_hash(value: dict[str, object]) -> str:
    return hashlib.sha256(_stable_json(value)).hexdigest()


def audience_hash(principal: Principal) -> str:
    return hashlib.sha256(
        _stable_json(
            {
                "permissions": sorted(principal.permissions),
                "subject": principal.subject,
                "tenant": principal.tenant_id,
            }
        )
    ).hexdigest()
