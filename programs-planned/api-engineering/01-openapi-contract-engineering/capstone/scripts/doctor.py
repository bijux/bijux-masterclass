#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]
CAPSTONE = COURSE / "capstone"
LOCAL_OASDIFF = COURSE / ".tools/bin/oasdiff"


def command_version(command: list[str]) -> str | None:
    if shutil.which(command[0]) is None:
        return None
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = (result.stdout or result.stderr).strip().splitlines()
    return text[0] if text else "available"


def main() -> int:
    failures: list[str] = []
    print("OpenAPI Contract Engineering — environment doctor")
    print(f"course: {COURSE}")
    print(f"python: {platform.python_version()} ({sys.executable})")
    if sys.version_info < (3, 11):
        failures.append("Python 3.11 or newer is required")

    required_commands = {
        "make": ["make", "--version"],
        "node": ["node", "--version"],
        "npm": ["npm", "--version"],
    }
    for name, command in required_commands.items():
        version = command_version(command)
        print(f"{name}: {version or 'MISSING'}")
        if version is None:
            failures.append(f"required command is missing: {name}")
    node_version = command_version(["node", "--version"])
    if node_version:
        match = re.search(r"v?(\d+)", node_version)
        if match and int(match.group(1)) < 22:
            failures.append("Node.js 22 or newer is required")

    optional = {
        "uv": ["uv", "--version"],
        "git": ["git", "--version"],
        "docker": ["docker", "--version"],
        "oasdiff": [str(LOCAL_OASDIFF if LOCAL_OASDIFF.is_file() else "oasdiff"), "--version"],
    }
    for name, command in optional.items():
        print(f"{name}: {command_version(command) or 'not installed'}")

    modules = ["yaml", "jsonschema", "httpx", "pytest", "fastapi", "pydantic"]
    for module in modules:
        state = "available" if importlib.util.find_spec(module) else "not installed; run make setup"
        print(f"python module {module}: {state}")

    versions = COURSE / "tool-versions.json"
    if versions.is_file():
        payload = json.loads(versions.read_text(encoding="utf-8"))
        print(f"pinned tool families: {len(payload)}")
    else:
        failures.append("tool-versions.json is missing")

    required_files = [
        COURSE / "README.md",
        COURSE / "mkdocs.yml",
        CAPSTONE / "spec/openapi.yaml",
        CAPSTONE / "spec/openapi-3.2.yaml",
        CAPSTONE / "services/python-fastapi/src/analysis_api/app.py",
        CAPSTONE / "services/typescript-fastify/src/app.ts",
    ]
    missing = [str(path.relative_to(COURSE)) for path in required_files if not path.is_file()]
    failures.extend(f"missing required file: {item}" for item in missing)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("PASS: core host and course structure are ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
