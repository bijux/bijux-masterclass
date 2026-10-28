#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json
import re
import sys
import yaml

COURSE = Path(__file__).resolve().parents[1]
SKIP = {'node_modules', 'dist', 'site', '__pycache__', '.pytest_cache'}
errors: list[str] = []


def visible(path: Path) -> bool:
    return not any(part in SKIP for part in path.parts)


def prose_words(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9_#'`.-]+", text))


def walk_nav(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for value in value for item in walk_nav(value)]
    if isinstance(value, dict):
        return [item for value in value.values() for item in walk_nav(value)]
    return []

required = [
    'README.md', '.nvmrc', 'Makefile', 'mkdocs.yml', 'package.json', 'tsconfig.base.json',
    'course-book/index.md', 'course-book/outcomes.md', 'course-book/study-plan.md',
    'course-book/reference.md', 'course-book/final-review.md',
    'course-book/final-review-solutions.md', 'course-book/capstone.md',
    'labs/README.md', 'compiler-labs/README.md', 'compiler-labs/manifest.json',
    'capstone/README.md', 'capstone/package.json', 'capstone/scripts/demo.sh',
    'fixtures/tls/ca-cert.pem', 'fixtures/tls/server-cert.pem', 'fixtures/tls/server-key.pem',
]
for rel in required:
    if not (COURSE / rel).is_file():
        errors.append(f'missing {rel}')

modules = sorted((COURSE / 'course-book').glob('module-*'))
if len(modules) != 10:
    errors.append(f'expected 10 modules, found {len(modules)}')
for number, module in zip(range(51, 61), modules, strict=False):
    if not module.name.startswith(f'module-{number:02d}-'):
        errors.append(f'nonsequential module: {module.name}')
    for filename, minimum in [('index.md', 1800), ('workbook.md', 430), ('solutions.md', 600)]:
        page = module / filename
        if not page.is_file():
            errors.append(f'missing {page.relative_to(COURSE)}')
            continue
        words = prose_words(page)
        if words < minimum:
            errors.append(f'{page.relative_to(COURSE)} too thin: {words} < {minimum}')
    chapter = module / 'index.md'
    if chapter.is_file():
        text = chapter.read_text(encoding='utf-8')
        for heading in ('## The governing question', '## Why this module comes now', '## Common wrong models'):
            if heading not in text:
                errors.append(f'{chapter.relative_to(COURSE)} missing {heading}')
        if not any(h in text for h in ('## ServiceWire increment', '## ServiceWire completion')):
            errors.append(f'{chapter.relative_to(COURSE)} missing ServiceWire increment or completion')
        if not any(h in text for h in ('## Observable outcomes', '## What you will be able to do')):
            errors.append(f'{chapter.relative_to(COURSE)} missing observable outcomes')
        if not any(h in text for h in ('## Ready to continue', '## Ready to complete the course', '## Readiness standard')):
            errors.append(f'{chapter.relative_to(COURSE)} missing readiness section')

for rel, minimum in [
    ('README.md', 500), ('course-book/index.md', 550), ('course-book/outcomes.md', 600),
    ('course-book/study-plan.md', 950), ('course-book/reference.md', 900),
    ('course-book/final-review.md', 850), ('course-book/final-review-solutions.md', 1800),
    ('course-book/capstone.md', 1500), ('capstone/README.md', 700),
    ('labs/README.md', 450), ('compiler-labs/README.md', 220),
]:
    page = COURSE / rel
    if page.is_file() and prose_words(page) < minimum:
        errors.append(f'{rel} too thin: {prose_words(page)} < {minimum}')

labs = sorted((COURSE / 'labs').glob('module-*'))
if len(labs) != 10:
    errors.append(f'expected 10 labs, found {len(labs)}')
for number, lab in zip(range(51, 61), labs, strict=False):
    if not lab.name.startswith(f'module-{number:02d}-'):
        errors.append(f'nonsequential laboratory: {lab.name}')
    brief = lab / 'README.md'
    if not brief.is_file():
        errors.append(f'missing {brief.relative_to(COURSE)}')
    elif prose_words(brief) < 500:
        errors.append(f'thin lab brief: {lab.name} ({prose_words(brief)} words)')
    for kind in ('starter', 'reference'):
        root = lab / kind
        for rel in ('package.json', 'tsconfig.json', 'src/index.ts'):
            if not (root / rel).is_file():
                errors.append(f'missing {(root / rel).relative_to(COURSE)}')
        if not list((root / 'tests').glob('*.test.ts')):
            errors.append(f'no tests in {root.relative_to(COURSE)}')

manifest_path = COURSE / 'compiler-labs/manifest.json'
try:
    cases = json.loads(manifest_path.read_text(encoding='utf-8')).get('cases', [])
except Exception as error:
    errors.append(f'invalid investigation manifest: {error}')
    cases = []
if len(cases) != 80:
    errors.append(f'expected 80 investigations, found {len(cases)}')
category_counts = Counter(case.get('category') for case in cases)
expected_categories = {'typecheck-pass': 40, 'typecheck-fail': 30, 'run-pass': 4, 'run-fail': 6}
if dict(category_counts) != expected_categories:
    errors.append(f'investigation category distribution {dict(category_counts)} != {expected_categories}')
ids: set[str] = set()
counts: defaultdict[int, int] = defaultdict(int)
allowed = {'typecheck-pass', 'typecheck-fail', 'run-pass', 'run-fail'}
for case in cases:
    cid = case.get('id')
    module = case.get('module')
    if not isinstance(cid, str) or not cid:
        errors.append('investigation without id')
        continue
    if cid in ids:
        errors.append(f'duplicate investigation id: {cid}')
    ids.add(cid)
    if module not in range(51, 61):
        errors.append(f'{cid}: invalid module {module}')
    else:
        counts[module] += 1
    if case.get('category') not in allowed:
        errors.append(f'{cid}: invalid category {case.get("category")}')
    for key in ('title', 'target', 'expectedPhase', 'principledRepair', 'weakRepair', 'path'):
        if not isinstance(case.get(key), str) or not case[key].strip():
            errors.append(f'{cid}: missing {key}')
    source = COURSE / 'compiler-labs' / str(case.get('path', ''))
    if not source.is_file():
        errors.append(f'{cid}: missing source {case.get("path")}')
    elif not (source.parent / 'tsconfig.json').is_file():
        errors.append(f'{cid}: missing tsconfig')
for module in range(51, 61):
    if counts[module] != 8:
        errors.append(f'module {module}: {counts[module]} investigations, expected 8')

capstone_sources = list((COURSE / 'capstone/src').glob('*.ts'))
capstone_tests = list((COURSE / 'capstone/tests').glob('*.test.ts'))
if len(capstone_sources) < 15:
    errors.append(f'capstone has only {len(capstone_sources)} source files')
if len(capstone_tests) < 10:
    errors.append(f'capstone has only {len(capstone_tests)} test files')
for source in ('app.ts','client.ts','command.ts','config.ts','discovery.ts','domain.ts','events.ts','http-shared.ts','http1.ts','http2.ts','main.ts','runtime.ts','service.ts'):
    if not (COURSE / 'capstone/src' / source).is_file():
        errors.append(f'capstone missing src/{source}')

package_names: list[str] = []
for path in COURSE.rglob('*.json'):
    if not visible(path):
        continue
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as error:
        errors.append(f'invalid JSON {path.relative_to(COURSE)}: {error}')
        continue
    if path.name == 'package.json' and isinstance(data, dict):
        name = data.get('name')
        if isinstance(name, str): package_names.append(name)
for name, count in Counter(package_names).items():
    if count > 1:
        errors.append(f'duplicate package name ({count}): {name}')

try:
    mkdocs = yaml.safe_load((COURSE / 'mkdocs.yml').read_text(encoding='utf-8'))
except Exception as error:
    errors.append(f'invalid mkdocs.yml: {error}')
    mkdocs = {}
for target in walk_nav(mkdocs.get('nav', [])) if isinstance(mkdocs, dict) else []:
    if target.startswith(('http://', 'https://')): continue
    if not (COURSE / target).is_file():
        errors.append(f'mkdocs target missing: {target}')

paragraphs: dict[str, Path] = {}
for page in COURSE.rglob('*.md'):
    if not visible(page): continue
    text = page.read_text(encoding='utf-8')
    if text.count('```') % 2:
        errors.append(f'unbalanced fence: {page.relative_to(COURSE)}')
    if re.search(r'\b(TODO|TBD|FIXME|coming soon|lorem ipsum)\b', text, flags=re.I):
        errors.append(f'unfinished marker: {page.relative_to(COURSE)}')
    anchors: set[str] = set()
    for _, heading in re.findall(r'^(#{1,6})\s+(.+?)\s*$', text, flags=re.M):
        anchor = re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-')
        if anchor in anchors:
            errors.append(f'duplicate heading anchor in {page.relative_to(COURSE)}: {heading}')
        anchors.add(anchor)
    stripped = re.sub(r'```.*?```', '', text, flags=re.S)
    for para in re.split(r'\n\s*\n', stripped):
        normalized = ' '.join(para.split())
        if len(normalized.split()) >= 55 and not normalized.startswith(('#','|')):
            prior = paragraphs.get(normalized)
            if prior and prior != page:
                errors.append(f'repeated substantial paragraph: {prior.relative_to(COURSE)} and {page.relative_to(COURSE)}')
            else:
                paragraphs[normalized] = page

for path in COURSE.rglob('*'):
    if path.is_dir() and path.name in SKIP:
        errors.append(f'generated directory present: {path.relative_to(COURSE)}')
    if path.is_symlink():
        errors.append(f'symlink present: {path.relative_to(COURSE)}')
    if path.is_file() and path.stat().st_size == 0:
        errors.append(f'zero-byte file: {path.relative_to(COURSE)}')

if errors:
    print('Course 6 audit failed:')
    for error in errors:
        print(f'  - {error}')
    raise SystemExit(1)

md_pages = sum(1 for path in COURSE.rglob('*.md') if visible(path))
ts_sources = sum(1 for path in COURSE.rglob('*.ts') if visible(path))
words = sum(prose_words(path) for path in COURSE.rglob('*.md') if visible(path))
print('Course 6 audit passed:')
print(f'  modules: {len(modules)}; labs: {len(labs)}; investigations: {len(cases)}')
print(f'  Markdown pages: {md_pages}; prose words: {words}')
print(f'  TypeScript sources: {ts_sources}; executable packages: {len(package_names)}')
