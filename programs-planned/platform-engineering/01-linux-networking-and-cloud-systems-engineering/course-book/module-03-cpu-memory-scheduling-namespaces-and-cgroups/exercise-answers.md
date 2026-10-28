# Worked Answers — Module 03: CPU, Memory, Scheduling, Namespaces, and cgroups

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Load versus utilization

Load includes runnable tasks and tasks in uninterruptible sleep, often I/O waits. Many tasks may be blocked on storage, raising load while CPUs are partly idle. Inspect process states, pressure stall information, disk latency, and run queues. Do not translate load directly into a percentage or conclude that adding CPU will repair an I/O bottleneck.

## Exercise 2 — RSS sum

Shared libraries and shared pages can appear in multiple RSS values, so summing double-counts them. RSS also changes with reclaim and includes file-backed cache. Use cgroup `memory.current` for group accounting, PSS where available for proportional sharing, and host memory/pressure evidence. Choose the metric that matches the boundary being managed.

## Exercise 3 — Page cache

No. Linux uses available memory for page cache and can reclaim it. Low free memory alone is normal. Examine available memory, reclaim activity, PSI, swap, major faults, latency, and cgroup events. A problem exists when working sets contend and useful work stalls or allocations fail, not merely when cache occupies RAM.

## Exercise 4 — memory.high and memory.max

`memory.high` is a throttling/reclaim boundary intended to create pressure when exceeded; workloads can exceed it but experience reclaim cost. `memory.max` is a hard ceiling; allocations can fail and processes may be killed within the cgroup. A design can use high as an early control and max as containment, then monitor `memory.events` and PSI.

## Exercise 5 — CPU quota surprise

The unit may have `cpu.max` or systemd `CPUQuota` limiting its bandwidth independently of host capacity. Once the quota for a period is consumed, tasks wait even when other CPUs are idle. Check unit properties and `cpu.stat` throttling counters in the same interval as request latency. A quota is an isolation policy, not automatic optimal scheduling.

## Exercise 6 — PSI value

PSI estimates time during which tasks are delayed because CPU, memory, or I/O resources are unavailable. It captures contention experienced by work rather than only resource occupancy. High memory PSI can reveal reclaim stalls before an OOM event; high I/O PSI can explain latency with low CPU. Correlate it with workload and cgroup scope.

## Exercise 7 — Namespace limitation

It may retain filesystem access through mounts, network access through its network namespace or host namespace, device access, and capabilities in relevant user namespaces. A PID namespace only changes process identifier visibility and parenting. Secure isolation also requires user, mount, network, capability, seccomp, LSM, device, and resource policy.

## Exercise 8 — pids.max

A process can create many tasks that consume PIDs, kernel stacks, descriptors, scheduler work, and service-manager resources before reaching a CPU or memory ceiling. `pids.max` bounds this class of exhaustion. The application must handle thread or process creation failure, and the limit must leave room for normal helpers and shutdown.

## Exercise 9 — Descriptor exhaustion

Descriptor-creating calls fail with `EMFILE` for the process. The API may fail to accept sockets, open logs, read configuration, or create temporary files. It can appear selectively broken. Inspect `/proc/<pid>/limits`, descriptor count, errors, and leak growth. Raising the limit hides a leak unless workload evidence justifies the requirement.

## Exercise 10 — OOM evidence

A graceful exit has application signal/cleanup events and a normal wait result. An OOM kill usually shows kernel or cgroup memory events, signal-based termination, and missing user-space cleanup. Check `memory.events`, kernel journal, supervisor result, and durable state. Logs may end abruptly because the process could not flush them.

## Exercise 11 — Limit versus reservation

It caps the service but does not reserve host memory. Ancestor cgroups, other workloads, kernel memory, NUMA placement, and host pressure can make allocations fail earlier. Reservation or capacity planning is a separate responsibility. Test under representative co-tenancy and keep recovery headroom.

## Exercise 12 — Resource checkpoint

Show the effective unit/cgroup control, run a bounded CPU workload, record `cpu.stat` before and after, observe increased throttling counters, and correlate with elapsed work. A unit file line proves desired policy only. The runtime cgroup and behavior prove enforcement in that environment.
