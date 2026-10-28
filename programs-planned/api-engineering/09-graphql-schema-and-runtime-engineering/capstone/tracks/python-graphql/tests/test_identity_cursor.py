import unittest

from graph_api.cursor import (
    CursorCodec,
    CursorState,
    audience_hash,
    normalized_filter_hash,
)
from graph_api.identity import decode_global_id, encode_global_id
from graph_api.model import Principal, ValidationError


class IdentityCursorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.codec = CursorCodec(b"0123456789abcdef0123456789abcdef")
        self.principal = Principal(
            "learner",
            "tenant-a",
            frozenset({"RUN_READ"}),
        )
        self.filter_hash = normalized_filter_hash({"status": "RUNNING"})
        self.state = CursorState(
            tenant_id="tenant-a",
            audience_hash=audience_hash(self.principal),
            scope="Query.analysisRuns",
            filter_hash=self.filter_hash,
            after_primary="2026-08-02T10:00:00Z",
            after_tiebreaker="run-2",
            high_water_primary="2026-08-03T10:00:00Z",
            high_water_tiebreaker="run-3",
            expires_at=2_000_000_000,
        )

    def test_global_id_roundtrip(self):
        value = encode_global_id("AnalysisRun", "run-1")
        self.assertEqual(decode_global_id(value), ("AnalysisRun", "run-1"))

    def test_global_id_rejects_unknown_type(self):
        with self.assertRaises(ValidationError):
            encode_global_id("Secret", "x")

    def test_cursor_binds_query_population(self):
        value = self.codec.encode(self.state)
        decoded = self.codec.decode(
            value,
            tenant_id="tenant-a",
            audience_hash=audience_hash(self.principal),
            scope="Query.analysisRuns",
            filter_hash=self.filter_hash,
            now_epoch=1_900_000_000,
        )
        self.assertEqual(decoded.after_key, self.state.after_key)
        self.assertEqual(decoded.high_water_key, self.state.high_water_key)

        with self.assertRaises(ValidationError):
            self.codec.decode(
                value,
                tenant_id="tenant-b",
                audience_hash=audience_hash(self.principal),
                scope="Query.analysisRuns",
                filter_hash=self.filter_hash,
                now_epoch=1_900_000_000,
            )

    def test_cursor_detects_scope_filter_audience_expiry_and_tampering(self):
        value = self.codec.encode(self.state)
        wrong_principal = Principal("other", "tenant-a", frozenset({"RUN_READ"}))
        invalid = [
            dict(scope="Project.analysisRuns"),
            dict(filter_hash=normalized_filter_hash({"status": "FAILED"})),
            dict(audience_hash=audience_hash(wrong_principal)),
            dict(now_epoch=2_000_000_001),
        ]
        base = {
            "tenant_id": "tenant-a",
            "audience_hash": audience_hash(self.principal),
            "scope": "Query.analysisRuns",
            "filter_hash": self.filter_hash,
            "now_epoch": 1_900_000_000,
        }
        for override in invalid:
            with self.subTest(override=override), self.assertRaises(ValidationError):
                self.codec.decode(value, **{**base, **override})

        changed = value[:-1] + ("A" if value[-1] != "A" else "B")
        with self.assertRaises(ValidationError):
            self.codec.decode(changed, **base)
