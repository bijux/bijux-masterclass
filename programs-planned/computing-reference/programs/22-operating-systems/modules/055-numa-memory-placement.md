---
module_id: OS-055
program: Operating Systems
level: 2
module_number: 55
title: NUMA Memory Placement
status: complete
last_verified: 2026-09-04
---

# NUMA Memory Placement

## One-Page Review

### Governing question

How should an operating system place, migrate, replicate, and reclaim memory across non-uniform nodes so computation obtains adequate locality, bandwidth, capacity, and resilience without violating policy, lifetime, or sharing semantics?

### Essential definitions

- **Non-uniform memory access (NUMA)** describes a system where memory latency or bandwidth depends on the accessing CPU and memory node.
- A **NUMA node** groups CPUs, memory, or other resources with a locality relationship exposed by the platform.
- A **distance matrix** is an abstract relative-cost description between initiator and target nodes; it is not a complete performance model.
- **First touch** allocates a demand-faulted page according to the policy and execution context of the thread that first materializes it.
- A **memory policy** selects eligible or preferred nodes for future allocation and sometimes requests migration of existing pages.
- **Local allocation** prefers memory near the allocating CPU subject to allowed nodes, capacity, watermarks, and fallback.
- **Interleave** distributes allocations over a node set to spread bandwidth and capacity demand.
- **Page migration** changes a page's physical node while preserving its virtual address and coordinating mappings, references, writeback, and hardware access.
- **Automatic NUMA balancing** samples access locality and may migrate tasks or pages based on observed behavior.
- A **cpuset** constrains the CPUs and memory nodes a workload may use and composes with affinity and memory policy.

### Central model, mechanism, or theorem

For workload phases `p`, minimize a measured objective such as `Cost=sum A[p,c,n]*D[c,n] + M + Q + I`, where `A` is access volume from CPU or initiator node `c` to memory node `n`, `D` is measured or modeled access cost, `M` is migration and copy cost, `Q` is capacity, reclaim, and queueing penalty, and `I` is interference with other workloads. Placement is constrained by allowed nodes, memory availability, page movability, sharing, device mappings, huge-page granularity, and service-level requirements.

Policy is an instruction for allocation, not proof of residency or performance. Demand faults, allocator fallback, shared page-cache ownership, migration failure, scheduler movement, reclaim, hotplug, and topology changes can all produce another physical result. Correct design couples CPU placement with memory placement, observes actual pages and access traffic, and adapts only when benefit exceeds movement and disruption.

### Critical invariants

- Every allocation uses the effective policy produced by task, mapping, cpuset, node availability, and allocation-context rules.
- Physical page movement preserves virtual mappings, contents, dirty and writeback state, references, accounting, and device coherence.
- Shared pages have one explicit placement authority or a documented compromise among consumers on different nodes.
- CPU migration and memory migration are coordinated so independent controllers do not chase each other or oscillate.
- Hard binding fails or invokes only documented fallback; it never silently claims locality that was not achieved.
- Huge pages, pinned pages, kernel objects, and hotplugged memory follow their own movability and granularity constraints.
- Performance claims report actual residency, local and remote access, bandwidth, latency, migration, reclaim, and workload phase.

### Common failures

Common mistakes are equating node distance with measured latency, assuming virtual allocation places physical pages, initializing a parallel array from one thread and blaming first touch, setting thread policy after pages already exist, expecting policy to migrate pages without a migration flag, pinning CPUs while leaving memory remote, binding tightly enough to create local exhaustion, interleaving a latency-sensitive pointer chain, migrating heavily shared or pinned pages repeatedly, interpreting a syscall's overall success as every-page success, and measuring steady-state locality while hiding warm-up, compaction, or migration cost.

### Compact example

Suppose local access cost is 10 units and remote cost is 30. A phase issuing 80 accesses from CPU node 0 to memory node 0 and 20 remotely has weighted mean cost 14. Another phase on CPU node 1 with 70 percent local and 30 percent remote has mean 16. These numbers illustrate the access-distance term only; real performance also depends on bandwidth saturation, cache hits, contention, migration, page size, and controller topology.

### Connections

[OS-031](031-address-translation.md), [OS-034](034-demand-paging.md), [OS-036](036-virtual-memory-page-replacement.md), [OS-039](039-shared-pages-and-page-cache.md), and [OS-051](051-per-cpu-state.md) establish translation, faults, reclaim, sharing, and locality. [OS-056](../ROADMAP.md) and [OS-057](../ROADMAP.md) connect placement to affinity and load balancing.

## Governing Question

On a NUMA machine, “memory” is not one uniform pool. A CPU can reach several controllers with different latency, bandwidth, congestion, and energy cost. Devices and accelerators can add further initiators and memory tiers.

The governing question is how to select and maintain placement over time. A correct answer respects policy and object semantics; a useful answer also responds to workload phase, capacity, sharing, scheduler movement, page size, and migration cost.

## Why This Matters

Remote memory can raise latency and consume scarce interconnect bandwidth. A database or graph workload that looks compute-bound can spend most cycles waiting on pages initialized or migrated to another socket.

Overly strict locality can be just as damaging. Binding to a full node triggers allocation failure or aggressive reclaim while other nodes sit idle. Replication consumes capacity and creates update coherence. Migration spends bandwidth and invalidates translations.

NUMA behavior also complicates evidence. Cache hits hide DRAM distance, averages hide hot pages, automatic balancing changes placement during measurement, and topology labels do not reveal real controller load. Durable engineering uses measured phases and explicit constraints.

## Prerequisites and Retrieval

Review [OS-008](008-kernel-memory-allocation.md), [OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-033](033-translation-lookaside-buffers.md), [OS-034](034-demand-paging.md), [OS-036](036-virtual-memory-page-replacement.md), [OS-038](038-memory-mapped-files.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-051](051-per-cpu-state.md), and [OS-052](052-smp-kernel-synchronization.md).

Retrieve these distinctions:

- virtual reservation and physical page materialization can occur at different times;
- the faulting thread can differ from the thread that reserved or later uses memory;
- anonymous, private file, shared file, huge, pinned, device, and kernel pages have different placement paths;
- scheduler affinity controls eligible CPUs, while memory policy controls eligible or preferred memory nodes;
- page-table updates and migration require synchronization and translation invalidation;
- allocation policy, actual residency, and observed access locality are separate facts;
- free capacity, usable watermarks, fragmentation, and bandwidth headroom are different resources;
- a page shared across sockets cannot be local to every consumer simultaneously.

## Learning Objectives

After this module, you should be able to:

1. interpret NUMA topology, node sets, relative distance, capacity, and bandwidth evidence;
2. predict first-touch placement and distinguish task-default from mapping-specific policies;
3. select local, preferred, preferred-many, bind, interleave, or weighted-interleave behavior;
4. explain cpuset composition, allocation fallback, reclaim, migration, and automatic balancing;
5. reason about shared pages, huge pages, pinned memory, file caches, devices, and memory hotplug;
6. coordinate CPU affinity and memory placement across workload phases without oscillation;
7. validate placement using residency, access, migration, latency, bandwidth, and failure evidence.

## Core Exposition

### Discover topology

Enumerate possible and online CPU nodes, memory nodes, CPUs per node, capacity and free memory, distance matrix, caches, links, and devices. Sparse identifiers and memory-only nodes are valid possibilities.

Firmware distance is a starting abstraction. Benchmark relevant access sizes, concurrency, read/write mix, and link contention before using it as a quantitative latency model.

### Local and remote access

A CPU normally reaches memory attached to its node with lower latency and without consuming an inter-socket link. Remote access traverses additional fabric and may contend with coherence and device traffic.

Caches can satisfy an access without reaching home memory. Measure last-level misses and controller or fabric events when attributing performance to placement.

### Capacity and bandwidth

Local capacity can be exhausted before system capacity. Local bandwidth can saturate while unused capacity remains, or interleaving can improve aggregate bandwidth even though some accesses are remote.

Placement objectives therefore include capacity and bandwidth as well as latency. One “nearest node” heuristic cannot serve every workload.

### Virtual allocation

Reserving an anonymous virtual range generally does not allocate all backing pages. Physical placement happens as pages are faulted, prepopulated, or otherwise materialized.

Measurements distinguish reserved, resident, and committed memory. A policy applied before faults influences future pages but does not prove that every page now resides there.

### First touch

Under common default behavior, the CPU and policy context of the thread that first writes an anonymous page strongly influence its node. A read of untouched anonymous memory may use a shared zero page rather than allocate private backing.

Parallel workers should initialize the portions they will use while running on intended CPUs. A serial initializer can place an entire dataset near one node and create remote access later.

### Task-default policy

A thread memory policy governs future allocations not overridden by a more specific mapping policy. Threads in one process can carry different policies.

Policy inheritance and restoration follow platform APIs. Libraries should avoid changing ambient thread policy without a scoped restore because unrelated allocations may be affected.

### Mapping policy

A range-specific policy attaches to eligible virtual memory areas and overrides the task default for future faults in that range. Alignment and mapping boundaries determine coverage.

Changing policy does not necessarily move pages that already exist. Migration flags or explicit operations are separate, and partial results require inspection.

### Default and local policy

Default policy returns to inherited or system behavior. A local preference asks for memory near the CPU that allocates when that node is allowed and suitable.

Local is dynamic with execution placement: migrating the faulting task changes which node is local. It is not a permanent binding to the node current when policy was configured.

### Preferred policy

Preferred policy tries one home node and falls back when necessary. Preferred-many permits a set of acceptable preferred nodes, allowing the allocator to choose by locality and availability.

Preference improves resilience to pressure and weakens placement certainty. Observability must report where fallback pages actually landed.

### Binding policy

Binding restricts allocation to a node set under the documented fallback and reclaim rules. It is useful for isolation, locality experiments, and hard data-placement requirements.

An undersized set can cause local reclaim, compaction, latency spikes, or allocation failure despite free memory elsewhere. Capacity planning includes working set, page tables, caches, huge pages, and operational reserve.

### Interleave policy

Interleave distributes page allocations over eligible nodes, often by a deterministic sequence. It spreads capacity and memory-controller demand for streaming or parallel access.

It deliberately makes some accesses remote. Pointer-chasing and single-thread latency workloads can suffer even while aggregate bandwidth improves.

### Weighted interleave

Weighted interleave apportions pages according to configured relative weights. Weights can represent asymmetric capacity or desired bandwidth use.

Static weights do not automatically follow changing workload or congestion. Record the active weights, allocation epoch, and resulting page distribution.

### Policy composition

Effective policy combines the requested mode and node mask with allowed memory nodes, online state, mapping type, flags, and allocation context. Cpuset changes can remap or constrain masks depending on static or relative semantics.

Query allowed and effective policy near the operation when correctness depends on it. Administrative reconfiguration can change eligibility concurrently.

### Cpuset constraints

A cpuset can constrain both CPUs and memory nodes. Scheduler affinity is further intersected with allowed CPUs; memory-policy nodes are evaluated within allowed memory.

Changing cpusets without coordinating pages and tasks can create remote placement or migration storms. Controllers publish one desired configuration and observe convergence.

### Anonymous memory

Private anonymous pages are naturally associated with the faulting task and are often migratable. Copy-on-write faults can allocate new pages according to the current policy rather than the original parent's location.

Fork, shared anonymous mappings, pins, huge pages, and memory locks change ownership and movability. The intended policy is tested through these transitions.

### File-backed memory

Shared file mappings use page-cache pages owned by the file mapping, not a private copy per task. The thread that first populates the cache and filesystem allocation rules can influence location.

Consumers on many nodes contend for one cached page placement. Readahead, I/O completion CPU, writeback, and storage-device locality complicate “first consumer” assumptions.

### Shared pages

A write-shared page cannot be independently placed for each reader without replication and coherence semantics. Choose a home near the dominant writer, interleave a large shared dataset, partition ownership, or accept remote access.

Read-only replicas improve locality but consume memory and require versioned replacement or invalidation when content changes.

### Kernel allocations

Kernel allocators can request a node, use the current task and CPU context, fall back under flags, or obtain per-CPU and per-node caches. Interrupt and device contexts can constrain allowed blocking and fallback.

Object metadata and payload placement both matter. A locally allocated descriptor that points to remote hot data does not solve the workload.

### Per-CPU and per-node caches

Per-CPU caches serve local allocations cheaply and refill from node pools. Per-node structures aggregate enough demand to amortize global coordination while limiting remote traffic.

Memory hidden in caches remains part of capacity. Pressure and hotplug drain paths return it without violating object ownership.

### Automatic NUMA balancing

Automatic balancing periodically makes selected mappings produce hinting faults, records which CPUs access pages, and can migrate pages or tasks to improve locality. It is an adaptive control loop.

Sampling faults and migration cost CPU and bandwidth. Shared workloads, rapid phase changes, pinned tasks, or external policy can confuse the signal and produce oscillation.

### Task versus page migration

Moving a task toward its pages can be cheaper than copying a large working set; moving pages toward a pinned task can preserve cache or device affinity. Multi-thread sharing changes the comparison.

Estimate remaining phase duration and benefit. Migration is wasteful when the phase ends before savings repay scanning, copy, TLB invalidation, and cache warming.

### Explicit page migration

An explicit interface can query locations or request individual pages move to target nodes without changing virtual addresses. Results are per page because some pages may already match, be busy, pinned, shared, invalid, or fail allocation.

The overall return value never substitutes for inspecting status entries. Privilege and ownership limit moving another process's pages or shared pages.

### Migration mechanism

Migration allocates a destination page, isolates the source from ordinary allocation or reclaim, blocks or retries conflicting users, copies state, replaces mappings, updates accounting, and releases the old page after references permit.

Dirty file pages, writeback, swap cache, references, device mappings, and huge pages have specialized coordination. Failures unwind without losing contents or mapping identity.

### Translation effects

Page migration preserves virtual address while changing the physical frame. Page-table entries are invalidated or replaced, and stale TLB translations are removed on relevant CPUs.

TLB shootdowns and cache warming add latency beyond the page copy. A page-migration benchmark includes these effects rather than measuring memory bandwidth alone.

### Pinned and unmovable pages

DMA pins, long-term user-page pins, kernel allocations, mlocked state, or unsupported mappings can prevent or delay movement. A device may retain physical addresses beyond a CPU page-table change.

Design interfaces to minimize unnecessary long-term pins and expose nonmovable capacity. Placement controllers treat migration failure as normal evidence, not an impossible exception.

### Transparent huge pages

Transparent huge pages reduce TLB overhead but allocate and migrate at larger granularity. One hot subpage can pull a large page to a node where its remaining contents are remote to other consumers.

Promotion, splitting, compaction, and collapse introduce latency and placement changes. Choose mapping advice and policy from access density and phase behavior.

### Reserved huge pages

Explicit huge-page pools are reserved per size and distributed across allowed nodes according to configuration and allocation context. Fragmentation and per-node free pools constrain later requests.

Verify the actual per-node pool. A global huge-page count can hide shortage on the node where a bound workload needs it.

### Reclaim and fallback

An allocator can reclaim local pages, compact memory, or fall back to another allowed node depending on policy and flags. Aggressive local reclaim may preserve locality while causing worse latency than remote allocation.

Tune only after measuring miss cost, reclaim stalls, workload reuse, and global pressure. Strict binding and preference intentionally choose different failure-versus-fallback behavior.

### Memory tiers

Systems can expose memory with differing latency, bandwidth, capacity, endurance, or device attachment. NUMA node identity can participate in tiering but does not alone describe every property.

Hotness-based promotion and demotion add another control loop. Coordinate it with task placement, automatic balancing, reclaim, and application policy to avoid repeated movement.

### Device locality

NIC, storage, and accelerator DMA traffic has topology. Placing buffers near the consuming CPU can be wrong if a remote device is the dominant initiator.

Jointly place interrupts, workers, queues, memory, and devices, then measure both CPU and DMA paths. IOMMU and peer-memory behavior remain part of the platform contract.

### Replication

Replicate immutable or read-mostly state per node so readers access local copies. Publish versions atomically and reclaim retired replicas after every reader domain quiesces.

Writes require invalidation, copy-and-publish, or an authoritative home. Replication is a consistency protocol, not merely an allocation flag.

### Workload phases

Initialization, loading, training, query, checkpoint, and cleanup phases can have different CPU and memory access matrices. A single lifetime policy can be suboptimal.

Phase transitions use hysteresis and minimum residence time. Controllers compare projected savings with migration and cache-warm cost before acting.

### Avoid controller oscillation

The scheduler may move tasks toward idle CPUs while the memory manager moves pages toward recent task locations. Independent fast reactions can chase one another.

Share observations, use common epochs, damp changes, and establish authority: pin compute and move pages, keep pages stable and move tasks, or jointly optimize at a slower cadence.

### Memory hotplug

Adding memory publishes new sections and nodes through ordered initialization before allocation. Offlining isolates ranges, migrates movable pages, handles unmovable blockers, drains allocator state, and removes reachability before physical removal.

Huge pages, vmemmap metadata, device memory, pins, and kernel objects can block offlining. Failure leaves the node in a coherent documented state rather than partially absent.

### Observability

Inspect topology, allowed masks, thread and mapping policies, page residency by mapping, local and remote access, faults, migration attempts and failures, reclaim, compaction, huge pages, controller bandwidth, and interconnect traffic.

Residency snapshots race movement and show location rather than use. Combine them with phase-aligned access samples and application latency.

### Experiment design

Compare default first touch, parallel first touch, local preference, binding, interleave, weighted interleave, and automatic balancing under fixed CPU placement. Then vary affinity deliberately.

Control cache warm-up, page population, huge-page settings, cpusets, background traffic, frequencies, and initial free memory. Include movement cost and convergence time in the reported interval.

### Assurance

Preserve hardware and firmware, topology, distances, kernel and configuration, cpusets, CPU affinity, memory policy, mapping types, page sizes, initial residency, workload phases, raw counters, migrations, failures, latency, bandwidth, energy, and limitations.

Assurance names scheduler, memory-management, architecture, device, application, performance, hotplug, security, and independent reviewers. A faster run on one topology does not certify portable NUMA placement.

## Definitions and Notation

Let CPU or initiator nodes be `C`, memory nodes `N`, phases `P`, access volume `A[p,c,n]`, relative or measured cost `D[c,n]`, capacity `K[n]`, and placement `X[o,n]` for object or page set `o`.

Let objective `J(X)=sum A[p,c,n]*D[c,n] + M(X) + Q(X) + I(X)`, where `M` is movement and translation cost, `Q` is capacity, reclaim, fragmentation, and queueing penalty, and `I` is interference. Weights depend on the service requirement.

Effective eligible nodes are `E=requested_policy_nodes intersect cpuset_allowed intersect online_memory_nodes`, further constrained by mapping type and allocation context. Preference can fall back within allowed nodes; binding follows its stricter contract.

For a contemplated migration with one-time cost `C_move`, remaining access count `R`, old mean cost `d_old`, and new mean cost `d_new`, migration has a simple positive gross case when `R*(d_old-d_new) > C_move`, before interference, uncertainty, and risk margins.

## Mechanisms, Invariants, or Proof Structure

1. **Discover reality.** Record CPUs, nodes, distances, controllers, devices, capacities, page sizes, allowed masks, and actual measured costs.
2. **Define the objective.** Choose latency, bandwidth, capacity, isolation, energy, or a weighted service requirement for each workload phase.
3. **Classify memory.** Separate anonymous, private, shared file, huge, pinned, device, kernel, immutable, and write-shared objects.
4. **Coordinate compute.** Couple scheduler affinity and memory policy so first touch and later execution have deliberate locality.
5. **Select policy.** Use local, preferred, preferred-many, bind, interleave, or weighted interleave with explicit fallback and failure semantics.
6. **Materialize deliberately.** Populate pages in the intended parallel context and verify actual residency rather than virtual reservation.
7. **Adapt cautiously.** Migrate task, page, or neither only when projected phase benefit exceeds copy, TLB, cache, and interference cost.
8. **Preserve migration safety.** Coordinate mappings, references, dirty state, devices, accounting, huge pages, and errors.
9. **Control shared state.** Partition, home, interleave, or version replicas with explicit authority and consistency.
10. **Bound pressure and lifecycle.** Cover reclaim, compaction, fallback, hotplug, pins, capacity reserve, and teardown.
11. **Measure end to end.** Observe residency, access, bandwidth, faults, migration, reclaim, latency, throughput, energy, and convergence.
12. **Retain evidence.** Preserve topology, configuration, policies, phases, counters, raw outputs, failures, reviewers, and limitations.

<!-- bijux-verify: {"id":"numa-weighted-access-cost","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"phase=ingest local-percent=80 mean-cost=14.00\nphase=query local-percent=70 mean-cost=16.00\ncombined-mean-cost=15.00\n","stderr":""}} -->
```python
local_cost = 10
remote_cost = 30
phases = (("ingest", 80, 20), ("query", 70, 30))
means = []

for name, local_accesses, remote_accesses in phases:
    total = local_accesses + remote_accesses
    mean = (local_accesses * local_cost + remote_accesses * remote_cost) / total
    means.append(mean)
    print(f"phase={name} local-percent={local_accesses} mean-cost={mean:.2f}")
print(f"combined-mean-cost={sum(means) / len(means):.2f}")
```

The executable example recomputes a two-distance weighted mean for equal-size phases. It does not measure hardware or model caches, bandwidth, contention, allocation, page faults, migration, TLBs, huge pages, devices, reclaim, energy, or phase imbalance.

## Alternatives and Trade-Offs

- Default first touch adapts naturally to the faulting thread but can preserve accidental serial initialization; explicit policy improves control and adds configuration coupling.
- Local preference favors latency and permits fallback; strict binding improves placement certainty and risks reclaim or failure under local pressure.
- Interleave spreads bandwidth and capacity but creates remote access; local placement minimizes simple latency and can saturate one controller.
- Weighted interleave represents asymmetric nodes but requires maintained weights; ordinary interleave is simpler and can mismatch capacity.
- Moving tasks avoids copying large working sets but can disrupt CPU cache, device, and scheduling locality; moving pages preserves CPU placement and consumes memory bandwidth and TLB work.
- Automatic balancing adapts without application changes but samples and can oscillate; manual placement is predictable and can become stale across phases.
- Huge pages reduce TLB pressure but migrate, allocate, and fragment at coarse granularity; base pages permit fine placement and more translation overhead.
- Per-node replication gives local reads but consumes capacity and complicates updates; one shared copy preserves simple authority and causes remote reads.
- Page migration preserves virtual addresses but can fail on pins and busy state; rebuild-and-publish enables semantic control and costs allocation and copying.
- Per-CPU allocation maximizes local fast paths but makes aggregation and hotplug expensive; per-node allocation shares locally and reduces multiplicity.
- Aggressive local reclaim preserves node affinity but stalls allocation and discards useful data; remote fallback consumes interconnect bandwidth and avoids immediate reclaim.
- Detailed sampling identifies hot pages but creates faults and overhead; coarse residency snapshots are cheap and do not show access direction.

## Failure Modes and Misconceptions

- **“NUMA distance is measured latency.”** It is a platform-relative abstraction requiring workload-specific measurement.
- **“Virtual allocation places physical memory.”** Demand faults or population create backing later.
- **“The allocating thread determines first touch.”** Another thread can materialize the page.
- **“Changing policy moves existing pages.”** Migration needs separate flags or operations.
- **“Bind guarantees success on the desired node.”** Capacity, allowed masks, page type, and errors still govern allocation.
- **“Interleave makes every access local.”** It distributes pages and intentionally creates remote accesses for some CPUs.
- **“CPU pinning solves memory locality.”** Existing pages can remain remote.
- **“Page migration is just a copy.”** Mappings, TLBs, references, dirty state, devices, and accounting participate.
- **“One migration return value describes all pages.”** Per-page status captures partial outcomes.
- **“A shared page has one obviously local node.”** Consumers can have conflicting locality.
- **“Huge pages always improve NUMA behavior.”** Coarse placement and migration can amplify mismatch.
- **“Automatic balancing always converges.”** phases and competing controllers can oscillate.
- **“Free remote memory implies usable local headroom.”** Node watermarks, fragmentation, and policy differ.
- **“Steady-state throughput includes placement cost.”** Warm-up and convergence must be reported explicitly.

## Worked Examples

### Example 1

A main thread zeros a 200 GiB array on node 0 before workers start on four sockets. Parallel first-touch initialization by each worker places its slice near later computation.

### Example 2

A latency-sensitive service prefers node 1 but permits fallback. Residency shows ten percent remote pages during pressure, which is expected policy behavior rather than silent failure.

### Example 3

A streaming analytics job interleaves pages across four controllers. Single-access latency rises, while aggregate bandwidth improves because all controllers serve traffic.

### Example 4

A task is pinned to node 2 after its heap was populated on node 0. Explicit migration can improve a long phase, but the plan includes copy and TLB costs.

### Example 5

An individual-page migration request reports some pages already local, some moved, and several busy or pinned. The controller consumes every status entry and retries only appropriate cases.

### Example 6

A shared read-mostly policy table is copied once per node and version-published. Updates build new replicas and retire old versions after readers quiesce.

### Example 7

A transparent huge page contains hot regions used by different sockets. Splitting permits finer migration, trading greater TLB pressure for better locality.

### Example 8

A workload bound to one memory node triggers reclaim stalls despite free memory elsewhere. Preferred-many policy uses two nearby nodes and reduces tail latency.

### Example 9

Automatic balancing moves pages toward a task while the scheduler repeatedly moves the task for load. Shared epochs and hysteresis stop the controllers from chasing each other.

### Example 10

Memory offlining fails because long-term DMA pins remain. The system reports blockers and leaves the range online rather than partially removing mapped physical state.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects controllers, cache coherence, interconnect topology, TLBs, DMA, and memory tiers. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects partitioning, work placement, shared-state ownership, and phase behavior.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects sharding, replication, page indexes, hotness tracking, and migration metadata. [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) connects capacity, isolation, observability, experiments, and service-level evidence.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies objective functions, interacting controllers, lifecycle hazards, trade studies, and assurance. Within this program, [OS-056](../ROADMAP.md) treats affinity, [OS-057](../ROADMAP.md) load balancing, and [OS-060](../ROADMAP.md) contention diagnosis.

## References

- Linux man-pages project, [numa(7)](https://man7.org/linux/man-pages/man7/numa.7.html), current page checked 2026-09-04. NUMA concepts, topology, interfaces, policies, process maps, library support, and related operations.
- Linux man-pages project, [set_mempolicy(2)](https://man7.org/linux/man-pages/man2/set_mempolicy.2.html), current page checked 2026-09-04. Thread-default policies, node masks, local, preferred, bind, interleave, weighted modes, flags, and errors.
- Linux man-pages project, [mbind(2)](https://man7.org/linux/man-pages/man2/mbind.2.html), current page checked 2026-09-04. Range policies, anonymous and file mappings, existing pages, strict and migration flags, cpusets, and partial conformance.
- Linux man-pages project, [get_mempolicy(2)](https://man7.org/linux/man-pages/man2/get_mempolicy.2.html), current page checked 2026-09-04. Thread and address policy, allowed nodes, page locations, flags, changing cpusets, and queries.
- Linux man-pages project, [move_pages(2)](https://man7.org/linux/man-pages/man2/move_pages.2.html), current page checked 2026-09-04. Per-page location queries and migration, status results, privileges, allowed nodes, policy interaction, and errors.
- Linux man-pages project, [proc_pid_numa_maps(5)](https://man7.org/linux/man-pages/man5/proc_pid_numa_maps.5.html), current page checked 2026-09-04. Effective mapping policies, page residency, dirty and mapped state, node counts, huge pages, and observation.
- Linux kernel documentation, [NUMA Memory Policy](https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html), current page checked 2026-09-04. Policy scopes, inheritance, node sets, constraints, modes, shared memory, APIs, and effective behavior.
- Linux kernel documentation, [Page migration](https://docs.kernel.org/mm/page_migration.html), current page checked 2026-09-04. Migration motivations, mechanisms, mapping replacement, movability, interfaces, failure, and NUMA use.
- Linux kernel documentation, [Transparent Hugepage Support](https://docs.kernel.org/admin-guide/mm/transhuge.html), current page checked 2026-09-04. Huge-page objectives, promotion, splitting, allocation, advice, controls, memory cost, and NUMA implications.
- Linux kernel documentation, [Memory Hot(Un)Plug](https://docs.kernel.org/admin-guide/mm/memory-hotplug.html), current page checked 2026-09-04. Adding and removing memory, online policies, migration, unmovable pages, huge pages, device memory, failure, and lifecycle.

## Exercises

### Exercise 1

Design placement for a four-socket in-memory database with initialization, read-mostly query, write-heavy compaction, shared metadata, and strict tail-latency goals.

### Exercise 2

Compare local, preferred-many, bind, interleave, and weighted-interleave policy for pointer chasing, streaming bandwidth, asymmetric capacity, and isolation.

### Exercise 3

Specify a safe automatic controller that chooses task migration, page migration, or no action without oscillating across workload phases.

### Exercise 4

Trace explicit page migration for anonymous, shared file, huge, dirty, pinned, and device-mapped pages, including partial failures and hotplug.

### Exercise 5

Build a validation and assurance plan for a NUMA placement change. Include residency, accesses, topology, pressure, huge pages, devices, and reproducibility.

## Answers to the Exercises

### Answer 1

Discover actual CPU, controller, link, device, capacity, and bandwidth topology. Pin or preferentially schedule each database worker group within one node and parallel-initialize its owned partitions so first touch follows future access. Use local or preferred-many allocation for latency-sensitive indexes with capacity reserve, and partition mutable metadata per node. Version and replicate immutable catalog data per node, with one serialized update authority and safe reclamation.

For scans, consider interleaving large streaming buffers across controllers after measuring bandwidth; do not interleave pointer-heavy indexes by default. Compaction builds destination partitions near their next owners, rate-limits copies, and publishes new versions rather than migrating hot pages blindly. Coordinate scheduler and memory decisions through epochs and hysteresis. Observe query latency, local and remote misses, bandwidth, residency, migration, reclaim, compaction, page sizes, and fallback during initialization, queries, compaction, checkpoints, pressure, and failover. Capacity plans include shared cache, huge-page pools, page tables, replicas, and operating reserve.

### Answer 2

Pointer chasing favors local or preferred placement because dependent misses expose latency; preferred-many adds resilience where several nodes are acceptably near. Binding gives isolation and repeatability but can reclaim or fail under local pressure, so reserve capacity and test failure. Streaming bandwidth can benefit from interleave across controllers even with remote accesses.

Asymmetric capacity or bandwidth can use weighted interleave, provided weights and resulting residency are observed and updated deliberately. Ordinary interleave gives equal distribution and simpler control. Tenant isolation can use cpusets plus binding, while flexible services use preference inside allowed nodes. For each case, report fallback, actual pages, local and remote traffic, controller saturation, latency tails, migration, reclaim, and phase; policy names alone do not prove the result.

### Answer 3

Sample access by phase and maintain stable task, page, and topology generations. Estimate task-move cost from CPU cache, device, scheduler and affinity disruption; estimate page-move cost from bytes, TLB invalidation, pins, bandwidth and expected failures. Project remaining-phase savings from the measured access matrix and require a margin above total cost.

Give one coordinator authority over both decisions. Apply minimum residence time, hysteresis, migration bandwidth and page-count budgets, and per-node capacity reserve. Prefer moving a small task toward a large shared working set, pages toward a long-lived pinned compute group, and neither for short or ambiguous phases. After action, wait for a convergence epoch before reevaluating. Treat failed, busy, shared and pinned pages explicitly. Roll back policy without pretending copied bandwidth is recoverable, and disable adaptation safely when telemetry or topology is unavailable.

### Answer 4

Stabilize the address space and page references, validate privilege and allowed destinations, then process each page independently. Allocate destination memory, isolate and lock or otherwise stabilize the source, coordinate page tables and mappings, copy content and metadata, replace mappings, invalidate stale TLBs, update node, reclaim, cgroup and policy accounting, then release the source only after references permit.

Anonymous movable pages follow the general path. Shared file pages require mapping, dirty, writeback and all-consumer coordination. Huge pages migrate or split under their supported granularity and capacity. Dirty pages can require writeback or specialized migration entries. Long-term pins and device DMA mappings can reject movement until their owners unpin and synchronize hardware. Hotplug first blocks new allocation, migrates what is movable, reports blockers, drains allocator and huge-page state, and removes the range only after reachability and references are gone. Return and retain per-page status; overall success never erases partial failure.

### Answer 5

Record the placement objective and permitted fallback, then preserve topology, firmware distances, measured latency and bandwidth, devices, CPU and memory masks, policies, mapping types, page sizes, huge-page configuration, initial free memory, automatic balancing, reclaim and compaction controls, kernel, firmware, affinity, and workload phases. Verify policy queries and actual residency before and throughout execution.

Measure local and remote access events, cache misses, controller and fabric bandwidth, faults, hinting faults, migrations attempted, succeeded and failed, per-page statuses, TLB invalidation, reclaim and compaction stalls, throughput, tail latency, energy, and convergence cost. Test serial and parallel first touch; local, preferred, bind, interleave and weighted modes; balanced and skewed sharing; pressure, fallback and allocation failure; base and huge pages; pins, DMA, file cache, fork and copy-on-write; task moves; hotplug; and competing workloads. Retain raw counters, maps, timestamps, seeds, traces, failures, reviewer roles, and limitations, and separate warm-up, adaptation, steady state, and teardown results.
