# Module 85 Solutions — Runtime Efficiency: Contention, Queueing, Batching, and Async Load

[Workbook](workbook.md) · [Chapter](index.md) · [MetricRail guide](../capstone.md)

## Part 1 — Saturation reasoning

### 1. Unloaded versus loaded latency

Service time remains 2 ms, but work waits before service. Queue residence or scheduler delay explains the 80 ms tail. Measure admission timestamp, enqueue, dequeue/service start, service end, and response completion. Also record queue depth and active workers. Unloaded latency says little about waiting near capacity.

### 2. Queue enlargement

The larger queue stores more payload and metadata, increases residence time, permits work to become stale, lengthens drain/shutdown, and delays recovery after a burst. It may be correct when bursts are bounded, requests remain valuable, memory is budgeted, and deadlines exceed worst queue delay. Otherwise explicit rejection protects useful work better than hidden waiting.

### 3. Batch size without age limit

At high load the batch fills quickly and amortizes fixed work. At low load a record may wait indefinitely. Bound batches by maximum item count, maximum bytes, and maximum age. Flush when any limit is reached. This bounds memory, latency, and failure/retry scope.

### 4. Lock sharding

Uniform or multi-tenant keys can spread across shards. One hot key remains contended in one shard. Sharding adds hash/dispatch cost, multiple locks for cross-key operations, and snapshot merge/order work. Measure shard distribution and critical-section duration before choosing shard count.

### 5. Blocking inside Tokio

The CPU loop monopolizes a runtime worker, delaying unrelated futures, timers, and I/O. Move bounded CPU work to a dedicated worker pool or `spawn_blocking`, but guard submission and active count with limits. The boundary must include cancellation/deadline semantics and shutdown ownership.

### 6. Offered versus completed throughput

The system receives 80k attempts/s, completes 50k, and rejects 30k. Calling it “50k requests/s” without rejection hides overload. For a closed accounting interval:

```text
offered = completed + failed + rejected + cancelled + still_in_flight_delta
```

At terminal shutdown, the in-flight delta must be zero.

## Part 2 — Repairs

### Case A

Stable service time plus growing queue means offered load exceeds service capacity. A larger queue only delays rejection. First verify whether the workload is legitimate and whether workers are actually saturated. Faster/more workers help only if CPU/downstream capacity exists and the service scales. Admission control is required regardless to bound overload. Choose the first optimization from profiles and scaling tests, not queue depth alone.

### Case B

Instrument lock acquisition wait and hold duration, tag keys/shards, and record work performed while held. Move allocation, formatting, tracing, and I/O outside the critical section. Run hot-key and uniform-key workloads. Schedule snapshots separately to see whether global traversal blocks writes. Sharding helps only after the protected invariant and skew are understood.

### Case C

Add an age timer and byte limit, possibly with smaller batches during low traffic and larger batches under sustained load. Measure per-item latency and throughput across arrival rates. The goal is not one fixed optimal size but a bounded policy whose trade-off is explicit.

### Case D

Place compression behind a bounded blocking executor. Reject or defer work when submission capacity is exhausted; do not queue unbounded closures. Give each request one deadline that includes queueing and execution. Join/close the executor during shutdown. Measure both blocking-pool wait and work time.

## Part 3 — Model answers

### Exercise 1

Stamp phases at one monotonic clock source. Admission ends when the request is accepted or rejected. Queue wait spans enqueue to service start. Service spans domain work only. Downstream wait spans explicit dependency operations. Rendering spans result-to-response bytes. Nested spans should not be added twice; either report disjoint intervals or a tree with inclusive/exclusive semantics.

### Exercise 2

Sweep offered rate below and above expected capacity, with several connection/concurrency levels, queue sizes, worker counts, and hot-key percentages. Stop on resource budget, error-rate, or latency safety thresholds. Plot offered/admitted/completed rates, p50/p95/p99 response and queue wait, utilization, queue depth, rejection, and memory. The knee is where added offered load produces disproportionate waiting or errors rather than useful completions.

### Exercise 3

Assign each source item an index. Store outcomes in `Vec<Option<Outcome>>` or a checked map keyed by index, reject duplicates/out-of-range results, and fill rejection/cancellation explicitly. After all producers/workers join, verify every slot is terminal before rendering in index order. Missing outcomes are protocol defects, not defaults.

### Exercise 4

Use a bounded admission semaphore or channel before spawning blocking work and a separate active-work permit if queued capacity differs. The request deadline begins before admission. If capacity is unavailable, return overload; if deadline expires, cancel waiting or ignore a late result according to contract. The blocking pool size follows CPU/dependency capacity, not request concurrency.

## Part 4 — Laboratory review

The laboratory should return one terminal outcome per offered value. Accepted count plus rejected count equals offered count; completed plus failed equals accepted after all tasks finish. Samples exist only for admitted items and carry source index. Overflow becomes `Failed`, not a missing slot or panic. The tuning report should show that larger queues may reduce rejection while increasing queue wait.

## Part 5 — MetricRail transfer

Connection admission, mailbox capacity, and active ingestion are independent limits. A common-key workload tests fast lookup and hot-state contention; unique keys test allocation/cardinality growth. Choose limits below the point where queue wait and memory accelerate. Batch count, bytes, and age must all be bounded. Shutdown tests should prove that every accepted request is completed, failed, rejected, or cancelled.

## Part 6 — Defense

Service time is active work; response includes waiting. Queues store overload. The knee is the transition from useful scaling to rapidly increasing waiting/errors. Reporting only completion hides rejected demand. Hot keys defeat uniform sharding assumptions. Three batch bounds constrain memory, latency, and payload. Unbounded blocking submission merely relocates the unbounded queue. A defensible admission limit is tied to measured saturation, memory budget, and an explicit overload response.
