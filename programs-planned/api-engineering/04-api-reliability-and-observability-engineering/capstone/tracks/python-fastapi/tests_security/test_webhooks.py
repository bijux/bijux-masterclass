import pytest

from api_security.errors import SecurityControlError
from api_security.secrets import SecretBytes
from api_security.webhooks import MemoryReplayStore, sign_webhook, verify_webhook


def test_shared_webhook_vectors(vector_loader):
    data=vector_loader("webhook.json")
    secret=SecretBytes(data["secret"])
    valid_case=data["cases"][0]
    valid_sig=sign_webhook(secret=secret,timestamp=valid_case["timestamp"],delivery_id=valid_case["deliveryId"],key_id=valid_case["keyId"],body=valid_case["body"].encode())
    replay=MemoryReplayStore()
    verify_webhook(body=valid_case["body"].encode(),timestamp=valid_case["timestamp"],delivery_id=valid_case["deliveryId"],key_id=valid_case["keyId"],signature=valid_sig,now=valid_case["timestamp"],keys={valid_case["keyId"]:secret},replay=replay)
    altered=data["cases"][1]
    with pytest.raises(SecurityControlError):
        verify_webhook(body=altered["body"].encode(),timestamp=altered["timestamp"],delivery_id=altered["deliveryId"]+"x",key_id=altered["keyId"],signature=valid_sig,now=altered["timestamp"],keys={altered["keyId"]:secret},replay=MemoryReplayStore())
    stale=data["cases"][2]
    stale_sig=sign_webhook(secret=secret,timestamp=stale["timestamp"],delivery_id=stale["deliveryId"],key_id=stale["keyId"],body=stale["body"].encode())
    with pytest.raises(SecurityControlError) as caught:
        verify_webhook(body=stale["body"].encode(),timestamp=stale["timestamp"],delivery_id=stale["deliveryId"],key_id=stale["keyId"],signature=stale_sig,now=stale["now"],keys={stale["keyId"]:secret},replay=MemoryReplayStore(),max_age_seconds=stale["maxAge"])
    assert caught.value.code=="webhook-stale"
    with pytest.raises(SecurityControlError) as caught:
        verify_webhook(body=valid_case["body"].encode(),timestamp=valid_case["timestamp"],delivery_id=valid_case["deliveryId"],key_id=valid_case["keyId"],signature=valid_sig,now=valid_case["timestamp"],keys={valid_case["keyId"]:secret},replay=replay)
    assert caught.value.code=="webhook-replay"
