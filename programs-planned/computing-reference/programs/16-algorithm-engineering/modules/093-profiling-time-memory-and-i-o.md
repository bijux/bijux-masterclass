---
module_id: ALGE-093
program: Algorithm Engineering
level: 2
module_number: 93
title: Profiling Time, Memory, and I/O
status: complete
last_verified: 2026-09-05
---

# Profiling Time, Memory, and I/O

## One-Page Review

### Governing question

How do we attribute an algorithm’s elapsed time, processor work, live and peak memory, and logical and physical I/O to mechanisms without mistaking a profiler’s partial observations for causation?

### Essential definitions

- A **profile** estimates where a measured resource is consumed across code, phases, stacks, objects, or events.
- **Instrumentation** records selected events at explicit points; **sampling** observes execution periodically or on counter overflow.
- **wall time** is elapsed duration across a boundary; **CPU time** accumulates scheduled processor execution in a declared scope.
- **live bytes** remain allocated at an instant; **allocated bytes** are cumulative allocation traffic; **resident set size (RSS)** is resident mapped memory attributed by an operating-system interface.
- **logical I/O** is requested by the application or runtime; **physical I/O** reaches a storage device or lower measured boundary.
- An **inclusive** cost includes descendants; an **exclusive** cost is attributed to the frame or phase itself.
- **observer effect** is behavior changed by measurement overhead, buffering, layout, scheduling, or lost events.

### Central model, mechanism, or theorem

For a single-threaded process without child work over interval $[s,e]$, a useful accounting check is

$$
0 \le T_{\mathrm{cpu}} \le T_{\mathrm{wall}},
\qquad
T_{\mathrm{residual}}=T_{\mathrm{wall}}-T_{\mathrm{cpu}}.
$$

The residual includes sleep, blocking, preemption, and measurement mismatch; it is not automatically “I/O time.” With parallel threads, aggregate CPU time can exceed wall time. Similar boundary discipline applies to bytes: logical bytes, filesystem traffic, block traffic, device traffic, and media traffic need not be equal because caching, read-ahead, buffering, compression, retries, and amplification intervene.

### Critical invariants

- Every metric names its unit, scope, boundary, clock or counter, aggregation, and collection mode.
- Correctness and the benchmark protocol remain unchanged between unprofiled and profiled runs.
- Inclusive and exclusive costs are never added as though disjoint.
- Allocation traffic, live heap, retained heap, RSS, virtual size, and peak values remain distinct.
- Requested, transferred, cached, block, device, and media I/O remain distinct.
- Counter support, privilege, multiplexing, scaling, sampling period, lost events, and symbol quality are recorded.
- Profiles are compared only across compatible workload and environment identities.
- A hot location is treated as an attribution lead, not proof that editing it improves the end-to-end metric.

### Common failures

Profiling an unrepresentative input; sorting by percentage while ignoring total duration; adding inclusive stack percentages; equating aggregate CPU with wall time; calling wall-minus-CPU I/O; reading RSS as heap; reading cumulative allocation as peak live memory; treating page-cache hits as zero I/O work; equating application bytes with device bytes; trusting unsupported or multiplexed hardware events without metadata; losing stacks through missing symbols or unwinding; attributing asynchronous work to the submitting thread; using one sample as a stable ranking; ignoring profiler overhead; and optimizing a hot function whose cost is forced by a higher-level algorithmic choice.

### Compact example

A run takes 100 ms wall and 80 ms process CPU. In a single-threaded, no-child scope, 20 ms is unaccounted scheduled time, but the profile cannot label it as disk wait without scheduler and I/O evidence. If two worker threads each use 80 ms during 100 ms wall, aggregate CPU is 160 ms and no contradiction exists. Scope changes the interpretation.

### Connections

[ALGE-090](./090-mapping-an-algorithm-across-memory-threads-and-storage.md) predicts resource pressures, [ALGE-091](./091-representative-workload-construction.md) selects inputs, and [ALGE-092](./092-benchmark-design-and-reproducibility.md) fixes the experiment. ALGE-094 next constructs pathological cases that can falsify a benign profile.

## Governing Question

Given a reproducible benchmark and a performance symptom, which time, allocation, residency, and I/O measurements at which boundaries can distinguish competing explanations, and what evidence would falsify each explanation?

## Why This Matters

Benchmarking establishes that behavior differs; profiling helps explain where and why. The distinction matters. A sampling profile can show most observed on-CPU samples in comparison code, yet the root cause may be a data representation that forces costly comparisons. A memory profile can identify a large cache, while RSS growth actually comes from mapped files or allocator fragmentation. An I/O counter can rise because read-ahead fetches unused blocks.

Profilers expose models implemented by tools and operating systems. They do not observe an abstract algorithm directly. Event availability varies by processor and kernel; permissions may restrict monitoring; unwinding can fail; counters can be multiplexed; sampling misses short phases; instrumentation perturbs them. Rigorous diagnosis triangulates compatible evidence and validates proposed causes by controlled change.

## Prerequisites and Retrieval

Retrieve machine-model boundaries from [ALGE-009](./009-machine-models-and-hidden-constants.md), empirical claims from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), cache behavior from [ALGE-072](./072-caching-and-paging-algorithms.md), external-memory accounting from [ALGE-085](./085-external-memory-cost-models.md), integrated resource reasoning from [ALGE-090](./090-mapping-an-algorithm-across-memory-threads-and-storage.md), and experiment controls from [ALGE-092](./092-benchmark-design-and-reproducibility.md).

## Learning Objectives

After this module, you should be able to:

1. distinguish benchmarking, tracing, instrumentation, sampling, counting, and causal validation;
2. interpret wall, process CPU, thread CPU, on-CPU, off-CPU, and parallel aggregate time by scope;
3. construct and read inclusive, exclusive, phase, call-path, and differential profiles;
4. distinguish allocation traffic, live/retained/peak heap, RSS, virtual memory, mapped pages, and fragmentation;
5. trace I/O across application, runtime, system-call, page-cache, filesystem, block, device, and media boundaries;
6. qualify hardware and software counters by support, multiplexing, scaling, loss, skid, and permissions;
7. estimate and test profiler overhead and missing-event bias; and
8. turn a hotspot into competing hypotheses and controlled end-to-end validation.

## Core Exposition

### Begin with a symptom and hypotheses

State the symptom in the benchmark’s primary units: latency rose 30%, peak RSS exceeds a limit, or physical writes doubled. Preserve workload, implementation, build, and environment identity. Then list mechanisms that could produce it. A latency increase might reflect more instructions, cache misses, blocking, contention, frequency reduction, faults, or downstream I/O.

Choose evidence that discriminates among hypotheses. On-CPU samples distinguish code paths while executing; scheduler events help identify runnable versus blocked time; allocation traces locate creation; heap snapshots locate retention; page-fault and block events connect memory demand to storage. Collecting every event at once can increase overhead and blur causality, so proceed from broad to focused.

### Separate benchmarking, profiles, and traces

A benchmark measures an outcome over a defined protocol. A counting profile aggregates events by location or phase. A sampling profile estimates a distribution from observations. A trace preserves ordered events and timestamps, often enabling latency and causality reconstruction. Instrumentation inserts explicit records or timers.

These products answer different questions. Counts lose order; traces can be enormous; samples have uncertainty; instrumentation observes only declared points. Use the least intrusive evidence that distinguishes the hypothesis, then validate under the unprofiled benchmark.

### Account for time by boundary

Use a monotonic elapsed clock for wall duration. Process CPU accumulates user and system CPU in the process scope; thread CPU narrows the scope. Neither includes time when that scope is not scheduled. Aggregate CPU across parallel workers may exceed wall time; utilization can be summarized as $T_{\mathrm{cpu}}/T_{\mathrm{wall}}$, with the processor capacity denominator stated.

Do not label wall-minus-CPU without evidence. It includes sleeping, locks, descheduling, I/O waits, page faults handled off CPU, child processes omitted from scope, accelerators, and collection mismatch. Off-CPU profiling uses scheduler or blocking events to attribute waiting, but asynchronous operations may complete in other contexts.

### Attribute phases before functions

Mark semantic phases—parse, build, compute, spill, merge, publish—using stable identities. Phase measurement connects costs to the algorithm. Function hotspots alone often mix setup and steady work or separate functions implementing one phase. Nested phase timers require a defined stack discipline and inclusive/exclusive treatment.

For interval trees, exclusive time equals a parent’s inclusive time minus the union of direct child intervals, not minus arbitrary overlapping asynchronous work. Concurrent intervals cannot be added to reconstruct wall time. Preserve timeline and execution context.

### Use sampling profiles carefully

Time-based sampling interrupts or observes at a configured frequency; event-based sampling triggers after event counts. A sample share estimates time or events under the sampling design. Short phases may receive zero samples. Correlated sampling periods can alias periodic workloads; jitter or alternative periods help diagnose this.

Resolve stacks with symbols, build IDs, mappings, and an unwinding method. Inlining, tail calls, generated code, stripped symbols, frame-pointer omission, and runtime stacks affect attribution. Record unresolved and truncated samples rather than redistributing them invisibly. Inclusive cost answers “which call paths contain work?”; exclusive cost answers “where was the sampled instruction?”

### Interpret counters as a measured model

Hardware performance events count architecture-specific or model-specific events such as cycles, instructions, cache-related events, and branch events. Event names can hide differing definitions. Some events are unsupported, constrained to certain counters, affected by speculative execution, or measured at a different cache or uncore scope.

When requested events exceed physical counters, the kernel/tool may multiplex them and scale counts by enabled/running time. Low running fractions increase uncertainty. Event groups can enforce simultaneous scheduling but may fail to schedule. Sampling has skid: the recorded instruction can follow the event. Record tool, kernel, processor, raw encoding where necessary, event scope, exclusion flags, group, enabled/running time, scaling, and loss.

### Profile allocation, liveness, and residency separately

Allocation traffic is the sum of bytes or objects allocated over time. A loop can allocate 10 GiB cumulatively while keeping only 10 MiB live. Live heap is reachable or allocator-live memory at a snapshot. Retained size attributes objects kept alive through a root. Peak live heap is a high-water mark, which may be missed by sparse sampling.

RSS is resident mapped pages attributed by the operating system and can include heap, stacks, code, shared libraries, mapped files, and shared pages under tool-specific accounting. Virtual size includes mappings not resident. Allocator arenas, fragmentation, caches, delayed release, copy-on-write, huge pages, and garbage collection separate object liveness from RSS. Always state platform semantics; even a field with the same name can differ across systems.

### Profile I/O across layers

At the application boundary, record operations, requested bytes, offsets, queueing, and semantic purpose. At the system-call boundary, calls and returned bytes reveal short reads/writes and errors. Page-cache counters expose hits, misses, dirtying, and faults only under their specific definitions. Filesystem and block traces show submitted, merged, completed, or retried requests. Device statistics aggregate lower-layer work.

Logical bytes can exceed physical reads when cache serves data. Physical bytes can exceed useful logical bytes through read-ahead, block granularity, metadata, journaling, compaction, RAID, retries, or write amplification. Compression can reverse relationships at different boundaries. Direct I/O changes caching and alignment rules but does not mean “raw media cost.”

### Use a deterministic evidence reducer

The following reference reduces already captured phase metrics. It refuses to call wall-minus-CPU I/O time and exposes logical/physical differences. Its values are fixtures, not live measurements.

<!-- bijux-verify: {"id":"profile-evidence-reducer","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"phase residuals: [('parse', 2), ('compute', 'parallel-or-scope-mismatch'), ('spill', 30)]\npeak live MiB: 96\nallocation traffic MiB: 480\nread physical/logical: 0.25\nwrite physical/logical: 1.5\n","stderr":""}} -->
```python
phases = [
    {"name": "parse", "wall_ms": 12, "cpu_ms": 10, "live_mib": 20},
    {"name": "compute", "wall_ms": 30, "cpu_ms": 60, "live_mib": 48},
    {"name": "spill", "wall_ms": 45, "cpu_ms": 15, "live_mib": 96},
]

residuals = []
for phase in phases:
    if phase["cpu_ms"] <= phase["wall_ms"]:
        residual = phase["wall_ms"] - phase["cpu_ms"]
    else:
        residual = "parallel-or-scope-mismatch"
    residuals.append((phase["name"], residual))

logical_read_mib, physical_read_mib = 800, 200
logical_write_mib, physical_write_mib = 120, 180
print("phase residuals:", residuals)
print("peak live MiB:", max(phase["live_mib"] for phase in phases))
print("allocation traffic MiB:", 480)
print("read physical/logical:", physical_read_mib / logical_read_mib)
print("write physical/logical:", physical_write_mib / logical_write_mib)
```

The compute phase illustrates aggregate CPU exceeding wall. The spill residual suggests blocked or descheduled time but requires scheduler/I/O evidence. A 0.25 read ratio is consistent with caching or boundary mismatch; a 1.5 write ratio is consistent with amplification. Neither ratio alone identifies a cause.

### Measure profiler overhead and perturbation

Run the frozen benchmark without profiling, with the candidate profiling configuration, and—when useful—with a lower-rate configuration. Compare primary outcomes and system behavior. Overhead is not necessarily additive or constant: stack unwinding, event volume, buffer flushes, instrumentation locks, and memory tracking can change scheduling and cache behavior.

Detect lost events and buffer overflow. A trace with 5% reported loss may be unusable for reconstructing rare latency paths even if aggregate counts look stable. Sampling bias can arise when collection is disabled in privileged code or blocked by security policy. State unavailable evidence instead of substituting a differently scoped metric silently.

### Compare profiles by absolute cost

Percentages are compositional. If function F stays at 10 ms while total time falls from 100 to 50 ms, its share rises from 10% to 20% without regression. Compare absolute attributed cost under compatible totals, then show shares. Normalize event counts by relevant work—per operation, byte, edge, or instruction—only when that denominator matches the mechanism.

Differential profiles subtract comparable attribution buckets, but code motion and symbol changes complicate matching. Retain additions, removals, unresolved buckets, totals, and confidence. A profile ranking from one run is not stable merely because a visualization is crisp.

### Move from correlation to mechanism

A hotspot yields a hypothesis. Inspect the algorithm, source, generated code, data layout, and call path. Predict another observable consequence: fewer comparisons should reduce both comparator calls and CPU work; better blocking should change misses and transfer behavior; avoiding materialization should reduce allocation traffic and peak liveness.

Implement one controlled change, rerun correctness, and measure the unprofiled primary outcome plus predicted secondary evidence. If the hotspot shrinks but end-to-end time does not, work may have moved, the phase may not be on the critical path, or profiler attribution may have misled. Preserve negative results.

### Secure and govern profiling data

Profiles can contain paths, symbols, addresses, process identities, stack content, keys, or sampled data. Linux documents access controls and leakage risks for performance monitoring [1]. Use least privilege, minimize collected fields, protect artifacts, and review retention. Do not grant broad system capability merely to avoid explaining an unavailable event.

Bind profiles to run IDs and store commands, versions, configuration, event definitions, raw files, conversion scripts, and loss/overhead records. Derived flame graphs and tables are governed outputs; raw data remains the evidence. Platform-specific tools must be labeled, and instructions should include a no-privilege fallback when it preserves the question.

## Definitions and Notation

Let $T_w$ be wall time, $T_p$ process CPU time, $T_i$ inclusive attributed time for interval or stack $i$, and $T_i^{\mathrm{self}}$ exclusive cost. Let $A$ be cumulative allocated bytes, $L(t)$ live bytes, $L_{\max}=\max_t L(t)$ peak live bytes, and $R(t)$ RSS under a named interface. Let $B_{\mathrm{logical}}$ and $B_{\mathrm{physical}}$ be bytes at declared upper and lower I/O boundaries.

A **hotspot** has large attributed cost under one profile. A **bottleneck** constrains the measured outcome under current conditions. **Skid** is distance between an event and recorded sample location. **Multiplexing** time-shares limited counters. **Attribution error** assigns observed cost to the wrong semantic owner.

## Mechanisms, Invariants, or Proof Structure

### Time-accounting premise

For one thread and matching interval, its CPU time cannot exceed wall time because it executes on at most one processor at once. Summed CPU across threads can exceed wall. Therefore a negative residual is evidence of parallel aggregation or mismatched scope, not negative waiting.

### Memory conservation check

For a fully observed allocator event stream, live bytes satisfy $L(t)=L(0)+A(0,t)-F(0,t)$, where $A(0,t)$ and $F(0,t)$ are allocated and freed bytes through $t$. Real tools may omit allocators, sampling, mappings, metadata, or delayed release, so disagreement diagnoses coverage before it diagnoses a leak.

### I/O boundary check

No universal inequality relates logical and physical bytes. A cache permits $B_{\mathrm{physical}}<B_{\mathrm{logical}}$; read-ahead or amplification permits the reverse. Any ratio must name direction and boundaries. A causal claim needs layer-specific events or a controlled perturbation such as cache state, access order, or block size.

## Alternatives and Trade-Offs

| Technique | Strength | Main risk | Best use |
|---|---|---|---|
| phase timers | semantic attribution | manual boundaries, overlap | algorithm phases |
| statistical CPU sampling | low/moderate overhead | sampling and unwind bias | broad on-CPU search |
| event sampling | mechanism-focused | skid and event semantics | counter hotspots |
| full tracing | order and latency paths | volume, loss, privacy | concurrency and I/O |
| allocation tracing | precise creation sites | high overhead, missed allocators | allocation churn |
| heap snapshots | retained/live structure | temporal blind spots | leaks and retention |
| RSS polling | process residency trend | coarse attribution | capacity symptoms |
| system-call tracing | requested kernel interface | overhead, async gaps | syscall behavior |
| block/device counters | lower-layer traffic | weak semantic ownership | physical I/O |

Triangulation is usually stronger than one maximal trace. Every added collector changes cost and expands the evidence boundary.

## Failure Modes and Misconceptions

- **“Wall minus CPU is I/O.”** It contains every off-scope or unscheduled cause.
- **“CPU above 100% is invalid.”** Aggregate CPU can exceed wall on parallel workers; state the capacity denominator.
- **“The top frame is the root cause.”** It may implement work forced by representation, input, or caller policy.
- **“RSS is heap.”** RSS includes several resident mapping classes and tool-specific shared-page accounting.
- **“Allocated bytes are retained bytes.”** Cumulative churn can be huge while live memory stays small.
- **“Zero device reads means no I/O cost.”** Cache lookup, copying, parsing, faults, and prior population still cost resources.
- **“Counters are portable facts.”** Event definitions and support vary across processors, kernels, and scopes.
- **“A flame graph is a timeline.”** Standard aggregated stacks do not preserve execution order.
- **“Profiling overhead subtracts cleanly.”** Perturbation can change scheduling and behavior nonlinearly.
- **“Removing a hotspot guarantees speedup.”** Work can move or remain off the critical path.

## Worked Examples

### Example 1

**Situation.** A single-threaded run records 100 ms wall and 80 ms matching process CPU.

**Reasoning.** The 20 ms residual includes all time not charged as process CPU: blocking, descheduling, sleeps, or scope mismatch. Without scheduler and I/O events, labeling it storage wait is unsupported.

**Conclusion.** The residual narrows a question but does not name a cause.

### Example 2

**Situation.** Four workers complete in 100 ms wall with 340 ms aggregate CPU.

**Reasoning.** Average use is 3.4 processor-equivalents during the interval. This is compatible with parallel execution on at least four available processors. Normalize by declared capacity if reporting utilization.

**Conclusion.** CPU and wall diverge predictably under parallelism.

### Example 3

**Situation.** Function F rises from 10% to 20% after an optimization.

**Reasoning.** Total runtime fell from 100 to 50 ms while F stayed at 10 ms. Its percentage doubled because the denominator shrank; F did not regress. Compare absolute cost and total.

**Conclusion.** Profile shares are not independent quantities.

### Example 4

**Situation.** An allocation profiler reports 8 GiB allocated and 32 MiB peak live.

**Reasoning.** High churn with short lifetimes can produce both. Inspect allocation rate, lifetime, collector/allocator cost, and retained roots. Do not claim an 8 GiB memory footprint.

**Conclusion.** Traffic and capacity answer different questions.

### Example 5

**Situation.** Heap liveness is 200 MiB but RSS is 650 MiB.

**Reasoning.** Investigate allocator arenas and fragmentation, stacks, native allocations, code, shared libraries, mapped files, huge pages, and accounting semantics. Compare mapped regions and allocator statistics before blaming live objects.

**Conclusion.** RSS-minus-heap is a diagnostic gap, not automatically a leak.

### Example 6

**Situation.** An application reads 800 MiB logically while the device reports 200 MiB.

**Reasoning.** The 0.25 physical/logical ratio is consistent with page-cache service, but boundaries or concurrent traffic may differ. Verify cache state, returned bytes, faults, block events, device scope, and collection interval.

**Conclusion.** Cross-layer ratios require aligned identities and boundaries.

### Example 7

**Situation.** A write path emits 120 MiB logically and the device reports 180 MiB.

**Reasoning.** A 1.5 ratio can reflect metadata, journaling, compaction, RAID, retries, or unrelated device work. Trace the filesystem/block path or vary one mechanism; the ratio does not select among causes.

**Conclusion.** Amplification is observed at boundaries; its mechanism needs more evidence.

### Example 8

**Situation.** Eight requested hardware events show 25% time running after multiplexing.

**Reasoning.** Scaled totals extrapolate from limited scheduled time and may miss phase variation. Reduce events, group only compatible necessities, repeat, record enabled/running time, and compare with algorithm invariants.

**Conclusion.** A printed scaled count is not equivalent to continuous observation.

### Example 9

**Situation.** A 99 Hz sampler profiles a workload with a 10 ms periodic phase.

**Reasoning.** Nearly aligned periods can over- or undersample recurring code. Change or jitter the sampling frequency and compare results, while recording duration and sample count. Event-based sampling may offer a different view.

**Conclusion.** Sampling schedules can alias program schedules.

### Example 10

**Situation.** Replacing a comparator halves comparator samples but wall time is unchanged.

**Reasoning.** Check whether work shifted to key extraction or memory access, whether comparisons were outside the critical path, and whether profiled/unprofiled inputs match. Predict and measure comparison counts, CPU, misses, and end-to-end wall.

**Conclusion.** Causal validation must reconnect local change to the primary outcome.

## Cross-Program Connections

- [Operating Systems OS-038](../../22-operating-systems/modules/038-memory-mapped-files.md) explains file mappings that affect RSS and I/O.
- [Operating Systems OS-065](../../22-operating-systems/modules/065-i-o-schedulers.md) connects application requests to lower-layer scheduling.
- [Computer Architecture CA-040](../../23-computer-architecture/modules/040-analyzing-cache-misses-from-an-access-trace.md) connects trace evidence to cache behavior.
- [Concurrent and Parallel Programming CONPAR-092](../../04-programming-languages-concurrent-and-parallel-programming/modules/092-roofline-and-operational-intensity-analysis.md) uses measured rate ceilings and operational intensity.
- [Large-Scale Data Systems Engineering LSDS-057](../../21-large-scale-data-systems-engineering/modules/057-memory-cpu-and-i-o-isolation.md) extends resource attribution under shared systems.
- [Data Structures Engineering DSE-010](../../17-data-structures-engineering/modules/010-benchmarking-a-structure-without-misleading-results.md) ties profiles to representation experiments.

## References

1. Linux kernel documentation, *Perf Events and Tool Security*. [Official documentation](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html). Checked 2026-09-05; access controls and available facilities are kernel/configuration dependent.
2. Linux man-pages project, *perf_event_open(2)*, man-pages 6.17. [Manual page](https://man7.org/linux/man-pages/man2/perf_event_open.2.html). Checked 2026-09-05.
3. Python Software Foundation, *time — Time Access and Conversions*, Python 3.14 documentation. [Official documentation](https://docs.python.org/3/library/time.html). Checked 2026-09-05; runtime behavior remains platform dependent where documented.
4. Python Software Foundation, *tracemalloc — Trace Memory Allocations*, Python 3.14 documentation. [Official documentation](https://docs.python.org/3/library/tracemalloc.html). Checked 2026-09-05.
5. Valgrind Developers, *Massif: a Heap Profiler*, Valgrind manual. [Official manual](https://valgrind.org/docs/manual/ms-manual.html). Checked 2026-09-05.
6. Brendan Gregg, *Systems Performance: Enterprise and the Cloud*, 2nd ed., Addison-Wesley, 2020. ISBN 978-0-13-682015-4.
7. Brendan Gregg, “The Flame Graph,” *Communications of the ACM* 59(6), 2016, 48–57. [doi:10.1145/2909476](https://doi.org/10.1145/2909476). Checked 2026-09-05.
8. Raj Jain, *The Art of Computer Systems Performance Analysis*, Wiley, 1991. ISBN 978-0-471-50336-1.

## Exercises

### Exercise 1

Define wall time, process CPU, thread CPU, on-CPU sample, off-CPU interval, inclusive cost, and exclusive cost for a parallel shortest-path run.

### Exercise 2

A four-thread run takes 250 ms wall and 700 ms aggregate CPU. Compute average processor-equivalents. Explain why wall-minus-CPU is invalid and what additional evidence diagnoses low utilization.

### Exercise 3

A process reports 2 GiB cumulative allocations, 120 MiB peak traced live heap, 430 MiB peak RSS, and 700 MiB virtual size. Diagnose what each number establishes and propose next measurements.

### Exercise 4

Compare phase instrumentation, on-CPU sampling, allocation tracing, and block-I/O tracing for an external sort whose wall time regressed.

### Exercise 5

Design a low-perturbation profiling campaign for a parallel graph engine with intermittent latency and RSS spikes. Include hypotheses, workload/run identity, time, memory, I/O, counters, overhead checks, privacy, and causal validation.

## Answers to the Exercises

### Answer 1

Wall time is monotonic elapsed duration across the complete declared invocation. Process CPU sums user/system execution charged to the process; thread CPU narrows that to one worker, and neither includes unscheduled time. An on-CPU sample attributes a sampled executing context; an off-CPU interval uses scheduler/blocking evidence to attribute time not running. Inclusive stack cost includes descendant frames, while exclusive cost is attributed to the sampled frame itself. In a parallel run, inclusive costs overlap in wall time and aggregate process CPU can exceed wall; scopes, intervals, and execution contexts must accompany every value.

### Answer 2

Average processor-equivalents are $700/250=2.8$. Subtracting gives $250-700=-450$ ms because aggregate CPU spans multiple threads; it cannot estimate waiting. To diagnose why four threads average 2.8 rather than four, inspect runnable/off-CPU state, locks and queues, work/span and load balance, worker timelines, core placement and migration, throttling/frequency, page faults, I/O completion, and whether process CPU omits child or accelerator work. Compare matched profiled and unprofiled runs.

### Answer 3

Two GiB is allocation traffic across time, not simultaneous footprint. The 120 MiB is the traced tool’s peak live objects and may omit native allocators, mappings, metadata, or a missed spike. RSS says 430 MiB of named process mappings were resident under the platform interface; it is not all heap and shared-page attribution may vary. Virtual size reserves/maps 700 MiB but need not be resident. Next capture allocator statistics and fragmentation, mapped-region categories, native allocations, stacks, mapped files, shared pages, garbage-collector state, time-aligned RSS/live curves, and tool coverage/overhead.

### Answer 4

Phase instrumentation cheaply identifies whether read, run generation, spill, merge, or publication regressed, but inserted timers and asynchronous overlap need care. On-CPU sampling locates executing stacks with moderate overhead but misses blocking and depends on symbols/unwinding. Allocation tracing explains object churn and creation sites but can be intrusive and cannot alone explain RSS. Block-I/O tracing reveals request timing and lower-layer traffic but may require privileges, create large sensitive traces, and weakly attribute semantic ownership. Start with phase and unprofiled resource totals, then add one focused collector per competing hypothesis and validate the proposed mechanism under the primary benchmark.

### Answer 5

Freeze representative graph/query cases and run IDs. Hypotheses should distinguish work imbalance, lock/queue delay, garbage collection or native retention, cache/fault effects, and storage spill. Establish unprofiled wall/CPU/RSS/I/O baselines and correctness. Add stable phase/queue markers, low-rate on-CPU and scheduler sampling, time-aligned live-heap/allocator/RSS/mapping snapshots, and logical/syscall/block I/O only when spill is plausible. Record processor/kernel/tool/event definitions, enabled/running time, lost samples, symbols, placement, temperature, and state. Compare no-profile, chosen-rate, and lower-rate outcomes for perturbation; split collectors across matched runs if simultaneous overhead is material. Minimize stack/path/address payloads, use least privilege, and protect retention. For each hotspot, predict another observable change, implement one controlled modification, rerun the unprofiled benchmark and oracle, and report negative as well as supporting evidence within the sampled platform and workload scope.
