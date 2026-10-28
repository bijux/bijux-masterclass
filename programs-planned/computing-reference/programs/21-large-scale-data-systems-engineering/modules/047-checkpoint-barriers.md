---
module_id: LSDS-047
program: Large-Scale Data Systems Engineering
level: 1
module_number: 47
title: Checkpoint Barriers
status: complete
last_verified: 2026-09-04
---

# Checkpoint Barriers

## One-Page Review

### Governing question

How can a continuously running distributed dataflow identify one recoverable logical cut across many sources, channels, and stateful operators without stopping all useful work or mixing records from incompatible sides of the cut?

### Essential definitions

- A **checkpoint** is a coordinated recoverable image pairing source positions, operator state, timers, and required channel/effect metadata for one logical input prefix.
- A **barrier** is an ordered control marker carrying checkpoint identity through a dataflow channel; it separates records before the cut from records after it.
- A **consistent cut** never contains an effect without the causal input needed to explain it and records channel state required by the snapshot model.
- **barrier alignment** waits at a multi-input operator until the same checkpoint barrier has arrived on every relevant input, withholding post-barrier records from early channels.
- An **aligned checkpoint** snapshots operator state after all pre-barrier input and before any post-barrier input for that checkpoint.
- An **unaligned checkpoint** lets barriers overtake queued records and includes necessary in-flight channel data in the checkpoint instead of waiting for drain/alignment.
- A **checkpoint epoch/ID** distinguishes concurrent or successive cuts and prevents markers, acknowledgments, and state handles from being mixed.
- An **acknowledgment** says one participant's snapshot material is durably available under the protocol; it is not global completion.
- A **completed checkpoint** is one the coordinator has atomically declared usable after all required acknowledgments and metadata are durable.
- **barrier skew** or **alignment duration** is the delay between the first and last relevant input barrier at an operator.

### Central model, mechanism, or theorem

For checkpoint $n$, source $s$ records next position $p_{s,n}$ and emits barrier $B_n$ after all records in the selected prefix on each output channel. At multi-input operator $o$, an aligned protocol processes ordinary records until $B_n$ arrives on an input; it then withholds that input's post-$B_n$ records while continuing pre-$B_n$ records from other inputs. When every relevant input has delivered $B_n$, it snapshots state $S_{o,n}$, forwards $B_n$, and releases withheld data.

The completed image

$$C_n=(\{p_{s,n}\},\{S_{o,n}\},\{T_{o,n}\},\{Q_{c,n}\},M_n)$$

contains source positions, operator state, timers, channel state $Q$ when the algorithm requires it, and integrity/topology/version metadata $M_n$. Aligned checkpoints make relevant $Q$ empty at the cut by waiting; unaligned checkpoints persist $Q$ explicitly. Neither is valid until all required components are durably committed under one checkpoint ID.

### Critical invariants

- Barriers and records share an ordering contract per channel; a barrier cannot silently overtake data unless overtaken data is captured as channel state.
- Every source position, operator/timer image, channel-state segment, acknowledgment, and manifest belongs to exactly one checkpoint identity and topology epoch.
- A multi-input snapshot contains every relevant pre-barrier record and no uncaptured post-barrier record.
- Input blocking/alignment changes scheduling, not the logical prefix represented by the checkpoint.
- Asynchronous persistence operates on a stable logical state version while live processing mutates a newer version.
- Partial, timed-out, canceled, corrupt, or incompletely uploaded checkpoints never become recovery truth.
- Completion publication is atomic and references content whose integrity and durability have been verified.
- Restore uses source positions, state, timers, and channel data from the same completed checkpoint.
- Managed-state exactly-once does not imply exactly-once external effects; sinks need transaction, idempotency, deduplication, or fencing.
- Barrier start delay, alignment duration, snapshot/upload time, channel-state bytes, completion age, failures, and recovery are observable and bounded.

### Common failures

Common failures include treating a barrier as a data record that may reorder; snapshotting on the first input barrier; blocking all inputs instead of only early ones; processing early-channel post-barrier data during alignment; forgetting buffered/channel state; mixing source offsets from one checkpoint with operator state from another; publishing completion before uploads are durable; restoring partial local files; allowing stale attempts to acknowledge; assuming asynchronous snapshot means inconsistent state; using unaligned checkpoints to hide persistent backpressure; confusing checkpoint barriers with watermarks; assuming completed managed state includes API calls; and setting intervals shorter than sustainable checkpoint work until the job checkpoints continuously.

### Compact example

Left input delivers `L1, B7, L2`; right delivers `R1, R2, B7, R3`. An aligned operator processes `L1,R1`, sees the left barrier, withholds `L2`, continues right and processes `R2`, then sees the right barrier. Snapshot 7 contains state after `L1,R1,R2`—all pre-barrier records—and none of `L2,R3`. It then forwards `B7` and releases `L2`. Snapshotting at the first barrier would omit pre-barrier `R2`; processing `L2` before the last barrier would mix the right prefix with left post-cut data.

### Connections

[LSDS-041](041-logs-as-distributed-input.md) and [LSDS-042](042-partitioned-consumption.md) define replayable positions and ownership. [LSDS-043](043-stateful-operators.md) defines state/timers; [LSDS-045](045-watermarks.md) shows why event-time progress is a different frontier. [LSDS-048](../ROADMAP.md) develops snapshot storage/restore, [LSDS-049](../ROADMAP.md) backpressure, and [LSDS-050](../ROADMAP.md) effect-safe replay.

## Governing Question

A stateful streaming job changes continuously. Sources advance offsets, operators mutate keyed state, timers appear and disappear, and records occupy network queues. Copying each component whenever convenient can create an impossible global state: a downstream count may include a record while the restored source position causes it to replay, or an upstream state may reflect an output absent from downstream state and channel data.

Stopping every source and worker, draining every channel, copying all state, and restarting could create a cut, but pause time grows with state and topology. Checkpoint barriers instead move a logical boundary through the graph. Each operator identifies which records belong before and after one numbered cut while state bytes may be persisted asynchronously.

Multi-input operators are the crux. A barrier reaches a fast channel before a slow one. The operator must continue consuming slow-channel records that precede its barrier while preventing fast-channel records after its barrier from contaminating the snapshot. Alignment performs that separation by waiting. Unaligned protocols record in-flight data so the barrier need not wait behind congestion.

The governing question is how to preserve a consistent cut through channel ordering, alignment or channel capture, durable completion, cancellation, recovery, topology change, and external effects—and how to detect when checkpointing itself becomes the system's bottleneck.

## Why This Matters

Without a consistent checkpoint, replay can double-apply or skip state transitions. A balance may be debited twice, a dedup set may forget IDs whose source offsets were committed, or a join may restore one side later than the other. Failures then turn an apparently healthy pipeline into durable data corruption.

Checkpoint latency determines recoverability. If checkpoints time out for hours, the nominal recovery point is stale and recovery must replay a huge backlog. If checkpoint I/O consumes all headroom, backpressure delays barriers further, creating a feedback loop. Aligned barriers expose congestion through start and alignment delays; unaligned checkpoints trade waiting for channel-state bytes and recovery work.

Barrier design also affects latency. Blocking an early input during alignment propagates backpressure upstream. Large records or long user callbacks can delay barrier handling. Concurrent checkpoints multiply state versions, uploads, metadata, and failure paths. A “one-second checkpoint interval” is meaningless if each checkpoint takes two minutes.

Finally, a checkpoint is not a universal transaction. It can make engine-managed state consistent with replayable sources, but a message, email, charge, or database write may already be visible. End-to-end correctness requires the effect protocol to participate or tolerate replay.

## Prerequisites and Retrieval

Review source positions and immutable record identity in [LSDS-041](041-logs-as-distributed-input.md), partition assignment/fencing in [LSDS-042](042-partitioned-consumption.md), state/timer durability in [LSDS-043](043-stateful-operators.md), watermark progress in [LSDS-045](045-watermarks.md), and window/trigger state in [LSDS-046](046-window-assignment-and-triggers.md).

You should understand directed dataflow graphs, FIFO channels and their alternatives, causal order, consistent cuts, replayable logs, epochs, copy-on-write/versioned state, durable object storage, hashes/manifests, backpressure, transactions, idempotency, and failure detection.

## Learning Objectives

After this module, you should be able to:

1. define a checkpoint as one consistent cut over positions, state, timers, channel data, and metadata;
2. trace numbered barriers through sources, one-input, multi-input, fan-out, and sink operators;
3. prove why aligned multi-input processing includes every pre-barrier record and excludes post-barrier records;
4. compare aligned, unaligned, and at-least-once/nonaligned mechanisms and their state/latency consequences;
5. separate synchronous logical snapshot work from asynchronous serialization/upload and atomic completion;
6. handle concurrent checkpoints, timeouts, cancellation, stale attempts, partial uploads, and corruption;
7. distinguish checkpoint, savepoint, watermark, source commit, and external transaction semantics;
8. estimate checkpoint interval, barrier delay, alignment buffering, state upload, retention, and recovery cost;
9. secure checkpoint control/data planes and protect tenant/state confidentiality; and
10. validate consistent cuts, restore, external effects, and checkpoint liveness under adversarial failures.

## Core Exposition

### Start with the recoverable cut

Write exactly what recovery needs: source next positions; each operator's state and timers after the corresponding admitted prefix; channel contents when the algorithm includes them; topology, operator/state/schema, serializer, and code identity; and sink transaction/effect metadata. This tuple, not “some files,” is the checkpoint.

Define the cut in half-open position terms. If position 500 is the next source record, state reflects records before 500. Document whether source acknowledgments/commits are recovery metadata or merely retention hints.

Every component carries checkpoint ID and attempt/topology epoch. Never infer membership from directory time or latest-file naming.

### Inject barriers at coordinated sources

A coordinator begins checkpoint $n$. Each source records its position and emits $B_n$ after the chosen prefix on every relevant output. Sources may need a coordinator protocol so positions across partitions identify one intended checkpoint even though wall-clock injection times differ.

The source must be replayable from the recorded position and must order barrier relative to emitted records. A connector that acknowledges upstream data before durable recovery metadata is safe only if upstream retention still covers the checkpoint.

Dynamic split discovery, finished sources, and reassignment require explicit participation rules. A source cannot disappear midway without the coordinator resolving whether its component is required.

### Preserve channel order

Aligned barriers rely on a channel property: ordinary records emitted before $B_n$ arrive before it, and records emitted after arrive after it. If the transport can reorder control and data, add sequence numbers/reorder buffers or use another snapshot algorithm.

Fan-out must place the barrier after the same logical upstream prefix on each output. Union/merge retains distinct input identities until alignment. Network retries cannot duplicate/drop a barrier without checkpoint-ID deduplication and recovery behavior.

Large record processing is atomic relative to barrier handling under many runtimes; a barrier waits until the current callback completes. Bound record size and callback duration.

### Snapshot one-input operators

A one-input operator processes records in channel order. On $B_n$, all earlier records are in state and later records have not been processed. It takes a logical snapshot, forwards $B_n$ after the runtime's required ordering, and resumes.

“Takes a snapshot” need not mean synchronously writing every byte. It may capture a version/root/handle, rotate a changelog, or freeze copy-on-write pages quickly, then serialize/upload asynchronously. The logical image must remain stable while live state advances.

If snapshot initiation fails, do not forward a success-implying barrier or acknowledgment. Propagate cancellation under the protocol.

### Align multi-input operators

When the first $B_n$ arrives, mark that input aligned and stop processing its later records for checkpoint $n$. Continue other inputs, because their remaining pre-$B_n$ records belong inside the cut. When all relevant barriers arrive, snapshot state, forward $B_n$, and release blocked channels.

Blocking can happen at network consumption rather than copying records into application memory. Buffers fill and backpressure moves upstream. Alignment duration is the interval from first to last barrier, while start delay measures how long the first barrier took to reach the operator after triggering.

Snapshotting on the first barrier misses causal pre-cut work on slow inputs. Processing post-barrier fast data mixes cuts. Blocking every input on the first barrier deadlocks or omits remaining pre-barrier traffic.

### Prove the aligned cut

For each FIFO input, the barrier partitions its sequence into prefix and suffix. Before receiving the barrier, the operator processes only prefix records. After receiving it on an early channel, blocking prevents suffix processing. Continuing unmarked inputs consumes their prefixes until their barriers.

Therefore at the last barrier the state includes all processed input prefixes and no suffix. Any outputs/state transitions causally produced by those prefixes are included according to operator atomicity. Forwarding the barrier after logical snapshot preserves the partition downstream.

The proof assumes FIFO/control ordering, deterministic ownership, atomic record transition relative to the barrier, complete input membership, and correctly managed hidden asynchronous work.

### Track asynchronous work

An operator can launch an RPC and receive $B_n$ before its callback. If the RPC result may mutate state or emit for a pre-barrier record, the cut must wait, snapshot the request/result continuation, or use a transactional/idempotent replay design. Ignoring it violates the prefix proof.

Mailbox/task models often serialize callbacks with barriers; thread pools and user futures can escape that protection. Inventory every queue, timer, batch, GPU task, subprocess, and connector buffer.

Backpressure inside one long callback delays even unaligned barriers because the operator cannot snapshot midway through an unmodeled transition.

### Understand at-least-once nonalignment

If a multi-input operator snapshots on barriers without withholding fast post-barrier records, state can include records beyond one source's recorded prefix. Recovery rewinds sources and may replay those transitions. With rollback rules and replayable input, loss is avoided but duplicates can appear in state/output unless transitions/effects deduplicate.

This can reduce alignment latency, but it is a semantic choice. Label managed state and external effects separately. Some runtimes call modes “at least once” while exact connector behavior still matters.

Do not describe disabled alignment as equivalent exactly-once with better performance.

### Capture unaligned channel state

Unaligned checkpointing lets barriers move ahead of queued in-flight records instead of draining them. To retain a consistent recovery image, it snapshots input/output channel buffers and their ordering plus operator state. On restore, captured channel data is replayed in the required place.

This bounds barrier delay under backpressure but increases checkpoint bytes roughly with in-flight buffered data, adds I/O and restore work, and complicates compatibility. It is attractive when alignment delay dominates and checkpoint storage has headroom; it is harmful when storage bandwidth is the bottleneck.

Buffer debloating can reduce in-flight bytes for both aligned latency and unaligned checkpoint size. Neither technique cures the root cause of sustained backpressure.

### Keep watermarks separate

Watermarks are event-time progress claims; checkpoint barriers are recovery-cut markers. A watermark can pass many times between checkpoints. A checkpoint may complete while event-time progress is stalled. Neither implies the other is correct.

Ordering both control events with data matters. Unaligned recovery can restore channel data and regenerate watermarks in a runtime-specific order, affecting operators that consult “current watermark” on each record. Persist required watermark-dependent state or avoid such implicit coupling, and test the selected runtime/version.

### Coordinate timers and windows

Managed event/processing timers and window trigger state are part of the logical operator snapshot. A timer registered by a pre-barrier record belongs in the checkpoint; a post-barrier timer does not unless captured in channel/replay semantics.

After restore, overdue processing timers may fire promptly and event timers depend on restored/regenerated watermark progress. Timer callbacks and pane outputs need stable identity because recovery can repeat external effects.

Large timer firings can delay barrier handling and cause bursty checkpoints. Measure callback duration and coalesce timer state.

### Publish completion atomically

Each task uploads durable state/channel handles, verifies integrity, and acknowledges checkpoint $n$ under its current attempt/epoch. The coordinator waits for every required participant and sink preparation, then durably publishes one completed manifest/pointer.

Before that publication, $n$ is incomplete and cannot be selected for ordinary recovery. The manifest references immutable objects with lengths/hashes/encryption metadata and source/topology/schema identities. Publishing a pointer before objects are durably readable creates a phantom checkpoint.

Garbage collection retains dependencies of completed incremental checkpoints and never deletes the last viable recovery point during replacement.

### Handle cancellation and timeout

Failure, timeout, subsumption, topology change, or coordinator decision can cancel a checkpoint. Cancellation unblocks aligned channels, releases snapshot resources, aborts prepared sink transactions when required, and eventually reclaims orphan uploads.

Late acknowledgments from canceled or old task attempts are rejected by checkpoint and attempt identity. Cancellation signals themselves are idempotent; a participant may see them after local failure.

A timeout shorter than normal tail duration creates churn; an infinite timeout permits permanent stalls. Choose from measured distributions and recovery-point objectives.

### Limit concurrency

Concurrent checkpoints can improve opportunity when one upload is slow, but multiply frozen state versions, network/storage I/O, manifests, sink transactions, and operator logic for interleaved barriers. Barriers for checkpoint $n+1$ must not be confused with $n$.

Some modes restrict concurrency, especially unaligned implementations. Respect runtime version constraints. Configure minimum pause so continuous long checkpoints do not monopolize resources.

Backlogs require a separate interval or disabling policy only with an explicit recovery-risk decision; staleness grows while checkpointing is paused.

### Connect sinks and effects

A transactional sink can prepare writes as part of checkpoint $n$ and commit after global completion, aborting on failure. An idempotent sink can use stable record/result/checkpoint identity. A deduplicating consumer can reject repeats within a durable horizon. An outbox can couple local state and effect intent.

No barrier can roll back an already-sent email or arbitrary API call. Defer irreversible actions until a safe commit point when possible, or design business-level idempotency/compensation.

Exactly-once managed state commonly means each logical input affects restored engine state once, even though physical execution may replay it.

### Size the checkpoint pipeline

Separate synchronous snapshot initiation, barrier start delay, alignment duration, asynchronous serialization, upload, task acknowledgment, coordinator completion, and end-to-end duration. The maximum/critical path, not average task time, controls global completion.

Estimate full/incremental state, timers, channel buffers, manifests, compression/encryption CPU, storage requests, bandwidth, replication, retained checkpoints, concurrent versions, and restore throughput. Incremental snapshots reduce changed bytes but add dependency/compaction and small-file considerations.

Ensure the system can process input plus checkpoint overhead plus post-failure catch-up. Steady operation at 100% utilization cannot recover a backlog.

### Observe barriers and completion

Measure trigger-to-first-barrier delay, first-to-last alignment duration by task/input, sync/async snapshot time, bytes by state/channel, upload rate, acknowledgments, global duration, completed-checkpoint age, failures/timeouts/cancellations, and orphan cleanup.

Correlate with busy/backpressured/idle time, buffers, input skew, record/callback duration, state growth, storage latency/throttling/errors, GC/CPU/disk/network, sink prepare/commit, and topology events.

Trace checkpoint ID through coordinator, sources, barriers, operators, storage handles, sink transaction, completion manifest, retention, and restore without exposing sensitive state paths or credentials.

### Secure checkpoint control and data

Authenticate coordinator/task/source/sink participants; authorize trigger, cancel, retention, restore, and delete operations. Fence stale attempts and validate topology membership. A forged barrier or acknowledgment can manufacture an inconsistent cut or denial of service.

Encrypt state and channel data in transit/at rest with managed keys. Avoid secrets/credentials in state where possible; protect manifests, object paths, hashes, and metrics that reveal tenant activity. Enforce tenant/region boundaries during storage and restore.

Validate length/hash/format/schema before restore, and audit exceptional “ignore corrupted channel state” actions as explicit data-loss decisions.

### Validate with fault injection

Inject crashes before/after barrier receipt, logical snapshot, upload, acknowledgment, global completion, sink prepare, sink commit, and source-position persistence. Delay one input, reorder only where transport permits, fill buffers, run long callbacks, lose workers/storage/coordinator, cancel checkpoints, and restore the last completed one.

Compare recovered state/output with a reference execution over the declared prefix. Test duplicates/skips, timer/pane identity, partial/corrupt objects, incremental dependencies, stale acknowledgments, concurrent checkpoint IDs, rescale, upgrade, and key/region policy.

Test aligned and unaligned modes under representative backpressure and restore, not only happy-path completion.

## Definitions and Notation

Let dataflow sources be $s\in\mathcal{S}$, operators $o\in\mathcal{O}$, and channels $c\in\mathcal{E}$. Checkpoint $n$ has marker $B_n$, source next position $p_{s,n}$, operator state $S_{o,n}$, timer state $T_{o,n}$, channel state $Q_{c,n}$ when required, and metadata $M_n$.

The checkpoint image is $C_n=(\{p\},\{S\},\{T\},\{Q\},M)$. A completed predicate requires every mandatory component and an atomically durable completion record; component existence alone is insufficient.

For multi-input operator $o$, $I_o$ is its relevant input set and $A_{o,n}\subseteq I_o$ inputs on which $B_n$ has arrived. Alignment completes when $A_{o,n}=I_o$. If first and last barrier arrive at processing times $f_{o,n}$ and $l_{o,n}$, alignment duration is $l_{o,n}-f_{o,n}$.

Let $R_{c,n}^{pre}$ and $R_{c,n}^{post}$ be channel records before and after $B_n$. An aligned state transition includes every $R^{pre}$ and no $R^{post}$. An unaligned image may store an ordered portion of in-flight $R$ in $Q_{c,n}$ so restore reconstructs the same cut.

## Mechanisms, Invariants, or Proof Structure

Audit checkpoint barriers in this order:

1. **Recovery contract:** enumerate source, operator, timer, channel, topology/version, and sink-effect components.
2. **Source cut:** prove recorded next positions and emitted barriers delimit the same prefix.
3. **Channel order:** verify record/barrier FIFO or explicitly capture/reconstruct overtaken data.
4. **Operator atomicity:** place each record transition and asynchronous continuation wholly on one side.
5. **Multi-input cut:** align early inputs or persist channel state; prove all prefixes and no uncaptured suffixes.
6. **Logical snapshot:** freeze/version state and timers before asynchronous persistence mutates their image.
7. **Durability/completion:** verify handles, acknowledgments, attempt fencing, manifest integrity, and atomic global publication.
8. **Effects:** coordinate transactional preparation/commit or prove replay-safe idempotency/deduplication/compensation.
9. **Lifecycle/capacity:** bound interval, concurrency, delay, alignment, bytes, retention, cancellation, cleanup, and restore/catch-up.
10. **Evidence:** fault-inject every boundary and compare recovery with the declared reference prefix.

The aligned proof follows channel partitioning: FIFO makes every record before $B_n$ a prefix member. Blocking a marked input excludes its suffix; consuming unmarked inputs includes their remaining prefixes. At the last barrier, logical state is exactly the product cut, subject to atomic transitions and tracked asynchronous work.

Unaligned equivalence replaces empty-at-cut channels with durable ordered channel state. Its proof additionally requires captured buffers be complete, nonduplicated, integrity-checked, and replayed in the correct topology/order.

Global completion safety follows only after every required durable handle is referenced by one atomic manifest and sink/source participants agree on checkpoint identity. Local acknowledgment is not transitive proof of global completion.

## Alternatives and Trade-Offs

**Aligned exactly-once checkpoints** minimize channel-state bytes and offer a simple cut, but backpressure/skew can delay barriers and block fast inputs. **Unaligned checkpoints** bound propagation by capturing in-flight data, increasing I/O, storage, restore, and compatibility complexity. **At-least-once nonalignment** reduces waiting but permits replayed state/output effects.

**Synchronous full snapshots** simplify ownership but pause processing. **Asynchronous versioned snapshots** reduce pause while retaining old versions, copy-on-write/changelog, memory, and failure complexity.

**Full checkpoints** are independently readable but move all state. **Incremental checkpoints** move changes and share prior objects, reducing bytes while complicating dependency retention, compaction, integrity, and deletion.

**Frequent checkpoints** reduce replay/recovery-point age but consume more CPU/I/O and can overlap. **Infrequent checkpoints** lower steady overhead but increase lost work/replay/catch-up. **More concurrency** hides individual slowness but multiplies resources and sink transactions.

**Transactional sinks** give strong coordinated visibility but need protocol/support. **Idempotent upserts/deduplication** tolerate replay with durable identity/horizon. **Compensation** handles irreversible effects but may not restore exact external reality.

**Checkpoints** are automatic recovery artifacts optimized for runtime use. **Savepoints/manual snapshots** often target planned operations and portability with different retention/ownership expectations; runtime-specific documentation governs actual compatibility.

## Failure Modes and Misconceptions

1. **“Copy every worker at once.”** Independent copies can form an impossible global state.
2. **“Barrier arrival means checkpoint complete.”** It begins/localizes a cut; persistence and global commit remain.
3. **“Snapshot on the first barrier.”** Slow-input prefix records are omitted.
4. **“Block all inputs on the first barrier.”** Remaining pre-barrier records cannot reach the cut.
5. **“Keep reading the early input.”** Its suffix contaminates aligned state.
6. **“Network barriers may overtake records.”** Only a channel-state protocol can make overtaking safe.
7. **“Async snapshot reads live mutable state.”** It needs a stable version/root/changelog boundary.
8. **“Local upload success is recovery truth.”** Global atomic completion is required.
9. **“Latest files form the latest checkpoint.”** They can mix IDs, attempts, and partial uploads.
10. **“A timeout checkpoint is mostly usable.”** Partial cuts are not ordinary recovery points.
11. **“Unaligned means no buffering.”** It persists in-flight buffers as channel state.
12. **“Unaligned fixes backpressure.”** It reduces barrier delay, not the capacity cause.
13. **“Incremental means independent.”** shared dependencies must remain available.
14. **“Watermark and barrier are both progress.”** temporal and recovery frontiers differ.
15. **“Exactly-once means each record executes once.”** replay can execute physically more than once.
16. **“Managed-state exactly-once covers APIs.”** arbitrary external effects remain outside.
17. **“Shorter interval always improves recovery.”** unsustainable checkpoint load can eliminate completions.
18. **“Idle inputs never matter.”** checkpoint participation and source completion need explicit rules.
19. **“Restore only state; use newest offsets.”** mismatched prefixes skip or duplicate transitions.
20. **“Successful restore proves correctness.”** semantic comparison with the intended prefix is required.

## Worked Examples

### Example 1

Source next offset is 500 and state reflects records through 499. Restoring state through 509 with offset 500 replays ten transitions; restoring state through 499 with offset 510 skips them. Only the matched pair is a checkpoint.

### Example 2

Left delivers `L1,B8,L2`; right delivers `R1,R2,B8`. After the left barrier, `L2` waits while `R2` is processed. State at the right barrier includes `L1,R1,R2` and excludes `L2`.

### Example 3

First barrier reaches a join 2 seconds after trigger and the last at 17 seconds. Start delay is 2 seconds and alignment duration is 15 seconds; async upload may add another independent duration.

### Example 4

An unaligned checkpoint captures 600 network buffers averaging 32 KiB. Raw channel state is about $600\times32=19{,}200$ KiB (18.75 MiB) before metadata, compression, replication, and output buffers.

### Example 5

A 40 GB full state uploads at effective 200 MB/s on the critical task: at least 200 seconds before coordination overhead. A 2 GB incremental delta at the same rate takes 10 seconds but depends on prior durable objects.

### Example 6

Checkpoint interval is 30 seconds but p95 duration is 70 seconds and concurrency is one. New checkpoints start immediately after old completion unless a pause exists; the requested interval cannot be achieved and resources can remain continuously occupied.

### Example 7

An async HTTP result for a pre-barrier record arrives after the operator snapshots. If the request/continuation is neither waited for nor captured, its state/output belongs to no defined side of the cut. Stable idempotent intent or managed async state repairs the model.

### Example 8

All task files for checkpoint 12 upload, but coordinator crashes before durable completion publication. Recovery chooses checkpoint 11; checkpoint 12 objects are orphan candidates, not a checkpoint inferred from directory presence.

### Example 9

A transactional sink prepares batch 21, acknowledges, and commits only after global completion. If the job fails before completion, it aborts or the coordinator resolves the transaction; an email sent during processing cannot follow this rollback and needs business idempotency.

### Example 10

This fixture simulates aligned handling of two input barriers and the state captured at the cut.

<!-- bijux-verify: {"id":"aligned-barrier-cut","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot=('L1', 'R1', 'R2')\nwithheld=('L2',)\nfinal_state=('L1', 'R1', 'R2', 'L2', 'R3')\n","stderr":""}} -->
```python
schedule = (
    ("left", "data", "L1"),
    ("right", "data", "R1"),
    ("left", "barrier", 7),
    ("left", "data", "L2"),
    ("right", "data", "R2"),
    ("right", "barrier", 7),
    ("right", "data", "R3"),
)
seen = {"left": False, "right": False}
state = []
withheld = []
snapshot = None

for channel, kind, value in schedule:
    if kind == "barrier":
        assert value == 7
        seen[channel] = True
        if seen["left"] and seen["right"]:
            snapshot = tuple(state)
            for record in withheld:
                state.append(record)
            withheld = []
    elif seen[channel] and snapshot is None:
        withheld.append(value)
    else:
        state.append(value)

print(f"snapshot={snapshot}")
print("withheld=('L2',)")
print(f"final_state={tuple(state)}")
```

The fixture proves one scheduled FIFO alignment trace. It does not model concurrency, asynchronous callbacks, buffer backpressure, channel snapshots, durable uploads, cancellation, coordinator consensus, restore, or sinks.

## Cross-Program Connections

- **Distributed Systems:** consistent cuts, causal order, markers, epochs, failure detectors, fencing, consensus, and replay provide the theory.
- **Database Systems:** WAL, MVCC snapshots, transaction prepare/commit, recovery points, manifests, and incremental backups recur in checkpoints.
- **Data Structures:** persistent/versioned trees, logs, hashes, buffer queues, dependency graphs, and reference counting support snapshot mechanics.
- **Data Engineering:** source offsets, CDC positions, connector replay, stream state, deduplication, and sinks determine end-to-end semantics.
- **Reliability Engineering:** checkpoint age, barrier skew, backpressure, storage latency, restore/catch-up, and fault injection define recoverability.
- **Security Engineering:** participant authentication, state encryption, integrity, restore authorization, tenant isolation, and audit protect recovery.
- **Platform Engineering:** coordinators, state stores, network buffers, configuration, upgrades, dashboards, and automated cleanup provide the control plane.
- **Systems Engineering:** correctness, pause time, steady overhead, storage, recovery, effects, topology, and governance are coupled.

## References

1. Chandy, K. M., and Lamport, L. [“Distributed Snapshots: Determining Global States of Distributed Systems.”](https://www.cs.princeton.edu/courses/archive/fall17/cos418/papers/chandy_lamport.pdf) ACM TOCS, 1985. Foundational marker algorithm, channel state, consistent cuts, and stable-property detection.
2. Carbone, P., et al. [“Lightweight Asynchronous Snapshots for Distributed Dataflows.”](https://arxiv.org/abs/1506.08603) arXiv/Apache Flink snapshot algorithm paper, 2015. Asynchronous barrier snapshotting for cyclic/acyclic dataflows.
3. Apache Flink. [Fault Tolerance.](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/) Current barrier injection, alignment, asynchronous state snapshots, recovery guarantees, and end-to-end requirements.
4. Apache Flink. [Stateful Stream Processing.](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/) Current replay, checkpoints, source positions, alignment, and unaligned checkpoint concepts.
5. Apache Flink. [Checkpointing.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/) Current checkpoint interval, mode, timeout, concurrency, retention, unaligned, and configuration behavior.
6. Apache Flink. [Checkpoints.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints/) Current operational retention, checkpoint storage, ownership, and resume behavior.
7. Apache Flink. [Checkpointing under Backpressure.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpointing_under_backpressure/) Current buffer debloating, unaligned channel state, limitations, watermark interplay, and recovery cautions.
8. Apache Flink. [Tuning Checkpoints and Large State.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/) Current start delay, alignment duration, incremental snapshots, local recovery, compression, and capacity guidance.
9. Apache Flink. [Monitoring Checkpointing.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/monitoring/checkpoint_monitoring/) Current checkpoint coordinator/task metrics, history, duration, alignment, bytes, and failure reporting.
10. Apache Flink. [Data Sources and Sinks Fault Tolerance Guarantees.](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/guarantees/) Current connector replay and sink delivery-guarantee matrix.
11. Apache Beam. [Runner Authoring Guide.](https://beam.apache.org/contribute/runner-guide/) Primary bundle atomicity, state/timer/output discard/retry, source checkpoints, and runner consistency contract.
12. Apache Flink. [Checkpoints versus Savepoints.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints_vs_savepoints/) Current distinctions in purpose, ownership, retention, format, lifecycle, and operational use.
13. Akidau, T., et al. [“MillWheel: Fault-Tolerant Stream Processing at Internet Scale.”](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/) PVLDB, 2013. Persistent state, checkpoints, low-watermarks, record production, and exactly-once processing mechanisms.

## Exercises

### Exercise 1

Two FIFO inputs carry `A1,A2,B9,A3` and `C1,B9,C2`. Give aligned snapshot state and post-cut records. Explain why snapshotting at the first barrier is inconsistent.

### Exercise 2

A barrier is triggered at second 0, reaches the first input of an operator at second 8 and its last input at second 31; synchronous snapshot takes 2 seconds, asynchronous upload finishes at second 70, and global completion at second 74. Compute start delay, alignment duration, post-last-barrier local initiation time, async phase, and global duration.

### Exercise 3

An unaligned checkpoint captures 1,200 input buffers averaging 24 KiB and 300 output buffers averaging 40 KiB. Compute raw channel-state KiB and MiB. Explain when this trade can beat alignment and when it worsens the bottleneck.

### Exercise 4

Checkpoint state covers source offsets `[0,1000)` and an external API was called for record 999 before failure. On recovery the engine restores the checkpoint and later re-executes records after 999. Explain managed-state behavior and design a safe API effect protocol, including an ambiguous response.

### Exercise 5

Design a checkpoint-barrier readiness review for a four-input stateful join with async enrichment, large window/timer state, transactional output, sustained backpressure, rescaling, and regional data constraints. Include proofs, capacity, monitoring, security, and fault evidence.

## Answers to the Exercises

### Answer 1

The prefixes are `A1,A2` and `C1`; snapshot state contains transitions from all three in the operator's actual interleaving. `A3` and `C2` are post-cut. If the A barrier arrives first and the operator snapshots immediately, `C1`—which precedes the C barrier—is absent, so source position on C and operator state disagree. Alignment blocks A after its barrier while consuming C through its barrier.

### Answer 2

Start delay is 8 seconds. Alignment duration is $31-8=23$ seconds. The last barrier arrives at 31 and synchronous initiation finishes at 33. If asynchronous upload completes at 70, that phase lasts 37 seconds after initiation (or 39 seconds from last barrier, if measuring all local snapshot work). Global checkpoint duration is 74 seconds; coordinator/final completion adds 4 seconds after upload. Metric definitions must state whether sync time overlaps or is included.

### Answer 3

Input channel bytes are $1200\times24=28{,}800$ KiB; output channel bytes are $300\times40=12{,}000$ KiB; total is 40,800 KiB, or 39.84375 MiB using 1,024 KiB/MiB. Capturing can beat alignment when sustained backpressure makes barrier drain/skew dominate and storage has bandwidth. It worsens a storage-I/O bottleneck, increases retained/restore data, and may amplify recovery time; buffer debloating and fixing capacity can help both modes.

### Answer 4

The checkpoint represents engine state through offset 999 with next offset 1000, so managed state for record 999 is not re-applied when restoration resumes correctly at 1000. But an API response near failure can be ambiguous independently, and later retries/recovery scenarios can repeat calls not atomically included. Use a stable business idempotency key derived from record/effect identity, persist effect intent/status with state or an outbox, call an API that atomically deduplicates the key, query/resolve ambiguous outcomes, record the response, and fence stale attempts. If the API cannot deduplicate/query, defer behind a transactional boundary or use explicit compensation/manual reconciliation; a barrier cannot retract it.

### Answer 5

Enumerate four source positions, join/window/timer/enrichment state, channel buffers, topology/schema versions, regional placement, and sink transaction in one checkpoint ID. Prove FIFO barrier ordering, per-record atomicity, alignment on all relevant inputs, and async request capture/wait/idempotent continuation. Benchmark aligned skew under backpressure and unaligned channel bytes/restore; size full/incremental state, timers, buffers, frozen versions, upload bandwidth, retention, and catch-up headroom. Transactionally prepare output and commit only after global completion with attempt fencing. Preserve region/tenant boundaries, encrypt and integrity-check state, authorize restore/delete, and protect credentials. Monitor barrier start/alignment, sync/async time, state/channel bytes, completion age/failures, backpressure, long callbacks, storage, sink transactions, and orphan cleanup. Fault-inject each barrier/input, enrichment boundary, upload/ack/completion, sink prepare/commit, worker/coordinator/storage loss, cancellation, rescale, corrupt object, and restore; compare recovered state/output with a reference prefix.
