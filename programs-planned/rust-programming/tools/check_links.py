#!/usr/bin/env python3
from pathlib import Path
import re, urllib.parse, sys
root=Path(__file__).resolve().parents[1]
pat=re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')
problems=[]; checked=0
for p in root.rglob('*.md'):
    for target in pat.findall(p.read_text(errors='ignore')):
        target=target.strip().split()[0].strip('<>')
        if not target or target.startswith(('#','http://','https://','mailto:')): continue
        target=urllib.parse.unquote(target.split('#',1)[0]);
        if not target: continue
        checked+=1
        if not (p.parent/target).resolve().exists(): problems.append((p.relative_to(root),target))
print(f'checked {checked} local Markdown links')
for p,t in problems: print(f'BROKEN {p} -> {t}')
raise SystemExit(1 if problems else 0)
