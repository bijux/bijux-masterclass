#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from urllib.parse import unquote
import re, sys

ROOT=Path(__file__).resolve().parents[2]
link_re=re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')
errors=[]
checked=0
for page in ROOT.rglob('*.md'):
    text=page.read_text(encoding='utf-8')
    for raw in link_re.findall(text):
        target=raw.strip().split()[0].strip('<>')
        if not target or target.startswith(('#','http://','https://','mailto:')): continue
        target=unquote(target.split('#',1)[0])
        if not target: continue
        destination=(page.parent/target).resolve()
        checked+=1
        if not destination.exists(): errors.append(f'{page.relative_to(ROOT)} -> {target}')
if errors:
    print('Broken local links:')
    for error in errors: print(f'  - {error}')
    sys.exit(1)
print(f'checked {checked} local Markdown links')
