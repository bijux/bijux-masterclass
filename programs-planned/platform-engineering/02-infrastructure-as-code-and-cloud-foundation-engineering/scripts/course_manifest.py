from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import COURSE, sha256

EXCLUDED_NAMES = {
    'MANIFEST.json', 'MANIFEST.sha256', '.DS_Store',
}
EXCLUDED_PARTS = {
    '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.venv', 'node_modules', '.terraform',
}


def included(path: Path) -> bool:
    rel = path.relative_to(COURSE)
    if path.name in EXCLUDED_NAMES or any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if path.suffix == '.pyc':
        return False
    if rel.parts[:2] == ('capstone', 'reports') and path.name != '.gitkeep':
        return False
    if rel.parts[:1] == ('reports',) and path.name not in {'.gitkeep', 'release-verification.json'}:
        return False
    return True


def build() -> dict:
    rows = []
    for path in sorted(p for p in COURSE.rglob('*') if p.is_file() and included(p)):
        rows.append({
            'path': path.relative_to(COURSE).as_posix(),
            'sha256': sha256(path),
            'bytes': path.stat().st_size,
            'mode': oct(path.stat().st_mode & 0o777),
        })
    return {'schemaVersion': '1.0', 'course': COURSE.name, 'files': rows}


def write_manifest() -> dict:
    manifest = build()
    path = COURSE / 'MANIFEST.json'
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    digest = sha256(path)
    (COURSE / 'MANIFEST.sha256').write_text(f'{digest}  MANIFEST.json\n')
    return manifest


def verify() -> tuple[dict, list[str]]:
    path = COURSE / 'MANIFEST.json'
    expected = json.loads(path.read_text())
    current = build()
    errors: list[str] = []
    expected_by = {row['path']: row for row in expected.get('files', [])}
    current_by = {row['path']: row for row in current.get('files', [])}
    for rel in sorted(set(expected_by) | set(current_by)):
        if rel not in expected_by:
            errors.append(f'unlisted file: {rel}')
        elif rel not in current_by:
            errors.append(f'missing file: {rel}')
        elif expected_by[rel] != current_by[rel]:
            errors.append(f'metadata/digest mismatch: {rel}')
    expected_digest = (COURSE / 'MANIFEST.sha256').read_text().split()[0]
    if sha256(path) != expected_digest:
        errors.append('MANIFEST.json digest does not match MANIFEST.sha256')
    return current, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['build', 'verify'])
    args = parser.parse_args()
    if args.command == 'build':
        manifest = write_manifest()
        print(json.dumps({'written': len(manifest['files'])}, indent=2))
        return 0
    manifest, errors = verify()
    print(json.dumps({'files': len(manifest['files']), 'valid': not errors, 'errors': errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
