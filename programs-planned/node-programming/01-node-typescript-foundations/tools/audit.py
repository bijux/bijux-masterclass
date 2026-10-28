#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, re, sys

COURSE=Path(__file__).resolve().parents[1]
errors: list[str]=[]

def words(path: Path) -> int:
    text=path.read_text(encoding='utf-8')
    text=re.sub(r'```.*?```',' ',text,flags=re.S)
    return len(re.findall(r"\b[\w’'-]+\b",text))

def require(condition: bool, message: str) -> None:
    if not condition: errors.append(message)

modules=sorted((COURSE/'course-book').glob('module-*'))
require(len(modules)==10,f'expected 10 modules, found {len(modules)}')
for index,module in enumerate(modules,1):
    require(module.name.startswith(f'module-{index:02d}-'),f'wrong module order: {module.name}')
    for name,minimum in [('index.md',1200),('workbook.md',250),('solutions.md',330)]:
        path=module/name
        require(path.is_file(),f'missing {path.relative_to(COURSE)}')
        if path.is_file(): require(words(path)>=minimum,f'{path.relative_to(COURSE)} has {words(path)} words; minimum {minimum}')

for name,minimum in [('index.md',1200),('outcomes.md',1000),('study-plan.md',1200),('reference.md',1800),('final-review.md',1200),('final-review-solutions.md',1200),('capstone.md',1800)]:
    path=COURSE/'course-book'/name
    require(path.is_file(),f'missing course-book/{name}')
    if path.is_file(): require(words(path)>=minimum,f'course-book/{name} has {words(path)} words; minimum {minimum}')

labs=sorted((COURSE/'labs').glob('module-*'))
require(len(labs)==10,f'expected 10 labs, found {len(labs)}')
for index,lab in enumerate(labs,1):
    require(lab.name.startswith(f'module-{index:02d}-'),f'wrong lab order: {lab.name}')
    readme=lab/'README.md'
    require(readme.is_file(),f'missing {readme.relative_to(COURSE)}')
    if readme.is_file(): require(words(readme)>=430,f'{readme.relative_to(COURSE)} has {words(readme)} words; minimum 430')
    for variant in ('starter','reference'):
        base=lab/variant
        for name in ('package.json','tsconfig.json'):
            require((base/name).is_file(),f'missing {(base/name).relative_to(COURSE)}')
        require(any((base/'src').glob('*.ts')),f'no source in {base.relative_to(COURSE)}')
        require(any((base/'tests').glob('*.test.ts')),f'no tests in {base.relative_to(COURSE)}')

cap=COURSE/'capstone'
for name in ('README.md','package.json','tsconfig.json'):
    require((cap/name).is_file(),f'missing capstone/{name}')
require(len(list((cap/'src').glob('*.ts')))>=8,'capstone source surface is incomplete')
require(len(list((cap/'tests').glob('*.test.ts')))>=5,'capstone test surface is incomplete')

manifest_path=COURSE/'compiler-labs/manifest.json'
require(manifest_path.is_file(),'missing compiler-labs/manifest.json')
if manifest_path.is_file():
    data=json.loads(manifest_path.read_text(encoding='utf-8'))
    cases=data.get('cases',[])
    require(len(cases)==80,f'expected 80 investigations, found {len(cases)}')
    ids=[case.get('id') for case in cases]
    require(len(ids)==len(set(ids)),'duplicate investigation id')
    for module in range(1,11):
        require(sum(case.get('module')==module for case in cases)==8,f'module {module} does not have 8 investigations')
    allowed={'typecheck-pass','typecheck-fail','run-pass','run-fail'}
    for case in cases:
        require(case.get('category') in allowed,f"invalid category for {case.get('id')}")
        path=COURSE/'compiler-labs'/str(case.get('path'))
        require(path.is_file(),f'missing investigation source {path.relative_to(COURSE)}')
        require((path.parent/'tsconfig.json').is_file(),f'missing investigation tsconfig for {case.get("id")}')
        for field in ('target','principledRepair','weakRepair'):
            require(isinstance(case.get(field),str) and len(case[field].strip())>=20,f'{case.get("id")} has weak {field}')

for path in COURSE.rglob('*'):
    if path.is_file():
        require(path.stat().st_size>0,f'zero-byte file: {path.relative_to(COURSE)}')
        if path.suffix in {'.md','.ts','.mjs','.py','.json','.toml','.yml','.yaml'} or path.name in {'Makefile'}:
            text=path.read_text(encoding='utf-8')
            if path.suffix=='.md':
                require(text.count('```')%2==0,f'unbalanced fence: {path.relative_to(COURSE)}')
            if 'compiler-labs' not in path.parts and 'tools' not in path.parts:
                for marker in ('TODO','TBD','FIXME','coming soon','lorem ipsum'):
                    require(marker.lower() not in text.lower(),f'unfinished marker {marker!r} in {path.relative_to(COURSE)}')

if errors:
    print('Course audit failed:')
    for error in errors: print(f'  - {error}')
    sys.exit(1)
print('Course audit passed:')
print(f'  modules: {len(modules)}')
print(f'  labs: {len(labs)}')
print('  investigations: 80')
print(f'  Markdown pages: {len(list(COURSE.rglob("*.md")))}')
print(f'  TypeScript sources: {len(list(COURSE.rglob("*.ts")))}')
