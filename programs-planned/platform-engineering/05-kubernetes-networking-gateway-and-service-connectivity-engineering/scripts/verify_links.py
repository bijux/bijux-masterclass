#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from common import ROOT, fail

link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
checked = 0
for source in list((ROOT / "course-book").rglob("*.md")) + list(ROOT.glob("*.md")):
    text = source.read_text(encoding="utf-8")
    for raw in link_pattern.findall(text):
        target = raw.strip().split(" ", 1)[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (source.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"link escapes course root: {source.relative_to(ROOT)} -> {target}")
        if not resolved.exists():
            fail(f"broken link: {source.relative_to(ROOT)} -> {target}")
        checked += 1
print(f"PASS local Markdown links — {checked} targets")
