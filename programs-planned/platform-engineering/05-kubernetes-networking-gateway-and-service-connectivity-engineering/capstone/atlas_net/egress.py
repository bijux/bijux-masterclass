from __future__ import annotations

from ipaddress import ip_address
from urllib.parse import urljoin, urlparse

from .models import Decision


def classify(address: str) -> str:
    peer = ip_address(address)
    if peer.is_loopback:
        return "loopback"
    if peer.is_link_local:
        return "link-local"
    if peer.is_private:
        return "private"
    if peer.is_multicast:
        return "multicast"
    if peer.is_unspecified:
        return "unspecified"
    if peer.is_reserved:
        return "reserved"
    return "public"


def validate_destination(
    url: str,
    answers: list[str],
    connected_peer: str,
    *,
    allowed_hosts: set[str],
    allowed_private: set[str] | None = None,
) -> Decision:
    """Bind one approved HTTPS hostname to the actual connected peer."""

    allowed_non_public = allowed_private or set()
    parsed = urlparse(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.fragment
    ):
        return Decision(False, "URLPolicyRejected", {})
    if parsed.hostname not in allowed_hosts:
        return Decision(False, "HostNotAllowed", {"host": parsed.hostname})
    if connected_peer not in answers:
        return Decision(
            False,
            "PeerNotInResolvedSet",
            {"peer": connected_peer, "answers": answers},
        )

    classes = {address: classify(address) for address in answers}
    forbidden = [
        address
        for address, address_class in classes.items()
        if address_class != "public" and address not in allowed_non_public
    ]
    if forbidden:
        return Decision(
            False,
            "ForbiddenAddressClass",
            {"addresses": forbidden, "classes": classes},
        )
    return Decision(
        True,
        "DestinationAllowed",
        {"host": parsed.hostname, "peer": connected_peer, "classes": classes},
    )


def validate_redirect(
    current_url: str,
    location: str,
    *,
    allowed_hosts: set[str],
) -> Decision:
    target = urljoin(current_url, location)
    parsed = urlparse(target)
    if parsed.scheme != "https" or parsed.hostname not in allowed_hosts:
        return Decision(False, "RedirectRejected", {"target": target})
    return Decision(True, "RedirectAllowed", {"target": target})
