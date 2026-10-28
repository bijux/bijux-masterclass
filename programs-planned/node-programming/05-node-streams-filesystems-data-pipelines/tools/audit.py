#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json
import re
import sys

COURSE = Path(__file__).resolve().parents[1]
errors: list[str] = []


def prose_words(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9_#'`.-]+", text))


required = [
    'README.md',
    'course-book/index.md',
    'course-book/outcomes.md',
    'course-book/study-plan.md',
    'course-book/reference.md',
    'course-book/final-review.md',
    'course-book/final-review-solutions.md',
    'course-book/capstone.md',
    'capstone/README.md',
    'capstone/package.json',
    'compiler-labs/manifest.json',
    'labs/README.md',
    'mkdocs.yml',
    'package.json',
    'tsconfig.base.json',
]
for rel in required:
    if not (COURSE / rel).is_file():
        errors.append(f'missing {rel}')

# Course-book depth and sequence.
modules = sorted((COURSE / 'course-book').glob('module-*'))
if len(modules) != 10:
    errors.append(f'expected 10 modules, found {len(modules)}')
for expected, module in enumerate(modules, start=41):
    if not module.name.startswith(f'module-{expected:02d}-'):
        errors.append(f'nonsequential module: {module.name}')
    for name, minimum in [('index.md', 1750), ('workbook.md', 700), ('solutions.md', 1150)]:
        path = module / name
        if not path.is_file():
            errors.append(f'missing {path.relative_to(COURSE)}')
            continue
        words = prose_words(path)
        if words < minimum:
            errors.append(f'{path.relative_to(COURSE)} too thin: {words} < {minimum}')
    chapter = module / 'index.md'
    if chapter.is_file():
        text = chapter.read_text(encoding='utf-8')
        expected_headings = [
            '## The governing question',
            '## Why this module comes now',
            '## Observable outcomes',
            '## The module ledger',
            '## Decision procedure',
            '## Common wrong models',
            '## Apply the mechanism in FlowLedger',
            '## Independent transfer',
            '## Readiness standard',
        ]
        for heading in expected_headings:
            if heading not in text:
                errors.append(f'{chapter.relative_to(COURSE)} missing heading: {heading}')

for rel, minimum in [
    ('course-book/capstone.md', 2200),
    ('course-book/final-review.md', 900),
    ('course-book/final-review-solutions.md', 1800),
    ('course-book/study-plan.md', 1200),
    ('course-book/reference.md', 900),
]:
    path = COURSE / rel
    if path.is_file() and prose_words(path) < minimum:
        errors.append(f'{rel} too thin: {prose_words(path)} < {minimum}')

# Labs are independent products with executable starter/reference packages.
labs = sorted((COURSE / 'labs').glob('module-*'))
if len(labs) != 10:
    errors.append(f'expected 10 labs, found {len(labs)}')
for expected, lab in enumerate(labs, start=41):
    if not lab.name.startswith(f'module-{expected:02d}-'):
        errors.append(f'nonsequential laboratory: {lab.name}')
    readme = lab / 'README.md'
    if not readme.is_file():
        errors.append(f'missing {readme.relative_to(COURSE)}')
    elif prose_words(readme) < 550:
        errors.append(f'thin lab brief: {lab.name} ({prose_words(readme)} words)')
    for kind in ('starter', 'reference'):
        root = lab / kind
        for rel in ('package.json', 'tsconfig.json', 'src/index.ts'):
            if not (root / rel).is_file():
                errors.append(f'missing {(root / rel).relative_to(COURSE)}')
        tests = list((root / 'tests').glob('*.test.ts'))
        if not tests:
            errors.append(f'no tests: {root.relative_to(COURSE)}')

# Compiler/runtime cases.
manifest_path = COURSE / 'compiler-labs/manifest.json'
if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    cases = manifest.get('cases', [])
else:
    cases = []
if len(cases) != 80:
    errors.append(f'expected 80 investigations, found {len(cases)}')
ids: set[str] = set()
module_counts: defaultdict[int, int] = defaultdict(int)
allowed_categories = {'typecheck-pass', 'typecheck-fail', 'run-pass', 'run-fail'}
for case in cases:
    cid = case.get('id')
    module = case.get('module')
    category = case.get('category')
    if not isinstance(cid, str) or not cid:
        errors.append('investigation without id')
        continue
    if cid in ids:
        errors.append(f'duplicate investigation id: {cid}')
    ids.add(cid)
    if module not in range(41, 51):
        errors.append(f'invalid module in {cid}: {module}')
    else:
        module_counts[module] += 1
    if category not in allowed_categories:
        errors.append(f'invalid category in {cid}: {category}')
    for key in ('title', 'target', 'expectedPhase', 'principledRepair', 'weakRepair', 'path'):
        if not isinstance(case.get(key), str) or not case[key].strip():
            errors.append(f'{cid} missing {key}')
    if isinstance(case.get('path'), str):
        source = COURSE / 'compiler-labs' / case['path']
        if not source.is_file():
            errors.append(f'{cid} source missing: {case["path"]}')
        elif not (source.parent / 'tsconfig.json').is_file():
            errors.append(f'{cid} tsconfig missing')
for module in range(41, 51):
    if module_counts[module] != 8:
        errors.append(f'module {module} has {module_counts[module]} investigations, expected 8')

# Capstone executable surface.
capstone_sources = list((COURSE / 'capstone/src').glob('*.ts'))
capstone_tests = list((COURSE / 'capstone/tests').glob('*.test.ts'))
if len(capstone_sources) < 10:
    errors.append(f'capstone has only {len(capstone_sources)} source files')
if len(capstone_tests) < 7:
    errors.append(f'capstone has only {len(capstone_tests)} test files')
for required_source in ('main.ts', 'command.ts', 'domain.ts', 'streams.ts', 'pipeline.ts', 'transaction.ts', 'child.ts'):
    if not (COURSE / 'capstone/src' / required_source).is_file():
        errors.append(f'capstone missing src/{required_source}')

# Parse JSON surfaces.
for path in COURSE.rglob('package.json'):
    if any(part in {'node_modules', 'dist', 'site'} for part in path.parts):
        continue
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as error:
        errors.append(f'invalid JSON {path.relative_to(COURSE)}: {error}')
for path in COURSE.rglob('tsconfig*.json'):
    if any(part in {'node_modules', 'dist', 'site'} for part in path.parts):
        continue
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as error:
        errors.append(f'invalid tsconfig {path.relative_to(COURSE)}: {error}')

# Reader-facing Markdown integrity and exact substantial repetition.
paragraphs: dict[str, Path] = {}
for page in COURSE.rglob('*.md'):
    if any(part in {'node_modules', 'dist', 'site'} for part in page.parts):
        continue
    text = page.read_text(encoding='utf-8')
    if text.count('```') % 2:
        errors.append(f'unbalanced fence: {page.relative_to(COURSE)}')
    if re.search(r'\b(TODO|TBD|FIXME|coming soon|lorem ipsum)\b', text, re.I):
        errors.append(f'unfinished marker: {page.relative_to(COURSE)}')
    headings: set[str] = set()
    for heading in re.findall(r'^(#{1,6})\s+(.+?)\s*$', text, flags=re.M):
        normalized = re.sub(r'[^a-z0-9]+', '-', heading[1].lower()).strip('-')
        if normalized in headings:
            errors.append(f'duplicate heading anchor in {page.relative_to(COURSE)}: {heading[1]}')
        headings.add(normalized)
    stripped = re.sub(r'```.*?```', '', text, flags=re.S)
    for para in re.split(r'\n\s*\n', stripped):
        normalized = ' '.join(para.split())
        if len(normalized.split()) >= 45 and not normalized.startswith(('#', '|')):
            prior = paragraphs.get(normalized)
            if prior and prior != page:
                errors.append(
                    f'repeated substantial paragraph: {prior.relative_to(COURSE)} and {page.relative_to(COURSE)}'
                )
            else:
                paragraphs[normalized] = page

if errors:
    print('Course 5 audit failed:')
    for error in errors:
        print(f'  - {error}')
    sys.exit(1)

md_pages = sum(1 for p in COURSE.rglob('*.md') if 'node_modules' not in p.parts)
ts_sources = sum(1 for p in COURSE.rglob('*.ts') if 'node_modules' not in p.parts)
words = sum(prose_words(p) for p in COURSE.rglob('*.md') if 'node_modules' not in p.parts)
print('Course 5 audit passed:')
print(f'  Markdown pages: {md_pages}')
print(f'  Markdown prose words: {words}')
print(f'  TypeScript sources: {ts_sources}')
print(f'  modules: {len(modules)}; labs: {len(labs)}; investigations: {len(cases)}')
