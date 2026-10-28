# Worked Answers — Module 07: Discovery, Routing, Gateways, and Traffic Topology

Use these solutions to audit your reasoning for **Discovery, Routing, Gateways, and Traffic Topology**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What is the difference between service discovery and load balancing?

Discovery yields eligible endpoints and metadata. Load balancing chooses among them. Neither decides business semantics.

**Decisive evidence:** registry selection trace

The chapter’s decisive distinction is this: A control-plane outage should not instantly erase all data-plane knowledge. Conversely, stale configuration needs an expiry or refresh policy. These trade-offs are visible in DNS, client-side discovery, proxies, gateways, and service meshes.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 2. Why should draining instances be removed from new traffic before process exit?

They need time to finish accepted requests and streams without receiving additional work. Liveness alone cannot express this state.

**Decisive evidence:** lifecycle routing test

In the cumulative capstone, the rule becomes concrete: Hard-coding instance addresses couples callers to deployment. Treating a DNS answer as health can send work to a process that is alive but draining. Treating liveness as readiness can restart a healthy process because a dependency is temporarily unavailable.

## 3. What belongs in the edge gateway?

Public TLS, credential normalization, request budgets, protocol adaptation, routing, bounded composition, and public error translation—not domain transitions or private database access.

**Decisive evidence:** gateway responsibility audit

A useful way to reason about the boundary is: Suppose the public client retries once, the gateway retries twice, a sidecar retries twice, and the gRPC library retries twice. One user attempt can become 18 service attempts. Select one owner per edge and make attempt count visible.

## 4. Why is one retry layer per edge important?

Multiple transparent layers multiply attempts and hide load. One accountable layer can apply idempotency, deadline, and observability correctly.

**Decisive evidence:** retry amplification test

The implementation consequence is: A proxy or mesh may support retries, but it lacks full application knowledge. Use infrastructure retries only for narrowly classified safe cases, such as connection establishment before any request bytes were accepted, and align them with the caller’s retry budget.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 5. How should a canary key be chosen?

Use a stable key such as tenant or resource when consistency matters, so the same flow does not bounce unpredictably between versions.

**Decisive evidence:** deterministic canary vector

The important nuance is: Both tracks implement health-aware version-filtered routing. The deterministic round-robin behavior supports shared tests. A real platform may use locality, least request, or adaptive algorithms, but those choices are only valid after eligibility and correctness.

**Evidence.** Execute legacy, shadow, canary, cutover, rollback, and decommission states while checking mixed-version compatibility, divergence, and data ownership.

## 6. Why can shadowing a write be dangerous?

The candidate may create duplicate or external effects. Writes need dry-run, effect suppression, or shared stable identity and comparison without authority.

**Decisive evidence:** shadow side-effect policy

Under concurrency or failure, the distinction becomes: Shadowing is useful only when side effects are controlled. Reads can often shadow directly. Writes need a simulation, dry-run, idempotent duplicate identity, or candidate path that records comparison without producing external effects.

**Evidence.** Execute legacy, shadow, canary, cutover, rollback, and decommission states while checking mixed-version compatibility, divergence, and data ownership.

## 7. What does a service mesh not know?

Business idempotency, resource ownership, compensation semantics, authoritative state, and whether a retry after commit is safe.

**Decisive evidence:** mesh/application responsibility matrix

The design remains honest only if: A mesh can provide workload mTLS, routing, telemetry, and some resilience policy. It does not know whether CompleteRun is idempotent, whether an artifact belongs to a tenant, or whether a compensation is semantically valid. The course treats a mesh as optional infrastructure whose policy must align with application ownership.

## 8. When should an unhealthy instance remain live?

A process may be live for diagnostics and graceful recovery while not ready or accepting business traffic. Restarting it may make recovery worse.

**Decisive evidence:** liveness/readiness/drain evidence

The consumer-facing consequence is: These graphs are not identical. A gateway may be on the network path without being a semantic dependency. A broker may carry events without appearing on a synchronous request path. A mesh sidecar may be a network hop but not a business service.

## 9. Why filter instances by supported version before balancing?

Routing to a healthy but incompatible provider creates semantic failure. Eligibility includes contract compatibility.

**Decisive evidence:** version-aware routing test

The operational consequence is: The course treats a mesh as an optional platform mechanism. The dependency graph and service contracts remain authoritative. An architecture that only works because the mesh retries every failure is not well designed.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 10. What is wrong with gateway-to-database access for fast composition?

It bypasses service ownership, couples schemas, weakens authorization, and prevents independent evolution.

**Decisive evidence:** data access audit

The strongest engineering interpretation is: The Notification extraction can replay events into a shadow consumer because delivery side effects are disabled. The Artifact extraction shadows reads and compares bytes, checksum, metadata, authorization, and latency before write ownership changes.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 11. How is failover different from retry?

Failover selects another eligible instance or region; retry repeats an operation. Both still require one deadline and safe effect semantics.

**Decisive evidence:** routing and retry ownership trace

The defect-oriented view is: A service name may resolve to changing endpoints. Long-lived HTTP/2 or gRPC channels can continue using an endpoint after DNS changes unless the client or proxy refreshes and reconnects. Very short connection lifetimes can increase handshake cost and reduce efficiency.

## 12. Why does DNS stability not prove application readiness?

DNS maps names to addresses; it can outlive process readiness or include endpoints whose business dependencies are unavailable.

**Decisive evidence:** health observation test

Across the Python and TypeScript tracks, the invariant is: Hard-coding instance addresses couples callers to deployment. Treating a DNS answer as health can send work to a process that is alive but draining. Treating liveness as readiness can restart a healthy process because a dependency is temporarily unavailable.
