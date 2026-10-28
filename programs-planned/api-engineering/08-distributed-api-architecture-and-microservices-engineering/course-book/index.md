# Distributed API Architecture and Microservices Engineering

Course 8 is about one difficult professional judgment:

> **Where should the network become an architectural boundary, and how do we keep the system correct after it does?**

The previous seven courses built a public HTTP contract, a durable service, security controls, reliability evidence, capacity discipline, asynchronous event contracts, and typed gRPC interfaces. None of those accomplishments automatically justify microservices. A distributed system adds independent failure, deployment, security, data ownership, latency, version skew, and operational cost. The correct goal is not more services. It is **clearer ownership with acceptable coordination cost**.

The course continues the Analysis Runs Platform and reaches a specific final architecture:

```text
Public clients
    |
Edge Gateway                no business data
    |
Analysis Control            projects, dataset metadata, runs, idempotency,
    |                        leases, authoritative events
    +------ gRPC ---------- Worker Plane
    |
    +------ capability ---- Artifact Service
    |
    +------ events -------- Notification Service
```

Notification Delivery is extracted first because it is already event-fed and independently retryable. Artifact Delivery is extracted second because storage and egress have distinct scaling and retention characteristics, but only after authorization and orphan reconciliation are redesigned. Analysis Control remains cohesive because its invariants share one transaction authority. Project, Dataset, and Idempotency table services are explicitly rejected.

## Reader path

1. Read [Start here](start-here.md).
2. Follow the [Study plan](study-plan.md).
3. Use the [Capstone guide](capstone.md) to understand the cumulative architecture.
4. Complete Modules 01–10 in order.
5. Do not advance past a checkpoint without producing its evidence.

## Course promise

After completing the course, you can:

- decide whether a service boundary is justified;
- define business and data ownership;
- design cross-service reads without shared databases;
- bound synchronous dependency chains;
- implement sagas and semantic compensation;
- preserve user and workload authority across services;
- design discovery, gateway, and routing responsibilities;
- release independently under bounded version skew;
- verify distributed outcomes under failure;
- extract, cut over, roll back, decommission, or merge a service back.

The course does not reward architecture theatre. Every service must have a named owner, owned data or a clearly non-data role, explicit contracts, failure semantics, release evidence, reconciliation, and an operator who knows what to do when the network lies.
