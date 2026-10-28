# Workbook — Module 86: Observability: Structured Tracing, Metrics, and Diagnostic Context

[Chapter](index.md) · [Laboratory](../../labs/module-06-structured-observability-harness/README.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Observability: Structured Tracing, Metrics, and Diagnostic Context** has become a usable model rather than remembered vocabulary. Its governing question is: *What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?* Preserve your first prediction and record decisive facts in a **signal dictionary**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 85 — Runtime Efficiency: Contention, Queueing, Batching, and Async Load that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?**
3. Draw the smallest **signal dictionary** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### 1. Span, event, metric, or health state?

Select the best primary signal for each question:

- Which phase made request 42 slow?
- What fraction of ingestion attempts were rejected for overload in the last five minutes?
- Is this instance willing to receive new traffic?
- Which exact malformed field caused one import to fail?
- How many durable series does the broker currently own?

Explain why the other signal types are weaker for each question.

### 2. Cardinality

A metric is labeled with `tenant_id`, `request_id`, `file_path`, and full error message. Predict operational consequences. Redesign the metric while preserving diagnostic ability elsewhere.

### 3. Advisory versus authoritative counters

An atomic `active_requests` counter is incremented at start and decremented at normal return. A panic skips decrement. Can the value decide whether shutdown is complete? Design a safer authority and explain the role the atomic counter may still serve.

### 4. Secret-bearing `Debug`

A request struct derives `Debug` and contains an API token and raw telemetry line. Predict all paths by which those values can escape. Design redaction at the type boundary rather than relying on every call site.

### 5. Readiness

A readiness endpoint calls three dependencies with no timeout and returns healthy if the process is alive. Diagnose both false-positive and false-negative behavior. Define bounded liveness, readiness, and degraded health semantics.

### 6. Signal cost

A span is created for every parsed field. Predict CPU, allocation, storage, and noise effects. Choose a coarser span hierarchy and bounded event policy.

## Part 2 — Diagnose and repair

### Case A — High latency, low CPU

Metrics show high p99 response latency, low CPU, normal error rate, and rising queue depth. What additional spans or metrics distinguish downstream wait, lock wait, runtime starvation, and admission delay?

### Case B — Error-rate spike with no examples

A counter `errors_total` rises, but errors have no class or operation. Redesign the taxonomy with bounded labels and show where detailed context belongs.

### Case C — Logs expose payloads

A production incident reveals that `tracing::error!(?request)` stored customer data. Repair the code and the operating policy. Include tests.

### Case D — Metrics disagree with broker state

A live gauge says 900 series; a snapshot contains 947. Decide whether this is a bug, expected lag, or authority confusion. How should the two values be named and documented?

## Part 3 — Focused exercises

### Exercise 1 — Operator question matrix

For five operator questions, record signal type, stable fields, bounded labels, authority, retention, and expected response action.

### Exercise 2 — Span tree

Design a MetricRail span hierarchy for connection, command, broker request, and snapshot. Mark fields inherited from parents and fields forbidden by privacy policy.

### Exercise 3 — Metric schema

Define counters/gauges/histograms for offered, accepted, rejected, failed, queue depth, active work, series count, and phase latency. State label sets and why each is bounded.

### Exercise 4 — Health model

Define `live`, `ready`, `degraded`, and `unhealthy` from local state. Specify time bounds, dependency policy, and which states remove the instance from admission.

### Exercise 5 — Diagnostic reconstruction

Invent one incident timeline containing overload, a malformed request, and a broker failure. Using only your proposed spans, metrics, events, and health states, reconstruct what an operator would observe minute by minute. Identify one question the current schema cannot answer and either add a bounded signal or explicitly accept the blind spot. Estimate cardinality and volume for the new signal before keeping it.

### Exercise 6 — Signal budget

Assign a per-request telemetry budget for the normal path and a per-minute budget for exceptional events. Estimate spans, events, fields, bytes, and label series. Decide what is always emitted, sampled, aggregated, or dropped under telemetry backpressure. The application’s correctness path must not become unbounded merely because the diagnostic sink is slow.

### Interleaved reasoning pass

1. For **Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the signal dictionary.
2. For **Design stable event names and fields that preserve causal context across async and threaded work**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the signal dictionary.
3. For **Choose metric types and label sets without creating unbounded cardinality**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the signal dictionary.
4. For **Distinguish live advisory telemetry from authoritative product state**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the signal dictionary.

5. Identify one guarantee from an earlier course that a careless implementation of **Observability: Structured Tracing, Metrics, and Diagnostic Context** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build the [Structured Observability Harness](../../labs/module-06-structured-observability-harness/README.md). Use a typed `Outcome`, stable event fields, a secret wrapper with redacted `Debug`, and bounded outcome metrics. Tests must prove that secret content is absent from debug/event output and that every outcome maps to one stable label.

### Laboratory acceptance trace

Before opening the reference implementation for **Structured Observability Harness**, record:

- the public behavior that demonstrates **Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Introduce a stable tracing schema and metrics contract. The service must expose enough information to distinguish malformed input, overload, store-capacity exhaustion, broker closure, timeout, and internal failure. Payload, tenant, metric, request ID, and raw error text must not become metric labels. Health must report broker/store failure rather than silently defaulting to zero.

Write `OBSERVABILITY.md` as an operator guide: questions first, queries/signals second, expected actions third.

### Capstone invariant trace

For the Module 86 MetricRail increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. What question is each signal type best at answering?
2. Why are high-cardinality metric labels dangerous?
3. When is an atomic metric advisory rather than authoritative?
4. How does redaction belong in type design?
5. Distinguish liveness, readiness, degradation, and detailed diagnostics.
6. What makes a tracing schema stable?
7. How do you test observability without asserting every prose message?
8. Defend one signal you deliberately chose not to emit.

### Exercise 6 — Reconstruct an incident from emitted evidence

Assume operators report that one tenant’s snapshots became slow while aggregate throughput remained normal. Using only your proposed spans, fields, metrics, and error records, write the exact investigation path from symptom to a falsifiable hypothesis. Identify the correlation key, the service stage in which latency accumulated, the tenant or metric dimensions that are safe to retain, and the evidence that distinguishes queueing from store growth or response transmission. Then remove one field that would create excessive cardinality or expose sensitive input, and replace it with a safer diagnostic.

### Observability acceptance gate

Instrumentation is accepted only when it answers a named operational question and has bounded cost. Every metric needs a unit, event definition, aggregation rule, and cardinality policy. Every span must have a lifecycle that matches the work it describes. Logs are not a substitute for authoritative counters, and a dashboard is not proof that the underlying events are semantically correct.

### Closed-book defense

In five minutes, answer “What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?” using the **signal dictionary**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside MetricRail. A list of APIs without the deciding relationship is incomplete.
