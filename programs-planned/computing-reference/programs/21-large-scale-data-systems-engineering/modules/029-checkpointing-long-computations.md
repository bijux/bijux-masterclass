---
module_id: LSDS-029
program: Large-Scale Data Systems Engineering
level: 1
module_number: 29
title: Checkpointing Long Computations
status: complete
last_verified: 2026-09-03
---

# Checkpointing Long Computations

## One-Page Review

### Governing question

How should a long-running data computation capture, validate, retain, and restore a consistent recovery point often enough to bound lost work without overwhelming storage, blocking useful progress, breaking sink semantics, or creating an unmaintainable state format?

### Essential definitions

- A **checkpoint** is a coordinated recovery snapshot of computation progress and required state.
- A **consistent cut** is a distributed snapshot that does not record an effect without the causal input/state needed to explain it.
- **recovery point objective** bounds acceptable progress loss or replay; **recovery time objective** bounds acceptable restoration time.
- A **checkpoint interval** is intended time between triggers; **minimum pause** bounds rest after completion; **timeout** abandons a stalled checkpoint.
- An **aligned checkpoint** blocks inputs that received a barrier until other inputs catch up; an **unaligned checkpoint** also captures relevant in-flight channel data.
- A **full checkpoint** writes the complete recovery state; an **incremental checkpoint** references prior immutable state and writes changes.
- A **savepoint** is an operator-managed snapshot intended for planned stop, upgrade, fork, or rescale; engine terminology varies.
- **lineage truncation** replaces a long recomputation graph with a checkpoint boundary.
- **restore compatibility** defines which code, schema, operator identity, partitioning, serializer, and engine versions can read a checkpoint.
- **checkpoint lineage** is the dependency graph among incremental/base files and metadata required for restoration.

### Central model, mechanism, or theorem

For checkpoint duration/cost `C`, checkpoint interval `T`, mean time between relevant failures `M`, and recovery cost `R`, a simple steady-state overhead fraction is `C/T + T/(2M) + R/M`. The first term is checkpoint work, the second is expected lost work under failures uniformly distributed within an interval, and the third is recovery. Ignoring constraints and higher-order effects, differentiating the first two terms gives `T*=sqrt(2CM)`. Production choices must also satisfy storage bandwidth, checkpoint completion, sink visibility, RPO/RTO, correlated failures, and tail distributions.

A correct checkpoint identifies source positions, operator/task state, pending timers or work, partition/ownership mapping, and in-flight or barrier state needed for one consistent cut. Durable metadata atomically names validated state objects. Recovery restores exactly that generation and replays from its recorded positions; end-to-end exactly-once still requires replayable sources and transactional or idempotent sinks.

### Critical invariants

- Every checkpoint generation represents one consistent cut, not a mix of task times or attempts.
- Source positions and state correspond to the same logical processing frontier.
- Operator/task identities remain stable or have an explicit state migration mapping.
- Snapshot objects are immutable, checksummed, durably replicated as required, and referenced by one complete committed metadata record.
- A checkpoint is declared complete only after every required participant and sink transaction acknowledges durably.
- Recovery never uses partial, superseded, corrupt, incompatible, or policy-expired state silently.
- Incremental checkpoints retain every referenced base/delta until no valid restore point needs it.
- Checkpoint concurrency, interval, timeout, and backpressure cannot prevent useful application progress indefinitely.
- Restore drills validate actual RPO/RTO, source retention, credentials, capacity, and sink reconciliation.
- Sensitive state follows minimization, encryption, residency, access, retention, deletion, and audit requirements.

### Common failures

Frequent failures are equating a cache with a reliable checkpoint, snapshotting state without source positions, advancing source offsets before sink/state commit, mixing generations, deleting an incremental base still referenced, choosing interval from averages alone, triggering faster than checkpoints finish, hiding backpressure with unaligned snapshots while in-flight state grows, using local checkpoint data after worker loss, changing operator IDs or serializers without migration, trusting checksum without restore, retaining secrets/personal state indefinitely, and claiming exactly-once because internal state restores while the external sink duplicates.

### Compact example

With checkpoint cost 4 minutes, mean time between relevant failures 720 minutes, and recovery 10 minutes, the simplified optimum is about 75.89 minutes. Checkpoint overhead and expected lost work are each about 5.27 percent; recovery adds 1.39 percent, for roughly 11.93 percent modeled overhead. A failure at minute 670 restored from a valid checkpoint at minute 600 replays 70 minutes and preserves 600. This model assumes independent uniformly timed failures and compatible cost units; it is not a production interval prescription.

### Connections

[LSDS-024](024-directed-acyclic-graph-execution.md) supplies consistent graph state and lineage, [LSDS-027](027-task-retry-and-speculation.md) supplies failover/replay, and [LSDS-028](028-intermediate-data-materialization.md) distinguishes retained data from recovery snapshots. [LSDS-030](../ROADMAP.md) traces these artifacts through a cluster engine.

## Governing Question

Long computations accumulate progress worth protecting. An iterative optimizer may run for days; a stateful dataflow may process continuously; a batch graph may build an expensive chain whose late failure would restart from raw input. Checkpoints trade ongoing overhead for bounded recovery.

The file bytes alone are not the checkpoint. Recovery needs a mutually consistent view of progress and state. If source offset 1,000 is recorded but state includes only records through 990, ten records disappear. If state includes through 1,000 but a nontransactional sink published only through 980, replay and visibility diverge.

The governing question is how to construct a recoverable cut, choose when and how to take it, and prove it remains restorable under realistic failure, version, storage, and governance conditions.

## Why This Matters

Checkpointing too rarely wastes hours after failure. Checkpointing too often consumes CPU, memory, I/O, network, metadata, and sink transactions, sometimes causing the backpressure and timeouts that make checkpoints fail. The optimal point changes with state size, dirty rate, storage health, failure domain, and delivery requirements.

Checkpointing changes semantics. A coordinated state snapshot can make replay appear as failure-free state evolution, but an external sink must participate or deduplicate. A local lineage cut can shorten a plan yet be unreliable under executor loss. A manually retained savepoint may support upgrade, while an engine-managed checkpoint may be optimized for one deployment and garbage-collected automatically.

Operational confidence comes from restore drills, not checkpoint-success counters. A snapshot can be complete and still unrestorable because source retention expired, code moved, serializers changed, encryption keys were revoked, credentials lack access, or a required base delta was deleted.

Checkpoint state can be highly sensitive: model parameters, keyed user history, timers, offsets, pending transactions, and secrets. Recovery requirements do not waive purpose, retention, residency, deletion, or access controls.

## Prerequisites and Retrieval

Recall distributed state, stages, dependencies, serialization, and scale accounting from [LSDS-005](005-distributed-task-graphs.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve durable storage, replication, checksums, and atomic publication from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Retrieve DAG lineage from [LSDS-024](024-directed-acyclic-graph-execution.md), lazy plan identity from [LSDS-025](025-lazy-evaluation-and-plan-construction.md), stage resources from [LSDS-026](026-stage-scheduling.md), retry/failover from [LSDS-027](027-task-retry-and-speculation.md), and materialization contracts from [LSDS-028](028-intermediate-data-materialization.md).

You should understand probability/expectation, derivatives or convex minimization, immutable manifests, barriers, replayable logs, transactions/idempotency, schemas/serialization, DAG lineage, encryption/key lifecycle, and recovery objectives.

## Learning Objectives

After this module, you should be able to:

1. distinguish cache, materialization, checkpoint, externalized checkpoint, and savepoint contracts;
2. specify a consistent cut across source positions, operator state, in-flight records, timers, and sinks;
3. derive and critique a simplified checkpoint-interval model;
4. choose full, incremental, aligned, unaligned, synchronous, or asynchronous snapshot mechanisms;
5. define generation metadata, atomic completion, validation, retention, and garbage collection;
6. design restore compatibility across code, operator IDs, schemas, serializers, partitions, and engines;
7. test source replay, sink transactions/idempotency, coordinator failure, corruption, and partial snapshots;
8. diagnose checkpoint duration, alignment, start delay, backpressure, storage saturation, and recovery tails;
9. verify RPO/RTO through destructive restore drills rather than configuration alone; and
10. govern sensitive recovery state through ownership, access, minimization, residency, retention, deletion, and review.

## Core Exposition

### What belongs in a checkpoint

A recovery snapshot normally includes source positions, operator/keyed state, local algorithm progress, timers, partition ownership, pending asynchronous work, and sink transaction handles. It also records plan/code/schema/serializer versions and the topology needed to map state back to operators.

Stateless transformations may need no state bytes, yet their stable identity and upstream position still matter. A long batch loop may checkpoint iteration number, model parameters, optimizer state, random generator state, input snapshot, and convergence metrics.

### Consistent cuts

In a distributed graph, workers observe progress at different times. A coordinator injects or establishes a logical barrier. Each input/operator records state corresponding to that frontier. A consistent cut never includes receipt/effect of a message while excluding the send or required channel content.

Barrier alignment waits for the frontier on every input and temporarily blocks faster inputs. This excludes post-barrier records from the state cut but can increase latency under skew/backpressure. Unaligned techniques capture in-flight channel data instead of waiting; they reduce alignment delay while increasing snapshot size and restore work.

For batch iteration, a simpler global boundary may finish a superstep, validate all partitions, and commit model/state plus iteration number. The synchronization cost can be high but semantics are explicit.

### Source and sink participation

Recovery rewinds a replayable source to recorded positions. Source retention must exceed detection, repair, restore, and catch-up time. A mutable file listing or API without historical versions cannot reliably replay the same input.

Exactly-once internal state does not guarantee exactly-once external output. A sink can stage writes under a checkpoint transaction and publish when that checkpoint completes; or it can use stable idempotency keys and reconciliation. A sink effect committed before the checkpoint may duplicate on replay unless its identity survives.

### Full and incremental snapshots

A full checkpoint writes all required state and has a simpler standalone dependency. Incremental checkpoints write newly created or changed immutable state and reference shared base files. They reduce recurring bytes when change rate is low, but lengthen dependency chains and complicate garbage collection, validation, transfer, and restore.

Incremental physical bytes and logical full-state size are different metrics. Deduplication or file merging can make storage accounting nonobvious. Track both, plus reference counts/mark-and-sweep reachability from retained restore points.

Periodically consolidating a long delta chain can improve restore time at a write spike. Test the trade-off under real dirty patterns and storage behavior.

### Synchronous and asynchronous phases

Many systems briefly establish the cut and copy or freeze a state view, then upload it asynchronously while processing continues. Copy-on-write or immutable state files preserve the older version until upload commits. This reduces pause but increases concurrent memory/disk/network demand.

A checkpoint is not complete when local copying starts. It completes only after every required state object, metadata entry, source position, and sink acknowledgment is durably committed. Failure during asynchronous upload discards the incomplete generation without corrupting the prior valid one.

### Interval economics

The simplified formula balances frequent checkpoint cost against expected replay. Differentiating `C/T + T/(2M)` yields `-C/T^2 + 1/(2M)=0`, hence `T=sqrt(2CM)`. Recovery `R/M` is constant in this simplification.

Assumptions are strong: checkpoint cost is constant, failures independent and uniformly located, one failure domain, recovery succeeds, useful work rate constant, and checkpoints do not overlap or alter failure probability. Real selection uses measured distributions, checkpoint completion tails, storage capacity, RPO, sink publication delay, and failure bursts.

If `T` is shorter than checkpoint duration or minimum pause, configured cadence is unattainable. Multiple concurrent checkpoints can improve frequency in delayed pipelines but amplify state/network pressure and lineage complexity.

### RPO, RTO, and catch-up

RPO concerns progress lost/replayed from the last usable checkpoint, not merely configured interval. A failed or slow checkpoint increases effective age. RTO includes detection, scheduling, metadata discovery, state download, deserialization, source seek, sink reconciliation, and catch-up to the pre-failure frontier.

Catch-up capacity matters for continuous workloads. If normal input rate equals maximum processing capacity, replay backlog never closes. Reserve headroom or temporarily scale within policy. Report time to recovered service, not just state-load duration.

### Checkpoint storage and metadata

Use durable storage outside the correlated compute failure domain for production recovery. Each generation has immutable state objects and compact metadata binding job/plan, operators, partitions, source positions, sink transactions, state handles, lengths/checksums, encryption/key versions, parent checkpoints, creation/completion times, and compatibility.

Commit metadata atomically after validating all participants. Keep the prior complete checkpoint until the new one is durable and restore-tested according to policy. Directory names and listings are not sufficient authority.

### Operator identity and compatibility

State maps to stable logical operator identifiers, not display position alone. Reordering or inserting operators can otherwise attach state incorrectly. Assign durable IDs and record partition/key-group mappings.

Restore compatibility spans code, state schema, serializers, numeric behavior, timer format, partitioning, connector/source offsets, sink transactions, engine version, and encryption keys. Planned upgrades use explicit migration, savepoints, compatibility tests, and rollback. “Deserializes” is weaker than “preserves semantics.”

### Lineage truncation for batch and iterative work

A long lazy plan can become expensive to schedule and replay. A reliable checkpoint materializes an intermediate and replaces prior lineage for recovery. A local checkpoint may truncate lineage while using executor/cache storage and therefore be lost; it is a performance tool, not a durable fault-tolerance promise.

Iterative algorithms must checkpoint all coupled state: parameters, optimizer moments, iteration/epoch, data order/shuffle seed, random generator, convergence/early-stop state, and side inputs. Saving weights alone may restart with different dynamics.

### Alignment, backpressure, and skew

Checkpoint start delay measures how long barriers take to reach an operator; alignment duration measures first-to-last input barrier time. High values can indicate backpressure, skew, network trouble, blocked asynchronous calls, or insufficient resources.

Unaligned checkpoints can bypass long alignment by recording in-flight data, but they do not repair the underlying throughput deficit. Large in-flight state can make checkpoint and restore expensive. Diagnose per-input/per-task distributions and end-to-end latency.

### Timeouts, failures, and concurrency

A timeout discards a checkpoint that cannot complete in time. Configure tolerated consecutive failures and alert before all recovery points age beyond RPO. Back off or reduce concurrency during storage degradation rather than continuously flooding it.

Coordinator failure during snapshot requires durable checkpoint-coordination state or safe abortion. Late acknowledgments carry generation IDs and cannot complete a superseded checkpoint. Partial objects are quarantined and garbage-collected after reconciliation.

### Retention and garbage collection

Retain enough independent recovery points to survive latent corruption and operator error, constrained by storage and privacy. Engine-managed checkpoints may be removed on cancellation; externalized checkpoints/savepoints may persist. Know the exact policy.

Incremental deletion uses reachability: an object can be removed only when no retained checkpoint metadata references it and no restore/transfer/audit/legal hold needs it. Reference updates and deletion must tolerate crashes. Periodically reconcile metadata with objects.

### Validation and restore drills

At creation, validate participant completeness, metadata schema, lengths/checksums, source offset ranges, operator/key-group coverage, sink transaction state, and compatibility. Sample semantic state invariants where feasible.

Regularly restore into an isolated environment, with production-equivalent scale and credentials, replay sources, reconcile sinks, compare state/output to a reference, measure every RTO phase, inject corruption/missing deltas, and exercise rollback. A checkpoint that has never restored is an unverified backup.

### Observability

Record triggers, completion/failure/timeout, end-to-end duration, synchronous pause, start delay, alignment, full/incremental bytes, objects/files, upload bandwidth, state by operator, dirty ratio, concurrent generations, age of last successful point, source retention margin, restore duration, replay volume, catch-up, and sink commit latency.

Relate metrics to useful processing throughput and p50/p95/p99 latency. Checkpoint success at the cost of permanent backpressure is not healthy. Track storage and API cost, retained lineage, cleanup lag, and failed/orphan bytes.

### Security, governance, and human impact

Checkpoint state can bypass source-level protections by containing decoded, joined, aggregated, or pending-decision information. Encrypt with recoverable key lifecycle, scope access to recovery roles, isolate tenants/purposes/regions, redact metadata/logs, and audit restores/downloads.

Deletion and correction may need propagation into checkpoints; legal/records needs may require holds. Define whether old state can resurrect deleted/corrected data after restore and apply tombstones or post-restore reconciliation. For systems affecting people, test replay timeliness, duplicate/lost effects, subgroup state quality, accessibility, correction, appeal, and named oversight.

## Definitions and Notation

- `C`: checkpoint time or normalized cost per completed generation.
- `T`: interval between usable checkpoints in the simplified model.
- `M`: mean time between relevant failures under a stated failure domain.
- `R`: recovery cost after a failure.
- `H(T)=C/T+T/(2M)+R/M`: simplified steady-state overhead fraction.
- `T*=sqrt(2CM)`: stationary optimum under the simplified assumptions.
- **frontier**: logical progress boundary represented by source positions and corresponding state.
- **barrier alignment**: waiting for a checkpoint marker on all relevant inputs before snapshotting.
- **in-flight state**: records/buffers captured when the cut does not wait for full alignment.
- **checkpoint generation**: unique snapshot attempt; only completed generations are restorable.
- **operator UID**: stable state-association identity across planning and compatible upgrades.
- **restore drill**: isolated controlled recovery that validates correctness and observed RPO/RTO.

## Mechanisms, Invariants, or Proof Structure

Audit checkpointing in this order:

1. Define failure domains, state/progress to protect, RPO, RTO, source replay horizon, sink guarantee, and catch-up need.
2. Pin job/plan/code/schema/serializer/operator/partition/input/security identities and migration policy.
3. Specify the consistent cut: source positions, operator state, timers/work, in-flight channels, and sink transactions.
4. Choose full/incremental, aligned/unaligned, synchronous/asynchronous, storage, replication, compression, encryption, and cadence.
5. Model checkpoint/replay/recovery cost with uncertainty and constrain interval, pause, timeout, concurrency, and budget.
6. Isolate generation objects, validate participant completeness/integrity, and atomically commit metadata only after durable acknowledgments.
7. Restore exactly one compatible generation, replay pinned sources, reconcile sinks, fence late generations, and preserve prior valid points.
8. Manage incremental reachability, retention, externalization, holds, key lifecycle, garbage collection, and verified deletion.
9. Monitor checkpoint age/duration/alignment/bytes/failures and useful throughput; respond before RPO or source retention is breached.
10. Run regular failure/corruption/upgrade/rollback drills at realistic scale and review outcomes with owners and affected stakeholders.

The consistency proof connects one recorded source frontier to operator state and sink transaction state. Restore plus replay must yield the declared failure-free observable result, subject to the stated at-least/exactly-once contract. Internal state consistency cannot prove sink uniqueness alone.

The interval derivation supplies a starting point, not a guarantee. Every assumption and hard constraint must be checked against measured checkpoint, failure, restore, replay, and service distributions.

<!-- bijux-verify: {"id":"checkpoint-interval-and-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"recommended_interval_minutes=75.89\ncheckpoint_overhead=5.27% expected_lost_work=5.27% recovery=1.39% total=11.93%\nreplay_minutes=70 work_preserved=600\n","stderr":""}} -->
```python
from math import sqrt


checkpoint_cost = 4
mean_time_between_failures = 720
recovery_cost = 10
interval = sqrt(2 * checkpoint_cost * mean_time_between_failures)
checkpoint_fraction = checkpoint_cost / interval
lost_work_fraction = interval / (2 * mean_time_between_failures)
recovery_fraction = recovery_cost / mean_time_between_failures
total = checkpoint_fraction + lost_work_fraction + recovery_fraction
last_checkpoint = 600
failure_time = 670

print(f"recommended_interval_minutes={interval:.2f}")
print(
    f"checkpoint_overhead={checkpoint_fraction:.2%} "
    f"expected_lost_work={lost_work_fraction:.2%} "
    f"recovery={recovery_fraction:.2%} total={total:.2%}"
)
print(f"replay_minutes={failure_time-last_checkpoint} work_preserved={last_checkpoint}")
```

The model treats time fractions as lost useful capacity and assumes a usable checkpoint. It omits storage contention, checkpoint failures, correlation, sink visibility, source retention, catch-up, and tail behavior.

## Alternatives and Trade-Offs

**No checkpoint versus periodic checkpoint.** Restart-from-source is simple for short deterministic work. Periodic snapshots protect expensive progress but add continuous overhead and format/lifecycle obligations.

**Full versus incremental.** Full points are self-contained but rewrite all state. Incremental points save recurring bytes but create dependency and cleanup complexity.

**Aligned versus unaligned.** Alignment minimizes in-flight snapshot state and supports a clean cut but can block under skew. Unaligned capture reduces alignment delay at larger snapshots/restores and does not solve throughput deficits.

**Synchronous versus asynchronous.** Synchronous snapshotting simplifies state stability but pauses work. Asynchronous upload lowers pause and increases concurrent resources/version retention.

**Durable versus local checkpoint.** Durable storage survives compute loss at network/storage cost. Local truncation is fast but unreliable under executor/domain loss.

**Frequent versus sparse cadence.** Frequent points reduce replay and can publish sinks sooner, but increase checkpoint pressure. Sparse points reduce overhead and increase RPO/recovery.

**Checkpoint versus savepoint.** Automated checkpoints optimize fault recovery/lifecycle. Savepoints support planned operational control and upgrades. Concrete engine semantics govern portability and cleanup.

**Retain many versus few points.** Multiple points protect against latent corruption/operator error. They increase storage, sensitive-data lifetime, key obligations, and dependency reachability.

## Failure Modes and Misconceptions

**"A cache is a checkpoint."** Cache loss may trigger lineage recomputation; local checkpointing can explicitly trade away reliability.

**"Saving state is enough."** Source positions, in-flight work, operator mapping, and sink transactions must describe the same cut.

**"Exactly-once means each record executes once."** Recovery can replay; the claim concerns declared state/effect observability.

**"Shorter interval always improves recovery."** Checkpoints can overlap, cause backpressure, fail, and reduce useful progress.

**"The configured interval is the RPO."** Failed/slow checkpoints and detection/retention determine age of the last usable point.

**"Unaligned checkpointing fixes backpressure."** It can reduce barrier delay while capturing more in-flight data; capacity deficit remains.

**"Incremental means each checkpoint stands alone."** Restore may require shared base and delta objects.

**"Checksum success proves restore."** Compatibility, completeness, semantics, source replay, credentials, and sink state can still fail.

**"Changing operator names is cosmetic."** Unstable IDs can orphan or misattach state.

**"Weights are the whole training state."** Optimizer moments, epoch/order, randomness, convergence, and data snapshot matter.

**"Completed checkpoints can be deleted FIFO."** Incremental dependencies, restores, audits, holds, and rollback must be considered.

**"Internal recovery proves end-to-end safety."** Replayable sources and transactional/idempotent sinks remain necessary.

## Worked Examples

### Example 1

A 30-minute batch job with cheap deterministic inputs may reasonably restart from source rather than spend minutes checkpointing. Record failure probability and deadline. “Long” is relative to recovery cost and objectives, not a fixed duration.

### Example 2

Four input partitions reach barrier 12 at different times. An aligned checkpoint blocks the first three until the fourth arrives, then snapshots state before post-barrier records. Alignment duration exposes skew/backpressure on the fourth branch.

### Example 3

Under severe backpressure, an unaligned checkpoint records channel buffers with operator state. It completes faster but writes 80 GiB of in-flight data and takes longer to restore. The application still needs enough capacity to catch up.

### Example 4

A 10-TiB keyed state changes 100 GiB per interval. Incremental snapshots reduce recurring write, but ten retained points share base files. Deleting the oldest metadata cannot delete any base still reachable from newer points.

### Example 5

Source offsets are committed at 1,000, operator state at 990, and sink through 980. This is not a consistent checkpoint. Coordinate the frontier and sink transaction or replay will lose or duplicate effects.

### Example 6

An iterative model stores weights but omits optimizer moments and shuffle seed. Restore changes the next update sequence. A complete checkpoint includes iteration/epoch, optimizer, random/order, input snapshot, and convergence state.

### Example 7

A local checkpoint truncates a large logical plan and speeds scheduler recovery while executors live. A rack loss removes its cache blocks and lineage has already been truncated. Use durable checkpointing when that failure must be tolerated.

### Example 8

Checkpoint metrics are green for months, but a drill fails because a serializer upgrade cannot read old state. Add compatibility fixtures, savepoint migration, rollback, and restore canaries before deploying the new code.

### Example 9

A checkpoint at minute 600 and failure at 670 imply 70 minutes replay. If source logs retain only 45 minutes, the checkpoint is unusable despite intact state. Retention margin is a first-class RPO/RTO dependency.

### Example 10

A benefits engine restores an old checkpoint containing data later corrected or deleted. Post-restore reconciliation must reapply durable correction/deletion tombstones before decisions resume. Privacy, domain, affected-party, accessibility, and incident reviewers define safe recovery.

## Cross-Program Connections

- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies consistent snapshots, replay, consensus, fencing, transactions, and failover.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies write-ahead logs, recovery, MVCC snapshots, checkpoints, and schema migration.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies checkpoints to pipelines, offsets, backfills, data quality, and publication.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies process images, memory snapshots, copy-on-write, filesystems, and crash recovery.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies barriers, consistent state, races, asynchronous copy, and cancellation.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies interval optimization, expected-cost models, incremental algorithms, and sensitivity analysis.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies barrier delay, backpressure, channel state, upload bandwidth, and congestion.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies durable stores, identities, orchestration, observability, restore automation, and drills.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies encrypted state, key recovery, least privilege, integrity, retention, and deletion.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies RPO/RTO, lifecycle, failure domains, coupled feedback, and risk evidence.

## References

1. Apache Flink. [Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/). Accessed 2026-09-03.
2. Apache Flink. [Fault Tolerance via State Snapshots](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/). Accessed 2026-09-03.
3. Apache Flink. [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Accessed 2026-09-03.
4. Apache Flink. [Savepoints](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/). Accessed 2026-09-03.
5. Apache Flink. [Checkpoints versus Savepoints](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints_vs_savepoints/). Accessed 2026-09-03.
6. Apache Flink. [Monitoring Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/monitoring/checkpoint_monitoring/). Accessed 2026-09-03.
7. Apache Spark. [RDD Programming Guide: Checkpointing and Persistence](https://spark.apache.org/docs/latest/rdd-programming-guide.html). Accessed 2026-09-03.
8. Apache Spark. [Local Checkpoint](https://spark.apache.org/docs/latest/api/R/reference/localCheckpoint.html). Accessed 2026-09-03.
9. Apache Spark. [Configuration: Checkpoint Storage and Compression](https://spark.apache.org/docs/latest/configuration.html). Accessed 2026-09-03.
10. Dask. [Advanced Graph Manipulation: Checkpoint](https://docs.dask.org/en/stable/graph_manipulation.html). Accessed 2026-09-03.
11. K. Mani Chandy and Leslie Lamport. [Distributed Snapshots: Determining Global States of Distributed Systems](https://lamport.azurewebsites.net/pubs/chandy.pdf). ACM TOCS 1985. Accessed 2026-09-03.
12. J. W. Young. [A First Order Approximation to the Optimum Checkpoint Interval](https://digital.library.unt.edu/ark:/67531/metadc1410636/). Communications of the ACM 1974. Accessed 2026-09-03.

## Exercises

### Exercise 1

Derive the simplified optimal interval, recompute the compact example, and list the assumptions that prevent direct production use.

### Exercise 2

Specify a consistent checkpoint cut for a two-input stateful join with timers, asynchronous lookups, replayable sources, and a transactional sink.

### Exercise 3

Design incremental checkpoint metadata, validation, retention, and garbage collection for 1,000 partitions and ten retained generations.

### Exercise 4

Plan a restore/upgrade drill that measures actual RPO/RTO and catches operator-ID, serializer, source-retention, sink, key, and capacity failures.

### Exercise 5

Specify named review and evidence for checkpointing a long-running regulated decision system whose state includes corrections and deletion requests.

## Answers to the Exercises

### Answer 1

For `H=C/T+T/(2M)+R/M`, derivative in `T` is `-C/T^2+1/(2M)`. Setting zero gives `T^2=2CM`, so `T*=sqrt(2CM)` and the positive second derivative gives a minimum. With `C=4`, `M=720`, `R=10`, interval is `sqrt(5760)=75.89`; checkpoint and replay fractions are about 5.27 percent each, recovery 1.39 percent, total 11.93 percent. It assumes constant compatible costs, independent uniformly located failures, successful restore, constant progress, no overlap/backpressure, and ignores RPO/RTO, source/sink/storage constraints, tails, correlation, and checkpoint failure.

### Answer 2

Assign one generation and inject barriers into both sources at recorded offsets. Each join partition aligns or captures channel state, drains/records pending asynchronous requests under deterministic IDs, snapshots keyed join buffers, timers and watermark/frontier, and acknowledges object checksums plus operator/partition identity. The sink opens a generation transaction and stages outputs. The coordinator commits metadata only after all source positions, operators, channel state, and sink prepare acknowledgments are durable, then commits/publishes the sink transaction according to its protocol. Recovery restores one generation, rewinds both sources, reissues/reconciles asynchronous lookups idempotently, and fences late prior generations.

### Answer 3

Metadata pins job/plan/operator/schema/serializer/partition/security identity; generation and parent/base; source/sink frontier; and, for every partition, immutable state handles with logical/full and incremental bytes, length, cryptographic checksum, encryption key version, and shared-object IDs. Validate IDs 0–999, state/key-group coverage, all objects/checksums, parent reachability, and atomic completion. Retain ten complete generations plus active restore/upgrade/audit/legal holds. Mark all objects reachable from those roots, sweep only unmarked objects after quarantine, and make reference/metadata changes crash-safe. Reconcile listings and manifests, test missing/corrupt bases, and compact long chains when measured restore cost warrants.

### Answer 4

Clone production plan/code/config and a governed input/source-log snapshot into isolation. Restore the oldest supported and newest checkpoint under production-scale state, credentials, keys, topology, bandwidth, and worker capacity. Inject missing/corrupt deltas, coordinator loss, slow storage, skew/backpressure, and sink ambiguous commit. Upgrade operator IDs/schema/serializer/engine using declared migration, validate key-group mapping and semantic reference output, then roll back. Measure detection, scheduling, metadata, download, deserialize, source seek, sink reconciliation, replay, catch-up, and service-resume time; compute actual progress loss and retention margin. Record owners, artifacts, failures, remediation, and repeat cadence.

### Answer 5

Pin purpose, state fields, source/sink and plan identities, operator/schema/serializer versions, frontier and effect guarantee, RPO/RTO, correction/deletion tombstone source, encryption/key recovery, residency/access, retention/holds, restore authorization, and incident/appeal procedure. Test lost/duplicate decisions, stale corrections, resurrected deletions, subgroup state coverage/quality, source retention, sink reconciliation, partial corruption, key revocation, upgrade, rollback, and post-restore accessibility/timeliness. Named review includes domain and decision owners, data stewards, affected communities or ethics oversight, privacy/legal/records/jurisdiction authorities, fairness/statistics, security/identity/key management, platform/runtime/storage/network operators, accessibility, incident/recovery, and independent assurance. Recovery speed cannot waive correction, appeal, purpose, minimization, retention, or deletion.
