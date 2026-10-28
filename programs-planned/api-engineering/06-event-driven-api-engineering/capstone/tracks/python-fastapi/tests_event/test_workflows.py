from __future__ import annotations

import unittest

from event_engineering.workflows import RunProcessManager, RunProcessState

from helpers import event


class WorkflowTests(unittest.TestCase):
    def test_requested_creates_stable_command_identity(self) -> None:
        manager = RunProcessManager()
        state = RunProcessState("run-001")
        requested = event(
            "60",
            event_type="org.bijux.analysis.run.requested.v1",
            data={"runId": "run-001", "requestedAt": "2026-08-07T10:00:00Z"},
        )
        self.assertEqual(manager.apply(state, requested), "applied")
        self.assertEqual(state.command_id, "start:run-001:1")
        self.assertEqual(manager.apply(state, requested), "duplicate")

    def test_terminal_state_is_monotonic(self) -> None:
        manager = RunProcessManager()
        state = RunProcessState("run-001")
        requested = event(
            "61",
            event_type="org.bijux.analysis.run.requested.v1",
            data={"runId": "run-001", "requestedAt": "2026-08-07T10:00:00Z"},
        )
        completed = event("62")
        manager.apply(state, requested)
        manager.apply(state, completed)
        self.assertEqual(state.status, "completed")
        self.assertEqual(manager.timeout(state, state.generation), "stale")

    def test_impossible_completion_is_rejected(self) -> None:
        manager = RunProcessManager()
        state = RunProcessState("run-001")
        with self.assertRaises(ValueError):
            manager.apply(state, event("63"))


if __name__ == "__main__":
    unittest.main()
