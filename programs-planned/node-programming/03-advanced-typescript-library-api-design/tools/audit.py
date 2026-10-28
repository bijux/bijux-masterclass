#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, tomllib
COURSE=Path(__file__).resolve().parents[1]
errors=[]
required=['README.md','course-book/index.md','course-book/outcomes.md','course-book/study-plan.md','course-book/reference.md','course-book/final-review.md','course-book/final-review-solutions.md','course-book/capstone.md','capstone/README.md','capstone/package.json','compiler-labs/manifest.json','mkdocs.yml']
for rel in required:
    if not (COURSE/rel).is_file(): errors.append(f'missing {rel}')
modules=sorted((COURSE/'course-book').glob('module-*'))
if len(modules)!=10: errors.append(f'expected 10 modules, found {len(modules)}')
for expected,module in enumerate(modules,start=21):
    if not module.name.startswith(f'module-{expected:02d}-'): errors.append(f'nonsequential module: {module.name}')
    for name,minimum in [('index.md',1900),('workbook.md',500),('solutions.md',620)]:
        path=module/name
        if not path.is_file(): errors.append(f'missing {path.relative_to(COURSE)}'); continue
        words=len(re.findall(r"[A-Za-z0-9_#'`.-]+",path.read_text(encoding='utf-8')))
        if words<minimum: errors.append(f'{path.relative_to(COURSE)} too thin: {words} < {minimum}')
labs=sorted((COURSE/'labs').glob('module-*'))
if len(labs)!=10: errors.append(f'expected 10 labs, found {len(labs)}')
for lab in labs:
    readme=lab/'README.md'
    if not readme.is_file(): errors.append(f'missing {readme.relative_to(COURSE)}')
    elif len(readme.read_text(encoding='utf-8').split())<300: errors.append(f'thin lab brief: {lab.name}')
    for kind in ('starter','reference'):
        root=lab/kind
        for rel in ('package.json','tsconfig.json','src/index.ts'):
            if not (root/rel).is_file(): errors.append(f'missing {(root/rel).relative_to(COURSE)}')
        if not list((root/'tests').glob('*.test.ts')): errors.append(f'no tests: {root.relative_to(COURSE)}')
manifest=json.loads((COURSE/'compiler-labs/manifest.json').read_text(encoding='utf-8'))
cases=manifest.get('cases',[])
if len(cases)!=80: errors.append(f'expected 80 investigations, found {len(cases)}')
ids=set()
for case in cases:
    cid=case.get('id'); module=case.get('module'); category=case.get('category')
    if cid in ids: errors.append(f'duplicate investigation id: {cid}')
    ids.add(cid)
    if module not in range(21,31): errors.append(f'invalid module in {cid}: {module}')
    if category not in {'typecheck-pass','typecheck-fail','run-pass','run-fail'}: errors.append(f'invalid category in {cid}: {category}')
    for key in ('title','target','principledRepair','weakRepair','path'):
        if not isinstance(case.get(key),str) or not case[key].strip(): errors.append(f'{cid} missing {key}')
    if isinstance(case.get('path'),str) and not (COURSE/'compiler-labs'/case['path']).is_file(): errors.append(f'{cid} source missing')
capstone_sources=list((COURSE/'capstone/src').glob('*.ts')); capstone_tests=list((COURSE/'capstone/tests').glob('*.test.ts'))
if len(capstone_sources)<10: errors.append(f'capstone has only {len(capstone_sources)} source files')
if len(capstone_tests)<6: errors.append(f'capstone has only {len(capstone_tests)} test files')
for package in COURSE.rglob('package.json'):
    if 'node_modules' in package.parts: continue
    try: json.loads(package.read_text(encoding='utf-8'))
    except Exception as error: errors.append(f'invalid JSON {package.relative_to(COURSE)}: {error}')
for config in COURSE.rglob('tsconfig.json'):
    if 'node_modules' in config.parts: continue
    try: json.loads(config.read_text(encoding='utf-8'))
    except Exception as error: errors.append(f'invalid tsconfig {config.relative_to(COURSE)}: {error}')
for page in COURSE.rglob('*.md'):
    if any(part in {'node_modules','dist','site'} for part in page.parts): continue
    text=page.read_text(encoding='utf-8')
    if text.count('```')%2: errors.append(f'unbalanced fence: {page.relative_to(COURSE)}')
    if re.search(r'\b(TODO|TBD|FIXME|coming soon|lorem ipsum)\b',text,re.I): errors.append(f'unfinished marker: {page.relative_to(COURSE)}')
if errors:
    print('Course 3 audit failed:')
    for error in errors: print(f'  - {error}')
    sys.exit(1)
md=sum(1 for p in COURSE.rglob('*.md') if 'node_modules' not in p.parts)
ts=sum(1 for p in COURSE.rglob('*.ts') if 'node_modules' not in p.parts)
words=sum(len(p.read_text(encoding='utf-8').split()) for p in COURSE.rglob('*.md') if 'node_modules' not in p.parts)
print('Course 3 audit passed:')
print(f'  Markdown pages: {md}')
print(f'  Markdown words: {words}')
print(f'  TypeScript sources: {ts}')
print(f'  modules: {len(modules)}; labs: {len(labs)}; investigations: {len(cases)}')
