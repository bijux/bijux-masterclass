---
module_id: OS-019
program: Operating Systems
level: 1
module_number: 19
title: Fair Scheduling
status: complete
last_verified: 2026-09-04
---

# Fair Scheduling

## One-Page Review

### Governing question

How can a scheduler divide finite processor service among competing tasks and groups according to explicit entitlements while still providing useful latency, isolation, locality, and overload behavior?

### Essential definitions

- **processor sharing** is an idealized model in which eligible tasks receive simultaneous fractional service.
- **weighted fairness** gives backlogged entity `i` a share proportional to positive weight `w_i` among peers in its allocation domain.
- **virtual runtime** is charged service normalized by weight or capacity so lagging entitled work becomes preferred.
- **lag** is the difference between service an entity should have received under a reference model and service it actually received.
- **scheduling latency** is the target horizon over which runnable entities should receive service, not an application deadline.
- **minimum granularity** limits excessively small slices and switch overhead.
- **hierarchical fairness** divides service among groups, then among their descendants, preserving administrative boundaries.
- **work conservation** uses otherwise idle capacity for eligible work; a quota or security partition may intentionally prevent it.

### Central model, mechanism, or theorem

For continuously backlogged peers with weights `w_i`, the ideal share is `s_i = w_i / sum_j(w_j)`. A virtual-time scheduler charges service `delta_i` as an increment proportional to `delta_i / w_i` and prefers an eligible entity with low virtual service or positive lag. Discrete quanta approximate the ideal; granularity, wakeups, hierarchy, capacity, and migration create bounded or measured deviation under stated rules.

Fairness is never “equal treatment” without a domain. The contract must name entities, weights, parent supply, time window, eligibility, borrowed idle capacity, and exceptions. It must also state whether the goal is proportional service, max-min allocation, bounded lag, response, or another justice criterion.

### Critical invariants

- Every eligible runnable entity has exactly one accounting identity in one scheduling hierarchy.
- Service is charged to the entity and ancestors that received it, using defined units and capacity normalization.
- Positive weights have documented scope; changing task count cannot multiply a group's parent entitlement.
- Sleep and wake placement provide latency without granting unbounded uncharged service.
- Idle-capacity borrowing does not erase entitlement or prevent a returning peer from reclaiming its share.
- Quota, throttling, affinity, deadline, and security constraints remain distinct from fair-share selection.
- Measurements include offered, eligible, throttled, and delivered populations over declared windows.

### Common failures

Common mistakes are equating equal CPU time with fairness, flattening a hierarchy, letting thread creation multiply entitlement, treating weight as reservation, measuring only long-term averages, giving sleepers unbounded credit, confusing a quota with a share, normalizing by wall time on unequal CPUs, ignoring interrupts and kernel work, assuming work conservation under security partitions, and declaring fairness from one synthetic trace.

### Compact example

Two continuously runnable tasks A and B have weights 1 and 3. Their ideal long-window shares are 25% and 75%. A discrete virtual-runtime scheduler runs the smaller normalized service value; over eight equal units it gives A two and B six. Both end with normalized service `2`. This demonstrates the arithmetic for one backlogged domain, not short-term response, hierarchy, multicore capacity, or a named kernel implementation.

### Connections

[OS-016](016-scheduling-objectives.md) defines metrics, [OS-017](017-round-robin-and-priority-scheduling.md) defines priority and quanta, and [OS-018](018-multilevel-feedback-queues.md) contrasts discrete feedback. [OS-020](../ROADMAP.md) develops scheduler measurement. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects fair CPU service to tenant admission and overload.

## Governing Question

Fair scheduling begins with scarcity and claims. If two tasks are runnable, should each receive half? What if one belongs to a tenant entitled to three times the service? What if that tenant created one hundred threads? What if one task slept for input, one is quota-throttled, and one cannot use the only idle CPU because of affinity or security?

No universal fairness rule answers all of these. Equality, proportional entitlement, max-min fairness, deadline urgency, need, payment, and safety criticality are different normative choices. The kernel mechanism must implement a declared policy while maintaining accounting and lifecycle invariants.

The governing question is how to translate a fairness definition into discrete dispatch decisions whose deviations, latency, hierarchy, borrowing, and failure behavior can be explained and measured.

## Why This Matters

Fair-share scheduling prevents a CPU-bound task from monopolizing a general-purpose machine and lets administrators divide capacity among users, services, or tenants. It supports responsiveness without requiring every normal task to carry an absolute priority.

Weak definitions create surprising harm. Per-thread fairness rewards applications for spawning threads. Long averaging windows hide starvation bursts. Sleeper bonuses can be gamed. CPU-only fairness ignores lock, memory, I/O, frequency, and interrupt interference. A weight can look like a capacity guarantee even though it only arbitrates when peers contend.

Multi-tenant and safety-relevant systems also need boundaries around fairness. Security may forbid co-scheduling. Recovery work may need reserved priority. Deadlines need admission rather than proportional share. Fair scheduling is one layer in a larger resource contract.

## Prerequisites and Retrieval

Recall objective vectors from [OS-016](016-scheduling-objectives.md), fixed-priority and RR mechanisms from [OS-017](017-round-robin-and-priority-scheduling.md), and feedback gaming from [OS-018](018-multilevel-feedback-queues.md). Understand weighted averages, trees, runnable state, affinity, and processor capacity.

Retrieve these distinctions:

- equal allocation and equitable allocation are not synonyms;
- weight determines relative contention share, not guaranteed supply;
- eligibility excludes sleeping, stopped, and throttled entities according to policy;
- fairness within a group differs from fairness between groups;
- a quota caps service while a reservation promises service under assumptions;
- service fairness, response fairness, and outcome fairness measure different things;
- ideal fluid sharing and discrete execution differ by granularity and overhead.

## Learning Objectives

After this module, you should be able to:

1. derive ideal equal and weighted shares for backlogged peers;
2. simulate normalized virtual-service selection and measure allocation error;
3. distinguish proportional, max-min, hierarchical, latency, and deadline objectives;
4. explain sleeper placement, minimum granularity, idle borrowing, and quota semantics;
5. detect thread-count, hierarchy, capacity, migration, and accounting distortions;
6. design fairness experiments across windows, workload phases, and tenant classes;
7. identify where scheduling policy requires administrative, security, or safety judgment.

## Core Exposition

### Define the allocation domain

A fair-share statement names the resource, contenders, parent domain, eligibility, and time window. “A and B are equal” is incomplete if A is a user containing ten tasks and B is one task. The scheduler can divide first among users, then among each user's tasks, or flatten all tasks; these yield different outcomes.

The resource may be CPU time, capacity-normalized service, or another accounted unit. On a heterogeneous machine, equal milliseconds need not mean equal work. On SMT siblings, simultaneous service is not independent. The definition must match the operational purpose.

### Fluid reference model

Generalized processor sharing imagines divisible service. If backlogged peers have weights 1 and 3, every instant divides capacity 1:3. Real CPUs run discrete tasks, so schedulers approximate this reference and track deviation.

The fluid model excludes switch cost, minimum execution granularity, cache effects, blocked tasks, and constraints. It is useful because it states entitlement precisely, not because hardware implements fractions of an instruction stream.

### Virtual service

Normalize executed service by weight. A task with weight 3 accumulates virtual service one-third as fast as a weight-1 task for equal physical runtime. Selecting low virtual service lets the higher-weight task run more often while normalized totals converge.

Initialization matters. Giving a waking task virtual time far behind current peers can grant a large burst; placing it far ahead damages response. Policies clamp, decay, or otherwise position sleepers to balance lag repayment against abuse.

### Lag and eligibility

Lag compares ideal entitled service with actual service while an entity is eligible under the reference model. A sleeping task may not accumulate ordinary entitlement because it did not demand CPU. A quota-throttled task is runnable in an application sense but ineligible under the CPU controller.

Eligibility definitions prevent unlimited credit during sleep. They also make metrics harder: a service dashboard needs runnable, throttled, affinity-blocked, and security-constrained intervals rather than dividing raw CPU time by wall time.

### Granularity and latency

Infinitesimal slices approximate fluid fairness but spend all capacity switching. Minimum granularity allows bounded local deviation to preserve throughput. A target scheduling horizon spreads service opportunities among runnable peers, but its exact behavior depends on task count and policy.

Scheduling latency is not an application deadline. Locks, blocking, interrupts, migration, and execution after dispatch all affect response. Fairness can bound share while still producing unacceptable tail latency.

### Hierarchical scheduling

Suppose groups G1 and G2 have equal parent weights. G1 contains one runnable task; G2 contains nine. Hierarchical fairness gives each group half, then divides G2's half internally. Flat per-task fairness gives G2 nine tenths. The correct result depends on the declared administrative entity.

Accounting must charge service to every ancestor. Moving a task between groups, creating children, deleting groups, and changing weights must preserve ownership and prevent reset-based evasion. Empty groups consume no ordinary share unless a reservation contract says otherwise.

### Idle-capacity borrowing

In a work-conserving weighted policy, a sole runnable group can use the full CPU even if its entitlement under contention is 25%. When peers return, the borrower yields future contention according to policy; borrowing does not necessarily create debt unless explicitly modeled.

Non-work-conserving reservations, quotas, partitions, or security constraints can leave capacity idle. That may be correct. Observability should attribute unused capacity to policy rather than labeling it scheduler failure.

### Weights, quotas, and reservations

Weights express relative shares among eligible siblings. A quota caps usage over a period and can throttle a high-weight group. A reservation supplies a minimum under admitted conditions. Burst allowances modify when capped service may be consumed. These controls compose but are not interchangeable.

A tenant can have weight 100 and still receive nothing if its parent is throttled or its affinity mask contains no online CPU. Conversely, it can receive all idle capacity while alone. User interfaces should state these conditional semantics.

### Max-min fairness

Max-min allocation first satisfies smaller demands, then divides remaining capacity among unsatisfied peers. A task demanding only 10% can receive 10%, leaving 90% for others rather than forcing equal 50% shares. Weighted max-min variants incorporate entitlements.

CPU schedulers often operate through time rather than a static allocation solver, but max-min reasoning helps distinguish unused demand from unfair denial. Demand estimation and nonparallel tasks complicate fleet or group placement.

### Nice values and Linux normal scheduling

Linux documents nice as affecting normal scheduling priority and describes autogroup and group interactions. CFS documentation uses virtual runtime; EEVDF documentation uses eligibility, lag, and virtual deadlines. These details are versioned implementation contracts, not proof that every generic fair scheduler behaves identically.

The mapping from nice to weight is not “one nice point equals one percent.” Per-thread Linux semantics, autogroups, cgroups, policy class, affinity, and load determine observed service. Query and measure the deployed system.

### Wakeups and interactivity

A pure long-window share can give a recently awakened task poor response. Wake placement or latency requests can favor it without granting unlimited service. The design must bound how far it may get ahead and how it repays or accounts for that preference.

Frequent short sleeps are both legitimate for event-driven tasks and a potential attack. Fairness review tests intentional boundary behavior and real interactive workloads, then reports false benefit and false penalty.

### Multicore and capacity

Fair selection and placement interact. A task cannot run on half a CPU if single-threaded, and parallel speedup can be sublinear. Per-CPU queues approximate global shares while preserving locality; balancing moves tasks and accounting state.

Capacity-aware accounting can normalize runtime by CPU performance. Frequency, thermal pressure, SMT interference, and NUMA memory make capacity dynamic. A mathematically correct virtual-time rule fed inaccurate capacity signals produces operationally unfair work completion.

### Uncharged and shared work

Interrupts, soft work, kernel threads, lock holders, and work delegated across tasks consume capacity. If service is charged to the wrong entity, one tenant can impose costs on another. CPU fairness alone also cannot compensate for memory bandwidth or I/O contention.

Define attribution and residual shared cost. Cross-resource isolation may require coordinated CPU, memory, I/O, and network controls. Perfect attribution is often impossible, so uncertainty belongs in the contract.

### Security constraints

Core scheduling or physical separation can prevent untrusted work from sharing SMT cores. This shrinks feasible placement and can strand capacity. Security is a hard constraint, not an unfairness bug to optimize away.

Weight and group-management permissions are authority. Prevent unauthorized movement, weight inflation, hierarchy creation, and observability leakage. Audit policy changes and bind them to durable tenant identity.

### Measurement and assurance

For each entity and ancestor, record eligible time, charged service, ideal share, lag, runnable delay, throttling, migrations, capacity, and completions. Evaluate multiple windows and workload phases. Include idle borrowing and returning peers.

Report offered demand, not only service. Stress task-count multiplication, wakeup gaming, group movement, quota boundaries, CPU loss, topology, and overload. Empirical fairness supports tuning; allocation policy and safety exceptions still require named human approval.

## Definitions and Notation

Let sibling entity `i` have weight `w_i > 0`, delivered service `x_i`, virtual service `v_i`, and eligibility indicator `e_i(t)`. For continuously eligible siblings, ideal instantaneous share is `s_i = w_i / sum_j(w_j)`.

For a service increment `delta_i`, a basic virtual charge is `v_i <- v_i + delta_i / w_i`. Define ideal cumulative service `g_i(t)` under the reference model and lag `lambda_i(t) = g_i(t) - x_i(t)`. Sign conventions vary, so implementations must document theirs.

For normalized allocations `y_i = x_i / w_i`, Jain's index is `J = (sum y_i)^2 / (n * sum y_i^2)`. It measures equality of normalized allocations for the selected population, not latency, utility, entitlement correctness, or moral fairness.

## Mechanisms, Invariants, or Proof Structure

A defensible fair-scheduling analysis follows seven obligations:

1. Name entities, hierarchy, resource unit, eligibility, weights, and observation windows.
2. Define the fluid or discrete reference allocation and permissible lag.
3. Define virtual charge, wake placement, granularity, and idle borrowing.
4. Prove task creation and hierarchy changes cannot multiply parent entitlement.
5. Separate weights, quotas, reservations, deadlines, affinity, and security constraints.
6. Include capacity, migration, uncharged work, overload, and cross-resource interference.
7. Recompute allocations and test adversarial traces while labeling empirical scope.

The executable model selects the task with the least normalized virtual service for eight equal units.

<!-- bijux-verify: {"id":"toy-weighted-virtual-runtime","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"timeline=A,B,B,B,A,B,B,B\nservice=A:2,B:6\nshares=A:25%,B:75%\nvirtual=A:2.00,B:2.00\n","stderr":""}} -->
```python
weights = {"A": 1, "B": 3}
service = {name: 0 for name in weights}
virtual = {name: 0.0 for name in weights}
timeline = []

for _ in range(8):
    task = min(weights, key=lambda name: (virtual[name], name))
    timeline.append(task)
    service[task] += 1
    virtual[task] += 1 / weights[task]

print("timeline=" + ",".join(timeline))
print(f"service=A:{service['A']},B:{service['B']}")
print(f"shares=A:{service['A'] * 100 // 8}%,B:{service['B'] * 100 // 8}%")
print(f"virtual=A:{virtual['A']:.2f},B:{virtual['B']:.2f}")
```

This establishes only deterministic arithmetic for two permanently eligible tasks, fixed capacity, unit slices, and no overhead. It is not CFS, EEVDF, or a multicore benchmark.

## Alternatives and Trade-Offs

- Equal share is simple but ignores differentiated entitlements.
- Weighted share encodes entitlement but does not guarantee response or minimum capacity.
- Fluid models are precise references; discrete quanta are implementable but create lag.
- Fine granularity reduces allocation error but increases switching and cache cost.
- Sleeper preference improves response but creates gaming and repayment questions.
- Hierarchy protects tenant shares but makes accounting and configuration more complex.
- Work conservation uses idle supply; strict partitions improve isolation at utilization cost.
- Capacity normalization targets work-equivalent service but depends on imperfect models.
- Global accounting improves accuracy; per-CPU structures improve scalability and locality.

## Failure Modes and Misconceptions

1. **“Fair means equal.”** Fairness can be weighted, hierarchical, max-min, deadline-based, or otherwise defined.
2. **“One task, one share.”** That rewards thread multiplication unless the intended entity is a task.
3. **“Weight guarantees capacity.”** It governs relative contention inside available parent supply.
4. **“Quota is entitlement.”** A cap can throttle without promising any minimum.
5. **“Sleeping tasks deserve accumulated CPU.”** Eligibility rules decide whether credit accrues.
6. **“Lowest virtual time always runs immediately.”** eligibility, granularity, affinity, and constraints intervene.
7. **“Long-term equality prevents starvation bursts.”** Short-window lag and response need separate limits.
8. **“Idle borrowing is unfair.”** It can be work-conserving if returning entitlements recover.
9. **“Equal milliseconds are equal service.”** CPU capacity and interference can differ.
10. **“Per-CPU fairness implies global fairness.”** placement and imbalance can violate global shares.
11. **“CPU accounting includes all imposed cost.”** interrupts and shared resources may be uncharged.
12. **“CFS and EEVDF are generic synonyms for fairness.”** They have specific documented mechanisms.
13. **“Jain index proves policy justice.”** It measures equality for chosen numeric inputs only.
14. **“A passing trace proves fairness.”** Workload, window, topology, and adversaries limit evidence.

## Worked Examples

### Example 1

A and B have weights 1 and 3 and remain runnable. Eight unit slices give 2 and 6 units, matching ideal shares. Different tie-breaking changes short order without changing this finite total.

### Example 2

Equal-weight user U has ten threads while V has one. Flat task fairness gives U ten elevenths. Hierarchical user fairness gives each user half, then divides U's half among its threads.

### Example 3

B sleeps for input while A runs alone. A borrows full CPU. When B wakes, normal weighted contention resumes; policy may place B for prompt response without retroactively charging A as wrongdoing.

### Example 4

A high-weight group exhausts a quota and is throttled. A lower-weight group uses the CPU. Selection respects eligibility: weight does not override the cap.

### Example 5

One task demands 10% and another can use all remaining capacity. Equal forced allocation wastes 40%; max-min allocation grants 10% and 90%.

### Example 6

A sleeper wakes with virtual time far behind and receives a long burst. Clamping its placement improves response while bounding how far it may lead continuously runnable peers.

### Example 7

A task receives equal runtime on a fast and slow core across two runs but completes unequal work. Capacity-normalized service explains the difference, subject to calibration and workload fit.

### Example 8

Tenant A causes network soft work charged outside its group. A CPU-time dashboard reports equal shares while B completes less work. Attribution and cross-resource metrics reveal the externalized cost.

### Example 9

Security forbids A and B from sharing SMT siblings, leaving one logical CPU idle. The allocation is admissible under the threat model even though a work-conserving unconstrained metric calls it wasteful.

### Example 10

A safety monitor receives reserved priority outside a best-effort fair hierarchy. Fair shares govern ordinary work only; the documented exception and capacity analysis protect the safety objective.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) develops tenant fairness, admission, queues, overload, and distributed allocation. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames isolation, SMT constraints, authority, and denial of service.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains heterogeneous capacity, topology, caches, NUMA, and SMT. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder requirements, budgets, hazards, and assurance.

Within this program, [OS-020](../ROADMAP.md) measures scheduler outcomes, later cgroup and container modules deepen hierarchy and isolation, and real-time modules separate proportional service from deadline guarantees.

## References

- Linux man-pages project, [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), current page checked 2026-09-04. Scheduling policies, nice, autogroups, priorities, preemption, limits, and privilege.
- Linux man-pages project, [getpriority(2) / setpriority(2)](https://man7.org/linux/man-pages/man2/setpriority.2.html), current page checked 2026-09-04. Nice values, range, scope, permissions, and Linux per-thread behavior.
- Linux man-pages project, [getrusage(2)](https://man7.org/linux/man-pages/man2/getrusage.2.html), current page checked 2026-09-04. CPU-time and context-switch accounting by process and thread.
- Linux man-pages project, [perf_event_open(2)](https://man7.org/linux/man-pages/man2/perf_event_open.2.html), current page checked 2026-09-04. Task and cgroup measurement, context-switch records, sampling, permissions, and multiplexing.
- Linux Kernel documentation, [CFS Scheduler](https://docs.kernel.org/scheduler/sched-design-CFS.html), current page checked 2026-09-04. Virtual runtime, ordered runnable entities, sleeper behavior, granularity, and group scheduling concepts.
- Linux Kernel documentation, [EEVDF Scheduler](https://docs.kernel.org/scheduler/sched-eevdf.html), current page checked 2026-09-04. Eligibility, lag, virtual deadlines, latency requests, and deferred dequeue behavior.
- Linux Kernel documentation, [Scheduler Statistics](https://docs.kernel.org/scheduler/sched-stats.html), current page checked 2026-09-04. Run, wait, wakeup, and scheduling-domain statistics with version constraints.
- Linux Kernel documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), current page checked 2026-09-04. CPU weight, max, burst, idle, partitions, hierarchy, and pressure interfaces.
- Linux Kernel documentation, [PSI — Pressure Stall Information](https://docs.kernel.org/accounting/psi.html), current page checked 2026-09-04. CPU, memory, and I/O pressure averages, totals, and triggers.
- Linux Kernel documentation, [Core Scheduling](https://docs.kernel.org/admin-guide/hw-vuln/core-scheduling.html), current page checked 2026-09-04. SMT trust domains, cookies, interfaces, limitations, and performance trade-offs.
- Linux Kernel documentation, [Capacity-Aware Scheduling](https://docs.kernel.org/scheduler/sched-capacity.html), current page checked 2026-09-04. CPU capacity, frequency, heterogeneous systems, utilization, and placement.
- Linux Kernel documentation, [Energy-Aware Scheduling](https://docs.kernel.org/scheduler/sched-energy.html), current page checked 2026-09-04. Energy models, performance domains, utilization, capacity, and placement limits.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Simple scheduler baseline, runnable state, per-CPU execution, locks, sleep, and wakeup.

## Exercises

### Exercise 1

Simulate weighted virtual service for weights 1, 2, and 5 over sixteen unit slices. Report timeline, delivered shares, normalized service, and maximum prefix deviation from ideal service.

### Exercise 2

Build a two-level hierarchy with parent weights 1:3 and three children in the second parent with weights 1:1:2. Derive full-contention shares, then analyze one idle child and a parent quota.

### Exercise 3

Compare equal share, weighted share, and max-min allocation for demands 10%, 40%, and 100% on one CPU. State the fairness interpretation of each result.

### Exercise 4

Design a fairness experiment covering task multiplication, sleepers, group movement, quotas, heterogeneous CPUs, SMT security, interrupts, overload, multiple windows, and observer effects.

### Exercise 5

Review fair scheduling for a multi-tenant platform that also hosts a safety monitor. Cover identity, hierarchy, cross-resource cost, overload, security, evidence, and human judgment.

## Answers to the Exercises

### Answer 1

The ideal shares are 1/8, 2/8, and 5/8, so over sixteen units the target totals are 2, 4, and 10. At each unit select the lowest `service/weight`, breaking ties by stable identity, then increment service. The ending normalized totals are all 2. A reproducible answer includes every prefix and computes deviation as delivered minus `t*w_i/sum(w)`.

Tie-breaking changes early prefixes; unit granularity bounds how closely the discrete schedule follows the fluid reference. A different slice size scales the deviation, and arrivals or sleeps change the eligible denominator. Ending totals alone cannot establish response behavior.

### Answer 2

Let parents P and Q have weights 1 and 3: P receives 25%, Q 75% under full contention. Q's children with weights 1,1,2 receive 18.75%, 18.75%, and 37.5% of the root. P's internal children divide its 25% according to P's local policy.

If one Q child is idle, Q's 75% is divided among remaining eligible children by their weights; a work-conserving root may also let Q borrow P's unused share. If Q has a 50% quota, it cannot realize its 75% weight once capped, and unused supply flows or idles according to root policy. Flattening child weights would violate parent isolation.

### Answer 3

Equal forced shares offer one third each, wasting about 23.33% because the first task demands only 10%. A work-conserving equal or max-min allocation first grants 10%, then divides 90% subject to remaining demand: the second reaches 40%, leaving 50% for the third. Thus max-min gives 10%, 40%, 50%.

Weighted allocation needs weights; demands alone do not define it. If weights are equal and unused entitlement is redistributed, it converges to the max-min result. Equality describes identical offered shares, max-min protects satisfied small demands while maximizing the minimum unsatisfied allocation, and weighted fairness encodes differentiated entitlement.

### Answer 4

Use stable tenant identities and compare one versus many threads at fixed group weight. Include CPU-bound peers, periodic sleepers, boundary wakeups, authorized and rejected group moves, quota exhaustion and replenishment, underload through overload, fast and slow cores, migration, thermal phases, SMT allowed and security-restricted, and high interrupt work.

Record offered and eligible demand, ancestor and child service, virtual service or lag where exposed, runnable delay, throttling, migrations, capacity, completions, cross-resource pressure, and multiple window sizes. Preserve topology, kernel, configuration, seeds, and raw traces; calibrate tracing overhead. Assert hierarchy and state invariants in addition to ratios. Results remain specific to tested workloads and system versions.

### Answer 5

Bind accounts to durable tenant groups so process creation cannot multiply parent entitlement. Define weights, quotas, borrowing, eligibility, placement, and cross-resource controls for CPU, memory, I/O, and network work. Attribute delegated and interrupt work where possible and document residual shared cost. Define overload shedding and administrative recovery capacity.

Place the safety monitor in an admitted, analyzable class or partition outside best-effort proportional fairness, with bounded blocking, interrupts, and platform supply. Enforce SMT and affinity security constraints before fair selection. Combine accounting audits, adversarial load, fault injection, and traces with safety analysis; observed ratios do not certify deadlines. Named platform, scheduler, security, tenancy, real-time, safety, independent-verification, and acceptance owners review assumptions and residual risk. This chapter claims no certification.
