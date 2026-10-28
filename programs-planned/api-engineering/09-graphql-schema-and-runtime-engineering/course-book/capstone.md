# Capstone — GraphQL Schema and Runtime Engineering

## Cumulative system

Course 9 continues the Analysis Runs Platform at the point where the previous course stopped. Its capstone exists to compose governed client-shaped capabilities while preserving the same projects, datasets, runs, artifacts, identities, and user journeys.

## Inherited state

The Course 8 distributed architecture handoff with explicit service, data, contract, and trust boundaries.

The inherited boundary is read-only: The Course 8 distributed architecture handoff with explicit service, data, contract, and trust boundaries. A difficult implementation is not permission to rewrite predecessor contracts, migrations, profiles, or evidence; the current course must solve the problem at its own owning layer.

## Course additions

- graph interface placement and operation lifecycle;
- type-system, nullability, resolver, source-ownership, and batching discipline;
- stable identifiers, connections, mutations, idempotency, and policy enforcement;
- persisted operations, demand control, caching, partial data, and observability;
- subscriptions, schema evolution, federation boundaries, and release governance;

## Increment map

| Module | Mechanism | Cumulative result |
|---:|---|---|
| 1 | Graph Interface Placement and the Operation Lifecycle | Publish the graph boundary and operation-lifecycle trace. |
| 2 | Type System, Nullability, and Semantic Modeling | Release Analysis Graph API 1.0 type and nullability policies. |
| 3 | Resolver Architecture, Batching, and Source Ownership | Replace N+1 nested calls with request-scoped batching. |
| 4 | Queries, Identifiers, Connections, and Pagination | Implement global IDs and stable, bound connections. |
| 5 | Mutations, Idempotency, Concurrency, and Domain Results | Expose idempotent create/start/cancel mutations over owning services. |
| 6 | Authorization, Tenancy, and Schema Exposure | Prove field, tenant, collection, and sensitive-output authorization. |
| 7 | Demand Control, Persisted Operations, and Caching | Admit only bounded trusted operations and record cost evidence. |
| 8 | Errors, Partial Data, Consistency, and Observability | Return truthful partial data with path-specific errors and traces. |
| 9 | Subscriptions, Resume, and Incremental Delivery | Deliver resumable run updates with gap and duplicate handling. |
| 10 | Schema Evolution, Federation, Governance, and Final Defense | Approve Graph API 1.0, reject breaking candidates, and publish Course 10 handoff. |

## Implementation route

Build the complete Course 9 increment in one primary track. Use the second track only after the chapter model is clear, then run shared vectors to test whether **compose governed client-shaped capabilities** survives an idiomatic implementation in another runtime.

## Final state

Analysis Graph API 1.0, GraphQL September 2025 schema, persisted operation registry, resolver ownership, demand policy, resumable subscriptions, compatibility gates, and platform-publication metadata.

## Handoff discipline

The successor receives only the settled result: Analysis Graph API 1.0, GraphQL September 2025 schema, persisted operation registry, resolver ownership, demand policy, resumable subscriptions, compatibility gates, and platform-publication metadata. Local caches, secrets, ad-hoc reports, and environment-specific artifacts remain outside the handoff.
