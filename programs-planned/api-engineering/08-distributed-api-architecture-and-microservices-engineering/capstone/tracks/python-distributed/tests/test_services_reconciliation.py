import hashlib
import unittest

from distributed_api.capability import CapabilityAuthority
from distributed_api.model import Conflict, RequestContext, RunState, ValidationError
from distributed_api.reconciliation import reconcile
from distributed_api.services import (
    AnalysisControlService,
    ArtifactService,
    Gateway,
    NotificationService,
)
from distributed_api.tour import run_tour


class ServiceReconciliationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.authority = CapabilityAuthority(
            issuer="analysis-control",
            key=b"course-eight-capability-key",
        )
        self.control = AnalysisControlService(self.authority)
        self.artifacts = ArtifactService(self.authority)
        self.notifications = NotificationService()
        self.ctx = RequestContext(
            "u",
            "tenant-a",
            "gateway",
            frozenset({"runs:read", "runs:write"}),
            10_000,
        )

    def complete(self):
        run = self.control.create_run(
            self.ctx,
            request_id="req",
            dataset_id="d",
        )
        self.control.start(run.run_id)
        body = b"result"
        digest = hashlib.sha256(body).hexdigest()
        token = self.control.mint_upload_capability(
            self.ctx,
            run_id=run.run_id,
            sha256=digest,
            max_bytes=10,
            now=1,
        )
        artifact = self.artifacts.store(
            token=token,
            tenant="tenant-a",
            content=body,
            now=2,
        )
        self.control.attach_and_complete(
            run_id=run.run_id,
            attempt_id=run.attempt_id,
            artifact_id=artifact.artifact_id,
            event_id="done",
        )
        event = next(
            item for item in self.control.events if item.get("event_id") == "done"
        )
        self.notifications.consume(event)
        return run, artifact

    def test_end_to_end_completion(self) -> None:
        run, artifact = self.complete()
        self.assertEqual(self.control.runs[run.run_id].state, RunState.COMPLETED)
        view = Gateway(self.control, self.artifacts).get_run_view(
            self.ctx,
            run.run_id,
        )
        self.assertFalse(view.partial)
        self.assertEqual(
            view.value["artifacts"][0]["artifact_id"],
            artifact.artifact_id,
        )

    def test_partial_view_is_explicit(self) -> None:
        run, _ = self.complete()
        view = Gateway(self.control, self.artifacts).get_run_view(
            self.ctx,
            run.run_id,
            artifact_available=False,
        )
        self.assertTrue(view.partial)
        self.assertIn("artifactsUnavailable", view.warnings)
        self.assertEqual(view.value["artifacts"], [])

    def test_artifact_store_is_idempotent_and_copies_input(self) -> None:
        run = self.control.create_run(
            self.ctx,
            request_id="req",
            dataset_id="d",
        )
        self.control.start(run.run_id)
        body = bytearray(b"result")
        digest = hashlib.sha256(body).hexdigest()
        token = self.control.mint_upload_capability(
            self.ctx,
            run_id=run.run_id,
            sha256=digest,
            max_bytes=10,
            now=1,
        )
        first = self.artifacts.store(
            token=token,
            tenant="tenant-a",
            content=bytes(body),
            now=2,
        )
        second = self.artifacts.store(
            token=token,
            tenant="tenant-a",
            content=bytes(body),
            now=2,
        )
        body[:] = b"xxxxxx"
        self.assertEqual(first.artifact_id, second.artifact_id)
        self.assertEqual(first.content, b"result")

    def test_upload_capability_requires_running_attempt(self) -> None:
        run = self.control.create_run(
            self.ctx,
            request_id="not-running",
            dataset_id="d",
        )
        with self.assertRaises(Conflict):
            self.control.mint_upload_capability(
                self.ctx,
                run_id=run.run_id,
                sha256="0" * 64,
                max_bytes=10,
                now=1,
            )

    def test_checksum_mismatch_rejected(self) -> None:
        run = self.control.create_run(
            self.ctx,
            request_id="req",
            dataset_id="d",
        )
        self.control.start(run.run_id)
        token = self.control.mint_upload_capability(
            self.ctx,
            run_id=run.run_id,
            sha256="0" * 64,
            max_bytes=10,
            now=1,
        )
        with self.assertRaises(ValidationError):
            self.artifacts.store(
                token=token,
                tenant="tenant-a",
                content=b"result",
                now=2,
            )

    def test_stale_attempt_rejected(self) -> None:
        run, artifact = self.complete()
        with self.assertRaises(Conflict):
            self.control.attach_and_complete(
                run_id=run.run_id,
                attempt_id="old",
                artifact_id=artifact.artifact_id,
                event_id="x",
            )

    def test_notification_is_idempotent(self) -> None:
        self.complete()
        event = next(
            item for item in self.control.events if item.get("event_id") == "done"
        )
        self.assertEqual(self.notifications.consume(event), "duplicate")

    def test_reconciliation_findings(self) -> None:
        findings = reconcile(
            control_artifact_refs=set(),
            artifact_ids={"a"},
            completed_runs={"r"},
            notification_run_ids=set(),
        )
        self.assertEqual(findings, ["orphan-artifact:a", "missing-notification:r"])

    def test_tour(self) -> None:
        result = run_tour()
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["reconciliation"], [])


if __name__ == "__main__":
    unittest.main()
