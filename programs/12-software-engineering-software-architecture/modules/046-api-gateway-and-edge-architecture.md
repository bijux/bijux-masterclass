---
module_id: SARCH-046
program: Software Engineering: Software Architecture
level: 1
module_number: 46
title: API Gateway and Edge Architecture
status: complete
last_verified: 2026-09-06
---

# API Gateway and Edge Architecture

## One-Page Review

### Governing question

How should an externally reachable edge mediate transport, identity, routing, admission, compatibility, and observation without becoming an unbounded bottleneck, a security bypass, or a hidden owner of domain policy?

### Essential definitions

- The **edge** is the controlled boundary where traffic crosses between trust, ownership, or network domains; it is a logical boundary, not necessarily one machine.
- A **reverse proxy** receives requests on behalf of origins; a **load balancer** selects destinations; an **API gateway** applies governed API mediation; these roles overlap but are not synonyms.
- A **web application firewall** detects or blocks selected application-layer threats; it does not prove an application is secure.
- A **backend for frontend (BFF)** presents a client-specific API while preserving domain authority behind it.
- **transport termination** ends a protected connection at an intermediary, making that intermediary part of the plaintext trust boundary.
- **authentication** establishes an identity claim; **authorization** decides whether that principal may perform an operation on a resource.
- **end-principal identity** identifies the user or machine on whose behalf work occurs; **workload identity** identifies the calling component.
- **admission control** decides whether work may enter; **rate limiting** bounds requests over time; a **quota** bounds consumption over a longer scope.
- **route ownership** assigns who may map a public contract to a target; **bypass resistance** ensures equivalent access cannot evade edge controls.
- **policy gravity** is the tendency for convenient centralized mediation to accumulate unrelated business decisions and coupling.

### Central model, mechanism, or theorem

Model the edge path as listener $L$, connection and transport context $T$, authenticated client principal $U$, edge workload $G$, route $R$, origin workload $O$, business resource $X$, and end-to-end operation $Q$. Evidence and authorization must bind the right identities to the right hop; a forwarding header supplied by an untrusted client is not that binding.

If peak admitted rate is $\lambda$ requests/s, one instance sustains $c$ requests/s under the chosen utilization target, and $r$ instances must remain unavailable, a necessary instance count is

$$
n\ge \left\lceil\frac{\lambda}{c}\right\rceil+r
$$

only when reserve instances are interchangeable and failures do not remove a correlated zone or dependency. Zone-loss planning instead evaluates remaining placement capacity explicitly.

### Critical invariants

- every public listener, name, certificate, route, origin, and owner is inventoried;
- untrusted forwarding, identity, routing, and size metadata is stripped or overwritten at the trust boundary;
- transport termination, re-encryption, origin authentication, and plaintext exposure are explicit;
- workload and end-principal identity remain distinct, integrity-protected, audience-bound, scoped, and short-lived;
- the resource owner authorizes business action; the edge enforces only coherent shared policy;
- routing, transformation, validation, caching, retry, timeout, and error semantics are versioned contracts;
- request size, header size, connection rate, concurrency, body rate, decompression, retries, and downstream amplification are bounded;
- admission considers tenant, principal, operation cost, origin capacity, and emergency reserve rather than IP address alone;
- no alternate origin path silently bypasses equivalent authentication, authorization, admission, or observation;
- edge configuration has ownership, review, validation, staged rollout, rollback, and last-known-good behavior;
- telemetry distinguishes client, edge, origin, dependency, and business outcomes without leaking credentials or sensitive payloads;
- overload, malformed traffic, ambiguous protocol parsing, dependency failure, credential rotation, and regional loss are tested.

### Common failures

Common failures include treating the edge as a security perimeter that makes internal authorization unnecessary; trusting client-supplied `Forwarded` or identity headers; terminating encryption without protecting the origin hop; routing by unvalidated host data; retrying mutations at the gateway; using one global rate limit for unequal operations; allowing unbounded uploads or decompression; caching personalized responses under incomplete keys; hiding breaking transformations; placing pricing or eligibility policy in gateway rules; exposing origins directly; coupling every deployment to one shared configuration; and declaring success from gateway 2xx rates while users fail downstream.

### Compact example

Peak traffic is 24,000 requests/s. One edge instance sustains 1,800 requests/s, but the operating target is 60%, so planned capacity is 1,080 requests/s. The lower bound is $\lceil24{,}000/1{,}080\rceil=23$ instances before zone loss, rollout, uneven traffic, TLS handshakes, large requests, or downstream cost. Placement must then prove that the remaining zones can carry the peak and that origin admission prevents the edge from forwarding more work than origins can safely serve.

### Connections

[SARCH-036](036-client-server-architecture.md) defines client and server roles; [SARCH-043](043-synchronous-request-response-integration.md) supplies deadline, retry, and ambiguous-outcome reasoning; [SARCH-044](044-asynchronous-messaging-integration.md) supplies pending alternatives. [SARCH-047](../ROADMAP.md) next examines cache boundaries. API Engineering owns protocol and gateway implementation depth; Security Engineering owns threat and authorization mechanisms.

## Governing Question

An edge concentrates unavoidable concerns: public naming, transport security, request parsing, origin selection, client authentication, abuse resistance, compatibility, and telemetry. Centralization can make these controls consistent and reduce duplicated implementation. It also makes a high-leverage failure and attack boundary.

The architectural task is to decide which policies are genuinely shared, preserve domain ownership, bound work before scarce resources are consumed, and maintain end-to-end identity and semantics across mediation. A gateway is useful infrastructure, not a substitute for sound service boundaries.

## Why This Matters

An exposed service is not reached through an abstract arrow. Connections arrive with protocol ambiguity, large bodies, slow senders, spoofed metadata, revoked credentials, uneven tenants, and bursts. The edge may terminate encryption, translate versions, select a region, retry, cache, or aggregate. Every action changes trust or semantics.

A gateway outage can remove an entire product even while origins are healthy. A bad route can send one tenant to another. An eager retry can duplicate a payment. A permissive header rule can turn an external string into administrator identity. Conversely, disciplined edge architecture creates a small, observable, governable entrance and lets domain services concentrate on owned behavior.

## Prerequisites and Retrieval

Retrieve client, server, origin, proxy, route, listener, name resolution, connection, TLS, certificate, principal, credential, token, audience, scope, authentication, authorization, request, response, header, body, cache, retry, deadline, rate, quota, concurrency, queue, overload, availability, configuration, deployment, and telemetry.

From SARCH-017 retrieve interoperability; SARCH-018 supplies evidence; SARCH-024 supplies runtime views; SARCH-036 supplies client-server structure; SARCH-041 supplies authority; and SARCH-043 supplies end-to-end deadlines, operation identity, admission, and failure semantics.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish edge, reverse proxy, load balancer, gateway, WAF, CDN, and BFF responsibilities;
2. draw trust, transport, identity, routing, and authority boundaries across every hop;
3. design secure forwarding metadata and origin authentication;
4. place shared technical policy at the edge without moving domain authority there;
5. bound connections, requests, bodies, decompression, retries, fan-out, and tenant work;
6. design cost-aware admission, rate limits, quotas, and overload behavior;
7. evolve routes, transformations, and contracts under mixed versions and rollback;
8. prevent bypass and control configuration as production code;
9. size and place the edge for failure, rollout, and origin capacity;
10. observe and test edge, origin, and business outcomes separately.

## Core Exposition

**Define the edge by trust transition.** The internet-facing listener is an obvious edge, but partner, mobile, administrative, regional, and internal platform boundaries may need different edges. Do not assume one gateway tier fits every audience and consequence.

Inventory public names, addresses, certificates, listeners, protocols, routes, origin pools, owners, and data classes. Unknown legacy listeners and direct origins defeat central policy. Treat shadow ingress as an architectural defect, not merely an asset-management issue.

**Separate adjacent roles.** A reverse proxy represents origins. A load balancer distributes traffic. A gateway validates and mediates API contracts. A WAF applies selected threat rules. A CDN serves or forwards content near clients. A BFF shapes an API for one client experience. A service mesh mediates service-to-service traffic.

One product may implement several roles, but the design should still name them. Otherwise a caching change can accidentally alter authentication, a route rule can acquire domain logic, or an operational owner can receive authority it should not have.

**Draw transport termination explicitly.** TLS protects a connection between two endpoints. If the edge terminates it, plaintext exists inside the edge process and perhaps in memory, logs, traces, or plugins. The origin hop needs its own authenticated protection when the threat model requires it.

Validate the intended server name and certificate on each hop. Define certificate issuance, rotation, revocation response, expiry monitoring, and emergency replacement. “Encrypted internally” is incomplete without authenticating the intended peer and protecting keys.

**Distinguish workload and end principal.** The edge is a workload calling an origin, while a user or client workload may be the end principal. Origins often need both: who is making the hop and on whose behalf.

Strip untrusted identity headers. Authenticate the external credential, then mint or forward integrity-protected context with constrained audience, scope, lifetime, issuer, and delegation semantics. Origins authenticate the gateway workload and validate end-principal context; they do not accept arbitrary headers from any internal caller.

NIST SP 800-207 rejects implicit trust based solely on network location [1]. That principle applies after an edge: an internal address is not business authorization.

**Keep resource authorization with the owner.** The edge can reject obviously invalid or unauthorized categories and enforce shared scopes. Only the domain owner knows current resource ownership, state, consent, segregation, or safety policy.

Putting every authorization decision at the edge creates stale replicas or gateway callbacks and lets direct paths bypass policy. Let the origin decide `may principal U transfer account X now?`; let the edge ensure authenticated context, coarse scope, route, and admission.

**Route by governed contract.** A route maps listener, host, method or operation, path, version, audience, and policy to owned origins. Resolve ambiguities deterministically. Reject unknown host or route rather than falling through to a default sensitive origin.

Avoid routing on client-controlled headers unless their trust and validation are explicit. Normalize cautiously: two components that parse path, length, transfer encoding, or header syntax differently can disagree about request boundaries and enable request smuggling. Use one strict supported interpretation and reject ambiguity.

**Control forwarding metadata.** RFC 7239 defines standardized forwarded information [2], but syntax does not make values trustworthy. Remove incoming values at the outer trusted boundary or retain them only in a clearly untrusted field. Append observations from trusted hops under a documented chain.

Client IP is fragile identity: shared networks, proxies, mobile changes, and attacker-controlled forwarding undermine it. It may support risk signals and coarse abuse controls, not replace authenticated principal or tenant identity.

**Bound work before expensive processing.** Limit connection attempts, concurrent connections, handshake work, header count and bytes, request line, body bytes, decompressed bytes, body rate, total duration, and idle time. Stream or spool large bodies under quotas rather than buffering without limit.

Compressed input needs a decompressed-size and ratio bound. Schema validation itself consumes CPU and memory; cheap framing and size checks should precede expensive parsing. Different operations require different limits.

**Design admission from resource cost.** A request count treats a cached read, large search, upload, and report generation as equal. Admission should combine tenant and principal fairness, operation class, estimated cost, concurrency, origin saturation, and emergency priority.

A token bucket with rate $r$ and capacity $b$ allows bounded bursts while limiting sustained admission. It is a policy mechanism, not a promise of origin capacity. Coordinate limits across instances or accept and document approximation. Define response semantics, retry guidance, and whether rejected work is safe to retry.

**Protect origins from amplification.** One accepted edge request can fan out to many origin calls, database queries, or transformations. Admission uses downstream work, not just incoming rate. An aggregator that accepts 10,000 requests/s and makes six required calls can produce 60,000 origin calls/s before retries.

Bound fan-out and call depth. Prefer coarse owned operations or precomputed views. A gateway should not become an uncontrolled distributed join merely because it can reach every service.

**Propagate deadlines and coordinate retries.** Begin with the client's latest useful result, reserve edge work, and propagate remaining deadline. Do not reset a full timeout at the gateway. Stop origin work when the result is no longer useful, subject to cleanup and correctness.

Retry only contract-declared safe transient failures under one coordinated policy. A gateway cannot infer mutation idempotency from method name alone. Preserve stable operation identity and never convert an unknown payment outcome into a new request.

**Use transformation sparingly.** Gateways can translate external and internal representations, redact fields, or bridge versions. Every transformation becomes a contract with tests, ownership, latency, failure, and rollback. Lossy translation may prevent round trips or signatures.

Prefer additive stable public contracts and place domain interpretation with its owner. A BFF may compose presentation-friendly results, but pricing, eligibility, and safety decisions remain authoritative services. Track policy gravity: rule count, change owners, release coupling, dependencies, and incident share.

**Cache only under complete variation.** Edge caching can reduce latency and origin load. Define method, status, freshness, validators, tenant, identity, authorization, locale, encoding, and every response-varying input. A shared cache key missing authorization context can disclose data.

Do not cache revocation, inventory, or personalized decisions beyond their allowed freshness. Invalidating at the edge does not invalidate downstream or client caches automatically. SARCH-047 treats cache boundaries in depth.

**Design errors as public semantics.** Preserve a stable distinction among malformed, unauthenticated, unauthorized, absent, conflict, precondition, rate limit, overload, unavailable origin, deadline, and internal failure. RFC 9457 provides a standard problem-details shape for HTTP APIs [3], but the domain still owns error meaning.

Do not leak stack traces, internal routes, credentials, or tenant data. Include a safe correlation identity and support path. A gateway-generated error must be distinguishable in telemetry from an origin rejection without forcing that internal distinction into unstable public detail.

**Control cross-origin and browser behavior deliberately.** Browser origin policy, preflight, cookies, redirects, and credentials create a different edge threat surface from machine APIs. Allow only intended origins, methods, headers, and credential combinations. Do not reflect arbitrary origins with credentials.

Cookie scope, same-site behavior, CSRF defense, token storage, and redirect validation require a coherent client model. A gateway header toggle cannot compensate for unsafe application flows.

**Treat configuration as executable production behavior.** Route and policy changes can expose data or remove a product instantly. Keep configuration versioned, reviewed, statically validated, tested against examples and forbidden cases, staged through limited traffic, observed, and rollback-capable.

Separate control plane from request-serving data plane. A control-plane outage should not erase last-known-good routes. Reject invalid or partial configuration atomically. Record who changed which listener, route, certificate, identity rule, or limit and why.

**Design for failure domains.** Capacity planning includes normal peak, zone loss, rollout, certificate handshake bursts, uneven tenant distribution, large bodies, WAF work, telemetry, and dependency failure. Spread independent instances across failure domains and prove remaining path capacity.

An edge can be redundant while sharing one DNS control, certificate authority, configuration service, identity provider, network path, or origin dependency. Availability multiplication assuming independence is usually optimistic unless the architecture establishes that independence.

**Coordinate edge and origin overload.** If an origin sheds load, the edge should not retry aggressively or route all traffic to another saturated region. Honor explicit pushback, reduce concurrency, and preserve administrative and recovery capacity. Fail optional features before critical actions.

Queues at the edge must be bounded by deadlines and memory. A long queue makes a healthy origin receive expired work. Early stable rejection can be safer than apparent acceptance followed by timeout.

**Prevent bypass.** Origins can restrict network paths, require gateway workload identity, or enforce equivalent policy for authorized alternate paths. Health, administration, metrics, and debug endpoints need their own exposure model. Do not publish them accidentally under wildcard routes.

Emergency bypass may be necessary, but it must be narrow, time-bound, strongly authenticated, observed, tested, and revoked. A permanent undocumented bypass is not resilience.

**Minimize and protect telemetry.** Record listener, route, version, client class, authenticated subject pseudonym where appropriate, workload identity, origin, status class, phase latency, size, admission result, retry count, and saturation. Separate transport, gateway, origin, and user outcome.

Never log bearer credentials, session cookies, raw secrets, or unrestricted bodies. Query strings and paths can contain sensitive data. Sampling must retain security and failure evidence without pretending a sampled trace is a ledger.

**Test adversarial and failure paths.** Test malformed framing, ambiguous lengths, oversized and slowly delivered bodies, decompression bombs, duplicated headers, path normalization, invalid host, spoofed forwarding identity, expired and wrong-audience credentials, tenant mixing, cache variation, and route shadowing.

Test origin slowness, response loss, retry ambiguity, overload, partial zone failure, configuration rejection, control-plane outage, certificate rotation, identity-key rotation, staged rollout, rollback, DNS change, and direct-origin attempts. Verify business outcomes and resource recovery.

**Know when to split edges.** Public consumer, partner, internal administrative, streaming, and bulk-upload traffic may need different identity, limits, data handling, availability, and ownership. Separate gateways or listener classes can reduce blast radius and policy conflict.

Do not fragment without reason: every extra edge adds certificates, routing, observation, and operations. Split by durable trust, workload, consequence, or ownership boundary—not team fashion.

## Definitions and Notation

Let request operation $Q$ enter listener $L$ under transport context $T$. External end principal is $U$; edge workload is $G$; selected route is $R$; origin workload is $O$; protected business resource is $X$. Authentication relations and authorization decisions name their issuer, audience, scope, and hop.

Let admitted arrival rate be $\lambda$, planned sustainable per-instance capacity be $c$, and number of available instances be $n$. Necessary aggregate condition is $nc\ge\lambda$. If physical instance peak is $p$ and target utilization is $u$, then $c=up$ as a planning constraint, not a measured guarantee.

For token bucket capacity $b$, refill rate $r$, and offered rate $a>r$, initial-full burst exhaustion time is $b/(a-r)$ under the simplified constant-rate model. Distributed enforcement, request cost, clock, and concurrency require additional mechanisms.

Downstream amplification $A(Q)$ is total origin work caused by one accepted request, including retries and fan-out. Edge admission must keep $\lambda E[A(Q)]$ and adverse high-cost classes within origin capacity.

## Mechanisms, Invariants, or Proof Structure

**Inventory invariant.** Every reachable listener, route, origin, certificate, alternate path, and owner belongs to one governed inventory; unknown or default exposure is rejected.

**Identity invariant.** Client-controlled metadata never becomes trusted identity without authentication and integrity protection. Workload, end principal, tenant, audience, scope, and delegation remain distinct.

**Authority invariant.** Shared transport and coarse access policy may be centralized, but the resource owner retains current domain authorization and decision semantics.

**Parsing invariant.** Every trusted hop agrees on one bounded request interpretation or rejects the request; ambiguous framing, normalization, and routing never pass downstream.

**Capacity invariant.** Connections, handshakes, headers, compressed and decompressed bodies, rates, quotas, concurrency, queues, retries, fan-out, and per-principal work are bounded.

**Deadline invariant.** One end-to-end deadline is propagated; edge queues, calls, and retries do not reset useful time.

**Bypass invariant.** Every authorized path to an origin supplies equivalent identity, authorization, admission, and observation, or is a separately governed exception.

**Configuration invariant.** Data plane serves one validated coherent configuration version and retains a tested last-known-good version through control-plane failure.

**Compatibility invariant.** Route, public contract, transformation, error, identity, and origin versions support mixed deployment and rollback under tests.

**Evidence invariant.** Client acceptance, edge status, origin status, committed business effect, and user outcome are distinct observations.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Direct origin exposure | fewer hops and simpler latency | duplicated controls and larger attack surface | origin independently satisfies full edge contract |
| Shared API gateway | consistent mediation and inventory | bottleneck, blast radius, policy gravity | audiences share coherent technical policy |
| Gateway per trust domain | isolated policy and failure | more operations and configuration | audiences differ materially in trust or consequence |
| Backend for frontend | client-specific composition | duplicated logic and client coupling | client experiences have stable distinct needs |
| Edge authentication | early rejection and shared mechanism | token and key concentration | origins also validate relevant authorization context |
| Origin-only domain authorization | current authoritative decisions | more origin work | resource state determines permission |
| Central rate limit | coordinated tenant control | dependency and latency | exact shared quotas justify coordination |
| Local approximate limit | fast and resilient | uneven global enforcement | bounded approximation is acceptable |
| Edge caching | lower latency and origin load | leakage and staleness risk | complete variation and freshness are defined |
| Edge transformation | compatibility bridge | hidden semantics and rollback cost | bounded owned transition needs it |
| Regional active edges | latency and failure isolation | routing and state complexity | remaining regions and origins can carry failover |

## Failure Modes and Misconceptions

1. **“The gateway is the security boundary.”** Resource owners still authenticate context and authorize actions.
2. **“Internal traffic is trusted.”** Location does not establish principal or permission.
3. **“TLS termination secures the whole path.”** The origin hop and intermediary plaintext remain.
4. **“Forwarded headers identify the client.”** Untrusted clients can supply them.
5. **“A WAF makes vulnerable code safe.”** It covers selected detectable patterns only.
6. **“One request has one unit of cost.”** Bodies, fan-out, and operations differ.
7. **“Rate limiting prevents overload.”** Concurrency, queueing, retries, and downstream work remain.
8. **“Gateway retries are transparent.”** They change load and can duplicate effects.
9. **“A 2xx proves the business outcome.”** It proves only the responding contract stage.
10. **“A default route improves availability.”** It can expose the wrong origin or tenant.
11. **“Edge transformation is free compatibility.”** Meaning and ownership can drift.
12. **“Caching authenticated traffic is safe by default.”** Variation errors can disclose data.
13. **“Redundant instances imply an independent edge.”** Control and dependencies can be shared.
14. **“Configuration is not code.”** It executes routing and security behavior.
15. **“Private origins cannot be bypassed.”** alternate paths, debug listeners, and credentials may exist.
16. **“Gateway metrics equal user reliability.”** Origin and business failures can be hidden.

## Worked Examples

### Example 1

**Situation.** Peak rate is 18,000 requests/s. Each instance peaks at 1,500/s, and target utilization is 65%. The edge spans three zones.

**Reasoning.** Planned capacity per instance is $1{,}500\times0.65=975$/s. The no-failure lower bound is $\lceil18{,}000/975\rceil=19$. Placing ten per zone gives 30 instances; loss of one zone leaves 20 and planned capacity 19,500/s. This still needs tests for skew, handshake bursts, shared dependencies, and origin capacity.

**Conclusion.** Zone-loss capacity must be evaluated from remaining placement, not an arbitrary reserve count.

### Example 2

**Situation.** A client sends `X-User: administrator` through a gateway that appends rather than removes identity headers.

**Reasoning.** Downstream parsers may select the attacker's value. The outer trusted edge strips all untrusted identity fields, authenticates the credential, creates integrity-protected audience-bound context, and records the client claim separately for forensics. Origin authenticates gateway workload and authorizes the represented principal on the resource.

**Conclusion.** Forwarded identity begins at a trusted authenticator, not at the client's header text.

### Example 3

**Situation.** A tenant has token bucket rate 600/s and capacity 3,000 but offers 1,800/s from a full bucket.

**Reasoning.** Net depletion is $1{,}800-600=1{,}200$ tokens/s, so simplified exhaustion time is $3{,}000/1{,}200=2.5$ seconds. Thereafter about 600/s are admitted if request cost is equal. Distributed instances need coordinated or explicitly approximate accounting, and concurrency limits still protect slow work.

**Conclusion.** A burst bucket controls one rate dimension; it does not replace cost and concurrency admission.

### Example 4

**Situation.** A gateway aggregator accepts 10,000 page requests/s and makes six required origin calls per request.

**Reasoning.** Baseline demand is 60,000 origin calls/s before retries, authentication lookups, and cache misses. Optional panels become soft, stable reads move to a correctly varied cache or projection, and a coarse owner operation replaces chatty calls. Admission tracks downstream work and origin saturation.

**Conclusion.** Edge request rate can hide dangerous downstream amplification.

### Example 5

**Situation.** A payment origin times out after the gateway sent a mutation, and the gateway retries with a new request ID.

**Reasoning.** The first payment may have committed. A new identity can double-charge. Gateway preserves the client's stable payment operation ID, retries only if the payment contract permits identical attempts, propagates the remaining deadline, and otherwise returns an unknown or pending outcome with authoritative inquiry.

**Conclusion.** Gateway convenience cannot override effect identity and ambiguous-outcome semantics.

### Example 6

**Situation.** A shared cache keys account responses only by path while authorization varies by user and tenant.

**Reasoning.** One user's response can be served to another. Disable shared caching until the contract defines tenant, principal or authorization class, representation, locale, encoding, version, and freshness variation. Sensitive resource decisions may remain uncacheable even with a complete technical key.

**Conclusion.** Cache correctness depends on every response-varying authority input.

### Example 7

**Situation.** A route rollout changes 5% of traffic to a new origin, but health checks only test TCP connect.

**Reasoning.** Validate configuration offline, exercise authenticated contract probes, then compare status classes, phase latency, authorization failures, business outcomes, and origin saturation for the limited route. Abort automatically on bounded indicators and retain last-known-good configuration if the control plane fails.

**Conclusion.** Safe route rollout observes contract and business behavior, not mere process reachability.

### Example 8

**Situation.** An upload endpoint permits 50 MB compressed bodies with no expanded-size limit.

**Reasoning.** A small compressed object can consume enormous memory or CPU. Bound compressed bytes, expanded bytes, ratio, stream rate, total duration, parser depth, fields, and temporary storage. Authenticate and admit before expensive work; parse in a constrained component; clean partial storage after failure.

**Conclusion.** Input limits cover resource expansion and time, not only wire bytes.

### Example 9

**Situation.** Origins are private, but a maintenance listener accepts the same API with a shared static credential.

**Reasoning.** The listener bypasses normal identity, tenant limits, and telemetry. Remove it or isolate it under a separate administrative contract with workload and human authentication, narrow operations, network restriction, approval, time-bound access, audit, and tests. Origins reject public-style calls lacking authorized path identity.

**Conclusion.** Bypass resistance includes maintenance and emergency paths, not only public DNS.

### Example 10

**Situation.** A regional healthcare gateway loses its identity provider while emergency clinicians need patient access.

**Reasoning.** The design does not fail open for arbitrary users. A separately governed emergency mode uses pre-provisioned strongly protected identities, narrow clinical scope, short offline validity, local resource authorization where possible, prominent break-glass reason, immutable audit, rate and export limits, and post-recovery review. Medication and consent rules remain with clinical authorities.

**Conclusion.** Emergency availability requires constrained delegated authority and evidence, not removal of authorization.

## Cross-Program Connections

- **API and Service Engineering:** owns HTTP and RPC semantics, schemas, gateway configuration, authentication interfaces, errors, and contract tests in depth.
- **Network Engineering:** owns DNS, routing, transport, congestion, TLS paths, load balancing, and address behavior.
- **Security Engineering:** owns threat modeling, credentials, tokens, authorization, WAF limits, key lifecycle, abuse resistance, and audit.
- **Software Delivery and Reliability Engineering:** owns SLOs, capacity, overload, observability, rollout, incident response, and disaster recovery.
- **Platform Engineering:** owns reusable ingress, certificates, identity bootstrap, policy distribution, telemetry, and safe self-service boundaries.
- **Distributed Systems Engineering:** owns partial failure, retries, deadlines, regional routing, configuration distribution, and consistency.
- **Software Engineering Patterns:** proxy, facade, adapter, decorator, and chain-of-responsibility mechanics illuminate gateway internals without deciding architecture.
- **Data Architecture Engineering:** classification, residency, minimization, lineage, and tenant boundaries constrain edge data handling.

## References

1. NIST, *SP 800-207: Zero Trust Architecture*, August 2020. <https://csrc.nist.gov/pubs/sp/800/207/final>
2. R. Petersson and M. Nilsson, *RFC 7239: Forwarded HTTP Extension*, IETF, June 2014. <https://www.rfc-editor.org/rfc/rfc7239>
3. S. Dalal, M. Nottingham, and E. Wilde, *RFC 9457: Problem Details for HTTP APIs*, IETF, July 2023. <https://www.rfc-editor.org/rfc/rfc9457>
4. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9110: HTTP Semantics*, IETF, June 2022. <https://www.rfc-editor.org/rfc/rfc9110>
5. E. Rescorla, *RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3*, IETF, August 2018. <https://www.rfc-editor.org/rfc/rfc8446>
6. T. Lodderstedt, J. Bradley, A. Labunets, and D. Fett, *RFC 9700: Best Current Practice for OAuth 2.0 Security*, IETF, January 2025. <https://www.rfc-editor.org/rfc/rfc9700>
7. OWASP Foundation, *OWASP API Security Top 10 — 2023*. <https://owasp.org/API-Security/editions/2023/en/0x11-t10/>
8. Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 2nd ed., Pragmatic Bookshelf, 2018.

## Exercises

### Exercise 1

Define edge, reverse proxy, load balancer, API gateway, WAF, BFF, transport termination, end-principal identity, workload identity, admission control, rate limit, quota, route ownership, bypass resistance, and policy gravity. Explain why these roles may coexist without becoming synonyms.

### Exercise 2

Peak traffic is 32,000 requests/s. Each instance peaks at 2,000/s and target utilization is 60%. Compute the no-failure lower bound. For equal placement across three zones and tolerance of one complete zone loss, compute the minimum integer instances per zone and total. Compute normal raw-peak utilization and state limitations.

### Exercise 3

Design the identity and authorization path from a mobile user through an internet gateway to an account service. Cover TLS termination and re-encryption, certificate validation, untrusted header sanitation, user and gateway identities, token audience and scope, resource authorization, logging, rotation, and bypass prevention.

### Exercise 4

Compare direct origin exposure, one shared gateway, gateways per trust domain, and BFFs for a public mobile app, business partners, internal operators, and bulk uploads. Address ownership, policy, capacity, failure, compatibility, and operations.

### Exercise 5

Design an edge for a national emergency-alert system during regional failure and hostile traffic. Cover listeners, identity, authorization, message authority, parsing, sizes, admission, priority, deadlines, retries, origins, zone and region loss, control-plane failure, configuration rollout, bypass, observation, privacy, and manual operation. Identify decisions the gateway must not own.

## Answers to the Exercises

### Answer 1

The **edge** is a controlled trust or ownership transition. A **reverse proxy** represents origins; a **load balancer** selects destinations; an **API gateway** mediates governed API concerns; a **WAF** applies selected threat rules; a **BFF** presents a client-specific API. **Transport termination** ends one protected connection. **End principal** is the user or machine represented; **workload identity** is the calling component. **Admission control** decides entry; a **rate limit** bounds time-based use; a **quota** bounds longer consumption. **Route ownership** governs public-to-origin mapping; **bypass resistance** prevents alternate evasion; **policy gravity** is accumulation of unrelated centralized logic. One component may perform several mechanisms, but their authority, failure, ownership, and evidence remain distinct.

### Answer 2

Planned per-instance capacity is $2{,}000\times0.60=1{,}200$/s. No-failure lower bound is $\lceil32{,}000/1{,}200\rceil=27$. With $z$ instances per zone, one-zone loss leaves $2z$; require $2z\times1{,}200\ge32{,}000$, so $z\ge13.33$ and minimum is 14 per zone, 42 total. Normal utilization relative to raw peak is $32{,}000/(42\times2{,}000)\approx38.1\%$. This omits uneven routing, correlated control or identity failure, handshakes, request-cost variation, large bodies, WAF work, rollout, origin capacity, and traffic growth; failure tests must validate sustained performance.

### Answer 3

The mobile client validates the gateway certificate and sends its credential over TLS. The gateway strips all client-supplied forwarding and identity headers, authenticates issuer, signature, audience, expiry, and required proof, and creates narrow integrity-protected context for the account-service audience. It calls over authenticated protected transport using gateway workload identity while preserving the end principal and tenant distinctly. The account service validates gateway and user context, then authorizes the current operation on the named account; the gateway does not infer ownership. Logs contain safe correlation and pseudonymous identities, never bearer tokens or account payloads. Certificate and signing-key rotation support overlap and revocation. The origin accepts only authorized gateway workload paths or applies an equivalent separately governed administrative contract, and direct-origin attempts are tested and rejected.

### Answer 4

Direct exposure is viable only when each origin independently supplies public transport, identity, abuse, compatibility, and operations. A shared gateway fits common public and partner technical policy but risks cross-audience blast radius and policy gravity. Separate trust-domain gateways isolate public mobile, partner, and internal administrative identities, limits, data, and availability; they cost more certificates, routing, deployment, and observation. A mobile BFF can compose client-shaped reads and reduce chatty calls while domain owners retain pricing and authorization. Bulk uploads deserve separate listeners and capacity because body size, duration, scanning, staging, and quotas differ. Choose boundaries from durable audience, consequence, workload, and ownership; maintain common governed platform mechanisms where they do not collapse isolation.

### Answer 5

Use separate public alert-submission, public read, agency partner, and administrative listeners with explicit owners. Authenticate agency workloads and officials, preserve both identities, and authorize jurisdiction and operation at alert authority; the gateway never decides whether an alert is true, its severity, geography, or cancellation. Strict parsing rejects ambiguous framing, spoofed forwarding data, invalid host, oversized or expanding bodies, and wrong-audience credentials. Cost-aware admission reserves capacity for authenticated life-safety commands, limits tenant and principal bursts, sheds public optional reads through safe cached content, and bounds queues, deadlines, retries, and fan-out. Instances span zones and regions whose remaining gateway, DNS, identity, configuration, network, and origin capacity is tested. Data planes retain validated last-known-good configuration through control-plane loss; changes use signed review, staged traffic, outcome comparison, and rollback. Origins require authorized path identity; break-glass paths are narrow, time-bound, audited, and rehearsed. Telemetry separates receipt, gateway acceptance, authoritative alert commit, distribution, and public outcome without logging credentials or sensitive drafts. Manual signed procedures preserve authority during disconnection. Full credit requires that timeout or gateway acceptance never become evidence that an alert was authorized, published, delivered, or cancelled.
