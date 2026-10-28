---
module_id: DSE-085
program: Data Structures Engineering
level: 2
module_number: 85
title: HyperLogLog
status: complete
last_verified: 2026-08-30
---

# HyperLogLog

## One-Page Review

### Governing question

How can a system estimate the number of distinct values with bounded memory while preserving duplicate insensitivity, merge semantics, estimator validity, and representation compatibility?

### Essential definitions

For a multiset stream (S), its **cardinality** is $n=|\{x:x\in S\}|$. HyperLogLog (HLL) hashes each canonical key to a uniform bit string. With precision (p), the first (p) bits select one of (m=2^p) registers. From the remaining bits, $\rho$ is one plus the number of leading zeros. Update is

$$
M[j]\leftarrow\max(M[j],\rho).
$$

Duplicates are idempotent because repeating the same hash repeats the same maximum. The classical raw estimator is

$$
E_{\mathrm{raw}}
=\alpha_m m^2
\left(\sum_{j=0}^{m-1}2^{-M[j]}\right)^{-1}.
$$

Its asymptotic relative standard error is approximately $1.04/\sqrt m$ under the ideal-hash model. Small-cardinality regimes need correction; the original algorithm uses linear counting $m\ln(m/V)$ when (V), the number of zero registers, remains positive and the raw estimate is small.

### Central model, mechanism, or theorem

One extreme zero-prefix observation is noisy. HLL performs stochastic averaging across (m) hash-selected substreams, stores the maximum rank in each, and uses a bias-corrected harmonic aggregation. The register array represents a join-semilattice: merge is componentwise maximum. Thus duplicate ingestion and overlapping input sets do not double count at the representation level, provided both sketches use the same precision, hash definition, seed, key encoding, register convention, and estimator family.

### Critical invariants

- A register changes only to a greater representable rank.
- Re-adding a value leaves the sketch unchanged.
- Merge is componentwise maximum, so it is associative, commutative, and idempotent.
- Equal dimensions alone do not establish merge compatibility; hashes and encodings define register meaning.
- Sparse-to-dense conversion must preserve the same logical register maxima.
- A cardinality estimate is not a retained sample, frequency table, membership oracle, or exact set.
- Hash collisions make distinct keys observationally identical; finite hash width limits the meaningful cardinality range.

### Common failures

Typical failures include feeding unstable serialization, merging different seeds, summing registers, using registerwise minimum for intersection, treating relative standard error as a deterministic bound, applying the raw estimator at small cardinality, overflowing packed registers, confusing event count with distinct count, silently changing estimator versions, and double-counting semantic entities whose identifiers were not normalized consistently.

### Compact example

A teaching sketch with (p=5) has 32 registers. Hashing 80 distinct integers leaves 3 zeros, a maximum rank of 6, raw estimate 67.672, and linear-counting estimate 75.748. Replaying all 80 values changes no register. Merging sketches for values 0–59 and 40–79 by registerwise maximum exactly reproduces the register array built from the 80-value union, despite 20 overlapping values.

### Connections

[DSE-084](084-count-min-sketch.md) supplies sketch contracts, hashing, estimator-versus-decision reasoning, and distributed envelopes. The roadmap successor is [DSE-086, “Quantile Sketches”](../ROADMAP.md), where mergeable summaries approximate rank rather than set cardinality. Database and Data Engineering own distinct aggregation plans, partition lineage, windowing, and schema semantics around the structure.

## Governing Question

How should HyperLogLog be derived, implemented, merged, serialized, corrected, tested, and operated so that “approximately distinct” remains a precise and reviewable claim?

## Why This Matters

Exact distinct counting retains every distinct identity or an equivalent exact structure, so memory grows with cardinality. A global product metric may span billions of events, thousands of shards, and repeated observations of the same user. HLL compresses each partition to a fixed-size register summary and merges overlaps without adding duplicates again at the sketch level.

That advantage is easy to misuse. HLL assumes hash outputs behave like uniform independent bit strings. Cardinality semantics depend on key normalization and scope. Estimator behavior changes across small, intermediate, and hash-saturation regimes. Sparse encodings, bias tables, compressed registers, and union objects differ across implementations. A production result is trustworthy only when the mathematical estimator, binary representation, stream identity, and product decision are specified together.

## Prerequisites and Retrieval

Retrieve:

- uniform hashing, geometric distributions, expectation, variance, and standard error;
- harmonic means, logarithms, relative versus absolute error, and confidence language;
- idempotent, associative, and commutative merge operations;
- canonical key serialization, hash seeds, versioned envelopes, and distributed lineage;
- the additive point-estimation contract and merge discipline of [DSE-084](084-count-min-sketch.md).

Recall that $\Pr[\rho(h)=k]=2^{-k}$ for $k\ge1$ when $\rho$ is one plus the leading-zero count of an ideal infinite fair bit string. Equivalently, $\Pr[\rho(h)>k]=2^{-k}$. Long zero prefixes are exponentially rare, so their maxima encode logarithmic information about how many distinct hashes were observed.

## Learning Objectives

After this chapter, you should be able to:

1. trace index and rank extraction from a finite hash value;
2. explain stochastic averaging, harmonic aggregation, and the $1.04/\sqrt m$ error scale;
3. apply and critique raw, small-range, and modern bias-corrected estimators;
4. prove duplicate idempotence and registerwise-max merge laws;
5. specify sparse/dense conversion, serialization, compatibility, and upgrade contracts;
6. diagnose hash, normalization, intersection, reset, overflow, concurrency, and privacy failures;
7. design deterministic, statistical, adversarial, and distributed validation evidence.

## Core Exposition

### Distinctness as a hash experiment

Let (D) be the set of canonical keys observed in a scope, and (n=|D|). HLL never sees mathematical identities directly; it sees hash values. A canonicalization function (c(x)) produces bytes, and a versioned hash (h(c(x))) produces (L) bits. Two equivalent entities encoded differently are counted separately. Two distinct entities with the same (L)-bit hash are indistinguishable. The operational estimand is therefore distinct canonical hash values, which approximates distinct semantic entities only when normalization and collision risk are acceptable.

The leading-zero statistic follows a geometric tail. Among (n) uniform hashes, the largest observed rank is near $\log_2 n$, but one maximum has high variance. LogLog-style algorithms split the hash stream into substreams. HLL uses (p) index bits to assign each hash to one of (m=2^p) registers and records the maximum rank of the remaining (L-p) bits in that register.

Use a consistent bit convention. An implementation may take high bits for the index and count zeros in the low suffix, or take low bits and count zeros in the high suffix. Either can work if hash uniformity supports it, rank bounds are correct, and every producer uses exactly the same convention. An all-zero suffix needs a defined maximum rank, normally (L-p+1); reading beyond the finite hash is a bug.

### Register update and sufficient state

For value (x), compute $j=\operatorname{index}(h(x))$ and $r=\rho(\operatorname{suffix}(h(x)))$, then set $M[j]=\max(M[j],r)$. A duplicate produces the same ((j,r)), hence no change after the first occurrence. Different keys may map to the same register; only the largest rank survives.

The array is deliberately lossy. It cannot enumerate values, answer membership, estimate frequency, or delete one value. Removing an element might require recovering the second-largest rank for its register, information that ordinary HLL discarded. Sliding windows therefore need time-partitioned sketches, expiring auxiliary state, or a different algorithm; decrementing a register is not a valid inverse.

Register width must represent ranks up to (L-p+1), plus any implementation sentinel or compression state. With 64-bit hashes and usual precision, six bits can represent raw ranks, but packed formats may store deltas from a baseline and exceptions. Overflow or a changed rank convention corrupts estimation and union semantics even if the byte array remains parseable.

### Raw estimator and stochastic averaging

Suppose register (j) summarizes a substream containing about (n/m) distinct hashes. Large (M[j]) suggests a larger substream. Directly averaging (2^{M[j]}) is unstable because extreme registers dominate. HLL instead uses a normalized harmonic form:

$$
Z=\left(\sum_{j=0}^{m-1}2^{-M[j]}\right)^{-1},
\qquad
E_{\mathrm{raw}}=\alpha_m m^2 Z.
$$

The constant $\alpha_m$ corrects asymptotic bias under the idealized model. The original presentation uses special constants for small standard register counts—approximately 0.673, 0.697, and 0.709 for (m=16,32,64)—and (0.7213/(1+1.079/m)) for larger (m). Copying a constant without matching the estimator definition is unsafe: indexing, rank origin, corrections, and register representation must agree.

For sufficiently large (m) away from boundary regimes, relative standard error is approximately

$$
\operatorname{RSE}\approx\frac{1.04}{\sqrt m}.
$$

At (p=12), (m=4096), giving about 1.625%. This is a standard-deviation scale under a probability model, not a hard interval that every sketch satisfies. Doubling precision by one bit doubles registers but reduces RSE only by a factor $1/\sqrt2$. Achieving half the RSE needs about four times as many registers.

### Small and large regimes

At low cardinality, many registers remain zero and the raw estimator has appreciable bias. Let (V=|\{j:M[j]=0\}|). Linear counting estimates

$$
E_{\mathrm{LC}}=m\ln(m/V).
$$

The original HLL procedure selects this estimate for a small raw range when (V>0). HyperLogLog++ uses sparse representation and empirically calibrated corrections; later work derives estimators that avoid some historical discontinuities and bias tables. “HLL estimate” is therefore incomplete metadata. The estimator name and version belong beside the registers.

At the other extreme, finite hash space causes collisions and rank censoring. The original 32-bit treatment included a large-range correction. Modern systems often hash to 64 or 128 bits and use newer estimators, but no finite hash eliminates saturation. A correction formula valid for one hash width must not be transplanted to another. Capacity planning must bound distinct hashes, birthday-collision risk, maximum rank, and estimator validity for the chosen implementation.

### Sparse and dense representations

A dense register array has fixed update and union mechanics but wastes space when few registers have changed. A sparse form stores observed index/rank information or encoded hashes until a threshold, then converts to dense. Sparse mode may be exact for a limited set of hashes or merely a more compact HLL encoding, depending on the implementation.

Conversion must be representation-preserving: expanding the sparse entries and taking per-register maxima must yield the same logical dense state as processing the same hashes directly. Transition thresholds are performance policies, not theorem constants. Tests should cover the entry immediately before, during, and after conversion; serialization in both modes; union of sparse with dense; and conversion during concurrent access.

### Union as a semilattice

For compatible arrays (A) and (B), define

$$
(A\sqcup B)[j]=\max(A[j],B[j]).
$$

Maximum is associative, commutative, and idempotent. Therefore union trees may be regrouped and reordered, retries of the identical sketch do not change the logical register state, and overlap between input sets is naturally represented. This is different from Count-Min Sketch, whose ordinary merge adds cells because frequencies from disjoint event partitions should accumulate.

The algebra does not make incompatible sketches compatible. Precision changes register partitioning. A different seed or key encoding changes the mapping. Some libraries support union across selected precision differences by downsampling to a lower precision under explicit rules; arbitrary upsampling cannot recreate information that was never stored. Treat library-specific union behavior as a versioned protocol.

### Intersection and set difference

Registerwise minimum is not an HLL intersection operator. Inclusion-exclusion can form

$$
|A\cap B|\approx\widehat{|A|}+\widehat{|B|}-\widehat{|A\cup B|},
$$

but subtracting similar noisy estimates can produce large relative error or even an impossible negative result. Joint maximum-likelihood estimators improve some cases, yet they need their own assumptions and evidence. When intersection, difference, or subset estimates are primary requirements, Theta-style sketches or another set-operation-oriented representation may be a better design.

### Serialization, lineage, and distributed use

A durable envelope should include format version, HLL algorithm and estimator version, precision, register/rank convention, hash algorithm and seed identity, canonical key schema, sparse/dense mode, register encoding, namespace, logical time window, producer generation, and checksum. An implementation should validate compatibility before allocating or mutating a union target.

Idempotent max merge prevents repeated identical register arrays from changing state, but it does not solve every delivery error. A late sketch built from a different key-normalization version may inflate distinctness. Resetting a window while writers still publish old-generation registers contaminates the new scope. A corrupted sketch with artificially high registers can dominate every later union. Lineage, authentication, generation fencing, and plausible-rank validation remain necessary.

### Concurrency, privacy, and operations

Concurrent register max can often use atomic compare-and-swap because each update is monotone. A query reading registers independently obtains a weak snapshot: values may come from different instants, but no register moves backward. If the API promises a linearizable estimate or serialized image, it needs stronger snapshot coordination. Sparse structures and mode conversion are especially likely to require locks, version words, or copy-on-write publication.

HLL is not anonymization. A sketch can reveal approximate population sizes, changes, unions, and small-set information; chosen inputs may probe behavior. Hashing identifiers without a privacy model does not make publication safe. Access control, minimum cohort rules, differential privacy where required, and seed management are separate responsibilities.

Operations should expose precision, estimator version, mode, zero-register count, maximum rank, register histogram, union rejection counts, corrupt-input counts, generation, and comparison against exact sampled windows. Alarms should detect implausible rank spikes, unexpected mode churn, incompatible producer versions, and estimates outside planned cardinality ranges.

### Evidence hierarchy

Deterministic tests prove update routing, duplicate idempotence, merge laws, conversion equivalence, serialization round trips, and rejection behavior. Statistical experiments across many independent seeds and declared cardinalities measure bias, RSE, quantiles, and interval coverage. Adversarial tests target normalization, chosen hashes, corrupt registers, downgrade, and generation races. Concurrency and crash tests validate publication and recovery. Benchmarks measure throughput, cache footprint, union fan-in, sparse/dense crossover, and serialized size.

The bounded model below uses 64-bit deterministic mixing, 32 unpacked registers, the classical raw constant for (m=32), and the original small-range selection. It is deliberately tiny so sampling error is visible. It checks representation invariants only; it is not evidence for production hashing, asymptotic RSE, bias correction, packed formats, concurrency, or deployment fitness.

<!-- bijux-verify: {"id":"hyperloglog-mechanisms","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"precision=5\nregisters=32\ntrue_union=80\nzero_registers=3\nnonzero_registers=29\nmax_rank=6\nraw_estimate=67.672\ncorrected_estimate=75.748\nrelative_error=-0.0532\nduplicates_idempotent=True\nmerge_matches_full=True\nmerge_commutative=True\nmerge_idempotent=True\nvalid=True\nevidence=hyperloglog_model\n","stderr":""}} -->
```python
import math

MASK = (1 << 64) - 1
PRECISION = 5
REGISTER_COUNT = 1 << PRECISION


def mix64(value):
    mixed = (value + 0x9E3779B97F4A7C15) & MASK
    mixed = ((mixed ^ (mixed >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    mixed = ((mixed ^ (mixed >> 27)) * 0x94D049BB133111EB) & MASK
    return mixed ^ (mixed >> 31)


def location(value):
    hashed = mix64(value)
    index = hashed & (REGISTER_COUNT - 1)
    suffix = hashed >> PRECISION
    rank = 1
    bit = 1 << (64 - PRECISION - 1)
    while bit and not (suffix & bit):
        rank += 1
        bit >>= 1
    return index, rank


def add(registers, value):
    index, rank = location(value)
    if rank > registers[index]:
        registers[index] = rank


def merge(left, right):
    return [
        max(left[index], right[index])
        for index in range(REGISTER_COUNT)
    ]


def estimate(registers):
    harmonic_sum = sum(2.0 ** (-rank) for rank in registers)
    raw = 0.697 * REGISTER_COUNT * REGISTER_COUNT / harmonic_sum
    zeros = sum(rank == 0 for rank in registers)
    corrected = raw
    if zeros and raw <= 2.5 * REGISTER_COUNT:
        corrected = REGISTER_COUNT * math.log(REGISTER_COUNT / zeros)
    return raw, corrected, zeros


full = [0 for _ in range(REGISTER_COUNT)]
left = [0 for _ in range(REGISTER_COUNT)]
right = [0 for _ in range(REGISTER_COUNT)]

for value in range(80):
    add(full, value)
for value in range(60):
    add(left, value)
for value in range(40, 80):
    add(right, value)

before_replay = full[:]
for value in range(80):
    add(full, value)

raw, corrected, zeros = estimate(full)
union = merge(left, right)
valid = before_replay == full and union == full and zeros == 3

print(f"precision={PRECISION}")
print(f"registers={REGISTER_COUNT}")
print("true_union=80")
print(f"zero_registers={zeros}")
print(f"nonzero_registers={REGISTER_COUNT - zeros}")
print(f"max_rank={max(full)}")
print(f"raw_estimate={raw:.3f}")
print(f"corrected_estimate={corrected:.3f}")
print(f"relative_error={(corrected / 80) - 1:.4f}")
print(f"duplicates_idempotent={before_replay == full}")
print(f"merge_matches_full={union == full}")
print(f"merge_commutative={merge(left, right) == merge(right, left)}")
print(f"merge_idempotent={merge(full, full) == full}")
print(f"valid={valid}")
print("evidence=hyperloglog_model")
```

## Definitions and Notation

- (D): set of distinct canonical values; (n=|D|): true cardinality.
- (L): hash width; (p): precision bits; (m=2^p): register count.
- (j): register index; $\rho$: one plus the leading-zero count in the hash suffix.
- (M[j]): maximum rank observed for register (j).
- (V): number of zero registers.
- $E_{\mathrm{raw}}$: classical harmonic raw estimate; $E_{\mathrm{LC}}$: linear-counting small-range estimate.
- $\alpha_m$: normalization constant tied to the raw estimator definition.
- **Relative error**: $(\widehat n-n)/n$; **RSE**: its modeled standard deviation divided by the true value.
- **Sparse mode**: a compact early-cardinality representation; **dense mode**: the full register array.
- **Logical sketch state**: the register maxima independent of a particular packed encoding.
- **Compatible union**: componentwise maximum between states with identical semantic configuration or an explicitly supported conversion.

## Mechanisms, Invariants, or Proof Structure

### Duplicate and union proof

For a value (x), update applies maximum with a fixed rank at a fixed register. Since $\max(a,r,r)=\max(a,r)$, replay is idempotent. For arrays, componentwise maximum inherits associativity, commutativity, and idempotence from scalar maximum. Each register of a union therefore equals the maximum rank produced by any distinct hash assigned to it.

### Estimator argument

The rank tail is geometric. Register maxima summarize substream scale; stochastic averaging across hash-selected substreams reduces variance; harmonic aggregation limits domination by extreme registers; $\alpha_m$ corrects asymptotic bias. The full theorem in the original analysis depends on an ideal-multiset model and analytic corrections. The short argument supplies mechanism and intuition, not a substitute proof of the constant or error law.

### Engineering invariants

- canonical bytes and hash/version metadata define value identity;
- every rank lies within the finite-hash and packed-register bounds;
- sparse and dense forms decode to the same logical maxima;
- union either validates compatibility completely or rejects before mutation;
- estimator version remains attached to stored state and reported results;
- sealed window/generation identity prevents old writers from contaminating new scope;
- corruption cannot install unchecked high ranks that permanently dominate a union;
- exact audits measure semantic distinctness with the same normalization rules.

## Alternatives and Trade-Offs

An exact hash set is appropriate when cardinality is small, identifiers must be recovered, deletion is required, or zero error is mandatory. Linear counting is simple and effective while many bitmap positions remain empty but loses range as the bitmap fills. Theta or bottom-(k) sketches use retained hash samples and naturally support union, intersection, and difference estimates at a larger size for comparable distinct-count accuracy. CPC targets stronger compression for unique counting. KMV sampling can expose witnesses and support set operations, but its memory/accuracy and update mechanics differ.

Within HLL, greater (p) reduces RSE but increases dense size and union bandwidth. Sparse mode saves early memory at conversion complexity. Four-bit compressed registers save bytes but require baselines and exception handling; wider registers simplify operations. Historical raw-plus-threshold correction is easier to teach, while modern empirical, HIP, or maximum-likelihood estimators can reduce bias or improve accuracy but create version and merge-order obligations. A mature library is preferable to an ad hoc packed implementation when its estimator and compatibility contract match the application.

## Failure Modes and Misconceptions

- **RSE is a deterministic maximum.** It is a distributional scale under a hash model.
- **Duplicates increment the estimate.** They leave the logical state unchanged; estimate variation comes from distinct hashes.
- **Max registers should be summed during merge.** HLL union takes componentwise maximum.
- **Idempotent merge means ingestion semantics cannot fail.** Wrong windows, schemas, or identities still produce a valid but wrong union.
- **Same precision means compatible.** Hash, seed, encoding, rank convention, and version must also agree.
- **Registerwise minimum gives intersection.** It has no such general estimator contract.
- **Inclusion-exclusion is always accurate.** Subtracting noisy, similar large estimates can magnify error.
- **HLL supports deletion.** A register maximum does not retain the next-largest witness.
- **The raw estimator works everywhere.** Small-range bias and finite-hash saturation require appropriate handling.
- **Six-bit registers can never overflow.** The bound depends on hash width, precision, rank origin, and exception encoding.
- **Hashing supplies privacy.** Cardinality and differencing can leak information; hashes may be reversible for small domains.
- **A sparse form is necessarily exact.** Its semantics depend on the implementation.
- **One seed experiment validates 1.04/sqrt(m).** RSE needs repeated independent trials over declared workloads.

## Worked Examples

### Example 1

**Index and rank trace.** Let (p=4) and a 16-bit teaching hash be 1011 000101001011. The index is binary 1011, or register 11. The suffix begins with three zeros then one, so $\rho=4$. If (M[11]=2), it becomes 4; if it is already 5, it stays 5. **Conclusion:** one hash deterministically chooses both the register and monotone rank update.

### Example 2

**Precision sizing.** For (p=12), (m=4096), so modeled RSE is (1.04/64=0.01625), or 1.625%. At (p=14), (m=16{,}384), RSE becomes (1.04/128=0.008125), or 0.8125%, while register storage quadruples. **Conclusion:** halving stochastic error costs about four times the registers.

### Example 3

**Small-range correction.** With (m=32) and (V=3), linear counting is $32\ln(32/3)\approx75.748$. The executable raw estimate is 67.672 for truth 80. **Conclusion:** early-cardinality estimator selection materially affects bias; zero-register evidence should not be discarded.

### Example 4

**Duplicate replay.** A batch of one million events contains only 12,000 canonical user IDs. Replaying the identical batch produces the same hashes and maxima, so the logical HLL state does not change. Replaying after changing normalization from lowercase to case-sensitive may change identities and inflate state. **Conclusion:** algebraic idempotence assumes stable semantic encoding.

### Example 5

**Overlapping union.** Sketch A represents IDs 0–59 and B represents 40–79. Their sets overlap by 20, but registerwise maximum produces the same state as hashing IDs 0–79 once. Adding estimates or registers would double count overlap. **Conclusion:** HLL union operates on representations, not on estimated scalars.

### Example 6

**Incompatible seed.** Two (p=14) byte arrays use different seeds. Register 812 in one has no relationship to register 812 in the other. Max-merging them constructs neither union distribution. **Conclusion:** equal layout does not imply equal random projection.

### Example 7

**Intersection instability.** Suppose estimates are (widehat{|A|}=1{,}000{,}000), (widehat{|B|}=1{,}010{,}000), and $widehat{|A\cup B|}=2{,}020{,}000$. Inclusion-exclusion reports (-10{,}000), an impossible intersection caused by estimator noise. **Conclusion:** clamp-to-zero hides rather than solves set-operation uncertainty.

### Example 8

**Packed-register corruption.** A malformed input sets one decoded register to rank 63 although (L-p+1=51). Because union is maximum, that rank persists into every downstream aggregate. Validation rejects it before merge and records the producer/checksum. **Conclusion:** monotonicity amplifies unchecked corruption.

### Example 9

**Window reset race.** A new daily generation starts at midnight, but an old writer publishes its previous register array after reset. Max merge carries yesterday's maxima forward. Generation fencing rejects the stale writer; late events go to a named correction window. **Conclusion:** HLL cannot infer temporal ownership from registers.

### Example 10

**Estimator version migration.** Stored logical registers were created under estimator A; software B introduces a new estimator without changing register update semantics. Re-estimation may be valid if B explicitly supports that logical format, but cached scalar estimates must be recomputed and versioned. If B changes hashing or rank definition, rebuild is required. **Conclusion:** distinguish representation compatibility from estimator compatibility.

## Cross-Program Connections

- **Database Engineering:** approximate distinct aggregation, grouping, and optimizer statistics need error-aware plans and exact fallbacks.
- **Data Engineering:** event-time windows, canonical schemas, replay, and partition union determine the represented set.
- **Distributed Systems:** semilattice merge enables convergent union, while generation and membership protocols define scope.
- **Security Engineering:** malicious ranks, chosen hashes, differencing attacks, and seed exposure require validation and access policy.
- **Concurrent and Parallel Programming:** atomic max, false sharing, sparse conversion, consistent snapshots, and tree reduction govern throughput.
- **Software Engineering Patterns:** versioned envelopes and compatibility matrices prevent silent cross-version corruption.

## References

1. Philippe Flajolet, Éric Fusy, Olivier Gandouet, and Frédéric Meunier, [HyperLogLog: The Analysis of a Near-Optimal Cardinality Estimation Algorithm](https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf), *AofA*, 2007.
2. Stefan Heule, Marc Nunkesser, and Alexander Hall, [HyperLogLog in Practice: Algorithmic Engineering of a State of the Art Cardinality Estimation Algorithm](https://research.google.com/pubs/archive/40671.pdf), *EDBT*, 2013.
3. Otmar Ertl, [New Cardinality Estimation Algorithms for HyperLogLog Sketches](https://arxiv.org/abs/1702.01284), 2017.
4. Otmar Ertl, [New Cardinality Estimation Methods for HyperLogLog Sketches](https://arxiv.org/abs/1706.07290), 2017.
5. Apache Software Foundation, [HyperLogLog Sketches Overview](https://datasketches.apache.org/docs/HLL/HllSketches.html), DataSketches documentation, accessed 2026-08-30.
6. Apache Software Foundation, [HLL Java 6.1.0 Package Contract](https://apache.github.io/datasketches-java/6.1.0/org/apache/datasketches/hll/package-summary.html), accessed 2026-08-30.
7. Seth Pettie and Dingyu Wang, [Simpler and Better Cardinality Estimators for HyperLogLog and PCSA](https://arxiv.org/abs/2208.10578), 2022.

## Exercises

### Exercise 1

For precisions (p=10,12,16), compute (m), approximate RSE, and raw bytes for one unpacked 6-bit register stored in each 8-bit byte. Explain which quantities exclude metadata.

### Exercise 2

Prove componentwise-max union is associative, commutative, and idempotent. Explain why these properties do not authorize merging sketches with different hash seeds.

### Exercise 3

A service reports a sudden 40% cardinality jump after a deployment. Precision and event volume are unchanged. Give a diagnosis plan covering semantic, representation, estimator, corruption, and statistical causes.

### Exercise 4

Design a compatible binary envelope and migration plan from a sparse HLL implementation using estimator A to a dense-capable implementation using estimator B. State when re-estimation, conversion, downsampling, or rebuild is allowed.

### Exercise 5

A privacy-sensitive analytics product needs daily distinct users, seven-day unions, and intersections between very similar cohorts. Propose a design, including where HLL fits, where it does not, and the verification evidence required.

## Answers to the Exercises

### Answer 1

At (p=10), (m=1024), RSE is (1.04/32=3.25\%), and byte-per-register storage is 1,024 bytes. At (p=12), (m=4096), RSE is (1.04/64=1.625\%), and storage is 4,096 bytes. At (p=16), (m=65{,}536), RSE is (1.04/256=0.40625\%), and storage is 65,536 bytes. These byte counts waste two bits per register and exclude object headers, alignment, sparse state, hash/estimator metadata, checksums, allocator overhead, and serialized framing.

### Answer 2

For each index (j), scalar maximum satisfies $\max(a,\max(b,c))=\max(\max(a,b),c)$, $\max(a,b)=\max(b,a)$, and $\max(a,a)=a$. Applying the identity independently at every register proves the three array laws. Different seeds map a key to different indices and ranks, so corresponding cells no longer summarize the same substream. The algebra still returns an array, but that array has no proved interpretation as the union. Compatibility is a premise of the operation, not a consequence of maximum.

### Answer 3

First compare exact sampled distinct counts under the old and new canonicalization: case folding, Unicode normalization, null treatment, tenant prefix, identifier field, and byte order. Inspect envelope hashes for seed, algorithm, precision, rank convention, estimator, sparse/dense, and generation changes. Validate all register ranks and checksums; identify a high-rank outlier or malformed union input. Recompute the new estimator from preserved logical registers and compare with the old estimator. Audit window bounds, late sources, and producer membership. Finally run repeated-seed simulations or historical backtests to judge whether the jump lies within ordinary estimator variation. Roll back or rebuild when the representation changed incompatibly; do not explain a deterministic schema change as “sketch noise.”

### Answer 4

The envelope carries magic/version, algorithm, estimator, precision, hash/seed, canonical schema, index/rank convention, representation mode, packed encoding, exception format, generation/scope, payload length, and checksum. First build a compatibility matrix. If B decodes A's sparse entries to exactly the same logical maxima and uses the same hash/rank semantics, conversion to B dense form is allowed and tested against direct construction. If only the estimator changes, preserve registers, recompute cached scalars, and label results B. Supported downsampling may fold high-precision registers according to a documented theorem; upsampling cannot invent missing partition detail. Any hash, seed, canonicalization, or rank change requires replay/rebuild from source identities. Dual writing and exact sampled comparison precede cutover; old readers remain until rollback expires.

### Answer 5

Use a separate compatible HLL per sealed day and cohort definition, with access-controlled envelopes, stable pseudonymous canonical IDs, generation fencing, and max-union for the seven-day set. Select precision from an explicit RSE and memory budget, use a maintained estimator, and compare exact protected samples across the expected cardinality range. HLL alone is a poor default for intersections of very similar large cohorts because inclusion-exclusion subtracts noisy estimates. Use a Theta/bottom-(k) family or a supported joint estimator with demonstrated interval coverage; exact computation may be required for consequential reports. Privacy controls include minimum cohorts, query auditing, release limits, and a formal privacy mechanism where the threat model requires it—hashing is not sufficient. Evidence includes deterministic union/serialization tests, multi-seed bias and coverage studies, intersection-specific validation, replay/window tests, corrupt-input and unauthorized-query tests, and versioned migration results.
