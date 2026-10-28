# Module 86 — Observability: Structured Tracing, Metrics, and Diagnostic Context

**86/90** · Course 9 · Module 86 of 90

[Course 9 overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [MetricRail guide](../capstone.md)

## The question

> What must a running system reveal so that an operator can distinguish load, dependency delay, overload, malformed input, software defect, and expected rejection without reproducing the incident locally?

## Why this comes now

A measured service still cannot be operated when its internal states are invisible or its telemetry is ambiguous. Module 86 turns the causal boundaries from Modules 81–85 into signals. The objective is not to emit more logs. It is to answer specific operational questions with stable, bounded, privacy-safe evidence.

Observability is part of the product contract because signal schemas, label cardinality, redaction, and sampling determine what can be diagnosed during failure. A signal that lies, explodes in cardinality, or leaks input is worse than no signal.

## What you will be able to do

After completing this module, you will be able to:

- separate events, spans, metrics, profiles, and domain audit records by the questions they can answer
- design stable event names and fields that preserve causal context across async and threaded work
- choose metric types and label sets without creating unbounded cardinality
- distinguish live advisory telemetry from authoritative product state
- propagate request, operation, tenant, and retry identities without recording secrets
- define health, readiness, and dependency status as explicit product contracts
- test observability output for required fields, redaction, boundedness, and deterministic semantics

## Core model

### The governing model

Observability is an externalized model of the system. Events explain discrete occurrences. Spans explain causal work and duration. Metrics summarize repeated behavior. Profiles localize resource cost. Domain audit records preserve business-significant transitions. No one signal replaces the others. Design them from operational questions, then make field names, units, cardinality, redaction, and ownership stable.

### 1. Start with operator questions

“Add logs” is not a design. Ask what an operator must distinguish: Did admission reject the request? Was the line malformed? Which dependency consumed the deadline? Did a retry attach to committed work? Was memory pressure caused by queue growth or retained series? Each question determines a signal, fields, and retention need.


### 2. Events and spans

An event records something that happened. A span represents an operation with a beginning, context, descendants, and duration. In asynchronous code, lexical scope and execution scope may differ, so instrumentation must propagate the correct span across spawned work. Avoid one event per byte or per loop iteration; evidence has its own cost.


### 3. Metrics and cardinality

Counters represent monotonically accumulated events, gauges represent current values, and histograms represent distributions. Labels create dimensions, but values such as request IDs, user names, raw paths, or arbitrary error messages create unbounded cardinality. Keep high-cardinality identity in sampled traces or domain records, not metric labels.


### 4. Advisory versus authoritative

A live atomic gauge may lag or miss transitions during panic. A metrics exporter may drop data. Product state in the broker or durable store may be authoritative. Name telemetry honestly: `inflight_observed` rather than `jobs_exact` when it is advisory. Reconstruct authoritative summaries from owned state when correctness decisions depend on them.


### 5. Context and redaction

Correlation needs stable identifiers for request, operation, tenant class, retry attempt, and component. It does not require recording payloads, authorization headers, secrets, or raw personal data. Redaction is part of the event schema. Use safe newtypes or explicit field selection rather than relying on `Debug` for production records.


### 6. Health is not one Boolean

Liveness asks whether the process can respond. Readiness asks whether it should receive new work. Dependency health describes external conditions. Degraded mode may be ready for reads but not writes. Health endpoints must be cheap, bounded, and honest; they must not perform expensive checks on every scrape or claim that a dependency is healthy from stale cached success.

Choose signals by question. Events record discrete decisions, spans preserve causal duration and nesting, metrics summarize populations, and audit records preserve security- or policy-relevant actions. The same occurrence may need more than one signal, but each signal should have one declared purpose and bounded field set.

### A module-specific decision table

| Operator question | Best primary signal | Boundary to protect |
|---|---|---|
| Why was this request rejected? | structured event with bounded code | never echo untrusted payload |
| Where did response time go? | nested spans for queue, service, downstream, write | avoid per-byte or per-loop spans |
| Is overload increasing? | counter plus queue/active gauges | labels must be finite enums |
| Is state authoritative? | broker query or durable store inspection | advisory atomics are not truth |
| Can this instance receive traffic? | readiness decision with named reasons | liveness alone is insufficient |
| Did a sensitive action occur? | access-controlled audit record | separate from high-volume debug logs |

### Working procedure

1. Begin with an operator question and the decision its answer enables.
2. Identify the authoritative state and the boundary where the observation is captured.
3. Choose event, span, metric, or audit record based on cardinality and time semantics.
4. Define stable names, field types, units, labels, redaction, and retention before instrumenting code.
5. Bound telemetry cost and decide whether the signal is exact, sampled, approximate, or advisory.
6. Test malformed and high-cardinality inputs to ensure they cannot become labels or unbounded messages.
7. Rehearse one diagnosis using only the emitted signals; remove fields that do not help and add missing causal boundaries.

### Failure patterns and principled repairs

#### Using free-form messages as the only schema, forcing every operational query to parse prose.

Free-form prose has unstable schema and forces downstream parsing. Keep human messages, but add bounded event names and typed fields.

#### Putting request IDs, file paths, tenant IDs, or error strings into metric labels.

High-cardinality identifiers turn metrics into unbounded storage. Keep them in sampled traces or controlled logs, not labels.

#### Recording payloads and secrets because they are available through `Debug`.

Derived `Debug` can expose secrets and entire payloads. Implement redacted domain formatting and bounded public errors.

#### Calling an advisory counter authoritative even though panic or cancellation can skip updates.

Cancellation or panic can skip advisory counter updates. Reconcile with authoritative state before making a correctness decision.

#### Creating a span per low-level iteration and making telemetry cost dominate the operation.

Instrumentation inside tight loops can dominate the work. Place spans at product boundaries and measure telemetry overhead.

#### Making readiness perform unbounded network checks or return success solely because the process is alive.

Readiness must reflect whether essential work can be accepted and completed. A live process can still be unavailable.

## Use the idea in a complete program

```rust
use tracing::{info, info_span, Instrument};

async fn process(tenant: &str, request_id: u64) {
    let span = info_span!(
        "ingest_request",
        tenant = tenant,
        request_id,
        outcome = tracing::field::Empty
    );
    async move {
        info!(record_count = 1_u64, "validated telemetry batch");
        tracing::Span::current().record("outcome", "accepted");
    }
    .instrument(span)
    .await;
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt().with_target(false).init();
    process("tenant-class-a", 42).await;
}
```

Read the example by asking which question each field answers. If a field has no operational question, remove it. If a metric label can take a value from arbitrary input, replace it with a bounded classification. If an event contains the original malformed line, redesign it around an error code, byte count, and source position.

Then simulate an incident with high p99 and rising queue depth. Determine whether the current spans distinguish queue residence from active processing. Observability is complete only when the next action can be chosen without guessing.

### MetricRail consequence

MetricRail uses a `connection` span with an internal numeric connection identifier and structured lifecycle events. Tenant and metric names are redacted in `Debug` and are not emitted as metric labels. Protocol errors return stable bounded codes and never echo the input line.

Counters report accepted records, invalid rejection, overload rejection, and completed snapshots. Active connections and queue depth are explicitly observational: they help diagnose pressure but do not replace the broker’s authoritative series count. Snapshot completion is recorded only after the full response, including `SNAPSHOT-END`, is written.

The `HEALTH` command distinguishes healthy, degraded because the broker is saturated, and unhealthy because the broker is unavailable. The operations guide explains the limits of that signal: it proves neither downstream reachability nor historical correctness.

### Boundary case: telemetry that creates the incident

An engineer adds tenant identifiers and full error messages as metric labels to make filtering easier. During a malformed-input attack, every distinct payload creates a new time series. The metrics backend consumes memory and network bandwidth, exporter queues fill, and the service spends more CPU reporting the attack than rejecting it. The observability design has become an amplification path.

Repair the schema by using a finite error-code enum and a bounded tenant class if one is genuinely needed. Keep exact request or tenant identity in access-controlled sampled traces, subject to redaction and retention policy. Add a counter for dropped or sampled diagnostic records so absence of detail is itself visible without unbounded labels.

Now measure the enabled instrumentation path. Compare request latency and CPU with representative tracing levels and exporter failure. A production signal must retain bounded behavior when its destination is slow or unavailable. The service should not block semantic work indefinitely because a diagnostic sink cannot accept events. This boundary belongs in the observability contract, not as an afterthought in the logging library configuration.

## Practice sequence

1. Write six operator questions before adding any signal.
2. Build a schema table with event name, fields, units, labels, cardinality, redaction, and authority.
3. Complete the Structured Observability Harness and test its output against secrets and adversarial identifiers.
4. Instrument queue residence and active service separately in one controlled scenario.
5. Measure the cost of enabled instrumentation on a representative workload.
6. Perform a diagnosis using only MetricRail’s traces, metrics, health response, and authoritative snapshot.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- choose among events, spans, metrics, and audit records from an operator question;
- design bounded metric labels and explain why identifiers do not belong there;
- distinguish advisory telemetry from authoritative state;
- state the redaction policy for malformed and sensitive input;
- measure and limit observability overhead;
- use MetricRail signals to distinguish malformed input, overload, queueing, and broker failure.

## Primary Rust references

- The `tracing` crate documentation for spans, events, fields, and instrumentation
- The `tracing-subscriber` documentation for filtering, formatting, and layered subscribers
- OpenTelemetry semantic-convention documentation when interoperable field naming is required

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

1. Complete the [Module 86 workbook](workbook.md).
2. Use the [reasoned solutions](solutions.md) only after writing your own answers.
3. Build the [Structured Observability Harness laboratory](../../labs/module-06-structured-observability-harness/README.md).
4. Apply the module to [MetricRail](../capstone.md).
