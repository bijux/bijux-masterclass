#!/usr/bin/env python3
from common import ROOT,fail
cb=ROOT/'course-book'
modules=sorted(p for p in cb.glob('module-*') if p.is_dir())
if len(modules)!=11: fail(f'expected 11 module directories, got {len(modules)}')
for i,module in enumerate(modules):
    needed={'index.md','lab.md','checkpoint.md'} if i==0 else {'index.md','exercises.md','exercise-answers.md','lab.md','checkpoint.md'}
    missing=[x for x in needed if not (module/x).is_file()]
    if missing: fail(f'{module.name} missing {missing}')
print('PASS course structure — orientation plus 10 modules')
