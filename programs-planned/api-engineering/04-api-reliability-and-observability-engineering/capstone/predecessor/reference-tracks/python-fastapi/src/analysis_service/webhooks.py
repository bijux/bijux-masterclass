from __future__ import annotations

from urllib.parse import SplitResult, urlsplit

import httpx

from .failures import ServiceError

APPROVED_WEBHOOK_HOST = "hooks.example.test"


def parse_destination(url: str) -> SplitResult:
    parsed = urlsplit(url)
    try:
        approved_port = parsed.port in {None, 443}
    except ValueError:
        approved_port = False
    approved = (
        parsed.scheme == "https"
        and parsed.hostname == APPROVED_WEBHOOK_HOST
        and parsed.username is None
        and parsed.password is None
        and parsed.fragment == ""
        and approved_port
    )
    if not approved:
        raise ServiceError(
            422,
            "Request validation failed",
            "Webhook destinations must use the approved HTTPS host.",
            "validation",
        )
    return parsed


def validate_destination(url: str) -> None:
    parse_destination(url)


class HttpxOutboundTransport:
    """Route approved training webhook URLs to the local receiver.

    Production code would resolve and connect to the approved destination while
    applying DNS/IP controls. This adapter intentionally keeps the course
    network-independent and does not pretend to be a general SSRF defence.
    """

    def __init__(self, training_base: str):
        self.training_base = training_base.rstrip("/")

    def _route(self, url: str) -> str:
        parsed = parse_destination(url)
        query = f"?{parsed.query}" if parsed.query else ""
        return f"{self.training_base}{parsed.path or '/'}{query}"

    def post(
        self,
        url: str,
        body: bytes,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> int:
        timeout = httpx.Timeout(timeout_seconds)
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                self._route(url),
                content=body,
                headers=headers,
            )
        return response.status_code
