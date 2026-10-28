# Module 03 — CPU, Memory, Scheduling, Namespaces, and cgroups

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** How does the kernel share finite host resources, and how can one workload be bounded without making false isolation claims?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Publish and exercise a resource envelope for Atlas using cgroup v2 and systemd resource controls, with explicit throttling and memory-failure behavior.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Distinguish CPU time, load average, utilization, run-queue pressure, and throttling.
- Explain virtual memory, resident memory, page cache, swap, overcommit, and out-of-memory selection.
- Read cgroup v2 hierarchy, controller, and pressure evidence.
- Use namespaces and cgroups as mechanisms without calling them complete security boundaries.
- Choose CPU, memory, task, and file-descriptor limits from workload evidence.
- Demonstrate bounded failure and recovery with safe stress fixtures.

## Capstone increment

Publish and exercise a resource envelope for Atlas using cgroup v2 and systemd resource controls, with explicit throttling and memory-failure behavior.

## Capacity is finite even when the abstraction is convenient

A host has finite CPU time, memory, tasks, descriptors, I/O bandwidth, and kernel structures. An application can be correct in isolation and still make the host unusable by consuming an unbounded share. Resource engineering begins by naming which quantity is constrained and what should happen at the boundary.

Atlas defines separate envelopes for API, worker, and edge. The values in the example units are teaching defaults, not capacity recommendations. A real value must come from workload evidence and leave headroom for the kernel, service manager, logging, and recovery.

## CPU observations are easy to misread

CPU utilization reports how much time processors spent in categories over an interval. Load average estimates runnable and uninterruptible work, not percentage CPU. A load of four means something different on a two-CPU host and an eight-CPU host. A task blocked in uninterruptible I/O can raise load without consuming CPU.

The scheduler chooses runnable tasks. Nice values influence policy but are not hard ceilings. CPU affinity restricts eligible CPUs. cgroup CPU weight distributes contention; CPU quota imposes a bandwidth ceiling over a period. A quota can produce throttling and tail latency even while host-wide CPU utilization appears moderate.

Use:

```bash
cat /proc/loadavg
cat /proc/stat
ps -eo pid,psr,stat,ni,pcpu,comm
cat /sys/fs/cgroup/<group>/cpu.stat
```

Look for `nr_throttled` and `throttled_usec` when testing a quota hypothesis.

## Virtual memory separates address space from residence

A process can reserve a large virtual address range without holding the same amount of physical memory. Resident set size approximates pages currently resident for a process but includes shared and file-backed pages in ways that complicate summation. Proportional set size can allocate shared pages proportionally when available.

The page cache uses otherwise available memory to cache file data. “Free memory is low” is not automatically pressure. Pressure appears when useful working sets compete, reclaim increases, swap or writeback dominates, latency rises, and allocations fail.

Linux overcommit policy influences whether reservations are accepted. The OOM killer acts when the kernel cannot satisfy memory needs; it selects victims using scores and context. A service killed by the OOM killer did not exit through its graceful signal path.

Inspect:

```bash
cat /proc/meminfo
cat /proc/<pid>/smaps_rollup
cat /proc/pressure/memory
cat /sys/fs/cgroup/<group>/memory.current
cat /sys/fs/cgroup/<group>/memory.events
```

## cgroup v2 is a hierarchy

cgroup v2 organizes processes into one hierarchy. Controllers distribute or limit resources along that hierarchy. A child cannot escape a limit imposed by an ancestor. systemd creates and owns cgroups for units and slices, so modifying cgroup files behind systemd without understanding ownership can be overwritten or create inconsistent policy.

Important controls include:

- `memory.max` for a hard memory boundary;
- `memory.high` for reclaim pressure before the hard boundary;
- `cpu.max` for quota and period;
- `cpu.weight` for relative share;
- `pids.max` for task count;
- `io.max` and `io.weight` where supported;
- pressure stall information for time lost waiting on resources.

A limit is not a reservation. `MemoryMax=512M` does not guarantee 512 MiB will be available when the host is already exhausted.

## Namespaces change views, not all authority

PID, mount, network, IPC, UTS, user, time, and cgroup namespaces provide scoped views or identifiers. They are foundational container mechanisms, but a namespace alone does not create a secure container. Processes still share one kernel; capabilities, seccomp, LSM policy, filesystem mounts, cgroups, and device access matter.

Course 3 will combine these mechanisms under OCI. Here, use `unshare` only to observe the primitive:

```bash
unshare --user --map-root-user --pid --fork --mount-proc sh
```

Whether that command is permitted depends on kernel and distribution policy. An unavailable unprivileged user namespace is an environment fact, not proof that namespaces do not exist.

## Resource limits have failure semantics

A useful resource policy specifies behavior at the boundary:

- CPU quota: requests become slower; readiness may remain true if latency is still acceptable.
- memory high: reclaim increases; monitor pressure and latency.
- memory max: allocation may fail or a process may be killed within the cgroup.
- task max: new threads or processes fail.
- descriptor limit: `open`, `accept`, or other descriptor-creating calls fail with `EMFILE`.
- disk quota: writes fail with `ENOSPC` or quota-specific errors.

The application must handle expected failures. A supervisor restart cannot repair a deterministic memory limit exceeded on every request.

## Worked investigation: green host, slow API

Suppose host CPU utilization is 45%, but Atlas p99 latency doubles. The API unit's `cpu.stat` shows increasing throttled time. The host has spare CPUs, yet `CPUQuota=50%` limits the unit to half of one CPU on average.

The correct response is not necessarily to remove the quota. Determine whether the quota was intended, whether the workload changed, and whether scaling or optimization is preferable. Record the offered workload, unit quota, throttling counters, request latency, and host utilization in the same interval.

## Bounded stress, not destructive stress

The course resource fixture allocates a bounded amount of memory and sleeps briefly under a transient user unit. It requires explicit opt-in. A lab should state maximum allocation, duration, cleanup, and abort conditions before running.

Never use an unbounded fork bomb, disk fill, or memory allocator as an educational shortcut. The skill is controlled failure, not surprise destruction.

## Choosing an Atlas envelope

Begin with behavior:

```text
API: bounded request body, bounded threads, no local computation loop
Worker: one claim at a time in Course 1, larger memory allowance
Edge: bounded clients and body, no durable state
```

Then select limits and prove them under the declared lab workload. Preserve `memory.events`, `cpu.stat`, process exit status, readiness result, and latency. A passing test with no pressure does not prove the boundary.

## Atlas implementation bridge

Inspect the `MemoryMax`, `CPUQuota`, and `TasksMax` properties in the units. Use the bounded resource lab only in a disposable VM. Preserve cgroup counters before, during, and after pressure so you can distinguish application allocation from kernel reclaim or throttling.

The dependency-light tests validate policies and state transitions, not kernel enforcement. Kernel evidence belongs in the Linux/privileged proof record.

## Design review prompts

- Which resource exhaustion should reject new work rather than kill a process?
- Which metric identifies pressure rather than mere usage?
- How much host headroom is reserved for recovery?
- Can one service create enough tasks or descriptors to starve another?
- Which namespace claim would still be false without capability and mount policy?

## Boundary case: pressure moves after optimization

Raising a CPU quota can move the bottleneck to database I/O, memory allocation, or connection capacity. Increasing memory can enlarge caches and improve latency, but it can also delay detection of a leak. Resource tuning is an experiment: define workload, change one boundary, observe multiple resources, and preserve correctness.

The Atlas course does not choose production limits from the reference values. It teaches how to prove that a limit is enforced and how the workload behaves when it is reached.

## Boundary case: reclaim and writeback coupling

Memory pressure can force dirty pages to be written, turning memory contention into I/O latency. A worker writing results may be delayed by global writeback even when its own CPU and memory counters look acceptable. PSI, block-device latency, dirty-page counters, and cgroup I/O evidence may be needed together.

## Resource worksheet

```text
resource:
normal demand:
burst demand:
hard boundary:
early-warning boundary:
application behavior at boundary:
supervisor behavior:
host headroom:
measurement window:
strongest executed evidence:
```

Complete this independently for API, worker, and edge; a single host-wide limit hides ownership.

## Field method: interpret pressure before choosing a limit

Resource limits are policy, not diagnosis. Before setting them, distinguish demand, utilization, contention, throttling, and failure. A CPU-bound worker may show high utilization with little queueing; a host with many runnable tasks may show run-queue pressure and increased latency; a cgroup may be throttled even when the host has idle cores because its quota is exhausted. `/proc/stat`, `vmstat`, `pidstat`, cgroup counters, and pressure-stall information answer different questions.

Memory evidence is equally layered. Virtual size is not resident memory. Resident memory includes private pages and shared mappings; page cache may be reclaimable; swap activity can preserve correctness while destroying latency; cgroup `memory.current` and `memory.events` describe the group's accounting and boundary events. An application allocation error, cgroup OOM kill, and host OOM kill are different failure paths with different owners.

Build the Atlas resource envelope from a workload statement:

```text
steady API requests per second:
maximum concurrent connections:
maximum request bytes:
worker concurrency:
largest in-flight job:
expected page-cache use:
startup burst:
shutdown deadline:
```

Then choose `MemoryHigh` as a pressure signal where appropriate, `MemoryMax` as a hard containment boundary, `TasksMax` to prevent process/thread explosions, and CPU controls that preserve both fairness and useful throughput. Do not set a memory ceiling equal to an observed average. Include transient allocation, interpreter overhead, native libraries, file buffers, and a measured safety margin.

Pressure Stall Information is useful because it measures time in which tasks cannot make progress due to CPU, memory, or I/O contention. It is not a direct SLO and does not identify the offending code by itself. Correlate it with cgroup counters, application latency, and host state.

The lab's key question is not whether a stress command can trigger a limit. It is whether Atlas fails inside the intended boundary, reports the failure truthfully, and releases resources so unrelated services recover. A limit that merely moves failure into an opaque restart loop is not a successful design.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| cgroup v2 controllers operate in one hierarchy and ancestor limits constrain descendants. | Linux cgroup v2 | cgroup files and systemd unit cgroup |
| A CPU quota is a ceiling, not a reservation. | Linux scheduler policy | `cpu.stat` and workload latency |
| A namespace changes a process view but is not a complete isolation or security boundary. | Linux mechanism/course policy | namespace inspection plus privilege policy |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Host average hides unit throttling

A cgroup can be throttled while host-wide CPU appears available.

### RSS arithmetic

Summing resident sets double-counts shared pages and ignores reclaim behavior.

### Limit without failure design

A memory or task ceiling without application behavior at the boundary converts overload into opaque crashes.


## Module synthesis

Return to the central question: **How does the kernel share finite host resources, and how can one workload be bounded without making false isolation claims?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**The worker has no memory ceiling, and readiness remains green while host memory pressure causes unrelated services to stall.**—fails for the predicted reason.

## Continue

Module 04 gives Atlas a deliberate model for durable and ephemeral bytes.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
