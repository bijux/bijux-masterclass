import pytest

from api_security.api_keys import ApiKeyRecord, digest_api_key, verify_api_key
from api_security.errors import SecurityControlError
from api_security.secrets import SecretBytes


def test_api_key_digest_and_verification():
    pepper = SecretBytes("fixture-pepper")
    raw = "ak_key01.high-entropy-fixture-secret"
    record = ApiKeyRecord("key01", "user-01", "tenant-01", digest_api_key(raw, pepper), frozenset({"projects:read"}))
    principal = verify_api_key(raw, records={"key01": record}, pepper=pepper, now=100)
    assert principal.subject == "user-01"
    with pytest.raises(SecurityControlError):
        verify_api_key("ak_key01.wrong", records={"key01": record}, pepper=pepper, now=100)


def test_revoked_api_key_fails():
    pepper = SecretBytes("pepper")
    raw = "ak_x.secret"
    record = ApiKeyRecord("x", "u", "t", digest_api_key(raw, pepper), frozenset(), revoked=True)
    with pytest.raises(SecurityControlError):
        verify_api_key(raw, records={"x":record}, pepper=pepper, now=0)
