from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlsplit, urlunsplit

SENSITIVE_KEYS = frozenset(
    {
        "authorization", "api_key", "apikey", "api-key", "password", "secret",
        "token", "access_token", "refresh_token", "webhooksecret", "webhook_secret",
        "private_key", "pepper",
    }
)
BEARER_RE = re.compile(r"(?i)(Bearer)\s+[A-Za-z0-9._~+/-]+")


class SecretBytes:
    __slots__ = ("__value",)

    def __init__(self, value: bytes | str) -> None:
        self.__value = value.encode("utf-8") if isinstance(value, str) else bytes(value)
        if not self.__value:
            raise ValueError("secret must not be empty")

    def reveal(self) -> bytes:
        return bytes(self.__value)

    def __repr__(self) -> str:
        return "SecretBytes([REDACTED])"

    def __str__(self) -> str:
        return "[REDACTED]"


@dataclass(slots=True)
class DictSecretProvider:
    values: Mapping[tuple[str, str], SecretBytes]

    def get(self, name: str, version: str) -> SecretBytes:
        return self.values[(name, version)]


def _redact_string(value: str) -> str:
    value = BEARER_RE.sub(r"\1 [REDACTED]", value)
    try:
        parsed = urlsplit(value)
        if parsed.scheme and parsed.hostname and (parsed.username is not None or parsed.password is not None):
            host = parsed.hostname
            if parsed.port is not None:
                host += f":{parsed.port}"
            return urlunsplit((parsed.scheme, f"[REDACTED]@{host}", parsed.path, parsed.query, parsed.fragment))
    except ValueError:
        pass
    return value


def redact(value: Any, *, key: str | None = None) -> Any:
    normalized = key.lower().replace("-", "_") if key else None
    if normalized is not None and (normalized in SENSITIVE_KEYS or normalized.replace("_", "") in SENSITIVE_KEYS):
        return "[REDACTED]"
    if isinstance(value, SecretBytes):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(k): redact(v, key=str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(v) for v in value]
    if isinstance(value, str):
        return _redact_string(value)
    return value
