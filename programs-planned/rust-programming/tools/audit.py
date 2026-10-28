#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import hashlib, json, re, tomllib

ROOT=Path(__file__).resolve().parents[1]
COURSES=[
 ('01-rust-foundations',range(1,11),60,3000,1400,900),
 ('02-rust-ownership-lifetimes-memory',range(11,21),80,3000,1400,850),
 ('03-rust-traits-generics-architectural-design',range(21,31),80,2300,900,850),
 ('04-rust-functional-programming',range(31,41),80,1800,1400,900),
 ('05-rust-metaprogramming',range(41,51),80,1800,950,1100),
 ('06-rust-systems-programming',range(51,61),80,1800,650,650),
 ('07-rust-concurrency-parallelism',range(61,71),80,1500,850,650),
 ('08-rust-async-networked-services',range(71,81),80,1600,450,400),
 ('09-rust-performance-production-engineering',range(81,91),80,1800,800,700),
]
errors=[]
CHAPTER_SPINE=[
 'The question','Why this comes now','What you will be able to do','Core model',
 'Use the idea in a complete program','Practice sequence','Ready to continue',
 'Primary Rust references','Continue',
]
WORKBOOK_SPINE=[
 'Part 1 — Predict','Part 2 — Diagnose and repair','Part 3 — Focused exercises',
 'Part 4 — Independent laboratory','Part 5 — Capstone transfer',
 'Part 6 — Reconstruct and defend',
]
VALID_COMPILER_OUTCOMES={'compile-pass','compile-fail','run-pass','run-fail','manual-review'}

def fail(message:str)->None: errors.append(message)
def words(text:str)->int: return len(re.findall(r"\b[\w'-]+\b",text))
def fences_ok(text:str)->bool:
    return len(re.findall(r'(?m)^\s*```',text))%2==0 and len(re.findall(r'(?m)^\s*~~~',text))%2==0

def dep_tables(data:dict):
    for key in ('dependencies','dev-dependencies','build-dependencies'):
        table=data.get(key,{})
        if isinstance(table,dict): yield key,table
    for target_name,target in (data.get('target',{}) or {}).items():
        if isinstance(target,dict):
            for key in ('dependencies','dev-dependencies','build-dependencies'):
                table=target.get(key,{})
                if isinstance(table,dict): yield f'target.{target_name}.{key}',table

expected_dirs=[c[0] for c in COURSES]
actual_dirs=[p.name for p in sorted(ROOT.glob('[0-9][0-9]-*')) if p.is_dir()]
if actual_dirs!=expected_dirs: fail(f'course directories differ: expected {expected_dirs}, found {actual_dirs}')

for required in ('README.md','START_HERE.md','REASONING_MODEL.md','SKILL_MAP.md','COURSE_MAP.md','PROGRESS.md','SOURCE_NOTES.md','GLOSSARY.md','Makefile','mkdocs.yml'):
    if not (ROOT/required).is_file(): fail(f'missing root reader surface: {required}')

all_modules=[]; compiler_ids=set(); package_names={}; normalized={}; substantial=defaultdict(list)
allowed_versions={'proc-macro2':'=1.0.107','quote':'=1.0.47','syn':'=3.0.3'}
allowed_course8_versions={'tokio':'=1.53.1','tokio-util':'=0.7.19','bytes':'=1.12.1','futures-util':'=0.3.33','hyper':'=1.8.0','hyper-util':'=0.1.20','http-body-util':'=0.1.4'}
allowed_course9_versions={'criterion':'=0.8.2','bytes':'=1.12.1','tokio':'=1.53.1','tracing':'=0.1.44','tracing-subscriber':'=0.3.23','hyper':'=1.8.0','hyper-util':'=0.1.20','http-body-util':'=0.1.4'}

for course_name,module_range,expected_cases,min_chapter,min_workbook,min_solution in COURSES:
    course=ROOT/course_name
    for required in ('README.md','Cargo.toml','Makefile','rust-toolchain.toml','clippy.toml','course-book/index.md','course-book/study-plan.md','course-book/capstone.md','course-book/reference.md','course-book/final-review.md','capstone/Cargo.toml','capstone/README.md'):
        if not (course/required).exists(): fail(f'{course_name}: missing {required}')
    found=[]
    modules=sorted((course/'course-book').glob('module-*/index.md'))
    for chapter in modules:
        m=re.match(r'module-(\d+)-',chapter.parent.name)
        if not m: fail(f'invalid module directory: {chapter.parent.relative_to(ROOT)}'); continue
        n=int(m.group(1)); found.append(n); all_modules.append(n)
        text=chapter.read_text(errors='strict')
        if words(text)<min_chapter: fail(f'module {n:02d} chapter thin: {words(text)} < {min_chapter}')
        if len(re.findall(r'(?m)^# ',text))!=1: fail(f'module {n:02d} chapter must have one H1')
        h2=re.findall(r'(?m)^## (.+)$',text)
        if h2!=CHAPTER_SPINE: fail(f'module {n:02d} chapter spine differs: {h2}')
        outcome_body=text.split('## What you will be able to do',1)[1].split('## Core model',1)[0]
        if len(re.findall(r'(?m)^- ',outcome_body))<5: fail(f'module {n:02d} chapter needs at least five observable outcomes')
        continue_body=text.split('## Continue',1)[1]
        for needle in ('workbook.md','solutions.md','../../labs/','../capstone.md'):
            if needle not in continue_body: fail(f'module {n:02d} Continue section omits {needle}')
        if f'**{n}/90**' not in text or 'Module %d of 90'%n not in text:
            fail(f'module {n:02d} has stale/missing ninety-module marker')
        for name,minimum in (('workbook.md',min_workbook),('solutions.md',min_solution)):
            p=chapter.parent/name
            if not p.is_file(): fail(f'module {n:02d} missing {name}'); continue
            t=p.read_text(errors='strict')
            if words(t)<minimum: fail(f'module {n:02d} {name} thin: {words(t)} < {minimum}')
            if len(re.findall(r'(?m)^# ',t))!=1: fail(f'module {n:02d} {name} must have one H1')
            if name=='workbook.md':
                workbook_h2=re.findall(r'(?m)^## (.+)$',t)
                if workbook_h2!=WORKBOOK_SPINE: fail(f'module {n:02d} workbook spine differs: {workbook_h2}')
                for needle in ('index.md','../capstone.md','solutions.md'):
                    if needle not in '\n'.join(t.splitlines()[:8]): fail(f'module {n:02d} workbook navigation omits {needle}')
            else:
                for needle in ('workbook.md','index.md','../capstone.md'):
                    if needle not in '\n'.join(t.splitlines()[:8]): fail(f'module {n:02d} solutions navigation omits {needle}')
    if found!=list(module_range): fail(f'{course_name}: expected {list(module_range)}, found {found}')

    labs=sorted(p for p in (course/'labs').glob('module-*') if p.is_dir())
    if len(labs)!=10: fail(f'{course_name}: expected 10 labs, found {len(labs)}')
    for lab in labs:
        for required in ('README.md','starter/Cargo.toml','solution/Cargo.toml'):
            if not (lab/required).exists(): fail(f'{lab.relative_to(ROOT)} missing {required}')
        readme=lab/'README.md'
        if readme.is_file():
            lab_text=readme.read_text(errors='strict')
            if words(lab_text)<300: fail(f'{readme.relative_to(ROOT)} too thin for independent use')
            if len(re.findall(r'(?m)^## Product$',lab_text))!=1: fail(f'{readme.relative_to(ROOT)} must contain exactly one Product section')
            if 'START_HERE.md#laboratory-method' not in lab_text: fail(f'{readme.relative_to(ROOT)} does not link the common laboratory method')
            if 'solution/' not in lab_text: fail(f'{readme.relative_to(ROOT)} does not explain reference comparison')
        for variant in ('starter','solution'):
            if not list((lab/variant).rglob('*.rs')): fail(f'{lab.relative_to(ROOT)}/{variant} has no Rust source')

    cap=course/'capstone'
    if not list((cap/'src').glob('*.rs')): fail(f'{course_name}: capstone missing src/*.rs')
    if not list((cap/'tests').glob('*.rs')): fail(f'{course_name}: capstone missing integration tests')
    if words((course/'course-book/capstone.md').read_text(errors='strict'))<2500:
        fail(f'{course_name}: capstone engineering guide is too thin')

    compiler_readme=course/'compiler-labs/README.md'
    if not compiler_readme.is_file() or words(compiler_readme.read_text(errors='strict'))<120:
        fail(f'{course_name}: compiler-labs/README.md is missing or too thin')
    study=(course/'course-book/study-plan.md').read_text(errors='strict')
    days=re.findall(r'(?m)^## Day (\d+) — ',study)
    if days!=[str(i) for i in range(1,11)]: fail(f'{course_name}: study plan must contain ordered Days 1..10, found {days}')
    overview=(course/'course-book/index.md').read_text(errors='strict')
    if '## What you will be able to do' not in overview: fail(f'{course_name}: course overview missing outcomes')
    else:
        outcome_section=overview.split('## What you will be able to do',1)[1].split('## ',1)[0]
        if len(re.findall(r'(?m)^- ',outcome_section))<12: fail(f'{course_name}: course overview needs at least twelve course outcomes')

    manifest=course/'compiler-labs/manifest.json'
    try: cases=json.loads(manifest.read_text())['cases']
    except Exception as exc: fail(f'{manifest.relative_to(ROOT)} invalid: {exc}'); cases=[]
    if len(cases)!=expected_cases: fail(f'{course_name}: expected {expected_cases} compiler cases, found {len(cases)}')
    for case in cases:
        cid=str(case.get('id','')).strip()
        if not cid: fail(f'{course_name}: compiler case missing id')
        elif cid in compiler_ids: fail(f'duplicate compiler id {cid}')
        else: compiler_ids.add(cid)
        outcome=case.get('outcome')
        if outcome not in VALID_COMPILER_OUTCOMES: fail(f'{cid}: invalid outcome category {outcome!r}')
        compile_expected='fail' if outcome=='compile-fail' else 'pass'
        if case.get('expected') != compile_expected:
            fail(f'{cid}: expected={case.get("expected")!r} conflicts with outcome={outcome!r}')
        if bool(case.get('run')) != (outcome in {'run-pass','run-fail'}):
            fail(f'{cid}: run flag conflicts with outcome={outcome!r}')
        for field in ('target_rule','intended_cause','principled_repair','weak_repair'):
            if not str(case.get(field,'')).strip(): fail(f'{cid}: empty {field}')
        generic_repair='Apply the smallest change that satisfies the stated language rule without weakening the API contract.'
        generic_weak='Avoid cloning, broadening visibility, erasing types, or deleting behavior merely to obtain compilation.'
        if case.get('principled_repair')==generic_repair or case.get('weak_repair')==generic_weak:
            fail(f'{cid}: generic compiler-lab repair metadata was not replaced')
        src=course/str(case.get('path','')); mode=case.get('mode','rustc')
        if mode=='rustc' and (not src.is_file() or src.suffix!='.rs'): fail(f'{cid}: missing Rust source {src}')
        elif mode=='cargo' and (not src.is_dir() or not (src/'Cargo.toml').is_file()): fail(f'{cid}: missing Cargo fixture {src}')
        elif mode not in {'rustc','cargo'}: fail(f'{cid}: invalid mode {mode}')
        if mode=='rustc' and src.is_file():
            specimen_text=src.read_text(errors='strict').lower()
            for answer_marker in ('specimen-outcome:','diagnostic-contract:','expected to compile','expected to fail'):
                if answer_marker in specimen_text: fail(f'{cid}: learner specimen reveals answer through {answer_marker!r}')

if sorted(all_modules)!=list(range(1,91)): fail(f'global module sequence is not 1..90: {sorted(all_modules)}')
progress=(ROOT/'PROGRESS.md').read_text(errors='strict')
if len(re.findall(r'(?m)^- \[ \] \*\*\d{2}\.',progress))!=90: fail('PROGRESS.md must contain exactly 90 checkboxes')

retired=('publication-candidate','evidence gate','review tier','submission package','coming soon','lorem ipsum','proof transcript')
for p in ROOT.rglob('*.md'):
    rel=p.relative_to(ROOT); text=p.read_text(errors='strict'); lower=text.lower()
    if not text.strip(): fail(f'empty Markdown: {rel}')
    if not fences_ok(text): fail(f'unbalanced Markdown fences: {rel}')
    headings=[]; fence_marker=None
    for line_number,line in enumerate(text.splitlines(),1):
        marker_match=re.match(r'^\s*(```|~~~)',line)
        if marker_match:
            marker=marker_match.group(1)
            if fence_marker is None: fence_marker=marker
            elif fence_marker==marker: fence_marker=None
            continue
        if fence_marker is not None: continue
        heading_match=re.match(r'^(#{1,6})\s+(.+)',line)
        if heading_match: headings.append((line_number,len(heading_match.group(1)),heading_match.group(2)))
    h1=[heading for heading in headings if heading[1]==1]
    if len(h1)!=1: fail(f'{rel} must contain exactly one H1, found {len(h1)}')
    if re.search(r'`(?:RF|OLM)-M\d{2}-O\d+`',text): fail(f'{rel} exposes retired internal outcome identifiers')
    if '.;' in text: fail(f'{rel} contains generated double punctuation .;')
    # No empty reader sections. Parent sections count the prose in their nested subsections.
    source_lines=text.splitlines()
    for idx,(line_no,level,title) in enumerate(headings):
        if level==1: continue
        end=len(source_lines)
        for next_line,next_level,_ in headings[idx+1:]:
            if next_level<=level:
                end=next_line-1; break
        body='\n'.join(source_lines[line_no:end])
        body='\n'.join(line for line in body.splitlines() if not re.match(r'^#{2,6}\s+',line))
        if words(body)<5: fail(f'{rel}:{line_no} section {title!r} is empty or only a label')
    if rel.name!='study-plan.md':
        names=[title.strip().lower() for _,level,title in headings if level>=2 and title.strip().lower()!='decision rule']
        duplicates={name for name in names if names.count(name)>1}
        if duplicates: fail(f'{rel} has duplicate heading anchors: {sorted(duplicates)}')
    for previous,current in zip(headings,headings[1:]):
        if current[1]>previous[1]+1:
            fail(f'{rel}:{current[0]} heading level jumps from H{previous[1]} to H{current[1]}')
            break
    if '/mnt/data/' in text: fail(f'construction path in {rel}')
    lines=text.splitlines()
    for metadata_key in ('hide:','search:'):
        if any(line.strip()==metadata_key for line in lines[1:]):
            fail(f'misplaced MkDocs front matter in {rel}: {metadata_key}')
    for phrase in retired:
        if phrase in lower: fail(f'{rel} contains retired/internal phrase {phrase!r}')
    if re.search(r'(?m)^\s*(?:[-*]\s*)?(?:TODO|TBD|FIXME)\s*(?::|—|-|$)',text): fail(f'unfinished marker in {rel}')
    norm=re.sub(r'\s+',' ',text).strip(); digest=hashlib.sha256(norm.encode()).hexdigest()
    if digest in normalized: fail(f'exact duplicate Markdown: {rel} and {normalized[digest]}')
    else: normalized[digest]=rel
    for block in re.split(r'\n\s*\n',text):
        b=' '.join(block.split())
        if len(b.split())>=45 and not b.startswith('```'): substantial[b].append(rel)
for para,paths in substantial.items():
    if len(paths)>10: fail(f'substantial paragraph repeated {len(paths)} times: {str(paths[0])}: {para[:100]}…')

for manifest in ROOT.rglob('Cargo.toml'):
    rel=manifest.relative_to(ROOT)
    try: data=tomllib.loads(manifest.read_text())
    except Exception as exc: fail(f'invalid TOML {rel}: {exc}'); continue
    pkg=data.get('package',{}); name=pkg.get('name') if isinstance(pkg,dict) else None
    if name:
        if name in package_names: fail(f'duplicate package {name}: {rel} and {package_names[name]}')
        else: package_names[name]=rel
    for table_name,table in dep_tables(data):
        for dep,spec in table.items():
            if isinstance(spec,dict) and ('path' in spec or spec.get('workspace') is True):
                pv=spec.get('path')
                if pv and not (manifest.parent/pv).resolve().exists(): fail(f'{rel}: missing path dependency {dep} -> {pv}')
                continue
            version=spec if isinstance(spec,str) else spec.get('version') if isinstance(spec,dict) else None
            in_c5=rel.parts and rel.parts[0]=='05-rust-metaprogramming'
            in_c7=rel.parts and rel.parts[0]=='07-rust-concurrency-parallelism'
            in_c8=rel.parts and rel.parts[0]=='08-rust-async-networked-services'
            in_c9=rel.parts and rel.parts[0]=='09-rust-performance-production-engineering'
            proc_macro=(data.get('lib',{}) or {}).get('proc-macro') is True
            approved_proc_macro = in_c5 and proc_macro and dep in allowed_versions and version==allowed_versions[dep]
            approved_rayon = in_c7 and dep=='rayon' and version=='=1.12.0'
            approved_async = in_c8 and dep in allowed_course8_versions and version==allowed_course8_versions[dep]
            approved_production = in_c9 and dep in allowed_course9_versions and version==allowed_course9_versions[dep]
            if not (approved_proc_macro or approved_rayon or approved_async or approved_production):
                fail(f'{rel}: unapproved external dependency {dep} ({table_name})')

for source in ROOT.rglob('*.rs'):
    rel=source.relative_to(ROOT); text=source.read_text(errors='strict')
    if 'compiler-labs' in rel.parts: continue
    for token in ('todo!','unimplemented!','dbg!'):
        if token in text: fail(f'{rel} contains {token}')
    has_unsafe=bool(re.search(r'\bunsafe\s*(?:fn|trait|impl|\{)|#\[unsafe\(',text))
    course_part = rel.parts[0] if rel.parts else ''
    course7_unsafe_lab = (
        course_part=='07-rust-concurrency-parallelism'
        and rel.as_posix().startswith('07-rust-concurrency-parallelism/labs/module-08-spsc-ring/solution/')
    )
    if has_unsafe and course_part!='06-rust-systems-programming' and not course7_unsafe_lab:
        fail(f'unsafe Rust outside approved Course 6/7 proof surfaces: {rel}')
    if has_unsafe and (course_part=='06-rust-systems-programming' or course7_unsafe_lab):
        lines=text.splitlines()
        test_region=False
        unsafe_definition=re.compile(r'^\s*(?:pub(?:\([^)]*\))?\s+)?unsafe\s+(?:extern\s+"[^"]+"\s+)?fn\s+[A-Za-z_][A-Za-z0-9_]*')
        for i,line in enumerate(lines):
            if line.strip() == '#[cfg(test)]':
                test_region=True
            if re.search(r'\bunsafe\s*\{',line) and 'unsafe {' in line:
                context='\n'.join(lines[max(0,i-5):i+1])
                if 'SAFETY:' not in context: fail(f'{rel}:{i+1} unsafe block lacks nearby SAFETY rationale')
            if not test_region and unsafe_definition.search(line):
                context='\n'.join(lines[max(0,i-12):i+1])
                if '# Safety' not in context: fail(f'{rel}:{i+1} unsafe function lacks # Safety contract')

for course_name,*_ in COURSES:
    tool=(ROOT/course_name/'rust-toolchain.toml').read_text(errors='strict')
    if '1.97.1' not in tool: fail(f'{course_name}: toolchain not pinned to 1.97.1')
    data=tomllib.loads((ROOT/course_name/'Cargo.toml').read_text())
    ws=data.get('workspace',{})
    if ws.get('resolver')!='3': fail(f'{course_name}: resolver must be 3')
    if (ws.get('package',{}) or {}).get('edition')!='2024': fail(f'{course_name}: edition must be 2024')

mkdocs=(ROOT/'mkdocs.yml').read_text(errors='strict')
for required in ('README.md','START_HERE.md','REASONING_MODEL.md','SKILL_MAP.md','COURSE_MAP.md','PROGRESS.md','GLOSSARY.md','SOURCE_NOTES.md'):
    if required not in mkdocs: fail(f'mkdocs navigation omits {required}')
for course_name,module_range,*_ in COURSES:
    for support in ('index.md','study-plan.md','capstone.md','reference.md','final-review.md'):
        rel=f'{course_name}/course-book/{support}'
        if rel not in mkdocs: fail(f'mkdocs navigation omits {rel}')
    for n in module_range:
        matches=list((ROOT/course_name/'course-book').glob(f'module-{n:02d}-*'))
        if len(matches)!=1: continue
        for name in ('index.md','workbook.md','solutions.md'):
            rel=(matches[0]/name).relative_to(ROOT).as_posix()
            if rel not in mkdocs: fail(f'mkdocs navigation omits {rel}')

for path in ROOT.rglob('*'):
    rel=path.relative_to(ROOT)
    if path.is_symlink(): fail(f'symlink in release: {rel}')
    if path.is_file() and path.stat().st_size==0: fail(f'zero-byte file: {rel}')
    if any(part in {'__MACOSX','__pycache__','target','site','.git'} for part in rel.parts) or path.name=='.DS_Store':
        fail(f'generated/platform artifact: {rel}')

print('Rust Courses 1–9 curriculum audit')
print(f'  modules: {len(all_modules)}')
print(f'  compiler specimens: {len(compiler_ids)}')
print(f'  Cargo packages: {len(package_names)}')
print(f'  Markdown pages: {len(list(ROOT.rglob("*.md")))}')
if errors:
    for error in errors: print('ERROR',error)
    raise SystemExit(1)
print('  result: PASS')
