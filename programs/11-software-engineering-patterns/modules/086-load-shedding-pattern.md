---
module_id: SEPAT-086
program: Software Engineering: Patterns
level: 2
module_number: 86
title: Load-Shedding Pattern
status: complete
last_verified: 2026-08-29
---

# Load-Shedding Pattern

## One-Page Review

### Governing question

When offered work exceeds currently sustainable capacity, which work should be rejected, degraded, deferred or abandoned early enough that the system maximizes useful completed outcomes instead of collapsing under wasted work?

### Essential definitions

- **offered load** is the arrival rate/cost presented to an admission boundary, including retries.
- **admitted load** is work allowed past a shed point toward protected resources.
- **sustainable capacity** is the workload-dependent rate/cost the system can complete within its defined correctness/latency/resource objectives.
- **overload** is a state in which offered/admitted work or resource pressure exceeds sustainable progress and tends to grow queues, latency or failure.
- **load shedding** is intentional non-admission or termination of selected work to preserve useful progress under overload.
- **goodput** is useful, correct work completed within the relevant deadline/quality contract per unit time; raw throughput may include useless/late work.
- A **shed point** is an early lifecycle boundary where work can be rejected cheaply and safely.
- A **criticality class** is an authenticated policy category describing consequence/value of completing or rejecting work.
- **graceful degradation** serves a cheaper, explicitly lower-quality result rather than the full operation.
- **hysteresis** uses different activation/recovery conditions so noisy pressure does not flap shedding on and off.

### Central model, mechanism, or theorem

For homogeneous offered rate λo and sustainable service rate μ, a necessary ideal admission condition is λa≤μ. If a fraction f is shed uniformly before expensive work,

$$
\lambda_a=(1-f)\lambda_o,
\qquad
f\ge 1-\frac{\mu}{\lambda_o}
$$

when λo>μ. This is a lower-bound planning calculation, not a controller: work costs differ, μ changes with state, signals lag, and rejection itself costs resources. The production objective is not maximum accepted traffic but maximum goodput subject to criticality, fairness, correctness and resource/safety limits. Once work has consumed expensive resources, shedding it may decrease goodput and encourage retries; reject as early as enough information permits and finish bounded useful admitted work where safe.

### Critical invariants

- Shed decisions protect a named local resource/dependency and use signals measured at an appropriate scope.
- The shedding path is cheaper and more reliable than the work it rejects; it does not require the saturated dependency.
- Admission occurs before large body allocation, queueing, fan-out or irreversible effects where protocol/security allows.
- Offered, admitted, rejected, degraded, late and useful-completed work are accounted separately.
- Criticality/priority is authenticated, finite and abuse-resistant; no class has an unbounded bypass.
- Queue count, bytes and age remain finite; expired work is not started merely because it was accepted earlier.
- Work already issued with ambiguous effects is reconciled; shedding/cancellation never claims rollback.
- Retry behavior distinguishes local-task imbalance from cluster-wide overload and obeys one retry owner/budget.
- Activation and recovery use tested thresholds/hysteresis/ramp so fleets do not oscillate or release a recovery herd.
- Protected work actually meets its outcome/latency objective under overload; rejection counts alone prove nothing.

### Common failures

Common failures include waiting for CPU=100% after latency has collapsed, using one aggregate CPU signal while memory/queue/connection pressure binds, rejecting after request-body parsing or database mutation, a shed path that synchronously logs to the failing store, treating every request equal despite cost/criticality, trusting client priority headers, dropping old issued mutations without reconciliation, large FIFO queues that ensure stale work, retrying every `503` at every layer, shifting all load to another already stressed region, an expensive fallback that doubles dependency work, hysteresis-free threshold flapping, synchronized recovery, health checks sharing the rejected worker pool, shed metrics with raw tenant cardinality, and claiming availability by counting degraded/default results as authoritative success.

### Compact example

A search service becomes nonlinear near 800 active cost units: queue delay and executor load rise before CPU saturates. At the header/route boundary it authenticates a bounded request envelope and classifies critical account lookup, standard search and optional recommendations. Above the high watermark it disables recommendations, rejects expensive anonymous searches and preserves finite authenticated standard/critical shares. It does not buffer rejected bodies or call downstream ranking. Recovery begins only below a lower watermark for a sustained interval and ramps admission with jitter. Responses label degraded/search coverage truthfully and instruct only bounded clients how to retry.

### Connections

[SEPAT-082](082-timeout-and-deadline.md) identifies stale/unfinishable work, [SEPAT-083](083-circuit-breaker.md) suppresses likely dependency failures, [SEPAT-084](084-bulkhead.md) preserves isolated capacity, and [SEPAT-085](085-rate-limiter.md) enforces temporal policy. Load shedding reacts to current overload and composes with all four.

## Governing Question

How should a service sense the onset of nonlinear overload, select valuable feasible work, reject cheaply, communicate truthfully and recover without turning partial overload into a fleet-wide retry or failover cascade?

Load shedding is controlled sacrifice. A well-designed service rejects some work so that the work it accepts finishes usefully. A poorly designed service accepts everything, completes little before caller deadlines and may crash or fail health checks, moving traffic to equally stressed peers. The difficult parts are trustworthy signals, decision location, workload value/cost, retry semantics and evidence beyond the knee of the capacity curve.

## Why This Matters

As utilization rises, systems rarely slow linearly. Queueing, context switching, lock contention, garbage collection, cache churn, I/O contention and downstream latency can create a knee where more offered load reduces useful completions. Longer residence increases in-flight memory/threads/connections; clients time out and retry; late server work is wasted; load amplifies itself.

Autoscaling and capacity planning remain primary, but reaction time, hard quotas, correlated failure, cold starts, flash crowds, attacks and dependency impairment make overload protection necessary. Shedding should be an exercised safety valve, not an excuse to underprovision. Its product and ethical consequences matter: deciding who loses service requires explicit criticality/fairness rather than accidental queue order.

## Prerequisites and Retrieval

Learners should retrieve:

- queueing, utilization, Little's Law, latency distributions and nonlinear saturation;
- executor/event-loop load, CPU, memory, connections and downstream quotas;
- finite queues, priority/fair scheduling and starvation;
- deadlines, cancellation, retry budgets and ambiguous effects;
- rate limiting, bulkheads, circuit breakers and autoscaling;
- authentication/authorization, denial-of-service defense and privacy;
- feedback control, smoothing, hysteresis and fault-injection testing.

Before continuing, explain why completing 600 useful requests/s and rejecting 400 early can be better than accepting 1,000 and completing only 400 before their deadlines.

## Learning Objectives

After this module, learners can:

1. distinguish offered load, admitted load, raw throughput, goodput and sustainable capacity;
2. identify resource/workload-specific overload signals and their lag/failure modes;
3. place cheap shed points through connection, request, queue and dependency lifecycles;
4. design authenticated criticality, cost, deadline-feasibility and fairness policies;
5. specify reject, degrade, bounded defer and already-issued-work behavior;
6. prevent retry, failover and recovery amplification;
7. use smoothing, hysteresis, probabilistic/stable selection and admission ramp safely;
8. verify protected goodput and correctness beyond saturation under realistic faults;
9. reason about security, high-stakes fail-safe modes and named human review.

## Core Exposition

### Define overload at a boundary

“The system is overloaded” is too broad. Name the resource owner and scope: one process executor, event loop, heap/cgroup, connection pool, dependency, shard, cell, zone or entire fleet. A task-local signal should protect that task; a fleet signal may coordinate routing but arrives slower and can be unavailable. Local and global protection often coexist.

Define work unit/cost, completion deadline/quality, sustainable goodput and which resource becomes unsafe. Load test the knee and failure mode. Capacity is conditional on payload, cache state, fan-out, dependency latency, deployment, hardware and feature configuration. A scalar requests/s value is not portable across workloads.

Overload signals include:

- active/runnable executor work relative to processors;
- event-loop lag and callback backlog;
- in-flight operations and queue count/bytes/oldest age;
- CPU throttling, memory/heap pressure and garbage-collection pause/debt;
- connection/file-descriptor/buffer/pool saturation;
- dependency latency, timeout, quota and circuit/bulkhead state;
- remaining-deadline distribution and late-result rate;
- goodput decline despite rising offered work.

CPU can be low while threads block on a dependency; memory can fail before CPU; average fleet utilization can hide one hot shard. Combine a small set of causal/local signals with explicit semantics. Avoid a complex opaque score unless its stability and failure behavior are validated.

### Detection lag, smoothing and hysteresis

Instantaneous signals are noisy; heavy smoothing reacts too late. Define sample interval, estimator/window and activation/recovery conditions. A high watermark H activates shedding. A lower watermark L<H plus a stable recovery duration exits it. This hysteresis prevents oscillation near one threshold.

Some shed points need per-request current decisions rather than a periodically toggled mode. Envoy's overload manager, for example, distinguishes resource-triggered actions and lifecycle shed points. Exact platform behavior is deployment/version specific.

Thresholds should preserve headroom before the nonlinear knee. Activating only after resource exhaustion makes the shed path compete for unavailable resources. Test sensor failure: missing memory limit, stalled metrics thread, clock pause or stale fleet aggregate. Conservative local hard bounds remain even if adaptive control fails.

### Place shed points early and progressively

Potential points include:

1. before accepting a new connection;
2. after minimal protocol headers but before request/filter chain/body allocation;
3. after bounded authentication/route/criticality classification;
4. before enqueueing or acquiring a bulkhead/dependency permit;
5. before expensive fan-out or optional features;
6. while queued, when deadline/age makes completion useless;
7. at streaming increments when cost/budget is exhausted.

Earlier rejection is cheaper but has less semantic information. Pre-auth defenses can use coarse network/global policy; post-auth shedding can be fair by tenant and criticality. Bound the work required to authenticate—otherwise attackers overload the classifier. Limit headers/body size and parsing cost before admission.

Do not start irreversible work and then shed it as if nothing happened. Once a mutation or external effect is issued, continue/reap/reconcile according to its durable state machine, even if the caller no longer waits. For pure cancellable compute, stopping low-value work can free capacity, but cancellation overhead and partial results must be understood.

### Goodput and deadline feasibility

Raw throughput counts operations processed/rejected or responses emitted; goodput counts correct useful outcomes within contract. Track:

$$
G=\frac{\text{useful terminal outcomes completed within contract}}{\text{time}}.
$$

A server can report high throughput by quickly returning errors, or consume high CPU completing results after caller deadlines. Neither is desired. Observe offered, admitted, shed, degraded, timed-out, abandoned, effect-uncertain and useful-completed work separately.

Deadline-aware admission estimates whether minimum useful service plus response/reconciliation reserve fits remaining time. Queue age/remaining slack can be more predictive than queue length. An estimate can be wrong, so maintain hard capacity bounds and record false admission/rejection outcomes. Do not discriminate against naturally expensive but important work solely because “shortest job first” maximizes count; value and fairness are policy.

### Shedding fraction and cost

For homogeneous work under a known offered rate λo and sustainable μ, the ideal minimum uniform fraction is f≥1−μ/λo. At λo=1,200/s and μ=750/s, f≥1−750/1,200=0.375, or 37.5%. The real controller needs margin because rejection costs, measurement lag, cost variance and μ degradation are omitted.

For weighted work, compare offered cost rate $\sum_j \lambda_j c_j$ with sustainable resource-cost rate. Shedding ten cheap requests may free less capacity than one expensive fan-out. Cost estimates must be bounded and resistant to manipulation; unknown streaming/output cost requires incremental admission or hard limits.

Deterministic stable selection by hash/tenant can preserve a consistent served cohort and reduce client flapping, but may repeatedly exclude the same users. Random shedding spreads pain probabilistically but one client may see unstable outcomes. Weighted fair/criticality scheduling provides explicit shares. Choose based on product/fairness and test distributions.

### Criticality, fairness and security

Criticality derives from authenticated operation semantics and consequence, not user-controlled priority. A practical hierarchy might include life/safety or control-plane work, committed-effect reconciliation, interactive authenticated work, best-effort anonymous work and optional/background features. Every class is finite; a flood of critical work can itself overload and may need independent bulkheads/subclasses.

Strict priority can starve lower classes. Reserve critical capacity, weighted shares, per-tenant floors/ceilings and aging where appropriate. State what progress noncritical work receives during prolonged pressure. Stable cohort shedding should rotate or provide an explicit fairness mechanism if continuous exclusion is unacceptable.

Attackers can manipulate expensive routes, key cardinality, retries and telemetry. Reject before expensive work, authenticate priority, cap payload/fan-out, protect observability, separate abuse controls from legitimate overload and avoid responses that reveal sensitive capacity/tenant state.

### Reject, degrade or defer

**Reject** when the interactive result cannot be served safely/usefully. HTTP services often use `503 Service Unavailable` for current service overload and may use `Retry-After` when recovery timing is meaningful; platform/application contracts vary. A rate-policy violation commonly uses `429`. Stable machine reasons distinguish local task overload, cluster overload, rate/quota and dependency unavailability without leaking topology.

**Degrade** when a cheaper result retains explicit value: fewer search shards/features, cached snapshot with age, lower resolution, partial optional fields. Do not fabricate authority, bypass revocation/security, or call an equally expensive fallback. Measure degraded quality/cost and keep the path exercised. Complex rarely used fallback can fail bimodally during incidents.

**Defer durably** only if the public contract permits asynchronous completion. Persist ownership before acknowledging; bound backlog count/bytes/age/tenants; use leases, idempotency and status. An in-memory “try later” queue is not durable acceptance.

**Finish admitted work** when bounded and still useful, especially after expensive progress. Rejecting new work often protects existing goodput better than cancelling everything. Stop optional future stages and avoid wasted late work. Effects already issued require reconciliation.

### Retry and upstream control

Shedding reduces server work only if clients do not immediately multiply it. Provide overload disposition and retry advice based on scope:

- a single task overloaded while peers have capacity may justify one load-balanced attempt under a budget;
- broad cluster/dependency overload should surface a do-not-retry/deadline-aware response;
- only the immediately upstream layer retries; higher layers receive terminal/degraded result;
- retries count in offered load and are shed like new work, often with a global retry ratio/token budget;
- backoff, jitter and absolute deadline remain mandatory.

The smaller/receiving service should control pace via rejection, pull, credits, queue demand or concurrency limits rather than relying solely on a larger caller's stale capacity estimate. Routing load away can overload alternatives; failover budgets and static headroom are necessary.

### Recovery

Do not remove shedding as soon as one sample improves. Require pressure below L for a stable period, then ramp admission. Continue jitter/backpressure and keep bulkhead/rate policies. Cold caches, connection establishment, JIT and queued clients make recovery capacity lower initially.

Fleet instances can synchronize modes. Jitter thresholds/timers where appropriate, coordinate only when needed, and preserve local protection if control plane fails. Configuration changes need versioning, audit, staged rollout and emergency disable that does not eliminate hard resource bounds.

### Deterministic hysteresis and criticality model

The following finite model activates shedding at pressure 900 milli-units and exits at or below 700. Optional work is rejected while shedding; critical work remains admitted in this small trace. It performs no real resource measurement.

<!-- bijux-verify: {"id":"sepat-086-shedding-hysteresis","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"pressures=650,820,920,850,680\nstates=normal,normal,shedding,shedding,normal\noptional=admit,admit,shed,shed,admit\ncritical=admit,admit,admit,admit,admit\nminimum_uniform_shed_percent=37.5\n","stderr":""}} -->
```python
def next_state(state, pressure, enter=900, exit_at=700):
    if state == "normal" and pressure >= enter:
        return "shedding"
    if state == "shedding" and pressure <= exit_at:
        return "normal"
    return state


def decision(state, criticality):
    if state == "shedding" and criticality == "optional":
        return "shed"
    return "admit"


pressures = [650, 820, 920, 850, 680]
state = "normal"
states = []
optional = []
critical = []

for pressure in pressures:
    state = next_state(state, pressure)
    states.append(state)
    optional.append(decision(state, "optional"))
    critical.append(decision(state, "critical"))

print("pressures=" + ",".join(str(value) for value in pressures))
print("states=" + ",".join(states))
print("optional=" + ",".join(optional))
print("critical=" + ",".join(critical))
print("minimum_uniform_shed_percent=" + str(round(100 * (1 - 750 / 1200), 1)))
```

This execution proves exact branch/arithmetic behavior for fixed samples only. It omits concurrency, noisy/lagged sensors, costs, queues, deadlines, authentication, fairness, effects, retries, distribution, actual rejection cost, protected goodput and safety.

### Observability and verification

Per bounded resource/task/class record offered/admitted/shed/degraded/durable-deferred cost and requests, signal values/age, state/threshold/config version, shed point, reason, queue/in-flight/resource pressure, remaining deadline, retry marker, response cost and useful terminal outcome. Protect cardinality and privacy. Dashboard aggregate and per-cell/shard distributions; averages hide hot instances.

Measure goodput and the capacity curve: ramp beyond expected peak until rejection then far beyond, while holding workload mix/payload/cache/dependency conditions. Verify the service plateaus useful completion rather than collapsing. Include sudden step load, slow ramp, expensive-request skew, partial task/cell imbalance, dependency slowdown, memory pressure, GC, control-plane/sensor failure, attack and recovery.

Required checks include:

- exact high/low thresholds, equality, noisy samples and missing/stale signal;
- shed path operates with dependency/logging/telemetry impairment;
- rejection happens before named expensive allocations/effects;
- finite queue count/bytes/age and stale-deadline eviction;
- authenticated criticality, tenant shares, starvation/priority abuse;
- cost-aware and stable/random selection distributions;
- admitted work completes within contract and effect uncertainty is reconciled;
- retry amplification stays within attempt/ratio budgets;
- failover cannot exceed alternative capacity;
- recovery hysteresis, ramp, cold state and fleet synchronization;
- shutdown and configuration rollout preserve hard protection.

Fault/load tests stay in isolated owned environments. A deterministic policy unit test or high rejection rate cannot prove overload survival.

## Definitions and Notation

Let offered/admitted rates be λo and λa, sustainable capacity μ, uniform shed fraction f, class j cost cⱼ and offered cost rate Λ=Σⱼλⱼcⱼ. Let signal vector z(t), enter threshold H, exit threshold L<H, and shedding state S(t). Let G be useful correct outcomes completed within contract per unit time.

Let operation identity/generation/effect state distinguish non-admitted work from admitted/issued ambiguous work. A shed outcome is local admission truth, not a statement about a previously issued remote effect.

## Mechanisms, Invariants, or Proof Structure

**Ideal admission bound.** For homogeneous work, if f≥1−μ/λo and rejection occurs before protected service with negligible cost, λa≤μ. Real systems require margin because assumptions fail.

**Queue instability.** Persistent λa>μ makes backlog grow without bound in the fluid idealization; a finite queue eventually fills. Shedding bounds admission/backlog but does not create μ.

**Goodput preservation condition.** If rejection cost is lower than full failed/late work and λa is held in the region where admitted work completes usefully, early shedding can yield greater G than accept-all collapse. This is conditional and must be measured.

**Hysteresis.** With enter H and exit L<H, signal variation entirely inside (L,H) cannot by itself toggle state. Large/noisy crossings still can; recovery dwell/ramp adds stability.

**Priority safety.** If critical admission is authenticated and independently finite, noncritical shedding can preserve its allocation. If critical work is unbounded or shares a saturated residual resource, the guarantee fails.

**No effect rollback.** Non-admission proves no protected effect only when shed occurs before issue. After issue, timeout/cancellation/shedding cannot imply absence of effect without an effect protocol.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation |
|---|---|---|
| proactive capacity/autoscaling | demand can be forecast and scale lead time fits | quotas/cold start/correlated faults remain |
| configured rate limiter | contractual temporal fairness/capacity is known | may not react to current slowdowns |
| concurrency bulkhead | in-flight resources/blast radius need hard bounds | saturation response still required |
| circuit breaker | dependency calls are recently likely to fail | detection interval/other overload remains |
| early rejection | interactive work cannot wait usefully | availability loss must be explicit |
| graceful degradation | cheaper result retains real value | complexity, stale/security/quality risks |
| finite priority queue | short bursts can wait and ordering has value | latency/memory; persistent overload fills it |
| durable defer | accepted work may complete asynchronously | backlog/idempotency/operations burden |
| routing/failover | independent destination has proven spare capacity | can transfer/correlate overload |
| constant-work design | demand-sensitive amplification can be removed | may cost more in normal state; not sufficient alone |

## Failure Modes and Misconceptions

- **Overload means high CPU.** Memory, queues, locks, connections or dependency latency may bind first.
- **Shedding means random 503s.** Signal, cost, value, fairness and retry semantics matter.
- **Rate limiting and shedding are identical.** One enforces temporal policy; one responds to current pressure.
- **Accepting more improves availability.** Late/wasted work can reduce goodput.
- **Queueing saves bursts.** Persistent overload turns queues into latency/memory failures.
- **Cancel oldest work always helps.** Issued effects/expensive progress may require completion/reconciliation.
- **Priority header identifies critical work.** Criticality is authenticated domain policy.
- **Critical traffic can bypass all limits.** It can overload too and must be finite.
- **Fallback is free.** It can be more expensive, stale, insecure or untested.
- **One high threshold is enough.** Detection can be late and recovery can flap.
- **Retry elsewhere fixes local overload.** It may overload peers/regions and multiply calls.
- **503 is always retryable.** Scope and explicit disposition/budget decide.
- **Autoscaling eliminates shedding.** Reaction/cold-start/dependency limits remain.
- **Rejection metrics prove resilience.** Protected goodput/latency/correctness must pass.
- **Normal-load tests cover degraded mode.** Rare code paths require continuous exercise.

## Worked Examples

### Example 1

A service accepts 1,200 homogeneous requests/s but sustains 750/s before the knee. The ideal minimum uniform fraction is 37.5%. Tests choose more margin because rejection costs 2% CPU and request cost varies. They verify useful completions plateau near the safe region rather than collapse.

### Example 2

CPU is 45%, yet all 40 database connections are occupied by slow calls and request threads queue. CPU-only control fails. The dependency bulkhead/in-flight/queue-age signals shed before connection acquisition; unrelated cached reads retain isolated capacity.

### Example 3

The gateway buffers 100 MiB uploads before checking memory pressure. Returning 503 afterward does not protect memory/network. It enforces header/auth/content-length/count/byte admission before body buffering and uses streaming incremental limits for unknown length.

### Example 4

A FIFO queue contains requests whose deadlines expired behind one slow item. Workers discard expired/generation-stale pure reads before service and track wasted wait. Already issued payment commands are not dropped; durable identities are reconciled.

### Example 5

Randomly rejecting 40% makes every user experience intermittent failure. Stable hash cohorts preserve consistent service for 60% but continually exclude 40%. Product policy instead uses per-tenant fair shares plus optional-feature shedding, with rotation/aging where long exclusion is unacceptable.

### Example 6

An attacker marks every request `critical`. The service derives class from authenticated principal, operation, current authority and safety policy. Critical work has its own finite bulkhead/rate; abuse cannot consume emergency reserve or create unbounded telemetry labels.

### Example 7

Each shed request is retried by SDK, service mesh and two application layers. One rejection becomes many. The immediate upstream owns one bounded retry only for local-task imbalance; cluster-overload disposition stops retries, and global retry ratio/token budgets count attempts.

### Example 8

Search degradation skips recommendations and searches fewer shards. Responses label coverage, snapshot age and omitted features. Authorization/revocation stays authoritative. Load tests prove degraded cost is lower; it does not call a cold backup that would double work.

### Example 9

Pressure falls below the high threshold for one sample and all instances admit fully, rebuilding the queue. Hysteresis requires sustained pressure below a lower threshold, then ramps each instance with jitter while caches/connections warm and downstream headroom is observed.

### Example 10

An emergency platform sheds noncritical telemetry transformations first, then bounded routine updates, while preserving authenticated command, acknowledgement and reconciliation capacity. It never fabricates safe sensor values. Hardware-in-loop tests combine telemetry flood, network/controller impairment, stale commands and limiter/control-plane failure to prove hazard-defined fail-safe behavior.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): critical flows, choke points, degradation and blast radius.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): beyond-knee load, fault, controller and fairness tests.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): scheduler/executor load, memory pressure, file descriptors and queues.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): DoS, priority authorization, key/cost manipulation and telemetry privacy.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): overload cascades, retries, failover, partial effects and recovery coordination.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): proxy shed points, autoscaling, fleet signals and staged configuration.

## References

1. Yanacek, David. “Using Load Shedding to Avoid Overload.” Amazon Builders' Library. <https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/>
2. Google. “Handling Overload.” *Site Reliability Engineering*, Chapter 21. <https://sre.google/sre-book/handling-overload/>
3. Google. “Addressing Cascading Failures.” *Site Reliability Engineering*, Chapter 22. <https://sre.google/sre-book/addressing-cascading-failures/>
4. Envoy Authors. “Overload Manager.” <https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager>
5. Magerramov, Joe. “Avoiding Overload in Distributed Systems by Putting the Smaller Service in Control.” Amazon Builders' Library. <https://aws.amazon.com/builders-library/avoiding-overload-in-distributed-systems-by-putting-the-smaller-service-in-control/>
6. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018.
7. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013.
8. Jain, Raj. *The Art of Computer Systems Performance Analysis*. Wiley, 1991.
9. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020.
10. Nichols, Kathleen, and Van Jacobson. “Controlling Queue Delay.” *Communications of the ACM* 55(7), 2012.
11. Fielding, Roy T., Mark Nottingham, and Julian Reschke. “HTTP Semantics.” RFC 9110. <https://www.rfc-editor.org/rfc/rfc9110>
12. OpenTelemetry Authors. “Semantic Conventions.” <https://opentelemetry.io/docs/specs/semconv/>

Overload signals, shed points, status mappings and platform actions vary by implementation/version. Current official sources were checked on 2026-08-29; verify exact deployed behavior and workload capacity.

## Exercises

### Exercise 1

Design load shedding for an API with critical account commands, standard searches, optional recommendations and large uploads. Define signals, shed points, cost/criticality/fairness, degradation, retry, recovery and evidence.

### Exercise 2

Homogeneous offered load is 2,000 requests/s and measured sustainable service is 1,250/s with rejection cost assumed negligible. Compute the ideal minimum uniform shed fraction and admitted rate. If request cost splits equally by count into cost 1 and cost 5, explain why uniform-by-count shedding can be wrong.

### Exercise 3

A stable service admits 700/s. Mean residence rises from 0.1 s to 1.2 s during dependency slowdown. Compute mean residents before/after using Little's Law and describe signals/shed points that react before collapse.

### Exercise 4

Diagnose a system that sheds at CPU 100% after body parsing and database dispatch, trusts priority headers, queues without byte/age limits, retries at three layers, reports cache fallback as fresh, uses one threshold and releases all traffic immediately on recovery. Redesign and specify decisive tests.

### Exercise 5

Design shedding/fail-safe behavior for a safety-critical command and telemetry system. Include criticality authority, irreversible effects, shared failures, overload/attack, evidence and named review.

## Answers to the Exercises

### Answer 1

Use process-local executor/event-loop, memory/body-byte, in-flight/queue-age and dependency/bulkhead signals plus global/cell context. Establish high/low thresholds and dwell/ramp from beyond-knee tests. At connection/header stage apply coarse global/network limits; after bounded authentication classify tenant/operation before body allocation. Enforce upload byte/stream budgets before buffering.

Critical commands have authenticated finite reserve and effect-aware handling; standard searches receive tenant-fair capacity; recommendations are disabled first; expensive anonymous searches/uploads reject. Searches may degrade shard/feature coverage with explicit metadata; commands never fabricate success. Queue count/bytes/age/deadline are finite. Issued mutations finish/reconcile rather than being labelled rolled back.

Return stable overload disposition with deadline-aware advice; one immediate upstream owns bounded retry only for proven local imbalance, while cluster overload is do-not-retry. Recovery requires lower threshold/dwell, jittered ramp and downstream/cold-cache validation. Tests sweep past knee with workload mix, dependency/memory faults, retries, key/priority attacks, cell imbalance and recovery while measuring protected goodput/latency/correctness.

### Answer 2

The ideal minimum is

$$
f\ge1-\frac{1250}{2000}=0.375=37.5\%.
$$

Uniform shedding at exactly 37.5% gives admitted rate (1−0.375)2,000=1,250 requests/s under homogeneous negligible-rejection assumptions.

With equal request counts but costs 1 and 5, total offered resource cost is dominated by cost-5 work. Uniform-by-count random rejection has variable freed cost and may reject many cheap/high-value requests while retaining expensive/optional ones. Use weighted cost and criticality/fair shares; sustainable capacity must be expressed in the binding resource unit, not request count. Cost estimates, rejection overhead and changing μ require margin and empirical control.

### Answer 3

Initially L=700×0.1=70 mean resident requests. During slowdown L=700×1.2=840—twelve times as many at the defined stable boundary, if stability still holds. This increase consumes memory, connections, threads and queue space and can create retries.

React to dependency in-flight/pool saturation, queue count/bytes/oldest age, executor/event-loop load, remaining-deadline/late-outcome rate and perhaps memory pressure—not only CPU. Shed before enqueue/acquiring the dependency or expensive fan-out; stop optional stages; expire stale queued pure work; preserve isolated critical capacity. A circuit breaker may suppress persistent dependency failure and a bulkhead hard-bounds concurrency.

### Answer 4

CPU-only activation is late and misses blocking/memory/connection overload. Post-body/dispatch rejection already spent resources and leaves ambiguous effects. Forgeable priority steals reserve. Unbounded queue retains memory/stale work. Three retry owners amplify load. Unlabelled cache fallback lies. One threshold flaps; full recovery creates a herd.

Add local multidimensional signals/headroom, high/low+dwell+ramp, and early coarse then authenticated shed points before body/dependency work. Bound queue count/bytes/age/deadline. Derive criticality from authenticated domain policy with finite per-class/tenant bulkheads. Track issued effects durably. Assign one retry owner plus attempt/ratio budgets. Label cache age/authority and verify its cost/security. Ramp recovery with jitter/cold-dependency evidence.

Tests cover each signal and sensor failure, exact/noisy thresholds, early work-allocation counters, body attacks, priority forgery/starvation, queue bounds/expiry, effect-response loss, layered retry elimination, degraded truth/security, fleet/cell imbalance, failover capacity, cold recovery and shutdown. The decisive oracle is protected useful completion/latency/correctness beyond the knee, not shed count.

### Answer 5

Classify authenticated emergency commands, acknowledgements/effect reconciliation, routine controls and noncritical telemetry transformation/storage. Each has finite isolated CPU/memory/communications/controller/device capacity; priority derives from signed authority, safety state, device generation/sequence and validity deadline. Attackers cannot self-promote. Telemetry floods shed before decoding/storage and cannot consume command reserve.

Never shed an already issued irreversible command as “not executed.” Durable command/effect state distinguishes reserved, issued, acknowledged, observed and uncertain; expiry/cancellation blocks future safe work but reconciliation continues. Missing telemetry enters a hazard-defined unknown/degraded/fail-safe state, never a fabricated normal value. Shared identity/time/network/power/control-plane failures are named residual risks.

Evidence includes formal timed resource/state/effect model, worst-case schedulability/capacity, model checking where feasible, hardware-in-loop overload/priority/effect races, telemetry and distributed-key attacks, network/controller/device/time/power/control-plane faults, fail-safe/recovery drills and protected audit. Approval requires named domain safety, controls, hardware, communications/real-time, distributed systems, security, reliability/operations, human-factors and regulatory reviewers with traceable hazards and acceptance criteria.
