# Module 6 — Traffic locality, source identity, and dual stack

Once a flow is allowed and a Service has eligible endpoints, the data plane still has to choose one. That choice can prefer local Nodes or zones, preserve or translate source addresses, honor session affinity, and select an address family. These are not harmless optimizations: they change availability, capacity, identity evidence, and failure behavior.

The engineering question is:

> Which endpoint-selection rule is a preference, which is a hard requirement, and what failure does each rule create when topology or address-family capacity changes?

## Learning outcomes

By the end of this module, you can:

- apply endpoint eligibility before locality preference;
- distinguish hard local traffic policy from soft topology preference;
- explain source preservation and its trust limitations;
- evaluate session affinity under NAT and uneven clients;
- design `PreferDualStack` and `RequireDualStack` behavior deliberately;
- detect IPv4/IPv6 asymmetry hidden by client fallback;
- include capacity, failure domains, and rejected traffic in locality evidence;
- produce a topology decision record rather than a latency-only benchmark.

## Eligibility comes before locality

Endpoint selection should begin with endpoints that satisfy the Service and readiness contract. Locality must not resurrect an endpoint that is unready, terminating under the current policy, on the wrong port, or otherwise ineligible.

A useful ordering is:

```text
all published endpoints
→ protocol and port compatibility
→ readiness/serving/termination eligibility
→ address-family compatibility
→ hard traffic-policy restriction
→ topology preference
→ load distribution or affinity
```

If a local endpoint is unready, “prefer local” should fall back under a soft preference. A hard local-only policy may instead produce no endpoint by design.

## Hard local traffic policies

### `internalTrafficPolicy: Local`

For internal Service traffic, local-only policy restricts selection to endpoints on the receiving Node. On a Node without an eligible local endpoint, traffic has no backend even if remote endpoints are healthy.

This can be appropriate for Node-local agents, per-Node caches, or workloads whose semantics require local ownership. It is dangerous when applied merely to reduce latency.

### `externalTrafficPolicy: Local`

For externally originated Service traffic, local policy can preserve the original source address and avoid an extra cross-Node hop. It also requires the external load balancer or routing layer to send traffic only to Nodes with usable local endpoints. Health checks and endpoint registration must converge correctly.

Failure modes include:

- a Node remains externally healthy after its last local endpoint becomes unavailable;
- uneven endpoint placement overloads a subset of Nodes;
- zone or Node loss removes external capacity faster than the control plane reacts;
- source preservation works on one provider path but not another;
- readiness and load-balancer health use different criteria.

Source preservation and availability are therefore coupled decisions.

## Soft topology preference

Topology-aware routing or traffic-distribution features can prefer nearby endpoints while retaining fallback, depending on the feature and implementation.

A preference answers:

> If several endpoints are eligible, which should be tried first?

A requirement answers:

> Which endpoints are allowed to be considered at all?

Confusing the two creates brittle systems. Hard zone-local rules can turn a healthy multi-zone service into an outage when one zone has no endpoint. Soft preference can lower latency while preserving fallback, but only if the implementation supports and proves it.

Record:

- topology key and source of topology labels;
- how hints or preferences are published;
- fallback behavior;
- minimum endpoint capacity per failure domain;
- behavior during rollout, rescheduling, and zone loss;
- feature version and implementation conformance.

## Source address is evidence, not authenticated identity

Traffic can pass through several source transformations:

```text
client source
→ external load balancer
→ Node or Gateway source
→ Service translation
→ backend-observed source
```

`externalTrafficPolicy: Local` may preserve the network source in some paths. A reverse proxy can also carry a forwarding header. Neither is automatically trustworthy.

Separate these identities:

1. **transport peer** — the address connected to the current socket;
2. **forwarded client address** — metadata written by a trusted proxy;
3. **workload identity** — identity established through certificates, tokens, or platform mechanisms;
4. **application principal** — authenticated user/service/tenant identity.

At an Internet-facing Gateway, replace incoming forwarding headers rather than appending to untrusted values. Trust the forwarded address only when the immediate transport peer belongs to the configured proxy boundary.

Course 3 authorization must never become “allow this Pod IP.”

## Session affinity

`ClientIP` session affinity uses a client source key to prefer one backend for a bounded interval. It can reduce cache misses or support transitional stateful behavior, but it has important limitations:

- many users behind one NAT address can hotspot one backend;
- source translation at a proxy can collapse all clients to the proxy address;
- timeout or backend removal changes the mapping;
- it is not durable session storage;
- it is not tenant identity;
- it does not guarantee connection reuse.

Use affinity only when the application benefit and failure behavior are explicit. A correctly designed stateless API should not require it for correctness.

## Dual-stack Service design

Kubernetes Service address-family policy commonly distinguishes:

- **single stack** — one family;
- **prefer dual stack** — request both where the cluster can provide them, while allowing one;
- **require dual stack** — both families are required for successful allocation.

These are desired-state contracts, not end-to-end proof. A Service can have both addresses while:

- Pods have only one family;
- one family lacks routes;
- NetworkPolicy covers only one family;
- Gateway listeners bind only one family;
- external DNS publishes only A or only AAAA;
- egress/NAT exists for one family;
- the application listens only on an IPv4 socket.

`RequireDualStack` should be used only when failing allocation is preferable to silently releasing a single-stack service.

## Client fallback can hide failure

Modern clients may race or rapidly fall back between IPv6 and IPv4. This improves user experience but can hide a broken family in normal success metrics.

A dual-stack test matrix should record:

| Test | Required evidence |
|---|---|
| explicit IPv4 DNS and connect | A answer, selected address, route, policy, backend |
| explicit IPv6 DNS and connect | AAAA answer, selected address, route, policy, backend |
| normal client behavior | family chosen and fallback timing |
| one-family fault | whether fallback succeeds and latency impact |
| policy denial | expected family-specific negative result |

Metrics should label address family with bounded cardinality. Do not store raw client or Pod addresses as unbounded metric labels.

## Locality and capacity

A locality decision must be evaluated under representative placement and failure, not only normal latency.

Suppose three zones have endpoint counts `3, 3, 1`, and clients are evenly distributed. A strict same-zone rule leaves the third zone with one-third the backend capacity of the others. A zone-local latency benchmark may look excellent while overload and rejection rise sharply in that zone.

Evidence should include:

- offered requests;
- admitted and rejected requests;
- successful and failed requests;
- queueing and backend utilization;
- endpoint counts per topology domain;
- behavior after one endpoint or zone is removed;
- cross-zone traffic under fallback;
- source-address behavior.

Do not exclude rejected traffic from the benchmark denominator. Course 5 of API Engineering established this measurement discipline; it applies here as well.

## External health checks and Kubernetes readiness

Cloud or external load balancers may health-check Nodes, Gateway Pods, Services, or endpoints using criteria different from Kubernetes readiness. A Node can be considered healthy by the external system even when it has no eligible local backend.

For local external traffic policy, prove:

- what the external system checks;
- how quickly it removes a Node;
- whether the check reflects local endpoint eligibility;
- behavior during graceful termination;
- behavior during Node partition;
- source preservation after failover.

Do not assume that “Kubernetes Ready” and “load balancer healthy” are the same state.

## Worked investigation — lower latency, worse availability

Atlas enables hard local internal traffic policy after a benchmark shows lower median latency. Requests originating on Nodes with an API Pod improve. A batch client scheduled on a Node with no API Pod begins receiving immediate failures.

The Service, EndpointSlices, routes, and NetworkPolicy are correct. The data plane intentionally has no local backend and does not fall back.

The fault is an architectural mismatch: the team wanted a preference but configured a requirement.

The repair evaluates two options:

- return to cluster-wide eligibility and use a soft topology preference;
- guarantee one eligible endpoint on every client Node and accept the capacity/operational cost of a hard local rule.

The decision record includes failure-domain behavior, not only latency.

## Capstone implementation

Module 6 uses:

- `capstone/atlas_net/locality.py` for hard and preferred locality behavior;
- `capstone/atlas_net/services.py` for family and endpoint eligibility;
- `capstone/manifests/base/11-api-service-prefer-close.yaml`;
- `capstone/manifests/labs/service-local-policy.yaml`;
- `capstone/scripts/locality_failure_lab.py`.

The semantic model records fallback and failure explicitly. It does not claim conformance of a cloud load balancer or production topology-aware routing implementation.

## Decision record

A topology policy should state:

- desired outcome: latency, source preservation, bandwidth, or fault containment;
- hard requirement versus soft preference;
- endpoint-capacity assumptions per Node/zone;
- fallback behavior;
- address-family behavior;
- external health-check contract;
- source-identity implications;
- negative tests and failure injection;
- rollback.

## Locality changes the capacity equation

A global backend pool can use spare capacity anywhere the network reaches. A hard-local or hard-zone policy partitions that capacity. The relevant question becomes whether every eligible traffic location has enough local healthy endpoints for its offered load and failure surge.

For each Node or zone, estimate:

```text
local admitted traffic
÷ local healthy endpoint capacity
```

Then repeat after one endpoint, one Node, and one zone fail. A policy that lowers median latency in steady state can create deterministic overload during a rollout or zone imbalance.

Preferred locality keeps fallback and therefore has different semantics from required locality. Record which mode is used, the fallback trigger, how quickly hints or endpoint populations converge, and whether traffic can cross the intended failure boundary during recovery.

## Source preservation is a chain of decisions

The backend may observe:

- the original client address;
- a cloud load-balancer address;
- a Node address;
- a Gateway or proxy address;
- a translated address created by the Service data plane.

Which address survives depends on the external load balancer, Service traffic policy, proxy topology, overlay, and return path. Preserving an address is not enough to make it trusted. The application must know which immediate hop is authorized to assert forwarding metadata and replace untrusted client-supplied values.

A source-identity dossier should show the address at the edge, Node, Gateway, Service, and backend, along with any `Forwarded` or `X-Forwarded-*` fields. Course 8 proves trusted-header replacement in the local TLS gateway.

## Dual-stack clients choose paths, not just records

A dual-stack name can return A and AAAA answers. Clients may race attempts, prefer one family, cache failures, or fall back after a delay. The user-visible result can therefore succeed over IPv4 while the IPv6 path is completely broken.

For each critical journey, collect family-specific evidence:

- DNS answers and TTLs;
- source and destination address selection;
- route and policy decisions;
- Service family and endpoint family;
- TLS identity;
- latency, failure, and fallback timing;
- Node and zone population.

Do not aggregate the families into one availability number when dual-stack is part of the promise. A release may legitimately claim IPv4-only support, but it must not declare dual-stack from object fields alone.

## Health checks are part of topology policy

External and internal load balancers often use health checks that do not follow the same path as user traffic. A check may originate from provider ranges, target a Node port, bypass a Gateway Route, use HTTP instead of HTTPS, or evaluate a different readiness endpoint.

Align four populations:

1. endpoints Kubernetes considers eligible;
2. backends the load balancer registers;
3. backends the health checker considers healthy;
4. backends user traffic can actually reach.

A local traffic policy makes this especially important: a Node without a local endpoint should not remain externally healthy if it cannot serve traffic under the declared policy.

## Topology metadata is control input

Node, zone, and region labels influence scheduling, endpoint hints, routing, storage placement, and disruption decisions. They therefore require controlled ownership. Incorrect topology labels can send traffic across an expensive or unavailable link even when every Pod and Service is healthy.

Test topology changes as data changes: relabel a disposable Node or alter the semantic model, observe endpoint preference, verify fallback, and restore the original value. The evidence should distinguish a topology decision from a reachability failure.

## Transition

Module 6 completes east-west Service selection and locality. Module 7 introduces the role-oriented Gateway API model for north-south and shared listener ownership, without transferring application ownership to the edge team.
