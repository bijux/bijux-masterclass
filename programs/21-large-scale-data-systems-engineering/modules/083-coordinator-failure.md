---
module_id: LSDS-083
program: Large-Scale Data Systems Engineering
level: 2
module_number: 83
title: Coordinator Failure
status: complete
last_verified: 2026-09-04
---

# Coordinator Failure

## One-Page Review

### Governing question

When the scheduler, driver, job manager, resource manager, or transaction coordinator fails, how can a successor become the only effective leader, reconstruct durable control state, reconcile still-running workers and uncertain commits, resume timers and progress, and avoid both lost work and split-brain publication?

### Essential definitions

- A **coordinator** owns authoritative job control: graph, scheduling, attempt arbitration, checkpoints, commits, timers, and terminal outcome.
- A **leader term/epoch** is a monotonically ordered identifier for one period of coordinator authority.
- **leader election** selects a candidate; **fencing** makes commands from every older term ineffective.
- A **durable control log** records accepted state transitions in replay order.
- A **control snapshot** is a compact durable image of state at a known log position.
- **reconciliation** compares recovered intent with live worker, resource-manager, shuffle, checkpoint, and sink evidence.
- An **in-flight action** was requested but lacks a recovered conclusive outcome.
- **work-preserving recovery** reuses compatible running tasks or durable intermediate results after coordinator failover.
- A **standby** is a non-leading candidate prepared to acquire authority; it is not an active peer writer.
- **recovery point objective (RPO)** bounds accepted control history that may be lost; **recovery time objective (RTO)** bounds restoration time.

### Central model, mechanism, or theorem

Let durable control state at sequence $k$ be

$$Q_k=(G,J,W,A,O,C,R,T),$$

covering graph/job state, worker registrations, attempts, output winners, checkpoints/commits, resource leases, and timers. Coordinator incarnation $c=(id,term)$ may mutate protected state only when $term=term_{authority}$ and transition preconditions hold. A successor recovers

$$Q_k=replay(snapshot_j,events_{j+1..k}),$$

acquires a strictly newer term, fences earlier leaders, resolves in-flight actions by stable identity, reconciles live components, and then resumes scheduling. Election without fencing permits two leaders; fencing without durable state loses decisions; replay without reconciliation mistakes stale records for live reality.

### Critical invariants

- At most one coordinator term can make effective mutations to workers, resources, checkpoints, shuffle ownership, and sinks.
- Every durable event has job identity, monotonic sequence, term, command/request ID, precondition, payload digest, and integrity protection.
- Acknowledged decisions meet the stated durability quorum before the coordinator reports success.
- Control snapshots identify an exact log position and are complete, versioned, checksummed, and replay-compatible.
- Stable job, task, attempt, transaction, checkpoint, and resource IDs survive coordinator replacement.
- In-flight publish/commit actions are unknown until authoritative downstream status resolves them.
- Workers re-register under the new term and report inventory; their local claims never override durable winners or terminal state.
- Timers, retry budgets, leases, and deadlines recover from durable logical state without double firing or immortal extension.
- Terminal job outcomes and committed outputs never regress to running because a stale snapshot was restored.
- Failover and disaster recovery have distinct failure-domain, RPO, RTO, and data-loss claims.

### Common failures

Common failures include assuming a lease alone fences an old leader; running active-active schedulers without serialized commands; acknowledging transitions before durable replication; persisting job submission but not code/config/credentials; snapshotting state without the corresponding log offset; replaying non-idempotent effects; rescheduling every task before workers re-register; trusting a worker's old success over a committed loser decision; retrying unknown table/sink commits with new IDs; resetting attempt counters and deadlines after failover; firing restored timers twice; deleting HA state while jobs are nonterminal; restoring coordinator storage without checkpoint/shuffle/catalog dependencies; and measuring election time while ignoring reconciliation and restored progress.

### Compact example

Term 7 durably records task `t1` committed, then records `commit-requested` for `t2` before the coordinator crashes. Term 8 wins election and is accepted by workers and the sink. Replay proves `t1` complete; `t2` is not runnable because its downstream commit may already have succeeded. The successor queries the sink using `t2`'s stable transaction ID, records committed or failed, and only then proceeds. A delayed term-7 coordinator cannot cancel attempts or publish because every protected component rejects its older term.

### Connections

[LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies stable request identity, [LSDS-055](055-work-stealing-and-speculation.md) supplies attempt arbitration, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies atomic outcomes, [LSDS-079](079-catalog-and-transaction-coordination.md) supplies coordinator primitives, [LSDS-081](081-task-level-failure-recovery.md) supplies retry state, and [LSDS-082](082-worker-and-executor-loss.md) supplies worker reincarnation and inventory.

## Governing Question

Workers perform bulk computation, but the coordinator decides what work exists and which results count. It often owns the graph, resource requests, task attempts, shuffle lifecycle, checkpoints, sink commits, retries, cancellation, and final job result. Losing this process can therefore erase the explanation of ongoing work even while all workers and data remain healthy.

High availability requires more than starting another process. The new coordinator must be uniquely authoritative, load an internally consistent history, discover what happened while the old leader was unreachable, and preserve decisions already made elsewhere. The old process may revive after a pause; workers may reconnect with partial inventories; a sink may have committed after the last control-log event.

The governing question is how to define the durable state machine and failover protocol so these ambiguities are resolved safely, progress resumes efficiently, and the claimed recovery boundary is observable and testable.

## Why This Matters

Coordinator failure can affect every task in a job or every job in a cluster. A fast election followed by full job replay may still violate an RTO. Preserving running workers without knowing their epochs or assignments can instead create duplicate commits. Reliability depends on how much control state is durable and which data-plane artifacts survive independently.

The coordinator is also a transaction participant. It may have sent an output commit, checkpoint completion, resource allocation, or cancellation whose response was lost. Blind retry or rollback can duplicate output, resurrect work, or delete committed artifacts. Stable identities and downstream status lookup are mandatory.

Finally, control-plane HA has correlated dependencies: consensus store, recovery filesystem, object store, DNS, identity provider, container registry, and resource manager. Three standby processes in one broken zone or using one inaccessible storage directory do not provide effective availability.

## Prerequisites and Retrieval

Review idempotent replay in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), attempt arbitration in [LSDS-055](055-work-stealing-and-speculation.md), atomic commit in [LSDS-071](071-table-snapshots-and-atomic-commit.md), catalog coordination in [LSDS-079](079-catalog-and-transaction-coordination.md), task recovery in [LSDS-081](081-task-level-failure-recovery.md), and worker loss in [LSDS-082](082-worker-and-executor-loss.md).

You should understand replicated logs, terms/epochs, quorum, leader election, leases, fencing, deterministic state machines, write-ahead logging, snapshots, checksums, idempotency, unknown outcomes, heartbeats, resource leases, checkpoints, recovery regions, timers, RPO/RTO, and failure domains.

For diagnosis retain cluster/job identity, coordinator ID/term, election and discovery history, log sequence/commit index, snapshot identity/checksum/schema, replay range, durable job artifact locations, worker/resource inventories, checkpoint handles, request/transaction IDs, in-flight reconciliation, fencing rejections, timer reconstruction, dependency health, and failover stage timestamps.

## Learning Objectives

After this module, you should be able to:

1. Separate election, leadership discovery, fencing, durable state, replay, and reconciliation.
2. Inventory coordinator state needed to recover scheduling and transaction decisions.
3. Design a term- and sequence-bearing control log plus compatible snapshots.
4. Recover job artifacts, attempts, resources, checkpoints, timers, and terminal outcomes.
5. Reconcile live workers and external commits without duplicate publication.
6. Explain when work-preserving recovery is safe and when global restart is required.
7. Distinguish local process restart, active-passive failover, replicated control state, and disaster recovery.
8. Design upgrades and schema migration that preserve recovery compatibility.
9. Inject failure at every control transition and verify stale-leader rejection.
10. Measure election, replay, reconciliation, resumed progress, data loss, and blast radius separately.

## Core Exposition

### Coordinator state inventory

Durable state commonly includes job submission and owner, graph/plan and version, code/config/environment digests, source assignments, stage/operator state, task/attempt epochs, selected winners, resource requests/leases, worker registrations, shuffle/intermediate inventory pointers, completed checkpoints, sink/table transactions, retry budgets, timers, cancellation, and terminal result.

Classify each field as authoritative durable state, reconstructible state, live-derived evidence, or cache. Persisting too little forces replay or ambiguity; persisting every heartbeat bloats the log. Derive noisy progress from workers, but durably record decisions whose loss can change correctness or externally visible behavior.

### Election, terms, and fencing

Use a consensus-backed lease or election service to serialize leadership. On acquisition obtain a monotonically ordered term/epoch. Publish leader discovery with that term. Every mutating RPC to workers, resource manager, shuffle/checkpoint services, and sinks carries it; recipients persist or compare the greatest accepted term.

Lease renewal supports liveness but clocks, pauses, and partitions make self-belief unsafe. The old coordinator stops voluntarily when renewal fails, yet safety comes from recipient-side rejection. If a protected component cannot fence by term, route all mutation through an authority that can.

### Durable event log

Represent control changes as deterministic events: job accepted, graph installed, attempt assigned/started, output ready/winner selected, resource granted/released, checkpoint triggered/completed, transaction requested/resolved, retry charged, cancelled, terminal. Sequence them per job or shard under explicit ordering.

Append and replicate before acknowledging according to RPO. Include event schema/version, term, stable command ID, causal/precondition reference, canonical payload digest, and checksum. Replaying an event must be idempotent; arbitrary callbacks, wall-clock reads, or external calls do not belong inside pure state reconstruction.

### Snapshots and compatibility

Periodically serialize a complete control state at committed log sequence $j$. Write privately, checksum, validate by reload, then publish its pointer. Retain enough prior snapshots/log to recover from corruption and in-progress upgrades. Garbage-collect only after all readers and rollback windows no longer require them.

Recovery reads the newest compatible valid snapshot and replays the exact suffix. A snapshot without its included sequence can double-apply events; skipping a gap loses decisions. Schema migration needs deterministic defaults, versioned readers, mixed-version tests, and an explicit irreversible cutover.

### Failover state machine

Detect suspicion, elect a successor, acquire new term, fence mutations, load and verify state, replay committed events, start leader services without scheduling, discover workers/resources/dependencies, reconcile in-flight state, rebuild timers/queues, and only then resume new assignments. Publish stage progress for operators.

Order matters. Reconciliation before fencing lets the old leader race. Scheduling before replay can duplicate terminal tasks. Waiting for every worker forever blocks liveness; use bounded registration windows and later stale-incarnation handling.

### Worker reconciliation

Workers learn the new leader through authoritative discovery, authenticate, and register worker incarnation, task attempts, blocks/state, and last accepted coordinator term/commands. The successor compares reports with recovered assignments and winner records.

Keep compatible current attempts, cancel/fence obsolete ones, reconstruct last-copy artifacts, and reschedule missing work. A worker claiming success supplies output evidence; only durable coordinator/sink publication decides visibility. Deduplicate reconnects and tolerate reports arriving in any order.

### Resource reconciliation

Query the resource manager using stable allocation IDs. Adopt live compatible resources already belonging to the job; release extras; re-request missing capacity under quotas. Do not allocate duplicates merely because the coordinator's transient cache was empty.

Resource requests and releases can also have unknown outcomes. Use idempotent request identities and compare desired versus actual state. Recovered credentials/tokens must remain valid or be renewed without accidentally granting authority to the old leader.

### Checkpoints, state, and timers

Recover only checkpoints durably marked complete with all required state handles and source/sink coordination. In-progress checkpoints are aborted or resolved according to protocol; their partial files are not current state. Restore operator coordinators and worker tasks consistently.

Persist timers as logical deadline plus identity and firing state. On recovery, overdue timers are enqueued once under the new term; future timers are rescheduled. Retry budgets and backoff derive from durable first-attempt/failure history, not a fresh process clock. Clock jumps need monotonic-duration or server-time policy.

### In-flight commits and unknown outcomes

For each `requested` but unresolved checkpoint, catalog, sink, or output commit, query its authority using stable transaction ID and proposed digest. Record the discovered terminal result. If status cannot be determined, retain unknown and block incompatible retry/cleanup.

Never infer failure merely because the recovered log lacks acknowledgement. The old leader may have crashed after the external commit but before its own record. Conversely, a prepared local manifest is not proof of publication. Reconciliation closes this dual-write gap.

### Work-preserving recovery

Preserve workers and intermediates only when identities, terms, assignments, code/config, graph version, artifact integrity, and recovered state align. This can avoid restarting long batch jobs. Stateful streaming usually resumes from a completed checkpoint, though unaffected data-plane processes may be reused by runtime protocol.

If durable progress metadata is missing, incompatible, or corrupt, fall back to a known-safe checkpoint or full restart and state the loss. “Best effort” adoption without a proof can mix two executions. Work preservation is an optimization layered on safe replay.

### Deployment and upgrade models

A single process with local restart has one failure domain and depends on local disk. Active-passive standbys reduce process recovery time but require external election and state storage. A replicated state machine can make control transitions directly quorum-durable but is more complex and still must reconcile external actions.

Rolling upgrades must preserve log/snapshot/RPC compatibility and leader fencing across versions. Upgrade standbys first where supported, canary failover, then advance writers. Do not let mixed versions interpret the same event differently. Disaster recovery across regions additionally coordinates replicated logs, recovery storage, catalogs/sinks, credentials, and explicit RPO.

### Observability and verification

Measure leader terms/transitions, renewal failures, split-brain/fencing rejects, detection/election/discovery, state load/replay, worker/resource/in-flight reconciliation, timer rebuild, scheduling resume, restored progress, job impact, state bytes/events, snapshot age, unknown actions, and dependency failures. Report p50/p95/p99 and maximum by job size/runtime/version/domain.

Inject crash or partition before and after each durable append, acknowledgement, worker command, checkpoint completion, resource request, output commit, timer firing, snapshot publication, and terminal transition. Pause the old leader and let it resume after failover. Corrupt/truncate snapshots/logs, lose responses, reorder worker reports, and fail dependencies. Compare with a reference state machine and external ledgers.

## Definitions and Notation

Let:

- $Q_k$ be coordinator control state after committed event sequence $k$;
- $E_i$ be durable event at sequence $i$ and $S_j$ a snapshot through $j$;
- $c=(id,t)$ be coordinator identity and term $t$;
- $t_a$ be the greatest term accepted by a protected component;
- $I$ be unresolved in-flight external actions;
- $W$ and $R$ be recovered worker and resource inventories;
- $T_d,T_e,T_l,T_q,T_x,T_s$ be detection, election, load, replay, reconciliation, and scheduling-resume times;
- $RPO$ be maximum committed control history loss and $RTO=T_s-T_d$;
- $B_p$ and $B_r$ be preserved and recomputed work bytes or compute-seconds;
- $U$ be unknown actions remaining after bounded reconciliation.

Failover stage latency should not be summed from unrelated percentiles; measure end-to-end histories. Work-preservation ratio $B_p/(B_p+B_r)$ needs a declared unit and eligible scope. Zero unknowns is meaningful only if every requested external action was inventoried.

## Mechanisms, Invariants, or Proof Structure

### Single-effective-leader proof

Election authority serializes terms and protected recipients remember greatest accepted term $t_a$. New leader uses $t_2>t_1$ and advances recipients. Any later command from old leader carries $t_1<t_a$ and is rejected. Multiple processes may believe they lead, but at most one term can make effective mutations, provided every correctness-bearing recipient enforces the comparison.

### Deterministic-replay proof

Snapshot $S_j$ is a valid serialization of $Q_j$ and events $E_{j+1..k}$ are complete, ordered, integrity-checked deterministic transitions. Applying each exactly by sequence reconstructs the same $Q_k$. Stable IDs make repeated load/replay harmless. External effects are referenced, not re-executed, during replay.

### Unknown-action reconciliation proof

For action identity $x$, downstream authority stores at most one result for its request digest. The successor queries $x$: committed records success, definitely absent/failed permits protocol-defined retry with the same identity, and indeterminate remains blocked. Therefore failover does not convert missing acknowledgement into duplicate publication.

### Terminal-monotonicity proof

Terminal outcome is a durable state transition at sequence $k$. Snapshots/log replay includes it, and transition rules forbid terminal-to-running movement. Worker reports or stale leader commands with earlier causal sequence cannot supersede it. Thus coordinator replacement cannot resurrect a finished, failed, or cancelled job.

### Adversarial verification

Test crash at every state transition, lease expiry under pause, two leader candidates, stale commands, corrupt/gapped log, incompatible snapshot, worker/resource reconnect races, completed/partial checkpoints, output timeout-after-commit, duplicate timer, reset retry budget, terminal-job report, dependency outage, upgrade rollback, and regional failover. Require one effective authority and exact or explicitly bounded recovery.

## Alternatives and Trade-Offs

**Cold process restart** is simple but lengthens recovery and shares a host/disk domain. **Warm standbys** shorten startup but still need election and durable state. **Replicated control state machines** minimize acknowledged-state loss but increase protocol and operational complexity.

**Event sourcing** gives audit and deterministic reconstruction but needs schema discipline, compaction, and replay control. **Database snapshots/rows** simplify queries but must preserve transactional ordering and external-action identities. Many systems combine a compact snapshot with a log suffix.

**Restart all work** is conservative and simple when sources/sinks are replay-safe. **Work-preserving failover** saves compute but requires durable progress and reconciliation. **Worker adoption** lowers latency while increasing protocol surface.

**Short leader leases** reduce takeover delay but amplify false elections under pause/network jitter. **Long leases** reduce churn but extend unavailability. Fencing preserves safety across either choice.

**Synchronous durable logging** increases control latency but tightens RPO. **Asynchronous persistence** improves throughput while explicitly risking acknowledged control-state loss; it cannot claim zero RPO.

## Failure Modes and Misconceptions

1. **Election creates one leader.** Without fencing, an old leader can still mutate.
2. **Lease loss stops the process.** Paused or partitioned code may resume.
3. **Standby count equals availability.** Shared dependencies and zones dominate.
4. **Worker state can reconstruct every decision.** Workers do not own global winners or terminal outcomes.
5. **Persisted job graph is sufficient.** Attempts, checkpoints, transactions, timers, and budgets matter.
6. **Acknowledged means durable.** Only if the protocol persisted before response.
7. **Snapshot alone is current.** Its log position and suffix are required.
8. **Replay may call external APIs again.** It should reconstruct intent and reconcile by ID.
9. **Missing acknowledgement means failure.** The external action may have committed.
10. **All workers should be killed on failover.** Compatible work can sometimes be adopted.
11. **All workers should be preserved.** Stale/incompatible attempts must be fenced.
12. **Timer recovery starts durations over.** That extends deadlines and retry budgets.
13. **Checkpoint files imply completion.** Coordinator completion metadata is required.
14. **Fast election means fast recovery.** Replay and reconciliation may dominate.
15. **Local disk backup provides HA.** It shares process/host failure domains.
16. **Active-active scheduling is free availability.** Command ordering and duplicate effects become harder.
17. **Rolling upgrade cannot affect recovery.** Event/RPC schemas may diverge.
18. **Regional restore is ordinary failover.** RPO and external dependency consistency differ.

## Worked Examples

### Example 1

Term 12 leader pauses; term 13 is elected and workers accept it. Term 12 resumes and sends cancel. Workers reject 12, so the current attempts remain valid.

### Example 2

Snapshot covers events through 1,000 and log begins at 1,001. Recovery verifies both, replays through committed 1,120, and refuses a snapshot claiming 1,010 when event 1,006 is missing.

### Example 3

Worker reports attempt `a3` output ready, but durable winner is `a2`. Success evidence from `a3` is retained for diagnosis then fenced/cleaned; it cannot replace `a2`.

### Example 4

Resource request `r7` was recorded before crash. The resource manager reports two live allocations for `r7`; successor adopts them instead of requesting duplicates.

### Example 5

Checkpoint 90 has all handles and a completed event. Checkpoint 91 has files but only a triggered event. Recovery uses 90 and later cleans uncommitted 91 after unknown-state checks.

### Example 6

Retry deadline was 12:05 and failover ends at 12:07. Recovery enqueues the overdue retry once; it does not create a new five-minute delay or fire from both leaders.

### Example 7

Table commit `tx42` succeeded but response was lost. Successor finds `tx42` in catalog history and records completion rather than rebuilding output.

### Example 8

Most batch workers retain verified shuffle. Reconciliation adopts their current attempts and blocks, so only work after the last durable coordinator progress snapshot is reconstructed.

### Example 9

Three standbys and the consensus service occupy one zone. A zonal outage removes all; replica count did not create cross-zone availability.

### Example 10

The executable fixture replays durable control events and identifies an unresolved commit for reconciliation.

<!-- bijux-verify: {"id":"coordinator-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"last_sequence=5\ncommitted=t1\nreconcile=t2\nrunnable=none\nnext_term=8\n","stderr":""}} -->
```python
events = [
    (1, "submit", "t1"),
    (2, "assign", "t1"),
    (3, "committed", "t1"),
    (4, "submit", "t2"),
    (5, "commit-requested", "t2"),
]
state = {}
for sequence, action, task in events:
    state[task] = action

committed = sorted(task for task, action in state.items() if action == "committed")
reconcile = sorted(task for task, action in state.items() if action == "commit-requested")
runnable = sorted(task for task, action in state.items() if action == "submit")

print(f"last_sequence={events[-1][0]}")
print(f"committed={','.join(committed) or 'none'}")
print(f"reconcile={','.join(reconcile) or 'none'}")
print(f"runnable={','.join(runnable) or 'none'}")
print("next_term=8")
```

## Cross-Program Connections

- **Distributed systems:** consensus, terms, leases, fencing, logs, snapshots, quorum, and failure detectors define leadership.
- **Database systems:** WAL, checkpoints, transaction recovery, commit records, and monotonic terminal state inform control recovery.
- **Operating systems:** process pauses, signals, clocks, file durability, and crash consistency create ambiguity.
- **Streaming:** operator coordinators, barrier checkpoints, source offsets, timers, and sink transactions require aligned recovery.
- **Scheduling:** worker adoption, resource reconciliation, quotas, attempt winners, and retry budgets restore progress.
- **Platform engineering:** zones, standby placement, dependency SLOs, upgrades, backup, and incident response determine availability.
- **Security:** authenticated election, term-bound commands, credential renewal, audit integrity, and least privilege protect failover.
- **Formal methods:** deterministic state machines, histories, linearization, invariants, and model checking test safety.

## References

1. Apache Flink, [High Availability Overview](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/ha/overview/). Current. Defines leader election, discovery, and persisted recovery state.
2. Apache Flink, [Kubernetes HA Services](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/ha/kubernetes_ha/). Current. Documents leader state and durable recovery storage.
3. Apache Flink, [ZooKeeper HA Services](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/ha/zookeeper_ha/). Current. Documents quorum-backed leadership and recovery configuration.
4. Apache Flink, [Batch Progress Recovery](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/batch/recovery_from_job_master_failure/). Current. Describes coordinator events, retained intermediates, and worker reconnection.
5. Apache Flink, [Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpointing_under_backpressure/). Current. Documents checkpoint progress and recovery-sensitive behavior.
6. Apache Flink, [Metrics](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/). Current. Defines coordinator, job-state, checkpoint, and resource metrics.
7. Apache Spark, [Standalone Mode](https://spark.apache.org/docs/latest/spark-standalone.html). Current. Documents master recovery, ZooKeeper standbys, and worker/application reconnection.
8. Apache Spark, [Running on YARN](https://spark.apache.org/docs/latest/running-on-yarn.html). Current. Documents driver/application-master deployment, attempts, and recovery configuration.
9. Apache Hadoop YARN, [ResourceManager Restart](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/ResourceManagerRestart.html). Current. Documents persisted application state and work-preserving recovery.
10. Apache Hadoop YARN, [ResourceManager High Availability](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/ResourceManagerHA.html). Current. Documents active/standby leadership, fencing, and failover.
11. Kubernetes, [Leases](https://kubernetes.io/docs/concepts/architecture/leases/). Current. Documents lease objects for heartbeats and leader election.
12. etcd, [API](https://etcd.io/docs/v3.6/learning/api/). Version 3.6. Defines revisions, transactions, leases, watches, and linearizable coordination primitives.
13. Diego Ongaro and John Ousterhout, [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf). 2014. Defines terms, leader election, replicated logs, commitment, and safety.

## Exercises

### Exercise 1

List the minimum durable state needed to recover a coordinator managing batch attempts, shuffle blocks, retry budgets, a completed checkpoint, and a table commit whose request was sent but not acknowledged.

### Exercise 2

Old leader term 20 pauses, term 21 takes over, and term 20 resumes. Design the checks required at workers, resource manager, checkpoint service, and sink so term 20 cannot cause harm.

### Exercise 3

A control snapshot claims sequence 5,000, the retained log starts at 5,002, and event 5,001 cannot be found. Explain the safe recovery choices and what must not happen.

### Exercise 4

Design worker and resource reconciliation after failover when some attempts are running, some workers are missing, one output winner is durable, and two allocation requests have unknown responses.

### Exercise 5

Design a failover experiment and dashboard that separates election time, state replay, reconciliation, resumed scheduling, restored useful progress, and end-to-end RTO.

## Answers to the Exercises

### Answer 1

Persist job/run identity and owner; graph, code/config/environment digests; logical tasks and attempt/epoch assignments; durable shuffle inventory pointers and selected output winners; attempt failure counts, first-failure times, backoff/deadlines, and remaining budgets; checkpoint ID, completion record, source/state/sink handles; resource request/allocation identities; and the table transaction's stable ID, request digest, target/base, staged objects, and `requested` state. Include coordinator term, event sequence/checksum/schema, terminal/cancellation state, and credentials or renewal metadata. Running worker/block claims can be reconciled live, but correctness-bearing decisions cannot be guessed.

### Answer 2

The election authority issues 21 and every mutating recipient persists greatest accepted term. Workers reject assignments, cancels, winner decisions, and block registrations below 21; the resource manager rejects acquire/release requests below 21 or routes them through an idempotent term-aware authority; checkpoint service rejects trigger/complete/abort from 20; sink rejects prepare/commit/abort for stale term while still resolving stable transaction IDs. Term 21 authenticates and reconciles before acting. The old leader also self-terminates on lease loss, but recipient-side comparison supplies safety when it cannot observe that loss.

### Answer 3

The state cannot be proven complete: replaying from 5,002 leaves an unknown transition, while pretending the snapshot includes 5,001 may lose a decision. Search replicated/backup log copies and prior valid snapshot plus a complete suffix. If none yields a gap-free history, fall back to a documented earlier recovery point whose external actions can be reconciled, or stop for repair with explicit RPO impact. Do not resume scheduling from 5,000, synthesize event 5,001, skip it, or re-execute external effects without stable-ID status checks.

### Answer 4

Acquire/fence the new term, replay durable state, and pause new scheduling. Ask authenticated workers for incarnation, attempts, and block inventories; adopt only assignments matching job/graph/code/epoch, cancel stale attempts, retain the durable winner regardless of loser reports, and derive recovery regions for missing workers/last-copy blocks. Query the resource manager by each stable request ID: adopt compatible granted allocations, record definitive failures for retry under the same logical request, and keep indeterminate requests blocked rather than duplicate them. Rebuild desired-minus-actual capacity under quotas, record reconciliation events, then resume.

### Answer 5

Inject crash, pause, and partition before/after durable events, checkpoint completion, allocation request, output commit, timer firing, and terminal transition; let the old leader resume after takeover. Record $T_d$, election/term acquisition, discovery, snapshot load, replay completion, worker/resource/commit reconciliation, timer rebuild, first new assignment, and return to pre-fault useful throughput. Graph stage and end-to-end percentiles, events/bytes replayed, workers/attempts/blocks adopted, work preserved/recomputed, unknown actions, stale-term rejections, duplicate-effect checks, and affected jobs. Assert exact final state and one effective leader; fast election alone is not the RTO result.
