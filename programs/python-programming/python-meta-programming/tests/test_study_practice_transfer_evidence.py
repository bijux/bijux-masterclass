from __future__ import annotations

import json
import subprocess
import sys
import unittest

from labs.study_practice.transfer_evidence import (
    build_transfer_evidence,
    render_transfer_evidence,
)


class StudyPracticeTransferEvidenceTests(unittest.TestCase):
    def test_packet_keeps_course_primary_and_transfer_observational(self) -> None:
        packet = build_transfer_evidence(module=7)

        self.assertEqual(
            packet["primary_product"],
            "course website and runnable course material",
        )
        self.assertFalse(packet["constructed"])
        self.assertFalse(packet["executed"])
        self.assertTrue(packet["targets"]["valid"])  # type: ignore[index]

    def test_one_module_packet_contains_one_exact_transfer(self) -> None:
        packet = build_transfer_evidence(module=10)

        self.assertEqual(len(packet["transfers"]), 1)  # type: ignore[arg-type]
        self.assertEqual(packet["transfers"][0]["module"], 10)  # type: ignore[index]
        self.assertEqual(
            packet["transfers"][0]["capstone_command"],  # type: ignore[index]
            "governance",
        )

    def test_all_module_packet_is_stable_json(self) -> None:
        rendered = render_transfer_evidence()

        self.assertEqual(json.loads(rendered), build_transfer_evidence())
        self.assertEqual(len(json.loads(rendered)["transfers"]), 10)

    def test_module_entrypoint_renders_requested_transfer(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "labs.study_practice.transfer_evidence",
                "--module",
                "4",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        packet = json.loads(result.stdout)

        self.assertEqual(packet["transfers"][0]["module"], 4)
        self.assertEqual(
            packet["transfers"][0]["capstone_command"],
            "action-wrapper",
        )


if __name__ == "__main__":
    unittest.main()
