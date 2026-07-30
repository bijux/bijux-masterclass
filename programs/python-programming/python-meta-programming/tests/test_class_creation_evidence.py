from __future__ import annotations

import json
import subprocess
import sys
import unittest

from labs.class_creation.evidence import build_evidence, render_evidence


class ClassCreationEvidenceTests(unittest.TestCase):
    def test_packet_contains_every_module_mechanism(self) -> None:
        self.assertEqual(
            list(build_evidence()),
            [
                "manual_construction",
                "resolution",
                "lifecycle",
                "declaration_namespace",
                "registry",
                "boundaries",
            ],
        )

    def test_rendered_packet_is_stable_json(self) -> None:
        first = render_evidence()
        second = render_evidence()

        self.assertEqual(first, second)
        self.assertEqual(json.loads(first), build_evidence())

    def test_module_entrypoint_prints_the_same_packet(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "labs.class_creation"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(json.loads(result.stdout), build_evidence())

    def test_packet_keeps_capability_limits_visible(self) -> None:
        evidence = build_evidence()

        self.assertIn(  # type: ignore[operator]
            "it does not justify a custom metaclass",
            evidence["manual_construction"]["claim_limits"],
        )
        self.assertIn(  # type: ignore[operator]
            "neither component discovers packages or coordinates processes",
            evidence["registry"]["claim_limits"],
        )


if __name__ == "__main__":
    unittest.main()
