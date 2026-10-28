---
module_id: OS-007
program: Operating Systems
level: 1
module_number: 7
title: Kernel Data Structures
status: complete
last_verified: 2026-09-04
---

# Kernel Data Structures

## One-Page Review

### Governing question

How should a kernel represent objects and relationships when operations must remain correct under interrupts, multiple CPUs, constrained allocation, hostile identifiers, and concurrent object destruction?

### Essential definitions

- An **intrusive data structure** embeds linkage inside the represented object, avoiding a separate wrapper allocation and permitting one object to participate in several structures through distinct link fields.
- An **index** maps a key, identifier, address, or range to an object; its lookup semantics do not by themselves define object lifetime.
- A **sentinel** is a distinguished node or value that simplifies boundary cases, such as a circular list head representing both collection identity and the empty state.
- A **reference count** records outstanding ownership claims under a defined acquisition and release protocol; it is not a substitute for preventing new references during teardown.
- **Read-copy update (RCU)** separates removal from reclamation so readers that began before removal can finish before memory is reused.
- A **per-CPU structure** provides CPU-local instances to reduce shared writes, with explicit aggregation, migration, and CPU-lifecycle semantics.
- An **invariant checker** traverses internal state to detect corruption or impossible relationships; it samples declared properties rather than proving all executions safe.

### Central model, mechanism, or theorem

Choose a kernel structure from the full contract, not asymptotic lookup alone:

`choice = operations × key/range semantics × concurrency × lifetime × context × locality × failure policy`.

A structure is correct only when its representation invariant, synchronization protocol, and reclamation protocol hold together. Removing a node from a list makes it unreachable through that list; it does not prove that concurrent readers dropped pointers. Finding an object by integer ID does not prove that the ID still denotes the same generation. A fast lookup without a lifetime acquisition is an unsafe lookup.

### Critical invariants

- Every linkage field belongs to exactly the intended structure state: unlinked, linked once in that structure, or explicitly transient under its lock.
- Ordering, balancing, hashing, range, and queue invariants are updated atomically from each observer's permitted perspective.
- Lookup and lifetime acquisition compose so a returned object cannot be reclaimed before use.
- Deletion blocks new ownership, removes reachability, waits for or accounts for prior readers, then reclaims exactly once.
- Interrupt and nonblocking contexts use only operations and allocation modes valid there.
- Per-CPU data is accessed under migration and CPU-hotplug rules, and aggregation tolerates concurrent updates as documented.
- Debug traversal and observability do not silently violate locking, lifetime, or latency constraints.

### Common failures

Common mistakes are choosing linked lists by familiarity despite poor locality, embedding one link in two lists, deleting during unsafe iteration, returning an indexed pointer without a reference, assuming reference count zero can race safely with lookup, freeing immediately after RCU removal, treating per-CPU as per-thread, trusting user-chosen hash keys, wrapping ring indexes incorrectly, and adding invariant scans to latency-critical paths.

### Compact example

A kernel tracks live devices in an ID-indexed structure and also links each device into a bus list. Lookup by ID occurs under an RCU read-side section, validates the device generation and “live” state, and conditionally acquires a reference. Removal first prevents new references, removes the device from both indexes under their update protocols, waits for prior RCU readers, drains outstanding references, then frees memory. The ID can later be reused only with a new generation, so a stale `(id, generation)` handle fails rather than naming the replacement.

### Connections

[OS-006](006-boot-process-and-kernel-initialization.md) establishes the initialized memory and concurrency environment. [OS-008](../ROADMAP.md) develops allocation and reclamation, [OS-021](../ROADMAP.md) develops kernel critical sections, and [OS-054](../ROADMAP.md) develops RCU. General structure theory belongs to [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md); memory ordering belongs to [Computer Architecture](../../23-computer-architecture/ROADMAP.md).

## Governing Question

Kernels represent processes, virtual-memory areas, timers, pages, file descriptors, mounts, sockets, routes, devices, waiters, interrupts, and credentials. These objects are accessed from system calls, interrupt handlers, worker threads, and other CPUs. They can disappear while a lookup is in progress. Some paths cannot sleep or allocate freely. A corrupt link can redirect privileged memory writes.

Textbook complexity is necessary but insufficient. An array provides excellent locality but may require a bounded dense key. A list supports constant-time insertion with a known location but linear search and pointer chasing. A balanced tree supplies ordered lookup; a range tree must additionally encode gaps and overlaps. A hash table needs collision and adversarial-load policy. A lockless queue needs a memory-order proof and safe reclamation.

The governing question is how to select and implement the entire representation, synchronization, ownership, and evidence contract for the kernel context that will use it.

## Why This Matters

Data structures concentrate kernel invariants. One process object can be in a global task list, scheduler run queue, parent-child relation, identifier map, signal state, and wait queue. Each membership has distinct locks and lifetime. Reusing the same link field or acquiring locks in inconsistent order can corrupt unrelated subsystems or deadlock the machine.

Performance is often dominated by memory behavior rather than big-O notation. Pointer-rich structures miss caches and prefetch poorly. Shared root nodes and global counters bounce cache lines among CPUs. A theoretically worse per-CPU scan can outperform a contended global tree for the actual update/read ratio.

Security also depends on representation. User-influenced hash keys can trigger collision attacks. Integer overflow can make a circular-buffer full check wrong. A stale ID can acquire authority over a newly allocated object. Debug printers can dereference freed memory or hold locks for unbounded time. Structure design belongs in the kernel threat and reliability model.

## Prerequisites and Retrieval

Recall from [OS-004](004-interrupts-and-exceptions.md) that hard-interrupt context cannot sleep and that local interrupt masking is not an SMP lock. Recall from [OS-006](006-boot-process-and-kernel-initialization.md) that publication and CPU release require ordering. You should understand arrays, linked lists, queues, heaps, search trees, hash tables, graphs, amortized analysis, caches, atomics, locks, and virtual memory.

Retrieve these distinctions:

- reachability through a container is not object ownership;
- deletion from an index is not memory reclamation;
- logical identity is not a raw address or immediately reusable integer;
- atomic pointer access does not publish initialized pointee state by itself;
- a read-mostly workload is not a read-only workload;
- average-case hashing is not an adversarial bound;
- structural validation and functional validation answer different questions.

## Learning Objectives

After completing this module, you should be able to:

- derive structure requirements from operations, keys, contexts, concurrency, lifetime, and locality;
- explain intrusive lists and the obligations of multiple memberships;
- choose among arrays, bitmaps, lists, queues, heaps, hash tables, ordered trees, and range indexes;
- distinguish lookup synchronization from lifetime acquisition;
- design insertion, removal, reference, RCU, and reclamation state transitions;
- reason about ring-buffer wrap and publication ordering;
- explain per-CPU benefits and aggregation, migration, and hotplug costs;
- identify adversarial keys, stale handles, corrupt links, and debug-path hazards;
- design invariant checks, stress tests, and representative benchmarks;
- identify safety or security claims requiring accountable human review.

## Core Exposition

### Start with the operation contract

List required operations and their frequency: lookup by exact ID, predecessor or successor, containing range, minimum deadline, FIFO removal, insertion, deletion, iteration, bulk drain, snapshot, and aggregation. State worst credible population and whether it is dense, sparse, ordered, or range-based. Specify which paths are latency critical.

Then add execution context. May the operation sleep? May it allocate? Can an interrupt nest it? Can several CPUs call it? Are readers allowed stale results? Must iteration be a consistent snapshot? Can a callback reenter the subsystem? These questions can eliminate otherwise attractive structures.

Finally state lifetime and failure. Who owns each object before insertion, while reachable, after removal, and during callbacks? What happens on allocation failure or duplicate keys? Are identifiers attacker chosen? Must corruption trigger containment, warning, repair, or fail-stop? The resulting contract guides the structure and API.

### Arrays, bitmaps, and direct indexing

Arrays are powerful when keys are bounded and reasonably dense. They provide predictable address calculation, compact metadata, and cache locality. Kernel tables for fixed resources, small descriptors, CPU masks, and state vectors often benefit. The cost is resizing, unused capacity, and careful bounds arithmetic.

A bitmap represents boolean membership compactly and supports word-at-a-time search and set operations. Atomic bit operations can coordinate state, but a bit rarely carries ownership by itself. The protocol must define whether set means reserved, initialized, visible, or merely pending, and which memory ordering connects the bit to associated data.

Direct indexes must reject out-of-range and overflowed keys before address calculation. Speculative execution and information exposure may add requirements beyond architectural bounds checks. A pointer loaded from a slot needs a lifetime protocol even if the slot access itself is atomic.

### Intrusive lists

An intrusive list embeds `next` and `prev` linkage, or an implementation-defined link object, in the payload. A generic implementation can recover the enclosing object from the member. No wrapper allocation is required, and deletion is constant time when the node is known.

Each logical membership needs a separate link field. A process can have one link for the global process collection and another for a parent's child collection. Placing the same link in both splices the structures together. Initialization, insertion, deletion, reinitialization, and poison or debug states must be defined.

Lists are excellent for ordered traversal, queues with known nodes, and bulk splicing. They are poor search indexes and often have weak cache locality. Linux's own documentation warns that an array may be preferable. “Insertion is constant time” omits the cost of finding the insertion point and synchronizing it.

Deleting while iterating requires an iterator that saves the next link before removal or a protocol such as RCU. A “safe iteration” macro may protect cursor mechanics but not concurrent access or object lifetime; its exact guarantee must be read, not guessed from its name.

### Queues, rings, and heaps

FIFO queues represent arrival order and work ownership. A linked queue handles variable population; a bounded ring uses a fixed array and producer/consumer indexes for locality and allocation-free operation. Full and empty states need unambiguous representation through a reserved slot, separate count, or monotonically increasing sequence numbers.

Unsigned wrap can be intentional if capacity and difference comparisons satisfy proven bounds. Masking an index requires power-of-two capacity. Producers publish payload before making a slot visible; consumers observe visibility before reading payload. On multiple producers or consumers, reservation and publication may be separate states.

A heap efficiently selects the minimum or maximum priority, deadline, or cost and stores densely. Arbitrary deletion requires an object-to-index mapping or search. Updating a key must restore heap order. Equal-key tie behavior matters for scheduler fairness and timer determinism.

### Hash tables and adversarial keys

Hash tables provide expected constant-time exact lookup when distribution and load remain controlled. Kernel use adds hostile keys, bounded memory, nonblocking context, resize coordination, and object lifetime. Hash functions may require keyed randomization when callers can construct collisions.

Separate chaining integrates naturally with intrusive nodes but pointer chasing hurts locality. Open addressing stores entries compactly but needs tombstone, clustering, resizing, and concurrent-probe rules. A fixed table avoids resize complexity but must define behavior at saturation. Resizing changes which table readers consult and therefore participates in synchronization and reclamation.

Never use a raw bucket lookup as authorization. Compare the full key, validate namespace or generation, confirm live state, and acquire object ownership. Hash equality narrows candidates; it does not establish identity.

### Ordered and range trees

Balanced search trees support ordered lookup, predecessor, successor, and traversal. Linux red-black trees embed nodes in objects and leave comparison and locking to users. Rotations preserve ordering while changing links, so readers need a synchronization model that prevents observation of invalid transient state.

Range indexes answer containment, overlap, gap, and next-range queries. Virtual memory needs these semantics rather than only exact keys. The structure must define endpoint convention, overflow behavior, overlap policy, and mutation visibility. Cache-aware multiway nodes can outperform binary trees by reducing depth and pointer misses.

Linux's XArray indexes objects by unsigned integers and includes its own API and locking expectations. Maple Tree is designed for non-overlapping ranges and is used for virtual-memory areas. These names are examples, not interchangeable containers; their permitted stored values, allocation modes, cursor rules, and RCU interactions differ.

### Identifier allocation and stale handles

An ID allocator finds unused integers; an ID map associates them with objects. Dense cyclic allocation, maximum limits, reservation, and allocation context affect the choice. Exposing IDs to user space or devices turns reuse into a security and correctness concern.

Suppose object A uses ID 7, a client caches 7, A is deleted, and object B receives 7. A late operation can target B. Pairing an index with a generation or using an unguessable capability reduces accidental aliasing, but wrap and validation policy still matter. The subsystem must also block new lookups while teardown drains old references.

An index does not own its entries unless the API explicitly says so. Decide whether insertion transfers a reference, removal returns one, and lookup acquires one. Error paths must restore both ID availability and object ownership exactly once.

### Per-CPU structures

Per-CPU counters, queues, caches, and statistics turn shared writes into CPU-local writes. This reduces cache-line contention and can make interrupt-context access allocation-free. Access is safe only when the executing thread cannot migrate between selecting and using its CPU instance, or the API handles migration.

Aggregation reads several instances that may change concurrently. The result may be approximate unless updates are stopped or a snapshot protocol exists. CPU hotplug must initialize a new instance, drain or transfer an outgoing instance, and ensure no late access after removal.

Per-CPU state trades fast local operations for memory proportional to CPU count, uneven capacity, and expensive global queries. A full queue on one CPU cannot necessarily borrow another's empty slots without an explicit stealing or rebalance protocol.

### Lookup, ownership, and reclamation

Locks can protect both reachability and reference acquisition: look up under the lock, increment a live object's reference, release the lock, use it, then decrement. Teardown marks the object dying under the same synchronization so no new references succeed, removes indexes, and waits for outstanding owners.

RCU lets readers traverse a published version while an updater removes an object. Removal prevents future readers from finding it; a grace period waits for readers that could still hold the old pointer. If use extends outside the RCU read-side section, the reader commonly needs a successful reference acquisition or another lifetime guarantee before leaving.

Reference counting and RCU solve different parts. A count keeps an already acquired object alive. RCU can protect the interval in which lookup finds the object and attempts that acquisition. Neither automatically revokes capabilities, stops device DMA, or cancels queued callbacks.

### Concurrency and memory ordering

A lock defines mutual exclusion and, under its API, visibility between holders. Lockless designs replace that convenient package with explicit atomic states and acquire/release or stronger ordering. Every published pointer needs a statement connecting initialization writes to reader observation.

Linearizability asks whether each operation appears to occur at one point consistent with real-time order. Some kernel structures intentionally promise weaker snapshots or tolerate stale reads. State the contract. “Lock-free” is a progress property, not a synonym for race-free, wait-free, faster, or safely reclaiming memory.

Interrupt disabling affects only eligible delivery on a local CPU. Preemption disabling prevents scheduler migration but not other CPUs. Spinlocks, sequence counters, RCU, atomics, and sleepable locks each protect different contexts and access patterns. Structure and synchronization must be designed together.

### Locality, sizing, and observability

Measure cache misses, remote cache-line transfers, allocation, lock wait, retries, traversal length, resize stalls, and tail latency. Big-O analysis does not predict constants or topology. A dense sorted array can beat a tree for small mostly read-only sets; a tree avoids costly shifts under frequent updates.

Size metadata deliberately. Embedding several links, locks, counters, and debug fields in millions of objects can dominate memory. Packing hot read fields together helps locality, while placing independently written counters on the same line creates false sharing. Layout can conflict with ABI, cache, and hardening requirements.

Debug aids include poisoned links, canaries, generation counters, lock assertions, reference tracking, cycle detection, and invariant walks. They need production cost and failure policy. Traversing a live structure without its read protocol can itself crash or report impossible mixed state.

## Definitions and Notation

Let structure state be `S`, its representation invariant `I(S)`, and operation `op` with precondition `P_op` and postcondition `Q_op`. Sequential correctness requires

`I(S) ∧ P_op(S) => I(op(S)) ∧ Q_op(S, op(S))`.

Concurrent correctness additionally requires a history model: linearizable operations have an admissible linearization point, while weaker structures name allowed stale or partial observations. The synchronization and memory-order protocol is part of `op`, not an annotation added afterward.

For object `x`, let `reachable(x)` mean an index can return it, `live(x)` mean new ownership may be acquired, and `refs(x)` count existing acquired owners under its protocol. A safe teardown order is

`live(x) := false; remove_reachability(x); wait_prior_readers(); wait_until(refs(x) = 0); reclaim(x)`.

Exact ordering and initial ownership vary, but reclaim must not precede any reader or owner that can dereference `x`. For handle `(id, gen)`, lookup succeeds only when the indexed object's current generation equals `gen` and lifetime acquisition succeeds.

For a bounded ring with monotonic producer `p`, consumer `c`, and capacity `N`, occupancy is `p - c` in a proven sequence-number domain and must satisfy `0 ≤ p - c ≤ N`. Physical slot selection is `sequence mod N`; publication ordering is a separate obligation.

## Mechanisms, Invariants, or Proof Structure

Review a kernel structure through seven obligations.

**Representation integrity.** Links, roots, heights, colors, bucket membership, ranges, indexes, counts, and sentinel state satisfy a declared invariant after every published operation.

**Identity integrity.** Full keys, namespaces, generations, object state, and authority checks prevent collision or reuse from selecting the wrong object.

**Synchronization integrity.** Every reader and writer follows the same locking, RCU, sequence, or atomic protocol, including interrupt, callback, debug, teardown, and error paths.

**Lifetime integrity.** Reachability, live state, references, grace periods, callbacks, DMA, and reclamation form an explicit state machine with no resurrection or double free.

**Context integrity.** Operations do not sleep or perform disallowed allocation in atomic context, recurse through unsafe callbacks, or hold locks across unbounded work.

**Progress integrity.** Collision chains, retries, resizing, scans, aggregation, and queues remain bounded or degrade under an explicit overload policy.

**Evidence integrity.** Invariant tests, concurrency stress, fault injection, formal models, and performance measurements state configuration and the properties they actually cover.

The executable model below implements a generation-tagged handle table. It checks stale-handle rejection and capacity reuse, not real concurrency or kernel memory safety.

<!-- bijux-verify: {"id":"toy-generation-handles","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=0:1\nlookup-first=device-a\nstale-after-remove=yes\nsecond=0:2\nstale-after-reuse=yes\nlookup-second=device-b\n","stderr":""}} -->
```python
class HandleTable:
    def __init__(self, capacity):
        self.slots = [None] * capacity
        self.generations = [0] * capacity

    def insert(self, value):
        index = self.slots.index(None)
        self.generations[index] += 1
        self.slots[index] = value
        return index, self.generations[index]

    def lookup(self, handle):
        index, generation = handle
        if not 0 <= index < len(self.slots):
            return None
        if self.generations[index] != generation:
            return None
        return self.slots[index]

    def retire(self, handle):
        if self.lookup(handle) is None:
            return False
        self.slots[handle[0]] = None
        return True


table = HandleTable(1)
first = table.insert("device-a")
print(f"first={first[0]}:{first[1]}")
print(f"lookup-first={table.lookup(first)}")
table.retire(first)
print("stale-after-remove=" + ("yes" if table.lookup(first) is None else "no"))
second = table.insert("device-b")
print(f"second={second[0]}:{second[1]}")
print("stale-after-reuse=" + ("yes" if table.lookup(first) is None else "no"))
print(f"lookup-second={table.lookup(second)}")
```

Passing proves only these sequential results for one slot and an unbounded Python generation integer. It does not address wrap, atomic publication, references, RCU, malicious guessing, allocation failure, or a real kernel object.

## Alternatives and Trade-Offs

**Arrays versus linked structures.** Arrays offer compactness and locality with bounds and resize costs. Linked structures support flexible insertion and stable node addresses but pay allocation, linkage, and cache-miss costs.

**Hash indexes versus ordered trees.** Hashing favors exact lookup under controlled load. Trees support order, ranges, and predictable logarithmic depth. Adversarial keys, resize, iteration, and memory footprint can reverse a simplistic choice.

**Global versus per-CPU structures.** Global structures simplify capacity and exact queries but contend. Per-CPU state improves local paths while increasing memory, aggregation, imbalance, and hotplug complexity.

**Locks versus RCU.** Locks provide direct mutual exclusion and can simplify updates. RCU enables cheap read-mostly traversal but separates removal from reclamation and complicates updates, callbacks, and teardown.

**Reference counts versus external ownership.** Reference counts support shared dynamic lifetime but add atomic traffic and cycle or resurrection hazards. Hierarchical or subsystem ownership can be cheaper when lifetimes nest cleanly.

**Bounded rings versus elastic queues.** Rings avoid allocation and provide predictable capacity. Elastic queues absorb bursts until memory pressure becomes the failure; both need explicit backpressure and drop policy.

**Generic containers versus specialized structures.** Generic APIs reduce duplicate code and concentrate tests. Specialized representations can encode invariants and locality better but increase maintenance and review surface.

## Failure Modes and Misconceptions

1. **“A list is the default kernel container.”** Arrays or other compact structures often provide better locality and simpler bounds.
2. **“Constant-time insertion means constant-time enqueue.”** Finding position, allocating, and synchronizing may dominate.
3. **“Safe iteration is concurrency safe.”** It may only preserve the next cursor during same-thread deletion.
4. **“Removing an entry frees it.”** Reachability and memory lifetime are separate.
5. **“A reference count prevents every use-after-free.”** Lookup must acquire the reference before teardown can reach zero.
6. **“RCU readers may retain pointers forever.”** Use beyond the read-side section needs another lifetime guarantee.
7. **“An atomic pointer publishes an object.”** Initialization visibility needs the matching memory order.
8. **“Hash lookup proves identity.”** Full key, namespace, generation, live state, and authority still matter.
9. **“Integer IDs are permanent capabilities.”** Reuse can redirect stale operations unless the protocol detects generations or revokes handles.
10. **“Per-CPU means race-free.”** Migration, remote access, aggregation, interrupt nesting, and hotplug create races.
11. **“Lock-free means faster.”** Contention, retries, cache traffic, reclamation, and workload determine performance.
12. **“Ring wrap is harmless with unsigned integers.”** Capacity and difference bounds must make wrap comparisons unambiguous.
13. **“Debug scans cannot hurt correctness.”** They can violate lifetime, recurse, hold locks, or create unbounded latency.
14. **“Big-O selects the production structure.”** Constants, cache topology, context, allocation, contention, and failure policy matter.

## Worked Examples

### Example 1

**Question:** One process object must appear in a global list and its parent's child list. Can both use the same intrusive link?

**Reasoning:** Each link stores neighbors for one membership. Inserting it into the second list overwrites the first membership and joins or corrupts the structures.

**Conclusion:** Embed a distinct, clearly named link for each independently maintained membership.

### Example 2

**Question:** A reader loads an object pointer from an ID table, releases the table lock, then increments its reference. What race exists?

**Reasoning:** A remover can delete the slot, observe the last reference, and free the object between unlock and increment. The reader then modifies freed memory.

**Conclusion:** Lookup and successful lifetime acquisition must overlap under a lock, RCU-plus-live-reference protocol, or equivalent mechanism.

### Example 3

**Question:** Why may a sorted array outperform a red-black tree for 24 rarely changing entries?

**Reasoning:** Binary search touches compact contiguous memory with few cache lines and no per-node links. Shifting 24 entries on rare updates may be cheaper than routine pointer chasing.

**Conclusion:** Population, update ratio, and locality can dominate asymptotic update cost.

### Example 4

**Question:** A level-triggered interrupt enqueues work into a full bounded ring. What must the subsystem define?

**Reasoning:** The handler may be unable to sleep or allocate. It needs a bounded choice: drop with accounting, mask and defer, overwrite only under an explicit loss policy, or signal backpressure to hardware.

**Conclusion:** Capacity exhaustion is part of the data-structure contract, especially in atomic context.

### Example 5

**Question:** An RCU updater unlinks a route and immediately frees it because new lookups cannot find it. Why is that unsafe?

**Reasoning:** A reader that began earlier may still hold the old pointer. Unlinking prevents future reachability but not prior dereference.

**Conclusion:** Reclamation waits for the relevant grace period and any ownership extending beyond it.

### Example 6

**Question:** A user can choose keys that all land in one hash bucket. What changes?

**Reasoning:** Expected constant lookup becomes linear, consuming privileged CPU and holding locks. Resize alone may preserve the collision if the hash is predictable.

**Conclusion:** Use an appropriate keyed hash, bounds, accounting, or worst-case structure for hostile keys.

### Example 7

**Question:** A per-CPU counter is summed while CPUs update it. Is the result wrong?

**Reasoning:** It may be an allowed approximate observation if the API states that semantics. If exact accounting drives authorization or billing, updates must be frozen, versioned, or reconciled.

**Conclusion:** Aggregation consistency is a contract choice, not an automatic property of per-CPU storage.

### Example 8

**Question:** A timer heap changes a task's deadline in place without repositioning the node. What fails?

**Reasoning:** Parent-child heap order may no longer hold, so extracting the root can miss the earliest deadline.

**Conclusion:** Key mutation must restore the structure invariant before publication.

### Example 9

**Question:** A diagnostic command walks every socket while holding the global update lock. Why can this be operationally dangerous?

**Reasoning:** Formatting or copying output can be slow, block, or fault. Updates and critical paths stall behind an unbounded observer.

**Conclusion:** Use bounded snapshots, restartable iteration, references, or a read-optimized protocol for observability.

### Example 10

**Question:** A medical controller uses a lock-free queue between an interrupt and actuator task. Does a stress test establish safety?

**Reasoning:** Safety also depends on memory ordering, capacity exhaustion, stale commands, deadline bounds, corruption detection, actuator limits, compiler and hardware behavior, and degraded-state policy.

**Conclusion:** A named safety authority and concurrency reviewer must assess the full evidence and residual risk; this module claims no certification.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) develops the abstract structures, proofs, and performance models. This module adds privileged failure impact, intrusive representation, atomic-context restrictions, reclamation, per-CPU topology, and kernel observability. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops linearizability, progress, atomics, and memory reclamation.

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains caches, coherence, atomic instructions, barriers, and topology. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects stale handles, collision attacks, memory corruption, and invariant hardening. [Database Engineering](../../18-database-engineering/ROADMAP.md) offers parallel lessons in indexes, latches, generations, and concurrent reclamation.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) adds hazard-based bounds and accountable evidence. Successors [OS-008](../ROADMAP.md), [OS-021](../ROADMAP.md), [OS-024](../ROADMAP.md), and [OS-054](../ROADMAP.md) deepen allocation, critical sections, atomics, and RCU used by these structures.

## References

- Linux Kernel documentation, [Linked Lists in Linux](https://docs.kernel.org/core-api/list.html), current page checked 2026-09-04. Intrusive circular-list representation, operations, iteration, splicing, and concurrency considerations.
- Linux Kernel documentation, [Red-black Trees in Linux](https://docs.kernel.org/core-api/rbtree.html), current page checked 2026-09-04. Embedded nodes, search responsibilities, insertion, deletion, caching, and augmented trees.
- Linux Kernel documentation, [XArray](https://docs.kernel.org/core-api/xarray.html), current page checked 2026-09-04. Integer-indexed objects, locking, marks, iteration, allocation modes, and advanced API cautions.
- Linux Kernel documentation, [Maple Tree](https://docs.kernel.org/core-api/maple_tree.html), current page checked 2026-09-04. Non-overlapping range storage, cursor operations, locking, allocation, and RCU-aware modes.
- Linux Kernel documentation, [ID Allocation](https://docs.kernel.org/core-api/idr.html), current page checked 2026-09-04. IDR and IDA semantics, cyclic allocation, locking, preload, and replacement.
- Linux Kernel documentation, [Circular Buffers](https://docs.kernel.org/core-api/circular-buffers.html), current page checked 2026-09-04. Power-of-two indexing and producer-consumer memory-order requirements.
- Linux Kernel documentation, [Adding reference counters to kernel objects](https://docs.kernel.org/core-api/kref.html), current page checked 2026-09-04. Reference acquisition, release, initialization, and lifetime rules.
- Linux Kernel documentation, [Per-CPU variables](https://docs.kernel.org/core-api/this_cpu_ops.html), current page checked 2026-09-04. CPU-local addressing and operations with migration and remote-access considerations.
- Linux Kernel documentation, [RCU Handbook](https://docs.kernel.org/RCU/index.html), current page checked 2026-09-04. Primary index for read-side, update, grace-period, reclamation, and verification guidance.
- Linux Kernel documentation, [Linux kernel memory barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Kernel memory-ordering requirements and limitations.
- Linux Kernel documentation, [Generic min-heap API](https://docs.kernel.org/core-api/min_heap.html), current page checked 2026-09-04. Dense heap operations and callback-based comparison and movement.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching uses of process tables, free lists, queues, buffers, page tables, references, and locks.

## Exercises

### Exercise 1

Choose structures for a dense CPU mask, sparse process-ID lookup, earliest-deadline timer selection, virtual-address ranges, FIFO completion queue, and read-mostly route table. State operations, concurrency, lifetime, context, capacity, and locality before naming each structure.

### Exercise 2

Design the full lifetime state machine for an ID-indexed device that is also linked into a bus list and accessed under RCU. Cover insertion ownership, live publication, lookup reference acquisition, removal, callbacks, DMA, grace period, last reference, and ID reuse.

### Exercise 3

Prove the representation conditions for a power-of-two bounded ring with monotonic sequence numbers. Include empty, full, wrap, reservation, payload publication, observation, cancellation, and producer or consumer death.

### Exercise 4

Design a fair benchmark comparing an intrusive list, sorted array, hash table, red-black tree, and multiway range tree for a kernel lookup workload. Include distributions, hostile keys, mutation, cache and NUMA effects, allocation, contention, memory, and tail latency.

### Exercise 5

A safety controller uses per-CPU queues, generation-tagged handles, and RCU to dispatch actuator commands. Construct an assurance review separating invariant tests, concurrency stress, formal reasoning, hardware evidence, fault injection, operational controls, and named human judgment.

## Answers to the Exercises

### Answer 1

Use a bitmap for a bounded dense CPU set because membership, intersection, and first-set search operate compactly by words. Use an integer index such as an XArray-like map for sparse process IDs, paired with namespace, generation, and lifetime acquisition. Use a min-heap for earliest deadline if arbitrary removal has an index map; define equal-deadline order. Use a range-aware balanced or multiway tree for virtual intervals, with half-open endpoints and overlap policy.

Use a bounded ring for completion FIFO when capacity and nonblocking behavior are explicit; otherwise a linked queue with an allocation and backpressure policy. A read-mostly route table might use a hash or trie plus RCU, depending on exact-match versus prefix semantics and hostile-key requirements. None of these choices is complete until reader/writer contexts, snapshot guarantees, allocation flags, ownership, reclamation, population, update ratios, and overload behavior are specified.

### Answer 2

Allocation begins with one construction owner while the object is unreachable and not live. Initialize both index and bus linkage, immutable identity, generation, locks, and device state. Under the update protocols, publish the bus membership and ID slot only after full initialization, then allow conditional reference acquisition. An RCU reader finds the slot, validates full ID, generation, namespace, and live state, acquires a reference before leaving its read-side section, and releases after use.

Teardown marks the device dying under synchronization that excludes new references, disables new submissions, removes both memberships, and revokes user-visible handles. It quiesces interrupts and DMA, cancels or drains callbacks, waits for prior RCU readers, then waits for all acquired references except the teardown owner. Only then does it release device state and memory exactly once. The integer slot may be reused with a new generation after old lookups cannot succeed; generation wrap needs a bound or a wider non-repeating identity.

### Answer 3

Let producer sequence `p` reserve the next write and consumer sequence `c` reserve the next read, with capacity `N = 2^k`. Maintain `0 ≤ p - c ≤ N` in a sequence domain wide enough that no live separation is ambiguous. Empty is `p = c`; full is `p - c = N`; physical position is `sequence & (N - 1)`. Raw masked indexes alone cannot distinguish full from empty.

A producer atomically reserves a unique sequence only when not full, writes the payload, then release-publishes that slot's sequence or ready state. A consumer acquire-observes readiness before reading, then release-publishes the slot as reusable. Multiple producers must not expose reservation as completion; multiple consumers must claim each ready sequence once. Cancellation publishes an explicit skipped state so the consumer cannot wait forever. If a participant can die, another agent needs authority and evidence to complete or abort reserved slots. Stress tests around counter wrap support the argument, but the actual atomic algorithm still needs a formal memory-model review.

### Answer 4

Generate populations from tiny to maximum credible size and lookups that are uniform, skewed, ordered, range-containing, hit, and miss. Include adversarial hash keys and sorted insertion. Sweep read/write/delete ratios, iteration, bulk updates, and resize. Run single CPU, shared-cache multicore, cross-socket NUMA, interrupt-like nonblocking contexts, and representative allocation pressure.

Measure operation distributions and high percentiles, cache and TLB misses, remote transfers, branch misses, lock wait, retries, allocations, resize pauses, memory per entry, and time under disabled preemption or interrupts. Hold semantics, lifetime safety, key hardening, compiler, CPU placement, initialization, and measurement endpoints constant. Report warm and cold states, confidence or run variation, saturation, and failure behavior. A structure that wins exact lookups may lose range queries, iteration, memory, or adversarial load; publish the decision against the stated mix.

### Answer 5

State command integrity, freshness, ordering, deadline, and safe-state properties. Inspect per-CPU selection under migration, interrupt nesting, remote access, CPU hotplug, and drain. Prove handle generation validation before authority and bound generation reuse. Trace RCU publication, removal, grace periods, references beyond read sections, callbacks, and final reclamation. Specify queue capacity, wrap domain, memory ordering, overload, stale-command rejection, and actuator acknowledgement.

Invariant tests check links, indexes, generations, queue occupancy, unique ownership, and reference states. Concurrency stress varies CPUs, preemption, interrupts, teardown, hotplug, and wrap; fault injection corrupts descriptors, delays readers, drops completions, exhausts queues, resets devices, and kills owners. Formal reasoning targets the state machine and hardware memory model; deployed evidence covers compiler, processor, DMA, timing, startup, recovery, monitoring, and configuration. A named concurrency expert, control engineer, safety authority, security reviewer, and acceptance owner must assess coverage, independence, unresolved findings, and residual risk. This chapter and its Python handle table claim no external certification.
