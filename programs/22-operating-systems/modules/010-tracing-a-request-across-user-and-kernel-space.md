---
module_id: OS-010
program: Operating Systems
level: 1
module_number: 10
title: Tracing a Request Across User and Kernel Space
status: complete
last_verified: 2026-09-04
---

# Tracing a Request Across User and Kernel Space

## One-Page Review

### Governing question

How can an investigator reconstruct one request across user code, system-call entry, kernel subsystems, scheduling, devices, interrupts, and return without mistaking incomplete observations for causality?

### Essential definitions

- A **trace event** is a timestamped observation at an instrumentation point with named fields and execution context.
- A **span** is an interval between defined start and end events; its duration is meaningful only when the endpoints refer to the same operation and clock domain.
- A **correlation key** is an identifier or tuple used to join observations believed to concern the same logical work.
- A **causal edge** states that one event enabled, submitted, woke, or otherwise preceded another by mechanism—not merely by nearby time.
- A **tracepoint** is a maintained static hook with a defined event schema; a **dynamic probe** attaches to a chosen function, instruction, or user-space offset without a permanent call site.
- **Observer effect** is behavior changed by tracing through added work, contention, buffering, stops, cache disruption, or timing.
- A **lost-event indicator** is explicit evidence that the recorded stream is incomplete; absence of an event without such accounting is ambiguous.

### Central model, mechanism, or theorem

Build a request explanation as a typed event graph:

`G = (V, E_order ∪ E_identity ∪ E_cause)`.

Vertices are observations with clock, CPU, task, process, namespace, and object context. Order edges come from a trustworthy clock and stream contract; identity edges use validated keys and generations; causal edges come from mechanisms such as submission-to-completion IDs, wakeup-to-schedule relations, or explicit context propagation. A plausible timestamp sequence is a hypothesis until these edges justify it.

### Critical invariants

- Capture starts before the request and ends after completion, with configuration, clocks, filters, buffer sizes, and loss counters recorded.
- Event schemas and symbol mappings match the exact binaries, kernel, modules, architecture, and configuration under investigation.
- Correlation keys are scoped for reuse, namespace, concurrency, and lifecycle; raw addresses and thread IDs are not assumed globally unique forever.
- Entry and exit events pair only when nesting, migration, blocking, restart, asynchronous completion, and missing events are handled.
- Time subtraction occurs only after clock domains, synchronization, resolution, and ordering guarantees are established.
- Tracing overhead, privileges, privacy exposure, and production risk are measured or bounded for the selected instrumentation.
- Conclusions separate direct observation, derived interval, causal inference, excluded alternatives, and remaining uncertainty.

### Common failures

Common mistakes are tracing only system calls and blaming the kernel for user-space queueing, assuming a long syscall spent all time on CPU, pairing events by PID after thread or identifier reuse, joining block or network requests by address alone, ignoring scheduler delay, mixing wall and monotonic clocks, treating function samples as complete execution paths, overlooking per-CPU buffer loss, enabling every event and perturbing the workload, exposing secrets in arguments, and presenting one trace as a representative distribution.

### Compact example

A thread calls `read`. A user marker identifies request 73, syscall entry confirms its boundary, a filesystem tracepoint maps it to a block request with a generation-tagged request ID, a scheduler event shows the thread sleeping, the block completion event names the same request, a wakeup event targets the same thread instance, a switch event shows when it actually ran, syscall exit reports bytes and status, and a user marker closes the operation. The investigator partitions latency into user-to-entry, kernel preparation, device wait, wakeup-to-run, return, and user handling. Missing block completion or a reported buffer overrun makes the causal path incomplete rather than proving the device stalled.

### Connections

[OS-003](003-system-calls-and-user-kernel-transitions.md) defines the syscall boundary, [OS-004](004-interrupts-and-exceptions.md) defines completion entry, and [OS-009](009-kernel-modules-and-drivers.md) defines driver ownership. [OS-017](../ROADMAP.md) develops context switching and [OS-093](../ROADMAP.md) develops eBPF observability. Distributed propagation connects to [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) and operational evidence to [Systems Engineering](../../26-systems-engineering/ROADMAP.md).

## Governing Question

A request visible in an application rarely maps to one uninterrupted kernel call. A library may buffer, batch, retry, or avoid a syscall. The kernel may validate, copy, look up state, acquire locks, enqueue work, block the task, schedule another CPU, submit to a device, receive an interrupt, run deferred completion, wake the task, and later return. Network and storage stacks can split or merge work, obscuring one-to-one identity.

Different tools observe different boundaries. A syscall tracer reveals arguments, results, signals, and time at the user-kernel ABI. Static tracepoints reveal maintained subsystem events. Function tracing and probes reveal implementation paths. Scheduler events explain runnable delay. Hardware counters sample resource behavior. User markers connect application semantics. None alone necessarily establishes end-to-end causality.

The governing question is how to choose the smallest sufficient observation set, create reliable identity and clock relationships, preserve loss and overhead evidence, reconstruct a typed path, and state conclusions at exactly the strength the data supports.

## Why This Matters

Latency is easily misattributed. A 40 ms syscall can include 30 ms asleep awaiting storage and 8 ms runnable but not scheduled, leaving little CPU execution in the named kernel function. A fast syscall may only enqueue work whose failure arrives asynchronously. A user request can wait in a runtime pool before crossing the boundary, invisible to kernel-only tracing.

Correct tracing accelerates debugging and capacity work. It can locate lock contention, scheduler delay, page faults, reclaim, queueing, device service, interrupts, retransmission, or user processing. Incorrect tracing generates confident folklore: “the filesystem is slow,” “the network dropped it,” or “the scheduler paused us” based on coincident timestamps or incomplete events.

Tracing is also a security and reliability action. Syscall arguments, paths, identifiers, packet metadata, and stack traces can reveal secrets. Attaching probes may require powerful privileges. High-rate event capture consumes CPU and memory and can change scheduling. Production evidence therefore needs data minimization, authorization, retention, integrity, and rollback.

## Prerequisites and Retrieval

Recall from [OS-003](003-system-calls-and-user-kernel-transitions.md) that library APIs, syscall wrappers, architecture entry, validation, and return are different layers. Recall from [OS-004](004-interrupts-and-exceptions.md) that interrupt work can be deferred and run on another CPU. Recall from [OS-007](007-kernel-data-structures.md) that identifiers and pointers can be reused. Recall from [OS-009](009-kernel-modules-and-drivers.md) that device ownership and completion are asynchronous.

Retrieve these distinctions:

- elapsed time is not CPU time;
- blocked is not runnable, and runnable is not executing;
- temporal adjacency is not a causal edge;
- a thread ID identifies an execution context only within a defined lifecycle and namespace;
- an address identifies storage, not necessarily the logical object generation that occupies it;
- function sampling estimates where execution occurs but does not record every call;
- tracing silence can mean no event, wrong filter, unsupported hook, disabled source, or data loss.

## Learning Objectives

After completing this module, you should be able to:

- draw the possible stages of a synchronous and asynchronous request across user and kernel space;
- select among syscall tracing, user events, tracepoints, function tracing, probes, performance events, and eBPF;
- define stable correlation keys and causal edges across task, queue, subsystem, and device transitions;
- pair entry and exit under nesting, blocking, restart, migration, and identifier reuse;
- partition latency into user, kernel execution, queue, scheduler, device, and return components;
- normalize clocks and detect buffer loss, sampling gaps, and symbol mismatches;
- design low-overhead capture with filters, triggers, aggregation, and bounded buffers;
- protect sensitive data and constrain tracing authority;
- reproduce and validate trace-derived claims with experiments and independent signals;
- identify operational or safety conclusions requiring accountable human review.

## Core Exposition

### Begin with a falsifiable question

Do not start by enabling every tracer. State the symptom, population, and competing explanations. For example: “Between client marker and response, are the 99th-percentile delays caused mainly before syscall entry, while waiting for block completion, or after wakeup while runnable?” Define the request class, time window, host, workload, and threshold.

List the minimum events that could distinguish those explanations: user start and end, syscall entry and exit, block submission and completion, scheduler sleep, wake, and switch. Add fields needed to join them. State what result would refute each hypothesis. This makes tracing an experiment rather than an unbounded log collection.

Record the exact environment before capture: kernel release and build identity, boot and tracing configuration, modules, application binary and debug identity, CPU topology and affinity, namespaces, workload, and tool versions. Dynamic implementation probes are especially sensitive to binary layout and optimization.

### Map the request path

A nominal synchronous I/O path may be:

`application → runtime/library → syscall entry → argument import → VFS → filesystem → block queue → driver → device → interrupt → completion → wakeup → syscall return → application`.

This is a map of possibilities, not a claim that every request visits every stage. Cache hits may avoid the device. Asynchronous APIs may return after submission. Read-ahead can issue unrelated I/O. One application read can split into several block requests; one device command can merge work from several callers.

Add side paths: page faults during user copy, memory allocation and reclaim, locks, throttling, cgroup policy, security hooks, network retransmission, work queues, soft interrupts, and scheduler delay. The purpose is to identify boundary events and fan-out/fan-in, not to instrument every function preemptively.

### Start at the syscall boundary

A syscall tracer such as strace observes process interactions with the Linux kernel, including system calls, signals, and state changes through ptrace. It is excellent for determining which syscalls occur, their user-visible arguments and results, and whether a call blocks or restarts. It does not by itself explain internal subsystem time.

Trace all relevant threads and descendants when the request can migrate among them. Decode file descriptors and timestamps carefully. A library call might perform several syscalls, and buffering may perform none at the moment the application operation begins. Injected tracing stops can materially perturb multithreaded or timing-sensitive work.

Syscall entry and exit tracepoints can provide lower-overhead kernel-side boundaries and integrate with other events. Pair them by thread instance and nesting state, accounting for signals, restarts, nonreturning calls, and event loss. A syscall duration is wall time between endpoints, not the amount of kernel CPU consumed.

### Add user-space semantic markers

Kernel events know tasks, descriptors, and kernel objects; they may not know that these belong to checkout 48 or query 912. Add a request identifier at user enqueue, dispatch, completion, and relevant handoffs. Linux user events can feed application-defined data into tracing infrastructure used by ftrace or perf, while uprobes can observe existing binaries when source instrumentation is unavailable.

Prefer explicit, bounded, nonsecret identifiers over payload copies. Define generation, process scope, sampling, and propagation across threads. If a runtime reuses request objects, pointer equality is insufficient. If work crosses processes, a per-process counter alone collides unless paired with process identity or a wider trace identity.

Uprobes attach to binary offsets or symbols and depend on the exact mapped object, relocation, inlining, optimization, and debug information. A missing probe hit can reflect an alternate implementation or optimized-away call. Maintained user events are more semantically stable when the application can expose them.

### Static tracepoints and dynamic probes

Static tracepoints are placed at meaningful kernel locations and expose structured fields. When disabled they are designed for low inactive overhead; when enabled, attached probes run in the caller's execution context. Event schemas should still be treated as versioned interfaces and recorded with the capture.

Use maintained subsystem tracepoints first because they express domain events such as scheduling, block issue and completion, networking, reclaim, or power transitions. They tend to survive refactoring better than function names and provide fields chosen for analysis.

Kprobes, kretprobes, fprobes, function graph tracing, and related dynamic facilities can observe implementation points not covered by tracepoints. They are powerful for a narrow hypothesis but more fragile. Inlining, tail calls, return-probe capacity, blacklisted locations, architecture details, recursion, and module unload can create misses or invalid assumptions.

Probe handlers execute under the context and constraints of the probed path. They must be bounded, reentrancy-aware, and safe for interrupt or atomic contexts. Instrumentation that allocates, locks, copies large data, or recursively triggers itself can change or destabilize the system under study.

### Scheduler state is part of latency

When a task blocks, record why and what event makes it runnable. A wakeup event means eligibility, not immediate execution. The interval from wake to scheduled execution is runnable delay; it can reflect CPU saturation, priority, affinity, throttling, interrupt load, or preemption rules.

Scheduler switch events let an analysis partition on-CPU and off-CPU intervals. State transitions must be interpreted using the kernel version's event fields. Migration means one task's events can appear in different per-CPU buffers. Merge them only with a valid common clock and ordering model.

A task can also be preempted while inside a syscall. Subtracting one broad “blocked” interval may miss multiple sleeps, runnable gaps, and CPU bursts. Construct the state timeline from switch and wake events, then intersect it with the request interval.

### Follow queue and object identity

At each asynchronous handoff, identify the outgoing work and its completion. A robust key may include device, queue, tag, generation, sector range, socket cookie, sequence, namespace, or subsystem-specific identifier. Verify whether splitting, merging, cloning, retry, remap, or batching changes cardinality.

Pointer values are weak keys. Allocators reuse addresses, and the same object can serve multiple lifecycle generations within one trace. Add creation or submission sequence and close the key when completion or release occurs. Reject ambiguous joins instead of selecting the nearest timestamp.

Fan-out produces a parent with several children; completion may require all, any, or a quorum. Fan-in combines several parents into one lower operation. Model these as graph edges rather than forcing a flat span pair. Record retry as a new attempt linked to one logical request.

### Interrupt and completion paths

Device completion may enter through a hard interrupt, poll loop, shared-vector handler, or another CPU. The top half may only acknowledge and schedule deferred work. Soft interrupt, threaded handler, tasklet, or work-queue execution can perform the actual queue completion and wakeup.

Correlate device command identity through each layer. An interrupt timestamp alone does not prove which request completed, especially with shared or batched vectors. Capture the queue completion event or a validated descriptor/tag transition. Lost interrupts, polling, and coalescing change the expected event pattern.

Measure interrupt-to-deferred-work delay separately from device service and wake-to-run delay. CPU affinity, interrupt moderation, queue depth, polling budget, and power state can shift these components without changing total device time.

### Clocks and ordering

Prefer one monotonic trace clock for all same-host events. Record the selected clock and its semantics. Per-CPU buffers may assign locally ordered timestamps, but cross-CPU ordering near equal times can be uncertain. Wall clock can jump or be disciplined and is usually inappropriate for short duration arithmetic.

Cross-host traces require explicit synchronization and uncertainty. Network time protocols provide estimates, not perfect simultaneity. Causal message identifiers can establish send-before-receive even when timestamps overlap within error bounds. Report interval uncertainty rather than manufacturing precise negative or sub-microsecond latency.

CPU frequency changes do not necessarily alter a properly chosen kernel trace clock, but counter sources and conversion can vary by platform. Validate with known paired events and document resolution. Do not mix application wall time, hardware device counters, and kernel monotonic time without measured transformations.

### Buffers, loss, and sampling

Tracing systems use bounded buffers. Under high event rate they may overwrite old data, drop new records, reserve per-CPU capacity, or throttle producers. Record buffer mode, size, per-CPU loss, overwrite markers, consumer lag, and start/stop order. An incomplete stream cannot support a complete path claim.

Filtering by PID alone can miss interrupts and workers executing on behalf of the request. Filter on stable subsystem keys where possible, use triggers to start a focused window, or aggregate in kernel space. Begin broad enough to discover handoffs, then narrow with verified correlation.

Sampling records a subset of events or execution locations. It estimates distributions under a known policy; it cannot prove that an unsampled event never occurred. Periodic sampling can alias with periodic workloads. Randomization, adequate sample counts, and repeated runs improve inference.

### eBPF and in-kernel aggregation

eBPF tracing programs can attach to tracepoints, probes, and other hooks; maintain maps keyed by request or task; calculate durations; filter early; and send bounded results to user space. The verifier checks program properties required for safe admission under its model, not the correctness of the tracing hypothesis or field semantics.

Bound map cardinality and define eviction, timeout, and identifier reuse. If an exit event is lost or never occurs, an entry map can leak state and later collide. Include generation, start time, or explicit cleanup. Per-CPU maps reduce contention but require careful aggregation.

Ring buffers preserve records only within capacity and consumption behavior. Reservation, submission, discard, wakeup, and dropped-event accounting are part of the evidence pipeline. Emitting raw every-event data can cost more than aggregating a histogram or retaining only threshold outliers.

### Reconstruct and test the graph

Normalize records into a schema with source, event name, timestamp, clock, CPU, task identity, process identity, namespace, correlation fields, payload version, and loss context. Preserve raw capture and transformation provenance. Resolve symbols against exact build IDs and module load ranges.

Construct identity edges only when scope and generation make the join unique. Construct causal edges from explicit mechanisms. Enforce local state machines: submit precedes completion, sleep precedes matching wake, wake precedes run, syscall entry precedes its exit. Flag or quarantine violations rather than silently sorting them away.

Partition latency with nonoverlapping intervals where possible. CPU execution, blocked wait, runnable delay, device service, and user queueing can overlap across children, so their sum may exceed wall time unless defined as a critical path. Name whether a metric is exclusive duration, inclusive duration, count, or sampled attribution.

Test the explanation. Change one suspected cause—queue depth, CPU affinity, device load, cache state, tracing filter—and predict which interval should move. Compare with independent counters or logs. Repeat enough requests to characterize distribution and show whether the traced example is typical or an outlier.

### Security, privacy, and operational control

Tracing kernel and other-process behavior requires strong authority because it can reveal arguments, memory, paths, addresses, credentials, timing, and cross-tenant activity. Apply least privilege, target filters, redaction, data classification, retention limits, encrypted transport and storage, and access audit.

Do not attach writable or behavior-changing probes when observation is the goal. Verify tool options that can inject failures, alter return values, or write memory. Production procedures need approval, duration and overhead bounds, automatic shutdown, rollback, and a stop condition if loss or latency rises.

Treat trace output as sensitive evidence. Hashing an identifier may still permit correlation or dictionary recovery. Raw kernel addresses undermine layout protections. Sanitizing after collection may be too late if the capture channel or storage is exposed.

## Definitions and Notation

For request `r`, let ordered boundary timestamps be `t_0, t_1, ..., t_n` in one validated clock domain. Segment duration is

`d_i = t_(i+1) - t_i`, with `d_i ≥ 0`,

and end-to-end duration is `D(r) = t_n - t_0`. If the segments form a nonoverlapping complete partition, `D(r) = sum(d_i)`. For overlapping child work, inclusive durations do not satisfy this equality; use union time or a critical path.

Let an event be `v = (source, kind, time, cpu, task, key, generation, fields)`. An identity join `v ~ w` is admissible only when their key scope and generation identify the same live operation. Timestamp closeness alone does not define `~`.

Let `v → w` denote a causal edge supported by a mechanism: program order within one execution context, explicit enqueue/dequeue identity, submit/completion identity, wake target, parent-child propagation, or a documented synchronization relation. A path explanation requires connected causal edges; sorted events provide only candidate order.

For task state within request interval `I_r`, define disjoint sets `C_r` for on-CPU, `B_r` for blocked, and `R_r` for runnable but not executing. When the state reconstruction is complete, `I_r = C_r ∪ B_r ∪ R_r` and the sets are pairwise disjoint. Missing scheduler events invalidate the partition.

## Mechanisms, Invariants, or Proof Structure

Review a cross-boundary trace through eight obligations.

**Question integrity.** The symptom, request population, hypotheses, refutations, metric, and acceptable uncertainty are fixed before interpreting the trace.

**Instrumentation integrity.** Hook semantics, schemas, binary identities, filters, privileges, context, and version compatibility match the target.

**Identity integrity.** Task, process, queue, object, device, and logical request keys include sufficient scope and generation for reuse and fan-out.

**Temporal integrity.** Clock sources, cross-CPU or cross-host transformations, resolution, and error bounds justify each subtraction and order claim.

**Causal integrity.** Each path edge comes from program order, synchronization, submission, completion, wakeup, or explicit propagation rather than timestamp adjacency.

**Completeness integrity.** Start and stop windows, event loss, overwrite, sampling, unsupported paths, and missing endpoints are recorded and constrain conclusions.

**Perturbation integrity.** CPU, memory, lock, stop, buffer, cache, and scheduling effects of observation are bounded against the phenomenon.

**Evidence integrity.** Raw capture, transformation, graph rules, outlier selection, repetitions, independent signals, privacy controls, and human interpretation are auditable.

The executable model below partitions a single synthetic request into adjacent intervals and checks that they sum to end-to-end latency.

<!-- bijux-verify: {"id":"toy-request-partition","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"total=27\nuser-to-entry=2\nkernel-before-wait=6\nwait-to-irq=12\nirq-to-wake=2\nwake-to-return=3\nreturn-to-user=2\nsum=27\n","stderr":""}} -->
```python
events = [
    ("user-start", 0),
    ("sys-enter", 2),
    ("sleep", 8),
    ("irq", 20),
    ("wake", 22),
    ("sys-exit", 25),
    ("user-end", 27),
]
labels = [
    "user-to-entry",
    "kernel-before-wait",
    "wait-to-irq",
    "irq-to-wake",
    "wake-to-return",
    "return-to-user",
]
durations = []
for index, label in enumerate(labels):
    duration = events[index + 1][1] - events[index][1]
    assert duration >= 0
    durations.append(duration)

total = events[-1][1] - events[0][1]
print(f"total={total}")
for label, duration in zip(labels, durations):
    print(f"{label}={duration}")
print(f"sum={sum(durations)}")
assert sum(durations) == total
```

Passing proves arithmetic only for one complete, ordered, nonoverlapping synthetic sequence. It does not establish event identity, clock validity, causality, trace completeness, scheduler state, device service, observer overhead, or a production diagnosis.

## Alternatives and Trade-Offs

**Syscall tracing versus kernel events.** Syscall tracing exposes the stable process boundary and decoded results but can perturb tasks and hides internal causes. Kernel events offer subsystem detail but require more correlation and privilege.

**Static tracepoints versus dynamic probes.** Tracepoints provide maintained semantic hooks and schemas. Dynamic probes reach missing locations but depend on exact implementation, symbols, optimization, and safe attachment.

**Raw events versus in-kernel aggregation.** Raw streams preserve detail for new questions but consume bandwidth and sensitive storage. Aggregation reduces cost and exposure but discards dimensions chosen too early.

**Complete capture versus sampling.** Complete capture supports per-request reconstruction when capacity holds. Sampling scales to high rates and distributions but cannot prove individual absence or exact paths.

**Global buffers versus per-CPU buffers.** Global order simplifies reconstruction but contends. Per-CPU buffers scale and preserve local order while requiring clock-aware merging and migration handling.

**Explicit markers versus inferred correlation.** Explicit request propagation creates strong joins but changes application code and data contracts. Inference works on existing systems but carries ambiguity and reuse risk.

**Always-on telemetry versus triggered tracing.** Always-on signals catch precursors but must be cheap and sparse. Triggered detail reduces normal overhead but can miss onset and needs a reliable trigger and prehistory.

## Failure Modes and Misconceptions

1. **“One application call equals one syscall.”** Libraries can buffer, batch, retry, split, or avoid calls.
2. **“Syscall duration is kernel CPU time.”** It includes blocked, runnable, preempted, and interrupt intervals.
3. **“Nearby timestamps prove causality.”** A mechanism or validated identity must connect events.
4. **“PID is a permanent request key.”** Threads serve many requests, identifiers reuse, and namespaces alter scope.
5. **“A pointer uniquely identifies an object.”** Storage can be reused for another generation during the capture.
6. **“Wakeup means the task ran.”** It only makes the task eligible; scheduling can occur later.
7. **“An interrupt proves request completion.”** Shared, coalesced, spurious, and deferred paths require command identity.
8. **“Sorted per-CPU traces give exact global order.”** Clock and merge uncertainty remain, especially for near-simultaneous events.
9. **“No event means nothing happened.”** Filters, disabled hooks, sampling, buffer loss, and unsupported paths are alternatives.
10. **“Function samples reconstruct every call.”** Sampling estimates a distribution and misses unsampled executions.
11. **“The verifier proves an eBPF diagnosis.”** It checks program admissibility properties, not hypothesis semantics.
12. **“More events always improve evidence.”** Overload, loss, observer effect, and analytical ambiguity can worsen it.
13. **“One slow trace explains the percentile.”** The example may be atypical or selected after observing the outcome.
14. **“Read-only tracing is harmless.”** It can expose secrets, require broad authority, and materially change timing.

## Worked Examples

### Example 1

**Question:** A `read` takes 20 ms in a syscall trace. Did the filesystem execute for 20 ms?

**Reasoning:** The thread may sleep for I/O, wait runnable, incur a page fault, or be preempted. Entry and exit bound elapsed time only.

**Conclusion:** Add scheduler and relevant subsystem events before attributing the interval.

### Example 2

**Question:** A user marker is emitted 8 ms before syscall entry. Where does that time belong?

**Reasoning:** It precedes the kernel boundary and may reflect runtime queueing, locks, CPU scheduling, or library work.

**Conclusion:** End-to-end analysis needs user events as well as kernel tracing.

### Example 3

**Question:** The closest block completion follows a thread's read by 3 ms. Is it the read's device operation?

**Reasoning:** Other requests may be in flight, and splitting, merging, cache hits, or readahead break proximity-based pairing.

**Conclusion:** Join through documented submission and completion identity, or label the association ambiguous.

### Example 4

**Question:** A task is woken at time 10 but switches onto a CPU at time 14. What is the four-unit interval?

**Reasoning:** It is runnable delay if scheduler events are complete and task identity is valid, not device service.

**Conclusion:** Separate wakeup from execution when partitioning latency.

### Example 5

**Question:** A return probe records fewer exits than entries. Must the function be hanging?

**Reasoning:** Calls may not return normally, probe capacity may be exhausted, the function may be inlined or optimized, or records may be lost.

**Conclusion:** Check probe semantics and missed-event counters before inferring stuck execution.

### Example 6

**Question:** An eBPF map keyed only by thread ID retains entry timestamps. What error appears after a missing exit?

**Reasoning:** Later work on that thread can overwrite or consume stale state and produce a false duration.

**Conclusion:** Add operation generation and timeout cleanup, and count unmatched entries and exits.

### Example 7

**Question:** Per-CPU records show completion at 100.001 and submission at 100.002. Did time run backward?

**Reasoning:** Cross-CPU clocks, conversion, resolution, merge order, or different requests may explain the inversion.

**Conclusion:** Validate identity and clock uncertainty before duration arithmetic.

### Example 8

**Question:** Enabling all function events makes the latency spike disappear. Was the bug fixed?

**Reasoning:** Instrumentation can serialize execution, change scheduling, overflow buffers, and alter race timing.

**Conclusion:** Measure observer effect and prefer hypothesis-specific static events or aggregation.

### Example 9

**Question:** A trace contains no loss marker. Is it complete?

**Reasoning:** The chosen facility may overwrite silently under its mode, filters may exclude handoffs, and capture may start late.

**Conclusion:** Completeness requires an explicit pipeline argument, not merely absence of a warning.

### Example 10

**Question:** A traced control request meets its deadline in 10,000 laboratory runs. Is a safety bound established?

**Reasoning:** Instrumentation, workload, hardware states, faults, rare interference, clock validity, and worst-case reasoning remain incomplete.

**Conclusion:** Named real-time, safety, instrumentation, and system owners must assess the evidence and residual risk; this module claims no certification.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies happens-before, synchronization, task state, and queue semantics used to infer causal edges. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains counters, clocks, interrupts, caches, DMA, and performance-monitoring hardware.

[Data Engineering](../../19-data-engineering/ROADMAP.md) contributes schema evolution, stream processing, joins, late data, loss, lineage, and reproducible transformations. Trace reconstruction is a data pipeline whose records require the same discipline. [Security Engineering](../../25-security-engineering/ROADMAP.md) covers observability privilege, sensitive payloads, pointer disclosure, audit, and evidence integrity.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames observability as partial evidence in a causal and assurance argument. Successors [OS-017](../ROADMAP.md), [OS-066](../ROADMAP.md), [OS-090](../ROADMAP.md), and [OS-093](../ROADMAP.md) deepen context switching, interrupt-driven I/O, performance counters, and eBPF observability.

## References

- strace project, [strace: Linux syscall tracer](https://strace.io/), current page checked 2026-09-04. Official description of tracing process-kernel interactions through system calls, signals, and process state.
- Linux man-pages project, [syscall(2)](https://man7.org/linux/man-pages/man2/syscall.2.html), current page checked 2026-09-04. Architecture-specific syscall calling conventions and wrapper distinctions.
- Linux Kernel documentation, [ftrace: Function Tracer](https://docs.kernel.org/trace/ftrace.html), current page checked 2026-09-04. Tracefs controls, tracers, buffers, clocks, events, filtering, instances, and function graphs.
- Linux Kernel documentation, [Using the Linux Kernel Tracepoints](https://docs.kernel.org/trace/tracepoints.html), current page checked 2026-09-04. Static hooks, schemas, caller context, enablement, registration, and synchronization.
- Linux Kernel documentation, [Notes on Analysing Behaviour Using Events and Tracepoints](https://docs.kernel.org/trace/tracepoint-analysis.html), current page checked 2026-09-04. Event discovery, recording, filtering, reporting, and analysis cautions.
- Linux Kernel documentation, [Kernel Probes](https://docs.kernel.org/trace/kprobes.html), current page checked 2026-09-04. Dynamic entry and return probes, missed instances, optimization, architecture limits, and probe context.
- Linux Kernel documentation, [Uprobe-tracer](https://docs.kernel.org/trace/uprobetracer.html), current page checked 2026-09-04. User-binary offset probes, return probes, fetch arguments, event enabling, and profiling.
- Linux Kernel documentation, [user_events: User-based Event Tracing](https://docs.kernel.org/trace/user_events.html), current page checked 2026-09-04. Application event registration, enabled-state checks, data writing, permissions, and integration with ftrace and perf.
- Linux Kernel documentation, [Event Histograms](https://docs.kernel.org/trace/histogram.html), current page checked 2026-09-04. Keys, values, timestamps, synthetic events, inter-event matching, latency calculation, and dropped entries.
- Linux Kernel documentation, [BPF ring buffer](https://docs.kernel.org/bpf/ringbuf.html), current page checked 2026-09-04. Multi-CPU event ordering goals, bounded buffers, reservation, submission, discard, wakeup, and query semantics.
- Linux man-pages project, [perf_event_open(2)](https://man7.org/linux/man-pages/man2/perf_event_open.2.html), current page checked 2026-09-04. Counting and sampling events, grouping, tracepoint integration, records, loss, filtering, and permissions.
- Linux Kernel documentation, [eBPF verifier](https://docs.kernel.org/bpf/verifier.html), current page checked 2026-09-04. Control-flow and state analysis, register and pointer tracking, helper constraints, and program admission scope.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. A compact request path across syscall entry, file and pipe operations, sleep and wakeup, disk descriptors, interrupts, and return.

## Exercises

### Exercise 1

Design the minimal trace plan for a slow cached-file read. Distinguish user queueing, syscall processing, page fault, filesystem cache hit, lock wait, blocked time, runnable delay, and user handling. State hooks, keys, clocks, loss checks, and refuting observations.

### Exercise 2

Given a storage path that splits one logical request into three block requests and retries one child, define the event graph, identities, generations, parent-child edges, completion rule, and critical-path calculation.

### Exercise 3

Design an eBPF-based latency aggregator for syscall entry and exit that remains correct under nested work, missing exits, thread-ID reuse, map pressure, event loss, and process termination. State what the verifier does and does not prove.

### Exercise 4

Compare syscall tracing, user events, static tracepoints, kprobes, uprobes, function graphs, performance sampling, and hardware counters for diagnosing a 99.9th-percentile service stall. Define a staged escalation with overhead and privacy gates.

### Exercise 5

Construct an assurance review for tracing a safety-critical control request across two hosts and a device. Cover clocks, causal identity, capture loss, perturbation, hardware counters, rare states, privacy, reproducibility, and named human judgment.

## Answers to the Exercises

### Answer 1

Emit a sampled request ID at application enqueue, syscall dispatch, and user completion. Record syscall entry and exit for the target thread instances; file and fault events that distinguish cached lookup from page fault; lock or contention events only if the first capture suggests them; and scheduler wake and switch events for task state. A cached path should have no causally linked block submission. Use file identity with mount or namespace and generation rather than pathname alone.

Use one monotonic trace clock, include CPU and task lifecycle, size buffers for the filtered rate, and record per-source loss and start order. User-dispatch-to-entry measures pre-kernel time; entry-to-exit is partitioned with on-CPU, blocked, and runnable intervals; exit-to-user-completion measures return-side work. A linked block issue refutes a pure cache-hit explanation; no page-fault event refutes a fault hypothesis only if that hook and capture are verified complete. Repeat across the latency distribution and compare tracing-off behavior.

### Answer 2

Give logical request `R` a nonreused trace generation. Each child receives `(R, child_index, attempt)` and a subsystem key containing device, queue, tag, and generation. Add causal edges from `R` dispatch to each child submission, from each submission to its uniquely matching completion or retry decision, and from failed attempt to next attempt. Do not overwrite the failed child node; retry is a new attempt preserving history.

Define parent completion as all three logical children having one terminal successful or policy-accepted result. Inclusive child durations can overlap and must not be summed as wall time. The device critical path is the longest causally connected chain from first required child submission through retries to the last required child completion, adjusted for dependencies rather than simply taking maximum independent duration. Missing or ambiguous child events make the parent path incomplete and must be reported.

### Answer 3

Key entries by a stable task identity plus syscall nesting or operation generation, not numeric TID alone. Store syscall number, monotonic start, process identity, and generation. On exit, validate the matching entry, calculate a nonnegative duration, aggregate into bounded histograms, then retire state. Track unmatched entries and exits. Use bounded map capacity with explicit eviction counts and terminate-state cleanup; expire entries older than a justified maximum and count them rather than reusing silently.

Handle restarted syscalls according to the selected tracepoint semantics and exclude nonreturning operations from paired-duration claims. Per-CPU aggregation reduces contention but needs a defined merge. Measure attach and map overhead, capture tool and kernel identities, and compare against an independent counter. The verifier can establish admissible control flow, pointer use, helper calls, and bounded execution under its model. It does not prove key uniqueness, event completeness, clock meaning, syscall semantics, low observer effect, privacy, or causal correctness.

### Answer 4

Begin with existing service metrics and sparse user markers to identify the affected operation and whether delay precedes syscall entry. Add filtered syscall tracing or syscall tracepoints for boundary, result, restart, and thread behavior. Add maintained scheduler and relevant subsystem tracepoints to partition blocked, runnable, queue, and completion intervals. Use event histograms or eBPF aggregation before emitting raw high-rate records.

Use uprobes when unmodifiable user binaries hide a critical boundary and kprobes or function graphs only when maintained events cannot test a narrow implementation hypothesis. Confirm exact symbols, missed-probe counts, and overhead. Use performance samples and hardware counters to characterize CPU hotspots, cache behavior, and contention statistically rather than reconstruct individual calls. At each stage check rate, loss, latency perturbation, permissions, sensitive fields, retention, and stop conditions. Reproduce with less intrusive evidence after localization.

### Answer 5

Assign an end-to-end command identity with generation and cryptographic or integrity protection appropriate to the threat model. Propagate it through both host applications, transport messages, kernel submissions, device commands, acknowledgements, and actuation. Establish causal send/receive and submit/complete edges from protocol identities. Measure each host's monotonic clock, cross-host synchronization offset and uncertainty, and device-counter transformation; avoid ordering claims within the combined error bound.

Prove capture windows surround the command, size buffers under worst traced rate, count loss at every stage, and preserve raw signed provenance and transformation versions. Measure instrumentation-on versus off timing, CPU, buffer, and network overhead under peak interference. Exercise packet loss, retry, clock adjustment, CPU migration, queue saturation, interrupt delay, device reset, stale completion, power transitions, and observation failure on deployed hardware. A named real-time specialist, tracing owner, device engineer, security and privacy reviewer, safety authority, independent verifier, and acceptance owner must review representativeness, uncertainty, excluded paths, and residual risk. This chapter and synthetic partition claim no certification.
