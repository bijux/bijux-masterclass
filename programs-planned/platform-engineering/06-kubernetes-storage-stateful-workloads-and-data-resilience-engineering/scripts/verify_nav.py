#!/usr/bin/env python3
from __future__ import annotations

import yaml
from common import ROOT, fail

configuration = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
seen: list[str] = []

def walk(node):
    if isinstance(node, str):
        seen.append(node)
    elif isinstance(node, list):
        for item in node:
            walk(item)
    elif isinstance(node, dict):
        for item in node.values():
            walk(item)

walk(configuration["nav"])
book = ROOT / "course-book"
all_pages = {path.relative_to(book).as_posix() for path in book.rglob("*.md")}
if len(seen) != len(set(seen)):
    fail("MkDocs nav contains duplicate page entries")
if set(seen) != all_pages:
    fail(
        "MkDocs nav coverage differs: "
        f"omitted={sorted(all_pages - set(seen))[:10]} "
        f"extra={sorted(set(seen) - all_pages)[:10]}"
    )
print(f"PASS exact MkDocs navigation — {len(seen)} pages")
