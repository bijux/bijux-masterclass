#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, fail, headings

book = ROOT / "course-book"
modules = [
    *sorted(book.glob("module-0[1-9]-*")),
    *sorted(book.glob("module-10-*")),
]
questions_total = answers_total = 0
for module in modules:
    questions = headings(module / "exercises.md")
    answers = headings(module / "exercise-answers.md")
    if len(questions) != 12 or questions != answers:
        fail(
            f"exercise/answer mismatch {module.name}: "
            f"{len(questions)} questions / {len(answers)} answers"
        )
    questions_total += len(questions)
    answers_total += len(answers)
    lab = (module / "lab.md").read_text(encoding="utf-8")
    checkpoint = (module / "checkpoint.md").read_text(encoding="utf-8")
    for heading in [
        "## Goal", "## Safety boundary", "## Baseline", "## Hypothesis",
        "## Controlled action", "## Oracle", "## Required evidence",
        "## Interpretation", "## Cleanup", "## Completion gate",
    ]:
        if heading not in lab:
            fail(f"{module.name} lab missing {heading}")
    for heading in ["## Required evidence", "## Decision defense", "## Progression gate"]:
        if heading not in checkpoint:
            fail(f"{module.name} checkpoint missing {heading}")
if questions_total != 120 or answers_total != 120:
    fail("expected 120 exercises and worked answers")
print("PASS 120 module-specific exercises, answers, 10 labs, and 10 checkpoints")
