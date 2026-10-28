#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

COURSE = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
problems: list[str] = []
count = 0

for file in sorted(COURSE.rglob("*.md")):
    if any(part in {"site", ".pytest_cache", "__pycache__"} for part in file.parts):
        continue
    for raw in PATTERN.findall(file.read_text(encoding="utf-8")):
        target = raw.split()[0].strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        count += 1
        resolved = (file.parent / target).resolve()
        try:
            resolved.relative_to(COURSE.resolve())
        except ValueError:
            problems.append(f"{file.relative_to(COURSE)} escapes course root: {target}")
            continue
        if not resolved.exists():
            problems.append(f"{file.relative_to(COURSE)} -> {target}")

if problems:
    raise SystemExit("broken local links:\n" + "\n".join(problems[:100]))
if count < 100:
    raise SystemExit(f"reader navigation is too sparse: only {count} local links")
print(f"PASS local Markdown links — {count}")
