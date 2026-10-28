from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .authorization import Policy, authorize
from .errors import SecurityControlError
from .models import Decision, Principal, ResourceFacts


@dataclass(frozen=True, slots=True)
class CredentialInputs:
    bearer_token: str | None = None
    api_key: str | None = None


def authenticate_exactly_one(
    inputs: CredentialInputs,
    *,
    bearer_validator: Callable[[str], Principal],
    api_key_validator: Callable[[str], Principal],
) -> Principal:
    supplied = int(inputs.bearer_token is not None) + int(inputs.api_key is not None)
    if supplied == 0:
        raise SecurityControlError("credential-required", "one credential is required", 401)
    if supplied != 1:
        raise SecurityControlError("credential-ambiguous", "multiple credential channels are prohibited", 400)
    if inputs.bearer_token is not None:
        return bearer_validator(inputs.bearer_token)
    assert inputs.api_key is not None
    return api_key_validator(inputs.api_key)


def security_decision(
    operation_id: str,
    *,
    inputs: CredentialInputs | None,
    resource: ResourceFacts,
    policies: dict[str, Policy],
    bearer_validator: Callable[[str], Principal],
    api_key_validator: Callable[[str], Principal],
) -> tuple[Principal | None, Decision]:
    if operation_id == "getHealth" and inputs is None:
        return None, authorize(operation_id, principal=None, resource=resource, policies=policies)
    if inputs is None:
        raise SecurityControlError("credential-required", "one credential is required", 401)
    principal = authenticate_exactly_one(inputs, bearer_validator=bearer_validator, api_key_validator=api_key_validator)
    return principal, authorize(operation_id, principal=principal, resource=resource, policies=policies)
