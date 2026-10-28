import pytest

from api_security.edge import evaluate_edge
from api_security.errors import SecurityControlError


def test_shared_edge_vectors(vector_loader):
    for case in vector_loader("edge.json")["cases"]:
        kwargs = dict(
            peer=case["peer"],
            headers=[tuple(x) for x in case["headers"]],
            trusted_proxies=case.get("trustedProxies", []),
            allowed_hosts=case.get("allowedHosts", ["api.example.test"]),
        )
        if case["valid"]:
            assert evaluate_edge(**kwargs).origin == case["origin"]
        else:
            with pytest.raises(SecurityControlError) as caught:
                evaluate_edge(**kwargs)
            assert caught.value.code == case["error"]


def test_network_trusted_proxy_range():
    context = evaluate_edge(
        peer="10.1.2.3",
        headers=[("host", "internal:8000"), ("x-forwarded-host", "api.example.test"), ("x-forwarded-proto", "https")],
        trusted_proxies=["10.0.0.0/8"],
        allowed_hosts=["api.example.test"],
    )
    assert context.trusted_proxy is True
