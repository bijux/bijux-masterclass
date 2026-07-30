from __future__ import annotations

import unittest

from labs.descriptor_systems.external import CountingStore
from labs.descriptor_systems.relational import (
    build_incident_model,
    inspect_columns,
    relational_model_evidence,
)


class DescriptorSystemRelationalTests(unittest.TestCase):
    def test_second_instance_reconstructs_field_values_from_backend(self) -> None:
        store = CountingStore()
        incident_type = build_incident_model(store)
        incident_type(
            12,
            severity="critical",
            summary="worker unavailable",
        )

        observer = incident_type(12)

        self.assertEqual(observer.severity, "critical")
        self.assertEqual(observer.summary, "worker unavailable")
        self.assertEqual(
            [event["operation"] for event in store.events],
            ["write", "write", "read", "read"],
        )

    def test_composed_column_normalizes_then_validates(self) -> None:
        incident_type = build_incident_model(CountingStore())
        incident = incident_type(3, severity=" WARNING ")

        self.assertEqual(incident.severity, "warning")
        with self.assertRaisesRegex(ValueError, "must be one of"):
            incident.severity = "urgent"

    def test_column_inspection_preserves_wrapper_and_backend_owners(self) -> None:
        incident_type = build_incident_model(CountingStore())
        contracts = inspect_columns(incident_type)

        self.assertEqual([contract.name for contract in contracts], ["severity", "summary"])
        self.assertEqual(
            contracts[0].layers,
            ("NormalizeText", "OneOf", "ExternalField"),
        )
        self.assertEqual(contracts[1].layers, ("ExternalField",))
        self.assertTrue(
            all(contract.backend_owner == "CountingStore" for contract in contracts)
        )

    def test_invalid_first_field_prevents_any_backend_write(self) -> None:
        store = CountingStore()
        incident_type = build_incident_model(store)

        with self.assertRaisesRegex(ValueError, "must be one of"):
            incident_type(7, severity="urgent", summary="should not be written")

        self.assertEqual(store.events, [])

    def test_evidence_refuses_a_production_orm_claim(self) -> None:
        evidence = relational_model_evidence()

        self.assertFalse(evidence["production_orm"])
        self.assertEqual(evidence["rejected_write"]["backend_writes_added"], 0)
        self.assertEqual(
            evidence["explicitly_absent"],
            [
                "transactions",
                "identity map",
                "query planning",
                "relationship loading",
                "schema migration",
            ],
        )


if __name__ == "__main__":
    unittest.main()
