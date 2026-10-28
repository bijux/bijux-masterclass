---
module_id: DE-052
program: Data Engineering
level: 2
module_number: 52
title: Topics, Partitions, and Offsets
status: complete
last_verified: 2026-09-03
---

# Topics, Partitions, and Offsets

## One-Page Review

### Governing question

How should an engineer define a stream's named topology and coordinate system so that parallelism, local order, progress, lag, retention, replay, scaling, and recovery remain precise as partitions and infrastructure change?

### Essential definitions

- A **topic** is a named logical channel with an owned event contract, access policy, lifecycle, and one or more physical order domains; it is not merely a string accepted by a broker.
- A **partition** or **shard** is an independently ordered subdivision of a stream and commonly a unit of placement, replication, throughput, ownership, and consumer parallelism.
- A **topic-partition identity** binds the cluster/stream identity, topic identity or generation, and partition/shard identity. Partition number alone is ambiguous.
- An **offset** is a broker-defined coordinate within one partition/log. It is normally positional metadata, not event identity, event time, business version, or a global sequence.
- A **next offset** is the coordinate from which consumption should resume. A commit of next offset $c_p$ normally means offsets strictly below $c_p$ are covered by that progress claim.
- The **beginning offset** $b_p$ is the earliest currently readable coordinate under retention and visibility rules; it need not be zero.
- The **end offset** $h_p$ is an exclusive head or next-write/read boundary under a named visibility/isolation rule. The last present record, when one exists, is below it.
- A **cut vector** $\mathbf{c}=(c_p)_{p\in P}$ selects one boundary per partition in topology $P$; it does not manufacture a total order among partitions.
- **Position lag** for partition $p$ is $L_p=\max(0,h_p-c_p)$ when the head and commit use compatible exclusive-next semantics.
- A **replay margin** $R_p=c_p-b_p$ measures how many retained coordinates separate a checkpoint from the earliest readable boundary; time/bytes and semantic artifacts must also be checked.
- A **topology epoch** identifies the partition set and routing/lineage rules for which coordinates are valid. Resharding can create a new epoch even if the logical stream name remains.
- **Partition skew** is unequal load, storage, lag, or state across partitions; **hot-key skew** is concentration caused by one semantic key and may survive adding partitions.
- **Replication** creates copies of a partition for durability/availability; replicas are not extra logical partitions and do not add independent consumer ordering domains.
- **Offset reset** chooses a new position after missing/invalid progress. It is a governed data decision that may skip or replay work, not routine error handling.
- A **coordinate translation** is explicit lineage or mapping between different topics, clusters, partitions, epochs, archives, or mirrored streams. Numeric equality alone is not translation.

### Central model, mechanism, or theorem

For topology epoch $\tau$ with partitions $P_\tau$, model partition $p$ as a local log

$$
S_{\tau,p}=(e_{\tau,p,b_p},\ldots,e_{\tau,p,h_p-1}),
$$

where the retained readable interval is $[b_p,h_p)$. A consumer checkpoint is the vector $\mathbf{c}=(c_p)$ with a declared next-offset convention. It is currently replayable only if

$$
\forall p\in P_\tau:\quad b_p\le c_p\le h_p.
$$

Its unread position lag and retained replay margin are

$$
L_p=h_p-c_p,\qquad R_p=c_p-b_p.
$$

These scalar differences are meaningful only inside the same coordinate domain. Operational status is vector-valued: total lag estimates work, maximum lag exposes stragglers, and minimum replay margin exposes the partition closest to irreversible expiry. A cut is therefore $(\tau,\mathbf{c})$, not a bare integer or timestamp.

### Critical invariants

- Topic identity binds owner, domain meaning, schema/compatibility, key/routing policy, partition topology, retention, access, region/cluster, and lifecycle; name reuse never silently inherits old coordinates.
- Each record is addressed by a full coordinate such as `(cluster, topic-id/generation, partition, offset)` plus occurrence/business identity; offset alone never deduplicates across domains.
- Order is claimed only within the documented partition and visibility boundary; no global order follows from comparing offsets or broker timestamps across partitions.
- Beginning, end, current/read, processed, durable-checkpoint, sink-accepted, and consumer-visible frontiers remain distinct and use an explicit inclusive/exclusive convention.
- A committed next offset advances only with the durable state and effects it claims; a fetched or locally processed position is not automatically recoverable progress.
- Every multi-partition snapshot, replay, deployment comparison, or publication records a complete cut vector and topology epoch, including absent/new/retired partitions.
- Retention never removes data still needed by the promised recovery objective without an alternative authoritative archive and verified coordinate mapping.
- Partition count and routing changes are versioned migrations with lineage, dual-read/write or cutover rules, state movement, and validation; they are not transparent capacity toggles.
- More partitions increase potential parallelism only when keys, traffic, consumers, brokers, state, and sinks distribute; the hottest indivisible key bounds useful scale.
- Replication factor, in-sync/acknowledged copies, leader/follower state, and failure domains are distinguished from partition count.
- Lag dashboards expose the vector distribution, time/bytes/records, oldest event age, head confidence, retention margin, and invalid/out-of-range positions—not just a sum.
- Timestamp lookup is treated as a service-specific search that returns a coordinate under retention and clock semantics, not as a precise universal substitute for offsets.
- Mirroring, restore, failover, compaction, and archive reconstruction preserve source coordinates in metadata or provide tested translation; destination offsets do not impersonate source offsets.
- Administrative creation, deletion, expansion, truncation, reset, and seek are authorized, audited, reviewed, and fenced against stale automation.

### Common failures

Common failures include using one topic for unrelated event families; encoding environment/version/consumer names into an unstable topic taxonomy; treating a partition number or offset as globally unique; comparing offsets across partitions; assuming offsets are dense record counts after compaction, transactions, filtering, or control entries; confusing last record offset with exclusive end offset; committing the last processed offset instead of the next position; summing lag while one partition is expired; resetting automatically to latest after an out-of-range error; adding partitions without evaluating key remapping and ordering continuity; assuming partition count equals consumer throughput; assuming replication adds read parallelism; estimating time lag from offsets without rates and timestamps; using wall-clock seek as an exact cut; reusing a deleted topic name while old checkpoints survive; copying messages to another cluster and reusing numeric offsets; and deleting a retired shard before every descendant and consumer cut is understood.

### Compact example

A three-partition topic in topology epoch `orders-v3` has retained ranges `[2,4)`, `[0,3)`, and `[1,2)`. A consumer's committed next offsets are `(3,1,2)`. Per-partition lag is `(1,2,0)`, total lag is three, maximum lag is two, and the minimum coordinate replay margin is one. Six records remain retained across the partitions. The checkpoint is presently readable because every commit lies inside its partition's interval. None of the bare numbers identifies an event outside `(topic epoch, partition)`, and the aggregate lag does not reveal which partition is slow.

### Connections

[DE-051](051-streams-logs-and-unbounded-data.md) established unbounded sources, finite cuts, backpressure, and semantic replay. [DE-030](030-designing-replayable-raw-ingestion.md) covers durable source evidence; [DE-044](044-retries-timeouts-and-idempotency.md) separates attempts from effects; [DE-049](049-run-metadata-and-operational-state.md) supplies authoritative progress identities. DE-053 will specialize routing keys and ordering, DE-054 group ownership and rebalances, DE-055 delivery semantics, and DE-056 exactly-once effects.

## Governing Question

A stream may look like one named sequence to a product owner while its broker stores many independent logs, moves their leaders, retains different prefixes, and lets consumers progress at different rates. What does it mean to say “read topic X through offset 100,” “the consumer is 5,000 behind,” or “add partitions for scale” when each statement omits the coordinate domain that makes it true?

The answer begins by separating semantic namespace from physical topology. A topic groups records under one contract. Partitions split that channel into independently ordered and placeable logs. Offsets locate positions within one such log. A consumer's progress over a partitioned topic is a vector, not one scalar. Replicas preserve a partition; they do not create new logical sequences.

This hierarchy makes parallelism possible. Different partitions can be written, stored, led, fetched, and processed concurrently. It also removes a default global order. Offset 90 in partition 0 has no mathematical before/after relationship with offset 12 in partition 1. If the product needs cross-key ordering or an atomic multi-partition cut, it must define and implement those semantics explicitly.

Coordinates also age. Retention or truncation can move a beginning offset forward. Compaction can remove older values while later coordinates remain. A consumer checkpoint may therefore be syntactically valid but no longer readable. Automatic fallback to earliest creates duplicates and semantic discontinuity; fallback to latest creates loss. Either choice needs a product recovery policy and evidence.

Finally, topology changes. Increasing partitions can change routing for future records. Shard splitting produces parents and children. Mirroring assigns destination coordinates. Topic deletion and recreation can reuse a name. Durable systems bind checkpoints to immutable identities, topology epochs, and lineage so that a familiar integer never silently refers to a different history.

## Why This Matters

Topics often become long-lived interfaces between teams. Producers and consumers deploy independently, access controls accumulate, schemas evolve, retention costs grow, and the topic name appears in code, dashboards, alerts, data catalogs, incident runbooks, and compliance inventories. A vague topic contract turns a convenient transport into an unowned public database.

Partitioning is the main scalability axis of many log systems. It spreads storage and network traffic, permits multiple active consumers, and limits failure/recovery units. But useful capacity is constrained by the hottest partition, hottest key, broker placement, replica work, consumer slot, state movement, and sink. A topic with 100 partitions can still be serialized by one key or throttled by one database connection pool.

Offset mistakes directly cause loss and duplication. An off-by-one commit can skip a record or replay it. Advancing a checkpoint before durable state/output makes recovery omit an effect. Advancing too late repeats work. Storing only a scalar for several partitions makes exact restart impossible. Treat coordinate conventions as part of the correctness contract.

Lag is a leading operational signal only when interpreted correctly. A total of 10,000 positions could mean evenly distributed small events or one partition blocked behind a giant transaction. The same position lag can represent milliseconds or hours as rates change. A zero broker lag can coexist with stale downstream publication. Measure records, bytes, time, oldest obligation, processing/sink visibility, and retention margin.

Retention makes coordinate safety time-bounded. If the earliest readable position crosses a checkpoint, the log alone can no longer reproduce the missing interval. This can happen during an outage even while brokers are healthy. Recovery capacity must catch up before the retention frontier, with margin for restore, state hydration, schema/key availability, and live traffic.

Topology evolution is a data migration. With common modulo-based routing, changing partition count can send the same key to a new partition. Old and new records then occupy different order domains. Stateful processors must move or rebuild keyed state. Kinesis-style resharding creates lineage between closed parent and open child shards. These mechanisms differ, but both require an explicit cutover and complete historical read plan.

Disaster recovery further exposes coordinate scope. A replicated topic in another cluster often has different destination offsets, retention, topic identity, and visibility. Numeric equality is not proof of equivalence. Preserve source coordinates and content identity, measure replication frontier, and rehearse consumer checkpoint translation.

## Prerequisites and Retrieval

Retrieve the product contract: event families and business owner; source of record; consumers and decisions; required key-level or cross-key order; latency/freshness; revision; retention/replay; availability/durability; region/residency; privacy/deletion; and recovery objectives. Determine whether one semantic channel is actually appropriate.

Retrieve topic metadata: immutable topic/resource ID if available; cluster/account/project/tenant/namespace; logical name and aliases; creation generation/time; environment; owner; schema subjects/versions; key/routing version; partition count; replication; durability acknowledgements; retention/compaction; quotas; encryption keys; ACLs; and deletion/recreation controls.

Retrieve partition metadata: partition/shard IDs; topology epoch; leader/owner and replicas; in-sync/healthy copies; storage placement/failure domains; beginning/high-watermark/log-end/last-stable or equivalent positions; bytes; rates; oldest/latest timestamps; segment/tier state; and leader epochs or truncation evidence.

Retrieve producer behavior: explicit partition versus key routing; partitioner algorithm/version/seed; null-key behavior; batching/compression; retries/idempotence; maximum in-flight requests; transactions; sequence identity; acknowledgment/durability; error handling; discovery refresh; and behavior when partitions expand.

Retrieve consumer behavior without yet assuming group semantics: assignment; fetch/read position; processed frontier; state-checkpoint frontier; sink-accepted frontier; committed/resume next offset; visibility/isolation; reset policy; seeks; pauses; retries; quarantine; backfills; and any stored source-coordinate envelope.

Retrieve retention and mutation controls: time and size limits; compaction/delete combination; tombstone lifetime; tiered storage; subscription retention; administrative record deletion; truncation; archive; backup/restore; legal hold; and how beginning coordinates are exposed. Confirm policy and observed enforcement separately.

Retrieve topology-change history: topic create/delete/recreate; partition expansion; shard split/merge; routing version; parent/child lineage; reassignment; leader changes; cluster migration; mirror mapping; state migration; checkpoint translation; validation; rollback; and old topology retirement gates.

Retrieve operational evidence: per-partition ingress/egress records and bytes; request latency/errors/throttles; disk/network/CPU; replica health; under-replication; leader imbalance; fetch rate; lag distribution; oldest record age; retained range; replay margin; storage growth; skew; oversized records/transactions; and consumer/sink freshness.

Distinguish logical topic from physical partition; partition from replica; partition ID from broker ID; topic name from immutable topic identity; offset from event ID; offset from sequence number in another system; offset from timestamp; offset from count; current fetch position from committed next offset; broker acknowledgement from application effect; high watermark from log end; visible end from physical end; beginning offset from zero; lag from freshness; aggregate lag from worst partition; reset from recovery; compaction from retention; repartition from replica reassignment; partition expansion from elastic consumer scaling; mirror from shared coordinate domain; and numeric equality from proven translation.

Create a topology contract:

| Concern | Required decision and evidence |
|---|---|
| Topic meaning | Owner, event families, source authority, schemas, consumers, lifecycle |
| Identity | Cluster/resource/topic generation, partition/shard, topology epoch |
| Routing | Key and partitioner version, null/explicit behavior, expansion semantics |
| Order | Exact per-partition scope, transaction/visibility boundary, cross-domain non-order |
| Coordinate | Offset/sequence semantics, next-position convention, gaps, timestamp lookup |
| Cut | Complete partition set and vector, inclusion convention, topology generation |
| Durability | Replicas, acknowledgement, health/in-sync rule, failure domains, restoration |
| Retention | Beginning frontier, time/size/compaction/tier rules, archive and margin |
| Progress | Fetch, process, state, sink, commit, publication frontiers and authority |
| Scale | Per-partition/key load, brokers, replicas, consumers, state and sink limits |
| Evolution | Add/split/merge/recreate/migrate lineage, cutover, validation, retirement |
| Governance | ACLs, tenant isolation, encryption, privacy/deletion, audit, admin fencing |

Write a testable claim: “For topic identity `T`, topology epoch $\tau$, and complete partition set $P_\tau$, every source coordinate `(T, τ, p, o)` refers to at most one retained log position; checkpoint vector $\mathbf{c}$ uses exclusive-next semantics and is bound to durable state/effects; every component satisfies $b_p\le c_p\le h_p$; lag and replay margin are measured per partition; routing/topology changes have explicit lineage; and recovery can reconstruct or translate every required coordinate before retention expires.”

## Learning Objectives

After completing this module, you should be able to:

1. define topics as governed semantic channels rather than arbitrary broker names;
2. distinguish partitions/shards, replicas, leaders, segments, brokers, assignments, and consumer instances;
3. scope offsets and sequence numbers to immutable topic, partition, cluster, and topology identities;
4. represent multi-partition progress and reproducible finite reads as cut vectors with explicit boundary conventions;
5. compute per-partition/total/maximum lag and replay margin while explaining their limitations;
6. diagnose off-by-one, out-of-range, retention, compaction, truncation, timestamp-seek, and topic-recreation hazards;
7. estimate useful partition count from throughput, skew, state, recovery, broker, consumer, and sink constraints;
8. design safe partition expansion, shard split/merge, topic migration, and disaster-recovery coordinate translation;
9. specify observability, security, privacy, administrative, testing, and recovery controls for topic topology; and
10. explain why partitions enable parallelism but do not themselves guarantee balanced load, business order, durability, or exactly-once effects.

## Core Exposition

### Treat a topic as a data product interface

A topic name should identify one coherent stream contract. Records share a source authority, key model, schema evolution strategy, retention class, security boundary, and compatible consumer expectations. Putting “everything about customers” into one topic can couple unrelated schemas, privacy purposes, traffic profiles, keys, and lifecycles. Splitting every event type into its own topic can create discovery and operational explosion. Choose the boundary by ownership and semantics, then validate scale.

Name plus environment is not durable identity. A topic may be deleted and recreated under the same name, moved to another cluster, restored from backup, or mirrored. Where the platform exposes an immutable resource/topic ID, persist it. Otherwise create a governed generation identifier. Bind schemas, checkpoints, archives, dashboards, and consumers to the generation.

Topic creation is an API contract change. Disable accidental auto-creation for governed production domains or constrain it tightly. Require owner, schema/key policy, partition/replication/retention settings, access, classification, quotas, observability, and deletion protection before producers write. Detect configuration drift after creation.

Topic taxonomies should express stable domain ownership, not deployment chronology. Avoid consumer-specific source topics when consumers should independently subscribe to the same facts. Avoid encoding a schema version in the topic name unless the version is genuinely an incompatible parallel contract with an explicit migration and retirement policy.

### Partition one logical channel into local logs

A partition is a logical ordered append domain. Brokers can place different partition leaders or owners on different machines and consumers can fetch them concurrently. Each partition may have replicated physical copies. A segment is a storage chunk inside one partition; it is not normally a semantic order domain.

Apache Kafka describes a topic as partitioned and each new event as appended to one partition. Apache Pulsar implements a partitioned topic as multiple internal topics. Amazon Kinesis models a stream as a set of shards, each an identified sequence of records. Product terms differ, but all illustrate that scalable stream topology contains several local sequences rather than one universal log.

Partition count supplies an upper bound on certain forms of parallelism, not a performance promise. One consumer task cannot split a partition's ordered processing arbitrarily without application-level concurrency and resequencing. More consumers than active assignable partitions may sit idle. Fewer consumers may process several partitions each. Downstream state and sink contention can dominate.

Partition identity must survive placement changes. Moving a leader from broker A to B does not create a new logical partition. Reassigning replicas changes placement. Truncating divergent data, deleting/recreating a topic, or resharding can change the coordinate history and requires an epoch or lineage boundary.

### Understand what an offset says—and does not say

An offset is assigned within a partition. In Kafka, records in a partition have sequential IDs called offsets. In other systems the coordinate may be a structured message ID or a shard sequence number. Do not erase these differences behind a generic integer API.

The full address includes cluster/stream/topic generation, partition or shard, and offset/sequence. `(orders-v3, 2, 19)` can identify one stored occurrence; bare `19` cannot. Even the full transport coordinate is not the domain occurrence identity: a retry can create two stored records for one business occurrence, and mirroring creates a new transport coordinate for equivalent content.

Offsets are order coordinates, not wall-clock time. Different partitions advance at different rates. Offset 50 in one partition need not precede offset 20 elsewhere. Broker timestamps can be producer-supplied or append-time and may be equal, skewed, corrected, or absent. Event-time order is a separate topic developed in DE-057.

Do not assume offset differences equal user record counts or bytes. Internal control entries, transactional visibility, compacted/deleted records, batch encoding, filters, and product-specific sequence behavior can create gaps or change what a fetch returns. Offset lag is a coordinate distance. Calibrate it with actual record/byte/time measures.

### Use half-open ranges and next-position checkpoints

Represent a retained readable interval as $[b_p,h_p)$. The beginning $b_p$ is included if a record exists there under visibility; the end $h_p$ is the next boundary and excluded. The number of coordinate slots is $h_p-b_p$, although visible user-record count may differ.

A resume checkpoint $c_p$ is also a next position. If processing and its claimed effects are durable through offset 41, commit 42. Recovery begins at 42. This convention makes an empty processed prefix $[b_p,b_p)$ and a complete read $[b_p,h_p)$ natural. APIs vary, so record the actual convention instead of assuming it.

Distinguish frontiers. The fetch position may advance after bytes enter a client buffer. The processed position may advance after transformation. A state checkpoint may become durable later. A sink may accept effects later still. The committed resume offset must correspond to the strongest durable boundary required by the application's delivery contract. DE-055 and DE-056 develop that coupling.

An end offset can also vary by isolation. A physical log end may include entries not yet replicated or transactions not yet visible. Kafka distinguishes positions such as log end, high watermark, and last stable offset in relevant contexts. Name the frontier used to compute lag; otherwise two dashboards can disagree while both perform correct subtraction.

### Represent progress as a vector

For partitions $P=\{0,1,2\}$, a cut might be $\mathbf{c}=\{0\mapsto 120,1\mapsto 83,2\mapsto 901\}$. It means prefixes below those next positions under one topology epoch. It does not order record `(0,119)` against `(2,900)`.

Persist the complete partition set, including empty partitions. If a new partition appears, a checkpoint reader must apply a documented initialization policy. If a partition is retired, preserve its terminal cut and lineage until recovery no longer needs it. A sparse map with silent defaults can skip new partitions or resurrect retired ones.

A multi-partition cut may need consistency beyond independent positions. If a producer transaction spans partitions, consumers using committed isolation may select a visibility frontier that excludes incomplete transactions. If application causality matters, capture transaction/causal metadata or coordinate through a higher-level snapshot protocol. A vector alone identifies prefixes; it does not prove business consistency.

Cuts support reproducible batch reads, shadow comparisons, backfills, incident capture, and release boundaries. Store them as immutable artifacts with topic generation, schema/transform/reference versions, and retrieval evidence. “Read until now” is not reproducible.

### Calculate lag without collapsing the diagnosis

With compatible exclusive heads and commits, $L_p=h_p-c_p$. Report the vector, sum, maximum, quantiles, and partitions above objective. A sum estimates total outstanding coordinate distance. A maximum identifies the worst serial domain. Neither is equivalent to freshness.

Convert to time only with evidence. The timestamp of the oldest unread record gives an obligation-age signal, but producer clock skew and late events complicate it. Divide lag by recent service rate only as an estimate when rates and record costs are stable. Measure bytes and estimated work because 1,000 tiny records can be cheaper than one huge transaction.

Compute replay margin $R_p=c_p-b_p$. The minimum across partitions identifies the checkpoint closest to falling outside broker retention. Convert margin to time/bytes using observed eviction and traffic, then include restore and catch-up duration. A zero margin can be valid at the earliest retained position but offers no coordinate cushion.

Negative apparent lag or commit beyond head indicates incompatible snapshots, epochs, visibility rules, stale metrics, truncation, or corruption—not “super-fast consumption.” Commit below beginning means the broker history required for direct resume has expired. Stop automatic processing and invoke the documented archive/reset/reconciliation path.

### Size partitions from constraints, not folklore

Let required peak ingress be $W$ bytes/s and demonstrated safe ingress per partition be $w$. A throughput lower bound is $N\ge\lceil W/w\rceil$. Derive similar bounds for egress, request rate, consumer processing, state/checkpoint recovery, and desired failover/rebuild time. Use the maximum and add tested headroom.

This arithmetic assumes traffic can distribute. Let $x_k$ be load for routing key $k$. If one indivisible ordered key requires more than one partition's safe capacity, no partition count solves it because that key maps to one order domain. Options include improving per-partition capacity, relaxing the order domain, splitting the semantic key with deterministic subkeys and later combination, isolating the tenant, aggregating upstream, or changing the product requirement.

Too few partitions limits throughput and consumer concurrency and increases failure/recovery blast radius per partition. Too many increase metadata, files/segments, replicas, leader elections, connections, fetch requests, checkpoints, assignments, rebalance/state movement, monitoring cardinality, and minimum resource footprint. Find a tested operating envelope.

Include growth and migration constraints. Some platforms permit only partition increase; some support split/merge with lineage; some manage capacity dynamically. A large initial count may avoid remapping but imposes ongoing cost. A small count preserves simplicity but makes later routing/state migration more likely.

### Diagnose skew at every layer

Measure ingress records, bytes, compressed bytes, request rate, batch size, key cardinality, largest keys, storage, egress, consumer time, state size, checkpoint bytes, and sink latency per partition. Broker balance by bytes can coexist with application imbalance by CPU or state.

Common causes include one large tenant, monotonically increasing or low-cardinality keys, null keys using sticky batching, explicit partition choices, inconsistent serializers/hash functions, traffic seasonality, giant transactions, and a downstream hot row. Inspect actual routed distributions before adding partitions.

Partition-level skew differs from broker placement skew. Several hot partitions may land on one broker even if each is individually reasonable. Replicas also consume disk/network. Reassignment can improve placement but cannot change which keys map to a partition. Routing redesign can improve key distribution but changes semantic order and state ownership.

Use bounded heavy-hitter telemetry without leaking sensitive raw keys. Hash or tokenize identifiers under an approved scheme, restrict diagnostic access, and expire samples. Keep tenant-level accountability where operational and legal policy permits it.

### Treat replication separately from partitioning

A partition leader/owner accepts or sequences writes while replicas copy the same logical log according to the system's protocol. Replication factor is the number of copies intended; actual healthy/in-sync/acknowledged copies determine current durability and availability. Placement across independent failure domains matters more than a raw count.

Three partitions replicated three ways produce three logical order domains and nine intended copies, not nine partitions. Consumers normally read the logical partition under platform rules. Adding replicas can improve failure tolerance and may increase replication traffic/storage; it does not automatically triple application consumption parallelism.

Leader changes should preserve the partition coordinate history under the platform's guarantees, but unclean failover or truncation can invalidate acknowledged assumptions. Record leader/topology epochs where exposed, alert on under-replication and unavailable partitions, and test failure under the configured acknowledgement policy.

Do not claim durable storage from replication configuration alone. Verify acknowledgements, minimum healthy replicas, disk persistence, correlated zones, retention/deletion, backup/archive, authentication to encryption keys, and restore. A replicated operator error or deletion remains replicated.

### Design retention around checkpoints

Retention advances $b_p$ independently of a consumer's progress in many log systems. A disconnected consumer does not necessarily pin data. Other subscription systems retain based on acknowledgement and policy. Retrieve the exact mechanism rather than importing Kafka intuition into Pulsar, Kinesis, or Pub/Sub.

Time-based and size-based retention interact with traffic skew. A hot partition may exhaust size retention sooner than a cold one, shrinking its time horizon. Compaction retains selected key history rather than an exact occurrence stream. Tiered storage can extend accessible history but changes latency, throughput, cost, and operational dependencies.

Monitor earliest readable offset and checkpoint per partition. Estimate time until crossing using recent byte/record eviction, but alert with conservative margins. Freeze deletion, expand retention, repair capacity, or archive affected ranges before the boundary passes. Once data expires, changing retention cannot resurrect it.

An archive is useful only with exact coordinate and integrity mapping. Store source topic generation, partition, offset range, record envelope/schema, object manifest, digest, encryption/key lineage, and gaps. Exercise reconstructing $[c_p,h_p)$ from broker plus archive into isolated outputs.

### Make offset reset an explicit data decision

When a consumer has no checkpoint, the application may start at earliest retained, latest/head, a timestamp-derived position, a snapshot cut, or a product-defined bootstrap. Each choice yields different data. Configuration defaults are not a substitute for product approval.

When $c_p<b_p$, earliest reset skips the expired interval unless an archive fills it. Latest reset skips everything currently retained. Neither is “recovery” by itself. Record the lost/replayed range, affected outputs/consumers, approval, compensating source, reconciliation, and new checkpoint generation.

When $c_p>h_p$, investigate topic recreation, restore/truncation, wrong cluster, stale metadata, corrupt state, or convention mismatch. Do not clamp silently. Bind immutable topic identity and compare topology epochs before any seek.

Timestamp seek is approximate and product-specific. It can select the first record at or after a broker/record timestamp, but clocks, equal timestamps, partition differences, retention, and indexing affect the result. Resolve each partition to a coordinate, persist the returned cut, inspect boundary samples, and accept explicit inclusion semantics.

### Evolve topology as a migration

Adding Kafka-style partitions leaves old records in old partitions and creates new order domains. With a partitioner based on `hash(key) mod N`, changing $N$ can remap many keys. A key's older records remain in its prior partition while new records may enter another, so naive concurrent reading can violate the intended per-key continuity.

A safe change versions the routing function and defines a cutover. Options include stopping producers at a recorded old cut, draining/state-checkpointing, starting the new topology; dual-writing with deduplicated shadow validation; creating a new topic generation and backfilling; or using stable virtual buckets mapped to physical partitions. Each has latency, complexity, and effect risks.

Stateful consumers need a migration plan: rebuild state from the complete history under the new routing, export/import keyed snapshots, or transfer state with checksums and fenced ownership. Validate per-key sequence, counts/digests, cut coverage, lag, capacity, and sink outcomes before publication.

Kinesis resharding illustrates explicit lineage: splitting a shard creates child shards and closing parents; consumers must process parents before children as required by the service/client model. A topology is then a directed acyclic lineage, not just a current list. Preserve terminal parent positions and child start relationships.

Do not delete old topics/shards/checkpoints at cutover. Retire only after retention/recovery obligations, all consumers, archive mapping, state, rollback window, security/privacy, and audit requirements are satisfied.

### Translate coordinates across copies and disasters

Mirroring writes source records into destination partitions that have their own offsets. Partition counts, batching, filters, compaction, transactions, and arrival order may differ. Persist the source coordinate and stable occurrence/content identity in the destination envelope or a mapping index.

Measure replication as a cut vector: for each source partition, record the highest source next position durably represented and verified at the destination. Destination end offset is not the source replication frontier. Reconcile counts/digests or domain materializations over exact cuts.

Failover requires selecting a destination topic generation, translating the consumer checkpoint, verifying schemas/keys/config/reference data, fencing the old writer/consumer, and handling records accepted on only one side. Failback is another migration, not a DNS reversal.

Backups restore bytes at a point in time but may allocate new resource IDs or offsets. Test whether exact coordinates survive. If not, produce a validated source-to-restored mapping and update every checkpoint/materialization lineage artifact atomically.

### Operate the topic topology

Inventory topics and owners. Alert on unknown/auto-created/orphan topics, configuration drift, unsafe replication, unauthorised ACL changes, expiring keys, unexpected partition changes, retention shrink, and deletion markers. Publish a catalog view that joins semantics with live topology.

For each partition expose ingress/egress records and bytes, append/fetch errors and latency, head and beginning positions, all relevant progress frontiers, lag and oldest obligation age, replay margin, storage/tier state, leader/replica health, and placement. Correlate with consumer state/checkpoint and sink publication.

Run drills: broker/leader loss, replica degradation, hot partition, large transaction, paused consumer, retention approach, out-of-range checkpoint, timestamp seek, partition expansion, mirror lag, topic recreation defense, archive replay, and regional failover. Verify domain outputs, not just client reconnection.

Administrative tools need typed guarded operations. A reset command should identify exact topic generation, group/application, partitions, old/new cut, estimated replay/skip, archive coverage, sink mode, approval, dry-run diff, and audit record. Destructive deletion or truncation requires stronger controls and recovery evidence.

### Secure and govern topology metadata

Topic names, keys, headers, offsets, and traffic patterns can disclose tenants, operations, or behavior even without payload access. Apply least privilege to metadata/list/describe APIs as well as read/write. Separate producer, consumer, operator, schema, and replication identities.

Authorize by durable domain boundaries. Wildcard ACLs over namespaces can accidentally expose newly created topics. Enforce tenant/environment isolation, encryption in transit and at rest, key rotation/availability, network boundaries, quotas, and audit. Test denial behavior so unauthorized producers cannot create shadow topics or choose arbitrary partitions to attack a hot shard.

Retention and compaction must implement privacy and legal policy across replicas, tiered storage, archives, mirrors, backups, dead letters, state stores, and materializations. An offset is not a stable deletion handle after compaction or migration; retain domain identity and lineage needed to find governed copies.

Metrics and diagnostic samples should minimize payload/key data. High-cardinality raw business keys in labels create cost, leakage, and unusable telemetry. Use bounded approved identifiers and controlled drill tooling.

### Review the design as a coordinate proof

A review should prove six linked claims. First, the topic boundary has coherent meaning and ownership. Second, every record has an unambiguous coordinate and separate occurrence identity. Third, routing and local ordering match the business order domain. Fourth, cut/progress conventions compose with state and effects. Fifth, partition/replica/storage/consumer/sink capacity survives skew and failure. Sixth, retention and topology lineage permit promised recovery.

For each claim distinguish configuration, static reasoning, local tests, load evidence, failure drills, and production measurements. A topic description showing 24 partitions and replication factor three establishes configuration only. It does not prove even routing, three healthy failure-domain-independent copies, safe commits, recoverable history, or consumer freshness.

Reject ambiguous statements. Replace “offset 500” with full coordinate and boundary semantics; “lag is low” with vector/time/byte evidence and freshness objective; “ordered” with exact key/partition/producer scope; “scale by adding partitions” with routing/state/cutover design; and “replicated to DR” with source-cut coverage and checkpoint translation proof.

## Definitions and Notation

Let $T=(I_T,C_T,\tau)$ denote a topic generation: immutable identity $I_T$, semantic contract $C_T$, and topology epoch $\tau$. Let $P_\tau$ be its complete set of partitions/order domains. A record coordinate is

$$
q=(I_T,\tau,p,o),\qquad p\in P_\tau,
$$

where $o$ is local to $p$. Occurrence identity $u(e)$ and business key $k(e)$ remain separate from $q$.

For each partition, define beginning $b_p$, compatible exclusive visible head $h_p$, and committed next position $c_p$. The retained coordinate interval is

$$
I_p=[b_p,h_p).
$$

The checkpoint is valid and directly readable when $b_p\le c_p\le h_p$. Its processed prefix claim is $[b_p,c_p)$ only if retained beginning is also the original/base boundary; more generally it claims an identified prior base plus interval ending at $c_p$.

Define position lag, replay margin, and retained coordinate span:

$$
L_p=h_p-c_p,\qquad R_p=c_p-b_p,\qquad D_p=h_p-b_p.
$$

Useful aggregates include

$$
L_\Sigma=\sum_{p\in P_\tau}L_p,\quad L_{\max}=\max_{p\in P_\tau}L_p,\quad R_{\min}=\min_{p\in P_\tau}R_p.
$$

These are coordinate arithmetic, not automatically record count, bytes, work, or time. Define $A_p$ as oldest unread obligation age, $X_p$ as unread bytes or estimated work, and $F_p$ as the required consumer-visible freshness frontier when available.

Let $r_v(k,N)$ be routing function version $v$ mapping key $k$ to one of $N$ partitions. A topology change from $(v,N)$ to $(v',N')$ has moved-key set

$$
K_\Delta=\{k:r_v(k,N)\ne r_{v'}(k,N')\}.
$$

For simple modulo routing, $K_\Delta$ can be large. Measure it on the actual key distribution rather than assuming incremental movement.

Let $\lambda_p$ and $\mu_p$ be effective offered and sustainable service work rates for partition $p$. A necessary steady-state condition is $\lambda_p<\mu_p$ for every relevant bottleneck, with headroom for variance and recovery. Aggregate capacity does not compensate for one indivisible hot partition.

A topology lineage graph $G=(V,E)$ represents topic/shard epochs as vertices and split, merge, migrate, mirror, restore, or recreate relationships as typed edges. A coordinate translation $\phi_{a\to b}$ must name its source/destination generations, coverage cut, multiplicity/filter semantics, integrity evidence, and gaps.

## Mechanisms, Invariants, or Proof Structure

Use this review chain:

1. **Establish semantic identity.** Show that the topic generation has one accountable contract, source authority, schema/key policy, consumer purpose set, security class, and lifecycle.
2. **Establish coordinate uniqueness.** Show that full `(cluster/topic generation, topology epoch, partition, offset)` addresses at most one transport occurrence and is stored beside separate occurrence/business identity.
3. **Establish order scope.** Show exactly which writes are sequenced in each partition, how visibility/transactions affect reads, and that no cross-partition order is inferred.
4. **Establish boundary convention.** Show beginning/head/checkpoint meanings with half-open examples and prove every progress publisher uses the same or an explicit translation.
5. **Establish cut completeness.** Enumerate every active, empty, new, and terminal partition for epoch $\tau$; reject missing entries or implicit defaults.
6. **Establish progress durability.** Couple $c_p$ to the exact state checkpoint, accepted sink effects, code/schema/reference versions, and fencing needed after restart.
7. **Establish direct replay.** Verify $b_p\le c_p\le h_p$ for every partition and sufficient schemas/keys/code/state/sink repair; otherwise prove archive coverage and mapping.
8. **Establish capacity.** Test per-partition/key/broker/replica/consumer/state/checkpoint/sink distributions under peak, burst, failure, replay, and concurrent live load.
9. **Establish evolution.** Version routing/topology, capture old/new cuts and lineage, migrate state/effects, validate equivalence, fence writers, and retain rollback/recovery evidence.
10. **Establish operational control.** Monitor vector lag/replay margin/replica health/config drift and rehearse typed reset, archive replay, reshard, restore, and failover procedures.

The central safety invariant is:

> No system interprets a coordinate, checkpoint, lag value, or reset target without the immutable topic generation, topology epoch, partition domain, visibility frontier, and boundary convention that give it meaning.

The progress invariant is:

> For each partition, durable resume position never exceeds the state and effects accepted by the recovery contract, and every required position remains readable or reconstructible until that contract expires.

The topology invariant is:

> Every routing or partition-set change has a recorded lineage and cutover such that each accepted occurrence belongs to the intended old or new domain, moved state is accounted for, and no stale writer or checkpoint silently crosses epochs.

The capacity invariant is:

> Every partition, especially the hottest key/domain, has sustainable service and recovery headroom across broker, replica, consumer, state, and sink constraints; aggregate spare capacity is not used to excuse a serial bottleneck.

This annotated executable demonstrates only half-open ranges and vector arithmetic:

<!-- bijux-verify: {"id":"topic-cut-and-lag","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"topology_epoch=orders-v3\npartition_count=3\nretained_ranges=((0, 2, 4), (1, 0, 3), (2, 1, 2))\ncommitted_next=((0, 3), (1, 1), (2, 2))\nlag_by_partition=((0, 1), (1, 2), (2, 0))\ntotal_lag=3\nmaximum_partition_lag=2\nminimum_replay_margin=1\nretained_coordinate_span=6\noffsets_are_partition_local=True\ncut_requires_topology_epoch=True\ntimestamp_is_not_offset=True\n","stderr":""}} -->
```python
topology_epoch = "orders-v3"
beginning = {0: 2, 1: 0, 2: 1}
head_next = {0: 4, 1: 3, 2: 2}
committed_next = {0: 3, 1: 1, 2: 2}

partitions = tuple(sorted(beginning))
assert partitions == tuple(sorted(head_next)) == tuple(sorted(committed_next))

retained_ranges = tuple(
    (partition, beginning[partition], head_next[partition])
    for partition in partitions
)
lag_by_partition = tuple(
    (partition, head_next[partition] - committed_next[partition])
    for partition in partitions
)
replay_margin = tuple(
    committed_next[partition] - beginning[partition]
    for partition in partitions
)

assert all(
    beginning[partition] <= committed_next[partition] <= head_next[partition]
    for partition in partitions
)

print(f"topology_epoch={topology_epoch}")
print(f"partition_count={len(partitions)}")
print(f"retained_ranges={retained_ranges}")
print(f"committed_next={tuple(sorted(committed_next.items()))}")
print(f"lag_by_partition={lag_by_partition}")
print(f"total_lag={sum(value for _, value in lag_by_partition)}")
print(f"maximum_partition_lag={max(value for _, value in lag_by_partition)}")
print(f"minimum_replay_margin={min(replay_margin)}")
print(f"retained_coordinate_span={sum(end - start for _, start, end in retained_ranges)}")
print("offsets_are_partition_local=True")
print("cut_requires_topology_epoch=True")
print("timestamp_is_not_offset=True")
```

The assertions show that one finite checkpoint lies inside all retained intervals. They do not prove that coordinate slots correspond one-to-one with visible domain records, that commits match durable sink effects, that timestamps are trustworthy, that routing is balanced, or that the broker survives failure.

## Alternatives and Trade-Offs

**One partition versus many.** One partition offers a simple total append order and minimal coordination but creates one throughput, storage, and recovery domain. Many partitions increase potential parallelism and distribute storage, but require vector progress, remove a default total order, increase metadata, and complicate routing/state evolution.

**Domain topic versus shared enterprise topic.** Domain topics align ownership, schemas, access, retention, and failure. A broad shared topic can simplify discovery or transport connections but couples unrelated governance and scaling. Excessive fragmentation creates topic/ACL/monitoring sprawl. Choose coherent contracts with platform automation.

**Key hashing versus explicit partition.** Hashing gives repeatable distribution when serializers/algorithm/count are stable. Explicit partition gives control but exposes topology to producers and can create hotspots/stale IDs. Random/sticky routing improves unkeyed batching/distribution but offers no semantic key locality.

**Physical partitions versus virtual buckets.** Direct `hash mod partition-count` is simple but remaps keys when count changes. Many stable virtual buckets mapped onto physical partitions can limit movement and support rebalancing, at the cost of mapping metadata, an extra routing layer, and possible imbalance among buckets.

**More partitions now versus later.** Preallocation avoids some expansion risk and increases future concurrency. It raises replica/storage/metadata/request/checkpoint cost and may exceed operational comfort. Later expansion delays cost but requires a proven migration for routing and state.

**Delete retention versus compaction.** Delete retention preserves an exact recent interval and expires by time/size. Compaction preserves selected recent values per key but not complete occurrence history. Combining them serves state bootstrap plus bounded history only under precisely tested tombstone and segment behavior.

**Broker retention versus authoritative archive.** Long broker retention enables fast native replay but consumes operational storage. An object archive can be cheaper and longer-lived but needs manifests, coordinate mapping, schemas/keys, restore throughput, and slower recovery. Many systems use both.

**Offset seek versus timestamp seek.** Exact offset cuts are reproducible in one topology. Timestamp seek is convenient for human time ranges but approximate across partitions and clocks. Resolve timestamps once to an inspected vector, then persist coordinates.

**In-place expansion versus new topic generation.** In-place expansion minimizes endpoint migration but can hide routing discontinuity. A new generation makes boundaries explicit and supports shadow validation, at the cost of dual infrastructure, copying, consumer migration, and eventual retirement.

**Active-passive mirror versus active-active production.** Active-passive simplifies authority and conflict but has replication lag and failover work. Active-active reduces regional write dependency but creates multi-writer identity, conflict/order, duplicate, and merge requirements. Numeric offsets never solve those domain conflicts.

**Managed automatic capacity versus explicit shards.** Automatic systems reduce manual count management but do not remove key skew, quotas, consumer/state/sink bottlenecks, coordinate scope, or recovery design. Explicit shards offer predictable units and control but demand forecasting and reshard operations.

## Failure Modes and Misconceptions

**“The topic is the schema.”** A name does not define payload meaning, source authority, key, evolution, correction, retention, or consumer rights. Attach and enforce a governed contract.

**“Offset 400 identifies the event.”** It identifies at most a position inside one partition generation. Preserve full transport coordinates and separate occurrence/business identity.

**“Offsets are timestamps.”** They establish local append order, not event time or cross-partition chronology. Timestamp lookup is a mapping query with retention/clock caveats.

**“Offsets are dense record counts.”** Gaps, compaction, transactions, control entries, batching, and filtering can invalidate that interpretation. Treat subtraction as coordinate lag until calibrated.

**“End offset is the last message.”** Many APIs return the exclusive next position. Confusing it with the last included offset produces off-by-one reads and commits.

**“Commit what I just processed.”** Under next-offset semantics, commit one past the covered record, but only after required state/effects are durable. Confirm the client API contract.

**“One topic has one offset.”** A partitioned topic has a vector. A scalar loses restart and cut information.

**“The sum of lag is healthy.”** One partition can be stuck or beyond retention while the sum appears acceptable. Report distribution, maximum, oldest obligation, and minimum replay margin.

**“Zero lag means fresh.”** The consumer may have caught the broker but publication, caches, source capture, or event-time completeness can still be stale. Measure end-to-end visibility.

**“Reset to latest fixes an invalid offset.”** It discards retained obligations. Reset to earliest may still skip expired history. Stop, quantify, recover from archive if possible, reconcile, and record approval.

**“Adding partitions preserves ordering.”** Common routing remaps keys, and old records do not move. Version and migrate routing/state at a cut.

**“More partitions fixes a hot customer.”** An indivisible ordered key still occupies one partition. Redesign the key/order domain or isolate the tenant.

**“Replication factor three means three safe copies.”** Current in-sync acknowledgement, placement, correlated failure, deletion, and restore matter. Configuration is not evidence.

**“A follower is another partition.”** It is a copy of the same logical log. Counting replicas as consumer order domains overstates parallelism.

**“A mirrored offset is the source offset.”** Destination append coordinates are local. Carry source coordinates and validate mapping.

**“Recreating the same name restores the topic.”** The generation and history changed. Stale checkpoints must fail closed on identity mismatch.

**“Compaction is deduplication.”** It retains selected key versions under product rules; it does not prove occurrence deduplication or preserve every historical delta.

**“Retention is uniform time.”** Size eviction and skew can shorten hot partitions. Observe actual beginnings and margins.

**“Automatic sharding removes topology.”** It may hide shard management, but keys, local order, sequence scope, quotas, consumer progress, lineage, and recovery still exist.

**“Timestamp seek reproduces 09:00 exactly.”** Each partition and clock can map differently; expired data cannot be sought back. Persist the resolved vector and boundary evidence.

## Worked Examples

### Example 1

A team proposes one `company-events` topic for payments, support tickets, employee audit, and IoT readings. The records have different owners, keys, retention, privacy, traffic, and consumers. The right review does not begin with partition count. It separates coherent domain contracts, then assigns each topic generation an owner, schema/key policy, access boundary, retention class, topology, and lifecycle. Shared platform conventions remain common without merging incompatible data products.

### Example 2

Topic `orders` has partition 0 offsets 90–100 and partition 1 offsets 10–20. Record `(p0,95)` cannot be declared later than `(p1,18)` from offsets. Each comparison is valid only within its local partition. If both concern the same order, routing is already violating the intended key order or the application needs explicit version/causal conflict semantics.

### Example 3

A reproducible read stores topology `orders-v3` and exclusive cut `{0:120,1:83,2:901}`. It processes offsets below each boundary. The artifact also records beginning positions, source topic ID, schema/transform versions, and gaps. Re-running against that vector selects the same coordinate prefixes while “read through 12:00” would require resolving mutable timestamps again.

### Example 4

A client processes offset 41. If its API commits the next position, it stores 42 after state and sink acceptance. Storing 41 causes offset 41 to be fetched again; storing 43 skips offset 42. If the client stores 42 before the sink accepts record 41, restart can skip its effect even though the arithmetic looks correct.

### Example 5

Beginning/head/commit for three partitions are `(100,160,130)`, `(50,80,49)`, and `(0,10,10)`. Lags appear 30, 31, and 0, but partition 1's commit is below its beginning. Total lag is not the main incident: direct replay has already become impossible for that partition. Stop, locate archive coverage for the missing interval, rebuild/reconcile, and create a governed new checkpoint.

### Example 6

A 12-partition topic averages 24 MiB/s, but one tenant contributes 9 MiB/s to a partition demonstrated safe at 6 MiB/s. Adding 12 more partitions might redistribute other keys but the tenant remains one key/order domain and still exceeds capacity. The team must improve that domain's capacity, split its semantic order safely, isolate it, aggregate upstream, or renegotiate the guarantee.

### Example 7

A producer uses `hash(customer_id) mod 8`. Expanding to 12 partitions changes the result for many customers. Old customer events remain in the prior partitions while new events enter new ones. The team creates `orders-v4`, versions routing, captures the old terminal vector, rebuilds keyed state into the new layout, shadow-compares materialization, cuts producers/consumers with fencing, and retains `v3` for rollback and replay obligations.

### Example 8

A shard-based stream splits parent shard `s0` into children `s1` and `s2`. Current metadata lists only the children, but an offline consumer still has unread parent records. Its recovery plan processes `s0` to its terminal sequence, then begins children according to recorded lineage. Treating the current shard list as the whole history would omit data.

### Example 9

An operator requests replay from `2026-08-01T09:00Z`. The system queries each partition's timestamp index and resolves `{0:550,1:712,2:98}`. It inspects boundary events, notes producer-clock semantics and one expired earlier interval, stores the resolved vector as the actual replay cut, and gets approval for archive supplementation. The timestamp never becomes the checkpoint itself.

### Example 10

A mirror writes source partition/offset into destination headers. Source cut `{0:900,1:700}` maps to a destination set with different numeric offsets due to batching and retries. DR readiness is based on verified coverage of the source cut and materialization digests, not destination end positions. Failover translates the consumer checkpoint, fences the primary, and reconciles events accepted near the boundary.

## Cross-Program Connections

Distributed systems contributes replicated logs, leader epochs, quorum acknowledgements, failure domains, partial order, transactions, snapshots, fencing, and state-machine safety. Partition coordinates are meaningful only under those protocols and epochs.

Data structures contributes sequences, half-open intervals, vectors, hash functions, consistent hashing, range partitioning, trees, and directed acyclic lineage graphs. Off-by-one and remapping errors are data-structure errors with production effects.

Algorithms contributes load balancing, balls-into-bins behavior, heavy hitters, skew estimation, partition refinement, graph traversal, and consistent-hash movement. Average-case distribution does not excuse adversarial keys.

Database systems contributes write-ahead logs, log sequence numbers, pages/segments, MVCC visibility, high-water marks, transaction boundaries, indexes, materialized views, compaction, and recovery. Similar terms do not guarantee identical semantics across systems.

API and service engineering contributes resource identity, namespace design, pagination/cursors, idempotency, versioning, conditional operations, quotas, authentication, authorization, and deprecation. A topic is a long-lived asynchronous API.

Platform engineering contributes self-service topic provisioning, policy enforcement, tenancy, defaults, drift detection, quota/capacity automation, dashboards, guarded administration, and lifecycle controllers. Safe platforms make the coordinate contract difficult to violate.

Security engineering contributes producer/consumer/operator separation, ACL design, encryption and key availability, metadata confidentiality, audit, denial-of-service controls, and supply-chain trust for clients/serializers.

Privacy engineering contributes purpose-bound access, minimization, retention/deletion, legal hold, lineage across replicas/archives/mirrors/state, and careful diagnostic key handling.

Site reliability engineering contributes per-partition SLIs, lag/freshness/retention margin, saturation, capacity, failure drills, reset/restore runbooks, regional failover, and evidence-driven objectives.

Formal methods contributes scoped identities, invariants, state machines, vector cuts, refinement across topology changes, and model/property testing for gaps, duplicates, resets, and stale epochs.

## References

1. Apache Kafka. [Introduction, Apache Kafka 4.3](https://kafka.apache.org/43/getting-started/introduction/). Accessed 2026-09-03. Primary documentation for topics, partitions, per-partition ordering, producers, consumers, retention, and replication.
2. Apache Kafka. [Design, Apache Kafka 4.3](https://kafka.apache.org/43/design/design/). Accessed 2026-09-03. Primary design documentation for partitioned logs, distribution, consumer position, delivery, and replication concepts.
3. Apache Kafka. [Log Implementation, Apache Kafka 4.3](https://kafka.apache.org/43/implementation/log/). Accessed 2026-09-03. Primary implementation documentation for log segments, offsets, indexes, retention, and compaction.
4. Apache Kafka. [Topic Configurations, Apache Kafka 4.3](https://kafka.apache.org/43/configuration/topic-configs/). Accessed 2026-09-03. Primary configuration reference for topic retention, cleanup, segment, replication, and size policies.
5. Apache Kafka. [TopicPartition API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/common/TopicPartition.html). Accessed 2026-09-03. Primary client API documentation for topic-and-partition identity.
6. Apache Kafka. [OffsetAndMetadata API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/OffsetAndMetadata.html). Accessed 2026-09-03. Primary client API documentation stating the committed offset should be the next record consumed.
7. Apache Pulsar. [Messaging Concepts, Apache Pulsar 4.2](https://pulsar.apache.org/docs/4.2.x/concepts-messaging/). Accessed 2026-09-03. Primary documentation for topic namespaces, partitioned topics, message IDs, routing, subscriptions, retention, and compaction.
8. Amazon Web Services. [Amazon Kinesis Data Streams Terminology and Concepts](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html). Accessed 2026-09-03. Primary documentation for streams, shards, partition keys, sequence numbers, retention, consumers, and capacity.
9. Amazon Web Services. [Reshard a Stream](https://docs.aws.amazon.com/streams/latest/dev/kinesis-using-sdk-java-resharding.html). Accessed 2026-09-03. Primary documentation for Kinesis shard split/merge operations and parent-child topology evolution.
10. Google Cloud. [Seek to a Timestamp or Snapshot](https://cloud.google.com/pubsub/docs/replay-overview). Accessed 2026-09-03. Primary documentation for Pub/Sub retention, snapshots, and seek/replay behavior.
11. Google Cloud. [Pub/Sub Subscription Seek API](https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.subscriptions/seek). Accessed 2026-09-03. Primary API reference for seeking retained messages by timestamp or snapshot and its retention boundary.

## Exercises

### Exercise 1

For each value, state whether it can identify one record by itself: topic name `orders`; partition `3`; offset `81`; `(orders,3,81)`; `(cluster-a, topic-resource-7, topology-v2, 3, 81)`; business event ID `evt-9`; timestamp `09:00`. Explain what each identifies, which identities must travel with a record, and why transport coordinate and occurrence identity are both required.

### Exercise 2

A four-partition topic reports beginning offsets `(5,20,0,11)`, exclusive heads `(25,25,8,18)`, and committed next offsets `(17,25,3,10)`. Compute per-partition lag where arithmetic is meaningful, total/max apparent lag, replay margins, and retained spans. Identify the correctness incident and prescribe a safe response.

### Exercise 3

A topic must sustain 32 MiB/s peak ingress. Testing establishes 6 MiB/s safe ingress per well-balanced partition with recovery reserve. Compute the throughput lower bound on partitions. Then a single ordered tenant generates 8 MiB/s. Explain why the bound is insufficient and propose at least three options. Also list costs that argue against choosing an arbitrarily huge partition count.

### Exercise 4

A consumer is 43,200,000 records behind after a six-hour outage. Live arrival is 2,000 records/s and demonstrated total processing capacity is 5,000 records/s. Broker retention remaining at recovery start is five hours for the hottest partition. Compute ideal catch-up time, determine whether direct recovery has margin under the simple model, and name evidence/controls needed before relying on it.

### Exercise 5

A topic with eight partitions uses `hash(key) mod 8` and must expand. Design a migration that preserves auditable per-key history and state. Include topic/topology identity, old/new cut vectors, producer routing, consumer/state behavior, validation, rollback, retention, mirror/DR mapping, and stale-writer fencing. Explain why simply changing the count to twelve is incomplete.

## Answers to the Exercises

### Answer 1

None of the first three values identifies one record: a topic contains many partitions/records, partition 3 exists in many topics/clusters/generations, and offset 81 is local. `(orders,3,81)` is still ambiguous across clusters and topic deletion/recreation. `(cluster-a, topic-resource-7, topology-v2,3,81)` can identify at most one transport position under a documented platform coordinate contract. `evt-9` identifies a logical occurrence only if its issuing authority/scope and uniqueness are governed; it may appear at multiple transport coordinates through retry or mirroring. `09:00` is neither unique nor a coordinate. Carry immutable topic generation, topology epoch, partition, offset, source coordinate if copied, and separate occurrence/business identity plus schema/integrity context. The coordinate supports exact retrieval/progress; occurrence identity supports deduplication, causation, correction, and cross-copy reconciliation.

### Answer 2

For partitions 0–3, apparent lags $h-c$ are `8,0,5,8`, totaling 21 with maximum 8. Replay margins $c-b$ are `12,5,3,-1`; retained spans $h-b$ are `20,5,8,7`. Partition 3's commit 10 is below beginning 11, so its direct replay prerequisite fails and treating its apparent lag as an ordinary queue is unsafe. Stop/fail closed rather than silently reset. Confirm topic generation, epochs, boundary/visibility conventions, and metric snapshot consistency; preserve the current cut; locate authoritative archive/snapshot coverage for the missing coordinate; reconstruct into isolation; validate counts/digests/domain state and sink effects; obtain approval for unavoidable loss if no source exists; reconcile consumers; then establish a new versioned checkpoint. Investigate why retention margin monitoring/capacity failed.

### Answer 3

The balanced throughput bound is $\lceil32/6\rceil=6$ partitions. But the ordered tenant alone needs 8 MiB/s and must occupy one order domain, exceeding the demonstrated 6 MiB/s capacity; distributing other keys or adding partitions does not split it. Options include increasing tested per-partition end-to-end capacity, isolating the tenant on a stronger dedicated stream, relaxing its total-order requirement and using deterministic subkeys plus explicit recombination/version conflict rules, aggregating upstream, or negotiating admission/latency. Excess partitions increase replicas/storage, broker/controller metadata, segments/files, connections/fetches, assignments/rebalances, state/checkpoint fragments, monitoring cardinality, leader elections, recovery operations, minimum compute, and cost.

### Answer 4

The backlog is 43.2 million records. Net recovery rate while live traffic continues is $5{,}000-2{,}000=3{,}000$ records/s, so ideal catch-up is $43{,}200{,}000/3{,}000=14{,}400$ seconds, or four hours. Against five hours remaining, the simplistic coordinate/time margin is one hour. It is not safe evidence by itself. Verify the hottest partition—not aggregate—capacity, bytes/record and large transactions, skew/state, source/network/broker read limits, checkpoint/GC, retries, sink acceptance, live/replay priority, head growth, actual beginning-offset eviction, schemas/keys/code/reference/state availability, and publication reconciliation. Extend/freeze retention or restore from archive, shed nonessential load, reserve capacity, alert on projected crossing, and checkpoint accepted effects while continuously recomputing the margin.

### Answer 5

Create a new topology epoch or preferably an explicit topic generation rather than treating twelve as the same coordinate space. Inventory immutable old topic identity, routing/serializer version, complete partition set, all consumers/checkpoints/state, mirrors, retention, and effects. Fence or pause old producers at an exact eight-component terminal cut, or dual-write through one authoritative router with occurrence IDs and receipts. Version the new routing and record the twelve-partition start cut. Rebuild or migrate keyed state from a complete old prefix, retaining each source coordinate; prevent new-key effects from racing unprocessed old-key history. Shadow-consume and compare per-key sequences, counts/digests, materializations, lag/capacity, and sink candidates over exact cuts. Cut readers/publication conditionally, fence stale producers and checkpoint writers by epoch, and preserve old data/state/archive plus rollback mapping until every consumer and recovery objective expires. Mirrors carry source generation/partition/offset and validate coverage rather than equating destination numbers. Merely changing eight to twelve remaps many `hash mod N` keys, leaves old records in prior partitions, creates two order domains per moved key, invalidates scalar/default checkpoints, and says nothing about state, effects, DR, or rollback.
