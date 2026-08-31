---
module_id: DSE-084
program: Data Structures Engineering
level: 2
module_number: 84
title: Count-Min Sketch
status: complete
last_verified: 2026-08-30
---

# Count-Min Sketch

## One-Page Review

### Governing question

How can a system estimate per-key frequencies from a stream using fixed memory while making the approximation contract, stream assumptions, and merge protocol precise?

### Essential definitions

A **frequency vector** (f\in\mathbb{R}^U) maps each key in universe (U) to its accumulated weight. An **insertion-only** stream applies updates ((x,\Delta)) with (\Delta\ge 0). A Count-Min Sketch (CMS) contains (d) rows of (w) counters and one hash function (h_j:U\rightarrow\{0,\ldots,w-1\}) per row. Update ((x,\Delta)) adds (\Delta) to (C[j,h_j(x)]) in every row. The ordinary point estimate is

$$
\widehat f_x=\min_{0\le j<d} C[j,h_j(x)].
$$

For nonnegative updates, collision mass can only raise a counter, so (f_x\le\widehat f_x). With pairwise-independent hashes, (w=\lceil e/\varepsilon\rceil), and (d=\lceil\ln(1/\delta)\rceil), the standard argument gives

$$
\Pr[\widehat f_x>f_x+\varepsilon\lVert f\rVert_1]\le\delta
$$

for a fixed query (x). This is an additive, probabilistic, point-query guarantee—not relative error for every key and not a simultaneous guarantee over an unbounded adaptive query sequence.

### Central model, mechanism, or theorem

In row (j), the queried counter decomposes as (f_x+Z_j), where (Z_j) is collision mass from other keys. Pairwise independence gives $\mathbb{E}[Z_j]\le\lVert f\rVert_1/w$. At width (e/\varepsilon), Markov's inequality bounds (\Pr[Z_j>\varepsilon\lVert f\rVert_1]\le 1/e). If rows are independently chosen, all (d) rows are bad with probability at most (e^{-d}\le\delta). The minimum selects any good row.

The counter matrix is a linear summary under ordinary updates. Two sketches can be added cell by cell only when their dimensions, hash definitions, seeds, key encoding, counter representation, and update semantics agree. Conservative update often reduces overcount in practice, but it is not the same linear transform and therefore changes the merge story.

### Critical invariants

- Each accepted update reaches exactly one counter in every row, or no row becomes visible.
- Standard insertion-only counters never fall below a queried key's true frequency.
- Counter overflow, partial row updates, and hash-version drift invalidate the intended contract.
- A merged ordinary sketch equals a sketch of the concatenated streams only under identical configuration.
- CMS estimates candidates supplied by some key-discovery mechanism; the matrix alone does not enumerate the key universe.
- Probability parameters describe randomness in hash selection under stated assumptions, not certainty for each deployed seed.

### Common failures

Teams promise relative error for rare keys, use negative updates with the insertion-only theorem, merge incompatible seeds, silently saturate counters, confuse conservative update with a mergeable linear sketch, or call every large estimate a heavy hitter without retaining candidate keys. Other failures include adversarially chosen collisions, reset races, double-counted shard epochs, and a serialization format that omits the hash identity.

### Compact example

Let (\varepsilon=0.01) and (\delta=10^{-6}). Then (w=\lceil e/0.01\rceil=272) and (d=\lceil\ln 10^6\rceil=14), for 3,808 counters. If the stream mass is (10^8), the theorem's additive allowance is (10^6). A key with true count 50 may therefore have a formally valid yet operationally useless estimate. Memory sizing must start from the decision being supported, not from attractive-looking percentages.

### Connections

Retrieve hashing, collision semantics, and owned mutation from [DSE-082](082-counting-and-scalable-bloom-filters.md). The roadmap successor is [DSE-085, “HyperLogLog”](../ROADMAP.md), where the target changes from per-key frequency to distinct cardinality. Database aggregation, telemetry pipelines, and distributed processing reuse the same merge identity and epoch-accounting obligations.

## Governing Question

How do we design, prove, implement, merge, and operate a Count-Min Sketch so that its small fixed memory supports a trustworthy frequency decision rather than an ambiguous approximate number?

## Why This Matters

Exact frequency maps grow with the number of distinct keys. That is often unacceptable on a switch, telemetry collector, storage engine, or streaming worker whose memory budget must remain fixed while the key population changes. CMS replaces per-key state with a rectangular counter matrix. Every event is observed, but collisions deliberately combine keys.

The apparent simplicity hides a contract stack. The mathematical guarantee depends on a stream model and hash assumptions. The implementation must make a multi-row update coherent, choose counter widths, and preserve hash identity. A distributed deployment must prevent lost or duplicated shard intervals. A product must define whether it needs a point estimate, a heavy-hitter candidate set, a threshold decision, or a mergeable summary. Graduate-level competence means being able to trace a claim from decision semantics through proof premises to bytes, concurrency, persistence, and monitoring.

## Prerequisites and Retrieval

Before proceeding, retrieve:

- pairwise-independent hashing, expectation, Markov's inequality, and independent repetition;
- the (\ell_1) norm (\lVert f\rVert_1=\sum_x |f_x|);
- insertion-only, strict-turnstile, and general-turnstile stream models;
- integer overflow, atomic publication, serialization compatibility, and epoch identity;
- approximate membership from [DSE-081](081-bloom-filters.md) and mutable approximate filters from [DSE-082](082-counting-and-scalable-bloom-filters.md).

Do not conflate a counting Bloom filter with CMS. Both use hashed counters, but the former answers approximate membership for owned insertions and deletions, whereas CMS estimates vector coordinates under an additive-error contract. Nor should CMS be confused with Count Sketch: signed hashing and a median estimator support a different noise analysis, particularly when signed updates matter.

## Learning Objectives

After this chapter, you should be able to:

1. derive the standard insertion-only point-query bound and identify every assumption;
2. translate (\varepsilon,\delta), counter width, and memory limits into a concrete matrix;
3. trace standard and conservative updates and explain why their algebra differs;
4. specify compatible merge, serialization, reset, and epoch protocols;
5. distinguish frequency estimation from candidate discovery and threshold policy;
6. diagnose overflow, negative-update, concurrency, skew, and adversarial-collision failures;
7. design tests that separate exact invariants, statistical evidence, and production fitness.

## Core Exposition

### The frequency-vector contract

Represent a stream as updates ((x_t,\Delta_t)). After (T) updates,

$$
f_x=\sum_{t:x_t=x}\Delta_t.
$$

Three stream models must be distinguished. In the **cash-register** or insertion-only model, every (\Delta_t\ge0). In the **strict-turnstile** model, signed updates are allowed but every coordinate remains nonnegative. In the **general-turnstile** model, coordinates may become negative. The familiar CMS minimum estimator has a one-sided proof in the first model: other keys add only nonnegative collision noise. Allowing negative contributions, even when each final coordinate is nonnegative, can make the noise in a bucket negative and destroy the no-underestimate invariant. Linearity of the matrix does not automatically preserve the semantics of the minimum estimator.

The universe may be enormous or implicit. CMS does not allocate by universe size. It does, however, require a stable canonical byte encoding for each key. If two workers encode an integer with different endianness, normalize Unicode differently, or include different tenant prefixes, “the same hash seed” does not mean the same projection.

### Construction and update

Choose width (w), depth (d), counter type, and independently selected row hashes (h_0,\ldots,h_{d-1}). Initialize (C\in\mathbb{R}^{d\times w}) to zero. For a standard update:

$$
C[j,h_j(x)]\leftarrow C[j,h_j(x)]+\Delta
\quad\text{for every }j.
$$

The work is (O(d)); storage is (O(wd)) counters plus configuration. In an insertion-only integer stream, each row sum should equal total accepted mass. That equality is a useful audit invariant, though concurrent snapshots may require a publication protocol to observe it consistently.

A point query reads one counter per row and returns their minimum. Every selected counter contains (f_x) plus contributions from colliding keys, so the minimum tries to find the least contaminated row. It does not identify which keys collided and cannot subtract their contributions exactly.

### Deriving the point-query guarantee

Fix a queried key (x). In row (j), define

$$
Z_j=\sum_{y\ne x} f_y\mathbf{1}[h_j(y)=h_j(x)].
$$

For an insertion-only stream, (Z_j\ge0) and

$$
C[j,h_j(x)]=f_x+Z_j.
$$

If the hash family makes a distinct pair collide with probability at most (1/w), linearity of expectation yields

$$
\mathbb{E}[Z_j]
\le\frac{\sum_{y\ne x}f_y}{w}
\le\frac{\lVert f\rVert_1}{w}.
$$

Set (w=\lceil e/\varepsilon\rceil). Then (\mathbb{E}[Z_j]\le\varepsilon\lVert f\rVert_1/e). Markov's inequality gives

$$
\Pr[Z_j>\varepsilon\lVert f\rVert_1]\le 1/e.
$$

If the row hashes are independently selected, the probability that every row exceeds the allowance is at most ((1/e)^d). Taking (d=\lceil\ln(1/\delta)\rceil) makes that at most (\delta). Since the estimate is the minimum, one good row is sufficient.

This proof is pointwise for a fixed (x). A simultaneous statement for (Q) predetermined queries can use a union bound and a per-query failure budget such as (\delta/Q). Adaptive queries against a revealed fixed sketch require more care: the query process may learn collision structure. A public unkeyed hash is also not a defense against an adversary choosing keys to collide.

### Interpreting additive error

The allowance is (\varepsilon\lVert f\rVert_1), not (\varepsilon f_x). Large keys may receive useful relative accuracy; tiny keys may not. Suppose total mass is one billion and (\varepsilon=10^{-4}). The additive allowance is 100,000. That can support a policy distinguishing multi-million-event keys, but not billing a key with count 12.

The guarantee is also an upper-tail statement. Standard insertion-only CMS never underestimates, so (\widehat f_x) can support conservative “definitely below” logic: if (\widehat f_x<\tau), then (f_x<\tau). Conversely, (\widehat f_x\ge\tau) does not prove (f_x\ge\tau); it identifies a candidate needing exact confirmation or a policy that tolerates false positives.

### Conservative update

Standard update increments all selected counters, including counters already inflated by unrelated keys. **Conservative update** first obtains the current minimum (m), then raises only selected counters below (m+\Delta) to that target (or, for unit updates, increments only counters at the minimum). It preserves no-underestimation for positive updates and often reduces accumulated collision error.

But conservative update is state dependent. If two shards apply it independently, cellwise addition of their matrices generally does not equal conservative update over the concatenated streams. Ordinary CMS is a linear map (S(f+g)=S(f)+S(g)); conservative update is not. A design must choose between this accuracy heuristic and unrestricted algebraic merge, or supply a separately proved aggregation procedure.

### Merge and distributed identity

For standard updates, cellwise addition is exact at the sketch level:

$$
C_{A\cup B}[j,k]=C_A[j,k]+C_B[j,k].
$$

This equality requires matching width, depth, row order, hash algorithm and parameters, seed material, key encoding, counter domain, and update interpretation. It also assumes that the represented stream regions are disjoint when union rather than double counting is intended.

A production envelope should serialize a format version, algorithm identifier, (w,d), counter type and overflow policy, hash-family identifier, seeds, key-schema identifier, update mode, stream model, tenant or namespace, time/epoch interval, and integrity checksum. Merge validation must reject a mismatch before touching the destination. Exactly-once transport is not supplied by the sketch: shard IDs and epoch IDs must prevent retry duplication, and checkpoint lineage must prevent overlapping intervals.

### Counters, overflow, and concurrency

The theorem treats counters as unbounded numbers. Machines do not. Wrapping an unsigned counter can create severe underestimates; signed overflow may be undefined in a systems language; saturation preserves monotonicity but loses merge equality and quantitative meaning after the limit. Options include wider counters, checked rejection, side overflow maps, hierarchical counters, proactive rotation, or exact rebuild from a retained source. Each option changes memory, update latency, and recovery semantics.

An update touches (d) cells. Independent atomic increments can give eventual per-cell correctness, but a concurrent query may observe a mixture of before and after states. Whether that is acceptable depends on the API. Strict snapshot semantics need versioning, seqlocks, reader epochs, copy-on-write generations, or another explicit protocol. A crash between row writes can permanently violate row-sum and no-underestimate expectations unless updates are logged or the sketch is reconstructible.

### Heavy hitters require candidates

CMS accepts a key and estimates its frequency; it does not invert counters into keys. To report heavy hitters, retain candidates through an exact bounded table, a heap fed by observed keys, a hierarchical search structure, or a dedicated frequent-items algorithm. Candidate admission and eviction form a separate error surface. Scanning every possible key defeats the large-universe premise.

A sound threshold workflow may use CMS as a gate: when (\widehat f_x) crosses a lower operational boundary, place (x) into an exact candidate table; confirm before charging, blocking, or alerting. Hysteresis prevents churn. The design must state whether false positives, delayed admission, and false negatives are permitted across the combined sketch-plus-candidate system rather than quoting only the CMS theorem.

### Range and inner-product queries

The original CMS work develops more than point queries. If ordered keys are decomposed into canonical dyadic ranges, a range sum can combine sketches for (O(\log |U|)) nodes; the total error and failure allocation must be composed across those nodes. Sketches of two nonnegative vectors can also estimate an inner product by combining corresponding row counters, with assumptions and error terms that differ from a point query.

These applications are not free consequences of owning one matrix. They require a representation, query algorithm, and theorem specific to the task. Reusing the phrase “CMS error” without restating the norm, stream model, and query family is not a specification.

### Operational evidence

Verification should have layers:

1. exact model tests for update routing, row sums, no-underestimate, merge identity, rejection, serialization, and overflow;
2. property tests across seeds, key encodings, weighted updates, boundaries, and shard partitions;
3. statistical experiments measuring error quantiles and failure frequency on declared synthetic and trace distributions;
4. adversarial tests for chosen collisions, malformed envelopes, duplicate epochs, and reset races;
5. concurrency and crash tests against a defined visibility and durability contract;
6. benchmarks for update/query throughput, cache behavior, memory, merge cost, and candidate-system accuracy.

Passing one deterministic fixture proves only that fixture's assertions. Statistical evidence cannot prove the universal theorem, and a theorem cannot validate an implementation's integer arithmetic or deployment protocol.

The following bounded model uses deliberately small parameters so collisions are visible. Its modular hashes are transparent teaching fixtures, not production hash functions. It checks standard insertion-only updates, no-underestimation for inserted keys, exact cellwise merge, row mass, and the error reduction of conservative update on one order. It does not validate the probability theorem, adversarial resistance, overflow, persistence, or concurrency.

<!-- bijux-verify: {"id":"count-min-mechanisms","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"width=7\ndepth=3\nstream_mass=27\nrow_mass_invariant=True\nstandard_no_underestimate=True\nmerge_matches_full=True\nstandard_total_overestimate=26\nconservative_total_overestimate=9\nkey_45=true:2,standard:13,conservative:7\nabsent_1_estimate=0\nabsent_2_estimate=1\nvalid=True\nevidence=count_min_model\n","stderr":""}} -->
```python
WIDTH = 7
DEPTH = 3
PRIME = 257
HASHES = ((3, 1), (5, 2), (7, 3))


def column(row, key):
    multiplier, offset = HASHES[row]
    return ((multiplier * key + offset) % PRIME) % WIDTH


def blank_sketch():
    return [[0 for _ in range(WIDTH)] for _ in range(DEPTH)]


def estimate(sketch, key):
    return min(sketch[row][column(row, key)] for row in range(DEPTH))


def standard_update(sketch, key, weight):
    for row in range(DEPTH):
        sketch[row][column(row, key)] += weight


def conservative_update(sketch, key, weight):
    target = estimate(sketch, key) + weight
    for row in range(DEPTH):
        col = column(row, key)
        if sketch[row][col] < target:
            sketch[row][col] = target


def merge(left, right):
    return [
        [
            left[row][col] + right[row][col]
            for col in range(WIDTH)
        ]
        for row in range(DEPTH)
    ]


stream = (
    (45, 2), (9, 1), (53, 1), (20, 7),
    (3, 6), (38, 5), (55, 4), (54, 1),
)
full = blank_sketch()
left = blank_sketch()
right = blank_sketch()
conservative = blank_sketch()
truth = {}

for position, (key, weight) in enumerate(stream):
    standard_update(full, key, weight)
    conservative_update(conservative, key, weight)
    truth[key] = truth.get(key, 0) + weight
    shard = left if position < 4 else right
    standard_update(shard, key, weight)

stream_mass = sum(truth.values())
row_mass_invariant = all(sum(row) == stream_mass for row in full)
standard_no_underestimate = all(
    estimate(full, key) >= frequency
    for key, frequency in truth.items()
)
standard_error = sum(
    estimate(full, key) - frequency
    for key, frequency in truth.items()
)
conservative_error = sum(
    estimate(conservative, key) - frequency
    for key, frequency in truth.items()
)
merge_matches_full = merge(left, right) == full
valid = (
    row_mass_invariant
    and standard_no_underestimate
    and merge_matches_full
    and conservative_error < standard_error
)

print(f"width={WIDTH}")
print(f"depth={DEPTH}")
print(f"stream_mass={stream_mass}")
print(f"row_mass_invariant={row_mass_invariant}")
print(f"standard_no_underestimate={standard_no_underestimate}")
print(f"merge_matches_full={merge_matches_full}")
print(f"standard_total_overestimate={standard_error}")
print(f"conservative_total_overestimate={conservative_error}")
print(
    "key_45="
    f"true:{truth[45]},standard:{estimate(full, 45)},"
    f"conservative:{estimate(conservative, 45)}"
)
print(f"absent_1_estimate={estimate(full, 1)}")
print(f"absent_2_estimate={estimate(full, 2)}")
print(f"valid={valid}")
print("evidence=count_min_model")
```

## Definitions and Notation

- (U): key universe; (f_x): accumulated weight of key (x).
- (\lVert f\rVert_1): total absolute vector mass; in an insertion-only stream, total accepted weight.
- (w,d): counter width and row depth.
- (h_j): row-(j) hash into ([w]); (C[j,k]): a counter cell.
- (Z_j): collision noise affecting key (x) in row (j).
- (\widehat f_x): point estimate, normally the minimum selected counter.
- (\varepsilon): additive-error fraction of total mass; (\delta): per-fixed-query upper failure probability under the theorem's assumptions.
- **Linear sketch**: a summary (S) satisfying (S(f+g)=S(f)+S(g)).
- **Conservative update**: a state-dependent positive-update rule that avoids raising already larger selected counters.
- **Heavy hitter**: a key whose frequency exceeds a defined norm-relative or total-mass-relative threshold; the definition must accompany the claim.
- **Sketch envelope**: serialized counters plus every compatibility and lineage field needed to interpret or merge them.

## Mechanisms, Invariants, or Proof Structure

### Point-estimate proof

The proof has five obligations: nonnegative collision noise; bounded pair collision probability; expectation of one row's noise; Markov's one-row tail bound; and independent repetition across rows. The minimum succeeds if any row is good. Removing nonnegativity invalidates the first step; reusing correlated row hashes invalidates the simple product step.

### Merge proof

For ordinary updates, every cell is a sum of weights selected by a fixed indicator:

$$
C_f[j,k]=\sum_x f_x\mathbf{1}[h_j(x)=k].
$$

Therefore (C_{f+g}[j,k]=C_f[j,k]+C_g[j,k]). The proof assumes identical indicators, which is why hash and encoding identity are part of correctness rather than metadata decoration. It proves algebraic combination of vectors, not absence of duplicated stream intervals.

### System invariants

At every committed boundary:

- dimensions and configuration digest match the serialized envelope;
- each standard insertion update contributes equal mass to every row;
- counters have not wrapped or exceeded an acknowledged saturation state;
- merge inputs have compatible configuration and declared, nonoverlapping lineage;
- reset publishes a whole new generation rather than mixing epochs;
- candidate-discovery claims name their auxiliary key-retention mechanism;
- monitoring distinguishes estimate distribution, collision pressure, saturation, dropped updates, duplicate epochs, and exact-sample error.

## Alternatives and Trade-Offs

An exact hash map gives exact point queries and key enumeration but memory grows with cardinality. Misra-Gries or Space-Saving directly retains a bounded candidate set for insertion-only frequent items, often making it a better answer to “which keys are heavy?” Count Sketch uses signed hashes and a median estimator, supporting different (\ell_2)-style error behavior and signed-update settings at greater width for a target accuracy. Sampling can preserve example records and support different estimands, but rare events may disappear. Bloom-family structures answer membership rather than frequency. Hierarchical CMS adds range or prefix discovery at extra update and query cost.

Standard CMS favors simple linear merge. Conservative update may lower positive bias but complicates distributed combination. Larger width lowers collision noise; greater depth lowers the chance that all rows are bad but increases update cost. Wider counters postpone overflow but consume memory. Keyed hashes improve resistance to chosen collisions but complicate reproducibility, rotation, and cross-worker coordination. An estimator derived from empirical counter-noise distributions can tighten typical answers, but it adds statistical assumptions and cannot be substituted silently for the minimum estimator's published contract.

## Failure Modes and Misconceptions

- **“One percent error” means relative error.** The classic allowance is (\varepsilon\lVert f\rVert_1), which can dwarf a rare key.
- **The estimate is exact when rows agree.** The same colliders may affect every row, particularly under weak or attacked hashing.
- **Strict turnstile is enough for the minimum proof.** Negative collision contributions can cause underestimation even if final coordinates remain nonnegative.
- **CMS lists heavy hitters.** It estimates named keys; candidate discovery is separate.
- **Any sketches of the same dimensions merge.** Hash, encoding, mode, counter, namespace, and lineage must also match.
- **Conservative update is linear.** Its writes depend on current counter values, so arbitrary cellwise shard merging does not reproduce a global conservative execution.
- **Saturation is safe because it cannot wrap.** It prevents wraparound but can destroy quantitative bounds and merge equality.
- **Atomic counters make an atomic update.** A query may observe a partially applied (d)-cell update.
- **A low average error validates (\delta).** Averages do not measure tail failure, and one dataset does not establish a distribution-free theorem.
- **Published hashes are harmless.** An adversary may generate colliding keys; keyed seeds and rotation may be required.
- **Resetting counters resets the stream.** Late events, retries, and old shard snapshots can contaminate a new epoch without lineage controls.
- **A successful deterministic test validates production.** It covers only selected keys, arithmetic, and configuration.

## Worked Examples

### Example 1

**Parameter sizing.** A service requests (\varepsilon=0.002) and (\delta=10^{-5}). Compute (w=\lceil e/0.002\rceil=1{,}360) and (d=\lceil\ln 100{,}000\rceil=12). The matrix has 16,320 counters. With 64-bit counters it occupies 130,560 bytes before alignment and metadata. **Conclusion:** accuracy parameters must be converted into counter bytes, not reported as abstract asymptotics.

### Example 2

**One-row bound.** Let total insertion mass be 2,000,000 and width 272. Expected collision noise in a row is at most (2{,}000{,}000/272\approx7{,}352.94). For (\varepsilon=0.01), the bad threshold is 20,000. Markov bounds the row's bad probability by (7{,}352.94/20{,}000\approx0.36765<1/e). **Conclusion:** width creates an expectation bound; depth amplifies it into a tail bound.

### Example 3

**Rare-key counterexample.** Total mass is (10^9), (\varepsilon=10^{-4}), and a key occurs 30 times. The formal additive allowance is 100,000, over 3,333 times the true count. **Conclusion:** the theorem may be correct while the estimator is unsuitable for rare-key billing.

### Example 4

**Merge trace.** Worker A and B share configuration digest cms-7x3-seed-k1. For a particular cell they hold 18 and 11, so the merged cell is 29. Worker C has the same dimensions but digest cms-7x3-seed-k2; its value 5 must not be added because it represents a different projection. **Conclusion:** compatibility is semantic identity, not rectangular shape.

### Example 5

**Duplicate epoch.** Shard s7 emits epoch 42 with counter mass 80,000. A retry is delivered twice. Cellwise merging both copies makes row mass 160,000 although the sketch arithmetic itself is flawless. Deduplicating the shard, epoch, and digest tuple before merge preserves the intended union. **Conclusion:** distributed exactly-once accounting lies outside CMS algebra.

### Example 6

**Negative-update failure.** In one row, key (x) has true frequency 8 while colliding key (y) has net update (-5). The selected counter is 3, below (f_x). Taking a minimum across such counters no longer guarantees an upper estimate. **Conclusion:** linear signed updates do not retain the insertion-only minimum theorem.

### Example 7

**Overflow policy.** A 16-bit unsigned counter at 65,530 receives weight 10. Wrapping yields 4 and creates underestimation. Saturation yields 65,535, avoids wrap, but the lost amount is unknown and future merges cannot recover it. A checked overflow side record can preserve meaning at added cost. **Conclusion:** counter representation is part of the estimator contract.

### Example 8

**Heavy-hitter gate.** A policy threshold is 50,000. CMS estimates key (k) at 53,000. Because positive collisions can inflate the estimate, the system admits (k) to an exact candidate table and confirms 47,500; it does not charge the key. **Conclusion:** an upper-biased sketch is useful as a candidate gate when downstream confirmation owns the consequential decision.

### Example 9

**Conservative-update trade-off.** The executable fixture has total overestimate 26 under ordinary updates and 9 under conservative update. Yet only the ordinary left and right shard matrices add exactly to the ordinary full-stream matrix. **Conclusion:** improved fixture accuracy and linear mergeability are different properties; neither dominates universally.

### Example 10

**Simultaneous query budget.** A report will issue 10,000 predetermined point queries and wants total failure probability at most (10^{-4}). A union-bound design assigns (\delta'=10^{-8}) per query, giving (d=\lceil\ln 10^8\rceil=19). This does not automatically cover indefinitely adaptive queries. **Conclusion:** the quantification over queries must be explicit when choosing depth.

## Cross-Program Connections

- **Database Engineering:** approximate group counts and join-size estimation require optimizer-specific error propagation and fallback paths.
- **Data Engineering:** shard merges, event-time windows, replay, deduplication, and schema evolution determine whether a sketch represents the intended stream.
- **Distributed Systems:** compatible semigroups do not solve delivery identity, epoch overlap, or consensus about reset boundaries.
- **Security Engineering:** public weak hashes permit chosen-collision denial or evasion; seed secrecy and rotation need threat modeling.
- **Software Engineering Patterns:** the sketch envelope is a versioned value object whose validation guards every merge boundary.
- **Concurrent and Parallel Programming:** cache-local counter layouts, atomic increments, snapshot semantics, and false sharing affect correctness and throughput.

## References

1. Graham Cormode and S. Muthukrishnan, [An Improved Data Stream Summary: The Count-Min Sketch and Its Applications](https://doi.org/10.1016/j.jalgor.2003.12.001), *Journal of Algorithms* 55(1), 2005; publisher record.
2. Graham Cormode, [Count-Min Sketch](https://doi.org/10.1007/978-3-642-27848-8_579-1), *Encyclopedia of Algorithms*, 2014; publisher record.
3. Cristian Estan and George Varghese, [New Directions in Traffic Measurement and Accounting](https://escholarship.org/uc/item/8rx3b221), *ACM SIGCOMM*, 2002; primary record and paper for multistage filters and conservative update.
4. Daniel Ting, [Count-Min: Optimal Estimation and Tight Error Bounds Using Empirical Error Distributions](https://arxiv.org/abs/1811.04150), *KDD*, 2018.
5. Moses Charikar, Kevin Chen, and Martin Farach-Colton, [Finding Frequent Items in Data Streams](https://www.cs.princeton.edu/courses/archive/spring04/cos598B/bib/CharikarCF.pdf), *Theoretical Computer Science* 312(1), 2004.
6. Graham Cormode and Marios Hadjieleftheriou, [Finding Frequent Items in Data Streams](https://hadjieleftheriou.com/papers/vldb08-2.pdf), *PVLDB* 1(2), 2008.
7. Apache Software Foundation, [Count-Min Sketch API](https://apache.github.io/datasketches-cpp/5.1.0/classdatasketches_1_1count__min__sketch.html), DataSketches C++ 5.1.0 documentation, accessed 2026-08-30.

## Exercises

### Exercise 1

For (\varepsilon=0.005), (\delta=10^{-7}), and 32-bit counters, compute (w,d), the counter count, and raw counter bytes. State the point-query guarantee for an insertion-only stream of mass 12,000,000.

### Exercise 2

Prove the ordinary CMS merge identity cell by cell. Then list six configuration fields whose mismatch invalidates the proof in a concrete implementation.

### Exercise 3

A deployment allows negative corrections, uses unsigned saturating counters, and advertises the insertion-only no-underestimate theorem. Diagnose the contradictions and propose two coherent redesigns.

### Exercise 4

Design a distributed CMS envelope and merge workflow for hourly telemetry across 200 shards with retries and late data. Include validation, deduplication, reset, overflow, and audit evidence.

### Exercise 5

A fraud service must find accounts above 0.05% of daily events, but blocking a legitimate account is costly. Daily mass is uncertain between (5\times10^7) and (2\times10^8). Design a sketch-plus-candidate decision system, including parameter logic, confirmation, and tests. Explain what CMS alone cannot promise.

## Answers to the Exercises

### Answer 1

(w=\lceil e/0.005\rceil=544). (d=\lceil\ln 10^7\rceil=17). There are (544\times17=9{,}248) counters, consuming (9{,}248\times4=36{,}992) raw bytes before alignment and metadata. The additive allowance is (0.005\times12{,}000{,}000=60{,}000). For a fixed key under nonnegative updates and the stated independent hash assumptions,

$$
f_x\le\widehat f_x\le f_x+60{,}000
$$

with probability at least (1-10^{-7}). This is not 0.5% relative error for the key.

### Answer 2

For fixed cell ((j,k)),

$$
C_{f+g}[j,k]
=\sum_x(f_x+g_x)\mathbf1[h_j(x)=k]
=C_f[j,k]+C_g[j,k].
$$

Since this holds for every cell, the matrices add. Concrete compatibility requires at least width, depth and row ordering, hash-family/version, per-row seeds, canonical key encoding/schema, counter numeric type and overflow rule, plus standard rather than conservative update semantics. Namespace and epoch lineage do not change the algebraic indicators, but they are necessary to ensure the vectors being added are the intended disjoint populations.

### Answer 3

Negative corrections remove nonnegative collision noise, so the minimum may underestimate. Unsigned counters cannot represent a negative cell, and saturation makes the linear transform and exact merge identity fail after clipping. One redesign keeps an insertion-only CMS for accepted positive events and records corrections in an exact bounded ledger or separately analyzed structure; queries combine them under a new contract. Another uses a signed linear sketch such as Count Sketch with signed counters and its applicable estimator/error theorem. Either design needs checked arithmetic, a declared stream model, and tests containing negative collisions. Merely changing the counter type does not restore the CMS minimum proof.

### Answer 4

The envelope contains format and algorithm versions, dimensions, row order, hash identity and seeds, key schema, counter type/overflow state, update mode, tenant, UTC hour, shard ID, source-offset interval, generation, and checksum. Each shard seals an immutable hourly snapshot and emits a unique lineage tuple. The reducer validates the complete configuration digest, checksum, nonoverlapping source interval, and unseen lineage before cellwise addition; retries are idempotently acknowledged. Late data enters a named correction epoch rather than mutating an already published hour invisibly. Generation publication makes reset atomic. Checked counters fail before overflow and trigger rotation or wider rebuild. Evidence includes per-row mass reconciliation, source-offset totals, accepted/rejected lineage logs, merge-order property tests, corrupted-envelope tests, replay tests, and exact sampled-key comparisons.

### Answer 5

The lowest threshold occurs at (0.0005\times5\times10^7=25{,}000); the highest is 100,000. Choose an additive allowance small relative to the lowest decision margin, not merely relative to maximum volume. For example, if exact confirmation should begin 5,000 below the threshold, require (\varepsilon\lVert f\rVert_1\le5{,}000) at the worst expected mass or rotate into smaller windows; at (2\times10^8), this means (\varepsilon\le2.5\times10^{-5}). Allocate (\delta) across the predetermined daily query budget and threat model. Feed observed keys whose estimate approaches the gate into a bounded exact table, retain hysteresis, and block only after exact confirmation. Deduplicate events and shard epochs, use compatible ordinary sketches for merge, and rebuild on overflow. Tests cover boundary counts, skew, candidate eviction, retry duplication, late data, seeds, chosen collisions, and exact sampled comparisons. CMS alone cannot enumerate accounts, guarantee relative error for a rare account, prevent threshold false positives, provide exactly-once ingestion, or justify blocking.
