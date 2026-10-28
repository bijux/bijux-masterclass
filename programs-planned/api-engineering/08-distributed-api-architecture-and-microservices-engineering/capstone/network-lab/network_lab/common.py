from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler
from typing import Any

from distributed_api.capability import CapabilityAuthority, CapabilityClaims
from distributed_api.model import RequestContext, Unauthorized, ValidationError


@dataclass(frozen=True)
class Caller:
    subject: str
    tenant: str
    scopes: frozenset[str]


def bearer_token(handler: BaseHTTPRequestHandler) -> str:
    value = handler.headers.get("Authorization", "")
    if not value.startswith("Bearer "):
        raise Unauthorized("missing bearer token")
    token = value.removeprefix("Bearer ").strip()
    if not token:
        raise Unauthorized("missing bearer token")
    return token


def verify_request_token(
    handler: BaseHTTPRequestHandler,
    *,
    issuer: str,
    audience: str,
    action: str,
    key: bytes,
    now: int | None = None,
) -> Caller:
    authority = CapabilityAuthority(issuer=issuer, key=key)
    claims = authority.verify(
        bearer_token(handler),
        audience=audience,
        tenant=handler.headers.get("X-Course-Tenant", ""),
        action=action,
        now=int(time.time()) if now is None else now,
    )
    scopes = frozenset(item for item in claims.resource.split(" ") if item)
    if action not in scopes:
        raise Unauthorized("delegated request lacks required scope")
    return Caller(claims.subject, claims.tenant, scopes)


def mint_request_token(
    *,
    issuer: str,
    audience: str,
    subject: str,
    tenant: str,
    scopes: frozenset[str],
    action: str,
    key: bytes,
    now: int | None = None,
    lifetime: int = 60,
    jti: str,
) -> str:
    issued_at = int(time.time()) if now is None else now
    if action not in scopes:
        raise ValidationError("cannot delegate a scope the caller does not hold")
    authority = CapabilityAuthority(issuer=issuer, key=key)
    return authority.mint(
        CapabilityClaims(
            jti=jti,
            issuer=issuer,
            audience=audience,
            subject=subject,
            tenant=tenant,
            resource=" ".join(sorted(scopes)),
            action=action,
            issued_at=issued_at,
            expires_at=issued_at + lifetime,
        )
    )


def context(caller: Caller, *, workload: str) -> RequestContext:
    return RequestContext(
        subject=caller.subject,
        tenant=caller.tenant,
        workload=workload,
        scopes=caller.scopes,
        deadline_ms=10_000,
    )


def read_json(handler: BaseHTTPRequestHandler, *, maximum: int = 1_048_576) -> Any:
    raw_length = handler.headers.get("Content-Length")
    if raw_length is None:
        raise ValidationError("Content-Length is required")
    try:
        length = int(raw_length)
    except ValueError as exc:
        raise ValidationError("invalid Content-Length") from exc
    if length < 0 or length > maximum:
        raise ValidationError("request body exceeds laboratory limit")
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValidationError("invalid JSON body") from exc


def send_json(
    handler: BaseHTTPRequestHandler,
    status: int,
    value: object,
) -> None:
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def request_json(
    method: str,
    url: str,
    *,
    body: object | None = None,
    token: str | None = None,
    tenant: str | None = None,
    timeout: float = 2.0,
) -> tuple[int, Any]:
    data = None
    headers: dict[str, str] = {}
    if body is not None:
        data = json.dumps(body, separators=(",", ":")).encode()
        headers["Content-Type"] = "application/json"
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    if tenant is not None:
        headers["X-Course-Tenant"] = tenant
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read()
            return response.status, json.loads(payload) if payload else None
    except urllib.error.HTTPError as exc:
        payload = exc.read()
        value = json.loads(payload) if payload else {"error": exc.reason}
        return exc.code, value
