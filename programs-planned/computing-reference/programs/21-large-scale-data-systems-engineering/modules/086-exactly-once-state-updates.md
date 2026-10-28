---
module_id: LSDS-086
program: Large-Scale Data Systems Engineering
level: 2
module_number: 86
title: Exactly-Once State Updates
status: complete
last_verified: 2026-09-04
---

# Exactly-Once State Updates

## One-Page Review

### Governing question

How can a stateful distributed dataflow retry, replay, migrate, and recover physical work while making each admitted logical input affect managed state exactly once—and how can operators prove the boundary without claiming that code ran once or arbitrary external effects occurred once?

### Essential definitions

- A **physical attempt** is one execution that may fail, race, or be retried.
- A **logical input** is the stable record or transaction whose state effect is being protected.
- A **state transition** applies deterministic function $\delta$ to committed state and a logical input.
- A **commit bundle** atomically couples state mutations with consumed-input progress and any participating timers or internal outputs.
- A **commit identity** uniquely names that bundle across retries.
- A **committed frontier** identifies the greatest source progress reflected in committed state under a stated partition/order model.
- A **fencing epoch** prevents an obsolete owner from publishing state after reassignment or recovery.
- **exactly-once state semantics** means committed state is equivalent to one valid failure-free application of each admitted logical input.
- **deduplication** rejects a repeated stable identity; it is one implementation technique, not the definition of exactly once.
- **deterministic replay** reproduces the same transition from the same committed predecessor and captured inputs.
- An **ambiguous commit** is one whose caller lost the outcome and must query by stable identity before retrying.

### Central model, mechanism, or theorem

For logical input $e$ and committed state version $S_v$, define

$$\delta(S_v,e)=(\Delta S,O,T),$$

where $\Delta S$ is the state mutation set, $O$ participating internal outputs, and $T$ timer registrations/deletions. Commit bundle

$$B=(j,p,q,v,g,h(e),\Delta S,O,T)$$

names job $j$, source partition $p$, input position $q$, expected predecessor version $v$, fencing epoch $g$, and canonical input fingerprint $h(e)$. The state service accepts $B$ only if its identity/fingerprint is consistent, $g$ is current, the predecessor/frontier rule holds, and no equivalent commit already succeeded. It atomically publishes the mutations, progress, timers, and participating outputs—or none—and stores a recoverable outcome.

With replayable input, a consistent checkpoint/commit log, deterministic transition inputs, idempotent outcome lookup, and fenced atomic publication, multiple physical attempts refine to one logical committed transition. This guarantee ends at the commit boundary: logs, metrics, HTTP calls, and nonparticipating sinks may still execute more than once.

### Critical invariants

- Stable logical-input and commit identities survive retry, restart, rescale, replay, and deployment.
- State mutation and the input frontier/deduplication record commit atomically.
- One commit identity cannot be reused with a different canonical input or mutation fingerprint.
- A bundle publishes all participating state, timers, and outputs or none of them.
- Only the current fencing epoch may publish; stale owners can compute but cannot commit.
- Per-partition progress advances without gaps under ordered-source semantics; multi-input progress is a vector, not one scalar.
- Recovery restores state and progress from the same committed cut, then replays strictly according to the source contract.
- Nondeterministic values and asynchronous results that affect state are captured, versioned, or made part of the committed input.
- Timer firing has stable logical identity and is coupled to state transition semantics.
- TTL, lateness, deletion, and schema evolution do not silently change replay meaning.

### Common failures

Common failures include equating invocation count with committed effects; updating state before source progress in separate commits; acknowledging progress before durable state; using worker attempt IDs as logical IDs; accepting same ID with changed payload; advancing offset 12 when 11 is absent; reducing a multi-input cut to one offset; allowing an expired lease holder to commit; performing remote reads that change between replay attempts; emitting an output before its state transition commits; restoring state from one epoch and offsets from another; expiring deduplication evidence before replay; treating processing-time timers as deterministic; mutating state concurrently without key serialization or conflict detection; and claiming end-to-end exactly once for an HTTP call outside the protocol.

### Compact example

At epoch 2, input `p0:1` adds 5 to key `a`. Its first attempt atomically commits `a=5` and frontier `p0=1`; a repeated attempt with the same identity returns the recorded outcome. Input `p0:2` adds 3 and commits `a=8`. A delayed epoch-1 owner tries `p0:3` and is fenced, so neither state nor frontier changes. Input `p1:1` adds 7 to `b`. Three logical commits result despite four accepted/retried executions: state is `a=8,b=7`, frontiers are `p0=2,p1=1`, and no gap is hidden.

### Connections

[LSDS-043](043-stateful-operators.md) defines keyed state, [LSDS-047](047-checkpoint-barriers.md) defines consistent input cuts, [LSDS-048](048-state-snapshots-and-recovery.md) supplies state restoration, [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) separates external effects, [LSDS-083](083-coordinator-failure.md) supplies epoch fencing, and [LSDS-085](085-checkpoint-based-recovery.md) supplies recoverable checkpoint selection.

## Governing Question

Fault-tolerant engines retry work deliberately. A worker can read a record, increment a counter, and fail before reporting success. Another worker then reads the record again. Preventing retries would trade duplicates for data loss; exactly-once state semantics instead allow repeated computation while committing one logical transition.

The phrase “processed exactly once” is dangerously compressed. Code may run twice. Logs may appear twice. A speculative attempt may coexist with the original. An asynchronous lookup may run again. What must be singular is the accepted effect within a named state boundary: the final state, committed input progress, timers, and protocol-participating outputs should be observationally equivalent to one valid failure-free execution.

The governing question is therefore which identities, atomic commit boundary, order rules, replay inputs, ownership epochs, and recovery evidence make that equivalence true. The answer must also state where it stops: managed state correctness does not automatically include arbitrary databases, APIs, files, notifications, or human actions.

## Why This Matters

Stateful pipelines maintain balances, sessions, joins, fraud features, inventory views, model aggregates, watermarks, and timers. One duplicated increment can bias every later result; one skipped transition can make an account or key permanently inconsistent. Because state is long-lived, small retry errors accumulate rather than disappearing with a task.

Exactly-once protocols impose real costs. They persist progress and mutation evidence, coordinate checkpoints or transactions, fence owners, retain replayable input, and delay visibility until commit. Hot keys serialize. Cross-partition transactions enlarge contention and failure scope. Deduplication indexes and changelogs consume storage. An at-least-once design with idempotent or algebraically duplicate-tolerant updates can be cheaper when its actual business semantics allow it.

Correctness also depends on time and nondeterminism. Replaying a transition that called the clock, generated a random value, read mutable configuration, or queried a changing service can commit a different result even if it commits once. Windows and timers add event-time, watermark, lateness, and cleanup policies. Exactly-once state is thus a protocol plus a deterministic input contract, not a checkbox.

## Prerequisites and Retrieval

Review stateful operators in [LSDS-043](043-stateful-operators.md), checkpoint barriers in [LSDS-047](047-checkpoint-barriers.md), state recovery in [LSDS-048](048-state-snapshots-and-recovery.md), safe reprocessing in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), coordinator fencing in [LSDS-083](083-coordinator-failure.md), and checkpoint recovery in [LSDS-085](085-checkpoint-based-recovery.md).

You should understand partitions and offsets, per-key state, write-ahead logs, transactions, compare-and-swap, idempotency, snapshots, changelogs, deterministic functions, event time, watermarks, timers, leases, fencing tokens, schema evolution, and read isolation.

For diagnosis retain source identity/generation/partition/position, canonical record ID and fingerprint, job/graph/operator/key/state name, predecessor/new state version, transition/commit ID, owner epoch, mutation/timer/output digests, prepare/commit outcome, checkpoint ID, restore frontier, replay attempts, duplicate/conflict/gap decision, code/schema/config digest, and externally visible observations.

## Learning Objectives

After this module, you should be able to:

1. define exactly-once state semantics as committed-effect equivalence, not one execution;
2. separate input, attempt, transition, checkpoint, owner-epoch, and output identities;
3. atomically couple state changes with source progress and participating outputs;
4. choose ordered-frontier, deduplication, transactional, or checkpoint-based mechanisms;
5. fence stale writers and resolve ambiguous commits by stable identity;
6. reason about multi-input vectors, timers, windows, and late data;
7. capture nondeterministic and asynchronous transition inputs for replay;
8. preserve semantics across rescaling, upgrades, TTL, and state migration;
9. bound the guarantee at nonparticipating sinks and side effects; and
10. prove behavior with histories, invariants, crash points, and state/output comparison.

## Core Exposition

### Specify the guarantee boundary

Name the state being protected, the admitted inputs, the visibility point, and the failures covered. “Each committed `(topic generation, partition, offset)` affects operator state and registered event-time timers once despite worker and coordinator crash” is testable. “The pipeline is exactly once” is not.

Distinguish at-least-once execution from at-most-once commitment. Liveness ensures a valid logical input is eventually represented; safety ensures it is not represented twice. Exactly-once state requires both within a retention and failure model. Late-data policy may intentionally reject an input; that is admission semantics, not loss after admission.

### Establish stable identity

An ordered durable source can use generation, partition, and offset as transport identity if replay preserves them. A source that republishes records or assigns nondeterministic positions needs a stable producer-provided logical ID and canonical fingerprint. The identity domain must include tenant/source generation when otherwise collision is possible.

Attempt ID, worker ID, and process-local sequence are unsuitable because retries change them. The same logical identity with a different fingerprint is a conflict. Store or quarantine it; never silently treat it as a harmless duplicate.

### Define the atomic transition bundle

For a keyed transition, read one committed predecessor, compute mutation/timer/output intents, and commit them with the input progress or deduplication decision. The commit may be a database transaction, a replicated-log entry, a conditional state version, or a checkpoint that consistently couples local state and replay positions.

If state commits but progress does not, replay can apply the mutation twice. If progress commits but state does not, recovery skips the mutation. The protocol must make both visible together or make one reconstructible from the other without ambiguity. All-or-none applies to every field whose later behavior depends on the transition.

### Serialize or validate competing updates

Per-key mailboxes often serialize transitions. Transactional stores can use pessimistic locking, optimistic version checks, or a replicated log. A bundle declares expected predecessor version $v$; a conditional commit succeeds only when the current version equals $v$ and the owner epoch is current.

On conflict, recompute from the newly committed predecessor rather than blindly replaying a stale mutation. Commutative/associative merge can relax order only when the application proves its algebra, duplicate behavior, and correction semantics. `balance += amount` is not idempotent merely because it is atomic.

### Couple ordered source progress

For a single ordered partition, frontier $F_p=q$ asserts all admitted positions through $q$ are reflected in state under the source contract. Accepting $q>F_p+1$ hides a gap unless missing positions are explicitly filtered, assigned elsewhere, or represented by a sparse acknowledgement structure.

Multiple partitions need vector $F=(F_1,\ldots,F_n)$. A join may consume unequal positions and event-time frontiers from both sides; its checkpoint must preserve a consistent vector plus buffered unmatched records, timers, and watermarks. A scalar “latest offset” cannot describe this cut.

### Use checkpoint-and-replay correctly

Barrier/checkpoint engines let workers mutate local managed state during processing, then periodically snapshot state with source positions. On failure they discard post-checkpoint working mutations, restore the complete cut, and replay input. Multiple invocations collapse to a state equivalent to one run because uncommitted state is rolled back.

The proof requires a replayable source, a consistent snapshot, matching state and positions, and deterministic state effects. A local log or incremental backend may accelerate restoration without changing the semantic boundary. Recovery must not mix a newer source frontier with older state.

### Use transactional micro-batches or epochs

An engine may stage mutations and outputs for an epoch, then atomically commit them with its input-offset vector. Retrying the same epoch uses one stable transaction ID. Readers see only committed epochs, and an incomplete epoch is aborted or resumed by outcome lookup.

Large epochs amortize coordination but increase latency, rollback work, hot-key contention, and ambiguous-state recovery. Small epochs raise commit overhead. The transaction timeout, checkpoint interval, source retention, and recovery time must be mutually feasible.

### Handle timers and windows as state

A timer registration, deletion, and firing changes future computation and belongs to the state protocol. Give a logical firing identity such as `(operator,key,window,timer-domain,timestamp,generation)`. Recovery may invoke a callback again; only its committed transition may take effect once.

Event-time results depend on watermark and allowed-lateness policy. Processing-time timers depend on runtime time and need explicitly documented recovery semantics. Cleanup/TTL tombstones must be checkpointed or deterministically reconstructed, or replay can resurrect removed state or suppress valid late input.

### Capture nondeterministic inputs

Pure deterministic $\delta$ is easiest to replay. Treat clock values, random seeds, model/config versions, locale, ordering choices, and mutable dimension records as input. Persist the chosen value or lookup result with the transition when it affects future state.

Asynchronous I/O is especially risky: attempt A may receive price 10, time out, and retry as attempt B after the service changes to 12. Committing either once does not make results reproducible. Use versioned lookups, durable request/result identity, or a side-input snapshot with a named effective version.

### Fence ownership and resolve ambiguity

Partition/key ownership changes on restart and rescale. The coordinator issues monotonically ordered epoch $g$; the commit service rejects older epochs. A lease alone cannot stop a paused old worker that wakes with valid credentials.

If a commit response is lost, query the commit identity. `committed` returns the recorded outcome, `aborted` permits a policy-controlled retry, and `unknown` triggers reconciliation—not a new identity. Commit/abort and outcome lookup must be idempotent and durable across coordinator failover.

### Preserve meaning through change

State schema, serializer, code, configuration, model, topology, partitioner, and timer format participate in the transition meaning. Record compatibility digests and use stable operator/state identities. Migrate state explicitly or reject restoration; do not reinterpret old bytes under new rules.

Rescaling redistributes logical key ownership while preserving state versions, input identities, and frontiers. A cutover fences the old graph before the new graph publishes. Rollback needs a compatible retained point and must account for any new-format state or downstream output already made visible.

### Bound external effects

Managed state exactly once does not make email, payment, HTTP, file, or arbitrary database calls exactly once. A call can occur before a failed state commit and run again. Logs can contain repeated attempts even while state is correct.

Bring an output inside the atomic commit protocol, use a checkpoint-aware transactional sink, publish a durable outbox intent with stable effect identity, or make the destination enforce idempotency. State the contract separately for managed state, internal shuffles/topics, and each external destination.

### Observe and verify histories

Measure admitted records, physical attempts, committed transitions, duplicate hits, fingerprint conflicts, gaps, version conflicts, stale-epoch rejections, prepare/commit/abort/unknown outcomes, commit latency, rollback/replay volume, checkpoint age, state/changelog bytes, timer duplicates, and state/output reconciliation.

Segment by job/operator/key partition, source/generation/partition, code/schema/config version, checkpoint/epoch, failure type, restore, and time window. Persist a causal trace linking input to attempts and one commit. Fault injection must kill execution before/after each mutation, progress write, prepare, publication, acknowledgement, checkpoint, and ownership transfer.

## Definitions and Notation

Let:

- $e=(i,p,q,x)$ be logical input with identity $i$, partition $p$, position $q$, and canonical payload $x$;
- $h(e)$ be its canonical fingerprint;
- $S_v$ be committed state at version $v$;
- $\delta(S_v,e)=(\Delta S,O,T)$ be its deterministic transition;
- $B=(j,p,q,v,g,h(e),\Delta S,O,T)$ be the commit bundle;
- $g$ be the fencing epoch and $g_c$ the current accepted epoch;
- $F_p$ be partition $p$'s committed frontier and $F$ the multi-partition frontier vector;
- $D[i]$ be a deduplication/outcome record for logical identity $i$;
- $A(e)$ be the number of physical attempts and $C(e)\in\{0,1\}$ the number of committed logical effects;
- $L_c$ be commit latency and $R$ be replayed records after recovery.

Safety requires $C(e)\le1$ for each admitted identity/fingerprint, while liveness requires $C(e)=1$ eventually for every valid non-rejected $e$ within the failure model. $A(e)$ may exceed one. A frontier is meaningful only with its source generation, ordering/gap rules, and the state version it certifies.

## Mechanisms, Invariants, or Proof Structure

### Atomic-bundle proof

Assume commit linearizes one bundle only when predecessor/frontier and epoch checks pass. Publication changes state, progress, timers, participating output, and durable outcome atomically. A crash before linearization leaves none visible; a crash after leaves the outcome queryable. Therefore no crash window exposes state without corresponding progress or vice versa.

### Retry-idempotence proof

Every attempt of logical input $e$ uses the same commit identity and fingerprint. The first valid linearization records its outcome. Later identical attempts return that outcome without reapplying $\Delta S$; changed fingerprints conflict. Thus arbitrarily many attempts produce at most one committed effect.

### Checkpoint-replay equivalence proof

Restore consistent state/frontier cut $(S_k,F_k)$ and replay admitted records after $F_k$ in the required order. Deterministic transitions and atomic checkpoint publication reconstruct the same logical transition sequence as a failure-free execution. Post-checkpoint failed attempts are discarded rather than compounded.

### Fencing proof

The commit service accepts only $g=g_c$ (or the precisely defined monotonic rule) and advances $g_c$ durably at ownership transfer. Once epoch $g+1$ is installed, an epoch-$g$ attempt cannot linearize even if its lease or network session survives. This prevents split-brain publication.

### Adversarial verification

Test empty state, first input, duplicates, same-ID/different-payload, gaps, out-of-order input, hot keys, multi-input skew, simultaneous attempts, lost commit responses, worker/coordinator crash at every boundary, stale owners, checkpoint rollback, timer re-fire, late data, TTL expiry, mutable lookup, serializer/code change, rescale, source truncation, and nonparticipating effects. Require exact state/history equivalence or explicit rejection.

## Alternatives and Trade-Offs

| Design | Strength | Cost or limitation |
|---|---|---|
| At-most-once processing | Low duplicate risk | Failure can lose admitted work |
| At-least-once plus idempotent assignment | Simple and often fast | Only fits truly idempotent replacement semantics |
| Ordered frontier plus atomic state | Compact evidence for ordered partitions | Needs gap-free order and careful partition ownership |
| Per-record deduplication ledger | Handles noncontiguous stable IDs | Index/storage/retention and conflict checks |
| Checkpoint rollback and replay | Efficient for managed distributed state | Visibility delayed to checkpoints; requires deterministic replay |
| Transactional micro-batch/epoch | Atomic state, progress, and participating outputs | Coordination latency, timeout, contention, larger failure scope |
| Commutative/CRDT-style merge | Tolerates reorder/concurrency for proven algebra | Not general; removal, duplicates, and business order remain hard |
| At-least-once mode | Lower coordination cost and latency | Applications must tolerate or repair duplicate state effects |

Choose from the required state algebra, source identity/order, latency, failure domains, external boundaries, retention, and operational capability. Stronger labeling without an enforceable protocol adds no safety.

## Failure Modes and Misconceptions

1. **“The function ran once.”** Retries and speculation invalidate invocation-count claims; inspect commits.
2. **State/progress dual write.** A crash between independent writes produces a duplicate or gap.
3. **Attempt identity.** New retries evade deduplication because the identity names execution, not input.
4. **Payload conflict ignored.** Same ID with changed semantics is silently misclassified as replay.
5. **Offset gap.** Advancing a compact frontier over missing work makes recovery skip it.
6. **Mixed recovery cut.** New offsets with old state violate transition equivalence.
7. **Stale owner.** Expired leases without enforcement allow split-brain state publication.
8. **Nondeterministic replay.** Clock, random, order, config, or lookup changes state meaning.
9. **Timer outside the bundle.** Re-fired callbacks apply a second transition or disappear.
10. **Premature TTL/dedup expiry.** Historical replay is accepted as new work.
11. **Blind mutation retry.** A stale computed delta overwrites or compounds a concurrent commit.
12. **External-boundary inflation.** Managed-state semantics are claimed for uncoordinated effects.
13. **Read isolation omitted.** Readers observe prepared/partial state or uncommitted outputs.
14. **Schema reinterpretation.** Old state bytes are read under incompatible new logic.
15. **Average-only evidence.** Rare ambiguity, hot-key contention, restore, and conflict tails disappear.

## Worked Examples

### Example 1

A counter attempt increments from 9 to 10 and crashes before progress acknowledgement. Atomic state/frontier commit makes recovery either see both `10` and the advanced offset or neither; separate writes could yield 11 after replay.

### Example 2

Two attempts race on state version 30. One conditionally commits version 31; the other fails its predecessor check and returns the recorded input outcome or recomputes from 31.

### Example 3

Partition frontier is 14 and position 16 arrives. The system buffers/reorders it or records sparse completion; it does not set a gap-free frontier to 16 while 15 is unresolved.

### Example 4

A two-stream join checkpoints left frontier 90, right frontier 44, unmatched buffers, watermark 12:00, and timers. Replacing that vector with scalar 90 would skip or duplicate right-side effects.

### Example 5

An event-time timer callback is invoked twice across recovery. Both attempts use the same logical timer identity; only one state transition commits.

### Example 6

An async exchange-rate lookup returned 1.08 before failure and 1.10 on retry. Versioning and persisting the chosen rate is necessary; exactly-once commit alone cannot make the transition deterministic.

### Example 7

State TTL deletes a session at watermark 18:00. The deletion/tombstone and watermark belong to recoverable state so replay cannot resurrect the session under an earlier cleanup view.

### Example 8

Rescaling moves key `customer-7` to a new worker at epoch 12. An epoch-11 write arrives late and is rejected at the state service despite its once-valid lease.

### Example 9

A transform logs twice but one state bundle commits. Logs prove attempts, not duplicate state. A separate email sent inside the transform may still be duplicated.

### Example 10

The executable fixture applies partition-ordered transitions with stable identities and epoch fencing.

<!-- bijux-verify: {"id":"exactly-once-state","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=p0:1,p0:2,p1:1\nduplicates=p0:1\nrejected=p0:3:stale-epoch\nstate=a:8,b:7\nfrontiers=p0:2,p1:1\ncommits=3\n","stderr":""}} -->
```python
current_epoch = 2
state = {}
frontiers = {"p0": 0, "p1": 0}
outcomes = {}
accepted, duplicates, rejected = [], [], []
attempts = [
    ("p0", 1, "a", 5, 2),
    ("p0", 1, "a", 5, 2),
    ("p0", 2, "a", 3, 2),
    ("p0", 3, "a", 99, 1),
    ("p1", 1, "b", 7, 2),
]

for partition, offset, key, delta, epoch in attempts:
    commit_id = f"{partition}:{offset}"
    fingerprint = (key, delta)
    if commit_id in outcomes:
        assert outcomes[commit_id] == fingerprint
        duplicates.append(commit_id)
    elif epoch != current_epoch:
        rejected.append(f"{commit_id}:stale-epoch")
    elif offset != frontiers[partition] + 1:
        rejected.append(f"{commit_id}:gap")
    else:
        state[key] = state.get(key, 0) + delta
        frontiers[partition] = offset
        outcomes[commit_id] = fingerprint
        accepted.append(commit_id)

print("accepted=" + ",".join(accepted))
print("duplicates=" + ",".join(duplicates))
print("rejected=" + ",".join(rejected))
print("state=" + ",".join(f"{key}:{state[key]}" for key in sorted(state)))
print("frontiers=" + ",".join(f"{key}:{frontiers[key]}" for key in sorted(frontiers)))
print(f"commits={len(outcomes)}")
```

## Cross-Program Connections

- **Distributed systems:** linearization, consensus-backed logs, fencing, retries, and failure detectors define publication safety.
- **Database systems:** transactions, WAL, MVCC, isolation, conditional updates, and recovery implement atomic state transitions.
- **Streaming:** offsets, barriers, checkpoints, watermarks, timers, windows, and replay define the state/input cut.
- **Data structures:** versioned maps, logs, deduplication indexes, and sparse acknowledgement sets encode evidence.
- **Concurrency:** serialization, optimistic validation, commutative merges, and conflict retry govern competing keys.
- **API engineering:** idempotency keys and outcome lookup extend the identity discipline to participating services.
- **Platform engineering:** stable identities, rollout fencing, state migration, telemetry, and restore drills operationalize it.
- **Security:** tenant-scoped IDs, authorization epochs, tamper-evident outcomes, retention, and audit protect state.

## References

1. Apache Flink, [Fault Tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/). Current. Defines exactly-once managed-state effects, checkpoint replay, and end-to-end prerequisites.
2. Apache Flink, [Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/). Current. Documents durable-source/state prerequisites and checkpoint modes.
3. Apache Flink, [Stateful Stream Processing](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/concepts/stateful-stream-processing/). Version 2.3. Explains state persistence through checkpoint and replay.
4. Apache Flink, [Fault Tolerance Guarantees of Data Sources and Sinks](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/datastream/guarantees/). Development documentation. States connector participation boundaries.
5. Apache Flink, [Upgrading Applications and Flink Versions](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/upgrading/). Current. Documents state restoration and external-write limitations during restart.
6. Apache Kafka, [Streams Core Concepts](https://kafka.apache.org/10/streams/core-concepts/). Version 10. Documents atomic Kafka input offsets, state-store updates, and output topics.
7. Apache Kafka, [KIP-129: Streams Exactly-Once Semantics](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/68717010/KIP-129%2BStreams%2BExactly-Once%2BSemantics). Accepted. Defines state/output equivalence under failure and transactional visibility.
8. Apache Beam, [Basics of the Beam Model](https://beam.apache.org/documentation/basics/). Current. Defines per-key/window state and timers.
9. Google Cloud Dataflow, [Exactly-once in Dataflow](https://cloud.google.com/dataflow/docs/concepts/exactly-once). Current. Distinguishes repeated execution, committed in-pipeline results, late data, and side effects.
10. Akidau et al., [MillWheel: Fault-Tolerant Stream Processing at Internet Scale](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/). 2013. Describes persistent state, low watermarks, and exactly-once record processing.
11. Apache Spark, [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html). Current. Documents fault-tolerant state stores, checkpoint recovery, and changelog checkpointing.
12. Apache Spark, [State Data Source](https://spark.apache.org/docs/latest/streaming/structured-streaming-state-data-source.html). Current. Documents inspection of committed checkpoint state and state changes.

## Exercises

### Exercise 1

Construct the two crash windows created when state mutation and source offset are committed independently. Explain the duplicate and loss outcomes.

### Exercise 2

Design a commit bundle and conditional checks for a partitioned account-balance aggregator with retries, rescaling, and same-ID/different-payload conflicts.

### Exercise 3

Explain how a two-input event-time join must checkpoint source progress, buffers, watermarks, timers, and output intents to preserve exactly-once state.

### Exercise 4

An asynchronous risk lookup can change during retry. Design a deterministic and auditable state transition without assuming the service joins the engine transaction.

### Exercise 5

Design a fault-injection campaign and dashboard that distinguish invocation attempts, committed state effects, internal outputs, and external side effects.

## Answers to the Exercises

### Answer 1

If state commits first and the worker crashes before offset commit, recovery resumes at the old offset and applies the mutation again. If offset commits first and the worker crashes before state, recovery starts after the record and its mutation is lost. Atomic publication of `(mutation, frontier/dedup outcome)` eliminates the intermediate visible states; checkpoint rollback also works when both components restore from the same consistent cut.

### Answer 2

Use input identity `(source generation, partition, offset)` plus canonical account/amount/currency/event-version fingerprint, stable transition ID, expected account-state version, expected partition frontier, and current owner epoch. Atomically validate the fingerprint, epoch, predecessor, and gap rule; update the balance/version; advance the frontier; and store the outcome. Identical retry returns it, changed payload conflicts, concurrent predecessor loses and recomputes, and rescaling installs a higher epoch before the new owner commits.

### Answer 3

Persist a frontier vector for both inputs, all unmatched records and indexes, the current event-time/watermark state, every registered/fired timer identity, and participating output intents in one checkpoint/epoch. Barrier alignment or captured in-flight channels must classify every record on one side of the cut. Recovery restores the entire tuple, replays after each component frontier, and exposes only committed outputs. A scalar offset or omitted timer/buffer can skip a match or fire it twice.

### Answer 4

Give the request a stable logical identity and bind it to input/state/code/model versions. Query a version-addressable risk snapshot, or durably record the first accepted lookup result and effective version before/with the state transition. Retries retrieve that result rather than asking “latest” again. Fence owners, detect changed request fingerprints, record provenance, and define how unavailable/unknown results resolve. Any effect at the risk service remains outside the guarantee unless it independently enforces idempotency.

### Answer 5

Trace stable input IDs through all attempt IDs to one commit ID/outcome. Kill workers/coordinator before and after read, mutation, timer update, prepare, publication, acknowledgement, checkpoint, and reassignment; duplicate/reorder input; lose responses; race old/new owners; change lookups; expire TTL; and restore. Compare state, frontiers, timers, and participating outputs to a serial reference, then reconcile every external effect separately. Dashboard attempts per input, commits, duplicate/conflict/gap/stale decisions, ambiguous outcomes, replay, checkpoint/commit latency, state divergence, internal-output duplicates, and external-effect duplicates by version and failure cohort.
