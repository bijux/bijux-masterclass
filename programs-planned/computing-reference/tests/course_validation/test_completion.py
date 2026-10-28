from __future__ import annotations

import csv
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from course_validation.blueprint import validate_blueprint
from course_validation.chapter import validate_chapter
from course_validation.completion import CompletionError, complete_module
from course_validation.result import ValidationResult
from course_validation.review import review_path
from fixtures import copy_blueprint
from test_chapter import valid_draft
from test_review import completed_review


class CompletionTests(unittest.TestCase):
    def _write_draft(self, root: Path) -> Path:
        path = (
            root
            / "programs/01-programming-languages-and-semantics/modules/"
            "001-programs-languages-and-observable-behavior.md"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(valid_draft(), encoding="utf-8")
        evidence = review_path(root, "PLS-001")
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(
            json.dumps(completed_review(valid_draft()), indent=2) + "\n",
            encoding="utf-8",
        )
        return path

    def test_validated_draft_transitions_all_owned_files(self) -> None:
        with copy_blueprint() as directory:
            root = Path(directory)
            chapter = self._write_draft(root)
            chapter_before = chapter.read_text(encoding="utf-8")
            csv_before = (root / "manifests/modules.csv").read_text(encoding="utf-8")
            jsonl_before = (root / "manifests/modules.jsonl").read_text(encoding="utf-8")

            outcome = complete_module(root, "PLS-001")

            self.assertIn("status: complete", chapter.read_text(encoding="utf-8"))
            self.assertTrue(validate_chapter(root, "PLS-001").ok)
            self.assertTrue(outcome.evidence_path.is_file())
            with (root / "manifests/modules.csv").open(encoding="utf-8", newline="") as handle:
                csv_rows = list(csv.DictReader(handle))
            json_rows = [
                json.loads(line)
                for line in (root / "manifests/modules.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual("complete", csv_rows[0]["status"])
            self.assertEqual("complete", json_rows[0]["status"])
            self.assertEqual(2999, sum(row["status"] == "planned" for row in csv_rows))
            chapter_after = chapter.read_text(encoding="utf-8")
            csv_after = (root / "manifests/modules.csv").read_text(encoding="utf-8")
            jsonl_after = (root / "manifests/modules.jsonl").read_text(encoding="utf-8")
            self.assertEqual(
                chapter_before.replace("status: draft", "status: complete", 1),
                chapter_after,
            )
            self.assertEqual(
                [1],
                [
                    index
                    for index, (before, after) in enumerate(
                        zip(csv_before.splitlines(), csv_after.splitlines(), strict=True)
                    )
                    if before != after
                ],
            )
            self.assertEqual(
                [0],
                [
                    index
                    for index, (before, after) in enumerate(
                        zip(jsonl_before.splitlines(), jsonl_after.splitlines(), strict=True)
                    )
                    if before != after
                ],
            )

    def test_invalid_draft_leaves_owned_files_unchanged(self) -> None:
        with copy_blueprint() as directory:
            root = Path(directory)
            chapter = self._write_draft(root)
            chapter.write_text(
                chapter.read_text(encoding="utf-8").replace("## Governing Question", "## Missing"),
                encoding="utf-8",
            )
            paths = (
                chapter,
                root / "manifests/modules.csv",
                root / "manifests/modules.jsonl",
            )
            before = {path: path.read_bytes() for path in paths}

            with self.assertRaises(CompletionError):
                complete_module(root, "PLS-001")

            self.assertEqual(before, {path: path.read_bytes() for path in paths})

    def test_missing_review_evidence_leaves_owned_files_unchanged(self) -> None:
        with copy_blueprint() as directory:
            root = Path(directory)
            chapter = self._write_draft(root)
            review_path(root, "PLS-001").unlink()
            paths = (
                chapter,
                root / "manifests/modules.csv",
                root / "manifests/modules.jsonl",
            )
            before = {path: path.read_bytes() for path in paths}

            with self.assertRaises(CompletionError):
                complete_module(root, "PLS-001")

            self.assertEqual(before, {path: path.read_bytes() for path in paths})

    def test_post_transition_failure_restores_owned_files(self) -> None:
        with copy_blueprint() as directory:
            root = Path(directory)
            chapter = self._write_draft(root)
            paths = (
                chapter,
                root / "manifests/modules.csv",
                root / "manifests/modules.jsonl",
            )
            before = {path: path.read_bytes() for path in paths}
            calls = 0

            def fail_second_blueprint_check(target: Path):
                nonlocal calls
                calls += 1
                if calls == 1:
                    return validate_blueprint(target)
                return ValidationResult(("forced post-transition defect",)), {}

            with patch(
                "course_validation.completion.validate_blueprint",
                side_effect=fail_second_blueprint_check,
            ):
                with self.assertRaises(CompletionError):
                    complete_module(root, "PLS-001")

            self.assertEqual(before, {path: path.read_bytes() for path in paths})


if __name__ == "__main__":
    unittest.main()
