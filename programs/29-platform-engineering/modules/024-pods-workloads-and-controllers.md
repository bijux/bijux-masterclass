---
module_id: PLAT-024
program: Platform Engineering
level: 1
module_number: 24
title: Pods, Workloads, and Controllers
status: complete
last_verified: 2026-09-02
---

# Pods, Workloads, and Controllers

## One-Page Review

### Governing question

How should a platform choose and configure Kubernetes workload controllers so that pod identity, placement, startup, availability, rollout, completion, disruption, and termination match the application's real operating semantics?

### Essential definitions

- A **Pod** is a disposable API object representing one co-scheduled group of containers that share selected namespaces, storage, lifecycle, and fate.
- A **pod template** is desired metadata and pod specification embedded in a workload resource; a template change normally creates replacement pods rather than mutating existing ones in place.
- A **ReplicaSet** maintains a selected count of interchangeable pod replicas; a **Deployment** manages ReplicaSets and revision rollout for such workloads.
- A **StatefulSet** manages pods with stable ordinal identities and, when configured, persistent-volume claims, plus ordered or parallel lifecycle semantics.
- A **DaemonSet** maintains a pod on every eligible node, or a selected subset, for node-local function.
- A **Job** manages one finite execution toward completion; a **CronJob** creates Jobs according to a schedule and concurrency policy.
- A **probe** is a kubelet diagnostic for startup, readiness, or liveness; each result drives different control behavior.
- **availability** is controller-specific evidence that a pod has remained ready for any required minimum duration; it is not application correctness.
- A **voluntary disruption** is an intentional eviction-compatible interruption such as node drain; an **involuntary disruption** arises from failures or resource pressure.
- A **PodDisruptionBudget (PDB)** constrains qualifying voluntary evictions for selected replicated pods; it does not govern every deletion, rollout, or failure.

### Central model, mechanism, or theorem

Model a workload contract as $W=(J,I,C,P,H,U,D,T,E,X)$: job semantics $J$, identity and persistence $I$, controller $C$, placement $P$, container composition $H$, update strategy $U$, disruption policy $D$, termination/cleanup $T$, outcome evidence $E$, and exceptions $X$. Choose $C$ from semantics: interchangeable continuous replicas, ordered stable members, node-local agents, finite indexed/non-indexed work, or scheduled Job creation. The controller reconciles pod objects, not business outcomes; readiness, availability, completion, and application success require explicit contracts.

### Critical invariants

- Application containers are not created as unmanaged singleton pods when replacement, rollout, completion, or ownership matters.
- A controller selector uniquely and immutably matches its own template labels and does not overlap another controller.
- Pod UID is disposable identity; durable application identity and data never depend on a replaceable pod occurrence unless a StatefulSet contract explicitly supplies stable ordinal semantics.
- Init containers, sidecars, application containers, and ephemeral debugging containers have distinct lifecycle and authority.
- Startup, readiness, and liveness probes answer different questions; liveness never depends on a transient downstream service.
- Rollout budgets are consistent with real capacity, readiness, termination time, topology, and dependency limits.
- Job work is idempotent or deduplicated because retries, replacement, and scheduled overlap can produce more than one execution attempt.
- PDBs protect only qualifying voluntary evictions; controller rollouts, direct deletion, node failure, and resource eviction need separate controls.
- Graceful termination, endpoint removal, drain, durable checkpoint, and forced-kill consequences are tested under the configured deadline.
- Status is interpreted through owner UID, revision, generation, pod conditions, container states, and task-level evidence—not a single `Running` phase.

### Common failures

Using bare pods; selecting Deployment for stable identity; using StatefulSet as a database guarantee; running node agents as Deployments; using CronJob for a continuously running service; overlapping selectors; counting terminating pods as healthy capacity; using liveness for dependency health; omitting startup probes for slow starts; placing setup loops in init containers without bounds; hiding application logic in sidecars; assuming PDBs constrain rollouts; forcing StatefulSet pod deletion during partitions; running non-idempotent Jobs; allowing CronJob overlap; setting impossible rollout budgets; and equating pod `Running` with ready, available, or successful.

### Compact example

A payment API uses a Deployment because replicas are interchangeable. Six desired replicas spread across three zones; `maxUnavailable: 1`, `maxSurge: 2`, `minReadySeconds: 30`, startup/readiness/liveness probes, and a 60-second termination contract reflect measured behavior. A PDB permits one healthy voluntary eviction, while the Deployment's own rolling strategy governs upgrades. The process stops accepting new work when termination begins, drains in-flight requests, checkpoints no pod-local state, and exits before the grace deadline. Status separates updated, ready, available, terminating, and old-revision pods; a synthetic transaction verifies service outcome.

### Connections

Retrieve journey and outcome evidence from [PLAT-011](011-developer-journeys.md) and [PLAT-012](012-time-to-first-successful-deployment.md), declarative ownership and status from [PLAT-023](023-kubernetes-declarative-resources.md), image/process contracts from [PLAT-021](021-container-images-as-platform-artifacts.md), and placement/resource/runtime controls from [PLAT-022](022-runtime-isolation-and-resource-controls.md).

## Governing Question

Is the workload a replaceable continuous service, a stable named member, a node-local facility, finite work, or scheduled creation—and what evidence proves its controller is preserving the intended service under updates, failures, and disruption?

Kubernetes offers several controllers because workloads have different identity and completion semantics. Choosing by a familiar YAML example hides those semantics. A Deployment assumes replaceable replicas. A StatefulSet offers stable ordinal identity but does not create data replication. A Job assumes finite completion and may retry. A DaemonSet follows eligible nodes. A CronJob schedules Jobs but does not guarantee exactly-once business execution.

The platform should turn these distinctions into paved workload classes with validated defaults, observable status, and explicit exceptions.

## Why This Matters

Pods are intentionally disposable. A node fails, an image changes, a probe restarts a container, a controller scales down, or a drain evicts a pod. Durable service comes from a higher-level controller plus application behavior, persistent data, traffic routing, placement, and recovery.

The wrong controller creates subtle failure. A database in a Deployment can reconnect a new pod to the wrong identity. A node agent in a Deployment may leave some nodes uncovered. A non-idempotent CronJob can bill twice after overlapping schedules. A liveness probe coupled to a database can restart every frontend during a database incident and amplify failure.

Controller status also tempts overclaiming. A pod in `Running` phase may have an unready application, a crashing sidecar, or a stuck request. A Deployment can meet replica counts while no transaction succeeds. Workload evidence must join Kubernetes state with application outcomes.

## Prerequisites and Retrieval

Retrieve Kubernetes objects, owner references, selectors, reconciliation, pod scheduling, resources, namespaces, images, signals, storage, service routing, idempotency, distributed membership, batch semantics, availability, and incident response.

You should understand processes, exit codes, retries, timeouts, health diagnostics, graceful shutdown, leader election, replication, queues, cron schedules, failure domains, persistent volumes, and eventual consistency.

## Learning Objectives

After completing this module, you should be able to:

1. explain pod lifetime, container states, phases, conditions, restarts, and replacement;
2. choose Deployment, StatefulSet, DaemonSet, Job, or CronJob from workload semantics;
3. design pod templates, selectors, ownership, composition, placement, resources, and security coherently;
4. distinguish startup, readiness, liveness, availability, completion, and business outcome;
5. configure rollout, partition, completion, retry, schedule, concurrency, disruption, and termination policy;
6. reason about init, sidecar, app, and ephemeral containers without lifecycle confusion;
7. diagnose controller status by UID, revision, generation, owner, and pod/container state; and
8. test update, failure, drain, retry, overlap, node loss, and cleanup behavior proportionately.

## Core Exposition

### Treat the Pod as a disposable execution envelope

A pod groups containers that must be placed together and share a network identity and selected volumes. Containers in a pod can communicate over localhost and coordinate through shared storage. This is tighter coupling than separate services and should reflect one operational fate.

The pod object receives a UID and is scheduled to one node. It is not moved to another node. If replacement is needed, a controller creates another pod with another UID. Names may resemble the old pod, but local writable layer, IP address, process state, and UID are new.

Most production applications should create workload resources, not bare pods. A bare pod lacks a controller that restores count, manages rollout, or records completion. Static pods are a node-level kubelet mechanism with different management and are not a general application path.

### Read pod state precisely

Pod phase is a deliberately small summary: Pending, Running, Succeeded, Failed, or Unknown. `Running` means the pod is bound and at least one container is running, starting, or restarting; it does not mean all containers are ready or useful.

Each container has waiting, running, or terminated state plus previous termination, reason, exit code, restart count, readiness, and started state. `CrashLoopBackOff` is a presentation of repeated restart delay, not a pod phase. Read the actual container state and events.

Pod conditions include scheduling, initialization, readiness to start containers where supported, container readiness, readiness, disruption targeting, and resize states. A custom readiness gate can require an external controller condition. Missing or false gates keep the pod unready.

Interpret status against deletion timestamp, node state, owner UID, workload generation/revision, and freshness. A ready pod already marked for termination is not future capacity.

### Compose containers by lifecycle

**Init containers** run sequentially to successful completion before normal app containers. Use them for bounded initialization that genuinely must precede the app. They can write shared volumes, but repeated failure blocks startup. Make their actions idempotent and time-bounded.

**Sidecar containers** run alongside application containers and support the same pod fate. Native sidecars expressed as restartable init containers have defined startup and reverse termination ordering. They contribute resources and failure modes. Do not use a sidecar when a separately scalable service or node agent is the real boundary.

**Application containers** deliver the pod's primary job. Multiple application containers should be inseparable in placement, scale, update, and ownership. Otherwise split them into separate workloads connected by a service contract.

**Ephemeral containers** are a troubleshooting subresource. They have restricted fields, no normal resource reservation, no probes, and no automatic restart. Their powerful diagnostic access needs RBAC, audit, approved images, runtime security, time bounds, and incident procedure; they are not an application extension mechanism.

### Design startup, readiness, and liveness probes

A startup probe asks whether initialization has completed. While it has not succeeded, liveness and readiness do not run. Size its failure threshold and period for realistic worst-case startup without masking permanent failure indefinitely.

A readiness probe asks whether this container should currently receive normal service traffic or count ready for relevant controllers. It may fail during warmup, overload, dependency loss, leadership change, or drain. Readiness should be cheap, local enough to avoid correlated failure, and representative of the operation being routed.

A liveness probe asks whether restarting the container is a reasonable recovery. It should detect irrecoverable local deadlock or corruption, not a temporary downstream outage. Restarting on dependency failure increases load and destroys useful diagnostics.

Probe timeout, period, thresholds, and implementation are a control loop. Account for CPU starvation and node pressure. An `exec` probe consumes process/container resources; HTTP/TCP/gRPC probes have network and protocol semantics. Protect probe endpoints from exposing sensitive internals.

### Choose Deployment for interchangeable continuous replicas

A Deployment manages ReplicaSets and rolling revision. Its pod selector must match template labels and remain disjoint from other controllers. ReplicaSets adopt matching eligible pods, so accidental overlap is ownership corruption, not harmless metadata.

Use a Deployment when any healthy replica can replace another and durable identity/data live outside pod occurrence. Configure desired replicas, template, update strategy, progress deadline, minimum ready duration, and revision retention.

RollingUpdate allows extra new pods through `maxSurge` and permits unavailable desired replicas through `maxUnavailable`. Values can be counts or percentages with rounding semantics. `Recreate` removes old pods before new creation and produces downtime unless another layer supplies service.

Capacity planning includes desired plus surge, terminating pods, resource requests, topology, quotas, provider limits, connections, and downstream load. A surge pod can remain scheduled while an old pod drains. Verify node and dependency capacity for the peak, not just steady state.

Pausing a rollout lets multiple template changes accumulate without progressing them. A progress deadline reports stalled progress; it does not automatically roll back. Rollback selects a retained Deployment revision and still performs a rollout, so forward/backward data compatibility remains necessary.

### Separate revision status from service success

Deployment status reports replicas, updated replicas, ready replicas, available replicas, unavailable replicas, and conditions. These counts have different meanings. Updated uses the current template revision; ready follows pod readiness; available requires readiness for any `minReadySeconds`.

The following synthetic inventory makes those distinctions visible.

<!-- bijux-verify: {"id":"workload-rollout-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"pods=7\nowned=6\ncurrent_revision=4\nupdated_ready=3\nold_ready=1\nterminating=1\norphan=1\nserving_candidates=4\n","stderr":""}} -->
```python
pods = [
    {"name": "api-a", "owner": "deploy-u1", "revision": 4, "ready": True, "deleting": False},
    {"name": "api-b", "owner": "deploy-u1", "revision": 4, "ready": True, "deleting": False},
    {"name": "api-c", "owner": "deploy-u1", "revision": 4, "ready": True, "deleting": False},
    {"name": "api-d", "owner": "deploy-u1", "revision": 4, "ready": False, "deleting": False},
    {"name": "api-old", "owner": "deploy-u1", "revision": 3, "ready": True, "deleting": False},
    {"name": "api-drain", "owner": "deploy-u1", "revision": 3, "ready": False, "deleting": True},
    {"name": "api-orphan", "owner": None, "revision": 4, "ready": True, "deleting": False},
]
owned = [pod for pod in pods if pod["owner"] == "deploy-u1"]
current = [pod for pod in owned if pod["revision"] == 4]
serving = [pod for pod in owned if pod["ready"] and not pod["deleting"]]
print(f"pods={len(pods)}")
print(f"owned={len(owned)}")
print(f"current_revision={len(current)}")
print(f"updated_ready={sum(pod['ready'] and not pod['deleting'] for pod in current)}")
print(f"old_ready={sum(pod['revision'] != 4 and pod['ready'] and not pod['deleting'] for pod in owned)}")
print(f"terminating={sum(pod['deleting'] for pod in owned)}")
print(f"orphan={sum(pod['owner'] is None for pod in pods)}")
print(f"serving_candidates={len(serving)}")
```

“Serving candidate” here uses readiness and deletion only. It does not prove EndpointSlice membership, minimum readiness duration, network reachability, application correctness, or user success.

### Choose StatefulSet for stable ordinal members

StatefulSet supplies each pod an ordinal, stable pod name/network identity, and stable volume-claim association when templates are configured. Replacement of `db-2` remains ordinal 2 and can attach its claim; the pod UID still changes.

Use it when the application understands member identity, ordered lifecycle, persistent storage, or partitioned update. The application must implement replication, consensus, sharding, backup, restore, fencing, and data compatibility. Kubernetes does not infer them.

Default `OrderedReady` creation proceeds in ordinal order and scaling down reverses order. `Parallel` relaxes ordering for applications that do not require it. A broken lower ordinal can block progress by design.

Rolling updates normally replace highest ordinals first and wait for readiness/minimum ready duration. A partition holds lower ordinals on the old revision for canary or staged rollout. `OnDelete` requires manual deletion to update pods. Inspect current and update revisions, not image tags alone.

Persistent claims commonly survive scale-down and deletion according to retention policy. This protects data but leaves lifecycle obligations and cost. Never force-delete a StatefulSet pod during uncertain node partition without understanding duplicate-member and storage-attachment risk.

### Choose DaemonSet for node-local function

DaemonSet reconciles one pod per eligible node, not a global replica count. Use it for networking, storage, telemetry, security, or device functions whose value exists on each target node.

Eligibility comes from node selector/affinity, taints/tolerations, architecture, OS, devices, and policy. The controller targets individual nodes and Kubernetes supplies special tolerations for important node conditions. This can keep critical agents present but also places them on impaired nodes; resources and failure behavior matter.

Configure rolling update availability/surge as supported, priority, resources, host access, and termination. A privileged node agent has node blast radius and belongs in a distinct platform-owned class. Measure coverage as ready/current pods over eligible nodes, with exclusions and node state visible.

### Choose Job for finite work

A Job represents completion, not perpetual availability. It creates pods until the required successes occur or failure policy stops further work. Pod restart policy is `Never` or `OnFailure`; container restart and pod replacement affect attempt visibility differently.

Use non-parallel Jobs for one logical task, work-queue parallelism for consumers drawing idempotent items, or indexed completion when each index has distinct work. Define completions, parallelism, active deadline, backoff, per-index behavior where used, success policy, pod failure policy, and cleanup.

At-least-once attempts are a practical expectation under retries and unknown outcomes. Use business idempotency keys, transactional claim/checkpoint, or deduplication. A pod exit code 0 proves process completion under its contract, not that every external side effect occurred exactly once.

Classify failures: retryable infrastructure, retryable business contention, permanent input, code defect, cancellation, deadline, or duplicate. Avoid retry storms. Preserve failed pod/log evidence long enough to diagnose while using TTL cleanup to avoid unbounded objects.

### Choose CronJob for scheduled Job creation

CronJob evaluates a schedule and creates Jobs. It does not make the business operation exactly once. Controller downtime, delayed scheduling, clock/time-zone rules, and concurrency can cause missed, late, or overlapping executions under documented semantics.

Set time zone when required, starting deadline, concurrency policy (`Allow`, `Forbid`, or `Replace`), suspension, and history limits. `Forbid` skips overlapping starts rather than queueing an infinite backlog. `Replace` terminates the current Job before a new one and is unsafe for non-resumable work.

Every scheduled execution needs a logical occurrence key derived from the intended schedule time, not only creation time. The application records completion idempotently so duplicate Jobs do not duplicate billing, notifications, or destructive maintenance.

### Place pods across real failure domains

Requests and hard constraints filter feasible nodes; scoring chooses among them. Node selectors/affinity express hardware, OS, zone, compliance, and workload class. Taints repel pods without matching tolerations. A toleration permits consideration; it does not force placement.

Topology spread constraints distribute matching pods across labeled domains. The pod must match its own selector, and node labels must be complete and trustworthy. Hard `DoNotSchedule` improves distribution guarantees but can leave pods pending when domains lack capacity. Soft `ScheduleAnyway` preserves placement but can concentrate risk.

Anti-affinity can separate replicas but is expensive at large scale and may deadlock constrained clusters. Prefer topology spread for common replica distribution. Stateful quorum placement needs application-aware failure-domain and storage analysis, not only equal counts.

Scheduling is not continuous rebalancing. A topology can become skewed after scale-down or node changes. Decide whether natural replacement, descheduling, or manual action should repair it.

### Design disruption policy accurately

Replicate applications that must survive a pod or node loss and spread replicas across independent domains. Requests prevent avoidable resource eviction; priority and preemption express consequence but do not create capacity.

A PDB selects pods and computes allowed voluntary disruptions against intended replicas and current health. Use either `minAvailable` or `maxUnavailable`. It influences clients that use the Eviction API, such as a respectful drain. Direct pod/deployment deletion and workload-controller rollouts are not constrained by it. Involuntary disruptions cannot be prevented, though they reduce healthy count.

Avoid a PDB that makes node maintenance impossible. Quorum systems must calculate safe availability from real membership; single-replica services cannot promise uninterrupted drain. Configure unhealthy-pod eviction policy so a permanently unready pod does not wedge maintenance without adding availability.

Test concurrent zone loss plus drain, not only one eviction from a healthy cluster. Maintenance objectives must include the time to reschedule, attach storage, start, warm, and become available.

### Make termination part of correctness

On pod deletion, Kubernetes marks termination and begins graceful shutdown. Service endpoint state changes so terminating pods do not receive normal new traffic. The kubelet runs `preStop` when configured, sends the stop signal, waits within the grace period, and ultimately force-kills remaining processes.

The application should observe termination, stop accepting new work, fail readiness or use endpoint terminating/serving semantics appropriately, drain, checkpoint or release leases, flush bounded data, and exit. The grace period includes hook and process shutdown; size it from measured worst-case behavior and upstream deadlines.

Container PID 1 must handle and reap signals correctly. A shell wrapper can swallow signals. Sidecars with native lifecycle remain until main containers terminate, then stop in reverse definition order; do not improvise fragile `preStop` ordering when native semantics fit.

Force deletion removes the API object without waiting for confirmation that node processes stopped. It can create duplicate stateful members or work. Use it only with node fencing, storage and membership knowledge, and explicit authority.

### Coordinate rollout with dependencies and data

Pod controller rollback does not roll back schemas, messages, caches, secrets, or external effects. Use expand/contract data evolution, backward/forward-compatible protocols, feature flags, and staged provider changes. Every old/new combination present during surge and drain must be supported.

Readiness can gate traffic but cannot make an incompatible rollout safe. A canary needs distinct traffic or task evidence, sufficient exposure, abort rules, and comparable baseline. Stateful partitions need data/leadership evidence per ordinal.

Set progress deadlines longer than legitimate placement, image pull, startup, readiness, and minimum-ready delay, but short enough to alert. Automation may pause or roll back only when backward transition is safe and evidence is unambiguous.

### Observe the full workload hierarchy

Trace Deployment to ReplicaSet to Pod to container and image digest; StatefulSet/DaemonSet directly to pods; CronJob to Job to pods. Verify owner UIDs and selectors. Orphans, adopted pods, duplicate controllers, and terminating lag change counts.

Observe desired/current/updated/ready/available/unavailable/terminating replicas, revision, generation, scheduling latency, image pull, init duration, startup/readiness/liveness results, restarts, exit reasons, throttling/OOM, termination duration, disruption allowance, Job active/succeeded/failed indexes, and CronJob intended versus actual schedule time.

Join these with service traffic, errors, latency, queue age, data health, and user task outcomes. Kubernetes evidence locates control behavior; application evidence proves useful work.

### Test controller behavior under failure

Test selector isolation, no-op reconciliation, update and rollback, insufficient surge capacity, unready canary, probe dependency failure, slow startup, sidecar failure, stuck init, SIGTERM and SIGKILL, node loss, drain/PDB, storage reattachment, duplicate Job attempt, partial side effect, CronJob overlap, controller restart, and garbage collection.

Record cluster version and feature gates. Workload behavior evolves: sidecar semantics, pod conditions, Job policies, StatefulSet update fields, and scheduling features have version requirements. Stable paved paths use supported features; alpha behavior needs explicit channel and rollback.

## Definitions and Notation

Let workload contract $W=(J,I,C,P,H,U,D,T,E,X)$ have the components defined in the review. Let desired replicas be $N$, maximum surge $S$, and maximum unavailable $U$. A Deployment rollout may transiently target up to $N+S$ non-terminated pods while requiring controller-defined availability of at least $N-U$, subject to rounding and current API semantics.

Let pod $p$ have owner UID $o(p)$, template revision $r(p)$, readiness $R(p,t)$, availability $A(p,t)$, and deletion marker $\delta(p,t)$. Generally $A(p,t)$ implies sustained readiness under controller rules, while readiness alone does not imply availability or business success.

For Job occurrence $k$, let attempt set be $B_k$. Business exactly-once effect is not implied by $\sum_{b\in B_k}\mathbf{1}[\operatorname{exit}(b)=0]\ge1$. External idempotency or deduplication must establish effect uniqueness.

Let eligible topology domains be $Z$ and matching pod count in domain $z$ be $n_z$. Spread skew is $\max_{z\in Z}n_z-\min_{z\in Z}n_z$ under the API's eligibility rules; incomplete labels or selectors change $Z$ or the counted set.

## Mechanisms, Invariants, or Proof Structure

The workload path is job semantics $\rightarrow$ controller selection $\rightarrow$ pod template/composition $\rightarrow$ identity/storage $\rightarrow$ resources/security/placement $\rightarrow$ probes $\rightarrow$ rollout or completion policy $\rightarrow$ disruption/termination $\rightarrow$ controller and application evidence $\rightarrow$ update, retry, recovery, or retirement.

Controller hierarchy provides level-based reconciliation: workload desired state creates or adopts owned pods; kube-scheduler binds unscheduled pods; kubelet runs containers and reports state; endpoint controllers and traffic systems react to readiness/deletion; garbage collection removes owned API dependents.

Invariants are controlled pod ownership, disjoint selectors, correct identity semantics, explicit container lifecycle roles, probe separation, feasible rollout capacity, idempotent finite work, bounded disruption claims, tested termination, and multi-layer evidence.

No controller proves application availability or exactly-once effects. Those claims require application, storage, network, dependency, and user-outcome evidence under stated failure assumptions.

## Alternatives and Trade-Offs

**One versus multiple containers per pod:** co-location simplifies localhost and shared-volume coordination but couples scale, placement, update, security, and fate. Split independently owned or scaled functions.

**Deployment versus StatefulSet:** Deployment maximizes replacement freedom; StatefulSet supplies stable ordinals and lifecycle at operational cost. State alone does not automatically require StatefulSet if it lives in an external service.

**Sidecar versus shared service/DaemonSet:** sidecars customize per-pod behavior and fate but multiply resources and rollout complexity. Shared services scale independently; DaemonSets fit node-local functions.

**RollingUpdate versus Recreate:** rolling preserves capacity but runs mixed revisions and needs surge. Recreate avoids overlap but incurs downtime and does not solve data rollback.

**Ordered versus parallel StatefulSet:** ordering supports membership dependencies but slows recovery/update and can wedge behind one member. Parallel suits independent ordinals.

**Container restart versus pod replacement:** `OnFailure` can retain pod-local context but hides attempt boundaries; `Never` exposes Job pod attempts. Choose for diagnostic and idempotency needs.

**Hard versus soft topology:** hard rules preserve placement properties but risk Pending pods; soft rules favor availability but can concentrate failure risk.

**Strict PDB versus maintainability:** tighter budgets reduce voluntary simultaneous loss but can block drain. Replication, unhealthy eviction, and tested replacement time are the durable solution.

## Failure Modes and Misconceptions

- **“A Pod is a small VM.”** It is a disposable process envelope with shared namespaces and node fate.
- **“Running means healthy.”** Read container states, readiness, availability, and application outcomes.
- **“StatefulSet makes software stateful.”** It supplies identity/storage associations; the application owns replication and consistency.
- **“A probe endpoint is one health check.”** Startup, readiness, and liveness drive different actions and need different evidence.
- **“PDB protects every outage.”** It constrains qualifying voluntary evictions, not rollout, deletion, or involuntary failure.
- **“Cron means once per schedule.”** Delays, overlap, retries, and duplicate creation require occurrence idempotency.
- **“Successful Job means exactly once.”** Multiple attempts can produce external effects before one reports success.
- **“Surge is free.”** It consumes nodes, quotas, connections, licenses, and dependency capacity while old pods drain.
- **“Force deletion stops a pod.”** It can remove API identity before node execution stops.
- **“Anti-affinity guarantees availability.”** It depends on labels, domains, capacity, and correlated infrastructure failure.
- **“Rollback restores the system.”** Controller revision rollback does not reverse data or external effects.
- **“Sidecars are invisible plumbing.”** They share resource, security, lifecycle, and failure budgets with the app.

## Worked Examples

### Example 1

A three-replica API uses startup for cache warmup, readiness for serving ability, and liveness only for local deadlock. Database outage fails readiness but not liveness, avoiding restart amplification.

### Example 2

A Deployment selector overlaps an older ReplicaSet outside its ownership tree. Admission blocks the rollout before adoption changes replica counts.

### Example 3

A database member needs stable ordinal and volume but implements its own quorum and fencing. StatefulSet supplies identity; the database protocol supplies safety.

### Example 4

A log collector must observe every eligible node. A DaemonSet with node-class selectors and bounded host access replaces a Deployment that left new nodes uncovered.

### Example 5

An indexed Job processes 100 shards. Each shard commits with occurrence/index idempotency, so pod retry after an unknown network outcome does not duplicate records.

### Example 6

A nightly invoice CronJob uses `Forbid` and a scheduled-occurrence key. A late duplicate Job sees the completed occurrence and exits without invoicing again.

### Example 7

A six-replica rollout allows one unavailable and two surge pods, but the namespace quota has no surge capacity. Preflight validation blocks it rather than waiting for a progress deadline.

### Example 8

A PDB allows one voluntary disruption, while a simultaneous zone failure already removes two replicas. Drain waits; operators restore capacity in another zone before continuing maintenance.

### Example 9

A pod needs 45 seconds to drain. A 60-second grace period and measured endpoint removal succeed; a forced deletion test demonstrates duplicate in-flight work and is reserved for fenced emergencies.

### Example 10

An ephemeral debugger image would add broad capabilities. Admission limits it to incident responders, a signed image, sandboxed runtime, audit, and a time-bounded case instead of weakening the workload template.

## Cross-Program Connections

Operating systems contributes processes, signals, exit status, namespaces, scheduling, and termination. Distributed systems contributes replica identity, membership, retries, leader/quorum behavior, partial failure, and idempotency. Reliability contributes probes, availability, rollout, disruption, drain, load shedding, and recovery.

Data engineering contributes durable state, checkpoints, shard identity, migrations, and exactly-once limitations. Security contributes workload identity, debug authority, admission, host access, and supply-chain identity. Performance contributes resource requests, warmup, surge capacity, topology, and tail latency.

Product engineering contributes consumer outcomes and safe defaults. API engineering contributes controller resources, status, selectors, ownership, versions, and errors. Organizational design assigns application, platform, node, storage, and incident authority.

## References

- Kubernetes Project, [*Pods and Workloads*](https://kubernetes.io/docs/concepts/workloads/), current documentation retrieved September 2, 2026. Pod abstraction and Deployment, StatefulSet, DaemonSet, Job, CronJob, and extension selection.
- Kubernetes Project, [*Pod Lifecycle*](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/), current documentation retrieved September 2, 2026. Pod phases, container states, conditions, restart behavior, probes, termination, stop signals, sidecar ordering, and garbage collection.
- Kubernetes Project, [*Liveness, Readiness, and Startup Probes*](https://kubernetes.io/docs/concepts/workloads/pods/probes/), updated 2026. Probe purposes, handlers, configuration, readiness effects, startup gating, and cascading-failure cautions.
- Kubernetes Project, [*Deployments*](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), current documentation retrieved September 2, 2026. ReplicaSets, selectors, rolling/recreate strategies, surge/unavailable budgets, progress, revisions, pause, and rollback.
- Kubernetes Project, [*StatefulSets*](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/), current documentation retrieved September 2, 2026. Ordinals, stable identity/storage, management policy, scaling, rolling/partitioned updates, and retention.
- Kubernetes Project, [*DaemonSet*](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/), current documentation retrieved September 2, 2026. Eligible-node coverage, scheduling, affinity, tolerations, priority, updates, and alternatives.
- Kubernetes Project, [*Jobs*](https://kubernetes.io/docs/concepts/workloads/controllers/job/), current documentation retrieved September 2, 2026. Completion, parallelism, indexed work, retries/backoff, failure/success policy, deadlines, suspension, and cleanup.
- Kubernetes Project, [*CronJob*](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/), current documentation retrieved September 2, 2026. Schedules, time zones, starting deadlines, concurrency, suspension, history, and duplicate/late execution limits.
- Kubernetes Project, [*Init Containers*](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/), current documentation retrieved September 2, 2026. Sequential completion, restart behavior, resource calculation, probes, and app-container startup.
- Kubernetes Project, [*Sidecar Containers*](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/), current documentation retrieved September 2, 2026. Native sidecar startup, restart, readiness, resource accounting, Jobs, and termination order.
- Kubernetes Project, [*Disruptions*](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/), current documentation retrieved September 2, 2026. Voluntary/involuntary disruption, PDB calculation and limits, Eviction API, unhealthy pods, and owner discovery.
- Kubernetes Project, [*Pod Topology Spread Constraints*](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/), current documentation retrieved September 2, 2026. Domains, skew, hard/soft behavior, selectors, node inclusion policy, defaults, and limitations.

## Exercises

### Exercise 1

Choose controllers and define workload contracts for a stateless API, replicated database, node security agent, 500-shard transformation, and hourly billing run. Justify identity, probes, updates, retries, disruption, and evidence.

### Exercise 2

Design a six-replica Deployment rollout across three zones. Include selectors, topology, resources, startup/readiness/liveness, surge/unavailable, minimum ready time, progress deadline, PDB, termination, canary evidence, and rollback limits.

### Exercise 3

Diagnose a status showing desired 10, current 12, updated 6, ready 8, available 7, unavailable 3, two terminating pods, repeated liveness failures, and no rollout progress.

### Exercise 4

Design a Job/CronJob execution contract that tolerates duplicate attempts, controller downtime, overlap, cancellation, partial external effects, poison inputs, and evidence cleanup.

### Exercise 5

Transfer the controller model to autonomous warehouse robots. Address disposable execution, durable robot identity, per-zone agents, finite picking work, scheduled maintenance, health, placement, disruption, safety stops, and human authority.

## Answers to the Exercises

### Answer 1

The API uses a Deployment: replicas are interchangeable, state is external, startup/readiness/liveness are separate, rolling capacity and drain are measured, and a PDB covers maintenance. The database uses a StatefulSet only because ordinal identity and volume claims matter; its replication, quorum, fencing, backup, and data compatibility remain application contracts. The security agent uses a DaemonSet over eligible nodes with platform-owned privileged runtime policy and coverage evidence. The transformation uses an indexed Job with 500 completions, bounded parallelism, per-index idempotency/checkpoint, failure policy, active deadline, and retained diagnostics. Hourly billing uses CronJob to create Jobs with explicit time zone, starting deadline, `Forbid` unless replacement is proven safe, and occurrence-key deduplication. Evidence distinguishes pod/controller state from API transaction, database health, node coverage, shard completion, and billed occurrence.

### Answer 2

Use one immutable selector matching template identity labels and no peer controller. Request capacity that permits six steady replicas plus two surge pods across namespace and node quotas. Spread matching pods with max skew one over zones and preferably hosts, while defining behavior if a zone lacks capacity. Startup covers worst-case initialization; readiness tests local serving and required dependencies without expensive fan-out; liveness detects only locally unrecoverable state. Set `maxSurge: 2`, `maxUnavailable: 1`, minimum-ready time long enough to expose warm failures, and progress deadline beyond pull/schedule/start/minimum-ready tails. A PDB allows one healthy voluntary eviction but is not claimed to constrain rollout. On termination, stop admission, drain, release leases, and exit within measured grace. Canary evidence includes revision-specific traffic, errors, latency, saturation, and synthetic task outcome. Rollback is permitted only while schemas/protocols/external effects remain backward compatible; otherwise pause and forward-fix.

### Answer 3

First bind every pod by owner UID, revision, deletion timestamp, node, and condition. Twelve current pods can be desired ten plus surge and terminating lag; do not count the two terminating as future capacity. Six updated means six still old or terminating. Eight ready but seven available suggests one has not satisfied minimum-ready duration. Three unavailable is consistent with desired minus available, but inspect current API semantics rather than deriving blindly. Repeated liveness failures may restart new pods before they become available, so compare startup gating, probe timeouts, CPU pressure, downstream coupling, exit/restart state, and revision. Check Pending reasons, quota/topology, image pull, init/sidecars, progress deadline, ReplicaSet events, and EndpointSlices. Pause rollout if harm continues, repair probe or application behavior, restore capacity, and only roll back if data/protocol compatibility permits. Do not “fix” by raising every threshold without reproducing the failure.

### Answer 4

Assign each logical occurrence a durable key from job purpose, schedule time, and shard/index. Before an external effect, atomically claim or check that key; record stages so retries resume or compensate. Job attempts are disposable and bounded by parallelism, deadlines, backoff, per-index failure policy, and poison-input quarantine. CronJob specifies time zone, starting deadline, concurrency policy, and suspension; controller downtime can cause a late start, while a duplicate sees the completed key and exits. Cancellation marks the occurrence and makes workers stop safely; it does not merely delete pods while effects continue. Unknown provider outcome is queried by idempotency key before retry. Retain Job/pod/log and business ledger evidence through an audit window, then use TTL/history cleanup. Completion requires intended items and external commitments reconciled, not one pod exit code.

### Answer 5

Treat a process controlling one robot session as disposable, but bind durable robot identity to hardware credentials and inventory, not process occurrence. A fleet controller assigns desired software and mission policy; a stable-member controller model fits robots whose individual identity and charging/storage state persist. Per-zone safety/network agents resemble DaemonSets over eligible zones or gateways. Picking orders are finite Jobs with order/item idempotency, checkpoint, cancellation, and reassignment rules. Maintenance scheduling resembles CronJob creation but uses durable occurrence records and avoids overlap. Startup proves sensors and calibration; readiness permits accepting work; liveness restarts only locally wedged software and never masks unsafe hardware. Placement respects physical zone, battery, load, and exclusion domains. Disruption drains the robot to a safe stop before update; emergency stop bypasses normal availability targets under named safety authority. Human operators retain override, incident, and workplace-safety authority. Controller status never proves a route is safe without physical sensing and domain validation.
