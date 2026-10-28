from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from typing import Sequence
from urllib.parse import urlsplit

from .errors import SecurityControlError


@dataclass(frozen=True, slots=True)
class ValidatedDestination:
    url: str
    hostname: str
    port: int
    addresses: tuple[str, ...]


def _public_address(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise SecurityControlError("invalid-address", "resolver returned an invalid IP address") from exc
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        address = address.ipv4_mapped
    return address.is_global


def validate_destination(
    url: str,
    *,
    addresses: Sequence[str],
    allowed_schemes: Sequence[str] = ("https",),
    allowed_ports: Sequence[int] = (443,),
) -> ValidatedDestination:
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        raise SecurityControlError("invalid-url", "outbound URL is invalid") from exc
    if parsed.scheme.lower() not in {x.lower() for x in allowed_schemes}:
        raise SecurityControlError("scheme", "outbound URL scheme is prohibited")
    if parsed.username is not None or parsed.password is not None:
        raise SecurityControlError("userinfo", "outbound URL user information is prohibited")
    if parsed.fragment:
        raise SecurityControlError("fragment", "outbound URL fragment is prohibited")
    if not parsed.hostname:
        raise SecurityControlError("host", "outbound URL host is required")
    try:
        port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    except ValueError as exc:
        raise SecurityControlError("port", "outbound URL port is invalid") from exc
    if port not in allowed_ports:
        raise SecurityControlError("port", "outbound URL port is prohibited")
    if not addresses:
        raise SecurityControlError("dns-empty", "outbound host resolved to no addresses")
    if not all(_public_address(value) for value in addresses):
        raise SecurityControlError("forbidden-address", "outbound host resolves to a forbidden address")
    return ValidatedDestination(url, parsed.hostname.lower(), port, tuple(addresses))


def verify_connected_peer(destination: ValidatedDestination, peer: str) -> None:
    normalized = str(ipaddress.ip_address(peer))
    approved = {str(ipaddress.ip_address(value)) for value in destination.addresses}
    if normalized not in approved:
        raise SecurityControlError("peer-mismatch", "connected peer was not approved for this request")
