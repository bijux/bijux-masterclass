# Distributed API Architecture and Microservices Engineering

**Course 8 of 10 — Distribute ownership deliberately**

## Course promise

Use ownership and failure evidence to approve, reject, extract, operate, and reverse service boundaries without creating a distributed monolith.

> **Governing question:** When does a remote service boundary create more value than the coordination, latency, consistency, security, release, and operational costs it introduces?

## Place in the program

**Incoming boundary:** The Course 7 platform with governed HTTP, event, and RPC interfaces and migration history through 015.

**Outgoing boundary:** Distributed Architecture Profile 1.0, explicit service and data ownership, versioned projections, saga and trust policies, independent release choreography, extraction evidence, and a GraphQL boundary brief.

Course 8 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the distribute ownership deliberately mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- distribution economics and boundary fitness functions;
- service, contract, and data ownership;
- cross-service queries, projections, dependency budgets, and sagas;
- workload identity, routing, version skew, and release choreography;
- fault verification, strangler extraction, rollback, decommission, and merge-back;

## Course-level learning outcomes

- Treat distribution as an economic and organizational decision rather than a maturity badge.
- Identify capabilities, invariants, and ubiquitous language that belong together.
- Enforce one authoritative writer for each business fact.
- Model the complete synchronous dependency graph and detect cycles.
- Distinguish local ACID transactions from distributed workflow guarantees.
- Separate workload identity, end-user identity, tenant context, and delegated authority.
- Distinguish service identity from instance address and endpoint health.
- Distinguish independent deployment from independent change and ownership.
- Separate service unit tests, contract tests, topology tests, and end-to-end outcome proofs.
- Sequence extraction from low-coupling evidence rather than organizational pressure.

## Module map

| Day | Chapter | Governing question | Capstone increment |
|---:|---|---|---|
| 1 | [Distribution Economics, Boundary Evidence, and Architecture Fitness Functions](module-01-distribution-economics-and-boundary-evidence/index.md) | When does a remote service boundary create more value than the coordination, latency, failure, and operational costs it introduces? | Publish a measured boundary scorecard that approves Notification Delivery for first extraction, approves Artifact Delivery conditionally, keeps Analysis Control cohesive, and rejects table-shaped services. |
| 2 | [Service Boundaries, Bounded Contexts, and Contract Ownership](module-02-service-boundaries-and-contract-ownership/index.md) | How do we draw service boundaries around cohesive decisions and language without turning tables, classes, or teams into accidental services? | Publish the service catalogue, bounded-context map, contract ownership map, and explicit list of capabilities that remain inside Analysis Control. |
| 3 | [Data Ownership, Replication, and Cross-Service Query Design](module-03-data-ownership-replication-and-cross-service-queries/index.md) | How can each service own its writes while the system still answers cross-capability questions without shared tables or hidden distributed transactions? | Split authoritative data ownership, build versioned projections for cross-service reads, define staleness budgets, and prove reconciliation for missing, duplicate, and out-of-order updates. |
| 4 | [Synchronous Collaboration, API Composition, and Dependency Budgets](module-04-synchronous-collaboration-and-dependency-budgets/index.md) | How do we keep synchronous service collaboration bounded so that fan-out, retries, and version skew do not make the public request path fragile? | Publish an acyclic synchronous dependency graph, one edge-owned deadline budget, bounded fan-out rules, and a gateway composition path that degrades truthfully. |
| 5 | [Distributed Workflows, Sagas, Compensation, and Process Managers](module-05-distributed-workflows-sagas-and-compensation/index.md) | How do we preserve business intent when one workflow crosses services that cannot share a transaction? | Implement the artifact-publication and run-completion saga with durable step identity, semantic locks, compensation, timeout handling, and operator-visible reconciliation. |
| 6 | [Service Identity, Authorization, and Trust Propagation](module-06-service-identity-authorization-and-trust-propagation/index.md) | How do services authenticate workloads, preserve end-user intent, and avoid confused-deputy failures without trusting caller-supplied identity headers? | Introduce workload identities, audience-bound service credentials, delegated user context, short-lived artifact capabilities, and explicit authorization at every trust boundary. |
| 7 | [Discovery, Routing, Gateways, and Traffic Topology](module-07-discovery-routing-gateways-and-traffic-topology/index.md) | How do callers find healthy service instances and route traffic without moving business ownership into gateways or creating several competing retry layers? | Implement service registration, health-aware routing, gateway edge policy, bounded traffic shifting, and an optional Kubernetes topology with explicit ownership of each routing decision. |
| 8 | [Deployment Independence, Version Skew, and Release Choreography](module-08-deployment-independence-version-skew-and-release-choreography/index.md) | How can services release independently while old and new clients, events, schemas, and database migrations coexist safely? | Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence. |
| 9 | [Distributed Verification, Fault Injection, and Operability](module-09-distributed-verification-fault-injection-and-operability/index.md) | How do we prove system behavior when individual services pass their tests but network partitions, version skew, and cross-service timing still create failures? | Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects. |
| 10 | [Incremental Extraction, Strangler Migration, and Final Architecture Defense](module-10-incremental-extraction-migration-and-final-defense/index.md) | How do we extract services incrementally, preserve every existing contract, and retain a safe path to stop, roll back, or merge a service back into the platform? | Extract Notification Delivery and Artifact Delivery through shadow, compare, backfill, cutover, and decommission phases; retain Analysis Control; and publish the Course 9 graph-access handoff. |

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- service-per-table decomposition;
- shared-database microservices;
- gateway-owned business workflows;
- distribution as a maturity badge;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 8, read each chapter around the question **When does a remote service boundary create more value than the coordination, latency, consistency, security, release, and operational costs it introduces?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
