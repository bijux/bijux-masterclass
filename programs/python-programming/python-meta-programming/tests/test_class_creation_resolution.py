from __future__ import annotations

import unittest

from labs.class_creation.resolution import resolution_evidence


class MetaclassResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evidence = resolution_evidence()

    def test_child_inherits_the_base_metaclass_without_redeclaring_it(self) -> None:
        inheritance = self.evidence["inheritance"]

        self.assertEqual(inheritance["base_metaclass"], "AuditMeta")  # type: ignore[index]
        self.assertEqual(inheritance["child_metaclass"], "AuditMeta")  # type: ignore[index]
        self.assertFalse(inheritance["explicit_child_metaclass"])  # type: ignore[index]

    def test_metaclass_events_happen_before_instance_creation(self) -> None:
        timing = self.evidence["timing"]

        self.assertEqual(  # type: ignore[index]
            timing["events_before_instance"],
            ["create:AuditedBase", "create:DeliveryAudit"],
        )
        self.assertFalse(timing["instance_creation_added_events"])  # type: ignore[index]

    def test_incompatible_metaclasses_raise_a_real_conflict(self) -> None:
        conflict = self.evidence["conflict"]

        self.assertEqual(conflict["failure_type"], "TypeError")  # type: ignore[index]
        self.assertTrue(conflict["mentions_metaclass_conflict"])  # type: ignore[index]

    def test_joint_metaclass_makes_the_choice_explicit(self) -> None:
        combined = self.evidence["combined"]

        self.assertEqual(combined["effective_metaclass"], "JointMeta")  # type: ignore[index]
        self.assertEqual(  # type: ignore[index]
            combined["joint_metaclass_bases"],
            ["AuditMeta", "PolicyMeta"],
        )
        self.assertFalse(combined["automatic_repair"])  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
