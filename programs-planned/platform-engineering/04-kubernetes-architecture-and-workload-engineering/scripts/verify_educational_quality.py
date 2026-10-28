#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import re
from common import COURSE, fail, passed

book = COURSE / "course-book"
pages = list(book.rglob("*.md"))
words = sum(len(p.read_text().split()) for p in pages)
if len(pages) < 90:
    fail(f"course book is incomplete: {len(pages)} pages")
if words < 40000:
    fail(f"course book is too shallow: {words} words")
for chapter in sorted(book.glob("module-[0-9][0-9]-*/index.md")):
    if chapter.parent.name.startswith("module-00"):
        continue
    count = len(chapter.read_text().split())
    if count < 1400:
        fail(f"main chapter too shallow: {chapter.parent.name} ({count})")
joined = "\n".join(p.read_text() for p in pages)
for marker in ("TODO", "TBD", "FIXME", "lorem ipsum", "coming soon"):
    if re.search(rf"\b{re.escape(marker)}\b", joined, re.I):
        fail(f"unfinished marker in course book: {marker}")
if "Write a reasoned answer that identifies" in joined:
    fail("repeated exercise-answer scaffold remains")
# Reject exact long-paragraph cloning across learner pages.
paragraphs = []
for path in pages:
    for paragraph in re.split(r"\n\s*\n", path.read_text()):
        normalized = " ".join(paragraph.split())
        if len(normalized.split()) >= 45 and not normalized.startswith("```"):
            paragraphs.append(normalized)
repeated = [(text, n) for text, n in Counter(paragraphs).items() if n > 2]
if repeated:
    fail(f"long learner paragraph repeated {repeated[0][1]} times")
passed(f"educational quality — {len(pages)} pages, {words} words, no filler or long-block cloning")
