#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, sys

COURSE=Path(__file__).resolve().parents[1]
errors=[]
for path in COURSE.rglob('*.ts'):
    if 'compiler-labs' in path.parts or 'tools' in path.parts: continue
    text=path.read_text(encoding='utf-8')
    rel=path.relative_to(COURSE)
    checks={
      r'@ts-ignore|@ts-nocheck': 'suppressed TypeScript diagnostic',
      r'\bTODO\b|\bFIXME\b|\bTBD\b': 'unfinished marker',
      r'\btodo\s*\(': 'placeholder function',
      r'\beval\s*\(': 'eval usage',
      r'new\s+Function\s*\(': 'dynamic Function constructor',
    }
    for pattern,label in checks.items():
        if re.search(pattern,text): errors.append(f'{rel}: {label}')
    # Explicit any is prohibited in executable materials; quoted prose is outside .ts files.
    if re.search(r'(?<![\w])any(?![\w])',text): errors.append(f'{rel}: explicit any')
if errors:
    print('TypeScript source audit failed:')
    for error in errors: print(f'  - {error}')
    sys.exit(1)
print(f'checked {sum(1 for p in COURSE.rglob("*.ts") if "compiler-labs" not in p.parts)} non-investigation TypeScript files')
