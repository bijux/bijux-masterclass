"""Fingerprint program, shared execution and actual runtime dependency inputs."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def fingerprint(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def program_inputs(root: Path, program: str) -> dict[str, str]:
    prefix = f"programs/{program}/"
    if not (root / prefix).is_dir() or ".." in Path(program).parts:
        raise ValueError("unknown program input boundary")
    tracked = (
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=root,
        )
        .decode()
        .split("\0")
    )
    result = {}
    for relative in filter(None, tracked):
        # Other course trees and the series publication pages are independent
        # inputs. Every shared recipe, script, workflow and configuration remains
        # included; the complete selected course tree includes fixtures and docs.
        if relative.startswith("programs/") and not relative.startswith(prefix):
            continue
        if relative.startswith("docs/"):
            continue
        path = root / relative
        if path.is_symlink():
            target = path.resolve(strict=True)
            target.relative_to(root.resolve())
            if not target.is_file():
                raise ValueError(f"unsupported directory execution symlink: {relative}")
            content = (
                b"symlink\0" + os.readlink(path).encode() + b"\0" + target.read_bytes()
            )
        elif path.is_file():
            content = (
                b"file\0"
                + str(path.stat().st_mode & 0o111).encode()
                + b"\0"
                + path.read_bytes()
            )
        else:
            raise ValueError(f"missing tracked execution input: {relative}")
        result[relative] = hashlib.sha256(content).hexdigest()
    if not any(relative.startswith(prefix) for relative in result):
        raise ValueError("selected program has no tracked inputs")
    return result


def runtime_inputs(
    python: Path, environment: dict[str, str] | None = None
) -> dict[str, Any]:
    script = """import csv,hashlib,importlib.metadata,io,json,os,pathlib,platform,sys,sysconfig

def payload(path):
    if not path.is_file():
        raise ValueError('missing runtime payload: '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()

packages=[]
for distribution in importlib.metadata.distributions():
    record=distribution.read_text('RECORD')
    installed_record=record is not None
    if installed_record:
        rows=list(csv.reader(io.StringIO(record)))
        if not rows or any(len(row)!=3 or not row[0] for row in rows):
            raise ValueError('malformed installed file inventory')
        entries=[pathlib.PurePosixPath(row[0]) for row in rows]
    else:
        sources=distribution.read_text('SOURCES.txt')
        if sources is None:
            raise ValueError('distribution has no file inventory')
        entries=[pathlib.PurePosixPath(line) for line in sources.splitlines() if line]
    files={}
    for entry in entries:
        if '__pycache__' in entry.parts or str(entry).endswith(('.pyc','.pyo')):
            continue
        path=pathlib.Path(distribution.locate_file(entry))
        if not path.is_file() and not installed_record:
            files[str(entry)]='legacy source manifest; not installed payload'
            continue
        files[str(entry)]=payload(path)
    packages.append({'name':distribution.metadata['Name'].lower().replace('_','-'),
                     'version':distribution.version,'installed_record':installed_record,'files':files})
stdlib=pathlib.Path(sysconfig.get_path('stdlib'))
standard={}
for directory, children, files in os.walk(stdlib):
    children[:]=[child for child in children if child not in {'site-packages','__pycache__'}]
    for name in files:
        path=pathlib.Path(directory)/name
        if not name.endswith(('.pyc','.pyo')):
            standard[str(path.relative_to(stdlib))]=payload(path)
print(json.dumps({'python':sys.version,'implementation':platform.python_implementation(),
'platform':platform.platform(),'machine':platform.machine(),
'interpreter_sha256':payload(pathlib.Path(sys.executable).resolve()),
'stdlib_digest':hashlib.sha256(json.dumps(standard,sort_keys=True).encode()).hexdigest(),
'packages':sorted(packages,key=lambda item:item['name'])},sort_keys=True))"""
    observed = json.loads(
        subprocess.check_output([str(python), "-c", script], text=True, env=environment)
    )
    for name in ("make", "git"):
        executable = shutil.which(name)
        if executable is None:
            raise ValueError(f"missing execution tool: {name}")
        observed[name + "_sha256"] = hashlib.sha256(
            Path(executable).resolve().read_bytes()
        ).hexdigest()
    observed["make"] = subprocess.check_output(
        ["make", "--version"], text=True
    ).splitlines()[0]
    observed["git"] = subprocess.check_output(["git", "--version"], text=True).strip()
    effective = os.environ if environment is None else environment
    observed["runner"] = {
        key: effective.get(key)
        for key in (
            "RUNNER_OS",
            "RUNNER_ARCH",
            "ImageOS",
            "ImageVersion",
            "imageos",
            "imageversion",
            "LANG",
            "LC_ALL",
            "TZ",
            "PYTHONHASHSEED",
            "PYTEST_ADDOPTS",
            "SNAKEMAKE_PROFILE",
            "DVC_CONFIG",
        )
    }
    return observed
