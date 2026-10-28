# Start here

Course 8 is the point at which the Analysis Runs Platform becomes distributed. That does **not** mean the course begins by creating many services. It begins by proving which boundaries are valuable enough to deserve a network.

The governing question is:

> Which responsibilities should become independently owned and deployed, and how do we preserve correctness when local calls, local transactions, and one release unit no longer contain the workflow?

The course extracts Notification Delivery first and Artifact Delivery second. It keeps Analysis Control cohesive. It treats Worker Plane and Edge Gateway as distinct component types rather than inventing business ownership for them. It also requires the learner to reject Project Service, Dataset Table Service, Idempotency Service, and other table-shaped boundaries.

## What you should already know

Complete Courses 1–7 or possess equivalent skill in:

- HTTP semantics and OpenAPI contracts;
- transactionally correct application services;
- PostgreSQL ownership, migrations, idempotency, and optimistic concurrency;
- authentication, authorization, capabilities, and hostile-input defenses;
- deadlines, cancellation, retry budgets, structured telemetry, SLOs, and incident evidence;
- benchmarking, capacity, admission control, and overload behavior;
- event contracts, outbox/inbox, replay, consumer idempotency, and schema evolution;
- gRPC, Protobuf compatibility, streaming, health, and lifecycle.

Course 8 uses those mechanisms as prerequisites. It revisits them only where a service boundary changes their meaning.

## What this course will not teach

This is not a tutorial on:

- splitting a repository;
- creating one deployment per table;
- Docker Compose as architecture;
- Kubernetes object syntax as a substitute for service design;
- service meshes as a substitute for deadlines, idempotency, or authorization;
- distributed transactions as a rescue mechanism for weak boundaries;
- organizational slogans about “two-pizza teams.”

The optional Compose and Kubernetes examples make topology concrete. The core course remains valid without them because the primary subject is ownership and distributed correctness.

## One primary language, one comparative language

Choose Python or TypeScript as your primary implementation track.

In the primary track you should:

- modify the boundary and ownership models;
- implement saga and capability changes;
- run all semantic and failure tests;
- explain language-specific concurrency and error behavior;
- produce the final architecture defense.

Use the other track to:

- compare idiomatic representation;
- run shared-vector parity;
- review where static types are insufficient without runtime validation;
- confirm that the architecture is not tied to one framework.

You are not expected to duplicate class names, folder structures, or dependency-injection styles. The externally relevant invariants must match:

- service and data ownership;
- deadline and retry ownership;
- saga identity and compensation;
- capability claims and validation;
- version-skew outcomes;
- extraction phase behavior;
- reconciliation findings;
- public and event-visible outcomes.

## How to study each module

Each numbered module contains five files.

### `index.md`

The authoritative chapter. Read it before opening implementation files. It explains the engineering problem, decision rules, worked examples, failure evidence, and capstone change.

### `exercises.md`

Twelve questions that require transfer. Write your answer before opening the worked answers. Several questions are intentionally about rejecting a design.

### `exercise-answers.md`

Reasoned answers with decisive evidence. Compare the rule and proof, not merely the wording.

### `lab.md`

A controlled architecture or failure experiment. Each lab declares setup, action, oracle, evidence, cleanup, and completion gate.

### `checkpoint.md`

The evidence required before continuing. Reading completion does not compensate for missing proof.

## The evidence ladder

A distributed claim requires more than a unit test. Course 8 uses nine layers:

1. **Boundary evidence** — why a remote service creates more value than cost.
2. **Contract evidence** — what providers, consumers, and event participants may rely on.
3. **Ownership evidence** — which service may write each fact and who operates it.
4. **Local mechanism evidence** — whether each component implements its rule.
5. **Topology evidence** — dependency depth, cycles, routing, identity, and network policy.
6. **Failure evidence** — before-call, after-commit, timeout, duplicate, stale-attempt, and partition schedules.
7. **Reconciliation evidence** — comparison of durable owner states after ambiguity.
8. **Release evidence** — old/new coexistence, shadow comparison, cutover, rollback, and decommission.
9. **Operator evidence** — SLOs, alerts, runbooks, ownership, and incident decisions.

Passing one layer does not imply the next. A contract test cannot prove one-writer data ownership. A clean trace cannot prove authoritative state. A Kubernetes manifest cannot prove independent deployment.

## Working rules

Keep these rules visible throughout the course:

- Never add a service before naming its owner, facts, contracts, failure value, and reversal criteria.
- Never let two services write the same authoritative fact.
- Never let one service read another service’s private database in the application path.
- Never hide a distributed transaction behind a client helper.
- Never retry a mutation without durable effect identity and one retry owner.
- Never place business authority in a gateway, broker, mesh, discovery system, or tracing platform.
- Never call a view “eventually consistent” without a staleness target, gap policy, and repair path.
- Never cut over without a semantic comparison oracle, one active writer, and a rollback target.
- Never keep a service only because deleting it would be embarrassing.

## Orientation commands

From the course root:

```bash
make doctor
make predecessor-proof
make structure-proof
make boundary-proof
make python-proof
make typescript-proof
make capstone-tour
make network-lab-proof
```

The dependency-light routes prove the course’s deterministic architecture model. Environment-backed routes add real database, container, network, and Kubernetes evidence. The course records that boundary explicitly.

## Your architecture journal

Maintain one short journal entry per module with:

```text
Decision made:
Evidence used:
Failure considered:
Guarantee preserved:
Cost introduced:
Residual risk:
Reversal condition:
```

This prevents the final architecture from becoming a diagram whose decisions cannot be reconstructed.
