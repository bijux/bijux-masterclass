# Worked Answers — Module 05: Runtime Profiling and Allocation Control

Use these solutions to audit your reasoning for **Runtime Profiling and Allocation Control**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. A function has 100 ms wall time and 4 ms CPU time. What is the first hypothesis?

The function mostly waits: I/O, locks, scheduling, pool acquisition, or sleep. CPU optimization is unlikely to remove 96 ms. Instrument the waiting boundary before changing computation.

The chapter’s decisive distinction is this: Elapsed wall time answers how long the caller waited. Process CPU time answers how much processor time the process consumed. The difference includes waiting for I/O, scheduling, locks, other processes, and sleep.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 2. A function has 80 ms wall time and 78 ms CPU time. What does that suggest?

CPU work is a strong candidate, though multicore and measurement scope still matter. Use a CPU profiler and inspect self/cumulative time under representative input.

In the cumulative capstone, the rule becomes concrete: If wall time is high and CPU low, investigate waiting and queueing. If both rise together, CPU work is a plausible bottleneck. On multicore processes, aggregate CPU time can exceed wall time because multiple threads or workers consume CPU.

## 3. Explain `tottime` versus cumulative time in cProfile.

`tottime` is time spent in the function body excluding callees; cumulative time includes called functions. A coordinator can have low self time and high cumulative time. Use both to understand where work is owned and performed.

A useful way to reason about the boundary is: If wall time is high and CPU low, investigate waiting and queueing. If both rise together, CPU work is a plausible bottleneck. On multicore processes, aggregate CPU time can exceed wall time because multiple threads or workers consume CPU.

## 4. Why run an unprofiled baseline?

Profilers add instrumentation, sampling, file output, or scheduling overhead. Without an unprofiled baseline, you may attribute profiler cost to the application or compare differently perturbed candidates.

The implementation consequence is: Use performance.eventLoopUtilization() to compare active and idle time over an interval and monitorEventLoopDelay() to observe scheduling delay. A high utilization value is not automatically bad; a high delay under the critical workload indicates callbacks cannot run promptly.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 5. How would you detect event-loop blocking in Node?

Run a periodic lightweight timer or request alongside the suspected operation, collect event-loop delay and utilization over the interval, and inspect a CPU profile. A large delay while CPU work executes on the loop indicates blocking.

The important nuance is: Use performance.eventLoopUtilization() to compare active and idle time over an interval and monitorEventLoopDelay() to observe scheduling delay. A high utilization value is not automatically bad; a high delay under the critical workload indicates callbacks cannot run promptly.

## 6. What can tracemalloc prove and not prove?

It can attribute Python-managed allocations and compare snapshots by traceback. It cannot account completely for native extension allocations, kernel buffers, PostgreSQL memory, or all RSS behavior.

Under concurrency or failure, the distinction becomes: tracemalloc tracks Python memory allocations and compares snapshots by traceback. It does not measure every native allocation, kernel buffer, or database process. Use it to locate Python object growth and temporary peaks, not as a complete resident-memory profiler.

## 7. Why can offloading every CPU task to an unbounded thread pool fail?

The queue can grow without limit, threads consume memory and contend for CPU, cancellation may not stop work, and downstream effects continue. Bound workers and queue, apply admission, and measure total latency.

The design remains honest only if: Offloading is not free. A thread pool has bounded workers and a queue. Moving CPU work to a worker thread or process can preserve event-loop responsiveness but adds transfer and coordination cost. Use a concurrency limit and measure total journey latency.

## 8. A response mapping creates three copies of a 1 MB list. What should you measure?

Allocation count/bytes, peak memory, CPU, garbage-collection behavior, response correctness, and end-to-end latency under concurrency. A projection or streaming approach may reduce copies if the contract permits.

The consumer-facing consequence is: A change that reduces allocations but increases code complexity needs a practical benefit in the critical workload. Reusing mutable objects across requests can introduce data races or information leaks; do not trade safety for fewer allocations.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 9. When is custom JSON encoding unjustified?

When serialization is not a limiting resource, gain is below practical threshold, maintenance complexity rises, or output/validation semantics become harder to prove. Prefer the standard path.

The operational consequence is: Common improvements include selecting only required columns, avoiding repeated date formatting, reusing immutable metadata, streaming encoders for large lists where contract permits, and removing redundant encode/decode cycles. Each requires output-byte or semantic equivalence tests.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 10. Why can an API optimization overload PostgreSQL?

Reduced application CPU raises completed request rate and therefore database demand. The bottleneck moves; query latency, pool wait, and database utilization can worsen under the same offered load.

The strongest engineering interpretation is: Some boundaries are valuable; indiscriminate copying is not. Measure how many objects and bytes are created per page. Avoid replacing validated public models with raw dictionaries solely for speed unless equivalent conformance and security proof exists.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 11. Design a blocking experiment for artifact checksum.

Generate a large checksum operation while issuing a steady stream of lightweight metadata requests. Record checksum wall/CPU and lightweight p95/event-loop delay. Compare inline, stored-checksum, and bounded-offload variants with identical bytes.

The defect-oriented view is: Offloading is not free. A thread pool has bounded workers and a queue. Moving CPU work to a worker thread or process can preserve event-loop responsiveness but adds transfer and coordination cost. Use a concurrency limit and measure total journey latency.

## 12. A candidate lowers allocations 40% but p95 and CPU do not change. Accept?

Not solely for performance. It may improve headroom or GC risk if a capacity model shows value, but the report needs a practical benefit. Otherwise retain simpler code and record the finding.

Across the Python and TypeScript tracks, the invariant is: A change that reduces allocations but increases code complexity needs a practical benefit in the critical workload. Reusing mutable objects across requests can introduce data races or information leaks; do not trade safety for fewer allocations.
