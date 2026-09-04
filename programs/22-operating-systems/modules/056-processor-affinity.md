---
module_id: OS-056
program: Operating Systems
level: 2
module_number: 56
title: Processor Affinity
status: complete
last_verified: 2026-09-04
---

# Processor Affinity

## One-Page Review

### Governing question

How should an operating system and its operators constrain a thread's eligible processors so that cache, NUMA, device, and timing locality improve without confusing eligibility with reservation, defeating load balance, or creating brittle dependencies on a changing topology?

### Essential definitions

- **Processor affinity** is the set of logical CPUs on which a thread is eligible to execute.
- A **requested mask** is the CPU set supplied by a thread, library, runtime, or administrator.
- An **effective mask** is the requested set after platform existence, online state, cpuset hierarchy, and other enforced constraints are applied.
- **Hard affinity** excludes CPUs outside a mask; **soft affinity** is a scheduler preference that may yield to stronger constraints or balancing needs.
- A **logical CPU** is one schedulable hardware thread, not necessarily one physical core.
- A **scheduling domain** groups CPUs across which the scheduler considers balancing according to topology and policy.
- A **cpuset** constrains the CPUs and memory nodes usable by a workload and can define partition boundaries.
- **IRQ affinity** selects processors eligible to receive an interrupt; it is distinct from the affinity of threads that later process the work.
- A **housekeeping CPU** handles operating-system activity intentionally kept away from isolated workload CPUs.
- **CPU capacity** is the scheduler's normalized estimate of useful compute capability and can vary across heterogeneous, frequency-scaled, or thermally constrained processors.

### Central model, mechanism, or theorem

For thread `t` at time `k`, reason from an effective eligibility set such as `E_t(k)=R_t(k) intersect C_t(k) intersect O(k) intersect P(k)`, where `R` is requested affinity, `C` is the cpuset or administrative allowance, `O` is the online CPU set, and `P` represents platform and scheduler-policy constraints. The scheduler chooses a CPU from `E`; it does not promise that the thread runs immediately, continuously, alone, or for a fixed share.

Choose a mask by minimizing a measured objective that includes migration and cache-warming cost, queueing and imbalance, NUMA and device distance, interference, heterogeneous capacity, power, and tail latency. The smallest mask is not automatically best: reducing migration can preserve warm state, but an overloaded or throttled CPU can cost more than rebuilding locality elsewhere.

### Critical invariants

- A runnable thread executes only on a CPU in its current effective affinity set.
- An accepted request is followed by a readback because silently imposed constraints can narrow the result.
- Affinity is maintained per thread; changing a process leader alone does not prove all sibling threads changed.
- CPU identifiers are treated as sparse, dynamic logical identifiers rather than dense physical-core numbers.
- Interrupts, workers, timers, per-CPU kernel work, devices, and memory placement are coordinated with application affinity.
- A nonempty desired mask has a documented response when hotplug or administrative changes make its intersection unusable.
- Isolation retains sufficient housekeeping capacity and validates that residual kernel and device work is bounded.
- Performance claims include run-queue delay, migrations, cache and NUMA evidence, CPU capacity, frequency, interrupts, and workload phase.

### Common failures

Common mistakes are calling affinity a CPU reservation, pinning only the process leader, treating logical CPUs as physical cores, parsing a configured mask without reading the effective mask, assuming CPU zero through `N-1` are online, splitting latency-sensitive threads across SMT siblings unknowingly, pinning compute while leaving IRQs and memory remote, isolating every CPU needed for housekeeping, constraining a pool until overload dominates locality, ignoring hotplug and cgroup changes, using a fixed-size mask on very large systems, and reporting throughput without queueing, frequency, thermal, or migration evidence.

### Compact example

A thread requests CPUs `{0,1,2,3}`, its cpuset permits `{1,2,3,4}`, and the online set is `{2,3,4,5}`. Its simple effective eligibility is `{2,3}`. That result says where it may run; it says nothing about when it runs, how long it waits, whether another runnable thread shares those CPUs, or whether its memory and interrupts are local.

### Connections

[OS-013](013-threads-and-execution-contexts.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), and [OS-057](../ROADMAP.md) connect affinity to threads, per-CPU ownership, shared-state traffic, memory locality, and load balancing.

## Governing Question

An affinity mask looks like a small bit set, but it sits at the intersection of scheduler policy, topology, cgroup delegation, hotplug, device routing, memory placement, and workload design. The governing question is therefore not merely which system call sets a bit. It is which processors should remain eligible, who owns that decision, how the constraint composes with stronger authorities, and what evidence shows a net benefit.

Good affinity design preserves useful locality while leaving enough placement freedom to absorb bursts, capacity asymmetry, faults, and topology change. It states failure and rollback behavior before a production incident forces the issue.

## Why This Matters

Moving a thread can evict private cache state, require translation and branch-predictor warm-up, and turn local memory or device access into remote traffic. Stable placement can reduce jitter for real-time control, network packet processing, storage queues, databases, and parallel runtimes.

Excessively narrow placement creates its own queue. A pinned thread cannot use idle capacity outside its mask, even when its chosen CPU is occupied by a higher-priority task, servicing interrupts, throttled, or thermally limited. Several supposedly isolated services can accidentally share an SMT core or last-level cache.

Affinity is also an operational contract. Container managers, batch schedulers, virtual-machine monitors, runtimes, and applications can all express masks. If their ownership and precedence are unclear, one layer silently defeats another and dashboards report configured intent rather than executable reality.

## Prerequisites and Retrieval

Review [OS-003](003-system-calls-and-user-kernel-transitions.md), [OS-013](013-threads-and-execution-contexts.md), [OS-015](015-process-states-and-wait-queues.md), [OS-016](016-scheduling-objectives.md), [OS-017](017-round-robin-and-priority-scheduling.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-033](033-translation-lookaside-buffers.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), and [OS-055](055-numa-memory-placement.md).

Retrieve these distinctions:

- a schedulable logical CPU can be one hardware thread within a physical core;
- runnable, running, eligible, reserved, isolated, and exclusive describe different states;
- cache topology, NUMA topology, device topology, and scheduler domains overlap but are not identical;
- process identifiers, thread-group identifiers, and kernel thread identifiers have different meanings;
- scheduling class and priority decide competition within eligible CPUs; affinity does not replace them;
- requested configuration can be narrowed by an administrative hierarchy and online state;
- CPU locality and physical-memory locality are independent controls;
- interrupts and deferred work can consume a CPU even when application tasks are excluded.

## Learning Objectives

After this module, you should be able to:

1. distinguish requested, allowed, online, effective, soft, hard, isolated, and exclusive CPU sets;
2. map logical CPUs to SMT siblings, cores, cache groups, NUMA nodes, devices, and capacity classes;
3. apply and verify per-thread affinity while handling dynamic mask size, permissions, inheritance, and races;
4. compose affinity with cpusets, partitions, scheduler domains, real-time policy, hotplug, and virtualization;
5. coordinate application threads with memory, interrupts, queues, workers, timers, and housekeeping;
6. choose mask width from locality, load, capacity, interference, resilience, and workload phases;
7. design experiments and assurance evidence that distinguish affinity effects from confounders.

## Core Exposition

### Affinity as eligibility

An affinity mask answers one narrow question: which logical CPUs may schedule this thread? If a mask contains CPU 4, the thread is eligible there. The mask does not allocate CPU 4, make it idle, prevent other work, guarantee a time slice, or establish a deadline.

This distinction prevents most conceptual errors. Reservation requires a capacity or admission mechanism; exclusivity requires other workloads to be excluded; isolation requires background work to be controlled; real-time guarantees require a timing model and verified interference bounds.

### Logical processors

Operating systems number logical CPUs. Two identifiers may be simultaneous multithreading siblings sharing execution resources, two separate cores sharing a last-level cache, or cores on different sockets.

Never infer physical structure from adjacent numbers. Discover topology through supported interfaces, preserve its generation, and treat identifiers as possibly sparse because firmware, boot configuration, failure, virtualization, or hotplug can leave holes.

### Requested and effective masks

The requested mask records intent. The kernel can intersect it with CPUs physically represented by the system and with a task's cpuset restriction. An empty usable intersection is rejected rather than creating a runnable task with nowhere to execute.

Read affinity back after setting it and observe the containing cpuset's effective CPUs. A successful write establishes that the request was accepted under one moment's state; concurrent hotplug or administrative reconfiguration can change later eligibility.

### Per-thread state

On Linux, affinity is a per-thread attribute. A call targeting the thread-group leader changes that one thread, not every worker already in the process.

A runtime changing a complete application must enumerate and coordinate its threads, handle arrivals and exits, and avoid racing thread creation. A safer architecture often sets affinity inside each newly created worker before it accepts work.

### Process and thread identifiers

Interfaces that use a parameter named `pid` may in practice identify a thread. Passing zero targets the calling thread; a process ID commonly identifies only its main thread. POSIX thread libraries expose a thread-handle interface for their managed threads.

Record which identity namespace an operator or container tool observes. Host, container, and library identifiers can differ, and stale identifiers can be reused after a thread exits.

### Inheritance and execution

A child created through `fork` inherits the caller's affinity, and the attribute remains across `execve` on Linux. Thread libraries generally arrange that new threads inherit the creating thread's mask.

Inheritance is useful for launching a constrained worker tree, but it can surprise a launcher whose own narrow mask leaks into unrelated helpers. Establish and verify the intended baseline before creating children, then apply role-specific masks deliberately.

### Soft affinity

Schedulers naturally prefer to keep a runnable thread near its previous CPU when doing so is compatible with fairness and load. This soft affinity preserves warm state without forbidding migration.

Soft placement is a valuable default for general services. It retains an escape route from overload, thermal throttling, or idle imbalance, whereas a single-CPU hard mask removes that option.

### Hard affinity

Hard affinity excludes all CPUs outside the effective mask. It is appropriate where device queues, licensed resources, per-CPU ownership, experiments, or carefully modeled timing require a firm boundary.

The constraint must still allow forward progress. A hard mask over one busy logical CPU can worsen latency; a mask over both SMT siblings can expose shared-resource interference; a stale mask can become invalid under hotplug.

### Mask representation

CPU masks are bit sets whose storage must cover the kernel's representable CPU range, not merely the current count of online processors. Fixed library types can be too small on large or unusually configured systems.

Use the platform's allocation and iteration helpers, size buffers defensively, retry documented size errors, and iterate only over valid returned bits. Do not build masks by shifting a machine word by an unchecked CPU identifier.

### Topology discovery

Capture possible, present, online, and isolated CPUs; SMT sibling sets; core, package, last-level-cache, and NUMA membership; scheduler capacity; and device attachment. These views can change independently.

Topology discovery belongs to configuration validation, not just initial installation. A virtual-machine resize, CPU failure, BIOS change, or kernel update can invalidate a previously sensible mask while leaving its text syntactically valid.

### SMT siblings

SMT siblings share parts of a physical core. Placing complementary threads together can improve utilization, but two execution-heavy or latency-sensitive threads can contend for issue bandwidth, caches, and other core resources.

Count physical cores and logical CPUs separately. Isolation that selects one sibling while leaving the other to general work does not isolate the physical core from interference.

### Cache and coherence locality

Keeping a thread on one CPU can retain private caches, TLB state, and predictor history. Keeping communicating threads within a shared cache can reduce data travel, while separating writers can reduce false sharing and coherence pressure.

These objectives can conflict. Producer and consumer colocation helps a shared queue, yet two compute-heavy workers may need separate cores. Use access and coherence measurements rather than a universal packing rule.

### NUMA locality

CPU affinity determines where code may execute; it does not relocate existing pages. A newly pinned worker can continue accessing memory faulted on another node.

Coordinate affinity with first touch, memory policy, page residency, migration, and device locality. Recheck after workload phases because scheduler and memory controllers that act independently can chase one another.

### Heterogeneous capacity

Not every eligible CPU necessarily has equal capacity. Architectures can mix performance classes, and frequency, power, thermal pressure, or virtualization can change delivered capacity over time.

A mask containing four logical CPUs is therefore not a stable promise of four equal units. Match latency-critical and background roles to measured capacity, then retain fallback for degraded or unavailable members.

### Scheduler domains

The scheduler organizes CPUs into topology-aware domains for balancing. Affinity limits the destinations available to a thread inside that broader structure, and cpuset partitions can reshape where balancing occurs.

Disabling balancing or creating partitions changes system behavior beyond one thread. Validate that every partition has a clear capacity owner and that imbalance cannot strand work beside idle CPUs outside its domain.

### Load balancing

Balancing migrates runnable work from busy CPUs toward idle or less-loaded eligible CPUs. A narrower affinity mask reduces candidate destinations and can create queueing even when machine-wide utilization is low.

Measure runnable time and run-queue delay alongside migrations. Fewer migrations accompanied by longer waits is not an automatic improvement; the useful objective is application service, not a counter minimized in isolation.

### Cgroup and cpuset composition

The cpuset controller provides a hierarchical administrative allowance. A child cannot grant CPUs its parent does not possess. The requested `cpuset.cpus` and read-only effective set can differ because of ancestry and online state.

Application affinity operates within this envelope. Workload managers should assign the envelope, and applications should express role-specific subsets without assuming authority to escape it.

### Cpuset partitions

A valid cpuset partition receives an exclusive CPU allocation from its parent; an isolated partition additionally disables scheduler load balancing for that partition. Requested exclusivity and effective exclusivity are distinct facts.

Partition validity can change when CPUs or ancestors change. Monitor the published state and effective sets, and treat invalidation as an operational event requiring capacity and placement reconciliation.

### CPU isolation

Isolation aims to keep unwanted work away from selected CPUs. Boot-time and cgroup mechanisms can reduce ordinary scheduler placement, but affinity is only one component.

Interrupts, kernel threads, timers, workqueues, remote callbacks, firmware activity, and SMT siblings can still disturb the physical resources. State the exact isolation boundary and measure residual activity instead of declaring a CPU silent.

### Housekeeping capacity

Housekeeping CPUs absorb general tasks, unbound work, timekeeping, management, and device activity excluded from isolated CPUs. Leaving too few housekeeping CPUs moves jitter elsewhere and can delay services needed by the isolated workload itself.

Budget housekeeping from measured peaks, failure conditions, and maintenance events. Preserve redundancy so hotplug or a device interrupt storm does not collapse the housekeeping set.

### Interrupt affinity

IRQ affinity controls which CPUs may receive a device interrupt. The effective mask can differ from the requested mask, and some interrupts are managed by the kernel or device subsystem.

Align each queue's interrupt with its consumer when cache and NUMA locality matter, but avoid concentrating all queues on one CPU. Observe actual interrupt counts per CPU and account for exceptions that cannot be freely moved.

### Managed interrupts

Managed interrupts carry device-provided affinity masks and lifecycle rules tied to queue allocation and CPU availability. Operator hints may be best-effort rather than absolute.

Design isolation around supported device behavior. A nominally isolated processor can still receive an interrupt when no suitable online housekeeping target exists or when hardware constraints require it.

### Deferred and per-CPU work

An interrupt can schedule softirq, tasklet, workqueue, polling, or kernel-thread activity on the same or another CPU. Moving only the top-half interrupt may leave the expensive work remote from the application.

Trace the complete path from hardware queue through interrupt, deferred processing, kernel worker, application thread, and memory. Each handoff has an affinity, wakeup, cache, and queueing consequence.

### Per-CPU kernel threads

Some kernel threads are bound by design because they own per-CPU duties. Others are movable or can be directed through subsystem controls. Blanket manipulation can violate kernel assumptions or merely be undone.

Use documented controls and enumerate remaining activity after configuration. Isolation assurance records unavoidable per-CPU work and its worst observed duration.

### Workqueues and timers

Unbound workqueues can execute on a configured housekeeping mask, whereas bound workers follow per-CPU semantics. Timers may be migrated under supported isolation configurations, but not every callback is freely movable.

Audit the subsystems used by the workload rather than extrapolating from an idle benchmark. Networking, storage, tracing, watchdogs, memory management, and control agents activate different paths.

### Devices and queues

Multiqueue devices often expose several interrupt and completion paths. A durable placement plan assigns queues to CPU groups, directs interrupts, maps software polling and worker threads, and locates buffers near the dominant initiator.

Queue count should match useful parallelism, not blindly match logical-CPU count. Too many queues consume vectors and memory; too few serialize work and concentrate interrupts.

### Runtime worker pools

Language runtimes and libraries can create workers after application initialization, change their number, or migrate user-level tasks independently of kernel threads. Pinning one visible thread may have little effect on actual work.

Use runtime-supported placement where available, inventory hidden pools, and make ownership explicit. Competing libraries should not each assume they own every CPU in the process mask.

### Parallel partitioning

Static partitioning assigns a worker and data shard to a CPU or locality group. It maximizes stable ownership when work is predictable, but skew leaves one worker overloaded while others cannot help.

Hierarchical work stealing can preserve local-first execution and permit controlled escape within a wider mask. The stealing policy becomes part of the locality and fairness model.

### Real-time scheduling

Affinity is essential to many fixed-priority and deadline analyses because it defines competing work and migration paths. It does not itself perform admission control or bound interrupt, kernel, firmware, or SMT interference.

For each CPU set, account for utilization, blocking, preemption, non-preemptible sections, interrupts, replenishment, and failure modes. A task pinned to an overloaded CPU remains eligible but cannot meet an impossible schedule.

### Priority and starvation

Scheduling policy and priority select among runnable threads sharing eligible CPUs. Narrow masks can concentrate high-priority work so ordinary threads receive little or no service.

Include control, logging, recovery, and teardown threads in the analysis. A service that meets its fast-path deadline but starves the thread that renews a lease or handles cancellation is not correct.

### Virtual machines and guests

A guest's virtual CPU identifiers describe a topology supplied by the hypervisor. Pinning inside the guest does not guarantee a physical core unless host vCPU placement and overcommit policy support it.

Coordinate guest vCPU, emulator, I/O, interrupt, memory, and host CPU placement. Evidence from only one layer cannot establish physical exclusivity or NUMA locality.

### Containers and orchestration

Containers usually share the host kernel and receive CPU allowances through cgroups and orchestration policy. A program can see more processors than its effective allocation if it queries the wrong interface.

Size pools from effective availability and quota as well as affinity. A mask of four CPUs with a one-CPU bandwidth quota permits location on four CPUs but does not provide four CPUs of compute time.

### CPU bandwidth controls

Affinity constrains place; bandwidth or quota controls constrain time. They compose but answer different questions. A thread can be pinned to an idle-looking CPU and still be throttled by its cgroup budget.

Collect throttling time and quota periods when evaluating affinity. Otherwise tail latency attributed to cache migration may actually be budget exhaustion.

### Power and thermal behavior

Packing work can let other cores enter deep idle states, while spreading work can increase throughput or reduce local thermal pressure. Frequency selection and package power limits couple neighboring cores.

Record frequency, throttling, temperature, and power policy during experiments. Repeating the same mask after thermal equilibrium can yield a different result from a short cold run.

### Hotplug

CPU hotplug changes online eligibility, migrates movable tasks, and invokes subsystem callbacks to drain or recreate per-CPU state. A desired mask can lose members even when its stored configuration remains unchanged.

Controllers subscribe to topology changes, recompute effective placement, and preserve at least one safe destination. Teardown waits for threads, interrupts, timers, workers, and per-CPU references to leave before considering a CPU unavailable.

### Empty intersections

A request whose intersection with present and permitted CPUs is empty fails. Administrative updates also need rules that prevent populated cgroups from becoming unrunnable or define how they inherit usable CPUs.

Validate intersections before rollout, but still handle races. A robust service reports the requested, allowed, online, and effective sets and enters a documented safe mode rather than spinning on a rejected mask.

### Permissions and delegation

Changing another thread's affinity requires an ownership relationship or privilege. Cgroup delegation separately governs who may change the administrative envelope.

Minimize privilege by letting the resource manager configure cpusets and letting each worker set its own subset. Audit changes because affinity can affect both availability and tenant isolation.

### Configuration ownership

Choose one authority for allocation of CPU groups and define which layers may narrow them. For example, an orchestrator owns tenant envelopes, a runtime owns worker-role subsets, and individual libraries merely observe.

Without ownership, startup order becomes policy: the last writer wins within constraints. Persist desired and observed masks with actor, reason, topology generation, and expiration or rollback conditions.

### Dynamic adaptation

An adaptive controller can widen or shift masks when run queues grow, locality degrades, CPUs fail, or capacity changes. Every move incurs warm-up and risks synchronized oscillation with load balancing or NUMA migration.

Use stable measurement windows, hysteresis, minimum residence time, bounded change size, and a single coordinating authority. Compare projected remaining benefit against migration and interference cost.

### Observation

Record requested and effective masks per thread; current and recent CPUs; voluntary and involuntary context switches; migrations; run-queue delay; utilization; scheduling class; priority; throttling; and wakeup paths.

Join those data with topology, frequency, capacity, cache misses, coherence, NUMA access, page residency, interrupts, softirqs, workqueues, and application latency. A CPU number without its topology generation is ambiguous evidence.

### Experiment design

Compare an unconstrained baseline, topology-aware broad masks, narrow masks, and deliberately adverse placement. Hold workload, data, compiler, kernel, firmware, power policy, quotas, interrupts, memory policy, and warm-up constant where possible.

Test idle and contended hosts, balanced and skewed work, short and long phases, hot and cold caches, SMT enabled and disabled, hotplug, throttling, and device bursts. Repeat in randomized order and preserve raw traces and uncertainty.

### Rollback and teardown

Rollback restores a known-good mask, cpuset structure, IRQ routing, workqueue mask, memory policy, and runtime configuration in a deliberate order. Widen application eligibility before removing its last currently usable CPU.

Teardown stops arrivals, drains work, joins workers, redirects interrupts and timers, releases per-CPU ownership, and only then dismantles partitions. Verify observed state because asynchronous migration can outlive the configuration write.

### Assurance

Assurance ties each placement claim to an invariant and observable evidence. Review roles include scheduler and kernel specialists, runtime owners, device and NUMA experts, performance engineers, and service operators.

Record unsupported hardware behavior, managed-interrupt limitations, firmware noise, virtualization, and counter uncertainty. Passing a deterministic mask calculation is evidence for set composition only, not proof of production latency or isolation.

## Definitions and Notation

Let `U(k)` be the logical CPUs represented at time `k`, `O(k)` the online subset, `R_t(k)` thread `t`'s requested affinity, `C_t(k)` its cpuset allowance, and `E_t(k)` its effective eligibility. A useful simplified relation is:

`E_t(k)=R_t(k) intersect C_t(k) intersect O(k) intersect U(k)`.

Let `q(c,k)` be queueing cost on CPU `c`, `m(t,c_old,c)` the migration and warm-up cost, `d(t,c)` the NUMA and device-distance cost, `i(t,c)` interference, and `h(c,k)` effective capacity. A placement controller can compare candidates through a measured objective such as `J(t,c)=q+m+d+i+service_penalty(h)`, subject to `c in E_t(k)` and scheduling-policy constraints. This is a decision model, not a claim that one scalar perfectly predicts a real scheduler.

Affinity is **per-thread** eligibility. A cpuset is an administrative CPU and memory envelope. An exclusive partition allocates processors between cpuset partitions. An isolated partition disables load balancing within its allocated set. A CPU reservation allocates capacity under an admission or ownership policy. These terms are not interchangeable.

## Mechanisms, Invariants, or Proof Structure

1. **Discover topology.** Capture possible, present, online and isolated CPUs, SMT, cores, caches, packages, NUMA nodes, capacities, devices, virtualization, and generation.
2. **Identify ownership.** Assign the resource manager, runtime, device subsystem, and application distinct authority over envelopes and subsets.
3. **Classify threads.** Separate latency-critical, throughput, housekeeping, control, interrupt, polling, worker, and recovery roles.
4. **Define constraints.** Record cpusets, quotas, scheduling classes, priorities, permissions, hotplug policy, and failure destinations.
5. **Choose topology groups.** Select masks by core, shared cache, node, device, and capacity rather than adjacent identifiers.
6. **Coordinate the path.** Align tasks, IRQs, deferred work, queues, memory, and devices where the workload requires locality.
7. **Apply per thread.** Set new workers before admission, cover hidden pools, handle dynamic mask sizes, and avoid enumeration races.
8. **Read back reality.** Verify per-thread effective affinity, cpuset effective CPUs, partition state, IRQ routing, and current topology.
9. **Test forward progress.** Exercise overload, quota exhaustion, high priority, hotplug, empty intersections, control paths, and teardown.
10. **Measure outcomes.** Observe queue delay, migrations, cache, NUMA, interrupts, capacity, power, throttling, latency, and throughput.
11. **Adapt conservatively.** Use hysteresis, residence time, bounded moves, and one coordinator across placement controllers.
12. **Retain evidence.** Preserve masks, topology generation, configuration actors, raw traces, failures, rollback, reviewers, and limitations.

<!-- bijux-verify: {"id":"processor-affinity-intersection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requested=0,1,2,3\ncpuset-allowed=1,2,3,4\nonline=2,3,4,5\neffective=2,3\nplacement-guaranteed=False\n","stderr":""}} -->
```python
requested = {0, 1, 2, 3}
cpuset_allowed = {1, 2, 3, 4}
online = {2, 3, 4, 5}
effective = requested & cpuset_allowed & online

def display(cpus):
    return ",".join(str(cpu) for cpu in sorted(cpus))

print(f"requested={display(requested)}")
print(f"cpuset-allowed={display(cpuset_allowed)}")
print(f"online={display(online)}")
print(f"effective={display(effective)}")
print("placement-guaranteed=False")
```

The executable example verifies deterministic set intersection. It does not invoke an affinity interface, observe a scheduler, model every platform constraint, reserve processor time, test cgroups or hotplug, or establish performance and isolation.

## Alternatives and Trade-Offs

- Soft affinity retains locality while permitting escape from overload; hard affinity gives a firm boundary and can strand work.
- One-CPU masks minimize voluntary migration but eliminate placement redundancy; wider masks increase balancing choices and may require warm-up.
- Packing communicating threads in one cache domain reduces transfer distance but increases shared-cache contention; spreading them provides resources and raises communication cost.
- Using both SMT siblings increases logical concurrency but shares a physical core; selecting one sibling per core improves interference isolation and leaves capacity unused.
- NUMA-local masks reduce remote access when pages are local; wider cross-node masks absorb load and can detach computation from its memory.
- Static worker ownership preserves cache state but suffers under skew; work stealing balances skew and introduces movement and synchronization.
- Exclusive cpuset partitions provide strong allocation boundaries but reduce global fungibility; ordinary cpusets allow more flexible sharing.
- Isolated partitions and boot controls reduce scheduler noise but increase housekeeping complexity; default balancing is simpler and less deterministic.
- Aligning IRQ and consumer improves cache and device locality but risks hotspotting; spreading queues increases throughput and coordination.
- Runtime-managed affinity understands worker roles but can conflict with orchestration; external management sees tenancy and may not understand application phases.
- Adaptive masks respond to failures and load but can oscillate; static masks are reproducible and become stale.
- High-performance CPUs reduce critical-path time but may consume more power or be scarce; efficient CPUs preserve power budget and can miss latency goals.
- Guest pinning controls virtual placement only; host pinning adds physical control and operational coupling.
- Narrow real-time partitions simplify interference analysis but reduce recovery capacity; broader eligibility improves failover and expands the interference set.

## Failure Modes and Misconceptions

- **“Affinity reserves a CPU.”** It limits eligibility and does not allocate time or exclude competitors.
- **“A successful set call guarantees the exact requested mask.”** Administrative and physical constraints can silently narrow usable CPUs.
- **“Process affinity changes every thread.”** Affinity is per thread on Linux.
- **“CPU count implies identifiers zero through count minus one.”** Identifiers can be sparse or offline.
- **“Adjacent CPU numbers are separate cores.”** They may be SMT siblings or cross a topology boundary.
- **“No migrations means good performance.”** Queueing, throttling, interference, and remote memory can dominate.
- **“Pinning compute makes memory local.”** Existing pages and device buffers remain where they were placed.
- **“Moving an IRQ moves all its work.”** Deferred processing and workers can run elsewhere.
- **“An isolated CPU is silent.”** Kernel, device, firmware, and sibling activity can remain.
- **“Four eligible CPUs equal four CPUs of capacity.”** Capacity, quota, SMT, frequency, and contention differ.
- **“The configured cpuset is the effective cpuset.”** Hierarchy and hotplug can change the effective set.
- **“A fixed-size bit mask handles every server.”** Kernel CPU ranges can exceed common static types.
- **“Real-time priority plus pinning guarantees a deadline.”** Admission, blocking, interrupts, and hardware interference still matter.
- **“The best benchmark mask is permanently best.”** workload phase, topology, thermal state, and competitors change.
- **“Removing affinity is a complete rollback.”** IRQs, workers, partitions, memory, quotas, and runtime state may still reflect the policy.

## Worked Examples

### Example 1

A thread requests CPUs 0 through 3, but its cgroup permits 1 through 4 and only 2 through 5 are online. Readback shows `{2,3}`. The application treats that as eligibility and separately observes queueing and runtime.

### Example 2

A packet queue's interrupt, polling thread, and buffer pages are placed near one NUMA-local core group. Throughput improves until all queues target the same group; spreading queue groups restores capacity without abandoning locality.

### Example 3

A service pins its main thread and leaves eight runtime workers unconstrained. Scheduler traces show the workers perform nearly all computation. Worker-init hooks apply role masks before accepting requests.

### Example 4

Two latency-sensitive threads are assigned CPU 8 and CPU 9 because their identifiers look separate. Topology shows they are SMT siblings. Moving one to a different physical core reduces tail interference.

### Example 5

A database worker moves from node 0 to node 1 but retains a large node-0 heap. The team either restores CPU locality or deliberately migrates and repopulates pages after estimating the remaining phase benefit.

### Example 6

A four-CPU affinity mask runs inside a one-CPU cgroup quota. The threads rotate across four locations but are throttled after consuming one CPU's budget. Quota, not eligibility, explains the latency spikes.

### Example 7

An isolated partition leaves one housekeeping CPU for storage, networking, logging, and management. A device storm overloads it and delays control traffic. The corrected plan reserves redundant measured housekeeping capacity.

### Example 8

A hot-unplug event removes the sole CPU in a desired single-CPU mask. The controller widens to a prevalidated sibling-core fallback, confirms the new effective mask, and records lost isolation until repair.

### Example 9

A guest pins a worker to virtual CPU 2, but the host overcommits that vCPU with unrelated guests. Coordinated host vCPU and memory placement is needed before claiming physical isolation.

### Example 10

An adaptive controller alternates a worker between two cache domains whenever a short queue sample changes. Minimum residence time, confidence intervals, and a migration-cost threshold stop the oscillation.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects logical CPUs, SMT, caches, coherence, NUMA, interrupts, heterogeneous capacity, power, and thermal limits. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects worker pools, partitioning, work stealing, ownership, synchronization, and scheduling.

[Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) connects virtual CPUs, tenancy, orchestration, quotas, placement, and noisy neighbors. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies constraints, interacting control loops, lifecycle analysis, assurance, and trade studies. Within this program, [OS-055](055-numa-memory-placement.md) covers memory locality, [OS-057](../ROADMAP.md) covers multicore load balancing, and [OS-060](../ROADMAP.md) covers contention diagnosis.

## References

- Linux man-pages project, [sched_setaffinity(2)](https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html), current page checked 2026-09-04. Per-thread masks, effective intersections, migration, permissions, inheritance, errors, and large masks.
- Linux man-pages project, [pthread_setaffinity_np(3)](https://man7.org/linux/man-pages/man3/pthread_setaffinity_np.3.html), current page checked 2026-09-04. POSIX-thread affinity interfaces, mask size, errors, inheritance, and thread handling.
- Linux man-pages project, [CPU_SET(3)](https://man7.org/linux/man-pages/man3/CPU_SET.3.html), current page checked 2026-09-04. Static and dynamically allocated CPU-set macros, sizing, iteration, and set operations.
- Linux man-pages project, [cpuset(7)](https://man7.org/linux/man-pages/man7/cpuset.7.html), current page checked 2026-09-04. CPU and memory constraints, affinity composition, hierarchy, scheduler balancing, and hotplug behavior.
- Linux man-pages project, [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), current page checked 2026-09-04. Scheduling policies, priorities, real-time behavior, reset rules, autogroups, and affinity interfaces.
- Linux kernel documentation, [SMP IRQ affinity](https://docs.kernel.org/core-api/irq/irq-affinity.html), current page checked 2026-09-04. Default, requested, and effective interrupt masks and per-IRQ controls.
- Linux kernel documentation, [Reducing OS jitter due to per-CPU kthreads](https://docs.kernel.org/admin-guide/kernel-per-CPU-kthreads.html), current page checked 2026-09-04. Per-CPU kernel-thread sources, affinity, offloading, interruption, and jitter limitations.
- Linux kernel documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), current page checked 2026-09-04. Hierarchical cpuset requests, effective CPUs, exclusive allocations, partitions, isolation, and hotplug effects.
- Linux kernel documentation, [Capacity Aware Scheduling](https://docs.kernel.org/scheduler/sched-capacity.html), current page checked 2026-09-04. CPU capacity, frequency invariance, asymmetric systems, utilization, energy, and scheduler topology.
- Linux kernel documentation, [CPU hotplug in the kernel](https://docs.kernel.org/core-api/cpu_hotplug.html), current page checked 2026-09-04. CPU masks, online and offline operations, callbacks, failure, synchronization, and per-CPU lifecycle.

## Exercises

### Exercise 1

Design processor placement for a NUMA network service with eight receive queues, polling threads, compute workers, shared control threads, and a latency objective. Include masks, interrupts, memory, overload, and rollback.

### Exercise 2

Given 32 logical CPUs arranged as two sockets, eight physical cores per socket, and two SMT siblings per core, compare masks for a compute-bound job, a cache-sharing pipeline, and a latency-critical control loop.

### Exercise 3

Specify an affinity controller that remains safe through cgroup changes, thread creation and exit, CPU hotplug, quota throttling, heterogeneous capacity, and partial configuration failure.

### Exercise 4

Construct an experiment that determines whether a narrow affinity mask improves a service. Identify baselines, confounders, metrics, adverse cases, and evidence limitations.

### Exercise 5

Audit the claim: “This container has four dedicated CPUs and therefore four CPUs of guaranteed compute.” State what must be inspected and what conclusions each observation permits.

## Answers to the Exercises

### Answer 1

Discover CPU, core, SMT, last-level-cache, NUMA, NIC, queue, and capacity topology. Allocate queue groups across physical cores local to the NIC, place each receive interrupt and polling thread in its group's mask, first-touch or bind its buffers within the corresponding allowed NUMA nodes, and let compute workers use a wider local-node mask with local-first work stealing. Keep control, logging, and recovery threads on redundant housekeeping CPUs outside the polling cores.

Budget each queue from measured peak packet rate and preserve spill behavior when one queue is skewed. Observe requested and effective thread masks, IRQ effective affinity, per-CPU interrupts and softirqs, queue occupancy, run-queue delay, migrations, cache and NUMA events, drops, throughput, and tail latency. Test device bursts, one failed CPU, a failed queue, quota pressure, and housekeeping overload. Rollback first widens application masks, redirects queues and interrupts, drains polling, restores memory and runtime policy, then removes partitions; every stage is read back.

### Answer 2

For the compute-bound job, begin with one logical CPU per physical core across the smallest NUMA region holding its memory. This avoids SMT competition; add siblings only after measuring whether extra logical concurrency helps. If the job needs more capacity than one socket or its memory is interleaved, use topology-balanced groups across both sockets and coordinate page placement.

For the pipeline, place tightly communicating adjacent stages on separate physical cores sharing a last-level cache, unless execution-resource or cache-capacity measurements favor separation. Keep a wider cache-domain mask for controlled failover. For the control loop, use a physical core whose SMT sibling is also excluded from unrelated work, direct movable interrupts and kernel work away, reserve housekeeping capacity, perform timing admission, and retain a prevalidated fallback core. Identifier adjacency alone never selects these masks; discovered topology does.

### Answer 3

The resource manager owns cpuset envelopes and publishes topology generations; the runtime owns per-role subsets. New workers set and read back their affinity before accepting work, while an event loop reconciles thread births, exits, effective cpusets, partition validity, online CPUs, capacity, and quota. Every desired mask includes a ranked fallback that intersects the currently effective envelope, and updates are generation-checked so stale observations cannot overwrite newer topology.

Use a transaction-like rollout: validate nonempty intersections and housekeeping reserve, widen fallback destinations, move threads and related IRQ or worker paths, verify observations, then remove obsolete CPUs. On partial failure, retain at least one known-good destination and report desired versus observed state. Hysteresis and minimum residence time limit adaptation; throttling is diagnosed separately from placement. Hotplug and cgroup events trigger reconciliation, not blind replay of stored identifiers, and teardown drains per-CPU ownership before removing partitions.

### Answer 4

Compare unconstrained scheduling, a topology-aware broad mask, the proposed narrow mask, and an adverse remote or SMT-sharing mask. Preserve binaries, inputs, request sequence, data placement, kernel, firmware, topology, cpuset, quota, scheduling policy, IRQ routing, runtime pool size, memory policy, power policy, and ambient load. Randomize run order, separate warm-up from steady state, repeat enough times to estimate variation, and test both idle and contended machines.

Collect effective masks per thread, current CPUs, migrations, run-queue delay, context switches, throttling, frequency, thermal pressure, cache and coherence events, NUMA accesses, interrupts, softirqs, workqueue activity, throughput, tail latency, deadline misses, energy, and recovery behavior. Exercise skew, bursts, SMT competition, hotplug, quota exhaustion, and device traffic. Attribute improvement only when service metrics change consistently with locality evidence; a lower migration count alone is insufficient, and results remain specific to the measured topology and workload phases.

### Answer 5

Inspect the container's requested and effective cpuset, exclusive and partition state, online CPUs, CPU quota and weight, host topology, SMT siblings, competing host tasks, guest or hypervisor mapping, scheduling classes, interrupts, kernel work, and runtime thread masks. Four identifiers prove at most four eligible logical CPUs. They may represent two physical cores, unequal capacities, or virtual CPUs sharing host processors.

An effective exclusive partition supports an allocation-boundary claim against tasks outside the partition, subject to its validity and kernel semantics. It does not by itself eliminate interrupts, firmware, SMT-sibling interference, or time quotas. A full four-CPU quota permits up to the configured bandwidth but does not prove immediate service; real-time guarantees need admission and bounded interference. Only coordinated host allocation, quotas, topology, device and kernel isolation, measured residual activity, and failure analysis can support a carefully scoped dedication or capacity claim.
