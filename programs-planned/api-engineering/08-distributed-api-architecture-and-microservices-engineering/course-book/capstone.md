# Capstone — Distributed API Architecture and Microservices Engineering

## Cumulative system

Course 8 continues the Analysis Runs Platform at the point where the previous course stopped. Its capstone exists to distribute ownership deliberately while preserving the same projects, datasets, runs, artifacts, identities, and user journeys.

## Inherited state

The Course 7 platform with governed HTTP, event, and RPC interfaces and migration history through 015.

The inherited boundary is read-only: The Course 7 platform with governed HTTP, event, and RPC interfaces and migration history through 015. A difficult implementation is not permission to rewrite predecessor contracts, migrations, profiles, or evidence; the current course must solve the problem at its own owning layer.

## Course additions

- distribution economics and boundary fitness functions;
- service, contract, and data ownership;
- cross-service queries, projections, dependency budgets, and sagas;
- workload identity, routing, version skew, and release choreography;
- fault verification, strangler extraction, rollback, decommission, and merge-back;

## Increment map

| Module | Mechanism | Cumulative result |
|---:|---|---|
| 1 | Distribution Economics, Boundary Evidence, and Architecture Fitness Functions | Publish a measured boundary scorecard that approves Notification Delivery for first extraction, approves Artifact Delivery conditionally, keeps Analysis Control cohesive, and rejects table-shaped services. |
| 2 | Service Boundaries, Bounded Contexts, and Contract Ownership | Publish the service catalogue, bounded-context map, contract ownership map, and explicit list of capabilities that remain inside Analysis Control. |
| 3 | Data Ownership, Replication, and Cross-Service Query Design | Split authoritative data ownership, build versioned projections for cross-service reads, define staleness budgets, and prove reconciliation for missing, duplicate, and out-of-order updates. |
| 4 | Synchronous Collaboration, API Composition, and Dependency Budgets | Publish an acyclic synchronous dependency graph, one edge-owned deadline budget, bounded fan-out rules, and a gateway composition path that degrades truthfully. |
| 5 | Distributed Workflows, Sagas, Compensation, and Process Managers | Implement the artifact-publication and run-completion saga with durable step identity, semantic locks, compensation, timeout handling, and operator-visible reconciliation. |
| 6 | Service Identity, Authorization, and Trust Propagation | Introduce workload identities, audience-bound service credentials, delegated user context, short-lived artifact capabilities, and explicit authorization at every trust boundary. |
| 7 | Discovery, Routing, Gateways, and Traffic Topology | Implement service registration, health-aware routing, gateway edge policy, bounded traffic shifting, and an optional Kubernetes topology with explicit ownership of each routing decision. |
| 8 | Deployment Independence, Version Skew, and Release Choreography | Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence. |
| 9 | Distributed Verification, Fault Injection, and Operability | Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects. |
| 10 | Incremental Extraction, Strangler Migration, and Final Architecture Defense | Extract Notification Delivery and Artifact Delivery through shadow, compare, backfill, cutover, and decommission phases; retain Analysis Control; and publish the Course 9 graph-access handoff. |

## Implementation route

Build the complete Course 8 increment in one primary track. Use the second track only after the chapter model is clear, then run shared vectors to test whether **distribute ownership deliberately** survives an idiomatic implementation in another runtime.

## Final state

Distributed Architecture Profile 1.0, explicit service and data ownership, versioned projections, saga and trust policies, independent release choreography, extraction evidence, and a GraphQL boundary brief.

## Handoff discipline

The successor receives only the settled result: Distributed Architecture Profile 1.0, explicit service and data ownership, versioned projections, saga and trust policies, independent release choreography, extraction evidence, and a GraphQL boundary brief. Local caches, secrets, ad-hoc reports, and environment-specific artifacts remain outside the handoff.
