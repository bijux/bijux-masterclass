#!/usr/bin/env python3
"""Audit whether a state-boundary migration is ready for cutover."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class MigrationCase:
    name: str
    expected_decision: str
    mutate: Callable[[Path], None] | None = None


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contract_path(case_dir: Path) -> Path:
    return case_dir / "migration-contract.json"


def decision_path(case_dir: Path) -> Path:
    return case_dir / "migration-decision.json"


def source_dir(case_dir: Path) -> Path:
    return case_dir / "source"


def target_dir(case_dir: Path) -> Path:
    return case_dir / "target"


def mutate_partial_copy(case_dir: Path) -> None:
    (target_dir(case_dir) / "report.md").unlink()


def mutate_unbounded_change(case_dir: Path) -> None:
    contract = read_json(contract_path(case_dir))
    contract["boundary"]["changed_surfaces"].append("metric-schema")
    write_json(contract_path(case_dir), contract)

    decision = read_json(decision_path(case_dir))
    decision["boundary"]["changed_surfaces"].append("metric-schema")
    write_json(decision_path(case_dir), decision)


def mutate_no_rollback(case_dir: Path) -> None:
    decision = read_json(decision_path(case_dir))
    decision["rollback"]["ready"] = False
    decision["rollback"]["retained"] = False
    write_json(decision_path(case_dir), decision)


def mutate_unverified_consumer(case_dir: Path) -> None:
    decision = read_json(decision_path(case_dir))
    decision["consumer_cutover"]["verified"] = False
    decision["consumer_cutover"]["receipts"] = []
    write_json(decision_path(case_dir), decision)


def mutate_ownerless_target(case_dir: Path) -> None:
    decision = read_json(decision_path(case_dir))
    decision["owners"]["registry"] = ""
    write_json(decision_path(case_dir), decision)


def mutate_stale_exception(case_dir: Path) -> None:
    decision = read_json(decision_path(case_dir))
    decision["exception"] = {
        "expires_at": "2025-12-31",
        "owner": "release-owner",
        "reason": "consumer verification service unavailable",
        "removal_condition": "record clean consumer retrieval",
    }
    write_json(decision_path(case_dir), decision)


def mutate_tool_ownership_overreach(case_dir: Path) -> None:
    decision = read_json(decision_path(case_dir))
    decision["owners"]["dvc"] = "consumer-lifecycle"
    decision["owners"]["registry"] = "artifact-lineage"
    write_json(decision_path(case_dir), decision)


CASES = (
    MigrationCase("complete-cutover", "APPROVE_CUTOVER"),
    MigrationCase("partial-copy", "BLOCK_CUTOVER", mutate_partial_copy),
    MigrationCase(
        "unbounded-change",
        "BLOCK_CUTOVER",
        mutate_unbounded_change,
    ),
    MigrationCase("no-rollback", "BLOCK_CUTOVER", mutate_no_rollback),
    MigrationCase(
        "unverified-consumer",
        "BLOCK_CUTOVER",
        mutate_unverified_consumer,
    ),
    MigrationCase(
        "ownerless-target",
        "BLOCK_CUTOVER",
        mutate_ownerless_target,
    ),
    MigrationCase(
        "stale-exception",
        "BLOCK_CUTOVER",
        mutate_stale_exception,
    ),
    MigrationCase(
        "tool-ownership-overreach",
        "BLOCK_CUTOVER",
        mutate_tool_ownership_overreach,
    ),
)


def prepare_case(
    case: MigrationCase,
    *,
    specimen: Path,
    publish: Path,
    workspace: Path,
) -> Path:
    case_dir = workspace / case.name
    shutil.copytree(publish, source_dir(case_dir))
    shutil.copytree(publish, target_dir(case_dir))
    shutil.copy2(
        specimen / "migration-contract.json",
        contract_path(case_dir),
    )
    shutil.copy2(
        specimen / "migration-decision.json",
        decision_path(case_dir),
    )
    if case.mutate is not None:
        case.mutate(case_dir)
    return case_dir


def file_inventory(root: Path) -> dict[str, dict[str, object]]:
    return {
        path.relative_to(root).as_posix(): {
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def target_matches_source(case_dir: Path) -> bool:
    return file_inventory(source_dir(case_dir)) == file_inventory(
        target_dir(case_dir)
    )


def one_boundary_changes(
    contract: dict[str, object],
    decision: dict[str, object],
) -> bool:
    contract_boundary = contract.get("boundary", {})
    decision_boundary = decision.get("boundary", {})
    if not isinstance(contract_boundary, dict) or not isinstance(
        decision_boundary,
        dict,
    ):
        return False
    expected = ["consumer-location"]
    return (
        contract_boundary.get("changed_surfaces") == expected
        and decision_boundary.get("changed_surfaces") == expected
    )


def before_and_after_proofs_named(
    contract: dict[str, object],
    decision: dict[str, object],
) -> bool:
    policy = contract.get("evidence_policy", {})
    before = decision.get("before_evidence", {})
    after = decision.get("after_evidence", {})
    if not all(
        isinstance(value, dict)
        for value in (policy, before, after)
    ):
        return False
    required_before = set(policy.get("required_before", []))
    required_after = set(policy.get("required_after", []))
    return (
        bool(required_before)
        and bool(required_after)
        and required_before == set(before)
        and required_after == set(after)
        and all(before.values())
        and all(after.values())
    )


def rollback_is_ready(
    contract: dict[str, object],
    decision: dict[str, object],
) -> bool:
    policy = contract.get("rollback_policy", {})
    rollback = decision.get("rollback", {})
    if not isinstance(policy, dict) or not isinstance(rollback, dict):
        return False
    retained_until = set(policy.get("old_boundary_retained_until", []))
    return (
        rollback.get("ready") is True
        and rollback.get("retained") is True
        and rollback.get("reference") == policy.get("rollback_reference")
        and retained_until == {"target-verification", "consumer-retrieval"}
    )


def consumer_cutover_is_verified(
    decision: dict[str, object],
) -> bool:
    cutover = decision.get("consumer_cutover", {})
    after = decision.get("after_evidence", {})
    if not isinstance(cutover, dict) or not isinstance(after, dict):
        return False
    receipts = set(cutover.get("receipts", []))
    expected = after.get("consumer-retrieval")
    return (
        cutover.get("verified") is True
        and bool(expected)
        and expected in receipts
    )


def responsibilities_have_owners(
    contract: dict[str, object],
    decision: dict[str, object],
) -> bool:
    policy = contract.get("ownership_policy", {})
    owners = decision.get("owners", {})
    if not isinstance(policy, dict) or not isinstance(owners, dict):
        return False
    return set(owners) == set(policy) and all(owners.values())


def exception_is_current(
    contract: dict[str, object],
    decision: dict[str, object],
    evaluation_date: date,
) -> bool:
    exception = decision.get("exception")
    if exception is None:
        return True
    policy = contract.get("exception_policy", {})
    if not isinstance(exception, dict) or not isinstance(policy, dict):
        return False
    required = set(policy.get("required_fields", []))
    if required != set(exception) or not all(exception.values()):
        return False
    try:
        expiry = date.fromisoformat(str(exception["expires_at"]))
    except ValueError:
        return False
    return expiry >= evaluation_date


def tool_boundaries_match_policy(
    contract: dict[str, object],
    decision: dict[str, object],
) -> bool:
    if not responsibilities_have_owners(contract, decision):
        return True
    return decision.get("owners") == contract.get("ownership_policy")


def decision_matches_contract(
    contract: dict[str, object],
    decision: dict[str, object],
) -> bool:
    contract_boundary = contract.get("boundary", {})
    decision_boundary = decision.get("boundary", {})
    if not isinstance(contract_boundary, dict) or not isinstance(
        decision_boundary,
        dict,
    ):
        return False
    return (
        decision.get("migration_id") == contract.get("migration_id")
        and decision.get("decision") == "APPROVE_CUTOVER"
        and decision_boundary.get("source_reference")
        == contract_boundary.get("source_reference")
        and decision_boundary.get("target_reference")
        == contract_boundary.get("target_reference")
        and decision_boundary.get("changed_surfaces")
        == contract_boundary.get("changed_surfaces")
    )


def preserved_invariants_are_explicit(
    contract: dict[str, object],
) -> bool:
    boundary = contract.get("boundary", {})
    if not isinstance(boundary, dict):
        return False
    return set(boundary.get("preserved_invariants", [])) == {
        "artifact-bytes",
        "exact-inventory",
        "promoted-meaning",
        "source-provenance",
    }


def assess_case(
    case: MigrationCase,
    case_dir: Path,
    output_root: Path,
    evaluation_date: date,
) -> dict[str, object]:
    contract = read_json(contract_path(case_dir))
    decision = read_json(decision_path(case_dir))
    checks = {
        "target_matches_source": target_matches_source(case_dir),
        "one_boundary_changes": one_boundary_changes(contract, decision),
        "before_and_after_proofs_named": before_and_after_proofs_named(
            contract,
            decision,
        ),
        "rollback_is_ready": rollback_is_ready(contract, decision),
        "consumer_cutover_is_verified": consumer_cutover_is_verified(
            decision
        ),
        "responsibilities_have_owners": responsibilities_have_owners(
            contract,
            decision,
        ),
        "exception_is_current": exception_is_current(
            contract,
            decision,
            evaluation_date,
        ),
        "tool_boundaries_match_policy": tool_boundaries_match_policy(
            contract,
            decision,
        ),
        "decision_matches_contract": decision_matches_contract(
            contract,
            decision,
        ),
        "preserved_invariants_are_explicit": (
            preserved_invariants_are_explicit(contract)
        ),
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    actual_decision = (
        "APPROVE_CUTOVER" if not failed_checks else "BLOCK_CUTOVER"
    )
    assessment = {
        "checks": checks,
        "decision": actual_decision,
        "expected_decision": case.expected_decision,
        "failed_checks": failed_checks,
        "finding": case.name.replace("-", "_").upper(),
        "result": (
            "PASS"
            if actual_decision == case.expected_decision
            else "FAIL"
        ),
        "source_inventory": file_inventory(source_dir(case_dir)),
        "target_inventory": file_inventory(target_dir(case_dir)),
    }
    evidence_path = case_dir / "assessment.json"
    write_json(evidence_path, assessment)
    assessment["evidence"] = evidence_path.relative_to(output_root).as_posix()
    return assessment


def run_audit(args: argparse.Namespace) -> dict[str, object]:
    if args.workspace.exists():
        shutil.rmtree(args.workspace)
    args.workspace.mkdir(parents=True)
    evaluation_date = date.fromisoformat(args.evaluation_date)

    findings = []
    for case in CASES:
        case_dir = prepare_case(
            case,
            specimen=args.specimen,
            publish=args.publish,
            workspace=args.workspace,
        )
        findings.append(
            assess_case(
                case,
                case_dir,
                args.output.parent,
                evaluation_date,
            )
        )

    return {
        "audit": "boundary_migration_governance",
        "decision_rule": (
            "Approve cutover only when one declared boundary changes while "
            "content, evidence, rollback, consumers, ownership, exceptions, "
            "and tool responsibilities remain governed."
        ),
        "evaluation_date": args.evaluation_date,
        "findings": findings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--publish", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evaluation-date", required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = run_audit(args)
    write_json(args.output, report)

    if args.check:
        failures = [
            item
            for item in report["findings"]
            if item["result"] != "PASS"
        ]
        if failures:
            names = ", ".join(item["finding"] for item in failures)
            raise SystemExit(f"unexpected migration audit decisions: {names}")


if __name__ == "__main__":
    main()
