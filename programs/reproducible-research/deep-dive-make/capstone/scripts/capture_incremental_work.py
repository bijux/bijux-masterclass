"""Capture whether one declared input selects exactly the expected rebuild scope."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath

from incremental_policy import read_incremental_policy

SCHEMA = "deep-dive-make-incremental-work-v1"


def snapshot(root: Path, paths: tuple[PurePosixPath, ...]) -> dict[str, int]:
    result: dict[str, int] = {}
    for relative in paths:
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"expected output is missing: {relative}")
        result[relative.as_posix()] = path.stat().st_mtime_ns
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--make", required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    case = read_incremental_policy(arguments.policy)[0]
    all_outputs = case.must_rebuild + case.must_remain
    subprocess.run(
        [arguments.make, "--no-print-directory", "all"], cwd=root, check=True
    )
    before = snapshot(root, all_outputs)
    source = root / case.input_path
    original = source.stat()
    try:
        advanced = max(before.values()) + 2_000_000_000
        os.utime(source, ns=(original.st_atime_ns, advanced))
        run = subprocess.run(
            [arguments.make, "--no-print-directory", "--trace", "all"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        os.utime(source, ns=(original.st_atime_ns, original.st_mtime_ns))
    after = snapshot(root, all_outputs)
    rebuilt = sorted(path for path in before if after[path] != before[path])
    expected = sorted(path.as_posix() for path in case.must_rebuild)
    unexpected = sorted(path for path in rebuilt if path not in expected)
    missing = sorted(path for path in expected if path not in rebuilt)
    report = {
        "schema": SCHEMA,
        "policy_sha256": hashlib.sha256(arguments.policy.read_bytes()).hexdigest(),
        "input": case.input_path.as_posix(),
        "expected_rebuild": expected,
        "observed_rebuild": rebuilt,
        "missing_rebuild": missing,
        "unexpected_rebuild": unexpected,
        "result": "PASS"
        if run.returncode == 0 and not missing and not unexpected
        else "FAIL",
        "trace": run.stdout + run.stderr,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if report["result"] != "PASS":
        print("FAIL: incremental requested-work contract", file=sys.stderr)
        return 1
    print(f"PASS: wrote incremental evidence to {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
