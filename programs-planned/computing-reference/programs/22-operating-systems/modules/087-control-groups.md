---
module_id: OS-087
program: Operating Systems
level: 2
module_number: 87
title: Control Groups
status: complete
last_verified: 2026-09-04
---

# Control Groups

## One-Page Review

### Governing question

How can an operating system account for and govern shared CPU, memory, I/O and process capacity across a changing hierarchy of workloads without confusing resource policy with namespace isolation?

### Essential definitions

- A **control group**, or **cgroup**, is a node in a hierarchy that contains processes or threads and exposes resource-controller interfaces.
- A **controller** accounts for or regulates one resource domain, such as CPU, memory, I/O, PIDs, cpusets or huge pages.
- **cgroup v2** is Linux's unified hierarchy: a process has one cgroup path for all controllers attached there.
- **subtree control** selects which controllers a parent distributes to its children.
- A **weight** divides contended capacity proportionally; a **limit** bounds consumption; a **protection** biases reclamation away from selected workloads.
- **delegation** grants one manager authority over a bounded subtree without granting authority over ancestors or the delegated root's resource ceilings.
- **pressure stall information**, or **PSI**, measures time in which tasks are delayed by CPU, memory or I/O scarcity.

### Central model, mechanism, or theorem

Cgroups form a resource-distribution tree. A child cannot escape an ancestor's effective constraints, and controllers interpret configuration hierarchically. Placement identifies which tasks are charged; controller files define policy; schedulers, reclaim and I/O paths enforce it. A valid design therefore proves tree ownership, task placement, controller enablement, effective ancestor bounds and measured outcomes separately.

### Critical invariants

- Every governed task is attached to the intended leaf before untrusted work begins.
- A nonroot domain does not both hold processes and distribute domain controllers to children.
- Each subtree has one coordinating writer and an explicit delegation boundary.
- Descendants cannot raise their effective resource access above ancestor ceilings.
- Weight, protection, throttle and hard-limit semantics are never treated as interchangeable.
- Configuration changes preserve viable CPU, memory and process capacity for managers and recovery paths.
- Controller counters, events, throttling and pressure are observed at the same hierarchy level as the policy claim.

### Common failures

A manager enables controllers at the wrong parent, writes limits before moving its own process, assumes CPU weight reserves idle capacity, treats `memory.high` as an OOM boundary, sets `pids.max` without counting helper processes, delegates writable controller files too broadly, measures only host totals, or mistakes a cgroup namespace's relative paths for resource enforcement.

### Compact example

Under saturated proportional scheduling, two sibling cgroups with CPU weights 100 and 300 receive abstract shares 25% and 75%. If their parent is capped at two CPUs of runtime, their long-run shares are approximately 0.5 and 1.5 CPUs while both remain runnable. The calculation is a capacity model, not a latency guarantee: affinity, scheduler class, runnable demand and ancestor throttling still matter.

### Connections

Control groups connect scheduling, memory reclaim, block I/O, containers, systemd units, admission control, capacity planning, observability, incident response and multi-tenant security.

## Governing Question

A machine has finite resources, but its workloads change faster than static partition tables can. The governing question is how cgroups attach resource accounting and policy to a hierarchy of tasks while keeping the meaning of shares, protections and limits precise under contention and ancestor constraints.

## Why This Matters

Without resource governance, one workload can consume CPU time, trigger global reclaim, saturate storage queues or exhaust process identifiers for unrelated services. Cgroups make these effects attributable and controllable without requiring a virtual machine per workload. They underpin service managers, container runtimes and cluster schedulers.

The interface is deceptively file-like. Correctness depends on topology, controller state, task placement and kernel enforcement semantics, not merely on successful writes. A value can be accepted yet have no observable effect because there is no contention, a controller is unavailable, an ancestor dominates, or measurement is taken from the wrong node. Safe operation needs a model and evidence.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain processes, threads, scheduling classes, CPU affinity and run queues;
- distinguish virtual memory, resident memory, page cache, reclaim, swap and OOM selection;
- describe block-device queues, throughput, latency and device major/minor identifiers;
- reason about filesystem mounts, ownership, capabilities and namespaces;
- distinguish accounting, prioritization, throttling, reservation and hard exclusion.

Retrieve the running kernel configuration and version, cgroup mount type, available and enabled controllers, systemd or runtime version, delegated subtree, workload-to-cgroup mapping, CPU topology, NUMA topology, storage device mapping, swap policy and relevant BPF or LSM policy. Record inherited ancestor settings as well as the target node's files.

## Learning Objectives

After completing this module, you should be able to:

1. model cgroup v2 as a unified hierarchical resource-distribution tree;
2. create nodes, enable controllers and place tasks without violating topology constraints;
3. distinguish process-granular domain control from thread-granular threaded subtrees;
4. reason about CPU weights, bandwidth caps, affinity and throttling evidence;
5. apply memory protections, throttles, hard limits, swap policy and OOM grouping correctly;
6. configure I/O, PID and cpuset controls with device and topology awareness;
7. delegate a subtree without exposing ancestor policy or creating multiple writers;
8. validate resource policy with controller statistics, events, PSI and adversarial load.

## Core Exposition

### Treat cgroups as a hierarchy of resource domains

Each directory in a cgroup v2 filesystem is a node. Processes placed in a node contribute charges and demand according to enabled controllers. Children subdivide their parent's effective resource domain. A leaf's local value is therefore never the entire policy; every ancestor can impose a tighter bound or distribute less capacity.

### Prefer the unified cgroup v2 model

Cgroup v2 provides one hierarchy for all attached controllers, so a process has a consistent resource-domain path. Cgroup v1 can mount controllers in independent hierarchies, allowing CPU, memory and I/O membership to diverge. Mixed deployments complicate delegation and evidence. New designs should target v2 and treat v1 compatibility as an explicit migration constraint.

### Discover availability before enabling policy

`cgroup.controllers` lists controllers available for distribution by a node. `cgroup.subtree_control` lists those enabled for its children. Availability depends on kernel configuration, mounts and ancestors. Writing `+memory` at a child cannot compensate for an ancestor that did not make the memory controller available there.

### Enable controllers from the parent

A node controls resource distribution among its immediate children. Enable a controller in the parent's `cgroup.subtree_control`, then configure that controller's files on children. This orientation prevents a child from choosing whether its siblings are governed. Provision hierarchy from the delegation root downward and verify the resulting files at each level.

### Preserve the no-internal-process constraint

For domain controllers, a nonroot cgroup cannot both contain member processes and distribute controllers to children. Before enabling subtree control, move resident processes into an appropriate leaf. Child directories alone are not the conflict; the precise conflict is processes in a node whose nonempty subtree control distributes domain resources.

### Move processes through cgroup.procs

Writing a PID to `cgroup.procs` moves the entire process into the destination cgroup. New children inherit cgroup membership. Placement is a race-sensitive launch operation: create policy, attach the launcher or child at the correct synchronization point, and release untrusted code only after verifying membership.

### Use thread mode only for a real threaded domain

`cgroup.threads` and threaded cgroups allow threads of one process to occupy different cgroups for controllers that support threaded operation. `cgroup.type` describes valid domain, threaded and domain-threaded states. The topology rules are stricter than ordinary leaves. Do not use thread mode to split unrelated processes or to bypass domain-controller constraints.

### Separate membership from namespace views

A cgroup namespace changes how cgroup paths appear through procfs and mount information. It does not create a cgroup, move a process, enable a controller or impose a limit. Verify actual membership from a trusted host view and inspect controller settings; a relative path of `/` inside a container is not proof of governance.

### Model weights as contingent proportions

`cpu.weight` expresses a relative share among active siblings when CPU is contended. If only one sibling is runnable, it can use otherwise idle capacity unless another constraint intervenes. Weights neither reserve a fixed core count nor cap bursts. Comparisons are meaningful among siblings within the same parent distribution.

### Use cpu.max for bandwidth ceilings

`cpu.max` specifies quota and period for ordinary CPU bandwidth control. A quota of 50 ms per 100 ms period represents at most one-half CPU on average for the group, although execution can occur in bursts and across CPUs. A child may throttle because its own quota or an ancestor's quota is exhausted.

### Observe CPU enforcement rather than infer it

Use `cpu.stat` to inspect usage, elapsed periods and throttling, and combine it with per-cgroup CPU PSI, runnable demand and latency. A service below its quota may still suffer from affinity, a saturated ancestor, a higher-priority scheduler class or short-period burst effects. Quota arithmetic alone is not diagnosis.

### Keep affinity and cpusets distinct from bandwidth

The cpuset controller constrains eligible CPUs and memory nodes. `cpuset.cpus.effective` and `cpuset.mems.effective` reveal the effective sets after hierarchy and hotplug. A two-CPU bandwidth allowance does not guarantee two eligible CPUs; an eight-CPU cpuset does not grant eight CPUs of runtime.

### Align cpuset partitions with topology

Exclusive partitions can isolate scheduling domains when configured with valid parent relationships. CPU siblings, NUMA nodes, interrupts and kernel work still affect performance. Validate effective membership after CPU online/offline changes and preserve housekeeping capacity outside isolated workload partitions.

### Treat memory.current as charged usage, not total impact

`memory.current` reports memory charged to the cgroup and descendants under controller rules. Inspect `memory.stat` to separate anonymous memory, file cache, kernel memory and other categories. External caches, shared resources, device memory and application-level reservations may not match the number operators call “memory use.”

### Distinguish memory.min and memory.low

`memory.min` is a hard memory protection within effective hierarchical limits; `memory.low` is best-effort protection. Both are bounded by ancestors and can be proportionally distributed under overcommit. Protection affects reclaim selection—it does not allocate physical pages in advance or make protected memory available when the machine lacks capacity.

### Use memory.high as a reclaim throttle

Crossing `memory.high` puts the cgroup under heavy reclaim pressure and throttles allocating tasks. It may be exceeded under extreme conditions and does not invoke the OOM killer. This makes it useful as an operational boundary paired with monitoring and remediation, not as a hard containment claim.

### Use memory.max as the hard usage boundary

`memory.max` is the primary hard limit. If usage cannot be reduced below it, the cgroup can invoke OOM handling. Temporary breach can still occur in constrained circumstances, so observe events and outcomes. Size headroom for kernel charges, cache behavior and workload concurrency instead of equating a heap setting with the full charge.

### Define OOM scope deliberately

`memory.oom.group` asks the kernel to treat the cgroup's tasks as an indivisible workload for cgroup OOM killing, subject to protected tasks. Without coherent scope, killing one arbitrary worker can leave a corrupt or permanently degraded service. OOM grouping does not replace restart policy, durability or dependency recovery.

### Govern swap independently

Memory and swap controls distinguish resident pressure from swap consumption. Disabling or tightly limiting swap can improve predictability but turn transient pressure into earlier OOM; permitting swap can protect availability while increasing tail latency and storage load. Inspect both memory and swap events under representative faults.

### Interpret memory.events hierarchically

`memory.events` reports events including low, high, max, OOM and OOM kills for the cgroup and descendants; `memory.events.local` excludes descendants. Use the file matching the claim. A rising `high` count proves boundary crossings, not their root cause, and a parent event may be generated by one child.

### Apply I/O weights to the correct device path

`io.weight` prioritizes contending I/O, while `io.max` sets bandwidth or IOPS ceilings by device major/minor number. Effects depend on the block layer, scheduler, device and writeback attribution. Resolve logical volumes, device-mapper layers and network storage before claiming that one configured device covers the workload's actual path.

### Combine throughput limits with latency evidence

A bandwidth cap can reduce noisy-neighbor throughput yet create queues and tail latency inside the capped workload. IOPS caps treat request count separately from request size. Collect `io.stat`, device telemetry, application latency and I/O PSI. A quiet device can still coexist with a throttled descendant or an upstream storage bottleneck.

### Bound process creation with the PIDs controller

`pids.max` limits the number of tasks in a cgroup hierarchy. When the limit would be exceeded, fork or clone fails; existing tasks are not killed. Count runtime helpers, sidecars and peak thread creation. Leave a separately governed recovery path so an exhausted workload cannot prevent its supervisor from acting.

### Use event files for lifecycle state

`cgroup.events` exposes state such as `populated` and `frozen`. The populated value includes descendants and supports teardown notification. `cgroup.freeze` can suspend a subtree and `cgroup.kill` can terminate a subtree, but asynchronous state transitions and races require reading events rather than assuming a write completed the lifecycle action.

### Read PSI as time lost to scarcity

CPU, memory and I/O pressure files report `some` and, where defined, `full` stall aggregates and rolling averages. `some` means at least one task was stalled; `full` means all non-idle tasks were stalled simultaneously. PSI complements utilization: high memory pressure can reveal reclaim stalls even when a simple memory percentage looks acceptable.

### Trigger action from sustained pressure carefully

PSI interfaces can notify when stall time exceeds a threshold within a window. Select windows from the service's recovery and latency objectives, then rate-limit actions. Pressure identifies scarcity impact, not which limit to raise; blind auto-expansion can transfer harm to siblings or violate an ancestor capacity plan.

### Delegate structure, not unlimited resources

Safe v2 delegation gives a manager write access to directory creation, task migration and subtree-control interfaces for a bounded subtree. The delegator retains control over the delegated root's limits, so the delegate may divide granted capacity but not escape it. Ownership of arbitrary controller files can allow a tenant to raise ceilings and is not safe delegation.

### Enforce one writer per subtree

The kernel does not generally prevent two privileged managers from rewriting the same tree. Establish one coordinating owner at every node. On systemd systems, request a service or scope with `Delegate=` and manage only below that boundary instead of editing systemd-owned nodes directly.

### Map service-manager properties to kernel effects

systemd settings such as `CPUWeight=`, `CPUQuota=`, `MemoryHigh=`, `MemoryMax=`, `IOWeight=` and `TasksMax=` map unit policy into cgroup controls. Unit hierarchy and accounting settings can affect controller enablement. Inspect the effective cgroup filesystem and unit properties together rather than assuming a configuration file line was applied.

### Treat runtime configuration as a transaction

An OCI runtime maps `cgroupsPath` and resource settings to host cgroups, attaches processes and reports unsupported controls. Creation, update and exec operations must preserve existing container policy. A failed partial update should not leave a task in an ungoverned leaf or overwrite limits for an unrelated container sharing a path.

### Apply limits in a survivable order

When lowering capacity, first determine current usage and descendants, install observation, preserve the management process, and choose a recoverable sequence. Lowering `memory.max` below usage can force reclaim or OOM; lowering `pids.max` below current count blocks growth; reducing CPU quota can delay the very cleanup needed to recover.

### Observe the complete effective path

Record `/proc/PID/cgroup`, the target directory, ancestor controller files, effective cpusets, local and hierarchical events, resource statistics and PSI. Correlate these with a durable workload identity because PIDs and paths can be reused. Snapshot topology with the measurements so later analysis knows the applicable ancestors.

### Test under contention and failure

Generate controlled CPU, allocation, I/O and process pressure against siblings; cross soft and hard boundaries; exhaust an ancestor; hot-unplug an eligible CPU; simulate swap and storage latency; and exercise manager restart. Verify both the protected workload and the harm imposed on neighbors. Idle-host success establishes almost nothing about resource isolation.

## Definitions and Notation

Let a cgroup tree be $T=(V,E)$, rooted at $r$. For node $v$, let $A(v)$ include $v$ and every ancestor through $r$. For resource $R$, the effective ceiling is abstracted as

$$
L_R^{eff}(v)=\min_{a\in A(v)} L_R(a),
$$

when comparable hard ceilings exist. Real controllers can add aggregation, topology and reclaim semantics, so this is a reasoning bound rather than a complete kernel formula.

For saturated sibling CPU groups $S$ under parent capacity $C$, an abstract weighted allocation is

$$
x_i=C\frac{w_i}{\sum_{j\in S}w_j},
$$

for positive weights $w_i$. Recursively applying this relationship models hierarchy. It assumes continuously runnable peers and omits affinity, scheduler classes, quotas and implementation details.

For CPU quota $q$ and period $p$, define the bandwidth fraction

$$
b=\frac{q}{p}.
$$

The value $b=0.5$ means half of one CPU's runtime on average, while $b=2$ means two CPUs' worth; it does not select CPUs or bound request latency.

For a PSI observation window of duration $W$ with accumulated qualifying stall time $s$, define

$$
\rho=\frac{s}{W},\qquad 0\leq \rho\leq 1.
$$

This ratio describes stall exposure for the specified PSI condition and window, not conventional utilization.

Let $M_{min}$, $M_{low}$, $M_{high}$ and $M_{max}$ denote configured memory interfaces. Their meanings form categories—hard protection, best-effort protection, reclaim throttle and hard usage limit—not a claim that every useful configuration is a strictly ordered reservation ladder.

## Mechanisms, Invariants, or Proof Structure

Review a cgroup design with these obligations.

1. **Topology obligation:** the unified hierarchy, root, ancestors, leaves and threaded domains are explicit.
2. **Availability obligation:** every required controller is present and enabled from the correct parent.
3. **Placement obligation:** all workload processes and threads enter the intended node before execution escapes supervision.
4. **Ownership obligation:** each subtree has one writer and every delegated boundary is bounded and auditable.
5. **Hierarchy obligation:** descendant policy is evaluated under every ancestor's distribution and ceiling.
6. **Semantic obligation:** weights, protections, throttles, hard limits and affinity are labeled distinctly.
7. **CPU obligation:** shares, bandwidth, eligible CPUs, scheduler class and throttling evidence agree.
8. **Memory obligation:** charges, reclaim, protections, swap, OOM scope and recovery remain viable.
9. **I/O obligation:** device mapping, scheduler support, writeback, throughput, IOPS and latency are verified.
10. **Population obligation:** PID limits, helper headroom, freeze, kill and teardown preserve control paths.
11. **Evidence obligation:** local and hierarchical counters, events and pressure support the claimed boundary.
12. **Assurance obligation:** resource governance is not mislabeled namespace, security, latency or physical isolation.

The proof follows the path from each task to the root, intersects applicable controller policy, then tests the enforcement mechanism under demand. It separately checks who may mutate that path and whether telemetry distinguishes local effects from ancestor or sibling effects. A successful file write proves only accepted configuration.

## Alternatives and Trade-Offs

- **Cgroup v2 versus v1:** v2 supplies one coherent hierarchy and delegation model; v1 compatibility may be required by old tooling but permits divergent controller trees.
- **Flat versus nested tree:** flat siblings simplify comparison; nesting mirrors ownership and permits delegated subdivision at the cost of inherited-policy complexity.
- **Weight versus quota:** weight preserves work conservation under contention; quota supplies a ceiling but can throttle despite idle capacity elsewhere.
- **Quota period length:** shorter periods limit burst duration and add enforcement overhead; longer periods permit larger bursts and longer throttled intervals.
- **Shared CPUs versus cpuset partition:** sharing raises utilization; partitioning improves interference control while risking stranded capacity and housekeeping mistakes.
- **memory.low versus memory.min:** best-effort protection is safer under overcommit; hard protection offers stronger reclaim priority and can starve unprotected memory.
- **memory.high versus memory.max:** high provides recoverable backpressure; max supplies containment and can trigger disruptive OOM handling.
- **Swap enabled versus constrained:** swap absorbs transient pressure; tight control improves latency predictability but reduces survival margin.
- **I/O weight versus maximum:** weight redistributes a busy device; maximum bounds a workload even when capacity would otherwise idle.
- **Per-device versus end-to-end I/O policy:** per-device control is enforceable in the block layer; end-to-end objectives account for mappings and remote bottlenecks.
- **Process versus thread placement:** process placement is auditable and broadly supported; thread mode permits internal differentiation with stricter topology rules.
- **Direct cgroupfs versus systemd API:** direct access exposes exact controls; manager APIs preserve single ownership and unit lifecycle.
- **Static policy versus runtime updates:** static values are reproducible; updates adapt to demand but require transactional validation and rollback.
- **Hard admission versus overcommit:** admission protects guarantees; overcommit improves utilization and makes protection behavior workload-dependent.
- **Host-wide versus per-cgroup PSI:** host PSI shows systemic scarcity; per-cgroup PSI localizes impacted workloads but must be related to ancestors.
- **Freeze versus cooperative quiescence:** freeze is kernel-enforced and abrupt; cooperation can preserve application invariants but may fail under overload.

## Failure Modes and Misconceptions

- “A cgroup is a container.” It is a resource and accounting mechanism used by containers and other workloads.
- “A cgroup namespace applies cgroup limits.” It changes path views only.
- “Creating a directory enables every controller.” Controllers must be available and enabled by the parent.
- “A child can enable a missing controller.” Availability flows downward from ancestors.
- “No internal processes means directories cannot have both children and tasks.” The precise v2 restriction concerns distributing domain controllers while holding processes.
- “Writing a thread ID to cgroup.procs moves one thread.” It moves the process; thread placement uses the threaded interface under its rules.
- “CPU weight reserves capacity.” Weight is relative among contending siblings.
- “CPU quota pins execution.” Bandwidth and CPU eligibility are independent.
- “A quota of 200% means two dedicated cores.” It means two CPUs' worth of runtime, subject to other constraints.
- “No local throttling means no CPU ceiling.” An ancestor can throttle the subtree.
- “Configured cpus equal effective cpus.” Ancestors and hotplug determine effective sets.
- “memory.current is the application's heap.” It includes controller-defined charges and descendants, not an application-language category.
- “memory.low guarantees allocation.” It is best-effort reclaim protection.
- “memory.min creates reserved pages.” It protects charged usage within hierarchical limits; it does not preallocate memory.
- “memory.high kills the workload.” It throttles and drives reclaim without invoking OOM.
- “memory.max can never be exceeded by one byte.” Kernel enforcement can permit temporary exceptional breaches while attempting containment.
- “An OOM kill restores application correctness.” Recovery depends on group scope, durability and supervision.
- “Disabling swap always improves reliability.” It trades latency behavior for less pressure absorption.
- “I/O weights work across unrelated devices.” Weight comparison and enforcement are tied to an actual device path and implementation.
- “An IOPS cap is a bandwidth cap.” Request sizes make the two quantities different.
- “pids.max kills excess tasks.” New creation fails; existing tasks remain.
- “Freezing is instantaneous after the write.” Completion is observable through events.
- “Deleting an empty-looking leaf is safe.” Descendants, races and persistent manager state must be checked.
- “Delegation means chown every controller file.” Safe delegation limits which structural files the delegate owns.
- “Root can tolerate multiple cgroup writers.” Competing managers produce nondeterministic placement and policy.
- “A successful setting proves isolation.” Enforcement needs contention, event and neighbor-impact evidence.

## Worked Examples

### Example 1

A service and batch sibling have weights 100 and 300. Both are continuously runnable under a parent capped at two CPUs. The abstract long-run allocations are 0.5 and 1.5 CPUs. When batch becomes idle, service may consume the parent's available two CPUs because a weight is not a cap.

### Example 2

The following executable toy recursively divides saturated parent capacity by sibling weights. It validates arithmetic only, not Linux scheduler behavior, quotas, affinity, scheduler classes or latency.

<!-- bijux-verify: {"id":"hierarchical-cgroup-weight-allocation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"service=2.00\nbatch=6.00\nservice/api=1.00\nservice/worker=1.00\nbatch/etl=6.00\ntotal_leaves=8.00\n","stderr":""}} -->
```python
def distribute(capacity, weights):
    total = sum(weights.values())
    return {name: capacity * weight / total for name, weight in weights.items()}

root = distribute(8.0, {"service": 1, "batch": 3})
service = distribute(root["service"], {"api": 1, "worker": 1})
batch = distribute(root["batch"], {"etl": 1})

print(f"service={root['service']:.2f}")
print(f"batch={root['batch']:.2f}")
print(f"service/api={service['api']:.2f}")
print(f"service/worker={service['worker']:.2f}")
print(f"batch/etl={batch['etl']:.2f}")
print(f"total_leaves={sum(service.values()) + sum(batch.values()):.2f}")
```

### Example 3

A parent has `cpu.max` equivalent to one CPU and a child equivalent to two CPUs. The child's local setting does not create extra capacity: the ancestor can throttle the entire subtree at one CPU. Diagnosis must inspect both `cpu.stat` files.

### Example 4

A team wants to enable memory control for two child services, but the team cgroup still contains its manager process. Enabling `+memory` fails under the domain topology constraint. Moving the manager to a dedicated leaf makes the team node a pure distributor.

### Example 5

A cache crosses `memory.high`. Its allocations slow under reclaim, `memory.events` increments `high`, and memory PSI rises, but no OOM kill occurs. The supervisor can shed load or resize within the ancestor budget before `memory.max` becomes relevant.

### Example 6

A container has `pids.max=64` and already contains 60 tasks. Four concurrent requests each try to create two threads. Some clone calls fail when the hierarchical count reaches 64; no old thread is selected for termination. The application must handle creation failure.

### Example 7

An administrator sets `io.max` on device 253:0, but database writes ultimately reach 259:2 through device mapper. The expected limit is absent on the physical queue. Tracing the mapping and applying policy at the intended layer repairs the evidence chain.

### Example 8

A runtime owns a systemd-delegated scope. It creates container leaves below the scope and enables available controllers in its subtree. It does not rewrite the scope's own `memory.max`, which remains the host manager's ceiling over every nested container.

### Example 9

CPU utilization is only 55%, yet request latency is high and `cpu.pressure` shows sustained `some` stalls. The service is constrained to a small effective cpuset whose CPUs are busy. Host-average idle capacity does not refute local CPU scarcity.

### Example 10

Before lowering `memory.max`, an operator sees current usage above the proposed value and moves the administration agent outside the target subtree. The operator first applies `memory.high`, observes reclaim and PSI, sheds load, then lowers the hard limit. The ordered transition preserves a recovery path.

## Cross-Program Connections

- **Platform engineering:** service managers and orchestrators translate workload intent into owned cgroup subtrees and updates.
- **Systems engineering:** resource budgets, hierarchy and feedback connect component policy to whole-system behavior.
- **Security engineering:** delegation boundaries, device policy and denial-of-service controls complement access isolation.
- **Performance engineering:** scheduler shares, reclaim, queues, NUMA placement and PSI explain tail-latency interference.
- **Reliability engineering:** OOM scope, PID headroom, freeze, kill and supervisor placement determine recoverability.
- **Data engineering:** batch CPU and storage demand needs bounded interference with latency-sensitive services.
- **Distributed systems:** admission and local enforcement must agree with cluster-level requests, limits and eviction policy.
- **Observability engineering:** counters, events, PSI, topology and durable workload identity support causal diagnosis.
- **API engineering:** file and manager APIs expose stateful, hierarchical controls whose errors and partial updates matter.
- **Virtualization engineering:** cgroups govern host resources for processes and virtual-machine monitors but do not replace guest isolation.

## References

1. Linux Kernel Documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), unified hierarchy, topology, delegation and controller interfaces; retrieved 2026-09-04.
2. Linux Kernel Documentation, [PSI — Pressure Stall Information](https://docs.kernel.org/accounting/psi.html), CPU, memory and I/O stall metrics, thresholds and per-cgroup interface; retrieved 2026-09-04.
3. Linux man-pages Project, [cgroups(7)](https://man7.org/linux/man-pages/man7/cgroups.7.html), cgroup concepts, v1/v2 differences, topology, events and delegation; retrieved 2026-09-04.
4. Linux man-pages Project, [cgroup_namespaces(7)](https://man7.org/linux/man-pages/man7/cgroup_namespaces.7.html), cgroup path virtualization and namespace roots; retrieved 2026-09-04.
5. Linux man-pages Project, [systemd.resource-control(5)](https://www.man7.org/linux/man-pages/man5/systemd.resource-control.5.html), unit hierarchy and resource-control properties; retrieved 2026-09-04.
6. systemd, [Control Group APIs and Delegation](https://systemd.io/CGROUP_DELEGATION/), single-writer ownership, service and scope delegation, and integration rules; retrieved 2026-09-04.
7. Open Container Initiative, [Linux Container Configuration](https://github.com/opencontainers/runtime-spec/blob/main/config-linux.md), cgroup paths, resources, unified settings and ownership requirements; retrieved 2026-09-04.
8. Linux Kernel Documentation, [CFS Bandwidth Control](https://docs.kernel.org/scheduler/sched-bwc.html), quota, period, throttling and hierarchical bandwidth behavior; retrieved 2026-09-04.
9. Linux Kernel Documentation, [Control Groups version 1](https://docs.kernel.org/admin-guide/cgroup-v1/cgroups.html), legacy hierarchy, task attachment and controller model for migration comparison; retrieved 2026-09-04.
10. Linux man-pages Project, [proc_pid_cgroup(5)](https://man7.org/linux/man-pages/man5/proc_pid_cgroup.5.html), process membership reporting for cgroup v1 and v2; retrieved 2026-09-04.

## Exercises

### Exercise 1

A parent is capped at four CPUs. Its two continuously runnable children have CPU weights 100 and 300, and neither has a tighter quota. Compute their abstract saturated shares. What changes when the heavier child is idle?

### Exercise 2

For `cpu.max` quota 30 ms and period 100 ms, compute the bandwidth fraction. Explain two reasons a request can still experience CPU delay before the cgroup consumes that quota.

### Exercise 3

Classify `memory.min`, `memory.low`, `memory.high` and `memory.max` as protection, throttle or hard limit. State why setting all four values is not equivalent to reserving that many physical bytes.

### Exercise 4

A delegated manager needs to create child cgroups, move its processes and enable controllers, but it must not raise the subtree's host-defined ceiling. Describe the ownership boundary and topology it should receive.

### Exercise 5

Design an evidence plan for a latency-sensitive service governed by CPU, memory, I/O and PID controls. Include a test that detects an ancestor bottleneck and one that protects the recovery path.

## Answers to the Exercises

### Answer 1

The weight sum is 400. Under the abstract saturated model, the first child receives $4(100/400)=1$ CPU and the second receives $4(300/400)=3$ CPUs. These are long-run proportional shares within the parent's four-CPU ceiling, not pinned processors or latency guarantees.

When the heavier child is idle, the lighter child may use capacity left idle by that sibling, up to the parent's capacity and any other effective constraints. A CPU weight does not cap use or reserve idle cycles for an absent workload. Affinity, cpusets and scheduler class could further change observed service.

### Answer 2

The fraction is $b=30/100=0.3$, or 30% of one CPU's runtime on average. Execution can be bursty within the period; the result neither pins a CPU nor promises when the 30 ms will be scheduled.

The task can wait behind competing runnable work before exhausting quota, and an ancestor can throttle the subtree first. It can also be delayed by a narrow or busy effective cpuset, higher-priority scheduler classes, or synchronization with a throttled peer. Inspect runnable demand, effective CPU placement, ancestor `cpu.stat` and CPU PSI.

### Answer 3

`memory.min` is hard reclaim protection within hierarchical effective bounds, `memory.low` is best-effort reclaim protection, `memory.high` is a reclaim-and-throttling boundary, and `memory.max` is the hard usage limit that can lead to cgroup OOM handling. These controls have different enforcement semantics.

Protections apply to charged memory in use and are bounded or divided by ancestors; they do not preallocate pages. High and max govern usage rather than create capacity. Overcommit, reclaimability, swap, kernel charges, descendants and machine-wide availability affect outcomes, so configured numbers are not a physical reservation ledger.

### Answer 4

The host manager should create and retain policy ownership of a delegated root with the desired ancestor ceilings. It grants the delegate only the structural interfaces needed to create and remove descendants, migrate tasks and control its own subtree. Under systemd this is normally a delegated service or scope, not an independently edited slice or root node.

The delegate moves its manager and workloads into leaves so the delegated internal node can distribute controllers. It enables only controllers made available by the parent and may subdivide capacity below the root. It does not own arbitrary files on the delegated root and cannot raise the effective limit above host ancestors. One manager writes each part of the tree.

### Answer 5

Record the service PID-to-cgroup mapping, tree and delegation owner; controller availability and subtree control; every ancestor's CPU and memory ceilings; effective CPUs and memory nodes; actual block-device mapping; task count and PID ceiling. Collect `cpu.stat`, `memory.current`, `memory.stat`, memory events, `io.stat`, cgroup events and CPU, memory and I/O PSI alongside request latency and durable workload identity.

Run controlled sibling contention for CPU and I/O, allocation pressure across high and max boundaries, and a process-creation burst. To detect ancestor restriction, cap or saturate the parent while leaving the child's local setting loose, then confirm ancestor throttling or pressure and degraded child service. Keep the supervisor and load-shedding agent in a separately budgeted cgroup; verify they can observe, kill or resize the target after PID exhaustion, throttling and memory pressure. Repeat during manager restart and topology change.
