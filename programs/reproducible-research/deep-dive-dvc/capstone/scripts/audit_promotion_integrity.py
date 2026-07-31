#!/usr/bin/env python3
"""Audit whether a release candidate earns promotion authority."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yaml


@dataclass(frozen=True)
class PromotionCase:
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
    return case_dir / "promotion-contract.json"


def decision_path(case_dir: Path) -> Path:
    return case_dir / "promotion-decision.json"


def publish_dir(case_dir: Path) -> Path:
    return case_dir / "publish"


def mutate_tampered_artifact(case_dir: Path) -> None:
    report = publish_dir(case_dir) / "report.md"
    report.write_text(
        report.read_text(encoding="utf-8")
        + "\nThis unreviewed sentence was added after approval.\n",
        encoding="utf-8",
    )


def mutate_unlisted_artifact(case_dir: Path) -> None:
    (publish_dir(case_dir) / "debug-notes.txt").write_text(
        "candidate-only investigation notes\n",
        encoding="utf-8",
    )


def mutate_threshold_drift(case_dir: Path) -> None:
    params_path = publish_dir(case_dir) / "params.yaml"
    params = yaml.safe_load(params_path.read_text(encoding="utf-8"))
    params["decision"]["threshold"] = 0.67
    params_path.write_text(
        yaml.safe_dump(params, sort_keys=True),
        encoding="utf-8",
    )

    manifest_path = publish_dir(case_dir) / "manifest.json"
    manifest = read_json(manifest_path)
    artifacts = manifest["artifacts"]
    assert isinstance(artifacts, list)
    entry = next(item for item in artifacts if item["path"] == "params.yaml")
    entry["bytes"] = params_path.stat().st_size
    entry["sha256"] = sha256(params_path)
    write_json(manifest_path, manifest)


def mutate_mutable_registry_reference(case_dir: Path) -> None:
    contract = read_json(contract_path(case_dir))
    contract["registry_reference"] = "incident-escalation/latest"
    write_json(contract_path(case_dir), contract)

    decision = read_json(decision_path(case_dir))
    decision["registry_reference"] = "incident-escalation/latest"
    write_json(decision_path(case_dir), decision)


def mutate_stale_source_approval(case_dir: Path) -> None:
    decision = read_json(decision_path(case_dir))
    decision["git_revision"] = "6c1b23050147eea7a112adf01e2a5d4b73dd18ea"
    write_json(decision_path(case_dir), decision)


def mutate_missing_required_review(case_dir: Path) -> None:
    decision = read_json(decision_path(case_dir))
    approvals = decision["approvals"]
    assert isinstance(approvals, list)
    decision["approvals"] = [
        approval
        for approval in approvals
        if approval["role"] != "risk-reviewer"
    ]
    write_json(decision_path(case_dir), decision)


CASES = (
    PromotionCase("complete-promotion", "ACCEPT"),
    PromotionCase(
        "tampered-artifact",
        "BLOCK",
        mutate_tampered_artifact,
    ),
    PromotionCase(
        "unlisted-artifact",
        "BLOCK",
        mutate_unlisted_artifact,
    ),
    PromotionCase(
        "threshold-drift",
        "BLOCK",
        mutate_threshold_drift,
    ),
    PromotionCase(
        "mutable-registry-reference",
        "BLOCK",
        mutate_mutable_registry_reference,
    ),
    PromotionCase(
        "stale-source-approval",
        "BLOCK",
        mutate_stale_source_approval,
    ),
    PromotionCase(
        "missing-required-review",
        "BLOCK",
        mutate_missing_required_review,
    ),
)


def prepare_case(
    case: PromotionCase,
    *,
    specimen: Path,
    source_publish: Path,
    workspace: Path,
) -> Path:
    case_dir = workspace / case.name
    shutil.copytree(source_publish, publish_dir(case_dir))
    shutil.copy2(
        specimen / "promotion-contract.json",
        contract_path(case_dir),
    )
    shutil.copy2(
        specimen / "promotion-decision.json",
        decision_path(case_dir),
    )
    if case.mutate is not None:
        case.mutate(case_dir)
    return case_dir


def registry_reference_is_immutable(contract: dict[str, object]) -> bool:
    reference = str(contract.get("registry_reference", ""))
    segments = {
        segment.lower()
        for segment in reference.replace(":", "/").split("/")
        if segment
    }
    mutable_tokens = {"best", "current", "latest"}
    return len(segments) >= 2 and not segments.intersection(mutable_tokens)


def inventory_matches_contract(
    contract: dict[str, object],
    manifest: dict[str, object],
    candidate: Path,
) -> bool:
    required = set(contract.get("required_artifacts", []))
    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list):
        return False
    recorded = {
        str(entry.get("path", ""))
        for entry in artifacts
        if isinstance(entry, dict)
    }
    present = {
        path.relative_to(candidate).as_posix()
        for path in candidate.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    return bool(required) and required == recorded == present


def artifact_integrity_matches_manifest(
    manifest: dict[str, object],
    candidate: Path,
) -> bool:
    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list) or not artifacts:
        return False
    for entry in artifacts:
        if not isinstance(entry, dict):
            return False
        target = candidate / str(entry.get("path", ""))
        if not target.is_file():
            return False
        if target.stat().st_size != int(entry.get("bytes", -1)):
            return False
        if sha256(target) != entry.get("sha256"):
            return False
    return True


def promoted_claims_agree(
    contract: dict[str, object],
    manifest: dict[str, object],
    candidate: Path,
) -> bool:
    claims = contract.get("promoted_claims", {})
    if not isinstance(claims, dict):
        return False
    expected = claims.get("decision_threshold")

    params = yaml.safe_load((candidate / "params.yaml").read_text(encoding="utf-8"))
    params_threshold = params.get("decision", {}).get("threshold")

    decision = manifest.get("decision", {})
    if not isinstance(decision, dict):
        return False
    manifest_threshold = decision.get("threshold")

    try:
        return (
            float(expected)
            == float(params_threshold)
            == float(manifest_threshold)
        )
    except (TypeError, ValueError):
        return False


def source_lock_matches_contract(
    contract: dict[str, object],
    source_lock: Path,
) -> bool:
    source = contract.get("source", {})
    return (
        isinstance(source, dict)
        and source_lock.is_file()
        and source.get("dvc_lock_sha256") == sha256(source_lock)
    )


def decision_matches_candidate(
    contract: dict[str, object],
    decision: dict[str, object],
) -> bool:
    source = contract.get("source", {})
    approval = contract.get("approval", {})
    if not isinstance(source, dict) or not isinstance(approval, dict):
        return False
    expected = {
        "release_id": contract.get("release_id"),
        "registry_reference": contract.get("registry_reference"),
        "git_revision": source.get("git_revision"),
        "dvc_lock_sha256": source.get("dvc_lock_sha256"),
        "decision": approval.get("required_decision"),
    }
    return all(decision.get(key) == value for key, value in expected.items())


def required_review_roles_approved(
    contract: dict[str, object],
    decision: dict[str, object],
) -> bool:
    approval = contract.get("approval", {})
    approvals = decision.get("approvals", [])
    if not isinstance(approval, dict) or not isinstance(approvals, list):
        return False
    required = set(approval.get("required_roles", []))
    present = {
        item.get("role")
        for item in approvals
        if isinstance(item, dict) and item.get("reviewer")
    }
    return bool(required) and required.issubset(present)


def consumer_contract_is_bounded(contract: dict[str, object]) -> bool:
    consumer = contract.get("consumer_contract", {})
    required = set(contract.get("required_artifacts", []))
    if not isinstance(consumer, dict):
        return False
    supported = set(consumer.get("supported_files", []))
    unsupported = consumer.get("unsupported_sources", [])
    return bool(supported) and supported.issubset(required) and bool(unsupported)


def assess_case(
    case: PromotionCase,
    case_dir: Path,
    source_lock: Path,
    output_root: Path,
) -> dict[str, object]:
    contract = read_json(contract_path(case_dir))
    decision = read_json(decision_path(case_dir))
    manifest = read_json(publish_dir(case_dir) / "manifest.json")
    candidate = publish_dir(case_dir)

    checks = {
        "registry_reference_is_immutable": registry_reference_is_immutable(
            contract
        ),
        "inventory_matches_contract": inventory_matches_contract(
            contract,
            manifest,
            candidate,
        ),
        "artifact_integrity_matches_manifest": (
            artifact_integrity_matches_manifest(manifest, candidate)
        ),
        "promoted_claims_agree": promoted_claims_agree(
            contract,
            manifest,
            candidate,
        ),
        "source_lock_matches_contract": source_lock_matches_contract(
            contract,
            source_lock,
        ),
        "decision_matches_candidate": decision_matches_candidate(
            contract,
            decision,
        ),
        "required_review_roles_approved": required_review_roles_approved(
            contract,
            decision,
        ),
        "consumer_contract_is_bounded": consumer_contract_is_bounded(
            contract
        ),
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    actual_decision = "ACCEPT" if not failed_checks else "BLOCK"
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
    }
    evidence_path = case_dir / "assessment.json"
    write_json(evidence_path, assessment)
    assessment["evidence"] = evidence_path.relative_to(output_root).as_posix()
    return assessment


def run_audit(args: argparse.Namespace) -> dict[str, object]:
    if args.workspace.exists():
        shutil.rmtree(args.workspace)
    args.workspace.mkdir(parents=True)

    findings = []
    for case in CASES:
        case_dir = prepare_case(
            case,
            specimen=args.specimen,
            source_publish=args.publish,
            workspace=args.workspace,
        )
        findings.append(
            assess_case(
                case,
                case_dir,
                args.lock_file,
                args.output.parent,
            )
        )

    return {
        "audit": "promotion_integrity",
        "decision_rule": (
            "Accept promotion only when immutable identity, exact inventory, "
            "artifact integrity, promoted claims, source provenance, approval, "
            "and the consumer boundary all agree."
        ),
        "findings": findings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--publish", type=Path, required=True)
    parser.add_argument("--lock-file", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
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
            raise SystemExit(f"unexpected promotion audit decisions: {names}")


if __name__ == "__main__":
    main()
