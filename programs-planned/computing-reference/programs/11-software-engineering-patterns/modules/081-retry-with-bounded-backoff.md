---
module_id: SEPAT-081
program: Software Engineering: Patterns
level: 2
module_number: 81
title: Retry with Bounded Backoff
status: complete
last_verified: 2026-08-29
---

# Retry with Bounded Backoff

## One-Page Review

### Governing question

When can another attempt improve the probability of a correct outcome without duplicating an effect, exhausting the caller's deadline, or amplifying an impaired dependency into an outage?

### Essential definitions

- An **attempt** is one execution of an operation under an attempt-specific timeout and shared logical request identity.
- A **retry** is an additional attempt after a prior attempt did not yield an acceptable terminal outcome.
- A **retry owner** is the single layer authorized to decide whether and when to issue another attempt.
- A **retry disposition** classifies an outcome as success, terminal failure, retryable, or ambiguous under operation semantics—not merely an error code.
- An **effect identity** durably binds repeated presentations of one logical command to the same intent and replay result.
- A **retry budget** bounds attempts, elapsed time, added load, concurrency, and sometimes tokens per client/dependency/tenant.
- **Capped exponential backoff** gives retry index i a maximum delay window Wᵢ = min(Wmax, W₀rⁱ).
- **Jitter** randomizes a delay within a specified window so independently failing clients do not remain synchronized.
- A **retry storm** is positive feedback in which failures create extra attempts, increasing load and causing more failures.
- A **recovery storm** occurs when delayed work synchronizes as a dependency becomes healthy.

### Central model, mechanism, or theorem

Retry eligibility is conjunctive:

$$
retryable = transient \land replaySafe \land budgetRemaining \land capacityAvailable
\land \neg cancelled \land policyAllows.
$$

For initial attempt plus R retries, maximum attempt count is A = 1 + R. With independent retry owners at layers j, worst-case leaf attempts multiply:

$$
A_{leaf}=\prod_j A_j.
$$

Backoff changes *when* attempts occur, not whether their effects are safe and not how many owners may multiply them. Full jitter samples Dᵢ uniformly from [0, Wᵢ], giving E[Dᵢ] = Wᵢ/2 under the ideal model. A retry starts only if its delay plus a meaningful attempt timeout fits the same inherited absolute deadline.

### Critical invariants

- Retry only when the outcome is plausibly transient and replay is demonstrably safe.
- Preserve one logical request/effect identity across attempts; use a new attempt and trace-span identity for each try.
- Assign exactly one automatic retry owner per dependency call path; disable or account for transport, SDK, proxy, queue and application retries.
- Bound attempts, total elapsed time, per-attempt time, delay, concurrent retry work, queued retry work and aggregate retry load.
- Derive every attempt from the original absolute deadline; never reset the caller's budget at an inner layer.
- Do not start an attempt that lacks time to finish or be reconciled meaningfully.
- Treat timeout, connection loss and cancellation after dispatch as potentially ambiguous effects.
- Honor trustworthy server pushback only within operation policy and remaining budget; malformed or excessive advice cannot bypass caps.
- Jitter clients and recovery admission; a cap without jitter can synchronize a herd at the cap.
- Record attempt number, owner, disposition, delay source, remaining budget, effect identity and terminal outcome without leaking secrets.

### Common failures

Common failures include retrying every exception, retrying POST because no response arrived, resetting deadlines per attempt, counting retries instead of total attempts, identical exponential schedules without jitter, stacking SDK/service-mesh/application retry loops, retrying from a saturated thread pool, unbounded delayed-task queues, obeying arbitrary `Retry-After` beyond the deadline, reusing an idempotency key for changed payload, assuming cancellation rolls back a committed write, retrying permanent authorization/input failures, concealing retry latency in success metrics, opening all recovery traffic at once, and calling an operation exactly-once because duplicate effects were not observed.

### Compact example

A payment command has a 1.2 s absolute budget and a durable idempotency key bound to merchant, amount, currency and authenticated principal. The application is the sole retry owner. Attempt one times out ambiguously after 250 ms; the client queries/replays using the same key. A full-jitter delay is selected inside a 100 ms window, but a second attempt starts only if delay plus its 300 ms timeout and reconciliation reserve fit. The ledger returns the recorded result if the first attempt committed. Without durable binding, the correct action after the ambiguous timeout is reconciliation or failure—not blind retry.

### Connections

[SEPAT-080](080-selecting-a-concurrency-pattern-from-blocking-and-ownership-constraints.md) supplies ownership and capacity analysis. Retry composes directly with the forthcoming SEPAT-082 Timeout and Deadline, SEPAT-083 Circuit Breaker, SEPAT-084 Bulkhead, SEPAT-085 Rate Limiter, SEPAT-086 Load-Shedding, SEPAT-088 Transactional Outbox, and SEPAT-089 Idempotent Consumer modules.

## Governing Question

How should a system recover from genuinely transient failure while proving that attempts are semantically safe, temporally bounded, load-bounded, desynchronized, observable and subordinate to one end-to-end outcome?

Retry is controlled repetition, not generic error handling. It trades more work and latency for another chance at success. The trade can be favorable when failures are brief, replay is safe, spare capacity exists and the caller still values the result. It is destructive when an effect is ambiguous, the dependency is overloaded, failure is permanent, multiple layers repeat work, or no useful time remains.

## Why This Matters

Distributed calls cannot generally distinguish “the callee did nothing” from “the callee committed and the response was lost.” Meanwhile, failures correlate: deployment, overload, network partition, quota exhaustion and dependency collapse affect many clients together. Immediate retries can turn a small impaired fraction into a synchronized surge. Exponential delay reduces frequency; jitter reduces phase alignment; budgets stop unbounded persistence; idempotency/reconciliation protects effects. All four are required, and none substitutes for admission control or capacity isolation.

At graduate depth, retry design must connect semantics, probability, queueing, control feedback, time budgets and durable state. An implementation that merely loops with `sleep` has not established correctness.

## Prerequisites and Retrieval

Learners should retrieve:

- failure classification, partial failure and ambiguous outcome;
- safe versus idempotent operation semantics;
- absolute deadlines, monotonic elapsed time and cancellation;
- queue capacity, utilization, overload and Little's Law;
- random variables, uniform expectation and independence assumptions;
- durable identity, conditional update, transaction and reconciliation;
- observability dimensions and fault-injection discipline;
- [bounded concurrency selection](080-selecting-a-concurrency-pattern-from-blocking-and-ownership-constraints.md).

Before proceeding, explain why a transport timeout is evidence about observation time rather than evidence that a remote effect did not occur.

## Learning Objectives

After this module, learners can:

1. classify retry eligibility from operation and outcome semantics rather than error-code folklore;
2. design capped, jittered schedules subordinate to absolute deadline and per-attempt reserves;
3. compute attempt multiplication and reason about retry-driven overload feedback;
4. distinguish idempotent effect, deduplication, replay, reconciliation and exactly-once claims;
5. assign one retry owner across application, library, transport, proxy and queue layers;
6. apply retry budgets, concurrency limits, server pushback and recovery admission;
7. implement a deterministic policy core with injectable clock/randomness for verification;
8. design tests and telemetry for transient, permanent, ambiguous, overload, cancellation and restart cases;
9. reject retry where durable workflow, operator action, compensation or immediate failure is safer.

## Core Exposition

Retry policy is a protocol over one logical operation. Its inputs include operation/effect semantics, outcome evidence, original absolute deadline, attempt count, dependency/tenant retry budget, admission capacity, cancellation state and trusted server advice. Its output is terminal success/failure, reconciliation, or a scheduled next attempt with an explicit delay and timeout.

The first question is not “how long should backoff be?” It is “what does repeating this operation mean?”

**Read-only is not automatically harmless.** An apparently read-only endpoint may consume scarce resources, generate audit records, advance a cursor or trigger cache fill. It can still be safe to repeat, but the load and side effects must be understood.

**Idempotent is not the same as side-effect free.** Applying the same intended operation repeatedly has the same intended effect as applying it once. HTTP `PUT` may be idempotent in protocol semantics, yet repeated requests still create network, log and authorization work. A payment creation command can be made replay-safe by a durable effect identity, but only if the server atomically binds identity to request fingerprint and terminal/in-progress outcome.

**Deduplication has a scope and lifetime.** A process-local cache does not protect after restart or across replicas. An expiring record does not protect attempts arriving after expiry. A key without payload/principal binding can return another operation's result or enable abuse. Durable idempotency commonly requires one transaction that reserves/binds the identity and applies or records the effect, plus a defined response for concurrent duplicate presentations.

### Outcome taxonomy

Classify at least these cases:

| Evidence after an attempt | Effect knowledge | Typical decision |
|---|---|---|
| local validation rejected before dispatch | definitely not issued | terminal unless caller changes input |
| connection failed before any request bytes/semantic dispatch, as proven by the transport | definitely not observed by application under exact contract | retry may be eligible |
| explicit overload/transient response before effect | no effect under endpoint contract | retry after pushback if budget/capacity allow |
| explicit version/auth/input/business rejection | terminal for unchanged request | do not retry blindly |
| timeout, reset or response loss after dispatch | ambiguous | replay only with durable safety; otherwise reconcile |
| success response | effect/result terminal under contract | stop; do not retry success because response was slow |

Status codes are inputs, not the complete policy. `503` can follow a committed mutation. `409` can be a permanent semantic conflict or a transient read-modify-write race requiring the whole transaction to restart. A client library cannot infer application effect semantics solely from transport status.

### One retry owner and multiplicative amplification

Suppose three layers each allow one initial attempt plus two retries. One top-level request can cause

$$
3\times3\times3=27
$$

leaf attempts. Five such layers yield 243. “Only two retries” is therefore meaningless without total-attempt terminology and ownership mapping. Inventory application loops, generated clients, SDK defaults, load balancers, service meshes, gateways, message redelivery and job schedulers. Assign one layer to retry each dependency operation; other layers either disable repetition or expose it in the same shared budget.

The best owner is usually the layer with enough semantic information to judge replay safety and enough end-to-end budget information to avoid useless work. Low-level transparent retries can be valid when the transport proves application code never observed the request, but they must be understood, surfaced and included in load/evidence analysis.

### Bounded schedule

For base window W₀ > 0, multiplier r > 1, cap Wmax and zero-based retry index i:

$$
W_i=\min(W_{max},W_0r^i).
$$

Common jitter families include:

- **full jitter:** Dᵢ sampled uniformly from [0, Wᵢ]; strong phase spreading, expected delay Wᵢ/2 under an ideal uniform source;
- **equal jitter:** Wᵢ/2 plus a sample from [0, Wᵢ/2]; prevents very short waits but has a larger mean;
- **decorrelated jitter:** next delay depends on the previous delay and a capped random range; useful in some persistent-client workloads but requires an exact specification and tests;
- **server pushback:** a trusted server-provided delay participates as a policy floor or explicit stop signal, subject to validation, local cap and remaining deadline.

Do not describe “exponential backoff with jitter” without naming the algorithm, initial window, multiplier, cap, maximum attempts, total deadline, random source/test injection and pushback rule. Different algorithms have different distributions and recovery behavior.

A cap bounds a single delay, not total duration. After reaching the cap, synchronized clients without jitter retry periodically at the same cadence. Jitter must continue at the cap. Long-lived background work additionally needs durable scheduling, fair admission and backlog/age bounds rather than sleeping worker threads.

### Deadline and attempt admission

Let absolute deadline be T, monotonic current time t, chosen delay d, minimum useful attempt time a, and reconciliation/cleanup reserve g. Start another attempt only if

$$
t+d+a+g\le T.
$$

The attempt receives a timeout no greater than the remaining budget after delay and reserve. It does not receive a fresh end-to-end timeout. Wall time is used for protocol timestamps when required; monotonic elapsed time prevents local wall-clock changes from extending budgets. Across machines, propagate an absolute protocol deadline or remaining duration according to the protocol's skew rules, then derive local monotonic budget.

Cancellation stops unnecessary future attempts and should interrupt cancellable waiting/work. It cannot prove a remote effect was undone. A late success after local cancellation still requires reaping, recording or reconciliation according to effect semantics.

### Load and stability

Let original logical request rate be λ and mean attempts per request be E[A]. The attempt arrival rate is approximately

$$
\lambda_{attempt}=\lambda E[A]
$$

at a defined boundary. If a dependency is already at capacity, retry raises utilization and waiting, which causes more timeouts and more retry: a positive-feedback loop. Backoff spreads work but does not reduce the total count by itself. Limit retry concurrency and tokens, shed new/retry work by policy, and stop retries when recent failure evidence says success is unlikely.

A retry budget can be a token bucket replenished by successful originals, a ratio cap such as retries/originals, or a finite concurrent/queued retry partition. Scope matters: per process does not constrain a fleet; global may unfairly couple tenants; per dependency/operation/tenant often provides a useful hierarchy. Preserve emergency/reserved capacity only under explicit priority and anti-starvation policy.

Recovery is another overload boundary. Thousands of clients whose capped timers expire together can overwhelm a newly healthy instance. Continue jitter, ramp admission, use connection/retry tokens, respect server pushback, warm caches gradually, and verify recovery from fleet-scale correlated failure.

### Retry-After and pushback

HTTP `Retry-After` can express either delay seconds or a date for applicable responses. Parse defensively, account for wall-clock uncertainty when using dates, cap the value by policy, and retry only if the operation was otherwise eligible. A delay that consumes the remaining useful budget means return/defer, not violate the caller's deadline. An untrusted upstream must not force unbounded resource retention. gRPC retry configuration similarly defines per-method attempts, exponential backoff and retryable status codes, with retry throttling/server pushback in supported implementations; exact runtime/version behavior must be verified.

### Inline versus durable retry

Inline retry is appropriate when another attempt can finish within the interactive deadline and the caller still awaits the same outcome. Durable retry belongs in a workflow/queue when work may outlive the request, needs long delays, must survive process restart, or requires operator reconciliation. The system must state whether acceptance means “effect completed,” “durably scheduled,” or merely “held in process memory.”

Durable retry adds its own semantics: lease/fencing, attempt visibility, next-at timestamp, maximum age, poison policy, deduplication, tenant fairness, shutdown/restart and effect reconciliation. It does not make an unsafe operation safe.

### Policy core and executable specification

A policy core should be pure where possible. Inject time, random samples and outcome classifications. Keep effect execution outside the policy so tests can exhaust boundaries deterministically. The following finite model computes capped windows, deterministic samples and amplification; it deliberately performs no I/O or sleeping.

<!-- bijux-verify: {"id":"sepat-081-bounded-backoff","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"windows_ms=100,200,400,800,1000\ndelays_ms=0,100,400,200,750\nscheduled_ms=1450\namplification_3_layers_2_retries=27\ndeadline_allows_attempt_4=false\n","stderr":""}} -->
```python
def capped_windows(base_ms, cap_ms, retry_count):
    return [min(cap_ms, base_ms * (2 ** index)) for index in range(retry_count)]


def sampled_delays(windows_ms, fractions):
    return [int(window * fraction) for window, fraction in zip(windows_ms, fractions)]


def leaf_attempts(layer_count, retries_per_layer):
    return (1 + retries_per_layer) ** layer_count


def attempt_fits(remaining_ms, delay_ms, attempt_ms, reserve_ms):
    return delay_ms + attempt_ms + reserve_ms <= remaining_ms


windows = capped_windows(100, 1000, 5)
delays = sampled_delays(windows, [0.0, 0.5, 1.0, 0.25, 0.75])
fits = attempt_fits(900, windows[3], 150, 50)

print("windows_ms=" + ",".join(str(value) for value in windows))
print("delays_ms=" + ",".join(str(value) for value in delays))
print("scheduled_ms=" + str(sum(delays)))
print("amplification_3_layers_2_retries=" + str(leaf_attempts(3, 2)))
print("deadline_allows_attempt_4=" + str(fits).lower())
```

This execution proves only arithmetic for fixed samples. It does not implement cryptographic randomness, a scheduler, deadlines, cancellation, networking, idempotency, fleet coordination, queue durability or overload control.

### Observability and verification

Record one logical operation with child attempts. Useful dimensions include operation/dependency, retry owner/policy version, attempt ordinal and total allowed, outcome disposition, status/error class, delay algorithm/window/selected delay, pushback, remaining deadline, attempt timeout, token decision, effect identity (protected/hash where sensitive), cancellation and terminal result. Control cardinality; never use secrets or raw user identifiers as metric labels.

Metrics should separate logical requests from attempts and report attempts per logical request, retry success, success-after-retry, terminal failure, ambiguous outcomes, prevented retries by reason, retry tokens, concurrent/queued retries, delay distribution, attempt latency, end-to-end latency and dependency load. “Retry success rate” alone can reward policies that create avoidable failures or conceal latency.

Tests need deterministic policy vectors plus integration evidence:

- permanent errors never retry;
- every allowed transient class does and every disallowed class does not;
- ambiguous mutation is reconciled or safely replayed with durable binding;
- changed payload/principal under one key is rejected;
- attempt and total time bounds hold at exact boundaries;
- cancellation during delay, dispatch and effect is handled;
- multiple retry layers cannot multiply silently;
- token/concurrency/queue limits hold under correlated failure;
- jitter distribution/independence is statistically checked separately from deterministic policy tests;
- restart preserves durable schedule and identity;
- recovery ramp survives fleet-scale synchronized impairment;
- telemetry accounts for every logical operation and attempt.

Fault injection must run only against isolated owned fixtures. A client-side unit test cannot prove server idempotency, durable effect reconciliation, real transport ambiguity or production capacity.

## Definitions and Notation

Let logical operation identity be q, effect identity be e, attempt ordinal k ∈ {1,…,Amax}, original absolute deadline T, local monotonic time t, remaining budget B(t), attempt timeout aₖ, retry delay Dᵢ after attempt i, capped window Wᵢ, cleanup/reconciliation reserve g, original request rate λ, and total attempt rate λattempt.

Let disposition function C(operation, outcome evidence) return success, terminal, retryable or ambiguous. Let S(q,e) mean replay is safe under the durable application contract—not merely the HTTP method name. Let P be policy permission, K be capacity/token admission, and X be cancellation. Eligibility is C=retryable ∧ S ∧ B sufficient ∧ K ∧ ¬X ∧ P. Ambiguous does not collapse into retryable without a replay/reconciliation proof.

## Mechanisms, Invariants, or Proof Structure

**Termination.** If Amax is finite and every attempt/delay is subordinate to finite T, the inline policy terminates by success, terminal/ambiguous decision, cancellation, budget exhaustion or attempt exhaustion. This requires timeouts/waits themselves to respect cancellation/deadline.

**Deadline preservation.** If each attempt is admitted only when t + Dᵢ + aᵢ + g ≤ T and its timeout is at most aᵢ, policy-driven work completes or enters reserved reconciliation by T under the local timing assumptions. Scheduler delay, uninterruptible calls and remote effects require separate evidence.

**Replay safety.** If every attempt carries the same e, the authority atomically binds e to the same authenticated request fingerprint and returns/reconciles one recorded effect, repeated presentations cannot intentionally create a second effect within that authority's scope. This does not prove behavior outside the authority, after retention expiry, or for downstream effects not in the atomic protocol.

**Load bound.** Amax bounds attempts per logical operation but not fleet concurrency. A token/concurrency mechanism with finite capacity Kr bounds admitted retry work at its scope. Layered owners invalidate the single-bound model unless their attempts are included explicitly.

**Desynchronization.** Independent random samples spread clients over windows in expectation; they do not guarantee a maximum instantaneous arrival count. Shared seeds, correlated clocks, coarse timers, cap synchronization and server pushback can re-correlate clients. Statistical/fleet tests are required.

**No universal liveness.** Retry cannot guarantee success. A permanent outage, partition, revoked authority, exhausted deadline or unsafe ambiguity must terminate/defer. Availability claims require a failure model and measured recovery/capacity evidence.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Trade-off or rejection condition |
|---|---|---|
| immediate failure | operation unsafe, failure permanent, latency budget tight | lower availability for brief transient faults |
| fixed delay with jitter | known periodic/resource recovery and narrow attempt range | does not adapt delay scale; still needs caps/budgets |
| capped exponential full jitter | many independent clients face transient/correlated failure | randomized latency; exact parameters need workload evidence |
| server pushback | server has better recovery/load knowledge and signal is trusted | stale/malformed/untrusted advice; must fit local policy/deadline |
| reconciliation query | outcome ambiguous and effect status is queryable | extra protocol/state and may itself be unavailable |
| durable scheduled workflow | delay exceeds request lifetime or restart survival required | queue/lease/dedup/backlog complexity and eventual outcome contract |
| circuit breaker | repeated attempts are unlikely during a persistent dependency fault | breaker does not prove replay safety or replace attempt deadlines |
| hedging | long-tail latency with spare capacity and safely duplicate work | concurrent amplification is stronger; requires cancellation/effect proof |
| fallback/degradation | lower-fidelity answer is semantically valid | stale/partial answer must be explicit and safe |
| operator/compensation | irreversible ambiguity or regulated effect needs judgment | slower and operationally costly but preserves control |

## Failure Modes and Misconceptions

- **“Three retries” means three attempts.** Many APIs use `maxAttempts`; others use retry count. State both explicitly.
- **Every timeout is transient.** Timeout describes observation, not root cause or effect status.
- **Exponential backoff prevents overload.** It delays load; attempt/token/admission bounds prevent excess load.
- **The cap bounds the policy.** It bounds one delay; attempts and total deadline require separate bounds.
- **Jitter guarantees no herd.** It improves distribution under assumptions; it gives no deterministic fleet peak bound.
- **Idempotency key equals idempotency.** Atomic binding, fingerprint, scope, concurrency behavior, retention and downstream effects matter.
- **Same trace ID across attempts is enough.** Trace correlation is not durable effect identity.
- **Cancellation reverses a request.** It is a signal; committed/issued effects may persist.
- **A 5xx list defines retryability.** Endpoint semantics and outcome phase are necessary.
- **Retries belong at every boundary.** Independent owners multiply attempts and destroy deadline/load accounting.
- **Sleep is harmless.** Sleeping workers/timers consume concurrency, memory and shutdown responsibility.
- **Successful retry proves a good policy.** It may conceal bad timeouts, overload or needless duplicate work.
- **A durable queue guarantees exactly once.** Redelivery still requires idempotent consumption/effect reconciliation.
- **Recovery means remove limits.** Cold dependencies and queued clients make gradual, jittered admission essential.
- **Client policy can prove server correctness.** Durable idempotency and effect status require server-side evidence.

## Worked Examples

### Example 1

A catalogue `GET` fails before headers with a documented transient transport outcome. The application owns at most two retries inside 500 ms, with full jitter and attempt timeout derived from the remaining budget. Repetition is semantically safe, but a per-dependency retry token still limits fleet load. Success-after-retry is recorded separately from first-attempt success.

### Example 2

A `POST /payments` times out after dispatch. Reusing body without durable identity could charge twice, so status `timeout` is classified ambiguous, not retryable. With a server-side key atomically bound to principal, merchant, currency, amount and response, replay using the same key can return the committed result; changed content under that key is rejected.

### Example 3

An SDK defaults to three total attempts, a service mesh retries once and application code retries twice. The apparent “two retries” can produce 3 × 2 × 3 = 18 dependency attempts. The team assigns the application as semantic owner, disables mesh repetition, configures SDK to one attempt (except documented transparent non-dispatch), and exposes actual transport attempts.

### Example 4

Ten thousand clients receive overload simultaneously. Deterministic waits of 100, 200, 400 and 800 ms reproduce four spikes. Full jitter spreads each retry across its window, while a token budget caps admitted retries. Statistical load tests validate distributions; correlated seed/timer tests ensure clients do not accidentally choose identical sequences.

### Example 5

An absolute deadline has 260 ms remaining. The selected delay is 80 ms, meaningful attempt timeout is 150 ms and cleanup reserve is 40 ms. Because 80 + 150 + 40 = 270 ms, the attempt is not started. Reducing the timeout below what the dependency can meaningfully satisfy would manufacture another timeout, so the client returns the best terminal/reconciliation response.

### Example 6

A trusted service returns `Retry-After: 2`, but only 700 ms useful budget remains. The client does not sleep past its caller's deadline. For interactive work it returns/degrades; for an accepted durable workflow it can schedule later under a different explicit contract. Pushback informs policy but does not enlarge authority or time.

### Example 7

A database transaction reports a serialization conflict. Retrying only the final write repeats a stale decision. The retry unit is the whole bounded read-modify-write transaction under a fresh snapshot, with the original logical identity/deadline and a finite conflict budget. Validation, uniqueness and authorization failures remain terminal.

### Example 8

A webhook delivery must continue for hours. Sleeping an HTTP worker is wrong. The producer writes an outbox record; a durable scheduler leases due deliveries, uses capped jitter, retains delivery/effect identity, records terminal/next-at state and moves poison work under policy. Tenant concurrency, backlog age and downstream pushback are bounded.

### Example 9

During shutdown, a process has timers, in-flight attempts and ambiguous writes. It stops new logical admission, cancels pending delays, prevents new inline attempts, allows a bounded drain, reaps results, persists/reconciles durable effects and records terminal uncertainty. Destroying the timer/executor first would strand ownership and telemetry.

### Example 10

An emergency-command service retries neither merely because radio acknowledgement is absent nor merely because the command is marked urgent. Each command has authenticated durable identity, sequence/fencing and device-specific effect semantics. Ambiguity triggers status reconciliation or a hazard-approved safe action. Backoff, priority reserve and fail-safe deadlines require named safety, controls, security and operations review plus hardware-in-loop evidence.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): resilience ownership, dependency policy and composition boundaries.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): deterministic time/randomness, fault injection, statistical oracles and trace accounting.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): durable retry schedules, idempotent pipelines, deduplication and backlog control.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): authenticated effect identity, replay defense, quota abuse and telemetry protection.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): partial failure, ambiguity, delivery semantics and recovery coordination.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): SDK/mesh defaults, fleet budgets, pushback, rollout and incident recovery.

## References

1. Fielding, Roy T., Mark Nottingham, and Julian Reschke. “HTTP Semantics.” RFC 9110, Sections 9.2.2 and 10.2.3, June 2022. <https://www.rfc-editor.org/rfc/rfc9110>
2. gRPC Authors. “Retry.” gRPC Documentation. <https://grpc.io/docs/guides/retry/>
3. gRPC Authors. “A6: Client Retries.” gRPC Proposal. <https://github.com/grpc/proposal/blob/master/A6-client-retries.md>
4. Brooker, Marc. “Timeouts, Retries, and Backoff with Jitter.” Amazon Builders' Library, 2019. <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
5. Brooker, Marc. “Exponential Backoff and Jitter.” AWS Architecture Blog, 2015. <https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/>
6. AWS. “Retry Behavior.” AWS SDKs and Tools Reference Guide. <https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html>
7. Google Cloud. “Retry Strategy.” Identity and Access Management Documentation. <https://cloud.google.com/iam/docs/retry-strategy>
8. Beyer, Betsy, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds. *Site Reliability Engineering*. O'Reilly, 2016.
9. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018.
10. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017.
11. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013.
12. Jain, Raj. *The Art of Computer Systems Performance Analysis*. Wiley, 1991.
13. OpenTelemetry Authors. “Semantic Conventions for RPC Metrics.” <https://opentelemetry.io/docs/specs/semconv/rpc/rpc-metrics/>

Protocol/library defaults and supported retry, pushback, telemetry, cancellation and deadline behavior vary by version. Current official sources were checked on 2026-08-29; verify the exact client, proxy, mesh, broker and server deployment.

## Exercises

### Exercise 1

Specify retry disposition, owner, identity, schedule, deadline, capacity, telemetry and shutdown policy for catalogue reads, payment creation, database serialization conflict and webhook delivery. State which cases do not use inline retry.

### Exercise 2

A policy has base window 50 ms, multiplier 2, cap 400 ms and four retries. Compute the four windows and expected total delay under ideal full jitter. If three independent layers each apply this policy, compute the maximum leaf attempts for one logical request. Explain limitations.

### Exercise 3

A request has 1,000 ms remaining. Cleanup reserve is 100 ms. Candidate retry delays/meaningful attempt times are (120,300), (350,500), and server pushback (800,200) ms. Decide which can start under the stated admission inequality, then explain why attempts are evaluated sequentially against current remaining time rather than all against the initial 1,000 ms.

### Exercise 4

Diagnose a platform where the application, SDK and mesh retry; every 5xx/timeout is retryable; idempotency keys live in a five-minute process cache; timers are unbounded; deadlines reset; cancellation is reported as rollback; and recovery immediately releases all callers. Redesign it and define decisive tests.

### Exercise 5

Design retry and reconciliation for a safety-critical remote actuator with intermittent transport, strict command deadlines and irreversible effects. Include threat model, durable identity, ordering/fencing, ambiguity, fail-safe behavior, capacity, evidence and named human review.

## Answers to the Exercises

### Answer 1

Catalogue read: application/client adapter is sole owner; retry documented transient pre-response outcomes with capped full jitter, shared absolute deadline, attempt/token/concurrency bounds and no unsafe cache-fill assumption. Logical identity persists; attempt/span changes. Record dispositions and dependency load.

Payment creation: a timeout after dispatch is ambiguous. Inline replay is allowed only with a durable server authority that atomically binds an authenticated idempotency key to request fingerprint and recorded in-progress/terminal result; otherwise reconcile/query or return uncertainty. Never treat cancellation as rollback.

Serialization conflict: retry the whole read-modify-write transaction, not only the write, under finite attempts/deadline and only for the exact transient conflict class. Semantic constraint/auth/input errors terminate.

Webhook: use durable scheduling rather than an interactive sleeping loop. Persist effect/delivery identity, next-at, attempt/age caps, lease/fence, response classification and terminal/dead-letter policy. Bound tenant/dependency concurrency and backlog; honor trustworthy pushback. Shutdown stops leases, fences workers, persists state and reconciles in-flight effects. Across all four, inventory and disable/account for other retry owners.

### Answer 2

The capped windows are 50, 100, 200 and 400 ms. Under an ideal independent uniform full-jitter sample, expected delay per window is half its width, so

$$
E[D_{total}]=25+50+100+200=375\text{ ms}.
$$

Four retries mean five total attempts at each layer. Three independent owners can produce

$$
5^3=125
$$

leaf attempts for one top-level logical request.

Expected delay is not a deadline guarantee or fleet peak bound. Scheduling overhead, attempt times, pushback, cancellation, cap behavior, random-source independence and outcome-dependent early termination are omitted. Actual amplification may be smaller, but the architecture must not depend on good luck; choose one owner and enforce aggregate budgets.

### Answer 3

Use delay + attempt + reserve ≤ remaining. The first candidate requires 120 + 300 + 100 = 520 ms and fits. The second requires 350 + 500 + 100 = 950 ms and also fits if evaluated now with the full 1,000 ms. Pushback requires 800 + 200 + 100 = 1,100 ms and does not fit.

These are alternative decisions at one instant, not a preapproved sequence. If the first attempt actually runs, monotonic time, scheduling and attempt duration reduce the remaining budget. A later retry recomputes against then-current time; it cannot reuse the original 1,000 ms. The attempt timeout is capped by the remainder, and an attempt too short to be meaningful is rejected rather than launched to manufacture another timeout.

### Answer 4

Three owners multiply attempts and obscure load. A status-only classifier repeats permanent errors and ambiguous mutations. A process cache fails across replicas/restart, expires while late attempts exist and may not bind payload/principal. Unbounded timers consume memory and create recovery spikes. Reset deadlines violate caller authority. Cancellation cannot establish remote rollback. Releasing all recovery traffic creates a herd.

Assign application/semantic adapter as one owner; configure SDK/mesh to one attempt except verified transparent non-dispatch behavior and expose actual attempts. Define operation-specific disposition using dispatch/effect evidence. Build durable atomic idempotency binding and reconciliation for mutations. Propagate one absolute deadline; admit only useful attempts. Use exact capped jitter, retry tokens, dependency/tenant concurrency and finite durable scheduling for long delays. Validate pushback and retain jitter/ramped admission during recovery. Treat cancellation and late results explicitly.

Tests enumerate every error/outcome phase, duplicate/concurrent/restart/expiry/key-mismatch behavior, exact deadline boundaries, cancel during delay/dispatch/effect, layered attempt count, timer/token/concurrency memory bounds, correlated failure, random distribution/seeds, cold recovery, shutdown and telemetry conservation between logical operations and attempts. Real datastore/transport/fault/load evidence is required; mocks alone cannot prove durability or ambiguity.

### Answer 5

Define each command as an authenticated durable tuple: command/effect identity, actuator identity, command fingerprint, principal/authority/policy version, sequence or fencing generation, issue/deadline interval and expected state. The authority atomically reserves/binds identity and records issued, acknowledged, observed, failed or uncertain state. Replays with changed content/authority fail. The actuator/controller rejects stale sequence/generation and makes duplicate same-identity application observably idempotent if physically possible.

Loss after issue is ambiguous. Before repeating an irreversible effect, reconcile device state/ledger/telemetry under a hazard analysis. If state cannot be known, enter the defined fail-safe or human-controlled recovery; do not equate urgency with blind repetition. Cancellation prevents future safe work but does not undo issued actuation. Backoff is capped, jittered and subordinate to command deadline; safety reserve and priority capacity are explicit. Overload cannot starve fail-safe control, yet priority admission has abuse protection.

Threats include replay, key theft, identifier collision, authority expiry, forged acknowledgement, stale device generation, tenant flooding, downgrade and telemetry tampering. Use mutual authentication, integrity/confidentiality, nonce/sequence/fence validation, least privilege, protected audit and bounded quotas.

Evidence includes formal state/effect/ordering model, protocol and hardware contracts, model checking where feasible, hardware-in-loop duplicate/late/out-of-order/lost-ack tests, timing/worst-case and capacity analysis, power/network/process/controller restart, security/adversarial tests, fail-safe drills and durable reconciliation audit. Production approval requires named controls/domain safety, hardware, communications, concurrency/distributed systems, security, reliability/operations, human-factors and regulatory reviewers with traceable hazards and acceptance criteria.
