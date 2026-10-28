---
module_id: PLAT-037
program: Platform Engineering
level: 1
module_number: 37
title: Service Connectivity
status: complete
last_verified: 2026-09-02
---

# Service Connectivity

## One-Page Review

### Governing question

How should a platform let one workload discover, authenticate, reach, balance across, and safely stop using another service while preserving protocol semantics, tenant boundaries, failure budgets, topology choices, and end-to-end evidence?

### Essential definitions

- A **service identity** is the stable logical name and authenticated principal of a service, distinct from any current IP address or process.
- **service discovery** maps a logical target to candidate endpoints and optional client policy at a revision/time.
- An **endpoint** is one network-reachable address, port, protocol, topology, readiness, and identity expectation for a service instance.
- A **Kubernetes Service** is a stable access abstraction over a logical endpoint set; it is not itself application health or authorization.
- An **EndpointSlice** is a scalable Kubernetes representation of endpoint addresses, ports, conditions, topology, and ownership.
- A **headless Service** publishes backend addresses without a cluster virtual IP or platform proxy load balancing.
- A **connection pool** reuses transport connections; its lifetime can outlast DNS, endpoint, certificate, route, or deployment changes.
- **load balancing** selects an eligible endpoint under a policy; configured weight is not guaranteed observed request share.
- A **circuit breaker** bounds connections, pending work, active requests, retries, or pools; it rejects excess work rather than repairing a dependency.
- **draining** stops assigning new work to an endpoint or connection while allowing bounded in-flight work to finish.

### Central model, mechanism, or theorem

For caller $c$, logical service $s$, and time $t$, resolver $D$ returns discovery revision $q$ with candidate endpoints $E_q$. Policy filters by authorization, protocol, readiness, topology, and health to eligible set $E_q^*$. Balancer $B$ chooses $e\in E_q^*$ for request $x$ subject to deadline, idempotency, retry budget, capacity, and connection state. Safe connectivity requires authenticated service identity and authorized flow, not merely successful DNS or TCP; bounded discovery staleness; endpoint lifecycle-aware pools; and evidence at name, route, transport, TLS, protocol, application, and user-outcome layers.

### Critical invariants

- Logical service name, ownership, API/protocol, port, authenticated identity, caller policy, and lifecycle are explicit and independently versioned from endpoint addresses.
- Discovery answers are bounded-staleness snapshots; clients refresh, reconcile removals, and preserve last-known-good only under declared limits.
- Only protocol-compatible, authorized, ready/serving, and policy-eligible endpoints receive new work; terminating endpoints drain according to explicit semantics.
- DNS, cluster virtual IPs, EndpointSlices, proxies, gateways, meshes, and client libraries have one declared ownership chain without competing route writers.
- Transport security authenticates the intended service identity and audience; successful encryption to an unintended peer is failure.
- Deadlines include queue, discovery, connect, TLS, proxy, server, and response time; retries never silently reset the caller's total budget.
- Retries and hedges are allowed only for semantically safe operations and consume bounded retry/load budgets with jitter.
- Connection, pending-request, concurrent-request, stream, and retry limits protect caller and dependency; overload is explicit and observable.
- Draining coordinates readiness, route removal, connection reuse, streams, shutdown grace, and deployment termination.
- Telemetry distinguishes discovery, routing, connect, TLS, protocol, server, dependency, policy, and application failures without high-cardinality endpoint chaos.

### Common failures

Hard-coding Pod IPs; using unqualified names across namespaces; confusing DNS success with reachability; caching DNS forever; treating headless answers as ordered/fresh load balancing; reading deprecated Endpoints at scale; selecting `ready` without understanding terminating behavior; setting `publishNotReadyAddresses` and then assuming readiness exclusion; using NetworkPolicy as application identity; allowing unrestricted egress; terminating TLS without checking service identity; sharing one pool across tenants with different policy; retrying non-idempotent writes; resetting deadlines per attempt; multiplying retries across layers; using round-robin over unequal endpoints; topology-local routing without failover; ejecting too many endpoints during shared failure; and declaring a rollout drained while long-lived connections still target old instances.

### Compact example

`checkout` calls logical target `inventory.prod.svc` over authenticated HTTP/2. DNS returns a stable Service address while EndpointSlices and the data plane track ready backends. The client has a 900 ms total deadline: 80 ms connect/TLS budget, 650 ms application attempt, and at most one jittered retry for an idempotent read within a 10% retry budget. The proxy enforces caller identity, destination identity, connection/request limits, and zone preference with cross-zone fallback. During rollout, an old endpoint becomes terminating, leaves new-request selection, sends graceful shutdown, drains streams for 20 seconds, then closes. Telemetry binds discovery revision, route, selected zone, attempt, peer identity, timing stages, and outcome without using raw endpoint IP as an unbounded metric label.

### Connections

This capability consumes environment/network boundaries from [PLAT-033](033-environment-provisioning.md), deployment and draining from [PLAT-034](034-deployment-capability.md), configuration from [PLAT-035](035-configuration-management.md), and workload identity/certificates from [PLAT-036](036-secret-delivery.md). It operationalizes Kubernetes Services, DNS, EndpointSlices, NetworkPolicy, and Gateway concepts introduced earlier and supplies later observability, data-service access, policy, reliability, and incident capabilities.

## Governing Question

What platform contract makes service-to-service communication stable at the logical interface while endpoint membership, addresses, topology, certificates, workload revisions, and failure conditions continually change?

Connectivity is a chain of state machines, not a boolean. Name resolution can succeed while no route exists. TCP can connect to the wrong workload. TLS can encrypt without validating the intended identity. An HTTP response can be syntactically valid yet violate the API contract. A successful request can still harm the user after retries duplicate a side effect.

The platform should offer a paved path for service naming, discovery, identity, authorization, routing, balancing, resilience, draining, and diagnosis. Applications still own API semantics, idempotency, deadlines, and domain health; the platform cannot infer them safely.

## Why This Matters

Ephemeral workload addresses are normal. Deployments replace Pods, autoscalers change membership, zones fail, and endpoints move. A stable service abstraction prevents every caller from tracking those changes independently, but it introduces controllers, caches, proxies, and policy whose behavior must be understood.

Connectivity mechanisms can amplify outages. Retries multiply load, health checks synchronize, short DNS TTLs overload resolvers, topology preference overloads surviving local capacity, and aggressive outlier ejection removes healthy endpoints during a shared dependency failure.

Security depends on direction and identity. Network reachability is not authorization. IP addresses are weak workload identity under reuse, NAT, proxies, and multi-tenancy. Service connectivity must bind an authenticated caller to an authenticated target and an allowed operation or route.

Long-lived connections hide change. HTTP/2, gRPC, database pools, WebSockets, and streaming RPCs can remain bound to endpoints after DNS or routing state changes. Deployment safety therefore depends on pool and protocol draining, not only endpoint removal.

## Prerequisites and Retrieval

Retrieve IP addressing/routing, TCP/UDP, DNS records and caching, TLS/mTLS, HTTP/1.1, HTTP/2 streams, HTTP/3/QUIC basics, gRPC, Kubernetes Pods/Services/EndpointSlices/readiness, NetworkPolicy, Gateway API, service accounts/workload identity, load-balancing algorithms, queues, deadlines, retries, idempotency, circuit breakers, health checks, graceful shutdown, distributed tracing, SLOs, and failure domains.

You should distinguish service identity from endpoint address; discovery from routing; readiness from liveness and application correctness; cluster IP from backend IP; headless discovery from load balancing; L3/L4 reachability from L7 authorization; connect timeout from request deadline; retry from replay safety; passive outlier detection from active health; configured topology preference from actual traffic; and route removal from connection/stream termination.

## Learning Objectives

After completing this module, you should be able to:

1. define a service-connectivity contract spanning name, protocol, identity, authorization, discovery, routing, and lifecycle;
2. choose cluster virtual IP, headless DNS, EndpointSlice/API discovery, gateway, mesh, or direct integration;
3. reason about DNS caching, endpoint conditions, topology, connection pools, and long-lived streams;
4. authenticate peers and authorize directional service flows with workload identity and network policy;
5. design deadlines, retries, hedges, connection limits, circuit breakers, and outlier detection from semantics and budgets;
6. coordinate readiness, endpoint removal, draining, shutdown, and rollout;
7. connect across namespaces, clusters, regions, and external dependencies without ambiguous ownership;
8. diagnose failures layer by layer with bounded-cardinality telemetry; and
9. operate connectivity control/data planes under scale, outage, upgrade, and rollback.

## Core Exposition

### Define the service contract

For every service, publish stable logical name, owner, API/protocol versions, ports, transport expectations, authenticated identity/trust domain, allowed callers/routes, availability class, topology, discovery method, endpoint readiness semantics, timeout/retry guidance, load characteristics, connection/stream behavior, and deprecation policy.

Names express durable intent, not deployment accidents. `inventory.prod.svc` is more useful than a Pod IP or ReplicaSet suffix. Decide namespace/tenant qualification and cross-environment naming so a short search path cannot accidentally select a same-named service elsewhere.

Named ports decouple service port from workload implementation port and support protocol metadata. Still verify protocol: sending cleartext HTTP to a TLS port or HTTP/1.1 assumptions to a gRPC-only endpoint produces confusing transport errors.

Ownership includes who may publish endpoints, routes, certificates, policy, DNS, and client defaults. One product experience may span several controllers, but their authoritative fields and reconciliation order must be unambiguous.

### Model the connectivity chain

Trace caller code to resolver, local cache, DNS/API control plane, endpoint set, route policy, proxy/load balancer, network path, destination listener, TLS peer, protocol handler, application method, dependency, and response. Each stage has distinct failure, timeout, evidence, and authority.

Model desired, programmed, and observed state. A Service object can exist while EndpointSlices are empty. A route can be accepted but not programmed. A proxy can hold stale assignments. A connection can survive after an endpoint disappears from discovery.

Treat data-plane success as scoped evidence. One synthetic probe from one zone does not prove all caller identities, address families, routes, protocols, sizes, or failure domains.

Create a diagnostic ladder: resolve name; inspect answer/revision/TTL; verify route and policy; connect; negotiate TLS and validate identity; negotiate protocol; call health or application operation; trace downstream and outcome.

### Use Kubernetes Service for stable access

A Kubernetes Service defines a logical endpoint set, usually from a selector, and a policy for access. ClusterIP gives a stable virtual address while controllers update EndpointSlices and a data-plane implementation routes to backends.

Validate selectors. An overly broad selector silently joins unrelated Pods; an overly narrow or changed label yields zero endpoints. Compare Service selector, Pod labels, EndpointSlice ownership, addresses, ports, and conditions.

Port and `targetPort` can differ. A named `targetPort` lets workload revisions use different numeric ports if the generated EndpointSlices remain coherent. Validate mixed revisions and protocols during rollout.

Service existence is not endpoint readiness or reachability. Observe API object, EndpointSlice membership, proxy/controller programming, network policy, and real requests separately.

### Understand EndpointSlice membership

EndpointSlices partition backend addresses by address type, port/protocol combination, and Service. Consumers must list/watch all slices for the Service label and reconcile a complete set; one slice is not the whole service.

Use `discovery.k8s.io/v1`, not the deprecated legacy Endpoints API. Legacy Endpoints can truncate beyond 1,000 addresses and lacks dual-stack and newer distribution information.

Interpret `serving`, `terminating`, and `ready`. Normally, ready approximates serving and not terminating. A terminating endpoint may remain serving during drain, and implementations may use serving+terminating endpoints if all endpoints terminate. `publishNotReadyAddresses` alters readiness assumptions.

Watch streams can disconnect, compact, duplicate, or reorder observations around relist boundaries. Maintain resource versions where supported, relist on expiration, apply idempotently, and periodically reconcile complete desired state.

### Choose virtual-IP or headless discovery

ClusterIP hides endpoint churn behind a stable address and platform data plane. It suits clients that should not implement discovery/load balancing. Behavior depends on proxy/network implementation, connection granularity, session affinity, traffic policy, and topology preferences.

A headless Service has no cluster IP or platform proxy load balancing. DNS returns backend addresses (for selector-backed ready endpoints under normal semantics), so clients own answer consumption, balancing, caching, health, removal, and connection lifecycle.

Headless mode suits stateful protocols, client-side balancing, and per-endpoint identity/topology. It is unsafe when a client uses only the first DNS answer forever or cannot refresh long-lived connections.

Selectorless Services and manually managed EndpointSlices can bridge external or migrated backends, but endpoint ownership, authorization, health, and lifecycle become platform responsibilities. Do not use the API server proxy as a generic path to arbitrary endpoints.

### Treat DNS as cached discovery

Normal Service A/AAAA records resolve to cluster IPs; headless records resolve to backend addresses. Named ports can publish SRV records. Cross-namespace callers should use qualified names to avoid search-path ambiguity.

DNS TTL is an upper caching signal, not guaranteed refresh timing across language runtimes, operating systems, sidecars, and applications. Some clients cache forever; others resolve per connection; negative answers may be cached separately.

Avoid retry storms when DNS fails. Use bounded caches, last-known-good only within declared staleness, backoff/jitter, and health evidence. Do not bypass service identity by falling back to a hard-coded IP.

DNS answers do not withdraw established connections. Pair resolution refresh with maximum connection age, idle timeout, endpoint update handling, or explicit pool draining where membership change matters.

### Design client-side discovery carefully

API/xDS/client resolvers can receive endpoints, health, priority, locality, weights, and service configuration faster or richer than DNS. This improves control but adds control-plane identity, authorization, watches, caches, schemas, and rollout risk.

Clients need bootstrap target, resolver deadlines, last-known-good cache, full snapshot plus incremental update semantics, version acknowledgement, rejection reporting, backoff, maximum staleness, and safe empty-set behavior.

An empty endpoint set may mean scale-to-zero, policy rejection, namespace error, rollout gap, control-plane outage, or actual unavailability. Preserve the distinction instead of silently retaining stale endpoints forever.

Keep discovery off the per-request critical path. Select from a locally validated snapshot, while refresh and reconciliation proceed asynchronously.

### Authenticate the destination and caller

TLS provides confidentiality/integrity only when the client validates the intended service identity, trust chain, name/SPIFFE ID, key usage, validity, and policy. A certificate valid for another internal service is not acceptable merely because the CA is trusted.

Mutual TLS authenticates both transport peers; authorization still decides whether caller identity may invoke destination/route/method. Proxies must preserve authenticated identity through a protected, explicit mechanism rather than trusting spoofable headers from arbitrary clients.

Rotate certificates and trust bundles using overlap and loaded-state evidence from PLAT-036. Connection reuse can keep old certificates alive beyond rotation; define maximum connection age or forced drain for compromise-sensitive cases.

Bind application tokens to audience and, where supported, proof-of-possession. Avoid one broad bearer token forwarded through multiple services.

### Enforce directional network policy

Kubernetes NetworkPolicy is additive. A connection requires source egress and destination ingress to allow it when both directions are isolated. Default behavior is non-isolated until selecting policies establish isolation, and implementation depends on a capable network plugin.

Use default-deny ingress and egress as a deliberate baseline, then allow DNS/identity/telemetry and exact service dependencies. Test actual enforcement; API object acceptance alone does not prove the network plugin enforces it.

IP/port policy constrains reachability, not application principal, HTTP method, tenant, or data authorization. Combine L3/L4 policy with workload identity and L7 authorization where needed.

Egress policy deserves equal attention. Unrestricted egress enables exfiltration and lets a compromised workload reach unintended control planes. Provide governed external destinations, proxies/gateways, DNS handling, and emergency behavior.

### Select routing and load balancing

Choose random, round-robin, least-request, weighted, ring-hash/consistent-hash, or priority/failover according to request cost, endpoint capacity, state affinity, and disruption behavior. Algorithm names hide implementation details such as slow start and connection-level versus request-level choice.

Round-robin assumes comparable endpoints and request costs. Least-request can adapt to variable latency but feedback may favor fast failures. Hash affinity preserves cache/session locality but needs bounded-load behavior and graceful membership changes.

Gateway API `backendRefs` weights express relative routing weights; they do not guarantee exact finite-sample request percentages. Observe actual attributed traffic, eligibility, route conditions, and data-plane programming.

Keep infrastructure routing separate from business partitioning. A tenant's authoritative shard belongs in domain routing/catalog state, not best-effort network load balancing.

### Use topology as a preference or guarantee deliberately

Same-node or same-zone routing can reduce latency and inter-zone cost, but it can overload local capacity or correlate failure. Kubernetes traffic distribution preferences differ from strict internal/external traffic policies.

Define fallback when local endpoints are absent, unready, or saturated. Strict local routing may intentionally return no endpoint; preference may cross zones. Make that choice visible to service owners.

Measure request distribution, capacity, errors, and failover by zone without turning every endpoint into a metric label. Test zone loss and asymmetric endpoint placement.

Multi-region routing adds DNS/global load balancing, health propagation, data consistency, residency, failover authority, and client retry interactions. Network reachability cannot make a non-replicated data service region-independent.

### Manage connection pools and long-lived streams

Pools reduce handshakes and latency but preserve endpoint, certificate, DNS, and protocol state. Bound idle time, maximum age, connections per endpoint, streams per connection, pending acquisition, and drain duration from workload and failure needs.

HTTP/2 multiplexes many streams over one connection, so connection-level balancing may concentrate requests. gRPC channels maintain subchannels and resolver/balancer state. WebSockets and streaming RPCs require explicit reconnection and resumption semantics.

When endpoint membership changes, stop new assignments, mark connections draining, let bounded in-flight work finish, and reconnect/resume elsewhere. Force closure after grace. Never assume removing an address from discovery moves existing streams.

Protect downstreams from reconnect storms with jitter, warm-up, concurrency limits, and staged rollout. A mass certificate or proxy restart can otherwise synchronize every client.

### Budget deadlines across the path

The caller owns an end-to-end deadline based on user/business usefulness. Allocate time for local queue, discovery if needed, connection acquisition, DNS, connect, TLS, proxy hops, server queue/compute, dependencies, and response transfer.

Propagate remaining deadline across hops. Each layer should stop work when the result is no longer useful. Per-attempt timeouts cannot exceed remaining total budget, and retries must not reset it.

Connect timeout and request deadline are different. A low connect timeout may be appropriate with several endpoints; a request can then spend most time in server processing. Queue/acquisition time must be visible rather than misclassified as server latency.

Avoid excessively short deadlines that create self-inflicted retries and abandoned work. Derive from latency distributions, user objectives, failure detection, and downstream budgets, then test overload and tail behavior.

### Retry only safe bounded work

Retry reads or idempotent operations for explicitly classified transient failures. A request ID alone does not create idempotency; the server must durably deduplicate the operation and return the prior result across retries.

Limit attempts, total deadline, retryable statuses, backoff, jitter, and retry concurrency/load. Prefer a retry budget relative to original traffic so a degraded dependency is not overwhelmed.

Avoid nested retries in SDK, sidecar, gateway, service, and job layers. If three layers each attempt three times, one logical operation can generate up to 27 downstream attempts before other fan-out.

Hedging sends overlapping attempts to reduce tail latency and consumes more concurrent capacity. Use only for safe operations, after a delay, with cancellation and a strict hedge budget.

### Bound overload with circuit breakers and bulkheads

Set limits for connections, pending requests, active requests/streams, connection pools, and retries per dependency/priority. Reject or shed before unbounded queues exhaust memory and make latency useless.

Circuit breakers are distributed local controls, not globally exact quotas. Envoy documents that concurrency races and per-endpoint minimum connections can exceed a nominal cluster connection threshold. Interpret metrics with implementation semantics.

Partition critical dependencies, tenants, priorities, and work classes so one overload does not consume all pools. But too many pools create their own memory, connection, and fairness cost.

Return explicit overload signals and honor upstream backpressure. Retrying a circuit-breaker rejection at the same saturated layer without delay worsens the problem.

### Use health and outlier detection conservatively

Readiness determines whether a workload should receive new traffic, but probes can be shallow or wrong. Client health checking can avoid backends that report not serving; it does not prove method-specific correctness or downstream health.

Passive outlier detection uses request failures/latency to eject endpoints. Shared dependency failure can make every endpoint look bad. Cap ejection percentage, require sufficient volume/hosts, distinguish local-origin from server errors, and retain capacity.

Active health success can prematurely re-admit an endpoint whose real traffic path remains broken. Pair active and passive signals and use slow start where appropriate.

Do not eject on caller-caused errors or expected application responses. Failure classification must match protocol and domain semantics.

### Coordinate rollout and graceful draining

Before serving, the new revision binds ports, protocol, identity, configuration, policy, and dependencies; readiness becomes true only when it can accept representative work. Then endpoint and route propagation must complete before meaningful traffic evidence.

On shutdown, mark not ready, observe endpoint/route removal, stop new application admission, notify protocol clients where supported, drain in-flight requests/streams and pools, flush required state, then exit before the termination deadline.

Budget pre-stop hooks and application grace within the orchestrator termination period. If the load balancer propagation time exceeds grace, clients will still reach a dead endpoint.

Rollout completion at the workload controller does not prove old connections or streams are gone. Observe active connections by revision, oldest connection age, and old-revision request rate.

### Govern gateways, meshes, and libraries

Client libraries are simple in topology but create language/version drift. Sidecar meshes standardize per-workload behavior but add proxies, injection, resources, lifecycle, and identity boundaries. Node proxies reduce sidecars but broaden node trust and attribution complexity. Gateways centralize cross-boundary policy and capacity.

Do not enable retries, timeouts, TLS, authorization, and telemetry independently at every layer. Declare which layer owns each behavior per route/protocol, and test combined effective policy.

Gateway API separates infrastructure ownership (GatewayClass/Gateway) from application routes and uses status conditions to report acceptance/programming. Cross-namespace references require explicit grants. Observe the implementation's conformance and status, not only stored YAML.

Treat control-plane configuration as production code: schema, policy, canary, rollback, stale-state behavior, version skew, and blast radius. A bad global mesh rule can exceed one application deployment's impact.

### Connect across clusters and external boundaries

Define global service identity, cluster-local instance identity, discovery authority, failover priority, health scope, address translation, TLS trust, policy, and data locality. Avoid same name with silently different semantics in different clusters.

Cross-cluster connectivity needs loop prevention and failure isolation. During partition, decide whether callers use local endpoints, stale remote endpoints, a secondary cluster, or fail closed. Record the chosen discovery and route revision.

For external dependencies, use governed egress with destination identity, DNS/TLS policy, connection/retry limits, audit, and provider-specific quotas. ExternalName is DNS indirection, not health, authorization, TLS correctness, or failover.

Private connectivity, NAT, and proxies can change source identity/address. Do not build destination authorization on an assumed client IP after translation.

### Observe and diagnose connectivity

Record logical source/destination, route and policy revision, protocol, attempt, response/error class, peer identity result, locality, timing stages, retry/hedge reason, circuit-breaker/outlier decision, and trace correlation. Sample safely and protect tenant/service relationship metadata.

Use low-cardinality service/route/zone labels for metrics. Raw IP, connection ID, DNS answer, certificate serial, and request ID belong in sampled logs/traces or protected diagnostic stores, not unbounded metric dimensions.

Distinguish DNS timeout/NXDOMAIN/stale result, no endpoint, policy denial, no route, connect refusal/timeout, TLS trust/name/expiry, protocol negotiation, reset, deadline, overload, server response, and application outcome.

Correlate both sides. Client “unavailable” and server “no request received” narrows the path; server completion after client deadline reveals abandoned work. Synthetic probes complement real traffic but do not replace it.

### Operate the capability

Measure resolution latency/failures/cache age, endpoint propagation, empty sets, route acceptance/programming, connection/TLS errors, loaded trust revision, pool utilization, queue/acquisition time, request/stream concurrency, retry/hedge amplification, circuit breaker rejection, ejection, topology distribution, drain duration, old-revision traffic, and user outcomes.

Capacity includes DNS QPS/cache, EndpointSlice watch fan-out, controller/API churn, proxy CPU/memory, TLS handshakes, connections/file descriptors, HTTP/2 streams, route count, telemetry cardinality, health checks, retries, and failover surge.

The following synthetic inventory demonstrates connectivity-control coverage.

<!-- bijux-verify: {"id":"service-connectivity-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"services=10\nqualified_identity=9\ndiscovery_reconciled=8\nmutual_authz=7\ndeadline_budgeted=8\nretry_bounded=7\noverload_bounded=7\ndrain_tested=8\nlayer_observed=9\n","stderr":""}} -->
```python
services = [
    {"name":"checkout",       "qualified_identity":True,  "discovery_reconciled":True,  "mutual_authz":True,  "deadline_budgeted":True,  "retry_bounded":True,  "overload_bounded":True,  "drain_tested":True,  "layer_observed":True},
    {"name":"inventory",      "qualified_identity":True,  "discovery_reconciled":True,  "mutual_authz":True,  "deadline_budgeted":True,  "retry_bounded":True,  "overload_bounded":True,  "drain_tested":True,  "layer_observed":True},
    {"name":"payments",       "qualified_identity":True,  "discovery_reconciled":True,  "mutual_authz":True,  "deadline_budgeted":True,  "retry_bounded":True,  "overload_bounded":True,  "drain_tested":True,  "layer_observed":True},
    {"name":"catalog",        "qualified_identity":True,  "discovery_reconciled":True,  "mutual_authz":True,  "deadline_budgeted":True,  "retry_bounded":True,  "overload_bounded":True,  "drain_tested":True,  "layer_observed":True},
    {"name":"shipping",       "qualified_identity":True,  "discovery_reconciled":True,  "mutual_authz":True,  "deadline_budgeted":True,  "retry_bounded":True,  "overload_bounded":True,  "drain_tested":True,  "layer_observed":True},
    {"name":"search",         "qualified_identity":True,  "discovery_reconciled":True,  "mutual_authz":True,  "deadline_budgeted":True,  "retry_bounded":True,  "overload_bounded":True,  "drain_tested":True,  "layer_observed":True},
    {"name":"recommendations", "qualified_identity":True, "discovery_reconciled":True,  "mutual_authz":True,  "deadline_budgeted":True,  "retry_bounded":True,  "overload_bounded":True,  "drain_tested":True,  "layer_observed":True},
    {"name":"notifications",  "qualified_identity":True,  "discovery_reconciled":True,  "mutual_authz":False, "deadline_budgeted":True,  "retry_bounded":False, "overload_bounded":False, "drain_tested":True,  "layer_observed":True},
    {"name":"legacy-erp",     "qualified_identity":True,  "discovery_reconciled":False, "mutual_authz":False, "deadline_budgeted":False, "retry_bounded":False, "overload_bounded":False, "drain_tested":False, "layer_observed":True},
    {"name":"shared-legacy",  "qualified_identity":False, "discovery_reconciled":False, "mutual_authz":False, "deadline_budgeted":False, "retry_bounded":False, "overload_bounded":False, "drain_tested":False, "layer_observed":False},
]

print(f"services={len(services)}")
for field in ("qualified_identity", "discovery_reconciled", "mutual_authz", "deadline_budgeted", "retry_bounded", "overload_bounded", "drain_tested", "layer_observed"):
    print(f"{field}={sum(service[field] for service in services)}")
```

The counts reveal contract gaps; they do not prove endpoint freshness, identity correctness, authorization enforcement, retry safety, overload containment, successful draining, or user outcomes.

## Definitions and Notation

Let caller $c$ request logical service $s$ at time $t$. Resolver $D(s,t)$ returns revision $q$, endpoint candidates $E_q$, TTL/staleness metadata, and optional client policy.

Each endpoint $e=(a,p,\pi,z,h)$ has address $a$, port $p$, protocol $\pi$, topology $z$, and health/lifecycle state $h$. Eligibility filter $P(c,s,x,q)$ applies identity, authorization, protocol, readiness, topology, and policy to yield $E_q^*\subseteq E_q$.

Balancer $B(E_q^*,x,\sigma)$ selects endpoint using request attributes $x$ and connection state $\sigma$. Selection probability or configured weight does not guarantee finite-sample observed traffic.

Let total deadline $T$ bound queue, discovery, acquisition, connect, TLS, proxy, application, dependency, and response time across all attempts. If layer $j$ permits $n_j$ attempts, naive maximum amplification across layers is $\prod_j n_j$; actual attempts are also bounded by deadline, cancellation, budgets, and failures.

Let $R_d(e,t)$ mean endpoint discovered, $R_p(e,t)$ programmed/eligible in the data plane, $R_c(e,t)$ accepting new connections, and $R_x(e,t)$ receiving requests/streams. Draining requires ordered convergence, not simultaneous equality.

## Mechanisms, Invariants, or Proof Structure

The connectivity assurance chain is:

1. define stable service name, owner, protocol/API, port, identity, callers, and lifecycle;
2. resolve a versioned endpoint set through a declared discovery authority;
3. filter endpoints by protocol, identity policy, readiness/lifecycle, topology, and health;
4. establish an authorized route and protected transport to the intended peer;
5. select endpoint under explicit balancing, affinity, and capacity rules;
6. bound queue, connection, stream, request, deadline, retry, and hedge behavior;
7. observe layered request and user outcomes, then reject/eject only with classified evidence;
8. reconcile endpoint/route change into pools and long-lived streams;
9. drain new work, in-flight work, connections, and shutdown during rollout; and
10. retire obsolete names, routes, policies, trust, discovery state, and compatibility.

This is not proof of reachability or correctness. DNS, APIs, controllers, proxies, networks, certificates, policies, clients, servers, dependencies, clocks, and telemetry can fail. The chain makes the chosen ownership and failure semantics testable.

The invariants are stable logical identity, bounded discovery staleness, eligible endpoint selection, single route ownership, intended-peer authentication, end-to-end deadline, bounded safe retries, overload containment, ordered drain, and layered evidence.

## Alternatives and Trade-Offs

**ClusterIP versus headless:** ClusterIP centralizes endpoint selection in the platform and simplifies clients. Headless exposes endpoints for client-side/stateful choice but transfers caching, balancing, health, and removal correctness to clients.

**DNS versus API/xDS discovery:** DNS is ubiquitous and loosely coupled but carries limited metadata and varied caches. APIs stream richer endpoints/policy and acknowledgements but add runtime client/control-plane complexity.

**Library versus proxy/mesh:** libraries avoid an extra hop/process but diverge across languages. Proxies standardize identity, policy, routing, and telemetry while adding resources, lifecycle, and another failure/control plane.

**L4 versus L7 routing:** L4 is protocol-agnostic and efficient but cannot authorize methods/paths or interpret responses. L7 offers richer policy and resilience but must parse protocols and protect metadata.

**Locality preference versus global balancing:** locality reduces latency/cost and failure-domain traffic. Global balancing uses capacity more evenly and survives local shortage but increases cross-zone exposure.

**Long-lived versus short-lived connections:** long-lived connections amortize handshake and support streams but retain stale endpoints/trust. Short lives improve rebalance and rotation at handshake, port, CPU, and latency cost.

**Active health versus passive outliers:** active probes test a designed path without user traffic but may be shallow. Passive signals reflect real requests but can misclassify shared failures and low samples.

**Fail fast versus wait-for-ready:** fail fast preserves deadlines and reveals unavailability. Waiting can bridge brief outages but consumes queue/deadline capacity and may hide persistent absence.

## Failure Modes and Misconceptions

- **“The Service IP is the service.”** it is one access abstraction; identity/API and backends remain distinct.
- **“DNS success proves connectivity.”** route, policy, endpoint, transport, TLS, protocol, and application can still fail.
- **“Low TTL guarantees fast failover.”** client/runtime caches and existing connections may ignore or outlive it.
- **“Headless DNS load balances.”** clients decide how to consume, cache, and select returned addresses.
- **“Ready means correct.”** readiness is an authored gate and can be shallow, stale, or overridden.
- **“NetworkPolicy authenticates services.”** it constrains address/port flows under plugin semantics; use workload identity too.
- **“mTLS authorizes the request.”** it authenticates transport peers; operation/tenant authorization remains.
- **“Round-robin means equal load.”** request cost, connections, streams, eligibility, and endpoint capacity differ.
- **“Topology preference keeps traffic local.”** preference can fall back; strict local policy can yield no endpoint.
- **“Retries improve availability.”** unsafe or multiplied retries duplicate effects and amplify overload.
- **“Circuit breaker prevents failure.”** it bounds resource use by rejecting work.
- **“Endpoint removal drains clients.”** existing pools and streams remain unless clients/proxies act.
- **“One successful probe proves the path.”** identities, zones, address families, routes, and methods differ.
- **“A mesh owns all resilience.”** application deadlines, idempotency, domain health, and combined layers remain.
- **“Old route YAML deletion retires connectivity.”** caches, pools, policies, DNS, trust, and consumers may persist.

## Worked Examples

### Example 1

A caller hard-codes a Pod IP. The rollout replaces that Pod and the address stops serving. A qualified Service name and readiness-backed EndpointSlices decouple callers from instance churn. Conclusion: stable identity must not be an ephemeral address.

### Example 2

A headless service returns six addresses, but a Java client caches the first for process lifetime. Five replicas receive no work and failover stalls. The client adopts supported resolver refresh, round-robin subchannels, and maximum connection age. Conclusion: headless discovery makes client behavior part of the platform contract.

### Example 3

`publishNotReadyAddresses` supports peer formation, but ordinary API traffic also reaches initializing members. Separate discovery and serving Services or enforce protocol-specific readiness. Conclusion: bootstrap discovery and user-serving eligibility can differ.

### Example 4

Source egress policy allows inventory, but inventory ingress omits checkout. Connections fail because both isolated directions must allow the flow. Conclusion: directional additive policy must be diagnosed on both endpoints.

### Example 5

A client validates only the internal CA, so it accepts a certificate for another service. Exact DNS/SPIFFE identity and audience validation rejects the peer. Conclusion: encryption without intended-peer authentication is insufficient.

### Example 6

Three layers each retry a payment request three times, producing up to 27 attempts. The service establishes durable idempotency, one owning retry layer, total deadline, retryable statuses, and a 5% budget. Conclusion: retry policy is end-to-end load policy.

### Example 7

Zone preference routes most traffic to two local replicas while eight remote replicas idle. Local saturation increases latency. Capacity-aware fallback and per-zone telemetry correct the imbalance. Conclusion: locality and capacity must be evaluated together.

### Example 8

A shared database outage causes every service endpoint to return 5xx; aggressive outlier detection ejects them all. Minimum volume, capped ejection, local/server error separation, and retained capacity avoid a self-created empty set. Conclusion: endpoint health signals may share a cause.

### Example 9

A gRPC rollout marks old Pods unready, but hours-long streams continue until the termination deadline kills them. The protocol sends graceful shutdown, stops new streams, supports resume tokens, and observes old-revision streams before exit. Conclusion: route drain and stream drain are different.

### Example 10

A route object is accepted but the controller reports unresolved backend reference. Stored configuration looks correct while no data-plane path exists. Status conditions, controller logs, programmed revision, and a scoped probe reveal the gap. Conclusion: desired route is not realized route.

## Cross-Program Connections

- **Computer Networks:** addressing, routing, DNS, transport, congestion, TLS, NAT, and protocol negotiation define the path.
- **Distributed Systems:** discovery, leases, watches, staleness, partial failure, retries, and membership changes govern convergence.
- **Algorithms:** hashing, weighted selection, queueing, backoff, and bounded-load balancing shape distribution.
- **Computer Security:** workload identity, mutual authentication, authorization, segmentation, egress, and metadata protection govern trust.
- **API Engineering:** deadlines, idempotency, status semantics, compatibility, and method safety determine resilience.
- **Operating Systems:** sockets, file descriptors, connection pools, DNS libraries, signals, and graceful process shutdown affect lifecycle.
- **Reliability Engineering:** SLOs, overload, bulkheads, retry budgets, health checks, draining, and failover bound incidents.
- **Data Engineering:** shard/leader discovery, database sessions, regional consistency, and stateful routing constrain network choices.

## References

1. Kubernetes, “Service,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/services-networking/service/
2. Kubernetes, “EndpointSlices,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/
3. Kubernetes, “DNS for Services and Pods,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
4. Kubernetes, “Network Policies,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/services-networking/network-policies/
5. Kubernetes, “Virtual IPs and Service Proxies,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/networking/virtual-ips/
6. Kubernetes, “Traffic Policies,” official documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/networking/virtual-ips/#traffic-policies
7. Gateway API, “HTTP Traffic Splitting,” project documentation, retrieved 2026-09-02. https://gateway-api.sigs.k8s.io/guides/user-guides/traffic-splitting/
8. Gateway API, “Gateway,” project API-type documentation, retrieved 2026-09-02. https://gateway-api.sigs.k8s.io/reference/api-types/gateway/
9. gRPC, “Service Config,” official documentation, retrieved 2026-09-02. https://grpc.io/docs/guides/service-config/
10. gRPC, “Retry,” official documentation, retrieved 2026-09-02. https://grpc.io/docs/guides/retry/
11. gRPC, “Health Checking,” official documentation, retrieved 2026-09-02. https://grpc.io/docs/guides/health-checking/
12. Envoy, “Circuit Breaking,” official documentation, retrieved 2026-09-02. https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking
13. Envoy, “Outlier Detection,” official API reference, retrieved 2026-09-02. https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/cluster/v3/outlier_detection.proto

## Exercises

### Exercise 1

Define service identity, discovery, endpoint, Kubernetes Service, EndpointSlice, headless Service, connection pool, load balancing, circuit breaker, outlier detection, and draining. State one non-guarantee for each.

### Exercise 2

Trace one gRPC request from logical target through DNS/API resolution, endpoint filtering, balancing, pool acquisition, connect, TLS/mTLS, NetworkPolicy/L7 authorization, HTTP/2 stream, server, response, deadline, telemetry, and endpoint drain.

### Exercise 3

A platform hard-codes Pod IPs, uses unqualified cross-namespace names, caches DNS forever, publishes unready endpoints, grants all egress, validates only the CA, retries every error in both proxy and SDK, has no connection limits, ejects endpoints after one failure, and declares drain complete when a Pod becomes unready. Diagnose at least fifteen failures and correct them.

### Exercise 4

Design connectivity for a multi-zone order API calling inventory over gRPC, a regional payment service over HTTP, and an external carrier API. Include discovery, identity, authorization, topology/failover, deadlines, idempotency/retries, overload, draining, and layer-specific evidence.

### Exercise 5

A stateful service must migrate from headless DNS/client-side balancing to a managed gateway/mesh without downtime. Clients include HTTP/2 streams, WebSockets, and short unary calls. Design dual-path compatibility, route ownership, identity, traffic progression, connection drain, rollback, and retirement proof.

## Answers to the Exercises

### Answer 1

Service identity is durable logical/authenticated identity but does not imply health. Discovery maps it to candidates but answers can be stale. An endpoint is one address/protocol/topology/lifecycle target but is not the service contract. A Kubernetes Service stabilizes access to an endpoint set but does not prove application correctness. EndpointSlice scales membership state but one slice is incomplete and conditions depend on controllers. A headless Service exposes backend addresses but does not load balance for the client. A connection pool reuses transports but can preserve stale membership/trust. Load balancing selects eligible endpoints but does not guarantee equal work. A circuit breaker bounds local resources but rejects rather than repairs. Outlier detection infers bad endpoints from observations but can misclassify shared failures. Draining stops new work and bounds old work but cannot preserve protocols lacking graceful resume.

### Answer 2

The client selects qualified logical target and remaining total deadline. Its resolver obtains a revisioned address/EndpointSlice snapshot and service config; policy filters protocol, ready/not-terminating status, topology, identity, and authorization. The balancer selects an endpoint under connection/request capacity. Pool acquisition time is charged to the deadline; if needed, DNS/connect and TLS occur, with exact destination identity and caller identity validated. Source egress and destination ingress permit the flow, while L7 policy authorizes the service/method. A gRPC subchannel opens an HTTP/2 stream, propagates remaining deadline and trace context, and the server performs domain work. Response/status and timing stages record route, attempt, peer identity, locality, and outcome. Retry occurs only if method/idempotency/status/budget/deadline permit. During drain, endpoint leaves new-work eligibility, the connection refuses new streams, in-flight streams complete or resume elsewhere, and old-revision traffic reaches zero before bounded closure.

### Answer 3

Pod IPs are ephemeral and unauthenticated; use stable service identity/discovery. Unqualified cross-namespace names can resolve unintended services; qualify namespace/domain. Infinite DNS cache ignores membership and failover; honor bounded refresh and drain old connections. Publishing unready endpoints sends traffic before service eligibility; separate bootstrap discovery or correct readiness. All egress enables exfiltration and unintended dependencies; default-deny then allow exact DNS, identity, telemetry, and services. CA-only TLS accepts wrong internal peers; validate exact name/SPIFFE ID, audience, and key usage. Retrying all errors repeats permanent failures and unsafe writes. Proxy plus SDK retries multiply attempts; choose one owner, safe statuses, total deadline, idempotency, backoff/jitter, and retry budget. No connection/pending/request/stream limits permits resource exhaustion; configure bulkheads/circuit breakers and overload response. One failure is insufficient outlier evidence; classify origin, require volume/consecutive evidence, cap ejection, and preserve capacity. Unready is only route intent; observe EndpointSlice/data-plane removal, stop new streams, drain pools/in-flight work, force close after grace, and prove zero old-revision traffic. Further fixes include route ownership, topology fallback, status conditions, low-cardinality telemetry, rollout and outage tests.

### Answer 4

Publish qualified names, protocol/API versions, identities, owners, and policies. Inventory uses ClusterIP or xDS-aware gRPC discovery with EndpointSlice-ready backends; service config sets client health, round-robin/least-request, 700 ms total deadline, and one idempotent inventory-read retry within budget. Prefer same zone with capacity-aware cross-zone fallback. Payment uses regional Gateway HTTPRoute, mutual workload identity, strict L7 method authorization, durable idempotency for payment creation, no blind write retry, circuit breakers, and explicit regional failover consistent with payment data. Carrier uses a governed egress gateway with DNS/TLS exact host identity, provider token audience, quotas, connection limits, two-second deadline, and retries only provider-documented idempotent operations. Default-deny egress/ingress allows exact flows. All paths record discovery/route revision, peer identity result, zone, pool/queue/connect/TLS/server time, attempts, overload, response class, and domain outcomes. Rollouts remove endpoints, drain connections/streams, and prove old traffic zero; zone/provider failure exercises fallback without retry amplification.

### Answer 5

First define one logical identity/API while distinguishing old headless and new managed paths. Deploy gateway/mesh infrastructure with no traffic, exact workload identities, route status evidence, protocol support, capacity limits, and no competing writer for old DNS. Release clients that can resolve both paths under a versioned preference and report selected path/connection revision. Mirror or progressively route short unary calls first, comparing outcomes and latency without double side effects. Move new HTTP/2 streams and WebSockets only after graceful shutdown, keepalive, maximum age, reconnect/resume, and cancellation semantics are tested. Progress by client cohort/zone while both paths accept compatible identity and authorization. Rollback stops new managed selection and drains managed connections without removing old discovery. Completion requires all supported clients selecting managed path, no new old connections, old stream/socket age reaching zero, equivalent outcomes, and tested failback. Then remove headless publication, old client resolver/config, routes/policy/trust/telemetry, and finally compatibility code after retention evidence.
