#!/usr/bin/env python3
"""Prepare a hash-locked documentation verification environment without replacing user work."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

DEFAULT_PROFILE = 'darwin-arm64-cpython-314'
PROFILE_PATH = 'configs/docs/environment-profiles.json'
VERIFICATION_RUNTIME = {'implementation': 'CPython', 'version': '3.14.4', 'system': 'Darwin', 'machine': 'arm64'}
DIRECT_PACKAGES = frozenset({'mkdocs', 'mkdocs-material', 'mkdocs-autorefs', 'pymdown-extensions',
                            'mkdocs-macros-plugin', 'mkdocs-git-revision-date-localized-plugin', 'mkdocs-minify-plugin', 'setuptools'})
MARKER = 'bijux-docs-environment.json'
PROBE = '''import json,platform,sys
print(json.dumps(dict(implementation=platform.python_implementation(),version=platform.python_version(),
system=platform.system(),machine=platform.machine(),prefix=sys.prefix,base_prefix=sys.base_prefix)))'''
PACKAGES = '''import importlib.metadata,json,re
rows=[(re.sub(r"[-_.]+","-",d.metadata["Name"]).lower(),d.version) for d in importlib.metadata.distributions()]
print(json.dumps(rows))'''

FILES = r'''import hashlib,json,os,sys,sysconfig
from pathlib import Path
scope=sys.argv[1]
root=Path(sysconfig.get_path("stdlib")) if scope=="stdlib" else Path(sys.prefix)
rows={}
for directory,children,names in os.walk(root):
 children[:]=sorted(name for name in children if name!="__pycache__" and
                   not(scope=="stdlib" and name=="site-packages"))
 for name in sorted(names):
  path=Path(directory)/name
  relative=path.relative_to(root).as_posix()
  if name.endswith((".pyc",".pyo")) or name=="bijux-docs-environment.json":continue
  if relative.startswith("bin/python"):continue
  if scope!="stdlib" and path.is_symlink() and not (relative.startswith("bin/") and
       path.resolve()==Path(sys.executable).resolve()):
   raise SystemExit("Unexpected environment file alias")
  rows[relative]={"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"size":path.stat().st_size,
                  "link":str(path.readlink()) if path.is_symlink() else None}
print(json.dumps(rows,sort_keys=True))'''


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(arguments: list[str], *, environment: dict[str, str]) -> str:
    result = subprocess.run(arguments, env=environment, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError('Documentation environment command failed: ' + ' '.join(arguments) + '\n' + result.stdout + result.stderr)
    return result.stdout.strip()


def normalized(name: str) -> str:
    return re.sub(r'[-_.]+', '-', name).lower()


def locked_packages(path: Path) -> dict[str, str]:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError('A regular documentation hash lock is required')
    rows = []
    pending = ''
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        pending += line[:-1].strip() + ' ' if line.endswith('\\') else line
        if not line.endswith('\\'):
            rows.append(pending.strip())
            pending = ''
    if pending:
        raise RuntimeError('Documentation lock has an incomplete continuation')
    packages = {}
    for row in rows:
        match = re.fullmatch(r'([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+!-]+)((?:\s+--hash=sha256:[a-f0-9]{64})+)', row)
        if not match:
            raise RuntimeError('Every documentation package requires one exact version and SHA-256 download hashes')
        name = normalized(match[1])
        if name in packages:
            raise RuntimeError('Documentation lock duplicates package ' + name)
        packages[name] = match[2]
    if not packages or not DIRECT_PACKAGES.issubset(packages):
        raise RuntimeError('Documentation lock must preserve the reviewed direct dependency inventory')
    return packages


def numeric_version(version: str) -> tuple[int, ...]:
    if not re.fullmatch(r'\d+(?:\.\d+)*', version):
        raise RuntimeError('Documentation range review requires a numeric version: ' + version)
    parts = tuple(int(part) for part in version.split('.'))
    return parts + (0,) * (4 - len(parts))


def declared_ranges(path: Path, packages: dict[str, str]) -> None:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError('A regular authored documentation requirements file is required')
    seen = set()
    for row in path.read_text().splitlines():
        row = row.strip()
        if not row or row.startswith('#'):
            continue
        match = re.fullmatch(r'([A-Za-z0-9_.-]+)>=(\d+(?:\.\d+)*),<(\d+(?:\.\d+)*)', row)
        if not match:
            raise RuntimeError('Review the documentation lock for the changed authored requirements syntax')
        name = normalized(match[1])
        if name not in packages or name in seen:
            raise RuntimeError('Documentation lock does not preserve authored requirement ' + name)
        version = numeric_version(packages[name])
        if not numeric_version(match[2]) <= version < numeric_version(match[3]):
            raise RuntimeError('Documentation lock violates authored version range for ' + name)
        seen.add(name)
    if seen != DIRECT_PACKAGES:
        raise RuntimeError('Review the documentation lock for changed authored plugin capabilities')


def artifact_path(root: Path, path: Path) -> Path:
    candidate = path if path.is_absolute() else root / path
    candidate = candidate.absolute()
    artifacts = root / 'artifacts'
    if '..' in candidate.parts or not candidate.is_relative_to(artifacts) or candidate == artifacts:
        raise RuntimeError('Documentation environment and receipts must remain inside repository artifacts/')
    for item in (candidate, *candidate.parents):
        if item == root:
            break
        if item.is_symlink():
            raise RuntimeError('Preserve symlinked documentation environment or artifact path: ' + str(item))
    return candidate


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def source_bytes(root: Path, relative: str) -> bytes:
    candidate = Path(relative)
    if candidate.is_absolute() or '..' in candidate.parts or not candidate.parts:
        raise RuntimeError('Documentation source input must remain inside its owning repository')
    current = root
    for part in candidate.parts:
        current = current / part
        if current.is_symlink():
            raise RuntimeError('A regular documentation source input is required: ' + relative)
    if not current.is_file():
        raise RuntimeError('A regular documentation source input is required: ' + relative)
    return current.read_bytes()


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise RuntimeError('Duplicate documentation admission key: ' + key)
        result[key] = value
    return result


def reviewed_profile(root: Path, name: str, lock: Path, packages: dict[str, str]) -> tuple[dict, dict]:
    body = source_bytes(root, PROFILE_PATH)
    document = json.loads(body, object_pairs_hook=unique_object)
    if (not isinstance(document, dict) or set(document) != {'schema', 'profiles'}
            or type(document['schema']) is not int or document['schema'] != 1
            or not isinstance(document['profiles'], dict) or name not in document['profiles']):
        raise RuntimeError('Select an explicitly reviewed documentation verification profile; production requires its own admission')
    profile = document['profiles'][name]
    keys = {'purpose', 'runtime', 'packages', 'direct_packages', 'lock_sha256', 'uv_version', 'source_inputs'}
    if (not isinstance(profile, dict) or set(profile) != keys
            or profile['purpose'] != 'verification-only'
            or profile['runtime'] != VERIFICATION_RUNTIME
            or profile['uv_version'] != '0.11.17'
            or not isinstance(profile['direct_packages'], list)
            or len(profile['direct_packages']) != len(DIRECT_PACKAGES)
            or set(profile['direct_packages']) != DIRECT_PACKAGES
            or not isinstance(profile['packages'], dict)
            or len(profile['packages']) != 44 or profile['packages'] != packages
            or profile['lock_sha256'] != digest(lock.read_bytes())
            or profile['source_inputs'] != ['scripts/docs_environment.py', 'makes/series-docs.mk']):
        raise RuntimeError('Documentation profile must preserve the reviewed 44-package dependency inventory and exact source contract')
    sources = {PROFILE_PATH: digest(body)}
    sources.update({relative: digest(source_bytes(root, relative)) for relative in profile['source_inputs']})
    return profile, sources


def prepare(root: Path, python: str, environment_path: Path, lock: Path,
            requirements: Path, uv: str, receipt: Path, *, install: bool = True, profile_name: str = DEFAULT_PROFILE) -> dict:
    root = root.resolve()
    target = artifact_path(root, environment_path)
    receipt = artifact_path(root, receipt)
    if receipt.is_relative_to(target):
        raise RuntimeError('Documentation receipt must not overwrite environment content')
    lock = lock if lock.is_absolute() else root / lock
    requirements = requirements if requirements.is_absolute() else root / requirements
    for original in (lock, requirements):
        try:
            relative = str(original.relative_to(root))
        except ValueError as error:
            raise RuntimeError('Documentation source input must remain inside its owning repository') from error
        source_bytes(root, relative)
    packages = locked_packages(lock)
    declared_ranges(requirements, packages)
    profile, sources = reviewed_profile(root, profile_name, lock, packages)
    sources.update({str(path.relative_to(root)): digest(path.read_bytes()) for path in (lock, requirements)})
    executable = shutil.which(python)
    uv_executable = shutil.which(uv)
    if not executable or not uv_executable:
        raise RuntimeError('Select installed Python and uv executables; automatic tool downloads are not allowed')
    executable = str(Path(executable).resolve())
    command_environment = dict(os.environ)
    command_environment.update(UV_CACHE_DIR=str(receipt.parent / 'cache/uv'),
                               UV_PYTHON_DOWNLOADS='never', PYTHONPYCACHEPREFIX=str(receipt.parent / 'cache/python'))
    runtime = json.loads(run([executable, '-I', '-B', '-c', PROBE], environment=command_environment))
    if any(runtime.get(key) != value for key, value in VERIFICATION_RUNTIME.items()) or runtime.get('prefix') != runtime.get('base_prefix'):
        raise RuntimeError('This documentation lock requires a base CPython 3.14.4 Darwin arm64 verification runtime; deployment Python 3.11 requires its own reviewed lock/profile')
    uv_version = run([uv_executable, '--version'], environment=command_environment)
    if not re.fullmatch(r'uv 0[.]11[.]17(?: \([^\r\n]*\))?', uv_version):
        raise RuntimeError('This documentation installer requires uv 0.11.17')
    base_files = json.loads(run([executable, '-I', '-B', '-c', FILES, 'stdlib'], environment=command_environment))
    identity = dict(schema=1, base_files_sha256=base_files, purpose='verification-only', profile=profile_name, source_sha256=sources, runtime=runtime, base_executable=executable,
                    base_executable_sha256=digest(Path(executable).read_bytes()), lock_sha256=digest(lock.read_bytes()),
                    requirements_sha256=digest(requirements.read_bytes()), uv_version=uv_version)
    marker = target / MARKER
    if target.exists():
        if not target.is_dir() or marker.is_symlink() or not marker.is_file():
            raise RuntimeError('Preserve the existing unowned environment; select a new artifacts/ environment path')
        try:
            owned = json.loads(marker.read_text(), object_pairs_hook=unique_object)
        except (ValueError, OSError) as error:
            raise RuntimeError('Preserve the invalid environment ownership marker') from error
        if set(owned) != ({*identity, 'status', 'site_files_sha256'} if owned.get('status') == 'ready' else {*identity, 'status'}) or any(owned.get(key) != value for key, value in identity.items()) or owned.get('status') not in ('preparing', 'ready'):
            raise RuntimeError('Preserve the stale documentation environment; select a new artifacts/ environment path')
    else:
        target.mkdir(parents=True)
        owned = {**identity, 'status': 'preparing'}
        write_json(marker, owned)
    venv_python = target / 'bin/python'
    if (target / 'bin').is_symlink():
        raise RuntimeError('Preserve the environment with a symlinked executable directory')
    if not venv_python.exists():
        if owned['status'] == 'ready':
            raise RuntimeError('Preserve the damaged ready environment; its interpreter is missing')
        run([executable, '-I', '-B', '-m', 'venv', '--without-pip', str(target)], environment=command_environment)
    if (venv_python.is_symlink() and venv_python.resolve() != Path(executable)
            or not venv_python.is_file()):
        raise RuntimeError('Preserve the environment with an unexpected interpreter executable')
    actual_runtime = json.loads(run([str(venv_python), '-I', '-B', '-c', PROBE], environment=command_environment))
    if (any(actual_runtime.get(key) != value for key, value in VERIFICATION_RUNTIME.items())
            or Path(actual_runtime.get('prefix', '')).resolve() != target.resolve()
            or actual_runtime.get('base_prefix') != runtime['base_prefix']):
        raise RuntimeError('Preserve the documentation environment with a mismatched interpreter')
    if install and owned['status'] != 'ready':
        existing_rows = json.loads(run([str(venv_python), '-I', '-B', '-c', PACKAGES], environment=command_environment))
        if (len(existing_rows) != len(dict(existing_rows))
                or any(packages.get(name) != version for name, version in existing_rows)):
            raise RuntimeError('Preserve unexpected packages in the preparing environment; sync must not remove user changes')
        run([uv_executable, '--no-config', 'pip', 'sync', '--require-hashes', '--python', str(venv_python), str(lock)], environment=command_environment)
    if install or owned['status'] == 'ready':
        rows = json.loads(run([str(venv_python), '-I', '-B', '-c', PACKAGES], environment=command_environment))
        if len(rows) != len(dict(rows)) or dict(rows) != packages:
            raise RuntimeError('Preserve the documentation environment with missing, changed or unexpected installed packages')
        run([uv_executable, '--no-config', 'pip', 'check', '--python', str(venv_python)], environment=command_environment)
        site_files = json.loads(run([str(venv_python), '-I', '-B', '-c', FILES, 'installed-files'], environment=command_environment))
        if owned['status'] == 'ready' and owned.get('site_files_sha256') != site_files:
            raise RuntimeError('Preserve the documentation environment with changed installed file bytes')
        owned['site_files_sha256'] = site_files
        owned['status'] = 'ready'
        write_json(marker, owned)
    if base_files != json.loads(run([executable, '-I', '-B', '-c', FILES, 'stdlib'], environment=command_environment)):
        raise RuntimeError('Documentation base runtime changed during environment admission')
    if sources != {relative: digest(source_bytes(root, relative)) for relative in sources}:
        raise RuntimeError('Documentation source changed during environment admission')
    result = dict(schema=1, purpose='verification-only', publication_approved=False, environment=str(target),
                  python=str(venv_python), status=owned['status'], package_count=len(packages), identity=identity)
    write_json(receipt, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--python', default='python3')
    parser.add_argument('--environment', type=Path, required=True)
    parser.add_argument('--lock', type=Path, default=Path('configs/docs/requirements-docs.lock'))
    parser.add_argument('--requirements', type=Path, default=Path('configs/docs/requirements-docs.txt'))
    parser.add_argument('--uv', default='uv')
    parser.add_argument('--receipt', type=Path, default=Path('artifacts/docs/environment.json'))
    parser.add_argument('--profile', default=DEFAULT_PROFILE)
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    try:
        result = prepare(args.root, args.python, args.environment, args.lock, args.requirements, args.uv, args.receipt, install=not args.prepare_only, profile_name=args.profile)
    except (RuntimeError, ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
