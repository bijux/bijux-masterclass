from __future__ import annotations

import json
import subprocess
import sys
import unittest

from labs.study_practice.evidence import build_study_evidence, render_study_evidence


class StudyPracticeEvidenceTests(unittest.TestCase):
    def test_packet_names_course_material_as_the_primary_product(self) -> None:
        packet = build_study_evidence()

        self.assertEqual(
            packet["primary_product"],
            "course website and runnable course material",
        )
        self.assertEqual(packet["integration_surface"], "incident-plugin capstone")
        self.assertEqual(
            packet["proof_order"],
            ["course command", "focused tests", "capstone transfer"],
        )

    def test_packet_contains_every_substantive_module_route(self) -> None:
        packet = build_study_evidence()
        routes = packet["routes"]

        self.assertEqual(len(routes), 10)  # type: ignore[arg-type]
        self.assertEqual(routes[0]["module"], 1)  # type: ignore[index]
        self.assertEqual(routes[-1]["module"], 10)  # type: ignore[index]

    def test_rendered_packet_is_stable_json(self) -> None:
        first = render_study_evidence(last_trusted_module=6)
        second = render_study_evidence(last_trusted_module=6)

        self.assertEqual(first, second)
        self.assertEqual(
            json.loads(first),
            build_study_evidence(last_trusted_module=6),
        )

    def test_module_entrypoint_accepts_a_reentry_boundary(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "labs.study_practice",
                "--last-trusted-module",
                "8",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        packet = json.loads(result.stdout)

        self.assertEqual(packet["reentry"]["last_trusted_module"], 8)
        self.assertEqual(packet["reentry"]["continue_with"]["module"], 9)
        self.assertTrue(packet["reentry"]["broad_gate_deferred"])


if __name__ == "__main__":
    unittest.main()
