from __future__ import annotations

import json
from pathlib import Path

import pytest

from cloud_model.network import (
    NetworkError,
    select_route,
    subnet_from_slot,
    trace_path,
    validate_network_plan,
)

CAPSTONE = Path(__file__).resolve().parents[1]


def load(rel: str):
    return json.loads((CAPSTONE / rel).read_text())


def test_subnet_slot_calculation() -> None:
    assert subnet_from_slot("10.64.0.0/16", 24, 0) == "10.64.0.0/24"
    assert subnet_from_slot("10.64.0.0/16", 20, 1) == "10.64.16.0/20"


def test_safe_network_plan() -> None:
    assert validate_network_plan(load("fixtures/network/network-plan-safe.json")) == []


def test_overlap_rejected() -> None:
    errors = validate_network_plan(load("fixtures/network/network-plan-overlap.json"))
    assert any("overlap" in error for error in errors)


def test_data_internet_route_rejected() -> None:
    errors = validate_network_plan(load("fixtures/network/network-plan-data-internet.json"))
    assert any("data subnet" in error for error in errors)


def test_longest_prefix_route_selection() -> None:
    route = select_route("10.64.16.10", [
        {"destination": "0.0.0.0/0", "target": "nat"},
        {"destination": "10.64.0.0/16", "target": "local"},
        {"destination": "10.64.16.0/20", "target": "inspection"},
    ])
    assert route.target == "inspection"


def test_private_egress_is_az_local() -> None:
    plan = load("fixtures/network/network-plan-safe.json")
    result = trace_path(plan, source_subnet="private-b", destination_ip="1.1.1.1")
    assert result["target"] == "nat-b"
    assert result["allowed"] is True


def test_unknown_subnet_rejected() -> None:
    with pytest.raises(NetworkError):
        trace_path(load("fixtures/network/network-plan-safe.json"), source_subnet="missing", destination_ip="1.1.1.1")
