---
module_id: PLAT-082
program: Platform Engineering
level: 2
module_number: 82
title: Control-Plane Capacity
status: complete
last_verified: 2026-09-02
---

# Control-Plane Capacity

## One-Page Review

### Governing question

How should a platform model, provision, protect, and verify control-plane capacity so ordinary demand, synchronized bursts, controller retries, fleet recovery, upgrades, telemetry, admission, and malicious or buggy clients cannot turn shared orchestration into unbounded queues, starvation, data-store instability, or a recovery deadlock?

### Essential definitions

- A **control plane** accepts intent, validates and persists desired state, schedules or orchestrates work, reconciles observed state, and exposes status; it is distinct from the workload data path even when they share infrastructure.
- **capacity** is the sustainable work a system can complete while meeting latency, correctness, durability, fairness, and recovery objectives—not merely its peak accepted request rate.
- **demand** is offered work, including user requests, watches/lists, controller reconciliation, background maintenance, retries, and recovery replay.
- A **work unit** is a normalized cost class such as read, write, list-by-cardinality, watch initialization, admission evaluation, reconciliation, or provider operation.
- **utilization** is demanded service time divided by available service time for a bottleneck resource.
- **headroom** is reserved capacity between expected/qualified demand and the onset of unsafe latency or instability.
- **concurrency** is work simultaneously occupying a resource; it differs from arrival rate and throughput.
- **backlog** is accepted work not yet completed; queue age often matters more than count.
- **flow control** classifies, queues, fairly dispatches, or rejects requests so one source cannot starve critical progress.
- **load shedding** rejects or defers lower-value work before overload destroys useful throughput.
- A **retry storm** occurs when failures or latency cause clients to increase offered load through synchronized or unbounded retries.
- A **recovery envelope** is the demand and degraded capacity expected after restart, failover, partition healing, restore, upgrade, or mass resynchronization.

### Central model, mechanism, or theorem

For work class $i$, offered rate is $\lambda_i$, mean service demand at bottleneck $k$ is $s_{ik}$, and available parallel capacity is $m_k$. Approximate utilization is

$$
\rho_k=\frac{\sum_i\lambda_i s_{ik}}{m_k}.
$$

Little’s Law relates average in-system work $L$ to effective arrival rate and time $W$: $L=\lambda W$ under stable long-run conditions. As a bottleneck approaches saturation, queue latency and retry amplification can rise sharply before CPU appears fully used. Capacity qualification therefore requires a multidimensional demand envelope, explicit headroom, bounded queues/retries, fairness for critical flows, and tests beyond the knee into controlled shedding and recovery.

### Critical invariants

- Capacity is specified per user journey and work class with latency, success, convergence, fairness, and recovery objectives.
- Demand inventories users, controllers, nodes/agents, watches, lists, writes, admission, background jobs, retries, upgrades, and recovery storms.
- Work is cost-weighted by object/payload/cardinality, fan-out, consistency, storage, serialization, webhook/provider calls, and reconciliation effects.
- Every accepted asynchronous item has a bounded queue, deadline/expiry, idempotency identity, retry policy, ownership, and observable age.
- Critical health, leader election, node/control-plane progress, recovery, and audit flows retain capacity under overload; exemptions are minimal and cannot carry arbitrary user work.
- Clients use list/watch or event mechanisms correctly, cache locally, paginate where supported, constrain selectors, back off with jitter, honor server throttling, and avoid synchronized resync.
- Admission, conversion, authorization, identity, DNS, network, storage, and provider quotas are part of the control-plane capacity path.
- The durable state store maintains quorum, disk latency, space, compaction, defragmentation, backup, and restore margins under peak and failure conditions.
- Horizontal replicas are credited only after shared bottlenecks, affinity, leadership, serialization, cache warm-up, and failure-domain loss are measured.
- Load tests use production-like schemas, object counts, watches, tenants, policy, latency, churn, and dependencies; toy request rates do not establish capacity.
- Capacity changes, limits, flow-control rules, client budgets, and provider quotas are versioned and tested for ordinary, degraded, and recovery states.
- Overload sheds or delays declared lower-priority work without silently losing accepted intent, corrupting state, or blocking the actions required to recover.

### Common failures

Sizing by node count alone; using average request rate; treating GET, LIST, WATCH, PATCH, and admission as equal; ignoring object size/cardinality; unpaginated fleet lists; periodic polling instead of watches; every controller resyncing at the same interval; zero-jitter retries; unlimited client concurrency; queues with no age/expiry; 202 response counted as capacity success; more API replicas assumed linear; etcd disk shared with noisy workloads; slow admission webhook holding concurrency; provider quota outside the model; flow-control catch-all receiving production work; health traffic exempted too broadly; load test with empty clusters; testing only below saturation; autoscaling after the bottleneck; no zone-loss headroom; compaction/defrag unplanned; and recovery replay larger than steady-state capacity.

### Compact example

A platform qualifies a production cluster for 25 steady writes/s, 500 reads/s, 6,000 watches, and bounded hourly batch operations, plus a recovery case in which 1,200 controllers reconnect and relist after one API-server zone is lost. It weights LIST by returned objects and writes by admission plus reconciliation fan-out. API Priority and Fairness reserves critical node, leader-election, and recovery flows; tenant automation has bounded concurrency and queues; interactive user changes retain a separate share. Clients use shared informers, pagination, jittered backoff, and `Retry-After`. Tests include slow etcd disk, webhook latency, provider throttling, cache cold start, compaction, and restore. Qualification stops at the highest envelope meeting journey SLOs and recovery time with declared headroom—not at the last rate before a crash.

### Connections

Control-plane capacity operationalizes SLOs from PLAT-081 and the autonomy/guardrail boundaries from PLAT-071–080. It relies on reconciliation mechanics from PLAT-051–060 and platform API/workflow/event architecture from PLAT-061–070. Its results determine fleet topology, dependency isolation, upgrades, overload protection, incident response, disaster recovery, cost, and scaling decisions in PLAT-083–090.

## Governing Question

How much useful orchestration can a platform sustain—and recover—when load is heterogeneous, stateful, recursive, bursty, and partially generated by the platform itself?

Control-plane demand is unlike a stateless web benchmark. One user request can write desired state, invoke admission, wake several controllers, call cloud APIs, publish events, update status repeatedly, and create thousands of watched changes. Failure creates additional reconciliation and retry work.

The correct objective is not to accept the most requests. It is to preserve critical progress and bounded user outcomes while rejecting or delaying work safely before shared state and recovery mechanisms destabilize.

## Why This Matters

A saturated control plane may leave running workloads serving traffic while preventing deployments, scaling, credential rotation, node repair, policy changes, or incident recovery. This creates deceptive partial availability: the data plane looks healthy until the next change is required.

Queueing turns small latency increases into large operational harm. Slow storage or admission increases time each request holds concurrency; queues grow; clients time out and retry; controllers fall behind; caches become stale; full relists add load. The system can cross a feedback-loop threshold abruptly.

Capacity is multi-tenant governance. An enthusiastic automation client, huge custom resource, broad list, or faulty controller can consume shared API, memory, storage, webhook, or provider capacity. Fairness and per-client budgets protect autonomy better than a fragile unbounded commons.

Recovery is usually the peak. API replicas restart cold, watches reconnect, controllers relist, leases renew, nodes report, admission dependencies recover, and queued user intent resumes. A system sized only for steady state may be unable to escape the failure state.

## Prerequisites and Retrieval

Retrieve queueing theory, Little’s Law, utilization, service demand, concurrency, tail latency and saturation; distributed consensus and quorum; API request lifecycle; Kubernetes API concepts, LIST/WATCH/resourceVersion, API Priority and Fairness, admission and controllers; etcd Raft, WAL, snapshots, compaction, defragmentation, quotas, disk latency and restore; caching and pagination; client rate limiting, exponential backoff and jitter; idempotency and work queues; load shedding and graceful degradation; SLOs and burn rates; capacity forecasting; workload/fault testing; multi-tenancy, quotas and priority; dependency/provider quotas; observability cardinality; high availability and failure domains; upgrade and disaster recovery.

Distinguish offered load from completed throughput; request count from cost; concurrency from rate; queue count from age; acceptance from convergence; control-plane availability from workload availability; read from consistent read; list from watch; watch connection from watch event rate; cache hit from storage read; controller worker count from useful throughput; horizontal replica from independent capacity; headroom from idle waste; overload rejection from failure; fairness from equal shares; steady state from recovery; and benchmark peak from qualified sustainable capacity.

## Learning Objectives

After completing this module, you should be able to:

1. map platform control-plane paths from intent through API, storage, admission, queues, controllers, providers, and status;
2. define cost-weighted work classes and demand envelopes for ordinary, burst, failure, recovery, upgrade, and adversarial states;
3. use utilization, Little’s Law, queue age, latency, throughput, and convergence to locate saturation knees;
4. design client budgets, pagination, shared watches/caches, jittered retries, deadlines, and idempotent queue behavior;
5. configure fair queuing, priority, concurrency, backpressure, and load shedding without starving recovery or tenants;
6. capacity-plan API servers, state stores, admission/conversion, controllers, workflow engines, and provider quotas as one path;
7. qualify scaling claims under shared bottlenecks, leader-only work, cache warm-up, zone loss, and maintenance;
8. run realistic workload and fault tests beyond saturation and through recovery;
9. forecast capacity, govern onboarding/launches, and connect headroom to SLO/error-budget decisions; and
10. migrate uncontrolled control-plane clients toward measurable budgets and conformance contracts.

## Core Exposition

### Map the control-plane work graph

Begin with user journeys: create environment, deploy, scale, rotate identity, change policy, delete, restore. Trace synchronous request filters and asynchronous effects. Mark authentication, authorization, admission, conversion, persistence, watches/events, queue, controller, provider API, status, audit, and notification.

One accepted object may trigger many writes. A controller can update status, create children, receive watch events about those children, and reconcile again. Quantify fan-out and feedback edges rather than benchmarking only the first API call.

Identify shared resources: API concurrency, CPU and memory; caches; etcd disk/network/quorum/space; admission and conversion webhooks; workflow database and workers; message broker; cloud quotas; DNS/identity; and telemetry pipelines.

Mark serial and leader-only sections. Adding replicas cannot scale work protected by one lock, one leader, one ordered partition, or one consensus commit path.

### Define cost-weighted work classes

Classify verb, resource, scope, consistency, payload/object size, returned cardinality, selector, dry-run, admission/conversion set, and expected controller fan-out. Keep classification low-cardinality enough to observe.

A cached GET differs from a linearizable read. A one-object PATCH differs from a LIST returning 100,000 objects. A watch establishment differs from ongoing event delivery. A custom resource may have expensive schema conversion or validating webhooks.

For asynchronous work, define reconcile cost by reads, writes, provider calls, expected duration, and retry behavior. Separate no-op reconciles from mutations; excessive no-op rate is still capacity demand.

Use empirical service demand from traces/profiles and controlled tests. Avoid one universal “request unit” unless its mapping to real resources is maintained.

### Build demand envelopes

Measure steady rate, diurnal peak, percentile bursts, concurrency, object population, watch count/event rate, change churn, queue arrivals, controller resync, and provider operations. Segment tenants, client identities, resources, and journeys.

Create named scenarios: normal peak; batch/launch; node churn; rolling control-plane upgrade; one-zone loss; network partition heal; API restart/cold cache; controller release; webhook slowdown; etcd maintenance; fleet policy rollout; and full disaster restore.

Include growth in nodes, objects, custom resource sizes, tenants, controllers, platform capabilities, audit volume, and automation sophistication. Node count is only one driver.

State simultaneity assumptions. Individually safe batch jobs can align on midnight, certificate expiry, Git polling, resync periods, or a regional recovery and exceed capacity together.

### Apply queueing reasoning carefully

Little’s Law $L=\lambda W$ helps validate measurements: if 100 completions/s spend 2 seconds in system, average in-system work is about 200. A mismatch suggests definitions, loss, or unstable windows need review.

Utilization near one leaves little room for variance. Tail service times, correlated bursts, blocking dependencies, and retries create queues well before average throughput stops rising. Find the latency/queue knee empirically.

Bound concurrency and queue. An infinite queue converts overload into expired work and memory/storage failure. Define maximum age/deadline and discard or reconcile superseded desired state safely.

Do not use steady-state formulas as exact guarantees during nonstationary recovery. Combine analytic models with traces, simulations, and fault/load experiments.

### Design efficient API clients

Cache locally and subscribe to changes rather than polling full collections. Kubernetes list-then-watch uses `resourceVersion`; clients must recover from unavailable history with a new list and watch. Use established client libraries where possible.

Share informers/caches among controllers observing the same resources. Scope watches and lists to required namespaces/resources/selectors. Pagination reduces response memory and transfer, though filtering and version semantics must be tested for the actual server.

Limit client QPS, burst, concurrency, and outstanding work. Back off exponentially with jitter, honor `429` and `Retry-After`, and stop retrying after deadlines or permanent errors. A timeout does not prove the server aborted work; idempotency prevents duplicate effects.

Stagger resync and maintenance. Avoid resync unless required; reconciliation should primarily react to watched desired/observed changes and periodic safety checks with randomized schedules.

### Bound controller work

Use rate-limited keyed work queues. Coalesce repeated events for the same subject and reconcile latest desired state rather than every intermediate notification when semantics allow.

Reconciliation is idempotent and level-based. Distinguish retryable, terminal, and waiting-for-dependency states. Exponential backoff is per key or failure domain so one broken tenant cannot occupy every worker.

Worker concurrency is a control, not a goal. Increasing workers can overwhelm API, etcd, database, provider quota, or downstream service and reduce throughput. Tune against end-to-end convergence and dependency saturation.

Expose queue depth, oldest age, arrival/completion/retry rates, active workers, service duration, result, dependency calls, and per-tenant/resource hot keys. Alert on threatened journey deadlines and recovery time.

### Protect with priority and fairness

Classify flows by authenticated identity, verb, resource, namespace/tenant, and purpose. Reserve progress for node health, leader election, control-plane recovery, critical writes, and incident operations. Separate expensive batch/list traffic and untrusted extensibility.

Kubernetes API Priority and Fairness uses FlowSchemas and PriorityLevelConfigurations to classify, limit, queue, fairly dispatch, or reject work. Queuing absorbs brief bursts; rejection prevents unbounded accumulation. Watch requests participate in APF, while some long-running requests have different treatment.

Fair does not mean equal. Shares reflect criticality and tenancy, with minimum progress and maximum consumption. Test classification: a broad exempt identity can bypass protection, while misclassified recovery traffic can deadlock restoration.

Observe seats/concurrency, queue length and wait, rejections, request latency, work estimates, and flow/priority labels. Rejection across levels without demand growth may indicate slow downstream service rather than wrong shares.

### Engineer admission and extension budgets

Every authentication/authorization/admission/conversion extension adds service time and failure dependency. Model match frequency, serial/parallel behavior, timeout, payload, external data/cache, replicas, zones, and failure policy.

Set per-extension latency and availability objectives tighter than the API journey allocation. Minimize matches and remote calls. Prefer in-process validation for suitable foundational controls.

Load-test worst legitimate objects and malicious complexity. A regex, schema, CEL expression, conversion, or external lookup whose cost grows unexpectedly with object size can consume API seats.

Protect recovery dependencies from self-interception. During webhook outage, the capacity needed to restore its Deployment, Service, DNS, certificates, or policy must remain available under deliberate failure behavior.

### Treat durable storage as the core bottleneck

Kubernetes writes and consistent reads ultimately depend on etcd. Raft commits depend on quorum network round trip and durable disk sync. Slow or variable disk can raise API latency, queues, heartbeats/elections, and retry load.

Provision dedicated low-latency storage and predictable CPU/memory/network. Monitor proposal/commit/apply latency, leader changes, failed proposals, fsync/WAL latency, peer RTT, database size, quota, fragmentation, compaction, watchers, and alarms.

Compaction removes old MVCC history; defragmentation reclaims backend space but has operational cost. Plan and test maintenance one member at a time as applicable, preserving quorum and SLO headroom. Avoid reaching space quota, which can put the cluster into restricted maintenance behavior.

Backups prove little without restore timing and integrity. Qualify restore plus control-plane cache/list/watch recovery, not only snapshot creation.

### Understand caches, lists, and watches

Watch caches reduce storage reads but consume memory and must initialize. Cold start or reinitialization can cause large lists and reconnect storms. Capacity test warm, cold, and partially unavailable histories.

Track objects returned, serialized bytes, list duration, cache hits/misses, watch count, initialization, event delivery lag, disconnects, `410 Gone`, and relists. A stable connection count can hide enormous event churn.

Large resources multiply memory, network, serialization, storage, audit, and client cache cost. Set object/payload/status limits and keep high-churn unbounded data out of desired-state objects.

Selectors reduce returned data only if server/index behavior supports them efficiently. Test actual versions and indexes; a filtered query may still scan many objects.

### Capacity-plan workflow and provider layers

A platform API may enqueue orchestration after Kubernetes accepts an object. Model workflow database connections/locks, broker partitions, workers, per-tenant concurrency, external API quotas, and callback/status writes.

Use provider rate limits as explicit resources. Schedule expensive creates/deletes, reserve incident capacity, and avoid every worker independently discovering throttling. Central token buckets or leases can coordinate budgets.

Bound fan-out and use sagas/compensation carefully. A bulk environment action should not enqueue millions of indivisible operations without cancel, pause, priority, or progress visibility.

Return acceptance only after durable intent. Expose queue position/age and deadline status. Load shedding before durable acceptance returns a retryable response; after acceptance, the platform owns eventual terminal outcome or explicit cancellation.

### Preserve headroom and failure capacity

Define headroom against the empirically observed knee for each bottleneck, not CPU alone. Reserve enough for demand variance, one failure domain, maintenance, instrumentation, and the recovery envelope.

Horizontal API replicas can add CPU/network/handler concurrency but share etcd and extensions. Losing one zone simultaneously reduces replicas and creates cross-zone traffic/reconnect load. Test N-1 and zonal routing behavior.

Vertical scale may reduce contention and simplify caches until single-process or machine limits. Horizontal scale improves failure tolerance but increases connections, caches, coordination, and backend demand. Choose from measured bottlenecks.

Autoscaling reacts after signals and may be too slow during a retry storm; it cannot scale a fixed quota, serial leader, or saturated datastore. Pre-provision critical recovery margin.

### Shed load and degrade deliberately

Reject excess work early with explicit retryability, reason, and `Retry-After`. Keep queues short enough that admitted work can meet deadlines. Jitter client retries and cap total attempts.

Defer catalog indexing, broad search, optional analytics, background scans, bulk reconciliations, and nonurgent drift checks before node health, identity, policy, deploy/rollback, secret rotation, and incident recovery.

Degradation must preserve correctness. Serve stale bounded catalog metadata if labeled; do not serve stale authorization or revocation decisions beyond policy. Coalesce superseded desired state but do not silently lose distinct user intent.

Test beyond saturation. A safe curve plateaus useful throughput, bounds latency/queues, sheds declared work, preserves priority/fairness, and recovers when demand falls. A system that collapses and remains in retry oscillation is not capacity-qualified.

### Test the production-shaped envelope

Generate realistic objects, distributions, schemas, admission policies, tenants, identities, lists, watches, churn, controller fan-out, audit, provider latency/quota, and telemetry. Empty-cluster API benchmarks are microbenchmarks.

Ramp slowly to find knees, hold plateaus for leaks/compaction, spike bursts, and soak. Measure arrival, completion, rejection, latency, in-flight, queue age, resource/service demand, errors, retries, leader/lease stability, convergence, and recovery.

Fault one dimension at a time and in credible combinations: slow disk plus writes, webhook latency plus deploy burst, API replica loss plus watch reconnect, provider throttling plus retry, compaction plus restore, and telemetry failure during overload.

Record tested version/configuration, topology, data population, workload generator, dependency behavior, results, confidence/limitations, and safe operating envelope. Requalify material upgrades and extensions.

### Forecast and govern growth

Forecast by drivers: tenants, nodes, objects, object bytes, watch/event rate, deployments, policies/webhooks, controllers, workflows, and provider operations. Relate each driver to measured work/resource demand.

Track weeks-to-headroom-exhaustion with uncertainty, not a single date. Capacity lead time includes quota requests, hardware/provider changes, load tests, migrations, and rollback.

Gate high-impact launches using declared workload shape and recovery test, not political priority alone. Tenant quotas and client conformance prevent one launch from consuming shared safety margin.

Use SLO/error-budget evidence: chronic latency/burn near the knee triggers capacity or demand reduction. Persistent excess margin may enable consolidation, but validate failure and recovery envelopes before removing it.

### Migrate uncontrolled clients

Inventory clients by identity, owner, version, verb/resource, rate, concurrency, list/watch, bytes/cardinality, retries, and business purpose. Find anonymous/shared credentials and catch-all flow classification.

Publish a client contract: supported libraries, user agent/identity, request budgets, pagination/watch, backoff/jitter, timeout, idempotency, field selection, resync, metrics, and deprecation.

Observe and warn first, then apply per-client concurrency/rate and APF classification. Give owners evidence and remediation. Expiring exceptions cover critical legacy clients while replacement proceeds.

Remove broad exemptions, synchronized polling, and unlimited workers after conformance. Retest the recovery envelope with migrated clients; steady-state rate reduction alone is insufficient.

## Definitions and Notation

Let $I$ be work classes and $K$ bottleneck resources. For class $i$ and resource $k$:

- $\lambda_i(t)$ is offered arrival rate;
- $x_i(t)$ is admitted rate;
- $\mu_i(t)$ is completed useful rate;
- $s_{ik}$ is mean service demand per completed work unit;
- $m_k$ is parallel service capacity;
- $q_i(t)$ and $a_i(t)$ are queue count and oldest age;
- $r_i(t)$ is retry amplification, offered attempts per original intent;
- $f_i$ is downstream reconciliation/provider fan-out;
- $H_k$ is required headroom fraction.

Approximate resource utilization is

$$
\rho_k(t)=\frac{\sum_i x_i(t)s_{ik}}{m_k},
$$

and a qualified envelope requires $\rho_k\le 1-H_k$ plus SLO, fairness, and recovery conditions. This linear form is a planning approximation; contention and tail behavior require empirical tests.

For a stable observation interval, Little’s Law gives

$$
L_i=\lambda_i W_i,
$$

where definitions of arrival and time-in-system share the same boundary. Retry-amplified offered load can be approximated as $\lambda_i^{attempt}=r_i\lambda_i^{intent}$, while downstream operation rate may approach $f_i\mu_i$.

Recovery debt $D(0)$ drains only if useful recovery completion $\mu_R$ exceeds new recovery arrivals $\lambda_R$:

$$
T_{drain}\approx\frac{D(0)}{\mu_R-\lambda_R},\qquad \mu_R>\lambda_R.
$$

If not, the recovery backlog cannot converge under the assumed envelope.

## Mechanisms, Invariants, or Proof Structure

### Capacity qualification mechanism

1. Select critical platform journeys and define latency, success, convergence, fairness, and recovery objectives.
2. Trace intent through APIs, filters, storage, watches/events, queues, controllers, providers, status, audit, and feedback loops.
3. Define cost-weighted work classes by operation, size/cardinality, consistency, extensions, fan-out, and tenant/client.
4. Measure steady, burst, batch, upgrade, failure, recovery, growth, and adversarial demand envelopes.
5. Locate bottlenecks using service demand, utilization, concurrency, latency, queue age, throughput, retry, and resource evidence.
6. Engineer client caches/watch/list behavior, pagination, budgets, deadlines, idempotency, jittered backoff, and staggered resync.
7. Bound controller/workflow queues and concurrency; coalesce safe desired state and coordinate provider quotas.
8. Configure priority, fairness, reserved critical progress, queue/reject behavior, and minimal exemptions.
9. Provision API, storage, extension, workflow, broker, and provider headroom for maintenance and failure-domain loss.
10. Load/fault test below, at, and beyond the knee through shedding and recovery using production-shaped state.
11. Record a versioned safe operating envelope, client contracts, forecasts, launch gates, dashboards, and runbooks.
12. Requalify after material version, policy, controller, schema, topology, tenant, provider, or demand changes.

### Admission invariant

The platform either rejects intent before durable acceptance with explicit retry semantics or owns a bounded path to terminal outcome/cancellation after acceptance. Overload cannot silently discard accepted work.

### Critical-progress invariant

Under every qualified overload and failure scenario, health, leader election, control-plane recovery, incident operations, and other named critical flows retain enough capacity to make progress.

### Client invariant

Every control-plane client has attributable identity/owner, bounded concurrency/rate/retries, deadlines, idempotency, efficient state observation, and observable demand. Shared or exempt identity cannot hide unbounded work.

### State-store invariant

Quorum, durable commit, disk/network latency, database space, maintenance, backup, and restore remain within tested margins for the qualified envelope and failure domain.

### Recovery invariant

After a qualified disruption, useful recovery completion exceeds new recovery work, critical queues drain within objective, and retry/relist feedback decays rather than sustaining overload.

### Proof sketch: stateless replica count cannot prove linear control-plane capacity

Let each of $n$ API replicas process stateless front-end work at rate $a$, but all writes require one shared durable store of capacity $e$. Write throughput is bounded by

$$
C(n)\le\min(na,e).
$$

Once $na\ge e$, adding replicas cannot increase the bound and may increase backend connections, cache/watch load, or retries. Admission webhooks, leader-only controllers, provider quotas, and serialized locks create analogous bounds. Therefore replica count or front-end benchmark cannot prove linear platform capacity. Scaling credit requires end-to-end measurement under the shared bottleneck and failure topology.

### Executable capacity audit

The synthetic audit classifies ten demand scenarios against API, state-store, and provider utilization plus recovery-drain conditions. It illustrates invariant checks, not a production sizing result.

<!-- bijux-verify: {"id":"control-plane-capacity-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"qualified=5\napi_headroom=1\nstore_headroom=1\nprovider_headroom=1\nrecovery_nonconvergent=1\ncritical_starvation=1\n"}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    api: float
    store: float
    provider: float
    recovery_arrival: int
    recovery_completion: int
    critical_progress: bool = True


scenarios = [
    Scenario("normal", .45, .40, .35, 20, 80),
    Scenario("daily-peak", .62, .55, .50, 30, 90),
    Scenario("batch", .68, .57, .65, 25, 75),
    Scenario("upgrade", .70, .61, .55, 45, 100),
    Scenario("zone-loss", .72, .69, .60, 60, 110),
    Scenario("api-burst", .86, .60, .55, 30, 90),
    Scenario("slow-disk", .65, .91, .50, 40, 80),
    Scenario("provider-throttle", .60, .55, .93, 40, 75),
    Scenario("retry-loop", .72, .70, .68, 100, 90),
    Scenario("misclassified-recovery", .70, .66, .60, 50, 85, False),
]

counts = {
    "qualified": 0,
    "api_headroom": 0,
    "store_headroom": 0,
    "provider_headroom": 0,
    "recovery_nonconvergent": 0,
    "critical_starvation": 0,
}

for scenario in scenarios:
    if not scenario.critical_progress:
        counts["critical_starvation"] += 1
    elif scenario.recovery_completion <= scenario.recovery_arrival:
        counts["recovery_nonconvergent"] += 1
    elif scenario.api > .75:
        counts["api_headroom"] += 1
    elif scenario.store > .75:
        counts["store_headroom"] += 1
    elif scenario.provider > .75:
        counts["provider_headroom"] += 1
    else:
        counts["qualified"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Validate work classification against traces and profiles. Reconcile original intents, attempts, admitted work, completions, downstream fan-out, and queue histories. Check Little’s Law only across stable, consistently bounded windows.

Use production-shaped state and dependency simulators. Ramp, spike, and soak through the latency knee, maximum safe envelope, rejection, and recovery. Inject disk latency, member/API replica/zone loss, admission and conversion slowdown, provider quota, cache cold start, watch reconnect, audit pressure, compaction, telemetry loss, and retry misbehavior.

Assert user SLOs, critical progress, tenant fairness, bounded queue age/memory, durable accepted intent, state consistency, stable quorum, safe shedding, and recovery time. Restore from backup and observe full relist/reconciliation. Repeat after material upgrades and compare regression with confidence and limitations.

## Alternatives and Trade-Offs

1. **Vertical versus horizontal API scale:** vertical scale simplifies caches and contention; horizontal scale improves failure tolerance but shares backends.
2. **One large cluster versus more cells:** consolidation improves utilization; cells bound blast radius and state/cardinality at fleet-management cost.
3. **Polling versus watch:** polling is simple and bounded per call; watches reduce repeated lists but consume memory/connections and reconnect work.
4. **Full list versus pagination:** full lists simplify clients; pagination bounds response resources but adds consistency and client complexity.
5. **Shared informer versus independent cache:** sharing reduces watches/memory; isolation prevents one consumer’s lifecycle from affecting others.
6. **Queue versus reject:** queues absorb brief bursts; early rejection prevents expired work and retry ambiguity.
7. **Global fairness versus priority classes:** uniform fairness limits monopolies; priority preserves critical progress but risks misclassification.
8. **Reserved headroom versus high utilization:** headroom funds bursts/failures; consolidation lowers cost but narrows recovery margin.
9. **Autoscaling versus pre-provisioning:** autoscaling adapts trends; pre-provisioning survives fast storms and fixed bottlenecks.
10. **More controller workers versus bounded concurrency:** workers reduce backlog until dependencies saturate; limits preserve system stability.
11. **Strong consistency versus cached reads:** strong reads provide current authority; caches reduce load with staleness semantics.
12. **Rich admission versus fast admission:** contextual policy increases assurance; synchronous dependencies consume latency and failure budget.
13. **Large resource objects versus external data:** in-object state is declarative; large/high-churn payloads multiply storage/watch costs.
14. **Frequent resync versus event-driven reconciliation:** resync repairs missed assumptions; synchronized full scans create periodic storms.
15. **Central provider throttle versus client-local retry:** central budgets coordinate scarcity; local logic is simpler but can amplify.
16. **Separate event storage versus one etcd:** separation isolates high-churn data; it adds topology and operations.
17. **Steady-state benchmark versus recovery qualification:** steady tests are repeatable; recovery tests expose the envelope that often matters most.
18. **Hard tenant quota versus borrowing:** quotas protect fairness; borrowing raises utilization but needs rapid reclaim and priority policy.

## Failure Modes and Misconceptions

- **“Node count determines capacity.”** Objects, churn, watches, clients, policies, bytes, fan-out, and topology matter.
- **“Requests have equal cost.”** Verb, consistency, cardinality, payload, admission, and downstream effects differ.
- **“Average QPS is the load.”** Bursts, concurrency, tails, recovery and retries drive overload.
- **“CPU below 100 percent means headroom.”** Disk, locks, queues, memory, network, quotas, or latency may be saturated.
- **“Peak throughput is safe capacity.”** Sustainable SLO, fairness, durability, maintenance, and recovery define capacity.
- **“More API replicas scale writes linearly.”** Shared etcd and extensions bound throughput.
- **“Autoscaling solves overload.”** It reacts late and cannot scale serial or externally limited resources.
- **“An infinite queue prevents rejection.”** It creates latency, expiry, memory pressure, and recovery debt.
- **“202 means capacity succeeded.”** It means acceptance only if intent is durable; convergence remains outstanding.
- **“Retries add reliability for free.”** They amplify load and duplicate effects without budgets/idempotency.
- **“Exponential backoff is enough.”** Without jitter, caps, deadlines, and permanent-error handling, storms persist.
- **“WATCH is free.”** Initialization, cache memory, events, serialization, network, and reconnects consume capacity.
- **“A stable watch count means stable load.”** Event rate and payload churn may explode.
- **“Selectors always make LIST cheap.”** Server indexing and scan behavior must be verified.
- **“Controller no-op reconciliation is harmless.”** Reads, serialization, caches, and downstream checks still consume work.
- **“More workers always drain faster.”** Downstream saturation can reduce total useful throughput.
- **“Fairness means equal shares.”** Critical progress and tenant contracts require explicit weights and bounds.
- **“Exempt traffic is safe.”** Broad exemptions bypass overload protection.
- **“Health checks prove control-plane usefulness.”** They may succeed while writes, storage, admission, or reconciliation fail.
- **“Running workloads mean the control plane is fine.”** The data plane may coast while recovery and change are blocked.
- **“etcd needs only capacity bytes.”** Durable sync latency, quorum RTT, watchers, fragmentation, and maintenance matter.
- **“Compaction immediately reclaims disk.”** Logical history removal and physical defragmentation are distinct.
- **“Snapshot success proves recovery.”** Restore, quorum, caches, watches, and reconciliation must be timed and verified.
- **“Provider quotas are outside platform capacity.”** They bound the promised journey.
- **“Load shedding is an outage.”** Controlled rejection can preserve more useful service than collapse.
- **“All accepted work must run eventually.”** Superseded or expired work may be safely canceled under an explicit contract.
- **“Toy objects benchmark production.”** Schema, payload, admission and fan-out shape cost.
- **“Test only to expected peak.”** Safe behavior beyond peak and recovery after shedding are requirements.
- **“One zone loss only subtracts replicas.”** It also shifts traffic and triggers reconnect/reconciliation.
- **“Steady-state success proves recovery.”** Recovery offered load and reduced capacity are different.

## Worked Examples

### Example 1

A portal sends a full cluster-wide pod LIST every five seconds per user. API CPU and network look like user growth. The platform replaces polling with scoped cached views sourced from shared watches, paginates administrative queries, and applies per-client budgets. It preserves direct API access for diagnosis with explicit limits. Load falls without changing cluster node count.

### Example 2

An operator increases controller workers from 20 to 200 to drain a queue. Cloud API throttling rises, retries multiply, reconciles slow, and queue age worsens. A coordinated provider token bucket, per-tenant concurrency, exponential jittered backoff, and coalescing by resource key produce higher useful throughput with 30 workers.

### Example 3

A validating webhook normally adds 20 ms but its external data service slows to five seconds during a deployment burst. Requests occupy API concurrency, APF queues fill, and unrelated writes receive 429. The policy moves bounded data to a local snapshot, sets a one-second timeout/failure policy by risk, narrows matching, reserves recovery traffic, and tests stale-data behavior.

### Example 4

Etcd disk fsync tail latency rises during colocated backup IO. API writes slow, leader heartbeats become unstable, clients retry, and apparent API demand doubles. Dedicated low-latency storage, IO isolation, member-by-member maintenance, fsync/peer monitoring, and retry budgets address the shared root rather than adding API replicas.

### Example 5

After a zone loss, remaining API servers inherit traffic while 2,000 controllers reconnect and relist. A warm benchmark never modeled this. Recovery testing adds cold-cache/list/watch scenarios, staggers clients with jitter, reserves node/leader/recovery shares, limits bulk flows, and sizes N-1 headroom until queue age and convergence meet objectives.

### Example 6

A custom resource stores multi-megabyte generated status updated every second. Each change persists, audits, fans out to watchers, and invalidates caches. The design moves high-volume samples to an external data service, keeps bounded summarized status and references in the resource, limits update cadence, and measures semantic freshness separately.

### Example 7

One tenant launches 10,000 environment deletions. A global FIFO queue delays incident rollbacks for every tenant. The workflow introduces per-tenant queues, weighted fair dispatch, bulk-operation concurrency, cancellation, provider budgets, and a high-priority recovery class. Accepted deletions remain durable and visible while critical work progresses.

### Example 8

An APF rule places all requests from a shared platform service account in an exempt level. A buggy catalog scan starves normal control-plane work. Workload-specific identities and user agents separate catalog, deploy, and recovery clients; exemptions shrink; FlowSchemas receive conformance tests; rejection and queue metrics are tied to owners.

### Example 9

A cluster is below its API QPS qualification but reaches etcd space quota because Events and stale history grow. Writes enter restricted behavior and recovery becomes urgent. The team monitors in-use and total database size, configures/test compaction, schedules safe defragmentation, separates high-churn Event storage where justified, and tests quota alarms before exhaustion.

### Example 10

A platform migrates anonymous automation clients. It inventories audit identities, QPS, concurrency, lists/watches, bytes, retries, and owners; publishes a client library/contract; shadows budgets and APF classes; warns owners; then progressively enforces. Expiring exceptions protect critical legacy flows. The final recovery test proves reconnect storms now converge within envelope.

## Cross-Program Connections

1. **Queueing theory:** arrival, service demand, utilization, Little’s Law, tails, and stability explain control-plane knees.
2. **Distributed systems:** consensus, leaders, partial failure, retries, idempotency, watches, and reconciliation generate capacity dynamics.
3. **Operating systems:** CPU scheduling, memory pressure, IO latency, concurrency, locks, and admission resemble resource governance.
4. **Database engineering:** MVCC, compaction, indexes, transactions, storage space, durability, and restore constrain state planes.
5. **Network engineering:** RTT, connection storms, cross-zone routing, flow control, backpressure, and bandwidth shape recovery.
6. **Site reliability engineering:** SLOs, headroom, overload, graceful degradation, incident response, and capacity forecasting guide operation.
7. **Security engineering:** authentication, admission, tenant isolation, abuse limits, audit, and protected recovery flows are capacity consumers and controls.
8. **Performance engineering:** workload models, service demand, profiling, ramp/spike/soak, regression, and production-shaped data establish evidence.
9. **Economics and FinOps:** reserved failure capacity, consolidation, quotas, provider limits, and scaling lead time trade cost against risk.
10. **Systems engineering:** feedback loops, common-mode bottlenecks, recovery envelopes, emergent overload, and invariants require whole-path analysis.

## References

1. Kubernetes. [Considerations for Large Clusters](https://kubernetes.io/docs/setup/best-practices/cluster-large/). Retrieved 2026-09-02.
2. Kubernetes. [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/). Retrieved 2026-09-02.
3. Kubernetes. [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02.
4. Kubernetes. [Controllers](https://kubernetes.io/docs/concepts/architecture/controller/). Retrieved 2026-09-02.
5. Kubernetes. [Metrics Reference](https://kubernetes.io/docs/reference/instrumentation/metrics/). Retrieved 2026-09-02.
6. Kubernetes. [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/). Retrieved 2026-09-02.
7. etcd. [Hardware Recommendations](https://etcd.io/docs/v3.6/op-guide/hardware/). Retrieved 2026-09-02.
8. etcd. [Performance](https://etcd.io/docs/v3.7/op-guide/performance/). Retrieved 2026-09-02.
9. etcd. [Maintenance](https://etcd.io/docs/v3.7/op-guide/maintenance/). Retrieved 2026-09-02.
10. etcd. [Monitoring](https://etcd.io/docs/v3.7/op-guide/monitoring/). Retrieved 2026-09-02.
11. Google. [Site Reliability Engineering: Handling Overload](https://sre.google/sre-book/handling-overload/). Retrieved 2026-09-02.
12. Google. [Site Reliability Engineering: Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/). Retrieved 2026-09-02.
13. Google. [The Site Reliability Workbook: Managing Load](https://sre.google/workbook/managing-load/). Retrieved 2026-09-02.
14. Internet Engineering Task Force. [RFC 6585: Additional HTTP Status Codes](https://www.rfc-editor.org/rfc/rfc6585). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Build cost-weighted demand envelopes for a platform API, Kubernetes control plane, and workflow layer in normal peak, zone loss, upgrade, and restore scenarios.

### Exercise 2

Design priority, fairness, queuing, rejection, and retry contracts for node health, leader election, interactive deploys, bulk policy rollout, catalog indexing, and tenant automation.

### Exercise 3

Diagnose a control plane whose API CPU is 55 percent while p99 writes, APF queues, controller backlog, and retries rise sharply.

### Exercise 4

Create a production-shaped qualification test for adding a custom resource, conversion webhook, validating policy, and controller to a fleet.

### Exercise 5

Plan migration of uncontrolled polling/retry clients to efficient watch/cache and bounded-demand contracts without blocking critical delivery.

## Answers to the Exercises

### Answer 1

Trace journeys into classes: cached/consistent GET; paginated/unpaginated LIST by returned/scanned objects; watch initialization and events; small/large writes; admission/conversion; audit; queue item; reconcile no-op/mutation; provider call; status update. Measure payload/cardinality, service demand, fan-out, concurrency, latency, retries, and owner/tenant.

Normal peak combines diurnal user/controllers and scheduled work. Zone loss removes API/store/worker capacity while shifting traffic and reconnecting watches. Upgrade includes version skew, cache cold start, leader moves, rollout and rollback. Restore begins from snapshot, cold caches, complete relists, reconciliation debt, node/agent reconnect, and provider status discovery.

For each scenario state simultaneity, growth, dependency latency/quota, $N-1$ topology, headroom, critical shares, SLOs, queue-age and recovery targets. Qualify only if every bottleneck, fairness, durable intent, and recovery convergence passes, not because aggregate QPS is below a limit.

### Answer 2

Give node health and leader election reserved high-priority progress with narrowly matched identities/verbs/resources; do not place arbitrary service-account traffic in exempt. Incident deploy/rollback gets a protected interactive class with short bounded queues. Ordinary deploys have fair per-tenant shares.

Bulk policy rollout and tenant automation receive bounded concurrency, fair queuing, cancellation/deadlines, and provider/write budgets. Catalog indexing is low priority, deferrable, and shed first. Every client has workload identity, QPS/burst/concurrency limit, idempotency, exponential backoff with jitter, maximum attempts/deadline, and honors 429/`Retry-After`.

Test classification and starvation under slow storage, webhook, zone loss, and recovery. Observe seats, queue/wait, rejections, completion and oldest age by owner. Keep enough unqueued rejection that bursts cannot become infinite recovery debt.

### Answer 3

CPU does not identify the bottleneck. Correlate request service/queue time, in-flight seats, APF levels, admission/conversion duration, etcd commit/apply/WAL fsync/peer RTT, database size/alarms, locks, network, memory/GC, and provider calls. Rising latency increases seat occupancy; queues and timeouts cause retry amplification even at moderate CPU.

Compare original intent to attempts and classify verbs/resources/clients. Look for slow disk, webhook/external auth, huge LIST/object, hot resource conflict, controller concurrency, or provider throttle. Temporarily preserve critical progress, shed bulk flows, cap offending clients, and stop unbounded retries before scaling.

Fix the measured bottleneck—dedicated disk, local policy data, efficient clients, lower fan-out, maintenance, or dependency capacity—then ramp through the prior knee and recovery scenario. Adding API replicas alone may worsen a shared backend.

### Answer 4

Populate realistic existing and new objects at target cardinality/size/churn. Run real schemas, conversion, validation, audit, watch consumers, controller fan-out, provider simulator/quotas, telemetry, and tenant identities. Include create/update/delete/list/watch, malformed maximum objects, old-version conversion, retry and finalizer paths.

Measure end-to-end journey SLOs plus API request/queue/rejection, webhook duration/failure, serialization/bytes, etcd commit/fsync/space, watch/cache/list, controller queue age/retry/convergence, provider calls, audit, CPU/memory/network/disk. Ramp, spike, soak, and exceed the knee.

Fault slow/unavailable conversion/admission, API replica/zone, etcd disk/member, provider quota, watch reconnect, cache cold start, telemetry, and restore. Assert critical progress, fairness, bounded queues, no lost accepted intent, consistent state, safe rollback, and recovery time. Record exact versions/config/state/workload and requalify changes.

### Answer 5

Inventory clients from audit/metrics by identity/user agent, owner, version, verbs/resources, QPS/burst/concurrency, list cardinality/bytes, watches/events, resync, timeouts, retries, and purpose. Establish baselines and identify shared/exempt credentials.

Publish supported clients and contract: workload identity, shared cache/informer, list-then-watch/resourceVersion handling, scoped selectors, pagination, QPS/burst/concurrency, jittered exponential backoff, 429/`Retry-After`, deadline, idempotency, resync staggering, metrics, and deprecation.

Provide adapters and test fixtures. Shadow rate/APF policy, warn with owner-specific evidence, migrate critical clients first, and keep narrow expiring exceptions. Progressively enforce per-client budgets and fair classes, monitoring journey SLO, rejection, queue age and owner response. Remove broad exemptions only after recovery tests prove relist/reconnect storms converge and rollback is available.
