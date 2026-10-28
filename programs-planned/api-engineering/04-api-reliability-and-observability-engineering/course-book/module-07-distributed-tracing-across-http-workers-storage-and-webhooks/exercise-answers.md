# Worked Answers — Module 07: Distributed Tracing Across Asynchronous Work

Use these solutions to audit your reasoning for **Distributed Tracing Across Asynchronous Work**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why should a durable worker usually not be a direct child of the request span?

It has an independent lifetime and may execute after the request, process, or trace sampling decision. A link preserves causality without false nesting.

The chapter’s decisive distinction is this: Begin with the failure Worker as long HTTP child . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design End the request after durable 202. Store accepted trace context with the job. Start a worker trace or root span linked to that context and record queue delay separately.

## 2. Where should trace context be stored for a job?

In a bounded validated durable field associated with the enqueue event/job, separate from business authority and safe to omit.

In the cumulative capstone, the rule becomes concrete: Apply Span relationship, Propagation carrier, Queue timing to this module’s capstone increment: Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits. State one misleading green signal and the durable observation that would overrule it.

## 3. How do you measure queue delay?

From durable enqueue timestamp to claim/start timestamp, represented separately from processing duration.

**Common mistake.** Describing a procedure for “How do you measure queue delay?” without a falsifiable completion condition.

A useful way to reason about the boundary is: A trace models causal execution, not merely shared identifiers. Synchronous work uses parent-child relationships; durable asynchronous work often uses links and new roots so queue delay, retries, and independent lifetimes remain truthful.

## 4. What does a span status of error mean?

The instrumented operation failed its semantic contract; it does not by itself decide the overall business transaction or HTTP response.

The implementation consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=07 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 5. Should every retry be a new trace?

Not necessarily. It should be a distinct attempt span; independent scheduled retries may use a new trace linked to the logical delivery/event.

**Common mistake.** Giving an unconditional answer to “Should every retry be a new trace?” without classifying responsibility and failure semantics.

The important nuance is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=07 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 6. Why can head sampling miss important failures?

The decision occurs before the later outcome. Tail sampling can retain based on outcome but depends on collector buffering and capacity.

Under concurrency or failure, the distinction becomes: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=07 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 7. May run ID be a span attribute?

Potentially as reviewed diagnostic detail because trace storage already has per-span cardinality, but privacy, size, and retention still apply; never assume it is safe or use it as a metric label.

The design remains honest only if: Apply Span relationship, Propagation carrier, Queue timing to this module’s capstone increment: Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits. State one misleading green signal and the durable observation that would overrule it.

## 8. What if context extraction fails from a job row?

Start a new trace, record a bounded invalid-context reason, and continue correct durable processing.

The consumer-facing consequence is: Begin with the failure Worker as long HTTP child . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design End the request after durable 202. Store accepted trace context with the job. Start a worker trace or root span linked to that context and record queue delay separately.

## 9. How should webhook delivery be linked?

The delivery/attempt trace links to the terminal outbox event and injects validated trace context into the outbound HTTP request if policy permits.

**Common mistake.** Describing a procedure for “How should webhook delivery be linked?” without a falsifiable completion condition.

The operational consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=07 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 10. What proves an artifact was published?

Immutable content and committed artifact metadata, not a storage span reporting success.

The strongest engineering interpretation is: A trace models causal execution, not merely shared identifiers. Synchronous work uses parent-child relationships; durable asynchronous work often uses links and new roots so queue delay, retries, and independent lifetimes remain truthful.

**Counterexample.** A component-level green signal hides a stalled or divergent end-to-end user journey.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 11. Trace trace context across asynchronous work in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/context.py` and `capstone/tracks/typescript-fastify/src/reliability/context.ts`. The required invariant is that untrusted incoming context is validated; synchronous work uses parentage and durable asynchronous work uses links plus attempt identity.

The defect-oriented view is: A trace models causal execution, not merely shared identifiers. Synchronous work uses parent-child relationships; durable asynchronous work often uses links and new roots so queue delay, retries, and independent lifetimes remain truthful.

## 12. Compare trace context across asynchronous work across Python and TypeScript

Both tracks must preserve this invariant: untrusted incoming context is validated; synchronous work uses parentage and durable asynchronous work uses links plus attempt identity. The intentional difference is that OpenTelemetry SDK calls differ; trace IDs, links, and privacy-safe attributes follow one topology.

Across the Python and TypeScript tracks, the invariant is: Apply Span relationship, Propagation carrier, Queue timing to this module’s capstone increment: Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits. State one misleading green signal and the durable observation that would overrule it.
