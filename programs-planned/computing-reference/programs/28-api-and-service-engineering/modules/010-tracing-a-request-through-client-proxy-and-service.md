---
module_id: API-010
program: API & Service Engineering
level: 1
module_number: 10
title: Tracing a Request Through Client, Proxy, and Service
status: complete
last_verified: 2026-09-01
---

# Tracing a Request Through Client, Proxy, and Service

## One-Page Review

### Governing question

How can an engineer reconstruct one request's path, transformations, timing, and outcome across a client, intermediaries, an origin service, and dependencies without mistaking telemetry for authoritative truth?

### Essential definitions

- A **request attempt** is one transmitted occurrence; retries of one logical operation are distinct attempts.
- A **trace** is a causally related graph of recorded operations, commonly represented by spans.
- A **span** records one timed operation with identity, parent/link relationships, attributes, events, status, and resource context.
- **trace context** is propagation metadata, standardized for HTTP by W3C `traceparent` and optional `tracestate`.
- A **route template** is a bounded operation label such as `/orders/{id}`; a raw target can contain secrets and unbounded identifiers.
- **sampling** selects which telemetry to retain; missing spans are not evidence that work did not occur.
- **correlation** links evidence; it does not prove causation, authorization, or completion.

### Central model, mechanism, or theorem

Represent an attempt as a directed acyclic evidence graph $G=(V,E)$, where each vertex is a recorded client, proxy, service, or dependency operation and edges represent declared parentage or links. For path $p$, end-to-end latency is not the sum of all span durations when spans overlap; the critical path is the maximum causal duration through $G$. Gaps, clock error, sampling, buffering, and instrumentation failure bound every conclusion.

### Critical invariants

Assign distinct attempt and logical-operation identities. Validate and regenerate untrusted trace context at trust boundaries according to policy. Preserve method, authority, route template, status, protocol version, and retry evidence consistently. Never log credentials, full sensitive targets, or uncontrolled bodies. Propagate deadlines and cancellation separately from trace context. Record transformations at proxies. Tie application completion claims to authoritative state, not span success alone.

### Common failures

Using one request ID for all retry attempts; treating trace ID as authentication; trusting client-supplied sampling state; naming spans with raw URLs; summing parallel spans; omitting queue time; marking a span successful because transport returned `200`; losing context across asynchronous work; sampling away rare failures; and claiming no dependency call occurred because its span is missing.

### Compact example

A client attempt lasts 180 ms: 20 ms network/edge, 10 ms gateway queue, 130 ms service span, and two parallel dependency spans of 80 and 110 ms. Adding every duration exaggerates latency because work overlaps. The trace shows the 110 ms dependency on the critical path, while logs and operation state determine whether the business effect committed.

### Connections

HTTP messages define what crosses each hop. Version semantics determine connection and stream evidence. Idempotency separates attempts from operations. Later API modules develop observability, gateways, deadlines, retries, and production readiness. Distributed systems supplies partial-observation and clock limits.

## Governing Question

Which evidence lets us follow one request through every ownership boundary, explain its latency and transformations, and determine what is known—or still unknown—about its outcome?

## Why This Matters

A client rarely talks directly to application code. DNS, connection establishment, TLS, an edge proxy, load balancer, gateway, service middleware, database, cache, and downstream services can all contribute latency or failure. A final `503` does not say which boundary failed. A client timeout does not say whether the origin committed.

Tracing makes causal structure visible, but it is an observation system with its own failures. Context can be malformed, spans can be dropped, clocks can skew, buffers can overflow, and sampling can omit the exact event being investigated. Reliable diagnosis combines traces with bounded metrics, structured logs, deployment/configuration evidence, and authoritative operation state.

RFC 9110 defines HTTP routing and intermediary semantics. W3C Trace Context Recommendation 1 defines interoperable `traceparent` and `tracestate` propagation. OpenTelemetry semantic conventions 1.44.0 provide current HTTP span naming and attribute guidance; because those conventions evolve, the chapter records the checked version and keeps its core reasoning vendor-neutral.

## Prerequisites and Retrieval

Retrieve HTTP requests and responses, proxy routing, retries, idempotency, monotonic versus wall clocks, queues, concurrency, structured logs, metrics, and graph paths. Recall that one logical operation may have several attempts and that response receipt is not the same as authoritative effect completion.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish logical operations, attempts, traces, spans, logs, and metrics;
2. propagate and validate standard trace context across HTTP boundaries;
3. design bounded-cardinality span names and safe attributes;
4. reconstruct queue, service, and dependency latency without double counting overlap;
5. trace proxy normalization, routing, retry, and protocol translation;
6. state sampling, clock, and missing-instrumentation limitations; and
7. combine telemetry with authoritative evidence for incident diagnosis.

## Core Exposition

### Start with identities and boundaries

Give the logical operation a durable operation or idempotency identity when the domain needs recovery. Give each network attempt its own attempt identity. Give the distributed trace a trace ID and each recorded operation a span ID. These identities can relate evidence but serve different contracts. A trace ID is neither a credential nor a proof that two payloads represent the same operation.

At an external edge, incoming trace fields are untrusted. Parse strictly, enforce size and count limits, and apply a policy for continuing or starting a trace. Attackers can choose trace IDs to force correlation, manipulate sampling hints, create high-cardinality state, or inject vendor data. Do not attach elevated trust to propagated context.

W3C `traceparent` carries version, trace ID, parent ID, and flags in a fixed interoperable format. `tracestate` carries bounded vendor-specific list members. A participating service normally creates a new span ID while retaining the trace ID. Context crosses process boundaries; span data is exported separately.

### Trace the client

Client-side evidence can distinguish name resolution, connection acquisition, connection establishment, TLS, request write, response headers, content read, and application parsing. Instrument only what the toolchain can observe honestly. A connection-pool wait is not network latency; a DNS cache hit is not a DNS exchange; a response-header timestamp is not business completion.

Record method, sanitized server address, protocol version, status, retry attempt, and route or operation name. Avoid raw query strings, credentials, bodies, high-cardinality IDs, and user data. If a client retries, create distinct attempt spans connected to the same logical operation; otherwise one long span hides amplification and ambiguous outcomes.

### Trace intermediaries

A proxy can terminate TLS, reconstruct the target URI, normalize fields, authenticate, authorize, rate-limit, select an upstream, translate protocol versions, queue, retry, and transform responses. Record these decisions as bounded attributes or child events where they materially explain behavior. Do not record secrets or a full policy dump.

Distinguish downstream response status from proxy-generated status. If connection acquisition to the origin fails and the proxy emits `503`, no origin server span may exist. If the origin returns `503`, the proxy should retain origin evidence. Retry spans need upstream attempt number, selected cluster, deadline remaining, and final choice without exposing raw instance identity unnecessarily.

Forwarding metadata such as client address and scheme has a trust policy separate from trace context. A trace can show which proxy asserted a value, but it does not validate that assertion. Record protocol translation at both sides so an HTTP/2 client exchange and HTTP/1.1 upstream exchange are not mistaken for one connection.

### Trace the service and dependencies

Server instrumentation begins after some work may already have occurred: kernel acceptance, server queueing, runtime scheduling, or middleware before hooks. If queue latency matters, record arrival and handler-start using a consistent clock at the same component. An absent queue span does not make queue time zero.

Name server spans by stable method and route template, not raw path. `/orders/{id}` bounds cardinality; `/orders/982734` creates one label per resource and can leak identifiers. Record response status and error classification, but interpret them by server/client span semantics. A `404` may be an expected application outcome rather than an instrumentation failure.

Dependency spans should identify the dependency system, bounded operation, outcome, and duration. Parallel calls overlap. Parent duration includes child work and local computation; adding children double-counts. To explain latency, reconstruct ordering and locate the critical path, queue gaps, uninstrumented intervals, and asynchronous edges.

### Asynchronous and detached work

Parent-child relationships imply a causal operation nested in another, but asynchronous workflows can outlive the initiating request. Use links or documented propagation across a message/operation resource rather than pretending a ten-minute job is nested inside a 100 ms request span. The HTTP request can end with `202`; the later operation has its own lifecycle and authoritative state.

Context propagation must not force tail sampling decisions prematurely or retain sensitive baggage indefinitely. Expire or transform context at domain boundaries, and distinguish trace correlation from business correlation. A payment reference may be searchable under tighter authorization even when trace data has expired.

### Timing and clocks

Use a monotonic clock for durations within one process. Wall-clock timestamps across hosts can be skewed. Distributed tracing backends may adjust visual timelines, but adjusted displays are evidence processing, not a proof of exact global ordering. Causality from parent/link relationships and message identities is often stronger than comparing timestamps separated by a few milliseconds.

For a sequential path, durations can approximate a sum when boundaries do not overlap and measurement points align. For parallel work, end-to-end duration follows the longest causal branch plus serial work. Let $L(v)$ be a span's exclusive contribution and predecessors define causality; critical-path length is the maximum path sum, not the sum over all vertices.

### Sampling and telemetry failure

Head sampling decides early and is cheap but can miss failures known only at the end. Tail sampling can retain slow/error traces after observing more data but costs buffering and can fail under overload. Either policy biases evidence. Record effective sampling configuration and supplement traces with aggregate metrics and controlled logs.

Instrumentation must be non-destructive and bounded. Exporters need queues, drop metrics, deadlines, redaction, and backpressure policy. Blocking a request indefinitely to export its trace defeats the service. A gap can mean no work, lost propagation, missing instrumentation, sampling, exporter failure, or storage/query omission; diagnosis must test alternatives.

<!-- bijux-verify: {"id":"critical-path-comparison","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"parallel-sum=190\nparallel-critical=110\nserial-overhead=70\nend-to-end=180\n","stderr":""}} -->
```python
dependencies = [80, 110]
end_to_end = 180
critical = max(dependencies)
print(f"parallel-sum={sum(dependencies)}")
print(f"parallel-critical={critical}")
print(f"serial-overhead={end_to_end - critical}")
print(f"end-to-end={end_to_end}")
```

This calculation verifies one stated latency decomposition. It does not prove span clocks aligned, dependencies fully overlapped, instrumentation complete, or the 70 ms remainder exclusively local work.

## Definitions and Notation

Let trace evidence be directed graph $G=(V,E)$. Vertex $v\in V$ is a recorded span with interval, attributes, and resource identity. Edge $(u,v)$ expresses recorded parentage or a causal link, not universal causal proof. A **critical path** is a longest causally ordered path under the selected duration model. **Exclusive time** approximates work not covered by child spans but can include gaps and instrumentation mismatch.

A **span name** is a bounded operation label. A **span attribute** is indexed contextual data subject to cardinality and privacy limits. An **event** is a timestamped occurrence within a span. A **resource attribute** describes the entity producing telemetry. **Baggage** is propagated application context and requires an explicit security/privacy contract; it is not a place for arbitrary user data.

## Mechanisms, Invariants, or Proof Structure

Trace an exchange in this order:

1. Identify logical operation, attempt, trace, and span identities separately.
2. Record client queue, connection, send, receive, and retry boundaries where observable.
3. At each proxy, record trust, normalization, routing, queue, translation, retry, and generated-response decisions.
4. At the service, use route templates and record handler queue, authorization outcome, status, and authoritative operation reference.
5. Instrument dependencies and asynchronous links with bounded semantic names.
6. Reconstruct causal order and critical path; do not sum overlapping spans.
7. Correlate with logs, metrics, deployment/configuration changes, and authoritative state.
8. State sampling, clocks, propagation, drops, redaction, and missing-span limitations.

The **identity invariant** prevents attempts, traces, and logical operations from being conflated. The **bounded-cardinality invariant** prohibits uncontrolled targets and identities in indexed labels. The **trust invariant** treats propagated context as untrusted metadata. The **evidence invariant** prevents telemetry success or absence from being promoted to business truth.

## Alternatives and Trade-Offs

**Full tracing versus sampling.** Full retention improves individual reconstruction but can be prohibitively expensive and privacy-sensitive. Sampling controls cost but biases visibility. Combine explicit sampling, aggregate metrics, targeted incident controls, and drop accounting.

**Automatic instrumentation versus manual spans.** Automatic instrumentation gives broad consistency and low effort. Manual spans capture domain boundaries and queue semantics but can duplicate library spans or encode volatile implementation details. Use automatic transport spans plus selective durable domain instrumentation.

**Raw target versus route template.** Raw targets help exact lookup but create cardinality and disclosure risk. Route templates support aggregation and stable operation ownership. Store carefully controlled occurrence identifiers in restricted logs when exact investigation is required.

## Failure Modes and Misconceptions

A trace is not a transaction log. Trace ID is not operation identity or authorization. Sampling flags are not a promise that data was stored. Span success is not domain success. Missing span is not proof of no call. Parent duration minus child durations is not always CPU time. Wall clocks do not establish precise cross-host order. Instrumentation can add latency, drop data, and leak secrets.

## Worked Examples

### Example 1

A gateway returns `503` before selecting an upstream. The trace contains client and gateway spans but no service span. Gateway connection metrics confirm acquisition failure. The conclusion is “no observed upstream attempt under available telemetry,” not absolute proof that no duplicate path existed.

### Example 2

A client retries a timed-out GET twice. Three attempt spans share one logical request correlation but have distinct span IDs and attempt numbers. This reveals amplification and different upstream selections; one merged span would hide both.

### Example 3

An attacker supplies a valid-looking `traceparent`. The edge parses it but applies its external-boundary sampling and `tracestate` policy, never treating the ID as identity. The trace remains correlation metadata rather than a security principal.

### Example 4

Span names use `/users/1287`, `/users/1288`, and so on. Cardinality and identifier leakage grow with traffic. Rename to `GET /users/{id}` and keep an authorized occurrence lookup elsewhere. Stable aggregation improves without losing the ability to investigate.

### Example 5

Two dependency spans last 80 ms and 110 ms in parallel inside a 180 ms request. Their sum is 190 ms, already longer than the parent. The critical branch is 110 ms; 70 ms remains serial/gap time under the simplified model. Summing spans is invalid.

### Example 6

The proxy receives HTTP/2 and calls the origin over HTTP/1.1. It records both protocol versions and its 12 ms upstream queue. The origin sees only HTTP/1.1. Without the proxy span, an operator could misattribute multiplexing behavior to the service.

### Example 7

A server span ends successfully after publishing work, but the later job fails. The initiating response was correctly `202`; the job trace is linked rather than nested and the operation resource records failure. HTTP transport success never implied job completion.

### Example 8

During overload, the trace exporter drops spans. A drop counter rises while request metrics continue. The team treats trace absence as telemetry degradation and uses sampled logs and operation IDs for recovery. Instrumentation failure becomes observable rather than silently falsifying conclusions.

### Example 9

Two hosts' wall clocks differ by 40 ms, making a child appear to start before its parent. Parent context and message identity establish causality; monotonic local durations remain usable. The display anomaly is not time travel or proof of malformed propagation.

### Example 10

A POST commits, the client times out, and the span is marked error because no response arrived. Operation lookup shows completion. The trace accurately records attempt failure while authoritative state records business success. Keeping both meanings prevents an unsafe retry.

## Cross-Program Connections

[HTTP Version Semantics](009-http-1-1-http-2-and-http-3-semantics.md) supplies stream and connection behavior, [Idempotency and Safety](008-idempotency-and-safety.md) separates attempts from operations, and [Headers and Metadata](004-headers-and-metadata.md) supplies propagation trust. Distributed systems owns partial evidence; reliability engineering owns telemetry pipelines; security engineering owns redaction and context abuse.

## References

- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Semantics*, RFC 9110, IETF Standards Track, June 2022, Section 7. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
- W3C Distributed Tracing Working Group. *Trace Context*, W3C Recommendation, 23 November 2021. Retrieved 2026-09-01. https://www.w3.org/TR/trace-context/
- OpenTelemetry Authors. *Semantic Conventions for HTTP Spans*, semantic conventions version 1.44.0. Retrieved 2026-09-01. https://opentelemetry.io/docs/specs/semconv/http/http-spans/

## Exercises

### Exercise 1

Distinguish a logical operation ID, request-attempt ID, trace ID, and span ID.

### Exercise 2

A 240 ms request contains sequential 30 ms proxy work and parallel 90 ms and 160 ms dependencies. Under the simplified full-overlap model, compute the critical dependency and unexplained/serial remainder.

### Exercise 3

Design tracing at an external gateway that terminates HTTP/3, retries HTTP/2 upstream, and emits a local `503` when no upstream is available.

### Exercise 4

Compare head sampling, tail sampling, and full retention for a low-rate payment API and a high-rate public catalog.

### Exercise 5

A trace shows a timed-out POST with a missing server span. Construct a diagnosis that avoids assuming either non-application or completion, and name the evidence needed for safe recovery.

## Answers to the Exercises

### Answer 1

The logical operation ID groups attempts intended to cause one domain effect. An attempt ID distinguishes each transmission/processing occurrence. A trace ID groups propagated telemetry across components for one causal observation graph. A span ID identifies one recorded operation in that trace. Systems may relate these identifiers, but none should silently substitute for another or serve as authorization.

### Answer 2

The critical dependency is 160 ms, not the 250 ms sum of both parallel calls. Under the stated full-overlap simplification, the remainder is $240-160=80$ ms, which can include the 30 ms proxy work plus client, queue, service, and instrumentation gaps. It cannot honestly be labeled CPU time without further evidence.

### Answer 3

Validate external trace context and apply edge sampling/privacy policy. Record the downstream HTTP/3 server span, bounded route, connection/queue timing, and attempt identity. Create a distinct HTTP/2 client span for each upstream attempt with remaining deadline and outcome. If selection fails, record a proxy-generated `503` and no fabricated origin span. Preserve operation identity separately, redact raw targets and credentials, and emit exporter-drop metrics.

### Answer 4

Full retention may be defensible for a low-rate, high-value payment flow if privacy, cost, and access controls are rigorous; it still cannot replace authoritative records. Tail sampling can retain errors and high latency but needs buffering and degrades under overload. Head sampling scales for a catalog but misses failures learned later. A sound design combines rate/error metrics, explicit sampling configuration, controlled logs, and temporary targeted sampling rather than claiming one policy is complete.

### Answer 5

The missing server span could mean the request never arrived, context was lost, instrumentation was absent, sampling/export failed, or query/storage omitted the span. The timeout says the client lacked a timely response, not whether the effect committed. Use operation/idempotency lookup, origin access evidence, gateway upstream-attempt records, authoritative database/workflow state, and telemetry-drop metrics. Retry only if the operation is idempotent/replayable within deadline or authoritative evidence proves non-application.
