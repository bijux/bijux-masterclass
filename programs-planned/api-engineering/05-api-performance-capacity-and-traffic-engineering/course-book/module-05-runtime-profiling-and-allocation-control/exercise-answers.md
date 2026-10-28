# Reference Answers — Module 05: Module 05 exercise answers — Runtime Profiling and Allocation Control

Read after attempting all twelve Runtime Profiling and Allocation Control exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. A function has 100 ms wall time and 4 ms CPU time. What is the first hypothesis?

The function mostly waits: I/O, locks, scheduling, pool acquisition, or sleep. CPU optimization is unlikely to remove 96 ms. Instrument the waiting boundary before changing computation.

## 2. A function has 80 ms wall time and 78 ms CPU time. What does that suggest?

CPU work is a strong candidate, though multicore and measurement scope still matter. Use a CPU profiler and inspect self/cumulative time under representative input.

## 3. Explain `tottime` versus cumulative time in cProfile.

`tottime` is time spent in the function body excluding callees; cumulative time includes called functions. A coordinator can have low self time and high cumulative time. Use both to understand where work is owned and performed.

## 4. Why run an unprofiled baseline?

Profilers add instrumentation, sampling, file output, or scheduling overhead. Without an unprofiled baseline, you may attribute profiler cost to the application or compare differently perturbed candidates.

## 5. How would you detect event-loop blocking in Node?

Run a periodic lightweight timer or request alongside the suspected operation, collect event-loop delay and utilization over the interval, and inspect a CPU profile. A large delay while CPU work executes on the loop indicates blocking.

## 6. What can tracemalloc prove and not prove?

It can attribute Python-managed allocations and compare snapshots by traceback. It cannot account completely for native extension allocations, kernel buffers, PostgreSQL memory, or all RSS behavior.

## 7. Why can offloading every CPU task to an unbounded thread pool fail?

The queue can grow without limit, threads consume memory and contend for CPU, cancellation may not stop work, and downstream effects continue. Bound workers and queue, apply admission, and measure total latency.

## 8. A response mapping creates three copies of a 1 MB list. What should you measure?

Allocation count/bytes, peak memory, CPU, garbage-collection behavior, response correctness, and end-to-end latency under concurrency. A projection or streaming approach may reduce copies if the contract permits.

## 9. When is custom JSON encoding unjustified?

When serialization is not a limiting resource, gain is below practical threshold, maintenance complexity rises, or output/validation semantics become harder to prove. Prefer the standard path.

## 10. Why can an API optimization overload PostgreSQL?

Reduced application CPU raises completed request rate and therefore database demand. The bottleneck moves; query latency, pool wait, and database utilization can worsen under the same offered load.

## 11. Design a blocking experiment for artifact checksum.

Generate a large checksum operation while issuing a steady stream of lightweight metadata requests. Record checksum wall/CPU and lightweight p95/event-loop delay. Compare inline, stored-checksum, and bounded-offload variants with identical bytes.

## 12. A candidate lowers allocations 40% but p95 and CPU do not change. Accept?

Not solely for performance. It may improve headroom or GC risk if a capacity model shows value, but the report needs a practical benefit. Otherwise retain simpler code and record the finding.
