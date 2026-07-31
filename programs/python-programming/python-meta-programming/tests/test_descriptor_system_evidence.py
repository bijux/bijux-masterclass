from __future__ import annotations

import json
import unittest

from labs.descriptor_systems.evidence import build_evidence, render_evidence


class DescriptorSystemEvidenceTests(unittest.TestCase):
    def test_packet_covers_each_mechanism_and_the_boundary_decision(self) -> None:
        self.assertEqual(
            list(build_evidence()),
            [
                "cache_invalidation",
                "external_storage",
                "composition",
                "hint_policy",
                "record_model",
                "architecture_boundary",
            ],
        )

    def test_packet_keeps_sources_of_truth_visible(self) -> None:
        evidence = build_evidence()

        self.assertEqual(
            evidence["cache_invalidation"]["before_dependency_change"]["storage_owner"],
            "instance.__dict__",
        )
        self.assertEqual(
            evidence["external_storage"]["field"]["source_of_truth"],
            "CountingStore",
        )

    def test_packet_names_unsupported_framework_powers(self) -> None:
        evidence = build_evidence()

        self.assertFalse(evidence["external_storage"]["transaction_support"])
        self.assertFalse(evidence["hint_policy"]["full_runtime_typing"])
        self.assertFalse(evidence["record_model"]["production_orm"])

    def test_rendered_packet_is_stable_json(self) -> None:
        rendered = render_evidence()

        self.assertEqual(rendered, render_evidence())
        self.assertEqual(json.loads(rendered), build_evidence())


if __name__ == "__main__":
    unittest.main()
