---
module_id: API-049
program: API & Service Engineering
level: 1
module_number: 49
title: Replay and Request Signing
status: complete
last_verified: 2026-09-01
---

# Replay and Request Signing

## One-Page Review

### Governing question

How can an API verify who possessed a signing key, which exact HTTP semantics that signer authorized, and whether this proof is fresh and unused—without confusing a valid signature with authorization, confidentiality, or exactly-once business execution?

### Essential definitions

- A **request signature** authenticates selected HTTP message components and metadata using a shared or private signing key.
- A **signature base** is the deterministic byte/string representation of the covered components that both signer and verifier construct.
- **Canonicalization** maps semantically relevant method, authority, target, fields, content digest, and signature parameters into that base.
- A **content digest** commits to message content bytes but provides no authenticity unless itself covered by a trusted signature or equivalent channel.
- A **replay** reuses a previously valid proof/request outside its intended single execution or context.
- A **freshness window** bounds accepted creation/expiration time; it limits replay duration but does not make a proof single-use.
- A **nonce/JTI** is a bounded unique proof identifier or server challenge used with stateful duplicate detection.
- **Sender-constrained tokens** require proof of a key associated with a token, reducing usefulness of a stolen bearer token.
- An **idempotency key** identifies one business operation across legitimate retries; it is not a cryptographic freshness nonce.

### Central model, mechanism, or theorem

For observed request $r$, proof $p$, key record $k$, and current time $t$, accept the proof only if

$$
V_{proof}(r,p,k,t)=V_{key}\land V_{alg}\land V_{sig}(B(r,p),p,k)\land V_{time}\land V_{nonce}\land V_{context}\land V_{content}.
$$

$B$ must cover every message component the application will trust. Then the protected operation separately requires

$$
\operatorname{allow}=V_{TLS}\land V_{proof}\land A(principal,client,action,object,state)\land I(operation).
$$

Stateful replay defense performs an atomic “insert nonce if absent” scoped to the principal/key/profile for at least the proof acceptance lifetime. A timestamp alone permits replay throughout its window.

### Critical invariants

Use a reviewed profile such as RFC 9421 rather than inventing concatenation. Verification reconstructs the effective request at the boundary whose semantics are protected. Method, authority/target, relevant query, content digest, content type, security-critical fields, signature metadata, key identity, and profile/tag are covered as required. Unsigned fields are untrusted or stripped. Key ID never selects an attacker-chosen algorithm without policy. Expiration, maximum age, clock skew, nonce format/size/scope, and duplicate-store consistency are explicit. Duplicate reservation is atomic across all accepting nodes and retained for the entire acceptance window. TLS remains mandatory; signatures do not encrypt. Authorization and object/state checks run after identity/proof. Retries use new one-time proofs while retaining an operation idempotency key. Request bodies are bounded and verified as the bytes/representation defined by the profile. Proxy, content-encoding, query, header, trailer, and redirect transformations are either normalized consistently before signing or prohibited. Key rotation/revocation and audit are testable.

### Common failures

Signing only the body but not method/target; trusting an unsigned digest; custom newline/JSON/query canonicalization; accepting algorithm/key type from the request; treating `keyid` as identity without key authorization; long timestamp windows with no nonce store; per-instance replay caches behind a load balancer; checking then inserting nonce non-atomically; expiring nonce records too early; using client time without bounded skew; storing attacker-sized raw nonces indefinitely; inserting nonce before authenticating it; forwarding a signature across a proxy that changes authority/path; ignoring duplicate query parameters or content encodings; verifying parsed/re-serialized JSON instead of defined bytes; considering DPoP a whole-request body signature; reusing one signature for retries; treating a signature as idempotency or permission; logging keys/signatures/tokens; and allowing presigned URLs far beyond their minimal audience/action/lifetime.

### Compact example

A webhook provider signs the creation time, unique delivery ID, `POST`, receiver authority/path, content type, and SHA-256 `Content-Digest` under a registered key/profile. The receiver buffers a bounded raw body, validates digest and signature, checks a two-minute age/skew policy, atomically records a hash of `(provider,keyid,delivery-id)` across the cluster, authorizes the provider/event type/tenant, and processes the business event idempotently by event ID. **Conclusion:** the signature authenticates selected delivery semantics, the nonce store rejects captured proof reuse, and the event ledger handles legitimate duplicate business delivery.

### Connections

[Credential and Token Handling](042-credential-and-token-handling.md) protects key/token material, [OAuth Authorization Flows](043-oauth-authorization-flows.md) supplies grants, [Idempotency Keys](037-idempotency-keys.md) handles legitimate retries, and [Concurrency Control at the API Boundary](038-concurrency-control-at-the-api-boundary.md) binds effects to state. [Designing an API Against Expected Abuse Cases](../ROADMAP.md) next composes these controls.

## Governing Question

Which request semantics must a proof bind, which key and profile make that proof trustworthy, what freshness state prevents reuse, and which separate controls determine whether the authenticated request may and should produce its business effect?

## Why This Matters

TLS authenticates and protects a connection, but applications sometimes need end-to-end proof across intermediaries, webhook authentication, workload/client proof of key possession, or sender-constrained access tokens. A captured bearer token can be replayed by anyone who holds it; a captured signed request can also be replayed unless freshness and duplicate detection are part of the protocol.

A mathematically valid signature can protect too little. If it covers the body but not method and target, an intermediary/attacker may move the signed content to a different operation. If it covers a digest but the digest field is unsigned, the body can be replaced with a new matching digest. If it covers a path before a proxy rewrites it but the verifier sees another path, legitimate messages fail—or deployments weaken verification until attacks pass. Security is determined by the application profile and verified components, not the primitive alone.

Replay has multiple meanings. Reusing the same proof can be rejected by a nonce/JTI ledger. Yet a legitimate key holder can sign the same business command again with a fresh nonce, and a retrying client may need to do exactly that after a timeout. Preventing duplicate charges/orders therefore also needs an idempotency key or domain uniqueness/invariant. Request signing proves possession and integrity; replay detection proves proof uniqueness within a scope/window; idempotency controls business effect.

Operational details dominate: clocks skew, requests pass proxies, bodies stream, keys rotate, regions partition, nonce stores can be attacked, and canonicalization varies. A durable design adopts a standard profile, states the exact trust boundary, makes every transformation explicit, and tests with captured raw requests through the real path.

## Prerequisites and Retrieval

Retrieve cryptographic hashes, MAC/HMAC versus digital signatures, authenticated channels/TLS, key identifiers/algorithms/rotation, HTTP methods/authority/path/query/fields/content/representation, structured fields, canonicalization, content digests, OAuth access tokens, DPoP, time/clock skew, nonce/JTI/challenge, atomic uniqueness stores/TTL, idempotency keys, retries, proxies/CDNs/service mesh, streaming/trailers/content encoding, authorization, audit, and denial-of-service controls.

Before selecting signing, retrieve threat actor/capture point, why TLS/bearer authentication is insufficient, signer/verifier/intermediary boundaries, request components affecting behavior, raw versus effective URI/authority, proxy normalization, body/content encoding/streaming limits, clock sources/skew, acceptable replay window, cluster/region topology and nonce-store consistency, retry/idempotency semantics, key provisioning/ownership/algorithms/rotation/revocation, token binding, redirects, error contract, observability/redaction, performance/availability budget, SDK interoperability, and incident recovery.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish message integrity/authentication, freshness, authorization, confidentiality, and idempotency;
2. define a complete standards-based signature profile and effective verification boundary;
3. bind method, authority/target, query, fields, content digest, and signature metadata correctly;
4. design timestamp, expiration, nonce/JTI, challenge, and distributed duplicate-store policy;
5. choose HMAC, asymmetric signatures, DPoP, webhook signatures, or presigned capabilities deliberately;
6. operate keys, proxies, streaming bodies, retries, failures, and observability safely; and
7. test tampering, replay, canonicalization, transformation, rotation, skew, partition, and resource-exhaustion cases.

## Core Exposition

### Start from the guarantee, not the signature primitive

A hash detects accidental/intentional content changes only when the expected hash is authenticated. A MAC such as HMAC proves that someone holding a shared secret produced a tag; every verifier holding that secret can also forge one. An asymmetric signature lets the verifier use a public key while the signer retains the private key, improving separation and attribution, though operational identity and key custody still determine what attribution means.

None encrypts the request. TLS remains necessary for confidentiality, server authentication, in-transit integrity, and metadata protection. Application signatures can add proof that survives selected intermediaries or binds a client/workload key, but they do not automatically hide URLs, headers, body, key IDs, or signatures.

State the threat: captured webhook, stolen bearer token, malicious/compromised intermediary, body/target transformation, cross-endpoint replay, or origin ambiguity. Then state which observer must verify what. If ordinary mutually authenticated TLS between tightly controlled workloads already meets the need, bespoke application signing may add more canonicalization/key/availability risk than value.

### Adopt an explicit HTTP message signature profile

RFC 9421 defines HTTP Message Signatures as signatures over an ordered set of message components plus signature parameters. The standard supplies component identifiers and serialization rules, but the application profile must still require algorithms, keys, components, timestamps, nonces, tag/profile, error behavior, and authorization mapping.

At minimum consider covering:

- derived method and target/authority components needed to prevent relocation;
- query semantics, including whether the whole query or named parameters are covered;
- `Content-Digest` and `Content-Type` for requests with content;
- security-critical routing, tenant, conditional, or idempotency fields the application trusts;
- signature `created`, `expires`, `nonce`, `keyid`, and application `tag`; and
- token/certificate identifier when the proof must bind another credential.

Covering `@method` and a content digest but not target can let the same signed body authenticate at another target accepted by the key. Covering target but not an idempotency or tenant field the application trusts lets that unsigned field change behavior. Conversely, signing volatile hop-by-hop fields creates fragility. The profile decides which components are authoritative and requires the verifier to discard or ignore security-relevant unsigned alternatives.

Multiple signatures can serve different hops/roles, but labels, component sets, key policy, and which result authorizes which action must be unambiguous. Never accept “any valid signature” when only a specific profile/tag/key class is authorized.

### Bind content with the correct digest semantics

RFC 9530 distinguishes `Content-Digest`, computed over actual HTTP message content, from `Repr-Digest`, computed over selected representation data. For a typical signed request body, the application specifies which digest field/algorithm is required, validates it against the exact defined bytes, and covers the digest field in the signature.

A digest alone is not a MAC/signature: an attacker can change body and digest together. A signed digest commits the signer to the corresponding body only if the verifier recomputes it, rejects unsupported/weak/ambiguous algorithms according to profile, and does not process content first.

Raw bytes, content encoding, transfer coding, trailers, and intermediary transformations matter. Decide whether the signer signs content before or after a content coding according to the chosen standard semantics; use libraries/profile test vectors. JSON whitespace/key order/numbers/duplicate names make “parse then reserialize” a dangerous custom canonicalizer. Prefer digesting the defined transmitted content rather than inventing canonical JSON unless an established canonical format/profile is required.

For streaming, bound size/time, compute digest incrementally, and do not commit irreversible effects before verification. Trailer-carried digest/signature support must be explicit across every intermediary; otherwise buffer/spool safely or use a standardized chunk-signing protocol. Protect temporary content and clean it on failure.

### Canonicalize at the semantic trust boundary

The signer and verifier must agree on method, scheme/authority, path, query, and fields. Reverse proxies commonly terminate TLS, rewrite host/path, normalize ports, decode/encode paths, reorder/combine fields, and append forwarding metadata. Define whether the external or internal effective target is signed and configure a trusted proxy to communicate it without accepting spoofed forwarding fields from clients.

Verify before an untrusted transformation, or guarantee that transformations preserve/reconstruct signed semantics. Do not “fix” failures by trying multiple canonicalizations, ignoring target, or falling back to unsigned values; this creates ambiguity an attacker explores.

Queries are especially hazardous: repeated parameters, empty values, order, plus versus percent encoding, case-sensitive names, Unicode, and framework parsing into maps can change meaning. Either cover the exact standard-derived target/query component or define a narrow profile with canonical parameter rules and reject ambiguous encodings. Ensure authorization/business code consumes the same interpretation that was signed.

HTTP fields can be combined/reordered/normalized under protocol rules, while some values are order-sensitive. Use RFC 9421 libraries and component rules, not raw string concatenation. Do not sign hop-by-hop fields. Reject conflicting duplicate routing/content/security fields before they reach an alternate parser.

Redirects change targets and generally require a new signature. Clients must not forward signed authorization material to a redirect destination automatically unless the profile explicitly and safely handles it.

### Design freshness and replay state together

Validate `created` is not too far in the future, signature age is below a maximum, and `expires` is present/within profile bounds where required. Use a reliable clock and a small explicit skew allowance. A long window improves tolerance/offline queuing but enlarges replay exposure and nonce retention; a short window raises clock and delayed-delivery failures.

Timestamp validation alone means a captured request remains valid throughout the window. For single-use proof, require a sufficiently unpredictable/unique nonce or JTI and atomically reserve it only after cheap structural bounds, key lookup/profile/time checks, and successful signature authentication. Scope the key by signer/key/profile and, where protocol defines, target/token. Retain the reservation until no verifier could accept the proof, including skew/delivery allowance.

All accepting nodes/regions need duplicate semantics consistent with the guarantee. Per-process caches let a replay hit another node. A distributed conditional insert/unique constraint can supply atomicity; partitions require fail-closed, region-bound proofs, or explicitly weaker documented behavior. Check-then-insert without atomicity races.

Defend the ledger: bound nonce length/format and accepted time before storage; store a cryptographic hash when appropriate; quota/rate-limit authenticated principals and unauthenticated failures; expire records; monitor cardinality/latency; and never let unauthenticated attacker-chosen nonces fill durable storage. Server challenges can reduce clock dependence and pre-generation but need issuance, binding, lifetime, and duplicate policy.

### Keep DPoP's guarantee precise

RFC 9449 DPoP sender-constrains OAuth tokens using a proof JWT. Required claims include unique `jti`, HTTP method `htm`, target URI `htu` (without query/fragment), and creation time `iat`; resource access also binds the access token via `ath`, and servers can require a nonce.

DPoP reduces the usefulness of a stolen access/refresh token when the attacker lacks the proof key. It is application-layer proof of possession, not full HTTP message signing: the standard proof does not bind arbitrary request bodies, all headers, or query parameters. Local authorization, object/state checks, TLS, and input validation remain necessary.

For strict replay rejection, track JTI in the defined context/window; RFC 9449 notes cluster state feasibility and memory-exhaustion considerations. A server nonce can narrow pre-generation/replay but repeated nonce use can be safe only when JTI duplicates are still rejected according to the profile.

### Separate proof replay from business duplication

A one-time nonce should change on a legitimate retry, because resending the exact proof is a replay. The idempotency key should remain stable for retries of the same intended business operation. The server authenticates each fresh request, then atomically maps `(principal,operation,idempotency-key)` to a request fingerprint and result.

If a client times out after a charge commits, it signs a new HTTP request with new timestamp/nonce and the original idempotency key. Replay protection accepts the new proof; idempotency returns the original outcome rather than charging again. Reusing the key with different business parameters is a conflict.

Even perfect proof-replay prevention cannot stop the legitimate signer from issuing two freshly signed “charge” requests with different nonces and idempotency keys. Domain limits, uniqueness, workflow/state transitions, confirmation, fraud/rate controls, and authorization govern that risk.

Webhook/event systems likewise separate unique delivery proof from event deduplication. Providers may retry the same event in newly signed deliveries; receivers authenticate each delivery and process the stable event ID idempotently. Retain event dedupe state for the business retry horizon, often longer than signature nonce state.

### Operate key identity, algorithms, and rotation safely

`keyid` is a lookup hint, not self-authenticating identity. Resolve it in a trusted registry bound to principal, tenant, environment, algorithm/key type, allowed signature profile/tags, actions/audiences, status, validity, and rotation lineage. Reject unknown, disabled, expired, wrong-environment, or unauthorized keys.

Pin allowed algorithms/profile; do not let attacker input switch asymmetric to HMAC or reinterpret public material as a shared secret. Use maintained cryptographic libraries, secure key sizes, constant-time MAC comparison, and secure private/shared key storage. Never reuse one shared HMAC secret across unrelated tenants/clients when attribution/isolation matters.

Rotation overlaps old/new verification only for a bounded period. Signers activate new key, verifiers receive it, traffic migrates, old proof windows/queues drain, then old key is disabled/removed according to incident and audit requirements. Revocation must propagate within a stated bound; a cryptographically valid proof under a revoked key is rejected by policy.

Log public key IDs and decision reasons when safe, never private/shared keys, raw bearer tokens, or full signature material unnecessarily. Key IDs and certificate chains can still reveal topology/identity, so protect operational logs and minimize public errors.

### Understand presigned URLs and signed capabilities

A presigned URL places a signature and expiration in a URL/query, creating a bearer capability for the covered resource/action. Anyone who obtains it can use it until expiry unless another control binds it. URLs leak through logs, browser history, referrers, analytics, screenshots, and forwarded messages.

Keep lifetime short, method/resource/headers/audience narrow, permissions minimal, HTTPS mandatory, response cache/referrer policy appropriate, and revocation feasible for sensitive objects. Avoid putting long-lived credentials or broad prefixes in the capability. Do not claim single-use unless the service atomically records a unique capability identifier.

AWS Signature Version 4 illustrates a mature application profile with canonical request, signed headers, payload hash, credential scope, and time-bound derivation. Its exact rules belong to AWS; copying fragments into a custom protocol is not interoperability or equivalent assurance.

### Verify in a safe order and observe without leaking

Before expensive work, enforce request size, field count, signature structure, supported profile/algorithm, key ID/nonce bounds, and rate limits. Resolve key and validate coarse time. Read/hash a bounded body as required, reconstruct the signature base, verify cryptographically, then atomically reserve the nonce. Only afterward treat signed components as authenticated and perform token, authorization, schema, object/state, idempotency, and business processing.

Ordering balances DoS and correctness: inserting an unverified nonce lets attackers poison the ledger; processing body/domain effects before digest/signature lets unauthenticated input act; revealing “nonce already used” before proof can create an oracle. Use generic public authentication errors while recording protected reason codes.

Observe verification outcome/reason, profile/tag, key class/ID (bounded), signer/client/tenant, age/skew bucket, nonce duplicate, body size/hash algorithm, target/action, proxy route, latency, idempotency outcome, trace, and key revision. Avoid raw signatures/nonces/tokens/body as metric labels or logs. Alert on replay bursts, skew drift, unknown keys/algorithms, canonicalization clusters, cross-target attempts, verification resource spikes, revoked-key use, and regional duplicate inconsistencies.

The executable model spells out the small RFC 2104 HMAC construction over SHA-256 to demonstrate component binding, time validation, comparison without content-dependent early exit, and atomic-style nonce uniqueness in one process. This is educational executable evidence; production code must use a maintained cryptographic/protocol library, and the model is neither an RFC 9421 implementation nor a distributed ledger.

<!-- bijux-verify: {"id":"signed-request-replay-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=allow\nreplay=deny:replay\ntampered=deny:signature\nstale=deny:time\nwrong_target=deny:signature\n","stderr":""}} -->
```python
import hashlib

KEY = b"demonstration-key-not-for-production"
NOW = 1_800_000_000
MAX_AGE = 120
seen = set()

def hmac_sha256(key, message):
    block_size = 64
    if len(key) > block_size:
        key = hashlib.sha256(key).digest()
    key = key.ljust(block_size, b"\x00")
    inner = bytes(byte ^ 0x36 for byte in key)
    outer = bytes(byte ^ 0x5C for byte in key)
    return hashlib.sha256(outer + hashlib.sha256(inner + message).digest()).hexdigest()

def equal(left, right):
    if len(left) != len(right):
        return False
    difference = 0
    for left_byte, right_byte in zip(left.encode(), right.encode()):
        difference |= left_byte ^ right_byte
    return difference == 0

def base(method, authority, path, body, created, nonce):
    digest = hashlib.sha256(body).hexdigest()
    return f"{method}\n{authority}\n{path}\n{digest}\n{created}\n{nonce}".encode()

def sign(method, authority, path, body, created, nonce):
    return hmac_sha256(KEY, base(method, authority, path, body, created, nonce))

def verify(method, authority, path, body, created, nonce, signature):
    if created > NOW + 5 or NOW - created > MAX_AGE:
        return "deny:time"
    expected = sign(method, authority, path, body, created, nonce)
    if not equal(expected, signature):
        return "deny:signature"
    replay_key = hashlib.sha256(("client-7|" + nonce).encode()).hexdigest()
    if replay_key in seen:
        return "deny:replay"
    seen.add(replay_key)
    return "allow"

body = b'{"amount":125,"currency":"EUR"}'
signature = sign("POST", "api.example", "/payments", body, NOW - 10, "nonce-1")
print("first=" + verify("POST", "api.example", "/payments", body, NOW - 10, "nonce-1", signature))
print("replay=" + verify("POST", "api.example", "/payments", body, NOW - 10, "nonce-1", signature))
print("tampered=" + verify("POST", "api.example", "/payments", body + b" ", NOW - 10, "nonce-2", signature))
stale = sign("POST", "api.example", "/payments", body, NOW - 121, "nonce-3")
print("stale=" + verify("POST", "api.example", "/payments", body, NOW - 121, "nonce-3", stale))
print("wrong_target=" + verify("POST", "api.example", "/refunds", body, NOW - 10, "nonce-4", signature))
```

The model omits TLS, HTTP structured-field parsing, key registry/rotation, asymmetric algorithms, DPoP, proxies, distributed atomic storage, streaming, authorization, idempotency, and side effects; each needs separate evidence.

## Definitions and Notation

Let request $r$ have effective method, authority, target, fields, and content. Proof $p$ contains signature value, covered-component identifiers, creation/expiration, nonce, key ID, algorithm/profile/tag metadata. $B(r,p)$ is the standards/profile-defined signature base. Trusted key record $k$ binds verification material to principal, algorithm, profile, status, and authorization context.

$V_{sig}$ verifies the cryptographic value over $B$; $V_{content}$ recomputes required digest; $V_{time}$ enforces creation, expiration, maximum age, and skew; $V_{nonce}$ atomically proves unused uniqueness in the profile scope; $V_{context}$ binds target, token, tenant, audience, or challenge as the profile demands. Replay key $n=(principal,keyid,profile,nonce)$ is reserved until $t_{retain}\ge t_{last-accept}$.

A **replay-safe proof** means the same accepted proof cannot pass again within the declared acceptance topology/scope. It does not mean the signer cannot authorize a semantically identical new request. **Idempotent execution** means retries identified as one operation do not duplicate its effect. **Exactly-once delivery** is not implied by either.

## Mechanisms, Invariants, or Proof Structure

1. State the capture/tampering/replay threat and why authenticated TLS or bearer tokens alone do not meet it.
2. Choose a maintained standards/profile implementation; fix algorithms, key classes, tags, and component requirements.
3. Define the effective HTTP boundary and cover every method/target/query/field/content/token semantic the application trusts.
4. Recompute and verify required content digest over the precisely defined bytes/representation before processing.
5. Resolve key ID through a trusted principal/profile/algorithm/status registry and verify signature without downgrade/fallback ambiguity.
6. Enforce creation/expiration/maximum age/skew and challenge policy, then atomically reserve a bounded nonce/JTI across accepting nodes.
7. Treat only covered components as authenticated; strip/reject conflicting unsigned inputs.
8. Separately authenticate token/context, authorize action/object/state, validate input, and apply domain invariants.
9. Use a stable idempotency key for legitimate retries but a fresh single-use proof; operate rotation/revocation and safe audit.
10. Test canonicalization/transformation, tampering, replay races/partitions, skew, body streaming, retries, key lifecycle, and resource exhaustion end to end.

Assuming unforgeability of the chosen primitive/key, correct standard serialization, complete component profile, authoritative key registry, and protected verifier, signature success supports that a key possessor produced the covered semantics. If the atomic nonce ledger includes every accepted proof in scope until its final possible acceptance, a second acceptance of the same scoped nonce is prevented. These bounded arguments do not prove signer intent, key custody, permission, full-message integrity, confidentiality, or business uniqueness.

## Alternatives and Trade-Offs

HMAC is fast and simple but signer/verifier share forgery power and secret distribution scales poorly. Asymmetric signatures isolate verifier public keys and support many verifiers/rotation, at greater computational/PKI complexity. Choose by trust topology, not fashion.

mTLS sender-authenticates a connection/workload and avoids application canonicalization, but proof may terminate at proxies and does not necessarily bind a message end-to-end. HTTP message signatures can span selected intermediaries and fields but require precise profiles and transformations. They can be combined.

DPoP sender-constrains OAuth tokens and binds method/URI/token with standardized JWT proof; it does not sign arbitrary body/query fields. Full HTTP message signatures can cover broader semantics but are not automatically OAuth token binding. A provider-specific webhook HMAC may be acceptable when exactly specified, maintained, and tested; a new custom scheme is expensive risk.

Client timestamps are stateless and cheap but only bound replay duration and suffer skew. Stateful nonce/JTI ledgers give single-proof rejection but add consistency, storage, availability, and DoS concerns. Server challenges reduce clock/pre-generation risks but add a round trip/state/profile complexity. Select per risk and delivery model.

Buffering bodies simplifies verification-before-processing but costs memory/disk/latency. Incremental digest with delayed commit supports streams, while trailers/chunk signing need end-to-end support. Set limits and never weaken body coverage merely for convenience.

Fail-closed replay storage protects integrity during outage but reduces availability. Region-bound challenges/proofs or strongly consistent stores can localize coordination; fail-open explicitly abandons the single-use guarantee and is unsuitable for high-risk effects. Document the decision and emergency mode.

## Failure Modes and Misconceptions

- **“The signature is valid, so the request is authorized.”** Key possession and message integrity do not grant action/object/state permission.
- **“TLS prevents replay.”** It protects a connection; captured application credentials/proofs and terminating intermediaries need their own model.
- **“A timestamp makes it unique.”** Every replay inside the window still has a valid timestamp.
- **“A nonce field prevents replay.”** Only scoped atomic duplicate detection/challenge semantics make it effective.
- **“A digest authenticates the body.”** An unsigned digest can be replaced alongside the body.
- **“We sign JSON.”** Undefined parse/reserialize/duplicate/number/Unicode rules create divergent bytes/semantics.
- **“Path is enough.”** Method, authority, query, content, and trusted headers can change the action.
- **“All headers should be signed.”** Hop-by-hop/volatile transformations break interoperability; profile the meaningful stable components.
- **“The proxy is transparent.”** Host/path/scheme/port/query/field rewrites change the effective signature boundary.
- **“DPoP signs the request body.”** Its standard proof binds method/target URI/token/time/JTI, not arbitrary content.
- **“One replay cache per node is fine.”** A captured proof can be routed to another node or race two nodes.
- **“Nonce checked then inserted.”** Non-atomic check/insert admits concurrent duplicates.
- **“Signed retries reuse the signature.”** One-time proof retries require a new nonce/signature; business idempotency key remains stable.
- **“Replay prevention means no duplicate charge.”** A signer can create a fresh proof; domain/idempotency controls remain required.
- **“Presigned means private or single-use.”** The URL is usually a bearer capability until expiry unless explicitly constrained/recorded.

## Worked Examples

### Example 1

**Situation:** A payment request signs only its JSON body. **Reasoning:** The same signed amount/payee can be moved from `/quotes` to `/payments` or from `POST` to another accepted method if target/method are unbound. Require a profile covering method, authority, target/query, content type/digest, time/nonce/key/profile, plus any trusted idempotency/tenant fields. **Conclusion:** signature coverage must bind operational semantics, not merely data bytes.

### Example 2

**Situation:** A request sends a SHA-256 `Content-Digest`, but the signature covers only target/time. **Reasoning:** An attacker replaces body and digest together; both individually validate. Cover the digest field in the signature and recompute it over defined content before processing. **Conclusion:** digest supplies integrity evidence only when anchored to authenticated metadata.

### Example 3

**Situation:** A five-minute timestamp window has no nonce ledger. **Reasoning:** A captured valid transfer can be replayed repeatedly for five minutes. A two-minute window merely reduces opportunities. Require bounded unique nonce and cluster-atomic reservation retained through the last skewed acceptance, plus idempotency/domain controls. **Conclusion:** timestamps bound replay exposure; state/challenges reject reuse.

### Example 4

**Situation:** Two API nodes each use an in-memory nonce set. **Reasoning:** The first request hits node A and replay hits B; both see unused. A concurrent replay can also race check/insert. Use a shared/partitioned authoritative atomic uniqueness operation, or region-bound proofs with explicit routing/guarantee; fail closed on unavailable integrity state. **Conclusion:** replay guarantee scope is a distributed-systems property.

### Example 5

**Situation:** Client retries a committed charge after timeout. **Reasoning:** Reusing the old nonce is correctly denied, but denying all retry would break recovery. Client creates a fresh timestamp/nonce/signature and reuses the same charge idempotency key/body fingerprint; server returns stored result. **Conclusion:** freshness identifiers rotate per HTTP attempt while operation identity remains stable.

### Example 6

**Situation:** An edge proxy rewrites external `/v1/pay` to internal `/payments` and changes authority. **Reasoning:** Signer/verifier bases differ. Verify external semantics at edge and pass authenticated internal context, or define a trusted reconstruction/profile with spoof-resistant forwarding metadata. Never try both paths/fallback. **Conclusion:** canonicalization must name the actual trust boundary and transformation owner.

### Example 7

**Situation:** A stolen DPoP-bound access token is presented without its key. **Reasoning:** Resource server validates token binding plus proof signature, `htm`, `htu`, `iat`, `jti`, `ath`, and nonce policy, so theft alone is insufficient. But altered body/query can remain outside DPoP coverage and a key-compromised attacker can create new proofs. **Conclusion:** DPoP narrows bearer replay; it is not full-request or authorization proof.

### Example 8

**Situation:** A webhook receiver parses JSON, reserializes sorted keys, then checks provider HMAC. **Reasoning:** Whitespace, numbers, duplicate members, Unicode, and provider byte definition diverge. Retain bounded raw bytes, verify provider-specified timestamp/signature over those bytes, then parse once; dedupe stable event ID separately. **Conclusion:** verify the profile-defined representation before semantic processing.

### Example 9

**Situation:** A key rotates while delayed signed jobs remain queued. **Reasoning:** Disabling old key immediately rejects legitimate queue entries; accepting indefinitely prolongs compromise. Bound signature/job age, deploy new verification then signing key, drain within declared overlap, revoke old key, and require re-sign/requeue outside it. Incident revocation may intentionally sacrifice delayed work. **Conclusion:** key overlap must be derived from maximum accepted proof/delivery lifetime.

### Example 10

**Situation:** An attacker sends millions of huge unique nonces with invalid signatures. **Reasoning:** Storing before authentication exhausts replay state. Bound request/nonce/profile/key/time, rate-limit, verify signature, then store only a fixed-size scoped hash atomically with TTL; monitor cardinality. **Conclusion:** the replay defense itself needs authentication-aware resource controls.

## Cross-Program Connections

- **Cryptography:** unforgeability, MAC/signature trust topology, hashes, constant-time comparison, key separation, and downgrade resistance bound proof claims.
- **Distributed Systems:** atomic uniqueness, replication, partitions, clocks, queues, retries, regions, and fail-open/closed choices determine replay behavior.
- **HTTP Semantics:** effective URI, fields, content/representation, intermediaries, redirects, encodings, trailers, and structured serialization define the signed message.
- **Identity and Access Management:** key ownership, workload/client identity, token sender constraint, revocation, delegation, and audit map proofs to principals.
- **Domain Modeling:** command uniqueness, state transitions, idempotency, invariants, and compensations prevent repeated business effects.
- **Platform Engineering:** gateways, service meshes, secret/key services, time synchronization, shared stores, SDKs, and observability operate the protocol.
- **Formal Methods:** explicit assumptions/component sets and trace/replay models reveal gaps between primitive security and system guarantees.
- **Reliability Engineering:** timeouts, delayed delivery, retry recovery, ledger outages, rotation overlap, and capacity controls trade availability against integrity.

## References

1. Backman, A., Richer, J., and Sporny, M. [RFC 9421: HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421.html). IETF, February 2024. Checked 2026-09-01.
2. Polli, R., and Pardue, L. [RFC 9530: Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html). IETF, February 2024. Checked 2026-09-01.
3. Fett, D., Campbell, B., Bradley, J., et al. [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession](https://www.rfc-editor.org/rfc/rfc9449.html). IETF, September 2023. Checked 2026-09-01.
4. Krawczyk, H., Bellare, M., and Canetti, R. [RFC 2104: HMAC: Keyed-Hashing for Message Authentication](https://www.rfc-editor.org/rfc/rfc2104.html). IETF, February 1997. Checked 2026-09-01.
5. Fielding, R., Nottingham, M., and Reschke, J. [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). IETF, June 2022. Checked 2026-09-01.
6. Amazon Web Services. [AWS Signature Version 4 for API Requests](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html). AWS IAM documentation. Checked 2026-09-01.

## Exercises

### Exercise 1

Define an RFC 9421 application profile for a multi-tenant payment command. Specify covered components, key/profile policy, digest, time/skew, nonce scope/storage, authorization, errors, and proxies.

### Exercise 2

Trace five deliveries: first valid request, exact replay on another node, tampered body/new digest, legitimate retry after timeout, and freshly signed duplicate business command. State which control decides each.

### Exercise 3

Diagnose a webhook receiver that parses JSON before HMAC verification, accepts timestamps for 24 hours, stores no delivery IDs, logs signatures/bodies, and processes on three independent regions.

### Exercise 4

Compare mTLS, HMAC webhooks, asymmetric HTTP Message Signatures, DPoP, and presigned URLs for browser, partner, workload, and object-download use cases.

### Exercise 5

Design replay/signing for intermittently connected industrial devices that may be offline for days, have secure hardware keys, upload large streams, and trigger safety-relevant commands.

## Answers to the Exercises

### Answer 1

Require a named payment profile/tag and approved asymmetric algorithm/key registry binding key ID to client/tenant/environment/actions/status. Cover `@method`, external scheme/authority/target URI or exact required query components, `Content-Type`, SHA-256/512 `Content-Digest`, tenant/grant header if used, `Idempotency-Key`, and signature `created`, bounded `expires`, 128-bit nonce, key ID, algorithm/tag. Edge verifies external semantics before rewrite and strips spoofed forwarding/security fields; origin trusts only edge-authenticated context. Enforce small age/skew, atomically hash/reserve `(client,keyid,profile,nonce)` across regions through last possible acceptance, fail closed on ledger outage, bound inputs before signature and store only after verification. Then validate token, tenant/object/amount/state/beneficiary, command fingerprint/idempotency, version, limits, and audit. Public failures are generic; protected logs distinguish time, signature, replay, key, authorization, and idempotency reasons without secrets.

### Answer 2

The first valid request passes signature/component/digest/time/key checks, atomically reserves nonce, passes authorization, and commits under idempotency. Exact replay on another node must fail the shared atomic nonce ledger. Tampered body with new digest fails because the signed digest value no longer matches the signature; tampered body with old digest fails digest recomputation. A legitimate retry creates a new proof/nonce but keeps the same idempotency key and fingerprint, so proof passes and stored result returns. A freshly signed duplicate with a new idempotency key is not cryptographic replay; domain uniqueness/workflow/risk policy must reject or deliberately create another operation. Each guarantee has a distinct decision owner.

### Answer 3

Retain a bounded raw request stream, validate provider key/profile/timestamp structure, compute provider-defined HMAC in constant time before parsing/side effects, and use a short justified timestamp window. Require unique delivery ID inside authenticated material and atomic cross-region hash reservation; separately dedupe stable event ID for the provider retry horizon. Route to a home region or use strongly consistent uniqueness; on integrity-store outage fail closed/queue unprocessed. Reject ambiguous content types/encodings and oversized bodies/nonces before expensive work. Stop logging signature, secret, and raw body; record bounded key/provider/event/delivery hashes, result, age, region, trace, and safe reason. Rotate secrets per provider/tenant with bounded overlap, replay/canonicalization test through real gateways, and only then parse, authorize event/tenant/object, validate schema, and process idempotently.

### Answer 4

mTLS fits managed workload-to-workload connection identity but usually terminates at proxies and does not create portable message proof. HMAC fits one provider/receiver webhook relationship with simple raw-body/timestamp/delivery profile, but shared secret gives both sides forging power and needs per-partner isolation. Asymmetric RFC 9421 fits partner/end-to-end selected HTTP semantics and many verifiers, with more key/profile/canonicalization operations. DPoP fits OAuth public/native/browser-capable clients needing sender-constrained tokens; it binds proof key/method/URI/token but not arbitrary body/query. Presigned URLs fit delegated narrow object upload/download where bearer sharing is accepted; use minimal method/resource/headers/lifetime and treat leakage/revocation/single-use explicitly. TLS, authorization, freshness, and business idempotency still apply as relevant.

### Answer 5

Use hardware-backed asymmetric device keys registered to device/site/firmware/profile/actions and mutually authenticated encrypted transport when connected. Separate telemetry uploads from safety commands. For offline uploads, sign a manifest/chunk-tree or standardized stream format containing device, boot/session sequence, monotonic counter, capture-time range, content digests, schema, and destination; server keeps durable per-device counter/session/event dedupe and allows delayed data without allowing delayed commands. Safety commands use server challenges, very short expiry, exact device/action/parameters/state, command sequence, two-way acknowledgement, and local safety interlocks; stale commands never become acceptable because the device was offline. Protect monotonic state against rollback, define reset/re-enrollment recovery with operator approval, cap/spool streams and verify before publication, rotate/revoke with offline overlap policy, and distinguish fresh transport delivery proof from stable operation IDs. Test clock loss, counter reset, power failure, duplicate chunks, reordering, gateway proxying, partitions, key compromise, revocation, and safe fail-closed behavior.
