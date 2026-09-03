---
module_id: LSDS-055
program: Large-Scale Data Systems Engineering
level: 2
module_number: 55
title: Work Stealing and Speculation
status: complete
last_verified: 2026-09-04
---

# Work Stealing and Speculation

## One-Page Review

### Governing question

How should a large-scale data system move unstarted work toward idle capacity and duplicate already-running work near the tail without violating ownership, output, fairness, or resource-safety invariants?

### Essential definitions

- **work stealing** lets an idle worker claim ready, not-yet-running work from another worker's queue.
- A **thief** requests work; a **victim** owns the queue from which work may be transferred.
- A **ready deque** supports owner-local insertion/removal and concurrent stealing from the opposite end.
- A **steal lease** is a bounded, epoch-scoped grant assigning one logical work item to one worker.
- A **straggler** is an attempt whose predicted completion materially delays its enclosing stage/job relative to a valid comparison cohort.
- **speculation** starts another attempt of an already-running logical task and accepts at most one valid result.
- A **logical task ID** names required work; an **attempt ID** names one execution of it.
- The **commit winner** is the single attempt whose validated result becomes visible for a logical task generation.
- A **false positive** is an attempt classified as a straggler even though duplication cannot improve the objective enough to justify its cost.
- **correlated slowness** affects both original and clone through a shared input, service, link, lock, quota, or algorithmic bottleneck.

### Central model, mechanism, or theorem

Work stealing redistributes queued parallelism: owners usually push/pop locally while idle workers steal eligible items, often from randomly selected victims. The claim transition must be atomic so a work item is queued or assigned once, never simultaneously owned by two workers. Speculation instead evaluates a running primary. Let $R_p$ be its predicted remaining time, $L_c$ clone startup delay, $R_c$ predicted clone runtime, and $M$ a risk margin. A clone is a candidate only when

$$B=R_p-(L_c+R_c)>M$$

with adequate confidence, eligible capacity, and duplicate-safe effects. Launch limits, fair-share charges, placement outside the suspected slow domain, an atomic first-valid-success commit, cancellation, and fencing turn that estimate into a safe control policy. This inequality is a decision model, not a universal guarantee.

### Critical invariants

- Stealing transfers only ready, movable, dependency-satisfied work; it never clones a running attempt.
- Exactly one live owner holds each non-speculative ready assignment under a queue/lease epoch.
- A logical task and its attempts have separate stable identities, pinned input/plan/code generations, and isolated intermediate output.
- At most one attempt result commits for a logical task generation; late or stale attempts are fenced.
- Speculated effects are absent, idempotent, transactional, or emitted only by a commit-aware publisher.
- Eligibility preserves hard resource, topology, security, residency, affinity, gang, and state-ownership constraints.
- Steal probes and clones are bounded, back off under contention, and consume accounted tenant capacity.
- Detection uses comparable tasks, sufficient observations, remaining-time estimates, and confidence—not elapsed time alone.
- Scheduler recovery reconstructs assignment, attempt, winner, cancellation, and cleanup state without double publication.
- Evaluation measures completion benefit against duplicate work, congestion, fairness, cost, and failure amplification.

### Common failures

Common failures include calling any queue pull “speculation”; allowing two thieves to claim one item; stealing work whose data, state, priority, or gang cannot move; probing every worker at once; stealing tasks too small to repay transfer overhead; labeling the naturally largest partition a straggler; cloning before enough peers finish; placing both attempts on the same impaired host/path; duplicating a serial bottleneck; letting both attempts publish; trusting cancellation as a fence; leaking loser shuffle files; ignoring nondeterminism; charging only the winner; and enabling speculation during cluster overload so clones worsen the tail they were meant to reduce.

### Compact example

A primary has 280 seconds of predicted work left. An eligible clone can start and finish in $5+35=40$ seconds, and policy requires a 10-second margin. The predicted benefit is 240 seconds, so duplication is eligible if confidence, budget, placement, and effect safety pass. A different primary with 45 seconds left yields only 5 seconds of predicted benefit and must not be cloned. Neither decision says whether queued work should be stolen.

### Connections

[LSDS-027](027-task-retry-and-speculation.md) establishes attempt and commit safety, [LSDS-031](031-shuffle-architecture.md) defines intermediate-output consequences, [LSDS-039](039-skewed-keys-and-heavy-hitters.md) separates skew from machine slowness, [LSDS-049](049-backpressure-across-operators.md) explains correlated congestion, and [LSDS-051](051-cluster-resource-models.md) through [LSDS-054](054-data-local-task-placement.md) constrain capacity, fairness, and placement.

## Governing Question

Parallel dataflow schedulers face two superficially similar forms of imbalance. First, a worker may be idle while another worker has many ready tasks queued. Moving an unstarted task can improve utilization. Second, most tasks in a stage may finish while one running attempt remains slow. Starting another attempt can reduce the stage tail. The first mechanism is work stealing; the second is speculation.

Conflating them damages reasoning. A stolen item changes queue ownership but should still have one execution. A speculative clone intentionally creates concurrent executions but must still yield one logical result. Stealing is primarily a load-distribution mechanism; speculation is a tail-risk hedge. They use different evidence, identities, synchronization, accounting, and cleanup.

The governing question is therefore not merely when to “run work elsewhere.” It is how to expose movable parallelism, select victims without central contention, preserve exactly-one assignment where intended, identify a consequential straggler rather than a merely slow task, decide whether a clone can finish sooner, place it in an independent domain, bound resource amplification, and make duplicate completion safe.

## Why This Matters

Large-scale jobs complete when their dependency-critical tasks complete. Average worker utilization can look healthy while a few queues remain imbalanced or a few attempts stretch the tail. Work stealing can convert otherwise idle capacity into progress without requiring a globally synchronized queue. Speculation can hedge transient host, disk, runtime, or network anomalies after ordinary scheduling has already placed work.

Both mechanisms spend control-plane and data-plane resources. Steal probes consume messages and contend on queues. Migration loses cache locality and may transfer task state or input. Speculative attempts repeat reads, decompression, CPU, shuffle writes, and service calls. Under saturation, the extra load can prolong every attempt. A scheduler must compare marginal benefit with marginal cost, not celebrate a rising steal or clone count.

Correctness is more important than speed. Duplicate owners can process one partition twice. Two successful attempts can race to publish different files or external effects. A cancelled loser may continue after a partition generation has advanced. Stable logical identity, distinct attempt identity, atomic claims/commits, fenced generations, and effect discipline are foundational—not cleanup details.

These choices also allocate shared capacity. A tenant whose clones are free in fair-share accounting can exceed its entitlement. Aggressive thieves can bypass priorities or drain work from data-local queues. A low-latency workload can improve its own tail while pushing duplicate cost onto batch tenants. Policy therefore needs per-job and cluster limits, eligibility rules, admission under headroom, explicit charging, and cross-tenant outcome metrics.

Finally, mitigation must not hide root causes. Persistent stragglers may reveal skewed partitions, failing disks, GC pressure, degraded networks, bad code, rate limits, or insufficient granularity. Stealing and speculation buy time while operators repair those causes; they are not substitutes for diagnosis.

## Prerequisites and Retrieval

Review distributed task graphs, stages, dependencies, and scheduling in [LSDS-005](005-distributed-task-graphs.md), [LSDS-006](006-stages-tasks-and-dependencies.md), and [LSDS-026](026-stage-scheduling.md). Revisit attempt identity and commit semantics in [LSDS-027](027-task-retry-and-speculation.md), shuffle lifecycle in [LSDS-031](031-shuffle-architecture.md), skew in [LSDS-039](039-skewed-keys-and-heavy-hitters.md), effect replay in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), and resource/fairness/locality in [LSDS-051](051-cluster-resource-models.md) through [LSDS-054](054-data-local-task-placement.md).

You should understand DAG readiness, partitions, worker queues, atomic compare-and-set or transactional claims, leases and epochs, task attempts, percentiles, progress metrics, critical paths, idempotency, shuffle commit, resource vectors, topology, and fair-share scheduling.

## Learning Objectives

After this module, you should be able to:

1. distinguish work stealing, work sharing, retry, hedging, and speculative task execution;
2. design per-worker ready queues with atomic ownership transfer and recovery-safe identities;
3. choose victim selection, steal batch size, backoff, and task granularity under contention;
4. preserve dependencies, affinity, priority, fairness, locality, gang, and state constraints during steals;
5. identify consequential stragglers using comparable cohorts and predicted remaining time;
6. evaluate clone benefit using startup, runtime, confidence, headroom, cost, and deadline;
7. isolate speculative attempts and implement atomic first-valid-success publication with fencing;
8. handle shuffle, external effects, nondeterminism, cancellation, and loser cleanup safely;
9. diagnose skew and correlated bottlenecks that duplication cannot cure; and
10. validate stealing and speculation using correctness, latency, utilization, amplification, fairness, and cost evidence.

## Core Exposition

### Separate the two control loops

A work-stealing loop runs when a worker lacks local ready work. It searches for an eligible queued item and transfers ownership before execution. A speculation loop runs when an attempt has executed long enough to be measured and peer evidence exists. It may create a second attempt while the primary remains live.

Keep separate events and metrics: `steal_requested`, `ready_item_transferred`, `clone_launched`, `attempt_won`, and `loser_fenced` describe different state transitions. A stolen task may later become a straggler and be speculated, but the scheduler must record both decisions independently.

### Expose ready parallelism

Only dependency-satisfied work belongs in a ready queue. A task waiting on a shuffle barrier, unavailable input, gang reservation, state handoff, or admission decision is not stealable merely because it appears in scheduler metadata. Materialize readiness from an authoritative DAG generation and invalidate it when upstream output or policy changes.

Per-worker queues reduce central contention and exploit warm local state. They can arise from initial placement, recursive fork/join, pull-based assignment, or locality-aware partitioning. The design must reveal enough surplus to idle workers without destroying the locality and batching that made local queues valuable.

### Use deques deliberately

In a common fork/join design, an owner pushes and pops from one end while thieves remove from the other. The owner gets recently created work with warm stack/cache context; thieves obtain older, often coarser subcomputations. This pattern is not mandatory for a distributed dataflow scheduler, but its asymmetry reduces synchronization and can improve granularity.

Deque indices, slots, and work-item generations must support one successful removal. A thief that loses a compare-and-set or lease race retries elsewhere; it does not execute the observed item anyway. Remote schedulers may implement this with a transactional queue, an owner RPC, or a durable claim record rather than shared-memory atomics.

### Select victims without a hotspot

Random victim selection distributes probes and avoids a central “most loaded worker” service whose view can be stale. Sampling two or a small number of candidates can choose the better visible surplus at modest cost. Topology-aware sampling can prefer a same-node or same-rack victim before wider search.

Pure randomness is not automatically fair or efficient. Exclude draining, unhealthy, incompatible, or protected workers; avoid repeatedly targeting the same victim; and use observed queue surplus without treating it as exact. A victim should retain enough work to stay busy. Sampling policy needs seeded replay in tests and entropy in production.

### Bound probes, batches, and contention

When many workers become idle together, unconstrained probes create a thundering herd. Limit outstanding requests, randomize victims, back off with jitter after empty/conflicted responses, and park workers when the system plausibly has no ready work. Wake them on new readiness rather than letting them spin indefinitely.

Stealing one tiny task can cost more than it saves. Batch claims amortize control overhead but risk draining the victim, moving too much data, or delaying high-priority work. Choose batch size from estimated duration, serialized descriptor/state size, locality, victim surplus, and thief capacity; cap both item count and predicted work.

### Preserve eligibility and scheduling policy

Before transfer, re-evaluate resources, architecture, devices, credentials, residency, data/state access, affinity/anti-affinity, priority, deadline, tenant quota, and failure-domain constraints. Some tasks are movable within a rack but not a region; some stateful work cannot move until a fenced handoff completes.

Stealing must not become an entitlement bypass. The thief executes under the task's tenant, priority, and resource accounting. A low-priority worker cannot take protected high-priority work merely to raise utilization. For gang/barrier stages, stealing one member without reserving the rest may create deadlock or wasted occupancy; steal the admissible gang or leave it queued.

### Balance locality against idleness

Initial queues often encode data or cache locality. Moving work may require a remote scan, shuffle fetch, model load, or state restore. Compare expected local wait with remote movement and execution cost as in [LSDS-054](054-data-local-task-placement.md). An idle worker is not free if it saturates a link needed by running tasks.

Use progressive scope: local worker, host, rack/zone, then wider candidates if waiting remains more costly. Preserve hard residency and attachment rules. Record original and execution location so locality loss and transfer amplification remain observable.

### Maintain one owner under failure

Give every logical item a generation and every assignment a unique lease/attempt identity. The victim atomically moves the item from queued to assigned-to-thief, or a shared store performs one conditional claim. A lease expiration is not permission for an old worker to keep publishing; the generation/epoch fences it.

If the owner crashes during transfer, reconciliation consults durable state: queued, offered, claimed, running, completed, or cancelled. An ambiguous RPC may be retried with the same request ID. The thief must learn whether it acquired the item rather than assuming failure means no transfer. Exactly-one assignment is a protocol property; exactly-once external effects require additional publication semantics.

### Detect a straggler, not merely a slow task

Elapsed time alone confuses large partitions, slow phases, late starts, and bad machines. Compare tasks with the same operator, input-size band, resource class, locality class, code/config generation, and relevant phase. Require sufficient completed peers or a trusted historical baseline. Normalize progress by bytes, records, iterations, or known work units when those measures are meaningful.

A straggler matters only if it lies near the stage/job tail or critical path. Cloning a slow task while hundreds of peers remain queued may displace more valuable ordinary work. Delay detection until there is evidence, but not so long that a clone cannot finish before the primary.

### Predict remaining time

For observed completed work $d$, total work estimate $D$, and elapsed runtime $t$, a simple linear rate is $v=d/t$ and predicted remaining time is $R_p=(D-d)/v$. This assumes stable rate and trustworthy progress. Startup, phase transitions, caching, spill, skew, GC, and nonlinear algorithms violate it.

Use phase-aware or survival models when justified, retain uncertainty intervals, and calibrate predictions by cohort. If total work is unknown, compare elapsed time with a robust cohort distribution but acknowledge weaker inference. Prefer estimated time to end over “slowest progress rate” when deciding which attempt most threatens completion.

### Decide whether a clone can win

Estimate clone queue/start delay $L_c$ and runtime $R_c$ on an eligible target. The gross predicted benefit is $B=R_p-(L_c+R_c)$. Require $B$ to exceed a safety margin and any deadline/cost threshold with adequate confidence. A positive mean benefit is insufficient if prediction error is large or the clone cannot get independent resources.

Prioritize the largest credible benefit on the critical tail, not every threshold crossing. Include the probability the primary finishes first, the duration for which both consume resources, data transfer, shuffle output, and cancellation latency. Disable or tighten speculation when headroom is low.

### Place clones independently

Do not clone onto the same host, disk, rack link, runtime pool, or degraded storage path suspected of causing slowness. Filter unhealthy/slow nodes and score distinct failure domains, data access, warmup, and predicted service. Independence is causal: different hosts can still share a saturated object-store prefix or downstream database.

If input skew is intrinsic, the clone repeats the same large work and probably loses. Split the partition, change the join/aggregation, or use skew-specific mitigation. If all tasks slow together, investigate shared backpressure or capacity rather than multiplying load.

### Separate logical tasks from attempts

The logical task ID binds DAG generation, partition/key range, input versions, plan/code/config, and expected output identity. The primary and clone receive distinct attempt IDs, credentials, scratch paths, logs, metrics, and leases. Downstream consumers reference the logical committed output, not an arbitrary attempt path.

Attempt-scoped identity supports cancellation and diagnosis. Logical identity supports deduplication and recovery. Reusing one ID for both makes it impossible to explain concurrent heartbeats, decide a winner, or clean a specific loser safely.

### Commit one valid winner

Each attempt writes isolated intermediate output and a manifest containing checksums, schema, partition identity, lineage, and attempt/generation. After validation, it conditionally installs the logical-task winner if no valid winner exists. The successful transaction publishes the winner pointer; losing attempts cannot overwrite it.

“First finished” means first valid attempt to win the commit, not first process to exit. A fast corrupt or wrong-generation result must lose. Scheduler restart reloads the durable winner record. Downstream readers resolve that record and ignore uncommitted attempt files.

### Fence cancellation and late completion

Cancellation is an optimization that saves resources; fencing is the correctness boundary. A loser may miss a signal, be partitioned, or finish while cancellation travels. Its expired lease or stale generation must prevent commit and external publication.

Track cancellation requested, acknowledged, process terminated, late result rejected, and cleanup completed separately. Retain attempt evidence long enough for audit. Garbage collection removes loser files only after no reader or recovery path can reference them.

### Protect shuffle and external effects

Speculative map attempts can produce multiple shuffle copies. Reducers must fetch only the committed attempt's registered blocks, or a shuffle service must atomically resolve logical partition to winner. Lost winner output follows the normal recomputation protocol; silently switching to a loser after publication can violate lineage.

Tasks that send email, charge accounts, mutate databases, acknowledge messages, or call non-idempotent services are unsafe to duplicate directly. Move effects behind an idempotency key and conditional transaction, or have attempts produce data for a single commit-aware publisher. Disable speculation when the sink/committer cannot support concurrent attempts.

### Address determinism and validation

Two correct attempts should produce semantically equivalent output for pinned inputs and execution context. Floating-point order, random seeds, clock reads, external lookups, and unordered iteration can differ. Define an equivalence rule where bit identity is unnecessary; otherwise pin nondeterministic inputs or reject speculative execution.

Validation can compare schema, range, record count, checksum, invariants, or sampled content before commit. Do not compare primary and clone only after publishing one: both might share a deterministic defect, and divergent outputs need containment and diagnosis.

### Govern resource amplification

Set per-task attempt caps, per-stage/job clone fractions, per-tenant concurrent clone limits, and a cluster-wide headroom gate. Charge CPU, memory, accelerator, storage, network, service quotas, and monetary cost for every attempt. Prioritize normal ready work when it offers more expected completion benefit.

Fairness accounting may charge instantaneous allocation or integrated resource-seconds. Either way, a tenant must not get free clones. Expose whether speculative capacity is reserved, opportunistic, preemptible, or counted against guarantees. Review energy and carbon effects alongside latency where relevant.

### Diagnose causes and validate policy

Correlate outliers with input size/key distribution, host health, CPU steal, GC, memory pressure, disk, network, storage/service latency, retries, locality, and backpressure. Quarantine bad infrastructure, repartition skew, tune memory/spill, repair code, or increase dependency capacity. Track how often a clone wins and why the primary was slow.

Validate with trace replay and controlled injection before canary rollout. Inject queue imbalance, empty victims, simultaneous thieves, claim ambiguity, worker crash, heterogeneous hosts, skew, GC pauses, slow disks, shared-link throttling, commit races, scheduler restart, cancellation loss, and external-effect faults. Gate on correctness first, then net tail benefit, duplicate-resource ratio, utilization, fairness, cost, and recovery behavior.

## Definitions and Notation

Let $w$ denote a worker and $Q_w$ its ready deque. A logical work item is $j=(g,p,i)$ for DAG generation $g$, partition/range $p$, and pinned input/plan identity $i$. A non-speculative assignment is $a=(j,e,w)$ with lease epoch $e$. An attempt $a_k$ is one execution of $j$; speculation permits several live $a_k$ but one committed winner.

Let $S_w$ be estimated stealable surplus at worker $w$, excluding work needed to keep the victim busy and items failing eligibility. Let $C_s$ be steal control/transfer cost and $T_j$ predicted task duration. A steal has useful granularity only when the expected reduction in idle/queue time materially exceeds $C_s$ and locality loss.

For a running primary, let $R_p$ be predicted remaining time. Let $L_c$ be clone queue and startup delay, $R_c$ clone runtime on its candidate, $M$ a safety/risk margin, and $B=R_p-(L_c+R_c)$ predicted benefit. Let $q$ be confidence that the clone path beats the primary, $C_c$ expected duplicate resource cost, and $H$ available headroom. Production admission can require thresholds on all of $B$, $q$, $C_c$, and $H$.

Let $A_j$ be the set of attempt IDs for $j$, and $W(j,g)$ be the durable winner record for generation $g$. The commit invariant is $|W(j,g)|\leq 1$. This does not claim only one attempt executed. A fence rejects any attempt whose task generation or lease epoch is older than the authoritative record.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Pin DAG generation, logical task/partition/input/plan identity, eligibility, priority, and tenant.
2. Admit only dependency-satisfied, unassigned, movable work to a ready queue.
3. Let idle workers sample eligible victims with bounded probes, backoff, and topology scope.
4. Atomically transfer a bounded item/batch under unique request, assignment, lease, and epoch identities.
5. Reconcile ambiguous transfer and worker failure from durable queued/claimed/running/completed state.
6. Build comparable attempt cohorts and estimate remaining time with uncertainty after sufficient evidence.
7. Admit a clone only when predicted benefit, independence, headroom, effect safety, fairness, and cost gates pass.
8. Run each attempt with isolated scratch/output, credentials, telemetry, and cancellation identity.
9. Validate output and atomically publish at most one winner; fence and clean every loser.
10. Replay failures and evaluate correctness, tail benefit, steal/clone overhead, amplification, fairness, and root-cause remediation.

For non-speculative work, suppose the queue removal/claim operation is linearizable and each item-generation has one authoritative state. Two thieves may observe $j$, but at most one conditional transition from `queued` to `claimed` succeeds. Therefore at most one current assignment exists. Liveness additionally requires retry/backoff, worker wakeup, lease recovery, and at least one eligible worker; the safety argument alone does not guarantee progress.

For speculation, multiple attempts are intentional. Suppose every attempt publishes only by a linearizable conditional install of $W(j,g)$, validation precedes installation, and stale generations are rejected. At most one attempt can install the winner, so downstream resolution observes one committed result. This proof does not cover non-transactional effects performed before commit; those require their own idempotency/transaction protocol or prohibition.

The benefit inequality is conditional. If estimates were exact and the clone starts at delay $L_c$, the clone beats the primary when $L_c+R_c<R_p$. Real estimates are uncertain and resource interference couples outcomes, so policy adds margin/confidence/headroom. Empirical calibration—not algebra alone—determines whether accepted clones improve production tails.

## Alternatives and Trade-Offs

- **Central global queue:** simple global ordering and visibility, but a throughput/availability hotspot and weaker locality than per-worker queues.
- **Work sharing/pushing:** loaded workers proactively send work; it can react early but needs trustworthy destination capacity and can push into congestion.
- **Pull-based stealing:** idle capacity initiates movement and naturally tracks demand; empty probes and stale victim views add overhead.
- **Random victim selection:** decentralized and robust to stale detail; topology, priorities, and skew may require filtered sampling.
- **Largest-queue victim:** targets visible surplus; maintaining exact global queue lengths can cost more than the improvement.
- **Single-item steals:** minimize victim drain and locality loss; control overhead dominates tiny items.
- **Batch steals:** amortize messages and feed parallel thieves; risk over-transfer, priority inversion, and stale claims.
- **Coarse tasks:** reduce launch/coordination cost; indivisible skew and stragglers become expensive.
- **Tiny tasks:** naturally balance queues and reduce tail impact; scheduler, metadata, serialization, and output overhead increase.
- **No speculation:** avoids amplification and duplicate-effect hazards; transient outliers determine stage completion.
- **Threshold speculation:** operationally simple; cohort heterogeneity and nonlinear progress create false positives.
- **Remaining-time prioritization:** targets tasks most likely to delay completion; depends on progress quality and calibrated prediction.
- **Kill-and-retry:** uses one attempt at a time and may escape a bad host; discards useful progress and loses the hedge.
- **Concurrent cloning:** preserves primary progress and reduces tail risk; doubles some resource usage until a winner emerges.
- **Partition splitting:** directly addresses divisible skew; requires operator/input support and safe result composition.
- **Capacity reservation for clones:** makes startup predictable; idle reserve reduces utilization when tails are healthy.
- **Opportunistic clones:** consume spare capacity cheaply; may start too late or disappear under preemption.

## Failure Modes and Misconceptions

- **“Stealing and speculation are synonyms.”** Stealing moves queued work; speculation duplicates running work.
- **“An empty local queue proves the worker should steal.”** The worker may be blocked, in a barrier, draining, incompatible, or intentionally reserved.
- **“Any visible queue item is stealable.”** Dependencies, leases, locality, state, gangs, priority, and policy may forbid transfer.
- **“A failed steal RPC means nothing was assigned.”** Ambiguous delivery requires idempotent request identity and reconciliation.
- **“Random probing cannot overload anything.”** Thousands of synchronized thieves can hammer the same workers and network.
- **“More stolen tasks imply better balance.”** Excess movement can reduce locality, increase contention, and drain victims.
- **“The longest-running attempt is the best clone candidate.”** It may process a larger partition or be seconds from completion.
- **“Low progress rate proves a bad machine.”** Progress units may be nonlinear, phase-specific, or dominated by input skew.
- **“A clone on another host is independent.”** Attempts may share storage, network, locks, quotas, services, or poison input.
- **“Cloning skew fixes skew.”** Both attempts repeat the same excess work; splitting or repartitioning is usually required.
- **“First process exit should win.”** Only a validated, current-generation result may win the atomic commit.
- **“Cancellation prevents duplicate output.”** Delayed or lost cancellation requires commit fencing.
- **“Deterministic code needs no attempt isolation.”** File paths, counters, locks, logs, and shuffle registration can still collide.
- **“Only the winning attempt consumes quota.”** Every attempt uses capacity and must be charged and observed.
- **“Speculation always helps at the tail.”** Under correlated overload, clones increase the bottleneck and worsen the tail.
- **“A high clone win rate proves success.”** Aggressive early cloning can win often while wasting resources and harming other jobs.
- **“Mitigation removes the need for repair.”** Persistent winners on particular hosts or data shapes are diagnosis signals.

## Worked Examples

### Example 1

Worker A has twelve ready 40-second tasks; worker B is idle. B steals three eligible tasks in one transaction while A retains enough work for its slots. The transfer improves parallelism if remote input and the claim message cost less than the queue wait it removes. It is work stealing: none of the three tasks had begun, and each retains one live assignment.

### Example 2

Fifty workers finish simultaneously and all probe worker A. A bounded protocol lets A serve four randomized/batched requests, rejects the rest cheaply, and tells unsuccessful thieves to back off with jitter. A readiness notification later wakes parked workers. Without those controls, queue-lock and RPC pressure can make A slower despite abundant work.

### Example 3

A queued task requires a local persistent volume and trusted-node label. An idle worker in another zone cannot steal it, even after waiting. The hard attachment and security filters precede utilization scoring. A same-zone worker with the volume attachment capability may steal it under the storage protocol; locality timeout cannot legalize the first worker.

### Example 4

A barrier stage needs eight workers concurrently. Stealing two members onto otherwise idle nodes without reserving the other six occupies slots but cannot cross the barrier. The scheduler must admit and place the gang as a unit, use a protocol that guarantees remaining members, or leave it queued. Ordinary independent-task stealing does not preserve gang liveness.

### Example 5

Two thieves receive the same stale queue snapshot. Each issues a conditional claim for item generation 19. One changes `queued` to `claimed(attempt-41, epoch-8)`; the other observes conflict and does not execute. If the successful reply is lost, retrying request 41 returns the recorded assignment instead of making another one.

### Example 6

A 600-partition stage has 540 completions. One remaining attempt has run 90 seconds but processed only 20% of a 100-unit partition; comparable tasks normally finish in 30–45 seconds. Its linear remaining estimate is 360 seconds. Because it is on the tail and a healthy target predicts 45 seconds after 5 seconds startup, it is a strong speculation candidate if resource and safety gates pass.

### Example 7

Another attempt processes a partition eight times larger than its peers at a normal bytes-per-second rate. Cloning repeats the large scan and merge, so both attempts remain slow and double network traffic. The correct mitigation is to split the key range, salt the heavy key, change the join, or otherwise address [LSDS-039](039-skewed-keys-and-heavy-hitters.md).

### Example 8

Primary and clone each write an attempt-scoped shuffle directory. The clone finishes first, validates its 64 blocks, and atomically installs its attempt ID as the map partition winner. Reducers resolve only that registration. The primary later finishes but its stale commit fails; cancellation and garbage collection remove its blocks after readers can no longer reference them.

### Example 9

A task writes a database row and sends an invoice email during execution. Launching a clone can perform both effects twice even if only one file output commits. The task must instead write an effect intent keyed by logical task and business operation; one transactional publisher claims and emits it, or speculation stays disabled for that task.

### Example 10

The following deterministic fixture applies a deliberately simple linear progress estimate. Production use also needs cohort validity, confidence, placement independence, resource headroom, cost, and effect-safety gates.

<!-- bijux-verify: {"id":"remaining-time-speculation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"remaining=(('fast', 7.5), ('straggler', 280.0), ('moderate', 60.0))\nspeculate=('straggler', 'moderate')\n","stderr":""}} -->
```python
observations = (
    ("fast", 100, 80, 30),
    ("straggler", 100, 20, 70),
    ("moderate", 100, 50, 60),
)
clone_seconds = 35.0
margin_seconds = 5.0

remaining = []
speculate = []
for name, total, completed, elapsed in observations:
    rate = completed / elapsed
    seconds_left = round((total - completed) / rate, 1)
    remaining.append((name, seconds_left))
    if seconds_left > clone_seconds + margin_seconds:
        speculate.append(name)

print(f"remaining={tuple(remaining)}")
print(f"speculate={tuple(speculate)}")
```

The fixture selects the two attempts with more than 40 predicted seconds left. It does not prove they should be cloned in a live cluster: the model treats progress as linear and clone runtime as known.

## Cross-Program Connections

- **Algorithms and data structures:** concurrent deques, atomic claims, randomized sampling, amortized analysis, critical paths, and queueing determine mechanism cost.
- **Distributed systems:** leases, epochs, idempotent requests, linearizable winner records, failure detectors, and reconciliation preserve ownership under faults.
- **Data engineering:** partitions, skew, shuffle, spill, state, and sink semantics determine whether movement or duplication helps and remains correct.
- **Platform engineering:** node health, topology, resource vectors, scheduler plugins, quotas, telemetry, and cancellation implement the policy.
- **Reliability engineering:** tail analysis, fault injection, fencing, degraded modes, cleanup, rollback, and root-cause repair contain amplification.
- **Security engineering:** tenant identity, credentials, residency, effect authorization, audit, and cross-tenant fairness remain attached to stolen and cloned work.
- **Performance engineering:** granularity, locality, contention, progress estimation, critical-tail benefit, and coordinated omission shape measurements.
- **Economics and sustainability:** duplicate CPU/network/storage, opportunity cost, monetary transfer charges, and energy constrain tail-latency hedging.

## References

1. Blumofe et al. [The Cilk Language and Work-Stealing Scheduler.](https://www.usenix.org/legacy/publications/library/proceedings/ana97/full_papers/blumofe/blumofe_html/node2.html) Primary description of ready deques, random victims, stealing, work/span performance, and structured computation.
2. Oracle. [ForkJoinPool (Java SE 25).](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ForkJoinPool.html) Current platform API for work-stealing execution, worker behavior, monitoring, blocking caveats, and lifecycle.
3. Delgado et al. [Hawk: Hybrid Datacenter Scheduling.](https://www.usenix.org/conference/atc15/technical-session/presentation/delgado) Primary cluster-scheduler work using randomized work stealing to improve heterogeneous workload scheduling.
4. Ousterhout et al. [The Case for Tiny Tasks in Compute Clusters.](https://www.usenix.org/conference/hotos13/session/ousterhout) Primary analysis of task granularity as a load-balancing and tail-mitigation choice.
5. Dean and Ghemawat. [MapReduce: Simplified Data Processing on Large Clusters.](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) Primary data-parallel scheduling paper covering task attempts, backup execution, locality, and output handling.
6. Zaharia et al. [Improving MapReduce Performance in Heterogeneous Environments.](https://www.usenix.org/conference/osdi-08/improving-mapreduce-performance-heterogeneous-environments) Primary LATE paper on remaining-time prioritization, fast-node selection, and speculative caps.
7. Ananthanarayanan et al. [Reining in the Outliers in Map-Reduce Clusters Using Mantri.](https://www.usenix.org/legacy/event/osdi10/tech/techAbstracts.html) Primary system publication on cause- and resource-aware outlier mitigation.
8. Dean and Barroso. [The Tail at Scale.](https://research.google/pubs/the-tail-at-scale/) Primary synthesis of latency-tail causes and hedging/tail-tolerance techniques at large scale.
9. Apache Spark. [Configuration: Speculative Execution.](https://spark.apache.org/docs/latest/configuration.html) Current speculation enablement, interval, quantile, runtime, multiplier, and efficiency controls.
10. Apache Hadoop. [JobConf API.](https://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapred/JobConf.html) Current MapReduce task-attempt and map/reduce speculative-execution controls.
11. Apache Flink. [Speculative Execution.](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/speculative_execution/) Current batch speculation, slow-task detection, blocked-node placement, winner/cancellation, source, and sink constraints.
12. Kubernetes. [Jobs.](https://kubernetes.io/docs/concepts/workloads/controllers/job/) Current indexed logical work identity, duplicate Pod possibility, first-success counting, retries, and cleanup behavior.
13. Verma et al. [Large-Scale Cluster Management at Google with Borg.](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) Primary production cluster-management paper covering task identity, rescheduling, priority, quota, packing, and availability policy.

## Exercises

### Exercise 1

State the semantic difference between stealing queued task $j$ and speculating running task $j$. Give the identity and atomicity requirement for each.

### Exercise 2

A victim has ten eligible 50-second tasks queued and two slots. An idle four-slot worker can steal tasks for a 4-second transfer/setup cost per batch. Design a bounded batch decision, and list assumptions that prevent the arithmetic from being a complete policy.

### Exercise 3

A primary has predicted remaining time 150 seconds. A clone has 12 seconds queue/start delay and predicted runtime 80 seconds. Policy margin is 20 seconds. Compute $B$ and decide basic eligibility. Then name at least five additional gates.

### Exercise 4

Design a safe speculative shuffle-output protocol that survives simultaneous completion, scheduler crash after winner selection, lost cancellation, and late loser output.

### Exercise 5

Design a production evaluation comparing no mitigation, work stealing only, speculation only, and both. Include workloads, faults, correctness, performance, resource, fairness, cost, canary, and rollback evidence.

## Answers to the Exercises

### Answer 1

Stealing moves $j$ from a ready queue to one worker before execution and intends one live assignment. Its atomic transition is one conditional `queued` to `claimed(assignment, epoch)` change with idempotent request recovery. Speculation leaves the primary running and creates another attempt for the same logical $j$. Each attempt has a distinct ID and isolated output, while one conditional winner record for the pinned logical generation permits at most one validated result to publish. Both require stale-generation fencing; only speculation intentionally duplicates computation.

### Answer 2

The thief has four slots and the victim should retain at least two tasks for its two slots, so stealing at most four tasks leaves six and can occupy the thief. One batch pays about four seconds rather than four separate control/setup costs; each 50-second task offers enough work to amortize that simplified cost. The scheduler should cap the batch by four items and predicted work, transfer atomically, and reduce it if the victim's running tasks will finish soon. Missing factors include data/state movement, input locality, queue age/priority, tenant fairness, resource-vector fit, failure domains, task-duration uncertainty, victim arrivals, serialization cost, gang constraints, and shared network contention.

### Answer 3

$B=150-(12+80)=58$ seconds. Because 58 exceeds the 20-second margin, the simple time gate passes. Additional gates include prediction confidence, valid comparison cohort, critical-tail position, independent placement, cluster headroom, per-job/tenant clone cap, duplicate resource/cost budget, pinned deterministic input, attempt-isolated output, safe external effects, target health/locality, deadline relevance, and cancellation/fencing support.

### Answer 4

Assign stable logical partition/generation identity and unique attempt IDs. Each attempt writes immutable attempt-scoped blocks plus a validated manifest. A linearizable conditional transaction installs one attempt ID as the logical winner; both simultaneous finishers may validate, but only one install succeeds. Persist the winner independently of scheduler memory before exposing it. Reducers resolve and pin that winner rather than listing arbitrary attempt directories. After restart, the scheduler reloads the same record. Cancellation saves resources but is not trusted: stale leases/generations fence loser registration and publication even if a loser finishes late. Garbage collection waits until readers and recovery no longer reference attempts, then removes all non-winner blocks with auditable tombstones.

### Answer 5

Replay representative DAGs spanning balanced/skewed inputs, tiny/coarse tasks, local/remote data, heterogeneous workers, barriers, shuffle, safe/unsafe sinks, and multiple tenants. Compare the four policies under queue imbalance, simultaneous idle workers, worker/scheduler loss, slow CPU/disk/network, GC pause, shared-service throttling, skew, commit races, and lost cancellation. First assert no duplicate assignment where disallowed, one valid winner, fenced stale attempts, correct shuffle resolution, effect deduplication, recovery, and cleanup. Then measure queue/idle time, steal success/probes/bytes, stage/job percentiles, deadline misses, clone launch/win/useful rate, duplicated resource-seconds and bytes, congestion, utilization, fairness/slowdown by tenant, monetary/energy cost, and root-cause classifications. Calibrate thresholds offline, shadow decisions, canary by workload and cluster, stop on correctness or fairness regressions, retain feature flags and the prior scheduler configuration, and roll back atomically while allowing already-issued attempts to reconcile safely.
