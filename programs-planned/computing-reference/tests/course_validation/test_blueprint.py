from __future__ import annotations

import csv
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from course_validation.blueprint import validate_blueprint
from fixtures import copy_blueprint


class BlueprintValidationTests(unittest.TestCase):
    def test_repository_blueprint_passes(self) -> None:
        result, summary = validate_blueprint(ROOT)

        self.assertEqual((), result.issues)
        self.assertEqual(30, summary["programs"])
        self.assertEqual(3000, summary["modules"])
        self.assertEqual(
            3000,
            summary["planned_modules"] + summary["complete_modules"],
        )

    def test_csv_jsonl_disagreement_fails(self) -> None:
        with copy_blueprint() as directory:
            root = Path(directory)
            jsonl_path = root / "manifests" / "modules.jsonl"
            lines = jsonl_path.read_text(encoding="utf-8").splitlines()
            row = json.loads(lines[0])
            row["status"] = "complete"
            lines[0] = json.dumps(row, ensure_ascii=False)
            jsonl_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            result, _ = validate_blueprint(root)

        self.assertTrue(any("CSV and JSONL" in issue for issue in result.issues))

    def test_complete_module_without_chapter_fails(self) -> None:
        with copy_blueprint() as directory:
            root = Path(directory)
            csv_path = root / "manifests" / "modules.csv"
            with csv_path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
                fields = reader.fieldnames
            self.assertIsNotNone(fields)
            rows[0]["status"] = "complete"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)

            jsonl_path = root / "manifests" / "modules.jsonl"
            json_rows = [json.loads(line) for line in jsonl_path.read_text(encoding="utf-8").splitlines()]
            json_rows[0]["status"] = "complete"
            jsonl_path.write_text(
                "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in json_rows),
                encoding="utf-8",
            )

            result, _ = validate_blueprint(root)

        self.assertTrue(any("complete status has no chapter" in issue for issue in result.issues))


if __name__ == "__main__":
    unittest.main()
