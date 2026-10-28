#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
selected = sys.argv[1:] or [path.name for path in sorted(ROOT.glob("[0-9][0-9]-*"))]
failures: list[tuple[str, str, str, str]] = []
total = 0
outcome_counts: dict[str, int] = {}

COMPILE_PASS = {"compile-pass", "run-pass", "run-fail", "manual-review"}
COMPILE_FAIL = {"compile-fail"}
VALID_OUTCOMES = COMPILE_PASS | COMPILE_FAIL

for name in selected:
    course = ROOT / name
    manifest = course / "compiler-labs" / "manifest.json"
    if not manifest.exists():
        continue
    cases = json.loads(manifest.read_text())["cases"]
    for case in cases:
        total += 1
        case_id = case["id"]
        outcome = case.get("outcome")
        if outcome not in VALID_OUTCOMES:
            failures.append((name, case_id, str(outcome), "unknown outcome category"))
            continue
        outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1

        source = course / case["path"]
        mode = case.get("mode", "rustc")
        with tempfile.TemporaryDirectory(prefix="rust-course-compiler-case-") as temporary:
            temporary_path = Path(temporary)
            environment = os.environ.copy()
            environment["CARGO_TERM_COLOR"] = "never"
            environment["CARGO_TARGET_DIR"] = str(temporary_path / "target")
            if mode == "rustc":
                output = temporary_path / "case"
                command = [
                    "rustc",
                    "--edition=2024",
                    "-Dwarnings",
                    str(source),
                    "-o",
                    str(output),
                ]
            elif mode == "cargo":
                command = [
                    "cargo",
                    "check",
                    "--quiet",
                    "--all-targets",
                    "--manifest-path",
                    str(source / "Cargo.toml"),
                ]
                output = None
            else:
                failures.append((name, case_id, outcome, f"unknown mode {mode!r}"))
                continue

            completed = subprocess.run(
                command,
                text=True,
                capture_output=True,
                env=environment,
            )
            compiled = completed.returncode == 0
            expected_compile = outcome in COMPILE_PASS
            if compiled != expected_compile:
                diagnostic = (completed.stderr or completed.stdout)[-1600:]
                failures.append((name, case_id, outcome, diagnostic))
                continue

            if outcome in {"run-pass", "run-fail"}:
                if mode == "rustc":
                    run_command = [str(output)]
                else:
                    run_command = [
                        "cargo",
                        "run",
                        "--quiet",
                        "--manifest-path",
                        str(source / "Cargo.toml"),
                    ]
                executed = subprocess.run(
                    run_command,
                    text=True,
                    capture_output=True,
                    env=environment,
                )
                run_succeeded = executed.returncode == 0
                expected_run = outcome == "run-pass"
                if run_succeeded != expected_run:
                    diagnostic = (executed.stderr or executed.stdout)[-1600:]
                    failures.append((name, case_id, outcome, diagnostic))

print(f"checked {total} compiler specimens")
for outcome in sorted(outcome_counts):
    print(f"  {outcome}: {outcome_counts[outcome]}")
for course_name, case_id, outcome, diagnostic in failures:
    print("FAIL", course_name, case_id, outcome, diagnostic, sep="\n  ")
raise SystemExit(1 if failures else 0)
