"""Compare compatible performance evidence without weakening semantic checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from collect_performance_evidence import SCHEMA

COMPARISON_SCHEMA = "deep-dive-make-performance-comparison-v1"
MATCHING_CONTEXT_KEYS = ("compiler", "make", "platform", "python", "runner")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def read_evidence(path: Path) -> dict[str, object]:
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read evidence {path}: {error}") from error
    if evidence.get("schema") != SCHEMA:
        raise ValueError(f"unsupported evidence schema in {path}")
    if evidence.get("result") != "PASS":
        raise ValueError(f"evidence did not pass: {path}")
    return evidence


def require_equal(
    baseline: dict[str, object],
    candidate: dict[str, object],
    key: str,
) -> None:
    if baseline.get(key) != candidate.get(key):
        raise ValueError(f"{key} mismatch")


def compare_context(
    baseline: dict[str, object], candidate: dict[str, object]
) -> dict[str, object]:
    for key in MATCHING_CONTEXT_KEYS:
        require_equal(baseline, candidate, key)
    baseline_repository = baseline.get("repository")
    candidate_repository = candidate.get("repository")
    if not isinstance(baseline_repository, dict) or not isinstance(
        candidate_repository, dict
    ):
        raise TypeError("repository context is missing")
    for label, repository in (
        ("baseline", baseline_repository),
        ("candidate", candidate_repository),
    ):
        if repository.get("revision") in (None, "unavailable"):
            raise ValueError(f"{label} revision is unavailable")
        if repository.get("status") != "clean":
            raise ValueError(f"{label} worktree is not clean")
    return {
        "baseline_revision": baseline_repository["revision"],
        "candidate_revision": candidate_repository["revision"],
        "compiler": baseline["compiler"],
        "make": baseline["make"],
        "platform": baseline["platform"],
        "python": baseline["python"],
        "runner": baseline["runner"],
    }


def compare_incremental_work(
    baseline: dict[str, object], candidate: dict[str, object]
) -> dict[str, object]:
    for key in (
        "schema",
        "policy_sha256",
        "input",
        "expected_rebuild",
        "observed_rebuild",
        "missing_rebuild",
        "unexpected_rebuild",
        "result",
    ):
        require_equal(baseline, candidate, key)
    if baseline.get("result") != "PASS":
        raise ValueError("incremental work did not pass")
    if baseline.get("missing_rebuild") or baseline.get("unexpected_rebuild"):
        raise ValueError("incremental work contains rebuild drift")
    return {
        "expected_rebuild": baseline["expected_rebuild"],
        "input": baseline["input"],
        "observed_rebuild": baseline["observed_rebuild"],
        "result": "PASS",
    }


def compare_scenario(
    name: str,
    baseline: dict[str, object],
    candidate: dict[str, object],
) -> dict[str, object]:
    for key in ("state", "jobs", "route", "convergence"):
        require_equal(baseline, candidate, key)
    if baseline["inventory"] != candidate["inventory"]:
        raise ValueError(f"{name} trusted-output inventory mismatch")

    baseline_summary = baseline["summary"]
    candidate_summary = candidate["summary"]
    assert isinstance(baseline_summary, dict)
    assert isinstance(candidate_summary, dict)
    baseline_median = float(baseline_summary["median_seconds"])
    candidate_median = float(candidate_summary["median_seconds"])
    delta = candidate_median - baseline_median
    percent = None
    if baseline_median != 0:
        percent = round((delta / baseline_median) * 100, 3)

    return {
        "baseline_median_seconds": baseline_median,
        "candidate_median_seconds": candidate_median,
        "convergence": "PASS",
        "delta_percent": percent,
        "delta_seconds": round(delta, 9),
        "trusted_outputs": "MATCH",
    }


def compare(
    baseline: dict[str, object], candidate: dict[str, object]
) -> dict[str, object]:
    require_equal(baseline, candidate, "policy_sha256")
    require_equal(baseline, candidate, "sample_count")
    baseline_context = baseline.get("context")
    candidate_context = candidate.get("context")
    if not isinstance(baseline_context, dict) or not isinstance(
        candidate_context, dict
    ):
        raise TypeError("execution context is missing")
    context = compare_context(baseline_context, candidate_context)
    baseline_incremental = baseline.get("incremental_work")
    candidate_incremental = candidate.get("incremental_work")
    if not isinstance(baseline_incremental, dict) or not isinstance(
        candidate_incremental, dict
    ):
        raise TypeError("incremental work evidence is missing")
    incremental_work = compare_incremental_work(
        baseline_incremental, candidate_incremental
    )
    baseline_scenarios = baseline["scenarios"]
    candidate_scenarios = candidate["scenarios"]
    assert isinstance(baseline_scenarios, dict)
    assert isinstance(candidate_scenarios, dict)
    if set(baseline_scenarios) != set(candidate_scenarios):
        raise ValueError("scenario set mismatch")

    comparisons: dict[str, object] = {}
    for name in sorted(baseline_scenarios):
        baseline_scenario = baseline_scenarios[name]
        candidate_scenario = candidate_scenarios[name]
        assert isinstance(baseline_scenario, dict)
        assert isinstance(candidate_scenario, dict)
        comparisons[name] = compare_scenario(
            name, baseline_scenario, candidate_scenario
        )

    return {
        "decision": (
            "Comparable timing deltas recorded. Interpret them against observed spread "
            "and an explicit operational objective before claiming an improvement."
        ),
        "execution_context": context,
        "incremental_work": incremental_work,
        "result": "PASS",
        "scenarios": comparisons,
        "schema": COMPARISON_SCHEMA,
        "semantic_equivalence": "PASS",
    }


def main() -> int:
    arguments = parse_arguments()
    output = arguments.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        report = compare(
            read_evidence(arguments.baseline),
            read_evidence(arguments.candidate),
        )
    except (KeyError, TypeError, ValueError) as error:
        report = {
            "failure": str(error),
            "result": "FAIL",
            "schema": COMPARISON_SCHEMA,
        }
        output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"PASS: wrote performance comparison to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
