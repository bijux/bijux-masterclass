---
module_id: LSDS-006
program: Large-Scale Data Systems Engineering
level: 1
module_number: 6
title: Stages, Tasks, and Dependencies
status: complete
last_verified: 2026-09-03
---

# Stages, Tasks, and Dependencies

## One-Page Review

### Governing question

How should a distributed engine divide a job into stages and partition tasks, track their attempts, and enforce dependencies so that scheduling, recovery, and completion remain correct and diagnosable?

### Essential definitions

- A **job** is one submitted computation with a declared result or continuing-service objective.
- A **stage** is a schedulable region whose tasks share an execution boundary, commonly separated by a blocking exchange, materialization, barrier, or resource transition.
- A **task** is one logical partition-level unit of work within a stage.
- An **attempt** is one execution of a task; several attempts may compete or retry to produce one logical outcome.
- A **stage dependency** states which upstream result conditions make a downstream stage ready.
- A **pipelined dependency** permits producer and consumer tasks to overlap through live channels.
- A **blocking dependency** requires declared upstream outputs to complete and become available before downstream tasks start.
- A **stage attempt** is one execution generation of a stage after fetch loss, coordinated failure, or adaptive replacement.

### Central model, mechanism, or theorem

Use identity hierarchy `H=(job, graph_version, stage, stage_attempt, task_partition, task_attempt, output_commit)`. A downstream blocking stage `s` is ready only when every required parent output partition for the selected parent stage attempt is valid and discoverable.

If stage `s` has partition universe `P_s`, it contains logical tasks `{(s,p) | p in P_s}`. Attempts `(s,p,a)` never increase required logical output count. Stage success requires exactly one accepted compatible outcome for every required `p`, not merely enough successful processes. Retry scope follows dependency and materialization boundaries.

### Critical invariants

- Job, graph, stage, stage-attempt, task, task-attempt, and output identities are distinct and durable.
- Task count derives from the stage's output/input partition contract, not worker count.
- A stage boundary records why pipelining cannot or should not continue.
- Every blocking consumer references one compatible complete upstream output set.
- At most one accepted logical output exists for each task partition and epoch.
- Failed, killed, speculative, and stale attempts cannot commit over a winner.
- Stage/job terminal states follow explicit state machines and durable evidence.
- Retry and cancellation preserve side-effect, shuffle, checkpoint, and sink semantics.

### Common failures

Frequent failures are calling every operator a stage, equating partitions with workers, counting attempts as tasks, treating “running” as “healthy,” launching downstream work from partial blocking output, retrying a whole job for one recoverable task, keeping stale shuffle output after a stage retry, hiding queued or infeasible tasks, and using aggregate stage averages that obscure the gating partition.

### Compact example

An extract stage has four logical tasks. A blocking shuffle creates a three-task join stage, followed by two aggregate tasks and one publish task. If `join[1]` fails once and then succeeds, the job still requires ten logical tasks but records eleven attempts. Publication waits for the accepted aggregate output set, not for an arbitrary count of successful attempts.

### Connections

[LSDS-005](005-distributed-task-graphs.md) supplies graph structure. [LSDS-007](../ROADMAP.md) explains narrow and wide partition dependencies, and [LSDS-009](../ROADMAP.md) develops failure assumptions. Scheduling mechanics connect to [Operating Systems](../../22-operating-systems/ROADMAP.md), [Platform Engineering](../../29-platform-engineering/ROADMAP.md), and [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

A logical graph says what depends on what, but a runtime must decide the size and lifecycle of executable units. A relational join is not one cluster task. It can become hundreds of partition tasks, separated from producers by an exchange. Adjacent filters may run in the same task pipeline. A failure can retry one attempt, one task, one stage generation, a coordinated region, or the whole job depending on what state survived.

The words job, stage, task, and attempt vary across products. Durable reasoning cannot depend on labels alone. Define each identity and its accepted outcome, the partition universe it covers, what makes it ready, how it transitions, and what failure invalidates it. Then map product-specific terms onto that model.

The governing question is how to choose boundaries that expose enough parallelism and recovery isolation without paying excessive scheduling, materialization, coordination, and metadata cost. Correctness requires compatible upstream results and one committed logical outcome per required partition. Performance requires seeing queueing, skew, transfer, and retry at the right level.

## Why This Matters

Stages determine where a runtime can pipeline and where it must synchronize. Fusing source, filter, and projection into one task avoids intermediate serialization. A repartitioning exchange creates producer outputs that many downstream tasks fetch, often forming a blocking stage boundary. The boundary changes latency, storage, recovery, and observability.

Tasks determine parallelism granularity. A stage with 10,000 partitions can expose 10,000 tasks over time, even on 100 workers. Workers are execution capacity; tasks are required logical units. Too few tasks cap parallelism and magnify skew. Too many increase launch, scheduling, serialization, metadata, connection, and tiny-output overhead.

Attempts determine failure correctness. A failed process may be retried; a slow task may be speculated. Two attempts can run for one task, but only one compatible output may become authoritative. Without attempt-qualified temporary output and an atomic or idempotent commit, retries duplicate records or corrupt shared paths.

Dependencies determine readiness. A narrow pipelined child may begin as its corresponding parent produces records. A blocking shuffle consumer may require every necessary map-output partition to be available. A barrier stage may require simultaneous resources or coordinated progress. Treating all arrows identically either destroys useful overlap or exposes incomplete data.

State machines determine operations. Submitted, queued, deploying, running, failing, restarting, cancelling, succeeded, failed, and cancelled have different meanings. A coordinator failover can make a locally suspended job recoverable elsewhere. “Not running here” is not necessarily globally terminal. Cleanup must follow the authoritative lifecycle.

Observability at only job level is too coarse. Operators need stage attempts, task distributions, failed/killed attempts, queue reasons, locality, input/shuffle/output bytes, spills, and tails. Spark's current monitoring API explicitly distinguishes jobs, stages, stage attempts, and task status. Flink's execution model distinguishes job vertices, parallel execution vertices, and executions.

## Prerequisites and Retrieval

Recall from [LSDS-005](005-distributed-task-graphs.md) the logical/physical graph distinction, blocking versus pipelined edges, work/span, lineage, and task-versus-attempt identity. Recall from [LSDS-004](004-data-locality.md) that eligible task placement depends on exact input copies, resources, topology, and queues.

You should understand partitions, joins, aggregation, finite state machines, retries, idempotency, materialization, and failure domains. Retrieve the invariant that primary logical partition count does not grow when replicas or attempts are added.

## Learning Objectives

After completing this module, you should be able to:

- map application, job, operator, stage, task, attempt, and output identities;
- explain why pipelines, shuffles, barriers, and materialization create stage boundaries;
- derive task sets from partition contracts rather than machines;
- distinguish dependency readiness from resource feasibility;
- compare pipelined, blocking, barrier, broadcast, and control dependencies;
- design task, stage, and job state machines with terminal-state evidence;
- scope retry at attempt, task, stage, coordinated region, or job level;
- prevent stale or speculative attempts from committing duplicate output;
- diagnose skew, queueing, fetch loss, and retry amplification;
- define batch and streaming stage completion and high-consequence review.

## Core Exposition

### Execution hierarchy

An **application** can submit one or more jobs. A **job** selects a result, action, query, materialization, or continuing computation. A logical plan is optimized and lowered into physical operators. The runtime groups or connects those operators into execution regions, commonly called stages or pipelines, then expands each region by partition into tasks.

A task is identified by job/graph version, stage, and logical partition. An attempt adds an execution number or unique token. A worker slot is merely a resource lease on which an attempt runs. One worker runs many tasks sequentially; one task can run on different workers across attempts.

A stage can also have attempts. If a blocking exchange's upstream files are lost, an engine may recompute its producers as a new stage attempt. Downstream consumers must not combine incompatible partitions from two generations unless the protocol proves equivalence. Stage attempt identity therefore belongs in shuffle and fetch metadata.

Terminology differs. MapReduce exposes map and reduce tasks. Spark displays jobs, stages, stage attempts, tasks, and task attempts. Flink may pipeline successive parallel subtasks and uses job vertices, execution vertices, and executions. Tez describes a vertex as a template from which parallel tasks are created. Architecture records should state semantics, then product names.

### Forming stages

A stage is not necessarily one logical operator. Adjacent per-partition operations can be fused or chained into the same task pipeline when they share partitioning, resource compatibility, and execution lifecycle. A source, parse, filter, and projection may run together without materializing each edge.

A blocking exchange commonly ends a stage. Producers partition and materialize outputs; consumers in the next stage fetch the partitions they need. All-to-all shuffle, global sort boundaries, or repartitioned aggregation are common causes. Module 007 develops dependency width; later shuffle modules develop transport.

Other boundaries include durable checkpoints, side-effect commits, incompatible resource types, required barriers, isolation policy, adaptive decision points, and APIs that force materialization. A GPU inference operator may require a resource transition even if its input dependency is otherwise narrow. A validation gate before publication is a control boundary.

Boundary placement is a trade. Longer pipelines reduce launch and I/O but enlarge retry units, memory pressure, and coupled backpressure. More stages expose cut points and independent resource profiles but add coordination and intermediate data. Record why each boundary exists.

### Deriving tasks from partitions

For stage `s` with logical partition set `P_s`, create one required task outcome per `p in P_s` unless the stage contract explicitly groups or splits partitions. Parallelism is `|P_s|`, not the number of workers currently available.

Input partitions and output partitions can differ. A source stage may have one task per file split. A shuffle consumer has one task per target shuffle partition. A coalescing stage can reduce output partitions without a full redistribution when dependency structure permits; repartitioning can increase or change them through an exchange.

The task must know exact input partitions and output identity. “Process any available data” is an allocation strategy, not a durable logical identity, unless work claiming has exactly-once or reconciliation semantics. Stable task IDs allow deduplicated attempts, metrics, lineage, and commit.

Partition sizes are rarely equal. Task count indicates maximum logical concurrency, while bytes, records, CPU, memory, state, and external latency determine durations. Splitting large partitions and coalescing tiny ones can help, but changes lineage, output layout, and downstream compatibility.

### Dependency categories

A **pipelined dependency** permits overlapping execution. Channels need establishment, buffer, backpressure, end-of-input, retry, and cancellation rules. In streaming, connected operators can remain running together indefinitely.

A **blocking dependency** requires an upstream result set to be committed or otherwise complete before consumers start. It simplifies replay and prevents partial-set interpretation while adding latency and storage. Readiness must check exact required partitions and compatible attempt generations.

A **barrier dependency** requires a cohort to acquire resources or reach a synchronization point. Gang scheduling may be needed so no participant holds resources while waiting forever for absent peers. Failure policy can restart the cohort rather than one member.

A **broadcast dependency** makes one upstream outcome available to many tasks. It can begin after the broadcast artifact is complete and validated, or use a streaming distribution protocol. Memory expansion and duplicate transfer matter.

A **control dependency** gates work on validation, approval, metadata, or another event. A **resource constraint** governs where a ready task may run; it should not be confused with predecessor readiness. A task can be dependency-ready and resource-infeasible.

### Scheduler layers

A graph or DAG scheduler determines which stages are structurally ready and translates failure into recomputation requirements. A task scheduler chooses ready tasks for available resources using locality, fairness, priority, exclusion, and capacity. A resource manager provisions or leases workers. Products may combine these roles, but diagnosis benefits from the distinction.

Admission occurs before or alongside scheduling. A job whose peak memory, shuffle, or output cannot fit safely should not flood queues. Stage-level resource profiles can request different CPUs, memory, accelerators, or isolation, subject to platform support.

Ready does not mean runnable. A stage may be ready while every task waits for GPUs. A task may be runnable but delayed for locality or fair share. A deployed attempt may wait on container startup or input. Metrics should assign each interval to a state and reason.

Priority and fairness apply across jobs and within a job. Always serving the largest ready stage can starve small jobs. Always serving tiny tasks can delay a critical stage. Scheduling objectives should name throughput, deadline, fairness, cost, or tail goals and retain evidence of trade-offs.

### Task attempt lifecycle

A robust attempt lifecycle includes created, eligible/queued, assigned, deploying, running, candidate-output, committed/succeeded, failed, killed/cancelled, and superseded states as appropriate. Transitions have stable event IDs and causal reasons. Terminal does not mean successful.

Before running, verify code, configuration, credentials, resource lease, input versions, and stage attempt. During running, report progress and heartbeats without treating absence as immediate proof of death. On output, write attempt-qualified candidates. Commit accepts one logical task outcome and fences stale attempts.

A killed attempt can continue briefly because cancellation is not instantaneous. It must remain unable to commit after another attempt wins or the stage is superseded. Cleanup tolerates late messages and repeated requests.

Task success is not just process exit zero. Required outputs must be complete, durable for their consumer horizon, checksummed or otherwise validated, and registered under the correct identity. For side-effecting tasks, the external commit or idempotency receipt is part of the outcome.

### Stage and job lifecycle

A stage can be waiting on dependencies, ready, active, completing, succeeded, retrying, failed, cancelled, or superseded. It succeeds when every required task partition has one accepted compatible outcome and any stage-level commit completes.

A stage retry must decide which outputs survive. Deterministic successful tasks may be reused if their inputs and generation remain compatible; lost shuffle files may require only selected producers; barrier or stateful regions may require coordinated restart. Reusing stale outputs merely because files exist violates the attempt contract.

A job lifecycle commonly distinguishes created/submitted, admitted, running, failing, restarting, cancelling, succeeded, failed, and cancelled. Coordinator loss can create a suspended or recovering state. Globally terminal status requires authoritative agreement that no other coordinator will resume it and cleanup is safe.

Streaming jobs normally remain running. Their health is expressed through input progress, processing lag, backpressure, checkpoints, restart count, and sink commits. A running state with rising lag is not healthy. A stopped process can be recoverable from durable state rather than globally failed.

### Retry scope and failure propagation

Retry the narrowest unit that preserves correctness and makes progress. A transient worker loss can retry one pure task. Lost blocking output can re-run its producer tasks. A corrupted stage-wide broadcast may invalidate every consumer. A failed barrier participant can require cohort restart. Coordinator or incompatible state may require job recovery.

Narrow retry is not always cheapest. Recomputing many scattered producers can create more overhead than restarting a compact stage. Retry policy should consider surviving materialization, lineage, state, transfer, contention, failure cause, and deadline.

Classify failures. User-code or deterministic data errors often repeat and should fail fast with a precise record/path rather than exhaust retry limits. Transient infrastructure errors can retry with backoff and placement exclusion. Resource exhaustion may need more memory, split partitions, or reduced concurrency. Fetch failure may indicate one missing file or a dead producer executor.

Retry budgets operate at several levels: task consecutive failures, stage attempts, executor exclusion, and job restarts. Reset rules and failure equivalence matter. Infinite retry hides terminal incompatibility and consumes capacity; a tiny budget harms availability during transient loss.

### Output commit and side effects

Attempt output should be isolated by attempt identity. A coordinator or transactional protocol elects one winner only after validation, then publishes the logical task output. Losers are cleaned asynchronously without threatening the winner.

Appending directly to a shared final file is unsafe under retry or speculation. Use partition-specific replacement, atomic rename where semantics support it, manifest commit, transactional sink, idempotency keys, or deduplicating downstream protocols. Filesystem/object-store semantics must be verified rather than assumed.

Stage-level output may need an all-partitions manifest. Consumers read only a committed manifest referencing one complete compatible set. This prevents a downstream stage from mixing old and new task attempts or seeing a partial directory listing as complete.

External effects require receipts and reconciliation. A successful data task whose notification failed may need only the notification retried; replaying the computation and effect together can duplicate it. Separate pure computation from effect commit where possible.

### Skew, tails, and utilization

Stage completion follows the last required task, so skew and stragglers dominate. Compare task duration, input bytes, records, CPU, GC, memory, spill, shuffle fetch, locality, output, and external wait distributions. The maximum and high quantiles matter more than the mean alone.

Speculation can copy an anomalously slow stateless attempt to another worker. It is ineffective when every attempt reads the same hot remote service or partition, and harmful during cluster-wide contention. Diagnose root cause and isolate candidate outputs.

Stage boundaries can leave resources idle. Downstream blocking stages wait while a few upstream tasks finish. Pipelining can improve overlap but shifts pressure into buffers and coupled lifecycles. Adaptive partition splitting may reduce tails if semantics and output compatibility permit.

Worker utilization is not job efficiency. A cluster can be busy recomputing doomed attempts, spilling, fetching remote shuffle, or waiting on a serial sink. Attribute useful and recovery work separately.

### Observability and retained evidence

Persist the submitted and physical graph versions, stage boundaries and reasons, partition counts, resource profiles, dependencies, task and attempt IDs, state transitions, output commits, and retry causality. Without event history, post-completion aggregates cannot reconstruct races.

For each stage report task status counts, attempts per task, queue/deploy/run time, locality, input/shuffle/output bytes, memory, spill, CPU, external wait, and distribution quantiles. Show the slowest tasks with their partition and worker history.

For dependencies report parent stage attempt, required partition set, materialization state, fetch failures, and readiness time. For jobs report admission, critical stage chain, restarts, cancellation, terminal authority, and cleanup.

Dashboards should distinguish zero progress because no data arrived, dependency block, resource infeasibility, backpressure, repeated failure, or coordinator loss. “0 active tasks” alone cannot determine health or completion.

## Definitions and Notation

Let job `j` use graph version `g`. Stage set is `S_(j,g)`. Stage `s` has logical partition universe `P_s`; task `t=(j,g,s,p)` for `p in P_s`. Stage attempt `r` and task attempt `a` give execution identity `(j,g,s,r,p,a)`.

Accepted outcome function `A(j,g,s,r,p)` is empty before commit and contains at most one valid attempt result. Stage attempt success requires `A` defined for every required `p in P_s` plus any stage-level commit. Attempt count never changes `|P_s|`.

For blocking dependency `u->s`, readiness requires a declared compatible successful attempt `r_u` and every upstream partition needed by tasks in `s` to be available. For pipelined dependency, readiness is a protocol predicate over deployed producers, channels, and available records.

Task runtime can be decomposed as `T=Q+D+I+C+X+O`, queue `Q`, deployment `D`, input/fetch `I`, compute `C`, exchange/spill `X`, and output/commit `O`. This accounting can overlap in pipelined systems and must state measurement conventions.

Stage retry amplification can be reported as total attempt work divided by accepted logical task work, alongside failed, killed, and speculative contributions. Ratios require a nonzero denominator and the resource dimension must be named.

## Mechanisms, Invariants, or Proof Structure

A stage/task design has eight obligations.

**1. Identity hierarchy.** Define application/job, graph, stage, stage attempt, task partition, task attempt, candidate artifact, and committed output IDs.

**2. Boundary rationale.** Record pipeline fusion and every exchange, barrier, materialization, effect, resource, or isolation boundary.

**3. Partition contract.** Derive logical task count, exact inputs, output partitioning, skew policy, and compatibility across adaptive changes.

**4. Dependency readiness.** Specify pipelined, blocking, barrier, broadcast, control, and resource conditions plus missing/stale metadata behavior.

**5. State machines.** Validate allowed task, stage, and job transitions, terminal authority, durable events, cancellation, recovery, and cleanup.

**6. Retry and commit.** Classify failure, scope retry, fence stale attempts, isolate candidates, accept one output, reconcile effects, and cap attempts.

**7. Performance evidence.** Measure queue/deploy/input/compute/exchange/output, task distributions, critical tails, useful versus repeated work, and dependency idle time.

**8. Operational and human review.** Retain graphs, events, outputs, faults, restore tests, exceptions, and domain/safety approvals appropriate to consequence.

The executable fixture validates blocking stage waves and identity counts for one finite batch hierarchy.

<!-- bijux-verify: {"id":"stage-task-attempt-invariants","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stage_waves=(('extract',), ('shuffle_join',), ('aggregate',), ('publish',))\nstage_count=4 logical_tasks=10\nattempts=11 succeeded_tasks=10\nfailed_attempts=1\nretried_task_attempts=((0, 'failed'), (1, 'succeeded'))\nmax_stage_tasks=4\npublish_ready_after=('aggregate',)\n","stderr":""}} -->
```python
stages = {
    "extract": {"tasks": 4, "parents": ()},
    "shuffle_join": {"tasks": 3, "parents": ("extract",)},
    "aggregate": {"tasks": 2, "parents": ("shuffle_join",)},
    "publish": {"tasks": 1, "parents": ("aggregate",)},
}

remaining = {
    name: set(stage["parents"])
    for name, stage in stages.items()
}
waves = []
while remaining:
    ready = tuple(sorted(name for name, parents in remaining.items() if not parents))
    if not ready:
        raise ValueError("stage graph contains a cycle")
    waves.append(ready)
    for name in ready:
        del remaining[name]
    for parents in remaining.values():
        parents.difference_update(ready)

attempts = []
for stage_name in (name for wave in waves for name in wave):
    for partition in range(stages[stage_name]["tasks"]):
        task = f"{stage_name}[{partition}]"
        if task == "shuffle_join[1]":
            attempts.append((task, 0, "failed"))
        attempt = 1 if task == "shuffle_join[1]" else 0
        attempts.append((task, attempt, "succeeded"))

logical_tasks = {
    (stage_name, partition)
    for stage_name, stage in stages.items()
    for partition in range(stage["tasks"])
}
succeeded_tasks = {
    task
    for task, _attempt, status in attempts
    if status == "succeeded"
}

print(f"stage_waves={tuple(waves)}")
print(f"stage_count={len(stages)} logical_tasks={len(logical_tasks)}")
print(f"attempts={len(attempts)} succeeded_tasks={len(succeeded_tasks)}")
print(
    "failed_attempts="
    f"{sum(status == 'failed' for _task, _attempt, status in attempts)}"
)
print(
    "retried_task_attempts="
    f"{tuple((attempt, status) for task, attempt, status in attempts if task == 'shuffle_join[1]')}"
)
print(f"max_stage_tasks={max(stage['tasks'] for stage in stages.values())}")
print(f"publish_ready_after={stages['publish']['parents']}")
```

The checker establishes only finite blocking dependencies, counts, and one modeled retry. It assumes every recorded success commits exactly once, which a real system must prove. It does not model pipelining, workers, resources, time, bytes, skew, shuffle loss, stage retries, speculation, cancellation, side effects, streaming, or coordinator failure.

## Alternatives and Trade-Offs

**Long pipelines versus more stages.** Long pipelines reduce launch and materialization but couple memory, backpressure, resources, and retry. More stages add isolation and independent tuning at coordination and I/O cost.

**Fine versus coarse tasks.** Fine tasks improve balance and retry granularity. Coarse tasks reduce scheduler and serialization overhead while amplifying stragglers and failure work.

**Blocking versus pipelined dependencies.** Blocking output is replayable and lifecycle-decoupled but adds latency/storage. Pipelining overlaps work and couples failure and pressure.

**Task retry versus stage retry.** Task retry is narrow when inputs survive. Stage retry restores a compatible generation when shared or exchange state is invalid, but repeats more work.

**Reuse successful output versus clean generation.** Reuse saves work when deterministic compatibility is proven. Clean rerun simplifies generation reasoning and costs more.

**Immediate failure versus retry budget.** Fast failure protects capacity on deterministic faults. Bounded retry tolerates transient infrastructure loss. Classification and backoff matter more than a universal count.

**Speculation versus diagnosis.** Speculation can reduce isolated tails. It duplicates work and cannot solve shared bottlenecks, deterministic skew, or unavailable services.

**Attempt commit versus transactional stage manifest.** Per-task commit supports incremental progress. A stage manifest gives consumers one complete compatible set. Many systems combine them.

**Static parallelism versus adaptive resizing.** Static partitions are reproducible. Adaptive split/coalesce reacts to skew but changes task identity, dependencies, and downstream layout.

**Batch terminal states versus streaming health.** Batch jobs can succeed after all required output commits. Streaming services need progress, checkpoint, lag, and continuing availability semantics.

## Failure Modes and Misconceptions

1. **Every operator is a stage.** Compatible operators can be fused into one task pipeline.
2. **A stage is one process.** It commonly expands into many partition tasks across workers.
3. **Task count equals worker count.** Tasks are logical work; workers are reusable capacity.
4. **Attempts are extra tasks.** They compete or retry to produce the same logical outcome.
5. **Task success is exit code zero.** Output validation, registration, and commit remain.
6. **Any successful attempt may publish.** Exactly one compatible winner must commit.
7. **Killed attempts stop instantly.** Late execution/messages require fencing and idempotent cleanup.
8. **All dependencies are blocking.** Pipelining, barriers, broadcasts, control, and resources differ.
9. **Pipelined means dependency-free.** Channels, backpressure, end-of-input, and failure bind peers.
10. **Partial shuffle files make consumers ready.** Blocking consumers need their declared complete set.
11. **Mixing stage attempts is harmless.** Partitions can reflect incompatible code, input, or graph versions.
12. **A ready task can run anywhere.** Resources, policy, locality, and isolation restrict candidates.
13. **A queued task is dependency-blocked.** It may be ready but resource-infeasible or fairness-delayed.
14. **Retry every failure equally.** Code faults, bad data, OOM, fetch loss, and worker loss need different action.
15. **Infinite retry improves reliability.** It can hide permanent faults and exhaust capacity.
16. **One retry limit governs all scopes.** Task, stage, executor, and job budgets interact.
17. **Successful files always survive.** Ephemeral worker loss can invalidate registered shuffle outputs.
18. **Speculation fixes skew.** Duplicate attempts process the same oversized partition.
19. **Stage averages expose stragglers.** The maximum required task gates completion.
20. **High worker utilization means useful progress.** Retried, spilling, or blocked work can dominate.
21. **Running means healthy.** Streaming lag and failed checkpoints can rise indefinitely.
22. **Not running means terminal.** Another coordinator may recover a suspended job.
23. **Cancellation permits immediate cleanup.** Attempts and consumers may still reference artifacts.
24. **Appending to a final path is retry-safe.** Attempts can duplicate or interleave effects.
25. **A clean state machine proves domain safety.** Domain consequences require independent review.

## Worked Examples

### Example 1

**Question:** A scan, filter, and projection share four input partitions. Must they be three stages?

**Reasoning:** Not if their types, partitioning, resources, effects, and pipeline lifecycle are compatible. Four fused tasks can execute the chain.

**Conclusion:** Stage boundaries arise from execution constraints, not operator count.

### Example 2

**Question:** A three-worker cluster runs a stage with twelve partitions. How many logical tasks exist?

**Reasoning:** Twelve, unless the stage contract groups partitions. Workers execute them in waves; adding workers changes concurrency, not task identity.

**Conclusion:** Partitioning defines tasks; resources define simultaneous attempts.

### Example 3

**Question:** One task fails twice then succeeds. How many outcomes are required?

**Reasoning:** One logical outcome and three recorded attempts. The accepted success fences failed or late candidates.

**Conclusion:** Count logical tasks separately from attempts.

### Example 4

**Question:** When is a shuffle consumer ready?

**Reasoning:** Under a blocking contract, when every required upstream partition from one compatible stage attempt is committed, registered, and fetchable—not merely when producers have started.

**Conclusion:** Readiness is an exact result-set condition.

### Example 5

**Question:** Why might a fetch failure rerun a successful producer?

**Reasoning:** The producer process exited successfully, but its ephemeral shuffle file was lost with the worker. Lineage reconstructs the required output.

**Conclusion:** Process success and durable availability differ.

### Example 6

**Question:** Should an OOM task consume four identical retries?

**Reasoning:** Usually not without changed resources, partition size, concurrency, or code. Identical retries repeat a deterministic capacity failure.

**Conclusion:** Failure classification should drive remedial action.

### Example 7

**Question:** Why qualify shuffle files with stage-attempt identity?

**Reasoning:** A restarted stage may use new code, partitions, or inputs. Consumers must not assemble one result set from stale and current files.

**Conclusion:** Generation identity protects dependency compatibility.

### Example 8

**Question:** Can speculation publish two sink partitions?

**Reasoning:** Both attempts can produce isolated candidates, but only the elected winner may publish the logical partition or effect receipt.

**Conclusion:** Speculation requires attempt-aware commit.

### Example 9

**Question:** Why is a running stream with rising queue delay unhealthy?

**Reasoning:** Input arrives faster than accepted processing; lag grows despite nonterminal task states. Checkpoint and sink progress may also be failing.

**Conclusion:** Streaming health requires progress evidence beyond state labels.

### Example 10

**Question:** Can retry counters approve a national emergency-alert stage?

**Reasoning:** No. Alert eligibility, geography, language/accessibility, duplicate suppression, urgency, acknowledgement, degraded networks, privacy, and public-safety consequence require named emergency-management, communications, accessibility, safety, privacy/security, distributed-systems, operations, and independent assurance review. No external review is claimed here.

**Conclusion:** High-consequence execution needs domain assurance beyond runtime state machines.

## Cross-Program Connections

[LSDS-005](005-distributed-task-graphs.md) supplies graph identity and lineage. [LSDS-007](../ROADMAP.md) formalizes partition dependency width, while [LSDS-008](../ROADMAP.md) develops worker-boundary serialization. [LSDS-009](../ROADMAP.md) supplies cluster failure assumptions. Later stage scheduling, retry, shuffle, and checkpoint modules deepen these mechanisms.

[Operating Systems](../../22-operating-systems/ROADMAP.md) owns processes, threads, scheduling, cancellation, and resource isolation. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns cluster resource provisioning, admission, quotas, placement, and workload lifecycle.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns failure detection, leases, coordination, idempotency, delivery, and consensus. [Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline intent, orchestration, contracts, and published datasets; this module owns runtime execution units beneath them.

MapReduce establishes partition tasks and bounded retries. Dryad and Tez expose vertex, edge, and task expansion. Spark's monitoring model shows jobs, stages, stage attempts, and task distributions. Flink documents parallel subtasks, executions, pipelined slots, job states, restarts, cancellation, and task lifecycle.

## References

- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI, 2004. Primary map/reduce task, retry, backup execution, and output-commit design.
- Michael Isard et al., [*Dryad: Distributed Data-Parallel Programs from Sequential Building Blocks*](https://www.microsoft.com/en-us/research/publication/dryad-distributed-data-parallel-programs-from-sequential-building-blocks/), EuroSys, 2007. Primary vertex, channel, scheduling, and failure-reexecution design.
- Matei Zaharia et al., [*Resilient Distributed Datasets*](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf), NSDI, 2012. Primary partition lineage and recomputation design.
- Apache Tez Project, [*Vertex API*](https://tez.apache.org/releases/0.10.3/tez-api-javadocs/org/apache/tez/dag/api/Vertex.html), checked 2026-09-03. Official vertex-template, task parallelism, resource, and execution-context documentation.
- Apache Spark Project, [*Monitoring and Instrumentation*](https://spark.apache.org/docs/latest/monitoring.html), checked 2026-09-03. Official current application, job, stage, stage-attempt, and task observability.
- Apache Spark Project, [*Configuration: Scheduling*](https://spark.apache.org/docs/latest/configuration.html#scheduling), checked 2026-09-03. Official current task and stage retry controls.
- Apache Flink Project, [*Jobs and Scheduling*](https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_scheduling/), checked 2026-09-03. Official current job graph, execution graph, pipelined task, state, restart, and cancellation behavior.
- Apache Flink Project, [*Task Lifecycle*](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/internals/task_lifecycle/), checked 2026-09-03. Official current task initialization, state recovery, execution, finish, checkpoint, interruption, and cleanup lifecycle.
- Apache Flink Project, [*Flink Architecture*](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/flink-architecture/), checked 2026-09-03. Official current JobManager, TaskManager, task-slot, operator-chain, and recovery roles.
- Apache Spark Project, [*RDD Programming Guide*](https://spark.apache.org/docs/latest/rdd-programming-guide.html), checked 2026-09-03. Official current partitions, transformations, actions, persistence, and shuffle behavior.

## Exercises

### Exercise 1

A stage has 120 output partitions and runs on 15 workers with four slots each. State logical task count, maximum immediate concurrency, minimum waves under ideal equal durations, and how two failed attempts affect logical output count.

### Exercise 2

Design stage boundaries for scan, parse, filter, repartition-by-customer, aggregate, validate, and publish. Explain fusion, blocking, control, and effect boundaries.

### Exercise 3

A shuffle stage attempt produced 99 of 100 durable partitions before coordinator loss. State the evidence required to reuse them safely rather than rerun the full stage.

### Exercise 4

Diagnose a stage with median task time 20 seconds, p95 24 seconds, maximum 18 minutes, one 400-GB input partition, and three speculative attempts for that partition.

### Exercise 5

A hospital executes a stage that publishes medication-allergy alerts to clinical devices. Specify identity, dependency, retry, commit, failure-test, and named review requirements.

## Answers to the Exercises

### Answer 1

There are 120 logical tasks, independent of worker count. Sixty slots allow at most 60 simultaneous attempts if every task fits and no other constraint applies, so ideal equal-duration execution needs at least two waves. Two failed attempts add attempt records and repeated work but do not change the 120 required logical outputs. Each partition still needs exactly one accepted compatible outcome.

### Answer 2

Scan, parse, and filter can fuse when schemas, resources, error behavior, and partition identity remain compatible. Repartition-by-customer creates a blocking exchange and ends that producer stage; customer aggregates run as tasks over target partitions. Validation can be part of aggregation only if it is partition-local and retry-compatible; a global validation result creates a barrier/control boundary. Publication should use a committed complete manifest plus a separate idempotent or transactional effect boundary so retries cannot expose partial or duplicate output. Record every boundary's partition, materialization, and recovery contract.

### Answer 3

Require durable graph and stage-attempt identity; exact code, configuration, input snapshots, partitioner, and schema; one validated candidate/committed artifact for each of the 99 partition IDs; checksums or content invariants; an authoritative commit log/manifest; no stale winner conflict; and storage durability independent of the failed coordinator. Recover the stage state machine, reconcile registrations against storage, compute only the missing partition, commit one 100-partition compatible manifest, and test consumer reads. File presence alone is insufficient.

### Answer 4

The maximum, not the median, gates the stage. The 400-GB partition is deterministic skew; three speculative copies repeat the same oversized work and compete for input/network rather than changing its size. Confirm its bytes, records, CPU, spill, fetch, and key distribution, then split the partition or salt/isolate heavy keys if semantics permit, increase appropriate resources, or change the upstream partitioner. Disable or constrain unhelpful speculation, quantify retry amplification, and validate downstream partition compatibility.

### Answer 5

Give each job/graph, stage generation, patient/encounter, allergy-rule/reference version, device-target partition, task, attempt, candidate alert, and accepted alert a durable identity. Inputs require exact medication/allergy and patient versions; publication waits for clinical validation and authorized routing. Retries use alert idempotency keys, durable outbox/receipt, acknowledgement, stale-attempt fencing, and reconciliation across offline devices. Test duplicate/reordered attempts, stale clinical data, unit/code mismatch, device and network loss, regional failover, partial publication, cancellation, rollback, audit replay, and downtime workflow. Named reviewers include pharmacists, allergy/immunology and prescribing clinicians, medication-safety and clinical-informatics owners, nursing/device workflow, patient-safety/quality, privacy/governance, cybersecurity, distributed-systems/operations and disaster recovery, accessibility, and the applicable independent clinical-safety authority. Local validators and this answer do not constitute external approval.
