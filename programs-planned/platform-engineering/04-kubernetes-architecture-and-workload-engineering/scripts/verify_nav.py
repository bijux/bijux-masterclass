#!/usr/bin/env python3
from common import COURSE, fail, passed
import yaml
nav=yaml.safe_load((COURSE/"mkdocs.yml").read_text())["nav"]
paths=[]
def walk(node):
    if isinstance(node,str): paths.append(node)
    elif isinstance(node,list):
        for item in node: walk(item)
    elif isinstance(node,dict):
        for value in node.values(): walk(value)
walk(nav)
book=COURSE/"course-book"
expected={p.relative_to(book).as_posix() for p in book.rglob("*.md")}
actual=set(paths)
if expected!=actual:
    fail(f"MkDocs nav mismatch missing={sorted(expected-actual)} extra={sorted(actual-expected)}")
passed(f"MkDocs navigation covers {len(actual)} course-book pages")
