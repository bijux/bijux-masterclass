from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

from analysis_rpc import analysis_pb2
from analysis_rpc.deadlines import Deadline, RetryPolicy
from analysis_rpc.errors import (
    Aborted, AlreadyExists, FailedPrecondition, InvalidArgument,
    NotFound, PermissionDenied, ResourceExhausted, Unauthenticated,
)
from analysis_rpc.lifecycle import Lifecycle, Phase
from analysis_rpc.models import Principal, State, advance, request_fingerprint
from analysis_rpc.security import authenticate, require, require_tenant
from analysis_rpc.store import InMemoryAnalysisStore
from analysis_rpc.streaming import chunk_bytes, parse_upload


WRITE = Principal(
    "user-write",
    "tenant-a",
    frozenset({"runs:read", "runs:write", "datasets:write", "artifacts:read"}),
)
WORKER = Principal("worker-1", "tenant-a", frozenset({"worker:connect"}), "worker")


class Clock:
    def __init__(self) -> None:
        self.value = 0.0
    def __call__(self) -> float:
        return self.value


class ProtobufModelTests(unittest.TestCase):
    def test_optional_presence_distinguishes_absent_and_empty(self) -> None:
        run = analysis_pb2.AnalysisRun()
        self.assertFalse(run.HasField("result_summary"))
        run.result_summary = ""
        self.assertTrue(run.HasField("result_summary"))
        self.assertEqual(run.result_summary, "")

    def test_int64_above_javascript_safe_integer_round_trips(self) -> None:
        value = 9_007_199_254_740_992
        run = analysis_pb2.AnalysisRun(revision=value)
        parsed = analysis_pb2.AnalysisRun.FromString(run.SerializeToString())
        self.assertEqual(parsed.revision, value)

    def test_oneof_upload_frame(self) -> None:
        frame = analysis_pb2.UploadDatasetRequest(chunk=b"x")
        self.assertEqual(frame.WhichOneof("frame"), "chunk")
        frame.metadata.parent = "projects/p-1"
        self.assertEqual(frame.WhichOneof("frame"), "metadata")
        self.assertEqual(frame.chunk, b"")

    def test_enum_zero_is_unspecified(self) -> None:
        self.assertEqual(analysis_pb2.RUN_STATE_UNSPECIFIED, 0)

    def test_golden_bytes_match_manifest(self) -> None:
        root = Path(__file__).parents[3]
        body = (root / "shared/golden/analysis-run-v1.bin").read_bytes()
        meta = json.loads((root / "shared/golden/analysis-run-v1.json").read_text())
        self.assertEqual(sha256(body).hexdigest(), meta["sha256"])
        run = analysis_pb2.AnalysisRun.FromString(body)
        self.assertEqual(run.name, "projects/p-1/runs/r-golden")
        self.assertTrue(run.HasField("result_summary"))


class DomainAndStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = InMemoryAnalysisStore()

    def create(self, request_id: str = "req-1"):
        return self.store.create_run(
            parent="projects/p-1",
            request_id=request_id,
            dataset_name="datasets/d-1",
            algorithm="qc",
            principal=WRITE,
        )

    def test_fingerprint_is_stable(self) -> None:
        args = dict(
            parent="projects/p-1", dataset_name="datasets/d-1",
            algorithm="qc", principal=WRITE,
        )
        self.assertEqual(request_fingerprint(**args), request_fingerprint(**args))

    def test_idempotency_replays(self) -> None:
        first = self.create()
        second = self.create()
        self.assertEqual(first.name, second.name)

    def test_idempotency_rejects_changed_input(self) -> None:
        self.create()
        with self.assertRaises(AlreadyExists):
            self.store.create_run(
                parent="projects/p-1",
                request_id="req-1",
                dataset_name="datasets/d-2",
                algorithm="qc",
                principal=WRITE,
            )

    def test_get_conceals_foreign_tenant(self) -> None:
        run = self.create()
        foreign = Principal("user-b", "tenant-b", WRITE.scopes)
        with self.assertRaises(NotFound):
            self.store.get_run(run.name, foreign)

    def test_stale_etag_aborts(self) -> None:
        run = self.create()
        with self.assertRaises(Aborted):
            self.store.cancel_run(
                name=run.name, etag='"run-0"',
                request_id="cancel-1", principal=WRITE,
            )

    def test_cancel_is_idempotent_for_cancelled_state(self) -> None:
        run = self.create()
        cancelled = self.store.cancel_run(
            name=run.name, etag=run.etag,
            request_id="cancel-1", principal=WRITE,
        )
        replay = self.store.cancel_run(
            name=run.name, etag=cancelled.etag,
            request_id="cancel-1", principal=WRITE,
        )
        self.assertEqual(replay.state, State.CANCELLED)

    def test_terminal_run_cannot_cancel(self) -> None:
        run = self.create()
        completed = self.store.advance_run(
            run.name, state=State.COMPLETED, progress=100, result="ok"
        )
        with self.assertRaises(FailedPrecondition):
            self.store.cancel_run(
                name=completed.name, etag=completed.etag,
                request_id="cancel-2", principal=WRITE,
            )

    def test_watch_sequences_are_monotonic(self) -> None:
        run = self.create()
        self.store.advance_run(run.name, state=State.RUNNING, progress=10)
        events = self.store.watch(run.name, 0, WRITE)
        self.assertEqual([event.sequence for event in events], [1, 2])

    def test_stale_assignment_generation_rejected(self) -> None:
        run = self.create()
        assignment = self.store.assign("worker-1", "tenant-a", 1)
        self.assertIsNotNone(assignment)
        assert assignment is not None
        self.store.advance_run(run.name, state=State.RUNNING, progress=1)
        with self.assertRaises(FailedPrecondition):
            self.store.complete_assignment(
                assignment_id=assignment.assignment_id,
                worker_id="worker-1",
                generation=assignment.lease_generation,
                success=True,
                result_summary="ok",
                failure_code="",
            )


class DeadlineSecurityLifecycleTests(unittest.TestCase):
    def test_child_deadline_uses_remaining_budget(self) -> None:
        clock = Clock()
        deadline = Deadline.after(5, clock)
        clock.value = 2
        self.assertEqual(deadline.child_timeout(reserve=0.5, cap=10), 2.5)

    def test_retry_requires_idempotency_for_mutation(self) -> None:
        policy = RetryPolicy(
            max_attempts=3, initial_backoff=0.1, multiplier=2,
            max_backoff=1, retryable_statuses=frozenset({"UNAVAILABLE"})
        )
        self.assertFalse(policy.allows(
            method="CreateRun", status="UNAVAILABLE", attempt=1,
            idempotent=False, remaining=2, next_delay=0.1,
        ))
        self.assertTrue(policy.allows(
            method="CreateRun", status="UNAVAILABLE", attempt=1,
            idempotent=True, remaining=2, next_delay=0.1,
        ))

    def test_duplicate_credentials_rejected(self) -> None:
        metadata = (
            type("M", (), {"key":"authorization","value":"Bearer learner-write"})(),
            type("M", (), {"key":"authorization","value":"Bearer learner-read"})(),
        )
        with self.assertRaises(Unauthenticated):
            authenticate(metadata)

    def test_scope_and_tenant_enforced(self) -> None:
        read = Principal("r", "tenant-a", frozenset({"runs:read"}))
        with self.assertRaises(PermissionDenied):
            require(read, "runs:write")
        with self.assertRaises(PermissionDenied):
            require_tenant(WRITE, "projects/p-b-1")

    def test_lifecycle_stops_admission_during_drain(self) -> None:
        life = Lifecycle()
        life.start()
        life.admit()
        life.drain()
        self.assertFalse(life.serving())
        with self.assertRaises(RuntimeError):
            life.admit()
        life.stop()
        self.assertEqual(life.phase, Phase.STOPPING)
        life.release()
        self.assertEqual(life.phase, Phase.STOPPED)


class StreamingTests(unittest.TestCase):
    def test_upload_metadata_must_be_first(self) -> None:
        with self.assertRaises(InvalidArgument):
            parse_upload([analysis_pb2.UploadDatasetRequest(chunk=b"x")])

    def test_upload_limits_and_digest(self) -> None:
        body = b"course-seven"
        digest = sha256(body).hexdigest()
        frames = [
            analysis_pb2.UploadDatasetRequest(
                metadata=analysis_pb2.UploadMetadata(
                    parent="projects/p-1", request_id="u-1",
                    filename="x.bin", media_type="application/octet-stream",
                    sha256=digest, expected_size_bytes=len(body),
                )
            ),
            analysis_pb2.UploadDatasetRequest(chunk=body),
        ]
        parsed = parse_upload(frames, max_chunk_bytes=64, max_total_bytes=64)
        self.assertEqual(b"".join(parsed.chunks), body)

    def test_upload_rejects_oversized_chunk(self) -> None:
        frames = [
            analysis_pb2.UploadDatasetRequest(
                metadata=analysis_pb2.UploadMetadata(
                    parent="projects/p-1", request_id="u-1",
                    filename="x.bin",
                )
            ),
            analysis_pb2.UploadDatasetRequest(chunk=b"xx"),
        ]
        with self.assertRaises(ResourceExhausted):
            parse_upload(frames, max_chunk_bytes=1, max_total_bytes=8)

    def test_chunk_bytes_is_ordered_and_complete(self) -> None:
        chunks = list(chunk_bytes(b"abcdef", chunk_size=2))
        self.assertEqual([offset for offset, _, _ in chunks], [0, 2, 4])
        self.assertTrue(chunks[-1][2])


if __name__ == "__main__":
    unittest.main()
