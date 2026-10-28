---
module_id: LSDS-090
program: Large-Scale Data Systems Engineering
level: 2
module_number: 90
title: Designing Recovery for Multi-Hour and Multi-Day Jobs
status: complete
last_verified: 2026-09-04
---

# Designing Recovery for Multi-Hour and Multi-Day Jobs

## One-Page Review

### Governing question

How should a data job that runs for hours or days preserve enough verified progress to survive task, worker, coordinator, storage, capacity, deployment, and region failures without restarting blindly, duplicating output, or discovering during an incident that its recovery point cannot be used?

### Essential definitions

- A **recovery unit** is the smallest independently retryable work item with stable input/output identity.
- A **durable boundary** is a validated materialization or checkpoint from which downstream work can resume.
- A **recovery graph** records dependencies among inputs, stage outputs, checkpoints, commit decisions, and remaining work.
- **recovery point objective (RPO)** bounds acceptable lost completed work or input progress under a named failure.
- **recovery time objective (RTO)** bounds time to restored useful service or job completion under that failure.
- **restart amplification** is total repeated work divided by work invalidated by the failure.
- A **checkpoint interval** is useful-work distance between recovery snapshots; checkpoint duration is its write/coordination cost.
- A **resume token** durably identifies source range, state/version, output ownership, and the next safe action.
- A **salvageable output** is attempt output that can be validated and adopted without violating provenance or atomicity.
- A **recovery drill** executes restore/replay/commit against retained artifacts and measures the actual objective.
- A **failure budget** limits repeated attempts, elapsed time, and resource/effect exposure before escalation.

### Central model, mechanism, or theorem

Represent job recovery state as directed acyclic graph

$$G_R=(V,E,A,C,D),$$

where $V$ are logical work/stage nodes, $E$ dependencies, $A$ immutable inputs and candidate artifacts, $C$ completed validated boundaries/checkpoints, and $D$ code/schema/config/environment digests. For failure $f$, select newest compatible boundary cut $K\subseteq C$ whose transitive artifacts are complete, durable in the required failure domain, readable, unexpired, and semantically consistent. Recovery closure $R_f(K)$ contains only unfinished or invalid descendants required for the target.

Choose $K$ by correctness first, then minimize predicted

$$T_{recover}(K)=T_{elect}+T_{capacity}+T_{validate}+T_{restore}(K)+T_{recompute}(R_f(K))+T_{commit}+T_{verify}.$$

For periodic checkpoint cost $d$, useful-work interval $c$, and independent failure rate $\lambda$, a simple steady-state approximation is overhead $d/c+\lambda c/2$, minimized near $c^*=\sqrt{2d/\lambda}$ under restrictive assumptions. Real design must include correlated failures, checkpoint overlap, restore bandwidth, artifact retention, tail latency, and hard RPO/RTO constraints.

### Critical invariants

- Every recovery unit has stable logical identity; attempts write private or conditional output.
- A boundary becomes selectable only after complete durability, integrity, dependency, and semantic validation.
- Recovery uses inputs, state, output handles, code, schema, configuration, and environment from one compatible lineage.
- Source progress never advances beyond committed state/output; output commit is idempotent or transactional.
- Coordinator state and ownership epochs survive failover and fence obsolete attempts.
- Intermediate artifacts state their failure domain, retention, checksum, producer version, and consumer dependencies.
- Checkpoint/materialization cadence is derived from objective and measured cost, not a round number.
- Retry policy distinguishes transient, deterministic, data-specific, capacity, dependency, and corruption failures.
- Recovery capacity, credentials, keys, network paths, and source retention exist for the full recovery horizon.
- Restore is practiced from older/fallback points and measured end to end, not inferred from checkpoint success.

### Common failures

Common failures include one monolithic task; checkpointing only the driver; trusting local disks as durable; recording “stage done” before output validation; overwriting final output from attempts; losing the exact code/schema/config bundle; retaining checkpoints but expiring source logs, encryption keys, or incremental bases; choosing the newest directory instead of newest valid cut; retrying deterministic bad data indefinitely; aggressive speculation of side-effecting tasks; making retry count the only budget while attempts last hours; restoring state without sink decisions; optimizing checkpoint duration while restore/replay tails exceed RTO; and never testing coordinator/region recovery.

### Compact example

A 16-hour job has a 4-hour extract materialized durably, a 10-hour join checkpointed after 6 hours, and a 2-hour publish. Failure near the join's end invalidates post-checkpoint work. Restoring the join checkpoint costs 0.5 hour, then 4 join hours and 2 publish hours remain: recovery is 6.5 hours instead of 16, saving 9.5. The 4 hours since the checkpoint is work RPO. An 8-hour RTO is met only if capacity, validation, sink reconciliation, and artifact reads fit the included assumptions.

### Connections

[LSDS-057](057-memory-cpu-and-i-o-isolation.md) supplies capacity isolation, [LSDS-081](081-task-level-failure-recovery.md) supplies retry units, [LSDS-083](083-coordinator-failure.md) supplies durable control state, [LSDS-084](084-lineage-based-recompute.md) supplies recovery closure, [LSDS-085](085-checkpoint-based-recovery.md) supplies consistent snapshots, and [LSDS-087](087-transactional-sinks.md) supplies output commit.

## Governing Question

For a five-minute job, full restart may be the simplest correct recovery strategy. For a two-day job, the same choice can burn scarce compute repeatedly, miss a deadline, outlive source retention, and amplify every intermittent failure. Long duration changes recovery from a retry setting into an architecture.

The job may contain very different phases: scanning immutable input, a costly shuffle, iterative optimization, stateful enrichment, and a transactional publish. Some work is cheap to recompute; some intermediate output is expensive but reusable; some state changes continuously; some effects cannot be repeated. One checkpoint mechanism rarely fits all stages.

The governing question is how to partition work, establish durable boundaries, persist coordinator and semantic identity, select a valid recovery cut, allocate recovery capacity, handle retryable versus terminal failures, commit outputs safely, and prove the entire recovery path within objectives.

## Why This Matters

The probability of encountering at least one failure rises with duration, parallelism, and dependency count. Even reliable components collectively expose worker loss, preemption, spot interruption, network/storage throttling, coordinator restart, credential rotation, source expiry, and software deployment during one run.

Recovery cost has several tails. Waiting for replacement capacity may dominate state loading. Restoring millions of tiny files may dominate bytes. A checkpoint can be complete but incompatible with current code. A replay can be fast but blocked by an expired source offset. A sink commit can remain ambiguous. RTO must include all stages from detection through verified progress.

Over-checkpointing also harms the job. Snapshot I/O competes with useful work; durable stage materialization adds storage and catalog operations; excessive fine-grained tasks overload schedulers. The durable design balances expected wasted work, checkpoint cost, failure correlation, deadline, storage, and operational complexity while never weakening correctness.

## Prerequisites and Retrieval

Review resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), task recovery in [LSDS-081](081-task-level-failure-recovery.md), coordinator recovery in [LSDS-083](083-coordinator-failure.md), lineage recompute in [LSDS-084](084-lineage-based-recompute.md), checkpoint recovery in [LSDS-085](085-checkpoint-based-recovery.md), exactly-once state in [LSDS-086](086-exactly-once-state-updates.md), and transactional sinks in [LSDS-087](087-transactional-sinks.md).

You should understand DAGs, stages/tasks/attempts, checkpoints, immutable materializations, lineage, transactions, leases/fencing, source offsets, checksums, failure domains, retries/backoff, stragglers/speculation, capacity scheduling, RPO/RTO, hazard rates, percentiles, and garbage collection.

For diagnosis retain job/run/graph/semantic digest, stage/unit/attempt IDs, input snapshots/ranges, boundary/checkpoint ID and dependency graph, output handles/checksums/counts, coordinator epoch/decision log, failure class/time/domain, retries/backoff, capacity request/wait, restore/recompute/commit/verify stages, source/key/credential retention, selected/fallback rejection reasons, progress rates, deadline/objectives, and cleanup/audit history.

## Learning Objectives

After this module, you should be able to:

1. decompose long jobs into stable retry and durable recovery units;
2. classify durable versus ephemeral artifacts by failure domain;
3. build a recovery graph and select a consistent validated boundary cut;
4. estimate checkpoint/materialization economics without overclaiming a simple model;
5. design coordinator recovery, fencing, resume tokens, and attempt-safe output;
6. classify failures and bound retries by attempts, time, resource, and deadline;
7. include capacity, retention, credentials, sinks, and verification in RPO/RTO;
8. handle stragglers, preemption, scale change, and regional loss safely;
9. observe progress, amplification, restore stages, and objective attainment; and
10. run fault-injection and restore drills that prove recovery artifacts usable.

## Core Exposition

### Define objectives by failure domain

List worker/process, node, rack/zone, coordinator, storage object, control plane, region, deployment, dependency, and operator-error failures. Set RPO/RTO and completion deadline for each. A local copy may meet worker RTO but not zone loss; a remote checkpoint may survive zone loss but restore slowly.

Define the target: resumed useful progress, first correct output, or full job completion. State whether the deadline resets after failure. Include maximum tolerated replay, duplicate effects, and manual intervention.

### Decompose stable recovery units

Partition by immutable input ranges or deterministic key/partition sets. Units must be neither multi-hour monoliths nor millions of scheduler-heavy fragments. Their output identity includes input snapshot/range, transformation digest, schema, partitioner, and logical unit—not attempt ID.

Record dependency edges and wide-boundary mappings. Iterations use explicit epoch/superstep. Dynamic/adaptive plans persist the executed mapping needed to recover exact logical output ownership.

### Choose durable stage boundaries

Materialize after expensive fan-in/shuffle, nonreplayable input, long iteration, external rate-limited read, or before a fragile publish when saved expected work justifies cost. Output is immutable/private until its manifest is complete and validated.

Do not materialize every edge reflexively. Durable boundaries add I/O, storage, catalog load, retention, and compatibility obligations. Recompute cheap deterministic narrow stages from an upstream boundary.

### Checkpoint within long stateful stages

If a single stage itself runs hours, periodically checkpoint iteration/state and source/work frontier. Capture timers, RNG/optimizer state, convergence counters, partition ownership, and external transaction handles that affect continuation.

Use incremental snapshots when dependency management and restore performance are verified. Local secondary copies accelerate node-stable recovery; durable primary copies remain authoritative for broader failures.

### Publish boundaries atomically

A boundary manifest lists all winning unit outputs, sizes, counts, checksums, schema/version, and lineage. Publish only after expected coverage and validation succeed. Partial attempt files remain unreachable.

Retries return identical handles or conflict. Speculative attempts compete under one winner rule. Readers and downstream stages consume only the committed manifest, making boundary adoption idempotent.

### Persist coordinator state and resume tokens

The coordinator records graph/semantic digest, unit states, attempts, leases/epochs, boundary handles, sink decisions, retry budget, and next safe actions in durable linearizable or replayable state. Workers cannot declare global completion.

Resume token must be self-validating and sufficient to reconstruct ownership. On failover, new coordinator increments epoch, fences old commands, reconciles workers/storage/sinks, and resumes rather than creating a second job identity.

### Classify failures before retry

Transient transport/throttling failures use bounded exponential backoff and jitter. Worker loss retries elsewhere. Capacity failure may pause and request a different pool. Deterministic code, schema, authorization, missing input, invariant, and corrupt-artifact failures should fail/quarantine rather than loop.

Data-specific poison partitions can be isolated only under declared completeness policy. Preserve evidence and never silently skip. A failure classifier can be wrong, so escalation and operator override are auditable.

### Bound retries and elapsed exposure

Define per-unit, stage, dependency, and job budgets for attempt count, cumulative elapsed time, resource cost, deadline slack, and external requests/effects. Backoff must not consume the entire completion deadline unnoticed.

Circuit breakers halt launch storms during dependency outages. Recovery-of-recovery failure may select an older boundary, but repeated fallback increases replay and must remain within retention/objectives.

### Model checkpoint economics

The $d/c+\lambda c/2$ approximation assumes independent exponential failures, uniform failure within interval, constant checkpoint cost, no overlap, and immediate capacity. Use it to reason, not to set policy blindly. Hard RPO may require shorter $c$ than economic optimum.

Measure checkpoint pause/async cost, interference, size/change rate, completion tails, restore bandwidth, replay throughput, and correlated loss. Stage boundaries may have discrete opportunities rather than periodic intervals.

### Plan capacity for recovery

Reserve or rapidly acquire enough scheduler quota, workers, memory, disk, shuffle, network, object requests, catalog/database connections, and sink capacity. Recovery often reads checkpoints and replays simultaneously, producing a different resource profile from steady execution.

Test cold-cache and region/zone placement. Locality preference can reduce time, but waiting indefinitely for lost locality violates RTO. Graceful decommission can migrate artifacts; involuntary loss cannot be assumed to cooperate.

### Align retention horizons

Retain source inputs/log offsets, root snapshots, intermediate boundaries, checkpoints and incremental bases, code/images/dependencies, schemas, models/reference data, encryption keys, credentials/access policy, transaction outcomes, and consumer-compatible output until the latest possible recovery plus margin.

The minimum horizon controls actual recoverability. A two-week checkpoint is useless if its source log expired after three days or its key was destroyed. Validate dependency closure continuously.

### Recover in a deterministic sequence

Elect/fence coordinator; stop or fence stale writers; classify failure; enumerate candidate cuts newest-first; validate integrity/compatibility/dependencies/access/source/sink state; allocate resources; restore; replay/recompute closure; resolve output commits; verify; then declare progress.

If a candidate fails, record reason and try an older policy-permitted cut. Never mix components from different cuts to appear newer. Unknown sink outcomes resolve before replay.

### Handle stragglers and preemption

Detect slow progress using input-normalized rates and comparable cohorts, not duration alone. Speculation is safe only for attempt-private/idempotent work; one logical winner commits. Split skewed units when stable subrange identities preserve coverage.

On planned preemption, stop admission, checkpoint/finish bounded work, persist handles, and relinquish leases. Replacement may overlap with terminating work, so destination-enforced fencing remains required.

### Verify completion and rehearse restore

Completion means all required units/boundaries/output commits and quality invariants validate—not merely all processes exited zero. Reconcile source ranges to output identities/counts/digests and classify every attempt artifact.

Regularly restore newest and older checkpoints in isolated environments with production-shaped state and cold storage. Delete/corrupt latest artifacts to prove fallback; revoke a key or exhaust capacity to test detection. Measure detection through verified progress and completion.

### Observe recovery effectiveness

Measure useful-work progress/rate, checkpoint/materialization cost and age, valid boundary coverage, attempts/failures by class, retry/backoff time, lost/repeated work, restart amplification, recovery closure, capacity wait, restore/replay/commit/verify latency, deadline slack, fallback, and achieved RPO/RTO.

Segment by job/stage/unit/attempt, input size/skew, code/schema version, boundary/checkpoint, failure domain/type, resource pool, storage/dependency, recovery versus steady mode, and observation window. Averages hide the incident-defining tail.

## Definitions and Notation

Let:

- $G_R=(V,E,A,C,D)$ be the recovery graph;
- $K\subseteq C$ be a valid compatible boundary cut;
- $R_f(K)$ be recompute closure after failure $f$;
- $W$ be useful work completed and $W_l$ work lost/repeated;
- $A_r=W_{repeated}/W_{invalidated}$ be restart amplification;
- $d$ be checkpoint cost and $c$ useful-work interval;
- $\lambda$ be an assumed independent failure rate;
- $T_e,T_a,T_v,T_s,T_r,T_c,T_q$ be election, capacity allocation, validation, state restore, recompute, commit, and verification times;
- $T_{recover}$ be their end-to-end sum;
- $H_i$ be retention horizon of required artifact/dependency $i$.

True recovery horizon is at most $\min_i H_i$. All time/cost models must state workload, failure distribution/domain, concurrency, percentile, and observation window. Restart amplification denominator must not be zero and must define invalidated work.

## Mechanisms, Invariants, or Proof Structure

### Recovery-cut correctness proof

Every selected boundary is complete, immutable, integrity-valid, dependency-closed, and produced under compatible $D$. Recomputing only unavailable descendants in topological order from pinned inputs/boundaries yields the declared target without mixing lineages.

### Attempt-safety proof

Attempts write private output keyed beneath one logical unit. A conditional manifest/transaction selects exactly one valid winner. Failed, stale, and speculative losers remain invisible and are later collected, so retries do not duplicate committed output.

### Coordinator-failover proof

Durable state contains decisions and resume actions. New coordinator installs higher epoch before commanding work; workers/storage/sinks reject old epochs. Replaying idempotent decisions converges to the same unit/boundary/commit state.

### Checkpoint-economics derivation

With checkpoint cost fraction $d/c$ and failures losing on average $c/2$ useful work at rate $\lambda$, expected overhead is $d/c+\lambda c/2$. Differentiating yields $-d/c^2+\lambda/2=0$ and $c^*=\sqrt{2d/\lambda}$. Violated assumptions require simulation/measurement, and hard objectives constrain the feasible interval.

### Adversarial verification

Test first/last/empty/huge units, worker/coordinator/storage/zone failure, corrupted/latest/missing incremental boundary, source/key/code expiry, capacity starvation, dependency outage, poison data, long straggler, speculative overlap, preemption, lost commit reply, sink unknown, cleanup race, fallback, and repeated recovery failure.

## Alternatives and Trade-Offs

| Strategy | Strength | Cost or limitation |
|---|---|---|
| Full job restart | Simplest state model | Catastrophic wasted work for long duration |
| Task retry from inputs | Fine-grained transient recovery | Wide dependencies and lost intermediates amplify work |
| Durable stage materialization | Cuts expensive upstream recompute | Storage, validation, catalog, and retention cost |
| Periodic state checkpoint | Bounded loss inside long stateful work | Snapshot overhead and restore dependency graph |
| Local recovery copy | Fast same-node restore | Not durable for node/zone loss |
| Replicated remote checkpoint | Broader durability | Network/storage and cold-restore time |
| Salvage attempt output | Saves expensive completed bytes | Complex integrity/ownership validation |
| Redundant/speculative execution | Reduces tail for safe work | Extra cost and duplicate-effect risk |

Combine mechanisms by stage and failure domain. The simplest mechanism meeting measured objectives is preferable to an elaborate untested recovery stack.

## Failure Modes and Misconceptions

1. **One giant task.** Any failure repeats hours of work.
2. **Driver-only checkpoint.** Worker state/output cannot be reconstructed consistently.
3. **Local equals durable.** Node or zone failure removes the only copy.
4. **File exists equals boundary.** Partial/corrupt output becomes selectable.
5. **Attempt writes final path.** Retries/speculation overwrite or duplicate.
6. **Newest checkpoint wins.** Compatibility/dependencies/source/sink state are unchecked.
7. **Retry everything.** Deterministic/data/auth/corruption failures burn the deadline.
8. **Count budget only.** One or two attempts can consume days and huge cost.
9. **Independent retention.** Shortest dependency horizon breaks the recovery chain.
10. **Checkpoint success equals RTO.** Capacity/restore/replay/commit/verify tails are omitted.
11. **Average recovery.** Rare correlated cold recovery defines real outages.
12. **Unsafe speculation.** Side effects or shared final files execute twice.
13. **Capacity on demand assumed.** Recovery queues behind healthy workloads.
14. **Mixed recovery roots.** New progress combines with old state/output.
15. **No drill.** Artifacts, credentials, tooling, and runbooks decay unnoticed.

## Worked Examples

### Example 1

A 30-hour monolith with one retry can consume nearly 60 hours; six 5-hour durable units cap ordinary retry loss near one unit plus overhead.

### Example 2

A 4-hour extract is validated and manifested, so a later join failure does not reread a rate-limited source.

### Example 3

An iterative model checkpoints weights, optimizer moments, epoch, shard frontier, and RNG state; weights alone cannot reproduce continuation.

### Example 4

A local checkpoint restores a process crash quickly but disappears with the node; remote primary is selected for node loss.

### Example 5

A deterministic schema error fails immediately into quarantine instead of consuming the four-attempt transient budget.

### Example 6

Checkpoint files remain for 14 days, but source retention is 3 days; actual complete replay horizon is at most 3 days.

### Example 7

Speculative tasks produce identical digest handles; a conditional manifest selects one. Different digests trigger investigation.

### Example 8

Recovery spends 20 minutes electing/validating, 90 waiting for capacity, 30 restoring, 180 recomputing, 20 committing, and 10 verifying: RTO is 350 minutes, not 30.

### Example 9

Corrupting the newest checkpoint makes selection fall back one generation and visibly increases replay distance rather than mixing files.

### Example 10

The executable fixture compares full restart with recovery from a validated mid-stage checkpoint.

<!-- bijux-verify: {"id":"long-job-recovery","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"total_runtime_hours=16.0\nselected=join-checkpoint-6h\nwork_rpo_hours=4.0\nrecovery_hours=6.5\nsaved_hours=9.5\nrto_target_hours=8.0\nrto_met=true\n","stderr":""}} -->
```python
extract_hours = 4.0
join_hours = 10.0
publish_hours = 2.0
checkpointed_join_hours = 6.0
restore_hours = 0.5
rto_target_hours = 8.0

total_runtime = extract_hours + join_hours + publish_hours
work_rpo = join_hours - checkpointed_join_hours
recovery = restore_hours + work_rpo + publish_hours
print(f"total_runtime_hours={total_runtime:.1f}")
print("selected=join-checkpoint-6h")
print(f"work_rpo_hours={work_rpo:.1f}")
print(f"recovery_hours={recovery:.1f}")
print(f"saved_hours={total_runtime - recovery:.1f}")
print(f"rto_target_hours={rto_target_hours:.1f}")
print(f"rto_met={str(recovery <= rto_target_hours).lower()}")
```

## Cross-Program Connections

- **Distributed systems:** failure domains, consensus state, fencing, atomic commit, and idempotency define safe recovery.
- **Data structures:** DAG closure, manifests, versioned maps, logs, and Merkle/checksum trees encode progress.
- **Scheduling:** quotas, locality, preemption, decommission, speculation, and capacity wait shape RTO.
- **Storage:** durable snapshots, replication, incremental dependencies, bandwidth, and retention shape feasibility.
- **Streaming:** source frontiers, state/timers, checkpoints, replay, and sinks define consistent continuation.
- **Reliability engineering:** RPO/RTO, hazard assumptions, tail latency, failure budgets, drills, and runbooks prove readiness.
- **Security:** credentials, encryption-key lifetime, scoped recovery access, and audit are recovery dependencies.
- **Economics:** expected lost work, checkpoint overhead, compute price, deadline penalties, and storage inform cadence.

## References

1. Apache Flink, [Checkpointing](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/checkpointing/). Current. Documents durable source/state prerequisites and checkpoint controls.
2. Apache Flink, [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Current. Covers local/remote recovery and large-state trade-offs.
3. Apache Flink, [Configuration](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/). Current. Documents recovery, restart, retained checkpoint, and high-availability controls.
4. Apache Flink, [Savepoints](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/). Current. Documents durable state images, ownership, and restoration.
5. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents task/stage failures, speculation, decommission, scheduling, and resource controls.
6. Apache Spark, [Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html). Current. Covers allocation, decommission, and concurrent resource scheduling.
7. Apache Spark, [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide). Current. Defines lineage, persistence, jobs, stages, and task execution.
8. Kubernetes, [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/). Current. Documents duplicate starts, concurrency, backoff, deadlines, replacement, and cleanup.
9. Kubernetes, [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/). Current. Defines voluntary/involuntary disruptions and availability controls.
10. Google Cloud Dataflow, [Design Pipeline Workflows](https://cloud.google.com/dataflow/docs/guides/pipeline-workflows). Current. Covers job lifecycle, snapshots, reliability, and regional recovery.
11. Apache Airflow, [DAG Runs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html). Current. Defines data intervals, run state, historical execution, and reruns.
12. Apache Iceberg, [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Current. Describes atomic commits, optimistic concurrency, retry, and snapshot isolation.

## Exercises

### Exercise 1

Design recovery units and durable boundaries for a 30-hour job with immutable extract, two wide joins, iterative scoring, and transactional publication.

### Exercise 2

Use the simple checkpoint-overhead model to derive a candidate interval, then list every assumption and hard constraint that can invalidate it.

### Exercise 3

Design coordinator resume state and fencing for worker overlap, lost acknowledgements, and ambiguous sink commits.

### Exercise 4

Create a retention matrix proving a 14-day recovery claim across inputs, boundaries, checkpoints, code, schemas, keys, credentials, and sinks.

### Exercise 5

Design a regional recovery drill with corrupted latest checkpoint, cold capacity, dependency throttling, fallback, verification, and an 8-hour RTO.

## Answers to the Exercises

### Answer 1

Partition extract and joins by stable source snapshot/range; materialize validated manifests after rate-limited extract and each expensive wide join. Checkpoint iterative weights, optimizer/RNG/epoch/shard frontier periodically. Attempts stage privately and one logical unit winner commits. Coordinator persists graph digest, units, leases, boundaries, retries, and sink transactions. Publish only after all required scoring outputs validate and the transaction commits; retain prior boundary and output snapshots. Model recompute closure and objective separately for task, node, coordinator, storage, and region failures.

### Answer 2

Given checkpoint cost $d$ and independent failure rate $\lambda$, minimize $d/c+\lambda c/2$ to obtain $c^*=\sqrt{2d/\lambda}$. Then constrain by maximum work RPO and deadline. Assumptions include exponential independent failures, uniform failure location, constant nonoverlapping checkpoint cost, stable work/failure rate, immediate capacity, always-valid checkpoints, no correlated storage loss, and restore/replay cost proportional to work. Measure tail snapshot/restore bandwidth, interference, dependency limits, retention, and correlated events; simulate when assumptions fail.

### Answer 3

Persist job/graph/semantic digest, logical units and attempt handles, accepted boundary manifests, checkpoint/source frontier, retry/failure budgets, sink decision/outcome, and next safe action. New coordinator obtains durable higher epoch before issuing commands. Workers and destinations reject lower epochs. Identical lost acknowledgements reconcile by stable unit/transaction identity and digest. Unknown sink outcome is queried under original transaction ID before retry; completed decisions replay idempotently. Storage scan finds candidate orphans but cannot adopt/delete them without coordinator lineage and lease checks.

### Answer 4

For every recovery point enumerate transitive source snapshots/log positions, materialized outputs and incremental bases, coordinator metadata, exact code/image/dependencies/runtime, schemas/serializers/models/references, encryption keys, workload credentials/policy, transaction outcome records, and consumer compatibility. Record location/failure domain, owner, expiry, integrity/access probe, and required horizon. The claim is bounded by the earliest expiring required item, so every entry must exceed 14 days plus detection/recovery margin or a tested substitute must exist. Automate closure validation and restore samples before expiry.

### Answer 5

Fence the primary coordinator/writers and start a new regional control plane with pre-reserved or measured cold capacity. Corrupt the newest checkpoint intentionally; selector must reject it with evidence and choose an older complete compatible point. Throttle storage/source/sink, verify backoff and no launch storm, restore remote state, replay exact closure, resolve sink unknowns, and compare input/output identities, counts, digests, state, and effects. Time detection, election, capacity, validation, restore, recompute, commit, and verification; their sum must be at most eight hours. Preserve artifacts and produce remediation for any margin shortfall.
