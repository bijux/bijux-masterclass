from __future__ import annotations

import json
import unittest

from labs.runtime_observation import build_evidence, render_evidence


class RuntimeObservationLabTests(unittest.TestCase):
    def test_visible_names_stay_distinct_from_stored_state(self) -> None:
        packet = build_evidence()["visible_names"]

        self.assertTrue(packet["acknowledge_is_visible"])
        self.assertFalse(packet["acknowledge_is_stored"])
        self.assertEqual(
            packet["stored_names"],
            ["_fallback_reads", "_property_reads", "title"],
        )

    def test_static_property_lookup_does_not_execute_descriptor(self) -> None:
        packet = build_evidence()["dynamic_access"]

        self.assertTrue(packet["static_lookup_returns_property"])
        self.assertEqual(packet["property_reads_after_static_lookup"], 0)

    def test_dynamic_property_checks_make_execution_visible(self) -> None:
        packet = build_evidence()["dynamic_access"]

        self.assertEqual(packet["resolved_score"], 7)
        self.assertEqual(packet["property_reads_after_dynamic_lookup"], 1)
        self.assertTrue(packet["hasattr_result"])
        self.assertEqual(packet["property_reads_after_hasattr"], 2)

    def test_type_packet_separates_role_from_exact_identity(self) -> None:
        packet = build_evidence()["type_checks"]

        self.assertTrue(packet["bool_is_instance_of_int"])
        self.assertFalse(packet["bool_is_exact_int"])
        self.assertTrue(packet["extension_matches_delivery_role"])
        self.assertFalse(packet["extension_is_exact_base_type"])

    def test_callability_does_not_promise_valid_invocation(self) -> None:
        packet = build_evidence()["callability"]

        self.assertTrue(packet["callable_instance"])
        self.assertFalse(packet["instance_attribute_does_not_install_protocol"])
        self.assertEqual(packet["valid_result"], "route:INC-42")
        self.assertEqual(packet["invalid_call_error"], "ValueError")

    def test_static_lookup_avoids_fallback_execution(self) -> None:
        packet = build_evidence()["static_lookup"]

        self.assertTrue(packet["fallback_is_attached"])
        self.assertTrue(packet["static_lookup_reports_missing"])
        self.assertEqual(packet["fallback_reads_after_static_lookup"], 0)
        self.assertEqual(packet["resolved_owner"], "generated:owner")
        self.assertEqual(packet["fallback_reads_after_dynamic_lookup"], 1)

    def test_rendered_packet_is_stable_json(self) -> None:
        rendered = render_evidence()

        self.assertEqual(json.loads(rendered), build_evidence())
        self.assertEqual(
            list(json.loads(rendered)),
            [
                "callability",
                "dynamic_access",
                "static_lookup",
                "type_checks",
                "visible_names",
            ],
        )


if __name__ == "__main__":
    unittest.main()
