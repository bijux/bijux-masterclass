# Reference Answers — Module 07: Distributed Tracing Across Asynchronous Work

Read after attempting all twelve Distributed Tracing Across Asynchronous Work exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why should a durable worker usually not be a direct child of the request span?

**Answer.** It has an independent lifetime and may execute after the request, process, or trace sampling decision. A link preserves causality without false nesting.

## 2. Where should trace context be stored for a job?

**Answer.** In a bounded validated durable field associated with the enqueue event/job, separate from business authority and safe to omit.

## 3. How do you measure queue delay?

**Answer.** From durable enqueue timestamp to claim/start timestamp, represented separately from processing duration.

**Common mistake.** Describing a procedure for “How do you measure queue delay?” without a falsifiable completion condition.

## 4. What does a span status of error mean?

**Answer.** The instrumented operation failed its semantic contract; it does not by itself decide the overall business transaction or HTTP response.

## 5. Should every retry be a new trace?

**Answer.** Not necessarily. It should be a distinct attempt span; independent scheduled retries may use a new trace linked to the logical delivery/event.

**Common mistake.** Giving an unconditional answer to “Should every retry be a new trace?” without classifying responsibility and failure semantics.

## 6. Why can head sampling miss important failures?

**Answer.** The decision occurs before the later outcome. Tail sampling can retain based on outcome but depends on collector buffering and capacity.

## 7. May run ID be a span attribute?

**Answer.** Potentially as reviewed diagnostic detail because trace storage already has per-span cardinality, but privacy, size, and retention still apply; never assume it is safe or use it as a metric label.

## 8. What if context extraction fails from a job row?

**Answer.** Start a new trace, record a bounded invalid-context reason, and continue correct durable processing.

## 9. How should webhook delivery be linked?

**Answer.** The delivery/attempt trace links to the terminal outbox event and injects validated trace context into the outbound HTTP request if policy permits.

**Common mistake.** Describing a procedure for “How should webhook delivery be linked?” without a falsifiable completion condition.

## 10. What proves an artifact was published?

**Answer.** Immutable content and committed artifact metadata, not a storage span reporting success.

## 11. Trace trace context across asynchronous work in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/context.py` and `capstone/tracks/typescript-fastify/src/reliability/context.ts`. The required invariant is that untrusted incoming context is validated; synchronous work uses parentage and durable asynchronous work uses links plus attempt identity.

## 12. Compare trace context across asynchronous work across Python and TypeScript

Both tracks must preserve this invariant: untrusted incoming context is validated; synchronous work uses parentage and durable asynchronous work uses links plus attempt identity. The intentional difference is that OpenTelemetry SDK calls differ; trace IDs, links, and privacy-safe attributes follow one topology.
