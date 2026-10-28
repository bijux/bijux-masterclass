from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
from dataclasses import dataclass
from typing import Any

from .model import Unauthorized, ValidationError


_SAFE_INTEGER = 9_007_199_254_740_991
_BASE64URL = re.compile(r"^[A-Za-z0-9_-]*$")


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(text: str) -> bytes:
    if not _BASE64URL.fullmatch(text):
        raise Unauthorized("malformed capability encoding")
    try:
        return base64.b64decode(
            text + "=" * (-len(text) % 4),
            altchars=b"-_",
            validate=True,
        )
    except (ValueError, base64.binascii.Error) as exc:
        raise Unauthorized("malformed capability encoding") from exc


def _canonical(value: dict[str, object]) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise Unauthorized(f"duplicate capability member: {key}")
        value[key] = item
    return value


def _non_empty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise Unauthorized(f"capability {field} must be a non-empty string")
    return value


def _safe_integer(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise Unauthorized(f"capability {field} must be a safe integer")
    if abs(value) > _SAFE_INTEGER:
        raise Unauthorized(f"capability {field} must be a safe integer")
    return value


@dataclass(frozen=True)
class CapabilityClaims:
    jti: str
    issuer: str
    audience: str
    subject: str
    tenant: str
    resource: str
    action: str
    issued_at: int
    expires_at: int
    sha256: str | None = None
    max_bytes: int | None = None

    def to_wire(self) -> dict[str, object]:
        wire: dict[str, object] = {
            "action": self.action,
            "audience": self.audience,
            "expires_at": self.expires_at,
            "issued_at": self.issued_at,
            "issuer": self.issuer,
            "jti": self.jti,
            "resource": self.resource,
            "subject": self.subject,
            "tenant": self.tenant,
        }
        if self.max_bytes is not None:
            wire["max_bytes"] = self.max_bytes
        if self.sha256 is not None:
            wire["sha256"] = self.sha256
        return wire

    @classmethod
    def from_wire(cls, raw: object) -> "CapabilityClaims":
        if not isinstance(raw, dict):
            raise Unauthorized("capability payload must be an object")
        required = {
            "jti",
            "issuer",
            "audience",
            "subject",
            "tenant",
            "resource",
            "action",
            "issued_at",
            "expires_at",
        }
        optional = {"sha256", "max_bytes"}
        keys = set(raw)
        if not required.issubset(keys) or not keys.issubset(required | optional):
            raise Unauthorized("capability payload fields are invalid")

        max_bytes = None
        if "max_bytes" in raw:
            max_bytes = _safe_integer(raw["max_bytes"], "max_bytes")
            if max_bytes <= 0:
                raise Unauthorized("capability max_bytes must be positive")

        return cls(
            jti=_non_empty_string(raw["jti"], "jti"),
            issuer=_non_empty_string(raw["issuer"], "issuer"),
            audience=_non_empty_string(raw["audience"], "audience"),
            subject=_non_empty_string(raw["subject"], "subject"),
            tenant=_non_empty_string(raw["tenant"], "tenant"),
            resource=_non_empty_string(raw["resource"], "resource"),
            action=_non_empty_string(raw["action"], "action"),
            issued_at=_safe_integer(raw["issued_at"], "issued_at"),
            expires_at=_safe_integer(raw["expires_at"], "expires_at"),
            sha256=(
                None
                if "sha256" not in raw
                else _non_empty_string(raw["sha256"], "sha256")
            ),
            max_bytes=max_bytes,
        )


class CapabilityAuthority:
    """Course-specific HMAC capability profile shared by both tracks."""

    def __init__(self, *, issuer: str, key: bytes) -> None:
        if len(key) < 16:
            raise ValidationError("capability key is too short")
        self.issuer = issuer
        self.key = key
        self._consumed: set[str] = set()

    def mint(self, claims: CapabilityClaims) -> str:
        if claims.issuer != self.issuer:
            raise ValidationError("issuer mismatch")
        if claims.expires_at <= claims.issued_at:
            raise ValidationError("invalid capability lifetime")
        if claims.max_bytes is not None and claims.max_bytes <= 0:
            raise ValidationError("max_bytes must be positive")
        payload = _b64url_encode(_canonical(claims.to_wire()))
        signature = _b64url_encode(
            hmac.new(
                self.key,
                payload.encode("ascii"),
                hashlib.sha256,
            ).digest()
        )
        return f"cap1.{payload}.{signature}"

    def verify(
        self,
        token: str,
        *,
        audience: str,
        tenant: str,
        action: str,
        now: int,
        consume_once: bool = False,
    ) -> CapabilityClaims:
        parts = token.split(".")
        if len(parts) != 3 or parts[0] != "cap1":
            raise Unauthorized("malformed capability")
        payload, signature = parts[1], parts[2]
        expected = _b64url_encode(
            hmac.new(
                self.key,
                payload.encode("ascii"),
                hashlib.sha256,
            ).digest()
        )
        if not hmac.compare_digest(expected, signature):
            raise Unauthorized("invalid capability signature")
        try:
            raw: Any = json.loads(
                _b64url_decode(payload),
                object_pairs_hook=_strict_object,
            )
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise Unauthorized("malformed capability payload") from exc
        claims = CapabilityClaims.from_wire(raw)
        if claims.issuer != self.issuer or claims.audience != audience:
            raise Unauthorized("capability audience or issuer mismatch")
        if claims.tenant != tenant or claims.action != action:
            raise Unauthorized("capability authority mismatch")
        if now < claims.issued_at or now >= claims.expires_at:
            raise Unauthorized("capability expired or not active")
        if consume_once:
            if claims.jti in self._consumed:
                raise Unauthorized("capability already consumed")
            self._consumed.add(claims.jti)
        return claims
