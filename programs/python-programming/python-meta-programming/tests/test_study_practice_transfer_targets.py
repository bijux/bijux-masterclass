from __future__ import annotations

import unittest

from labs.study_practice.catalog import route_for
from labs.study_practice.transfer import (
    CAPSTONE_TRANSFERS,
    transfer_target_evidence,
)


class StudyPracticeTransferTargetTests(unittest.TestCase):
    def test_every_published_command_resolves_at_each_entry_level(self) -> None:
        evidence = transfer_target_evidence()

        self.assertTrue(evidence["valid"])
        self.assertEqual(evidence["missing"], [])
        self.assertEqual(evidence["checked_count"], 30)

    def test_target_evidence_covers_three_levels_in_stable_order(self) -> None:
        evidence = transfer_target_evidence()

        self.assertEqual(
            evidence["levels"],
            ["repository", "course", "capstone"],
        )
        first_module = evidence["checked"][:3]  # type: ignore[index]
        self.assertEqual(
            [record["level"] for record in first_module],
            ["repository", "course", "capstone"],
        )

    def test_study_catalog_and_transfer_catalog_publish_the_same_course_command(self) -> None:
        for transfer in CAPSTONE_TRANSFERS:
            with self.subTest(module=transfer.module):
                self.assertEqual(
                    route_for(transfer.module).capstone_command,
                    f"make {transfer.course_command}",
                )

    def test_transfer_commands_never_point_at_runtime_invocation(self) -> None:
        commands = {transfer.capstone_command for transfer in CAPSTONE_TRANSFERS}

        self.assertNotIn("demo", commands)
        self.assertNotIn("trace", commands)
        self.assertNotIn("invoke", commands)


if __name__ == "__main__":
    unittest.main()
