# Module 87 — Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation

**Course 9 · Day 7 · Module 87 of 100**
`██████████████████████░░░` **87/100**

[Program](../../../README.md) · [Course 9](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-07-overload-control-simulator/README.md) · [MetricRail guide](../capstone.md)

[← Module 86: Observability: Structured Tracing, Metrics, and Diagnostic Context](../module-86-observability-structured-tracing-metrics-and-diagnostic-context/index.md) · [Module 88: Security and Supply-Chain Engineering →](../module-88-security-and-supply-chain-engineering/index.md)

## The question

> How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?

## Why this comes now

Signals reveal failure; Module 87 decides how the product behaves when failure or excess demand occurs. Reliability is not the absence of errors. It is the preservation of explicit outcomes, deadlines, capacity, and recovery behavior when the normal envelope is exceeded.

This module connects service-level objectives to concrete admission, retry, and degradation policies. Those policies must protect useful work without hiding incomplete results or amplifying load.

### Prerequisite bridge

Module 86 established **Observability: Structured Tracing, Metrics, and Diagnostic Context**. Before continuing, verify that you can test observability output for required fields, redaction, boundedness, and deterministic semantics. This module preserves that capability and adds the ability to write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous. Module 88, **Security and Supply-Chain Engineering**, will rely on both when it asks: *Which assets, trust boundaries, dependencies, build inputs, and operational capabilities could be abused, and which controls reduce that risk without relying on hidden assumptions?*

### Scope boundary

This module owns the reasoning for **reliability under load: slos, load shedding, retries, and degradation** inside Course 9. The course teaches measurement and operational reasoning, not folklore optimization. It does not promise universal performance rankings, complete security proof, or production readiness from one green pipeline. Every conclusion is scoped to a workload, artifact, environment, and time. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

After completing this module, you will be able to:

- write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous
- derive admission and shedding policies from protected resources and customer-visible priorities
- build retries around idempotency, one deadline budget, bounded attempts, and retryable classifications
- distinguish overload, dependency failure, local defect, malformed input, cancellation, and deliberate rejection
- design degraded modes that preserve explicit subsets of behavior rather than silently returning stale or partial results
- reason about error budgets as a decision aid rather than a promise that failures are acceptable anywhere
- test recovery, hysteresis, retry amplification, cold restart, and partial dependency loss

## Core model

### The governing model

Reliability is controlled behavior outside the happy path. Model it as `objective → indicator → resource envelope → failure taxonomy → response policy → recovery evidence`. An SLO without an indicator cannot be measured. A retry without idempotency and a deadline can amplify an outage. A degraded mode without a semantic contract is data corruption with a friendly name. Every resilience mechanism needs a trigger, bound, observable state, and exit condition.

### 1. SLIs and SLOs

An SLI defines the measured population and success criterion: for example, the fraction of admitted snapshot requests completed within 100 ms and with a semantically complete response. An SLO sets a target over a window. State exclusions narrowly; excluding every overload or dependency failure makes the objective meaningless.


### 2. Error budgets

The error budget is the allowed gap between perfect service and the objective over the window. It supports release and risk decisions; it does not excuse violating individual correctness or security contracts. Burn rate asks how quickly the budget is being consumed and can trigger alerts across short and long windows.


### 3. Admission and shedding

Rejecting work early can preserve accepted work. Choose the protected resource: queue slots, memory, workers, dependency concurrency, or per-tenant quota. Shedding should be cheap, typed, observable, and fair according to product policy. Do not accept and then time out work that could have been rejected before consuming scarce capacity.


### 4. Retry discipline

Retry only failures classified as transient and only when the operation is safe under duplicate execution or protected by idempotency. Use one overall deadline, cap attempts, back off, add bounded jitter, and honor server hints. Account for retries as offered load because they can amplify a struggling dependency.


### 5. Degraded modes

A degraded mode states exactly which semantics remain. Examples include serving a bounded cached snapshot with an age field, accepting ingestion while delaying expensive summaries, or disabling an optional export. Silent truncation, stale data without age, or weakened validation are not valid degradation.


### 6. Recovery and hysteresis

If overload mode activates and deactivates at one noisy threshold, the system can flap. Use sustained evidence, separate enter and exit thresholds, or minimum dwell times where justified. Recovery tests must prove queues drain, permits return, caches refresh, retries stop, and readiness changes back.

Reliability decisions are population decisions. An SLI must define which requests count, where success is observed, and how rejection, timeout, dependency failure, and client cancellation enter the denominator. A retry or degraded mode is valid only when it preserves that declared user-visible meaning.

### A module-specific decision table

| Failure situation | Safer default | Required explicit contract |
|---|---|---|
| capacity exhausted before commit | reject quickly | bounded code and retry guidance |
| ambiguous mutation commit | do not retry blindly | idempotency identity and retention |
| dependency timeout | consume one overall deadline | attempt cap, backoff, jitter, terminal error |
| expensive optional feature under pressure | explicit degraded rejection | freshness/completeness statement |
| transient recovery signal | require hysteresis | enter and exit thresholds |
| exhausted error budget | slow or stop risky rollout | ownership and escalation path |

### Working procedure

1. Define the user-visible population and success condition for each SLI.
2. Assign one deadline across queueing, attempts, backoff, and response.
3. Reject excess demand before semantic commit when possible.
4. Retry only classified transient failures and only when idempotency or read-only semantics make repetition safe.
5. Make degraded responses explicit about completeness, freshness, and unavailable features.
6. Use hysteresis and minimum dwell time so recovery does not oscillate.
7. Test overload, retry amplification, dependency slowness, and recovery with complete terminal accounting.

### Failure patterns and principled repairs

#### Defining availability as process uptime while requests fail or time out.

Process uptime ignores user-visible timeouts and failures. Measure success at the service boundary that callers experience.

#### Excluding overload and dependency failures from the SLI even though users observe them.

Overload and dependency failure cannot be erased from the population merely because they are inconvenient. State any exclusion and its user justification.

#### Retrying every error independently in several layers.

Layered retries multiply attempts. Assign one retry authority and expose downstream retry behavior.

#### Resetting the timeout on each retry instead of enforcing one end-to-end deadline.

Per-attempt timeout resets can exceed the caller deadline. Derive every attempt from one absolute deadline.

#### Calling partial or stale data a success without an explicit degraded response contract.

Partial or stale output must be labeled. If correctness cannot be preserved, reject explicitly instead of returning plausible success.

#### Opening admission immediately after one good sample and causing oscillation.

One good sample is not recovery. Use separate enter and exit thresholds with enough evidence to prevent flapping.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous, construct one positive and one causal negative example. Mark the first decisive fact in the **SLO and overload policy** and state which evidence could falsify the claim.

2. **Outcome 2.** For derive admission and shedding policies from protected resources and customer-visible priorities, construct one positive and one causal negative example. Mark the first decisive fact in the **SLO and overload policy** and state which evidence could falsify the claim.

3. **Outcome 3.** For build retries around idempotency, one deadline budget, bounded attempts, and retryable classifications, construct one positive and one causal negative example. Mark the first decisive fact in the **SLO and overload policy** and state which evidence could falsify the claim.

4. **Outcome 4.** For distinguish overload, dependency failure, local defect, malformed input, cancellation, and deliberate rejection, construct one positive and one causal negative example. Mark the first decisive fact in the **SLO and overload policy** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Admission {
    Accept,
    RejectOverloaded,
}

fn decide(queue_len: usize, capacity: usize, recovering: bool) -> Admission {
    let limit = if recovering { capacity / 2 } else { capacity };
    if queue_len >= limit {
        Admission::RejectOverloaded
    } else {
        Admission::Accept
    }
}

fn main() {
    assert_eq!(decide(10, 10, false), Admission::RejectOverloaded);
    assert_eq!(decide(4, 10, true), Admission::Accept);
}
```

Use the example to draw a deadline timeline. Include queue wait, first attempt, backoff, second attempt, and response. If the sum can exceed the caller’s deadline, the policy is invalid even when every individual timeout looks reasonable.

Then classify each error before choosing retry. Invalid input, authorization failure, and deterministic domain rejection are not transient. Capacity or dependency unavailability may be transient, but retry is still unsafe for a mutation without an idempotency contract.

### MetricRail consequence

MetricRail rejects connection, mailbox, active-ingest, series, and identifier-storage capacity with bounded public outcomes. Store capacity is reported as `CAPACITY`, not as malformed input. This distinction matters for both user behavior and overload metrics.

The supplied load client performs one attempt per record because the protocol has no durable idempotency key. The course guide states the conditions a future retrying client would require rather than demonstrating unsafe automatic mutation retries.

Snapshot pressure is a candidate degraded mode: ingestion may remain correct while expensive snapshots are rejected explicitly. The service must never silently omit rows or weaken record validation to preserve apparent availability. Recovery requires measured memory and queue headroom, not one successful request.

### Quantitative check: one deadline, not a stack of timeouts

A caller has 750 ms remaining. The first dependency attempt receives at most 250 ms. After it fails with a retryable capacity response, the client waits a jittered 80 ms. The second attempt may use at most 250 ms, leaving 170 ms for a final bounded backoff, one last attempt, and response construction. The policy must recompute remaining time before every action; it cannot blindly start a 250 ms third attempt when only 120 ms remains.

Write the timeline with absolute deadlines rather than summing optimistic durations after the fact. A server-provided retry hint is advisory: cap it by both the configured maximum and the remaining deadline. If the hint consumes the rest of the budget, return the terminal capacity outcome instead of sleeping until the caller times out.

Now add ambiguous commit. If the first mutation may have succeeded before the connection failed, the second attempt is safe only when the same idempotency identity causes the server to return the original terminal result. Without that contract, “retryable transport error” is not enough information to repeat the operation.

### Boundary case: retries turn overload into collapse

A dependency begins returning capacity errors. Three layers independently retry: the client library, the service handler, and a gateway. Each performs up to three attempts. One user operation can now create as many as twenty-seven downstream attempts, all while the dependency is least able to serve them. Apparent resilience becomes positive feedback.

Assign one retry authority. Classify the capacity response, respect a bounded server hint, and use one end-to-end deadline that includes queueing, attempts, and backoff. If the operation mutates state, require a durable idempotency identity or return the ambiguous outcome without automatic repetition. Record original operations and attempts separately so the retry multiplier remains visible.

Load shedding must occur before expensive work and before semantic commit whenever possible. Recovery also needs hysteresis: reopen admission only after capacity remains below the exit threshold for a declared interval. Otherwise a single successful probe releases a burst, the dependency overloads again, and the system oscillates. The repaired policy reduces both user delay and total work during failure.

## Practice sequence

1. Define ingestion success, latency, overload, and snapshot-freshness SLIs with exact populations.
2. Complete the Overload Control Simulator and verify terminal accounting under recovery.
3. Draw one 750 ms retry timeline and prove that all attempts and backoff fit inside it.
4. Identify MetricRail’s semantic commit point and explain why pre-commit rejection is safer.
5. Design an explicit snapshot-degraded response and its recovery thresholds.
6. Test that overload never becomes unbounded queueing and that invalid input never becomes retryable.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- define an SLI with numerator, denominator, observation point, and exclusions;
- distinguish rejection before commit from ambiguous failure after commit;
- construct a retry policy from one overall deadline and idempotency contract;
- explain retry amplification across layers;
- design a degraded mode that states completeness and freshness honestly;
- map every MetricRail capacity failure to a stable terminal outcome.

## Primary Rust references

- The Tokio and Hyper documentation for deadlines, cancellation, connection handling, and overload surfaces
- Site Reliability Engineering references for service-level indicators, objectives, error budgets, and burn rates
- Protocol documentation for retry and idempotency semantics used by dependencies

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

Continue to [Module 88 — Security and Supply-Chain Engineering](../module-88-security-and-supply-chain-engineering/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
