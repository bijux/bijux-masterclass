#!/usr/bin/env python3
from pathlib import Path
import re, sys
COURSE=Path(__file__).resolve().parents[1]
errors=[]; checked=0
for path in COURSE.rglob('*.ts'):
    if any(part in {'compiler-labs','node_modules','dist','site'} for part in path.parts): continue
    checked+=1; text=path.read_text(encoding='utf-8'); rel=path.relative_to(COURSE)
    checks={r'@ts-ignore|@ts-nocheck':'suppressed TypeScript diagnostic',r'\bTODO\b|\bFIXME\b|\bTBD\b':'unfinished marker',r'\beval\s*\(':'eval usage',r'new\s+Function\s*\(':'dynamic Function constructor'}
    for pattern,label in checks.items():
        if re.search(pattern,text): errors.append(f'{rel}: {label}')
    if re.search(r'(?<![\w])any(?![\w])',text): errors.append(f'{rel}: explicit any')
if errors:
    print('TypeScript source audit failed:'); [print(f'  - {e}') for e in errors]; sys.exit(1)
print(f'checked {checked} non-investigation TypeScript files')
