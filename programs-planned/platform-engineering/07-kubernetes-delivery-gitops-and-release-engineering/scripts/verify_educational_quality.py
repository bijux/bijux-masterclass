#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
import re
from common import ROOT, fail, words
book=ROOT/'course-book'; pages=list(book.rglob('*.md'))
main=[p for p in book.glob('module-*/index.md') if 'module-00-' not in p.as_posix()]
short=[(p.parent.name,words(p)) for p in main if words(p)<1750]
if short: fail(f"main chapters below 1,750 words: {short}")
orientation=book/'module-00-orientation/index.md'
if words(orientation)<1000: fail(f"orientation too short: {words(orientation)}")
answer_count=0; short_answers=[]
for p in sorted(book.glob('module-*/exercise-answers.md')):
    parts=re.split(r'(?m)^##\s+(\d+\.\s+.+)$',p.read_text())
    for i in range(1,len(parts),2):
        answer_count+=1; n=len(parts[i+1].split())
        if n<25: short_answers.append((p.parent.name,parts[i],n))
if answer_count!=120 or short_answers: fail(f"worked-answer quality count={answer_count} short={short_answers[:5]}")
combined='\n'.join(p.read_text() for p in pages)
for marker in ['TODO','TBD','lorem ipsum','write your answer here','insert content']:
    if marker.lower() in combined.lower(): fail(f"unfinished marker: {marker}")
paragraphs=[]
for p in pages:
    paragraphs.extend(re.sub(r'\s+',' ',b.strip()) for b in p.read_text().split('\n\n') if len(b.split())>=55)
repeat=[(x,n) for x,n in Counter(paragraphs).items() if n>=4]
if repeat: fail(f"repeated long prose {repeat[0][1]}x: {repeat[0][0][:100]}")
print(f"PASS educational quality — {len(pages)} pages, {sum(words(p) for p in pages)} words, 120 worked answers")
