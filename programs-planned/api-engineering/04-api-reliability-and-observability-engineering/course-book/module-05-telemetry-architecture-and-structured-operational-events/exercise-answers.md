# Worked Answers — Module 05: Telemetry Architecture and Structured Events

Use these solutions to audit your reasoning for **Telemetry Architecture and Structured Events**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why are logs, metrics, and traces not interchangeable?

They preserve different shapes: discrete detail, aggregate populations, and causal execution. Forcing one shape into another creates cardinality, cost, or missing-context defects.

The chapter’s decisive distinction is this: Apply Signal purpose, Telemetry schema, Trace context to this module’s capstone increment: Define the telemetry schema, W3C trace-context boundary, structured event vocabulary, redaction policy, bounded exporters, and collector-failure behavior across API, worker, storage, and webhook paths. State one misleading green signal and the durable observation that would overrule it.

## 2. What should happen when an incoming traceparent is invalid?

Start a new trusted trace context, optionally record a bounded invalid-context reason, and never echo the raw value into labels.

In the cumulative capstone, the rule becomes concrete: Begin with the failure Secret enters batch buffer . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Apply recursive structural and pattern redaction before enqueue. Test the sink contents, not only exported output. , and rerun the focused regression in both languages.

## 3. May tenant ID be a trace attribute?

Only after privacy and cardinality review; prefer pseudonymized or bounded identifiers and never use it as a metric label by default.

A useful way to reason about the boundary is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=05 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 4. Why redact before buffering?

Every local copy is an exposure surface. Remote redaction cannot remove secrets already written to memory dumps, files, or stdout.

The implementation consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=05 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 5. What is the correct customer behavior during collector outage?

Customer work continues when authoritative dependencies are healthy; bounded telemetry may be dropped and the drop count is surfaced locally.

The important nuance is: Apply Signal purpose, Telemetry schema, Trace context to this module’s capstone increment: Define the telemetry schema, W3C trace-context boundary, structured event vocabulary, redaction policy, bounded exporters, and collector-failure behavior across API, worker, storage, and webhook paths. State one misleading green signal and the durable observation that would overrule it.

## 6. Should baggage carry an access token?

No. Baggage propagates widely and may be logged or exported. Authentication remains in the protected request boundary.

**Common mistake.** Giving an unconditional answer to “Should baggage carry an access token?” without classifying responsibility and failure semantics.

Under concurrency or failure, the distinction becomes: Begin with the failure Secret enters batch buffer . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Apply recursive structural and pattern redaction before enqueue. Test the sink contents, not only exported output. , and rerun the focused regression in both languages.

## 7. How should elapsed time be measured?

With a monotonic clock within a process. Wall timestamps support human correlation but not trusted duration across clock adjustments.

**Common mistake.** Describing a procedure for “How should elapsed time be measured?” without a falsifiable completion condition.

The design remains honest only if: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=05 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 8. What does a trace ID prove?

It correlates evidence that claims the same trace; it does not prove an operation committed, succeeded, or even emitted all spans.

The consumer-facing consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=05 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 9. Why version event names and fields?

Queries, alerts, dashboards, and incident tools depend on semantics. Versioning prevents silent meaning changes.

The operational consequence is: Apply Signal purpose, Telemetry schema, Trace context to this module’s capstone increment: Define the telemetry schema, W3C trace-context boundary, structured event vocabulary, redaction policy, bounded exporters, and collector-failure behavior across API, worker, storage, and webhook paths. State one misleading green signal and the durable observation that would overrule it.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 10. When is dropping telemetry acceptable?

When buffers are bounded and customer correctness is independent; drops must be counted and important audit/security evidence may require a separate durable path.

The strongest engineering interpretation is: Begin with the failure Secret enters batch buffer . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Apply recursive structural and pattern redaction before enqueue. Test the sink contents, not only exported output. , and rerun the focused regression in both languages.

## 11. Trace bounded structured telemetry in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/telemetry.py` and `capstone/tracks/typescript-fastify/src/reliability/telemetry.ts`. The required invariant is that events use versioned names and bounded attributes, are recursively redacted, and never replace durable business records.

The defect-oriented view is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=05 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 12. Compare bounded structured telemetry across Python and TypeScript

Both tracks must preserve this invariant: events use versioned names and bounded attributes, are recursively redacted, and never replace durable business records. The intentional difference is that logging/export APIs differ; the serialized safe event contract is shared.

Across the Python and TypeScript tracks, the invariant is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=05 TRACK=typescript and explain why the same public and durable outcome holds in the other language.
