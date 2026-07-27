"""Capture the execution context needed to interpret local performance evidence."""

from __future__ import annotations

import hashlib
import platform
import shlex
import shutil
import subprocess
from pathlib import Path


def command_identity(command: str) -> dict[str, str]:
    arguments = shlex.split(command)
    if not arguments:
        raise ValueError("tool command must not be empty")
    executable = shutil.which(arguments[0])
    if executable is None:
        raise ValueError(f"tool is not available: {arguments[0]}")
    result = subprocess.run(
        [*arguments, "--version"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"cannot identify {command}: {detail}")
    output = result.stdout.strip() or result.stderr.strip()
    if not output:
        raise ValueError(f"{command} --version produced no identity")
    return {
        "command": command,
        "executable": str(Path(executable).resolve()),
        "version": output.splitlines()[0],
    }


def repository_identity(workspace: Path) -> dict[str, str]:
    root = subprocess.run(
        ["git", "-C", str(workspace), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if root.returncode != 0:
        return {
            "revision": "unavailable",
            "status": "unavailable",
            "status_sha256": "unavailable",
        }

    repository = Path(root.stdout.strip())
    revision = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "-C", str(repository), "status", "--porcelain=v1", "--untracked-files=all"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    return {
        "revision": revision,
        "status": "clean" if not status else "dirty",
        "status_sha256": hashlib.sha256(status.encode()).hexdigest(),
    }


def capture_execution_context(
    *,
    workspace: Path,
    make_command: str,
    compiler_command: str,
    runner_label: str,
) -> dict[str, object]:
    label = runner_label.strip()
    if not label:
        raise ValueError("runner label must not be empty")
    return {
        "compiler": command_identity(compiler_command),
        "make": command_identity(make_command),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "repository": repository_identity(workspace),
        "runner": label,
    }
