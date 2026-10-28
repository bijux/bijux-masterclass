# Two-Week Study Plan — Distributed API Architecture and Microservices Engineering

## Rhythm

Course 8 uses ten teaching days over two weeks. Orientation freezes the incoming boundary before Day 1; each day moves from the distribute ownership deliberately model to transfer problems, a controlled experiment, and an evidence defense. The middle weekend is for repairing failed checkpoints, not adding features.

| Day | Module | Required result |
|---:|---|---|
| 1 | [Distribution Economics, Boundary Evidence, and Architecture Fitness Functions](module-01-distribution-economics-and-boundary-evidence/index.md) | Publish a measured boundary scorecard that approves Notification Delivery for first extraction, approves Artifact Delivery conditionally, keeps Analysis Control cohesive, and rejects table-shaped services. |
| 2 | [Service Boundaries, Bounded Contexts, and Contract Ownership](module-02-service-boundaries-and-contract-ownership/index.md) | Publish the service catalogue, bounded-context map, contract ownership map, and explicit list of capabilities that remain inside Analysis Control. |
| 3 | [Data Ownership, Replication, and Cross-Service Query Design](module-03-data-ownership-replication-and-cross-service-queries/index.md) | Split authoritative data ownership, build versioned projections for cross-service reads, define staleness budgets, and prove reconciliation for missing, duplicate, and out-of-order updates. |
| 4 | [Synchronous Collaboration, API Composition, and Dependency Budgets](module-04-synchronous-collaboration-and-dependency-budgets/index.md) | Publish an acyclic synchronous dependency graph, one edge-owned deadline budget, bounded fan-out rules, and a gateway composition path that degrades truthfully. |
| 5 | [Distributed Workflows, Sagas, Compensation, and Process Managers](module-05-distributed-workflows-sagas-and-compensation/index.md) | Implement the artifact-publication and run-completion saga with durable step identity, semantic locks, compensation, timeout handling, and operator-visible reconciliation. |
| 6 | [Service Identity, Authorization, and Trust Propagation](module-06-service-identity-authorization-and-trust-propagation/index.md) | Introduce workload identities, audience-bound service credentials, delegated user context, short-lived artifact capabilities, and explicit authorization at every trust boundary. |
| 7 | [Discovery, Routing, Gateways, and Traffic Topology](module-07-discovery-routing-gateways-and-traffic-topology/index.md) | Implement service registration, health-aware routing, gateway edge policy, bounded traffic shifting, and an optional Kubernetes topology with explicit ownership of each routing decision. |
| 8 | [Deployment Independence, Version Skew, and Release Choreography](module-08-deployment-independence-version-skew-and-release-choreography/index.md) | Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence. |
| 9 | [Distributed Verification, Fault Injection, and Operability](module-09-distributed-verification-fault-injection-and-operability/index.md) | Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects. |
| 10 | [Incremental Extraction, Strangler Migration, and Final Architecture Defense](module-10-incremental-extraction-migration-and-final-defense/index.md) | Extract Notification Delivery and Artifact Delivery through shadow, compare, backfill, cutover, and decommission phases; retain Analysis Control; and publish the Course 9 graph-access handoff. |

## Suggested day

```text
08:30  retrieval practice and checkpoint repair
09:00  chapter reading and diagram reconstruction
11:00  worked examples and standards review
13:00  primary-track implementation reading
15:00  exercises before answers
17:00  controlled lab
19:30  evidence package and checkpoint defense
```

The two-week schedule is subordinate to evidence. If the distribute ownership deliberately argument becomes unclear, stop at the last green checkpoint, reduce the counterexample, and resume only after the owning mechanism is understood.

## Weekend synthesis

At the Week 1 boundary, reconstruct how Modules 1–5 change the platform while preserving this incoming state: The Course 7 platform with governed HTTP, event, and RPC interfaces and migration history through 015. Rerun those checkpoints and postpone every feature that does not serve the Course 8 responsibility.

## Recovery route

When a checkpoint fails:

1. isolate the first broken invariant;
2. restore the predecessor baseline if necessary;
3. reduce the failing case;
4. repair the owning mechanism;
5. retain the case as a regression;
6. update your explanation before continuing.
