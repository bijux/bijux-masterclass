# Module 07 — Distributed Tracing Across Asynchronous Work

> **Program stage:** Course 4 of 6 — Operate and recover the promise.

> **Central question:** How does trace context cross HTTP, queues, workers, storage, retries, and webhooks without inventing false parentage?

## Where this module fits

Validate trace context, use parent-child relationships for synchronous calls, and links for durable asynchronous continuation. You arrive from Module 06 with all earlier checkpoints still green. API 1.2 and security profile 1.0 are fixed. This course adds budgets, telemetry, recovery, and operational decisions; observations may explain durable truth but never replace it. The result is the baseline for **SLOs, Error Budgets, Dashboards, and Alerts**.

## Learning outcomes

- Parse and validate W3C trace context.
- Create bounded span names and attributes.
- Represent queue and worker attempts accurately.
- Link asynchronous work to durable causation.
- Understand sampling and missing-span limits.

## Capstone result

Implement validated context, synchronous parent-child spans, asynchronous links, attempts, queue time, and privacy-safe attributes.

One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.

## Core reliability model

### Driving question

> How do we reconstruct causality across synchronous calls, durable queues, workers, storage, and webhooks without inventing parentage or exposing sensitive context?

A trace models causal execution, not merely shared identifiers. Synchronous work uses parent-child relationships; durable asynchronous work often uses links and new roots so queue delay, retries, and independent lifetimes remain truthful.

### 1. Span relationship

Parent-child expresses nested causal work within one execution lifetime. Links associate work that is causally related but independently scheduled or multiply sourced.

**Failure if confused.** Making a worker span a days-long child of the HTTP request distorts duration and cancellation semantics.
### 2. Propagation carrier

Trace context crosses HTTP headers or durable message/job fields through explicit inject/extract boundaries.

**Failure if confused.** Relying on process-local async context loses correlation after queue persistence or restart.
### 3. Queue timing

Enqueue, queue delay, claim, processing, and acknowledgement are distinct intervals.

**Failure if confused.** One worker span from acceptance to completion hides whether latency came from backlog or execution.
### 4. Attempt identity

Retries are separate attempts linked to one logical operation. Attempt number is bounded; run ID remains diagnostic detail rather than a metric label.

**Failure if confused.** Overwriting one span across retries loses failure history.
### 5. Span status and errors

Status summarizes whether the operation met its semantic outcome; exception events carry sanitized details. HTTP status alone is not always the semantic result.

**Failure if confused.** A handled 404 lookup may be expected while a 200 response with corrupt artifact is failure.
### 6. Sampling

Head sampling decides before later outcome; tail sampling can use outcome but requires a collector path. Sampling policy changes visibility, not correctness.

**Failure if confused.** Assuming every failed run has a retained trace makes diagnosis brittle.
### 7. Clock skew

Trace visualization across hosts depends on clocks and collector correction. Durations within spans use monotonic timing.

**Failure if confused.** Comparing wall timestamps can show child work before parent.
### 8. Context privacy

Trace attributes and baggage pass through many systems. Values are bounded, redacted, and not authorization evidence.

**Failure if confused.** Adding dataset filename or access token to every span distributes sensitive data.

For a new Analysis Runs failure:

Apply **Span relationship, Propagation carrier, Queue timing** to this module’s capstone increment: Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Validate context at every trust boundary | Extract only the supported trace-context profile and start clean on invalid input. | Async child misuse: Trace appears hours long and cancellation semantics lie | `trace vectors` |
| 2 | Use links for durable asynchronous handoff | Worker execution starts independently and links to accepted/enqueue context. | Context lost at queue: Worker cannot correlate accepted request | `trace topology test` |
| 3 | Separate queue delay from processing | Enqueue, claim, and execution timings are distinct. | Queue time hidden: Execution blamed for backlog | `span model review` |
| 4 | Represent every retry as an attempt | Attempts have separate spans and bounded attempt attributes. | Retry span overwritten: Failure history disappears | `retry trace fixture` |
| 5 | Keep attributes bounded and redacted | No raw secrets, payloads, filenames, or unbounded identifiers are default attributes. | Sensitive attributes: Trace backend receives secrets | `attribute schema guard` |
| 6 | Do not require traces for correctness | Durable reconciliation passes even when all spans are dropped. | Trace required for correctness: Sampling changes reconciliation | `sampling-loss test` |
| 7 | Propagate across outbox and webhook | Delivery trace links to the terminal domain event and creates a client span for the outbound call. | Invalid context trusted: Caller controls correlation identity | `webhook trace scenario` |
| 8 | Document sampling semantics | Head/tail policy, expected blind spots, and collector dependence are explicit. | Unbounded span events: One failure floods exporter | `sampling profile` |


### Evidence boundary

Deterministic contexts prove propagation rules; backend sampling, clock skew, and trace visualization require live multi-process execution.

## Worked failures


### Case 1 — Worker as long HTTP child

#### Initial system

The request span remains open until analysis completes hours later, making the API latency span meaningless and coupling worker execution to client lifetime.


#### Correct design

End the request after durable 202. Store accepted trace context with the job. Start a worker trace or root span linked to that context and record queue delay separately.


#### Lesson

Durable asynchronous work has an independent lifetime.
### Case 2 — Retry overwritten

#### Initial system

Webhook attempts reuse one span ID and update its attributes. Only the final outcome remains.


#### Correct design

Create one logical delivery span or trace with separate attempt spans, preserving failure class, delay, peer, and final acknowledgement.


#### Lesson

Attempts are evidence, not mutable state.
### Case 3 — Trace loss called data loss

#### Initial system

A sampled-out completion trace leads operators to conclude the run never completed.


#### Correct design

Query durable terminal state and artifact checksum first; use trace availability as a diagnostic quality signal.


#### Lesson

Missing evidence is not negative business evidence.
### Case 4 — Baggage carries tenant role

#### Initial system

A role is copied into baggage and downstream services authorize from it. A caller injects a higher role.


#### Correct design

Authorization uses validated identity/policy state. Baggage is ignored for privilege and may be rejected entirely.


#### Lesson

Propagation is not trust delegation.

## Python implementation

### Mechanism under review

Use contextvars and explicit durable carriers to build a linked worker trace model; keep OTel SDK integration optional and prove reconciliation without spans.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/context.py`
- `capstone/tracks/python-fastapi/src/api_reliability/otel_adapter.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_context_deadline.py`

### Executable invariant

```python
from api_reliability.context import parse_traceparent

context = parse_traceparent(
    "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
)
child = context.child("b7ad6b7169203331")
assert child.trace_id == context.trace_id
assert child.span_id != context.span_id
```

The cited files own the complete implementation and regression evidence.

### Guided failure investigation — Worker as long HTTP child

**Initial condition.** The request span remains open until analysis completes hours later, making the API latency span meaningless and coupling worker execution to client lifetime.

**Expected repair.** End the request after durable 202. Store accepted trace context with the job. Start a worker trace or root span linked to that context and record queue delay separately.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=07 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **Async child misuse.** Trace appears hours long and cancellation semantics lie The decisive check is topology review.
- **Context lost at queue.** Worker cannot correlate accepted request The decisive check is durable propagation vector.
- **Queue time hidden.** Execution blamed for backlog The decisive check is separate timing spans.
- **Retry span overwritten.** Failure history disappears The decisive check is attempt-span count.
- **Sensitive attributes.** Trace backend receives secrets The decisive check is redaction scan.
- **Trace required for correctness.** Sampling changes reconciliation The decisive check is drop-all-traces test.

## TypeScript implementation

### Mechanism under review

Use AsyncLocalStorage for in-process propagation and explicit serialized context for jobs; distinguish promise ancestry from trace parentage and test restart loss.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/context.ts`
- `capstone/tracks/typescript-fastify/src/reliability-otel.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/context-deadline.test.mjs`

### Executable invariant

```typescript
const context = parseTraceparent(
  "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
);
const child = childOf(context, "b7ad6b7169203331");
if (child.traceId !== context.traceId) throw new Error("trace disconnected");
```

The cited files own the complete implementation and regression evidence.

### Guided failure investigation — Worker as long HTTP child

**Initial condition.** The request span remains open until analysis completes hours later, making the API latency span meaningless and coupling worker execution to client lifetime.

**Expected repair.** End the request after durable 202. Store accepted trace context with the job. Start a worker trace or root span linked to that context and record queue delay separately.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=07 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **Async child misuse.** Trace appears hours long and cancellation semantics lie The decisive check is topology review.
- **Context lost at queue.** Worker cannot correlate accepted request The decisive check is durable propagation vector.
- **Queue time hidden.** Execution blamed for backlog The decisive check is separate timing spans.
- **Retry span overwritten.** Failure history disappears The decisive check is attempt-span count.
- **Sensitive attributes.** Trace backend receives secrets The decisive check is redaction scan.
- **Trace required for correctness.** Sampling changes reconciliation The decisive check is drop-all-traces test.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **Async child misuse** | A queued task is recorded as a child span for convenience. | The trace implies overlapping synchronous execution that never occurred. | A timeline assertion is absent. | topology review. |
| **Context lost at queue** | Only the payload is persisted. | The asynchronous effect cannot be related to its cause. | A unit test invokes the worker directly with in-memory context. | durable propagation vector. |
| **Queue time hidden** | Only processing spans are instrumented. | Backlog delay disappears from the journey. | An empty queue makes waiting negligible. | separate timing spans. |
| **Retry span overwritten** | One span is reused for the logical operation. | Attempt count, delay, and failure ownership become invisible. | No retry occurs in the normal case. | attempt-span count. |
| **Sensitive attributes** | Rich payload attributes accelerate debugging. | Secrets or personal data enter exporters and retention systems. | Assertions inspect names, not sensitive values. | redaction scan. |
| **Trace required for correctness** | Trace IDs are convenient correlation keys. | Sampling or telemetry loss breaks business processing. | Local tests sample every trace. | drop-all-traces test. |
| **Invalid context trusted** | All inbound propagation is accepted. | Malformed identifiers and flags poison the trace graph. | Trusted fixtures are valid. | parser vectors. |
| **Unbounded span events** | Every retry or item can be attached for detail. | A large operation creates oversized spans and exporter pressure. | Small fixtures produce few events. | event-count guard. |

## What you add to the capstone

### Increment

Trace API ingress, PostgreSQL calls, job enqueue/claim, worker attempts, artifact publication, outbox dispatch, and webhook acknowledgement with validated context, links, bounded attributes, and explicit sampling limits.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/context.py`
- `capstone/tracks/python-fastapi/src/api_reliability/otel_adapter.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_context_deadline.py`
- `capstone/tracks/typescript-fastify/src/reliability/context.ts`
- `capstone/tracks/typescript-fastify/src/reliability-otel.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/context-deadline.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Validate context at every trust boundary.** Extract only the supported trace-context profile and start clean on invalid input.
- **Use links for durable asynchronous handoff.** Worker execution starts independently and links to accepted/enqueue context.
- **Separate queue delay from processing.** Enqueue, claim, and execution timings are distinct.
- **Represent every retry as an attempt.** Attempts have separate spans and bounded attempt attributes.
- The planted failure **Worker as long HTTP child** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Worker as long HTTP child**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **End the request after durable 202. Store accepted trace context with the job. Start a worker trace or root span linked to that context and record queue delay separately.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How do we reconstruct causality across synchronous calls, durable queues, workers, storage, and webhooks without inventing parentage or exposing sensitive context?” is decided by durable state rather than telemetry?
2. What is the smallest fault that disproves the design?
3. Which label, context value, or event field could become unbounded?
4. What happens after restart halfway through the operation?
5. Which Course 3 security constraint could observability violate?
6. Which proof is local and which needs a live environment?
7. How do the two tracks preserve the same invariant idiomatically?
8. What behavior would block release despite OpenAPI compatibility?

### Required artifacts

Record `accept`, `accept-with-residual-risk`, or `reject`. A rejection names the failed requirement and exact evidence needed for reconsideration.

## Representative implementation

These are the smallest useful entry points for **Distributed Tracing Across Asynchronous Work**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/context.py`

```python
from __future__ import annotations

from dataclasses import dataclass
import re
import secrets

_TRACEPARENT = re.compile(
    r"^(?P<version>[0-9a-f]{2})-(?P<trace>[0-9a-f]{32})-"
    r"(?P<span>[0-9a-f]{16})-(?P<flags>[0-9a-f]{2})$"
)
_HEX_ZERO_32 = "0" * 32
_HEX_ZERO_16 = "0" * 16


class TraceContextError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class TraceContext:
    trace_id: str
    span_id: str
    sampled: bool = False
    tracestate: str | None = None
    remote: bool = False

    def traceparent(self) -> str:
        flags = "01" if self.sampled else "00"
        return f"00-{self.trace_id}-{self.span_id}-{flags}"

    def child(self, span_id: str | None = None) -> "TraceContext":
        value = span_id or secrets.token_hex(8)
        _validate_hex(value, 16, "span-id")
        return TraceContext(
            trace_id=self.trace_id,
            span_id=value,
            sampled=self.sampled,
            tracestate=self.tracestate,
            remote=False,
        )


def _validate_hex(value: str, length: int, label: str) -> None:
    if len(value) != length or not re.fullmatch(r"[0-9a-f]+", value):
        raise TraceContextError(f"invalid {label}")
    if set(value) == {"0"}:
        raise TraceContextError(f"zero {label} is invalid")


def parse_traceparent(value: str) -> TraceContext:
    """Parse the course's strict W3C Trace Context version-00 profile.

    The course deliberately does not claim to implement future-version parsing.
    Unknown versions are rejected instead of being silently reinterpreted.
    """

    match = _TRACEPARENT.fullmatch(value.strip())
    if not match:
        raise TraceContextError("malformed traceparent")
    if match.group("version") != "00":
        raise TraceContextError("unsupported traceparent version")
    trace_id = match.group("trace")
    span_id = match.group("span")
    if trace_id == _HEX_ZERO_32 or span_id == _HEX_ZERO_16:
        raise TraceContextError("zero trace or span identifier")
    flags = int(match.group("flags"), 16)
    return TraceContext(
        trace_id=trace_id,
        span_id=span_id,
        sampled=bool(flags & 0x01),
        remote=True,
    )


def new_root(*, sampled: bool = False) -> TraceContext:
    return TraceContext(
        trace_id=secrets.token_hex(16),
        span_id=secrets.token_hex(8),
        sampled=sampled,
    )
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/context.ts`

```typescript
import { randomBytes } from "node:crypto";

export class TraceContextError extends Error {}

export interface TraceContext {
  readonly traceId: string;
  readonly spanId: string;
  readonly sampled: boolean;
  readonly remote: boolean;
}

const TRACEPARENT = /^([0-9a-f]{2})-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$/;

export function parseTraceparent(value: string): TraceContext {
  const match = TRACEPARENT.exec(value.trim());
  if (match === null) throw new TraceContextError("malformed traceparent");
  const [, version, traceId, spanId, flags] = match;
  if (version !== "00") throw new TraceContextError("unsupported traceparent version");
  if (/^0+$/.test(traceId!) || /^0+$/.test(spanId!)) throw new TraceContextError("zero identifier");
  return { traceId: traceId!, spanId: spanId!, sampled: (Number.parseInt(flags!, 16) & 1) === 1, remote: true };
}

export function formatTraceparent(context: TraceContext): string {
  return `00-${context.traceId}-${context.spanId}-${context.sampled ? "01" : "00"}`;
}

export function newRoot(sampled = false): TraceContext {
  return { traceId: randomBytes(16).toString("hex"), spanId: randomBytes(8).toString("hex"), sampled, remote: false };
}

export function childOf(parent: TraceContext, spanId = randomBytes(8).toString("hex")): TraceContext {
  if (!/^[0-9a-f]{16}$/.test(spanId) || /^0+$/.test(spanId)) throw new TraceContextError("invalid span-id");
  return { traceId: parent.traceId, spanId, sampled: parent.sampled, remote: false };
}
```

Compare the two tracks by this invariant: **untrusted incoming context is validated; synchronous work uses parentage and durable asynchronous work uses links plus attempt identity**. The intended implementation difference is: OpenTelemetry SDK calls differ; trace IDs, links, and privacy-safe attributes follow one topology.

## Module synthesis

The module answer to “How do we reconstruct one outcome across HTTP, database, worker, storage, and webhook boundaries without inventing false parentage?” is now executable in the capstone: One run can be followed from client request through worker attempt, artifact publication, outbox dispatch, and receiver acknowledgement.

## Next in the story

Module 08, [SLOs, Error Budgets, Dashboards, and Alerts](../module-08-slos-error-budgets-dashboards-and-alerts/index.md), asks: *How do operational signals become explicit objectives and actionable decisions rather than decorative dashboards?* The current checkpoint must remain green while that new responsibility is added.
