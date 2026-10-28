---
module_id: LSDS-041
program: Large-Scale Data Systems Engineering
level: 1
module_number: 41
title: Logs as Distributed Input
status: complete
last_verified: 2026-09-03
---

# Logs as Distributed Input

## One-Page Review

### Governing question

How can a distributed processor treat a partitioned append log as durable, replayable input while correctly interpreting offsets, ordering, visibility, replication, retention, compaction, transactions, schema evolution, and finite snapshots?

### Essential definitions

- A **log partition** is an ordered append sequence with a separately advancing position space; ordering is normally guaranteed within that partition, not across a topic.
- A **record** carries payload plus key, headers, timestamp, schema/encoding identity, producer metadata, and broker-assigned position as supported by the system.
- An **offset** or **entry ID** names a position in one log partition/ledger; it is not inherently a global record ID, event timestamp, or exact count of readable records.
- The **log-start offset** $L_p$ is the earliest position currently available in partition $p$; the **high/end offset** $H_p$ is an exclusive upper read boundary under a named visibility rule.
- A **snapshot vector** fixes one end position $E_p$ for every included partition so an unbounded log can be read as finite input.
- **retention** removes old segments according to time, size, acknowledgement/backlog, or administrative policy; replay before $L_p$ is impossible from that log.
- **compaction** selectively removes superseded keyed records while generally preserving remaining order and position identity; it is not ordinary time retention or a full history.
- A **tombstone** is a key-associated deletion record whose own retention determines whether a rebuilding consumer observes the deletion.
- An **acknowledged append** has only the durability/visibility promised by the chosen acknowledgement, quorum/replica, flush, and failure configuration.
- A **leader/writer epoch** fences obsolete writers and disambiguates positions across failover or truncation; position alone may not prove lineage.

### Central model, mechanism, or theorem

For each selected partition $p$, freeze a read interval $[S_p,E_p)$ with $L_p\le S_p\le E_p\le H_p$ under one metadata snapshot and visibility policy. The finite distributed input is the union of readable records whose partition-local positions fall inside those intervals. A checkpoint stores the next position $C_p$ plus topic/partition identity, leader or lineage epoch when exposed, source configuration, and processing snapshot identity.

Positional span $E_p-S_p$ is not necessarily readable record count. Compaction, control batches, aborted transactions, filters, sparse ledger schemes, and retention holes can reduce application-visible records. Similarly, lag $H_p-C_p$ is a positional measure unless the implementation explicitly defines it otherwise.

Durability is conditional: producer acknowledgement policy, minimum in-sync/quorum size, writer fencing, committed boundary, replica placement, storage failure assumptions, and unclean recovery jointly determine which acknowledged records survive. Replayability further requires retention horizon to exceed detection, repair, backfill, and checkpoint age with margin.

### Critical invariants

- Topic/stream namespace, cluster, partition identity, position type, and writer/leader epoch are never conflated.
- Records consumed from one partition respect the source's committed order; no cross-partition total order is invented.
- Start/end bounds use declared inclusive/exclusive semantics and one visibility/isolation rule.
- Acknowledged, replicated, committed, flushed, visible, consumed, checkpointed, and externally effected are distinct states.
- Producer retries use supported idempotence/deduplication identity or downstream logic tolerates duplicates; sequence scope and expiry are explicit.
- Checkpoints store the next unread position only after corresponding operator state/effects satisfy their consistency contract.
- Retention, compaction, tombstone, tiering, and deletion policies preserve the required replay/rebuild horizon or fail visibly.
- Schema, key normalization/partitioning, timestamp semantics, transaction markers, and codec versions remain interpretable during replay.
- Metadata, data blocks, checksums/MACs, authorization, encryption, quotas, and tenant/region placement are validated.
- Partition discovery and snapshot membership are versioned; newly created partitions cannot silently enter a supposedly finite input.

### Common failures

Common failures include assuming topic-wide order; treating offsets as timestamps or stable global IDs; using $H-C$ as an exact unread-record count after compaction; starting at “latest” and claiming completeness; committing position before durable effects; confusing producer acknowledgement with end-to-end processing; retrying non-idempotent appends; allowing an obsolete writer after failover; reading uncommitted transactional data unintentionally; rebuilding after retention has passed the needed start; assuming compacted logs contain every change or a point-in-time snapshot; dropping tombstones too early; changing partition count without analyzing key routing; using broker timestamps as trusted event time; evolving schemas without old readers/defaults; discovering partitions during a bounded run without a policy; and exposing payloads, keys, headers, offsets, or credentials in logs and metrics.

### Compact example

Partition 0 currently exposes $L_0=120$, $H_0=180$ and partition 1 exposes $L_1=40$, $H_1=95$. A bounded job freezes $S=(130,50)$ and $E=(175,90)$, giving positional spans 45 and 40. It does not promise 85 application records: compaction and aborted transactions may leave fewer. If a checkpoint requests partition 0 position 110, the 10-position gap below $L_0$ is an explicit retention loss; silently resetting to 120 changes the dataset. If a new partition appears after the snapshot vector is frozen, it belongs to a later run unless the manifest is deliberately revised.

### Connections

[LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md) provide storage and metadata failure models; [LSDS-027](027-task-retry-and-speculation.md) provides attempt identity. [LSDS-042](../ROADMAP.md) assigns partition consumption, [LSDS-044](../ROADMAP.md) separates event time from log order, and [LSDS-047](../ROADMAP.md) through [LSDS-050](../ROADMAP.md) connect offsets with checkpoints, recovery, backpressure, and effect-safe replay.

## Governing Question

A distributed log turns continuously arriving records into an addressable sequence that many independent processors can revisit. It decouples producer availability from consumer speed, enables recovery and backfill, and gives stream processors a durable input boundary. But “the log” is not one universal sequence. It is typically a set of partitions, segments, replicas, leaders or writers, metadata epochs, retention policies, and consumer positions.

An application sees a record only after several decisions: which producer partitioner routed it; whether the append was acknowledged; whether it crossed a committed/visible boundary; which isolation mode the reader chose; whether retention or compaction preserved it; whether schema and authorization still allow decoding; and whether the processor's checkpoint starts before it.

Offsets make replay efficient but easy to misunderstand. An offset is scoped to a partition. Two partitions can both have offset 10 without ordering relation. Gaps can be legitimate after compaction. Timestamps can be out of order or broker-assigned. A position can be reused or invalidated across systems with truncation unless an epoch/lineage identity accompanies it.

The governing question is how to define a source contract that turns these storage facts into correct input: exact partition membership and bounds, explicit visibility, durable append assumptions, replay horizon, schema/key/timestamp semantics, failure identity, and lifecycle controls.

## Why This Matters

Logs are the bridge between online events and scalable processing. They absorb bursts, isolate producers from downstream maintenance, allow multiple derived views, and let a failed processor replay. A finite batch can be defined by capturing end positions; a continuous job advances them through checkpoints.

The same decoupling hides risk. A consumer may be weeks behind while retention is seven days. A key-routing change can split one entity's order across partitions. A producer timeout can cause a duplicate. An unclean leader choice can lose an acknowledged suffix. A compaction tombstone can disappear before a state rebuild sees it. A transaction-aware reader and an uncommitted reader can process different logical inputs from the same bytes.

Logs are also operational databases. Partition count, segment size, replication, indexes, page cache, tiered storage, fetch batching, quotas, and backlog determine capacity and tail latency. Too many partitions burden metadata, recovery, file descriptors, and elections. Too few cap parallelism and create hot leaders.

Intermediate position data is security-sensitive. Topic names, keys, headers, schemas, offsets, lag, and access patterns can reveal tenants and business activity. Long retention expands both replay value and breach exposure. A log-source design must integrate authorization, encryption, audit, regional placement, deletion, and legal holds.

## Prerequisites and Retrieval

Retrieve partition functions, serialization, scale accounting, and cluster failure assumptions from [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve replication, read/write pipelines, failure detection, object semantics, multipart commit, and metadata consistency from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review task retry and checkpoint identity in [LSDS-027](027-task-retry-and-speculation.md) through [LSDS-030](030-tracing-a-batch-job-through-a-cluster-engine.md). You should understand append-only files, segments/indexes, checksums, quorum acknowledgement, leader epochs/fencing, half-open intervals, key hashing, schemas, transactions, idempotency, retention, encryption, and backpressure.

## Learning Objectives

After this module, you should be able to:

1. specify a distributed log using topics/streams, partitions/ledgers, records, segments, positions, and epochs;
2. distinguish partition order, append acknowledgement, committed visibility, event time, consumption, checkpoint, and external effects;
3. construct finite snapshot vectors with exact partition membership and half-open offset bounds;
4. explain why offsets and lag are not universal record IDs, timestamps, or exact counts;
5. reason about replication, in-sync/quorum acknowledgement, leader/writer fencing, truncation, and failure availability;
6. configure retention, compaction, tombstones, and tiering from replay/rebuild objectives and capacity;
7. preserve producer idempotence, transaction visibility, schema compatibility, and key-routing identity;
8. detect retention gaps, stale epochs, corrupt batches, partition-set drift, and ambiguous resets rather than silently changing input;
9. measure ingress, backlog, position/time lag, replication health, storage, decode errors, and replay headroom; and
10. protect and retire log data, metadata, credentials, schemas, checkpoints, indexes, caches, and diagnostics.

## Core Exposition

### Define the source namespace and partition set

A source begins with a cluster/service identity, tenant/namespace, topic or stream, and partition/ledger set. Names alone are insufficient across environments. Capture immutable resource IDs or qualified endpoints where available and bind authorization to them.

Partitions provide independent append and read parallelism. Within one partition, a broker or log service assigns positions in accepted order. Across partitions there is generally no total order unless the application carries and validates another sequencing relation.

For a finite run, freeze the partition set. Pattern subscription plus dynamic discovery is useful for continuous operation, but a new topic or partition changes the input domain. A bounded snapshot must state whether discovery is disabled, cut off at metadata epoch, or incorporated through a revised manifest.

### Understand records, batches, and positions

Physical logs usually batch records for compression and I/O. A batch can carry base offset, offset deltas, timestamps, producer ID/epoch/sequence, transaction/control flags, codec, record count, lengths, and checksum. Application records can carry keys, nullable values, and ordered headers.

Offsets locate records within a partition's position space. They do not prove content identity: use record/business IDs or producer sequence identities for deduplication. They do not define event time. They may have gaps after compaction or control filtering, so subtraction is a position distance.

The common checkpoint convention stores the next offset to read. If record offset 17 has been durably incorporated, checkpoint 18. Mixing “last processed” and “next unread” conventions creates duplicates or skips; encode the convention in schema and tests.

### Separate ordering domains

Partition append order is a total order only for records visible within that partition. Producer concurrency, retries, multiple writers, idempotence settings, and transactional isolation shape what reaches it. Key partitioning can place one entity in one partition, but only while key normalization and partition function/count remain stable.

Event-time order is different. Devices reconnect, clocks skew, and upstream systems buffer. Ingestion/broker timestamps may approximate arrival order but not business occurrence. Processing time is yet another clock. Later modules use watermarks/windows to handle event time.

If an application needs a global sequence, it must pay for a global sequencer, merge through a proven ordering key, or accept partial order. Sorting by per-partition offset is meaningless without a defined partition precedence and does not recover causal order.

### Specify append acknowledgement and ambiguity

A producer send crosses serialization, routing, leader append, replica/quorum acknowledgement, and response. A timeout is ambiguous: the record may or may not have committed. Blind retry can duplicate it. Supported producer idempotence associates producer identity/epoch and sequence numbers so a broker can reject duplicate retry within its contract.

Acknowledgement strength is configurable. Leader-only acknowledgement has different loss exposure from an acknowledgement that waits for an in-sync set or quorum. “All” must be interpreted using the current replica set and minimum in-sync policy, not assumed to mean every configured replica under every system.

Record the exact failure assumptions: correlated zone loss, disk corruption, fsync semantics, replica placement, unclean election, metadata quorum, and identity expiry. Do not advertise durability stronger than the weakest configured path.

### Preserve leader or writer lineage

Single-leader partitions and single-writer ledgers require fencing. After failover, the new owner must prevent the old owner from continuing an acknowledged history. Epochs/terms, compare-and-set metadata, and quorum intersection are common mechanisms.

A replica can hold an uncommitted suffix. Recovery establishes a committed/high-water boundary and may truncate divergent suffixes before serving. A reader should not treat a locally present record as committed merely because bytes exist.

Checkpoints that store only `(partition,offset)` may be insufficient when a source permits truncation/reuse. Include leader epoch, ledger generation, stream incarnation, or another lineage token when the API exposes it; otherwise document how out-of-range or divergent positions are detected.

### Distinguish committed and application-visible data

Committed visibility normally prevents readers from observing records that could disappear under supported failover. Transactional logs add aborted and pending records plus commit/abort control markers. A read-committed consumer filters aborted transactions and may stop before an unstable transaction; read-uncommitted exposes a different input.

Control batches are log protocol records, not application events. Connectors must interpret them. Position can advance across records that the application never receives, reinforcing that lag is not exact business-event count.

Pin isolation mode in source state and deployment configuration. Changing it during replay can add or remove records without any offset change and invalidate deterministic comparison.

### Build a finite snapshot vector

At planning time, list selected partitions and fetch a start $S_p$ and exclusive end $E_p$ for each under a documented metadata/visibility snapshot. Persist the vector as an immutable input manifest. Validate $L_p\le S_p\le E_p\le H_p$ before execution.

Workers read only $[S_p,E_p)$. They do not chase a moving end. If a partition is added later, it is absent from this snapshot. If retention advances $L_p$ beyond $S_p$ before or during the run, fail with a data-gap diagnosis or restore from an archive; silently using the new earliest position changes the input.

For continuous input, checkpoints repeatedly capture advancing next positions together with operator state. The source remains conceptually a vector, not one scalar offset.

### Treat retention as a replay service objective

Time/size retention deletes old segments and advances $L_p$. Some systems retain unacknowledged subscription backlogs differently from acknowledged history. Define whether retention is independent of consumer checkpoints, driven by subscriptions, or both.

Required horizon includes maximum consumer outage, detection time, repair, redeploy, backfill overlap, audit replay, checkpoint age, and margin. Capacity approximates compressed ingress rate times horizon times physical replication plus indexes, segment slack, compaction/tiering, and headroom. Use per-partition tails, not only topic averages.

Monitor replay headroom: time or bytes until the required checkpoint falls behind deletion eligibility. Alert before loss, not only after an offset-out-of-range error. Legal holds and deletion requests can override normal lifecycle and need explicit resolution.

### Understand compaction and tombstones

Key compaction retains at least a latest value per key according to the implementation's guarantees while removing superseded values asynchronously. Remaining records preserve their original relative order and positions; gaps are normal. The uncompacted head means duplicates/older values may coexist temporarily.

A compacted log is suitable for rebuilding latest keyed state only if key semantics remain stable and the consumer handles multiple versions. It does not preserve every historical transition and is not automatically a point-in-time snapshot. Keyless records may receive different treatment depending on the system.

Tombstones represent deletion. If tombstones expire before a rebuilding consumer reaches them, old external state can resurrect. Set delete-marker retention from the maximum rebuild lag or pair compacted input with a verified baseline snapshot and cutoff.

### Manage segments, indexes, and integrity

Logs roll immutable or sealed segments to bound files, enable deletion/compaction/tiering, and support recovery. Sparse offset and time indexes locate a nearby physical position; readers scan forward to the requested offset. Segment size/time trades file count, deletion granularity, compaction eligibility, recovery, and cache behavior.

Checksums or message authentication codes detect corruption/substitution at batch or entry granularity. Validate declared lengths before allocation, bound decompression expansion, and reject corrupt data rather than skipping silently. Replica repair must not copy corruption as truth without integrity/commit evidence.

Indexes and metadata are reconstructable in some systems but still operationally critical. Monitor rebuild duration, open files, page cache, journal/data disks, directory/inode pressure, and remote-tier indexes.

### Evolve schemas and key semantics safely

Every record needs an interpretable contract: schema identifier/version, encoding, field defaults, logical types, null rules, and compatibility policy. Long retention means old bytes outlive current application code. Archive schemas and decoder dependencies for the replay horizon.

Forward/backward compatibility labels are insufficient without transformation tests. Field reuse, type narrowing, default changes, timezone/decimal interpretation, unknown enums, and deleted fields can corrupt replay. Quarantine or fail visibly on undecodable data according to policy; silent dropping changes completeness.

Key encoding is more sensitive because it controls partitioning and compaction identity. Changing normalization, hash, serializer, or partition count can split an entity and cause “latest key” semantics to diverge. Use versioned keys, explicit migration topics, or routing layers with a proof.

### Handle timestamps without inventing guarantees

A record may carry producer event time, broker append time, database commit time, or several clocks. Name the source, unit, timezone, precision, trust boundary, and behavior when absent/invalid. A batch timestamp may summarize records rather than equal each record's event time.

Time-based offset lookup usually returns a position near a broker-indexed timestamp under implementation semantics, not a universal exact boundary for application event time. Verify returned records and handle partitions with no match.

Do not authorize, expire, or financially settle solely from untrusted producer timestamps. Preserve raw and normalized time plus validation outcome when governance requires traceability.

### Bound partition evolution and routing

Adding partitions increases future parallelism but usually changes default hash-to-partition mapping. Existing keys may route to new partitions, breaking per-key ordering across the change. Sticky/batched routing for keyless records affects distribution and latency.

Treat partition-count change as a data-contract migration. Record old/new counts, effective point, producer versions, routing algorithm, and downstream handling. If one entity must remain ordered, introduce a stable shard space mapped onto physical partitions or drain/cut over with explicit epochs.

Too many partitions increase leader election, metadata, file handles, replication traffic, checkpoints, connections, and recovery time. Too few limit throughput and consumer parallelism. Size from per-partition rates, tails, retention, broker resources, and failure/reassignment objectives.

### Use tiered storage with explicit locality semantics

Tiering moves sealed immutable segments from broker-local storage to remote object/storage services while preserving a logical read interface. It expands economical retention but adds fetch latency, request limits/cost, cache behavior, remote credentials, and another durability/consistency boundary.

Local and total retention differ. A replay within global retention may still miss the local cache and become remote-bound. Capacity and SLOs must model hot and cold reads separately. Prefetch and restore workflows should be bounded and tenant-aware.

Verify offload completeness before local deletion, authenticate remote objects/indexes, handle partial multipart artifacts, and test provider outage. Tiering is not a backup unless independence, immutability, restore, deletion, and disaster assumptions are proven.

### Turn positions into safe processing state

Reading advances a volatile fetch position; processing advances application state; checkpointing makes a recovery position durable; side effects may commit elsewhere. These are different. The next unread position can advance durably only with the corresponding state/effect protocol.

At-least-once recovery checkpoints before/after effects in a way that may replay, so sinks need idempotency/deduplication. Exactly-once state processing coordinates source positions and operator state; end-to-end exactly-once additionally needs compatible transactional or idempotent sinks. Broker offset commit alone does not establish it.

LSDS-042 develops assignment/rebalance; LSDS-047–050 develop checkpoint barriers and reprocessing. Here, define the source token so those protocols have stable identity.

### Observe input health and replayability

Track per partition: ingress records/bytes, append latency/errors/retries, acknowledgement mode, leader/writer epoch, replica/in-sync/quorum health, start/high/stable offsets, consumer next position, positional lag, estimated time/byte lag, oldest required checkpoint, and retention headroom.

Also track segment count/size/age, compaction backlog/dirty ratio, tombstone age, local/remote tier bytes/fetches, corrupt batches, decode/schema failures, transaction filtering, throttling, hot partitions, reassignments, auth failures, and checkpoint age. Aggregate carefully without losing maxima.

Do not put raw keys, payloads, credentials, or unbounded topic/tenant labels into general metrics. Keep diagnostic sampling authorized, redacted, rate-limited, audited, and short-lived.

### Validate failure, replay, and lifecycle

Generate multiple partitions, duplicate producer retries, missing/late records, leader failover, divergent uncommitted suffixes, corrupt batches, stale metadata, transactions that commit/abort/hang, compaction holes, expired tombstones, retention gaps, new partitions, schema changes, and tier outage.

Differentially compare bounded replay against an authoritative manifest and record IDs. Vary batch size, position convention, visibility, restart points, partition order, connector parallelism, and checkpoint failures. Assert no silent reset, invented global order, skipped committed input, included aborted input, or mixed source incarnation.

Exercise access revocation, credential rotation, region/tenant isolation, deletion, holds, cache eviction, index rebuild, and disaster restore. Confirm data and derived metadata disappear only after replay/recovery references end and policy allows.

## Definitions and Notation

- $p\in P$: one selected log partition in a frozen partition set $P$.
- $L_p$: earliest currently readable/log-start position for $p$.
- $H_p$: exclusive current high/end boundary under a named visibility rule.
- $S_p,E_p$: inclusive start and exclusive frozen end for a bounded interval $[S_p,E_p)$.
- $C_p$: checkpointed next unread position for a processor.
- $H_p-C_p$: positional lag, not necessarily exact application-record count.
- **record identity**: application or producer identity used to recognize duplicate content; distinct from broker position.
- **writer/leader epoch**: monotone lineage token used to fence obsolete owners and qualify positions.
- **snapshot vector**: immutable mapping from every included partition to its start/end positions plus source identity/configuration.
- **retention headroom**: estimated distance/time between the oldest required position and deletion eligibility/start advancement.
- **stable/committed boundary**: highest boundary safe for a chosen replication/transaction visibility contract.

## Mechanisms, Invariants, or Proof Structure

1. Pin cluster/resource identity, partition set, metadata epoch, schemas, key routing, and visibility/isolation.
2. Define record/batch format and distinguish content identity, partition position, event time, and processing time.
3. State append acknowledgement, quorum/in-sync, persistence, fencing, corruption, and failover assumptions.
4. Freeze half-open $[S_p,E_p)$ intervals for bounded input or checkpoint next positions for continuous input.
5. Validate start bounds against retention and position lineage; never silently reset a missing interval.
6. Preserve partition order without inventing cross-partition order; filter protocol/control/aborted records per declared visibility.
7. Ensure retention, compaction/tombstones, schema/key history, and tiering cover replay/rebuild objectives.
8. Coordinate source positions with operator state and effects through the appropriate recovery protocol.
9. Observe tails, replica health, backlog/headroom, storage/tiering, corruption, decode, auth, and checkpoint age.
10. Test failure/replay/adversarial cases, then expire data, metadata, credentials, caches, and diagnostics under policy.

The bounded-input completeness argument is set-based: the manifest names every partition in $P$ and a half-open interval. Each readable, application-visible record in those intervals is assigned once to processing. Compaction or transaction filtering means interval cardinality cannot be inferred from offset arithmetic; completeness is relative to the log's declared visibility at the snapshot, not an imagined original history.

Durability and processing correctness are separate. Replication/fencing protect committed source records under stated failures. Checkpoint/effect protocols protect how those records influence derived state. Strong source durability does not prevent double-applied effects, and exactly-once operator state cannot reconstruct records already removed by retention.

## Alternatives and Trade-Offs

**Single partition** provides one append order but caps write/read parallelism and creates a failure hotspot. **Many partitions** scale throughput and placement but expose only partial order and increase metadata/recovery cost.

**Leader/in-sync replication** and **quorum-ledger replication** make different commit, availability, and placement trade-offs. Both require fencing and explicit acknowledgement semantics. **Asynchronous geo-replication** lowers local latency but permits regional lag/loss exposure on disaster.

**Time/size retention** preserves full recent history until segment deletion. **Key compaction** preserves recent keyed state more economically but discards transitions and requires tombstones. Policies can be combined only with precisely understood deletion behavior.

**Local storage** gives predictable hot reads at capacity cost. **Tiered storage** extends retention cheaply while adding remote latency, requests, cache, credentials, and outage dependencies.

**Read uncommitted** minimizes visibility delay but can expose aborted/unstable data. **Read committed** provides a transactional view while filtering control/aborted records and potentially stopping at a stability boundary.

**Dynamic partition discovery** supports continuous growth. **Frozen manifests** make bounded inputs reproducible. **Earliest/latest defaults** are convenient but weaker than explicit positions and gap policy.

**Broker-managed cursor/acknowledgement** simplifies delivery workflows. **Processor-checkpointed positions** compose source progress with operator state. End-to-end effects still need an explicit protocol.

## Failure Modes and Misconceptions

1. **“A topic is one ordered queue.”** Ordering is normally per partition.
2. **“Offset 100 happened before offset 90 elsewhere.”** Cross-partition offsets have no inherent comparison.
3. **“Offsets uniquely identify business events.”** Retries, copies, migrations, and different partitions require content identity.
4. **“Lag equals unread records.”** Compaction, control records, aborted transactions, and filters create differences.
5. **“Latest means caught up.”** Starting at latest deliberately excludes prior retained history.
6. **“Acknowledged means every configured replica has fsynced.”** Interpret the actual ack/in-sync/quorum/storage contract.
7. **“A timeout means append failure.”** Success may have occurred; retry needs idempotence or tolerated duplicates.
8. **“Replica bytes are committed.”** Uncommitted/divergent suffixes may be truncated.
9. **“Broker order is event-time order.”** Producer clocks and buffering violate it.
10. **“Compaction is lossless history compression.”** It removes superseded transitions.
11. **“A compacted topic is immediately a unique-key snapshot.”** Cleaning is asynchronous and duplicates can coexist.
12. **“Tombstones can expire quickly.”** A lagging rebuild can resurrect deleted state.
13. **“Retention is a storage-only setting.”** It bounds outage recovery, replay, audit, and backfill.
14. **“Reset to earliest repairs out-of-range.”** It hides a missing prefix and changes input.
15. **“Adding partitions only increases capacity.”** It can change key routing and per-key order.
16. **“Schema registry availability guarantees decodability.”** Old schemas, code, logical semantics, and authorization must remain usable.
17. **“Committed broker offsets mean exactly-once effects.”** Source progress is only one component.
18. **“Tiered storage is automatically a backup.”** Failure independence, restore, integrity, and deletion require proof.

## Worked Examples

### Example 1

Topic `orders` has partitions 0 and 1. `(orders,0,15)` and `(orders,1,15)` are two positions with no ordering relationship. A global `15` is incomplete identity.

### Example 2

A worker durably incorporates offsets 80 through 89 from one partition. Under next-unread convention it checkpoints 90. Checkpointing 89 would replay record 89; checkpointing 91 would skip record 90.

### Example 3

The high offset is 1,000 and checkpoint is 900, but compaction left 23 application records plus two control records. Positional lag is 100; readable business-record count is 23 under the chosen visibility.

### Example 4

A producer times out after sending sequence 42. Retrying with the same supported producer identity/epoch/sequence can be deduplicated within its contract. Retrying as a new producer identity can append a second business event unless the payload has downstream identity.

### Example 5

At 50 MiB/s compressed ingress, seven days of logical retention is about 28.8 TiB before physical replication, indexes, segment slack, compaction/tier copies, and headroom: $50\times604{,}800$ MiB.

### Example 6

A rebuild needs offset 400, but $L_p=450$. The missing half-open interval $[400,450)$ is a data gap. Resetting to 450 may restore liveness but cannot claim complete reconstruction.

### Example 7

A compacted log contains `K=v1` at 10, `K=v2` at 20, and a tombstone at 30. A rebuild that observes all produces absence. If the tombstone expires while an external snapshot still contains `K=v1`, replay can incorrectly resurrect `K`.

### Example 8

A bounded job freezes ends `{0:500,1:900}`. Producers continue and partition 2 is created. The job stops at 500/900 and excludes partition 2; a later manifest can include it. Chasing live ends would make termination and reproducibility undefined.

### Example 9

A transaction writes to two partitions and aborts. A read-uncommitted source may surface the data records; a read-committed source filters them using control metadata. Both can advance positions, so visibility belongs in snapshot identity.

### Example 10

This fixture replays compacted visible records within two frozen half-open intervals. It demonstrates position holes, tombstone deletion, and next-unread checkpoints.

<!-- bijux-verify: {"id":"partition-log-snapshot","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"positional_span=6 physical_records=5 holes=1\nstate={'A': 'v2', 'C': 'v1', 'X': 'v7'} checkpoints={0: 5, 1: 4}\n","stderr":""}} -->
```python
logs = {
    0: [(2, "A", "v2"), (3, "B", None), (4, "C", "v1")],
    1: [(1, "X", "v5"), (3, "X", "v7")],
}
bounds = {0: (2, 5), 1: (1, 4)}

state = {"B": "old"}
physical_records = 0
for partition in sorted(bounds):
    start, end = bounds[partition]
    for offset, key, value in logs[partition]:
        if start <= offset < end:
            physical_records += 1
            if value is None:
                state.pop(key, None)
            else:
                state[key] = value

positional_span = sum(end - start for start, end in bounds.values())
checkpoints = {partition: end for partition, (_, end) in bounds.items()}
print(
    f"positional_span={positional_span} physical_records={physical_records} "
    f"holes={positional_span - physical_records}"
)
print(f"state={dict(sorted(state.items()))} checkpoints={checkpoints}")
```

The fixture validates deterministic local interval and tombstone arithmetic only. It does not model replication, transactions, concurrent appends, segment deletion, real compaction, connector checkpoints, or distributed effects.

## Cross-Program Connections

- **Data Engineering:** change-data capture, schema registries, dead-letter handling, backfills, and lineage depend on durable log identity and replay horizon.
- **Data Architecture:** event contracts, domains, ownership, retention classification, and regional boundaries determine topic/stream design.
- **Distributed Systems:** replicated logs, leader election, epochs, quorum intersection, fencing, failure detectors, and consensus define committed history.
- **Database Systems:** write-ahead logs, change streams, transaction isolation, log sequence numbers, snapshots, and recovery share concepts but not interchangeable guarantees.
- **Security Engineering:** producer/consumer authorization, credential rotation, encryption, integrity, tenant isolation, audit, and deletion govern log access.
- **Reliability Engineering:** backlog, retention headroom, replica health, hot partitions, tier latency, and restore drills turn replayability into an operated SLO.
- **API and Service Engineering:** idempotency keys, outbox patterns, versioned events, and error contracts determine whether retries create duplicate business effects.
- **Systems Engineering:** retention, partition count, durability, availability, cost, replay, and privacy are coupled lifecycle decisions rather than isolated settings.

## References

1. Apache Kafka. [Introduction.](https://kafka.apache.org/43/getting-started/introduction/) Current primary overview of events, topics, partitions, producers, consumers, retention, and replication.
2. Apache Kafka. [Design.](https://kafka.apache.org/43/design/design/) Current primary design documentation for partition routing/order, batching, delivery semantics, idempotent producers, transactions, replication, and log compaction.
3. Apache Kafka. [Message Format.](https://kafka.apache.org/43/implementation/message-format/) Current on-disk record-batch, offsets, timestamps, producer epoch/sequence, CRC, transaction/control, compression, key/value, and header format.
4. Apache Kafka. [Topic Configurations.](https://kafka.apache.org/43/configuration/topic-configs/) Current configuration contract for retention, compaction, tombstones, segmenting, replication constraints, message sizes, and remote/local retention.
5. Apache Kafka. [Basic Kafka Operations.](https://kafka.apache.org/43/operations/basic-kafka-operations/) Current operational documentation for consumer positions/lag and explicit offset resets.
6. Apache Kafka. [Tiered Storage.](https://kafka.apache.org/43/operations/tiered-storage/) Current primary documentation for local versus remote log retention and remote-log operation.
7. Apache BookKeeper. [Concepts and Architecture.](https://bookkeeper.apache.org/docs/getting-started/concepts/) Primary definitions for append-only ledgers, entries, replication, entry identity, last-confirmed position, and authentication codes.
8. Apache BookKeeper. [The BookKeeper Protocol.](https://bookkeeper.apache.org/docs/development/protocol/) Primary protocol description for ensemble/write/ack quorums, acknowledgement order, last-add-confirmed, writer fencing, and recovery.
9. Apache Pulsar. [Architecture Overview.](https://pulsar.apache.org/docs/next/concepts-architecture-overview/) Primary architecture documentation for brokers, BookKeeper storage, ledgers, managed logs, cursors, persistence, and recovery.
10. Apache Pulsar. [Message Retention and Expiry.](https://pulsar.apache.org/docs/4.1.x/cookbooks-retention-expiry/) Primary documentation distinguishing acknowledged-message retention, subscription backlog, and time-to-live expiry.
11. Apache Pulsar. [Tiered Storage.](https://pulsar.apache.org/docs/4.2.x/concepts-tiered-storage/) Primary documentation for sealed immutable segments, offload eligibility, remote storage, and long retention.
12. Apache Flink. [Apache Kafka Connector.](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/) Current connector documentation for explicit starting/stopping offsets, bounded input, dynamic partition discovery, checkpointed offsets, metrics, event time, and security.
13. Ongaro, D., and Ousterhout, J. [“In Search of an Understandable Consensus Algorithm.”](https://raft.github.io/raft.pdf) USENIX ATC, 2014. Formal background for replicated-log terms, leader epochs, commit safety, and membership changes; product logs may use different protocols.

## Exercises

### Exercise 1

A bounded job freezes partitions 0 and 1 at intervals `[120,180)` and `[40,95)`. Compaction/control filtering leaves 48 and 44 application-visible records respectively. Compute positional span, visible count, and holes/filter difference. State what each number means.

### Exercise 2

A topic ingests 80 MiB/s compressed at its p99 hour, requires 10 days replay plus 20% headroom, uses three physical copies, and budgets 8% extra for indexes/segment slack. Estimate provisioned physical TiB using 1 TiB = $2^{20}$ MiB. State major omitted costs.

### Exercise 3

A processor needs next position 700, current $L_p=760$, and current $H_p=1{,}100$. Explain why resets to earliest and latest are both semantic changes. Give a safe incident workflow.

### Exercise 4

A compacted key log has `acct=v1`, then `acct=v2`, then an `acct` tombstone. An external snapshot predates all three. Identify the condition under which replay rebuilds deletion correctly and the failure if tombstone retention is shorter than rebuild lag.

### Exercise 5

Design the minimal immutable manifest for a finite log replay over several partitions. Include fields needed to detect wrong cluster/topic, partition drift, offset convention/range, truncation lineage, visibility, schema/key semantics, and authorization without embedding secrets.

## Answers to the Exercises

### Answer 1

Positional span is $(180-120)+(95-40)=60+55=115$. Visible count is $48+44=92$. The difference is 23 positions. Span describes the selected position space; 92 is the application-visible records under the stated compaction/control rule; 23 are absent/filtered positions, not proof of accidental data loss.

### Answer 2

Logical retained MiB is $80\times864{,}000\times1.2=82{,}944{,}000$ MiB. Three copies and 8% overhead give $82{,}944{,}000\times3\times1.08=268{,}738{,}560$ MiB, or about $256.29$ TiB. Omitted costs include uneven partitions, bursts beyond p99 hour, compaction/tiering overlap, journals, metadata, remote copies, filesystem reserve, repair headroom, compression change, and disaster margin.

### Answer 3

The missing interval `[700,760)` cannot be read from the current log. Earliest skips that interval but processes `[760,...)`; latest additionally skips all retained data through 1,099. A safe workflow stops effects, records the gap and source lineage, finds a verified archive/snapshot or upstream resnapshot, constructs a new explicit manifest and reconciliation plan, obtains required approval, replays/deduplicates, and only then resumes. If loss is accepted, document the changed completeness contract rather than calling it recovery.

### Answer 4

The rebuild must start from a baseline compatible with the log cutoff and observe the tombstone before it expires/gets removed. It then applies v1, v2, and deletion, leaving no account. If the tombstone disappears while the old external snapshot still contains `acct`, replay may see no deletion and resurrect stale v1. Tombstone horizon must exceed worst-case rebuild lag or deletion must be represented in another durable baseline.

### Answer 5

Include manifest ID/version; qualified cluster/service and immutable topic/stream identity; metadata snapshot/partition-set epoch; exact partitions; per-partition inclusive start, exclusive end, and next-offset convention; stream incarnation and leader/ledger epoch where available; visibility/isolation and transaction/control handling; schema registry/resource IDs and compatibility set; key encoding/normalization/partitioner/count versions; record codec and timestamp semantics; creation time/owner/purpose; expected retention/tiering window; integrity/signature; and authorization-policy references. Store credential references or workload identity, never secrets.
