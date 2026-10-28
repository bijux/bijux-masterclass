---
module_id: DSE-082
program: Data Structures Engineering
level: 2
module_number: 82
title: Counting and Scalable Bloom Filters
status: complete
last_verified: 2026-08-30
---

# Counting and Scalable Bloom Filters

## One-Page Review

### Governing question

How can approximate-membership filters support deletion and unbounded growth without converting counter collisions, overflow, ownership mistakes, or error-budget composition into false negatives or unbounded query cost?

### Essential definitions

- A **counting Bloom filter (CBF)** replaces each ordinary bit with a nonnegative counter. Insert increments every derived position; a query is maybe iff all are positive; a valid delete decrements the same positions.
- **Ownership** is authoritative knowledge that an element occurrence represented by this filter exists and may be deleted. A probabilistic maybe is not ownership.
- **Multiplicity** counts live insertion occurrences under the API contract. Counter values are aggregate hash loads, not exact per-key multiplicities.
- **Overflow** occurs when an increment exceeds counter capacity; **underflow** when a decrement would cross zero. Wrapping either is unsafe.
- A **transactional counter update** preflights or rolls back all k positions so an operation is not partially applied.
- A **scalable Bloom filter (SBF)** appends new fixed-capacity subfilters as cardinality grows. Insert targets an active layer; membership is the OR of layer queries.
- An **error budget** assigns per-layer false-positive targets `p_i` so aggregate error stays under a declared bound.
- For layer false-positive events `F_i`, the union bound is `Pr(any F_i)<=sum p_i`; under additional independence, `1-product(1-p_i)` estimates composition.
- A **stable/decaying filter** evicts evidence to bound an unending stream and intentionally permits forgetting; it does not retain ordinary no-false-negative semantics.

### Central model, mechanism, or theorem

A CBF retains the ordinary membership projection: replacing every positive counter with one yields its bit filter. Safe deletion has a stronger precondition than insertion. If an authoritative multiplicity ledger says x has a live represented occurrence, decrementing exactly the increments contributed by that occurrence preserves every remaining occurrence's positive counters. Deleting x merely because the CBF says maybe can decrement counters owned only by colliding members and create false negatives.

Counter overflow is not safely solved by ordinary saturation followed by later decrement: once increments are lost, a decrement can reach zero while unrecorded occurrences remain. Safe choices include reject-before-mutation, widen/rebuild, exact overflow side state, or a saturated sentinel that is never decremented until reconstructed. Underflow must reject or signal corruption, never clamp/wrap silently.

For a scalable sequence with `p_i=p_0*r^i`, `0<r<1`, the union-bound budget is `sum p_i=p_0/(1-r)`. To target aggregate at most P, choose `p_0<=P(1-r)`. Independence can yield a smaller estimate but is not needed for the bound. More layers increase query hashes/cache probes and metadata, so growth needs consolidation/aging policy as well as memory.

### Critical invariants

1. Insert/delete/query use identical canonical bytes, positions, layer identity, and policy; repeated positions follow one explicit increment convention.
2. Delete is authorized by exact ownership and multiplicity routing, never by filter maybe alone.
3. All counter increments/decrements are bounded and atomic as one logical operation; overflow/underflow cannot wrap or partially mutate.
4. If saturation loses count information, later deletion cannot use that counter normally until exact reconstruction.
5. Each scalable layer is immutable or safely synchronized after publication, with exact cardinality/capacity and pinned error budget.
6. A scalable query checks every layer that may own the element; layer retirement/rebuild is atomically published and reader-safe.
7. Aggregate false-positive claims use a stated union bound or justified dependence model and include number of layers/query distribution.

### Common failures

- Deleting an absent false-positive key and damaging real members that share its counters.
- Treating minimum counter value as an exact element multiplicity.
- Using saturating counters, then decrementing them as if no increments were lost.
- Letting an increment wrap to zero or a decrement wrap to maximum.
- Updating some positions before discovering overflow in another, leaving a partial insertion.
- Decrementing every maybe-positive scalable layer because the owning layer is unknown.
- Giving every new layer the same p, so aggregate false-positive probability grows with layer count.
- Creating layers forever without accounting for lookup fan-out, cache, metadata, or consolidation cost.

### Compact example

A 32-cell, three-probe CBF with maximum counter 3 accepts exactly three occurrences of key 3; a fourth is rejected before mutation. Removing the three owned occurrences returns the counters to zero. Keys 7, 11, and 19 are then inserted; deleting owned 11 preserves maybe for 7 and 19, while an unowned delete of 23 is rejected. Separately, six distinct members fill scalable layers of capacity 2 and 4 with error budgets 0.040 and 0.020. Their union bound is 0.060; an independence estimate is 0.0592.

### Connections

DSE-081 supplies ordinary Bloom derivation and one-sided semantics; DSE-083 compares cuckoo/quotient deletion-capable filters; DSE-084 separates frequency estimation from membership counters. Database and Data Engineering use dynamic cache directories, streaming duplicate suppression, partitions, joins, and retention; Concurrent Programming supplies atomic multi-location update/publication reasoning.

## Governing Question

How do we add lifecycle operations to Bloom membership while preserving an auditable relationship between authoritative set state, approximate counters/layers, and one-sided error guarantees?

## Why This Matters

Ordinary Bloom filters fit immutable sets with known approximate cardinality. Many systems are neither immutable nor bounded: cache entries expire, routes change, distributed membership moves, streaming keys grow, and file catalogs rotate. Rebuilding after every change is too costly. Counting filters permit deletion; scalable filters permit growth.

Those extensions introduce new correctness state. A bit only records whether at least one insertion touched it. A counter records the number of hash contributions to a cell, but collisions erase which keys contributed. A sequence of subfilters records membership across layers, but a query does not reveal authoritative ownership. Operations that infer ownership from these summaries can destroy evidence.

Operationally, counter width and layer count become capacity limits. Overflow can be rare in a random model yet catastrophic when it wraps. An infinite geometric false-positive budget can be bounded while real query CPU grows with every layer. The design must specify both mathematical composition and lifecycle protocols: ownership, atomic updates, rebuild, publication, concurrency, persistence, and observability.

## Prerequisites and Retrieval

Retrieve:

- ordinary Bloom filters, false-positive approximation, no-false-negative proof, hash derivation, serialization, and overload;
- multisets, reference counts, invariants, checked arithmetic, transactions, linearization, snapshots, and copy-on-write publication;
- geometric series, union bound, event independence, probability budgets, and workload-weighted cost;
- cache expiry, streaming windows, distributed ownership, repair, duplicate delivery, idempotency, and epochs;
- property/state-machine testing, concurrency histories, fault injection, golden formats, and capacity alarms.

Diagnostic retrieval: a CBF maybe means all aggregate counters are positive. It does not prove that x contributed any of them. Therefore it cannot authorize deletion.

## Learning Objectives

After this module, you can:

1. define CBF insert/query/delete semantics with exact ownership and multiplicity preconditions;
2. prove safe deletion for owned occurrences and construct false-negative counterexamples for unowned deletion;
3. design overflow, underflow, repeated-position, partial-update, persistence, and concurrency policies;
4. derive scalable geometric error budgets and distinguish union bounds from independence estimates;
5. route insertion/deletion/query across layers and publish rebuild/consolidation safely;
6. distinguish counting membership from frequency estimation and stable/decaying membership;
7. test dynamic filters against an exact multiset/model across sequential, concurrent, corrupt, and adversarial histories;
8. measure memory, false positives, update/query CPU, layer fan-out, rebuild, and downstream savings.

## Core Exposition

**Define the counted object.** Choose set or multiset API. In a set API, duplicate insert may be rejected/idempotent through an authoritative exact directory; CBF alone cannot reliably detect duplicates because maybe can be false. In a multiset API, every accepted occurrence increments and only a matching owned removal decrements. Persist an exact multiplicity/ownership source or issue deletion tokens carrying filter generation/layer and operation identity.

**Preserve the projection invariant.** Let `c[j]` be a counter and projected bit `b[j]=1` iff `c[j]>0`. For every live occurrence, each of its hash-position contributions is included in corresponding counters. Query reads the projection. If every deletion removes exactly one previously accepted occurrence and arithmetic is exact, remaining occurrences keep at least their own contribution at every position.

**Treat repeated positions explicitly.** Hash derivation may produce the same cell twice for one element. One convention increments once per probe occurrence; deletion must decrement with identical multiplicity. Another deduplicates positions and increments once per distinct cell; every operation and format must use the same rule. The finite model uses three formulas that are distinct for exercised keys, but production cannot assume that property without enforcement.

**Authorize deletion externally.** Suppose absent z happens to be maybe because three cells are positive from a,b,c. Decrementing z removes contributions that z never made. If one cell falls to zero, a real member using it becomes false negative. Check exact ownership first. In distributed systems also prove epoch/shard/generation ownership so a delayed duplicate delete is rejected idempotently.

**Reject overflow transactionally.** Precompute the complete position multiset and required increment per cell. Check every counter has headroom; only then apply all increments. Under locks or compare-and-swap, the check and updates must linearize against competitors. If failure occurs mid-persistence, recovery must see pre- or post-operation, not partial counters. Rebuild/widen before capacity exhaustion.

**Do not decrement lost saturation.** Saturating 3 at max while accepting more occurrences loses their count. After one removal, changing 3→2 undercounts; eventually zero can appear with live occurrences. A permanent overflow sentinel can remain positive and refuse decrements until rebuild, preserving membership but accumulating false positives. Exact side overflow counters can retain information. Silent saturate-and-decrement is invalid.

**Model deletion and growth together.** The executable model preflights a bounded CBF and uses an exact occurrence ledger. Its independent scalable sequence appends fixed layers and evaluates the error-budget formulas.

<!-- bijux-verify: {"id":"counting-and-scalable-filter-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"counter_cells=32\ncounter_max=3\naccepted_duplicate_inserts=3\noverflow_insert_rejected=True\noverflow_transactional=True\nowned_delete_safe=True\nunowned_delete_rejected=True\nremaining_members_positive=True\nscalable_layers=2\nlayer_capacities=2,4\nlayer_error_budgets=0.040,0.020\nunion_bound=0.060\nindependent_composition=0.0592\nscalable_members_positive=True\nvalid=True\nevidence=counting_and_scalable_filter_model\n","stderr":""}} -->
```python
cell_count = 32
maximum = 3
counters = [0] * cell_count
ownership = {}


def positions(value):
    return ((value * 5 + 1) % cell_count, (value * 11 + 3) % cell_count, (value * 17 + 5) % cell_count)


def insert(value):
    selected = positions(value)
    if any(counters[position] >= maximum for position in selected):
        return False
    for position in selected:
        counters[position] += 1
    ownership[value] = ownership.get(value, 0) + 1
    return True


def remove(value):
    if ownership.get(value, 0) == 0:
        return False
    selected = positions(value)
    if any(counters[position] <= 0 for position in selected):
        raise AssertionError("counter invariant")
    for position in selected:
        counters[position] -= 1
    ownership[value] -= 1
    return True


def maybe(value):
    return all(counters[position] > 0 for position in positions(value))


accepted = sum(insert(3) for _ in range(3))
before_rejection = tuple(counters)
overflow_rejected = not insert(3)
overflow_transactional = before_rejection == tuple(counters)
for _ in range(3):
    remove(3)
for value in (7, 11, 19):
    insert(value)
owned_delete_safe = remove(11) and not maybe(11)
unowned_delete_rejected = not remove(23)
remaining_positive = all(maybe(value) for value in (7, 19))

layers = []


def layer_positions(value, bits, probes):
    return tuple((value * 5 + 1 + probe * (value * 6 + 1)) % bits for probe in range(probes))


def new_layer(index):
    capacity = 2 * (2 ** index)
    return {"capacity": capacity, "budget": 0.04 * (0.5 ** index), "bits": capacity * 8,
            "probes": 3, "array": 0, "count": 0}


def scalable_insert(value):
    if not layers or layers[-1]["count"] >= layers[-1]["capacity"]:
        layers.append(new_layer(len(layers)))
    layer = layers[-1]
    for position in layer_positions(value, layer["bits"], layer["probes"]):
        layer["array"] |= 1 << position
    layer["count"] += 1


def scalable_maybe(value):
    return any(all(layer["array"] & (1 << position)
                   for position in layer_positions(value, layer["bits"], layer["probes"]))
               for layer in layers)


for value in range(10, 16):
    scalable_insert(value)
scalable_positive = all(scalable_maybe(value) for value in range(10, 16))
budgets = [layer["budget"] for layer in layers]
union_bound = sum(budgets)
independent = 1
for budget in budgets:
    independent *= 1 - budget
independent = 1 - independent
valid = (accepted == 3 and overflow_rejected and overflow_transactional and owned_delete_safe
         and unowned_delete_rejected and remaining_positive and scalable_positive)
print(f"counter_cells={cell_count}")
print(f"counter_max={maximum}")
print(f"accepted_duplicate_inserts={accepted}")
print(f"overflow_insert_rejected={overflow_rejected}")
print(f"overflow_transactional={overflow_transactional}")
print(f"owned_delete_safe={owned_delete_safe}")
print(f"unowned_delete_rejected={unowned_delete_rejected}")
print(f"remaining_members_positive={remaining_positive}")
print(f"scalable_layers={len(layers)}")
print("layer_capacities=" + ",".join(str(layer["capacity"]) for layer in layers))
print("layer_error_budgets=" + ",".join(f"{budget:.3f}" for budget in budgets))
print(f"union_bound={union_bound:.3f}")
print(f"independent_composition={independent:.4f}")
print(f"scalable_members_positive={scalable_positive}")
print(f"valid={valid}")
print("evidence=counting_and_scalable_filter_model")
```

The CBF model uses tiny counters, three simple arithmetic positions, and exact Python ownership. It exercises no repeated positions, concurrent updates, persistence, saturation, corruption, or probabilistic false positives; `not maybe(11)` is fixture-specific, not promised by deletion. The scalable layers use crude bit sizing and declared budgets not derived from their finite layouts. Independence is only arithmetic over declared p values. The run proves bounded transition behavior for these inputs, not target error rates or production safety.

**Handle underflow as a defect signal.** With verified ownership and invariant-preserving history, selected counters must be positive before delete. Zero reveals wrong layer/generation, duplicate delete, lost insertion, corruption, repeated-position mismatch, or race. Reject the complete operation and surface evidence. Clamping a zero hides the defect and may leave other positions decremented.

**Choose counter representation from risk.** Fixed c-bit counters use c times ordinary bitmap memory before packing overhead; load distribution, n, k, m, skew, adversaries, and concurrency determine overflow risk. “Four bits is enough” is a workload/model claim, not a universal rule. Variable/overflow encodings reduce common-case memory but add indirection and crash/concurrency complexity. Monitor maximum and high-percentile counters plus rejected operations.

**Separate membership from frequency.** `min_j c[h_j(x)]` can upper-bound a contribution count under some conventions, but collisions overestimate and repeated positions complicate it. A CBF designed for deletion is not automatically a statistically analyzed frequency sketch. Count-Min Sketch in DSE-084 gives an explicit additive-error model; exact per-key multiplicity still needs authoritative state.

**Build scalable layers monotonically.** Give layer i a capacity `n_i`, size `m_i`, probe policy `k_i`, and budget `p_i`. Insert distinct new keys into the newest nonfull layer. Once full, freeze it and append another with larger capacity and usually tighter p. Query all live layers until any says maybe. Exact deduplication before insertion requires authoritative state; using maybe to suppress an insert can create a false negative if the maybe was false.

**Compose error conservatively.** For absent x, scalable maybe occurs if any layer false-positives. The union bound needs no independence: at most `sum p_i`. If layer events are independent, exact composition is `1-product(1-p_i)`, but shared input encodings/hash derivation and query distributions can correlate them. Domain-separate seeds and measure realized joint behavior; promise the conservative budget unless stronger premises are proved.

**Allocate an infinite budget.** With target P and tightening ratio r, choose `p_i=P(1-r)r^i`; the infinite sum is P. For P=0.06,r=0.5, budgets begin 0.03,0.015,0.0075—not the finite model's illustrative 0.04/0.02. Layer capacities can grow geometrically by factor s>1. Tighter later p requires more bits/item, while growing capacity amortizes metadata. Round and recompute every layer.

**Bound layer fan-out.** Even a bounded false-positive sum does not bound hashes, cache misses, or metadata because a negative query checks every layer. Track layer count and expected/percentile query work. Consolidate frozen layers into a new filter built from authoritative members, shard by epoch/range, or cap lifecycle duration. Publish replacement atomically; retain old layers for pinned readers until safe reclamation.

**Route deletion to ownership.** A scalable CBF may store layer ID/generation in an exact handle returned at insertion. Deleting via that handle decrements only the owning layer and validates epoch/multiplicity. Searching for maybe-positive layers and decrementing one or all is unsafe: false positives and duplicates make routing ambiguous. A rebuild from current authoritative set can remove dead elements without dynamic counters.

**Specify concurrency linearization.** CBF operations touch multiple counters plus ownership. A global/striped lock, transactional memory, versioned copy, or carefully designed multiword protocol must give a linearization point. Per-counter atomics alone prevent lost arithmetic but allow queries to observe partial inserts/deletes. Scalable append must publish fully initialized layer metadata and bits before readers see it. Retiring layers requires epoch/hazard/reference protection.

**Persist and recover coherently.** Counters without the exact ownership ledger—or vice versa—cannot safely accept deletes after crash. Rebuild from an authoritative WAL/set, checkpoint both at a common sequence, or log idempotent operations with generation and operation IDs. Validate checksums, widths, max values, position policy, layer capacities/counts, and budget metadata. Unknown/corrupt filters fall back to authoritative lookup or explicit error, not absence.

**Distinguish scalable from stable.** Scalable filters grow state to retain every inserted member under ordinary no-false-negative semantics. Stable Bloom filters bound state for infinite streams by probabilistically decrementing/aging cells, eventually forgetting older elements. They can support approximate recent duplicate detection, but false negatives are intentional relative to all-time membership. State time/window and error semantics explicitly.

**Use rebuild as normal maintenance.** Rebuild repairs high occupancy, overflow sentinels, deleted residue, excess layers, changed hashes, and cardinality misestimates. Take an authoritative snapshot at sequence e, build/validate new filter, capture/apply later mutations or quiesce, then atomically publish a new generation. Readers pin generation; deletes carry correct ownership; reclaim old state after references drain.

**Test state machines.** Generate sequences of insert, duplicate insert, owned delete, duplicate/unowned delete, overflow, rebuild, serialize/recover, and layer rollover. Compare against an exact multiset and assert every live member is maybe after each committed operation. Inject repeated positions, skew/collisions, maximum counters, partial failures, corrupt checkpoints, concurrent histories, delayed operations, and epoch reuse. For scalable filters, measure per-layer and aggregate false positives across seeds/query distributions.

## Definitions and Notation

Let C be a vector of m counters in `[0,M]`, `P(x)` the probe multiset or deduplicated position set under a declared convention, and `A(x)` authoritative live multiplicity. Projection `B[j]=1[C[j]>0]`. Safe deletion requires `A(x)>0` and removes exactly one accepted occurrence's contributions.

For scalable layers i, let capacity `n_i`, bits `m_i`, probes `k_i`, target/upper-bound `p_i`, and event `F_i(x)` for absent x. Aggregate event is union of F_i. `Pr(union F_i)<=sum p_i`; equality/product formulas require stronger dependence knowledge.

## Mechanisms, Invariants, or Proof Structure

### Owned-deletion proof

1. Exact state establishes `A(x)>0` in generation/layer g.
2. The accepted insertion contributed one unit at every occurrence in declared `P_g(x)` without overflow loss.
3. Preflight proves every required counter is positive and the whole decrement will commit atomically.
4. Decrement exactly those contributions and update A in the same logical transaction.
5. Every remaining occurrence retains its own contribution at all positions, so every live member remains maybe.
6. Reject absent, stale, duplicate, overflow-ambiguous, corrupt, or wrong-generation deletion before mutation.

### Scalable error-budget proof

1. Assign each layer a validated false-positive bound `p_i` for the declared absent-query/hash model.
2. A scalable false positive implies at least one `F_i` because query is OR across layers.
3. Apply union bound to obtain aggregate at most `sum p_i` without independence.
4. Choose a summable sequence such as `p_i=P(1-r)r^i`, whose infinite geometric sum is P.
5. Account separately for query fan-out, false-negative-free publication, and empirical joint behavior.
6. Recompute after rounding/layout changes and reject claims when per-layer premises are unverified.

### Lifecycle evidence proof

1. Pin exact multiset/ownership oracle, operation IDs, generations, policies, widths, capacities, and budgets.
2. Model-check/generated-test committed sequential histories against live-member positivity and rejected-operation nonmutation.
3. Linearizability-test concurrent histories and fault every persistence/publication boundary.
4. Measure overflow/underflow headroom, layers, occupancy, per-layer/aggregate p, CPU/cache/memory, and tails.
5. Rebuild from an authoritative snapshot plus delta and compare logical queries before/after publication.
6. Exercise rolling compatibility, rollback, delayed deletes, corruption, and safe authoritative bypass.

## Alternatives and Trade-Offs

| Design | Capability | Primary cost/risk | Best-fit evidence |
|---|---|---|---|
| Fixed-width CBF | deletion with external ownership | c-times bit memory, overflow and multi-counter atomicity | dynamic-set histories, width/load/adversary bounds |
| Overflow side table/sentinel | compact common counters | indirection, rebuild and crash complexity | overflow frequency, exact recovery, tails |
| Scalable Bloom sequence | unknown/growing cardinality | layer query fan-out and metadata | budget composition, growth, consolidation |
| Rebuilt ordinary Bloom | simple immutable reads, deletes absorbed at rebuild | authoritative enumeration and rebuild lag/cost | snapshot/delta publication and stale-state tolerance |
| Cuckoo/quotient filter | deletion/locality/enumeration options | load/relocation/metadata failure modes | insertion failure, p, concurrency, resize |
| Stable/decaying filter | bounded memory for unending recent-history stream | intentional forgetting/false negatives | time-recency semantics and stream error study |

Counting and scalable mechanisms can be combined, but complexity multiplies: deletion routing across layers, per-layer counter width, overflow, and rebuild all coexist. Prefer the simplest lifecycle satisfying actual requirements. If authoritative members are already enumerable and changes are batched, immutable rebuilds may be safer and smaller.

## Failure Modes and Misconceptions

**“Maybe means the key can be deleted.”** False positives make this unsafe. Require exact ownership.

**“Counters store per-key counts.”** They store aggregate cell contributions. Collisions prevent exact attribution.

**“Saturation preserves safety.”** Only if the saturated state is never decremented normally or lost increments are tracked exactly.

**“Atomic increments make insert atomic.”** A reader can observe some of k counters before others. Define multi-location visibility.

**“Four-bit counters always suffice.”** Width adequacy depends on load, hash model, skew, adversaries, and required failure probability.

**“A scalable filter has target p because every layer does.”** Equal per-layer p accumulates. Allocate a summable budget.

**“Layer false positives are independent.”** Shared queries, encodings, hashes, and data distributions can correlate them. Union bound is safer.

**“Use maybe to deduplicate layer insertion.”** A false positive can suppress the only insertion and produce a future false negative.

**“Delete from every positive layer.”** Some positives are false and duplicates may have defined ownership. Route exactly.

**“Bounded aggregate p means bounded query cost.”** Negative queries still inspect every relevant layer.

**“Stable and scalable mean similar things.”** Scalable grows to retain history; stable evicts history to bound memory.

**“Rebuild is just a copy.”** It needs a consistent authoritative snapshot, mutation delta/quiescence, validation, atomic publication, and reader-safe reclamation.

## Worked Examples

### Example 1

Members a and b share cell 5. Counters for a's other cells are 1; absent z false-positives using cell 5 plus two cells owned by a. Deleting z decrements those counters and can zero a's evidence. The operation was invalid because `A(z)=0`, regardless of maybe.

### Example 2

A 2-bit counter at 3 accepts a fourth contribution by saturating at 3. Later one deletion changes it to 2 although three contributions remain; repeated deletes can reach zero early. Reject/widen/side-count, or keep a nondecrementable overflow sentinel until rebuild.

### Example 3

An element's probe multiset is `[4,4,9]`. Per-probe convention increments cell 4 twice and cell 9 once; delete must decrement 4 twice. Deduplicated convention increments each once. Mixing conventions across versions creates under/overcount and possible false negatives.

### Example 4

With target aggregate P=0.01 and r=0.5, geometric budgets are `p_i=0.005*(0.5)^i`: 0.005, 0.0025, 0.00125, and so on. Their infinite sum is 0.01. Three layers have union bound 0.00875, leaving budget for future layers.

### Example 5

For two layer bounds 0.04 and 0.02, union bound is 0.06. Under independence, composition is `1-(0.96)(0.98)=0.0592`. Claim 0.06 without independence; the smaller figure is a conditional model estimate.

### Example 6

Ten layers each meet p=1%. Union bound is 10%; independence estimate is `1-0.99^10≈9.562%`. Equal budgets therefore do not preserve a 1% aggregate target, and each negative lookup also pays ten layer probes.

### Example 7

A deletion handle `{generation:12,layer:3,key_digest:d,op:88}` arrives twice. Exact operation state commits the first and records op 88; the second is rejected without counter mutation. After rebuild generation 13, a delayed generation-12 handle is stale and cannot touch new counters.

### Example 8

Counter positions have values `[2,1,4]`; an owned delete needs one decrement each, but a crash after the first yields `[1,1,4]`. A query during or after partial recovery can be inconsistent. WAL the logical operation and redo/undo idempotently, or publish a copy-on-write version atomically.

### Example 9

A scalable filter's layer capacities double 1M,2M,4M and budgets halve. Seven million keys fill three layers. A negative query computes three filter checks. Consolidating into a validated 7M-key filter reduces fan-out but needs authoritative enumeration, peak build memory, delta capture, and atomic generation switch.

### Example 10

A stable filter decrements random counters before inserting each stream item. Under bounded space it reaches a stationary occupancy, but an old item can eventually lose one required positive counter and query negative. That is acceptable only for explicitly approximate recent-duplicate semantics, never all-time membership.

## Cross-Program Connections

- **Probability and Statistics:** balls-into-bins load, counter tails, union bounds, dependence, geometric budgets, and empirical intervals govern sizing.
- **Database Engineering:** exact catalogs/WAL/MVCC generations authorize deletion, recovery, rebuild, and reader-safe publication.
- **Data Engineering:** streaming duplicate detection, TTL windows, file/partition churn, and unbounded cardinality motivate scalable or decaying semantics.
- **Distributed Systems:** duplicate delivery, epochs, ownership transfer, repair, delayed deletes, and replicas require idempotent routed operations.
- **Concurrent Programming:** multiword atomicity, linearizability, memory ordering, snapshots, epochs, and reclamation protect live evidence.
- **Security Engineering:** chosen collisions and delete requests can target counters; authorization, keyed hashing, quotas, and rebuild limit abuse.
- **Performance Engineering:** counter packing, cache lines, layer fan-out, rebuild peaks, and downstream savings determine whether flexibility pays.

## References

1. Li Fan, Pei Cao, Jussara Almeida, and Andrei Z. Broder, [Summary Cache: A Scalable Wide-Area Web Cache Sharing Protocol](https://www.cs.princeton.edu/courses/archive/spr05/cos598E/bib/p254-fan.pdf), *IEEE/ACM Transactions on Networking* 8(3), 2000.
2. Paulo Sérgio Almeida, Carlos Baquero, Nuno Preguiça, and David Hutchison, [Scalable Bloom Filters](https://webarchive.di.uminho.pt/haslab.uminho.pt/cbm/publications/scalable-bloom-filters.html), *Information Processing Letters* 101, 2007.
3. Fan Deng and Davood Rafiei, [Approximately Detecting Duplicates for Streaming Data Using Stable Bloom Filters](https://webdocs.cs.ualberta.ca/~drafiei/papers/DupDet06Sigmod.pdf), *SIGMOD*, 2006.
4. Flavio Bonomi et al., [An Improved Construction for Counting Bloom Filters](https://theory.stanford.edu/~rinap/papers/esa2006b.pdf), *ESA*, 2006.
5. Domenico Ficara, Stefano Giordano, Gregorio Procissi, and Fabio Vitucci, [MultiLayer Compressed Counting Bloom Filters](https://people.unipi.it/gregorio_procissi/pubblicazioni/), *IEEE INFOCOM*, 2008; author publication record.
6. Alexander Broder and Michael Mitzenmacher, [Network Applications of Bloom Filters: A Survey](https://www.eecs.harvard.edu/~michaelm/postscripts/im2005b.pdf), *Internet Mathematics* 1(4), 2004.
7. Ana Rodrigues, Ariel Shtul, Carlos Baquero, and Paulo Sérgio Almeida, [Time-limited Bloom Filter](https://arxiv.org/abs/2306.06742), 2023.

## Exercises

### Exercise 1

Give a minimal counterexample showing how deleting an absent false-positive element creates a false negative for a live member. Include positions, counters before/after, and the missing ownership check.

### Exercise 2

Design an overflow-safe multiset CBF operation for repeated positions under concurrent inserts/deletes. State counter width/max, position multiplicities, preflight, locking/linearization, ownership update, persistence, and recovery behavior.

### Exercise 3

A scalable filter targets aggregate P=0.02 with r=0.25 and capacities starting at 100,000 then doubling. Compute the first four p_i, their four-layer union bound, remaining infinite budget, and total four-layer capacity. State what independence would and would not change.

### Exercise 4

Compare scalable Bloom, rebuilt ordinary Bloom, counting Bloom, and stable Bloom for: an append-only unknown-size archive; a dynamic exact cache directory; and all-time duplicate detection on an infinite stream under fixed memory. Explain infeasibility where appropriate.

### Exercise 5

Design a verification matrix for a persistent scalable CBF with deletion handles and online consolidation. Include sequential state-machine oracle, concurrency, fault/recovery, compatibility/corruption, probability, capacity, performance, migration, and rollback evidence.

## Answers to the Exercises

### Answer 1

Let live a use positions `{1,2}` and live b use `{2,3}`, producing counters `[c1,c2,c3]=[1,2,1]`. Absent z hashes to `{1,3}` and therefore false-positives. If delete(z) decrements its positions, counters become `[0,2,0]`; a now queries cell 1 zero and b queries cell 3 zero, so both false-negative. Exact `A(z)=0` would reject before mutation. Maybe cannot establish contribution ownership.

### Answer 2

Canonicalize the position multiset into `(cell,required_delta)` pairs. Under a lock/transaction covering ownership plus all cells, verify `A(x)` for delete, verify every increment satisfies `c<=M-delta`, or every decrement `c>=delta`, then WAL one generation/op-ID-tagged logical operation. Apply all deltas and exact multiplicity update and commit at one linearization point. Reject without mutation on overflow/underflow/stale/duplicate operation; never wrap/silently saturate. Recovery idempotently redoes committed or discards/undoes uncommitted operations. Queries synchronize or read an immutable version so they never observe partial deltas.

### Answer 3

Set `p_i=P(1-r)r^i=0.015*(0.25)^i`. The first four are 0.015, 0.00375, 0.0009375, and 0.000234375. Their union-bound sum is 0.019921875; remaining infinite budget is `0.02-0.019921875=0.000078125`. Capacities are 100k,200k,400k,800k, totaling 1.5M. Independence would permit `1-product(1-p_i)` as a slightly smaller estimate, but it would not alter the unconditional union bound, prove concrete layer p, or reduce four layer checks.

### Answer 4

Use a scalable Bloom sequence for append-only unknown size, with geometric error budget and consolidation/fan-out controls. A rebuilt ordinary Bloom also works if authoritative enumeration and batch rebuild latency/peak are acceptable. For a dynamic exact cache directory, use a CBF only with exact ownership/multiplicity and safe overflow/concurrency, or periodically rebuilt ordinary filters if stale-inclusive semantics permit; scalable append-only layers alone cannot remove safely. All-time membership for an infinite distinct stream under fixed memory and fixed nontrivial error is infeasible in this family; a stable filter answers approximate recent membership by forgetting and must advertise false negatives, while scalable state grows without bound.

### Answer 5

Generate insert/duplicate/owned-delete/unowned-delete/overflow/underflow/rollover/rebuild histories against an exact generation-layer multiset and assert all live members positive plus rejected nonmutation after every commit. Linearizability-test races on shared/repeated counters, handles, append, consolidation, reader pins, and reclamation. Kill before/after WAL, counter, checkpoint, delta, and manifest sync; recover exact ownership/counters or rebuild. Mutate widths, maxima, policies, checksums, lengths, layers, budgets, and generations; require safe bypass/error. Across seeds/load/skew/adversarial keys measure per-layer/joint false positives with intervals, overflow tails, memory, cache/CPU, layer fan-out, update/query tails, rebuild peak/debt, and downstream savings. Test rolling formats, old handles, canary logical comparison, abort thresholds, and rollback without premature old-generation reclamation.
