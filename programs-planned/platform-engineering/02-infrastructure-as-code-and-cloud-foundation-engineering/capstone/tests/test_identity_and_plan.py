from __future__ import annotations

import json
from pathlib import Path

import pytest

from cloud_model.identity import canonical_json, digest_object
from cloud_model.plan import (
    PlanError,
    apply_moves,
    assert_plan_current,
    build_plan,
    plan_summary,
    saved_plan_identity,
)

CAPSTONE = Path(__file__).resolve().parents[1]


def load(rel: str):
    return json.loads((CAPSTONE / rel).read_text())


def test_canonical_json_is_stable() -> None:
    left = {"b": 2, "a": [3, 1]}
    right = {"a": [3, 1], "b": 2}
    assert canonical_json(left) == canonical_json(right)
    assert digest_object(left) == digest_object(right)


def test_plan_adds_endpoint_without_replacing_network() -> None:
    config = load("fixtures/plan/config-v2-intended.json")["resources"]
    state = load("fixtures/plan/state-v1.json")["resources"]
    actions = build_plan(config, state)
    summary = plan_summary(actions)
    assert summary["counts"]["create"] == 1
    assert summary["counts"]["replace"] == 0
    assert summary["counts"]["delete"] == 0


def test_unstable_keys_propose_delete_and_create() -> None:
    config = load("fixtures/plan/config-v2-unstable-keys.json")["resources"]
    state = load("fixtures/plan/state-v1.json")["resources"]
    summary = plan_summary(build_plan(config, state))
    assert summary["counts"]["create"] == 2
    assert summary["counts"]["delete"] == 2


def test_moves_preserve_remote_identity() -> None:
    state = load("fixtures/migrations/flat-network-state.json")["resources"]
    moves = load("fixtures/migrations/network-moves.json")
    moved = apply_moves(state, moves)
    by_address = {row["address"]: row for row in moved}
    assert by_address["module.network.aws_vpc.this"]["remote_id"] == "vpc-001"
    assert by_address['module.network.aws_subnet.private["euc1-az1"]']["remote_id"] == "subnet-001"


def test_duplicate_move_target_rejected() -> None:
    state = load("fixtures/migrations/flat-network-state.json")["resources"]
    moves = [
        {"from": "aws_vpc.atlas", "to": "module.network.aws_vpc.this"},
        {"from": "aws_subnet.private_a", "to": "module.network.aws_vpc.this"},
    ]
    with pytest.raises(PlanError):
        apply_moves(state, moves)


def test_saved_plan_binds_source_state_and_target() -> None:
    config = load("fixtures/plan/config-v2-intended.json")["resources"]
    state_doc = load("fixtures/plan/state-v1.json")
    actions = build_plan(config, state_doc["resources"])
    identity = saved_plan_identity(
        source_digest="source-1",
        dependency_digest="deps-1",
        state_lineage=state_doc["lineage"],
        state_serial=state_doc["serial"],
        target={"account": "100000000005", "region": "eu-central-1"},
        actions=actions,
    )
    assert_plan_current(
        identity,
        source_digest="source-1",
        dependency_digest="deps-1",
        state_lineage="atlas-lineage-1",
        state_serial=1,
        target={"account": "100000000005", "region": "eu-central-1"},
    )
    with pytest.raises(PlanError, match="stateSerial"):
        assert_plan_current(
            identity,
            source_digest="source-1",
            dependency_digest="deps-1",
            state_lineage="atlas-lineage-1",
            state_serial=2,
            target={"account": "100000000005", "region": "eu-central-1"},
        )
