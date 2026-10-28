---
module_id: LSDS-085
program: Large-Scale Data Systems Engineering
level: 2
module_number: 85
title: Checkpoint-Based Recovery
status: complete
last_verified: 2026-09-04
---

# Checkpoint-Based Recovery

## One-Page Review

### Governing question

How can a running distributed dataflow capture a consistent, complete, durable, and compatible recovery point—covering sources, operator state, channels, coordinators, timers, and sinks—without stopping useful work, and later restore it without gaps, duplicates, mixed epochs, or broken incremental dependencies?

### Essential definitions

- A **checkpoint** is a coordinator-committed recovery snapshot of a running job at one logical epoch.
- A **consistent cut** contains process and channel state that could occur together in one valid execution.
- A **checkpoint barrier** marks an input position belonging to a checkpoint epoch.
- **aligned checkpointing** pauses channels that have received a barrier until the remaining input barriers arrive.
- **unaligned checkpointing** captures in-flight channel buffers so barriers can overtake queued records.
- A **full checkpoint** contains a self-sufficient state image; an **incremental checkpoint** references unchanged state shared with earlier checkpoints.
- A **state handle** identifies durable bytes plus size, checksum, encryption, and ownership metadata.
- A **completed checkpoint** has every required acknowledgement/handle and one durable coordinator completion record.
- **restore compatibility** maps checkpointed operator/state identity and schema to the recovering graph/runtime.
- **replay distance** is source work between the selected checkpoint and the recovery target/head.

### Central model, mechanism, or theorem

Checkpoint $C_k$ is

$$C_k=(P_k,S_k,H_k,O_k,T_k,D_k),$$

where $P_k$ are replayable source positions, $S_k$ operator/keyed state, $H_k$ captured in-flight channel state, $O_k$ operator-coordinator/timer state, $T_k$ sink transaction preparations, and $D_k$ graph/code/schema/serializer digests. It is recoverable only if every required component is complete, durable, integrity-valid, mutually consistent, and compatible, and the coordinator durably records `completed(k)`.

Recovery chooses the newest checkpoint satisfying those predicates, restores all components from the same $k$, resolves/aborts later effects, and replays sources from $P_k$. Bytes from a later incomplete checkpoint cannot be mixed in. Exactly-once managed state follows only with a consistent cut and replay; end-to-end effects additionally require transactional or idempotent sinks.

### Critical invariants

- Checkpoint ID/epoch is globally unambiguous within a stable job identity and graph version.
- Source positions, operator state, channel state, coordinator state, timers, and sink preparations all belong to the same checkpoint.
- Completion is published only after every mandatory durable handle and acknowledgement validates.
- Temporary/partial state is private and cannot be selected by recovery because files happen to exist.
- Aligned checkpoints exclude post-barrier channel records from state; unaligned checkpoints capture required in-flight buffers exactly once.
- Incremental checkpoints retain every referenced base/shared object until no live checkpoint depends on it.
- Operator IDs, key-group mapping, state names/types, serializers, code, and topology satisfy explicit compatibility rules.
- Recovery never advances source positions beyond restored state or replays from before state without duplicate-safe semantics.
- Sink transactions after the selected checkpoint are resolved by stable ID before abort, retry, or cleanup.
- Retention keeps at least the policy-required independently recoverable points and continuously verifies restorability.

### Common failures

Common failures include choosing the largest checkpoint directory; accepting local copies when the durable primary is incomplete; pairing state from checkpoint 51 with source positions from 52; marking completion before object durability; losing incremental base files during cleanup; assuming unaligned means less state; ignoring in-flight buffers or watermark/timer semantics; restoring by operator display name after topology changes; changing serializers without migration; allowing concurrent checkpoints to overwrite shared ownership; deleting externalized state on job cancellation unexpectedly; retrying a sink commit with a new identity; optimizing checkpoint duration while restore time grows; and never testing restore until an incident.

### Compact example

Checkpoints 40–43 exist. Checkpoint 41 lacks completion, 42 was written by incompatible code digest `b`, and 43 claims completion but has two of three required handles. Recovery for digest `a` selects checkpoint 40, whose source offset is 1,200 and state size 640 MiB. If the durable source head is 1,550, replay distance is 350 records. It does not combine 43's newer offset with 40's state. Sink transaction identities after 40 are reconciled before replay.

### Connections

[LSDS-043](043-stateful-operators.md) supplies managed state, [LSDS-048](048-state-snapshots-and-recovery.md) introduces snapshot mechanics, [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies replay safety, [LSDS-081](081-task-level-failure-recovery.md) supplies retry regions, [LSDS-083](083-coordinator-failure.md) supplies completion recovery, and [LSDS-084](084-lineage-based-recompute.md) supplies materialization cuts.

## Governing Question

Lineage can reconstruct immutable derived partitions, but mutable keyed/operator state may summarize years of events. Replaying from the beginning can exceed retention and RTO. A checkpoint periodically turns a distributed live computation into a durable recovery root.

No process observes a global instant directly. Records are simultaneously queued, processed, emitted, and acknowledged across channels. A valid checkpoint must capture a causally consistent cut: no recorded receive without the corresponding send, no source advancement without matching state, and no omitted in-flight record that will not replay.

The governing question is how to produce, store, complete, select, restore, migrate, retain, and verify these cuts under backpressure, asynchronous I/O, failure, rescaling, upgrades, and external sink transactions.

## Why This Matters

Checkpoint design determines data-loss and duplicate boundaries for stateful processing. A corrupt or inconsistent point may remain unnoticed for months until the primary execution fails. Frequent checkpoints reduce replay but consume network, storage, CPU, disk bandwidth, and sink coordination; infrequent ones increase recovery tails and lineage/state-log retention.

Backpressure makes aligned barriers wait behind queued data, extending duration or causing timeouts. Unaligned checkpoints bound barrier delay by persisting channel buffers, but can increase checkpoint size and restore work. Incremental/changelog methods reduce write volume while increasing dependency and cleanup complexity.

Operationally, “checkpoint succeeded” is not enough. Teams need evidence for durability domain, compatibility, restore duration, replay distance, sink outcome, retained recovery points, and practiced recovery under the actual job size and deployment version.

## Prerequisites and Retrieval

Review managed state in [LSDS-043](043-stateful-operators.md), checkpoint basics in [LSDS-048](048-state-snapshots-and-recovery.md), replay safety in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), task recovery in [LSDS-081](081-task-level-failure-recovery.md), coordinator recovery in [LSDS-083](083-coordinator-failure.md), and lineage cuts in [LSDS-084](084-lineage-based-recompute.md).

You should understand consistent cuts, happens-before, source offsets, barriers, operator/keyed state, key groups, timers/watermarks, channel buffers, copy-on-write, snapshots, incremental state, checksums, object storage, transactions, serializers, rescaling, RPO/RTO, and garbage collection.

For diagnosis retain job/graph/code digest, checkpoint ID/type/mode, trigger/barrier/ack/completion times, source positions, operator/subtask/key-group handles, channel-state bytes, coordinator/timer state, sink transaction IDs, shared-state dependency graph, checksums/encryption keys, failure reason, selected restore point, restore stages, replay distance, and cleanup history.

## Learning Objectives

After this module, you should be able to:

1. Define a checkpoint as a consistent distributed cut rather than a directory of files.
2. Trace source, operator, channel, coordinator, timer, and sink state for one epoch.
3. Compare aligned, unaligned, full, incremental, and changelog checkpointing.
4. Design durable state handles, acknowledgements, atomic completion, and cleanup.
5. Select the newest complete, integrity-valid, compatible restore point.
6. Restore state and source positions without gaps or unintended duplicates.
7. Map stable operator/state identities through rescaling and supported upgrades.
8. Tune checkpoint interval, timeout, concurrency, and retention from workload evidence.
9. Test corruption, partial completion, missing shared state, and sink ambiguity.
10. Measure checkpoint overhead and recovery effectiveness separately.

## Core Exposition

### Consistent distributed cuts

A global state combines local operator state and messages in transit. If it records a downstream state change caused by message $m$ but neither an upstream send nor channel copy of $m$, the cut is impossible. Barrier protocols establish which side of the checkpoint each record belongs to.

For replayable sources, source position is part of the cut. For stateful sinks, prepared transaction identity belongs too. Operator-coordinator state, rescaling assignments, timers, and watermarks can affect future behavior and must be included according to runtime semantics.

### Barrier propagation and alignment

Sources inject checkpoint barrier $k$ after positions $P_k$. A single-input operator snapshots after consuming its barrier and forwards it. A multi-input aligned operator blocks inputs that delivered $k$ until all barriers arrive, snapshots pre-barrier state, then resumes.

Alignment prevents post-barrier records on fast inputs from entering the pre-barrier state. Under skew/backpressure the slowest input controls duration and buffered/blocking cost. Track start delay and alignment separately from asynchronous state upload.

### Unaligned checkpoints

Unaligned mode lets barriers overtake queued buffers and includes necessary in-flight channel data in $H_k$. Recovery first restores channel contents so those records are not lost or fetched twice. This makes checkpoint duration less coupled to draining backpressure but moves bytes to checkpoint/restore I/O.

It does not solve the cause of backpressure, reduce application latency automatically, or fit every topology/runtime feature. Large unstable in-flight state can increase storage and recovery time. Validate watermark, timer, ordering, rescaling, and concurrent-checkpoint constraints for the exact runtime version.

### State backends and handles

State backend manages working state; checkpoint storage holds durable snapshots. A worker writes private state objects and returns handles containing logical owner, checkpoint, size, checksum, location/generation, encryption metadata, and shared-state references. The coordinator validates expected acknowledgements.

Local copies may accelerate restore but are secondary. Durable primary must survive required failure domains and be readable by replacement workers. Credentials and encryption keys must outlive the retention horizon or have supported rewrapping/migration.

### Full, incremental, and changelog state

Full checkpoints write a self-contained image, simplifying restore and deletion but consuming bandwidth. Incremental checkpoints reuse unchanged immutable files and write deltas; changelog approaches persist state mutations between materializations. Both reduce steady writes for large slowly changing state.

Dependency depth, random reads, compaction, shared ownership, and missing-base risk move to restore. Maintain a reference graph, not filename age. Periodic full/materialized points bound restore chains. Verify that retained checkpoints are independently restorable with their dependencies.

### Completion protocol

Coordinator assigns checkpoint ID, records trigger, gathers source/operator/channel/coordinator/sink handles, verifies completeness, and durably records completion. Only then can sources/sinks receive checkpoint-complete notifications and older state become eligible for policy-based cleanup.

A worker acknowledgement can be lost after upload; retries use checkpoint/subtask/attempt identity. Duplicate handles must be identical or rejected. Failure/timeout aborts the candidate and sink preparations, but unknown external outcomes require status lookup. Partial objects are cleaned after the completion decision is durable.

### Restore-point selection

Enumerate coordinator-completed checkpoints newest first. Check job identity, graph/operator mapping, code/runtime compatibility, state schema/serializer, key-group/parallelism mapping, every required handle and shared dependency, checksum, storage availability, encryption access, source retention, and sink status.

If one fails, record the reason and try an older policy-permitted point. Never repair a cut by mixing components from different IDs. A manual savepoint may favor portability while an automatic checkpoint favors recovery speed; honor its ownership and compatibility contract.

### Recovery sequence

Fence old execution, resolve post-checkpoint sink/commit unknowns, choose $C_k$, build compatible topology, redistribute key groups/operator state, restore coordinator/timers and channel state, set sources to $P_k$, initialize sinks with $T_k$, and start coordinated processing. Publish recovered epoch before accepting stale messages.

Measure state download/open/deserialization, scheduler/resource wait, channel restore, source seek, replay/catch-up, first output, and restored steady progress. A quick state load can still have hours of replay lag.

### Compatibility and rescaling

Assign stable operator UIDs and state names. Record key serializer/snapshot, state descriptor/type, max parallelism/key-group mapping, topology edges, union/broadcast/operator state redistribution semantics, timer format, and coordinator protocol. Display names and graph positions are brittle.

Supported schema/serializer evolution uses explicit compatibility/migration. Rescaling redistributes state by recorded mapping without changing logical ownership. Removing, splitting, or combining operators requires a declared mapping. Test both forward upgrade and rollback before deleting old-format checkpoints.

### Interval, timeout, and concurrency

Short intervals lower replay distance but can overlap, saturate storage, and prevent useful progress. Set minimum pause, maximum concurrent checkpoints, timeout, tolerable failure policy, and backpressure mode from state size/change rate, upload bandwidth, alignment, sink latency, source replay rate, and RTO/RPO.

Let checkpoint duration approach interval only with deliberate concurrency/capacity. Continuous checkpointing can create positive feedback: I/O slows processing, increases backpressure/channel state, enlarges checkpoints, and slows I/O further. Admission and circuit breakers protect the job and storage.

### Retention, ownership, and security

Retain multiple valid points across corruption and upgrade horizons, plus shared incremental dependencies and externalized/manual points under their claim policy. Cleanup is coordinator-driven, reference-aware, idempotent, and delayed past unknown uploads/commits. Cancellation policy must be explicit.

Checkpoint state may contain full sensitive records, keys, windows, timers, and source positions. Encrypt, authorize by job/tenant, isolate paths, audit reads/restores/deletes, rotate keys compatibly, and prevent path substitution. Sanitized diagnostics must not expose state payloads.

### Observability and verification

Measure triggers, completion/failure/timeout, start delay, alignment, synchronous/asynchronous duration, state/channel bytes, full/incremental ratio, upload throughput, shared-dependency depth, retained bytes/count, age/replay distance, restore-stage time, replay/catch-up, sink resolution, and RPO/RTO. Segment by operator/subtask, checkpoint mode, backend, storage, job/version, and load.

Kill tasks/coordinator during barrier, snapshot, upload, acknowledgement, completion, and notification. Corrupt/delete handles and incremental bases; throttle storage; create backpressure/skew; lose sink responses; change topology/serializer/parallelism; restore old/new versions; and race cancellation/cleanup. Compare state/output with a reference.

## Definitions and Notation

Let:

- $C_k=(P_k,S_k,H_k,O_k,T_k,D_k)$ be checkpoint $k$;
- $P_k$ be source positions and $S_k$ operator/keyed state;
- $H_k$ be in-flight channel state and $O_k$ coordinator/timer state;
- $T_k$ be sink preparations and $D_k$ compatibility digests;
- $B_s,B_h,B_i$ be operator, channel, and incremental-delta bytes;
- $t_k$ be trigger time and $c_k$ durable completion time;
- $A_k$ be alignment duration and $U_k$ asynchronous upload duration;
- $p_k$ be source position and $p_h$ recovery-time head;
- $R_k=p_h-p_k$ be replay distance in source-specific units;
- $G_I$ be the incremental shared-state dependency graph;
- $RPO$ and $RTO$ be recovery objectives under named failure domains.

Checkpoint duration $c_k-t_k$ is not restore time. Bytes need categories and compressed/uncompressed labels. Replay distance can be records, offsets, event time, or bytes and cannot be compared without source semantics. Completion rate needs triggers as denominator and a time window.

## Mechanisms, Invariants, or Proof Structure

### Consistent-cut proof

For aligned barriers, each operator snapshots after all inputs reach barrier $k$, so pre-barrier records are reflected in state and post-barrier records are excluded and will replay after $P_k$. For unaligned barriers, records overtaken by the barrier are included exactly in $H_k$. Assuming reliable barrier/channel bookkeeping, the combined local/channel state forms a valid cut.

### Atomic-completion proof

Every required component writes private immutable state and acknowledges a validated handle. Coordinator durably publishes `completed(k)` only after the complete set exists. Recovery selects only published complete IDs. Therefore a crash before publication exposes no selectable partial checkpoint, while a crash after publication leaves one durable recovery root.

### Restore-equivalence proof

Restore all components of $C_k$, seek sources to $P_k$, and replay under matching $D_k$. The consistent-cut proof ensures every input effect is either represented in restored state/channel/sink preparation or replayed, but not omitted. Deterministic processing reconstructs equivalent managed state; sink exactly-once needs its transaction protocol.

### Incremental-retention proof

Treat each checkpoint as roots in shared-state graph $G_I$. An object is deletable only when its reference count from every retained/completing/unknown checkpoint is zero and no active restore lease exists. Removing only zero-reachable objects preserves all retained restore chains. Age alone cannot prove this.

### Adversarial verification

Test empty/large state, no/one/many inputs, alignment skew, huge channel buffers, task/coordinator crash at each phase, duplicate/lost acknowledgements, partial/corrupt handle, missing base, source retention gap, sink unknown, topology/serializer change, rescale, key loss, cleanup race, and old-version restore. Require exact state/effects or explicit rejection/fallback.

## Alternatives and Trade-Offs

**Aligned checkpoints** minimize captured channel state and give straightforward cuts but can stall under backpressure. **Unaligned checkpoints** reduce alignment sensitivity but capture more in-flight data and add restore/compatibility complexity.

**Full snapshots** simplify independence and restore. **Incremental/changelog snapshots** reduce writes but add dependency graphs, compaction, and potentially longer restore. Periodic full cuts bound risk.

**Frequent checkpoints** reduce replay and RPO but increase interference. **Infrequent checkpoints** lower write overhead but increase recovery tail and retained source requirements.

**Automatic checkpoints** optimize routine recovery and lifecycle. **Savepoints/externalized checkpoints** support operations and user-controlled retention but may have different portability, ownership, and performance.

**Local recovery copies** reduce network restore on surviving hosts. **Distributed primary state** survives node loss/rescaling. The former cannot replace the latter for durable guarantees.

## Failure Modes and Misconceptions

1. **Checkpoint is a folder.** It is a completed coordinator decision over a consistent component set.
2. **Largest numeric ID is safest.** It may be incomplete or incompatible.
3. **Uploaded bytes mean complete.** Every required handle and completion record matter.
4. **Mixing IDs gets the newest state.** It creates an impossible cut.
5. **Source offset alone is recovery.** Operator and sink state must correspond.
6. **Aligned means no buffering.** Channels and operators still buffer; barriers coordinate the cut.
7. **Unaligned removes backpressure.** It changes snapshot behavior, not the cause.
8. **Unaligned is always smaller/faster.** In-flight bytes can be large.
9. **Incremental checkpoint is independently complete.** It may need shared bases.
10. **Old objects are unreferenced.** Retained descendants may depend on them.
11. **Local state is durable primary.** Node loss can remove it.
12. **Operator names are stable IDs.** Topology refactors break them.
13. **Serializer changes are automatic.** Compatibility/migration is explicit.
14. **More frequent always improves recovery.** Interference may prevent completion.
15. **Checkpoint duration equals RTO.** Resource wait, restore, and replay add time.
16. **Exactly-once means one execution.** Replay physically reprocesses records.
17. **Managed-state exactly-once covers HTTP effects.** Sinks need separate guarantees.
18. **A successful checkpoint is proven restorable.** Only restore tests prove the path.

## Worked Examples

### Example 1

State reflects source offset 1,000 but restored source starts at 1,200. Records 1,001–1,200 are skipped. Pairing positions and state by checkpoint ID prevents this.

### Example 2

Fast input receives barrier 8 while slow input has queued records. Alignment blocks fast input until slow barrier arrives, keeping post-barrier records out of checkpoint-8 state.

### Example 3

Under heavy backpressure, unaligned checkpoint captures 12 GiB of channel buffers. Completion is quicker, but restore must read and replay those buffers before new input.

### Example 4

Incremental checkpoints 50–53 share base file `x`. Deleting `x` because checkpoint 50 expired breaks 51–53; reference reachability keeps it.

### Example 5

Checkpoint 60 has 99 of 100 subtask handles. Its directory is large and recent but unselectable. Recovery uses complete checkpoint 59.

### Example 6

Operator display name changes while stable UID remains. State maps successfully. Reusing the UID for different semantics would be corrupt and must fail compatibility.

### Example 7

Parallelism changes from 4 to 8 under constant max parallelism. Key groups redistribute deterministically; arbitrary state-file splitting would not preserve ownership.

### Example 8

Checkpoint upload response is lost. Worker retries the same subtask/checkpoint identity; identical handle is accepted rather than counted twice.

### Example 9

Sink transaction after checkpoint 70 may have committed. Recovery looks it up by transaction ID before abort/replay, preventing duplicate external output.

### Example 10

The executable fixture selects the newest complete compatible checkpoint and calculates replay distance.

<!-- bijux-verify: {"id":"checkpoint-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selected_checkpoint=40\nsource_offset=1200\nstate_mib=640\nreplay_records=350\nrejected=41:incomplete,42:incompatible,43:missing-handles\n","stderr":""}} -->
```python
checkpoints = [
    {"id": 40, "complete": True, "digest": "a", "handles": 3, "required": 3, "offset": 1200, "mib": 640},
    {"id": 41, "complete": False, "digest": "a", "handles": 3, "required": 3, "offset": 1300, "mib": 650},
    {"id": 42, "complete": True, "digest": "b", "handles": 3, "required": 3, "offset": 1400, "mib": 660},
    {"id": 43, "complete": True, "digest": "a", "handles": 2, "required": 3, "offset": 1450, "mib": 670},
]
required_digest = "a"
rejected = []
selected = None
for checkpoint in reversed(checkpoints):
    if not checkpoint["complete"]:
        rejected.append(f'{checkpoint["id"]}:incomplete')
    elif checkpoint["digest"] != required_digest:
        rejected.append(f'{checkpoint["id"]}:incompatible')
    elif checkpoint["handles"] != checkpoint["required"]:
        rejected.append(f'{checkpoint["id"]}:missing-handles')
    else:
        selected = checkpoint
        break

print(f'selected_checkpoint={selected["id"]}')
print(f'source_offset={selected["offset"]}')
print(f'state_mib={selected["mib"]}')
print(f'replay_records={1550 - selected["offset"]}')
print(f'rejected={",".join(reversed(rejected))}')
```

## Cross-Program Connections

- **Distributed systems:** consistent cuts, barriers, causality, durable commits, and failure domains define snapshot safety.
- **Database systems:** WAL, checkpoints, MVCC snapshots, recovery, and transaction prepare/commit provide analogous mechanisms.
- **Streaming:** source offsets, keyed state, timers, watermarks, channel buffers, and sink commits form the cut.
- **Storage:** copy-on-write, incremental files, checksums, encryption, retention, and throughput determine durability.
- **Scheduling:** key-group placement, restart regions, resource wait, and local recovery determine restore time.
- **Schema engineering:** stable IDs, serializer snapshots, migrations, and rollback preserve compatibility.
- **Security:** state confidentiality, scoped access, key lifetime, audit, and deletion protect checkpoint contents.
- **Reliability engineering:** RPO/RTO, fault injection, restore drills, percentile stages, and dependency capacity prove readiness.

## References

1. Chandy and Lamport, [Distributed Snapshots: Determining Global States of a Distributed System](https://research.cs.wisc.edu/areas/os/Qual/papers/snapshots.pdf). 1985. Defines consistent global cuts and channel-state capture.
2. Apache Flink, [Fault Tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/). Current. Explains source positions, operator state, checkpoint recovery, and exactly-once boundaries.
3. Apache Flink, [Stateful Stream Processing](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/concepts/stateful-stream-processing/). Version 2.3. Describes barriers, aligned/unaligned snapshots, and restore.
4. Apache Flink, [Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/). Current. Documents interval, timeout, concurrency, retention, and unaligned controls.
5. Apache Flink, [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Current. Covers alignment, local recovery, incremental state, and large-state operation.
6. Apache Flink, [Monitoring Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/monitoring/checkpoint_monitoring/). Current. Defines checkpoint status, duration, alignment, bytes, and subtask evidence.
7. Apache Flink, [Savepoints](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/). Current. Documents operator identity, restore mapping, ownership, and claim modes.
8. Apache Spark, [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html). Current. Documents checkpointed progress/state and restart semantics.
9. Apache Spark, [State Data Source](https://spark.apache.org/docs/latest/streaming/structured-streaming-state-data-source.html). Current. Documents inspection of committed checkpoint state and metadata.
10. Apache Kafka, [Running Streams Applications](https://kafka.apache.org/documentation/streams/developer-guide/running-app/). Current. Documents task migration and state restoration from changelog topics.
11. Apache Kafka, [Processor API](https://kafka.apache.org/documentation/streams/developer-guide/processor-api/). Current. Documents persistent state stores, changelogs, and restoration.
12. RocksDB, [Checkpoints](https://github.com/facebook/rocksdb/wiki/Checkpoints). Current. Documents consistent database snapshots using shared immutable files.
13. Google Cloud Dataflow, [Exactly-once in streaming](https://cloud.google.com/dataflow/docs/concepts/exactly-once). Current. Describes replay, state, deduplication, and external side-effect boundaries.

## Exercises

### Exercise 1

Explain why operator state from checkpoint 20, source offsets from 21, and sink preparation from 19 do not form a valid “best available” restore point.

### Exercise 2

Compare aligned and unaligned checkpoint behavior for a two-input join under sustained backpressure, including snapshot bytes, processing pause, restore, and correctness.

### Exercise 3

Design completion and cleanup for incremental checkpoints that share immutable state files while acknowledgements can be duplicated or lost.

### Exercise 4

Design an upgrade from parallelism 8 to 16 with serializer evolution. State identities, compatibility gates, rollback, and validation must be explicit.

### Exercise 5

Design a restore drill and dashboard proving the latest retained checkpoint is usable and meets a 15-minute RTO.

## Answers to the Exercises

### Answer 1

The state may already reflect records beyond checkpoint 20 while the source position can skip or replay a different set, and the sink preparation belongs to yet another transaction frontier. There is no proof these components coexist in one causal execution, so gaps or duplicates are possible. Select one coordinator-completed checkpoint ID whose source, operator/channel/coordinator state, and sink metadata all validate; otherwise fall back intact or fail explicitly.

### Answer 2

Aligned mode blocks the fast input after its barrier until the slow barrier arrives, snapshots operator state without overtaken post-barrier channel records, and usually writes fewer channel bytes; alignment delay and backpressure can dominate. Unaligned mode captures queued in-flight buffers, lets barriers pass, and may complete predictably while writing more bytes. Restore must load those buffers and process them before/with upstream replay according to runtime rules. Both can produce a consistent cut when implemented correctly; unaligned changes the performance location and compatibility constraints, not the required result semantics or root backpressure.

### Answer 3

Write attempt-private immutable files, identify each by content/generation/checksum, and return idempotent handles keyed by checkpoint/operator/subtask/attempt. Coordinator accepts identical duplicate acknowledgements, rejects conflicting ones, and publishes completion only after every required handle and dependency validates. Maintain durable references from completing, completed, retained, unknown, and actively restoring checkpoints. On abort/expiry, remove that root; delete a shared object only at zero reachability after leases and safety delay. Unknown acknowledgements/uploads reconcile before cleanup, and periodic restore verification detects missing bases.

### Answer 4

Use stable operator UIDs/state names and constant compatible max parallelism/key-group mapping. Persist serializer snapshots and require the new serializer to report compatible-as-is or execute a tested migration; reject incompatible state. Create and validate a retained checkpoint/savepoint under the old version, restore a canary at 16, verify every key group exactly once, timers/watermarks, state/output equivalence, and sink continuity, then cut over with fenced old execution. Keep old code and recovery point through rollback window; do not write an irreversible new format until rollback policy accepts it.

### Answer 5

Continuously validate handle count, checksums, shared dependencies, source retention, code/serializer compatibility, keys, and sink transaction state. In an isolated environment fence production effects, allocate production-like resources, restore the latest point, replay/catch up against a pinned source, and compare managed state and outputs with reference invariants. Inject one missing latest handle to prove fallback. Time election/resource wait, download/open/deserialization, channel/state initialization, source seek, replay, first output, and steady-progress restoration; end-to-end must be at most 15 minutes. Dashboard checkpoint age/distance, completion failures, bytes/dependency depth, restore stages, fallback count, unknown sinks, and achieved RPO/RTO.
