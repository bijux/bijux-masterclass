import json
import unittest
from pathlib import Path

from distributed_api.capability import CapabilityAuthority, CapabilityClaims
from distributed_api.model import Unauthorized
from distributed_api.saga import ArtifactCompletionSaga, SagaState


CAPSTONE = Path(__file__).resolve().parents[3]
CAPABILITY_VECTOR = CAPSTONE / "shared" / "vectors" / "capability.json"


class CapabilitySagaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.authority = CapabilityAuthority(
            issuer="control",
            key=b"0123456789abcdef0123456789abcdef",
        )

    def claims(self, **overrides: object) -> CapabilityClaims:
        values: dict[str, object] = {
            "jti": "j1",
            "issuer": "control",
            "audience": "artifact-service",
            "subject": "u",
            "tenant": "t",
            "resource": "r",
            "action": "artifact:upload",
            "issued_at": 10,
            "expires_at": 20,
            "sha256": "abc",
            "max_bytes": 10,
        }
        values.update(overrides)
        return CapabilityClaims(**values)  # type: ignore[arg-type]

    def test_capability_round_trip(self) -> None:
        token = self.authority.mint(self.claims())
        out = self.authority.verify(
            token,
            audience="artifact-service",
            tenant="t",
            action="artifact:upload",
            now=11,
        )
        self.assertEqual(out.resource, "r")

    def test_wrong_audience_rejected(self) -> None:
        token = self.authority.mint(self.claims())
        with self.assertRaises(Unauthorized):
            self.authority.verify(
                token,
                audience="control",
                tenant="t",
                action="artifact:upload",
                now=11,
            )

    def test_tampering_rejected(self) -> None:
        token = self.authority.mint(self.claims())
        altered = token[:-1] + ("A" if token[-1] != "A" else "B")
        with self.assertRaises(Unauthorized):
            self.authority.verify(
                altered,
                audience="artifact-service",
                tenant="t",
                action="artifact:upload",
                now=11,
            )

    def test_python_matches_cross_language_golden_token(self) -> None:
        vector = json.loads(CAPABILITY_VECTOR.read_text())["interoperability"]
        wire = vector["claims"]
        authority = CapabilityAuthority(
            issuer=wire["issuer"],
            key=vector["key_utf8"].encode("utf-8"),
        )
        claims = CapabilityClaims(
            jti=wire["jti"],
            issuer=wire["issuer"],
            audience=wire["audience"],
            subject=wire["subject"],
            tenant=wire["tenant"],
            resource=wire["resource"],
            action=wire["action"],
            issued_at=wire["issued_at"],
            expires_at=wire["expires_at"],
            sha256=wire["sha256"],
            max_bytes=wire["max_bytes"],
        )
        self.assertEqual(authority.mint(claims), vector["expected_token"])

    def test_saga_happy_path_and_duplicates(self) -> None:
        saga = ArtifactCompletionSaga("s", "r", "a")
        self.assertEqual(
            saga.record_artifact(
                event_id="e",
                artifact_id="x",
                attempt_id="a",
            ),
            "stored",
        )
        self.assertEqual(
            saga.record_artifact(
                event_id="e",
                artifact_id="x",
                attempt_id="a",
            ),
            "duplicate",
        )
        self.assertEqual(
            saga.complete(command_id="c", current_attempt_id="a"),
            "completed",
        )
        self.assertEqual(saga.state, SagaState.COMPLETED)

    def test_stale_attempt_requires_compensation(self) -> None:
        saga = ArtifactCompletionSaga("s", "r", "a")
        self.assertEqual(
            saga.record_artifact(
                event_id="e",
                artifact_id="x",
                attempt_id="old",
            ),
            "compensate",
        )
        self.assertEqual(saga.compensate(action_id="comp"), "compensated")


if __name__ == "__main__":
    unittest.main()
