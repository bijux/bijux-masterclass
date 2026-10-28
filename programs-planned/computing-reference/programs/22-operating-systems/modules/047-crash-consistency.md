---
module_id: OS-047
program: Operating Systems
level: 1
module_number: 47
title: Crash Consistency
status: complete
last_verified: 2026-09-04
---

# Crash Consistency

## One-Page Review

### Governing question

How can a filesystem and its applications guarantee meaningful recovered states when execution stops without warning after an arbitrary permitted subset and order of writes has become persistent?

### Essential definitions

- A **crash state** is the persistent state observable after abrupt failure and lower-layer effects.
- A **failure model** states which writes can be lost, reordered, torn, duplicated, or reported inaccurately.
- A **persistence dependency** requires one event to become durable before another may become durable.
- A **crash-consistency invariant** must hold in every recovered state allowed by the failure model and synchronization history.
- A **recovery procedure** transforms an admissible crash state into a mountable, specified state.
- A **durability point** is an API-visible event after which named effects must survive failures within the stated model.
- A **crash oracle** decides whether recovered state belongs to the set permitted by the specification.
- **Bounded crash testing** explores workloads and crash points within explicit limits rather than claiming exhaustive universal coverage.

### Central model, mechanism, or theorem

Let execution produce persistence events `E` with dependency relation `≺`. A legal crash cut `C subseteq E` is downward closed: if `b in C` and `a ≺ b`, then `a in C`, except where the failure model explicitly permits dependency violation. Recovery `R(C)` must terminate and produce a state satisfying filesystem invariants `Inv_FS` and the application-visible contract `Spec(H)`, where `H` records completed operations and synchronization points.

Correctness is quantified over all legal cuts, not only clean shutdown and one convenient write prefix. Journaling, copy-on-write roots, shadow paging, checksums, replicated metadata, and scanning are mechanisms for restricting or repairing cuts. None substitutes for a precise device model, end-to-end flush behavior, recovery idempotence, or application protocol.

### Critical invariants

- Every recovered namespace reference resolves to a valid object of the expected generation and type.
- Allocated storage has valid ownership, and no ordinary unit is simultaneously free or incompatibly owned elsewhere.
- Newly reachable content is initialized; recovery never reveals stale bytes from a prior owner.
- Committed journal records or published roots are accepted only after identity, sequence, bounds, checksum, and persistence validation.
- Recovery is bounded and safe to repeat after another crash.
- Successful synchronization preserves exactly the data and metadata named by its contract, including required directory state.
- Tests and proofs use the same explicit failure assumptions as the implementation and claimed deployment.

### Common failures

Common mistakes are assuming device completion means nonvolatile persistence, testing only prefix-ordered writes, treating sector writes as universally atomic, using `rename` as a durability primitive without synchronization, flushing a file but not its new directory entry, accepting any mountable state as correct, replaying non-idempotent procedures, using checksums as ordering proof, overlooking a crash during recovery, and claiming exhaustive assurance from a bounded workload generator.

### Compact example

A service writes `config.new`, synchronizes it, renames it over `config`, and synchronizes the parent directory. The data-before-rename and rename-before-directory-sync dependencies exclude a recovered name pointing to uninitialized content after the final success. Omitting the file sync can expose a new name with old or zero data; omitting the directory sync can lose the publication despite a successful file sync, depending on the filesystem contract.

### Connections

[OS-043](043-file-allocation.md) through [OS-046](046-journaling.md) provide mappings, ownership, caching, and log recovery. [OS-050](../ROADMAP.md) uses these invariants in complete filesystem design; later storage and distributed-systems work broadens the failure model.

## Governing Question

A crash does not politely occur between operations. It can happen during a metadata block write, after a device acknowledged volatile cache contents, halfway through recovery, or after an application observed success but before a containing directory was durable.

The governing question is which recovered states are permitted and how to exclude dangerous ones. The answer begins with explicit layers and persistence events, derives invariants for every legal crash cut, and verifies both recovery mechanism and application protocol.

## Why This Matters

Filesystems store the state on which executables, databases, configuration, identity, and audit trails depend. A locally atomic in-memory operation can leave several persistent structures disagreeing after power loss.

Structural mountability is not enough. A filesystem can recover a valid namespace while losing a supposedly durable file, exposing stale contents, or violating an application's replace protocol. Each claim needs a specification at the right layer.

Crashes are also hard to test. The state space combines workloads, write order, torn boundaries, cache flushes, allocation choices, concurrency, and recovery crashes. Bounded systematic exploration and formal reasoning complement—not replace—each other.

## Prerequisites and Retrieval

Review [OS-024](024-atomic-operations.md), [OS-037](037-copy-on-write.md), [OS-042](042-inodes-and-metadata.md), [OS-043](043-file-allocation.md), [OS-044](044-filesystem-free-space-management.md), [OS-045](045-buffer-cache-and-page-cache.md), and [OS-046](046-journaling.md).

Retrieve these distinctions:

- concurrency linearization and persistence ordering solve different problems;
- visibility, cache dirtiness, I/O submission, device completion, media persistence, and recovered observability are distinct;
- atomicity granularity belongs to a particular layer and alignment;
- a journal commit and copy-on-write root are meaningful only if their dependencies are stable first;
- metadata consistency, file-content durability, namespace durability, and application transaction semantics differ;
- `fsync`, `fdatasync`, directory sync, `syncfs`, and clean unmount have different scopes;
- fault injection needs a specification-derived oracle, not merely “mount succeeded”;
- a verified implementation inherits assumptions about hardware, compiler, runtime, and recovery environment.

## Learning Objectives

After this module, you should be able to:

1. define crash, storage, and recovery models using persistence events, dependencies, and legal cuts;
2. derive cross-structure invariants for namespaces, inodes, allocation, references, quotas, data initialization, and logs;
3. compare journaling, copy-on-write, shadow paging, log structuring, synchronous update, and scan-and-repair;
4. specify crash-safe create, replace, append, truncate, and delete protocols at filesystem and application layers;
5. construct idempotent bounded recovery with corruption and repeated-crash handling;
6. design trace capture, crash injection, state reconstruction, workload generation, and precise oracles;
7. evaluate empirical and formal assurance without overstating coverage.

## Core Exposition

### Failure layers

An application issues system calls, the filesystem mutates caches and metadata, the block layer schedules requests, controllers buffer them, and media records them. Virtualization, RAID, network storage, and replication add more layers.

Each boundary has acknowledgement and ordering semantics. A correct argument identifies the layer whose failure is modeled and the assumptions made about every lower layer.

### Clean shutdown versus crash

Clean shutdown stops new mutation, drains writeback, commits recovery state, flushes devices, and records a clean marker. A crash skips some or all of those steps.

Passing clean unmount tests exercises lifecycle code but says little about arbitrary persistence cuts. Crash recovery must not depend on shutdown having run.

### Volatile state

CPU caches, kernel memory, page cache, filesystem caches, device queues, and controller write-back caches can contain newer state than nonvolatile media. Different failures preserve different subsets.

A kernel panic with powered storage differs from total power loss. Test reports name the exact event rather than using “crash” as one universal condition.

### Persistence events

Model a write, flush, force-unit-access request, journal commit, or root publication as an event only at the layer where it changes recoverable state. Submission is not persistence.

Events carry range, payload version, device, atomicity unit, and completion semantics. Dependencies constrain which combinations can survive.

### Legal crash cuts

A crash cut selects events persistent before failure. Under a strict dependency graph, the set is downward closed; relaxed devices enlarge the allowed set.

Enumerating only source-code order is unsound when writes can reorder. Conversely, generating impossible cuts wastes testing and can produce false failures.

### Atomic-write assumptions

Storage can promise atomicity for aligned units under stated sizes, commands, and power-failure conditions. Larger writes may tear into independently persistent pieces.

Never infer atomic sectors from convention. Query capabilities where available, honor alignment and maximums, and retain checksums or redundant copies appropriate to the threat model.

### Reordering

Queues merge, split, and reorder writes for throughput. A later completion can precede earlier media persistence unless barriers or command semantics establish order.

Persistence graphs model required edges. The implementation issues flush or force-unit-access operations and verifies that every layer preserves them.

### Volatile device caches

A device may acknowledge data held only in volatile cache. A flush requests earlier writes reach nonvolatile storage; force-unit-access-like flags apply persistence semantics to a write.

Devices or virtual layers that falsely acknowledge these commands invalidate the proof. Power-cut tests and trusted specifications support the assumption.

### Torn writes

A multi-sector metadata block can contain a mixture of old and new bytes after failure. Checksums detect many tears; duplicated records with generations can select a complete copy.

Detection without a recoverable alternate can still mean data loss or mount refusal. The policy states whether corruption is repaired, quarantined, or fatal.

### Lost writes and misdirected writes

A completed write can be lost under a faulty layer, or land at the wrong address. End-to-end checksums incorporating owner and logical address help detect misdirection.

Crash consistency often assumes non-Byzantine storage. If lost or misdirected writes are in scope, redundancy and integrity metadata expand the design.

### Cross-structure invariants

A directory entry, inode, extent map, free-space map, reverse map, reference count, quota record, and checksum describe overlapping facts. Recovery must make them agree.

State that is individually well formed can still be globally corrupt. Bidirectional ownership checks find both leaks and cross-links.

### Data initialization

Before metadata makes newly allocated storage reachable, bytes must contain caller data or guaranteed zeros. Unwritten extents and ordered writes encode this dependency.

Publishing first can reveal a previous owner's contents even when the filesystem remains structurally mountable. This is a security invariant.

### Journaling

Write-ahead journaling records metadata images or intentions and commits them before dependent home reuse. Recovery replays valid committed work and rejects incomplete transactions.

The proof includes log space, sequence, revoke, checksum, checkpoint, and device-ordering rules. Journaling is one mechanism, not the definition of crash consistency.

### Copy-on-write trees

Copy-on-write constructs new data and metadata away from the current committed tree, then publishes a new root after dependencies become persistent. The old root remains a recovery fallback.

Root atomicity, generation, checksum, tree validation, allocator bootstrapping, and device flush order determine whether publication is trustworthy.

### Shadow paging

Shadow paging preserves old pages while writing replacements and atomically switches a root or page table. It resembles tree copy-on-write at a different abstraction.

Repeated small updates can amplify writes and fragment layout. Reclaim of old shadows occurs only after no recovery point needs them.

### Log-structured state

A log-structured filesystem appends new versions and reconstructs state from checkpoints plus later records. It avoids many in-place overwrites but still needs segment validity, sequence, checksums, and cleaner crash safety.

Cleaning relocates live data and updates ownership, creating its own persistence protocol. Append-only does not mean recovery-free.

### Soft updates and ordered dependencies

Dependency-tracking systems order metadata writes so no persistent pointer references uninitialized or free storage. Temporary leaks can be safer than cross-links and later repaired.

The dependency graph can be intricate under cycles and reuse. Correctness requires every write ordering to preserve the chosen invariants.

### Synchronous update

Writing each change to stable storage before returning simplifies some reasoning but cannot atomically update multiple sectors without a log, shadow, or stronger device primitive.

It also incurs high latency and can deadlock if metadata dependencies are ordered poorly. “Synchronous” describes timing, not necessarily transaction atomicity.

### Scan and repair

A checker traverses persistent structures and reconciles inconsistencies after an unclean state. It can recover from cases outside the normal log but costs time and may face ambiguous authority.

Repair conservatively quarantines uncertain blocks and records data loss. It does not silently invent which of two valid-looking owners was intended.

### Recovery specification

A recovery specification defines allowed post-recovery states for each durable history, not simply an algorithm. It covers data, metadata, return values, and synchronization boundaries.

For a completed unsynchronized write, several outcomes may be allowed. For a successfully synchronized file, the permitted set is narrower.

### Recovery idempotence

Recovery can itself crash. Repeating it from any intermediate persistent state must reach the same allowed result or another state from which progress resumes safely.

Physical after-images, set-to-value operations, generations, and durable intents support idempotence. Blind increments and remove-then-add procedures require guards.

### Recovery termination

Disk input is untrusted. Recovery bounds record counts, lengths, tree depths, allocation, retry, decompression, and total work.

Cycle detection and checked arithmetic prevent corrupt images from causing infinite loops or memory exhaustion. Refusing mount can be the safe result.

### Crash during mount

Journal replay or orphan processing can write storage even during a nominally read-only mount unless replay is disabled under specific rules. A second crash can interrupt those writes.

Recovery state or idempotent operations preserve restartability. Tests include every replay and cleanup persistence point.

### Create protocol

Creating a file changes inode allocation, initialized inode, directory entry, parent metadata, quota, and possibly data blocks. A filesystem transaction preserves structural dependencies.

An application requiring durable nonempty creation writes content, synchronizes the file, publishes the name as needed, and synchronizes the directory under the platform contract.

### Replace protocol

A common application pattern writes a candidate in the destination directory, applies metadata, synchronizes it, atomically renames it over the target, then synchronizes the parent.

Recovery should reveal the old complete version or the new complete version at the claimed point. Temporary files, multiple directories, and errors require explicit cleanup and sync scope.

### Append protocol

Appending changes data, size, mappings, checksums, and allocation. Concurrent append atomicity, write size, and persistence are separate properties.

Record-oriented applications add framing, length, checksum, and commit markers so recovery can reject a torn final record even when the filesystem preserves bytes as specified.

### Truncate protocol

Shrinking updates size, mapping trees, page cache, free space, reference counts, quota, and orphan or intent state. Publishing free space before removing all references risks double allocation.

Large truncates use bounded restartable work. Recovery preserves enough intent to finish without restoring removed tails or leaking blocks indefinitely.

### Delete protocol

Unlink removes a directory reference but open handles can retain the object. Durable deletion can require synchronizing the parent directory; physical sanitization is a different claim.

Crash recovery balances link counts, orphan state, open-independent persistence, allocation, and quotas. It never treats discard as proof of erasure.

### Rename semantics

Rename can be namespace-atomic within one filesystem, meaning lookup sees an old or new binding rather than a torn directory operation. That does not itself force the operation to survive power loss.

Replacement, exchange, cross-directory parents, and cross-filesystem moves have distinct contracts. Tests cover every affected directory and object.

### File synchronization

`fsync` requests persistence of a file's modified data and associated metadata under the platform contract; `fdatasync` can omit metadata unnecessary for later retrieval.

Errors from delayed allocation or writeback can surface here. Applications check the result and do not infer directory-entry durability from file synchronization alone.

### Directory synchronization

A new name, removal, or rename changes directory data and metadata. Synchronizing the file object need not persist that namespace mutation.

Application protocols open and synchronize each required parent directory. Unsupported directory synchronization is a portability constraint to address, not ignore.

### Filesystem-wide synchronization

`syncfs` targets dirty state for one filesystem and reports applicable writeback errors. Whole-system sync has broader scheduling and waiting semantics.

Neither creates a multi-file application transaction. It can establish a coarse durability boundary when its documented scope matches the requirement.

### Multi-device filesystems

Metadata and data can span devices with different queues, caches, atomicity, and failure. A flush on one device does not automatically order another.

Mirrors, parity, journals, and roots need cross-device commit and degraded-recovery rules. Partial device loss differs from simultaneous power failure.

### Virtualized and network storage

Guests depend on hypervisors, host caches, virtual controllers, network protocols, and remote stable-storage acknowledgments. Every layer must propagate flush and ordering truthfully.

Testing only an emulated device can miss host power-loss behavior. Record the full storage stack and failure injection boundary.

### Checksums and generations

Checksums detect selected corruption; generations distinguish old and new versions. Together they help recovery select a complete current record.

They do not prove a record was persisted in the required order or that semantically related structures agree. Cross-structure validation remains necessary.

### Application-level checksums

Applications can frame records with version, length, checksum, and commit state to recognize incomplete tails. This complements the filesystem contract.

An application checksum cannot recover bytes the filesystem was never required to persist. Redundancy or regeneration handles detected loss.

### Workload history

The oracle needs completed operations, failed operations, synchronization successes and failures, open handles, and known ordering. Return values constrain which recovered outcomes are legal.

Ignoring error returns makes the expected state ambiguous. Trace capture happens at the semantic interface and lower persistence layer.

### Crash injection

Tests record or control writes, flushes, and completion, then cut execution at selected persistence points. A reconstructed image represents the chosen legal cut rather than a normal shutdown.

Kernel panic, process kill, virtual power loss, device fault, and physical power cut test different models. Name the mechanism and its blind spots.

### Bounded black-box testing

Systematic generators enumerate short workloads, operation arguments, synchronization placements, and crash points within declared bounds. Small sequences can expose complex implementation bugs.

Bounded exploration is not proof beyond its operations, lengths, initial state, concurrency, filesystem, and failure model. Coverage metadata is part of the result.

### Crash oracle

An oracle checks more than successful mount. It compares names, content, metadata, links, allocation, and permitted old-or-new outcomes against the durable history.

The oracle avoids overconstraint: unsynchronized state may legally vary. It also avoids underconstraint: a mountable but supposedly durable missing file is a failure.

### Model-based testing

A small reference model executes application operations and tracks allowed persistent states after each sync boundary. Generated filesystem images are compared to that set after recovery.

Nondeterminism, timestamps, allocation, and filesystem-specific guarantees are normalized only when the specification permits it.

### Formal crash reasoning

Crash-aware logics specify normal and crash postconditions for operations and recovery. Machine-checked proofs can quantify over repeated crashes under a formal disk model.

Assumptions and trusted code remain visible: hardware atomicity, compiler, extraction, runtime, drivers, and specification adequacy. Verification does not eliminate empirical integration tests.

### Differential testing

Running one workload across filesystems can reveal differing outcomes, but difference is not automatically a bug because contracts differ. Compare each outcome to its declared specification.

Version, mount mode, block size, device model, and feature set are controlled. A consensus among implementations is not a correctness oracle.

### Observability and evidence

Record application calls and results, persistence events, ranges, payload hashes, dependency edges, flushes, device completions, crash cut, reconstructed image, recovery writes, recovered state, oracle decision, and limitations.

Preserve kernel, filesystem, mount, hardware or emulator, cache settings, workload seed, model version, raw traces, and disk images so another reviewer can reproduce the claim.

### Security and assurance

Adversarial tests target stale-data disclosure, cross-links, rollback, forged checksums, malformed logs, replay bombs, resource exhaustion, recovery privilege, sanitization claims, and device lies.

Assurance names filesystem, storage, VM, application, recovery, security, formal-methods, testing, and independent-verification reviewers. Absence of observed failures within a bound is not certification.

## Definitions and Notation

Let `E={e_1,...,e_n}` be persistence events with partial order `≺`, and let legal crash cut `C subseteq E` be downward closed: `b in C and a ≺ b implies a in C`. Let `P(C)` reconstruct the persistent bytes produced by cut `C` under the atomicity model.

Let recovery function `R` map a crash image to recovered state, possibly producing additional persistence events. Let history `H` contain operation invocations, results, and successful synchronization points. `Allowed(H,F)` is the set of application-visible states permitted under failure model `F`.

Crash consistency requires, for every legal `C`, termination or safe refusal and `R(P(C)) in Allowed(H,F)` while satisfying structural invariants `Inv_FS`. Repeated-crash safety quantifies over cuts during `R` as well.

A test bound `B=(operations,sequence_length,arguments,initial_states,concurrency,cuts,failures)` describes explored space. Passing every case in `B` proves only absence of oracle-detected violations within `B` under its model.

## Mechanisms, Invariants, or Proof Structure

1. **Declare the failure model.** Name layers, atomicity units, reorder, volatile caches, flush behavior, device loss, corruption, and crash-during-recovery assumptions.
2. **Specify allowed outcomes.** Tie namespace, content, metadata, ownership, and errors to completed operations and successful synchronization points.
3. **Derive persistence edges.** Order initialization before reachability, log or new trees before commit, owner removal before free reuse, and file state before durable publication.
4. **Implement a recovery mechanism.** Use validated journals, roots, intents, generations, checksums, replicas, or scans that realize the specified cuts.
5. **Bound recovery.** Validate every disk-controlled length, address, feature, tree, record, allocation, and retry before use.
6. **Make recovery repeatable.** Ensure every replay, orphan, cleaner, and repair transition is idempotent or guarded by durable progress.
7. **Propagate errors.** Preserve writeback, allocation, checksum, flush, device, and recovery failures through the entitled API and operational state.
8. **Compose application protocols.** Use opened handles, file sync, atomic namespace operations, directory sync, framing, and cleanup matching the requirement.
9. **Generate legal crash states.** Capture actual persistence events and dependencies; inject cuts without adding clean-shutdown behavior.
10. **Apply a precise oracle.** Accept all specified nondeterminism but reject lost durable effects, stale disclosure, structural inconsistency, and forbidden mixtures.
11. **Triangulate assurance.** Combine bounded testing, fuzzing, model checking, proofs, device fault tests, and independent review with explicit coverage.
12. **Preserve evidence.** Retain histories, traces, cuts, images, recovery writes, oracle versions, outcomes, environments, and limitations.

<!-- bijux-verify: {"id":"persistence-cut-enumeration","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events=data,rename,dirsync dependencies=data<rename;rename<dirsync\nlegal-cuts=4\ncut=none outcome=old\ncut=data outcome=old\ncut=data+rename outcome=new-visible-not-guaranteed\ncut=data+rename+dirsync outcome=new-durable\n","stderr":""}} -->
```python
events = ("data", "rename", "dirsync")
dependencies = {"rename": {"data"}, "dirsync": {"rename"}}


def legal(cut: set[str]) -> bool:
    return all(required <= cut for event, required in dependencies.items() if event in cut)


cuts = []
for mask in range(1 << len(events)):
    cut = {event for index, event in enumerate(events) if mask & (1 << index)}
    if legal(cut):
        cuts.append(cut)

print("events=data,rename,dirsync dependencies=data<rename;rename<dirsync")
print(f"legal-cuts={len(cuts)}")
for cut in cuts:
    label = "+".join(event for event in events if event in cut) or "none"
    if "dirsync" in cut:
        outcome = "new-durable"
    elif "rename" in cut:
        outcome = "new-visible-not-guaranteed"
    else:
        outcome = "old"
    print(f"cut={label} outcome={outcome}")
```

The executable model enumerates downward-closed cuts for one simplified dependency chain. It omits real files, system calls, device behavior, concurrency, errors, recovery writes, and filesystem-specific guarantees.

## Alternatives and Trade-Offs

- Write-ahead journaling limits recovery scanning but adds log writes, finite credits, checkpoints, and replay complexity.
- Copy-on-write trees retain old roots and avoid many in-place tears but amplify writes and complicate allocation and reclamation.
- Logical logs are compact but version-coupled; physical after-images are larger but simpler to replay.
- Full data journaling strengthens coupling at high bandwidth cost; ordered metadata modes reduce writes with narrower content guarantees.
- Synchronous updates narrow volatile windows but add latency and cannot alone atomically change multiple units.
- Scan-and-repair handles broader damage but costs downtime and can face ambiguous ownership.
- Strong device flushes simplify ordering but cost latency; batching amortizes them while enlarging loss windows.
- Fine-grained application sync minimizes unrelated I/O but is easy to omit; coarse filesystem sync is simpler and costlier without adding application atomicity.
- Bounded black-box testing finds real implementation faults without source changes but cannot prove behavior outside its bound.
- Formal verification quantifies over a model but depends on specifications and trusted assumptions; physical fault tests cover integration but sample states.
- Redundant checksummed metadata improves detection and selection but consumes space and can share common-mode failures.
- Conservative recovery avoids corruption by refusing mount or quarantining space but reduces availability.

## Failure Modes and Misconceptions

- **“Completed I/O is durable.”** Volatile caches and intermediate layers can acknowledge before nonvolatile persistence.
- **“Crash state is a source-order prefix.”** Reordering and tearing can create other legal subsets.
- **“Sectors are always atomic.”** Atomicity is capability-, size-, alignment-, command-, and failure-specific.
- **“Journaling solves every crash problem.”** Data mode, device ordering, application scope, and replay correctness remain.
- **“Checksums enforce ordering.”** They detect selected corruption but do not make dependencies persist first.
- **“Mountable means correct.”** Durable application data can be missing or stale in a structurally valid filesystem.
- **“Rename makes replacement durable.”** Atomic namespace visibility differs from post-crash persistence.
- **“File sync persists the containing name.”** Directory synchronization can be separately required.
- **“Recovery runs only once.”** Another crash can interrupt replay, orphan cleanup, or repair.
- **“A procedure is idempotent because its result is.”** Remove-then-add sequences can fail differently when replayed.
- **“More fault injection automatically improves assurance.”** Illegal cuts and weak oracles produce noise or false confidence.
- **“Different filesystems should recover identically.”** Their documented contracts and modes can permit different states.
- **“A verified filesystem needs no hardware testing.”** Proof assumptions may not match drivers, devices, or integration.
- **“No failures found means crash safety is proved.”** Empirical coverage is bounded by workloads, states, cuts, and oracle.

## Worked Examples

### Example 1

A block allocation bitmap reaches storage before the inode extent that owns it. Recovery sees a leak; the inverse order could expose a block still marked free and is more dangerous.

### Example 2

A metadata block write tears across sectors. Its checksum fails, so recovery selects a valid older generation or refuses mount instead of trusting mixed bytes.

### Example 3

A journal payload is acknowledged only in a volatile device cache, but the commit persists. Replay lacks truthful inputs, demonstrating a broken flush chain.

### Example 4

A copy-on-write filesystem writes new leaves and internal nodes, flushes them, then publishes a checksummed root. A crash before root publication selects the old complete tree.

### Example 5

A service synchronizes a candidate file and renames it but omits parent sync. The live process sees the new name, yet its required post-crash publication remains unproven.

### Example 6

An append consists of payload, length, checksum, and commit marker. Recovery ignores a torn final frame while preserving all prior committed frames.

### Example 7

A crash interrupts orphan cleanup after some extents are freed. Durable progress and idempotent ownership checks let the next mount resume without freeing them twice.

### Example 8

A black-box tester enumerates all sequences of up to three operations from create, write, rename, unlink, and sync, then reconstructs each captured persistence cut and applies a content-aware oracle.

### Example 9

A filesystem and thin-provisioning pool both buffer writes. Guest flush reaches the virtual device but is not propagated to the pool, invalidating the guest's recovery assumption.

### Example 10

A machine-checked filesystem proof assumes atomic disk blocks and correct flushes. Power-cut testing targets those trusted assumptions while the proof covers all modeled crash sequences.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) connects logs, commit records, checkpoints, recovery, record framing, and application transactions. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects caches, write ordering, persistence domains, atomic units, controllers, and media.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies failure models, hazard analysis, traceability, fault injection, and assurance cases. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) extends crash recovery to replicas, epochs, quorum persistence, and uncertain outcomes.

Within this program, [OS-043](043-file-allocation.md) through [OS-046](046-journaling.md) supply the affected structures and mechanisms; [OS-050](../ROADMAP.md) combines them into an end-to-end filesystem design.

## References

- Linux kernel documentation, [ext4 Journal (jbd2)](https://docs.kernel.org/filesystems/ext4/journal.html), current page checked 2026-09-04. Commit ordering, data modes, checksums, revokes, fast commits, idempotent replay, and checkpoints.
- Linux kernel documentation, [Explicit volatile write-back cache control](https://docs.kernel.org/block/writeback_cache_control.html), current page checked 2026-09-04. Device volatile caches, flushes, force unit access, ordering, and filesystem persistence obligations.
- Linux kernel documentation, [ext4 General Information](https://docs.kernel.org/admin-guide/ext4.html), current page checked 2026-09-04. Recovery, data journaling modes, barriers, commit intervals, error policy, delayed allocation, and mount semantics.
- Linux kernel documentation, [ext4 Orphan File](https://docs.kernel.org/filesystems/ext4/orphan.html), current page checked 2026-09-04. Recovering unlinked and truncating inodes, journaled orphan updates, checksums, and bounded block layout.
- Linux man-pages project, [fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html), current page checked 2026-09-04. File data and metadata synchronization, device completion, delayed errors, and separate directory synchronization.
- Linux man-pages project, [sync(2) and syncfs(2)](https://man7.org/linux/man-pages/man2/sync.2.html), current page checked 2026-09-04. System-wide and filesystem-scoped dirty-state synchronization and error reporting.
- Linux man-pages project, [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html), current page checked 2026-09-04. Namespace replacement atomicity, exchange, no-replace, cross-filesystem limits, open-object behavior, and failures.
- Mohan et al., [Finding Crash-Consistency Bugs with Bounded Black-Box Crash Testing](https://arxiv.org/abs/1810.02904), OSDI 2018 paper checked 2026-09-04. Bounded workload generation, persistence-state reconstruction, oracles, coverage, and discovered filesystem faults.
- Chen et al., [FSCQ: A Formally Certified Crash-Proof File System](https://css.csail.mit.edu/fscq/), project and peer-reviewed publications checked 2026-09-04. Crash Hoare Logic, machine-checked recovery specifications, repeated crashes, implementation extraction, and trusted assumptions.
- Chajed et al., [Verifying a High-Performance Crash-Safe File System Using a Tree Specification](https://www.chajed.io/papers/dfscq%3Asosp2017.pdf), SOSP 2017 paper checked 2026-09-04. Tree-based specification, verified crash safety, logging, recovery, application sync behavior, and proof boundaries.

## Exercises

### Exercise 1

Define failure and persistence models for a local filesystem above a volatile-cache device. Derive legal crash cuts for a logged metadata transaction.

### Exercise 2

Specify crash-safe application protocols for create, atomic replace, append, and delete. State every successful return and synchronization dependency.

### Exercise 3

Compare journaling, copy-on-write roots, synchronous update, and scan-and-repair for atomicity, performance, recovery, and corruption.

### Exercise 4

Design bounded black-box crash testing with trace capture, workload generation, image reconstruction, recovery crashes, and a specification-derived oracle.

### Exercise 5

Build an assurance case combining model reasoning, formal proof, fault injection, physical power cuts, evidence, limitations, and reviewers.

## Answers to the Exercises

### Answer 1

Model kernel memory and device cache as volatile under power loss; define aligned atomic-write units and permit independent persistence of larger request fragments. A completed ordinary write need not be nonvolatile. A successful flush orders all prior applicable writes before its completion, and force-unit-access writes are durable on completion, assuming truthful propagation through every layer. Corruption or device loss is outside the basic model and added as a separate extension.

For a journal transaction define events for ordered file data, descriptors, payloads, revokes, precommit flush, commit record, commit persistence, home checkpoint writes, and tail advance. Add edges from all recovery inputs and ordered data to commit and from checkpoint completion to tail reuse. Enumerate downward-closed cuts including torn units allowed by the model. Recovery discards incomplete transactions, replays valid committed images with revokes, and never scans beyond validated geometry or sequences.

### Answer 2

For durable create, create under the intended parent, write and validate content, set required metadata, synchronize the file, then synchronize the parent directory. For replace, build a candidate in the destination directory, synchronize it, rename atomically over the target, and synchronize the parent; if two parents change, include both according to the platform contract. Check every call and preserve old or new complete recovery outcomes.

For append, use one-writer or documented concurrent-append semantics and frame records with version, length, checksum, and commit indication; synchronize at required transaction boundaries. Recovery discards an incomplete tail. For durable delete, unlink and synchronize the parent while respecting open-reference lifetime; do not claim physical sanitization. Each protocol specifies cleanup after partial failure and does not turn multiple independent files into one transaction without another coordination mechanism.

### Answer 3

Journaling writes recovery records before home changes and offers bounded replay, group commit, and selectable data coupling, but adds log bandwidth, credits, checkpoint pressure, and revoke complexity. Copy-on-write builds new trees and atomically publishes a root, retaining an old fallback, but adds write amplification, allocator bootstrapping, and delayed reclamation. Synchronous updates reduce volatile windows but cannot atomically cover several units and impose latency. Scan-and-repair needs less normal-path metadata but makes recovery slow and potentially ambiguous.

Compare each under the same torn-write, reorder, cache, corruption, and repeated-crash model. Evaluate write amplification, flushes, latency, throughput, maximum loss window, recovery time, stale-data prevention, space pressure, repair authority, implementation complexity, and application-visible sync contract. Hybrids are common and inherit every mechanism's composition obligations.

### Answer 4

Define a bound over initial filesystem images, operation alphabet, sequence length, names, sizes, offsets, synchronization placement, concurrency, allocation states, persistence cuts, and failures. Generate workloads, record calls and returns plus lower-layer writes and flushes, and reconstruct each legal cut without clean shutdown. Boot recovery under instrumentation, optionally cut every recovery write, and repeat until stable or safely refused.

The reference model derives allowed names, contents, metadata, and old-or-new outcomes from successful synchronization history. The oracle checks mount outcome, structural invariants, stale-byte absence, ownership, links, and application content while accepting specified nondeterminism. Deduplicate equivalent states but retain coverage maps. Preserve workload, seed, trace, cut, image, environment, recovery writes, oracle version, raw result, and exact bound; report passing only within that scope.

### Answer 5

State requirements and an explicit failure model, then derive cross-structure and application invariants plus persistence dependencies. Use model checking for finite protocol states, machine-checked proof for implementation components and repeated recovery under its disk model, fuzzing for malformed images, bounded crash testing for syscall sequences, block-layer fault injection for reorder and I/O errors, and physical power cuts for controller and media assumptions.

Trace every claim to evidence and identify trusted hardware, firmware, hypervisor, drivers, compiler, proof kernel, specifications, test oracle, and operational settings. Independently reproduce representative failures and recovery. Record unmodeled corruption, concurrency, scale, wear, device loss, and distributed layers as limitations rather than implied coverage. Named filesystem, storage, VM, application, recovery, security, formal-methods, testing, operations, and independent-verification reviewers approve their boundaries and residual risks.
