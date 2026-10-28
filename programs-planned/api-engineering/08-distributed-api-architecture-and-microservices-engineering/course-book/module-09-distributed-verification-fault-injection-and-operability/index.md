# Module 09 — Distributed Verification, Fault Injection, and Operability

> **Program stage:** Course 8 of 10 — Distribute ownership deliberately.

> **Central question:** How do we prove system behavior when individual services pass their tests but network partitions, version skew, and cross-service timing still create failures?

## Where this module fits

Module 08 produced **Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence**. This module extends that result by asking: **How do we prove system behavior when individual services pass their tests but network partitions, version skew, and cross-service timing still create failures?**

The new capstone increment is **Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects**. It becomes the prerequisite for **Incremental Extraction, Strangler Migration, and Final Architecture Defense**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Separate service unit tests, contract tests, topology tests, and end-to-end outcome proofs.
- Test failure timing before invocation, after commit, during delivery, and during recovery.
- Use traces and durable state together rather than treating telemetry as authority.
- Design bounded fault injection with abort and cleanup conditions.
- Verify dependency graphs, ownership, and version matrices mechanically.
- Diagnose distributed incidents from one critical journey without requiring omniscient logs.

## Capstone increment

Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects.

## Local correctness does not compose automatically

Each service can pass its unit tests while the system fails. Examples:

- both services accept the same fact as authoritative;
- a timeout after commit causes duplicate cross-service effects;
- old and new versions interpret an optional field differently;
- a projection silently skips a version;
- a gateway retry and sidecar retry amplify load;
- a compensation runs twice;
- a cutover routes users inconsistently;
- traces look healthy while durable state diverges.

Distributed verification therefore organizes evidence by failure boundary.

## The proof ladder

### Service-local tests

Pure rules, persistence adapters, authorization, and protocol behavior. Necessary, not sufficient.

### Contract tests

Provider and consumer expectations for HTTP, events, and gRPC. These catch shape and selected behavior drift.

### Topology tests

No synchronous cycles, bounded public depth, permitted trust edges, one data owner, version-compatible routes, and declared failure domains.

### Schedule tests

Control when failure happens:

```text
before request send
after receive before local commit
after commit before response
after publish before acknowledgement
after cutover before comparison window ends
```

The timing is part of the test case.

### Reconciliation tests

Compare durable authority after ambiguity. The operator should not need to infer correctness from logs.

### Release tests

Run old/new combinations, shadow comparisons, canary thresholds, rollback, and decommission gates.

### Environment-backed topology tests

Use real processes, databases, broker, DNS, and network policy. These prove properties unavailable to an in-process model, but still do not prove every production schedule.

## Fault injection with a contract

A fault plan names:

- hypothesis;
- target boundary;
- exact injection point;
- blast radius;
- expected service and user outcome;
- durable oracle;
- telemetry expected;
- abort condition;
- cleanup;
- residual uncertainty.

“Kill a container and see what happens” is an activity, not an experiment.

## Ten planted defects

Course 8 includes defects that superficially look productive:

1. shared database access;
2. Project table service;
3. synchronous cycle;
4. unbounded gateway fan-out;
5. uncontrolled dual writes;
6. missing saga compensation;
7. gateway business logic;
8. trusted identity header;
9. incompatible version skew;
10. ownerless service.

Each defect has a named rejecting proof. A proof that cannot reject its assigned defect is weak even if the happy path passes.

## Observability across services

Course 4 established traces, metrics, logs, and durable reconciliation. Course 8 applies them to ownership boundaries:

- one edge trace id;
- span per remote attempt;
- link from asynchronous event processing;
- service, instance, version, and attempt attributes;
- no sensitive authority in baggage;
- metrics by bounded service and operation dimensions;
- logs with stable effect and saga ids.

Telemetry helps locate ambiguity. It does not decide which database is authoritative.

## Incident diagnosis

A useful incident view starts from a critical journey:

```text
user submitted run
Control committed request
worker uploaded artifact
Artifact published object
Control did not attach reference
Notification never received completion
```

The response is not “all services are green.” It is a state comparison: artifact orphan, run still running, no completion event. The owner of the saga decides compensation or repair.

## Contract tests and false confidence

Consumer-driven contract tests can prove that known consumer expectations remain valid. They cannot prove that the service has a good boundary, that data ownership is correct, or that an unknown consumer is safe. Use them within the larger proof ladder.

## Python and TypeScript implications

Both tracks run shared semantic vectors and independent unit tests. The course tool separately verifies architecture YAML, service-owned migrations, release candidates, and planted defects. The optional Compose/Kubernetes routes are classified as environment-backed rather than silently simulated.

## Evidence required before Module 10

All ten defects must be rejected. Produce at least one after-commit ambiguity test, one version-skew topology test, one reconciliation report, and one bounded fault plan with cleanup.

## A distributed proof matrix

Unit tests remain necessary, but they cover only local logic. Course 8 organizes evidence by claim:

| Claim | Minimum evidence |
|---|---|
| one writer per fact | ownership catalogue plus credential/database tests |
| no synchronous cycle | declared graph proof plus runtime trace review |
| idempotent cross-service effect | duplicate and lost-response schedule |
| compensatable workflow | failure before and after every durable step |
| bounded version skew | old/new matrix and rollback rehearsal |
| tenant isolation | negative cross-tenant tests at every owner |
| safe cutover | shadow comparison, canary, reconciliation, route rollback |
| operable service | SLO, alerts, runbook, owner, recovery exercise |

A passing consumer contract test does not prove data ownership. A passing saga unit test does not prove the relay, database, and retry topology. Evidence must match the claim.

## Fault injection needs a falsifiable contract

A fault experiment should declare:

```text
hypothesis
preconditions
fault point and duration
blast radius
expected durable state
expected client-visible outcome
expected telemetry
abort condition
cleanup
reconciliation result
```

“Kill Artifact Service and see what happens” is not sufficient. A stronger experiment is:

> While a run is `running`, terminate Artifact Service after it commits an artifact but before the worker receives the response. The worker retries with the same effect identity. Exactly one artifact remains published, Control eventually attaches that artifact or marks it for compensation, and no run is reported complete without an authoritative reference.

That statement can fail.

## Failure schedules across boundaries

For each command or event, inject failure at these points:

- before send;
- after send, before receive;
- before owner commit;
- after owner commit, before response or acknowledgement;
- during retry delay;
- after caller deadline;
- during version rollout;
- during consumer replay;
- during compensation;
- during reconciliation.

Not every combination needs a bespoke integration test, but critical effects need representative coverage.

## Ten planted defects as proof sensitivity

The course includes ten defects, but the important lesson is not their number. A proof suite should demonstrate that it rejects realistic regressions:

- a second writer to an authoritative fact;
- a table-shaped service with no decision ownership;
- a synchronous cycle;
- unbounded fan-out;
- non-atomic dual write;
- workflow without compensation;
- gateway business authority;
- trusted identity header;
- unsupported version skew;
- ownerless service.

If deleting the check or inserting the defect still passes, the proof is ceremonial.

## Runtime topology evidence

Static declarations can drift from runtime. Collect and compare:

- service-to-service traces;
- network flow logs where available;
- destination and operation metrics;
- service discovery records;
- certificate or workload identities;
- database connection principals;
- event producer and consumer identities.

An undeclared Control → Notification call should be visible as a graph violation. A Notification credential writing Control tables should be impossible and detectable.

Telemetry is evidence, not authority. A missing trace does not prove a call did not occur unless sampling and collection guarantees support that claim.

## Distributed tracing rules

A trace should preserve causal structure without inventing parentage. Synchronous downstream calls are child spans. Asynchronous consumers commonly link to the producing context while starting a new trace or processing span according to the instrumentation model.

Record:

- service and operation;
- contract version;
- attempt or delivery identity;
- remaining deadline class;
- route version;
- outcome and error category;
- sanitized tenant pseudonym;
- message or saga identity where safe.

Do not put credentials or full personal data in trace attributes or baggage.

## Reconciliation as an integration oracle

After a fault schedule, compare owner state:

```text
Control completed runs
Artifact published objects
Notification delivery records
Event/outbox history
Saga terminal states
```

The result should have no unexplained orphan, missing reference, duplicate current effect, or version gap. Reconciliation often finds failures that request-level assertions miss.

The reconciliation tool should be deterministic and read-only. It emits stable finding IDs so repeated runs can distinguish persistent from resolved findings.

## Contract tests and their limits

Consumer-driven contract tests can prove that a provider response satisfies a consumer’s declared expectations. They cannot prove:

- the provider owns the data;
- all consumers are known;
- production traffic follows the declared topology;
- a workflow is idempotent under response loss;
- an authorization decision is complete;
- a migration is reversible;
- an event replay is side-effect safe.

Use contract tests as one layer, not as a distributed-system certificate.

## Operability review per service

Before a service is considered independently owned, it needs:

- one SLO or clearly justified absence;
- bounded resource and dependency budgets;
- health and drain behavior;
- dashboards by critical journey;
- alerts tied to user or data risk;
- backup and restore ownership for authoritative data;
- migration procedure;
- replay or reconciliation procedure;
- incident and escalation owner;
- decommission and merge-back path.

A service that cannot be operated independently is not independently deployable in practice.

## Incident diagnosis exercise

Scenario:

```text
Public run retrieval succeeds.
Artifact detail is intermittently absent.
Artifact Service error rate is low.
Gateway p99 increases.
Control has current references.
One Artifact version is draining.
```

A disciplined diagnosis asks:

1. Is partiality explicitly reported?
2. Which route versions handled requests?
3. Is discovery sending traffic to a draining endpoint?
4. Are deadlines exhausted before Artifact is called?
5. Did a proxy retry hide connection failures?
6. Are capability validations failing for one issuer key?
7. Does reconciliation find missing artifacts or only retrieval failures?

The answer cannot be obtained from one service log. Course 4’s observability skills now operate across ownership boundaries.

## Verification cost feeds back into architecture

If a proposed service split requires an unmanageable proof matrix, that is architecture evidence. Complexity in testing, release, and reconciliation is not an external inconvenience; it is part of the boundary’s cost.

The best correction may be to simplify the workflow or merge a boundary, not to add another test framework.

## Module synthesis

You are ready to leave this module when you can **separate service unit tests, contract tests, topology tests, and end-to-end outcome proofs, test failure timing before invocation, after commit, during delivery, and during recovery, and use traces and durable state together rather than treating telemetry as authority** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Inject after-commit response loss in artifact storage and reconcile by stable effect identity** and requiring the following oracle: **All legitimate schedules converge or produce explicit manual findings; every planted defect fails the intended gate; cleanup restores the baseline.**

The cumulative platform now includes **Build a distributed proof ladder spanning contract, component, topology, fault, reconciliation, and operator evidence, then use it to reject ten planted architecture defects**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Incremental Extraction, Strangler Migration, and Final Architecture Defense](../module-10-incremental-extraction-migration-and-final-defense/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
