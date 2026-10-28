---
module_id: LSDS-071
program: Large-Scale Data Systems Engineering
level: 2
module_number: 71
title: Table Snapshots and Atomic Commit
status: complete
last_verified: 2026-09-04
---

# Table Snapshots and Atomic Commit

## One-Page Review

### Governing question

How should a lakehouse table represent immutable snapshots and publish one new table state atomically so readers never observe partial writes, concurrent writers serialize or conflict safely, retries do not duplicate data, unknown outcomes are resolved, and old files remain available until no retained snapshot can reference them?

### Essential definitions

- A **table snapshot** is an immutable, identified table state: schema/spec/properties plus the exact live data, delete, index, and metadata files needed to read it.
- A **table root** is the authoritative catalog pointer, log version, or timeline state from which readers discover the current snapshot.
- An **atomic commit** changes visibility at one serialization point from a valid base state to a complete new state; it does not make every earlier object write simultaneous.
- **compare-and-swap (CAS)** publishes a new root only if the current root still equals the writer's expected base.
- **optimistic concurrency control (OCC)** lets writers prepare concurrently, then detects incompatible changes while committing.
- **rebase** applies a writer's logical action to a newer base after validating that its assumptions still hold.
- An **orphan file** was created by an abandoned/failed attempt but is not reachable from any committed retained snapshot.
- An **unknown commit outcome** occurs when the client loses the response and cannot yet tell whether publication succeeded.
- **snapshot retention** keeps old snapshots and referenced files available for active readers, time travel, branches/tags, audit, or recovery.
- A **transaction identifier** records application/batch progress atomically with table changes so a retry can detect prior success.

### Central model, mechanism, or theorem

Let snapshot $S_b$ reference live-file set $F_b$. A logical update proposes additions $A$ and removals $R$, producing

$$F_n=(F_b\setminus R)\cup A.$$

The writer creates immutable content and metadata under unique names, validates $R\subseteq F_b$ and operation-specific assumptions against the current state, then performs one conditional publication `CAS(root, b, n)`. Before success, readers pinning $b$ see all of $F_b$; after success, new readers see the complete $n$ while old readers may continue using $b$. A failed CAS publishes nothing and may rebase only after revalidation. Atomicity therefore comes from authoritative root/log publication plus immutability and retention—not from directory listing order, timestamps, or rewriting files in place.

### Critical invariants

- Every committed snapshot has a unique durable identity, parent/reference lineage, complete metadata graph, schema/spec IDs, operation/provenance, and integrity information.
- Readers resolve one authoritative root and pin one snapshot for the query; concurrent commits cannot change their file set mid-read.
- Data/delete/manifest/metadata files are immutable after publication and use collision-resistant attempt-scoped names.
- Exactly one writer wins a root/version serialization point; no committed root references missing, partial, corrupt, or unauthorized content.
- A retry validates assumptions against the new base; it never blindly republishes removals or replacements computed from stale state.
- Lost acknowledgments enter status checking; unknown success is not treated as failure and replayed without an idempotency check.
- Application progress/transaction IDs and table modifications commit together when exactly-once ingestion is claimed.
- Snapshot expiration and orphan cleanup distinguish reachable, active, retained, staged, unknown-outcome, and safely unreferenced files.
- Table services such as compaction, clustering, index/metadata rewrite, and cleanup obey the same conflict and publication contracts.
- Metrics and audit connect writer, attempt, base/new snapshot, logical operation, files/bytes, conflicts, retries, status checks, and cleanup.

### Common failures

Common failures include listing data directories to infer table state; overwriting live files; publishing metadata before all content is durable; using rename as if every object store supplied filesystem semantics; retrying an unknown commit and duplicating a batch; treating any CAS failure as safe automatic retry; rebasing a compaction after one input file was removed; deleting files because they are absent only from the latest snapshot; expiring a snapshot used by a branch, tag, audit, or active reader; using wall-clock modification time as commit order; committing data but not source progress; and claiming single-table atomicity as an atomic multi-table transaction.

### Compact example

Snapshot 41 references `{a,b,c}`. A writer creates immutable `d` and `e`, proposes removing `b`, writes new manifests/metadata for `{a,c,d,e}`, then conditionally swaps the table root from 41 to 42. Readers already pinned to 41 may still read `b`; new readers see 42 and never a half-written set. If another writer publishes 42 first, this writer's CAS fails. It may rebase an append, but a rewrite of `b` must fail or recompute if `b` is no longer live. Its unreferenced files are cleanup candidates only after commit outcome, retention, and concurrent-use safety are known.

### Connections

[LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) defines data files, [LSDS-031](031-shuffle-architecture.md) and [LSDS-063](063-exchange-operators.md) produce distributed writer outputs, [LSDS-062](062-coordinator-and-worker-architecture.md) supplies commit coordination, [LSDS-068](068-adaptive-query-execution.md) supplies attempt/epoch reasoning, [LSDS-069](069-federated-query.md) distinguishes multi-source consistency, and [LSDS-070](070-diagnosing-a-distributed-query-from-plan-to-network.md) supplies commit diagnostics.

## Governing Question

Distributed workers can write thousands of files, but a table update should become visible as one state transition. Readers must see either the old table or the new table—not a directory while files are still arriving. Concurrent appends, overwrites, deletes, compactions, schema changes, and maintenance must not lose one another. A driver failure after publication must not cause a retry to duplicate input.

Open table formats solve this by separating immutable content creation from metadata publication. Data and metadata files can be written speculatively because they are invisible until referenced by an authoritative snapshot. A small atomic operation—catalog pointer swap, new log version, or timeline completion—serializes visibility.

The governing question is how to define that serialization point and everything around it: snapshot construction, reader pinning, conflict validation, idempotent retry, lost acknowledgments, catalog/storage requirements, cleanup, retention, and operational evidence.

## Why This Matters

Object stores provide scalable durable blobs, not a transactional table by themselves. A directory may contain files from completed, failed, retried, or concurrent writers. File modification time does not define table membership. In-place mutation creates torn readers and races. Table metadata supplies an explicit, versioned set.

Snapshots enable consistent reads without holding writer locks, time travel, rollback, incremental change processing, audit, reproducible training/analysis, and safe table services. Atomic publication makes distributed jobs appear as one table commit even though content arrived over time.

The protocol is only as strong as its assumptions. An unsafe catalog, non-atomic version creation, overwritten log entry, prematurely deleted content, ambiguous commit response, or unversioned writer can corrupt the table. Operational discipline—status checks, retention, protocol compatibility, credential boundaries, and repair tooling—is part of correctness.

## Prerequisites and Retrieval

Review storage layouts in [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), worker serialization in [LSDS-008](008-serialization-across-workers.md), shuffle in [LSDS-031](031-shuffle-architecture.md), resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), distributed plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), coordinator/worker state in [LSDS-062](062-coordinator-and-worker-architecture.md), exchange in [LSDS-063](063-exchange-operators.md), AQE epochs in [LSDS-068](068-adaptive-query-execution.md), federation consistency in [LSDS-069](069-federated-query.md), and causal diagnosis in [LSDS-070](070-diagnosing-a-distributed-query-from-plan-to-network.md).

You should understand immutable objects, metadata graphs, sets, CAS/conditional writes, MVCC, OCC, snapshots, isolation, retries, idempotency, distributed task attempts, object-store semantics, checksums, retention, garbage collection, and authorization.

## Learning Objectives

After this module, you should be able to:

1. define snapshot identity, contents, lineage, and reader pinning independently of directory listing;
2. design prepare–validate–publish–confirm–clean commit phases over immutable files;
3. identify the authoritative serialization point and required catalog/storage primitives;
4. distinguish append, overwrite, delete, metadata, and table-service conflicts;
5. rebase compatible logical actions while rejecting stale destructive assumptions;
6. resolve lost acknowledgments and unknown commit outcomes without duplicate data;
7. atomically bind application transaction IDs/checkpoints to table changes;
8. manage branches, tags, time travel, rollback, retention, active readers, and orphan cleanup;
9. instrument commit latency, files/bytes, conflicts, retries, status checks, failures, and garbage; and
10. validate atomic visibility, concurrency, recovery, compatibility, security, and lifecycle behavior.

## Core Exposition

### Define a snapshot as an immutable metadata graph

A snapshot identifies table-level metadata and a complete reachable graph of manifests/indexes and data/delete files. It also records schema and partition-spec identities, properties/protocol features, operation, parent/lineage, sequence/version information, summary counts, and provenance as the format supports.

The set is explicit. Readers do not scan a directory and guess which files belong. Unreferenced files can coexist safely because reachability, not presence, defines table state. Persistent metadata structures reuse unchanged nodes across snapshots so commits need not rewrite all metadata.

Snapshot ID, log version, sequence number, commit timestamp, and branch reference are different concepts. Use the format's durable identity rather than wall-clock time when exact reproducibility matters.

### Pin readers to one root

A reader resolves a table through its authoritative catalog/log, loads one snapshot identity, and uses only that snapshot's reachable metadata. It may cache metadata under version-aware rules, but refresh must not splice a new root into an active scan.

Concurrent commits can advance the root while the reader continues. This is MVCC: immutable old versions remain readable until retention permits removal. No reader lock is required for ordinary snapshot reads, but the system must protect old files long enough.

Time-travel by timestamp requires a defined mapping from time to snapshot and cannot infer order reliably from object modification timestamps. Time-travel by exact snapshot/version/tag is clearer.

### Separate preparation from publication

A write has distinct phases:

1. bind base snapshot, logical operation, writer/attempt, application transaction, schema/spec, and authorization;
2. write immutable data/delete/index content under unique names;
3. collect selected task-attempt outputs and validate integrity/metrics;
4. write immutable manifest/metadata nodes describing the proposed new snapshot;
5. validate operation assumptions and conflicts against the current root;
6. atomically publish the new root/version;
7. confirm success, record lineage/progress, and release or schedule cleanup.

Content creation before publication is intentionally non-atomic and invisible. Publication must never point to content that has not completed durability and integrity checks.

### Choose one authoritative serialization point

Iceberg-style catalogs atomically replace a metadata-location pointer conditioned on the base. Delta-style logs atomically create or ratify the next version. Hudi-style timelines atomically transition an action to completed. The representations differ, but correctness needs one authoritative winner for each serialization position.

If a catalog manages the table, readers and writers must use it as source of truth. Direct filesystem writers can bypass catalog conflict checks and corrupt split-brain state. Conversely, filesystem/log protocols require storage operations such as atomic create-if-absent and consistent discovery defined by that protocol.

Document whether the commit becomes successful at catalog ratification, object visibility, pointer swap, or timeline completion. Cleanup and status checking depend on that definition.

### Treat data files as immutable

Never modify a file referenced by a committed snapshot. Updates and deletes create replacement data files, delete files, or log records according to the table format. Compaction writes new files and atomically replaces references to old ones.

Use globally unique or transaction/attempt-scoped paths. Speculative tasks may generate multiple candidates; the coordinator selects exactly one attempt per logical partition. Unselected outputs remain unreferenced and later eligible for guarded orphan cleanup.

Checksums, lengths, schemas, encryption metadata, partition values, record counts, and column statistics should be validated before publication. A root pointing at a corrupt or unauthorized file is atomically wrong.

### Model snapshot changes as set transformations

For base files $F_b$, additions $A$, and removals $R$,

$$F_n=(F_b\setminus R)\cup A.$$

Require $A$ use new immutable identities and, for destructive operations, validate $R$ is still live and belongs to the intended logical scope. Metadata/schema/spec/property changes are additional state transformations and conflicts, not merely file-set edits.

An append has $R=\varnothing$ and often rebases cleanly by attaching $A$ to a newer base. An overwrite computed from a predicate may need validation that no concurrent file now matches that predicate. A compaction may commit only if every rewritten input remains live and unchanged under its contract.

### Validate conflicts by logical operation

CAS failure means the base changed, not necessarily that logical operations conflict. Load the new current state and validate assumptions:

- append: are schema/spec/protocol compatible, and can new files be added without violating constraints?
- replace partitions/overwrite: did concurrent changes add or remove files in the replacement domain?
- row delete/update/merge: did concurrent data or delete files affect the predicate/key domain?
- schema/spec/property change: does the new state preserve IDs, compatibility, and ownership expectations?
- compaction/clustering: are all source files still live, and did conflicting deletes/rewrites appear?

Conflict detection too broad wastes work; too narrow loses updates or publishes invalid transformations. Define validation in table semantics, not just paths.

### Rebase actions rather than replay artifacts blindly

On compatible conflict, apply the logical action to the new base and regenerate the necessary metadata graph. Reuse immutable data files when their content and metadata remain valid. Do not reuse a stale manifest or removal list if its assumptions changed.

Bound attempts and total time with backoff/jitter. Hot tables can cause repeated conflicts and starvation. Admission, smaller conflict domains, write serialization, partitioning, branches, or a catalog service may be preferable under sustained contention.

A retry is a new commit attempt with lineage to the same logical transaction. Metrics should separate metadata-only rebase from expensive data recomputation.

### Resolve unknown commit outcomes

Suppose publication succeeds but the client loses the response. Retrying the logical data as a new transaction can duplicate rows. Treat transport timeout or coordinator failure around publication as **unknown**, not failed.

Status checking uses commit UUID, application transaction ID, proposed snapshot metadata/provenance, or catalog ratification record to determine:

- committed: return success and never republish;
- definitely not committed: retry under the normal conflict protocol;
- still unknown: keep checking within a bound, then surface an actionable unknown state and block unsafe automated replay.

Do not delete candidate files while outcome is unknown; they may be live. Recovery tools need durable identifiers and audit evidence.

### Make streaming/batch retries idempotent

For application ID $u$ and batch/checkpoint $k$, atomically record `(u,k)` in the same table commit as $A,R$. Before writing/retrying, read the table transaction state. If $k$ is already committed under the application protocol, skip data publication and advance recovery.

The application defines ordering and monotonicity semantics. The table protocol merely stores the identifier atomically unless it promises more. Do not claim exactly-once end to end if source offset acknowledgment, transformation state, or external side effects are outside the atomic boundary.

Task idempotency and commit idempotency are different. Unique file names prevent overwrite, but only transaction identity prevents duplicate logical batches.

### Define isolation honestly

Snapshot readers see one committed version. Concurrent writes are serialized by the commit point, but isolation level depends on conflict validation. Serializable isolation requires detecting predicate/domain conflicts relevant to the logical operations; snapshot isolation alone can allow write skew across disjoint physical files.

Append-only workloads can safely allow high concurrency. Deletes, merges, constraints, and table services need stronger validation. State guarantees per operation and engine integration, not just format marketing.

Single-table atomicity does not make updates across two tables atomic. A job can commit table A and fail before table B. Multi-table transactions require a shared catalog/coordinator protocol with group ratification, recovery, and readers that honor it, or application-level compensation/reconciliation.

### Respect object-store primitives

Object stores commonly provide atomic visibility for one completed object write and may provide strong reads/listing, conditional creates, generations, or ETags. Those properties are storage-specific and can evolve. Table protocols should use explicit conditional primitives, not assume filesystem rename directories or rely on list order.

Immutable uniquely named objects reduce coordination. A catalog CAS can point to new metadata without renaming data files. Conditional `If-Match`/generation checks prevent overwriting a root changed by another writer.

Strong listing is valuable operationally but does not replace snapshot metadata or transaction conflict validation. A perfectly consistent directory still contains files that should not be in the table.

### Use branches, tags, and write-audit-publish

A branch is a named mutable reference to a snapshot lineage; a tag is commonly a retained named snapshot. They support experiments, audits, reproducible milestones, and isolated write workflows. Reference-specific retention must protect reachable snapshots.

Write-audit-publish prepares and validates changes on a branch, then advances the production reference under ancestry and policy checks. Fast-forward is safe only if the target has not diverged and every intervening snapshot is acceptable. Otherwise merge/rebase needs defined semantics.

Branch isolation is not authorization by itself. Enforce who may create, write, validate, or advance each reference and audit the promotion.

### Design rollback as a new controlled transition

Rollback changes the current reference to an older valid snapshot or publishes a new snapshot restoring earlier content. It does not erase the intervening history immediately. Concurrent writers, schema/protocol compatibility, downstream consumers, and transaction IDs still matter.

Prefer a tested, auditable reference operation over copying old metadata into place. Verify the target's files have not been expired and that current readers/writers understand the transition.

Rollback of table metadata cannot undo external effects or already consumed downstream data. Coordinate recovery beyond the table boundary.

### Retain snapshots safely

Retention policy combines minimum snapshots, maximum age, branch/tag rules, active-query leases when used, streaming/incremental consumer watermarks, audit/legal holds, rollback objectives, and storage budget. The latest main snapshot is never a complete liveness set by itself.

A file may be deleted only when unreachable from every retained reference/snapshot and outside protection windows. Expiring a snapshot removes time-travel reachability; later physical deletion may be separate and retryable.

Long-lived readers without explicit leases need a retention floor longer than maximum supported query duration. Otherwise a pinned snapshot can reference deleted data.

### Clean orphans conservatively

Orphan cleanup enumerates candidate objects not reachable from retained committed metadata. It must also exclude recent/staged writers, unknown outcomes, in-flight attempts, external references, and storage/control-plane delay windows.

Use a safety age and, where possible, writer/transaction registry. Never delete solely because a file is absent from the latest snapshot. Emit a dry-run inventory, ownership/age/reachability reason, bytes, and approval/audit before destructive removal in high-risk environments.

Cleanup is idempotent and failure-tolerant. A missing orphan is success; a permission error is observable. Limit request rate and cost so cleanup does not harm writers/readers.

### Evolve protocol and schema with snapshots

Record protocol reader/writer versions or features in table metadata. A writer may enable a feature only after verifying deployed readers/writers will handle it or are fenced. Unknown required features must fail closed rather than ignore semantic state.

Schema and partition evolution use stable field/spec IDs. Existing files remain interpreted under the schema/spec recorded for their snapshot/file. Concurrent schema changes participate in commit conflicts and rebasing.

Upgrades need mixed-version tests, canaries, rollback constraints, and a clear point after which older clients are no longer authorized.

### Secure the commit boundary

Separate permissions for writing content, publishing table roots, managing branches/tags, changing schema/protocol/properties, expiring snapshots, and deleting objects. A worker usually needs write-only access to its attempt prefix, not authority to publish or delete the table.

Bind commits to actor, workload, application/transaction ID, base/new snapshot, operation, policy decision, files/bytes, and checksums. Encrypt content and metadata, protect keys across retention, and avoid sensitive values in filenames/statistics/provenance.

The catalog/root is a high-integrity control plane. Audit conditional failures, unauthorized changes, direct-storage writers, root rollback, and cleanup.

### Observe and test the protocol

Measure prepare/metadata/validation/publication/status-check latency, files/bytes, manifest depth, conflicts by operation/domain, rebase attempts, data reuse/recompute, unknown outcomes, catalog/storage errors, orphans, cleanup age/bytes, retained snapshots, active references, and reader planning failures.

Test failpoints before/after every durable write and immediately before/after publication response. Inject concurrent appends, overlapping overwrites/deletes/merges, compaction races, schema/protocol changes, worker speculation, coordinator crash, lost acknowledgment, stale catalog cache, corrupt/missing content, permission changes, clock skew, object throttling, and cleanup overlap.

Readers should observe only complete old or complete new snapshots. Differentially compare logical results. Verify retry idempotency and no lost update. Shadow cleanup and protocol changes, canary writer/reader combinations, and retain a kill switch that stops publication or deletion safely.

## Definitions and Notation

Let table state at snapshot $s$ be

$$S_s=(F_s,D_s,M_s,\Sigma_s,P_s,C_s),$$

where $F$ is data files, $D$ delete/change files, $M$ metadata graph, $\Sigma$ schema, $P$ partition/protocol properties, and $C$ commit/provenance state. The authoritative table root maps a reference such as `main` to $s$.

A logical operation $O=(A,R,V)$ contains additions, removals, and validation assumptions $V$. Applying it to base $b$ yields candidate $n=O(S_b)$ only if $V(S_b)$ holds. On current state $c\ne b$, rebase is permitted only if $V(S_c)$ holds and $O(S_c)$ preserves the operation's semantics.

Publication is a linearizable conditional operation

$$\operatorname{publish}(ref,b,n)\in\{\text{success},\text{conflict},\text{unknown},\text{failure}\}.$$

`unknown` is distinct because the serialization point may already have occurred. Let $Reach(Retained)$ be all objects reachable from retained snapshots/references. An orphan candidate $x$ is safely deletable only when $x\notin Reach$, no in-flight/unknown writer may reference it, and all safety-age/hold/lease rules pass.

## Mechanisms, Invariants, or Proof Structure

### Atomic visibility argument

1. Base root $b$ references a complete immutable graph and remains unchanged during preparation.
2. Writer creates $A$ and candidate metadata under unique names; no reader discovers them through table membership yet.
3. Writer validates content integrity and operation assumptions against current state.
4. Conditional publication has one winner and changes authoritative reference from $b$ to complete $n$ atomically.
5. A reader resolving before publication pins $b$; a reader resolving after pins $n$; neither constructs membership from directory timing.
6. Retention preserves every object reachable from both snapshots while supported readers may use them.

Thus readers see old or new membership, assuming authoritative root linearizability, immutable durable content, correct metadata construction, and retention. The argument does not cover multiple independent table roots.

### Conflict/rebase audit

1. Bind logical operation and base assumptions, not just output paths.
2. On conflict, load the authoritative new base.
3. Determine concurrent changes since the original base by file/domain/schema/spec/protocol/reference.
4. Re-evaluate predicate/key/file and metadata assumptions.
5. Reuse content only when invariant under rebase; regenerate metadata and recompute invalid data work.
6. Bound retries and preserve one application transaction identity.
7. Publish conditionally again or return a precise conflict.

### Unknown-outcome audit

1. Persist commit/transaction identity before publication.
2. After ambiguous transport failure, do not classify as ordinary failure.
3. Query authoritative catalog/log/timeline for identity, proposed snapshot, or ratification.
4. If committed, finalize locally; if definitely absent, retry; if unknown, continue bounded status checks and prevent duplicate replay.
5. Preserve files until outcome and retention are safe; escalate with identifiers and evidence.

## Alternatives and Trade-Offs

### Catalog pointer swap

A catalog can provide CAS, centralized policy, stable object identity, and fast current-root lookup. It is a high-availability control-plane dependency and must prevent direct bypass. Catalog-managed commits can support richer coordination but require every client to honor the catalog.

### Append-only log versions

Atomic create-if-absent for the next version produces an auditable serial log and self-contained table. Snapshot reconstruction may require checkpoints/compaction and consistent discovery as specified. Writers must never overwrite an existing entry.

### Timeline state transitions

Requested/inflight/completed states expose long-running actions and table services. They support recovery and richer scheduling but add state-machine and clock/coordination complexity. Only completed actions belong to ordinary reader snapshots under the defined contract.

### Pessimistic locking

Locks can serialize conflicting writers before expensive work, reducing late aborts. They reduce concurrency and require lease/fencing/recovery correctness. A lock without fenced publication can still allow a paused former holder to corrupt state.

### Optimistic concurrency

OCC maximizes parallel preparation when conflicts are rare and allows metadata-only append rebases. Under hot overlapping writes it wastes work and may starve. Conflict domains, early detection, branches, or serialization can improve behavior.

### Copy-on-write versus merge-on-read

Copy-on-write replaces data files and gives simple reads but increases write amplification. Merge-on-read publishes base plus change/delete logs, lowering write latency but increasing read/compaction complexity. Both still need snapshot atomicity and retention.

## Failure Modes and Misconceptions

- **“Files exist, so they are in the table.”** Only committed metadata reachability establishes membership.
- **“Atomic commit writes all files atomically.”** Files are prepared first; one metadata publication changes visibility.
- **“Strong object listing creates table transactions.”** It does not define membership, conflicts, or snapshot isolation.
- **“CAS conflict means the write must fail.”** Compatible logical actions may rebase after validation.
- **“All retries are safe.”** Destructive operations and unknown outcomes need validation/idempotency.
- **“A timeout means commit failed.”** Publication may have succeeded before the response was lost.
- **“Unique filenames guarantee exactly-once.”** They prevent overwrite, not duplicate logical batches.
- **“Latest snapshot defines deletable files.”** Old snapshots, branches/tags, readers, unknown writers, and holds may reference them.
- **“Commit time is snapshot identity.”** Clocks and publication timestamps have format-specific semantics.
- **“Snapshot isolation is always serializable.”** Predicate/write-skew conflicts require sufficient validation.
- **“Single-table atomicity covers the pipeline.”** Source offsets, other tables, sinks, and notifications need their own protocol.
- **“Rollback erases bad effects.”** It changes table visibility but not external consumers/effects or history immediately.

## Worked Examples

### Example 1

**Commit an append.** Writer reads base 10, creates three unique data files and one manifest, builds metadata 11, and wins `CAS(main,10,11)`. A concurrent reader pinned to 10 finishes unchanged. A later reader sees all three additions in 11.

### Example 2

**Rebase compatible appends.** Writers A and B both start at 20. A publishes 21. B's CAS fails, but B removes nothing and its files remain compatible. B rebuilds metadata on 21 and publishes 22. Both appends survive; B does not rewrite data.

### Example 3

**Reject stale compaction.** Compactor rewrites files `x,y` into `z`. Before it commits, a delete transaction removes/replaces `x`. The compactor cannot rebase by removing `x,y`; validation fails because `x` is no longer live. It recomputes on the new snapshot or abandons `z` as an orphan candidate.

### Example 4

**Resolve a lost acknowledgment.** A writer publishes transaction `(orders-stream,900)` but times out. Recovery finds that identifier and the proposed snapshot in the authoritative log, returns success, and skips data replay. Treating the timeout as failure would duplicate batch 900.

### Example 5

**Pin a reader.** Query Q resolves snapshot 51 and plans its file set. Commits 52 and 53 arrive during execution. Q continues with 51. Retention cannot delete files unique to 51 until Q's supported lifetime/lease and other policies permit it.

### Example 6

**Promote an audit branch.** A write advances `audit` from snapshot 70 to 73 while `main` remains 70. Validation passes. Because `main` has not diverged, a conditional fast-forward advances it to 73. If `main` were 72 on another lineage, promotion would require explicit merge/rebase semantics.

### Example 7

**Guard orphan cleanup.** File `u` is absent from current main but referenced by a retained tag, so it is live. File `v` is unreachable but only ten minutes old and may belong to an unknown writer, so it is protected. File `w` is unreachable from all retained references, older than the safety window, and absent from writer registries; dry-run lists it for deletion.

### Example 8

**Fence task attempts.** Two speculative attempts write different files for logical partition 8. The coordinator selects attempt 2 and places only its file in the candidate manifest. Attempt 1's output never becomes table data and is labeled by attempt for later cleanup.

### Example 9

**Separate tables.** A job publishes customer table snapshot 14, then fails before orders snapshot 31. Each table is internally atomic, but the pair is not. Recovery must compensate/reconcile, or a shared multi-table protocol must group publication; a dashboard must not claim one transaction.

### Example 10

**Execute a snapshot set transformation.**

<!-- bijux-verify: {"id":"snapshot-set-transition","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot_files=a.parquet,c.parquet,d.parquet,e.parquet\nfile_count=4\nremoved_count=1\norphan_candidates=unused.parquet\nidempotent_replay=yes\n","stderr":""}} -->
```python
base = {"a.parquet", "b.parquet", "c.parquet"}
additions = {"d.parquet", "e.parquet"}
removals = {"b.parquet"}
written_by_attempt = additions | {"unused.parquet"}

assert removals <= base
new_snapshot = (base - removals) | additions
orphan_candidates = written_by_attempt - additions

committed_transactions = {("orders-stream", 900)}
replay = ("orders-stream", 900)

print(f"snapshot_files={','.join(sorted(new_snapshot))}")
print(f"file_count={len(new_snapshot)}")
print(f"removed_count={len(removals)}")
print(f"orphan_candidates={','.join(sorted(orphan_candidates))}")
print(f"idempotent_replay={'yes' if replay in committed_transactions else 'no'}")
```

The set arithmetic does not implement catalog CAS, conflict validation, durability, or safe physical deletion; those are separate protocol obligations.

## Cross-Program Connections

- **Database systems:** MVCC, snapshots, isolation, serializability, OCC, write skew, constraints, and transactions define semantics.
- **Distributed systems:** consensus/catalog roots, CAS, retries, fencing, idempotency, unknown outcomes, leases, and recovery define publication.
- **Data engineering:** files, manifests, delete logs, schema/partition evolution, compaction, streaming checkpoints, and time travel define table state.
- **Object storage:** immutable objects, conditional writes, generations/ETags, listing, durability, throttling, and lifecycle define primitives.
- **Platform engineering:** catalogs, credentials, writer versions, quotas, audit, telemetry, repair tools, and kill switches operate commits.
- **Reliability engineering:** failpoints, status checks, rollback, retention, orphan cleanup, canaries, and disaster recovery bound failures.
- **Security and governance:** publication/delete authority, branches/tags, provenance, encryption, retention holds, and audit protect the control plane.
- **Performance engineering:** file/metadata write amplification, conflict waste, commit latency, planning depth, retention bytes, and cleanup cost establish value.

## References

1. Apache Iceberg. [Table Format Specification.](https://iceberg.apache.org/spec/) Current snapshot, manifest, metadata, sequence, reference, optimistic-concurrency, and atomic-swap requirements.
2. Apache Iceberg. [Reliability.](https://iceberg.apache.org/docs/nightly/reliability/) Current snapshot-tree, atomic update, concurrent-write, retry-cost, validation, and object-store reasoning.
3. Apache Iceberg. [Branching and Tagging.](https://iceberg.apache.org/docs/latest/branching/) Current snapshot references, branch/tag retention, write-audit-publish, fast-forward, and schema behavior.
4. Apache Iceberg. [Maintenance.](https://iceberg.apache.org/docs/latest/maintenance/) Current snapshot expiration, old metadata, orphan-file cleanup, rewriting, and retention guidance.
5. Apache Iceberg. [Configuration.](https://iceberg.apache.org/docs/latest/configuration/) Current commit/status-check retry bounds, history retention, garbage collection, metadata, and write behavior properties.
6. Delta Lake. [Transaction Log Protocol.](https://github.com/delta-io/delta/blob/master/PROTOCOL.md) Current atomic versions, actions, MVCC snapshots, transaction identifiers, checkpoints, features, staged/ratified/published commits, and writer requirements.
7. Delta Lake. [Storage and Concurrency Requirements.](https://github.com/delta-io/delta) Current atomic visibility, mutual exclusion, consistent discovery, transaction protocol, and project compatibility context.
8. Apache Hudi. [Concurrency Control.](https://hudi.apache.org/docs/concurrency_control/) Current atomic timeline commits, snapshot isolation, writer/table-service concurrency, locking, OCC/NBCC, and conflict detection.
9. Apache Hudi. [Technical Specification.](https://hudi.apache.org/learn/tech-specs/) Current timeline, MVCC, file slices, reader/writer expectations, action publication, metadata, and concurrency requirements.
10. Apache Hudi. [Timeline.](https://hudi.apache.org/docs/next/timeline/) Current requested/inflight/completed action states, instant/completion time, atomic transitions, and table-service action types.
11. Amazon Web Services. [Amazon S3 Data Consistency Model.](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) Current single-key atomicity and read/list-after-write behavior for PUT/DELETE operations.
12. Google Cloud. [Cloud Storage Consistency.](https://docs.cloud.google.com/storage/docs/consistency) Current object read/write/delete/list consistency and documented exceptions/propagation behavior.
13. Microsoft. [Conditional Headers for Blob Service Operations.](https://learn.microsoft.com/en-us/rest/api/storageservices/specifying-conditional-headers-for-blob-service-operations) Current ETag, `If-Match`, `If-None-Match`, time, tag, response, and operation semantics.

## Exercises

### Exercise 1

Design an end-to-end atomic append protocol for 2,000 distributed tasks with retry/speculation. Include base binding, attempt outputs, integrity, metadata, publication, unknown outcome, application transaction ID, cleanup, and observability.

### Exercise 2

Given base files `{a,b,c,d}`, additions `{e,f}`, and removals `{b,d}`, compute the candidate set. Then analyze concurrent append `{g}` versus concurrent rewrite removing `b`: which operation can rebase and what must be validated?

### Exercise 3

Design conflict validation for append, partition overwrite, equality delete/merge, schema evolution, and compaction. State assumptions, conflict domain, reusable work, retry, and failure behavior.

### Exercise 4

Design snapshot/reference retention and orphan cleanup for 8-hour queries, daily streaming checkpoints, 30-day audit tags, a legal hold, and writers whose commit result can remain unknown for one hour.

### Exercise 5

Design a validation and rollout campaign for a new catalog-backed commit implementation. Include storage primitives, concurrency histories, failpoints, unknown outcomes, mixed clients, security, performance, canaries, kill switches, and rollback.

## Answers to the Exercises

### Answer 1

Bind table/reference, base snapshot, logical append, application/batch ID, writer epoch, schema/spec/protocol, and policy. Each logical task writes immutable uniquely named files; speculation produces attempt-scoped candidates. Select one successful attempt per task, validate all 2,000 contributions, checksums, lengths, schemas, partitions, counts, encryption, and no duplicate logical outputs. Write immutable manifests and candidate metadata containing the transaction ID and provenance. Reload root, revalidate append compatibility, then conditionally publish. Persist commit identity before the call. On lost response, status-check the authoritative catalog/log for transaction/candidate before replay. If conflict is append-compatible, rebuild metadata on the new base while reusing files; bound retries. Record phase latencies, files/bytes, attempts/waste, conflicts, rebases, CAS/status checks, result, and cleanup. Unselected/abandoned files enter guarded cleanup only after outcome, retained reachability, active writers, and safety age permit.

### Answer 2

The candidate is `({a,b,c,d} - {b,d}) union {e,f} = {a,c,e,f}`. If another writer only appends `g`, the original remove/add operation may rebase onto `{a,b,c,d,g}` and produce `{a,c,e,f,g}` if its logical replacement domain excludes `g`, schemas/spec/protocol remain compatible, and `b,d` remain live. If a concurrent rewrite removes or replaces `b`, the original assumptions fail: it cannot remove/rewrite stale `b` again or publish output computed from it. It must recompute from the new file(s) or fail. Merely seeing a CAS conflict cannot decide; validate the logical domain and inputs.

### Answer 3

Append validates schema/spec/protocol and table constraints; it usually reuses all new files and regenerates metadata. Partition overwrite validates that no concurrent add/remove in its target partition/predicate domain changes the intended replacement; otherwise recompute/fail. Equality delete/merge validates data/delete files and key/predicate domain, including concurrent rows that could match; safe rebase may require re-reading/replanning. Schema evolution validates stable IDs, compatible types/defaults, concurrent field/property changes, and client protocol. Compaction validates every source data/delete file remains live and unchanged under its semantics; any overlapping rewrite/delete forces recomputation/failure, while disjoint changes can rebase. All retries retain one transaction identity, use new commit attempts, bound time, and never overwrite published artifacts.

### Answer 4

Retain every snapshot reachable from main, branches, 30-day audit tags, legal-hold references, streaming consumer checkpoints/watermarks, and active-query leases. Make the query lease exceed eight hours with renewal/grace, or set an age floor safely above maximum query duration. Preserve daily checkpoints long enough for recovery and record exact snapshot IDs. Legal-hold content has no automated expiry until authorized release. Protect every file from writers/in transactions whose outcome is unknown for at least the one-hour resolution bound plus clock/control-plane safety margin. Snapshot expiration first removes eligible metadata references; physical cleanup computes reachability across all retained references and excludes staged/inflight/unknown/recent files. Use dry-run inventories, reason/owner/age, bytes, approvals, rate limits, idempotent deletion, audit, and alerts for leases or unknown outcomes nearing limits.

### Answer 5

Verify the catalog's conditional publication is linearizable, durable, fenced, and authoritative; verify object writes are whole/immutable and all discovery/conditional primitives match the protocol. Generate histories of concurrent appends, overlapping/disjoint overwrites/deletes/merges, schema/spec/protocol changes, compaction, branching, promotion, rollback, and cleanup; check serializability/snapshot claims and no lost updates. Add failpoints before/after every data/metadata write, validation, ratification/publication, response, cache refresh, and cleanup; inject lost responses, coordinator/catalog/storage failure, throttling, corruption, stale clients, clock skew, and permission changes. Verify transaction idempotency and status checks. Run mixed reader/writer/version/feature tests and fence incompatible direct-storage clients. Audit least privilege, publication/delete separation, encryption, provenance, redaction, and legal retention. Shadow commits/read validation, canary noncritical tables, compare commit/plan/conflict/retry/storage metrics, kill-switch new publication/deletion on invariant breach, and roll back clients/catalog routing without abandoning unknown commits or deleting candidate files.
