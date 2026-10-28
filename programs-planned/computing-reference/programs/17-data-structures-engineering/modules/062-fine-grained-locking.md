---
module_id: DSE-062
program: Data Structures Engineering
level: 2
module_number: 62
title: Fine-Grained Locking
status: complete
last_verified: 2026-08-30
---

# Fine-Grained Locking

## One-Page Review

### Governing question

How can a data structure replace one global lock with several narrower synchronization domains while preserving representation invariants, linearizability, visibility, deadlock freedom, lifecycle safety, and a measured performance benefit?

### Essential definitions

- A **guard map** maps each mutable field, node, bucket, range, or invariant to the lock or protocol that protects it.
- **fine-grained locking** permits operations on independent regions to overlap by using multiple locks with narrower protection domains.
- **lock striping** maps many logical objects to a fixed, smaller array of locks, usually by a stable hash-to-stripe function.
- **lock coupling** or **hand-over-hand locking** acquires the next node's lock before releasing the current node's lock during traversal.
- A **lock order** is a strict global order in which every operation acquires multiple locks; a strict order prevents cycles in the lock wait-for graph.
- **validation** rechecks that observations made before or between acquisitions still describe a legal current neighborhood.
- A **linearization point** is the instant between invocation and response at which an operation takes effect in the abstract sequential history.
- **structural modification** changes reachability or routing, such as linking, unlinking, rotating, splitting, merging, or resizing.
- **safe reclamation** delays destruction or reuse until no thread can retain a reference to the retired object.
- **false sharing** occurs when independent frequently written data, such as adjacent locks, share a cache line and cause coherence traffic.

### Central model, mechanism, or theorem

Let mutable representation regions be `R`, locks be `L`, and `guard(r)` identify the lock protecting each region `r`. An operation computes a finite protection set, acquires all required locks according to one strict order or a proven coupling protocol, validates any observations made without the complete set, performs its abstract effect while every touched invariant is protected, restores the representation invariant, and releases locks on every exit. If conflicting abstract effects share an exclusive protection domain, synchronized visibility follows the target memory model, and each operation has a valid linearization point, then histories can be linearizable while effects on disjoint regions overlap.

The deadlock argument for ordered acquisition is short. Every wait edge points from a held lower-ranked lock to a requested higher-ranked lock. A directed cycle would imply a strict chain `rank(L1) < rank(L2) < ... < rank(L1)`, which is impossible. This proves absence of lock-order cycles under the assumptions; it does not prove starvation freedom, bounded waiting, crash recovery, or safety of callbacks and other resources.

### Critical invariants

1. Every mutable location and cross-location invariant has one documented guard rule.
2. Conflicting operations share at least one exclusive lock for the interval containing their linearization points.
3. Multi-lock acquisition follows one strict order, or the algorithm proves why its coupling/retry discipline cannot cycle.
4. Traversal never releases the only protection that keeps the next reference reachable and valid before acquiring substitute protection.
5. Any state observed before acquiring the complete protection set is validated before mutation or trusted return.
6. Insert, delete, split, merge, rotate, rebalance, resize, and clear protect all affected routing and metadata state.
7. Unlock publishes a restored invariant; exceptions, cancellation, timeouts, and failed validation release exactly the locks actually acquired.
8. Retired locks/nodes are not destroyed or reused while holders, waiters, traversers, or stale references can still reach them.
9. Lock identity and rank remain stable for the duration of acquisition; equal objects/stripes are deduplicated.
10. Granularity is justified by workload measurements including throughput, tails, contention, retries, hold time, cache behavior, and memory cost.

### Common failures

- Giving each node a lock but leaving `size`, root/head, resize state, or parent-child relations unguarded.
- Locking the current node, reading `next`, releasing current, and only then locking `next`.
- Acquiring two bucket or node locks in argument order, so reversed calls can deadlock.
- Using mutable addresses, recycled IDs, or current array indexes as ranks without a stability argument.
- Mutating after optimistic traversal without validating adjacency, marks, version, or routing epoch.
- Removing a node safely from the abstract set and freeing it while another thread retains its address.
- Assuming read locks are harmless even though comparison, lazy caches, metrics, or callbacks write.
- Resizing a striped table while operations still map keys with different stripe/table generations.
- Counting locks or uncontended microbenchmarks as evidence of scalable throughput.
- Treating race-detector silence as a proof of invariants, linearizability, deadlock freedom, or reclamation safety.

### Compact example

A striped map has four stable mutexes and maps key `k` to stripe `k mod 4`. Operations on keys 0 and 1 can hold different stripes simultaneously; keys 0 and 4 conflict. A two-key operation deduplicates equal stripes and otherwise acquires stripe IDs in ascending order. The bounded executable model below confirms these properties for one finite schedule and eight integer keys. It does not create runtime threads or establish fairness, memory-model behavior, arbitrary-schedule correctness, or speedup.

### Connections

[DSE-061](061-thread-safe-wrappers-and-coarse-grained-locks.md) supplies the single-lock correctness baseline. [DSE-023](023-linear-probing.md) and [DSE-031](031-binary-search-trees.md) supply representations whose routing and structural invariants constrain lock placement. The next module, DSE-063, applies these ideas to concurrent hash maps; the [program roadmap](../ROADMAP.md) continues through concurrent queues, atomics, nonblocking progress, reclamation, and linearizability testing.

## Governing Question

Can we decompose a concurrent data structure's state and proof so independent operations overlap, without introducing an unguarded invariant, inconsistent observation, lock cycle, use-after-free, or performance regression?

## Why This Matters

A coarse lock intentionally converts an object into one synchronization domain. That is often the best starting point: its proof is compact, its failure surface is visible, and its constant costs can be low. It also serializes operations that have no semantic conflict. Two updates to different hash buckets, two tree traversals in disjoint subtrees, or a read and a distant mutation may wait solely because the implementation chose one global lock.

Fine-grained locking tries to make physical conflicts approximate abstract conflicts. The goal is not a large lock count. The goal is useful overlap with a proof that remains reviewable. Locks introduce acquisition instructions, queueing state, metadata, cache-line traffic, ordering rules, more exceptional exits, and more possible schedules. A design with 10,000 node locks can perform worse than one mutex at modest concurrency or when most operations touch a shared root.

The correctness difficulty is decomposition. A field may be local while an invariant is global. A tree node owns child links, yet a rotation changes a grandparent link, two child links, balance metadata, and reachability. A hash bucket may own entries, yet resizing changes the routing function by which every operation finds a bucket. A list node can be logically absent before its memory is safe to reclaim. `size` and capacity thresholds span regions even when keys do not.

There are consequently four distinct questions. **Safety:** which locks make every read/write and invariant transition legal? **Abstract correctness:** where does each operation linearize, and what do snapshots or aggregates promise? **Liveness:** can acquisitions cycle, retry forever, starve, or convoy? **Economics:** does reduced contention outweigh lock, cache, memory, and maintenance costs on the intended workload? A production-grade design answers all four.

Fine-grained locks remain relevant even when a library offers a concurrent collection. Library types have precise semantics: retrievals may be nonblocking, iterators may be weakly consistent, aggregate sizes may be estimates, and atomic compute callbacks may block competing updates. Engineers must understand those contracts before composing them. They also need these principles for storage engines, schedulers, caches, indexes, allocators, and kernels where a standard container does not own the whole invariant.

## Prerequisites and Retrieval

Retrieve sequential specifications, representation invariants, alias ownership, hash tables, linked lists, balanced trees, graph reachability, mutex semantics, memory visibility, wait-for graphs, exceptions, cancellation, and latency distributions. From [DSE-002](002-representation-invariants.md), retrieve the distinction between local shape facts and whole-representation invariants. From [DSE-061](061-thread-safe-wrappers-and-coarse-grained-locks.md), retrieve the wrapper proof: private ownership, complete API coverage, invariant restoration, target-language synchronization, and operation-specific linearization points.

You should be able to draw a wait-for graph, prove that a strict order is acyclic, distinguish data-race freedom from linearizability, and explain why a pointer can remain readable at the machine level while no longer being a valid object reference. Retrieve workload concepts including key popularity, read/write ratio, skew, operation mix, concurrency level, service time, throughput, and percentile latency.

## Learning Objectives

After completing this module, you can:

1. derive a guard map from representation fields and invariants;
2. distinguish node, bucket, range, subtree, stripe, and reader-writer locking;
3. trace lock coupling without exposing an unprotected traversal edge;
4. prove deadlock freedom for strict multi-lock ordering and identify assumptions;
5. place and justify linearization points for success, absence, retry, and failure;
6. validate optimistic observations before committing structural changes;
7. design safe locking for delete, rotation, resize, bulk, snapshot, and lifecycle operations;
8. separate logical removal from physical unlinking and memory reclamation;
9. diagnose starvation, livelock, false sharing, hot regions, and lock proliferation; and
10. construct correctness and performance evidence that can justify or reject finer granularity.

## Core Exposition

**Start with the abstract conflict relation.** For operations `a` and `b`, define an abstract conflict when their relative order can affect a return value or legal abstract state. Two inserts of different set elements may commute; two writes of the same map key do not; a snapshot conflicts with every update if it promises one atomic state. The physical protection relation must cover every abstract conflict, but it may conservatively serialize additional pairs.

Write the sequential specification first. For a sorted set, define `contains`, `add`, and `remove`, duplicate behavior, comparison order, and lifecycle. For a map, define key equality, atomic conditional methods, iteration consistency, aggregate accuracy, and resize observability. A vague API cannot be rescued by careful locks because there is no legal history against which to judge it.

**Build a guard map, not a lock inventory.** A guard map is a review artifact connecting state to protection:

| State or invariant | Guard rule | Why |
|---|---|---|
| List node key and successor | node lock while reachable | update adjacency atomically |
| Head/root identity | sentinel/root lock or versioned root protocol | routing entry point is shared |
| Hash bucket contents | corresponding bucket/stripe lock | same-bucket conflicts serialize |
| Table pointer and routing generation | resize lock/protocol | operations must use one generation |
| Exact global size | global counter lock or proved atomic scheme | bucket locks alone do not protect the sum |
| Node lifetime | reclamation protocol, not merely node mutex | a stale reference can outlive unlink |

The table forces cross-region invariants into view. If `size` must equal total entries at every linearization point, it needs a compositional counter design or wider locking. If size is an estimate, the API must say so. A lock protects code only when every access follows the same rule; its physical proximity to a field proves nothing.

**Choose granularity from stable ownership.** Per-node locks maximize potential locality but add memory, allocation, initialization, destruction, and traversal operations. Per-bucket locks fit hash routing but can be numerous and complicate resize. Striping bounds lock count: `stripe(k) = spread(hash(k)) mod S`. Many buckets share `S` stable locks, trading controlled false conflicts for lower metadata cost and simpler lifetime.

Range locks protect key intervals and can express scans, but overlapping-range detection becomes a concurrency structure of its own. Subtree locks can exploit tree locality but root-to-leaf traffic and rotations complicate ownership. Reader-writer locks allow compatible readers inside one region but add mode transitions and policy. Granularity can vary by layer: a short structural lock protects table generation while bucket locks protect entries.

Stable ownership is crucial. If a node moves, does its lock move with the node, protect its current position, or protect an immutable key range? If resizing changes bucket indices, an operation must not acquire a lock using the old array and mutate a bucket selected by the new array. Common strategies keep stripe identity stable across resizes, use a table-generation object whose locks live as long as users, or coordinate migration through explicit old/new ownership states.

**Use lock coupling when traversal itself needs protection.** In a sorted linked list with sentinels, a traversal at predecessor `p` reads successor `c`. To advance safely under pessimistic lock coupling:

1. hold `p.lock`;
2. read `c = p.next` while protected;
3. acquire `c.lock` before releasing `p.lock`;
4. confirm the algorithm's adjacency/lifecycle conditions;
5. release `p.lock` and continue with `c` as the protected current node.

At the update window, hold predecessor and current locks. An insertion between them creates a fresh node, initializes it privately, sets its successor to current, then publishes it through `p.next`. A successful insert can linearize at that publication. A removal can linearize at a logical mark or predecessor-link change, depending on the specified algorithm. Failed membership/update operations linearize at a protected observation proving presence or absence.

Acquiring current before predecessor is not arbitrary: all traversals follow list order, producing a natural strict acquisition order. A thread never moves backward while retaining a forward lock. Sentinels eliminate empty/head boundary special cases. The exact proof still needs node lifetime: acquiring `c.lock` is unsafe if `c` can be freed between reading the pointer and acquisition. Coupling must prevent that gap, or a separate pin/hazard/epoch/reference scheme must keep `c` alive.

Lock coupling can be correct but expensive. Every traversed node causes acquisition/release and cache traffic even for reads. Optimistic list designs instead traverse without locks, lock only a candidate predecessor/current neighborhood, then validate that both remain reachable, unmarked, and adjacent. Validation failure releases and retries. This changes the proof and liveness: the mutation window is shorter, but a contended operation can repeatedly lose validation.

**Order every multi-lock operation.** Define a strict rank independent of call argument order. For stripes, integer stripe IDs work if the stripe array remains the same generation. For immutable tree depth, parent-before-child can work for downward protocols but rotations and upward operations require careful rules. Memory addresses can be unique while objects live, but reuse, portability, relocation, equality, and same-object cases demand explicit treatment; a durable object ID may be safer.

For a two-key atomic move, compute both protection identities before acquisition. If equal, acquire once. Otherwise acquire `min(rank)` then `max(rank)` and release in reverse. Validate that both keys still belong to those domains if routing can change. Never accept `(source, destination)` argument order as lock order: concurrent moves `A→B` and `B→A` would produce the classic two-lock cycle.

The proof assumes operations never acquire an unranked external resource while holding ranked locks. Logging, allocation, callbacks, equality/hash/comparison, destructors, page faults, I/O, and condition waits can introduce hidden dependencies. Either constrain them, place them outside protected intervals, include them in a system-wide order, or use a protocol that releases and validates.

**Separate observation, protection, validation, and commit.** Optimistic traversal reads a candidate location before owning all locks. Those reads can guide a search only under a memory-safe mechanism; they cannot automatically justify a mutation. After acquiring locks, validate facts such as:

- predecessor/current remain reachable in the same table generation;
- neither node is logically deleted when the algorithm requires live nodes;
- predecessor still points to current;
- versions observed during search still match;
- the key still maps to the protected bucket/stripe;
- capacity and resize state still permit this update.

If validation fails, release all locks and retry from a defined point. A retrying operation must not have performed irreversible callbacks, I/O, publication, or external side effects. Bound or instrument retries when latency matters. Backoff can reduce contention but is an empirical policy, not a correctness proof.

**Prove linearizability operation by operation.** “Locks are held” is not a proof. Identify abstract effects and their points. A successful linked-list `add(x)` may linearize when the predecessor successor link first reaches the initialized new node. A failed add linearizes at the protected/validated observation of an equal live node. A successful remove may linearize when a logical deletion mark becomes visible or when unlink occurs; the choice affects concurrent `contains`. A lookup can linearize at a validated matching observation or at the read that establishes absence.

Disjoint operations can linearize concurrently in real time; the proof need only place them in some sequential order because their abstract effects commute. Conflicting operations share protection so their points are ordered. Nonoverlapping calls must preserve real-time order. Pending, timed-out, or cancelled calls need explicit rules about whether an effect may already have occurred.

Memory visibility comes from the official primitive and language memory model. Lock release publishes protected initialization only to acquisitions linked by the specified synchronization relation. Mixing locked writes with plain unlocked reads is not made safe because the machine is cache coherent. If an algorithm deliberately uses atomic reads plus locks for writes, it needs a mixed atomic/lock proof, not a mutex-only argument.

**Structural operations expose the real design.** In a tree rotation, local-looking changes cross several ownership domains: parent link to pivot, pivot child, transferred subtree parent link, balance/color metadata, perhaps root, and aggregate counters. Locking only the two rotated nodes is insufficient if another traversal uses the parent link or transferred child. Designs may lock a bounded neighborhood in rank order, use versioned optimistic validation, serialize rare rebalances with a structural lock, or choose a concurrency-friendly representation such as a skip list.

Hash-table resize is similarly global. Options include stopping updates under a resize lock; publishing a new generation and migrating while operations help; maintaining per-bucket migration states; or keeping stable stripes across arrays. Each needs routing rules for lookup/update during migration, one-entry ownership, publication ordering, failure recovery, and reclamation of the old table. Fine-grained ordinary operations do not imply a fine-grained resize.

Bulk methods and snapshots must have declared consistency. Locking all stripes in rank order gives an atomic snapshot but pauses updates and can create a long convoy. Copying each stripe independently yields a weakly consistent traversal, not one instant. Versioned retry may deliver an atomic snapshot only if the validation proof covers all regions and progress under writes is acceptable. Approximate aggregates may be composed from striped counters with stated error/recency semantics.

**Deletion is two problems.** Logical removal changes the abstract set/map. Physical unlinking removes a node from traversal. Reclamation makes its storage available for destruction or reuse. A node mutex cannot by itself show that no thread read the pointer earlier and is about to access or acquire it. Destroying a locked mutex or one with waiters is invalid under common APIs.

Managed runtimes can keep object memory alive through references but do not automatically preserve algorithmic validity; stale nodes can be unlinked or marked. Native systems need reference counts, hazard pointers, epochs, read-copy-update, ownership transfer, or another scheme whose guarantees match the access pattern. Reclamation is studied later in the program, but a fine-grained design must state the dependency now rather than hide `free` after unlink.

**Liveness extends beyond deadlock.** Strict order prevents cycles among participating locks, not starvation. Nonfair locks can repeatedly admit newcomers; reader-preferring policies can starve writers; writer preference can inflate reader tails. Optimistic validation can livelock under sustained mutation. A preempted holder can block one hot region; if that region is root or stripe 0, practical behavior may resemble a global lock.

Timeout and cancellation complicate partial acquisition. Track exactly which locks succeeded, unwind in reverse, and leave abstract state unchanged unless the operation crossed its linearization point. `tryLock` loops that release and retry can avoid blocking cycles but may livelock and require backoff/fairness analysis. Robust process-shared mutexes can report owner death with the lock acquired and protected state inconsistent; recovery must validate/repair the whole affected invariant before marking it consistent.

**Measure the mechanism, not the slogan.** Compare against the correct coarse implementation with identical semantics, representation, allocator, workload, and validation. Vary threads, operation mix, key distribution/skew, size, read/write ratio, resize frequency, NUMA placement, and critical-section work. Report throughput and percentile/end-to-end latency, not averages alone.

Instrument acquisition wait, hold duration, contention/failure, retry counts, queue depth if available, operations per stripe/node, and time in resize/reclamation. Profile cache misses/coherence and scheduler behavior when tools permit. Pad or separate hot lock metadata only after measuring false sharing; padding every node can damage cache capacity. A finer design earns adoption only when its relevant workload benefit exceeds added correctness, memory, maintenance, and operational cost.

**Test in layers.** Sequential tests establish the abstract type. Invariant assertions under the proper locks catch representation corruption. Controlled schedules target adjacency, reversed two-key calls, resize/mutation overlap, cancellation after partial acquisition, exceptions, and removal with stale references. History tests record invocation, response, arguments, and results for linearizability checking. Race detectors discover some unsynchronized memory accesses; dynamic lock dependency tools discover exercised order cycles. Stress and fault injection broaden evidence but do not exhaust schedules.

The following executable artifact is deliberately a finite state model, not a threaded benchmark. It demonstrates stripe exclusion, simultaneous ownership of distinct stripes, stable mapping, deduplication/order for two-key acquisition, full release, and final-state invariants for one deterministic schedule.

<!-- bijux-verify: {"id":"striped-lock-schedule-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stripes=4\nkeys=0,1,2,3,4,5,6,7\nsum_values=28\nmax_parallel_owners=2\nsame_stripe_conflict_rejected=True\nordered_pair=1,3\nlocks_released=True\nall_invariants=True\nevidence=finite_fine_grained_lock_model\n","stderr":""}} -->
```python
class StripedScheduleModel:
    def __init__(self, stripe_count):
        self.stripe_count = stripe_count
        self.owners = [None] * stripe_count
        self.values = {}
        self.max_parallel_owners = 0

    def stripe(self, key):
        return key % self.stripe_count

    def acquire(self, worker, stripe):
        if self.owners[stripe] is not None:
            return False
        self.owners[stripe] = worker
        active = len({owner for owner in self.owners if owner is not None})
        self.max_parallel_owners = max(self.max_parallel_owners, active)
        return True

    def release(self, worker, stripe):
        assert self.owners[stripe] == worker
        self.owners[stripe] = None

    def put(self, worker, key, value):
        stripe = self.stripe(key)
        assert self.acquire(worker, stripe)
        self.values[key] = value
        self.release(worker, stripe)

    def ordered_stripes(self, first_key, second_key):
        return sorted({self.stripe(first_key), self.stripe(second_key)})


model = StripedScheduleModel(4)
assert model.acquire("left", model.stripe(0))
assert model.acquire("right", model.stripe(1))
same_stripe_conflict_rejected = not model.acquire("blocked", model.stripe(4))
model.values[0] = 0
model.values[1] = 1
model.release("right", model.stripe(1))
model.release("left", model.stripe(0))

for key in range(2, 8):
    model.put("loader", key, key)

ordered_pair = model.ordered_stripes(5, 7)
locks_released = all(owner is None for owner in model.owners)
all_invariants = (
    sorted(model.values) == list(range(8))
    and sum(model.values.values()) == 28
    and same_stripe_conflict_rejected
    and ordered_pair == [1, 3]
    and locks_released
)

print(f"stripes={model.stripe_count}")
print("keys=" + ",".join(str(key) for key in sorted(model.values)))
print(f"sum_values={sum(model.values.values())}")
print(f"max_parallel_owners={model.max_parallel_owners}")
print(f"same_stripe_conflict_rejected={same_stripe_conflict_rejected}")
print("ordered_pair=" + ",".join(str(stripe) for stripe in ordered_pair))
print(f"locks_released={locks_released}")
print(f"all_invariants={all_invariants}")
print("evidence=finite_fine_grained_lock_model")
```

The assertions are exact executable evidence for this bounded model. They do not execute OS threads, exercise a real mutex, prove target-language happens-before, cover arbitrary interleavings or hashes, measure contention, or establish production linearizability. Those claims require implementation-specific tests, history analysis, race/lock-order tools, and workload measurement.

## Definitions and Notation

Let the sequential abstract object be `A` and concrete representation be `C`. Let `I(C)` be its representation invariant. Let `R = {r1, ..., rn}` be protection regions and `L = {l1, ..., lm}` be locks. A **guard map** `g: R → 2^L` gives the lock set required to access each region; some invariants require the union of several region guards or an additional structural lock.

For operation `op`, let `read(op)` and `write(op)` be abstract locations it observes and changes. Operations conflict when their relative order can affect abstract state/results. The implementation's protection-set function `P(op, C)` must ensure conflicting effects share exclusive protection during the relevant interval. Because the location can depend on mutable routing, `P` may be tentative until validation.

Let `rank: L → Q` map locks to a strict totally ordered domain `Q`. Ordered acquisition requires each thread's newly acquired distinct lock to have rank greater than every lock it currently retains in the protocol. Equal lock identities are deduplicated. A **wait-for graph** has a thread-to-lock edge for a requested unavailable lock and a lock-to-thread edge for current ownership.

For a striped table with `S > 0`, `stripe(k) = spread(hash(k)) mod S`. A **false conflict** occurs when nonconflicting keys map to one stripe and serialize. Increasing `S` can reduce false conflicts but increases metadata and may worsen locality. `S` is a tuning parameter, not a semantic guarantee.

A history `H` records invocation and response events. `op1 <H op2` means `op1` returns before `op2` is invoked. A history is **linearizable** if completed calls (with the formal treatment of pending calls) can be arranged into a legal sequential history preserving `<H`. The **linearization point** of an operation is the proof event realizing that placement.

A node can be **logically removed** (absent from `A`), **physically unlinked** (not reachable through normal traversal), yet not **reclaimed** (storage cannot be destroyed/reused). A **retired** node awaits a reclamation guarantee. These are three separate state transitions.

For measurement, let `W` be time waiting to acquire, `H` lock hold time, `X` end-to-end operation latency, `T(p)` throughput at concurrency `p`, `Rtry` retries per operation, and `C(l)` acquisitions/contentions by lock. These are empirical random variables/counters, not correctness quantities.

## Mechanisms, Invariants, or Proof Structure

### Guard-map derivation

1. State the sequential abstract operations and consistency of aggregates/iteration.
2. Enumerate concrete fields, reachability edges, metadata, callbacks, lifecycle state, and reclamation state.
3. Write local and cross-region invariants, including resize/rotation transitional states.
4. Assign a stable guard rule to every access and invariant transition.
5. For each operation, derive tentative routing, required protection set, acquisition order, validation predicate, effect, and release/failure path.
6. Audit every API surface, including reads, diagnostics, serialization, bulk methods, iterators, close, and error formatting.

### Safety and linearizability proof template

For each operation, establish:

1. references used before locking remain memory-safe under ownership/reclamation assumptions;
2. acquisitions synchronize with preceding releases as required by the target memory model;
3. validation establishes that the protected neighborhood still represents the searched abstract location;
4. all reads/writes that can violate `I` occur with the necessary guards;
5. the operation restores `I` before publishing/releasing protection;
6. one concrete event is a legal linearization point for every return class;
7. conflicting points are ordered by shared exclusive protection, while commuting disjoint points may be placed either way;
8. exception, timeout, cancellation, and retry paths neither leak locks nor create an unreported abstract effect.

### Deadlock theorem for ranked locks

Assume every blocking acquisition while holding protocol locks requests a distinct lock of strictly greater rank, rank remains stable, all relevant locks/resources participate, and release does not add wait edges. Suppose a deadlock cycle exists. Traversing the cycle follows acquisitions from each held lock to a strictly higher requested lock, yielding `rank(l1) < rank(l2) < ... < rank(lk) < rank(l1)`. Transitivity gives `rank(l1) < rank(l1)`, contradicting irreflexivity. Therefore no such lock-order cycle exists.

This is a proof under assumptions, not universal deadlock freedom. Condition waits, callbacks, allocator/runtime locks, I/O, signal/interrupt contexts, same-lock recursion, and protocols that violate or dynamically change rank fall outside unless modeled. It also says nothing about starvation, livelock, priority inversion, or bounded completion.

### Coupling invariant

During forward traversal, the thread holds protection for the edge/reference by which it obtains the next node until it has acquired protection or a lifetime pin sufficient for that node. At an update window, all edges and node states whose simultaneous consistency establishes adjacency are protected and validated. Release moves monotonically with traversal. This invariant prevents a gap in which both current and successor relation are unprotected.

### Resize and lifecycle invariant

Each operation belongs to one routing generation or follows an explicit migration protocol. Entries are reachable according to exactly the states allowed by that protocol—never lost, duplicated abstractly, or mutated through an unprotected generation. Old table/node/lock storage remains alive until no operation, holder, waiter, or retained reference can use it. Close/destruction prevents new entrants, waits or cancels according to policy, and reclaims only after quiescence.

### Evidence ladder

1. Sequential specification and invariant tests.
2. Static guard-map/API audit and rank audit.
3. Deterministic schedules for adjacency, reversed arguments, retries, partial acquisition, structural change, and deletion.
4. Recorded-history linearizability checking over bounded/stress executions.
5. Race, memory, and dynamic lock-dependency tools within their documented scope.
6. Fault/cancellation/owner-death and lifecycle testing where supported.
7. Differential behavior against a coarse correct oracle.
8. Workload-calibrated throughput, tail, wait/hold, retry, cache, resize, and reclamation measurement.

Passing a lower rung does not imply the higher ones. No finite execution proves all schedules; tools can have blind spots; a formal model proves only its modeled assumptions; a benchmark says nothing about abstract correctness.

## Alternatives and Trade-Offs

| Design | Potential overlap | Main proof advantage | Main cost or limit |
|---|---|---|---|
| One coarse mutex | none within object | simple total order and whole invariant | convoying and unrelated serialization |
| Per-node coupling | operations separated along path | local adjacency protection | lock per hop, memory/lifetime complexity |
| Optimistic fine locking | long traversals overlap | short mutation window | validation retries and starvation risk |
| Per-bucket locks | different buckets overlap | aligns with hash routing | hot buckets and resize coordination |
| Fixed lock striping | different stripes overlap | bounded stable lock set/order | false conflicts; aggregates still global |
| Reader-writer region locks | compatible reads overlap | explicit read/write modes | mode/fairness/upgrade complexity |
| Hierarchical/subtree locks | disjoint branches overlap | structure-aware conflicts | rotations and ancestor traffic |
| Immutable/persistent snapshots | readers avoid mutation locks | stable read view | allocation, publication, reclamation |
| Actor/owner thread | messages overlap outside owner | serialized state ownership | queueing, backpressure, cross-object protocols |
| Transactional/optimistic validation | speculative disjoint work | declarative commit validation | aborts, retry side effects, runtime constraints |
| Atomic/nonblocking algorithms | no mutex-holder blocking | stronger possible progress class | memory ordering, ABA, reclamation complexity |

A hybrid is common. A table can use stable stripes for entries, an atomic/versioned table pointer for routing, and a rare global resize protocol. A tree can use optimistic reads, node locks for updates, and a short structural lock for rare rebalance. Hybrid correctness must be proved as a composition: adding mechanisms does not let each assume the others are absent.

Reader-writer locks help only when read critical sections are sufficiently long, concurrent readers are common, and writes are not starved. If reads touch one cache line briefly, mode bookkeeping can dominate. Upgrade is especially hazardous: two readers that both wait to upgrade can deadlock unless the primitive supplies a specific conversion protocol. Release-read-then-acquire-write requires revalidation.

Lock striping is often the engineering midpoint. It bounds metadata and provides a simple integer order for multi-key operations. It cannot express perfect independence, and a skewed workload can overload one stripe. Hash spreading, stripe count, placement, and resize generation need measurement and stability arguments.

Nonblocking designs are not an automatic successor. They can avoid lock-holder preemption but require precise atomic memory ordering, helping, ABA defense, and safe reclamation. A well-designed fine-grained lock can be easier to prove, operate, and port. The choice should follow required progress guarantees, platform primitives, workload, team review capacity, and evidence—not fashion.

## Failure Modes and Misconceptions

- **“One lock per node means node-local invariants.”** Reachability, order, height, color, count, and routing cross node boundaries. Derive guards from invariants.
- **“Disjoint keys never conflict.”** They may share a stripe, bucket, ancestor, allocator, resize generation, exact counter, or snapshot obligation.
- **“Acquire both locks in parameter order.”** Reversed operations can form a two-lock cycle. Normalize by stable identity/rank and deduplicate.
- **“Address order is always stable.”** Moving collectors, object reuse, cross-process representations, and lifetime gaps can invalidate the premise. State the platform/lifetime assumptions or choose durable IDs.
- **“Unlock current, then lock next is coupling.”** It creates an unprotected gap. Acquire substitute protection before release.
- **“The node lock prevents use-after-free.”** A stale traverser can hold only an address, not the mutex. Reclamation needs a separate guarantee.
- **“Validation is an assertion for debug builds.”** In optimistic designs it is part of production correctness; failure must retry or return according to the algorithm.
- **“A read lock means the code is read-only.”** Comparators, caches, reference counts, metrics, lazy initialization, and callbacks can write. Audit transitive behavior.
- **“Fine-grained locks make snapshots fast.”** Atomic snapshots may require all locks or a global/version protocol, becoming the widest operation.
- **“A fixed acquisition order proves liveness.”** It proves absence of one class of cycles under assumptions, not fairness, starvation freedom, livelock freedom, or deadlines.
- **“Try-lock makes deadlock impossible at no cost.”** Release-and-retry can livelock, waste work, and create unstable tails.
- **“More stripes always scale.”** Lock memory, false sharing, cache footprint, shared roots/counters, and workload skew can dominate.
- **“A concurrent library map behaves like a locked map.”** Retrieval, iterator, aggregate, and bulk semantics may be deliberately weaker or different. Read the contract.
- **“The race detector passed, so the algorithm is linearizable.”** Race freedom cannot detect wrong return histories, misplaced linearization points, logical removal errors, or unexercised schedules.
- **“The benchmark proves the design.”** Performance evidence covers only tested hardware, workload, runtime, and configuration; it cannot establish correctness.

## Worked Examples

### Example 1

**Situation.** A table has eight buckets and four fixed stripes, with bucket `b` guarded by stripe `b mod 4`. Updates target buckets 1 and 6.

**Reasoning.** Bucket 1 maps to stripe 1; bucket 6 maps to stripe 2. The updates have distinct exclusive guards and may overlap if they touch no global exact metadata. Buckets 1 and 5 would both map to stripe 1 and serialize even if their keys do not conflict abstractly. That is a false conflict introduced by bounded striping.

**Conclusion.** Striping provides bounded lock cost and partial overlap, not one-to-one independence.

### Example 2

**Situation.** Two threads execute atomic transfers `move(A,B)` and `move(B,A)`. The implementation locks source then destination.

**Reasoning.** The first can hold `LA` waiting for `LB`; the second can hold `LB` waiting for `LA`. The wait-for graph contains a cycle. Instead, compute both lock identities, acquire the smaller rank first, handle `LA = LB` with one acquisition, validate both objects, perform the move, and release in reverse.

**Conclusion.** Semantic argument roles must not determine multi-lock order; stable normalized rank prevents the two-lock cycle.

### Example 3

**Situation.** A sorted-list traversal holds node `p`, reads `c = p.next`, releases `p`, and then tries to acquire `c`.

**Reasoning.** Between release and acquisition, another operation can unlink and reclaim `c`, or replace `p.next`. The first thread may lock invalid storage or reason about a neighborhood that no longer exists. Correct pessimistic coupling acquires `c` while retaining `p`; an optimistic design requires a lifetime-safe reference plus later adjacency/mark validation.

**Conclusion.** Hand-over-hand locking overlaps acquisitions: protection is transferred before the old protection is released.

### Example 4

**Situation.** An optimistic list search finds predecessor 10 and current 20 for insertion of 15, then locks both. Meanwhile another thread inserted 12.

**Reasoning.** Merely owning locks on the old node objects does not prove they remain adjacent. Validation detects `pred.next != curr`; inserting 15 through the stale predecessor/current pair would unlink or bypass 12 depending on code. The operation releases and restarts. It has not yet linearized and must not have emitted an irreversible side effect.

**Conclusion.** Locks protect current objects; validation connects pre-lock observations to the current representation.

### Example 5

**Situation.** A per-bucket map protects every bucket correctly, but increments plain global `size` under only the chosen bucket lock.

**Reasoning.** Inserts in two buckets hold different locks and can perform conflicting read-modify-write sequences on `size`, losing an increment. Solutions include a global counter lock (which may become hot), an atomic counter with defined snapshot semantics, striped counters plus an approximate aggregate, or acquiring all regions for an exact snapshot. Each solution changes proof or performance.

**Conclusion.** Local bucket safety does not protect cross-bucket metadata; its semantics and guard must be explicit.

### Example 6

**Situation.** A balanced tree rotation locks pivot `x` and child `y` but not `x`'s parent `p` or the transferred subtree `β`.

**Reasoning.** The rotation changes `p`'s link, `x`/`y` child links, possibly `β`'s parent, and balance metadata; it may change root. A traversal through unprotected `p` can miss or duplicate reachability, and a concurrent change to `β` can violate parent/ordering invariants. The algorithm needs a documented neighborhood protocol, validation/versioning, or a wider structural lock.

**Conclusion.** Structural scope follows changed invariants, not the two nodes featured in the textbook rotation picture.

### Example 7

**Situation.** A hash table doubles its bucket array while key operations compute stripe from the current bucket index.

**Reasoning.** One operation can route with the old mask while another publishes the new array; without a generation protocol they can acquire unrelated locks for the same entry. Keeping lock stripe based on stable key hash can preserve conflict protection, but lookup still needs defined old/new migration states. Old array and lock storage cannot be reclaimed until prior users leave.

**Conclusion.** Resize requires coherent routing, migration, and lifetime rules; ordinary bucket locking is insufficient.

### Example 8

**Situation.** An atomic snapshot acquires all 64 stripes in ascending order, copies entries, then releases them.

**Reasoning.** The strict order avoids stripe cycles and the held set can define one snapshot instant, but the copy blocks every update and may allocate or invoke key/value operations. A stripe-at-a-time copy shortens blockage but is only weakly consistent. A versioned retry can preserve atomicity under assumptions but may starve during sustained writes.

**Conclusion.** Snapshot consistency is an API choice with direct granularity and liveness consequences.

### Example 9

**Situation.** Removing node `n` acquires predecessor and `n`, unlinks it, releases both, and immediately destroys `n.lock` and frees `n`.

**Reasoning.** A traverser may have read `n` earlier under an allowed optimistic read and be about to validate or acquire its lock. Unlink establishes abstract absence, not absence of references. A hazard, epoch, reference, RCU, or quiescence protocol must prove no such user remains before destruction/reuse.

**Conclusion.** Logical deletion, unlinking, and reclamation are distinct proof events.

### Example 10

**Situation.** A 32-stripe design is 1.7 times faster than a coarse lock in a uniform-key, write-heavy microbenchmark at 32 threads, but production has one key receiving 70% of traffic and frequent exact snapshots.

**Reasoning.** The experiment does not represent production conflict distribution or widest operation. The hot key serializes at one stripe, and snapshots acquire every stripe. Re-run with observed skew, operation mix, object size, snapshot frequency, hardware/NUMA placement, and report tails, waits, holds, retries, and cache effects. The coarse baseline may win or a special hot-key/sharded design may be required.

**Conclusion.** Granularity is validated against deployment-shaped workload evidence, not a favorable uniform benchmark.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** [CONPAR-018](../../04-programming-languages-concurrent-and-parallel-programming/modules/018-lock-ordering-and-deadlock-prevention.md) develops system-wide ordering and deadlock prevention; this module specializes those ideas to data-structure routing and invariants.
- **Software Engineering Patterns:** the [patterns roadmap](../../11-software-engineering-patterns/ROADMAP.md) treats ownership, coordination, and messaging as reusable design boundaries; fine granularity shows where any such design must be justified by invariants and evidence.
- **Database Engineering:** the [database roadmap](../../18-database-engineering/ROADMAP.md) applies lock granularity to records, pages, ranges, and transactions, adding logical lock managers and isolation semantics.
- **Operating Systems:** the [operating-systems roadmap](../../22-operating-systems/ROADMAP.md) supplies scheduler and primitive behavior; kernel lock-dependency tooling illustrates runtime checking of exercised lock orders.
- **Security Engineering:** concurrency defects can become use-after-free, corruption, or availability vulnerabilities; guard and reclamation proofs are part of attack-surface reduction.
- **Performance Engineering:** contention matrices, skew, tail latency, coherence, false sharing, and NUMA placement determine whether finer locking delivers useful scalability.

## References

1. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990, pp. 463–492. Primary definition and locality/composition foundation.
2. Steve Heller, Maurice Herlihy, Victor Luchangco, Mark Moir, William N. Scherer III, and Nir Shavit, [“A Lazy Concurrent List-Based Set Algorithm”](https://cs.brown.edu/~mph/HellerHLMSS05/2005-OPODIS-Lazy.pdf), OPODIS 2005. Primary comparison of coarse locking, lock coupling, optimistic locking, lazy synchronization, and nonblocking lists.
3. Oracle, [`java.util.concurrent.locks` package specification](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/package-summary.html), Java SE 26. Official support and intended use for hand-over-hand and lock-reordering disciplines.
4. Oracle, [`ReentrantReadWriteLock`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/ReentrantReadWriteLock.html), Java SE 26. Official mode, fairness, downgrading, and unsupported read-to-write upgrade behavior.
5. Oracle, [`ConcurrentHashMap`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html), Java SE 26. Official current retrieval, update, weak iterator, aggregate, and atomic-compute semantics.
6. The Open Group, [`pthread_mutex_lock`, `pthread_mutex_trylock`, `pthread_mutex_unlock`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html), POSIX.1-2024. Official ownership, recursive/error-checking/robust behavior and owner-death recovery contract.
7. Linux Kernel documentation, [Runtime locking correctness validator](https://www.kernel.org/doc/html/latest/locking/lockdep-design.html), accessed 2026-08-30. Official lock-class, dependency, nested-lock, and cycle-validation model.
8. SEI CERT C Coding Standard, [CON35-C: Avoid deadlock by locking in a predefined order](https://wiki.sei.cmu.edu/confluence/display/c/CON35-C.+Avoid+deadlock+by+locking+in+a+predefined+order), accessed 2026-08-30. Official engineering guidance for predefined multi-lock order.

## Exercises

### Exercise 1

Define guard map, lock striping, lock coupling, validation, linearization point, logical removal, physical unlinking, and reclamation. State why a node mutex does not by itself solve reclamation.

### Exercise 2

A striped map uses `stripe(k) = k mod 4`. Transaction `T1` atomically updates keys 6 and 1; `T2` updates keys 5 and 2. Derive the stripe set and acquisition sequence for both. Show why acquiring by caller key order can deadlock and why sorted, deduplicated stripe order cannot form a stripe-order cycle under the stated protocol.

### Exercise 3

Diagnose this optimistic sorted-list insertion: traverse without locks to obtain `pred` and `curr`; lock only `pred`; if `pred.key < x < curr.key`, set `pred.next = new(x, curr)`; unlock. Identify missing safety/linearizability obligations and propose a corrected lock/validation outline without assuming garbage collection solves algorithmic validity.

### Exercise 4

Design locking and API semantics for a resizable hash map that uses fixed stripes, supports `get`, `putIfAbsent`, exact `size`, weakly consistent iteration, and atomic two-key `move`. State the protected state, order, resize generation rule, linearization points, reclamation dependency, and expected bottlenecks.

### Exercise 5

A spatial index stores objects in tree regions. Most updates are geographically local, but an operation can migrate an object between distant regions and a query can request an atomic global snapshot. Propose a fine-grained design and an evidence plan. Explain when you would retain or restore a coarse lock instead.

## Answers to the Exercises

### Answer 1

A guard map assigns each representation region/invariant the lock set or protocol required for access. Lock striping hashes many logical regions onto a fixed smaller lock array. Lock coupling acquires the next node before releasing current protection. Validation rechecks that speculative observations still match protected current state. A linearization point is the proof event at which an operation takes abstract effect. Logical removal makes a node absent from the abstract object; unlinking removes normal reachability; reclamation permits destruction/reuse.

A mutex governs conforming acquisitions; it does not announce that no thread retains a raw/reference path to its containing node. A traverser can read a node before unlink and later access or acquire it. Therefore a lifetime mechanism—pin/reference, hazard pointer, epoch, RCU, ownership/quiescence, or equivalent—must prove the last possible user is gone before destroying node and lock.

### Answer 2

`T1` maps keys 6 and 1 to stripes `{2,1}`, so its normalized acquisition is `[1,2]`. `T2` maps keys 5 and 2 to `{1,2}`, also `[1,2]`. Caller order would make `T1` acquire 2 then request 1 while `T2` acquires 1 then requests 2, producing a cycle. Normalization makes both compete first for stripe 1; only its holder proceeds to stripe 2.

More generally every retained-to-requested edge increases stripe ID. A cycle would require a strict increasing chain returning to its starting ID, impossible. Deduplication matters when two keys share a stripe: acquiring the same nonreentrant lock twice can self-deadlock. The proof assumes no other locks/resources are acquired out of order and that stripe identity/generation remains stable while the operation runs.

### Answer 3

The algorithm does not protect or validate `curr`. After traversal, `pred` may be removed, `pred.next` may no longer be `curr`, `curr` may be removed/reclaimed, or a key between them may have been inserted. The inequality on stale object keys does not prove current adjacency. Locking only predecessor also may conflict with a remover whose protocol protects both nodes, and there is no stated lifetime mechanism for speculative references.

A corrected outline obtains memory-safe references under a pin/epoch/managed-reference rule, locks `pred` and `curr` in the algorithm's forward order, then validates that both are eligible/live and `pred.next is curr`. If validation fails, it releases and retries without side effects. If an equal key exists it returns false at a protected validated observation. Otherwise it privately initializes `new`, sets `new.next = curr`, and publishes via `pred.next = new`; that publication is the successful insertion's candidate linearization point. It restores invariants before reverse release and retires nodes only through the reclamation protocol.

### Answer 4

Use a table-generation object holding bucket array, fixed stable stripe array, routing metadata, resize state, and a lifetime reference/epoch. A key's spread hash selects a stable stripe; bucket selection additionally uses the acquired generation's mask. `get` follows declared synchronization—either the stripe lock or a separately proved atomic-read path. `putIfAbsent` locks its stripe, validates generation/routing, checks and publishes atomically. A two-key `move` computes/deduplicates stripe IDs, acquires ascending IDs, validates generation and both mappings, commits both effects, then releases reverse.

An exact `size` can use a dedicated counter lock/atomic counter whose update participates before operation response and whose read semantics are defined; this may be hot. Weak iteration may copy one stripe at a time and explicitly not represent one instant. Resize obtains an exclusive generation/resize protocol, publishes/migrates entries under defined stripe ownership, makes operations retry/help when generation changes, and retires the old array only after no users remain. Candidate points are protected entry publication/removal, the validated absence observation, the atomic two-key commit boundary defined by held stripes, and the exact counter read under its contract. Bottlenecks include the counter, hot stripes, resize coordination, hash skew, and wide two-key overlap.

### Answer 5

Partition the index by stable top-level regions, each with a lock or versioned subtree owner, while a short root/generation protocol protects routing. Local updates lock one region and validate its generation. Migration computes source/destination identities, deduplicates and acquires them in global region-rank order, validates object presence, capacity and routing, then atomically removes/adds while both locks are held. Tree splits/merges use a structural protocol covering parent routing and affected regions. Retired region objects survive through epoch/reference quiescence.

For an atomic global snapshot, acquire all region locks in rank order and copy immutable state, or use a global version with a proved retry/snapshot mechanism; document possible writer pause or retry starvation. Evidence includes guard/rank review, deterministic reversed migrations, split/migration/snapshot schedules, history linearizability checks, race and lock-dependency tools, cancellation/fault tests, and measurements under observed geographic skew with throughput, tail latency, waits/holds, retries, cache/NUMA effects, and snapshot frequency.

Retain or restore a coarse lock when the root/global snapshot dominates, migrations are common, region identity is unstable, reclamation cannot be made safe, the fine-grained proof is not reviewable, or deployment-shaped measurements do not beat the coarse implementation enough to justify complexity. Correct simplicity is the baseline, not a failure.
