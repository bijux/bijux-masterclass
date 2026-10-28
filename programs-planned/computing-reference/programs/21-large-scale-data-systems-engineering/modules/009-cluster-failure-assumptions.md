---
module_id: LSDS-009
program: Large-Scale Data Systems Engineering
level: 1
module_number: 9
title: Cluster Failure Assumptions
status: complete
last_verified: 2026-09-03
---

# Cluster Failure Assumptions

## One-Page Review

### Governing question

Which faults can a cluster data system experience, what evidence can distinguish them, which failures are correlated, what state survives, and under what capacity and timing assumptions can the workload recover correctly?

### Essential definitions

- A **fault** is a hypothesized cause; an **error** is an incorrect internal state; a **failure** is externally observable service deviation.
- A **failure model** states which component, timing, communication, storage, and adversarial behaviors a design considers.
- **Crash-stop** means a process stops and does not return under the same identity; **crash-recovery** permits it to restart with only declared durable state.
- An **omission fault** loses a send, receive, or operation; a **timing fault** completes too early, late, or unpredictably.
- A **network partition** preserves some communication paths while preventing others, so different components retain different views.
- A **gray failure** is partial, intermittent, asymmetric, or performance-degraded behavior that binary health checks represent poorly.
- A **failure domain** is a set of components exposed to one common cause, such as process, host, rack, zone, account, software version, or control plane.
- A **failure detector** emits suspicions from observations; timeout does not prove remote process death.
- **Recovery point objective (RPO)** bounds acceptable data loss; **recovery time objective (RTO)** bounds acceptable restoration time under stated scenarios.

### Central model, mechanism, or theorem

Record assumptions as `A=(unit, fault_modes, timing, detector, correlation_domains, surviving_state, redundancy, retry_scope, capacity_after_failure, RPO, RTO, evidence)`. A recovery claim is conditional on every relevant clause. Replicas improve availability only when their failure events and dependencies have the assumed correlation.

If three replicas independently fail with probability `q=0.1`, probability of at least one survivor is `1-q^3=0.999`. If all share a zone that fails with probability `z=0.02`, it becomes `(1-z)(1-q^3)=0.97902` under the toy model. Placement labels do not establish independence; common power, storage, network, identity, software, and operators can dominate.

### Critical invariants

- Component liveness, reachability, timeliness, correctness, and state durability are separate properties.
- Suspicion never grants two actors unfenced authority over one logical role or output.
- Replica placement matches the named common-cause domains in the objective.
- Recovery depends only on state proven to survive the modeled fault.
- Retried work remains idempotent, transactional, or attempt-fenced.
- The surviving cluster has enough capacity to restore and catch up without a retry cascade.
- Control-plane, data-plane, storage, dependency, and human failures are modeled together.
- RPO/RTO and availability numbers name scenarios, denominators, independence assumptions, and evidence.

### Common failures

Frequent failures are treating a missed heartbeat as proof of death, assuming failures are independent, counting replicas that share a host or zone, storing checkpoints in the same failure domain as workers, ignoring slow/partial failures, failing over without fencing, retrying deterministic faults, omitting control-plane or credential dependencies, restoring without catch-up capacity, and claiming availability from replica count alone.

### Compact example

A worker stops heartbeating while its shuffle files remain on local disk. It may be dead, paused, isolated, overloaded, or unable to reach the coordinator. The scheduler can suspect and replace it, but output commits need fencing because the old attempt may still run. If the host is lost, its local shuffle disappears; if only the control path is partitioned, destroying the local files can expand recovery unnecessarily.

### Connections

[LSDS-006](006-stages-tasks-and-dependencies.md) supplies task and attempt identity. [LSDS-007](007-narrow-and-wide-transformations.md) supplies recovery cones, and [LSDS-008](008-serialization-across-workers.md) supplies byte/state compatibility. [LSDS-010](../ROADMAP.md) integrates work, movement, and state under these assumptions.

## Governing Question

At cluster scale, some component is frequently slow, unreachable, restarting, out of space, corrupted, or being upgraded. “Machines fail” is too vague to design against. A worker process crash differs from host loss because local shuffle may survive one and not the other. A network partition differs from a crash because both sides may continue acting. A software bug or bad configuration can affect every replica simultaneously.

Every fault-tolerance mechanism embeds assumptions. Heartbeats assume useful timing behavior. Lineage assumes deterministic/repeatable inputs and code. Replication assumes failures are not perfectly correlated. Checkpoints assume their storage and metadata survive the target failure. Retry assumes the next attempt can succeed and repeated effects are safe. Failover assumes stale authority can be fenced.

The governing question is how to make those assumptions explicit, testable, and tied to workload consequences. For each scenario, identify the failed unit, observable evidence, ambiguity, common-cause boundary, lost and surviving state, authority transition, recomputation/replay, remaining capacity, and measurable restoration target. Then test the scenario rather than inferring safety from architecture diagrams.

## Why This Matters

Distributed data jobs amplify partial failures. One lost worker can remove shuffle blocks needed by hundreds of downstream tasks. One slow storage service can stall checkpoints across the cluster. One retry policy can multiply load until healthy workers fail. One incorrect coordinator failover can accept outputs from incompatible job generations.

Fault classification changes the response. A transient network omission may warrant bounded retry. A deterministic bad record will fail on every worker. An out-of-memory partition needs splitting or more resources. A corrupted artifact needs quarantine and regeneration from a trusted boundary. A credential expiration requires control-plane repair. Treating them all as “task failed” wastes capacity and can obscure the cause.

Correlation dominates availability. Replicas on different processes but one host do not survive host loss. Hosts in one rack can share power and top-of-rack networking. Zones can share a regional control plane, object store, identity system, software image, or operator action. Geographic replicas can still share a destructive schema migration. Failure domains are causal, not merely labels.

Recovery time includes detection, decision, provisioning, restore, replay, validation, and catch-up. A streaming system that restarts in five minutes but processes backlog slower than new input has not recovered steady-state service. A batch system that reconstructs shuffle at full production load may overwhelm storage or miss its deadline.

## Prerequisites and Retrieval

Recall from [LSDS-004](004-data-locality.md) that task placement depends on topology and exact data copies. Recall from [LSDS-006](006-stages-tasks-and-dependencies.md) that tasks, attempts, outputs, and stage generations are distinct. Recall from [LSDS-007](007-narrow-and-wide-transformations.md) how dependencies determine recovery cones, and from [LSDS-008](008-serialization-across-workers.md) that retained bytes require compatible decoders.

You should understand probability, conditional probability, finite state machines, heartbeats, leases, fencing, replication, checkpoints, idempotency, backpressure, capacity, percentiles, and service-level objectives. Retrieve the principle that absence of evidence is not evidence of absence in an asynchronous system.

## Learning Objectives

After completing this module, you should be able to:

- distinguish faults, errors, failures, symptoms, and root causes;
- specify crash-stop, crash-recovery, omission, timing, partition, corruption, and Byzantine scope;
- explain why timeout-based failure detectors provide suspicion rather than proof;
- identify process, host, rack, zone, region, dependency, version, and administrative domains;
- expose invalid independence assumptions in availability calculations;
- map each failure scenario to lost/surviving working, shuffle, checkpoint, source, and sink state;
- design fencing and attempt identity for ambiguous failover;
- classify deterministic, transient, resource, data, and dependency failures before retry;
- account for retry amplification, degraded capacity, restore traffic, and catch-up;
- define RPO, RTO, detection, restore, and steady-state recovery evidence;
- design fault injection and recovery drills with bounded blast radius; and
- specify high-consequence review beyond infrastructure availability.

## Core Exposition

### Fault, error, failure, and observation

A fault is a cause such as a bit flip, process defect, cable cut, expired credential, or operator command. It can create an internal error: corrupt memory, stale routing, or invalid state. A failure occurs when delivered behavior violates the service contract. An alert, exception, timeout, or metric is an observation, not automatically the cause.

The same observation has multiple explanations. A missing heartbeat can mean process death, host loss, network partition, CPU starvation, garbage-collection pause, coordinator overload, credential failure, or telemetry loss. The same cause can produce different symptoms depending on timing and redundancy.

Maintain causal humility in automation and incident response. Record event time, observer, path, generation, and uncertainty. Do not name “node failure” when the evidence says only “coordinator received no renewal before its deadline.” Subsequent cloud, network, process, and storage evidence may refine the diagnosis.

Correct response can precede certainty. A scheduler may launch a replacement when suspicion is high enough, while fencing both attempts from conflicting commits. Safety comes from authority/commit protocols; availability comes from timely suspicion and replacement. Conflating them makes timeout tuning carry impossible correctness responsibility.

### Component failure modes

**Crash-stop** models a process that halts permanently under its identity. It simplifies reasoning but omits restart and retained local state. **Crash-recovery** models a process that can return, retaining only explicitly durable state. Volatile memory vanishes; local disks may or may not survive depending on host and provisioning.

**Omission** includes lost messages, reads, writes, or acknowledgements. A sender may not know whether an acknowledged effect occurred if the response was lost. **Timing faults** include extreme delay, pauses, clock error, and deadline misses. An operation can eventually succeed after its caller has timed out and retried.

**Network partitions** create asymmetric knowledge. The worker may reach storage but not the coordinator; the coordinator may reach a replacement but not the old worker. Packets can be delayed, duplicated, reordered, or selectively lost. A clean all-links-down model misses real asymmetric routing and firewall changes.

**Corruption** can affect memory, transit, local disk, remote state, metadata, or computation. Detection requires checksums, validation, redundancy, provenance, or independent recomputation. If the same bad source or code feeds every replica, recomputation reproduces the error.

**Byzantine behavior** permits arbitrary or adversarial deviation. Most cluster data engines do not implement full Byzantine fault tolerance among workers; they rely on trusted software/administration plus authentication, isolation, validation, and audit. State exactly what hostile behaviors are excluded and which security controls remain.

### Gray and performance failures

A component can answer health checks while failing a subset of data, peers, disks, or requests. It can return stale data, corrupt one block, throttle one tenant, leak memory slowly, or exhibit extreme tail latency. These gray failures can last longer than clean crashes because automation sees ambiguous evidence.

Measure operation-specific success and latency, not only process presence. Compare paths and peers. A worker that reads local disk but cannot fetch remote shuffle is healthy for one action and failed for another. A storage endpoint that serves small metadata reads but stalls multipart writes needs capability-specific status.

Slow components consume resources. An attempt waiting on a slow fetch holds memory, connections, and a slot. Downstream retries add more requests. Health checks sharing saturated queues can fail and trigger removal, concentrating load on survivors. Performance degradation can become an availability failure through feedback.

Use deadlines, bounded queues, concurrency limits, load shedding, circuit breaking where appropriate, and retry budgets. These mechanisms must preserve dataflow correctness: abandoning a fetch cannot silently mark its target complete, and shedding a state update cannot be hidden as success.

### Failure detectors and timing assumptions

In a purely asynchronous model, message delay and process pause are unbounded, so an observer cannot distinguish a failed process from a very slow or partitioned one by silence alone. Practical systems add timing assumptions and failure detectors: heartbeats, leases, health probes, transport errors, and external infrastructure state.

A heartbeat interval, timeout, missed-count threshold, and observer path define detection behavior. Short timeouts reduce detection delay but increase false suspicion during pauses or congestion. Long timeouts reduce false positives while delaying recovery. One global timeout rarely fits task execution, control heartbeats, storage, and cross-region links.

Kubernetes uses Node status updates and Lease renewals as heartbeats; the control plane interprets missing observations and can mark a node `Unknown` before eviction. This exemplifies suspicion and policy delay, not mathematical proof that the host is dead.

Record detector completeness and accuracy expectations under measured timing distributions. Monitor late heartbeats, false removals, flapping, detector lag, and recovery started from suspicion. Test coordinator overload because the detector itself can fail or fall behind.

### Authority, epochs, and fencing

Ambiguous failure creates duplicate actors. An old coordinator can be partitioned from the quorum while a new leader takes over. An old task can continue after its lease expires while a speculative or retry attempt runs. Without fencing, both can publish results or mutate sinks.

Give authority a monotonically ordered epoch, lease token, or generation accepted by the protected resource. A writer presents its token on every commit; the resource rejects stale generations. Local belief that a lease expired is not enough if the sink cannot enforce ownership.

Task output uses job, graph, stage, partition, and attempt identity plus an accepted-winner protocol. Coordinator failover reconstructs authoritative accepted state before issuing new work. Late success messages and temporary files remain harmless because they cannot supersede the winner.

Clock-based leases require bounded clock/communication assumptions and conservative expiry. Consensus-backed epochs shift the dependency to quorum availability and durable log correctness. State the assumptions rather than calling either mechanism infallible.

### Failure domains and common causes

List physical domains: process, container, VM/host, disk, rack, power unit, network fabric, zone, region, and provider. List logical domains: binary version, configuration, schema, credentials, tenant quota, scheduler, control plane, storage service, DNS, identity, dependency, and operator procedure.

Replica placement protects only against domains it spans. Three processes on one host survive process crashes but not host loss. Three hosts in one zone may survive a host but not a zone or shared storage outage. Three regions can fail together under a global credential revocation or corrupt rollout.

Independence is a strong statistical assumption. Shared causes create correlated events and heavy tails. Even when zones are engineered separately, workload failover couples them: loss of one shifts compute, traffic, and restore load to others. Capacity correlation can produce cascade without simultaneous infrastructure loss.

Maintain a dependency/failure-domain inventory and verify placement from actual runtime topology. Anti-affinity is a scheduling intent; audit realized assignments and underlying mappings. Object storage or control services may advertise regional durability but need their own documented model and tested behavior.

### Probability and availability claims

For independent identical replica failure probability `q`, at least one of `n` replicas survives with probability `1-q^n`. A quorum of `k` survives by summing the binomial probabilities for at least `k` live replicas. These formulas are conditional on independence, identical probabilities, the time window, and all shared dependencies being available.

If a shared domain fails with probability `z` and conditional replica failures occur only when it survives, at-least-one availability becomes `(1-z)(1-q^n)` in the simplified model. The shared event dominates as `n` grows. More same-domain replicas approach `1-z`, not one.

Availability is not durability. A service can answer while returning stale/incomplete data; durable state can survive while computation is unavailable. Nor is component availability automatically job success: the job may require all partitions, a coordinator, schema registry, source, sink, and deadline.

Use probability models for design comparison, not as substitutes for incident data or failure tests. Document event definitions, observation window, conditional structure, repair, maintenance, and confidence. Real failure/repair processes are not necessarily stationary or independent.

### State survival matrix

Inventory state by layer: task memory, worker/executor memory, local disk, shuffle blocks, caches, coordinator metadata, distributed checkpoints, input logs/files, output candidates, committed sinks, schema/configuration, credentials, and audit records. For each fault scenario state whether it survives, is accessible, is authoritative, and is compatible.

Process crash can erase heap while leaving host-local files. Container rescheduling can lose ephemeral volumes. Host loss erases local state and every colocated attempt. Zone loss may remove workers plus a zonal storage endpoint. Coordinator loss can leave data blocks intact but lose unpersisted scheduling decisions.

Local recovery is an optimization, not durable truth, when the target fault includes host loss. Flink's current large-state guidance describes local snapshots as secondary while the distributed primary establishes checkpoint ground truth. This separation makes the assumption visible.

Checkpoint existence is insufficient. It needs a complete manifest, compatible code/schema/serializer, source positions still replayable, accessible encryption keys, and a sink protocol that preserves the promised semantics. Restore drills must test the entire set.

### Dataflow-specific recovery

For narrow lineage, a lost partition can often recompute from a bounded parent cone. For wide exchange, one lost producer's ephemeral blocks can affect many downstream targets. Durable shuffle narrows recomputation while adding storage dependencies. Record whether blocks survive process, executor, host, rack, and zone loss.

Batch recovery can retry one attempt, producer partition, stage region, or job. Stateful streaming usually restores a consistent operator/source state and replays input; sinks need transactional or idempotent behavior for end-to-end effects. Flink's fault-tolerance documentation explicitly conditions end-to-end exactly-once behavior on replayable sources and transactional or idempotent sinks.

Nondeterministic code, mutable external lookups, and changing input violate simple replay equivalence. Capture versions/snapshots or define reconciliation. A task that reads “current exchange rate” can produce a different result after retry even when its record bytes are identical.

Recovery must fence stale attempts and generations. Never assemble a result from incompatible shuffle stage attempts or checkpoints. Validate reconstructed output before publishing and retain causal events for repeated failure analysis.

### Retry classification and amplification

Classify before retry. Transient transport errors may succeed elsewhere or later. Worker/host loss warrants replacement and lineage recovery. OOM requires changed resources, partitioning, or code. Deterministic bad data/code should fail precisely or follow an explicit quarantine policy. Corruption requires trusted regeneration. Authorization failures require credentials/policy repair.

Retries consume capacity and can amplify an outage. If each failed request produces retries while capacity is already reduced, retry load delays original and recovery work. Identical synchronized backoff creates waves. Use bounded attempts, exponential backoff with jitter, budgets at task/stage/job/dependency levels, and admission/load shedding.

Speculation is a controlled duplicate, not universal fault tolerance. It helps random stragglers when spare capacity exists. It worsens deterministic skew, shared bottlenecks, and external side effects unless commit is fenced. Compare avoided tail time with duplicate CPU, input, shuffle, and sink pressure.

Stop conditions matter. Infinite retry can keep a permanently incompatible job “running” while consuming cluster capacity. Too-small budgets turn brief infrastructure events into failures. Escalate with the failure class, evidence, and last known compatible recovery point.

### Capacity after failure and catch-up

Redundancy without spare capacity can fail under load transfer. After losing fraction `f` of capacity, survivors receive more work plus restore, replay, checksum, and cache-warming traffic. If steady input rate exceeds post-failure processing rate, backlog grows.

For input rate `lambda` and recovery processing rate `mu`, catch-up requires `mu > lambda` after restoration. Clearing backlog `B` takes at least `B/(mu-lambda)` under a simple constant-rate model, excluding further failures and warm-up. A nominal restart time that omits catch-up understates RTO.

Reserve capacity or define degraded service, priority, backfill suspension, and admission policies. Keep restore traffic from starving live production. Rate-limit retries and data repair. Test cold caches, remote checkpoint bandwidth, schema/credential services, and scheduler provisioning at failure scale.

Cascades cross domains through automation. Removing slow workers concentrates load; autoscaling and restore pull images and state; clients retry; logs increase; health probes contend; another zone receives failover. Model the feedback loop, not only the initiating component loss.

### Recovery objectives and evidence

Define scenario-specific RPO and RTO. “Zone failure RTO 30 minutes” names the fault and timer start more usefully than “highly available.” Split RTO into detection, decision, provisioning, restore, validation, catch-up, and effect reconciliation. Define completion: accepting work, processing current input, or clearing backlog.

For batch jobs, objectives may be deadline completion and maximum repeated work rather than continuous availability. For streaming, define source lag, state consistency, sink effect semantics, and time to sustainable throughput. For interactive query, define success rate, latency, freshness, and degraded-result policy.

Evidence includes topology snapshots, state-survival matrices, detector distributions, failure injections, recovery traces, checkpoint restore drills, backlog curves, sink reconciliation, repeated trials, and post-incident records. Test from target scale and under realistic concurrent load.

Reliability claims need denominators and exclusions. Report job successes over eligible runs, partition/task failure and retry rates, data-loss/correction incidents, RPO/RTO attainment by scenario, and confidence/observation period. Avoid multiplying component percentages without a dependency model.

### Testing failure assumptions

Begin with tabletop review of the assumption register and dependency graph. Then test narrow reversible faults: kill a task process, pause a worker, sever one path, corrupt a test block, expire a test credential, fill a test disk, and delay storage. Expand to host/rack/zone simulations only with authorization and safeguards.

Each experiment declares hypothesis, blast radius, abort condition, observer, expected state loss, expected fencing, capacity threshold, and validation. Protect real users and data. Fault injection without invariant checking merely demonstrates that something happened.

Test ambiguity: partition rather than kill; pause beyond lease expiry then resume; deliver late successes; lose acknowledgement after an effect; restore from an older compatible checkpoint; make the failure detector or coordinator slow. These cases expose split authority and replay defects.

Re-run after topology, dependency, code, configuration, schema, capacity, or incident changes. Production incidents update the model. A passed worker-kill test does not validate region loss, corrupt rollout, or storage-control-plane outage.

## Definitions and Notation

Let failure assumption record be `A=(U,F,T,D,C,S,N,Q,K,RPO,RTO,E)`: component units `U`; permitted fault modes `F`; timing model `T`; detectors `D`; correlation domains `C`; surviving state `S`; redundancy placement `N`; retry/recovery scope `Q`; post-failure capacity `K`; recovery objectives; and evidence `E`.

For event `L_i` that replica `i` is unavailable in a stated interval, at-least-one availability is `P(not intersection_i L_i)`. Only under independence does this become `1-product_i P(L_i)`. For identical probability `q`, it reduces to `1-q^n`.

For `n=3` and quorum `k=2` under independent live probability `1-q`, quorum availability is `(1-q)^3 + 3(1-q)^2 q`. A common domain event `Z` with probability `z` multiplies conditional availability by `1-z` only in the simplified model where `Z` causes total loss and conditional replica failures behave as assumed.

Let detector at observer `o` emit `suspect_o(x,t)`. Suspicion is not identical to predicate `crashed(x,t)`. Safety mechanisms must tolerate false suspicion; liveness objectives bound detection and failover under stated timing conditions.

Let `S_f` be authoritative compatible state surviving fault `f`, and `W_f` the work required to restore missing state/results. A recovery plan is valid only if `S_f` suffices to reconstruct/continue the workload and post-failure resources can execute `W_f` within the objective.

For backlog `B`, arrival rate `lambda`, and sustainable recovery service rate `mu`, ideal catch-up time is `B/(mu-lambda)` only when `mu>lambda`. If `mu<=lambda`, backlog cannot clear under the stated constant rates.

## Mechanisms, Invariants, or Proof Structure

To make a recovery claim:

1. Name externally visible correctness and availability obligations.
2. Enumerate component, communication, timing, corruption, dependency, and adversarial fault modes.
3. Map physical and logical common-cause domains.
4. State detector evidence, ambiguity, timing assumptions, and false-suspicion behavior.
5. Inventory authoritative, local, ephemeral, durable, and external state survival.
6. Prove authority fencing, attempt isolation, and replay/effect safety.
7. Calculate redundancy only from justified conditional/correlation assumptions.
8. Verify post-failure restore, retry, and catch-up capacity.
9. Test each scenario with invariant checks and retained traces.
10. Review domain consequences and residual excluded faults.

The following executable toy model shows how one shared-zone event changes replica availability. It demonstrates arithmetic under declared assumptions, not a forecast for any real cluster.

<!-- bijux-verify: {"id":"correlated-failure-arithmetic","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"any_independent_workers=999/1000 decimal=0.999000\nany_shared_zone=48951/50000 decimal=0.979020\nany_independent_zones=124794621/125000000 decimal=0.998357\nquorum_independent_workers=243/250 decimal=0.972000\nquorum_shared_zone=11907/12500 decimal=0.952560\nindependence_overstatement=0.019980\n","stderr":""}} -->
```python
from fractions import Fraction

worker_failure = Fraction(1, 10)
zone_failure = Fraction(1, 50)

any_independent = 1 - worker_failure**3
quorum_independent = (
    (1 - worker_failure) ** 3
    + 3 * (1 - worker_failure) ** 2 * worker_failure
)
any_shared_zone = (1 - zone_failure) * any_independent
quorum_shared_zone = (1 - zone_failure) * quorum_independent

replica_failure_across_zones = (
    zone_failure + (1 - zone_failure) * worker_failure
)
any_independent_zones = 1 - replica_failure_across_zones**3

for name, value in (
    ("any_independent_workers", any_independent),
    ("any_shared_zone", any_shared_zone),
    ("any_independent_zones", any_independent_zones),
    ("quorum_independent_workers", quorum_independent),
    ("quorum_shared_zone", quorum_shared_zone),
):
    print(f"{name}={value} decimal={float(value):.6f}")

print(
    "independence_overstatement="
    f"{float(any_independent - any_shared_zone):.6f}"
)
```

The same-zone at-least-one probability is 0.97902 rather than 0.999 because the two-percent shared event bypasses all three replicas. Treating the worker failures as wholly independent overstates this toy availability by 0.01998, or 1.998 percentage points. Independent zones in the third line are also an assumption, not a property established by their names.

The model omits repair, duration, maintenance, load transfer, shared software/storage/control planes, and uncertainty. Real evidence needs a conditional failure/dependency model, observed or justified parameters, and scenario tests. More decimal places do not compensate for invalid assumptions.

Safety proof asks whether false suspicion, delayed messages, resumed old actors, and duplicate attempts can violate output/state invariants. Liveness proof asks whether a real failure is eventually suspected, replacement can obtain resources, state can be restored, and backlog can clear. Availability measurement asks whether the user-visible objective held. Do not collapse these obligations.

## Alternatives and Trade-Offs

Fast failure detection reduces idle time but increases false positives and duplicate recovery. Conservative detection reduces churn but delays failover. Adaptive detectors can follow latency distributions but add complexity and still require fencing.

Lineage recomputation minimizes steady-state replication for deterministic batch work but increases recovery time and dependency load. Durable shuffle reduces recomputation at storage/operational cost. Frequent checkpoints reduce replay/RPO but consume I/O, coordination, and storage. Local checkpoint copies accelerate likely same-host recovery but do not replace independent durable state.

Active replication reduces failover time and can serve reads, while increasing cost, coordination, and correlated software exposure. Warm standby lowers cost but needs tested provisioning and state lag. Cold restore is cheapest in steady state and slowest/most dependency-heavy during recovery.

Spreading across domains improves common-cause tolerance but increases network distance, transfer cost, consistency latency, and operational complexity. Cross-region designs need explicit data sovereignty, identity, key, dependency, and capacity assumptions. Blind anti-affinity can worsen locality and cost.

Retrying narrowly saves completed work, but reconstructing many scattered shuffle blocks can cost more than restarting a compact stage. Whole-region restart provides a clean consistent boundary while repeating more work. Choose from state survival, dependency shape, side effects, corruption scope, and capacity.

Fail-open behavior can preserve availability while violating correctness, privacy, or safety. Fail-closed protects some invariants while denying service. Degraded modes must name what is omitted, who is affected, and which consequences are acceptable; infrastructure cannot decide domain policy alone.

Probabilistic models enable comparison but can create false precision. Scenario-based objectives are concrete but do not aggregate every combination. Use both: assumptions and math for design, drills and incidents for evidence, and explicit residual risk for excluded cases.

## Failure Modes and Misconceptions

1. **A timeout proves a crash.** It proves only that an observation missed a deadline.
2. **A process is either healthy or dead.** Partial, slow, and asymmetric behavior is common.
3. **Restart preserves local state.** Survival depends on process, container, host, and volume lifecycle.
4. **Three replicas mean three failure domains.** They may share host, rack, zone, software, or services.
5. **Different zones are independent.** Regional control, identity, storage, software, and load can correlate them.
6. **Anti-affinity proves placement.** Verify realized and underlying topology.
7. **Replica availability equals data durability.** Serving and preserving correct data are different objectives.
8. **Component availability multiplies directly.** Dependencies and conditional correlation determine composition.
9. **More replicas eliminate a shared-domain event.** Same-domain replication approaches the shared-domain ceiling.
10. **A checkpoint file proves recoverability.** Completeness, metadata, code, schemas, keys, sources, and sinks matter.
11. **Local checkpoint state is durable truth.** Host loss can remove it.
12. **Lineage always reproduces output.** Nondeterminism and mutable dependencies can change results.
13. **A successful retry proves a transient fault.** It may mask corruption or nondeterminism.
14. **Every failure deserves retry.** Deterministic and authorization failures need different remedies.
15. **Infinite retry improves availability.** It can exhaust capacity and hide terminal failure.
16. **Speculation fixes every straggler.** It duplicates deterministic skew and shared bottlenecks.
17. **Failover is safe after lease expiry.** The protected resource must fence stale authority.
18. **Control-plane loss leaves data jobs unaffected.** Scheduling, schemas, keys, and coordination may stop.
19. **Storage replication covers application errors.** Replicas can preserve corrupt or deleted data faithfully.
20. **Restart time equals RTO.** Restore, validation, replay, reconciliation, and catch-up follow.
21. **Survivors can absorb failed capacity.** Restore and retry traffic can overload them.
22. **Running means recovered.** Lag can continue growing when processing stays below arrival rate.
23. **A worker-kill test validates disaster recovery.** It covers one narrow scenario.
24. **Fault injection alone validates safety.** Invariants and outcomes must be checked.
25. **Infrastructure recovery proves domain safety.** Domain effects require independent review.

## Worked Examples

### Example 1

**Question:** A worker misses three heartbeats. What is known?

**Reasoning:** Only that renewals were not observed through that path before deadlines. Death, pause, partition, overload, and detector failure remain possible.

**Conclusion:** Suspect and recover with fencing; do not treat silence as proof.

### Example 2

**Question:** Three executors run on one host. Which failure do they tolerate?

**Reasoning:** Independent process crashes may leave others, but host, local-disk, kernel, power, and many network failures remove all three.

**Conclusion:** Count failure domains, not processes.

### Example 3

**Question:** Why can an old task commit after its timeout?

**Reasoning:** It may have been paused or partitioned and later resume. Timeout does not stop its CPU or revoke sink authority.

**Conclusion:** Attempt/generation fencing belongs at commit.

### Example 4

**Question:** A task fails with the same parse error on four hosts. Continue retrying?

**Reasoning:** The evidence suggests deterministic code/data failure; unchanged placement cannot help.

**Conclusion:** Stop, identify the record/schema/code, and apply explicit correction or quarantine policy.

### Example 5

**Question:** Does a remote checkpoint guarantee stream recovery?

**Reasoning:** Only if its manifest/state are complete and compatible, source history is replayable, keys/dependencies are accessible, and sink semantics can reconcile replay.

**Conclusion:** Restore is an end-to-end contract.

### Example 6

**Question:** A region loses 40% of workers; survivors had 20% spare capacity. What risk follows?

**Reasoning:** Remaining demand plus restore/retry traffic exceeds spare capacity unless work is shed, delayed, or added elsewhere.

**Conclusion:** Replica placement without degraded-capacity planning can cascade.

### Example 7

**Question:** Input arrives at 100 MB/s and restored processing sustains 95 MB/s. Will backlog clear?

**Reasoning:** No; `mu<=lambda`, so lag grows even after tasks restart.

**Conclusion:** Recovery requires sustainable catch-up capacity.

### Example 8

**Question:** Why is corruption different from block loss?

**Reasoning:** Loss is visible absence; corruption may appear valid and propagate. Regeneration must begin from a trusted validated ancestor, not copy the damaged block.

**Conclusion:** Detection and trusted provenance are recovery prerequisites.

### Example 9

**Question:** What does a successful zone drill establish?

**Reasoning:** It supports the exact topology, load, dependencies, fault injection, objectives, and invariants observed in that trial. It does not prove independence or every regional fault.

**Conclusion:** Scope evidence to scenario and conditions.

### Example 10

**Question:** Can a 30-minute infrastructure RTO approve recovery of emergency dispatch analytics?

**Reasoning:** No. Dispatch continuity, data freshness, location/identity accuracy, degraded manual operation, duplicate/missed alerts, prioritization, accessibility, privacy/security, regional coordination, and life-safety consequences require named dispatch, emergency-management, field-operations, public-safety, accessibility, privacy/security, data-governance, resilience, and independent safety review. No external approval is claimed here.

**Conclusion:** Technical restoration time is only one life-safety obligation.

## Cross-Program Connections

[Operating Systems](../../22-operating-systems/ROADMAP.md) supplies process crash, storage, resource exhaustion, clocks, and isolation. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies partitions, packet loss, routing, congestion, and failure detection paths. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies malicious faults, identity, key failure, compromise, and incident response.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns formal failure models, consensus, leases, fencing, replication, consistency, and recovery semantics. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns node lifecycle, placement, health, provisioning, quotas, and control planes. This program owns how those mechanisms affect dataflow partitions, shuffle, state, checkpoints, and job completion.

[Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline failure handling, backfills, source/sink contracts, and operational objectives. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns authoritative data, lineage, retention, and recovery governance. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns hazards, assurance cases, common-cause analysis, and system-level validation.

MapReduce and RDDs demonstrate task retry and lineage under worker loss. Flink documents checkpoint/source/sink conditions and local-versus-primary state. Kubernetes documents heartbeat/Lease observations and node-state policy. Failure-detector theory separates suspicion from truth under asynchronous communication. Borg and DieHard address placement and correlated failure; Google SRE documents overload and retry cascades.

## References

- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI, 2004. Primary worker/master failure, task reexecution, locality, output, and backup-task design.
- Matei Zaharia et al., [*Resilient Distributed Datasets*](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf), NSDI, 2012. Primary lineage, partition reconstruction, and node-failure recovery design.
- Tushar Deepak Chandra and Sam Toueg, [*Unreliable Failure Detectors for Reliable Distributed Systems*](https://www.cs.toronto.edu/~christoff/files/UnreliableFailureDetectorsForReliableDistributedSystems.pdf), JACM, 1996. Primary failure-detector completeness/accuracy model.
- Abhishek Verma et al., [*Large-Scale Cluster Management at Google with Borg*](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/), EuroSys, 2015. Primary cluster scheduling, availability, placement, and correlated-failure context.
- Mohammad T. Islam et al., [*DieHard: Reliable Scheduling to Survive Correlated Failures in Cloud Data Centers*](https://research.google/pubs/diehard-reliable-scheduling-to-survive-correlated-failures-in-cloud-data-centers/), SC, 2018. Primary correlated-failure and job-reliability model.
- Apache Flink Project, [*Fault Tolerance via State Snapshots*](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/), checked 2026-09-03. Official current checkpoint, replayable-source, and transactional/idempotent-sink conditions.
- Apache Flink Project, [*Tuning Checkpoints and Large State*](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/), checked 2026-09-03. Official current primary distributed and secondary local state recovery behavior.
- Kubernetes Project, [*Nodes*](https://kubernetes.io/docs/concepts/architecture/nodes/#node-heartbeats), checked 2026-09-03. Official current heartbeat, Node condition, controller, and eviction behavior.
- Kubernetes Project, [*Leases*](https://kubernetes.io/docs/concepts/architecture/leases/), checked 2026-09-03. Official current heartbeat and leader-election Lease usage.
- Mike Ulrich, [*Addressing Cascading Failures*](https://sre.google/sre-book/addressing-cascading-failures/), Google SRE Book. Official overload, retry amplification, health-check, capacity, and failure-testing guidance.

## Exercises

### Exercise 1

Write an assumption record for executor process crash, host loss, and zone network isolation. Include observation, ambiguity, state survival, authority, recovery, capacity, and evidence.

### Exercise 2

Three replicas each have independent conditional failure probability 0.05, but all share a rack with failure probability 0.01. Calculate simplified at-least-one availability and compare it with the erroneous wholly independent result.

### Exercise 3

A stream restores in 8 minutes with 960 GB of backlog. New input arrives at 2 GB/min and post-restore processing is 6 GB/min. Estimate ideal catch-up time and total time to current, then list omitted factors.

### Exercise 4

Diagnose repeated task timeouts where CPU, network, and storage dashboards look normal, but one binary version appears on every affected worker and retries move to workers with the same version.

### Exercise 5

A regional public-benefits computation must recover after zone loss without duplicate or missing decisions. Specify failure model, state, fencing, capacity, tests, objectives, and named review.

## Answers to the Exercises

### Answer 1

For process crash, observe process/transport exit plus missed heartbeats while allowing pause/path ambiguity; heap is lost, host-local shuffle may survive, and a fenced attempt can retry on the same/other executor. For host loss, observe infrastructure state plus all colocated paths failing; heap, ephemeral volumes, local shuffle, and local checkpoint copies are lost, so recover from remote inputs/shuffle/checkpoints. For zone isolation, each side may remain live; fence coordinator/output authority through a surviving quorum, stop or isolate ambiguous actors, use state outside the zone, provision verified capacity elsewhere, and control replay/retry load. For each, name graph/checkpoint/sink generations, RPO/RTO/catch-up, detector distributions, placement evidence, injection/abort conditions, output reconciliation, and repeated trace results.

### Answer 2

Wholly independent at-least-one availability is `1-0.05^3=0.999875`. With a one-percent shared rack event and conditional independent replica loss otherwise, it is `0.99*(1-0.05^3)=0.98987625`. The erroneous model overstates availability by `0.00999875`, nearly one percentage point. This arithmetic remains conditional on the toy event definitions, interval, independence after rack survival, and all other dependencies.

### Answer 3

Net catch-up rate is `6-2=4 GB/min`, so ideal backlog clearance is `960/4=240 minutes`. Adding the eight-minute restore gives about 248 minutes to current processing under constant rates. The model omits detection and decision time if not included, provisioning, validation, cache warm-up, checkpoint reads competing with live input, variable/compressed units, retries, sink throughput, rate changes, additional failures, and safety margin. The workload is not caught up merely because tasks restarted at minute eight.

### Answer 4

The version correlation suggests a deterministic software regression or configuration bundled with that version, not random worker failure. Compare unaffected versions on the same data/partitions, inspect rollout and exception/stack/progress traces, and reproduce with a bounded record/workload. Stop retrying onto identical code, halt/canary-reverse the rollout under change policy, preserve evidence, and fence incompatible outputs. Validate rollback compatibility for shuffle/checkpoint/schema state, then test the corrected version. Normal aggregate resources do not exclude a version-specific deadlock, parser loop, protocol mismatch, or data-dependent fault.

### Answer 5

Model process/host/zone loss, asymmetric partition, slow dependencies, corrupt state, coordinator ambiguity, storage/identity outage, bad rollout, and operator error. Place authoritative checkpoints, input snapshots/logs, schemas, keys, and commit metadata outside the target domain; version computation/rules/inputs; fence coordinator, task attempts, and decision publication; use idempotent decision/effect identities and correction/appeal lineage. Reserve remote restore plus catch-up capacity and define zone-loss RPO, detection, restoration, backlog, decision-publication, and reconciliation targets. Test late old actors, mixed generations, partial/corrupt checkpoints, source replay, sink acknowledgement loss, skew, capacity loss, dependency outage, rollback, and manual degraded operation. Named reviewers include benefits-policy/legal owners, caseworkers and appeals specialists, identity/data-quality governance, accessibility/language access, privacy/civil-rights and security experts, distributed-data/platform resilience, operations/disaster recovery, affected-community representation, and independent fairness/safety assurance. Internal availability tests do not constitute external approval.
