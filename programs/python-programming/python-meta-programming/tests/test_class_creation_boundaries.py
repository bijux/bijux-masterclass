from __future__ import annotations

import unittest

from labs.class_creation.boundaries import DECISIONS, boundary_evidence


class ClassCreationBoundaryTests(unittest.TestCase):
    def test_every_decision_names_a_selected_and_refused_owner(self) -> None:
        for decision in DECISIONS:
            with self.subTest(pressure=decision.pressure):
                self.assertTrue(decision.selected_owner)
                self.assertTrue(decision.refused_owner)
                self.assertNotEqual(
                    decision.selected_owner,
                    decision.refused_owner,
                )

    def test_every_decision_names_cost_and_escalation(self) -> None:
        for decision in DECISIONS:
            with self.subTest(pressure=decision.pressure):
                self.assertTrue(decision.accepted_cost)
                self.assertTrue(decision.escalation_signal)

    def test_metaclass_is_not_the_default_owner(self) -> None:
        selected = [decision.selected_owner for decision in DECISIONS]

        self.assertEqual(selected.count("metaclass with external registry"), 1)
        self.assertEqual(selected.count("metaclass __prepare__"), 1)
        self.assertEqual(len(selected), 7)

    def test_registration_alone_stops_at_init_subclass(self) -> None:
        registration = next(
            decision
            for decision in DECISIONS
            if decision.pressure
            == "register every concrete subclass in one class family"
        )

        self.assertEqual(registration.selected_owner, "__init_subclass__")
        self.assertEqual(registration.refused_owner, "metaclass")

    def test_discovery_is_explicitly_outside_class_creation(self) -> None:
        discovery = next(
            decision
            for decision in DECISIONS
            if decision.pressure == "discover installed plugins across processes"
        )

        self.assertEqual(discovery.selected_owner, "explicit discovery service")
        self.assertEqual(discovery.refused_owner, "metaclass")

    def test_manifest_preserves_the_review_fields(self) -> None:
        evidence = boundary_evidence()

        self.assertEqual(len(evidence["decisions"]), 7)  # type: ignore[arg-type]
        self.assertEqual(  # type: ignore[index]
            evidence["owner_ladder"][0],
            "plain class definition",
        )
        self.assertEqual(  # type: ignore[index]
            len(evidence["metaclass_acceptance_test"]),
            4,
        )


if __name__ == "__main__":
    unittest.main()
