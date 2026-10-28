---
module_id: DSE-078
program: Data Structures Engineering
level: 2
module_number: 78
title: Bloom-Assisted Lookup
status: complete
last_verified: 2026-08-30
---

# Bloom-Assisted Lookup

## One-Page Review

### Governing question

How can probabilistic membership filters safely avoid unnecessary SSTable reads without creating false-negative data loss, incompatibility bugs, or misleading performance claims?

### Essential definitions

- A **Bloom filter** represents a set with an m-bit array and k deterministic hash-derived probes per inserted item.
- A **negative** means “definitely not in the represented set” only when the filter is intact, compatible, complete, and queried in its construction domain.
- A **positive** means “may be present”; the data index/block remains authoritative and can reveal a false positive.
- A **false positive** is a filter-positive query for an absent represented item. A **false negative** is forbidden for an ordinary correctly constructed Bloom filter and is a correctness defect in integration.
- **Bits per key** `b=m/n` and probe count k shape memory, CPU, and false-positive probability.
- A **whole-key filter** represents exact user keys; a **prefix filter** represents outputs of a pinned prefix extractor and supports only compatible query shapes.
- A **full-file filter** covers an SSTable; a **block-based/partitioned filter** narrows smaller regions and changes cache/read behavior.
- A **filter policy identity** binds hash scheme, seed, probe derivation, encoded format/version, key transformation, and domain.

### Central model, mechanism, or theorem

Under the usual independent uniform-hash approximation after inserting n items,

`p_fp ~= (1 - exp(-kn/m))^k`,

and the real-valued optimum is `k ~= (m/n) ln 2`, with `p_fp ~= (0.6185)^(m/n)`. These are design approximations, not guarantees for a concrete hash, finite layout, cache-local variant, skewed domain, or adversarial keys. Measure realized positives and authoritative misses.

For a negative point lookup across candidate runs i with valid false-positive rates `p_i`, the expected number of unnecessary authoritative probes is roughly `sum p_i` if each applicable filter is checked and independence/workload assumptions hold. The end-to-end cost also includes filter metadata reads/cache misses, hashes, range metadata, indexes, data blocks, decompression, and base-record access. Allocating equal bits per key across levels need not minimize this sum under a fixed memory budget; run sizes and access probabilities matter.

The safety rule is asymmetric: a valid negative can prune; a positive cannot answer found. If filter bytes, checksum, policy, comparator, prefix extractor, file identity, or feature are missing/invalid/unsupported, fall back to the authoritative path or report corruption/unsupported according to policy—never treat uncertainty as absence.

### Critical invariants

1. Every represented user key/prefix is inserted using exactly the transformation and hash policy used by compatible readers.
2. Filter policy/version/domain and file/block identity are persisted and validated before pruning.
3. No valid inserted item tests negative; golden and exhaustive-per-built-filter checks detect builder/reader drift.
4. A negative skips only the file/block set the filter actually covers; range/sequence/snapshot logic still selects candidate sources.
5. A positive triggers authoritative lookup and never directly returns a value.
6. Corrupt, truncated, unavailable, unknown, or incompatible filters cannot produce an absence result.
7. Metrics separate true positives, false positives, true negatives, inapplicable/invalid filters, filter metadata I/O, and data reads saved/incurred.

### Common failures

- Hashing internal keys at build time but user keys at read time, or vice versa.
- Changing seed, comparator normalization, prefix extractor, or policy name without invalidating old filters.
- Using whole-key negative to skip a prefix/range query, or a prefix filter for an incompatible seek.
- Omitting tombstoned/older user keys from a file filter when the file still contains relevant entries.
- Treating a positive as proof of existence or a filter error as a negative.
- Checking the wrong partition/block filter because its mapping/index is corrupt or stale.
- Spending more I/O/cache/CPU to retrieve a filter than the avoided data probe costs.
- Reporting configured p instead of observed false positives by level, query class, and cache state.

### Compact example

Three immutable runs each contain three keys and a 16-bit, two-probe filter. Lookup `beta` receives a negative from run 0 and a positive from run 1, then finds beta in run 1: two filter checks, one authoritative read. Absent `mu` is negative in runs 0 and 1, positive in run 2, and misses there: three checks, one false-positive read, two reads safely skipped.

### Connections

DSE-076 supplies LSM candidate/version semantics, DSE-077 the filter meta-block and immutable file contract, DSE-081 develops Bloom-filter mathematics, and DSE-082 variants with deletion/growth. Database Engineering adds query semantics and corruption policy; Performance Engineering adds memory/cache/workload optimization.

## Governing Question

How do we turn a Bloom filter's mathematical no-false-negative property into a trustworthy on-disk optimization whose failures degrade to extra work or explicit errors, never missing data?

## Why This Matters

An absent point key in an LSM can otherwise require index/data probes in every overlapping L0 file and each level. Small membership summaries can reject most files before data I/O, often shifting negative lookups from many random reads toward memory/cache probes. This is valuable for caches, metadata stores, databases, and object-backed sorted runs.

The optimization sits on a dangerous branch: a negative prevents an authoritative read. A builder that forgot a key, a reader using a different hash, a corrupt offset, an incompatible prefix extractor, or a stale cache entry can become silent data loss. A false positive is expected and safe; a false negative from integration is not “probabilistic.”

Filter economics are also system-specific. Full filters may occupy substantial memory; partitioned filters can bound cache admission but add index/meta reads. On very fast storage, hash/cache CPU can dominate. Positive-heavy workloads benefit less. Large ranges usually need ordered indexes rather than membership. Memory allocated to filters competes with block cache and memtables. The correct design optimizes end-to-end misses and tails under a correctness-first fallback.

## Prerequisites and Retrieval

Retrieve:

- sets, bit arrays, hashing, probability, expectation, exponential approximations, and empirical confidence;
- LSM memtable/run/level candidate selection, internal versus user keys, tombstones, snapshots, and point/range reads;
- SSTable metaindex/filter blocks, checksums, policy identities, cache keys, handles, and format migration;
- prefix extractors, comparator/normalization, bounds, iterators, and query-domain preconditions;
- property testing, golden files, corruption injection, metrics, cache-state benchmarks, and adversarial inputs.

Diagnostic retrieval: a false positive costs an extra authoritative probe and then returns absent; a false negative skips the only file containing the newest visible entry and returns wrong absence. Their risk is fundamentally asymmetric.

## Learning Objectives

After this module, you can:

1. derive approximate Bloom false-positive probability and probe-count choice with assumptions;
2. integrate filters after range/version candidate selection and before authoritative data lookup;
3. distinguish whole-key, prefix, full, block-based, and partitioned filter domains;
4. version hash/policy/transformation and validate filter bytes, mapping, checksum, and file identity;
5. specify safe fallback for missing, corrupt, incompatible, unavailable, or uncached filters;
6. test zero false negatives over inserted items plus realized false positives over absent workloads;
7. allocate memory among levels/files/filters/cache using expected end-to-end work rather than configured p alone;
8. observe and tune filter effectiveness, CPU, metadata reads, cache behavior, data probes, and tails.

## Core Exposition

**Place the filter in the read pipeline.** First determine candidate files from manifest, snapshot/sequence, key range, level overlap, and file properties. For each candidate, load/validate the applicable filter. A negative prunes that candidate. A positive or unavailable/inapplicable filter continues to the file index and data block. The authoritative internal-key lookup resolves versions and tombstones. Filters do not replace range metadata, indexes, or MVCC.

**Represent the correct domain.** Most LSM point filters insert user keys, not internal keys containing sequence, so one filter member covers every version/tombstone for that user key in the file. If a builder inserts only live/latest values but the file still stores older or deletion entries relevant to snapshots/compaction, pruning can be incorrect. State whether merge operands, range tombstones, blobs, and partition keys are represented.

**Persist policy identity.** A policy includes algorithm family, format version, bit/probe layout, hash and seed/domain separation, key canonicalization, prefix extractor, comparator relationship, and checksum context. A reader must select decoding by the file's identity, not current configuration. Unknown policies are ignored with authoritative fallback or rejected as required features; they are never interpreted approximately.

**Validate construction completely.** A builder receives the final file's represented keys after ordering. It initializes bounded storage, adds every domain element, finalizes format/checksum, and records item count/bits/probes/policy. Before publication, test every distinct inserted element against the final encoded filter. This O(n) check does not prove the hash implementation universally, but it directly catches many builder/serialization false negatives.

**Model the pruning asymmetry.** The finite example uses deterministic educational hashes and per-run bit sets. It checks all nine inserted items, then compares two lookup paths.

<!-- bijux-verify: {"id":"per-run-bloom-pruning-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"runs=3\nbits_per_filter=16\nhash_probes=2\ninserted_keys=9\nall_members_positive=True\nlookup_beta=beta\nbeta_filter_checks=2\nbeta_data_reads=1\nlookup_mu=ABSENT\nmu_filter_checks=3\nmu_data_reads=1\nmu_false_positive_runs=1\nfilter_skipped_reads_for_mu=2\nvalid=True\nevidence=per_run_bloom_pruning_model\n","stderr":""}} -->
```python
runs = [
    ["alpha", "delta", "kappa"],
    ["beta", "epsilon", "lambda"],
    ["gamma", "theta", "omega"],
]
bit_count = 16
probe_count = 2


def positions(key):
    first = sum(ord(char) for char in key)
    second = sum((index + 1) * ord(char) for index, char in enumerate(key)) | 1
    return [(first + probe * second) % bit_count for probe in range(probe_count)]


def build_filter(run):
    bits = set()
    for key in run:
        bits.update(positions(key))
    return bits


filters = [build_filter(run) for run in runs]


def may_contain(bits, key):
    return all(position in bits for position in positions(key))


def lookup(key):
    checks = 0
    reads = 0
    false_positive_runs = 0
    for run, bits in zip(runs, filters):
        checks += 1
        if not may_contain(bits, key):
            continue
        reads += 1
        if key in run:
            return key, checks, reads, false_positive_runs
        false_positive_runs += 1
    return None, checks, reads, false_positive_runs


all_members_positive = all(may_contain(bits, key) for run, bits in zip(runs, filters) for key in run)
beta, beta_checks, beta_reads, _ = lookup("beta")
mu, mu_checks, mu_reads, mu_false = lookup("mu")
valid = all_members_positive and beta == "beta" and mu is None and mu_false == 1
print(f"runs={len(runs)}")
print(f"bits_per_filter={bit_count}")
print(f"hash_probes={probe_count}")
print(f"inserted_keys={sum(len(run) for run in runs)}")
print(f"all_members_positive={all_members_positive}")
print(f"lookup_beta={beta}")
print(f"beta_filter_checks={beta_checks}")
print(f"beta_data_reads={beta_reads}")
print("lookup_mu=" + ("ABSENT" if mu is None else mu))
print(f"mu_filter_checks={mu_checks}")
print(f"mu_data_reads={mu_reads}")
print(f"mu_false_positive_runs={mu_false}")
print(f"filter_skipped_reads_for_mu={len(runs) - mu_reads}")
print(f"valid={valid}")
print("evidence=per_run_bloom_pruning_model")
```

The hashes are intentionally weak and deterministic for reproducibility; the bit sets are not serialized Bloom blocks. Runs contain unique strings and no versions/tombstones, range pruning, cache, corruption, policy migration, or I/O. The selected absent key has one deterministic false positive. This run proves only pruning control flow for these inputs.

**Derive approximate sizing carefully.** A particular bit remains zero after kn independent probes with probability approximately `exp(-kn/m)`, so all k queried bits are one with approximate probability `(1-exp(-kn/m))^k`. Differentiating the idealized expression gives `k=(m/n)ln2`. Implementations choose integer/clamped k and may shard/cache-line-localize bits, changing realized behavior. Small n, blocked layouts, poor hashes, adversarial keys, and duplicate insertions require measurement.

**Whole-key versus prefix is a type distinction.** Whole-key filters support exact key membership. A prefix filter inserts `Transform(key)` and can prune a seek/iteration only if the query and bounds remain within a compatible transformed prefix domain. A changed extractor, `total_order_seek`, short key, reverse comparator, or cross-prefix range may make it inapplicable. Make applicability an explicit decision with tests, not an implicit option interaction.

**Choose filter granularity.** One full filter per SSTable needs one filter query to prune the file and can be compact, but loading it can create cache cliffs for large files. Block-based filters cover groups of data blocks; the index must first map target to the correct filter region, and corrupt mapping cannot prune. Partitioned filters split metadata by key range so cache loads are bounded; they add top-level index lookups and more cache churn. Measure p and metadata I/O together.

**Treat filter storage as untrusted.** Validate metaindex handle, filter policy name/version, checksum, length/count/offset arrays, bit count, probe count bounds, partition mapping, and file identity with checked arithmetic before probing. A zero-length or malformed filter cannot mean an empty set unless the format explicitly proves it represents an empty file. Bound hashes, memory, decompression, and error reporting.

**Define safe fallback.** If optional filter is absent, uncached, I/O-failed, corrupt, unsupported, or inapplicable, continue through file index/data unless broader corruption policy requires explicit error. If filter is a required authenticated component, fail accordingly. Record why pruning was unavailable. A system that silently maps filter failure to negative converts availability/corruption into data loss.

**Filters and tombstones interact only through membership.** A point filter says the file may contain some internal entry for user key. It cannot determine whether that entry is a value, tombstone, merge operand, expired version, or visible snapshot result. A positive must read authoritative entries; a negative only excludes that file's contribution. Range tombstones may need separate metadata because their start key/domain can affect keys not inserted individually.

**Allocate memory by avoided work.** A level/file with many negative probes, expensive storage, and high candidate probability may deserve more bits than a hot cached or rarely consulted level. Under simplifying assumptions, negative lookup expected false-positive reads sum across candidates. Research such as Monkey co-optimizes filters and merge policy. Production allocation also weighs filter metadata cache, block cache displacement, CPU hashes, positive workload, range queries, and tail objectives.

**Observe ground truth.** For each file/level/query class count filter checked, true negative (read skipped), positive, authoritative true positive, authoritative false positive, inapplicable, missing, cache hit/miss, I/O/error/corrupt/unsupported, data block read, bytes, CPU, and latency. The observed false-positive denominator is eligible absent membership queries, not all operations. Sample/aggregate without leaking sensitive keys.

**Test zero false negatives continuously.** Builder self-checks all inserted distinct domain values. Golden files pin policies. Cross-version readers test old/new formats and extractors. Property tests generate sets/queries and compare with exact set. Mutate every bit/header/offset/checksum/policy. Fault filter reads/cache replacement. Test compaction output, empty files, duplicate keys, prefixes, short keys, tombstones, range deletions, and comparator changes. A canary can bypass filters for sampled negative decisions and compare authoritative results.

## Definitions and Notation

Let m be filter bits, n distinct represented domain items, k probe count, `b=m/n` bits per item, and `p_i` realized/target false-positive probability for candidate i. `H_policy(x)` returns k positions under a versioned transformation/hash policy. Filter decision is `maybe` iff every bit is one.

Let `Candidate(q,file,snapshot)`, `Applicable(q,policy)`, and `Valid(filter,file)` be explicit predicates. Only `Candidate and Applicable and Valid and negative` permits pruning. `TrueNegative`, `FalsePositive`, and `TruePositive` are determined against authoritative file membership, not final database visibility. False negative is an invariant violation.

## Mechanisms, Invariants, or Proof Structure

### No-false-negative proof

1. Define represented domain transform and deterministic k valid positions.
2. Insert every distinct represented element by setting all those positions.
3. Serialize/deserialize without losing or changing set bits or policy identity.
4. Query an inserted element using the identical transform/hash/layout.
5. Every queried bit was set and ordinary Bloom insertion never clears it, so result is maybe.
6. Any negative for an inserted item identifies construction, format, corruption, concurrency, or compatibility failure—not expected probability.

### Lookup refinement proof

1. Select complete candidate sources by range/version/snapshot independently of filters.
2. For each candidate, establish filter validity, identity, domain, and query applicability.
3. Valid negative proves represented key/prefix absent from only that covered source and safely prunes it.
4. Positive/unknown/inapplicable continues to authoritative index/data and version resolution.
5. Found/deleted/absent final result equals the unfiltered read algorithm.
6. File/version pinning prevents compaction, cache, or identity reuse from changing the evidence mid-read.

### Tuning/evidence proof

1. State memory, candidate/run, workload, independence/hash, cache, and storage assumptions.
2. Derive approximate p and expected false-positive probes under those assumptions.
3. Instrument decisions against authoritative membership without changing correctness path.
4. Measure memory/CPU/filter metadata/data I/O/bytes/tails in representative steady state.
5. Vary bits/probes/granularity/allocation and confirm zero observed false negatives in compatibility/fault gates.
6. Choose policy from service objectives and retain rollback/bypass when evidence regresses.

## Alternatives and Trade-Offs

| Choice | Strength | Cost/proof burden |
|---|---|---|
| No filter | simplest authoritative path | negative read amplification |
| Whole-key filter | exact point-domain pruning | not prefix/range summary |
| Prefix filter | prefix seek pruning | extractor/query applicability |
| Full-file filter | one file-level decision | large metadata/cache cliff |
| Block-based filter | finer data-block pruning | mapping and more structures |
| Partitioned filter | bounded cache loads/tails | top-level index and I/O |
| More bits/key | lower approximate p | memory/cache displacement |
| More probes | potentially lower p to optimum | CPU/cache accesses |
| Equal per-level p | simple configuration | often not cost-optimal |
| Workload-weighted memory | lower expected cost | telemetry/adaptation stability |
| Optional fallback | corruption degrades to work | may expose data corruption later |
| Required authenticated filter | stronger file contract | availability on filter damage |

## Failure Modes and Misconceptions

- **“Bloom filters sometimes have false negatives.”** Correct ordinary filters do not; integration defects do.
- **“Positive means the key exists.”** It means inspect authoritative storage.
- **“Negative means absent from database.”** It covers one represented file/block domain only.
- **“Hash internal keys for point lookup.”** Usually filter user-key domain; specify exact contract.
- **“Prefix filters accelerate any range.”** Only queries compatible with extractor/domain may prune.
- **“Unknown policy can use current hash.”** Fall back or reject; never reinterpret.
- **“Corrupt filter can be ignored as empty.”** Ignore optimization by probing data or report corruption.
- **“Configured p is observed p.”** Measure eligible absent queries and authoritative outcomes.
- **“More bits always improve latency.”** Cache displacement, metadata I/O, hashes, positives, and media change the optimum.
- **“One filter per level is enough.”** Overlap/file structure and update lifecycle determine ownership/granularity.
- **“Filters solve range scans.”** They are membership summaries; ordered indexes/fences serve general ranges.
- **“Filter checksum proves no false negatives.”** It does not prove complete insertion, correct domain, or compatible hashing.

## Worked Examples

### Example 1

**Problem.** Estimate p for 10 bits/key and k=7.

**Derivation.** `p≈(1-exp(-0.7))^7≈0.0082` under ideal assumptions. Real format/hash/layout/workload may differ.

**Conclusion.** Sizing predicts a target; measurement validates realization.

### Example 2

**Problem.** Choose ideal k for 8 bits/key.

**Derivation.** `8 ln2≈5.55`, so compare supported integer 5/6 plus implementation CPU/cache constraints.

**Conclusion.** Probe count is discrete and system-dependent.

### Example 3

**Problem.** Trace beta in the model.

**Derivation.** Run 0 negative skips data. Run 1 positive causes one authoritative read and finds beta. Search stops under newest-to-oldest source ordering.

**Conclusion.** Negative saves work; positive delegates correctness.

### Example 4

**Problem.** Trace absent mu.

**Derivation.** Two negative filters skip runs; run 2 produces a false positive, so one data read misses. Final result remains absent.

**Conclusion.** False positives cost work, not correctness.

### Example 5

**Problem.** Filter omits a tombstoned user key present in file.

**Derivation.** A negative can skip the tombstone and expose an older value in another run. Insert every represented user key regardless of entry kind under the policy.

**Conclusion.** Tombstones must participate in membership domain.

### Example 6

**Problem.** Prefix extractor changes from 4 bytes to delimiter prefix.

**Derivation.** Old filter hashes another domain. Reader detects policy identity mismatch and ignores it or uses compatible old extractor; it cannot issue negatives with the new transform.

**Conclusion.** Transformation is persisted format semantics.

### Example 7

**Problem.** Filter checksum fails.

**Derivation.** If optional, mark corrupt/unusable and query index/data; if required, report corruption. Never return not found from damaged bits.

**Conclusion.** Safe failure is extra work or explicit error.

### Example 8

**Problem.** Ten candidate levels each have p=1% for absent key.

**Derivation.** Expected false-positive authoritative probes are roughly 0.10 under simplifying independence; probability of at least one is `1-0.99^10≈9.56%`.

**Conclusion.** Small per-run p accumulates across candidates.

### Example 9

**Problem.** Full filter is 8 MiB but negative data read is cached and cheap.

**Derivation.** Loading/evicting filter may cost more than the saved probe. Partition/cache/pin differently or reduce bits; compare end-to-end tails.

**Conclusion.** Filter memory has opportunity and I/O cost.

### Example 10

**Problem.** Dashboard reports 0.5% positives but not authoritative outcomes.

**Derivation.** It cannot distinguish true from false positives or compute realized p. Add counters/sampling for exact file membership, eligible negatives, bypass reasons, reads/bytes saved, CPU, and latency.

**Conclusion.** Optimization quality needs ground truth.

## Cross-Program Connections

- **Database Engineering:** point lookup, MVCC/tombstones, indexes, corruption policy, backup, migration, and query observability define filter correctness context.
- **Data Engineering:** probabilistic file/partition pruning, lake metadata, streaming dedup hints, and remote object range requests reuse safe-negative logic.
- **Security Engineering:** adversarial collisions, hash-flood/CPU, malformed offsets, cache identity, tenant leakage, corrupt negatives, and telemetry privacy are trust boundaries.
- **Distributed Systems:** replicas may hold different file sets/policies; repair and rolling upgrades require per-file compatibility and no shared false-negative assumption.
- **Performance Engineering:** bits/probes, blocked/cache-local layouts, filters versus block cache, workload skew, candidate frequency, remote cost, and tails drive allocation.
- **Formal Methods:** refinement proves filtered reads equivalent to authoritative reads when validity/applicability/no-false-negative assumptions hold.

## References

1. Google LevelDB, [`util/bloom.cc`](https://github.com/google/leveldb/blob/main/util/bloom.cc), current source accessed 2026-08-30. Maintainer hash/probe/format policy implementation and compatibility behavior.
2. Google LevelDB, [“Table Format: Filter Meta Block”](https://github.com/google/leveldb/blob/main/doc/table_format.md), current maintainer documentation accessed 2026-08-30. Filter policy naming, block-offset grouping, offsets, and metaindex discovery.
3. RocksDB Project, [“RocksDB Bloom Filter”](https://github.com/facebook/rocksdb/wiki/RocksDB-Bloom-Filter), current maintainer documentation accessed 2026-08-30. Full, block-based, partitioned, whole-key/prefix, cache, metrics, and format behavior.
4. RocksDB Project, [“Prefix Seek”](https://github.com/facebook/rocksdb/wiki/Prefix-Seek), current maintainer documentation accessed 2026-08-30. Prefix extractor/query compatibility and configuration constraints.
5. Niv Dayan, Manos Athanassoulis, and Stratos Idreos, [“Optimal Bloom Filters and Adaptive Merging for LSM-Trees”](https://cs-people.bu.edu/mathan/publications/tods18-dayan.pdf), *ACM TODS* 43(4), 2018. Primary cross-level memory/allocation and LSM lookup trade-off analysis.
6. Apache Cassandra, [`bloom_filter_fp_chance`](https://cassandra.apache.org/doc/latest/cassandra/reference/cql-commands/create-table.html), current documentation accessed 2026-08-30. Official per-table SSTable filter false-positive/memory configuration.
7. Google LevelDB, [“Filters”](https://github.com/google/leveldb/blob/main/doc/index.md), current maintainer usage documentation accessed 2026-08-30. Bits-per-key and avoided random-read motivation.
8. RocksDB Project, [“New Bloom Filter Format”](https://rocksdb.org/blog/2014/09/12/new-bloom-filter-format.html), maintainer engineering note, 2014. Full-file filter layout motivation and measured implementation context.

## Exercises

### Exercise 1

Derive the approximate false-positive formula and optimal real k. Compute p and candidate-level accumulation for 8 bits/key, k=6, and six independent candidate files. State every assumption and what must be measured.

### Exercise 2

Specify a safe LSM point-read algorithm using manifest/range/sequence selection, whole-key filters, indexes/data, snapshots, tombstones, cache/file pinning, and outcomes for negative, positive, missing, corrupt, unsupported, unavailable, and inapplicable filters.

### Exercise 3

Design a versioned filter block/policy for SSTables. Include domain, hash/seed/probes, bits, empty representation, offsets/partitions, checksum/file identity, builder self-check, parser bounds, cache key, migration, downgrade, and fuzz/golden evidence.

### Exercise 4

Design prefix-filter applicability for composite tenant/time keys and forward iterators. Cover extractor, short keys, bounds, cross-prefix ranges, total-order seeks, reverse scans, comparator changes, tombstones, and rolling upgrades.

### Exercise 5

Audit a system that hashes internal keys during build and user keys during read, treats unknown policy/checksum failure as negative, uses prefix filters for all ranges, reports configured p as realized, and allocates equal bits/key while filters evict hot data blocks.

## Answers to the Exercises

### Answer 1

A bit remains zero after kn ideal independent uniform probes with probability `(1-1/m)^(kn)≈exp(-kn/m)`. Thus one is one with probability `1-exp(-kn/m)`, and all k query bits are one with approximate `p=(1-exp(-kn/m))^k`. Minimizing ideal p yields `k=(m/n)ln2`; for b=8, ideal k≈5.55, so k=6 is natural.

`p≈(1-exp(-6/8))^6≈0.0216`. Across six independent applicable absent-file queries, expected false-positive probes ≈`6p≈0.1296`; probability at least one ≈`1-(1-p)^6≈0.1228`. Assumptions include fixed n/m, independent uniform hashes/probes/files, correct filters, eligible absent membership, and no caching/cost variation. Measure actual positives confirmed absent, hashes/CPU, filter metadata/cache I/O, data probes/bytes, file/level distribution, workload skew, and tails.

### Answer 2

Pin a manifest/version and snapshot. Select every source whose range and sequence can contribute. For each file, pin immutable identity and determine whole-user-key filter policy validity/applicability. A valid negative skips that file only. Positive, missing optional, unavailable/uncached, unsupported optional, or inapplicable proceeds to checked index/data. Corrupt optional filter can fall back while surfacing corruption telemetry; required/authenticated-policy corruption returns explicit error.

Authoritative lookup compares internal versions under snapshot, returning value, visible tombstone/absence, merge result, or explicit corrupt/I/O/unsupported. Never let filter answer found or convert errors to absent. File/cache references survive compaction; cache key includes database/file generation, offset/type/format/policy. Instrument true negatives, confirmed true/false positives, bypass reasons, data reads/bytes, CPU, and latency, and sample bypass negatives against authoritative path.

### Answer 3

Persist algorithm/format version, exact user-key/prefix transform, hash family/seed/domain separation, probe derivation/count bounds, bit count, distinct item count, empty-set encoding, full/block/partition mapping, comparator relationship, checksum algorithm/scope, file/component identity, and required/optional feature status. Use checked canonical offsets/lengths/counts and map each partition to exact covered data regions.

Builder inserts every represented domain element including tombstones/versions' user keys, finalizes, then queries every distinct inserted item against serialized/decoded filter before file publication. Parser validates identity/checksum, arithmetic, bit/probe bounds, offsets/order, empty case, mapping, resource limits. Cache key includes immutable file generation and policy/partition. Golden old/new files and cross-version readers cover upgrade/downgrade; unknown optional falls back. Property tests compare exact sets with zero false negatives, absent p distributions, every-field mutation/truncation, corrupt mapping/checksum, adversarial hashes, and file-ID reuse.

### Answer 4

Define canonical composite encoding and prefix extractor—for example complete tenant component, not arbitrary bytes that split encoding. Filter inserts each represented transformed prefix. A forward iterator may prune only when lower/upper bounds and seek semantics guarantee all possible results share one applicable prefix; a cross-tenant/time range cannot. Short/invalid keys, unbounded ranges, total-order mode, reverse scans, and extractor mismatch bypass unless individually proven.

Tombstone/user entries must contribute the same represented prefix domain. Comparator/normalization and extractor identity are versioned per file. During rolling upgrade, readers retain old extractors for compatible files or ignore their filters; builders write the new policy only after readers can handle it. Tests enumerate prefix boundaries, short keys, successor/end computation, inclusive/exclusive bounds, cross-prefix and reverse queries, comparator versions, tombstones, snapshots, and authoritative equivalence under split/compaction.

### Answer 5

Builder/reader domain mismatch causes false negatives; choose and persist one domain, typically user key, rebuild incompatible filters, and self-check all inserted elements. Unknown policy or bad checksum is uncertainty/corruption, so bypass to authoritative data or fail explicitly—never negative. Prefix pruning requires proven query/extractor compatibility; general ranges use ordered index/fences.

Configured p is only an approximation/target. Count eligible absent checks and confirmed false positives by file/level/query/cache state, zero false negatives via builder/canary tests, and reads/bytes/CPU/tails. Equal bits may waste memory on rarely consulted/cheap levels while evicting valuable blocks. Optimize expected end-to-end cost under memory using candidate frequency, run size, media, true-positive mix, filter cache loads, block-cache displacement, and steady-state workload; canary and retain a bypass/rollback path.
