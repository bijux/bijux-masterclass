# Module 03 — Authentication and Token Validation

> **Program stage:** Course 3 of 6 — Defend the promise.

> **Central question:** How should a resource server validate bearer tokens and API keys without trusting convenient claims?

## Where this module fits

Validate bearer tokens and API keys against explicit issuer, audience, algorithm, lifetime, key, and revocation policy. You arrive from Module 02 with all earlier checkpoints still green. API 1.2 and its durable service behavior are fixed. This course adds controls derived from explicit threats; it does not redefine successful business outcomes or treat middleware configuration as proof of security. The result is the baseline for **Authorization and Policy Enforcement**.

## Learning outcomes

- Accept exactly one credential mechanism.
- Select accepted JWT algorithms from server configuration.
- Validate signature, type, issuer, audience, time, subject, tenant, scopes, and token ID.
- Handle key rotation and unknown key identifiers safely.
- Store API-key digests rather than reusable keys.

## Capstone result

Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation.

Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.

## Core security model

### Driving question

> How does the service establish a trustworthy principal from an untrusted credential without becoming an authorization server?

A bearer token is untrusted input until signature, key, algorithm, issuer, audience, type, time, subject, and local status are all validated. Authentication creates a principal; it does not authorize a resource action.

### 1. Credential channel

Accept exactly the documented bearer or API-key channel; reject multiple or mixed credentials unless a named combination is required.

Define expected issuer, audience, token type, algorithms, claim requirements, clock skew, maximum lifetime, and revocation behavior.

Verifier configuration selects algorithms; attacker-controlled JWT headers never expand the set.

Retrieve keys only from configured issuer metadata, cache with bounds, handle unknown `kid`, and support controlled overlap rotation.

Check `exp`, `nbf`, `iat`, maximum token age/lifetime, and clock skew with an injectable clock.

Map validated claims to immutable subject, tenant, client, scopes, roles, assurance, and authentication time.

Local state can deny a `jti`, subject session, API key, or key version before nominal expiry.

Look up a non-secret key identifier and compare a peppered digest in constant time; store no recoverable key.

### Synthesis

Draw the capstone data flow and annotate where each concept is owned. Any concept with no owner becomes a Module 03 defect.

## A resource server validates a profile, not “a JWT”

A signed token is a container for claims. Acceptance requires a resource-server profile that says which token types, algorithms, issuers, audiences, keys, times, and claims are meaningful for this API. Signature verification is one step in that profile, not the final decision.

Process a bearer token in a fixed order. First, accept exactly one credential channel. Parse the compact form under size and segment limits. Read only the minimum protected-header data needed to select a key, and choose accepted algorithms from server configuration rather than from the token. Resolve the key only from a trusted issuer configuration. Verify the signature. Then validate `typ`, issuer, audience, temporal claims, subject, tenant, client identity where required, token identifier, scopes, maximum lifetime, and local revocation state.

The order matters. Fetching a key location supplied by an untrusted header turns authentication into SSRF. Trying every configured key for an unknown `kid` makes key selection ambiguous and can amplify work. Accepting a valid signature from the wrong issuer or for another audience lets a credential escape the boundary for which it was minted.

### Time and rotation are system behavior

Use an injected clock. Tests should exercise exactly-before, exactly-at, and exactly-after `nbf` and `exp`, permitted clock skew, maximum token age, and future `iat`. Sleeping tests are slow and nondeterministic; using the wall clock inside the validator hides boundary decisions.

Key rotation needs overlap. During rollout, verifiers may accept the retiring and new public keys while the issuer signs only with the new key. Retirement occurs after the maximum token lifetime plus skew and distribution delay, not immediately after configuration deployment. An unknown key identifier may trigger one bounded refresh from the configured issuer source; it must not trigger arbitrary discovery from token content.

Revocation and expiration solve different problems. Expiration is a predeclared upper bound. Revocation is a decision that a still-unexpired token must no longer authorize access. A local revocation store therefore needs issuer and token identifier, expiry-aware cleanup, and consistent availability assumptions. If the store is unavailable, the security profile must define fail-closed or a narrowly justified degraded mode; silence is not a policy.

API keys require a different profile. Generate high-entropy keys, show the secret once, store an identifier plus keyed digest, compare in constant time, support explicit status and rotation, and never place the usable value in logs or examples. Hashing a low-entropy key without a separate pepper does not protect against offline guessing after database disclosure.

Authentication errors should be useful to a conforming client without becoming an oracle. A 401 response can state that the credential is missing or invalid and advertise the expected scheme. It should not echo token text, disclose whether a particular subject exists, reveal key inventory, or differentiate revocation from signature failure to an attacker. Detailed reason codes belong in restricted, redacted security events.

## Security requirements and standards

The course profile turns the mental model into enforceable requirements. `MUST` denotes a non-compensable course invariant; `SHOULD` requires a recorded exception.

1. The implementation MUST satisfy **Credential channel**: Accept exactly the documented bearer or API-key channel; reject multiple or mixed credentials unless a named combination is required.
2. The implementation MUST satisfy **Resource-server profile**: Define expected issuer, audience, token type, algorithms, claim requirements, clock skew, maximum lifetime, and revocation behavior.
3. The implementation MUST satisfy **Algorithm allowlist**: Verifier configuration selects algorithms; attacker-controlled JWT headers never expand the set.
4. The implementation MUST satisfy **JWKS trust**: Retrieve keys only from configured issuer metadata, cache with bounds, handle unknown `kid`, and support controlled overlap rotation.
5. The implementation MUST satisfy **Temporal validation**: Check `exp`, `nbf`, `iat`, maximum token age/lifetime, and clock skew with an injectable clock.
6. The implementation MUST satisfy **Principal construction**: Map validated claims to immutable subject, tenant, client, scopes, roles, assurance, and authentication time.
7. The implementation MUST satisfy **Revocation**: Local state can deny a `jti`, subject session, API key, or key version before nominal expiry.
8. The implementation MUST satisfy **API-key verification**: Look up a non-secret key identifier and compare a peppered digest in constant time; store no recoverable key.

## Worked attacks and defenses

The Authentication and Token Validation cases are bounded course fixtures. Trace the attacker-controlled value through every interpreter, then identify the policy decision and smallest rejection evidence; do not target external systems.

### Attack 1 — Algorithm confusion

A token header requests an algorithm not approved for the issuer or attempts key-type confusion.

### Attack 2 — Wrong audience

A valid token minted for another API is replayed to the Analysis Runs service.

### Attack 3 — Unknown key identifier

A token references a key outside the trusted JWKS and the verifier falls back to an arbitrary key.

### Attack 4 — Long-lived token

A technically unexpired token exceeds the service maximum lifetime or freshness policy.

### Attack 5 — Decode without verify

Claims are parsed to make an authorization decision before signature validation.

### Attack 6 — Credential ambiguity

A bearer token and API key are supplied together and different middleware selects different identities.


## Python implementation

Use PyJWT only through a narrow validator that supplies allowed algorithms, key selected from a trusted JWKS, expected issuer/audience, and required claims. Inject `Clock`, `JwkProvider`, and `RevocationStore`. Convert library exceptions into a small internal credential-error vocabulary.

## TypeScript implementation

Use Node `crypto.verify` or a pinned JOSE library behind the same profile. Parse compact JWT parts strictly, reject duplicate JSON members in header/payload, convert NumericDate values without unsafe coercion, and construct a frozen principal only after all checks pass.

## Failure patterns

For each pattern, explain why it can look reasonable, construct the smallest counterexample, and identify the missing authoritative boundary.

### 1. Decoding a JWT to find `kid` and then trusting unvalidated issuer-controlled URLs.


### 2. Accepting any token with a valid signature while skipping audience.


### 3. Using a generous clock skew that effectively extends token life.


### 4. Logging the credential or decoded sensitive claims on failure.


### 5. Treating scopes as authorization to every object.


### 6. Keeping fixture private keys in public handoff artifacts.


## What you add to the capstone

### Objective

Issue controlled valid and invalid tokens, execute the full rejection matrix, rotate JWKS with overlap, revoke one `jti`, and prove API-key verification. Plant an audience bypass and show the cross-audience token is accepted before repair.

## Representative implementation

These are the smallest useful entry points for **Authentication and Token Validation**.

### Python — `capstone/tracks/python-fastapi/src/api_security/tokens.py`

```python
from .models import Principal


class Clock(Protocol):
    def now(self) -> int: ...


class RevocationStore(Protocol):
    def is_revoked(self, issuer: str, token_id: str, now: int) -> bool: ...


@dataclass(frozen=True, slots=True)
class TokenProfile:
    issuer: str
    audience: str
    algorithms: tuple[str, ...] = ("RS256",)
    token_type: str = "at+jwt"
    clock_skew_seconds: int = 30
    max_lifetime_seconds: int = 900
    required_claims: tuple[str, ...] = (
        "iss", "aud", "sub", "exp", "iat", "jti", "tenant", "scope"
    )


@dataclass(slots=True)
class MemoryRevocations:
    revoked: set[tuple[str, str]]

    def is_revoked(self, issuer: str, token_id: str, now: int) -> bool:
        return (issuer, token_id) in self.revoked


def _numeric_date(claims: Mapping[str, object], name: str) -> int:
    value = claims.get(name)
    if isinstance(value, bool) or not isinstance(value, int):
        raise SecurityControlError("invalid-token", f"claim {name} must be an integer NumericDate", 401)
    return value


def _audience_matches(value: object, expected: str) -> bool:
    if isinstance(value, str):
        return value == expected
    if isinstance(value, list) and all(isinstance(x, str) for x in value):
        return expected in value
    return False


def validate_access_token(
    token: str,
    *,
    profile: TokenProfile,
    jwks: Mapping[str, object],
    now: int,
    revocations: RevocationStore,
) -> Principal:
    if token.count(".") != 2:
        raise SecurityControlError("invalid-token", "credential is not a compact JWT", 401)
    try:
        header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as exc:
        raise SecurityControlError("invalid-token", "JWT header is invalid", 401) from exc
    alg = header.get("alg")
    typ = header.get("typ")
    kid = header.get("kid")
    if alg not in profile.algorithms:
        raise SecurityControlError("invalid-token", "JWT algorithm is not accepted", 401)
    if typ != profile.token_type:
        raise SecurityControlError("invalid-token", "JWT type is not accepted", 401)
    if not isinstance(kid, str) or not kid:
        raise SecurityControlError("invalid-token", "JWT key identifier is required", 401)
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/tokens.ts`

```typescript
import type { Principal } from "./models.js";
import { parseStrictJson } from "./strict-json.js";

export interface TokenProfile {
  readonly issuer: string;
  readonly audience: string;
  readonly algorithms: readonly string[];
  readonly tokenType: string;
  readonly clockSkewSeconds: number;
  readonly maxLifetimeSeconds: number;
  readonly requiredClaims: readonly string[];
}

export interface JsonWebKey { readonly kid?: string; readonly alg?: string; readonly kty?: string; readonly [key: string]: unknown }
export interface Jwks { readonly keys: readonly JsonWebKey[] }
export interface Revocations { isRevoked(issuer: string, tokenId: string, now: number): boolean }

function decodeSegment(segment: string): Uint8Array {
  try { return Buffer.from(segment, "base64url"); }
  catch { throw new SecurityControlError("invalid-token", "JWT encoding is invalid", 401); }
}

function objectValue(raw: Uint8Array): Record<string, unknown> {
  const value = parseStrictJson(raw);
  if (typeof value !== "object" || value === null || Array.isArray(value)) throw new SecurityControlError("invalid-token", "JWT JSON value is not an object", 401);
  return value as Record<string, unknown>;
}

function numeric(claims: Record<string, unknown>, name: string): number {
  const value = claims[name];
  if (typeof value !== "number" || !Number.isSafeInteger(value)) throw new SecurityControlError("invalid-token", `claim ${name} must be an integer NumericDate`, 401);
  return value;
}

function audienceMatches(value: unknown, expected: string): boolean {
  return value === expected || (Array.isArray(value) && value.every((x) => typeof x === "string") && value.includes(expected));
}

export function validateAccessToken(input: {
  token: string; profile: TokenProfile; jwks: Jwks; now: number; revocations: Revocations;
}): Principal {
  const parts = input.token.split(".");
  if (parts.length !== 3 || parts.some((x) => x.length === 0)) throw new SecurityControlError("invalid-token", "credential is not a compact JWT", 401);
  const [encodedHeader, encodedClaims, encodedSignature] = parts as [string, string, string];
  const header = objectValue(decodeSegment(encodedHeader));
  const claims = objectValue(decodeSegment(encodedClaims));
  const alg = header.alg;
  const typ = header.typ;
  const kid = header.kid;
  if (typeof alg !== "string" || !input.profile.algorithms.includes(alg)) throw new SecurityControlError("invalid-token", "JWT algorithm is not accepted", 401);
  if (typ !== input.profile.tokenType) throw new SecurityControlError("invalid-token", "JWT type is not accepted", 401);
  if (typeof kid !== "string" || kid.length === 0) throw new SecurityControlError("invalid-token", "JWT key identifier is required", 401);
  const matches = input.jwks.keys.filter((key) => key.kid === kid);
  if (matches.length !== 1) throw new SecurityControlError("invalid-token", "JWT key identifier is unknown or ambiguous", 401);
  const key = createPublicKey({ key: matches[0], format: "jwk" });
  const verifier = createVerify("RSA-SHA256");
  verifier.update(`${encodedHeader}.${encodedClaims}`);
  verifier.end();
  if (!verifier.verify(key, Buffer.from(encodedSignature, "base64url"))) throw new SecurityControlError("invalid-token", "JWT signature is invalid", 401);
  for (const required of input.profile.requiredClaims) if (!(required in claims)) throw new SecurityControlError("invalid-token", `required claim ${required} is missing`, 401);
  if (claims.iss !== input.profile.issuer) throw new SecurityControlError("invalid-token", "JWT issuer is not accepted", 401);
  if (!audienceMatches(claims.aud, input.profile.audience)) throw new SecurityControlError("invalid-token", "JWT audience is not accepted", 401);
  const iat = numeric(claims, "iat"); const exp = numeric(claims, "exp");
  const nbf = claims.nbf === undefined ? iat : numeric(claims, "nbf");
  const skew = input.profile.clockSkewSeconds;
  if (iat > input.now + skew || nbf > input.now + skew) throw new SecurityControlError("invalid-token", "JWT is not yet valid", 401);
  if (exp <= input.now - skew) throw new SecurityControlError("invalid-token", "JWT is expired", 401);
  if (exp <= iat || exp - iat > input.profile.maxLifetimeSeconds) throw new SecurityControlError("invalid-token", "JWT lifetime is not accepted", 401);
  const sub = claims.sub; const tenant = claims.tenant; const jti = claims.jti; const scope = claims.scope;
  if ([sub, tenant, jti, scope].some((x) => typeof x !== "string" || x.length === 0)) throw new SecurityControlError("invalid-token", "JWT identity claims are invalid", 401);
```

Compare the two tracks by this invariant: **algorithm, key, type, issuer, audience, time, subject, tenant, token ID, scopes, and revocation are all required by profile**. The intended implementation difference is: crypto/JWK APIs differ; the accepted claim set and rejection taxonomy must match.

## Module synthesis

The module answer to “How does a resource server establish one unambiguous caller identity from an untrusted credential?” is now executable in the capstone: Fixture credentials are replaced by a deterministic but realistic resource-server validation boundary.

## Next in the story

Module 04, [Authorization and Policy Enforcement](../module-04-authorization-and-policy-enforcement/index.md), asks: *After identity is known, which exact action on which exact resource is allowed, and where is that decision enforced?* The current checkpoint must remain green while that new responsibility is added.
