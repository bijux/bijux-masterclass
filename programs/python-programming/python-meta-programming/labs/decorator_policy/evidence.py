from __future__ import annotations

import inspect
import json
import warnings

from .retry import retry
from .validation import UnsupportedHintError, validated


class TransientDeliveryError(RuntimeError):
    """Controlled retryable failure for the evidence packet."""


def retry_evidence() -> dict[str, object]:
    """Show that retry policy multiplies execution and owns waiting."""

    events: list[str] = []
    attempts = 0

    def record_sleep(delay: float) -> None:
        events.append(f"sleep:{delay:.1f}")

    @retry(
        exceptions=(TransientDeliveryError,),
        max_attempts=3,
        backoff_seconds=(0.1, 0.2),
        sleep=record_sleep,
    )
    def deliver(incident_id: str) -> str:
        nonlocal attempts
        attempts += 1
        events.append(f"attempt:{attempts}")
        if attempts < 3:
            raise TransientDeliveryError(f"attempt {attempts}")
        return f"delivered:{incident_id}"

    policy_before_call = deliver.__retry_policy__
    result = deliver("INC-42")
    return {
        "events": events,
        "result": result,
        "underlying_execution_count": attempts,
        "captured_policy": {
            "exceptions": list(policy_before_call.exception_names),
            "max_attempts": policy_before_call.max_attempts,
            "backoff_seconds": list(policy_before_call.backoff_seconds),
        },
        "visible_signature": str(inspect.signature(deliver)),
    }


def exhausted_retry_evidence() -> dict[str, object]:
    """Prove the finite stopping rule and preservation of the final failure."""

    failure = TransientDeliveryError("still unavailable")
    attempts = 0

    @retry(
        exceptions=(TransientDeliveryError,),
        max_attempts=2,
        backoff_seconds=(0.0,),
        sleep=lambda _: None,
    )
    def fail() -> None:
        nonlocal attempts
        attempts += 1
        raise failure

    try:
        fail()
    except TransientDeliveryError as caught:
        same_failure_object = caught is failure
    else:
        same_failure_object = False

    return {
        "attempts": attempts,
        "same_final_failure_object": same_failure_object,
        "stopping_rule": "raise the second retryable failure after two total attempts",
    }


def validation_evidence() -> dict[str, object]:
    """Contrast strict enforcement, warning-only observation, and refusal."""

    executions: list[str] = []

    @validated()
    def strict_render(incident_id: str) -> str:
        executions.append("strict")
        return incident_id

    @validated(on_mismatch="warn", validate_return=False)
    def warning_render(incident_id: str) -> object:
        executions.append("warning")
        return incident_id

    try:
        strict_render(42)  # type: ignore[arg-type]
    except TypeError as error:
        strict_failure = str(error)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warning_result = warning_render(42)  # type: ignore[arg-type]

    try:

        @validated()
        def unsupported(values: list[int]) -> int:
            return len(values)

    except UnsupportedHintError as error:
        refused_hint = str(error)

    return {
        "strict": {
            "failure": strict_failure,
            "executed": "strict" in executions,
        },
        "warning": {
            "message": str(caught[0].message),
            "executed": "warning" in executions,
            "result": warning_result,
        },
        "refusal": {
            "message": refused_hint,
            "timing": "decoration",
        },
    }


def build_evidence() -> dict[str, dict[str, object]]:
    """Build the deterministic evidence packets taught in Module 05."""

    return {
        "retry": retry_evidence(),
        "retry_exhausted": exhausted_retry_evidence(),
        "validation": validation_evidence(),
    }


def render_evidence() -> str:
    """Render stable JSON for learner inspection and review."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
