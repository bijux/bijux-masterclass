from __future__ import annotations

from typing import Any, Callable

from .envelope import EventEnvelope


def build_event_ingress(
    validate: Callable[[dict[str, Any]], EventEnvelope],
    dispatch: Callable[[EventEnvelope], dict[str, Any]],
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Framework-independent core used by an optional FastAPI route."""

    def ingress(body: dict[str, Any]) -> dict[str, Any]:
        event = validate(body)
        return dispatch(event)

    return ingress
