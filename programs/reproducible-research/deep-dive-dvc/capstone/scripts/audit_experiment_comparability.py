from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExperimentCase:
    name: str
    expected_decision: str


CASES = (
    ExperimentCase("controlled-threshold", "KEEP_FOR_PROMOTION_REVIEW"),
    ExperimentCase("mixed-control-change", "BLOCK_COMPARISON"),
    ExperimentCase("mutated-baseline-contract", "BLOCK_COMPARISON"),
    ExperimentCase("population-drift", "BLOCK_COMPARISON"),
    ExperimentCase("metric-schema-drift", "BLOCK_COMPARISON"),
    ExperimentCase("missing-candidate-intent", "BLOCK_COMPARISON"),
    ExperimentCase("unsafe-promotion-request", "BLOCK_PROMOTION"),
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["DVC_NO_ANALYTICS"] = "true"
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        check=check,
        text=True,
        capture_output=True,
    )


def record(
    receipts: dict[str, object],
    name: str,
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = run(command, cwd=cwd, check=check)
    receipts[name] = {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    return completed


def flatten(value: dict[str, Any], prefix: str = "") -> dict[str, object]:
    result: dict[str, object] = {}
    for key, item in value.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(item, dict):
            result.update(flatten(item, path))
        else:
            result[path] = item
    return result


def changed_paths(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> list[str]:
    baseline_values = flatten(baseline)
    candidate_values = flatten(candidate)
    keys = set(baseline_values) | set(candidate_values)
    return sorted(
        key
        for key in keys
        if baseline_values.get(key) != candidate_values.get(key)
    )


def configure_candidate(case: ExperimentCase, workspace: Path) -> None:
    params_path = workspace / "params.yaml"
    contract_path = workspace / "experiment-contract.json"
    params = read_json(params_path)
    contract = read_json(contract_path)

    decision = params["decision"]
    assert isinstance(decision, dict)
    decision["threshold"] = 0.5

    if case.name == "mixed-control-change":
        decision["review_capacity"] = 6
    elif case.name == "mutated-baseline-contract":
        baseline = contract["baseline"]
        assert isinstance(baseline, dict)
        baseline["threshold"] = 0.6
    elif case.name == "population-drift":
        data_path = workspace / "data" / "evaluation.csv"
        data_path.write_text(
            data_path.read_text(encoding="utf-8") + "INC-209,0.52,0\n",
            encoding="utf-8",
        )
    elif case.name == "metric-schema-drift":
        evaluation = params["evaluation"]
        assert isinstance(evaluation, dict)
        evaluation["metric_schema"] = "classification-v2"
    elif case.name == "missing-candidate-intent":
        candidate = contract["candidate"]
        assert isinstance(candidate, dict)
        candidate["intent"] = ""
    elif case.name == "unsafe-promotion-request":
        write_json(
            workspace / "promotion-request.json",
            {"candidate": case.name, "promote": True},
        )

    write_json(params_path, params)
    write_json(contract_path, contract)


def baseline_matches_contract(
    contract: dict[str, Any],
    params: dict[str, Any],
    metrics: dict[str, Any],
) -> bool:
    baseline = contract.get("baseline")
    if not isinstance(baseline, dict):
        return False
    decision = params.get("decision")
    evaluation = params.get("evaluation")
    result_metrics = metrics.get("metrics")
    population = metrics.get("population")
    if not all(
        isinstance(value, dict)
        for value in (decision, evaluation, result_metrics, population)
    ):
        return False
    return (
        decision["threshold"] == baseline.get("threshold")
        and evaluation["population_id"] == baseline.get("population_id")
        and evaluation["metric_schema"] == baseline.get("metric_schema")
        and population["id"] == baseline.get("population_id")
        and metrics["metric_schema"] == baseline.get("metric_schema")
        and result_metrics == baseline.get("expected_metrics")
    )


def tradeoff_meets_review_policy(
    contract: dict[str, Any],
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    policy = contract.get("promotion")
    baseline_metrics = baseline.get("metrics")
    candidate_metrics = candidate.get("metrics")
    if not all(
        isinstance(value, dict)
        for value in (policy, baseline_metrics, candidate_metrics)
    ):
        return False
    recall_gain = (
        float(candidate_metrics["recall"]) - float(baseline_metrics["recall"])
    )
    return (
        recall_gain >= float(policy["minimum_recall_gain"])
        and float(candidate_metrics["precision"])
        < float(baseline_metrics["precision"])
        and float(candidate_metrics["precision"])
        >= float(policy["minimum_precision"])
    )


def promotion_decision_is_recorded(workspace: Path) -> bool:
    request_path = workspace / "promotion-request.json"
    if not request_path.exists():
        return True
    decision_path = workspace / "promotion-decision.json"
    if not decision_path.exists():
        return False
    decision = read_json(decision_path)
    return bool(decision.get("decision") and decision.get("evidence"))


def classify(
    case: ExperimentCase,
    *,
    workspace: Path,
    baseline_commit: str,
    baseline_params: dict[str, Any],
    baseline_metrics: dict[str, Any],
    candidate_params: dict[str, Any],
    candidate_metrics: dict[str, Any] | None,
    candidate_run: subprocess.CompletedProcess[str],
    current_commit: str,
) -> dict[str, object]:
    contract = read_json(workspace / "experiment-contract.json")
    candidate_contract = contract.get("candidate")
    assert isinstance(candidate_contract, dict)
    allowed_changes = candidate_contract.get("allowed_changes")
    changed = changed_paths(baseline_params, candidate_params)
    target_threshold = candidate_contract.get("target_threshold")

    checks = {
        "baseline_matches_recorded_contract": baseline_matches_contract(
            contract,
            baseline_params,
            baseline_metrics,
        ),
        "candidate_intent_present": bool(
            str(candidate_contract.get("intent", "")).strip()
        ),
        "changed_controls_are_allowed": (
            isinstance(allowed_changes, list)
            and changed == sorted(str(value) for value in allowed_changes)
        ),
        "candidate_targets_intended_threshold": (
            candidate_params.get("decision", {}).get("threshold")
            == target_threshold
        ),
        "evaluation_population_is_stable": (
            candidate_metrics is not None
            and candidate_metrics.get("population")
            == baseline_metrics.get("population")
        ),
        "metric_schema_is_stable": (
            candidate_metrics is not None
            and candidate_metrics.get("metric_schema")
            == baseline_metrics.get("metric_schema")
        ),
        "candidate_reproduced": (
            candidate_run.returncode == 0 and candidate_metrics is not None
        ),
        "tradeoff_meets_review_policy": (
            candidate_metrics is not None
            and tradeoff_meets_review_policy(
                contract,
                baseline_metrics,
                candidate_metrics,
            )
        ),
        "baseline_git_commit_is_unchanged": baseline_commit == current_commit,
        "promotion_decision_is_recorded": promotion_decision_is_recorded(
            workspace
        ),
    }
    comparison_checks = {
        key: value
        for key, value in checks.items()
        if key != "promotion_decision_is_recorded"
    }
    promotion_requested = (workspace / "promotion-request.json").exists()
    if not all(comparison_checks.values()):
        decision = "BLOCK_COMPARISON"
    elif promotion_requested and not checks["promotion_decision_is_recorded"]:
        decision = "BLOCK_PROMOTION"
    else:
        decision = "KEEP_FOR_PROMOTION_REVIEW"

    passed = decision == case.expected_decision
    return {
        "finding": case.name.upper().replace("-", "_"),
        "result": "PASS" if passed else "FAIL",
        "decision": decision,
        "expected_decision": case.expected_decision,
        "changed_paths": changed,
        "checks": checks,
        "failed_checks": [
            name for name, value in checks.items() if value is False
        ],
        "evidence": {
            "workspace": str(workspace),
            "baseline_metrics": str(
                workspace / "evidence" / "baseline-metrics.json"
            ),
            "candidate_metrics": str(
                workspace / "evidence" / "candidate-metrics.json"
            ),
            "receipts": str(workspace / "evidence" / "receipts.json"),
        },
    }


def audit_case(
    case: ExperimentCase,
    *,
    specimen: Path,
    case_root: Path,
    dvc: Path,
) -> dict[str, object]:
    workspace = case_root / "workspace"
    shutil.copytree(specimen, workspace)
    receipts: dict[str, object] = {}

    setup_commands = (
        ("git_init", ["git", "init", "--initial-branch=main"]),
        ("git_name", ["git", "config", "user.name", "bijux"]),
        (
            "git_email",
            ["git", "config", "user.email", "bijux@example.invalid"],
        ),
        ("dvc_init", [str(dvc), "init"]),
        ("baseline_repro", [str(dvc), "repro"]),
        ("git_add", ["git", "add", "."]),
        (
            "git_commit",
            ["git", "commit", "-m", "record approved experiment baseline"],
        ),
    )
    for name, command in setup_commands:
        record(receipts, name, command, cwd=workspace)

    baseline_commit = record(
        receipts,
        "baseline_commit",
        ["git", "rev-parse", "HEAD"],
        cwd=workspace,
    ).stdout.strip()
    baseline_params = read_json(workspace / "params.yaml")
    baseline_metrics = read_json(workspace / "metrics" / "metrics.json")

    configure_candidate(case, workspace)
    candidate_run = record(
        receipts,
        "candidate_run",
        [str(dvc), "exp", "run"],
        cwd=workspace,
        check=False,
    )
    record(
        receipts,
        "experiment_show",
        [str(dvc), "exp", "show", "--no-pager", "--json"],
        cwd=workspace,
        check=False,
    )
    record(
        receipts,
        "experiment_diff",
        [str(dvc), "exp", "diff", "--json"],
        cwd=workspace,
        check=False,
    )
    current_commit = record(
        receipts,
        "current_commit",
        ["git", "rev-parse", "HEAD"],
        cwd=workspace,
    ).stdout.strip()

    candidate_params = read_json(workspace / "params.yaml")
    candidate_metrics_path = workspace / "metrics" / "metrics.json"
    candidate_metrics = (
        read_json(candidate_metrics_path)
        if candidate_metrics_path.exists()
        else None
    )

    evidence_dir = workspace / "evidence"
    write_json(evidence_dir / "baseline-params.json", baseline_params)
    write_json(evidence_dir / "baseline-metrics.json", baseline_metrics)
    write_json(evidence_dir / "candidate-params.json", candidate_params)
    if candidate_metrics is not None:
        write_json(evidence_dir / "candidate-metrics.json", candidate_metrics)
    write_json(evidence_dir / "receipts.json", receipts)

    finding = classify(
        case,
        workspace=workspace,
        baseline_commit=baseline_commit,
        baseline_params=baseline_params,
        baseline_metrics=baseline_metrics,
        candidate_params=candidate_params,
        candidate_metrics=candidate_metrics,
        candidate_run=candidate_run,
        current_commit=current_commit,
    )
    write_json(case_root / "finding.json", finding)
    return finding


def write_summary(path: Path, findings: list[dict[str, object]]) -> None:
    rows = ["finding\tresult\tdecision\tchanged_paths\tfailed_checks"]
    for finding in findings:
        changed = finding["changed_paths"]
        failed = finding["failed_checks"]
        assert isinstance(changed, list)
        assert isinstance(failed, list)
        rows.append(
            "\t".join(
                [
                    str(finding["finding"]),
                    str(finding["result"]),
                    str(finding["decision"]),
                    ",".join(str(value) for value in changed),
                    ",".join(str(value) for value in failed),
                ]
            )
        )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dvc", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    specimen = args.specimen.resolve()
    workspace_root = args.workspace.resolve()
    output = args.output.resolve()
    dvc = args.dvc.resolve()

    if workspace_root.exists():
        shutil.rmtree(workspace_root)
    workspace_root.mkdir(parents=True)

    findings = [
        audit_case(
            case,
            specimen=specimen,
            case_root=workspace_root / case.name,
            dvc=dvc,
        )
        for case in CASES
    ]
    report = {
        "specimen": str(specimen),
        "workspace": str(workspace_root),
        "findings": findings,
    }
    write_json(output, report)
    write_summary(output.parent / "summary.tsv", findings)

    failed = [item for item in findings if item["result"] != "PASS"]
    if args.check and failed:
        print(
            "FAIL: experiment evidence did not match expected decisions",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(f"PASS: audited experiment comparability in {output}")


if __name__ == "__main__":
    main()
