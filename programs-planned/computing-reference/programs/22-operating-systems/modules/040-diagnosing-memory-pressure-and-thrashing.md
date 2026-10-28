---
module_id: OS-040
program: Operating Systems
level: 1
module_number: 40
title: Diagnosing Memory Pressure and Thrashing
status: complete
last_verified: 2026-09-04
---

# Diagnosing Memory Pressure and Thrashing

## One-Page Review

### Governing question

How can an operator distinguish healthy memory utilization from harmful pressure and true thrashing, identify the responsible scope and mechanism, and intervene without converting a transient symptom into data loss or a larger outage?

### Essential definitions

- **Memory utilization** describes occupied capacity; high utilization alone does not imply harm.
- **Memory pressure** occurs when demand for usable memory forces reclaim, compaction, throttling, or allocation delay that affects work.
- **Direct reclaim** makes an allocating task participate synchronously in freeing memory.
- A **refault** is renewed demand for content that was recently evicted.
- **Swap churn** is repeated page-out and page-in activity with little useful progress.
- **Pressure stall information (PSI)** quantifies time in which tasks lose progress because a resource is contended.
- **Thrashing** is sustained replacement and fault activity that leaves execution dominated by memory stalls rather than useful work.

### Central model, mechanism, or theorem

Diagnose over a window `Delta`: capacity state `C`, demand and locality `W`, reclaim work `R`, refault and swap feedback `E`, stall time `S`, and useful service output `U`. Pressure is operationally harmful when reclamation or waiting rises and `U` or latency degrades; thrashing is supported when rapid eviction-and-return or swap cycling coincides with sustained stalls and collapsed progress.

No single counter proves the diagnosis. Use synchronized deltas, rates, ratios, and latency distributions at system, NUMA node, cgroup, process, and allocation-order scopes. Correlate before changing one variable, then verify both service recovery and absence of transferred harm.

### Critical invariants

- Absolute counters are converted to deltas over known monotonic intervals with reset and wrap handling.
- Capacity, activity, stall, and service evidence share the same clock and workload phase.
- Anonymous, file, slab, page-table, huge-page, pinned, swap, and cache memory remain separately attributed.
- Global, node, cgroup, process, and container scopes are not silently mixed.
- Reclaim scans, pages actually freed, refaults, writeback, compaction, OOM, and pressure stalls are distinguished.
- Mitigation preserves workload priority, data integrity, durability, and a rollback path.
- Evidence containing process maps, allocation sites, or identifiers is access-controlled and retention-bounded.

### Common failures

Common mistakes are alarming on low free memory while cache is healthy, treating RSS as additive across shared pages, reading cumulative VM counters as instantaneous rates, blaming swap merely because allocated swap is nonzero, diagnosing global shortage from a local cgroup limit, raising limits without capacity, disabling swap blindly, dropping caches as a benchmark ritual, and declaring recovery when memory usage falls but latency remains broken.

### Compact example

During a ten-second incident, page scans rise by 6,000 and steals by 1,800, 900 pages refault after 1,200 evictions, swap-in and swap-out remain high, memory `full` PSI accounts for 25% of the interval, and request throughput falls 58%. The correlated evidence supports thrashing. If the same scan activity occurred in background while PSI stayed near zero and throughput held steady, it would instead support productive reclaim.

### Connections

[OS-034](034-demand-paging.md) through [OS-039](039-shared-pages-and-page-cache.md) define the mechanisms producing faults, eviction, COW, mapped I/O, and cache state. [OS-041](../ROADMAP.md), [OS-048](../ROADMAP.md), and [OS-049](../ROADMAP.md) connect filesystems, journaling, and crash consistency.

## Governing Question

Memory systems are designed to use RAM. An almost-full machine can be efficient, while a machine with apparent free memory can stall on a cgroup ceiling, NUMA node, high-order allocation, dirty writeback, or pinning.

The governing question is therefore causal: what demand exceeded which usable supply, what mechanism attempted recovery, how much useful progress was lost, and which intervention addresses that constraint at acceptable risk?

## Why This Matters

Memory incidents often masquerade as CPU, disk, database, or network problems. Reclaim burns CPU; swap and writeback create I/O; faults inflate latency; OOM kills look like application crashes; NUMA imbalance creates remote-access slowdown.

Poor interventions can worsen the outage. Adding a cache may expand the working set, raising `memory.max` can threaten neighbors, aggressive reclaim can induce refault, and disabling swap can convert slowdown into abrupt failure.

Diagnosis must combine kernel mechanics with workload outcomes. The objective is not a pretty memory chart; it is restored useful service with understood capacity headroom and verified recurrence controls.

## Prerequisites and Retrieval

Review [OS-034](034-demand-paging.md), [OS-035](035-page-faults.md), [OS-036](036-virtual-memory-page-replacement.md), [OS-037](037-copy-on-write.md), [OS-038](038-memory-mapped-files.md), and [OS-039](039-shared-pages-and-page-cache.md).

Retrieve these distinctions:

- free, available, reclaimable, committed, resident, proportional, and working-set memory differ;
- cumulative counters, gauges, event counts, time totals, averages, and histograms require different calculations;
- minor and major faults do not map one-to-one to fast and disk-bound events;
- background reclaim and direct reclaim have different application effects;
- scan count, eviction count, reclaimed bytes, and successful allocation are different outcomes;
- swap allocation, page-out, page-in, zswap activity, and swap-device I/O differ;
- global capacity, NUMA-node reserves, zones, cgroups, and allocation orders can fail independently;
- correlation narrows hypotheses but controlled change and recovery validate causation.

## Learning Objectives

After this module, you should be able to:

1. build a synchronized memory-incident evidence set across capacity, activity, stalls, and service outcomes;
2. compute counter deltas, rates, reclaim efficiency, refault ratios, swap churn, and stall fractions;
3. distinguish healthy cache use, productive reclaim, direct-reclaim latency, fragmentation, leaks, and thrashing;
4. localize pressure to system, node, cgroup, process, mapping, or allocation order;
5. choose safe mitigations such as load shedding, limit repair, working-set reduction, writeback relief, or capacity addition;
6. design reproducible pressure experiments and rollback gates;
7. construct an assurance and post-incident record without overstating evidence.

## Core Exposition

### Begin with service impact

Establish the incident interval and the affected user outcome: throughput, queue depth, request latency, deadline misses, job progress, UI responsiveness, or failure rate. Memory activity without lost service may be normal optimization.

Use monotonic timestamps and preserve the pre-incident baseline. Align deployment, load, cgroup, kernel, storage, and topology changes on the same timeline.

### Utilization is not pressure

Unused RAM provides little value, so kernels fill it with page cache and other reclaimable data. Low `MemFree` alone is not evidence of scarcity; an available-memory estimate includes capacity likely obtainable without destructive intervention.

Conversely, a global total can look comfortable while a constrained domain stalls. Always name the resource scope and allocation requirement.

### Inventory memory classes

Partition memory into anonymous, file cache, shared memory, slab, page tables, kernel stacks, network buffers, huge pages, device or pinned pages, compressed memory, and explicit reservations. Identify which classes are reclaimable, swappable, movable, or protected.

Avoid double counting shared pages across processes. Use proportional measures when answering ownership questions and system totals for capacity conservation.

### Gauges and counters

A gauge such as current resident bytes has meaning at one sample time. A cumulative counter such as pages scanned has meaning as a difference between samples. Reset, restart, namespace change, and counter width affect deltas.

Calculate rates only with actual elapsed monotonic time. Sampling too slowly hides spikes; sampling too rapidly can add noise and overhead.

### Free reserves and watermarks

Allocators maintain reserves and zone watermarks so critical and burst allocations can proceed. Background reclaim begins before absolute exhaustion; direct reclaim begins when immediate supply is insufficient under policy.

Inspect per-node and per-zone state when allocation locality or DMA constraints matter. Machine-wide free pages may be unusable for the requested zone or order.

### Background reclaim

Background reclaim converts cold reclaimable content into free capacity asynchronously. Evidence includes scanner CPU, scanned and stolen pages, writeback, and whether free targets recover.

High background activity can be acceptable during a workload transition if application stalls stay low and refaults remain controlled. It is not automatically thrashing.

### Direct reclaim

Direct reclaim puts allocation latency on the requesting task. A thread can scan, unmap, wait for writeback, or trigger filesystem work before its allocation completes.

Track count and duration, not just pages reclaimed. A low-volume high-latency direct-reclaim path can dominate p99 while aggregate memory metrics look calm.

### Scan efficiency

A simple ratio is pages reclaimed or stolen divided by pages scanned over the same scope and interval. Low efficiency suggests hot, pinned, dirty, protected, or otherwise ineligible candidates, but interpretation depends on implementation counters.

A high ratio does not prove good policy: the system may efficiently evict pages that refault immediately. Combine efficiency with refault and service evidence.

### Refaults and working sets

Refault history estimates whether recently evicted file or anonymous content was still useful. High refault relative to eviction under stable demand suggests the effective working set exceeds protected capacity or victim selection is wrong.

Normalize by bytes, type, generation, or eviction opportunity as supported. One process can refault shared content charged to another domain, so attribution remains policy-sensitive.

### Page-fault evidence

Minor faults include mapping, COW, or cache-resident work under platform definitions; major faults often indicate blocking retrieval, not necessarily one local-disk operation. Report class and latency whenever possible.

Fault rate can rise during healthy startup and fall during a frozen workload. It must be correlated with progress and lifecycle phase.

### Swap state

Allocated swap can contain cold pages without current I/O and is not itself a fault. Diagnose page-out and page-in rates, device latency, queueing, compressed-cache hits and rejects, and which domains are active.

Sustained bidirectional turnover plus refaults and lost progress supports churn. One-directional page-out during a phase change can be productive.

### Compressed swap

Zswap or zram trades CPU and RAM for reduced storage I/O. Measure compression ratio, pool size, store failures, rejects, evictions, decompression latency, and backing-device writeback.

Incompressible pages or a full pool can create repeated rejected work. A lower disk-I/O graph may hide CPU and memory pressure transferred into compression.

### File-cache pressure

Sequential scans can fill cache and displace reusable data; dirty writers can hold memory until writeback catches up. Measure active and inactive file bytes, readahead use, dirty and writeback bytes, refaults, and storage throughput.

Dropping caches destroys diagnostic state and rarely represents a durable fix. It can temporarily improve free memory while making subsequent reads slower.

### Anonymous pressure

Heap, stack, private COW, anonymous shared memory, and some runtime arenas contribute anonymous demand. RSS growth can reflect a valid workload expansion, retained reusable arenas, fragmentation, or a leak.

Compare live-object or application allocation evidence, working-set activity, reclaimability, swap, and post-load recovery. One heap profile may exclude native, shared, or kernel memory.

### Slab and kernel memory

Dentries, inodes, network buffers, page tables, and subsystem caches can grow outside a process heap. Some are reclaimable; some are pinned by active objects or references.

Inspect cache-specific object counts and shrink behavior. Blaming the largest slab without explaining its owning workload and lifecycle is not diagnosis.

### Pinned and unevictable memory

Memory locks, DMA pins, device buffers, ramfs-like content, and kernel reservations can be unavailable to ordinary reclaim. A pin leak produces low scan efficiency and apparent capacity that cannot be reused.

Correlate pin acquisition and release, device activity, locked mappings, and driver lifecycle. Forcing reuse would violate correctness.

### Fragmentation and compaction

A high-order allocation can fail even when enough base pages exist in total. Compaction moves pages to assemble contiguous runs, consuming CPU and potentially stalling allocators.

Inspect requested order, free-area distribution, compaction scan and migration, huge-page policy, and fallback behavior. More reclaim may not repair immovable fragmentation.

### NUMA-local pressure

A task constrained to one node can enter reclaim or remote access while other nodes retain free memory. CPU placement, memory policy, migration, and node watermarks explain the mismatch.

Record per-node memory classes, allocation failures, remote hits, migrations, and cgroup placement. A global dashboard can erase the causal boundary.

### Cgroup pressure

A cgroup can be throttled at `memory.high`, fail and invoke scoped OOM at `memory.max`, or experience reclaim despite global headroom. Effective `memory.min` and `memory.low` protections shape competition.

Read current usage, stat categories, event deltas, swap and zswap limits, NUMA state, and per-cgroup PSI. Hierarchical and local event views must not be confused.

### PSI some and full

Memory `some` time means at least some tasks are stalled on memory; `full` time means all non-idle tasks are simultaneously stalled under PSI's definition. Sustained full time is strong lost-progress evidence and is specifically useful for identifying thrashing.

Recent averages aid trend display; the cumulative microsecond total enables exact interval deltas. Triggers can alert on a declared stall amount within a window.

### I/O pressure coupling

Memory reclaim can wait on swap or dirty writeback, raising both memory and I/O PSI. Storage congestion may be cause, consequence, or an independent co-incident bottleneck.

Correlate block or remote I/O latency, queue depth, writeback, swap, filesystem errors, and task stacks. Do not infer direction from two rising charts alone.

### CPU pressure coupling

Page scanning, compression, compaction, fault handling, and allocator contention consume CPU. A workload may lose progress from memory work even before it sleeps on I/O.

Profile reclaim CPU and scheduler delay. Adding CPU can mask but not eliminate a working-set capacity deficit.

### Detecting thrashing

Require a pattern: repeated eviction followed by rapid refault or swap-in, high reclaim or fault work, sustained memory stalls, and collapsing useful throughput or latency. Rule out startup, one-time cache turnover, planned checkpointing, and load changes.

Define thresholds from service objectives and baselines, not universal folklore. The same stall fraction can be acceptable in a batch node and catastrophic in an interactive service.

### OOM events

OOM is a terminal capacity policy after reclaim cannot satisfy the allocation under its scope and constraints. Capture global or cgroup context, selected victim, allocation order, allowed nodes, protection, unreclaimable state, and preceding pressure.

An OOM kill may temporarily restore free memory while leaving the root cause. Repeated restarts can create a kill loop and erase evidence.

### Building a causal timeline

Place load, allocation, cache, reclaim, faults, swap, PSI, latency, throttling, and OOM on one timeline. Identify which change leads and which follows, including uncertainty from sample cadence.

Use task stacks, tracepoints, profiles, and application metrics to test candidate mechanisms. Preserve raw data before dashboards downsample it.

### Safe immediate mitigations

Options include shedding low-priority load, reducing concurrency, pausing batch work, rolling back a working-set regression, raising a misconfigured limit within verified capacity, moving a workload, relieving writeback, or adding memory.

Choose the smallest reversible action that addresses the identified scope. Protect control-plane and diagnostic capacity during intervention.

### Risky interventions

Blind cache drops erase useful data, broad OOM killing harms availability, disabling swap removes a safety tier, extreme swappiness shifts I/O cost, and unbounded limit increases transfer risk to neighbors.

Kernel tuning without a controlled experiment creates persistent hidden state. Record old value, new value, owner, expiry or review trigger, and rollback condition.

### Capacity and load control

When combined working sets exceed available protected memory, replacement policy alone cannot create capacity. Reduce admitted work, shrink per-request state, stage jobs, add memory, or accept an explicit failure policy.

Queueing can amplify memory demand because stalled work retains buffers while new work arrives. Admission control may recover both memory and latency faster than low-level tuning.

### Experimental validation

Reproduce with bounded synthetic or replayed load in an isolated environment. Sweep capacity and concurrency across the knee where stalls accelerate, rather than testing one point.

Change one policy at a time and compare steady state, overload, and recovery. Include cold and warm starts, dirty and clean data, swap configurations, NUMA placement, and realistic storage.

### Observability quality

Document units, scopes, reset behavior, kernel configuration, field availability, sample interval, aggregation, and missing data. Parse keyed interfaces by name because fields can vary or be added.

Validate dashboards against raw counters and controlled activity. Derived ratios with tiny denominators need suppression or confidence labeling.

### Security and assurance

Process maps, memory dumps, allocation stacks, and cgroup names may expose secrets or tenant identity. Minimize capture, redact safely, restrict access, and define retention.

Adversaries can intentionally allocate, pin, dirty, fault, compress poorly, or create reclaim contention. Quotas, priorities, bounded work, protected reserves, and tested overload policy are part of defense.

## Definitions and Notation

For interval `Delta=t_1-t_0`, counter rate is `r_X=(X_1-X_0)/Delta` after validating monotonicity. Let scan delta be `Q`, reclaimed delta `K`, eviction delta `V`, refault delta `J`, memory full-stall delta `S_f`, and useful output rate `U`.

Illustrative reclaim efficiency is `eta=K/Q` for `Q>0`; refault-per-eviction is `rho=J/V` for `V>0`; full-stall fraction is `sigma=S_f/Delta` after unit conversion. These are diagnostic features, not universal thresholds or proofs.

Let evidence vector be `D=(C,W,R,E,S,U,G)`, where `G` captures scope and configuration. A diagnosis names the hypothesized causal mechanism, contradicting evidence, uncertainty, and a reversible test.

## Mechanisms, Invariants, or Proof Structure

A reviewable pressure diagnosis follows twelve obligations:

1. Define service symptom, incident window, baseline, clocks, and workload phase.
2. Identify system, node, zone, cgroup, process, mapping, and allocation-order scopes.
3. Inventory anonymous, file, slab, page-table, huge, pinned, swap, compressed, and reserved memory.
4. Convert counters to validated deltas and rates while retaining gauges and distributions.
5. Correlate reclaim, refault, fault, swap, writeback, compaction, PSI, OOM, and service output.
6. Distinguish productive background work, synchronous stalls, fragmentation, limits, leaks, and thrashing.
7. Build a causal timeline and record evidence that contradicts the leading hypothesis.
8. Select a reversible mitigation matched to the constrained scope and workload priority.
9. Protect integrity, control-plane headroom, tenant isolation, and evidence during response.
10. Verify service recovery, pressure relief, absence of transferred harm, and rollback readiness.
11. Reproduce the capacity knee and validate a durable prevention change under overload.
12. Preserve raw data, configuration, limitations, owners, and independent review.

The executable classifier recomputes one interval's diagnostic features from supplied deltas.

<!-- bijux-verify: {"id":"pressure-window-analysis","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scan-efficiency=0.30\nrefault-per-eviction=0.75\nswap-in-per-s=40.0 swap-out-per-s=60.0\nmemory-full-stall=25.0%\nthroughput-drop=58.0%\ndiagnosis=thrashing-likely\n","stderr":""}} -->
```python
interval_seconds = 10.0
deltas = {
    "pages_scanned": 6000,
    "pages_reclaimed": 1800,
    "pages_evicted": 1200,
    "pages_refaulted": 900,
    "pages_swapped_in": 400,
    "pages_swapped_out": 600,
    "memory_full_stall_us": 2_500_000,
}
throughput_before = 1000.0
throughput_during = 420.0

scan_efficiency = deltas["pages_reclaimed"] / deltas["pages_scanned"]
refault_ratio = deltas["pages_refaulted"] / deltas["pages_evicted"]
swap_in_rate = deltas["pages_swapped_in"] / interval_seconds
swap_out_rate = deltas["pages_swapped_out"] / interval_seconds
stall_fraction = deltas["memory_full_stall_us"] / (interval_seconds * 1_000_000)
throughput_drop = 1.0 - throughput_during / throughput_before
likely = stall_fraction >= 0.10 and refault_ratio >= 0.50 and throughput_drop >= 0.30

print(f"scan-efficiency={scan_efficiency:.2f}")
print(f"refault-per-eviction={refault_ratio:.2f}")
print(f"swap-in-per-s={swap_in_rate:.1f} swap-out-per-s={swap_out_rate:.1f}")
print(f"memory-full-stall={stall_fraction:.1%}")
print(f"throughput-drop={throughput_drop:.1%}")
print("diagnosis=" + ("thrashing-likely" if likely else "insufficient-evidence"))
```

The toy uses hand-selected thresholds and already-correct deltas. It omits counter resets, scope mismatch, workload phase, latency distributions, page sizes, kernel semantics, sampling error, causality, and production safety.

## Alternatives and Trade-Offs

- Coarse fleet dashboards reveal broad patterns but hide node, cgroup, and millisecond stalls.
- High-frequency sampling catches spikes but adds storage, parsing, and observer overhead.
- PSI measures lost progress directly but does not identify the memory owner or mechanism alone.
- VM counters expose mechanisms but require version-aware semantics and workload correlation.
- Per-process profiling localizes allocations but can miss shared and kernel memory.
- Load shedding restores headroom quickly but reduces admitted work.
- Raising a cgroup limit avoids local throttling but can endanger siblings and global reserves.
- Swap extends survivable capacity but can turn overload into long latency.
- Disabling swap bounds disk churn but increases abrupt OOM risk.
- Compressed swap reduces device I/O but consumes CPU and some RAM.
- Working-set protection reduces thrashing but can trigger earlier OOM when capacity is insufficient.
- Adding memory treats capacity shortage but does not repair leaks, pinning, or bad locality automatically.

## Failure Modes and Misconceptions

1. **“Low free memory means pressure.”** reclaimable cache can make high use healthy.
2. **“Available memory means every allocation succeeds.”** scope, zone, node, order, and policy constrain usability.
3. **“RSS values can be summed.”** shared pages create double counting.
4. **“A rising cumulative counter is a current spike.”** interval deltas and time are required.
5. **“Major fault means one disk read.”** backing, readahead, and platform definitions differ.
6. **“Any swap use is thrashing.”** cold allocated swap can be idle.
7. **“High scan efficiency is healthy.”** quickly refaulted victims can still destroy progress.
8. **“One global chart explains a cgroup incident.”** local limits can stall with global headroom.
9. **“OOM proves the machine has no free bytes.”** allocation constraints and protection determine eligibility.
10. **“Dropping caches fixes memory.”** it destroys useful state and hides the cause temporarily.
11. **“Disabling swap fixes latency.”** it can replace slowdown with immediate failure.
12. **“More memory fixes every issue.”** leaks and unbounded admission consume the new capacity too.
13. **“Correlation proves the root cause.”** controlled intervention and recovery supply stronger evidence.
14. **“Lower usage means recovery.”** service latency, stalls, errors, and transferred harm must recover too.

## Worked Examples

### Example 1

`MemFree` is low, but available memory is healthy, background reclaim is quiet, PSI is zero, and throughput meets its objective. The evidence supports useful cache occupation, not an incident.

### Example 2

Direct-reclaim events are rare but each aligns with p99.9 latency spikes during high-order buffer allocation. Order-specific compaction and fragmentation evidence explains what aggregate RSS missed.

### Example 3

Scans and reclaimed pages are both high during a batch phase, yet refault remains low, memory PSI is negligible, and throughput is stable. Reclaim is productive rather than thrashing.

### Example 4

File refaults surge after a sequential backup scan displaces a database index. Readahead and cache ownership evidence identify pollution; lowering database memory would worsen the wrong workload.

### Example 5

Swap-out occurs once after a phase change and pages remain cold. No swap-in, stall, or throughput loss follows, so nonzero swap allocation is not diagnosed as churn.

### Example 6

Swap-in and swap-out remain high, zswap rejects incompressible pages, full memory PSI rises, and completed jobs fall. The correlated loop supports anonymous thrashing and compression overhead.

### Example 7

A container records `memory.high` events and per-cgroup PSI while the host retains available memory. The cause is scoped throttling, so a verified limit or workload adjustment is more precise than host tuning.

### Example 8

A NUMA-bound service reclaims locally and accesses remote memory while another node is free. CPU and memory placement correction restores latency without adding machine-wide capacity.

### Example 9

Pinned device pages grow after failed requests and never release. Reclaim efficiency collapses; balanced pin counters and driver lifecycle traces identify a resource leak that cache eviction cannot fix.

### Example 10

An OOM-killed service restarts, warms its cache, hits the same limit, and dies again. Admission control and retained pre-kill evidence break the loop before root-cause remediation.

## Cross-Program Connections

[Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects allocators, RSS, mappings, native leaks, and low-level observability. [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies service objectives, incident timelines, rollback, load shedding, and post-incident learning.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects cache locality, working sets, fragmentation, and memory accounting. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames resource margins, feedback loops, overload, causal evidence, safety, and assurance.

Within this program, [OS-036](036-virtual-memory-page-replacement.md) defines reclaim policy and [OS-039](039-shared-pages-and-page-cache.md) defines shared cache state; [OS-056](../ROADMAP.md), [OS-079](../ROADMAP.md), and [OS-089](../ROADMAP.md) revisit observability, NUMA, and resource management.

## References

- Linux kernel documentation, [PSI — Pressure Stall Information](https://docs.kernel.org/accounting/psi.html), current page checked 2026-09-04. Some and full stalls, cumulative totals, averages, triggers, cgroup scope, thrashing, and workload control.
- Linux kernel documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), current page checked 2026-09-04. Memory use, protections, high and maximum boundaries, events, PSI, NUMA, swap, zswap, reclaim, throttling, and scoped OOM.
- Linux kernel documentation, [Concepts overview](https://docs.kernel.org/admin-guide/mm/concepts.html), current page checked 2026-09-04. Zones, nodes, reclaimable memory, page cache, anonymous memory, watermarks, background and direct reclaim, compaction, and OOM.
- Linux kernel documentation, [Multi-Gen LRU](https://docs.kernel.org/mm/multigen_lru.html), current page checked 2026-09-04. Recency generations, refault feedback, file and anonymous selection, working-set estimation, minimum time-to-live, thrashing prevention, and proactive reclaim.
- Linux kernel documentation, [zswap](https://docs.kernel.org/admin-guide/mm/zswap.html), current page checked 2026-09-04. Compressed swap cache, CPU-memory-I/O trade-offs, pool limits, backing writeback, rejection, hysteresis, shrinker, and statistics.
- Linux kernel documentation, [Documentation for /proc/sys/vm](https://docs.kernel.org/admin-guide/sysctl/vm.html), current page checked 2026-09-04. Swappiness cost model, dirty policy, overcommit, watermarks, cache pressure, compaction, and OOM-related controls.
- Linux man-pages project, [proc_vmstat(5)](https://man7.org/linux/man-pages/man5/proc_vmstat.5.html), current page checked 2026-09-04. Keyed virtual-memory statistics, field variability, free pages, faults, reclaim, writeback, NUMA, compaction, and working-set counters.
- Linux man-pages project, [proc_meminfo(5)](https://man7.org/linux/man-pages/man5/proc_meminfo.5.html), current page checked 2026-09-04. System memory gauges, free and available memory, anonymous and cached content, dirty and writeback, slab, page tables, commitments, swap, and huge pages.
- Linux man-pages project, [proc_pid_smaps(5)](https://man7.org/linux/man-pages/man5/proc_pid_smaps.5.html), current page checked 2026-09-04. Per-mapping RSS, PSS, shared and private clean and dirty bytes, referenced state, anonymous memory, swap, page sizes, locks, and flags.
- Linux kernel documentation, [Delay accounting](https://docs.kernel.org/accounting/delay-accounting.html), current page checked 2026-09-04. Per-task delay categories, swap-in and reclaim delay, thrashing, PSI integration, collection controls, and diagnostic tooling.

## Exercises

### Exercise 1

Design an incident evidence table spanning capacity, reclaim, faults, swap, writeback, PSI, and service output. Define scope, units, cadence, deltas, and missing-data policy.

### Exercise 2

Given two synchronized samples, compute reclaim efficiency, refault ratio, swap rates, PSI fraction, and throughput change. State why the result does or does not prove thrashing.

### Exercise 3

Diagnose three cases: cgroup `memory.high` throttling with host headroom, NUMA-local exhaustion, and high-order fragmentation. Provide discriminating evidence and mitigation.

### Exercise 4

Design a safe response to anonymous swap churn and full memory PSI in a latency-sensitive service. Cover immediate action, risks, verification, rollback, and prevention.

### Exercise 5

Construct an assurance and post-incident review for an OOM and restart loop. Include evidence preservation, security, causal testing, capacity policy, and reviewers.

## Answers to the Exercises

### Answer 1

Use one monotonic timestamp per sample and retain wall-clock correlation separately. Record system, node, zone, cgroup and process identity; free and available bytes; anonymous, file, slab, page-table, huge, pinned, dirty, writeback, swap and compressed bytes; allocation order; scan and reclaim counters; refaults; faults; compaction; swap directions; PSI totals and averages; cgroup events; OOM; storage latency; CPU reclaim time; throughput and latency histograms.

Label each field as gauge, cumulative counter, event, total time, ratio, or distribution with source, unit, reset behavior, kernel and configuration dependency. Compute deltas only across compatible monotonic samples. Mark unavailable fields rather than substituting zero. Preserve raw keyed values, cadence, gaps, workload phase, deployment events, and dashboard transformations.

### Answer 2

Validate that counter identity, scope, units, and generation match and that the interval is positive. Compute `eta=Delta reclaimed/Delta scanned`, `rho=Delta refault/Delta eviction`, directional swap deltas divided by seconds, full-stall microseconds divided by interval microseconds, and `1-U_during/U_before` for comparable demand.

High refault, bidirectional swap, full stalls, and falling throughput together support a thrashing hypothesis, but thresholds are workload-specific and correlation alone does not prove direction. Check startup, load, writeback, storage, compaction, and sampling changes. A reversible capacity or load intervention followed by refault, PSI, and service recovery provides stronger causal evidence.

### Answer 3

For cgroup throttling, host available memory stays healthy while the target shows `memory.high` event deltas, per-cgroup reclaim and PSI, and usage near its effective boundary. Verify hierarchy and protections; reduce its working set or raise the limit only within capacity and neighbor budgets.

For NUMA pressure, one node or allowed-node set crosses watermarks, local reclaim and remote access rise, and other nodes retain capacity. Repair CPU and memory policy, migrate, or widen allowed nodes. For fragmentation, base-page totals exist but requested high order lacks contiguous blocks; compaction scans, migration failure, and order-specific allocation latency rise. Use smaller-order fallback, change huge-page or buffer strategy, or address immovable allocations. Global cache drops do not directly solve any of the three.

### Answer 4

Protect diagnostics and control-plane memory, then shed low-priority load or cap concurrency so outstanding work and buffers fall. If a recent deployment expanded the working set, roll it back. Move or pause batch tenants and relieve a verified swap-device or writeback bottleneck. Do not disable swap or increase limits blindly.

Verify that full and some PSI, page-in and page-out, refaults, direct-reclaim latency, queue depth, and service tails recover without OOM or neighbor regression. Keep an explicit rollback for every tuning change. Durably reduce per-request memory, bound admission, size capacity at the measured knee with margin, configure scoped protection and failure policy, and load-test steady, overload, and recovery states.

### Answer 5

Before restart erases state, retain scoped OOM report, allocation order and allowed nodes, cgroup limits and events, PSI totals, memory classes, reclaim and compaction deltas, swap and writeback, task lifecycle, deployment and load, victim choice, and service impact. Redact process maps, identifiers, stacks, and dumps under a defined access and retention policy.

Reproduce the loop with bounded load and inject the suspected capacity change. Prove admission, limit, protection, reclaim, victim, restart backoff, and evidence-preservation policies compose without a synchronized retry storm. Track corrective owner, capacity model, rollback, alert thresholds, and expiry for temporary tuning. Named kernel-memory, application-runtime, platform, storage, performance, security, reliability, capacity, and independent-verification reviewers assess residual risk; one successful restart or added-memory test alone does not prove prevention.
