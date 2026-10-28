from __future__ import annotations
from pathlib import Path
import hashlib, json, os, re, subprocess, sys

COURSE = Path(__file__).resolve().parents[1]
PROGRAM = COURSE.parent
CAPSTONE = COURSE / "capstone"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env: merged.update(env)
    result = subprocess.run(command, cwd=cwd, env=merged, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        print(result.stdout)
        raise SystemExit(result.returncode)
    return result


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def passed(message: str) -> None:
    print(f"PASS {message}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
