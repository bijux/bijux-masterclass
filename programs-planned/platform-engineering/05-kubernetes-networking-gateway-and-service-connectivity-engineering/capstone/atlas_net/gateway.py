from __future__ import annotations

from .models import Decision, HttpMatch, HttpRoute, Listener, ReferenceGrant


def hostname_matches(pattern: str, hostname: str) -> bool:
    pattern = pattern.lower().rstrip(".")
    hostname = hostname.lower().rstrip(".")
    if pattern.startswith("*."):
        suffix = pattern[1:]
        return hostname.endswith(suffix) and hostname.count(".") == pattern.count(".")
    return pattern == hostname


def reference_allowed(
    route: HttpRoute,
    grants: list[ReferenceGrant],
) -> bool:
    if route.namespace == route.backend_namespace:
        return True
    return any(
        grant.namespace == route.backend_namespace
        and route.namespace in grant.from_namespaces
        and "HTTPRoute" in grant.from_kinds
        and "Service" in grant.to_kinds
        for grant in grants
    )


def attach(
    listener: Listener,
    route: HttpRoute,
    grants: list[ReferenceGrant],
) -> Decision:
    if route.namespace not in listener.allowed_namespaces:
        return Decision(
            False,
            "NotAllowedByListener",
            {"observedGeneration": route.generation},
        )
    hostname_intersects = any(
        hostname_matches(listener.hostname, route_hostname)
        or hostname_matches(route_hostname, listener.hostname)
        for route_hostname in route.hostnames
    )
    if not hostname_intersects:
        return Decision(
            False,
            "NoMatchingListenerHostname",
            {"observedGeneration": route.generation},
        )
    if not reference_allowed(route, grants):
        return Decision(
            False,
            "RefNotPermitted",
            {"observedGeneration": route.generation},
        )
    return Decision(
        True,
        "Accepted",
        {"observedGeneration": route.generation},
    )


def _path_score(match: HttpMatch, path: str) -> tuple[int, int]:
    if match.path_type == "Exact":
        return (2, len(match.path)) if path == match.path else (-1, -1)
    if match.path_type == "PathPrefix":
        matched = path == match.path or path.startswith(match.path.rstrip("/") + "/")
        return (1, len(match.path)) if matched else (-1, -1)
    return (-1, -1)


def select_route(
    routes: list[HttpRoute],
    listener: Listener,
    *,
    host: str,
    path: str,
    method: str,
    headers: dict[str, str],
    grants: list[ReferenceGrant],
) -> Decision:
    normalized_headers = {key.lower(): value for key, value in headers.items()}
    candidates: list[tuple[int, int, str, int, HttpRoute]] = []

    for route in routes:
        if not attach(listener, route, grants).allowed:
            continue
        if not any(hostname_matches(name, host) for name in route.hostnames):
            continue

        for index, match in enumerate(route.matches):
            path_score = _path_score(match, path)
            if path_score[0] < 0:
                continue
            if match.method and match.method != method:
                continue
            if any(
                normalized_headers.get(key.lower()) != value
                for key, value in match.headers
            ):
                continue
            candidates.append(
                (path_score[0], path_score[1], route.name, index, route)
            )

    if not candidates:
        return Decision(False, "NoMatchingRoute", {})

    candidates.sort(
        key=lambda item: (item[0], item[1], item[2]),
        reverse=True,
    )
    winner = candidates[0][-1]
    return Decision(
        True,
        "Matched",
        {
            "route": winner.name,
            "namespace": winner.namespace,
            "candidates": [item[2] for item in candidates],
        },
    )


def canonical_forwarded(
    peer_ip: str,
    scheme: str,
    host: str,
    incoming: dict[str, str],
) -> dict[str, str]:
    """Replace untrusted forwarding identity at the trusted edge."""

    forbidden = {
        "forwarded",
        "x-forwarded-for",
        "x-forwarded-proto",
        "x-forwarded-host",
    }
    result = {
        key: value for key, value in incoming.items() if key.lower() not in forbidden
    }
    result.update(
        {
            "Forwarded": f'for="{peer_ip}";proto={scheme};host="{host}"',
            "X-Forwarded-For": peer_ip,
            "X-Forwarded-Proto": scheme,
            "X-Forwarded-Host": host,
        }
    )
    return result


def retry_allowed(
    method: str,
    idempotency_key: str | None,
    body_replayable: bool,
    remaining_ms: int,
    minimum_attempt_ms: int = 100,
) -> Decision:
    safe_operation = method.upper() in {
        "GET",
        "HEAD",
        "OPTIONS",
        "PUT",
        "DELETE",
    } or bool(idempotency_key)
    allowed = (
        safe_operation
        and body_replayable
        and remaining_ms >= minimum_attempt_ms
    )
    return Decision(
        allowed,
        "RetryAllowed" if allowed else "RetryRejected",
        {
            "safeOperation": safe_operation,
            "bodyReplayable": body_replayable,
            "remainingMs": remaining_ms,
        },
    )
