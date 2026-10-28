# Reference Answers — Module 02: Domain State and Invariants

Read after attempting all twelve Domain State and Invariants exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is a run status enum insufficient by itself?

It closes the vocabulary but does not define legal transitions, state-specific fields, idempotent commands, or race outcomes. Those require an explicit policy.

## 2. Can a failed run return to queued for retry? State the course decision and alternative.

In the frozen public model failed is terminal. Internal job attempts may retry before the run is declared failed. A new public retry operation would require a future contract decision.

## 3. Why does progress 100 imply completion?

Otherwise clients observe a completed measure with a non-terminal lifecycle. The invariant keeps progress and state semantically coherent.

## 4. What is emitted when the same idempotent cancellation request is repeated?

The system may return the same accepted state without creating a second logical transition event. Exact behavior must be explicit and consistent.

## 5. Distinguish cancellation requested from cancelled.

Requested is durable intent awaiting worker observation; cancelled is a terminal result after the active execution acknowledges the request before committing completion.

## 6. Why should event identity be persisted rather than recomputed?

Recomputed identity can change across retries or serialization and prevents receivers from deduplicating the same logical event.

## 7. Classify a stale ETag and malformed ETag.

A malformed validator is invalid request syntax/validation. A syntactically valid validator that no longer matches is 412 Precondition Failed.

## 8. Why conceal foreign ownership as 404?

It prevents callers from learning whether another principal’s resource exists. The query and error mapping must implement that policy consistently.

## 9. Design a property for progress sequences.

Starting at an allowed value, every accepted update must be within bounds and not less than the previous value; 100 is accepted only with completion.

## 10. Where should an event timestamp be assigned?

At application orchestration/persistence when an accepted transition is recorded, using the injected clock—not inside the pure transition function.

## 11. Trace domain invariants and canonical values in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/domain.py` and `capstone/tracks/typescript-fastify/src/domain.ts`. The required invariant is that both tracks reject illegal run transitions and produce identical canonical bytes for fingerprints.

## 12. Compare domain invariants and canonical values across Python and TypeScript

Both tracks must preserve this invariant: both tracks reject illegal run transitions and produce identical canonical bytes for fingerprints. The intentional difference is that Python uses dataclasses and enums; TypeScript uses readonly types and discriminated unions.
