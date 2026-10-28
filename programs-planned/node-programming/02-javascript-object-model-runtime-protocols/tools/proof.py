#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

COURSE = Path(__file__).resolve().parents[1]


def capture(command: list[str]) -> str | None:
    requested = command[0]
    executable = requested if Path(requested).is_file() else shutil.which(requested)
    if executable is None:
        return None
    result = subprocess.run(
        [executable, *command[1:]],
        cwd=COURSE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def normalized_version(text: str | None) -> str | None:
    if text is None:
        return None
    match = re.search(r"(?:Version\s+|v)?(\d+\.\d+\.\d+)", text)
    return match.group(1) if match else None


def expected_versions() -> dict[str, str]:
    package = json.loads((COURSE / "package.json").read_text(encoding="utf-8"))
    return {
        "node": (COURSE / ".nvmrc").read_text(encoding="utf-8").strip().lstrip("v"),
        "npm": package["packageManager"].split("@", 1)[1],
        "typescript": package["devDependencies"]["typescript"],
    }


def observed_versions() -> dict[str, str | None]:
    local_tsc = COURSE / "node_modules" / ".bin" / "tsc"
    tsc_command = str(local_tsc) if local_tsc.exists() else "tsc"
    return {
        "node": normalized_version(capture(["node", "--version"])),
        "npm": normalized_version(capture(["npm", "--version"])),
        "typescript": normalized_version(capture([tsc_command, "--version"])),
    }


def run_step(label: str, command: list[str]) -> None:
    print(f"\n== {label} ==", flush=True)
    result = subprocess.run(command, cwd=COURSE, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def check_toolchain(strict: bool) -> list[str]:
    expected = expected_versions()
    observed = observed_versions()
    mismatches: list[str] = []

    print("== toolchain ==")
    for tool in ("node", "npm", "typescript"):
        actual = observed[tool] or "unavailable"
        required = expected[tool]
        marker = "OK" if actual == required else "MISMATCH"
        print(f"{tool:10} required={required:10} observed={actual:12} {marker}")
        if actual != required:
            mismatches.append(f"{tool}: required {required}, observed {actual}")

    if strict and mismatches:
        print("\nPinned-baseline proof cannot continue:")
        for mismatch in mismatches:
            print(f"- {mismatch}")
        print("Use `make verify` for an explicitly compatibility-only run.")
        raise SystemExit(2)
    return mismatches


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the course under the pinned baseline or a declared compatibility toolchain."
    )
    parser.add_argument(
        "--compatibility",
        action="store_true",
        help="run all available checks without claiming the pinned Node/TypeScript baseline",
    )
    args = parser.parse_args()
    strict = not args.compatibility

    mismatches = check_toolchain(strict=strict)

    steps = [
        ("course audit", [sys.executable, str(COURSE / "tools/audit.py")]),
        ("link audit", [sys.executable, str(COURSE / "tools/check_links.py")]),
        ("source audit", [sys.executable, str(COURSE / "tools/check_ts_sources.py")]),
        ("investigations", [sys.executable, str(COURSE / "tools/run_investigations.py")]),
        ("package build and tests", [sys.executable, str(COURSE / "tools/run_packages.py"), "test", "--jobs", "8"]),
    ]
    for label, command in steps:
        run_step(label, command)

    mkdocs = shutil.which("mkdocs")
    if mkdocs is None:
        print("\n== documentation ==")
        print("UNAVAILABLE: mkdocs is not installed")
        if strict:
            raise SystemExit(2)
    else:
        run_step(
            "documentation",
            [mkdocs, "build", "--strict", "-f", str(COURSE / "mkdocs.yml")],
        )

    if args.compatibility:
        print("\nCompatibility verification passed for every available check.")
        if mismatches:
            print("This result does not establish the pinned release baseline:")
            for mismatch in mismatches:
                print(f"- {mismatch}")
        if mkdocs is None:
            print("- documentation rendering was unavailable")
    else:
        print("\nPinned-baseline proof passed.")


if __name__ == "__main__":
    main()
