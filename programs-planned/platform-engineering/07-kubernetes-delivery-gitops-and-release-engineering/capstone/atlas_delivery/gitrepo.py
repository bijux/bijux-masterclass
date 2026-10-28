from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(repo: str | Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def commit(repo: str | Path, message: str) -> str:
    run_git(repo, "add", "-A")
    run_git(repo, "commit", "-m", message)
    return run_git(repo, "rev-parse", "HEAD")


def current_commit(repo: str | Path) -> str:
    return run_git(repo, "rev-parse", "HEAD")


def graph(repo: str | Path) -> str:
    return run_git(repo, "log", "--graph", "--decorate", "--oneline", "--all")
