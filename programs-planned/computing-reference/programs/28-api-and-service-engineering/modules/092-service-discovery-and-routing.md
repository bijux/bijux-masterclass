---
module_id: API-092
program: API & Service Engineering
level: 2
module_number: 92
title: Service Discovery and Routing
status: complete
last_verified: 2026-09-02
---

# Service Discovery and Routing

## One-Page Review

### Governing question

How should a caller resolve a stable service identity into an authorized, compatible, healthy-enough endpoint set and choose routes under churn, caching, partial failure, multi-region policy, load, and control-plane staleness without turning discovery into hidden correctness or security authority?

### Essential definitions

- **service identity** is the stable logical name/security identity of a capability, distinct from endpoint address or deployment instance.
- An **endpoint** is a concrete address/protocol/port plus metadata for one serving instance or proxy.
- **service discovery** maps a service/target identity to candidate endpoints and service configuration.
- **registration** publishes endpoint metadata; a **lease** makes it valid only while renewed through a bounded expiry.
- **eligibility** is the conjunction of registration, lease, readiness/health, identity, policy, version/capability, tenant, and locality constraints.
- A **resolver** obtains and caches discovery results; a **load balancer/router** selects among eligible candidates for an operation.
- **client-side routing** selects in the caller/runtime; **server-side routing** sends to an intermediary/virtual IP/proxy that selects upstream.
- **draining** removes new work while allowing bounded in-flight work to finish before deregistration/termination.

### Central model, mechanism, or theorem

At time $t$, the eligible endpoint set for caller/operation context $q$ is

$$
E_t(q)=G_t\cap L_t\cap H_t\cap I_t\cap P_t(q),
$$

where $G$ is registered, $L$ lease-valid, $H$ health/readiness-eligible, $I$ authenticated identity/metadata-valid, and $P$ policy-compatible. Routing chooses only from the caller’s locally known approximation $\widehat E_t$ and therefore must bound staleness, validate endpoints at connection/handshake, handle selection failure, and expose discovery revision/age. For positive weights $w_i$, simple weighted choice uses $p_i=w_i/\sum_{j\in E}w_j$; weight is policy/capacity intent, not proof of current load.

### Critical invariants

Logical identity is stable; endpoints are ephemeral. Registration authority and endpoint/workload identity are authenticated. Lease, readiness, serving, terminating/draining, version/capability, region/zone, tenant/environment, protocol, and capacity metadata have defined sources and semantics. Empty, stale, partial, and contradictory discovery results produce explicit bounded behavior.

Routing does not bypass authorization, data residency, consistency, or contract compatibility. Health is layered: process alive, accepting new work, and able to serve the relevant operation are different claims. Retries do not blindly rediscover/reselect into amplification or duplicate effects. Control-plane updates are versioned, ordered/reconciled, cached as last-known-good within expiry, observable, and recoverable; unknown or unauthorized endpoints never become a fail-open fallback.

### Common failures

Service name equals DNS host forever; endpoint IP used as identity; anyone can self-register; lease without fencing; stale deregistration removes a replacement; readiness equals liveness; active check differs from real traffic; one global “healthy” bit; endpoint advertised before keys/config/data ready; termination before drain; DNS TTL ignored by runtimes; negative cache outlives recovery; watches drop events; incremental update applied without snapshot/revision; split-brain registries; empty set falls back to hardcoded address; wrong tenant/region/version endpoint; global failover violates residency/consistency; least-connections ignores multiplexed/long work; retry chooses same failed endpoint; passive ejection cascades; weights stale; canary stickiness lost; thundering re-resolution; discovery on every request; control-plane outage erases routes; and telemetry omits resolution age/revision/selection reason.

### Compact example

Three endpoints have weights 2, 3, and 5, so weighted probabilities are 20%, 30%, and 50%. The weight-5 endpoint begins draining: discovery marks it not eligible for new work before termination. The remaining weights renormalize to 40% and 60%; existing connections drain within deadline. Clients that missed the update still validate connection/workload identity and use bounded passive failure handling. **Conclusion:** discovery state, route policy, connection validation, and drain behavior jointly determine safety.

### Connections

[Tracing Through Client, Proxy, and Service](010-tracing-a-request-through-client-proxy-and-service.md), [Deadlines](071-timeout-and-deadline-budgets.md), [Retries](072-retries-and-backoff.md), [Circuit Breaking](073-circuit-breaking-and-bulkheads.md), [Load Shedding](074-api-level-load-shedding.md), [Fan-Out](077-fan-out-and-tail-latency.md), [Consistency](079-consistency-and-read-after-write-expectations.md), and [Gateway Responsibilities](091-api-gateways-and-edge-responsibilities.md) constrain routing. The next module distinguishes service-mesh relationships from discovery ownership.

## Governing Question

What identity, registration, lease, health, metadata, consistency, cache, load-balancing, locality/failover, security, observability, and lifecycle rules make service discovery and routing safe for independently deployed distributed services?

## Why This Matters

Distributed services need stable names while instances scale, restart, relocate, roll versions, drain, and fail. Hardcoded addresses couple releases and failover. Discovery adds indirection so callers can find current capacity—but every indirection result is a time-delayed claim about a changing world.

Discovery cannot guarantee an endpoint will work. An endpoint can fail after publication; a healthy process can reject one tenant/version; network partitions show different sets to callers; caches intentionally preserve old data. The client/router must combine discovery with connection identity, deadlines, passive evidence, retry budgets, and application semantics.

Routing changes correctness, not just load. It selects region, replica freshness, version/capability, tenant boundary, and sometimes state shard/leader. Sending a read to a stale replica after write, a regulated tenant across a border, or a new client to an old server can violate the contract while every endpoint is “healthy.”

Discovery is also a privileged control plane. A forged registration redirects credentials/data; a global bad snapshot drops all endpoints; a stampede against DNS/registry spreads outages. Durable architecture limits authority/blast radius and provides last-known-good behavior without accepting arbitrary endpoints.

## Prerequisites and Retrieval

Retrieve [Tracing a Request Through Client, Proxy, and Service](010-tracing-a-request-through-client-proxy-and-service.md), [Authentication Context Propagation](033-authentication-context-propagation.md), [Concurrency Control](038-concurrency-control-at-the-api-boundary.md), [Deadlines](071-timeout-and-deadline-budgets.md), [Retries and Backoff](072-retries-and-backoff.md), [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), [API-Level Load Shedding](074-api-level-load-shedding.md), [Fan-Out and Tail Latency](077-fan-out-and-tail-latency.md), [Consistency and Read-After-Write](079-consistency-and-read-after-write-expectations.md), [Preventing Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), [Independent Evolution](090-evolving-an-api-without-coordinated-consumer-releases.md), and [Gateway Responsibilities](091-api-gateways-and-edge-responsibilities.md).

Retrieve service catalog/names/owners; DNS zones/records/TTL/resolvers; registry schemas/APIs/consistency/leases; endpoint identities/certificates; orchestration readiness/termination; protocol/port/version/capability/tenant/region/zone/shard/leader/capacity metadata; resolver/cache/watch/refresh behavior; routing/load-balancing/affinity/failover; health checks/passive ejection; retry/circuit/deadline; control/data-plane topology/config revisions; SLO/capacity/cost; telemetry; incident history; rollout/rollback/DR; and bypass/fallback paths.

## Learning Objectives

After completing this module, you can:

1. distinguish logical service identity, target, endpoint, registration, lease, resolver, router, and workload identity;
2. model endpoint eligibility as a conjunction of registration, lease, health, identity, and operation-specific policy;
3. compare DNS, SRV/SVCB, registry/watch, client-side, proxy-side, and hybrid discovery;
4. design authenticated registration, leases, generations/fencing, deregistration, readiness, drain, and termination sequencing;
5. manage snapshots/deltas, revisions, caches, TTL, negative answers, watch loss, compaction, partitions, and last-known-good state;
6. choose random, round-robin, weighted, least-load, power-of-two, consistent-hash, priority, locality, and subset routing appropriately;
7. integrate discovery with deadlines, connection pools, retries, circuits, load shedding, affinity, consistency, and version compatibility;
8. secure multi-tenant/environment endpoint metadata, resolver/control-plane access, workload identity, and routing policy;
9. observe discovery age/revision, eligible-set churn, selection, endpoint outcomes, ejection, drain, and control-plane health; and
10. test and recover discovery/routing under churn, stale views, overload, partial failure, regional failover, and rollout.

## Core Exposition

### Separate names, endpoints, and identities

Give the capability a stable service identity with owner and trust domain. A discovery target can add namespace/environment/port/protocol/subset, but do not make a pod IP, host, deployment name, or mutable team label the durable product identity.

Endpoint address answers where to connect now. Workload identity answers what authenticated service instance accepted the connection. Verify that identity/audience during TLS/mTLS or equivalent handshake; registry possession alone is not authorization.

Record service and endpoint metadata provenance. Route policy may use region, zone, shard, leader/follower, version/capability, protocol, tenant class, rollout cohort, and capacity—only when the responsible controller owns and authenticates that field.

Keep discovery from exposing sensitive topology broadly. Callers receive only the targets/metadata they are authorized to use.

### Choose discovery mechanism from requirements

DNS is distributed, ubiquitous, cache-oriented, and fits relatively coarse name-to-record mapping. RFC 1034 describes DNS concepts/resolvers; TTL and resolver/application caching mean updates are not instantaneous. Address records may hide endpoints behind a virtual IP/load balancer.

RFC 2782 SRV records locate services with priority/weight/port; application/protocol specifications must define how clients use them. RFC 9460 SVCB/HTTPS records support alternative endpoints and parameters for services/HTTP origins. Client/runtime support and security remain prerequisites.

A registry/watch API can distribute richer endpoint metadata and faster changes with revisions, snapshots/deltas, leases, and authorization, at higher control-plane coupling/complexity. Kubernetes DNS and EndpointSlices illustrate coarse service naming alongside scalable endpoint data.

Hybrid designs use DNS to locate gateway/control plane, registry to configure proxies/clients, and workload handshake to authenticate endpoints. Do not stack mechanisms without defining precedence, cache, and failure behavior.

### Allocate client-side and server-side routing

Client-side discovery exposes endpoint sets to a library/runtime, enabling per-request load balancing, locality, connection pools, and fast passive feedback without an extra proxy hop. It increases language/runtime/version/config complexity and topology exposure.

Server-side routing sends callers to stable virtual address/proxy/gateway; it centralizes policy/telemetry and hides endpoints but adds hop/blast radius and may obscure caller-specific deadlines/affinity. The proxy itself still needs discovery.

gRPC name resolution feeds target information to client load balancing and supports DNS/xDS/custom resolvers. Preserve the distinction: resolving candidates does not select one or guarantee readiness.

Select one authoritative routing layer for a given decision or coordinate budgets. Client, gateway, mesh, and service independently retrying/rebalancing create unpredictable paths and amplification.

### Authenticate registration and ownership

Only an authorized orchestrator/workload/controller may register endpoints under a service/namespace/environment. Bind registration to workload identity, deployment generation, owner, protocol/port, and allowed metadata. Prevent arbitrary host/port/tenant/region claims.

Prefer controller-derived registration from desired/observed orchestration state over every process mutating shared registry, while retaining service readiness signals. Validate address ranges and forbid loopback/metadata/admin networks where inappropriate to prevent SSRF/routing injection.

Audit create/update/delete with actor, revision, old/new value, reason, and source. Quotas protect registry/control plane from high-cardinality or flapping workloads.

Separate permission to publish endpoint, change route weights/policy, and alter service ownership. A compromised instance should not reroute all traffic.

### Use leases, generations, and fencing

A lease expires unless renewed, bounding ghost endpoints after crash/partition. Define renewal interval, expiry, clock model, grace, ownership, and how data planes treat near-expiry/stale records. Lease validity does not prove application health.

Use unique instance/generation IDs. A delayed deregistration from old instance must not delete a new registration reusing the same address/name. Compare-and-delete/fencing token applies only to the generation that owns the lease.

Renewals can stampede. Jitter, batch, shard, and rate-limit while ensuring expiry margin. During control-plane partition, decide whether existing endpoints remain last-known-good, leases expire locally, or service availability yields to safety.

Record server-observed lease timestamps/revisions rather than trusting client wall clocks. Test pause, clock skew, lost renewal, duplicate registration, address reuse, and delayed messages.

### Distinguish liveness, readiness, serving, and operation health

Liveness asks whether the process should be restarted. Readiness asks whether it should receive new traffic. Serving can be protocol/service-specific. Draining/terminating removes new work while bounded in-flight work completes. Do not use one bit for all.

Readiness should cover critical local initialization/config/keys/listeners and dependencies required for the declared service, without recursively failing on every optional downstream. A check that always calls a shared database can synchronize failure and eject the entire fleet.

Active checks probe from a particular network/path with synthetic request. Passive signals observe real connection/reset/status/latency, but mix caller input, overload, and downstream failure. Combine carefully and avoid treating one client-specific denial as global endpoint death.

Health can be operation/subset specific. An endpoint might serve reads but not writes, old version but not new, tenant A but not B. Encode only stable policy dimensions; do not create unbounded per-request health metadata.

### Sequence readiness, draining, and termination

On startup: establish workload identity/config/listener/dependencies, pass readiness, publish/activate endpoint, then receive traffic. Publishing before capability is ready creates predictable errors.

On shutdown: mark not-ready/draining in authoritative state, propagate update, stop new work, signal connection drain, finish/cancel in-flight work within deadline, deregister/revoke lease, then terminate. Account for cached clients that missed the update.

Servers still reject or redirect safely after drain begins; client/proxy uses connection failures/passive feedback and bounded retries. Drain duration reflects longest allowed stream/request, not infinite sessions.

Rolling deployments need capacity headroom so drain and new readiness do not overload survivors. Observe endpoint counts and in-flight work per generation.

### Distribute snapshots and deltas safely

Snapshots are self-contained and recover from missed events at bandwidth cost. Deltas are efficient but require base revision/order/deduplication and reconciliation. Watchers reconnect after loss/compaction using last acknowledged revision or fetch snapshot.

Every response has authoritative version/revision and resource identity. Apply an atomic coherent set where cross-resource dependencies matter; do not publish route before referenced cluster/endpoints/policy exist.

xDS illustrates dynamic resource discovery via management servers and versioned request/response patterns. Regardless of protocol, clients ACK/NACK or report rejected config, retain last-known-good, and expose convergence.

Partial/malformed update never empties safe state silently. Unknown fields/version compatibility follow control-plane contract, and policy/schema upgrades are staged across clients.

### Bound cache staleness and refresh

Cache reduces latency/load and allows data-plane continuity. Define positive TTL/lease bound, refresh-before-expiry, jitter, stale-while-error limit, negative caching, maximum last-known-good age, eviction, and memory/cardinality.

DNS TTL is an upper freshness hint only if every resolver/runtime honors it; some pool connections or cache longer/shorter. Measure effective behavior. Long-lived connections can outlive record TTL and need drain/keepalive policy.

Negative answers require bounded TTL; otherwise a transient empty state prevents recovery. Empty endpoint set is meaningful—do not fall back to hardcoded/untrusted address. Return unavailable/wait-for-ready only within caller deadline and queue bounds.

Prevent thundering refresh with jitter, request coalescing/singleflight, backoff, local caches, and hierarchical distribution. Do not resolve on every request.

### Define endpoint eligibility as policy

Start from registered lease-valid endpoints, then filter by authenticated service identity, readiness/serving, environment/tenant, protocol/port, version/capability, shard/leader/replica role, region/residency, rollout cohort, maintenance/drain, and circuit/ejection state.

Policy is caller/operation specific. A follower can serve stale-tolerant read but not linearizable write; a canary serves opted-in clients; a regional endpoint may be prohibited for regulated tenant.

If filters yield empty, report which stage removed candidates without leaking sensitive topology. Do not relax security/residency/version automatically. A deliberate failover policy can broaden locality while keeping nonnegotiable predicates.

Keep eligibility deterministic for a given revision/context and test precedence/interactions. Avoid free-form labels that silently control routing.

### Choose a load-balancing algorithm honestly

Round-robin/random work for roughly homogeneous independent requests; connection pooling/multiplexing can distort request distribution. Weighted selection expresses expected capacity/rollout share. For weights 2,3,5, probabilities are 0.2,0.3,0.5; update/renormalize when membership changes.

Least-connections/least-requests uses feedback but can favor slow-starting or broken endpoints, misread long streams, and herd clients when state is delayed. Power-of-two choices reduces global measurement needs by sampling candidates and selecting the less loaded under a defined signal.

Consistent/rendezvous hashing provides affinity and limited remapping under membership change, useful for caches/shards, but hot keys/failed members and uneven weights need handling. Affinity is not correctness unless state architecture makes it so.

Priority/locality routing prefers zones/regions and spills on capacity/health thresholds. Define failover ordering, reserve capacity, data consistency/residency, and recovery hysteresis to avoid flapping.

### Incorporate capacity, slow start, and overload

Endpoint weights come from declared capacity or controlled rollout, not instantaneous truth. Combine with concurrency/latency/passive load carefully. New endpoints need slow start/warmup for caches/JIT/connections; failed endpoints need cautious re-entry.

Load shedding belongs at endpoints and upstream layers because discovery can lag. Endpoint saturation must not be encoded by rapid registration flapping; use concurrency limits/backpressure and stable health/ejection signals.

Outlier detection/ejection can protect traffic but creates positive feedback: ejecting slow endpoints increases load on survivors. Cap ejection percentage, require evidence volume, distinguish local network/client failures, and probe/reintroduce gradually.

Model headroom under rolling drain, zone loss, failover, retry amplification, fan-out, connection limits, and control-plane churn. Routing cannot create capacity.

### Integrate retries, circuits, and connection pools

A retry may reselect another endpoint only when operation is safe/idempotent or protected, body replayable, deadline/budget remains, and failure class suggests endpoint-local/transient cause. Do not turn a service-wide overload into endpoint roulette.

Track attempted endpoint set to avoid immediate repeats where appropriate, but do not scan entire fleet. Bound attempts and propagate cancellation. Retry selection is part of load-balancing policy.

Circuit state can be per endpoint, locality, service, operation, or caller depending on failure scope. Per-client circuits fragment evidence; global circuits amplify false positives. Share only signals with understood scope.

Connection pools react to membership: stop new streams on draining endpoint, close after grace, validate identity on new connection, and prevent stale pool from ignoring discovery indefinitely.

### Preserve consistency, affinity, and version contracts

Route writes/reads according to promised consistency. Read-after-write may require leader, session token, causal version, or bounded wait; “nearest healthy replica” is insufficient.

Shard/partition routing maps key to authoritative set and epoch. Stale shard map can send to old owner; servers validate epoch/ownership and redirect/reject safely. Discovery is not the sole correctness fence.

Session affinity stabilizes caches/state but must survive endpoint churn or fail over explicitly. Do not rely on local memory without documented loss/migration behavior.

During rolling versions, filter or negotiate compatible endpoints. Routing new capability to old server is an unsafe matrix cell; routing policy/revision must exclude it and rollback remain compatible.

### Secure discovery and routing

Authenticate/authorize resolver, registry, controllers, data planes, and endpoints. Encrypt sensitive control traffic, rotate keys/certs, sign/verify config where needed, and audit access/mutations. Separate read/write/admin and tenant namespaces.

Validate endpoint addresses, ports, protocols, names, metadata, reference closure, sizes, counts, and update rates. Prevent registry poisoning, SSRF, environment crossover, malicious weights, topology exfiltration, and denial through flapping/cardinality.

DNS security/authenticity and transport requirements depend on environment; endpoint TLS/workload identity remains decisive. Discovery says where, not who.

Use least privilege: caller resolves only eligible services; controller manages only owned namespaces; endpoint cannot change global route; operator emergency actions are scoped/audited/expiring.

### Design locality and regional failover

Prefer local zone to reduce latency/egress and isolate failure, but keep enough cross-zone diversity for correlated host/rack loss. Avoid sending all traffic to one tiny local subset when it lacks capacity.

Regional failover requires health plus data plane readiness, replicated state/consistency, identity/keys, quotas, dependencies, capacity, residency/legal, version/config, and DNS/control-plane convergence. Exercise it.

Failover and failback use hysteresis, staged cohorts, capacity/rate ramp, state reconciliation, and explicit decision authority. Rapid oscillation worsens outage.

Partition behavior is policy: region may continue with stale last-known-good endpoints or fail closed for strong consistency/security. Do not discover across a partition and assume data correctness.

### Observe discovery and routing decisions

For each resolver/data plane, expose target/service, source mechanism/server, last successful refresh, revision/age, cache hit/stale/negative, watch reconnect/error/NACK, candidate and eligible counts by bounded reason, and convergence lag.

For routing, record algorithm/policy revision, locality/subset/version/cohort, selected endpoint identity (controlled cardinality), connection/reuse, attempts/ejection/drain, latency/error, and origin effect correlation. Separate resolution, connection, TLS, queue, service, and response latency.

Do not put arbitrary endpoint IDs/tenant/users in unbounded metrics; use secure logs/traces or sampled exemplars with privacy policy. Keep control-plane audit distinct from request telemetry.

Alert on prolonged empty sets, stale beyond policy, unknown/unauthorized endpoints, membership/weight flapping, readiness-to-traffic lag, config rejection/skew, ejection saturation, zone imbalance, failed drain, and fallback use.

### Test, operate, and evolve the subsystem

Test resolver parsers and policy with snapshots/deltas, reordering/duplication/loss/compaction, invalid metadata, huge sets, address reuse, expiry, clock/pause, negative cache, empty set, control-plane outage, split brain, and client version skew.

Integration/fault tests cover endpoint crash/drain/startup, network partition, DNS/registry unavailable, stale caches/connections, identity mismatch, zone/region loss, overload/ejection, retry storm, canary rollback, shard move, and recovery/failback.

Version discovery schemas/protocols/policies; stage management and data-plane upgrades, maintain last-known-good compatibility, and observe ACK/NACK/convergence. Temporary subsets/weights/routes have owner/expiry/removal.

Back up/restore service names/ownership, endpoint policy—not ephemeral instances unnecessarily—certificates/keys, route configs, revisions/audit, and management state. Rebuild endpoints from authoritative orchestration and reconcile after restore.

## Definitions and Notation

Let $G_t$ be registered endpoints, $L_t$ lease-valid endpoints, $H_t$ readiness/health-eligible endpoints, $I_t$ endpoints with valid authenticated identity/metadata, and $P_t(q)$ endpoints satisfying policy for caller/operation context $q$. True eligible set is their intersection $E_t(q)$; a resolver/router acts on delayed local view $\widehat E_t(q)$.

For positive endpoint weight $w_i$, normalized weighted choice probability is $p_i=w_i/\sum_{j\in E}w_j$. Let lease expiry be $e=t_{renew}+L$ under authoritative server time; the endpoint is lease-valid only before $e$. Let discovery revision be $v$ and local last-update age $a$.

A **snapshot** replaces a coherent resource set; a **delta** changes a known base. **NACK** reports rejected update while retaining last-known-good. **Outlier ejection** temporarily removes an endpoint based on scoped passive evidence; it is not deregistration.

## Mechanisms, Invariants, or Proof Structure

**Eligibility conjunction.** An endpoint can be registered but expired, healthy but wrong tenant/version, or policy-compatible but unauthenticated. Each predicate independently prevents safe selection; routing must choose from their intersection, not any one list or average health score.

**Staleness impossibility.** An endpoint may fail immediately after any successful discovery response. No cached/control-plane snapshot can guarantee present reachability. Therefore routing needs bounded staleness plus connection identity/timeout/passive failure handling; discovery alone cannot prove success.

**Generation-fencing argument.** Old instance A and replacement B reuse an address. A delayed delete without generation can remove B. Requiring delete token/generation equal to the current lease owner makes A’s stale delete inapplicable to B.

**Weight normalization.** For weights 2,3,5, sum is 10 and probabilities are 20%,30%,50%. Removing weight-5 endpoint leaves sum 5, so remaining shares become 40%,60%. The arithmetic is correct only if endpoints remain eligible and weights represent desired relative share.

Operational invariants are: stable logical identity; authenticated registrations/endpoints; lease generation fenced; readiness/drain distinct; updates versioned/reconcilable; cache/staleness bounded; empty unsafe fallbacks forbidden; eligibility context-specific; selection capacity-aware; retries bounded/idempotent; service verifies shard/authorization/consistency; failover preserves nonnegotiable policy; decisions observable; and recovery tested.

## Alternatives and Trade-Offs

DNS minimizes client coupling and scales through caching but offers coarse metadata and slow/variable convergence. Registry watches offer rich fast updates but add client/control-plane state and outage coupling. Hybrid designs localize each role with explicit precedence.

Client-side load balancing removes proxy hop and uses direct feedback but multiplies implementations/upgrades and exposes topology. Proxy-side centralizes policy and hides endpoints but adds latency/capacity/blast radius. Standardized data-plane proxies can combine centralized control with distributed routing.

Short TTL/lease improves failure cleanup but raises query/renewal load and sensitivity to pauses/partitions. Long values improve continuity/load but prolong ghosts. Pair bounded staleness with passive connection failure/drain and identity verification.

Active health detects before traffic but may not represent real operations and can synchronize dependency load. Passive health reflects real paths but conflates caller/input/downstream failures and reacts after harm. Combine scoped evidence with conservative ejection/re-entry.

Locality routing lowers latency/egress but concentrates zone failure and can overload small subsets. Global balancing uses capacity but increases latency/cost/residency/consistency risks. Use hierarchical priority with headroom and governed failover.

Affinity improves cache/state locality but creates hot spots and complicates failover. Stateless/random routing balances well but may require shared state. Make correctness independent of affinity where feasible.

## Failure Modes and Misconceptions

- “DNS name is service identity.” Name resolution and authenticated workload identity are separate.
- “Registered means healthy.” Lease/readiness/policy/identity can fail independently.
- “Health is one Boolean.” Liveness, readiness, serving, operation, and drain differ.
- “TTL means every client refreshes then.” Runtimes/connections/caches vary.
- “Watch never loses events.” Reconnect, compaction, reorder, and snapshot recovery are necessary.
- “Empty means use last hardcoded IP.” That can bypass identity/policy and route stale instances.
- “Least connections is least load.” Multiplexing, stream cost, and delayed feedback distort it.
- “Weights are live capacity.” They are declared relative routing intent.
- “Passive errors identify a bad server.” Client input/network/downstream overload can be scoped differently.
- “Eject all slow endpoints.” Positive feedback can collapse survivors.
- “Nearest is always best.” Consistency, residency, version, and capacity can dominate.
- “Failover is an address change.” State, identity, dependencies, quota, and policy must be ready.
- “Retry fixes stale discovery.” It can multiply load/effects and select the same failure domain.
- “Discovery authorizes the request.” Services still authenticate/authorize and verify ownership/epoch.
- “Control plane can push partial config.” Cross-resource references may require atomic coherence.
- “Endpoint count proves capacity.” Request cost/concurrency/headroom determine capacity.

## Worked Examples

### Example 1

Endpoint registers successfully but presents workload certificate for another service. Connection identity validation rejects it; registry membership alone never grants trust.

### Example 2

Old instance’s delayed deregistration arrives after replacement reused address. Generation mismatch prevents deletion of the replacement lease.

### Example 3

Three endpoints weighted 2,3,5 receive expected 20%,30%,50%. Weight-5 drains; remaining shares renormalize to 40%,60% for new work.

### Example 4

DNS record TTL is 30 seconds, but client pool holds connections for 30 minutes. Drain/connection policy—not TTL alone—determines stale endpoint use.

### Example 5

A transient NXDOMAIN is cached for ten minutes. Service recovers in seconds but callers remain down. Negative TTL is bounded and refresh/backoff observable.

### Example 6

Passive ejection sees timeouts caused by one client’s network and removes healthy endpoints globally. Evidence is scoped per data plane/locality before global action.

### Example 7

Nearest follower is healthy but cannot satisfy read-after-write token. Policy routes to a replica meeting causal version or waits/fails within deadline.

### Example 8

New client capability could hit old server during rollout. Version/capability eligibility filters remove unsafe cells; rollback versions remain in matrix tests.

### Example 9

Registry watch loses deltas after compaction. Client fetches coherent snapshot, validates revision/resources, and keeps prior known-good until atomic apply.

### Example 10

Region failover endpoints are reachable but lack data residency approval and fresh state. Policy refuses automatic broadening and returns attributable unavailable rather than violating contract.

## Cross-Program Connections

[Network Engineering](../../24-network-engineering/ROADMAP.md) supplies DNS, addressing, routing, load balancing, TLS, anycast, connection behavior, and network failure diagnosis.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies workload identity, registry/control-plane authorization, endpoint validation, SSRF/poisoning defense, tenant isolation, key/certificate rotation, and audit.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies leases, failure detectors, clocks, consistency, membership, partitions, replication, hashing, leader/shard routing, and recovery.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies service catalogs, orchestrator registration, discovery control planes, DNS, proxies, EndpointSlices, xDS, policy, tenancy, SLOs, and self-service.

[Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies regional/zone topology, managed DNS/load balancing, autoscaling, networking, capacity, failover, multi-account/project boundaries, and infrastructure recovery.

## References

1. IETF, [RFC 1034: Domain Names — Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034.html).
2. IETF, [RFC 2782: A DNS RR for Specifying the Location of Services](https://www.rfc-editor.org/rfc/rfc2782.html).
3. IETF, [RFC 9460: Service Binding and Parameter Specification via DNS](https://www.rfc-editor.org/rfc/rfc9460.html).
4. Kubernetes, [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/).
5. Kubernetes, [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/).
6. gRPC, [Custom Name Resolution](https://grpc.io/docs/guides/custom-name-resolution/).
7. Envoy, [xDS REST and gRPC Protocol](https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol).

## Exercises

### Exercise 1

Design discovery/registration/lease/readiness/drain for a service scaling across three zones with rolling versions, address reuse, 10,000 endpoints, and clients using long-lived multiplexed connections.

### Exercise 2

For eligible endpoint weights 2, 3, and 5, compute selection shares before and after the weight-5 endpoint drains. Then explain why those shares do not prove capacity or actual request distribution.

### Exercise 3

Design a resolver/watch/cache state machine for snapshots, deltas, revision gaps, compaction, negative results, control-plane outage, malformed updates, and recovery without per-request discovery or unsafe fallback.

### Exercise 4

Choose routing policy for writes requiring a leader, read-after-write sessions, stale-tolerant reads, a 5% canary, zone-local preference, regulated tenants, and regional disaster failover. State precedence and empty-set behavior.

### Exercise 5

Diagnose an incident where latency causes passive ejection, survivors overload, clients retry across zones, discovery flaps, and global failover serves stale data. Design stabilization, evidence, and durable changes.

## Answers to the Exercises

### Answer 1

Use stable service/namespace/environment identity and controller-authenticated endpoint registrations with unique generation, workload identity, protocol/port, zone, version/capability and server-time lease. Shard/batch/jitter renewals and watches for 10,000 endpoints; clients consume coherent snapshots/deltas with revisions, ACK/NACK, reconnect/compaction snapshot, last-known-good and bounded age. Startup establishes identity/config/listener/dependencies, readiness, then activation. Shutdown marks drain/not-ready, propagates, stops new streams, signals connection drain, waits bounded longest supported stream, compare-and-delete by generation, then terminates; stale clients get connection close/passive failure and safe bounded retry. Long-lived pools honor discovery drain and max connection age/keepalive rather than DNS TTL alone. Rolling version eligibility prevents unsafe pairs and keeps capacity headroom across zones. Test pause/partition/address reuse/lost watch/config skew, observe readiness-to-traffic/drain completion, and never use endpoint address as identity.

### Answer 2

Initial sum is $2+3+5=10$, so shares are $2/10=20\%$, $3/10=30\%$, and $5/10=50\%$. Once weight-5 endpoint becomes ineligible for new work, remaining sum is $2+3=5$, so shares renormalize to $2/5=40\%$ and $3/5=60\%$. These are policy probabilities conditional on eligible membership and the selection algorithm. Actual traffic differs through finite randomness, connection pooling/multiplexing, affinity, request cost/duration, retries, ejection, locality, in-flight work, stale client views, and changing membership. Weights express desired relative share, not measured live capacity. Validate concurrency/latency/errors/saturation, warmup/headroom, per-client distribution, and drain behavior before interpreting them as safe load allocation.

### Answer 3

Maintain target, authoritative source/trust, current coherent revision/resource graph, last successful/attempt time, expiry/max-stale, cache state, watch session/base revision and backoff. Validate signed/authenticated response, schema/version, size/count, references, endpoint identity metadata, tenant/environment and monotonic revision. Apply full snapshot atomically; apply idempotent delta only to matching base, deduplicate/order, and fetch snapshot on gap/compaction/unknown base. NACK malformed/incompatible update while retaining known-good and reporting reason. Coalesce/jitter refresh and never resolve per request. Bound positive and negative TTL; empty authoritative set remains empty/unavailable, not hardcoded fallback. During outage serve last-known-good only within policy while connection identity/timeout/passive handling remains; after expiry fail attributable/wait only within deadline/queue bound. On recovery snapshot/reconcile, then resume watch; expose age/revision/convergence/negative/stale/reconnect/NACK/eligible counts.

### Answer 4

Nonnegotiable filters first: authenticated service/environment, tenant authorization/residency, protocol/version/capability, valid lease/readiness, shard/role/epoch. Writes select current leader and server validates epoch. Read-after-write carries causal/session version and selects leader or replica proven caught up, otherwise bounded wait/fail. Stale-tolerant reads may use ready followers. Canary applies only compatible opted-in population with stable 5% cohort; it never overrides leader/residency. Within eligible subset prefer same zone subject to capacity/headroom, then cross-zone. Regional failover is a separately approved priority tier requiring residency, replicated/fresh-enough state, keys/identity, dependencies, quota/capacity and compatible config; activate with hysteresis/cohorts and reconcile/fail back. If filters empty, return attributable unavailable or bounded wait within deadline; do not relax tenant/residency/version/consistency. Record policy revision, filter reasons, selected role/zone/region/version and causal outcome.

### Answer 5

Stop positive feedback: disable/scope passive global ejection, cap ejection percentage, halt cross-zone/global retries, shed/admit by priority/concurrency, preserve healthy capacity, extend no arbitrary timeouts, and freeze discovery/config changes at known-good. Determine whether latency originates endpoint saturation, dependency, network/client locality, control-plane churn, or telemetry. Keep consistency-sensitive traffic from stale failover; route writes/causal reads only to authoritative/fresh tier and fail safely. Recover gradually: probe/reintroduce endpoints with slow start, restore zones within headroom, bounded retries, stabilize leases/readiness, then reconcile state and fail back with hysteresis. Correlate discovery revision/age, eligible/ejected sets, client locality, attempts, saturation, dependency latency and data-version outcomes. Durable changes include scoped health signals/minimum evidence, ejection caps, service-level circuit/overload policy, retry budget, stable registration versus saturation, capacity/zone reserves, failover freshness/residency gates, update-rate protection, fault/load tests, and runbooks/alerts for flap/ejection/failover.
