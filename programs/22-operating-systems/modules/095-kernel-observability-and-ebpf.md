---
module_id: OS-095
program: Operating Systems
level: 2
module_number: 95
title: Kernel Observability and eBPF
status: complete
last_verified: 2026-09-04
---

# Kernel Observability and eBPF

## One-Page Review

### Governing question

How can an operator observe kernel behavior with bounded risk and overhead, use eBPF safely across kernel versions, and turn partial event streams into claims whose scope, loss and uncertainty are explicit?

### Essential definitions

- **observability** is the ability to infer selected internal behavior from exposed state, counters, events and samples under stated assumptions.
- A **tracepoint** is a maintained static hook with a declared event schema and execution location.
- A **dynamic probe** attaches to an implementation location such as a function entry, return or instruction without a permanent semantic hook.
- A **performance event** counts or samples software or hardware activity under a configured scope, period and privilege policy.
- An **eBPF program** is kernel-admitted bytecode associated with a program type, context, helper set and attachment mechanism.
- The **eBPF verifier** symbolically explores program states to establish required admission properties such as initialized reads, bounded accesses and permitted helper use under the kernel's model.
- A **BPF map** is kernel-managed state shared among BPF programs or between kernel and user space, with type-specific concurrency, capacity and lifetime semantics.
- **BTF** is type and source metadata used by BPF tooling and the kernel; **CO-RE** uses BTF-guided relocations to adapt supported field and type references to a target kernel.

### Central model, mechanism, or theorem

An observation is a pipeline, not a direct copy of reality:

`phenomenon -> hook -> admitted program -> filter/sample -> state or record -> buffer -> reader -> decoder -> retained evidence -> inference`.

Each edge has scope, semantics, capacity, timing, failure and privilege. The verifier checks whether a program is admissible for its declared context; it does not prove that the chosen hook denotes the intended phenomenon, keys remain unique, events are complete, clocks are comparable, maps never evict, records arrive, decoding matches the build, overhead is negligible, data is private, or the final diagnosis is causal.

### Critical invariants

- Every metric or event names its source boundary, population, unit, clock, identity and kernel/tool build.
- Static tracepoints are preferred for maintained semantics; dynamic probes are tied to exact code and verified attachment.
- Loaded bytecode, BTF, relocations, program type, helpers, maps and attachment state match the reviewed artifact.
- Map capacity, key lifecycle, update atomicity, eviction and per-CPU merge behavior are explicit.
- Produced, dropped, overwritten, delivered, decoded and retained records are counted separately.
- Collection overhead, rate and sensitive fields remain within predeclared budgets and stop conditions.
- Absence of an observation is not treated as absence of the phenomenon unless coverage and loss justify it.

### Common failures

Frequent failures are attaching to an inlined function, treating a return probe as complete, reading a field with mismatched layout, believing CO-RE preserves semantics, keying long-lived state only by reused PID, leaking entries on missing exits, overflowing histograms, filling maps with attacker-controlled cardinality, ignoring per-CPU merge races, losing ring-buffer records, mixing clocks, tracing secrets, leaving pinned objects after the loader exits, enabling excessive privilege, and calling a verifier-accepted program a correct diagnosis.

### Compact example

A team investigates request-tail latency. A user marker carries a generation-tagged request ID. Stable scheduler and block tracepoints mark enqueue, switch, issue and completion boundaries. A BPF program filters to one service, keeps bounded per-CPU histograms, and emits only anomalies through a sized ring buffer. The loader verifies target BTF and CO-RE relocation results, attaches through owned links, records map limits and cleans up on rollback. User space records buffer loss, unmatched starts, evictions, CPU coverage and clock configuration. An independent application timer and device counter cross-check the finding before a scheduling delay is called causal.

### Connections

Kernel observability connects tracing, performance analysis, verifier design, type metadata, concurrency, streaming systems, security policy, privacy, incident response and experimental method.

## Governing Question

Kernel behavior is concurrent, short-lived and distributed across system calls, interrupts, work queues, schedulers, memory management, filesystems, networking and devices. Logs often describe only failures chosen in advance. A useful diagnosis needs evidence at the boundary where a hypothesis makes a different prediction.

Instrumentation also changes the system. A probe executes in a kernel context, consumes CPU, touches caches, contends on state and can generate more data than readers sustain. eBPF makes programmable filtering and aggregation available near events, but introduces a loader, bytecode, verifier, JIT or interpreter, maps, helpers, attachment links, type metadata and a privileged lifecycle.

The governing question is therefore both epistemic and operational: what exactly was observed, what could have been missed, and what new risk did observation introduce?

## Why This Matters

Without kernel evidence, teams often attribute latency to storage when tasks were runnable, blame the scheduler for lock contention, count aggregates as wire packets, or optimize CPU hot spots unrelated to end-to-end delay. Carefully selected counters and events partition the path and falsify alternatives.

Unsafe observability can become an outage or security incident. High-rate raw tracing can exhaust memory or I/O. Dynamic probes can depend on unstable layouts. Maps can retain cross-tenant identifiers. Debug privileges can expose kernel pointers, payloads or another process's activity. A persistent BPF link can outlive the process thought to own it.

The evidence can also mislead while remaining technically correct. Sampling changes denominators. Ring buffers drop bursts. Per-CPU counters are merged at different instants. A tracepoint reports a queue transition, not business completion. A flame graph describes sampled on-CPU stacks, not all wall time. Observability engineering must preserve these distinctions.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace system calls, interrupts, scheduler transitions and asynchronous I/O;
- distinguish counters, event traces, samples, profiles and logs;
- reason about finite queues, sampling bias, clock domains and identifier reuse;
- explain kernel/user privilege and the lifecycle of file descriptors and pinned objects;
- distinguish program safety, semantic correctness and causal inference.

Retrieve the exact kernel build and configuration; boot parameters; tracepoint formats; function symbols and compiler output; BPF program, map and link inventory; bytecode and translated/JITed form; verifier log; program type and expected attach type; BTF identity; CO-RE relocation results; helper and kfunc availability; map type, flags, sizes and occupancy; ring/perf-buffer capacities; loss and overwrite counters; sampling policy; trace clock; CPU and namespace coverage; loader/tool versions; credentials and capabilities; pinned paths; retention policy; overhead experiment; raw evidence checksum; and teardown result.

## Learning Objectives

After completing this module, you should be able to:

1. choose counters, tracepoints, function tracing, dynamic probes, performance samples or eBPF by governing question;
2. state the semantic and execution-context contract of an observation hook;
3. explain the eBPF load, verify, attach, execute, detach and object-lifetime sequence;
4. scope verifier guarantees for registers, pointers, stack state, branches and helpers;
5. design bounded maps, keys, aggregation and transport with explicit loss accounting;
6. use BTF and CO-RE without assuming semantic compatibility;
7. govern privileges, sensitive data, overhead and persistent objects;
8. validate a kernel observation with independent evidence and reproducible artifacts.

## Core Exposition

### Start with a falsifiable question

Write the competing mechanisms before choosing a tool. “Why is the service slow?” is too broad. “Does the 99.9th-percentile delay accrue while the thread is runnable but not executing, rather than waiting for block completion?” identifies scheduler and block boundaries and predicts different evidence.

Name the population, interval, units, workload, configuration and decision. Collection that cannot change a decision is likely unnecessary risk.

### Build a boundary map

Draw user enqueue, syscall entry, subsystem admission, queueing, device issue, completion interrupt, wakeup, runnable state, actual scheduling, syscall exit and user completion as separate boundaries. Not every request crosses every boundary, and one logical request may fan out into many kernel objects.

Choose the smallest set of observations that distinguishes hypotheses. Begin with existing counters, then stable events, then narrow dynamic probes. High-resolution raw tracing is an escalation, not a default.

### Distinguish counters, events and samples

A counter accumulates occurrences or quantities but loses order and individual identity. An event records a selected occurrence and fields at a point. A sample records activity chosen by time, count or another trigger and estimates a larger population.

Rates require interval deltas and known resets. Traces require loss and correlation handling. Samples require probability, period, multiplexing and bias. Do not compare their values as though they had the same denominator.

### Prefer maintained tracepoints

Tracepoints are placed at domain-relevant kernel locations and expose structured fields. When enabled, attached callbacks run in the caller's context. Their schemas and placement can still change, so capture the exact event format and kernel build.

A tracepoint named “complete” may mean a kernel object completed, not that data reached durable media or an application consumed it. Read its definition and subsystem path.

### Use function tracing for implementation paths

ftrace can record function entry and, with appropriate tracers, call relationships or durations. Filters and instances narrow scope. Function graphs expose implementation behavior but inherit recursion, clock, tail-call, inlining and instrumentation constraints.

The duration between entry and return is elapsed time in that context, not automatically CPU service. Nested interrupts, preemption and blocking need separate interpretation.

### Use dynamic probes for narrow gaps

Kprobes, kretprobes, fprobes and related mechanisms reach implementation points without permanent tracepoints. Uprobes reach user binaries. They depend on exact symbols, instruction placement, calling convention, optimization and object lifetime.

Return probes can miss instances when capacity is exhausted or when control never returns normally. Inlined or optimized functions may have no intended site. Validate actual attachments and missed-hit counters.

### Use performance events statistically

`perf_event_open` can count or sample hardware and software events under task, CPU, cgroup or system scope. Groups seek coordinated scheduling; multiplexing scales counts when hardware slots are insufficient. Sampling records can be lost when buffers overflow.

Hardware event meanings and support are processor-specific. A sampled stack distribution estimates execution under its sampling rule; it does not reconstruct every call or blocked interval.

### Understand the eBPF lifecycle

A loader opens an object, resolves maps and relocations, creates kernel objects, requests program load, receives verifier success or failure, initializes state, attaches programs, consumes outputs, and eventually detaches and releases or unpins objects. Each step can partially succeed.

Own file descriptors and links explicitly. On rollback, detach new links before discarding control state. Inventory pinned maps, programs and links because filesystem pinning can intentionally extend kernel-object lifetime beyond the loader.

### Bind program type to context

Program type and expected attachment determine context layout, permissible return values, helpers, kfuncs and operational effect. A tracing program, socket filter, cgroup policy, LSM hook and XDP program do not share one authority model.

Validate the requested and actual attach target. A program safe for one context cannot be transplanted merely because the bytecode loads elsewhere.

### Scope the verifier result

The verifier analyzes control flow and abstract register, stack and pointer states. It checks initialized use, bounded and aligned accesses under known pointer types, legal helpers and other program-type rules. State pruning avoids exploring equivalent continuations repeatedly.

Acceptance means the kernel established its required program properties under that verifier version and configuration. It does not validate the source, intent, event semantics, map key, statistical estimator, privacy policy or operational usefulness.

### Treat pointers as typed capabilities

Verifier pointer types distinguish contexts, map values, stack, packets and other kernel-managed regions. Arithmetic can lose type information. Null checks can refine a nullable map-value result. Direct packet access needs bounds proved against the valid end.

Helpers can invalidate pointers or change packet layout. Re-establish required bounds after such operations. Never generalize one helper's lifetime and locking contract to another.

### Bound control-flow complexity

Loops, callbacks, subprograms and iterators are accepted only when the verifier can establish their safety within implementation limits and contracts. A source-level small loop can generate a large state space when bounds or branches are imprecise.

Verifier rejection is not proof that a program would execute unsafely; acceptance is not a performance bound. Simplify state, narrow scalar ranges and choose appropriate helpers without weakening semantics.

### Treat helpers and kfuncs as privileged APIs

Helpers expose operations specific to program types. Kfuncs expose declared kernel functions under BTF and verifier rules. Argument validation establishes the documented calling contract; it does not prove the called functionality fits the deployment's security policy.

Record helper and kfunc dependencies and target-kernel support. A feature probe should fail explicitly rather than silently omit essential evidence.

### Understand execution mode

Accepted bytecode may run through an interpreter or JIT depending on architecture and policy. JIT compilation changes native code, hardening options, diagnostics and attack surface. Capture translated or JITed output when required for review.

Do not assume identical overhead or behavior across modes. Verify active configuration and test on the production architecture.

### Choose maps by semantics

Hash, array, per-CPU, LRU, queue, stack, ring and specialized maps have distinct allocation, update, iteration, eviction and concurrency behavior. Choose from the state transition, not popularity.

Declare key and value schemas, maximum entries, flags, memory budget, full-map response and teardown. Map creation success does not ensure future inserts succeed.

### Design keys for identity lifetime

PID or TID values are reused. Pointers are unstable and may leak addresses. File descriptors are process-relative. Long-lived correlation needs a generation, start time, cookie or domain-specific identifier whose creation and retirement are defined.

Missing terminal events leak start entries and later reuse creates false duration. Bound age, delete on every outcome where observable, and count unmatched starts and exits.

### Merge per-CPU state carefully

Per-CPU maps reduce contention but create multiple snapshots. Reading CPUs sequentially does not produce one atomic global instant. CPU hotplug and reset add lifecycle concerns.

For rates, take per-CPU deltas across defined intervals before summing when semantics require it. For histograms, ensure every bucket uses the same boundaries and sufficient counter width.

### Bound cardinality

Keys derived from addresses, flows, paths, cgroups or attacker-controlled labels can exhaust a map. LRU eviction bounds memory but silently removes state needed for pairing or rare-event analysis unless counted.

Prefer bounded dimensions and in-kernel histograms. Rate-limit anomaly records. Reject designs whose maximum memory or per-event work cannot be calculated.

### Use transport buffers deliberately

BPF ring buffers and perf-event buffers move records to user space with different ordering and topology properties. Reservation can fail. Submission and discard have defined lifecycle. A slow reader, large record or burst causes loss.

Instrument reservation failures and reader-side loss indicators. Choose overwrite versus discard behavior consciously. Delivered records are not the same as events seen by the program.

### Separate ordering from timestamping

A shared ring can preserve reservation-order relationships useful across CPUs, while per-CPU buffers scale differently. Neither makes independent clocks identical or creates causality absent from events.

Record the clock source and conversion. Wall clock can step; per-CPU hardware counters may need synchronization; boot-time clocks may include or exclude suspend. Negative durations usually reveal a clock or identity error, not time travel.

### Treat BTF as versioned type evidence

BTF encodes types, strings, function and line information used by the kernel and loaders. Capture the target BTF identity. A field with the same name can change meaning even when its type remains relocatable.

CO-RE relocations adapt supported accesses to target type layouts. They improve portability across compatible kernels; they do not make internal functions stable, preserve event semantics, provide a universal ABI or compensate for a missing field essential to the algorithm.

### Verify relocation and fallback behavior

Inspect load logs and relocation results on every supported kernel family. Feature-detect optional fields and define whether their absence disables a metric, uses a validated alternate, or fails the deployment.

A fallback that emits zeros can look like healthy absence. Encode availability and schema version alongside data so decoders distinguish missing evidence from measured zero.

### Govern attachment and replacement

Prefer attachment objects with clear ownership and atomic replacement semantics where supported. Confirm link target, program ID and attach flags after load. Pin only when persistence is required and assign cleanup ownership.

During upgrade, avoid gaps and double counting. Version maps and records, drain old buffers, attach or replace at a defined boundary, and retain evidence that names the producing program.

### Restrict privilege and delegation

BPF loading, tracing, performance events and tracefs access can expose or affect system-wide state. Kernel and distribution policy, capabilities, LSMs, sysctls and namespaces determine availability. Do not infer safety from a loader running in a container.

Use a narrow privileged agent that validates signed or reviewed programs and exposes a constrained request API. Delegating map access or pinned objects delegates their information and mutation authority too.

### Protect sensitive fields

Kernel events can contain addresses, filenames, commands, identifiers, network metadata and payload fragments. Filter at collection when possible, hash only with a threat-appropriate keyed scheme, and bound retention and access.

In-kernel redaction lowers exposure but makes debugging harder and may create linkable pseudonyms. Review tenant boundaries and legal purpose before collection, not after raw traces have spread.

### Budget observer effect

Inactive hooks, enabled callbacks, map contention, stack capture, symbolization, wakeups and user-space export have different costs. Measure throughput, tail latency, CPU, cache, memory and drop rate with and without the exact configuration.

Instrumentation can slow the producer enough to remove the original overload, or add contention that creates a new one. Use staged escalation, canaries, maximum duration and automatic abort thresholds.

### Account for every pipeline loss

Count source opportunities where an independent counter exists, program invocations, filter/sample decisions, map update failures, evictions, reservation failures, kernel-buffer drops, reader gaps, decode failures and retention sampling. Keep each denominator.

If no independent source count exists, say that completeness is unknown. An empty output can mean no events, failed attachment, rejected filtering, full transport, crashed reader or incompatible decoder.

### Aggregate without destroying tails

Histograms and sketches reduce export volume but impose bucket boundaries, counter widths and merge semantics. A mean hides multimodal and tail behavior. Percentiles derived from coarse buckets have interval uncertainty.

Choose ranges before the run, count underflow and overflow, and retain totals. Do not average percentiles across CPUs or intervals; merge compatible distributions or raw sufficient statistics first.

### Validate the observation chain

Use a controlled workload that generates known events. Verify attach state, expected map changes, record schema, timestamps, CPU coverage, loss counters and teardown. Compare selected results with an independent counter or tracer.

Differential validation can run a high-overhead trusted method briefly beside the production method. Agreement over a test population raises confidence; disagreement localizes a boundary but does not automatically name which source is correct.

### Infer causality conservatively

Temporal order and correlation do not prove cause. State a mechanism, predict evidence under intervention, rule out clock and selection artifacts, and reproduce with a controlled change. Preserve counterevidence and uncertainty.

A BPF program can calculate the requested number perfectly from the wrong population. Review the semantic path with the same rigor as bytecode safety.

### Preserve and retire evidence

Store kernel build ID, BTF digest, program and map IDs, source artifact, loader version, configuration, attachment inventory, clocks, buffer sizes, loss, workload and raw-data checksum. Generated dashboards are not a substitute for raw bounded evidence.

At completion, detach links, close descriptors, unpin objects if policy requires, verify maps no longer update and remove sensitive captures under retention rules. Cleanup is part of the experiment.

## Definitions and Notation

For an observation interval, let $N_s$ be source occurrences at the declared hook boundary, $N_r$ program runs, $N_f$ events retained after filter or sampling, $N_m$ successful state updates or record constructions, $N_e$ emitted records, $N_d$ delivered records, and $N_c$ correctly decoded records. Under the declared pipeline,

$$
N_s\ge N_r\ge N_f\ge N_m\ge N_e\ge N_d\ge N_c,
$$

only when each stage processes at most one corresponding item and no aggregation or fan-out occurs. Otherwise use explicit multiplicities rather than forcing this inequality.

Transport loss is $L_t=N_e-N_d$ and decode loss is $L_c=N_d-N_c$. A reported delivery fraction is

$$
q_d=\frac{N_d}{N_e},
$$

provided $N_e>0$ and both counts share one definition and interval.

For independent Bernoulli sampling probability $p$ from a fixed population $N_s$, observed count $n$ has $E[n]=pN_s$, and the inverse-probability estimator is $\widehat N_s=n/p$. Scheduling, adaptive filters and burst loss can violate this simple model.

## Mechanisms, Invariants, or Proof Structure

1. **Question obligation:** define mechanism, competing explanations, population, interval and decision before collection.
2. **Boundary obligation:** prove the selected hook occurs where its name and fields support the claim.
3. **Artifact obligation:** bind source, bytecode, BTF, relocation, verifier, translated program and decoder to exact versions.
4. **Admission obligation:** validate program type, context, control flow, pointers, stack, helpers, return values and target under the active kernel.
5. **State obligation:** define map keys, ownership, concurrency, capacity, eviction, failure and lifetime.
6. **Transport obligation:** count construction, reservation, submission, kernel loss, delivery and decode outcomes.
7. **Identity obligation:** distinguish concurrent objects and identifier generations across missing events and reuse.
8. **Time obligation:** use a named clock and justify comparison, ordering, suspend and cross-CPU behavior.
9. **Overhead obligation:** measure perturbation and enforce rate, memory, duration and abort budgets.
10. **Security obligation:** minimize loader privilege, program effects, exposed fields, delegated objects and retention.
11. **Inference obligation:** cross-check semantics, uncertainty and alternatives before claiming cause.
12. **Lifecycle obligation:** upgrade without silent gaps, preserve reproducible evidence, detach and verify cleanup.

## Alternatives and Trade-Offs

- **Counters versus traces:** counters are cheap and durable but lose identity; traces preserve transitions but create volume and loss.
- **Static tracepoints versus dynamic probes:** tracepoints offer maintained schemas; probes reach gaps but depend on implementation.
- **Function tracing versus sampling:** tracing records selected calls; sampling estimates where execution spends time with lower event volume.
- **Raw events versus in-kernel aggregation:** raw data supports new questions; aggregation reduces exposure and transport at the cost of detail.
- **Global maps versus per-CPU maps:** global state simplifies snapshots but contends; per-CPU state scales but needs non-atomic merging.
- **Hash maps versus LRU maps:** fixed hashes preserve entries until explicit removal but fill; LRU bounds memory by evicting evidence.
- **Ring buffer versus per-CPU transport:** a shared ring aids cross-CPU order; per-CPU paths can reduce contention.
- **Fixed-rate versus adaptive sampling:** fixed probability supports simpler estimators; adaptation protects capacity but complicates inference.
- **BTF/CO-RE versus per-kernel builds:** relocations improve compatible portability; dedicated builds can validate exact internals at operational cost.
- **Interpreter versus JIT:** interpretation avoids native generation; JIT improves speed while adding architecture-specific code and hardening concerns.
- **Persistent pins versus loader-owned descriptors:** pins survive restarts; descriptor ownership simplifies cleanup.
- **Broad root agent versus constrained broker:** broad tools are flexible; brokers narrow privilege and accepted programs.
- **Synchronous export versus deferred reading:** prompt export lowers buffer pressure; deferred reads reduce wakeups but risk overwrite.
- **Precise stacks versus bounded identifiers:** stacks aid diagnosis but cost time and expose addresses; IDs need later symbolization.
- **Fail-open observability versus policy enforcement:** losing diagnostics may be acceptable; losing a BPF security decision may change authorization.
- **Long capture versus staged bursts:** long duration catches rare events; short controlled windows reduce perturbation and privacy exposure.

## Failure Modes and Misconceptions

1. **“Observability shows the internal state.”** It supports bounded inference from selected outputs.
2. **“A tracepoint name is its full contract.”** Inspect placement, fields and exact build.
3. **“Function return time is CPU time.”** Blocking, preemption and interrupts can occur between entry and return.
4. **“A kretprobe sees every return.”** capacity, control flow and attachment constraints can cause misses.
5. **“A flame graph explains wall latency.”** On-CPU samples omit blocked and off-CPU intervals unless separately represented.
6. **“The verifier proves the source program correct.”** It admits bytecode under kernel rules.
7. **“Verifier acceptance proves termination cost is small.”** Safety and acceptable production overhead are different claims.
8. **“All BPF programs have the same permissions.”** Program type, attachment, helpers and loader authority differ.
9. **“A helper call is safe for policy because arguments verify.”** Verifier safety is not deployment authorization.
10. **“CO-RE makes kernel internals an ABI.”** It relocates compatible type references; semantics can change.
11. **“BTF presence guarantees the intended field exists.”** Target types and essential relocation results must be checked.
12. **“PID is a permanent identity.”** Numeric task IDs are reused.
13. **“A map update cannot fail after creation.”** capacity, allocation and flags still matter.
14. **“LRU preserves the important keys.”** It preserves according to its eviction behavior, not analytical value.
15. **“Per-CPU counters form an atomic global snapshot.”** sequential reads observe different instants.
16. **“A ring buffer prevents loss.”** reservation and delivery fail under pressure.
17. **“Zero records means zero events.”** attachment, filtering, loss, reader and decode failures can also explain it.
18. **“Timestamps create causality.”** clock comparability and mechanism still need proof.
19. **“More events always improve diagnosis.”** volume increases overhead, loss and multiple-comparison risk.
20. **“In-kernel aggregation has no observer effect.”** maps, helpers, cache traffic and contention consume resources.
21. **“Sampling every tenth event is random.”** deterministic periodic sampling can alias periodic workloads.
22. **“Percentiles can be averaged.”** merge compatible distributions, not quantiles.
23. **“Container root scopes tracing to the container.”** underlying kernel policy determines visibility and authority.
24. **“The loader exiting removes everything.”** pinned objects and links can persist.
25. **“A dashboard preserves evidence.”** transformations can discard raw schema, loss and uncertainty.
26. **“Detaching ends the experiment.”** verify no attachments or updates remain and retire sensitive artifacts.

## Worked Examples

### Example 1

A static block-completion tracepoint and application completion differ by 8 milliseconds. Scheduler events show the application thread remained runnable. The block event disproves device delay for that interval; it does not alone prove scheduler policy caused the wait.

### Example 2

A dynamic probe targets a function optimized away in one fleet kernel. The loader reports no essential attachment, but a wrapper converts that to success with zero results. Failing closed on required attachment prevents false “no events” evidence.

### Example 3

A start-time map uses TID only. A missing exit leaves an entry; later ID reuse produces a multi-hour duration. A generation cookie plus age expiry and unmatched-event counters prevents silent collision.

### Example 4

An LRU flow map stays within memory budget but evicts rare slow flows during attack traffic. Counting eviction and using bounded latency histograms reveals that completeness changed under load.

### Example 5

Per-CPU histograms are read and reset sequentially while traffic continues. Summed totals span different boundaries. A coordinated interval protocol or read-without-reset plus per-CPU deltas makes the interval explicit.

### Example 6

CO-RE successfully relocates a renamed structure field of the same type, but its unit changed. The program loads and emits plausible values. A semantic compatibility test catches what type relocation cannot.

### Example 7

Full stack capture on every packet reduces throughput enough to remove queue buildup. Filtered anomaly sampling reproduces the queue while an independent counter confirms the same population.

### Example 8

The program emits 5,000 records, the ring delivers 4,900 and the decoder accepts 4,880. Reporting 4,880 as the source count hides at least two distinct losses and any earlier filter or hook gap.

### Example 9

A privileged observability agent accepts arbitrary object files from tenants. Verifier memory-safety checks do not prevent cross-tenant metadata collection through permitted helpers. A reviewed program catalog and constrained parameters narrow delegation.

### Example 10

An upgrade attaches a new program before detaching the old one, doubling counters for six seconds. Producer version and link inventory expose overlap; an atomic replacement mechanism or explicit cutover interval prevents it.

## Cross-Program Connections

- **Performance engineering:** counters, samples, histograms and observer effect determine valid bottleneck evidence.
- **Distributed systems:** clocks, identifiers, partial traces, loss and causal inference recur across machine boundaries.
- **Streaming systems:** bounded buffers, backpressure, sampling, schemas and aggregation govern event pipelines.
- **Security engineering:** privileged loaders, kernel introspection, policy hooks, JITs and data exposure require threat models.
- **Compiler engineering:** bytecode generation, BTF, relocations, abstract interpretation and JIT compilation shape admission.
- **Data engineering:** denominators, schema versions, lineage, retention and uncertainty determine analytical validity.
- **Platform engineering:** fleet rollout, feature detection, canaries, pin cleanup and evidence collection operationalize BPF.
- **API engineering:** tracepoints, helpers, kfuncs, maps and link interfaces are versioned contracts with distinct stability.
- **Privacy engineering:** process, path, address and network observations can identify people, tenants or workloads.
- **Formal methods:** abstract states, invariants and proof scopes clarify what verifier acceptance establishes.

## References

1. Linux Kernel Documentation, [Linux Tracing Technologies Guide](https://docs.kernel.org/trace/index.html), tracing frameworks, tracepoints, function tracing and probe facilities; retrieved 2026-09-04.
2. Linux Kernel Documentation, [ftrace](https://docs.kernel.org/trace/ftrace.html), tracefs controls, instances, clocks, buffers, events, filters and function graphs; retrieved 2026-09-04.
3. Linux Kernel Documentation, [Using the Linux Kernel Tracepoints](https://docs.kernel.org/trace/tracepoints.html), hook activation, caller execution context, schemas and synchronization; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Kernel Probes](https://docs.kernel.org/trace/kprobes.html), entry and return probes, missed instances, optimization and architecture limitations; retrieved 2026-09-04.
5. Linux man-pages Project, [perf_event_open(2)](https://man7.org/linux/man-pages/man2/perf_event_open.2.html), counting, sampling, grouping, multiplexing, records, loss and permissions; retrieved 2026-09-04.
6. Linux Kernel Documentation, [eBPF Verifier](https://docs.kernel.org/bpf/verifier.html), abstract register and pointer states, initialized stack, branch exploration, pruning and helper validation; retrieved 2026-09-04.
7. Linux Kernel Documentation, [eBPF Syscall](https://docs.kernel.org/userspace-api/ebpf/syscall.html), program and map commands, object information, flags and file-descriptor lifecycle; retrieved 2026-09-04.
8. Linux Kernel Documentation, [BPF Maps](https://docs.kernel.org/bpf/maps.html), map families, key/value operations and user/kernel sharing; retrieved 2026-09-04.
9. Linux Kernel Documentation, [BPF Ring Buffer](https://docs.kernel.org/bpf/ringbuf.html), reservation, submission, discard, ordering, wakeups and bounded capacity; retrieved 2026-09-04.
10. Linux Kernel Documentation, [BPF Type Format](https://docs.kernel.org/bpf/btf.html), kernel and ELF metadata, function and line information and CO-RE relocations; retrieved 2026-09-04.
11. Linux Kernel Documentation, [libbpf Overview](https://docs.kernel.org/bpf/libbpf/libbpf_overview.html), open, load, attach and teardown lifecycle plus BTF-based CO-RE; retrieved 2026-09-04.

## Exercises

### Exercise 1

Choose an observation sequence to distinguish block-device service time, wakeup-to-run delay and user-space processing in a slow request. State each boundary, clock, identity and independent cross-check.

### Exercise 2

An event pipeline has 100,000 source opportunities, 20,000 sampled runs, 19,950 successful map updates, 1,250 emitted anomalies, 1,200 delivered records and 1,188 decoded records. Compute update success, transport delivery and decode success with correct denominators; explain what cannot be inferred.

### Exercise 3

Design a BPF start/finish latency correlator that handles nested operations, missing exits, task-ID reuse, map pressure, CPU migration, clock choice, reload and teardown. State what verifier acceptance does not prove.

### Exercise 4

Plan a CO-RE rollout across three kernel families when one lacks an optional field and another changes the field's semantics. Include BTF identity, relocation tests, feature policy, schema versions, canaries and rollback.

### Exercise 5

Audit a tenant-facing observability service that loads arbitrary BPF objects, pins maps indefinitely, exports raw paths and claims zero events means policy compliance. Produce a constrained design with privilege, capacity, privacy, loss and evidence controls.

## Answers to the Exercises

### Answer 1

Carry a generation-tagged application request ID at user enqueue and completion. Record syscall entry/exit if relevant, block issue and completion for each derived request, scheduler wakeup, runnable enqueue, switch-in and switch-out for the task instance. Use one documented trace clock or calibrated conversion and distinguish a logical request from multiple block objects.

Device service is issue-to-block-completion; wakeup-to-run is successful wake or runnable enqueue to switch-in; user processing is bounded by user markers with intervening kernel intervals subtracted only when clocks and nesting permit. Record unmatched events and trace loss. Cross-check block counts and service with device or subsystem counters, runnable delay with scheduler statistics, and end-to-end latency with the application's independent monotonic timer.

### Answer 2

Update success is `19,950 / 20,000 = 99.75%`. Transport delivery is `1,200 / 1,250 = 96%`. Decode success is `1,188 / 1,200 = 99%`. The calculation is reproducible:

<!-- bijux-verify: {"id":"observability-pipeline-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"update_success 99.75%\ntransport_delivery 96.00%\ndecode_success 99.00%\nend_to_end_source 1.188%\nknown_post_emit_loss 62\n"}} -->
```python
source = 100_000
sampled = 20_000
updated = 19_950
emitted = 1_250
delivered = 1_200
decoded = 1_188

print(f"update_success {updated / sampled:.2%}")
print(f"transport_delivery {delivered / emitted:.2%}")
print(f"decode_success {decoded / delivered:.2%}")
print(f"end_to_end_source {decoded / source:.3%}")
print("known_post_emit_loss", emitted - decoded)
```

The 1.188 percent end-to-end ratio is not completeness: sampling and anomaly filtering intentionally remove populations, source opportunities may not equal actual hook invocations, aggregation can change multiplicity, and no numbers establish field semantics, unbiased selection, unique identity, clock correctness or low observer effect.

### Answer 3

Key state by task-generation identity plus an operation identifier or bounded nesting slot, not TID alone. On start, reject or count an occupied slot, store the chosen monotonic timestamp and producer version, and handle insertion failure. On finish, look up the matching generation and operation, validate ordering, calculate duration, update a per-CPU bounded histogram and delete state. Count missing starts, missing finishes, negative or overflow durations, full maps and evictions. Expire stale entries through a bounded cleanup design and account for task exit.

CPU migration is harmless only if the clock is comparable and the lookup is global; a per-CPU start map needs an explicit migration strategy. Upgrade through an owned link replacement and producer schema version, avoiding overlap or gaps, then drain and detach. The verifier can establish admitted pointer, stack, control-flow and helper use. It does not prove identity uniqueness, event pairing, timestamp meaning, no losses, histogram semantics, low overhead, privacy or causal correctness.

### Answer 4

Record the BTF digest and build identity for all three families. In CI, load the exact object, inspect every essential and optional relocation, verifier result, program and attach type, then run a semantic fixture whose known kernel actions produce known outputs. The fully compatible family uses the primary schema. The family missing an optional field emits an explicit availability bit and omits only the derived metric; if the field is essential, fail deployment instead.

The semantically changed family cannot be accepted merely because relocation succeeds. Implement and review a family-specific interpretation or declare it unsupported, assign a new record schema version and validate against independent counters. Canary each path with overhead and loss thresholds. Preserve the previous program and link, use a defined replacement boundary, drain versioned buffers, and roll back atomically or detach the rejected version. Evidence binds data to source object, BTF, relocation log, program ID and decoder.

### Answer 5

Replace arbitrary loading with a catalog of reviewed, signed programs and bounded parameters. A narrow broker verifies artifact identity, allowed program/attach types, helpers, maps, target scope and expected BTF before loading. Tenant authorization limits cgroups, processes or other enforceable scope; kernel and LSM policy deny direct BPF, performance and tracefs access outside the broker.

Give every map a memory/cardinality budget, ownership, TTL, full-map behavior and tenant boundary. Pin only required objects under broker-owned paths, inventory them continuously and remove them at expiry or tenant deletion. Filter and tokenize paths in kernel or the earliest trusted stage, protect the token key, minimize fields and enforce retention. Export attachment status, program runs, filters, map failures/evictions, buffer reservation failures, reader loss and decode failures. “Zero events” is reported as unknown unless required attachment, coverage and loss controls prove the monitored population. Audit logs bind each decision to program, kernel, BTF, tenant, policy and teardown evidence.
