#!/usr/bin/env python3
from common import ROOT, fail, headings
book=ROOT/'course-book'
modules=[*sorted(book.glob('module-0[1-9]-*')),*sorted(book.glob('module-10-*'))]
q=a=0
for module in modules:
    questions=headings(module/'exercises.md'); answers=headings(module/'exercise-answers.md')
    if len(questions)!=12 or questions!=answers:
        fail(f"exercise/answer mismatch {module.name}: {len(questions)} / {len(answers)}")
    q+=len(questions); a+=len(answers)
    lab=(module/'lab.md').read_text(); checkpoint=(module/'checkpoint.md').read_text()
    for h in ['## Goal','## Safety boundary','## Baseline','## Hypothesis','## Controlled action','## Oracle','## Required evidence','## Interpretation','## Cleanup','## Completion gate']:
        if h not in lab: fail(f"{module.name} lab missing {h}")
    for h in ['## Required evidence','## Decision defense','## Progression gate']:
        if h not in checkpoint: fail(f"{module.name} checkpoint missing {h}")
if (q,a)!=(120,120): fail(f"expected 120/120, got {q}/{a}")
print('PASS 120 exercises, 120 matching worked answers, 10 labs, and 10 checkpoints')
