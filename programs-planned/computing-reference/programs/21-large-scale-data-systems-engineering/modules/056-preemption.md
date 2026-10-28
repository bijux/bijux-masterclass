---
module_id: LSDS-056
program: Large-Scale Data Systems Engineering
level: 2
module_number: 56
title: Preemption
status: complete
last_verified: 2026-09-04
---

# Preemption

## One-Page Review

### Governing question

When and how should a cluster revoke resources from running data workloads so higher-value or entitled work can start, while bounding lost work, preserving application safety, and preventing starvation or disruption cascades?

### Essential definitions

- **preemption** revokes an allocation from a running or admitted workload to satisfy a scheduling policy or urgent resource need.
- The **preemptor** is the blocked workload or policy demand to be served; a **victim** is an allocation selected for revocation.
- **eviction** asks a workload to terminate and release resources; not every eviction is caused by scheduler preemption.
- **kill preemption** terminates a victim; **requeue preemption** returns it to pending state; **suspend/resume** pauses CPU execution while retaining some state/resources.
- **checkpoint-and-restart** persists recoverable state before termination and later resumes from that state.
- **grace period** is bounded time between notice and forced termination.
- **disruption budget** limits simultaneous voluntary unavailability for a protected workload.
- **reclamation** takes borrowed/idle capacity back for its entitled owner; **priority preemption** serves a more important workload.
- **preemption debt** records repeated harm so future selection avoids chronic victims and preserves long-run fairness.
- **released capacity** is resource capacity actually reusable by the preemptor, not merely marked for termination.

### Central model, mechanism, or theorem

For blocked preemptor $p$, calculate its resource deficit vector $\Delta_p$ on each feasible placement. Choose an eligible victim set $V$ whose actually releasable resources cover that deficit after grace/cleanup, while minimizing disruption cost

$$C(V)=\sum_{v\in V}(L_v+R_v+S_v+F_v)+P(V),$$

where $L_v$ is lost work, $R_v$ restart/restore cost, $S_v$ service/state risk, $F_v$ fairness debt, and $P(V)$ interaction penalty. The selection is admissible only if policy authorizes $p$ over every victim, hard availability/state/security constraints hold, the released vector fits $p$ in one valid placement, and predicted start benefit exceeds disruption and delay. Preemption is a state machine: decide, reserve intent, notify, checkpoint/drain, fence, terminate, confirm release, bind the preemptor, requeue/recover victims, and reconcile failures.

### Critical invariants

- Only an authorized priority, guarantee, quota reclamation, deadline, or safety rule can preempt.
- Victims are selected from capacity the preemptor can actually use on one feasible placement.
- Protected quorum, disruption, residency, state-ownership, and minimum-service constraints remain satisfied.
- Every decision is generation-scoped, idempotent, auditable, and fenced against stale victim or preemptor actions.
- Grace is bounded; forced termination occurs only after policy-defined notice and durability rules.
- Capacity is credited only after the runtime confirms it is reusable.
- Victim checkpoints and outputs are committed atomically or discarded; partial effects cannot masquerade as progress.
- Requeued work retains identity, attempt history, priority aging, and fair accounting without double publication.
- Rate, concurrency, tenant, and topology limits prevent disruption storms and correlated loss.
- Repeated victimization accumulates protection/debt so opportunistic work does not become permanently starved.

### Common failures

Common failures include equating queue priority with permission to kill; selecting many small victims that still do not create a feasible resource vector; preempting a quorum or all replicas in one failure domain; counting terminating processes as free; allowing unbounded grace to block the preemptor; killing checkpointable work just before a checkpoint; suspending jobs that retain the memory or license the preemptor needs; requeueing poison work forever; losing task generation/output fencing; evicting the same tenant repeatedly; triggering reciprocal preemption loops; bypassing disruption budgets; and measuring “victims selected” instead of preemptor start, victim recovery, lost work, and cross-tenant impact.

### Compact example

A preemptor needs 6 CPU and 10 GiB on one node, which has 2 CPU and 4 GiB free: its deficit is (4 CPU, 6 GiB). Two eligible batch victims release (2,4) and (2,2) with combined disruption cost 25. A single alternative releases (4,8) at cost 40. If all constraints and release times are comparable, choose the two-victim set. Do not combine resources from different nodes unless the preemptor can span them.

### Connections

[LSDS-048](048-state-snapshots-and-recovery.md) defines recoverable state, [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) protects effects, [LSDS-051](051-cluster-resource-models.md) defines resource vectors, [LSDS-052](052-static-and-dynamic-allocation.md) explains allocation lifecycle, [LSDS-053](053-fair-and-capacity-scheduling.md) supplies entitlement, and [LSDS-054](054-data-local-task-placement.md) constrains feasible replacement placement.

## Governing Question

Without preemption, a cluster can promise priority or minimum shares yet fail to deliver them until existing work finishes. A short emergency pipeline may wait behind hours-long best-effort tasks. A queue may be entitled to capacity currently borrowed by another queue. A gang may need a contiguous vector that idle fragments cannot satisfy. Preemption makes such promises enforceable by revoking allocations.

Revocation is not free. A killed map task loses compute; a stateful operator may need a checkpoint and replay; a suspended process can retain memory, devices, or licenses; a service replica can reduce availability; a shuffle producer can invalidate downstream data. Grace and checkpointing reduce loss but delay the preemptor. The scheduler must decide whether the benefit of earlier admission justifies the disruption and which victims create usable capacity at least cost.

The governing question covers four linked problems: policy authority, feasible victim-set selection, safe execution of revocation, and recovery/accounting afterward. A system that solves only the knapsack-like selection problem can still corrupt state, strand capacity, or repeatedly punish one tenant.

## Why This Matters

Priority without enforceable reclamation is advisory. When workloads are long-running, non-preemptive queues can violate response objectives and minimum-share guarantees for long periods. Preemption lets a cluster reserve little or no idle capacity while still admitting urgent work, reclaiming borrowed quota, and converging toward fair allocation.

Data systems make disruption unusually expensive. Intermediate shuffle may be executor-local. Stateful streams hold large keyed state. Training or iterative jobs accumulate in-memory progress. External sinks may observe partial effects. A choice that looks cheap in CPU/memory can trigger terabytes of recomputation or long checkpoint restore. Scheduler policy needs application-level recovery metadata, not just process identifiers.

Fragmentation also matters. A preemptor needing one 8-GPU host is not helped by evicting eight one-GPU tasks on different hosts. A task needing 100 GiB memory cannot use reclaimed CPU without memory. The vector must fit a feasible node, rack, topology, device, volume, security, and gang placement.

Preemption can amplify failure. Simultaneously stopping all replicas, checkpointing thousands of jobs to one object store, or restarting victims together creates correlated load. Repeated oscillation consumes resources without useful work. Rate limits, topology-aware selection, hysteresis, and restart smoothing are therefore safety controls.

The mechanism is a governance boundary. Priorities can be abused to evict other users; quota reclamation can surprise borrowers; operators can bypass voluntary-disruption APIs; and chronic victimization can make “best effort” effectively “never completes.” Explicit authorization, quotas on high priorities, audit trails, debt/aging, and published service contracts are required.

## Prerequisites and Retrieval

Review checkpoint coordination and state recovery in [LSDS-047](047-checkpoint-barriers.md) and [LSDS-048](048-state-snapshots-and-recovery.md), replay-safe effects in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), resource models and allocation in [LSDS-051](051-cluster-resource-models.md) and [LSDS-052](052-static-and-dynamic-allocation.md), fair/capacity scheduling in [LSDS-053](053-fair-and-capacity-scheduling.md), locality in [LSDS-054](054-data-local-task-placement.md), and attempts/fencing in [LSDS-027](027-task-retry-and-speculation.md).

You should understand resource vectors, placement feasibility, priority and entitlement, borrowing, leases and generations, task attempts, checkpoint barriers, shuffle lineage, idempotent effects, quorum/availability, failure domains, queueing delay, and conditional transactions.

## Learning Objectives

After this module, you should be able to:

1. distinguish scheduler preemption, eviction, node-pressure termination, cancellation, and ordinary failure;
2. derive preemption authority from priority, guarantee, quota reclamation, deadline, or safety policy;
3. compute per-placement resource deficits and choose feasible victim sets rather than scalar capacity totals;
4. estimate lost work, checkpoint/restart, service risk, fairness debt, and interaction costs;
5. choose kill, requeue, suspend/resume, checkpoint/restart, shrink, or application-aware drain;
6. design notice, grace, fencing, termination, release confirmation, and binding state transitions;
7. protect replicated services, gangs, stateful operators, shuffle, local storage, and external effects;
8. prevent cascades, oscillation, starvation, priority abuse, and correlated restart load;
9. account for every disruption and restore victims fairly; and
10. validate policy using preemptor outcomes, victim recovery, lost work, availability, fairness, and cost.

## Core Exposition

### Classify the initiating condition

Preemption needs a durable reason code. Common authorities are higher priority, a minimum-share or reservation violation, reclaiming borrowed quota for its owner, a deadline policy, an administrative emergency, or resource-safety enforcement. Node-pressure eviction may terminate workloads too, but it responds to local exhaustion rather than a pending preemptor selected by the scheduler.

Keep these paths distinct in events and accounting. An involuntary hardware loss is not voluntary policy disruption. User cancellation is not a victim-selection decision. The reason determines authorization, disruption-budget handling, notification, compensation, and SLO reporting.

### Verify the preemptor is genuinely blocked

First attempt ordinary placement, backfilling, queue reorder, elastic resize, and eligible alternative resources. Pin the preemptor's generation, resource vector, topology, device, volume, security, gang, and deadline constraints. If it cannot run even after candidate victims leave, preemption only creates harm.

Re-evaluate admission and quota. A malicious or misconfigured workload must not trigger eviction by claiming a nonexistent high priority or impossible vector. Reserve its queue position and decision generation while victims terminate so another workload cannot consume the reclaimed resources unexpectedly.

### Compute deficits per feasible placement

For candidate node or placement group $n$, compute $\Delta_{p,n}=\max(0,r_p-f_n)$ componentwise, where $r_p$ is requested resources and $f_n$ currently free capacity. Include CPU, memory, accelerators, ephemeral storage, I/O/network classes, ports, licenses, volume attachments, and any extended resource.

Do not sum victims cluster-wide unless the workload can span those locations. Filter candidates violating hard affinity, residency, architecture, topology, health, or gang rules. The result is a set of local victim-selection problems plus global policy constraints.

### Define victim eligibility

A victim must be lower in the applicable policy order or be consuming reclaimable borrowed capacity. Exclude protected system workloads, non-preemptible classes, indispensable quorum members, tasks inside a minimum protected runtime, incompatible disruption states, and allocations whose removal cannot free required resources.

Eligibility is time-dependent. A workload may become safe after its next checkpoint, another replica becomes ready, or an exemption window ends. Conversely, a disruption budget can close when a replica fails. Revalidate immediately before the irreversible action.

### Estimate disruption cost

Lost work includes compute since the last durable checkpoint/materialization, plus in-flight shuffle and uncommitted output. Restart cost includes queue delay, image/model/input loading, state restore, replay, cache warming, and downstream recomputation. Service risk covers unavailable replicas, quorum margin, connection draining, and customer impact.

Fairness cost accounts for past victimization, remaining service, age, and entitlement. Interaction penalties capture choosing multiple replicas, checkpointing many jobs to one store, evicting adjacent shuffle producers, or triggering synchronized restarts. Cost estimates require uncertainty and conservative floors; a task with no progress report is not free.

### Choose a minimal feasible victim set

Victim selection is a multidimensional covering problem. Minimize cost subject to componentwise resource coverage, placement, policy, and safety constraints. Greedy “lowest priority first” is easy but can kill many tasks or miss a feasible vector. Exact enumeration is possible for small candidate sets; larger systems use bounded search and heuristics.

Prefer fewer disruptions when costs are similar, but not if one huge victim loses hours of work. Account for expected release time: graceful shutdown or checkpoint may make a nominally cheap victim too slow for the preemptor's deadline. Preserve a fallback set if a selected victim does not release capacity.

### Select the least destructive mechanism

Kill/cancel releases most resources quickly and loses volatile progress. Requeue terminates then restarts under the same logical job, suitable when the framework already tolerates attempts. Checkpoint-and-restart preserves progress at storage and time cost. Suspend/resume can preserve memory state but may retain exactly the memory, accelerator context, local disk, or license needed by the preemptor.

Elastic shrink asks a malleable job to release workers or parallelism without killing the whole job. Application-aware drain stops new input, commits a checkpoint, hands off state, and exits. Choose per workload/resource; one global preemption mode is rarely correct.

### Coordinate notice and grace

Write a durable preemption intent before notification, with reason, decision generation, deadline, expected resources, and target recovery mode. Signal the application once using an idempotent request. Grace lets it drain, checkpoint, flush telemetry, or reject unsafe timing under policy.

Grace must be bounded and included in the preemptor start estimate. If the application completes before the deadline, record ordinary completion while still reconciling intent. If grace expires, enforce the declared action. Do not extend grace indefinitely through repeated notices.

### Make checkpointing trustworthy

A preemption checkpoint must use the same correctness protocol as a failure-recovery checkpoint: consistent state, pinned sources, durable metadata, checksums, atomic publication, and sink coordination. A local file that disappears with the victim is not recovery.

Schedule around checkpoint cadence when delay is acceptable. If a checkpoint is nearly complete, waiting can greatly reduce lost work; if the preemptor has an immediate safety deadline, forced termination may win. Cap concurrent checkpoint bandwidth so mass preemption does not overload storage or backpressure unrelated jobs.

### Fence outputs and state ownership

Assign a new attempt/ownership epoch when a victim is requeued or state moves. The old process may outlive termination signaling or return after a network partition. Every state update, shuffle registration, checkpoint commit, and external publication must reject stale epochs.

Exactly one logical task result may become current. External effects require idempotency keys, transactions, or a commit-aware publisher. Preemption is operationally similar to failure from the task's perspective; it does not waive replay-safety requirements.

### Confirm resources are actually reusable

Marking a workload `terminating` does not free memory, devices, volumes, ports, local storage, or licenses. The node/runtime must confirm process death, cleanup, detach, and resource-ledger update. Suspended workloads retain declared resources. Graceful processes can linger.

Only then bind or start the preemptor. Keep the reservation scoped to the intended preemptor or policy class while release occurs. If cleanup fails, quarantine the resource and try another feasible victim set rather than double-allocating.

### Protect services and quorum systems

For replicated services, check current health, zone/rack distribution, quorum, leader role, ongoing rollouts, and involuntary failures. A disruption budget is a coordination interface, not proof that the application is safe in every failure scenario. Preemption should prefer redundant, healthy, non-leader replicas and serialize disruptions.

High priority alone must not take the cluster below a hard safety floor. Where emergency policy can override a soft budget, make the override explicit, narrowly authorized, and audited. Replacement readiness may need to precede victim termination.

### Handle gang and distributed workloads

Preempting one worker from an all-or-nothing gang can strand the remaining workers while freeing too little for the preemptor. Model the victim at workload/gang scope, or use an application-supported shrink protocol. Likewise, a preemptor gang needs its entire feasible resource set reserved before disruption begins.

For distributed training, membership and collective communication may fail when one worker leaves. A coordinated checkpoint and whole-job requeue may cost less than cascading timeouts. Track topology and network reservations as part of the vector.

### Handle batch dataflow and shuffle

Batch tasks often tolerate attempt loss, but local intermediate output can make the true cost much larger than one task's elapsed runtime. If a preempted map produced shuffle blocks already consumed or needed, preserve them through an external shuffle service or account for map recomputation and reducer fetch failure.

Prefer victims at safe boundaries between tasks/stages or just after durable materialization. Requeue logical tasks with new attempts and preserve winner fencing. Avoid simultaneously preempting many producers for the same downstream stage.

### Handle stateful streaming

A stateful operator needs a consistent checkpoint/savepoint, input position, timer state, and sink transaction boundary. Application-aware drain may be mandatory. State transfer and replay time must enter cost; maintaining service capacity during restore may require overlapping replacement rather than immediate reclamation.

Preempting one hot-key owner can increase backlog and checkpoint pressure across the job. Coordinate at job graph level, rate-limit concurrent moves, and validate end-to-end processing/effect semantics. “Restartable” does not mean “cheaply preemptible.”

### Integrate fairness and borrowing

Capacity lending improves utilization when owners are idle. Reclamation makes lending credible: borrowers accept that resources may be taken back under published rules. Prefer reclaiming above-guarantee or borrowed usage before disrupting within-guarantee allocations.

Priority and fair share interact. A high-priority workload should not necessarily evict guaranteed service from another tenant if policy forbids it. Charge the preemptor and victims accurately, retain victim age/deficit, and record preemption debt to prevent the same low-priority job from restarting forever.

### Prevent starvation and priority abuse

Use priority quotas, admission controls, maximum concurrent disruptions, victim exemption windows, aging, restart credits, and per-tenant debt. Cap how much high-priority demand can arrive without reservation. Otherwise a tenant can label all work urgent and externalize its queueing cost.

Best-effort work may be preemptible, but its contract should still specify whether eventual progress is expected. If yes, provide protected windows, backfill estimates, checkpoint support, or isolated capacity. Observe completed useful work, not merely allocation time.

### Prevent oscillation and cascades

Do not let a victim immediately preempt another workload on requeue unless policy explicitly allows it. Add hysteresis between trigger and release thresholds, minimum runtimes, and cooldowns. Maintain one authoritative preemption graph to detect cycles and superseded intents.

Spread checkpoint and restart traffic. Rate-limit by node, rack, storage system, tenant, and application. During degraded capacity, tighten protection because each additional disruption consumes scarce recovery bandwidth.

### Observe the full lifecycle

Record preemptor/victim IDs and generations, reason/policy rule, candidate placement, deficit vector, candidates rejected with reasons, selected set/cost, notice/grace, checkpoint outcome, fence/termination, actual release time/vector, preemptor start, and victim recovery/completion.

Metrics include decision and release latency, useful capacity reclaimed, preemptor start/deadline benefit, victims and lost work, checkpoint/restore bytes/time, restart count, disruption-budget pressure, stale-action rejects, fairness/debt, service availability, storage/network spikes, and cost. Attribute failures to policy, runtime, application, or infrastructure.

### Validate and roll out conservatively

Replay production traces with exact vectors/topology and simulate counterfactual start/recovery times. Inject slow termination, hung checkpoint, node loss during grace, stale controller, duplicate intent, scheduler restart, resource-ledger lag, unavailable storage, lost signal, victim completion, preemptor cancellation, and rollback.

Start with shadow recommendations, compare selected sets with operator expectations, and then canary preemptible workload classes. Put correctness, availability, and maximum-disruption gates ahead of latency gains. Keep a kill switch and versioned prior policy; reconcile already-issued intents during rollback rather than forgetting them.

## Definitions and Notation

Let preemptor $p$ request resource vector $r_p$. Candidate placement $n$ has free vector $f_n$, so deficit is $\Delta_{p,n}=\max(0,r_p-f_n)$ componentwise. Each victim $v$ has allocated vector $r_v$, releasable vector $u_v\leq r_v$, expected release time $t_v$, and eligibility predicate $E(p,v,n)$.

For victim set $V$, require $\sum_{v\in V}u_v\succeq\Delta_{p,n}$ on the same feasible placement. Disruption cost is $C(V)=\sum(L_v+R_v+S_v+F_v)+P(V)$: lost work, recovery, service/state risk, fairness debt, and interactions. These components must be normalized to a declared objective or shown separately.

Let $T_p^0$ be predicted start without preemption and $T_p^V$ start after notice, checkpoint, termination, cleanup, and bind. Gross start benefit is $G=T_p^0-T_p^V$. Preemption is economically plausible only if weighted benefit exceeds $C(V)$ with adequate confidence and policy authority. A deadline or safety rule may use lexicographic rather than monetary comparison.

A preemption intent $I=(p,g_p,V,g_V,d,m)$ pins preemptor/victim generations, deadline $d$, and recovery mode $m$. Durable victim state progresses through selected, notified, draining/checkpointing, fenced, terminating, released, requeued/restoring, and recovered/finished. Transitions are idempotent and monotone except explicit supersession.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Authenticate the request and resolve the exact priority, guarantee, reclamation, deadline, or safety authority.
2. Pin preemptor identity/generation and prove it is blocked after ordinary feasible placement and elastic alternatives.
3. Compute componentwise deficits separately for each feasible node/topology/gang placement.
4. Filter victims by policy, resource usefulness, disruption/quorum/state rules, minimum runtime, and current generation.
5. Estimate lost work, restore, release time, service/state risk, fairness debt, and correlated interaction cost.
6. Choose a bounded, minimal-cost feasible set and persist an idempotent intent/reservation with fallback.
7. Notify once, grant bounded grace, checkpoint/drain under storage/rate limits, then fence and terminate as declared.
8. Confirm actual reusable resources before binding the intended preemptor; quarantine ambiguous cleanup.
9. Requeue/restore victims with new epochs, retained priority/debt/accounting, safe output/effect semantics, and smoothed load.
10. Reconcile controller failures and validate preemptor benefit, victim completion, availability, fairness, amplification, and rollback.

If every admitted victim set covers $\Delta_{p,n}$ using actually releasable vectors on placement $n$, then after confirmed releases the preemptor's vector fits there, assuming no intervening allocation consumes the reserved capacity. This explains why intent reservation and release confirmation are necessary. Cluster-wide scalar totals do not prove placement feasibility.

If victim generations are fenced before replacement attempts publish, and every durable state/output commit conditionally checks the current generation, then an old victim cannot overwrite new ownership after delayed termination. This safety sketch assumes all effect paths participate; an uncontrolled external side effect remains outside it.

Long-run fairness needs more than local cost minimization. If the cheapest victim is always the same workload, repeated selection can prevent completion. Aging, debt, exemptions, or progress guarantees change future eligibility/cost so accumulated service loss is eventually protected under the declared contract.

## Alternatives and Trade-Offs

- **No preemption:** simplest recovery and stable execution; priority and share guarantees may wait for long tasks.
- **Reserved idle capacity:** urgent work starts predictably; utilization and economics suffer when reserve is unused.
- **Backfilling:** fills gaps with work expected to finish before reservations; duration errors can still delay priority work.
- **Kill/cancel:** fastest full release; maximizes lost progress and may abandon the logical workload.
- **Requeue:** integrates with attempt-based batch recovery; repeated victims can thrash without aging/debt.
- **Checkpoint/restart:** preserves progress; checkpoint time/storage load can exceed the admission benefit.
- **Suspend/resume:** resumes quickly from memory; retained memory/devices/licenses may not solve the deficit.
- **Gang time slicing:** shares CPU over time; memory footprint and synchronization overhead persist.
- **Elastic shrink:** avoids total disruption and fragmentation; only malleable frameworks can surrender resources safely.
- **Application-aware drain:** preserves state/effects and service; coordination increases start latency and complexity.
- **Lowest-priority-first:** transparent policy; may choose an expensive or infeasible collection of victims.
- **Minimum victim count:** reduces blast radius; one large victim may lose much more work.
- **Minimum disruption cost:** protects progress; estimation is uncertain and can repeatedly favor the same victim.
- **Youngest-first:** often reduces lost work; continually arriving jobs may never receive a protected run window.
- **Disruption-budget enforcement:** protects availability; can block urgent preemptors unless capacity or overrides exist.
- **Hard priority:** predictable ordering; priority inflation and starvation require governance.
- **Quota reclamation:** makes borrowing safe for owners; borrowers need clear contracts and checkpointability.

## Failure Modes and Misconceptions

- **“A higher number can preempt anything.”** Priority is scoped by authorization, quotas, guarantees, and hard safety rules.
- **“Eviction and preemption are identical.”** Preemption is one scheduling cause; node pressure, drain, update, and user deletion differ.
- **“Enough aggregate free resources means the job fits.”** Vectors, topology, devices, volumes, gangs, and fragmentation constrain placement.
- **“Allocated equals releasable.”** Suspended tasks, local storage, device contexts, licenses, and slow cleanup may retain resources.
- **“Selected victims mean the preemptor will start.”** Release, reservation, revalidation, and binding can still fail.
- **“The youngest task is always cheapest.”** It may hold vital shuffle, state, a leader role, or an expensive warm cache.
- **“Grace is always humane.”** Unbounded grace defeats urgent admission and can invite gaming; bounded, class-specific grace is needed.
- **“Checkpoint requested means checkpoint durable.”** Completion, consistency, checksum, publication, and recoverability must be verified.
- **“SIGTERM fences a workload.”** A partitioned or stuck process may continue; epochs fence publication and ownership.
- **“A disruption budget prevents every outage.”** It covers defined voluntary paths and observed status can lag; hard system safety needs more.
- **“One pod from every replica set is safe.”** concurrent failures, rollouts, topology, and quorum margins can correlate.
- **“Suspend frees the node.”** It often retains memory and other non-CPU resources.
- **“Requeue is free.”** queue delay, restore, input reread, cache warming, shuffle loss, and repeated effects all cost.
- **“Best effort may starve forever.”** If eventual progress is promised, debt, aging, or protected windows must enforce it.
- **“Preemption fixes under-capacity.”** Continuous urgent demand requires admission control or capacity, not endless victims.
- **“Rollback means deleting intents.”** In-flight notices, fences, victims, and reservations still require reconciliation.

## Worked Examples

### Example 1

A 32-GiB urgent task cannot run on a node with 16 GiB free. Killing four 4-GiB tasks there can fit it; killing one 32-GiB task on another node cannot. Victim selection must solve the deficit on a candidate placement, not improve a cluster-wide total.

### Example 2

A low-priority batch task finished a durable checkpoint 20 seconds ago and has no external effects. A peer of equal resource size has run 45 minutes since its checkpoint and owns needed shuffle output. Although both have the same priority/vector, the first has much lower recovery cost—unless repeated prior victimization raises its fairness debt enough to protect it.

### Example 3

A suspended training job releases CPU but retains 200 GiB memory and four GPU contexts. It cannot make room for a GPU preemptor needing those resources. Checkpoint-and-requeue or cancel can release them; suspend/resume is useful only when the deficit is CPU and memory residency is intentionally shared.

### Example 4

A replicated metadata service has five replicas, one already unavailable, and requires four healthy for its service floor. Preempting any healthy replica violates the floor even if a soft voluntary-disruption policy appears to permit one. The scheduler must wait for recovery, create a ready replacement, choose another workload, or invoke an explicitly authorized emergency rule.

### Example 5

A streaming operator receives notice, completes checkpoint 91, and is fenced at ownership epoch 14. Its replacement restores checkpoint 91 under epoch 15. The old process survives a network partition and tries to commit sink transaction 14; the sink rejects the stale epoch. Termination signaling alone would not protect the output.

### Example 6

A gang preemptor requires eight colocated accelerator slots. Evicting one slot on each of eight unrelated hosts leaves the gang blocked. The scheduler reserves a valid eight-slot topology first, selects victims inside that placement, and begins disruption only if the whole gang can bind after release.

### Example 7

A borrower uses 70 units while its nominal quota is 40 because an owner is idle. The owner later requests 25 units. Reclaiming 25 borrowed units restores the owner's promise without claiming the borrower behaved incorrectly. The lending contract must disclose notice, grace, checkpoint support, and whether repeated borrowing establishes no future entitlement.

### Example 8

A controller writes intent 8, sends notice, and crashes. On restart it sees the victim checkpointed but still running. Replaying intent 8 is idempotent: it verifies the checkpoint, fences the old generation, requests termination again, and awaits actual release. Creating intent 9 without reconciliation could double-count capacity or duplicate requeue.

### Example 9

Aggressive preemption starts a dashboard job 30 seconds sooner but kills 200 map attempts, overloads object storage with restart reads, and delays three other tenants by ten minutes. Preemptor latency improved; cluster policy failed. Evaluation must price victim and shared-system outcomes, not only the favored job.

### Example 10

This fixture enumerates eligible victim sets for one node and minimizes declared disruption cost after covering both CPU and memory deficits.

<!-- bijux-verify: {"id":"victim-set-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deficit=(4, 6)\nvictims=('batch-a', 'batch-b')\nreclaimed=(4, 6) cost=25\n","stderr":""}} -->
```python
from itertools import combinations

deficit = (4, 6)
victims = (
    ("batch-a", (2, 4), 20),
    ("batch-b", (2, 2), 5),
    ("batch-c", (4, 8), 40),
)

candidates = []
for size in range(1, len(victims) + 1):
    for group in combinations(victims, size):
        reclaimed = tuple(sum(item[1][i] for item in group) for i in range(2))
        if all(reclaimed[i] >= deficit[i] for i in range(2)):
            cost = sum(item[2] for item in group)
            candidates.append((cost, len(group), group, reclaimed))

cost, _, group, reclaimed = min(candidates)
print(f"deficit={deficit}")
print(f"victims={tuple(item[0] for item in group)}")
print(f"reclaimed={reclaimed} cost={cost}")
```

The result depends entirely on declared eligibility, vectors, costs, and one-node scope. A production solver also includes release time, uncertainty, topology, fairness, state, and correlated disruption.

## Cross-Program Connections

- **Operating systems:** signals, process termination, suspension, cgroups, memory/device release, and checkpoint/restore implement revocation locally.
- **Algorithms:** multidimensional covering, constrained optimization, approximate search, and online scheduling shape victim selection.
- **Distributed systems:** idempotent intents, epochs, leases, fencing, consensus-backed state, and reconciliation handle ambiguity/failure.
- **Data engineering:** shuffle lineage, state snapshots, replay, sinks, partition ownership, and DAG boundaries determine lost work.
- **Platform engineering:** priority classes, quotas, disruption APIs, node pressure, lifecycle hooks, and resource ledgers operationalize policy.
- **Reliability engineering:** quorum, failure domains, graceful degradation, fault injection, recovery load, and rollback bound blast radius.
- **Security/governance:** authorization, priority quotas, audit, tenant isolation, and transparent service classes prevent abusive eviction.
- **Economics:** reserved headroom, borrowed capacity, opportunity cost, lost resource-seconds, storage/network charges, and energy quantify trade-offs.

## References

1. Kubernetes. [Pod Priority and Preemption.](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/) Current priority classes, victim selection, graceful termination, disruption-budget interaction, and preemption limitations.
2. Kubernetes. [Disruptions.](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) Current voluntary/involuntary disruption distinctions, budgets, eviction behavior, and disruption conditions.
3. Kubernetes. [Node-Pressure Eviction.](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/) Current node-local pressure signals, eviction thresholds, victim ranking, and resource reclamation behavior.
4. Kubernetes. [Pod Lifecycle: Termination of Pods.](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) Current graceful termination, signals, endpoints, force deletion, and cleanup lifecycle.
5. Kueue. [Preemption.](https://kueue.sigs.k8s.io/docs/concepts/preemption/) Current workload-level priority, within-queue/cohort reclamation, borrowing, fair-sharing strategies, and target minimization.
6. Apache Hadoop. [Fair Scheduler.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html) Current minimum/fair-share preemption thresholds, timeouts, utilization gates, queues, and DRF context.
7. Apache Hadoop. [CapacityScheduler.](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html) Current capacity guarantees, queues, priorities, reservations, and proportional capacity preemption configuration.
8. SchedMD. [Slurm Workload Manager: Preemption.](https://slurm.schedmd.com/preempt.html) Current cancel, requeue, suspend/gang modes, grace, eligibility, ordering, and resource-release limitations.
9. Verma et al. [Large-Scale Cluster Management at Google with Borg.](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) Primary production cluster-management paper covering priority, quota, overcommitment, rescheduling, availability, and user impact.
10. Schwarzkopf et al. [Omega: Flexible, Scalable Schedulers for Large Compute Clusters.](https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/) Primary shared-state scheduler paper covering concurrent placement decisions, conflicts, and scalable policy evolution.
11. Hindman et al. [Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center.](https://www.usenix.org/conference/nsdi11/mesos-platform-fine-grained-resource-sharing-data-center) Primary two-level resource-sharing paper covering offers, revocation limitations, fairness, and framework behavior.
12. Dean and Ghemawat. [MapReduce: Simplified Data Processing on Large Clusters.](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) Primary task/attempt, intermediate-output, failure recovery, and backup-execution design.
13. Apache Flink. [Checkpoints.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints/) Current consistent checkpoint, retention, storage, recovery, and operational configuration for stateful dataflow.

## Exercises

### Exercise 1

Distinguish priority preemption, quota reclamation, node-pressure eviction, user cancellation, and hardware failure. State why the reason must remain durable.

### Exercise 2

A preemptor needs (8 CPU, 24 GiB). Node A has (4,8) free and victims $x=(4,8)$ cost 10 and $y=(2,16)$ cost 5. Node B has (0,24) free and victim $z=(8,0)$ cost 30. Which victim sets make the task fit, and which has lower declared cost?

### Exercise 3

Compare kill, requeue, suspend/resume, checkpoint/restart, and elastic shrink for a stateful job. Identify resources actually released and correctness prerequisites.

### Exercise 4

Design a recovery-safe preemption state machine for scheduler crash, lost notice, hung checkpoint, victim completion during grace, slow cleanup, preemptor cancellation, and late victim writes.

### Exercise 5

Design a production validation and rollout for a new preemption policy. Include authorization, placement, availability, state/effects, fairness, abuse, metrics, fault injection, canary, and rollback.

## Answers to the Exercises

### Answer 1

Priority preemption serves an authorized more-important pending workload. Quota reclamation returns borrowed capacity to its entitled owner. Node-pressure eviction protects a node from local exhaustion and may have no waiting preemptor. User cancellation expresses workload-owner intent. Hardware failure is involuntary loss, not a scheduling policy. The durable reason selects authorization, victim rules, grace, disruption-budget semantics, compensation/accounting, alerts, and SLO attribution; collapsing them hides abuse and prevents correct recovery.

### Answer 2

On A, the deficit is (4,16). Victim $x$ alone leaves memory short, and $y$ alone leaves CPU short; together they reclaim (6,24), cover the deficit, and cost 15. On B, the deficit is (8,0), so $z$ alone fits at cost 30. Both placements are feasible under the supplied scalar assumptions; A with $x,y$ has lower declared cost. Real selection also checks topology, vector dimensions beyond CPU/memory, release time, eligibility, state/service risk, fairness debt, and interaction cost.

### Answer 3

Kill releases all runtime-held resources quickly but loses volatile progress and requires fenced output/effect semantics. Requeue combines termination with a new attempt and needs idempotent identity, durable inputs/checkpoints, and bounded retry/debt. Suspend preserves memory state and usually releases CPU only; it may retain memory, accelerators, local disk, ports, and licenses. Checkpoint/restart releases resources after a consistent durable checkpoint and later restores state/input positions/sink transactions, paying I/O and delay. Elastic shrink releases selected workers/resources while the job remains live but requires a framework protocol for membership, repartitioning, state transfer, and collective recovery. Actual runtime confirmation, not the requested mode, determines the released vector.

### Answer 4

Persist one generation-scoped intent before notification. Make notice idempotent and record acknowledgement without assuming termination. During bounded grace, accept either a validated atomic checkpoint or ordinary completion; a hung checkpoint reaches a deadline and follows the declared fallback. Fence state/output ownership before replacement publication and require current epochs everywhere. Confirm process death, detach/cleanup, and ledger release before binding. On scheduler restart, replay incomplete monotone transitions. If the preemptor cancels, stop new disruption where reversible, release reservations, but still reconcile already-notified/fenced victims. Requeue with a new epoch and preserved debt/history. Reject late old-epoch writes. Quarantine ambiguous resources rather than double-allocate.

### Answer 5

Define and test priority/guarantee/reclamation authority, high-priority quotas, non-preemptible classes, and audit. Replay exact resource vectors, nodes, topology, devices, volumes, gangs, and queue state; prove each selected set can make its preemptor fit. Model quorum, replicas, disruption budgets, failure domains, checkpoints, shuffle, state restore, sinks, and epoch fencing. Test repeated victimization, borrowing, aging/debt, priority inflation, cross-tenant slowdown, and eventual-progress contracts. Inject controller/node loss, duplicate/lost notice, hung/corrupt checkpoint, storage pressure, slow termination, cleanup lag, victim completion, preemptor cancellation, stale writes, and restart storms. Measure decision/release/start latency, deadlines, actual resources, lost work, checkpoint/restore, recovery completion, availability, stale rejects, fairness, disruptions, congestion, cost, and energy. Shadow decisions, then canary explicitly safe workload classes with hard safety/rate gates. Keep versioned policy/configuration and a kill switch; rollback new decisions while reconciling every in-flight intent to a terminal state.
