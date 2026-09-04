---
module_id: OS-020
program: Operating Systems
level: 1
module_number: 20
title: Measuring Scheduler Latency and Throughput
status: complete
last_verified: 2026-09-04
---

# Measuring Scheduler Latency and Throughput

## One-Page Review

### Governing question

How can we measure scheduler delay and delivered throughput without confusing clock artifacts, blocked time, incomplete work, tracing overhead, or synthetic load with the property we intend to evaluate?

### Essential definitions

- **release time** is when work becomes eligible to run under the measured contract.
- **dispatch latency** is time from a defined runnable or release event to actual execution.
- **wakeup latency** is time from a wake event to schedule-in; it is only one kind of dispatch latency.
- **scheduler delay** is accumulated time eligible but not running.
- **service time** is charged execution time; **response time** and **turnaround time** depend on application boundaries.
- **throughput** is completed correct units per declared observation interval.
- **censoring** occurs when observations lack the endpoint required for a metric, often because work remains unfinished.
- **coordinated omission** occurs when a load generator stops issuing independent arrivals while the system is slow, thereby omitting delays users would have experienced.
- **observer effect** is the change introduced by clocks, tracing, counters, logging, or sampling.

### Central model, mechanism, or theorem

For job `i`, let release be `r_i`, runnable enqueue `q_i`, first schedule-in `s_i`, completion `c_i`, and charged execution `x_i`. Then dispatch latency is `s_i-r_i` or `s_i-q_i` only after choosing the boundary; turnaround is `c_i-r_i`; scheduler delay sums runnable-not-running intervals; blocking sums ineligible intervals.

An evidence claim must bind metric definition, population, clock, instrumentation point, aggregation, observation window, workload, system configuration, and missing-data rule. A precise number with any of those unspecified is not reproducible scheduler evidence.

### Critical invariants

- Timestamps use one compatible clock domain or a validated conversion and remain monotonic for duration calculations.
- Event identity correlates release, enqueue, run, preemption, wake, completion, and cancellation without reuse ambiguity.
- State intervals partition eligible waiting, running, blocked, throttled, and terminal time according to the model.
- Throughput counts correct completions while also reporting offered, admitted, failed, shed, canceled, and unfinished work.
- Aggregation preserves the population and does not average percentiles or discard harmed classes silently.
- Measurement overhead, loss, sampling, clock resolution, warmup, and environmental configuration are recorded.
- Empirical maxima remain observed values, not universal worst-case bounds.

### Common failures

Common mistakes are timing a context-switch ping-pong and naming it scheduler latency, subtracting unrelated clocks, measuring from a timer's intended rather than actual expiration without saying so, including blocked time as run-queue delay, dropping unfinished requests, reporting only completions under overload, averaging per-host percentiles, using closed-loop load that omits queued arrivals, ignoring trace loss, benchmarking only warm caches, and treating one maximum as a real-time proof.

### Compact example

Four jobs are offered during a ten-second window, but only three finish. Their release-to-first-run latencies are 0.4, 1.0, and 3.0 seconds, giving mean 1.47 and observed maximum 3.0. Completion throughput is `3/10 = 0.30 jobs/s`; one job remains censored. Reporting only the three latencies without the unfinished fourth job makes the overload picture look better than the delivered service.

### Connections

[OS-014](014-context-switching.md) separates switch duration from recovery, [OS-015](015-process-states-and-wait-queues.md) defines wake transitions, and [OS-016](016-scheduling-objectives.md) defines response and throughput. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames evidence, budgets, and assurance.

## Governing Question

Scheduler performance is a chain of events. A device or timer makes work ready; a wake path publishes eligibility; a run queue receives the task; policy selects it; context switching transfers the CPU; the task reacquires resources; and application work eventually completes. A single interval rarely represents the whole chain.

Instrumentation observes different boundaries. Scheduler tracepoints reveal enqueue and switch events. Application timestamps reveal request arrival and completion. Performance counters sample hardware events. `/proc` and scheduler statistics expose cumulative fields. Each source has different scope, enablement, precision, loss, privilege, and perturbation.

The governing question is how to construct a measurement model before collecting numbers, then validate that the captured events actually support the intended latency or throughput claim.

## Why This Matters

Bad scheduler measurements drive bad policy. Reducing a microbenchmark's ping-pong time may not improve wakeup-to-response latency. Raising throughput by dropping slow requests harms users even if completed-request percentiles improve. Pinning tasks can stabilize one run while creating unrealistic locality.

Production incidents also require attribution. A task may wait because it is blocked on I/O, runnable behind competitors, quota-throttled, affinity-constrained, descheduled by interrupt work, or delayed after dispatch by a lock. “CPU latency” without state intervals cannot distinguish them.

Real-time claims demand stronger discipline. A trace can reveal violations and characterize tested conditions, but absence of a large delay does not prove a bound. Measurement complements workload and schedulability analysis; it does not replace them.

## Prerequisites and Retrieval

Recall switch boundaries from [OS-014](014-context-switching.md), runnable and blocked state from [OS-015](015-process-states-and-wait-queues.md), objective metrics from [OS-016](016-scheduling-objectives.md), and fair-share eligibility from [OS-019](019-fair-scheduling.md). Understand monotonic clocks, distributions, percentiles, rates, and experimental controls.

Retrieve these distinctions:

- intended timer expiration, actual interrupt, wake call, runnable enqueue, and schedule-in are different events;
- context-switch count, switch duration, scheduler delay, wakeup latency, and response are different metrics;
- CPU time is not wall time or completed useful work;
- offered load, admitted load, and completed throughput are different populations;
- median, high percentile, observed maximum, and analytical bound are different claims;
- per-task, per-process, per-group, per-CPU, and system accounting have different scopes;
- tracing a system changes it and can lose events.

## Learning Objectives

After this module, you should be able to:

1. define event boundaries for dispatch, wakeup, run-queue, response, and completion latency;
2. reconstruct runnable, running, blocked, throttled, and terminal intervals from correlated events;
3. compute throughput while retaining failures, shedding, and censored work;
4. select clocks, tracepoints, counters, and sampling methods with explicit limitations;
5. detect percentile aggregation, coordinated omission, warmup, trace-loss, and observer errors;
6. design repeatable scheduler experiments across load, topology, and failure conditions;
7. separate empirical characterization from worst-case and certification claims.

## Core Exposition

### Start with a causal timeline

Write the expected event sequence before choosing a tool. For a sleeping task, relevant points may be external stimulus, interrupt entry, predicate publication, wake request, runnable enqueue, scheduler selection, schedule-in, lock reacquisition, first useful instruction, and response completion.

No single pair answers every question. Wake-to-run isolates part of scheduler delivery. Stimulus-to-run includes device and wake handling. Request-to-response includes blocking and useful work. State the pair in metric names and documentation.

### Clock selection

Duration measurements require a monotonic clock not subject to wall-clock steps. Linux clock interfaces document monotonic, raw, boot-inclusive, process CPU, and thread CPU clocks with different semantics. Suspend, frequency correction, virtualization, and cross-CPU synchronization can matter.

Resolution reported by an API is not measurement accuracy. Read overhead, serialization, compiler motion, vDSO versus syscall paths, and timestamp placement add error. Calibrate by measuring the clock path and validate cross-source timestamp alignment.

### Event identity and correlation

Process IDs and thread IDs can be reused. File descriptors, request addresses, and queue slots can also be recycled. Correlation needs a generation or unique request identity whose lifetime spans every recorded endpoint.

Lost trace records break interval reconstruction. Sequence numbers, per-CPU loss counters, impossible-transition checks, and terminal reconciliation expose gaps. Silently pairing the next matching identifier can invent plausible but false latency.

### State interval reconstruction

For each task, construct a state machine: runnable enqueue starts eligible wait; schedule-in ends wait and starts execution; preemption ends execution and begins eligible wait; block ends execution and begins ineligible wait; wake ends blocked state and normally begins runnable wait.

Throttling and stopped states need separate categories. Migration changes queue ownership without necessarily changing eligibility. Nested or out-of-order events indicate loss, clock mismatch, or a model error and should invalidate affected samples rather than be coerced.

### Dispatch and wakeup latency

Release-to-first-run applies to a job model. Enqueue-to-run measures scheduler queueing. Wake-call-to-run includes wake processing after the timestamp location. Intended-timer-deadline-to-handler or to-thread includes timer and interrupt error.

Report which task, priority, group, affinity, and CPU produced each endpoint. A waker timestamp on one CPU and a run timestamp on another require a comparable clock domain. Migration and idle-state exit can dominate the result.

### Switch duration is different

A switch trace interval around scheduler handoff measures the instrumented boundary. A ping-pong benchmark includes synchronization, wakeup, selection, two transfers, clock reads, and possibly system calls. Neither automatically captures cache and TLB recovery after return.

Name the measured operation. Separate direct handoff, wake-to-run, and end-to-end response instead of subtracting an assumed “switch constant.”

### Throughput and correctness

Throughput is correct completed work per window. Define whether the denominator is wall time, active test time, or admitted interval, and whether warmup and drain are included. Completion at the boundary needs a consistent inclusion rule.

Report offered, admitted, started, completed, failed, timed out, canceled, shed, retried, and unfinished counts. Retries can inflate operation count while useful outcomes decline. Correctness checks belong in the benchmark.

### Censoring and survivor bias

An unfinished job has no completion latency, but it still belongs to offered load. Dropping it from distributions biases results under overload. Report censored counts and age distributions; use survival analysis where the question warrants it.

Completed-request percentiles are conditional on completion. Compare them alongside admission, loss, and backlog. A policy that never completes hard work can otherwise appear excellent.

### Coordinated omission

A closed-loop generator waits for a response before issuing the next request. When service slows, it reduces offered arrivals, omitting queueing that an independent user population would create. This can hide saturation tails.

Use an open-loop or independently scheduled arrival process when that matches reality, and record intended issue time even if the generator falls behind. Closed-loop load is valid for closed-loop systems, but its result must not be generalized to independent arrivals.

### Distributions and aggregation

Retain raw observations or mergeable histograms with known precision. Compute fleet percentiles from the combined population, not by averaging host percentiles. Report sample count, quantile definition, confidence or run-to-run variation, and class stratification.

Means support additive reasoning but can hide tails. Maximum observed depends on sample size. A high percentile with ten observations is unstable. Plot time order as well as distributions to expose warmup, thermal drift, and phase changes.

### Scheduler statistics and proc interfaces

Linux scheduler statistics can expose run, wait, wake, and domain counters when configured. `/proc/stat` reports aggregate CPU categories and system counters; `/proc/loadavg` reports load-related fields. `getrusage` supplies CPU time and voluntary and involuntary context-switch counts.

These are cumulative observations with scopes and version details. A delta needs consistent sampling and wrap, reset, process-exit, hotplug, and aggregation handling. A load average is not CPU utilization or scheduler latency.

### Tracepoints and ftrace

Trace event interfaces expose available events, enabling, filters, and formats. Scheduler events can correlate wakeup and switch activity. Function tracing can inspect execution paths but adds overhead and may recurse or alter timing.

Capture metadata, buffer size, clock, filters, CPU mask, event format, trace loss, and tool version. Restrict access: scheduler traces reveal process names, timing, and tenant behavior.

### Performance counters

Performance events can count cycles, instructions, cache behavior, context switches, and software events subject to hardware and kernel support. Multiplexing scales counts and increases uncertainty. Sampling can skid, lose records, and attribute shared or kernel work imperfectly.

Use counters to explain, not merely correlate. A rise in cache misses after migration supports a hypothesis only with workload controls and compatible event semantics. Preserve raw counts, enabled and running time, privilege exclusions, and CPU model.

### OS noise and timer latency

Linux osnoise and timerlat tracers distinguish interference from interrupts, soft interrupts, threads, and related sources under their documented model. `rtla` wraps analysis interfaces and has configuration, tracing, affinity, priority, and threshold options.

These tools help characterize deployed kernels but do not capture every firmware, hypervisor, device, or hardware delay. Tool threads and tracing also consume resources. Validate the test topology and external time reference when consequences demand it.

### Experimental design

Define workload class, arrivals, service demand, concurrency, priorities, groups, quotas, affinity, topology, memory placement, power policy, thermal state, kernel, firmware, mitigations, and background load. Include cold and warm states, underload through overload, steady and bursty arrivals, and failures.

Randomize run order where drift matters. Repeat across boots and machines. Use baselines and negative controls. Store commands, configuration, raw events, summaries, and analysis code in governed artifacts.

### Real-time and assurance boundaries

Real-time evaluation measures release jitter, interrupt latency, wakeup, dispatch, execution, blocking, preemption, and deadline response under credible interference. An observed maximum is one sample. Analytical bounds require execution and blocking models plus platform assumptions.

Safety-relevant conclusions need trace-integrity checks, independent clock or monitor where required, fault injection, configuration control, and named review. This module provides measurement discipline, not certification.

## Definitions and Notation

For job `i`, let intended release be `r_i`, runnable enqueue `q_i`, first schedule-in `s_i`, completion `c_i`, execution service `x_i`, deadline `d_i`, and terminal outcome `o_i`. Define:

- release-to-run `D_i = s_i-r_i`;
- enqueue-to-run `E_i = s_i-q_i`;
- turnaround `T_i = c_i-r_i` when completion exists;
- tardiness `L_i = max(0,c_i-d_i)` when both endpoints exist;
- throughput `X = correct_completions / observation_duration`;
- censor indicator `z_i=1` when a required endpoint is absent at observation end.

Let `N_offered`, `N_admitted`, `N_completed`, `N_failed`, `N_shed`, and `N_censored` describe populations. These counts should reconcile under the benchmark's lifecycle rules.

## Mechanisms, Invariants, or Proof Structure

A defensible measurement review follows eight obligations:

1. Define the causal event chain and exact metric endpoints.
2. Validate clock monotonicity, domain conversion, resolution, and read overhead.
3. Use lifetime-unique correlation and reject traces with unreconciled loss or impossible transitions.
4. Reconstruct running, runnable, blocked, throttled, and terminal intervals without overlap.
5. Reconcile offered, admitted, completed, failed, shed, canceled, and censored populations.
6. Specify arrival process, windows, aggregation, quantiles, warmup, drain, and coordinated-omission policy.
7. Record workload, topology, kernel, firmware, power, thermal, security, and instrumentation configuration.
8. Separate observed results, causal inference, analytical bounds, and assurance approval.

The executable example keeps unfinished work visible while computing completed-job metrics.

<!-- bijux-verify: {"id":"toy-scheduler-measurement","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"offered=4 completed=3 censored=1\nthroughput=0.30 jobs/s\nmean-response=1.47 s\nmax-response=3.00 s\ndeadline-misses=1\n","stderr":""}} -->
```python
jobs = [
    {"release": 0.0, "first": 0.4, "complete": 3.0, "deadline": 4.0},
    {"release": 1.0, "first": 2.0, "complete": 4.0, "deadline": 5.0},
    {"release": 2.0, "first": 5.0, "complete": 9.0, "deadline": 8.0},
    {"release": 3.0, "first": None, "complete": None, "deadline": 9.0},
]
window = 10.0
completed = [job for job in jobs if job["complete"] is not None]
responses = [job["first"] - job["release"] for job in completed]
misses = sum(job["complete"] > job["deadline"] for job in completed)

print(f"offered={len(jobs)} completed={len(completed)} censored={len(jobs)-len(completed)}")
print(f"throughput={len(completed) / window:.2f} jobs/s")
print(f"mean-response={sum(responses) / len(responses):.2f} s")
print(f"max-response={max(responses):.2f} s")
print(f"deadline-misses={misses}")
```

The toy demonstrates bookkeeping only. It has no scheduler trace, state intervals, clock error, retries, sampling, confidence analysis, or real-time bound.

## Alternatives and Trade-Offs

- Application timestamps capture outcomes but obscure kernel attribution.
- Scheduler tracepoints expose transitions but not all application work.
- Counters are lower volume but aggregate or sample causality.
- Full tracing improves reconstruction while increasing perturbation and data sensitivity.
- Open-loop load exposes queueing; closed-loop load models dependent clients and applies backpressure.
- Long runs reveal rare tails and thermal state but increase drift and configuration exposure.
- Pinning improves repeatability while reducing realism for migratory workloads.
- Synthetic tests isolate mechanisms; production-like tests improve relevance but reduce control.
- Observed maxima find violations; analytical bounds address unobserved executions under assumptions.

## Failure Modes and Misconceptions

1. **“Scheduler latency has one definition.”** Release, wake, enqueue, and schedule-in boundaries differ.
2. **“A syscall clock is ground truth.”** clock domain, placement, overhead, and resolution matter.
3. **“CPU time measures response.”** It excludes runnable and blocked wall time.
4. **“A switch count measures switch cost.”** Count has no duration or recovery information.
5. **“Ping-pong equals context-switch time.”** It includes synchronization, wakeup, selection, and clocks.
6. **“Load average is utilization.”** It has documented but different semantics.
7. **“Completed percentiles describe offered work.”** failures and unfinished work are censored.
8. **“Closed-loop load is always realistic.”** It omits independent arrivals during slow responses.
9. **“Average host p99 is fleet p99.”** Percentiles do not aggregate that way.
10. **“More tracing is more accurate.”** buffers overflow and probes perturb schedules.
11. **“Warm caches reduce noise.”** They can remove the deployment behavior of interest.
12. **“One counter proves cause.”** attribution and competing explanations remain.
13. **“No observed violation proves compliance.”** coverage is finite.
14. **“Maximum observed is worst case.”** a bound requires assumptions and analysis beyond sampling.

## Worked Examples

### Example 1

A timer should expire at 10.000, interrupts at 10.003, wakes a task at 10.004, and the task runs at 10.009. Timer-to-run is 9 ms; wake-to-run is 5 ms. Calling both “scheduler latency” hides 4 ms of timer and wake handling.

### Example 2

A task spends 8 ms blocked on storage, 3 ms runnable, and 2 ms executing. Turnaround is 13 ms, scheduler delay 3 ms, and service 2 ms. Optimizing the run queue cannot remove the storage interval.

### Example 3

A ping-pong round trip is 20 microseconds. Dividing by two estimates a composite one-way operation, not low-level context-switch duration, because signaling, enqueue, selection, clock reads, and cache effects remain.

### Example 4

A trace loses one schedule-out record. The next schedule-in would create overlapping running intervals. Sequence and state validation reject that task segment rather than fabricating a duration.

### Example 5

A server offers 1,000 requests, completes 800, rejects 100, and leaves 100 pending. Reporting 800 completion latencies alone hides 20% noncompletion; population reconciliation makes overload visible.

### Example 6

A closed-loop client sends one request at a time. During a one-second stall it issues nothing. An open-loop model scheduled at 100 requests/s would accumulate 100 delayed arrivals, producing a different and valid workload claim.

### Example 7

Two hosts report p99 values 10 and 100 ms with 10,000 and 10 samples. Their average 55 ms is not the fleet p99. Merge raw observations or compatible histograms with population weights.

### Example 8

Enabling full function tracing removes a latency spike by shifting timing and prevents the original race. A lighter scheduler event set plus hardware or external evidence offers a different observer trade-off.

### Example 9

A migrated task's wake-to-run latency is modest but request response rises with cache misses. Correlated counters support a locality hypothesis; controlled pinned and migratory runs test it.

### Example 10

A real-time test records no violation across one billion releases. This is strong empirical evidence for the tested platform and workload, but firmware, fault, and untested-state assumptions still prevent a universal bound claim.

## Cross-Program Connections

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) develops requirements, evidence, uncertainty, hazards, and acceptance. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) develops open- and closed-loop load, coordinated omission, tails, admission, and overload.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains clocks, counters, caches, TLBs, frequency, and topology. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames tracing authority and workload information leakage.

Within this program, [OS-021](../ROADMAP.md) begins kernel synchronization, whose lock and interrupt delays later measurements must distinguish from run-queue delay.

## References

- Linux man-pages project, [clock_gettime(2)](https://man7.org/linux/man-pages/man2/clock_gettime.2.html), current page checked 2026-09-04. Clock IDs, monotonicity, CPU clocks, dynamic clocks, resolution, and errors.
- Linux man-pages project, [getrusage(2)](https://man7.org/linux/man-pages/man2/getrusage.2.html), current page checked 2026-09-04. CPU time, faults, context-switch counts, and process and thread scope.
- Linux man-pages project, [perf_event_open(2)](https://man7.org/linux/man-pages/man2/perf_event_open.2.html), current page checked 2026-09-04. Hardware and software events, sampling, context-switch records, multiplexing, attribution, and errors.
- Linux man-pages project, [proc_stat(5)](https://man7.org/linux/man-pages/man5/proc_stat.5.html), current page checked 2026-09-04. Aggregate CPU categories, interrupts, context switches, boot time, running, and blocked counts.
- Linux man-pages project, [proc_loadavg(5)](https://man7.org/linux/man-pages/man5/proc_loadavg.5.html), current page checked 2026-09-04. Load averages, runnable entity counts, and latest process identifier.
- Linux Kernel documentation, [Scheduler Statistics](https://docs.kernel.org/scheduler/sched-stats.html), current page checked 2026-09-04. Run, wait, wakeup, and domain statistics with version and configuration constraints.
- Linux Kernel documentation, [Using the Linux Kernel Tracepoints](https://docs.kernel.org/trace/events.html), current page checked 2026-09-04. Event discovery, enablement, filtering, formats, and interface behavior.
- Linux Kernel documentation, [ftrace](https://docs.kernel.org/trace/ftrace.html), current page checked 2026-09-04. Tracing infrastructure, clocks, buffers, tracers, filtering, snapshots, and overhead controls.
- Linux Kernel documentation, [OSNOISE Tracer](https://docs.kernel.org/trace/osnoise-tracer.html), current page checked 2026-09-04. Runtime noise measurement and attribution to interrupts, soft interrupts, and threads.
- Linux Kernel documentation, [Timerlat Tracer](https://docs.kernel.org/trace/timerlat-tracer.html), current page checked 2026-09-04. Timer IRQ and thread latency, thresholds, stacks, user workloads, and interpretation.
- Linux Kernel documentation, [rtla-osnoise](https://docs.kernel.org/tools/rtla/rtla-osnoise.html), current page checked 2026-09-04. OS-noise histograms and top mode, affinity, priorities, thresholds, tracing, and options.
- Linux Kernel documentation, [PSI — Pressure Stall Information](https://docs.kernel.org/accounting/psi.html), current page checked 2026-09-04. CPU, memory, and I/O stall averages, totals, and triggers.
- Linux Kernel documentation, [Perf Events and Tool Security](https://docs.kernel.org/admin-guide/perf-security.html), current page checked 2026-09-04. Data categories, credentials, access control, resource limits, and security scope.

## Exercises

### Exercise 1

Construct an event timeline from timer intention through response and calculate timer error, wake processing, wake-to-run, lock reacquisition, work, and total response. State compatible clock assumptions.

### Exercise 2

Given offered, admitted, completed, failed, shed, retried, and unfinished records, design reconciliation rules and compute throughput and latency populations without survivor bias.

### Exercise 3

Design open-loop and closed-loop experiments for the same service. Explain coordinated omission, generator lag, admission, warmup, drain, and overload reporting.

### Exercise 4

Specify a scheduler trace validator that handles task-ID reuse, migration, lost events, impossible state transitions, clock domains, and buffer overflow.

### Exercise 5

Construct an assurance review for measured dispatch latency in a safety-relevant controller. Cover instrumentation, platform state, faults, analytical bounds, and human judgment.

## Answers to the Exercises

### Answer 1

Let intended expiry be 100.000 ms, interrupt entry 100.004, wake request 100.006, runnable enqueue 100.007, schedule-in 100.015, predicate lock acquisition 100.018, and response completion 100.025. Timer-to-interrupt is 4 microseconds, interrupt-to-wake 2, wake-to-enqueue 1, enqueue-to-run 8, run-to-lock 3, work-to-response 7, and total intended-expiry-to-response 25.

All timestamps must share one validated monotonic domain or use measured conversions. Placement must say whether timestamps occur before or after publication. Resolution and read overhead are reported; negative or causally impossible intervals invalidate the record.

### Answer 2

Assign one terminal outcome per admitted generation. Offered equals admission plus rejection or shedding under the chosen boundary. Admitted equals correct completion plus failure plus cancellation plus unfinished, with retries either linked as attempts to one logical request or counted separately and labeled. Reconcile at observation end and retain ages for unfinished work.

Throughput counts correct logical completions divided by the declared window. Completion latency applies only to completed work and is reported with counts and censoring; release-to-first-run can include an unfinished task only if that endpoint exists. Do not silently convert timeouts or shed work into absent samples.

### Answer 3

The open-loop generator schedules arrivals independently and records intended issue time even when late; offered backlog reveals queueing. The closed-loop generator waits for each response or permits a fixed outstanding population, modeling dependent clients and backpressure. Run both only if both populations matter, and label them separately.

Calibrate generator capacity, record missed issue deadlines, synchronize clocks where distributed, hold configuration constant, and span underload to overload. Define warmup exclusion without discarding bad steady states, stop admission at the window boundary, drain with separately labeled completions, and report offered, admitted, failed, shed, and censored populations.

### Answer 4

Use `(task_id,generation)` plus CPU and sequence metadata. Maintain per-task state and per-CPU current ownership. Validate enqueue only from allowed states, schedule-in only for eligible queued tasks, schedule-out only for the CPU's current task, and migration with one source and destination owner. Reject overlapping running intervals and negative durations.

Read trace loss and overwrite indicators, reconcile per-CPU sequence gaps, preserve event-format versions, and avoid pairing across gaps without proof. Validate clock monotonicity per CPU and cross-CPU conversion before migration intervals. Mark affected observations missing rather than repairing them heuristically. Report validator rejection counts with measurement results.

### Answer 5

Define release, runnable, schedule-in, useful work, output, deadline, and safe response. Use a monotonic validated clock, bounded instrumentation, unique event correlation, loss detection, and an independent monitor where required. Lock kernel, firmware, topology, affinity, power, thermal, interrupt, memory, and tracing configuration.

Exercise nominal load, overload, CPU loss, device and timer faults, thermal throttling, trace overflow, and recovery. Decompose timer, interrupt, wake, run-queue, blocking, execution, and output delay. Compare traces with schedulability and worst-case blocking analysis; observed maxima do not become bounds. Named real-time, kernel, measurement, platform, safety, security, independent-verification, and acceptance owners review evidence and residual risk. This chapter claims no certification.
