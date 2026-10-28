# Event-Driven Job Engine

## Product

Build a dependency-aware job engine that combines graph validation, bounded execution, cancellation, typed lifecycle events, and deterministic reconciliation. This is an independent integration product, not a simplified alias for TaskHarbor.

Read [Module 40](../../course-book/module-40-integrated-event-driven-architecture-and-independent-change/index.md).

## Domain

Each job has a unique ID, dependency IDs, and a lazy async producer. Validate the complete graph before invoking any producer. Reject unknown dependencies, self-dependency, and cycles with causal messages.

## Scheduler contract

A job becomes ready only after all dependencies succeed. A failed or cancelled dependency blocks the job. Active jobs never exceed the positive concurrency limit. External cancellation stops new starts and is forwarded to running jobs. Every accepted job receives exactly one source-ordered terminal outcome.

## Event contract

Publish immutable `started`, `succeeded`, `failed`, `blocked`, and `cancelled` events after the corresponding authoritative transition. The event callback is observational; it may not mutate scheduler state. State how observer throw is handled.

## Required tests

Cover empty graph, duplicate ID, unknown dependency, cycle, linear chain, diamond graph, independent reverse completion, failure blocking, cancellation with running siblings, concurrency 1 and 3, and exact terminal accounting. Tests should control completion with deferred promises rather than elapsed time.

## Compatibility fixture

Keep one manifest from before the independent feature and prove the new implementation either accepts it with defined defaults or rejects it with a versioned migration message. Silent reinterpretation is not accepted.

## Process-level acceptance

Run the real CLI over a manifest containing dependencies, mixed durations, one failure, and a shutdown request. Assert stable source-ordered reporting, one terminal result per accepted task, bounded completion, and the documented exit status.

## Independent extension

Add resource labels so two jobs with the same exclusive label cannot run together even when global capacity remains. Map the change through domain model, readiness, running-state bookkeeping, tests, and documentation. Preserve source-ordered output and complete accounting.

## Implementation stages

Validate the graph completely before execution. Implement ready-state derivation and indexed terminal storage. Add finite running capacity, cancellation, and events. Test temporal invariants with controlled producers. Add the exclusive-resource extension only after the base scheduler is proven.

## Review questions

Which facts have one authority? Which invariants are temporal? Can an observer change execution? How does the engine prove complete terminal accounting? Which change surfaces does the resource-label extension affect?

## Completion evidence

Submit the authority map, temporal test plan, graph adversarial tests, reversed-completion tests, cancellation trace, and extension impact map. The final defense should identify the exact boundary where Course 5 starts.

## Architecture dossier

Submit an authority map, task-state transition table, promise-ownership ledger, cancellation tree, event schema, context schema, capacity equation, lifecycle state machine, and deterministic-output policy. Each artifact must reference the tests that establish it.

The independent extension must change at least validation, scheduling, public output, and tests. Merely adding a field to a type does not pass. Include one unsupported claim that remains outside Course 4 and identify the later mechanism required to establish it.
