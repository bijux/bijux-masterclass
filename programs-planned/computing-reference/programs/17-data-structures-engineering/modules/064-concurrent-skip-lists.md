---
module_id: DSE-064
program: Data Structures Engineering
level: 2
module_number: 64
title: Concurrent Skip Lists
status: complete
last_verified: 2026-08-30
---

# Concurrent Skip Lists

## One-Page Review

### Governing question

How can a probabilistic ordered index support overlapping search, insertion, deletion, and range navigation while preserving comparator order, one logical membership decision, safe publication, linearizable point operations, stated range semantics, progress, and memory lifetime?

### Essential definitions

- A **skip list** is a sorted level-0 linked list plus progressively sparser forward-pointer levels used as search indexes.
- A node's **height** is the number of consecutive levels in which it participates, starting at level 0.
- A **tower** is one logical node and its forward links across those levels.
- A **search path** moves right while the next key precedes the target, then descends a level.
- A **predecessor/successor window** contains the adjacent nodes around a target at each relevant level.
- A **fully linked** flag in some lock-based algorithms distinguishes a completely published tower from one still being installed.
- A **mark** or logical-deletion state makes a node absent before all physical links are removed.
- **helping** lets one operation complete another operation's announced structural work.
- A **weakly consistent range traversal** tolerates concurrent changes without promising one atomic snapshot.
- A **linearization point** places a point operation at one instant between invocation and response in the abstract ordered-map history.
- A **reclamation protocol** delays node destruction/reuse until no traverser can retain or dereference it.

### Central model, mechanism, or theorem

Let level 0 contain every live key in strict comparator order. For each higher level `i`, its nodes form an ordered subsequence of level `i-1`; a node of height `h` appears exactly at levels `0..h-1`. Search begins at the highest current level and preserves the invariant `pred.key < target <= succ.key` while moving right and down. With independent geometric heights, the expected search and update path length is logarithmic, but a particular topology can be taller or slower.

A concurrent algorithm must identify one membership-defining event. Common designs make successful insertion linearize when the new node is linked at level 0 or becomes fully linked; higher links are auxiliary and may be installed afterward under a stated rule. Removal often linearizes at a logical mark, with physical unlinking/help later. Every point lookup must interpret partial publication and marks consistently. This separation is valid only with target-language atomic/lock ordering and safe node lifetime.

### Critical invariants

1. Level 0 contains every live abstract key exactly once in strict comparator order.
2. Every higher level is an ordered subsequence of the level below; towers contain no holes.
3. Comparator equivalence and ordering remain stable for every stored key.
4. An operation validates the predecessor/successor window it will modify after acquiring protection or before successful CAS.
5. Exactly one specified event changes logical membership for each successful insert/remove.
6. Readers never treat an uninitialized, partially linked under invalid states, marked, or reclaimed node as live.
7. Failed/duplicate operations linearize at a protected or validated observation consistent with the abstract set/map.
8. Physical unlinking can lag logical deletion, but stale links preserve ordered traversal and are eventually helped or tolerated by contract.
9. Head height, level metadata, range views, comparator, callbacks, size, clear, and lifecycle each have explicit concurrent semantics.
10. Retired nodes, index nodes, and whole list storage remain alive through every possible reader, holder, iterator, or helper.

### Common failures

- Treating expected `O(log n)` as a deterministic worst-case guarantee.
- Allowing a node to appear at level 2 without appearing at levels 0 and 1.
- Publishing an upper link before initialized level-0 membership under a reader algorithm that trusts upper links.
- Locking predecessor nodes found earlier without validating that their successor windows remain current.
- Acquiring duplicate predecessor locks twice when several levels share one predecessor.
- Physically unlinking first and choosing a vague later linearization point for deletion.
- Freeing a marked/unlinked tower while an optimistic reader retains it.
- Mutating a key or comparator policy after insertion.
- Claiming a range iterator is an atomic snapshot because every individual step is safe.
- Benchmarking uniform point lookups while production depends on skewed inserts, range scans, deletion, or descending traversal.

### Compact example

A deterministic four-level model gives integer keys 1–15 heights based on divisibility by powers of two: all keys occur at level 0, evens at level 1, multiples of four at level 2, and 8 at level 3. Search for 11 advances through 8 and 10 before examining 11. The executable verifies ordered levels, subsequence/tower invariants, predecessor 10, presence/absence, and range 5–10. It models topology only—not threads, locks, atomics, random-height probability, deletion, or memory ordering.

### Connections

[DSE-014](014-singly-linked-lists.md) supplies base-list invariants; [DSE-040](040-skip-lists.md) supplies sequential probabilistic structure; [DSE-062](062-fine-grained-locking.md) supplies validation and lifetime obligations; [DSE-063](063-concurrent-hash-maps.md) contrasts unordered per-key concurrency and resize. The [program roadmap](../ROADMAP.md) next develops lock-free stacks and queues, atomic primitives, reclamation, and history testing.

## Governing Question

Can an ordered concurrent index use a probabilistically sparse tower structure to avoid global balancing while giving precise point, navigation, range, progress, publication, deletion, and lifecycle guarantees?

## Why This Matters

Ordered concurrent indexes support floor/ceiling queries, priority selection, interval navigation, leaderboards, schedulers, version tables, time-series windows, and storage-engine memory tables. Hash maps usually offer expected constant-time point lookup but cannot naturally enumerate a key interval in comparator order. Balanced trees provide order, yet rotations and rebalancing modify neighborhoods that complicate fine-grained concurrency. Skip lists replace deterministic balance with randomized height and mostly local forward-link changes.

That structural simplicity is real but easy to overstate. A concurrent skip list is not merely several linked lists with atomic pointers. Search can encounter nodes during insertion or deletion. An update may have the same predecessor on many levels, so lock acquisition must deduplicate. A node can be logically absent while upper links still reach it. Range traversal can cross many concurrent linearization points without representing any single state. Memory reclamation remains necessary even when logical algorithms are correct.

The base level usually carries abstract membership; upper levels accelerate navigation. This distinction permits index maintenance to lag or be helped, but only if readers define how partial towers are interpreted. Some implementations initialize a node and link bottom-up, then publish `fullyLinked`; some nonblocking designs use CAS and marked references; some insertion-only structures never delete nodes until the whole arena dies, radically simplifying lifetime. These contracts must not be mixed.

Probability affects engineering. With promotion probability `p`, expected height and pointer cost are controlled, but the realized topology varies. A hostile or broken random source can create many tall nodes or a nearly flat list. Fixed maximum height avoids unbounded arrays but influences large-`n` behavior. Random level generation must be thread-safe, cheap, reproducible when testing, and not accidentally synchronized as one global bottleneck.

Library names also hide semantic differences. Java's `ConcurrentSkipListMap` documents expected average logarithmic operations, weakly consistent iterators, nonconstant `size`, and different performance characteristics for ascending and descending views. RocksDB's inline skip list supports concurrent insert and read under explicit lifetime/immutability conditions and retains nodes until destruction. A course-level design must teach how to read these exact contracts rather than infer universal behavior.

## Prerequisites and Retrieval

Retrieve linked-list reachability, total orders and comparator equivalence, maps/sets, geometric distributions, expectation, logarithms, representation invariants, locks, compare-and-set, memory visibility, linearizability, lock-free progress, ABA, and safe reclamation. From [DSE-040](040-skip-lists.md), retrieve sequential search and height generation. From [DSE-062](062-fine-grained-locking.md), retrieve guard maps, optimistic validation, ranked/deduplicated locking, structural publication, and distinction among logical removal, unlinking, and reclamation.

From [DSE-063](063-concurrent-hash-maps.md), retrieve conditional map APIs, callback hazards, exact versus weak aggregate semantics, security/resource limits, and workload-shaped evidence. You should be able to trace a top-down search, state why `compare(a,b)=0` defines map-key equivalence, and explain why an atomically loaded pointer still requires a valid object lifetime.

## Learning Objectives

After completing this module, you can:

1. derive skip-list ordering, tower, and search-window invariants;
2. compute expected height/pointer behavior under a geometric promotion model;
3. distinguish level-0 membership from auxiliary upper-level indexing;
4. compare coarse, lock-coupled, optimistic fine-lock, lazy, and nonblocking updates;
5. justify linearization points for successful, duplicate, absent, and removed outcomes;
6. design publication and deletion states that readers interpret consistently;
7. specify point, navigation, range, size, callback, and lifecycle semantics;
8. connect marking/unlinking to ABA prevention and reclamation;
9. analyze skew, random-height quality, range scans, cache layout, and memory overhead; and
10. construct correctness, probability, fault, progress, and production-performance evidence.

## Core Exposition

**Begin with the ordered abstract type.** Define whether the object is a set, map, or multimap. For a map, specify `get`, `put`, `putIfAbsent`, conditional replace/remove, first/last, lower/floor/ceiling/higher, subrange views, iteration direction, size, snapshot, clear, and close. State null policy, comparator equivalence, mutable-value ownership, callback behavior, and whether range views are live.

The comparator defines both ordering and key identity. If `compare(a,b)=0`, the map normally treats keys as equivalent even when object equality differs. It must be antisymmetric in sign, transitive, and stable while keys are stored. Mutable comparison fields can move a key conceptually without changing links, breaking both lookup and uniqueness. Comparators are callbacks and may block, throw, acquire locks, or reenter; constrain and audit them.

**Derive the sequential topology.** A head sentinel has forward pointers up to a maximum level. Every node has height at least one. Level 0 is a sorted linked list of all keys. Level `i+1` contains only nodes also in level `i`. Search maintains a current predecessor. At each level from high to low, advance while `next.key < target`; when advancing would reach or pass target, descend. At level 0, successor determines presence or insertion position.

With promotion probability `p` and independent heights, `Pr[height >= h] = p^(h-1)` for `h >= 1` until the cap. The expected number of levels in one uncapped tower is

`E[height] = Σ_{h>=1} Pr[height >= h] = Σ_{j>=0} p^j = 1/(1-p)`.

For `p=1/2`, expected forward pointers per node are 2; implementation layout, alignment, backward links, marks, values, allocator metadata, and capped distribution change actual bytes. Expected search is logarithmic under the model, but probability does not guarantee a particular instance or deadline.

**Separate abstract state from index state.** The cleanest proof selects one base-level event as membership. Upper levels are search accelerators. A search reaching a node through an upper level must still follow rules that establish its live base membership. Conversely, a freshly inserted base node may be live before all upper links exist if the algorithm permits this.

In a lazy lock-based design, a new node is privately initialized with random height and successor pointers. The updater searches for predecessor/successor arrays. It locks the distinct required predecessors in a deterministic order, validates that none are marked and each expected link remains current, then links levels under the algorithm's publication order. A `fullyLinked` state can prevent readers/removers from treating an incomplete tower as live. Successful insertion may linearize when `fullyLinked` becomes true; an alternative design can linearize at level-0 link publication and treat later index installation as auxiliary. Pick one and prove every operation against it.

Duplicate predecessor objects are common: one tall node can precede the target at several levels. Acquiring its nonreentrant lock once per level self-deadlocks. Deduplicate by identity, follow a documented order, and release only acquired locks. If validation fails, release and retry without irreversible callbacks or external effects.

**Search is optimistic but not assumption-free.** A read-only traversal often follows atomic/acquire links without locking. It may see a marked node, partially installed index, or stale upper link. The algorithm defines whether to skip marked nodes, help unlink, restart, or descend. All nodes reached must remain alive. A collector can preserve allocation but not logical validity; native memory needs a pin, hazard, epoch, reference, RCU, arena-lifetime, or equivalent guarantee.

Point lookup linearizes at a validated observation. Presence can linearize at the read/state check showing an equivalent fully live base node. Absence needs a moment when the predecessor/successor window excludes the target under the algorithm's interference rules. Simply finishing a traversal after many concurrent changes is not automatically a proof.

**Deletion is a protocol.** A remover finds the victim, establishes it is fully published/live, then makes one logical-deletion state transition. In lock-based lazy algorithms it may lock/mark the victim, lock distinct predecessors, validate links, and unlink the tower top-down or bottom-up according to the proof. In nonblocking algorithms it marks links with CAS and helpers physically bypass marked nodes.

If logical marking is the deletion linearization point, subsequent lookups treat the node absent even while links remain. Only one remover wins the mark. Physical unlink is cleanup and must preserve order. Re-inserting an equivalent key can coexist physically with a marked predecessor only if traversal and uniqueness rules distinguish them. Reclamation waits beyond unlink until no reader/helper holds the old node.

The ABA problem can arise when a link value changes from address A to B and later appears as A because storage was reused; a CAS may accept a state that is not the one originally observed. Tagged/versioned references can help with comparison identity, while safe reclamation prevents premature reuse/dereference. Neither universally replaces the other.

**Nonblocking variants demand an explicit progress proof.** A lock-free skip list usually marks logical deletion in pointer metadata and uses CAS to link/bypass nodes. Failed CAS indicates interference and triggers retry or helping. To claim lock-freedom, show that infinite failure by one operation entails successful system-wide operations—not merely that no mutex appears in source. Allocation, comparator code, reclamation, scheduler, and runtime can still block outside the abstract algorithm.

Wait-free lookup claims require a bounded-step argument under the exact model; retry/help paths can invalidate that claim. Starvation of one updater is compatible with lock-freedom. Instrument retries and help so a theoretically nonblocking design does not hide operational livelock or tail collapse.

**Range semantics require deliberate choice.** Point linearizability composes across objects, but a traversal performing many point reads need not equal one snapshot. A weakly consistent iterator can move through safe ordered links and reflect a mixture of updates. Its contract should say whether it may miss overlapping inserts, observe removals, duplicate entries, or include only elements live at some moment during traversal.

An atomic range snapshot needs a stronger mechanism: a global/wide lock, persistent version, MVCC epoch, validated version scan, or copy under quiescence. Validation may retry indefinitely under writes. Live submap views must apply bounds atomically to each operation and define behavior when the backing map changes. Descending traversal may need backward links or repeated predecessor search and can cost differently from ascending traversal.

`size()` is also a range over all membership. Maintaining an atomic count can give a count of completed updates at its read instant, but iteration still may represent another sequence of instants. Traversal-based size is nonconstant and can be inaccurate during updates. Never silently turn a library's documented status method into an atomic snapshot claim.

**Height generation is mechanism and attack surface.** A common generator counts successes from independent Bernoulli trials until failure or maximum height. Use per-thread/generator state or an appropriate concurrency-safe source; a single locked RNG can serialize insertions. Test deterministic seeds, extremes (all height 1, many maximum height), and distribution quality. A caller must not normally choose arbitrary height, or it can force memory/work imbalance.

Maximum level should relate to supported capacity and promotion probability with overflow-safe calculation. Head growth/publication must be synchronized. It can be safe to retain a high head level after tall-node deletion; shrinking it concurrently adds complexity and rarely changes abstract semantics. Bound node height before allocation to prevent malformed or adversarial metadata from causing oversized objects.

**Layout determines real cost.** Towers can use variable-sized inline forward arrays, separate index nodes, fixed arrays, or pointer towers. Inline layouts reduce allocations/indirection but complicate allocation and reclamation. Separate index nodes allow base entry/index lifetimes to differ. Marks may steal pointer bits only when alignment and platform representation permit; portable code must not assume spare bits.

RocksDB's `InlineSkipList` documents an insertion/read contract built around immutable node content after publication, release stores, no deletion until whole-list destruction, and external lifetime safety. That design is excellent for an append-only memtable but cannot be copied into a general delete-capable map without adding deletion/reclamation semantics.

The following executable artifact isolates deterministic topology and search. Heights based on powers of two replace randomness so output is reproducible. It checks the structural facts a concurrent algorithm must preserve but executes no concurrency protocol.

<!-- bijux-verify: {"id":"skip-list-topology-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"levels=4\nlevel_widths=15,7,3,1\nkeys=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15\nsearch_11=True\nsearch_16=False\npredecessor_11=10\nrange_5_10=5,6,7,8,9,10\nforward_hops_11=2\nordered_levels=True\ntower_subset_invariant=True\nevidence=finite_skip_list_topology_model\n","stderr":""}} -->
```python
def deterministic_height(key, maximum):
    height = 1
    while height < maximum and key % (2 ** height) == 0:
        height += 1
    return height


class SkipListTopology:
    def __init__(self, keys, maximum_height):
        self.levels = []
        for level in range(maximum_height):
            self.levels.append([
                key for key in keys
                if deterministic_height(key, maximum_height) > level
            ])

    def find(self, target):
        current = None
        hops = 0
        for level in reversed(self.levels):
            for key in level:
                if current is not None and key <= current:
                    continue
                if key < target:
                    current = key
                    hops += 1
                else:
                    break
        return target in self.levels[0], current, hops

    def range_keys(self, lower, upper):
        return [key for key in self.levels[0] if lower <= key <= upper]


topology = SkipListTopology(list(range(1, 16)), 4)
found_11, predecessor_11, hops_11 = topology.find(11)
found_16, _, _ = topology.find(16)
ordered_levels = all(level == sorted(level) for level in topology.levels)
tower_subset = all(
    set(topology.levels[level]).issubset(topology.levels[level - 1])
    for level in range(1, len(topology.levels))
)

print(f"levels={len(topology.levels)}")
print("level_widths=" + ",".join(str(len(level)) for level in topology.levels))
print("keys=" + ",".join(str(key) for key in topology.levels[0]))
print(f"search_11={found_11}")
print(f"search_16={found_16}")
print(f"predecessor_11={predecessor_11}")
print("range_5_10=" + ",".join(str(key) for key in topology.range_keys(5, 10)))
print(f"forward_hops_11={hops_11}")
print(f"ordered_levels={ordered_levels}")
print(f"tower_subset_invariant={tower_subset}")
print("evidence=finite_skip_list_topology_model")
```

The model verifies exact topology, not the expected complexity of randomized heights. It has no threads, concurrent mutation, locks, CAS, marks, partial towers, callbacks, memory model, reclamation, arbitrary schedule, fault injection, or performance measurement.

**Evidence must match the contract.** Sequential differential tests compare ordered point/navigation/range results with a trusted sorted map. Invariant checks verify level-0 order/uniqueness, tower prefixes, higher-level subsequences, marks/publication states, head height, and size policy. Controlled schedules target same-key inserts, insertion versus deletion, duplicate predecessors, partial publication, marked-node search, helper races, iterator overlap, callback failure, clear/close, and stalled operations.

Record invocation/response histories and check point-operation linearizability. Model-check bounded topologies when possible. Use race/memory/sanitizer tools and reclamation-specific tests within their limitations. For lock-free claims, test stalled threads and quantify system progress/retries rather than equating throughput with proof.

Benchmark against a coarse locked sorted map, concurrent tree, and relevant library with equal semantics. Vary point/range mix, range length/direction, read/write/delete ratios, existing/missing keys, sequential versus random keys, comparator cost, key skew, size, height probability/cap, threads, allocator, CPU/NUMA placement, and reclamation. Report throughput, tails, comparisons, forward hops, CAS failures/retries/help, marks awaiting unlink, retired bytes, level distribution, allocations, cache misses, and memory per entry.

## Definitions and Notation

Let comparator `cmp` define strict order `<` and equivalence `≈`, where `a ≈ b` iff `cmp(a,b)=0`. Let level 0 be `L_0` and higher levels `L_i`. The topology invariant is `L_{i+1} ⊆ L_i`, each `L_i` is strictly ordered, and every live abstract key occurs exactly once in `L_0`.

For node `x`, height `h(x) >= 1` means `x` participates at levels `0..h(x)-1`. Under independent promotion probability `p`, `Pr[h(x) >= j] = p^(j-1)` before the maximum cap and uncapped `E[h]=1/(1-p)`. These are distribution statements, not guarantees about one execution.

A search for target `k` produces predecessor/successor arrays `pred[i]`, `succ[i]` such that `pred[i].key < k <= succ[i].key` under sentinel conventions. A **valid window** additionally satisfies the concrete algorithm's reachability, mark, generation, and adjacency predicates at modification time.

Let node lifecycle states be `N` (private/new), `P` (partially linked), `F` (fully live), `D` (logically deleted/marked), `U` (physically unlinked), and `R` (reclaimable). Not every implementation represents every state, but its allowed transitions and reader interpretation must be explicit. Membership linearization may be `P→F`, level-0 publication, or a specified CAS; deletion may be `F→D`.

A history `H` records operation invocations/responses. Linearizability requires a legal sequential ordered-map history preserving nonoverlap real-time order. Weak traversal consistency is an independently specified property and cannot be substituted into that definition.

For evidence, let `C` be comparisons, `Q` forward hops, `F_cas` failed CAS operations, `R_op` retries, `A` active/retired allocation bytes, and `X_q` the `q`th latency percentile. Measurements require a named runtime, workload, topology, and instrumentation method.

## Mechanisms, Invariants, or Proof Structure

### Search proof

1. Start at head on a safely published current maximum level.
2. At each level, follow only lifetime-safe forward links interpreted under mark/publication rules.
3. Each right move strictly increases key and remains below target; each descent preserves the bracketing window.
4. At level 0, a validated equivalent live successor proves presence; a validated strict successor window proves absence.
5. Identify the read/validation event that linearizes the returned outcome.

### Lazy locked insertion proof

1. Generate a bounded height and initialize the candidate privately.
2. Search for predecessor/successor windows; return duplicate only from a live validated observation.
3. Deduplicate and order required predecessor locks.
4. Revalidate adjacency, marks, and publication states after acquisition.
5. Initialize all candidate forward links before any reachable publication.
6. Link according to the algorithm's level order and publish membership at the stated event.
7. Restore tower/subsequence invariants and release exactly acquired locks on every exit.

### Removal and reclamation proof

1. Find and validate one fully live equivalent victim.
2. Win exactly one logical mark; this is the specified deletion point when applicable.
3. Prevent new operations from treating the victim as live.
4. Acquire/validate or CAS-bypass every reachable tower link while maintaining order.
5. Permit helpers to finish idempotent unlink work under the progress model.
6. Retire only after unlink; reclaim only after the lifetime protocol proves no reader/helper/iterator can retain the node.

### Progress proof obligations

For blocking algorithms, give a global lock order, failure cleanup, fairness/starvation caveats, and bounds/telemetry for waits. For optimistic locking, analyze validation livelock and backoff. For lock-free algorithms, identify the successful shared-state step forced by repeated interference and define which operations/help count as progress. For wait-free claims, provide a per-operation step bound. Treat allocator, comparator, reclamation, and external callbacks separately.

### Evidence ladder

1. Comparator-law and sequential ordered-map differential tests.
2. Deterministic and randomized topology/distribution invariant tests.
3. Controlled publication, duplicate, removal, helper, range, failure, and lifecycle schedules.
4. Bounded history linearizability/model checking for point operations.
5. Race, memory-order, lock-order, sanitizer, and reclamation tooling.
6. Progress experiments with stalled/preempted operations and retry/help telemetry.
7. Adversarial height, key skew, comparator, capacity, and memory-pressure tests.
8. Deployment-shaped point/range throughput, tails, cache, allocation, and retained-memory measurement.

## Alternatives and Trade-Offs

| Design | Point update mechanism | Range behavior | Principal trade-off |
|---|---|---|---|
| Coarse locked sorted map | one mutex | easy atomic traversal under lock | no internal concurrency |
| Fine-locked skip list | predecessor/node locks | safe traversal needs separate contract | lock count/order/validation |
| Lazy optimistic skip list | search, lock window, validate | often weak unless widened | short holds, retries/partial states |
| Nonblocking skip list | CAS, marking, helping | point progress does not imply snapshot | memory order, ABA, reclamation |
| Concurrent balanced tree | node/path/structural protocol | natural ordered navigation | rotations/rebalancing complexity |
| Copy-on-write/persistent tree | publish immutable root | cheap stable snapshots | update allocation/reclamation |
| Sharded ordered maps | per-shard lock/index | global merge required | simple shards, hard global order |
| LSM/memtable skip list | often insert-only until freeze | ordered scan natural | duplicates/versions resolved elsewhere |

Skip lists trade deterministic balance for probabilistic simple local changes. Trees may have better worst-case guarantees and cache layouts; B-trees reduce pointer overhead and suit storage/cache lines; persistent trees simplify snapshots. Select by required semantics and evidence.

Insertion-only arena lifetime is a powerful specialization. It removes deletion and per-node reclamation and can make lock-free reads much simpler, as in a memtable that is frozen then destroyed after readers leave. It is not a general map with remove/replace; storage-engine sequence/version semantics often resolve multiple entries elsewhere.

Backward pointers speed descending iteration but add update/publication state. Without them, descending operations can repeatedly search predecessors. Java's current documentation warns that ascending views are faster than descending ones. The choice should follow workload, not symmetry aesthetics.

## Failure Modes and Misconceptions

- **“Skip lists guarantee logarithmic time.”** Standard randomized skip lists give expected/probabilistic bounds under height assumptions.
- **“Upper levels contain the data.”** Usually level 0 defines membership and upper links are indexes; state the concrete design.
- **“Bottom-up insertion is always correct.”** It is correct only with reader interpretation, publication ordering, and chosen linearization point.
- **“One predecessor per level means one lock per level.”** Predecessors can repeat; deduplicate or self-deadlock.
- **“Locks make the old search window current.”** Links and marks can change before acquisition; validate after locking.
- **“Marked means safe to free.”** Marking changes abstract membership, not pointer lifetime.
- **“CAS removes ABA.”** CAS can be fooled by reuse; use tags/algorithmic constraints and reclamation.
- **“Lock-free means every caller finishes.”** System progress can coexist with starvation; allocators/callbacks may block.
- **“Weak iterator means arbitrary output.”** It still owes order, safety, and the library's specified overlap behavior.
- **“Point linearizability gives an atomic range.”** A multi-step traversal can span many map states.
- **“Atomic size and iterator should agree.”** They may observe different instants unless one snapshot protocol binds them.
- **“Random height is not shared state.”** A global RNG lock/state can serialize or race; distribution and bounds matter.
- **“A GC runtime solves removal.”** It can retain memory yet still leave logical marks, partial towers, or stale observations wrong.
- **“More levels always speed search.”** Tall towers add pointers, cache misses, publication work, and contention.
- **“Uniform point benchmarks select the structure.”** Range length/direction, mutation, skew, comparator, memory, and reclamation can reverse results.

## Worked Examples

### Example 1

**Situation.** With promotion probability `p=1/2`, estimate forward-pointer slots for one million nodes before implementation overhead.

**Reasoning.** Uncapped expected height is `1/(1-p)=2`. Expected slots are about two million. This is not actual bytes: pointer width, node headers, values, marks, alignment, maximum cap, head, allocator metadata, and realized heights matter.

**Conclusion.** Probability supplies a capacity estimate, not a memory measurement.

### Example 2

**Situation.** A candidate of height 4 has the same predecessor node at levels 0–3. Code locks `pred[i]` in a loop.

**Reasoning.** A nonreentrant lock is acquired four times by one thread and self-deadlocks. Build the distinct lock set, order it under the algorithm's rule, acquire each once, validate every affected level, and release once.

**Conclusion.** Lock ownership follows distinct nodes, not array positions.

### Example 3

**Situation.** An insertion links a node at level 2 before level 0 and readers trust any reachable upper node as present.

**Reasoning.** A reader can return a key absent from the membership-defining base list, and the tower has a hole. Either publish bottom-up and require a fully-linked state, make upper visibility nonauthoritative, or choose/prove another atomic multi-level scheme.

**Conclusion.** Publication order and reader interpretation jointly define correctness.

### Example 4

**Situation.** Two inserters search for absent key 10, then lock old predecessor/successor windows.

**Reasoning.** The first publishes 10. The second's pre-lock window is stale. Post-acquisition validation must fail or reveal the live equivalent node; it returns duplicate at a valid observation rather than linking a second 10.

**Conclusion.** Optimistic search requires validation to enforce uniqueness.

### Example 5

**Situation.** A remover marks key 20, but upper links still reach it when a lookup arrives.

**Reasoning.** If mark is the deletion point, lookup must treat 20 absent and may help bypass it or continue safely. Physical reachability does not restore membership. Node lifetime remains protected until all readers/helpers leave.

**Conclusion.** Logical state, physical links, and reclaimability are independent.

### Example 6

**Situation.** A lock-free inserter repeatedly loses CAS at one predecessor while other keys continue to be inserted.

**Reasoning.** Continued successful interfering CAS can satisfy system-wide lock-freedom even though this caller starves. Record retries, use appropriate helping/backoff, and do not advertise wait-freedom. A deadline-sensitive API may need stronger admission/fairness policy.

**Conclusion.** Progress classes describe different guarantees.

### Example 7

**Situation.** A range iterator visits 5, then a concurrent operation removes 6 and inserts 5.5 before the iterator's current position.

**Reasoning.** A weak forward iterator may legally miss 5.5 and skip marked 6 while continuing in order, if documented. It does not represent one snapshot. An atomic range requires versioning, locking, MVCC, or validated retry.

**Conclusion.** Safe ordered traversal is weaker than snapshot consistency.

### Example 8

**Situation.** A native implementation unlinks node A and immediately allocates node B at the same address while a reader retains A's pointer.

**Reasoning.** The reader can dereference B as A or a CAS can see address A again. Epoch/hazard/reference/RCU lifetime prevents reuse until old readers finish; tags can additionally distinguish versions where the algorithm needs it.

**Conclusion.** Reclamation is part of the algorithm, not allocator cleanup.

### Example 9

**Situation.** An insert-only storage-engine memtable never deletes nodes and freezes the entire structure before reclamation.

**Reasoning.** Readers need a guarantee the memtable remains alive; immutable node content and release/acquire link publication can support lock-free reads. Multiple logical versions may coexist and are resolved by sequence semantics. This specialization eliminates per-node delete but not lifetime/publication requirements.

**Conclusion.** Restricted lifecycle can simplify concurrency more than a clever general deletion algorithm.

### Example 10

**Situation.** A concurrent skip list wins random point lookups, while production performs long descending scans with expensive comparison and frequent deletion.

**Reasoning.** The benchmark omitted descending-path design, scan consistency, comparator cost, marks/unlink help, retired memory, and allocator/cache behavior. Compare equal APIs under observed mixes and report tails, comparisons, hops, retries, level distribution, and bytes.

**Conclusion.** Ordered-index selection requires range- and lifecycle-shaped evidence.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** [CONPAR-023](../../04-programming-languages-concurrent-and-parallel-programming/modules/023-happens-before-relations.md) supplies visibility; later atomic/progress modules support CAS, helping, ABA, and reclamation arguments.
- **Database Engineering:** the [database roadmap](../../18-database-engineering/ROADMAP.md) places ordered in-memory indexes inside transactions, MVCC, logging, and storage-engine lifecycle.
- **Algorithms and Complexity:** randomized analysis separates expected path bounds from realized and adversarial behavior.
- **Security Engineering:** comparator work, caller-controlled height, capacity growth, and retained retired nodes can become denial-of-service surfaces.
- **Performance Engineering:** cache locality, pointer count, allocation, search comparisons, scan direction, NUMA, and reclamation dominate beyond asymptotics.
- **Software Engineering Patterns:** snapshot, iterator, accessor, lifecycle, and callback contracts must remain visible at the abstraction boundary.

## References

1. William Pugh, [“Concurrent Maintenance of Skip Lists”](https://15721.courses.cs.cmu.edu/spring2019/papers/07-oltpindexes1/pugh-concurrent-tr1990.pdf), UMIACS-TR-90-80 / CS-TR-2222.1, revised 1990. Primary concurrent skip-list algorithms and proofs.
2. William Pugh, [“Skip Lists: A Probabilistic Alternative to Balanced Trees”](https://paper-notes.zhjwpku.com/assets/pdfs/skiplists-cacm1990.pdf), *Communications of the ACM* 33(6), 1990, pp. 668–676. Primary sequential structure and probability analysis.
3. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990. Primary history-correctness framework.
4. Keir Fraser, [“Practical Lock-Freedom”](https://www.cs.otago.ac.nz/cosc440/readings/lock-freedom.pdf), University of Cambridge Technical Report UCAM-CL-TR-579, 2004. Primary nonblocking skip-list design and progress context.
5. Oracle, [`ConcurrentSkipListMap`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/ConcurrentSkipListMap.html), Java SE 26. Official current ordered-map, iterator, size, and performance semantics.
6. Oracle, [`ConcurrentNavigableMap`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/ConcurrentNavigableMap.html), Java SE 26. Official concurrent range-view and navigation interface.
7. RocksDB Project, [`InlineSkipList` source and invariants](https://github.com/facebook/rocksdb/blob/main/memtable/inlineskiplist.h), accessed 2026-08-30. Official publication, immutability, insertion, reader-lifetime, and no-deletion implementation contract.
8. RocksDB Project, [MemTable documentation](https://github.com/facebook/rocksdb/wiki/MemTable), accessed 2026-08-30. Official skip-list memtable, concurrent-insert, scan, layout, and workload trade-offs.

## Exercises

### Exercise 1

Define tower, height, search window, fully linked, logical mark, physical unlink, helping, weak range traversal, lock-free, and reclamation. State the level-subsequence and membership invariants.

### Exercise 2

For promotion probability `p=1/4`, derive uncapped expected node height. For 800,000 nodes, estimate expected forward-pointer slots, then explain at least five reasons measured memory differs.

### Exercise 3

Diagnose an insertion that searches, locks each predecessor array entry without deduplication, checks only that predecessors are unmarked, links upper levels before level 0, and returns. Give a corrected lazy-locking outline with a clear membership event.

### Exercise 4

Specify a concurrent ordered map supporting point operations, floor/ceiling, weak ascending iteration, and an explicit atomic snapshot method. Choose blocking, lazy, or nonblocking point updates and explain snapshot, size, comparator, deletion, progress, and reclamation semantics.

### Exercise 5

A storage engine needs a write-optimized in-memory ordered structure with concurrent inserts, point reads, forward range scans, immutable versioned entries, no per-entry delete, and whole-memtable freeze/reclamation. Design the skip-list lifecycle and evidence plan; identify which general concurrent-map problems disappear and which remain.

## Answers to the Exercises

### Answer 1

A tower is one node's participation across consecutive levels; height is its level count. A search window is the predecessor/successor pair bracketing a target. Fully linked identifies a completely published node in algorithms using that state. A mark changes logical membership to deleted; unlink removes physical incoming links. Helping completes another operation's announced work. Weak traversal remains safe/ordered under documented overlap without one snapshot. Lock-free means system-wide progress despite individual delay. Reclamation proves storage may be reused/destroyed.

Each higher level must be an ordered subsequence of the level below, with no tower holes. Level 0 contains every live equivalence class exactly once in comparator order. Partial/marked nodes are interpreted by one stated protocol, and no node is reclaimed while any traversal/helper/iterator can retain it.

### Answer 2

`E[h]=1/(1-p)=1/(3/4)=4/3`. Expected forward slots are `800,000 * 4/3 ≈ 1,066,667`. This is a distribution expectation before a maximum cap. Actual memory also includes pointer width, node/key/value headers, mark/version fields, alignment/padding, allocator metadata/fragmentation, head/sentinels, backward links or separate index nodes, realized random heights, maximum-level truncation, retired but unreclaimed nodes, and runtime object/GC overhead.

The expectation assumes independent correctly distributed heights. A shared biased RNG, adversarial height input, or implementation-specific promotion rule changes it. Measure allocated/resident/retired bytes under the target allocator and workload.

### Answer 3

Repeated predecessor objects can make a thread reacquire one nonreentrant lock and self-deadlock. Merely checking unmarked predecessors does not prove `pred[i].next[i] == succ[i]`; an intervening insertion can make the window stale. Publishing upper links first violates tower-prefix structure and may expose a node readers incorrectly treat as live. Returning without a full publication state leaves membership ambiguous.

Correctly choose bounded height and initialize the candidate privately. Search arrays, then form distinct predecessor locks, acquire under the algorithm's order, and validate predecessor/victim marks plus exact adjacency at every affected level. On failure release and retry without irreversible effects. Initialize all candidate successors. Link level 0 then higher levels under a reader-compatible order; after required links, release-store `fullyLinked=true`, making that transition the insertion linearization point. Duplicate failure linearizes at a validated equivalent fully linked node. Release exactly acquired locks on every exception/exit, and retire unused candidates safely.

### Answer 4

One valid design uses lazy optimistic point updates: lock/validate distinct predecessor windows, fully-linked publication, victim marking, later unlink, and epoch reclamation. `get`, put-if-absent, conditional replace/remove, floor, and ceiling are linearizable point/navigation operations with operation-specific live-node observations. The stable comparator is immutable, nonblocking, nonreentrant, and exception policy is specified; mutable values are replaced atomically as immutable cells.

Ascending iteration is weakly consistent: it follows lifetime-safe level-0 links in order, skips marked nodes, may miss overlapping inserts behind its cursor, and never promises agreement with size. `size` is an atomic completed-membership counter but not a traversal snapshot. `snapshot()` acquires a dedicated snapshot gate that point updates briefly enter around their membership event, captures/copies all live level-0 entries, then releases; it may pause writers and has entry/byte/deadline limits. Alternatively MVCC could avoid the gate at greater version/reclamation cost.

The lock order prevents cycles but fairness is not promised; validation can starve, so retries/waits are measured. Mark is deletion's linearization point; unlink is helped cleanup; epochs delay reuse. Clear/close use the snapshot/lifecycle gate and wait for entrants/epochs before destruction.

### Answer 5

Use an arena-owned skip list whose entries contain immutable internal key `(user_key, descending_sequence, type)` and immutable value/reference. Writers allocate and initialize complete nodes privately, select bounded heights with per-thread RNG, and publish links with CAS/release ordering. Reads use acquire loads and retain a memtable reference/epoch. No node is marked, unlinked, or reused while the memtable is mutable; multiple versions coexist and higher database semantics resolve them.

Freeze atomically prevents new writers, waits for/coordinates in-flight insert publication, then exposes a read-only memtable for flush and readers. Reclaim the entire arena only after flush ownership and all reader/version references are gone. This removes per-node deletion, ABA from node reuse, delete helping, exact in-place replacement, and per-node reclamation. It does not remove duplicate-insert policy, publication visibility, comparator stability, random-height bounds, failed CAS/retry, freeze/writer races, whole-object lifetime, range consistency relative to sequence snapshots, memory/capacity limits, or callback safety.

Evidence includes sequential/version-order differential tests; level/tower/publication invariants; same-key and adjacent concurrent insert schedules; stalled writer at freeze; reader during publication/freeze; deterministic extreme heights; race/memory tools; reference/arena lifetime faults; and production-shaped insert/read/forward-scan benchmarks reporting tails, comparisons, hops, CAS retries, height distribution, allocation bytes, cache/NUMA behavior, freeze latency, and retained memtables.
