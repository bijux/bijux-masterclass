#!/usr/bin/env python3
from common import COURSE, fail, passed
import re
book=COURSE/"course-book"
required_general=["index.md","start-here.md","study-plan.md","capstone.md","evidence-model.md","language-strategy.md","standards.md","glossary.md"]
for name in required_general:
    if not (book/name).is_file(): fail(f"missing course-book/{name}")
modules=sorted(p for p in book.glob("module-*") if p.is_dir())
if len(modules)!=11: fail(f"expected orientation plus ten modules, got {len(modules)}")
numbered=[p for p in modules if not p.name.startswith("module-00")]
for module in numbered:
    for name in ("index.md","exercises.md","exercise-answers.md","lab.md","checkpoint.md"):
        if not (module/name).is_file(): fail(f"missing {module.name}/{name}")
    words=len((module/"index.md").read_text().split())
    if words < 1400: fail(f"chapter too shallow: {module.name} ({words} words)")
    q=re.findall(r"^## (\d+)\. ", (module/"exercises.md").read_text(), re.M)
    a=re.findall(r"^## (\d+)\. ", (module/"exercise-answers.md").read_text(), re.M)
    if q!=a or len(q)!=12: fail(f"exercise/answer mismatch in {module.name}: {len(q)}/{len(a)}")
    lab=(module/"lab.md").read_text()
    for heading in ("Goal","Safety boundary","Baseline","Hypothesis","Controlled action","Oracle","Evidence","Interpretation","Cleanup","Completion gate"):
        if f"## {heading}" not in lab: fail(f"lab missing {heading}: {module.name}")
    checkpoint=(module/"checkpoint.md").read_text()
    for heading in ("Required evidence","Decision defense","Progression gate"):
        if f"## {heading}" not in checkpoint: fail(f"checkpoint missing {heading}: {module.name}")
passed(f"course structure — {len(numbered)} modules, {len(numbered)*12} exercises and answers")
