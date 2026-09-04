---
module_id: OS-034
program: Operating Systems
level: 1
module_number: 34
title: Demand Paging
status: complete
last_verified: 2026-09-04
---

# Demand Paging

## One-Page Review

### Governing question

How can an operating system defer physical allocation and data loading until access while bounding fault latency, resource use, data integrity, and failure behavior?

### Essential definitions

- **demand paging** populates a virtual page only when an access requires it.
- A **resident page** currently has usable physical memory backing under the relevant mapping.
- An **anonymous page** is not initially backed by ordinary file content; first access commonly observes zero-filled memory.
- A **file-backed page** derives content from a mapped file and may be shared through a page cache.
- A **minor fault** can be resolved without reading page content from storage, under the measurement contract in use.
- A **major fault** requires storage or otherwise blocking backing retrieval under the operating system's accounting definition.
- **readahead** fetches additional data predicted to be needed after an access or fault.

### Central model, mechanism, or theorem

For virtual page `v`, model state `S(v)` as `reserved`, `zero`, `cached`, `loading`, `resident`, `evicted`, `error`, or `invalid`, qualified by mapping generation and permissions. A valid access to a nonresident state faults. The handler revalidates the mapping, reserves bounded resources, obtains zero or backing content, verifies the result, publishes a PTE, and wakes waiters.

Demand paging trades eager work for conditional work: it reduces initial allocation and I/O for untouched pages, but transfers latency and failure into first access. Correct policy controls admission, concurrent-fault coalescing, readahead, memory pressure, deadlines, and recovery.

### Critical invariants

- Every newly exposed anonymous byte is zeroed before user access unless an explicit initialized source replaces it.
- File-backed content corresponds to the validated object, offset, length, mapping generation, and truncation policy.
- Concurrent faults for one page publish at most one authoritative result and release losing resources.
- Fault handling never exceeds configured memory, I/O, wait, readahead, or retry budgets.
- A mapping change, unmap, truncate, or process exit prevents stale fault completion from installing obsolete state.
- Published PTEs have correct permissions and are ordered with page initialization and translation-cache rules.
- Fault metrics distinguish access population, copy-on-write, protection, storage wait, and fatal errors.

### Common failures

Common mistakes are assuming virtual reservation commits memory, exposing uncleared frames, performing duplicate reads for concurrent faults, holding a mapping lock across uncontrolled I/O, installing a page after its region was unmapped, treating every minor fault as cheap, issuing unbounded readahead, using residency probes as stable reservations, confusing overcommit with available memory, and benchmarking after warmup while claiming first-touch performance.

### Compact example

A process maps 16 pages anonymously but touches only indices 0, 3, 3, 9, and 15. Demand paging allocates four distinct zeroed pages rather than sixteen; the repeated touch to page 3 is a hit after its first fault. If four threads fault page 9 together, one owner initializes and publishes it while the others wait and revalidate. Allocation failure returns the documented fault outcome rather than exposing partial state.

### Connections

[OS-031](031-address-translation.md), [OS-032](032-page-tables.md), and [OS-033](033-translation-lookaside-buffers.md) supply translation and publication. [OS-035](../ROADMAP.md) expands fault classification, and [OS-036](../ROADMAP.md) explains how resident pages become eviction candidates.

## Governing Question

Virtual memory lets software reserve and describe more address space than it immediately backs with physical frames. Demand paging realizes the promise only when a load, store, or instruction fetch reaches an unpopulated page. That fault can allocate zero memory, find cached file data, wait for storage, or fail.

The governing question is how to move work into this exceptional path without making behavior unbounded or racy. The design must preserve mapping identity across waits, coordinate duplicate faults, publish initialized bytes, respect pressure, and report latency honestly.

## Why This Matters

Demand paging shortens process startup, supports sparse heaps and stacks, shares file cache, enables memory-mapped databases, and makes copy-on-write practical. Untouched code and data need not consume resident memory or I/O bandwidth.

The costs arrive at inconvenient times. First request latency can include page-table allocation, zeroing, filesystem lookup, storage, decompression, reclaim, and scheduling. Under pressure, faulting can form feedback loops: stalled threads hold resources, reclaim generates I/O, and latency triggers more concurrency.

Security and correctness are inseparable. New pages must not disclose old data. A delayed read must not populate a mapping that now names another file generation. User-space fault delegation must validate layout changes and liveness.

## Prerequisites and Retrieval

Review [OS-031](031-address-translation.md), [OS-032](032-page-tables.md), and [OS-033](033-translation-lookaside-buffers.md). Recall wait queues from [OS-015](015-process-states-and-wait-queues.md), concurrency from [OS-021](021-critical-sections-in-the-kernel.md), and file mappings from [OS-027](027-shared-memory.md).

Retrieve these distinctions:

- reserving virtual range, committing backing, making a page resident, and locking it resident are different;
- missing PTE, nonresident data, copy-on-write, and protection denial can all fault for different reasons;
- minor and major are accounting categories, not universal latency guarantees;
- page cache identity includes backing object and offset, not merely virtual address;
- readahead is speculation and must be bounded separately from demanded work;
- residency observation can become stale immediately;
- successful fault resolution and durable file update are unrelated guarantees.

## Learning Objectives

After this module, you should be able to:

1. model anonymous, file-backed, cached, loading, resident, evicted, error, and invalid page states;
2. trace first-touch allocation, zero fill, page-cache lookup, storage read, and PTE publication;
3. design concurrent-fault coalescing with mapping-generation revalidation;
4. bound readahead, I/O, memory, wait, retry, and overload;
5. reason about truncation, unmap, copy-on-write, userfault handling, NUMA, huge pages, and overcommit;
6. distinguish residency, minor and major fault counters, latency, and working-set evidence;
7. build reproducible cold, warm, pressure, and failure experiments.

## Core Exposition

### Reservation versus population

Creating a mapping establishes virtual-region metadata and an access contract. It need not allocate a private physical frame for every page. The first qualifying access can allocate page tables and backing memory.

Applications must not treat a large successful reservation as proof that later writes cannot fail or trigger system-wide pressure. Admission includes overcommit, resource controls, and the fault-time failure policy.

### Anonymous first touch

Anonymous memory must initially read as zero under the mapping contract. Implementations can map a shared read-only zero page for reads and allocate a private zeroed frame on write, or allocate earlier. The observable rule is initialized zero content and correct permissions.

Zeroing consumes bandwidth. Reusing a frame without clearing it leaks information. Hardware-assisted clearing, background zeroing, and larger pages change cost but not the confidentiality invariant.

### File-backed first touch

A file-backed fault computes object offset from mapping offset and virtual-page position, validates it against file and region state, and looks in the page cache. If content is present and valid, the handler can install a mapping without storage read. Otherwise it initiates or joins retrieval.

Short final pages, holes, truncation, I/O error, filesystem semantics, and shared versus private mapping affect the result. Bytes beyond valid backing cannot be invented from stale memory.

### Page cache

The page cache lets reads and mappings share cached file content. Cache residency is not synonymous with a PTE in one process. A page can be cached yet unmapped, or mapped in many address spaces.

Identity and invalidation follow the backing object and offset. Replacement, truncation, direct I/O interactions, and writeback require filesystem contracts beyond the demand-fault core.

### Minor and major faults

Operating systems expose fault counters such as minor and major. A minor fault often means resolution without backing-device I/O; it can still allocate, zero, lock, contend, invalidate, or wait. A major fault indicates a path accounted as requiring blocking retrieval, but exact definitions are platform-specific.

Never infer latency from the category alone. Measure fault duration and correlated I/O, reclaim, and scheduling under the target kernel.

### Fault path

The handler decodes fault address, access type, privilege, and architecture cause. It locates region metadata under appropriate synchronization and rejects invalid or prohibited access. For a valid missing page, it selects anonymous, file, swap, shared, or delegated handling.

Operations that sleep or perform I/O often require releasing locks. On reacquisition, revalidate mapping generation, permissions, object identity, and current PTE before publication.

### Concurrent faults

Several threads can fault the same page. Without coordination they may allocate or read duplicates and race to install results. A per-page loading marker, locked cache entry, or compare-and-publish protocol elects an owner and lets others wait or independently prepare with safe loser cleanup.

Wakeups occur after result or error state is visible. Waiters loop and recheck because mapping changes, signals, cancellation, and spurious wakes can alter outcomes.

### Stale completion

A fault can wait on storage while another thread unmaps the range, changes permissions, remaps another object at the same address, or truncates the file. Virtual address equality does not prove the original request remains current.

Carry mapping or object references and a generation. Before installing, compare current region, offset, access, generation, and PTE. A stale result may remain useful in the page cache but cannot enter the obsolete virtual mapping.

### PTE publication

Initialize content and metadata before making a leaf reachable. Install permissions consistent with the fault and region; a read fault need not grant write. Apply architecture-defined page-table ordering and translation invalidation where required.

Update reverse mappings, reference counts, accessed state, and accounting in an order that leaves cleanup safe on every failure path.

### Readahead

Sequential access often benefits from fetching pages beyond the immediate fault. Readahead converts future storage waits into background or batched work. Random access can make it waste I/O, cache capacity, memory bandwidth, and useful pages.

Bound window, outstanding reads, bytes, and per-tenant impact. Adapt from observed access without allowing one stream to evict unrelated hot data. Demand work retains priority over speculative work.

### Advice interfaces

Applications can provide sequential, random, needed, or discard advice through platform interfaces. Advice is generally policy input rather than a correctness or residency guarantee. Effects differ by mapping type and kernel.

Use advice to improve measured behavior, not to remove explicit latency and failure handling. Validate flags and page-aligned range semantics.

### Prefaulting

Touching pages or using population interfaces can shift faults out of a latency-critical phase. Prefaulting consumes memory and bandwidth even for unused pages and can create synchronized bursts.

Stage and rate-limit warming. Verify that pages remain resident until use or use a locking mechanism under limits when the requirement truly demands it.

### Residency probes

Interfaces such as Linux `mincore` report page residency at observation time under their contract. Another thread or reclaim can change it immediately. Residency does not guarantee a later access avoids all faults or waits.

Treat probes as diagnostics or hints. They can expose page-presence information and therefore carry security and permission considerations.

### Memory locking

Locking pages can prevent ordinary eviction and reduce some latency variance, subject to resource limits and platform semantics. It does not necessarily prepopulate every page unless requested through the correct interface and flags.

Locked memory consumes scarce resident capacity. Admission and cleanup must prevent one process from starving the system.

### Huge-page demand

Faulting a huge page can populate a large aligned region and improve TLB reach, but allocation, zeroing, collapse, and copy-on-write costs are larger. Under fragmentation, a huge allocation can fail or trigger compaction.

Transparent policies may fall back to base pages. Record the page size actually obtained and measure first-touch as well as steady state.

### NUMA placement

First touch often influences which NUMA node backs anonymous memory, subject to policy. The thread doing initialization may not be the eventual owner. Parallel initialization can distribute pages or accidentally create remote access.

State node policy, CPU placement, migration, and rebalancing. Benchmark topology-aware first touch and production access patterns.

### Copy-on-write interaction

A private file or fork-shared page can be resident but write-protected for copy-on-write. A write fault allocates and copies a private page rather than retrieving original content. This is demand allocation driven by protection state.

Concurrent copy faults, pins, huge-page splits, allocation failure, and stale region changes need the same revalidation and publication discipline.

### Swap and compressed backing

An evicted anonymous page may be represented by a nonpresent swap or compressed-store entry. Fault resolution retrieves, decompresses, verifies, and installs it. Storage and CPU costs vary by tier.

Corruption, I/O failure, depleted swap, and concurrent swap-in require explicit outcomes. A success counter does not prove acceptable tail latency.

### Memory pressure and reclaim

Fault-time allocation can trigger direct reclaim or compaction, making application threads perform memory-management work. Reclaim can wait for writeback and compete for I/O with the page being demanded.

Resource controls, reserved memory, admission, background reclaim, and working-set sizing reduce but do not eliminate pressure. Track pressure and reclaim time alongside faults.

### Overcommit and OOM

Systems can permit virtual commitments larger than immediately available backing under policy. Later population may fail or cause an out-of-memory response that selects a victim. A successful mapping call is therefore not a complete availability guarantee.

Critical systems reserve, pre-fault, lock, or otherwise provision resources according to platform contracts, while still planning for hardware error and process failure.

### User-space fault handling

Linux `userfaultfd` can delegate missing, minor, or write-protect fault handling for registered regions and supported backing. Faulting threads can remain stopped until a monitor supplies, continues, or rejects the page.

The monitor negotiates features, tracks fork, remap, remove, and unmap events as required, validates addresses and generations, bounds queues and latency, and survives or fails safely. It is useful for post-copy migration and checkpoint restoration but creates a new liveness dependency.

### Deadlocks and reentrancy

Fault handlers allocate memory, take locks, and may perform filesystem I/O. If a caller faults while holding a lock needed by the handler or reclaim path, the system can deadlock. Kernel code distinguishes contexts where faults or sleeping are forbidden.

User-space real-time and signal code similarly avoids unexpected faults by controlling stacks, buffers, and residency before entering constrained regions.

### Security

Zero new pages, validate file bounds, prevent stale installation, constrain userfault managers, and limit residency disclosure. Malicious access patterns can cause fault storms, sparse page-table growth, storage thrash, or readahead pollution.

Apply per-domain memory and I/O limits, validate fault rates, and ensure error paths do not reveal prior content or map unintended frames.

### Observability

Record faults by cause and outcome, latency distribution, page-cache hit, storage and decompression time, zeroing, allocation, reclaim, compaction, readahead issued and useful, waiters coalesced, stale completions, page size, NUMA node, and OOM events.

Trace carefully: page-fault probes and cold-cache preparation alter scheduling and cache state. Preserve kernel, filesystem, device, memory pressure, mapping, workload, and raw samples.

### Assurance

Review demand paging as an asynchronous state machine with untrusted timing. Prove zeroing, identity, bounds, owner election, stale-result rejection, publication, and terminal error behavior. Inject failures at allocation, I/O, revalidation, and wakeup boundaries.

Performance evidence covers cold, warm, pressure, and failure regimes. Passing first-touch tests does not certify confidentiality, liveness, or worst-case latency.

## Definitions and Notation

For virtual page `v` and mapping generation `g`, state `S(v,g)` is one of `reserved`, `zero`, `cached`, `loading`, `resident`, `evicted`, `error`, or `invalid`. A transition publishes only if current region generation and object identity still equal those captured by the fault.

Let demanded set be `D`, populated set `P`, and resident set `R`. In general, `D`, `P`, and `R` vary over time: a demanded page can later be evicted, and a prefetched resident page may never be demanded. Do not assume permanent subset relations without a time index.

For observation window, let fault count be `F`, total fault time `T_f`, demanded I/O bytes `B_d`, speculative readahead bytes `B_r`, and useful readahead bytes `B_u`. Readahead usefulness ratio `B_u/B_r` is defined only when `B_r>0` and does not by itself capture latency benefit or eviction harm.

## Mechanisms, Invariants, or Proof Structure

A reviewable demand-paging design follows ten obligations:

1. Define mapping, backing object, offset, permissions, generation, and page-size state.
2. Classify missing, cached, copy-on-write, evicted, protected, delegated, error, and invalid faults.
3. Zero anonymous frames and validate file content and bounds before exposure.
4. Elect or coordinate concurrent fault owners and release all losing resources.
5. Bound allocation, I/O, readahead, waiters, retries, deadlines, and per-domain pressure.
6. Revalidate mappings after every unlocked wait and reject stale completion.
7. Publish content, PTE, reverse mapping, accounting, wakeup, and invalidation in safe order.
8. Define reclaim, overcommit, OOM, truncation, unmap, exit, and handler failure.
9. Treat advice, residency, counters, and userfault features according to platform scope.
10. Measure cold, warm, pressure, NUMA, huge-page, and failure behavior separately.

The executable model shows repeated touches allocate one page per distinct demanded index rather than one page per access or reservation.

<!-- bijux-verify: {"id":"toy-demand-population","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"reserved=16\ntouches=0,3,3,9,15\nfaults=4\nresident=0,3,9,15\nuntouched=12\n","stderr":""}} -->
```python
reserved = 16
touches = [0, 3, 3, 9, 15]
resident = set()
faults = 0

for page in touches:
    assert 0 <= page < reserved
    if page not in resident:
        resident.add(page)
        faults += 1

print(f"reserved={reserved}")
print("touches=" + ",".join(map(str, touches)))
print(f"faults={faults}")
print("resident=" + ",".join(map(str, sorted(resident))))
print(f"untouched={reserved - len(resident)}")
```

The toy models only distinct first touches. It omits frames, zeroing, page tables, file cache, I/O, concurrency, eviction, pressure, failures, and timing.

## Alternatives and Trade-Offs

- Demand population avoids work for untouched pages but moves latency and failure to access.
- Eager population stabilizes a later phase but spends memory and bandwidth up front.
- Readahead can hide sequential I/O but pollutes cache for random or adversarial patterns.
- Shared zero pages reduce read-only anonymous allocation but require copy-on-write for mutation.
- Per-page fault serialization avoids duplicate work but can concentrate waiter latency.
- Speculative duplicate preparation reduces locking but wastes resources and complicates loser cleanup.
- Huge-page faults improve translation reach but increase allocation, zeroing, and fragmentation cost.
- User-space fault handling enables migration and custom policy but adds a liveness and security dependency.
- Memory locking reduces eviction variance but consumes scarce resident capacity.

## Failure Modes and Misconceptions

1. **“A successful mapping allocates every page.”** reservation and population are separate.
2. **“Anonymous memory needs no initialization.”** reused frames must not disclose old bytes.
3. **“A minor fault is free.”** it can allocate, contend, zero, and schedule.
4. **“A major fault always means one disk read.”** accounting and backing tiers vary.
5. **“Concurrent faults safely duplicate.”** publication, accounting, and loser cleanup can race.
6. **“The address still means the same after I/O.”** unmap, remap, and truncate can change it.
7. **“Readahead cannot hurt.”** it consumes I/O, memory, and cache capacity.
8. **“Residency probes reserve pages.”** observation can become stale immediately.
9. **“Warm benchmarks measure demand paging.”** they exclude first-touch and retrieval.
10. **“Overcommit creates memory.”** later population still faces finite resources.
11. **“Locked means already resident.”** flags and platform behavior determine population.
12. **“Huge faults are ordinary faults with more bytes.”** allocation and transition constraints differ.
13. **“Userfault delegation cannot corrupt the client.”** stale layout handling and supplied content matter.
14. **“Fault counts explain latency.”** duration, cause, coalescing, reclaim, and scheduling are required.

## Worked Examples

### Example 1

A process reserves 16 anonymous pages and touches four distinct indices. Four pages populate; twelve remain unpopulated. Repeated access to one resident page does not fault again absent eviction or permission change.

### Example 2

Two threads first-write one anonymous page. Both allocate; compare-and-publish installs one. The losing zeroed frame is released and accounting decremented exactly once.

### Example 3

A file fault starts I/O at offset 1 MiB. The mapping is replaced before completion. Generation validation rejects installation into the new mapping while the page cache may retain valid old-object data.

### Example 4

Sequential access makes 90 percent of readahead bytes useful and reduces major-fault stalls. Random access makes most speculative bytes unused and evicts a hot index. Adaptive bounded windows distinguish them.

### Example 5

A latency test warms every page before timing and reports no faults. It measures resident access, not startup. A separate cold run includes controlled cache state and first-touch distribution.

### Example 6

Anonymous allocation under pressure enters direct reclaim and waits for file writeback. The fault itself uses no swap read, yet latency is high. Pressure and reclaim metrics explain it.

### Example 7

A first-touch initialization thread runs on NUMA node 0, while workers run on node 1. Pages remain remote. Worker-local initialization or explicit memory policy changes placement.

### Example 8

A huge anonymous write fault cannot obtain contiguous backing and triggers compaction before falling back. Median improves later, but p99 startup worsens; both phases belong in the decision.

### Example 9

A userfault monitor crashes with clients stopped on missing pages. A supervisor-enforced timeout terminates or switches to a documented fallback instead of leaving indefinite waits.

### Example 10

An attacker maps a sparse range and touches one page in each distant region, consuming data and page-table memory. Per-domain accounting and admission bound the fault storm.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) connects mapped files, cache, writeback, and recovery. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies memory hierarchy, NUMA, TLBs, and page-walk costs.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames zeroing, stale mappings, residency disclosure, and denial of service. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity, latency, failure, observability, and assurance reasoning.

Within this program, [OS-031](031-address-translation.md) through [OS-033](033-translation-lookaside-buffers.md) provide translation mechanics; [OS-035](../ROADMAP.md), [OS-036](../ROADMAP.md), and [OS-037](../ROADMAP.md) cover fault handling, replacement, and working sets.

## References

- Linux kernel documentation, [Memory Management Concepts](https://docs.kernel.org/admin-guide/mm/concepts.html), current page checked 2026-09-04. Virtual memory, demand paging, anonymous memory, page cache, reclaim, compaction, NUMA, and OOM.
- Linux kernel documentation, [Page Tables](https://docs.kernel.org/mm/page_tables.html), current page checked 2026-09-04. Fault paths, missing mappings, table allocation, read, copy-on-write, shared faults, and MMU updates.
- Linux kernel documentation, [Memory Management APIs](https://docs.kernel.org/core-api/mm-api.html), current page checked 2026-09-04. Page-cache operations, readahead triggers, folio retrieval, errors, and kernel allocation interfaces.
- Linux kernel documentation, [Userfaultfd](https://docs.kernel.org/admin-guide/mm/userfaultfd.html), current page checked 2026-09-04. Missing, minor, and write-protect modes, feature negotiation, resolution, security, and use cases.
- Linux man-pages project, [userfaultfd(2)](https://man7.org/linux/man-pages/man2/userfaultfd.2.html), current page checked 2026-09-04. Fault delegation, modes, events, lifecycle, nonblocking I/O, fork, remap, remove, and unmap.
- Linux man-pages project, [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), current page checked 2026-09-04. Anonymous and file mappings, population, locking, huge pages, faults, sharing, and backing-size caveats.
- Linux man-pages project, [madvise(2)](https://man7.org/linux/man-pages/man2/madvise.2.html), current page checked 2026-09-04. Access-pattern advice, population, discard, huge-page, fork, and reclamation behaviors.
- Linux man-pages project, [mincore(2)](https://man7.org/linux/man-pages/man2/mincore.2.html), current page checked 2026-09-04. Residency observation, alignment, vector sizing, errors, and non-stable snapshots.
- Linux man-pages project, [mlock(2)](https://man7.org/linux/man-pages/man2/mlock.2.html), current page checked 2026-09-04. Resident locking, population flags, limits, inheritance, errors, and real-time concerns.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching lazy allocation, page faults, zeroing, fork, copy-on-write exercises, and address-space lifecycle.

## Exercises

### Exercise 1

Design anonymous demand allocation for concurrent first reads and writes. Include zero pages, private frames, owner election, accounting, failure, and stale mapping.

### Exercise 2

Specify a file-backed fault state machine. Cover page-cache identity, storage I/O, coalescing, truncation, unmap, short final page, error, and publication.

### Exercise 3

Design bounded adaptive readahead for sequential and random workloads. Include fairness, usefulness metrics, memory pressure, cancellation, and cold testing.

### Exercise 4

Construct an experiment separating minor, major, copy-on-write, reclaim, and huge-page fault cost across warm and cold regimes.

### Exercise 5

Build an assurance review for user-space fault handling during post-copy migration. Cover liveness, generations, corruption, overload, evidence, and human review.

## Answers to the Exercises

### Answer 1

Represent the region as valid but unpopulated with a generation. A first read may install a shared read-only zero page; a first write allocates a private frame and clears it completely. A per-page marker or PTE lock elects an owner. Waiters sleep on state and recheck generation, permissions, and current PTE after wake.

If duplicate preparation is permitted, only one compare-and-publish succeeds and every loser releases its frame and provisional accounting. Before publication, verify the region still exists and refers to the same generation. Allocation failure leaves no reachable partial page and yields the documented process or API outcome. A later write to the shared zero mapping enters copy-on-write.

### Answer 2

Derive backing key from referenced object identity and page-aligned offset under a stable mapping generation. Look up or create a loading cache entry. One owner issues bounded retrieval; peers wait without holding mapping locks. Validate I/O length, checksum or filesystem status where applicable, holes, and final-page zero rules.

After I/O, reacquire mapping state and compare object, offset, generation, permissions, and PTE. Truncation or unmap makes virtual installation stale even if cache content is valid for the old object. Publish initialized cache state before the PTE and wake waiters after terminal success or error is visible. Release references and error accounting exactly once.

### Answer 3

Begin with a small per-stream window and grow only after consecutive demanded pages validate sequentiality. Cap pages, bytes, outstanding I/O, total cache share, and per-tenant share. Random or backward access shrinks or disables the window. Demand reads outrank speculative requests; pressure and low usefulness reduce global budgets.

Track issued `B_r`, later demanded `B_u`, latency avoided, demand displaced, cancellations, and cache age. Cancel obsolete windows on unmap, close, and pattern change when supported. Compare disabled, fixed, and adaptive policies using controlled cold state, identical traces, representative storage, pressure, multiple tenants, repeated runs, and raw tail latency.

### Answer 4

Create separate phases: resident warm access; absent PTE with cached backing; anonymous zero first touch; file data absent from cache; copy-on-write; direct reclaim and writeback pressure; base-page and actual huge-page first touch. Validate achieved state using platform diagnostics without claiming the diagnostic reserves it.

Record fault cause and counters, per-fault and application latency, storage, zeroing, allocation, reclaim, compaction, page size, cache state, CPU, NUMA node, memory pressure, context switches, and high percentiles. Control kernel, filesystem, device, mapping flags, affinity, frequency, background load, and repetitions. Major/minor labels remain platform accounting, while measured duration supports latency claims.

### Answer 5

Negotiate exact userfault features and register bounded generation-tagged ranges. The monitor authenticates migration source, validates address, page size, generation, access flags, and content before atomic copy or continue. Track fork, remap, remove, and unmap events so delayed pages cannot populate reused layouts. Bound event queue, in-flight fetches, memory, bandwidth, retry, and per-page deadline.

Monitor crash, network partition, corrupt page, duplicate event, client exit, remap race, and overload invoke documented termination, retry, or safe fallback; faulting threads never wait indefinitely beyond policy. Preserve kernel and feature versions, topology, traces, raw fault latency, completion, and corruption tests. Named kernel, migration, runtime, network, security, performance, operations, safety, and independent-verification reviewers assess residual risk. A successful migration demo is not certification.
