---
module_id: DSE-026
program: Data Structures Engineering
level: 1
module_number: 26
title: Cuckoo Hashing
status: complete
last_verified: 2026-08-30
---

# Cuckoo Hashing

## One-Page Review

### Governing question

How can a hash table give each key a small fixed set of candidate locations and relocate occupants on insertion while preserving placement feasibility, bounded lookup, transactional failure, and honest probabilistic claims?

### Essential definitions

- **cuckoo hashing** gives each key two or more candidate locations; insertion may evict and relocate existing keys.
- In the classic two-table scheme, key `k` belongs in `T0[h0(k)]` or `T1[h1(k)]`.
- A **cuckoo graph** has table cells as vertices and one edge per key joining its two candidates.
- A **placement/orientation** assigns every key edge to one endpoint with each single-slot vertex receiving at most one edge.
- An **augmenting path** starts at a candidate of the new key and follows resident keys to alternate candidates until reaching EMPTY.
- A **kick-out chain** performs those evictions, sometimes choosing victims greedily or randomly.
- A **cycle/failure** means a bounded insertion procedure found no placement; it does not necessarily mean all physical slots are occupied.
- **rehash/reseed** chooses new hash functions and reinserts every key; **resize** also changes capacity.
- A **stash** is a small separately searched overflow area for keys not placed in the main graph.
- **bucketized cuckoo hashing** gives each candidate bucket several slots, changing load thresholds, graph/hypergraph analysis, and lookup work.

### Central model, mechanism, or theorem

For a classic two-table single-slot map, represent each key as an edge between its two candidate cells. A placement orients each edge toward the cell storing it, with indegree at most one. A connected component is placeable exactly when it is a pseudoforest—its edge count does not exceed its vertex count. A component with two independent cycles has more edges than vertices and cannot be placed without a stash, new hash functions, more capacity, buckets, or candidates.

Lookup checks exactly the candidate cells (plus a governed stash), filters by hash/fingerprint, and confirms equality. Deletion clears the one cell containing the key; it does not break a probe chain. Insertion is the hard operation. A transactional breadth-first search can discover an EMPTY endpoint first, then move residents backward along the path and publish the new key. If no path exists within the complete reachable component, the current placement problem is infeasible; if the search is deliberately bounded, exhaustion is only an operational failure and must trigger a controlled fallback.

### Critical invariants

1. Every live key appears exactly once in one of its current candidate slots or a documented stash.
2. Candidate derivation is deterministic for stable key/hash state and produces valid, sufficiently distinct buckets.
3. Lookup examines all candidate buckets and stash entries, then confirms equality; fingerprints are filters only.
4. An augmenting path alternates buckets and resident keys and ends at a genuinely EMPTY slot.
5. Relocation moves every displaced key only to its alternate legal location and preserves one live owner throughout the failure contract.
6. Duplicate detection occurs before insertion publishes a second equivalent key.
7. Failed bounded search, allocation, construction, move, hash, or rehash leaves the stated prior/recoverable state.
8. Rehash/resize recomputes every candidate under new capacity/seeds and publishes an exact-once placement.
9. Load, stash size, search/kick budget, hash assumptions, concurrency, and security limits are explicit.

### Common failures

- Deriving two identical or strongly correlated candidates and counting them as two choices.
- Starting evictions before checking whether an equivalent key already occupies another candidate.
- Randomly kicking until an unbounded loop rather than enforcing a budget and fallback.
- Treating kick-budget exhaustion as proof that the graph is infeasible.
- Moving a resident to a cell that is not its alternate candidate.
- Overwriting an occupant before safely retaining its complete key/value/hash state.
- Rehashing with the same failing seeds and unchanged capacity indefinitely.
- Claiming classic lookup is worst-case two memory accesses while using buckets, stash, locks, retries, or equality collisions.
- Applying the classic near-half total-slot load regime to bucketized or multi-choice variants.
- Assuming a stash fixes arbitrary hash flooding or can grow without bound.

### Compact example

Let keys carry explicit candidates `(T0 index,T1 index)`. A occupies `T0[0]`; C occupies `T1[1]`. Inserting D with candidates `(0,1)` sees both occupied. A's alternate `T1[0]` is empty, so the path `T0[0] -> T1[0]` moves A and installs D. After another `(0,1)` key occupies the second endpoint, a further parallel edge makes that two-vertex component have three competing edges and no single-slot placement. The executable trace finds the path transactionally and reports the later failure without corrupting the table.

### Connections

[DSE-021](021-hash-functions-and-distribution.md) owns hash independence and reduction; [DSE-023](023-linear-probing.md), [DSE-024](024-quadratic-probing-and-double-hashing.md), and [DSE-025](025-robin-hood-hashing.md) provide non-relocating and displacement-balancing contrasts. The [program roadmap](../ROADMAP.md) next covers hopscotch neighborhoods, resizing, and hash-flooding resistance.

## Governing Question

Which candidate scheme, graph invariant, insertion search, relocation transaction, failure fallback, and evidence make cuckoo hashing correct and operationally bounded for real keys, values, threads, and adversaries?

## Why This Matters

Cuckoo hashing moves complexity away from lookup. A classic successful or unsuccessful lookup examines two known cells rather than scanning an unbounded cluster. Deletion can clear a cell directly. Independent candidate addresses may expose memory-level parallelism. These properties suit read-heavy in-memory indexes, packet-processing tables, filters, and concurrent maps.

Insertion pays the debt. A new key can displace a resident, which displaces another, producing a long path or cycle. A table may have many EMPTY slots yet be unable to place a key because its connected cuckoo-graph component has no free orientation. Randomized success statements depend on load, capacity convention, hash-family independence, bucket width, candidate count, key set, and failure policy.

Engineering adds payload lifetime, rollback, duplicate updates, stash bounds, resize latency, references, serialization, NUMA/cache behavior, concurrency, and hostile inputs. An implementation that merely limits a random kick loop can be safe, but it cannot label every limit hit “table full” or silently lose the currently evicted key.

## Prerequisites and Retrieval

Retrieve abstraction, representation, operation, cost, layout, genericity, iteration, testing, and benchmarking tools from [DSE-001](001-abstract-data-types-and-concrete-representations.md) through [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve hash/reduction/security assumptions from [DSE-021](021-hash-functions-and-distribution.md), collision-layout contrast from [DSE-022](022-separate-chaining.md), three-state open addressing from [DSE-023](023-linear-probing.md), probe-family arithmetic from [DSE-024](024-quadratic-probing-and-double-hashing.md), and relocation/lifetime lessons from [DSE-025](025-robin-hood-hashing.md).

## Learning Objectives

After completing this module, you should be able to:

1. model classic cuckoo placement as graph orientation;
2. distinguish physical capacity, candidate reachability, and graph feasibility;
3. implement lookup/update/delete with exact duplicate and equality semantics;
4. discover and commit an augmenting path transactionally;
5. design bounded kick/search, rehash, resize, reseed, and stash fallbacks;
6. separate classic, bucketized, multi-choice, stash, and filter variants;
7. state load and probability claims with their hash/model assumptions;
8. design payload lifetime, invalidation, concurrency, and security contracts;
9. test graph excess, cycles, rollback, and adversarial candidate structure;
10. benchmark lookup simplicity against insertion tails, movement, retries, and memory.

## Core Exposition

**Define the candidate contract.** In the classic construction, two arrays `T0,T1` each have `m` single-entry cells. Key `k` has candidates `(0,h0(k))` and `(1,h1(k))`. The table contains a key only in one of those cells. The two table tags make the vertices distinct even if the numeric indices match.

One high-quality full hash can sometimes derive two bucket indices through domain-separated mixing, but “two formulas” does not imply independence. Identical candidates within one physical bucket layout reduce choice. Hash-family theory must match the derivation actually deployed. Equal keys must yield compatible candidate sets; indexed key state must not mutate.

Unique-map lookup computes both candidates, checks occupied metadata/fingerprints, then equality. It may issue independent bucket reads in parallel where the machine and layout support it, but observable work includes both buckets, stash, synchronization/version retries, hash bytes, and equality candidates. A fingerprint mismatch is not proof about an equal key unless the fingerprint contract follows from the same compatible hash.

Update checks all legal locations before changing the existing value. Insertion likewise excludes an existing equivalent key before relocation. Otherwise two equivalent keys can occupy the two candidates and make later update/delete ambiguous. Construction failure must leave the existing map unchanged under the documented guarantee.

Deletion locates the exact key and clears/destroys that cell. No later key relies on a linear probe-history terminator, so tombstones are unnecessary in the classic sequential representation. Concurrent deletion still needs publication order and reclamation; bucketized layouts may maintain compact slot metadata but not linear-probing reachability tombstones.

**The cuckoo graph explains feasibility.** Create one vertex for each cell in both arrays and one edge for each key between its candidates. Storing a key at an endpoint orients its edge toward that vertex. Single-slot capacity requires indegree at most one.

A tree component with `e=v-1` has at least one empty vertex and can orient edges toward all other vertices. A unicyclic component with `e=v` can occupy every vertex. A connected component with `e>v` has more keys than cells and is impossible. Thus the classic graph is placeable exactly when every component is a pseudoforest. Parallel edges and self-like candidate degeneracy must be modeled honestly; three parallel keys competing for two vertices fail.

This is stronger than global load. Ten empty cells in other components cannot help an overfull component whose keys have no edges to them. A new seed or capacity changes graph edges/vertices and may repair placement. A stash removes selected edges from the main graph, reducing component excess at the cost of extra lookup state.

**Insertion searches for an augmenting path.** Start from both candidate vertices of the new key. If either is EMPTY, construct there. Otherwise each resident key has one alternate endpoint. Breadth-first search explores these alternating edges until it finds EMPTY. The path has bucket vertices `b0,...,bt`; the resident at `b_i` can legally move to `b_(i+1)`. Commit from the empty end backward, then place the new key at `b0`.

Planning before mutation distinguishes search from publication and often finds shorter relocation paths than blind kicking. It consumes a visited set/queue and can be bounded for latency. A complete search of the reachable finite component that finds no EMPTY proves no augmenting path for the current orientation; in the classic pseudoforest setting, adding the edge may be infeasible. A deliberately capped search does not prove that: a longer path may exist.

Random-walk insertion instead chooses a candidate, evicts its resident, and carries that key to its alternate, repeating until EMPTY. It uses little planning memory and is central to classic descriptions, but requires a kick limit. On limit exhaustion, the carried key remains live logical state that must enter a stash or transactional rehash/rollback; it must never be dropped. Deterministic victim rules can cycle; randomization changes probability, not the need for a bound.

**Commit order governs lifetime safety.** For trivial records, reverse-path assignment is straightforward. For owning or failure-prone values, overwriting the predecessor before the resident has a safe destination can destroy the only copy. Options include no-throw moves, node/payload indirection, preconstructed temporary ownership, a relocation log with rollback, copy-on-write table construction, or a documented basic guarantee with all entries recoverable.

The new key/value should be fully constructed before any slot is marked occupied. Cached hashes/fingerprints and payload references move together. Reverse commit starts from known EMPTY, so each move has vacant destination; publish metadata only after payload initialization and clear the source only when ownership transferred. If callbacks can throw during path planning, no physical state should yet have changed.

**Failure is a designed transition.** An insertion can fail because the graph is unplaceable, a search/kick budget expires, a stash is full, maximum capacity is reached, allocation fails, a callback fails, or concurrent validation repeatedly aborts. These causes have different remedies and telemetry.

Common fallback order is: try bounded placement; if configured, place in a bounded stash; otherwise choose new independent seeds and reinsert all entries; grow if load/graph risk or retry policy requires; stop after a governed attempt/resource limit and report failure. Reusing exactly the same candidates recreates the same structural obstruction. Infinite rehash is not resilience.

Rehash/resize builds a new table from the complete logical set, including the pending/carried key and stash. Recompute every candidate with new seeds/capacity, place each exactly once, and publish only after success. Retain the old table for rollback or readers under the concurrency protocol. Checked arithmetic governs bucket counts, stash, queue memory, and reserve calculation.

**Load conventions must name the denominator.** In two arrays of `m` single cells, total physical capacity is `2m`; `n/(2m)` is total-slot load, while papers may parameterize `n/m`. The classic random-graph transition occurs near one key per side-size—near one-half of total single-slot capacity—not near a universally applicable “50% hash-table load” rule.

Bucketized cuckoo tables give each candidate bucket `b>1` slots; multi-choice variants use `d>2` hashes. They can support much higher measured loads but lookup touches up to `d` buckets and filters multiple slots. Their feasibility is a capacitated graph/hypergraph problem with different thresholds. Do not transfer classic constants, stash bounds, or failure probabilities without the exact theorem.

The original Pagh-Rodler analysis gives expected constant lookup and amortized insertion under specified universal/random assumptions and rehash rules. Later stash work bounds failure under particular fully random or explicit hash families, stash size, load, and loop budget. A later generalized-stash paper reports a counterexample to an earlier generalized analysis. This correction is a useful engineering lesson: probability claims are specifications with proof dependencies, not folklore.

**A stash trades main-table failure for another bounded structure.** Lookup must search the stash as well as candidates. Delete/update must find either location. Rehash should retry stash entries; deletion may open paths that allow draining it. Stash size must be bounded and instrumented. If it becomes a general overflow list, lookup is no longer fixed small work and an attacker can concentrate it.

Stash entries own full payloads and hashes under the same exception/concurrency policy. A hardware or cryptographic setting may choose stash size from a target failure probability, but only under the matching key/hash/adversary model. Adaptive adversaries who learn seeds or observe placements need a different analysis.

**Layout controls bucket cost.** Classic two arrays give two isolated reads but low total-slot utilization. Bucketization amortizes metadata/cache lines and improves placement flexibility. Separate fingerprints filter equality; partial keys must never create false negatives. Inline payloads simplify ownership but make kick chains move large values. Node/dense indirection moves pointers/indices, improving relocation and reference stability at allocation/index-repair cost.

Current `libcuckoo` is a bucketized concurrent C++ implementation with a source-defined algorithm, bucket slot count, partial-key paths, locks, reserve/rehash, and multiwriter behavior. Current DPDK hash code uses eight-entry cuckoo buckets and exposes explicit concurrency/RCU-related configuration. These are scoped systems, not instantiations of the classic single-slot theorem.

Iteration scans tables/buckets plus stash and may be `O(capacity)`. Relocation changes physical order; rehash changes candidates; deletion destroys a value. State iterator/reference invalidation per operation. Logical serialization writes key/value records and semantic metadata, not seeds, raw buckets, lock words, or an accidental iteration order unless a versioned physical snapshot protocol owns compatibility.

**Concurrency makes path relocation a transaction.** A reader can check bucket A while a writer moves the target to bucket B and miss it in both unless locks, versions, duplicate publication, or validation prevent the race. Two insertions can plan paths through the same buckets. Resize changes candidate arrays while operations run. Delete can reclaim a payload still observed by a reader.

Sharded/bucket locks need an acquisition order, deadlock strategy, path revalidation, and resize coordination. Optimistic readers need version snapshots and retry. Multiwriter designs may lock candidate/path buckets, restart when versions change, and use safe payload lifetime. Progress, fairness, memory ordering, ABA, cancellation, iterator snapshots, and reclamation require algorithm-specific evidence; “two lookups” is not a concurrency proof.

**Security and operational limits remain.** Adversarial keys can collapse candidate pairs, create overfull components, exhaust kick/search budgets, fill the stash, and force repeated expensive rehashes. A secret seed reduces predictability but does not make weak candidate derivation independent or prevent resource attacks after leakage/adaptation.

Use keyed/randomized hashing where appropriate, per-request item/time/capacity/rehash limits, bounded stash and retries, graph/path/stash telemetry, backoff, and alternate structures. Preserve old data on failure. Record candidate-pair collisions, component/path exploration, path length, moves, kick limit hits, stash occupancy, rehash reasons/attempts, seed changes without exposing seeds, load, memory, and latency tails.

**Testing combines a reference map and graph oracle.** Generate insert/update/get/delete/reserve/rehash operations; compare logical contents. Check every live key is in exactly one candidate or stash, every occupied cell holds a key that names it, counts match, duplicates are absent, and all operations terminate. Build the cuckoo graph for small cases and independently test component edge/vertex excess and matching/orientation feasibility.

Force identical candidate pairs, parallel edges, trees, one-cycle and two-cycle components, disconnected empties, both candidates occupied with short/long path, bounded-search false failure, true infeasibility, deletion opening a path, stash fill/drain, repeated seed failures, maximum capacity, constant/structured hashes, duplicate updates, and injected construction/move/hash/equality/allocation failures. For concurrent claims, use history/linearizability tests, race tools, stalled writers, resize/delete races, and reclamation stress.

Benchmark realistic and adversarial candidate distributions across load, bucket width, candidate count, hit/miss/update/delete mix, insertion path/kick tails, stash and rehash events, payload size/layout, fingerprints, cache/NUMA, locks/retries, memory, throughput, and p50/p95/p99/max latency. Report candidate buckets, equality calls, path nodes, moves, rehash work, bytes moved/hashed, stash scans, failures, toolchains, hardware, seeds, repetitions, and uncertainty.

The executable oracle below uses explicit candidate pairs and transactional BFS. It verifies a two-write augmenting path, fixed-candidate lookup, direct deletion, safe reuse, a genuinely infeasible parallel-edge insertion, and graph placement invariants. It is not a randomized or concurrent performance result.

<!-- bijux-verify: {"id":"cuckoo-augmenting-path-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"table0=D,B,E,E,E\ntable1=A,F,E,E,E\naugmenting_path_writes=2\nlookup_A=ALPHA\ndeleted_C=CHARLIE\nfailed_key=G\nsize=4\ninvariant=True\nevidence=finite_cuckoo_augmenting_path_trace\n","stderr":""}} -->
```python
from collections import deque

EMPTY = object()


class CuckooMap:
    def __init__(self, side_capacity):
        self.tables = [[EMPTY] * side_capacity for _ in range(2)]
        self.size = 0

    def candidates(self, key):
        _, left, right = key
        return ((0, left), (1, right))

    def slot(self, bucket):
        table, index = bucket
        return self.tables[table][index]

    def set_slot(self, bucket, value):
        table, index = bucket
        self.tables[table][index] = value

    def other(self, key, bucket):
        first, second = self.candidates(key)
        assert bucket == first or bucket == second
        return second if bucket == first else first

    def locate(self, key):
        for bucket in self.candidates(key):
            resident = self.slot(bucket)
            if resident is not EMPTY and resident[0][0] == key[0]:
                return bucket
        return None

    def put(self, key, value):
        existing = self.locate(key)
        if existing is not None:
            self.set_slot(existing, (key, value))
            return False, 0

        roots = self.candidates(key)
        queue = deque(roots)
        parent = {roots[0]: None, roots[1]: None}
        endpoint = None
        while queue:
            bucket = queue.popleft()
            resident = self.slot(bucket)
            if resident is EMPTY:
                endpoint = bucket
                break
            alternate = self.other(resident[0], bucket)
            if alternate not in parent:
                parent[alternate] = bucket
                queue.append(alternate)

        if endpoint is None:
            return False, 0

        path = []
        bucket = endpoint
        while bucket is not None:
            path.append(bucket)
            bucket = parent[bucket]
        path.reverse()
        for index in range(len(path) - 1, 0, -1):
            self.set_slot(path[index], self.slot(path[index - 1]))
        self.set_slot(path[0], (key, value))
        self.size += 1
        return True, len(path)

    def get(self, key):
        bucket = self.locate(key)
        if bucket is None:
            raise KeyError(key)
        return self.slot(bucket)[1]

    def delete(self, key):
        bucket = self.locate(key)
        if bucket is None:
            raise KeyError(key)
        value = self.slot(bucket)[1]
        self.set_slot(bucket, EMPTY)
        self.size -= 1
        return value

    def invariant(self):
        live = []
        for table_index, table in enumerate(self.tables):
            for slot_index, resident in enumerate(table):
                if resident is EMPTY:
                    continue
                key, _ = resident
                if (table_index, slot_index) not in self.candidates(key):
                    return False
                live.append(key[0])
        return len(live) == self.size and len(set(live)) == self.size


table = CuckooMap(5)
a = ("A", 0, 0)
b = ("B", 1, 1)
c = ("C", 0, 1)
d = ("D", 0, 1)
f = ("F", 0, 1)
g = ("G", 0, 1)

assert table.put(a, "ALPHA")[0]
assert table.put(b, "BRAVO")[0]
assert table.put(c, "CHARLIE")[0]
inserted, path_writes = table.put(d, "DELTA")
assert inserted and path_writes == 2
lookup_a = table.get(a)
deleted_c = table.delete(c)
assert table.put(f, "FOXTROT")[0]
failed, _ = table.put(g, "GOLF")
assert not failed and table.locate(g) is None

for table_index, slots in enumerate(table.tables):
    labels = ["E" if slot is EMPTY else slot[0][0] for slot in slots]
    print(f"table{table_index}=" + ",".join(labels))
print(f"augmenting_path_writes={path_writes}")
print(f"lookup_A={lookup_a}")
print(f"deleted_C={deleted_c}")
print("failed_key=G")
print(f"size={table.size}")
print(f"invariant={table.invariant()}")
print("evidence=finite_cuckoo_augmenting_path_trace")
```

## Definitions and Notation

- `m`: cells per side in the classic two-table scheme; total main capacity is `2m`.
- `n`: live keys in main table plus any governed stash.
- `h0,h1`: candidate functions; candidate vertices are `(0,h0(k))` and `(1,h1(k))`.
- **cuckoo graph** `G=(V,E)`: bucket vertices and key edges.
- **orientation/placement**: assignment of each edge to a candidate endpoint within bucket capacity.
- **component excess**: edge count minus vertex capacity/count under the exact variant.
- **augmenting path**: alternating candidate/resident path ending in available capacity.
- **kick budget**: maximum evictions before fallback; an operational latency bound, not necessarily a feasibility proof.
- **stash**: bounded auxiliary collection searched by lookup and included in logical size.
- `d`: candidate buckets per key; `b`: slots per bucket in generalized schemes.

## Mechanisms, Invariants, or Proof Structure

Lookup correctness enumerates the complete candidate set and stash, filters, and confirms equality. Deletion removes exactly one located copy. Classic placement correctness maps keys to graph edges and occupied cells to an indegree-at-most-one orientation; per-component `e<=v` characterizes pseudoforest feasibility.

Transactional insertion discovers a bucket path before mutation. Each path edge is justified by the resident's alternate candidate; reverse moves begin at EMPTY and preserve exact legal placement. New publication adds one key. No-path from complete exploration and budget exhaustion are distinguished.

Rehash correctness treats old table, stash, and pending key as one logical set, computes new candidates, places each exactly once, and publishes after success. Probabilistic claims name load denominator, bucket/candidate variant, hash family, adversary, stash, and retry rules.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Blind/random kick chain | little planning memory | cycles, long tails, rollback/carried key |
| BFS augmenting path | shorter/transactional path possible | queue/visited memory and validation |
| Two single-slot tables | two candidate checks, simple graph | near-half total-slot regime |
| Bucketized cuckoo | higher utilization/fewer failures | multi-slot scans and new threshold theory |
| More than two choices | more placement flexibility | more hashes/reads and hypergraph proof |
| Bounded stash | reduces rehash probability | extra lookup, capacity, attack surface |
| Node/dense indirection | cheap moves/stable payload options | pointers, allocation, index repair |
| Linear/grouped probing | no global kick path | clustering/tombstones/probe tails |

## Failure Modes and Misconceptions

- **“Two candidates mean independent choices.”** derivation and hash family determine dependence.
- **“Any empty slot can accept the key.”** only a reachable candidate/augmenting endpoint matters.
- **“Low global load prevents failure.”** one graph component can be overfull.
- **“Kick limit means impossible.”** it may only mean the chosen search did not find a longer path.
- **“More kicks eventually succeed.”** an excess component has no valid orientation.
- **“The evicted key is temporary garbage.”** it remains live logical state and must be retained.
- **“Deletion needs a tombstone.”** classic candidate lookup does not rely on probe-chain history.
- **“Lookup always costs exactly two.”** buckets, stash, equality, synchronization, and retries add work.
- **“Fifty-percent load is universal.”** denominator and variant change the threshold.
- **“A stash is unbounded chaining.”** it must be small, searched, drained, and governed.
- **“Rehash means resize.”** new seeds can retain capacity; resize changes both graph vertices and reductions.
- **“Atomic bucket words solve concurrency.”** path movement, validation, resize, and reclamation remain.

## Worked Examples

### Example 1

One key with candidates `T0[2],T1[4]` is one edge. Storing it in either endpoint is a valid orientation. Conclusion: physical position must remain a legal candidate.

### Example 2

A tree component with four vertices and three keys has an empty root; orient each edge away from that root to occupy the other three vertices. Conclusion: a tree component is placeable with one free cell.

### Example 3

A three-vertex triangle-like multigraph component with three edges is unicyclic and can occupy all vertices. Adding a fourth internal edge gives `e=4>v=3`. Conclusion: the added key is structurally infeasible under current candidates.

### Example 4

Ten EMPTY cells lie in disconnected components while three parallel keys share two candidate vertices. Conclusion: global emptiness cannot repair local excess.

### Example 5

D sees occupied candidates `T0[0]` and `T1[1]`; A at `T0[0]` can move to empty `T1[0]`. Reverse commit moves A then installs D. Conclusion: path planning separates proof from mutation.

### Example 6

A capped BFS explores 32 buckets and stops, while an EMPTY exists at depth 33. Conclusion: budget exhaustion requires fallback but does not prove infeasibility.

### Example 7

A random kick loop reaches its limit while carrying key Z. Dropping Z loses data; placing it in a bounded stash or rebuilding the complete set preserves semantics. Conclusion: the carried key remains owned.

### Example 8

Two arrays of 100 cells store 90 keys: total-slot load is 0.45, while `n/m=0.9`. Conclusion: every load claim must state its denominator.

### Example 9

With two candidate buckets of eight slots, lookup can compare up to sixteen metadata entries plus stash, not two cells. Conclusion: bucketized cuckoo changes both utilization and read work.

### Example 10

An insert p99 spike comes from three failed reseeds and full rebuilds even though median lookup stays two bucket reads. Conclusion: insertion failure policy belongs in latency and capacity planning.

## Cross-Program Connections

- **Algorithms:** matchings, graph orientation, pseudoforests, augmenting paths, random graphs, and probability bounds explain placement.
- **Programming languages:** ownership, no-throw movement, rollback, generics, references, and destruction govern path commit.
- **Computer architecture:** independent bucket reads can overlap, while kick chains, cache lines, NUMA, and payload size determine movement cost.
- **Software engineering:** failure taxonomy, bounded retries, observability, seed governance, and model testing are part of the data structure.
- **Database engineering:** read-heavy hash indexes and joins need skew, build failure, spill, resize, and tail-latency plans.
- **Concurrent programming:** path relocation is a multi-bucket transaction with locks/versions, retries, resize, and reclamation.
- **Security engineering:** chosen candidate pairs can force component excess, stash growth, and rehash denial of service.

## References

1. Rasmus Pagh and Flemming Friche Rodler, [Cuckoo Hashing](https://www.rasmuspagh.net/papers/cuckoo.pdf). Primary classic construction and analysis under stated hash/load/rehash assumptions.
2. Adam Kirsch, Michael Mitzenmacher, and Udi Wieder, [More Robust Hashing: Cuckoo Hashing with a Stash](https://www.eecs.harvard.edu/~michaelm/postscripts/esa2008full.pdf). Primary graph/stash analysis and bounded insertion context.
3. Martin Aumüller, Martin Dietzfelbinger, and Philipp Woelfel, [Explicit and Efficient Hash Families Suffice for Cuckoo Hashing with a Stash](https://arxiv.org/abs/1204.4431). Primary explicit-family, graph-excess, stash, and insertion analysis.
4. William Kuszmaul, [Generalized Cuckoo Hashing with a Stash, Revisited](https://arxiv.org/abs/2010.01890). Primary correction/counterexample and generalized failure-probability analysis.
5. Efficient Computing at Carnegie Mellon, [`libcuckoo`](https://github.com/efficient/libcuckoo). Current concurrent bucketized cuckoo-map documentation, tests, and benchmark entry points.
6. Efficient Computing at Carnegie Mellon, [`cuckoohash_map.hh`](https://github.com/efficient/libcuckoo/blob/master/libcuckoo/cuckoohash_map.hh). Current primary source for buckets, partial keys, locking, lookup/update/delete, reserve, and rehash behavior.
7. DPDK Project, [`rte_cuckoo_hash.h`](https://doc.dpdk.org/api/rte__cuckoo__hash_8h_source.html). Current primary source for eight-slot buckets and concurrency/RCU-related representation options.
8. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Observable hash/equality, average/worst complexity, rehash, invalidation, and exception requirements without a mandated placement algorithm.
9. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/legacy/event/sec03/tech/full_papers/crosby/crosby.pdf). Primary collision-driven resource-attack evidence.
10. Rasmus Pagh, [Cuckoo Hashing for Undergraduates](https://www.rasmuspagh.net/papers/cuckoo-undergrad.pdf). Authorial derivation of candidate placement and graph reasoning for independent review of the core mechanism.

## Exercises

### Exercise 1

Specify classic two-table map get/update/delete semantics, candidate derivation, equality filtering, duplicate prevention, size, payload lifetime, and bounded behavior. Explain why deletion does not need linear-probing tombstones.

### Exercise 2

Prove the pseudoforest placement criterion for connected classic cuckoo-graph components. Construct a tree, unicyclic component, and excess-one failure using explicit candidate pairs.

### Exercise 3

Write transactional BFS augmenting-path insertion pseudocode. Distinguish complete no-path, bounded-search exhaustion, allocation/callback/move failure, and concurrent validation failure, and assign a safe fallback to each.

### Exercise 4

Design rehash/resize/reseed/stash policy for untrusted keys and a maximum-capacity environment. Include checked arithmetic, retry bounds, rollback, stash drain, serialization, invalidation, and telemetry.

### Exercise 5

Design tests and benchmarks comparing classic, bucketized, stash, concurrent, linear/grouped probing, and chaining designs. Prevent denominator, probability-model, and “two reads” claims from becoming misleading.

## Answers to the Exercises

### Answer 1

Require positive side capacity, two deterministic in-range candidates with documented derivation, stable compatible hash/equality, and at most one equivalent key. Get checks both candidate cells and bounded stash, filters by stored hash/fingerprint, confirms equality, and returns absent only after all legal locations. Update changes only the located value. Insert first runs the same duplicate search, then performs a failure-safe placement. Delete destroys/clears exactly the located cell or stash entry and decrements size once. Since lookup directly enumerates every legal location rather than stopping along a historical probe chain, clearing a cell cannot hide another key and no tombstone is required. All operations retain explicit bounds; failures preserve the documented prior/recoverable logical set.

### Answer 2

Orient each key edge toward its storage vertex, whose indegree is at most one. Summing indegrees shows any connected component with `e>v` is impossible. If a connected component is a tree (`e=v-1`), choose an empty root and orient each edge away from it so every other vertex receives one edge. If it is unicyclic (`e=v`), orient the cycle cyclically and orient attached tree edges away from the cycle; every vertex receives at most one. Thus `e<=v` components are placeable. Example tree: edges `(a,b),(b,c)`; unicyclic multigraph: two parallel edges `(a,b)`; failure: three parallel edges between `a,b`, with `e=3>v=2`.

### Answer 3

Check duplicates first. Initialize BFS with the new key's candidate buckets and parent markers. On an occupied bucket, follow its resident key to every alternate candidate; mark visited. On EMPTY, reconstruct the bucket path. Prepare ownership and commit from EMPTY backward, moving each complete resident only to its legal alternate, then publish the new entry at the root and increment size. Complete exploration with no EMPTY proves no augmenting path for that state and triggers stash/new seeds/grow. Budget exhaustion may hide a longer path and triggers the same controlled fallback without an impossibility claim. Allocation/hash/equality failure before commit changes nothing; move failure needs no-throw indirection or rollback/basic recovery. Concurrent version change discards the plan and retries within a bound.

### Answer 4

Track total and per-bucket load, candidate-pair collisions, path exploration/length, moves, stash occupancy, rehash reasons/attempts, failures, memory, and latency. Use keyed/domain-separated hashes appropriate to the threat model, but cap input, time, capacity, path, stash, and rehash attempts. On placement failure, use a small bounded stash if allowed; otherwise build a new table with new seeds and, when warranted, checked larger legal capacity. Include old main/stash plus pending key exactly once; publish only after success, retaining old state on failure. Retry stash after deletions/rehash. Maximum capacity returns a typed failure. State reference/iterator invalidation and synchronization. Serialize logical entries/config version, never secret seeds or raw buckets.

### Answer 5

Model-test logical operations and independently validate candidate legality, uniqueness, size, graph excess/matching, stash, termination, destruction, and rollback. Force parallel pairs, disconnected empties, tree/unicyclic/excess components, short/long paths, false budget failure, true infeasibility, stash fill/drain, seed retries, maximum capacity, poor hashes, callback/move failure, and concurrency histories where claimed. Benchmark identical semantics/budgets over key distributions, total-slot and paper-specific load metrics, bucket widths/choices, hit/miss/update/delete mixes, build/churn, path/kick/stash/rehash tails, payload layouts, cache/NUMA, locks/retries, memory, throughput, and p50/p95/p99/max latency. Report actual buckets/slots/equalities, moves, retries, bytes, hardware/toolchains, seeds, repetitions, uncertainty, and raw artifacts; attach every probability claim to its exact theorem model.
