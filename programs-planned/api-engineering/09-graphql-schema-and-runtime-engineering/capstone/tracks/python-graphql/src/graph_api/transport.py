"""Course profile for GraphQL-over-HTTP request admission."""

from __future__ import annotations

from dataclasses import dataclass


GRAPH_RESPONSE = "application/graphql-response+json"


@dataclass(frozen=True)
class HttpRequest:
    method: str
    accept: str
    content_type: str | None
    operation_type: str


@dataclass(frozen=True)
class HttpDecision:
    accepted: bool
    status: int
    response_content_type: str
    reason: str


def evaluate(request: HttpRequest) -> HttpDecision:
    """Evaluate the bounded HTTP transport profile used in the course."""

    if GRAPH_RESPONSE not in request.accept:
        return HttpDecision(
            accepted=False,
            status=406,
            response_content_type=GRAPH_RESPONSE,
            reason="unsupported Accept",
        )

    if request.method == "GET" and request.operation_type != "query":
        return HttpDecision(
            accepted=False,
            status=405,
            response_content_type=GRAPH_RESPONSE,
            reason="GET may not execute mutation or subscription",
        )

    if (
        request.method == "POST"
        and request.content_type != "application/json"
    ):
        return HttpDecision(
            accepted=False,
            status=415,
            response_content_type=GRAPH_RESPONSE,
            reason="POST requires application/json in course profile",
        )

    if request.method not in {"GET", "POST"}:
        return HttpDecision(
            accepted=False,
            status=405,
            response_content_type=GRAPH_RESPONSE,
            reason="unsupported method",
        )

    return HttpDecision(
        accepted=True,
        status=200,
        response_content_type=GRAPH_RESPONSE,
        reason="accepted",
    )
