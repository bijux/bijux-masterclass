import pytest

from api_security.errors import SecurityControlError
from api_security.strict_json import parse_strict_json


def test_shared_strict_json_vectors(vector_loader):
    for case in vector_loader("strict-json.json")["cases"]:
        kwargs = {"max_depth": case.get("maxDepth", 32)}
        if case["valid"]:
            assert parse_strict_json(case["text"].encode(), **kwargs) is not None
        else:
            with pytest.raises(SecurityControlError) as caught:
                parse_strict_json(case["text"].encode(), **kwargs)
            assert caught.value.code == case["error"]


def test_malformed_utf8_and_byte_limit():
    with pytest.raises(SecurityControlError, match="not valid UTF-8"):
        parse_strict_json(b'{"x":"\xff"}')
    with pytest.raises(SecurityControlError) as caught:
        parse_strict_json(b'{"long":"12345"}', max_bytes=5)
    assert caught.value.status == 413
