---
module_id: API-093
program: API & Service Engineering
level: 2
module_number: 93
title: Service Mesh Relationships
status: complete
last_verified: 2026-09-02
---

# Service Mesh Relationships

## One-Page Review

### Governing question

Which workload-transport security, routing, resilience, and telemetry responsibilities can a service mesh supply, how do they compose with applications, gateways, discovery, identity, and platforms, and which API/domain guarantees must remain outside the mesh?

### Essential definitions

- A **service mesh** is an infrastructure layer/control system for governed service-to-service communication through managed data-plane interception or explicit proxies.
- The **data plane** carries traffic and enforces received policy; the **control plane** distributes identities, trust bundles, routes, clusters, security, resilience, and telemetry configuration.
- A **sidecar** is a workload-local proxy process/container; **node/ambient/sidecarless modes** intercept or proxy traffic elsewhere. Placement changes failure and trust boundaries, not required guarantees.
- **workload identity** authenticates a workload/service instance; it is not automatically end-user, tenant, action, or object authorization.
- **traffic interception** redirects selected traffic through the data plane; **capture completeness** is evidence that intended paths cannot bypass equivalent controls.
- **peer authentication** establishes who is on the other connection; **authorization policy** determines which authenticated workload may reach a bounded service/port/operation context.
- A **mesh revision** is an immutable control/data-plane/config identity used to reason about compatibility, convergence, and rollback.
- **policy composition** is the interaction among client library, application, gateway, mesh, discovery, and platform decisions—not simply “most strict wins.”

### Central model, mechanism, or theorem

For one logical call through client/application and $k$ proxy hops, latency is

$$
L_{total}=L_{app}+\sum_{i=1}^{k}L_{proxy,i}+L_{network},
$$

while retry allowances multiply: $A\le\prod_i(r_i+1)$ before fan-out/hedging. Mesh safety requires capture $C$, authenticated workload identity $I$, policy correctness $P$, protocol preservation $S$, bounded resilience $B$, and observable/converged configuration $O$ as a conjunction. Even $C\land I\land P\land S\land B\land O$ does not prove end-user/object authorization, domain effects, consistency, or API compatibility.

### Critical invariants

The mesh’s purpose, topology, interception scope, bypass paths, ownership, and degraded modes are explicit. Workload identities/trust domains/keys are attested, short-lived/rotated, audience/scoped, and verified at the receiving boundary. Plaintext versus mTLS is measurable; migration never silently downgrades. Services retain authorization for user/tenant/action/object/property/state.

Timeout/retry/circuit/load-balancing policy has one end-to-end owner and respects deadlines, idempotency, bodies, effects, overload, and application semantics. Gateway handles external/product edge responsibilities; discovery supplies eligible endpoints; mesh consumes or distributes routing without inventing business truth. Data planes retain known-good config during bounded control-plane failure, reject invalid updates, expose revision/convergence, preserve protocol semantics, and can be upgraded/removed without changing public contracts.

### Common failures

“Encrypted means authorized”; workload identity used as end user; namespace/location trusted implicitly; permissive mTLS remains forever; traffic bypasses sidecar/node interception; health/probe/admin traffic accidentally captured; application connects by IP and defeats identity; gateway and mesh duplicate auth/routing/retries; mesh retries unsafe call; client+mesh+service retry multiplication; proxy timeout exceeds deadline; circuit ejects healthy workloads on downstream failure; outlier detection cascade; percentage route ignores version compatibility; mirroring causes effects/secrets leakage; protocol sniffing misclassifies; HTTP/2/gRPC/stream semantics damaged; telemetry double-counts attempts; sidecar resource starvation; node proxy expands blast radius; control-plane outage pushes/retains wrong config; policy selectors match too broadly; multicluster trust/residency violated; and teams cannot debug or bypass safely during incident.

### Compact example

A checkout service calls payments through two mesh proxies. mTLS proves the caller workload identity `checkout`, and mesh policy permits it to reach payments. That does not prove the end user may charge card X or amount Y. Payments verifies propagated user/tenant context, object/action authorization, idempotency, and state; mesh supplies authenticated workload transport and telemetry. **Conclusion:** workload-to-workload authorization narrows reachability but cannot replace domain authorization.

### Connections

[Authentication Context](033-authentication-context-propagation.md), [Object Authorization](046-object-level-authorization.md), [Deadlines](071-timeout-and-deadline-budgets.md), [Retries](072-retries-and-backoff.md), [Circuit Breaking](073-circuit-breaking-and-bulkheads.md), [Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), [Gateway Responsibilities](091-api-gateways-and-edge-responsibilities.md), and [Service Discovery](092-service-discovery-and-routing.md) define the adjacent authorities. Later testing and operations modules verify the combined path.

## Governing Question

How should teams decide whether to adopt a mesh, allocate gateway/discovery/application/platform responsibilities, establish workload identity and mTLS, compose routing/resilience/telemetry, operate multiple data-plane modes and clusters, and retain debuggable failure and exit paths?

## Why This Matters

A mesh can standardize workload identity, encryption, traffic policy, discovery integration, telemetry, and progressive routing without requiring every application language to implement them. This is valuable in polyglot fleets and zero-trust programs.

But the mesh adds distributed infrastructure to every call. Sidecars consume resources and share workload fate; node/ambient proxies enlarge shared blast radius; control planes distribute privileged policy; interception obscures paths. Latency, retries, failures, and telemetry now arise outside application code.

Responsibility ambiguity is the deeper risk. An API team may assume the mesh handles authorization while the mesh only authenticates workloads. A platform may enable retries that duplicate domain effects. A gateway and mesh may route by different versions. “Transparent” infrastructure hides assumptions until incident or migration.

The right question is not whether a mesh has features. It is whether centralized infrastructure can enforce a clearly bounded cross-cutting invariant better than libraries/gateways/applications, with acceptable cost, failure, ownership, compatibility, and exit.

## Prerequisites and Retrieval

Retrieve [Authentication Context Propagation](033-authentication-context-propagation.md), [Authorization Checks](034-authorization-checks.md), [Object-Level Authorization](046-object-level-authorization.md), [Replay and Request Signing](049-replay-and-request-signing.md), [Deadlines](071-timeout-and-deadline-budgets.md), [Retries and Backoff](072-retries-and-backoff.md), [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), [Load Shedding](074-api-level-load-shedding.md), [Fan-Out and Tail Latency](077-fan-out-and-tail-latency.md), [Preventing Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), [Independent Evolution](090-evolving-an-api-without-coordinated-consumer-releases.md), [Gateway Responsibilities](091-api-gateways-and-edge-responsibilities.md), and [Service Discovery and Routing](092-service-discovery-and-routing.md).

Retrieve service/trust/traffic diagrams; mesh mode/topology/version/support; interception/capture/bypass; control/data-plane identities and trust bundles; workload attestation/credentials; peer/authz policies; gateways/egress; discovery/routes/subsets/locality; client/app/gateway/mesh timeout/retry/circuit/load-balance; protocols/streaming; telemetry/sampling; resource/capacity/latency/cost; config source/revisions/convergence; multicluster/federation/residency; rollout/upgrade/rollback; incident/debug/escape; and non-mesh/legacy workloads.

## Learning Objectives

After completing this module, you can:

1. distinguish mesh data/control plane, sidecar/node/ambient modes, gateways, discovery, application libraries, and service ownership;
2. decide mesh adoption from required invariants, heterogeneity, risk, cost, failure, operability, and exit rather than feature count;
3. define workload identities, trust domains/bundles, attestation, credential rotation, mTLS modes, and peer authorization;
4. preserve end-user/tenant/domain authorization and application semantics beyond workload reachability;
5. verify interception/capture and secure ingress, egress, probes, admin ports, direct IP, DNS, host-network, and legacy paths;
6. compose discovery, routing, canary/mirror/locality, retries, deadlines, circuits, load shedding, and connection pools end to end;
7. measure proxy latency/resource/error/attempt overhead and avoid double-counted or sensitive telemetry;
8. version, validate, stage, converge, roll back, and recover mesh configuration and control/data-plane upgrades;
9. operate multicluster/multinetwork trust/routing/failover without violating identity, version, consistency, or residency; and
10. design incident escape and mesh removal/migration while preserving contracts and security.

## Core Exposition

### Start with invariants, not a product

List problems: unauthenticated east-west traffic, inconsistent certificates, unknown service dependencies, polyglot telemetry, unsafe retries, rollout routing, or egress control. For each, name the exact invariant, threat/failure, current evidence, authoritative owner, and alternatives.

Compare application library/framework, gateway/proxy, network policy, workload identity system, sidecar mesh, node/ambient mesh, or managed service. A mesh is justified when traffic-path enforcement across heterogeneous workloads outweighs added data/control-plane cost and risk.

Set success/guardrail measures: mTLS capture/identity, denied unexpected reachability, reduced credential handling, configuration lead time, incident detection, app code reduction—plus latency tails, CPU/memory, availability, policy errors, toil, cost, and debugging.

Define non-goals explicitly: business authorization, schema compatibility, transaction/idempotency meaning, data consistency, product ownership, and all observability.

### Map topology and responsibility

Draw external gateway/ingress, east-west data planes, waypoint/node/sidecar proxies, egress gateways, discovery, certificate/identity issuers, policy/config management, telemetry collectors, and applications. Mark interception per inbound/outbound/protocol/port.

Gateway owns external client/product protocol/auth/admission/routing. Discovery owns candidate endpoint membership/metadata. Mesh data plane authenticates/encrypts/filters/routes observed workload traffic and reports telemetry. Application owns API/domain semantics, end-user/object authorization, effects/state/consistency/idempotency, and local health/load shedding.

Platform owns mesh availability/security/upgrades/paved configuration/support; service owners own service-specific policy, dependencies, retries/routes, SLO impact, and incident participation. Security owns trust/required controls/risk authority.

Record precedence/composition with libraries and gateways. Two valid policies can interact harmfully; “mesh wins” is not a design.

### Understand data-plane placement

Sidecars localize policy/telemetry and failure/resource impact per workload but multiply processes/upgrades and share pod lifecycle. Node/ambient approaches reduce per-workload lifecycle burden but share fate/trust/resources across workloads and may require waypoint/L7 components.

Explicit proxies make participation visible but require application integration. Transparent interception eases adoption but has kernel/network/DNS/protocol exceptions and can hide bypass.

Choose topology by required L4 versus L7 policy, identity, tenancy/isolation, platform support, workload types, performance, failure containment, and operations. Istio currently documents sidecar and ambient data-plane modes; vendor topology is not an invariant.

Test mixed modes during migration. Traffic may be plaintext, singly proxied, doubly proxied, or bypassed depending direction and versions.

### Establish workload identity and trust domains

Issue identity from attested workload attributes under an owned trust domain, not IP/namespace alone. SPIFFE specifies workload identity concepts/identifiers and related standards; adopting a URI format does not by itself establish trustworthy attestation or authorization.

Define trust domain, federation, selectors/attestors, issuer/root/intermediate, key protection, credential lifetime/rotation/overlap/revocation, clock behavior, and workload API delivery. Bind identity to service/account/deployment/environment as policy needs, avoiding ephemeral instance attributes in stable policy.

At connection, verify chain/trust bundle, peer identity, service audience/expected SAN, time, policy, and destination. A valid identity from wrong trust domain/service remains unauthorized.

Federation expands trust blast radius. Map identities deliberately; do not treat same name across clusters/organizations as same principal.

### Roll out mTLS without silent downgrade

Inventory plaintext/mTLS paths, ports, protocols, headless/direct-IP/host-network/VM/external/legacy traffic, gateways, probes, and bypass. Measure actual peer identities and encryption, not configuration intent.

Migration may begin permissive to support mixed workloads, but permissive mode has owner, scope, telemetry, deadline, and contraction gate. Deploy identity/proxies, verify connectivity and policy, narrow plaintext, then enforce strict mTLS. Unknown/unmeshed traffic fails as designed.

Avoid fallback from failed mTLS to plaintext unless explicitly bounded for migration. An attacker must not trigger downgrade. Protect control/telemetry traffic too.

TLS termination/re-encryption across gateway/mesh hops changes peer identity. Preserve external user context separately and authenticate each workload hop.

### Authorize workload reachability, not business actions

Mesh policy can allow workload A to reach service B/port/method/path when reliably parsed. Default-deny plus explicit service identities reduces lateral movement. Keep selectors stable, reviewed, tenant/environment scoped, and test negative paths.

The service still validates end-user/tenant context and current action/object/property/state authorization. Workload `checkout` may call payments but cannot authorize arbitrary card/amount/user.

Do not base high-risk policy solely on spoofable headers unless the mesh/gateway strips, validates, and protects them. L7 parsing limitations/protocol upgrades/encryption affect enforcement.

NIST SP 800-207 states that network location/ownership does not grant implicit trust and focuses protection on resources. Mesh mTLS is one mechanism within a broader zero-trust architecture, not the architecture itself.

### Verify capture and prevent bypass

Enumerate inbound/outbound, loopback, direct IP, DNS, alternate interfaces, host network, privileged workloads, init/startup race, UDP, unsupported protocols, tunnels, egress, admin/probe, and failure paths. Confirm which are intentionally captured/exempt.

Use network policy/firewall/routing/workload permissions so bypass cannot reach protected service without equivalent identity/policy. Receiving services listen/accept only through intended boundary where feasible.

Capture configuration is versioned/tested. A proxy crash or unavailable node component must not silently open direct plaintext; fail-open/closed follows risk and availability policy.

Monitor plaintext, unknown identity, bypass, policy shadow/deny, and traffic not represented in expected mesh telemetry. Absence of telemetry is not proof of no traffic.

### Compose discovery and traffic routing

Mesh consumes discovery or distributes endpoints/routes through its control plane. Preserve service identity, endpoint workload identity, readiness/drain, version/capability, tenant/environment, locality, shard/leader, and policy metadata.

Traffic splitting/canary must exclude incompatible version pairs and preserve stable cohort identity. Percentage is expected request share, not consumer migration. Routing by headers requires trusted/protected source and cache/security analysis.

Mirroring/shadowing must suppress effects/credentials/sensitive data or use safe synthetic/recorded inputs. Duplicating a live payment or webhook is not observability.

Locality/failover cannot override residency, consistency, capacity, version, or authorization. Endpoint/service verifies shard/ownership/epoch and domain invariants.

### Budget timeouts and retries once

Inventory client library, application, gateway, sidecar/node/waypoint, and service retries/timeouts. Mesh defaults are contract-affecting. Propagate deadline/cancellation and reserve proxy/network/application margins.

If client, mesh, and service each retry once, simplified maximum attempts is $2^3=8$ before fan-out/hedging. Assign retry owner per operation; disable redundant layers. Mesh often lacks domain effect/idempotency knowledge.

Retry only safe/idempotent or idempotency-key-protected replayable requests on scoped transient conditions within deadline/budget/backoff/jitter. Avoid retrying overload and ambiguous partial response/effect.

Long streams require idle/connection/max-duration semantics distinct from request timeout. Proxy drain/upgrade must preserve/cancel streams predictably.

### Compose circuits, outlier detection, and load shedding

Per-proxy outlier/circuit state is local and fragmented; global policy can overreact. Scope failures by endpoint/service/operation/locality/caller and distinguish network, caller input, downstream, overload, and proxy errors.

Ejection raises survivor load; cap it, require evidence, slow-start re-entry, and maintain headroom. A downstream database outage can make all service endpoints fail—endpoint roulette worsens it.

Services still enforce local concurrency/admission/load shedding from real resource state. Mesh connection/request limits protect transport and callers but cannot know business priority fully.

Observe retry/ejection/circuit interaction. A mesh can turn a partial latency event into a synchronized outage if every proxy makes the same delayed decision.

### Preserve protocol and application behavior

Define supported HTTP versions, gRPC, TCP, streaming, WebSocket, upgrades, trailers, cancellation, server push if relevant, keepalive, DNS, and opaque traffic. Protocol detection/sniffing must not misclassify bytes or change security policy.

Proxies preserve method/path/authority/headers/body/status/trailers and do not normalize inconsistently with gateway/service/signatures. Request/response limits and buffering/backpressure fit streaming.

L7 routing/telemetry is unavailable for opaque/encrypted protocols unless termination occurs; do not claim method-level policy then. L4 identity/reachability can still apply.

Test generated clients, large/streaming bodies, cancellation/deadline, half-close, connection reuse, upgrades, malformed/duplicate metadata, and proxy version skew.

### Build trustworthy telemetry

Mesh supplies connection/request/response/attempt telemetry because it observes transport, but not necessarily logical operation, domain effect, end-user, or correct outcome. Join with application instrumentation and trusted context.

OpenTelemetry HTTP conventions distinguish client/server spans and retries/redirects. With two proxies, naïve instrumentation can create several spans/metrics for one call; model hops and attempts deliberately and avoid double-counting request volume/latency.

Record mesh/control/data-plane revision, source/destination workload identity/service, route/subset/locality, peer auth/mTLS mode, policy decision, attempts, proxy/upstream error, latency phases, sizes, connection reuse/ejection—using bounded cardinality and privacy controls.

Never log tokens, cookies, full sensitive headers/bodies, or uncontrolled identities. Sampling/drop/exporter failure can erase rare/bypass evidence; expose telemetry health.

### Account for latency, resources, and capacity

Measure application baseline and each proxy/hop overhead across p50/p95/p99, connections, streaming, payloads, TLS handshakes/resumption, policy complexity, telemetry, and failure. Average microbenchmarks do not predict tail under contention.

Sidecars need CPU/memory/file descriptors/connections/ephemeral storage and startup/drain resources; starvation causes application-visible failure. Node/ambient components need per-node capacity/isolation so one workload cannot exhaust neighbors.

Proxy autoscaling/capacity includes connection and stream count, encryption, filters, route clusters, logs/traces, control-plane updates, and failover. Telemetry backpressure must not exhaust data plane.

Charge/show mesh cost without encouraging bypass. Attribute shared platform cost and consumer/service benefit transparently.

### Engineer the control plane and configuration

Treat identity, trust bundles, peer auth, authorization, routes, subsets, destinations, retries/timeouts/circuits, telemetry, egress, and gateways as versioned owned policy. Validate selector/reference closure, conflicts, shadowing, unsafe wildcard, bypass, retry safety, timeout bounds, protocol match, and tenancy.

xDS is one current dynamic-resource mechanism. Whatever protocol, data planes validate, ACK/NACK, retain atomic last-known-good, expose revision/age/convergence, and handle partial/stale/unknown resources safely.

Control-plane outage should normally stop new config/identity operations while existing data plane serves bounded known-good; credential expiry/revocation and stale policy limits are explicit. Empty or permissive fallback is unsafe.

Partition control planes and blast radius by environment/region/tenant/risk where justified. Back up/restore policy/source/ownership/trust/keys/audit and rebuild ephemeral proxies/endpoints from authoritative state.

### Upgrade and migrate data-plane modes safely

Build compatibility matrix among application/protocol, old/new proxy, old/new control plane/config schema, gateway, discovery, identity, and peer. Rolling upgrade creates mixed proxy pairs; test mTLS/ALPN/protocol/policy/telemetry.

Stage control plane then data plane according to supported skew, canary low-risk workloads, observe, expand by cell, and keep rollback. Certificate/trust rotation overlaps valid chains and tests old/new peers.

Sidecar-to-ambient or vendor migration changes capture, identity delivery, L7 waypoint, policy semantics, telemetry, resources, failure, and bypass. Run equivalence/security tests rather than translate config names blindly.

Remove old mode only after every workload/path—including jobs, VMs, host network, DR, gateways, egress, and support tools—is migrated or explicitly excepted.

### Handle multicluster, egress, and external services

Multicluster identity/federation defines trust-domain mapping, discovery, network gateways, service naming, locality/failover, config ownership, and policy. Same service name does not guarantee same owner/version/data.

Cross-cluster/region routing preserves residency, consistency, capacity, encryption, version/capability, and failure isolation. Exercise partition and stale control/discovery views.

Egress policy controls destinations/identity/TLS/DNS/ports and provides audit, but arbitrary external API semantics, credentials, SSRF protection, retries, and data governance still need application/gateway controls. Avoid universal egress proxy as hidden business integration layer.

External/legacy workloads get explicit identities/adapters/gateways or remain outside with equivalent controls; never label their source network as trusted workload identity.

### Operate incidents, escape, and lifecycle

Runbooks distinguish app, proxy, node, control plane, identity/cert, discovery, policy, route, upstream, and telemetry failure. Provide safe inspection of effective config, certificates/identity, route/cluster/endpoints, policy trace, and connection stats without secrets.

Emergency controls—deny, drain, route, retry disable, policy rollback, capture bypass—are scoped, authenticated, audited, tested, and expiring. A bypass that removes mTLS/auth cannot be the default incident fix; use equivalent protected escape only when designed.

Assign platform SLO/support and service policy ownership. Measure control/data-plane availability, config convergence/rejection, identity issuance/rotation, mTLS/plaintext/bypass, latency/resource overhead, policy denies, retry/ejection, and incidents.

Temporary routes, permissive auth, aliases, telemetry filters, and exceptions have removal gates. Maintain an exit plan: application contracts/identity semantics independent enough to move libraries/proxies/vendors or remove mesh without breaking APIs.

## Definitions and Notation

Let $k$ proxy hops contribute latency $L_{proxy,i}$; total observed path latency is application plus proxies plus network, acknowledging overlap/measurement-boundary details. Let each retrying layer $i$ permit $r_i\ge0$ retries; simplified maximum attempts is $A\le\prod_i(r_i+1)$ before fan-out/hedging.

Let $C$ be capture completeness, $I$ workload identity validity, $P$ policy correctness, $S$ protocol-semantic preservation, $B$ bounded resilience/resources, and $O$ observable/config-converged operation. These are necessary mesh-layer conditions, not sufficient application correctness.

A **trust bundle** contains verification authorities for a trust domain/federation. **Permissive mTLS** accepts plaintext and mTLS during bounded migration. **Waypoint** denotes an L7 proxy associated with selected traffic/workloads in some ambient architectures; exact implementation is product-specific.

## Mechanisms, Invariants, or Proof Structure

**Layer-boundary argument.** Workload identity establishes which service made a connection. Two users through the same workload can have different rights to the same object. Therefore mesh peer authorization cannot entail end-user/object/action authorization; application context and domain state remain necessary.

**Retry multiplication.** Client, mesh, and service each allowing one retry yields $(1+1)^3=8$ attempts for one logical call. Individually reasonable policies compose multiplicatively, so retry ownership/budget must be end to end.

**Capture counterexample.** Policy denies direct A→B through proxy, but B also listens on a reachable un-intercepted interface. A connects directly and bypasses identity/policy. Therefore configured proxy policy is insufficient without capture/bypass evidence or equivalent service/network enforcement.

**Latency decomposition.** Adding proxies cannot have negative processing/resource cost; even when pipelining overlaps components, each adds potential queueing/failure/tail variance. Therefore mesh performance must be measured end to end and per hop under representative load, not assumed transparent.

Operational invariants are: invariants/non-goals explicit; topology/capture known; workload identity attested/verified; mTLS downgrade controlled; domain auth retained; discovery/routing policy compatible; retries/deadlines/circuits owned end to end; protocols preserved; telemetry hop-aware/minimized; capacity isolated; config last-known-good/convergent; upgrades matrix-tested; multicluster policy bounded; incident escape protected; and mesh removable.

## Alternatives and Trade-Offs

Sidecars maximize per-workload isolation/L7 locality but add lifecycle/resource count. Node/ambient modes reduce app coupling but enlarge shared blast radius and may add waypoint complexity. Choose by isolation, protocol/policy, operations, and capacity—not fashion.

Libraries provide semantic context/performance but require language adoption/upgrades. Mesh provides polyglot enforcement but lacks domain meaning. Combine narrowly and prevent duplicate retries/telemetry/config.

Strict mTLS/default-deny improves containment but can break unknown/legacy paths. Permissive migration preserves availability but permits downgrade/plaintext. Make it observable, scoped, dated, and contract toward strict.

L7 policy/routing enables operation awareness but requires termination/parsing and increases coupling/privacy/CPU. L4 identity/reachability is simpler and protocol-agnostic but coarser. Keep domain authorization in application either way.

Central control plane gives consistency but broad blast radius. Federated/tenant control planes improve isolation/autonomy but complicate policy/trust. Partition ownership while maintaining common identity/interoperability rules.

Rich automatic telemetry accelerates diagnosis but creates cost/cardinality/privacy and duplicate spans. Instrument the minimum useful transport evidence and join application effects selectively.

## Failure Modes and Misconceptions

- “Mesh means zero trust.” It supplies mechanisms within a broader identity/resource policy architecture.
- “mTLS means request authorized.” It authenticates/encrypts workload transport.
- “Namespace is identity.” Identity needs attestation and verified trust domain.
- “All traffic is captured.” Direct IP, host network, startup, protocol, and bypass paths need evidence.
- “Transparent means no application impact.” Latency, retries, errors, drains, and protocols change.
- “Mesh replaces gateway.” External client/product/edge responsibilities differ.
- “Mesh replaces discovery.” It consumes/distributes endpoint information and still faces staleness.
- “Retry defaults improve reliability.” Layered retries amplify and can duplicate effects.
- “Outlier ejection removes bad instances.” Failure scope and survivor overload can make it harmful.
- “Traffic split proves consumer migration.” Requests are not consumers or semantic compatibility.
- “Mirror is read-only.” Mirrored downstream may still cause effects/data exposure.
- “Proxy telemetry is end-to-end truth.” It observes transport attempts, not business effects.
- “Control plane is off-path.” Its configuration/identity shapes every data-plane decision.
- “Permissive mode is harmless.” It is a downgrade/bypass window.
- “More policy in mesh is better.” Domain logic in infrastructure becomes hidden coupling.
- “Mesh adoption is irreversible.” Lack of an exit plan is an architecture failure.

## Worked Examples

### Example 1

Mesh authenticates `checkout` workload to payments. Payments still checks end-user, tenant, card, amount, state, and idempotency before effect.

### Example 2

Client, sidecar, and service each retry once. One logical call can produce eight attempts; mesh retry is disabled for the payment operation.

### Example 3

Strict policy exists, but service host port is directly reachable outside interception. Network/service listener controls close the bypass before claiming enforcement.

### Example 4

Permissive mTLS migration shows 2% plaintext from legacy jobs. Jobs receive workload identities and tests; strict mode waits until authorized exceptions close.

### Example 5

Five-percent canary routing sends a new-only request to old endpoint. Discovery/version eligibility is added before percentage splitting.

### Example 6

Mirrored checkout request triggers notification in shadow backend. Mirroring is replaced with sanitized recorded input and effect-suppressed environment.

### Example 7

Endpoint latency causes every sidecar to eject it; survivors overload. Ejection cap, evidence scope, slow re-entry, and service load shedding stabilize the fleet.

### Example 8

Control-plane update is invalid. Data planes NACK and retain last-known-good revision; convergence alert prevents partial permissive fallback.

### Example 9

Sidecar CPU starvation raises application p99 although app code is idle. Resource reservations, proxy telemetry, and capacity tests expose the shared fate.

### Example 10

Sidecar-to-ambient migration leaves host-network support tool unmeshed. Capture inventory and DR rehearsal block old-mode removal until equivalent controls exist.

## Cross-Program Connections

[Network Engineering](../../24-network-engineering/ROADMAP.md) supplies TLS, proxies, interception, routing, connection behavior, DNS, load balancing, and packet/flow diagnosis.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies zero trust, workload identity, PKI, attestation, mTLS, least privilege, policy, bypass analysis, key rotation, and incident response.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies discovery, retries/deadlines, failure detectors, load balancing, partitions, configuration consistency, multiregion state, and recovery.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies mesh product ownership, control planes, identity integration, policy-as-code, tenancy, upgrades, telemetry, self-service, support, and cost.

[Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies clusters/networks/regions, certificate/key services, autoscaling, resource isolation, gateways, multicloud connectivity, and disaster recovery.

## References

1. Istio, [The Istio Service Mesh](https://istio.io/latest/about/service-mesh/).
2. Istio, [Architecture](https://istio.io/latest/docs/ops/deployment/architecture/).
3. Linkerd, [Architecture](https://linkerd.io/2-edge/reference/architecture/).
4. SPIFFE, [SPIFFE Standard](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE.md).
5. Envoy, [xDS REST and gRPC Protocol](https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol).
6. OpenTelemetry, [Semantic Conventions for HTTP Spans](https://opentelemetry.io/docs/specs/semconv/http/http-spans/).
7. NIST, [SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final).

## Exercises

### Exercise 1

Create a responsibility matrix for internet gateway, service mesh, discovery, identity provider, platform, checkout, and payments. Cover external/end-user/workload identity, routing, authorization, retries, telemetry, policy, incidents, and SLOs.

### Exercise 2

Design migration from plaintext mixed services to strict workload mTLS/default-deny across sidecars, VMs, jobs, host-network tools, gateways, and disaster recovery without silent downgrade.

### Exercise 3

A client, gateway, mesh, and service permit 1, 0, 2, and 1 retries. Compute simplified maximum attempts and redesign ownership for a non-idempotent order operation.

### Exercise 4

Plan a sidecar-to-ambient mesh migration across old/new control/data planes, L4 and L7 policy, workload identity, telemetry, canary routing, multicluster failover, and rollback.

### Exercise 5

Diagnose an incident with mesh p99 latency, proxy CPU saturation, outlier-ejection cascade, stale discovery, partial control-plane convergence, duplicate traces, and reports that direct traffic bypassed policy. Define stabilization and durable verification.

## Answers to the Exercises

### Answer 1

Gateway owns external TLS/protocol, client credential validation, protected end-user/tenant context, edge admission/quota, public version/route and edge telemetry. Identity provider/workload issuer owns credentials, trust bundles, attestation, rotation. Discovery owns eligible endpoint membership/version/locality/readiness. Mesh owns captured service-to-service mTLS/workload peer auth, coarse workload reachability, eligible routing consumption, bounded transport resilience, hop telemetry and config enforcement. Checkout/payments services own API/domain semantics, propagated user validation, action/object/property/state authorization, idempotency/effects, consistency, local load shedding and business telemetry; payments is authoritative for charge. Platform owns mesh/gateway/discovery capability SLO/security/upgrades/support, while service owners own route/retry/policy/SLO impact. Incident command coordinates; specialists retain authority. Explicitly map bypass, config source, retry/deadline budget, generated errors, SLO measurement and escalation; no layer infers another’s success.

### Answer 2

Inventory every source/destination/port/protocol and actual plaintext/mTLS identity, including direct IP, loopback, VMs, batch jobs, host network, probes/admin, ingress/egress, failover and DR. Establish owned trust domains/attestation, short-lived credentials/rotation overlap and endpoint peer verification. Deploy proxies/identity to receivers and senders in compatibility-tested cohorts; permissive mode is scoped with plaintext telemetry, owner, expiry and deny target. Add workload allow policies from observed/declared dependencies, negative tests, and network/listener enforcement that prevents bypass. Migrate VMs/jobs/tools through supported workload identity/gateway or explicit equivalent control. Rehearse DR and key/control-plane outage. Move service by service to strict mTLS/default deny only after all paths/versions, readiness/drain, telemetry and rollback pass. Never fall back to plaintext after failed handshake. Remove permissive exceptions and old credentials/routes after full cadence/recovery evidence.

### Answer 3

The simplified bound is $(1+1)(0+1)(2+1)(1+1)=2\times1\times3\times2=12$ attempts before hedging/fan-out. For a non-idempotent order, require client-scoped idempotency key, canonical request fingerprint, durable atomic effect/result/deduplication, conflict/retention and outcome lookup. Assign retry to the client for ambiguous transport failure within end-to-end deadline, or one informed layer; disable gateway/mesh whole-call retries. Service may retry internal transient dependencies only before/under effect boundary and remaining budget. Propagate deadline/cancellation, bound attempts/backoff/jitter, avoid overload retries, preserve replayable body, and classify pre-send versus post-send ambiguity. Count logical order, attempts, dedupe hits and effects separately; test response loss after commit, proxy restart/drain, partial data/control-plane failure and retry storms.

### Answer 4

Inventory capture/policy/identity/routes/protocols and build old/new control plane × sidecar/ambient/waypoint × gateway/discovery/application compatibility matrix. Define invariant equivalence for mTLS identity, L4 reachability, L7 method/path policy, retries/timeouts, routes/canaries, telemetry, bypass, egress and failure. Upgrade/stage supported control plane, introduce ambient L4 to canary workloads while sidecars coexist, then waypoints only where L7 is required; ensure double capture/proxy loops and policy precedence are impossible. Test workload credential/trust rotation, mixed peers, protocols/streams, version subsets, multicluster identity/discovery/residency/failover, latency/resources and control outage. Observe effective revision, mTLS/plaintext, denies, routes, attempts and trace topology. Roll back cohort without removing compatibility needed by already-migrated peers. Migrate jobs/VMs/host network/DR, close exceptions, remove sidecars/webhooks/config/resources only after evidence.

### Answer 5

Stabilize by freezing control updates at known-good, disabling mesh retries/outlier ejection or capping/scoping them, shedding load at services, restoring proxy CPU/memory/connection headroom, and preventing cross-zone retry amplification. Keep nonnegotiable auth/consistency; do not open direct bypass. Compare revisions/ACK-NACK/convergence, discovery age/endpoints, proxy/application latency phases, CPU/throttling/queues, attempts/ejections, and network/dependency errors. Quarantine divergent cells and roll back config/data-plane canary atomically. Verify bypass via flow/network/listener/capture evidence and close with network/service enforcement. Fix duplicate trace instrumentation/attempt modeling without losing audit. Durable work: resource reservations/load tests, retry owner/deadline, ejection evidence/caps/slow re-entry, discovery last-known-good bounds, atomic referenced config, convergence gates, capture tests, direct-path denial, telemetry health/cardinality, multiversion fault tests, runbooks and safe authenticated escape.
