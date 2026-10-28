# Module 85 — Runtime Efficiency: Contention, Queueing, Batching, and Async Load

**85/90** · Course 9 · Module 85 of 90

[Course 9 overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [MetricRail guide](../capstone.md)

## The question

> When work is correct and bounded, where do contention, waiting, scheduling, queueing, batching, and blocking determine throughput and tail latency?

## Why this comes now

After bytes and allocations are understood, the next production cost is waiting. A handler can remain fast in isolation while users experience long responses because work waits for admission, a queue, a lock, a runtime worker, a batch, or a downstream service. Module 85 makes that hidden residence time visible.

This module also separates concurrency from capacity. More tasks, threads, or connections can increase throughput only until a serialized resource or finite service rate becomes dominant. Beyond that point, extra concurrency stores waiting work and amplifies tail latency.

## What you will be able to do

After completing this module, you will be able to:

- separate service time, wait time, queue depth, concurrency, throughput, and utilization
- apply Little’s Law as a consistency check while stating its steady-state assumptions
- find lock contention, convoying, hot sharding, wake amplification, and blocking-runtime violations
- design queue, semaphore, and batch capacities from latency and memory budgets
- distinguish throughput batching from latency-sensitive coalescing
- measure saturation and knee points instead of reporting only unloaded latency
- preserve deterministic accounting when load shedding, cancellation, and retries interact

## Core model

### The governing model

A request’s latency is `queue wait + service + downstream wait + response`. Optimizing service code may not matter when queue wait dominates. Capacity creates a queueing system: arrival rate, service rate, concurrency, and queue policy determine delay and rejection. Every buffer is deferred work and memory. Every batch is a waiting policy. Every shared lock is a serialization point. Measure each phase separately.

### 1. Latency decomposition

End-to-end latency hides waiting. Instrument admission wait, queue residence, active service, lock acquisition, downstream I/O, and rendering separately. A lower service time with a deeper queue can worsen tail latency. Use an absolute monotonic clock for durations and retain request identity across spans.


### 2. Little’s Law as a check

Under stable long-run conditions, average items in a system are approximately arrival rate multiplied by average time in the system: `L = λW`. It is not a capacity formula for arbitrary bursts, unstable overload, or nonstationary traffic. It is useful for detecting inconsistent telemetry and estimating the implications of a latency objective.


### 3. Contention and convoying

A lock can have low average hold time yet severe tail effects when many tasks line up. Convoying occurs when delayed holders stall others. Sharding can reduce contention but introduces routing, skew, aggregation, and memory costs. Measure actual key distribution; a hot tenant can defeat uniform sharding.


### 4. Async scheduling cost

Async tasks are cheap relative to operating-system threads but not free. Polling, wakeups, channel operations, allocations, and executor scheduling consume work. A wake storm or busy loop can dominate. Blocking code on a runtime worker delays unrelated tasks; move it to an appropriate blocking boundary or redesign it.


### 5. Batching is a policy

Batching amortizes fixed cost such as syscalls, locks, or encoding. It also adds wait, memory, and failure scope. Define maximum items, maximum bytes, and maximum age. A batch flushes when any bound is reached. Unlimited “wait until full” behavior violates latency during low traffic.


### 6. Saturation and overload

Load tests should find the knee where throughput stops scaling and latency accelerates. Beyond capacity, accepting more work usually raises memory and tail latency without increasing useful throughput. Admission control and load shedding protect completed work. Report offered load, admitted load, completed throughput, rejection, and resource use separately.

Response time can be decomposed as admission wait + queue residence + active service + downstream wait + response write. The decomposition is a diagnostic model, not an assumption that every component is directly observable. Instrument enough boundaries to distinguish the dominant term, then use load sweeps to find where useful completions stop scaling.

### A module-specific decision table

| Accumulation point | Bound required | Signal required | Failure policy |
|---|---|---|---|
| accepted connections | concurrent connection limit | active and rejected connections | reject before per-connection state grows |
| broker mailbox | item and byte capacity | observed depth and residence | typed overload response |
| active ingest | execution permit count | active service and wait | reject or wait within one deadline |
| blocking work | submission and worker limits | pool wait and execution time | shed or defer, never unbounded enqueue |
| batch | items, bytes, and age | fill ratio and oldest age | flush on any bound |
| snapshot | output and memory limit | render time and bytes | explicit snapshot rejection |

### Working procedure

1. Enumerate every place work can wait or accumulate.
2. Give each place one owner, one capacity, one unit, and one terminal overload behavior.
3. Instrument offered, admitted, started, completed, rejected, failed, and cancelled work separately.
4. Sweep offered load below, near, and above expected capacity while varying concurrency and key skew.
5. Decompose response time into queue and service components wherever possible.
6. Locate the knee where added demand produces waiting or rejection rather than useful completion.
7. Set the initial envelope below the knee with failover and rollout headroom; do not use the largest observed completion number as capacity.

### Failure patterns and principled repairs

#### Reporting unloaded median latency as evidence of production capacity.

Unloaded median latency says little about queueing or saturation. Add an offered-load sweep and tail distributions.

#### Increasing queue capacity until rejections disappear while ignoring memory and queue residence time.

A larger queue hides rejection by storing more delay and memory. Bound it from the latency and memory budget instead.

#### Sharding a lock without measuring key skew or the cost of merged snapshots.

Sharding helps only if keys distribute and merge cost remains acceptable. Measure hot-key skew and snapshot reconstruction.

#### Adding a batch size but no age or byte limit.

Item count alone cannot bound batch memory or waiting time. Add byte and age limits and flush on the first bound reached.

#### Calling blocking filesystem or CPU-heavy work directly from async runtime workers.

Blocking work on async runtime workers delays unrelated I/O and timers. Move it behind a bounded blocking boundary with lifecycle ownership.

#### Using completed throughput alone and hiding offered load, rejected work, cancellations, and retries.

Completion throughput omits rejected, cancelled, and retried demand. Report the complete terminal accounting.

## Use the idea in a complete program

```rust
#[derive(Debug, Clone, Copy)]
struct BatchPolicy {
    max_items: usize,
    max_bytes: usize,
}

fn should_flush(policy: BatchPolicy, items: usize, bytes: usize) -> bool {
    items >= policy.max_items || bytes >= policy.max_bytes
}

fn main() {
    let policy = BatchPolicy { max_items: 64, max_bytes: 32 * 1024 };
    assert!(should_flush(policy, 64, 1));
    assert!(should_flush(policy, 2, 32 * 1024));
    assert!(!should_flush(policy, 2, 1024));
}
```

Use the example to separate active work from elapsed response. Add a queue before the worker and measure residence independently. Then increase offered load while holding service time constant. The sudden increase in tail response should be explained by waiting, not by claiming that the handler became slower.

Next, vary one concurrency control at a time. If throughput does not rise but queue depth and p99 do, the bottleneck is elsewhere. That observation is more useful than selecting a larger worker count by intuition.

### MetricRail consequence

MetricRail has three independent live capacities: accepted connections, broker mailbox entries, and active ingestion permits. The service rejects connection admission before allocating connection-task state, rejects broker submission before semantic commit, and reports store-capacity exhaustion separately from malformed records.

Run repeated `metricrail load` scenarios across declared concurrency values. The client reports offered, completed, protocol-rejected, and transport-failed operations. Response percentiles include only terminal protocol responses; timeouts remain failures rather than being silently mixed into latency. Server telemetry provides advisory active-connection and queue-depth observations, while the broker remains authoritative for committed series state.

The goal is to identify whether connection handling, mailbox residence, single-broker serialization, ordered-map updates, or response writes set the knee. The initial production envelope must preserve space for rollout overlap and failover, not merely avoid failure on a quiet benchmark host.

### Quantitative check: convert the latency objective into queue capacity

Assume one broker can sustain 2,500 record updates per second under the representative hot-key mix, and the admitted-ingestion p95 objective is 40 ms. If active service consumes 12 ms at p95, only 28 ms remains for admission, queue residence, and response writing. A mailbox of 10,000 records is therefore not justified merely because memory can hold it. At the measured service rate, draining 10,000 queued records would take about four seconds before accounting for new arrivals.

Use the latency budget to derive a much smaller operating region, then validate it experimentally because arrival bursts and service-time variance matter. Record queue depth together with oldest-item age; depth alone cannot tell whether a queue of 100 is harmless or already stale. If the service must absorb a short burst, state the burst size and duration explicitly and ensure the resulting residence remains within the objective.

This calculation is not a precise queueing model. It is a contradiction detector. When a proposed capacity implies waiting far beyond the product deadline, the configuration is wrong before a load test begins.

### Boundary case: higher throughput with worse useful capacity

A batching experiment raises completed throughput by 30% at heavy load. At low load, records wait for a full batch and p95 latency rises from 12 ms to 1.8 seconds. At overload, the batch queue holds maximum-size records, so memory grows beyond the service budget. The throughput gain is real, but the policy is incomplete.

Repair the design with three independent bounds: maximum items, maximum encoded bytes, and maximum age of the oldest item. Flush when any bound is reached. Then include shutdown behavior: a quiescing service must either process the partial batch within the grace period or return a terminal outcome for every admitted item. Cancellation cannot silently abandon committed work.

Rerun both sparse and saturated workloads. The batch may remain useful for a background reporting path while being unacceptable for interactive ingestion. This is a production-level conclusion: one mechanism can be correct for one operation class and wrong for another, even inside the same service. Capacity is attached to an operation and latency objective, not to the process as a whole.

## Practice sequence

1. Draw MetricRail’s accumulation map and assign a unit to every capacity.
2. Use the Bounded Throughput Tuner lab to preserve one terminal outcome per offered item.
3. Run a load sweep below and above saturation with several concurrency settings.
4. Separate offered, admitted, completed, rejected, and failed rates.
5. Add one confirming experiment for the suspected bottleneck rather than immediately increasing a queue.
6. Write the recommended envelope, headroom, and overload response as product policy.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- decompose response time into waiting and active components;
- name every place work can accumulate in a service;
- explain why larger queues can reduce apparent errors while worsening the product;
- find a saturation knee from offered, completed, queue, and tail data;
- design a batch policy with item, byte, and age limits;
- state MetricRail’s distinct connection, mailbox, execution, store, and snapshot capacities.

## Primary Rust references

- The Tokio documentation for runtime behavior, task spawning, synchronization, and blocking work
- The Rust standard library synchronization documentation
- Queueing-theory references for Little’s Law, with its steady-state assumptions stated explicitly

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

1. Complete the [Module 85 workbook](workbook.md).
2. Use the [reasoned solutions](solutions.md) only after writing your own answers.
3. Build the [Bounded Throughput Tuner laboratory](../../labs/module-05-bounded-throughput-tuner/README.md).
4. Apply the module to [MetricRail](../capstone.md).
