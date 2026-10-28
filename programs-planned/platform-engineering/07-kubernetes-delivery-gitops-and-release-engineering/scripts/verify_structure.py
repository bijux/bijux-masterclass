#!/usr/bin/env python3
from common import ROOT, fail
book=ROOT/'course-book'
modules=sorted(p for p in book.glob('module-*') if p.is_dir())
if len(modules)!=11: fail(f"expected orientation plus 10 modules, got {len(modules)}")
for module in modules:
    required={'index.md','lab.md','checkpoint.md'}
    if 'module-00-' not in module.name: required|={'exercises.md','exercise-answers.md'}
    missing=sorted(x for x in required if not (module/x).is_file())
    if missing: fail(f"{module.name} missing {missing}")
for d in ['guides','reference','casebook','capstone','assessment','instructor']:
    if not (book/d).is_dir(): fail(f"missing course-book/{d}")
for d in ['atlas_delivery','tests','repository','controllers','secrets','progressive','fleet','policy','releases','planted-defects','shared/vectors','handoff','predecessor/handoff','gitopsprobe-go']:
    if not (ROOT/'capstone'/d).exists(): fail(f"missing capstone/{d}")
print('PASS reader-first course structure, capstone, native lanes, and handoffs')
