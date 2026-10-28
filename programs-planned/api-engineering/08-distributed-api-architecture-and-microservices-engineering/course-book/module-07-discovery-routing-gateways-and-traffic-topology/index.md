# Discovery, Routing, Gateways, and Traffic Topology

**Module 07 of 10**

> **Governing question:** How do callers find healthy service instances and route traffic without moving business ownership into gateways or creating several competing retry layers?

## Place in the program

The platform now has explicit service and data ownership, bounded synchronous collaboration, and one durable cross-service workflow. This module adds the next necessary property without weakening the previous guarantees.

## Learning outcomes

- distinguish service identity from instance address and endpoint health
- compare DNS, registry, client-side, proxy, and platform routing models
- keep authentication normalization and protocol adaptation at the edge while preserving domain ownership
- avoid business workflows and private data stores inside the gateway
- design canary, shadow, and failover routes with bounded blast radius
- evaluate service mesh features without making the mesh the source of application correctness

## Capstone result

Implement service registration, health-aware routing, gateway edge policy, bounded traffic shifting, and an optional Kubernetes topology with explicit ownership of each routing decision.


## Service name, instance address, and health are different

A service is a logical capability. An instance is one running copy. An address is one route to an instance. A health observation is a time-bounded claim about whether an instance should receive a class of work.

Hard-coding instance addresses couples callers to deployment. Treating a DNS answer as health can send work to a process that is alive but draining. Treating liveness as readiness can restart a healthy process because a dependency is temporarily unavailable.

## Discovery models

### Platform DNS

Kubernetes Services and cluster DNS provide stable names over changing pods. This is a good default for many systems. The application still needs deadline, compatibility, and response policy.

### Service registry

Instances register metadata such as version, zone, protocol, and readiness. Client or proxy selects a compatible healthy instance. Registry freshness and split-brain behavior must be understood.

### Client-side load balancing

The client resolves several endpoints and chooses one. This can integrate gRPC health and service configuration but makes client libraries more operationally significant.

### Proxy or sidecar routing

A local or shared proxy handles discovery and balancing. It centralizes traffic policy but can obscure attempts and retries unless observability is explicit.

### Gateway routing

The edge gateway routes public traffic by host, path, tenant, version, or canary policy. It should not become the internal service registry for every call.

## Health-aware routing

The reference registry selects only instances that are healthy, accepting, and compatible with the caller’s supported versions. Round-robin is intentionally simple; the important lesson is eligibility before balancing.

A good instance state includes:

```text
identity
service name
contract version
zone or failure domain
healthy
accepting new work
drain deadline
last observation time
```

A stale health record should expire rather than remain healthy forever.

## Gateway responsibilities

The gateway may own:

- public TLS termination;
- credential extraction and validation boundary;
- public request-size and rate policy;
- protocol adaptation;
- absolute request deadline;
- trace initiation;
- route and version selection;
- bounded response composition;
- public error translation.

It must not own:

- run state transitions;
- artifact retention decisions;
- notification retry policy;
- cross-service saga state;
- private database queries;
- authorization rules only it can enforce.

A “smart gateway, dumb services” design centralizes business risk at the edge and leaves internal routes unsafe.

## Retry layers

Suppose the public client retries once, the gateway retries twice, a sidecar retries twice, and the gRPC library retries twice. One user attempt can become 18 service attempts. Select one owner per edge and make attempt count visible.

Mesh or proxy retries are safest for well-understood, idempotent transport failures. Application mutations still require durable idempotency and outcome reconciliation.

## Traffic shifting

Course 8 uses four route modes:

- **legacy** — only the original path is authoritative;
- **shadow** — candidate runs but its result is not returned;
- **canary** — a deterministic bounded fraction uses the candidate;
- **cutover** — candidate is authoritative, with rollback retained;
- **decommissioned** — legacy path is removed after the evidence window.

Canary routing must be stable for a key when stateful behavior or comparison matters. Random per-request routing can alternate a user between incompatible state views.

## Shadow traffic

Shadowing is useful only when side effects are controlled. Reads can often shadow directly. Writes need a simulation, dry-run, idempotent duplicate identity, or candidate path that records comparison without producing external effects.

The Notification extraction can replay events into a shadow consumer because delivery side effects are disabled. The Artifact extraction shadows reads and compares bytes, checksum, metadata, authorization, and latency before write ownership changes.

## Service mesh boundary

A mesh can provide workload mTLS, routing, telemetry, and some resilience policy. It does not know whether `CompleteRun` is idempotent, whether an artifact belongs to a tenant, or whether a compensation is semantically valid. The course treats a mesh as optional infrastructure whose policy must align with application ownership.

## Python and TypeScript implications

Both tracks implement health-aware version-filtered routing. The deterministic round-robin behavior supports shared tests. A real platform may use locality, least request, or adaptive algorithms, but those choices are only valid after eligibility and correctness.

## Evidence required before Module 8

Demonstrate instance registration, health removal, compatible version selection, shadow comparison, bounded canary routing, and gateway refusal to execute a business transition.
## Control plane and data plane

Routing systems are easier to reason about when two concerns are separated.

The **control plane** decides or distributes configuration:

- service names and endpoints;
- health status;
- route weights;
- certificate trust;
- policy declarations;
- version and locality metadata.

The **data plane** handles each request or stream:

- resolves or selects an endpoint;
- establishes a connection;
- forwards bytes and metadata;
- applies configured timeouts or limits;
- records telemetry.

A control-plane outage should not instantly erase all data-plane knowledge. Conversely, stale configuration needs an expiry or refresh policy. These trade-offs are visible in DNS, client-side discovery, proxies, gateways, and service meshes.

## Stable service identity versus changing instances

A caller depends on a service identity such as `artifact-service`, not on pod or process addresses. Instances are replaceable. Discovery maps the stable identity to eligible endpoints.

Eligibility is not only “process is alive.” It may include:

- ready for this interface;
- correct service version;
- correct locality;
- not draining;
- healthy enough for new work;
- authorized for this tenant or environment.

Kubernetes Service and DNS abstractions can provide stable names and endpoint sets. Client libraries, proxies, or a mesh may perform balancing. The application still owns semantic deadlines, idempotency, and fallback.

## Gateway as edge, not brain

The capstone gateway owns:

- public protocol termination;
- credential normalization;
- request budget creation;
- route selection;
- bounded response composition;
- edge telemetry.

It does not own:

- run state transitions;
- artifact retention decisions;
- notification retry policy;
- tenant resource authorization;
- cross-service saga state.

Putting business rules in the gateway creates a hidden central monolith that is harder to test and release. A gateway should enforce edge policy and delegate owner decisions.

## Route selection needs stable identity

Random canaries make comparison and rollback noisy. A deterministic route key—such as a hash of tenant and stable request identity—can keep related traffic on one version during evaluation.

A routing decision should record:

```text
route policy version
stable selection key
selected service version
fallback eligibility
deadline budget
shadow/canary mode
```

Do not use sensitive raw identifiers in logs. A pseudonymized stable key can support analysis without disclosing user data.

## Shadow traffic is not free

Shadowing sends a copy of representative input to a candidate while the current path remains authoritative. The candidate must suppress or isolate side effects.

Unsafe shadow examples:

- sending real webhooks twice;
- charging a payment method;
- publishing duplicate events;
- mutating a shared database;
- acquiring real worker leases.

Safe strategies include:

- read-only comparison;
- dedicated shadow tenant and storage;
- effect sink that records intent without execution;
- deterministic simulation for external calls;
- replay against captured, sanitized inputs.

The comparison oracle covers semantics, authorization, error class, resource use, and latency—not merely JSON equality.

## Retry policy across proxy layers

A proxy or mesh may support retries, but it lacks full application knowledge. Use infrastructure retries only for narrowly classified safe cases, such as connection establishment before any request bytes were accepted, and align them with the caller’s retry budget.

Record one retry owner. Disable hidden retries in other layers or include them in the attempt budget. Telemetry should show original request identity and attempt number across layers.

## Service mesh: useful mechanism, dangerous abstraction

A service mesh can centralize:

- workload mTLS;
- endpoint discovery;
- traffic policy;
- telemetry transport;
- selected connection-level resilience.

It cannot determine:

- business idempotency;
- saga compensation;
- whether stale data is safe;
- resource authorization;
- correct partial response semantics;
- service ownership.

The course treats a mesh as an optional platform mechanism. The dependency graph and service contracts remain authoritative. An architecture that only works because the mesh retries every failure is not well designed.

## DNS and connection lifetime

A service name may resolve to changing endpoints. Long-lived HTTP/2 or gRPC channels can continue using an endpoint after DNS changes unless the client or proxy refreshes and reconnects. Very short connection lifetimes can increase handshake cost and reduce efficiency.

Operational policy should define:

- discovery refresh behavior;
- connection age or drain behavior;
- endpoint removal semantics;
- readiness and graceful shutdown;
- retry on connection failure;
- how version skew appears during rolling deployment.

The Course 7 channel and health lessons remain relevant; Course 8 adds multiple independently released services and routing layers.

## Traffic topology review

Draw at least three views:

1. **logical dependency graph** — which service depends on which capability;
2. **network flow graph** — which workloads can connect through which proxies;
3. **request path graph** — actual calls for each critical journey.

These graphs are not identical. A gateway may be on the network path without being a semantic dependency. A broker may carry events without appearing on a synchronous request path. A mesh sidecar may be a network hop but not a business service.

Comparing the views reveals undeclared calls and accidental centralization.

## Failure examples

### Discovery returns no endpoints

The caller fails within its remaining budget and reports dependency unavailability. It does not extend the public deadline while waiting indefinitely for discovery.

### One endpoint is unhealthy

The balancer stops sending new work after health or connection evidence. In-flight operations follow cancellation and retry policy.

### Gateway is unavailable

Public traffic fails even if backend services are healthy. The gateway needs its own capacity, redundancy, and SLO because it is a required edge component.

### Mesh control plane is unavailable

Existing data-plane configuration may continue for a bounded period. New policy or endpoint changes may be delayed. Runbooks must distinguish control-plane and service failure.

### Candidate canary produces wrong authorization

Semantic comparison blocks promotion immediately, even if latency is better.

These are topology-specific failure modes, not generic “network error” labels.
