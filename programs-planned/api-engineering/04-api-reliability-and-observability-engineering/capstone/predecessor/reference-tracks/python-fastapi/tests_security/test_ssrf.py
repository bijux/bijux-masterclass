import pytest

from api_security.errors import SecurityControlError
from api_security.ssrf import validate_destination, verify_connected_peer


def test_shared_ssrf_vectors(vector_loader):
    for case in vector_loader("ssrf.json")["cases"]:
        kwargs={"url":case["url"],"addresses":case["addresses"],"allowed_ports":case.get("allowedPorts",[443])}
        if case["valid"]:
            destination=validate_destination(**kwargs)
            verify_connected_peer(destination,case["addresses"][0])
        else:
            with pytest.raises(SecurityControlError):
                validate_destination(**kwargs)


def test_connected_peer_must_be_approved():
    destination=validate_destination("https://hooks.example.test/x",addresses=["93.184.216.34"])
    with pytest.raises(SecurityControlError) as caught:
        verify_connected_peer(destination,"8.8.8.8")
    assert caught.value.code=="peer-mismatch"
