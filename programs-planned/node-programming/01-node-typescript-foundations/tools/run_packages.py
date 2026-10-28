#!/usr/bin/env python3
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse, os, shutil, subprocess, sys

COURSE=Path(__file__).resolve().parents[1]

def compiler() -> str:
    local=COURSE/'node_modules/.bin/tsc'
    if local.exists(): return str(local)
    found=shutil.which('tsc')
    if found: return found
    raise SystemExit('tsc not found; run npm install in the course root')

def packages() -> list[Path]:
    result=[]
    for package in COURSE.rglob('package.json'):
        if package.parent in {COURSE, COURSE/'compiler-labs'}: continue
        if (package.parent/'tsconfig.json').is_file(): result.append(package.parent)
    return sorted(result)

def run_one(base: Path, mode: str, tsc: str) -> tuple[Path,bool,str]:
    dist=base/'dist'
    if dist.exists(): shutil.rmtree(dist)
    command=[tsc,'-p',str(base/'tsconfig.json')]
    if mode=='typecheck': command.append('--noEmit')
    build=subprocess.run(command,cwd=base,text=True,capture_output=True)
    if build.returncode!=0: return base,False,(build.stdout+build.stderr)
    if mode!='test': return base,True,''
    tests=sorted((dist/'tests').glob('*.test.js'))
    if not tests: return base,False,'no emitted test files\n'
    node=shutil.which('node') or 'node'
    executed=subprocess.run([node,'--test',*[str(p) for p in tests]],cwd=base,text=True,capture_output=True)
    return base,executed.returncode==0,executed.stdout+executed.stderr

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=('typecheck','build','test'))
    parser.add_argument('--jobs',type=int,default=min(4,os.cpu_count() or 1))
    args=parser.parse_args()
    tsc=compiler(); items=packages(); failures=[]
    with ThreadPoolExecutor(max_workers=max(1,args.jobs)) as pool:
        futures={pool.submit(run_one,item,args.mode,tsc):item for item in items}
        for future in as_completed(futures):
            base,ok,output=future.result()
            print(f'[{"PASS" if ok else "FAIL"}] {base.relative_to(COURSE)}')
            if not ok: failures.append((base,output))
    for base,output in failures:
        print(f'\n--- {base.relative_to(COURSE)} ---\n{output[-5000:]}')
    print(f'{args.mode}: {len(items)-len(failures)}/{len(items)} packages passed')
    return 1 if failures else 0
if __name__=='__main__': raise SystemExit(main())
