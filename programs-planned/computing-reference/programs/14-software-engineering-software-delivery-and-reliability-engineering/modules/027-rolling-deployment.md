---
module_id: SDRE-027
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 27
title: Rolling Deployment
status: complete
last_verified: 2026-09-06
---

# Rolling Deployment

## One-Page Review

### Governing question

How can a service replace old instances with new ones incrementally while preserving enough serving capacity, maintaining mixed-version compatibility, draining retired work, and preventing a failed rollout from expanding?

### Essential definitions

- a **rolling deployment** replaces members of a running population in bounded batches instead of constructing a complete parallel environment or switching every member at once;
- the **desired population** is the controller's target number of serving units, not proof that those units are useful;
- a **candidate unit** runs the new deployment subject; an **old unit** runs the source subject;
- **surge** is temporary population above the desired count during replacement;
- **unavailability budget** is the maximum desired capacity that policy permits to be unavailable during replacement;
- **readiness** is an admission signal that a unit can receive the work represented by that signal now;
- **availability** is a controller-defined state that may require readiness to remain stable for a minimum interval;
- **draining** stops new admission to an old unit while bounded in-flight work finishes or is safely transferred;
- the **mixed-version window** is the interval in which old and new subjects can act in the same system;
- **rollout generation** identifies one desired transition so stale controllers and observations cannot govern a newer transition;
- a **progress deadline** detects lack of rollout progress; detection is not itself repair or rollback;
- **rollback** is another controlled deployment toward a compatible earlier subject, not reversal of prior data effects.

### Central model, mechanism, or theorem

Let $N$ be desired replicas, $S$ allowed surge units, and $U$ allowed unavailable units. A count-based controller commonly aims to preserve

$$
R_{nonterm}\le N+S
\qquad\text{and}\qquad
A\ge N-U,
$$

where $R_{nonterm}$ counts non-terminating units and $A$ counts available units. Progress by replacement requires at least one slot: $S+U\ge1$. These count constraints are necessary but not sufficient. If serving unit $i$ has demonstrated sustainable capacity $c_i$, real capacity is

$$
C_{available}=\sum_{i\in Available}c_i,
$$

and policy should require $C_{available}\ge(1+h)\lambda$ for workload demand $\lambda$ and headroom $h$, subject to dependency and failure assumptions.

### Critical invariants

- every old and candidate unit is bound to an immutable deployment subject and rollout generation;
- new units do not receive authoritative work until startup, readiness, compatibility, and observation gates pass;
- old units do not terminate until new-admission removal and bounded draining satisfy policy;
- available serving capacity, not replica count alone, remains above the declared demand bound;
- old and new versions safely share protocols, schemas, messages, caches, and external effects throughout the mixed-version window;
- singleton and partition authority is fenced independently of process lifetime;
- missing telemetry, stale observations, or exceeded guardrails halt expansion;
- surge demand on schedulers and shared dependencies remains within demonstrated limits;
- a progress timeout reports stalled work and triggers declared policy; it never counts as successful recovery;
- rollback is permitted only while the target and current state remain mutually compatible.

### Common failures

Failures include counting started processes as capacity, exposing a candidate before warm-up, using liveness as readiness, setting both surge and unavailability to zero, terminating before routes converge, ignoring persistent connections and queues, deploying incompatible wire or schema changes, storing sessions locally, permitting old singleton workers after replacement, letting autoscaling hide candidate regression, measuring only fleet-wide health, rolling several generations concurrently, treating a deadline as automatic rollback, and returning to code that cannot interpret new state.

### Compact example

A ten-replica API allows surge three and unavailability two. The controller creates at most three non-terminating candidates beyond the desired population, waits until each passes startup, readiness, a stable-ready interval, and version-tagged service checks, then removes new admissions from at most two old units. Old units drain bounded requests before termination. Capacity is computed from measured per-version throughput, not ten green probe results. A schema gate confirms both versions coexist. Any missing telemetry or incompatible generation pauses replacement.

### Connections

[SDRE-026](026-canary-deployment.md) develops controlled candidate evaluation; a rolling deployment can embed a canary pause but does not inherently perform one. [SDRE-028](../ROADMAP.md) develops feature flags, which can decouple code presence from feature exposure. Platform Engineering owns concrete controllers; Distributed Systems owns reconciliation, leases, and partial failure.

## Governing Question

A rolling deployment appears simple: start one new instance, stop one old instance, and repeat. That description assumes instances are interchangeable, readiness is truthful, workload is stateless, routing changes immediately, capacity is homogeneous, versions coexist safely, and the controller never loses or repeats work. Production systems violate several of those assumptions at once.

The governing problem is therefore a constrained state transition. The release system must preserve service and authority while membership changes. It must decide when a candidate is eligible to serve, when an old member is safe to drain, how many members may change concurrently, which evidence permits the next batch, and what to do when the system is left between generations.

## Why This Matters

Rolling replacement uses less duplicate capacity than blue-green deployment and bounds the simultaneous change compared with an all-at-once restart. It is widely applicable to replicated services, workers, agents, and infrastructure components. Its defining cost is a mixed-version interval. That interval turns compatibility from a desirable property into a release invariant.

Current Kubernetes Deployment documentation is a useful concrete implementation example: a rolling update incrementally scales new ReplicaSets up and old ones down, with `maxSurge`, `maxUnavailable`, `minReadySeconds`, and `progressDeadlineSeconds` controlling parts of the process [1]. Those fields are Kubernetes semantics, not a universal definition of rolling deployment. Kubernetes also warns that terminating Pods can make the actual process count temporarily exceed the desired replicas plus configured surge [1].

Current Kubernetes probe documentation distinguishes startup, readiness, and liveness: a startup probe delays the other probes, readiness controls Service endpoint eligibility, and repeated liveness failure can restart a container [2]. These mechanisms provide local signals. They do not prove business correctness, sustained throughput, downstream health, or safe rollback.

Google's SRE guidance recommends fitting rollout shape to service risk and expanding changes progressively across production scope [4, 5]. The durable principle is controlled exposure with observable state. The chapter uses Kubernetes for precise current examples while keeping the design model independent of one orchestrator.

## Prerequisites and Retrieval

Retrieve deployment subject, artifact digest, desired state, actual state, controller, reconciliation, replica, readiness, liveness, startup, capacity, utilization, queue, session, connection, schema compatibility, idempotency, lease, fencing, SLO, error budget, rollback, and partial failure.

From SDRE-024 retrieve expand–migrate–contract and mixed-version database safety. From SDRE-025 retrieve routing authority, warm-up, and draining. From SDRE-026 retrieve stage guardrails and version-attributed observation. Rolling deployment combines these controls around incremental membership replacement.

## Learning Objectives

After completing this module, you should be able to:

1. define rolling deployment independently of a specific platform;
2. distinguish desired, running, ready, available, serving, and terminating populations;
3. derive count and capacity constraints for a replacement batch;
4. design startup, readiness, stable-ready, admission, drain, and termination gates;
5. reason about heterogeneous units, warm-up, shared dependencies, and overload feedback;
6. maintain protocol, schema, message, cache, and state compatibility across versions;
7. preserve singleton, partition, and job authority with leases or fencing;
8. coordinate rolling replacement with autoscaling and topology constraints;
9. design progress, pause, cancellation, rollback, and stale-generation behavior;
10. test and audit a rollout controller without mistaking local observations for universal guarantees.

## Core Exposition

**Define the deployment subject and population.** A rollout changes a population from source subject $V_o$ to candidate subject $V_n$. A subject includes artifact digest, effective configuration, secret references, schema assumptions, dependency contracts, and runtime policy. Mutable names such as `latest` or `production` are inadequate because the controller cannot prove what a unit runs after the label moves.

Inventory every unit governed by the rollout. HTTP replicas may share a Deployment, while queue consumers, schedulers, migration processes, and background threads live elsewhere. If they change together semantically but are controlled separately, the release plan must coordinate them explicitly. A green web fleet does not compensate for an old worker emitting incompatible messages.

**Separate population states.** `Running` often means a process exists. `Ready` means a declared admission check currently succeeds. `Available` may add a stable-ready interval. `Serving` means real work can reach the unit through all relevant routing layers. `Terminating` means retirement has begun but the process or its effects can still exist. These sets overlap imperfectly.

A controller should reconcile from observed state rather than assume each command completed. It records unit identity, subject, generation, lifecycle state, route membership, outstanding work, and observations. A create timeout leaves an unknown outcome: retrying blindly can exceed surge, while assuming failure can stall. Read-after-write reconciliation resolves uncertainty.

**Choose replacement budgets.** For desired count $N$, integer surge $S$, and unavailable allowance $U$, count policy commonly limits non-terminating population to $N+S$ and requires at least $N-U$ available units. With no free surge and no permitted unavailability, no unit can be added or removed, so $S=U=0$ cannot make progress.

Larger $S$ starts candidates sooner but consumes compute, addresses, quotas, image bandwidth, and downstream connections. Larger $U$ reduces resource demand but removes serving capacity before replacements prove themselves. Batch concurrency increases speed and correlated risk. Choose values from demonstrated capacity, startup distribution, failure domains, SLOs, and release risk—not aesthetic percentages.

Kubernetes resolves percentage budgets against desired replicas: `maxUnavailable` percentages are rounded down and `maxSurge` percentages are rounded up [1]. For $N=10$, 20% unavailable gives $U=2$ and 30% surge gives $S=3$. Other controllers may define rounding and counting differently, so portable policy must name the implementation.

**Use capacity, not count, as the service invariant.** Ten replicas do not imply ten equal units. Candidate code may consume more CPU; one zone may use smaller machines; cold caches may reduce throughput; a dependency may cap concurrency. Let $c_i$ be demonstrated sustainable capacity of available unit $i$. Require the sum of relevant capacities to exceed workload plus headroom under declared failure assumptions.

Capacity is multidimensional. A unit can meet request throughput but exhaust memory, database connections, queue leases, or network bandwidth. Check latency and saturation as demand approaches the bound. Include surge effects: thirty new instances opening connection pools simultaneously can overload a healthy database before they serve traffic.

An especially dangerous loop is remove–overload–fail-readiness. Removing old units increases load on the remainder; overloaded candidates fail readiness; routing concentrates further; liveness restarts them; restarts create more warm-up demand. Halt replacement before this positive feedback consumes the fleet. Readiness may shed traffic, while liveness should identify unrecoverable process failure rather than transient overload [2].

**Gate candidate admission.** Candidate creation is only the first step. A robust sequence is: schedule; start; complete one-time initialization; pass startup; pass readiness; remain ready for a minimum stable interval; verify version identity and observation; admit traffic; then evaluate service guardrails. A cheap `/ready` response cannot prove dependency semantics or capacity.

Kubernetes `minReadySeconds` illustrates a stable-ready gate: a newly created Pod must remain ready without container crashes for the configured duration before it is considered available [1]. The default is zero, which is fast but provides no stability observation. A stable interval should cover credible startup oscillation, not be copied as a ritual value.

Startup work must be safe to repeat because schedulers and controllers retry. Data migrations should not be hidden inside every replica startup. Cache warming must not create authoritative side effects. Large image pulls, just-in-time compilation, model loading, and connection establishment belong in rollout-time capacity estimates.

**Remove admission before termination.** Retirement reverses the admission sequence. Mark an old unit ineligible for new work, propagate that state through gateways or queue ownership, observe that new admissions stopped, drain bounded in-flight work, release leases, and terminate only after the drain policy succeeds or its failure rule runs.

Current Kubernetes Pod lifecycle documentation says terminating endpoints remain represented in EndpointSlices but are marked not ready for ordinary traffic; a separate `serving` condition can support draining-aware consumers [3]. The kubelet sends a termination signal and later forcibly stops remaining containers after the grace period [3]. This mechanism does not define application-level completion: the application must stop accepting work, handle signals, bound requests, and make retries safe.

Persistent HTTP connections, gRPC streams, WebSockets, queue reservations, and long jobs require explicit maximum duration or transfer semantics. A process killed after a grace period may leave a client uncertain whether an effect committed. Idempotency keys, durable checkpoints, leases, and response protocols contain that ambiguity.

If route propagation is bounded by $P$ and admitted work duration by $L$, a simple lower bound for drain observation is $P+L$. If either is unbounded, elapsed time alone cannot establish quiescence. Directly observe new admissions, active work, lease ownership, and effect generations.

**Design for mixed versions.** During a rolling deployment, an old client can call a new server and a new worker can consume an old message. Requests can traverse several versions in one trace. Compatibility must cover wire formats, APIs, database schema and data, serialized cache values, event envelopes, authentication claims, configuration, and operational commands.

Use tolerant readers only where ambiguity is safe; version messages when semantics differ; make additive schema changes before readers depend on them; backfill separately; remove old representations after the mixed-version and rollback windows close. A field being optional syntactically does not guarantee semantic compatibility.

External effects need idempotency and stable ownership. If both versions can bill the same order, replica health is irrelevant. Singleton schedulers, leaders, partitions, and exclusive devices use a lease or fencing token checked at the effect boundary. Process termination is not fencing: a delayed old process can awaken after its lease has expired.

Local sessions and ephemeral disks make replacement stateful. Move durable session state outside the unit, use version-compatible encoding, or provide explicit affinity and migration. Affinity alone can prevent old units from draining when sessions never expire.

**Preserve topology and failure tolerance.** Replacement batches should span failure domains deliberately. Replacing every replica in one zone first may leave a nominal count but lose zone tolerance. Conversely, spreading one candidate everywhere increases blast radius. Decide whether the risk requires one-zone canarying, balanced per-zone replacement, or sequential region rollout.

Topology constraints, disruption budgets, maintenance, and node failures can interact. A rollout budget is not a disaster budget unless the controller reserves capacity for concurrent failures. If policy permits two unavailable replicas and a node failure removes two more, the service can exceed its intended loss. Model exogenous failure during deployment.

**Coordinate autoscaling.** An autoscaler changes $N$ while the rollout changes membership. Define which generation owns desired size and how percentages are recalculated. Candidate inefficiency may cause scale-out, masking a regression until old units disappear; later rollback can leave excess capacity. Scale-in can select old or new members in ways that violate the rollout's intended batch.

Controllers need one reconciled policy: preserve minimum serving capacity, prefer removal consistent with rollout direction, keep topology constraints, and attribute resource signals by version. Freeze scaling only when the service can tolerate frozen capacity; otherwise make the interaction explicit and test it.

**Observe each batch.** Tag requests, jobs, resource metrics, dependency calls, retries, queue age, correctness signals, and business outcomes by exact subject and generation. Fleet aggregates hide a candidate whose few units fail while old units carry the load. Missing version labels or delayed telemetry are rollout failures, not neutral evidence.

Each batch has entry conditions, minimum exposure, guardrails, and an exit decision: advance, hold, pause, cancel, roll forward, or roll back. A rolling deployment is not automatically a canary; immediate replacement can cycle through the entire fleet before slow signals arrive. Insert evaluation pauses when risk requires representative evidence.

**Handle progress and generations.** Progress means declared movement toward a safe target: candidates become available, old units drain, or a blocked condition is resolved. A deadline detects that progress has not occurred. It should record the exact generation and reason, page or halt according to policy, and preserve state for reconciliation.

Kubernetes reports `ProgressDeadlineExceeded` when a Deployment fails to progress within `progressDeadlineSeconds`; current documentation states that the controller continues retrying and does not itself perform an automatic rollback [1]. Operators must not confuse status reporting with recovery.

Serialize incompatible rollouts. If generation 42 is half deployed when 43 arrives, either complete, cancel safely, or define rollover semantics. Every actuation uses compare-and-swap against expected generation. A stale controller for 42 cannot delete a valid 43 unit or reverse its route. Observations without generation identity cannot authorize action.

Pause should stop new impact while leaving a coherent serving population. Cancellation does not imply restoration; it may simply stop further replacement. Record the resulting subjects and capacity. Resume revalidates evidence because dependencies and traffic may have changed while paused.

**Treat rollback as another rollout.** Returning from $V_n$ to $V_o$ again creates a mixed-version window and consumes capacity. It does not undo database writes, emitted events, emails, payments, or device commands. Before rollback, verify that $V_o$ remains available, patched, configured, and able to interpret all current state.

If compatibility has expired, disable the feature or roll forward. A rapid security patch may justify a larger batch and shorter observation window because leaving old vulnerable units also has cost. The policy should make that trade-off explicit rather than silently bypass controls.

**Test the controller.** Exercise wrong digest, slow image pull, unschedulable surge, readiness flapping, false-positive liveness, heterogeneous capacity, dependency connection storm, route lag, stuck stream, failed drain, duplicated job, stale lease, incompatible schema, missing version telemetry, zone loss, autoscaling during replacement, controller restart, stale generation, progress timeout, rollback after state change, and cleanup failure. Recovery starts from observed state and never marks uncertainty as completion.

## Definitions and Notation

Let $V_o$ and $V_n$ be immutable old and new deployment subjects. Let generation $g$ identify the desired transition. Let $N_g(t)$ be the desired population at time $t$, $R_o(t)$ and $R_n(t)$ running non-terminating populations, $A_o(t)$ and $A_n(t)$ available populations, and $T(t)$ terminating units.

For integer surge $S$ and unavailable allowance $U$, a count controller seeks

$$
R_o(t)+R_n(t)\le N_g(t)+S
$$

and

$$
A_o(t)+A_n(t)\ge N_g(t)-U.
$$

Terminating processes may still consume resources even when excluded from the first count. Therefore physical process count can be as high as $R_o+R_n+T$ and must be checked separately.

Let $c_i(t)$ be demonstrated sustainable capacity for available unit $i$, $\lambda(t)$ be demand, and $h$ be required headroom. A necessary capacity gate is

$$
\sum_{i\in Available(t)}c_i(t)\ge(1+h)\lambda(t).
$$

The gate is model-relative: workload mix, burstiness, dependencies, and failure assumptions determine whether $c_i$ is transferable.

Let $P$ bound admission-removal propagation and $L$ bound admitted work lifetime. Under enforced bounds and no work creation after admission closes, $D\ge P+L$ is a conservative drain observation interval. Retries, queues, nested work, and unbounded streams require stronger models.

## Mechanisms, Invariants, or Proof Structure

**Progress condition.** With fixed $N$ and atomic replacement units, at least one of surge or unavailability must be positive. If $S=0$, a candidate cannot be added before an old unit leaves. If $U=0$, an old available unit cannot leave before a candidate becomes available. With both zero, neither first action is permitted, so progress is impossible.

**Count versus capacity counterexample.** Four available units each previously sustain 100 requests/s. A candidate regression reduces two new units to 40 requests/s. The count remains four, but capacity falls from 400 to 280 requests/s. For demand 300, the count invariant passes while the capacity invariant fails.

**Mixed-version invariant.** Suppose a candidate writes value $x$ outside the old reader's accepted domain. During the mixed window, an old unit can read $x$ and fail. Therefore safe rolling replacement requires shared reachable state to remain in the intersection of both versions' accepted domains, or routing and ownership must prevent that interaction.

**Drain argument.** After at most $P$, no new work is admitted to the old unit. Work admitted before convergence ends within $L$. Thus no such work remains after $P+L$, provided work cannot create unbounded descendants and observations cover every path. Violating any premise invalidates the time bound.

**Executable rollout policy.** This deterministic model checks a few invariants and Kubernetes-style percentage rounding. It neither implements Kubernetes nor proves a production rollout safe.

<!-- bijux-verify: {"id":"rolling-deployment-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid_budget=True\nzero_zero_progress=False\nten_replica_unavailable=2\nten_replica_surge=3\nhealthy_batch=allowed\ncount_only_batch=denied:capacity\nunready_candidate=denied:readiness\nincompatible_versions=denied:compatibility\nstale_generation=denied:generation\nrollback_is_rollout=True\nterminating_can_exceed_nominal=True\n","stderr":""}} -->
```python
import math

def batch(readiness, capacity, demand, compatible=True,
          expected_generation=9, actual_generation=9):
    if expected_generation != actual_generation:
        return "denied:generation"
    if not compatible:
        return "denied:compatibility"
    if not readiness:
        return "denied:readiness"
    if capacity < 1.25 * demand:
        return "denied:capacity"
    return "allowed"

n = 10
unavailable = math.floor(n * 0.20)
surge = math.ceil(n * 0.30)
print(f"valid_budget={surge + unavailable >= 1}")
print(f"zero_zero_progress={0 + 0 >= 1}")
print(f"ten_replica_unavailable={unavailable}")
print(f"ten_replica_surge={surge}")
print(f"healthy_batch={batch(True, 1300, 1000)}")
print(f"count_only_batch={batch(True, 1100, 1000)}")
print(f"unready_candidate={batch(False, 1300, 1000)}")
print(f"incompatible_versions={batch(True, 1300, 1000, compatible=False)}")
print(f"stale_generation={batch(True, 1300, 1000, expected_generation=8)}")
print("rollback_is_rollout=True")
nonterminating, desired, allowed_surge, terminating = 12, 10, 2, 2
print(f"terminating_can_exceed_nominal={nonterminating + terminating > desired + allowed_surge}")
```

## Alternatives and Trade-Offs

**Rolling versus blue-green.** Rolling replacement uses bounded extra capacity but keeps versions mixed longer and cannot offer a complete untouched environment. Blue-green prepares a whole target and a retained source at greater resource cost.

**Rolling versus canary.** Rolling describes membership replacement. Canarying describes bounded production evaluation against decision criteria. A controller can pause a rolling deployment after one candidate batch to create canary evidence; continuous immediate rolling is not equivalent.

**Surge-first versus remove-first.** Surge-first preserves serving count and permits candidate proof before retirement, but requires quota and stresses shared dependencies. Remove-first fits fixed capacity but spends availability before candidate evidence.

**Small versus large batches.** Small batches bound correlated impact and make attribution clearer but lengthen mixed-version exposure. Large batches finish faster and may be appropriate for urgent security removal, while increasing blast radius and resource spikes.

**Fixed count versus percentage budget.** Counts are predictable for small fleets. Percentages scale with population but require explicit rounding and can change when autoscaling changes the denominator.

**Readiness-only versus stable-ready availability.** Immediate admission reduces latency. Requiring a stable interval catches crash loops and warm-up oscillation but slows progress. Neither replaces service-level observation.

**Stateless replacement versus state transfer.** Externalized compatible state makes units disposable. Local state transfer can preserve sessions or caches but adds ownership, ordering, corruption, and rollback protocols.

**Automatic rollback versus operator decision.** Automation responds quickly to strong, reversible guardrails. Ambiguous failures and irreversible effects require containment and diagnosis. In all cases, rollback eligibility is checked rather than assumed.

## Failure Modes and Misconceptions

- **“All desired replicas are running, so capacity is safe.”** Running does not imply ready, serving, warm, or sufficiently capable.
- **“Readiness proves correctness.”** a narrow probe can pass while business operations fail.
- **“Liveness should fail under overload.”** restart storms can intensify overload.
- **“Zero surge and zero unavailability is safest.”** it prevents any replacement progress.
- **“Surge affects compute only.”** candidates also consume addresses, pulls, secrets, connections, and quotas.
- **“Desired plus surge bounds every process.”** terminating processes may remain and consume resources.
- **“Stopping routing drains the unit.”** propagation, connections, queues, and jobs can outlive route intent.
- **“Graceful termination guarantees completion.”** applications and clients define effect and retry semantics.
- **“Backward-compatible API means compatible release.”** schemas, messages, caches, claims, and side effects also matter.
- **“Replica shutdown revokes authority.”** delayed processes need lease or fencing enforcement.
- **“Rolling is automatically canarying.”** replacement without evaluation can spread a defect rapidly.
- **“Fleet averages reveal candidate health.”** old units can mask candidate failure.
- **“A progress deadline rolls back.”** a deadline can merely report stalled progress.
- **“Autoscaling makes rollout safer.”** it may mask candidate inefficiency or disrupt batch accounting.
- **“Rollback restores the past.”** it is a new rollout and cannot undo durable effects.
- **“Fast completion minimizes all risk.”** speed shortens mixed-version exposure but reduces observation and enlarges batches.

## Worked Examples

### Example 1

**Prove whether the budget can progress.** A fixed ten-unit service sets $S=0$ and $U=0$. Adding a candidate would produce eleven non-terminating units, violating $N+S=10$. Removing an old available unit first would leave nine, violating $N-U=10$. Conclusion: neither legal first action exists; at least one budget must be positive.

### Example 2

**Apply percentage rounding.** A Kubernetes Deployment has ten desired replicas, `maxUnavailable: 20%`, and `maxSurge: 30%`. Current Kubernetes rules round unavailable down to $\lfloor2\rfloor=2$ and surge up to $\lceil3\rceil=3$ [1]. The controller may target at least eight available and at most thirteen non-terminating Pods during the update. Conclusion: state exact platform rounding before reasoning from percentages.

### Example 3

**Reject count-only capacity.** Four old instances sustain 100 requests/s each. Two are replaced by candidates sustaining only 40 each. Four instances remain available, but total capacity is $2(100)+2(40)=280$ requests/s. With demand 300 and no headroom, the service is already short. Conclusion: equal replica count can hide a 30% capacity loss.

### Example 4

**Include headroom.** Demand is 800 requests/s and policy requires 25% headroom, so available demonstrated capacity must be at least $1.25\cdot800=1000$ requests/s. Eight warm units at 130 requests/s provide 1,040; eight cold candidates at 110 provide 880. Conclusion: readiness of the cold fleet does not satisfy the capacity gate.

### Example 5

**Bound a drain.** Admission removal propagates within 12 seconds and every accepted request has an enforced 45-second deadline. With no queues or descendant work, observe for at least $12+45=57$ seconds and confirm zero new admissions and zero active requests. A WebSocket without a lifetime bound breaks the derivation. Conclusion: time-based draining is valid only when its premises are enforced.

### Example 6

**Prevent schema failure.** Candidate version B adds nullable column `timezone`, old version A ignores it, and both write the old required columns. This additive state remains readable by both. If B instead stores a new required enum value that A rejects, any rolling or rollback window containing A becomes unsafe. Conclusion: deploy expand-compatible representation before candidate dependence; contract only after old readers disappear.

### Example 7

**Fence a singleton.** Old scheduler A holds generation 31; candidate B acquires generation 32. A delayed A process wakes and submits settlement work. The settlement store accepts effects only with current generation 32, so A is rejected even though its process still runs. Conclusion: effect-boundary fencing, not termination timing, preserves single authority.

### Example 8

**Diagnose an overload loop.** Three old units are removed; candidates are cold and exceed readiness latency; traffic concentrates on remaining old units; their latency rises; an aggressive liveness probe restarts them. The correct response is to halt replacement, restore capacity, and separate overload readiness from unrecoverable liveness. Conclusion: probe policy can turn a rollout regression into cascading failure.

### Example 9

**Reconcile a lost command.** The controller times out after requesting candidate C9. On restart it observes C9 running and ready under generation 18. Creating another would exceed surge; assuming failure would stall. It adopts the observed unit, validates its subject and generation, and continues. Conclusion: idempotent reconciliation starts from observed state after uncertain outcomes.

### Example 10

**Reject an unsafe rollback.** At 60% candidate exposure, new workers have emitted messages with semantics the old workers cannot interpret. Errors rise. Replacing candidates with old workers would increase consumers that mishandle queued messages. The team halts expansion, disables production of the new message form, drains or translates the queue, and rolls forward with a compatible reader. Conclusion: an earlier binary is not a valid rollback target after compatibility has expired.

## Cross-Program Connections

- **Platform Engineering:** schedulers, readiness gates, topology rules, autoscalers, and reconcilers implement replacement.
- **Systems Engineering:** capacity models, failure budgets, saturation, and recovery requirements define safe operating envelopes.
- **Distributed Systems:** generations, leases, fencing, idempotency, and partial failure preserve authority.
- **Operating Systems:** signals, process termination, resource pressure, and connection behavior shape draining.
- **Network Engineering:** endpoint propagation, persistent connections, and load balancing separate desired from observed traffic.
- **Database Engineering:** schema and data-domain compatibility determine coexistence and rollback.
- **API and Service Engineering:** wire compatibility, idempotency keys, deadlines, and error semantics govern cross-version calls.
- **Security Engineering:** patch urgency, credential revocation, image identity, and old-version exposure alter rollout policy.
- **Software Architecture:** state placement, singleton work, caching, and dependency boundaries determine replaceability.
- **Testing and Quality Engineering:** failure injection, capacity tests, probe tests, and version-attributed assertions produce evidence.

## References

1. Kubernetes Authors, [“Deployments”](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), current documentation retrieved 2026-09-06. Used for current Kubernetes-specific rolling-update, percentage-rounding, minimum-ready, progress-deadline, and terminating-Pod semantics; not treated as a platform-independent guarantee.
2. Kubernetes Authors, [“Liveness, Readiness, and Startup Probes”](https://kubernetes.io/docs/concepts/workloads/pods/probes/), current documentation retrieved 2026-09-06. Used for current probe purposes and actions.
3. Kubernetes Authors, [“Pod Lifecycle”](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/), current documentation retrieved 2026-09-06. Used for current termination, EndpointSlice, serving-condition, grace-period, and forced-stop behavior.
4. Dinah McNutt, “Release Engineering,” in Betsy Beyer et al., *Site Reliability Engineering*, O'Reilly, 2016, [online edition](https://sre.google/sre-book/release-engineering/); retrieved 2026-09-06.
5. Google SRE, [“Service Best Practices”](https://sre.google/sre-book/service-best-practices/), *Site Reliability Engineering*, O'Reilly, 2016; retrieved 2026-09-06. Used for progressive rollout and risk-bound expansion principles.
6. Alec Warner et al., [“Canarying Releases”](https://sre.google/workbook/canarying-releases/), *The Site Reliability Workbook*, O'Reilly, 2018; retrieved 2026-09-06. Used to distinguish replacement mechanics from evaluated canary exposure.
7. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, Chapters 10 and 12. Used for deployment-pipeline, incremental release, and rollback discipline.
8. Michael Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018. Used for capacity, stability, timeout, and cascading-failure reasoning.
9. IETF, [RFC 9110: *HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), June 2022; retrieved 2026-09-06. Used for durable request and connection vocabulary; orchestrator-specific draining remains implementation-defined.

## Exercises

### Exercise 1

Define rolling deployment, surge, unavailability budget, readiness, availability, draining, mixed-version window, and rollout generation. Explain why running, ready, available, and serving are not synonyms.

### Exercise 2

A service has $N=24$, surge 25%, and unavailability 12.5%. Under Kubernetes rounding rules, calculate $S$, $U$, maximum non-terminating population, and minimum available population. Explain why terminating Pods can make physical process count exceed the first maximum.

### Exercise 3

Six homogeneous old units each sustain 250 requests/s. Demand is 1,000 requests/s and policy requires 20% headroom. Candidate units sustain 160 requests/s during warm-up and 260 afterward. Design a surge-first batch gate and determine how many old units may be removed after two candidates become ready but before they are warm.

### Exercise 4

Design a rolling deployment for an HTTP API, a queue consumer, and a daily billing singleton released together. Cover admission, readiness, messages, schema, draining, retries, version telemetry, and authority.

### Exercise 5

A critical security vulnerability affects the old version. The candidate is wire-compatible but changes a database representation that becomes unreadable by old code after a backfill. Design an accelerated rollout and identify the exact point after which binary rollback is unsafe.

## Answers to the Exercises

### Answer 1

A rolling deployment replaces a population incrementally; surge is temporary population above desired count; an unavailability budget bounds desired capacity allowed to be unavailable; readiness signals current admission eligibility; availability is a controller state that may require stable readiness; draining stops new work and handles bounded work already admitted; the mixed-version window contains both subjects; and rollout generation identifies one desired transition. Running says a process exists. Ready reports a check. Available adds controller policy. Serving means real work can reach and be handled by the unit. Routing delay, warm-up, false probes, or insufficient capacity can make these states differ.

### Answer 2

Surge is $S=\lceil24(0.25)\rceil=6$. Unavailability is $U=\lfloor24(0.125)\rfloor=3$. The target maximum non-terminating population is $24+6=30$, and the minimum available population is $24-3=21$. Terminating Pods can be excluded from the non-terminating count while their processes remain alive during grace and drain, so physical process count can temporarily exceed 30. Quotas and dependency load must account for them separately.

### Answer 3

Required capacity is $1000(1+0.20)=1200$ requests/s. Six old units provide 1,500. Surge two candidates and do not count them as removal capacity merely because readiness passes. If their demonstrated warm-up capacity is 160 each, total with all old units is 1,820. Removing two old units leaves $4(250)+2(160)=1320$, which clears the numerical bound; removing three leaves $3(250)+2(160)=1070$, which fails. Therefore at most two old units may be removed under the given homogeneous assumptions, and a conservative policy may remove fewer because failures, workload mix, and shared dependencies are unmodeled. Once warm, two candidates contribute 520 and support a recalculated next step.

### Answer 4

Bind all three components to one release plan but separate their controllers. The API candidate passes startup, readiness, stable-ready, version identity, and capacity before receiving new requests; old API units leave routing, drain bounded connections, and use idempotency keys for uncertain retries. Messages carry a versioned envelope readable by both consumer versions, stable idempotency identity, and a lease or partition generation; an old consumer finishes or relinquishes its bounded reservation before termination. The database uses additive expand-compatible schema until both API and consumers finish. Billing authority is a fenced generation checked by the durable billing effect boundary, so only one scheduler can charge. Telemetry tags subject and generation for requests, messages, effects, resource use, and errors. Missing signals halt expansion; rollback is allowed only while old readers accept all state and messages.

### Answer 5

First deploy the candidate reader/writer in a mode that preserves the old representation, validate capacity and wire compatibility, and use larger reviewed batches because every remaining old unit carries security exposure. Keep minimum serving capacity, topology tolerance, and version-attributed security and reliability guardrails. After all authoritative readers are candidate-compatible, perform a separately observed backfill. The exact rollback boundary is the first committed state that lies outside the old code's accepted domain—not merely when the backfill starts or ends. Before that boundary, binary rollback can be another accelerated rollout if state and configuration remain compatible. After it, do not reintroduce old code: halt risky writes, contain exposure, and roll forward or translate state. Record the reduced observation interval and residual risk as an explicit emergency policy decision.
