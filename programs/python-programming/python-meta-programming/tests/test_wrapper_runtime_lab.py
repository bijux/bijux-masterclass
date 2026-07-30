from __future__ import annotations

import json
import unittest

from labs.wrapper_runtime import build_evidence, render_evidence


class WrapperRuntimeLabTests(unittest.TestCase):
    def test_lifecycle_separates_expression_application_and_call_order(self) -> None:
        packet = build_evidence()["lifecycle"]

        self.assertEqual(
            packet["definition_events"],
            [
                "factory:outer",
                "factory:inner",
                "decorate:inner:render_status",
                "decorate:outer:render_status",
            ],
        )
        self.assertEqual(
            packet["call_events"],
            [
                "enter:outer",
                "enter:inner",
                "body:INC-42:critical",
                "exit:inner",
                "exit:outer",
            ],
        )

    def test_lifecycle_exposes_closed_over_wrapper_ownership(self) -> None:
        packet = build_evidence()["lifecycle"]

        self.assertEqual(packet["outer_wrapper_closure"], ["events", "function", "label"])
        self.assertEqual(packet["wrapper_depth"], 2)
        self.assertEqual(
            packet["visible_signature"],
            "(incident_id: 'str', *, severity: 'str' = 'warning') -> 'str'",
        )

    def test_thin_wrapper_preserves_result_and_exception_identity(self) -> None:
        packet = build_evidence()["thin_wrapper"]

        self.assertTrue(packet["same_result_object"])
        self.assertTrue(packet["same_exception_object"])
        self.assertEqual(
            packet["events"],
            [
                "start:succeed",
                "success:object",
                "start:fail",
                "failure:DemonstrationFailure",
            ],
        )

    def test_metadata_packet_contrasts_bare_and_preserved_wrappers(self) -> None:
        packet = build_evidence()["metadata"]

        self.assertEqual(
            packet["bare"],
            {
                "name": "wrapped",
                "doc": None,
                "signature": "(*args: 'Any', **kwargs: 'Any') -> 'ResultT'",
                "has_wrapped": False,
            },
        )
        self.assertEqual(packet["preserved"]["name"], "preserved_handler")
        self.assertEqual(packet["preserved"]["doc"], "Render one incident.")
        self.assertEqual(
            packet["preserved"]["signature"],
            "(incident_id: 'str', *, severity: 'str' = 'warning') -> 'str'",
        )
        self.assertTrue(packet["preserved"]["has_wrapped"])
        self.assertTrue(packet["preserved"]["unwrap_is_original"])

    def test_rendered_evidence_is_stable_json(self) -> None:
        rendered = render_evidence()

        self.assertEqual(json.loads(rendered), build_evidence())
        self.assertEqual(
            list(json.loads(rendered)),
            ["lifecycle", "metadata", "thin_wrapper"],
        )


if __name__ == "__main__":
    unittest.main()
