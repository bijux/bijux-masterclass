---
module_id: SEPAT-083
program: Software Engineering: Patterns
level: 2
module_number: 83
title: Circuit Breaker
status: complete
last_verified: 2026-08-29
---

# Circuit Breaker

## One-Page Review

### Governing question

When recent evidence says a dependency call is unlikely to succeed, how can a caller stop spending scarce time and capacity, then test recovery without turning half-open state into a new traffic surge?

### Essential definitions

- A **circuit breaker** is a stateful admission policy around a dependency operation; it is not an electrical safety device or a health oracle.
- **Closed** state admits calls and records classified recent outcomes.
- **Open** state short-circuits eligible calls without invoking the protected dependency.
- **Half-open** state admits a bounded number of owned recovery probes while other calls remain rejected or explicitly degraded.
- A **breaker key** identifies the narrow dependency/resource/operation/tenant scope whose outcomes share one state machine.
- A **recordable outcome** is a result that policy classifies as evidence about dependency availability or latency.
- A **sliding window** is a bounded recent population by count or time used to calculate failure/slow-call evidence.
- A **minimum sample size** prevents a small number of calls from producing an unstable percentage decision.
- An **open interval** is the earliest time before which no recovery probe is admitted.
- A **probe lease** is the concurrency-safe ownership token for a half-open trial; every lease must terminate as success, failure, timeout, cancellation, or abandonment.

### Central model, mechanism, or theorem

For N recorded calls with F classified failures, the observed failure rate is

\[
\hat p_f=\frac{F}{N}.
\]

A simple policy opens only if N ≥ Nmin and p̂f ≥ θf; a separate slow-call rule may use S/N ≥ θs. The decision is conditional evidence, not a proof that the dependency is down. Open state reduces protected-call admission toward zero. After a bounded interval, at most H half-open probe leases are issued. Probe results atomically decide whether to reopen, remain half-open under an exact rule, or close and begin a fresh observation epoch.

### Critical invariants

- Breaker scope matches failure independence: unrelated shards, regions, tenants or operations do not poison one another accidentally.
- Only configured dependency/latency outcomes affect the breaker; business, authentication, validation and caller-cancellation failures are classified separately.
- Closed-state evidence is finite, recent and requires a stated minimum population.
- State transition and probe-lease accounting are atomic under concurrency.
- Open calls do not reach the protected dependency and are distinguishable from dependency failures.
- Half-open concurrency, count, deadline and workload are bounded; ordinary traffic is not an uncontrolled probe flood.
- Every admitted call retains its own deadline, cancellation, retry/effect and capacity policy.
- Success never resets an unrelated breaker, and stale completions cannot close a newer open epoch.
- Fallback/degradation is truthful about freshness, completeness and authority; a default is not fabricated success.
- Manual force-open/close/reset is authenticated, audited, scoped, expiring where appropriate and safe under races.

### Common failures

Common failures include one global breaker for all dependencies, counting every exception, opening on one cold-start call, using lifetime totals that never forget an incident, resetting consecutive failures on every success, allowing all waiting calls into half-open state, probing with an unsafe mutation, using a health endpoint that does not exercise the failed path, letting cancelled probes consume leases forever, treating open as a retryable transient and spinning, stacking application/mesh/SDK breakers with conflicting state, returning stale data as current, closing on a late success from an old epoch, persisting breaker state forever across deployment, and claiming that a breaker supplies timeout, bulkhead, rate limit or correctness by itself.

### Compact example

A checkout service calls three independent payment regions. Breakers are keyed by region and authorization operation, not by the payment brand globally. A 20-call window with at least 10 samples opens at 60% classified dependency failure. Open state fails fast for 15 seconds. Then one idempotent status-read probe with a 300 ms deadline is leased; other calls remain rejected. A probe failure reopens with a new epoch; two policy-required successes close. Payment declines and invalid cards remain business outcomes and never trip the breaker.

### Connections

[SEPAT-081](081-retry-with-bounded-backoff.md) supplies bounded retry semantics and [SEPAT-082](082-timeout-and-deadline.md) supplies inherited time budgets. Circuit Breaker composes with forthcoming Bulkhead, Rate Limiter, Load-Shedding and resilience-composition modules, but cannot replace them.

## Governing Question

How should a concurrent system convert recent, correctly classified dependency evidence into temporary call suppression and controlled recovery while preserving truthful outcomes, independent failure domains and end-to-end ownership?

A circuit breaker is a feedback controller with deliberately coarse state. Its useful behavior is not merely “throw after five errors.” It must define what population is observed, which outcomes mean dependency impairment, whose traffic shares state, who owns a recovery probe, how old results are rejected, and what callers observe while access is suppressed.

## Why This Matters

Remote calls can tie up threads, connections, buffers and caller deadlines while a dependency is persistently unhealthy. Retrying likely failures magnifies load. A breaker makes the caller fail fast during an evidence-backed interval, conserving some work and giving the dependency room to recover. However, an incorrectly scoped breaker creates correlated denial of service: one bad shard can block healthy shards, one tenant can poison everyone, or a recovery spike can re-break a healthy dependency.

The pattern also changes public semantics. An open decision is local policy evidence, not a response from the dependency. Cached or default fallback may be useful, but it cannot silently claim current authoritative data. For mutations with ambiguous outcomes, open state stops new calls but does not resolve effects already dispatched.

## Prerequisites and Retrieval

Learners should retrieve:

- finite-state machines, atomic transitions, epochs/generations and leases;
- proportions, sampling error, count/time windows and base rates;
- partial failure, independent failure domains and ambiguous outcomes;
- deadlines, cancellation, retry budgets and idempotency;
- concurrency limits, queueing, overload and backpressure;
- metrics cardinality, traces and fault injection;
- [Retry with Bounded Backoff](081-retry-with-bounded-backoff.md) and [Timeout and Deadline](082-timeout-and-deadline.md).

Before proceeding, explain why a client-observed timeout can be breaker evidence under policy but cannot prove that a remote mutation did not commit.

## Learning Objectives

After this module, learners can:

1. specify closed, open and half-open transitions as a concurrency-safe state machine;
2. define breaker keys from actual failure independence and dependency ownership;
3. classify recordable success, failure, slow, ignored and ambiguous outcomes;
4. compare count-based, time-based, consecutive-failure and weighted evidence;
5. select minimum samples, thresholds, open intervals and bounded probe rules;
6. prevent stale completion, abandoned lease and recovery-flood races;
7. compose breakers with deadlines, retries, bulkheads, rate limits and truthful fallback;
8. design telemetry and fault experiments that distinguish short circuits from dependency calls;
9. reject breaker use where queue/durable workflow, exception handling or infrastructure routing owns recovery.

## Core Exposition

### Define the protected contract and key

Begin with a dependency policy: logical operation, resource endpoint, deadline, retry owner, concurrency limit, effect semantics, expected failure classes, fallback and recovery. The breaker key is the smallest scope whose outcomes predict one another. Candidate dimensions include dependency service, region, shard, endpoint, operation class, credential/quota pool and tenant.

Too broad a key blocks healthy resources. Too narrow a key produces huge cardinality, tiny samples and little protection. Per-user breakers often permit an attacker to create unbounded state; a bounded tenant tier or resource pool may be safer. Keys need lifecycle, eviction and metrics-cardinality policy. Eviction does not erase durable effect state because breaker state must never own it.

A service mesh may know destination endpoint and transport status but not business semantics. Application code may know operation/effect meaning but not per-connection pool saturation. Choose one authoritative breaker at each protected boundary or deliberately coordinate layers; hidden independent breakers make diagnosis and recovery unpredictable.

### Classify outcomes before counting

Typical categories are:

| Outcome | Breaker evidence? | Reason |
|---|---:|---|
| dependency connection refusal/unavailable | usually failure | predicts inability to serve |
| dependency timeout under a valid attempt budget | policy-dependent failure/slow | may indicate latency impairment; false timeout calibration matters |
| server overload/quota response | resource-keyed failure or explicit open-until | requires correct quota/resource scope and pushback |
| payment decline, not found, version conflict | normally success/ignored | dependency served a valid business result |
| invalid input or unauthenticated caller | ignored | caller/application fault does not predict dependency health |
| caller cancelled before useful dependency evidence | ignored | local interest ended |
| ambiguous mutation timeout | failure evidence plus separate reconciliation | breaker cannot determine effect state |
| short-circuited call | never dependency failure | no protected call occurred |

“Success” for breaker purposes means the dependency responded as expected at the protected protocol boundary, not that the business request achieved its desired outcome. Misclassification can open a breaker during a sale because many cards are declined, or remain closed while every call takes longer than its useful deadline.

Slow-call evidence requires an operation-specific threshold. Count slow success separately from failure; define whether an eventual timeout appears in both categories or exactly one. Keep denominator semantics explicit.

### Sliding evidence

A count window retains the last N classified outcomes. A time window retains outcomes in recent buckets/interval. Count windows respond after a fixed population but stretch across quiet periods. Time windows represent recency but have variable sample size. Both need a minimum sample threshold.

For N≥Nmin, a basic failure rule is F/N≥θf. A slow rule is S/N≥θs. Threshold equality must be specified. Percentage rules with N=2 are unstable; Nmin avoids the most obvious error but does not prove statistical confidence or optimal control. Weighted/adaptive methods can reflect severity, yet add explainability, feedback and validation burden. Configuration must be versioned and changed cautiously.

Consecutive-failure counters are simple and responsive but one intermittent success resets all evidence and order dominates results. Lifetime counters remember obsolete incidents. Exponentially weighted estimates trade bounded memory for less transparent effective samples. Use the simplest model justified by the failure/recovery process and prove boundary behavior.

Closed-state concurrency means outcomes complete out of issue order. The window should define whether order is completion time, start time or bucket time. Completion-time recording reflects observed recent results but slow old calls can arrive after a new epoch; carry epoch/generation and ignore state transitions from obsolete ownership while still recording appropriate telemetry.

### Closed to open

State evaluation and transition must be atomic. Multiple concurrent failures may cross a threshold together; exactly one transition creates a new open epoch and timestamp/reason. Calls already admitted before opening may finish. Their outcomes cannot retroactively become short circuits, and stale successes must not close the newly open breaker.

Opening suppresses future protected admissions, not work already issued. Propagate cancellation only where operation semantics permit; reconcile ambiguous mutation effects. The open result should carry a stable local error classification and perhaps retry/pushback advice bounded by caller deadline. Retry logic must treat open as “do not immediately retry through the same breaker.”

An accelerated open can use explicit trustworthy overload/pushback or a catastrophic connection signal, but document why one observation is sufficient and scope it narrowly. Manual force-open is useful for incidents/maintenance; it requires authorization, audit, expiry and clear interaction with automatic transitions.

### Open interval

Open duration is a recovery hypothesis, not a cure. Too short causes oscillation and probe load; too long rejects healthy calls after recovery. A fixed interval is predictable. Increasing/jittered intervals may protect persistent failures and desynchronize instances. Server pushback can inform the earliest probe time if authenticated/trusted and capped.

Use monotonic local time for interval enforcement. Fleet-local breakers open and probe independently, potentially creating many simultaneous probes; jitter and shared dependency capacity matter. A globally coordinated breaker offers consistent suppression but adds availability, latency and partition semantics. Most breakers are local; design recovery load at fleet scale instead of assuming one probe globally.

Open calls need no queue unless a separate durable-work contract owns deferral. Holding interactive calls until half-open defeats fail-fast behavior and creates a recovery herd.

### Half-open probe ownership

At or after the eligible time, an atomic transition or lease grants no more than H probe calls. Other calls remain short-circuited. H is derived from recovery capacity and evidence needs, not current waiting population. Probe workloads should exercise the failed path but be safe and representative. A shallow health endpoint can succeed while authentication, data shard or write path remains broken; an unsafe mutation is a poor probe without durable idempotency.

Every lease terminates. Success, classified failure, timeout, caller cancellation, process shutdown and abandoned callback all release/resolve it. A probe deadline prevents half-open state from hanging forever. A generation identifies the half-open epoch so late results cannot change later state.

Closing rules vary: one successful probe, K consecutive successes, or a bounded probe batch meeting a rate threshold. State the exact rule. One success is fast but noisy; multiple successes delay recovery and add load. After close, ramp traffic or retain bulkhead/rate-limit control—closing all fleet breakers can still flood a cold dependency.

A failure generally reopens and starts a new interval. If simultaneous probes are allowed, define mixed-result ordering: “any classified failure reopens” is conservative; a completed batch decision needs snapshot/lease rules. Do not let a success close after a peer already reopened.

### State machine and deterministic trace

The finite model below demonstrates one threshold-based breaker with a single half-open lease. It deliberately omits threads, real calls and a rolling window. Events are processed sequentially so its purpose is transition arithmetic, not production synchronization.

<!-- bijux-verify: {"id":"sepat-083-circuit-state","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"states=closed,closed,open,open,half-open,closed\ndecisions=call,call,trip,reject,probe,close\nprotected_calls=4\nshort_circuits=1\n","stderr":""}} -->
```python
def apply_event(state, failures, now_ms, opened_ms, event):
    if state == "open":
        if now_ms < opened_ms + 100:
            return state, failures, opened_ms, "reject", 0, 1
        return "half-open", failures, opened_ms, "probe", 1, 0

    if state == "half-open":
        if event == "success":
            return "closed", 0, opened_ms, "close", 0, 0
        return "open", failures, now_ms, "trip", 0, 0

    if event == "failure":
        failures += 1
        if failures >= 3:
            return "open", failures, now_ms, "trip", 1, 0
    return "closed", failures, opened_ms, "call", 1, 0


state = "closed"
failures = 0
opened = -1000
states = []
decisions = []
protected = 0
shorts = 0

for now, event in [(0, "failure"), (10, "failure"), (20, "failure"),
                   (50, "failure"), (120, "eligible"), (130, "success")]:
    state, failures, opened, decision, called, rejected = apply_event(
        state, failures, now, opened, event
    )
    states.append(state)
    decisions.append(decision)
    protected += called
    shorts += rejected

print("states=" + ",".join(states))
print("decisions=" + ",".join(decisions))
print("protected_calls=" + str(protected))
print("short_circuits=" + str(shorts))
```

The explicit `probe` event is schematic lease ownership in a deterministic trace; a real implementation must atomically derive it from open expiry and forbid concurrent leases. This execution does not verify clocks, sliding samples, thread safety, I/O, cancellation, effect safety, fallback, fleet coordination or recovery capacity.

### Fallback and public truth

Fail-fast is still failure. A fallback may return cached data with age/source, omit an optional feature, route to an independently isolated alternative, durably schedule work, or reject clearly. It must preserve authorization, privacy, consistency and domain meaning. “Default balance = 0,” “payment approved,” or stale clinical state can be more dangerous than unavailability.

Alternative dependencies need their own capacity/deadline/breaker and can fail concurrently. Automatically failing over all traffic may overload the backup. Cache fallback must not bypass revocation or tenant isolation. Telemetry distinguishes authoritative, stale, partial and scheduled outcomes.

### Composition

Place attempt deadlines around every admitted protected call. A breaker does not stop hangs without them. Apply bounded retry through the breaker so open state terminates the retry path; avoid recording each retry and logical request inconsistently. A bulkhead constrains concurrent resources even while the breaker is closed and during initial failure detection. Rate limiting and load shedding control offered work and protect recovery.

Composition order depends on intended metrics and resource ownership. If a retry executes inside one breaker call, the breaker sees the final logical outcome but may hide load/slow attempts. If each attempt passes through the breaker, each dependency call contributes evidence, but layered retry must stop on open. Document the unit and instrument both logical operations and physical attempts.

Circuit state is not durable business state. Usually a process restart begins a conservative fresh state or uses platform health evidence; persisting an old open state can reject after recovery, while clearing it can cause a restart probe storm. Design startup admission and fleet jitter explicitly.

### Observability and verification

Expose bounded-cardinality state by key, transition count/reason, current sample count/failure/slow rates, short-circuit count, protected calls, half-open leases/in-flight/results, open duration, manual override and configuration version. Trace whether a call was admitted, its epoch and outcome classification. Never label metrics by raw user ID or arbitrary URL.

Breaker-open alerts need context: protected dependency signals, caller impact, fallback truth and recovery. High open-call “success” from fallback can hide outage. Dashboard logical success, authoritative/degraded results and dependency calls separately.

Verification includes:

- every outcome class and threshold equality just below/at/above minimum sample;
- count/time-window eviction, quiet periods and completion ordering;
- concurrent threshold crossing creates one epoch;
- already admitted calls and stale completion cannot close a newer epoch;
- open calls never invoke dependency or enter an unbounded queue;
- exact interval boundaries use monotonic time;
- half-open permits no more than H under contention;
- probe success/failure/timeout/cancel/abandon/shutdown resolves leases;
- mixed simultaneous probe outcomes follow one documented rule;
- fallback security, freshness, authority and capacity remain truthful;
- fleet correlated failure/recovery, restart and configuration rollout stay bounded;
- actual library/mesh defaults and metric units match policy.

Fault tests must run on isolated owned fixtures. A unit state machine cannot prove dependency recovery, production thresholds, thread safety, availability or safe fallback.

## Definitions and Notation

Let state Q ∈ {closed, open, half-open}; breaker key b; epoch g; window population N; failure count F; slow count S; minimum sample Nmin; thresholds θf and θs; open time to; interval Δo; half-open maximum leases H; and current leased set Lg with |Lg|≤H.

Outcome classifier C maps a physical protected call to success, failure, slow-success, ignored or ambiguous categories under operation policy. A short-circuit produces no C input because no dependency call occurred. Durable effect state E is external to Q. Probe result can transition Q only if its lease epoch equals current g.

## Mechanisms, Invariants, or Proof Structure

**Suppression.** In open state before eligible probe time, admission returns locally without protected invocation. Therefore dependency calls from this breaker are zero for those decisions, subject to calls admitted before opening and other clients/breakers.

**Probe bound.** If lease acquisition atomically tests |Lg|<H and adds one unique lease, then concurrent half-open protected calls are at most H. Correctness requires terminal release/epoch invalidation under every completion path.

**Stale-result safety.** If transitions accept probe results only when result epoch equals current g and lease remains owned, an old result cannot close/reopen a later epoch. It may still need effect reconciliation.

**Sampling limit.** F/N is an observed proportion for the selected window, not a causal or future probability guarantee. Nmin reduces decisions from tiny denominators but does not establish confidence, independence or optimal threshold.

**Failure isolation condition.** If all resources sharing b have correlated health, suppression is targeted. If healthy and unhealthy independent resources share b, opening causes avoidable denial to the healthy subset. Correct scope is therefore a premise, not a state-machine consequence.

**No effect guarantee.** Opening controls future admission. It cannot retract an already issued operation or infer its commit status; ambiguous mutations require independent durable identity/reconciliation.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation |
|---|---|---|
| bounded retry only | failures are brief, sparse and spare capacity exists | persistent faults still consume attempts; needs deadline/load bounds |
| timeout only | main risk is hung/slow call | repeated timed failures can exhaust capacity |
| bulkhead | need resource isolation regardless of outcome history | does not suppress likely failures or test recovery |
| rate limiter/load shedder | offered load exceeds policy/capacity | does not infer dependency health |
| infrastructure routing/health | endpoint failure is owned by platform load balancing | health may be shallow; application semantics absent |
| durable queue/workflow | work can be deferred and must survive request/process | changes outcome contract; needs idempotency/backlog policy |
| manual force-open | maintenance or known incident requires deterministic suppression | operational delay/error and authority risk |
| adaptive breaker | nonstationary workloads justify measured control | feedback opacity, training drift and validation burden |
| no breaker | local deterministic errors or low-cost failure with sufficient isolation | rely on explicit timeout/capacity/error handling instead |

## Failure Modes and Misconceptions

- **A breaker detects outages.** It reacts to local classified observations; sampling and network perspective matter.
- **Open means dependency is down.** It means local policy currently suppresses calls.
- **Every exception counts.** Caller/business/security failures often say nothing about dependency health.
- **Every success resets evidence.** That consecutive-counter behavior can hide high failure rates.
- **One breaker per service is enough.** Regions, shards, operations and quota pools may fail independently.
- **One breaker per user is precise.** It can explode state/cardinality and enable abuse.
- **Half-open means normal traffic resumes.** It means bounded owned probes only.
- **A health ping proves recovery.** It may bypass the failed data/authorization/write path.
- **A probe cancellation is neutral.** It must resolve the lease and exact policy outcome.
- **Closing creates capacity.** Recovery traffic still needs bulkhead, rate and admission control.
- **Fallback equals success.** Stale/partial/default results must remain explicit.
- **Breaker replaces timeout.** Admitted calls can still hang.
- **Breaker resolves ambiguous writes.** It cannot determine effects already dispatched.
- **Shared breaker state is always better.** Coordination can add a critical dependency and partition problem.
- **Passing state tests proves production thresholds.** Workload, dependency and fleet evidence remain necessary.

## Worked Examples

### Example 1

A catalogue search breaker counts connection failures, valid timeouts and server overload as failures; empty results and not-found are successful protocol outcomes; invalid query and caller cancellation are ignored. Slow successful searches enter a separate slow-call population. This avoids opening when customer searches legitimately return nothing.

### Example 2

A 20-call count window has Nmin=10 and θf=50%. At N=9 with nine failures it stays closed because the sample floor is unmet. At N=10 with five failures it opens if equality is inclusive. The policy test fixes `>=`; configuration documentation states that exact boundary.

### Example 3

A database has 64 shards. One global breaker opens after shard 17 fails, rejecting 63 healthy shards. The corrected key is cluster/region/shard plus operation class where read and write recovery differs. Key lifecycle and bounded metrics prevent arbitrary IDs from allocating unlimited breaker state.

### Example 4

Twenty application instances open together for 10 seconds. Without jitter, each grants five probes simultaneously and sends 100 recovery calls. The fleet applies jittered eligibility, H=1 per instance, dependency bulkhead and gradual post-close admission; load testing verifies the recovering database can absorb the bound.

### Example 5

A half-open probe is cancelled after dispatch. If the lease is merely decremented with no outcome, the breaker can oscillate or admit another unsafe probe while the first effect remains ambiguous. The policy reopens/holds according to configured cancellation semantics, releases the lease exactly once, fences late result by epoch and reconciles effect identity.

### Example 6

Two probes are allowed. Probe A fails and atomically reopens epoch 8. Probe B succeeds later with epoch 7. The success is recorded as stale telemetry but cannot close epoch 8. Without generation comparison, completion order would make health state nondeterministic.

### Example 7

An application breaker and service mesh both open on different windows. The app returns fallback while mesh rejects its recovery probes, so it never observes recovery. The team assigns transport endpoint ejection to the mesh and operation-semantic breaker to application with explicit interaction, or removes one layer; telemetry reveals both decisions.

### Example 8

A profile service falls back to a cache. The response includes snapshot age/version and omits revocable authorization decisions that cannot safely be stale. Cache access has its own bulkhead and deadline. Metrics separate authoritative, stale-degraded and unavailable outcomes instead of claiming 100% success.

### Example 9

During shutdown, the breaker stops new admissions, resolves/rejects half-open leases, preserves ownership of in-flight calls, reaps late results and emits final transitions. It does not persist volatile open state as business truth. Startup uses bounded/jittered admission so simultaneous restarts do not hammer the dependency.

### Example 10

An emergency-control breaker protects a remote sensor path. It never substitutes a fabricated normal reading. Open state triggers a hazard-defined degraded/fail-safe mode, while probe traffic is authenticated, side-effect safe and priority bounded. Clock, network, sensor and fallback failures require hardware-in-loop tests and named safety, controls, security and operations review.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): dependency boundaries, failure domains, fallback and policy ownership.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): state-model, race, threshold and fault-injection testing.
- [Network Engineering](../../24-network-engineering/ROADMAP.md): endpoint health, connection errors, regional routing and ambiguous transport outcomes.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): key/cardinality abuse, manual override authority and safe stale-data fallback.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): partial failure, generations, distributed observation and recovery coordination.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): SDK/mesh breakers, fleet configuration, telemetry and incident operation.

## References

1. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018.
2. Fowler, Martin. “Circuit Breaker.” 2014. <https://martinfowler.com/bliki/CircuitBreaker.html>
3. Microsoft. “Circuit Breaker Pattern.” Azure Architecture Center. <https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker>
4. AWS. “Circuit Breaker Pattern.” AWS Prescriptive Guidance. <https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html>
5. Resilience4j Authors. “CircuitBreaker.” Reference Documentation. <https://resilience4j.readme.io/docs/circuitbreaker>
6. OpenTelemetry Authors. “Semantic Conventions for HTTP and RPC.” <https://opentelemetry.io/docs/specs/semconv/>
7. Beyer, Betsy, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds. *Site Reliability Engineering*. O'Reilly, 2016.
8. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017.
9. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013.
10. Jain, Raj. *The Art of Computer Systems Performance Analysis*. Wiley, 1991.
11. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020.
12. gRPC Authors. “Health Checking.” gRPC Documentation. <https://grpc.io/docs/guides/health-checking/>

Library state models, window algorithms, threshold semantics, automatic transitions and metrics vary by version. Current official sources were checked on 2026-08-29; inspect exact runtime, mesh and dependency behavior.

## Exercises

### Exercise 1

Specify breaker keys and outcome classifiers for a multi-region payment authorization dependency with business declines, input/authentication failures, overload, timeouts, ambiguous mutations and independent regional quotas.

### Exercise 2

A count window contains 24 outcomes: 9 classified failures, 5 slow successes and 10 normal successes. Compute failure and slow rates. With Nmin=20, θf=40% and θs=20%, state which inclusive rule opens. Then evict four oldest normal successes and add four failures; recompute.

### Exercise 3

Design a concurrency-safe half-open protocol with H=2, two required successes, any-failure-reopens, probe deadline and epoch fencing. Analyze simultaneous success/failure and cancellation.

### Exercise 4

Diagnose a system with one global breaker, every exception counted, no minimum samples, all traffic admitted after timer expiry, stale successes resetting state, application/mesh breakers, fallback reported as current success and no bulkhead. Redesign and define decisive tests.

### Exercise 5

Design circuit behavior for a safety-critical telemetry/control dependency. Include false-open/false-close consequences, probe/fallback safety, time/effect semantics, security, capacity, evidence and named review.

## Answers to the Exercises

### Answer 1

Key at least by payment provider/region and authorization operation, plus quota/credential pool if those fail independently. Do not globally couple healthy regions. Bound key creation; tenant-specific keys require justified isolation and lifecycle.

Valid declines are protocol successes because the provider served the decision. Invalid input, expired caller authority and authentication rejection caused locally are ignored; provider authentication failure due to shared credentials may be a distinct operational breaker signal. Connection unavailable, explicit regional overload and calibrated dependency timeouts are failures. Slow successes can populate a separate latency rule. Short circuits never enter the dependency denominator.

An ambiguous authorization timeout is failure evidence for availability but retains durable payment/effect identity and reconciliation; the breaker cannot declare non-authorization. Retry honors one owner/deadline/idempotency and stops on open. Regional failover has its own capacity/breaker and does not silently duplicate authorization.

### Answer 2

Initially N=24. Failure rate is 9/24=37.5%, below 40%. Slow rate is 5/24≈20.83%, meeting the inclusive 20% slow threshold. Because N≥20, the slow-call rule opens while the failure rule does not.

After four normal successes leave and four failures arrive, N remains 24. Failures become 13 and normal successes 6; slow successes remain 5. Failure rate is 13/24≈54.17%, and slow rate remains 5/24≈20.83%. Both inclusive rules open.

This arithmetic assumes categories are disjoint, the evicted four are known normal successes and completion ordering defines the window. It does not prove independence, optimal thresholds or future health.

### Answer 3

Open expiry atomically begins epoch g+1 in half-open with empty lease/result sets. Admission atomically grants at most two unique leases tagged with epoch and deadline; all other callers short-circuit. Each terminal path resolves its lease once. A classified failure atomically reopens a new epoch immediately. A success increments success count only if epoch/current lease match; the second valid success closes and starts a fresh closed window.

If success and failure race, linearization decides: if failure reopens first, later old-epoch success is stale; if success arrives first but has not yet reached two, failure reopens. If second success closes just before a failure from the same batch, “any failure” would be violated unless closing waits for the entire granted batch or cancels/invalidate unresolved leases under an explicit rule. Therefore grant a batch of at most two and decide after both terminal, or use sequential H=1 probes for two successes. For H=2 batch semantics, any failure reopens; two successes close.

Probe timeout/cancellation/abandonment resolves lease and reopens (or counts failure) under policy; it never leaves half-open capacity consumed forever. Late completions are fenced. Effect ambiguity is reconciled separately.

### Answer 4

The global key creates cross-resource denial. Counting caller/business exceptions poisons health evidence. Tiny samples flap. Timer-expiry flood overwhelms recovery. Stale completion races state. Layered breakers conflict. Unlabelled fallback lies. Without bulkhead, initial/closed calls can exhaust resources before opening.

Define dependency/resource/operation keys; bounded key lifecycle; explicit outcome categories; count/time window with Nmin and inclusive thresholds; monotonic open interval; H-sized epoch-tagged probe leases with deadline/terminal cleanup; exact close/reopen batch rule; and gradual post-close admission. Assign application versus mesh ownership or specify complementary scopes. Keep per-call deadlines, bounded retry, dependency bulkhead/rate control and ambiguous-effect reconciliation. Label fallback freshness/authority.

Tests cover classifier table, threshold/minimum/equality/window eviction, concurrent one-transition opening, pre-open in-flight calls, stale epochs, zero dependency calls while open, exact interval, H under contention, mixed probe results, cancel/timeout/abandon/shutdown, fleet recovery/restart, key eviction/cardinality attack, fallback auth/freshness/capacity, layered configuration and telemetry conservation.

### Answer 5

Partition by genuinely independent sensor/control path and safety function; never let noncritical telemetry poison emergency actuation unless the dependency is truly shared. Define which missing/slow/invalid/authentication outcomes indicate path impairment. False open may remove needed information/control; false close may consume critical capacity or use untrustworthy data. Threshold/open duration/probe count require hazard and worst-case timing analysis, not generic defaults.

Open state enters an explicit degraded/fail-safe mode and never fabricates normal telemetry or successful actuation. Probes are authenticated, bounded, side-effect free where possible and representative of the failed path. If an actuation probe is unavoidable, durable command identity, fencing, device state and reconciliation protect irreversible effects. Deadline/cancellation does not prove rollback. Critical capacity is isolated, rate bounded and abuse protected.

Threats include forced breaker opening, probe spoofing, key/cardinality exhaustion, stale fallback, manual-override abuse, replay and telemetry tampering. Apply mutual authentication, integrity, least privilege, bounded keys, signed/audited expiring override and protected observability.

Evidence includes formal state/timed/effect model, model checking of concurrent transitions where feasible, hardware-in-loop path/probe/fallback tests, threshold sensitivity, worst-case timing/capacity, clock/network/sensor/controller/power faults, security/adversarial tests, fail-safe/recovery drills and audit reconciliation. Approval requires named domain safety, controls, hardware, communications, distributed/concurrency, security, reliability/operations, human-factors and regulatory reviewers with traceable hazards and acceptance criteria.
