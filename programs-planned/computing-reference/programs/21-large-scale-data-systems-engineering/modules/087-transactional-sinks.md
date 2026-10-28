---
module_id: LSDS-087
program: Large-Scale Data Systems Engineering
level: 2
module_number: 87
title: Transactional Sinks
status: complete
last_verified: 2026-09-04
---

# Transactional Sinks

## One-Page Review

### Governing question

How can a distributed dataflow make sink output visible exactly once despite replay, parallel attempts, checkpoint rollback, coordinator failure, and uncertain commit replies—and where must the claimed guarantee stop?

### Essential definitions

- A **sink transaction** groups output writes under one stable commit identity.
- A **committable** is durable metadata sufficient to validate, commit, abort, or recover prepared output.
- **prepare** closes an attempt's writes and makes them durable but not yet reader-visible.
- A **global decision** records whether one checkpoint/epoch's complete committable set commits or aborts.
- A **commit point** is the sink operation after which output is durably visible under the promised reader isolation.
- An **ambiguous outcome** occurs when the caller cannot tell whether commit took effect.
- **fencing** prevents an obsolete job, subtask, or transaction generation from committing.
- **read-committed visibility** excludes aborted and still-prepared output.
- A **transaction timeout** bounds prepared lifetime but can break recovery if shorter than outage duration.
- An **idempotent commit** returns the same successful outcome when repeated for the same identity.
- A **manifest commit** atomically publishes references to immutable attempt files rather than rewriting their bytes.

### Central model, mechanism, or theorem

For checkpoint/epoch $k$, subtask $s$, and attempt $a$, writer produces private output $W_{k,s,a}$ and committable

$$m_{k,s}=(j,k,s,g,u,h,n,b),$$

where $j$ is job identity, $g$ fencing generation, $u$ stable sink transaction/staging identity, $h$ content digest, $n$ records, and $b$ bytes. Coordinator accepts one valid committable per required subtask, stores set $M_k$, and durably decides `commit(k)` only after the corresponding source/state checkpoint completes.

Committer applies idempotent `commit(j,k,g,M_k)`: validate identity, epoch, completeness, checksums, destination/schema, and ownership; atomically publish all output or a committed manifest; record outcome; then acknowledge. Recovery queries outcome by the same identity and resumes commit or abort. Under durable preparation, one global decision, fencing, atomic/idempotent publication, and committed-only reads, many physical writes/commit calls yield one logical visible sink epoch.

### Critical invariants

- Job, checkpoint, subtask, attempt, transaction, and output identities are distinct and stable where required.
- Attempt output remains private until its checkpoint/epoch has one durable commit decision.
- Exactly one valid committable exists per required logical writer, or conflicts fail closed.
- Global commit is impossible before the complete source/state checkpoint and committable set are durable.
- Commit and abort are idempotent by stable transaction identity; unknown outcomes are queried, not guessed.
- Old job/subtask generations cannot prepare or commit after fencing.
- Readers use the isolation or manifest pointer required to hide prepared/aborted data.
- Transaction timeout exceeds checkpoint, outage, and recovery bounds with margin, or recovery handles expiry explicitly.
- Cleanup never removes prepared data needed by an undecided/committed epoch or an active recovery.
- The guarantee names destination, write mode, key/partition, visibility, readers, retention, and failure domains.

### Common failures

Common failures include writing directly to final names; generating a new transaction ID on retry; treating a successful flush as commit; committing subtasks independently before global checkpoint completion; losing prepared handles from checkpoint state; accepting duplicate committables with different content; retrying an unknown commit as a new transaction; relying on leases without destination-enforced fencing; letting consumers read uncommitted records; expiring transactions during a long outage; deleting multipart uploads or staging files too early; using append for correction when replacement is intended; assuming an atomic file rename exists in object storage; and claiming exactly once for destinations or readers outside the protocol.

### Compact example

Checkpoint 24 expects subtasks 0–2. Attempts stage 40, 35, and 25 records under stable identities, for 100 total. Subtask 1's acknowledgement is duplicated with the same digest and is accepted idempotently; a changed digest would fail. After checkpoint 24 completes, the coordinator publishes one commit decision. The first commit response is lost, so recovery queries transaction `orders/job-7/24`, finds `committed`, and does not republish. Readers using committed visibility see 100 records once.

### Connections

[LSDS-047](047-checkpoint-barriers.md) supplies barriers, [LSDS-048](048-state-snapshots-and-recovery.md) supplies sink recovery state, [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies stable effect identity, [LSDS-083](083-coordinator-failure.md) supplies decision recovery, [LSDS-085](085-checkpoint-based-recovery.md) supplies checkpoint completion, and [LSDS-086](086-exactly-once-state-updates.md) supplies atomic state/progress semantics.

## Governing Question

An engine may restore its internal state perfectly and still duplicate output. A sink writer can send records, lose its acknowledgement, and be retried. A checkpoint can roll back after some destination writes are visible. A coordinator can fail between recording a global decision and notifying committers. Transactional sinks close this final boundary by connecting dataflow commit epochs to destination visibility.

“Transactional” alone is insufficient. A database transaction per record may commit before the engine knows the input is durable. A producer transaction may be invisible only to consumers configured for committed reads. A table commit may atomically swap metadata while orphan data files remain. An HTTP endpoint may offer no prepare or outcome-query operation at all.

The governing question is how writer attempts produce private durable output, how their handles join one checkpoint decision, how commit becomes atomic and retryable, how stale writers are fenced, how readers observe results, and how recovery resolves every prepared, committed, aborted, expired, or unknown transaction.

## Why This Matters

Transactional sinks protect ledger rows, change streams, table snapshots, files, indexes, and downstream topics from replay duplicates and partial epoch visibility. Without them, an upstream exactly-once claim ends before the output consumers who depend on it.

They also create operational obligations. Prepared transactions hold locks, connections, producer IDs, multipart uploads, staging storage, or catalog leases. Commit latency delays visibility and checkpoint completion. A destination outage can accumulate undecided epochs. Timeouts that protect the destination can invalidate the engine's recovery horizon.

Different sinks need different publication mechanisms: database/XA prepare and commit, log transactions with committed reads, immutable files plus atomic metadata, conditional versioned upserts, or destination-native idempotency. The system must prove the mechanism used, not infer safety from connector branding.

## Prerequisites and Retrieval

Review checkpoint barriers in [LSDS-047](047-checkpoint-barriers.md), snapshots in [LSDS-048](048-state-snapshots-and-recovery.md), replay-safe effects in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), coordinator decisions in [LSDS-083](083-coordinator-failure.md), recovery points in [LSDS-085](085-checkpoint-based-recovery.md), and exactly-once state in [LSDS-086](086-exactly-once-state-updates.md).

You should understand atomic commit, two-phase commit, write-ahead logs, idempotency, fencing, transaction isolation, source offsets, checkpoints, object storage, immutable files, manifests, compare-and-swap, schema/partition evolution, and garbage collection.

For diagnosis retain job/graph/checkpoint/subtask/attempt/generation IDs, transaction/staging ID, destination/table/topic/partition/schema, committable digest/count/bytes, prepare/decision/commit/abort timestamps and outcomes, checkpoint status, reader isolation, transaction timeout/age, retry count, unknown-outcome lookup, fenced calls, orphan ownership, cleanup history, and source-to-sink reconciliation totals.

## Learning Objectives

After this module, you should be able to:

1. define a transactional sink's exact visibility boundary;
2. separate writer, committable, coordinator, committer, and reader responsibilities;
3. design stable identities, private staging, preparation, and global commit;
4. couple sink decisions to a complete source/state checkpoint;
5. make prepare, commit, abort, and outcome lookup idempotent;
6. fence stale job and writer generations at the destination;
7. compare database, log, table/manifest, file, and idempotent-upsert sinks;
8. size timeouts, concurrency, retention, and cleanup safely;
9. reconcile prepared, committed, aborted, expired, and unknown outcomes; and
10. verify exactly-once visibility with crash injection and reader-side evidence.

## Core Exposition

### Define the visible effect

State whether the sink appends facts, replaces keyed state, publishes a table snapshot, finishes files, or calls a command endpoint. Define logical uniqueness, ordering, visibility point, and authorized readers. One committed epoch may contain many records; one logical business effect may span epochs and need a separate key.

Name the guarantee: no missing or duplicate rows for admitted source positions in committed table snapshots, for example. Record-level “delivery” is ambiguous when corrections, updates, deletes, compaction, and late data change physical representation.

### Separate writer and committer

Writers run in parallel and fail often. They stage under attempt-private names or destination transactions, then emit compact committables. A committable includes stable logical owner, attempt provenance, destination, content/count/checksum, schema/partition metadata, and everything recovery needs without the original process.

Committers validate and publish. Separating them prevents a task from making global output visible before the engine decides its checkpoint. The committer may be parallel by destination partition, followed by a global catalog/manifest commit.

### Prepare durable private output

Prepare must durably close the write set without exposing it to normal readers. Database sinks use prepared transactions or a durable outbox/staging table. Log sinks end a producer transaction but wait to commit. File/table sinks close immutable data files and persist their metadata.

A flush only moves buffers; it does not prove isolation, completeness, or commit. Preparation must survive the worker, coordinator, and required storage failures. Credentials and encryption keys must remain usable through recovery.

### Form the complete committable set

The coordinator knows which logical subtasks/partitions are required for checkpoint $k$. It accepts one content-consistent committable per logical writer and persists $M_k$ in checkpoint/coordinator state. Duplicate acknowledgements are harmless only when identities and digests match.

Missing writers prevent completion. Speculative attempts compete through an explicit winner rule; their outputs never merge accidentally. Rescaling maps old and new writer identities without letting both own the same transaction namespace.

### Bind commit to checkpoint completion

The sink epoch may commit only after the source positions and operator state that produced it form a durable complete checkpoint. If sink output commits earlier and the engine rolls back, replay duplicates it. If the checkpoint completes but sink preparation is absent, recovery cannot finish output.

Persist the global decision before sending commit calls. A coordinator crash then recovers the decision and repeats idempotent notification. Do not infer decision from whichever destination calls happened to finish.

### Make every operation idempotent

`prepare(u)`, `commit(u)`, `abort(u)`, and `status(u)` use stable identity $u$. Repeated identical commit returns the committed receipt. Abort after committed reports conflict/committed rather than deleting output. Same identity with different digest fails.

When a response is lost, query status. Creating $u'$ and sending the same data again is a second transaction, not a retry. Destinations without durable outcome lookup need an idempotency ledger or a publication design whose final identity can be conditionally checked.

### Fence old generations

Include job incarnation and writer generation in transactional IDs, and enforce ownership at destination/catalog. A stopped or partitioned old job must not commit after a replacement restores. Unique transaction prefixes prevent unrelated jobs from aborting or reusing one another's transactions.

Fencing also applies to abort and cleanup. An obsolete worker must not delete the current owner's staging data. Authorization should scope each job to its intended destination and namespace.

### Enforce reader isolation

Producer-side transactions are meaningful only if readers hide uncommitted/aborted records. For logs, require committed isolation along the protected path. For tables, readers resolve one atomic metadata snapshot. For files, readers consume a committed manifest or finished-name contract rather than listing staging prefixes.

Caches, CDC feeds, indexes, materialized views, and exports can observe different boundaries. Include them in the contract or label them downstream at-least-once consumers.

### Database and XA sinks

One database can atomically update destination rows and an idempotency/epoch ledger. Cross-resource XA adds prepare/recover/commit but holds database resources and depends on driver/database support. Configure prepared-transaction capacity, connection limits, recovery credentials, and timeout.

Avoid retry settings that create new transactions after ambiguous writes. Verify isolation, unique keys, constraint conflicts, deadlock retry, and whether commit outcome is queryable after client/session loss.

### Transactional log sinks

Transactional producers group writes, and sometimes consumed offsets, under stable producer/transactional identity. Broker epochs fence prior producers; consumers must read committed. Commit frequency trades visibility latency and transaction overhead.

Transaction timeout must exceed worst checkpoint plus restart/recovery time. Expiry is not merely a performance event: the broker may abort work the engine expects to commit. Monitor open transaction age and last stable offset.

### File and table sinks

Writers create immutable attempt files. A committable lists path/generation, size, record count, checksum, partition, schema, and statistics. Global commit conditionally publishes a manifest/catalog snapshot once; retries recognize the same snapshot/commit ID.

Object stores generally do not offer a cross-object atomic rename. Metadata publication supplies the atomic point. Orphan cleanup is reachability-based and delayed past undecided epochs, restore leases, multipart-upload lifetime, and catalog uncertainty.

### Upsert and idempotent destinations

If a destination cannot prepare, a stable primary key plus monotonic source version and conditional write can make repeated replaceable effects converge. Equal key/version must compare payload fingerprint; older versions are ignored; conflicting equal versions fail.

This is not a transactional append and may not preserve atomic multi-record visibility. Declare whether readers can observe a partially advanced epoch and whether that is acceptable.

### Operate backlog, timeouts, and cleanup

Bound concurrent prepared epochs by destination capacity. Apply admission/backpressure before locks, staging bytes, or transaction IDs exhaust. Choose timeout greater than checkpoint duration plus maximum detection, scheduling, restore, and commit recovery, with measured margin.

Reconciler enumerates engine decisions and destination states, repairs missing notifications, classifies unknowns, aborts proven losers, and removes unreachable orphans after safety delay. Never clean solely by age while ownership is uncertain.

### Observe and prove visibility

Measure staged/prepared/committed/aborted/expired/unknown transactions; records/bytes/committables; prepare/decision/commit latency; retries; fenced calls; reader lag; open age; timeout headroom; orphan bytes; cleanup; and source-state-sink reconciliation.

Kill writers/coordinator/committer before and after prepare, checkpoint completion, durable decision, destination commit, and acknowledgement. Lose responses, duplicate/change committables, expire transactions, split ownership, corrupt staging, and race cleanup. Read through the promised isolation and compare visible output to a reference.

## Definitions and Notation

Let:

- $k$ be checkpoint/epoch and $s$ logical sink subtask;
- $a$ be physical attempt and $g$ fencing generation;
- $W_{k,s,a}$ be private staged output;
- $m_{k,s}=(j,k,s,g,u,h,n,b)$ be its committable;
- $M_k=\{m_{k,s}\}$ be the complete committable set;
- $d_k\in\{commit,abort\}$ be the durable global decision;
- $V_k$ be reader-visible output after commit;
- $t_p,t_d,t_c$ be prepare, decision, and commit times;
- $T_x$ be destination transaction timeout and $T_r$ worst recovery duration;
- $N_s,N_c,N_v$ be staged, committed, and visible record counts.

Timeout safety needs a measured policy such as $T_x>T_{checkpoint}+T_r+T_{commit}+M$, not equality at average duration. Count equality alone is insufficient: verify stable IDs/content and exclusions. Commit latency $t_c-t_p$ differs from checkpoint duration and reader visibility lag.

## Mechanisms, Invariants, or Proof Structure

### No-early-visibility proof

Attempt data is private and promised readers expose only committed transactions/manifests. Before durable decision and publication, none of $W_{k,s,a}$ belongs to $V_k$. Failed and losing attempts therefore cannot leak into the protected view.

### Atomic-epoch proof

Coordinator decides commit only for complete $M_k$ after checkpoint $k$ is durable. Destination atomically commits the transaction or one manifest pointer. Thus readers observe all declared output for $k$ or none, subject to the destination's stated isolation.

### Retry and ambiguity proof

All retries use $u$ and identical digest $h$. After a lost reply, status/commit returns the recorded outcome; it cannot create a second identity. Therefore repeated commit messages add no second visible epoch.

### Fencing proof

Destination accepts only current generation $g_c$. Once replacement generation is installed, prior prepare/commit/abort calls fail. This prevents restored and stale jobs from publishing competing histories.

### Adversarial verification

Test empty/nonempty epochs, no/one/many writers, duplicates/conflicts/missing handles, worker/coordinator/committer crash at every boundary, lost responses, timeout, destination failover, stale jobs, reader isolation, schema/partition change, rescale, corrupted/missing staging, cleanup races, and old-checkpoint restore.

## Alternatives and Trade-Offs

| Sink pattern | Strength | Cost or boundary |
|---|---|---|
| Flush on checkpoint | At-least-once durability | Replay may duplicate visible data |
| Per-record idempotent upsert | Low coordination for replaceable keys | No atomic multi-record epoch; retention/version rules |
| Database transaction/ledger | Strong local atomicity and queryable outcome | Destination contention and transaction scope |
| XA/two-phase commit | Atomic prepared work across supported resources | Blocking/resources, configuration, recovery complexity |
| Transactional log | Atomic partitions and committed reads in one log system | Visibility delay, timeouts, consumer isolation |
| Immutable files plus manifest | Scalable writes and atomic table snapshot | Orphans, catalog conflicts, metadata/cleanup burden |
| Shadow materialization and swap | Strong isolation for backfill/rebuild | Extra storage and explicit cutover |

Prefer the narrowest mechanism that enforces the real visibility contract. A weaker mechanism may be correct when outputs are naturally idempotent or duplicates are explicitly tolerated and reconciled.

## Failure Modes and Misconceptions

1. **Flush equals commit.** Durable buffers can still be visible early or replayed.
2. **New retry transaction.** It defeats idempotent outcome recovery.
3. **Subtask early commit.** Readers observe a partial epoch before global success.
4. **Incomplete committable set.** A completed checkpoint cannot finish all output.
5. **Conflicting duplicate handle.** Same identity names different bytes.
6. **Unknown means aborted.** Blind replay can duplicate a successful commit.
7. **Lease-only ownership.** Paused old writers can publish after reassignment.
8. **Uncommitted reads.** Consumers observe prepared or aborted records.
9. **Short timeout.** Destination expires transactions during engine recovery.
10. **Final-name overwrite.** Attempts race and destroy provenance/content.
11. **Object-store rename assumption.** Multi-object publication is not atomic.
12. **Age-only cleanup.** Recovery-required staging is deleted.
13. **Connector-name guarantee.** Actual mode/config/version/read isolation may differ.
14. **Count-only reconciliation.** Duplicate/missing identities can cancel numerically.
15. **Boundary inflation.** Downstream exports/APIs are outside the committed sink.

## Worked Examples

### Example 1

Three writers prepare 40, 35, and 25 rows. Commit waits for all three and the checkpoint decision; 100 visible rows appear atomically.

### Example 2

A duplicate committable has the same transaction ID and digest, so it is idempotent. The same ID with another digest blocks the epoch.

### Example 3

Commit succeeds but its reply is lost. Recovery queries the same ID, observes `committed`, and acknowledges without replaying output.

### Example 4

A Kafka-like transaction is committed, but a consumer configured to read uncommitted records had already seen aborted attempts. That consumer is outside the exactly-once visibility contract.

### Example 5

Worst checkpoint plus recovery plus commit is 18 minutes; a 15-minute transaction timeout is unsafe even if median completion is 40 seconds.

### Example 6

An epoch-8 producer resumes after epoch 9 is installed. Destination fencing rejects its commit rather than relying on its expired lease.

### Example 7

Four Parquet files are staged. One atomic table-manifest pointer exposes them; listing their staging prefix is not a supported read path.

### Example 8

An upsert repeats key 7/version 12 with the same digest and converges; key 7/version 12 with a changed digest is quarantined.

### Example 9

Cleanup finds an old multipart upload but an undecided checkpoint still references it. Reachability keeps it despite age.

### Example 10

The executable fixture validates one complete committable set and idempotently resolves a lost commit acknowledgement.

<!-- bijux-verify: {"id":"transactional-sink","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"checkpoint=24\nrecords=100\ncommittables=3\nduplicate_acks=1\ndecision=commit\ncommit_calls=2\nvisible_commits=1\nstatus=committed\n","stderr":""}} -->
```python
expected = {0, 1, 2}
acks = [(0, "a", 40), (1, "b", 35), (1, "b", 35), (2, "c", 25)]
committables = {}
duplicate_acks = 0
for subtask, digest, records in acks:
    value = (digest, records)
    if subtask in committables:
        assert committables[subtask] == value
        duplicate_acks += 1
    else:
        committables[subtask] = value

assert set(committables) == expected
transaction = "orders/job-7/24"
outcomes = {}
commit_calls = 0
for _ in range(2):  # first acknowledgement is lost
    commit_calls += 1
    outcomes.setdefault(transaction, "committed")

print("checkpoint=24")
print(f"records={sum(value[1] for value in committables.values())}")
print(f"committables={len(committables)}")
print(f"duplicate_acks={duplicate_acks}")
print("decision=commit")
print(f"commit_calls={commit_calls}")
print(f"visible_commits={len(outcomes)}")
print(f"status={outcomes[transaction]}")
```

## Cross-Program Connections

- **Distributed systems:** atomic commit, consensus decisions, epochs, fencing, and ambiguity recovery govern publication.
- **Database systems:** transactions, XA, WAL, isolation, constraints, and recovery implement database sinks.
- **Streaming:** checkpoints, replay, committables, and watermarks connect source/state progress to output.
- **Storage:** immutable files, multipart uploads, manifests, catalogs, checksums, and GC implement table/file sinks.
- **API engineering:** stable idempotency identities and status lookup handle nontransactional protocols.
- **Platform engineering:** credentials, transaction capacity, rollout fencing, telemetry, and reconciliation sustain guarantees.
- **Security:** namespace authorization, encryption, audit, and tenant isolation protect prepared and committed data.
- **Reliability engineering:** timeout budgets, fault injection, reader probes, and identity reconciliation prove behavior.

## References

1. Apache Flink, [Data Sinks](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/sinks/). Current. Defines writers, committables, committers, state, and two-phase commit support.
2. Apache Flink, [Fault Tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/). Current. States transactional/idempotent sink requirements for end-to-end exactly once.
3. Apache Flink, [Kafka DataStream Connector](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/). Current. Documents transactional identity, checkpoints, committed visibility, and timeout caveats.
4. Apache Flink, [Kafka Table Connector](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/kafka/). Current. Documents delivery modes and consumer isolation.
5. Apache Flink, [FileSystem Connector](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/filesystem/). Current. Documents part-file lifecycle, checkpoint publication, multipart uploads, and recovery caveats.
6. Apache Flink, [JDBC Connector](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/datastream/jdbc/). Development documentation. Documents XA requirements, resource capacity, and retry constraints.
7. Apache Kafka, [Producer Configurations](https://kafka.apache.org/10/configuration/producer-configs/). Version 10. Documents idempotence, transactional IDs, and transaction timeout configuration.
8. Apache Kafka, [Consumer Configurations](https://kafka.apache.org/10/configuration/consumer-configs/). Version 10. Documents committed versus uncommitted isolation.
9. Apache Spark, [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html). Current. Documents `foreachBatch` identifiers, deduplication, and fault-tolerant sink semantics.
10. Apache Iceberg, [Flink Writes](https://iceberg.apache.org/docs/latest/flink-writes/). Current. Documents checkpoint-driven exactly-once table writes.
11. Apache Iceberg, [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Current. Describes atomic metadata commits, optimistic concurrency, and retry.
12. Apache Flink, [Fault Tolerance Guarantees of Data Sources and Sinks](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/datastream/guarantees/). Development documentation. Catalogs connector-specific delivery boundaries.

## Exercises

### Exercise 1

Design writer, committable, decision, commit, reader, and recovery states for a three-subtask transactional sink.

### Exercise 2

Explain how to recover when destination commit may have succeeded but the coordinator lost the reply.

### Exercise 3

Design an object-table sink without assuming atomic rename or trusting prefix listing as committed state.

### Exercise 4

Calculate and justify transaction-timeout requirements when checkpoint, outage detection, resource allocation, restore, and commit have heavy tails.

### Exercise 5

Design a validation campaign proving sink exactly-once visibility across writer, coordinator, destination, and reader failures.

## Answers to the Exercises

### Answer 1

Each writer stages private durable output and emits one stable ID/digest/count committable. Coordinator persists the complete three-handle set with checkpoint state, then durably records commit or abort. Committer applies that decision idempotently under the current fencing generation. Readers expose only committed transaction/manifest state. Recovery enumerates decisions and destination status, repeats missing commit/abort by the same IDs, rejects conflicts, and delays orphan cleanup until no undecided or restoring owner references data.

### Answer 2

Do not create a new transaction. Recover the durable global decision and query destination status using the original transaction ID and generation. If committed, record/return the existing receipt; if prepared and decision is commit, repeat idempotent commit; if aborted, reconcile against the decision and fail or replay under policy; if unknown, retain staging and escalate/reconcile. Fence older coordinators throughout.

### Answer 3

Write immutable attempt files with unique paths/generations and checksums. Prepare a committable containing every file and partition/schema statistic. After checkpoint completion, conditionally commit one catalog snapshot/manifest referencing the complete winning set and stable epoch ID. Readers resolve only catalog snapshots. A retry detects the same snapshot ID/content; conflicts fail. Reachability plus active leases governs orphan/multipart cleanup, and corrupt or missing files block publication.

### Answer 4

Use high-percentile or bounded checkpoint duration plus failure detection, scheduling/resource wait, state restore, decision recovery, destination reconnect, and commit time, then add operational margin. The destination timeout must exceed that sum for supported failures and remain within destination capacity/security policy. Measure open-transaction age and headroom; if a required outage can exceed the maximum allowed timeout, use another sink protocol or accept/document a weaker recovery guarantee.

### Answer 5

Kill each writer before/after prepare and acknowledgement; kill coordinator before/after checkpoint completion and durable decision; kill committer before/after destination commit and acknowledgement. Duplicate, omit, and alter committables; lose responses; expire transactions; fail over destination; race old/new generations and cleanup; corrupt staging; restore older checkpoints. Read only through promised isolation and compare stable IDs/content to source/state reference, not counts alone. Track every prepared item to committed, aborted, retained-unknown, or safely deleted disposition.
