# Reasoned Solutions — Module 87: Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-07-overload-control-simulator/README.md) · [MetricRail guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 87: Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation**. Compare the reasoning against this question: *How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Failure reasoning

### 1. Define the user-visible event

Process uptime measures only whether a process exists. A caller-visible availability SLI could be:

```text
valid ingestion requests completed successfully within deadline
---------------------------------------------------------------
valid ingestion requests offered to the service
```

Capacity rejection may be counted separately or included according to the public contract, but it cannot be silently excluded if users observe it. Invalid requests belong to a different class because the service correctly rejects them.

### 2. Retry multiplication

If “three retries” means one initial plus three additional attempts, and layers independently repeat their whole downstream operation, the maximum multiplies: `4 × 3 × 3 = 36` attempts. Even under alternative wording, the general danger is multiplicative. During overload, extra attempts consume the exact dependency capacity needed for recovery. One layer should own retry policy, with explicit budgets and signals preventing nested blind retries.

### 3. Per-attempt timeout

Fresh five-second timeouts across retries can exceed the eight-second caller budget by many multiples. Compute one absolute deadline at the outer boundary. Before each admission, attempt, and backoff, calculate remaining time; stop when insufficient. A timeout is a budget boundary, not an instruction to reset the clock.

### 4. Load shedding

Immediate bounded rejection preserves queue/memory capacity and lets callers choose retry/fallback before their deadline. Accepting doomed work consumes resources, delays useful requests, and often produces the same failure later. Shedding is protective when the rejection is explicit, fast, observable, and tied to a capacity policy.

### 5. Degraded success

Stale data can be successful only when the API declares freshness metadata or a degraded status, the age is bounded, callers can distinguish it from fresh authoritative data, and the fallback does not violate safety. Silent substitution is semantic drift.

### 6. Recovery oscillation

One-percent hysteresis invites rapid open/close oscillation. Enter recovery at a high threshold or sustained violation; leave only below a lower threshold for a minimum stable duration and after critical resources recover. Recovery should increase admission gradually when necessary.

## Part 2 — Repairs

### Case A

Timeouts trigger retries, retries add load, queues grow, latency rises, and more timeouts occur. Choose one retry authority—often the client or edge with full request context—and disable nested automatic retries. Retry only transient classes, cap attempts, share one deadline, honor server retry hints, and use idempotency for operations that may commit before response loss.

### Case B

Classifying overload as client error improves the displayed SLI by relabeling product failure. Keep invalid-input rate separate from capacity-rejection rate. The primary availability objective should state whether admitted-only or offered-valid requests are counted; both can be useful, but the denominator must be visible.

### Case C

Assign a stable idempotency key to the intended semantic operation. The server records in-progress and terminal outcomes for that key within a bounded retention policy. A retry attaches to the existing operation or receives the cached result. Request IDs can identify attempts; idempotency keys identify semantic intent.

### Case D

If enrichment is nonessential, accept the core record, mark enrichment unavailable, return explicit degraded metadata, bound how long deferred enrichment or stale data is allowed, emit bounded signals, and keep a recovery probe/state machine. If enrichment changes authorization or correctness, degradation is not safe and the request must fail.

## Part 3 — Model answers

### Exercise 1

A valid ingestion success SLI counts syntactically valid, authorized requests completed within deadline over all such offered requests. Latency uses the same successful population and reports percentiles. Snapshot freshness compares data age against a declared bound. Overload rejection is reported as its own rate over valid offered requests. Internal correctness failure counts invariant/protocol defects separately and should have a near-zero objective. Exclusions must be narrow, stable, and caller-justified.

### Exercise 2

The outer call computes `deadline = now + total_budget`. Each loop checks remaining time, attempts only retryable failures, caps attempts, and chooses `sleep = min(backoff+jitter, remaining_after_min_attempt_budget)`. The idempotency key remains constant across attempts; attempt/request IDs may change. Tests use deterministic jitter and a paused/fake clock.

### Exercise 3

Example:

- `Normal`: queue below 70%, latency within objective, full operations admitted.
- `Recovering`: entered after queue above 90% or sustained tail breach; expensive work rejected, retry hints emitted.
- `Degraded`: essential dependency unavailable; only safe subset permitted.
- Exit recovery only after queue below 50% and latency healthy for a fixed dwell period.

Exact thresholds require load evidence; the state machine prevents oscillation and hidden policy.

### Exercise 4

One source request terminates as success, domain failure, invalid, overloaded/rejected, deadline/cancelled, or internal failure. Attempts are subordinate records. Idempotency ensures at most one semantic commit; terminal accounting is keyed by source intent, not attempt count. At shutdown, every accepted source is terminal.

## Part 4 — Laboratory review

The simulator validates nonzero capacity, threshold ordering, retry limits, and unique source IDs. It reports source offered separately from attempts and admitted attempts. Rejected attempts may schedule bounded retries, but each source eventually has exactly one `Completed` or `Rejected` terminal outcome. Recovery ticks and maximum queue reveal policy behavior without wall-clock noise.

## Part 5 — MetricRail transfer

MetricRail should reject each exhausted capacity with a stable class and possibly bounded retry guidance. Retrying non-idempotent aggregation can double-count; either provide an idempotent operation key or document at-least-once semantics. A single deadline covers connection, queue, and broker. Degraded health may permit snapshots while ingestion is closed, but that state must be visible to clients and readiness.

## Part 6 — Defense

Uptime ignores request outcomes. Retry layers multiply. One deadline bounds total caller experience. Shedding protects finite resources and useful work. Degraded success requires explicit metadata and bounded semantics. Hysteresis prevents oscillation. Source intent, attempts, and executions are separate identities. MetricRail should expose capacity exhaustion rather than accept work it cannot complete within its contract.

## Deep reasoning and transfer

### Decisive model

> How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?

Build a **SLO and overload policy**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Derive admission and shedding policies from protected resources and customer-visible priorities.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Build retries around idempotency, one deadline budget, bounded attempts, and retryable classifications.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Distinguish overload, dependency failure, local defect, malformed input, cancellation, and deliberate rejection.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Design degraded modes that preserve explicit subsets of behavior rather than silently returning stale or partial results.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the SLO and overload policy.

### Reference implementation comparison

For [Overload Control Simulator](../../labs/module-07-overload-control-simulator/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In MetricRail, Module 87 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation**, which relationship decides this question: “How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to MetricRail?
