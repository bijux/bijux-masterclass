# Two-Week Study Plan — GraphQL Schema and Runtime Engineering

## Rhythm

Course 9 uses ten teaching days over two weeks. Orientation freezes the incoming boundary before Day 1; each day moves from the compose governed client-shaped capabilities model to transfer problems, a controlled experiment, and an evidence defense. The middle weekend is for repairing failed checkpoints, not adding features.

| Day | Module | Required result |
|---:|---|---|
| 1 | [Graph Interface Placement and the Operation Lifecycle](module-01-graph-interface-placement-and-operation-lifecycle/index.md) | Publish the graph boundary and operation-lifecycle trace. |
| 2 | [Type System, Nullability, and Semantic Modeling](module-02-type-system-nullability-and-semantic-modeling/index.md) | Release Analysis Graph API 1.0 type and nullability policies. |
| 3 | [Resolver Architecture, Batching, and Source Ownership](module-03-resolver-architecture-batching-and-source-ownership/index.md) | Replace N+1 nested calls with request-scoped batching. |
| 4 | [Queries, Identifiers, Connections, and Pagination](module-04-queries-identifiers-connections-and-pagination/index.md) | Implement global IDs and stable, bound connections. |
| 5 | [Mutations, Idempotency, Concurrency, and Domain Results](module-05-mutations-idempotency-concurrency-and-domain-results/index.md) | Expose idempotent create/start/cancel mutations over owning services. |
| 6 | [Authorization, Tenancy, and Schema Exposure](module-06-authorization-tenancy-and-schema-exposure/index.md) | Prove field, tenant, collection, and sensitive-output authorization. |
| 7 | [Demand Control, Persisted Operations, and Caching](module-07-demand-control-persisted-operations-and-caching/index.md) | Admit only bounded trusted operations and record cost evidence. |
| 8 | [Errors, Partial Data, Consistency, and Observability](module-08-errors-partial-data-consistency-and-observability/index.md) | Return truthful partial data with path-specific errors and traces. |
| 9 | [Subscriptions, Resume, and Incremental Delivery](module-09-subscriptions-resume-and-incremental-delivery/index.md) | Deliver resumable run updates with gap and duplicate handling. |
| 10 | [Schema Evolution, Federation, Governance, and Final Defense](module-10-schema-evolution-federation-governance-and-final-defense/index.md) | Approve Graph API 1.0, reject breaking candidates, and publish Course 10 handoff. |

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

The two-week schedule is subordinate to evidence. If the compose governed client-shaped capabilities argument becomes unclear, stop at the last green checkpoint, reduce the counterexample, and resume only after the owning mechanism is understood.

## Weekend synthesis

At the Week 1 boundary, reconstruct how Modules 1–5 change the platform while preserving this incoming state: The Course 8 distributed architecture handoff with explicit service, data, contract, and trust boundaries. Rerun those checkpoints and postpone every feature that does not serve the Course 9 responsibility.

## Recovery route

When a checkpoint fails:

1. isolate the first broken invariant;
2. restore the predecessor baseline if necessary;
3. reduce the failing case;
4. repair the owning mechanism;
5. retain the case as a regression;
6. update your explanation before continuing.
