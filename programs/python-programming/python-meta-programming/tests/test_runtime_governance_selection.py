from __future__ import annotations

import unittest

from labs.runtime_governance.selection import DECISIONS, selection_evidence


class GovernanceSelectionTests(unittest.TestCase):
    def test_every_decision_contains_operational_evidence(self) -> None:
        for decision in DECISIONS:
            with self.subTest(pressure=decision.pressure):
                self.assertTrue(decision.blast_radius)
                self.assertTrue(decision.observability)
                self.assertTrue(decision.rollback)
                self.assertTrue(decision.proof)
                self.assertTrue(decision.escalation_signal)

    def test_outcomes_include_approval_constraint_and_rejection(self) -> None:
        evidence = selection_evidence()

        self.assertEqual(
            evidence["outcome_counts"],
            {"approve": 1, "constrain": 2, "reject": 3},
        )

    def test_untrusted_eval_is_rejected_to_a_process_boundary(self) -> None:
        decision = next(
            item
            for item in DECISIONS
            if item.proposed_mechanism == "eval with empty builtins"
        )

        self.assertEqual(decision.decision, "reject")
        self.assertEqual(decision.selected_owner, "isolated policy service")

    def test_plugin_metaclass_is_approved_with_an_escalation_boundary(self) -> None:
        decision = next(
            item
            for item in DECISIONS
            if item.proposed_mechanism == "PluginMeta"
        )

        self.assertEqual(decision.decision, "approve")
        self.assertIn("external I/O", decision.escalation_signal)

    def test_import_hook_is_tooling_only_and_reversible(self) -> None:
        decision = next(
            item
            for item in DECISIONS
            if item.proposed_mechanism == "meta path finder"
        )

        self.assertEqual(decision.decision, "constrain")
        self.assertIn("remove finder", decision.rollback)


if __name__ == "__main__":
    unittest.main()
