---
module_id: LSDS-081
program: Large-Scale Data Systems Engineering
level: 2
module_number: 81
title: Task-Level Failure Recovery
status: complete
last_verified: 2026-09-04
---

# Task-Level Failure Recovery

## One-Page Review

### Governing question

When one distributed task attempt fails, which work must be retried, which outputs and state may be reused, how is one winner committed, and how can the system distinguish transient recovery from deterministic failure without duplicating external effects or turning local faults into job-wide replay storms?

### Essential definitions

- A **logical task** is one unit of required work identified independently of any execution attempt.
- A **task attempt** is one execution of a logical task under an attempt ID, epoch, input assignment, code/config digest, and resource placement.
- A **recovery region** is the smallest dependency region that must restart to reconstruct a valid execution state.
- A **materialization boundary** durably records intermediate output so downstream recovery need not replay its producers.
- **lineage recovery** deterministically recomputes a lost partition from recorded dependencies and stable inputs.
- **co-failing tasks** restart together because pipelining or shared state prevents independent reuse.
- An **output commit protocol** selects one attempt's complete output and prevents losers or retries from becoming visible.
- A **retry budget** bounds attempts, elapsed time, failure rate, or consumed resources for a logical scope.
- A **poison input** deterministically fails compatible attempts until data, code, or policy changes.
- **speculation** runs redundant attempts for suspected slowness; it is not proof that the original failed.

### Central model, mechanism, or theorem

Let execution graph $G=(V,E)$ contain logical tasks and edges labeled pipelined, replayable, or durably materialized. Attempt $a$ of task $v$ executes immutable assignment $I_v$ under epoch $e$ and produces attempt-scoped output $O_{v,a}$. On failure, recovery set $R(v)$ is the least valid region containing the failed/co-failing task and every producer or consumer whose required state cannot be reconstructed across a durable boundary.

Correct recovery requires two properties:

$$Result(retry(R),S_c)=Result(reference,S_c)$$

for a valid checkpoint/materialized state $S_c$, and

$$\sum_a visible(O_{v,a})=1$$

for every successfully completed logical task. The first is replay equivalence; the second is winner-only publication. Determinism, replayable sources, checkpoint compatibility, attempt isolation, fencing, and transactional or idempotent sinks are premises—not consequences of retry.

### Critical invariants

- Logical task identity, attempt identity, execution epoch, input assignment, and output identity are distinct and durably traceable.
- An attempt reads one immutable input/state version and code/config/environment digest.
- Recovery scope follows dependency and durability boundaries, not merely the process that reported the error.
- Partial attempt output is private until commit, or the sink can idempotently/transactionally neutralize replay.
- At most one compatible attempt wins each logical output; late or speculative losers are fenced and cleaned safely.
- Reused intermediate output has validated completeness, checksum, producer identity, epoch, partitioning, and retention.
- Stateful recovery restores a mutually consistent checkpoint and source position before replay.
- Retries are bounded, classified, backoff-aware, and do not conceal deterministic application or data errors.
- Cancellation propagates to running attempts, outstanding I/O, retries, and commit operations without revoking already committed truth.
- Metrics distinguish logical failures, attempt failures, retries, recovered work, recomputed work, duplicate effects, and terminal jobs.

### Common failures

Common failures include retrying only the reporting process while its pipelined region is inconsistent; reusing an incomplete shuffle partition; naming outputs only by logical task so attempts overwrite one another; allowing a timed-out loser to publish after replacement; treating user-code exceptions as transient forever; retrying a non-replayable source; restoring state without matching source offsets; assuming deterministic output despite time, randomness, locale, or external lookup drift; incrementing an external counter inside replayable work; counting speculative losers as outages; excluding healthy hosts after poison-data failures; and raising retry counts until a system merely fails more slowly and expensively.

### Compact example

Tasks `extract`, `parse`, and `shuffle-write` form one pipelined region; the completed shuffle is a durable boundary before `aggregate` and `publish`. If `parse` fails before the shuffle commit, all three tasks restart because their in-flight state and output cannot be reused, while the downstream region has not yet acquired valid input. Each retry writes attempt-scoped shuffle blocks. The coordinator validates completeness and selects one attempt set. If the same record fails three compatible placements with the same signature, classification shifts from host fault toward deterministic poison input instead of endlessly excluding workers.

### Connections

[LSDS-043](043-stateful-operators.md) supplies state semantics, [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies replay safety, [LSDS-031](031-shuffle-architecture.md) supplies intermediate durability, [LSDS-055](055-work-stealing-and-speculation.md) supplies redundant attempts, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies publication, and [LSDS-073](073-optimistic-concurrency.md) supplies conditional validation.

## Governing Question

Large jobs contain thousands or millions of task attempts, so some process, disk, network path, input block, runtime, or user function will fail. Restarting the whole job for every isolated fault wastes successful work. Retrying only the failed process can be incorrect when its output was pipelined, state was shared, or downstream consumers observed partial data.

The recovery unit is therefore a semantic dependency region. Durable shuffle blocks, checkpoints, replayable sources, and committed outputs can stop propagation. Pipelined channels, aligned state, unavailable partitions, and coupled operators expand it. The scheduler must combine this graph with exact attempt and output state.

The governing question is how to calculate that scope, reconstruct it reproducibly, arbitrate attempts, handle side effects, and stop retrying when evidence says the failure is permanent or the recovery cost exceeds policy.

## Why This Matters

Fine-grained recovery is a principal reason distributed data systems can finish despite routine faults. It lowers mean recovery time and protects completed compute. But every retry repeats code and may repeat reads, writes, API calls, state mutations, metrics, or notifications. “The framework retries tasks” is not an end-to-end correctness guarantee.

Recovery also shapes architecture. Ephemeral pipelining improves normal-path latency but enlarges co-failure regions. Durable shuffle narrows replay but costs storage and commit coordination. Small bundles reduce lost work but add scheduling and checkpoint overhead. Local state speeds recovery but cannot replace durable primary state after node loss.

Poor classification produces retry storms, noisy-neighbor incidents, quarantined healthy capacity, and delayed diagnosis. Operators need evidence that separates infrastructure transience, resource mismatch, corrupt input, deterministic code, protocol incompatibility, and sink-commit ambiguity.

## Prerequisites and Retrieval

Review stateful operators in [LSDS-043](043-stateful-operators.md), replay in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), shuffle durability in [LSDS-031](031-shuffle-architecture.md), work stealing/speculation in [LSDS-055](055-work-stealing-and-speculation.md), snapshots in [LSDS-071](071-table-snapshots-and-atomic-commit.md), and OCC in [LSDS-073](073-optimistic-concurrency.md).

You should understand DAGs, partitions, attempts, epochs, deterministic replay, lineage, shuffle, checkpoints, barriers, heartbeats, leases, fencing, backoff, idempotency, transactions, checksums, resource limits, cancellation, and failure domains.

For diagnosis retain job/stage/task/attempt/epoch IDs, graph and edge durability, assignment and input versions, code/config/container digest, checkpoint/source offsets, host/executor, resource request/usage, heartbeat and exception chain, output inventory/checksums, commit decision, retry timeline, failure signature, and external-effect identity.

## Learning Objectives

After this module, you should be able to:

1. Separate logical tasks, attempts, epochs, assignments, and committed outputs.
2. Derive recovery regions from pipelining, state, lineage, and materialization boundaries.
3. Decide when intermediate data is reusable and when producers must recompute it.
4. Design attempt-scoped output and winner-only commit protocols.
5. Make source, state, and sink behavior safe under replay.
6. Classify transient, resource, deterministic, poison-data, and unknown failures.
7. Configure bounded retries, backoff, exclusion, and escalation by failure evidence.
8. Distinguish speculation, retry, rescaling, and job restart semantics.
9. Test adversarial timing, partial output, late attempts, and commit ambiguity.
10. Measure recovery effectiveness, amplification, correctness, and blast radius.

## Core Exposition

### Task and attempt state machine

A logical task moves through pending, running attempts, committed success, terminal failure, or cancellation. Attempts move through assigned, launched, running, output-ready, commit-authorized, committed, failed, superseded, or lost. Only the coordinator's durable logical decision completes the task.

Identity includes job/run, stage/operator, logical partition/bundle, attempt, and execution epoch. Reusing a task number after graph regeneration without the epoch can make stale messages and blocks look current. Heartbeat loss is suspicion, not proof of process death; duplicate execution is normal during uncertainty.

### Recovery-region construction

Label edges by recoverability. A durable verified shuffle boundary allows a downstream task to retry without its producer. A lost shuffle partition follows lineage to its producers. Pipelined operators often co-fail because no reusable boundary separates them. Stateful streaming commonly restarts the affected region from a consistent checkpoint so channels and state agree.

Compute the least closed region satisfying every missing input and state dependency. Then validate scheduler capabilities: some runtimes restart all tasks, some a pipelined region, some a bundle, and some preserve finished batch partitions. Advertised scope must match actual configuration and version.

### Reusable intermediate results

Reuse requires a complete committed artifact, stable logical producer/epoch, exact partitioning and serialization contract, checksum, accessible replicas, and retention through all consumers. A worker's “finished” message is insufficient if its local disk vanished or the coordinator never committed the block inventory.

Track materialization state separately from task state. On executor loss, invalidate only blocks whose durable availability fell below policy, then propagate through consumers. Remote shuffle or replicated exchange can narrow recomputation but adds metadata, lifecycle, and consistency failure modes.

### Determinism and replay

Lineage recomputation assumes stable inputs and semantically repeatable transforms. Pin files/snapshots, schema, locale/time zone, libraries, configuration, and external reference versions. Seed randomness from logical identity when randomness belongs to semantics. Avoid current time and unordered iteration where output identity matters.

Bitwise equality may be unnecessary if a declared semantic equivalence tolerates floating-point order changes, but the contract must be explicit. A retry on changed input is a new computation, not recovery. Nondeterministic upstream output can make downstream partitioning, aggregates, and deduplication diverge.

### Attempt output and commit

Each attempt writes to unique private names or transactional identities and produces a manifest of files, lengths, checksums, records, and partition coverage. The coordinator chooses one compatible complete attempt per logical task. Publication conditionally records winners or commits the job/table as a whole; losers cannot overwrite winners.

Commit calls can be duplicated and responses lost. Make commit idempotent by logical output/transaction ID and request digest. Resolve unknown outcome before promoting another attempt or deleting artifacts. Cleanup is delayed, reachability-aware, and safe if invoked repeatedly.

### Stateful and streaming recovery

Restore operator state and source positions from the same completed checkpoint. Discard state changes, timers, and outputs after it unless the protocol recorded them as committed. Replay sources from the checkpointed position. Exactly-once state means effects on managed state are equivalent to once, not that user code physically executed once.

End-to-end exactly-once additionally needs replayable sources and transactional or idempotent sinks. Region recovery must respect checkpoint barrier topology and coordinator state. Local checkpoint copies improve speed when placement survives, but durable primary copies remain authority.

### External side effects

Task code that sends email, charges money, increments a remote counter, or appends without identity may repeat. Prefer emitting intent to a transactional sink/outbox committed with task/job progress. Otherwise use stable idempotency keys and a service that records result by key.

Do not mistake “attempt succeeded” for “effect committed.” Model prepare, commit, abort, and unknown outcomes. A speculative loser may have performed the effect even when its output is discarded. Metrics and logs should tolerate duplicates or label attempt identity.

### Failure classification

Classify transport timeout, worker/process loss, preemption, disk corruption, unavailable input, OOM/resource limit, user exception, data decode/validation, assertion, permission, quota, protocol/version, cancellation, and commit unknown. Preserve the deepest causal chain and stable signature.

Retry transient placement/service failures across suitable domains. Resource failures may need more memory, smaller partitions, spill, or skew handling—not identical retry. Reproducible user/data failures should fail fast, quarantine policy-approved records, or route to repair. Permission and protocol errors require configuration change.

### Retry policy and containment

Budgets can cap attempts per logical task, failures per interval, total job retries, elapsed recovery time, recomputed bytes, or cost. Use capped exponential backoff with jitter for shared dependencies. Immediate retry on a new host can be appropriate for host-specific loss; do not stampede a degraded service.

Exclusion needs evidence and expiry. A host with repeated infrastructure faults may be quarantined; hosts encountering the same poison record are victims, not causes. Bound concurrent recovery so failure does not consume all capacity and starve healthy jobs. Escalate with a compact reproducer and retained artifacts.

### Speculation and stragglers

Speculation launches redundant attempts because progress is unusually slow, not because failure is proven. Winner arbitration and side-effect safety must already support duplicate execution. Compare within relevant task cohorts and account for skew, locality, cold cache, and heterogeneous hardware.

Killing the original too early can discard the only viable attempt. Limit speculative copies and suppress them for non-idempotent tasks or scarce resources. Report speculative wins, losses, and wasted work separately from failure recovery.

### Cancellation and cleanup

Job/stage cancellation stops scheduling new retries and propagates tokens to running compute, I/O, shuffle fetch, and commit waits. Attempts check cancellation at safe boundaries and release leases/resources. A cancellation racing a completed durable commit cannot rewrite history; return the committed outcome.

Private attempt output remains until winner/unknown decisions and retention horizons make deletion safe. Cleanup uses exact inventories rather than broad prefixes, is idempotent, and cannot delete a winning artifact referenced by a recovered coordinator.

### Observability and verification

Measure logical tasks, attempts, failures by class/signature, attempts per success, recovery-region size, replayed records/bytes/time, preserved work, output-commit conflicts/unknowns, duplicate-effect detections, backoff, exclusion, local/remote restore, recovery latency, and terminal rate. Segment by job/stage/operator, code version, input cohort, host/domain, resource class, sink, and scheduler version.

Use deterministic fault injection at read, compute, shuffle write, acknowledgement, state snapshot, sink prepare, commit request, and response. Kill workers before/after output readiness; corrupt or remove blocks; delay heartbeats; resume fenced attempts; duplicate messages; lose commit responses; and replay poison inputs. Compare outputs and external effects with a failure-free reference.

## Definitions and Notation

Let:

- $G=(V,E)$ be the logical execution graph;
- $v\in V$ be a logical task and $a$ an attempt number;
- $e$ be an execution epoch and $I_v$ the immutable assignment;
- $O_{v,a}$ be attempt-scoped output and $W_v$ its selected winner;
- $R(f)\subseteq V$ be the recovery region for failure $f$;
- $S_c$ and $P_c$ be checkpoint state and matching source positions;
- $B_r$ be bytes recomputed and $B_p$ bytes of prior work preserved;
- $T_r$ be time from detected failure to restored progress;
- $A_v$ be attempts for logical task $v$ and $K_v$ its cap;
- $d_k=\min(d_{max},d_0 2^k)+J_k$ be retry delay with jitter;
- $z$ be an epoch/fencing token accepted by output/state services.

Attempt amplification is $\sum_v|A_v|/|V|$ only for a declared job scope. Recovery amplification may be $B_r/B_{lost}$, but zero/unknown denominators need separate labels. Preserved work is not recovered output unless its integrity and compatibility were validated.

## Mechanisms, Invariants, or Proof Structure

### Recovery-closure proof

Start with failed/co-failing tasks. For each required input or state unavailable at a durable compatible boundary, add its producer/region; for each in-flight pipelined dependency invalidated by the failure, add its coupled task. Iterate to a fixed point. Tasks outside the closure depend only on durable valid artifacts or have not observed invalid output, so restarting the closure suffices under deterministic replay.

### Winner-only publication proof

Attempts write disjoint private outputs. A conditional coordinator record changes logical task $v$ from uncommitted to winner $a$. Only artifacts named by that record enter final publication, and output services reject stale epoch $z$. Competing or late attempts cannot change the selected record, so at most one attempt's output becomes visible.

### Checkpoint-replay proof

A completed checkpoint atomically associates operator state $S_c$ with source positions $P_c$. Recovery discards uncommitted post-checkpoint effects, restores $S_c$, and replays from $P_c$. Deterministic transitions reconstruct equivalent managed state. End-to-end equivalence further requires sinks to commit transactionally with the checkpoint or deduplicate stable effect identities.

### Retry-termination argument

Every retry consumes an attempt/time/rate/cost budget. Success commits one winner; classified nonretryable failure terminates immediately; exhausting any governing budget produces terminal failure with evidence. Thus repeated deterministic failure cannot loop indefinitely, assuming budget accounting itself is durable across coordinator recovery.

### Adversarial verification

Test zero/one/many attempts, process and host loss, lost/corrupt shuffle blocks, partial output, delayed acknowledgement, duplicate success, speculative overlap, stale epoch, checkpoint corruption, source drift, sink timeout-after-commit, poison record, OOM/skew, permission denial, cancellation race, and coordinator restart. Require exact result/effect equivalence or explicit terminal classification.

## Alternatives and Trade-Offs

**Whole-job restart** is simple and restores one global boundary but discards healthy work. **Region restart** narrows cost but requires dependency/durability tracking. **Task-only retry** is cheapest when inputs and outputs are independently replayable; it is invalid for coupled state.

**Lineage recomputation** saves storage and supports elastic replay but can cascade through long graphs. **Durable materialization** bounds replay and enables reuse but costs I/O, commits, retention, and cleanup. **Local recovery** reduces latency on surviving hosts; **remote durable state** survives host loss.

**Small bundles/tasks** reduce retry loss and expose parallelism but add scheduling and commit overhead. **Large tasks** amortize overhead but increase stragglers, memory pressure, and lost work.

**Fixed retries** are understandable but ignore time and shared-failure bursts. **Failure-rate/exponential policies** adapt better but require careful windows, caps, jitter, and durable accounting. **Fail-fast** protects capacity for deterministic faults but needs high-confidence classification.

**Transactional sinks** provide strong composition but require protocol support. **Idempotent effects** are simpler when stable keys exist. **Compensation** is a later semantic action and does not erase the interval in which the original effect was visible.

## Failure Modes and Misconceptions

1. **Task ID equals attempt ID.** Retries and speculation create multiple attempts.
2. **Heartbeat loss proves death.** Pauses and partitions create duplicates.
3. **Retry only the failed process.** Coupled dependencies determine scope.
4. **Finished output is reusable.** It needs durable commit and integrity.
5. **Lineage guarantees determinism.** Inputs and transformations may drift.
6. **Retry executes once.** Physical execution is commonly repeated.
7. **Exactly-once state means one invocation.** It means equivalent managed effects.
8. **Framework retry protects every API call.** External effects need their own protocol.
9. **Logical task output path is safe.** Attempts can overwrite or interleave.
10. **First success message wins safely.** Completeness and conditional commit matter.
11. **Timeout means commit failed.** Outcome may be unknown.
12. **More retries improve reliability.** Deterministic failures amplify load.
13. **OOM is transient.** Identical resources and input usually reproduce it.
14. **Every failed host is unhealthy.** Poison input travels between healthy hosts.
15. **Speculative loser is a failure.** It may simply finish later.
16. **Local checkpoint is durable.** Host loss can remove it.
17. **Cancellation can undo committed output.** It cannot rewrite durable truth.
18. **Cleanup by prefix is harmless.** Winner and unknown artifacts may share it.

## Worked Examples

### Example 1

Attempt `stage4/task9/a1` loses heartbeat. Scheduler launches `a2`; `a1` later returns. Epoch fencing and winner CAS allow only one output manifest to commit.

### Example 2

A map output block is lost after its producer exited. Lineage pins the original input split and code digest, recomputes that map partition, and reruns only reducers needing the replacement block.

### Example 3

Three fused transforms process one Beam bundle. An element failure discards the whole bundle output and retries its elements; per-element side effects would duplicate without idempotency.

### Example 4

One task OOMs on the same skewed partition on three hosts. Host exclusion wastes capacity. Split the partition, increase/spill memory, or repair the algorithm.

### Example 5

State checkpoint 80 contains source offsets 1,000–1,999. Restoring its state with offsets from checkpoint 81 either duplicates or skips effects; the pair is indivisible.

### Example 6

Attempt writes three of four files and crashes. Its private manifest never reaches complete, so none becomes visible. Retry writes a separate complete set and wins.

### Example 7

Sink commit succeeds but response is lost. The retry asks by transaction ID and learns it committed; issuing a new ID would duplicate the batch.

### Example 8

A remote shuffle retains verified blocks after worker loss, so reducers continue. If one block checksum fails, lineage invalidates that partition and its affected consumers.

### Example 9

Retry budget permits four attempts or ten minutes. A shared-service outage uses jittered backoff; the time budget expires first and produces a terminal classified failure.

### Example 10

The executable fixture computes the pipelined region restarted after a parse-task failure.

<!-- bijux-verify: {"id":"recovery-region","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"failed=parse\nrecovery_region=extract,parse,shuffle-write\nwork_units=100\noutside_region=aggregate,publish\n","stderr":""}} -->
```python
tasks = {"extract": 20, "parse": 30, "shuffle-write": 50, "aggregate": 80, "publish": 10}
pipelined = [("extract", "parse"), ("parse", "shuffle-write"), ("aggregate", "publish")]
failed = "parse"

region = {failed}
changed = True
while changed:
    changed = False
    for left, right in pipelined:
        if (left in region) != (right in region):
            region.update((left, right))
            changed = True

outside = set(tasks) - region
print(f"failed={failed}")
print(f"recovery_region={','.join(sorted(region))}")
print(f"work_units={sum(tasks[name] for name in region)}")
print(f"outside_region={','.join(sorted(outside))}")
```

## Cross-Program Connections

- **Distributed systems:** failure suspicion, leases, fencing, consensus, idempotency, and partial failure shape attempt control.
- **Operating systems:** processes, signals, exit status, OOM killing, cgroups, local storage, and cleanup provide failure evidence.
- **Database systems:** transactions, WAL, savepoints, recovery, and exactly-once effects inform output commit.
- **Streaming:** checkpoints, barriers, replayable sources, timers, and transactional sinks define state recovery.
- **Storage:** checksums, replication, durable shuffle, object visibility, and retention decide reuse.
- **Platform engineering:** quotas, priority, exclusion, autoscaling, incident response, and SLOs contain recovery storms.
- **Security:** attempt isolation, scoped credentials, stale-worker fencing, and audit prevent replay abuse.
- **Testing:** deterministic schedulers, fault injection, reference models, and history analysis verify recovery.

## References

1. Apache Flink, [Task Failure Recovery](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/task_failure_recovery/). Version 2.3. Documents restart and failover strategies, including pipelined-region recovery.
2. Apache Flink, [Fault Tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/). Current. Explains state snapshots, replay, and end-to-end exactly-once premises.
3. Apache Flink, [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Current. Documents task-local versus durable recovery state.
4. Apache Flink, [Batch Progress Recovery](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/batch/recovery_from_job_master_failure/). Current. Describes retained intermediates and coordinator progress recovery.
5. Apache Beam, [Execution Model](https://beam.apache.org/documentation/runtime/model/). Current. Defines bundle processing, retry, co-failure, and discarded bundle output.
6. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents task failure, exclusion, scheduler, speculation, and network controls.
7. Apache Spark, [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html). Current. Describes lineage, persistence, tasks, and shuffle behavior.
8. Apache Spark, [Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html). Current. Documents scheduling, cancellation, pools, and dynamic allocation behavior.
9. Apache Hadoop, [OutputCommitter API](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/OutputCommitter.html). Current. Defines task/job commit, abort, recovery, and repeatability hooks.
10. Apache Hadoop, [MapReduce Tutorial](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html). Current. Documents attempts, speculative execution, task failure, and output commit.
11. Kubernetes, [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/). Current. Documents pod retries, backoff limits, completion tracking, and failure policies.
12. Google Cloud Dataflow, [Exactly-once in streaming](https://cloud.google.com/dataflow/docs/concepts/exactly-once). Current. Explains record deduplication, retries, and side-effect caveats.
13. Apache Iceberg, [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Current. Documents atomic commits, idempotent retry, conflict handling, and unknown outcomes.

## Exercises

### Exercise 1

A graph has pipelined tasks A–B–C, a durable shuffle from C to D, and pipelined D–E. B fails before C commits its shuffle. Which tasks form the immediate recovery region, and what changes if C's matching shuffle was already durably committed before its local copy was lost?

### Exercise 2

Design an attempt-output protocol for a task producing four files under speculation. Include naming, manifests, completeness, winner selection, late attempts, unknown commit outcome, and cleanup.

### Exercise 3

The same partition fails with identical decode exception on four different hosts. Explain classification, retry decision, host exclusion, evidence retention, and repair choices.

### Exercise 4

Specify recovery for a stateful operator whose last completed checkpoint contains state at source offset 9,000 while some records through 9,500 reached an external HTTP API.

### Exercise 5

Design a fault-injection experiment and dashboard that proves region recovery saves work without duplicating output under worker loss and lost acknowledgements.

## Answers to the Exercises

### Answer 1

Before shuffle commit, A, B, and C co-fail because no durable boundary separates their in-flight region; D and E have no valid input to preserve. If the exact C output was already durably committed with complete partition inventory and checksums, losing B/C local state does not require recomputation for consumers: D can read the durable shuffle. Recompute only if the logical job still requires missing producer completion state or the durable artifact fails identity/integrity/retention checks.

### Answer 2

Name files by job, epoch, logical task, attempt, and file ordinal. Each attempt writes private objects and a manifest covering exactly four files with lengths/checksums and input/code digest. A conditional coordinator record selects one complete compatible manifest for the logical task; final job publication references only winners. Output storage rejects stale epochs, late attempts become superseded, and a lost response is resolved by logical transaction ID before another selection. Cleanup reads winner/unknown inventories, waits through retention, and idempotently deletes only unreachable loser objects.

### Answer 3

Cross-host reproduction with the same partition, code/config digest, and exception strongly indicates deterministic poison data or decoder logic, not four bad hosts. Stop identical retries when the bounded policy reaches its confidence/budget threshold; do not exclude those hosts. Retain protected input identity/offset, schema, bytes or minimal reproducer, code digest, exception chain, and attempt placements. Repair data/schema/decoder, quarantine only under explicit semantics, or fail the job; then start a new compatible run rather than disguising changed semantics as retry.

### Answer 4

Restore managed state and source position together from checkpoint 9,000 and replay later records. The API calls through 9,500 may repeat because they lie after the checkpoint. Safe recovery requires stable per-effect idempotency keys that the API remembers, or a transactional outbox/sink whose commit coordinates with checkpoint completion. Without either, exactly-once external effects cannot be claimed; reconcile API results by recorded identity before reopening and document possible duplicates or compensation.

### Answer 5

Run a failure-free reference, then inject worker death before output-ready, after output-ready, during winner CAS, and after durable commit before acknowledgement. Include concurrent speculation and block loss on each side of a durable boundary. Compare final files/records and external effect identities exactly; assert one winner per logical task and no stale-epoch publication. Measure recovery-region tasks, replayed/preserved bytes and time, attempts, commit conflicts/unknown resolution, cleanup, and end-to-end recovery latency by stage/host/cache. Region recovery is proven useful only when results match and preserved work exceeds the reference restart baseline under matched load.
