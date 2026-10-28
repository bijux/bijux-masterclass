# The Analysis Runs Platform

## Domain story

A principal works inside one tenant. The principal creates a project, registers or uploads a dataset, submits an analysis run with parameters, observes the run’s progress, and retrieves one or more verified artifacts. A webhook subscription can receive completion or failure facts. Later, independent consumers project, audit, notify, and analyze those facts.

The workflow is deliberately stable across the six courses:

```text
create project
→ register or upload dataset
→ submit analysis run
→ observe durable progress
→ retrieve a verified artifact
→ deliver and deduplicate a webhook
→ publish governed integration events
→ apply independent consumer effects
```

## Resource and ownership model

Projects own datasets and analysis runs. A run consumes one dataset and a parameter set. Its state machine permits only declared transitions. Artifacts become available only after successful publication. Principals are tenant-bound, and policy decisions combine operation permission with resource ownership or an explicitly governed support context.

The platform distinguishes four forms of state:

1. **public representation state** exposed by the API;
2. **authoritative durable state** in PostgreSQL and artifact storage;
3. **operational observation** in telemetry;
4. **derived asynchronous state** in projections and consumer effects.

A central program rule is that these forms must not impersonate one another. A trace can help locate a failed transaction, but it cannot prove the transaction committed. An event projection can rebuild a view, but it cannot retroactively change the source fact. A contract example can illustrate a response, but it cannot prove a provider returned it.

## Architecture progression

### Course 1 — Contract laboratory

The platform exists as a canonical OpenAPI description, two reference providers, mocks, generated or authored clients, schema fixtures, and conformance tests. State is intentionally simple. The purpose is to separate public promise from framework behavior.

### Course 2 — Durable modular service

PostgreSQL becomes authoritative. Transactions, idempotency records, version columns, keyset cursors, durable jobs, leases, content-addressed artifacts, and a transactional webhook outbox make the contract honest under restart and concurrency.

### Course 3 — Security boundary

The service gains threat-derived requirements, strict edge parsing, resource-server validation, default-deny authorization, tenant and ownership enforcement, hostile-input controls, SSRF defense, secret handling, abuse budgets, and incident evidence.

### Course 4 — Operated system

Deadlines, cancellation, resilience, lifecycle states, structured events, metrics, traces, SLOs, alerts, runbooks, fault injection, incident roles, and durable-state reconciliation make failure diagnosable and recoverable.

### Course 5 — System under pressure

Workload identities, comparable benchmarks, query plans, runtime profiles, bounded admission, authorization-aware caching, traffic policy, capacity models, and regression gates make growth a measured engineering problem rather than a guess.

### Course 6 — Asynchronous public boundary

A transactional event outbox, AsyncAPI contract, CloudEvents envelope profile, delivery model, inbox deduplication, schema evolution, replay, projections, process managers, event-time computation, event security, dead-letter custody, and governance extend the platform beyond synchronous HTTP.

## Why the platform remains one system

The program deliberately resists premature microservices. The learner first masters ownership and failure in one coherent service. Event consumers are introduced because asynchronous independence creates a real need, not because more deployables look advanced. A later distributed-architecture course can decompose the system only after the learner understands what distribution multiplies.

## Final platform invariant

At every stage, the same user-facing outcome must remain explainable from boundary to authority:

```text
accepted input
→ owned decision
→ durable transition
→ protected access
→ observable operation
→ bounded resource use
→ governed asynchronous fact and effect
```

When one arrow is missing, the platform is not complete no matter how sophisticated the surrounding tools appear.
