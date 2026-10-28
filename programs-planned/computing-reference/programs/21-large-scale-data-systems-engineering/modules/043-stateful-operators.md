---
module_id: LSDS-043
program: Large-Scale Data Systems Engineering
level: 1
module_number: 43
title: Stateful Operators
status: complete
last_verified: 2026-09-04
---

# Stateful Operators

## One-Page Review

### Governing question

How can a distributed stream operator remember information across records while keeping state correctly partitioned, bounded, recoverable, rescalable, migratable, observable, and consistent with input positions, timers, outputs, and deletion policy?

### Essential definitions

- A **stateful operator** produces behavior from the current input plus retained state; a stateless operator depends only on the current record and immutable configuration.
- **keyed state** is logically scoped by operator, state name, current key, and sometimes window/namespace; it is co-partitioned with keyed input.
- **operator state** belongs to a parallel operator instance rather than one key and needs explicit redistribution semantics on rescale.
- **broadcast/replicated state** copies a control dataset to many instances; deterministic update order/version is required for convergence.
- A **state descriptor** fixes durable name, type/schema, serializer, defaults, TTL, and compatibility identity.
- A **working state backend** serves live reads/writes in heap, embedded storage, or another engine-managed form; **checkpoint storage** retains durable snapshots for recovery.
- A **changelog** records state mutations so a local store can be rebuilt or incremental snapshots can reference changes.
- A **timer** is durable deferred operator work scoped to key/namespace and time domain; it is part of state, not a reliable wall-clock callback by itself.
- **time-to-live (TTL)** makes state logically expired under specified clock, update/access, visibility, and cleanup rules; physical reclamation can lag logical expiry.
- A **key group** or virtual shard is a stable state-transfer unit that maps many keys to parallel instances and permits rescaling up to a configured maximum.

### Central model, mechanism, or theorem

For key $k$, ordered input $e_i$, state schema/code version $v$, and current state $s_{k,i}$, define a deterministic transition

$$T_v(s_{k,i},e_i)=(s_{k,i+1},O_i,\Theta_i),$$

where $O_i$ is an ordered or explicitly unordered output collection and $\Theta_i$ is the timer-registration/cancellation delta. Initialization, missing/null state, duplicate input, late input, error, and deletion semantics are part of $T_v$. State for different keys can execute independently only when no hidden shared mutable state or cross-key ordering contract exists.

A consistent recovery point pairs source next positions with every operator state/timer snapshot produced from exactly the admitted prefix. Restoring state without matching positions duplicates updates; restoring positions without state skips them. External effects require a compatible transaction, idempotency, deduplication, or fencing protocol.

Capacity counts more than logical values. For live keys $K$, state variables $j$, encoded state $b_{k,j}$, and backend/index/timer/TTL overhead $h_{k,j}$, working storage is approximately $\sum_{k,j}(b_{k,j}+h_{k,j})$ plus caches, memtables, logs, compaction, snapshots, and headroom. Key count, value-size tails, timers, churn, write amplification, snapshot bytes, and restore rate determine operability.

### Critical invariants

- Operator UID, state name, key/namespace encoding, serializer/schema, code version, and time semantics are durable identity.
- All records for one keyed state domain route by the same stable key partitioning; the current task accesses only its owned keys.
- Each admitted input affects state/timers/outputs according to one declared transition and delivery contract; retries cannot silently double-apply.
- Checkpoints pair source positions with state and timer images at one consistent cut; incomplete snapshots never become recovery truth.
- Working state, durable snapshot, changelog, cache, and external database roles are distinguished and integrity-checked.
- TTL specifies clock, refresh policy, read visibility, cleanup mode, migration behavior, and business/legal consequence.
- Rescaling assigns every state shard/key group to exactly one new owner and transfers no state outside allowed tenant/region boundaries.
- Schema migration reads all retained old formats or performs a verified rewrite; key schema/routing changes use an explicit state migration.
- State, timers, buffers, snapshots, changelogs, compaction, restore traffic, and cleanup work are bounded/admitted.
- Sensitive state follows least privilege, encryption, audit, retention, deletion, backup, and legal-hold requirements.

### Common failures

Common failures include hiding mutable globals inside a “stateless” function; querying another key from ordinary keyed state; using a remote database without defining consistency; retaining every event instead of sufficient state; treating heap state as durable; restoring state and offsets from different checkpoints; emitting side effects before recoverable state without idempotency; using wall-clock time as deterministic event logic; assuming timer firing is exactly once; using TTL solely to cure memory pressure; assuming expired bytes are immediately deleted; refreshing TTL on reads unintentionally; evolving a serializer without old-byte tests; renaming state/operator IDs and losing restore mapping; changing key encoding in place; rescaling beyond stable virtual-shard limits; broadcasting nondeterministic updates; and exposing raw keys or state values in metrics, logs, or query endpoints.

### Compact example

A per-account balance operator stores `(balance,last_event_time)` and retains a separate event-ID dedup set for the required replay horizon. Events `(+5 at 0)`, `(-2 at 2)`, a duplicate of the second, and another account `(+7 at 3)` produce two live states. With processing-time TTL 5 and strict expiry when `now-last_update>5`, arrival at time 9 expires both old balances before applying `(+1)` for the first account. Four unique events are accepted, one retry is rejected, and final balance is 1—not 4—because TTL defines semantic reset. If that reset is not business-correct, TTL is not an acceptable capacity remedy.

### Connections

[LSDS-041](041-logs-as-distributed-input.md) and [LSDS-042](042-partitioned-consumption.md) define source/checkpoint and ownership identity. [LSDS-044](../ROADMAP.md) through [LSDS-046](../ROADMAP.md) develop event time, watermarks, windows, and triggers; [LSDS-047](../ROADMAP.md) and [LSDS-048](../ROADMAP.md) develop consistent barriers/snapshots; [LSDS-050](../ROADMAP.md) completes effect-safe replay.

## Governing Question

Many streaming questions cannot be answered from one record. Deduplication asks what has been seen. Fraud detection remembers a sequence. A join buffers unmatched rows. A window keeps an aggregate and timers. A model update depends on prior parameters. This retained information turns a dataflow node into a long-lived database partition.

State adds locality and failure obligations. Records for a key must reach the state owner. The working copy must fit or spill efficiently. A durable copy must survive worker loss. Checkpoints must align it with source positions. Reassignment must restore or transfer it before processing. Rescaling must repartition it without omission or duplication.

State also ages. Schemas, serializers, code, partitioning, retention rules, and privacy policy change while applications run. A field rename that is harmless in stateless code can make years of checkpoint bytes unreadable. A key change can merge or split state domains. TTL may delete a customer's history and change outputs.

The governing question is how to specify the transition and state lifecycle as durable contracts, choose backend and cleanup mechanisms from workload evidence, and preserve consistent behavior through retries, timers, snapshots, rescaling, upgrades, and deletion.

## Why This Matters

Stateful operators make low-latency continuous computation possible. Keeping per-key state local avoids a remote database round trip for every record. Incremental updates avoid rescanning history. Timers schedule inactivity detection and deferred output. Checkpoints and changelogs make a failed worker replaceable.

The same advantages create large failure surfaces. A million keys can become a billion. A few hot keys can hold giant maps or queues. Embedded LSM compaction can saturate disk. Checkpoint duration can exceed the interval and never converge. Restore can take longer than retention headroom. State skew can defeat otherwise balanced source partitions.

Correctness bugs are durable. A non-idempotent transition applied twice remains wrong after every future checkpoint. An incompatible serializer can strand all state during deployment. Nondeterministic iteration can change output or snapshot bytes. A timer restored twice can duplicate an external effect unless output is protected.

State often concentrates sensitive facts: profiles, sessions, balances, location sequences, model features, and deletion markers. Local disks, incremental snapshot objects, changelogs, standby replicas, debug queries, and metrics all become governed data stores. Fast cleanup must not violate recovery; durable recovery must not violate deletion.

## Prerequisites and Retrieval

Retrieve partitioning, serialization, failure assumptions, and scale accounting from [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve storage replication, integrity, metadata, and lifecycle from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review combiners/aggregation algebra in [LSDS-023](023-partitioners-and-combiners.md) and [LSDS-038](038-distributed-aggregation.md), skew in [LSDS-039](039-skewed-keys-and-heavy-hitters.md), log snapshots in [LSDS-041](041-logs-as-distributed-input.md), and assignment frontiers in [LSDS-042](042-partitioned-consumption.md). You should understand deterministic state machines, key-value/LSM storage, serializers, checkpoints, changelogs, transactions, idempotency, timers, TTL, hashing, and capacity distributions.

## Learning Objectives

After this module, you should be able to:

1. distinguish stateless, keyed, operator, broadcast, window, timer, and external state;
2. specify a versioned per-key transition with initialization, ordering, duplicate, error, output, timer, and deletion behavior;
3. select value/list/map/set/combining state according to access and growth patterns;
4. separate live backend, checkpoint storage, changelog, cache, standby, and external source-of-truth roles;
5. estimate working-set, write, snapshot, changelog, restore, and cleanup cost using tail distributions;
6. define TTL as a semantic clock/visibility/refresh/cleanup policy and test its boundary behavior;
7. coordinate source positions, state, timers, and output effects for the promised recovery semantics;
8. rescale using stable key groups or explicit operator-state redistribution without losing ownership;
9. migrate state schema, serializer, code, key routing, and operator identity through rehearsed restore; and
10. observe, secure, retain, delete, and audit state across local and durable copies.

## Core Exposition

### Identify what must be remembered

Begin with the minimal information future records need. A running count needs one integer, not all events. A mean needs sum and count. Deduplication needs identifiers for a bounded horizon or a probabilistic structure with declared error. An exact temporal join may need every unmatched row until a time bound proves it can be discarded.

Write the business invariant before choosing an API. Define key and namespace, initial state, transition order, outputs, duplicates, corrections, late events, errors, and deletion. Identify whether state is authoritative or a reconstructable materialization.

Hidden process memory—module globals, static caches, library singletons—is state too. If the engine does not manage it, checkpoint/rescale semantics exclude it. Make it immutable configuration, managed state, or an explicitly reconstructable cache.

### Specify a deterministic transition

For each key, treat processing as a versioned state machine. $T_v$ consumes current state and one ordered record (or a defined batch) and returns new state, outputs, and timer changes. Avoid reading wall clock, random values, remote mutable data, or nondeterministic collection order unless these inputs/results are captured.

Batch invocation order may be unspecified by some APIs. If results depend on order, request/provide a deterministic order with tie-break identity, or make the transition commutative. Floating-point accumulation can vary with reassociation; state the tolerance or stronger summation method.

Failures must be explicit: reject and stop, quarantine without state change, retry idempotently, or apply compensating logic. Catch-and-drop is a semantic policy, not generic resilience.

### Choose the correct state scope

Keyed state is partitioned by the current input key; runtime APIs commonly prevent arbitrary other-key access. This preserves local consistency and enables redistribution. Namespaces may further scope state by window or timer domain.

Operator state belongs to a subtask. On rescale, list-like state might redistribute round-robin, union state might copy the full collection to every subtask, and custom state needs a declared mapping. It is suitable for source shard positions or local operator metadata, not accidental per-key maps.

Broadcast state replicates control rules/configuration. All replicas must apply a deterministic versioned update stream or use immutable snapshots. Large or high-churn broadcasts multiply network/memory/checkpoint cost.

### Match state type to access pattern

Value state supports one typed scalar/object per key. Map state provides keyed subentries and point updates. List/bag state supports append/iteration but can grow without random deletion. Set state expresses membership. Combining state stores a mergeable accumulator compactly.

The logical API does not reveal physical cost. Reading a list may deserialize all entries; iterating a map may scan storage; `contains` may be indexed. Measure backend-specific access, serialization, and write amplification.

Avoid nested unbounded collections in one value because every update may rewrite the whole object and one hot key becomes indivisible. Prefer granular map/list structures or externalized data only when consistency is specified.

### Separate working state from durable recovery

Working state is local to the current operator owner for low-latency access. Heap backends hold objects in managed process memory; embedded disk/LSM backends keep indexed data locally with caches and memtables. Neither is durable merely because bytes are on a worker disk.

Checkpoint storage holds persistent snapshots in a fault-independent store. A changelog can continuously record updates and reconstruct a local store. Standby replicas pre-restore state to reduce failover. These mechanisms have different freshness, durability, cost, and deletion behavior.

Document the source of truth. If input plus code can reconstruct state, the checkpoint/changelog bounds recovery time. If state contains external decisions not reproducible from input, its durability and audit requirements are stronger.

### Account for state economics

Count active keys, entries per key, encoded key/value bytes, backend/index/allocator overhead, timers, TTL timestamps, caches, write-ahead logs, memtables, sorted levels, local checkpoints, remote snapshots, changelog replicas, and standby copies.

Measure distributions: maximum and p95/p99 value size, updates per key, read/write latency, bytes per update, compaction debt, checkpoint delta/full bytes, duration, upload throughput, restore rate, and cleanup backlog. Logical state size alone misses physical amplification.

If 20 million keys each need a 40-byte encoded value plus 56 bytes overhead, base working set is 1.92 GB before indexes/caches/snapshots. A ten-entry map per key may multiply entry overhead. Capacity includes failure/rebuild headroom.

### Understand backend trade-offs

Heap state offers low access latency and simple object access but competes with application memory and garbage collection; snapshots may serialize large graphs. Embedded LSM state supports larger-than-heap working sets and incremental snapshots but adds serialization, block cache, write amplification, compaction, local disk, and native memory.

Remote state services centralize durability and can allow stateless compute, but every access adds network latency, rate limits, failure domains, transactions, and cost. Caching creates coherence and recovery questions. A remote lookup is not automatically engine-managed state.

Choose with representative read/write mix, key/value tails, locality, checkpoint/restore SLOs, rescale frequency, disk type, CPU, and operational expertise. Benchmark failure recovery, not only steady-state throughput.

### Couple state with input progress

A checkpoint must capture the state after exactly the input prefix represented by saved source positions. Multi-input operators need a consistent cut so records before and after the checkpoint are not mixed incorrectly. LSDS-047 explains barriers.

On recovery, restore both positions and state/timers from the same completed checkpoint. Discard partial/newer local mutations or replay them through a proven changelog protocol. Never combine the newest offset file with an older state image.

At-least-once recovery may replay records into state; the runtime must roll state back before replay or transitions must tolerate duplicates. Exactly-once state is not exactly-once external effects; sinks need coordination.

### Treat timers as managed state

Timer registration includes key, namespace, time domain, timestamp, identifier, and callback/code version. Registration/cancellation must be checkpointed with state. On restore, overdue timers may fire promptly and timing can bunch.

Processing-time timers depend on wall clock and scheduling, so exact firing instant is not deterministic. Event-time timers depend on watermark progress and are developed later. Neither should directly perform an unprotected non-idempotent effect.

Deduplicate timer intent or make callbacks idempotent. Bound timers per key and globally. Replacing a timer needs defined identity; repeated registration may overwrite or duplicate depending on API.

### Define TTL semantically

TTL must state clock (processing/event/ingestion), duration, strict boundary, refresh on create/write/read, visibility of expired values, cleanup mechanism, and behavior across restore/migration. “One day” is incomplete.

Logical expiry can hide a value before physical cleanup removes bytes. Lazy cleanup on access leaves cold expired entries; background/compaction cleanup consumes resources. Snapshots/changelogs/backups may retain old bytes longer. TTL is not proof of secure deletion.

Expiry changes results. Dedup state expiring too early permits duplicate effects. Join state expiring too early loses matches. Session state expiring can reset behavior. Derive TTL from event lateness, replay horizon, outage, correction, business/legal rules, and margin—not memory pressure alone.

### Bound unbounded state explicitly

Every state collection needs an admission and eviction rule: time, count, bytes, watermark, completion, reference release, approximation, or explicit deletion. Global/windowless state without TTL can grow forever as new keys arrive.

Use sufficient aggregates instead of raw history. Spill-aware maps instead of giant values. Approximate membership/sketches can bound memory only with declared error and privacy implications. Fail or shed through explicit policy when hard caps are reached; silent eviction corrupts results.

Track state growth derivative and projected exhaustion. Rate limiting input may slow growth but cannot fix a state model whose live set monotonically increases.

### Handle hot keys and state skew

Keyed locality makes one key single-owner by default. A hot key can dominate CPU, state, timers, and checkpoint bytes even when partitions are balanced by record count. A giant nested state value may be impossible to split transparently.

Decomposable aggregates can shard a logical key and merge partial states. Sequence detectors, ordered sessions, and arbitrary keyed functions may require one owner. Alternatives include hierarchical state, larger resources, external partitionable stores, bounded approximation, or product limits.

Measure per-key/state-namespace tails carefully without exposing raw sensitive keys. Salted/sharded state needs semantic proof, deterministic routing, rescale handling, and exactly-one output ownership.

### Rescale through stable transfer units

Virtual key groups decouple logical key hash from current parallelism. Each key group maps to exactly one operator instance, and rescaling reassigns groups rather than rehashing durable keys arbitrarily. A configured maximum bounds future parallelism/granularity.

Snapshot state plus key-group identity, then assign every group exactly once to new owners. Restore completes before effects. Transfer may use shared remote snapshot handles rather than copying through a coordinator. Verify checksums, tenant/region eligibility, and source generation.

Operator state needs its own redistribution rule. Broadcast/union state can multiply on scale-out. Rescale cost includes snapshot, network/storage reads, backend ingest/compaction, caches, and lost processing capacity.

### Migrate schemas, serializers, and code

State identity includes durable operator UID, state name, type/schema, serializer and compatibility snapshot, key schema, namespace, TTL metadata, and code semantics. Renaming or deleting descriptors can orphan state.

Test new serializers against real old bytes and downgrade paths. Compatible field addition/removal still needs default/null/business semantics. Some engines support only selected types; key schema migration is especially dangerous because binary identity and routing can change.

For incompatible change, use an offline/online state processor, dual-read/write versioned state, export-transform-import, or replay from source into a new job. Pin a cutoff, validate counts/invariants, preserve rollback, and retire old artifacts only after acceptance.

### Manage broadcast and shared control state

Rules, models, or configuration often arrive on a control stream and are broadcast to keyed workers. Apply updates by monotone version with deterministic conflict/tie rules. A worker must know which rule version produced each output when audit matters.

Broadcast snapshots can be large and replicated per task. Incremental update loss or reordering causes divergent results. Coordinate control-data checkpoints with main input or define temporal join semantics.

Do not hide a mutable network client/cache as shared operator state. Its failures and versions must be explicit, and authorization cannot rely on eventually refreshed local data when stale denial would be unsafe.

### Make external effects explicit

Updating managed state and emitting a dataflow record can often participate in the engine's checkpoint/replay protocol. Calling a database, payment API, email service, or file sink inside a transition does not automatically participate.

Use transactional sinks, idempotency keys based on stable input/output identity, dedup tables retained for replay horizon, or an outbox committed with state. Fence obsolete operator attempts/generations. Define response ambiguity and retry.

Queries against live state also need consistency. Debug/queryable-state endpoints may show one task's current uncheckpointed view, a completed snapshot, or a remote materialization. Label freshness and do not use an observational interface as an authoritative transaction endpoint.

### Observe state without leaking it

Measure keys/entries/bytes by state and operator, value-size tails, access latency, cache hit, backend memory/disk, WAL/compaction, timer count/age, TTL expired/cleanup, checkpoint full/delta bytes/duration/failures, restore bytes/rate/time, and rescale movement.

Correlate with input rates, backpressure, source lag, hot partitions/keys, GC/native memory, disk utilization, snapshot store limits, changelog lag, and sink latency. Stable total bytes can hide runaway one-key state or compaction debt.

Expose state contents only through authorized, audited, rate-limited tools with redaction. Raw keys and rare-state sizes can identify people. High-cardinality labels can overload telemetry and create another retention surface.

### Validate lifecycle and adversarial behavior

Model-test $T_v$ for empty/missing/null state, duplicates, reordering, retries, errors, delete, late records, timer races, TTL boundary, and nondeterministic iteration. Compare replay/repartition/batch sizes against a reference state machine.

Inject worker/coordinator/storage loss during update/checkpoint/restore/rescale/migration/compaction; corrupt snapshots/changelogs; expire credentials; fill disk/memory; delay timers; create hot/giant keys; and fail external effects ambiguously.

Restore every supported historical state version into the new binary before rollout. Verify source/state/timer cut, output multiset/order, exactly-one state ownership, resource bounds, privacy deletion, legal holds, and rollback.

## Definitions and Notation

- $s_{k,i}$: managed state for key $k$ before its $i$th admitted transition.
- $e_i$: input record/batch with declared order and identity.
- $T_v$: transition under code/schema version $v$.
- $O_i$: output records/effects intent returned by the transition.
- $\Theta_i$: timer registration/cancellation delta.
- $K$: current set of live state keys; $j$ indexes named state variables/entries.
- $b_{k,j},h_{k,j}$: encoded content and physical metadata/backend overhead bytes.
- **working backend**: owner-local live state service; distinct from durable checkpoint storage.
- **key group**: stable virtual partition used to assign/transfer keyed state.
- **logical expiry**: state becomes invisible under TTL; physical cleanup may occur later.
- **consistent cut**: paired source positions, operator states, timers, and protocol metadata describing one admitted input prefix.

## Mechanisms, Invariants, or Proof Structure

1. Freeze operator/state/key/namespace identity, transition version, ordering, duplicate, error, output, timer, and deletion semantics.
2. Route each key to one current state owner and reject hidden/unmanaged mutable state.
3. Choose minimal state types and backend from access patterns, physical amplification, snapshot, restore, and failure evidence.
4. Admit every state/timer collection with explicit count/byte/time/completion bounds and hot-key handling.
5. Pair source positions, state, timers, and emitted data at a completed consistent checkpoint cut.
6. Protect external effects with transaction, idempotency/deduplication, outbox, and generation fencing.
7. Define TTL clock/refresh/visibility/cleanup/migration and distinguish logical expiry from deletion.
8. Rescale each key group/operator-state item to exactly one eligible owner; restore before processing/effects.
9. Rehearse schema/serializer/code/key migrations and rollback using real old bytes and invariant checks.
10. Observe, fault-test, retain, and delete all working/snapshot/changelog/standby/cache/diagnostic copies under policy.

Determinism means replaying the same qualified input order from the same compatible state yields semantically equivalent state, timers, and outputs. It does not require byte-identical snapshots when serialization/compaction permits representation differences, but equivalence and numerical tolerances must be defined.

Consistency follows when a completed checkpoint names exactly one state/timer image and source-position vector for the same cut. Recovery discards later uncommitted mutations and replays from those positions. External effects remain outside this proof unless incorporated by a compatible protocol.

## Alternatives and Trade-Offs

**Recompute from retained input** minimizes durable state machinery but can make recovery too slow. **Snapshots** bound replay while adding storage/I/O. **Changelogs** support incremental recovery but add continuous writes and compaction. **Standbys** reduce failover latency at replicated compute/storage cost.

**Heap state** offers fast object access with GC/snapshot pressure. **Embedded disk/LSM state** scales working sets with serialization/compaction/native-memory cost. **Remote state** centralizes durability and elasticity while adding network/transaction/service dependency.

**Fine-grained map/list state** supports incremental operations but pays per-entry overhead. **One serialized value** is compact for small objects but rewrites/deserializes the whole value. **Combining state** is efficient only when sufficient algebra exists.

**Processing-time TTL** is operationally simple but replay timing can differ. **Event-time TTL** follows data progress but depends on watermarks/late-data contract. **Access-refresh TTL** preserves popular data but makes reads mutate lifecycle.

**Eager migration** rewrites cost upfront and validates all bytes. **Lazy migration** spreads cost but leaves mixed formats and runtime surprises. **Replay into a new job** gives isolation when input retention and deterministic logic suffice.

**More key groups** improve future rescale granularity but increase metadata. **Fewer groups** reduce overhead while limiting placement. **State sharding** helps decomposable hot keys but complicates semantics and finalization.

## Failure Modes and Misconceptions

1. **“State is just a variable.”** Durable identity, ownership, snapshot, restore, and migration make it a database contract.
2. **“Local disk means durable.”** Worker loss can remove the working copy.
3. **“Checkpoint storage is the live backend.”** They serve different access and recovery roles.
4. **“Exactly-once state means exactly-once API calls.”** External effects need their own protocol.
5. **“Replay will repair any state.”** A nondeterministic or non-idempotent transition can reproduce corruption.
6. **“All state is per key.”** Operator and broadcast state redistribute differently.
7. **“Another key can be read locally.”** Keyed APIs intentionally scope access and placement.
8. **“List state is bounded because each item is small.”** Count can grow without limit.
9. **“TTL is only memory management.”** Expiry changes business results and dedup/join correctness.
10. **“Expired means erased.”** Physical copies can persist in backend levels, snapshots, logs, and backups.
11. **“Read-refresh TTL is harmless.”** Observation can extend retention and alter behavior.
12. **“Timers fire exactly once at their timestamp.”** Recovery and scheduling require idempotent semantics.
13. **“Schema-compatible records imply state compatibility.”** State serializers, keys, names, and code semantics differ.
14. **“Rename the state and restore.”** Durable mapping may be lost.
15. **“Changing key type is an ordinary migration.”** It can merge/split identity and routing.
16. **“Rescaling rehashes state safely.”** Stable key-group ownership and transfer proof are required.
17. **“Broadcast state converges eventually.”** Nondeterministic order can create permanent replica divergence.
18. **“Total state bytes prove health.”** hot-key tails, compaction debt, timers, and restore rate can dominate.

## Worked Examples

### Example 1

A running count keeps one integer per key. Storing all records instead changes state from $O(|K|)$ values to $O(N)$ history and adds no information required for future counts.

### Example 2

Twenty million keys with 40 encoded value bytes and 56 bytes of entry/backend overhead require at least $20\text{M}\times96=1.92$ GB before caches, indexes, logs, snapshots, replication, and headroom.

### Example 3

A keyed map has 100 subentries averaging 24 bytes content and 40 bytes overhead. The approximate per-key base is 6.4 KB, not 2.4 KB; one million such keys is about 6.4 GB before backend amplification.

### Example 4

Checkpoint C contains source next offset 500 and balance 90. A newer local state has balance 100 after offsets 500–509. Restoring balance 100 with offset 500 applies those ten updates twice; restoring balance 90 with offset 510 skips them.

### Example 5

A dedup ID lives for one hour, but source retries can occur for six hours after outage. A duplicate at hour two is accepted. Memory was bounded, but the promised deduplication contract was violated.

### Example 6

State expires when `now-last_write>300`. At exactly 300 seconds it remains; at 301 it is logically absent. A `>=` implementation changes the boundary. Tests must pin strictness and clock.

### Example 7

An event-time timer for timestamp 1,000 is restored when the watermark is already 1,100. It may fire immediately after recovery. Its output uses a stable timer/business ID so a prior ambiguous effect deduplicates.

### Example 8

1,024 key groups run on 32 tasks, about 32 groups each. Scaling to 64 moves group ownership, not key identity, and averages 16 groups per task. Maximum parallelism remains bounded by the group count.

### Example 9

A state field changes from 32-bit integer cents to decimal currency plus code. Even if a serializer can add fields, business migration must define currency for old values, overflow, rounding, validation, and rollback.

### Example 10

This fixture applies a deterministic per-key transition with separate durable dedup identity and strict processing-time TTL.

<!-- bijux-verify: {"id":"stateful-transition-ttl","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=4 duplicates=1 evicted=('a', 'b')\nstate={'a': (1, 9)} seen=4\n","stderr":""}} -->
```python
events = (
    ("a", "e1", 0, 5),
    ("a", "e2", 2, -2),
    ("a", "e2", 2, -2),  # producer retry
    ("b", "e3", 3, 7),
    ("a", "e4", 9, 1),
)
ttl = 5
state = {}
seen = set()
accepted = duplicates = 0
evicted = []

for key, event_id, now, delta in events:
    for old_key, (_, last_write) in tuple(state.items()):
        if now - last_write > ttl:
            evicted.append(old_key)
            del state[old_key]
    if event_id in seen:
        duplicates += 1
        continue
    seen.add(event_id)
    balance = state.get(key, (0, now))[0]
    state[key] = (balance + delta, now)
    accepted += 1

print(
    f"accepted={accepted} duplicates={duplicates} "
    f"evicted={tuple(evicted)}"
)
print(f"state={dict(sorted(state.items()))} seen={len(seen)}")
```

The fixture validates one local transition and TTL boundary. It does not model distributed checkpoints, timer services, backend cleanup, replay, rescaling, schema migration, or external effects; the dedup set deliberately has a separate longer lifecycle.

## Cross-Program Connections

- **Data Structures:** hash maps, LSM trees, logs, Bloom filters, heaps, timer wheels, indexes, and persistent structures determine access/amplification.
- **Distributed Systems:** state machines, snapshots, logs, consistent cuts, epochs, transactions, replay, and failure detectors underpin recovery.
- **Database Systems:** MVCC, WAL, compaction, indexes, schema migration, isolation, and conditional effects recur inside state backends.
- **Data Engineering:** CDC identity, dedup horizons, stream-table joins, enrichment, backfills, and schema registries shape state contracts.
- **Security Engineering:** state encryption, key management, least privilege, query controls, tenant isolation, retention, deletion, and audit protect concentrated data.
- **Reliability Engineering:** checkpoint/restore SLOs, compaction debt, disk/native memory, hot keys, capacity, and restore drills make state operable.
- **Platform Engineering:** stable operator identity, storage classes, workload placement, rollout/rollback, autoscaling, and telemetry support lifecycle.
- **Systems Engineering:** state size, latency, correctness, recovery, cost, evolution, and privacy form a coupled lifecycle system.

## References

1. Akidau, T., et al. [“MillWheel: Fault-Tolerant Stream Processing at Internet Scale.”](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/) PVLDB, 2013. Foundational keyed state, timers, persistent state, low-watermarks, and exactly-once processing design.
2. Apache Flink. [Stateful Stream Processing.](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/) Current concepts for keyed state, key groups, checkpoint/savepoint persistence, rescaling, backends, and recovery semantics.
3. Apache Flink. [Working with State.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/state/) Current API documentation for keyed/operator/broadcast state, descriptors, types, TTL, and checkpointed functions.
4. Apache Flink. [Fault Tolerance via State Snapshots.](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/) Current explanation of local working backends, durable checkpoint storage, consistent snapshots, and recovery.
5. Apache Flink. [State Schema Evolution.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/serialization/schema_evolution/) Current serializer/schema migration support and limitations, including key-schema restrictions.
6. Apache Flink. [State TTL Migration Compatibility.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/state_migration/) Current version-qualified TTL serializer/backend migration behavior and limitations.
7. Apache Flink. [Tuning Checkpoints and Large State.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/) Current operational guidance for large state, checkpoint barriers, backend storage, and recovery behavior.
8. Apache Beam. [Programming Guide: State and Timers.](https://beam.apache.org/documentation/programming-guide/) Current state types, per-key/window scope, timers, deferred access, and garbage-collection contracts.
9. Apache Beam. [Runner Authoring Guide: State and Timers.](https://beam.apache.org/contribute/runner-guide/) Primary runner contract for atomic bundle outputs/state/timers/watermarks and per-key/window consistency.
10. Apache Kafka. [Processor API: Fault-Tolerant State Stores.](https://kafka.apache.org/43/streams/developer-guide/processor-api/) Current state-store, changelog, compaction, custom restore, and co-partitioning documentation.
11. Apache Kafka. [Running Streams Applications.](https://kafka.apache.org/43/streams/developer-guide/running-app/) Current documentation for task migration, changelog replay, checkpoints, standby/warmup replicas, and recovery lag.
12. Apache Spark. [TransformWithState.](https://spark.apache.org/docs/latest/streaming/structured-streaming-transform-with-state.html) Current arbitrary state processor, state variables, TTL, timers, initial state, output/time modes, schema evolution, and testing documentation.
13. Apache Spark. [Configuration: Structured Streaming State Store.](https://spark.apache.org/docs/latest/configuration) Current configuration contracts for state-store provider/encoding/schema checks and related streaming state behavior.

## Exercises

### Exercise 1

A keyed store has 12 million live keys. Each has two values of 24 and 40 encoded bytes; each state entry adds 48 bytes physical overhead. Estimate base bytes before backend amplification. If indexes/caches/WAL add 65%, compute the working estimate in decimal GB.

### Exercise 2

A checkpoint contains state after offsets `[0,800)` and source next offset 800. A local store later includes `[800,850)`, but the last completed checkpoint remains 800. Explain the only safe pair on recovery and how the 50 records are handled.

### Exercise 3

Deduplication must cover a 24-hour normal retry window, 8-hour maximum outage, 6-hour catch-up, and 20% margin. Compute a minimum TTL under additive planning. Explain clock/refresh/retention assumptions still required.

### Exercise 4

A job has 4,096 key groups and scales from 64 to 160 instances. Compute average groups per instance before and after. State why averages do not prove balanced state or fast restore and what transfer invariants apply.

### Exercise 5

Design a stateful-operator upgrade review for renaming a field, changing key normalization, adding TTL, and changing timer behavior. Separate changes that may be serializer-compatible from those needing semantic/state migration, and give verification evidence.

## Answers to the Exercises

### Answer 1

Per key, content is $24+40=64$ bytes and two entry overheads are $2\times48=96$, total 160 bytes. Base is $12\text{M}\times160=1.92$ GB. With 65% amplification, $1.92\times1.65=3.168$ GB. This excludes size tails, allocator rounding, compaction peaks, snapshots, replication, timers, and failure headroom.

### Answer 2

Restore the completed pair: state through 799 and source next offset 800. Discard/untrust the newer local mutations unless an engine-specific validated changelog protocol incorporates them into the same recovery point. Re-read offsets 800–849 and deterministically rebuild their state/output; effect protocol must tolerate replay. State through 849 paired with offset 800 duplicates, while old state paired with offset 850 skips.

### Answer 3

Additive horizon is $24+8+6=38$ hours; with 20% margin it is 45.6 hours, so configure at least that precision or round conservatively upward (for example 46 hours). Specify processing versus event-time clock, strict boundary, refresh on write/read, logical visibility, cleanup lag, checkpoint/changelog retention, and whether outage/catch-up can overlap rather than add. Legal/business deletion may constrain the result.

### Answer 4

Before scaling, average is $4096/64=64$ groups per instance. Afterward it is $4096/160=25.6$, so some instances receive 25 and some 26 if count-balanced. Groups can differ greatly in bytes, keys, timers, and update rate. Every group must map to exactly one eligible new owner; state/timers/checkpoint identity and checksums must match; restore/fencing completes before effects; no group is omitted or duplicated.

### Answer 5

A field rename may be serializer-incompatible even if business meaning is unchanged; test old bytes, migration rules, defaults, downgrade, and state invariants. Changing key normalization is a key-identity/routing migration that may merge/split states and needs explicit export/rekey/merge policy or replay into a new job. Adding TTL changes state serialization in some versions and always changes semantics; validate engine/version compatibility, existing-entry behavior, clock/refresh/boundary, replay horizon, and deletion. Timer behavior changes $T_v$ semantics and persisted timer interpretation; version timer IDs/namespaces, migrate/cancel old timers, test overdue recovery and idempotent effects. Evidence includes production-derived snapshot rehearsal, counts/checksums, sampled semantic diffs, replay comparison, resource estimates, failure injection, rollback restore, and policy approval.
