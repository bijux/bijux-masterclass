from __future__ import annotations

import json
import sys
import unittest

from labs.runtime_objects import build_evidence, render_evidence


class RuntimeObjectLabTests(unittest.TestCase):
    def test_function_packet_exposes_closure_behavior(self) -> None:
        packet = build_evidence()["function"]

        self.assertTrue(packet["callable"])
        self.assertEqual(packet["free_variables"], ["prefix"])
        self.assertEqual(packet["result"], "incident: queue lag")

    def test_class_packet_traces_function_to_bound_method(self) -> None:
        packet = build_evidence()["class"]

        self.assertEqual(packet["class_metaclass"], "type")
        self.assertTrue(packet["class_stores_function"])
        self.assertTrue(packet["bound_method_has_instance"])
        self.assertTrue(packet["bound_method_has_function"])

    def test_module_packet_proves_cache_identity_and_stale_copy(self) -> None:
        synthetic_module_name = "_bijux_runtime_object_lab"

        packet = build_evidence()["module"]

        self.assertTrue(packet["cached_import_preserves_identity"])
        self.assertEqual(packet["module_status"], "new")
        self.assertEqual(packet["copied_status"], "old")
        self.assertTrue(packet["copied_value_is_stale"])
        self.assertNotIn(synthetic_module_name, sys.modules)

    def test_instance_packet_compares_storage_models(self) -> None:
        packet = build_evidence()["instance"]

        self.assertEqual(packet["regular_storage"], {"title": "queue lag"})
        self.assertFalse(packet["slotted_has_dict"])
        self.assertTrue(packet["slotted_rejects_undeclared_attribute"])

    def test_object_graph_packet_reaches_the_defining_module(self) -> None:
        packet = build_evidence()["object_graph"]

        self.assertTrue(packet["instance_points_to_class"])
        self.assertTrue(packet["bound_method_points_to_instance"])
        self.assertTrue(packet["bound_method_points_to_function"])
        self.assertTrue(packet["function_points_to_module_namespace"])
        self.assertTrue(packet["global_used_by_call"])
        self.assertEqual(packet["result"], "CRIT: queue lag")

    def test_rendered_packet_is_stable_json(self) -> None:
        rendered = render_evidence()

        self.assertEqual(json.loads(rendered), build_evidence())
        self.assertEqual(
            list(json.loads(rendered)),
            ["class", "function", "instance", "module", "object_graph"],
        )


if __name__ == "__main__":
    unittest.main()
