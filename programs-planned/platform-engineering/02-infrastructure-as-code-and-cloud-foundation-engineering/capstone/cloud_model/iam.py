from __future__ import annotations

import fnmatch
from typing import Any


class PolicyError(ValueError):
    pass


def _values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def _matches(patterns: Any, value: str) -> bool:
    return any(fnmatch.fnmatchcase(value, pattern) for pattern in _values(patterns))


def _conditions_match(conditions: dict[str, Any], context: dict[str, str]) -> bool:
    for operator, entries in conditions.items():
        if operator not in {"StringEquals", "StringLike", "Bool"}:
            raise PolicyError(f"unsupported course condition operator: {operator}")
        for key, expected in entries.items():
            actual = context.get(key)
            if actual is None:
                return False
            expected_values = _values(expected)
            if operator == "StringEquals" and actual not in expected_values:
                return False
            if operator == "StringLike" and not any(fnmatch.fnmatchcase(actual, p) for p in expected_values):
                return False
            if operator == "Bool" and actual.lower() not in {v.lower() for v in expected_values}:
                return False
    return True


def evaluate_policy(
    policy: dict[str, Any],
    *,
    action: str,
    resource: str,
    context: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Evaluate a bounded identity-policy subset for course vectors.

    This is intentionally not a complete AWS IAM policy engine. It supports
    Action, Resource, Effect, and selected conditions so that least-authority
    vectors are executable and their limitation remains visible.
    """

    context = context or {}
    matching_allows: list[str] = []
    matching_denies: list[str] = []
    for index, statement in enumerate(policy.get("Statement", [])):
        if not _matches(statement.get("Action", []), action):
            continue
        if not _matches(statement.get("Resource", []), resource):
            continue
        if not _conditions_match(statement.get("Condition", {}), context):
            continue
        sid = str(statement.get("Sid", f"statement-{index}"))
        if statement.get("Effect") == "Deny":
            matching_denies.append(sid)
        elif statement.get("Effect") == "Allow":
            matching_allows.append(sid)
    if matching_denies:
        decision = "deny"
        reason = "explicit-deny"
    elif matching_allows:
        decision = "allow"
        reason = "explicit-allow"
    else:
        decision = "deny"
        reason = "implicit-deny"
    return {
        "decision": decision,
        "reason": reason,
        "allowStatements": matching_allows,
        "denyStatements": matching_denies,
    }


def validate_policy_shape(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if policy.get("Version") != "2012-10-17":
        errors.append("AWS policy Version must be 2012-10-17")
    for index, statement in enumerate(policy.get("Statement", [])):
        sid = statement.get("Sid", f"statement-{index}")
        if statement.get("Effect") not in {"Allow", "Deny"}:
            errors.append(f"{sid}: invalid Effect")
        if not statement.get("Action"):
            errors.append(f"{sid}: Action is required")
        if not statement.get("Resource"):
            errors.append(f"{sid}: Resource is required")
        actions = _values(statement.get("Action", []))
        resources = _values(statement.get("Resource", []))
        if statement.get("Effect") == "Allow" and "*" in actions and "*" in resources:
            errors.append(f"{sid}: wildcard action and resource requires explicit exception")
    return errors
