# Worked Answers — Module 03: Authentication and Token Validation

Use these solutions to audit your reasoning for **Authentication and Token Validation**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is signature validity insufficient?

The token may be from the wrong issuer, intended for another audience, expired, revoked, wrong type, or missing required identity claims.

The chapter’s decisive distinction is this: The order matters. Fetching a key location supplied by an untrusted header turns authentication into SSRF. Trying every configured key for an unknown kid makes key selection ambiguous and can amplify work. Accepting a valid signature from the wrong issuer or for another audience lets a credential escape the boundary for which it was minted.

## 2. Who chooses the accepted JWT algorithm?

The resource-server configuration, not the token header.

In the cumulative capstone, the rule becomes concrete: Process a bearer token in a fixed order. First, accept exactly one credential channel. Parse the compact form under size and segment limits. Read only the minimum protected-header data needed to select a key, and choose accepted algorithms from server configuration rather than from the token. Resolve the key only from a trusted issuer configuration. Verify the signature.

## 3. Why validate `typ`?

It reduces cross-JWT confusion by distinguishing access tokens from other signed JWT objects when the profile defines a type.

A useful way to reason about the boundary is: A signed token is a container for claims. Acceptance requires a resource-server profile that says which token types, algorithms, issuers, audiences, keys, times, and claims are meaningful for this API. Signature verification is one step in that profile, not the final decision.

## 4. How should an unknown `kid` be handled?

Refresh trusted JWKS according to bounded policy once if appropriate, then reject; never fetch attacker-provided locations or try arbitrary keys.

The implementation consequence is: Key rotation needs overlap. During rollout, verifiers may accept the retiring and new public keys while the issuer signs only with the new key. Retirement occurs after the maximum token lifetime plus skew and distribution delay, not immediately after configuration deployment. An unknown key identifier may trigger one bounded refresh from the configured issuer source; it must not trigger arbitrary discovery from token content.

## 5. What does audience express?

The resource server or service for which the token is intended.

The important nuance is: A bearer token is untrusted input until signature, key, algorithm, issuer, audience, type, time, subject, and local status are all validated. Authentication creates a principal; it does not authorize a resource action.

**Counterexample.** A validly signed credential for another issuer, audience, tenant, or token type is accepted as local authority.

**Evidence.** Run a token matrix varying signature, algorithm, key ID, issuer, audience, type, time, revocation, tenant, subject, and simultaneous credential presentation.

## 6. Why inject a clock?

Temporal behavior becomes deterministic and boundary cases can be tested without sleeps.

Under concurrency or failure, the distinction becomes: Use an injected clock. Tests should exercise exactly-before, exactly-at, and exactly-after nbf and exp, permitted clock skew, maximum token age, and future iat. Sleeping tests are slow and nondeterministic; using the wall clock inside the validator hides boundary decisions.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 7. What is the difference between token expiry and revocation?

Expiry is issuer-declared temporal validity; revocation is an earlier local or issuer decision to deny use.

The design remains honest only if: Revocation and expiration solve different problems. Expiration is a predeclared upper bound. Revocation is a decision that a still-unexpired token must no longer authorize access. A local revocation store therefore needs issuer and token identifier, expiry-aware cleanup, and consistent availability assumptions. If the store is unavailable, the security profile must define fail-closed or a narrowly justified degraded mode; silence is not a policy.

## 8. Why store API-key digests?

Database disclosure should not reveal usable keys; a keyed digest with separate pepper resists direct recovery and rainbow tables.

The consumer-facing consequence is: API keys require a different profile. Generate high-entropy keys, show the secret once, store an identifier plus keyed digest, compare in constant time, support explicit status and rotation, and never place the usable value in logs or examples. Hashing a low-entropy key without a separate pepper does not protect against offline guessing after database disclosure.

## 9. Why reject bearer plus API key?

It creates principal ambiguity and confused policy unless the protocol explicitly defines combined authentication.

The operational consequence is: Issue controlled valid and invalid tokens, execute the full rejection matrix, rotate JWKS with overlap, revoke one jti, and prove API-key verification. Plant an audience bypass and show the cross-audience token is accepted before repair.

**Counterexample.** A validly signed credential for another issuer, audience, tenant, or token type is accepted as local authority.

**Evidence.** Run a token matrix varying signature, algorithm, key ID, issuer, audience, type, time, revocation, tenant, subject, and simultaneous credential presentation.

## 10. What should a 401 response reveal?

Enough protocol information to indicate invalid/missing credentials without reflecting token content, key state, or internal validation details.

The strongest engineering interpretation is: Authentication errors should be useful to a conforming client without becoming an oracle. A 401 response can state that the credential is missing or invalid and advertise the expected scheme. It should not echo token text, disclose whether a particular subject exists, reveal key inventory, or differentiate revocation from signature failure to an attacker. Detailed reason codes belong in restricted, redacted security events.

## 11. Trace resource-server credential validation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/tokens.py` and `capstone/tracks/typescript-fastify/src/security/tokens.ts`. The required invariant is that algorithm, key, type, issuer, audience, time, subject, tenant, token ID, scopes, and revocation are all required by profile.

The defect-oriented view is: Use PyJWT only through a narrow validator that supplies allowed algorithms, key selected from a trusted JWKS, expected issuer/audience, and required claims. Inject Clock, JwkProvider, and RevocationStore. Convert library exceptions into a small internal credential-error vocabulary.

## 12. Compare resource-server credential validation across Python and TypeScript

Both tracks must preserve this invariant: algorithm, key, type, issuer, audience, time, subject, tenant, token ID, scopes, and revocation are all required by profile. The intentional difference is that crypto/JWK APIs differ; the accepted claim set and rejection taxonomy must match.

Across the Python and TypeScript tracks, the invariant is: Use Node crypto.verify or a pinned JOSE library behind the same profile. Parse compact JWT parts strictly, reject duplicate JSON members in header/payload, convert NumericDate values without unsafe coercion, and construct a frozen principal only after all checks pass.
