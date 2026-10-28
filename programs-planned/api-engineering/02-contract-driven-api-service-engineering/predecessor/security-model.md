# Security model

## Three separate questions

1. **Authentication:** which principal does the credential represent?
2. **Scope authorization:** may that principal invoke this class of operation?
3. **Object authorization:** may that principal act on this concrete resource?

The capstone tests all three. A correct bearer token with `artifacts:read` still cannot retrieve another owner's artifact.

## OpenAPI semantics

The canonical contract exposes OAuth-style scope requirements and an API-key alternative. Multiple Security Requirement Objects express OR; multiple schemes inside one requirement express AND. The course includes a truth table so learners must reason about the structure rather than visually guessing.

## Deterministic local verifier

No authorization server is included. Fixed tokens map to fixed principals and scopes. This keeps tests hermetic and permits precise `401` versus `403` checks.

## Destination controls

User-provided callback and webhook URLs can create server-side request forgery risk. The training models only accept HTTPS URLs under `hooks.example.test`. A real deployment would additionally resolve and re-check addresses, block private and link-local ranges, limit redirects, authenticate delivery, rotate secrets, and apply egress policy.

## Secret handling

Webhook creation accepts a secret but returns only a hint. Examples use non-production values. Request and proof logs must not emit credential or secret bodies. Problem Details do not include stack traces or internal exception text.
