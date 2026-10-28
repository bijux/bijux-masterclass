#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import unquote
import re, sys
ROOT=Path(__file__).resolve().parents[2]
link_re=re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)');errors=[];checked=0
for page in ROOT.rglob('*.md'):
    if any(part in {'node_modules','dist','site'} for part in page.parts): continue
    text=page.read_text(encoding='utf-8')
    text=re.sub(r'```.*?```','',text,flags=re.S)
    text=re.sub(r'`[^`]*`','',text)
    for raw in link_re.findall(text):
        target=raw.strip().split()[0].strip('<>')
        if not target or target.startswith(('#','http://','https://','mailto:')): continue
        target=unquote(target.split('#',1)[0])
        if not target: continue
        checked+=1; destination=(page.parent/target).resolve()
        if not destination.exists(): errors.append(f'{page.relative_to(ROOT)} -> {target}')
if errors:
    print('Broken local links:'); [print(f'  - {e}') for e in errors]; sys.exit(1)
print(f'checked {checked} local Markdown links')
