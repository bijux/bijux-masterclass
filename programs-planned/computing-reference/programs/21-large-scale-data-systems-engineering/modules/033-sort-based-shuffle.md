---
module_id: LSDS-033
program: Large-Scale Data Systems Engineering
level: 1
module_number: 33
title: Sort-Based Shuffle
status: complete
last_verified: 2026-09-03
---

# Sort-Based Shuffle

## One-Page Review

### Governing question

When should a shuffle producer organize output through sorting, and how can it form, spill, merge, index, publish, and consume sorted runs while preserving partition and key semantics under bounded memory, retries, skew, comparator changes, and storage failure?

### Essential definitions

- A **sort-based shuffle** groups shuffle output by sorting records or record pointers primarily by destination partition and optionally by key.
- A **sort key** is the tuple used for ordering, such as `(destination, user_key, tie_breaker)`.
- A **comparator** defines the ordering relation and must be compatible across producers, spills, merges, and consumers.
- A **sorted run** is an immutable sequence ordered by the pinned comparator.
- A **k-way merge** combines up to $k$ sorted runs into one sorted sequence using their current minimum elements.
- **secondary sort** extends the shuffle key so records grouped by a primary key arrive in a defined secondary order.
- **partition clustering** means records for each destination are contiguous; it does not necessarily mean records inside that destination are key-sorted.
- A **bypass path** groups directly by destination without merge sorting when ordering or map-side aggregation is unnecessary and destination count is suitably bounded.
- **sort stability** preserves input order among comparator-equal records; distributed shuffle does not provide it unless an explicit global tie-breaker is part of the contract.
- **comparison amplification** is comparator work caused by in-memory sorts and multi-pass merge beyond one inspection per record.

### Central model, mechanism, or theorem

For $N$ records and $S$ sorted spill runs, comparison sorting each balanced run costs approximately $O(N\log(N/S))$ total comparisons. A heap-based $F$-way merge costs $O(N\log F)$ per full merge pass, with about $\lceil\log_F S\rceil$ passes in a balanced plan. Disk I/O follows the spill model from [LSDS-032](032-map-side-buffering-and-spill.md): one initial write and, absent reuse or byte reduction, one read plus one write per full merge pass.

Correctness rests on a single compatible total-order contract. If each input run is sorted by comparator $\preceq$, repeatedly emitting the least current head yields a sorted output containing the multiset union of all inputs. Partition-first ordering makes each destination contiguous. Adding user key next makes equal keys contiguous inside a destination. Neither choice alone establishes a deterministic order among comparator-equal records.

### Critical invariants

- The partition function, comparator, schema, serializer, normalization, null/NaN/collation rules, and format are pinned by exchange identity.
- The comparator is deterministic and satisfies the required total-order properties for all admitted keys.
- Every in-memory run and completed spill is sorted under exactly that comparator.
- Merge emits each input record once, loses none, duplicates none, and preserves nondecreasing order.
- Destination boundaries in the final index match partition-first ordering and stored byte ranges.
- Combining groups only comparator-equivalent keys under an equality relation compatible with partitioning and reduction semantics.
- Attempt-scoped runs remain private until final data/index validation and winner publication.
- Memory, fan-in, input buffers, output buffers, file descriptors, and merge concurrency remain bounded.
- Comparator or serialization exceptions fail the attempt cleanly; they never publish a partially ordered result.
- Telemetry distinguishes partition clustering, key ordering, comparison CPU, spill/merge I/O, and downstream sort avoidance.

### Common failures

Common failures include claiming “sort shuffle” implies globally sorted output, sorting by key before destination so partitions are interleaved, using inconsistent hash/equality/comparator semantics, letting locale or library upgrades change ordering, treating NaN/null behavior as obvious, relying on unstable order for equal keys, comparing deserialized objects with nondeterministic state, opening all runs in one merge, using tiny fan-in and multiplying passes, applying an unsafe combiner during merge, bypassing sort when downstream needs ordering, publishing an index before the final merge is durable, mixing attempt runs, undercounting comparator or deserialization CPU, and tuning for record count while variable key width dominates memory.

### Compact example

Four individually sorted runs contain 6, 5, 4, and 3 keys. A heap-based four-way merge keeps one head per run, emits 18 keys in nondecreasing order, and uses bounded head memory plus output buffering. If records are ordered by `(partition,key)`, final partition counts of 5, 4, and 9 produce byte/index boundaries only after serialization; record counts alone cannot locate byte ranges. Comparator-equal records need an explicit tie-breaker such as stable source identity if reproducible order matters.

### Connections

[LSDS-023](023-partitioners-and-combiners.md) defines partition/equality and combiner contracts, [LSDS-031](031-shuffle-architecture.md) defines logical blocks and publication, and [LSDS-032](032-map-side-buffering-and-spill.md) defines buffers, runs, merge passes, and I/O amplification. [LSDS-034](../ROADMAP.md) contrasts hash-based shuffle, while [LSDS-037](../ROADMAP.md) uses ordered partitions for distributed sort-merge joins.

## Governing Question

A shuffle needs destination clustering: all bytes for reducer 0, then reducer 1, and so on, or an equivalent indexed physical layout. Sorting is one scalable way to build that grouping from a stream whose destinations arrive arbitrarily. It replaces many simultaneous partition writers with one bounded record/index structure and sequential spill runs.

Some consumers also need key ordering. Reduce-style grouping wants equal keys adjacent. Sort-merge join wants compatible ordered inputs. Secondary sort wants values for one group in a prescribed order. These stronger contracts change the comparator and can make the shuffle output reusable by downstream operators.

The governing question is which ordering the exchange truly needs and how to establish it using external-memory runs without confusing physical clustering with semantic global order. Correctness depends on comparator properties, partition compatibility, attempt identity, and merge completeness; performance depends on comparison cost, key representation, spill count, fan-in, disks, and downstream reuse.

## Why This Matters

Sort-based shuffle often reduces physical files and turns output into long sequential ranges. Compared with one writer per destination, it can bound buffers and file descriptors even when reducer parallelism is large. Sorted runs also make multi-pass merging natural and enable streaming grouped consumption.

Sorting is not free. Comparison may dominate CPU for complex or wide keys. Deserialization for comparison can allocate heavily. Multi-pass merge rereads and rewrites bytes. A comparator that consults locale, mutable state, current time, or inconsistent encodings can violate ordering or reproducibility.

The word “sort” is operationally ambiguous. Some engines sort only by destination index as a clustering technique; records within a destination remain unordered. Others order by destination and user key. SQL `ORDER BY` is a result-level semantic promise and usually requires range partitioning plus local ordering, not merely an internal sort-shuffle writer.

The design can remove downstream work when contracts align. If the final shuffle range is already ordered by the grouping or join key, the consumer may stream it. If comparator, null direction, collation, or partition boundaries differ, the apparent order is unusable and another sort is required.

## Prerequisites and Retrieval

Retrieve ordering, comparison sorting, heaps, external merge, serialization, partitions, and scale accounting from [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve immutable blocks, indexes, checksums, and metadata consistency from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review partitioners/combiners in [LSDS-023](023-partitioners-and-combiners.md), attempts/materialization in [LSDS-027](027-task-retry-and-speculation.md) and [LSDS-028](028-intermediate-data-materialization.md), tracing in [LSDS-030](030-tracing-a-batch-job-through-a-cluster-engine.md), and shuffle/buffering in [LSDS-031](031-shuffle-architecture.md) and [LSDS-032](032-map-side-buffering-and-spill.md). You should understand total orders, equivalence relations, stable sorting, heap operations, logarithms, multiway merge, byte indexes, and atomic publication.

## Learning Objectives

After this module, you should be able to:

1. distinguish destination clustering, per-partition key order, secondary order, and global result order;
2. specify comparator, equality, partitioning, normalization, null/NaN, collation, and tie-break contracts;
3. trace records through pointer sorting, run formation, spill, k-way merge, final indexing, and publication;
4. prove k-way merge preserves order and multiset contents under explicit assumptions;
5. estimate run-sort comparisons, merge comparisons, passes, and disk amplification;
6. choose merge fan-in using memory, descriptor, device, and comparison constraints;
7. evaluate bypass paths, prefix/radix techniques, combining, compression, and downstream sort reuse;
8. handle comparator exceptions, giant keys, skew, corruption, cancellation, retry, and speculation;
9. validate ordering and destination boundaries with adversarial fixtures and independent oracles; and
10. govern sensitive sort keys, temporary runs, collation metadata, access, retention, and deletion.

## Core Exposition

### Define the ordering promise first

Write the sort tuple explicitly. `(destination)` clusters partitions only. `(destination,user_key)` additionally orders keys within each partition. `(destination,primary_key,secondary_key)` supports secondary sort. A deterministic tie-breaker such as source snapshot, source partition, record offset, and stable record identity may extend the tuple when equal records need reproducible order.

Global ordering is different. Hash destinations have no monotonic relation, so concatenating reducers does not produce global key order. Range partitioning with nonoverlapping ordered boundaries plus local key ordering can do so, subject to boundary and comparator consistency.

Do not promise stability accidentally. Local stable sort preserves order from one input sequence, but distributed producers and retries have no single stable input sequence. Encode the desired tie-break semantics.

### Comparator contract

A sorting comparator must be deterministic and define a total preorder/order appropriate to the implementation. Informally, it needs consistent sign, transitivity, and total comparability for admitted values. Comparator equality must agree with any grouping equality used by the reducer, or explicitly define a coarser grouping comparator.

Partitioning must agree with grouping: keys that group together must reach the same destination. Hashing raw bytes while comparing normalized text can violate this. Normalize once under a pinned version or ensure hash/equality/comparison share semantics.

Specify ascending/descending directions, null placement, NaN behavior, signed zero, numeric overflow, timestamp/time-zone handling, string encoding, Unicode normalization, collation locale/version, case folding, and composite-field order. Reject unsupported values deterministically.

### Binary versus object comparison

Comparing serialized keys can avoid full object allocation and garbage collection. Fixed-width numeric prefixes, length-prefixed fields, or normalized byte encodings can support fast comparison. The binary ordering must exactly match the logical comparator.

Object comparison is simpler when user types already implement ordering but can allocate during decode and call arbitrary code. Protect the runtime from nontermination, exceptions, mutation, and side effects. Comparator code should be pure.

Prefix comparison or cached normalized keys can reject most comparisons cheaply, falling back to full keys on collisions. Account for prefix memory and ensure fallback preserves exact semantics.

### In-memory run formation

The producer emits serialized records into pages and appends compact pointers containing destination, key location/length, and record offset. When the buffer freezes, sort pointers rather than moving variable-size records. A sequential writer follows sorted pointers to emit destination-contiguous bytes.

Comparison sort is common, but destination indices may use counting/radix-style clustering. Fixed-width sortable prefixes may use radix passes. Algorithm choice must preserve the same declared tuple and remain within memory.

The buffer from [LSDS-032](032-map-side-buffering-and-spill.md) needs reserve for sort workspaces and worst-case comparator access. An in-place pointer sort uses less extra memory than copying records but still needs stack/work arrays depending on algorithm.

### Spill runs

Each spill run is independently sorted under one comparator identity. Its metadata includes attempt/exchange/run ID, comparator and serializer versions, min/max keys when safe, record/byte counts, destination ranges, checksum, codec/encryption, and completion state.

Runs are immutable after validation. A merge can trust order only after validating metadata and, where risk warrants, sampled or complete monotonicity. A checksum proves bytes were preserved, not that the comparator was correct.

Sensitive min/max keys should not appear in filenames or unrestricted telemetry. Store protected summaries or opaque digests when values reveal users or business data.

### K-way merge

Open at most $F$ runs, allocate a bounded input buffer for each, and place each current head in a min-heap keyed by the comparator. Remove the least head, emit it, advance that run, and reinsert its next head. Complexity is $O(N\log F)$ comparisons for one pass, with lower constants possible for specialized merge structures.

Correctness follows by induction. Initially each head is the least remaining element of its run. The least head across runs is therefore the least remaining element overall. Emitting it keeps output ordered; advancing exposes the next least of that run. When all runs exhaust, every input element was emitted exactly once.

This proof assumes every input is sorted, reads are complete, comparator results are consistent, and output failures do not masquerade as success. Validate those premises.

### Merge planning and fan-in

If $S>F$, merge in passes. Balanced grouping reduces maximum depth, while size-aware planning can avoid repeatedly rewriting a very large run alongside tiny runs. The final merge may directly produce the fetchable data/index, or consumers may merge multiple runs if the architecture supports it.

Large fan-in reduces pass count but consumes file descriptors, read buffers, heap entries, and random-read streams. On spinning disks, too many interleaved runs can destroy sequentiality. On SSDs, CPU/comparison or bandwidth may dominate. Choose from measured constraints.

Async prefetch can overlap I/O with comparison but needs bounded queues per input. A stalled run can block ordered output when its next key is unknown; speculative prefetch cannot skip it safely.

### Partition boundaries and indexes

With destination-first ordering, records for destination $j$ are contiguous. The writer records the byte offset at every destination transition and a final file length. Empty destinations have equal consecutive offsets. Block length is `offset[j+1]-offset[j]`.

Validate offsets are monotonic, begin at zero or declared base, end at file length, and match decoded destination membership. Record counts help reconciliation but cannot replace byte offsets under variable serialization/compression.

If compression uses independent destination frames, byte ranges remain directly fetchable. A compression stream spanning destinations can make random block access impossible unless indexes also identify restart points.

### Key grouping and combining

Sorted equal keys are adjacent, enabling streaming combine: retain one current key and aggregate as equal records arrive. This can reduce output without a large hash table. It works only if grouping equality and comparator equality align and the combiner algebra is safe.

The combiner may run per spill and during merge, so partial aggregate types must be serializable and comparable/groupable with raw mapped values under a defined representation. Changing key representation accidentally can break order.

Large single-key groups can make aggregate state large even though sorting is bounded. Use streaming algebra, spillable state, or explicit limits; sorting alone does not solve hot-key memory.

### Secondary sort

To deliver values for primary key $k$ ordered by secondary field $s$, partition by $k$, sort by `(k,s,tie_breaker)`, and group by $k$. The partitioner ignores $s$ so all group members meet. The grouping comparator ignores $s$, while the sort comparator includes it.

These relations must be compatible: if grouping says two keys are equal, partitioning must colocate them; sorting must place the group contiguously. The reducer then sees a group whose iteration order follows secondary keys, modulo explicit tie semantics.

### Bypass and adaptive paths

When there is no map-side aggregation and destination count is small, a writer may bypass merge sorting: append directly to destination buffers/files and later consolidate. This avoids comparison work but increases per-destination resources. Current engine thresholds are implementation choices, not universal constants.

Adaptive selection may consider $R$, expected output, key width, aggregation, disks, memory, and downstream ordering. Record the selected writer and format in physical plan identity so attempts do not mix incompatible outputs.

Bypass must not be chosen when downstream depends on key order. Partition clustering alone may suffice for an order-insensitive hash aggregation or transfer, but not for streaming group or sort-merge operators.

### Skew and comparator cost

Partition skew controls output range size and reducer tails. Key skew can also change producer sort cost: many equal prefixes can force expensive full-key comparisons; one giant key/group can stress combining. Variable-width keys change cache locality and decoded-object cost.

Measure comparisons, prefix fallbacks, comparator CPU, decoded bytes/allocations, run sizes, destination sizes, equal-key group sizes, merge depth, and time. A nominal $O(N\log N)$ statement does not explain constants or data-dependent behavior.

Use controlled heavy-hitter summaries and protected key hashes. Never place raw sensitive keys into metric labels or broad trace attributes.

### Failures, attempts, and compatibility

Comparator exception, nontransitivity detection, malformed key, disk failure, checksum error, or truncated run fails the attempt. Candidate runs remain in attempt-scoped storage. Retry uses the same exchange/comparator version or a new generation that invalidates old outputs.

Speculative attempts sort independently and may produce byte-different but semantically equivalent equal-key order when no tie-breaker is promised. Only the winner publishes. If reproducible bytes are required, the comparator tuple and serialization must fully determine order and encoding.

Engine/library/locale upgrades can change ordering. Persist comparator identifiers and compatibility, test old/new fixtures, and recompute rather than merge incompatible runs.

### Observability

Record records/bytes, key bytes, destination count, comparator identity, run count/sizes, sort algorithm, comparisons, prefix fallbacks, sort CPU/wall time, spill/merge reads/writes, passes, fan-in, file handles, input-buffer wait, compression, combine reduction, final block distribution, and bypass choice/reason.

Trace slow producer attempts through buffer freeze, sort, spill, merge groups, final index, checksum, and publication. Report p50/p95/p99 and maximum; one deep merge controls the stage tail. Separate user-key ordering from destination-only clustering in metadata and dashboards.

### Validation and adversarial testing

Use an independent oracle comparator on small fixtures. Include empty input, one record, already/reverse ordered data, all equal keys, duplicate composite keys, every destination empty/nonempty pattern, giant keys, invalid encodings, nulls, NaNs, signed zeros, Unicode normalization, locale changes, and boundary values.

Verify every run and final output is monotonic, contains the expected multiset, uses correct destination ranges, and yields correct groups. Randomized/property tests compare sorting/merge with a trusted in-memory result. Metamorphic tests change spill boundaries and fan-in without changing semantics.

Inject short reads/writes, corrupt index/data, missing runs, comparator exceptions, cancellation, disk-full, descriptor exhaustion, process death, retry, and speculation. Verify no partial publication, leak, deadlock, or cross-attempt mix.

### Security and governance

Sort keys and min/max summaries can reveal identities, amounts, locations, or ranks. Minimize stored metadata, encrypt spill/final files where required, scope access by tenant/run/attempt, and redact logs/traces. Treat custom comparator code as untrusted execution subject to review and resource controls.

Temporary runs require purpose-limited retention and deletion across disks, remote services, indexes, caches, and keys. A forensic hold must be explicit, authorized, audited, and expired. Deterministic tie-breakers should use scoped stable identity, not unnecessarily propagated personal identifiers.

## Definitions and Notation

Let records be ordered by comparator relation $\preceq_E$ pinned to exchange $E$. Let $N$ be total records, $S$ initial sorted runs, $F\ge2$ merge fan-in, and $P=\lceil\log_F S\rceil$ balanced full passes for $S>1$.

If balanced runs have $N/S$ records, their total comparison-sort work is approximately:

$$
S\,O((N/S)\log(N/S))=O(N\log(N/S)).
$$

One heap-based merge pass is $O(N\log F)$ comparisons and bounded head state $O(F)$ plus input/output buffers. Across $P$ full passes the simplified comparison bound is $O(PN\log F)$.

For destination-first order, index offsets $o_0,\ldots,o_R$ satisfy $0=o_0\le o_1\le\cdots\le o_R=L$, where $L$ is file length; destination block $j$ is byte range $[o_j,o_{j+1})$.

Comparator equality $a\sim_c b$ means neither compares below the other. Grouping equality may be coarser for secondary sort, but grouping-equivalent records must be contiguous and must share a destination.

## Mechanisms, Invariants, or Proof Structure

Audit a sort-based shuffle in this order:

1. Pin destination, key, secondary, tie-breaker, normalization, null/NaN, collation, equality, and comparator semantics.
2. Prove partitioning and grouping compatibility and distinguish partition clustering from local/global ordering.
3. Choose binary/object/prefix comparison and charge key, pointer, sort, and decode memory.
4. Form immutable individually sorted runs under one exchange/comparator identity.
5. Plan bounded merge fan-in/passes from memory, descriptors, disks, and run sizes.
6. Prove k-way merge order and multiset preservation; validate every premise.
7. Build and validate destination byte boundaries, frames, checksums, and attempt-scoped publication.
8. Validate combining, secondary sort, bypass, and downstream order reuse against explicit contracts.
9. Test comparator compatibility, failure, cancellation, retry, speculation, and upgrade boundaries.
10. Measure comparison/I/O/tail behavior and review key sensitivity, retention, and deletion.

The k-way merge proof is inductive: current heads are minima of their own remaining runs, so the least head is the global least remaining record. Emitting it preserves order and advances exactly one input. Termination after all inputs exhaust establishes multiset equality and sortedness.

Partition contiguity follows when destination is the first sort component. All records with smaller destination compare first and all with larger destination compare later. Equal consecutive offsets represent empty partitions. This does not prove key order unless key is the next component.

Determinism is stronger than sortedness. A comparator can consider two records equal, allowing different valid orders. Reproducible byte output requires a total tie-break plus deterministic serialization, spill/merge behavior or an output definition invariant to equivalent-order variation.

## Alternatives and Trade-Offs

**Destination-only versus destination-plus-key sort.** Destination-only clustering reduces comparison work. Key sorting enables streaming groups/joins at higher CPU and key-memory cost.

**Comparison versus radix/prefix sorting.** Comparison supports general keys. Radix/prefix methods exploit encodings but require exact semantic compatibility and fallback.

**Binary versus object comparator.** Binary comparison avoids allocation; object comparison is expressive. Encoding bugs and arbitrary user code are their respective risks.

**Stable versus explicit tie-break ordering.** Local stability is cheap but not a distributed promise. Explicit stable identity creates reproducibility at wider keys and possible privacy cost.

**Large versus small fan-in.** Large fan-in reduces passes while consuming descriptors/buffers and random reads. Small fan-in bounds resources but amplifies I/O.

**Sort writer versus bypass writer.** Sorting scales to many destinations and order needs. Bypass avoids comparisons for bounded destinations but multiplies writers/resources.

**Producer combine versus reducer-only aggregation.** Sorted adjacency enables streaming combine and byte reduction. It is useful only with safe algebra and sufficient reduction.

**Persist sorted outputs versus recompute.** Retention may accelerate retries/downstream reuse but increases storage, sensitive-data lifetime, and compatibility obligations.

## Failure Modes and Misconceptions

**“Sort shuffle means globally sorted data.”** Global order needs ordered partition ranges plus local order; hash destinations do not compose globally.

**“Destination clustering means keys are sorted.”** An engine may sort only partition indices.

**“A comparator that usually works is sufficient.”** Rare transitivity, null, NaN, normalization, or version errors can corrupt arbitrary merges.

**“Stable local sort preserves input order globally.”** Producer concurrency and retry have no shared input sequence.

**“Checksums validate ordering.”** They validate byte integrity, not comparator semantics or monotonicity.

**“More fan-in always reduces time.”** Descriptor, buffer, cache, and random-I/O costs can dominate.

**“The heap contains all records.”** A k-way merge needs current heads plus bounded buffers, not full inputs.

**“Secondary sort partitions by the complete sort key.”** It normally partitions/groups by the primary key while sorting by the extended key.

**“Bypass is always equivalent.”** It is invalid when consumers rely on key ordering or merge-time combination.

**“Equal-key order is deterministic.”** Comparator equality permits multiple valid orders without a tie-breaker.

**“Sorted spills from different versions can merge.”** Comparator/normalization/serialization compatibility must be proven.

**“Sort cost is only disk I/O.”** Comparisons, key decode, allocation, cache behavior, and merge coordination can dominate.

## Worked Examples

### Example 1

Sorting by `(destination,key)` produces destination ranges and key order within each reducer. Sorting by `(key,destination)` can interleave destinations and cannot produce one contiguous block per reducer without another grouping step.

### Example 2

Two strings compare equal after case folding but hash differently as raw UTF-8. They may reach different reducers and never group. Hash and comparator must share the normalization/equality contract.

### Example 3

Four sorted runs merge with a heap of at most four heads. After emitting one head, only that run advances. The algorithm does not load all 18 fixture keys into merge memory.

### Example 4

Offsets `(0, 120, 120, 500)` describe three destinations: 120 bytes, empty, and 380 bytes. Equal offsets are valid; decreasing offsets or a final offset different from file length are corruption.

### Example 5

For secondary sort by event time within user, partition and group by user but sort by `(user,event_time,event_id)`. The event ID resolves equal timestamps reproducibly without depending on arrival order.

### Example 6

One comparator reads the process locale and another worker uses a different locale. Individually sorted runs may be mutually incompatible. Pin collation data/version or use a locale-independent normalized encoding.

### Example 7

Sixty-four runs with fan-in eight need two balanced passes. Fan-in 64 uses one pass but needs 64 input buffers and descriptors per merge, possibly across many concurrent tasks.

### Example 8

A destination-only bypass path is safe for an order-insensitive downstream hash aggregation with no map-side combination. It is unsafe for a reducer API promising sorted keys.

### Example 9

Two speculative attempts contain the same records but differ in equal-key order. Both are semantically sorted when no tie-breaker is promised; only the winner publishes. Byte equality cannot be assumed.

### Example 10

This fixture performs a heap-based k-way merge and verifies order and multiset size. It models integer keys, not byte indexes, spill I/O, attempts, or comparator failure.

<!-- bijux-verify: {"id":"sorted-run-merge","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"runs=4 input_records=18 output_records=18\nmerged=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)\nnondecreasing=True\n","stderr":""}} -->
```python
from heapq import merge


runs = (
    (1, 5, 7, 12, 16, 18),
    (2, 4, 9, 13, 17),
    (3, 8, 11, 15),
    (6, 10, 14),
)
output = tuple(merge(*runs))
nondecreasing = all(left <= right for left, right in zip(output, output[1:]))
print(
    f"runs={len(runs)} input_records={sum(map(len, runs))} "
    f"output_records={len(output)}"
)
print(f"merged={output}")
print(f"nondecreasing={nondecreasing}")
```

## Cross-Program Connections

- **Algorithms:** comparison sorting, heaps, radix techniques, k-way merge, stability, lower bounds, and external-memory analysis provide the core machinery.
- **Data structures:** compact pointers, pages, tournament/heap structures, indexes, prefixes, and streaming groups determine constants.
- **Databases:** external sort, `ORDER BY`, grouping, secondary indexes, sort-merge join, and physical properties reuse ordered partitions.
- **Distributed systems:** partition compatibility, attempts, generations, retries, speculative winners, and failure domains preserve exchange correctness.
- **Storage systems:** sequential runs, range indexes, checksums, compression frames, file descriptors, and multi-pass I/O shape physical behavior.
- **Programming languages:** comparator purity, object layout, serialization, Unicode, floating-point edge cases, and library versioning affect semantics.
- **Performance engineering:** comparison counts, merge depth, key width, cache locality, I/O amplification, skew, and tails guide choices.
- **Security:** keys and min/max summaries can reveal sensitive ordering; scoped identity, encryption, redaction, and deletion limit exposure.
- **Testing:** property, metamorphic, differential, fault-injection, and compatibility tests are essential because rare keys can violate order.
- **Governance:** collation and tie-break decisions can change visible rankings and require domain review when outcomes affect people.

## References

1. Jeffrey Dean and Sanjay Ghemawat, [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), 2004.
2. Apache Hadoop, [MapReduce Tutorial: Shuffle, Sort, Comparators, and Secondary Sort](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html), accessed 2026-09-03.
3. Apache Hadoop, [MapReduce Default Configuration](https://hadoop.apache.org/docs/stable3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml), accessed 2026-09-03.
4. Apache Spark, [Configuration: Sort-Based Shuffle](https://spark.apache.org/docs/latest/configuration.html), accessed 2026-09-03.
5. Apache Spark, [RDD Programming Guide: Shuffle Operations](https://spark.apache.org/docs/latest/rdd-programming-guide.html), accessed 2026-09-03.
6. Apache Spark, [Tuning Guide](https://spark.apache.org/docs/latest/tuning.html), accessed 2026-09-03.
7. Apache Spark, [SQL Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html), accessed 2026-09-03.
8. Apache Flink, [Batch Shuffle: Sort Shuffle](https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/ops/batch/batch_shuffle/), accessed 2026-09-03.
9. Apache Flink, [ExternalSorter API](https://nightlies.apache.org/flink/flink-docs-release-2.2/api/java/org/apache/flink/runtime/operators/sort/ExternalSorter.html), accessed 2026-09-03.
10. Apache Flink, [Configuration](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/), accessed 2026-09-03.
11. Apache Flink, [ORDER BY Clause](https://nightlies.apache.org/flink/flink-docs-stable/docs/sql/reference/queries/orderby/), accessed 2026-09-03.
12. Dask, [Shuffling Performance](https://docs.dask.org/en/latest/dataframe-groupby.html), accessed 2026-09-03.

## Exercises

### Exercise 1

Define sort, partition, and grouping contracts for secondary sorting purchases by `(customer, timestamp, purchase_id)` while reducers group by customer. State the required compatibility properties.

### Exercise 2

A producer has 1,000,000 records, 20 equal-sized initial runs, and merge fan-in five. Estimate balanced merge passes and asymptotic comparison work for initial run sorting and merging. Explain why the estimates may miss runtime.

### Exercise 3

Prove the heap-based k-way merge outputs a sorted multiset union. List every implementation premise that the mathematical proof assumes.

### Exercise 4

Design an adversarial comparator and index test suite covering numeric, text, null, floating-point, composite, corruption, attempt, and upgrade cases.

### Exercise 5

Choose between sort and bypass writers for three cases: 40 destinations with no combine/order need; 20,000 destinations with reducer key-order promise; and 200 destinations with safe high-reduction streaming combine. Justify what must be measured.

## Answers to the Exercises

### Answer 1

Partition by normalized customer only so every purchase for one customer reaches one reducer. Sort by `(normalized_customer, timestamp, purchase_id)` using pinned ascending/null/time-zone and identifier semantics. Grouping compares only normalized customer. Grouping-equivalent records must hash/partition identically; the full sort must place each customer group contiguously; timestamp and purchase ID establish deterministic within-group order. Pin schema, normalization/collation, serializer, comparator version, and malformed/null policy. If purchase IDs are not unique, add a stable scoped record identity or decline to promise order among complete ties.

### Answer 2

$P=\lceil\log_5 20\rceil=2$. Balanced initial run size is 50,000, so total initial comparison work is approximately $O(1{,}000{,}000\log 50{,}000)$. Two full heap-merge passes cost approximately $O(2\times1{,}000{,}000\log5)$. Constants depend on key width, prefix success, comparator/decode/allocation, data order, equality frequency, cache, sort implementation, uneven runs, combining, async I/O, compression, disks, and whether the final merge or partial groups avoid a full pass.

### Answer 3

Each run head is its least unconsumed element. The least head across all runs is therefore the least unconsumed element globally. Emit it and advance exactly its run; the remaining heads again satisfy the invariant. Induction yields nondecreasing output, and exhaustion after one advance per element yields the exact multiset union. Premises include individually sorted complete inputs, one consistent deterministic comparator, total comparability, correct heap ordering, exact-once head advancement, no read omission/duplication/corruption, sufficient error propagation, correct termination, immutable inputs, and successful output writes. Attempt/generation selection is an external premise too.

### Answer 4

Test minima/maxima/overflow-adjacent integers, decimals and numeric scale, negative/positive zero, infinities, multiple NaNs, null placement, empty/long strings, invalid UTF-8, canonically equivalent Unicode, case folding, locale/collation versions, timestamps/time zones, nested/composite prefix ties, and identical full keys. Check sign symmetry, transitivity, totality, equality/hash/partition compatibility, stable tie policy, and binary-versus-object differential results. Verify sortedness and multiset equality across randomized spill boundaries/fan-in. Corrupt data/index/offsets, omit/duplicate runs, throw comparator exceptions, cancel, retry, speculate, and compare old/new library and schema versions. No failing case may publish.

### Answer 5

For 40 destinations without combine or order, bypass may avoid comparison at bounded writer/buffer/file cost; measure output size, descriptors, disk pattern, and consolidation. For 20,000 destinations with key-order promise, destination-plus-key sort is appropriate because bypass resources scale poorly and cannot meet order without another sort; measure key/comparator CPU, runs, fan-in, and tails. For 200 destinations with a high-reduction safe combine, sort enables streaming equal-key combination, though hash aggregation could be compared; measure distinct keys, reduction ratio, aggregate memory, comparator versus hash cost, spill, output, and skew. Engine thresholds are inputs, not the decision itself; correctness contracts dominate.
