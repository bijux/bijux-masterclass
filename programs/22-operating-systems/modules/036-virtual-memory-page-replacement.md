---
module_id: OS-036
program: Operating Systems
level: 1
module_number: 36
title: Virtual-Memory Page Replacement
status: complete
last_verified: 2026-09-04
---

# Virtual-Memory Page Replacement

## One-Page Review

### Governing question

When physical memory is scarce, which resident page should an operating system reclaim so it restores allocatable capacity without destroying a workload's useful working set, violating backing-store semantics, or imposing unbounded stalls?

### Essential definitions

- **Page replacement** selects reclaimable resident memory for eviction or reuse.
- A **reference string** is the ordered sequence of virtual-page accesses used to analyze a replacement policy.
- A **resident set** is the set of a process's pages currently held in physical memory.
- A **working set** is the pages actively used during a defined recent window.
- A **reuse distance** counts distinct intervening references between two accesses to the same page.
- A **refault** occurs when an evicted page is needed again and must be brought back.
- **Thrashing** is sustained replacement activity that leaves execution dominated by memory stalls rather than useful work.

### Central model, mechanism, or theorem

For access trace `r_1,...,r_n` and capacity `k`, a policy maintains resident state `S_t`, where `|S_t| <= k`. A miss chooses an eligible victim using observed history and cost estimates; it cannot know the future OPT victim in a live system. Total harm is not merely fault count: it includes scan CPU, writeback or swap I/O, refault latency, blocked allocation, fairness, and lost locality.

A safe reclaim transition is `eligible -> isolated -> validated -> cleaned or stored -> unmapped -> reusable`. Any failed validation returns the page without losing references or data. Feedback from refaults and stall time corrects a policy whose recency samples or cost estimates were wrong.

### Critical invariants

- Only reclaimable pages enter victim selection; pins, locks, hardware ownership, and unevictable mappings remain authoritative.
- Dirty or uniquely backed content reaches durable or recoverable backing before its frame is reused.
- Every mapped victim is unmapped with correct reference accounting and translation invalidation.
- Selection scopes honor memory protections, cgroup policy, NUMA placement, and fairness boundaries.
- Reclaim work, writeback, retries, and direct-allocation stalls are bounded or reach an explicit failure policy.
- Refault, scan, eviction, writeback, swap, and pressure-stall evidence is separated by memory type and scope.

### Common failures

Common mistakes are treating textbook LRU as implementable without observation cost, evicting a dirty page as cheaply as a clean cache page, scanning pinned pages repeatedly, assuming a referenced bit proves future reuse, applying one global queue without tenant protections, measuring only page-fault count, responding to thrashing with still more indiscriminate reclaim, and validating an algorithm only on one friendly trace.

### Compact example

With three frames and trace `A,B,C,A,D,B`, a second-chance queue initially fills with `A,B,C`. The second access to `A` sets its reference bit. When `D` arrives, the hand clears reference bits until it finds an unreferenced page; the exact victim depends on all intervening bit observations. The example shows why Clock approximates recency at bounded metadata cost, not why it reproduces exact LRU.

### Connections

[OS-031](031-address-translation.md) through [OS-035](035-page-faults.md) establish mappings and faults. [OS-037](../ROADMAP.md), [OS-038](../ROADMAP.md), and [OS-039](../ROADMAP.md) develop copy-on-write, mapped files, and swap.

## Governing Question

Free memory is an operating reserve, not an end in itself. Reclaiming too late pushes allocation into synchronous work; reclaiming too early discards useful cache. The replacement problem therefore combines eligibility, prediction, cost, isolation, persistence, concurrency, and feedback.

The governing question is not simply “which page is oldest?” It is which reclaimable unit, in which accounting domain and node, can be removed at acceptable total cost while preserving correctness and service objectives.

## Why This Matters

Replacement policy controls whether memory overcommit becomes efficient multiplexing or a latency collapse. It affects application tail latency, filesystem throughput, swap traffic, storage endurance, CPU spent scanning, NUMA locality, and the point at which out-of-memory policy acts.

Real pages are heterogeneous. A clean file-cache page may be discarded and reread; anonymous content normally needs swap or another preservation mechanism; dirty file data needs writeback; a pinned page may be ineligible; a huge folio amplifies both the benefit and cost of one decision.

Textbook algorithms expose core ideas, but production systems observe references imperfectly and operate concurrently. An engineer must connect the model to hardware access bits, page-table walks, reverse mappings, reclaim domains, writeback, and measurable workload harm.

## Prerequisites and Retrieval

Review [OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-033](033-translation-lookaside-buffers.md), [OS-034](034-demand-paging.md), and [OS-035](035-page-faults.md).

Retrieve these distinctions:

- virtual-page identity differs from physical-frame identity;
- present, referenced, dirty, mapped, pinned, and reclaimable are independent properties;
- eviction removes residency, while writeback preserves modified content and swap preserves anonymous content;
- a page fault is an event, while a refault is feedback about a prior eviction;
- local policy acts within one resident set, while global policy arbitrates among workloads;
- a clean eviction can still be costly if it destroys locality;
- free-page watermarks, background reclaim, and direct reclaim describe pressure response, not victim quality;
- correctness, throughput, tail latency, and fairness require different evidence.

## Learning Objectives

After this module, you should be able to:

1. simulate OPT, FIFO, LRU, and Clock-style replacement on a reference string;
2. explain Belady's anomaly, the stack property, working sets, reuse distance, and refault feedback;
3. classify clean file, dirty file, anonymous, swap-backed, huge, mapped, pinned, and unevictable candidates;
4. trace safe isolation, revalidation, writeback, unmapping, invalidation, accounting, and reuse;
5. distinguish background, direct, global, cgroup, NUMA, and proactive reclaim;
6. diagnose thrashing with scan, refault, I/O, latency, and pressure-stall evidence;
7. design tests and assurance arguments for concurrent, multi-tenant replacement policy.

## Core Exposition

### Capacity and reference strings

A reference string records page identities in access order. Given `k` frames, an access hits if its page is resident and misses otherwise. A simplified analysis counts misses after starting empty.

The trace omits access latency, read versus write, sharing, page size, and concurrency unless those are explicitly modeled. Two policies with equal miss counts can impose very different I/O and stall cost.

### Optimal replacement

The offline OPT policy evicts the page whose next use lies farthest in the future, or is never used again. For a fixed trace and capacity, it gives the minimum achievable miss count and is useful as a comparison bound.

An online kernel cannot observe future accesses. OPT is therefore an oracle baseline, not an implementation prescription. Trace representativeness and future knowledge must be labeled when reporting the gap.

### FIFO and Belady's anomaly

FIFO evicts the page resident for the longest time, regardless of recent reuse. It is simple and cheap but can remove a heavily used page because arrival age is not access recency.

For some traces, increasing FIFO's frame count increases misses. This is Belady's anomaly. It warns that plausible queue rules need adversarial traces and that more capacity does not rescue every policy monotonically.

### LRU and the stack property

Exact least-recently-used replacement evicts the page whose last access is oldest. Its resident sets have the stack property: for the same prefix, the pages resident with `k` frames are a subset of those resident with `k+1`. Consequently, exact LRU does not exhibit Belady's anomaly.

Maintaining a perfectly ordered operation on every memory reference is generally too expensive. Production mechanisms sample or batch recency and therefore approximate the mathematical policy.

### Clock and second chance

Clock places candidates in a circular order with a reference bit. At selection, a set bit is cleared and the hand advances; the first eligible candidate observed with a clear bit is selected. Hardware accessed bits or software tracking can supply the signal.

Clock bounds ordering metadata and amortizes scanning, but scan length grows when many pages are recently referenced or ineligible. Reference-bit clearing also changes the observation state and may require page-table synchronization.

### Aging and generations

Aging periodically shifts sampled reference information into counters; generation-based policies group pages by observed access epochs. Both retain more temporal information than one reference bit without maintaining exact order.

Linux Multi-Gen LRU divides evictable folios into generations, ages through page-table and reverse-map walks, and uses refault feedback when choosing types and tiers. That is one current implementation, not a universal operating-system contract.

### Working sets

The working-set model treats pages referenced in a recent time or reference window as the active demand of a workload. If combined working sets exceed available capacity, frequent eviction and refault can dominate progress.

Window choice is policy. Too short excludes genuine reuse; too long protects obsolete pages. Working-set estimates should include uncertainty and be evaluated against stalls, not accepted as ground truth.

### Reuse distance

Reuse distance for a reference is the count of distinct pages accessed since the previous reference to that page. Under a fully associative exact-LRU model, a reuse distance below capacity predicts a hit; larger distance predicts a miss.

Real mappings, replacement scopes, page sizes, and sampled recency weaken this equivalence. Reuse-distance distributions remain valuable for capacity analysis when their abstraction is explicit.

### Refault feedback

An eviction loses information unless the system leaves a compact history marker. A quick refault suggests the page was still in the working set and that selection was costly. Delayed or absent refault is evidence, though not proof, that eviction was useful.

Compare refault distance or age within the same accounting scope. A page can be reloaded by another process or cgroup, so shared-cache attribution needs deliberate ownership rules.

### Eligibility before ranking

Victim ranking operates only after eligibility. Pins, locked memory, device ownership, unevictable mappings, active writeback, migration, isolation, and filesystem constraints can temporarily or permanently exclude a page.

Repeatedly scanning ineligible pages wastes CPU and can create false scarcity. Track why candidates were rejected and move durable exclusions out of ordinary reclaim queues.

### Clean file-backed pages

A clean file-cache page has a recoverable copy in its backing object and can often be discarded after mapping and reference checks. Reuse still incurs storage or network I/O, so “clean” does not mean “free.”

Mapped pages require reverse-map work and page-table invalidation. Concurrent access can set referenced state or acquire a reference during reclaim, requiring revalidation.

### Dirty file-backed pages

Dirty file data must be written back, migrated to another valid representation, or retained. Starting writeback may defer rather than complete reclamation. Congested or failed storage can turn memory pressure into long stalls.

Replacement and writeback policy are coupled. A system needs limits on dirty memory, background flushing, error propagation, and evidence distinguishing pages scanned, submitted, cleaned, and actually freed.

### Anonymous and swap-backed pages

Anonymous pages do not ordinarily have a file copy. Eviction requires swap, compressed memory, another configured tier, or proof that content can be discarded under a defined semantic such as lazy-free state.

Swap availability is not the same as useful swap performance. Anonymous selection must account for allocation, I/O, encryption, compression, device health, and the cost of later swap-in.

### Shared pages and ownership

A file-cache page can serve many address spaces and accounting domains. Evicting it based on one process's apparent inactivity can harm active sharers. Reverse mappings and cache ownership rules shape both cost and fairness.

Reference counts alone do not measure utility. Preserve mapping, cgroup, object, and access evidence needed to avoid charging or protecting the wrong workload.

### Huge pages and folios

One huge mapping or multi-page folio covers more memory than a base page. Reclaiming it may release substantial capacity but can discard hot subpages with cold ones; splitting offers finer choice at CPU, lock, metadata, and fragmentation cost.

The unit of accounting, access sampling, writeback, migration, and invalidation must agree. Never silently compare a folio count with a base-page count.

### NUMA and memory tiers

On NUMA systems, reclaiming local memory can preserve a node's allocation reserve but push future access remote. Migration to another node or slower tier may be preferable to discard, depending on bandwidth, latency, and policy.

Global free capacity can hide local pressure. Record node, tier, allocation policy, migration, and remote-access consequences rather than diagnosing only a machine-wide total.

### Reclaim scopes and fairness

Global reclaim searches system memory; local or targeted reclaim acts within a node, cgroup, process range, or other domain. Protection and limit controls can reserve memory, bias victim choice, throttle a workload, or trigger domain-local OOM policy.

Fairness is not identical to equal page counts. Shared cache, protected services, batch jobs, and differently costly pages need explicit service policy. A low-priority scanner must not reclaim protected memory merely because it is easy to find.

### Watermarks and background reclaim

Systems maintain free-memory thresholds to start background reclaim before allocations fail. Linux documentation describes `kswapd` waking near a low watermark and direct reclaim as pressure becomes more severe.

Watermarks create headroom for bursts and constrained allocations. They do not decide which page is cold, and tuning them trades reserve size, background work, and synchronous risk.

### Direct reclaim and allocation stalls

When an allocator performs reclaim synchronously, application progress is now coupled to scanning, unmapping, writeback, and storage. A successful allocation may still violate a latency objective.

Bound per-attempt work, propagate reclaim progress accurately, and separate allocator latency from background throughput. Retry without new candidates or completed I/O is a livelock risk.

### Proactive reclaim and advice

Proactive reclaim tries to free cold memory before acute pressure. Linux exposes examples through cgroup `memory.reclaim`, `MADV_COLD`, `MADV_PAGEOUT`, and DAMON-based reclamation under their documented constraints.

Advice is not proof of inactivity, and an accepted request need not guarantee an exact amount reclaimed. Validate ranges, permissions, partial outcomes, refault harm, and interaction with normal pressure policy.

### Thrashing and load control

Thrashing occurs when the active demand exceeds useful capacity or policy repeatedly evicts soon-needed pages. Faults, swap, writeback, and scan CPU rise while useful throughput falls and latency grows.

Policy correction may protect a working set, reduce multiprogramming, shed load, migrate a job, add memory, or terminate work. Merely scanning faster can worsen contention. Full memory pressure-stall time is especially useful evidence of system-wide lost progress.

### Out-of-memory policy

Reclaim can fail because nothing is eligible, backing is exhausted, writeback is stuck, or protected working sets consume capacity. The terminal response may reject allocation, invoke a scoped or global OOM policy, or degrade service according to system rules.

OOM is not itself a replacement algorithm. The system must record the exhausted scope, protections, reclaim attempts, eligible bytes, backing state, and decision inputs.

### Concurrency and the reclaim transition

A scanner isolates a candidate so competing reclaimers do not act on it simultaneously. It then rechecks references, mappings, dirty state, writeback, pins, generation, and ownership before destructive steps.

If state changed, it restores the page to the proper structure. If eviction proceeds, it preserves content, unmaps safely, performs required translation invalidation, updates counters and histories, and releases the frame exactly once.

### Observability and experiments

Measure scanned, skipped, isolated, reactivated, written, swapped, evicted, and refaulted pages; scan CPU; direct-reclaim duration; allocation latency; I/O; PSI; OOM events; and workload throughput and tail latency. Partition by anonymous or file, clean or dirty, node, cgroup, page size, and reclaim source.

Experiments preserve policy configuration, kernel build, hardware accessed-bit behavior, memory size, page sizes, NUMA placement, swap and storage configuration, cache warmup, trace, workload phase, repetitions, and raw samples.

### Security and assurance

Replacement must preserve isolation, content confidentiality, and backing integrity. A reused frame is sanitized before exposure; swap and compressed stores follow protection policy; diagnostics do not disclose addresses or victim contents.

Adversarial workloads can churn access bits, dirty pages, pin memory, induce shared-cache contention, or force expensive reclaim. Resource limits, privilege checks, fair accounting, bounded work, and independently reviewed failure policy are part of assurance.

## Definitions and Notation

Let reference trace be `R=(r_1,...,r_n)`, capacity be `k`, resident set before access `t` be `S_t`, and fault indicator be `F_t=1` when `r_t` is not in `S_t`. The simplified miss count is `M_k(R)=sum(F_t)`.

For page `p`, let `next_t(p)` be its next reference after time `t`; OPT selects an eligible resident page maximizing this value, with no future reference treated as infinity. Let `d_t(p)` be distinct-page reuse distance, and `W(t,Delta)` the pages used in the selected recent window.

For candidate `p`, use cost estimate `C(p)=C_scan+C_unmap+C_preserve+C_refault+C_fairness`. The components are policy-weighted observations, not universally comparable physical constants.

## Mechanisms, Invariants, or Proof Structure

A reviewable replacement design follows twelve obligations:

1. Define the reclaim scope, capacity pressure, allocation objective, and policy version.
2. Separate eligibility from ranking and preserve every pin, lock, mapping, and backing constraint.
3. State how recency or frequency is observed and the cost and error of sampling.
4. Rank clean file, dirty file, anonymous, shared, huge, NUMA, and tiered memory with explicit costs.
5. Isolate a victim under concurrency and revalidate state before each irreversible transition.
6. Preserve dirty or unique content before reuse and propagate backing failures.
7. Unmap, invalidate translations, update reverse maps, histories, ownership, and counters in safe order.
8. Bound scanning, writeback, direct reclaim, retries, and external dependencies.
9. Honor cgroup, NUMA, protection, priority, and multi-tenant fairness rules.
10. Detect thrashing through refault and stall feedback and invoke load or capacity policy.
11. Test deterministic traces, races, failures, page types, and hostile workloads.
12. Preserve configuration and raw evidence while labeling model, implementation, and empirical claims.

The executable toy compares FIFO, exact LRU, and second-chance misses on one deterministic trace.

<!-- bijux-verify: {"id":"replacement-policy-simulator","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"frames=3 trace=70120304230321201701\nfifo=15\nlru=12\nclock=14\n","stderr":""}} -->
```python
trace = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
frames = 3

def fifo_misses(items, capacity):
    resident = []
    hand = 0
    misses = 0
    for page in items:
        if page in resident:
            continue
        misses += 1
        if len(resident) < capacity:
            resident.append(page)
        else:
            resident[hand] = page
            hand = (hand + 1) % capacity
    return misses

def lru_misses(items, capacity):
    resident = []
    misses = 0
    for page in items:
        if page in resident:
            resident.pop(resident.index(page))
        else:
            misses += 1
            if len(resident) == capacity:
                resident.pop(0)
        resident.append(page)
    return misses

def clock_misses(items, capacity):
    resident = []
    referenced = []
    hand = 0
    misses = 0
    for page in items:
        if page in resident:
            referenced[resident.index(page)] = 1
            continue
        misses += 1
        if len(resident) < capacity:
            resident.append(page)
            referenced.append(1)
            continue
        while referenced[hand] == 1:
            referenced[hand] = 0
            hand = (hand + 1) % capacity
        resident[hand] = page
        referenced[hand] = 1
        hand = (hand + 1) % capacity
    return misses

print(f"frames={frames} trace={''.join(str(page) for page in trace)}")
print(f"fifo={fifo_misses(trace, frames)}")
print(f"lru={lru_misses(trace, frames)}")
print(f"clock={clock_misses(trace, frames)}")
```

This model assumes equal base pages, one global fully associative frame pool, reads only, no pins, no writeback, no concurrency, and initially empty memory. Its miss counts do not predict a production kernel's latency or victim choices.

## Alternatives and Trade-Offs

- OPT supplies a lower-bound oracle but requires unavailable future knowledge.
- FIFO has tiny metadata cost but ignores reuse and can exhibit Belady's anomaly.
- Exact LRU has strong trace properties but impractical per-reference ordering overhead at machine scale.
- Clock reduces metadata work but can scan many referenced or ineligible pages.
- Generational aging captures broader recency but adds page-table walking and tuning complexity.
- Frequency signals protect repeatedly used pages but can retain stale historical popularity.
- Clean-file preference frees memory cheaply but can overprotect anonymous memory and cause cache refaults.
- Anonymous reclaim expands usable capacity with swap but adds storage, compression, and confidentiality cost.
- Local reclaim improves attribution but can strand capacity or punish one workload.
- Global reclaim pools capacity but complicates fairness, ownership, and isolation.
- Proactive reclaim creates headroom but risks evicting pages before demand proves pressure.
- Larger pages reduce mapping overhead but make replacement decisions coarser.

## Failure Modes and Misconceptions

1. **“LRU is just a linked list.”** exact LRU requires observing and ordering every relevant reference.
2. **“Referenced means hot.”** a sampled bit proves a past access in a window, not future utility.
3. **“More frames always reduce faults.”** FIFO can exhibit Belady's anomaly.
4. **“Clean pages are free victims.”** refault and backing latency can be severe.
5. **“Dirty eviction immediately frees memory.”** writeback may defer reclaim and block on storage.
6. **“Anonymous memory is unreclaimable.”** swap or another backing tier can preserve it, with costs.
7. **“A high reference count means high value.”** sharing and pins differ from predicted reuse.
8. **“One queue is fair.”** tenant protections, ownership, NUMA, and priorities require policy.
9. **“Successful reclaim means healthy memory.”** allocation can succeed after unacceptable stalls.
10. **“Fault count detects thrashing.”** scan CPU, refaults, I/O, PSI, and lost throughput are also required.
11. **“Scanning harder fixes pressure.”** it can amplify lock, CPU, and I/O contention.
12. **“Page counts compare all units.”** base pages, huge folios, and bytes are not interchangeable.
13. **“Advice guarantees eviction.”** applicability, races, and partial outcomes constrain it.
14. **“OOM means replacement is broken.”** protection and backing policy may intentionally forbid further reclaim.

## Worked Examples

### Example 1

OPT sees that `C` is never referenced again while `A` and `B` return, so it evicts `C`. A live kernel cannot make that choice from future knowledge; the result is an offline comparison bound.

### Example 2

FIFO with four frames has more misses than with three on a known adversarial trace. The anomaly invalidates the claim that its resident set monotonically contains the smaller-capacity set.

### Example 3

A Clock scan finds six referenced pages, clears their bits, skips two pinned pages, and finally isolates a cold clean file page. Metrics distinguish eight examined candidates from one reclaimed page.

### Example 4

A clean database index page refaults milliseconds after eviction. The policy records the eviction history and raises its protection rather than continuing to label all clean file pages cheap.

### Example 5

A dirty file page enters writeback, but the device is congested. The scanner does not count it as freed; background flushing and allocation-stall metrics expose the dependency.

### Example 6

A swapless host faces cold anonymous memory and active file cache. Anonymous pages without discard semantics are not silently destroyed; the policy reclaims eligible file data or reaches its capacity failure policy.

### Example 7

A 2 MiB huge page contains one frequently touched 4 KiB region. Whole-folio eviction causes costly refault, while splitting creates CPU and fragmentation cost. The experiment reports bytes and page size.

### Example 8

A cgroup exceeds `memory.high`. Its tasks experience reclaim pressure and throttling while a protected sibling retains its effective boundary. Machine-wide free memory alone does not explain the observed stall.

### Example 9

Two reclaimers isolate the same logical object through different mappings. Isolation and current-reference revalidation ensure only one completes destructive removal and every acquired reference is released once.

### Example 10

After a policy change, page faults fall but memory `full` PSI and p99 request latency rise because direct reclaim waits on dirty writeback. The deployment is rolled back despite the attractive fault count.

## Cross-Program Connections

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies online algorithms, adversarial sequences, amortized analysis, and competitive bounds. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects queues, lists, counters, histograms, and concurrent indexes.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies accessed and dirty bits, TLB invalidation, caches, NUMA, and memory tiers. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames capacity, feedback, overload, liveness, observability, and assurance.

Within this program, [OS-034](034-demand-paging.md) and [OS-035](035-page-faults.md) create and service nonresidency; [OS-037](../ROADMAP.md) through [OS-039](../ROADMAP.md) apply replacement constraints to COW, mapped files, and swap.

## References

- Linux kernel documentation, [Concepts overview](https://docs.kernel.org/admin-guide/mm/concepts.html), current page checked 2026-09-04. Reclaimable and unreclaimable memory, low and minimum watermarks, background `kswapd`, direct reclaim, and allocation stalls.
- Linux kernel documentation, [Multi-Gen LRU](https://docs.kernel.org/mm/multigen_lru.html), current page checked 2026-09-04. Generations, aging, eviction, page-table and reverse-map walks, tiers, refault feedback, working-set estimation, and protection.
- Linux kernel documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), current page checked 2026-09-04. Memory accounting, `memory.min`, `memory.low`, `memory.high`, `memory.max`, `memory.reclaim`, events, and per-cgroup pressure.
- Linux kernel documentation, [PSI — Pressure Stall Information](https://docs.kernel.org/accounting/psi.html), current page checked 2026-09-04. Some and full stalls, averages, totals, triggers, cgroup scope, thrashing, and dynamic workload control.
- Linux kernel documentation, [Examining Process Page Tables](https://docs.kernel.org/admin-guide/mm/pagemap.html), current page checked 2026-09-04. Dirty, writeback, LRU, active, referenced, unevictable, anonymous, swap-cache, and swap-backed flags.
- Linux kernel documentation, [DAMON-based Reclamation](https://docs.kernel.org/admin-guide/mm/damon/reclaim.html), current page checked 2026-09-04. Proactive cold-region monitoring, reclaim, speed limits, activation watermarks, and stated scope.
- Linux man-pages project, [madvise(2)](https://man7.org/linux/man-pages/man2/madvise.2.html), current page checked 2026-09-04. Page-aligned advice, `MADV_COLD`, `MADV_PAGEOUT`, anonymous swap-out, dirty file writeback, and applicability constraints.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching treatment of virtual memory, page tables, faults, allocation, locking, and deliberate simplifications.

## Exercises

### Exercise 1

Simulate OPT, FIFO, exact LRU, and Clock on a trace with three and four frames. State assumptions, test for anomaly or inclusion, and explain implementation cost.

### Exercise 2

Design a concurrent reclaim transition for clean file, dirty file, and anonymous pages. Cover eligibility, isolation, revalidation, backing failure, unmapping, and cleanup.

### Exercise 3

Specify a multi-tenant replacement policy across cgroups and NUMA nodes. Include protection, shared ownership, local pressure, fairness, and terminal capacity policy.

### Exercise 4

Construct an experiment that distinguishes productive reclaim from thrashing. Define workload controls, metrics, thresholds, raw evidence, and rollback criteria.

### Exercise 5

Build an assurance review for page replacement on a latency-sensitive system. Address page types, huge pages, swap, writeback, hostile workloads, concurrency, and human review.

## Answers to the Exercises

### Answer 1

Start each policy empty and process the identical ordered trace at capacities three and four. OPT evicts the eligible resident whose next use is farthest or absent; FIFO replaces by arrival; LRU replaces by most recent reference order; Clock defines initial hand position, insertion bit, hit behavior, and clearing rule. Record state and miss or hit after every access.

Compare FIFO miss counts for an anomaly and compare exact-LRU resident sets after every prefix for inclusion. Do not generalize from one trace. Label OPT as future-aware and Clock as an approximation. Account for per-reference metadata, victim scan length, bit clearing, hardware support, concurrency, and page-table traversal, not only miss count.

### Answer 2

Filter out pinned, locked, unevictable, isolated, migrating, or otherwise prohibited pages before ranking. Isolate one candidate and snapshot object, mapping, dirty, writeback, reference, page-size, owner, and generation state. Revalidate after locks change and after every wait.

A clean file page can proceed toward unmapping if content remains recoverable. A dirty file page must complete or safely join writeback and handle storage error. An anonymous page requires valid swap or tier backing unless explicit discard semantics apply. Before frame reuse, remove mappings, invalidate translations, update reverse maps and histories, and account bytes exactly once. Any race restores the candidate to the correct queue and releases every reference.

### Answer 3

Define reclaim scopes by cgroup and NUMA node, with effective minimum and best-effort protection, throttle and hard-limit behavior, and node allocation policy. Charge private memory to its owning domain and define shared-cache attribution explicitly. Rank only eligible pages in the selected scope, but allow controlled escalation when local candidates cannot satisfy an allocation.

Measure reclaimed and refaulted bytes, direct-reclaim latency, PSI, remote accesses, migrations, protection events, and workload service objectives per domain. Prevent a high-scanning or high-dirtying tenant from externalizing unlimited work. Terminal policy names when to throttle, migrate, reject allocation, shed load, or invoke scoped OOM rather than silently violating protection.

### Answer 4

Use replayable locality phases: steady working set, capacity step, streaming scan, dirty burst, swap pressure, and recovery. Control memory size, CPU placement, page sizes, kernel and policy configuration, cgroups, storage, swap, cache warmup, request load, and repetitions. Preserve raw timelines.

Measure scans, skips, reactivations, evictions, writeback, swap-in and swap-out, refault age, background CPU, direct-reclaim duration, allocation latency, memory and I/O PSI, OOM events, throughput, and p50 through p99.9 latency. Productive reclaim releases bytes with tolerable refault and service cost; thrashing combines rapid refault or swap turnover with sustained stalls and lost throughput. Roll back on predefined service-objective or pressure thresholds even if faults decline.

### Answer 5

Enumerate clean and dirty file, anonymous, swap-backed, shared, pinned, device, base, huge, NUMA, and tiered states. Prove eligibility, isolation, post-wait revalidation, content preservation, mapping removal, translation invalidation, ownership, exact cleanup, bounded scanning, writeback and retry, and a defined capacity-failure response.

Inject concurrent access, unmap, migration, pinning, duplicate isolation, writeback error and timeout, swap exhaustion, compression failure, huge-page split failure, cgroup protection conflicts, local-node exhaustion, reference-bit churn, and refault storms. Preserve configurations, traces, counters, PSI, latency, and limitations. Named memory-management, filesystem, storage, architecture, security, performance, real-time, reliability, and independent-verification reviewers assess residual risk; trace simulations and passing stress tests alone do not certify the system.
