from __future__ import annotations

from dataclasses import dataclass
from ipaddress import ip_address, ip_network
from typing import Iterable, Sequence

from .errors import SecurityControlError

CRITICAL_SINGLETONS = frozenset(
    {
        "authorization",
        "content-length",
        "host",
        "x-api-key",
        "x-forwarded-host",
        "x-forwarded-proto",
    }
)


@dataclass(frozen=True, slots=True)
class EdgeContext:
    client_peer: str
    external_scheme: str
    external_host: str
    origin: str
    trusted_proxy: bool


def _normalized_headers(headers: Sequence[tuple[str, str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for name, value in headers:
        key = name.strip().lower()
        result.setdefault(key, []).append(value.strip())
    for name in CRITICAL_SINGLETONS:
        if len(result.get(name, [])) > 1:
            raise SecurityControlError("ambiguous-header", f"multiple {name} header fields")
    return result


def _peer_trusted(peer: str, configured: Sequence[str]) -> bool:
    address = ip_address(peer)
    for item in configured:
        if "/" in item and address in ip_network(item, strict=False):
            return True
        if "/" not in item and address == ip_address(item):
            return True
    return False


def evaluate_edge(
    *,
    peer: str,
    headers: Sequence[tuple[str, str]],
    allowed_hosts: Sequence[str],
    trusted_proxies: Sequence[str] = (),
    direct_scheme: str = "https",
) -> EdgeContext:
    parsed = _normalized_headers(headers)
    trusted = _peer_trusted(peer, trusted_proxies)
    host = (parsed.get("host") or [""])[0].lower()
    scheme = direct_scheme.lower()
    if trusted:
        host = (parsed.get("x-forwarded-host") or [host])[0].lower()
        scheme = (parsed.get("x-forwarded-proto") or [scheme])[0].lower()
    if scheme not in {"https", "http"}:
        raise SecurityControlError("scheme-not-allowed", "external scheme is not accepted")
    allowed = {h.lower() for h in allowed_hosts}
    if host not in allowed:
        raise SecurityControlError("host-not-allowed", "external host is not accepted")
    origin = f"{scheme}://{host}"
    return EdgeContext(peer, scheme, host, origin, trusted)
