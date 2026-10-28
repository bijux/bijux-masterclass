# Module 8 — TLS, HTTP semantics, and backend protocol integrity

A Gateway can route to the correct Service and still violate the application contract. The listener may present the wrong certificate, use the wrong HTTP authority, trust a spoofed forwarding header, retry an unsafe request, buffer an unbounded upload, or speak plaintext to a backend that was assumed to be authenticated.

Networking is not complete when a TCP connection opens. The transport and application protocols must preserve identity, authority, timing, and message semantics across every proxy hop.

The engineering question is:

> Where does each TLS and HTTP trust decision occur, which peer is authenticated at that point, and which transformations are allowed before the request reaches Atlas?

## Learning outcomes

By the end of this module, you can:

- compare frontend termination, passthrough, and re-encryption without conflating them;
- separate SNI, certificate identity, HTTP authority, and backend identity;
- review certificate issuance, rotation, loading, and expiry as operational state;
- define a trusted forwarding-header boundary;
- compose timeout budgets across client, Gateway, Service, and backend;
- determine when retries are safe and when they duplicate effects;
- reason about buffering, streaming, body limits, and backpressure;
- prove backend protocol behavior rather than inferring it from an open port.

## Two connections, not one

With TLS termination at a Gateway, a client request commonly creates two distinct connections:

```text
client
  └── TLS connection A ──> Gateway
                              └── connection B ──> backend
```

Connection A and connection B have separate:

- peers;
- authentication decisions;
- protocols;
- timeouts;
- source addresses;
- certificates or plaintext boundaries;
- failure modes.

Calling this path “end-to-end TLS” is incorrect unless TLS remains in place and the client’s intended backend identity is authenticated through the full design. In the Atlas baseline, frontend HTTPS terminates at the shared Gateway and the Gateway-to-API hop is documented as HTTP. That is a deliberate accepted boundary, not an accidental omission.

## Three TLS placement models

### Frontend termination

The Gateway terminates client TLS, validates the incoming handshake as a server, and forwards a new request to the backend.

The Gateway owns:

- private-key access;
- certificate selection;
- supported TLS versions and cipher profile;
- SNI handling;
- client-facing protocol negotiation;
- HTTP authority validation;
- forwarding metadata;
- backend connection policy.

The backend must trust the Gateway as a proxy boundary, not treat the client socket as direct.

### Passthrough

The Gateway forwards encrypted bytes without terminating the client TLS session. Routing is generally based on information available before decryption, commonly SNI and connection metadata.

Passthrough preserves backend termination but limits L7 routing and filtering. The backend owns certificates and client protocol behavior. A passthrough Gateway cannot safely claim awareness of HTTP paths it never decrypts.

### Re-encryption

The Gateway terminates client TLS and establishes a second TLS connection to the backend. This protects the backend hop only when the Gateway validates the backend peer:

- trust anchor or approved issuer;
- expected DNS name or SAN;
- certificate validity;
- revocation/rotation policy where applicable;
- protocol and ALPN expectations.

Encryption without peer verification prevents passive observation but does not establish that the Gateway connected to the intended backend.

## SNI, certificate identity, and HTTP authority

These fields are related but distinct.

1. **SNI** is sent during the TLS handshake so the server can choose configuration and a certificate.
2. **Certificate identity** is established by validating the chain, validity, key usage, and expected hostname against SANs.
3. **HTTP authority** (`Host` in HTTP/1.1 or `:authority` in HTTP/2) identifies the logical HTTP target after TLS is established.

A request can send SNI `atlas.example.invalid`, validate a matching certificate, then carry a different HTTP authority. A shared edge must define whether that mismatch is rejected, redirected, or routed. Atlas rejects an unexpected authority with `421 Misdirected Request` in the local laboratory.

Do not infer HTTP authority from the TCP destination or SNI alone.

## Certificate lifecycle is distributed state

A Kubernetes Secret update does not prove that the Gateway is serving the new certificate. The controller and data plane must observe, load, and activate it.

A rotation timeline should record:

```text
new key/certificate issued
→ Secret or certificate reference updated
→ controller observes new resource version
→ data plane loads material
→ listener begins presenting new certificate
→ old certificate overlap period ends
→ old key is revoked or destroyed
```

Test from an independent client and record the presented certificate fingerprint or serial number. Include wrong-hostname, expired, untrusted-issuer, and missing-chain negative tests.

Certificate authority is also an ownership question. Who may issue for `*.example.invalid`? Who may reference the Secret? Who owns emergency rotation? Course 8 will govern cluster secret and admission policy; Course 5 records the edge contract.

## Backend protocol integrity

A Service port named `grpc` or `http2` is descriptive, not proof. A TCP handshake proves only transport reachability.

For HTTP/2 or gRPC, verify:

- TLS or cleartext mode as designed;
- ALPN negotiation where TLS is used;
- HTTP/2 preface and settings exchange;
- content type and framing;
- end-to-end deadline/cancellation behavior;
- whether an intermediary downgrades or buffers unexpectedly;
- health-check protocol compatibility.

For ordinary HTTP, verify authority, method, path, headers, body, status, and connection behavior. Protocol assumptions belong in the Gateway/backend contract, not only in port names.

## Read the TLS handshake as evidence

A TLS failure should be decomposed instead of reported as “certificate error.” Record the handshake stages that matter to the selected path:

```text
TCP connection
→ ClientHello with SNI and offered ALPN protocols
→ server certificate chain and key-exchange parameters
→ client chain construction and trust-anchor decision
→ SAN/hostname validation
→ negotiated protocol and cipher
→ Finished messages
→ application protocol exchange
```

A capture can show SNI, protocol offers, alerts, and timing, but encrypted application data remains protected. Client diagnostics can show chain and hostname decisions. Gateway logs can show certificate selection. These are complementary surfaces.

Common failures include:

- the listener serves a default certificate because SNI did not match;
- the certificate contains the right common name but not the required SAN;
- an intermediate certificate is missing;
- the client trusts a different root set from the test machine;
- the certificate has expired or is not yet valid;
- key usage or extended key usage is incompatible with server authentication;
- the client and listener share no protocol/cipher profile;
- ALPN negotiates HTTP/1.1 while the backend contract expects HTTP/2;
- a proxy presents a new certificate that the client did not intend to trust.

Do not disable hostname verification to “test connectivity” and then count the result as TLS success. If local DNS is inconvenient, pin the TCP socket to an address while still supplying the intended SNI and hostname to the TLS verifier, as the Course 5 loopback lab does.

## Backend TLS policy and target identity

When the Gateway uses TLS to the backend, the target identity must be explicit. “Use HTTPS on port 8443” is incomplete. The Gateway needs to know which name it expects, which trust anchors are authoritative, and which backend protocol is negotiated.

Gateway API provides policy resources for backend TLS in supported profiles. Their presence does not prove implementation support or successful peer verification. Review:

- policy attachment to the exact Service and port;
- approved CA source;
- expected hostname or SAN;
- cross-namespace reference authority;
- status and observed generation;
- controller conformance for the feature;
- rotation behavior;
- failure when the backend presents the wrong identity.

A backend certificate issued by a trusted CA but valid only for another service must be rejected. Trusting the issuer without checking the service name authenticates “some member of this PKI,” not the intended Atlas backend.

## Trusted forwarding metadata

An Internet client can send `X-Forwarded-For`, `Forwarded`, `X-Forwarded-Proto`, or any custom header. If the Gateway appends to or preserves those values without a trust rule, the application can be tricked into believing an attacker-chosen identity or scheme.

At the first trusted proxy boundary:

1. discard or replace untrusted forwarding metadata;
2. write the transport peer actually observed;
3. record the external scheme and authority established by the Gateway;
4. define whether later trusted proxies append in a known order;
5. configure the application to trust metadata only from approved immediate peers.

Forwarded addresses are operational evidence, not authenticated user or workload identity. Application authorization still uses Course 3 credentials and policy.

## Timeouts form one budget

Independent timeout values can multiply latency. Suppose:

```text
client deadline:          10 s
Gateway request timeout:  30 s
backend connect timeout:   5 s
backend retry count:        3
```

The Gateway may continue work after the client has abandoned the request, and retries can exceed the original client budget.

Start with one end-to-end deadline, then derive child budgets:

```text
remaining budget
− transport and processing reserve
= maximum backend attempt budget
```

Include:

- DNS resolution;
- connection establishment;
- TLS handshake;
- request-body upload;
- backend processing;
- response headers;
- streaming idle time;
- total request lifetime;
- retry backoff.

Cancellation should propagate where the protocol and application support it. A disconnected client does not automatically stop backend work.

## Retry safety

A retry is safe only when all relevant conditions hold:

- the failure is plausibly transient;
- the operation is idempotent or has an idempotency contract;
- the request body can be replayed without corruption or unbounded buffering;
- the remaining deadline covers another attempt;
- retry policy will not amplify load during an outage;
- downstream components do not also retry independently without a shared budget.

Retrying `GET` is often semantically safer than retrying a command, but even safe methods can create load amplification. Retrying `POST /analysis-runs` can duplicate work unless the same idempotency key and request fingerprint are preserved through the Gateway and authoritative service.

A retrying proxy cannot repair an application that lacks idempotent effect semantics.

## Buffering, streaming, and body limits

A proxy may buffer a request or response to support retries, transformations, security inspection, or slow-client isolation. Buffering consumes memory or disk and delays streaming. Disabling buffering can expose backpressure and connection-lifetime pressure to the backend.

Define:

- maximum request-header and body size;
- maximum buffered bytes;
- spill-to-disk policy and storage ownership;
- stream idle timeout;
- total stream lifetime;
- behavior when the client is slower than the backend;
- whether the body is replayable;
- cancellation cleanup;
- metrics for buffered and rejected traffic.

A large upload path should not be made “reliable” by buffering the entire body in Gateway memory.

## HTTP semantics across proxies

The Gateway can alter semantics through:

- path rewrites;
- redirects;
- header modification;
- method handling;
- retries;
- mirroring;
- compression;
- buffering;
- protocol conversion.

Review every transformation against the public API contract. A path rewrite can bypass application routing assumptions. A redirect can change origin and credential behavior. Mirroring can disclose protected data. Compression can create CPU pressure or side-channel risk in some contexts.

The edge is not authorized to invent application behavior merely because it can express a filter.

## Connection reuse, draining, and protocol state

Gateways reuse backend connections to reduce handshake and connection cost. Reuse changes failure and rollout behavior:

- a connection can remain bound to an endpoint after it leaves the eligible set;
- certificate rotation may affect new connections while old TLS sessions remain;
- HTTP/2 multiplexes many requests over one connection, so draining one endpoint needs protocol-aware GOAWAY and timeout behavior;
- connection pools can concentrate load or retain stale DNS/endpoint state;
- backend shutdown must allow the Gateway to stop opening new streams and finish or cancel existing ones.

Define separate limits for connection age, idle time, request lifetime, and graceful drain. During rollout, observe both new connections and established long-lived streams. “Endpoint removed from EndpointSlice” does not prove every proxy connection was closed.

## Worked investigation — a retry creates two analyses

A Gateway is configured to retry backend `500` responses. The client submits `POST /analysis-runs`. The first backend attempt commits the run but loses the response during a process crash. The Gateway retries to another Pod without preserving a valid idempotency contract. Two runs are created.

The network delivered exactly what the retry policy requested. The failure was semantic: the edge treated a non-idempotent effect as replay-safe.

The repair is to:

- preserve the client’s idempotency key and request fingerprint;
- ensure the authoritative service persists replay state transactionally;
- retry only within the original deadline;
- limit attempts and amplification;
- test the commit-with-lost-response case;
- expose retry/attempt evidence in telemetry.

Course 2 owns durable idempotency. Course 5 ensures the Gateway does not weaken it.

## Capstone implementation

Module 8 uses:

- `capstone/atlas_net/tls.py` for certificate and hostname decisions;
- `capstone/atlas_net/gateway.py` for forwarding-header and retry policy;
- `capstone/atlas_net/localnet.py` for real local TLS proxying;
- `capstone/pki/` for bounded course certificate fixtures;
- `capstone/scripts/tls_gateway_lab.py` for wrong-hostname rejection and verified SNI/hostname success;
- `capstone/manifests/frontier/backend-tls-policy-example.yaml` as a standards-frontier example, not an executed baseline claim.

The successful local test pins the TCP socket to loopback while preserving CA-chain verification, SNI, certificate hostname verification, and HTTP authority validation. It proves the fixture path, not managed certificate automation or cloud Gateway behavior.

## Release evidence

A credible TLS/HTTP release records:

- listener protocol and certificate references;
- issued names, chain, key usage, and validity;
- rotation and overlap procedure;
- SNI/authority mismatch behavior;
- frontend and backend TLS boundaries;
- backend identity-verification method;
- forwarding-header trust contract;
- timeout and retry budget;
- request/response size and streaming policy;
- protocol negotiation evidence;
- negative tests for wrong name, untrusted issuer, unsafe retry, and oversized body.

## Certificate validation is an algorithm, not a padlock

A client authenticates a TLS server only when it builds a path to a trusted anchor, verifies signatures and validity, matches the intended DNS or IP identity, enforces key usage and policy, negotiates an allowed protocol, and rejects failure. Pinning the socket to a local address while validating `atlas.example.invalid` is useful in a laboratory because it separates routing from logical identity. Disabling hostname verification or trusting the presented leaf certificate directly changes the claim and is not an acceptable repair.

The validation dossier should record the intended authority, SNI name, verified certificate names, trust anchors, validity interval, negotiated protocol, and failure observed for a wrong name and an untrusted issuer. A successful encrypted connection without peer verification proves confidentiality against some passive observers, not server identity.

## Frontend and backend TLS are independent trust decisions

When the Gateway terminates client TLS and opens a second TLS connection to a backend, two identities exist:

```text
client authenticates Gateway listener identity
Gateway authenticates backend service identity
```

The backend may also authenticate the Gateway with mTLS. Each connection needs its own expected names, trusted roots, certificate lifecycle, and failure policy. Re-encryption without backend name verification does not prove that the intended service received the request.

A standards resource such as BackendTLSPolicy or implementation-specific configuration can express part of this relationship. The release still needs evidence that the selected controller supports the feature and that the data plane verifies the configured backend identity.

## Connection reuse changes retry and rollout behavior

A request can be retried by the client, cloud load balancer, Gateway, SDK, or application. Independent retry loops multiply one failure into many backend attempts. Define one end-to-end budget and allocate it deliberately:

```text
client deadline
  > gateway queue and processing
  > backend connection and TLS
  > one or more bounded attempts
  > backoff
  > response transmission
```

A retry is safe only when operation semantics support replay or the same idempotency identity is preserved through every attempt. A proxy's ability to resend bytes does not make a command idempotent.

Long-lived HTTP/2 and gRPC connections also affect rollout. New Routes, certificates, or backend sets can be correct for new connections while existing sessions continue through old upstream state. Test new and established connections separately.

## Streaming and buffering are resource policies

A Gateway may buffer, stream, transform, or reject bodies. Buffering can isolate a backend from a slow client and enable retries, but it consumes memory or disk and delays first-byte delivery. Streaming lowers buffering but holds connections and requires end-to-end backpressure.

For uploads, downloads, server-sent events, WebSockets, and gRPC streams, define:

- maximum header and body sizes;
- read, write, idle, and overall deadlines;
- memory and disk buffering limits;
- cancellation propagation;
- client-disconnect behavior;
- backend connection reuse;
- retry prohibition or replay mechanism;
- telemetry that avoids payload leakage.

A correct small JSON request does not prove the streaming path.

## Forwarded metadata is a protocol between trusted hops

The first trusted proxy must remove or overwrite untrusted forwarding headers before adding its own values. The backend should trust them only from an approved immediate peer and retain that peer address for audit.

The forwarding contract should define format, append-versus-replace behavior, maximum chain length, malformed-value handling, logical scheme and authority derivation, privacy, and bypass behavior. Course 8's loopback Gateway proves replacement of a forged `X-Forwarded-For` value for the fixture path. It does not establish behavior for an external load balancer that was not executed.

## Transition

Module 8 secures and preserves north-south protocol behavior. Module 9 follows traffic leaving Atlas toward external dependencies, where DNS changes, redirects, NAT state, proxies, private endpoints, and optional service-mesh controls create new ownership and trust decisions.
