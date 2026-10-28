from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from course_validation.chapter import REQUIRED_SECTIONS, REVIEW_SUBSECTIONS, validate_chapter_text

ARTIFACTS = ROOT / "artifacts"


def manifest_row() -> dict[str, str]:
    return {
        "module_id": "PLS-001",
        "program_name": "Programming Languages & Semantics",
        "level": "1",
        "module_number": "1",
        "module_title": "Programs, Languages, and Observable Behavior",
        "status": "planned",
    }


def substantive(label: str) -> str:
    return (
        f"{label} presents a concrete situation, states its assumptions, follows the mechanism "
        "through each relevant consequence, checks a boundary condition, and ends with an "
        "explicit conclusion that can be reviewed independently."
    )


def valid_draft() -> str:
    front = """---
module_id: PLS-001
program: Programming Languages & Semantics
level: 1
module_number: 1
title: Programs, Languages, and Observable Behavior
status: draft
last_verified: 2026-08-28
---

# Programs, Languages, and Observable Behavior
"""
    sections: list[str] = []
    for section in REQUIRED_SECTIONS:
        body = substantive(section)
        if section == "One-Page Review":
            body = "\n\n".join(f"### {name}\n\n{substantive(name)}" for name in REVIEW_SUBSECTIONS)
        elif section == "Worked Examples":
            body = "\n\n".join(f"### Example {number}\n\n{substantive(f'Example {number}')}" for number in range(1, 11))
        elif section == "Exercises":
            body = "\n\n".join(f"### Exercise {number}\n\n{substantive(f'Exercise {number}')}" for number in range(1, 6))
        elif section == "Answers to the Exercises":
            body = "\n\n".join(f"### Answer {number}\n\n{substantive(f'Answer {number}')}" for number in range(1, 6))
        elif section == "References":
            body = "\n".join(
                (
                    "- Author One. *Foundational Text*. First edition, 2020.",
                    "- Author Two. \"Primary Research Result.\" Journal, 2021.",
                    "- Standards Body. *Current Specification*. Revision 2026.",
                )
            )
        sections.append(f"## {section}\n\n{body}")
    return front + "\n\n".join(sections) + "\n"


class ChapterValidationTests(unittest.TestCase):
    def test_valid_draft_passes_structural_validation(self) -> None:
        result = validate_chapter_text(valid_draft(), manifest_row(), allow_draft=True)
        self.assertEqual((), result.issues)

    def test_missing_example_fails(self) -> None:
        text = valid_draft().replace("### Example 10", "### Demonstration 10")
        result = validate_chapter_text(text, manifest_row(), allow_draft=True)
        self.assertTrue(any("example headings" in issue for issue in result.issues))

    def test_manifest_identity_mismatch_fails(self) -> None:
        row = manifest_row()
        row["module_title"] = "Different Canonical Title"
        result = validate_chapter_text(valid_draft(), row, allow_draft=True)
        self.assertTrue(any("title differs" in issue for issue in result.issues))

    def test_completion_requires_both_statuses(self) -> None:
        result = validate_chapter_text(valid_draft(), manifest_row())
        self.assertTrue(any("complete status" in issue for issue in result.issues))

    def test_completed_chapter_passes_when_both_statuses_match(self) -> None:
        row = manifest_row()
        row["status"] = "complete"
        text = valid_draft().replace("status: draft", "status: complete")
        result = validate_chapter_text(text, row)
        self.assertEqual((), result.issues)

    def test_duplicate_worked_examples_fail(self) -> None:
        text = valid_draft()
        text = text.replace(substantive("Example 2"), substantive("Example 1"), 1)
        result = validate_chapter_text(text, manifest_row(), allow_draft=True)
        self.assertTrue(any("exact normalized duplicates" in issue for issue in result.issues))

    def test_unresolved_local_link_fails(self) -> None:
        text = valid_draft().replace(
            substantive("Cross-Program Connections"),
            f"{substantive('Cross-Program Connections')} See [missing](missing.md).",
        )
        ARTIFACTS.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ARTIFACTS) as directory:
            path = Path(directory) / "chapter.md"
            result = validate_chapter_text(text, manifest_row(), allow_draft=True, path=path)
        self.assertTrue(any("unresolved local link" in issue for issue in result.issues))

    def test_missing_reference_definition_fails(self) -> None:
        text = valid_draft().replace(
            substantive("Cross-Program Connections"),
            f"{substantive('Cross-Program Connections')} See [the successor][successor].",
        )
        ARTIFACTS.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ARTIFACTS) as directory:
            path = Path(directory) / "chapter.md"
            result = validate_chapter_text(text, manifest_row(), allow_draft=True, path=path)
        self.assertTrue(any("missing Markdown reference" in issue for issue in result.issues))

    def test_code_fence_headings_and_links_are_not_chapter_structure(self) -> None:
        text = valid_draft().replace(
            substantive("Core Exposition"),
            substantive("Core Exposition")
            + "\n\n```text\n## Demonstrated Heading\n[example](missing.md)\n```",
        )
        ARTIFACTS.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ARTIFACTS) as directory:
            path = Path(directory) / "chapter.md"
            result = validate_chapter_text(text, manifest_row(), allow_draft=True, path=path)
        self.assertEqual((), result.issues)

    def test_code_fence_bullets_do_not_count_as_references(self) -> None:
        text = valid_draft().replace(
            "- Standards Body. *Current Specification*. Revision 2026.",
            "```text\n- Not a real reference inside example data.\n```",
        )
        result = validate_chapter_text(text, manifest_row(), allow_draft=True)
        self.assertTrue(any("at least three" in issue for issue in result.issues))

    def test_legacy_math_delimiters_fail_validation(self) -> None:
        text = valid_draft().replace(
            substantive("Definitions and Notation"),
            substantive("Definitions and Notation") + " Let \\(x\\) be a value.",
        )
        result = validate_chapter_text(text, manifest_row(), allow_draft=True)
        self.assertTrue(any("GitHub inline math" in issue for issue in result.issues))


if __name__ == "__main__":
    unittest.main()
