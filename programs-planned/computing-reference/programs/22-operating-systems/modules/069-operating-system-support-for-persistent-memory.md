---
module_id: OS-069
program: Operating Systems
level: 2
module_number: 69
title: Operating-System Support for Persistent Memory
status: complete
last_verified: 2026-09-04
---

# Operating-System Support for Persistent Memory

## One-Page Review

### Governing question

How should an operating system discover, provision, map, flush, protect, observe, and recover byte-addressable persistent memory so that applications receive explicit durability and failure-atomicity guarantees rather than accidentally treating ordinary memory visibility as persistence?

### Essential definitions

- **Persistent memory (PMEM)** is nonvolatile media exposed close enough to the processor's load/store path that software can access it through memory mappings, while retaining data across a specified loss of power.
- A **persistence domain** is the platform boundary inside which accepted data survives the failures covered by the platform contract.
- **Visibility** means another observer can read a value; **persistence** means the value has reached the applicable durability domain. Neither implies the other without an explicit contract.
- A **region** is a platform-described range assembled from one or more persistent-memory devices, possibly interleaved across them.
- A **namespace** is a persistently identified allocation of region capacity presented through a mode such as `fsdax`, `devdax`, `sector`, or `raw`.
- **Filesystem DAX (fsdax)** permits direct mappings of file extents and avoids page-cache copies while retaining filesystem naming, allocation, permissions, and metadata.
- **Device DAX (devdax)** exposes a character device whose address range can be mapped directly, without filesystem file semantics.
- A **cache-line writeback** initiates movement of dirty processor-cache data toward the persistence domain; an ordering or persistence barrier establishes required completion and order according to the architecture.
- **Failure atomicity** means that recovery observes one allowed complete state, not an arbitrary mixture of an interrupted multi-location update.
- A **media error** or **poison** marks an address range whose contents cannot be consumed reliably and may surface as an I/O error or a synchronous machine-check-style fault, depending on the access path.

### Central model, mechanism, or theorem

Represent an update as data records $D$, a publication record $C$, and a platform persistence relation $\prec_p$. A recoverable commit requires

$$
D_1, D_2, \ldots, D_n \prec_p C,
$$

plus a recovery predicate that accepts $C$ only when its version, checksum, length, and references validate. The implementation must translate that relation into the correct mapping, cache writeback, persistence barrier, filesystem synchronization, and device behavior for the actual platform. A CPU store, cache coherence, `mmap`, `write`, or an interrupt alone does not establish $\prec_p$.

The operating system owns the end-to-end resource lifecycle: firmware discovery, region assembly, namespace labels, stable identity, mode selection, page metadata, mapping revocation, bad-block reporting, security state, firmware activation, hotplug, and evidence. Applications own data-structure protocols above the mapping, but the kernel must expose no stronger durability or atomicity than the path implements.

### Critical invariants

- A physical device, interleave set, region, namespace, block device, DAX device, filesystem, file, and virtual mapping retain distinct identities and lifetimes.
- Capacity is not exposed until firmware descriptors, address ranges, interleave geometry, labels, and conflicts validate.
- Namespace mode, alignment, metadata placement, and destructive reconfiguration are explicit and auditable.
- CPU visibility, cache coherence, device visibility, and persistence are never treated as synonymous.
- Data reaches the persistence domain before the commit record that makes it recoverable.
- Recovery accepts only self-consistent versions and never follows unchecked persistent offsets or lengths.
- Filesystem data and filesystem metadata use the filesystem's durability contract; raw mappings use the applicable architecture and library contract.
- Every mapping is revoked or proven unreachable before capacity is removed, reconfigured, sanitized, or repurposed.
- Poison, bad blocks, health degradation, and synchronization failures reach the responsible owner and cannot be cleared as if clearing restored lost data.
- Backup, encryption, access control, sanitization, and secret retention account for persistence across process exit, reboot, and device transfer.

### Common failures

Common mistakes are calling persistent memory “RAM that survives reboot,” assuming byte addressability means byte failure atomicity, using a volatile store as a durable commit, issuing cache-line writeback without a barrier, assuming a memory barrier flushes dirty cache lines, confusing ADR or eADR marketing with a measured platform contract, selecting DAX only for speed, using transient `/dev/pmemN` names as identity, changing namespace mode without a destructive-change gate, trusting a checksum without bounding its covered length, clearing poison without restoring data, treating `msync` and `fsync` as interchangeable everywhere, unmapping while another process retains a reference, and benchmarking steady state without crash recovery.

### Compact example

Two fixed slots contain version, value, checksum, and commit state. Version 1 is valid and committed. Version 2 has valid data but its commit bit was not made persistent before the simulated crash. Recovery rejects version 2 and selects version 1. The example demonstrates publication ordering and validation only; it executes no persistent-memory instruction and proves nothing about a real cache, filesystem, or device.

### Connections

[OS-031](031-address-translation.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-042](042-inodes-and-metadata.md), [OS-055](055-numa-memory-placement.md), [OS-061](061-device-discovery-and-driver-models.md), [OS-063](063-direct-memory-access.md), [OS-064](064-block-and-character-devices.md), [OS-067](067-zero-copy-and-kernel-bypass.md), and [OS-068](068-storage-queues-and-nvme.md) connect persistent memory to mappings, filesystems, topology, device lifecycle, I/O semantics, direct access, and storage identity.

## Governing Question

Persistent memory crosses boundaries that operating systems traditionally kept separate. Volatile memory normally offers load/store access but loses state on power failure. Storage normally survives power failure but is reached through block I/O, buffering, and explicit synchronization. Persistent memory can offer both direct access and retention, but it does not erase the need to define ordering, atomicity, ownership, recovery, or errors.

The governing question is therefore not how to bypass one copy. It is how to expose a trustworthy durability contract through firmware, kernel, filesystem, processor caches, libraries, and application recovery. Each layer can weaken the whole path. A fast store whose commit marker reaches media before its payload is a fast corruption mechanism.

## Why This Matters

Direct access can remove page-cache duplication, system calls on the data path, block submission, and interrupt completion. Those savings matter for small random accesses and memory-like data structures. They also transfer responsibilities to software that storage stacks previously centralized: cache flushing, failure-atomic updates, media-error handling, and recovery validation.

Persistent memory changes failure shape. A programming error can become durable. Stale pointers, allocator damage, exposed secrets, and partially initialized objects survive restart. A load from poisoned media can fault synchronously rather than return an ordinary block I/O error. An administrator can destroy a namespace while believing it is merely changing a performance mode.

The technology also informs newer memory tiers and CXL-attached capacity. Even when a particular medium changes, the operating-system questions remain useful: what is the identity, where is the persistence domain, which agent owns cache state, how is removal contained, and what can recovery prove?

## Prerequisites and Retrieval

Review [OS-002](002-privilege-levels-and-protection-rings.md), [OS-004](004-interrupts-and-exceptions.md), [OS-031](031-address-translation.md), [OS-034](034-demand-paging.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-042](042-inodes-and-metadata.md), [OS-055](055-numa-memory-placement.md), [OS-061](061-device-discovery-and-driver-models.md), [OS-062](062-memory-mapped-and-port-mapped-i-o.md), [OS-063](063-direct-memory-access.md), [OS-064](064-block-and-character-devices.md), and [OS-068](068-storage-queues-and-nvme.md).

Retrieve these distinctions:

- retention, durability, recoverability, consistency, and availability are different properties;
- a CPU store can reside in a store buffer, processor cache, memory-controller queue, or persistent domain;
- cache coherence orders observations among processors but does not by itself define power-fail persistence;
- a compiler barrier, CPU memory barrier, cache-line writeback, and persistence barrier solve different problems;
- firmware device, region, namespace, device node, filesystem, inode, file offset, and virtual address are different names;
- page-cache bypass does not bypass filesystem allocation, permissions, metadata, or recovery;
- block I/O errors and load/store machine checks have different delivery and containment paths;
- logical checksums detect some corruption but do not repair missing redundancy;
- synchronization success is evidence under a contract, not proof against failures outside that contract;
- a crash-consistent local structure is not automatically application-consistent across several structures or services.

## Learning Objectives

After this module, you should be able to:

1. distinguish persistent memory from volatile RAM, conventional storage, memory-mapped I/O, and ordinary file mappings;
2. trace platform discovery through devices, interleave sets, regions, namespace labels, modes, device nodes, filesystems, and process mappings;
3. state persistence-domain, visibility, ordering, atomicity, and recovery assumptions explicitly;
4. design failure-atomic updates using logs, copy-on-write, dual slots, versions, checksums, and ordered publication;
5. choose among block access, fsdax, devdax, sector translation, and raw mode from semantics rather than fashion;
6. handle NUMA placement, page metadata, hotplug, poison, health, security, sanitization, firmware, virtualization, and backup;
7. test crash behavior with enumerated crash points, fault injection, recovery oracles, and evidence scoped to the actual platform.

## Core Exposition

### Persistent memory is a contract

A medium is useful as persistent memory only through a complete platform contract. The contract states which writes survive which failures, where energy-backed buffering ends, which instructions or system calls establish persistence, what atomic granularity is guaranteed, and how errors surface.

“Nonvolatile” describes retention of the medium. It does not establish that the latest CPU stores reached it or that a multi-field object is consistent. “Byte addressable” describes access granularity. It does not establish byte-level power-fail atomicity.

### Platform discovery

On firmware-described systems, tables such as ACPI NFIT identify persistent-memory devices, address ranges, interleave descriptions, flush hints, and health interfaces. The kernel validates table lengths, address arithmetic, overlap, device references, and supported capabilities before constructing objects.

Firmware is input, not authority beyond validation. Malformed or conflicting descriptors must not cause arbitrary physical memory to be mapped or exposed.

### Devices, interleave sets, and regions

A physical NVDIMM is not necessarily a contiguous namespace. Firmware can interleave system physical addresses across several devices to increase bandwidth or meet platform geometry. The kernel assembles compatible mappings into a region.

Failure scope follows this construction. Losing one member of an interleave set can affect addresses distributed across the region. Inventory and incident tooling must preserve the mapping from a failing device to regions and namespaces.

### Namespace labels

Namespace labels persistently describe how region capacity is allocated and identified. They carry identifiers and mode-related metadata so the same allocation can be reconstructed after reboot.

Label updates need their own redundancy and sequencing. A valid data area with corrupt allocation metadata can become inaccessible or be assigned twice. Before repair, preserve raw evidence and determine whether the label state, media, or both are damaged.

### Stable identity

Kernel enumeration names such as `/dev/pmem0` can depend on discovery order. Automation should use namespace UUIDs or stable links and verify expected size, mode, region, and ownership.

Identity validation matters before destructive commands. A human-readable tag is useful context but is not a cryptographic authorization or an exclusive ownership proof.

### Namespace modes

Linux tooling commonly exposes `raw`, `sector`, `fsdax`, and `devdax` modes. Each changes the device interface, metadata, atomicity, and filesystem expectations.

Mode changes can destroy existing data. A safe control plane requires the namespace to be idle, verifies its durable identity, records the requested target, obtains explicit authorization, and confirms the resulting topology.

### Raw mode

Raw mode exposes namespace capacity with few abstractions. It does not add sector atomicity and can lack facilities needed for robust DAX integration.

Use it for specialized provisioning or diagnosis only when its limitations are part of the design. “Raw” does not mean faster under every workload or safer because fewer layers exist.

### Sector mode and BTT

Existing block software may assume a sector write is failure atomic. Persistent memory's native write path may permit a power failure to leave a sector containing old and new portions.

The Block Translation Table adds indirection and metadata so the exposed block device provides atomic sector-update semantics. This compatibility costs capacity, metadata work, and write amplification. It protects its stated sector abstraction, not arbitrary application transactions.

### Filesystem DAX

fsdax uses a block device under a DAX-capable filesystem. A file mapping can point at storage extents directly instead of page-cache pages. The filesystem still owns names, permissions, allocation, holes, truncation, reflink restrictions, and metadata recovery.

The active DAX state of a file can depend on filesystem flags, mount policy, media capability, and inode instantiation. Applications can query the effective state; they should not infer it from a mount string or directory flag alone.

### Device DAX

devdax exposes a character device whose capacity can be mapped directly. It offers an address-space object rather than files and directories. Alignment constraints and page-size support are part of the interface.

The application or runtime now owns allocation, naming inside the range, permissions beyond the device boundary, consistency, and recovery. Use devdax when that ownership is deliberate, not merely because it sounds more direct.

### Page metadata

Some kernel and subsystem operations require a `struct page` for each page frame. DAX modes may reserve capacity for this metadata or consume system RAM, depending on configuration.

Metadata placement affects usable capacity and scaling. Provisioning calculations must include it; otherwise a requested nominal namespace can yield less usable capacity than an operator expects.

### DAX and the page cache

Ordinary buffered files use page-cache pages that absorb reads and writes. DAX removes that extra data copy for supported mappings and direct I/O paths.

Bypass changes accounting and compatibility. Interfaces that pin ordinary pages, splice data, or expect page-cache behavior may be restricted when mappings lack normal page structures. DAX is an access mode with semantic consequences, not a universal acceleration switch.

### Faulting a DAX mapping

On a page fault, the filesystem resolves the file offset to an allocated extent, ensures newly allocated storage cannot expose stale data, and inserts an appropriate mapping. Filesystem locking must coordinate faults with truncate, hole punch, and extent relocation.

A mapping is a capability to persistent bytes. Revocation and layout changes must account for all processes and pins that can still reach those bytes.

### CPU stores and cache state

A normal cached store can become visible to another coherent CPU while remaining dirty in a processor cache. If that cache is outside the persistence domain, sudden power loss can discard the latest value.

The software protocol therefore identifies modified cache lines and invokes the architecture's persistence primitive or a maintained library that selects it. Hard-coding one instruction ignores CPU capability, mapping type, and platform domain.

### Writeback and barriers

A cache-line writeback begins or requests movement toward the persistence domain. A persistence barrier waits for or orders that movement as defined by the platform. Both may be required.

A general memory barrier can constrain observation order without evicting dirty data. Conversely, issuing writebacks for several lines without the required barrier may fail to establish the intended data-before-commit order.

### Persistence domains

Architectures and platforms can place processor caches, memory-controller queues, and device buffers inside or outside the protected domain. ADR commonly protects a platform-defined memory-controller path; eADR may extend protection further. Exact definitions are platform contracts, not portable assumptions.

Code should use stable persistence APIs and record the platform features under which tests ran. Recovery documentation must state the failures covered: process crash, kernel panic, warm reset, sudden power loss, device loss, or site loss are not equivalent.

### Filesystem synchronization

For conventional file writes, `fsync` requests synchronization of file data and required metadata. Creating or renaming a file can also require synchronizing the containing directory for a complete namespace durability protocol.

For mapped files, `msync` controls synchronization of a range under its interface. DAX and `MAP_SYNC` can support efficient direct persistence in conjunction with appropriate CPU instructions. The exact recipe depends on mapping and filesystem guarantees; one system call name is not a universal durability proof.

### Failure-atomic updates

Persistence does not make a multi-location update atomic. If a structure changes fields $a$, $b$, and $c$, a crash can occur between their persistence events.

Common protocols include write-ahead logging, undo logging, redo logging, copy-on-write, shadow paging, and dual-slot publication. Each defines allowed persistent states and a deterministic recovery choice.

### Data before publication

An immutable new record can be populated, validated, and persisted before a pointer or version record publishes it. The publication record is then persisted after the data barrier.

Recovery validates the publication record and every persistent reference before following it. The ordering relation matters more than source-code order because compiler, processor, and persistence mechanisms can each reorder or delay effects.

### Checksums and versions

A checksum can detect some torn or corrupted records. A monotonically interpreted generation helps recovery select among valid alternatives. Lengths, types, offsets, and reserved fields also require validation.

Checksums are not atomicity and versions are not freshness proofs by themselves. Protect the metadata describing checksum coverage, handle version wrap, and define what happens when no valid copy remains.

### Persistent pointers

A process virtual address is not a stable persistent pointer. Address-space layout, mapping base, namespace layout, and software version can change across restart.

Store bounded offsets or stable object identifiers. On recovery, validate arithmetic against the mapped length, alignment, object type, and allocation metadata before forming a pointer.

### Allocation and reclamation

A persistent allocator must make allocation metadata and object initialization crash consistent. Publishing an object before its initialization is durable exposes uninitialized or stale data.

Reclamation is harder when readers or old roots may still reference an object. Use epochs, reference protocols, logs, or copy-on-write roots, and make recovery able to distinguish allocated, initialized, published, retired, and reusable states.

### Concurrency and durability

Locks coordinate live threads but usually disappear on crash. A lock-protected sequence can still be persistently inconsistent unless it also follows a durability protocol.

Conversely, flushing every store does not make concurrent access race free. State both the volatile synchronization order and the persistence order, then prove that every crash prefix has a valid recovery outcome.

### Media errors and poison

Firmware and hardware can report uncorrectable media ranges. The kernel tracks affected blocks or addresses and surfaces them through device health, bad-block lists, I/O failures, or synchronous faults on direct access.

A DAX load can encounter poison in an instruction context. Applications needing availability must arrange containment, redundancy, signal or exception handling where supported, and repair. Retrying the same load indefinitely does not reconstruct data.

### Scrubbing and error clearing

Address-range scrubbing discovers latent errors before an application touches them. Monitoring turns health and threshold events into owned action.

Clearing an error can permit the address to be used again after the platform-specific repair or overwrite operation. It does not recover the former contents. Restore data from a verified replica or backup before declaring service recovery.

### Hotplug and removal

Removal begins by preventing new opens and mappings, quiescing users, revoking or unmapping access, draining kernel references, and only then dismantling namespaces and regions. Physical disappearance before containment can turn a later load into a fatal fault.

Busy refusal is a safety result. A force option must not silently convert live references into memory corruption.

### NUMA placement

Persistent-memory ranges have topology. A local processor may reach one region with lower latency or higher bandwidth than a remote processor.

Place threads, mappings, interrupts, and replicas according to measured topology. NUMA locality does not justify losing redundancy by placing all copies in one failure domain.

### Security and access control

File permissions, device permissions, namespaces, MAC policy, and process isolation govern who can map the range. Once mapped, load/store access may evade per-operation mediation that a system-call path would provide.

Minimize mapping scope, validate offsets, use least privilege, and treat a writable persistent mapping as a high-impact capability. Memory-safety bugs can corrupt durable state immediately.

### Encryption, keys, and sanitization

Device security functions can lock, unlock, erase, or overwrite supported media. Filesystem or application encryption can provide different threat boundaries. Key availability during early boot and recovery is part of operability.

Deleting a namespace or filesystem metadata is not guaranteed sanitization. Decommissioning must use a supported cryptographic erase or verified overwrite process and account for remapped or inaccessible media.

### Firmware lifecycle

Persistent-memory devices can contain firmware for media management and health. Staging and activating firmware may require quiescing memory activity or rebooting.

Treat activation as a coordinated maintenance event: inventory affected regions, preserve backups, stop mutations, verify health, activate, re-enumerate, and validate namespace identity and data before reopening service.

### Virtualization and emulation

A virtual machine can receive emulated, passed-through, or file-backed persistent memory. Each arrangement changes the persistence domain and failure path.

Host `fsync`, guest barriers, virtual firmware tables, migration, snapshots, and storage caches must compose. A guest instruction cannot force durability beyond what the host backing contract provides.

### Backup and replication

Persistent memory survives some local failures; it is not a backup. Software defects, operator mistakes, device loss, security compromise, and site loss can destroy durable bytes.

Capture application-consistent roots, validate checksums, quiesce or use a protocol-aware snapshot, and test restoration on independent storage. Byte-copying a structure during mutation can preserve an impossible state.

### Observability

Record stable namespace identity, device and region membership, mode, size, alignment, NUMA node, filesystem and mount state, DAX state, mappings, health, bad blocks, scrub results, firmware, security state, and destructive operations.

Application telemetry should include format version, selected recovery root, rejected records, checksum failures, repair actions, and recovery duration without exposing sensitive payloads.

### Testing persistence

Enumerate crash points around allocation, initialization, writeback, barrier, publication, reclamation, filesystem metadata, and replica acknowledgement. At each point, terminate the process, crash the kernel where feasible, or cut power in a controlled rig, then run an independent recovery oracle.

Emulation is valuable for state-machine coverage but cannot prove physical cache and power behavior. Hardware tests need platform inventory, repeatability, raw evidence, and explicit limits.

### Performance measurement

Compare buffered I/O, direct I/O, fsdax, and devdax only under equivalent semantics. Measure operation latency distributions, cache misses, flush and barrier costs, fault latency, remote-NUMA access, write amplification, recovery time, CPU cost, and capacity overhead.

Removing synchronization can produce impressive but invalid numbers. Benchmark the durability level the application actually promises.

## Definitions and Notation

Let:

- $P$ be a persistent-memory platform;
- $R$ be a firmware-described region;
- $N$ be a namespace allocated from $R$;
- $M$ be a virtual mapping of all or part of $N$;
- $D$ be the set of data records for one logical update;
- $C$ be the commit or publication record;
- $V(x)$ mean update $x$ is visible to a relevant observer;
- $W(x)$ mean dirty cache lines covering $x$ have been submitted for writeback;
- $P(x)$ mean $x$ has reached the applicable persistence domain;
- $x \prec_v y$ mean visibility of $x$ precedes visibility of $y$;
- $x \prec_p y$ mean persistence of $x$ precedes persistence of $y$;
- $G(x)$ be the generation stored in record $x$;
- $H(x)$ be the recorded checksum of $x$;
- $B(x)$ be the validated byte range occupied by $x$.

Visibility does not generally entail persistence:

$$
V(x) \nRightarrow P(x).
$$

Source order does not by itself entail persistence order:

$$
\operatorname{store}(x) <_{src} \operatorname{store}(y)
\nRightarrow x \prec_p y.
$$

A publication protocol requires:

$$
\left(\forall d \in D: P(d)\right) \land
\left(\forall d \in D: d \prec_p C\right) \land P(C).
$$

Recovery accepts a candidate $x$ only if:

$$
\operatorname{valid}(x)=
\operatorname{committed}(x) \land
B(x) \subseteq M \land
H(x)=\operatorname{checksum}(x) \land
\operatorname{format}(x)\in F_{supported}.
$$

Among valid candidates, a dual-slot design may choose the greatest generation under a defined non-wrapping or wrap-safe comparison:

$$
x^*=\arg\max_{x\in X,\ \operatorname{valid}(x)} G(x).
$$

This notation is a reasoning model. Real guarantees come from the architecture, kernel, filesystem, device, and platform contracts plus empirical validation.

## Mechanisms, Invariants, or Proof Structure

### Obligation 1: validate discovery

Every exposed address belongs to exactly one validated topology interpretation. Check firmware structure sizes, arithmetic overflow, physical overlap, interleave references, supported mappings, and reserved ranges before registration.

Counterexample: trusting a malformed length lets a region extend into ordinary RAM or MMIO, turning namespace access into corruption.

### Obligation 2: preserve identity

Destructive and recovery operations identify the namespace through durable identifiers plus expected topology and size, not discovery-order names alone.

Counterexample: after a boot-order change, an automation script reformats `/dev/pmem0` although the intended namespace is now `/dev/pmem1`.

### Obligation 3: make provisioning transactional

Namespace allocation, labels, mode, page metadata, device publication, and rollback form one controlled transition. Failed provisioning must not leave overlapping ownership or a falsely usable device.

Counterexample: a label update becomes visible on half an interleave set, and two hosts infer different allocations.

### Obligation 4: match access mode to semantics

The selected interface supplies all required naming, protection, allocation, alignment, atomicity, and recovery behavior, or the application explicitly supplies missing layers.

Counterexample: an application migrates from a sector-mode block device to raw mode while retaining its assumption that 512-byte writes cannot tear.

### Obligation 5: separate visibility from persistence

For every durable claim, identify the dirty bytes, mapping type, cache state, writeback primitive, barrier, persistence domain, and completion evidence.

Counterexample: one CPU reads another CPU's coherent store, but power fails before the dirty line leaves an unprotected cache.

### Obligation 6: order data before commit

All records reachable from a new durable root validate and persist before the root is persisted. Reclamation of the old graph occurs only after no valid recovery path requires it.

Counterexample: a new root pointer is durable while one referenced node still contains old or uninitialized bytes.

### Obligation 7: validate recovery input

Recovery treats persistent bytes as untrusted input. It bounds every length and offset, checks format and checksum, prevents arithmetic overflow and cycles, and chooses only a permitted version.

Counterexample: a torn length produces an out-of-range pointer that recovery dereferences before checksum validation.

### Obligation 8: compose filesystem durability

File data, extent allocation, size, names, and directory entries use the filesystem's documented ordering and synchronization rules. Application cache persistence does not substitute for missing namespace metadata durability.

Counterexample: durable file contents are unreachable after crash because the new directory entry was never synchronized.

### Obligation 9: contain mapping lifetime

Truncate, hole punch, device disable, mode change, firmware activation, sanitization, and hot-remove cannot proceed past the point of danger while live mappings or pins remain.

Counterexample: an old process writes through a devdax mapping after the range has been reassigned to another tenant.

### Obligation 10: surface media failure

Health and poison are attributed to affected addresses and owners. Fault delivery, repair, replica restoration, bad-block clearing, and service resumption form an auditable workflow.

Counterexample: an operator clears the bad-block record and reports recovery although the only copy of the data was lost.

### Obligation 11: preserve security across retention

Authorization covers open, mapping, administration, keys, backup, crash dumps, and decommissioning. Sanitization is verified against the device's supported semantics.

Counterexample: an application deletes its files, but secrets remain in unallocated persistent extents later assigned to another user.

### Obligation 12: scope evidence

Tests state platform, firmware, kernel, filesystem, namespace mode, mount state, persistence-domain assumption, workload, crash mechanism, and recovery oracle. Evidence proves only the exercised configuration and failure classes.

Counterexample: a process-kill test is presented as evidence that dirty processor caches survive sudden power removal.

## Alternatives and Trade-Offs

- **Buffered file I/O versus fsdax:** buffering provides mature caching and compatibility; fsdax removes copies and changes fault, pinning, and persistence responsibilities.
- **fsdax versus devdax:** fsdax retains filesystem objects and metadata; devdax gives a raw address space and shifts more policy to the application.
- **Raw versus sector mode:** raw mode minimizes translation; sector mode uses BTT metadata and work to preserve sector atomicity for block consumers.
- **`map=mem` versus `map=dev`:** system-memory page metadata preserves namespace capacity but consumes RAM; device-resident metadata scales with capacity but reduces usable PMEM.
- **Write-ahead logging versus copy-on-write:** logging can update in place with replay complexity; copy-on-write simplifies old-root preservation but adds allocation and write amplification.
- **Undo versus redo records:** undo permits rollback of in-place changes; redo preserves intended changes for replay and usually needs a separate commit decision.
- **Checksums versus replication:** checksums detect covered corruption; replication can restore data but introduces placement, ordering, quorum, and split-brain concerns.
- **Fine-grained flush versus batched persistence:** fine granularity lowers exposure and can raise instruction cost; batching amortizes barriers while enlarging the rollback window.
- **Library abstraction versus hand-coded instructions:** a maintained library adapts to platform capabilities; hand coding can specialize but expands portability and validation risk.
- **Direct mappings versus mediated operations:** mappings reduce crossings; mediation centralizes bounds checks, authorization, accounting, and error translation.
- **Local placement versus failure-domain diversity:** NUMA-local copies reduce access latency; separated replicas better tolerate socket, region, or device failure.
- **Synchronous repair versus degraded operation:** immediate repair simplifies state; degraded service can preserve availability but requires explicit poison isolation and redundancy.
- **Runtime firmware activation versus reboot:** runtime activation can reduce planned downtime but still requires quiescence and careful recovery; reboot offers a broader reset boundary.
- **Passphrase lock versus application encryption:** device security protects media under its threat model; application encryption can bind protection to data ownership but adds key and recovery complexity.
- **Emulation versus physical power-fail tests:** emulation gives deterministic crash-point coverage; physical testing exercises actual caches, firmware, power, and media behavior.

## Failure Modes and Misconceptions

- **“Persistent memory is just durable RAM.”** It also needs a persistence-domain and recovery contract.
- **“Byte addressable means byte atomic.”** Access granularity and power-fail atomicity are separate.
- **“Another thread saw the value, so it is persistent.”** Coherent visibility may precede persistence.
- **“A memory fence flushes caches.”** Ordering and writeback are distinct operations unless a documented primitive combines them.
- **“Cache-line writeback alone completes persistence.”** The required completion or ordering barrier may still be missing.
- **“Source-code order is persistence order.”** Compilers, CPUs, caches, and controllers can invalidate that inference.
- **“DAX means no filesystem.”** fsdax retains filesystem allocation and metadata even though data bypasses the page cache.
- **“DAX is always faster.”** Small accesses can benefit, while faults, flushes, NUMA distance, writes, and compatibility can dominate.
- **“`mmap` makes writes durable.”** Mapping establishes addressability, not a universal durability boundary.
- **“`MAP_SYNC` removes the need for CPU persistence operations.”** Its contract works in conjunction with appropriate instructions.
- **“`fsync` on a new file always persists its name.”** The containing directory can require separate synchronization.
- **“A checksum makes an update atomic.”** It detects some invalid states; a publication protocol chooses among them.
- **“The newest generation is always correct.”** It must first pass bounds, format, checksum, and commit validation.
- **“Persistent pointers can store virtual addresses.”** virtual placement is not stable across mappings or restart.
- **“A process lock protects crash recovery.”** volatile lock state disappears and can leave durable fields partially updated.
- **“BTT makes every transaction atomic.”** It provides its documented sector-update abstraction, not arbitrary multi-sector application atomicity.
- **“Device names are stable identities.”** discovery order can change; validate durable identifiers.
- **“Changing namespace mode is a reversible toggle.”** reconfiguration can destroy contents and metadata.
- **“Clearing poison restores the old bytes.”** it clears an error condition after repair or overwrite; lost content needs restoration.
- **“Persistent media is a backup.”** persistence does not defend against correlated hardware loss, bugs, attackers, or operator error.
- **“Deleting files sanitizes media.”** data can remain in unallocated or remapped locations.
- **“A virtual guest barrier proves host durability.”** durability cannot exceed the host backing and failure contract.
- **“Process-kill testing proves power-fail safety.”** it exercises a narrower failure boundary.
- **“One successful reboot proves recovery.”** crash points, interleavings, media faults, and platform states require systematic coverage.

## Worked Examples

### Example 1

An inventory reports two physical devices interleaved into region 0. Region 0 contains an fsdax namespace with UUID `A` and a devdax namespace with UUID `B`. The current nodes are `/dev/pmem0` and `/dev/dax0.1`.

An automation request names UUID `B`, expected mode `devdax`, expected size, and region membership. The tool refuses a supplied `/dev/dax0.0` path because its resolved UUID differs. This is correct: device-node position is observation, while durable identity plus expected attributes authorizes the target.

### Example 2

A 256 GiB namespace reserves 64 bytes of page metadata per 4 KiB page. The approximate metadata is

$$
\frac{256\times 2^{30}}{4096}\times 64 = 4\times 2^{30}\text{ bytes}=4\text{ GiB}.
$$

Device-resident metadata therefore leaves roughly 252 GiB before other alignment and label costs. An operator who promises a 256 GiB filesystem from nominal region capacity has omitted a material provisioning cost.

### Example 3

An application stores payload `new`, issues cache-line writeback for the payload, stores a commit word, and returns without a persistence barrier. Source order exists, but the platform has not established payload-before-commit persistence.

The corrected abstract sequence is populate payload, write back every dirty payload line, execute the required persistence barrier, publish and write back the commit word, then execute the required completion barrier before reporting durable success. The concrete primitives come from the supported platform API.

### Example 4

This runnable model simulates two slots after a crash. It deliberately models no real cache instruction:

<!-- bijux-verify: {"id":"persistent-dual-slot-recovery","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"slot version=1 value=10 committed=True valid=True\nslot version=2 value=20 committed=False valid=False\nrecovered version=1 value=10\n","stderr":""}} -->
```python
def checksum(version, value):
    return (version * 31 + value * 17) % 256


slots = [
    (1, 10, 201, True),
    (2, 20, 146, False),
]

for version, value, recorded, committed in slots:
    valid = committed and recorded == checksum(version, value)
    print(
        f"slot version={version} value={value} "
        f"committed={committed} valid={valid}"
    )

valid_slots = [
    item
    for item in slots
    if item[3] and item[2] == checksum(item[0], item[1])
]
chosen = max(valid_slots, key=lambda item: item[0])
print(f"recovered version={chosen[0]} value={chosen[1]}")
```

Expected output:

`slot version=1 value=10 committed=True valid=True`, then `slot version=2 value=20 committed=False valid=False`, then `recovered version=1 value=10`.

Version 2's payload and checksum agree, but recovery rejects it because publication did not complete. This establishes one logical selection rule only.

### Example 5

A service creates `state.next`, writes and synchronizes its contents, renames it to `state`, and crashes. On a filesystem whose contract requires directory synchronization for durable name changes, the content can be durable while the new name is not.

The protocol synchronizes the file, performs the atomic rename under the filesystem contract, and synchronizes the containing directory. If it also removes an old file, it accounts for the relevant directory metadata. PMEM media does not eliminate namespace durability.

### Example 6

A devdax application stores a persistent offset `o=4096` into a 1 MiB mapping. After corruption, recovery reads `o=2^{64}-16`. Adding an object length wraps machine arithmetic and appears small.

Safe recovery rejects the record before pointer formation: parse into a type that permits checked arithmetic, require alignment, require `o <= mapping_length`, require `length <= mapping_length - o`, validate the object header and checksum, and bound graph traversal.

### Example 7

A monitoring event identifies poison in a cache line belonging to replica 1. The application catches the supported fault path, marks replica 1 unavailable, reads and validates replica 2, quiesces writers, overwrites or replaces the damaged range through the platform repair workflow, clears the error indication, rewrites from replica 2, persists it, and revalidates.

Simply issuing `clear-errors` before capturing location and restoring content would lose forensic evidence and could expose unknown bytes as healthy data.

### Example 8

An administrator wants to convert namespace UUID `A` from fsdax to devdax. Preflight finds a mounted filesystem and two writable mappings. The operation refuses.

After application shutdown, unmount, mapping verification, backup and restore test, the operator records identity and label state, performs the destructive conversion, verifies UUID policy, size, alignment, NUMA node and device type, then initializes the application's devdax layout. The refusal was part of correctness, not inconvenience.

### Example 9

A benchmark compares buffered writes that acknowledge before `fsync` with DAX writes that flush and fence every record. DAX appears slower. The comparison measures different durability contracts.

A fair experiment compares acknowledged volatile operations with one another or acknowledged durable operations with one another. It records batching, record size, read/write ratio, NUMA placement, cache temperature, fault behavior, recovery time, and CPU consumption.

### Example 10

A guest maps virtual persistent memory backed by a host file. Guest recovery survives process restart and virtual-machine reboot, but a host power cut loses recent data because the backing stack acknowledged before stable storage.

The evidence proves guest-software crash consistency under the tested host behavior, not power-fail durability. The deployment either strengthens host synchronization and storage guarantees or weakens the advertised service contract.

## Cross-Program Connections

- **Computer architecture:** cache hierarchy, store buffers, writeback instructions, barriers, machine checks, memory controllers, ADR, eADR, and NUMA define the hardware side of persistence.
- **Data structures engineering:** logs, copy-on-write trees, dual roots, checksums, allocators, epochs, and bounded persistent references turn byte ranges into recoverable structures.
- **Database systems:** WAL, steal/no-steal policies, checkpoints, group commit, recovery idempotence, and transaction isolation generalize directly to PMEM designs.
- **Filesystem engineering:** extent allocation, DAX faults, inode state, rename, directory synchronization, truncate, hole punch, bad blocks, and repair remain active below mapped files.
- **Distributed systems:** local persistence is only one replica event; quorum, fencing, epochs, idempotence, and failure domains determine service durability.
- **Security engineering:** durable corruption, least-privilege mappings, encryption, key recovery, crash dumps, sanitization, and device transfer change the threat model.
- **Platform engineering:** inventory, maintenance gates, health monitoring, firmware rollout, topology-aware placement, backups, and incident evidence operationalize the kernel contract.
- **API and service engineering:** a durable acknowledgement must name its failure model; an API that returns success before its promised persistence boundary is semantically incorrect.
- **Formal methods:** crash-prefix reasoning, state-machine refinement, invariants, linearization points, and model checking help enumerate persistent states that testing might miss.
- **Performance engineering:** flush batching, fault cost, cache traffic, write amplification, recovery objectives, and semantic equivalence prevent invalid “faster storage” conclusions.

## References

1. Linux Kernel Documentation, [Non-Volatile Memory Device (NVDIMM)](https://docs.kernel.org/driver-api/nvdimm/index.html), subsystem documentation index; retrieved 2026-09-04.
2. Linux Kernel Documentation, [LIBNVDIMM: Non-Volatile Devices](https://docs.kernel.org/driver-api/nvdimm/nvdimm.html), firmware discovery, regions, namespaces, labels, and namespace abstractions; retrieved 2026-09-04.
3. Linux Kernel Documentation, [BTT - Block Translation Table](https://docs.kernel.org/driver-api/nvdimm/btt.html), atomic sector-update design over persistent memory; retrieved 2026-09-04.
4. Linux Kernel Documentation, [NVDIMM Security](https://docs.kernel.org/driver-api/nvdimm/security.html), device security states, key handling, erase, and overwrite interfaces; retrieved 2026-09-04.
5. Linux Kernel Documentation, [NVDIMM Runtime Firmware Activation](https://docs.kernel.org/driver-api/nvdimm/firmware-activate.html), activation states and quiescence; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Direct Access for files](https://docs.kernel.org/filesystems/dax.html), fsdax motivation, effective inode state, configuration, and limitations; retrieved 2026-09-04.
7. Linux Kernel Documentation, [Linux kernel memory barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), ordering concepts and persistent-memory barriers; retrieved 2026-09-04.
8. Linux man-pages, [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), shared mappings, `MAP_SHARED_VALIDATE`, and `MAP_SYNC`; retrieved 2026-09-04.
9. Linux man-pages, [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html), file data, metadata, device synchronization, and directory caveat; retrieved 2026-09-04.
10. NDCTL User Guide, [Managing Namespaces](https://docs.pmem.io/ndctl-user-guide/v68/managing-namespaces), namespace modes, capacity overhead, mode conversion, and destructive-change cautions; retrieved 2026-09-04.

## Exercises

### Exercise 1

A team updates a 128-byte record spanning two cache lines and then stores an eight-byte root pointer. Specify a failure-atomic copy-on-write protocol. State the persistence order, recovery validation, and at least four assumptions that must be documented.

### Exercise 2

Choose `fsdax`, `devdax`, `sector`, or buffered block access for each workload and justify the missing responsibilities: a legacy database requiring sector atomicity; a multi-tenant file service; a single-purpose persistent object store with its own allocator; and a workload dominated by reusable cached reads.

### Exercise 3

Design a safe fsdax-to-devdax namespace conversion runbook. Include target identity, preconditions, destructive authorization, evidence, postconditions, and rollback or restore behavior.

### Exercise 4

A DAX application receives a fault while reading persistent offset 8192. Monitoring reports a media error at the same address. Design containment and recovery for both a replicated and an unreplicated deployment. Explain why clearing the error is not recovery.

### Exercise 5

Design a validation campaign for a persistent queue. Cover crash-point enumeration, concurrency, corrupted metadata, power failure, process failure, kernel failure, virtualization, NUMA, performance, and the limits of the resulting evidence.

## Answers to the Exercises

### Answer 1

Allocate a new record at an unpublished, bounded persistent offset. Write its format, generation, length, payload, backward-compatible fields, and checksum while it is unreachable. Write back both cache lines and execute the required persistence barrier. Then write a new root slot containing the offset, generation, root checksum, and commit state; write back that slot and execute the required completion barrier before acknowledging durable success. Preserve the old root and record until the new root is known persistent and no supported recovery path needs the old generation.

Recovery reads both root slots without following their offsets immediately. It validates root format, commit state, checksum, generation comparison, offset alignment, and checked range bounds. It then validates the referenced record's format, generation, length, and checksum. It chooses the newest fully valid root under a defined wrap rule; if neither is valid, it enters an explicit restore or repair state.

Document at least: the platform persistence domain and covered failures; the atomic write granularity assumed for each root field or how torn roots are detected; the exact persistence API for the mapping and CPU; the namespace mode and filesystem contract; the checksum's corruption model; mapping alignment; version-wrap policy; concurrency synchronization; and whether device loss or only power loss is covered. Source order and a lock are insufficient.

### Answer 2

For the legacy database requiring sector atomicity, choose sector mode when it must run directly on PMEM as an ordinary block consumer and its safety genuinely depends on atomic sectors. BTT supplies that compatibility at metadata and write costs. Buffered block access is also reasonable if the broader stack already meets its tested durability needs. The database still owns transactions spanning sectors.

For the multi-tenant file service, choose a filesystem, usually buffered access unless measured workloads justify fsdax. The filesystem supplies names, permissions, quotas or accounting, allocation, and administrative tools. fsdax can remove copies but expands mapping, error, and compatibility responsibilities; tenant isolation remains mandatory.

For the single-purpose object store with its own persistent allocator and recovery format, devdax can be appropriate. The service must supply allocation, stable offsets, failure atomicity, access mediation, checksums, recovery, backups, mapping containment, and poison handling. It must also meet alignment and page-metadata constraints.

For reusable cached reads, buffered file access is a strong default because the page cache can absorb repeated reads and integrate with reclaim. DAX can be slower if the workload benefits from DRAM caching or suffers remote-media latency. Measure equivalent consistency and durability before changing modes.

### Answer 3

Resolve the requested namespace UUID to its current device, region, physical members, mode, size, alignment, NUMA node, filesystem, and owner. Compare all fields with the approved change record. Refuse on ambiguity. Inventory labels, health, bad blocks, firmware, security state, mount state, open descriptors, mappings, and pins.

Quiesce application writers, take an application-consistent backup, and perform a test restore to independent capacity. Unmount the filesystem and prove there are no live mappings or holders. Record the data-loss consequence of mode conversion and obtain explicit destructive authorization naming the UUID and expected topology.

Perform the supported disable and reconfiguration operation. Preserve command output under controlled access. Re-enumerate rather than assuming device names, then validate identity policy, new `devdax` mode, character device, size, alignment, permissions, NUMA placement, health, and absence of unexpected namespaces. Initialize a versioned application format, test persistence and recovery, and only then reopen service.

Rollback is restoration, not merely toggling the mode back: recreate the approved target mode and layout, restore the verified backup, validate application state, and record any identity change. If any precondition or validation fails, remain quiesced and preserve evidence.

### Answer 4

First stop repeated access to the affected range, capture the fault, stable namespace identity, physical mapping, offset, process and operation, health state, bad-block list, and recent mutations. Quiesce writers whose consistency protocol could involve the record. Do not let a generic signal retry loop touch the poisoned line again.

With replication, fence the damaged replica, select another replica only after validating its epoch, checksum, and application consistency, and continue in an explicitly degraded state if policy permits. Repair or replace the media range through the supported workflow, clear the hardware error only at the appropriate stage, rewrite from the good replica, persist, reread and validate, then rejoin under the replication protocol.

Without replication, isolate the object and determine whether a verified backup or higher-level reconstruction exists. Restore into known-good capacity and validate dependencies. If no source exists, report permanent data loss; inventing bytes would violate integrity. Service may continue only if the application has a defined unavailable-object state.

Clearing an error changes device or kernel error bookkeeping after a platform-specific overwrite or repair. It cannot reconstruct the former content, repair application references, select the right generation, or prove replicas agree. Recovery ends only when valid data and application invariants are restored.

### Answer 5

Model queue states such as empty slot, initialized unpublished record, data persisted, publication started, publication persisted, consumer claimed, consumer result persisted, reclamation pending, and reusable. Enumerate crashes before and after every writeback and barrier, plus during allocation, wrap, resize, checkpoint, recovery, and reclamation. Use an oracle that parses persistent bytes independently and checks bounds, checksums, generations, reachability, no duplicate delivery where promised, and no loss beyond the stated acknowledgement boundary.

Run concurrent producers and consumers with forced preemption and adversarial scheduling. Mutate lengths, offsets, checksums, versions, commit words, free lists, and graph edges; require bounded rejection rather than unsafe traversal. Inject media errors in data and metadata. Exercise process kill, kernel panic, warm reset, and controlled sudden power loss separately because each covers different volatile state. Repeat across supported CPUs, firmware, kernels, filesystems, namespace modes, alignments, and local and remote NUMA placement.

For virtualization, test guest restart, host process failure, host kernel failure, snapshot and migration, and actual backing-store power failure. Trace guest barriers through the host contract. For performance, measure equivalent durability semantics: throughput, latency percentiles, flush and barrier rate, cache misses, CPU, faults, recovery time, and capacity overhead.

Record seeds, crash point, platform inventory, raw logs, recovered image digest, oracle result, and environmental controls. Emulation establishes state-machine coverage; it does not prove physical persistence. Tests on one eADR platform do not prove ADR behavior, device-loss tolerance, untested filesystems, or application correctness beyond the oracle. State those limits with every result.
