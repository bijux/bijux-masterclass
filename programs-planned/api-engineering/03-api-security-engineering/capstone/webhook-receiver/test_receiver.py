from api_security.secrets import SecretBytes
from api_security.webhooks import MemoryReplayStore, sign_webhook, verify_webhook


def test_receiver_profile_round_trip():
    secret = SecretBytes("fixture-webhook-secret")
    body = b'{"event":"analysis.completed"}'
    signature = sign_webhook(secret=secret, timestamp=1000, delivery_id="d1", key_id="k1", body=body)
    verify_webhook(body=body, timestamp=1000, delivery_id="d1", key_id="k1", signature=signature, now=1000, keys={"k1": secret}, replay=MemoryReplayStore())
