# Workbook — Module 87: Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation

[Chapter](index.md) · [Laboratory](../../labs/module-07-overload-control-simulator/README.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation** has become a usable model rather than remembered vocabulary. Its governing question is: *How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?* Preserve your first prediction and record decisive facts in a **SLO and overload policy**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 86 — Observability: Structured Tracing, Metrics, and Diagnostic Context that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?**
3. Draw the smallest **SLO and overload policy** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### 1. Define the user-visible event

A service reports 99.99% process uptime, but 4% of ingestion requests time out. Is availability 99.99%? Define an SLI whose denominator and successful event match what the caller observes.

### 2. Retry multiplication

A client retries three times, an edge proxy retries twice, and an internal worker retries twice. Calculate the maximum attempts triggered by one original request if policies compose naively. Predict what happens during dependency overload.

### 3. Per-attempt timeout

Each retry receives a fresh five-second timeout, while the caller’s intended deadline is eight seconds. Predict maximum elapsed time and write the correct deadline rule.

### 4. Load shedding

A queue is full. Compare immediate overload rejection with accepting the request and letting it wait past its deadline. Which preserves more useful work and why?

### 5. Degraded success

A snapshot endpoint returns stale cached data when the store is unavailable. Under what contract can this be a successful degraded response rather than a silent correctness failure?

### 6. Recovery oscillation

Admission closes when queue depth exceeds 90% and reopens as soon as it falls to 89%. Predict behavior under bursty load. Design hysteresis and a recovery criterion.

## Part 2 — Diagnose and repair

### Case A — Retry storm

Latency rises, clients time out, and total attempts triple while successful completions fall. Identify the feedback loop. Repair policy at one authoritative layer and state how idempotency affects the design.

### Case B — Hidden overload

The service counts rejected requests as “client errors” and excludes them from the SLI. Explain why the objective becomes self-serving. Define separate dimensions for invalid input and capacity rejection.

### Case C — Ambiguous commit

The client times out after sending an ingestion record. The server may have committed it. Design request identity and retry behavior that avoids duplicate semantic execution.

### Case D — Dependency degradation

A nonessential enrichment dependency fails. The current implementation fails all ingestion. Design a degraded mode with explicit response semantics, bounded duration, observability, and recovery.

## Part 3 — Focused exercises

### Exercise 1 — SLI/SLO table

Define SLIs for:

- valid ingestion success;
- ingestion latency;
- snapshot freshness;
- overload rejection;
- internal correctness failure.

For each, define numerator, denominator, exclusions, window, and objective. Do not hide product-visible failure through exclusions.

### Exercise 2 — One-deadline retry budget

Design a retry function using one absolute deadline, bounded attempts, exponential backoff, deterministic jitter for tests, retryable error classes, and an idempotency key. Show how remaining time constrains every attempt and sleep.

### Exercise 3 — Overload state machine

Design `Normal`, `Recovering`, and `Degraded` states using queue depth, latency, and resource pressure. Specify entry/exit thresholds, minimum dwell time, and allowed operations.

### Exercise 4 — Terminal accounting

For one source request, list all terminal states and prove that retry attempts do not inflate the count of semantic requests.

### Exercise 5 — Retry ownership record

For a three-layer client, proxy, and service path, write which layer owns retries, which errors are retryable, where the idempotency key is created, how retry hints are interpreted, and which deadline is authoritative. Describe the behavior when the response is lost after commit. Then state which lower layers are forbidden from retrying automatically and how that prohibition is verified in tests or configuration.

### Exercise 6 — Error-budget response

Assume the monthly objective has consumed 70% of its error budget in the first week. Define which releases, experiments, and capacity changes remain allowed. Tie the decision to measured causes rather than treating the error budget as a punishment counter. Include the evidence required to resume ordinary rollout speed.

### Interleaved reasoning pass

1. For **Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the SLO and overload policy.
2. For **Derive admission and shedding policies from protected resources and customer-visible priorities**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the SLO and overload policy.
3. For **Build retries around idempotency, one deadline budget, bounded attempts, and retryable classifications**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the SLO and overload policy.
4. For **Distinguish overload, dependency failure, local defect, malformed input, cancellation, and deliberate rejection**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the SLO and overload policy.

5. Identify one guarantee from an earlier course that a careless implementation of **Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build the [Overload Control Simulator](../../labs/module-07-overload-control-simulator/README.md). The simulation must distinguish source arrivals, attempts, admitted attempts, scheduled retries, completed requests, and terminal rejection. Recovery uses hysteresis. Every source ID receives exactly one terminal result, and invalid policies are rejected before simulation.

Run scenarios for steady load, short burst, sustained overload, recovery, and retry amplification. The simulator is deterministic so policy changes can be compared causally.

### Laboratory acceptance trace

Before opening the reference implementation for **Overload Control Simulator**, record:

- the public behavior that demonstrates **Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Define MetricRail’s service objectives and error taxonomy. Add explicit admission responses for full connection, mailbox, active-work, series, and output capacities. If clients may retry ingestion, define idempotency or clearly state that retries can duplicate aggregation. Use one request deadline across admission, queueing, and execution. Specify which operations remain available in degraded mode and how readiness changes.

### Capstone invariant trace

For the Module 87 MetricRail increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. Why is process uptime not request availability?
2. How do retry layers multiply load?
3. Why must retries share one overall deadline?
4. What makes load shedding protective rather than hostile?
5. When may stale or partial data be called success?
6. Why does recovery need hysteresis?
7. Distinguish source requests, attempts, and semantic executions.
8. Defend one failure that MetricRail should expose rather than mask.

### Exercise 6 — Allocate an error and retry budget

Given a monthly availability objective of 99.9%, calculate the total error budget for a thirty-day month. Divide it among invalid input, overload rejection, internal failure, timeout, and planned rollout risk without pretending all failures have equal meaning. Then model a client retry policy for one transient failure class. Bound attempts, total elapsed time, and additional offered load. Explain how retries consume both the caller’s deadline and the service’s capacity, and name the signal that disables retries when the service is already saturated.

### Reliability acceptance gate

A resilience mechanism is acceptable only when its failure domain and capacity cost are explicit. Load shedding must occur before an expensive or irreversible commitment; degradation must preserve the most important contract; retry must be safe for the operation and bounded by one deadline. “Eventually succeeds” is not a useful claim if duplicate effects, amplified load, or unbounded waiting remain possible.

### Closed-book defense

In five minutes, answer “How does the service preserve useful work and recover predictably when demand, dependency latency, error rate, or resource pressure exceeds the normal operating envelope?” using the **SLO and overload policy**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside MetricRail. A list of APIs without the deciding relationship is incomplete.
