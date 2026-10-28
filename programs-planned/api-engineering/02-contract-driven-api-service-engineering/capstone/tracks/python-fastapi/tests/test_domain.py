from __future__ import annotations

import pytest

from analysis_service.domain import (
    RunSnapshot,
    RunState,
    canonical_json,
    evolve,
    filter_fingerprint,
    parse_cursor,
    parse_project_etag,
    project_etag,
    request_fingerprint,
    retry_delay_seconds,
    verify_webhook_signature,
    webhook_signature,
)
from analysis_service.failures import ServiceError


def test_canonical_json_orders_objects_but_preserves_arrays() -> None:
    assert canonical_json({"b": 2, "a": [2, 1]}) == b'{"a":[2,1],"b":2}'


def test_nonfinite_numbers_are_rejected() -> None:
    with pytest.raises(TypeError):
        canonical_json({"n": float("nan")})


def test_fingerprint_binds_owner_operation_and_body() -> None:
    body = {"projectId": "prj_0001"}
    assert len(
        {
            request_fingerprint("create", "learner", body),
            request_fingerprint("create", "other", body),
            request_fingerprint("update", "learner", body),
        }
    ) == 3


def test_filter_fingerprint_is_order_independent() -> None:
    assert filter_fingerprint("list", "learner", {"b": 2, "a": 1}) == (
        filter_fingerprint("list", "learner", {"a": 1, "b": 2})
    )


def test_etag_roundtrip() -> None:
    assert parse_project_etag(project_etag("prj_0001", 7), "prj_0001") == 7


def test_absent_cursor() -> None:
    assert parse_cursor(None) is None


@pytest.mark.parametrize(
    "value",
    [
        "0",
        "-1",
        "1e3",
        " 1",
        "١",
        "9223372036854775808",
    ],
)
def test_bad_cursor(value: str) -> None:
    with pytest.raises(ServiceError):
        parse_cursor(value)


def test_running_cancellation_is_request_then_observation() -> None:
    requested = evolve(
        RunSnapshot(RunState.RUNNING, 40),
        "request-cancel",
    )
    assert requested.state is RunState.RUNNING
    assert requested.cancellation_requested
    assert evolve(requested, "observe-cancel").state is RunState.CANCELED


def test_terminal_transition_fails() -> None:
    with pytest.raises(ServiceError):
        evolve(
            RunSnapshot(RunState.COMPLETED, 100),
            "request-cancel",
        )


def test_signature_matches_cross_language_vector() -> None:
    secret = "course-callback-signing-secret"
    timestamp = "1700000000"
    body = (
        b'{"eventId":"evt_0001","eventType":"analysis.completed",'
        b'"runId":"run_0001"}'
    )
    expected = (
        "sha256="
        "7fe00dbc1737f3cffaf66adcad12576f40959bb9dd4f797587342dfe69f48f13"
    )
    assert webhook_signature(secret, timestamp, body) == expected
    assert verify_webhook_signature(secret, timestamp, body, expected)
    assert not verify_webhook_signature(secret, "1700000001", body, expected)


def test_retry_delay_is_bounded() -> None:
    assert [retry_delay_seconds(i) for i in range(1, 5)] == [1, 2, 4, 8]
    assert retry_delay_seconds(99) == 300
def test_canonical_json_rejects_cross_language_number_ambiguity() -> None:
    with pytest.raises(TypeError):
        canonical_json({"value": 1.0})
    with pytest.raises(TypeError):
        canonical_json({"value": 9_007_199_254_740_992})


def test_canonical_json_sorts_unicode_by_code_point() -> None:
    assert canonical_json({"😀": 1, "￿": 2}) == (
        '{"￿":2,"😀":1}'.encode("utf-8")
    )


