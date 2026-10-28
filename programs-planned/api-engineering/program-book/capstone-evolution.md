# Capstone Evolution

## Course 1 — Contract surface

The platform begins as a canonical OpenAPI contract, two reference providers, consumer scenarios, mocks, schema fixtures, and compatibility gates. Persistence is intentionally instructional.

## Course 2 — Durable service

PostgreSQL, migrations, transactions, persistent idempotency, conditional updates, stable pagination, worker leases, artifact integrity, and transactional webhook delivery make the public contract durable.

## Course 3 — Security boundary

Threats, identity, resource authorization, hostile input, outbound destination policy, secrets, abuse controls, and incident evidence harden the same service.

## Course 4 — Operational truth

Deadlines, lifecycle, structured telemetry, metrics, traces, SLOs, alerts, runbooks, fault experiments, and reconciliation make failures diagnosable and recoverable.

## Course 5 — Pressure and capacity

Workloads, benchmark evidence, query plans, runtime profiles, concurrency controls, caches, quotas, load shedding, and capacity models protect the guarantees under demand.

## Course 6 — Asynchronous contract

AsyncAPI and CloudEvents publish durable facts. Outbox, inbox, replay, workflow, windowing, dead-letter, and event-governance mechanisms extend the system across asynchronous time.

## Course 7 — Typed RPC

Protobuf and gRPC add controlled internal unary and streaming interactions with deadlines, cancellation, flow control, workload identity, health, and wire compatibility.

## Course 8 — Distributed ownership

Notification and artifact capabilities are extracted only after boundary evidence. Data ownership, projections, sagas, trust propagation, release choreography, and strangler migration are proved.

## Course 9 — Graph composition

A GraphQL gateway exposes governed client-shaped views and mutations while preserving service ownership, authorization, demand bounds, partial-data truth, and subscription resume semantics.

## Course 10 — Organizational platform

Catalog, registry, policy, lifecycle, templates, docs, sandboxes, SDKs, provenance, runtime reconciliation, product analytics, and support workflows turn the interfaces into a governed portfolio.

## Final architecture

```text
Consumers
  ├── HTTP/OpenAPI
  ├── GraphQL
  ├── Events/AsyncAPI
  └── SDKs and CLI
          |
          v
      Edge and Graph layers
          |
          v
  Analysis Control ── gRPC ── Worker Plane
        |           |    \ events
        v     v
 Artifact   Notification
 Service     Service
        \     /
         API Platform
  catalog, registry, policy,
  docs, lifecycle, support
```

The diagram is a map of responsibilities, not a requirement to deploy every box separately in every environment.
