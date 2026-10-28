# Course contents

This document inventories the complete learner product for **Course 8 — Distributed API Architecture and Microservices Engineering**. The authoritative reading path begins at [`course-book/start-here.md`](course-book/start-here.md). The course book explains the subject; the capstone, code, topology, fixtures, and proof scripts supply practical evidence.

## Course outcome

By the end of the course, the learner can decide whether a capability deserves independent deployment, assign service and data ownership, design bounded synchronous and asynchronous collaboration, preserve security and business intent across failures, release independently under version skew, extract incrementally, reconcile divergent states, and defend or reverse the resulting architecture.

The final capstone does not maximize service count. It makes five component roles explicit:

| Component | Kind | Business authority |
|---|---|---|
| Edge Gateway | edge component | none |
| Analysis Control | business service | projects, dataset metadata, runs, idempotency, leases, workflow state, event publication |
| Artifact Service | business service | artifact identity, metadata, bytes, integrity, publication, and retention |
| Notification Service | business service | subscriptions, delivery attempts, retry state, and receiver evidence |
| Worker Plane | compute plane | none; attempts work under Control authority |

Notification Delivery is extracted first. Artifact Delivery is extracted second. Analysis Control remains cohesive because its run, idempotency, lease, and event decisions share transaction authority. The course explicitly rejects table-per-service decomposition, shared application databases, an Idempotency Service, gateway-owned workflows, and ownerless shared data services.

## Reader-first course book

The course book contains **61 navigated pages** and approximately **49,974 words**. Orientation is followed by ten full modules. Every numbered module has one stable five-file shape:

```text
index.md
exercises.md
exercise-answers.md
lab.md
checkpoint.md
```

- `index.md` is the self-contained authoritative chapter.
- `exercises.md` contains twelve transfer questions.
- `exercise-answers.md` contains twelve matching worked answers.
- `lab.md` defines setup, controlled actions, correctness oracle, evidence, cleanup, and completion gate.
- `checkpoint.md` defines the non-compensable evidence required before progression.

The course therefore includes:

```text
10 complete modules
120 numbered exercises
120 matching reasoned answers
10 failure-oriented laboratories
10 evidence checkpoints
```

## Module progression

| Module | Governing question | Cumulative result |
|---:|---|---|
| 1. Distribution Economics, Boundary Evidence, and Architecture Fitness Functions | When does a remote boundary create more value than cost? | A measured scorecard approves two extractions, keeps Analysis Control cohesive, and rejects weak candidates. |
| 2. Service Boundaries, Bounded Contexts, and Contract Ownership | How do we draw boundaries around cohesive decisions and language? | A service catalogue, contract ownership map, bounded-context map, and rejected-boundary register. |
| 3. Data Ownership, Replication, and Cross-Service Query Design | How can services own writes while the platform still answers cross-capability questions? | One writer per fact, service-owned migration histories, versioned projections, staleness policies, and reconciliation. |
| 4. Synchronous Collaboration, API Composition, and Dependency Budgets | How do we prevent fan-out, retry, and timeout multiplication? | An acyclic dependency graph, absolute budgets, one retry owner, bounded composition, and explicit partial responses. |
| 5. Distributed Workflows, Sagas, Compensation, and Process Managers | How is business intent preserved without a global transaction? | A recoverable artifact-publication and run-completion saga with stable identities, fencing, compensation, and reconciliation. |
| 6. Service Identity, Authorization, and Trust Propagation | How do workloads preserve user intent without trusting the network? | Workload identity, end-user delegation, exact cross-language capabilities, local owner authorization, and network-policy defense in depth. |
| 7. Discovery, Routing, Gateways, and Traffic Topology | How do callers locate healthy instances without placing business authority in routing infrastructure? | Health-aware selection, service topology, edge policy, shadow and canary routing, and bounded gateway responsibility. |
| 8. Deployment Independence, Version Skew, and Release Choreography | How can providers and consumers release independently? | A mixed-version matrix, expand-and-contract changes, feature suppression, canary evidence, rollback, and decommission policy. |
| 9. Distributed Verification, Fault Injection, and Operability | How do we prove the outcome when every service can pass locally? | A layered proof system, five-process failure evidence, reconciliation, bounded fault plans, and ten rejected architecture defects. |
| 10. Incremental Extraction, Strangler Migration, and Final Architecture Defense | How do we extract safely and retain a path to stop or reverse? | Shadow, canary, cutover, data migration, decommission, merge-back criteria, final defense, and a Course 9 boundary handoff. |

## Cumulative capstone

The capstone continues the Analysis Runs Platform inherited from Course 7. It contains the following major areas.

### `predecessor/handoff/`

The exact 46-file Course 7 handoff. It preserves public HTTP, event, and RPC contracts, compatibility policy, migration history through 015, security and lifecycle decisions, shared vectors, and the service-boundary dossier. Course 8 verifies these bytes before making changes.

### `architecture/`

The decision system:

- boundary scorecard;
- service catalogue;
- data-ownership map;
- synchronous and asynchronous dependency graph;
- consistency and staleness policy;
- saga catalogue;
- security policy;
- release and version-skew policy;
- extraction plan;
- version ledger;
- six architecture decision records.

### `tracks/python-distributed/`

The primary dependency-light reference includes:

- boundary scoring;
- service and fact ownership;
- versioned projections;
- dependency graph and cycle detection;
- saga and compensation state;
- exact capability serialization and validation;
- service registry and routing;
- version-skew policy;
- strangler phase transitions;
- Analysis Control, Artifact, Notification, and Gateway semantics;
- deterministic reconciliation;
- an end-to-end semantic tour.

### `tracks/typescript-distributed/`

The strict TypeScript comparative reference implements the same externally relevant invariants idiomatically. The two tracks share golden vectors, including a byte-identical artifact capability token. TypeScript compilation is part of the dependency-light proof.

### `network-lab/`

A five-process, standard-library laboratory:

```text
course client / operator
          |
          v
Edge Gateway -------> Analysis Control
          |                   ^       |
          v                   |       v committed event
Artifact Service <------ Worker Plane  broker-relay step
                                      |
                                      v
                            Notification Service
```

The laboratory performs real loopback TCP calls, authenticates workload hops, delegates a narrow artifact capability, completes one run, records one notification, then terminates Artifact Service. The gateway must return authoritative run state with `partial: true` and `artifactsUnavailable`; it may not return an empty artifact list as complete truth.

### `database/`

- exact legacy migrations 001–015;
- Analysis Control owner-local migration head 001;
- Artifact Service migration head 002;
- Notification Service migration head 002;
- Platform Catalogue migration head 001;
- an environment-backed `make postgres-proof` route that applies all owner-local histories to isolated PostgreSQL schemas.

The one-database/multiple-schema arrangement is only a laboratory isolation technique. The architecture contract still requires separate credentials and no private cross-service table access.

### `security/`

A documented, course-specific artifact capability profile. It specifies canonical JSON, exact signing input, claims, safe integer rules, lifetime, audience, resource, tenant, checksum, size, and constant-time verification. The course explicitly states that this teaching profile is not JWT, OAuth, PASETO, or an Internet standard and does not replace workload authentication.

### `topology/`

- an executable Docker Compose build of the five-process network laboratory;
- Kubernetes Namespace, ServiceAccount, Deployment, Service, Secret fixture, event broker, and NetworkPolicy declarations;
- explicit evidence boundaries for static configuration versus applied, failure-tested infrastructure.

### `shared/vectors/`

Ten cross-language vector families cover:

- boundary decisions;
- capability validation and exact bytes;
- consistency and projection behavior;
- dependency graph behavior;
- extraction phases;
- ownership;
- reconciliation;
- routing;
- saga schedules;
- version skew.

### `releases/` and `planted-defects/`

One accepted Distributed Architecture Profile 1.0 release and ten deliberately rejected candidates. Each planted defect names the exact proof expected to reject it, including shared database ownership, synchronous cycles, missing rollback, gateway business state, and unsupported version skew.

### `handoff/`

A sanitized eight-file Course 9 handoff. It exposes service and query boundaries required for GraphQL without permitting direct database joins, unbounded resolver fan-out, or a second domain model in the graph gateway.

## Language strategy

Course 8 uses one primary implementation track and one comparative track.

In the primary track, the learner modifies and proves the architecture deeply. In the comparative track, the learner checks that the same invariant survives a different type system and runtime. The course requires parity in ownership, contract behavior, capability bytes, saga identity, routing outcomes, extraction phases, and reconciliation. It does not require artificial one-to-one duplication of framework structure.

## Proof routes

The primary dependency-light routes are:

```bash
make doctor
make predecessor-proof
make structure-proof
make boundary-proof
make ownership-proof
make data-proof
make dependency-proof
make saga-proof
make reconciliation-proof
make security-proof
make routing-proof
make release-proof
make extraction-proof
make migration-proof
make vector-proof
make python-proof
make typescript-proof
make distributed-proof
make network-lab-proof
make planted-defect-proof
make final-defense-proof
make handoff-proof
make core-proof
```

Environment-backed routes are:

```bash
TEST_DATABASE_URL=... make postgres-proof
make compose-proof
make kubernetes-proof
make docs-build
make full-proof
```

A route is reported as passed only when it executes. Missing external dependencies are reported as not executed rather than converted into synthetic success.

## Completion standard

The course is complete only when the learner can show all of the following:

1. Course 7’s handoff is intact.
2. Every service and contract has one accountable owner.
3. Every authoritative fact has exactly one writer.
4. No application path reads another service’s private database.
5. The synchronous graph is acyclic and the public depth is bounded.
6. One absolute deadline and one retry owner govern each remote edge.
7. Partial and stale data are represented explicitly.
8. The artifact completion saga survives duplicate, timeout, and stale-attempt schedules.
9. Workload identity and delegated user authority remain distinct.
10. Capability bytes and decisions match across Python and TypeScript.
11. Supported provider/consumer version skew passes and unsupported skew is rejected.
12. Shadow evidence is clean before canary and cutover.
13. Rollback, decommission, and merge-back conditions exist.
14. Five-process failure evidence shows truthful degradation.
15. Reconciliation ends with no unexplained findings.
16. The final architecture defense explains both the chosen extractions and the rejected ones.
