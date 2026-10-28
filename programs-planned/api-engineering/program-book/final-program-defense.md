# Final Program Defense

## Purpose

The final defense is not a slide presentation. It is a sequence of claims and evidence showing that the same Analysis Runs Platform remains coherent across ten layers.

## Required demonstrations

1. Trace one public HTTP operation from OpenAPI contract to durable state and client behavior.
2. Demonstrate idempotent replay, stale conditional update rejection, and worker recovery.
3. Reject a hostile identity, cross-tenant access, unsafe upload, and forbidden outbound destination.
4. Diagnose a failed critical journey from structured events, metrics, and traces without treating telemetry as business truth.
5. Compare a baseline and candidate workload and reject a faster-but-wrong release.
6. Publish and consume an event with duplicate delivery, inbox deduplication, and bounded replay.
7. Execute unary and streaming RPC behavior with deadline, cancellation, flow-control, and compatibility evidence.
8. Defend one service extraction and reject one distributed-monolith candidate.
9. Execute a persisted GraphQL operation with batching, authorization, demand control, and truthful partial data.
10. Publish the portfolio through the catalog, registry, lifecycle, documentation, sandbox, SDK, runtime, and support workflows.

## Non-compensable failures

The program cannot pass while any of these remain:

- an earlier handoff was rewritten;
- public behavior differs across supported providers without a declared release;
- a tenant can observe or mutate another tenant’s resource;
- accepted work can disappear silently;
- a benchmark omits missing outcomes or compares unlike environments;
- a consumer effect can duplicate without detection;
- a service boundary has multiple writers for one business fact;
- graph demand is unbounded or authorization occurs after protected I/O;
- governance accepts missing blocker evidence through an average score;
- the evidence report claims an environment-dependent proof that was not run.

## Graduation artifact

The final dossier contains the version ledger, contracts, ownership map, release decisions, residual risks, consumer migration state, runtime reconciliation, support model, and exact evidence boundary.
