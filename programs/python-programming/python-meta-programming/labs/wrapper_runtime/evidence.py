from __future__ import annotations

import inspect
import json
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar


ResultT = TypeVar("ResultT")


class DemonstrationFailure(RuntimeError):
    """Failure used to prove that thin observation does not rewrite exceptions."""


def tracing_decorator(
    label: str,
    events: list[str],
) -> Callable[[Callable[..., ResultT]], Callable[..., ResultT]]:
    """Record factory, decoration, and call timing for one wrapper layer."""

    events.append(f"factory:{label}")

    def decorate(function: Callable[..., ResultT]) -> Callable[..., ResultT]:
        events.append(f"decorate:{label}:{function.__name__}")

        @wraps(function)
        def wrapped(*args: Any, **kwargs: Any) -> ResultT:
            events.append(f"enter:{label}")
            try:
                result = function(*args, **kwargs)
            except BaseException as error:
                events.append(f"raise:{label}:{type(error).__name__}")
                raise
            events.append(f"exit:{label}")
            return result

        return wrapped

    return decorate


def lifecycle_evidence() -> dict[str, object]:
    """Expose decorator expression, application, and invocation order."""

    events: list[str] = []

    @tracing_decorator("outer", events)
    @tracing_decorator("inner", events)
    def render_status(incident_id: str, *, severity: str = "warning") -> str:
        events.append(f"body:{incident_id}:{severity}")
        return f"{incident_id}:{severity}"

    definition_events = list(events)
    closure_names = sorted(inspect.getclosurevars(render_status).nonlocals)
    result = render_status("INC-42", severity="critical")
    return {
        "definition_events": definition_events,
        "call_events": events[len(definition_events) :],
        "result": result,
        "outer_wrapper_closure": closure_names,
        "visible_signature": str(inspect.signature(render_status)),
        "wrapper_depth": _wrapper_depth(render_status),
    }


def observing_decorator(
    events: list[str],
) -> Callable[[Callable[..., ResultT]], Callable[..., ResultT]]:
    """Observe one call while preserving its result and exception object."""

    def decorate(function: Callable[..., ResultT]) -> Callable[..., ResultT]:
        @wraps(function)
        def wrapped(*args: Any, **kwargs: Any) -> ResultT:
            events.append(f"start:{function.__name__}")
            try:
                result = function(*args, **kwargs)
            except BaseException as error:
                events.append(f"failure:{type(error).__name__}")
                raise
            events.append(f"success:{type(result).__name__}")
            return result

        return wrapped

    return decorate


def thin_wrapper_evidence() -> dict[str, object]:
    """Prove result identity and exception identity across thin observation."""

    events: list[str] = []
    result_marker = object()
    failure = DemonstrationFailure("controlled failure")

    @observing_decorator(events)
    def succeed() -> object:
        return result_marker

    @observing_decorator(events)
    def fail() -> None:
        raise failure

    returned = succeed()
    try:
        fail()
    except DemonstrationFailure as caught:
        same_failure = caught is failure
    else:
        same_failure = False

    return {
        "events": events,
        "same_result_object": returned is result_marker,
        "same_exception_object": same_failure,
        "failure_type": type(failure).__name__,
    }


def metadata_evidence() -> dict[str, object]:
    """Compare a bare forwarding shell with a preserved wrapper."""

    def bare(function: Callable[..., ResultT]) -> Callable[..., ResultT]:
        def wrapped(*args: Any, **kwargs: Any) -> ResultT:
            return function(*args, **kwargs)

        return wrapped

    def preserved(function: Callable[..., ResultT]) -> Callable[..., ResultT]:
        @wraps(function)
        def wrapped(*args: Any, **kwargs: Any) -> ResultT:
            return function(*args, **kwargs)

        return wrapped

    @bare
    def bare_handler(incident_id: str, *, severity: str = "warning") -> str:
        """Render one incident."""

        return f"{incident_id}:{severity}"

    @preserved
    def preserved_handler(incident_id: str, *, severity: str = "warning") -> str:
        """Render one incident."""

        return f"{incident_id}:{severity}"

    return {
        "bare": {
            "name": bare_handler.__name__,
            "doc": bare_handler.__doc__,
            "signature": str(inspect.signature(bare_handler)),
            "has_wrapped": hasattr(bare_handler, "__wrapped__"),
        },
        "preserved": {
            "name": preserved_handler.__name__,
            "doc": preserved_handler.__doc__,
            "signature": str(inspect.signature(preserved_handler)),
            "has_wrapped": hasattr(preserved_handler, "__wrapped__"),
            "unwrap_is_original": inspect.unwrap(preserved_handler)
            is preserved_handler.__wrapped__,
        },
    }


def _wrapper_depth(function: Callable[..., object]) -> int:
    depth = 0
    current = function
    while hasattr(current, "__wrapped__"):
        depth += 1
        current = current.__wrapped__
    return depth


def build_evidence() -> dict[str, dict[str, object]]:
    """Build the deterministic evidence packets taught in Module 04."""

    return {
        "lifecycle": lifecycle_evidence(),
        "thin_wrapper": thin_wrapper_evidence(),
        "metadata": metadata_evidence(),
    }


def render_evidence() -> str:
    """Render stable JSON for learner inspection and review."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
