# GraphQL Schema and Runtime Engineering

**Course 9 of 10 — Compose governed client-shaped capabilities**

## Course promise

Design a governed GraphQL schema and runtime that composes service-owned capabilities with bounded execution and truthful partial results.

> **Governing question:** How can clients select graph-shaped data and operations without moving business ownership, authorization, cost, or consistency into an uncontrolled gateway?

## Place in the program

**Incoming boundary:** The Course 8 distributed architecture handoff with explicit service, data, contract, and trust boundaries.

**Outgoing boundary:** Analysis Graph API 1.0, GraphQL September 2025 schema, persisted operation registry, resolver ownership, demand policy, resumable subscriptions, compatibility gates, and platform-publication metadata.

Course 9 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the compose governed client-shaped capabilities mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- graph interface placement and operation lifecycle;
- type-system, nullability, resolver, source-ownership, and batching discipline;
- stable identifiers, connections, mutations, idempotency, and policy enforcement;
- persisted operations, demand control, caching, partial data, and observability;
- subscriptions, schema evolution, federation boundaries, and release governance;

## Course-level learning outcomes

- Place GraphQL without changing service authority.
- Design types around client concepts.
- Map every field to one source.
- Design meaningful roots.
- Distinguish mutation serialization from transactionality.
- Enforce field and tenant authorization.
- Separate validity from affordability.
- Separate request and execution errors.
- Map durable events to subscription responses.
- Classify schema evolution by client direction.

## Module map

| Day | Chapter | Governing question | Capstone increment |
|---:|---|---|---|
| 1 | [Graph Interface Placement and the Operation Lifecycle](module-01-graph-interface-placement-and-operation-lifecycle/index.md) | Where does GraphQL belong, and what happens between receiving a document and returning a response? | Publish the graph boundary and operation-lifecycle trace. |
| 2 | [Type System, Nullability, and Semantic Modeling](module-02-type-system-nullability-and-semantic-modeling/index.md) | How does the schema make useful promises without promising values the runtime cannot sustain? | Release Analysis Graph API 1.0 type and nullability policies. |
| 3 | [Resolver Architecture, Batching, and Source Ownership](module-03-resolver-architecture-batching-and-source-ownership/index.md) | How can nested graph execution remain faithful to service ownership without producing N+1 calls? | Replace N+1 nested calls with request-scoped batching. |
| 4 | [Queries, Identifiers, Connections, and Pagination](module-04-queries-identifiers-connections-and-pagination/index.md) | How can clients navigate lists and relationships without unstable pages, leaked internals, or unbounded work? | Implement global IDs and stable, bound connections. |
| 5 | [Mutations, Idempotency, Concurrency, and Domain Results](module-05-mutations-idempotency-concurrency-and-domain-results/index.md) | How do graph mutations preserve the durable command guarantees of the owning service? | Expose idempotent create/start/cancel mutations over owning services. |
| 6 | [Authorization, Tenancy, and Schema Exposure](module-06-authorization-tenancy-and-schema-exposure/index.md) | How can clients select flexible fields without gaining flexible authority? | Prove field, tenant, collection, and sensitive-output authorization. |
| 7 | [Demand Control, Persisted Operations, and Caching](module-07-demand-control-persisted-operations-and-caching/index.md) | How can a client-shaped query language remain bounded under adversarial and accidental demand? | Admit only bounded trusted operations and record cost evidence. |
| 8 | [Errors, Partial Data, Consistency, and Observability](module-08-errors-partial-data-consistency-and-observability/index.md) | How does the graph tell the truth when some fields succeed, some fail, and some are stale? | Return truthful partial data with path-specific errors and traces. |
| 9 | [Subscriptions, Resume, and Incremental Delivery](module-09-subscriptions-resume-and-incremental-delivery/index.md) | How can real-time graph results remain authorized, bounded, and recoverable across disconnects? | Deliver resumable run updates with gap and duplicate handling. |
| 10 | [Schema Evolution, Federation, Governance, and Final Defense](module-10-schema-evolution-federation-governance-and-final-defense/index.md) | How does the graph evolve without breaking clients, erasing service ownership, or becoming an ungoverned platform? | Approve Graph API 1.0, reject breaking candidates, and publish Course 10 handoff. |

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- direct database joins by the graph gateway;
- unbounded arbitrary query execution;
- using GraphQL to replace every existing interface;
- federation without ownership evidence;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 9, read each chapter around the question **How can clients select graph-shaped data and operations without moving business ownership, authorization, cost, or consistency into an uncontrolled gateway?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
