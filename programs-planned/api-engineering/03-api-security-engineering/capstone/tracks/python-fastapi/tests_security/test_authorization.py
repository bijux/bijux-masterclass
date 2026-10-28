from pathlib import Path

from api_security.authorization import authorize
from api_security.models import Principal, ResourceFacts
from api_security.runtime import load_policy_matrix


def principal(raw):
    if raw is None:
        return None
    return Principal(
        raw["sub"], raw["tenant"], frozenset(raw.get("scopes", [])),
        frozenset(raw.get("roles", [])), assurance=raw.get("assurance", "baseline"),
        auth_age_seconds=raw.get("authAgeSeconds", 0),
    )


def resource(raw):
    return ResourceFacts(raw.get("tenant"), raw.get("owner"), frozenset(raw.get("members", [])), raw.get("creator"), raw.get("status"))


def test_shared_authorization_vectors(vector_loader):
    from conftest import POLICIES
    policies = load_policy_matrix(POLICIES)
    for case in vector_loader("authorization.json")["cases"]:
        decision = authorize(case["operationId"], principal=principal(case.get("principal")), resource=resource(case.get("resource", {})), policies=policies)
        assert decision.allowed is case["allow"], case["id"]
        if case.get("conceal"):
            assert decision.conceal


def test_unknown_operation_default_denies():
    from conftest import POLICIES
    decision = authorize("newUnmappedOperation", principal=Principal("u","t",frozenset({"all"})), resource=ResourceFacts(tenant="t",owner="u"), policies=load_policy_matrix(POLICIES))
    assert not decision.allowed and decision.reason == "policy.missing"
