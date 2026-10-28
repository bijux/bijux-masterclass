# Worked Answers — Module 02: Domain State and Invariants

Use these solutions to audit your reasoning for **Domain State and Invariants**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is a run status enum insufficient by itself?

It closes the vocabulary but does not define legal transitions, state-specific fields, idempotent commands, or race outcomes. Those require an explicit policy.

The chapter’s decisive distinction is this: An invariant has one authoritative implementation. Database constraints may reinforce it and transport validation may reject malformed input earlier, but neither should invent a different rule. The state transition policy is the reference for legal run changes.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 2. Can a failed run return to queued for retry? State the course decision and alternative.

In the frozen public model failed is terminal. Internal job attempts may retry before the run is declared failed. A new public retry operation would require a future contract decision.

In the cumulative capstone, the rule becomes concrete: The Domain State and Invariants increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 3. Why does progress 100 imply completion?

Otherwise clients observe a completed measure with a non-terminal lifecycle. The invariant keeps progress and state semantically coherent.

A useful way to reason about the boundary is: Progress may remain the same or increase within a running execution, but it may not decrease. It reaches 100 only with completion. This rule is visible in SSE/NDJSON events and therefore cannot be a UI convention.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 4. What is emitted when the same idempotent cancellation request is repeated?

The system may return the same accepted state without creating a second logical transition event. Exact behavior must be explicit and consistent.

The implementation consequence is: The API records a cancellation request. A worker later observes it before a commit boundary and transitions to cancelled. If completion commits first, cancellation returns a conflict. This gives a deterministic rule for a real race.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 5. Distinguish cancellation requested from cancelled.

Requested is durable intent awaiting worker observation; cancelled is a terminal result after the active execution acknowledges the request before committing completion.

The important nuance is: The API records a cancellation request. A worker later observes it before a commit boundary and transitions to cancelled. If completion commits first, cancellation returns a conflict. This gives a deterministic rule for a real race.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 6. Why should event identity be persisted rather than recomputed?

Recomputed identity can change across retries or serialization and prevents receivers from deduplicating the same logical event.

Under concurrency or failure, the distinction becomes: State summarizes the current truth; an event records that a transition occurred. status=completed is not the same object as analysis.run.completed. Events need stable identifiers and timestamps because streams and webhooks may replay them.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 7. Classify a stale ETag and malformed ETag.

A malformed validator is invalid request syntax/validation. A syntactically valid validator that no longer matches is 412 Precondition Failed.

The design remains honest only if: The same English sentence can map to different protocol meaning. A malformed ID is validation, an absent owned resource is not found, a forbidden transition is conflict, a missing If-Match is precondition required, and a stale validator is precondition failed.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 8. Why conceal foreign ownership as 404?

It prevents callers from learning whether another principal’s resource exists. The query and error mapping must implement that policy consistently.

The consumer-facing consequence is: Claim Required evidence ---: --- --- 1 all source/target transitions classified Write the narrow command and machine-readable oracle. 2 terminal states have no outgoing edges Write the narrow command and machine-readable oracle. 3 progress never decreases Write the narrow command and machine-readable oracle. 4 100 progress requires completion Write the narrow command and machine-readable oracle. 5 cancellation race table deterministic Write the narrow command and machine-readable oracle.

## 9. Design a property for progress sequences.

Starting at an allowed value, every accepted update must be within bounds and not less than the previous value; 100 is accepted only with completion.

The operational consequence is: Artifacts exist only for completed runs. An empty list before completion would ambiguously mean no result versus not ready. The public contract therefore reports lifecycle conflict until completion and returns persisted artifacts afterward.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 10. Where should an event timestamp be assigned?

At application orchestration/persistence when an accepted transition is recorded, using the injected clock—not inside the pure transition function.

The strongest engineering interpretation is: For Domain State and Invariants , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 11. Trace domain invariants and canonical values in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/domain.py` and `capstone/tracks/typescript-fastify/src/domain.ts`. The required invariant is that both tracks reject illegal run transitions and produce identical canonical bytes for fingerprints.

The defect-oriented view is: The excerpt for Domain State and Invariants isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## 12. Compare domain invariants and canonical values across Python and TypeScript

Both tracks must preserve this invariant: both tracks reject illegal run transitions and produce identical canonical bytes for fingerprints. The intentional difference is that Python uses dataclasses and enums; TypeScript uses readonly types and discriminated unions.

Across the Python and TypeScript tracks, the invariant is: The Domain State and Invariants increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior The comparison track must expose the same public outcomes even when internal libraries and control flow differ.
