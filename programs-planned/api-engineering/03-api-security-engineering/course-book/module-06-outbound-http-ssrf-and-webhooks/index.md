# Module 06 — Outbound HTTP, SSRF, and Webhook Integrity

> **Program stage:** Course 3 of 6 — Defend the promise.

> **Central question:** How can outbound HTTP and webhook delivery avoid SSRF, rebinding, redirect abuse, tampering, and replay?

## Where this module fits

Validate destinations through parse, resolution, peer connection, redirect, signing, freshness, and replay boundaries. You arrive from Module 05 with all earlier checkpoints still green. API 1.2 and its durable service behavior are fixed. This course adds controls derived from explicit threats; it does not redefine successful business outcomes or treat middleware configuration as proof of security. The result is the baseline for **Secrets, Cryptography, and Sensitive Data**.

## Learning outcomes

- Reject forbidden schemes, ports, credentials, fragments, and address ranges.
- Evaluate every resolved address and the connected peer.
- Revalidate redirects and DNS changes.
- Sign exact webhook bytes with key identity and timestamp.
- Reject stale and replayed deliveries.

## Capstone result

Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense.

Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.

## Core security model

> How does the service communicate with tenant-controlled destinations without becoming a network pivot or accepting forged and replayed events?

Outbound URLs are capabilities, not strings. Secure delivery requires parsed destination policy, DNS and connected-peer checks, redirect revalidation, bounded transport, exact-byte authentication, freshness, durable replay state, and receiver idempotency.

Separate public behavior, control decision, authoritative state, evidence, and operating assumption for every concept.

### 1. URL policy

Parse with a standards-compliant URL parser; allow named schemes and ports; reject user information, fragments, invalid host forms, and ambiguous normalization.

Resolve all answers and reject loopback, private, link-local, multicast, unspecified, reserved, documentation, and other forbidden ranges according to the deployment policy.

A hostname with any forbidden answer is denied; selecting only a convenient public answer creates rebinding opportunities.

The transport connects to a validated address and verifies the actual peer, rather than resolving for policy and resolving again independently.

Every redirect target repeats the full parse, resolution, and peer policy; credentials and sensitive headers are not forwarded across origins.

Connection, TLS, header, body, redirect, and total deadlines are explicit; response bodies are bounded or streamed safely.

The sender signs exactly the bytes transmitted plus versioned metadata; the receiver verifies before parsing or acting.

Timestamp windows limit stale reuse; durable delivery IDs prevent repeated acceptance; business processing remains idempotent.

## Outbound requests create a second untrusted edge

A webhook URL is not harmless configuration. It asks the service to resolve a name, connect from a privileged network location, follow protocol behavior, and transmit signed data. The security decision spans registration and every delivery attempt.

Start with a strict URL policy: allowed scheme, explicit or default port, no user information, no fragment, normalized host syntax, and a bounded path/query length. A host allowlist may be appropriate for a training topology, but suffix matching alone is insufficient: `trusted.example.attacker.test` and Unicode lookalikes demonstrate why parse results, not text fragments, matter.

Resolve the hostname and inspect every answer. Reject loopback, unspecified, private, link-local, multicast, documentation, carrier-grade NAT, metadata-service, and organization-reserved ranges according to the deployment policy. Handle IPv4-mapped IPv6 and alternative textual forms. A mixed public/private answer is rejected rather than selecting the convenient public address.

### Validation and connection must be one decision

DNS rebinding exists when policy checks one resolution and the HTTP client performs another. The connection path must use the validated address set while preserving the intended TLS server name and Host authority, then verify the connected peer belongs to that set. If the client library cannot provide that guarantee, the honest production control belongs in a constrained egress proxy or network policy; application validation alone should not be described as complete.

Redirects restart the policy. Do not automatically follow a 302 from a public host to a private address. Parse, resolve, validate, connect, and count each hop under a small maximum. Revalidate on every retry because DNS and configuration may change after registration.

Webhook integrity protects the receiver from forged or replayed delivery, not from a malicious destination. Sign the exact bytes transmitted, plus a stable delivery identifier, timestamp, and key identifier under an explicit course profile. The receiver verifies with constant-time comparison, enforces freshness, stores the delivery ID durably before applying the effect, and returns the same logical result for a duplicate.

Do not parse and reserialize JSON before verification. Property order, whitespace, Unicode escapes, and numeric representations can change while the data appears equivalent. The signature covers transport bytes. If a standard HTTP message-signature profile is adopted later, its covered components and canonicalization rules must replace—not be mixed with—the course-specific profile.

Rotation again requires overlap. The sender signs with the active key; the receiver can verify the active and retiring keys for a bounded window identified by key ID. Retiring a key before all in-flight retries expire creates an avoidable outage. Keeping every historical key forever expands compromise impact.

## Security requirements and standards

1. The service MUST satisfy **URL policy**: Parse with a standards-compliant URL parser; allow named schemes and ports; reject user information, fragments, invalid host forms, and ambiguous normalization.
2. The service MUST satisfy **Address classification**: Resolve all answers and reject loopback, private, link-local, multicast, unspecified, reserved, documentation, and other forbidden ranges according to the deployment policy.
3. The service MUST satisfy **Mixed-answer rejection**: A hostname with any forbidden answer is denied; selecting only a convenient public answer creates rebinding opportunities.
4. The service MUST satisfy **Connect-time peer binding**: The transport connects to a validated address and verifies the actual peer, rather than resolving for policy and resolving again independently.
5. The service MUST satisfy **Redirect policy**: Every redirect target repeats the full parse, resolution, and peer policy; credentials and sensitive headers are not forwarded across origins.
6. The service MUST satisfy **Outbound budgets**: Connection, TLS, header, body, redirect, and total deadlines are explicit; response bodies are bounded or streamed safely.
7. The service MUST satisfy **Exact-byte webhook signature**: The sender signs exactly the bytes transmitted plus versioned metadata; the receiver verifies before parsing or acting.
8. The service MUST satisfy **Freshness and replay**: Timestamp windows limit stale reuse; durable delivery IDs prevent repeated acceptance; business processing remains idempotent.

## Worked attacks and defenses

Run only against course fixtures. The goal is to understand control boundaries, not to maximize payload novelty.

### Attack 1 — Private-address hostname

A syntactically valid HTTPS hostname resolves to `127.0.0.1`, RFC1918 space, or a cloud metadata address.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 2 — DNS rebinding

Validation resolves a public address; the HTTP client resolves again after the answer changes to a forbidden peer.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 3 — Redirect pivot

An allowed public URL responds with a redirect to a private or credential-bearing destination.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 4 — Alternative IP text

Integer, octal-like, IPv4-mapped IPv6, zone identifiers, or unusual normalization bypasses string checks.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 5 — Webhook body reserialization

The sender signs canonical JSON but transmits differently spaced or ordered bytes, so receiver and sender authenticate different messages.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.
### Attack 6 — Webhook replay

A valid old completion event is submitted repeatedly to trigger duplicate downstream effects.

Trace precondition, controlled input, interpretations, security decision, harmful outcome, expected evidence, and residual risk.

### Prioritization

Rank these attacks using explicit asset impact, caller capability, exposure, and confidence in controls. Record which require environment-backed evidence.

## Python implementation

### Reference design

Model URL evaluation as a pure `DestinationPolicy` over parsed URL and injected resolver results. The real transport receives the validated address set and must expose the connected peer for verification. Use HMAC-SHA256 over a versioned signing string containing timestamp, delivery ID, key ID, and SHA-256 of exact body bytes; compare with `hmac.compare_digest`.

### Work method

Use explicit immutable inputs, narrow exception taxonomies, and standard-library/PyJWT cryptography through named profiles.

## TypeScript implementation

### Reference design

Use WHATWG `URL` for parsing, `dns.promises.lookup({all:true, verbatim:true})` behind an injected resolver, Node `net.isIP`/explicit CIDR classification, and an HTTP agent or connector that pins the selected address. Sign and verify `Buffer` values, not parsed objects; use `timingSafeEqual` only after equal-length checks.

## Failure patterns

### 1. Allowlisting hosts by suffix without DNS/address policy.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 2. Checking a URL at registration but not again at each delivery.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 3. Following redirects automatically without revalidation.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 4. Resolving once for policy and letting the client resolve again.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 5. Signing parsed JSON or a framework-reconstructed body.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

### 6. Keeping replay IDs only in process memory.

Explain why it seems reasonable, what attacker capability invalidates it, and where the repair belongs.

## What you add to the capstone

### Objective

Evaluate the shared destination matrix, run controlled redirect and peer-change simulations, sign and verify exact webhook bytes, and prove replay rejection. Plant a hostname-suffix-only policy and a parse/reserialize signature implementation, capture both bypasses, then repair.

### Required artifacts

Do not modify predecessor bytes or convert missing environment capabilities into passes.

## Representative implementation

These are the smallest useful entry points for **Outbound HTTP, SSRF, and Webhook Integrity**.

### Python — `capstone/tracks/python-fastapi/src/api_security/ssrf.py`

```python


@dataclass(frozen=True, slots=True)
class ValidatedDestination:
    url: str
    hostname: str
    port: int
    addresses: tuple[str, ...]


def _public_address(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise SecurityControlError("invalid-address", "resolver returned an invalid IP address") from exc
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        address = address.ipv4_mapped
    return address.is_global


def validate_destination(
    url: str,
    *,
    addresses: Sequence[str],
    allowed_schemes: Sequence[str] = ("https",),
    allowed_ports: Sequence[int] = (443,),
) -> ValidatedDestination:
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        raise SecurityControlError("invalid-url", "outbound URL is invalid") from exc
    if parsed.scheme.lower() not in {x.lower() for x in allowed_schemes}:
        raise SecurityControlError("scheme", "outbound URL scheme is prohibited")
    if parsed.username is not None or parsed.password is not None:
        raise SecurityControlError("userinfo", "outbound URL user information is prohibited")
    if parsed.fragment:
        raise SecurityControlError("fragment", "outbound URL fragment is prohibited")
    if not parsed.hostname:
        raise SecurityControlError("host", "outbound URL host is required")
    try:
        port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    except ValueError as exc:
        raise SecurityControlError("port", "outbound URL port is invalid") from exc
    if port not in allowed_ports:
        raise SecurityControlError("port", "outbound URL port is prohibited")
    if not addresses:
        raise SecurityControlError("dns-empty", "outbound host resolved to no addresses")
    if not all(_public_address(value) for value in addresses):
        raise SecurityControlError("forbidden-address", "outbound host resolves to a forbidden address")
    return ValidatedDestination(url, parsed.hostname.lower(), port, tuple(addresses))


def verify_connected_peer(destination: ValidatedDestination, peer: str) -> None:
    normalized = str(ipaddress.ip_address(peer))
    approved = {str(ipaddress.ip_address(value)) for value in destination.addresses}
    if normalized not in approved:
        raise SecurityControlError("peer-mismatch", "connected peer was not approved for this request")
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/ssrf.ts`

```typescript
import { SecurityControlError } from "./errors.js";

export interface ValidatedDestination { readonly url: string; readonly hostname: string; readonly port: number; readonly addresses: readonly string[] }

function publicIpv4(value: string): boolean {
  const parts = value.split(".").map(Number); if (parts.length !== 4 || parts.some((x) => !Number.isInteger(x) || x < 0 || x > 255)) return false;
  const [a,b] = parts as [number,number,number,number];
  if (a === 0 || a === 10 || a === 127 || a >= 224) return false;
  if (a === 100 && b >= 64 && b <= 127) return false;
  if (a === 169 && b === 254) return false;
  if (a === 172 && b >= 16 && b <= 31) return false;
  if (a === 192 && (b === 0 || b === 168)) return false;
  if (a === 198 && (b === 18 || b === 19 || b === 51)) return false;
  if (a === 203 && b === 0) return false;
  return true;
}

function publicAddress(value: string): boolean {
  const lower = value.toLowerCase();
  if (lower.startsWith("::ffff:")) return publicIpv4(lower.slice(7));
  if (value.includes(".")) return publicIpv4(value);
  if (lower === "::" || lower === "::1" || lower.startsWith("fe80:") || lower.startsWith("fc") || lower.startsWith("fd") || lower.startsWith("2001:db8:")) return false;
  return /^[0-9a-f:]+$/u.test(lower) && /^[23]/u.test(lower);
}

export function validateDestination(input: { url: string; addresses: readonly string[]; allowedSchemes?: readonly string[]; allowedPorts?: readonly number[] }): ValidatedDestination {
  let parsed: URL; try { parsed = new URL(input.url); } catch { throw new SecurityControlError("invalid-url", "outbound URL is invalid"); }
  const schemes = input.allowedSchemes ?? ["https:"]; if (!schemes.map((x) => x.endsWith(":") ? x : `${x}:`).includes(parsed.protocol)) throw new SecurityControlError("scheme", "outbound URL scheme is prohibited");
  if (parsed.username !== "" || parsed.password !== "") throw new SecurityControlError("userinfo", "outbound URL user information is prohibited");
  if (parsed.hash !== "") throw new SecurityControlError("fragment", "outbound URL fragment is prohibited");
  const port = parsed.port === "" ? (parsed.protocol === "https:" ? 443 : 80) : Number(parsed.port);
  if (!(input.allowedPorts ?? [443]).includes(port)) throw new SecurityControlError("port", "outbound URL port is prohibited");
  if (input.addresses.length === 0) throw new SecurityControlError("dns-empty", "outbound host resolved to no addresses");
  if (!input.addresses.every(publicAddress)) throw new SecurityControlError("forbidden-address", "outbound host resolves to a forbidden address");
  return Object.freeze({ url: input.url, hostname: parsed.hostname.toLowerCase(), port, addresses: [...input.addresses] });
}

export function verifyConnectedPeer(destination: ValidatedDestination, peer: string): void {
  if (!destination.addresses.includes(peer)) throw new SecurityControlError("peer-mismatch", "connected peer was not approved for this request");
}
```

Compare the two tracks by this invariant: **the service validates URL policy, every resolved address, connected peer, redirects, exact signed bytes, freshness, and replay identity**. The intended implementation difference is: resolver/client APIs differ; no implementation may re-resolve outside the validated connection path.

## Module synthesis

The module answer to “How does the service call a user-chosen destination without becoming a network pivot or accepting forged delivery?” is now executable in the capstone: Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.

## Next in the story

Module 07, [Secrets, Cryptography, and Sensitive Data](../module-07-secrets-cryptography-and-sensitive-data/index.md), asks: *How do we use cryptographic mechanisms without exposing keys, inventing protocols, or leaking sensitive data through diagnostics?* The current checkpoint must remain green while that new responsibility is added.
