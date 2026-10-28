#!/usr/bin/env python3
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse, os, shutil, signal, subprocess, sys

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

def run_bounded(command: list[str], cwd: Path, timeout: int) -> tuple[int, str]:
    process = subprocess.Popen(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=timeout)
        return process.returncode, output
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        output, _ = process.communicate()
        return 124, output + f"\ncommand timed out after {timeout} seconds\n"

def run_one(base: Path, mode: str, tsc: str) -> tuple[Path,bool,str]:
    dist=base/'dist'
    if dist.exists(): shutil.rmtree(dist)
    command=[tsc,'-p',str(base/'tsconfig.json')]
    if mode=='typecheck': command.append('--noEmit')
    build_code, build_output = run_bounded(command, base, 60)
    if build_code != 0:
        return base, False, build_output
    if mode!='test': return base,True,''
    tests=sorted((dist/'tests').glob('*.test.js'))
    if not tests: return base,False,'no emitted test files\n'
    node=shutil.which('node') or 'node'
    test_code, test_output = run_bounded(
        [node, '--test', *[str(p) for p in tests]],
        base,
        60,
    )
    return base, test_code == 0, test_output

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
            print(f'[{"PASS" if ok else "FAIL"}] {base.relative_to(COURSE)}', flush=True)
            if not ok: failures.append((base,output))
    for base,output in failures:
        print(f'\n--- {base.relative_to(COURSE)} ---\n{output[-5000:]}')
    print(f'{args.mode}: {len(items)-len(failures)}/{len(items)} packages passed')
    return 1 if failures else 0
if __name__=='__main__': raise SystemExit(main())
