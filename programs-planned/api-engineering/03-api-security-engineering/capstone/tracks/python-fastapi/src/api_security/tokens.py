from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence

import jwt
from jwt.algorithms import RSAAlgorithm

from .errors import SecurityControlError
from .models import Principal


class Clock(Protocol):
    def now(self) -> int: ...


class RevocationStore(Protocol):
    def is_revoked(self, issuer: str, token_id: str, now: int) -> bool: ...


@dataclass(frozen=True, slots=True)
class TokenProfile:
    issuer: str
    audience: str
    algorithms: tuple[str, ...] = ("RS256",)
    token_type: str = "at+jwt"
    clock_skew_seconds: int = 30
    max_lifetime_seconds: int = 900
    required_claims: tuple[str, ...] = (
        "iss", "aud", "sub", "exp", "iat", "jti", "tenant", "scope"
    )


@dataclass(slots=True)
class MemoryRevocations:
    revoked: set[tuple[str, str]]

    def is_revoked(self, issuer: str, token_id: str, now: int) -> bool:
        return (issuer, token_id) in self.revoked


def _numeric_date(claims: Mapping[str, object], name: str) -> int:
    value = claims.get(name)
    if isinstance(value, bool) or not isinstance(value, int):
        raise SecurityControlError("invalid-token", f"claim {name} must be an integer NumericDate", 401)
    return value


def _audience_matches(value: object, expected: str) -> bool:
    if isinstance(value, str):
        return value == expected
    if isinstance(value, list) and all(isinstance(x, str) for x in value):
        return expected in value
    return False


def validate_access_token(
    token: str,
    *,
    profile: TokenProfile,
    jwks: Mapping[str, object],
    now: int,
    revocations: RevocationStore,
) -> Principal:
    if token.count(".") != 2:
        raise SecurityControlError("invalid-token", "credential is not a compact JWT", 401)
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as exc:
        raise SecurityControlError("invalid-token", "JWT header is invalid", 401) from exc
    alg = header.get("alg")
    typ = header.get("typ")
    kid = header.get("kid")
    if alg not in profile.algorithms:
        raise SecurityControlError("invalid-token", "JWT algorithm is not accepted", 401)
    if typ != profile.token_type:
        raise SecurityControlError("invalid-token", "JWT type is not accepted", 401)
    if not isinstance(kid, str) or not kid:
        raise SecurityControlError("invalid-token", "JWT key identifier is required", 401)
    keys = jwks.get("keys")
    if not isinstance(keys, list):
        raise SecurityControlError("identity-configuration", "trusted JWKS has no key list", 500)
    matches = [k for k in keys if isinstance(k, dict) and k.get("kid") == kid]
    if len(matches) != 1:
        raise SecurityControlError("invalid-token", "JWT key identifier is unknown or ambiguous", 401)
    try:
        key = RSAAlgorithm.from_jwk(json.dumps(matches[0]))
        claims = jwt.decode(
            token,
            key=key,
            algorithms=[alg],
            options={
                "verify_signature": True,
                "verify_aud": False,
                "verify_iss": False,
                "verify_exp": False,
                "verify_nbf": False,
                "verify_iat": False,
                "require": list(profile.required_claims),
            },
        )
    except jwt.PyJWTError as exc:
        raise SecurityControlError("invalid-token", "JWT signature or structure is invalid", 401) from exc
    if claims.get("iss") != profile.issuer:
        raise SecurityControlError("invalid-token", "JWT issuer is not accepted", 401)
    if not _audience_matches(claims.get("aud"), profile.audience):
        raise SecurityControlError("invalid-token", "JWT audience is not accepted", 401)
    iat = _numeric_date(claims, "iat")
    exp = _numeric_date(claims, "exp")
    nbf = claims.get("nbf", iat)
    if isinstance(nbf, bool) or not isinstance(nbf, int):
        raise SecurityControlError("invalid-token", "claim nbf must be an integer NumericDate", 401)
    skew = profile.clock_skew_seconds
    if iat > now + skew or nbf > now + skew:
        raise SecurityControlError("invalid-token", "JWT is not yet valid", 401)
    if exp <= now - skew:
        raise SecurityControlError("invalid-token", "JWT is expired", 401)
    if exp <= iat or exp - iat > profile.max_lifetime_seconds:
        raise SecurityControlError("invalid-token", "JWT lifetime is not accepted", 401)
    subject = claims.get("sub")
    tenant = claims.get("tenant")
    token_id = claims.get("jti")
    scope = claims.get("scope")
    if not all(isinstance(v, str) and v for v in (subject, tenant, token_id, scope)):
        raise SecurityControlError("invalid-token", "JWT identity claims are invalid", 401)
    if revocations.is_revoked(profile.issuer, token_id, now):
        raise SecurityControlError("revoked-token", "credential has been revoked", 401)
    roles_value = claims.get("roles", [])
    if not isinstance(roles_value, list) or not all(isinstance(x, str) for x in roles_value):
        raise SecurityControlError("invalid-token", "roles claim is invalid", 401)
    auth_time = claims.get("auth_time", iat)
    if isinstance(auth_time, bool) or not isinstance(auth_time, int) or auth_time > now + skew:
        raise SecurityControlError("invalid-token", "authentication time is invalid", 401)
    assurance = claims.get("acr", "baseline")
    if not isinstance(assurance, str):
        raise SecurityControlError("invalid-token", "assurance claim is invalid", 401)
    client_id = claims.get("client_id")
    if client_id is not None and not isinstance(client_id, str):
        raise SecurityControlError("invalid-token", "client identifier is invalid", 401)
    return Principal(
        subject=subject,
        tenant=tenant,
        scopes=frozenset(scope.split()),
        roles=frozenset(roles_value),
        client_id=client_id,
        token_id=token_id,
        assurance=assurance,
        auth_age_seconds=max(0, now - auth_time),
    )
