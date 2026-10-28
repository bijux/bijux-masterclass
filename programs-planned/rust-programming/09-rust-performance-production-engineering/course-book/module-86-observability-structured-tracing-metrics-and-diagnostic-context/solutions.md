# Reasoned Solutions — Module 86: Observability: Structured Tracing, Metrics, and Diagnostic Context

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-06-structured-observability-harness/README.md) · [MetricRail guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 86: Observability: Structured Tracing, Metrics, and Diagnostic Context**. Compare the reasoning against this question: *What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Signal reasoning

### 1. Span, event, metric, or health state?

Request-phase latency belongs in nested spans with request correlation. A five-minute overload fraction belongs in bounded counters/rates. Willingness to receive traffic belongs in readiness state. One malformed field belongs in a structured event/error tied to source context. Durable series count belongs in authoritative broker/store state and may be exported as a gauge with documented sampling. Metrics aggregate; traces correlate one operation; events record discrete facts; health summarizes admission-relevant state.

### 2. Cardinality

Those labels create near-unbounded time series, memory/storage growth, expensive queries, and accidental disclosure. Keep metric labels to bounded dimensions such as operation and outcome class. Put request/tenant/file context into redacted structured events or traces with controlled retention and sampling. Error messages become a bounded error code plus detailed event context.

### 3. Advisory versus authoritative counters

The atomic counter can drift after panic or cancellation, so it cannot prove shutdown completion. The task owner or `JoinSet` is authoritative because it owns every accepted task and can join them. The counter remains useful for live trend dashboards if documented as advisory and reconciled after join.

### 4. Secret-bearing `Debug`

Leak paths include tracing/logging, panic messages, assertion failures, error chains, crash reports, and ad hoc debug output. Wrap secrets in a type whose `Debug` and `Display` redact by default; expose the value only through an explicit method for domain use. Avoid storing raw payloads in broad structs and test formatted output for absence of known secret markers.

### 5. Readiness

Unbounded dependency checks can hang the endpoint and remove healthy instances during dependency trouble; process-alive success admits traffic to a broken broker. Liveness should answer whether the process/event loop is functioning with bounded local checks. Readiness should answer whether new work can be accepted under local capacity and required dependency state. Degraded health may serve limited operations while rejecting expensive ones. Detailed diagnostics can be separate and authenticated.

### 6. Signal cost

Per-field spans multiply subscriber work, allocations/formatting, storage, and analysis noise. Use a connection or request span, phase spans for parse/broker/store/render, and sampled events for exceptional field failures. Aggregate field counts and durations as bounded metrics.

## Part 2 — Incident repairs

### Case A

Add disjoint phase spans for admission, queue wait, lock acquisition, downstream I/O, and service; record queue and active-work gauges; inspect runtime task scheduling/blocked-thread signals. Rising queue with low CPU often points to downstream or lock wait, but the phase evidence must decide.

### Case B

Use bounded classes such as operation=`ingest|snapshot`, outcome=`invalid|overloaded|capacity|timeout|internal`, and perhaps protocol version. Detailed source line, field, causal chain, and request context belong in an event/trace. The metric answers “how much and which class”; the event answers “what happened here.”

### Case C

Remove broad `Debug` recording, introduce redacted wrappers and field allowlists, and scrub stored telemetry according to retention policy. Rotate exposed credentials if necessary. Add tests formatting request/error types and capturing representative events to assert secret and payload markers do not appear. Update code review guidance so `?value` on untrusted/secret types is prohibited unless the type itself is safe.

### Case D

If the gauge is asynchronously sampled, lag may be expected; name it `observed_series` and document sampling. If the broker publishes the value after every mutation, a mismatch is a bug. The snapshot’s broker-owned count is authoritative for the snapshot instant. Authority must be explicit instead of forcing operators to infer which number is “real.”

## Part 3 — Model answers

### Exercise 1

A matrix row might ask “Are clients being rejected because the queue is full?” The primary signal is `requests_total{operation="ingest", outcome="overloaded"}` plus queue-depth gauge; labels are bounded; counters are process-local and reset semantics are documented; retention supports SLO windows; action is reduce load/scale or investigate capacity. A related trace supplies individual context but is not the aggregate authority.

### Exercise 2

A suitable tree is:

```text
connection{connection_id, peer_class}
  command{operation, protocol_version}
    broker_request{outcome}
      store_apply{new_series}
    snapshot{series_count, output_bytes}
```

Request IDs may be trace fields if sampled and retention-controlled, not metric labels. Raw tenant, metric, payload, secret, and complete error text are forbidden. Parent fields should not be repeated on every event.

### Exercise 3

Counters: offered/accepted/rejected/failed by bounded operation/outcome. Gauges: queue depth, active work, authoritative series count. Histograms: queue wait, service, response, snapshot bytes using controlled buckets. Do not label by tenant/request/path. Cardinality is the product of label value sets; every set must be finite and reviewed.

### Exercise 4

- **Live:** runtime loop and essential internal task can answer within a short local deadline.
- **Ready:** broker is alive, configuration valid, and admission capacity exists; optional dependencies follow declared policy.
- **Degraded:** safe limited behavior remains, such as reads while writes are rejected.
- **Unhealthy:** essential authority is gone or invariants are compromised.

Dependency checks are bounded and cached where appropriate. Only ready instances receive normal new traffic.

## Part 4 — Laboratory review

The typed outcome prevents free-form label growth. `Secret` redacts in `Debug`; the event never stores secret content. Metrics count by a fixed outcome set. Tests should assert exact stable fields and absence of the raw secret, while avoiding brittle assertions on human-facing prose not declared stable.

## Part 5 — MetricRail transfer

MetricRail should distinguish protocol invalidity, store/series capacity, mailbox overload, connection admission, timeout, and internal failure with bounded codes. Health must propagate broker/store failure; replacing errors with zero creates false health. The operator document should map symptoms to signals and actions, not inventory every emitted field.

## Part 6 — Defense

Metrics answer aggregate rate/distribution, traces answer one operation’s path, events capture discrete context, and health answers admission/lifecycle state. High-cardinality labels create unbounded series. Advisory metrics can drift; owned state/task registries are authoritative. Redaction should be default behavior of sensitive types. Liveness is process function; readiness is admission; degradation is limited service; diagnostics explain. Stable schemas use named bounded fields and versioned semantics. Test fields, codes, redaction, and relationships rather than unstable prose. A deliberately omitted signal is correct when its cost, cardinality, or privacy risk exceeds its operational value.

## Deep reasoning and transfer

### Decisive model

> What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?

Build a **signal dictionary**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Design stable event names and fields that preserve causal context across async and threaded work.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Choose metric types and label sets without creating unbounded cardinality.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Distinguish live advisory telemetry from authoritative product state.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Propagate request, operation, tenant, and retry identities without recording secrets.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the signal dictionary.

### Reference implementation comparison

For [Structured Observability Harness](../../labs/module-06-structured-observability-harness/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In MetricRail, Module 86 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Observability: Structured Tracing, Metrics, and Diagnostic Context**, which relationship decides this question: “What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to MetricRail?
