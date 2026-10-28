---
module_id: OS-044
program: Operating Systems
level: 1
module_number: 44
title: Filesystem Free-Space Management
status: complete
last_verified: 2026-09-04
---

# Filesystem Free-Space Management

## One-Page Review

### Governing question

How should a filesystem represent, find, reserve, allocate, reclaim, verify, and report free storage efficiently without double allocation, silent leaks, unfair exhaustion, or crash-induced inconsistency?

### Essential definitions

- **Free space** is storage eligible for allocation under the filesystem's ownership and policy rules.
- A **bitmap** records allocation state with bits indexed by allocation unit.
- A **free-space extent** records the start and length of one contiguous free run.
- A **summary** compresses free-space facts, such as total free units or largest run, to prune searches.
- A **reservation** promises capacity to future work without necessarily selecting final physical units.
- A **locality group** or allocation region partitions search, locking, and placement responsibility.
- **Discard** or **trim** informs a lower layer that selected logical device ranges no longer contain live filesystem data.
- A **leak** is allocated-but-unreachable space; a **cross-link** is ordinary space claimed incompatibly by multiple owners.

### Central model, mechanism, or theorem

Partition allocatable storage into units `U`. Let authoritative ownership `O_t(u)` be `free`, `reserved(r)`, or `owned(x)` at time `t`. Search indexes `I_t`, counters `C_t`, reservations `Q_t`, quotas, file maps, metadata maps, and device-discard state are related views with explicit freshness and recovery rules.

Allocation is a transaction from eligible free units to one owner; release is the reverse only after no live or recovery reference remains. Correctness requires exclusive ownership, capacity conservation, bounded and policy-compliant search, atomic publication, safe initialization, idempotent recovery, and reconciliation in both directions. A fast summary may be stale within declared bounds, but it must never authorize allocation without validating authoritative state.

### Critical invariants

- Every allocatable unit has exactly one logical state: free, reserved by a named claim, or owned by valid filesystem state.
- No unit containing live data, metadata, journal state, snapshot reference, bad-block exclusion, or recovery work appears allocatable.
- Counters, bitmaps, free-extent indexes, buddy summaries, reservations, quotas, and owner mappings reconcile under their declared consistency points.
- Allocation publishes ownership only after capacity and metadata credit are secured; failure unwinds each reservation exactly once.
- Release makes a unit reusable only after stale mappings, cache state, references, and recovery obligations are gone.
- Crash recovery cannot turn one physical unit into two owners or disclose a former owner's bytes.
- User-visible free-space reports state whether capacity is immediately available, privileged, reserved, delayed, reclaimable, or provisioned elsewhere.

### Common failures

Common mistakes are trusting a free counter without checking fragmentation, treating discard as deallocation, exposing reserved blocks to unprivileged callers, updating a bitmap without its checksum or group counter, forgetting metadata space needed to allocate data, double-releasing a canceled reservation, reusing blocks still referenced by a snapshot, assuming thin-provisioned logical free space implies physical capacity, and repairing from one damaged free-space index without cross-checking owners.

### Compact example

A bitmap for sixteen blocks marks `0–2`, `6–8`, and `12–15` allocated. A four-block request cannot use the six free blocks in aggregate unless it accepts multiple extents; the only contiguous run of length four is `12–15`, which is not free. A contiguous request therefore fails while a scattered request may succeed. Total free count and allocation feasibility are different questions.

### Connections

[OS-043](043-file-allocation.md) defines file mappings and ownership transitions. [OS-046](../ROADMAP.md) and [OS-047](../ROADMAP.md) develop journaling and crash consistency; [OS-050](../ROADMAP.md) composes them into a filesystem design.

## Governing Question

Free space looks like absence, but a filesystem must represent it positively enough to find useful ranges quickly and prove that no live owner still needs them. Every allocation changes both an owner's map and global capacity state.

The governing question is how to make this cross-structure transition fast under concurrency and recoverable after failure. The answer separates authoritative ownership, search accelerators, reservations, policy, reporting, and lower-layer reclamation hints.

## Why This Matters

Every create, write, copy-on-write fault, directory split, xattr growth, journal transaction, and repair operation can need storage. Data allocation can fail even when a free-byte counter looks healthy because metadata, alignment, region, quota, or contiguous-run constraints are exhausted.

A free-space bug can corrupt the whole filesystem. Double allocation lets independent objects overwrite one another. A leak consumes capacity indefinitely. Premature reuse or discard can destroy data still required by snapshots, journals, or recovery.

Free-space policy also drives performance and fairness. Locality, fragmentation, parallelism, wear, reserved capacity, project quotas, and thin provisioning determine which workload succeeds and where its bytes land.

## Prerequisites and Retrieval

Review [OS-021](021-critical-sections-in-the-kernel.md), [OS-025](025-deadlock-conditions-and-avoidance.md), [OS-037](037-copy-on-write.md), [OS-042](042-inodes-and-metadata.md), and [OS-043](043-file-allocation.md).

Retrieve these distinctions:

- a file map records ownership, while a free-space structure records eligible absence of ownership;
- data units, metadata units, journal credits, quotas, and device capacity can be exhausted independently;
- total free units do not imply a sufficiently long aligned run;
- a reservation reduces available capacity before final placement but is not necessarily a physical mapping;
- a cache or summary accelerates search but does not replace authoritative validation;
- logical device deallocation and physical media erasure are separate contracts;
- snapshots and reflinks preserve physical ownership beyond one file mapping;
- visible free space, safely allocatable space, privileged reserve, and lower-layer provisioned capacity differ.

## Learning Objectives

After this module, you should be able to:

1. compare bitmaps, free lists, extent trees, buddy summaries, counting schemes, and log-structured reclamation;
2. design region, locality, alignment, fragmentation, and concurrency policies;
3. trace reservation, allocation, release, discard, and recovery as ownership transitions;
4. explain metadata reserves, quotas, snapshots, thin provisioning, zoned devices, and online resize constraints;
5. specify counters, summaries, checksums, caches, and their validation boundaries;
6. construct bidirectional consistency checks and conservative repair procedures;
7. test capacity behavior, failures, crashes, fairness, performance, and evidence.

## Core Exposition

### Free space as state

A unit is free only if no live data, metadata, journal, snapshot, bad-block, or recovery owner claims it and policy makes it eligible. “Not found in one file” is not enough evidence.

The authoritative state can be encoded directly or derived during reconstruction. Search structures and counters are secondary views unless the format explicitly makes them authoritative.

### Allocation granularity

Filesystems allocate blocks, clusters, segments, zones, or variable-size objects. One bitmap bit can represent one block or a larger cluster.

Larger granularity shrinks metadata and favors large files but increases internal fragmentation. The format must make units, reserved prefixes, device boundaries, and tail fragments unambiguous.

### Bitmaps

A bitmap provides compact exact state and constant-time test or update for a known unit. Word-at-a-time scanning and CPU bit operations can locate candidate runs.

Finding a long range may scan many bits, especially near capacity. In-memory summaries or buddy structures accelerate search, while the persistent bitmap remains validated at allocation.

### Bitmap boundaries

Mapping unit `u` to byte and bit uses checked division and remainder. The final bitmap byte can include padding bits that must remain allocated or otherwise ineligible.

Filesystem metadata residing inside an apparent group is marked unavailable even during lazy initialization. Off-by-one mistakes at group or device ends are corruption bugs.

### Free lists

A linked free list is simple and supports constant-time single-unit removal when a head is available. It performs poorly for contiguous-range search and is vulnerable to lost nodes, cycles, duplicates, and damaged links.

Grouping multiple free addresses in one block improves traversal but makes those blocks bootstrap metadata. Recovery proves the list contains every eligible unit exactly once.

### Counting free runs

A run list records `(start,length)` rather than every free unit. It is compact when free space is contiguous and supports range allocation naturally.

Allocation splits or shortens records; release inserts and coalesces neighbors. Heavy fragmentation expands the index, and concurrency must prevent overlapping insertions.

### Free-space trees

Balanced trees index free extents by address, length, or both. Address order supports adjacency and coalescing; length order finds best-fit candidates efficiently.

Maintaining two indexes requires transactional agreement. Tree nodes themselves consume space, so low-space operations reserve metadata needed to update the free-space structure.

### Buddy summaries

A buddy structure groups power-of-two aligned free runs by order. Allocation splits larger buddies; release coalesces with a free partner.

It finds aligned runs quickly but rounds requests or combines a bitmap with derived buddy summaries. Filesystem-specific multiblock allocators may use buddy information as an in-memory search accelerator over persistent bitmaps.

### Hierarchical summaries

Per-region counters, largest-run values, histograms, and tree-node aggregates prune regions that cannot satisfy a request. A false negative can strand usable capacity; a false positive costs search and must be rejected by authoritative validation.

Concurrent updates can make relaxed summaries temporarily approximate. Their allowed error, refresh trigger, and recovery reconstruction are part of the design.

### Allocation regions

Block groups or allocation groups partition capacity, locks, counters, and indexes. Region-local operations scale and contain damage, while higher-level selection spreads or groups workloads.

Fixed region sizes simplify addressing. Flexible groupings can place metadata together and enable longer runs but complicate locality and feature interpretation.

### Region selection

Selection considers preferred device, file or directory locality, requested length, free count, largest run, fragmentation, temperature, quota domain, and contention.

Fallback broadens search deterministically and terminates. Repeatedly scanning impossible regions under near-full conditions can turn capacity pressure into a denial of service.

### First fit

First fit selects the first eligible run in search order. It is simple and fast when search hints are good but can concentrate fragmentation at the beginning.

Rotating the starting hint spreads work. A hint is never authority; validate that the candidate is still free after acquiring the required lock.

### Best fit and worst fit

Best fit minimizes immediate leftover size but can create many tiny fragments. Worst fit preserves medium runs by consuming the largest but can destroy scarce large extents.

Policies use size classes, locality goals, and workload evidence rather than assuming one heuristic dominates. Correctness is independent of the chosen fit rule.

### Alignment and boundaries

Direct I/O, erase units, RAID stripes, zones, atomic-write units, and metadata structures impose alignment or boundary constraints. The allocator rounds and validates without overflowing or crossing forbidden ranges.

Alignment padding can remain free or become part of a reservation under declared accounting. Report why aggregate space was unsuitable.

### Locality

Keeping related data and metadata near each other can reduce seeks or I/O requests. Keeping independent hot workloads apart can increase device parallelism and reduce contention.

Locality is a policy objective, not an ownership invariant. When the preferred region is full, correct fallback is better than falsely returning global exhaustion.

### Fragmentation metrics

Total free count, number of free extents, largest free extent, size histogram, and entropy-like distribution measures describe different aspects. File extent count measures allocated layout, not the free-space map directly.

Evaluate allocation latency and I/O effects at multiple fullness levels. One scalar fragmentation score cannot explain every workload and device.

### Reservations

Delayed allocation, copy-on-write, transactions, and repair can reserve space before final placement. A reservation has owner, quantity, class, lifetime, and release or consumption rules.

Admission subtracts reservations from availability. Cancellation releases exactly once; allocation converts the same claim rather than charging twice.

### Data and metadata reserves

A request for data can require new extent-tree nodes, checksums, reference-count records, journal blocks, or free-space-tree updates. Consuming the final unit as data can make it impossible to record ownership safely.

Separate or worst-case metadata reserves keep forward progress. Emergency capacity is narrowly scoped and audited so privileged operations do not silently consume user guarantees.

### Root reserves

Some filesystems withhold a fraction or fixed amount for privileged recovery and essential services. User-visible reports distinguish total free from unprivileged available capacity.

The reserve improves recovery under fullness but is not infinite. Policy defines eligible callers and prevents ordinary privileged workloads from exhausting it accidentally.

### Quotas

User, group, project, or dataset quotas limit allocation independently of global space. Reservations charge the appropriate domain before dirty work is admitted.

Ownership transfer, reflink, snapshots, compression, and delayed allocation require a stated accounting unit. Quota counters reconcile with allocation and reservations after recovery.

### Copy-on-write reserves

Shared blocks save current space but a future write may require a full private copy plus mapping metadata. Systems choose guaranteed reserve, pessimistic admission, overcommit, or failure-on-write semantics.

Snapshots can therefore transform an apparently in-place overwrite into allocation pressure. Observability reports exclusive, shared, referenced, and reserved quantities separately.

### Release ordering

Truncate, unlink, overwrite, and snapshot deletion eventually release storage. The last owner disappears only after mapping removal, cached I/O exclusion, reference-count update, and recovery logging make reuse safe.

Publishing “free” before removing an old reference invites double ownership. Delaying release is a leak risk but safer than premature reuse until recovery resolves intent.

### Deferred free

Large operations can exceed one transaction. Deferred intents record work so later transactions finish release without losing ownership history.

Recovery replays unfinished intents idempotently. Each extent is either still owned, transferred to a durable intent, or free—never absent from every account.

### Journaling free-space changes

Bitmap, counter, mapping, quota, and reference changes participate in a journal transaction or equivalent ordered protocol. Replay applies committed updates and ignores incomplete ones.

Transaction credits include splits and coalesces that the free-space index may need. Low-space handling cannot depend on allocating unreserved metadata recursively.

### Copy-on-write free-space trees

A copy-on-write filesystem constructs updated free-space and ownership trees in new blocks, then publishes a new root. Old roots remain valid until no snapshot or recovery point needs them.

Root publication reduces in-place inconsistency but creates bootstrap and reserve obligations: updating the space tree itself consumes space tracked by that tree.

### Counters and `statfs`

Global and per-group counters accelerate reporting and region choice. User APIs can report total blocks, free blocks, and blocks available to an unprivileged caller with filesystem-specific interpretations.

Counters may lag pending reservations or distributed updates. Capacity monitoring records interface, privilege, mount, freshness, and whether reclaimable or thin-provisioned space is included.

### Lazy initialization

Formatting a large filesystem can avoid eagerly zeroing every bitmap or inode table when metadata flags make the initial state derivable. Background work initializes structures before ordinary use requires them.

Derived free state must still exclude fixed metadata. Checksums, feature flags, and group descriptors distinguish genuinely initialized data from reconstructible state.

### Checksums

Checksums on bitmaps and descriptors detect selected corruption and misdirected writes. They do not tell which of two conflicting ownership records is semantically correct.

Validation also checks counts, reserved ranges, group bounds, mappings, reverse maps, reference counts, and journal state. Repair needs independent evidence.

### Online growth and shrink

Growing adds devices, groups, bitmaps, descriptors, and capacity under a feature-compatible transition. New space becomes allocatable only after its ownership metadata is durable and discoverable.

Shrinking relocates all owners out of the removed range, blocks new allocations there, drains references, updates indexes, and changes geometry. Free count alone does not prove a tail is removable.

### Multiple devices

Striping, mirroring, parity, tiers, and failure domains turn one logical allocation into multiple physical placements. Eligibility includes device health, profile, redundancy, stripe geometry, and repair reserves.

Logical free space can be unusable for a requested profile when devices are imbalanced. Reports expose profile-specific constraints instead of one misleading total.

### Thin provisioning

A thin logical device can advertise address space not currently backed by physical capacity. The filesystem's free map and the pool's physical free map are independent layers.

Monitor and reserve both. Exhaustion below the filesystem can surface as I/O errors even while `statfs` reports free blocks.

### Discard and trim

After durable filesystem release, discard can tell a supporting lower layer that a logical range no longer contains live data. Online discard issues hints during operation; batch trim scans free ranges later.

Discard does not create filesystem free space and does not guarantee physical erasure, timing, or performance. Never issue it for blocks retained by snapshots or recovery.

### Secure deletion

Modern storage remaps, caches, snapshots, compression, and wear leveling make overwrite-based deletion unreliable. Discard is also not a universal sanitization primitive.

Security designs use encryption-key destruction, device sanitization commands, controlled lifecycle, or documented media guarantees. Free-space management only establishes filesystem nonownership.

### Zoned storage

Sequential-write zones constrain placement and reset. A zone may have unused capacity that cannot accept an arbitrary overwrite without relocation or garbage collection.

The allocator tracks write pointers, open-zone limits, live data, and reset eligibility. “Free bytes” must be interpreted through zone state.

### Concurrency

Region locks, tree locks, atomic counters, per-CPU caches, and reservations permit parallel allocation. A candidate found optimistically is revalidated under the authoritative update lock.

Lock order spans inode maps, free indexes, groups, quotas, reference counts, journals, and devices. Retries release provisional resources without double credit.

### Per-CPU and local caches

Small free ranges or reservations can be cached near CPUs or workloads to reduce global contention. Cached capacity remains globally accounted and is drained for balancing, unmount, resize, and recovery boundaries.

Hoarding can cause apparent exhaustion elsewhere. Limits and reclamation allow global demand to reclaim idle local stock.

### Near-full behavior

Search cost, tree splits, copy-on-write amplification, and fragmentation worsen near full capacity. Reserve thresholds and earlier failure preserve metadata and recovery progress.

Test at many fullness levels with concurrent workloads. A filesystem that works at 50 percent utilization has not established safe behavior at 99 percent.

### Scrubbing and reconciliation

Offline or online scrub compares file and metadata mappings, free indexes, bitmaps, reverse maps, reference counts, reservations, quotas, and bad-block records.

Bidirectional checks find both claimed-as-free cross-links and owned-but-unreachable leaks. Online scrub coordinates with cached and mutating state before drawing conclusions.

### Conservative repair

When ownership is uncertain, quarantine prevents reuse while evidence is gathered. Rebuilding free space from trusted owner mappings is safer than declaring unrecognized units free.

Repair records provenance, discarded records, recovered owners, data loss, and residual ambiguity. It reserves workspace without depending circularly on the structure being rebuilt.

### Observability and experiments

Record request length and alignment, chosen region and policy, search iterations, free-run histograms, counters, reservations, quotas, cache transfers, transaction credits, latency, failure reason, discard, crash point, and recovery reconciliation.

Preserve filesystem geometry, feature flags, mount options, device topology, fullness, workload seed, raw traces, and tool versions. Separate semantic validation from benchmark conclusions.

### Security and assurance

Adversarial tests target integer overflow, padding bits, stale summaries, duplicate frees, reservation cancellation races, quota bypass, emergency-reserve abuse, snapshot references, malformed trees, checksum mismatch, thin-pool exhaustion, discard misuse, and crashes.

Assurance names filesystem-format, allocator, concurrency, storage, recovery, security, capacity, performance, and independent-verification reviewers. Matching one free counter is not certification.

## Definitions and Notation

Let allocatable universe `U={0,...,N-1}` be partitioned at time `t` into free `F_t`, reserved `R_t`, and owned `A_t`. Thus `U=F_t disjoint_union R_t disjoint_union A_t`, after excluding permanently unavailable units from `U`.

For each unit `u`, ownership function `O_t(u)` returns `free`, `reserved(r)`, or `owned(x)`. Let `B_t` be a bitmap view, `E_t` a free-extent index, `C_t` summary counters, and `Q_t(d)` quota or reservation charge for domain `d`.

For request `(k,a,g,p)`, `k` is length, `a` alignment, `g` preferred region, and `p` policy. A candidate interval `[s,s+k)` is eligible only if it lies in `U`, every unit is free, `s mod a=0`, boundaries and profile hold, and required metadata credit is reserved.

Capacity conservation is `|F_t|+|R_t|+|A_t|=|U|`. This numeric equality is necessary but not sufficient: pairwise disjointness and agreement with all forward and reverse owner maps are also required.

## Mechanisms, Invariants, or Proof Structure

1. **Define the universe.** Establish geometry, units, reserved metadata, bad ranges, devices, profiles, zones, and feature-dependent exclusions.
2. **Validate the request.** Check length, alignment, overflow, quota domain, allocation class, locality hint, and worst-case metadata needs.
3. **Reserve capacity.** Atomically charge data, metadata, quota, journal, and copy-on-write obligations before admitting deferred work.
4. **Search boundedly.** Use summaries, regions, trees, bitmaps, caches, and fallback rules that terminate under fragmentation and contention.
5. **Revalidate authority.** Under the update lock, prove every candidate unit is free and eligible; summaries never authorize alone.
6. **Initialize and transfer.** Prevent stale exposure, update owner and free-space structures, and publish one recoverable transition.
7. **Release safely.** Remove all live mappings and references before changing ownership to free; coalesce and credit exactly once.
8. **Synchronize views.** Maintain or rebuild bitmaps, trees, buddy summaries, counters, reservations, quotas, reverse maps, and checksums.
9. **Persist atomically.** Journal changes or publish copy-on-write roots with sufficient credits, flush semantics, and late-error propagation.
10. **Recover idempotently.** Complete or unwind allocation and deferred-free intents and prove ownership in both directions.
11. **Report honestly.** Distinguish total, available, reserved, reclaimable, fragmented, profile-eligible, logical, and physical capacity.
12. **Preserve evidence.** Retain geometry, policy, request, search, ownership, transaction, crash, repair, and limitation records.

<!-- bijux-verify: {"id":"bitmap-contiguous-allocation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before=1110001110000000 free=10 largest=7\nallocated-start=9 length=4\nafter=1110001111111000 free=6 largest=3\nrequest-length=4 result=none\n","stderr":""}} -->
```python
used = [True, True, True, False, False, False, True, True, True] + [False] * 7


def largest_free(bits: list[bool]) -> int:
    best = run = 0
    for occupied in bits:
        run = 0 if occupied else run + 1
        best = max(best, run)
    return best


def allocate(bits: list[bool], length: int) -> int | None:
    run = 0
    for index, occupied in enumerate(bits):
        run = 0 if occupied else run + 1
        if run == length:
            start = index - length + 1
            bits[start:index + 1] = [True] * length
            return start
    return None


print(f'before={"".join("1" if b else "0" for b in used)} free={used.count(False)} largest={largest_free(used)}')
start = allocate(used, 4)
print(f"allocated-start={start} length=4")
print(f'after={"".join("1" if b else "0" for b in used)} free={used.count(False)} largest={largest_free(used)}')
print(f"request-length=4 result={allocate(used, 4) or 'none'}")
```

The executable model demonstrates a first-fit bitmap scan and the difference between total free units and largest contiguous run. It omits reservations, alignment, metadata, concurrency, persistence, quotas, devices, and real filesystem behavior.

## Alternatives and Trade-Offs

- Bitmaps are compact and exact but can require long scans; extent trees accelerate range queries but consume and mutate metadata nodes.
- Free lists simplify single-unit allocation but make contiguity and corruption detection weak.
- Buddy summaries find aligned power-of-two runs quickly but can waste space or require a finer authoritative bitmap.
- Address-ordered trees coalesce efficiently; length-ordered trees find fit efficiently; maintaining both increases transactional work.
- Small regions improve locality and lock granularity but can strand capacity; large regions broaden choice but increase contention and scan cost.
- First fit is simple, best fit preserves large leftovers sometimes, and goal-directed allocation improves locality; each produces different fragmentation.
- Strong reservations make delayed writes predictable but lower utilization; overcommit improves utilization but moves failure later.
- Large metadata and emergency reserves preserve forward progress but reduce user-visible capacity.
- Eager discard keeps lower layers informed but adds latency and fragmentation; batch trim amortizes work but delays notification.
- Checksummed redundant summaries improve detection and recovery but cost space and update bandwidth.
- Per-CPU caches reduce contention but can hoard capacity and complicate exact reports.
- Online repair preserves service but must synchronize with mutation; offline repair gets a stable view but requires downtime.

## Failure Modes and Misconceptions

- **“Free means no file currently names it.”** Metadata, journals, snapshots, and recovery work can own space too.
- **“The counter is the allocator.”** Counters summarize capacity; candidate units still require authoritative validation.
- **“Enough free blocks means a contiguous request succeeds.”** Alignment, fragmentation, region, and profile constraints can prevent it.
- **“Reserved and allocated are the same.”** A reservation promises capacity; final placement can remain undecided.
- **“Canceling twice is harmless.”** Double credit creates false capacity and eventual double allocation.
- **“Freeing before unlinking the map saves time.”** It creates an interval where two owners can use the same block.
- **“Discard frees filesystem blocks.”** Filesystem release comes first; discard is a lower-layer hint.
- **“Discard securely erases data.”** Media remapping and device semantics make that claim invalid without a sanitization contract.
- **“Snapshots do not affect free space until copied.”** Shared references keep physical units owned.
- **“Root reserves are ordinary free space.”** Availability depends on caller and recovery policy.
- **“Logical thin space guarantees physical capacity.”** The lower pool can exhaust independently.
- **“A checksum identifies the correct owner.”** It detects selected corruption but not semantic conflict.
- **“Rebuilding the bitmap alone repairs allocation.”** File maps, metadata maps, reverse maps, counts, and reservations must reconcile.
- **“One midpoint benchmark characterizes the allocator.”** Near-full, fragmented, concurrent, and device-specific regimes differ sharply.

## Worked Examples

### Example 1

A bitmap byte covers eight blocks; the final group has only five valid blocks. Padding bits remain ineligible so scanning cannot allocate beyond device end.

### Example 2

A region reports 1,000 free blocks but its largest run is eight. A 64-block contiguous request skips it using the summary and validates a candidate in another region.

### Example 3

Delayed writes reserve 128 data blocks plus extent-tree and journal credit. Cancellation releases every charge once even though no physical data blocks were selected.

### Example 4

A best-fit allocator consumes a 17-block run for a 16-block request and leaves a one-block fragment. A size-class policy might choose a 32-block run to preserve useful distributions.

### Example 5

Snapshot deletion removes the last shared reference to an extent. A deferred-free intent preserves ownership until reference, reverse-map, free-tree, quota, and journal changes finish.

### Example 6

An unprivileged caller sees 5 GiB available while total free is 6 GiB because 1 GiB is reserved for metadata, recovery, and privileged operations.

### Example 7

A mirrored allocation needs equal eligible extents on two healthy devices. Ten free gigabytes on one device cannot satisfy the profile when its partner has no space.

### Example 8

`statfs` reports free blocks inside a thin logical device, but the backing pool reaches zero. Monitoring both layers predicts the I/O failure that filesystem counters alone cannot.

### Example 9

Batch trim enumerates ranges already free and durable, then sends discard hints. A crash or unsupported device may leave physical reclamation incomplete without changing filesystem ownership.

### Example 10

Scrub finds block 900 marked free but referenced by an inode extent. It quarantines the block and investigates journal and reverse-map evidence rather than reallocating it or trusting the bitmap blindly.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) connects bitmaps, free lists, buddy systems, interval trees, B-trees, summaries, and checksums. [Data Engineering](../../19-data-engineering/ROADMAP.md) connects partitioning, compaction, capacity planning, skew, and storage accounting.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames stale-data exposure, quota abuse, sanitization, corruption, and repair authority. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity margins, cross-layer requirements, failure analysis, and assurance.

Within this program, [OS-043](043-file-allocation.md) supplies owner mappings; [OS-046](../ROADMAP.md), [OS-047](../ROADMAP.md), and [OS-050](../ROADMAP.md) connect free-space transactions to journaling, recovery, and complete filesystem design.

## References

- Linux kernel documentation, [ext4 Block Groups](https://docs.kernel.org/filesystems/ext4/blockgroup.html), current page checked 2026-09-04. Group layout, flexible and meta block groups, bitmap and inode-table placement, redundant metadata, and lazy initialization.
- Linux kernel documentation, [ext4 Block and inode Bitmaps](https://docs.kernel.org/filesystems/ext4/bitmaps.html), current page checked 2026-09-04. Per-unit bitmap representation, group-size relationship, uninitialized state, and fixed metadata exclusions.
- Linux kernel documentation, [ext4 Block Group Descriptors](https://docs.kernel.org/filesystems/ext4/group_descr.html), current page checked 2026-09-04. Bitmap locations, free counters, flags, descriptor sizes, and bitmap and descriptor checksums.
- Linux kernel documentation, [ext4 Block and Inode Allocation Policy](https://docs.kernel.org/filesystems/ext4/allocators.html), current page checked 2026-09-04. Multiblock allocation, delayed allocation, locality, block-group selection, speculative allocation, and fragmentation.
- Linux kernel documentation, [ext4 Bigalloc](https://docs.kernel.org/filesystems/ext4/bigalloc.html), current page checked 2026-09-04. Cluster allocation, bitmap meaning, large-file trade-offs, and compatibility constraints.
- Linux kernel documentation, [XFS Online Fsck Design](https://docs.kernel.org/filesystems/xfs/xfs-online-fsck-design.html), current page checked 2026-09-04. Free-space indexes, reverse mappings, reference counts, reservations, deferred work, and conservative online repair.
- Linux man-pages project, [statvfs(3)](https://man7.org/linux/man-pages/man3/statvfs.3.html), current page checked 2026-09-04. Filesystem block totals, free blocks, unprivileged availability, inode counts, sizes, and flags.
- util-linux project, [fstrim(8)](https://man7.org/linux/man-pages/man8/fstrim.8.html), current page checked 2026-09-04. Batch discard of unused filesystem ranges, minimum extent, device behavior, repetition, and safety considerations.
- Linux man-pages project, [mount(2)](https://man7.org/linux/man-pages/man2/mount.2.html), current page checked 2026-09-04. Filesystem mount flags and the distinction between VFS and filesystem-specific options.
- Linux kernel documentation, [iomap Library Design](https://docs.kernel.org/filesystems/iomap/design.html), current page checked 2026-09-04. Hole, delayed, mapped, unwritten, shared, and dirty mapping states and allocation obligations.

## Exercises

### Exercise 1

Compare bitmap, free-list, extent-tree, and buddy approaches for exactness, range search, fragmentation, concurrency, persistence, and repair.

### Exercise 2

Design allocation and release transactions that coordinate owner maps, free indexes, counters, reservations, quotas, metadata credit, initialization, and crashes.

### Exercise 3

Specify a near-full policy for delayed allocation, copy-on-write, metadata growth, emergency reserves, fairness, and honest error reporting.

### Exercise 4

Design discard, thin-provisioning, multi-device, and zoned-storage integration without overstating free or sanitized capacity.

### Exercise 5

Build a scrub, repair, test, and performance plan for free-space management. Include corruption, concurrency, resize, crashes, evidence, and reviewers.

## Answers to the Exercises

### Answer 1

A bitmap gives compact exact per-unit state and constant known-unit tests, but long-run discovery can scan heavily near full. A free list makes single-unit removal simple but has weak range search and corruption containment. An address-ordered extent tree supports adjacency and coalescing; a length index accelerates fit, but tree nodes consume space and duplicate indexes need transactional agreement. A buddy summary finds aligned power-of-two runs quickly but can round requests and is often derived over finer state.

Compare bytes per unit, search bounds, aligned-run behavior, split and merge cost, lock granularity, persistent update amplification, reconstruction source, and corruption cases. A hybrid can keep a persistent bitmap as authority with in-memory buddy and counter summaries. Whichever design is chosen, summaries prune candidates but authoritative state validates the final range.

### Answer 2

Validate checked length, alignment, profile, region, quota, and worst-case data and metadata needs. Atomically reserve capacity and transaction credit, search bounded indexes, lock the candidate region, then revalidate every unit against authoritative free state. Initialize or mark storage unwritten, update owner map, free map, reverse map, counters, quota, checksum, and journal or copy-on-write state, and publish at one recoverable point. Failure releases each provisional claim once.

Release first removes the last live owner and cache or I/O reference under the lifecycle protocol, transfers work to a durable deferred-free intent if needed, then updates reference counts, reverse maps, owner maps, free indexes, counters, and quota. Only afterward is the range reusable and eligible for discard. Recovery completes or cancels intents idempotently and checks that every mapped unit is owned and every free unit lacks an owner.

### Answer 3

Reserve separate data, mapping-tree, free-tree, reference-count, quota, and journal capacity before accepting deferred dirty work. Keep an emergency pool for narrowly defined recovery and administrative operations, with per-domain limits and audit. Copy-on-write admission estimates private data and split metadata; snapshot-heavy workloads expose shared and exclusive pressure separately. Throttle before terminal fullness to preserve writeback and reclaim progress.

Use fair queues or bounded local caches so one tenant cannot hoard all reservations. Reclaim canceled reservations, unused preallocation, deletable snapshots under policy, and idle caches before broad failure, but never count merely possible reclamation as guaranteed. Return quota, profile, metadata, fragmentation, thin-pool, or global exhaustion distinctly and propagate delayed errors through synchronization and status channels.

### Answer 4

Filesystem ownership changes first and becomes recoverably durable. Batch trim or online discard then sends aligned hints only for ranges with no snapshot, journal, bad-block, or recovery owner; failure or unsupported discard leaves filesystem free state unchanged. Do not claim secure erasure without a device sanitization or cryptographic lifecycle contract.

Track thin-pool physical capacity separately from filesystem logical free space and reserve headroom for metadata and copy-on-write at both layers. For multi-device profiles, report capacity satisfiable under redundancy and health constraints, not the sum of bytes. For zoned devices, account write pointer, open-zone limits, live ranges, relocation, and reset eligibility. Cross-layer monitoring correlates filesystem requests with pool, device, and zone failures.

### Answer 5

Generate empty, full, nearly full, fragmented, aligned, multigroup, multidevice, quota-limited, snapshot-heavy, thin, and zoned states. Race allocation, release, reservation cancel, truncate, clone, snapshot deletion, writeback, trim, resize, scrub, and repair. Inject duplicate frees, bitmap and counter mismatch, invalid padding bits, overlapping extents, lost reservations, checksum failures, device errors, and crashes at every owner/free transaction boundary.

Scrub compares forward mappings, metadata ownership, free maps, reverse maps, reference counts, reservations, quotas, descriptors, checksums, and journal intent in both directions. Quarantine ambiguity and rebuild only from a justified authority. Measure search iterations, allocation latency, free-run distributions, contention, cache hoarding, amplification, discard cost, and failure thresholds across fullness. Preserve geometry, features, topology, seeds, traces, disk images, raw outputs, repair decisions, and limitations. Named allocator, format, concurrency, storage, recovery, security, capacity, performance, and independent-verification reviewers assess the evidence.
