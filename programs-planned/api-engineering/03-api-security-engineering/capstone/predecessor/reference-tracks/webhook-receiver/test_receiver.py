from hmac import new as hmac_new
import json
import time

from receiver import verify_signature


def test_signature_vector() -> None:
    body = json.dumps({"eventId": "evt_0001"}, separators=(",", ":")).encode()
    timestamp = str(int(time.time()))
    secret = "course-callback-signing-secret"
    signature = "sha256=" + hmac_new(secret.encode(), timestamp.encode() + b"." + body, "sha256").hexdigest()
    assert verify_signature(secret, timestamp, body, signature)


def test_changed_body_is_rejected() -> None:
    body = b"{}"
    timestamp = "1700000000"
    secret = "course-callback-signing-secret"
    signature = "sha256=" + hmac_new(secret.encode(), timestamp.encode() + b"." + body, "sha256").hexdigest()
    assert not verify_signature(secret, timestamp, b'{"changed":true}', signature)
