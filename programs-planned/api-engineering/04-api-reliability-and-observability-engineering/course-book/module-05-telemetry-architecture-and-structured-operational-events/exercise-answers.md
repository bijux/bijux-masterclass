# Reference Answers — Module 05: Telemetry Architecture and Structured Events

Read after attempting all twelve Telemetry Architecture and Structured Events exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why are logs, metrics, and traces not interchangeable?

**Answer.** They preserve different shapes: discrete detail, aggregate populations, and causal execution. Forcing one shape into another creates cardinality, cost, or missing-context defects.

## 2. What should happen when an incoming traceparent is invalid?

**Answer.** Start a new trusted trace context, optionally record a bounded invalid-context reason, and never echo the raw value into labels.

## 3. May tenant ID be a trace attribute?

**Answer.** Only after privacy and cardinality review; prefer pseudonymized or bounded identifiers and never use it as a metric label by default.

## 4. Why redact before buffering?

**Answer.** Every local copy is an exposure surface. Remote redaction cannot remove secrets already written to memory dumps, files, or stdout.

## 5. What is the correct customer behavior during collector outage?

**Answer.** Customer work continues when authoritative dependencies are healthy; bounded telemetry may be dropped and the drop count is surfaced locally.

## 6. Should baggage carry an access token?

**Answer.** No. Baggage propagates widely and may be logged or exported. Authentication remains in the protected request boundary.

**Common mistake.** Giving an unconditional answer to “Should baggage carry an access token?” without classifying responsibility and failure semantics.

## 7. How should elapsed time be measured?

**Answer.** With a monotonic clock within a process. Wall timestamps support human correlation but not trusted duration across clock adjustments.

**Common mistake.** Describing a procedure for “How should elapsed time be measured?” without a falsifiable completion condition.

## 8. What does a trace ID prove?

**Answer.** It correlates evidence that claims the same trace; it does not prove an operation committed, succeeded, or even emitted all spans.

## 9. Why version event names and fields?

**Answer.** Queries, alerts, dashboards, and incident tools depend on semantics. Versioning prevents silent meaning changes.

## 10. When is dropping telemetry acceptable?

**Answer.** When buffers are bounded and customer correctness is independent; drops must be counted and important audit/security evidence may require a separate durable path.

## 11. Trace bounded structured telemetry in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/telemetry.py` and `capstone/tracks/typescript-fastify/src/reliability/telemetry.ts`. The required invariant is that events use versioned names and bounded attributes, are recursively redacted, and never replace durable business records.

## 12. Compare bounded structured telemetry across Python and TypeScript

Both tracks must preserve this invariant: events use versioned names and bounded attributes, are recursively redacted, and never replace durable business records. The intentional difference is that logging/export APIs differ; the serialized safe event contract is shared.
