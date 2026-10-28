---
module_id: OS-037
program: Operating Systems
level: 1
module_number: 37
title: Copy-on-Write
status: complete
last_verified: 2026-09-04
---

# Copy-on-Write

## One-Page Review

### Governing question

How can an operating system let independent address spaces temporarily share physical content, then preserve private-memory semantics when either side writes, without leaks, stale permissions, duplicate publication, or unbounded fault cost?

### Essential definitions

- **Copy-on-write (COW)** defers copying shared content until an operation requires a private writable version.
- A **COW mapping** is a logically private mapping whose current physical content may be shared and write-protected.
- A **COW fault** is a write-permission fault that policy resolves by copying or exclusively promoting the page.
- **Exclusive promotion** makes an already unique COW page writable without copying it.
- A **map count** tracks page-table mappings; a **reference count** covers a broader set of object references.
- A **pin** stabilizes memory for an external or kernel user and can restrict copying, migration, or reclamation.
- **Break COW** means establishing the faulting mapping's private writable version.

### Central model, mechanism, or theorem

Each logical mapping `m` refers to version `v` with access state `A(m)`. A fork-like operation adds read-only COW mappings to the same immutable version. On write, resolution validates `(m,v,g)`: if the version is provably exclusive and otherwise eligible, it may promote; otherwise it allocates `v'`, copies stable content, atomically redirects `m` to `v'`, updates references, invalidates stale translations, and retries.

The abstraction is observational: before either party writes, both read the pre-share bytes; after one writes, that party reads its new bytes while the other continues to read the old bytes. Physical sharing, allocation timing, and fault counts are implementation details unless an interface exposes them.

### Critical invariants

- A private write never becomes visible through another logically private mapping.
- No writable alias to shared COW content exists unless sharing semantics explicitly permit it.
- The source remains stable during copying, or concurrent modification is serialized or detected.
- Exactly one winning version is published for each resolved mapping transition; losers release candidates.
- Map counts, references, pins, reverse mappings, page tables, and accounting agree after every outcome.
- Allocation failure, unmap, exec, exit, truncation, huge-page change, and concurrent faults leave a valid old mapping or a defined error.
- Writable publication and required TLB or device invalidation occur in architecture-correct order.

### Common failures

Common mistakes are marking only the child's mapping read-only, confusing every read-only fault with COW, using reference count alone to prove exclusivity, copying from a source that can change, losing dirty state, double-copying concurrent faults without loser cleanup, mishandling zero pages or huge pages, allowing DMA pins to bypass isolation, and measuring fork speed without charging later write amplification.

### Compact example

A parent and child share frame `F0` read-only after `fork`. The parent writes. Its handler verifies private COW policy, allocates `F1`, copies stable `F0`, publishes the parent's writable mapping to `F1`, decrements the old reference, invalidates the parent's stale read-only translation, and retries. The child still reads `F0`. If the child later becomes the only mapper of `F0`, policy may promote it writable without another copy after proving exclusivity.

### Connections

[OS-031](031-address-translation.md) through [OS-036](036-virtual-memory-page-replacement.md) supply mapping, faults, and physical-memory policy. [OS-038](../ROADMAP.md), [OS-039](../ROADMAP.md), and [OS-040](../ROADMAP.md) extend mapped files, page cache, and swap.

## Governing Question

Eagerly copying an address space preserves private semantics but wastes time and memory when the child soon calls `exec`, exits, or touches few pages. COW changes the cost schedule: share now, pay on the first private write.

That optimization transfers work into a concurrent fault path. Correctness depends on mapping policy, source stability, allocation, accounting, publication, and invalidation. The governing question is how to defer work while keeping the eager-copy observable contract.

## Why This Matters

COW makes process creation practical, implements private file mappings, supports zero-page sharing and same-page merging, and appears in snapshots, virtual machines, and language runtimes. The shared phrase hides different ownership and durability contracts in each domain.

Fault-time copies can create latency spikes and memory amplification precisely when the system is under pressure. Huge pages increase the copy unit; multi-threaded writers create contention; device pins and external page tables add consumers that ordinary process mappings do not capture.

COW bugs are severe. A missed write-protection transition can violate isolation, while reference and cleanup mistakes cause leaks, use-after-free, or corrupted data. Security reviews therefore treat COW as a state machine, not merely an optimization slogan.

## Prerequisites and Retrieval

Review [OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-033](033-translation-lookaside-buffers.md), [OS-034](034-demand-paging.md), [OS-035](035-page-faults.md), and [OS-036](036-virtual-memory-page-replacement.md).

Retrieve these distinctions:

- logical privacy differs from current physical exclusivity;
- mapping permissions, virtual-memory-area policy, and backing-object permissions are separate;
- map count and reference count describe different ownership facts;
- read-only can mean immutable policy, COW, dirty tracking, deduplication, or userfault write protection;
- an atomic PTE change does not alone stabilize the source page, VMA, or reverse mapping;
- CPU TLBs and device page tables can cache permissions independently;
- fork-time savings can become later copy, allocation, compaction, and fault cost;
- a base page, transparent huge page, and multi-page folio are different accounting units.

## Learning Objectives

After this module, you should be able to:

1. derive COW's observational contract from eager private copying;
2. trace fork setup and write-fault resolution through locks, references, allocation, copying, publication, and invalidation;
3. distinguish copy, exclusive promotion, zero-page allocation, genuine protection failure, and delegated write tracking;
4. reason about concurrent faults, unmap, exit, pins, DMA, huge pages, deduplication, and replacement;
5. diagnose lost isolation, stale writable aliases, leaks, double copies, dirty-state loss, and fault storms;
6. quantify deferred cost, copy amplification, memory savings, latency, and pressure;
7. construct tests and assurance evidence for COW lifecycle correctness.

## Core Exposition

### The observational contract

Suppose eager fork would give parent and child independent byte-for-byte copies at the fork point. COW is correct if every permitted sequence of reads and writes produces the same process-visible bytes, aside from documented timing, resource, and diagnostic differences.

This is more precise than “share until write.” Signals, allocation failure, mapped-file behavior, pins, and external observers may expose differences, so the interface contract must state which observations matter.

### Fork setup

A fork-like operation duplicates address-space metadata and page-table structure as required, but maps eligible private pages to shared physical content. Writable private entries in both parent and child become read-only COW entries before either can write through an old translation.

The kernel increments the proper page, anonymous-memory, and mapping references. Failure halfway through must unwind child state and preserve the parent's valid mappings and permissions.

### Parent-side write protection

Protecting only the new child is incorrect: the parent could retain a writable TLB entry and modify shared data without faulting. Setup must revoke or replace writable translations for every private participant covered by the share.

Page-table update, architecture invalidation, and visibility ordering form one transition. Other CPUs running the parent and secondary device mappings must be included under their respective protocols.

### Fault classification

A write fault on a read-only entry is not automatically COW. The handler combines raw fault evidence with current VMA access, mapping type, PTE state, backing identity, write-protect reason, generation, and execution context.

Private COW may copy or promote. Genuine read-only policy fails. Dirty tracking may only update metadata. Userfault write protection may delegate. A stale or migration entry follows its own protocol.

### Source stability

Copying must observe a coherent source version. Page, folio, anonymous-memory, mapping, or other locks and references stabilize content according to the implementation. A writable alias, DMA writer, migration, or truncation can invalidate a naive snapshot.

If stability cannot be held through allocation, acquire a durable reference, allocate outside constrained locks, then reacquire and revalidate identity and generation before copying or publication.

### Allocation and zeroing

The destination must have the correct size, node or tier policy, cgroup charge, encryption domain, and initialization. A general copy overwrites every byte, but failure paths must never expose stale allocator content.

Allocation can trigger reclaim, compaction, or OOM policy. The old read-only mapping remains valid until a replacement is ready; failure must not partially redirect the mapping.

### Copying data

The copy unit may be a base page, folio, or huge page. Architecture-specific routines handle cache coherence, tags, and metadata. The handler does not infer that a successful byte copy also transferred dirty, access, ownership, or security metadata.

Copy cost consumes memory bandwidth and pollutes caches. Large COW bursts can compete with the workload whose progress triggered them.

### Atomic publication

Before publication, the handler reacquires the required VMA and page-table stability and verifies the mapping still refers to expected source version `v` under generation `g`. It then compare-publishes the destination as private and writable.

If another fault already won, the candidate is discarded and current state is used. A losing allocation must not decrement the winner's source reference or leak its destination.

### Reference and map counts

A page's reference count can include page cache, pins, transient kernel users, migration, swap cache, or compound-page relationships beyond PTE mappings. Map count tracks a narrower surface.

Neither number alone universally proves that in-place promotion is safe. The proof uses implementation-specific ownership, pin, mapping, and version state under the required locks.

### Exclusive promotion

If the faulting mapping is the sole relevant owner of a COW version and no constraint requires a distinct copy, the handler may make it writable in place. This avoids allocation and data movement.

Exclusivity is a transient predicate. It must be established at publication time, not inferred from an earlier unlocked count. KSM, swap, pins, device access, and huge-page state can forbid the shortcut.

### Shared zero pages

Many untouched anonymous reads can map one immutable zero page. A write cannot modify that page; it allocates a private zeroed destination and installs it writable.

This path need not physically copy known zeros, but it remains a COW-like logical transition. The zero page is never promoted writable merely because one process happens to reference it.

### Private file mappings

`MAP_PRIVATE` creates a private COW view of file-backed data. Reads can use page-cache content, while a private write creates anonymous or otherwise private modified state rather than updating the underlying file through that mapping.

Truncation, invalidation, partial final pages, and I/O errors complicate fault classification. File identity and offset must be revalidated after waits.

### Shared mappings are different

A shared writable mapping is intended to propagate modifications according to its contract; breaking it into private COW pages would violate semantics. COW applies only where logical privacy or snapshot versioning demands separation.

The same physical frame can participate in both shared and private relationships under controlled rules. Mapping type, not physical sharing alone, determines write behavior.

### Dirty and accessed state

After a COW write fault, the new mapping's accessed and dirty state must reflect the resolved operation under architecture and OS rules. The old page's historical dirty state remains associated with its own backing and lifecycle.

Losing dirty information can discard data; transferring it indiscriminately can trigger wrong writeback. Treat content and metadata as separate obligations.

### TLB and device invalidation

Fork setup removes write permission; fault resolution grants it to one mapping. Cached CPU translations must not retain obsolete rights. Architecture rules determine invalidation scope, ordering, batching, and remote synchronization.

Devices using mirrored page tables or pinned buffers may require MMU-notifier or driver coordination. CPU page-table correctness alone cannot revoke a DMA engine's access.

### Concurrent writes

Two threads in one address space can fault on the same COW PTE. Both may allocate and copy optimistically, but only one publishes against the expected old entry. The loser observes the installed writable mapping and releases its candidate.

Parent and child can fault concurrently on their separate PTEs. Each must preserve the shared source until its transition completes; one side becoming exclusive can change the other's legal optimization.

### Unmap, exit, and exec races

A process can unmap the address, exit, or replace its address space while a fault waits for memory. VMA references and generations prevent use-after-free, but the handler must still reject stale publication.

Cleanup decrements each installed or transient reference exactly once. A candidate prepared for a vanished mapping is released without resurrecting the mapping.

### Pins and direct memory access

Long-lived pins can allow a device or kernel subsystem to access content outside ordinary PTE faults. A future process fork does not automatically turn an external writable DMA path into COW-aware access.

Pin APIs, write intent, MMU notifiers, and filesystem rules define legal combinations. Linux distinguishes pinning APIs and documents special tracking because ordinary references are insufficient for these interactions.

### Huge pages and splitting

A write to one byte of a shared huge page presents a choice: copy the whole huge unit, split it and copy a smaller page, or use another supported mechanism. Whole copies preserve large mappings but amplify work; splitting adds latency, fragmentation, and metadata transitions.

Splitting can fail when pages are pinned. Concurrent collapse, split, migration, and faults require higher-level and leaf page-table stabilization.

### Same-page merging

Deduplication can discover identical anonymous pages and replace them with one write-protected shared version. A later writer breaks sharing through COW. Unlike fork, sharing was created by content identity rather than ancestry.

Hash or byte comparison must not merge mutable content without stabilization. Security and side-channel policy may restrict cross-domain deduplication even when bytes match.

### Swap and page replacement

Shared anonymous content may be selected for swap or reclamation. Swap entries, reverse mappings, COW status, and reference counts must preserve which logical mappings still share a version after swap-in.

Replacement can break or reconstruct sharing according to policy, but no process may observe another's later private writes. Fault metrics distinguish COW allocation from swap-in and combined paths.

### Memory accounting

At fork, virtual commitments can increase while physical resident bytes remain shared. Later writes allocate private pages and may charge a cgroup or process at fault time. Report shared, proportional, private, resident, and committed measures with their definitions.

Peak write amplification matters for capacity planning. A fork-heavy workload that looks cheap at creation can rapidly approach an eager-copy footprint.

### Error and overload behavior

COW fault allocation may fail because of cgroup limits, physical pressure, compaction failure, or exhausted backing policy. The kernel applies its defined allocation, OOM, signal, or termination behavior without corrupting the old version.

Repeated faults on an unchanged entry signal lost publication or invalidation. Bound retries and record the PTE identity, generation, allocation, wait, and terminal outcome.

### User-space write protection

Linux `userfaultfd` write-protect mode can notify user space of writes to registered pages. It supports dirty tracking and migration workflows, but its unprotect operation is not automatically a private COW copy.

The manager must distinguish missing, minor, and write-protect events, follow negotiated feature support, track unmap and remap events, and provide a liveness policy if the handler stops responding.

### Testing and observability

Test parent and child reads, writes from each side, concurrent same-PTE and different-PTE faults, zero pages, private files, genuine protection, unmap, exit, exec, allocation failure, pins, device mappings, huge pages, KSM, swap, and pressure.

Measure fork time, page-table memory, shared and private bytes, COW faults, copies, promotions, bytes copied, loser allocations, fault latency, allocation and compaction time, invalidation, refault, swap, OOM, and cleanup balance.

### Security and assurance

COW's core security property is noninterference between logically private mappings after either writes. Zero destination memory as required, preserve tags and permissions, constrain diagnostics, and prevent stale writable translations.

Adversaries can force high-rate faults, race mappings, exploit integer and count boundaries, pin pages, or amplify huge-page copies. Assurance combines invariants, fault injection, race detection, architecture testing, resource bounds, and independent review.

## Definitions and Notation

Let logical mappings be `m in M`, physical or backing versions be `v in V`, mapping relation be `P_t(m)=v`, access state be `A_t(m)`, reference state be `Q_t(v)`, and mapping generation be `g_t(m)`. Content of a version is `B_t(v)`.

For mappings `p` and `c` immediately after a fork-like share at time `f`, `P_f(p)=P_f(c)=v`, both are write-protected COW, and reads return `B_f(v)`. After parent write of bytes `x`, there exists private `v'` such that `P(p)=v'`, `B(v')` includes `x`, and `P(c)=v` with unchanged `B(v)`.

Fault resolution `R(m,v,g)` returns `copy`, `promote`, `delegate`, `deny`, `retry`, or `fail`. `copy` and `promote` require the current mapping to match `(v,g)` at publication.

## Mechanisms, Invariants, or Proof Structure

A reviewable COW mechanism follows twelve obligations:

1. Define the eager-copy observable contract and which mappings are eligible for sharing.
2. Stabilize setup so all private participants lose writable access before sharing becomes visible.
3. Record COW reason, backing identity, references, ownership, page size, and generation.
4. Classify write faults against current policy rather than treating all read-only entries alike.
5. Stabilize source content and allocate a correctly charged and initialized destination.
6. Revalidate VMA, PTE, version, permissions, pins, and generation after every wait.
7. Compare-publish exactly one destination or exclusive promotion and clean up losers.
8. Preserve dirty, accessed, reverse-map, swap, tag, and accounting semantics.
9. Order writable publication with CPU and device translation invalidation.
10. Handle unmap, exit, exec, truncation, KSM, huge pages, pins, replacement, and failure.
11. Bound fault work, retries, copying, compaction, and external-handler delay.
12. Test noninterference and lifecycle balance while preserving raw evidence and limitations.

The executable state machine illustrates a fork, one copying write, and one later exclusive promotion.

<!-- bijux-verify: {"id":"cow-state-machine","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"after-fork parent=10 child=10 shared=True\nafter-parent-write parent=11 child=10 shared=False copies=1\nafter-child-write parent=11 child=12 frames=2 copies=1\nrefs=F0:1,F1:1\n","stderr":""}} -->
```python
frames = {0: {"value": 10, "refs": 1}}
mappings = {"parent": {"frame": 0, "cow": False, "writable": True}}
copies = 0

def fork(parent, child):
    frame = mappings[parent]["frame"]
    frames[frame]["refs"] += 1
    mappings[parent]["cow"] = True
    mappings[parent]["writable"] = False
    mappings[child] = {"frame": frame, "cow": True, "writable": False}

def write(process, value):
    global copies
    mapping = mappings[process]
    frame = mapping["frame"]
    if mapping["cow"] and frames[frame]["refs"] > 1:
        frames[frame]["refs"] -= 1
        new_frame = max(frames) + 1
        frames[new_frame] = {"value": frames[frame]["value"], "refs": 1}
        mapping["frame"] = new_frame
        copies += 1
    mapping["cow"] = False
    mapping["writable"] = True
    frames[mapping["frame"]]["value"] = value

def read(process):
    return frames[mappings[process]["frame"]]["value"]

fork("parent", "child")
print(f"after-fork parent={read('parent')} child={read('child')} shared={mappings['parent']['frame'] == mappings['child']['frame']}")
write("parent", 11)
print(f"after-parent-write parent={read('parent')} child={read('child')} shared={mappings['parent']['frame'] == mappings['child']['frame']} copies={copies}")
write("child", 12)
print(f"after-child-write parent={read('parent')} child={read('child')} frames={len(frames)} copies={copies}")
print("refs=" + ",".join(f"F{frame}:{state['refs']}" for frame, state in sorted(frames.items())))
```

The toy serializes all operations and treats reference count as sufficient for promotion. It omits page tables, TLBs, map counts, locks, pins, backing objects, huge pages, failures, and actual process isolation; production code cannot inherit those simplifications.

## Alternatives and Trade-Offs

- Eager copying gives predictable post-fork ownership but spends time and memory on untouched pages.
- COW reduces initial work but moves allocation and copying into write-fault latency.
- Exclusive promotion avoids a copy but requires a strong, current exclusivity proof.
- Whole huge-page copying preserves large mappings but can amplify a tiny write.
- Splitting enables fine-grained copies but adds metadata, fragmentation, and race complexity.
- Shared zero pages save memory but every first write requires allocation.
- Same-page merging increases sharing but adds scanning, comparison, break-COW work, and side-channel concerns.
- Coarse address-space locking simplifies races but serializes unrelated faults and mapping operations.
- Fine-grained VMA and PTE locking improves scalability but expands revalidation obligations.
- User-space write protection enables flexible tracking but adds permissions, protocol, and liveness dependencies.
- Long-lived pins simplify device access but obstruct COW, migration, writeback, and reclamation.
- Overcommit improves utilization but can defer capacity failure until a COW fault.

## Failure Modes and Misconceptions

1. **“COW makes copying free.”** it defers and sometimes avoids copies; later writes still cost.
2. **“Only the child needs write protection.”** the parent could otherwise modify shared content silently.
3. **“Every read-only write fault is COW.”** immutable, tracking, migration, and delegated states differ.
4. **“Reference count one proves exclusivity.”** pins, cache, compound pages, and transient references complicate it.
5. **“Atomic PTE replacement solves the race.”** source, VMA, reverse-map, and external mappings also need stability.
6. **“Two copies are merely inefficient.”** loser reference and publication mistakes can corrupt lifecycle state.
7. **“Copying bytes copies semantics.”** dirty state, tags, ownership, and accounting require separate treatment.
8. **“A private file write updates the file.”** private COW modification is not shared file writeback.
9. **“A shared mapping should break COW.”** private separation would violate its propagation contract.
10. **“Pins are ordinary references.”** writable DMA can bypass CPU fault mediation.
11. **“Huge-page COW is one base-page copy.”** copy or split policy changes the unit and cost.
12. **“Fork memory usage equals resident bytes.”** shared, private, committed, and proportional measures differ.
13. **“Fast fork proves COW is efficient.”** later fault latency and copy amplification complete the cost.
14. **“Passing fork tests proves isolation.”** concurrency, invalidation, pins, failure, and hostile races remain.

## Worked Examples

### Example 1

A parent forks and the child immediately executes a new program. COW pays page-table and metadata setup but avoids copying untouched user pages, demonstrating the intended common-case saving.

### Example 2

The parent retains a writable TLB entry after fork setup. It changes shared data without a fault, and the child observes the write. A synchronous permission revocation and invalidation protocol prevents this isolation failure.

### Example 3

Two parent threads fault on the same COW PTE. Both allocate and copy; one compare-publishes. The loser sees the changed PTE, frees its candidate, and retries the already writable mapping.

### Example 4

The child is the only remaining owner after the parent exits. Under the current page and mapping locks, the handler proves eligibility and promotes the old page writable without copying.

### Example 5

A read of untouched anonymous memory uses the shared zero page. The first store allocates a private zeroed page; the globally shared zero page can never be promoted writable.

### Example 6

A `MAP_PRIVATE` file page is read from the page cache, then modified. The new private version changes process-visible bytes but is not written back as a shared update to that file mapping.

### Example 7

A fault drops a lock to allocate while another thread unmaps the range. Revalidation rejects the candidate, releases it, and reports current mapping state instead of resurrecting the address.

### Example 8

An RDMA device holds a writable long-term pin across process creation. Ordinary PTE write protection cannot intercept device writes, so the pin and memory-sharing policy must prohibit or explicitly coordinate the combination.

### Example 9

A store touches one base-page region within a shared huge page. Whole-page copying causes large latency; splitting would be cheaper in bytes but fails because the page is pinned. The defined fallback preserves correctness.

### Example 10

A service's median fork time falls, but a traffic burst makes children dirty most pages. COW-fault p99, bytes copied, compaction, and cgroup OOM evidence reveal deferred memory amplification.

## Cross-Program Connections

[Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects fork, private mappings, faults, and native-memory APIs. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies reference counting, versioning, persistent structures, and concurrent publication.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies page permissions, atomic PTE updates, TLBs, caches, tags, and IOMMUs. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames noninterference, side channels, stale permissions, hostile races, and resource exhaustion.

Within this program, [OS-035](035-page-faults.md) classifies the trap and [OS-036](036-virtual-memory-page-replacement.md) governs physical pressure; [OS-038](../ROADMAP.md) through [OS-040](../ROADMAP.md) develop mapped files, shared cache, and swap interactions.

## References

- Linux man-pages project, [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html), current page checked 2026-09-04. Independent memory spaces, Linux COW implementation, page-table duplication cost, memory locks, and fork-specific mapping advice.
- Linux man-pages project, [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), current page checked 2026-09-04. `MAP_PRIVATE` copy-on-write mappings, shared mappings, file visibility, inheritance, and partial final pages.
- Linux kernel documentation, [Page Tables](https://docs.kernel.org/mm/page_tables.html), current page checked 2026-09-04. Permissions, dirty state, MMU walks, page faults, lazy allocation, COW, swap, and nonpageable kernel mappings.
- Linux kernel documentation, [Process Addresses](https://docs.kernel.org/mm/process_addrs.html), current page checked 2026-09-04. VMA, mmap, reverse-map, and page-table locking; atomicity; concurrent hardware updates; installation; invalidation; and lock ordering.
- Linux kernel documentation, [Memory Management APIs](https://docs.kernel.org/core-api/mm-api.html), current page checked 2026-09-04. COW mapping terminology, anonymous write behavior, fault callbacks, folio operations, and mapping APIs.
- Linux kernel documentation, [pin_user_pages() and related calls](https://docs.kernel.org/core-api/pin_user_pages.html), current page checked 2026-09-04. Pin versus ordinary reference semantics, writable memory access, long-term DMA, MMU notifiers, huge-page accounting, and tests.
- Linux kernel documentation, [Transparent Hugepage Support](https://docs.kernel.org/mm/transhuge.html), current page checked 2026-09-04. Huge mapping lifecycle, split fallback, page-table locking, pinned-page split failure, map counts, and copy cost.
- Linux kernel documentation, [Kernel Samepage Merging](https://docs.kernel.org/mm/ksm.html), current page checked 2026-09-04. Write-protected identical pages, stable and unstable trees, COW breaks, swapping, counters, and operational controls.
- Linux man-pages project, [userfaultfd(2)](https://man7.org/linux/man-pages/man2/userfaultfd.2.html), current page checked 2026-09-04. Missing, minor, and write-protect events, feature negotiation, write unprotection, range lifecycle, permissions, and handler liveness.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching treatment of address spaces, fork, page tables, reference ownership, faults, and deliberate simplifications.

## Exercises

### Exercise 1

Specify fork-time COW setup and unwind. Cover both address spaces, PTE permissions, reference ownership, invalidation, partial failure, and the observational contract.

### Exercise 2

Design a concurrent write-fault state machine with copy and exclusive-promotion paths. Include source stability, allocation, revalidation, loser cleanup, and errors.

### Exercise 3

Analyze COW interactions with private files, shared zero pages, KSM, swap, huge pages, and writable device pins. Define legal transitions for each.

### Exercise 4

Build a measurement plan comparing eager copy and COW for a fork-heavy service. Include workload phases, memory metrics, latency, amplification, pressure, and rollback.

### Exercise 5

Construct a security and assurance review for COW in a multi-core kernel. Cover isolation, stale translations, races, resource bounds, tests, evidence, and reviewers.

## Answers to the Exercises

### Answer 1

Freeze the relevant address-space changes, create child metadata, and walk eligible private mappings. For each mapping, acquire proper source and page-table references, mark both parent and child entries read-only with an explicit COW reason, update anonymous or backing ownership, and perform architecture-required invalidation before either participant can write through stale permission.

Track installed child entries and parent entries changed by the operation. On allocation or setup failure, remove every child mapping and reference exactly once and restore parent state only when doing so cannot create a writable shared alias. The postcondition is either a valid child whose reads match eager copying and whose writes separate, or no child with the parent's original observable state preserved.

### Answer 2

Snapshot the fault and stabilize the current private VMA, expected COW PTE, source version, page size, backing, and generation. Under implementation-specific ownership locks, test exclusive promotion; if it is not proved, retain a stable source reference, allocate and charge a destination, copy coherent content, and prepare metadata.

Reacquire the current PTE and compare it with the expected source and generation. The winner publishes a writable private entry, transfers dirty and access state correctly, updates reverse maps and references, invalidates stale CPU and relevant device translations, and retries. A loser releases its candidate and uses current state. Unmap, permission change, allocation failure, pin conflict, or backing error leaves the old mapping valid or returns the defined terminal outcome. Repeated unchanged faults are bounded.

### Answer 3

A private file mapping may share clean page-cache content, but its write creates private state and does not become shared file writeback. A global zero page always allocates on write and is never promoted. KSM shares by stable content identity, then breaks sharing on write while observing security-domain policy. Swap must preserve shared-version identity or safely reconstruct it after swap-in.

For a huge page, policy chooses supported whole copy, safe split and base-page copy, or defined fallback; pins can make split impossible. A writable device pin can bypass CPU PTE faults, so fork or COW setup must reject, pre-break, revoke through notifier coordination, or use a documented device-aware mechanism. None of these cases can infer legality from a raw reference count.

### Answer 4

Compare identical request and child lifecycles under eager and COW implementations or controlled models: immediate exec, read-mostly child, sparse writes, dense writes, parent and child concurrent writes, huge-page use, and memory pressure. Control CPU and NUMA placement, page sizes, allocator state, cgroup limits, swap, storage, process size, repetitions, and warmup.

Record fork duration, page-table bytes, shared and proportional resident bytes, private bytes, commitments, COW faults, copies, promotions, bytes copied, loser allocations, allocation and compaction time, fault p50 through p99.9, TLB invalidation, reclaim, swap, PSI, throughput, and OOM. Preserve raw timelines and configuration. Roll back if tail latency, pressure, error rate, or peak capacity crosses a declared service threshold, even when median fork time improves.

### Answer 5

State noninterference: after sharing, a private write by one mapping cannot alter bytes read through another. Prove complete write revocation at setup, correct classification, stable source, initialized destination, current-generation publication, exact reference balance, dirty and tag preservation, CPU and device invalidation, bounded retry, and valid failure state.

Inject parent and child writes on many CPUs, same-PTE races, unmap, exit, exec, permission change, allocation and compaction failure, huge-page collapse and split, KSM merge, swap, writable pins, delayed device invalidation, stale TLBs, counter boundaries, and fault storms. Preserve traces, page-table snapshots where safe, counters, latency, configurations, and limitations. Named kernel-memory, architecture, device, filesystem, security, performance, reliability, and independent-verification reviewers assess residual risk; unit and stress tests alone do not certify isolation.
