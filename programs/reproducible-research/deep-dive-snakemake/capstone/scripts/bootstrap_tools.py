#!/usr/bin/env python3
"""Admit a metadata-owned capstone tool environment without replacing user work."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tomllib
from pathlib import Path

MARKER = "bijux-capstone-toolchain.json"
RUNTIME = """import json,platform,sys
print(json.dumps(dict(implementation=platform.python_implementation(),version=platform.python_version(),
system=platform.system(),machine=platform.machine(),prefix=sys.prefix,base_prefix=sys.base_prefix)))"""
CLOSURE = """import importlib.metadata,json,re,sys,tomllib
from packaging.requirements import Requirement
from packaging.markers import default_environment
from packaging.specifiers import SpecifierSet
from pathlib import Path
lock=Path(sys.argv[1]); project=tomllib.loads(Path(sys.argv[2]).read_text())["project"]
environment=default_environment(); environment["extra"]="dev"
expected={}; pending=""
for raw in lock.read_text().splitlines():
 line=raw.strip()
 if not line or line.startswith("#"):continue
 pending+=line[:-1].strip()+" " if line.endswith("\\\\") else line
 if line.endswith("\\\\"):continue
 requirement=Requirement(pending.split(" --hash=",1)[0]);pending=""
 if requirement.marker and not requirement.marker.evaluate(environment):continue
 version=next(iter(requirement.specifier)).version
 name=re.sub(r"[-_.]+","-",requirement.name).lower()
 if name in expected and expected[name]!=version:
  raise SystemExit("Ambiguous locked distribution: "+name)
 expected[name]=version
rows=[(re.sub(r"[-_.]+","-",d.metadata["Name"]).lower(),d.version)
      for d in importlib.metadata.distributions()]
if len(rows)!=len(dict(rows)) or dict(rows)!=expected:
 raise SystemExit("Installed closure differs from the exact platform lock")
if not SpecifierSet(project["requires-python"]).contains(environment["python_full_version"]):
 raise SystemExit("Unsupported metadata Python runtime")
for entry in project["dependencies"]+project["optional-dependencies"]["dev"]:
 requirement=Requirement(entry)
 if requirement.marker and not requirement.marker.evaluate(environment):continue
 name=re.sub(r"[-_.]+","-",requirement.name).lower()
 if name not in expected or not requirement.specifier.contains(expected[name]):
  raise SystemExit("Locked tool violates package metadata: "+name)
print(json.dumps(dict(packages=expected,runtime=environment),sort_keys=True))"""


def sha(body: bytes) -> str:
    """Bind the exact bytes admitted by a toolchain boundary."""
    return hashlib.sha256(body).hexdigest()


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    """Refuse duplicate identity keys rather than accepting the last value."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise RuntimeError("Duplicate toolchain identity key: " + key)
        result[key] = value
    return result


def source(root: Path, path: Path) -> bytes:
    """Read a regular source input confined to its repository."""
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise RuntimeError("Toolchain source must remain in its owning repository") from error
    current = root
    for part in relative.parts:
        if part in (".", ".."):
            raise RuntimeError("Unsafe toolchain source path")
        current /= part
        if current.is_symlink():
            raise RuntimeError("Toolchain source aliases are forbidden")
    if not current.is_file():
        raise RuntimeError("A regular toolchain source input is required: " + str(relative))
    return current.read_bytes()


def artifact(root: Path, path: Path) -> Path:
    """Protect every path outside the repository artifact boundary."""
    candidate = path.absolute()
    if (
        ".." in candidate.parts
        or candidate == root / "artifacts"
        or not candidate.is_relative_to(root / "artifacts")
    ):
        raise RuntimeError("Toolchain outputs must remain inside repository artifacts/")
    for current in (candidate, *candidate.parents):
        if current == root:
            break
        if current.is_symlink():
            raise RuntimeError("Toolchain artifact aliases are forbidden")
    return candidate


def run(arguments: list[str], environment: dict[str, str]) -> str:
    """Propagate every failed toolchain child before confirmation."""
    result = subprocess.run(arguments, env=environment, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(
            "Toolchain command failed: "
            + " ".join(arguments)
            + "\n"
            + result.stdout
            + result.stderr
        )
    return result.stdout.strip()


def prepare(
    root: Path,
    capstone: Path,
    python: str,
    target: Path,
    uv: str,
    receipt: Path,
    *,
    fresh: bool = False,
) -> dict:
    """Create or strictly revalidate an owned locked environment."""
    root = root.resolve()
    target, receipt = artifact(root, target), artifact(root, receipt)
    if receipt.is_relative_to(target):
        raise RuntimeError("Toolchain receipt must not overwrite environment content")
    paths = [
        capstone / name
        for name in (
            "pyproject.toml",
            "requirements-tools.lock",
            "requirements-tools.provenance.json",
            "Makefile",
            "scripts/bootstrap_tools.py",
        )
    ]
    captured = {str(path.relative_to(root)): sha(source(root, path)) for path in paths}
    metadata = tomllib.loads(source(root, paths[0]).decode())["project"]
    provenance = json.loads(source(root, paths[2]), object_pairs_hook=unique_object)
    if provenance != {
        "schema": 1,
        "pyproject_sha256": captured[str(paths[0].relative_to(root))],
        "lock_sha256": captured[str(paths[1].relative_to(root))],
        "extra": "dev",
    }:
        raise RuntimeError("Regenerate the tools lock from its current package metadata")
    executable, installer = shutil.which(python), shutil.which(uv)
    if not executable or not installer:
        raise RuntimeError("Select installed Python and uv; automatic downloads are forbidden")
    executable, installer = str(Path(executable).resolve()), str(Path(installer).resolve())
    environment = {
        **os.environ,
        "UV_CACHE_DIR": str(receipt.parent / "cache/uv"),
        "UV_PYTHON_DOWNLOADS": "never",
        "PYTHONPYCACHEPREFIX": str(receipt.parent / "cache/python"),
    }
    runtime = json.loads(run([executable, "-I", "-B", "-c", RUNTIME], environment))
    declared_python = metadata.get("requires-python", "")
    minimum = re.fullmatch(r">=(\d+)\.(\d+)", declared_python)
    version = tuple(int(part) for part in runtime["version"].split("."))
    if (
        minimum is None
        or runtime.get("implementation") != "CPython"
        or runtime.get("prefix") != runtime.get("base_prefix")
        or version[:2] < (int(minimum[1]), int(minimum[2]))
    ):
        raise RuntimeError("Select a supported base CPython admitted by package metadata")
    uv_version = run([installer, "--version"], environment)
    if not re.fullmatch(r"uv 0\.11\.17(?: \([^\r\n]*\))?", uv_version):
        raise RuntimeError("The reviewed tools installer requires uv 0.11.17")
    identity = {
        "schema": 1,
        "source_sha256": captured,
        "runtime": runtime,
        "python_sha256": sha(Path(executable).read_bytes()),
        "uv_sha256": sha(Path(installer).read_bytes()),
        "uv_version": uv_version,
        "base_executable": executable,
    }
    marker = target / MARKER
    if target.exists():
        if not target.is_dir() or marker.is_symlink() or not marker.is_file():
            raise RuntimeError("Preserve the unowned tool environment; select a new artifact path")
        owned = json.loads(marker.read_text(), object_pairs_hook=unique_object)
        if (
            set(owned) != {*identity, "status"}
            or any(owned.get(key) != value for key, value in identity.items())
            or owned.get("status") not in ("preparing", "ready")
        ):
            raise RuntimeError("Preserve the stale tool environment; select a new artifact path")
        if fresh:
            raise RuntimeError("Clean-room confirmation requires a new artifact environment")
    else:
        target.mkdir(parents=True)
        owned = {**identity, "status": "preparing"}
        marker.write_text(json.dumps(owned, indent=2, sort_keys=True) + "\n")
        run([executable, "-I", "-B", "-m", "venv", "--without-pip", str(target)], environment)
    venv_python = target / "bin/python"
    if (
        (target / "bin").is_symlink()
        or not venv_python.is_file()
        or (venv_python.is_symlink() and str(venv_python.resolve()) != executable)
    ):
        raise RuntimeError("Preserve the tool environment with a missing or changed interpreter")
    admitted = json.loads(run([str(venv_python), "-I", "-B", "-c", RUNTIME], environment))
    if (
        any(admitted.get(key) != value for key, value in runtime.items() if key != "prefix")
        or Path(admitted["prefix"]).resolve() != target
    ):
        raise RuntimeError("Preserve the mismatched tool environment interpreter")
    if owned["status"] != "ready":
        existing = run(
            [
                str(venv_python),
                "-I",
                "-B",
                "-c",
                "import importlib.metadata,json;"
                'rows=[d.metadata["Name"] for d in importlib.metadata.distributions()];'
                "print(json.dumps(rows))",
            ],
            environment,
        )
        if json.loads(existing):
            raise RuntimeError("Preserve unexpected packages in the preparing tool environment")
        run(
            [
                installer,
                "--no-config",
                "pip",
                "sync",
                "--require-hashes",
                "--python",
                str(venv_python),
                str(paths[1]),
            ],
            environment,
        )
    closure = json.loads(
        run(
            [str(venv_python), "-I", "-B", "-c", CLOSURE, str(paths[1]), str(paths[0])], environment
        )
    )
    run([installer, "--no-config", "pip", "check", "--python", str(venv_python)], environment)
    tools = {
        name: run([str(target / "bin" / name), "--version"], environment)
        for name in ("snakemake", "pytest", "ruff")
    }
    if captured != {str(path.relative_to(root)): sha(source(root, path)) for path in paths}:
        raise RuntimeError("Toolchain source changed during admission")
    owned["status"] = "ready"
    marker.write_text(json.dumps(owned, indent=2, sort_keys=True) + "\n")
    result = {
        "schema": 1,
        "environment": str(target),
        "identity": identity,
        "closure": closure,
        "tools": tools,
        "status": "ready",
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    """Expose explicit owned paths and fail closed on admission errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--capstone", type=Path, required=True)
    parser.add_argument("--python", default="python3.11")
    parser.add_argument("--uv", default="uv")
    parser.add_argument("--environment", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()
    try:
        result = prepare(
            args.root,
            args.capstone,
            args.python,
            args.environment,
            args.uv,
            args.receipt,
            fresh=args.fresh,
        )
    except (RuntimeError, ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
