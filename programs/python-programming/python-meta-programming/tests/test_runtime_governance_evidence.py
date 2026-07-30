from __future__ import annotations

import json
import subprocess
import sys
import unittest

from labs.runtime_governance.evidence import build_evidence, render_evidence


class RuntimeGovernanceEvidenceTests(unittest.TestCase):
    def test_packet_contains_every_governance_surface(self) -> None:
        self.assertEqual(
            list(build_evidence()),
            [
                "dynamic_execution",
                "interface_contracts",
                "reversible_patching",
                "tooling_boundaries",
                "mechanism_selection",
            ],
        )

    def test_rendered_packet_is_stable_json(self) -> None:
        first = render_evidence()
        second = render_evidence()

        self.assertEqual(first, second)
        self.assertEqual(json.loads(first), build_evidence())

    def test_module_entrypoint_prints_the_same_packet(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "labs.runtime_governance"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(json.loads(result.stdout), build_evidence())

    def test_packet_contains_approval_constraint_and_rejection(self) -> None:
        evidence = build_evidence()

        self.assertEqual(  # type: ignore[index]
            evidence["mechanism_selection"]["outcome_counts"],
            {"approve": 1, "constrain": 2, "reject": 3},
        )
        self.assertFalse(  # type: ignore[index]
            evidence["dynamic_execution"]["trust_boundary"][
                "ast_validation_is_a_sandbox"
            ],
        )


if __name__ == "__main__":
    unittest.main()
