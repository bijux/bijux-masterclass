import pytest

from api_security.authorization import Policy
from api_security.errors import SecurityControlError
from api_security.gateway import CredentialInputs, authenticate_exactly_one, security_decision
from api_security.models import Principal, ResourceFacts

P = Principal("u1", "t1", frozenset({"projects:read"}))


def validator(_value: str) -> Principal:
    return P


def test_exactly_one_credential_channel():
    assert authenticate_exactly_one(CredentialInputs(bearer_token="x"), bearer_validator=validator, api_key_validator=validator) == P
    with pytest.raises(SecurityControlError) as caught:
        authenticate_exactly_one(CredentialInputs(), bearer_validator=validator, api_key_validator=validator)
    assert caught.value.code == "credential-required"
    with pytest.raises(SecurityControlError) as caught:
        authenticate_exactly_one(CredentialInputs("x", "y"), bearer_validator=validator, api_key_validator=validator)
    assert caught.value.code == "credential-ambiguous"


def test_integrated_authentication_and_authorization():
    policies = {"getProject": Policy("getProject", frozenset({"projects:read"}), relationship="owner", conceal=True)}
    principal, decision = security_decision("getProject", inputs=CredentialInputs(bearer_token="x"), resource=ResourceFacts(tenant="t1", owner="u1"), policies=policies, bearer_validator=validator, api_key_validator=validator)
    assert principal == P and decision.allowed
    _, denied = security_decision("getProject", inputs=CredentialInputs(bearer_token="x"), resource=ResourceFacts(tenant="t2", owner="u2"), policies=policies, bearer_validator=validator, api_key_validator=validator)
    assert not denied.allowed and denied.conceal
