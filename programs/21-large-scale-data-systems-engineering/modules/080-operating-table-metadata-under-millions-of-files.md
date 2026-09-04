---
module_id: LSDS-080
program: Large-Scale Data Systems Engineering
level: 2
module_number: 80
title: Operating Table Metadata Under Millions of Files
status: complete
last_verified: 2026-09-04
---

# Operating Table Metadata Under Millions of Files

## One-Page Review

### Governing question

How can a table containing millions of live and historical files remain plannable, committable, observable, and recoverable without listing storage, materializing its entire metadata graph, trusting stale indexes, or letting small-file and snapshot churn overwhelm the control plane?

### Essential definitions

- A **metadata root** is the immutable snapshot-scoped entry point resolved by the catalog.
- A **manifest list** is a snapshot-level index of manifests and their partition/file summaries.
- A **manifest** records a bounded cohort of data or delete files plus partitions, metrics, and lineage.
- **hierarchical pruning** rejects metadata containers before reading their children.
- **planning amplification** is metadata bytes or entries processed per selected data byte/file.
- **metadata compaction** rewrites equivalent metadata into better-sized or better-clustered containers.
- **metadata debt** is avoidable planning, commit, retention, or recovery cost caused by accumulated metadata shape.
- A **snapshot-scoped cache** keys derived metadata by immutable root, snapshot, schema/spec, and reader semantics.
- **authoritative inventory** is the snapshot graph; object-store listing is a diagnostic input, not membership truth.
- A **planning budget** bounds metadata bytes, requests, entries, memory, concurrency, and elapsed time.

### Central model, mechanism, or theorem

For snapshot $s$, let manifest list $L_s$ reference manifests $M_s$. Query predicate $q$ first selects

$$M_q=\{m\in M_s:summary(m)\not\perp project(q,spec_m)\},$$

then selects files $F_q$ from only those manifests using partition and file metrics. Correct pruning is conservative: unknown, truncated, incompatible, or missing summaries remain candidates. Planning work is proportional to the selected metadata frontier, not necessarily total files, when summaries are useful. Operators control frontier size through bounded manifests, locality-aware grouping, incremental writes, snapshot expiration, index maintenance, and streaming/parallel readers while preserving one pinned snapshot and deterministic results.

### Critical invariants

- Every plan begins from one catalog-resolved immutable metadata root and one pinned snapshot/reference.
- Manifest-list and manifest pruning has no false negatives; unknown evidence selects rather than rejects.
- File identity, content type, schema ID, partition-spec ID, sequence, metrics semantics, and checksum survive metadata rewrites.
- Data and delete applicability is planned together; optimizing one side never drops required deletes.
- Planning memory is bounded through projection, streaming, batching, spill, or backpressure rather than assumed proportional to cluster RAM.
- Caches bind immutable snapshot/root and interpretation version; mutable aliases never key correctness-bearing entries alone.
- Metadata compaction preserves the exact live entry multiset and snapshot semantics and publishes atomically.
- Snapshot/metadata cleanup is reachability-based and respects branches, tags, leases, unknown commits, and retention.
- Listing discrepancies trigger reconciliation; they do not silently add or remove table membership.
- SLOs separate catalog resolution, root load, manifest pruning, file pruning, delete pairing, and final task creation.

### Common failures

Common failures include recursively listing a warehouse to plan queries; loading every manifest and file entry into driver memory; assuming millions of files require millions of object requests; pruning on truncated or NaN bounds unsafely; mixing partition specs without per-manifest projection; caching by table name only; losing delete files during manifest rewrite; merging manifests into giant serial bottlenecks; creating one manifest per microbatch forever; expiring snapshots while branches or unknown commits still reference them; treating object count as metadata bytes; hiding planner OOMs behind higher memory; and benchmarking warm cache while production misses are cold and concurrent.

### Compact example

A snapshot has five manifests covering partition-day ranges and 440,000 file entries. Query days 18–22 overlaps only two manifest summaries containing 210,000 entries. The planner reads 160 MiB of 340 MiB manifest metadata, then file metrics reduce the final task set further. The first-level reduction is 52.9% of manifest bytes, not a promise about data bytes. If a bound is missing or truncated ambiguously, that manifest remains selected. Regrouping manifests by day may improve future pruning without changing any table row.

### Connections

[LSDS-066](066-vectorized-execution-at-cluster-scale.md) supplies memory-aware execution, [LSDS-068](068-adaptive-query-execution.md) supplies feedback, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies pinned roots, [LSDS-072](072-manifest-and-metadata-trees.md) supplies hierarchy, [LSDS-076](076-compaction-planning.md) supplies rewrite economics, [LSDS-077](077-file-clustering-and-ordering.md) supplies locality, and [LSDS-079](079-catalog-and-transaction-coordination.md) supplies authority.

## Governing Question

At small scale, opening every footer or listing every partition can look acceptable. At millions of files, metadata becomes its own distributed workload: many objects, request throttling, driver heaps, serialization, caches, retries, catalog traffic, and maintenance commits. A query can fail before reading one data row.

Modern table formats replace recursive listing with versioned indexes. The root identifies a snapshot; a manifest list summarizes manifests; manifests summarize files; optional indexes add statistics. This changes the scaling question from “how many files exist?” to “how much of the metadata frontier must this operation inspect, and under which correctness rules?”

The governing question is how to keep that frontier bounded and useful across ingestion, queries, deletes, evolution, retention, cold starts, concurrent planners, and disaster recovery while preserving exact snapshot membership.

## Why This Matters

Metadata planning lies on every query's critical path. High p99 latency delays interactive work, batch starts, streaming recovery, compaction, and commits. Driver OOMs and request storms can take down shared catalogs or object stores. Small files harm both data execution and metadata density.

The same graph controls correctness. A missing data entry loses rows; a missing delete entry resurrects them; an extra historical entry duplicates data; stale partition semantics mis-prune; premature cleanup destroys time travel. Performance changes must therefore prove semantic equivalence rather than merely reduce object counts.

Operationally, metadata has capacity, cost, freshness, availability, confidentiality, and recovery needs. File paths, bounds, counts, partitions, and access patterns may be sensitive. A platform needs explicit ownership and SLOs for this control plane.

## Prerequisites and Retrieval

Review vectorized execution memory in [LSDS-066](066-vectorized-execution-at-cluster-scale.md), adaptive feedback in [LSDS-068](068-adaptive-query-execution.md), atomic roots in [LSDS-071](071-table-snapshots-and-atomic-commit.md), manifest graphs in [LSDS-072](072-manifest-and-metadata-trees.md), compaction in [LSDS-076](076-compaction-planning.md), clustering in [LSDS-077](077-file-clustering-and-ordering.md), deletes in [LSDS-078](078-deletion-vectors-and-row-level-changes.md), and catalogs in [LSDS-079](079-catalog-and-transaction-coordination.md).

You should understand immutable DAGs, manifests, partition transforms, conservative bounds, tri-valued reasoning, column metrics, object-store requests, pagination, streaming iterators, backpressure, cache keys, checksums, snapshots, branches, OCC, compaction, garbage collection, and percentile SLOs.

For diagnosis retain root/snapshot/reference, manifest-list identity/size, manifest count/bytes/entry counts, selected and rejected summaries with reasons, schema/spec/sequence IDs, delete-pair counts, request/byte/latency traces, concurrency, cache keys/hits/age, heap/spill/GC, task counts, and maintenance/reachability history.

## Learning Objectives

After this module, you should be able to:

1. Explain why snapshot indexes replace storage listing as membership authority.
2. Model two-level manifest and file pruning without false negatives.
3. Budget planning by requests, bytes, entries, memory, concurrency, and latency.
4. Stream, batch, parallelize, cache, and spill metadata safely.
5. Preserve schema/spec/sequence/delete semantics across mixed metadata cohorts.
6. Diagnose small manifests, giant manifests, stale statistics, and driver bottlenecks.
7. Rewrite metadata with equivalence, OCC, and atomic-publication proofs.
8. Operate snapshot expiration and orphan cleanup from reachability.
9. Design cold/warm, selective/full-scan, and concurrent planning experiments.
10. Define capacity, cost, security, recovery, and planning SLO evidence.

## Core Exposition

### Metadata hierarchy as an index

Resolve catalog pointer, load table metadata, select a snapshot/reference, read its manifest list, prune manifests, read selected manifests, prune entries, pair data with applicable deletes, and emit scan tasks. Each level should remove work using conservative summaries before descending.

The manifest list stores per-manifest counts and partition summaries. Each manifest stores file partition tuples and column metrics. Different formats implement different trees or metadata tables, but the durable idea is indexed authoritative membership rather than recursive discovery.

### Conservative two-level pruning

Project a row predicate through each manifest's partition spec. Reject a manifest only when its complete compatible summary proves disjointness. For selected manifests, reject a file only when partition/column evidence proves it cannot match. Null, NaN, collation, timestamp zone, decimal scale, truncation, schema evolution, and transform semantics belong in that proof.

Unknown does not mean empty. Missing bounds, obsolete metrics, encrypted/unavailable indexes, or unsupported transforms produce candidates. Record pruning reason codes so false-negative investigations can reconstruct decisions.

### Snapshot and evolution cohorts

Pin one root before planning and keep it throughout the plan. Manifests may use different partition specs and schemas. Interpret each with its stored IDs; project the query separately. Never reinterpret an old partition tuple using today's spec or compare incompatible bounds as if encodings matched.

Plan data and delete manifests under their sequence/applicability rules. Parallel workers receive the same immutable context and return deterministic entry batches. A head change after pinning does not mutate the query's snapshot.

### Bounded memory and concurrency

Project only required manifest fields. Iterate pages/blocks, emit bounded batches, and release decoded objects. Use a memory budget for entries, decoded strings, metric maps, delete-pair state, and task buffers; spill deterministic intermediates to `artifacts/`-equivalent managed scratch when needed.

Parallelism hides latency but can overwhelm object storage, catalog, network, heap, or CPU. Use separate bounded pools, request-rate limits, byte permits, cancellation, per-tenant fairness, and adaptive concurrency. Preserve stable task identity/order only where consumers require it.

### Metadata shape and write path

Fast appends can add manifests without rewriting old ones, keeping commits cheap. High-frequency microbatches may create many tiny manifests; oversized manifests reduce request count but increase unavoidable bytes and serial decode. Target sizes are workload-dependent.

Group manifests by partition/spec/content and common pruning dimensions. Writers should roll bounded manifests, reuse valid existing manifests, merge when thresholds justify it, and publish summary counts. Backpressure or aggregate commits when write cadence creates metadata faster than maintenance can normalize it.

### Metadata compaction

Select exact input manifests at a base snapshot, read every live entry, optionally regroup, write new manifests and list, verify entry multiset and metadata fields, validate inputs/current semantics, and atomically publish. Data files need not be rewritten.

Track benefit as reduced requests/bytes/latency for representative plans, not merely fewer manifests. One enormous replacement can worsen selective queries. Preserve data/delete separation, spec cohorts, sequence inheritance, file status, statistics, key metadata, and provenance.

### Caching and locality

Immutable objects are excellent cache keys: catalog identity plus table UUID, metadata path/checksum, snapshot, manifest path/length, schema/spec interpretation, and reader version. Cache raw bytes separately from decoded objects. Bound memory, validate integrity, coalesce concurrent misses, and use negative caching carefully.

Warm caches can hide poor metadata shape; cold caches reveal object-request cost. Locate shared caches near compute only after addressing correctness, tenancy, encryption, and eviction. Mutable table names or `latest` pointers must be resolved before accessing immutable cache entries.

### Auxiliary indexes and metadata tables

Partition statistics, column-statistics indexes, bloom filters, metadata tables, and server-side scan planning can reduce footer and manifest work. They are derived and snapshot/version scoped. Each needs build lag, coverage, schema, integrity, compatibility, and fallback semantics.

An index may reject only within its proven coverage. Missing or stale shards select candidates. Compare index maintenance bytes and commit latency with saved planning/data bytes. An index whose own files explode recreates the same metadata problem one level higher.

### Retention and garbage collection

Historical snapshots, branches, tags, streaming checkpoints, legal holds, and unknown commits keep metadata and data reachable. Expire references/snapshots according to policy, then compute reachability before deleting objects. Metadata-log length and snapshot count are different controls.

Orphan cleanup compares authoritative reachability with storage inventory after a safety horizon. Listing is useful here, but eventual visibility and active staged writes require age, ownership, and unknown-outcome protection. Never derive current membership by deleting whatever is absent from a listing.

### Capacity, security, and recovery

Forecast live/historical file entries, manifests, snapshots, branches, metadata bytes, commit rate, planning concurrency, request rate, cache size, and maintenance throughput. Budget burst and cold-start behavior. Quotas need tenant/operation fairness so one full scan cannot starve all selective plans.

Encrypt and authorize metadata like data; paths, partitions, bounds, counts, delete patterns, and predicates leak information. Back up catalog roots and required encryption/policy state. Recovery walks each restored root, verifies checksums and referenced objects, samples full plans, and tests a conditional commit.

### Measurement and SLOs

Instrument catalog/root/list/manifest/file-filter/delete-pair/task-create stages. Record total/selected manifests and entries, metadata requests/bytes, pruning ratios by level, cache state, retries/throttles, heap/GC/spill, planner CPU, output tasks/data bytes, and end-to-end percentiles.

Benchmark point/range predicates, no-match, full scans, evolved specs, many deletes, cold/warm cache, concurrent tenants, throttling, corrupt objects, and unavailable indexes. Report logical result equality separately from speed. SLOs should bind table cohort and plan class; a single fleet median conceals pathological tables.

## Definitions and Notation

Let:

- $s$ be a pinned snapshot and $L_s$ its manifest list;
- $M_s$ be manifests referenced by $L_s$;
- $F_s$ and $D_s$ be live data and delete-file entries;
- $q$ be a query predicate and $project(q,spec_m)$ its partition projection;
- $M_q\subseteq M_s$ and $F_q\subseteq F_s$ be selected manifests and files;
- $B_L,B_M,B_I$ be manifest-list, manifest, and auxiliary-index bytes read;
- $N_M,N_F,N_T$ be manifests, file entries, and emitted tasks processed;
- $R_o$ be metadata object requests and $H$ peak planning heap bytes;
- $A_m=(B_L+B_M+B_I)/B_{selected\ data}$ be byte planning amplification when the denominator is nonzero;
- $P_M=1-|M_q|/|M_s|$ be manifest-count prune fraction;
- $P_B=1-B_{M_q}/B_{M_s}$ be manifest-byte prune fraction;
- $\lambda_w$ and $\mu_c$ be metadata creation and compaction service rates.

Count and byte ratios answer different questions. A full scan legitimately has $P_M=0$ while remaining healthy. When $\lambda_w>\mu_c$ for sustained periods, debt grows; burst queues still need time-window and backlog units. Latencies require cache state and concurrency labels.

## Mechanisms, Invariants, or Proof Structure

### Hierarchical-pruning proof

If summary predicate $S_m$ is conservative, $S_m\perp q$ implies no child entry can match. Therefore rejecting only proven-disjoint manifests preserves all matches. Applying the same rule to complete compatible file metrics preserves matching files. Any unknown remains selected, so uncertainty increases work rather than causing row loss.

### Streaming-memory argument

With batch size $b$, bounded decoded entry size $e$, bounded delete state $d$, and bounded task buffer $t$, planner working memory is $O(be+d+t)$ rather than $O(|F_s|)$. This depends on consumers honoring backpressure and caches not retaining every decoded object.

### Metadata-rewrite equivalence

Let $E(I)$ and $E(O)$ be normalized live entry multisets for selected input and output manifests, including content type, identity, partition/spec, sequence, metrics, and status. Require $E(I)=E(O)$ and unchanged applicability under snapshot rules. Conditional atomic replacement then changes physical metadata shape without changing table results.

### Queue-stability argument

If average metadata production exceeds sustainable compaction, backlog diverges. Stability requires lowering creation, increasing service, or accepting a bounded retention policy. Averages alone are insufficient: provision burst capacity and track oldest-item age, since small steady backlog can hide one starved cohort.

### Adversarial verification

Test empty and full scans, missing/truncated bounds, null/NaN, mixed schemas/specs, data/delete manifests, giant and tiny manifests, corrupt checksums, duplicate/missing entries, cold cache, thundering herd, cancellation, throttling, partial index coverage, concurrent rewrite, branches/tags, unknown commits, and orphan listing lag. Verify exact results or explicit failure and bounded resources.

## Alternatives and Trade-Offs

**Recursive listing** needs little format metadata but scales poorly and cannot identify snapshot membership safely. **Manifest trees** give authoritative versioned membership and pruning but require maintenance and compatible readers. **Metadata tables/services** centralize listings and indexes but introduce their own freshness and availability contracts.

**Small manifests** enable selective reads and cheap replacement units but increase objects and per-request overhead. **Large manifests** amortize requests but increase unavoidable decode and tail latency. **Locality grouping** improves common predicates but may worsen others and costs rewrites.

**Single-node planning** avoids a distributed bootstrap and can be fast with strong pruning. **Distributed planning** increases capacity for full scans but adds scheduling, shuffle, duplicate work, and coordinator complexity. Use evidence from the selected frontier.

**Client caches** are simple and tenant-local. **Shared caches** improve reuse but require isolation, eviction, encryption, and failure control. **Server-side planning** can hide metadata topology and vend minimal tasks but concentrates compute and protocol coupling.

**Eager index maintenance** improves freshness but extends write latency. **Asynchronous indexes** protect writes but require coverage watermarks and conservative fallback.

## Failure Modes and Misconceptions

1. **Millions of files require listing millions of objects.** Indexed snapshot membership avoids that.
2. **Manifest count equals planning cost.** Bytes, entries, requests, cache, and selectivity matter.
3. **Fewer manifests is always better.** Giant manifests harm selective plans.
4. **Unknown bounds mean no match.** They must remain candidates.
5. **Current spec interprets old partitions.** Each manifest carries its spec identity.
6. **Data pruning can ignore deletes.** Missing applicable deletes resurrect rows.
7. **More planner threads always help.** Dependencies throttle and heaps saturate.
8. **A larger driver fixes scaling.** Unbounded materialization still fails.
9. **Cache by table name is safe.** Rename/head movement makes it ambiguous.
10. **Warm benchmark represents production.** Cold starts and churn need separate evidence.
11. **Metadata rewrite is cosmetic.** It must preserve every correctness field.
12. **Compaction should run at one global threshold.** Workloads and costs differ.
13. **Auxiliary index is authoritative.** Coverage and freshness may be partial.
14. **Snapshot expiration immediately frees bytes.** Reachability and cleanup follow.
15. **Storage listing defines live files.** The snapshot graph defines membership.
16. **Orphan means old.** Active or unknown attempts may also be old.
17. **Median planning latency is sufficient.** Tails and table cohorts expose failure.
18. **Metadata is nonsensitive.** Paths, bounds, and access patterns can leak data.

## Worked Examples

### Example 1

Five manifests contain 440,000 entries. A date predicate selects two containing 210,000. File-count pruning at the manifest level is $(1-210/440)\times100\approx52.27\%$; this is not data-byte pruning.

### Example 2

A string upper bound is truncated to `mar`. Predicate `market='mars'` cannot safely reject the file unless the format's truncation ordering proves disjointness. Otherwise it remains selected.

### Example 3

Snapshot has spec 1 manifests partitioned by day and spec 2 by hour. The same timestamp predicate is projected independently under each spec; decoding both as hour is wrong.

### Example 4

Planner processes 10,000-entry batches and emits tasks to a bounded queue. A slow consumer blocks producers, keeping heap bounded rather than accumulating all two million entries.

### Example 5

One thousand 100-KiB manifests cost many requests. Rewriting them into 10-MiB cohorts can reduce requests, but grouping unrelated partitions might increase selective bytes. Measure both.

### Example 6

Cache entry keyed only by `db.t` returns snapshot 80 after head advances to 81. Keying decoded content by immutable metadata path permits reuse while fresh resolution chooses the correct root.

### Example 7

Column-statistics index covers snapshots through 900; query pins 905. It may prune covered files, but files added in 901–905 require manifest/file evidence and cannot be assumed absent.

### Example 8

Branch `audit` retains snapshot 400 after `main` expires it. Reachability keeps its manifests and data; main-branch age alone cannot authorize deletion.

### Example 9

Writers create 80 small manifests/minute while maintenance sustains 50. Debt grows 30/minute until ingestion aggregates commits or maintenance capacity rises.

### Example 10

The executable fixture recomputes first-level manifest selection and byte reduction.

<!-- bijux-verify: {"id":"manifest-frontier","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"manifests_total=5\nmanifests_selected=2\nfiles_indexed=440000\nfiles_considered=210000\nmetadata_bytes_total=340\nmetadata_bytes_read=160\nreduction_percent=52.9\n","stderr":""}} -->
```python
manifests = [
    (0, 9, 100_000, 80),
    (10, 19, 120_000, 90),
    (20, 29, 90_000, 70),
    (30, 39, 80_000, 60),
    (40, 49, 50_000, 40),
]
query_low, query_high = 18, 22
selected = [m for m in manifests if not (m[1] < query_low or m[0] > query_high)]
total_bytes = sum(m[3] for m in manifests)
read_bytes = sum(m[3] for m in selected)

print(f"manifests_total={len(manifests)}")
print(f"manifests_selected={len(selected)}")
print(f"files_indexed={sum(m[2] for m in manifests)}")
print(f"files_considered={sum(m[2] for m in selected)}")
print(f"metadata_bytes_total={total_bytes}")
print(f"metadata_bytes_read={read_bytes}")
print(f"reduction_percent={100 * (1 - read_bytes / total_bytes):.1f}")
```

## Cross-Program Connections

- **Data structures:** B-trees, LSM trees, Bloom filters, compressed bitmaps, DAGs, and iterators inform metadata indexes.
- **Database systems:** catalogs, statistics, MVCC, vacuum, buffer pools, and query optimizers expose analogous control-plane costs.
- **Distributed systems:** immutable snapshots, consistency, throttling, queues, retries, and reachability govern correctness.
- **Operating systems:** paging, working sets, readahead, file descriptors, and backpressure guide bounded planners.
- **Platform engineering:** SLOs, quotas, tenant fairness, cache fleets, capacity, and incident response operate planning.
- **Security engineering:** encrypted metadata, path confidentiality, policy, audit, and deletion govern sensitive summaries.
- **Performance engineering:** cold/warm experiments, percentiles, attribution, and cost models separate bottlenecks.
- **Formal methods:** conservative abstraction and equivalence proofs validate pruning and rewrites.

## References

1. Apache Iceberg, [Performance](https://iceberg.apache.org/docs/latest/performance/). Current. Explains manifest-list and manifest filtering for scan planning.
2. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines metadata roots, snapshots, manifest lists, manifests, summaries, and statistics.
3. Apache Iceberg, [Maintenance](https://iceberg.apache.org/docs/latest/maintenance/). Current. Documents manifest rewriting, snapshot expiration, and orphan cleanup.
4. Apache Iceberg, [Configuration](https://iceberg.apache.org/docs/latest/configuration/). Current. Documents manifest merge, metadata retention, planning, and commit controls.
5. Apache Iceberg, [REST Catalog Specification](https://iceberg.apache.org/rest-catalog-spec/). Current. Documents lazy snapshot loading, caching, server-side planning, and metrics capabilities.
6. Apache Iceberg, [Puffin Specification](https://iceberg.apache.org/puffin-spec/). Current. Defines snapshot-scoped statistics containers and integrity metadata.
7. Delta Lake, [Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Current. Defines log actions, checkpoints, sidecars, and file-removal retention.
8. Delta Lake, [Best Practices](https://docs.delta.io/best-practices/). Current. Covers file compaction and partition sizing.
9. Apache Hudi, [Table Metadata](https://hudi.apache.org/docs/metadata/). Current. Documents metadata-table file listings and statistics indexes.
10. Apache Hudi, [Technical Specification](https://hudi.apache.org/learn/tech-specs/). Current. Defines metadata-table listing and column-statistics records.
11. Apache Paimon, [Manifest](https://paimon.apache.org/docs/master/concepts/spec/manifest/). Current. Defines manifest files, lists, entries, and merge behavior.
12. Apache Parquet, [Page Index](https://parquet.apache.org/docs/file-format/pageindex/). Current. Defines page-level indexes and conservative skipping metadata.
13. Apache Spark, [Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Current. Documents file discovery, partition sizing, caching, and parallelism controls.

## Exercises

### Exercise 1

A manifest list references 800 manifests totaling 24 GiB. A query selects 40 manifests totaling 3 GiB, which contain 2 million of 30 million file entries. Compute manifest-count, manifest-byte, and entry-count prune fractions.

### Exercise 2

Design a bounded planner for 15 million file entries with a 2-GiB heap budget. Include projection, batches, concurrency, delete pairing, backpressure, cancellation, and spill.

### Exercise 3

State the proof obligations for rewriting 4,000 small data and delete manifests into 120 larger manifests while writers continue committing.

### Exercise 4

An asynchronous statistics index covers snapshot 500 while a query pins 507. Explain safe use of the index and the evidence required before it may reject files.

### Exercise 5

Design an operational dashboard and experiment matrix that distinguishes poor metadata shape, cold-cache cost, object throttling, driver pressure, and weak pruning.

## Answers to the Exercises

### Answer 1

Manifest-count pruning is $1-40/800=95\%$. Manifest-byte pruning is $1-3/24=87.5\%$. Entry-count pruning is $1-2/30\approx93.33\%$. Report all three: selected manifests are larger than average, so count alone overstates saved metadata bytes.

### Answer 2

Pin one root and project only identity, content, spec/sequence, partition, required metrics, and delete fields. Decode manifests through a byte-limited pool into fixed entry batches; pair deletes using bounded partition/file cohorts; emit tasks to a bounded consumer queue. Account decoded strings/maps and cache separately, reserve headroom below 2 GiB, spill deterministic oversized join state, propagate cancellation, close streams, and cap object requests and bytes independently. Test the budget with worst-case entries rather than averages.

### Answer 3

Pin base snapshot and exact inputs; normalize every entry including status, identity, content, partition/spec, schema, sequence, metrics, equality IDs, key metadata, and lineage; require input/output multiset equality and identical delete applicability; validate checksums and summary conservatism; ensure unselected manifests remain referenced; conditionally publish against a head where inputs and interpretation still apply; retry/replan on conflict; and retain old manifests for snapshots/branches that reference them.

### Answer 4

Bind the index to its declared snapshot/coverage. It may reject only files whose exact identities and compatible schema/metric semantics are covered through 500 and whose index evidence proves disjointness. Files or changes from 501–507, missing shards, unknown encodings, and changed fields/specs fall back to authoritative manifests and remain candidates unless other conservative evidence rejects them. Validate checksum, coverage watermark, build source, and result equality before expanding use.

### Answer 5

Graph stage percentiles for catalog/root, list, manifest reads, entry filtering, delete pairing, and task creation alongside total/selected counts and bytes, requests/throttles/retries, cache hit/age, heap/GC/spill, concurrency, tasks, and selected data bytes. Segment by table, predicate class, snapshot/spec, cache state, engine/version, region, and tenant. Run matched cold/warm selective, no-match, full-scan, evolved-spec, delete-heavy, concurrent, throttled, and index-disabled trials. Poor shape raises manifest requests/bytes; cold-cache cost changes warm/cold delta; throttling raises wait/retry; driver pressure raises heap/GC/spill; weak pruning raises selected fractions and downstream data bytes.
