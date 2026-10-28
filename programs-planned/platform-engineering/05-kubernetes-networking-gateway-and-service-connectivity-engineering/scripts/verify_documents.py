#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, fail, markdown_headings


course_book = ROOT / "course-book"
modules = [
    *sorted(course_book.glob("module-0[1-9]-*")),
    *sorted(course_book.glob("module-10-*")),
]

for module in modules:
    questions = markdown_headings(module / "exercises.md")
    answers = markdown_headings(module / "exercise-answers.md")
    if len(questions) != 12 or questions != answers:
        fail(
            f"exercise/answer mismatch {module.name}: "
            f"{len(questions)} questions / {len(answers)} answers"
        )

    lab = (module / "lab.md").read_text(encoding="utf-8")
    checkpoint = (module / "checkpoint.md").read_text(encoding="utf-8")

    required_lab_sections = [
        "## Goal",
        "## Safety boundary",
        "## Baseline",
        "## Hypothesis",
        "## Controlled action",
        "## Oracle",
        "## Required evidence",
        "## Interpretation",
        "## Cleanup",
        "## Completion gate",
    ]
    for heading in required_lab_sections:
        if heading not in lab:
            fail(f"{module.name} lab missing {heading}")

    required_checkpoint_sections = [
        "## Required evidence",
        "## Decision defense",
        "## Progression gate",
    ]
    for heading in required_checkpoint_sections:
        if heading not in checkpoint:
            fail(f"{module.name} checkpoint missing {heading}")

print("PASS 120 exercises, matching answers, 10 complete labs and checkpoints")
