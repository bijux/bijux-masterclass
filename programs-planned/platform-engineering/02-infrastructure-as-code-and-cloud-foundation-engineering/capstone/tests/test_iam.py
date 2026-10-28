from __future__ import annotations

import json
from pathlib import Path

from cloud_model.iam import evaluate_policy, validate_policy_shape

CAPSTONE = Path(__file__).resolve().parents[1]


def load(rel: str):
    return json.loads((CAPSTONE / rel).read_text())


def test_policy_vectors() -> None:
    policy = load("fixtures/identity/atlas-instance-policy.json")
    assert validate_policy_shape(policy) == []
    for vector in load("fixtures/identity/atlas-instance-vectors.json"):
        result = evaluate_policy(
            policy,
            action=vector["action"],
            resource=vector["resource"],
            context=vector.get("context", {}),
        )
        assert result["decision"] == vector["expected"], vector["name"]


def test_explicit_deny_overrides_allow() -> None:
    policy = load("fixtures/identity/atlas-instance-policy.json")
    result = evaluate_policy(
        policy,
        action="s3:PutObject",
        resource="arn:aws:s3:::atlas-dev-backup/results/r1",
        context={"aws:SecureTransport": "false"},
    )
    assert result["decision"] == "deny"
    assert result["reason"] == "explicit-deny"


def test_wildcard_admin_policy_flagged() -> None:
    errors = validate_policy_shape(load("fixtures/identity/bad-administrator-policy.json"))
    assert any("wildcard" in error for error in errors)
