---
module_id: DSE-063
program: Data Structures Engineering
level: 2
module_number: 63
title: Concurrent Hash Maps
status: complete
last_verified: 2026-08-30
---

# Concurrent Hash Maps

## One-Page Review

### Governing question

How can a hash map support overlapping lookup and update while preserving unique-key semantics, visibility, linearizability, collision invariants, coherent resize, safe lifetime, bounded resource behavior, and an API whose weak and strong observations are explicit?

### Essential definitions

- A **concurrent map** exposes map operations with a documented concurrent-history and memory-visibility contract.
- A **key-equivalence relation** determines whether two keys represent one mapping; equal keys must produce compatible hashes.
- A **bucket** is the collision-resolution region selected from a hash and table generation.
- A **stripe** is one of a fixed set of synchronization domains shared by one or more buckets.
- An **atomic conditional operation** combines observation and update, such as put-if-absent, compare-and-replace, or compare-and-delete.
- A **table generation** is one routing array plus its capacity, synchronization, migration, and lifetime state.
- **incremental resize** distributes migration across operations or helpers instead of stopping the whole map for one transfer.
- A **forwarding/migration marker** tells an operation how to continue when its old bucket has moved.
- A **weakly consistent iterator** tolerates concurrent updates but need not represent one instant or include every overlapping change.
- A **linearization point** is the proof event placing an operation in the legal sequential map history.
- A **hash-flooding attack** supplies many colliding keys to force long chains/probes, contention, or CPU exhaustion.

### Central model, mechanism, or theorem

For key `k` in generation `G`, routing computes `h = spread(hash(k))` and `bucket_G(h)`. A correct operation obtains memory-safe access to one coherent generation, follows its synchronization/migration protocol, compares only within locations permitted by collision resolution, and either observes or changes exactly one mapping under a justified linearization point. Conflicting operations on equivalent keys share an ordering mechanism even during resize. Publication makes initialized entries visible; deletion and old-generation retirement remain unreclaimed until no operation can reference them.

Incremental migration can preserve map semantics if each old bucket has a monotonic state, every key has one authoritative logical mapping, operations use that state to choose old/new ownership, transfer is idempotent or exclusively owned, and the old generation remains alive through quiescence. This is a conditional proof pattern—not evidence that any arbitrary “check both tables” implementation is correct.

### Critical invariants

1. Key equivalence is reflexive/symmetric/transitive for stored keys, and equivalent keys hash compatibly for the map's lifetime.
2. At most one live abstract mapping exists per equivalence class.
3. Every live entry is reachable through the routing/migration states allowed by one coherent generation protocol.
4. Reads never return an uninitialized, reclaimed, logically deleted, or mismatched key/value entry.
5. Put-if-absent, replace-if-equal, compute, and compare-delete combine their test and effect atomically.
6. Resize never loses an update, resurrects a removal, duplicates an abstract mapping, or frees old storage while reachable.
7. Entry, bucket, stripe, count, table-pointer, resize, and lifecycle state each have a documented guard/atomic rule.
8. Hash/equality/remapping callbacks obey concurrency, side-effect, recursion, exception, and duration contracts.
9. Iteration, size, bulk, clear, serialization, and snapshot advertise exact, weak, approximate, or quiescent semantics accurately.
10. Capacity, collision length, retries/help, callback work, retained generations, and per-key contention have operational limits and evidence.

### Common failures

- Wrapping `get` then `put` instead of exposing atomic put-if-absent or compute.
- Routing under one capacity and locking/mutating a bucket in another generation.
- Copying an old bucket while an update can land behind the migration scan.
- Publishing a new entry before its key, value, hash, and next/control fields are initialized.
- Treating a concurrent iterator or `size()` as an atomic snapshot without that contract.
- Calling slow, recursive, blocking, or side-effecting user code while a hot bin is protected.
- Removing an entry then immediately reusing its memory while readers can retain it.
- Accepting mutable keys whose hash/equality changes after insertion.
- Ignoring adversarial collisions because average lookup is expected constant time.
- Selecting a library by its type name while assuming unsupported whole-map transactions.

### Compact example

A bounded model begins with four buckets, publishes an eight-bucket generation, and migrates old buckets monotonically. Operations route to old storage until their old bucket is marked migrated and to new storage afterward. Keys inserted on either side of the boundary are transferred or placed in the new table exactly once. The executable checks ten square mappings and mid-resize lookups; it uses no threads or real memory-ordering primitive and proves only that finite state machine.

### Connections

[DSE-023](023-linear-probing.md), [DSE-024](024-quadratic-probing-and-double-hashing.md), and [DSE-027](027-hopscotch-hashing.md) supply collision layouts. [DSE-062](062-fine-grained-locking.md) supplies guard maps, ordered acquisition, validation, and reclamation obligations. The [program roadmap](../ROADMAP.md) proceeds to concurrent skip lists, lock-free stacks and queues, atomic primitives, reclamation, and history testing.

## Governing Question

Can a concurrent hash map provide precisely specified per-key and aggregate behavior while lookup, mutation, collision management, resize, callbacks, and reclamation overlap—and can its correctness and scaling claims be reproduced?

## Why This Matters

Concurrent maps sit in caches, registries, deduplication tables, schedulers, metrics systems, graph algorithms, compilers, runtimes, and request coordination. Their friendly key/value interface hides an unusually dense combination of concerns: hashing invokes user policy, collisions create shared hot regions, resizing changes routing for every key, deletion creates lifetime hazards, and aggregate views rarely compose naturally from per-key operations.

A synchronized sequential map can be fully linearizable with one lock. It is also one queue. A concurrent map tries to order only operations whose abstract effects conflict, often allowing retrievals to overlap updates. That can transform throughput, but only for workloads that distribute across keys/bins and do not constantly invoke whole-map behavior. One hot key, one colliding bucket, one global counter, or frequent resize can dominate.

The word “concurrent” does not determine semantics. Java's `ConcurrentHashMap` documents nonblocking retrieval, per-key happens-before for observed updates, weakly consistent iterators, limited usefulness of aggregate status during concurrent updates, and atomic remapping methods with restrictions. Go's `sync.Map` is specialized for write-once/read-many or disjoint-key patterns and explicitly recommends an ordinary typed map plus locking for many other cases. oneTBB distinguishes concurrent-safe operations from `clear`, `swap`, and rehash surfaces and uses accessors whose lifetime controls blocking. These are different contracts, not interchangeable implementations of a magical map.

The engineering lesson is to select the abstract contract first. Does `get` observe the latest completed write for its key? Is `size` exact at a point, eventually accurate, or only useful when quiescent? Does iteration show a snapshot? May `compute` invoke a function more than once? Can a callback recursively update the map? Can a two-key transfer be atomic? Does `clear` overlap operations? Answers determine architecture and proof.

Hash maps also face algorithmic denial of service. Expected `O(1)` assumes a hash distribution model. Attackers or accidental skew can concentrate work and contention. Randomized keyed hashing, collision-tree conversion, per-tenant quotas, size limits, deadlines, admission control, and telemetry are operational defenses; none excuses an unspecified worst case.

## Prerequisites and Retrieval

Retrieve hash functions, equality relations, separate chaining, open addressing, load factors, tombstones, linear probing, double hashing, hopscotch neighborhoods, amortized resize, sequential map specifications, representation invariants, locks, atomics, memory visibility, linearizability, and latency distributions. From [DSE-002](002-representation-invariants.md), retrieve abstraction ownership. From [DSE-062](062-fine-grained-locking.md), retrieve guard maps, stripes, validation, generations, ordered acquisition, and separation of logical deletion from reclamation.

You should be able to state why equivalent keys must hash identically, why a mutable key breaks reachability, why expected constant time depends on distribution/load, and why successful publication requires target-language ordering. From [DSE-029](029-hash-flooding-resistance.md), retrieve adversarial collision reasoning. Retrieve API-level histories with invocation and response events and understand that per-key linearizability does not automatically create multi-key transactions or atomic snapshots.

## Learning Objectives

After completing this module, you can:

1. specify concurrent map operations, consistency, visibility, callbacks, and lifecycle;
2. derive invariants for chained, striped, open-addressed, hopscotch, and split-ordered designs;
3. identify linearization points for lookup and conditional update outcomes;
4. design a coherent stop-the-world or incremental resize protocol;
5. distinguish exact, approximate, weakly consistent, and quiescent aggregate behavior;
6. reason about publication, deletion, ABA, and old-generation reclamation;
7. audit hash, equality, and remapping callbacks for reentrancy and side effects;
8. defend against hot keys, collision flooding, unbounded growth, and expensive values;
9. compare coarse, striped, fine-locked, optimistic, and nonblocking architectures; and
10. build layered correctness, fault, security, and workload evidence.

## Core Exposition

**Specify a concurrent map, not merely a thread-safe dictionary.** Let abstract state be a finite partial function `M: K ⇀ V` over key equivalence `≈`. Define at least:

- `get(k)` returns the current associated value or absence;
- `put(k,v)` installs `v` and defines its prior-value result;
- `putIfAbsent(k,v)` tests and inserts as one operation;
- `remove(k)` and `remove(k, expected)` distinguish unconditional and conditional deletion;
- `replace(k, old, new)`, `compute`, and merge define callback invocation and failure;
- `size`, iteration, bulk operations, snapshot, clear, close, and serialization state their concurrency semantics.

Define null/absence representation, key/value ownership, comparison exceptions, mutation of stored values, iterator update support, and timeout/cancellation. If callers need an atomic transfer between keys, per-key methods do not suffice; expose a wider transaction/protocol or state that it is unsupported.

**Hash and equivalence are part of correctness.** For stored lifetime, `a ≈ b` must imply compatible hashes. Hash and equality should be stable, deterministic within the map's required scope, and safe to invoke under the selected synchronization. A mutable key that changes hash can become unreachable in its old bucket and appear absent while still stored. A nontransitive comparator can create duplicate equivalence classes.

Hash and equality are executable callbacks. They may throw, block, allocate, acquire locks, recurse into the map, mutate keys, or consume adversarial time. Compute hash before acquiring an internal stripe only when the key can be safely accessed and the routing algorithm permits it. Cache a stored entry's spread hash when useful, but ensure it matches the equality contract. Never hold internal locks across arbitrary callbacks without a declared, audited contract.

**Choose a collision architecture.** Separate chaining stores a list/tree/array per bucket. It makes bucket ownership visible and deletion straightforward, but pointer chasing and per-entry allocation affect locality and reclamation. A striped chained baseline is often durable: stable stripes protect multiple buckets, and multi-key operations normalize stripe order. Hot bins remain hot.

Open addressing keeps entries in a dense array, improving locality, but a key's probe sequence spans slots. Concurrent insertion must claim slots and publish metadata/value safely; deletion uses tombstones, backward shifting, versions, or rebuild rules without breaking other searches. A lock per nominal home bucket may not protect a probe that crosses regions. Hopscotch hashing keeps an entry within a bounded neighborhood of its home and maintains neighborhood metadata; concurrent relocation must update all involved slots/bitmaps with a correct locking or atomic protocol.

Cuckoo-style tables give multiple candidate homes and relocate paths. Concurrent displacement crosses bins and can form lock-order or validation complexity. Split-ordered lists keep items in one ordered list and change bucket-directory interpretation rather than physically moving all items at resize; their nonblocking benefits depend on a correct list algorithm, atomics, and reclamation. These are architectures with different proof and hardware costs, not plug-compatible collision policies.

**Derive the guard and publication rules.** A striped chained map might state:

| State | Protection/publication |
|---|---|
| Bucket link structure | exclusive stripe for that bucket generation |
| Immutable entry key/hash | initialize privately before link publication |
| Mutable value | stripe, per-entry accessor lock, or atomic/versioned cell |
| Table pointer/capacity | generation lock or acquire/release publication protocol |
| Migration state | resize protocol plus bucket/stripe ownership |
| Exact count | atomic counter or dedicated compositional guard |
| Retired entries/generations | reference, epoch, hazard, RCU, or quiescence protocol |
| Closed/configuration state | lifecycle/configuration guard with entrant protocol |

Publishing a node link before key/value initialization lets a racing reader observe partial state. Initialize unreachable storage, then publish with the release action required by the language; readers use the corresponding acquire/lock relation before dereferencing. Plain pointer coherence is not a language-level proof.

**Place per-operation linearization points.** Under a bucket lock, successful `putIfAbsent` can linearize at publication of the new entry; failure can linearize at the protected observation of an equivalent live key. Replacement linearizes at the protected/atomic value change; compare-replace failure at the observation showing mismatch or absence. Removal can linearize at logical marking or unlink, depending on concurrent readers and the specified algorithm.

A lock-free/optimistic retrieval may traverse several states. Its point is not “somewhere during get” by assertion: identify the load/validation that proves the returned mapping existed, or show a legal point for absence across resize. If it sees a forwarding marker, follows the new generation, and returns a value, the proof must connect that path to one authoritative mapping.

Real-time order matters. If `put(k,v)` returns before a later `get(k)` begins, a linearizable map cannot return the replaced prior value. Java's official map contract additionally documents the synchronization relation for an observed update. Other libraries may specify different visibility language; consult the actual version contract.

**Conditional APIs close composition gaps.** `if get(k) is absent: put(k,v)` allows two callers to observe absence and both perform work. `putIfAbsent` orders test and insertion. Cache loading often needs stronger semantics: should one loader run, may several compute with one winner, are failures cached, can the loader call the map, and what happens on timeout? A map method cannot promise exactly-once external side effects merely by serializing final association.

Remapping callbacks are particularly dangerous. Java documents that atomic compute may block competing updates and requires the function to be short/simple and not modify the same map. Go's `LoadOrStore` accepts a precomputed value and has different work-duplication implications. Design APIs around replayability and lock scope. If computation runs outside protection, use version/compare commit and accept retries; keep irreversible effects idempotent or separate.

**Resize is a distributed state transition.** A simple correct baseline acquires every stripe in global order, allocates/transfers, publishes the new table, then releases. It pauses map operations and may have long tails, but its proof is reviewable. Allocation and hashing/comparison should be staged carefully so failure leaves the old map valid.

Incremental resize divides work. A generation `G_old` points or transitions to `G_new`. Each old bucket has a state such as `unmigrated`, `moving`, or `migrated`. An operation encountering migration may help, wait, retry, or route according to state. The design must answer:

1. Who exclusively owns transfer of an old bucket, or how is transfer idempotent?
2. Where do updates land before, during, and after the migration marker?
3. What publication order prevents an update behind the transfer scan?
4. How does lookup avoid false absence while ownership changes?
5. When is the new table globally current?
6. Who completes abandoned migration after cancellation or thread failure?
7. When can old buckets, locks, and generation metadata be reclaimed?

One safe lock-based pattern takes the old bucket's stable stripe, transfers all entries to new destinations under the required new protection, marks the old bucket migrated, then releases. Operations lock/recheck the old-bucket marker; before the mark they mutate old, afterward they route new. Multi-stripe transfer must follow an order or stage private lists to avoid cycles. This pattern still needs exact handling of failures and a generation lifetime pin.

Copy-then-publish without excluding updates can lose a write that lands after copying but before the marker. Searching both tables may avoid some false absence but can expose duplicate values, resurrect deletions, or make conditional operations non-atomic. “Look in both” is not a migration protocol.

The executable artifact models a deliberately simpler ownership rule. One operation owns each old-bucket migration; a per-bucket monotonic marker determines whether puts/gets use old or new storage. It demonstrates finite state transitions, not real concurrent execution.

<!-- bijux-verify: {"id":"incremental-resize-state-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"old_buckets=4\nnew_buckets=8\nmigrated_buckets=4\nkeys=0,1,2,3,4,5,6,7,8,9\nsum_values=285\nlookups_during_resize=16,36\nold_entries=0\nnew_occupied_buckets=8\nall_invariants=True\nevidence=finite_incremental_resize_model\n","stderr":""}} -->
```python
class IncrementalResizeModel:
    def __init__(self, bucket_count):
        self.old = [{} for _ in range(bucket_count)]
        self.new = None
        self.migrated = [False] * bucket_count

    def put(self, key, value):
        old_index = key % len(self.old)
        if self.new is not None and self.migrated[old_index]:
            self.new[key % len(self.new)][key] = value
        else:
            self.old[old_index][key] = value

    def get(self, key):
        old_index = key % len(self.old)
        if self.new is not None and self.migrated[old_index]:
            return self.new[key % len(self.new)].get(key)
        return self.old[old_index].get(key)

    def begin_resize(self, new_bucket_count):
        assert self.new is None
        self.new = [{} for _ in range(new_bucket_count)]

    def migrate(self, old_index):
        assert self.new is not None
        if self.migrated[old_index]:
            return
        for key, value in list(self.old[old_index].items()):
            self.new[key % len(self.new)][key] = value
        self.old[old_index].clear()
        self.migrated[old_index] = True

    def snapshot(self):
        result = {}
        for bucket in self.old:
            result.update(bucket)
        if self.new is not None:
            for bucket in self.new:
                result.update(bucket)
        return result


model = IncrementalResizeModel(4)
for key in range(8):
    model.put(key, key * key)

model.begin_resize(8)
model.migrate(0)
during_first = model.get(4)
model.put(8, 64)
model.migrate(2)
during_second = model.get(6)
model.put(9, 81)
model.migrate(1)
model.migrate(3)

state = model.snapshot()
old_entries = sum(len(bucket) for bucket in model.old)
occupied_new = sum(bool(bucket) for bucket in model.new)
all_invariants = (
    sorted(state) == list(range(10))
    and sum(state.values()) == 285
    and all(model.migrated)
    and old_entries == 0
    and during_first == 16
    and during_second == 36
)

print(f"old_buckets={len(model.old)}")
print(f"new_buckets={len(model.new)}")
print(f"migrated_buckets={sum(model.migrated)}")
print("keys=" + ",".join(str(key) for key in sorted(state)))
print(f"sum_values={sum(state.values())}")
print(f"lookups_during_resize={during_first},{during_second}")
print(f"old_entries={old_entries}")
print(f"new_occupied_buckets={occupied_new}")
print(f"all_invariants={all_invariants}")
print("evidence=finite_incremental_resize_model")
```

The exact output proves the assertions for this deterministic state machine. It does not run threads, implement locks/atomics, allow a migration/update interleaving inside one method, use arbitrary hashes/equality, simulate failure, establish memory visibility, prove arbitrary schedules, or measure performance.

**Deletion requires lifetime discipline.** In chaining, logical deletion/unlink may occur under a bucket guard while a lock-free reader still holds an entry pointer. In open addressing, reuse of a slot/version can create ABA-like confusion. Managed memory can prevent physical deallocation but not stale semantic observations. Native implementations require epoch, hazard, reference-count, RCU, or another scheme matched to reads. Old table generations require the same treatment.

Values also have ownership semantics. Returning a mutable value reference may outlive map protection. Options include immutable/thread-safe values, defensive copies, accessor/guard objects whose lifetime retains protection, atomically replaceable immutable cells, or an explicit contract that map safety covers association topology only. oneTBB accessors make the protection lifetime visible and warn that long lifetimes block others.

**Aggregate operations are not free composition.** A concurrent map may maintain an exact atomic count for completed updates, but reading count concurrently with multiple updates need not yield a snapshot consistent with a later iteration. Striped counters reduce contention while returning an estimate or a sum sampled over time. Java documents aggregate status as generally useful only without concurrent updates; Go `Range` does not promise a consistent snapshot.

Weak iteration can visit entries reflecting different moments while guaranteeing each yielded entry was valid under specified conditions. It must not crash, duplicate beyond contract, or follow freed storage. Atomic snapshots require freezing all regions, persistent/versioned state, multi-version techniques, or validated retry. `clear` can be a wide lifecycle transition rather than many independent removes; library documentation may classify it as unsafe for concurrent use.

**Progress and capacity are part of operations.** A map that grows without bound can exhaust memory. Define maximum entries/bytes, resize threshold, maximum capacity, allocation-failure behavior, and backpressure/eviction ownership. Eviction introduces a policy structure and callbacks that must compose with map locks; do not hide it inside a remapping callback.

Hot-key contention is abstractly unavoidable for atomic updates to one value, though techniques such as sharded counters can weaken semantics for aggregation. Hash flooding turns many distinct keys into one collision domain. Tree bins can bound comparison depth when keys support a safe order; keyed random hashing makes chosen collisions harder; per-request work limits and telemetry contain damage. Hash randomization is a defense under a threat model, not a replacement for capacity control.

**Evidence must span correctness and workload.** Start with sequential differential tests against a simple map. Check key uniqueness, reachability, bucket/probe metadata, count, and generation invariants. Use deterministic schedules around same-key conditional updates, collision chains, migration markers, delete/read, resize/clear/close, and callback exceptions. Record histories for linearizability checking. Use race/memory tools and lock-dependency analysis within scope; inject allocation/cancellation faults; force tiny capacities and deliberately colliding keys.

Benchmark against a coarse locked map and relevant library implementation with identical semantics. Vary readers/writers, hit/miss, key skew, collision distribution, table size/load, value size, resize rate, callback cost, thread count, CPU topology, and memory allocator. Report throughput and tails plus per-bin/stripe waits, retries/CAS failures, migration help, retained generations, chain/probe distribution, allocations, cache misses, and memory. A concurrent map is successful when the required contract is correct and its deployment-shaped evidence justifies complexity.

## Definitions and Notation

Let `K` be keys, `V` values, `≈` a key-equivalence relation, and abstract map `M: K/≈ ⇀ V`. For stored keys, `k1 ≈ k2` requires compatible hash output. A map operation history uses invocation/response events; `op1 <H op2` when the first returns before the second begins.

Let raw hash be `hash(k)` and mixed/spread value `h(k)`. In generation `G` with capacity `m_G`, routing `b_G(k)` selects a bucket/probe home. For power-of-two tables it is often a mask of spread bits; the precise scheme is implementation policy. Load factor is `α = n/m`, with `n` live mappings and `m` primary bucket/slot capacity. Expected costs assume a distribution/probing model and controlled `α`.

A **live entry** represents one abstract mapping. A **tombstone** preserves an open-addressing search path after deletion. A **forwarding marker** redirects an operation from an old bucket/generation. A **generation pin** is a reference/epoch/read-side state preventing reclamation while an operation can use `G`.

For old bucket `i`, migration state `μ_i` may be `U` (unmigrated), `X` (owned/in progress), or `M` (migrated). A correct protocol defines authoritative lookup/update location for every state and makes allowed transitions monotonic. The bounded model collapses `X` into an indivisible method and uses only `U→M`; production concurrency cannot assume that indivisibility without a lock/atomic mechanism.

An operation **linearizes** at event `lp(op)` between its invocation and response. A map is linearizable when calls can be arranged into a legal sequential map history preserving `<H`. **Weak consistency** is a separate, API-defined condition, not “almost linearizable.”

For evidence, let `T(p)` be throughput at concurrency `p`, `X_q` the `q`th percentile end-to-end latency, `W_s` wait for stripe/bin `s`, `H_s` hold time, `F` failed retries/CAS, `D` collision depth/probe length, and `G_r` retained generations. Measurements are observations under named conditions, never semantic proofs.

## Mechanisms, Invariants, or Proof Structure

### Map-operation proof template

1. Pin/read one coherent table generation with target-language synchronization.
2. Compute hash/equality safely and route according to that generation.
3. Acquire or atomically validate the collision region and any migration state.
4. Establish presence, absence, or expected-value predicate over equivalent keys.
5. Perform no effect for failure, or publish exactly one initialized change for success.
6. Identify the operation-specific linearization event.
7. Restore collision, count, routing, and lifecycle invariants before release.
8. Retire removed/replaced storage only through the reclamation protocol.
9. Release pins/locks on success, exception, retry, timeout, and cancellation.

### Resize proof obligations

1. New generation construction is private and failure-safe before publication.
2. Each old bucket has one authoritative monotonic migration state.
3. Transfer and updates cannot pass each other unobserved.
4. Lookup checks the authoritative location and cannot return false absence across handoff.
5. Conditional operations see one atomic key state across handoff.
6. Each equivalence class has at most one live abstract mapping, even if physical forwarding/copies coexist.
7. Count and capacity thresholds are changed exactly as specified, not once per physical copy.
8. Helpers can complete abandoned work or the owner-failure policy is explicit.
9. Old generation is reclaimed only after every potential user is quiescent.

### Security and resource invariants

Capacity and total retained bytes are bounded or governed by admission/eviction. Per-operation collision/probe/help/callback work is bounded, metered, interruptible, or protected by deadlines appropriate to its context. Hash seeds and sensitive keys are not leaked through diagnostics. Authorization decisions are not cached past their invalidation contract. Tenant/key namespaces prevent one principal from exhausting another's map budget where isolation is required.

### Verification ladder

1. Sequential specification, hash/equality laws, and differential tests.
2. Representation checks for uniqueness, reachability, probes/chains, counts, and generations.
3. Controlled same-key, collision, callback, migration, deletion, clear, and shutdown schedules.
4. Bounded/exhaustive history checking and linearizability analysis.
5. Race, memory, sanitizer, and lock-order tools for supported executions.
6. Allocation/callback/cancellation/owner-failure and reclamation fault tests.
7. Adversarial collisions, hot keys, capacity pressure, and tenant isolation tests.
8. Production-shaped throughput, tails, contention, retries, migration, cache, allocator, and retained-memory measurement.

Each rung answers different questions. Correct final contents do not validate return histories; race freedom does not validate resize semantics; a linearizability checker does not prove memory safety; a uniform benchmark does not cover malicious collisions or production skew.

## Alternatives and Trade-Offs

| Architecture | Read/update overlap | Resize strategy | Principal trade-off |
|---|---|---|---|
| Coarse locked sequential map | none inside map | exclusive rebuild | simplest complete proof |
| Striped chained map | across stripes; mode-dependent reads | all-stripe or incremental bins | false conflicts, pointers, hot bins |
| Per-bucket/node locked chaining | across fine regions | ordered/global/generation protocol | many locks and reclamation |
| Concurrent open addressing | across slots/probe regions | rebuild/generation migration | locality versus relocation/tombstone proof |
| Hopscotch map | bounded neighborhoods | coordinated rebuild | locality and bounded search; relocation metadata |
| Cuckoo-style concurrent map | candidate-bin overlap | rebuild or multi-generation | relocation paths and cycles/retries |
| Split-ordered list | nonblocking algorithm-dependent | directory growth without moving items | list/atomic/reclamation complexity |
| Copy-on-write/persistent map | reads on immutable snapshot | publish new root/table | update allocation and reclamation |
| Actor-owned map | requests serialized by owner | owner rebuild | queue/backpressure; simple ownership |
| Sharded maps | parallel independent maps | per-shard plus directory | no native whole-map atomicity |

Choose libraries by semantics and workload. Java `ConcurrentHashMap` is strong for many general per-key operations but deliberately does not offer a whole-table exclusion lock. Go `sync.Map` is specialized and untyped at its API boundary; an ordinary typed map plus mutex often better owns related invariants. oneTBB accessors can keep element protection across user code, which is powerful but makes accessor lifetime a blocking concern.

Sharding above the map can be simpler than an intricate internal algorithm. Each shard owns a conventional map and lock; keys route stably; multi-key operations order shard locks. The cost is false conflicts, shard skew, rebalancing, and aggregate semantics. This is often a useful baseline.

Lock-free does not mean wait-free, memory-free, callback-safe, or faster. Nonblocking tables require atomics, memory ordering, ABA handling, and reclamation; resize is especially demanding. Adopt one only when required progress or measured workload benefit justifies proof/maintenance cost and a mature implementation matches the platform.

## Failure Modes and Misconceptions

- **“Concurrent means every method can overlap.”** Constructors, destructors, clear, swap, rehash, bulk functions, or iterators may have different rules.
- **“Thread-safe calls compose.”** `get` plus `put`, or two per-key changes, is not an atomic compound action.
- **“Equivalent keys are a sequential detail.”** Inconsistent or mutable hash/equality breaks concurrent uniqueness and routing too.
- **“Lock the home bucket.”** Open-addressing probes/relocations and resize may cross that protection domain.
- **“Readers need no synchronization because entries are immutable.”** Readers still need safe publication, current routing, deletion handling, and lifetime.
- **“Search old and new during resize.”** Without authoritative ownership it can miss, duplicate, resurrect, or violate conditional atomicity.
- **“Copied means migrated.”** An update can land after copying; the handoff/marker order is the critical protocol.
- **“Garbage collection solves deletion.”** It may preserve memory but not current reachability, marks, duplicate mappings, or value semantics.
- **“Atomic size is an atomic snapshot.”** A count can be exact for updates while not correspond to a concurrent traversal's mixed-time view.
- **“Weak iterator means anything is allowed.”** The library still owes its documented safety, duplication, visibility, and lifetime guarantees.
- **“Compute is a convenient place for I/O.”** It can hold a hot bin, block competitors, recurse, fail, or repeat depending on contract.
- **“Expected O(1) prevents denial of service.”** Chosen collisions, hot keys, expensive equality, growth, and allocator pressure violate average assumptions.
- **“More concurrency level/stripes guarantees scale.”** Routing skew, shared counts, resize, cache coherence, and hardware topology determine results.
- **“A race detector proves the map.”** It cannot prove legal histories, absence semantics, migration correctness, liveness, or unsupported paths.
- **“One benchmark selects the best map.”** API strength, key lifecycle, workload mix, tails, capacity, failure, and operational evidence all matter.

## Worked Examples

### Example 1

**Situation.** Two workers implement cache insertion as `v=get(k); if absent: put(k,build())`.

**Reasoning.** Both can observe absence, both run `build`, and the later `put` replaces or loses against the first. Individual calls may be linearizable. `putIfAbsent` makes association atomic but may still allow duplicated precomputation. A single-loader API needs a placeholder/future or atomic compute contract, including failure/cancellation and callback restrictions.

**Conclusion.** Atomic association and exactly-once computation are different requirements.

### Example 2

**Situation.** A striped chained table has 16 stripes and 256 buckets. An attacker supplies keys all mapping to bucket 7.

**Reasoning.** Every operation reaches one collision chain and stripe, so potential cross-stripe concurrency is irrelevant. Chain work can become linear unless tree/bounds defenses apply, and lock hold grows with comparisons. Keyed hashing may frustrate chosen collisions; capacity/work quotas and metrics remain necessary.

**Conclusion.** Collision distribution controls both algorithmic work and synchronization contention.

### Example 3

**Situation.** Key object `q` hashes from a mutable username. After insertion, code changes that field.

**Reasoning.** Lookup computes a new bucket while the physical entry remains under the old hash. An equal freshly constructed key may not find it, and a second mapping can be inserted. Locks cannot repair a violated stable-key premise.

**Conclusion.** Stored key equivalence/hash state must be immutable or owned/frozen for its map lifetime.

### Example 4

**Situation.** Resize copies old bucket 2, then before marking it migrated a writer inserts key `x` into old bucket 2; the resizer marks and routes future readers new.

**Reasoning.** `x` was behind the copy frontier and is absent from new. Future lookup follows the marker and falsely returns absence. Holding/owning the old bucket through copy and marker, or using an atomic forwarding/help protocol, orders the write before transfer or forces it into new.

**Conclusion.** The migration handoff must close the copy/update race.

### Example 5

**Situation.** During migration, an implementation keeps physical copies in both generations and increments exact size for each new-table insertion.

**Reasoning.** Migration changes representation, not abstract membership. Incrementing for a physical copy double-counts. The count changes only at abstract insertion/removal linearization points; transfer preserves it. Lookup/conditional updates also need one authoritative logical version.

**Conclusion.** Physical duplication during a protocol must not become abstract duplication.

### Example 6

**Situation.** `compute(k,f)` invokes `f` while protecting key `k`; `f` recursively calls `compute(k,g)`.

**Reasoning.** A nonreentrant guard self-deadlocks; reentrancy can expose an intermediate placeholder or produce recursive-update exceptions/undefined semantics. Running `f` outside protection permits interference and retry, so effects may repeat. The API must constrain recursion and side effects rather than silently choose.

**Conclusion.** Remapping callback semantics are part of the concurrent map contract.

### Example 7

**Situation.** A monitoring endpoint reports `size=100`, then iterates 99 entries while updates run.

**Reasoning.** An exact atomic count read and a weak iterator can each satisfy their contracts at different instants. Their combination is not an atomic snapshot. The endpoint should label approximate/live data, quiesce, or request a real snapshot mechanism.

**Conclusion.** Individually valid aggregate observations do not compose into one map state.

### Example 8

**Situation.** A lock-free reader loads entry pointer `e`; a remover unlinks/frees it; allocator reuses the address for another entry before the reader validates.

**Reasoning.** Pointer equality may appear unchanged while identity/content changed—an ABA/use-after-free hazard. Logical CAS correctness needs a version/tag or algorithmic defense, and physical access needs hazard/epoch/reference/RCU reclamation.

**Conclusion.** Atomic link updates and safe reclamation are separate obligations.

### Example 9

**Situation.** A oneTBB accessor remains in an outer scope while the owner performs network I/O.

**Reasoning.** The accessor retains update access; other operations on that key block for the I/O duration. Narrow the accessor scope, copy required state, release, perform I/O, then conditionally commit with version semantics if needed. The second design may conflict/retry and must define it.

**Conclusion.** User-visible guard lifetime can turn application work into map contention.

### Example 10

**Situation.** Map A wins a uniform 90%-read benchmark, while service traffic is 40% writes, Zipf-skewed, includes periodic clear/snapshot, and stores 4 KiB values.

**Reasoning.** The benchmark omits hot-key serialization, allocator/cache footprint, wide operations, and realistic mutation. Reproduce hit/miss, skew, sizes, resize, callbacks, CPU topology, and deadlines; compare equal semantics and measure tails, waits, probes, migration, memory, and retained generations.

**Conclusion.** Concurrent-map selection is a contract-and-workload experiment, not a universal leaderboard.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** [CONPAR-023](../../04-programming-languages-concurrent-and-parallel-programming/modules/023-happens-before-relations.md) supplies visibility ordering, while the program's atomic and nonblocking modules supply progress tools.
- **Software Engineering Patterns:** the [patterns roadmap](../../11-software-engineering-patterns/ROADMAP.md) helps separate cache, registry, sharding, proxy, and coordination responsibilities from the container mechanism.
- **Database Engineering:** the [database roadmap](../../18-database-engineering/ROADMAP.md) develops hash indexes, buffer/concurrency control, and transactional multi-record semantics beyond per-key map atomicity.
- **Security Engineering:** adversarial hashing, capacity exhaustion, callback amplification, tenant isolation, and stale authorization caches make map policy part of security design.
- **Performance Engineering:** collision/probe distributions, key skew, cache locality, allocation, coherence, NUMA, throughput, and tails determine useful scalability.
- **Distributed Systems:** an in-process linearizable map does not provide distributed consensus, durability, replication, or exactly-once effects; those require separate protocols.

## References

1. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990. Primary correctness definition and locality/composition basis.
2. Oracle, [`ConcurrentHashMap`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html), Java SE 26. Official retrieval, update, aggregate, iterator, bulk, and remapping semantics.
3. Oracle, [`ConcurrentMap`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/ConcurrentMap.html), Java SE 26. Official atomic conditional-operation interface contract.
4. The Go Project, [`sync.Map`](https://pkg.go.dev/sync#Map), accessed 2026-08-30. Official specialization guidance, operation semantics, and synchronizes-before contract.
5. UXL Foundation, [oneTBB `concurrent_hash_map` specification](https://uxlfoundation.github.io/oneTBB/main/specification/source/containers/concurrent_hash_map_cls.html), accessed 2026-08-30. Official safe/unsafe surfaces and accessor-based container contract.
6. Ori Shalev and Nir Shavit, [“Split-Ordered Lists: Lock-Free Extensible Hash Tables”](https://people.csail.mit.edu/shanir/publications/Split-Ordered_Lists.pdf), *Journal of the ACM* 53(3), 2006, pp. 379–405. Primary nonblocking extensible-table design.
7. Maurice Herlihy, Nir Shavit, and Moran Tzafrir, [“Hopscotch Hashing”](https://people.csail.mit.edu/shanir/publications/disc2008_submission_98.pdf), DISC 2008. Primary concurrent neighborhood/open-addressing design.
8. Python Software Foundation, [PEP 456 — Secure and interchangeable hash algorithm](https://peps.python.org/pep-0456/), 2013. Official threat analysis and keyed-hash design rationale for collision attacks.

## Exercises

### Exercise 1

Define key equivalence, bucket, stripe, table generation, atomic conditional operation, forwarding marker, weakly consistent iterator, logical deletion, and reclamation. Explain why per-key linearizability does not provide an atomic two-key transfer.

### Exercise 2

A four-bucket map grows to eight. Keys use identity hash. Old bucket 1 contains keys 1, 5, and 9. Under the module's simplified locked migration pattern, trace transfer, marker publication, a concurrent `put(13,v)`, and subsequent lookups for each possible ordering of the put relative to bucket ownership. State the required invariant.

### Exercise 3

Diagnose a chained map whose `putIfAbsent` performs an unlocked lookup, allocates a node, acquires a stripe, and inserts without rechecking. Include duplicate computation, uniqueness, publication, exceptions, and reclamation. Give a corrected outline.

### Exercise 4

Specify an API and architecture for a multi-tenant request-deduplication map. It needs one in-flight computation per tenant/request ID, bounded memory, expiry, cancellation, and safe result sharing. State what the map guarantees and what it cannot guarantee about external side effects.

### Exercise 5

You must choose among a coarse locked typed map, stable striped map, Go `sync.Map`, Java `ConcurrentHashMap`, and a nonblocking custom table for a new service. Construct a decision/evidence protocol that prevents a benchmark-only choice and includes a rollback criterion.

## Answers to the Exercises

### Answer 1

Key equivalence defines which keys denote one association; equivalent keys require compatible hashes. A bucket is a collision region selected by hash/generation. A stripe is a stable lock domain shared by buckets. A generation is a routing table plus capacity, migration, synchronization, and lifetime state. Atomic conditional operations combine observation and effect. A forwarding marker redirects operations after migration. A weak iterator tolerates overlap under specified non-snapshot semantics. Logical deletion removes abstract membership; reclamation permits physical reuse/destruction.

Per-key linearizability orders operations that affect each key, but a transfer requires one indivisible relationship across source and destination. Another operation can observe after source removal and before destination insertion unless a two-key protocol locks/orders both domains or uses a transaction. Two legal per-key histories can therefore violate the desired cross-key invariant.

### Answer 2

All old keys satisfy modulo 4 equals 1; in the new table they route to buckets 1 (`1,9`) and 5 (`5`). Migration acquires old bucket/stripe ownership, transfers all current entries under required new protection, publishes the monotonic migrated marker, then releases. If `put(13,v)` acquires before migration ownership, it inserts in old bucket 1 and the transfer includes it, routing to new bucket 5. If it waits and observes the published marker after ownership, it inserts directly in new bucket 5. It cannot legally insert into old after the transfer scan and escape before the marker.

Subsequent lookups observe marker and route new: 1/9 in new bucket 1 and 5/13 in new bucket 5. The invariant is that the ownership/marker boundary totally orders old-bucket updates with transfer: every update is either included in transfer or routed to new, never neither or abstractly both. Old storage remains pinned until pre-marker users leave.

### Answer 3

Two callers can both see absence and allocate; without recheck both can link equivalent keys, violating uniqueness. Even if collision code happens to replace one, both computations/allocations occur and return semantics can be wrong. A node must be privately initialized before release publication. Hash/equality/allocation exceptions must leave no lock or partial link. A losing/unlinked node and replaced node need safe ownership/reclamation.

Correctly compute a stable hash and allocate/initialize a candidate outside the stripe when safe. Acquire the current generation/stripe, validate generation routing, and search again under protection. If present, return its value/status and dispose/retire the unused candidate safely. If absent, publish exactly one initialized node; publication is the success linearization point, while protected presence observation is the failure point. Restore count/collision invariants, release on every exit, and retry on generation change without repeating irreversible external effects.

### Answer 4

Partition by tenant and request ID with stable hashing and capacity accounting per tenant/global. Store immutable entry states such as `in_flight(future, owner, deadline, generation)`, `succeeded(result, expiry)`, or `failed(policy, expiry)`. An atomic put-if-absent elects one owner; followers receive the same future. Completion conditionally replaces the exact in-flight generation, preventing a late owner from overwriting a newer retry. Cancellation policy distinguishes cancelling one waiter from cancelling shared work. Expiry is validated on lookup and removed through an ordered/atomic compare-delete; background cleanup is bounded and safe.

Values/results are immutable or safely shared; callbacks execute outside bin locks. Admission rejects or evicts under explicit per-tenant/global entry/byte limits, with metrics for hot IDs, waits, failures, expiry lag, and retained results. The map guarantees one elected in-flight entry per equivalence key and defined sharing/transition semantics. It cannot guarantee an external RPC ran exactly once: the owner can perform the effect and fail before publishing completion. Use idempotency keys and downstream transactional/deduplication protocols for that claim.

### Answer 5

First specify required language/type safety, per-key methods, multi-key/aggregate semantics, iteration, callbacks, lifecycle, memory bounds, progress, and supported runtimes. Establish a coarse typed map as the correctness oracle unless latency/progress requirements already disqualify blocking. Map candidates to contracts: do not use `sync.Map` outside its specialized patterns without evidence; use Java/oneTBB only where their precise methods and lifetime semantics match; custom nonblocking code requires atomic/reclamation expertise and a progress need.

Create sequential differential, collision, resize, callback-fault, delete/reclamation, history-linearizability, race/memory, and capacity/security tests. Benchmark identical semantics using observed read/write/hit/miss, key skew, table/value sizes, collision profile, resize/clear/snapshot rates, callbacks, thread count, allocator, and CPU/NUMA topology. Record throughput, tails, per-key/bin contention, retries, migration, allocations, cache behavior, and retained bytes.

Choose the least complex candidate meeting correctness, operational, and measured objectives with reviewable evidence. Define rollback before launch—for example, any correctness anomaly, unbounded retained generation, tail regression above the service budget, or benefit below the maintenance threshold returns to the coarse/striped baseline. Revalidate when workload, runtime, hardware, key policy, or required semantics change.
