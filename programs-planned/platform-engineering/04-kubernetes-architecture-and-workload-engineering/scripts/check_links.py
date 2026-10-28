#!/usr/bin/env python3
from __future__ import annotations
from common import COURSE, fail, passed
from pathlib import Path
import re
count=0
for path in COURSE.rglob("*.md"):
    text=path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)",text):
        if target.startswith(("http://","https://","mailto:","#")): continue
        clean=target.split("#",1)[0]
        if not clean: continue
        candidate=(path.parent/clean).resolve()
        if not candidate.exists(): fail(f"broken link {path.relative_to(COURSE)} -> {target}")
        count+=1
passed(f"local Markdown links — {count}")
