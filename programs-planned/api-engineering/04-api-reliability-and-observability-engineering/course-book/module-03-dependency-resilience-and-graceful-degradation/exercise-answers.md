# Worked Answers — Module 03: Dependency Resilience and Graceful Degradation

Use these solutions to audit your reasoning for **Dependency Resilience and Graceful Degradation**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. When should a circuit breaker not be used?

For local validation, one-off calls, already-fast failures, or when circuit state would hide required correctness rather than protect capacity.

The chapter’s decisive distinction is this: Apply Dependency contract, Circuit breaker, Bulkhead to this module’s capstone increment: Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified. State one misleading green signal and the durable observation that would overrule it.

## 2. Why is a bulkhead different from rate limiting?

A bulkhead caps concurrent in-flight work; rate limiting controls admission over time.

In the cumulative capstone, the rule becomes concrete: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=03 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Isolate the dependency, force failure and recovery, and inspect breaker state, probe ownership, capacity isolation, truthful partial response, and unaffected journeys.

## 3. May telemetry export use a circuit?

Yes, to fail fast and protect resources, but export must already be non-authoritative and bounded.

A useful way to reason about the boundary is: Begin with the failure Telemetry collector outage . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Use bounded asynchronous export and local drop accounting. Customer requests complete from authoritative state. , and rerun the focused regression in both languages.

## 4. Can PostgreSQL reads use stale fallback?

Only if public semantics allow staleness and security remains correct; the capstone does not guess run status from telemetry.

The implementation consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=03 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 5. What happens when artifact publication fails?

Do not mark completed. Retry inside policy or fail durably after exhaustion.

The important nuance is: Apply Dependency contract, Circuit breaker, Bulkhead to this module’s capstone increment: Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified. State one misleading green signal and the durable observation that would overrule it.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 6. How should half-open probes be selected?

Use a representative bounded preferably side-effect-free operation under a strict deadline.

**Common mistake.** Describing a procedure for “How should half-open probes be selected?” without a falsifiable completion condition.

Under concurrency or failure, the distinction becomes: Begin with the failure Telemetry collector outage . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Use bounded asynchronous export and local drop accounting. Customer requests complete from authoritative state. , and rerun the focused regression in both languages.

## 7. Why record transitions rather than unique rejection series?

Transitions are low-volume events; rejection counters use bounded dependency/result labels.

The design remains honest only if: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=03 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 8. What makes degradation truthful?

Response and durable state still satisfy documented semantics, with omitted or stale information represented explicitly.

The consumer-facing consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=03 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Isolate the dependency, force failure and recovery, and inspect breaker state, probe ownership, capacity isolation, truthful partial response, and unaffected journeys.

## 9. How can a bulkhead starve work?

One tenant or destination may consume every permit; fairness or partitioning can be required.

**Common mistake.** Describing a procedure for “How can a bulkhead starve work?” without a falsifiable completion condition.

The operational consequence is: Apply Dependency contract, Circuit breaker, Bulkhead to this module’s capstone increment: Create policies for PostgreSQL, artifact storage, webhook delivery, and telemetry export; apply circuits, bulkheads, and truthful degradation only where justified. State one misleading green signal and the durable observation that would overrule it.

## 10. Should an open circuit affect readiness?

Only if the dependency is required for the traffic the readiness endpoint admits.

**Common mistake.** Giving an unconditional answer to “Should an open circuit affect readiness?” without classifying responsibility and failure semantics.

The strongest engineering interpretation is: Begin with the failure Telemetry collector outage . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Use bounded asynchronous export and local drop accounting. Customer requests complete from authoritative state. , and rerun the focused regression in both languages.

## 11. Trace dependency-local resilience in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/circuit.py` and `capstone/tracks/typescript-fastify/src/reliability/circuit.ts`. The required invariant is that circuits, bulkheads, retry policy, and degradation apply per dependency and never convert uncertain durable outcomes into success.

The defect-oriented view is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=03 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 12. Compare dependency-local resilience across Python and TypeScript

Both tracks must preserve this invariant: circuits, bulkheads, retry policy, and degradation apply per dependency and never convert uncertain durable outcomes into success. The intentional difference is that state-machine mechanics differ; open, half-open, probe, and recovery decisions are shared.

Across the Python and TypeScript tracks, the invariant is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=03 TRACK=typescript and explain why the same public and durable outcome holds in the other language.
