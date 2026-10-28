from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HttpOutcome:
    eligibility: str
    outcome: str


def classify_http_outcome(operation: str, status: int) -> HttpOutcome:
    """Classify one completed request for the course availability SLI.

    Client-policy and validation failures are excluded because the service
    fulfilled the protocol correctly. Timeout, overload, and server failures
    remain eligible bad events because they represent unavailable service for a
    valid journey. The policy is explicit and shared by both implementations.
    """

    if not 100 <= status <= 599:
        raise ValueError("status must be an HTTP status code")
    if operation.startswith("internal") or operation.startswith("/internal/"):
        return HttpOutcome("excluded", "neutral")
    if 200 <= status < 400:
        return HttpOutcome("eligible", "good")
    if status in {408, 425, 429} or status >= 500:
        return HttpOutcome("eligible", "bad")
    return HttpOutcome("excluded", "neutral")
