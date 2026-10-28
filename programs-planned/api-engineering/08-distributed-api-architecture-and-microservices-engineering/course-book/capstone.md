# Capstone — extracting the Analysis Runs Platform deliberately

## Starting point

Course 7 left one modular service with mature public HTTP, event, and gRPC boundaries. Its 46-file handoff contains the contracts, migrations, interaction decisions, security policies, shared vectors, and a service-boundary dossier. The dossier proposes candidates but approves no extraction. Course 8 begins from those exact bytes.

## Final topology

```text
Public clients
      |
      v
Edge Gateway ---------------------------+
      |                                  |
      v                                  v
Analysis Control                    Artifact Service
      |                                  ^
      | gRPC                             | capability-bound upload/download
      v                                  |
Worker Plane ----------------------------+
      |
      | durable Analysis Events
      v
Notification Service
```

The diagram is intentionally small. Course 8 does not create a service for projects, datasets, idempotency, saga storage, or every table.

### Analysis Control

Authoritative for projects, dataset metadata, analysis runs, idempotency, worker leases, run transitions, process-manager state, and event publication. These facts share invariants and transaction authority.

### Artifact Service

Authoritative for artifact identity, bytes, checksums, object keys, publication state, retention, and content delivery. It accepts short-lived capabilities minted after Control authorization. It does not query the Control database or trust caller identity headers.

### Notification Service

Authoritative for webhook subscriptions, delivery attempts, retry schedules, receiver evidence, and delivery retention. It reacts to durable run events and never blocks run completion.

### Worker Plane

Runs and scales independently. It owns execution resources and ephemeral session state, not run truth. Control validates lease generation and completion attempts.

### Edge Gateway

Owns public-edge protocol handling, request budgets, routing, and bounded response composition. It stores no domain state and makes no run-transition decisions.

## Why this topology

Notification is extracted first because a durable event already separates run completion from delivery. Artifact is extracted second because storage, egress, integrity, and retention form a distinct capability, but the boundary requires redesigned authorization and reconciliation. Analysis Control remains cohesive because splitting its run, lease, idempotency, and event decisions would create a distributed transaction around the platform’s most sensitive invariant.

## The central distributed workflow

```text
1. Public client submits a run through the gateway.
2. Analysis Control commits run, idempotency, and outbox state.
3. Worker Plane receives/claims execution under current lease generation.
4. Control grants a run-attempt-scoped upload capability.
5. Worker uploads bytes to Artifact Service.
6. Artifact commits exactly one checksum-bound effect.
7. Artifact publishes ArtifactStored.
8. Control validates the current attempt and completes the run.
9. Control publishes AnalysisRunCompleted transactionally.
10. Notification creates delivery attempts idempotently.
11. Reconciliation compares all authoritative states.
```

There is no global transaction. Correctness comes from:

- owner-local transactions;
- stable business-effect identities;
- outbox and inbox records;
- explicit intermediate states;
- current-attempt fencing;
- idempotent commands and consumers;
- semantic compensation;
- reconciliation.

## Capstone artifacts

The capstone is not only code. It contains the evidence required to defend the architecture:

```text
architecture/
    boundary scorecard
    service catalogue
    data ownership
    dependency graph
    consistency and staleness policy
    saga catalogue
    security policy
    release policy
    extraction plan
    version ledger
    architecture decision records

database/
    legacy migration history 001–015
    service-owned migration heads

tracks/
    Python semantic reference
    TypeScript semantic reference

network-lab/
    five-process loopback implementation
    real delegated calls and explicit degradation

security/
    cross-language artifact capability wire profile

topology/
    executable Compose laboratory
    Kubernetes deployment and NetworkPolicy declarations

shared/vectors/
    cross-language boundary, ownership, consistency,
    graph, saga, capability, routing, version, extraction,
    and reconciliation cases

releases/
    accepted distributed profile
    deliberately rejected candidates

planted-defects/
    ten architecture regressions the proof suite must reject

handoff/
    sanitized boundary material for Course 9
```

## Rejected architecture

The final defense must explain why the course rejects:

- a service for every table;
- a shared application database with “logical ownership” only;
- an Idempotency Service;
- gateway-owned workflows;
- synchronous notification calls from run completion;
- Artifact Service calling Control for each authorization decision;
- Worker Plane deciding completion because a stream sent `success`;
- an ownerless Shared Data Service;
- a service mesh as the owner of retry or business policy.

## Required final proof

The capstone passes only when you can show:

- one accountable owner for every service and contract;
- one authoritative writer for every business fact;
- no synchronous dependency cycle;
- a bounded public synchronous depth;
- one recoverable artifact completion saga;
- short-lived audience-bound capabilities;
- explicit partial response semantics;
- replayable and gap-aware projections;
- supported mixed versions;
- clean shadow and canary evidence;
- route, data, and event rollback boundaries;
- zero unexplained reconciliation findings;
- decommission and merge-back criteria.
