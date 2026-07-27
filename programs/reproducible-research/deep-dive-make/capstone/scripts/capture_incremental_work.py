"""Capture whether declared inputs select exactly their expected rebuild scopes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath

from incremental_policy import IncrementalCase, read_incremental_policy

SCHEMA = "deep-dive-make-incremental-work-v2"


def snapshot(root: Path, paths: tuple[PurePosixPath, ...]) -> dict[str, int]:
    result: dict[str, int] = {}
    for relative in paths:
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"expected output is missing: {relative}")
        result[relative.as_posix()] = path.stat().st_mtime_ns
    return result


def capture_case(
    root: Path, case: IncrementalCase, make_command: str
) -> dict[str, object]:
    subprocess.run(
        [make_command, "--no-print-directory", "all"], cwd=root, check=True
    )
    outputs = tuple(sorted(case.governed_outputs))
    before = snapshot(root, outputs)
    source = root / case.input_path
    original = source.stat()
    try:
        advanced = max(before.values()) + 2_000_000_000
        os.utime(source, ns=(original.st_atime_ns, advanced))
        run = subprocess.run(
            [make_command, "--no-print-directory", "--trace", "all"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        os.utime(source, ns=(original.st_atime_ns, original.st_mtime_ns))
    after = snapshot(root, outputs)
    rebuilt = sorted(path for path in before if after[path] != before[path])
    expected = sorted(path.as_posix() for path in case.must_rebuild)
    unexpected = sorted(path for path in rebuilt if path not in expected)
    missing = sorted(path for path in expected if path not in rebuilt)
    return {
        "expected_rebuild": expected,
        "input": case.input_path.as_posix(),
        "missing_rebuild": missing,
        "observed_rebuild": rebuilt,
        "result": "PASS"
        if run.returncode == 0 and not missing and not unexpected
        else "FAIL",
        "trace": run.stdout + run.stderr,
        "unexpected_rebuild": unexpected,
    }


def write_summary(cases: list[dict[str, object]], output: Path) -> None:
    lines = [
        "input\tresult\texpected_rebuild\tobserved_rebuild\tmissing\tunexpected"
    ]
    for case in cases:
        fields = [str(case["input"]), str(case["result"])]
        for key in (
            "expected_rebuild",
            "observed_rebuild",
            "missing_rebuild",
            "unexpected_rebuild",
        ):
            values = case[key]
            assert isinstance(values, list)
            fields.append(",".join(str(value) for value in values) or "-")
        lines.append("\t".join(fields))
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--make", required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    cases = [
        capture_case(root, case, arguments.make)
        for case in read_incremental_policy(arguments.policy)
    ]
    report = {
        "cases": cases,
        "policy_sha256": hashlib.sha256(arguments.policy.read_bytes()).hexdigest(),
        "result": "PASS"
        if all(case["result"] == "PASS" for case in cases)
        else "FAIL",
        "schema": SCHEMA,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    write_summary(cases, arguments.output.with_name("incremental-summary.tsv"))
    if report["result"] != "PASS":
        failed = ", ".join(
            str(case["input"]) for case in cases if case["result"] != "PASS"
        )
        print(f"FAIL: incremental requested-work contract: {failed}", file=sys.stderr)
        return 1
    print(f"PASS: wrote incremental evidence to {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
