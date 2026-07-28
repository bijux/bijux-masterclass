from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RecoveryCase:
    name: str
    expected_decision: str


CASES = (
    RecoveryCase("complete-migration", "ACCEPT"),
    RecoveryCase("current-only-copy", "BLOCK"),
    RecoveryCase("release-only-copy", "BLOCK"),
    RecoveryCase("stale-release-claim", "BLOCK"),
    RecoveryCase("mutating-recovery-route", "BLOCK"),
    RecoveryCase("missing-time-objective", "BLOCK"),
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
        "stderr": completed.stderr,
        "stdout": completed.stdout,
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


def configure_contract(case: RecoveryCase, author: Path) -> None:
    contract_path = author / "recovery-contract.json"
    contract = read_json(contract_path)

    if case.name == "stale-release-claim":
        revisions = contract["protected_revisions"]
        assert isinstance(revisions, list)
        revisions[0]["expected_sha256"] = "0" * 64
    elif case.name == "mutating-recovery-route":
        route = contract["recovery_route"]
        assert isinstance(route, list)
        route.insert(1, "dvc push --remote candidate")
    elif case.name == "missing-time-objective":
        contract.pop("recovery_time_objective_seconds", None)

    write_json(contract_path, contract)


def prepare_history(
    case: RecoveryCase,
    *,
    specimen: Path,
    case_root: Path,
    dvc: Path,
) -> tuple[Path, dict[str, object]]:
    author = case_root / "author"
    legacy_remote = case_root / "legacy-remote"
    candidate_remote = case_root / "candidate-remote"
    shutil.copytree(specimen, author)
    legacy_remote.mkdir(parents=True)
    candidate_remote.mkdir(parents=True)
    configure_contract(case, author)

    receipts: dict[str, object] = {}
    commands = (
        ("git_init", ["git", "init", "--initial-branch=main"]),
        ("git_name", ["git", "config", "user.name", "bijux"]),
        (
            "git_email",
            ["git", "config", "user.email", "bijux@example.invalid"],
        ),
        ("dvc_init", [str(dvc), "init"]),
        (
            "legacy_remote",
            [
                str(dvc),
                "remote",
                "add",
                "legacy",
                str(legacy_remote),
            ],
        ),
        (
            "candidate_remote",
            [
                str(dvc),
                "remote",
                "add",
                "candidate",
                str(candidate_remote),
            ],
        ),
        (
            "default_remote",
            [str(dvc), "remote", "default", "legacy"],
        ),
        (
            "track_release",
            [str(dvc), "add", "data/observations.csv"],
        ),
        ("git_add_release", ["git", "add", "."]),
        (
            "git_commit_release",
            ["git", "commit", "-m", "record published observations"],
        ),
        ("git_tag_release", ["git", "tag", "release-2025-q1"]),
    )
    for name, command in commands:
        record_command(receipts, name, command, cwd=author)

    observations = author / "data" / "observations.csv"
    observations.write_text(
        observations.read_text(encoding="utf-8") + "OBS-104,27\n",
        encoding="utf-8",
    )
    for name, command in (
        (
            "track_main",
            [str(dvc), "add", "data/observations.csv"],
        ),
        (
            "git_add_main",
            ["git", "add", "data/observations.csv.dvc"],
        ),
        (
            "git_commit_main",
            ["git", "commit", "-m", "record current observations"],
        ),
        (
            "seed_legacy_remote",
            [str(dvc), "push", "--all-commits", "--remote", "legacy"],
        ),
    ):
        record_command(receipts, name, command, cwd=author)

    if case.name == "current-only-copy":
        migration_command = [
            str(dvc),
            "push",
            "--remote",
            "candidate",
        ]
        record_command(
            receipts,
            "migrate_current_only",
            migration_command,
            cwd=author,
        )
    elif case.name == "release-only-copy":
        record_command(
            receipts,
            "select_release",
            ["git", "checkout", "release-2025-q1"],
            cwd=author,
        )
        record_command(
            receipts,
            "restore_release",
            [str(dvc), "checkout", "data/observations.csv.dvc"],
            cwd=author,
        )
        record_command(
            receipts,
            "migrate_release_only",
            [
                str(dvc),
                "push",
                "--remote",
                "candidate",
                "data/observations.csv.dvc",
            ],
            cwd=author,
        )
        record_command(
            receipts,
            "return_to_main",
            ["git", "checkout", "main"],
            cwd=author,
        )
    else:
        record_command(
            receipts,
            "migrate_protected_history",
            [
                str(dvc),
                "push",
                "--all-commits",
                "--remote",
                "candidate",
            ],
            cwd=author,
        )

    return author, receipts


def route_is_read_only(contract: dict[str, Any]) -> bool:
    route = contract.get("recovery_route")
    if not isinstance(route, list) or not route:
        return False
    mutating_prefixes = (
        "dvc push",
        "dvc gc",
        "dvc remote add",
        "dvc remote modify",
        "dvc remote remove",
    )
    return not any(
        str(command).startswith(mutating_prefixes) for command in route
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_count(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def restore_revision(
    *,
    author: Path,
    case_root: Path,
    revision: dict[str, Any],
    dvc: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    revision_name = str(revision.get("revision", ""))
    reviewer = case_root / f"reviewer-{revision_name}"
    receipts: dict[str, object] = {}

    clone = record_command(
        receipts,
        "clone",
        ["git", "clone", "--no-local", str(author), str(reviewer)],
        cwd=case_root,
        check=False,
    )
    checkout = record_command(
        receipts,
        "checkout_revision",
        ["git", "checkout", revision_name],
        cwd=reviewer,
        check=False,
    )

    cache = reviewer / ".dvc" / "cache"
    artifact = reviewer / "data" / "observations.csv"
    shutil.rmtree(cache, ignore_errors=True)
    artifact.unlink(missing_ok=True)

    started = time.monotonic()
    pull = record_command(
        receipts,
        "cache_empty_pull",
        [
            str(dvc),
            "pull",
            "--remote",
            "candidate",
            "data/observations.csv.dvc",
        ],
        cwd=reviewer,
        check=False,
    )
    duration_seconds = time.monotonic() - started

    restored = artifact.exists() and pull.returncode == 0
    actual_sha256 = file_sha256(artifact) if restored else None
    actual_row_count = row_count(artifact) if restored else None
    evidence = {
        "revision": revision_name,
        "revision_resolved": (
            clone.returncode == 0 and checkout.returncode == 0
        ),
        "restored": restored,
        "expected_sha256": revision.get("expected_sha256"),
        "actual_sha256": actual_sha256,
        "expected_row_count": revision.get("expected_row_count"),
        "actual_row_count": actual_row_count,
        "content_claim_matches": (
            restored
            and actual_sha256 == revision.get("expected_sha256")
            and actual_row_count == revision.get("expected_row_count")
        ),
        "duration_seconds": round(duration_seconds, 6),
    }
    return evidence, receipts


def audit_case(
    case: RecoveryCase,
    *,
    specimen: Path,
    workspace: Path,
    dvc: Path,
) -> dict[str, object]:
    case_root = workspace / case.name
    author, author_receipts = prepare_history(
        case,
        specimen=specimen,
        case_root=case_root,
        dvc=dvc,
    )
    contract = read_json(author / "recovery-contract.json")
    protected = contract.get("protected_revisions")
    protected_revisions = protected if isinstance(protected, list) else []
    objective = contract.get("recovery_time_objective_seconds")
    objective_seconds = (
        float(objective)
        if isinstance(objective, (int, float)) and objective > 0
        else None
    )

    revision_evidence: list[dict[str, object]] = []
    reviewer_receipts: dict[str, object] = {}
    for revision in protected_revisions:
        evidence, receipts = restore_revision(
            author=author,
            case_root=case_root,
            revision=revision,
            dvc=dvc,
        )
        revision_evidence.append(evidence)
        reviewer_receipts[str(evidence["revision"])] = receipts

    checks = {
        "time_objective_declared": objective_seconds is not None,
        "recovery_route_is_read_only": route_is_read_only(contract),
        "multiple_protected_revisions_named": len(protected_revisions) >= 2,
        "all_protected_revisions_resolved": (
            bool(revision_evidence)
            and all(item["revision_resolved"] for item in revision_evidence)
        ),
        "all_protected_revisions_restored": (
            bool(revision_evidence)
            and all(item["restored"] for item in revision_evidence)
        ),
        "all_content_claims_match": (
            bool(revision_evidence)
            and all(
                item["content_claim_matches"] for item in revision_evidence
            )
        ),
        "all_restores_within_objective": (
            objective_seconds is not None
            and bool(revision_evidence)
            and all(
                float(item["duration_seconds"]) <= objective_seconds
                for item in revision_evidence
            )
        ),
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    decision = "ACCEPT" if not failed_checks else "BLOCK"
    result = "PASS" if decision == case.expected_decision else "FAIL"

    write_json(
        case_root / "receipts.json",
        {
            "author": author_receipts,
            "reviewers": reviewer_receipts,
        },
    )
    write_json(case_root / "revision-evidence.json", revision_evidence)

    return {
        "finding": case.name.replace("-", "_").upper(),
        "expected_decision": case.expected_decision,
        "decision": decision,
        "result": result,
        "checks": checks,
        "failed_checks": failed_checks,
        "revision_evidence": revision_evidence,
        "evidence": {
            "receipts": str(
                (case_root / "receipts.json").relative_to(workspace)
            ),
            "revision_evidence": str(
                (case_root / "revision-evidence.json").relative_to(workspace)
            ),
        },
    }


def write_summary(path: Path, findings: list[dict[str, object]]) -> None:
    lines = [
        "finding\texpected\tdecision\tresult\tfailed_checks",
        *(
            "\t".join(
                (
                    str(item["finding"]),
                    str(item["expected_decision"]),
                    str(item["decision"]),
                    str(item["result"]),
                    ",".join(str(value) for value in item["failed_checks"]),
                )
            )
            for item in findings
        ),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit protected revision recovery during remote migration.",
    )
    parser.add_argument("--specimen", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dvc", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    specimen = args.specimen.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    dvc = args.dvc.resolve()

    shutil.rmtree(workspace, ignore_errors=True)
    workspace.mkdir(parents=True)
    findings = [
        audit_case(
            case,
            specimen=specimen,
            workspace=workspace,
            dvc=dvc,
        )
        for case in CASES
    ]
    report = {
        "audit": "protected_revision_recovery",
        "decision_rule": (
            "Accept cutover only when every protected revision is restored "
            "from an empty cache, matches its content claim, uses a "
            "read-only route, and meets the declared time objective."
        ),
        "findings": findings,
    }
    write_json(output, report)
    write_summary(output.with_name("summary.tsv"), findings)

    failures = [item for item in findings if item["result"] != "PASS"]
    if args.check and failures:
        for item in failures:
            print(
                f"{item['finding']}: expected "
                f"{item['expected_decision']}, got {item['decision']}",
                file=sys.stderr,
            )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
