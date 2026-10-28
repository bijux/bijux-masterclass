#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import re

from common import ROOT, fail

course_book = ROOT / "course-book"
pages = list(course_book.rglob("*.md"))
main_chapters = list(course_book.glob("module-*/index.md"))

short_chapters = [
    path
    for path in main_chapters
    if "module-00" not in path.as_posix()
    and len(path.read_text(encoding="utf-8").split()) < 2000
]
if short_chapters:
    fail(
        "main chapters below 2,000 words: "
        f"{[path.parent.name for path in short_chapters]}"
    )

orientation = course_book / "module-00-orientation" / "index.md"
if len(orientation.read_text(encoding="utf-8").split()) < 800:
    fail("orientation is not substantial enough for independent study")

answer_lengths: list[tuple[str, str, int]] = []
for path in sorted(course_book.glob("module-*/exercise-answers.md")):
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^##\s+(\d+\.\s+.+)$", text)
    for index in range(1, len(parts), 2):
        heading = parts[index]
        body_words = len(parts[index + 1].strip().split())
        answer_lengths.append((path.parent.name, heading, body_words))

short_answers = [entry for entry in answer_lengths if entry[2] < 55]
if short_answers:
    fail(f"worked answers below 55 words: {short_answers[:8]}")

combined = "\n".join(path.read_text(encoding="utf-8") for path in pages)
for marker in ["TODO", "TBD", "lorem ipsum", "write your answer here"]:
    if marker.lower() in combined.lower():
        fail(f"unfinished marker {marker}")

paragraphs: list[str] = []
for path in pages:
    paragraphs.extend(
        re.sub(r"\s+", " ", block.strip())
        for block in path.read_text(encoding="utf-8").split("\n\n")
        if len(block.split()) >= 45
    )
counts = Counter(paragraphs)
repeated = [(paragraph, count) for paragraph, count in counts.items() if count >= 4]
if repeated:
    paragraph, count = repeated[0]
    fail(f"repeated long prose {count}x: {paragraph[:100]}")

print(
    "PASS educational quality — "
    f"{len(pages)} pages, "
    f"{sum(len(path.read_text(encoding='utf-8').split()) for path in pages)} words, "
    f"{len(answer_lengths)} worked answers"
)
