#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from collections import defaultdict, Counter
import hashlib, json, re, tomllib, sys

ROOT=Path(__file__).resolve().parents[1]
COURSES=[
 ('01-rust-foundations',range(1,11),60),('02-rust-ownership-lifetimes-memory',range(11,21),80),
 ('03-rust-traits-generics-architectural-design',range(21,31),80),('04-rust-functional-programming',range(31,41),80),
 ('05-rust-metaprogramming',range(41,51),80),('06-rust-systems-programming',range(51,61),80),
 ('07-rust-concurrency-parallelism',range(61,71),80),('08-rust-async-networked-services',range(71,81),80),
 ('09-rust-performance-production-engineering',range(81,91),80),('10-rust-advanced-mastery',range(91,101),80),
]
errors=[]
def fail(x): errors.append(x)
def words(t): return len(re.findall(r"\b[\w'-]+\b",re.sub(r'```.*?```','',t,flags=re.S)))
def fences_ok(t): return len(re.findall(r'(?m)^\s*```',t))%2==0 and len(re.findall(r'(?m)^\s*~~~',t))%2==0
expected=[c[0] for c in COURSES]
actual=[p.name for p in sorted(ROOT.glob('[0-9][0-9]-rust-*')) if p.is_dir()]
if actual!=expected: fail(f'course directories differ: expected {expected}, found {actual}')
for required in ('README.md','START_HERE.md','REASONING_MODEL.md','SKILL_MAP.md','COURSE_MAP.md','PROGRESS.md','SOURCE_NOTES.md','GLOSSARY.md','Makefile','mkdocs.yml'):
    if not (ROOT/required).is_file(): fail(f'missing root reader surface: {required}')
# Reader-route numbering must expose every module exactly once.
progress_numbers=[int(x) for x in re.findall(r'(?m)^- \[ \] \*\*(\d{2,3})\.',(ROOT/'PROGRESS.md').read_text())]
if progress_numbers!=list(range(1,101)): fail(f'progress sequence differs: {progress_numbers}')
nav_numbers=[int(x) for x in re.findall(r"(?m)^\s*- '(\d{1,3}) —",(ROOT/'mkdocs.yml').read_text())]
if nav_numbers!=list(range(1,101)): fail(f'MkDocs module sequence differs: {nav_numbers}')
all_modules=[]; compiler_ids=set(); packages={}; normalized={}; substantial=defaultdict(list)
for cname,nums,expected_cases in COURSES:
    c=ROOT/cname
    for req in ('README.md','Cargo.toml','Makefile','rust-toolchain.toml','clippy.toml','course-book/index.md','course-book/study-plan.md','course-book/capstone.md','course-book/reference.md','course-book/final-review.md','capstone/Cargo.toml','capstone/README.md','compiler-labs/README.md','compiler-labs/manifest.json'):
        if not (c/req).exists(): fail(f'{cname}: missing {req}')
    found=[]
    for chapter in sorted((c/'course-book').glob('module-*/index.md'), key=lambda p: int(re.match(r'module-(\d+)-', p.parent.name).group(1))):
        m=re.match(r'module-(\d+)-',chapter.parent.name)
        if not m: fail(f'invalid module directory {chapter.parent.relative_to(ROOT)}'); continue
        n=int(m.group(1)); found.append(n); all_modules.append(n)
        t=chapter.read_text()
        if words(t)<1600: fail(f'module {n} chapter thin: {words(t)}')
        if len(re.findall(r'(?m)^# ',t))!=1: fail(f'module {n} chapter needs one H1')
        for h in ('The question','Why this comes now','What you will be able to do','Core model','Use the idea in a complete program','Practice sequence','Ready to continue','Primary Rust references','Continue'):
            if f'## {h}' not in t: fail(f'module {n} missing {h}')
        if f'Module {n} of 100' not in t or f'**{n}/100**' not in t: fail(f'module {n} stale progress marker')
        for fn,minw in (('workbook.md',850),('solutions.md',850)):
            p=chapter.parent/fn
            if not p.exists(): fail(f'module {n} missing {fn}'); continue
            x=p.read_text()
            if words(x)<minw: fail(f'module {n} {fn} thin: {words(x)}')
            if len(re.findall(r'(?m)^# ',x))!=1: fail(f'module {n} {fn} needs one H1')
        wb=(chapter.parent/'workbook.md').read_text()
        for h in ('Part 1 — Predict','Part 2 — Diagnose and repair','Part 3 — Focused exercises','Part 4 — Independent laboratory','Part 5 — Capstone transfer','Part 6 — Reconstruct and defend'):
            if f'## {h}' not in wb: fail(f'module {n} workbook missing {h}')
    if sorted(found)!=list(nums): fail(f'{cname}: expected {list(nums)}, found {sorted(found)}')
    labs=sorted(p for p in (c/'labs').glob('module-*') if p.is_dir())
    if len(labs)!=10: fail(f'{cname}: expected 10 labs, found {len(labs)}')
    for lab in labs:
        for req in ('README.md','starter/Cargo.toml','solution/Cargo.toml'):
            if not (lab/req).exists(): fail(f'{lab.relative_to(ROOT)} missing {req}')
        if (lab/'README.md').exists() and words((lab/'README.md').read_text())<600: fail(f'{lab.relative_to(ROOT)}/README.md thin')
        for v in ('starter','solution'):
            if not list((lab/v).rglob('*.rs')): fail(f'{lab.relative_to(ROOT)}/{v} has no Rust source')
    guide=(c/'course-book/capstone.md').read_text()
    if words(guide)<3200: fail(f'{cname}: capstone guide thin: {words(guide)}')
    if words((c/'capstone/README.md').read_text())<500: fail(f'{cname}: capstone README thin')
    study=(c/'course-book/study-plan.md').read_text()
    days=re.findall(r'(?m)^## Day (\d+) — ',study)
    if days!=[str(i) for i in range(1,11)]: fail(f'{cname}: study days differ: {days}')
    cases=json.loads((c/'compiler-labs/manifest.json').read_text())['cases']
    if len(cases)!=expected_cases: fail(f'{cname}: expected {expected_cases} investigations, found {len(cases)}')
    for case in cases:
        cid=str(case.get('id','')).strip()
        if not cid: fail(f'{cname}: case missing id')
        elif cid in compiler_ids: fail(f'duplicate case id {cid}')
        else: compiler_ids.add(cid)
        for field in ('target_rule','intended_cause','principled_repair','weak_repair'):
            if not str(case.get(field,'')).strip(): fail(f'{cid}: empty {field}')
        target=c/case['path']
        if not target.exists(): fail(f'{cid}: missing path {case["path"]}')
if all_modules!=list(range(1,101)): fail(f'module sequence differs: {all_modules}')
# TOML and package/path checks
for p in ROOT.rglob('*.toml'):
    try: data=tomllib.loads(p.read_text())
    except Exception as e: fail(f'invalid TOML {p.relative_to(ROOT)}: {e}'); continue
    package=data.get('package')
    if isinstance(package,dict) and package.get('name'):
        name=package['name']
        if name in packages: fail(f'duplicate package {name}: {packages[name]} and {p.relative_to(ROOT)}')
        packages[name]=p.relative_to(ROOT)
    for key in ('dependencies','dev-dependencies','build-dependencies'):
        table=data.get(key,{})
        if not isinstance(table,dict): continue
        for dep,spec in table.items():
            if isinstance(spec,dict) and 'path' in spec and not (p.parent/spec['path']).resolve().exists():
                fail(f'{p.relative_to(ROOT)} unresolved path dependency {dep} -> {spec["path"]}')
# Markdown quality and residue
for p in ROOT.rglob('*.md'):
    t=p.read_text()
    rel=p.relative_to(ROOT)
    if not fences_ok(t): fail(f'unbalanced Markdown fence: {rel}')
    # One H1, unique headings, and no hierarchy jumps keep rendered navigation stable.
    headings=[]; in_code=False; previous_level=0
    for line_no,line in enumerate(t.splitlines(),1):
        if line.strip().startswith('```'):
            in_code=not in_code; continue
        if in_code: continue
        m=re.match(r'^(#{1,6})\s+(.+)$',line)
        if not m: continue
        level=len(m.group(1)); title=m.group(2).strip()
        headings.append((title,line_no,level))
        if previous_level and level>previous_level+1: fail(f'heading jump in {rel}:{line_no}')
        previous_level=level
    if sum(1 for _,_,level in headings if level==1)!=1: fail(f'{rel} needs exactly one H1 outside code')
    counts=Counter(title for title,_,_ in headings)
    for title,count in counts.items():
        if count>1: fail(f'duplicate heading in {rel}: {title!r}')
    # Exact repeated substantial blocks inside one page are editorial defects, not depth.
    seen_blocks={}
    for block in re.split(r'\n\s*\n',re.sub(r'```.*?```','',t,flags=re.S)):
        block_norm=re.sub(r'\s+',' ',block.strip())
        if len(block_norm.split())<12 or block_norm.startswith('#'): continue
        if block_norm in seen_blocks: fail(f'repeated substantial block in {rel}: {block_norm[:80]!r}')
        seen_blocks[block_norm]=True
    if re.search(r'Your answer must include:\s*(?:\n\s*)?#{1,6}\s',t): fail(f'dangling answer prompt in {rel}')
    norm=re.sub(r'\s+',' ',t).strip()
    h=hashlib.sha256(norm.encode()).hexdigest()
    if h in normalized: fail(f'exact duplicate Markdown: {normalized[h]} and {rel}')
    normalized[h]=rel
    if re.search(r'(?i)\b(?:ninety-module|courses? 1.?9|module \d+ of 90)\b',t): fail(f'stale 90-module wording in {rel}')
    if re.search(r'(?m)^\s*(?:[-*]\s*)?(?:TODO|TBD|FIXME)\s*(?::|—|-|$)',t): fail(f'unfinished marker in {rel}')
    for para in re.split(r'\n\s*\n',re.sub(r'```.*?```','',t,flags=re.S)):
        q=re.sub(r'\s+',' ',re.sub(r'[#*`>\[\]()_|]',' ',para)).strip().lower()
        if len(q.split())>=45: substantial[q].append(rel)
for q,files in substantial.items():
    uniq=list(dict.fromkeys(files))
    if len(uniq)>=8: fail(f'substantial paragraph repeated in {len(uniq)} files: {str(uniq[:3])}')
# Unsafe policy: only Course 6, Course 7 SPSC proof, and Course 10 InlineBatch proof.
allowed_unsafe=('06-rust-systems-programming/','07-rust-concurrency-parallelism/labs/module-08-spsc-ring/solution/','10-rust-advanced-mastery/capstone/src/inline_batch.rs','10-rust-advanced-mastery/labs/module-06-inline-batch/solution/')
for p in ROOT.rglob('*.rs'):
    rel=p.relative_to(ROOT).as_posix(); t=p.read_text(errors='ignore')
    if re.search(r'\bunsafe\s*(?:\{|fn\b|impl\b|trait\b|extern\b)',t) and not any(rel.startswith(a) for a in allowed_unsafe):
        if 'compiler-labs/' not in rel: fail(f'unsafe Rust outside approved proof surfaces: {rel}')
# residue
for p in ROOT.rglob('*'):
    if p.name in {'.DS_Store','__MACOSX'} or p.name=='target' or '__pycache__' in p.parts: fail(f'generated/platform residue: {p.relative_to(ROOT)}')
print('Rust Courses 1–10 curriculum audit')
print('  modules:',len(all_modules))
print('  investigations:',len(compiler_ids))
print('  Cargo packages:',len(packages))
print('  Markdown pages:',len(list(ROOT.rglob('*.md'))))
for e in errors: print('ERROR',e)
raise SystemExit(1 if errors else 0)
