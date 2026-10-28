from __future__ import annotations

import argparse
import json
from pathlib import Path

import jwt

ROOT = Path(__file__).resolve().parent
ISSUER = "https://issuer.security.test"
AUDIENCE = "analysis-runs-api"
KID = "fixture-rsa-2026-01"


def issue_token(
    *,
    now: int,
    subject: str = "user-01",
    tenant: str = "tenant-01",
    scope: str = "projects:read projects:write runs:read runs:write",
    audience: str = AUDIENCE,
    issuer: str = ISSUER,
    token_id: str = "fixture-jti-01",
    lifetime: int = 600,
    roles: list[str] | None = None,
    assurance: str = "baseline",
    algorithm: str = "RS256",
) -> str:
    key = (ROOT / "private" / "fixture-private.pem").read_bytes()
    claims = {
        "iss": issuer,
        "aud": audience,
        "sub": subject,
        "tenant": tenant,
        "scope": scope,
        "iat": now,
        "nbf": now,
        "exp": now + lifetime,
        "auth_time": now,
        "jti": token_id,
        "roles": roles or [],
        "acr": assurance,
        "client_id": "course-client",
    }
    return jwt.encode(claims, key, algorithm=algorithm, headers={"kid": KID, "typ": "at+jwt"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", type=int, required=True)
    parser.add_argument("--subject", default="user-01")
    parser.add_argument("--tenant", default="tenant-01")
    parser.add_argument("--scope", default="projects:read")
    args = parser.parse_args()
    print(issue_token(now=args.now, subject=args.subject, tenant=args.tenant, scope=args.scope))


if __name__ == "__main__":
    main()
