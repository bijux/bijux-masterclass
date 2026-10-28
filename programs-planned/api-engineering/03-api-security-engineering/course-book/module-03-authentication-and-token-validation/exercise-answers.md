# Reference Answers — Module 03: Authentication and Token Validation

Read after attempting all twelve Authentication and Token Validation exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is signature validity insufficient?

**Answer.** The token may be from the wrong issuer, intended for another audience, expired, revoked, wrong type, or missing required identity claims.

## 2. Who chooses the accepted JWT algorithm?

**Answer.** The resource-server configuration, not the token header.

## 3. Why validate `typ`?

**Answer.** It reduces cross-JWT confusion by distinguishing access tokens from other signed JWT objects when the profile defines a type.

## 4. How should an unknown `kid` be handled?

**Answer.** Refresh trusted JWKS according to bounded policy once if appropriate, then reject; never fetch attacker-provided locations or try arbitrary keys.

## 5. What does audience express?

**Answer.** The resource server or service for which the token is intended.

## 6. Why inject a clock?

**Answer.** Temporal behavior becomes deterministic and boundary cases can be tested without sleeps.

## 7. What is the difference between token expiry and revocation?

**Answer.** Expiry is issuer-declared temporal validity; revocation is an earlier local or issuer decision to deny use.

## 8. Why store API-key digests?

**Answer.** Database disclosure should not reveal usable keys; a keyed digest with separate pepper resists direct recovery and rainbow tables.

## 9. Why reject bearer plus API key?

**Answer.** It creates principal ambiguity and confused policy unless the protocol explicitly defines combined authentication.

## 10. What should a 401 response reveal?

**Answer.** Enough protocol information to indicate invalid/missing credentials without reflecting token content, key state, or internal validation details.

## 11. Trace resource-server credential validation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/tokens.py` and `capstone/tracks/typescript-fastify/src/security/tokens.ts`. The required invariant is that algorithm, key, type, issuer, audience, time, subject, tenant, token ID, scopes, and revocation are all required by profile.

## 12. Compare resource-server credential validation across Python and TypeScript

Both tracks must preserve this invariant: algorithm, key, type, issuer, audience, time, subject, tenant, token ID, scopes, and revocation are all required by profile. The intentional difference is that crypto/JWK APIs differ; the accepted claim set and rejection taxonomy must match.
