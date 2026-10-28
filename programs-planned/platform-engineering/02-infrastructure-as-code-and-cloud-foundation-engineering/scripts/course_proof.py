from __future__ import annotations

import ast
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import yaml

from common import COURSE, CAPSTONE, load_json

MODULE_FILES = {'index.md', 'exercises.md', 'exercise-answers.md', 'lab.md', 'checkpoint.md'}
LAB_HEADINGS = {'Goal', 'Safety boundary', 'Baseline', 'Hypothesis', 'Controlled action', 'Oracle', 'Evidence', 'Interpretation', 'Cleanup', 'Completion gate'}
CHECKPOINT_HEADINGS = {'Required evidence', 'Decision defense', 'Progression gate'}


def run(name: str, command: list[str], *, env=None) -> dict:
    result = subprocess.run(command, cwd=COURSE, text=True, capture_output=True, env=env, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"{name} failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return {'name': name, 'status': 'pass', 'outputTail': (result.stdout + result.stderr)[-1200:]}


def numbered_headings(path: Path) -> list[str]:
    return re.findall(r'^##\s+(\d+)\.\s+(.+?)\s*$', path.read_text(encoding='utf-8'), flags=re.M)


def structure_checks() -> dict:
    modules = sorted((COURSE / 'course-book').glob('module-*'))
    if len(modules) != 11:
        raise RuntimeError(f'expected 11 module directories, found {len(modules)}')
    for module in modules:
        names = {p.name for p in module.iterdir() if p.is_file()}
        if module.name == 'module-00-orientation':
            required = {'index.md', 'lab.md', 'checkpoint.md'}
        else:
            required = MODULE_FILES
        missing = required - names
        if missing:
            raise RuntimeError(f'{module.name} missing {sorted(missing)}')
        lab_text = (module / 'lab.md').read_text(encoding='utf-8')
        headings = set(re.findall(r'^##\s+(.+?)\s*$', lab_text, flags=re.M))
        if not LAB_HEADINGS.issubset(headings):
            raise RuntimeError(f'{module.name} lab missing {sorted(LAB_HEADINGS - headings)}')
        checkpoint_text = (module / 'checkpoint.md').read_text(encoding='utf-8')
        checkpoint_headings = set(re.findall(r'^##\s+(.+?)\s*$', checkpoint_text, flags=re.M))
        if not CHECKPOINT_HEADINGS.issubset(checkpoint_headings):
            raise RuntimeError(
                f'{module.name} checkpoint missing '
                f'{sorted(CHECKPOINT_HEADINGS - checkpoint_headings)}'
            )
        if module.name != 'module-00-orientation':
            exercises = numbered_headings(module / 'exercises.md')
            answers = numbered_headings(module / 'exercise-answers.md')
            if len(exercises) != 12 or exercises != answers:
                raise RuntimeError(f'{module.name} exercise/answer identity mismatch')
            answer_text = (module / 'exercise-answers.md').read_text(encoding='utf-8')
            answer_matches = list(re.finditer(r'^##\s+\d+\.\s+.+$', answer_text, flags=re.M))
            for index, match in enumerate(answer_matches):
                end = answer_matches[index + 1].start() if index + 1 < len(answer_matches) else len(answer_text)
                answer_words = len(answer_text[match.end():end].split())
                if answer_words < 30:
                    raise RuntimeError(
                        f'{module.name} answer {index + 1} is too thin: {answer_words} words'
                    )
            words = len((module / 'index.md').read_text().split())
            if words < 1800:
                raise RuntimeError(f'{module.name} chapter is too thin: {words} words')
    return {'name': 'course-structure', 'status': 'pass', 'modules': len(modules)}


def parse_checks() -> dict:
    json_count = 0
    yaml_count = 0
    for path in COURSE.rglob('*.json'):
        if any(part in {'.pytest_cache', '__pycache__'} for part in path.parts):
            continue
        load_json(path)
        json_count += 1
    for path in list(COURSE.rglob('*.yaml')) + list(COURSE.rglob('*.yml')):
        if any(part in {'.pytest_cache', '__pycache__'} for part in path.parts):
            continue
        yaml.safe_load(path.read_text(encoding='utf-8'))
        yaml_count += 1
    return {'name': 'data-parsing', 'status': 'pass', 'json': json_count, 'yaml': yaml_count}


def python_syntax() -> dict:
    count = 0
    for path in COURSE.rglob('*.py'):
        if any(part in {'.pytest_cache', '__pycache__'} for part in path.parts):
            continue
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        count += 1
    return {'name': 'python-syntax', 'status': 'pass', 'files': count}


def docs_navigation_checks() -> dict:
    config = yaml.safe_load((COURSE / 'mkdocs.yml').read_text(encoding='utf-8'))
    nav = config.get('nav', [])
    referenced: list[str] = []

    def walk(value) -> None:
        if isinstance(value, str) and value.endswith('.md'):
            referenced.append(value)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)

    walk(nav)
    actual = sorted(path.relative_to(COURSE / 'course-book').as_posix() for path in (COURSE / 'course-book').rglob('*.md'))
    listed = sorted(referenced)
    if len(listed) != len(set(listed)):
        raise RuntimeError('mkdocs navigation contains duplicate Markdown paths')
    missing = sorted(set(actual) - set(listed))
    unknown = sorted(set(listed) - set(actual))
    if missing or unknown:
        raise RuntimeError(f'mkdocs navigation mismatch: missing={missing[:10]} unknown={unknown[:10]}')
    return {'name': 'mkdocs-navigation', 'status': 'pass', 'pages': len(actual)}


def shell_syntax_checks() -> dict:
    files = sorted({
        *COURSE.rglob('*.sh'),
        *(path for path in COURSE.rglob('*') if path.is_file() and path.parent.name == 'bin'),
    })
    for path in files:
        result = subprocess.run(['bash', '-n', str(path)], text=True, capture_output=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(f'shell syntax failed for {path.relative_to(COURSE)}: {result.stderr}')
    return {'name': 'shell-syntax', 'status': 'pass', 'files': len(files)}


def quality_checks() -> dict:
    paragraphs: Counter[str] = Counter()
    unfinished = []
    forbidden = re.compile(r'\b(TODO|TBD|FIXME|lorem ipsum|coming soon)\b', re.I)
    md_files = sorted((COURSE / 'course-book').rglob('*.md'))
    for path in md_files:
        text = path.read_text(encoding='utf-8')
        if forbidden.search(text):
            unfinished.append(path.relative_to(COURSE).as_posix())
        for paragraph in re.split(r'\n\s*\n', text):
            normalized = ' '.join(paragraph.split())
            if len(normalized.split()) >= 45 and not normalized.startswith('```'):
                paragraphs[normalized] += 1
    repeated = [p for p, count in paragraphs.items() if count >= 4]
    if unfinished:
        raise RuntimeError(f'unfinished markers in {unfinished[:10]}')
    if repeated:
        raise RuntimeError(f'repeated long course-book paragraphs: {len(repeated)}')
    return {'name': 'reader-quality', 'status': 'pass', 'markdownFiles': len(md_files), 'repeatedLongParagraphs': 0}


def main() -> int:
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([str(CAPSTONE), str(CAPSTONE / 'runtime')])
    checks = [structure_checks(), docs_navigation_checks(), parse_checks(), python_syntax(), shell_syntax_checks(), quality_checks()]
    checks.append(run('handoff-proof', [sys.executable, 'scripts/verify_handoff.py']))
    checks.append(run('hcl-guard', [sys.executable, 'scripts/hcl_guard.py']))
    checks.append(run('link-check', [sys.executable, 'scripts/check_links.py']))
    checks.append(run('python-tests', [sys.executable, '-m', 'pytest', '-q', 'capstone/tests'], env=env))
    checks.append(run('capstone-tour', [sys.executable, 'capstone/scripts/run_capstone_tour.py'], env=env))
    report = {'course': COURSE.name, 'passed': True, 'checks': checks}
    report_dir = COURSE / 'reports'
    report_dir.mkdir(exist_ok=True)
    (report_dir / 'core-proof.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, indent=2))
        raise
