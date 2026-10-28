import json
from pathlib import Path

import jwt
import pytest

from api_security.errors import SecurityControlError
from api_security.tokens import MemoryRevocations, TokenProfile, validate_access_token

NOW = 1_760_000_000


def _fixture(vector_loader):
    from conftest import IDENTITY, load_issuer
    issuer = load_issuer()
    jwks = json.loads((IDENTITY / "jwks.json").read_text())
    return issuer, jwks


def test_valid_fixture_access_token(vector_loader):
    issuer, jwks = _fixture(vector_loader)
    token = issuer.issue_token(now=NOW, scope="projects:read runs:write", roles=["tenant-admin"])
    principal = validate_access_token(
        token,
        profile=TokenProfile(issuer=issuer.ISSUER, audience=issuer.AUDIENCE),
        jwks=jwks,
        now=NOW + 5,
        revocations=MemoryRevocations(set()),
    )
    assert principal.subject == "user-01"
    assert principal.scopes == {"projects:read", "runs:write"}


@pytest.mark.parametrize("change,code", [
    ({"audience": "other-api"}, "invalid-token"),
    ({"issuer": "https://evil.example"}, "invalid-token"),
    ({"lifetime": 5000}, "invalid-token"),
])
def test_invalid_profile_claims(vector_loader, change, code):
    issuer, jwks = _fixture(vector_loader)
    token = issuer.issue_token(now=NOW, **change)
    with pytest.raises(SecurityControlError) as caught:
        validate_access_token(token, profile=TokenProfile(issuer=issuer.ISSUER, audience=issuer.AUDIENCE), jwks=jwks, now=NOW + 1, revocations=MemoryRevocations(set()))
    assert caught.value.code == code


def test_revoked_token(vector_loader):
    issuer, jwks = _fixture(vector_loader)
    token = issuer.issue_token(now=NOW, token_id="revoked-jti")
    with pytest.raises(SecurityControlError) as caught:
        validate_access_token(token, profile=TokenProfile(issuer=issuer.ISSUER, audience=issuer.AUDIENCE), jwks=jwks, now=NOW + 1, revocations=MemoryRevocations({(issuer.ISSUER, "revoked-jti")}))
    assert caught.value.code == "revoked-token"


def test_unknown_key_id(vector_loader):
    from conftest import IDENTITY, load_issuer
    issuer, jwks = _fixture(vector_loader)
    key = (IDENTITY / "private" / "fixture-private.pem").read_bytes()
    claims = {"iss": issuer.ISSUER, "aud": issuer.AUDIENCE, "sub": "u", "tenant": "t", "scope": "projects:read", "iat": NOW, "nbf": NOW, "exp": NOW + 300, "jti": "j"}
    token = jwt.encode(claims, key, algorithm="RS256", headers={"kid":"unknown", "typ":"at+jwt"})
    with pytest.raises(SecurityControlError):
        validate_access_token(token, profile=TokenProfile(issuer=issuer.ISSUER, audience=issuer.AUDIENCE), jwks=jwks, now=NOW, revocations=MemoryRevocations(set()))
