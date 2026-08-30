---
module_id: DSE-081
program: Data Structures Engineering
level: 2
module_number: 81
title: Bloom Filters
status: complete
last_verified: 2026-08-30
---

# Bloom Filters

## One-Page Review

### Governing question

How can a fixed-size randomized bit structure answer approximate set-membership queries with a controlled false-positive rate, zero false negatives under its contract, and evidence that distinguishes asymptotic design formulas from finite implementation behavior?

### Essential definitions

- A **Bloom filter** for a set S uses an m-bit array and k deterministic hash-derived positions per element.
- `insert(x)` sets all k positions for x; `query(x)` returns **maybe present** iff all are set and **definitely absent** otherwise.
- A **false positive** is `maybe` for `x not in S`; it is expected. A **false negative** for an inserted in-domain element is forbidden unless the contract explicitly permits deletion/decay or corruption.
- **Occupancy** is the fraction of one-bits. In the ideal balls-into-bins model, expected zero fraction after n insertions is approximately `exp(-kn/m)`.
- **Bits per distinct element** is `b=m/n`. Under the standard approximation, false-positive probability is `(1-exp(-k/b))^k`.
- The continuous approximate optimum is `k*=b ln 2`; the corresponding approximation is `(1/2)^(b ln 2)`, often written about `(0.6185)^b`.
- **Double hashing** derives positions `h1(x)+i*h2(x) mod m`; asymptotic results do not excuse weak, correlated, zero-cycle, or incompatible concrete hashes.
- A **blocked Bloom filter** confines probes to a cache-sized block, exchanging locality for a changed probability distribution.
- A **query distribution** may be fixed independently of construction or adaptively chosen after observing answers; guarantees differ.

### Central model, mechanism, or theorem

Assume kn independent uniform draws into m bits. A fixed bit remains zero with exact probability `(1-1/m)^(kn)`, approximated by `exp(-kn/m)`. Replacing random occupancy by its mean gives the familiar approximation

`p_approx=(1-exp(-kn/m))^k`.

This derivation is useful for sizing but is not the exact finite false-positive probability: queried positions can repeat, bit events are dependent, occupancy is random, and real hash derivation/layout adds correlations. Exact analyses condition on occupancy or use combinatorial distributions. Treat the formula as a model whose assumptions and error are checked for the operating range.

Solving the approximation for a target p at the optimal real k gives

`m ~= -n ln(p)/(ln 2)^2`, and `k ~= (m/n)ln2` before integer and implementation constraints.

No-false-negative reasoning is deterministic, not probabilistic: if insertion and query use identical positions and bits never clear or corrupt, every queried position for an inserted element is set. Probability enters only for absent elements. Ordinary Bloom filters do not support arbitrary deletion because clearing a shared bit can create false negatives.

### Critical invariants

1. Construction and queries use the same canonical bytes, policy identity, m, k, seeds, position derivation, and modulo/block layout.
2. Every distinct represented element has all of its positions set before publication; insertion is monotone and no ordinary deletion clears bits.
3. Bounds, allocation, serialization length, endian/bit order, checksum, version, and concurrent publication are validated.
4. “Definitely absent” is returned only for an intact, compatible filter in its declared domain; `maybe` requires an authoritative set lookup when exact membership is needed.
5. Sizing uses expected distinct cardinality and overload policy; duplicates do not consume the n assumed by the set model but skewed or adversarial inputs affect hashes.
6. Report configured/approximated, realized finite-query, and upper-confidence false-positive rates separately.
7. Benchmarks include hash CPU, memory/cache access, serialization, contention, and downstream work saved—not only bit probes.

### Common failures

- Calling `maybe` “present,” or treating false-negative bugs as part of the allowed error rate.
- Sizing for operations instead of distinct elements, then silently exceeding capacity.
- Rounding k to zero, using incompatible reader/writer seeds, or deriving a zero/short-cycle step under power-of-two m.
- Clearing bits for deletion without counters or another safe scheme.
- Using the approximate formula as an exact finite probability or service guarantee.
- Testing absent keys from a distribution that overlaps construction, leaks duplicates, or is unrepresentative/adaptively adversarial.
- Combining filters with different layouts/policies, or assuming bitwise intersection exactly represents set intersection.
- Optimizing p while random cache misses or hashes cost more than the downstream lookup saved.

### Compact example

A finite filter has m=128, n=16 inserted integers, and two visibly derived 64-bit mixed values for double-hash positions. The approximate optimum is `k≈5.545`, so the approximation chooses k=6. Exhaustively querying the fixed absent range `[16,10016)` finds the lowest realized count at k=4 (281/10,000) rather than k=6 (287/10,000). This does not refute the asymptotic optimum: the sample, finite layout, correlated double hashing, and deterministic query set are different from the ideal model.

### Connections

DSE-078 covers safe SSTable pruning, DSE-080 memory/read/write trade-offs, DSE-082 counting/scalable variants, and DSE-083 cuckoo/quotient alternatives. Probability and Statistics supplies concentration and confidence; Security supplies keyed hashing and adaptive-adversary analysis; Database/Data Engineering apply filters to joins, files, partitions, and distributed exchange.

## Governing Question

How do we derive, implement, and evaluate a Bloom filter so that its one-sided error contract remains exact while its probabilistic efficiency claims remain properly scoped?

## Why This Matters

Exact hash sets store keys or fingerprints and can be expensive when the only useful action is to reject most absent candidates. A Bloom filter stores superimposed evidence in a bit array: one zero is enough to prove absence, while all ones preserve ambiguity. That asymmetry makes it valuable before disk, network, decompression, join, cache, or remote-object work.

Its apparent simplicity hides three different correctness layers. The abstract data structure requires monotone insertion and consistent positions. The probabilistic model assumes a hash/query process. The deployed component requires safe encoding, publication, concurrency, compatibility, and fallback. A proof at one layer does not automatically establish the next.

Graduate-level treatment must also resist “formula laundering.” The standard false-positive expression is an approximation derived through occupancy assumptions. It is excellent for initial sizing in suitable regimes, but exact finite probability, realized workload rate, and tail/service risk are different quantities. A production decision combines derivation, finite recomputation, statistical measurement, and systems cost.

## Prerequisites and Retrieval

Retrieve:

- sets, exact membership, bit arrays, modular arithmetic, hash families, independence, and collision behavior;
- Bernoulli indicators, occupancy, expectation, conditioning, binomial confidence intervals, union bounds, and asymptotics;
- byte canonicalization, serialization, checksums, format versions, integer overflow, allocation bounds, and concurrency publication;
- cache lines, SIMD, branch behavior, memory bandwidth, CPU hashing, and downstream I/O/network cost;
- adversarial inputs, keyed hashing, chosen-query attacks, rate limiting, and data-distribution drift.

Diagnostic retrieval: an absent query can be a true negative or false positive. An inserted query must be positive under the ordinary intact contract. This is one-sided error, not an unreliable yes/no classifier.

## Learning Objectives

After this module, you can:

1. derive zero-bit occupancy, the standard false-positive approximation, optimal k, and target-bit sizing with assumptions;
2. distinguish exact finite probability, approximation, empirical rate, and confidence bound;
3. implement bounded monotone insertion/query with deterministic policy-compatible hash derivation;
4. prove no false negatives for inserted elements under stated invariants;
5. reason about duplicates, overload, empty filters, repeated positions, integer rounding, and saturation;
6. compare independent hashing, double hashing, partitioned/blocked layouts, and cache/CPU trade-offs;
7. design serialization, compatibility, concurrency, and corruption handling that fails safely;
8. validate probability and end-to-end value under representative and adversarial queries.

## Core Exposition

**Specify the abstract contract.** The filter represents a mathematical set S in a declared key domain. Inserting x is idempotent: setting already-set bits changes nothing. Query returns `absent` if any required bit is zero and `maybe` otherwise. It cannot enumerate S, recover keys, count multiplicity, or return exact membership. An exact caller follows `maybe` with an authoritative lookup.

**Prove the deterministic half first.** Let positions for x be `P(x)`. Insertion sets every bit in `P(x)`. Subsequent ordinary insertions only change zero to one. A later compatible query reads the same `P(x)`, so every bit is one and the result is maybe. No independence assumption is needed. A false negative therefore locates a violated premise: omitted insertion, bit clearing, race, corruption, incompatible policy, wrong domain, or querying before safe publication.

**Derive occupancy carefully.** One independent uniform probe misses a particular bit with probability `1-1/m`; kn probes leave it zero with `(1-1/m)^(kn)`, approaching `exp(-kn/m)`. Expected one fraction is its complement. For an absent query with k independent uniform positions, substituting expected occupancy yields `(1-exp(-kn/m))^k`. The substitution ignores dependencies and occupancy variance. State “standard approximation,” not “exact probability.”

**Optimize within the approximation.** Let `b=m/n`. Differentiating the logarithm of `(1-exp(-k/b))^k` over real k gives `k=b ln2`, where approximately half the bits are set. Implementations choose an integer, often compare floor/ceiling, and may cap k for CPU. Solving the optimum approximation gives `m=-n ln p/(ln2)^2`. Round m up to allocation/block constraints and choose k from the actual rounded m; never allow k<1.

**Model finite behavior.** The deterministic program builds eight filters for the same finite set and evaluates one fixed absent query range. A visible, fixed-width integer mixer supplies two values from which k positions are derived. Statistical independence, hash-family universality, and cryptographic strength are neither claimed nor required for the finite output.

<!-- bijux-verify: {"id":"finite-bloom-sizing-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bits=128\nmembers=16\nabsent_queries=10000\nbits_per_member=8.0\nideal_real_k=5.5452\napprox_best_k=6\nempirical_best_k=4\nk4_set_bits=52\nk4_false_positives=281\nk4_empirical_rate=0.0281\nall_members_positive=True\nempty_filter_negative=True\nordinary_deletion_supported=False\nvalid=True\nevidence=finite_bloom_sizing_model\n","stderr":""}} -->
```python
import math

bit_count = 128
members = tuple(range(16))
absent = tuple(range(16, 10016))
mask = (1 << 64) - 1


def mix64(value):
    value = (value + 0x9E3779B97F4A7C15) & mask
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & mask
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & mask
    return value ^ (value >> 31)


def positions(value, probe_count):
    first = mix64(value)
    step = mix64(value + 0xD1B54A32D192ED03) | 1
    return tuple((first + probe * step) % bit_count for probe in range(probe_count))


def build(probe_count):
    bits = 0
    for value in members:
        for position in positions(value, probe_count):
            bits |= 1 << position
    return bits


def maybe(bits, value, probe_count):
    return all(bits & (1 << position) for position in positions(value, probe_count))


results = []
for probe_count in range(1, 9):
    bits = build(probe_count)
    false_positives = sum(maybe(bits, value, probe_count) for value in absent)
    approximation = (1 - math.exp(-probe_count * len(members) / bit_count)) ** probe_count
    results.append((probe_count, bits, false_positives, approximation))

approx_best = min(results, key=lambda result: result[3])
empirical_best = min(results, key=lambda result: result[2])
k4 = results[3]
all_members_positive = all(maybe(k4[1], value, 4) for value in members)
empty_filter_negative = all(not maybe(0, value, 4) for value in members + absent[:10])
valid = approx_best[0] == 6 and empirical_best[0] == 4 and all_members_positive and empty_filter_negative
print(f"bits={bit_count}")
print(f"members={len(members)}")
print(f"absent_queries={len(absent)}")
print(f"bits_per_member={bit_count / len(members):.1f}")
print(f"ideal_real_k={bit_count / len(members) * math.log(2):.4f}")
print(f"approx_best_k={approx_best[0]}")
print(f"empirical_best_k={empirical_best[0]}")
print(f"k4_set_bits={k4[1].bit_count()}")
print(f"k4_false_positives={k4[2]}")
print(f"k4_empirical_rate={k4[2] / len(absent):.4f}")
print(f"all_members_positive={all_members_positive}")
print(f"empty_filter_negative={empty_filter_negative}")
print("ordinary_deletion_supported=False")
print(f"valid={valid}")
print("evidence=finite_bloom_sizing_model")
```

This uses only 16 integer members, 128 bits, double-hash-derived positions, k in 1…8, and a fixed contiguous set of 10,000 absent integers. It neither samples an ideal independent hash family nor estimates repeated-run uncertainty. The visible integer mixer is educational, unkeyed, and has no universality or adaptive-security claim. Python's arbitrary-precision integer is not a packed concurrent/serialized filter. The empirical winner is specific to these inputs and is not a tuning recommendation.

**Understand the finite gap.** Exact analysis can condition on J, the number of occupied bits: if a query makes k independent draws with replacement, its conditional positive probability is `(J/m)^k`; then average over J's occupancy distribution. Repeated query positions and hash construction change details. Papers have corrected overly casual interpretations of the classic approximation. In practice, compare mathematically appropriate finite calculations for small filters and empirical trials for the implemented hash/layout.

**Count distinct elements.** Repeated insertion of one key does not add new positions after the first time, so capacity depends on distinct represented elements. If only operation count is available, cardinality estimation uncertainty must become sizing headroom. Underestimating n raises occupancy and p. A fixed filter cannot expand while preserving exactly the same ordinary layout; rebuild, shard, or use a scalable variant studied in DSE-082.

**Handle empty and saturated states.** A correctly initialized all-zero nondegenerate filter returns absent for every query. An all-one filter returns maybe for every query and is correct but useless. Define n=0 sizing separately because bits-per-item and target formulas divide by n. Reject m=0, k=0, overflows, impossible allocations, and serialized lengths that do not match m.

**Choose hash derivation deliberately.** Computing k full hashes is often expensive. Double hashing uses `h1+i*h2`; asymptotic analysis supports it under premises, but concrete modulo arithmetic matters. For power-of-two m, an odd step visits the full residue cycle; repeated positions can still occur when k exceeds m. Domain-separate filters, version seeds and canonical encoding, and test low-entropy/adversarial key sets. A public fast hash may permit chosen collisions; keyed hashing can raise attack cost but creates secret rotation/distribution concerns.

**Trade locality against probability.** A classic filter scatters k probes across the bit array, potentially causing k cache misses. A blocked filter hashes first to a cache-line-sized block and places remaining probes within it. This improves locality and SIMD potential but creates per-block load variance and usually a different false-positive rate. Partitioned variants allocate one position per partition. Compare realized p, cache misses, instructions, branches, and memory bandwidth rather than reusing the classic formula unchanged.

**Represent bits portably.** Specify bit numbering within bytes, byte order for integer metadata, m, k, hash/policy ID, seed/key identifier, item-count estimate, format version, and checksum/authentication as required. Validate lengths and arithmetic before allocation or probing. Mask unused tail bits consistently. Golden vectors should pin canonical input bytes, positions, encoded bytes, and query results across languages and releases.

**Publish concurrency safely.** Atomic bitwise OR can support concurrent insertion only if memory ordering, word tearing, and query visibility are defined. A query racing an incomplete insertion can observe some zero positions and return a transient false negative. Options include build-then-immutably-publish, synchronize queries with insertion completion, or specify weaker concurrent semantics. Snapshotting mutable bits must not lose concurrent sets; copying and publication need a consistent protocol.

**Do not delete ordinary bits.** Different elements share positions. Clearing all positions for removed x can clear the only evidence for retained y, creating a false negative. Rebuilding from authoritative members is safe. Counting Bloom filters replace bits with counters and require overflow/underflow correctness; stable/decaying filters intentionally allow forgetting and therefore change the guarantee. These belong to DSE-082.

**Combine only compatible filters.** Bitwise OR of equal-policy/equal-layout filters represents the union without false negatives for either input, though p rises with occupancy. Bitwise AND has no general exact set-intersection semantics: bits shared by unrelated elements survive, and elements in the true intersection remain positive, but the result can have false positives unrelated to a freshly built intersection. Mismatched m, k, seeds, encoding, or domain cannot be combined.

**Measure statistical evidence.** For a fixed filter, query absent keys independently drawn from a declared distribution and count X false positives among q eligible queries. Report `X/q` and a binomial interval such as Wilson, not only a configured p. Multiple filters, time windows, adaptive tuning, or selected best runs require multiple-comparison care. Hash seeds and input/query generators are part of reproducibility. Exhaustive finite universes can avoid sampling error but remain universe-specific.

**Consider adaptive adversaries.** Once an absent key produces maybe for a fixed immutable filter, repeated queries remain positive; errors are deterministic conditional on the built state. An attacker can search for and replay false positives, so an average rate under fresh random queries may not bound operational load. Use keyed/rotated hashing where justified, authoritative negative caching, rate limits, quotas, rebuilds, and designs with explicit adaptive guarantees. Never use a Bloom positive as authorization or proof of identity.

**Optimize end-to-end saved work.** Approximate memory is worthwhile when valid negatives avoid more cost than hash/probe/cache overhead. Let q be eligible negative queries, p realized false-positive rate, `C_filter` filter cost, and `C_authoritative` avoided lookup cost. A rough expected cost is `q*C_filter + q*p*C_authoritative`, compared with `q*C_authoritative` without the filter. Positive queries, cache state, construction/rebuild, memory displacement, and tail effects require fuller measurement.

**Test properties and failure paths.** Generate random sets and assert every inserted item is maybe; compare absent outcomes with an exact set. Test duplicate insertion, m/k boundaries, repeated positions, empty/all-one filters, overload, low-entropy keys, canonical encodings, hash/seed drift, corrupt/truncated bytes, tail bits, cross-language golden vectors, concurrent publication, and rebuild. Measure p across seeds/distributions and benchmark downstream work with and without the filter.

## Definitions and Notation

Let universe U contain represented set S with `n=|S|`; m is allocated bits; k is probe count; `b=m/n` for n>0; `P(x)` is the ordered/multiset probe sequence; J is occupied-bit count; and `rho=J/m`. A false positive occurs for `x in U\S` when every position in `P(x)` is one.

`p_approx(m,n,k)=(1-exp(-kn/m))^k` is the standard approximation. `p_emp=X/q` is the realized rate for q declared eligible absent queries. These are not interchangeable with a confidence upper bound, a per-filter worst case, or an adaptive-adversary guarantee.

## Mechanisms, Invariants, or Proof Structure

### No-false-negative proof

1. Fix canonical encoding, filter identity, m, k, and deterministic `P` for construction and query.
2. Insert every x in S by setting each position in `P(x)`.
3. Permit only monotone zero-to-one changes before immutable publication; prevent partial visibility.
4. Preserve bits and policy exactly through storage/transport.
5. Query x using the identical `P(x)`; every inspected bit was set and not cleared.
6. Therefore x returns maybe; any observed negative falsifies a premise rather than arising probabilistically.

### Sizing derivation review

1. State independent uniform probe and absent-query assumptions.
2. Derive exact per-bit zero probability `(1-1/m)^(kn)` and exponential approximation.
3. Identify the additional occupancy/independence approximation used for `(1-exp(-kn/m))^k`.
4. Optimize the approximate expression over real k, then evaluate allowed integer/layout choices.
5. Round m upward, recalculate k, and include expected-cardinality uncertainty/headroom.
6. Compare finite analysis and implemented empirical results; label deviations rather than hiding them.

### Evidence proof

1. Pin implementation, policy, generator, seeds, construction set, absent-query distribution, q, and hardware.
2. Exhaustively verify all inserted distinct elements are positive.
3. Compare queries against an exact set and count eligible true negatives/false positives.
4. Report occupancy, approximation, empirical rate, interval, hash/cache/CPU cost, and downstream work.
5. Repeat across load factors, seeds, distributions, layouts, and adversarial searches.
6. Gate publication on compatibility/corruption/concurrency tests and retain safe fallback/rebuild.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or changed premise | Evidence needed |
|---|---|---|---|
| k independent hashes | closest to textbook abstraction | hash CPU/randomness and scattered probes | hash independence quality, CPU/cache, finite p |
| Double hashing | two base hashes derive many probes | correlations and modulo/step edge cases | golden positions, cycles, distributions, finite p |
| Blocked/cache-line Bloom | one/few cache-line touches | load imbalance and different p | block occupancy tails, cache misses, SIMD/CPU |
| Partitioned Bloom | structured one-probe-per-partition | layout/rounding constraints | partition load, encoding, finite p |
| Exact hash/fingerprint set | exact or controllable fingerprint collision | stores more information; resizing/lookup cost | memory, collision contract, tails |
| Cuckoo/quotient filter | deletion/enumeration/locality options | relocation/load/failure/metadata complexity | build failure, p, concurrency, resize |
| Counting/scalable Bloom | deletion or growth | counters/multiple filters and changed error budget | overflow, underflow, composition, rebuild |

For very small n, headers, alignment, minimum allocation, and exact fingerprints may dominate. For extremely low target p, k and memory grow; a fingerprint table or layered verification may be faster. For ranges, nearest-neighbor, frequency, multiplicity, or enumeration, Bloom membership is the wrong query abstraction.

## Failure Modes and Misconceptions

**“Bloom filters sometimes say absent for members.”** Not ordinary intact filters. False negatives indicate a contract or implementation violation.

**“The formula is exact.”** The common exponential expression is an approximation with independence/occupancy substitutions; finite and concrete hashing behavior differs.

**“Optimal k is always round(b ln2).”** It is optimal for a specific approximate false-positive objective. CPU, locality, integer/layout constraints, and realized finite p can choose differently.

**“n is insertion calls.”** It is distinct represented cardinality in the set model. Duplicates are idempotent.

**“A positive proves membership.”** It proves only that the filter cannot reject. Consult the authoritative set.

**“A cryptographic digest makes the filter secure.”** Public deterministic filters can still be searched and replayed; security needs a threat model, secret management, and adaptive evidence.

**“Clearing k bits deletes one key.”** Shared bits make this unsafe and can create false negatives for other keys.

**“OR and AND implement exact union and intersection.”** Compatible OR preserves union membership with increased p. AND is not equivalent to rebuilding the exact intersection.

**“One empirical rate validates p.”** It validates one built filter and query set. Report uncertainty and variation across seeds/distributions/load.

**“A lower p always improves the system.”** Extra bits/hashes/cache misses can cost more than the authoritative work avoided.

**“Hash modulo is trivial.”** Bias, overflow, signedness, endian encoding, zero/short cycles, and cross-language behavior can change positions.

**“Concurrent atomic OR guarantees readers never miss.”** Readers can observe a partially inserted element unless completion/publication ordering is specified.

## Worked Examples

### Example 1

For m=10,000, n=1,000, and k=7, `b=10`; the approximation is `(1-exp(-0.7))^7≈0.008194`. This is about 0.819%, not a per-filter guarantee. The ideal real k is `10 ln2≈6.931`, making integer 7 a natural candidate.

### Example 2

For n=5,000 and target `p=0.01`, approximate optimal bits are `-5000 ln(0.01)/(ln2)^2≈47,925.3`, rounded up before alignment. Bits per item are about 9.585; real k is about 6.644, so compare allowed integers 6 and 7 after actual m rounding.

### Example 3

One bit remains zero after kn independent draws with `(1-1/m)^(kn)`. At m=128,n=16,k=4 this is `(127/128)^64≈0.6053`; the exponential approximation is `exp(-0.5)≈0.6065`. Close per-bit expectation does not make the complete query probability exact.

### Example 4

Insert x with positions `{2,9,14}` and y with `{9,18,27}`. Clearing x's positions deletes bit 9 even though y needs it. A later y query becomes negative. Rebuilding or a correctly sized counting variant is required for deletion.

### Example 5

A filter sized for 1 million distinct keys receives 2 million. At fixed m and approximately optimal original k, occupancy rises and p can increase dramatically. Reject insertion, rebuild/shard, or use a growth-capable contract; silently accepting overload violates the promised performance envelope, though no-false-negative membership can remain.

### Example 6

With m=64 and double-hash step 16, positions repeat after four increments because `gcd(16,64)=16`. Eight requested probes cover at most four bits. For power-of-two m, forcing an odd step makes the step coprime to m, but repeated positions still occur if k>m and other correlations remain.

### Example 7

Two compatible filters A and B use identical m/k/policy. `bits(A) OR bits(B)` keeps every position for every member of either set, so it has no false negatives for the union. Its occupancy and false positives can exceed each input. Combining different seeds has no such meaning.

### Example 8

Observe X=100 false positives in q=10,000 eligible absent queries: point estimate 1%. A rough normal standard error is `sqrt(0.01*0.99/10000)≈0.000995`; a rough 95% interval is about 0.805%–1.195%, though Wilson is preferred near boundaries. One sample cannot certify a strict 1% maximum.

### Example 9

A filter costs 80 ns and has p=1%; the avoided authoritative lookup costs 100 microseconds. Expected negative-path cost is roughly `0.08 + 0.01*100=1.08 microseconds`, versus 100 without filtering. If the authoritative lookup is a 50 ns cache hit, the same filter is counterproductive.

### Example 10

An attacker discovers 500 absent keys that are false positives and replays them. The observed rate on those requests becomes 100%, despite a 1% fresh-random-query rate. Rate limiting, secret-keyed rotation, authoritative negative caching, or an adaptively robust design is needed; average p is not a security control.

## Cross-Program Connections

- **Probability and Statistics:** occupancy, conditioning, asymptotics, binomial intervals, multiple testing, and sampling design govern claims.
- **Algorithms:** hashing, approximate membership lower bounds, cache-aware layout, and dynamic variants define the design space.
- **Database Engineering:** filters prune pages/files/joins but require authoritative lookup, format compatibility, and corruption-safe fallback.
- **Data Engineering:** partition/file filters, distributed joins, shuffle reduction, and object-store requests turn p into network/I/O economics.
- **Security Engineering:** adversarial keys, replayed false positives, keyed hashing, secret rotation, and denial-of-service limits alter guarantees.
- **Concurrent and Parallel Programming:** atomic bit sets, visibility, immutable publication, snapshots, and SIMD probing determine runtime correctness.
- **Performance Engineering:** hash throughput, cache lines, memory bandwidth, downstream costs, and representative workload experiments determine value.

## References

1. Burton H. Bloom, [Space/Time Trade-offs in Hash Coding with Allowable Errors](https://www.cs.princeton.edu/courses/archive/spr05/cos598E/bib/p422-bloom.pdf), *Communications of the ACM* 13(7), 1970.
2. Adam Kirsch and Michael Mitzenmacher, [Less Hashing, Same Performance: Building a Better Bloom Filter](https://www.eecs.harvard.edu/~michaelm/postscripts/rsa2008.pdf), *Random Structures & Algorithms* 33, 2008.
3. Felix Putze, Peter Sanders, and Johannes Singler, [Cache-, Hash- and Space-Efficient Bloom Filters](https://ae.iti.kit.edu/english/1268.php), *Journal of Experimental Algorithmics* 14, 2010.
4. Prosenjit Bose et al., [On the False-Positive Rate of Bloom Filters](https://doi.org/10.1016/j.ipl.2008.05.018), *Information Processing Letters* 108(4), 2008.
5. Ken Christensen, Allen Roginsky, and Miguel Jimeno, [A New Analysis of the False-Positive Rate of a Bloom Filter](https://www.nist.gov/publications/new-analysis-false-positive-rate-bloom-filter), NIST publication record, 2010.
6. Alexander Broder and Michael Mitzenmacher, [Network Applications of Bloom Filters: A Survey](https://www.eecs.harvard.edu/~michaelm/postscripts/im2005b.pdf), *Internet Mathematics* 1(4), 2004.
7. Moni Naor and Eylon Yogev, [Bloom Filters in Adversarial Environments](https://eprint.iacr.org/2015/113.pdf), IACR Cryptology ePrint, 2015.
## Exercises

### Exercise 1

For n=2,000 and target p=0.001, compute approximate optimal m, bits per item, and real k. Round m up to a multiple of 64 and compare the approximation for the two nearest positive integer k values. State every assumption.

### Exercise 2

Prove the ordinary no-false-negative property, then identify one concrete counterexample for each violated premise: incomplete insertion, clearing a shared bit, incompatible seed, and query racing publication.

### Exercise 3

Design a finite evaluation that distinguishes the standard approximation from realized p. Specify construction cardinalities, m/k sweep, hash policies/seeds, absent-query distributions, exact-set oracle, repetitions, confidence intervals, and adaptive-query test.

### Exercise 4

Two compatible filters each have m=32,k=3. A represents `{a,b}` and B `{b,c}`. Explain what bitwise OR and AND guarantee about union/intersection membership and false positives. Explain what changes if B uses another seed.

### Exercise 5

Design a production readiness gate for a serialized concurrently built Bloom filter. Cover bounds, canonical bytes, hash derivation, golden vectors, no-false-negative properties, corruption, compatibility, concurrency visibility, overload, performance, observability, and fallback.

## Answers to the Exercises

### Answer 1

`m≈-2000 ln(0.001)/(ln2)^2≈28,755.2` bits, or about 14.378 bits/item before alignment. Rounding to the next 64-bit multiple gives m=28,800 and b=14.4. Real `k=b ln2≈9.981`, so compare k=9 and 10: `(1-exp(-9/14.4))^9≈0.001011` and `(1-exp(-10/14.4))^10≈0.000989`. This assumes distinct elements, independent uniform probes, absent queries independent of construction, the standard occupancy approximation, fixed capacity, and no layout/hash/cache constraint; exact finite and empirical results remain required.

### Answer 2

For x inserted completely, every bit in deterministic compatible `P(x)` is set; monotone later insertions do not clear them, so query sees all ones. Counterexamples: a builder crashes after setting only the first of three positions; deleting y clears a bit shared with x; a reader's new seed computes positions different from the writer's; or a reader observes a mutable filter after the first atomic OR but before insertion completion. Each creates a negative through a violated deterministic premise, not probabilistic false-negative allowance.

### Answer 3

Choose small-to-large n and load factors, aligned m values, and k around/beyond `b ln2`. For independent/full, double-hash, and blocked policies, pin implementation and many recorded seeds. Build from exact distinct sets drawn from uniform, skewed, structured, and low-entropy distributions. Query disjoint absent sets from matching, shifted, adversarial, and exhaustive finite domains; compare every answer with an exact set and first assert all members positive. Record occupancy, repeated positions, X/q with Wilson intervals, per-filter/seed distribution, approximation and finite calculation where tractable. Add a search-then-replay adaptive test, plus hash/cache/CPU and downstream savings.

### Answer 4

Compatible OR retains every set bit from A and B, so all members of `{a,b,c}` remain positive; increased occupancy can raise false positives. Compatible AND retains every position of b because b's identical positions occur in both, so it has no false negative for the true intersection member. Bits independently contributed by a and c can coincide and create positives not present in a freshly built `{b}` filter; AND is not an exact intersection representation. With another seed, b has different positions, so AND can clear required bits and OR cannot be queried meaningfully under one policy; do not combine them.

### Answer 5

Gate checked m/k/length/allocation arithmetic, tail-bit rules, version/policy/seed/key ID/checksum, and canonical cross-language bytes. Pin golden position/encoding vectors and property-test every inserted member, duplicates, empty/saturated/overloaded states, repeated probes, and exact-set absent results across seeds. Mutate/truncate headers/bits/checksums and require authoritative fallback or explicit corruption, never absence. Prove build-then-publish or insertion-completion memory ordering under races and snapshots. Test rolling compatibility and rebuild. Benchmark hashes, cache, contention, memory, construction, query classes, downstream work, tails, and adversarial replay. Emit occupancy, estimated distinct n, configured/empirical p, incompatibility/corruption/fallback, and capacity alarms with safe bypass.
