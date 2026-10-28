---
module_id: DSE-083
program: Data Structures Engineering
level: 2
module_number: 83
title: Cuckoo and Quotient Filters
status: complete
last_verified: 2026-08-30
---

# Cuckoo and Quotient Filters

## One-Page Review

### Governing question

How can compact fingerprint tables provide approximate membership, deletion, locality, and merge/resize capabilities while preserving placement, metadata, ownership, and bounded-failure invariants at high load?

### Essential definitions

- A **fingerprint** is an f-bit hash-derived representative of a key. Two different keys can share it, causing false positives and deletion ambiguity.
- A **cuckoo filter** stores fingerprints in small buckets. A key has two candidate buckets; insertion may evict a fingerprint and relocate it to its alternate bucket.
- With power-of-two bucket count and `i2=i1 XOR H(fp)`, **alternate-bucket involution** means applying the same transformation to i2 returns i1.
- **Bucket size** b and **load factor** alpha=stored fingerprints/(buckets*b) shape space, false positives, relocation length, and insertion-failure probability.
- A **stash** temporarily/exactly holds placements that the main table could not accommodate; it must participate in queries, persistence, capacity, and rebuild.
- A **quotient filter (QF)** stores a p-bit fingerprint split into q-bit quotient and r-bit remainder (`p=q+r`). The quotient is the canonical bucket; the remainder is stored compactly.
- A **run** contains sorted remainders sharing a quotient; a **cluster** is one or more adjacent runs shifted by open-address collisions.
- QF metadata commonly marks whether a canonical bucket is occupied and whether a stored remainder is a continuation and/or shifted from its canonical slot.
- A **soft collision** shares quotient but not necessarily full fingerprint; a **hard fingerprint collision** shares the complete p/f bits and is indistinguishable inside the filter.

### Central model, mechanism, or theorem

Both structures store fingerprints rather than keys, so their no-false-negative contract is conditional on successful insertion, intact metadata, compatible hashing, and valid lifecycle operations. A maybe is not exact ownership. To delete safely, use an authoritative key/multiplicity record or handle; otherwise deleting one indistinguishable fingerprint can remove the only representation of another key.

For a cuckoo filter, let i be one candidate and `delta(fp)=H(fp) mod 2^a`; define alternate `i XOR delta`. XOR is self-inverse:

`(i XOR delta) XOR delta = i`.

This permits relocation using only the fingerprint, since an evicted entry need not retain its original key. Delta must obey the concrete scheme's nondegeneracy and compatibility rules. Insertion is probabilistic/bounded: reaching a kick limit is a normal capacity outcome requiring rollback, stash, resize, or rebuild—not silent loss.

For a quotient filter, a p-bit fingerprint z decomposes uniquely as `q=z >> r` and `rem=z & (2^r-1)`; reconstruction is `(q << r)|rem`. Compact storage shifts remainders away from canonical slots, so metadata and run/cluster ordering must make the quotient recoverable. A corrupted occupied/continuation/shifted bit can alter parsing and membership for a whole cluster.

### Critical invariants

1. Key encoding, full fingerprint width, bucket/quotient/remainder bits, seeds, and version are identical across insert/query/delete/recovery.
2. Every successfully inserted fingerprint is in one of its legal cuckoo buckets or declared stash, or in the uniquely decodable QF run for its quotient.
3. Cuckoo relocation preserves every evicted fingerprint, is bounded, and rolls back atomically on failure.
4. QF remainders in each run remain sorted as required; clusters/runs and occupied/continuation/shifted metadata decode uniquely after shifts.
5. Delete is authorized by exact ownership/multiplicity and removes exactly one representation; maybe alone cannot authorize it.
6. Load thresholds leave headroom for insertion/rebuild and are enforced before latency/failure cliffs.
7. Resizing/merging preserves enough fingerprint bits and policy identity, publishes atomically, and keeps old generations for pinned readers.

### Common failures

- Reporting successful insert before a relocation chain commits, then losing the final evicted fingerprint.
- Mutating the live table during kicks and failing without rollback.
- Choosing alternate bucket from the original key so an evicted fingerprint cannot be relocated independently.
- Deleting an absent key whose fingerprint collides with a live member.
- Treating insertion failure near high load as an impossible exception.
- Shifting QF remainders without updating all affected metadata, splitting/merging runs incorrectly.
- Resizing from remainders alone without reconstructing the old quotient/full fingerprint.
- Comparing nominal bits/item while omitting empty-slot headroom, metadata, stash, allocator, and failed-build cost.

### Compact example

An eight-bucket cuckoo table with two slots/bucket and 4-bit fingerprints inserts 15 fixture values (load 15/16=0.9375) with four relocations. XOR alternate mapping is involutive, every inserted key queries maybe, an owned deletion succeeds, an unowned deletion is rejected, and remaining keys stay positive. The same values produce 15 separate 8-bit fingerprints for a quotient model: 4 quotient bits and 4 remainder bits form 10 quotient runs and five soft collisions; recombination exactly reconstructs the fingerprint multiset.

### Connections

DSE-081–082 supply Bloom probability, ownership, deletion, and growth; DSE-084–085 cover frequency/cardinality sketches; DSE-086 onward covers spatial/vector structures. Hashing and randomized algorithms explain placement; Database/Storage Engineering use filters in tables and LSMs; Concurrent Programming supplies relocation/publication/reclamation correctness.

## Governing Question

How do we engineer fingerprint-based approximate membership so that space/locality gains survive insertion failure, collision-aware deletion, metadata shifts, concurrency, persistence, and adversarial load?

## Why This Matters

Bloom filters scatter several bit probes and ordinary variants cannot delete. Cuckoo filters concentrate lookup into two small buckets and can delete stored fingerprints. Quotient filters arrange remainders in contiguous runs, supporting locality, deletion, iteration over fingerprints, merge, and resize. These capabilities are valuable for in-memory caches, SSD-resident indexes, LSM metadata, deduplication, routing, and bioinformatics.

They pay for capability with structural state. A cuckoo insertion can displace a chain and fail at high load. A quotient filter uses compact metadata whose meaning depends on neighboring slots. Both store only fingerprints, so exact key identity is deliberately lost. A correct algorithm must state what happens on collision, overload, crash, concurrent mutation, and rebuild.

Performance claims are also conditional. Cuckoo filters can offer good locality and space at particular false-positive rates/load factors; quotient filters can exploit sequential access and mergeability. But fingerprints, bucket slack, metadata bits, stash, alignment, SIMD lanes, and rebuild headroom determine real space. Load-factor distributions and implementation details determine tails. “Better than Bloom” is a measured/model-specific comparison, not a universal theorem.

## Prerequisites and Retrieval

Retrieve:

- hash tables, cuckoo hashing, open addressing, linear/Robin-Hood probing, load factor, connected components, and randomized insertion;
- fingerprints, collision probability, approximate membership, union bounds, adversarial queries, and exact ownership;
- bit packing, quotient/remainder decomposition, circular arrays, runs/clusters, stable sorting, and metadata state machines;
- transactional rollback, linearization, versioned publication, WAL/checkpoints, crash recovery, and epoch reclamation;
- property/state-machine tests, invariant checking, fuzzing, workload distributions, tail latency, and capacity planning.

Diagnostic retrieval: a false positive and a hard fingerprint collision look identical inside either filter. Only exact external state can decide whether a requested deletion owns a stored representation.

## Learning Objectives

After this module, you can:

1. derive cuckoo candidate buckets and prove alternate-bucket involution;
2. implement bounded relocation with rollback/stash/resize outcomes and validate successful placement;
3. explain fingerprint-width, bucket-size, load-factor, and false-positive trade-offs with scoped formulas;
4. authorize deletion safely under fingerprint collisions and multiplicity;
5. decompose/reconstruct QF fingerprints and explain run/cluster metadata invariants;
6. design QF insert/delete/shift/merge/resize with atomic publication and corruption checks;
7. compare cuckoo, quotient, counting Bloom, and ordinary Bloom filters by capability and measured system cost;
8. verify sequential/concurrent/fault histories plus statistical insertion/query evidence.

## Core Exposition

**Start from the fingerprint contract.** Hash canonical key bytes into a sufficiently wide value, then retain f or p bits according to format. Query asks whether that fingerprint representation exists in legal structure positions. Different keys can be indistinguishable. The filter may enumerate fingerprints, but not original keys. Positive authorization, uniqueness, exact deletion, and value retrieval remain external responsibilities.

**Build cuckoo candidates compatibly.** One common scheme computes first bucket from the key hash and second as `i1 XOR hash(fp)`. Because bucket count is a power of two, mask indices and persist the exact hash/seed/fingerprint rules. The alternate transform must be derivable from the stored fp alone. Avoid a zero delta if the design promises two distinct buckets; analyze fingerprint-dependent weak cycles and biased indices.

**Query two bounded buckets.** Compute fp,i1,i2 and scan b slots in each, often vectorized. A matching fp returns maybe. Absent returns only if neither legal bucket nor stash contains fp. Approximate false-positive intuition often uses roughly `2b/2^f` at low collision probability/high occupancy, but slot dependence, duplicate fingerprints, occupancy, semi-sorting, and hash scheme require the paper/implementation's exact model and empirical validation.

**Insert with a transaction.** If either bucket has space, insert. Otherwise choose a victim, replace it with current fp, compute the victim's alternate bucket, and repeat. Bound kicks and detect cycles/time. Because every intermediate victim represents a member, failure must restore the original table or retain the last victim in a durable stash before reporting success. Copy-on-write trial state is simple but expensive; production uses logged/locked paths or rebuild.

**Model the two structures narrowly.** The program uses a copy-on-write cuckoo relocation trial and exact ownership, then independently demonstrates quotient/remainder reconstruction.

<!-- bijux-verify: {"id":"cuckoo-and-quotient-filter-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cuckoo_buckets=8\nbucket_slots=2\ninserted=15\nload_factor=0.9375\nrelocations=4\nalternate_involution=True\nall_inserted_positive=True\nowned_delete=True\nunowned_delete_rejected=True\nremaining_positive=True\nquotient_bits=4\nremainder_bits=4\nquotient_runs=10\nsoft_collisions=5\nfingerprints_reconstructed=True\nvalid=True\nevidence=cuckoo_and_quotient_filter_model\n","stderr":""}} -->
```python
mask = (1 << 64) - 1
bucket_count = 8
bucket_slots = 2
buckets = [[] for _ in range(bucket_count)]
ownership = {}
relocations = 0


def mix64(value):
    value = (value + 0x9E3779B97F4A7C15) & mask
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & mask
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & mask
    return value ^ (value >> 31)


def fingerprint(value):
    return (mix64(value) & 15) or 1


def alternate(index, stored_fingerprint):
    delta = (mix64(stored_fingerprint) & (bucket_count - 1)) or 1
    return index ^ delta


def candidates(value):
    first = (mix64(value + 0xD1B54A32D192ED03) >> 4) & (bucket_count - 1)
    return first, alternate(first, fingerprint(value))


def insert(value):
    global buckets, relocations
    stored_fingerprint = fingerprint(value)
    first, second = candidates(value)
    for index in (first, second):
        if len(buckets[index]) < bucket_slots:
            buckets[index].append(stored_fingerprint)
            ownership[value] = ownership.get(value, 0) + 1
            return True
    trial = [bucket[:] for bucket in buckets]
    current = stored_fingerprint
    index = first
    kicks = 0
    for step in range(16):
        slot = (current + step) % bucket_slots
        trial[index][slot], current = current, trial[index][slot]
        kicks += 1
        index = alternate(index, current)
        if len(trial[index]) < bucket_slots:
            trial[index].append(current)
            buckets = trial
            relocations += kicks
            ownership[value] = ownership.get(value, 0) + 1
            return True
    return False


def maybe(value):
    stored_fingerprint = fingerprint(value)
    first, second = candidates(value)
    return stored_fingerprint in buckets[first] or stored_fingerprint in buckets[second]


def remove(value):
    if ownership.get(value, 0) == 0:
        return False
    stored_fingerprint = fingerprint(value)
    for index in candidates(value):
        if stored_fingerprint in buckets[index]:
            removed = False
            retained = []
            for existing in buckets[index]:
                if existing == stored_fingerprint and not removed:
                    removed = True
                else:
                    retained.append(existing)
            buckets[index] = retained
            ownership[value] -= 1
            return True
    raise AssertionError("placement invariant")


values = tuple(range(3, 60, 4))
inserted = all(insert(value) for value in values)
involution = all(alternate(alternate(index, fingerprint(value)), fingerprint(value)) == index
                 for value in values for index in candidates(value))
all_positive = all(maybe(value) for value in values)
owned_delete = remove(27)
unowned_rejected = not remove(99)
remaining_positive = all(maybe(value) for value in values if value != 27)

full_fingerprints = sorted(mix64(value) & 255 for value in values)
quotient_remainders = sorted((value >> 4, value & 15) for value in full_fingerprints)
quotient_runs = len({quotient for quotient, remainder in quotient_remainders})
reconstructed = sorted((quotient << 4) | remainder
                       for quotient, remainder in quotient_remainders) == full_fingerprints
valid = (inserted and involution and all_positive and owned_delete and unowned_rejected
         and remaining_positive and reconstructed)
print(f"cuckoo_buckets={bucket_count}")
print(f"bucket_slots={bucket_slots}")
print(f"inserted={len(values)}")
print(f"load_factor={len(values) / (bucket_count * bucket_slots):.4f}")
print(f"relocations={relocations}")
print(f"alternate_involution={involution}")
print(f"all_inserted_positive={all_positive}")
print(f"owned_delete={owned_delete}")
print(f"unowned_delete_rejected={unowned_rejected}")
print(f"remaining_positive={remaining_positive}")
print("quotient_bits=4")
print("remainder_bits=4")
print(f"quotient_runs={quotient_runs}")
print(f"soft_collisions={len(quotient_remainders) - quotient_runs}")
print(f"fingerprints_reconstructed={reconstructed}")
print(f"valid={valid}")
print("evidence=cuckoo_and_quotient_filter_model")
```

The mixer and victim choices are deterministic educational fixtures. Copying the whole table gives rollback but is not a production transaction. Exact Python ownership—not the cuckoo filter—authorizes deletion. No insertion failure, stash, duplicate ownership, concurrency, serialization, corruption, or false-positive sample is exercised. The quotient half stores sorted `(quotient,remainder)` pairs, not a shifted array or metadata bits, so it proves decomposition only, not a QF implementation.

**Treat insertion failure as part of the API.** At higher alpha, displacement components and kick tails grow. Return a distinct failure before losing state; expose attempts/kicks/stash/load. Resize or rebuild at a conservative threshold derived from bucket size, fingerprint scheme, concurrency, workload, and target failure probability. A full filter remains query-correct for existing members but cannot accept promised growth.

**Design the stash completely.** A stash can absorb rare failures and reduce rebuilds, but every query and delete must check it, every checkpoint must persist it, and capacity must be bounded. An unbounded stash degenerates into another table. Losing a stash on crash creates false negatives for inserts previously acknowledged as successful.

**Delete with exact ownership.** If two keys share fp and candidate buckets, the filter cannot tell their copies apart. For a set API, an exact directory or generation-scoped handle establishes that x was inserted. Remove one matching occurrence and update exact multiplicity atomically. Deleting a maybe-only absent key can remove a colliding member. Duplicate fingerprints require multiplicity or duplicate-insert policy.

**Understand quotienting.** Hash x to p bits. The q high bits choose canonical slot among `2^q`; the r low bits are stored. If canonical slots could hold unbounded remainders, quotient need not be stored. Open addressing shifts entries; metadata lets a decoder map shifted sorted remainders back to their quotient. Increasing r lowers fingerprint-collision probability but expands each slot; increasing q expands slot count and changes load/headroom.

**Maintain runs and clusters.** All remainders for one quotient form a sorted run. Adjacent runs displaced by occupied canonical buckets form a cluster. Lookup checks the occupied bit at canonical quotient; if occupied, it finds cluster start by walking backward through shifted entries, then advances runs using continuation/occupied structure and compares sorted remainders. Bound probes and treat malformed metadata as corruption, not absence.

**Insert a QF entry coherently.** Determine q/r. If quotient unoccupied, mark it occupied. Find its run or insertion point, shift later slots right to an empty slot, adjust shifted/continuation flags, and place remainder in order. Wraparound complicates circular indexing. Mutation touching a cluster is multi-slot; concurrent readers cannot observe half-shifted metadata. Use locks/versioned blocks/copy-on-write and crash logging.

**Delete and compact a run.** Authorize exact occurrence, locate matching remainder in the quotient's run, remove one, shift subsequent cluster entries left as allowed, and update run/occupied/continuation/shifted metadata. If a hard fingerprint collision has multiple copies, exact multiplicity decides whether one remains. Deleting by filter maybe alone is unsafe. Test deleting first/middle/last/only remainder and cluster wraparound.

**Resize QFs from reconstructable fingerprints.** Because q and remainder reconstruct p-bit fingerprint, a larger table can use more high bits as quotient and fewer/remaining bits appropriately if total stored fingerprint information and policy allow. Reinsert reconstructed fingerprints into a new layout. You cannot increase p and recover discarded bits without original keys; a resize that needs lower p-related error requires authoritative rebuild.

**Merge compatible QFs.** Ordered fingerprint iteration enables streaming merge of compatible filters, preserving multiplicities under declared set/multiset semantics. Compatibility includes full p, hash/seed/domain, encoding, and ownership policy. The merged load may exceed target, and hard collisions remain indistinguishable. Build a new filter, validate, then atomically publish rather than mutating two live structures in place.

**Compare false positives honestly.** A cuckoo maybe arises when query fp matches any fingerprint in its candidate buckets/stash. A QF maybe arises when p-bit fingerprint occurs in its quotient run. Approximate rates depend on f/p, alpha, bucket size, duplicates, hash distribution, and query distribution. Quote formulas with premises, then measure across seeds/load/adversarial keys. Successful insertion and lookup error are separate probabilities.

**Engineer concurrency by ownership boundary.** Cuckoo queries touch two buckets but insert relocation spans many; locking buckets without deadlock or exposing transient loss is subtle. QF operations shift clusters. Options include coarse locks, ordered lock acquisition with restart, version counters/seqlocks for readers, immutable shards, or copy-on-write generations. Verify linearizability and bounded retry under contention; per-slot atomics alone do not establish structural consistency.

**Persist formats defensively.** Store magic/version, algorithm family, fingerprint/hash policy, seeds/key IDs, bucket/q/r/slot metadata, load/count, stash, checksums, and generation. Validate all arithmetic, lengths, indices, metadata state combinations, and counts before queries. Unknown/corrupt optional filters fall back to authoritative state or explicit error. Never parse malformed cluster metadata into a negative result.

**Plan adversarial behavior.** Public filters permit searching/replaying false positives; chosen keys may stress particular buckets/runs or relocation. Keyed hashing can make targeting harder but requires secret rotation and rebuild. Bound insert work, stash, cluster length, memory, and query work; rate-limit abusive clients; isolate tenants; retain authoritative verification. Approximate membership is never authorization.

**Measure lifecycle cost.** Record bits per successfully stored member including slack/metadata/stash; load; insertion successes/failures/kicks/retries; bucket/cluster probe distributions; false-positive rates; deletes; rebuild/resize/merge bytes and peaks; CPU/cache/memory; concurrency stalls; recovery; and downstream work saved. Benchmark from empty through target load and churn, not only a favorable fixed alpha.

## Definitions and Notation

For cuckoo filters, N buckets, b slots/bucket, f fingerprint bits, n stored occurrences, `alpha=n/(Nb)`, candidates `i1(x)` and `i2=i1 XOR delta(fp)`, and kick limit L. Placement invariant maps every stored fp to one of its legal pair/stash.

For quotient filters, p-bit fingerprint z, q quotient bits, r=p-q remainder bits, `quot(z)=floor(z/2^r)`, `rem(z)=z mod 2^r`, and `z=quot*2^r+rem`. Run/cluster metadata encodes canonical ownership after displacement. A hard collision has equal z; soft collision has equal quotient only.

## Mechanisms, Invariants, or Proof Structure

### Cuckoo placement proof

1. Fix canonical hash/fingerprint policy and derive two legal buckets with an involutive alternate function.
2. Start from a table where every fp occupies a legal bucket/stash.
3. During a kick, place current fp in a legal bucket and carry the evicted fp without loss.
4. Compute evicted fp's other legal bucket using fp alone; repeat within bound.
5. On empty slot/stash, commit complete path atomically; on failure restore exact pre-state or rebuild.
6. Query both buckets/stash; deletion additionally requires exact ownership and removes one representation.

### Quotient decoding proof

1. Split every p-bit fingerprint uniquely into q-bit quotient and r-bit remainder.
2. Maintain sorted remainders per quotient and contiguous runs within uniquely delimited clusters.
3. Maintain occupied to identify nonempty canonical quotients, continuation to delimit runs, and shifted to locate cluster starts/canonical displacement.
4. Decode a query's run from canonical quotient and metadata, then compare its remainder.
5. Insert/delete shifts update every affected remainder/flag atomically and preserve sorted/run/cluster structure.
6. Recombining decoded quotient/remainder yields exactly the stored fingerprint multiset.

### Evidence proof

1. Compare committed histories with an exact multiset and verify every live key remains maybe after each operation.
2. Enumerate stored fingerprints and validate legal cuckoo placement or QF decode/reconstruction.
3. Exercise load thresholds, kick/cluster tails, failure rollback, stash, wraparound, duplicates, and hard/soft collisions.
4. Linearizability-test concurrent query/insert/delete/resize/merge and fault every persistence/publication boundary.
5. Measure insertion failure and false positives across seeds, loads, distributions, churn, and adversarial search.
6. Validate format compatibility/corruption, rebuild/rollback, resource bounds, and authoritative bypass.

## Alternatives and Trade-Offs

| Structure | Strength | Main risk/cost | Evidence focus |
|---|---|---|---|
| Cuckoo filter | two-bucket locality, deletion, compact low-p regimes | relocation/failure tails, slack/stash, concurrency | success probability, kicks, load, fp collisions |
| Quotient filter | locality, fingerprint iteration, merge/resize | metadata/cluster shifts and corruption blast radius | decode invariants, cluster tails, atomic shifts |
| Counting Bloom | simple dynamic projection | multiple counter probes, width/overflow, exact ownership | counter tails, atomic multi-counter updates |
| Ordinary Bloom | simple monotone construction and analysis | no deletion, scattered probes, fixed capacity | p, hash/cache cost, rebuild |
| Exact fingerprint/key table | exact or wider collision contract | more bits, resize/table metadata | exactness, memory, tails |

Semi-sorting cuckoo fingerprints, blocked layouts, counting quotient filters, vector quotient filters, and Morton/xor/ribbon filters move the frontier again. Each changes formulas, load failure, supported updates, construction, metadata, and hardware behavior. Select from required operations and measured workload, not family reputation.

## Failure Modes and Misconceptions

**“Cuckoo insertion always succeeds below capacity.”** Placement can fail before physical fullness; probability/tails depend on graph/load/algorithm.

**“A kick overwrites one slot, so it is atomic.”** The evicted fingerprint remains unplaced until the chain commits or stash/rollback captures it.

**“The alternate bucket can hash the original key.”** Relocation retains only fp; alternate must be derivable from fp and current bucket.

**“Delete any matching fingerprint.”** Only with exact ownership/multiplicity. False positives and hard collisions make maybe insufficient.

**“QF stores only remainders, so quotient is lost.”** Canonical location plus run/cluster metadata reconstructs quotient—if invariants are intact.

**“Three metadata bits are independent flags.”** Their combinations encode structural relationships; arbitrary mutation can make the cluster undecodable.

**“QF resize can improve fingerprint precision.”** It can repartition stored p bits, not recover discarded hash bits without keys.

**“Merge means bitwise OR.”** QFs merge ordered fingerprint streams under compatibility and capacity rules; cuckoo layouts require reinsertion/rebuild.

**“High load is always best space efficiency.”** Near the cliff, kick/cluster tails, failures, stash, concurrency, and rebuild headroom can dominate.

**“A successful query benchmark proves update fitness.”** Churn, failure rollback, deletion, resize, merge, and recovery are separate workloads.

**“Fingerprint filters secure membership.”** They are approximate performance structures, not authorization or integrity proofs.

**“Malformed metadata can be treated as empty.”** That converts corruption into false negatives; fail or use authoritative fallback.

## Worked Examples

### Example 1

With N=8, `delta(fp)=5`, and first bucket 3, second is `3 XOR 5=6`; from bucket 6, alternate is `6 XOR 5=3`. This involution lets an evicted fp move without its original key. If delta=0, both candidates collapse to one bucket.

### Example 2

A table with 1024 buckets and four slots stores 3686 fingerprints: `alpha=3686/4096≈0.8999`. Bits per stored member must include `1024*4*f/3686` plus metadata/stash/alignment, not just f. Reserving load headroom is real space.

### Example 3

A relocation path evicts A→B→C and reaches its kick limit with C unplaced. Reporting failure after mutating live buckets loses C; reporting success lies about the new key. Roll back A/B/C moves, place C in a durable stash, or build/commit a resized table.

### Example 4

Keys x and y share 8-bit fp and candidates. After both insert, two copies may exist. Exact multiplicity says two. Deleting x removes one and y stays maybe; a second unowned delete of x could remove y's copy, so exact state must reject it.

### Example 5

For p=12 and q=7, r=5. Fingerprint `0b101101001011` has quotient its top seven bits and remainder bottom five; reconstruction shifts quotient five and ORs remainder. A resize may repartition the same 12 bits but cannot create a 16-bit fingerprint.

### Example 6

Fingerprints `(q=4,r=2),(4,7),(4,11)` form one sorted run. If canonical slot 4 is occupied by a previous cluster, all may be shifted. Occupied marks quotient 4 exists; continuation distinguishes later run elements; shifted helps locate cluster start. Deleting r=2 must make r=7 the run start.

### Example 7

Two QFs with identical p/hash policy expose sorted fingerprint streams `[5,20,20,90]` and `[7,20,80]`. Multiset merge yields `[5,7,20,20,20,80,90]`; set merge would deduplicate by policy. The destination must have capacity and represent chosen multiplicities.

### Example 8

At load 70%, p99 cluster length may be modest; at 95%, a particular workload can exhibit long clusters and insert shifts. Average O(1) language does not protect service tails. Measure cluster-length and bytes-moved distributions at supported load/churn.

### Example 9

A reader scans QF metadata while a writer shifts four slots. Without a version/lock, it can combine old continuation with new remainder and return absent for a live key. A block seqlock can make the reader retry if version changes; copy-on-write can publish a coherent replacement.

### Example 10

An attacker searches public fingerprints for keys targeting one bucket pair, raising relocation failures or false-positive downstream work. Keyed/domain-separated hashing, quotas, kick/work bounds, stash caps, monitoring, and rebuild reduce risk; approximate maybe never grants access.

## Cross-Program Connections

- **Algorithms and Probability:** cuckoo graphs, random walks, open addressing, quotienting, occupancy, and tail bounds explain success and failure.
- **Database Engineering:** filters, exact catalogs, WAL, MVCC generations, corruption policy, and LSM rebuilds provide authoritative lifecycle.
- **Data Engineering:** mergeable fingerprints, SSD locality, deduplication, partitions, and large immutable runs motivate quotient-based designs.
- **Concurrent Programming:** multi-bucket relocation, cluster shifting, seqlocks, ordered locks, copy-on-write, and epochs define linearizable implementations.
- **Security Engineering:** chosen keys, fingerprint replay, tenant isolation, keyed hashing, and bounded work address denial-of-service risk.
- **Performance Engineering:** load curves, p99 kicks/clusters, cache/SIMD behavior, rebuild peaks, and end-to-end savings determine production fit.

## References

1. Bin Fan, David G. Andersen, Michael Kaminsky, and Michael D. Mitzenmacher, [Cuckoo Filter: Practically Better Than Bloom](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf), *CoNEXT*, 2014.
2. David Eppstein, [Cuckoo Filter: Simplification and Analysis](https://arxiv.org/abs/1604.06067), 2016.
3. Michael A. Bender et al., [Don't Thrash: How to Cache Your Hash on Flash](https://vldb.org/pvldb/vol5/p1627_michaelabender_vldb2012.pdf), *PVLDB* 5(12), 2012.
4. Prashant Pandey, Michael A. Bender, Rob Johnson, and Rob Patro, [A General-Purpose Counting Filter: Making Every Bit Count](https://prashantpandey.github.io/projects/2_filter/), *SIGMOD*, 2017; author project and publication record.
5. Prashant Pandey et al., [Vector Quotient Filters: Overcoming the Time/Space Trade-Off in Filter Design](https://users.cs.utah.edu/~pandey/courses/cs6968/spring23/papers/vqf.pdf), *SIGMOD*, 2021.
6. Michael A. Bender et al., [Adaptive Quotient Filters](https://arxiv.org/abs/2405.10253), 2024.

## Exercises

### Exercise 1

For a power-of-two cuckoo table, prove alternate-bucket involution. Then explain why zero delta, non-power-of-two reduction, incompatible hash versions, and deriving i2 from the original key can each break a concrete relocation design.

### Exercise 2

Design a failure-atomic cuckoo insertion with bucket locks, bounded kicks, and stash/resize. State linearization, rollback/logging, deadlock/retry, crash recovery, reader behavior, and metrics.

### Exercise 3

A QF uses p=16,q=10. Decompose fingerprint `0xB6D3`, reconstruct it, and explain how its run is found when its canonical slot lies inside a shifted cluster. State corruption checks.

### Exercise 4

Compare a cuckoo filter, quotient filter, counting Bloom filter, and ordinary Bloom filter for a high-churn in-memory cache, an SSD-resident merge-heavy index, and an immutable SSTable. State assumptions and evidence that could reverse each choice.

### Exercise 5

Design a verification matrix covering exact-oracle histories, placement/decode invariants, hard/soft collisions, failure/load tails, deletion ownership, concurrency, persistence/corruption, resize/merge, statistical false positives, adversarial behavior, and rollback.

## Answers to the Exercises

### Answer 1

Let `alt(i,f)=i XOR d(f)`. Then `alt(alt(i,f),f)=(i XOR d) XOR d=i` by XOR cancellation. `d=0` collapses choices and hurts capacity. Masking modulo a power of two keeps XOR indices in range; arbitrary modulo after XOR can destroy involution. A version/seed change computes another d and strands stored fp. If i2 requires the original key, an evicted fp alone cannot discover its other bucket, so the relocation state must store more information or use the fingerprint-derived scheme.

### Answer 2

Compute fp/candidates and acquire a deterministic lock protocol or construct a private relocation plan with version validation. Carry every evicted fp and old slot value; bound kicks. Linearize when the complete path/stash entry commits under validated locks/version. On limit, restore the logged before-images or leave live state untouched, then atomically add to bounded durable stash or trigger resize; never acknowledge until one succeeds. Avoid deadlock with ordered acquisition/restart and bound starvation. WAL path/stash/manifest or copy-on-write generation so recovery selects pre/post state. Readers use locks, versions/retry, or immutable generation. Record load, attempts, kicks, cycles, retries, stash, failures, resize time/peak, and latency tails.

### Answer 3

`r=p-q=6`. For `z=0xB6D3=46803`, quotient is `z>>6=731` (`0x2DB`) and remainder is `z & 0x3F=19` (`0x13`); `(731<<6)|19=46803`. Check occupied at canonical slot 731. Walk backward across shifted slots to cluster start, then advance run boundaries using occupied/continuation semantics until quotient 731's run, and compare sorted remainder 19. Validate q/r/p, array length, occupancy/count bounds, allowed flag combinations, circular-walk limits, run/cluster ordering, checksum, and reconstruction; malformed metadata yields corruption/fallback, not absence.

### Answer 4

Start with cuckoo for high-churn RAM when two-bucket locality, deletion, bounded load, and relocation concurrency meet tails; CBF may win with simpler updates or cuckoo failures may reverse it. Start with QF/buffered variants for SSD merge-heavy work because locality and ordered fingerprint iteration/merge fit; cluster tails or complex crash shifts may favor immutable Bloom layers. Start with ordinary Bloom for immutable SSTable simplicity, compact monotone build, and no deletion need; a QF may win if merge/resize/locality and measured space/query are better. Compare full bits including slack/metadata, false positives, build/insert failure, CPU/cache/I/O, churn, p99, rebuild, faults, concurrency, and authoritative integration.

### Answer 5

Generate insert/delete/duplicate/failure/resize histories against an exact multiset and assert all successfully inserted live keys remain maybe. Enumerate cuckoo fp legal buckets/stash and decode every QF cluster/run to reconstruct its sorted fingerprint multiset. Force hard/soft collisions, zero/weak deltas, wraparound, first/middle/last run deletes, kick limits, full buckets, long clusters, stash exhaustion, and load sweeps. Linearizability-test bucket relocations and QF shifts with queries/deletes/rebuilds. Kill/mutate every log, slot, metadata, stash, manifest, and publication boundary; require pre/post recovery or explicit corruption. Verify compatible/incompatible merge/resize, old reader pins, ownership handles, and rollback. Across seeds/workloads/adversarial searches report insertion failures, false positives with intervals, kicks/clusters, resource/tail metrics, and downstream savings.
