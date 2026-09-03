---
module_id: LSDS-059
program: Large-Scale Data Systems Engineering
level: 2
module_number: 59
title: Autoscaling Data Clusters
status: complete
last_verified: 2026-09-04
---

# Autoscaling Data Clusters

## One-Page Review

### Governing question

How should a data platform change workload, node, and storage capacity as demand changes while preserving latency, throughput, state, placement, fairness, cost, and recovery invariants across several delayed feedback loops?

### Essential definitions

- **horizontal workload scaling** changes the number of replicas, executors, tasks, or parallel subtasks.
- **vertical scaling** changes CPU, memory, or another resource assigned to one unit of work.
- **node autoscaling** adds or removes machines or capacity classes to satisfy schedulable workload requests.
- **desired capacity** is a controller's policy target; **requested**, **provisioned**, **ready**, and **effective capacity** are distinct later states.
- **backlog** is admitted work not yet completed; **lag** is a domain-specific distance from the desired processing frontier.
- **deadband** is a metric interval in which the controller intentionally makes no change.
- **stabilization window** selects or delays recommendations over recent history to suppress oscillation.
- **cooldown** prevents another action until an actuation has had time to become observable.
- **headroom** is deliberately unused capacity reserved for uncertainty, bursts, failures, or recovery.
- **consolidation** removes or replaces nodes after proving their work can move without violating declared constraints.

### Central model, mechanism, or theorem

For backlog $B$, arrival rate $\lambda$, useful service rate $\mu$ per ready replica, and target drain horizon $H$, a simple target is

$$n^*=\left\lceil\frac{\lambda+B/H}{\mu}\right\rceil.$$

The formula is only a demand estimate. A safe controller filters and timestamps observations, checks metric validity, applies bounds, headroom, deadbands, rate limits, and asymmetric stabilization, then records a desired target. Separate reconcilers turn that target into requested workload units, schedulable resource requests, nodes, ready units, and effective service. Each transition has delay and failure modes. Correct autoscaling therefore requires explicit state, idempotent actions, coordination among horizontal, vertical, node, storage, and dependency loops, plus conservative scale-down for stateful work.

### Critical invariants

- Every decision identifies metric event time, freshness, source, policy generation, and workload generation.
- Desired, requested, provisioned, scheduled, ready, healthy, and effective capacity are never treated as synonyms.
- Scale-out does not admit more work than downstream services, storage, network, quotas, or control planes can safely support.
- Scale-in proves state, shuffle, local data, quorum, disruption, topology, and availability constraints before removal.
- Retries and replay do not double-apply a resize, lose a prior target, or reset stabilization history silently.
- Horizontal and vertical controllers do not compete over the same utilization signal without a coordination rule.
- Node scale-out follows unschedulable resource requests and placement constraints, not host utilization alone.
- Tenant guarantees, maxima, priorities, and cost attribution remain enforced while capacity changes.
- Missing, delayed, reset, or contradictory metrics lead to a declared safe mode rather than arbitrary shrinkage.
- Every controller has bounded authority, a disable/freeze path, and reconciliation after restart or rollback.

### Common failures

Common failures include scaling an I/O-bound stream from CPU alone; reacting to retries as new demand; ignoring warmup and observing an action twice; using average memory for an OOM-sensitive process; requesting a vertical size no node can host; adding replicas while a database is already saturated; scaling nodes from utilization rather than pending requests; removing nodes that hold shuffle or local state; treating provisioned executors as productive; scaling to zero without an external durable trigger; allowing HPA, VPA, framework, and node controllers to chase one another; forgetting cloud quota or topology scarcity; and celebrating lower cost while backlog age, recovery time, or tenant fairness regresses.

### Compact example

A stream has 12,000 queued records, receives 300 records/s, and each ready replica sustainably processes 100 records/s. To drain existing backlog in 60 seconds while keeping up with arrivals, it needs 500 records/s, or five replicas. That answer assumes homogeneous replicas, stable rates, no startup delay, and sufficient downstream and node capacity. Production policy must add measured uncertainty and actuation constraints.

### Connections

[LSDS-051](051-cluster-resource-models.md) defines capacity vectors, [LSDS-052](052-static-and-dynamic-allocation.md) separates reservation from utilization, [LSDS-053](053-fair-and-capacity-scheduling.md) constrains tenant allocation, [LSDS-054](054-data-local-task-placement.md) supplies placement feasibility, [LSDS-056](056-preemption.md) governs disruptive reclamation, [LSDS-057](057-memory-cpu-and-i-o-isolation.md) defines resource enforcement, and [LSDS-058](058-multi-tenant-queueing.md) preserves queue guarantees while demand changes.

## Governing Question

Data-cluster demand changes at many time scales. An interactive query burst may last seconds, a scheduled pipeline may create an hour-long wave, a streaming partition change may persist for weeks, and seasonal growth may require a new storage topology. Scaling can change application replicas, framework executors, task parallelism, CPU or memory per replica, worker nodes, storage servers, control-plane capacity, or a dependent service. These are different actuators with different constraints and delays.

An autoscaler closes a feedback loop: observe, estimate, decide, request, actuate, and observe again. The loop is distributed. Metrics arrive late, provisioning may fail, a new node may take minutes to boot, an executor may be ready before its cache is warm, and a stateful operator may restart to redistribute state. Meanwhile another controller changes requests or removes nodes. A locally sensible action can become globally destabilizing.

The governing question is how to choose signals, model useful service, coordinate layers, bound action, protect state and tenants, diagnose blocked capacity, and validate that automatic changes improve system objectives rather than merely moving queues or cost.

## Why This Matters

Static peak capacity is simple but expensive, and it may still fail when peak assumptions are wrong. Manual scaling is slow and inconsistent. Unbounded automatic scaling can turn measurement noise into resource churn, amplify a dependency outage, or destroy recoverable state during scale-in. Data systems are particularly sensitive because their capacity is not fungible: partitions, caches, shuffle files, checkpoints, storage locality, quorum, network paths, and skew determine what added resources can actually do.

Autoscaling also changes reliability and organizational policy. A tenant that can create arbitrary pending requests can induce expensive node growth. A workload that understates requests may appear efficient until eviction or OOM. Scale-down can consume disruption budgets needed for incident response. Spot capacity may make a burst cheap but increase replay and deadline risk. The controller therefore implements economic, fairness, and risk decisions, not just arithmetic.

The correct objective is not maximum utilization. It is to meet declared latency, throughput, freshness, deadline, recovery, and fairness objectives at acceptable cost and risk. That requires observing the entire causal path from demand through ready capacity to completed useful work.

## Prerequisites and Retrieval

Review resource vectors and fragmentation in [LSDS-051](051-cluster-resource-models.md), static/dynamic allocation in [LSDS-052](052-static-and-dynamic-allocation.md), scheduling and queueing in [LSDS-053](053-fair-and-capacity-scheduling.md) and [LSDS-058](058-multi-tenant-queueing.md), state-aware placement in [LSDS-054](054-data-local-task-placement.md), preemption in [LSDS-056](056-preemption.md), and runtime isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md).

You should understand feedback, rates and queues, percentiles, CPU/memory requests and limits, pods/executors/tasks, checkpoints, shuffle, graceful termination, topology constraints, quotas, control-plane reconciliation, idempotence, and service-level objectives.

## Learning Objectives

After this module, you should be able to:

1. distinguish horizontal, vertical, node, storage, and control-plane scaling;
2. map desired, requested, provisioned, ready, and effective capacity as separate states;
3. derive backlog- and service-rate-based targets with explicit assumptions;
4. choose signals for batch, streaming, query, and stateful workloads;
5. stabilize delayed feedback with deadbands, windows, cooldowns, and rate bounds;
6. coordinate workload rightsizing, replica scaling, node provisioning, and consolidation;
7. preserve checkpoints, shuffle, locality, quorum, and disruption constraints during scale-in;
8. handle missing metrics, scale-to-zero, quota exhaustion, and dependency saturation safely;
9. instrument autoscaling decisions for causal diagnosis, fairness, and cost attribution; and
10. validate policies through trace replay, fault injection, canarying, and rollback.

## Core Exposition

### Define the objective before the actuator

Start with workload outcomes: queue age, completion deadline, query latency, stream freshness, recovery time, and tenant guarantees. Add cost, energy, and disruption budgets. A utilization target is an intermediate control choice, not a business objective. Ninety-percent CPU may be excellent for batch throughput and disastrous for a latency-sensitive service.

State scope and time horizon. An interactive service may optimize seconds-to-minutes response, a batch fleet hourly deadline attainment, and storage quarterly growth. One controller should not blend incomparable objectives into an unexplained score.

### Separate scaling layers

Horizontal workload scaling changes count or parallelism. It works when work can partition and each added unit can contribute. Vertical scaling changes a unit's resource requests or limits and may require restart or rescheduling. Node scaling changes the substrate from which workload requests are placed. Storage scaling changes capacity, throughput, shard or replica layout, usually with data movement. Control-plane scaling protects schedulers, metadata stores, gateways, and operators.

Draw ownership and interfaces between controllers. The workload controller publishes desired replicas or resource requirements. The scheduler exposes why requests are pending. The node controller provisions a matching capacity class. Readiness gates expose when capacity is usable. A framework may then redistribute partitions or stages.

### Model the capacity state machine

For every unit, distinguish desired, API-requested, accepted, provisioned, registered, scheduled, ready, healthy, and effectively serving. A node can be running in the provider yet unavailable to the scheduler. A pod can be ready while a cache or state transfer is incomplete. An executor can exist while a stage lacks divisible work.

Record transition timestamps and reason-coded failures. Capacity debt is the gap between desired and effective capacity over time. Without this state machine, dashboards attribute provisioning delay, placement failure, and warmup delay to the wrong controller.

### Choose signals that represent useful pressure

CPU is helpful when CPU is the dominant bottleneck and requests reflect need. It is weak for I/O-bound consumers, blocked queries, memory pressure, and work throttled by a dependency. A good signal connects demand to useful completion: input and processing rates, durable queue length and age, consumer lag, busy time, runnable tasks, remaining work, query concurrency, or deadline slack.

Use several signals only with an explicit rule. A conservative scale-out may take the maximum target from CPU and backlog, while scale-in requires all signals to agree. Normalize units and sampling windows. Do not average gauges across inactive instances or sum cumulative counters without rates and reset handling.

### Estimate service capacity

Let arrival rate be $\lambda$, ready-replica useful service be $\mu$, backlog be $B$, and desired drain horizon be $H$. The target $\lceil(\lambda+B/H)/\mu\rceil$ says capacity must both keep up and retire accumulated work. Estimate $\mu$ from comparable workload, data shape, resource size, locality, and dependency conditions. A mean across skewed partitions is misleading.

Add safety headroom for forecast error and failures, then clamp to policy minimum and maximum. If service rate falls as replicas increase because a database or network saturates, a linear model is invalid. Learn a capacity curve or stop scale-out at the safe dependency envelope.

### Scale batch work from work remaining

Batch pressure is not merely pending-task count. Consider critical-path work remaining, stage parallelism, task duration distribution, data locality, startup time, deadline, and maximum useful parallelism. Adding executors beyond available tasks or a serial stage only adds cost. Skewed stragglers may require repartitioning or speculation rather than a larger fleet.

For a deadline, compute the service rate needed to finish remaining work with recovery margin. Reject or renegotiate infeasible deadlines instead of requesting unbounded nodes. Scheduled pre-scaling can reduce startup delay when arrivals are predictable, but actual metrics must correct forecast errors.

### Scale streaming work from rates and lag

Streaming systems expose input rate, processing rate, busy time, watermark or offset lag, checkpoint duration, backpressure, and partition parallelism. Lag alone can grow because a source is unavailable or timestamps changed; CPU alone can be low while operators wait on I/O. Combine rate and backlog semantics with source validity.

Parallelism changes may redistribute keyed state and restart operators. The benefit of more capacity must exceed checkpoint, transfer, and warmup cost. Cap target parallelism by partition/key-group divisibility and downstream capacity. Protect checkpoint health before initiating another rescale.

### Scale query services from concurrency and latency

Interactive query fleets should observe queue age, admitted concurrency, latency percentiles by class, cancellation, memory spills, and backend saturation. Average CPU hides queued work and tail latency. Separate admission from execution so autoscaling does not convert overload into a larger uncontrolled fan-out.

Keep a warm minimum when cold start violates the latency objective. For heterogeneous queries, use class-specific cost estimates and concurrency limits. Scaling coordinators and workers may require different policies because coordinator state and metadata load are not proportional to scan capacity.

### Treat memory vertically and conservatively

Memory is a stock, not a continuously consumed rate like CPU time. Average memory can hide rare heap peaks, native allocations, buffers, cache, state, and OOM kills. Use distributions and workload phases, distinguish working set from reclaimable cache, and retain failure margin.

Vertical changes may restart a workload, alter packing, or create an unschedulable request larger than every node. Validate proposed sizes against node classes, quotas, limits, checkpoint/restart cost, and horizontal policy. If horizontal scaling uses CPU utilization while vertical scaling changes CPU requests, the loops share a denominator and need a coordination rule or separate signals.

### Coordinate horizontal and node autoscaling

Horizontal scaling creates or removes schedulable requests. Node autoscaling should examine unschedulable requests and their placement constraints, then decide whether an available node class would make them placeable. Low node utilization alone is not evidence that a particular pending pod can fit.

Include DaemonSet and system overhead, zones, accelerators, volumes, architecture, labels, taints, affinity, and maximum node size. Report when quota, provider capacity, incompatible topology, or invalid requests block provisioning. Do not let a workload controller repeatedly raise desire when the substrate has declared a hard ceiling.

### Account for provisioning and warmup delay

Measurement, decision, API propagation, provider allocation, image pull, scheduling, initialization, registration, cache fill, state transfer, and readiness all add delay. Size stabilization and cooldown against the end-to-end loop, not merely controller execution time. Otherwise the controller sees unchanged pressure and repeats a request whose effect is still in flight.

Track outstanding desired capacity and age. Apply anti-windup: when actuation is saturated by maximum size or quota, do not accumulate an ever-growing hidden command. Surface unmet demand and degrade admission or SLOs explicitly.

### Stabilize the feedback loop

Filter noise without erasing bursts. A deadband avoids changing capacity for small errors. A scale-up stabilization policy may act promptly on credible high demand; scale-down commonly chooses a conservative recommendation across a longer window. Rate limits bound replicas or percentage changed per interval. Cooldown prevents judging an unfinished action.

Use asymmetric policy because shortage and surplus have different costs. Still bound scale-up to protect dependencies and budgets. Define behavior for counter resets, clock skew, sparse samples, newly ready units, and workloads terminating during a decision.

### Handle missing and stale metrics

Every sample needs event time, collection time, freshness limit, source health, and workload-generation identity. Missing is not zero. A stale low value must not trigger scale-in, and a stale high value must not cause limitless growth. Reject mixed generations after a rollout when their performance profiles differ.

Choose a safe mode per workload: hold current size, allow bounded scale-out from durable backlog, freeze scale-in, or fall back to a static minimum. Alert on the loss of decision evidence. Recovery should rebuild history deliberately rather than treating an empty window as calm demand.

### Design scale-to-zero as a separate mode

A workload at zero replicas cannot emit an internal utilization metric. It needs a durable external activation signal such as a queue, event source, or scheduler-owned pending-work record. The trigger must survive restarts and deduplicate activation. Polling interval and cold-start path become part of the SLO.

Keep a nonzero minimum for services with tight latency, fragile initialization, leader election, or no durable trigger. Scale-to-zero must not delete state, lose ownership leases, or make the metric source depend on the absent consumer.

### Preserve state during workload rescaling

Before reducing stateful parallelism, establish where state lives, how it is checkpointed, and how ownership transfers. Require a recent durable checkpoint or savepoint where appropriate, verify restoration compatibility, bound redistribution bandwidth, and prevent concurrent schema or topology changes from invalidating the recovery point.

For keyed streams, rescaling can redistribute key groups and restart tasks. For storage services, shard movement changes failure domains and network load. Treat rescale as an operational change with progress, cancellation, timeout, and rollback—not an instantaneous integer assignment.

### Preserve shuffle, cache, and local data

Removing an executor or node may delete shuffle blocks, caches, spill files, or local replicas that later stages require. A framework can preserve correctness through external shuffle service, shuffle tracking, decommission and block migration, or reliable shuffle storage. The exact mechanism must be enabled and tested before aggressive idle removal.

Locality affects effective service: newly added remote workers may initially slow jobs or overload the network. Charge warmup and reconstruction cost to the scaling evaluation. Never assume recomputable data is free to recompute during a deadline or incident.

### Make node consolidation a proof obligation

Scale-down candidates must pass a simulation: every non-terminating workload can move to remaining capacity while respecting requests, topology, volumes, ports, affinities, disruption budgets, system workloads, and tenant guarantees. Local storage, singleton system pods, or unavailable zones may make a node non-removable.

Cordon, drain, checkpoint or decommission, observe replacement readiness, then terminate. Bound concurrent disruption and abort on new pressure. Consolidation that swaps instance types must include boot time, price volatility, capacity availability, and data movement—not just a cheaper hourly rate.

### Protect downstream dependencies

More consumers can increase useful throughput only while downstream storage, database, network, API, or lock capacity remains available. Observe dependency queueing, throttling, errors, and service-rate saturation. Couple admission and maximum replica bounds to a declared dependency envelope.

During an outage, retries can inflate queue length without representing new useful demand. Use stable logical-work identifiers, retry budgets, exponential backoff, and circuit breaking. A controller should distinguish new arrivals from repeated attempts where possible.

### Enforce quota, fairness, and cost boundaries

Autoscaling does not override tenant maxima, priority fences, queue guarantees, or resource flavors. Attribute desired, requested, provisioned, ready, used, and wasted capacity to a tenant and policy generation. A tenant should not escape allocation policy by choosing a more aggressive scaler.

Use a reserved reliable baseline for steady critical demand and elastic or interruptible capacity for suitable bursts. Include interruption probability, checkpoint/replay cost, egress, license, and control-plane charges. Define global budget and provider-quota ceilings before an incident.

### Observe causes, not only sizes

Emit the raw and normalized metric, sample interval and freshness, computed recommendation, previous/desired/bounded target, policy generation, outstanding actuation, and decision reason. Correlate provider request, scheduler decision, workload readiness, useful service, state transfer, and completion.

Measure time to requested, provisioned, scheduled, ready, and effective capacity; target error; oscillation; action count; backlog age; latency/deadline; OOM and throttling; checkpoint/recovery; evictions; lost work; dependency saturation; cost; and carbon or energy where governed. Dashboards must show blocked reasons and maximum-bound demand, not flatten them into “at max.”

### Roll out and recover controllers safely

Version policy and model inputs. Run offline trace replay, then shadow recommendations without actuation. Canary a bounded workload or queue with hard limits, observe full delay cycles, and compare against an agreed baseline. Freeze or roll back automatically on safety invariant breach.

Controller restart reconstructs desired state, outstanding operations, stabilization history, and completed idempotency keys. A rollback must reconcile resources created by the new generation and preserve stateful operations already in progress. Provide manual freeze, bounded override, and audit paths for incidents.

## Definitions and Notation

Let $B(t)$ be durable backlog, $\lambda(t)$ arrival rate, and $\mu(n,x)$ useful service rate per ready unit under replica count $n$ and context $x$ such as data shape, resource size, locality, and dependency health. Let $H$ be a target drain horizon, $h>1$ a headroom factor, and $n_{\min},n_{\max}$ policy bounds.

A simple unconstrained target is $n^*=\lceil h(\lambda+B/H)/\mu\rceil$, then $n_d=\min(n_{\max},\max(n_{\min},n^*))$. This assumes positive comparable service rate, parallelizable work, and enough downstream/substrate capacity. If $\mu$ depends strongly on $n$, use the measured aggregate capacity curve rather than multiplying a constant.

Let $n_d$, $n_q$, $n_p$, $n_r$, and $n_e$ denote desired, requested, provisioned, ready, and effective units. Capacity debt over interval $[a,b]$ can be summarized as $\int_a^b\max(0,n_d(t)-n_e(t))dt$. Let $L=L_m+L_d+L_p+L_s+L_w$ combine measurement, decision, provisioning, scheduling, and warmup delay.

For a utilization-style signal, a proportional replica recommendation often has the form $n^*=\lceil n_c m_c/m_t\rceil$, where $n_c$ is current replicas, $m_c$ observed metric, and $m_t>0$ target. Its validity depends on signal proportionality and stable denominators. A deadband $\epsilon$, scale rate bound $\Delta$, stabilization window $W$, and cooldown $T_c$ limit action. These are policy parameters to calibrate, not universal constants.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Declare workload outcome, scope, time horizon, risk, disruption, fairness, and cost objectives.
2. Identify horizontal, vertical, node, storage, control-plane, and dependency controllers plus their authority boundaries.
3. Define metric semantics, units, event time, freshness, generations, missing-data mode, and durable demand identity.
4. Estimate useful service and target capacity with explicit parallelism, skew, warmup, downstream, quota, and topology assumptions.
5. Apply minima/maxima, headroom, deadband, asymmetric stabilization, action-rate bounds, cooldown, and outstanding-action accounting.
6. Reconcile desired through requested, provisioned, scheduled, ready, healthy, and effective states with idempotent operations.
7. Prove scale-out is supportable by dependencies and scale-in preserves state, shuffle, quorum, placement, disruption, and tenant guarantees.
8. Coordinate horizontal, vertical, node, storage, and framework loops so one controller's actuator is another's explicit input.
9. Observe causal transitions, blocked reasons, capacity debt, outcomes, cost, fairness, and policy/model generation.
10. Replay traces and faults, shadow, canary, freeze on invariant breach, and reconcile controller restart or rollback.

If every decision uses samples from one accepted generation and refuses stale data, then a stale low sample cannot directly authorize scale-in. This does not prove signal correctness; source semantics and collection health still require validation.

If a node is terminated only after simulation places all protected workloads on remaining capacity and drain confirms those moves under unchanged assumptions, scale-down preserves declared placement constraints. Concurrent arrivals, failures, or topology changes can invalidate the simulation, so the operation needs reservation, version checks, and abort conditions.

The backlog formula balances modeled arrival plus a finite drain rate. It does not prove five replicas will deliver five times one-replica throughput. That conclusion additionally requires divisible work, homogeneous effective units, no shared bottleneck, and stable service measurement. Validation must test the capacity curve and record saturation.

## Alternatives and Trade-Offs

- **Static peak fleet:** predictable and operationally simple; expensive and still wrong when peaks or failures exceed assumptions.
- **Scheduled scaling:** removes predictable cold start; forecast errors need metric correction and bounded surplus.
- **CPU-based horizontal scaling:** widely available and responsive for CPU-bound work; weak for backlog, I/O, memory, and dependencies.
- **Backlog/rate scaling:** connects to work completion; requires trustworthy queue semantics and service-rate estimates.
- **Latency-based scaling:** targets user outcome; delayed, noisy, and confounded by dependencies or admission.
- **Vertical scaling:** improves per-unit fit and can reduce waste; may restart work and conflict with horizontal scaling or node sizes.
- **Horizontal scaling:** spreads failure and increases parallelism; adds coordination, shuffle, partition, and dependency load.
- **Reactive node provisioning:** follows actual pending requests; boot delay can miss bursts and deadlines.
- **Warm pools or overprovisioning:** reduce scale-out latency; retain idle cost and can mask slow provisioning.
- **Predictive scaling:** can act before demand; model drift and correlated errors require conservative fallback.
- **Long stabilization:** suppresses churn and protects state; responds slowly to genuine change.
- **Fast scale-down:** saves cost quickly; risks lost shuffle, cold starts, repeated data movement, and availability loss.
- **Scale-to-zero:** eliminates idle compute; needs durable external activation and accepts cold start.
- **Spot or preemptible burst:** reduces nominal cost; interruption, checkpoint, replay, and scarcity affect effective cost.
- **Automatic consolidation:** improves packing; simulations, drains, topology, and disruption make it operationally complex.
- **Framework-native autoscaling:** understands stages or operators; can conflict with platform-level request and node controllers.

## Failure Modes and Misconceptions

- **“CPU is demand.”** blocked or I/O-bound work can have low CPU and severe backlog.
- **“A replica is capacity.”** it may be pending, cold, unhealthy, skewed, or unable to acquire work.
- **“Node utilization drives scale-out.”** unschedulable requests and placement constraints determine needed nodes.
- **“Five replicas provide five times throughput.”** shared bottlenecks, skew, serial work, and coordination break linearity.
- **“Missing means zero.”** collection failure must not authorize destructive scale-in.
- **“Memory averages are safe.”** rare peaks and non-heap allocations cause OOM despite a low mean.
- **“Vertical and horizontal scaling compose automatically.”** request changes alter utilization denominators and packing.
- **“Cooldown begins when the API accepts.”** effective capacity may still be minutes away.
- **“Retries are fresh demand.”** retry storms can make an impaired dependency attract more consumers.
- **“Scale-to-zero is just minimum zero.”** activation must come from a durable source outside absent replicas.
- **“Any pending pod justifies a node.”** no available node type may satisfy its request or topology.
- **“Provisioned equals productive.”** boot, pull, register, state restore, cache warmup, and skew delay service.
- **“Idle executors are disposable.”** they may hold shuffle, cache, leases, or expensive recovered state.
- **“Recomputable means free.”** reconstruction consumes time, bandwidth, capacity, and deadline margin.
- **“Consolidation is bin packing.”** disruption, volumes, system workloads, quorum, and new arrivals also matter.
- **“Autoscaling bypasses quota.”** capacity automation remains subordinate to tenant and global policy.
- **“Lower hourly cost proves success.”** latency, backlog, failure, replay, and operator burden may increase total cost.
- **“A controller restart starts fresh.”** outstanding operations and stabilization history must reconcile durably.

## Worked Examples

### Example 1

A consumer's CPU is 25%, but durable lag grows by 10,000 records each minute while processing rate is below arrival rate. CPU-based scale-in would worsen freshness. Rate-and-backlog policy requests more consumers only after verifying partitions and the sink can use them.

### Example 2

An HPA creates 20 pods, but 12 remain unschedulable because their memory requests exceed current free blocks. Node autoscaling evaluates matching node classes and topology. The dashboard keeps desired 20, ready 8, and effective 7 distinct rather than reporting “scaled to 20.”

### Example 3

A VPA recommends 70 GiB for a worker, while the largest eligible node leaves 60 GiB after system overhead. Applying it would create permanent pending work. Policy caps or provisions a compatible class before rollout and records the unfulfilled recommendation.

### Example 4

A batch stage has 40 remaining tasks and 100 executors. Adding another 100 cannot increase stage parallelism. The scheduler waits for the next wide stage or reduces idle executors only after protecting shuffle needed downstream.

### Example 5

A stateful stream scales from eight to sixteen subtasks. It completes a durable checkpoint, requests parallelism, redistributes key groups, restores state, waits for useful processing, and only then starts cooldown. If restore time violates the freshness budget, the change aborts or rolls back.

### Example 6

A database outage makes consumer calls fail and retry. Queue length triples, but logical new-arrival rate is unchanged and dependency errors are saturated. A bounded controller freezes further scale-out, applies retry backoff, and protects recovery instead of multiplying load.

### Example 7

A fleet is quiet for ten minutes, yet one node hosts local shuffle required by a later stage. Consolidation simulation marks it non-removable until shuffle tracking, migration, or reliable external storage proves recovery. Low CPU alone does not permit termination.

### Example 8

A query service normally scales to zero overnight, but its only trigger metric is emitted by the service itself. At zero, it can never reactivate. Moving activation to the durable request queue fixes the zero-observer paradox; a warm minimum may still be required for latency.

### Example 9

The node controller reaches its provider quota while backlog continues rising. Repeating provider calls adds no capacity. Anti-windup holds the bounded target, emits `provider_quota_exhausted`, triggers admission degradation, and exposes capacity debt until quota or policy changes.

### Example 10

The fixture derives a backlog-and-rate target under a deliberately simple linear service model.

<!-- bijux-verify: {"id":"backlog-replica-target","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"required_rate=500.0\nraw_target=5\nbounded_target=5\n","stderr":""}} -->
```python
import math

backlog = 12_000
arrival_per_second = 300
service_per_replica = 100
drain_horizon_seconds = 60
minimum_replicas = 2
maximum_replicas = 20

required_rate = arrival_per_second + backlog / drain_horizon_seconds
raw_target = math.ceil(required_rate / service_per_replica)
bounded_target = min(maximum_replicas, max(minimum_replicas, raw_target))

print(f"required_rate={required_rate}")
print(f"raw_target={raw_target}")
print(f"bounded_target={bounded_target}")
```

The output says five ready, equally productive replicas are needed if rates remain steady and capacity scales linearly. It omits warmup, uncertainty, skew, dependency ceilings, placement, and node availability; those become explicit production constraints rather than hidden rounding factors.

## Cross-Program Connections

- **Control theory:** delayed observations, deadbands, hysteresis, saturation, anti-windup, and interacting loops determine stability.
- **Algorithms:** queue estimation, online decisions, forecasts, bin packing, constrained placement, and change-point detection shape policy.
- **Distributed systems:** reconciliation, idempotency, generations, leases, partial failure, and stale observations govern controller correctness.
- **Data engineering:** DAG parallelism, partition skew, consumer lag, checkpoints, shuffle, caches, and deadlines define useful capacity.
- **Platform engineering:** workload autoscalers, resource requests, schedulers, node provisioners, quotas, disruption budgets, and telemetry implement the loop.
- **Reliability engineering:** overload, recovery margin, dependency protection, canaries, freeze paths, and rollback bound failure.
- **Economics and sustainability:** baseline versus burst capacity, interruption, data movement, licenses, cost, and energy influence the optimum.
- **Security and governance:** tenant identity, budget authority, quota, audit, and protection against demand amplification constrain automation.

## References

1. Kubernetes. [Workload Autoscaling.](https://kubernetes.io/docs/concepts/workloads/autoscaling/) Current overview of horizontal and vertical workload autoscaling concepts.
2. Kubernetes. [Horizontal Pod Autoscaling.](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/) Current replica recommendation, metrics, tolerance, behavior, stabilization, and readiness semantics.
3. Kubernetes. [Node Autoscaling.](https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/) Current node provisioning and consolidation based on workload requests and placement constraints.
4. Kubernetes Autoscaler. [Vertical Pod Autoscaler Components.](https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/components.md) Current recommender, updater, admission-controller, and checkpoint responsibilities.
5. Kubernetes Autoscaler. [Cluster Autoscaler README.](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/README.md) Current cluster-autoscaler purpose, provider integrations, and operating entry points.
6. Kubernetes Autoscaler. [Cluster Autoscaler FAQ.](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md) Current scale-up, scale-down, placement, disruption, and node-group constraints.
7. Apache Spark. [Configuration.](https://spark.apache.org/docs/latest/configuration.html) Current dynamic-allocation backlog, idle, minimum/maximum, shuffle, and decommission settings.
8. Apache Flink. [Elastic Scaling.](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/elastic_scaling/) Current adaptive scheduling and declarative-resource scaling behavior and limitations.
9. Apache Flink Kubernetes Operator. [Autoscaler.](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/managing/autoscaler/) Development documentation for rate-based metrics, utilization boundaries, stabilization, and parallelism changes; version-specific behavior must be verified before use.
10. KEDA. [ScaledObject Specification.](https://keda.sh/docs/2.21/reference/scaledobject-spec/) Current polling, cooldown, replica bounds, fallback, trigger, and scale-to-zero configuration.
11. Rzadca et al. [Autopilot: Workload Autoscaling at Google Scale.](https://research.google/pubs/autopilot-workload-autoscaling-at-google-scale/) Primary account of horizontal and vertical resource management, historical signals, slack, and risk.
12. Tirmazi et al. [Borg: The Next Generation.](https://research.google/pubs/borg-the-next-generation/) Primary account of later Borg architecture, workload behavior, overcommitment, and automatic vertical scaling.
13. Kubernetes. [Disruptions.](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) Current voluntary/involuntary disruption concepts, graceful eviction, and disruption-budget boundaries.

## Exercises

### Exercise 1

A queue has 36,000 records, receives 400 records/s, and each ready replica sustainably processes 200 records/s. Compute the raw replica target for a 90-second drain horizon. Then state five assumptions the arithmetic does not prove.

### Exercise 2

Design coordinated policies for horizontal workload scaling, vertical memory recommendations, and node autoscaling. Specify controller inputs, outputs, authority, timing, and how you prevent shared-signal oscillation.

### Exercise 3

Design safe scale-down for a mixed Spark and stateful-streaming cluster. Cover shuffle, checkpoints, local data, topology, disruption, concurrent demand, abort conditions, and evidence of completion.

### Exercise 4

Specify observability for a workload that repeatedly requests 100 replicas but reaches only 60. Include state transitions, reason codes, metrics, generations, fairness, cost, and operator actions.

### Exercise 5

Design an evaluation that compares CPU, backlog/rate, scheduled, and predictive autoscaling. Include trace cases, faults, success metrics, shadowing, canary limits, freeze conditions, and rollback.

## Answers to the Exercises

### Answer 1

The backlog drain rate is $36{,}000/90=400$ records/s. Combined with 400 records/s arriving, required rate is 800 records/s. At 200 records/s per replica, the raw target is $\lceil800/200\rceil=4$. It assumes stable arrival and service rates, homogeneous ready replicas, divisible work with at least four-way parallelism, no shared downstream saturation, and negligible provisioning/warmup during the horizon. It also does not prove placement, quota, failure headroom, or acceptable checkpoint cost.

### Answer 2

The horizontal controller consumes durable backlog/rate and publishes bounded desired replicas. It does not use CPU utilization whose denominator changes with requests. The vertical recommender consumes memory peaks, OOM/throttling, phases, and comparable history, then publishes advisory request ranges; an updater applies them only in a maintenance or checkpoint-safe window. The node controller consumes unschedulable requests plus placement constraints and publishes provider operations. A coordinator validates proposed vertical sizes against node classes, freezes horizontal scale-in during restart, carries outstanding actions into cooldown, uses separate generations, and exposes hard quota or topology ceilings. Each controller has one actuator, freshness rules, idempotency, rate bounds, and a safe hold mode.

### Answer 3

Inventory which executors hold required shuffle/cache and which stream tasks own state. Spark removal requires an enabled, tested external-shuffle, shuffle-tracking, decommission/migration, or reliable-storage mechanism; otherwise protect the executor. Streaming scale-down requires a recent durable checkpoint/savepoint, compatible restore, bounded state transfer, and healthy checkpoint history. Simulate all protected workloads on remaining nodes with volumes, zones, affinities, system overhead, quorum, and disruption budgets. Cordon, decommission/checkpoint, drain gradually, confirm replacement/effective capacity, then terminate. Abort on new pressure, failed checkpoint, transfer timeout, topology change, unavailable replacement, or SLO breach. Evidence includes state/checkpoint identity, shuffle disposition, drain events, zero orphan work, ready/effective capacity, and recovered latency/backlog.

### Answer 4

Record raw metrics with event/collection time, freshness, workload and policy generation; recommendation before and after bounds; desired 100; API-requested and accepted units; pending requests with scheduler reason; provider operations; provisioned, registered, scheduled, ready, healthy, and effective counts; warmup and service rate; and capacity debt. Reason codes might identify tenant maximum, provider quota, incompatible topology, node-class shortage, image failure, admission denial, or readiness failure. Attribute requested/provisioned/wasted cost to tenant, show guarantee and maximum effects, and correlate backlog age and SLO impact. Operators need freeze, bounded override, quota escalation, invalid-request rejection, admission degradation, and rollback controls—not a single “60/100” gauge.

### Answer 5

Replay normal cycles, sudden bursts, slow ramps, batch schedules, partition changes, skew, and quiet periods. Inject stale/missing/reset metrics, slow provisioning, quota exhaustion, unavailable node classes, dependency saturation, retry storms, failed readiness, checkpoint failure, controller restart, and unsafe drain candidates. Compare SLO attainment, queue/backlog age, deadline, time to effective capacity, target error, action count/oscillation, lost work, disruption, dependency load, tenant fairness, and full cost. Run each policy offline against held-out traces, shadow live recommendations, then canary bounded noncritical workloads through several complete delay cycles. Freeze on state loss, quota/fairness breach, dependency overload, unbounded churn, or material SLO regression. Roll back policy generation while reconciling outstanding nodes, replicas, state transfers, and stabilization history.
