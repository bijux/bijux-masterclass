from __future__ import annotations

from typing import Iterable, Mapping, Any


class RuntimePolicyError(ValueError):
    pass


def validate_route(route: Mapping[str,Any]) -> None:
    if route.get("domainAuthz") not in {"owner-service","graph-and-owner-services"}:
        raise RuntimePolicyError("domain-policy-at-edge")
    if not str(route.get("host","")).endswith(".example.invalid"):
        raise RuntimePolicyError("unexpected-course-host")
    if route.get("edgeAuthn") not in {"oauth2","mtls"}:
        raise RuntimePolicyError("unsupported-edge-authn")


def route_drift(desired: Iterable[Mapping[str,Any]], current: Iterable[Mapping[str,Any]]) -> dict[str,Any]:
    d={r["id"]:dict(r) for r in desired}; c={r["id"]:dict(r) for r in current}
    missing=sorted(set(d)-set(c)); extra=sorted(set(c)-set(d)); changed=sorted(k for k in set(d)&set(c) if d[k]!=c[k])
    return {"missing":missing,"extra":extra,"changed":changed,"inSync":not(missing or extra or changed)}
