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
class HandoffCase:
    name: str
    expected_decision: str


CASES = (
    HandoffCase("complete-handoff", "ACCEPT"),
    HandoffCase("missing-remote-object", "BLOCK"),
    HandoffCase("undiscoverable-remote", "BLOCK"),
    HandoffCase("untracked-stage-dependency", "BLOCK"),
    HandoffCase("stale-execution-record", "BLOCK"),
    HandoffCase("mutating-review-route", "BLOCK"),
    HandoffCase("missing-result-contract", "BLOCK"),
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


def record_command(
    receipts: dict[str, object],
    name: str,
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = run(command, cwd=cwd, check=check)
    receipts[name] = receipt(completed, command=command)
    return completed


def configure_case_source(case: HandoffCase, author: Path) -> None:
    contract_path = author / "handoff-contract.json"
    contract = read_json(contract_path)

    if case.name == "mutating-review-route":
        route = contract["review_route"]
        assert isinstance(route, list)
        route.insert(1, "dvc push")
        write_json(contract_path, contract)
    elif case.name == "missing-result-contract":
        contract.pop("claim")
        write_json(contract_path, contract)
    elif case.name == "untracked-stage-dependency":
        (author / ".gitignore").write_text(
            "/policy/severity-policy.json\n",
            encoding="utf-8",
        )


def prepare_author(
    case: HandoffCase,
    *,
    specimen: Path,
    case_root: Path,
    dvc: Path,
) -> tuple[Path, Path, dict[str, object]]:
    author = case_root / "author"
    shared_remote = case_root / "shared-dvc-remote"
    shutil.copytree(specimen, author)
    shared_remote.mkdir(parents=True)
    configure_case_source(case, author)

    receipts: dict[str, object] = {}
    commands = (
        ("git_init", ["git", "init", "--initial-branch=main"]),
        ("git_name", ["git", "config", "user.name", "bijux"]),
        (
            "git_email",
            ["git", "config", "user.email", "bijux@example.invalid"],
        ),
        ("dvc_init", [str(dvc), "init"]),
    )
    for name, command in commands:
        record_command(receipts, name, command, cwd=author)

    remote_command = [str(dvc), "remote", "add", "-d", "shared"]
    if case.name == "undiscoverable-remote":
        remote_command.insert(3, "--local")
    remote_command.append(str(shared_remote))
    record_command(
        receipts,
        "configure_remote",
        remote_command,
        cwd=author,
    )
    record_command(
        receipts,
        "track_data",
        [str(dvc), "add", "data/incidents.csv"],
        cwd=author,
    )
    record_command(
        receipts,
        "initial_repro",
        [str(dvc), "repro"],
        cwd=author,
    )
    record_command(
        receipts,
        "git_add",
        ["git", "add", "."],
        cwd=author,
    )
    record_command(
        receipts,
        "git_commit",
        ["git", "commit", "-m", "record reviewer handoff"],
        cwd=author,
    )

    if case.name != "missing-remote-object":
        record_command(
            receipts,
            "initial_push",
            [str(dvc), "push"],
            cwd=author,
        )

    if case.name == "stale-execution-record":
        incidents = author / "data" / "incidents.csv"
        incidents.write_text(
            incidents.read_text(encoding="utf-8") + "INC-105,5,0\n",
            encoding="utf-8",
        )
        record_command(
            receipts,
            "track_changed_data",
            [str(dvc), "add", "data/incidents.csv"],
            cwd=author,
        )
        record_command(
            receipts,
            "push_changed_data",
            [str(dvc), "push", "data/incidents.csv.dvc"],
            cwd=author,
        )
        record_command(
            receipts,
            "git_add_changed_pointer",
            ["git", "add", "data/incidents.csv.dvc"],
            cwd=author,
        )
        record_command(
            receipts,
            "git_commit_changed_pointer",
            ["git", "commit", "-m", "record changed data pointer"],
            cwd=author,
        )

    return author, shared_remote, receipts


def parse_status(completed: subprocess.CompletedProcess[str]) -> object:
    if completed.returncode != 0 or not completed.stdout.strip():
        return None
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None


def route_is_read_only(contract: dict[str, Any]) -> bool:
    route = contract.get("review_route")
    if not isinstance(route, list) or not route:
        return False
    forbidden = ("dvc push", "dvc gc", "dvc remote modify")
    return not any(
        any(str(command).startswith(prefix) for prefix in forbidden)
        for command in route
    )


def result_matches_claim(
    contract: dict[str, Any],
    result_path: Path,
) -> bool:
    claim = contract.get("claim")
    if not isinstance(claim, dict) or not result_path.exists():
        return False
    result = read_json(result_path)
    return claim == result


def audit_reviewer(
    case: HandoffCase,
    *,
    author: Path,
    case_root: Path,
    dvc: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    reviewer = case_root / "reviewer"
    receipts: dict[str, object] = {}
    record_command(
        receipts,
        "clone",
        ["git", "clone", "--no-local", str(author), str(reviewer)],
        cwd=case_root,
    )
    remote_list = record_command(
        receipts,
        "remote_list",
        [str(dvc), "remote", "list"],
        cwd=reviewer,
        check=False,
    )
    pull = record_command(
        receipts,
        "pull",
        [str(dvc), "pull"],
        cwd=reviewer,
        check=False,
    )
    status = record_command(
        receipts,
        "status_before_repro",
        [str(dvc), "status", "--json"],
        cwd=reviewer,
        check=False,
    )
    repro = record_command(
        receipts,
        "repro",
        [str(dvc), "repro"],
        cwd=reviewer,
        check=False,
    )

    contract_path = reviewer / "handoff-contract.json"
    contract = read_json(contract_path)
    parsed_status = parse_status(status)
    checks = {
        "remote_discoverable": (
            remote_list.returncode == 0 and "shared" in remote_list.stdout
        ),
        "pull_succeeded": pull.returncode == 0,
        "recorded_state_clean_before_repro": parsed_status == {},
        "repro_succeeded": repro.returncode == 0,
        "review_route_avoids_remote_mutation": route_is_read_only(contract),
        "result_contract_present": isinstance(contract.get("claim"), dict),
        "result_matches_claim": result_matches_claim(
            contract,
            reviewer / "reports" / "summary.json",
        ),
    }
    decision = "ACCEPT" if all(checks.values()) else "BLOCK"
    passed = decision == case.expected_decision
    finding = {
        "finding": case.name.upper().replace("-", "_"),
        "result": "PASS" if passed else "FAIL",
        "decision": decision,
        "expected_decision": case.expected_decision,
        "checks": checks,
        "failed_checks": [
            name for name, value in checks.items() if value is False
        ],
        "evidence": {
            "reviewer": str(reviewer),
            "contract": str(contract_path),
            "result": str(reviewer / "reports" / "summary.json"),
        },
    }
    return finding, receipts


def write_summary(path: Path, findings: list[dict[str, object]]) -> None:
    rows = ["finding\tresult\tdecision\tfailed_checks"]
    for finding in findings:
        failed_checks = finding["failed_checks"]
        assert isinstance(failed_checks, list)
        rows.append(
            "\t".join(
                [
                    str(finding["finding"]),
                    str(finding["result"]),
                    str(finding["decision"]),
                    ",".join(str(value) for value in failed_checks),
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

    findings: list[dict[str, object]] = []
    case_receipts: dict[str, object] = {}
    for case in CASES:
        case_root = workspace_root / case.name
        case_root.mkdir()
        author, shared_remote, author_receipts = prepare_author(
            case,
            specimen=specimen,
            case_root=case_root,
            dvc=dvc,
        )
        finding, reviewer_receipts = audit_reviewer(
            case,
            author=author,
            case_root=case_root,
            dvc=dvc,
        )
        findings.append(finding)
        case_receipts[case.name] = {
            "shared_remote": str(shared_remote),
            "author": author_receipts,
            "reviewer": reviewer_receipts,
        }
        write_json(case_root / "evidence" / "finding.json", finding)
        write_json(
            case_root / "evidence" / "receipts.json",
            case_receipts[case.name],
        )

    report = {
        "specimen": str(specimen),
        "workspace": str(workspace_root),
        "findings": findings,
        "receipts": case_receipts,
    }
    write_json(output, report)
    write_summary(output.parent / "summary.tsv", findings)

    failed = [item for item in findings if item["result"] != "PASS"]
    if args.check and failed:
        print(
            "FAIL: reviewer handoff evidence did not match expectations",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(f"PASS: audited reviewer handoffs in {output}")


if __name__ == "__main__":
    main()
