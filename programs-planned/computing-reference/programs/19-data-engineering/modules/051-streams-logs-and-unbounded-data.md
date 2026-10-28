---
module_id: DE-051
program: Data Engineering
level: 2
module_number: 51
title: Streams, Logs, and Unbounded Data
status: complete
last_verified: 2026-09-03
---

# Streams, Logs, and Unbounded Data

## One-Page Review

### Governing question

How should an engineer model, retain, transform, and operate data that continues to arrive without a natural final element, so that every emitted result has a precise cut, meaning, replay boundary, resource envelope, and correction path?

### Essential definitions

- A **stream** is a sequence or partially ordered collection of observations made available over time; its source may be bounded or unbounded.
- A **bounded dataset** has a finite, knowable membership under a declared cut; **unbounded data** has no intrinsic final element, even though every observation at a finite instant is a finite prefix.
- An **event** records that something occurred, an **observation** records what a producer/source reported, and a **command** requests an effect. Treating these as interchangeable changes replay and ownership semantics.
- A **log** is a durable append-oriented record of ordered entries within an explicit ordering domain. Append-only physical history can represent mutable business state through assertions, corrections, and tombstones.
- A **record envelope** binds source/epoch, identity, key, payload, schema, time fields, ordering coordinate, transaction/correlation context, and integrity metadata.
- A **stream cut** is a consistent boundary selecting a finite prefix from every relevant source/order domain; “now” without captured coordinates is not reproducible.
- A **materialization** is a derived state or result computed from a stream prefix under a transformation, schema, conflict, and time policy.
- A **changelog** represents changes to a logical relation; applying it under declared rules yields a materialized relation at a cut.
- **Replay** reprocesses retained observations from a named cut or checkpoint under the same or a new explicit semantic version.
- **Lag** is distance between a producer/head coordinate and an acknowledged or accepted consumer coordinate, measured in source positions, records/bytes, or time under defined semantics.
- **Backlog** is accepted work not yet brought to the required processing/acceptance state; it is not merely queue length.
- **Backpressure** is a mechanism by which constrained downstream demand limits upstream production/admission or triggers a bounded overflow policy.
- **Stability** means long-run effective service capacity exceeds offered load for each constrained stage/resource, with headroom for variance and recovery.
- A **retention horizon** is the earliest boundary still replayable after accounting for log data, schemas, code/configuration, keys, reference data, state/checkpoints, and sink compatibility.
- **Streaming** describes a processing relationship to incrementally available data; low latency, exactly-once effects, event-time correctness, and infinite retention are separate properties.

### Central model, mechanism, or theorem

Let source $S$ expose an unbounded logical sequence

$$
S=(e_1,e_2,\ldots),
$$

within a declared ordering domain. At any durable cut $c$, the known prefix $S_{\le c}$ is finite. A materialization is therefore cut-relative:

$$
M(c)=\operatorname{fold}_{f,v}(M_0,S_{\le c}),
$$

where $f$ is a deterministic transition rule, $v$ binds schema/code/configuration/reference semantics, and $M_0$ is an identified base state. Later observations can produce $M(c')\ne M(c)$ without making the earlier answer dishonest, provided its cut and revision policy were explicit.

For stage $i$ over interval $t$, let $A_i(t)$ be admitted work, $C_i(t)$ accepted service, and backlog

$$
B_i(t+1)=\max(0,B_i(t)+A_i(t)-C_i(t)).
$$

If sustained effective arrival exceeds sustainable service, backlog or loss must grow; more buffering only delays the consequence. A sound design chooses admission/backpressure/load shedding, retention, state, result revision, and recovery semantics rather than hiding the mismatch behind an “unbounded” queue.

### Critical invariants

- Source system, epoch, ordering domain, record coordinate, occurrence identity, payload/schema, and transaction boundary are explicit; no global order is inferred from local positions or timestamps.
- Every emitted snapshot/result names the exact stream cut, transformation/schema/configuration/reference versions, base/checkpoint, and revision/late-data policy.
- Physical append-only history is distinguished from business truth: updates, retractions, corrections, and tombstones require interpretation.
- Bounded and unbounded describe source membership under a cut, not file versus broker, batch versus streaming API, or finite versus infinite execution time alone.
- Reprocessing the same accepted prefix under the same deterministic semantics yields the same logical materialization within declared equivalence.
- Checkpoints/progress cannot advance beyond durable recoverable source and sink/state evidence; process acknowledgement alone is insufficient.
- Buffers, queues, in-flight work, keyed/window state, retry lanes, quarantine, and candidates have explicit capacity, admission, spill, expiry, and overload behavior.
- Every constrained stage/resource has measured offered load, sustainable service capacity, variance/headroom, and a response when backlog age threatens retention or objectives.
- Backpressure crosses each asynchronous boundary or an explicit bounded loss/degradation policy owns the gap; local flow control does not automatically slow an external producer.
- Retention covers the proven replay/recovery horizon and includes schemas, codecs, encryption keys, code/configuration, reference data, checkpoints, and output repair capability.
- Source-of-record, event/log, materialized view, and consumer copy ownership are distinct; deletion/privacy/security policy applies to all retained representations.
- Schema and semantic evolution preserve self-description or registry identity, compatibility direction, old-reader/writer behavior, and historical replay interpretation.
- Metrics expose input/head, accepted progress, backlog records/bytes/age, throughput, saturation, drops/quarantine, retention margin, checkpoints, and materialization freshness.
- “Exactly once,” “real time,” “ordered,” “immutable,” and “complete” are never used without their scope and evidence.

### Common failures

Common failures include calling any message feed a log; assuming append-only means truthful or immutable under administrative deletion; equating stream processing with one-record-at-a-time execution; treating a broker as the system of record without retention/restore proof; using ingestion timestamp as global order; publishing a mutable aggregate without cut/revision; updating a table from events while discarding retractions; acknowledging before durable state/output; sizing only record counts while bytes/skew/state dominate; buffering without a bound; retrying into overload; measuring lag only as offsets while old large records remain; applying backpressure inside one library while the external source continues; expiring log data before recovery/replay; changing schema/codec/reference data without preserving historical interpretation; replaying events into non-idempotent sinks; and claiming the stream is current because consumers are connected.

### Compact example

An append-only account-change stream contains six deltas. Prefix cut 3 materializes `A=3, B=4`; cut 6 materializes `A=6, B=3, C=2`. Neither snapshot is “the” timeless stream; each is correct only under its cut and fold. A processor accepts arrival counts `(3,5,2,6)` over four seconds with capacity four per second. Backlog follows `(0,0,1,0,2)`: total average arrival equals capacity, yet bursts create a maximum backlog of two and leave two records pending. The finite trace demonstrates prefix and queue arithmetic, not long-run stability. Replay additionally requires retained entries and interpretation artifacts.

### Connections

[DE-026](026-database-change-data-capture.md) introduces database change capture, and [DE-030](030-designing-replayable-raw-ingestion.md) defines durable raw evidence. [DE-039](039-deterministic-transformations.md) and [DE-044](044-retries-timeouts-and-idempotency.md) supply replay and effect constraints; [DE-049](049-run-metadata-and-operational-state.md) provides authoritative run/checkpoint identities; [DE-050](050-designing-an-operable-data-workflow.md) supplies capacity and recovery envelopes. DE-052 through DE-060 will specialize log topology, ordering, consumers, delivery/effect guarantees, time, windows, state, and disorder.

## Governing Question

What exactly does a streaming result mean when the input has no final row, different observers see different prefixes, producers can correct prior facts, consumers can fall behind, and retained history is finite?

A bounded query can wait until its declared input membership is complete, run, and publish one result. An unbounded source does not offer that natural completion point. Engineers must choose when to observe, which prefix or time domain counts, what result is emitted, whether later arrivals revise it, and how long the system can recover or replay. These choices are semantics, not implementation tuning.

The term stream is overloaded. It may mean transport bytes, messages delivered through a queue, an ordered commit log, database change events, a sequence of domain facts, an unbounded relational changelog, or a programming API. Each has different identity, order, retention, and replay properties. Begin with a contract rather than assuming properties from the product category.

Likewise, append-only storage does not mean business state never changes. A later record may supersede an earlier assertion, reverse a transaction, delete a key, correct event time, or change schema interpretation. Materialized state is a function of the selected history and fold rules. Preserving the log keeps evidence; it does not choose the correct projection.

Streaming also moves resource failure from a single job into continuous stability. Bursts create queues, slow keys accumulate state, unavailable sinks consume retention margin, and retries amplify demand. A system whose steady offered load meets or exceeds effective capacity cannot catch up without admission change, scaling a real bottleneck, degradation, or loss. Unlimited logical input must be operated with finite resources.

## Why This Matters

Businesses increasingly need new facts before the next batch boundary: fraud decisions, inventory, telemetry, personalization, operational dashboards, audit trails, and data synchronization. Incremental processing can reduce latency and avoid repeatedly scanning old data. It also exposes timing, ordering, retry, state, and recovery choices that a bounded batch may hide.

Unboundedness changes completeness. “All records” is undefined without a cut, watermark, manifest, transaction boundary, or other closure rule. A current account balance can be correct through source position 500 while position 501 already exists elsewhere. A daily window may be emitted before all late events. A dashboard must communicate cut/freshness/revision, not merely a number.

Logs decouple production from consumption. Multiple consumers can process at different rates, replay independently, and construct new views. This is valuable only while data, schemas, keys, and source coordinates remain available and consumers can catch up before retention. A slow consumer can silently cross the point where recovery from the log is possible.

Streaming magnifies skew. Average input rate can be modest while one key, partition, tenant, large record, or transaction dominates a worker. State for an unbounded cardinality of inactive keys can grow forever. Byte rate, compute cost, state size, checkpoint duration, sink latency, and metadata operations matter alongside record rate.

Failure boundaries are distributed. A processor can update state, emit a sink write, then crash before advancing progress. A source can redeliver. A worker can restart from an older checkpoint. A downstream API may commit after timeout. Later modules develop delivery and exactly-once effects; this introduction establishes why stable identity, replay, candidate outputs, receipts, and reconciliation are prerequisites.

Streaming history is security-sensitive. Event logs often preserve detailed behavior, deleted values, old permissions, identifiers, and schema versions. Broad consumer access or indefinite retention creates a durable leakage surface. Encryption, tenant isolation, purpose limitation, field minimization, access auditing, deletion, and derived-state handling belong in the design.

Finally, batch and streaming are not opposing religions. A bounded snapshot can be read from a log cut; an unbounded table can be maintained by changelog; a streaming system may execute micro-batches; a batch repair can bootstrap streaming state. A unified semantic model lets teams select execution according to latency, cost, correctness, and operational needs.

## Prerequisites and Retrieval

Retrieve the product/consumer contract: decision, acceptable latency, correctness/completeness, revision, access, retention, failure/degradation, replay, and recovery expectations. Identify whether consumers need individual events, an ordered history, current keyed state, windowed aggregates, alerts, synchronization effects, or snapshots.

Retrieve source semantics: source of record; system/cluster/tenant/epoch; bounded/unbounded nature; event/command/state meaning; occurrence identity; keys; ordering domains; transaction boundaries; event/ingestion times; delete/tombstone/correction semantics; duplicate/reorder/loss guarantees; schemas/codecs; expected rates/sizes/skew; retention; replay/reset; acknowledgement; quotas; and failure contacts.

Retrieve transport/log semantics: topics/streams/partitions/shards; append authority; record coordinate/offset/sequence; replication/durability; acknowledgement levels; retention by time/size; compaction; administrative mutation/deletion; transaction support; maximum record/transaction; producer/consumer flow control; redelivery; snapshots; backups; region failure; and monitoring.

Retrieve processing semantics: bounded versus unbounded collections; per-record/micro-batch/hybrid execution; transformation graph; stateless/stateful operations; keys; joins; aggregation; event/processing time; windows/watermarks/triggers; delivery/effect guarantees; checkpoint/state backend; restart/rescale; side outputs/quarantine; and determinism.

Retrieve materialization/sink semantics: logical relation and primary key; insert/update/delete/upsert/retraction; candidate/accepted/published generations; transactional boundary; idempotency/fencing; conflict resolution; consistency/read visibility; schema evolution; output revision; audit; and consumer caching.

Retrieve capacity/stability evidence: arrival records/bytes/transactions by distribution; bursts; compression; decode/transform cost; hot keys; state cardinality/size/TTL; checkpoint and recovery bandwidth; network; broker storage/IO; consumer throughput; sink QPS/connections/slots/logs; in-flight/buffer limits; retry amplification; quotas; headroom; retention margin; and growth.

Retrieve recovery evidence: source and log retention; immutable raw archive; checkpoint frequency/durability/compatibility; exact restore position; schemas/codecs/keys/code/config/reference versions; reprocessing isolation; sink receipts; output repair; bootstrap snapshot and change cut; disaster restore; and last replay exercise.

Retrieve governance: payload/metadata classification; tenant boundaries; producer and consumer identities; authorization; encryption and key lifecycle; schema registry access; secrets; diagnostic samples; retention/deletion/legal hold; purpose; residency; derived materializations; and audit.

Distinguish observation from event; event from command; event log from application log; source coordinate from event time; sequence from set; local order from global order; boundedness from storage medium; unbounded source from infinite individual record; stream from transport connection; append from durability; append-only storage from immutable administration; history from current truth; record from logical occurrence; message delivery from effect; changelog from snapshot; tombstone from absence; cut from clock time; head from accepted progress; lag positions from lag time/bytes; queue length from backlog obligation; buffer from durable retention; backpressure from dropping; state from checkpoint; checkpoint from sink commit; replay from duplicate delivery; replay horizon from configured retention alone; and low latency from semantic correctness.

Create a streaming foundation contract:

| Concern | Required decision and evidence |
|---|---|
| Meaning | Event/observation/command/state change, source of record, correction authority |
| Identity | Source/epoch, occurrence ID, key, transaction, schema, payload binding |
| Order | Exact ordering domain/coordinate, concurrency, timestamp roles, no inferred global order |
| Boundedness | Natural completion or unbounded source, finite cuts and closure semantics |
| Log | Append/durability/replication, retention/compaction/deletion, coordinate and restore |
| Transform | Graph/version, stateless/stateful fold, deterministic envelope, revision policy |
| Materialization | Relation/key, update/retract/delete, cut, candidate/publication, consumer visibility |
| Progress | Head and accepted checkpoints, lag records/bytes/time, gaps and confidence |
| Flow | Arrival/service distributions, buffers, backpressure/admission, overload/loss behavior |
| State | Key/window scope, growth/TTL, checkpoint/restore/rescale, schema compatibility |
| Recovery | Replay horizon, raw/snapshot bootstrap, interpretation artifacts, sink reconciliation |
| Governance | Producer/consumer authority, tenant/privacy/security, retention/deletion/audit |

Write a testable claim: “For source epoch `e`, ordering domains `P`, and cut vector `c`, every retained record through `c` has identity/schema/integrity evidence; transformation `f@v` folds from checkpoint `k` to materialization generation `m(c)`; accepted progress does not exceed recoverable source/state/sink receipts; offered load fits service with bounded backlog and retention margin; and replay from the preserved base reproduces `m(c)` under declared equivalence.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish streams, event logs, changelogs, snapshots, commands, observations, materializations, and transport connections;
2. model an unbounded source through finite reproducible cuts without claiming a natural final result;
3. specify record envelopes, source epochs, ordering domains, corrections/tombstones, schema identity, and transaction context;
4. derive cut-relative materializations as deterministic folds and explain when incremental and batch recomputation are equivalent;
5. calculate backlog evolution, throughput, lag, retention margin, and basic stability while preserving burst and skew caveats;
6. design bounded buffers and backpressure/admission/load-shedding behavior across asynchronous and external boundaries;
7. connect checkpoints, state, source progress, candidate outputs, sink receipts, and replay into a safe recovery boundary;
8. evaluate log retention, compaction, archival raw, schema/key/code/reference preservation, and bootstrap strategies;
9. choose between record-at-a-time, micro-batch, bounded replay, and unified relational/dataflow models according to product constraints; and
10. identify the security, privacy, tenancy, observability, testing, and operational evidence required before trusting a streaming product.

## Core Exposition

### Define the thing that flows

Begin with domain meaning. “OrderPlaced” may be a fact owned by checkout; “SetCustomerTier” is a command; a CDC row update is an observation of database mutation; a periodic sensor reading is an observation; a current customer record is state. These have different truth, duplication, correction, privacy, and replay semantics.

An event should record an occurrence that producers do not rewrite silently. Correction is another explicit event or governed supersession. A command may be accepted, rejected, retried, or produce several events. A state-transfer message may simply announce the latest version and make intermediate versions irrelevant to some consumers. Name which model applies.

Define occurrence identity separate from payload equality and transport delivery. Two users can perform identical actions; one action can be delivered twice; one identity with different payload is a conflict. Bind source/epoch, producer, key, schema, payload digest, event/record time fields, transaction/correlation/causation, and trace context as needed.

Do not infer domain truth from an append. Producers can be buggy or unauthorized, and a database CDC record reports a storage transition, not necessarily a business event. Validate producer authority and contract; retain lineage to the source of record.

### Separate sequence, stream, and log

A mathematical sequence has a total order. A production stream may be a union of independently ordered sources with no meaningful global order. A network connection carries bytes over a period but is not necessarily durable or replayable. A broker topic can be partitioned into logs. Use qualified language.

A log appends entries and provides a coordinate within its order domain. Apache Kafka describes event streaming as capturing, storing, processing, and routing real-time event streams and provides durable topic storage; its design documentation describes partitioned logs. The product illustrates a log-backed stream, but topology, offsets, producers, consumer groups, and guarantees require explicit configuration and are developed in later modules.

Append-only means new logical entries are added rather than earlier entries edited through the normal API. Administrative deletion, retention expiry, compaction, corruption, or disaster may still remove bytes. Replication improves durability only under named acknowledgements, failure domains, and restore evidence.

Application logs are diagnostic text/events about software execution. An event log is domain or state-change data designed for consumption and replay. Mixing them creates unstable schemas, sensitive leakage, and incorrect retention expectations.

### Model boundedness independently of execution

A bounded dataset has finite membership under a declared boundary: a manifest, snapshot, transaction cut, file set, or coordinate range. Its size may be enormous or initially unknown. An unbounded dataset continues to acquire members and has no intrinsic final cut.

Apache Beam defines bounded and unbounded `PCollection`s by source nature and uses one programming model for data-parallel transforms. A bounded amount can also be read from an unbounded source by choosing a cut. Conversely, a file directory watched forever is an unbounded source even though each file is finite.

Batch execution can process a bounded prefix of a log. A streaming engine can process a bounded dataset. Micro-batch systems repeatedly process finite increments while presenting continuous results. Boundedness, latency, and execution engine are orthogonal.

An individual event must be bounded in bytes and processing. “Unbounded element” APIs usually mean an operation that can emit or work indefinitely, not that a single serialized record may consume infinite resources. Set record, transaction, decompression, nesting, and computation limits.

### Use cuts to make statements reproducible

For one totally ordered log, cut $c$ selects all entries at or before coordinate $c$. For multiple independent domains, use a cut vector $\mathbf{c}=(c_1,\ldots,c_p)$. A wall-clock query time is not a cut unless every source maps it consistently and durably.

A consistent cut must respect transactions and causal/source constraints the product needs. Reading half a multi-record transaction can expose impossible state. Combining a snapshot with CDC requires a boundary showing which changes are included in the snapshot and which begin the log tail.

Every materialized output records cut vector, source epochs, gaps, schema/transform/config/reference versions, base checkpoint, and publication generation. A consumer can then distinguish “balance through c” from timeless truth.

Cuts support audits, replay, backfills, testing, and comparisons. Run old and new transformations against the same prefix. Recompute a materialization from base plus log. Freeze a failing interval before retention advances. Never re-resolve “latest available” during reconstruction.

### Interpret an append-only changelog

An append-only physical log can encode inserts, updates, deletes, corrections, and retractions. Define the logical relation and key. Common records carry before/after images, operation type, version, and source transaction metadata. A tombstone may mean logical delete, compaction hint, redaction marker, or missing value depending on contract.

PostgreSQL logical decoding converts persistent table changes from write-ahead logging into an application-specific stream, and replication slots identify streams of changes for clients. Old row availability depends on replica identity and configuration. Debezium connectors capture database changes and route change events through Kafka Connect or other messaging infrastructure. These are mechanisms; consumers still need keys, schema, transaction, snapshot/tail, delete, and replay semantics.

Define fold $M_{n+1}=f(M_n,e_{n+1})$. For keyed replacement, a newer authorized version replaces prior value; for delta events, add/subtract; for sets, insert/delete; for facts, append. Conflict/order policy must be explicit. An arbitrary last-arrival-wins rule can corrupt state.

Keep history distinct from the materialized view. A current-state table is fast to query but cannot necessarily reconstruct how it arose. A compacted log may preserve latest keys but lose intermediate facts. Retain what audit, replay, corrections, and consumers require.

### Relate streaming to tables and snapshots

A stream prefix can be viewed as a finite relation of records. A changelog can maintain a table. A table snapshot difference can produce changes. This duality supports unified batch/stream APIs but does not erase operational distinctions such as arrival, retention, state, and revisions.

Apache Flink describes itself as a stateful processor for bounded and unbounded streams, and its Table/SQL concepts present unified relational semantics for batch and streaming modes. Streaming relational queries may emit updates/retractions and retain state; consumers must support the result mode and keys.

Not every query has a finite stable result over an unbounded input. Global `count(*)` changes forever. An unwindowed sort of all history cannot emit a final total order with bounded memory. A join may retain unmatched records indefinitely. Rewrite into incremental keyed state, finite windows, approximations, bounded reference joins, or a consumer-facing revision contract.

Snapshots remain useful. Periodically publish an immutable materialization and cut, bootstrap new consumers from it, then apply the tail. Verify snapshot/log continuity. A snapshot without the tail is stale; a tail without a compatible base may require replay from origin.

### Choose emission and revision semantics

Ask four questions for every result: what is computed; where in event/data time; when is it emitted; and how do later records change it? The Dataflow Model paper makes these axes explicit for unbounded and out-of-order processing and discusses correctness/latency/cost tradeoffs. Later modules develop event time, windows, watermarks, and late data.

Possible outputs include per-event transformed facts, continuously updated keyed state, periodic snapshots, finite-window aggregates, alerts, and external effects. Each needs a consumer contract. A dashboard can accept revised aggregates; a payment cannot be casually retracted.

Label provisional versus final under the declared policy. “Final” is scoped to an observed completeness criterion and allowed lateness, not metaphysical certainty. A source correction after finalization may create a new revision or restatement.

Use stable output identity so a later revision supersedes rather than duplicates. Record prior/new generation and cause. Preserve consumer notification and cache invalidation. If consumers cannot process retractions, design append-only compensations or delay emission.

### Understand progress without a terminal end

An unbounded job does not reach 100 percent of all future input. Progress is relative to source heads/cuts, accepted processing coordinates, materialization freshness, backlog, and consumer objectives. Define each ordering domain.

Coordinate lag is $H-C$ only within a comparable source/epoch/domain and may not reflect work. One large compressed record can cost more than thousands of small ones. Track records, bytes, event/ingestion age, estimated work, state/checkpoint, and sink backlog.

Use accepted progress, not merely fetched/read positions. If a consumer fetches records, updates memory, then crashes before durable state/output, recovery must reread. Checkpoint cannot pass the greatest input represented by a recoverable state and committed/idempotent output boundary.

For multiple domains report distributions/max and attribution rather than summing incomparable offsets. A single hot/shard lag can violate a product while total throughput looks healthy.

Retention margin is time/positions/bytes between the oldest needed replay coordinate and earliest retained coordinate, adjusted for observed catch-up capacity and restore time. Alert before margin reaches zero; once history expires, scaling cannot reconstruct it.

### Analyze flow, backlog, and stability

At a queue boundary, backlog evolves from prior backlog plus admitted arrivals minus accepted service. Measure rates over distributions and time horizons. Average arrival below average capacity is necessary but not sufficient for bounded latency under bursts, variance, vacations/outages, and correlated load.

For stable long-run operation, sustainable effective service must exceed offered load at each bottleneck with headroom. Capacity includes downstream quotas, serialization, network, checkpoint pauses, garbage collection, state backend, and sink commits—not nominal worker CPU alone.

Little's Law relates long-run average number in a stable system $L$, arrival/throughput rate $\lambda$, and time in system $W$ as $L=\lambda W$, under its assumptions. It is a diagnostic relationship, not permission to ignore distributions or overloaded/nonstationary periods.

Measure backlog age and deadline risk, not only count. A queue of ten enormous old transactions may be worse than a million tiny recent metrics. Segment by tenant/key/class and enforce fairness so a hot producer cannot starve others.

Plan recovery capacity. After an outage of duration $d$ at arrival rate $\lambda$, backlog is roughly $\lambda d$ before considering retries. With post-recovery capacity $\mu>\lambda$, ideal catch-up time is approximately $\lambda d/(\mu-\lambda)$. This ignores burst, state, sink, and quota limits; validate empirically.

### Make every buffer bounded

Buffers exist in clients, brokers, network libraries, workers, shuffle, state backends, sinks, retry queues, dead letters, candidates, and consumers. Inventory capacity in records and bytes, allocation, spill, persistence, eviction, fairness, and metrics.

An unbounded in-memory queue converts load mismatch into process death. A disk spill converts it into storage pressure and slower recovery. A durable broker converts it into retention/cost pressure. None eliminates the mismatch.

When full, choose deliberately: block/backpressure, reject admission, shed low-priority work, sample/aggregate, spill within bound, route to quarantine, degrade, or fail. Silent overwrite/drop is rarely acceptable for business events. Telemetry streams may permit sampling under an explicit loss contract.

Set maximum record and decompression ratios to prevent one element from exhausting memory. Bound per-key and total state. Use quotas and fair scheduling across tenants. Reserve capacity for control messages and recovery so data floods cannot make the system unmanageable.

### Propagate backpressure across boundaries

Backpressure means downstream demand controls upstream emission/admission. Reactive Streams specifies asynchronous stream processing with nonblocking backpressure so receivers are not forced to buffer arbitrary elements. Its scope is an API boundary; it does not automatically slow a database, device, webhook producer, or broker retention clock.

Map the whole path. A library may request ten records at a time while its connector prefetches thousands. A broker consumer may pause fetching while the producer continues, increasing durable backlog. A sink may throttle after the processor has already acknowledged source progress.

For push sources that cannot slow, admission must reject, shed under contract, or durably absorb within capacity/retention. For pull sources, reduce fetch. For partitioned consumption, pause hot domains while preserving heartbeat/lease behavior. For external APIs, respect rate and retry-after with jitter.

Avoid feedback oscillation. Aggressive scale-up, pause/resume, and retry can hunt around a limit. Use measured control intervals, hysteresis, bounded change, and downstream signals. Preserve fairness and critical priorities.

Backpressure is not failure recovery. A stuck consumer may require failover; a deterministic poison record requires quarantine; state corruption requires restore; retention exhaustion requires source/archive recovery. Classify why service fell behind.

### Build durable recovery boundaries

A recoverable streaming state binds source cut, operator state/checkpoint, code/config/schema/runtime, timers/time policies, pending transactions, and sink effect boundary. Store a manifest/digest and verify restore.

Checkpoint frequency trades recovery replay against coordination/storage/runtime cost. A frequent checkpoint that is slow, corrupted, or incompatible is weak evidence. Track completion duration, age, size, failures, alignment/pauses, retention, and restore tests.

Source acknowledgement/progress can advance only when the corresponding record is safely represented in recoverable state and output effects. Exactly how depends on the delivery/effect protocol; later modules develop this. If source and sink cannot transact together, stable intent/idempotency receipts or reconciliation are required.

Restart from a known checkpoint and replay the tail. Reject source epoch mismatch or missing coordinates. Fence stale workers. Keep candidate outputs isolated until validation/publication. Compare materialization controls before and after recovery.

Savepoints/snapshots support planned upgrades, while checkpoints support failure recovery; product terminology differs. Preserve operator/state identifiers and serializers. Test scale changes, schema evolution, code rollback/forward, and partial checkpoint loss.

### Establish the real replay horizon

Configured broker retention is only one component. Effective replay begins at the latest of the earliest available required artifacts: log records/raw archive, snapshot/base, schemas/codecs, encryption keys, transformation and dependencies, configuration, reference data, state migration, and compatible sink repair.

Time-based retention interacts with backlog and outage. A seven-day setting does not guarantee seven days if size limits evict earlier, compaction removes history, keys expire, or restoration takes days. Verify earliest coordinates per order domain and storage tier.

Keep authoritative raw beyond broker retention when recovery/business requirements demand it. [DE-030](030-designing-replayable-raw-ingestion.md) specifies manifests and durable source evidence. A bootstrap snapshot plus exact log boundary can shorten recovery, but continuity and compatibility must be proven.

Compaction preserves selected key state, not necessarily event history, sequence, duplicates, or audit. Tombstone retention affects deletion reconstruction. Archive migrations must retain coordinates, envelopes, schemas, integrity, and order-domain mapping.

Exercise full replay into isolated outputs. Measure read/compute/state/sink capacity and catch-up time; compare results at the same cut; test gaps/corruption/old schemas; and verify production publication/consumer repair. “We could replay” without a drill is a hypothesis.

### Evolve schemas and semantics over continuous history

Every record references a writer schema or self-describing version. Consumers choose compatible readers. Define backward/forward/full compatibility in terms of old/new producer/consumer operations, not only registry acceptance.

Additive fields can still break strict consumers, change defaults, alter keys, or expose sensitive data. Type/precision/time-zone/enumeration and semantic changes may decode while producing wrong answers. Test supported version pairs and representative historical records.

Long-lived streams contain many versions. Preserve registry entries indefinitely enough for retention/replay; avoid deleting codecs/classes/keys needed by archives. Bind transformation semantics to record schema and reference policy.

State schema evolves too. A new key or aggregation cannot necessarily restore an old checkpoint. Plan compatible state migration or bootstrap replay. Dual-read/write periods add reconciliation and exit criteria.

Unknown fields/types should fail or route safely under contract, not silently disappear when meaning/security is uncertain. Quarantine preserves source coordinate and bounded diagnostic evidence without blocking every domain unnecessarily.

### Secure and govern continuous data

Authenticate producers and authorize append by exact stream/tenant/schema. Validate size, schema, key, timestamps, transaction context, and rate. One compromised producer can create cost, backlog, poison records, or cross-tenant leakage.

Authorize consumers by purpose, field, tenant, history depth, and environment. A stream often contains history no longer visible in current operational state. Derived materializations and caches inherit classification and deletion obligations.

Encrypt transport and storage, manage key rotation/retention for replay, isolate accounts/networks, protect schemas/metadata, and audit reads/resets/exports. Consumer ability to reset backward is powerful access to history.

Minimize sensitive payloads at the source contract. Tokenization/pseudonymization does not eliminate linkage. Avoid secrets and unnecessary personal data in keys/headers, which may appear broadly in metrics/logs.

Deletion in immutable/log systems requires an explicit strategy: source minimization, keyed compaction, tombstones, rewrite, encryption-key erasure, derived-state purge, and proof across replicas/archives/backups. No single mechanism universally satisfies policy; involve privacy/legal/security owners.

### Observe an unbounded system

Instrument source head/availability, records/bytes/transactions in, schema/rejection/quarantine, per-domain accepted progress, records/bytes/time lag, oldest backlog age, throughput/service time, buffer occupancy, backpressure/pause, drops, retries, state size/cardinality/TTL, checkpoint age/duration/failure, sink commit, materialization cut/freshness, retention margin, restore/replay rate, and cost.

Track distributions and top contributors. Averages hide hot keys and stalled domains. Bound metric cardinality; keep exact identifiers in structured state/logs and use exemplars/trace links where safe.

Alert on consumer/product objectives, imminent retention loss, sustained instability, checkpoint/recovery risk, unauthorized access, and silent loss—not every transient delivery retry. A connected consumer with growing lag is unhealthy despite process liveness.

Monitor the monitoring and source progress. Missing head metrics can make lag appear zero. Emit last-success timestamps and cross-check independent broker/source/sink controls.

Retain run/deployment/schema/checkpoint/reset/rebalance/backfill/incident annotations. Diagnose changes in lag through arrival, service, retries, state, and sink saturation, not by increasing consumers blindly.

### Test finite traces without forgetting infinity

Every automated test uses finite input. That is sufficient to falsify invariants and verify behavior on chosen prefixes, not to prove bounded memory or correctness for all future sequences. State the coverage.

Test empty/singleton, large records, bursts, hot keys, schema versions, transactions, corrections, deletes/tombstones, duplicates/reorder/late inputs, gaps, backpressure, full buffers, source/sink outage, timeout/unknown effects, crash before/after checkpoint, stale worker, checkpoint corruption, restore, replay, rescale, retention boundary, and privacy deletion.

Use model/property testing for fold equivalence: incremental materialization at cut $c$ equals batch/reference evaluation of the same prefix; splitting a prefix and checkpointing between pieces preserves result; replaying under same semantics preserves output; changed semantics create a new generation.

Load/soak tests measure sustainable capacity, tail latency, state growth, garbage collection, checkpoint behavior, retry amplification, retention margin, and cost. Include failure/recovery catch-up, not just steady input.

Shadow new consumers from exact cuts, suppress external effects, compare materializations, and verify reset/replay. Canary by stable order domain/tenant when results remain separable. Keep old state/checkpoints compatible through rollback window.

The following finite model demonstrates cut-relative changelog materialization and burst backlog under fixed service capacity. It does not prove ordering, delivery, durability, event-time completeness, long-run stability, state bounds, or sink correctness.

<!-- bijux-verify: {"id":"stream-prefix-and-backlog","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"record_count=6\nprefix_cut_3=((\u0027A\u0027, 3), (\u0027B\u0027, 4))\nprefix_cut_6=((\u0027A\u0027, 6), (\u0027B\u0027, 3), (\u0027C\u0027, 2))\nprefix_total_cut_3=7\nprefix_total_cut_6=11\narrival_counts=(3, 5, 2, 6)\nservice_capacity_per_interval=4\nbacklog_trajectory=(0, 0, 1, 0, 2)\nmaximum_backlog=2\nrecords_accepted=16\nrecords_serviced=14\nrecords_pending=2\nstream_has_natural_end=False\nmaterialization_is_cut_relative=True\nretention_required_for_replay=True\n","stderr":""}} -->
```python
records = (
    (1, "A", 5),
    (2, "B", 4),
    (3, "A", -2),
    (4, "A", 3),
    (5, "B", -1),
    (6, "C", 2),
)


def materialize(prefix):
    state = {}
    for position, key, delta in records:
        if position > prefix:
            break
        state[key] = state.get(key, 0) + delta
    return tuple(sorted(state.items()))


cut_3 = materialize(3)
cut_6 = materialize(6)

arrivals = (3, 5, 2, 6)
capacity = 4
backlog = 0
trajectory = [backlog]
serviced = 0
for count in arrivals:
    available = backlog + count
    completed = min(available, capacity)
    serviced += completed
    backlog = available - completed
    trajectory.append(backlog)

print(f"record_count={len(records)}")
print(f"prefix_cut_3={cut_3}")
print(f"prefix_cut_6={cut_6}")
print(f"prefix_total_cut_3={sum(value for _key, value in cut_3)}")
print(f"prefix_total_cut_6={sum(value for _key, value in cut_6)}")
print(f"arrival_counts={arrivals}")
print(f"service_capacity_per_interval={capacity}")
print(f"backlog_trajectory={tuple(trajectory)}")
print(f"maximum_backlog={max(trajectory)}")
print(f"records_accepted={sum(arrivals)}")
print(f"records_serviced={serviced}")
print(f"records_pending={backlog}")
print("stream_has_natural_end=False")
print("materialization_is_cut_relative=True")
print("retention_required_for_replay=True")
```

## Definitions and Notation

Let:

- $S_j=(e_{j,1},e_{j,2},\ldots)$ be source/order-domain $j$ within source epoch $\epsilon_j$;
- $p_j(e)$ be an immutable coordinate valid only within $(S_j,\epsilon_j)$;
- $\mathbf{c}=(c_1,\ldots,c_m)$ be a cut vector over $m$ domains;
- $S_{\le\mathbf{c}}=\bigcup_j\{e\in S_j:p_j(e)\le c_j\}$ be the finite selected prefix;
- $f_v$ be transformation/fold semantics at version $v$;
- $M_v(\mathbf{c})$ be the materialization at the cut;
- $h_j(t)$ be source head and $a_j(t)$ accepted/recoverable progress;
- $L_j^p=h_j-a_j$ be coordinate lag where subtraction is defined;
- $B_i(t)$ be backlog at stage $i$;
- $\lambda_i$ and $\mu_i$ be effective offered-arrival and service rates;
- $Q_i$ be total bounded queue/buffer capacity and $X_i$ the overflow policy;
- $K$ be a recoverable checkpoint containing cut and operator state identity;
- $R_{data}$, $R_{schema}$, $R_{code}$, $R_{key}$, $R_{reference}$, $R_{state}$, and $R_{sink}$ be earliest replayable boundaries for required artifacts; and
- $R^*=\max(R_{data},R_{schema},R_{code},R_{key},R_{reference},R_{state},R_{sink})$ be the effective earliest replay boundary under a comparable coordinate/time mapping.

For deterministic prefix composition, if $\mathbf{a}\preceq\mathbf{b}$ and $\Delta(\mathbf{a},\mathbf{b})$ is the exact intervening ordered change set, then

$$
M_v(\mathbf{b})=
\operatorname{fold}_{f_v}(M_v(\mathbf{a}),\Delta(\mathbf{a},\mathbf{b})),
$$

provided schema, reference, conflict/order, and state semantics match. This is the incremental/batch equivalence obligation.

Backlog recurrence is

$$
B_i(t+1)=\min\left(Q_i,\max(0,B_i(t)+A_i(t)-C_i(t))\right),
$$

only if overflow $X_i$ accounts explicitly for work above $Q_i$. Omitting the overflow term silently loses obligations.

For sustained stationary periods, $\lambda_i<\mu_i$ is a basic stability requirement. Equality has no headroom for variance/failure, and finite samples cannot prove long-run stability. Catch-up requires recovery capacity strictly above continuing arrival.

## Mechanisms, Invariants, or Proof Structure

The foundation argument has nine links.

1. **Meaning and authority.** Every record is classified as event, observation, command, or state change and names its authoritative producer/source. Without this, replay can repeat commands or mistake storage mutation for business truth.
2. **Identity and order scope.** Source epoch, occurrence identity, payload/schema, transaction, and local coordinate are bound. Without this, duplicates/conflicts and ordering cannot be reasoned about.
3. **Finite cut.** Every result selects explicit coordinates/closure across all required domains. Without this, “current” and “complete” cannot be reproduced.
4. **Deterministic interpretation.** Versioned fold, schema, configuration, reference data, time/conflict rules, and base state map the prefix to a materialization. Without this, retained bytes do not determine meaning.
5. **Durable progress/effects.** Accepted checkpoint never exceeds recoverable state/output receipts and stale attempts are fenced. Without this, failure creates loss or duplicate effects.
6. **Bounded flow.** Every queue/state has capacity and overflow/backpressure; effective service plus headroom covers admitted load or degradation/loss is explicit. Without this, finite infrastructure eventually fails.
7. **Replay continuity.** Data/log, snapshot/checkpoint, schemas/codecs, keys, code/config/reference, and sink repair overlap for the promised horizon. Without this, reset cannot reconstruct state.
8. **Governed history.** Producer/consumer/tenant authorization, privacy, retention/deletion, encryption, and audit cover log and derived state. Without this, replayability becomes a security/compliance liability.
9. **Observed and exercised operation.** Lag/backlog/retention/state/checkpoint/sink metrics plus finite-prefix equivalence, load, failure, restore, and replay tests support the claims. Without this, contracts remain untested assumptions.

The conclusion is bounded: under complete source domains, intact positions, deterministic compatible interpretation, durable state/effects, sufficient capacity, and retained artifacts, $M_v(\mathbf{c})$ can be reproduced and operated within the declared envelope. It does not prove future arrival bounds, global event order, source truth, exactly-once effects, event-time completeness, or indefinite replay.

Key invariants include:

- equal occurrence identity binds equal canonical payload/schema/transaction context; conflict is quarantined;
- positions are compared only within the same source, epoch, and ordering domain;
- every materialization generation names a complete cut vector and transformation environment;
- folding the prefix directly equals folding a valid base checkpoint plus exact suffix under declared equivalence;
- accepted source progress is no later than durable checkpoint and sink-effect evidence;
- total buffered/in-flight/state/candidate work remains within declared capacity or overflow is counted/dispositioned;
- backlog/loss cannot be hidden by missing head metrics, consumer reset, compaction, or retention expiry;
- schema/code/key/reference retention reaches at least the oldest advertised replay boundary;
- corrections/deletes propagate through every materialized/consumer representation under policy; and
- replay writes an isolated new generation or idempotent same-intent effect, never blind duplication.

The executable model shows only two properties: six deltas fold to different cut-relative states, and a capacity-four server facing four finite arrival intervals leaves a burst backlog even when total arrival equals total nominal capacity. It deliberately does not extrapolate stability from that trace.

## Alternatives and Trade-Offs

**Event log versus current-state feed.** A history log supports replay/audit/new views but costs retention and exposes old data. Current-state updates reduce volume and speed bootstrap but lose intermediate facts. Keep the representation consumers and recovery actually require.

**Broker retention versus raw archive.** Broker replay is low-latency and coordinate-native; long retention costs capacity and remains tied to broker failure domains. Raw archival is cheaper/durable but slower and needs manifest/order/schema fidelity. Use explicit tiered continuity.

**Record-at-a-time versus micro-batch.** Per-record processing can minimize latency and react quickly but increases coordination/effect overhead. Micro-batches amortize IO/transactions and simplify vectorized computation but add interval latency and larger retry units. Semantics depend on cuts/effects, not marketing labels.

**Push versus pull.** Push minimizes polling but can overwhelm receivers and requires admission/loss policy. Pull naturally conveys demand but sources may continue accumulating retained data. Many brokers combine producer push with consumer pull.

**Durable buffer versus direct flow.** Durable queues decouple failures/rates and enable replay but add latency, cost, retention, and duplicate/order concerns. Direct streaming reduces copies but couples availability and recovery. Choose at failure boundaries.

**Backpressure versus load shedding.** Backpressure preserves data when upstream can slow and retention suffices. Shedding preserves system health when input cannot slow, but needs explicit priority/sampling/degradation semantics and loss accounting.

**Full history versus compaction.** Full logs support audit/reconstruction at storage cost. Key compaction accelerates current-state recovery but discards intermediate history and complicates deletes. Tier by use case and prove continuity.

**Changelog versus periodic snapshots.** Changelogs support incremental freshness and history; consumers bear fold/state complexity. Snapshots are simple to consume but stale/large and need manifest boundaries. Snapshot plus tail often supports bootstrap.

**Unified batch/stream model versus separate systems.** Unified APIs reduce duplicated logic and support equivalence; execution/state/operations still differ. Separate optimized systems can be simpler locally but risk semantic drift. Bind both to one contract and comparison cut.

**Exact versus approximate materialization.** Exact state can be unbounded/expensive; approximate sketches bound resources but introduce error/confidence/version concerns. Use only when consumer decisions tolerate quantified error.

**Indefinite state versus TTL.** Keeping state protects long-lived correlations but grows without bound and retains sensitive data. TTL bounds cost/privacy but changes semantics for returning keys/late events. Make expiry part of the product contract.

**Source-native schema versus normalized envelope.** Native data preserves fidelity and feature detail but burdens heterogeneous consumers. Normalization aids interoperability but can discard transaction/delete/order semantics. Preserve raw envelope and create governed derivatives.

**Low latency versus revision stability.** Early outputs improve responsiveness but revise as more data arrives. Delayed outputs improve completeness but miss decisions. Define provisional/final/retraction behavior per consumer.

**Exactly-once branding versus explicit boundaries.** A platform guarantee may cover internal state/checkpoint but not an external side effect. State source, state, sink, transaction, retry, and consumer boundaries separately; later modules refine them.

## Failure Modes and Misconceptions

- **“A stream is infinite.”** It may be unbounded without actually producing infinitely many records; each observed prefix is finite.
- **“A big file is unbounded.”** Known fixed membership is bounded even if huge; a watched directory can be unbounded.
- **“Streaming means millisecond latency.”** Processing style and latency objective are separate; buffering, windows, state, and sinks dominate.
- **“A log is globally ordered.”** Order normally exists only within named domains; timestamps do not create consensus order.
- **“Append-only means immutable forever.”** Retention, compaction, administration, corruption, keys, and disasters can remove accessibility.
- **“The log is truth.”** It is evidence emitted by authorized or faulty producers; domain authority and correction policy decide truth.
- **“Events never change.”** Prior events remain historical facts, but later correction/retraction can change materialized business state.
- **“A tombstone is just null.”** Its delete/compaction/absence semantics depend on the protocol and consumer.
- **“Current state can always regenerate history.”** Latest values omit intermediate events, prior permissions, and causal sequence.
- **“History can always regenerate current state.”** Only with complete compatible fold/schema/reference/key/base semantics.
- **“Consumer position proves output.”** Progress is safe only through durable recoverable state and effects.
- **“Zero offset lag means fresh data.”** Head metrics can be missing; source production can be late; sink/publication/consumer visibility can lag.
- **“Average arrival below capacity means safe.”** Bursts, skew, failures, checkpoints, and tail service require headroom/bounds.
- **“More buffering fixes overload.”** It increases time before overflow while latency and retention risk grow.
- **“Backpressure prevents producer overload everywhere.”** It crosses only boundaries that propagate demand; external sources may continue.
- **“Dropping is backpressure.”** Dropping is load shedding/loss and needs an explicit contract and accounting.
- **“More consumers always increase throughput.”** Ordering domains, hot keys, sink quota, and coordination can cap or reduce it.
- **“Compaction is backup.”** It may remove history and shares system failure/administrative domains unless independently protected.
- **“Seven-day retention means seven-day recovery.”** Size eviction, interpretation artifacts, restore time, and sink repair can shorten it.
- **“Checkpoint success proves recovery.”** Restore compatibility, source continuity, sink reconciliation, and materialization equality must be tested.
- **“Unified APIs make batch and streaming operationally identical.”** Semantics can align while lifecycle, state, latency, and failure differ.
- **“Exactly once applies end to end automatically.”** Every side-effect and consumer boundary needs a scoped protocol/evidence.

## Worked Examples

### Example 1

A 4 TB immutable file manifest contains a fixed object set. It is bounded although processing lasts hours. A directory receiving one 10 KB file each minute is unbounded unless a manifest/cut freezes membership. Choosing files “present when workers list” is neither a reproducible bounded dataset nor a sound stream cut.

### Example 2

Three source shards expose local heads `(120,80,200)`. A materialization records accepted cuts `(118,80,197)`. Lag is `(2,0,3)` within each shard; summing offsets is meaningless. Shard 3 contains one large transaction and dominates time lag. The product reports maximum/event-age/bytes alongside coordinates and retains the vector with its generation.

### Example 3

A customer changelog contains `insert(v1)`, `update(v2)`, and `delete`. The physical history has three immutable entries; the current relation has no row. A compacted representation may retain a tombstone temporarily. An audit consumer needs all three, while a cache bootstrap needs deletion state. Retention policies differ.

### Example 4

A database snapshot is taken at source boundary `b`, while logical decoding begins from the exact exported cut. New consumer state loads the snapshot, validates it, then applies changes strictly after `b`. Starting from a wall-clock approximate time risks a gap or overlap. Overlap can be tolerable only with stable identity/idempotent fold; gaps are not.

### Example 5

A metrics source produces bursts of 10,000 records/s while the processor sustains 6,000. A memory queue absorbs one burst, but repeated bursts increase backlog and GC until crash. The design adds bounded admission, durable buffer, tenant quotas, batch aggregation permitted by the product, and capacity headroom; overflow is counted and alerted rather than silently lost.

### Example 6

A Reactive Streams subscriber requests 100 elements and pauses when its sink slows. Its connector had already prefetched 10,000, and the upstream devices continue emitting. Local nonblocking backpressure prevents one library queue from growing but not broker backlog or device production. End-to-end design sizes prefetch/retention and defines device admission/shedding.

### Example 7

A global count over an unbounded stream changes with every record and never has a natural final result. The product instead emits versioned current counts at explicit cuts and periodic immutable snapshots. Consumers requiring daily stable values use event-time windows and later revision rules, which DE-057 and DE-058 develop.

### Example 8

A processor checkpoints source cut 500 and keyed state but calls an email API before the checkpoint. It crashes after the API commits. Replaying from 500 can send again unless the email uses a stable effect identity and receipt/reconciliation. Internal state recovery alone does not give an end-to-end exactly-once effect.

### Example 9

Broker retention is 72 hours, schema versions are retained a year, but an encryption key version is destroyed after 48 hours. Effective replay of older ciphertext is 48 hours, not 72. The team aligns key retention with privacy/recovery policy and tests archive restore; it never retains keys indefinitely by accident.

### Example 10

A new aggregation implementation shadows the accepted consumer from cut 1,000 through 2,000 using the same schema/reference/config. It publishes only to an isolated candidate and compares keyed results with a bounded batch reference over that exact prefix. Equality supports incremental equivalence for this case; load, disorder, failure, and future inputs need separate evidence.

## Cross-Program Connections

Distributed systems supplies partial order, replicated logs, consensus, failure detectors, delivery semantics, leases/fencing, idempotency, backpressure, and distributed snapshots. Streaming systems compose these; they do not repeal network, clock, or failure uncertainty.

Database systems supplies write-ahead/change logs, transactions, MVCC snapshots, materialized views, incremental view maintenance, relational changelogs, keys, indexes, and recovery. A stream-table model makes these connections explicit.

Operating systems and networking contribute pipes, sockets, buffers, flow/congestion control, bounded queues, scheduling, memory pressure, and zero-copy/serialization tradeoffs. Application backpressure is one layer in a longer resource path.

Queueing theory contributes arrival/service processes, utilization, Little's Law, waiting-time distributions, bursts, stability, and priority/fairness. Production workloads violate simple stationary assumptions, so measure and simulate tails/failures.

API and service engineering contributes event/command contracts, versioning, idempotency keys, conditional operations, rate limits, authentication/authorization, pagination/cursors, webhooks, and error/retry semantics.

Security engineering contributes producer authenticity, consumer least privilege, tenant isolation, integrity, encryption/key lifecycle, audit, supply-chain trust, and denial-of-service resistance. Long-retained event history increases both recovery power and attack value.

Privacy engineering contributes minimization, purpose limitation, retention/deletion, historical access, derived-data purge, pseudonymization limits, and data-subject/regulatory workflows. Immutability claims must coexist with lawful governance.

Formal methods contributes sequence/prefix/fold algebra, state machines, invariants, determinism, refinement, and model/property testing. Finite traces can falsify designs; proof assumptions must name source/order/effect completeness.

Site reliability engineering contributes SLIs/SLOs, backlog/lag/retention margin, saturation, overload control, capacity, incident response, restore/replay drills, and safe change. Continuous systems require continuous evidence of stability.

## References

1. Apache Beam. [Basics of the Beam model](https://beam.apache.org/documentation/basics/). Accessed 2026-09-03. Primary documentation for unified batch/stream processing and bounded/unbounded collections.
2. Apache Beam. [Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/). Accessed 2026-09-03. Primary documentation for immutable distributed collections, boundedness, timestamps, windows, and state.
3. Apache Kafka. [Introduction](https://kafka.apache.org/intro). Accessed 2026-09-03. Primary project introduction to event streaming, durable topic storage, processing, and routing.
4. Apache Kafka. [Documentation: Design](https://kafka.apache.org/documentation/#design). Accessed 2026-09-03. Primary design documentation for Kafka's partitioned log and storage/processing model.
5. Apache Flink. [Apache Flink Documentation](https://nightlies.apache.org/flink/flink-docs-stable/). Accessed 2026-09-03. Primary project documentation describing stateful computation over bounded and unbounded streams.
6. Apache Flink. [Table API and SQL: Streaming Concepts](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/concepts/overview/). Accessed 2026-09-03. Primary documentation for unified relational batch/stream semantics and streaming state.
7. Reactive Streams. [Reactive Streams Specification for the JVM](https://github.com/reactive-streams/reactive-streams-jvm). Accessed 2026-09-03. Primary specification for asynchronous stream exchange with nonblocking backpressure.
8. Akidau, Tyler, et al. [The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf). *Proceedings of the VLDB Endowment* 8(12), 2015. Primary research paper on event-time processing and result-emission/revision tradeoffs.
9. PostgreSQL Global Development Group. [Logical Decoding](https://www.postgresql.org/docs/current/logicaldecoding.html). Accessed 2026-09-03. Primary documentation for streaming database modifications through logical decoding and replication slots.
10. Debezium. [Architecture](https://debezium.io/documentation/reference/stable/architecture.html). Accessed 2026-09-03. Primary project documentation for capturing database changes and routing change-event streams.
11. Cloud Native Computing Foundation. [CloudEvents Specification 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md). Accessed 2026-09-03. Versioned primary specification for interoperable event identity, source, type, schema, time, and data context.

## Exercises

### Exercise 1

Classify each source as bounded or unbounded under a precise contract: a 2 TB file; a table queried without a snapshot; a Kafka topic through a recorded cut vector; an object prefix watched continuously; and a database snapshot plus CDC tail. Explain why storage size and API style are insufficient.

### Exercise 2

A delta log contains `(1,A,+10)`, `(2,B,+3)`, `(3,A,-4)`, `(4,B,+2)`, `(5,A,+1)`. Compute materializations at cuts 2 and 5. State every identity/semantic artifact required to reproduce cut 5 and how a later correction should be represented.

### Exercise 3

A source admits `(7,12,4,9,3)` MB each minute and a stage accepts at most 8 MB/minute. Starting at zero, compute backlog after every minute, total admitted/serviced/pending, and maximum backlog. Explain what the finite trace can and cannot establish about stability and retention.

### Exercise 4

After a six-hour outage, an input continues at 2,000 records/s. Recovery capacity is 5,000 records/s while new input continues. Estimate ideal catch-up time. Then identify at least five real constraints that can make the estimate unsafe and the evidence needed before relying on it.

### Exercise 5

A product claims seven-day replay because its broker retention is seven days. Schemas are retained 30 days, raw archive 90 days, checkpoint/state serializers four days, encryption keys five days, reference snapshots three days, and the sink can safely repair six days. Determine the effective replay horizon and propose a durable design for a required 14-day recovery objective.

## Answers to the Exercises

### Answer 1

The 2 TB file is bounded only when its immutable identity/member bytes are fixed; size does not matter. A mutable table query without snapshot/cut is not a reproducible bounded population and behaves as a changing source during processing. A Kafka topic restricted to exact source epochs and a recorded per-partition cut vector is bounded for that read, although the topic continues. A continuously watched object prefix is unbounded because new members may arrive without a final manifest. A database snapshot alone is bounded; snapshot plus an open-ended CDC tail is unbounded, while snapshot plus a recorded terminal tail cut is bounded. APIs and storage media can serve either model; membership closure decides boundedness.

### Answer 2

At cut 2, materialization is `A=10, B=3`. At cut 5, A is `10-4+1=7` and B is `3+2=5`. Reproduction requires source/epoch and ordering domain, positions 1–5 with no gaps, occurrence/payload/schema/transaction identity, retained bytes/envelopes, fold/code/config/runtime version, initial/base state, key and delta semantics, reference data, encryption keys/codecs, and output equivalence/publication identity. A later correction appends a new authorized event with its own identity and causation/supersession reference—such as a compensating delta—rather than rewriting position 3. It yields a new materialization generation at a later cut.

### Answer 3

Using $B_{t+1}=\max(0,B_t+A_t-8)$, backlog begins 0 and becomes `0,4,0,1,0` after the five intervals. Total admitted is `7+12+4+9+3=35` MB. Service is 7, 8, 8, 8, and 4 MB, totaling 35; pending is zero; maximum backlog is 4 MB. This finite trace shows how bursts wait and that this specific workload clears. It does not prove long-run stability, tail latency, record/state cost, arrival stationarity, failure recovery, or sufficient retention. Average arrival is 7 MB/minute below nominal 8, but headroom, variance, checkpoints, sink limits, and future bursts require measurement.

### Answer 4

The outage accumulates $2{,}000\times6\times3{,}600=43{,}200{,}000$ records. Net catch-up capacity is $5{,}000-2{,}000=3{,}000$ records/s, so ideal catch-up takes 14,400 seconds or four hours. This assumes immediate constant recovery, uniform records, no retries, no checkpoints, and unconstrained sink. Real constraints include bytes/large transactions, hot-key/skew/state, decode/transform cost, broker/network read limits, sink QPS/transactions/logs, checkpoint/GC pauses, retry/duplicate work, live priority/fairness, storage tier restore, quotas/cost, and changing input. Load-test representative backlog plus continuing traffic; measure all resource saturation, accepted not merely fetched throughput, checkpoint/sink commits, retention margin, and consumer freshness before relying on four hours.

### Answer 5

The effective end-to-end replay horizon is the minimum available duration across required artifacts, which is three days because historical reference snapshots expire first; state serializers allow four and keys five, so the broker's seven-day setting does not establish seven days. To reach 14 days, retain or reconstruct every required component for more than 14 days plus restore/catch-up margin: log or authoritative raw archive with positions/manifests, bootstrap snapshots/checkpoints, all writer/reader schemas/codecs and state serializers/migrations, decryption keys under approved security/privacy policy, immutable code/config/runtime/dependencies, reference-data generations, and sink idempotency/repair receipts. Verify time- and size-based eviction, compaction/deletion, tenant access, and output repair. Exercise isolated replay from the oldest promised boundary through current cut at representative capacity, compare materialization, and conditionally publish/repair consumers before advertising the horizon.
