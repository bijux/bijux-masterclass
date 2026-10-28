#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import re
from common import ROOT, fail, words

book = ROOT / "course-book"
pages = list(book.rglob("*.md"))
main = [path for path in book.glob("module-*/index.md") if "module-00-" not in path.as_posix()]
short = [(path.parent.name, words(path)) for path in main if words(path) < 2300]
if short:
    fail(f"main chapters below 2,300 words: {short}")
orientation = book / "module-00-orientation" / "index.md"
if words(orientation) < 850:
    fail(f"orientation too short: {words(orientation)} words")
answer_count = 0
short_answers = []
for path in sorted(book.glob("module-*/exercise-answers.md")):
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^##\s+(\d+\.\s+.+)$", text)
    for index in range(1, len(parts), 2):
        answer_count += 1
        count = len(parts[index + 1].split())
        if count < 70:
            short_answers.append((path.parent.name, parts[index], count))
if answer_count != 120:
    fail(f"expected 120 worked answers, got {answer_count}")
if short_answers:
    fail(f"worked answers below 70 words: {short_answers[:8]}")
combined = "\n".join(path.read_text(encoding="utf-8") for path in pages)
for marker in ["TODO", "TBD", "lorem ipsum", "write your answer here", "insert content"]:
    if marker.lower() in combined.lower():
        fail(f"unfinished marker: {marker}")
paragraphs = []
for path in pages:
    paragraphs.extend(
        re.sub(r"\s+", " ", block.strip())
        for block in path.read_text(encoding="utf-8").split("\n\n")
        if len(block.split()) >= 55
    )
counts = Counter(paragraphs)
repeated = [(text, count) for text, count in counts.items() if count >= 4]
if repeated:
    text, count = repeated[0]
    fail(f"repeated long prose {count}x: {text[:110]}")
print(
    "PASS educational quality — "
    f"{len(pages)} pages, {sum(words(path) for path in pages)} words, "
    f"{answer_count} substantive worked answers"
)
