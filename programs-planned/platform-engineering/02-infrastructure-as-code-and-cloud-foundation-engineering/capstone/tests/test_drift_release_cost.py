from __future__ import annotations

import json
from pathlib import Path

from cloud_model.cost_quota import evaluate_cost_profile, evaluate_quotas
from cloud_model.drift import classify_difference, validate_move_map
from cloud_model.release import evaluate_candidate

CAPSTONE = Path(__file__).resolve().parents[1]


def load(rel: str):
    return json.loads((CAPSTONE / rel).read_text())


def test_drift_categories() -> None:
    emergency = classify_difference(load("fixtures/migrations/remote-emergency-rule.json"))
    normalization = classify_difference(load("fixtures/migrations/provider-normalization.json"))
    conflict = classify_difference(load("fixtures/migrations/lineage-conflict.json"))
    assert emergency["category"] == "intentional-emergency-change"
    assert normalization["category"] == "provider-normalization"
    assert conflict["category"] == "state-conflict"


def test_move_map_is_unique() -> None:
    assert validate_move_map(load("fixtures/migrations/network-moves.json")) == []
    errors = validate_move_map([{"from": "a", "to": "x"}, {"from": "b", "to": "x"}])
    assert errors


def test_cost_and_quotas() -> None:
    cost = evaluate_cost_profile(load("fixtures/economics/cost-profile.json"))
    quotas = evaluate_quotas(load("fixtures/economics/quota-profile.json"))
    assert cost["withinBudget"] is True
    assert cost["decision"] == "pass"
    assert quotas["allSufficient"] is True


def test_release_candidates() -> None:
    accepted = evaluate_candidate(load("releases/accepted/candidate.json"))
    rejected = evaluate_candidate(load("releases/rejected-public-ssh/candidate.json"))
    review = evaluate_candidate(load("releases/review-nat-cost/candidate.json"))
    not_executed = evaluate_candidate(load("releases/not-executed-live-cloud/candidate.json"))
    assert accepted["decision"] == "dependency-light-only"
    assert rejected["decision"] == "reject"
    assert review["decision"] == "review"
    assert not_executed["decision"] == "not-releasable"
