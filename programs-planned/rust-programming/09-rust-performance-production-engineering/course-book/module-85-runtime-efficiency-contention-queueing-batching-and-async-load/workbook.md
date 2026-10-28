# Module 85 Workbook — Runtime Efficiency: Contention, Queueing, Batching, and Async Load

[Chapter](index.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

This workbook studies behavior near saturation. Record offered load, admitted load, completed load, queue residence, service time, rejection, cancellation, and resource use separately. Throughput without accounting is not a capacity result.

## Part 1 — Predict

### 1. Unloaded versus loaded latency

A handler takes 2 ms in isolation. At 400 requests/s with four workers it still has 2 ms service time, but p99 response latency reaches 80 ms. Predict the missing latency component and the measurements needed to confirm it.

### 2. Queue enlargement

A queue grows from 100 to 10,000 slots. Rejections disappear during a burst. Predict effects on memory, latency, stale work, shutdown, and recovery. When might the larger queue still be correct?

### 3. Batch size without age limit

A writer flushes only when 1,000 records accumulate. Predict behavior at high and low arrival rates. Design a three-dimensional batch policy.

### 4. Lock sharding

A map is split into 64 shards. Predict which key distributions benefit and which may not. Identify costs introduced into snapshots and multi-key operations.

### 5. Blocking inside Tokio

An async task performs a 200 ms CPU loop without yielding. Predict effects on unrelated timers and I/O on a small runtime. Choose an execution boundary and explain its capacity limit.

### 6. Offered versus completed throughput

A load report says “50k requests/s” but counts only successful completions and omits 30k rejected attempts/s. Explain why the result is misleading and construct the complete accounting identity.

## Part 2 — Diagnose and repair

### Case A — Queueing collapse

Throughput plateaus, queue depth rises continuously, and service time is stable. Diagnose the system. Should the first repair be faster workers, more workers, admission control, or a larger queue? State the evidence needed.

### Case B — Contended critical section

CPU utilization is low, lock wait is high, and one hot tenant dominates requests. Design a sequence that distinguishes long critical sections, key skew, allocator work under lock, and snapshot interference.

### Case C — Batching moves latency

Batching doubles throughput, but low-traffic p95 becomes seconds. Repair the batch policy while preserving most throughput gain.

### Case D — Hidden blocking

Async traces show long gaps with no poll activity. A dependency performs synchronous compression. Explain how to isolate it without creating an unbounded `spawn_blocking` flood.

## Part 3 — Focused exercises

### Exercise 1 — Latency decomposition

Define:

```text
response = admission + queue_wait + service + downstream_wait + rendering
```

Specify how each phase is observed and which clock boundaries avoid double counting.

### Exercise 2 — Saturation curve

Design a load matrix varying offered rate, concurrency, queue capacity, worker count, and key skew. State the stop conditions and the plots needed to identify the knee.

### Exercise 3 — Capacity identity

For every offered item, require exactly one terminal outcome: completed, failed, rejected, or cancelled. Design data structures that preserve source order despite out-of-order completion.

### Exercise 4 — Bounded blocking pool

Design a wrapper around blocking work with separate admission and active-work limits, one overall deadline, and explicit overload behavior.

### Exercise 5 — Interpret one saturation table

Create a table for offered rates below, near, and above capacity. Include admitted, completed, failed, rejected, queue depth, queue wait p95, service p95, response p95, CPU, and memory. Mark the first point where useful completions stop scaling proportionally and explain whether the limiting mechanism is CPU, serialized state, downstream wait, or admission. Propose one confirming experiment. A larger queue is not a confirming experiment unless queue storage itself is the hypothesis.

### Exercise 6 — Queue-age policy

Design a queue item that carries admission time, source identity, and deadline without exposing mutable timing state to every worker. Specify whether expired work is rejected before enqueue, while waiting, or immediately before service, and how each terminal outcome is recorded. Explain why processing expired work can reduce useful throughput even when workers are otherwise idle later.

## Part 4 — Independent laboratory

Build the [Bounded Throughput Tuner](../../labs/module-05-bounded-throughput-tuner/README.md). The product must return exactly one terminal `Outcome` for every offered input, keep results in source order, expose queue-wait and service samples for admitted work, and treat arithmetic overflow as a terminal failure rather than a missing result. Explore at least six `(queue_capacity, max_active)` settings.

## Part 5 — Capstone transfer

Instrument MetricRail from socket admission through broker queueing and store mutation. Run controlled loads with common keys, hot-key skew, and unique-series growth. Choose connection, mailbox, and active-ingest limits from the saturation curve and memory budget. If batching is introduced, bound it by item count, bytes, and age. No configuration change is accepted without terminal accounting and shutdown tests.

## Part 6 — Reconstruct and defend

1. Distinguish service time from response time.
2. Why does a queue hide overload rather than remove it?
3. What is the knee of a saturation curve?
4. Why must offered load and rejection be reported?
5. What does key skew do to lock sharding?
6. How do count, bytes, and age jointly bound a batch?
7. Why is unbounded `spawn_blocking` not an isolation strategy?
8. Defend one admission limit with evidence.

### Exercise 6 — Construct a saturation experiment

Choose a fixed request mix and sweep offered concurrency across at least six points from comfortably below capacity to sustained overload. For every point record offered rate, accepted rate, completed rate, p50 and p99 latency, queue occupancy, active work, overload rejections, timeouts, and CPU. Identify the knee where additional offered work stops increasing useful throughput. Then repeat with one changed capacity parameter. Explain whether the change increased service capacity, merely moved waiting into another queue, or increased tail latency to preserve acceptance.

### Runtime-efficiency acceptance gate

A tuning change must be evaluated on both sides of saturation. Below the knee it should not add needless coordination; above the knee it must not hide overload by allowing unbounded waiting. State which component owns admission and why every accepted unit still has a bounded path to a terminal outcome. Thread count, queue length, and batch size are policy variables, not independent speed controls.

