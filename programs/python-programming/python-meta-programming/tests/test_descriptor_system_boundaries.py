from __future__ import annotations

import unittest

from labs.descriptor_systems.boundaries import (
    DesignPressure,
    boundary_evidence,
    decide_owner,
)


class DescriptorSystemBoundaryTests(unittest.TestCase):
    def test_one_attribute_normalization_stays_in_a_descriptor(self) -> None:
        decision = decide_owner(DesignPressure.NORMALIZE_ONE_ATTRIBUTE)

        self.assertEqual(decision.owner, "descriptor")
        self.assertEqual(decision.refused_weaker_owner, "caller convention")
        self.assertEqual(decision.refused_stronger_owner, "model framework")

    def test_local_invalidation_names_the_cross_instance_escalation_signal(self) -> None:
        decision = decide_owner(DesignPressure.INVALIDATE_LOCAL_DERIVATION)

        self.assertEqual(decision.owner, "coordinated descriptor system")
        self.assertIn("instances or processes", decision.escalation_signal)

    def test_record_coordination_moves_to_a_session_or_unit_of_work(self) -> None:
        decision = decide_owner(DesignPressure.COORDINATE_RECORD_WRITES)

        self.assertEqual(decision.owner, "session or unit of work")
        self.assertEqual(decision.refused_weaker_owner, "smart field descriptor")

    def test_evidence_covers_every_named_pressure_and_both_refusals(self) -> None:
        evidence = boundary_evidence()

        self.assertEqual(len(evidence["decisions"]), len(DesignPressure))
        self.assertTrue(evidence["power_is_not_the_goal"])
        for decision in evidence["decisions"]:
            self.assertTrue(decision["refused_weaker_owner"])
            self.assertTrue(decision["refused_stronger_owner"])
            self.assertTrue(decision["escalation_signal"])


if __name__ == "__main__":
    unittest.main()
