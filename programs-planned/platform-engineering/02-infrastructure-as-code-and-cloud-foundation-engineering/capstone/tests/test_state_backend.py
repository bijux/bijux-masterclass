from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

import pytest

from cloud_model.state_backend import (
    LockRegistry,
    StateError,
    validate_backend_profile,
    validate_state_transition,
)

CAPSTONE = Path(__file__).resolve().parents[1]


def load(rel: str):
    return json.loads((CAPSTONE / rel).read_text())


def test_safe_backend_profile() -> None:
    assert validate_backend_profile(load("fixtures/state/backend-safe.json")) == []


def test_unsafe_backend_reports_multiple_failures() -> None:
    errors = validate_backend_profile(load("fixtures/state/backend-unsafe.json"))
    assert len(errors) >= 6
    assert any("workload runtime authority" in error for error in errors)


def test_state_serial_and_lineage() -> None:
    validate_state_transition(
        load("fixtures/state/state-current.json"),
        load("fixtures/state/state-next.json"),
    )
    with pytest.raises(StateError, match="lineage"):
        validate_state_transition(
            load("fixtures/state/state-current.json"),
            load("fixtures/state/state-wrong-lineage.json"),
        )


def test_lock_registry_excludes_concurrent_owner() -> None:
    registry = LockRegistry()
    now = datetime(2026, 8, 9, tzinfo=timezone.utc)
    lease = registry.acquire("atlas/dev/foundation", "pipeline-a", now=now)
    with pytest.raises(StateError, match="pipeline-a"):
        registry.acquire("atlas/dev/foundation", "pipeline-b", now=now)
    registry.release(lease.key, lease.token)
    second = registry.acquire("atlas/dev/foundation", "pipeline-b", now=now)
    assert second.owner == "pipeline-b"


def test_expired_lock_can_be_reacquired() -> None:
    registry = LockRegistry()
    now = datetime(2026, 8, 9, tzinfo=timezone.utc)
    registry.acquire("state", "a", ttl_seconds=1, now=now)
    lease = registry.acquire("state", "b", now=now + timedelta(seconds=2))
    assert lease.owner == "b"


def test_wrong_lock_token_rejected() -> None:
    registry = LockRegistry()
    lease = registry.acquire("state", "a")
    with pytest.raises(StateError, match="token"):
        registry.release(lease.key, "not-the-token")
