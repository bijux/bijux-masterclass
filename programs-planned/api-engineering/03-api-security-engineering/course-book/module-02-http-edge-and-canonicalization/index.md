# Module 02 — HTTP Edge and Canonicalization

> **Program stage:** Course 3 of 6 — Defend the promise.

> **Central question:** Which raw HTTP message should the application trust after proxies, parsers, duplicate fields, and size limits intervene?

## Where this module fits

Harden host, scheme, forwarding, media type, request size, duplicate header, and strict JSON boundaries. You arrive from Module 01 with all earlier checkpoints still green. API 1.2 and its durable service behavior are fixed. This course adds controls derived from explicit threats; it does not redefine successful business outcomes or treat middleware configuration as proof of security. The result is the baseline for **Authentication and Token Validation**.

## Learning outcomes

- Define direct-client and trusted-proxy behavior.
- Reject ambiguous singleton headers and duplicate JSON members.
- Normalize only after preserving raw evidence.
- Enforce content type and body limits before model validation.
- Separate browser CORS policy from API authentication.

## Capstone result

Establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation.

FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.

## Core security model

### Driving question

> How do all components agree on one safe interpretation of the request before identity or business logic runs?

Security decisions are unsound when a proxy, server, framework, and application can interpret the same bytes differently. The edge must establish one bounded request representation and one trusted external origin.

### 1. Raw-message ownership

Body and critical headers are security inputs before framework schema validation. Exactly one layer owns limits and ambiguity checks.

Forwarded fields are accepted only from configured immediate peers and interpreted with an explicit chain policy.

Scheme, host, and port are reconstructed deterministically for redirects, metadata, callback comparisons, and security policy.

Conflicting `Content-Length`, `Host`, authorization, or forwarding values are rejected rather than guessed.

Reject duplicate members, malformed UTF-8, non-finite values, trailing content, excessive depth, and dangerous prototype keys.

A JSON operation accepts only approved JSON media types; multipart and streams use separate parsers and limits.

CORS controls browser read permission; it is not API authentication and does not protect non-browser clients.

Header count/size, body bytes, nesting, parse time, and connection lifetime are separate budgets.

### Synthesis

Draw the capstone data flow and annotate where each concept is owned. Any concept with no owner becomes a Module 02 defect.

## The edge is a protocol decision, not a middleware collection

Framework request objects are already interpretations. Headers may have been merged, case-normalized, decoded, or discarded; a proxy may have rewritten the host, scheme, and client address. Security decisions that depend on those values must therefore define which component owns the canonical interpretation and which raw evidence remains available.

For each deployment topology, write a trust rule. A direct client connection may use the socket peer, request target, and Host field. A proxied deployment may trust one exact proxy network to replace those values with a specified forwarding convention. The application must ignore forwarding fields from every other peer. “We are behind a load balancer” is not a rule because it does not identify the trusted peer set, number of hops, overwrite behavior, or failure mode.

Critical singleton fields deserve special treatment. Two Authorization fields, two Host fields, or conflicting Content-Length values are not a request the application should repair. Reject ambiguity before authentication or body parsing. Some HTTP request-smuggling classes depend on disagreement between intermediaries and cannot be solved solely in application code; the course control establishes a strict application boundary while requiring edge-server and proxy configuration to agree on malformed-message handling.

### Canonicalization has an order

Security validation commonly fails because decoding and checking occur in the wrong sequence. Preserve raw input for diagnostics, then apply the one protocol-defined parse, then validate the parsed result, then normalize only where the application has defined an equivalence relation. Repeated percent decoding, opportunistic Unicode folding, or trimming values that the protocol treats as significant can create a second language understood only by part of the stack.

Strict JSON illustrates the point. JSON object member names are not required to be unique by every parser behavior in practice. If one layer keeps the first `role` and another keeps the last, the message has no single meaning. The course parsers reject duplicate members, malformed UTF-8, non-finite numeric forms, excessive depth, and an over-budget body before Pydantic or TypeBox constructs application models.

Body limits must be enforced while bytes are read. Checking Content-Length alone trusts a client assertion and misses chunked transfer. Reading the complete body and then comparing length has already paid the memory cost. The decisive test sends a stream that crosses the limit and observes bounded allocation and an early documented response.

CORS belongs to browser permission policy. It can stop selected browser scripts from reading responses; it does not authenticate a caller, protect a bearer token used outside a browser, or constrain a curl client. Treating a permissive or restrictive CORS configuration as authorization is a category error.

At the end of this module, one raw inbound message must have one accepted interpretation or one rejection. The Python ASGI middleware and Fastify content-type/parser hooks may be shaped differently, but they must agree on critical duplicates, proxy trust, host/scheme, media type, byte budget, and strict JSON outcomes.

## Security requirements and standards

The course profile turns the mental model into enforceable requirements. `MUST` denotes a non-compensable course invariant; `SHOULD` requires a recorded exception.

1. The implementation MUST satisfy **Raw-message ownership**: Body and critical headers are security inputs before framework schema validation. Exactly one layer owns limits and ambiguity checks.
2. The implementation MUST satisfy **Proxy trust**: Forwarded fields are accepted only from configured immediate peers and interpreted with an explicit chain policy.
3. The implementation MUST satisfy **External origin**: Scheme, host, and port are reconstructed deterministically for redirects, metadata, callback comparisons, and security policy.
4. The implementation MUST satisfy **Critical-header uniqueness**: Conflicting `Content-Length`, `Host`, authorization, or forwarding values are rejected rather than guessed.
5. The implementation MUST satisfy **Strict JSON**: Reject duplicate members, malformed UTF-8, non-finite values, trailing content, excessive depth, and dangerous prototype keys.
6. The implementation MUST satisfy **Media-type boundary**: A JSON operation accepts only approved JSON media types; multipart and streams use separate parsers and limits.
7. The implementation MUST satisfy **CORS**: CORS controls browser read permission; it is not API authentication and does not protect non-browser clients.
8. The implementation MUST satisfy **Resource limits**: Header count/size, body bytes, nesting, parse time, and connection lifetime are separate budgets.

## Worked attacks and defenses

The HTTP Edge and Canonicalization cases are bounded course fixtures. Trace the attacker-controlled value through every interpreter, then identify the policy decision and smallest rejection evidence; do not target external systems.

### Attack 1 — Forwarded-host spoof

A direct client supplies `X-Forwarded-Host: internal.example` and the app generates a trusted-origin link from it.

### Attack 2 — Duplicate authorization

Two credential headers are merged differently by proxy and framework, producing inconsistent principal selection.

### Attack 3 — Request smuggling precursor

Conflicting message-length headers cause front and back components to disagree about request boundaries.

### Attack 4 — Duplicate JSON member

`{"role":"reader","role":"admin"}` is accepted with first-wins in one component and last-wins in another.

### Attack 5 — Deep nesting exhaustion

A small byte body contains extreme nested arrays and consumes parser stack or CPU.

### Attack 6 — CORS misconception

A denied browser preflight is treated as proof that scripted non-browser callers cannot invoke the API.


## Python implementation

Implement an ASGI middleware that reads bounded raw bytes, rejects ambiguous critical headers, invokes a strict JSON decoder with `object_pairs_hook`, and replays the validated body to FastAPI. Do not modify Starlette private request attributes. Put verified edge context in `scope["state"]`.

## TypeScript implementation

Register a Fastify content-type parser for JSON that receives text or bytes, applies the same duplicate/depth/number profile, and returns a parsed value. Use an `onRequest` hook for raw headers and proxy policy before authentication. Avoid relying on plain `JSON.parse` for duplicate-member detection.

## Failure patterns

For each pattern, explain why it can look reasonable, construct the smallest counterexample, and identify the missing authoritative boundary.

### 1. Trusting forwarding headers from every peer because the app is “usually” behind a proxy.


### 2. Applying a body limit after reading the entire body into memory.


### 3. Letting the framework merge duplicate headers before the security layer inspects them.


### 4. Using `json.loads` or `JSON.parse` alone and assuming all parsers agree.


### 5. Using CORS as an authorization mechanism.


### 6. Redirecting to a Host-derived URL without host policy.


## What you add to the capstone

### Objective

Run the same hostile raw-message corpus through Python and TypeScript adapters. Plant a trust-all forwarding mode and a plain JSON parser, capture the policy bypasses, repair them, and retain regressions.

## Representative implementation

These are the smallest useful entry points for **HTTP Edge and Canonicalization**.

### Python — `capstone/tracks/python-fastapi/src/api_security/edge.py`

```python


@dataclass(frozen=True, slots=True)
class EdgeContext:
    client_peer: str
    external_scheme: str
    external_host: str
    origin: str
    trusted_proxy: bool


def _normalized_headers(headers: Sequence[tuple[str, str]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for name, value in headers:
        key = name.strip().lower()
        result.setdefault(key, []).append(value.strip())
    for name in CRITICAL_SINGLETONS:
        if len(result.get(name, [])) > 1:
            raise SecurityControlError("ambiguous-header", f"multiple {name} header fields")
    return result


def _peer_trusted(peer: str, configured: Sequence[str]) -> bool:
    address = ip_address(peer)
    for item in configured:
        if "/" in item and address in ip_network(item, strict=False):
            return True
        if "/" not in item and address == ip_address(item):
            return True
    return False


def evaluate_edge(
    *,
    peer: str,
    headers: Sequence[tuple[str, str]],
    allowed_hosts: Sequence[str],
    trusted_proxies: Sequence[str] = (),
    direct_scheme: str = "https",
) -> EdgeContext:
    parsed = _normalized_headers(headers)
    trusted = _peer_trusted(peer, trusted_proxies)
    host = (parsed.get("host") or [""])[0].lower()
    scheme = direct_scheme.lower()
    if trusted:
        host = (parsed.get("x-forwarded-host") or [host])[0].lower()
        scheme = (parsed.get("x-forwarded-proto") or [scheme])[0].lower()
    if scheme not in {"https", "http"}:
        raise SecurityControlError("scheme-not-allowed", "external scheme is not accepted")
    allowed = {h.lower() for h in allowed_hosts}
    if host not in allowed:
        raise SecurityControlError("host-not-allowed", "external host is not accepted")
    origin = f"{scheme}://{host}"
    return EdgeContext(peer, scheme, host, origin, trusted)
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/edge.ts`

```typescript
import { SecurityControlError } from "./errors.js";

const CRITICAL = new Set(["authorization", "content-length", "host", "x-api-key", "x-forwarded-host", "x-forwarded-proto"]);

export interface EdgeContext {
  readonly clientPeer: string;
  readonly externalScheme: string;
  readonly externalHost: string;
  readonly origin: string;
  readonly trustedProxy: boolean;
}

function headerMap(headers: readonly (readonly [string, string])[]): Map<string, string[]> {
  const result = new Map<string, string[]>();
  for (const [name, value] of headers) {
    const key = name.trim().toLowerCase();
    result.set(key, [...(result.get(key) ?? []), value.trim()]);
  }
  for (const name of CRITICAL) {
    if ((result.get(name)?.length ?? 0) > 1) throw new SecurityControlError("ambiguous-header", `multiple ${name} header fields`);
  }
  return result;
}

function trusted(peer: string, configured: readonly string[]): boolean {
  // The dependency-light reference accepts exact addresses. CIDR handling belongs
  // to the environment-backed adapter and is not silently simulated here.
  return configured.includes(peer);
}

export function evaluateEdge(input: {
  peer: string;
  headers: readonly (readonly [string, string])[];
  allowedHosts: readonly string[];
  trustedProxies?: readonly string[];
  directScheme?: string;
}): EdgeContext {
  const headers = headerMap(input.headers);
  const isTrusted = trusted(input.peer, input.trustedProxies ?? []);
  let host = (headers.get("host")?.[0] ?? "").toLowerCase();
  let scheme = (input.directScheme ?? "https").toLowerCase();
  if (isTrusted) {
    host = (headers.get("x-forwarded-host")?.[0] ?? host).toLowerCase();
    scheme = (headers.get("x-forwarded-proto")?.[0] ?? scheme).toLowerCase();
  }
  if (scheme !== "https" && scheme !== "http") throw new SecurityControlError("scheme-not-allowed", "external scheme is not accepted");
  if (!input.allowedHosts.map((x) => x.toLowerCase()).includes(host)) throw new SecurityControlError("host-not-allowed", "external host is not accepted");
  return Object.freeze({ clientPeer: input.peer, externalScheme: scheme, externalHost: host, origin: `${scheme}://${host}`, trustedProxy: isTrusted });
}
```

Compare the two tracks by this invariant: **critical singleton headers, trusted proxy assertions, media type, body size, and strict JSON are decided before model construction**. The intended implementation difference is: ASGI and Fastify hooks differ; ambiguous raw messages must be rejected identically.

## Module synthesis

The module answer to “Which bytes and proxy assertions does the application actually trust before framework parsing begins?” is now executable in the capstone: FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.

## Next in the story

Module 03, [Authentication and Token Validation](../module-03-authentication-and-token-validation/index.md), asks: *How does a resource server establish one unambiguous caller identity from an untrusted credential?* The current checkpoint must remain green while that new responsibility is added.
