# Module 05 — Runtime Profiling and Allocation Control

> **Program stage:** Course 5 of 10 — Sustain the promise under pressure.

> **Central question:** Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort?

## Where this module fits

Module 04 produced **Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics**. This module extends that result by asking: **Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort?**

The new capstone increment is **Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements**. It becomes the prerequisite for **Queueing, Concurrency, and Backpressure**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Separate wall-clock, process CPU, and allocation measurements.
- Choose sampling, deterministic, or tracing profilers for the question.
- Read call counts, cumulative time, self time, and caller relationships.
- Use `tracemalloc` snapshots to locate Python allocation growth.
- Measure Node event-loop delay and utilization.
- Identify synchronous blocking inside asynchronous request paths.
- Measure serialization and validation cost without bypassing them.
- Avoid micro-optimizations that increase copying or memory.
- Compare runtime-specific improvements through the shared workload envelope.

## Capstone increment

Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements.

## Core performance model

### 1. Wall time, CPU time, and waiting


Elapsed wall time answers how long the caller waited. Process CPU time answers how much processor time the process consumed. The difference includes waiting for I/O, scheduling, locks, other processes, and sleep.

Measure both around a focused operation:

```text
wall_ns = monotonic_end - monotonic_start
cpu_ns  = process_cpu_end - process_cpu_start
```

If wall time is high and CPU low, investigate waiting and queueing. If both rise together, CPU work is a plausible bottleneck. On multicore processes, aggregate CPU time can exceed wall time because multiple threads or workers consume CPU.

Do not infer CPU bottleneck from high host CPU alone. Identify the process, code path, workload, and saturation relationship.


### 2. Profiler choice


A deterministic call profiler instruments function calls and reports call counts and time attribution. Python’s `cProfile` is suitable for CPU-bound call analysis with known overhead. A sampling profiler interrupts periodically and generally has lower overhead but statistical resolution. Tracing and span instrumentation explains stages, not line-level CPU.

Choose the least intrusive tool that answers the question. Profile a representative workload, not a contrived one-line function unless isolating a mechanism. Run an unprofiled baseline because profiler overhead can change scheduling and cache behavior.

The capstone dependency-light route uses `cProfile` and Node’s built-in inspector/CPU profile hooks where available, plus focused timers. Reports state profiler type and overhead boundary.


### 3. Python call and allocation analysis


`cProfile` reports primitive calls, total calls, self time (`tottime`), and cumulative time. A wrapper function with low self time can still dominate cumulative time because its callees are expensive. Sort by cumulative time to find expensive call trees, then by self time to locate work.

`tracemalloc` tracks Python memory allocations and compares snapshots by traceback. It does not measure every native allocation, kernel buffer, or database process. Use it to locate Python object growth and temporary peaks, not as a complete resident-memory profiler.

Warm imports and stable fixtures before recording. Keep profiling output outside the timed response path.


### 4. Node event-loop behavior


Node.js executes JavaScript callbacks on an event loop. Synchronous CPU work blocks the loop, delaying unrelated requests and timers. Asynchronous APIs do not make the JavaScript before and after an `await` free.

Use `performance.eventLoopUtilization()` to compare active and idle time over an interval and `monitorEventLoopDelay()` to observe scheduling delay. A high utilization value is not automatically bad; a high delay under the critical workload indicates callbacks cannot run promptly.

CPU profiles show JavaScript stack samples. Native work, garbage collection, and I/O need complementary evidence. Record runtime version and flags because JIT and garbage collector behavior can change.


### 5. Serialization, validation, and mapping


The Analysis Runs list path can allocate multiple representations:

```text
database row
→ persistence object
→ domain/application result
→ framework response model
→ JSON-compatible structure
→ encoded bytes
```

Some boundaries are valuable; indiscriminate copying is not. Measure how many objects and bytes are created per page. Avoid replacing validated public models with raw dictionaries solely for speed unless equivalent conformance and security proof exists.

Common improvements include selecting only required columns, avoiding repeated date formatting, reusing immutable metadata, streaming encoders for large lists where contract permits, and removing redundant encode/decode cycles. Each requires output-byte or semantic equivalence tests.


### 6. Blocking inside async code


In Python, synchronous file reads, compression, hashing, database drivers, or CPU loops inside an async request can block the event loop. In Node, synchronous filesystem, crypto, compression, or large JSON work does the same.

Offloading is not free. A thread pool has bounded workers and a queue. Moving CPU work to a worker thread or process can preserve event-loop responsiveness but adds transfer and coordination cost. Use a concurrency limit and measure total journey latency.

The capstone blocking experiment runs one expensive operation while lightweight health-like requests arrive. The decisive signal is not the expensive request’s own latency; it is delay imposed on unrelated work.


### 7. Allocation pressure and garbage collection


High allocation rate can increase allocator and garbage-collector work even when peak memory remains bounded. Large temporary lists, repeated string concatenation, and whole-body copies are typical sources.

Measure allocation rate or snapshot differences around a stable workload. Compare object counts and retained growth, not only process RSS. RSS may remain high because runtimes retain arenas for reuse.

A change that reduces allocations but increases code complexity needs a practical benefit in the critical workload. Reusing mutable objects across requests can introduce data races or information leaks; do not trade safety for fewer allocations.


### 8. The bottleneck can move


After reducing serialization CPU, database or network cost may dominate. This is expected. Performance work is iterative:

```text
measure → identify limiting resource → change → remeasure
```

Do not keep optimizing the old function after it falls below the decision threshold. The capacity model in Module 9 records bottleneck migration.

A local runtime improvement can also increase offered pressure on downstream dependencies. Higher API throughput may saturate the database sooner. Run the critical mixed workload after a micro-level fix.

## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Question-specific profiler | Profiler type and target correspond to CPU, allocation, or event-loop question. | A flame graph is collected without a decision question. | Experiment plan |
| Unprofiled baseline retained | Profiled and unprofiled runs are distinguished. | Profiler overhead is called application cost. | Paired envelopes |
| Wall/CPU separated | Elapsed and process CPU are reported with units. | Waiting is optimized as CPU or vice versa. | Runtime report |
| Output equivalence | Serialization/validation change preserves public response and policy. | Faster raw output bypasses guarantees. | Conformance and byte/semantic vectors |
| Async responsiveness measured | Unrelated lightweight work is measured during expensive operation. | Blocking hidden by measuring only slow request. | Blocking experiment |
| Allocation scope honest | Python/native/runtime/kernel memory boundaries are stated. | `tracemalloc` called total memory proof. | Evidence boundary |
| Offload bounded | Threads/workers and queues have explicit limits. | Offload moves unbounded queue elsewhere. | Concurrency configuration |
| Mixed workload rerun | Focused gain is validated in critical workload. | Bottleneck moves and system worsens. | Run series |

## Worked failures

### Case 1 — The async checksum loop

**Initial condition.** A Python async route computes a large SHA-256 and transforms metadata synchronously before yielding.

**Analysis.** The work is CPU-bound on the event-loop thread, delaying unrelated requests.

**Correct response.** Reuse stored checksums where integrity permits or offload bounded CPU work; measure lightweight request delay and total cost.

**Lesson.** `async def` does not make CPU work asynchronous.

### Case 2 — The faster raw dictionary

**Initial condition.** Replacing response models with raw database dictionaries cuts serialization time.

**Analysis.** Internal fields and type differences may escape; validation and read-only filtering are bypassed.

**Correct response.** Remove redundant conversions while preserving an explicit public projection and conformance tests.

**Lesson.** Serialization is also a security boundary.

### Case 3 — The memory leak diagnosis

**Initial condition.** RSS rises after a workload and does not fall, so a leak is declared.

**Analysis.** Runtime allocators may retain arenas; caches may retain bounded entries; native buffers may be involved.

**Correct response.** Compare allocation snapshots, object reachability, cache size, repeated steady-state cycles, and RSS trend.

**Lesson.** Retained RSS alone does not identify a leak.

### Case 4 — The microbenchmark victory

**Initial condition.** A custom JSON helper is 30% faster on a tiny object but list workload p95 is unchanged.

**Analysis.** Serialization was not the limiting resource or the object shape was unrepresentative.

**Correct response.** Keep the simpler implementation unless another objective justifies the helper.

**Lesson.** Mechanism benchmarks do not replace journey evidence.

## Python implementation

### Mechanism

The Python runtime module measures wall and process CPU, captures `tracemalloc` snapshots, produces stable cProfile summaries, and runs an event-loop blocking probe.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/runtime.py`
- `capstone/tracks/python-fastapi/src/api_performance/profiling.py`
- `capstone/tracks/python-fastapi/tests_performance/test_runtime_profiling.py`

### Focused example

```python
from api_performance.runtime import measure_callable

result, sample = measure_callable(lambda: encode_run_page(page))
assert sample.wall_ns > 0
assert sample.cpu_ns > 0
assert result.startswith(b"{")
```

The helper measures only the callable, returns the value, and records wall and CPU nanoseconds. Separate tooling profiles repeated representative calls and writes reports after timing.

### Python-specific failure to avoid

`cProfile` adds deterministic instrumentation overhead and `tracemalloc` observes Python allocations only. Name those limits. When offloading, bound the executor and propagate cancellation intentionally.

## TypeScript implementation

### Mechanism

The TypeScript runtime module records high-resolution wall time, event-loop utilization/delay snapshots, allocation proxies, and focused serialization timings.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/runtime.ts`
- `capstone/tracks/typescript-fastify/src/performance/profiling.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/runtime-profiling.test.mjs`

### Focused example

```typescript
const { value, sample } = measureCallable(() => encodeRunPage(page));
if (sample.wallNs <= 0n || sample.cpuUserMicros < 0) {
  throw new Error("invalid sample");
}
if (!value.startsWith("{")) throw new Error("invalid JSON");
```

Wall time remains bigint nanoseconds. CPU usage comes from the process delta and is reported in microseconds. Event-loop delay is collected over a workload interval, not around one synchronous call only.

### TypeScript-specific failure to avoid

A promise-returning function can still perform long synchronous work before its first `await` or after resolution. Measure loop delay and avoid synchronous filesystem/compression APIs in request paths.

## Cross-language invariant

Both tracks emit a common runtime sample with wall time, CPU time, operation count, bytes, and evidence notes. Exact nanosecond values need not match; units, scope, and correctness do.

## Failure patterns

- **Wall/CPU confusion.** I/O wait is optimized with CPU tricks. **Decisive check:** paired clocks.
- **Profiler-as-production.** Instrumented result is treated as normal latency. **Decisive check:** unprofiled baseline.
- **Async label fallacy.** Synchronous work blocks event loop inside async handler. **Decisive check:** lightweight probe delay.
- **Validation bypass.** Raw serialization leaks fields. **Decisive check:** conformance oracle.
- **RSS-only leak claim.** Allocator retention is misdiagnosed. **Decisive check:** snapshot and repeated-cycle evidence.
- **Old bottleneck fixation.** Function stays target after another resource dominates. **Decisive check:** mixed workload rerun.

## Evidence and design review

Before accepting the module increment, answer:

1. Is the observed time CPU, waiting, allocation, or event-loop queueing?
2. Which profiler can answer that question with acceptable overhead?
3. Does the optimized output preserve exact public semantics and field policy?
4. What unrelated work is delayed by the expensive path?
5. Did allocation reduction change retained memory or only temporary objects?
6. Which downstream resource becomes limiting after the change?

## Module synthesis

You are ready to leave this module when you can **separate wall-clock, process CPU, and allocation measurements, choose sampling, deterministic, or tracing profilers for the question, and read call counts, cumulative time, self time, and caller relationships** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Inject a synchronous blocking operation into the async request path** and requiring the following oracle: **profile points to the claimed code or wait boundary; unrelated request delay exposes event-loop blocking; public response semantics remain equivalent; allocation and CPU reports state their scope.**

The cumulative platform now includes **Profile named phases, detect blocking work, bound profiling overhead, and prove mechanism-level improvements**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Queueing, Concurrency, and Backpressure](../module-06-queueing-concurrency-and-backpressure/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
