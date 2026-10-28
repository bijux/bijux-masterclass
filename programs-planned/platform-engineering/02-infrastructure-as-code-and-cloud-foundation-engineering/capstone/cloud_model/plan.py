from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable

from .identity import digest_object


@dataclass(frozen=True)
class PlanAction:
    address: str
    action: str
    reason: str
    before: dict[str, Any] | None
    after: dict[str, Any] | None
    remote_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class PlanError(ValueError):
    pass


def _by_address(rows: Iterable[dict[str, Any]], *, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        address = str(row.get("address", ""))
        if not address:
            raise PlanError(f"{label} row has no address")
        if address in result:
            raise PlanError(f"duplicate {label} address: {address}")
        result[address] = row
    return result


def apply_moves(
    state_rows: list[dict[str, Any]],
    moves: list[dict[str, str]] | None,
) -> list[dict[str, Any]]:
    moved = [dict(row) for row in state_rows]
    by_address = _by_address(moved, label="state")
    for mapping in moves or []:
        source = mapping["from"]
        target = mapping["to"]
        if source not in by_address:
            raise PlanError(f"move source is absent: {source}")
        if target in by_address:
            raise PlanError(f"move target already exists: {target}")
        row = by_address.pop(source)
        row["address"] = target
        by_address[target] = row
    return list(by_address.values())


def _changed_keys(before: dict[str, Any], after: dict[str, Any]) -> set[str]:
    keys = set(before) | set(after)
    return {key for key in keys if before.get(key) != after.get(key)}


def build_plan(
    config_rows: list[dict[str, Any]],
    state_rows: list[dict[str, Any]],
    *,
    moves: list[dict[str, str]] | None = None,
) -> list[PlanAction]:
    """Calculate a bounded semantic plan for course fixtures.

    This models identity, update, replacement, and deletion decisions. It does
    not claim to reproduce OpenTofu provider planning.
    """

    state_rows = apply_moves(state_rows, moves)
    config = _by_address(config_rows, label="configuration")
    state = _by_address(state_rows, label="state")
    actions: list[PlanAction] = []

    for address in sorted(set(config) | set(state)):
        desired = config.get(address)
        current = state.get(address)
        if current is None and desired is not None:
            actions.append(
                PlanAction(address, "create", "address is absent from state", None,
                           dict(desired.get("attributes", {})))
            )
            continue
        if desired is None and current is not None:
            actions.append(
                PlanAction(address, "delete", "address is absent from configuration",
                           dict(current.get("attributes", {})), None,
                           str(current.get("remote_id", "")) or None)
            )
            continue
        assert desired is not None and current is not None
        if desired.get("type") != current.get("type"):
            actions.append(
                PlanAction(address, "replace", "resource type changed",
                           dict(current.get("attributes", {})),
                           dict(desired.get("attributes", {})),
                           str(current.get("remote_id", "")) or None)
            )
            continue
        before = dict(current.get("attributes", {}))
        after = dict(desired.get("attributes", {}))
        changed = _changed_keys(before, after)
        if not changed:
            actions.append(
                PlanAction(address, "no-op", "declared attributes match state",
                           before, after, str(current.get("remote_id", "")) or None)
            )
            continue
        replace_on_change = set(desired.get("replace_on_change", []))
        replacement_keys = sorted(changed & replace_on_change)
        if replacement_keys:
            action = "replace"
            reason = "replacement-sensitive attributes changed: " + ", ".join(replacement_keys)
        else:
            action = "update"
            reason = "attributes changed: " + ", ".join(sorted(changed))
        actions.append(
            PlanAction(address, action, reason, before, after,
                       str(current.get("remote_id", "")) or None)
        )
    return actions


def plan_summary(actions: list[PlanAction]) -> dict[str, Any]:
    counts = {name: 0 for name in ("create", "update", "replace", "delete", "no-op")}
    for action in actions:
        counts[action.action] = counts.get(action.action, 0) + 1
    destructive = [a.address for a in actions if a.action in {"delete", "replace"}]
    payload = {
        "counts": counts,
        "destructiveAddresses": destructive,
        "actions": [action.as_dict() for action in actions],
    }
    payload["planDigest"] = digest_object(payload)
    return payload


def saved_plan_identity(
    *,
    source_digest: str,
    dependency_digest: str,
    state_lineage: str,
    state_serial: int,
    target: dict[str, str],
    actions: list[PlanAction],
) -> dict[str, Any]:
    payload = {
        "sourceDigest": source_digest,
        "dependencyDigest": dependency_digest,
        "stateLineage": state_lineage,
        "stateSerial": state_serial,
        "target": target,
        "plan": plan_summary(actions),
    }
    payload["identity"] = digest_object(payload)
    return payload


def assert_plan_current(
    identity: dict[str, Any],
    *,
    source_digest: str,
    dependency_digest: str,
    state_lineage: str,
    state_serial: int,
    target: dict[str, str],
) -> None:
    checks = {
        "sourceDigest": source_digest,
        "dependencyDigest": dependency_digest,
        "stateLineage": state_lineage,
        "stateSerial": state_serial,
        "target": target,
    }
    for key, value in checks.items():
        if identity.get(key) != value:
            raise PlanError(f"saved plan is stale or mis-targeted: {key}")
