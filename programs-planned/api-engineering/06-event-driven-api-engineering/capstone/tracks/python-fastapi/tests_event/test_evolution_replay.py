from __future__ import annotations

import unittest

from event_engineering.evolution import UpcasterChain, compare_object_schemas
from event_engineering.replay import ReplayPlan, execute_replay

from helpers import event


class EvolutionReplayTests(unittest.TestCase):
    def test_optional_addition_accepted(self) -> None:
        old = {"type": "object", "properties": {"runId": {"type": "string"}}, "required": ["runId"]}
        new = {"type": "object", "properties": {"runId": {"type": "string"}, "summary": {"type": "string"}}, "required": ["runId"]}
        report = compare_object_schemas(old, new)
        self.assertEqual(report.status, "accepted")

    def test_required_addition_rejected(self) -> None:
        old = {"type": "object", "properties": {"runId": {"type": "string"}}, "required": ["runId"]}
        new = {"type": "object", "properties": {"runId": {"type": "string"}, "region": {"type": "string"}}, "required": ["runId", "region"]}
        self.assertEqual(compare_object_schemas(old, new).status, "rejected")

    def test_enum_expansion_requires_review(self) -> None:
        old = {"type": "object", "properties": {"kind": {"type": "string", "enum": ["full"]}}}
        new = {"type": "object", "properties": {"kind": {"type": "string", "enum": ["full", "partial"]}}}
        self.assertEqual(compare_object_schemas(old, new).status, "review-required")

    def test_upcaster_chain(self) -> None:
        chain = UpcasterChain()
        chain.register(1, 2, lambda value: {**value, "summary": None})
        self.assertEqual(chain.apply({"runId": "r"}, 1, 2), {"runId": "r", "summary": None})

    def test_bounded_dry_replay(self) -> None:
        events = [event("30"), event("31")]
        plan = ReplayPlan(
            replay_id="r1",
            consumer="analytics:v2",
            mode="dry-run",
            allowed_types=frozenset({events[0].type}),
            maximum_events=2,
            side_effects="disabled",
        )
        report = execute_replay(plan, events, lambda _, dry: dry)
        self.assertEqual((report.selected, report.would_apply), (2, 2))

    def test_replay_bound_enforced(self) -> None:
        events = [event("32"), event("33")]
        plan = ReplayPlan("r2", "analytics:v2", "apply", frozenset({events[0].type}), 1, "disabled")
        with self.assertRaises(RuntimeError):
            execute_replay(plan, events, lambda *_: True)


if __name__ == "__main__":
    unittest.main()
