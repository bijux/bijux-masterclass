from __future__ import annotations

import unittest

from api_performance.identity import IdentityError, canonical_json_bytes, sha256_identity
from api_performance.models import (
    BenchmarkEnvelope,
    CorrectnessReport,
    EnvironmentFingerprint,
    ModelError,
    OutcomeCounts,
    WorkloadSpec,
)


class IdentityTests(unittest.TestCase):
    def test_sorted_identity_is_stable(self) -> None:
        left = {"b": 2, "a": {"y": 2, "x": 1}}
        right = {"a": {"x": 1, "y": 2}, "b": 2}
        self.assertEqual(canonical_json_bytes(left), canonical_json_bytes(right))
        self.assertEqual(sha256_identity(left), sha256_identity(right))

    def test_non_finite_rejected(self) -> None:
        with self.assertRaises(IdentityError):
            canonical_json_bytes({"value": float("nan")})

    def test_unsupported_type_rejected(self) -> None:
        with self.assertRaises(IdentityError):
            canonical_json_bytes({"value": {1, 2}})


class ModelTests(unittest.TestCase):
    def workload(self, **overrides: object) -> WorkloadSpec:
        values = {
            "id": "WL-RUN-LIST",
            "model": "open",
            "rate_per_second": 120.0,
            "duration_seconds": 60,
            "dataset_id": "DS-MEDIUM",
            "request_mix": {"listRuns": 1.0},
        }
        values.update(overrides)
        return WorkloadSpec(**values)

    def environment(self) -> EnvironmentFingerprint:
        return EnvironmentFingerprint(
            runtime="python",
            runtime_version="3.13.5",
            cpu_logical=4,
            memory_limit_bytes=1_073_741_824,
            process_count=1,
            worker_count=1,
            source_revision="abc123",
            dataset_id="DS-MEDIUM",
            database_profile="local",
        )

    def test_annotations_do_not_change_workload_identity(self) -> None:
        a = self.workload(annotations={"note": "a"})
        b = self.workload(annotations={"note": "b"})
        self.assertEqual(a.identity, b.identity)

    def test_semantic_field_changes_identity(self) -> None:
        self.assertNotEqual(
            self.workload(rate_per_second=100).identity,
            self.workload(rate_per_second=120).identity,
        )

    def test_invalid_mix_rejected(self) -> None:
        with self.assertRaises(ModelError):
            self.workload(request_mix={"a": 0.4, "b": 0.4})

    def test_environment_identity(self) -> None:
        env = self.environment()
        self.assertTrue(env.identity.startswith("sha256:"))

    def test_correctness_conjunction(self) -> None:
        report = CorrectnessReport(True, {"contract": True, "security": True})
        self.assertTrue(report.passed)
        with self.assertRaises(ModelError):
            CorrectnessReport(True, {"contract": False})

    def test_outcome_validation(self) -> None:
        counts = OutcomeCounts(100, 100, 90, 100, 10, 0, 0)
        self.assertEqual(counts.schedule_coverage, 1.0)
        with self.assertRaises(ModelError):
            OutcomeCounts(100, 101, 100, 100, 0, 0, 0)

    def test_publishable_envelope(self) -> None:
        workload = self.workload()
        env = self.environment()
        envelope = BenchmarkEnvelope(
            profile_version="1.0",
            workload_id=workload.id,
            workload_hash=workload.identity,
            environment_hash=env.identity,
            evidence_class="B",
            correctness=CorrectnessReport(True, {"contract": True}),
            outcomes=OutcomeCounts(10, 10, 10, 10, 0, 0, 0),
            summary={"p95Ms": "10"},
            source_revision="abc123",
        )
        self.assertTrue(envelope.publishable)


if __name__ == "__main__":
    unittest.main()
