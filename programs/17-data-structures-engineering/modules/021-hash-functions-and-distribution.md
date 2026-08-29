---
module_id: DSE-021
program: Data Structures Engineering
level: 1
module_number: 21
title: Hash Functions and Distribution
status: complete
last_verified: 2026-08-29
---

# Hash Functions and Distribution

## One-Page Review

### Governing question

What equality contract, key encoding, hash family, seed policy, bucket reduction, workload model, threat model, and evidence make hash-based indexing dependable rather than merely fast on friendly examples?

### Essential definitions

- A **hash function** maps a key domain K to a finite integer range; table code then maps that value to buckets/probe choices.
- A **collision** occurs when distinct non-equivalent keys receive the same hash or bucket.
- **distribution** describes bucket loads for a specified key set and mapping, not a property proved by a few outputs.
- **load factor** is stored entries divided by available buckets/slots under the table representation.
- A **hash family** is a set of functions from which one function may be selected by a seed.
- A family is **universal** when every distinct key pair collides with probability at most `1/m` over a random family choice into m outputs (under the stated definition).
- **keyed hashing** makes outputs depend on a secret key/seed; **stable hashing** promises reproducible outputs under a versioned specification.
- **hash flooding** is adversarial collision concentration that drives a table toward worst-case work.
- **avalanche/mixing** concerns how input-bit changes affect output bits; it is not by itself a collision-security proof.
- **canonical encoding** is an unambiguous byte representation of a structured key, including type, boundaries, and normalization policy.

### Central model, mechanism, or theorem

For n distinct keys mapped independently and uniformly to m buckets, expected bucket load is `n/m`. For each unordered key pair define indicator `Iij=1` when the pair collides. Then

\[
E[C]=E\left[\sum_{i<j} I_{ij}\right]
=\sum_{i<j}P(h(x_i)=h(x_j))
=\binom{n}{2}\frac1m.
\]

This is an expectation under a model, not a guarantee for a fixed public function or adversarial keys. A universal family restores a per-pair expected bound by selecting h randomly after the key set is fixed. Table operation cost still depends on its collision-resolution scheme, load policy, and independence assumptions.

### Critical invariants

1. If equality says `x≈y`, their hash values are equal for the entire membership lifetime.
2. Key state participating in equality/hash does not mutate while indexed, unless removal/reinsertion is performed safely.
3. Structured keys have one unambiguous, versioned encoding with checked lengths and domains.
4. Full hash computation and bucket reduction are distinguished; power-of-two tables require useful low-bit distribution.
5. Seed scope matches the goal: random/secret for adversarial in-memory tables, stable/versioned for persisted identities or partitioning.
6. Collision handling remains correct for all collisions; distribution affects cost, not semantic equality.
7. Resizing/rehashing recomputes placement under the correct function/seed and observes failure/invalidation contracts.
8. Security, reproducibility, statistical quality, and speed claims use separate evidence.

### Common failures

- Requiring unequal keys to have unequal hashes—impossible when a large domain maps to a finite range.
- Hashing fields inconsistent with equality, or mutating a key after insertion.
- Concatenating variable fields without length/type framing so `(ab,c)` and `(a,bc)` encode alike.
- Calling `hash % m` “uniform” without specifying the hash-output distribution and modulo bias.
- Masking low bits from a hash whose entropy resides mainly in high bits.
- Using a language's randomized process hash for durable files, caches, partitions, or signatures.
- Using a fast unkeyed mixer against attacker-chosen keys, or a table hash as a password/MAC/content-integrity primitive.
- Treating chi-square, avalanche, or SMHasher-like tests as proof of universality or cryptographic strength.
- Benchmarking only successful integer lookups and ignoring hashing bytes, equality checks, collisions, misses, resize, memory, and hostile inputs.

### Compact example

Mapping all 256 byte values by `h mod 10` produces six buckets of 26 and four of 25: small deterministic modulo bias because 10 does not divide 256. Separately, hashes `0,16,...,240` masked into 16 buckets all land in bucket zero; a finite xor-folding transformation spreads that particular set across all 16. The trace proves these inputs only, not general mixer quality.

### Connections

[DSE-003](003-operation-contracts.md) supplies equality/mutation contracts; [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md) supply evidence discipline. The [program roadmap](../ROADMAP.md) next applies these foundations to separate chaining and linear probing.

## Governing Question

How should keys be defined, encoded, mixed, seeded, reduced, attacked, tested, and measured so that a hash table's correctness and expected performance claims match its actual environment?

## Why This Matters

Hash tables power symbol tables, caches, indexes, deduplication, routing, interning, sets, and counters. Their appealing expected constant-time operations rely on a pipeline: equality chooses equivalence classes; an encoder exposes key information; a hash maps it to a finite value; reduction/probing maps into storage; collision resolution preserves semantics; resizing controls load.

A defect at any layer can be catastrophic. Equality/hash disagreement makes present keys unreachable. Weak low bits collapse a power-of-two table. Predictable collisions turn small requests into large CPU work. Process-randomized hashes make persisted artifacts nondeterministic. A cryptographic digest may be secure yet unnecessarily expensive for a trusted in-memory table, while a fast table mixer may be wholly unsuitable for authentication.

“Good hash” has no context-free meaning. The correct choice depends on key structure, table algorithm, output width, seed lifecycle, attacker capability, reproducibility, runtime contract, hardware, and cost of hashing versus comparing/probing. This module builds that decision model before later modules implement collision strategies.

## Prerequisites and Retrieval

Retrieve abstraction/equality/operation invariants from [DSE-001](001-abstract-data-types-and-concrete-representations.md), [DSE-002](002-representation-invariants.md), and [DSE-003](003-operation-contracts.md); cost and locality models from [DSE-004](004-time-space-and-allocation-cost.md), [DSE-005](005-contiguous-and-linked-layouts.md), and [DSE-006](006-memory-locality-and-cache-behavior.md); genericity and traversal contracts from [DSE-007](007-genericity-and-type-constraints.md) and [DSE-008](008-iterators-and-traversal-protocols.md); and adversarial testing/measurement from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. derive the equality–hash coherence contract and mutation restriction;
2. distinguish full hash, fingerprint, bucket index, and probe sequence;
3. calculate expected loads/colliding pairs under explicit randomness assumptions;
4. explain universal hashing and why family selection matters against fixed inputs;
5. construct unambiguous canonical encodings for composite keys;
6. analyze modulo, masking, low-bit, width, and resize effects;
7. choose random, secret, deterministic, or versioned seeds for the actual lifecycle;
8. separate table hashing, content digests, MACs, password hashing, and sharding;
9. design distribution/collision/security tests without overstating statistical evidence;
10. benchmark full lookup/update workloads across realistic and adversarial keys.

## Core Exposition

**Equality comes first.** A map stores one value per equivalence class under its key predicate. The predicate must be reflexive, symmetric, transitive, and stable while the key is indexed. The hash contract is one-way:

\[
x\approx y\Longrightarrow h(x)=h(y).
\]

Equal hashes do not imply equal keys. Collision resolution must invoke equality before claiming a match. The ISO C++ unordered-container requirements explicitly require equivalent keys to hash identically; Python and Java express analogous contracts in their data models.

If equality ignores case, normalization, tenant-excluded fields, or representation differences, hashing must ignore/normalize identically. For a user record equal by `(tenant,id)`, including mutable display name in the hash violates coherence. Conversely, omitting many equality fields is correct but may increase collisions.

Mutating an indexed key can strand it in the bucket selected by its old hash. Libraries restrict key mutation directly or rely on programmers to preserve the invariant. Safe changes remove under the old identity, mutate, then reinsert, while handling aliases and failure.

**Hashing is a pipeline.** A logical key becomes canonical bytes/words, a core hash produces w bits, optional finalization/mixing spreads information, and a table maps the result to a bucket or probe sequence. Cached fingerprints can reject nonmatches before expensive equality but are not identities. Debug each stage separately.

Composite encodings need domain separation. Raw concatenation makes `(b"ab",b"c")` indistinguishable from `(b"a",b"bc")`. Use type tags plus fixed-width or varint lengths with checked arithmetic, or a streaming hasher API whose `Hash` contract frames values unambiguously. Specify integer width/endian, signed representation, floating-point NaN/zero equality, strings/bytes distinction, Unicode normalization, absent/null, collection order, and schema version.

Never serialize pointers, padding, uninitialized bytes, locale formatting, or process-private object hashes as durable key material. Stable hashing begins with stable canonical bytes; a stable algorithm cannot repair an ambiguous encoding.

**Uniform hashing is a model.** Suppose each distinct key independently chooses one of m buckets uniformly. A named bucket has binomial load with mean n/m. Linearity of expectation gives expected colliding pairs `n(n-1)/(2m)`. It does not require indicator independence for the mean, though tail bounds and probe analyses may require stronger independence.

The pigeonhole principle guarantees a collision whenever more than m distinct keys map into m outputs. A 64-bit output reduces accidental pair-collision probability for ordinary n but cannot eliminate collisions, and birthday effects appear far below `2^64` keys. Table correctness must not depend on uniqueness.

A fixed public function can look uniform on one corpus yet have structured collisions on another. “Simple uniform hashing” is an analysis assumption, not a postcondition of multiplying by a constant. Report whether randomness is over inputs, a randomly chosen function, seed generation, or experiments.

**Universal hashing randomizes the function.** For a family H mapping K to m values, a common universal condition is that for every distinct x,y, choosing h uniformly from H yields collision probability at most 1/m. Carter and Wegman's primary work uses randomized family choice to obtain input-independent expected storage/retrieval behavior.

The adversary model matters. If the key set is fixed without seeing the random selection, the per-pair bound controls expected collisions. If an attacker learns the seed/function through disclosure or adaptive timing queries, that analysis may no longer apply. Pairwise independence, strong universality, k-independence, and almost-universality are distinct definitions; cite the exact one a proof needs.

A seed is not decorative randomness. It selects a function or perturbs state under a defined family. Low-entropy, reused, exposed, or attacker-chosen seeds may not provide the expected protection. Seed creation and fork/snapshot/clone behavior are operational concerns.

**Bucket reduction can discard quality.** `b=h mod m` is exact uniform only if h is uniform over a range evenly divisible by m, or a rejection/range-reduction method removes bias. With w-bit uniform h and arbitrary m, modulo bucket counts differ by at most one across all `2^w` outputs, but relative bias can matter in some sampling applications. A hash table usually cares more about structured keys and collision strategy than tiny full-range modulo bias; measure and model rather than chanting a rule.

For m a power of two, `h & (m-1)` uses low bits. If the hash fails to mix varying key information into low bits, occupancy collapses. Prime capacities do not magically repair a weak or adversarial hash; they only change which patterns survive modulo. Some tables use multiplicative high-bit range reduction. Use the table's actual mapping.

Resizing changes m and often bucket/probe positions. A table may reuse cached full hashes but must recompute reduction; changing the seed/function requires rehashing keys. Failure must leave a coherent old table or complete migration. Incremental rehashing has two-table lookup/state rules developed later.

**Distribution quality has layers.** Diffusion/avalanche tests ask whether input-bit changes influence output bits. Bias tests inspect marginal output bits/buckets. Differential and collision tests target structured relationships. Corpus histograms reveal workload interactions. These can find defects but cannot prove security or universal-family bounds.

Chi-square tests assume a sampling model and yield a statistic/p-value, not a certificate that outputs are independent uniform. Multiple testing produces false discoveries; tiny samples lack power; huge samples flag irrelevant deviations. Preserve seeds, key generators, expected counts, significance policy, and failing inputs. Add causal mutants such as dropping a field or low bits to prove the suite notices relevant flaws.

Legacy material's “good versus pathological” buckets are useful demonstrations, but labels such as perfect distribution, fixed machine timings, or broad claims about current runtime algorithms are not durable evidence. Current CPython and Rust behavior must be tied to current official documentation; implementations may change.

**Threat model chooses keyed versus public hashing.** Crosby and Wallach demonstrated algorithmic-complexity denial of service using attacker-induced collisions. A service parsing attacker-chosen names into a hash table should assume hostile structure and bounded request cost. Defenses include a secret randomized/keyed table hash, alternative collision structures with worst-case bounds, input/resource limits, monitoring, and architecture-specific fallbacks.

SipHash was designed as a fast short-input pseudorandom function and motivated partly by hash flooding. CPython's PEP 456 introduced SipHash-family support for string/bytes hashing, while current Python documentation states those hashes are salted unpredictably and vary across runs. Rust's current `HashMap` documentation describes randomly seeded HashDoS resistance and warns the default algorithm is subject to change. Cite contracts, not folklore such as one eternal round count.

Secret-key table hashing is not automatically a general MAC API: output width, domain, forgery policy, key handling, side channels, and protocol framing differ. Likewise SHA-2/SHA-3/BLAKE content digests target cryptographic properties beyond bucket distribution and may be unnecessary on a trusted hot path. Password hashing deliberately uses salt and expensive memory/time. Consistent hashing/partitioning optimizes movement and balance across nodes and requires reproducible cross-process algorithms. These are different tools.

**Stable and randomized hashes solve conflicting problems.** A process-random seed frustrates precomputed collisions and intentionally changes iteration/layout. A persistent on-disk index, content-address, cache key, test vector, or distributed partition needs deterministic, versioned results. Do not persist `hash(key)` from a runtime that reserves the right to change algorithms or seeds.

If stability is required, define `algorithm-id`, output width, canonical encoding version, seed/key (public if distribution only), byte order, and upgrade/migration. Changing any can relocate every record. For sharding, evaluate weighted/skewed keys and node churn; uniform buckets in one process do not prove balanced load when key frequencies differ.

**Cost includes key work.** Hashing a 10-kilobyte string is not O(1) in key length. A lookup cost model includes canonicalization, hash computation/caching, bucket/probe accesses, metadata scans, equality comparisons, cache misses, allocation, resize, locks, and reclamation. Caching hashes trades memory/invalidation for fewer recomputations.

Benchmark hits and misses, key lengths/types, repeated/fresh hashes, load factors, table sizes, collisions, resize boundaries, successful/failed inserts, deletes/tombstones, iteration, and adversarial cases. Record throughput and latency distributions, CPU profiles, comparisons/probes, cache misses, bytes hashed, allocations, memory, and seed/toolchain/hardware. Change one factor at a time: replacing a hash while also changing key encoding and table layout destroys attribution.

**Verification joins algebra and adversaries.** Property tests generate equal-but-differently-represented keys and require equal hashes, plus arbitrary collisions whose equality resolution remains correct. Mutation tests drop each equality field from hashing, change normalization, omit length framing, truncate bits, or force constant hashes. The table must remain semantically correct under constant hash even if slow.

Distribution tests use named corpora: sequential integers, aligned addresses, prefixes/suffixes, Unicode, composite fields, real traces, and generated/adversarial patterns. Analyze full hashes and actual buckets at every relevant capacity. Security review checks seed source/scope, disclosure/adaptation, input limits, worst-case behavior, and operational detection. Cryptographic selection requires specialist review and published primitives rather than home-designed mixing.

The executable trace below demonstrates two finite bucket-mapping phenomena; it does not endorse xor-folding as a general hash.

<!-- bijux-verify: {"id":"finite-bucket-mapping-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"modulo_counts=26,26,26,26,26,26,25,25,25,25\nmodulo_spread=1\nmasked_bad_max_load=16\nmasked_mixed_max_load=1\nmasked_mixed_nonempty=16\nevidence=finite_bucket_mapping_trace\n","stderr":""}} -->
```python
def bucket_counts(values, bucket_count):
    counts = [0] * bucket_count
    for value in values:
        counts[value % bucket_count] += 1
    return counts


modulo = bucket_counts(range(256), 10)
aligned = [value << 4 for value in range(16)]
bad = bucket_counts(aligned, 16)
mixed = bucket_counts([value ^ (value >> 4) for value in aligned], 16)
print("modulo_counts=" + ",".join(map(str, modulo)))
print(f"modulo_spread={max(modulo) - min(modulo)}")
print(f"masked_bad_max_load={max(bad)}")
print(f"masked_mixed_max_load={max(mixed)}")
print(f"masked_mixed_nonempty={sum(count > 0 for count in mixed)}")
print("evidence=finite_bucket_mapping_trace")
```

## Definitions and Notation

- `K`: logical key domain partitioned by equality relation `≈`.
- `h:K→{0,...,2^w-1}`: w-bit hash function under a named encoding/seed.
- `m`: current bucket/slot count; `b(h,m)` is the table's reduction.
- `n`: number of stored distinct equivalence classes; `α=n/m` is nominal load factor.
- **collision**: distinct non-equivalent x,y with equal full hash or bucket, as explicitly named.
- **preimage/collision resistance**: cryptographic properties, not synonyms for statistical spread.
- **seed/key**: parameter selecting/configuring a function; secrecy and reproducibility are separate policies.
- **fingerprint/tag**: stored subset/derivation of hash bits used to filter candidates, never equality proof.
- **HashDoS**: resource-exhaustion attack through pathological table behavior.
- **canonical encoding**: versioned injective representation over the key equivalence classes intended by the application.

## Mechanisms, Invariants, or Proof Structure

Correctness begins with equivalence/hash coherence and stable indexed state. Prove operations always compare equivalent candidates after bucket/probe filtering and do not use hash equality as key equality. A constant hash is a semantic stress oracle.

Expected-distribution reasoning defines indicators for bucket loads or colliding pairs, states where probability resides, and applies linearity. Universal-family proofs quantify over every fixed distinct pair and randomness over chosen h. Tail/probe claims require their additional independence/table premises.

Encoding proof shows two non-equivalent structured keys cannot produce the same encoded byte sequence merely from field-boundary/type ambiguity. Hash collisions remain possible after encoding. Security proof then names adversary knowledge/adaptation, seed entropy/lifecycle, resource bounds, and collision-resolution worst case.

## Alternatives and Trade-Offs

| Choice | Strength | Cost/risk |
|---|---|---|
| Public fast noncryptographic hash | high trusted-input throughput | predictable adversarial collisions |
| Random universal family | input-independent expected pair bounds | seed/family assumptions and per-use integration |
| Secret keyed PRF-style table hash | HashDoS resistance goal | key lifecycle, cost, side-channel/review scope |
| Stable versioned hash | reproducible storage/partitioning | precomputation attacks if used unprotected online |
| Cryptographic digest | content integrity/addressing properties | cost; not automatically table or password policy |
| Cached full hash/fingerprint | avoids repeated key work/comparisons | memory, invalidation, collision handling |
| Power-of-two reduction | fast/simple and table-friendly | exposes low-bit weakness |
| Arbitrary/prime modulo | different pattern interaction | division cost/bias; no cure for bad hashes |

## Failure Modes and Misconceptions

- **“No collisions in tests means collision-free.”** Finite outputs guarantee collisions for a larger domain.
- **“Different hash proves different object.”** It proves non-equality only when equal keys must hash equal; equal hash proves nothing.
- **“Random inputs validate hostile inputs.”** The probability space and adversary differ.
- **“A random seed fixes any mixer.”** Protection depends on a defined family and inaccessible/unpredictable selection.
- **“Modulo creates randomness.”** It only reduces existing values and can reveal structure/bias.
- **“Prime bucket count guarantees spread.”** It cannot repair ignored fields or constructed collisions.
- **“Avalanche proves cryptographic security.”** Statistical diffusion does not establish PRF/MAC/collision-resistance claims.
- **“SipHash means stable outputs.”** keyed/process-random use intentionally changes results with the key.
- **“SHA makes a table safe.”** unbounded inputs, collision resolution, equality, memory, and request limits still matter.
- **“Hash is O(1).”** variable-length key encoding/hashing is linear in processed input absent caching/bounds.
- **“Runtime hashes are durable IDs.”** algorithms, widths, seeds, and versions may change.
- **“One histogram certifies the function.”** it covers one generator, size, reduction, seed, and sample.

## Worked Examples

### Example 1

Two user keys compare case-insensitively: `Admin≈admin`. Hashing original spelling gives different values, so lookup may miss. Canonical case folding must match the exact equality policy. Conclusion: equality determines hashing inputs.

### Example 2

Encoding fields by concatenation maps `(ab,c)` and `(a,bc)` to `abc`. Type tags and lengths produce distinct encodings before hashing. Conclusion: a hash cannot recover boundaries the encoder erased.

### Example 3

For n=1000,m=1024 under independent uniform hashing, expected colliding pairs are `1000·999/(2·1024)≈487.79`, although expected bucket load is below one. Conclusion: collisions can be numerous in pairs while occupancy remains sparse.

### Example 4

All 256 w=8 outputs reduced modulo 10 give counts 26 in six buckets and 25 in four. Conclusion: modulo bias is exact and bounded here, not zero.

### Example 5

Sixteen values with their low four bits zero map through `h&15` to one bucket. Their high bits vary, but masking discards them. Conclusion: distribution must be judged after actual reduction.

### Example 6

A constant hash sends every key to one bucket. A correct chained map still returns exact values after equality checks, though operations degrade. Conclusion: distribution is a performance/security property, not semantic correctness.

### Example 7

A process-randomized string hash produces different layouts after restart. Serializing its bucket numbers makes a cache unreadable. Conclusion: durable placement requires a specified stable algorithm/version.

### Example 8

An attacker submits many colliding names to an unkeyed chained table; insertion scans a growing bucket and aggregate work becomes quadratic. Conclusion: average-case claims need an adversarial resource model.

### Example 9

A chi-square run returns an ordinary p-value for one million random keys, but a corpus of page-aligned addresses collapses low bits. Conclusion: generic random tests do not replace domain-structured corpora.

### Example 10

Profiling shows 22% in hashing. Replacing the algorithm before counting calls cannot distinguish expensive bytes from redundant rehashing or avoidable canonicalization. Conclusion: optimize the measured causal path one factor at a time.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) connects equivalence relations, object identity, mutation, and observable iteration.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects byte encodings, integer overflow, SIMD, entropy, cached metadata, and ABI width.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) connects stable identifiers, caches, compatibility, and migration.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects randomized analysis, balls into bins, adversarial testing, and profiling.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects hash indexes/joins, persisted formats, statistics, skew, spill, and rehashing.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) connects partition functions, key skew, reproducibility, and hot partitions.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns HashDoS, keyed primitives, secrets, resource limits, MACs, digests, and password hashing.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects consistent hashing, membership changes, replicas, and versioned placement.

## References

1. J. Lawrence Carter and Mark N. Wegman, [Universal Classes of Hash Functions](https://citeseerx.ist.psu.edu/document?doi=d8777ef17c18609781aa889055100603b13b2986&repid=rep1&type=pdf). Primary 1979 paper defining randomized hash classes and input-independent expected storage/retrieval analysis.
2. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/legacy/event/sec03/tech/full_papers/crosby/crosby.pdf). Primary 2003 security paper demonstrating remotely induced hash-table worst cases.
3. Jean-Philippe Aumasson and Daniel J. Bernstein, [SipHash: a Fast Short-Input PRF](https://eprint.iacr.org/2012/351.pdf). Primary design/security/performance paper and hash-flooding motivation.
4. Python Project, [PEP 456: Secure and Interchangeable Hash Algorithm](https://peps.python.org/pep-0456/). Accepted design history for CPython string/bytes hash hardening and interchangeable implementation.
5. Python Software Foundation, [Python 3 Data Model](https://docs.python.org/3/reference/datamodel.html#object.__hash__). Current equality/hash coherence, width, override, unhashable, and salted str/bytes behavior.
6. Rust Project, [`HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current default random seeding, HashDoS intent, algorithm-change warning, key mutation logic error, and table behavior.
7. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Equivalent-key/hash coherence, buckets, rehashing, and average/worst-case requirements.
8. NIST, [FIPS 202: SHA-3 Standard](https://csrc.nist.gov/pubs/fips/202/final). Normative cryptographic hash/extendable-output standard illustrating a goal distinct from ordinary table distribution.
9. Go Project, [`hash/maphash`](https://pkg.go.dev/hash/maphash). Current seeded byte-sequence hash API, seed comparability restrictions, and explicit non-cryptographic guidance.
10. Rust Project, [`Hash` trait](https://doc.rust-lang.org/std/hash/trait.Hash.html). Current equality coherence, prefix-free encoding requirement, portability warning, and derive/custom implementation contract.

## Exercises

### Exercise 1

Specify equality, immutability, and hashing for a composite `(tenant_id, normalized_email)` key, including Unicode/case policy, encoding, and failure cases.

### Exercise 2

Derive expected bucket load and colliding-pair count under independent uniform hashing, then state what changes under only a universal-family per-pair bound.

### Exercise 3

Diagnose a power-of-two table whose keys are aligned integer addresses and whose bucket histogram collapses. Propose mapper/hash changes and causal tests.

### Exercise 4

Design separate hashing profiles for an attacker-facing in-memory map, a persisted on-disk index, cross-service sharding, content integrity, and password storage.

### Exercise 5

Create a verification and benchmark plan for replacing a production table hasher after profiling reports high CPU and periodic collision spikes.

## Answers to the Exercises

### Answer 1

Define equality only after choosing the email identity policy: for example tenant bytes must match and emails compare by a pinned, application-approved normalization/case rule, not an unspecified locale transform. Normalize once or hash through the identical pure canonicalizer. Encode a schema/type tag, checked tenant-byte length and bytes, then checked normalized-email length and UTF-8 bytes; distinguish null/absent and reject malformed/disallowed forms. Equal keys therefore encode identically and hash identically. Freeze both fields while indexed; changes remove under old identity then insert the new key. Test equal alternative spellings, unequal tenants, ambiguous concatenations, empty/max lengths, malformed input, normalization-version migration, forced collisions, and mutation attempts.

### Answer 2

For independent uniform choices, a bucket load is the sum of n indicators each with expectation 1/m, so expected load is n/m. There are `n(n-1)/2` unordered pairs; each collides with probability 1/m, so expected colliding pairs are `n(n-1)/(2m)` by linearity. With a universal family and a fixed distinct key set before random h selection, each pair probability is at most 1/m, so expected pairs are at most that expression. This alone does not give full independence, the same tail bounds, a secret-against-adaptive-attacker guarantee, or table probe costs; those require the exact family, adversary, and collision strategy.

### Answer 3

If bucket is `h&(m-1)` and h preserves address low bits, alignment makes many low bits zero. Confirm by recording full-hash bit frequencies and bucket loads across each capacity, then test the exact aligned corpus. Candidate changes are a reviewed final mixer that moves varying address bits into low positions, multiplicative high-bit reduction, or hashing stable object identity bytes rather than raw alignment-heavy representation. Keep the table/corpus/load fixed and change one mapper; require semantic results under a constant-hash oracle, improved structured-corpus loads/probes, no regression on other corpora, and measured latency/CPU/cache behavior. A prime m is a comparator, not a proof or universal cure.

### Answer 4

Use a per-process/instance secret randomly seeded, reviewed HashDoS-resistant table hasher plus resource limits for attacker-facing maps; outputs are ephemeral. Define canonical bytes and an algorithm/version/width/byte order for persisted indexes, with migration and collision resolution. Define a separately versioned deterministic partition function and topology policy for cross-service sharding; test skew and membership changes. Use an approved cryptographic digest/MAC profile for integrity/authenticity according to whether a secret is needed. Use a dedicated password-hashing scheme with unique salts, configured memory/time cost, versioning, and upgrade—not any table hash or fast general digest. Separate keys, domains, APIs, and evidence.

### Answer 5

First count hash calls, bytes/call, canonicalization, cache hits, full/bucket collisions, probes/equality checks, load/resize events, key distributions, and collision-spike inputs. Form competing hypotheses: expensive primitive, redundant calls, costly encoding, weak distribution after reduction, skew/duplicates, or resize/tombstone behavior. Preserve representative and hostile traces. Benchmark one change at a time with fixed table/layout/semantics, including hits/misses, lengths/types, load sweep, resize, updates/deletes, memory, allocations, profiles, probes, cache misses, p50/p95/p99, throughput, and seed variation. Property-test equality coherence, prefix-free encoding, constant-hash correctness, mutation restrictions, and migration/reproducibility requirements. Security review covers seed entropy/scope/disclosure, adaptive attackers, request limits, fallback, and monitoring. Roll out with collision/probe/latency telemetry and rollback; do not infer cryptographic strength or universal production improvement from statistical batteries or a synthetic speedup.
