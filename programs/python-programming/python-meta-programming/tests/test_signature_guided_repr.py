from __future__ import annotations

import unittest

from labs.runtime_evidence.repr_demo import (
    IncidentRecord,
    SlottedIncident,
    build_demo,
)
from labs.runtime_evidence.safe_repr import SignatureGuidedRepr, ordered_state, stored_state


class SignatureGuidedReprTests(unittest.TestCase):
    def test_constructor_contract_orders_dictionary_state_before_extras(self) -> None:
        record = IncidentRecord("INC-42")

        self.assertEqual(
            repr(record),
            "IncidentRecord(incident_id='INC-42', severity='warning', owner='platform')",
        )
        self.assertEqual(
            ordered_state(record),
            (
                ("incident_id", "INC-42"),
                ("severity", "warning"),
                ("owner", "platform"),
            ),
        )

    def test_slotted_state_is_rendered_without_evaluating_property(self) -> None:
        record = SlottedIncident("INC-43", "critical")

        rendered = repr(record)

        self.assertEqual(
            rendered,
            "SlottedIncident(incident_id='INC-43', severity='critical', property_reads=0)",
        )
        self.assertEqual(record.property_reads, 0)
        self.assertNotIn("risk_score", stored_state(record))

    def test_inherited_and_private_slots_are_collected_from_storage(self) -> None:
        class BaseRecord(SignatureGuidedRepr):
            __slots__ = ("base_value", "__token")

            def __init__(self, base_value: int) -> None:
                self.base_value = base_value
                self.__token = "stored"

        class ChildRecord(BaseRecord):
            __slots__ = ("child_value",)

            def __init__(self, base_value: int, child_value: int) -> None:
                super().__init__(base_value)
                self.child_value = child_value

        record = ChildRecord(1, 2)

        self.assertEqual(
            stored_state(record),
            {
                "child_value": 2,
                "base_value": 1,
                "_BaseRecord__token": "stored",
            },
        )
        self.assertEqual(
            repr(record),
            "ChildRecord(base_value=1, child_value=2, _BaseRecord__token='stored')",
        )

    def test_custom_getattribute_and_getattr_are_not_used_for_discovery(self) -> None:
        class GuardedRecord(SignatureGuidedRepr):
            def __init__(self, incident_id: str) -> None:
                object.__setattr__(self, "incident_id", incident_id)
                object.__setattr__(self, "lookup_count", 0)

            def __getattribute__(self, name: str) -> object:
                if name not in {"lookup_count", "__dict__", "__class__"}:
                    count = object.__getattribute__(self, "lookup_count")
                    object.__setattr__(self, "lookup_count", count + 1)
                return object.__getattribute__(self, name)

            def __getattr__(self, name: str) -> object:
                raise AssertionError(f"dynamic fallback executed for {name}")

        record = GuardedRecord("INC-44")

        rendered = repr(record)

        self.assertEqual(rendered, "GuardedRecord(incident_id='INC-44', lookup_count=0)")
        self.assertEqual(record.lookup_count, 0)

    def test_demo_labels_each_evidence_source(self) -> None:
        packet = build_demo()

        self.assertEqual(packet["property_reads_after_repr"], 0)
        self.assertEqual(
            packet["evidence"],
            {
                "ordering": "constructor-signature",
                "values": "instance-storage",
                "dynamic_member_lookup": False,
                "frame_inspection": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
