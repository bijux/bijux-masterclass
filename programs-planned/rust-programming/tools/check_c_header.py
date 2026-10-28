#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import shutil, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[1]
cap=ROOT/'06-rust-systems-programming/capstone'
headers=list(cap.rglob('*.h'))
if not headers:
    print('no Course 6 C header found')
    raise SystemExit(1)
header=headers[0]
errors=[]
source=f'#include "{header.name}"\nint main(void) {{ return 0; }}\n'
with tempfile.TemporaryDirectory(prefix='rust-course-c-header-') as d:
    tmp=Path(d); (tmp/'check.c').write_text(source); (tmp/'check.cpp').write_text(source)
    for compiler,lang,std,src in [('gcc','c','c11','check.c'),('clang','c','c11','check.c'),('g++','c++','c++17','check.cpp'),('clang++','c++','c++17','check.cpp')]:
        exe=shutil.which(compiler)
        if not exe: continue
        result=subprocess.run([exe,f'-std={std}','-Wall','-Wextra','-Werror','-fsyntax-only','-I',str(header.parent),str(tmp/src)],capture_output=True,text=True)
        if result.returncode: errors.append(f'{compiler}: {result.stderr}')
print(f'checked {header.relative_to(ROOT)} with available C/C++ front ends')
for e in errors: print('ERROR',e)
raise SystemExit(1 if errors else 0)
