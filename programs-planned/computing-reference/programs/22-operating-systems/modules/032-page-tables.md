---
module_id: OS-032
program: Operating Systems
level: 1
module_number: 32
title: Page Tables
status: complete
last_verified: 2026-09-04
---

# Page Tables

## One-Page Review

### Governing question

How can software construct, publish, modify, and reclaim hierarchical translation tables so hardware resolves addresses efficiently without violating isolation or using stale mappings?

### Essential definitions

- A **page table** is a memory-resident translation structure interpreted by an MMU and managed by privileged software.
- A **table entry** points to a next-level table; a **leaf entry** maps a page or block and supplies permissions and attributes.
- A **root** is the initial table and translation context selected for an address space.
- A **page walk** indexes successive tables with virtual-page-number fields until it reaches a leaf or fault state.
- A **folded level** is a software abstraction for a hierarchy level absent from a particular hardware configuration.
- A **huge-page leaf** terminates a walk above the base-page level and maps a larger aligned region.
- A **break-before-make transition** invalidates an old mapping before installing an incompatible replacement when an architecture requires it.

### Central model, mechanism, or theorem

For `L` levels, `b` index bits per level, and `p` offset bits, a virtual address decomposes as `(vpn[L-1],...,vpn[0],offset)`. A walk begins at root frame `R`, reads entry `vpn[i]`, and either faults, follows a next-table pointer, or terminates at a valid leaf. A leaf at level `i` maps `2^(p+b*i)` bytes and requires corresponding virtual and physical alignment.

Sparse hierarchical tables allocate metadata only for populated regions. Their correctness depends on entry encoding, checked indices, permission accumulation, architecture-defined publication, translation-cache invalidation, and deferred reclamation of frames and table pages.

### Critical invariants

- Every entry is in exactly one valid architecture-defined state: invalid, table, leaf, or approved software encoding.
- Table pointers and leaf frames meet required alignment and physical-address-width constraints.
- Effective permissions never exceed the policy permitted by the region and all relevant walk levels.
- A leaf's mapped size matches its level; unused low physical-frame bits cannot create a misaligned large mapping.
- Newly reachable tables are fully initialized before publication, and invalidated tables are not freed while walkers or cached translations can use them.
- Mapping replacement follows required entry atomicity, ordering, invalidation, and break-before-make rules.
- Accounting covers root, intermediate, leaf, huge-page, duplicated, and shared table memory.

### Common failures

Common mistakes are treating every valid entry as a leaf, using a leaf at an illegal level, publishing an uninitialized child table, allowing reserved bits, misaligning huge mappings, forgetting permissions inherited from upper levels, freeing an empty table before remote walkers quiesce, modifying entries without the right lock, invalidating the wrong address-space identity, and estimating table cost as one entry per mapped page only.

### Compact example

In RISC-V Sv39, a 39-bit canonical virtual address uses three 9-bit VPN indices and a 12-bit offset. Address `0x123456789` decomposes into indices `4`, `282`, `86` and offset `0x789`. A root entry at index 4 can point to a level-1 table, whose entry 282 points to a level-0 table, whose entry 86 maps a 4 KiB page. A leaf at level 1 would instead map a properly aligned 2 MiB region.

### Connections

[OS-031](031-address-translation.md) defines the translation contract. [OS-033](../ROADMAP.md) adds translation caches and invalidation; [OS-034](../ROADMAP.md) uses faults to populate entries; [OS-036](../ROADMAP.md) applies replacement and reclamation under memory pressure.

## Governing Question

A flat array with one entry for every possible virtual page becomes enormous as address width grows. Hierarchies make sparse address spaces affordable by allocating lower-level tables only where mappings exist. Hardware then trades table memory for dependent lookup work, usually hidden by translation caches.

The governing question is how privileged software maintains this shared hardware-software data structure while processors concurrently translate addresses. Correctness is not just choosing the right frame number. It includes legal entry states, permissions, ordering, invalidation, table-page lifetime, and architecture-specific transition rules.

## Why This Matters

Page tables implement process isolation, sharing, demand paging, copy-on-write, executable permissions, device mappings, huge pages, and virtualization. They are both data structures and security policy consumed by hardware.

One malformed entry can expose privileged memory. One stale translation can write a frame that has been reassigned. One prematurely freed table can become attacker-controlled data while a walker still interprets it. Conversely, conservative invalidation and locking can dominate scalability.

Engineers need a model that separates portable hierarchy concepts from architecture encodings and kernel implementation details. Measurements must cover sparse and dense layouts, base and huge pages, faults, updates, and multiprocessor invalidations.

## Prerequisites and Retrieval

Recall powers of two, bit fields, tree traversal, concurrency, and [OS-031](031-address-translation.md). Recall locks and publication from [OS-021](021-critical-sections-in-the-kernel.md) and reference lifetime from [OS-027](027-shared-memory.md).

Retrieve these distinctions:

- table entries and leaf entries can share storage format but have different meanings;
- hierarchy level determines mapped size and required alignment;
- hardware entry encodings and an OS's generic table abstraction are distinct;
- present, valid, accessible, young, dirty, special, swapped, and migrating are not synonyms;
- page-table memory, mapped data frames, region metadata, and cached translations have different lifetimes;
- installing a mapping and revoking a mapping can require different synchronization;
- a smaller table footprint can increase walk depth or fragmentation elsewhere.

## Learning Objectives

After this module, you should be able to:

1. calculate multilevel indices, offsets, mapped sizes, and worst-case table memory;
2. distinguish invalid, next-table, base-page leaf, and huge-page leaf encodings;
3. explain sparse allocation, level folding, permissions, and software-defined nonpresent state;
4. design safe table allocation, publication, replacement, collapse, and reclamation;
5. reason about concurrent faults, locks, invalidations, and address-space identity;
6. compare base pages, huge pages, radix depth, inverted structures, and nested tables;
7. validate implementations with architecture-scoped tests, runtime checking, and measured evidence.

## Core Exposition

### Why hierarchy

Suppose an address space exposes `V` virtual pages and an entry consumes `E` bytes. A flat table costs `V*E` bytes even when only a few pages are mapped. A radix hierarchy allocates paths for populated regions plus shared upper nodes.

Hierarchy cost depends on clustering. Contiguous mappings share upper tables; scattered mappings can allocate many nearly empty nodes. Include allocator granularity because one used entry can require a full table page.

### Address fields

At each level, a VPN field indexes an entry. If a table page holds `2^b` entries, the field is `b` bits. The page offset consumes `p` low bits. Implemented virtual-address bits can also impose sign-extension or canonicality rules.

Extract indices only after validating address form. Use unsigned checked shifts and masks with architecture-defined widths. Do not let host-language shift behavior silently accept an invalid width.

### Walk states

Each step reads an entry atomically at the width required by the architecture. An invalid encoding faults. A valid table encoding supplies the aligned physical address of the next table. A legal leaf supplies output frame, permissions, and attributes.

Reserved combinations fault or have extension-specific meaning. Software cannot treat unknown bits as ignored. Entry interpretation includes translation mode and enabled architecture extensions.

### Leaf size by level

A base-page leaf consumes only the page offset beneath it. A leaf one level higher additionally treats the lower VPN field as output offset, multiplying size by `2^b`. At level `i`, mapped bytes are `2^(p+b*i)` in a uniform radix.

The physical output base must align to that size. Otherwise low bits that the walk expects to supply from the virtual address conflict with the encoded frame, producing an architectural fault or invalid mapping.

### Example: Sv39

Sv39 uses a 12-bit page offset and three 9-bit indices. Tables contain 512 eight-byte entries in a 4 KiB page. Level-0 leaves map 4 KiB, level-1 leaves 2 MiB, and level-2 leaves 1 GiB, with alignment matching each size.

This example clarifies the generic arithmetic but is not a template for every architecture. Intel and Arm modes vary in address widths, root layout, entry fields, leaf legality, and control registers.

### Entry permissions

Leaf entries commonly encode user or supervisor access, read, write, execute, accessed, dirty, global, and memory attributes. Some architectures combine permissions across upper and leaf entries. Control registers can further modify effective access.

Construct entries from reviewed helpers rather than arbitrary bit operations. Reject write-without-required-read or reserved combinations where the architecture does. Keep software bits within explicitly available fields.

### Nonpresent software states

An OS may use entries that hardware sees as invalid to encode swap locations, migration, guard state, poison, or other metadata. These states must never be mistaken for physical table pointers or accessible leaves.

Define an exclusive tagged state machine and conversion helpers. Validate that address and metadata bits fit without colliding with architecture extensions or encryption and physical-address fields.

### Allocation of table pages

To map a missing path, allocate a zeroed child table, initialize its metadata, and publish its pointer into the parent with architecture-approved ordering and atomicity. Zeroing prevents stale entries and information disclosure.

Concurrent creators can allocate duplicate children. A compare-and-install or parent lock chooses one; the loser releases its unreachable table. Allocation failure leaves the old hierarchy valid and reports a defined outcome.

### Publication

The child must be fully initialized before a hardware or software walker can reach it. A release-style publication concept captures intent, but the actual primitives come from the architecture and kernel page-table API.

Publishing a leaf likewise orders frame initialization and entry visibility. Device or persistent-memory mappings may require additional attribute-specific ordering beyond ordinary RAM.

### Modification locking

Operating systems combine address-space locks, region locks, per-table locks, atomic entry operations, and read-side lifetime schemes. Lock choice depends on whether the operation changes region metadata, upper tables, or a single leaf.

Follow a global lock order. Fault handlers can allocate and retry, so they must revalidate the entry after dropping a lock. A cached pointer to a table is unsafe unless its lifetime remains protected.

### Permission upgrades and downgrades

Making an entry more permissive can have different ordering needs from revoking access. Revocation must ensure no processor continues using a stale permissive translation. Architecture helper contracts encode some of these differences.

Compare old and new entries, classify the transition, and apply exact invalidation scope. Do not optimize away invalidation based only on memory equality if cached derived state can differ.

### Break before make

Some incompatible mapping changes require clearing the old valid entry, ordering that invalidation, invalidating cached translation state, and only then installing the replacement. Overwriting in place can permit unpredictable mixtures of old and new attributes.

The requirement and exact sequence are architecture-specific. Generic code uses provided change helpers rather than assuming x86, Arm, or RISC-V rules transfer unchanged.

### Removing leaves

Unmapping first prevents new translations, then invalidates old cached translations, updates reverse mapping and accounting, and releases mapped-frame references when safe. Batching can amortize invalidation but extends the interval before reuse.

The PTE page may become empty, yet freeing it requires excluding concurrent faults and walkers. Parent entry removal, remote invalidation, grace periods, and table-page reclamation form one protocol.

### Collapsing and splitting

Contiguous compatible base mappings can collapse into a huge leaf if virtual and physical alignment, attributes, references, and policy allow. Splitting allocates lower tables, populates equivalent leaves, switches the parent, and invalidates as required.

Concurrent access must see only permitted old or new semantics. Failure during preparation retains the old mapping; failure after the transition follows an explicit recovery state.

### Sparse versus dense regions

Stacks, heaps, mapped files, and sparse reservations produce different table occupancy. A dense region amortizes upper nodes. Random single pages can cost one or more table pages each until paths converge.

Track page-table memory per address space and workload. Attackers can exploit sparse mappings to consume kernel memory even when resident data is small.

### Shared kernel mappings

Kernels may share upper mappings among address spaces or maintain separate views for isolation. Global translations reduce switch cost but enlarge the impact of erroneous permissions and invalidation.

Architecture mitigations can require separate user and kernel roots. Measure context-switch and table memory cost under the actual mitigation configuration.

### Recursive and direct access

Software needs a way to address table pages: a direct physical map, temporary mapping, recursive table entry, or architecture-specific helper. Each method has address-space, recursion, permission, and concurrency constraints.

Do not expose page tables writable to user mode. Debug and introspection paths use stable snapshots or documented locks and redact physical information when required.

### Translation-cache interaction

Hardware can cache leaf translations and intermediate walk results. Table memory is therefore not the only copy of effective state. Invalidation must cover the relevant virtual range, address-space identifier, page size, processor set, and virtualization stage.

OS-033 develops these caches. Page-table code must expose changes through the architecture's invalidation interface before reclamation or permission claims rely on them.

### Page-table accounting

Account root pages, intermediate pages, duplicated roots, huge-page metadata, reverse mappings, locks, and deferred-free queues. Table pages themselves consume memory and can trigger reclaim or allocation failure.

Report both logical entries and allocated bytes. A one-entry table page is not eight bytes of physical cost.

### Nested tables

Virtualization can combine guest and host hierarchies. A guest walk reads guest page-table entries through a second translation stage, multiplying potential memory references. Hardware caches intermediate and combined results.

Both layers require identity, invalidation, dirty tracking, permission, and reclamation. A host cannot trust guest entries as host physical addresses.

### Devices and IOMMUs

IOMMUs use related tables to translate device-generated addresses. Device caches and asynchronous transactions create distinct invalidation and completion rules. CPU page-table helpers are not automatically correct for DMA.

Pinning and unmapping coordinate devices, drivers, IOMMU state, and physical pages. Reuse waits for completed invalidation and outstanding DMA exclusion.

### Validation and hardening

Boot-time helper tests can check architecture implementations against generic semantics. Runtime page-table checking can detect illegal flag combinations or prohibited mappings closer to creation, with memory and performance overhead.

Validators are defense in depth, not substitutes for transition proofs. They cover configured rules and observed operations, not every stale cache, race, or microarchitectural behavior.

### Observability

Record table pages, occupancy, allocation failures, walk depth, huge-leaf use, splits, collapses, permission changes, invalidation scope and duration, shootdowns, and deferred frees. Correlate with faults and workload phases.

Debug walks must declare synchronization. A best-effort dump can combine generations and should not be treated as proof of an impossible hardware walk.

### Security and assurance

Audit entry construction, reserved bits, physical width, user-supervisor access, write-execute combinations, aliases, zeroing, invalidation, identifier reuse, table-page reuse, sparse-memory exhaustion, and introspection.

Assurance combines architecture review, state-machine reasoning, concurrency analysis, runtime checks, fault injection, and measured evidence. This chapter does not certify any concrete page-table implementation.

## Definitions and Notation

Let base page size be `2^p`, uniform entries per table be `2^b`, and levels be `L`. Virtual address `v` decomposes into `L` indices `vpn[i]` and `p` offset bits. A leaf at level `i` maps `M_i=2^(p+b*i)` bytes.

Let entry state be one of `I` invalid, `N(q)` next table at frame `q`, `L_i(f,perm,attr)` leaf at level `i`, or `S(x)` approved software state that hardware treats as nonpresent. These states are disjoint under a fixed translation mode.

If table pages have size `P_t` and `n_t` pages are allocated, table footprint is at least `n_t*P_t` plus metadata. Entry count alone is insufficient. Reclamation requires no reachable parent pointer, no relevant walker, no stale cached translation, and no protected software reference.

## Mechanisms, Invariants, or Proof Structure

A reviewable page-table implementation follows ten obligations:

1. Fix translation mode, address form, levels, radix, page sizes, and entry width.
2. Decode mutually exclusive invalid, table, leaf, reserved, and software states.
3. Check address width, indices, physical width, leaf legality, alignment, and attributes.
4. Accumulate effective permissions and enforce least privilege across aliases.
5. Zero and initialize child tables before atomic, ordered parent publication.
6. Lock or validate every concurrent allocation, fault, permission, and structural transition.
7. Apply architecture-defined replacement, break-before-make, and invalidation sequences.
8. Delay leaf, frame, and table-page reclamation until walkers and caches are excluded.
9. Bound and account sparse tables, huge-page transitions, nesting, and deferred work.
10. Test helpers and transitions while labeling architecture and measurement scope.

The executable Sv39 model computes indices and mapped sizes for each possible leaf level.

<!-- bijux-verify: {"id":"toy-sv39-indices","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"vpn=4,282,86\noffset=0x789\nleaf-sizes=4096,2097152,1073741824\nentries-per-table=512\n","stderr":""}} -->
```python
virtual = 0x123456789
offset_bits = 12
index_bits = 9
levels = 3
mask = (1 << index_bits) - 1

indices_low_first = [
    (virtual >> (offset_bits + index_bits * level)) & mask
    for level in range(levels)
]
indices = list(reversed(indices_low_first))
sizes = [1 << (offset_bits + index_bits * level) for level in range(levels)]

print("vpn=" + ",".join(map(str, indices)))
print(f"offset={virtual & ((1 << offset_bits) - 1):#x}")
print("leaf-sizes=" + ",".join(map(str, sizes)))
print(f"entries-per-table={1 << index_bits}")
```

The toy checks arithmetic only. It omits canonicality, PTE encoding, permissions, physical width, memory reads, faults, caches, concurrency, and lifetime.

## Alternatives and Trade-Offs

- Flat tables provide direct indexing but scale with the entire virtual page space.
- Radix hierarchies support sparse spaces but add dependent walks and table-page allocation.
- More levels extend address width while increasing cold-walk and metadata costs.
- Base leaves minimize fragmentation but increase PTE count and TLB pressure.
- Huge leaves reduce depth and metadata but require alignment and complicate split, copy, and revoke.
- Shared roots reduce memory and switching but enlarge invalidation and isolation coupling.
- Fine-grained locks improve parallel modification but complicate table lifetime and lock ordering.
- Batched unmap amortizes shootdowns but delays physical reuse and resource return.
- Runtime table checking catches corruption early but consumes memory and execution time.

## Failure Modes and Misconceptions

1. **“Every valid entry maps data.”** it may point to another table.
2. **“A leaf is legal at every level.”** modes restrict levels and alignment.
3. **“Zeroing new tables is optional.”** stale valid bits can publish unintended mappings.
4. **“Upper entries carry no policy.”** effective permissions can include several levels.
5. **“Reserved bits are available to software.”** extensions and hardware define them.
6. **“Entry write completes publication.”** ordering and cache invalidation remain.
7. **“An empty table can be freed immediately.”** concurrent walkers may retain access.
8. **“One PTE costs one entry width.”** sparse mappings allocate whole table pages and metadata.
9. **“Huge pages only change performance.”** they change alignment and transition units.
10. **“A generic helper has identical machine encoding.”** abstraction semantics span different architectures.
11. **“A TLB flush always means global flush.”** scope includes range, identity, CPU, and stage.
12. **“Hardware ignores nonpresent contents.”** software must still keep encodings disjoint and safe.
13. **“CPU and IOMMU tables share lifecycle rules.”** device transactions add distinct completion.
14. **“A page-table dump is a consistent snapshot.”** concurrent changes can mix generations.

## Worked Examples

### Example 1

Sv39 address `0x123456789` yields root-to-leaf indices 4, 282, 86 and offset `0x789`. Each index selects one of 512 entries.

### Example 2

A level-1 Sv39 leaf maps 2 MiB. Encoding a PFN not aligned to 2 MiB is invalid because lower VPN bits supply that portion of the output address.

### Example 3

Two faults allocate the same missing child table. A parent lock installs one and the loser releases its zeroed unreachable allocation. Both then rewalk current state.

### Example 4

A kernel initializes a parent pointer before clearing old bytes in the child. A hardware walker observes a stale valid entry. Initialize fully, then publish with required ordering.

### Example 5

A permission downgrade changes writable to read-only but omits remote invalidation. Another CPU writes through a cached permission. Revocation completes only after the invalidation protocol.

### Example 6

A last leaf is removed and its table page appears empty. A concurrent fault still holds a protected pointer. Deferred reclamation waits until the reader exits.

### Example 7

One mapped page in each widely separated upper region allocates many table pages. Resident data is small while kernel table memory grows. Per-address-space accounting detects the attack.

### Example 8

Base entries collapse into a huge leaf during access. Preparation builds equivalent state; the architecture-approved switch and invalidation ensure walkers see an allowed old or new mapping.

### Example 9

A guest PTE points to guest physical frame 20. The hypervisor translates that frame again. Treating 20 as host physical bypasses the second-stage isolation model.

### Example 10

A debugging walk reads a parent, loses the lock, and follows a freed child. Stable walker APIs or lifetime protection are required even for diagnostics.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies radix trees, sparse representations, tagging, and reclamation. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) develops MMU walks, caches, privilege, and memory attributes.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames page tables as authority-bearing state. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies invariants, capacity, hazards, observability, and assurance.

Within this program, [OS-031](031-address-translation.md) defines addresses, while [OS-033](../ROADMAP.md), [OS-034](../ROADMAP.md), [OS-035](../ROADMAP.md), and [OS-036](../ROADMAP.md) cover translation caches, demand, faults, and replacement.

## References

- Linux kernel documentation, [Page Tables](https://docs.kernel.org/mm/page_tables.html), current page checked 2026-09-04. Linux hierarchy, folding, MMU walks, faults, base and huge leaves, and architecture abstraction.
- Linux kernel documentation, [Process Addresses](https://docs.kernel.org/mm/process_addrs.html), current page checked 2026-09-04. Region and page-table locking, PTE access, stability, modification, and traversal.
- Linux kernel documentation, [Architecture Page Table Helpers](https://docs.kernel.org/next/mm/arch_pgtable_helpers.html), current page checked 2026-09-04. Generic entry-state and modification semantics expected from architecture implementations.
- Linux kernel documentation, [Page Table Check](https://docs.kernel.org/mm/page_table_check.html), current page checked 2026-09-04. Runtime hardening, illegal mappings and flags, double mapping, overhead, and limitations.
- RISC-V International, [Supervisor-Level ISA](https://docs.riscv.org/reference/isa/priv/supervisor.html), current specification checked 2026-09-04. Sv39, Sv48, Sv57, PTE states, page walks, permissions, alignment, ASIDs, and fences.
- Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), revision page checked 2026-09-04. Current paging structures, entry formats, permissions, large pages, caching, and invalidation references.
- Arm, [Learn the architecture: Memory management](https://developer.arm.com/documentation/101811/latest/), current documentation checked 2026-09-04. Translation tables, descriptor types, blocks and pages, attributes, faults, and maintenance.
- Linux kernel documentation, [Examining Process Page Tables](https://docs.kernel.org/admin-guide/mm/pagemap.html), current page checked 2026-09-04. Pagemap interfaces, page state, privilege restrictions, and observation limits.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching Sv39 page-table construction, walking, mapping, freeing, process address spaces, and traps.

## Exercises

### Exercise 1

For a four-level table with 9-bit indices and 12-bit offset, calculate indices, leaf sizes, flat-table cost, and sparse-table worst cases for a supplied mapping set.

### Exercise 2

Design concurrent missing-path allocation. Cover zeroing, duplicate allocation, parent locking, publication, retry, failure, and accounting.

### Exercise 3

Specify a permission downgrade and leaf removal protocol. Include entry transition, invalidation scope, address-space identity, walkers, frame and table reclamation.

### Exercise 4

Design collapse from base leaves to one huge leaf and rollback. State alignment, compatibility, locking, reference, failure, and observability requirements.

### Exercise 5

Construct an assurance review for page-table helper code. Cover encodings, reserved bits, tests, concurrency, IOMMU distinctions, evidence, and human review.

## Answers to the Exercises

### Answer 1

With `b=9`, `p=12`, and four levels, extract indices at shifts 39, 30, 21, and 12, each masked by 511; offset is masked by 4095. Leaf sizes from lowest upward are 4 KiB, 2 MiB, 1 GiB, and 512 GiB if the architecture permits leaves at those levels. Legality is separate from arithmetic.

A flat base-page table for `2^(12+36)` virtual bytes needs `2^36` entries; at eight bytes each it consumes `2^39` bytes. A radix hierarchy allocates a root and paths for mapped regions. Worst-case sparse placement maximizes distinct nodes at each lower level, capped by mapped pages and fan-out; calculate whole table pages, not used entry bytes. State address-width and canonical restrictions.

### Answer 2

Walk under the required parent-table lifetime and lock. When an invalid entry needs a child, allocate a zeroed table outside locks that forbid allocation, initialize metadata and accounting provisionally, reacquire the lock, and compare current entry. If another actor installed a compatible child, release the candidate and follow the winner. If state is incompatible, abort or retry.

If still missing, order all child initialization before atomically publishing the aligned table descriptor. Release the lock, rewalk if the API requires it, and expose committed accounting. Allocation failure changes no reachable hierarchy. Every losing and error path frees exactly one unreachable candidate, and a concurrent teardown prevents publication through generation or lock validation.

### Answer 3

Classify the old leaf and desired transition while holding the page-table and region protection required by the OS. Apply the architecture helper for write protection or clear the leaf if break-before-make is required. Order the update, invalidate the exact range, page size, address-space identity, processors, and translation stage, then wait for completion before relying on revocation.

For removal, delete reverse mapping and mapping references in defined order. Prevent new walkers, and defer mapped-frame reuse until pins, aliases, remote cached translations, and protected readers are gone. If the containing table becomes empty, remove its parent pointer and separately defer the table page until software and hardware walkers cannot reach it. Failure leaves a defined valid or invalid state.

### Answer 4

Require virtual and physical alignment to huge size, contiguous frames, identical compatible permissions and attributes, no incompatible pins or per-page states, and policy approval. Lock the region and affected tables, revalidate every base leaf and reference, prepare the huge descriptor without exposing it, and use the architecture's valid transition and invalidation sequence.

Before the commit point, allocation or validation failure leaves base mappings unchanged. After clearing old state, rollback follows a prebuilt-table or explicit recovery protocol. Update reverse mappings, accounting, accessed and dirty aggregation, and deferred lower-table reclamation. Concurrent faults and observers see only permitted old, transitional-invalid, or new state. Record collapse latency, failures, fragmentation, invalidation, and later split cost.

### Answer 5

For each translation mode, enumerate invalid, table, leaf, reserved, huge, swap, migration, special, and extension encodings. Verify physical width, alignment, legal leaf levels, permission combinations, software-bit allocation, and round-trip helper behavior. Boot tests and runtime checking exercise creation and modification semantics, illegal flags, double mappings, huge transitions, and configured extensions.

Concurrency review covers locks, atomic width, ordering, faults, invalidation, identity reuse, walkers, and delayed reclamation. IOMMU code receives separate device-cache and DMA completion analysis. Preserve architecture revision, kernel configuration, test logs, fault injection, and performance overhead. Named architecture, memory-management, concurrency, virtualization, device, security, testing, safety, and independent reviewers assess residual risk. Passing helper tests is not certification.
