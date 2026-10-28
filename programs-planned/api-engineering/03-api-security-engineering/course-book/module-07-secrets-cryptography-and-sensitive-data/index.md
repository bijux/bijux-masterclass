# Module 07 — Secrets, Cryptography, and Sensitive Data

> **Program stage:** Course 3 of 10 — Defend the promise.

> **Central question:** How should secrets, cryptographic keys, sensitive fields, logs, retention, and audit evidence be handled?

## Where this module fits

Module 06 produced **Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense**. This module extends that result by asking: **How should secrets, cryptographic keys, sensitive fields, logs, retention, and audit evidence be handled?**

The new capstone increment is **Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records**. It becomes the prerequisite for **Abuse Resistance and Resource Budgets**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish hashing, HMAC, encryption, and password hashing.
- Keep secret values out of representation and logs.
- Rotate signing and verification keys with overlap.
- Redact nested structures and embedded credentials.
- Minimize, retain, and delete sensitive data deliberately.

## Capstone increment

Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records.

## Core security model

> How are credentials, keys, sensitive fields, logs, and audit evidence handled so normal operation and failure do not expose or misuse them?

Cryptography is useful only when key ownership, purpose, encoding, comparison, rotation, and failure behavior are explicit. Sensitive data must be classified, minimized, non-rendering, redacted structurally, and retained only as long as justified.

Separate public behavior, control decision, authoritative state, evidence, and operating assumption for every concept.

### 1. Secret provider

Application code requests named secret versions through an interface; it does not read arbitrary environment variables throughout the codebase.

Secret wrappers refuse useful `repr`, `str`, JSON serialization, or accidental logging while allowing explicit byte access at the narrow cryptographic boundary.

Token verification keys, API-key peppers, webhook secrets, audit-chain keys, and data-encryption keys are not reused.

The course names algorithm, key type/length, encoding, version, inputs, output form, and rotation behavior rather than saying “encrypted” or “hashed.”

Authentication tags and digests are compared with a timing-resistant primitive after validating shape and length.

Recursive redaction follows field classifications and embedded-token patterns across nested maps, arrays, exceptions, and event attributes.

Stable keyed identifiers support correlation without exposing raw subject or tenant identifiers; they remain sensitive and reversible only by brute force/domain knowledge constraints.

Ordered records include previous digest and current canonical record digest. This detects some local edits but requires external anchoring for stronger tamper evidence.

## A secret has a lifecycle and a purpose

A secret is not merely a string hidden from Git. It is created, distributed, held in memory, used for one purpose, rotated, revoked, audited, and eventually destroyed. Design that lifecycle before choosing whether the local adapter reads a file, environment variable, operating-system key store, or managed secret service.

Expose secret material through a narrow provider interface and a non-rendering wrapper. `repr`, `str`, JSON serialization, validation errors, debug logging, tracing attributes, and exception chaining must not reveal the value. Reveal bytes only at the cryptographic or client-construction boundary, keep the scope short, and never return the raw value from a diagnostic endpoint.

Separate keys by purpose and environment. JWT issuer keys, API-key peppers, webhook HMAC secrets, audit pseudonymization keys, data-encryption keys, and test fixtures have different compromise consequences and rotation schedules. Reusing one “master secret” couples all those domains and makes safe revocation impossible.

### Choose cryptography from the property

Use a password-hashing construction for human-memorable passwords, a keyed digest for high-entropy API-key verification, authenticated encryption when confidentiality and integrity are required, and HMAC or a suitable signature scheme for message authenticity. Hashing is not encryption; encoding is neither. Random identifiers need a cryptographically secure generator and enough entropy for their exposure and lifetime.

Constant-time comparison protects secret-dependent equality checks from timing leakage within the implementation boundary. It does not compensate for a weak key, verbose error differences, network-level timing dominated by other work, or an authorization flaw.

Rotation records need a key identifier, status, activation time, retirement condition, and verification overlap. The system must distinguish “may sign,” “may verify,” and “revoked.” Emergency compromise may require immediate denial and accepted delivery loss; routine rotation should preserve in-flight work.

Redaction is structural. Traverse nested mappings, arrays, objects, URLs, and free text; match a reviewed set of sensitive field names; remove bearer patterns; cap retained length; and reject unsupported types rather than invoking arbitrary object rendering. Pseudonymize identifiers with a keyed construction when correlation is required without exposing raw identity. Plain hashing of a small identifier space is reversible by enumeration.

Audit evidence has limits. A local hash chain can reveal accidental modification or a rewrite that does not also replace its trusted anchor. It does not make a host administrator unable to rewrite history. State the external anchoring or append-only storage required for a stronger claim.

Data minimization is a security control. Do not collect request bodies, artifact contents, tokens, or full URLs merely because a telemetry library can. Define retention and deletion for security events and incident evidence, and ensure backup copies follow the same policy or document the delay explicitly.

## Security requirements and standards

1. The service MUST satisfy **Secret provider**: Application code requests named secret versions through an interface; it does not read arbitrary environment variables throughout the codebase.
2. The service MUST satisfy **Non-rendering value**: Secret wrappers refuse useful `repr`, `str`, JSON serialization, or accidental logging while allowing explicit byte access at the narrow cryptographic boundary.
3. The service MUST satisfy **Key purpose separation**: Token verification keys, API-key peppers, webhook secrets, audit-chain keys, and data-encryption keys are not reused.
4. The service MUST satisfy **Algorithm profile**: The course names algorithm, key type/length, encoding, version, inputs, output form, and rotation behavior rather than saying “encrypted” or “hashed.”
5. The service MUST satisfy **Constant-time comparison**: Authentication tags and digests are compared with a timing-resistant primitive after validating shape and length.
6. The service MUST satisfy **Structural redaction**: Recursive redaction follows field classifications and embedded-token patterns across nested maps, arrays, exceptions, and event attributes.
7. The service MUST satisfy **Pseudonymization**: Stable keyed identifiers support correlation without exposing raw subject or tenant identifiers; they remain sensitive and reversible only by brute force/domain knowledge constraints.
8. The service MUST satisfy **Audit integrity**: Ordered records include previous digest and current canonical record digest. This detects some local edits but requires external anchoring for stronger tamper evidence.

## Worked attacks and defenses

Run only against course fixtures. The goal is to understand control boundaries, not to maximize payload novelty.

### Attack 1 — Secret exception rendering

A failed request prints a settings object whose default representation includes database and webhook credentials.

Trace the **Secrets, Cryptography, and Sensitive Data** precondition, controlled input, interpretation, decision, harmful outcome, expected evidence, and residual risk.
### Attack 2 — Key reuse

The same HMAC key signs webhooks and pseudonymizes users, coupling compromise and enabling cross-domain analysis.

Trace the **Secrets, Cryptography, and Sensitive Data** precondition, controlled input, interpretation, decision, harmful outcome, expected evidence, and residual risk.
### Attack 3 — Log injection and leakage

Hostile input creates fake multiline audit entries or embeds bearer tokens in error details.

Trace the **Secrets, Cryptography, and Sensitive Data** precondition, controlled input, interpretation, decision, harmful outcome, expected evidence, and residual risk.
### Attack 4 — Incomplete redaction

Top-level `token` is removed but nested authorization headers, URL credentials, or exception messages remain.

Trace the **Secrets, Cryptography, and Sensitive Data** precondition, controlled input, interpretation, decision, harmful outcome, expected evidence, and residual risk.
### Attack 5 — Rotation outage

A producer switches keys before receivers know the new key, or removes the old verifier before in-flight deliveries finish.

Trace the **Secrets, Cryptography, and Sensitive Data** precondition, controlled input, interpretation, decision, harmful outcome, expected evidence, and residual risk.
### Attack 6 — False audit immutability

A local hash chain is called immutable even though an attacker who can rewrite the log can recompute the chain.

Trace the **Secrets, Cryptography, and Sensitive Data** precondition, controlled input, interpretation, decision, harmful outcome, expected evidence, and residual risk.

### Prioritization

Rank these attacks using explicit asset impact, caller capability, exposure, and confidence in controls. Record which require environment-backed evidence.

## Python implementation

### Reference design

Use a `SecretBytes` wrapper with redacted representations and explicit `reveal()` at the crypto boundary. Define `SecretProvider.get(name, version)` and test that logging/config serialization cannot expose values. Redact recursively before logging; canonicalize audit records and hash-chain them with a separate keyed digest.

### Work method

Use explicit immutable inputs, narrow exception taxonomies, and standard-library/PyJWT cryptography through named profiles.

## TypeScript implementation

### Reference design

Represent secrets as classes with private fields, `toString()` redaction, and no `toJSON` disclosure. Avoid structural typing that allows plain strings to masquerade as secrets; use branded types at boundaries. Recursively copy and redact objects without mutating application data. Use `timingSafeEqual` correctly.

## Failure patterns

### 1. Using one master secret for every purpose.

Explain why the unsafe **Secrets, Cryptography, and Sensitive Data** design appears reasonable, which attacker capability invalidates it, and which boundary owns the repair.

### 2. Passing raw secret strings through domain objects and exceptions.

Explain why the unsafe **Secrets, Cryptography, and Sensitive Data** design appears reasonable, which attacker capability invalidates it, and which boundary owns the repair.

### 3. Redacting only keys named exactly `password`.

Explain why the unsafe **Secrets, Cryptography, and Sensitive Data** design appears reasonable, which attacker capability invalidates it, and which boundary owns the repair.

### 4. Hashing low-entropy identifiers without a key and calling them anonymous.

Explain why the unsafe **Secrets, Cryptography, and Sensitive Data** design appears reasonable, which attacker capability invalidates it, and which boundary owns the repair.

### 5. Rotating a verifier with no overlap or version identifier.

Explain why the unsafe **Secrets, Cryptography, and Sensitive Data** design appears reasonable, which attacker capability invalidates it, and which boundary owns the repair.

### 6. Claiming local hash chaining prevents a privileged attacker from rewriting history.

Explain why the unsafe **Secrets, Cryptography, and Sensitive Data** design appears reasonable, which attacker capability invalidates it, and which boundary owns the repair.

## What you add to the capstone

### Objective

Add secret wrappers/providers, recursive redaction, keyed pseudonyms, and audit chaining. Run a canary-secret scan across logs, exceptions, reports, and handoff. Plant a secret-bearing dataclass/default object representation and prove the canary leaks before repair.

### Required artifacts

Do not modify predecessor bytes or convert missing environment capabilities into passes.

## Representative implementation

These are the smallest useful entry points for **Secrets, Cryptography, and Sensitive Data**.

### Python — `capstone/tracks/python-fastapi/src/api_security/secrets.py`

```python
BEARER_RE = re.compile(r"(?i)(Bearer)\s+[A-Za-z0-9._~+/-]+")


class SecretBytes:
    __slots__ = ("__value",)

    def __init__(self, value: bytes | str) -> None:
        self.__value = value.encode("utf-8") if isinstance(value, str) else bytes(value)
        if not self.__value:
            raise ValueError("secret must not be empty")

    def reveal(self) -> bytes:
        return bytes(self.__value)

    def __repr__(self) -> str:
        return "SecretBytes([REDACTED])"

    def __str__(self) -> str:
        return "[REDACTED]"


@dataclass(slots=True)
class DictSecretProvider:
    values: Mapping[tuple[str, str], SecretBytes]

    def get(self, name: str, version: str) -> SecretBytes:
        return self.values[(name, version)]


def _redact_string(value: str) -> str:
    value = BEARER_RE.sub(r"\1 [REDACTED]", value)
    try:
        parsed = urlsplit(value)
        if parsed.scheme and parsed.hostname and (parsed.username is not None or parsed.password is not None):
            host = parsed.hostname
            if parsed.port is not None:
                host += f":{parsed.port}"
            return urlunsplit((parsed.scheme, f"[REDACTED]@{host}", parsed.path, parsed.query, parsed.fragment))
    except ValueError:
        pass
    return value


def redact(value: Any, *, key: str | None = None) -> Any:
    normalized = key.lower().replace("-", "_") if key else None
    if normalized is not None and (normalized in SENSITIVE_KEYS or normalized.replace("_", "") in SENSITIVE_KEYS):
        return "[REDACTED]"
    if isinstance(value, SecretBytes):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(k): redact(v, key=str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(v) for v in value]
    if isinstance(value, str):
        return _redact_string(value)
    return value
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/secrets.ts`

```typescript
const SENSITIVE = new Set(["authorization","api_key","apikey","password","secret","token","access_token","refresh_token","webhooksecret","webhook_secret","private_key","pepper"]);
const BEARER = /(Bearer)\s+[A-Za-z0-9._~+/-]+/giu;

export class SecretBytes {
  readonly #value: Uint8Array;
  constructor(value: Uint8Array | string) {
    this.#value = typeof value === "string" ? new TextEncoder().encode(value) : new Uint8Array(value);
    if (this.#value.byteLength === 0) throw new Error("secret must not be empty");
  }
  reveal(): Uint8Array { return new Uint8Array(this.#value); }
  toString(): string { return "[REDACTED]"; }
  toJSON(): string { return "[REDACTED]"; }
}

function redactString(value: string): string {
  const bearer = value.replace(BEARER, "$1 [REDACTED]");
  try {
    const url = new URL(bearer);
    if (url.username !== "" || url.password !== "") { url.username = "[REDACTED]"; url.password = ""; return url.toString().replace("%5BREDACTED%5D", "[REDACTED]"); }
  } catch { /* ordinary string */ }
  return bearer;
}

export function redact(value: unknown, key?: string): unknown {
  const normalized = key?.toLowerCase().replaceAll("-", "_");
  if (normalized !== undefined && (SENSITIVE.has(normalized) || SENSITIVE.has(normalized.replaceAll("_", "")))) return "[REDACTED]";
  if (value instanceof SecretBytes) return "[REDACTED]";
  if (Array.isArray(value)) return value.map((item) => redact(item));
  if (value !== null && typeof value === "object") return Object.fromEntries(Object.entries(value as Record<string, unknown>).map(([k,v]) => [k,redact(v,k)]));
  if (typeof value === "string") return redactString(value);
  return value;
}
```

Compare the two tracks by this invariant: **secrets never render, keys are separated by purpose, redaction is recursive, and rotation has explicit overlap and retirement**. The intended implementation difference is: wrapper types differ; logs, exceptions, fixtures, and handoffs must expose the same safe surface.

## Module synthesis

You are ready to leave this module when you can **Distinguish hashing, HMAC, encryption, and password hashing, Keep secret values out of representation and logs, and Rotate signing and verification keys with overlap** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Remove or bypass the central control for Secrets, Cryptography, and Sensitive Data in a temporary branch** and requiring the following oracle: **secret-provider boundary; non-rendering values; purpose-separated keys; explicit algorithm profiles.**

The cumulative platform now includes **Add secret-provider boundaries, non-rendering values, redaction, pseudonymization, rotation, and privacy-bounded audit records**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Abuse Resistance and Resource Budgets](../module-08-abuse-resistance-and-resource-budgets/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
