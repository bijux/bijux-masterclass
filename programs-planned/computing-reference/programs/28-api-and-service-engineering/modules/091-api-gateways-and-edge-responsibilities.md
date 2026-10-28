---
module_id: API-091
program: API & Service Engineering
level: 2
module_number: 91
title: API Gateways and Edge Responsibilities
status: complete
last_verified: 2026-09-02
---

# API Gateways and Edge Responsibilities

## One-Page Review

### Governing question

Which connection, protocol, trust, routing, traffic, resilience, observability, and lifecycle responsibilities belong at an API gateway/edge, which must remain end-to-end or service/domain-owned, and how can that boundary avoid becoming a privileged bottleneck or hidden application?

### Essential definitions

- An **API gateway** is a managed intermediary that accepts client-facing traffic and applies governed cross-cutting connection, protocol, trust, routing, and traffic policy before an upstream.
- The **edge** is the outer trust/network boundary for a particular exposure; it is architectural, not necessarily one product or hop.
- A **reverse proxy** acts toward clients as the selected origin-facing intermediary; a gateway may add API-aware policy and control-plane integration.
- **authentication termination** validates external credentials/context; **authorization** still requires the resource/action/domain decision at the authoritative service boundary.
- **protected forwarding context** is gateway-derived identity/tenant/capability metadata whose untrusted inbound names are stripped and whose integrity/confidentiality is protected downstream.
- A **routing policy** maps a validated request to an eligible backend based on governed authority, route, version/capability, health, locality, and rollout—not arbitrary client destinations.
- The **data plane** processes live traffic; the **control plane** distributes routes, identities, policy, certificates, quotas, and telemetry configuration.
- **edge-generated response** is a response produced without upstream completion, such as authentication denial, rate limit, malformed request, or gateway timeout.

### Central model, mechanism, or theorem

For request path hops $h_0\ldots h_n$, every hop transforms message/context under a declared contract. End-to-end safety requires the conjunction

$$
P\land T\land I\land R\land B\land O,
$$

where $P$ is protocol-semantic preservation, $T$ trusted-context integrity, $I$ identity/authentication validity, $R$ safe deterministic routing, $B$ bounded resource/resilience behavior, and $O$ observable attribution. A gateway pass cannot prove service object authorization or business invariants. Retry amplification across layers is multiplicative: if layer $i$ permits $r_i$ retries, one logical operation can produce up to $\prod_i(r_i+1)$ attempts before hedging/fan-out.

### Critical invariants

The gateway has an explicit responsibility/authority matrix. It parses and normalizes deterministically, rejects ambiguity, preserves method/status/header/body semantics unless an owned translation contract says otherwise, and never forwards spoofable identity as trusted. External credentials are validated under current issuer/audience/key/revocation policy; downstream context is minimal, protected, and audience-bound. Services enforce domain/action/object/property authorization.

Routing cannot become SSRF, tenant crossover, or unsafe failover. Timeouts fit end-to-end deadlines; retries are centrally budgeted and limited to safe/idempotent/replayable operations. Rate limits and overload protect shared capacity without pretending to be billing truth. Edge/origin failures, transformations, attempts, and policy revisions are distinguishable. Configuration is reviewed, validated, progressively delivered, reversible, audited, and independent of the per-request control plane.

### Common failures

Gateway as business monolith; one “central auth” check replaces object authorization; forwarding client-supplied identity/role/tenant; trusting `X-Forwarded-*` from the internet; token accepted for wrong issuer/audience; secrets/tokens logged; arbitrary upstream URL/host routing; ambiguous duplicate headers or path normalization; request smuggling; protocol translation changes semantics; retrying unsafe bodies; client+gateway+service retries multiply; timeout exceeds caller deadline; retrying overload; global rate limiter fails open/closed accidentally; cache omits auth/tenant/version; 502/504 masks cause; gateway span blamed on origin; high-cardinality sensitive metrics; control-plane outage removes data-plane config; config blast radius global; health check differs from real dependency; TLS termination leaves unprotected internal hop; and legacy transform/route never removed.

### Compact example

An internet client sends `X-User-Id: admin` with a valid token for tenant A. The gateway strips all protected internal headers, validates token issuer/audience/signature/time, derives subject/tenant/scopes, signs/encrypts minimal downstream context, and routes only to the allowlisted service. The service then checks whether that subject may update the requested object in tenant A. **Conclusion:** edge authentication establishes trusted context; domain authorization remains at the resource/effect boundary.

### Connections

[Tracing Through Client, Proxy, and Service](010-tracing-a-request-through-client-proxy-and-service.md), [Authentication Context Propagation](033-authentication-context-propagation.md), [Object-Level Authorization](046-object-level-authorization.md), [Retries](072-retries-and-backoff.md), [Load Shedding](074-api-level-load-shedding.md), [Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), and [Independent Evolution](090-evolving-an-api-without-coordinated-consumer-releases.md) define end-to-end constraints. Later modules separate service discovery, mesh, testing, and operations from edge responsibilities.

## Governing Question

How should teams allocate, implement, secure, test, operate, and evolve API gateway responsibilities across external clients, intermediaries, services, service discovery, identity systems, policy control planes, and multi-tenant platform ownership?

## Why This Matters

A gateway is positioned to solve common edge problems once: certificates, protocol parsing, external authentication, routing, admission control, quotas, consistent metadata, rollout, and edge observability. That leverage also creates a high-value target and blast radius. One malformed route, stale key, permissive header, retry policy, or configuration rollout can affect every service.

Centralization tempts teams to move domain behavior outward. Soon the gateway joins data, translates business state, owns per-customer exceptions, and decides authorization without authoritative objects. Releases then couple through one privileged monolith while services no longer know their own security/contract.

HTTP intermediaries are protocol participants. Path, authority, method, headers, content, conditions, caching, retries, status, and trailers carry meaning. “Just proxying” can break signatures, idempotency, negotiation, streaming, and client diagnostics. Protocol translation must be an explicit contract, not incidental configuration.

The edge is also a partial observer. It sees accepted connections/requests but may not know business effects, downstream authorization, internal retries, or consumer identity behind a relay. Its metrics are valuable but not complete. Durable design assigns each decision to the narrowest authoritative boundary and preserves end-to-end evidence.

## Prerequisites and Retrieval

Retrieve [Tracing a Request Through Client, Proxy, and Service](010-tracing-a-request-through-client-proxy-and-service.md), [HTTP Methods and Their Semantics](002-http-methods-and-their-semantics.md), [Headers and Metadata](004-headers-and-metadata.md), [Caching](007-caching.md), [Authentication Context Propagation](033-authentication-context-propagation.md), [Authorization Checks](034-authorization-checks.md), [Rate Limits and Quotas](039-rate-limits-and-quotas.md), [Credential and Token Handling](042-credential-and-token-handling.md), [Object-Level Authorization](046-object-level-authorization.md), [Replay and Request Signing](049-replay-and-request-signing.md), [Retries and Backoff](072-retries-and-backoff.md), [API-Level Load Shedding](074-api-level-load-shedding.md), and [Preventing Failure Amplification](080-preventing-failure-amplification-across-service-calls.md).

Retrieve traffic/exposure/trust diagrams; client/protocol/streaming requirements; DNS/load-balancer/CDN/WAF/gateway/mesh/backend chain; TLS/mTLS/certificates; identity issuers/keys/audiences/scopes; protected header/context contract; routes/discovery/health/failover; timeout/retry/circuit/load-shed/rate/quota/cache policies; request/body/header limits; transformations; tenant/environment separation; config source/review/deploy/rollback; SLO/capacity/cost; logs/metrics/traces/audit; incidents/threat models; consumer/ownership/deprecation inventory; and DR/control-plane behavior.

## Learning Objectives

After completing this module, you can:

1. distinguish edge, reverse proxy, API gateway, load balancer, WAF, service discovery, and service mesh responsibilities;
2. create an explicit gateway/service/platform/identity/domain responsibility and authority matrix;
3. preserve HTTP/RPC/stream semantics through parsing, normalization, forwarding, transformation, and edge-generated responses;
4. terminate external authentication while preserving service-owned action/object/property authorization;
5. establish protected downstream identity/tenant/capability context without trusting spoofable headers;
6. design allowlisted routing, health, failover, version/capability/cohort policy without SSRF or cross-tenant leakage;
7. budget deadlines, retries, body replay, rate limits, overload, caches, and connection resources end to end;
8. attribute client/gateway/upstream/policy failures and attempts through safe logs, metrics, traces, and audit;
9. operate a multi-tenant gateway data/control plane through validation, progressive delivery, isolation, rollback, and recovery; and
10. keep domain logic out of the edge and retire temporary routes, transforms, credentials, and policy safely.

## Core Exposition

### Draw the actual edge and hop chain

Inventory client, DNS, CDN, DDoS/WAF, cloud/network load balancer, ingress/reverse proxy, API gateway, mesh sidecar/proxy, service, and dependencies. A branded “gateway” may be several hops; a service can have separate internet, partner, employee, and internal edges.

For every hop record trust zone, owner, protocol termination/origination, address/authority, TLS/mTLS, authentication, authorization, routing, mutation, retry/cache, limits, telemetry, and failure responses. Identify which hop is externally reachable and whether bypass to service exists.

Use separate data and control flows. Certificate/key/route/policy/identity discovery/config/audit paths fail differently from live requests. A control-plane outage should not wipe known-good data-plane configuration.

Document proxy chains and loop prevention. Forwarded client address/scheme/host is evidence only from trusted immediate peers; strip or overwrite untrusted fields at the first trusted boundary.

### Allocate responsibilities by authority and information

Place connection/protocol concerns where traffic enters: TLS termination/passthrough, ALPN/protocol negotiation, parsing, header/body limits, connection/stream limits, basic normalization, trusted forwarding metadata, and edge denial.

Place external credential validation and coarse admission at the gateway when it has issuer/audience/route policy and reduces duplicate work. Place domain authorization where current resource ownership, action, object/property, state, and tenant invariants are authoritative—usually the service.

Place routing at the gateway only over allowlisted discovery/policy outputs. Service discovery owns endpoint membership/health metadata; the gateway consumes it. A service mesh primarily governs service-to-service traffic and does not automatically own external product/consumer policy.

Keep business orchestration, database joins, consumer-specific domain transformations, transaction state, and authoritative product decisions out of generic edge configuration. A bounded façade/BFF can be a separate owned API product even if deployed beside a gateway.

### Preserve protocol semantics

RFC 9110 defines HTTP semantics for methods, fields, status, representations, caching, conditions, and intermediaries. Preserve method/authority/path/query/header/content/trailer meaning and distinguish connection-specific metadata. Do not silently convert an unsafe operation to a retryable one.

Parse once according to one strict policy. Reject conflicting content lengths, invalid transfer encodings, ambiguous authority, invalid percent/path normalization, duplicate security-sensitive fields, and size/count limits consistently across edge and origin. Differential parsing enables request smuggling and auth/routing disagreement.

Streaming, WebSocket, SSE, gRPC, uploads, and trailers require protocol-aware timeout/buffering/backpressure behavior. Buffering an unbounded stream for inspection or retry can exhaust memory and destroy latency.

When translating protocols or envelopes, define exact mapping for methods/operations, metadata, content, status/errors, streaming/cancellation/deadlines, identity, retry/idempotency, and observability. Test round-trip/loss and unsupported behavior.

### Terminate transport security deliberately

Decide TLS termination/passthrough/re-encryption per trust boundary, certificate ownership, inspection, routing, client authentication, and end-to-end requirements. Termination makes plaintext available at that component; downstream links still require protection appropriate to threat and network.

Automate certificate issuance/rotation/revocation, secure private keys, validate names/chains/time, and monitor expiry/handshake/protocol/cipher. Test overlap and rollback during rotation.

For mTLS clients, bind authenticated certificate identity to registration/tenant policy and propagate only a protected derived identity if terminating. Never trust a client-cert header received from an untrusted hop.

Enforce modern protocol policy without surprising supported clients; collect version/cipher compatibility evidence before retirement. TLS protects transport, not application authorization, input safety, or data minimization.

### Authenticate at the gateway without centralizing all authorization

Validate credential type, signature/MAC, issuer, audience/resource, time/not-before/expiry, algorithm/key, required claims, token binding/proof if used, revocation/introspection policy, and route eligibility. Cache keys/introspection boundedly with expiry/revocation trade-offs.

RFC 6750 defines bearer tokens: possession is sufficient to use one, so protect against disclosure in transit, logs, URLs, errors, caches, and telemetry. Do not forward external tokens deeper than required; exchange/downscope for audience-specific credentials where architecture supports it.

The gateway can enforce coarse scope/route/method policy and deny obvious unauthenticated traffic. The service still verifies downstream trust and decides action/object/property/tenant/state authorization. Defense in depth prevents bypass/stale/misconfigured edge from becoming total compromise.

Distinguish authentication failure, insufficient permission, hidden resource, and upstream failure according to contract without leaking sensitive existence.

### Build protected forwarding context

Reserve internal header/metadata names. At the first trusted gateway, strip every inbound occurrence before deriving subject, client/application, tenant, scopes/roles, authentication method/time/strength, credential/token ID where safe, and trace/request correlation.

Minimize context; do not serialize whole tokens or uncontrolled claims. Protect integrity/authenticity via mTLS plus trusted network/workload identity, signed envelope, or authenticated channel; protect confidentiality and prevent replay/audience misuse. Include issuer/audience/expiry/key/version as needed.

Services accept context only from authenticated eligible gateway/workload identities and reject direct/untrusted duplicates. Define propagation through internal hops and whether each may attenuate but never elevate authority.

RFC 7239 `Forwarded` can disclose proxy information lost in forwarding, but client/address/host fields have privacy and trust limits. Treat them as untrusted unless produced by the known proxy chain; never use raw client IP as principal.

### Route safely and deterministically

Match normalized authority/host, path/operation, method, protocol, version/profile, tenant/exposure, and cohort under reviewed priority. Reject ambiguity and unknown host/path. Avoid dynamic arbitrary upstream URLs, DNS names, or client-controlled headers that create SSRF/open proxy behavior.

Consume discovery endpoints with identity, health/readiness, locality, zone/region, weights, and version/capability. Validate namespace/tenant/environment and use last-known-good policy during control-plane failure. Endpoint health does not prove application dependencies or semantic readiness.

Failover preserves data residency, tenant, version, consistency, capacity, and authorization. A healthy endpoint in the wrong region/contract may be worse than failure.

Canary/blue-green routing uses stable consumer/tenant/session keys when required, explicit capability compatibility, bounded cohorts, and observable assignment. Avoid retrying a request into a different semantic version after partial effect.

### Bound deadlines, timeouts, retries, and buffering

Propagate caller deadline where supported and reserve edge, network, upstream, and response margins. Gateway timeout cannot exceed caller usefulness; service observes cancellation and stops waste where safe.

Inventory retry layers: client, CDN/LB, gateway, mesh, service, SDK, queue. If two layers each allow one retry, maximum attempts can reach $(1+1)(1+1)=4$ before fan-out/hedges. Assign retry ownership or a shared budget.

Retry only safe/idempotent or idempotency-key-protected operations, on classified transient conditions, with bounded attempts/deadline/backoff/jitter and replayable request body. Never retry after ambiguous partial response/effect without contract support. Honor overload and `Retry-After` policy.

Limit header/body/decompression/buffering/connection/stream resources and stream with backpressure. A gateway that buffers a 10 GiB upload to enable retry creates a new failure mode.

### Enforce rates, quotas, and overload without confusing semantics

Separate abuse/network protection, concurrency/admission, rate smoothing, contractual quota, and billing/accounting. Each has different identity, consistency, accuracy, latency, failure, and communication requirements.

Key limits by trusted principal/application/tenant/operation/tier, not spoofable IP alone. Bound cardinality and protect hot tenants. Distributed approximate limiters trade strictness for availability; state the overshoot/undershoot and multi-region behavior.

Fail-open versus fail-closed is per risk: security/paid hard quota may fail closed; safety-critical read during limiter outage may use bounded local emergency budget. Never let one dependency outage turn the gateway into unlimited admission or total global denial by accident.

Return stable status/error, limit/reset/retry information where safe, and correlation. Services still load-shed based on real local saturation; gateway quotas cannot see every downstream bottleneck.

### Cache only under an explicit contract

Honor method/status/cache-control/validators/vary/auth semantics. Cache key includes normalized authority/path/query plus representation/version/profile, tenant/principal/authorization dimensions where required. Incorrect omission leaks data or mixes semantics.

Decide CDN/shared/private cache placement, TTL/staleness, invalidation, conditional revalidation, negative/error caching, request coalescing, and purge authorization. Do not cache authentication/authorization denials or personalized responses by default without proof.

Gateway caches can protect origins but hide deployments and serve stale policy/data. Observe hits/misses/age/version/tenant safely and test rollback/deprecation. Purge/namespace old and new contract representations during evolution.

Caching does not eliminate service correctness: origin still enforces authorization and returns correct cache metadata.

### Transform sparingly and transparently

Safe transformations include controlled header normalization, correlation, compression negotiation, and governed compatibility adapters. Every mutation has owner, contract, version, test, telemetry, failure behavior, and removal condition.

Avoid arbitrary JSON rewriting, field defaults, error reshaping, or business enrichment in generic policies. It can bypass signatures, validation, authorization, privacy, SDK assumptions, and origin observability.

If edge response/error normalization is required, distinguish gateway-generated from upstream response while preserving public contract. Do not turn every upstream failure into generic 500.

Request/response body inspection has latency, memory, encryption, privacy, and size limits. Schema validation at edge is defense/feedback, not proof of service behavior; maintain exact contract/dialect alignment.

### Make failures attributable

Distinguish DNS/connection/TLS/protocol/authn/policy/rate/overload/route/discovery/upstream connect/timeout/reset/invalid response and gateway internal/config failures. Stable public errors need not expose topology, but operators require attributable cause.

RFC 9209 defines `Proxy-Status` for intermediaries to convey proxy information, especially generated errors. Apply privacy/security policy; do not expose internal hostnames or sensitive detail indiscriminately.

Use correct 502/503/504 distinctions according to actual contract and retry semantics. Preserve upstream status when safe; record whether the gateway generated or forwarded it.

Maintain incident controls: traffic drain, route disable, quota/load-shed, credential/key revocation, config rollback, safe static response, and escalation. Kill switches are scoped, authenticated, audited, tested, and cannot silently persist.

### Observe the edge without creating a surveillance surface

Correlate request/client/gateway/upstream spans without treating trace ID as identity. OpenTelemetry HTTP conventions define client/server and reverse-proxy examples and retry/redirect semantics; use stable route templates and bounded attributes.

Record trusted consumer/principal reference where lawful, route/operation, requested/resolved version/profile, gateway/backend, policy/config revision, outcome/source, status/stable error, attempts, rate/cache decision, latency phases, sizes/cost buckets, region, and trace correlation. Separate logical operation, edge request, and upstream attempts.

Never log tokens, credentials, cookies, unrestricted headers, raw sensitive URLs/query/body, or unnecessary personal identifiers. Allowlist/redact at collection; control access, retention, tenant isolation, export, and audit.

Measure edge SLO and end-to-end consumer outcome separately. A gateway can be healthy while origin behavior fails, or report high latency caused entirely before/after it.

### Engineer the configuration and control plane

Treat routes, certificates, identity issuers/keys, policy, quotas, transforms, clusters, and telemetry as versioned reviewed code/artifacts with schema, ownership, references, provenance, and environment promotion.

Validate syntax and semantic invariants: no ambiguous/shadowed routes, bypass, unsafe wildcard, duplicate policy, missing backend/secret, tenant crossover, incompatible protocol, retry on unsafe operation, unbounded timeout/body, cache without auth dimension, or forbidden transform.

Test offline plus ephemeral/integration traffic, diff rendered effective config, canary by gateway shard/tenant/route, observe, then expand. Keep atomic last-known-good rollback and compatibility across control/data-plane versions.

Control-plane push/pull failures, partial rollout, stale caches, clock/key skew, and split brain are expected. Data planes serve last-known-good within bounded expiry; high-risk revocation may require fail-safe behavior. Report config convergence and reject unknown/incompatible revisions.

### Design tenancy, availability, and capacity

Choose shared versus dedicated gateways/control planes from isolation, scale, compliance, customization, and cost. Shared systems need tenant-scoped admin/RBAC, quotas, secrets/certs, route namespaces, logs, policy, and blast-radius cells.

Avoid one global fleet/config/key/limiter dependency. Partition by region/exposure/risk/tenant where justified, with explicit failover and consistent ownership. Isolation also prevents noisy configuration or high cardinality from exhausting control plane.

Capacity models connections/streams/handshakes, request rate, concurrency, headers/body/buffering, TLS crypto, policy evaluation, auth/introspection, transformations, logging, upstream fan-out, and control-plane churn. Load test distributions and failure modes.

High availability includes DNS/LB, data planes, discovery, identity keys/introspection, limiter/cache, config, certificate/key, telemetry backpressure, and operator access. Degraded modes are designed, not improvised.

### Govern lifecycle and keep the gateway thin

Assign platform ownership for gateway capability/SLO/security/config tooling and API product/service ownership for routes/contracts/upstreams/consumer policy. Publish support boundaries, escalation, change/compatibility, and exception process.

Review gateway policies with API design/security/reliability. Temporary version routes, header aliases, adapters, exception allowlists, and consumer overrides have owner, scope, expiry, metrics, and migration task.

Deprecation/removal covers route, credential/audience/scope, certificate, transform, cache namespace, quota tier, upstream cluster, telemetry, docs/SDK, and consumer communication. Prove no dormant/failover/support/replay dependency.

Measure gateway value through reduced integration effort, consistent security/reliability, safe self-service, incident/blast-radius reduction, and policy lead time—not number of centralized features. If a rule requires domain data or frequent per-API branching, move it to an owned service/façade.

## Definitions and Notation

Let path hops be $h_0\ldots h_n$. Each applies transformation $f_i$ to message/context and produces an attributable outcome. Let $P,T,I,R,B,O$ denote protocol preservation, trust-context integrity, identity validity, safe routing, bounded resources/resilience, and observability; edge safety requires their applicable conjunction.

Let layer $i$ permit $r_i\ge0$ retries. Without fan-out/hedging, one logical operation can cause at most $A=\prod_i(r_i+1)$ attempts under the simplified bound. Let caller deadline be $D$ and edge/upstream/return/margin budgets $d_e,d_u,d_r,d_m$, requiring $d_e+d_u+d_r+d_m\le D$.

A **policy revision** is immutable effective configuration identity. A **trusted peer** is authenticated/authorized to assert the specific forwarded context, not merely located on an internal network. **Bypass** is a path reaching upstream without equivalent required controls.

## Mechanisms, Invariants, or Proof Structure

**Authority argument.** A gateway may know authenticated subject/scope and route, but not authoritative ownership/state of arbitrary domain object. Two requests with identical edge-visible claims can target objects owned by different tenants. Therefore gateway authentication/coarse policy cannot prove object authorization; the service must decide at the resource/effect boundary.

**Header-spoofing counterexample.** If gateway preserves inbound `X-User-Id` and service trusts it, an external client can assert another identity despite valid authentication. Strip-and-regenerate protected context plus authenticated downstream peer removes the untrusted assertion path.

**Retry multiplication.** With one client retry and one gateway retry, $A=(1+1)(1+1)=4$ upstream attempts can arise for one logical operation; adding a service retry doubles it to eight. Independent “small” retry policies therefore amplify load/effects multiplicatively and need one budget/owner.

**Cache-key counterexample.** Two tenants request the same URI but authorization yields different representations. A shared cache keyed only by URI can serve tenant A’s data to B. Therefore every representation/security-varying dimension must be in key/validation, or the response is not shared-cacheable.

Operational invariants are: edge/hops explicit; protocol parsing unambiguous; trusted headers stripped/derived/protected; external token audience scoped; services authorize domain objects/actions; routes allowlisted; retries/deadlines/limits end-to-end bounded; caches tenant/auth/version safe; generated failures attributable; telemetry minimized; config progressive/reversible; control-plane failure last-known-good; tenancy isolated; and temporary edge logic removed.

## Alternatives and Trade-Offs

Central gateway policy improves consistency and reduces repeated edge work but increases blast radius/latency and can bottleneck ownership. Per-service edge logic preserves autonomy but duplicates security and diverges. Centralize stable cross-cutting mechanisms; federate route/product policy with guardrails.

TLS termination enables routing/auth/inspection but exposes plaintext at the gateway. Passthrough preserves end-to-end encryption but limits L7 policy and client-identity translation. Use explicit trust requirements and re-encrypt/mTLS where terminating.

Gateway authentication reduces invalid traffic and centralizes issuer logic; service validation provides bypass/staleness defense. Both cost latency/complexity. Use derived audience-bound context and service trust verification rather than forwarding reusable bearer tokens everywhere.

Global exact rate limits enforce strict quota but add latency/consistency/outage coupling. Local/partitioned limits are resilient but overshoot. Choose from contractual/security consequence and document bounds/degraded mode.

Gateway retries hide transient failures but amplify load and duplicate effects. Client/service retries may know semantics better. Assign the layer with idempotency/deadline/body/effect knowledge and suppress redundant layers.

Body transformation/validation gives uniformity but adds buffering/privacy/coupling. Prefer contract enforcement and service-owned semantics; reserve edge mutation for small stable governed concerns.

## Failure Modes and Misconceptions

- “The gateway is the edge.” Real paths often contain several independently owned edges.
- “Internal headers are trusted.” Only authenticated eligible peers can assert specific context.
- “Gateway auth means service auth is unnecessary.” Object/action/state authority remains downstream.
- “Client IP identifies a consumer.” NAT, proxies, spoofing, mobility, and privacy defeat it.
- “HTTP proxying is transparent.” Parsing, headers, caching, retries, and transformations alter semantics.
- “A healthy endpoint is safe to route.” Version, tenant, region, capacity, and dependencies matter.
- “One retry is harmless.” Layered retries multiply.
- “POST can never retry.” Idempotency contract/body replay/effect knowledge determine safety.
- “Global quota should fail closed.” Degraded behavior depends on security/contract/safety consequence.
- “Cache by URL.” Auth, tenant, version, representation, and policy can vary.
- “502 is an origin error.” The intermediary can generate it; attribution matters.
- “Log every header for debugging.” Tokens/secrets/personal data make that unsafe.
- “Control plane is off the request path, so irrelevant.” Its stale/partial config shapes every request.
- “Gateway can host small business rules.” Exceptions accumulate into a privileged monolith.
- “Service mesh replaces gateway.” Internal and external trust/product responsibilities differ.
- “Temporary compatibility routes can stay.” Unowned legacy edge paths expand attack and test surface.

## Worked Examples

### Example 1

Client sends spoofed `X-Tenant-Id`. Gateway strips it, validates audience-bound token, derives tenant, signs minimal internal context, and service authorizes the requested object in that tenant.

### Example 2

Client and gateway each retry once. One logical call creates up to four upstream attempts; adding service retry would create eight. Gateway retry is disabled for the unsafe operation.

### Example 3

Two tenants request identical URI. Cache keyed only by URI leaks A’s representation to B. Policy makes response private or keys/validates trusted tenant and authorization dimensions.

### Example 4

Gateway timeout is 60 seconds while caller deadline is 10. Upstream works uselessly after client leaves. Budgets are reduced and cancellation propagated within the 10-second deadline.

### Example 5

A route uses client-supplied `X-Upstream-Host`, creating an open proxy/SSRF path. It is replaced with an allowlisted route-to-discovery mapping and authenticated tenant scope.

### Example 6

New gateway JSON normalizer and old service parse duplicate headers differently. Differential tests reveal ambiguity; edge rejects duplicate security-sensitive fields before rollout.

### Example 7

Limiter store fails. Paid write quota fails closed with stable retry guidance; critical read uses bounded local emergency budget. Both degraded modes are explicit and audited.

### Example 8

Gateway returns 504 after its upstream deadline and records `Proxy-Status` internally/safely, while a separate metric marks gateway-generated timeout rather than origin status.

### Example 9

Control plane is unavailable during config rollout. Data planes keep immutable last-known-good revision; new changes stop, convergence alerts fire, and traffic does not fall back to empty routes.

### Example 10

A two-year field-rename transform has no remaining consumers. Inventory and DR rehearsal confirm replacement; route/transform/flag/cache namespace/tests/metrics/docs are removed together.

## Cross-Program Connections

[Network Engineering](../../24-network-engineering/ROADMAP.md) supplies DNS, routing, load balancing, TLS, proxies, DDoS, connection behavior, packet/flow diagnostics, and network failure modes.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies trust boundaries, identity, token validation, authorization, secrets, SSRF, request smuggling, WAF/abuse, tenant isolation, audit, and key/certificate lifecycle.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies discovery, health, retries, deadlines, load shedding, partitions, replicated limiters/config, failure attribution, and recovery.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies gateway control planes, self-service routes/policies, tenancy, paved paths, policy-as-code, progressive config delivery, catalogs, SLOs, and support.

[Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies regional edges, managed load balancing/WAF/DDoS, certificates/keys, autoscaling, networking, availability cells, capacity, and cost.

## References

1. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
2. IETF, [RFC 7239: Forwarded HTTP Extension](https://www.rfc-editor.org/rfc/rfc7239.html).
3. IETF, [RFC 9209: The Proxy-Status HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9209.html).
4. IETF, [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750.html).
5. OpenTelemetry, [Semantic Conventions for HTTP Spans](https://opentelemetry.io/docs/specs/semconv/http/http-spans/).
6. OWASP, [OWASP API Security Top 10 — 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/).
7. Kubernetes SIG Network, [Gateway API](https://gateway-api.sigs.k8s.io/).

## Exercises

### Exercise 1

Create a responsibility/authority matrix for an internet API path containing CDN/WAF, cloud load balancer, API gateway, service mesh, identity provider, service, and database. Cover protocol, identity, authorization, routing, resilience, observability, config, and incidents.

### Exercise 2

Design protected authentication-context propagation when the gateway terminates OAuth bearer tokens and mTLS partners, services require tenant/object authorization, and direct internal/bypass traffic is possible.

### Exercise 3

A client permits two retries, gateway one, and service two. Compute the simplified maximum attempts. Redesign deadlines/retry/idempotency/overload ownership for a non-idempotent payment request.

### Exercise 4

Design gateway behavior for identity-key outage, global rate-limiter outage, discovery staleness, partial config rollout, origin overload, and telemetry backpressure. State fail-open/closed/last-known-good and evidence.

### Exercise 5

Audit a gateway that performs version routing, JSON field transforms, error rewriting, object authorization, cache, quota, retries, and canary release for 200 APIs. Decide what remains, moves, or becomes a separate owned façade, and plan safe migration.

## Answers to the Exercises

### Answer 1

CDN/WAF owns internet connection/DDoS/basic L7 abuse and cache only under contract; load balancer owns regional/fleet connection distribution and health; gateway owns client-facing protocol normalization/limits, external credential validation, protected context, allowlisted API route/version/cohort, coarse scope policy, contractual quota/admission, bounded cache/retry/deadline, edge errors/telemetry, and route policy lifecycle. Identity provider owns credential issuance, issuer/audience/key/revocation/introspection. Discovery/mesh own authenticated service endpoint membership, internal routing/mTLS and bounded service-to-service policy/telemetry, not public product authorization. Service owns domain parsing/semantics, action/object/property/tenant authorization, idempotency/effects, state, local load shedding, business errors/SLO. Database owns durable constraints/transactions/access. Platform owners run edge/mesh capabilities; API owner owns route/offer; security owns required controls; incident command owns response. For every hop specify config source, peer trust, mutation, timeout/retry/cache, generated failures, SLO, escalation, and bypass equivalence.

### Answer 2

At the first trusted gateway strip reserved identity/tenant/scope/client-cert fields. For bearer tokens validate scheme/signature, issuer, route-specific audience, algorithm/key, time, required claims and revocation policy; never log or forward reusable token unless required. For mTLS validate chain/name/time/revocation and map certificate identity to registered partner/tenant. Derive minimal subject/client/tenant/scopes/auth method/time/strength/context version/expiry/audience; send over gateway-to-service mTLS/workload identity and sign/audience-bind the context if intermediaries require it. Services accept it only from eligible gateway identities, verify integrity/expiry/audience, and then authorize action/object/property/current tenant state. Direct paths require equivalent authentication/context or are denied by network/service policy. Propagate end-user identity separately from workload caller, prevent elevation by downstream hops, rotate keys with overlap, audit derivation, test spoof/duplicate/replay/wrong audience/bypass/stale keys, and provide safe degraded behavior.

### Answer 3

The simplified bound is $(2+1)(1+1)(2+1)=3\times2\times3=18$ upstream service attempts for one logical operation before hedging/fan-out. For payment, require a client-scoped idempotency key with durable request fingerprint, atomic effect/result/deduplication, conflict and retention semantics. Prefer client retry only after ambiguous failure within an end-to-end deadline; gateway does not retry the unsafe body unless the idempotency contract and replayability are proven; service retries only internal transient dependencies under the remaining shared budget, not the whole payment effect. Propagate deadline/cancellation, classify connection-before-send versus ambiguous post-send, cap attempts/backoff/jitter, honor overload/Retry-After, load shed early, and expose outcome lookup/reconciliation. Count logical payment, transport attempts, dedupe hits, and effects separately; test response loss after commit, concurrency, gateway failover, limiter/origin overload, and retry storms.

### Answer 4

Identity-key discovery uses verified cached keys only within bounded freshness/rotation; unknown key/authentication normally fails closed, while known current sessions follow explicit policy—never skip signature/audience. Limiter outage follows per-policy consequence: hard paid/security writes fail closed or use tiny signed local allocation; critical reads may use bounded local emergency capacity with alerts/audit. Discovery uses authenticated last-known-good endpoints within expiry, removes definitively unhealthy targets, and never routes arbitrary/wrong-region/tenant/version endpoints; exhaustion yields attributable unavailable. Partial config rollout keeps immutable compatible revisions, canaries by cell, reports convergence, and atomically rolls back; no empty/default permissive config. Origin overload disables retries, sheds by priority/concurrency, honors backpressure, preserves capacity for health/control, and returns stable retry guidance. Telemetry backpressure samples/drops boundedly without blocking traffic or secrets spilling to fallback; retain critical security/audit separately and expose drop health. Test each degraded mode, expiry transition, recovery/reconciliation, and correlated multi-dependency failure.

### Answer 5

Keep stable cross-cutting version/profile routing, strict small compatibility transforms with expiry, contract-safe edge-error attribution, cache only with complete auth/tenant/version keys, trusted quota/admission, bounded safe retries, and canary routing. Move object/action/property authorization to services; gateway retains external auth/coarse route scope. Move domain JSON transforms and business error mapping to canonical service adapter or create a separately owned façade/BFF with contract/SLO/security/lifecycle; avoid generic policy code. Services own idempotency/effects and local overload. Inventory all 200 APIs, policy owners, consumers, bypass, dependencies, versions, cache/retry/auth semantics, incidents, and temporary logic. Define target matrix; deploy service/facade behavior and protected context first, shadow/differential test without effects, migrate routes by low-risk cohort with semantic/security/cache/load evidence, and keep rollback. Remove gateway branches only after per-consumer outcomes and horizon evidence, update docs/SDK/catalog/support, delete stale flags/routes/transforms/cache namespaces/scopes/tests/metrics, and retain audited decisions. Partition control/data-plane blast radius and establish platform versus product decision rights.
