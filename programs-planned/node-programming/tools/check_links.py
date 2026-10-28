#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SKIP = {"node_modules", "dist", "site", "__pycache__"}
errors: list[str] = []
checked = 0

for page in ROOT.rglob("*.md"):
    if any(part in SKIP for part in page.parts):
        continue
    text = page.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    for raw in LINK.findall(text):
        target = raw.strip().split()[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        checked += 1
        destination = (page.parent / target).resolve()
        if not destination.exists():
            errors.append(f"{page.relative_to(ROOT)} -> {target}")

if errors:
    print("Broken local Markdown links:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)

print(f"checked {checked} local Markdown links")
