---
module_id: DSE-028
program: Data Structures Engineering
level: 1
module_number: 28
title: Resizing and Incremental Rehashing
status: complete
last_verified: 2026-08-30
---

# Resizing and Incremental Rehashing

## One-Page Review

### Governing question

How can a dynamic hash table change capacity and placement without losing, duplicating, or ambiguously owning keys, while bounding latency, allocation, failure, iteration, and concurrent migration costs?

### Essential definitions

- **resize** changes physical capacity; **rehash** recomputes placement, possibly at the same capacity or with new seed/policy.
- **stop-the-world rebuild** constructs the entire destination before publishing it.
- **incremental rehash** keeps old and new representations live while migrating bounded units over multiple operations.
- A **migration unit** is the smallest authoritative unit transferred, such as an old chaining bucket, group, partition, or directory-selected table.
- A **migration cursor/bitmap** records which units are old-owned, moving, or new-owned.
- **authority** identifies the one representation whose entry is logically current for a key/unit.
- **helping** makes ordinary operations perform bounded migration work.
- **growth debt** is remaining migration work; **progress** means that debt eventually decreases.
- **same-size rebuild** removes tombstones/repairs distribution without adding capacity.
- **hysteresis** separates grow and shrink thresholds to avoid oscillation.

### Central model, mechanism, or theorem

Let old table `O` have capacity `m`, new table `N` capacity `m'`, and cursor `c` over old buckets. In a cursor-based chained design:

- old buckets with index `<c` are empty and new-owned;
- old buckets with index `>=c` may contain old-owned entries;
- every new insertion is placed in `N`;
- an update/delete that finds an old-owned key either mutates it under the authority protocol or transfers it to `N` before committing;
- lookup checks `N` first, then only the key's not-yet-migrated old bucket;
- migrating bucket `c` reinserts every live entry into `N`, empties `O[c]`, and advances `c` only after transfer is complete.

The abstraction invariant is exact-once logical membership despite two physical tables. A step budget measured only in bucket count does not necessarily bound time: one chained bucket may contain many entries, while open-addressed clusters/groups may have placement dependencies. The migration unit and latency budget must match the representation.

### Critical invariants

1. Every logical key is represented exactly once under one current authority; equal duplicates cannot straddle old and new.
2. Every physical entry satisfies the placement rule for its table's current capacity and hash configuration.
3. Migration metadata agrees with old-bucket emptiness and lookup/write routing.
4. New inserts and transferred updates publish in the new table; old authority is removed only after safe new construction.
5. A migration step either transfers a complete unit or exposes a recoverable state with unambiguous authority.
6. Counts, load/fill/tombstones, growth debt, allocation ownership, and payload lifetime agree across both tables.
7. Completion retires old storage only after no operation/iterator can reference it.
8. Grow, shrink, same-size rebuild, reserve, maximum capacity, failure, and concurrency policies are explicit.

### Common failures

- Copying old physical slots/bucket numbers instead of recomputing from full hashes.
- Looking only in the new table while a key remains old-owned.
- Writing a new copy without removing or superseding the old copy, creating ambiguous updates/deletes.
- Advancing the migration cursor before all entries in that unit are safely represented.
- Migrating an old entry after a newer new-table update and overwriting the new value.
- Counting “one bucket per operation” as bounded latency despite an adversarially huge chain.
- Starting a second resize without a defined nested-migration or finish-first policy.
- Shrinking immediately after growing under a threshold with no hysteresis.
- Retiring old memory while readers, iterators, or handles still reference it.
- Calling reserve or rehash successful after checked-size, allocation, hash, equality, or move failure.

### Compact example

A four-bucket chained map contains keys 0 and 4 in old bucket zero and key 1 in old bucket one. Growth allocates eight new buckets. Migrating one unit moves keys 0 and 4, empties old bucket zero, and advances cursor to one. Key 8 inserted during migration goes directly to new bucket zero. Updating old-owned key 1 transfers it to new bucket one before changing its value. Later cursor steps see old bucket one empty, finish remaining buckets, and retire the old array. The executable trace verifies exact ownership throughout.

### Connections

[DSE-021](021-hash-functions-and-distribution.md) owns full hashes/reduction; [DSE-022](022-separate-chaining.md) supplies bucket migration; [DSE-023](023-linear-probing.md) through [DSE-027](027-hopscotch-hashing.md) show why migration units depend on collision layout. The [program roadmap](../ROADMAP.md) next addresses flooding resistance and integrates a memory-efficient map.

## Governing Question

Which trigger, destination construction, authority protocol, migration unit, progress budget, failure boundary, and retirement proof make resizing correct and latency-aware for the actual table representation?

## Why This Matters

Fixed capacity eventually wastes memory or degrades operations. Growth restores headroom; shrink releases excess; same-size rebuild clears tombstones or bad physical history; reseeding changes adversarial placement. Yet every one changes where keys belong. A correct map cannot merely allocate a larger array and copy bytes.

A stop-the-world rebuild is conceptually clean and often fast in aggregate, but one insertion may pay `Theta(n)` work and allocate old plus new capacity simultaneously. Incremental designs distribute work, improving tail latency, but every operation must understand a mixed old/new state. Progress can stall under read-only workloads, paused iterators, allocation pressure, or contention. Two-table memory remains until completion.

Production implementations choose different decompositions. Redis incrementally migrates chaining buckets. Current Go maps bound an individual Swiss-table rebuild by partitioning the overall hash space with extendible-hashing-style directory tables. OpenJDK `ConcurrentHashMap` coordinates cooperative transfer. Abseil's probe sequence depends on whole-table capacity, so its monolithic table normally rebuilds as a unit. These are separate architectures with different invariants.

## Prerequisites and Retrieval

Retrieve abstraction, representation, operation, cost, layout, cache, genericity, iteration, testing, and benchmarking from [DSE-001](001-abstract-data-types-and-concrete-representations.md) through [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve hash/reduction from [DSE-021](021-hash-functions-and-distribution.md), chaining and rehash basics from [DSE-022](022-separate-chaining.md), live/fill/tombstone rules from [DSE-023](023-linear-probing.md), and relocation/coverage constraints from [DSE-024](024-quadratic-probing-and-double-hashing.md) through [DSE-027](027-hopscotch-hashing.md).

## Learning Objectives

After completing this module, you should be able to:

1. distinguish capacity growth, shrink, same-size rebuild, and reseeding;
2. implement a failure-atomic stop-the-world rebuild;
3. define old/new authority and lookup/write routing during incremental migration;
4. derive exact-once bucket transfer and completion/retirement;
5. choose a representation-appropriate migration unit and latency budget;
6. design grow/shrink/load/tombstone thresholds with checked arithmetic and hysteresis;
7. specify iterator/reference, serialization, and allocation behavior across migration;
8. reason about helping, concurrent transfer, memory ordering, and reclamation;
9. test interleavings, stalled progress, nested triggers, failure, and hostile buckets;
10. benchmark amortized work, operation tails, memory overlap, and completion time.

## Core Exposition

**Resize is a representation transformation.** The logical map is a set of unique key/value associations. Its physical table encodes capacity, hash seed/mix, reduction, probe or bucket layout, slot metadata, and possibly iteration order. Changing any placement input requires deriving each live entry's destination from full semantic/hash information.

Copying an old bucket index is wrong when `m` changes. Copying an open-addressed slot array retains clusters/tombstones whose reachability proof used the old modulus. Copying a hop bitmap retains old homes. Cuckoo candidates and Robin Hood distances change. Reinsert or use a variant-specific split theorem that proves how old placement maps to new placement.

**Stop-the-world rebuild is the reference design.** Compute a legal destination capacity with checked arithmetic. Allocate and initialize destination metadata. For each live old entry, recompute all destination placement parameters and insert it exactly once, without consulting stale tombstones/physical order as logical content. When destination size and invariants match source, publish it and retire old storage after references are excluded.

If allocation, hashing, equality, or move/copy can fail, retain the old table until destination completion. Node indirection or cached hashes can avoid moving/rehashing expensive payloads, but new bucket/probe metadata still changes. A strong guarantee may require copyability/no-throw move or a rollback/basic guarantee. `rehash` and `reserve` API contracts must name these conditions.

Stop-the-world cost is `Theta(n)` placement work plus destination initialization, with peak memory roughly old plus new plus temporary state. Amortized analysis can charge geometric growth across prior insertions, but it does not erase the single-operation latency or memory spike.

**Triggers combine correctness and workload policy.** Growth commonly considers prospective live load `n/m`; open addressing also considers fill/tombstones and required EMPTY reserve. Same-size rebuild handles tombstone accumulation, collision layout, or seed change. Shrink should use a lower threshold than growth and require a target capacity with sufficient headroom.

Use hysteresis: for example, grow above a measured upper bound and shrink only below a materially lower bound after sustained evidence. Exact numbers depend on representation, key/value size, allocator, misses, iteration, latency, and memory budget. Do not copy another library's threshold without its layout/workload.

`reserve(x)` translates desired live entries through maximum load using checked ceiling arithmetic and selects a legal capacity. Guard multiplication, addition, shifts, next-prime/power calculations, byte size, alignment, and allocator maximum. Maximum capacity must return a typed failure rather than wrap to a smaller table or loop.

**Incremental migration needs a state machine.** A simple chaining design holds old table `O`, new table `N`, and cursor `c`. Before migration, only `O` exists. Starting growth allocates empty `N`, sets cursor zero, and routes new inserts to `N`. Each help step transfers one or more old buckets. Completion drops `O` and returns to one-table state.

For cursor state:

- `O[i]` is empty for every `i<c`;
- entries in `O[i]` for `i>=c` are old-owned unless individually transferred;
- all `N` entries obey new placement;
- no logical key appears in both tables;
- total logical size equals old plus new live entries.

Lookup computes the full hash once, checks `N` first, then checks the old bucket only if that bucket is not already migrated. New-first prevents a stale old copy from superseding a newer new value in designs that temporarily permit shadowing; the stricter executable design never permits duplicates.

**Writes choose one authority.** New keys enter `N`. For an existing key found in `N`, update there. If found old-owned, a clean policy removes/transfers the complete entry to `N`, applies the update, then leaves no old copy. Delete finds/removes whichever authority owns the key. A write racing migration must serialize or validate so migration cannot resurrect an old value after update/delete.

Alternative shadowing designs can leave an obsolete old copy plus a new authoritative copy, but then they need tombstone/version rules so lookup, migration, delete, count, iteration, and completion distinguish them. Exact-once physical ownership is simpler when payload movement supports it.

**Bucket migration is an exact-once transaction.** Freeze/exclusively own old bucket `c`. Detach or enumerate its entries. For each, recompute new bucket from full hash and construct/link it in `N`, resolving any concurrent/new copy according to authority. Only after every entry is safely represented may old bucket become empty and cursor advance.

If the operation fails mid-bucket, retain a per-entry authority log, roll back new insertions, or expose a documented moving state. Advancing early makes remaining entries unreachable because routing skips migrated old buckets. Copying before removing without duplicate rules can double count and deliver stale values.

The executable implementation uses immutable Python tuples and exclusive sequential execution. It can remove an old-owned key, place/update it in `N`, and transfer whole buckets without callback failure. Its finite trace proves that state machine only, not generic allocation/lifetime safety.

**A unit count is not a time bound.** In separate chaining, one bucket may contain `Theta(n)` entries under a poor hash. “One bucket per command” then permits an unbounded pause. Limit entries, bytes, or elapsed time, but a partially migrated bucket needs finer authority metadata. Tree bins, node lists, and destructor/hash cost further change work.

Open addressing is harder to slice by physical bucket because entries' reachability depends on probe sequences and EMPTY boundaries. Migrating one slot can break old search unless the old table remains queryable with moved markers/shadowing. Cluster/group/table partitions, forwarding metadata, or directory indirection can form safer units.

Current Go's Swiss design solves this at another level: each individual Swiss table is a complete probe-dependent table, while the map directory partitions the hash space. An individual table is bounded in size; it can rebuild/split all at once without copying the entire map. This bounds growth work by the maximum subtable, not by pretending a group transfer is independently valid.

**Progress must survive workload shape.** If only mutating operations help migration, a read-only map can retain two tables forever. That may be acceptable if no further write occurs, but memory debt persists. Background work, lookup helping, scheduled maintenance, or forced completion can guarantee progress with different synchronization/latency costs.

Measure debt in remaining entries/bytes/units and age. Apply a bounded help quota per operation or time slice. Avoid long scans over empty old buckets by bounding empty visits as well as migrated entries. Redis's current source explicitly limits empty-bucket visits and offers operation-triggered plus time-budgeted rehash functions; these details are source scoped.

Paused safe iterators or snapshots may block movement. Define whether iteration pauses rehash, traverses both tables, uses versions, or snapshots logical entries. A pause counter must be exception-safe so cancellation cannot freeze migration indefinitely. Operational telemetry should expose paused duration and debt.

**Nested resize triggers require policy.** While growing, new table load may itself cross a threshold because migration is slow or writes surge. Options include increase the destination before starting, finish current migration synchronously, allow a larger destination replacement with rollback, or support a carefully specified multi-generation scheme. Silently starting a third ambiguous table is not acceptable.

Shrink during growth should normally wait. Same-size cleanup during growth may be redundant. Reserve should calculate a destination sufficient for current logical size plus request/headroom. Rate-limit oscillation and repeated allocation failure. A seed-change attack response may require immediate rebuild even without load change, but must have retry/resource limits.

**Iteration and order are part of the contract.** Iterating both tables risks duplicates or misses when entries move. A single-threaded iterator can pause migration and traverse old/new exactly once. A versioned iterator may tolerate moves with documented weak semantics. A snapshot can copy logical entries. Current Go specifies map-iteration behavior under mutation; its source must implement those language semantics, not generic expectations.

Physical iteration order changes on every rebuild and during migration. References/pointers may remain stable with node indirection even as bucket links move, while flat values relocate. State iterator, reference, handle, and entry-view validity separately for insert, migrate step, rehash, delete, and clear.

Logical serialization should not expose two-table state. Serialize unique key/value entries with a versioned semantic format. A physical checkpoint needs stable snapshot coordination, exact capacity/hash/seed/metadata formats, authority markers, endian/layout compatibility, and validation; never leak secret seeds casually.

**Concurrency turns migration into publication and reclamation.** A concurrent lookup can race a transfer between its checks. A writer can update the old entry while migration copies it. Multiple helpers can claim the same unit. Completion can free old storage while a reader still holds its address.

Use locks, atomic unit states, forwarding nodes, versions, or descriptors to define one linearization and authority protocol. Helpers claim disjoint units or cooperate idempotently. Lookup validates table generation/unit state and retries when transfer overlaps. Writes lock/validate both relevant authorities. Memory ordering publishes destination payload before forwarding/new-owned state.

OpenJDK's current `ConcurrentHashMap` source has transfer indices and forwarding/control machinery for cooperative resizing. Its exact node/bin/lock semantics belong to that implementation. A custom table cannot inherit its guarantees by naming a `transferIndex`.

Retire old arrays only after all units transferred, helpers finished, and preexisting readers/iterators excluded through locks, epochs, hazard pointers, reference counts, GC, or the language runtime. Logical completion and memory reclamation are distinct events.

**Resource and security concerns persist.** Rehash can become an attacker-amplified `Theta(n)` operation. Collision-heavy old buckets defeat bucket-count latency budgets; repeated chosen inputs can force grow/reseed cycles; peak two-table memory can exhaust the process. Secret hashing reduces predictable collisions but does not bound allocation or migration work.

Enforce entry/byte/capacity/rehash/retry/time limits, robust hash policy, backpressure, telemetry, and alternate structures. Preserve the old logical map on failed rebuild. Record trigger/reason, old/new capacity, live/fill, debt units/entries/bytes, help work and duration, empty scans, operation retries, paused iterators, allocations/peak memory, failures, completion age, and latency percentiles.

**Testing must exercise every mixed state.** Model-test put/update/get/delete/reserve/rehash/shrink/clear against a reference map. After every operation assert unique logical keys, size equals old plus new, old buckets below cursor empty, each entry placed under its table's rule, and lookup routing finds its authority.

Enumerate small capacities and interleave help before/after every write/read/delete. Force all entries in one old bucket, empty spans, update/delete of next-to-migrate key, insertion during migration, duplicate candidates, completion boundary, second resize trigger, same-size rebuild, shrink hysteresis, maximum arithmetic, allocation/hash/equality/move/destructor failure, iterator pause/cancel, and stalled progress.

For concurrent variants, record histories for linearizability, delay at claim/copy/publish/advance/retire points, run multiple helpers, update/delete during transfer, force resize-on-resize, and use race/reclamation tools. A green sequential map test does not establish concurrent safety.

Benchmark stop-the-world and incremental strategies over realistic/adversarial hashes, live/fill loads, read/write/delete mixes, chain/cluster distributions, help budgets, iterator behavior, payload sizes/layouts, cache/NUMA, memory pressure, locks/retries, throughput, p50/p95/p99/max operation latency, peak memory, and time-to-completion. Report amortized totals and individual tails.

The executable trace below verifies a finite sequential two-table chained map. It migrates one bucket, inserts during migration, transfers an old-owned key on update, completes bounded cursor steps, deletes in the new table, and checks exact placement/authority/count invariants throughout.

<!-- bijux-verify: {"id":"incremental-rehash-authority-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cursor_after_first=1\nold_remaining_after_first=1\nupdate_one_authority=new\nlookup_eight=EIGHT\nfinal_capacity=8\nkeys=0,1,5,8\nsize=4\ninvariant=True\nevidence=finite_incremental_rehash_trace\n","stderr":""}} -->
```python
class IncrementalMap:
    def __init__(self, capacity):
        self.current = [[] for _ in range(capacity)]
        self.old = None
        self.cursor = None
        self.size = 0

    @staticmethod
    def bucket(table, key):
        return hash(key) % len(table)

    @classmethod
    def find(cls, table, key):
        index = cls.bucket(table, key)
        for position, entry in enumerate(table[index]):
            if entry[0] == key:
                return index, position
        return None

    def locate(self, key):
        found = self.find(self.current, key)
        if found is not None:
            return "new", self.current, found
        if self.old is not None:
            old_index = self.bucket(self.old, key)
            if old_index >= self.cursor:
                found = self.find(self.old, key)
                if found is not None:
                    return "old", self.old, found
        return None

    def put(self, key, value):
        located = self.locate(key)
        if located is not None:
            authority, table, (bucket_index, position) = located
            if authority == "new":
                table[bucket_index][position] = (key, value)
                return False, authority
            table[bucket_index].pop(position)
            destination = self.bucket(self.current, key)
            self.current[destination].append((key, value))
            return False, "new"
        destination = self.bucket(self.current, key)
        self.current[destination].append((key, value))
        self.size += 1
        return True, "new"

    def get(self, key):
        located = self.locate(key)
        if located is None:
            raise KeyError(key)
        _, table, (bucket_index, position) = located
        return table[bucket_index][position][1]

    def delete(self, key):
        located = self.locate(key)
        if located is None:
            raise KeyError(key)
        _, table, (bucket_index, position) = located
        value = table[bucket_index].pop(position)[1]
        self.size -= 1
        return value

    def start_rehash(self, capacity):
        assert self.old is None and capacity > 0
        self.old = self.current
        self.current = [[] for _ in range(capacity)]
        self.cursor = 0

    def migrate_step(self, units=1):
        while self.old is not None and units > 0:
            entries = self.old[self.cursor]
            for key, value in entries:
                assert self.find(self.current, key) is None
                destination = self.bucket(self.current, key)
                self.current[destination].append((key, value))
            self.old[self.cursor] = []
            self.cursor += 1
            units -= 1
            if self.cursor == len(self.old):
                self.old = None
                self.cursor = None

    def invariant(self):
        keys = []
        for table in (self.current,) if self.old is None else (self.current, self.old):
            for bucket_index, entries in enumerate(table):
                for key, _ in entries:
                    if self.bucket(table, key) != bucket_index:
                        return False
                    keys.append(key)
        if self.old is not None:
            if any(self.old[index] for index in range(self.cursor)):
                return False
        return len(keys) == self.size and len(set(keys)) == self.size


table = IncrementalMap(4)
for key, value in ((0, "ZERO"), (4, "FOUR"), (1, "ONE")):
    assert table.put(key, value)[0]
table.start_rehash(8)
table.migrate_step()
cursor_after_first = table.cursor
old_remaining_after_first = sum(len(bucket) for bucket in table.old)
assert table.put(8, "EIGHT")[0]
inserted, update_authority = table.put(1, "ONE_UPDATED")
assert not inserted and table.get(1) == "ONE_UPDATED"
assert table.put(5, "FIVE")[0]
lookup_eight = table.get(8)
while table.old is not None:
    table.migrate_step()
assert table.delete(4) == "FOUR"

keys = sorted(key for bucket in table.current for key, _ in bucket)
print(f"cursor_after_first={cursor_after_first}")
print(f"old_remaining_after_first={old_remaining_after_first}")
print(f"update_one_authority={update_authority}")
print(f"lookup_eight={lookup_eight}")
print(f"final_capacity={len(table.current)}")
print("keys=" + ",".join(map(str, keys)))
print(f"size={table.size}")
print(f"invariant={table.invariant()}")
print("evidence=finite_incremental_rehash_trace")
```

## Definitions and Notation

- `O,N`: old and new physical tables during migration.
- `m,m'`: old and destination capacities.
- `c`: cursor/index of the next old migration unit.
- `n`: logical live entry count across both tables.
- **authority**: representation whose copy controls the current logical value.
- **migration unit**: bucket/group/partition/table transferred under one state transition.
- **growth debt**: remaining units, entries, or bytes not yet migrated.
- **help quota**: bounded migration work assigned to an ordinary/background operation.
- **forwarding marker/version**: metadata routing or invalidating operations during transfer.
- **retirement**: logical removal and later safe reclamation of old storage.

## Mechanisms, Invariants, or Proof Structure

Stop-the-world correctness is a bijection from source live entries to destination entries under new placement, with source retained until destination validation/publication. Incremental correctness strengthens this with an authority partition: old units before cursor are empty/new-owned; later units may be old-owned; all new writes use or transfer to new authority.

Lookup/update/delete correctness follows routing plus exact-once uniqueness. Unit migration computes new placement for every resident, publishes safely, empties old ownership, then advances metadata. Completion follows when debt is zero and no operation can retain old references; reclamation may occur later.

Progress and latency proofs count representation-appropriate entries/bytes/time, not merely nominal units. Concurrent proofs additionally establish claims, revalidation, linearization, helping, memory order, generation changes, and reclamation.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Stop-the-world rebuild | simple authority/failure proof | single latency and peak-memory spike |
| Two-table cursor migration | bounded bucket progress | mixed routing and huge-bucket risk |
| Entry/byte/time-budget migration | tighter latency control | partial-unit authority metadata |
| Directory/subtable splitting | bounded local rebuild | indirection/directory and split semantics |
| Cooperative concurrent transfer | parallel progress | claims, forwarding, retries, reclamation |
| Same-size rebuild | clears tombstones/history | full movement without new capacity |
| Background migration | independent progress | scheduler, contention, shutdown coordination |
| Operation helping | amortizes work naturally | read-only stall or foreground latency |

## Failure Modes and Misconceptions

- **“Resize is memcpy.”** placement depends on capacity/hash/layout.
- **“Rehash always grows.”** cleanup or reseeding may retain capacity.
- **“Check new only.”** old-owned keys remain until their unit transfers.
- **“Check old first.”** a stale old representation can shadow newer authority.
- **“Temporary duplicates are harmless.”** count/update/delete/iteration need explicit shadow/version semantics.
- **“Cursor advance is progress.”** it is valid only after exact transfer and old-unit emptying.
- **“One bucket bounds latency.”** a bucket can contain many expensive entries.
- **“Amortized constant means no pause.”** total charging does not bound operation tails.
- **“Helping guarantees completion.”** workload, pauses, failures, or contention can stall it.
- **“Shrink at low load immediately.”** absent hysteresis, workloads oscillate.
- **“Logical completion frees memory.”** readers may still require deferred reclamation.
- **“Concurrent transfer is sequential transfer with atomics.”** authority, linearization, retries, and lifetime differ.

## Worked Examples

### Example 1

Key 5 in capacity four belongs to bucket one; after growth to eight it belongs to bucket five. Conclusion: old bucket indices cannot be copied.

### Example 2

Old bucket zero holds keys 0,4 under capacity four. Migrating to eight places them in new buckets zero and four, empties old zero, then advances cursor. Conclusion: full hashes/new reduction drive transfer.

### Example 3

After cursor reaches one, lookup key 4 checks new bucket four and does not consult old bucket zero. Conclusion: migration metadata narrows routing.

### Example 4

Key 1 remains in old bucket one, then update transfers it to new bucket one and changes the value. Conclusion: a write establishes one new authority rather than leaving duplicates.

### Example 5

A map has one old bucket with one million constant-hash entries. Migrating “one bucket” is `Theta(n)`. Conclusion: count entries/bytes/time for latency.

### Example 6

At grow threshold 0.8 and shrink threshold 0.75, alternating one insertion/deletion can resize repeatedly. A shrink threshold 0.3 plus sustained evidence creates hysteresis. Conclusion: threshold separation prevents oscillation.

### Example 7

A safe iterator pauses migration, throws, and fails to decrement the pause counter. Debt never progresses. Conclusion: pause ownership needs RAII/finally/cancellation safety.

### Example 8

A writer updates old key K while a helper has copied its former value but not advanced authority. Without locking/version validation, the helper can publish stale K. Conclusion: migration and writes serialize on logical authority.

### Example 9

All entries have transferred, but a reader holds an old bucket pointer from before completion. Conclusion: logical retirement precedes safe memory reclamation.

### Example 10

Stop-the-world has lower total CPU but a 40 ms p99 spike; incremental adds 8% CPU and keeps p99 under 2 ms while doubling memory longer. Conclusion: selection balances totals, tails, and overlap.

## Cross-Program Connections

- **Algorithms:** amortized analysis, incremental transformations, work/debt potentials, and hashing placement justify cost and progress.
- **Programming languages:** allocation, exceptions, moves, destructors, iterators, and ownership define failure and retirement.
- **Computer architecture:** peak memory, cache/TLB behavior, prefetch, NUMA, and bandwidth shape migration cost.
- **Software engineering:** explicit state machines and observability prevent transitional authority from becoming permanent ambiguity.
- **Database engineering:** online index rebuild, compaction, partition splits, and dual-read migration share authority/cutover problems.
- **Concurrent programming:** helping, forwarding, versions, linearization, epochs, and hazard reclamation govern cooperative transfer.
- **Security engineering:** collision-heavy units and repeated rebuild triggers amplify CPU and memory denial of service.

## References

1. Redis Project, [`dict.c`](https://github.com/redis/redis/blob/unstable/src/dict.c). Current primary source for two tables, cursor/bucket transfer, bounded empty visits, operation helping, time-budgeted rehash, lookup/delete routing, and pause behavior.
2. Redis Project, [`dict.h`](https://github.com/redis/redis/blob/unstable/src/dict.h). Current primary representation/API source for old/new tables, used counts, cursor, pause state, iterators, and rehash functions.
3. Go Project, [runtime maps `map.go`](https://github.com/golang/go/blob/master/src/internal/runtime/maps/map.go). Current primary source for directory-selected Swiss tables, capped table growth, splits, and iterator requirements.
4. Go Project, [Faster Go Maps with Swiss Tables](https://go.dev/blog/swisstable). Official engineering explanation of bounded incremental growth through capped subtables and extendible hashing.
5. OpenJDK Project, [`ConcurrentHashMap.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/concurrent/ConcurrentHashMap.java). Current primary source for cooperative transfer, transfer index, forwarding/control states, lookup, and concurrency.
6. Abseil Project, [`raw_hash_set.h`](https://github.com/abseil/abseil-cpp/blob/master/absl/container/internal/raw_hash_set.h). Current whole-table probe/layout source used to scope monolithic rebuild and relocation behavior.
7. Rust Project, [`std::collections::HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current reserve, shrink, capacity, iteration, hashing, and invalidation/API context.
8. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Observable load, rehash, complexity, hash/equality, and invalidation requirements without a resize algorithm mandate.
9. ISO C++ working draft, [Unordered Container Exception Guarantees](https://eel.is/c%2B%2Bdraft/unord.req.except). Current rehash/insert/erase exception-safety requirements for comparison with custom containers.
10. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/legacy/event/sec03/tech/full_papers/crosby/crosby.pdf). Primary collision-driven resource-attack evidence relevant to migration units and repeated rebuilds.

## Exercises

### Exercise 1

Specify a failure-atomic stop-the-world rebuild for a generic map. Include capacity arithmetic, full-hash placement, duplicate/count proof, payload lifetime, publication, invalidation, and maximum-capacity failure.

### Exercise 2

Give get/put/update/delete/migrate-step pseudocode for cursor-based incremental chained rehash. Prove exact-once authority and explain why new-first lookup alone is insufficient without a duplicate policy.

### Exercise 3

Replace one-bucket helping with an entry/byte/time budget that permits partial bucket migration. Design metadata so lookup, writes, failure, and concurrent helpers know which entries are authoritative.

### Exercise 4

Design grow, shrink, same-size cleanup, reserve, nested-trigger, iterator, serialization, progress, retirement, and telemetry policies for a latency-sensitive service under memory pressure.

### Exercise 5

Design property/fault/concurrency tests and a benchmark comparing stop-the-world, cursor-based, and partition-split growth. Include adversarial collisions and prove the reported metrics cover completion rather than only steady-state lookup.

## Answers to the Exercises

### Answer 1

Compute required destination from requested live capacity and maximum load with checked ceiling arithmetic, legal capacity selection, byte/alignment/allocator limits, and a typed maximum failure. Allocate empty destination while retaining source. Enumerate each live logical entry exactly once, recompute placement from full hash under new capacity/seed, construct/insert with duplicate prohibition, and track destination count/invariants. On allocation/hash/equality/move failure, destroy partial destination and preserve source unless a documented recoverable basic guarantee applies. After exact count/content validation, atomically/exclusively publish destination, then retire/reclaim source after readers/iterators are excluded. State relocation invalidation. Tombstones/old slots/bitmaps are not copied as logical entries.

### Answer 2

During migration, get checks N, then O only if the old bucket is not migrated. Put checks both; new keys enter N. Update in N mutates N; update in O transfers/removes old ownership then writes N. Delete removes the found authority. Migrate claims bucket c, transfers each old entry to its recomputed N bucket unless an explicit newer authority policy says otherwise, empties O[c], then advances c; at old capacity, retire O. Invariant: buckets below c empty, remaining O entries valid old placements, all N entries valid new placements, unique union size n. New-first lookup determines precedence but does not stop duplicate copies from breaking size, iteration, later delete, or migration overwrite; either forbid duplicates physically or add explicit version/shadow/tombstone semantics everywhere.

### Answer 3

Give each old bucket a state plus per-entry or detached-list cursor: OLD, MOVING(position/generation), NEW. A helper claims the unit generation, detaches a bounded prefix or records entry identities, and transfers until entry/byte/deadline budget. Entries individually transition by locking/version/CAS from old authority to new; lookup checks N then old entries not marked transferred and validates generation. Writes either claim/transfer the target entry or update the current version. Failures leave untransferred entries old-owned and transferred entries new-owned; helper resume is idempotent. Multiple helpers claim disjoint ranges or validate versions. Bucket becomes NEW only after no old-owned entries remain. This metadata complexity is the price of a genuine time/byte rather than nominal bucket bound.

### Answer 4

Grow on prospective live/fill/EMPTY/probe budget; same-size rebuild on tombstone/probe/seed pressure; shrink below a materially lower sustained threshold with target headroom and rate limits. Reserve uses checked requested capacity and can finish/replace current migration under one defined nested policy. Bound help by entries/bytes/time and guarantee background or forced progress for read-only/stalled cases; expose debt age. Iterators pause with exception-safe ownership, validate versions, or snapshot/traverse generations under documented semantics. Serialize logical unique entries, not transitional tables/seeds. Retire after zero debt/helpers and reclaim after reader grace. Track triggers, capacities, loads, debt units/entries/bytes/age, help work/duration, empty scans, pauses, retries, allocations/peak memory, failures, completion time, throughput, and latency percentiles; enforce memory/capacity/retry/time limits.

### Answer 5

Generate logical operations against a reference map and interleave migration at every boundary; assert unique union, exact size, cursor/unit state, old/new placement, lookup authority, and eventual completion. Force huge/empty buckets, tombstones/clusters as applicable, writes/deletes to moving entries, inserts during migration, completion and nested triggers, grow/shrink oscillation, maxima, callback/move/allocation failure, iterator pause/cancel, and stalled helping. Concurrent tests delay claim/copy/publish/advance/retire, run helpers with updates/deletes/resizes, check linearizable histories, races, and reclamation. Benchmark realistic/adversarial hashes over sizes, loads, operation mixes, unit budgets, payloads, cache/NUMA, locks/retries, and memory pressure. Report total CPU, per-operation tails, peak overlap, debt/completion age, moves/bytes/empty scans, failures/retries, throughput, hardware/toolchains, repetitions, uncertainty, and raw artifacts—not lookup alone after migration finishes.
