#!/usr/bin/env python3
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json, os, shutil, subprocess, sys, tempfile

COURSE=Path(__file__).resolve().parents[1]
ROOT=COURSE/'compiler-labs'

def compiler() -> str:
    local=COURSE/'node_modules/.bin/tsc'
    if local.exists(): return str(local)
    found=shutil.which('tsc')
    if found: return found
    raise SystemExit('tsc not found; run npm install in the course root')

def check(case: dict[str,object], tsc: str) -> tuple[str,bool,str]:
    case_id=str(case['id']); category=str(case['category'])
    source=ROOT/str(case['path']); config=source.parent/'tsconfig.json'
    if category.startswith('typecheck'):
        result=subprocess.run([tsc,'-p',str(config),'--pretty','false'],cwd=source.parent,text=True,capture_output=True)
        expected=category=='typecheck-fail'
        ok=(result.returncode!=0)==expected
        return case_id,ok,result.stdout+result.stderr
    with tempfile.TemporaryDirectory(prefix=f'{case_id}-') as directory:
        result=subprocess.run([
          tsc,'-p',str(config),'--pretty','false','--noEmit','false',
          '--outDir',directory,'--declaration','false','--declarationMap','false','--sourceMap','false',
        ],cwd=source.parent,text=True,capture_output=True)
        if result.returncode!=0: return case_id,False,result.stdout+result.stderr
        emitted=Path(directory)/'case.js'
        run=subprocess.run([shutil.which('node') or 'node',str(emitted)],cwd=source.parent,text=True,capture_output=True)
        if category=='run-pass':
            ok=run.returncode==0 and run.stdout==case.get('expectedStdout','')
        else:
            ok=run.returncode!=0 and str(case.get('expectedStderrContains','')) in run.stderr
        return case_id,ok,f'stdout={run.stdout!r}\nstderr={run.stderr!r}\n'

def main() -> int:
    data=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    cases=data['cases']; tsc=compiler(); failures=[]
    jobs=min(16,os.cpu_count() or 1)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures=[pool.submit(check,case,tsc) for case in cases]
        for future in as_completed(futures):
            case_id,ok,output=future.result()
            print(f'[{"PASS" if ok else "FAIL"}] {case_id}')
            if not ok: failures.append((case_id,output))
    for case_id,output in failures:
        print(f'\n--- {case_id} ---\n{output[-4000:]}')
    print(f'investigations: {len(cases)-len(failures)}/{len(cases)} passed')
    return 1 if failures else 0
if __name__=='__main__': raise SystemExit(main())
