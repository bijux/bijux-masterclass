---
module_id: LSDS-078
program: Large-Scale Data Systems Engineering
level: 2
module_number: 78
title: Deletion Vectors and Row-Level Changes
status: complete
last_verified: 2026-09-04
---

# Deletion Vectors and Row-Level Changes

## One-Page Review

### Governing question

How can an immutable-file table represent row deletes, updates, and merges without rewriting every touched data file immediately, while ensuring each reader applies the right delete to the right row exactly once under snapshot, sequence, partition, schema, concurrency, compaction, and protocol-evolution rules?

### Essential definitions

- A **deletion vector (DV)** is an immutable bitmap or equivalent set of physical row positions deleted from one referenced data file.
- A **position delete** identifies a row by immutable data-file identity and zero-based physical row position.
- An **equality delete** identifies rows by equality over a declared set of stable field IDs.
- **copy-on-write (COW)** materializes a row change by rewriting affected data files before commit.
- **merge-on-read (MOR)** commits data plus delete/delta structures and reconciles them while reading or during later compaction.
- A **delete applicability rule** decides whether a delete structure affects a data file using reference, partition, sequence, and content semantics.
- **delete cardinality** is the number of distinct physical rows represented by a position mask or delete structure.
- A **tombstone** is a logical record that removes or supersedes an earlier key/version under an ordered merge rule.
- **purge/materialization** rewrites live rows into new files and removes now-incorporated delete structures from the current snapshot.
- A **row identity** is a stable logical identifier distinct from a file position, unless a protocol explicitly defines lineage.

### Central model, mechanism, or theorem

For data file $f$ with physical positions $P_f=\{0,\ldots,n_f-1\}$, let applicable position deletes be $D_f\subseteq P_f$ and applicable equality predicates be $E_f$. A reader returns

$$Live(f)=\{r_{f,p}:p\in P_f\setminus D_f\land \neg match(r_{f,p},E_f)\}.$$

Applicability is versioned protocol logic, not proximity in a directory. A DV normally references exactly one immutable file; its set bits are positions to suppress. An equality delete may affect multiple older files in the same permitted partition/sequence scope. An update is commonly delete-old plus insert-new, with ordering that prevents the delete from removing its own replacement. At most one effective DV per referenced file simplifies readers; writers merge new positions with prior applicable position deletes. Compaction decodes the snapshot-visible live state, writes replacement files, validates inputs, and atomically removes incorporated deletes.

### Critical invariants

- Every position delete binds an immutable data-file identity and a valid physical position; file rewriting creates a different identity and position domain.
- A DV's declared cardinality, offset, length, checksum, codec/version, and referenced file agree with its actual bitmap payload.
- The effective deleted-position set is union semantics; duplicate delete positions do not delete additional rows.
- A snapshot has at most the protocol-allowed number of effective vectors per data file, and supersession rules prevent double interpretation.
- Equality deletes bind stable field IDs, types, null/NaN equality, partition scope, and sequence ordering.
- A delete never applies to a replacement/new row unless the protocol's ordering says it should.
- Readers combine file, delete, schema, partition-spec, and sequence metadata from one pinned snapshot.
- Updates preserve key uniqueness and deterministic winner semantics across retries, concurrent writes, and compaction.
- Purge/compaction removes a delete structure only when every effect it represents is materialized or otherwise preserved.
- Unsupported delete features cause explicit reader/writer rejection; silent ignoring is forbidden.

### Common failures

Common failures include treating a row position as stable after rewrite; attaching a DV to a file path that can be overwritten; allowing two independent vectors for one file without union/supersession; adding a new DV that omits prior position deletes; applying equality deletes to newer replacement rows; matching fields by name instead of stable ID; treating SQL null equality as ordinary equality without protocol rules; pruning delete files from data bounds incorrectly; counting bitmap bits without range validation; purging some deletes while dropping others; enabling a table feature before every reader supports it; retrying an unknown row-change commit with a new transaction ID; and vacuuming data or delete files still reachable from retained snapshots.

### Compact example

Data file `f` has rows at positions 0–5. The current DV for `f` contains `{1,4}`. A new delete targets position 3. The writer creates a replacement vector `{1,3,4}`, validates that `f` and the old vector still apply, and publishes metadata that supersedes the old vector. Readers return positions `{0,2,5}`. If compaction later writes those three rows to new file `g`, positions in `g` start from zero and the old vector must not be applied to `g`. Snapshot-pinned readers may still need `f` and its old vector until retention expires.

### Connections

[LSDS-043](043-stateful-operators.md) supplies keyed update state, [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies idempotency, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies snapshot publication, [LSDS-072](072-manifest-and-metadata-trees.md) supplies file/delete metadata, [LSDS-073](073-optimistic-concurrency.md) supplies conflict validation, [LSDS-074](074-schema-evolution-at-scale.md) supplies stable field identity, and [LSDS-076](076-compaction-planning.md) supplies materialization planning.

## Governing Question

Columnar analytical files are optimized because they are immutable. A one-row update should not require in-place mutation, yet rewriting a multi-gigabyte file for every changed row creates enormous write amplification and latency. Delete structures separate logical visibility from physical bytes: keep the data file and publish a compact description of rows that no longer belong to the snapshot.

This moves work and risk. Readers must discover all applicable deletes, match them correctly, and avoid suppressing later rows. Position-based representations are cheap and precise but coupled to file identity and ordinal. Equality representations survive physical position changes but require keys, typed equality, and ordering. DVs compact position sets but introduce binary formats, cardinalities, offsets, and supersession.

The governing question is how to define, publish, read, merge, compact, evolve, and observe these structures so deferred rewriting remains correct under concurrent row changes and long snapshot retention.

## Why This Matters

Row-level changes power CDC ingestion, deduplication, corrections, privacy deletion, slowly changing dimensions, transactional merges, and mutable serving views. COW offers simple reads but high write amplification. MOR lowers write cost but increases read planning, merge CPU, memory, metadata, and compatibility requirements.

Deletes are correctness-bearing negative data. Missing one resurrects a row. Applying one too broadly removes a valid row. A stale vector can silently corrupt every query while data files and row counts look plausible. Delete metadata therefore deserves the same integrity, audit, and retention controls as data.

Deferred physical deletion also changes compliance language. A row can be logically invisible in the current snapshot while its bytes remain in a retained file. Legal erasure may require purge, snapshot expiration, replica/cache handling, and verified physical lifecycle—not merely a DV bit.

## Prerequisites and Retrieval

Review keyed state in [LSDS-043](043-stateful-operators.md), replay safety in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), snapshot publication in [LSDS-071](071-table-snapshots-and-atomic-commit.md), metadata graphs in [LSDS-072](072-manifest-and-metadata-trees.md), OCC in [LSDS-073](073-optimistic-concurrency.md), stable schema identity in [LSDS-074](074-schema-evolution-at-scale.md), and compaction planning in [LSDS-076](076-compaction-planning.md).

You should understand immutable files, row groups/pages, physical positions, bitmaps and set union, primary/equality keys, null and NaN semantics, MVCC, sequence numbers, partition specs, manifests, predicate pruning, update ordering, idempotency, snapshots, compaction, checksums, and feature negotiation.

For diagnosis retain the exact snapshot, data/delete manifests, data-file identities and row counts, DV container identity/offset/length/cardinality/checksum, equality-field IDs and schemas, sequence numbers, partition/spec IDs, operation/transaction IDs, reader/version, planner applicability trace, and compaction/retention history.

## Learning Objectives

After this module, you should be able to:

1. Distinguish COW, MOR, position deletes, equality deletes, DVs, and update logs.
2. Model physical row positions as scoped to one immutable file identity.
3. Apply partition, sequence, reference, and equality rules to select deletes.
4. Merge new and prior position deletes without loss or double interpretation.
5. Explain update-as-delete-plus-insert ordering and idempotency.
6. Design a reader pipeline that prunes, loads, validates, and applies deletes.
7. Coordinate concurrent changes to the same data file or key range.
8. Purge deletes through equivalence-preserving compaction.
9. Roll out protocol features across all readers, writers, and maintenance tools.
10. Verify row visibility, bitmap integrity, performance, and physical erasure evidence.

## Core Exposition

### Four row-change strategies

**Copy-on-write** reads affected files, applies changes, writes replacements, and atomically swaps them. Readers see ordinary files and no deferred merge for those changes. Sparse updates pay high read/write/shuffle cost and conflict over large files.

**Position delete files** store `(file identity, position)` pairs, sometimes deleted row values. They can batch deletes for multiple files but readers may scan and join delete rows. Positions are precise only for the named immutable file.

**Deletion vectors** encode positions, commonly as compressed bitmaps, for one referenced file. Membership tests and cardinality can be efficient. A container may hold multiple vector blobs, but manifest metadata must identify exact blob offset and length. One effective vector per file avoids reader unions over many generations.

**Equality deletes or keyed delta logs** identify logical rows and defer matching/merging. They avoid reading target files during write but require typed key equality, ordering, possible hash state, and wider applicability scans. Product-specific MOR logs may carry inserts and updates rather than standardized equality deletes.

### Physical position identity

File position is a zero-based ordinal in the exact logical row sequence defined by the file reader. It is not a byte offset, row-group-local index, key, or stable row ID. Projection and predicate pushdown must retain the mapping to original positions before applying a DV. If a vector says position 9 is deleted, a reader cannot first filter rows and then treat the filtered row's index as the original position.

Rewriting, sorting, compacting, or changing row-group boundaries creates new positions. The new file needs no old DV; the compactor materializes live rows. A content-addressed or immutable unique file identity prevents a path from referring to different bytes over time.

### Bitmap representation

For file with $n$ rows, DV set $D\subseteq\{0,\ldots,n-1\}$. A dense bitset needs roughly $n/8$ bytes; compressed bitmap size depends on distribution. Roaring-style containers exploit sparse values and runs. Never infer correctness from compact size.

Validate every decoded position is nonnegative and below row count, declared cardinality equals distinct set bits, container version/codec is supported, checksum and length match, and referenced file metadata agrees. Duplicate logical deletes collapse under set union.

To add positions $N$, form $D'=D\cup N$. If older position-delete files also apply and the new protocol says a DV supersedes them, include their positions in $D'$ before publishing. A missing prior bit resurrects a row.

### Applicability

Delete selection begins from one pinned snapshot. For a DV, require exact referenced data file and any format-defined partition and sequence conditions. For position-delete files, use referenced file when present, partition/spec scope, and sequence age. For equality deletes, select based on stable equality field IDs, partition rules, data/delete sequence relationship, and conservative metrics overlap.

Ordering distinguishes old and new rows. If update commit writes a delete for old key `k` plus replacement row `k`, the delete must apply to the old file but not the replacement. Many protocols use data sequence numbers: equality delete applies to strictly older data, while position delete can target a same-commit known position under defined rules. Implement the exact specification.

### Equality semantics

An equality delete declares field IDs, not display names. Reader resolves their historical/current types and compares protocol-defined values. Null, NaN, signed zero, decimal scale, timestamps, binary, nested optional parents, and collation require explicit rules. SQL predicate `a = NULL` is not a substitute for table-format delete equality.

Keys need not be application-unique unless declared. One equality tuple can remove many matching rows from applicable files. Key evolution is dangerous: dropping, renaming by name-only mapping, changing type, partitioning, or identifier semantics must preserve historical delete interpretation.

### Reader pipeline

The planner selects data files from query predicates, then selects all delete structures that could apply. Delete pruning must be conservative: a false positive costs work; a false negative returns deleted rows. Use partitions, referenced-file identity, sequences, and metrics in that order under format rules.

The scan validates delete metadata and payload, maps physical positions before row filtering, applies position membership, and evaluates equality/keyed merges. It can push row-range information into DVs or indexes, but optimization cannot change original ordinal. Apply query residual after or alongside deletes while preserving position mapping.

Record applicability decisions per data/delete pair in debug traces. High-level “two delete files read” is insufficient when diagnosing a resurrected row.

### Updates and merges

An update often becomes delete of old physical/logical row plus insertion of new row. A merge combines source matching, target visibility, conflict validation, and action ordering. One source row matching multiple targets, multiple source rows matching one target, retries, and late CDC events need deterministic policy.

Persist source transaction/batch identity. On retry, detect committed identity rather than emitting a second replacement. Capture target data/delete files or key/predicate ranges in the read/validation set. A concurrent update to the same file/key can invalidate a position plan even if both publish different vector objects.

### Concurrent DV updates

Writers A and B read vector $D$. A adds set $X$ and publishes $D\cup X$. B cannot publish $D\cup Y$ against the new head because it would lose $X$. It refreshes, unions $Y$ with the current effective vector, validates that the referenced file remains live and unchanged, and conditionally publishes $D\cup X\cup Y$.

If the data file was rewritten or removed, B's positions have no target and cannot be rebased by path. Re-identify logical rows from source/key evidence or abort. Exactly one effective vector per file means metadata publication also supersedes the prior vector atomically.

### Statistics and query planning

Data-file min/max and row count may describe physical rows including logically deleted ones. They remain conservative for finding live rows but can lose precision when boundary values are deleted. Live row count can be estimated as $n-|D|$ for one validated DV and no other delete types, but equality deletes and duplicate delete encodings complicate it.

Delete metrics allow pruning delete files against data/query ranges. They must cover every deleted tuple or be omitted. A compact vector usually lacks value metrics unless supplemental metadata exists. Query cost should include vector fetch/decode, bitmap membership, equality hash/sort merge, extra columns, and reduced output.

### Purge and compaction

Purge selects exact data files and all applicable deletes at base snapshot, decodes live rows, writes new files, validates logical equivalence, and atomically replaces both the old data files and incorporated delete structures. If a delete file also applies to unrewritten data, it cannot simply be removed; split/rewrite it or retain it.

The new file receives new identity and positions. New statistics describe live output. Concurrent changes to inputs, vectors, equality deletes, schema/spec, or key semantics trigger conflict/replan. Old files/vectors remain for retained snapshots until expiration and cleanup.

Trigger purge from read cost, deleted density, vector/log count, compliance deadlines, protocol migration, or layout maintenance—not one universal percentage. A highly deleted cold file may still have low operational payback but high erasure priority.

### Feature rollout and downgrade

DVs and delete encodings are protocol features. Inventory every batch/stream reader, writer, query engine, maintenance service, catalog inspector, CDC exporter, backup, recovery, sharing, and audit tool. Deploy capability before enabling writes; fence unsupported clients; canary; verify mixed old/new snapshots; then expand.

Downgrade may require applying/purging all vectors and rewriting metadata/history before removing a feature. Disabling new vector creation does not make existing vectors disappear. Rollback of the table pointer must retain capable readers for snapshots that already use the feature.

### Security, privacy, and observability

Delete structures may reveal which rows changed, keys, values, file locations, cardinalities, and access patterns. Encrypt and authorize them like data. Verify container integrity and prevent path substitution. Audit writer, reason, legal request, transaction, target snapshot/files, positions/keys under protected access, and purge proof.

Track physical/live rows, deleted positions, vector bytes/cardinality/density, vectors/delete files per data file, equality rows, vector fetch/decode/cache, delete matching CPU/memory, candidate pairs, rows suppressed, row-change latency, conflicts/retries/unknowns, compaction backlog, current versus retained physical bytes, and erasure deadlines. Segment by snapshot, delete type, partition/spec, schema, engine/version, and file-size/density cohort.

## Definitions and Notation

Let:

- $f$ be an immutable data file with identity $id_f$ and physical row count $n_f$;
- $P_f=\{0,\ldots,n_f-1\}$ be its position domain;
- $D_f\subseteq P_f$ be the effective position-delete set;
- $E_f$ be applicable equality-delete tuples/predicates;
- $r_{f,p}$ be row at position $p$;
- $seq_d(f)$ and $seq_x(d)$ be data and delete sequence numbers;
- $part(f)$ and $spec(f)$ be partition tuple and specification identity;
- $card(D_f)=|D_f|$ be vector cardinality;
- $density(D_f)=|D_f|/n_f$ for $n_f>0$;
- $L(f)$ be live rows after every applicable delete/update rule;
- $B_{dv}$ and $B_f$ be vector and data-file bytes;
- $A_r$ be read amplification including data/delete work;
- $T$ be a stable logical transaction ID.

Position sets use union, so $|D_1\cup D_2|$ can be less than $|D_1|+|D_2|$. Never add cardinalities without checking overlap. Density is undefined for zero-row files and is not itself a performance or purge threshold.

## Mechanisms, Invariants, or Proof Structure

### Position-mask correctness

Assume immutable $f$, validated position domain, and complete effective set $D_f$. The reader enumerates original positions and returns exactly those not in $D_f$, so every set bit suppresses its target and every unset position remains, subject to equality/query filters. Filtering before recovering original ordinals or applying $D_f$ to another file violates the premise.

### DV replacement proof

Current vector is $D$, new requested positions are $N$, and prior applicable position deletes are $P$. Writer publishes one replacement $D'=D\cup N\cup P$ while atomically superseding prior position structures for $f$. Set union preserves every earlier deletion and makes duplicates idempotent. Conditional validation prevents concurrent $D\cup X$ from being lost.

### Update ordering proof

An update removes old row in file with data sequence $a$ and adds replacement with sequence $b>a$. Equality delete at sequence $b$ applies to data with sequence strictly below $b$, so it removes the old row and not the replacement. This argument depends on exact protocol comparison; changing `strictly less` to `less or equal` deletes the new row.

### Purge equivalence

Let $I$ be selected data plus all applicable deletes and $O$ rewritten files. Require decoded live multiset $L(I)=L(O)$ under schema, key, sequence, null, and ordering rules. Delete structures can be removed from current state only if their effects on every remaining applicable file are preserved. Publish atomically and retain old state for pinned snapshots.

### Adversarial verification

Test empty, singleton, dense, run-heavy, duplicate, out-of-range, negative, 32/64-bit-boundary, truncated, checksum-failed, wrong-file, wrong-offset, and unsupported-codec vectors. Test equality null/NaN/type evolution, same-commit replacement, concurrent union, input rewrite, timeout-after-commit, partial purge, retained snapshots, and unsupported readers. Expected result is exact visibility or explicit failure, never silent fallback that exposes deleted rows.

## Alternatives and Trade-Offs

**COW** gives simple fast reads and immediate physical normalization but amplifies sparse writes. **MOR** lowers write latency and amplification but shifts merge work and protocol complexity to readers/compaction.

**Position deletes** are exact and cheap to test but coupled to file identity/ordinal. **Equality deletes** are independent of physical position but require keys, typed comparison, ordering, and broader matching. **DVs** compact per-file positions but need bitmap integrity and synchronous merge/supersession.

**One DV per file** bounds reader lookup and clarifies state but makes concurrent writers merge prior bits. **Multiple vector generations** simplify appends but increase read fan-in and precedence complexity.

**Immediate purge** reduces read debt and physical retention but pays COW cost. **Deferred purge** protects writes but accumulates vectors/logs, storage, and compliance complexity.

**Global equality deletes** simplify unpartitioned key deletion but can pair with many files. **Partition-scoped deletes** prune better but require partition evolution and key-routing correctness.

**Stable row IDs** can support lineage and updates beyond physical position but require allocation, persistence, and cross-engine semantics. **File position** is compact and readily available but changes on rewrite.

## Failure Modes and Misconceptions

1. **Position is a byte offset.** It is a logical row ordinal in one file.
2. **Position survives rewrite.** New file identity creates a new domain.
3. **DV means row ID.** It identifies positions, not stable logical entities.
4. **Two vectors can be read independently forever.** Protocols may require one effective merged vector.
5. **Cardinalities add.** Duplicate positions make union smaller.
6. **New vector may omit old deletes.** That resurrects rows.
7. **Equality delete uses column names.** Stable field IDs and types bind keys.
8. **SQL null equality defines delete equality.** The table protocol must define it.
9. **Delete applies to every matching file.** Partition and sequence scope constrain it.
10. **Same sequence comparison is arbitrary.** It can decide whether a replacement survives.
11. **Query filtering can renumber rows first.** DVs require original positions.
12. **Data bounds describe only live rows.** Deleted boundary values may remain in statistics.
13. **Delete-file pruning may be aggressive.** A false negative exposes deleted rows.
14. **Update is one in-place mutation.** Immutable tables often encode delete plus insert.
15. **Retrying merge is harmless.** Stable transaction identity is required.
16. **Purge can drop a shared equality delete.** It may still affect unrewritten files.
17. **Logical deletion proves physical erasure.** Retained bytes, caches, and replicas remain.
18. **Feature disable equals downgrade.** Existing vectors still require capable readers.

## Worked Examples

### Example 1

File `f` has 10 rows and DV `{2,5,9}`. Live positions are `{0,1,3,4,6,7,8}`, cardinality is 3, and density is 30%. A bit 10 is invalid because positions end at 9.

### Example 2

Existing DV is `{1,4}`, an older position-delete file contributes `{4,6}`, and a new operation adds `{2}`. Replacement DV is `{1,2,4,6}` with cardinality 4, not 5.

### Example 3

File `g` replaces `f` after compaction. Even if `g` contains the same live rows, its position 1 may represent a different row. The DV referencing `f` cannot attach to `g`.

### Example 4

Equality delete on field ID 7 has key `A`. It applies to data sequence 30; replacement row `A` is written at sequence 31 alongside delete sequence 31. Strict older-than application removes the old row but preserves the replacement.

### Example 5

Query pruning selects two data files. A global equality delete could affect either, so both pairings remain candidates. Its key bounds exclude one file only if bounds are complete, compatible, and conservatively disjoint.

### Example 6

Two writers add positions `{3}` and `{8}` to base vector `{1}`. First publishes `{1,3}`. Second refreshes and publishes `{1,3,8}`. Publishing `{1,8}` would resurrect position 3.

### Example 7

A reader filters `country='SE'` before tracking original ordinals. The surviving array indices no longer match the file DV. Correct execution retains original positions or applies the vector before position-destroying filtering.

### Example 8

Purge rewrites file `a` but an equality delete also applies to untouched `b`. Removing that delete would expose rows in `b`. Split/materialize its effects for `a` while retaining an applicable structure for `b`.

### Example 9

A privacy request is logically deleted at snapshot 100. Physical erasure is not complete until affected data/delete/history objects expire or are purged, replicas/caches follow policy, and an audit verifies unreachable deletion under the required retention/legal constraints.

### Example 10

The executable fixture merges duplicate position sets and derives live rows.

<!-- bijux-verify: {"id":"deletion-vector-union","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deleted_positions=1,2,4,6\ncardinality=4\nlive_positions=0,3,5,7\ndensity_percent=50.0\nout_of_range=no\n","stderr":""}} -->
```python
row_count = 8
existing_dv = {1, 4}
position_file = {4, 6}
new_deletes = {2}

effective = existing_dv | position_file | new_deletes
out_of_range = any(position < 0 or position >= row_count for position in effective)
live = [position for position in range(row_count) if position not in effective]

print(f"deleted_positions={','.join(map(str, sorted(effective)))}")
print(f"cardinality={len(effective)}")
print(f"live_positions={','.join(map(str, live))}")
print(f"density_percent={100 * len(effective) / row_count:.1f}")
print(f"out_of_range={'yes' if out_of_range else 'no'}")
```

## Cross-Program Connections

- **Data structures:** bitsets, Roaring bitmaps, sets, sparse/dense representations, and rank/select operations implement position masks.
- **Database systems:** MVCC, tombstones, secondary indexes, heap tuple IDs, vacuum, and WAL offer related identity/lifecycle models.
- **Streaming:** CDC ordering, keys, epochs, checkpoints, deduplication, and late events drive row-change semantics.
- **File formats:** row-group/page ordinals, column projection, statistics, checksums, and immutable identities determine applicability.
- **Distributed systems:** atomic commits, OCC, idempotency, unknown outcomes, retention, and garbage collection preserve state.
- **Query engines:** split planning, conservative delete pruning, bitmap filtering, equality joins, vectorization, and caching determine read cost.
- **Platform engineering:** capability rollout, fleet inventory, compaction queues, metrics, audits, and incident response operationalize deletes.
- **Security and governance:** logical deletion, physical erasure, legal holds, key exposure, lineage, and audit evidence define compliance.

## References

1. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines position/equality deletes, deletion vectors, sequence applicability, manifests, and row lineage.
2. Apache Iceberg, [Puffin Specification](https://iceberg.apache.org/puffin-spec/). Current. Defines the blob container used for deletion vectors.
3. Apache Iceberg, [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Current. Documents atomic commits, concurrent writes, retries, and validation.
4. Apache Iceberg, [Maintenance](https://iceberg.apache.org/docs/latest/maintenance/). Current. Covers data-file rewrite and snapshot/orphan lifecycle.
5. Delta Lake, [Deletion Vectors](https://docs.delta.io/delta-deletion-vectors/). Current. Documents soft deletes, supported operations, purge, and limitations.
6. Delta Lake, [Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Current. Defines deletion-vector descriptors, file actions, and table features.
7. Delta Lake, [Concurrency Control](https://docs.delta.io/concurrency-control/). Current. Documents row-level changes and optimistic conflict classes.
8. Apache Hudi, [Table and Query Types](https://hudi.apache.org/docs/table_types/). Current. Describes copy-on-write, merge-on-read, base files, logs, and query freshness.
9. Apache Hudi, [Compaction](https://hudi.apache.org/docs/compaction/). Current. Documents merging log updates into versioned base files.
10. Apache Paimon, [Table Index](https://paimon.apache.org/docs/master/concepts/spec/tableindex/). Current. Documents deletion-file bitmap formats, checksums, and position ranges.
11. Apache Paimon, [Primary Key Table with Iceberg](https://paimon.apache.org/docs/master/iceberg/primary-key-table/). Current. Documents deletion-vector interoperability and feature constraints.
12. RoaringBitmap, [Format Specification](https://github.com/RoaringBitmap/RoaringFormatSpec). Current. Defines portable compressed bitmap encodings.
13. Apache Parquet, [Page Index](https://parquet.apache.org/docs/file-format/pageindex/). Current. Defines row/page index structures relevant to physical position filtering.

## Exercises

### Exercise 1

A 12-row file has existing DV `{1,5,7}`, a position-delete file `{5,9}`, and new deletes `{0,9}`. Compute replacement set, cardinality, live positions, and density.

### Exercise 2

Explain why an equality delete written at sequence 50 should use a strict age rule for a replacement row also written at 50. What happens under a non-strict comparison?

### Exercise 3

Design the reader steps for query predicate `region='EU'` when data files have DVs and equality deletes. Include conservative pruning and ordinal preservation.

### Exercise 4

Two writers concurrently modify the DV for the same file. Describe safe retry if the file remains live, and the required response if it was compacted away.

### Exercise 5

Design evidence for proving both logical deletion and required physical erasure of a customer record under retained snapshots and legal holds.

## Answers to the Exercises

### Answer 1

Union is `{0,1,5,7,9}` because duplicates collapse. Cardinality is 5. Live positions are `{2,3,4,6,8,10,11}`. Density is $5/12\times100\approx41.67\%$. Validate every position is within 0–11 before publication.

### Answer 2

The delete represents removal of the old row and the same commit inserts its replacement. Applying equality deletes only to strictly older data removes the pre-update file while preserving the sequence-50 replacement. A less-than-or-equal rule would also match and suppress the new row, turning an update into a delete. Follow the table protocol's exact comparison.

### Answer 3

Pin the snapshot; prune data files conservatively with partition/file statistics; select every DV by exact referenced file plus partition/sequence rules; select equality deletes by partition, sequence, stable field IDs, and only sound metric disjointness. Validate payloads and schemas. Enumerate original file ordinals, apply DV/position masks before any operation that renumbers rows, evaluate applicable equality keys under protocol null/type semantics, then evaluate the query residual and projection. Trace pairwise applicability and counts.

### Answer 4

Both start from effective set $D$. The loser refreshes current vector $D'$, unions its requested positions, validates the same immutable data file and prior position structures remain applicable, writes a replacement vector, and CAS-publishes metadata that supersedes the current one. It retains the same transaction ID. If compaction replaced the file, physical positions no longer identify target rows; abort/replan from logical key or source evidence rather than attach positions to the new file.

### Answer 5

For logical deletion, record authorized request/transaction, target identity, commit snapshot, applicable delete structure, and queries over current state showing no visible match across supported readers. For physical erasure, inventory every data/delete file and snapshot/branch/tag, legal hold, replica, cache, backup, and export that may contain the bytes. Resolve holds, purge/rewrite affected files, expire permitted snapshots, run reachability-based cleanup, verify object deletion and key/lifecycle state, and retain tamper-evident audit evidence without preserving the sensitive value itself. A current-query absence alone proves only logical invisibility.
