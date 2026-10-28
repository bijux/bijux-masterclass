---
module_id: OS-080
program: Operating Systems
level: 2
module_number: 80
title: Profiling the Kernel Network Path
status: complete
last_verified: 2026-09-04
---

# Profiling the Kernel Network Path

## One-Page Review

### Governing question

How should an engineer measure a kernel network path deeply enough to localize CPU, queueing, drops, wakeups, ownership, offload, memory, and device delay while preserving clock meaning, packet identity, workload representativeness, system safety, privacy, and an honest account of observer effect?

### Essential definitions

- A **measurement question** names one outcome, population, interval, scope, and suspected mechanism before instrumentation is chosen.
- A **stage boundary** is an observable transition such as device completion, NAPI poll, protocol entry, socket enqueue, task wake, syscall return, qdisc enqueue, driver submit, or transmit completion.
- **Residence time** is elapsed time between entry and exit of a queue or stage; **service time** is active processing time and need not equal residence.
- A **tracepoint** is a statically defined event with a more durable field contract than a probe attached to an internal function.
- A **dynamic probe** observes a function or instruction location not already covered by a suitable stable event and is sensitive to kernel layout and optimization.
- A **sampling profiler** periodically attributes on-CPU execution to instruction pointers or call stacks; it estimates CPU cost, not off-CPU queue delay.
- A **histogram** aggregates a value distribution into bounded buckets or keyed summaries instead of retaining every event.
- A **clock domain** is one timestamp source and synchronization scope, such as NIC hardware, monotonic kernel time, per-CPU cycle counter, or userspace clock.
- **Observer effect** is the change in workload or system behavior caused by instrumentation, collection, symbolization, storage, or analysis.
- **Drop attribution** identifies the earliest stage and reason that abandoned a packet, distinct from downstream symptoms such as retransmission or timeout.

### Central model, mechanism, or theorem

Represent an observation as

$$
O=(q,p,g,s,c,t,k,v,w,e),
$$

where $q$ is the measurement question, $p$ the packet or sampled-flow identity, $g$ configuration generation, $s$ stage, $c$ CPU, queue, device and namespace context, $t$ timestamp plus clock domain, $k$ event kind, $v$ typed values, $w$ sampling weight, and $e$ instrumentation error or loss.

End-to-end latency can be decomposed only when events belong to the same logical work and clocks are comparable. CPU samples explain where execution time accumulates; paired events explain residence; counters explain populations and loss; packet or receiver evidence validates wire semantics. No single instrument proves all four.

### Critical invariants

- Every measurement states population, units, clock, sampling rule, configuration generation, aggregation and known exclusions.
- Timestamps are subtracted only within one coherent clock or after measured cross-clock calibration with uncertainty.
- Packet identity survives aggregation, segmentation, cloning, retransmission and sampling only under an explicit correlation rule.
- Stage entry and exit pair by a key whose reuse, concurrency, loss and lifetime are bounded.
- Per-CPU counters are combined with their reset, wrap, migration and read-consistency semantics.
- Trace buffers, maps, histograms, stack stores and output channels are bounded; lost events are counted and reported.
- Instrumentation never dereferences unproved packet data, retains stale kernel pointers, or logs sensitive payload by default.
- Profiling overhead is measured against a baseline at representative load and includes consumer, symbolization and storage cost.
- Offload and capture points are named so aggregates, wire packets, device time and host time are not conflated.
- Causal claims require a controlled intervention or convergent independent evidence, not merely temporal correlation.

### Common failures

Common failures are starting with a fashionable tool rather than a question, calling function duration packet latency, subtracting NIC and host clocks without calibration, correlating by reused pointer after object free, counting one GRO or GSO aggregate as one wire packet, sampling only successful packets, ignoring trace-buffer loss, summing per-CPU counters across reset, attaching unstable probes when tracepoints exist, tracing every packet at line rate, generating unbounded flow-cardinality maps, symbolizing in the hot path, exposing addresses or payload, treating a flame graph as wall-time analysis, changing several tunables at once, and concluding causation from one before/after run.

### Compact example

One correlated receive sample reaches device completion at 100 µs, driver handoff at 108, protocol processing at 135, socket enqueue at 150, and application observation at 220 on a coherent clock. Stage deltas are 8, 27, 15, and 70 µs; total is 120 µs. The largest observed interval is socket-to-application, suggesting scheduler, wakeup, socket queue, or application investigation. One sample does not establish a distribution, and these boundaries do not separate every mechanism inside the 70 µs interval.

### Connections

[OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-070](070-designing-an-i-o-path-for-latency-or-throughput.md), and [OS-071](071-socket-layer-architecture.md) through [OS-079](079-offload-and-receive-side-scaling.md) connect profiling to clocks, concurrency, memory, queues, packets, offload, sockets and causal diagnosis.

## Governing Question

The kernel network path is not one call stack. Receive work begins in a device and DMA ring, crosses interrupt or polling contexts, may move among CPUs, becomes protocol and socket state, wakes a task, and ends in userspace. Transmit runs through socket memory, protocols, qdiscs, device queues and later completion. Offload changes where work occurs and what any observer sees.

The governing question is how to build a trustworthy evidence chain across those boundaries without turning the measurement system into the bottleneck. Profiling must distinguish on-CPU work, queued residence, deferred device work, contention, memory locality and downstream application delay. It must also state what could not be observed.

## Why This Matters

Network incidents often present far from their cause. An application timeout can originate at NIC ring loss, NAPI budget exhaustion, protocol rejection, filter drop, socket overflow, scheduler delay or peer behavior. Increasing every queue can hide loss while worsening tail latency.

Optimizations also shift work. GRO reduces packet-processing calls but changes observation granularity. TSO moves segmentation beyond host capture. RPS can reduce one CPU's load while adding IPIs and remote memory. Aggregate throughput can improve while one tenant's p99 deteriorates.

Kernel instrumentation is privileged and potentially disruptive. Dynamic probes can depend on build-specific layouts. Full packet keys create high cardinality and sensitive logs. A rigorous plan uses the least invasive instrument that answers the question, bounds every state structure, and validates overhead.

## Prerequisites and Retrieval

Review [OS-004](004-interrupts-and-exceptions.md), [OS-007](007-kernel-data-structures.md), [OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-070](070-designing-an-i-o-path-for-latency-or-throughput.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), [OS-074](074-protocol-processing.md), [OS-075](075-routing-and-neighbor-tables.md), [OS-076](076-connection-state-management.md), [OS-077](077-congestion-control-hooks.md), [OS-078](078-packet-filtering.md), and [OS-079](079-offload-and-receive-side-scaling.md).

Retrieve these distinctions:

- device timestamp, interrupt time, NAPI processing, queue residence, task wakeup, scheduled execution and syscall return are different events;
- wall time, on-CPU time, off-CPU time, queue delay, service time and completion time are different measures;
- tracepoint, function trace, dynamic probe, sampling profile, hardware counter, packet capture and application trace have different evidence;
- packet, SKB, GSO aggregate, GRO aggregate, fragment, clone, retransmission and socket byte range have different identity;
- device queue, NAPI budget, CPU backlog, protocol queue, socket queue, qdisc and application queue are different capacity stages;
- counter increment, event record, sampled event, histogram bucket and estimated population have different statistical meaning;
- configured feature, executed offload, capture representation and wire representation can differ;
- correlation, localization, mechanism evidence, controlled intervention and causal conclusion are different strengths;
- instrumentation allocation, ring-buffer overwrite, map eviction, event loss and consumer lag are different measurement failures;
- useful diagnostic context, personal data, secrets, payload and long-term identifiers require different handling.

## Learning Objectives

After this module, you should be able to:

1. turn a network performance or correctness symptom into a scoped measurement question and path-stage hypothesis;
2. select counters, tracepoints, histograms, dynamic probes, sampling, hardware events, packet capture and application evidence by claim;
3. correlate work across CPUs, queues, packets, aggregates, sockets and clock domains with explicit uncertainty;
4. separate on-CPU service, queue residence, wakeup delay, device work, offload and peer time;
5. design bounded low-overhead instrumentation with event-loss, privacy, version and pointer-lifetime safeguards;
6. run controlled experiments across affinity, NAPI, offloads, queue depths, routing, filters and application placement;
7. communicate findings with distributions, denominators, configuration, limitations and falsifiable causal claims.

## Core Exposition

### Begin with a falsifiable question

Write the outcome, population, time interval, namespace, interface, direction, protocol and load regime. “Why is networking slow?” is not actionable. “Why did p99 receive-to-application latency for service A exceed 2 ms on queue 3 during the 14:00 load plateau?” identifies a population and boundary.

State candidate mechanisms and disconfirming evidence. If the hypothesis is NAPI budget exhaustion, relevant observations include poll work, budget hits, rescheduling, backlog and CPU saturation. A short socket queue and long scheduler delay would redirect the investigation.

### Draw the path before instrumenting

Inventory receive descriptors, interrupts, NAPI, XDP, SKB construction, GRO, protocol processing, filters, route or local decision, socket queue, wakeup and application. For transmit, include system call, socket queue, protocol, qdisc, GSO, driver ring, DMA completion and any hardware timestamp.

Mark context, CPU, queue, ownership, clock and possible drop at each boundary. Include virtualization, tunnel and namespace layers. This map prevents a measurement at one similarly named function from being mistaken for the entire stage.

### Use counters for coarse localization

Start with interface and driver statistics, per-queue drops, NAPI polls and budget exhaustion, backlog drops, protocol errors, filter verdicts, socket drops, qdisc statistics, retransmissions and application outcomes. Compare increments over the same interval, not unrelated cumulative totals.

Know counter definitions and reset behavior. Driver-specific statistics can change by device and version. A zero counter can mean no event, unsupported collection, wrong namespace, offloaded bypass, or a read from the wrong layer.

### Prefer stable tracepoints for transitions

Tracepoints expose named events and typed fields without attaching to arbitrary instructions. Use the narrowest event set and filters needed to correlate the population. Record event format and kernel build with the result.

Tracepoint presence does not guarantee the exact semantic boundary desired. Read its contract and source when necessary. An enqueue trace can occur before admission failure or after accounting depending on the event definition.

### Use dynamic probes as a scoped fallback

Kprobes and fprobes can instrument functions lacking stable events. They depend on symbols, compiler transformations, inlining, arguments, architecture ABI and kernel version. Validate attachment and missed-hit counters on the exact build.

Never dereference an internal pointer after its protected lifetime or assume a struct offset from another kernel. Fetch only the fields needed, bound strings and packet bytes, and prefer BTF or other build-matched type information where supported.

### Sample CPU cost rather than tracing every call

Sampling profilers estimate which instructions and stacks consume on-CPU cycles without recording every packet event. Separate softirq, kthread, process, interrupt and userspace contexts. Weight samples correctly and report frequency and lost samples.

A hot stack indicates CPU service demand, not why a task waited off CPU or a packet sat in a queue. Pair it with residence measurements, scheduler events and queue occupancy when latency is the question.

### Attribute exclusive and inclusive cost

Inclusive stack cost contains callees; exclusive cost attributes the sampled instruction or frame. A protocol function can appear hot because checksum, filter or memory allocation below it dominates. Report both when drawing optimization conclusions.

Cycles, instructions, cache misses, branch misses and stalled cycles add architectural evidence. Hardware events have multiplexing, model and attribution limits, especially across interrupts and migrated work.

### Measure queue residence with paired events

Record enqueue and dequeue or completion timestamps under a stable key. The difference is residence, which includes waiting and possibly service depending on boundaries. Track queue length or bytes at enqueue to connect latency with pressure.

Pairing state is bounded by capacity and timeout. Key reuse, clones, retransmissions and drops require generation or explicit terminal events. Count unmatched starts, unmatched ends, evictions and negative intervals rather than silently discarding them.

### Choose correlation identity deliberately

An SKB pointer is unique only during object lifetime and can be reused. A five-tuple merges packets and can change through NAT. Sequence ranges work for some TCP questions but retransmit. Hardware descriptors wrap. Sampled hashes can collide.

Use a composite of stable object identity plus generation, queue index plus descriptor generation, or protocol tuple plus sequence and direction as the claim requires. Redact or hash sensitive values with a run-specific key and quantify collision risk.

### Track representation changes

GRO merges multiple received packets, GSO represents multiple future packets, fragments reassemble, clones create multiple consumers, and tunnels expose outer and inner tuples. Correlation must define whether it follows wire frame, logical packet, aggregate, byte range or flow.

Emit lineage at merge, split, clone and transform when feasible. Otherwise terminate one identity and start another with an aggregate count. Do not compute a “per-packet” denominator from mixed representations.

### Reconcile clocks before subtraction

Kernel monotonic timestamps across CPUs may be coherent on a supported platform; cycle counters or device clocks may not share epoch, rate or synchronization. Record clock name, resolution, drift and conversion.

Calibrate device and host clocks using the supported timestamping relationship and carry uncertainty. A negative cross-CPU latency is evidence of clock or correlation failure, not a faster path. Use a global trace clock for cross-event histograms where appropriate.

### Build bounded histograms in kernel

Histograms answer distributions without exporting every event. Choose units and bucket boundaries before collection. Logarithmic buckets cover wide tails; linear buckets resolve a narrow SLO boundary. Report underflow, overflow, count, sum where safe, and event loss.

Keyed histograms by CPU, queue, namespace or reason localize variation, but unbounded flow keys become a memory attack. Predeclare cardinality, use top-k or sampling, and expire state under a tested policy.

### Understand trace-buffer loss

Per-CPU ring buffers have finite capacity. Overwrite mode loses old events; stop-on-full loses later coverage. A slow reader, burst, stack capture or verbose payload increases loss. Read buffer and tool loss indicators.

Loss is not necessarily uniform: the hottest CPU can drop the most events, biasing results toward healthy paths. Report loss per CPU and rerun with narrower filters or aggregation.

### Localize drops at the earliest owner

Device statistics can show missed frames or ring errors. Driver and stack drop reasons identify later rejection. Filters, routes, protocols, sockets and qdiscs have distinct counters. Retransmission is downstream evidence of loss, not its location.

Use drop monitoring or reasoned tracepoints with sampling and rate bounds. One packet can be cloned; a dropped clone does not necessarily mean all delivery failed. Define the object and terminal outcome counted.

### Connect network work to scheduling

Socket enqueue and wakeup do not mean the application ran. Correlate task wake, runnable time, schedule-in and syscall or userspace observation. CPU saturation, priority, affinity, cgroup throttling and lock contention can dominate the tail after network processing completes.

Likewise, an application can delay receive and fill socket queues, producing upstream drops. Treat user and kernel as one causal path while keeping ownership boundaries clear.

### Account for offload observation points

A host capture before TSO can show one large packet with an incomplete checksum. The wire and receiver see segments with completed checksums. GRO can make later receive capture show aggregates. Hardware timestamp placement depends on device and direction.

Run controlled offload-on/off comparisons and capture at multiple points when wire correctness matters. Turning off offloads changes CPU, packet rate and timing, so it is an intervention, not a neutral observation.

### Profile locks and memory locality

CPU samples can reveal spin or atomic hot spots, but contention also needs waiter, owner and hold-time evidence. Per-queue locks, socket locks, qdisc locks and global tables have different domains. Attribute by call path and object class.

Measure cache misses, remote NUMA access, allocation, page-pool reuse and cross-CPU enqueue when placement is suspected. Moving work can reduce one lock and increase remote memory elsewhere.

### Control instrumentation overhead

Estimate event rate before enabling a probe. Bound maps, stacks, strings, packet snapshots and output. Filter in kernel, aggregate early, sample predictably, and move formatting and symbolization out of the hot path.

Measure baseline, instrumentation enabled without consumer, full collection and teardown at representative load. Compare throughput, latency, drops, CPU, memory and scheduling. If overhead changes the bottleneck, narrow the experiment and state that limitation.

### Preserve privacy and operational safety

Packet tuples, process identifiers, cgroup paths, payload, stack symbols and timing can reveal users or secrets. Collect only required fields, hash with run-scoped keys, restrict tracefs and output access, encrypt storage, limit retention, and audit export.

Have an automatic timeout and kill path for production tracing. Preallocate bounded buffers, avoid management-network starvation, and cleanly remove probes and maps. An abandoned probe is a production change.

### Design controlled experiments

Hold workload, offered rate, topology, kernel, firmware, application version and observer configuration constant. Change one mechanism such as RPS, coalescing, GRO, queue depth or affinity. Randomize or alternate trials to reduce time trends and warmup bias.

Use enough repetitions and report distributions, confidence or variability, not one average. Watch competing tenants and control traffic. Revert and reproduce. A change that removes the symptom without moving the measured mechanism is evidence against the hypothesis.

### Communicate causal strength honestly

Counters can localize; traces can order observed events; profiles can attribute CPU samples; experiments can support causality. State claims at the level the evidence supports. “Queue 3 budget exhaustion correlates with tail latency” is weaker than “reducing queue-3 load in randomized trials removed budget exhaustion and lowered tail latency while controls were stable.”

Record missing events, clock uncertainty, sample weights, offload view, probe version, observer overhead and alternative explanations. Reproducibility includes the instrumentation recipe and cleanup.

## Definitions and Notation

Let a correlated work item have ordered timestamps $t_0,\ldots,t_n$ in one coherent clock. Stage residence is

$$
\Delta_i=t_{i+1}-t_i,
$$

and observed end-to-end time is $T=t_n-t_0=\sum_i\Delta_i$. This equality fails when events mismatch, clocks differ, or hidden parallel branches alter identity.

Let true event population be $N$, sampled observations $n$, and inclusion probability $\pi_j>0$ for event $j$. A weighted count estimator is

$$
\widehat{N}=\sum_{j\in sample}\frac{1}{\pi_j}.
$$

Uniform sampling simplifies this; adaptive or stage-dependent sampling requires recorded weights.

For per-CPU counter $C_k(t)$ without reset or wrap in interval $[a,b]$, total increment is

$$
\Delta C=\sum_k(C_k(b)-C_k(a)).
$$

CPU hotplug, reset, width and snapshot consistency must be handled before applying the formula.

Let observed cost with instrumentation be $Y_I$ and matched baseline $Y_0$. Relative observer overhead is

$$
O_Y=\frac{Y_I-Y_0}{Y_0},
$$

with sign interpreted according to whether larger $Y$ is harmful and with trial uncertainty reported.

Let paired-state capacity be $M$, current entries $m$, and trace-buffer loss $L_c$ on CPU $c$. Valid evidence requires $m\le M$ and reporting every $L_c$, eviction and unmatched event.

## Mechanisms, Invariants, or Proof Structure

Review a profiling study with these obligations.

1. **Question obligation:** outcome, population, interval, scope, load regime, hypothesis and disconfirming evidence are stated first.
2. **Path obligation:** stage, context, CPU, queue, ownership, representation, clock and drop points are mapped.
3. **Semantic obligation:** each counter, tracepoint, probe, sample and capture field has a verified meaning on the exact build.
4. **Clock obligation:** differences use coherent clocks or calibrated conversion with quantified uncertainty.
5. **Identity obligation:** correlation survives reuse, concurrency, sampling, aggregation, segmentation, cloning and retransmission as claimed.
6. **Capacity obligation:** trace buffers, maps, histograms, stacks and outputs are bounded, and every loss indicator is collected.
7. **Attribution obligation:** CPU service, queue residence, scheduler delay, device work, drop and peer time remain distinct.
8. **Offload obligation:** observation points and logical-versus-wire representations are named and validated.
9. **Overhead obligation:** baseline and instrumented trials quantify hot-path, consumer, memory and storage effects.
10. **Safety obligation:** probes use protected data, minimum fields, privacy controls, timeouts, access restrictions and cleanup.
11. **Experiment obligation:** interventions control confounders, repeat, revert and observe affected as well as competing populations.
12. **Claim obligation:** conclusions match evidence strength and state exclusions, uncertainty, missing events and alternatives.

The evidence proof is a chain, not one graph. A population counter establishes denominator and loss. Correlated timestamps establish observed stage residence. Samples attribute CPU execution. Queue and scheduler state supply off-CPU mechanism. Capture or peer evidence resolves offload and wire behavior. A controlled intervention tests whether changing the suspected mechanism changes the outcome.

This chain remains conditional on instrument semantics, clock correctness, matching accuracy, sampling design and observer overhead. State those assumptions rather than presenting a visualization as self-validating.

## Alternatives and Trade-Offs

- **Counters versus events:** counters are cheap and aggregate; events preserve ordering and consume buffers.
- **Tracepoints versus dynamic probes:** tracepoints are more stable; probes reach missing boundaries and depend on build details.
- **Tracing versus sampling:** tracing reconstructs selected events; sampling estimates CPU cost with less event-volume dependence.
- **Per-packet correlation versus flow aggregation:** packets localize precise paths; flows bound cardinality and blur variation.
- **Pointers versus protocol keys:** pointers are cheap during lifetime; protocol keys survive layers and collide or expose data.
- **Linear versus logarithmic histograms:** linear buckets resolve narrow ranges; logarithmic buckets cover wide tails compactly.
- **Kernel aggregation versus raw export:** aggregation controls rate; raw events permit later questions and increase overhead.
- **Overwrite versus stop-on-full buffers:** overwrite preserves recent context; stop preserves early context and ends coverage.
- **Hardware timestamps versus kernel timestamps:** hardware approaches device boundaries; kernel clocks integrate software stages more easily.
- **Full stacks versus instruction samples:** stacks explain callers and cost more; instruction samples have less context.
- **Always-on metrics versus incident probes:** always-on data supplies baseline; targeted probes provide depth during a bounded interval.
- **Offloads enabled versus disabled:** enabled reflects production; disabled clarifies logical packets while changing work and timing.
- **Production canary versus lab replay:** production represents reality with risk; lab control improves isolation and may miss interactions.
- **High sampling rate versus low perturbation:** more samples reduce some variance; overhead and buffer pressure rise.
- **Rich identifiers versus privacy:** detailed keys improve correlation; minimization reduces sensitivity and cardinality.
- **Automated diagnosis versus manual synthesis:** automation scales known patterns; humans can integrate novel evidence and introduce bias.

## Failure Modes and Misconceptions

- “Start with the most powerful tracer.” Start with the narrowest instrument that tests the question.
- “Function runtime equals packet latency.” Queueing, preemption, device and application time may dominate.
- “A flame graph shows off-CPU delay.” Ordinary CPU sampling shows where execution occurred.
- “A tracepoint name defines its semantics.” Verify fields and placement on the exact kernel.
- “Dynamic function probes are stable interfaces.” Compiler and kernel changes can move or remove targets.
- “An SKB pointer is a permanent packet ID.” Objects are cloned, freed and addresses reused.
- “A five-tuple uniquely names a packet.” It names a flow view and changes through NAT or tunnels.
- “One packet remains one object.” fragments, GRO, GSO, cloning and retransmission change representation.
- “All timestamps can be subtracted.” Clock domains need coherence or calibration.
- “A negative latency is an optimization.” It usually exposes clock or correlation error.
- “No trace record means no event.” Buffers, filters or consumers may have lost it.
- “Trace loss is random.” Hot CPUs and bursts can be preferentially missing.
- “Summing counters always works.” Resets, wrap, migration and inconsistent reads can invalidate deltas.
- “Equal packets per queue means balanced work.” Bytes and protocol CPU can differ.
- “Retransmission locates a host drop.” It proves a recovery response, not the loss stage.
- “Socket enqueue means application received data.” Wakeup and scheduling remain.
- “A host capture is the wire.” TSO, checksum offload and GRO alter observation.
- “Turning off offload is only measurement.” It changes CPU, packet rate and timing.
- “Per-flow maps are bounded by traffic rate.” Attackers can maximize unique keys.
- “Symbolization is free because it is userspace.” collection and storage still compete for resources.
- “More events always improve confidence.” Biased, lossy or disruptive events can worsen evidence.
- “One before/after run proves causation.” Time trends and workload variation remain confounders.
- “Average latency describes tails.” Distributions and population counts are required.
- “Profiling data is operationally harmless.” It can contain payload, identities, topology and kernel addresses.
- “Disabling the tool cleans everything.” Probes, maps, buffers, consumers and permissions all need verified teardown.

## Worked Examples

### Example 1

Interface missed-frame counters rise before any NAPI or protocol event exists. Driver ring occupancy is high and application queues are short. The evidence localizes current loss before kernel packet construction; socket tuning cannot recover frames never received.

### Example 2

The following executable toy decomposes one correlated sample using one coherent clock. It establishes arithmetic only, not a latency distribution, clock validity, stage completeness, kernel path or cause.

<!-- bijux-verify: {"id":"network-path-latency-decomposition","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"device_to_driver=8us\ndriver_to_protocol=27us\nprotocol_to_socket=15us\nsocket_to_application=70us\ntotal=120us dominant=socket_to_application\n","stderr":""}} -->
```python
events = [
    ("device", 100),
    ("driver", 108),
    ("protocol", 135),
    ("socket", 150),
    ("application", 220),
]
deltas = []

for (left_name, left), (right_name, right) in zip(events, events[1:]):
    name = f"{left_name}_to_{right_name}"
    duration = right - left
    deltas.append((name, duration))
    print(f"{name}={duration}us")

dominant = max(deltas, key=lambda item: item[1])[0]
print(f"total={events[-1][1] - events[0][1]}us dominant={dominant}")
```

### Example 3

CPU sampling shows 35 percent of network softirq samples under a checksum routine. Hardware checksum offload is configured but final-path fallback counters rise for one tunnel. The combined evidence suggests valid software work, not necessarily a bad checksum implementation.

### Example 4

A per-packet map uses SKB addresses without generations. Under load, a freed address is reused before a late terminal event, producing a negative duration. Adding protected lifetime or a generation and timeout exposes unmatched events instead of a false latency.

### Example 5

Trace loss is 0.1 percent overall but 12 percent on CPU 7, the suspected hot queue. Aggregate completeness is misleading. Narrowing to queue 7 stage events reduces loss below the experiment threshold.

### Example 6

A pre-NIC capture shows 64 KiB TCP packets with incomplete checksums. A receiver capture shows valid MTU-sized segments. TSO and checksum offload explain the representation difference; the host capture is not evidence of malformed wire traffic.

### Example 7

Socket enqueue-to-task-wakeup is short, but wakeup-to-schedule latency dominates p99 when the application cgroup is throttled. Network stack CPU tuning would not address the current queueing mechanism.

### Example 8

An unbounded histogram keyed by source address grows during a scan and creates memory pressure. Replacing it with fixed prefix buckets, top-k tracking and a run timeout preserves the question while bounding state.

### Example 9

Enabling full function graph tracing lowers throughput 30 percent and eliminates burst loss by slowing offered work. The apparent improvement is observer effect. Filtered tracepoints and in-kernel histograms reproduce the original load.

### Example 10

Alternating trials move half of RSS buckets away from a hot CPU. Queue-3 budget exhaustion and p99 latency fall together; control queues remain stable; reverting restores both. The intervention strengthens the causal claim beyond the original correlation.

## Cross-Program Connections

- **Performance engineering:** hypotheses, sampling, percentiles, counters, profiling, controlled experiments and observer effect define method.
- **Network engineering:** packet paths, queues, offloads, retransmission, capture points and wire semantics define observations.
- **Data engineering:** event schemas, clocks, joins, sampling weights, histograms, loss and provenance determine analytic validity.
- **Statistics:** population, bias, variance, confidence, repeated trials and causal inference constrain conclusions.
- **Security engineering:** privileged probes, kernel pointers, packet data, trace access and bounded maps define exposure.
- **Platform engineering:** fleet-safe instrumentation, canaries, dashboards, incident response, rollback and retention operationalize profiling.
- **API and service engineering:** request IDs, application spans, deadlines, socket queues and user-visible latency complete the path.
- **Distributed systems:** clock domains, correlation identifiers, partial observation and asynchronous stages recur across services.
- **Computer architecture:** PMUs, cache misses, NUMA, interrupts, DMA and cycle counters explain low-level costs.
- **Reliability engineering:** baselines, fault injection, runbooks, cleanup, evidence limits and reproducibility support safe diagnosis.

## References

1. Linux Kernel Documentation, [Linux Tracing Technologies Guide](https://docs.kernel.org/trace/index.html), trace frameworks, tracepoints, function tracing, probes and analysis guidance; retrieved 2026-09-04.
2. Linux Kernel Documentation, [ftrace](https://docs.kernel.org/trace/ftrace.html), tracefs, tracers, events, ring buffers, clocks, filters and function graphs; retrieved 2026-09-04.
3. Linux Kernel Documentation, [Event Histograms](https://docs.kernel.org/trace/histogram.html), keys, values, synthetic events, inter-event latency, clocks and bounded aggregation; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Kernel Probes](https://docs.kernel.org/trace/kprobes.html), kprobe and kretprobe behavior, missed hits, architecture constraints and limitations; retrieved 2026-09-04.
5. Linux Kernel Documentation, [BPF Ring Buffer](https://docs.kernel.org/bpf/ringbuf.html), bounded event transport, ordering, reservation, submission, discard and wakeups; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Interface Statistics](https://docs.kernel.org/networking/statistics.html), standard network statistics, driver interfaces, ethtool and per-queue considerations; retrieved 2026-09-04.
7. Linux Kernel Documentation, [Devlink Trap](https://docs.kernel.org/networking/devlink/devlink-trap.html), packet traps, drop reasons, actions, metadata and statistics for offloaded data paths; retrieved 2026-09-04.
8. Linux Kernel Documentation, [NAPI](https://docs.kernel.org/networking/napi.html), polling, receive budgets, completion, threading, busy polling and queue relationships; retrieved 2026-09-04.
9. Linux Kernel Documentation, [Scaling in the Linux Networking Stack](https://docs.kernel.org/networking/scaling.html), RSS, RPS, RFS, XPS, per-CPU backlog and flow placement; retrieved 2026-09-04.
10. Linux Kernel Documentation, [`struct sk_buff`](https://docs.kernel.org/networking/skbuff.html), packet geometry, fragments, cloning, checksum and segmentation metadata affecting observation; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design a profiling plan for high receive p99 latency with normal throughput. Map stages, hypotheses, counters, traces, sampling, clocks, identity, overhead and decision criteria.

### Exercise 2

Specify a bounded cross-CPU enqueue/dequeue correlator that survives object-address reuse, event loss, timeout, CPU hotplug and trace-buffer pressure.

### Exercise 3

Diagnose apparent checksum corruption and giant packets in a host capture when checksum and segmentation offloads, GRO and a tunnel are enabled.

### Exercise 4

Design a controlled experiment to test whether RSS imbalance, RPS remote enqueue, NUMA placement or application scheduling causes one service's tail latency.

### Exercise 5

Construct a production-safe profiling and reporting standard for kernel network incidents. Include privacy, access, loss, overhead, cleanup, reproducibility and claim limits.

## Answers to the Exercises

### Answer 1

Define the outcome as receive-to-application p99 for one service, namespace, interface, flow class and load interval. Map device completion, interrupt, NAPI start/end, XDP, SKB, GRO, protocol, filter, socket enqueue, wakeup, schedule-in and userspace observation. Hypotheses include ring loss, NAPI budget, protocol CPU, socket residence and scheduler delay.

Begin with interval deltas for device, per-queue, NAPI, backlog, protocol, filter, socket and application counters. Sample CPU stacks by context. Add filtered tracepoints around the two stages still consistent with evidence. Use a generation-tagged sampled flow or protected object identity, one global coherent trace clock, and bounded in-kernel histograms. Record unmatched events and per-CPU buffer loss.

Run matched baseline and instrumented load to bound overhead. Decide in advance that a stage is implicated only if its p99 residence rises with the outcome across repetitions and an intervention changes both without moving loss elsewhere. Preserve alternative explanations and stop if trace loss or overhead exceeds thresholds.

### Answer 2

Key an entry by object address plus allocation or observation generation, or by another identifier whose uniqueness interval is proved. Store enqueue timestamp, clock ID, CPU, queue, configuration generation and expiry in a fixed-capacity map. Preallocate or enforce insertion failure without hot-path allocation.

On dequeue, require key and generation, use the same coherent clock, emit or aggregate nonnegative duration, then delete once. Terminal drop also deletes. Timeout evicts unmatched enqueue with a reason. Missing enqueue increments unmatched-end; capacity rejection and replacement have separate counters.

Use per-CPU shards for writes and a bounded merge if safe, while allowing cross-CPU lookup for dequeue. CPU hotplug drains or migrates shard state before destruction. Count ring-buffer loss per CPU, map insertion failure, eviction, collision, negative difference and consumer lag. Sample at stable flow or hash probability and record the inclusion weight.

### Answer 3

First identify capture position. A pre-NIC transmit capture can see one GSO aggregate and a partial checksum because the NIC will segment and complete it. A post-GRO receive observer can see an aggregate after the NIC delivered several frames. Tunnel offloads add inner and outer checksum and segmentation layers.

Collect SKB checksum state, checksum level, GSO type, size and segments, inner and outer header offsets, selected device features and fallback counters. Capture at a receiver or external wire point where segmentation and checksum completion have occurred. Verify which checksum a capture tool recalculates.

Run bounded paired trials with relevant offload combination disabled, recognizing that this changes CPU and packet timing. If receiver wire packets are valid and only host pre-device capture reports errors, the observation explains the symptom. If corruption persists at the receiver only with one exact tunnel feature, localize between final-path validation and device completion, then capture driver/device health and firmware generation.

### Answer 4

Hold offered flows, payloads, service version, kernel, NIC configuration and competing traffic constant. Record RSS hash and bucket distribution, per-queue packets/bytes/CPU/budget, IRQ and NAPI CPUs, RPS target and IPIs, page and socket NUMA placement, task wake-to-run latency, cgroup throttling and application CPU.

Alternate one controlled change at a time: rebalance selected RSS buckets, disable RPS for a canary queue, move memory or application workers locally, and pin or unpin the service within safe limits. Repeat and revert each intervention. Observe throughput, drops, retransmission, queue residence and p50/p99 latency for target and control services.

RSS causality gains support if bucket movement changes hot-queue service and tail while other factors remain stable. RPS causality requires remote enqueue/IPI and cache or latency changes. NUMA causality requires remote-memory evidence and response to local placement. Scheduler causality requires dominant wake-to-run delay and response to CPU or throttling changes.

### Answer 5

Require a written question, population, path map, instrument semantics, expected rate, fixed buffer/map capacity, sampling rule, clock, identity, maximum duration, abort thresholds and cleanup command. Prefer counters and stable tracepoints; justify dynamic probes against the exact kernel and type information.

Restrict tracefs, BPF and output permissions. Exclude payload by default, minimize tuples, use run-scoped keyed hashes, redact kernel addresses, encrypt storage and set deletion time. Preallocate bounded state, rate-limit exports, count loss and automatically disable on CPU, memory, latency or drop overhead.

Report repository or script version, kernel, driver, firmware, device, topology, namespaces, offloads, workload, offered rate, trial schedule, clock, buckets, sample weights, lost events, map evictions, baseline overhead and cleanup verification. Separate raw observations, derived metrics, localization, intervention and causal conclusion.

Static event contracts can still change, dynamic probes are build-specific, sampling omits unsampled work, clocks have uncertainty, correlations can collide, captures depend on offloads, and instrumentation changes the path. Finite controlled trials cannot prove every production workload. State these limits and retain enough bounded artifacts for independent reproduction.
