---
module_id: PLAT-029
program: Platform Engineering
level: 1
module_number: 29
title: Health, Readiness, and Lifecycle
status: complete
last_verified: 2026-09-02
---

# Health, Readiness, and Lifecycle

## One-Page Review

### Governing question

How should a platform distinguish startup, local liveness, traffic readiness, dependency capability, disruption, and termination so automation recovers failures without causing restart storms, traffic loss, corrupt work, or unsafe shutdown?

### Essential definitions

- A **startup probe** determines whether a container has completed startup; while it has not succeeded, kubelet suppresses that container's liveness and readiness probes.
- A **liveness probe** asks whether restarting this container is an appropriate recovery for a locally stuck condition.
- A **readiness probe** asks whether a running container should presently receive ordinary traffic or participate as ready; failure does not restart it.
- A **Pod condition** is typed status with `True`, `False`, or `Unknown` plus reason, message, and transition time.
- A **readiness gate** adds an external/custom Pod condition that must be `True`, together with container readiness, for the Pod `Ready` condition to be true.
- A **lifecycle hook** is kubelet-triggered `PostStart` or `PreStop` handling; hook delivery can occur more than once and must be idempotent.
- **termination grace** is the bounded interval shared by `PreStop` execution and process shutdown before forcible termination.
- **draining** stops admission of new work and completes, transfers, checkpoints, or safely abandons accepted work before termination.
- A **terminating endpoint** represents a pod with deletion initiated; its EndpointSlice `ready` is false while `serving` may remain true for drain-aware consumers.
- A **PodDisruptionBudget (PDB)** limits simultaneous unavailability through cooperating voluntary eviction operations; it is not a universal availability guarantee.
- **restart policy** controls kubelet response to container exit; controller replacement and pod recreation are separate recovery layers.

### Central model, mechanism, or theorem

Model lifecycle assurance as $L=(S,V,R,D,A,H,T,E,P,O,X)$: startup $S$, liveness $V$, readiness $R$, dependency/degraded capability $D$, accepted-work accounting $A$, hook/signal behavior $H$, termination/drain $T$, endpoint propagation $E$, disruption policy $P$, observations $O$, and declared exceptions $X$. For a pod $p$, traffic eligibility is a conjunction of container readiness, every readiness gate, Service selection, endpoint-controller state, data-plane propagation, and consumer behavior. Safe termination requires new work to stop, outstanding work to reach a safe boundary, state to flush or transfer, and processes to exit within grace; no single probe or hook proves the sequence.

### Critical invariants

- Startup, liveness, readiness, dependency capability, and business correctness have separate predicates and failure actions.
- Liveness depends only on evidence that a container-local restart can improve; shared dependency, overload, or node/network failure does not trigger synchronized restarts.
- Readiness is cheap, bounded, side-effect-free, and answers traffic safety; it never performs migrations, repairs, large fan-out, or unbounded dependency work.
- Startup budget covers measured cold-start and recovery tails without weakening steady-state liveness detection.
- Readiness gates have one authoritative controller, explicit absence/Unknown behavior, bounded update latency, observed generation/version, and cleanup.
- Every hook and signal handler is idempotent, bounded, observable, and correct if repeated, delayed, skipped by catastrophic failure, or cut off at grace expiry.
- The grace interval includes endpoint propagation, `PreStop`, application drain, sidecar ordering, state flush, and uncertainty; `PreStop` sleep is never mistaken for proof that traffic stopped.
- Readiness loss and deletion are propagated asynchronously, so applications reject or redirect new work after entering drain even if stale clients still connect.
- Rollout, scale-down, eviction, preemption, node pressure, node loss, direct deletion, and process failure are tested as distinct lifecycle paths.
- PDB, replica count, topology, surge/unavailable settings, workload protocol, and real readiness jointly protect availability; none substitutes for the others.

### Common failures

Using one `/health` result for all probes; checking a shared database in liveness; setting liveness thresholds below normal pause or overload; omitting startup probes for slow applications; making readiness call every dependency; returning ready before cache/schema/listener initialization; using readiness as an alert; treating a TCP accept as functional health; running expensive `exec` probes; ignoring probe timeouts and concurrency; relying on `PreStop` alone to remove traffic; spending all grace sleeping; handling SIGTERM in a non-PID-1 child; assuming hooks run exactly once or always run; expecting PDB to stop direct deletion or involuntary failure; and declaring graceful shutdown without checking accepted-work loss.

### Compact example

A payments API has a startup probe that permits measured cold recovery, a liveness endpoint that checks its event loop and immutable local invariants, and a readiness endpoint that verifies listener, current configuration, credential freshness, queue headroom, and ability to provide the advertised API without fan-out to every downstream dependency. A cloud-load-balancer controller owns an external registration readiness gate. On deletion, the process observes SIGTERM, atomically stops accepting new operations, reports not ready, returns retry guidance on stale connections, drains bounded idempotent requests, checkpoints durable work, and exits. Endpoint status, gateway drain, `PreStop`, native sidecar shutdown, and a 75-second grace budget are tested under rollout, drain, preemption, and forced kill. Metrics record probe cause, effective readiness, gate version, active work, drain duration, forced exits, and user outcomes without making the probe itself expensive.

### Connections

Retrieve controller rollout and pod identity from [PLAT-024](024-pods-workloads-and-controllers.md), endpoint conditions and connection drain from [PLAT-025](025-services-and-ingress.md), configuration/credential reload from [PLAT-026](026-configuration-and-secrets.md), state flush/fencing from [PLAT-027](027-storage-and-stateful-workloads.md), and scheduling/preemption/eviction from [PLAT-028](028-scheduling-and-placement.md). Reliability, distributed-systems, API, operating-systems, and testing programs supply failure and verification methods.

## Governing Question

What question does each lifecycle signal answer, which component acts on it, what recovery does failure trigger, how quickly and reliably does state propagate, and what evidence proves a workload safely started, served, degraded, drained, stopped, and recovered?

Kubernetes exposes several overlapping-looking mechanisms because they control different state machines. Kubelet probes containers. Pod conditions aggregate readiness and setup. Endpoint controllers project readiness into traffic destinations. Workload controllers replace pods. PDBs mediate certain eviction calls. Processes receive hooks and signals. Proxies and clients cache or reuse connections.

A platform must preserve those distinctions. “Healthy” is too vague to drive automation: the same dependency outage might justify degraded responses, readiness withdrawal, no restart, alerting, or regional failover depending on the contract.

## Why This Matters

Health automation can amplify failure. If every replica restarts because a shared database times out, remaining capacity shrinks and recovery load rises. If readiness fan-out overloads dependencies, the detector becomes the incident. If liveness kills a process during a long garbage-collection pause or migration, it can create a permanent restart loop.

Lifecycle mistakes lose work. Endpoint removal, load-balancer propagation, signal delivery, application drain, connection lifetime, state flush, and sidecar shutdown are concurrent or ordered only under specific rules. A fixed sleep can appear safe in a small test while stale proxies or long requests exceed it in production.

Clear contracts also make debugging faster. Pending scheduling, sandbox setup, image pull, startup, readiness, liveness restart, crash, OOM, eviction, deletion, and forced kill have different evidence and owners. Collapsing them into “pod down” hides the repair.

## Prerequisites and Retrieval

Retrieve processes, PID 1, Unix signals, exit codes, timeouts, retries, idempotency, files and sockets, HTTP/TCP/gRPC, queues, transactions, checkpoints, connection pools, load balancers, eventual consistency, pods, containers, Services, EndpointSlices, controllers, rollout, disruption, resource pressure, and observability.

You should distinguish detection from diagnosis, traffic eligibility from process existence, local failure from dependency failure, container restart from pod replacement, graceful deletion from sudden node loss, accepted from completed work, and a control-plane condition from end-to-end user success.

## Learning Objectives

After completing this module, you should be able to:

1. define separate startup, liveness, readiness, dependency, degradation, and business-success predicates;
2. choose HTTP, TCP, gRPC, or exec probes and tune delay, interval, timeout, success/failure thresholds, and termination grace;
3. interpret pod phases, container states, restart reasons, built-in conditions, readiness gates, and EndpointSlice conditions;
4. implement idempotent PostStart/PreStop hooks, PID-1 signal handling, stop signals, and native sidecar lifecycle;
5. budget safe termination across traffic propagation, work drain, checkpoint, process exit, and forcible shutdown;
6. combine PDBs, replica/topology capacity, rollout policy, eviction behavior, and application protocols;
7. observe lifecycle transitions without turning probes into heavy diagnostic systems; and
8. test and diagnose restart loops, never-ready pods, stuck termination, traffic loss, and disruption failure by layer.

## Core Exposition

### Define state predicates before mechanisms

Write one sentence per predicate:

- **Started:** initialization that must precede steady checks has completed.
- **Live:** the local process can make progress, or a restart is the right recovery.
- **Ready:** this instance can safely accept its advertised class of new work now.
- **Capable:** dependencies and credentials permit a named operation or degraded mode.
- **Correct:** representative business work produces the required outcome.
- **Draining:** no new ordinary work is admitted and accepted work is converging to a safe boundary.
- **Terminated safely:** no acknowledged work was silently lost and state/ownership is consistent.

Attach an actor and action. Startup/liveness failure can restart a container. Readiness failure changes traffic eligibility. Dependency signals may shed features or trip circuit breakers. Business checks may page or stop rollout. Drain controls admission and completion. Do not let one Boolean perform all actions.

### Understand pod and container state boundaries

Pod phase (`Pending`, `Running`, `Succeeded`, `Failed`, `Unknown`) is a coarse summary, not a complete lifecycle. A Running pod can be unready, crash-looping one container, or serving errors. Inspect container `Waiting`, `Running`, and `Terminated` states, last termination reason/exit code/signal, restart count, and timestamps.

Built-in conditions separate `PodScheduled`, `PodReadyToStartContainers`, `Initialized`, `ContainersReady`, `Ready`, and disruption/resize states. Sandbox, network, volumes, and dynamic resources precede container creation under the current readiness-to-start semantics. Image pull and application startup occur later.

Controllers create replacement pods; kubelet restarts containers within a bound pod according to restart policy. A pod is not moved to another node. Node loss causes controller replacement after control-plane detection, while local processes may have uncertain fate under partition.

### Use startup probes for slow or variable initialization

A startup probe protects a slow-starting container from steady-state liveness and readiness. Until startup succeeds, kubelet does not execute the other two for that container. If startup reaches its failure threshold, kubelet stops/restarts the container according to policy.

The nominal startup failure window is influenced by initial delay, period, timeout, and failure threshold. Choose it from measured cold image/filesystem/cache/database recovery, schema checks, replay, JIT, and dependency conditions under load—not the median developer laptop start.

Startup should check irreversible local progress prerequisites, not wait forever for an optional shared dependency. Separate “still progressing,” “locally stuck,” and “dependency unavailable.” Initialization that cannot be safely repeated needs external idempotency and ownership, because container/pod restart can replay it.

Do not compensate for missing startup design with an enormous liveness initial delay. That delays detection after every steady-state restart and cannot express startup progress clearly.

### Make liveness conservative and local

Liveness asks whether killing and restarting this container is likely to improve availability. Appropriate signals include a deadlocked event loop, irrecoverable internal invariant, lost worker supervision, or a local subsystem that cannot be reinitialized in process.

Do not make liveness require database, DNS, identity provider, peer quorum, object storage, or every dependency. Their outage affects all replicas; synchronized restarts destroy warm state, generate connection storms, and hide the root cause.

High CPU, queue depth, latency, or overload generally calls for readiness shedding, backpressure, scaling, or diagnosis—not restart—unless the application has a proven unrecoverable mode. OOM and process crash already trigger exit/restart behavior; a liveness probe is optional when the process reliably self-terminates on fatal state.

Keep liveness implementation independent of the serving worker pool where possible but still meaningful. A health thread that responds while the main event loop is dead is a false live signal. Bound response time and avoid allocations/locks that fail precisely under pressure.

### Define readiness as safe admission of new work

Readiness should become true only after listeners, routes, configuration, credentials, local state, caches required for correctness, membership, and any mandatory dependency capability are ready. It remains active throughout container life and may withdraw/recover without restart.

Dependency checks require judgment. If an API cannot perform any advertised operation without its database, removing it can prevent useless traffic. If it can serve cached reads, queue durable writes, or return a controlled partial response, declaring every replica unready may turn a dependency outage into total connection failure. Model capability and degradation explicitly.

Readiness is not a monitoring endpoint. It should not query every downstream service, scan a large table, perform writes, repair state, or emit large bodies. Monitoring may use richer diagnostics and user-facing synthetic transactions without being called every few seconds by every kubelet.

For non-Service workers, readiness still contributes Pod Ready, rollout, PDB availability, and controller decisions. Define it from ability to process owned work safely, not from an irrelevant HTTP listener.

### Choose probe mechanisms deliberately

HTTP probes can validate a dedicated path/status and named port; kubelet connects to the pod IP from the node. Keep response bodies tiny and do not rely on ordinary Service routing. HTTPS verifies a protected transport path under kubelet behavior but health endpoints still need an explicit threat model.

TCP probes prove a connection can be established, not that a protocol or application operation is correct. They are suitable when accepting the port is the intended minimal predicate. A stalled server can accept while failing work.

gRPC probes use the standardized health checking protocol under supported Kubernetes behavior. Service names can distinguish liveness and readiness. Confirm port/TLS/auth constraints and feature compatibility rather than assuming HTTP options apply.

Exec probes run a process in the container and consume its resources. Shell startup, forks, locks, missing tools, environment, and timeouts can produce false failure or process leaks. Prefer an in-process endpoint when possible; if exec is required, use a small direct binary/command with no shell pipeline and bounded runtime.

### Tune thresholds from detection and false-action cost

`initialDelaySeconds` postpones probing; `periodSeconds` sets nominal cadence; `timeoutSeconds` bounds one attempt; `failureThreshold` requires consecutive failures; `successThreshold` controls recovery for readiness and must be one for startup/liveness.

A simplified worst-case steady failure detection bound is approximately

$$
T_{detect}\lesssim failureThreshold\times periodSeconds+timeoutSeconds+J,
$$

where $J$ covers scheduling, node load, and implementation uncertainty. Validate actual behavior rather than treating the expression as a guarantee.

Short timeouts and threshold one react quickly but turn transient scheduling/network pauses into churn. Long windows preserve stability but serve broken traffic longer. Tune startup, liveness, and readiness independently from service error budgets and recovery actions.

Probe-level `terminationGracePeriodSeconds` can bound shutdown after failed startup/liveness where supported; readiness probes cannot set it. A rapid liveness restart may need different grace than planned pod deletion, but it still must avoid corrupting state.

### Inventory lifecycle control decisions

The following synthetic inventory distinguishes probe and external-gate coverage across workload types.

<!-- bijux-verify: {"id":"health-lifecycle-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"workloads=8\nstartup=2\nliveness=3\nreadiness=6\nexternal_gates=2\ntotal_grace_seconds=360\n","stderr":""}} -->
```python
workloads = [
    {"name": "api",       "startup": True,  "liveness": True,  "readiness": True,  "gate": True,  "grace": 45},
    {"name": "worker",    "startup": True,  "liveness": True,  "readiness": False, "gate": False, "grace": 60},
    {"name": "proxy",     "startup": False, "liveness": True,  "readiness": True,  "gate": False, "grace": 30},
    {"name": "metrics",   "startup": False, "liveness": False, "readiness": True,  "gate": False, "grace": 10},
    {"name": "migration", "startup": False, "liveness": False, "readiness": False, "gate": False, "grace": 120},
    {"name": "cache",     "startup": False, "liveness": False, "readiness": True,  "gate": False, "grace": 20},
    {"name": "signer",    "startup": False, "liveness": False, "readiness": True,  "gate": True,  "grace": 60},
    {"name": "sidecar",   "startup": False, "liveness": False, "readiness": True,  "gate": False, "grace": 15},
]
print(f"workloads={len(workloads)}")
print(f"startup={sum(item['startup'] for item in workloads)}")
print(f"liveness={sum(item['liveness'] for item in workloads)}")
print(f"readiness={sum(item['readiness'] for item in workloads)}")
print(f"external_gates={sum(item['gate'] for item in workloads)}")
print(f"total_grace_seconds={sum(item['grace'] for item in workloads)}")
```

The fixture is a design inventory, not evidence that any predicate, timing, external registration, graceful drain, work preservation, or recovery is correct in a real cluster.

### Use readiness gates for external prerequisites

Pod readiness gates add condition types to the final Ready calculation. All containers must be ready and every named gate condition must be `True`; absent conditions default false. A controller can represent cloud load-balancer registration, network programming, security attestation, data warmup, or application membership that kubelet cannot determine.

Give each condition a qualified type and one authoritative writer. Status updates need conflict-safe patches, reason/message, transition time, observed version/generation where meaningful, bounded retries, leader election, RBAC, and cleanup. A dead controller can hold every pod unready.

Avoid gates for facts already covered by local readiness or for optional dependencies. Gate latency extends rollout and PDB unavailability, so observe it separately. Reject a controller that marks `True` from desired state without verifying external realization.

### Treat probe output as control-plane input

Probe responses should be low-cardinality and non-sensitive. Kubelet needs pass/fail; operators need separate metrics/logs that explain which local predicate failed. Do not return credentials, internal topology, full dependency errors, heap state, or customer data.

Probe endpoints must resist unauthenticated abuse according to network reachability. Keeping them minimal limits information disclosure and resource amplification. NetworkPolicy and host/node probe paths must be tested together; a policy that blocks kubelet probes can remove all endpoints.

Alert from user outcomes and sustained lifecycle anomalies, not each readiness flap. Useful signals include probe attempts/outcomes/latency, state transition reasons, restart rate, time to startup/ready, ready replica count, gate age, and correlation with resource/dependency incidents.

### Implement process lifecycle correctly

The application process should run as container PID 1 or use an init that forwards signals and reaps children. On the configured stop signal—normally SIGTERM—the process transitions exactly once into drain, stops new admission, coordinates workers, flushes bounded state, closes resources, and exits with a meaningful code.

A lifecycle `StopSignal` can override the image's `STOPSIGNAL` under supported Kubernetes behavior. Keep image and pod contracts aligned; a nonstandard signal must be handled and documented across runtime versions.

Processes must also handle crash, SIGKILL, node loss, and power loss, where no graceful code runs. Durable protocols, transactions, leases, idempotency, replay, and fencing—not `PreStop`—provide correctness for abrupt failure.

### Use hooks as bounded coordination, not guarantees

`PostStart` starts around container creation and is not guaranteed to run before the ENTRYPOINT. A slow/hung handler can block transition to Running; failure kills the container. Initialization requiring strict order belongs in the process or init-container design.

`PreStop` runs before the stop signal for management-triggered termination when the container is still running. Its runtime consumes the pod termination grace; the process receives TERM only after the hook completes. A 55-second hook plus 10-second application shutdown does not fit a 60-second grace.

Hook delivery is intended at least once, so handlers must be idempotent. A kubelet/node crash may prevent useful completion. Keep hooks small: notify the process, set a local drain flag, or use the built-in sleep action only for a justified propagation allowance. Long remote calls or state migrations are fragile.

Record hook start/end/failure without leaking data. Test repeated delivery and force-kill during each step.

### Budget the termination sequence end to end

When deletion begins, the API records a deletion timestamp and grace. Kubelet begins local graceful shutdown while controllers update endpoints and workload availability. These paths are concurrent and propagate through watches, proxies, gateways, external load balancers, DNS/client caches, and existing connections.

Terminating EndpointSlice endpoints have `ready=false`; `terminating=true`; `serving` can communicate actual serving state to drain-aware consumers. Ordinary service traffic should avoid them, but stale routes and open connections remain possible. The application must reject new nonessential work after drain starts.

For total grace $G$, design a conservative budget

$$
G\ge T_{propagate}+T_{preStop}+T_{drain}+T_{flush}+T_{exit}+M,
$$

where propagation and application work can overlap only when the implementation proves it, and $M$ covers tail uncertainty. Measure percentiles and maximum accepted work duration.

At grace expiry, kubelet/runtime forcibly stops remaining processes with SIGKILL. The API may grant a small extension if a `PreStop` hook is still running under documented behavior, but do not design availability around that emergency detail.

### Drain traffic and work by protocol

HTTP servers stop listening or mark connections draining, reject new operations with suitable retry semantics, and let bounded idempotent requests finish. HTTP/2, gRPC, WebSocket, and long polling need explicit connection-age, GOAWAY/reconnect, and stream policy. Closing keepalive immediately can reset work; waiting forever defeats grace.

Queue consumers stop fetching, extend/return leases safely, finish or checkpoint current messages, commit acknowledgements only after durable effects, and exit. A worker with no HTTP Service still needs readiness/work-ownership and drain evidence.

Databases and stateful members transfer leadership, leave membership, flush logs, release/fence leases, or preserve crash recovery. Never use a readiness endpoint to perform those operations. Jobs may need checkpoint and Pod failure policy; their completion semantics differ from continuously serving controllers.

Define accepted-work counters and terminal outcomes: completed, durably handed off, retriable/unacknowledged, or explicitly failed. “Process exited zero” is not proof no work was lost.

### Coordinate multi-container pods and sidecars

Containers in a pod share fate but have independent probes/restarts. Pod Ready requires relevant container readiness plus gates; an unnecessary sidecar readiness probe can block the application, while omitting a critical proxy readiness can expose traffic before the path works.

Without native sidecar semantics, ordinary containers receive stop signals in unspecified order. A proxy exiting before the application drains can reset requests; an application exiting before a log/mesh sidecar flushes can lose telemetry or leave connections.

Native sidecars declared through restartable init-container semantics start before app containers and are terminated after regular containers, in reverse sidecar order under current behavior. They still share the pod grace budget; slow main-container shutdown can leave sidecars little time and forced sidecar exits can be normal.

Prefer explicit protocol coordination over assumed timing. Test app/proxy/agent start, readiness, restart, liveness failure, normal termination, and forced termination combinations.

### Separate restart, replacement, and failover

Container restart preserves pod identity, volumes, network namespace depending on sandbox state, and node. It can fix local process state but not node, zone, corrupt shared data, incompatible configuration, or missing capacity.

Pod replacement creates new identity/IP and repeats scheduling, sandbox, volume, image, startup, and readiness. Workload controllers maintain desired replicas but may be constrained by surge/unavailable, topology, PDB, storage, and capacity.

Application failover transfers ownership or traffic between replicas/regions. Kubernetes readiness and endpoints participate but do not implement quorum, fencing, replication, or data recovery. Keep liveness from fighting application failover by restarting a slow follower or old leader at the wrong moment.

Restart backoff prevents tight crash loops but increases recovery delay. Observe root termination cause and previous logs before deleting the pod and erasing evidence.

### Design PDBs from actual availability

A PDB selects pods and specifies either `minAvailable` or `maxUnavailable`. The disruption controller reports current/desired healthy and allowed disruptions. Cooperating eviction clients such as node drain consult it.

PDB does not block direct pod/controller deletion, rollout initiated by the workload owner, many involuntary failures, or every preemption path. It cannot create replicas, capacity, topology, working readiness, or application quorum. A zero-disruption budget can block node maintenance indefinitely.

Selectors must match exactly the intended controller set; policy/v1 empty selectors match all pods in the namespace. Percent rounding and scale behavior need tests. Choose unhealthy-pod eviction policy so a permanently unready pod does not make maintenance impossible while preserving the intended budget.

For quorum systems, derive budget from protocol and member health rather than replica count alone. Coordinate one node/zone at a time, wait for replacement readiness and data repair, then continue.

### Distinguish disruption paths

Voluntary eviction, direct deletion, Deployment rollout, StatefulSet update, scale-down, scheduler preemption, taint eviction, node-pressure eviction, graceful node shutdown, node partition/loss, liveness restart, OOM, and application crash invoke different controls and grace behavior.

The `DisruptionTarget` condition can identify several impending disruption reasons, including scheduler preemption, taint-manager deletion, Eviction API, PodGC, or kubelet termination. It is evidence, not certainty that deletion completes; interrupted disruption can clear.

Build a lifecycle matrix: trigger, initiator, PDB participation, grace/hook expectation, replacement owner, data/work risk, and evidence. Test every high-impact row. A graceful rollout test does not prove node-loss safety.

### Observe lifecycle without probe amplification

Record pod UID/revision, node, phase/conditions with observed generation where available, container current/last state, exit code/signal/reason, restart count/backoff, probe type/outcome/latency/reason, gate writer/version, endpoint conditions, active connections/work, drain stage/duration, hook outcome, grace/forced kill, and replacement readiness.

Correlate user traffic/errors, load-balancer/gateway endpoint state, queue leases, transactions, and controller status. A readiness failure may reduce errors or cause overload elsewhere; observe both local action and system result.

Events are bounded and aggregated. Export durable metrics/logs for fleet analysis while keeping cardinality controlled. Do not log every successful probe or sensitive dependency response.

Key service-level measures include cold-start tail, time from ready loss to traffic cessation, termination request to no-new-work, accepted-work completion ratio, forced termination rate, restart-loop rate, unready-but-live duration, and disruption completion time.

### Diagnose common lifecycle incidents by state

For never-ready pods, inspect scheduling/setup conditions, init containers, image/config/secret/volume, startup probe timing/outcome, container logs, readiness result, custom gates, endpoint status, and dependency capability. Do not add delay without locating the state.

For restart loops, inspect current and previous termination reasons, exit/signal, OOM, hook failure, startup/liveness events, probe timeout/threshold, resource pressure, dependency correlation, and backoff. Disable a dangerous liveness action through a reviewed rollout if it is amplifying an incident; retain monitoring.

For traffic to terminating pods, correlate deletion timestamp, Ready/serving/terminating endpoint conditions, proxy/gateway/watch lag, external load balancer, connection pools, keepalive/streams, process drain flag, and new-work rejection. A longer sleep may hide but not fix a non-draining client.

For stuck Terminating, inspect grace deadline, finalizers separately, `PreStop` duration, process signal handling/PID 1, uninterruptible I/O, volume unmount, node reachability, sidecars, and API deletion state. Force deletion removes the API object without proving node process or data safety; use only with fencing and incident controls.

### Test lifecycle as a temporal contract

Automated tests should delay startup, hang locally, fail one/shared dependency, overload, flap readiness, timeout probes, repeat hooks, send stop signals, hold long connections, interrupt streams, retain queue leases, exhaust grace, kill the node, and restore dependencies.

Measure ordered facts rather than only final status: no traffic before readiness; no liveness during startup; readiness loss before ordinary endpoint use ceases; no new accepted work after drain; accepted work completes/hands off; state remains valid after SIGKILL; replacement becomes ready; capacity and error budgets hold.

Run tests under rollout surge, scale-down, eviction, preemption, PDB block, zone/node loss, sidecars, storage, service mesh, external load balancer, and real client libraries. Synthetic single-pod HTTP tests miss the distributed races.

### Govern lifecycle as a platform contract

Provide language libraries and workload templates that separate predicates, expose cheap endpoints, handle PID-1 signals, register drain state, count accepted work, and emit standard metrics. Defaults should be safe but applications own domain-specific readiness and work completion.

Admission can require probes for serving workloads, forbid identical dependency-heavy liveness/readiness endpoints, bound probe rates/timeouts, require grace and PDB metadata for critical tiers, validate selector overlap, and restrict unsafe lifecycle hooks.

Offer lifecycle classes by workload type: stateless HTTP, streaming/gRPC, queue worker, singleton/stateful member, batch/Job, and proxy sidecar. Each includes probe semantics, drain protocol, grace range, disruption policy, capacity/topology assumptions, conformance tests, and consumer diagnostics.

## Definitions and Notation

Let $S_p(t)$, $V_p(t)$, $R_p(t)$, and $G_{p,i}(t)$ denote startup, liveness, readiness, and readiness-gate predicates for pod $p$. A simplified Pod Ready predicate is

$$
Ready_p(t)=ContainersReady_p(t)\land\bigwedge_i G_{p,i}(t).
$$

Service traffic eligibility additionally requires

$$
Eligible_p=Ready_p\land Selected_p\land EndpointReady_p\land Programmed_p\land Reachable_p,
$$

with propagation delay between changes. During termination, `ready=false`, `terminating=true`, and `serving` may remain true for drain-aware behavior.

Let $A(t)$ be accepted unfinished work. Safe application exit at $t_e$ requires

$$
|A(t_e)|=0
$$

or every remaining item has a durable, unambiguous handoff/retry state. Let $t_d$ be drain start and $t_k$ force-kill deadline; termination must make the safety condition true before $t_k$ under the graceful path.

Define restart amplification $a$ during a shared incident as restarted replicas divided by replicas with local unrecoverable failure. A dependency-based liveness design can make $a\gg1$.

## Mechanisms, Invariants, or Proof Structure

The mechanism is a set of coupled state machines. Kubelet sequences startup and periodic probes, updates container readiness and restart behavior, invokes hooks/signals, and enforces grace. Pod conditions aggregate container and controller-owned gates. Endpoint controllers and data planes translate readiness/deletion into traffic state. Workload/disruption controllers replace or evict pods. Applications own acceptance, work completion, state, and failover.

The **predicate-separation invariant** assigns one question and action to startup, liveness, readiness, capability, and correctness. The **local-recovery invariant** ensures liveness restart can improve the detected state. The **probe-safety invariant** makes checks bounded, cheap, side-effect-free, and non-sensitive.

The **gate-ownership invariant** gives external conditions authoritative writers and freshness. The **drain invariant** stops new admission and safely resolves accepted work before force kill. The **propagation invariant** assumes stale routing and defends in the application.

The **abrupt-failure invariant** preserves correctness without hooks through durable protocols. The **disruption invariant** combines PDB with replicas, topology, capacity, readiness, and workload semantics. The **evidence invariant** distinguishes control-plane conditions from user outcome.

This is an assurance structure, not a proof of availability or zero work loss. Kubelet/runtime behavior, network and endpoint propagation, process code, clients, controllers, dependencies, storage, failure timing, and operational execution remain assumptions requiring tests.

## Alternatives and Trade-Offs

No liveness probe is correct when a process exits reliably on fatal state; it avoids false restarts but cannot detect hangs. Conservative liveness recovers proven deadlocks more slowly; aggressive liveness reduces detection time but risks cascading churn.

Local-only readiness avoids shared-dependency amplification but can route requests that cannot succeed. Dependency-aware readiness protects clients when no useful response is possible but can remove all capacity. Capability-specific routes, degraded modes, circuit breakers, and explicit errors often outperform one global Boolean.

HTTP/gRPC probes express protocol semantics but add server code and network path. TCP is simple but shallow. Exec can inspect local state but creates processes and container coupling. Choose the minimum mechanism that validly answers the predicate.

Short grace accelerates rollout and node maintenance but increases forced termination and lost work. Long grace protects streams/jobs but consumes capacity and slows recovery; bound operation/connection ages or checkpoint work to make grace finite.

`PreStop` sleep is simple propagation padding but wastes grace and assumes a delay distribution. Application drain plus endpoint-aware proxies is stronger but needs integration. Native sidecars improve ordering while sharing grace and version requirements.

PDB with `minAvailable` maps directly to a minimum count; `maxUnavailable` scales naturally with controller replicas. Strict budgets protect service but can block maintenance; permissive unhealthy-pod eviction improves drain progress but can reduce recovery opportunity for an already unhealthy set.

## Failure Modes and Misconceptions

- **“Liveness means the service is healthy.”** It means restart is the selected recovery for a local condition; dependency and user success are separate.
- **“Readiness failure restarts the pod.”** It changes readiness/traffic participation; kubelet continues probing the running container.
- **“Startup is just a long initial delay.”** It explicitly suppresses liveness/readiness until success and has its own failure action.
- **“TCP success proves the API works.”** It proves a connection was accepted at that address/port.
- **“Every dependency belongs in readiness.”** Shared failures can withdraw all replicas and amplify load; model useful degraded capability.
- **“The endpoint disappears before SIGTERM.”** endpoint and local shutdown paths propagate concurrently; stale/new connections remain possible.
- **“PreStop adds time before grace starts.”** Grace starts before the hook; hook and process exit share it.
- **“Hooks run once and always run.”** Delivery may repeat, and catastrophic/node failure can skip graceful completion.
- **“SIGTERM reaches my application automatically.”** PID 1, wrappers, signal forwarding, and custom stop signals determine delivery/handling.
- **“PDB guarantees availability.”** It governs cooperating voluntary eviction and depends on real ready replicas/capacity/protocol.
- **“A zero exit proves graceful drain.”** Accepted work, acknowledgements, transactions, and clients require separate evidence.
- **“Force deleting a stuck pod stops it.”** It removes API state; an unreachable node may still run a process until fenced.

## Worked Examples

### Example 1

A JVM needs 80 seconds for cold recovery but liveness allows 30. A startup probe grants the measured tail; steady liveness remains fast enough to detect a later event-loop deadlock.

### Example 2

All API replicas restart when DNS fails because liveness resolves a dependency. Liveness becomes local; readiness/capability and circuit breakers handle DNS failure without a restart storm.

### Example 3

A TCP readiness probe passes while a request worker pool is deadlocked. A bounded in-process endpoint verifies listener and dispatcher progress without invoking downstream operations.

### Example 4

A cloud load balancer takes 20 seconds to register new targets. Its controller owns a readiness gate, so rollout availability does not count pods before external registration is observed.

### Example 5

A 60-second `PreStop` sleep consumes a 60-second grace and the process receives no useful drain time. The team measures propagation, starts drain immediately, and budgets hook plus work completion explicitly.

### Example 6

HTTP/2 clients keep streams on a terminating endpoint. The server sends graceful reconnect guidance, refuses new streams, bounds stream age, finishes accepted calls, and reports drain completion.

### Example 7

A queue worker has no readiness probe because it has no Service. Rollouts count it ready before it owns a valid lease. Worker readiness now reflects safe consumption, and drain stops fetch then resolves acknowledgements.

### Example 8

A PDB blocks node drain because one selected pod is permanently unready. The owner repairs readiness and chooses a reviewed unhealthy-pod eviction policy rather than bypassing every budget.

### Example 9

An application container exits after draining, then its legacy proxy sidecar exits first on another run and resets traffic. Native sidecar ordering plus explicit proxy/app drain coordination makes termination repeatable.

### Example 10

A node partition leaves an old stateful process running after its API pod is force deleted. Infrastructure and application fencing precede replacement ownership; graceful hooks were never a safety boundary.

## Cross-Program Connections

Operating systems contributes processes, PID 1, signals, exit, resource pressure, and forcible termination. Distributed systems contributes partial failure, failure detectors, leases, fencing, eventual propagation, and failover. Networking contributes endpoints, connection lifetime, load balancers, streams, and drain.

Reliability contributes health-model design, error budgets, restart amplification, overload, disruption, incident diagnosis, and failure injection. API engineering contributes protocol health, idempotency, retry guidance, long requests, and graceful shutdown. Data and database engineering contribute transactions, checkpoints, acknowledgements, replay, quorum, and work ownership.

Testing contributes temporal assertions, chaos/fault injection, and end-to-end outcome verification. Security contributes health endpoint exposure, hook authority, sensitive output, and node fencing. Platform product engineering packages safe lifecycle defaults while preserving application-owned semantics.

## References

- Kubernetes Project, [*Liveness, Readiness, and Startup Probes*](https://kubernetes.io/docs/concepts/workloads/pods/probes/), current documentation retrieved September 2, 2026. Probe purposes, startup suppression, liveness restart, readiness traffic behavior, mechanisms, and selection guidance.
- Kubernetes Project, [*Configure Liveness, Readiness and Startup Probes*](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/), current documentation retrieved September 2, 2026. HTTP/TCP/gRPC/exec configuration, delay/period/timeout/thresholds, probe behavior, named ports, and probe-level grace.
- Kubernetes Project, [*Pod Lifecycle*](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/), current documentation retrieved September 2, 2026. Phases, container states, restart policy/backoff, conditions, readiness gates, pod termination, endpoints, signals, force kill, and sidecar order.
- Kubernetes Project, [*Pod Conditions*](https://kubernetes.io/docs/concepts/workloads/pods/pod-condition/), current documentation retrieved September 2, 2026. Built-in conditions, transition fields, DisruptionTarget reasons, interruption behavior, and failure-policy use.
- Kubernetes Project, [*Container Lifecycle Hooks*](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks), current documentation retrieved September 2, 2026. PostStart, PreStop, StopSignal, exec/HTTP/sleep handlers, timing, shared grace, failure, and at-least-once delivery.
- Kubernetes Project, [*Sidecar Containers*](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/), current documentation retrieved September 2, 2026. Restartable init containers, startup/readiness, Job behavior, resource accounting, and reverse-order termination after application containers.
- Kubernetes Project, [*EndpointSlices*](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/), current documentation retrieved September 2, 2026. Endpoint `ready`, `serving`, and `terminating` conditions, pod mapping, drain behavior, and consumer interpretation.
- Kubernetes Project, [*Explore Termination Behavior for Pods and Their Endpoints*](https://kubernetes.io/docs/tutorials/services/pods-and-endpoint-termination-flow/), current documentation retrieved September 2, 2026. Observed deletion, EndpointSlice termination, readiness, hooks, signals, and traffic-drain flow.
- Kubernetes Project, [*Disruptions*](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/), current documentation retrieved September 2, 2026. Voluntary/involuntary disruption, availability mitigation, PDB scope/limits, eviction, and application/cluster-owner roles.
- Kubernetes Project, [*Specifying a Disruption Budget for Your Application*](https://kubernetes.io/docs/tasks/run-application/configure-pdb/), current documentation retrieved September 2, 2026. Selectors, `minAvailable`, `maxUnavailable`, rounding, empty-selector semantics, unhealthy-pod eviction policy, and operational choices.
- Kubernetes Project, [*Safely Drain a Node*](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/), current documentation retrieved September 2, 2026. Cordoning, Eviction API, PDB-aware drain, DaemonSets, local data, completion, and uncordon workflow.
- Kubernetes Project, [*Pod Priority and Preemption*](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/), current documentation retrieved September 2, 2026. Preemption lifecycle, victims, termination grace, PDB best effort, nominated nodes, and priority/QoS interactions.

## Exercises

### Exercise 1

Design startup, liveness, readiness, capability, drain, grace, PDB, and evidence contracts for an HTTP API, gRPC streaming service, queue worker, three-member database, and one-shot migration Job.

### Exercise 2

Audit a pod whose one `/health` endpoint checks five dependencies for startup/liveness/readiness, uses 1-second timeout and threshold one, has a 45-second `PreStop` sleep with 30-second grace, runs behind an external load balancer, and writes accepted work only in memory.

### Exercise 3

Derive a termination budget for a service whose endpoint/data-plane propagation p99 is 12 seconds, bounded request duration is 25 seconds, checkpoint p99 is 8 seconds, process exit is 3 seconds, `PreStop` coordination is 2 seconds, and uncertainty margin is 10 seconds. Explain concurrency assumptions and what happens to longer streams.

### Exercise 4

Diagnose a rollout where new pods alternate between never-ready and liveness restarts, old pods receive traffic for 20 seconds after deletion, PDB blocks node drain, and the service mesh sidecar sometimes exits before the application.

### Exercise 5

Transfer the lifecycle model to autonomous warehouse robots receiving jobs through a fleet coordinator. Address boot self-test, local liveness, readiness for new jobs, degraded capability, external gates, accepted-job drain, safe stop, maintenance disruption, abrupt power loss, evidence, and human authority.

## Answers to the Exercises

### Answer 1

The HTTP API uses measured startup, local event-loop liveness, readiness for listener/config/credential and useful API capability, bounded HTTP drain, zone-spread replicas, PDB, and user/request evidence. The gRPC service additionally stops new streams, sends reconnect/GOAWAY semantics, bounds or transfers long streams, and measures connection drain. The queue worker's readiness means it can safely acquire/renew leases even without a Service; drain stops fetch, completes/checkpoints or releases messages, then exits. Database startup includes recovery/membership, liveness avoids killing a slow valid replica, readiness follows quorum/role policy, termination transfers leadership and fences ownership, and PDB derives from quorum plus repaired replicas. The migration Job usually needs startup/progress and a hard execution deadline rather than traffic readiness; work is idempotent, checkpointed, uses Job failure policy, and native sidecars cannot block completion. Each separates local restart, pod replacement, application failover, and business validation.

### Answer 2

One dependency-heavy endpoint couples distinct actions and can restart every replica during shared failure. Split startup progress, local unrecoverable liveness, and traffic readiness/capability; use richer dependency monitoring separately. A one-second single failure threshold is vulnerable to node load and transient latency; measure distributions and choose bounded consecutive-failure/recovery behavior. Startup receives its own tail budget. The 45-second hook cannot fit inside 30-second grace, so the process may never receive TERM before SIGKILL. Begin application drain immediately, replace fixed sleep with measured propagation coordination, and budget hook, endpoint/load-balancer propagation, accepted-work resolution, persistence, and exit. Add an external-registration readiness gate if the controller can verify load-balancer state. In-memory accepted work cannot survive force kill or node loss; make operations idempotent and persist/acknowledge only after a durable result or handoff. Test stale routes, long connections, repeated/skipped hooks, dependency outage, and abrupt node loss.

### Answer 3

Without proven overlap, a conservative sum is $12+2+25+8+3+10=60$ seconds, so configure grace above 60 seconds with an operationally rounded margin rather than exactly at it. If endpoint propagation and work drain run concurrently, the critical path may use their maximum instead of their sum, but only a test showing drain begins immediately and stale clients are rejected justifies that reduction. `PreStop` consumes grace and must complete before TERM, so the application should enter drain through a reliable early signal/coordination path. Requests longer than 25 seconds violate the assumed bound: cap them, checkpoint/transfer them, return retryable state before shutdown, or allocate a separately justified longer grace. Existing streaming connections need explicit graceful close/reconnect and maximum age; otherwise no finite budget proves completion. Measure accepted/completed/handoff work and forced kills during real proxy/load-balancer rollouts.

### Answer 4

Start with pod UID/revision timelines. For new pods, compare startup probe budget, application initialization progress, readiness causes, liveness cause/threshold, previous termination reason, resources, config/credentials, gates, and dependency correlation. Liveness may be firing before startup completes or using the same readiness dependency; add/correct startup and localize liveness rather than increasing every delay. For old traffic, trace deletion timestamp, EndpointSlice ready/serving/terminating, mesh/gateway/watch propagation, external load balancer, client keepalive/streams, process drain flag, and new-work rejection. Repair the actual 20-second propagation/drain path. PDB blockage may reflect insufficient genuinely ready replacements, selector error, strict budget, or unhealthy-pod policy; restore availability before choosing policy, never bypass blindly. Adopt supported native sidecar ordering or explicitly coordinate app/mesh drain, with enough shared grace. Re-run rollout, node drain, preemption, long stream, hook repeat, and forced kill while verifying user outcomes and accepted work.

### Answer 5

Boot startup verifies hardware, maps, brakes, sensors, battery, localization, signed configuration, and coordinator identity before other checks. Local liveness detects controller deadlock or unrecoverable sensor-bus state only when a safe local restart can improve it. Readiness for new jobs requires safe locomotion, sufficient battery/capacity, current map/zone authorization, and reachable coordination; degraded capability may permit return-to-base or low-risk local movement without accepting ordinary jobs. An external gate can represent cleared aisle/maintenance authorization with one authoritative controller and freshness. On drain, the robot stops accepting jobs, finishes or durably transfers its current job, reaches a safe location, parks/brakes, records load custody, and acknowledges completion before power-down. Maintenance budgets limit how many robots leave a zone while preserving emergency capacity. Abrupt power loss relies on durable job/position state and physical fail-safe brakes, not hooks. Evidence tracks state transitions, assigned/accepted/completed jobs, location, gate version, battery, safe stop, overrides, and fleet capacity. Human safety officers can halt or isolate robots immediately; automation never delays an emergency stop to preserve throughput.
