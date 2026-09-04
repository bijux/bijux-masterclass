---
module_id: LSDS-075
program: Large-Scale Data Systems Engineering
level: 2
module_number: 75
title: Metadata Mechanics of Partition Evolution
status: complete
last_verified: 2026-09-04
---

# Metadata Mechanics of Partition Evolution

## One-Page Review

### Governing question

How can a lakehouse table change its physical partition layout without rewriting all historical files, changing logical queries, losing pruning correctness, or allowing old and new writers, overwrites, metadata, and maintenance to interpret partition values under the wrong rules?

### Essential definitions

- A **partition specification** is an identified set of partition fields that derives physical partition tuples from logical row fields.
- A **partition field** has stable identity, source-field identity, transform, result type, and display name.
- A **partition transform** deterministically maps a logical value to a coarser value such as identity, year, month, day, hour, bucket, or truncate.
- **hidden partitioning** derives partition values and query pruning predicates from logical columns so users need not encode the physical layout in queries.
- **partition evolution** publishes a new default specification for future writes while historical files remain bound to their original specifications.
- **split planning** plans each specification cohort with the predicate projection valid for that cohort and unions the candidates.
- An **inclusive projection** produces a partition predicate that may retain false positives but never excludes a partition containing a qualifying row.
- A **residual predicate** is the row-level condition still required after partition pruning.
- A **spec cohort** is the files and manifests written under one partition-specification ID.
- **layout convergence** gradually rewrites old cohorts into the target specification when justified; it is not required for logical correctness.

### Central model, mechanism, or theorem

Let logical predicate $q$ apply to source rows. File $f$ was written under specification $\sigma(f)$ with transform tuple $\tau_{\sigma(f)}$. For each active specification $k$, the planner computes an inclusive projected predicate $\pi_k(q)$, selects candidate files $P_k(q)$, and retains a row residual. Correct mixed-layout planning requires

$$C(q)\subseteq \bigcup_k P_k(q),$$

where $C(q)$ is every live file that could contain a matching row. Evolution changes the default spec for new files; it does not reinterpret old partition tuples. Each manifest/file entry carries its spec ID, and each spec binds stable source and partition-field IDs to exact transforms. A day-to-hour change therefore plans old day files with day projection and new hour files with hour projection, then evaluates the original row predicate across both.

### Critical invariants

- Every content file and manifest is interpreted using the exact partition-specification ID under which it was written.
- Source-field and partition-field identities are stable and never inferred only from display name, tuple position, or path text.
- Transform definitions include exact hashing, truncation, null, timestamp, timezone, encoding, and parameter semantics.
- Predicate projection is inclusive for every active spec; unknown transforms or unavailable values weaken pruning instead of excluding files.
- The logical query is independent of physical partition layout and the residual predicate preserves row-level correctness.
- Evolution atomically publishes a new default spec; old files and their metadata are not rewritten or relabeled.
- Concurrent writers validate that the spec used for staged files remains accepted at commit and record that spec on every output.
- Overwrite, replace-partition, delete, compaction, and cleanup operations define scope across all active specs rather than only the current layout.
- Metadata tables and operational tools expose spec IDs and heterogeneous partition values without silently merging incompatible fields.
- Layout rewrite preserves rows, delete applicability, file lineage, schema/spec IDs, snapshot isolation, and rollback until old cohorts expire.

### Common failures

Common failures include treating a partition as a directory name; relabeling old day files as hourly; comparing tuples by ordinal after a field reorder; reusing a partition-field ID for a different transform; pruning all files with only the current spec; asking users to add physical partition predicates; assuming finer granularity is always better; changing bucket count while treating bucket numbers as comparable; dropping the old day field before metadata consumers migrate; using dynamic partition overwrite after evolution without understanding its new scope; letting stale writers omit spec IDs; compacting mixed-spec files while copying old partition tuples; and deleting “old partitions” by path rather than snapshot reachability.

### Compact example

An events table originally uses spec 3: `day(event_time)`. At snapshot 90, spec 4 becomes default: `hour(event_time)`. Historical file `d.parquet` remains tagged spec 3 with tuple `2026-09-04`; new file `h.parquet` is tagged spec 4 with tuple `2026-09-04T10`. Query `event_time >= 10:15 AND event_time < 10:45` projects to day `2026-09-04` for spec 3 and hour `10` for spec 4. Both files are candidates, and the original timestamp predicate filters rows. Reinterpreting the old day tuple as an hour would lose data.

### Connections

[LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) supplies layout economics, [LSDS-064](064-distributed-hash-and-merge-joins.md) illustrates hash semantics, [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md) supplies dynamic predicates, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies publication, [LSDS-072](072-manifest-and-metadata-trees.md) supplies pruning metadata, [LSDS-073](073-optimistic-concurrency.md) supplies validation, and [LSDS-074](074-schema-evolution-at-scale.md) supplies stable source identity.

## Governing Question

Partition layouts age. A daily time partition may become too coarse as traffic grows, while an hourly layout may create too many small files for old sparse data. A fixed bucket count may skew after tenant growth. A once-important region field may stop filtering queries. Rebuilding a multi-petabyte table merely to change layout can be slower and riskier than tolerating mixed physical organization.

Modern metadata-driven tables can keep historical files in their original layouts and use a new layout for future writes. This is safe only because the table records partition semantics as versioned metadata rather than inferring them from directory names. The query engine separately projects one logical predicate into each specification.

The governing question is how specification identity, transform semantics, manifest grouping, predicate projection, write validation, overwrites, metadata tables, and optional convergence cooperate. Partition evolution is not a DDL string; it is a persistent multi-layout read/write protocol.

## Why This Matters

Partitioning affects scan pruning, write distribution, file size, skew, metadata cardinality, object requests, compaction, and operational ownership. Too coarse reads excess data. Too fine produces tiny files and high metadata cost. Bucketing can distribute load but becomes opaque when bucket count or hashing changes. Identity partitioning can expose sensitive values in paths and metadata.

Without hidden partitioning, logical queries become coupled to physical columns such as `event_date`. When the layout changes from day to hour, users must rewrite filters correctly or scans become slow and sometimes wrong. A metadata transform lets the engine derive physical predicates from the original source predicate and preserve query shape.

Mixed layouts complicate every operation that reasons about physical partitions. Dynamic overwrite, partition replacement, file rewrite, deletion, retention, statistics, metadata queries, and cost estimation must not assume the current spec describes old files. A single missing spec ID can turn an optimization bug into data loss.

## Prerequisites and Retrieval

Review storage-layout selection in [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), hashing and joins in [LSDS-064](064-distributed-hash-and-merge-joins.md), runtime pruning in [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md), atomic snapshots in [LSDS-071](071-table-snapshots-and-atomic-commit.md), metadata trees in [LSDS-072](072-manifest-and-metadata-trees.md), OCC in [LSDS-073](073-optimistic-concurrency.md), and schema identity in [LSDS-074](074-schema-evolution-at-scale.md).

You should understand immutable files, snapshots, stable IDs, partition tuples, transforms, predicate logic, inclusive projection, residual evaluation, hashing, timestamps/time zones, manifests, pruning statistics, dynamic overwrite, compaction, schema evolution, concurrency, and reachability.

Before changing a production spec, retrieve all registered spec IDs and defaults, file/byte/row counts by spec and partition value, source-field IDs and types, transform definitions, active writers/readers, overwrite modes, metadata-table consumers, maintenance jobs, delete files, sort orders, query predicates, pruning traces, skew, small-file distributions, and rollback/retention constraints.

## Learning Objectives

After this module, you should be able to:

1. Model partition specifications as identified transforms over stable source fields.
2. Explain why old files remain bound to old specs after evolution.
3. Derive inclusive partition predicates for identity, temporal, truncate, and bucket layouts.
4. Prove mixed-spec split planning cannot exclude a matching file.
5. Distinguish partition pruning from residual row filtering.
6. Analyze day-to-hour, bucket-count, add/drop, rename, and reorder changes.
7. Identify unsafe overwrite and maintenance behavior across layouts.
8. Coordinate spec updates with concurrent and cached writers.
9. Plan evidence-driven layout convergence without making it a correctness prerequisite.
10. Diagnose performance and correctness by specification cohort.

## Core Exposition

### Specification as typed metadata

Represent partition specification $\sigma_k$ as an ordered presentation of fields, each carrying partition-field ID, source-field ID, transform name/parameters, result type, and display name. The ID and transform define meaning; position and name aid presentation.

A file entry stores `spec_id=k` plus its partition tuple. A manifest typically groups entries with one spec so its partition schema is unambiguous. Table metadata retains all specifications required by reachable snapshots and designates one default for new writes. Removing a field from the default does not erase its definition from historical specs.

### Transform semantics

An identity transform returns the source value. Temporal transforms map dates/timestamps to year, month, day, or hour under specified epoch and zone semantics. Bucket transforms hash typed source bytes with an exact algorithm and reduce modulo $N$. Truncate transforms group numbers or prefixes under defined handling of negatives, decimals, Unicode, and binary.

Null input normally maps to null, but this must be specified. Transform results are not interchangeable even if printed alike. Bucket 3 under `bucket[16]` is not the same range as bucket 3 under `bucket[32]`. A day number and hour number cannot share a field ID merely because both are integers.

### Hidden partitioning and projection

Users write `event_time >= a AND event_time < b`. For each spec, the planner applies projection $\pi_k$ from source predicate to partition predicate. Projection is inclusive: it may select a partition containing no matching rows, but never reject one that could contain a match.

For a day transform over `ts`, a range within one day selects that day, but the row residual still checks exact timestamps. For a width-10 truncation of `id`, predicate `id=37` maps to partition 30. For bucket transforms, equality can map to one bucket because the exact typed hash is known; an arbitrary range generally cannot exclude buckets usefully.

Projection must follow Boolean logic conservatively. Conjunction may combine safe projected terms. Disjunction must retain any partition allowed by either branch. Negation is especially dangerous because an inclusive projection cannot simply negate an inclusive child and remain inclusive. Use the format's defined projection rules.

### Split planning across specs

Let active spec IDs be $K_s$. For each $k$, inspect manifests/files labeled $k$, compute $\pi_k(q)$, and obtain $P_k(q)$. Candidate union is

$$P(q)=\bigcup_{k\in K_s}P_k(q).$$

Every candidate is read with the original logical residual $q$ or a proven equivalent residual. Cost estimates should report pruning separately by cohort. A new hourly cohort may prune well while a large daily cohort dominates I/O; one aggregate percentage conceals the migration state.

Unknown transforms present a compatibility boundary. A reader may ignore the field for pruning and retain affected files when the protocol permits that fallback. A writer cannot safely produce new tuples using a transform it does not implement. Required transform capabilities belong in client inventory.

### Evolution operations

**Add field:** a new spec adds a derived field with a fresh partition-field ID. New files carry it; old files remain in old specs. Metadata-table rows for a unified view may show null/absent for old files, but that is not the old row's transform value.

**Remove field:** a new spec omits the field. Historical files keep it. Some older format versions use a void transform to preserve tuple/ID compatibility. Dropping can change metadata-table schemas and overwrite behavior.

**Rename/reorder:** retain field identity and transform. Rename affects presentation; reorder must not alter tuple identity. Legacy positional formats may impose restrictions.

**Change transform or parameter:** create a new field/spec identity unless the specification explicitly defines evolution equivalence. Day-to-hour, bucket-count, or truncate-width changes produce different domains.

### Time evolution

Changing month to day or day to hour increases granularity for future files. A narrow timestamp query may retain an entire old month/day but only precise new partitions. Correctness is unchanged; efficiency differs by cohort.

Time zones and boundaries are critical. A timestamp-with-zone transform normally uses a defined instant/UTC interpretation, while a local timestamp has no zone. Daylight-saving gaps and overlaps, epoch units, and inclusive/exclusive range endpoints require fixtures. Never parse directory strings as the authoritative transform.

### Bucket evolution

Bucket count changes redistribute future rows. Even if both use the same hash, `hash(x) mod 16` and `hash(x) mod 32` are distinct transforms. Equality predicate can derive one bucket for each spec; join co-partitioning or overwrite scope cannot assume bucket numbers align across counts.

Increasing buckets may reduce per-bucket load but increase files and shuffle coordination. Hot keys stay hot because deterministic hashing does not split one value across buckets. Measure key frequency, writer parallelism, file sizes, query equality patterns, and metadata cost.

### Overwrite and delete semantics

Static overwrite by explicit logical predicate can validate and remove matching files across specs. Dynamic partition overwrite derives replacement scope from partitions produced by the writer's current spec. After day-to-hour evolution, it may replace hours rather than the historical day partitions an operator expected.

Treat layout change as a semantic change for dynamic overwrite APIs. Prefer explicit logical predicates and modern transactional write interfaces. Validate concurrent additions across all specs with inclusive projection. A delete cannot inspect only the default spec.

### Concurrent writers

The spec update atomically changes table metadata and default spec. Writers stage files under a specific spec ID and must record it. At commit they refresh and validate whether that spec remains accepted and whether the operation's semantics survive the change.

An append staged under the prior spec may sometimes commit safely, producing another old-cohort file, if policy and protocol allow. A dynamic overwrite staged under the old default is far more dangerous. Organizations may fence old writers after cutover to accelerate convergence and avoid mixed behavior. Make policy explicit rather than assuming “latest default” rewrites staged tuple semantics.

### Maintenance and convergence

Partition evolution does not require immediate rewrite. New data naturally accumulates in the new cohort. Rewrite old files only when expected savings exceed I/O, compute, conflict, retention, and risk costs.

A convergence job reads rows under old specs, computes the target transform from source values, writes new files labeled with target spec, preserves delete/application semantics, and atomically replaces validated inputs. It does not copy old partition tuple values into new metadata. Work can prioritize hot query ranges, skewed partitions, tiny files, or compliance needs.

Maintain rollback: old snapshots and files remain reachable until validation and retention permit expiration. Rewriting layout may change file paths, clustering, statistics, and CDC/file-level lineage even when row content is equal; downstream file consumers need contracts.

### Observability and verification

Track files, rows, bytes, manifests, partitions, small files, skew, and age by spec. For queries track manifests/files considered and retained per spec, projected predicate, residual, metadata bytes, data bytes, planning and scan time, cache state, and runtime filters. For writers track chosen spec, stale-spec commits/rejections, distribution, file size, and overwrite scope.

Build transform fixtures for nulls, negative values, Unicode, decimals, timestamp boundaries, daylight-saving transitions, and hash vectors. Compare planner candidates with a conservative full-file scan on controlled data. Test old/new/mixed specs, all supported engines, cached metadata, concurrent spec change, dynamic overwrite, delete, compaction, rollback, and metadata-table queries.

## Definitions and Notation

Let:

- $q$ be a logical row predicate;
- $\sigma_k$ be partition specification with ID $k$;
- $\tau_k$ be its tuple of transforms;
- $src(p)$ and $id(p)$ be a partition field's source-field and partition-field IDs;
- $\pi_k(q)$ be inclusive projection of $q$ under $\sigma_k$;
- $r_k(q)$ be the row residual after partition pruning;
- $F_k$ be live files written under spec $k$;
- $C_k(q)\subseteq F_k$ be files that could contain matching rows;
- $P_k(q)$ be files retained by partition/metadata pruning;
- $K_s$ be spec IDs reachable at snapshot $s$;
- $B_k$, $N_k$, and $R_k$ be bytes, files, and rows in cohort $k$;
- $g_k(x)$ be the physical partition tuple for logical row $x$ under spec $k$.

Soundness requires $C_k(q)\subseteq P_k(q)$ for every $k$, hence $C(q)\subseteq\bigcup_kP_k(q)$. Precision $|C_k|/|P_k|$ is often not directly observable without reading rows; candidate and scanned/matched evidence must be labeled.

Partition counts across specs are not directly additive measures of granularity. Sixteen buckets plus thirty-two buckets are two domains, not forty-eight coordinated buckets. Null/absent unified metadata fields must retain their spec context.

## Mechanisms, Invariants, or Proof Structure

### Mixed-spec pruning proof

Take any matching row in file $f$. Its file belongs to exactly one cohort $k=\sigma(f)$. Because $\pi_k$ is inclusive, the partition tuple cannot be rejected by the projected predicate; file-level metadata is also required to be inclusive. Thus $f\in P_k(q)$ and therefore $f\in\bigcup_kP_k(q)$. The proof fails if the wrong spec, transform, source type, timezone, field ID, or Boolean projection is used.

### Old-file stability proof

Evolution creates new spec $k+1$ and changes the default for future writes. It does not mutate file $f$, its manifest entry, or its `spec_id=k`. Readers resolve $k$ from retained table metadata and interpret its tuple with $\sigma_k$. Therefore old layout meaning remains stable. Relabeling, deleting old spec metadata, or positionally merging tuples breaks the premise.

### Convergence equivalence

For validated old input set $I$, the rewrite decodes every row $x$, computes $g_{target}(x)$, and writes output $O$. Correctness requires keyed row multiset equality, schema resolution equality, and preserved delete semantics between $I$ and $O$. File count, partition count, or aggregate bytes alone cannot prove this.

### Overwrite audit

State overwrite intent as logical predicate $q_o$, not an unqualified physical partition list. For every active spec, project $q_o$ inclusively, find possibly affected files, validate intervening additions, and apply the original residual where exactness is needed. If the API instead defines dynamic current-spec replacement, document that changed semantic and prevent users from assuming historical layouts are covered.

### Deployment proof obligations

Before activation, verify every reader can interpret the new spec or conservatively ignore unknown pruning fields as allowed; every writer/maintenance tool either writes the new spec correctly or is fenced/explicitly permitted to use an older one; metadata queries handle heterogeneous tuples; and rollback retains both spec definitions. Publish atomically and validate canary files by recomputing transforms from source rows.

## Alternatives and Trade-Offs

**Evolve in place** preserves table identity and avoids full rewrite, but introduces mixed-spec planning and operational complexity. **Shadow migration** yields one clean target layout but needs duplicate storage, catch-up, cutover, and lineage handling.

**Immediate convergence** simplifies steady state sooner but spends large I/O and increases conflicts. **Natural convergence** rewrites only through normal retention/compaction but may leave inefficient historical cohorts for years.

**Time partitions** match range queries and lifecycle operations but can skew with traffic cycles. **Hash buckets** spread many keys and support equality pruning, but obscure range locality and changing $N$ creates new domains. **Truncation** preserves coarse order but depends on data distribution.

**Fine granularity** reduces candidate bytes for selective queries but increases partitions, manifests, small files, and writer coordination. **Coarse granularity** improves file aggregation and metadata scale but reads more unrelated data.

**Hidden partitions** decouple queries from layout and enable evolution. **Explicit partition columns** are transparent to some tools but burden writers/users and couple queries to physical design.

**Allow old-spec appends** improves availability during rolling upgrades. **Fence old writers** shortens mixed-layout duration and simplifies expectations. Choose based on compatibility, overwrite semantics, convergence goals, and incident recovery.

## Failure Modes and Misconceptions

1. **“Partition equals directory.”** Membership comes from snapshot metadata and spec identity.
2. **Current spec applies to all files.** Historical tuples keep historical semantics.
3. **Name identifies a partition field.** Stable source and partition IDs are required.
4. **Tuple order is identity.** Reorder breaks positional consumers.
5. **Bucket numbers match across counts.** Different $N$ values define different domains.
6. **Finer is always faster.** Metadata and small-file costs can dominate.
7. **Hot keys disappear with more buckets.** One key still hashes to one bucket.
8. **Projection replaces residuals.** Coarse transforms admit false positives.
9. **Negating an inclusive projection is safe.** It can create false negatives.
10. **Unknown transform means empty.** Readers retain affected files or fail per protocol.
11. **Old data gains new partition values.** Unified metadata nulls do not imply transformed history.
12. **Drop removes historical metadata.** Old specs remain needed for retained files.
13. **Dynamic overwrite keeps its scope.** Current-spec partitions may differ after evolution.
14. **Stale appends are always harmless.** Policy, schema, protocol, and convergence may reject them.
15. **Compaction copies tuple metadata.** It must recompute the target transform from rows.
16. **Path deletion expires partitions.** Reachability and snapshot retention govern deletion.
17. **One pruning ratio describes migration.** Cohort-level behavior can differ drastically.
18. **Row equality is the only rewrite contract.** Deletes, lineage, statistics, CDC, and rollback also matter.

## Worked Examples

### Example 1

Spec 1 partitions by month and spec 2 by day. Query for 2026-09-04 retains September from spec 1 and day 04 from spec 2. Both cohorts evaluate the same logical residual; the old monthly file may read extra days but cannot be skipped.

### Example 2

Spec 3 uses a 16-bucket transform over `account_id` and spec 4 uses a 32-bucket transform. Equality `account_id=91` hashes once, then reduces modulo 16 and 32 separately. A join cannot assume bucket 7 in both specs contains identical key sets.

### Example 3

Adding `day(event_time)` to an unpartitioned table affects new files only. Old files appear in the unpartitioned cohort and must be retained for any potentially matching time predicate. A metadata-table null for the new field is not proof those rows have null timestamps.

### Example 4

A day partition field is renamed from `event_day` to `business_day` while retaining ID and transform. ID-aware metadata remains stable. A script that selects metadata columns by name needs a controlled migration even though data-file pruning is unchanged.

### Example 5

Dynamic overwrite writes hours 10 and 11 under the new spec. It replaces those hourly partitions, not an old day partition containing the same hours. If the user's intent is “replace the whole day across history,” use an explicit logical day predicate.

### Example 6

An old writer stages day-partitioned files while the table changes to hours. Policy allows additive old-spec commits for 30 minutes. The commit records old spec ID, validation checks schema/protocol, and monitoring counts stale-spec bytes. Dynamic overwrites from that writer remain fenced.

### Example 7

A convergence job rewrites January from month to day. It recomputes day values from each row, compares keyed row multisets and predicate aggregates, preserves applicable deletes, then atomically replaces only validated source files.

### Example 8

Predicate `NOT (ts >= a AND ts < b)` cannot be implemented by simply negating an inclusive day projection. Boundary days contain both matching and nonmatching rows. Retain conservative partitions and evaluate the row residual.

### Example 9

Query dashboards show 90% overall file pruning. The old spec holds 80% of bytes and prunes only 30%; the small new cohort prunes 99%. Bytes and latency by spec reveal that convergence of hot old ranges may be valuable.

### Example 10

The executable fixture applies one timestamp predicate to day and hour cohorts and unions candidates.

<!-- bijux-verify: {"id":"partition-evolution-planning","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"specs_planned=2\nday_candidates=old-day.parquet\nhour_candidates=new-10.parquet\nall_candidates=new-10.parquet,old-day.parquet\nresidual_required=yes\n","stderr":""}} -->
```python
query_day = "2026-09-04"
query_hour = "2026-09-04T10"
files = [
    {"path": "old-day.parquet", "spec": "day", "partition": "2026-09-04"},
    {"path": "old-other.parquet", "spec": "day", "partition": "2026-09-03"},
    {"path": "new-10.parquet", "spec": "hour", "partition": "2026-09-04T10"},
    {"path": "new-11.parquet", "spec": "hour", "partition": "2026-09-04T11"},
]

day_candidates = [f["path"] for f in files if f["spec"] == "day" and f["partition"] == query_day]
hour_candidates = [f["path"] for f in files if f["spec"] == "hour" and f["partition"] == query_hour]
all_candidates = sorted(day_candidates + hour_candidates)

print("specs_planned=2")
print(f"day_candidates={','.join(day_candidates)}")
print(f"hour_candidates={','.join(hour_candidates)}")
print(f"all_candidates={','.join(all_candidates)}")
print("residual_required=yes")
```

## Cross-Program Connections

- **Data structures:** persistent maps, tagged unions, immutable DAGs, and stable identifiers model heterogeneous specs.
- **Query engines:** predicate normalization, inclusive projection, residual evaluation, split enumeration, cost estimation, and dynamic filtering consume partition metadata.
- **Storage engineering:** file size, object count, directory conventions, lifecycle, and rewrite I/O determine layout cost.
- **Distributed systems:** atomic metadata changes, stale clients, OCC, epochs, fencing, retries, and rollback govern evolution.
- **Database systems:** partition pruning, online repartitioning, global/local indexes, and transactional DDL provide analogies.
- **Streaming:** rolling writers, checkpoints, late data, time semantics, and dynamic overwrites make spec transitions long-lived.
- **Platform engineering:** capability inventory, canaries, observability, maintenance budgets, and repair tools operationalize the format.
- **Governance and security:** partition values may expose sensitive categories; retention, deletion, audit, and access policy span all specs.

## References

1. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines partition specs, transforms, field IDs, evolution, and scan planning.
2. Apache Iceberg, [Partitioning](https://iceberg.apache.org/docs/latest/partitioning/). Current. Explains hidden partitioning and logical-predicate pruning.
3. Apache Iceberg, [Evolution](https://iceberg.apache.org/docs/1.7.0/evolution/). Versioned. Describes mixed partition layouts and split planning.
4. Apache Iceberg, [Spark DDL](https://iceberg.apache.org/docs/latest/spark-ddl/). Current. Documents add/drop partition fields and overwrite cautions.
5. Apache Iceberg, [UpdatePartitionSpec API](https://iceberg.apache.org/javadoc/nightly/org/apache/iceberg/UpdatePartitionSpec.html). Nightly. Defines partition-spec update operations and commit behavior.
6. Apache Iceberg, [Spark Writes](https://iceberg.apache.org/docs/latest/spark-writes/). Current. Documents overwrite modes and distribution behavior.
7. Apache Iceberg, [Spark Queries](https://iceberg.apache.org/docs/latest/spark-queries/). Current. Documents metadata tables used to inspect files, partitions, and manifests.
8. Trino, [Iceberg Connector](https://trino.io/docs/current/connector/iceberg.html). Current. Documents partitioning transforms, metadata tables, and procedures from a reader/engine perspective.
9. Apache Spark, [Data Sources](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html). Current. Documents partitioned data-source read/write behavior.
10. Delta Lake, [Liquid Clustering](https://docs.delta.io/delta-clustering/). Current. Provides a contrasting evolvable data-layout mechanism.
11. Apache Hudi, [Table and Query Types](https://hudi.apache.org/docs/table_types/). Current. Describes file groups, partitions, and query semantics.
12. Apache Paimon, [Primary Key Table](https://paimon.apache.org/docs/master/primary-key-table/). Current. Documents partition and bucket layout considerations.
13. Apache Hive, [Language Manual DDL](https://hive.apache.org/docs/latest/language/languagemanual-ddl/). Current. Provides the explicit partition-management contrast.

## Exercises

### Exercise 1

A table has old monthly files and new daily files. Derive candidate cohorts for query `ts >= 2026-09-04 10:00 AND ts < 2026-09-04 11:00`, and state the residual.

### Exercise 2

Explain why bucket 5 under an 8-bucket transform of `id` cannot be treated as the same partition as bucket 5 under a 16-bucket transform. For equality `id=x`, what should the planner do?

### Exercise 3

A dynamic overwrite job historically replaced a day. The default spec changes from day to hour. What can go wrong, and what write semantics should replace it?

### Exercise 4

Design a convergence validation for rewriting old month-partitioned files into daily files. Include more than row counts.

### Exercise 5

For one query, spec A has 1,000 files and retains 200; spec B has 300 files and retains 6. Compute per-cohort and aggregate file-retention rates, then explain why byte and latency evidence is still required.

## Answers to the Exercises

### Answer 1

The monthly cohort retains month `2026-09`; the daily cohort retains day `2026-09-04`. Both evaluate the original hour-range predicate as the row residual because neither transform identifies only 10:00–11:00. File-level timestamp bounds may prune further if interpreted inclusively, but they do not change the spec projection rule.

### Answer 2

The transforms use different modulo domains: one contains eight equivalence classes and the other sixteen. Bucket labels alone do not identify the same key set. The planner hashes typed `x` using the specified algorithm and computes `hash(x) mod 8` for the old cohort and `hash(x) mod 16` for the new cohort, retaining the appropriate bucket in each. Range predicates usually cannot map to one bucket.

### Answer 3

The job may replace only hours it happens to emit under the new spec while leaving older day files, producing duplicates or stale rows relative to its intended whole-day replacement. Treat the evolution as an overwrite-semantic change, fence the old job, and use a transactional static overwrite/delete defined by the explicit logical day predicate with validation across every active spec.

### Answer 4

Pin the source snapshot and exact input files. Decode rows with historical schema/specs, recompute target day transforms from source timestamps, preserve keys and delete applicability, and write target-spec files. Compare canonical keyed row multisets, nulls, timestamp boundaries, aggregates by day and important dimensions, predicate results, schema values, deletes, statistics, and CDC/lineage expectations. Validate inputs still live before atomic replacement; retain the old snapshot for rollback.

### Answer 5

Spec A retains $200/1000=20\%$ of files. Spec B retains $6/300=2\%$. Aggregate retention is $206/1300\approx15.85\%$. File counts conceal size skew: A's retained files could be tiny or enormous. Metadata fetches, bytes selected/read, row groups, cache state, planning time, scan time, and concurrency determine impact. Report these by spec before prioritizing convergence.
