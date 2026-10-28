---
module_id: OS-016
program: Operating Systems
level: 1
module_number: 16
title: Scheduling Objectives
status: complete
last_verified: 2026-09-04
---

# Scheduling Objectives

## One-Page Review

### Governing question

What should a scheduler optimize, for whom, over which time horizon, and under which correctness, isolation, energy, and assurance constraints?

### Essential definitions

- **Response time** is time from arrival or release until first useful service.
- **Turnaround time** is time from arrival until completion.
- **Waiting time** is eligible time not executing, under a precisely stated eligibility model.
- **Throughput** is completed work per observation interval; **utilization** is the fraction of a resource's capacity assigned or productively used under a declared denominator.
- **Fairness** is a specified allocation relationship among contenders, not merely equal CPU time.
- A **deadline** is a time requirement; **tardiness** is `max(0, completion - deadline)`.
- **work conservation** means an eligible resource does not remain idle while admissible work can use it.
- **isolation** limits one workload's ability to consume another workload's promised resource or latency budget.
- **admission control** rejects or reshapes demand when accepting it would invalidate guarantees.

### Central model, mechanism, or theorem

For job `i`, let arrival be `a_i`, first run `s_i`, completion `c_i`, service demand `p_i`, deadline `d_i`, and weight `w_i`. Then:

`response_i = s_i - a_i`, `turnaround_i = c_i - a_i`, and `tardiness_i = max(0, c_i - d_i)`.

A scheduling contract chooses an objective vector, such as `(deadline misses, tail response, weighted fairness, throughput, energy)`, plus hard constraints. There is generally no single scalar “best schedule.” Workload class, time horizon, overload policy, topology, and measurement semantics determine whether an apparent improvement is real.

### Critical invariants

- Only eligible, admitted work receives service, and each running task owns a valid processor context.
- Accounting charges service, wait, throttling, and interference to the intended task and control group.
- Priority, weight, budget, quota, affinity, and deadline fields have defined units, scope, and inheritance.
- Guarantees include every competing execution context and bounded blocking assumed by their analysis.
- Overload behavior is explicit: reject, throttle, shed, degrade, miss deadlines, or redistribute under policy.
- Fairness and utilization are evaluated over declared windows; short-term deviation is not silently hidden by long-term averages.
- Measurements distinguish scheduling delay from blocking, execution, device service, and application work.

### Common failures

Common mistakes are optimizing average turnaround while starving large jobs, treating 100% utilization as success, equating equal runtime with fairness, confusing nice values with reservations, promising deadlines without admission control, omitting interrupt and lock interference, ignoring heterogeneous CPU capacity, improving median latency while worsening tails, measuring only completed requests under overload, pinning for locality without capacity analysis, and presenting one synthetic trace as universal evidence.

### Compact example

Three simultaneous jobs require 6, 2, and 4 time units. First-come-first-served in that input order completes them at 6, 8, and 12, so mean turnaround is `26/3 = 8.67`. Shortest-job-first completes them at 2, 6, and 12, so mean turnaround is `20/3 = 6.67`. The second schedule improves this metric for a known finite batch, but it assumes demand is known and can starve long jobs under continuing short arrivals. An operational design must add prediction errors, response, fairness, priorities, and overload.

### Connections

[OS-014](014-context-switching.md) supplies the transfer mechanism, [OS-015](015-process-states-and-wait-queues.md) supplies eligibility transitions, and [OS-017](../ROADMAP.md) applies round-robin and priority policies. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies workload, queueing, and tail analysis; [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies requirements and assurance.

## Governing Question

The scheduler makes scarcity visible. When runnable demand exceeds processor capacity, giving service to one task delays another. Even below saturation, task placement affects cache locality, energy, thermal headroom, simultaneous multithreading interference, and wakeup response. “Run the next task” is therefore a resource-allocation decision with multiple stakeholders.

Objectives conflict. A batch order that minimizes mean completion can postpone a long job indefinitely. Rapid preemption can improve interactive response while reducing throughput. Strict isolation can leave capacity unused. Consolidating work can save energy but reduce fault and thermal margins. Security-driven core separation can sacrifice utilization.

The governing question must name the beneficiary and evidence: application request, user, tenant, control group, deadline task, whole machine, or fleet. It must also name the time window and adverse conditions. Without those, “fair,” “fast,” and “efficient” are slogans rather than testable requirements.

## Why This Matters

Scheduling affects every service-level objective above the processor. Run-queue delay contributes to request latency; throttling changes queue growth; preemption changes lock hold time; placement changes memory locality; and overload policy decides which work survives saturation.

Poor objectives can make a locally impressive system globally worse. Maximizing CPU utilization with busy low-value work increases power and delays urgent work. Minimizing average latency can hide abandoned requests. Equal shares can be unfair when tenants purchased different weights or tasks have unequal parallel efficiency.

Safety and real-time systems need feasibility, bounded interference, and defined missed-deadline behavior. Multi-tenant systems need accounting and isolation. Mobile systems care about energy and thermal constraints. General-purpose systems combine these concerns, so policy needs hierarchy and explicit trade-offs.

## Prerequisites and Retrieval

Recall runnable and blocked states from [OS-015](015-process-states-and-wait-queues.md), switching costs from [OS-014](014-context-switching.md), and shared execution contexts from [OS-013](013-threads-and-execution-contexts.md). You should understand means, percentiles, rates, queues, deadlines, weights, and feedback.

Retrieve these distinctions:

- mechanism enacts a choice; policy defines preference;
- runnable delay is not blocking time or service time;
- a priority orders contention but does not inherently reserve capacity;
- a weight expresses proportional entitlement only within a specified hierarchy and workload;
- a quota caps consumption; a reservation or admitted budget promises availability under stated assumptions;
- average, percentile, maximum observed, and proven bound are different evidence;
- processor count is not capacity on heterogeneous or thermally constrained hardware.

## Learning Objectives

After this module, you should be able to:

1. define response, turnaround, waiting, throughput, utilization, fairness, deadline, and tardiness metrics;
2. explain conflicts among latency, throughput, fairness, isolation, energy, locality, and security;
3. distinguish priority, weight, quota, budget, reservation, and admission control;
4. construct objective vectors and hard constraints for interactive, batch, multi-tenant, and real-time workloads;
5. identify denominator, censoring, overload, capacity, topology, and observer errors in measurements;
6. evaluate a policy with adversarial arrivals and mixed workload classes;
7. state where empirical tuning ends and human assurance or formal schedulability review begins.

## Core Exposition

### From goals to measurable contracts

A useful requirement states population, event boundaries, statistic, target, window, and operating conditions. “Low latency” becomes: for admitted interactive tasks under a declared load envelope, release-to-first-run latency stays below a target percentile, while batch work receives a minimum weighted share over a longer window.

Hard constraints are checked before soft optimization. CPU affinity, security domains, resource availability, deadline admission, and safety partitions can exclude placements. Among feasible choices, policy can optimize a lexicographic or weighted objective. Hiding hard constraints inside a score risks trading away correctness.

### Latency metrics

For job `i`, response begins at release `a_i` and ends at first useful execution `s_i`. Turnaround ends at completion `c_i`. Scheduler delay covers intervals when the task is runnable but not running. Blocking time covers intervals when it is ineligible. These categories require consistent transition timestamps.

Means describe aggregate work but are sensitive to workload mix and can conceal tails. Percentiles require enough independent observations, defined aggregation, and treatment of unfinished requests. Maximum observed is a sample result, not a worst-case proof. Deadline systems often count misses and maximum tardiness in addition to latency distributions.

### Throughput and utilization

Throughput depends on completed units and correctness. Dropping difficult requests can inflate apparent completion latency among survivors while reducing useful throughput. Report offered, admitted, completed, failed, canceled, and shed work.

Utilization needs a denominator. A CPU can be scheduled 100% while stalled on memory or doing retries. Heterogeneous CPUs have different capacity, frequency changes over time, and thermal limits alter sustainable service. Work conservation can improve utilization but may conflict with isolation, energy, cache partitioning, or reserved slack.

### Fairness

Equal time is one fairness definition. Proportional share allocates according to weights. Max-min fairness protects smaller demands before distributing excess. Deadline and priority systems intentionally allocate unequally. Hierarchical scheduling first divides among groups, then among tasks inside each group.

For nonnegative allocations `x_i`, Jain's index is `(sum x_i)^2 / (n * sum x_i^2)`. It ranges from `1/n` to 1, but ignores whether allocations match entitlements. Applying it to normalized shares `x_i / w_i` can test proportionality, still without measuring latency or utility.

Fairness is window-dependent. A scheduler can allow short-term bursts while converging over a longer virtual-time horizon. Too short a window mistakes granularity for injustice; too long a window hides interactive starvation.

### Priority, weights, and quotas

Priority determines precedence when tasks contend. It can cause starvation and inversion unless aging, budgets, inheritance, ceilings, or other protocols constrain it. Nice-like controls commonly influence relative share rather than guaranteeing a particular percentage.

Weights divide eligible capacity among backlogged peers under a hierarchy. Quotas cap usage during a period and can cause throttling even while the CPU is otherwise available, depending on policy. Reservations or real-time budgets require capacity supply and admission assumptions. These controls should not be described interchangeably.

### Deadlines and admission

For periodic or sporadic task `i`, execution budget `C_i`, period or minimum inter-arrival `T_i`, and relative deadline `D_i` define a demand model. A runtime interface accepting these values does not prove the model or system feasible. Analysis must include blocking, interrupts, kernel work, migration, nonpreemptive regions, and resource sharing.

Admission control protects accepted guarantees by rejecting, delaying, or reshaping new demand. Under overload, an unadmitted best-effort system must define which work degrades. Deadline misses may be counted, jobs may be dropped, quality may reduce, or a safe state may be entered.

### Interactive and batch objectives

Interactive work values quick response and bounded tails. Batch work values throughput and completion. Shortest-job policies improve mean completion when sizes are known, but estimates are imperfect and continual short arrivals can starve long jobs. Aging, attained-service policies, or reserved shares can constrain that failure.

Preemption granularity trades response against overhead and locality. Wakeup preference can reduce interactive delay but permit gaming by tasks that sleep strategically. Policy must distinguish genuine blocking from behavior intended to capture priority.

### Multicore capacity and placement

On multiple CPUs, selection and placement interact. Migration can balance load but loses cache and NUMA locality. Packing can save energy by allowing idle states; spreading can increase parallel capacity and reduce contention. Simultaneous multithreading siblings share execution structures and may be restricted for security.

Capacity-aware scheduling models CPUs with unequal performance. Energy-aware scheduling estimates energy consequences within a performance domain. Both depend on platform data and workload behavior. Incorrect topology, capacity, thermal, or utilization signals can defeat the objective.

### Isolation and hierarchy

Control groups or equivalent domains organize accounting and allocation. A hierarchy can give a tenant a share, then divide that share among its services. Quotas contain runaway demand; weights arbitrate contention; placement limits choose CPUs. Memory, I/O, and lock contention can still violate CPU-only isolation.

Isolation requires protection from uncharged work. Interrupts, soft work, kernel threads, shared caches, frequency coupling, and work performed on another task's behalf complicate accounting. A resource contract should name these exclusions or incorporate them.

### Energy, thermal, and sustainability

Running fast then idling can save energy for some hardware and workloads; spreading work can be better for others. Frequency, idle states, migration, wakeups, and memory traffic interact. Energy per completed correct unit is often more informative than instantaneous power.

Thermal throttling turns peak capacity into a temporary condition. Evaluation must run long enough to reach representative thermal state and include battery, cooling, firmware, and platform policy. Fleet objectives can also include carbon-aware timing, subject to deadlines and data locality.

### Security as a scheduling constraint

Tasks sharing a physical core, cache, or simultaneous-multithreading sibling can interfere and may form side channels. Core scheduling and domain separation can constrain co-scheduling. Security partitions reduce the feasible set and may lower utilization; treating this as a mere performance regression ignores the threat model.

Priority and quota interfaces are authority-bearing. Permissions, inheritance, delegation, and denial-of-service behavior need review. Observability data can expose tenant workload patterns.

### Feedback and stability

Schedulers use estimates of runnable demand, utilization, capacity, deadlines, or task behavior. Feedback with stale or noisy signals can oscillate: frequent migration destroys locality, load appears to move, and the controller reverses again. Hysteresis, bounded adaptation, and stable measurement windows can help.

Application autoscaling and admission controllers form additional loops around the scheduler. Local policies should be analyzed as a coupled system rather than tuned independently.

### Measurement and evidence

Measure offered load, admissions, queue depth, runnable delay, response, turnaround, completions, errors, deadline misses, CPU time, throttling, migrations, context switches, energy, frequency, and thermal state as relevant. Stratify by class and tenant; a global percentile can hide a harmed group.

Use trace replay, synthetic adversarial arrivals, production-like benchmarks, stress, and fault injection. Preserve configuration, kernel, firmware, topology, workload seed, and raw results. Compare against explicit baselines and confidence intervals where sampling applies.

### Assurance boundaries

Empirical evidence supports tuning under tested conditions. Hard real-time guarantees need schedulability analysis and platform bounds. Safety, security, labor, and tenancy fairness involve value judgments and authority beyond an algorithm. Named reviewers and acceptance owners must assess residual risk; this chapter claims no certification.

## Definitions and Notation

For each job `i`, define arrival `a_i`, first service `s_i`, completion `c_i`, required service `p_i`, deadline `d_i`, weight `w_i`, and allocated service `x_i(t)` over window `t`. Then:

- response `R_i = s_i - a_i`;
- turnaround `F_i = c_i - a_i`;
- tardiness `L_i = max(0, c_i - d_i)`;
- throughput `X = completed / window`;
- utilization `U = busy_capacity / available_capacity`, with both terms defined;
- normalized allocation `y_i = x_i / w_i` for a proportional-share audit;
- Jain index `J = (sum y_i)^2 / (n * sum y_i^2)` when all terms and the population are meaningful.

An objective vector `O = (misses, tail_R, mean_F, fairness_error, energy)` needs an ordering or weights and hard constraint set `H`. A schedule is admissible only if it satisfies `H`; optimization compares admissible schedules under `O`.

## Mechanisms, Invariants, or Proof Structure

A defensible scheduling-objective review proceeds as follows:

1. Define stakeholders, job classes, arrival and service boundaries, and workload envelope.
2. Separate hard eligibility, isolation, security, affinity, and feasibility constraints from soft objectives.
3. Define every metric's numerator, denominator, population, time window, censoring, and aggregation.
4. Trace priority, weight, quota, budget, and admission semantics through hierarchy and overload.
5. Include topology, capacity, blocking, interrupts, shared resources, energy, and thermal assumptions.
6. Test adversarial arrivals, size-estimation error, saturation, failures, and strategic behavior.
7. Label empirical results, analytical bounds, policy judgments, and external assurance separately.

The following executable model compares one metric for two schedules of a finite simultaneous batch.

<!-- bijux-verify: {"id":"toy-scheduling-objectives","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fcfs-order=A,B,C\nfcfs-mean-turnaround=8.67\nsjf-order=B,C,A\nsjf-mean-turnaround=6.67\n","stderr":""}} -->
```python
jobs = {"A": 6, "B": 2, "C": 4}

def mean_turnaround(order):
    now = 0
    completion = []
    for name in order:
        now += jobs[name]
        completion.append(now)
    return sum(completion) / len(completion)

fcfs = ["A", "B", "C"]
sjf = sorted(jobs, key=jobs.get)
print(f"fcfs-order={','.join(fcfs)}")
print(f"fcfs-mean-turnaround={mean_turnaround(fcfs):.2f}")
print(f"sjf-order={','.join(sjf)}")
print(f"sjf-mean-turnaround={mean_turnaround(sjf):.2f}")
```

The result establishes only batch arithmetic with simultaneous arrival, exact known service, one processor, no preemption, and no overhead. It does not establish fairness, online performance, deadline feasibility, or Linux policy behavior.

## Alternatives and Trade-Offs

- Mean response rewards aggregate latency but can hide tails and harmed classes.
- Tail objectives protect rare delays but need large samples and can trade throughput for slack.
- Work conservation uses idle capacity but can weaken strict isolation or energy objectives.
- Proportional sharing supports weighted fairness but does not guarantee prompt response or deadlines.
- Priority improves urgency but risks starvation and inversion without controls.
- Reservations protect admitted work but strand capacity unless reclaim is safely specified.
- Packing can save energy and cache footprint; spreading can improve capacity and fault or thermal margins.
- Affinity preserves locality; migration balances load and survives capacity changes.
- Simple policies are auditable; adaptive policies can exploit workload structure but add instability and gaming risk.

## Failure Modes and Misconceptions

1. **“The scheduler should maximize utilization.”** Busy time can be low-value, incorrect, or harmful work.
2. **“Lower average means better.”** Tails, starvation, and class-specific harm may worsen.
3. **“Equal CPU time is fair.”** Entitlements, demand, utility, and hierarchy can differ.
4. **“Nice is a reservation.”** Relative weight during contention is not guaranteed capacity.
5. **“High priority guarantees a deadline.”** Blocking, overload, interrupts, and capacity still apply.
6. **“Deadline parameters prove feasibility.”** They are claims requiring admission and complete analysis.
7. **“One CPU equals one unit of capacity.”** Heterogeneity, frequency, thermal state, and SMT contradict this.
8. **“Work conservation is always desirable.”** Isolation, security, power, and reserved slack may forbid use.
9. **“Pinning always improves latency.”** It can overload one CPU and block recovery.
10. **“Completed-request percentiles cover overload.”** Shed, canceled, and unfinished work may be censored.
11. **“Fairness at one second implies fairness.”** Results depend on the chosen window.
12. **“Fewer switches mean higher throughput.”** Blocking and prompt preemption may enable useful work.
13. **“A benchmark winner is universally best.”** Workload, topology, policy, and version bound the result.
14. **“Observed worst case is a bound.”** Tests sample behaviors; proof needs stronger assumptions and analysis.

## Worked Examples

### Example 1

For jobs A=6, B=2, and C=4 arriving together, FCFS completes at 6, 8, and 12; SJF completes at 2, 6, and 12. Mean turnaround improves, but a stream of short jobs supplies a starvation counterexample for unbounded SJF.

### Example 2

An editor and compiler contend. A short scheduling granularity improves keystroke response, while a long granularity reduces switch cost for compilation. Assign the editor a response objective and the compiler a long-window share instead of forcing one metric on both.

### Example 3

Two tenants have weights 1 and 3 and remain backlogged. The intended long-window shares are 25% and 75% within their parent allocation. A 50/50 result has perfect equality but violates weighted entitlement.

### Example 4

A group has a 50 ms quota per 100 ms period. It consumes the budget early and is throttled despite an idle CPU later. The cap provides containment, not work conservation or a latency reservation.

### Example 5

A periodic task declares `C=2 ms`, `T=10 ms`, `D=10 ms`. Feasibility analysis must add blocking and interference; accepting five such tasks merely because their nominal utilization sums to one leaves no margin for kernel or device work.

### Example 6

A placement policy moves a memory-intensive task to an idle but remote NUMA CPU. Run-queue balance improves while completion slows. Capacity, locality, migration cost, and memory placement belong in the objective.

### Example 7

A mobile system packs background work onto efficient cores so other cores enter deep idle. Under an interactive burst it expands capacity. Energy per completed request and response tails evaluate the policy better than CPU utilization alone.

### Example 8

Security policy prevents mutually distrusting tenants from sharing SMT siblings. Throughput decreases, but the schedule satisfies a hard threat-model constraint. Comparing only throughput would rank an inadmissible schedule first.

### Example 9

A service reports a better 99th percentile after overload shedding. Offered requests rose, admission fell, and rejected requests were excluded. Reporting offered, admitted, completed, rejected, and unfinished populations reveals the trade.

### Example 10

A safety controller reserves capacity and rejects noncritical work when analysis would be violated. It records deadline misses and enters a defined safe mode under platform degradation. General-purpose fairness is subordinate to the reviewed safety contract.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) develops workload models, percentiles, capacity, admission, queues, fairness, and overload across services. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects processor sharing to isolation and side-channel constraints.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder requirements, budgets, hazards, and assurance. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies topology, heterogeneous capacity, caches, SMT, power, and thermal mechanisms.

Within this program, [OS-017](../ROADMAP.md), [OS-018](../ROADMAP.md), [OS-019](../ROADMAP.md), and [OS-020](../ROADMAP.md) instantiate round-robin, priority, feedback, real-time, and multiprocessor objectives.

## References

- Linux man-pages project, [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), current page checked 2026-09-04. Policies, static priorities, nice values, preemption, CPU-time limits, autogroups, and privilege.
- Linux man-pages project, [sched_setattr(2)](https://man7.org/linux/man-pages/man2/sched_setattr.2.html), current page checked 2026-09-04. Policy attributes, utilization clamps, deadline runtime and period, flags, validation, and errors.
- Linux man-pages project, [sched_setaffinity(2)](https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html), current page checked 2026-09-04. Per-thread CPU masks, migration, permissions, intersection, and topology effects.
- Linux man-pages project, [getrusage(2)](https://man7.org/linux/man-pages/man2/getrusage.2.html), current page checked 2026-09-04. CPU time, faults, context-switch counts, scope, and accounting fields.
- Linux Kernel documentation, [CFS Scheduler](https://docs.kernel.org/scheduler/sched-design-CFS.html), current page checked 2026-09-04. Virtual runtime, ordered runnable tasks, sleeper behavior, and tunables.
- Linux Kernel documentation, [EEVDF Scheduler](https://docs.kernel.org/scheduler/sched-eevdf.html), current page checked 2026-09-04. Eligibility, virtual deadlines, lag, latency requests, and deferred dequeue behavior.
- Linux Kernel documentation, [Deadline Task Scheduling](https://docs.kernel.org/scheduler/sched-deadline.html), current page checked 2026-09-04. Runtime, deadline, period, CBS behavior, admission, migration, and bandwidth.
- Linux Kernel documentation, [Capacity-Aware Scheduling](https://docs.kernel.org/scheduler/sched-capacity.html), current page checked 2026-09-04. CPU capacity, frequency, heterogeneous systems, utilization, and placement.
- Linux Kernel documentation, [Energy-Aware Scheduling](https://docs.kernel.org/scheduler/sched-energy.html), current page checked 2026-09-04. Energy models, performance domains, utilization, capacity, placement, and limitations.
- Linux Kernel documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), current page checked 2026-09-04. CPU weights, bandwidth limits, burst, pressure, partitions, and hierarchical resource control.
- Linux Kernel documentation, [PSI — Pressure Stall Information](https://docs.kernel.org/accounting/psi.html), current page checked 2026-09-04. CPU, memory, and I/O stall measurement, averages, totals, and triggers.
- Linux Kernel documentation, [Core Scheduling](https://docs.kernel.org/admin-guide/hw-vuln/core-scheduling.html), current page checked 2026-09-04. SMT trust domains, cookies, security motivation, interfaces, and performance trade-offs.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching scheduler loops, runnable states, context switches, locks, sleep and wakeup, and multiprocessor invariants.

## Exercises

### Exercise 1

Recompute FCFS and SJF response and turnaround for A=6, B=2, C=4 arriving together. Then construct an online arrival sequence that starves a long job under strict shortest-job preference.

### Exercise 2

Write scheduling contracts for an interactive editor, batch build, multi-tenant service, and periodic controller. Define hard constraints, objective ordering, workload envelope, metrics, and overload behavior.

### Exercise 3

Audit a hierarchy where group G1 has weight 1 and G2 weight 3, while G2 contains equal-weight tasks X and Y. Derive intended shares under full contention and explain idle-capacity and quota variants.

### Exercise 4

Design an evaluation matrix for a capacity- and energy-aware scheduler on heterogeneous CPUs. Include topology, load, arrivals, thermal state, affinity, migration, SMT security, metrics, baselines, and observer effects.

### Exercise 5

Construct an assurance review for deadline tasks sharing locks and interrupts with best-effort work. Cover demand validity, admission, blocking, capacity degradation, overload, evidence, and named human judgment.

## Answers to the Exercises

### Answer 1

With simultaneous arrivals, response equals start time. FCFS A,B,C starts at 0,6,8 and completes at 6,8,12: mean response `14/3 = 4.67`, mean turnaround `26/3 = 8.67`. SJF B,C,A starts at 0,2,6 and completes at 2,6,12: mean response `8/3 = 2.67`, mean turnaround `20/3 = 6.67`.

Release long job L at time zero with demand 100, then release a demand-1 job whenever the processor is about to choose. Strict shortest-job preference keeps selecting the new short job, so L can wait indefinitely. Aging, an attained-wait bound, or a reserved share can prevent that behavior, with explicit effects on mean completion.

### Answer 2

The editor contract prioritizes release-to-first-run and input-to-render tails while guaranteeing a small long-window share to background work. The build prioritizes throughput and completion with bounded starvation. The tenant service first enforces security and group isolation, then weighted share and per-class tail latency under an admitted envelope. The controller treats feasibility, deadline misses, blocking, and safe degradation as hard concerns.

Each contract defines offered and admitted populations, service boundaries, percentiles or bounds, windows, topology, and failures. Under overload the editor degrades background work, the build lengthens completion, the service sheds by class, and the controller rejects admission or enters its reviewed safe mode. These are policy choices requiring owners.

### Answer 3

Under full contention and equal capacity, G1 receives `1/(1+3)=25%`; G2 receives 75%. Within G2, X and Y each receive half of G2, or 37.5% of the parent capacity. Directly comparing all three task weights would incorrectly flatten the hierarchy.

If G1 is idle and policy is work-conserving, G2 may borrow the remainder without changing its entitlement when G1 returns. A quota on G2 can forbid borrowing or throttle it after a period budget. A reservation for G1 needs an available capacity and admission model; weight alone does not promise 25% when the parent itself is constrained.

### Answer 4

Cross efficient and performance cores, SMT on and security-restricted, pinned and migratable placement, compute and memory workloads, bursty and steady arrivals, underload through overload, cold through thermally stable runs, and nominal versus degraded frequency. Record firmware, kernel, energy model, topology, cooling, power source, affinity, and workload seeds.

Measure offered, admitted, and completed work; class response and turnaround distributions; runnable delay; fairness error; migrations; cache behavior; energy per correct completion; frequency; temperature; throttling; and deadline misses. Compare simple fixed placements and current policy. Randomize runs, calibrate measurement power and tracing overhead, retain raw data, and avoid generalizing beyond tested machines and workloads.

### Answer 5

Validate each task's worst-case execution demand, minimum arrival separation, deadline, resource graph, and safe output. Admission includes interrupt, kernel-thread, nonpreemptive, migration, cache and TLB, extension-state, and lock interference. Apply reviewed priority inheritance or ceiling rules and bound every critical section. Reserve or isolate capacity only with platform and failure assumptions.

Define behavior for overload, CPU loss, thermal throttling, timer failure, missed releases, deadline misses, and best-effort denial. Combine schedulability analysis with stress, tracing, fault injection, and configuration control; observed maxima do not replace bounds. Named real-time, kernel, platform, concurrency, safety, security, independent-verification, and acceptance owners review assumptions and residual risk. This chapter claims no certification.
