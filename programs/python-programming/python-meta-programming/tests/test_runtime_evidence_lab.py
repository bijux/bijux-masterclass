from __future__ import annotations

import json
import unittest

from labs.runtime_evidence import build_evidence, render_evidence
from labs.runtime_evidence.evidence import caller_names


class RuntimeEvidenceLabTests(unittest.TestCase):
    def test_signature_packet_reports_enforced_parameter_kinds(self) -> None:
        packet = build_evidence()["signature"]

        self.assertEqual(
            packet["parameter_kinds"],
            {
                "incident_id": "positional_only",
                "severity": "positional_or_keyword",
                "retries": "keyword_only",
                "metadata": "var_keyword",
            },
        )
        self.assertEqual(packet["evidence_strength"], "strong-call-shape")

    def test_binding_packet_uses_python_call_rules(self) -> None:
        packet = build_evidence()["binding"]

        self.assertEqual(
            packet["bound_arguments"],
            {
                "incident_id": "INC-42",
                "severity": "warning",
                "retries": 2,
                "metadata": {"owner": "platform"},
            },
        )
        self.assertTrue(packet["keyword_for_positional_only_rejected"])
        self.assertEqual(packet["partial_arguments"], {"retries": 3})

    def test_provenance_packet_keeps_generated_source_best_effort(self) -> None:
        packet = build_evidence()["provenance"]

        self.assertEqual(packet["module"], "labs.runtime_evidence.evidence")
        self.assertEqual(packet["file_name"], "evidence.py")
        self.assertTrue(packet["file_backed_source_available"])
        self.assertEqual(packet["generated_file_label"], "<generated-runtime-evidence>")
        self.assertFalse(packet["generated_source_available"])
        self.assertEqual(packet["evidence_strength"], "best-effort-provenance")

    def test_member_packet_makes_dynamic_execution_visible(self) -> None:
        packet = build_evidence()["members"]

        self.assertEqual(packet["dynamic_value"], 7)
        self.assertEqual(packet["property_reads_after_getmembers"], 1)
        self.assertTrue(packet["static_value_is_property"])
        self.assertEqual(packet["property_reads_after_static_lookup"], 0)

    def test_frame_packet_is_bounded_and_diagnostic_only(self) -> None:
        packet = build_evidence()["frames"]

        self.assertEqual(packet["caller_names"], ["frame_evidence", "build_evidence"])
        self.assertEqual(packet["bounded_to"], 2)
        self.assertFalse(packet["retains_frame_objects"])
        self.assertEqual(packet["evidence_strength"], "diagnostic-only")

    def test_caller_name_helper_rejects_unbounded_request(self) -> None:
        with self.assertRaisesRegex(ValueError, "limit must be at least 1"):
            caller_names(0)

    def test_rendered_packet_is_stable_json(self) -> None:
        rendered = render_evidence()

        self.assertEqual(json.loads(rendered), build_evidence())
        self.assertEqual(
            list(json.loads(rendered)),
            ["binding", "frames", "members", "provenance", "signature"],
        )


if __name__ == "__main__":
    unittest.main()
