---
module_id: CONPAR-098
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 98
title: Tracing and Profiling Parallel Execution
status: complete
last_verified: 2026-08-29
---

# Tracing and Profiling Parallel Execution

## One-Page Review

### Governing question

How can measurements from threads, processes, accelerators, operating systems, and distributed services reconstruct enough causal and resource behavior to explain parallel performance without confusing observation, correlation, and proof?

### Essential definitions

- A **profile** aggregates measurements by code, calling context, resource, or state; it answers where cost accumulated.
- A **trace** records time-stamped events and relationships; it answers when observed events occurred and how they may relate.
- **instrumentation** emits data at selected operations; **sampling** observes execution periodically or after counter events.
- **wall time** is elapsed interval; **CPU time** accumulates scheduled CPU execution; **device time** belongs to an accelerator clock/domain.
- A **clock domain** is a time source with its own rate, resolution, offset, drift, synchronization, and monotonicity properties.
- A **correlation ID** joins logically related events across tasks, ranks, messages, streams, kernels, and services.
- A **span** is an interval with identity, start/end, attributes, status, and causal parent or links; nesting is not the only causality relation.
- **work** is total operation cost in the chosen metric; **span** or critical-path length is the longest dependency-chain cost.
- **inclusive cost** includes descendants; **exclusive cost** excludes them.
- **on-CPU**, **runnable**, **blocked**, **idle**, **device-active**, and **communication** are distinct states.
- **sampling bias** arises when observation probability, frequency, unwinding, multiplexing, or workload phase distorts estimates.
- **observer effect** is the behavior change caused by instrumentation, buffers, interrupts, serialization, synchronization, or output.
- **loss accounting** records dropped, overwritten, throttled, unsymbolized, uncorrelated, and unavailable observations.
- A **measurement claim** binds a finding to build, input, topology, tool/configuration, collection health, repeated runs, and uncertainty.

### Central model, mechanism, or theorem

Represent execution as a directed acyclic graph for the observed interval: vertices are measured operations with duration or resource cost, and edges are program order, task dependencies, synchronization, message, transfer, launch/completion, or explicit context links. Total work `W` is the sum of vertex costs in a non-overlapping metric; span `S` is the maximum dependency-path sum; average parallelism is `W/S`; observed elapsed time `T` satisfies model-dependent lower bounds such as `T >= max(S, W/P)` for `P` equivalent processors. A timeline alone establishes temporal overlap, not causality. Edges require semantic identifiers and API/runtime evidence; clock mapping and loss/overhead must be validated before quantitative conclusions.

### Critical invariants

The measured binary/configuration/input/topology are immutable and recorded; collection windows align; clocks are monotonic and mapped with uncertainty; stable IDs survive task migration and asynchronous boundaries; thread/process/device/rank identities do not collide; units are explicit; sampling period/frequency and multiplex scaling are retained; stack unwinding and symbols are validated; buffers report loss; instrumentation overhead is measured against a baseline; warm-up and steady-state phases are separated; causality is derived from semantics rather than visual proximity; work does not double-count overlapping metrics; critical paths follow legal dependencies; repeated runs expose variance; raw traces remain available; and findings never exceed collection coverage.

### Common failures

Teams profile a debug or different binary, omit symbols, measure startup instead of steady state, compare unlike inputs/topologies, read CPU utilization as useful work, infer dependency from adjacent bars, subtract timestamps from unsynchronized clocks, merge ranks with reused IDs, ignore buffer loss, confuse inclusive and exclusive time, sum overlapping intervals, treat samples as exact event counts, ignore profiler throttling/multiplexing, optimize a sampled hot function while the application waits elsewhere, attribute asynchronous GPU work to launch call duration, compare instrumented and baseline runs without uncertainty, expose sensitive trace baggage, or declare causality and scalability from one attractive visualization.

### Compact example

A dependency graph has operation durations `A=4`, `B=3`, `C=5`, `D=2`, with edges `A->B`, `A->C`, `B->D`, `C->D`. Work is 14; critical path is `A,C,D` with span 11; average parallelism is `14/11 = 1.273`. The sum of task durations is not elapsed time because B and C may overlap.

### Connections

[Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md) defines work and span. [Communication–Computation Overlap](086-communication-computation-overlap.md) distinguishes useful overlap. [Parallel Performance Models](091-amdahl-gustafson-and-work-span-models.md) supplies bounds. [Systematic Concurrency Testing](097-systematic-concurrency-testing.md) provides causal replay traces. The [program roadmap](../ROADMAP.md) next addresses failure containment in long-running jobs.

## Governing Question

Which collection method, clock/correlation model, metric semantics, experimental design, and evidence checks are necessary to distinguish computation, waiting, scheduling, communication, memory, and device bottlenecks in a parallel execution?

Tracing and profiling are measurement sciences. Tools produce observations, not explanations automatically. A defensible explanation combines semantic relationships, calibrated collection, repeated experiments, and a falsifiable optimization hypothesis.

## Why This Matters

Parallel performance is temporal and relational. A flat profile may show an expensive barrier but not which rank arrived late. A trace may reveal the late rank but not which instruction or memory event consumed cycles. GPU launch calls are short while kernels execute asynchronously. High CPU utilization can be spin waiting. Low utilization can be intentional blocking or insufficient parallelism.

The observer changes the system. Fine-grained events consume bandwidth, perturb caches, add synchronization, overflow buffers, and alter scheduling. Sampling reduces overhead but introduces uncertainty and may miss short or phase-specific behavior. Distributed clocks drift; accelerator clocks need correlation; identifiers can be lost across queues.

Production-grade analysis therefore begins with a question and chooses the narrowest credible signal. It validates collection health, reconstructs causal structure, compares controlled repetitions, tests one change at a time, and retains raw evidence plus limitations.

## Prerequisites and Retrieval

Retrieve:

- speedup, work/span, load imbalance, communication overlap and scaling from [Work Stealing](047-work-stealing.md), [Communication–Computation Overlap](086-communication-computation-overlap.md), [Load Imbalance Across Nodes](088-load-imbalance-across-nodes.md), [Scaling a Parallel Program Across Multiple Nodes](090-scaling-a-parallel-program-across-multiple-nodes.md), and [Amdahl, Gustafson, and Work–Span Models](091-amdahl-gustafson-and-work-span-models.md);
- CPU, NUMA, GPU and hybrid placement from [NUMA-Aware Allocation and Scheduling](093-numa-aware-allocation-and-scheduling.md) and [Hybrid Threads, SIMD, GPU, and Message Passing](094-hybrid-threads-simd-gpu-and-message-passing.md); and
- deterministic causal evidence from [Designing for Replayable Concurrency](070-designing-for-replayable-concurrency.md) and [Systematic Concurrency Testing](097-systematic-concurrency-testing.md).

Retrieval prompt: state question and expected mechanism; build/commit/toolchain; workload/input/phase; hosts/CPUs/NUMA/GPUs/ranks/threads/affinity/frequency; profiler/tool/version/config/permissions; instrumentation and sampling events; clock domains/mapping uncertainty; IDs/context propagation; buffers/loss; symbols/unwinding; warm-up/window/repetitions; baseline overhead; metric units/scaling; dependency schema; analysis query; hypothesis/intervention; raw artifacts; sensitive fields; and unsupported coverage.

## Learning Objectives

After completing this module, a learner can:

1. choose counters, statistical profiles, traces, and application annotations by question;
2. distinguish wall, CPU, runnable, blocked, communication, and accelerator time;
3. validate clock mapping, context propagation, symbols, stacks, buffers, and loss;
4. reconstruct task/message/launch dependencies without inferring causality from proximity;
5. compute work, span, average parallelism, utilization, imbalance, and overlap with correct denominators;
6. identify sampling, multiplexing, observer, warm-up, phase, and survivorship biases;
7. analyze threads, MPI ranks, GPU streams, NUMA nodes, and hybrid execution together;
8. design reproducible before/after experiments with uncertainty and equivalence gates;
9. operate scalable, secure trace collection and artifact retention; and
10. constrain high-stakes performance conclusions to reviewed evidence.

## Core Exposition

### Begin with a falsifiable question

“Why is it slow?” is not a collection plan. Ask whether elapsed time is limited by one serial dependency, load imbalance, runnable delay, lock contention, memory stalls, communication, synchronization, GPU starvation, transfers, or excessive task granularity. State what observation would support and refute each hypothesis.

Choose counters for aggregate resource events, samples for code/calling-context attribution, instrumentation for exact semantic operations, and tracing for ordering/overlap. Start low overhead, then narrow the window and add detail. Avoid collecting every signal across a full-scale run merely because the tool permits it.

Record a run identity: source and binary digest, compiler/link flags, libraries/runtime/drivers/firmware, machine allocation, CPU model/frequency policy, NUMA/affinity, GPU and interconnect, rank/thread placement, environment, input, seed, warm-up, measured phase, tool and configuration. Performance comparisons without configuration equivalence are anecdotes.

### Understand measurement semantics

Elapsed wall duration describes user-visible completion. CPU time sums scheduled execution across threads and can exceed wall time. Runnable time means eligible but not scheduled. Blocked time needs a reason: mutex, condition, I/O, page fault, MPI, device synchronization, or scheduler. Spin loops appear on-CPU but may perform no useful work.

Hardware counters count or estimate architected/microarchitectural events within documented scope. Events, names, privilege levels, skid, counter width and availability vary. When more events are requested than physical counters, multiplexing time-shares them and scales counts; retain time-enabled/time-running and reject inadequate coverage. Derived ratios require compatible denominators and intervals.

Samples estimate where selected events occurred. Expected sample share can approximate cost share when observation is representative, but short regions, aliasing with periodic behavior, throttling, migration, lost samples and failed stack unwinding bias results. Confidence grows with independent samples and repeated runs, not prettier percentages.

Instrumentation provides semantic identity but adds calls, timestamps, buffering and data. Inclusive duration of a parent overlaps children; summing both double-counts. Event counts may be exact only if every event is emitted and retained. Validate loss counters and buffer policy.

### Compute work and critical path

This deterministic model calculates work and longest dependency path for four operations. It assumes durations are additive vertex weights and dependencies are complete; it does not collect a trace, correct clocks, model resource contention, or prove the measured program has this DAG.

<!-- bijux-verify: {"id":"trace-dag-work-span","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"topological_order=A,B,C,D\nwork=14\ncritical_path=A,C,D\nspan=11\naverage_parallelism=1.272727\nlower_bound_p2=11\n","stderr":""}} -->
```python
durations = {"A": 4, "B": 3, "C": 5, "D": 2}
predecessors = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]}
order = ["A", "B", "C", "D"]
longest = {}
paths = {}
for operation in order:
    if predecessors[operation]:
        parent = max(predecessors[operation], key=lambda item: longest[item])
        longest[operation] = longest[parent] + durations[operation]
        paths[operation] = paths[parent] + [operation]
    else:
        longest[operation] = durations[operation]
        paths[operation] = [operation]
work = sum(durations.values())
end = max(order, key=lambda item: longest[item])
span = longest[end]
lower_bound_p2 = max(span, (work + 1) // 2)
print(f"topological_order={','.join(order)}")
print(f"work={work}")
print(f"critical_path={','.join(paths[end])}")
print(f"span={span}")
print(f"average_parallelism={work / span:.6f}")
print(f"lower_bound_p2={lower_bound_p2}")
```

Construct edges from semantics: actor program order, spawn/join, future completion/await, lock release/acquire, message send/matched receive, collective membership, transfer completion, stream/event dependency, kernel launch/completion, and explicit trace context. Mere timestamp order is not causality. Missing IDs create uncertain edges; preserve uncertainty rather than inventing a path.

Critical-path cost identifies work that directly constrains the observed completion under the graph model. Optimizing an off-path hot operation may save resources without reducing latency. Conversely, a short task can be decisive because successors wait for it. Compare the path across runs; optimization can move the bottleneck.

### Align clocks and identities

Use monotonic clocks for local durations. Wall clocks can step under synchronization adjustments. Each host, process runtime, device, and NIC may have a separate clock with offset and drift. Map clocks through documented correlation samples, fit offset/rate over the collection interval when necessary, retain residual/error bounds, and never claim ordering finer than uncertainty.

For messages, causal send/receive identities can order events without synchronized wall clocks. For GPU work, use runtime/tool correlation between host launch and device timestamps rather than subtracting raw clocks. Long runs require periodic recalibration; migration between cores may matter on platforms without a consistently synchronized source.

Identifiers need a namespace: run, host, process/rank, thread/task, resource, operation/span, message, stream, device, kernel and object generation. Thread IDs and addresses can be reused. Propagate context explicitly across work queues, futures, RPC and messages; links represent fan-in/fan-out better than forcing a false parent tree. Validate missing, duplicate, forged and high-cardinality context.

### Validate collection health

Before interpreting, inspect tool exit status, target start/end, recording window, event support, permissions, frequency/period, throttling, multiplex ratios, sample/event/loss counts, buffer fill/overwrite, stack-unwind failures, symbol/module mapping, clock calibration, ID orphans, truncated files and exporter/backpressure errors.

Run known-positive probes: a named busy loop should attract CPU samples; a controlled sleep should appear blocked; an annotated region should start/end once; a message should correlate; a kernel should appear on the intended device/stream. A missing expected probe invalidates related absence claims.

Measure observer effect with representative unprofiled and profiled repetitions. Compare elapsed distribution, throughput, memory, I/O, scheduling, rank skew and outputs. A small total overhead can still reorder fine-grained tasks. Reduce annotation rate, sample frequency, call stacks, metrics, ranks, duration, or event detail until collection is healthy, but record what was removed.

### Analyze parallel states and imbalance

Partition each worker's measured interval into useful work, scheduler/runtime overhead, runnable delay, synchronization wait, communication wait, I/O, device wait, idle and unknown. Categories must be mutually exclusive for occupancy sums. Define utilization denominator: allocated cores, available cores, active worker capacity, GPUs, or interval wall time.

For each phase, compare per-rank/thread task counts, useful durations, arrival times and exit times. Maximum, median, tail, coefficient of variation and critical-rank identity are more informative than mean alone. Barrier time is a symptom: trace backward from last arrival to its work, scheduling, NUMA placement, communication, data partition or OS noise.

Distinguish insufficient parallelism from scheduling failure. A DAG with average parallelism 1.27 cannot sustain eight workers even with perfect scheduling. A wide ready queue plus idle cores implicates affinity, runtime throttling, resource constraints or visibility. Empty ready queues implicate dependencies or task creation.

### Analyze CPU, memory, MPI, and GPU together

CPU profiles need reliable stacks and module symbols. Attribute samples to calling context, not only leaf functions. Separate user/kernel/guest and on/off-CPU views. Use hardware counters after identifying a region; derive bandwidth or miss rates with correct event semantics rather than generic labels.

MPI analysis correlates rank-local compute, point-to-point messages, collectives and MPI implementation state. Match messages using communicator, source/destination, tag, sequence/request identity where available. Collective duration alone does not distinguish late arrival, algorithm, network or progress. MPI profiling and tool interfaces expose implementation-dependent data; enumerate names at runtime and record portability limits.

For GPUs, correlate host API, queues/streams, transfers, kernels, synchronization and device activity. Launch duration is host enqueue cost, not kernel duration. Explain gaps: CPU failed to submit, dependency blocked, transfer serialized, device resource unavailable, or instrumentation missing. Kernel occupancy is not achieved useful throughput; combine timeline with kernel metrics and correctness.

Hybrid analysis must preserve which rank/thread owns each device context and buffer. Oversubscription, NUMA distance, shared-copy engines, MPI progress threads and GPU context serialization cross layers. One tool rarely sees every layer; merge only formats with defined clocks, IDs, units and provenance.

### Distinguish overlap from progress

Two bars overlap in time but may compete for the same bottleneck. Define useful overlap as both activities make required progress. Compare bytes/operations completed, resource counters and end-to-end critical path. Communication hidden behind computation reduces exposed wait only if dependencies allow consumption afterward.

Compute overlap from interval intersections only when intervals share a trustworthy clock and categories. Avoid summing pairwise overlap across many tasks because the same time can be counted repeatedly. Use a sweep or occupancy timeline for union/intersection. Keep host, device and network resource dimensions distinct.

### Design before/after experiments

Freeze correctness, input, result digest, build mode, affinity, topology, warm-up and measurement window. Randomize or interleave baseline and candidate runs to reduce temporal drift. Run enough independent repetitions to report median and dispersion or confidence intervals; retain raw values and outliers with causes when known.

Predeclare primary metrics and practical threshold. Check that collection health and profiler overhead are comparable. A statistically detectable change may be operationally irrelevant; a large apparent change from different frequency, cache warmth or node placement is invalid. Confirm the hypothesized mechanism in traces/counters, not only elapsed time.

After optimization, rerun correctness, sanitizer/systematic tests, resource limits and full-scale behavior. Reduced time can come from omitted work, precision loss, changed semantics or measurement gaps. Inspect work/output invariants.

### Operate secure scalable evidence

Trace size grows with event rate × participants × duration × bytes/event. Budget per rank/device, use bounded buffers with explicit loss, selective windows, trigger/snapshot modes, aggregation, compression and governed retention. Never let all ranks overwrite one filename. Store schemas, analysis queries and tool versions with raw evidence; exported images alone are not reproducible.

Traces reveal source paths, symbols, topology, hostnames, message sizes, identifiers, queries and baggage. Do not place secrets or personal data in context. Validate untrusted trace headers, restrict propagation, pseudonymize, encrypt, authorize access and bound retention. Profiling permissions and kernel/device interfaces expand attack surface.

### High-stakes limits

For real-time or safety-critical systems, profiling overhead can cause deadline failure or hide it. Use qualified/noninterfering target mechanisms where required, measure perturbation, preserve target equivalence and combine with hardware timing analysis. Average latency never establishes worst-case execution time.

Named performance/real-time, concurrency/runtime, compiler/hardware/device/network, domain/safety, security/privacy, operations, quality/regulatory, human-factors/accessibility, ethics and independent validation reviewers must approve high-stakes evidence. No trace alone certifies deadlines, capacity or safe operation.

## Definitions and Notation

- `W`: total non-overlapping work in a declared cost metric.
- `S`: longest dependency-path cost (span).
- `P`: equivalent processing resources in the stated model.
- `T`: measured elapsed time for aligned interval.
- `A = W/S`: average parallelism of the modeled DAG.
- `U = useful_resource_time / available_resource_time`: utilization with named numerator/denominator.
- `C_i(t)`: mapping from clock domain `i` to reference time, with uncertainty `epsilon_i`.
- `L`: loss ledger: expected, recorded, dropped, overwritten, throttled, unsymbolized and orphaned observations.
- `O`: measured observer effect between comparable baseline/profiled distributions.
- `E`: evidence package: identities, configuration, health, raw data, query, results, uncertainty, limitations and reviewers.

## Mechanisms, Invariants, or Proof Structure

### Experimental-equivalence proof

Bind baseline/candidate to source, binary, input/output, topology, affinity, environment, phase and run protocol. Record deviations and randomization/repetition; reject semantic or collection inequivalence.

### Collection-integrity proof

Validate supported events, clocks, correlation, symbols/stacks, buffers/loss, sampling/multiplex scaling, target window and overhead with known-positive probes and health counters.

### Causal-analysis proof

Derive graph edges from runtime/API semantics and stable identities; mark missing/uncertain edges; compute work/span/overlap without double-counting; connect bottleneck to a falsifiable mechanism.

### Intervention proof

Change one owned mechanism; preserve correctness/work/output; repeat equivalent measurements; demonstrate both end metric and predicted causal signal; check bottleneck migration and regressions.

### Claim-boundary proof

Handoff names workload, scale, hardware, tools, clocks, sampling/events, loss, overhead, uncertainty, unsupported layers, raw artifacts, analysis query and review. It never generalizes one observed execution to universal causality, scalability or worst-case timing.

## Alternatives and Trade-Offs

| Method | Best evidence | Principal limitation |
|---|---|---|
| aggregate counters | low-overhead resource totals | weak code/causal attribution |
| statistical sampling | calling-context cost estimates | uncertainty, bias and unwind loss |
| function instrumentation | exact entered regions/counts | overhead and nesting double-count risk |
| event tracing | ordering, overlap and waits | volume, clocks and observer effect |
| distributed spans | cross-service logical flow | sampling/context gaps; coarse runtime detail |
| hardware tracing | detailed control flow/events | platform, privilege, volume and decode limits |
| application annotations | domain-semantic phases/tasks | maintenance and coverage burden |
| controlled scheduler trace | reproducible causal choices | modeled rather than natural timing |
| analytic performance model | explanatory bounds/prediction | assumptions require measurement validation |

## Failure Modes and Misconceptions

- **“The tallest bar caused latency.”** only dependency-path work constrains that completion.
- **“Temporal order proves causality.”** semantic edges are required.
- **“CPU utilization is useful work.”** spinning/runtime overhead also consume CPU.
- **“A GPU launch duration is kernel time.”** launches are asynchronous.
- **“Samples are exact counts.”** they are observations under a sampling process.
- **“One hundred percent means all cores.”** define the denominator and tool convention.
- **“Inclusive times can be summed.”** descendants overlap parents.
- **“Clock synchronization is exact.”** retain offset/drift uncertainty.
- **“Thread IDs are globally unique.”** namespace and generation are needed.
- **“No event means no activity.”** loss, filters, permissions or unsupported APIs may explain absence.
- **“Low average overhead means no perturbation.”** local schedule effects can be large.
- **“More events improve truth.”** excess collection can lose data and alter behavior.
- **“Barrier optimization starts at the barrier.”** find the last arriver's causal path.
- **“Occupancy means throughput.”** active resources may stall or do unnecessary work.
- **“One run establishes improvement.”** quantify variation and equivalence.
- **“Faster output is correct output.”** preserve work/result invariants.
- **“A screenshot is evidence.”** retain raw data, schema, query and configuration.
- **“Average latency proves deadlines.”** worst-case claims need different evidence.

## Worked Examples

### Example 1

**DAG analysis.** Four operations have work 14 and span 11. **Conclusion:** eight workers cannot overcome dependency-limited average parallelism 1.273.

### Example 2

**Last arriver.** Seven ranks wait in a collective while rank 3 handles twice the partition. **Conclusion:** the collective is where imbalance becomes visible, not necessarily its cause.

### Example 3

**Runnable delay.** Ready tasks coexist with idle allocated cores because affinity confines workers to two CPUs. **Conclusion:** distinguish scheduler placement from DAG width.

### Example 4

**Sampling loss.** Thirty percent of requested counter time is multiplexed away and stacks fail in a key library. **Conclusion:** quantify/reconfigure before ranking hotspots.

### Example 5

**Clock error.** Host A appears to receive before host B sends within a 400-microsecond mapping uncertainty. Message identity establishes causality; timestamps cannot order them finely. **Conclusion:** uncertainty bounds interpretation.

### Example 6

**GPU gap.** Host thread blocks before enqueueing the next kernel; device goes idle. **Conclusion:** correlate host scheduling and stream dependencies before tuning kernel occupancy.

### Example 7

**False overlap.** Compute and transfer timelines overlap, but both contend for memory bandwidth and completion slows. **Conclusion:** temporal intersection is not useful progress.

### Example 8

**Observer effect.** Full call tracing adds 18% elapsed time and removes task stealing; lower-rate sampling plus targeted annotations preserves behavior. **Conclusion:** collection fidelity includes perturbation.

### Example 9

**Before/after.** Candidate median improves 8%, output digest matches, but CPU frequency differs. Rerun interleaved under fixed policy. **Conclusion:** mechanism and equivalence precede credit.

### Example 10

**Emergency dispatch platform.** Trace evidence must preserve incident/unit/operator/authorization/location/configuration generations, causal assignment/acknowledgment/status edges, clock uncertainty, offline gaps, priority/preemption, overload/degraded paths, deadline distributions and protected sensitive data. Named emergency-operations/domain, real-time/performance, concurrency/runtime, network/device/GIS, safety/security/privacy, reliability/operations, quality/regulatory, human-factors/accessibility, ethics and independent validation reviewers must approve any capacity or deadline claim; none is claimed here. **Conclusion:** observed traces cannot authorize emergency-service capacity.

## Cross-Program Connections

- **Algorithms:** DAGs and longest paths connect traces to work/span bounds.
- **Operating systems:** scheduling, counters, tracepoints, interrupts and symbols shape visibility.
- **Compilers:** optimization, inlining, frame information and code layout change attribution.
- **Distributed systems:** causal context, clock uncertainty, messages and partial traces cross hosts.
- **Databases/data engineering:** trace schemas, joins, aggregation and lineage determine analysis correctness.
- **Cloud/platform:** topology, throttling, virtualization, collectors and retention affect production evidence.
- **GPU/HPC:** ranks, streams, devices and interconnects require multi-clock multi-resource analysis.
- **Security/privacy:** context and symbols disclose architecture and data.
- **Statistics:** sampling, repetition, uncertainty and experiment design constrain conclusions.
- **Safety:** worst-case and hazard evidence exceed average profiling.

## References

1. OpenTelemetry Project, *OpenTelemetry Specification 1.60.0*, current specification; retrieved 2026-08-29. <https://opentelemetry.io/docs/specs/otel/>
2. W3C, *Trace Context Level 2*, W3C Candidate Recommendation Snapshot; retrieved 2026-08-29. <https://www.w3.org/TR/trace-context-2/>
3. Linux perf contributors, *perf: Linux Profiling with Performance Counters*, current documentation; retrieved 2026-08-29. <https://perfwiki.github.io/main/tutorial/>
4. HPCToolkit Project, *HPCToolkit User Documentation*, current documentation; retrieved 2026-08-29. <https://hpctoolkit.gitlab.io/hpctoolkit/users/>
5. VI-HPS, *Score-P and OTF2 Documentation*, current documentation; retrieved 2026-08-29. <https://www.vi-hps.org/projects/score-p/documentation/documentation.html>
6. Lawrence Livermore National Laboratory, *Caliper 2.15.0 Documentation*, current documentation; retrieved 2026-08-29. <https://software.llnl.gov/Caliper/>
7. NVIDIA, *Nsight Systems User Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/nsight-systems/UserGuide/>
8. Intel, *Intel VTune Profiler Documentation*, current documentation; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler-documentation.html>
9. MPI Forum, *MPI 5.0: Tool Support and Performance Variables*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node403.htm>
10. Jeffrey K. Hollingsworth, Barton P. Miller, and Jon Cargille, “Dynamic Program Instrumentation for Scalable Performance Tools,” Scalable High-Performance Computing Conference, 1994. <https://doi.org/10.1109/SHPCC.1994.296656>

## Exercises

### Exercise 1

For the executable DAG, add edge `B->C`. Recompute work, span, average parallelism and the lower bound for two processors. Explain why work stays constant.

### Exercise 2

Design a collection-health checklist and known-positive probes for a 64-rank CPU application. Include counters, sampling, call stacks, MPI events, clocks, IDs, loss, overhead and artifacts.

### Exercise 3

A hybrid run has CPU tasks, host-to-device transfers, two GPU streams and an MPI progress thread. Define correlation IDs, causal edges, clock mappings, mutually exclusive state categories and three bottleneck hypotheses with refuting evidence.

### Exercise 4

Design a before/after experiment for reducing a collective's exposed wait. Include equivalence, repetition, uncertainty, critical-path analysis, output correctness, profiler perturbation and bottleneck migration.

### Exercise 5

Transfer trace/profile evidence to a concurrent air-traffic flow-management service. Specify identity, time, causality, deadline/capacity, loss, security, failure, validation and named reviewer invariants without claiming operational approval.

## Answers to the Exercises

### Answer 1

The new dependencies force `A,B,C,D`; work remains `4+3+5+2=14` because task costs did not change. Span becomes 14, average parallelism `14/14=1`, and `max(S, ceil(W/2)) = max(14,7)=14`. Work counts required operation cost; adding precedence reduces available concurrency but does not add work. This assumes additive non-overlapping vertex weights and complete dependencies, not measured contention.

### Answer 2

Record binary/source/tool/kernel/CPU/topology/affinity/input/window. Confirm all ranks start/end and unique rank/process/thread IDs. Query event support/units/privilege; retain sample period/frequency, time-enabled/time-running, throttling and loss. Known probes include a symbolized busy loop attracting samples, controlled sleep appearing off-CPU, nested annotation count/duration, matched rank message, and barrier with one delayed rank. Check module maps, call-stack depth/unwind failures, clock offsets/drift/residuals, orphan/duplicate correlations, buffer fill/overwrite and rank-unique files. Compare multiple unprofiled/profiled runs for elapsed, rank skew, memory and output. Retain raw files, schema, exact commands, health report, analysis query and limitations; fail related absence claims when probes or collection health fail.

### Answer 3

Namespace run/rank/process/thread/task/message/request/buffer-generation/device/context/stream/transfer/kernel IDs. Edges include actor order, task spawn/join, MPI send/request completion and matched receive, buffer readiness to transfer, transfer completion to kernel, stream/event dependencies, kernel completion to return transfer/consumer, and progress-thread completion to application request. Map CPU monotonic clocks per host and each device clock through repeated tool correlation samples with residual uncertainty; use message causality across hosts. Partition CPU capacity into useful/runnable/blocked/spin/runtime/MPI/device-wait/idle/unknown and each GPU engine into kernel/transfer/idle/unknown without double-counting. Hypotheses: CPU submission starvation (refuted by ready kernels queued before gaps), transfer serialization (refuted by independent copy-engine overlap and no dependency), or MPI progress delay (refuted by timely request completion before critical consumer). Resource counters and path movement must support the surviving mechanism.

### Answer 4

Freeze build mode, result digest, input/partition, ranks/threads, nodes/network, affinity/frequency, MPI/runtime settings, warm-up and phase. Interleave randomized baseline/candidate repetitions; report raw elapsed/exposed-wait values, median and dispersion/confidence interval plus a practical threshold. Validate identical profiler configuration, loss, clock uncertainty, symbols and comparable overhead. Build semantic message/collective/task edges and show the late-arrival or communication segment leaves the critical path, rather than merely shrinking an inclusive MPI bar. Confirm work/item/message/output invariants and correctness tests. Inspect whether synchronization, computation, network, memory or another collective becomes critical at small and full scale. Reject improvement if outputs differ, collection health fails, configurations differ or the proposed causal signal does not change.

### Answer 5

Use synthetic/deidentified traffic scenarios in an isolated non-operational environment. Namespace flight/track/plan/sector/constraint/clearance/controller/session/model/weather/configuration and message generations; propagate authenticated correlation without sensitive baggage. Use monotonic clocks within nodes, calibrated mappings with uncertainty across nodes/sensors, and semantic ingest/validation/prediction/conflict-detection/recommendation/acknowledgment edges. Define deadlines and capacity by percentile plus worst-case/hazard evidence separately; record loss, orphan context, clock gaps, stale/duplicate/out-of-order tracks, partition/restart/overload/degraded behavior and human acknowledgment. Bind traces to target-equivalent build/configuration/scenario/topology, validate collection probes/overhead, preserve raw governed evidence and independent output/safety checks. Encrypt, restrict, audit and expire artifacts; reject untrusted context and exclude operational credentials/routes. Named air-traffic operations/control, aviation safety/human factors, real-time/performance/concurrency, surveillance/weather/network, software/hardware/toolchain, cybersecurity/privacy, reliability/operations, quality/regulatory/certification, accessibility/ethics and independent validation reviewers must approve claims. No external review, capacity guarantee, deadline proof, certification or operational authorization is claimed.
