---
module_id: OS-031
program: Operating Systems
level: 1
module_number: 31
title: Address Translation
status: complete
last_verified: 2026-09-04
---

# Address Translation

## One-Page Review

### Governing question

How does a system translate process virtual addresses into protected physical locations while preserving isolation, controlled sharing, lifecycle, and performance under faults and concurrent mapping changes?

### Essential definitions

- A **virtual address** is the address generated in a process or execution context before final physical translation.
- A **physical address** identifies a location in the processor and memory-system physical address domain.
- A **page** is a fixed-size aligned virtual-memory unit; a **page frame** is an aligned physical-memory unit.
- A **virtual page number (VPN)** selects a virtual page and a **page offset** selects a byte within it.
- A **page-table entry (PTE)** describes a translation or another architecture-defined state plus permissions and attributes.
- A **memory-management unit (MMU)** applies translation and access checks for memory references.
- A **page fault** is a precise architectural exception for a translation, presence, permission, or related access condition.

### Central model, mechanism, or theorem

For page size `P=2^p`, virtual address `v` decomposes into `VPN=floor(v/P)` and `offset=v mod P`. A valid leaf mapping `T_a(VPN)=(PFN,perm,attr)` in address space `a` yields physical address `PFN*P+offset` only if the access type, privilege, and attributes pass all checks.

Translation is indexed by address-space identity as well as virtual address. The same `v` can name different frames in different processes, and several virtual pages can deliberately map one frame. A miss or denied access transfers control through an exception; software may establish a valid mapping, implement copy-on-write, deliver a process fault, or terminate the access.

### Critical invariants

- Every successful translated interval remains within the mapped page or explicitly crosses into separately validated pages.
- User access cannot reach supervisor-only or otherwise unauthorized mappings through any alias.
- Mapping publication, replacement, and removal are synchronized with page-table walkers, translation caches, and physical-frame lifetime.
- Permissions implement least access and distinguish read, write, execute, user, global, and architecture-specific attributes.
- Shared aliases preserve coherent ownership rules; private copy-on-write never modifies the original shared frame after separation.
- Fault handling validates cause, address, access type, privilege, and current mapping generation before recovery.
- Arithmetic, page size, address width, canonicality, and alignment assumptions are explicit and checked.

### Common failures

Common mistakes are confusing virtual and physical addresses, assuming one page size, using unaligned masks incorrectly, ignoring overflow at page boundaries, updating a PTE without invalidating stale translations, freeing a frame before all translations and walkers release it, granting write plus execute by convenience, treating every fault as an error, trusting user-controlled fault addresses, and measuring only TLB-hit translation.

### Compact example

With 4 KiB pages, virtual address `0x12345` has VPN `0x12` and offset `0x345`. If the current address space maps VPN `0x12` to PFN `0x9a` with read permission, a load targets physical address `0x9a345`. A write faults if write permission is absent. A fault handler may recognize a valid copy-on-write mapping, allocate and copy a frame, publish a writable replacement, invalidate stale translation state, and retry.

### Connections

[OS-012](012-process-creation-and-program-loading.md) creates address spaces; [OS-027](027-shared-memory.md) relies on deliberate shared mappings. [OS-032](../ROADMAP.md) develops hierarchical page tables, and [OS-033](../ROADMAP.md) develops translation caches.

## Governing Question

Programs use addresses as if each process owns a large contiguous memory space. Hardware and the operating system jointly turn that illusion into isolated, sparse, shared, demand-loaded, and protected storage. The translation can be cached, nested, huge-page-backed, or absent.

The governing question is how the mapping state, hardware walk, permissions, faults, caches, and frame lifecycle compose so every successful access reaches the intended bytes and every rejected access fails safely. Correctness includes concurrency: changing a translation while another processor uses it is a distributed state transition inside one machine.

## Why This Matters

Address translation enables process isolation, shared libraries, memory-mapped files, copy-on-write fork, demand paging, guard pages, and virtualization. Its behavior affects nearly every load and store even when caches hide the cost.

Errors are security-critical. A writable alias can defeat read-only policy. Stale translation state can reach a reused frame. Overflow can validate the wrong range. Overbroad executable mappings expand code-injection opportunities. Fault paths can deadlock because they allocate or take locks from fragile contexts.

Performance decisions also interact with correctness. Larger pages reduce translation reach pressure but increase fragmentation and copying. Aggressive unmapping saves memory but forces invalidations and shootdowns. Review requires both semantic and measured evidence.

## Prerequisites and Retrieval

Recall binary representation, powers of two, processor privilege, process address spaces from [OS-012](012-process-creation-and-program-loading.md), and synchronization from [OS-021](021-critical-sections-in-the-kernel.md).

Retrieve these distinctions:

- virtual address, linear address, guest physical address, and host physical address may be different stages;
- page size determines offset width but architectures may support several page sizes;
- a page-table entry contains permissions and attributes, not only a frame number;
- a page fault can be expected control flow or a fatal policy violation;
- changing memory-resident tables does not automatically retire every cached translation;
- mapping lifetime and physical-frame lifetime require coordinated reclamation;
- translation correctness and translation performance require different evidence.

## Learning Objectives

After this module, you should be able to:

1. decompose and recombine virtual addresses for power-of-two page sizes;
2. explain address-space roots, page-table walks, leaf mappings, permissions, and faults;
3. distinguish absent, invalid, protected, demand, copy-on-write, and access-tracking states;
4. reason about aliases, mapping changes, invalidation, and safe frame reclamation;
5. analyze huge pages, nested translation, device mappings, and side-channel boundaries;
6. diagnose overflow, canonicality, alignment, permission, and stale-translation failures;
7. design experiments and assurance arguments with architecture-specific scope.

## Core Exposition

### The virtual-address abstraction

Each process normally executes in an address space selected by an architecture-specific root and associated identity. Identical numerical virtual addresses in two processes can translate to different physical frames. The kernel may also maintain shared regions or separate roots according to architecture and mitigation policy.

Virtual memory is sparse. A large valid address range does not imply that every address is mapped or resident. The OS can reserve ranges, create mappings lazily, and reject gaps.

### Page decomposition

For power-of-two page size `P=2^p`, the low `p` address bits are the offset and upper translated bits form the VPN. Alignment clears the low `p` bits. Round-up calculations require checked addition before masking to avoid overflow.

A range `[v,v+n)` can span several pages even when `n<P`. Validate the last byte using checked arithmetic and account for every page. Zero length and addresses near the maximum need explicit policy.

### Frames and mappings

Physical memory is divided into frames at a base granularity. A leaf translation pairs a virtual page with a physical frame and attributes. Several virtual pages may alias one frame for sharing, libraries, or kernel access.

Aliasing complicates protection and cache attributes. All aliases must use compatible memory types and lifetime rules. Removing one mapping does not free a frame while other mappings, pins, I/O, or kernel references remain.

### Translation roots and context

A privileged register or equivalent state identifies the current translation root and mode. Address-space identifiers can tag cached translations so context switches need not discard everything, but identifiers have finite scope and reuse rules.

The effective translation key therefore includes virtual page, address-space identity, privilege and mode, and sometimes virtualization context. Software must invalidate or version state before reusing an identity for unrelated mappings.

### Hierarchical lookup

Architectures commonly split VPN bits into indices for multiple page-table levels. The root entry points to the next table; a valid leaf entry supplies a frame at the supported page size. Larger leaf pages terminate the walk earlier and use more address bits as offset.

The exact number of levels, index widths, entry formats, and canonical-address rules are architecture-specific. Linux exposes a conceptual hierarchy and folds unused levels so common code can span architectures.

### Permissions

Entries can constrain read, write, execute, user or supervisor access and carry accessed, dirty, global, memory-type, and other attributes. Effective permission can combine multiple walk levels and processor control state.

Apply write xor execute where feasible, keep user and supervisor mappings distinct, and grant only required access. Permission upgrades and downgrades need correct synchronization and translation-cache invalidation.

### Accessed and dirty state

Architectures may record that a mapping was accessed or written, in hardware or through faults and software. Operating systems use this evidence for reclamation, writeback, and aging.

These bits are sampled state under concurrency. Clearing and observing them races with new accesses and cached translations. Algorithms need architecture-specific synchronization and tolerate approximate recency where policy permits.

### Fault categories

A translation can fault because the address is invalid, a table entry is absent, the page is intentionally nonresident, permissions reject the access, the address is noncanonical, alignment rules fail, or an architecture-specific condition applies.

The exception supplies context such as faulting address, access type, and privilege. The handler revalidates against current mapping state because another thread may have changed it between fault and lock acquisition.

### Demand allocation

A valid virtual region can have no frame yet. On first access, the handler allocates a zeroed frame or retrieves backing data, builds the entry, publishes it with required ordering, and retries. Failure returns an allocation or process-level fault according to policy.

Zeroing prevents disclosure of prior contents. Admission and memory limits remain enforceable even though reservation was cheap.

### Copy-on-write

After fork or snapshot, mappings can share a read-only frame. A write fault allocates a private frame, copies content, and installs a writable mapping for the writer. Concurrent faults need serialization or compare-and-publish logic so frames and references are not leaked or confused.

If the frame is already exclusively owned, an implementation may upgrade without copying under its rules. The proof must cover aliases, pins, refcounts, failure after allocation, and invalidation.

### Translation caches

Processors cache translations and walk intermediates. Changing a PTE in memory does not imply all processors immediately stop using the old cached result. The architecture defines invalidation instructions, ordering, scope, and when remote processors must participate.

OS-033 develops TLBs in detail. Here the core invariant is that frame reuse and permission changes wait until no stale translation can authorize the old access.

### Mapping updates

A safe update sequence depends on the change. Installing a new mapping, replacing a frame, revoking permission, and removing a mapping can require different barriers and invalidation. Break-before-make rules exist on some architectures and configurations.

Page-table memory itself has ownership. Walkers may observe entries concurrently, so publication uses architecture-approved atomicity and ordering. Reclaim tables only after walkers and cached references cannot use them.

### Huge pages

Larger pages increase translation reach per cache entry and reduce walk depth. They can improve streaming or large working sets. They also increase internal fragmentation, allocation constraints, copy-on-write cost, and blast radius of permission changes.

Promotion requires compatible contiguous mappings and attributes; demotion creates smaller entries and invalidation work. Measure hit rates, faults, memory waste, compaction, and tail latency.

### Shared and file mappings

Different virtual pages can map the same file-backed or shared frame. Visibility and synchronization rules belong to the mapping and language protocol, while address translation enforces reach and permission.

Truncating backing storage under active mappings can create faults. File durability is separate from translation and visibility. Validate object offsets and lifecycle in addition to virtual ranges.

### Kernel and user boundaries

Supervisor mappings must not be accessible from user mode. Architectural protections and mitigation strategies can limit speculative or transient exposure, but the exact defense depends on hardware and kernel configuration.

Copying data across the boundary validates the complete user range and handles faults without trusting a prior check forever. Another thread can change mappings unless the API pins, locks, copies, or otherwise establishes stability.

### Devices and memory types

Some physical addresses refer to devices rather than ordinary RAM. Their access width, order, side effects, cacheability, and barriers differ. Ordinary memory loads, speculative access, or incompatible aliases can be incorrect.

Use architecture and OS mapping APIs for device memory. A physical address alone does not describe safe access semantics.

### Nested translation

Virtualized systems can translate guest virtual to guest physical and then guest physical to host physical. Permissions and faults can arise at either stage, and cached combined translations add context.

Nested walks increase worst-case memory references, though caches reduce observed cost. Hypervisors coordinate invalidation, dirty logging, migration, and device access across both stages.

### Canonical and valid addresses

Architectures may implement fewer virtual-address bits than register width and require unused high bits to follow a canonical pattern. Applying arithmetic before validating canonicality or overflow can transform an invalid range into an apparently valid one.

Treat addresses as untrusted integers at interfaces. Use checked range helpers tied to the current address-width and privilege contract.

### Concurrency and locking

Faults and mapping operations can occur in many threads. Coarse address-space locks simplify invariants but limit scalability. Fine-grained table and region locks improve concurrency while increasing lifetime and lock-order complexity.

Fault handlers must know which operations may sleep, allocate, recurse into faults, or take other locks. Never hold a lock across user copy or I/O unless the contract permits resulting faults and waits.

### Security

Translation is an authority mechanism. Audit writable-executable aliases, user-supervisor separation, frame zeroing, stale translations, integer overflow, speculative exposure, device mappings, row and cache side channels, and privileged introspection.

Physical frame numbers can reveal sensitive placement information. Operating systems restrict page-table and physical mapping interfaces according to threat model.

### Observability and evidence

Record mapping operations, faults by cause, allocation and I/O latency, page sizes, permission changes, invalidations, shootdown time, working-set size, and memory pressure. Hardware counters and tracing require platform-specific interpretation.

Microbenchmarks distinguish hot translations from cold walks and faults. Preserve CPU, architecture mode, page size, kernel, mitigations, topology, load, and raw distributions.

### Assurance

Review translation changes as concurrent security state transitions. Prove range arithmetic, permission monotonicity where intended, publication, invalidation, and delayed reclamation. Inject faults and races, but recognize that testing cannot enumerate all interleavings or microarchitectural behavior.

Safety-relevant systems require named architecture, OS, security, concurrency, and independent reviewers. This chapter provides reasoning tools, not a certified MMU or kernel.

## Definitions and Notation

Let page size `P=2^p`. For virtual address `v`, `VPN=v div P` and `offset=v mod P`, with `0<=offset<P`. Address space `a` supplies translation `T_a(VPN)=(PFN,perm,attr,g)` at generation `g`. If valid and authorized, physical address is `PFN*P+offset` under checked representable arithmetic.

For range `[v,v+n)`, last exclusive address `e=v+n` must not overflow, and every VPN from `floor(v/P)` through `floor((e-1)/P)` for positive `n` must satisfy the requested access. Zero length is handled before `e-1`.

Let mapping reference count be `r`, pins `q`, and stale-translation possibility `z`. A physical frame is reclaimable only after the owning protocol establishes `r=0`, `q=0`, and `z=false` plus any device or kernel-specific references.

## Mechanisms, Invariants, or Proof Structure

A reviewable translation design follows ten obligations:

1. State address width, translation stages, page sizes, roots, and identity scope.
2. Use checked decomposition, alignment, and complete range validation.
3. Specify entry validity, leaf levels, permissions, attributes, and reserved encodings.
4. Separate absent, demand, copy-on-write, protected, and fatal fault states.
5. Publish table changes with architecture-defined atomicity and ordering.
6. Invalidate cached translations before permission or frame-lifetime guarantees depend on it.
7. Track aliases, mappings, pins, walkers, tables, and frames through delayed reclamation.
8. Analyze huge pages, sharing, devices, nesting, and concurrent mapping changes.
9. Enforce least privilege, zeroing, overflow safety, and introspection policy.
10. Measure hit, walk, fault, invalidation, and pressure regimes with scoped evidence.

The executable model decomposes and translates a 4 KiB-page virtual address and checks read versus write permission.

<!-- bijux-verify: {"id":"toy-address-translation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"vpn=0x12\noffset=0x345\nphysical=0x9a345\nread=allowed\nwrite=fault\n","stderr":""}} -->
```python
page_size = 4096
virtual = 0x12345
vpn, offset = divmod(virtual, page_size)
mapping = {0x12: (0x9A, {"read"})}
pfn, permissions = mapping[vpn]
physical = pfn * page_size + offset

print(f"vpn={vpn:#x}")
print(f"offset={offset:#x}")
print(f"physical={physical:#x}")
print("read=" + ("allowed" if "read" in permissions else "fault"))
print("write=" + ("allowed" if "write" in permissions else "fault"))
```

The toy uses one flat trusted mapping and unbounded integers. It omits table walks, caches, concurrency, faults, page sizes, address widths, attributes, and lifecycle.

## Alternatives and Trade-Offs

- Single-level tables simplify lookup but consume space proportional to virtual address range.
- Hierarchical tables allocate sparsely but add dependent walk memory references.
- Base pages limit fragmentation but increase table and translation-cache pressure.
- Huge pages improve reach but increase fragmentation, promotion, copy, and revocation costs.
- Hardware-managed walks reduce common trap overhead but constrain entry formats and invalidation rules.
- Software-managed translation misses increase flexibility but add exception-path cost.
- Coarse mapping locks simplify lifetime proofs but restrict parallel faults and updates.
- Fine-grained locking scales updates but complicates ordering and reclamation.
- Shared mappings reduce copies while expanding alias, synchronization, and corruption concerns.

## Failure Modes and Misconceptions

1. **“A pointer is a physical address.”** normal process pointers are interpreted through an address space.
2. **“All systems use 4 KiB pages.”** supported base and huge sizes vary.
3. **“A PTE only stores a frame.”** validity, permissions, attributes, and software states also matter.
4. **“Writing a PTE changes every CPU immediately.”** cached translations require defined invalidation.
5. **“Unmap means the frame is free.”** aliases, pins, walkers, and stale translations can remain.
6. **“Every page fault is a bug.”** demand allocation and copy-on-write intentionally fault.
7. **“A prior range check stays true.”** concurrent mapping changes can invalidate it.
8. **“Read-only means no writable alias exists.”** protection must cover every relevant mapping.
9. **“Huge pages are always faster.”** fragmentation, compaction, and fault costs can dominate.
10. **“Accessed bits give exact recency.”** observation and clearing race with access.
11. **“Physical RAM semantics apply to device mappings.”** ordering and side effects differ.
12. **“Canonicality follows from integer width.”** architectures impose additional address-form rules.
13. **“Nested translation only doubles one lookup.”** walks and caches interact at several levels.
14. **“A hot-load benchmark measures translation.”** hits omit cold walks, faults, invalidation, and pressure.

## Worked Examples

### Example 1

For 4 KiB pages, `0x12345` decomposes into VPN `0x12` and offset `0x345`. Mapping to PFN `0x9a` yields `0x9a345`; a read-only permission makes a write fault.

### Example 2

A 32-byte access begins 16 bytes before a page end. It crosses into the next page. Validating only the first VPN misses a fault or permission boundary.

### Example 3

Two processes map virtual `0x400000`; one reaches frame A and one frame B. Numerical equality does not imply shared storage. Mapping a common frame deliberately creates sharing.

### Example 4

A kernel clears a present entry and immediately reuses its frame. Another CPU retains the old translation and writes the reused frame. Invalidate and wait under the architecture protocol before reuse.

### Example 5

A write fault on a copy-on-write page races in two threads. Both allocate copies. Compare-and-publish or locking selects one installed mapping and releases the losing frame safely.

### Example 6

Range check computes `v+n` near the maximum address and wraps low. Checked addition rejects the request before page alignment or user access.

### Example 7

A writable kernel alias remains for a user page marked read-only. The user mapping is protected, but system-wide immutability is false. Audit aliases by the actual security property.

### Example 8

A huge-page promotion reduces translation misses but copies or compacts memory during a latency-critical burst. High-percentile latency worsens despite better steady-state throughput.

### Example 9

A hypervisor revokes guest access at the second stage while the guest first-stage entry remains valid. The combined translation must be invalidated in the correct virtualization context.

### Example 10

A diagnostic reads page-table state while mappings change and reports an impossible hybrid. It must hold the documented lock, use a snapshot interface, or label results best effort.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) develops MMUs, caches, privilege, and translation hardware. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames isolation, least privilege, aliases, speculative exposure, and side channels.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies invariants, hazards, observability, and assurance. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects address-space limits and faults to runtime isolation and operations.

Within this program, [OS-027](027-shared-memory.md) consumes mappings, while [OS-032](../ROADMAP.md), [OS-033](../ROADMAP.md), [OS-034](../ROADMAP.md), and [OS-035](../ROADMAP.md) develop page tables, TLBs, faults, and demand paging.

## References

- Linux kernel documentation, [Page Tables](https://docs.kernel.org/mm/page_tables.html), current page checked 2026-09-04. Hierarchies, frames, levels, folding, MMUs, TLBs, faults, permissions, and dirty state.
- Linux kernel documentation, [Process Addresses](https://docs.kernel.org/mm/process_addrs.html), current page checked 2026-09-04. Virtual regions, page tables, locks, faults, and concurrent modification.
- Linux kernel documentation, [Memory Management Concepts](https://docs.kernel.org/admin-guide/mm/concepts.html), current page checked 2026-09-04. Virtual and physical memory, pages, mappings, translation roots, hierarchy, and demand paging.
- RISC-V International, [*The RISC-V Instruction Set Manual, Volume II: Privileged Architecture*](https://docs.riscv.org/reference/isa/_attachments/riscv-privileged.pdf), current specification checked 2026-09-04. Address-translation modes, VPN fields, entries, permissions, faults, ASIDs, fences, and two-stage translation.
- Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), revision page checked 2026-09-04. Current paging, protection, translation caching, invalidation, and virtualization architecture references.
- Arm, [Learn the architecture: Memory management](https://developer.arm.com/documentation/101811/latest/), current documentation checked 2026-09-04. Translation regimes, tables, descriptors, permissions, attributes, faults, and TLB maintenance.
- Linux man-pages project, [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), current page checked 2026-09-04. Mapping creation, sharing, protection, offsets, huge pages, faults, and backing-size caveats.
- Linux man-pages project, [mprotect(2)](https://man7.org/linux/man-pages/man2/mprotect.2.html), current page checked 2026-09-04. Protection changes, alignment, access faults, protection keys, and errors.
- Linux kernel documentation, [Examining Process Page Tables](https://docs.kernel.org/admin-guide/mm/pagemap.html), current page checked 2026-09-04. User-visible page-map information, presence, swapping, exclusivity, privileges, and scanning.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching RISC-V page tables, address spaces, mapping, process growth, fork, traps, and kernel access.

## Exercises

### Exercise 1

For 16 KiB pages, decompose a set of virtual addresses and validate a range that begins near a page boundary. Include zero length and overflow.

### Exercise 2

Specify a safe permission downgrade and unmap protocol on a multiprocessor. Cover table updates, invalidation, identity, walkers, and frame reclamation.

### Exercise 3

Design a concurrent copy-on-write fault path. Include duplicate faults, allocation failure, aliases, pins, publication, invalidation, and cleanup.

### Exercise 4

Compare base and huge pages for a latency-sensitive workload. Include reach, fragmentation, faults, promotion, NUMA, and empirical method.

### Exercise 5

Construct an assurance review for a user-to-kernel range interface. Cover arithmetic, mapping races, faults, permissions, side channels, evidence, and human review.

## Answers to the Exercises

### Answer 1

With `P=16384=2^14`, offset is the low 14 bits and VPN is `v div P`. Use `divmod` or checked shifts and masks tied to `P`, not a hard-coded 4 KiB mask. For positive `n`, checked-add `e=v+n`; reject overflow, then validate pages from `v div P` through `(e-1) div P`. An access beginning eight bytes before the boundary with length sixteen needs two mappings and permissions.

Handle `n=0` before subtracting one; define whether it validates no memory or is rejected by the calling API. Validate architecture address width and canonical form before and after any permitted transformation. Page-round-up computes checked `v+(P-1)` before clearing low bits.

### Answer 2

Lock or version the address-space mapping, prevent new users of the old entry, and perform the architecture-approved break or permission update with required atomicity and ordering. Issue local and remote invalidation for the exact address-space identity and range or a conservatively broader scope. Wait for acknowledgments under the architecture's completion contract before relying on revoked permission.

Unmap also removes region metadata and reference ownership. Delay page-table and frame reclamation until concurrent walkers, faults, pins, aliases, I/O, and stale translations are excluded. Address-space identifier reuse occurs only after old tagged translations cannot match. Failure paths keep either the old valid mapping or a deliberately invalid, recoverable state.

### Answer 3

On a write-protection fault, lock or snapshot the region and PTE, confirm it is still the expected copy-on-write generation, and obtain references to the old frame. Allocate a zero-safe new frame without holding forbidden locks, copy stable content, then reacquire validation. Atomically publish only if the old entry still matches; otherwise release the unused copy and retry current state.

Update refcounts and reverse mappings in a defined order, preserve pins and shared aliases, install writable permission only for the new private frame, and perform required invalidation before retry. Allocation failure leaves the old read-only mapping intact and returns a defined process outcome. Concurrent winners cannot leak frames or decrement the old reference twice.

### Answer 4

Base pages require more leaf entries and TLB reach but allocate and revoke in smaller units. Huge pages reduce walk depth and translation misses for large contiguous working sets but consume contiguous memory, waste partial-page capacity, and enlarge copy-on-write, migration, and permission units. Promotion and compaction can create tail spikes; demotion adds tables and invalidation.

Benchmark representative footprint, access pattern, producer placement, NUMA policy, memory pressure, fork and copy behavior, and promotion settings. Record faults, TLB and walk events where reliable, compaction, CPU, memory waste, throughput, and high-percentile latency across repetitions. Preserve architecture, kernel, page sizes, topology, mitigations, and raw samples. Restrict conclusions to that environment.

### Answer 5

Define accepted address domain, zero-length rule, maximum length, access direction, privilege, canonicality, and fault outcome. Use checked arithmetic and validate every page. Establish mapping stability through copying helpers, locks, pins, or retry semantics; never trust a validation that another thread can invalidate. Enforce user-supervisor permissions and avoid writable-executable or incompatible aliases.

Test boundaries at zero, page ends, maximum address, overflow, unmapped gaps, protection changes, concurrent unmap, copy-on-write, memory pressure, and fault injection. Analyze speculative exposure, timing and page-presence disclosure, and pin denial of service. Named architecture, kernel-memory, concurrency, security, testing, safety, and independent-verification reviewers assess assumptions and residual risk. Passing tests and the toy arithmetic do not certify the interface.
