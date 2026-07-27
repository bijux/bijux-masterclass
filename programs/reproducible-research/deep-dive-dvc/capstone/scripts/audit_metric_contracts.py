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


PRIMARY_VALUE_PATH = (
    "metrics.positive_class_f1_at_fixed_threshold.value"
)


@dataclass(frozen=True)
class ComparisonCase:
    name: str
    source: str
    expected_decision: str
    threshold: float = 0.65


CASES = (
    ComparisonCase(
        "comparable-candidate",
        "comparable-candidate.json",
        "ACCEPT",
    ),
    ComparisonCase(
        "additive-metric",
        "additive-metric.json",
        "ACCEPT",
    ),
    ComparisonCase(
        "population-drift",
        "population-drift.json",
        "REJECT",
    ),
    ComparisonCase(
        "unit-drift",
        "unit-drift.json",
        "REJECT",
    ),
    ComparisonCase(
        "control-drift",
        "comparable-candidate.json",
        "REJECT",
        threshold=0.50,
    ),
    ComparisonCase(
        "schema-version-drift",
        "schema-version-drift.json",
        "REJECT",
    ),
    ComparisonCase(
        "missing-population-identity",
        "missing-population-identity.json",
        "REJECT",
    ),
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def nested(document: dict[str, Any], *keys: str) -> Any:
    value: Any = document
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


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


def receipt(
    completed: subprocess.CompletedProcess[str],
    *,
    command: list[str],
) -> dict[str, object]:
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def primary_value(document: dict[str, Any]) -> float | None:
    metric_name = nested(
        document,
        "comparison_contract",
        "primary_metric",
        "name",
    )
    value = nested(document, "metrics", str(metric_name), "value")
    return float(value) if isinstance(value, int | float) else None


def compare_contracts(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    dvc_diff: dict[str, Any],
) -> dict[str, object]:
    baseline_contract = nested(baseline, "comparison_contract")
    candidate_contract = nested(candidate, "comparison_contract")
    baseline_metrics = nested(baseline, "metrics")
    candidate_metrics = nested(candidate, "metrics")
    baseline_value = primary_value(baseline)
    candidate_value = primary_value(candidate)

    checks = {
        "comparison_contract_present": isinstance(candidate_contract, dict),
        "schema_version_same": nested(
            baseline, "comparison_contract", "schema_version"
        )
        == nested(candidate, "comparison_contract", "schema_version"),
        "population_identity_present": nested(
            candidate,
            "comparison_contract",
            "population",
            "identity",
        )
        is not None,
        "population_identity_same": nested(
            baseline,
            "comparison_contract",
            "population",
            "identity",
        )
        == nested(
            candidate,
            "comparison_contract",
            "population",
            "identity",
        ),
        "population_rows_same": nested(
            baseline,
            "comparison_contract",
            "population",
            "rows",
        )
        == nested(
            candidate,
            "comparison_contract",
            "population",
            "rows",
        ),
        "decision_threshold_same": nested(
            baseline,
            "comparison_contract",
            "controls",
            "decision_threshold",
        )
        == nested(
            candidate,
            "comparison_contract",
            "controls",
            "decision_threshold",
        ),
        "metric_name_same": nested(
            baseline,
            "comparison_contract",
            "primary_metric",
            "name",
        )
        == nested(
            candidate,
            "comparison_contract",
            "primary_metric",
            "name",
        ),
        "metric_definition_same": nested(
            baseline,
            "comparison_contract",
            "primary_metric",
            "definition",
        )
        == nested(
            candidate,
            "comparison_contract",
            "primary_metric",
            "definition",
        ),
        "metric_unit_same": nested(
            baseline,
            "comparison_contract",
            "primary_metric",
            "unit",
        )
        == nested(
            candidate,
            "comparison_contract",
            "primary_metric",
            "unit",
        ),
        "aggregation_same": nested(
            baseline,
            "comparison_contract",
            "primary_metric",
            "aggregation",
        )
        == nested(
            candidate,
            "comparison_contract",
            "primary_metric",
            "aggregation",
        ),
        "primary_value_present": baseline_value is not None
        and candidate_value is not None,
        "dvc_reports_primary_value_change": nested(
            dvc_diff,
            "metrics/metrics.json",
            PRIMARY_VALUE_PATH,
            "diff",
        )
        is not None,
    }
    semantic_checks = [
        value
        for key, value in checks.items()
        if key != "dvc_reports_primary_value_change"
    ]
    compatible = all(semantic_checks)

    assert isinstance(baseline_contract, dict)
    assert isinstance(candidate_contract, dict)
    assert isinstance(baseline_metrics, dict)
    assert isinstance(candidate_metrics, dict)
    added_metrics = sorted(set(candidate_metrics) - set(baseline_metrics))
    removed_metrics = sorted(set(baseline_metrics) - set(candidate_metrics))

    return {
        "decision": "ACCEPT" if compatible else "REJECT",
        "checks": checks,
        "values": {
            "baseline": baseline_value,
            "candidate": candidate_value,
            "delta": (
                round(candidate_value - baseline_value, 4)
                if baseline_value is not None and candidate_value is not None
                else None
            ),
        },
        "metric_keys": {
            "added": added_metrics,
            "removed": removed_metrics,
        },
    }


def prepare_baseline(
    *,
    specimen: Path,
    workspace: Path,
    dvc: Path,
) -> tuple[dict[str, Any], dict[str, object]]:
    shutil.copytree(specimen, workspace)
    commands = (
        ["git", "init", "--initial-branch=main"],
        ["git", "config", "user.name", "bijux"],
        ["git", "config", "user.email", "bijux@example.invalid"],
        [str(dvc), "init"],
        [str(dvc), "repro"],
        ["git", "add", "."],
        ["git", "commit", "-m", "record baseline metric contract"],
    )
    receipts: dict[str, object] = {}
    for index, command in enumerate(commands):
        completed = run(command, cwd=workspace)
        receipts[f"baseline_command_{index + 1}"] = receipt(
            completed,
            command=command,
        )

    status_command = [str(dvc), "status"]
    status = run(status_command, cwd=workspace)
    receipts["baseline_status"] = receipt(status, command=status_command)
    return read_json(workspace / "metrics" / "metrics.json"), receipts


def run_case(
    case: ComparisonCase,
    *,
    specimen: Path,
    workspace_root: Path,
    dvc: Path,
) -> dict[str, object]:
    workspace = workspace_root / case.name
    baseline, baseline_receipts = prepare_baseline(
        specimen=specimen,
        workspace=workspace,
        dvc=dvc,
    )
    shutil.copyfile(
        workspace / "cases" / case.source,
        workspace / "cases" / "selected.json",
    )
    params_path = workspace / "params.yaml"
    params = read_json(params_path)
    decision = params["decision"]
    assert isinstance(decision, dict)
    decision["threshold"] = case.threshold
    write_json(params_path, params)

    status_command = [str(dvc), "status"]
    status = run(status_command, cwd=workspace)
    repro_command = [str(dvc), "repro"]
    repro = run(repro_command, cwd=workspace)
    diff_command = [str(dvc), "metrics", "diff", "--json"]
    diff = run(diff_command, cwd=workspace)
    dvc_diff = json.loads(diff.stdout)
    candidate = read_json(workspace / "metrics" / "metrics.json")
    comparison = compare_contracts(baseline, candidate, dvc_diff)

    evidence_dir = workspace / "evidence"
    write_json(evidence_dir / "baseline-metrics.json", baseline)
    write_json(evidence_dir / "candidate-metrics.json", candidate)
    write_json(evidence_dir / "dvc-metrics-diff.json", dvc_diff)
    write_json(evidence_dir / "comparison.json", comparison)
    (evidence_dir / "dvc-status.txt").write_text(
        status.stdout + status.stderr,
        encoding="utf-8",
    )
    (evidence_dir / "dvc-repro.txt").write_text(
        repro.stdout + repro.stderr,
        encoding="utf-8",
    )

    actual_decision = comparison["decision"]
    checks = comparison["checks"]
    assert isinstance(checks, dict)
    passed = (
        actual_decision == case.expected_decision
        and checks["dvc_reports_primary_value_change"] is True
        and "evaluate_metric_contract" in status.stdout
        and "evaluate_metric_contract" in repro.stdout
    )
    finding = {
        "finding": case.name.upper().replace("-", "_"),
        "result": "PASS" if passed else "FAIL",
        "decision": actual_decision,
        "expected_decision": case.expected_decision,
        "checks": checks,
        "values": comparison["values"],
        "metric_keys": comparison["metric_keys"],
        "evidence": {
            "workspace": str(workspace),
            "baseline_metrics": str(evidence_dir / "baseline-metrics.json"),
            "candidate_metrics": str(evidence_dir / "candidate-metrics.json"),
            "dvc_status": str(evidence_dir / "dvc-status.txt"),
            "dvc_repro": str(evidence_dir / "dvc-repro.txt"),
            "dvc_metrics_diff": str(evidence_dir / "dvc-metrics-diff.json"),
            "comparison": str(evidence_dir / "comparison.json"),
        },
    }
    return {
        "finding": finding,
        "baseline": baseline,
        "baseline_receipts": baseline_receipts,
        "dvc_receipts": {
            "status": receipt(status, command=status_command),
            "repro": receipt(repro, command=repro_command),
            "metrics_diff": receipt(diff, command=diff_command),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dvc", type=Path)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    specimen = args.specimen.resolve()
    workspace_root = args.workspace.resolve()
    output = args.output.resolve()
    dvc = (
        args.dvc.resolve()
        if args.dvc
        else Path(sys.executable).with_name("dvc")
    )

    if workspace_root.exists():
        shutil.rmtree(workspace_root)
    workspace_root.mkdir(parents=True)

    case_reports = [
        run_case(
            case,
            specimen=specimen,
            workspace_root=workspace_root,
            dvc=dvc,
        )
        for case in CASES
    ]
    findings = [report["finding"] for report in case_reports]
    first_baseline = case_reports[0]["baseline"]
    baseline_value = primary_value(first_baseline)
    baseline_finding = {
        "finding": "BASELINE_METRIC_CONTRACT_CONVERGES",
        "result": "PASS" if baseline_value == 0.7368 else "FAIL",
        "decision": "ACCEPT",
        "checks": {
            "primary_value_is_expected": baseline_value == 0.7368,
            "population_identity_is_present": nested(
                first_baseline,
                "comparison_contract",
                "population",
                "identity",
            )
            is not None,
            "decision_threshold_is_declared": nested(
                first_baseline,
                "comparison_contract",
                "controls",
                "decision_threshold",
            )
            == 0.65,
        },
    }
    report = {
        "specimen": str(specimen),
        "workspace": str(workspace_root),
        "findings": [baseline_finding, *findings],
        "cases": case_reports,
    }
    write_json(output, report)

    failed = [
        finding
        for finding in report["findings"]
        if finding["result"] != "PASS"
    ]
    if args.check and failed:
        print(
            "FAIL: metric contract audit findings did not match expectations",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(f"PASS: audited metric contracts in {output}")


if __name__ == "__main__":
    main()
