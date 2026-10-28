---
module_id: DE-059
program: Data Engineering
level: 2
module_number: 59
title: Stateful Stream Transformations
status: complete
last_verified: 2026-09-03
---

# Stateful Stream Transformations

## One-Page Review

### Governing question

How can a streaming transformation safely remember prior events, schedule future actions, recover and rescale, evolve its stored representation, bound resource use, and produce replay-equivalent results without confusing local working state with a durable source-coupled recovery point?

### Essential definitions

- A **stateful transformation** computes an output or decision from the current input plus remembered information from earlier inputs or timers.
- **Keyed state** is logically partitioned by the same stable key that routes records; a task accesses the state for its current key.
- **Operator state** belongs to a parallel operator instance rather than an individual key and needs an explicit redistribution rule on rescale.
- **Broadcast state** replicates control/reference updates to parallel tasks under a deterministic update contract.
- A **state primitive** is a runtime-managed value, list, map, reducing, aggregating, or comparable structure with defined serialization and access semantics.
- A **transition function** maps prior state, input, metadata, and policy version to new state, outputs, and timer operations.
- A **timer** is durable scheduled state that invokes a callback when event-time or processing-time progress reaches its condition.
- A **checkpoint** is an automatically managed consistent recovery snapshot that couples operator state with replayable source positions under the runtime's protocol.
- A **savepoint** is an operator-initiated consistent state image intended for controlled stop/resume, fork, upgrade, or rescale; its compatibility and ownership differ by runtime.
- A **state backend/store** holds the live working representation; **checkpoint storage** or a **changelog** supplies durable recovery evidence.
- A **changelog** records state mutations so a store can be restored by replaying them from a known position.
- A **key group/shard** is a stable redistribution unit between logical keys and parallel tasks.
- **State TTL** is an automated visibility/cleanup policy tied to a specified clock and update rule; it is not automatically a business retention guarantee.
- **State schema evolution** changes the serialized key/value/timer representation while preserving an explicit compatibility path.
- **Recovery point objective (RPO)** bounds accepted state/effect loss; **recovery time objective (RTO)** bounds restore, replay, warm-up, and availability time.

### Central model, mechanism, or theorem

For key $k$, ordered input $x_n$, metadata $m_n$, prior state $S_{k,n}$, and policy/state schema version $v$, define a deterministic transition

$$
(S_{k,n+1},Y_n,T_{k,n+1})=F_v(S_{k,n},x_n,m_n,T_{k,n}),
$$

where $Y_n$ is a finite output sequence and $T$ is timer state. A recovery cut $C_j$ must bind source position vector $P_j$, operator state $S_j$, timers $T_j$, and effective topology/schema/configuration identity $V_j$:

$$
C_j=(P_j,S_j,T_j,V_j).
$$

If the source can replay exactly the suffix after $P_j$, restoration decodes the complete state/timer image, and every transition uses the same ordered inputs and deterministic dependencies, then replay reconstructs the same logical state and outputs before sink-side qualification. End-to-end exactly-once additionally requires transactional or idempotent output coordination; a correct state checkpoint alone cannot retract duplicate external effects.

Approximate state capacity is

$$
B_{live}\approx\sum_k(B_{key}+B_{value}+B_{index}+B_{timers})+B_{backend},
$$

and recovery time includes snapshot acquisition plus replay/warm-up, not merely process restart.

### Critical invariants

- Key extraction, normalization, partition function, maximum shard/key-group space, topology identity, and state ownership are versioned.
- Each logical key has one active writer epoch for a state shard; stale or concurrent owners cannot both publish accepted results.
- State name, primitive, serializer/schema, default/absence semantics, invariants, clock, TTL, and cleanup behavior are explicit.
- Transition logic is deterministic with respect to recorded input, metadata, policy/reference versions, and timer events; wall-clock, randomness, and remote reads are captured or isolated.
- A durable recovery cut couples replayable source positions with the exact state and timers produced through those positions.
- Checkpoint completion, retention, integrity, encryption, restore test, and ownership are observed rather than inferred from job health.
- Timers are keyed/windowed as documented, restored, deduplicated or replaced deliberately, and cleared with their associated state.
- State TTL never expires an unresolved business obligation merely to control storage; post-expiry late/recovery behavior is defined.
- State and changelog/checkpoint retention cover maximum recovery/backfill horizons with margin and legal/privacy constraints.
- Rescaling moves each redistribution unit once, preserves logical key ownership, and cannot change key serialization silently.
- State schema, operator identity, topology, backend, and runtime upgrades have a tested restore or rebuild path plus rollback.
- Outputs carry deterministic identity/version and use sink semantics compatible with recovery replay.
- Metrics expose state size/cardinality/skew, timers, checkpoint age/duration/failure, alignment/backpressure, changelog/restore lag, TTL cleanup, and migration progress.
- A bounded oracle, snapshot inspection, fault injection, and exact-cut reconciliation validate both outputs and hidden state.

### Common failures

Common failures include storing state in a process variable; assuming local disk is a backup; keying by mutable or nondeterministic data; reading remote mutable reference data during transitions; checkpointing state without source position; acknowledging source progress before durable state/effect; treating “exactly once” as one execution; registering unbounded duplicate timers; using processing-time TTL for event-time obligations; changing serializer, key type, state name, operator ID, partition count, or backend in place; disabling changelogs without accepting recovery loss; restoring a stale snapshot after changelog/source retention expired; rescaling without stable shard mapping; querying state without a consistent cut; and measuring only record throughput while checkpoint age and restore debt grow.

### Compact example

Offsets 0–2 update keyed totals to `a=3` and `b=7`, with last event times 6 and 4 and event-time cleanup timers 16 and 14. A checkpoint records next source offset 3 plus both keyed states and timers. Offset 3 then changes `a` to 7 and replaces its timer with 19. Restoring the checkpoint and replaying from offset 3 reproduces the same live state. Watermarks 15 and 20 fire `b` then `a`. This arithmetic assumes deterministic order and transition logic; it says nothing about whether an external sink applies replayed emissions once.

### Connections

[DE-052](052-topics-partitions-and-offsets.md) defines partition/source positions, [DE-053](053-producer-keys-and-ordering.md) defines key ownership and order, [DE-055](055-delivery-semantics-in-streaming-pipelines.md) defines recovery delivery, [DE-056](056-exactly-once-effects.md) qualifies external effects, and [DE-058](058-windows-and-watermarks.md) defines event-time progress and cleanup. DE-060 adds explicit late, duplicate, and out-of-order policy; DE-061 begins object-storage and lakehouse practice.

## Governing Question

A stateless map can reprocess one record without remembering history. A balance, distinct set, session, rolling feature, fraud rule, join, deduplicator, pattern detector, or inactivity alert cannot. Its result depends on earlier records, scheduled time, or both. That dependency becomes production data even when it lives inside a stream processor.

State creates three coupled obligations. Semantics must define what the memory means and how each ordered input changes it. Operations must keep the working set available, durable, bounded, observable, and movable. Change management must preserve or intentionally rebuild state when code, schema, topology, partitioning, or runtime changes.

The governing question is not “which state API should we call?” It is “what recovery history will be accepted as equivalent?” A correct design identifies the transition function, key ownership, input cut, timers, dependencies, output identity, state representation, snapshot/changelog protocol, retention, and migration path that make that equivalence testable.

Managed state reduces implementation burden but does not choose business semantics. Runtimes cannot infer whether absence means zero, unknown, deleted, expired, or not yet restored. They cannot decide whether TTL may forget a payment obligation. They cannot make a nondeterministic remote lookup replay identically. These decisions remain part of the data contract.

## Why This Matters

State corruption can outlive the triggering incident. A transient duplicate incorporated into a lifetime aggregate affects every later output. A bad reference-data update broadcast across tasks can alter millions of keys. A changed serializer may make the only viable checkpoint unreadable.

Recovery couples data and computation. If state is restored at offset 1,000 but the source resumes at 1,100, one hundred effects disappear. If the source resumes at 900, two hundred transitions repeat. Repetition can be safe for managed state under the runtime protocol but still duplicate emails, payments, or non-idempotent database writes.

State determines scaling limits. Adding workers does not help one hot key that must be processed sequentially. A one-byte business flag may cost far more after key, serializer, index, TTL metadata, timer, changelog, cache, and checkpoint amplification. Large state slows checkpointing, deployment, rescale, and incident recovery.

Cleanup is correctness policy. Retaining everything is unbounded and may violate privacy or erasure requirements. Expiring too early converts delayed data or disaster replay into a new initial state. A generic access-based TTL can silently reset histories that the business believes are continuous.

State migration is a data migration. Renaming an operator or changing a key type can orphan stored state. A rolling deployment may let old and new transition functions update shards under different rules. Savepoint success does not prove that the new program interprets every byte correctly.

## Prerequisites and Retrieval

Retrieve the business state machine: key; initial/absent state; accepted input order; transition rules; output and side-effect identity; invalid transition; correction; terminal state; reopening; timers; finality; and responsible owner.

Retrieve input identity and order: topic/source generation; partition/shard; offset/sequence; event ID/version; transaction boundary; key field and normalization; timestamp authority; watermark; schema; retries; backfill; and replay horizon.

Retrieve each state declaration: operator and stable ID; state name; primitive; key/window scope; serialized key/value schema; serializer and compatibility snapshot; default/null/empty semantics; invariants; TTL; timer families; broadcast/operator redistribution; and query exposure.

Retrieve runtime topology: source, repartition, operator chain, parallelism, maximum parallelism/shard count, key-group assignment, input gates, async operations, sink, internal topics, state backend/store, local directories, managed memory/cache, checkpoint storage, and encryption identities.

Retrieve recovery configuration: checkpoint interval/timeout/minimum pause/concurrency; aligned or unaligned mode; incremental/full snapshot; changelog; retention/count; externalization; source participation; sink transaction; failure restart; local recovery; standby replica; savepoint format; operator IDs; and restore command.

Retrieve observed recovery evidence: latest completed checkpoint and age; duration and alignment; persisted bytes versus full state size; failures; source position vector; state/timer counts; changelog lag/start offsets; standby/warm-up lag; snapshot checksum; restore duration; replay rate; and reconciliation result.

Retrieve capacity evidence: distinct active keys; per-key state and timer distribution; hot-key rate; skew; state reads/writes per record; cache hit; compaction; spill; local disk; remote snapshot throughput; checkpoint amplification; recovery bandwidth; source backlog; and quota headroom.

Retrieve change history: code/policy/reference version; operator topology/UID; state names; key and value schema; serializer snapshots; state backend/provider; parallelism/max parallelism; repartition topic; TTL semantics; timer behavior; runtime version; savepoint/checkpoint ownership; and rollback compatibility.

Retrieve governance: data classification; state encryption; tenant boundary; interactive query authorization; deletion/erasure propagation to local state, checkpoints, changelogs, and standbys; retention/legal hold; audit; backup disposal; and incident access.

Distinguish working state from durable snapshot; checkpoint from savepoint; local recovery cache from authoritative recovery copy; keyed from operator/broadcast state; source offset from state-store changelog offset; state TTL from window lateness/business retention; event-time timer from processing-time timer; transition exactly-once from end-to-end effect exactly-once; logical state size from checkpoint delta; restart time from full recovery time; serializer compatibility from semantic compatibility; and queryable state from a transactionally consistent business view.

Create a state contract:

| Concern | Required decision and evidence |
|---|---|
| Meaning | Key, initial state, transition, invariant, outputs, invalid/terminal behavior |
| Representation | Primitive, key/value/timer schema, serializer, names, operator/topology version |
| Ownership | Partition function, shard/key groups, active writer epoch and rescale rule |
| Time | Event/processing timers, watermark, TTL clock/update/visibility and cleanup |
| Recovery | Source cut, snapshot/changelog, completion, retention, restore and replay |
| Effects | Output identity, transaction/idempotency, commit boundary and reconciliation |
| Capacity | Keys, skew, bytes, timers, I/O, checkpoint, changelog, restore and quotas |
| Change | Compatibility matrix, savepoint/rebuild, dual run, cutover and rollback |
| Governance | Classification, encryption, access, deletion, retention and audit |
| Evidence | Model tests, snapshot inspection, fault injection, restore drill and exact-cut oracle |

Write a falsifiable claim: “Topology `risk-state-v3` keys by canonical account ID into 4,096 stable shards; transition version 7 consumes one partition-ordered source record at a time, reads only versioned broadcast rules, replaces one event-time timer, and emits deterministic upserts; completed checkpoints bind offsets, keyed/broadcast state, timers, and sink transaction; 30-day event-time cleanup matches correction policy; savepoint restore and rebuild paths are tested; and monthly kill/restore/rescale drills reconcile every key to a bounded oracle.”

## Learning Objectives

After completing this module, you should be able to:

1. specify a deterministic keyed transition function including metadata, outputs, and timers;
2. distinguish keyed, operator, broadcast, working, checkpointed, and changelog-backed state;
3. explain why recovery must couple state/timers with replayable source positions;
4. qualify managed-state and end-to-end delivery guarantees across sources and sinks;
5. choose state primitives, backends, snapshots, changelogs, and standby strategies from workload evidence;
6. design event-time/processing-time timers and TTL without premature obligation loss;
7. estimate state, checkpoint, replay, hot-key, and restore capacity;
8. rescale through stable shards/key groups and fenced ownership;
9. evolve operator identity, state schema, serializer, topology, and backend safely; and
10. inspect, fault-test, restore, and reconcile hidden state against an exact-cut oracle.

## Core Exposition

### Start with a state machine, not a store

Define the logical state independent of runtime classes. For each key, list states, accepted events, guards, transitions, outputs, timer registration/cancellation, and terminal behavior. Define absence explicitly: it might mean no history, expired history, deleted subject, or restore not complete.

Keep the transition small and deterministic. Inputs include record metadata when partition/offset, event version, or timestamp affects the decision. Policy and reference-data versions are inputs too. Record any unavoidable nondeterministic result before it changes durable state.

Separate a durable fact from a cache. A cache can be discarded and reconstructed without semantic loss. A balance, dedup receipt, join candidate, unresolved workflow, or correction obligation cannot be forgotten under the same policy.

### Key state by stable ownership

Keyed state colocates all transitions for one key with the records for that key. Apache Flink describes keyed state as partitioned with keyed streams and accessible only for the current key. This gives local update efficiency, but correctness depends on identical key extraction and serialization at every producer/repartition boundary.

Use a stable domain identifier, canonical encoding, tenant namespace, and version. Null, malformed, oversized, mutable, or adversarial keys need explicit routing. A customer email is usually a bad long-lived state key because normalization and ownership can change.

One hot key cannot be parallelized by adding ordinary keyed workers. If the transition is decomposable, shard by a deterministic subkey and merge with an associative operation. Otherwise accept sequential ownership and isolate/capacity-plan it.

### Choose the correct state scope and primitive

Value state suits one current aggregate or machine state. Map state supports keyed members and point changes. List/bag state supports multiple retained items but can grow without bound. Reducing or aggregating state can apply associative compaction early. Primitive semantics, iteration order, nulls, and update atomicity are runtime-specific.

Operator state is appropriate when ownership belongs to a source/operator instance, such as assigned partitions and offsets. Its rescale redistribution can be even-split, union, or custom depending on API. It should not hide per-business-key state that needs deterministic repartition.

Broadcast state distributes control updates to all tasks. Apply identical updates deterministically; do not let task-local arrival races produce different rule maps. Retain rule version with outputs and checkpoints.

Name every state object durably. In Flink savepoint restoration, stable operator UIDs map stored state back to the new topology. Generated identities can change with topology edits. State names and serializer descriptors are part of compatibility, not private refactoring details.

### Make transitions deterministic and ordered

For a partition-ordered source, one key's transition sequence should be reproducible from the same source cut. Do not iterate unordered maps when output order matters. Do not call current wall time, unseeded randomness, host locale, mutable environment, or an unversioned service inside the state update.

Asynchronous enrichment creates an ordering decision. Capture the response and version as a durable input, preserve sequence, or explicitly permit unordered completion with a commutative merge. A retry must not observe a different remote answer invisibly.

If duplicate or out-of-order records are possible, state includes the evidence needed to decide them: event ID, version, sequence, or bounded reorder buffer. DE-060 develops these policies; DE-059 requires their memory and recovery to be explicit.

### Couple source position, state, and timers

A state snapshot without its source position is ambiguous. A source position without matching state is equally unsafe. A consistent cut says exactly which inputs contributed to every state shard and timer.

Flink's checkpoint model includes source pointers and operator state through checkpoint barriers; multi-input alignment can ensure the snapshot covers inputs consistently. Recovery rewinds and replays. Its “exactly once” state claim means replayed records affect managed state once in the recovered logical history, not that the runtime invokes user code once.

A changelog-backed store records mutations and restores local state by replaying the changelog. Kafka Streams documents compacted changelog topics for fault-tolerant stores and compaction plus deletion for window stores. Disabling logging removes that recovery mechanism and standby eligibility.

Record the recovery cut identity and prove it through a restore, not by comparing timestamps from separate dashboards.

### Distinguish live state, backup, and operational image

The live state backend optimizes reads/writes. Durable checkpoint storage protects recovery. Local disk/cache speeds restart but may vanish with the worker. A savepoint is an operator-controlled image for planned change. These layers have different ownership, retention, portability, and deletion.

Flink currently documents heap and embedded RocksDB-style backends plus backend-specific snapshot trade-offs. Incremental checkpoints store changes relative to prior snapshots and can reduce checkpoint bytes, but restore may need multiple files and its speed depends on network, CPU, and I/O bottlenecks. A displayed delta size is not total recoverable state.

Kafka Streams local stores can restore from changelog topics; standby replicas trade extra storage and processing for lower failover lag. A warm local copy is not safe if its changelog/source history has been truncated beyond the needed position.

### Treat timers as state

An event-time timer fires when the operator's watermark passes its timestamp; a processing-time timer uses runtime time. Both must be restored consistently and registered/cancelled idempotently. Repeatedly adding a timer per record can create millions of redundant entries unless the runtime deduplicates the exact namespace/timestamp.

Use event-time timers for decisions tied to domain progress, such as closing inactivity after event time. Use processing-time timers for operational reminders and timeouts. Replay may reproduce event-time behavior but not historical processing-time wall schedule unless that schedule is recorded.

Timer callbacks are transitions. They read and update state, emit versioned output, and clear or replace timers atomically under the runtime contract. Test timer/event races at the same timestamp and after restore.

### Design TTL and cleanup from semantics

TTL bounds state only when its clock, refresh event, visibility rule, and cleanup mechanism match the obligation. Access-based, write-based, processing-time, and event-time expiry yield different histories. Lazy deletion can leave bytes after logical expiry; background cleanup can create I/O load.

Flink's state API documents TTL behavior and version-specific migration compatibility. Spark `TransformWithState` supports TTL on its state variables, with current APIs tying TTL behavior to supported time modes. Product details evolve; pin and test the deployed version.

State needed for maximum source replay, offline delay, correction, dispute, or legal recovery cannot expire earlier without a separate durable authority. Erasure requirements may require the opposite: remove subject state and all governed recovery copies on an auditable schedule.

When expired state receives a later record, define whether it initializes anew, routes to reconciliation, rebuilds from history, or fails closed. A default zero can turn forgotten history into a plausible but false aggregate.

### Bound state and checkpoint cost

Estimate active keys, states per key, serialized key/value sizes, indexes, timers, window/join multiplicity, backend metadata, cache/write buffers, changelog replication, checkpoints, and standbys. Use distributions: p50 hides a tenant holding half the state.

State write rate matters as much as size. Each record can cause read-modify-write, timer changes, changelog append, checkpoint dirtiness, compaction, and sink update. Large records or high churn can saturate local disk and remote checkpoint bandwidth.

Checkpoint duration must remain below the configured interval/timeout with headroom. Alignment can add delay under backpressure. Too-frequent checkpoints consume throughput; too-infrequent checkpoints increase replay and RPO exposure. Measure completed checkpoint age, not configuration alone.

### Calculate recovery debt

Recovery time includes scheduling, artifact/config fetch, snapshot/changelog download, deserialization, index/cache warm-up, replay from checkpoint to source head, state-store catch-up, sink transaction recovery, and validation before serving.

A planning lower bound is

$$
T_{restore}\gtrsim\frac{B_{download}}{r_{network}}+rac{B_{decode}}{r_{decode}}+rac{N_{replay}}{r_{replay}}+T_{coordination}.
$$

Rates interact and parallelism/skew limit them, so do not simply trust the sum. If new input arrives faster than recovery processes it, backlog never converges. Standbys/local recovery reduce some terms but need freshness and failure-domain evidence.

Test worst retained checkpoints and cold workers. A fast restart with tiny development state is not an RTO result.

### Rescale through stable redistribution units

Directly mapping keys to task numbers makes task count part of state identity. Use a stable virtual shard/key-group space, then assign groups to current tasks. Flink key groups serve as the atomic unit for redistributing keyed state and are tied to maximum parallelism.

Rescale must move each unit completely, prevent two active writers, preserve timers and source ownership, and resume from a consistent cut. Measure transfer bytes, network/disk contention, checkpoint duration, and skew after placement.

Changing key serialization or maximum shard space can be a rekey/rebuild rather than an ordinary rescale. Prove runtime support; do not infer it from a successful job submission.

### Coordinate outputs and external effects

Managed state and output may share a transactional boundary only for supported sinks. Otherwise a crash can occur after an external effect but before the checkpoint acknowledges it, or after state mutation but before effect visibility.

Emit deterministic effect IDs from input/business identity plus transition version. Use transactional sinks, idempotent target operations, outbox/commit protocols, or reconciliation. DE-056 supplies the full effect argument.

Interactive queries against local state are operationally useful but can expose a moving, sharded, restoring view. Route by current ownership, authenticate tenant access, label consistency and checkpoint position, and do not present it as a globally transactional database unless the runtime proves that property.

### Evolve state as durable data

Inventory operator IDs, state names, key/value schemas, serializer snapshots, timers, TTL metadata, topology, backend, and runtime version before change. Compatibility has two levels: bytes may decode, yet new code may interpret them differently.

Flink documents supported state-schema evolution by serializer/type and notes that key-schema evolution is not generally supported because changed keys can collapse identities. Spark's current `TransformWithState` guide similarly distinguishes value-side evolution and unsupported key-side changes. Treat product matrices as version-specific.

For compatible evolution, take and retain a tested savepoint/checkpoint, deploy with stable identities, restore in isolation, scan invariants, replay a finite suffix, and compare. For incompatible changes, run an explicit state transformer if supported or rebuild from authoritative history into a new topology/output generation.

Never allow old and new writers to publish the same state key without epoch fencing and consumer version rules. Define rollback before the new format writes irreversible state.

### Observe hidden state directly

Monitor logical state entries/bytes per operator and shard, distribution by key, timer count/age, TTL expirations/cleanup, local disk/cache/compaction, changelog append/restore lag, checkpoint start/completion age/duration/alignment/bytes/failure, savepoint integrity, restart/replay rate, standby freshness, and sink commit/reconciliation.

Inspect actual state when possible. Spark's state data source exposes checkpoint state for testing and incident investigation, including current support for `TransformWithState` variables and timers. Such inspection is powerful but versioned/experimental and requires privacy and consistency controls.

Attach exemplars from output to source partition/offset, key, transition version, prior/new state digest, timer operation, checkpoint generation, and effect ID. Avoid logging full sensitive state.

### Test failure, recovery, and migration

Model-test transition sequences including empty, invalid, terminal, reopen, duplicate, reorder, correction, and timer/event equality. Compare incremental execution with a bounded reference implementation over the same ordered cut.

Kill workers before/after state write, output, barrier, checkpoint completion, changelog flush, timer firing, and sink commit. Corrupt or remove local state; restore cold; truncate only in isolated tests; lose one region; rescale up/down; move hot shards; and verify fencing.

Test oldest retained snapshot plus maximum replay, expired TTL, new/removed fields, renamed operators/state, changed serializer/backend/runtime, rollback after new writes, and rebuild convergence. Validate hidden state and timers, not output samples alone.

### Review the complete state argument

A defensible stateful design connects fifteen claims: state-machine meaning is explicit; key ownership is stable; state scope/primitive fits; transitions are deterministic; source order and state cut align; timers recover; live/durable layers are distinct; TTL matches obligations; capacity includes amplification/skew; checkpoints meet RPO; cold recovery meets RTO; rescale preserves ownership; outputs survive replay; schema/topology changes restore or rebuild; and direct inspection plus fault/reconciliation evidence validates the claim.

If one link is missing, narrow the guarantee. A state store can be durable but semantically wrong, checkpointed but paired with the wrong offset, recoverable but outside RTO, rescalable but hot-key bound, byte-compatible but meaning-incompatible, or internally exactly once while duplicating external effects.

## Definitions and Notation

For key $k$ and its $n$th accepted transition, define:

- $x_{k,n}$: input record or timer event.
- $m_{k,n}$: stable metadata such as source position, timestamp, schema, and policy version.
- $S_{k,n}$: logical state before the transition.
- $Y_{k,n}$: finite output sequence from the transition.
- $T_{k,n}$: registered timer set/state.
- $v$: transition and state-schema version.
- $P_j$: vector of next source positions captured at recovery cut $j$.
- $C_j$: complete recovery cut.
- $G$: number of stable virtual key groups/shards.
- $p$: current parallel task count.
- $B$: bytes and $r$: sustainable rate for capacity/recovery estimates.

The transition is

$$
(S_{k,n+1},Y_{k,n},T_{k,n+1})
=F_v(S_{k,n},x_{k,n},m_{k,n},T_{k,n}).
$$

Replay equivalence requires the same accepted order and deterministic dependencies:

$$
F_v^*(S_{k,0},X_k,M_k)=F_v^*(S_{k,0},X_k,M_k).
$$

The tautological notation emphasizes that hidden wall time, randomness, locale, mutable remote data, or iteration order effectively changes $M_k$ and invalidates the premise.

A recovery cut is

$$
C_j=(P_j,S_j,T_j,V_j,D_j),
$$

where $V_j$ identifies topology/code/state configuration and $D_j$ identifies required versioned dependencies. Integrity and completion evidence are part of the usable cut even if not inside its payload.

With a stable group function $g(k)\in\{0,\dots,G-1\}$, rescaling changes only owner assignment

$$
owner_p(g):\{0,\dots,G-1\}\rightarrow\{0,\dots,p-1\},
$$

not $g(k)$. Platform mapping algorithms differ; do not substitute an illustrative modulo function for the runtime contract.

Approximate live bytes are

$$
B_{live}\approx N_k(\bar B_{key}+\bar B_{value}+\bar B_{index})+N_t\bar B_{timer}+B_{backend}.
$$

Durable footprint may multiply this by changelog replication, retained full/incremental snapshots, standbys, and object-store versions. Incremental checkpoint bytes are a delta, not $B_{live}$.

A rough cold-recovery lower bound is

$$
T_{recovery}\gtrsim T_{schedule}+\frac{B_{fetch}}{r_{fetch}}+\frac{B_{decode}}{r_{decode}}+\frac{N_{replay}}{r_{replay}}+T_{warm}+T_{validate}.
$$

Dependencies and bottlenecks make the terms non-independent; drills establish the actual distribution.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Define meaning.** Specify key, initial state, transition graph, outputs, timers, invalid/terminal/correction behavior, and invariants.
2. **Bind identity and order.** Record canonical key, partition/shard function, source generation/position, sequence/version, and ownership epoch.
3. **Declare representation.** Name operator/state, primitive, key/value/timer schema, serializer, TTL, topology, backend, and version.
4. **Eliminate hidden inputs.** Capture time, randomness, reference data, remote results, locale, and policy as deterministic dependencies.
5. **Establish recovery cuts.** Couple replayable source positions with complete state/timers/configuration and durable completion/integrity evidence.
6. **Qualify effects.** Prove managed-state delivery separately from transactional/idempotent sink behavior and reconciliation.
7. **Bound lifecycle.** Align TTL/cleanup, changelog/source/snapshot retention, privacy deletion, correction, and disaster horizons.
8. **Plan capacity and recovery.** Measure key/timer distributions, amplification, hot keys, checkpoints, replay, standbys, quotas, RPO, and RTO.
9. **Control rescale and change.** Preserve group ownership and stable IDs or rebuild isolated state; dual-run, compare, cut over, and retain rollback.
10. **Test evidence.** Model transitions, inspect snapshots, inject crash/rescale/corruption, cold restore, and reconcile exact cuts.

The ownership invariant is:

> Every logical key maps to one state shard and one fenced active writer epoch; rescaling moves ownership without splitting or duplicating accepted histories.

The recovery invariant is:

> A declared recovery point contains or references the exact source positions, state, timers, topology/schema/dependency versions, and completion evidence needed to replay one coherent history.

The determinism invariant is:

> Given identical accepted ordered inputs, metadata, initial state, timer progress, and versioned dependencies, live and recovered executions produce equivalent logical state and deterministic output identities.

The lifecycle invariant is:

> State is retained for every promised retry, replay, delay, correction, and obligation horizon unless an authoritative external record supports reconstruction; privacy/legal deletion applies consistently across working and recovery copies.

This executable models keyed totals, event-time timer replacement, a source-coupled checkpoint, deterministic suffix replay, timer firing, and illustrative virtual-shard reassignment. It does not implement a production checkpoint protocol, exact-once sink, runtime serializer, or platform key-group algorithm.

<!-- bijux-verify: {"id":"keyed-state-recovery","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"checkpoint_next_offset=3\nstate_after_checkpoint=(('a', (3, 2, 6, 16)), ('b', (7, 1, 4, 14)))\nstate_after_live=(('a', (7, 3, 9, 19)), ('b', (7, 1, 4, 14)))\nrestore_matches_live=True\ntimer_emissions=(('b', 7, 14), ('a', 7, 19))\nremaining_timer_keys=()\nkey_groups=(('a', 1), ('b', 2))\nowners_parallelism_2=(('a', 1), ('b', 0))\nstate_cells=8\n","stderr":""}} -->
```python
records = (
    {"offset": 0, "key": "a", "event_time": 2, "delta": 5},
    {"offset": 1, "key": "b", "event_time": 4, "delta": 7},
    {"offset": 2, "key": "a", "event_time": 6, "delta": -2},
    {"offset": 3, "key": "a", "event_time": 9, "delta": 4},
)
timer_delay = 10


def apply(state, record):
    old = state.get(record["key"], (0, 0, None, None))
    total, count, _, _ = old
    state[record["key"]] = (
        total + record["delta"],
        count + 1,
        record["event_time"],
        record["event_time"] + timer_delay,
    )


def stable_view(state):
    return tuple(sorted(state.items()))


checkpoint_next_offset = 3
checkpoint_state = {}
for record in records[:checkpoint_next_offset]:
    apply(checkpoint_state, record)

live_state = checkpoint_state.copy()
for record in records[checkpoint_next_offset:]:
    apply(live_state, record)

restored_state = checkpoint_state.copy()
for record in records[checkpoint_next_offset:]:
    apply(restored_state, record)

timer_state = live_state.copy()
timer_emissions = []
for watermark in (15, 20):
    for key, (total, count, event_time, timer_time) in sorted(tuple(timer_state.items())):
        if timer_time <= watermark:
            timer_emissions.append((key, total, timer_time))
            del timer_state[key]

group_count = 4
key_groups = tuple((key, sum(key.encode("utf-8")) % group_count) for key in sorted(live_state))
owners = tuple((key, group % 2) for key, group in key_groups)

print(f"checkpoint_next_offset={checkpoint_next_offset}")
print(f"state_after_checkpoint={stable_view(checkpoint_state)}")
print(f"state_after_live={stable_view(live_state)}")
print(f"restore_matches_live={restored_state == live_state}")
print(f"timer_emissions={tuple(timer_emissions)}")
print(f"remaining_timer_keys={tuple(sorted(timer_state))}")
print(f"key_groups={key_groups}")
print(f"owners_parallelism_2={owners}")
print(f"state_cells={sum(len(value) for value in live_state.values())}")
```

The modulo owner mapping and byte-sum groups are illustrative only. Production must use its runtime's stable key serialization, hash, maximum-parallelism, ownership, and fencing contract.

## Alternatives and Trade-Offs

**Stateless recomputation versus managed state.** Recomputing from an indexed external authority simplifies worker recovery but adds remote latency/load. Managed local state is fast and integrated with stream recovery but adds snapshots, migration, and capacity obligations.

**Keyed versus operator state.** Keyed state naturally redistributes by stable business key. Operator state fits source/instance ownership but requires explicit repartition semantics and is unsuitable for arbitrary per-key queries.

**Value/reducing state versus list/map state.** Compact aggregates bound memory and I/O but lose raw history. Collections support correction and richer logic but amplify state and cleanup complexity.

**Heap versus embedded/disk-backed state.** Heap favors direct low-latency access for bounded state but is memory/GC constrained. Disk-backed serialized state scales larger and supports different checkpoint trade-offs at serialization, compaction, cache, and local-disk cost.

**Full versus incremental checkpoints.** Full images are self-contained but rewrite all state. Incremental snapshots reduce changed bytes but depend on a file graph and can shift restore bottlenecks. Measure both checkpoint and cold restore.

**Snapshot versus changelog recovery.** Snapshots capture periodic images; changelogs continuously record mutations. Hybrids reduce replay or snapshot cost but require coordinated retention, compaction, and position integrity.

**Cold restore versus standby replica.** Cold restore minimizes steady duplicate resources but increases failover. Standbys shorten recovery when fresh and in the right failure domain, at storage/network/compute cost.

**Event-time versus processing-time timer.** Event-time timers replay with domain progress but can stall with watermarks. Processing-time timers support operational deadlines but their historical schedule is not naturally replay-stable.

**TTL versus explicit deletion timer.** TTL is convenient and backend-optimized but may use implicit clock/refresh/lazy cleanup. Explicit timers expose semantics and outputs but add timer state and code.

**Stable virtual shards versus direct task hashing.** Virtual groups support rescale without changing logical key identity. Direct mapping is simpler but entangles state with current parallelism.

**Compatible in-place restore versus rebuild.** Restore preserves accumulated state and shortens migration when compatibility is proven. Rebuild costs replay time but can handle new keys/meaning and provides a clean comparison generation.

**Interactive state query versus exported materialized view.** Direct query is fresh and useful for debugging but sharded/restoring and operationally coupled. An exported view has clearer API/SLO isolation but additional latency and duplication.

**Exactly-once managed state versus at-least-once plus idempotence.** Runtime exactly-once simplifies internal history at checkpoint/alignment cost. At-least-once can improve throughput but requires transition/output identities that absorb replay.

## Failure Modes and Misconceptions

**“A class field is state.”** It may vanish on restart and may not be partitioned, snapshotted, or restored by the runtime.

**“Local persistent storage is durable recovery.”** A worker or zone failure can remove it; authoritative remote snapshot/changelog evidence is distinct.

**“Checkpoint interval is the RPO.”** Only successfully completed, retained, readable cuts count, and sink/source guarantees qualify loss.

**“Exactly once means the function ran once.”** Recovery can invoke it again while reconstructing an equivalent managed-state history.

**“Exactly-once state means exactly-once email/payment.”** External effects need a transactional or idempotent protocol.

**“Offset commit can be independent of state.”** Mismatched positions and state cause loss or repeated transitions.

**“Any key works if it hashes.”** Mutable normalization, schema changes, nondeterministic serialization, nulls, or tenant collisions split or combine histories.

**“More workers fix hot keys.”** One indivisible ordered key remains on one owner unless the state algebra supports subsharding.

**“Map/list state is bounded by available disk.”** Semantic growth also increases checkpoints, changelog, restore, iteration, compaction, and deletion cost.

**“TTL is business retention.”** Its clock, refresh, visibility, and physical cleanup may not match delayed facts or legal obligations.

**“Expired state means the key never existed.”** It may mean forgotten history; a later record needs explicit reinitialization/rebuild/reconciliation policy.

**“Timer registration is free.”** Timers consume managed state, snapshots, indexes, and firing work; duplicate families can cause storms.

**“Processing timers replay historically.”** Restore occurs at a new wall/runtime time unless the framework persists and defines overdue behavior.

**“Incremental checkpoint size is total state.”** It commonly reports changed data; full recovery may reference several retained files.

**“A savepoint proves upgrade compatibility.”** The new program must map operators and decode/interpret state correctly under tested semantics.

**“Adding a nullable field is always safe.”** Runtime serializer/type/version matrices differ, and semantic defaults can still be wrong.

**“Changing key schema is ordinary evolution.”** It may change ownership or collapse distinct histories and often requires rekey/rebuild.

**“Rescale only moves compute.”** It transfers state/timers/source ownership and can dominate deployment and RTO.

**“Standby count guarantees instant failover.”** Replicas need capacity, placement, freshness, compatible history, and assignment.

**“Queryable state is a database snapshot.”** Reads may span shards and recovery moments without global transaction semantics.

**“Output samples validate state.”** Hidden corruption, stale timers, orphan keys, and wrong TTL can remain invisible until later events.

**“Renaming an operator is cosmetic.”** Stable state mapping may depend on its durable UID/name.

## Worked Examples

### Example 1

A fraud score stores `ValueState` per account with last accepted business version and aggregate features. The canonical account ID routes both source and state. A profile-service response is first materialized as a versioned stream input; retry does not perform an unrecorded fresh lookup.

### Example 2

A process checkpoints state consistent through next offsets `(p0=101,p1=88)`. It crashes after processing later records. Restore returns to that cut and replays the suffix. Internal state converges; deterministic effect IDs prevent replayed alerts from becoming duplicate notifications.

### Example 3

A dedup store disables its changelog to reduce broker traffic. Its host fails and local disk is lost. The application has no fault-tolerant store or standby to recover receipts, so old inputs can become new effects. The team either restores changelogging or narrows the safety claim.

### Example 4

One tenant sends 40% of all records under one key. Overall CPU is low, but its owner queues and its state grows. Adding tasks redistributes other key groups only. The design introduces deterministic subaccounts whose aggregates merge associatively, while retaining tenant-level sequencing where required.

### Example 5

An inactivity detector replaces one event-time timer at `last_seen+30m`. A newer event cancels/replaces the old timer. After checkpoint/restore the timer remains. When the watermark passes it, the callback emits an idempotent status revision and clears the key state.

### Example 6

A processing-time TTL of one day deletes device state during a weekend outage, although devices may upload after seven days. Monday's record initializes a false zero baseline. The repair aligns online state with the seven-day obligation or reconstructs from an authoritative durable history before transition.

### Example 7

A RocksDB-backed job reports 2 GB incremental checkpoint deltas but holds 400 GB logical state. Capacity and recovery planning use referenced full state, remote download, compaction, replay, and cache warming—not the 2 GB dashboard number alone.

### Example 8

A deployment inserts a stateless map before a stateful operator and relies on generated operator IDs. Restore cannot map the old state as intended. Stable explicit IDs and a preproduction savepoint restore would have exposed the problem.

### Example 9

State value schema adds `currency` with default `USD`. Bytes decode, but historical multi-currency keys are semantically misclassified. The migration derives currency from versioned source history and reconciles balances rather than accepting serializer compatibility as business correctness.

### Example 10

A cold-region drill restores a 6 TB snapshot at 1 GB/s effective aggregate fetch, decodes at 0.8 GB/s, and replays 900 million records at 150,000/s. Even naive sequential lower bounds are 100, 125, and 100 minutes respectively; orchestration and warm-up add more, so a 30-minute RTO claim fails without architectural change.

## Cross-Program Connections

Distributed systems contributes state-machine replication, consistent cuts, logical clocks, fencing, consensus, partial failure, checkpoint algorithms, and replay equivalence.

Database systems contributes transactions, WAL/changelogs, MVCC snapshots, indexes, compaction, isolation, materialized views, schema migration, and recovery.

Algorithms and data structures contributes hash partitioning, virtual shards, associative aggregates, incremental algorithms, heaps/timer wheels, sketches, and complexity under skew.

Operating systems contributes process memory, page cache, filesystem durability, local disk failure, mmap/native memory, scheduling, clocks, and crash consistency.

Storage engineering contributes LSM trees, write amplification, bloom filters, SST files, object-store bandwidth, checksums, retention, and garbage collection.

Formal methods contributes deterministic transition systems, invariants, linearization points, refinement, model checking, and trace equivalence.

Site reliability engineering contributes RPO/RTO, checkpoint-age SLOs, cold restore, capacity, chaos drills, incident inspection, and recovery runbooks.

Platform engineering contributes state backends, checkpoint storage, identities, autoscaling, deployment/savepoint orchestration, encryption, quotas, and observability.

API and service engineering contributes idempotency keys, versioned upserts, transactional outbox/inbox, query consistency, status resources, and correction contracts.

Security engineering contributes tenant-isolated keys, tamper-resistant source identity, encryption, least privilege, snapshot/changelog access, malicious hot keys, and audit.

Privacy and governance contributes minimization, retention, erasure across live/backup copies, legal hold, classification, lineage, and accountable corrections.

Software architecture contributes aggregates, event sourcing, CQRS, workflow/process managers, domain state machines, ownership boundaries, and rebuildable projections.

## References

1. Apache Flink. [Stateful Stream Processing](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/). Accessed 2026-09-03. Primary conceptual documentation for keyed state, colocated partitioning, key groups, checkpoints/savepoints, and rescaling.
2. Apache Flink. [Working with State](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/state/). Accessed 2026-09-03. Primary API documentation for keyed value/list/map/reducing/aggregating state, state TTL, operator state, redistribution, and broadcast state.
3. Apache Flink. [Fault Tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/). Accessed 2026-09-03. Primary documentation for source-position/operator-state snapshots, checkpoint barriers, aligned cuts, replay, managed-state guarantees, and sink qualification.
4. Apache Flink. [Savepoints](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/). Accessed 2026-09-03. Primary operations documentation for consistent operational state images, stable operator UIDs, restore, format, ownership, and rescale/update use.
5. Apache Flink. [State Schema Evolution](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/serialization/schema_evolution/). Accessed 2026-09-03. Primary documentation for serializer-driven value-state migration, supported type changes, and key-schema limitations.
6. Apache Flink. [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Accessed 2026-09-03. Primary operations documentation for monitoring, incremental checkpoints, timer placement, memory, local recovery, and large-state capacity.
7. Apache Beam. [Programming Guide: State and Timers](https://beam.apache.org/documentation/programming-guide/#state-and-timers). Accessed 2026-09-03. Primary documentation for per-key/window state, state primitives, event/processing timers, output timestamps, cleanup, and test considerations.
8. Apache Kafka. [Processor API, Apache Kafka 4.3](https://kafka.apache.org/43/streams/developer-guide/processor-api/). Accessed 2026-09-03. Primary documentation for state stores, source metadata, punctuation/commit, changelog restoration, window-store retention, and consequences of disabling logging.
9. Apache Kafka. [Configuring a Streams Application, Apache Kafka 4.3](https://kafka.apache.org/43/streams/developer-guide/config-streams/). Accessed 2026-09-03. Primary configuration documentation for state directories, internal naming, standby/warm-up replicas, recovery lag, and state-store suppliers.
10. Apache Spark. [TransformWithState Programming Guide](https://spark.apache.org/docs/latest/streaming/structured-streaming-transform-with-state.html). Accessed 2026-09-03. Primary documentation for arbitrary stateful processors, value/list/map state, timers, TTL, initial state, output/time modes, and value-side schema evolution.
11. Apache Spark. [State Data Source Integration Guide](https://spark.apache.org/docs/latest/streaming/structured-streaming-state-data-source.html). Accessed 2026-09-03. Primary documentation for inspecting checkpoint state, variables, timers, joins, snapshots, and change feeds for testing and investigation.

## Exercises

### Exercise 1

Records `(offset,key,event_time,delta)` are `(0,a,2,+5)`, `(1,b,4,+7)`, `(2,a,6,-2)`, `(3,a,9,+4)`. State is `(total,count,last_event,timer)` and each input replaces its key's timer with `event_time+10`. Compute state after a checkpoint whose next offset is 3, final live state, and event-time timer outputs when watermarks advance to 15 then 20 and callbacks emit `(key,total,timer)` and clear state. Explain replay from the cut.

### Exercise 2

A job has 8 million active keys. Mean serialized key is 24 bytes, value 96 bytes, index/backend estimate 80 bytes per key, and 1.5 timers per key at 32 bytes each. There are two local copies (active plus standby), three retained full-equivalent remote checkpoint copies, and a changelog whose retained compressed size is 0.6 times one logical live copy. Estimate logical live bytes and total footprint under this simplified model. List omitted amplification.

### Exercise 3

A cold restore fetches 3 TB decimal at 750 MB/s, decodes it at 600 MB/s, and must replay 360 million records at 120,000 records/s. Scheduling/coordination/warm-up/validation totals 12 minutes. Using a sequential lower-bound model, compute each term and total minutes. State why real recovery can be better or worse and how incoming rate affects convergence.

### Exercise 4

A keyed application changes from 128 to 320 parallel tasks while keeping 4,096 stable key groups. Explain what must remain invariant, what moves, how ownership is fenced, which source/state/timer/output evidence is captured, and how you test hot-group placement and rollback. Assess a simultaneous key-serialization change.

### Exercise 5

Design a migration that changes value state from `(balance_cents,last_seq)` to multi-currency `(amount_minor,currency,last_seq,policy_version)`, renames code packages, changes state backend, and tightens TTL. Include semantic compatibility, operator/state identity, savepoint versus rebuild decision, source cut, shadow comparison, timer/TTL handling, sink versions, cold restore, cutover, rollback, governance, and reconciliation.

## Answers to the Exercises

### Answer 1

Through offset 2, `a` receives +5 then -2, so its state is `(3,2,6,16)`; `b` is `(7,1,4,14)`. The checkpoint stores next offset 3 with both states/timers. Applying offset 3 gives live `a=(7,3,9,19)` and unchanged `b=(7,1,4,14)`. At watermark 15, `b`'s timer 14 fires and emits `(b,7,14)` before clearing. At watermark 20, `a`'s timer 19 emits `(a,7,19)` and clears. Restore decodes the checkpoint and replays only offset 3, reproducing the pre-timer live state when transition code, order, metadata, and dependencies match. Sink idempotency/transaction still qualifies repeated emitted effects.

### Answer 2

Per key the simplified live estimate is $24+96+80+1.5\times32=248$ bytes. One logical live copy is $8{,}000{,}000\times248=1{,}984{,}000{,}000$ bytes, or 1.984 GB decimal. Active plus standby uses 3.968 GB. Three remote full-equivalent copies use 5.952 GB. The retained changelog is $0.6\times1.984=1.1904$ GB. Total is 11.1104 GB decimal. This omits allocator/serialization headers, LSM/write/cache/bloom/index amplification beyond the estimate, filesystem/object versions, replication inside storage services, incremental ancestry, checkpoint metadata, compression variability, tombstones, hot-key tails, network buffers, and temporary compaction/restore copies.

### Answer 3

Fetch time is $3{,}000{,}000\text{ MB}/750=4{,}000$ seconds, or about 66.67 minutes. Decode time is $3{,}000{,}000/600=5{,}000$ seconds, or about 83.33 minutes. Replay is $360{,}000{,}000/120{,}000=3{,}000$ seconds, or 50 minutes. Adding 12 minutes gives a sequential lower-bound planning total of 212 minutes. Fetch/decode/replay may pipeline and parallelize, reducing the sum, while contention, skew, throttling, retries, compaction, cache misses, and validation can increase it. If new input arrives at or above sustainable replay rate, the remaining backlog does not converge; capacity must exceed incoming rate with recovery headroom.

### Answer 4

The canonical key bytes, group function, 4,096 group identities, per-key transition order, state/timer contents, source cut, and output identities remain invariant. Only the mapping from groups to 320 active task instances changes. Take a completed consistent recovery image; stop/fence old writer epochs; redistribute each group exactly once through the supported restore/rescale mechanism; restore its timers and source ownership; start new epochs; and admit output only after ownership is proven. Compare group/key counts and state digests, timer distribution, offsets, checkpoint/restore metrics, output revisions, hot-group load, and bounded-oracle results; retain the old image and routing plan for rollback. A simultaneous key-serialization change can change group assignment and identity, so it is not ordinary rescale: separate it and rebuild/rekey through an explicit migration unless the runtime proves exact compatibility.

### Answer 5

Define the new domain invariant first: currency authority, minor-unit scale, conversion prohibition or versioned rate policy, last-sequence behavior, policy version, absence, and TTL obligation. Preserve stable operator UIDs/state names despite package rename where supported; inventory both backend and serializer compatibility. If old cents are provably one currency and the runtime supports value migration plus backend restore, test an isolated savepoint conversion. Otherwise rebuild a new topology/state/output generation from an exact retained source cut, deriving currency from authoritative versioned history. Do not combine backend, serializer, TTL, and meaning changes in one untested restore. Dual-run through the same ordered cut; compare every key's balance/sequence, timers, expired/retained set, state size, outputs, and ledger totals. Give sinks versioned upsert keys and fence old/new writers. Run oldest-image cold restore and rollback after representative new writes before cutover. Tightened TTL cannot delete unresolved corrections/disputes and must propagate governed erasure to snapshots/changelogs/standbys. Cut over by named generation after domain approval, retain a compatible rollback/rebuild source horizon, and reconcile ongoing output and post-expiry cases.
