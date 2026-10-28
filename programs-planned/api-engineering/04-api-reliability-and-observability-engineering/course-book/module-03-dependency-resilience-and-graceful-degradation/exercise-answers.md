# Reference Answers — Module 03: Dependency Resilience and Graceful Degradation

Read after attempting all twelve Dependency Resilience and Graceful Degradation exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. When should a circuit breaker not be used?

**Answer.** For local validation, one-off calls, already-fast failures, or when circuit state would hide required correctness rather than protect capacity.

## 2. Why is a bulkhead different from rate limiting?

**Answer.** A bulkhead caps concurrent in-flight work; rate limiting controls admission over time.

## 3. May telemetry export use a circuit?

**Answer.** Yes, to fail fast and protect resources, but export must already be non-authoritative and bounded.

## 4. Can PostgreSQL reads use stale fallback?

**Answer.** Only if public semantics allow staleness and security remains correct; the capstone does not guess run status from telemetry.

## 5. What happens when artifact publication fails?

**Answer.** Do not mark completed. Retry inside policy or fail durably after exhaustion.

## 6. How should half-open probes be selected?

**Answer.** Use a representative bounded preferably side-effect-free operation under a strict deadline.

**Common mistake.** Describing a procedure for “How should half-open probes be selected?” without a falsifiable completion condition.

## 7. Why record transitions rather than unique rejection series?

**Answer.** Transitions are low-volume events; rejection counters use bounded dependency/result labels.

## 8. What makes degradation truthful?

**Answer.** Response and durable state still satisfy documented semantics, with omitted or stale information represented explicitly.

## 9. How can a bulkhead starve work?

**Answer.** One tenant or destination may consume every permit; fairness or partitioning can be required.

**Common mistake.** Describing a procedure for “How can a bulkhead starve work?” without a falsifiable completion condition.

## 10. Should an open circuit affect readiness?

**Answer.** Only if the dependency is required for the traffic the readiness endpoint admits.

**Common mistake.** Giving an unconditional answer to “Should an open circuit affect readiness?” without classifying responsibility and failure semantics.

## 11. Trace dependency-local resilience in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/circuit.py` and `capstone/tracks/typescript-fastify/src/reliability/circuit.ts`. The required invariant is that circuits, bulkheads, retry policy, and degradation apply per dependency and never convert uncertain durable outcomes into success.

## 12. Compare dependency-local resilience across Python and TypeScript

Both tracks must preserve this invariant: circuits, bulkheads, retry policy, and degradation apply per dependency and never convert uncertain durable outcomes into success. The intentional difference is that state-machine mechanics differ; open, half-open, probe, and recovery decisions are shared.
