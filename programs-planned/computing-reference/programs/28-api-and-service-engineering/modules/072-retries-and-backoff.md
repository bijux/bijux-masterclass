---
module_id: API-072
program: API & Service Engineering
level: 2
module_number: 72
title: Retries and Backoff
status: complete
last_verified: 2026-09-02
---

# Retries and Backoff

## One-Page Review

### Governing question

When can another attempt improve success without repeating an effect or worsening overload, and how should deadlines, attempt limits, backoff, jitter, server pushback, and retry-load budgets bound that decision?

### Essential definitions

- A **logical operation** is one user/domain intent; an **attempt** is one execution/transmission of it.
- A **retry** starts another attempt after an observed failure or ambiguous result.
- A **retryable failure** is plausibly transient and safe to attempt again under the same operation/effect identity.
- **backoff** delays later attempts; **exponential backoff** grows delay geometrically up to a cap.
- **jitter** randomizes delay to desynchronize clients; **full jitter** samples from zero to the capped exponential delay.
- A **retry budget** limits retry traffic relative to initial useful traffic or via tokens over a window.
- **server pushback** communicates delay or “do not retry” from the receiving service.
- A **retry storm** is positive feedback in which failures create attempts that add load and create more failures.

### Central model, mechanism, or theorem

For base delay $b$, multiplier $g>1$, cap $c$, and retry index $k\ge0$, capped backoff is

$$
d_k=\min(c,bg^k),\qquad J_k\sim U(0,d_k)
$$

for full jitter. Retry $k$ is admissible only if the original deadline has room for $J_k$, connection/setup, a minimum useful attempt, and final response; the operation remains identity-safe; the failure class is retryable; and per-request plus fleet/endpoint retry budgets allow it.

### Critical invariants

Every attempt carries the same logical operation/idempotency/effect identity and immutable request fingerprint. The client knows which statuses/phases are retryable and which are permanent, overload, expired, conflict, or uncertain. Only one intentional layer owns retries. Maximum attempts includes the initial attempt; total elapsed time and retry load are independently bounded.

Backoff is capped and jittered per client/operation, honors valid `Retry-After` or protocol pushback without exceeding deadline, and is cancelled when interest ends. Overload reduces retries rather than amplifying them. Non-idempotent or uncertain writes query outcome/reconcile before another effect attempt. Metrics separate logical operations, initial attempts, retries, transparent/library retries, successes-after-retry, budget suppression, pushback, and final outcomes.

### Common failures

Retry every error; retry validation/auth/conflict/expired commands; new idempotency key per attempt; `maxRetries` confused with total attempts; immediate or deterministic exponential schedules synchronize clients; uncapped delay; backoff sleeps past deadline; same timeout restarted each attempt; nested retries multiply; retrying an overloaded dependency; ignoring `Retry-After`; trusting absurd/unverified pushback; resetting counters after redirect/failover; retry budget per instance grows with autoscaling; retry after partial body/stream or committed write without semantics; SDK transparent retries invisible; retries switch region and violate affinity/order; and success-after-retry hides initial-failure rate.

### Compact example

Ten thousand clients receive a transient `503`. Fixed one-second retry creates another 10,000-request spike. With full jitter over `[0,2s]`, attempts spread at about 5,000/s on average, but that can still overload a 3,000/s dependency. A shared retry token budget and server pushback suppress excess attempts; callers whose deadlines cannot fit delay plus useful work fail. **Conclusion:** jitter reduces synchronization, while capacity-aware budgets determine whether retry is allowed at all.

### Connections

[Idempotency Keys](037-idempotency-keys.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), [Idempotent Consumers](067-idempotent-consumers.md), [Dead-Letter Handling](068-dead-letter-handling.md), and [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md) define identity, ambiguity, and the hard time envelope. The next modules add circuit breakers, bulkheads, load shedding, graceful degradation, and tail controls.

## Governing Question

For each failure and operation, who is authorized to make another attempt, with what unchanged identity, after what randomized delay, inside which time/load budgets, and how will the system prove retries improved rather than destabilized reliability?

## Why This Matters

Retries convert some transient failures into successes. Connections race with failover, packets are lost, leaders change, replicas restart, locks conflict, and load balancers select a bad endpoint. A second attempt can be exactly the right recovery mechanism.

Retries also create load precisely when a dependency may have least capacity. Google SRE describes positive feedback where overload failures are retried, increasing offered traffic until fewer requests succeed. Nested layers multiply attempts: three layers with four attempts each can send $4^3=64$ calls to the deepest dependency for one logical operation. Exponential schedules without randomness reproduce synchronized waves.

Safety is separate from transience. A timed-out read is usually repeatable; a timed-out charge may already have committed. HTTP method semantics, application idempotency keys, provider outcome lookup, database uniqueness, and consumer inbox/effect ledgers decide whether another attempt repeats an effect. A network error does not prove the server saw nothing.

Libraries can retry invisibly. gRPC documents transparent retry and configurable method policies, backoff, retry throttling, server pushback, and a commit point after response headers. Cloud SDKs, database drivers, proxies, service meshes, and brokers have their own defaults. The application must inventory all layers and reason about aggregate attempts, deadlines, identity, and telemetry.

## Prerequisites and Retrieval

Retrieve [HTTP Methods and Their Semantics](002-http-methods-and-their-semantics.md), [Idempotency and Safety](008-idempotency-and-safety.md), [Idempotency Keys](037-idempotency-keys.md), [Request-Scoped Transaction Boundaries](036-request-scoped-transaction-boundaries.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), [Idempotent Consumers](067-idempotent-consumers.md), and [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md).

Retrieve every client/SDK/proxy/mesh/load-balancer/driver/broker retry policy and default; method/status/transport failure semantics; idempotency/outcome-query contract; original deadline propagation; endpoint/region/affinity behavior; `Retry-After`/pushback support; backoff/jitter algorithm and RNG; retry throttling/tokens; queue/load-shedding signals; and attempt/log/trace metrics.

## Learning Objectives

After completing this module, you can:

1. distinguish logical operations, attempts, transparent retries, redelivery, replay, and hedges;
2. classify failures by transience, safety, ambiguity, overload, and business meaning;
3. preserve stable request/effect identity and resolve timeout-after-commit uncertainty;
4. design capped exponential backoff with appropriate jitter and server pushback;
5. fit attempts, delays, setup, and response inside one propagated deadline;
6. prevent multiplicative retries by assigning one owning layer;
7. enforce per-operation, per-client, endpoint, tenant, and fleet retry budgets;
8. coordinate retries with load shedding, circuit breakers, failover, ordering, and streams;
9. observe retry benefit, amplification, suppression, and final outcomes; and
10. verify policies under synchronized faults, overload, ambiguous writes, and recovery.

## Core Exposition

### Model one operation and many attempts

Assign one logical operation ID before the first attempt. Every retry preserves operation/idempotency/effect ID, canonical request fingerprint, tenant/subject, deadline, authorization context or documented reauthorization, and causation. Attempt number, endpoint, connection, start time, failure, and backoff are attempt metadata.

Define `maxAttempts` unambiguously as total attempts including initial. If configuration uses `maxRetries`, translate and report both. Counters do not reset when resolving DNS, following allowed redirects, changing connection, failover endpoint, or crossing a proxy unless a new logical operation is intentionally created.

Transport libraries may retry before application logic observes the call. Inventory and include those attempts in load/telemetry. gRPC distinguishes transparent retry from configured retry and commits the RPC after response headers, after which it does not retry automatically. Exact semantics are protocol/runtime specific.

Redelivery/replay is not necessarily a client retry, but shares identity/idempotency concerns. A hedged attempt overlaps rather than waits for failure. Keep categories distinct in metrics and policy.

### Classify before retrying

Build a method-specific decision table from phase, status/code, provider detail, whether request bytes may have reached application, and effect state:

- connection failure provably before send: often retryable;
- transient name/route/leader/unavailable: potentially retryable with backoff;
- overload/throttling: retry only with pushback and budget, often fail/degrade;
- deadline/cancellation: retry only if original deadline/interest remains;
- validation/malformed/unsupported: never retry unchanged;
- authentication: refresh once only for a well-defined expired credential, not bad credentials;
- authorization/policy: no blind retry;
- not found: only if eventual creation/replication contract makes it transient;
- conflict/precondition: re-read/replan, not identical transport retry;
- rate limit/quota: honor documented reset/pushback; hard quota may be terminal;
- domain rejection: normal terminal outcome;
- unknown/timeout after send: outcome query/idempotent same-key retry or reconciliation;
- server defect: bounded retry may move endpoint, but repeated signature opens circuit/escalates.

HTTP status class alone is insufficient: some `409` conflicts support a new conditional attempt after refreshed state; some `500` responses cache an idempotency-key result and should be returned consistently; some `404` are permanent. Publish safe machine-readable error/retry semantics.

Never retry an unchanged request when only input/policy can fix it. Retrying expensive deterministic failures wastes capacity and delays feedback.

### Prove operation safety

Safe/read-only methods can still have incidental metering/logging load, but intended resource effect is repeatable. Idempotent writes require the same key and fingerprint to return/resume one outcome. Conditional updates use versions/ETags and replan on conflict rather than blindly repeat stale state.

For external payment/email/shipment, persist effect intent and stable provider key before call. On timeout query outcome; if confirmed, return it; if absent and provider contract permits, retry same key; if unknowable, reconcile/manual action. A new key creates a new effect.

Stream/upload retries require replayable request body and resumption semantics. After partial upload/response consumption, restarting can duplicate data or violate ordering unless chunk IDs/offsets/checksums and server state are defined. Do not buffer unbounded bodies merely to enable automatic retries.

Authorization may expire/change during long backoff. Decide whether original accepted delegation continues or each attempt reauthorizes. Expired business command never becomes safe because transport is retryable.

### Use capped exponential backoff

For retry index $k$ after the initial attempt, compute $d_k=\min(c,bg^k)$. A common $g$ is 2, but base/cap/multiplier come from recovery times, deadline, load, and product requirements—not folklore.

Without cap, delays become operationally unusable/overflow. With a cap and no attempt/elapsed budget, clients retry at capped frequency forever. Bound total attempts, elapsed time, and retry tokens independently.

Backoff should occur before the next attempt, cancellable by caller/deadline. Deduct sleep elapsed from remaining budget. Do not schedule an attempt when delay+setup+minimum useful execution+response cannot fit.

Reset backoff only after meaningful sustained success or a new logical operation, not one lucky response during outage. Long-lived agents need state/token recovery rules so restart does not synchronize/reset an entire fleet.

### Choose and implement jitter

Deterministic exponential backoff synchronizes clients that failed together. Full jitter samples $J_k\sim U(0,d_k)$ and has expected delay $d_k/2$. Equal/decorrelated jitter variants trade minimum delay, spread, and memory of prior delay. Specify the actual algorithm and test distribution.

Randomness must be independently seeded across clients/processes; cloning VM/container RNG state or deterministic request seed can resynchronize. Avoid modulo bias/overflow and ensure duration units/rounding do not collapse small delays to zero.

Jitter spreads load; it does not reduce total retry count or make excess capacity appear. If 10,000 retries spread over two seconds hit a 3,000/s spare budget, throttling/suppression is still required.

For scheduled offline/mobile fleets, randomize initial schedule and retry; otherwise deployment/network restoration produces thundering herd even with later backoff.

### Honor server pushback safely

HTTP `Retry-After` can express a delay or date for statuses such as service unavailable; gRPC/provider mechanisms can communicate pushback. Treat valid pushback as a lower bound or policy input, clamped to remaining deadline/client maximum and adjusted for date clock skew.

Pushback can say do not retry. Honor it. Do not choose the smaller of exponential backoff and server delay merely to retry sooner. When no valid hint exists, use client policy.

Validate syntax/range; untrusted intermediaries/servers must not make clients sleep forever, overflow timers, or synchronize at an exact date. Add jitter around allowed server window when contract permits. Record source and chosen delay.

Server hints are advisory within end-to-end usefulness. If delay exceeds deadline, fail/degrade/queue durable work rather than wait. Hard quota reset may require asynchronous scheduling, not interactive retry.

### Fit the deadline budget

Before each retry calculate remaining $B(t)$ from [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md). Reserve final response/cleanup and, for writes, outcome query. Attempt timeout is at most remaining budget minus delay/future reserve.

Do not give every attempt the full original timeout. A three-attempt policy with 500 ms each cannot fit a 700 ms caller deadline plus backoff. Prefer fewer meaningful attempts over many cut short attempts.

When initial failure arrives late, retry may be impossible even if error class is transient. Report deadline/budget suppression separately from nonretryable. Cancellation interrupts backoff timers immediately.

For asynchronous jobs, per-attempt deadline/backoff lives inside business expiry/age/max-attempt policy. Persist next-attempt time and counters; process restart does not reset them. Late commands terminate or dead-letter with explicit disposition.

### Assign one retrying layer

Place retry where operation semantics, deadline, identity, and failure classification are best known—often the edge/application caller for whole operation or a carefully selected client library for one dependency. Disable/restrict other layers.

If $L$ layers each allow $A_l$ total attempts, worst deepest attempts are $\prod_l A_l$. Three layers with four attempts create 64. Even when probabilities reduce average, correlated outages approach worst case.

Infrastructure transparent retry can be safe for proven pre-application failures, but it still consumes network/capacity and must be observable. Application retry should account for library attempt commitment behavior. Database transaction retries belong around the whole transaction after rollback, not individual statements that leave inconsistent context.

Service meshes cannot infer business idempotency from method/path alone unless contract/config is exact. Avoid enabling broad write retries by default.

### Enforce retry budgets and throttling

Per-request max attempts prevents one operation looping; it does not cap a million clients. Add retry budget per destination/method/tenant/client/fleet. Express as tokens, maximum retry-to-initial ratio, or rate/concurrency tied to successful initial traffic.

A token bucket spends tokens on retry and replenishes on qualified successes/new requests up to cap. gRPC retry throttling describes a token counter that decreases on failures and recovers on success, pausing retries below a threshold. Exact policies differ.

Budget should follow destination failure domain, not only process. Autoscaling 100 clients each with independent generous bucket can multiply retry load. Central/global coordination improves cap accuracy but adds dependency; combine conservative local tokens with service pushback/load shedding and fleet telemetry.

Fairness prevents one tenant/key/operation from consuming all retry capacity. Critical safe reads may get a tier distinct from batch enrichment. Never allow retries to bypass normal quotas/admission.

Budget exhaustion returns/degrades/queues durably; it is a protection success, not a client-library bug. Alert on sustained suppression and root cause.

### Coordinate with overload controls

Overload is the worst time for optimistic retries. Servers shed early with explicit overload/pushback. Clients reduce attempts, lengthen backoff, open circuit, use alternate safe capacity, degrade, or fail. Retrying immediately against another replica can spread a local problem into regional cascade.

Failover is not free. Preserve data locality, session/leader affinity, consistency, idempotency store scope, and region authority. A cross-region retry can double a non-global effect or read stale state. Endpoint selection requires contract.

Circuit breaker blocks attempts during known failure; half-open probes consume dedicated small budget and are not general retries. Bulkheads isolate retry concurrency. Load shedding applies equally to retries and may prioritize initial useful work.

Cache/stale/partial response can be more valuable than another attempt. Degradation semantics must be explicit and observable.

### Handle batches, queues, and streams

For batch APIs, retry only failed items when per-item outcomes/identities are authoritative. Retrying whole batch can duplicate completed items. If batch is atomic, one batch ID/outcome governs retry.

Message consumers use redelivery/delayed retry rather than blocking worker sleep. Preserve message/effect ID, attempt/first-failure time, key/version, and deadline. Retry topics can reorder; keep per-key gap policy. After bounded attempts/age, dead-letter/terminal disposition with ownership.

Streams need reconnection/resumption token/offset and replay window. A disconnect after receiving data cannot simply restart at zero. Preserve last acknowledged position and deduplicate frames/events. Backoff reconnects with jitter and respects server limits; fleet reconnect after outage needs budget.

Long polling/webhooks distinguish transport delivery attempts from business event identity. A webhook sender records each attempt and recipient response but reuses event ID/signature semantics.

### Observe whether retries help

Measure logical operations, initial attempts, total attempts, retries by index/reason/phase, transparent/library retries, retryable decisions, suppressed by deadline/budget/circuit/pushback, backoff requested/actual, server hints, endpoint/region, success-after-retry, final failure, unknown outcome, and latency/load/cost amplification.

Key ratios include attempts per operation, retry traffic as fraction of initial traffic, recovery probability by attempt index/error, added latency, and marginal successes per retry. If third retries almost never succeed, remove them. If retry successes conceal high initial failure, alert on initial health separately.

Trace one logical operation with child attempt spans/links and stable operation ID while avoiding sensitive/high-cardinality metric labels. Record the final outcome once; do not count each failed attempt as independent user failure.

Dashboards correlate retry rate with dependency saturation, load shedding, circuit state, deadlines, deployments, regions, and SLO/error budget. Retry storms can look like demand growth unless attempts are separated.

### Verify policy under faults

Unit/property tests cover classification table, stable identity/fingerprint, total-attempt semantics, exponential/cap arithmetic, full-jitter bounds/distribution, timer cancellation, deadline feasibility, pushback parsing/clamping, token replenishment/spend, and overflow/clock/RNG edges.

Integration tests fail before send, after partial send, before/after application receipt, after commit before response, during response body, and across connection/leader/region changes. Assert which layer retries, exact attempts, unchanged ID, outcome query, and no duplicate effects.

Load/chaos tests synchronize thousands of clients, restart fleets, fail a dependency, overload it, send pushback, partition a region, recover capacity, and vary autoscaling. Verify retries decay/spread, remain below budget, initial traffic is protected, circuits/bulkheads coordinate, and recovery does not create a herd.

Test batch partial results, queue retry ordering/expiry/DLQ, stream resume, process restart with persisted counters, and malicious pushback. Reconcile logical outcomes/effect ledgers, not only transport successes.

## Definitions and Notation

Let $A$ be total maximum attempts including initial, $k\in[0,A-2]$ retry-delay index, base $b$, multiplier $g$, cap $c$, and full-jitter delay $J_k\sim U(0,\min(c,bg^k))$ with expected value half its upper bound.

If each failed attempt independently warrants another with probability $p$, expected truncated attempts are $E[N]=\sum_{i=0}^{A-1}p^i=(1-p^A)/(1-p)$ for $p\ne1$. Correlated outages invalidate independence and approach $A$.

For layers $l=1..L$ with total attempts $A_l$, worst deepest attempts per logical operation are $\prod_l A_l$. Let initial request rate be $\lambda_0$ and retry rate $\lambda_r$; retry ratio/budget may constrain $\lambda_r/\lambda_0\le\rho$ over a defined window and destination scope.

## Mechanisms, Invariants, or Proof Structure

1. Assign stable logical/effect identity and immutable fingerprint before initial attempt.
2. Inventory all retrying layers, transparent behavior, endpoints, and commitment boundaries.
3. Classify each method/status/phase by transience, safety, ambiguity, overload, and business meaning.
4. Select one owner and explicit total attempts, elapsed/deadline, backoff/jitter, pushback, and endpoint policy.
5. Before each attempt verify original interest/deadline, useful-work floor, idempotency/outcome state, and retry tokens.
6. Use cancellable capped randomized backoff; preserve counters across restart/failover.
7. Suppress retries during overload through budgets, pushback, circuits, bulkheads, and shedding.
8. Handle batch/queue/stream retry with per-item/message/position identity, order, expiry, and terminal path.
9. Observe logical outcomes separately from attempts and measure marginal retry benefit/amplification.
10. Verify synchronized, ambiguous, overloaded, multi-layer, regional, recovery, and adversarial cases.

Proof sketch: unchanged identity plus an authoritative idempotency/effect protocol makes repeated attempts observationally one effect within its scope. Capped jitter spreads attempt times, and retry budgets bound added load under their scope. Neither proves recovery: correlated clients can still exceed capacity, semantic-unsafe operations can duplicate, and nested/unobserved layers can violate the bound.

## Alternatives and Trade-Offs

**No retry versus bounded retry.** No retry minimizes load/ambiguity but exposes transient faults. Bounded retry improves availability when recovery probability justifies added time/load.

**Fixed versus exponential backoff.** Fixed is predictable but synchronized/aggressive during long outage. Exponential reduces frequency; cap/attempt budget prevents impractical or endless waits.

**Full versus equal/decorrelated jitter.** Full jitter maximizes spread and can retry immediately; equal retains a minimum; decorrelated evolves from prior delay. Select from workload/recovery evidence.

**Client versus server-controlled delay.** Client works without trusted hints; server knows overload/recovery better. Combine validated pushback with client maximum/deadline/jitter.

**Local versus global retry budget.** Local is available/simple but multiplies with fleet scale. Global is accurate but adds coordination/failure. Conservative local plus server shedding/telemetry is common.

**Same endpoint versus failover.** Same preserves locality/session/cache; alternate escapes instance fault but may spread overload/violate consistency or effect scope.

**Retry versus asynchronous durable scheduling.** Interactive retry fits short transient windows. Durable scheduler handles long recovery but changes response/workflow contract and needs expiry/status.

**Retry versus hedge.** Retry waits for failure; hedge overlaps and cuts tail at higher load. Both require deadline/idempotency/budget, but hedges need loser cancellation.

## Failure Modes and Misconceptions

1. Every `5xx`, timeout, network error, or exception is retried identically.
2. Validation, authorization, conflict, domain rejection, or expired work retries unchanged.
3. New idempotency/effect ID is generated per attempt.
4. `maxRetries` and total attempts are confused across libraries.
5. Backoff is deterministic, uncapped, non-cancellable, or sleeps beyond deadline.
6. Jitter is assumed to reduce total load/capacity need.
7. RNG seed/rounding synchronizes cloned clients.
8. Server pushback is ignored, shortened, malformed, or trusted without bounds.
9. Each attempt restarts original timeout/deadline.
10. Browser, gateway, mesh, service, SDK, and driver all retry multiplicatively.
11. Retry counters reset on process restart, redirect, endpoint, or region change.
12. Per-instance token buckets expand retry capacity with autoscaling.
13. Retries bypass quotas, load shedding, circuit, or tenant fairness.
14. Partial batch/upload/response/stream is restarted without item/offset semantics.
15. Overloaded service is retried onto every healthy replica/region.
16. Timeout-after-commit is treated as failure and non-idempotent effect repeats.
17. Success-after-retry masks initial failure and excessive marginal cost.
18. Tests cover one client/steady state but not synchronized fleet failure/recovery.

## Worked Examples

### Example 1

A GET fails before response with transient connection reset. One owning client retries same operation under remaining deadline with full jitter. Proxy/mesh retries are disabled, so total attempt count is known.

### Example 2

A POST charge times out after send. Client queries `charge-88`; provider reports success. It returns existing outcome rather than retrying with a new key.

### Example 3

Four total attempts use $b=100$ ms, $g=2$, $c=500$ ms. Full-jitter bounds before retries are `[0,100]`, `[0,200]`, `[0,400]` ms; expected waits total 350 ms before setup/execution.

### Example 4

Browser, gateway, and service each allow four total attempts. Worst database calls are $4^3=64$. Policy assigns retries only to the service's database client with three total attempts; upper bound becomes three.

### Example 5

A 503 includes valid `Retry-After: 10`, but caller has 3 seconds remaining. Client does not retry interactively; it returns/degrades instead of sleeping past usefulness.

### Example 6

Dependency overload drops retry tokens below threshold. Initial requests still receive admission/fail-fast results, but retry attempts pause until successes replenish tokens. Suppression prevents positive feedback.

### Example 7

A batch of 1,000 items returns 970 successes and 30 typed transient failures with per-item IDs. Client retries only 30; retrying whole batch would repeat 970 effects.

### Example 8

After a regional outage, one million mobile clients reconnect. Randomized initial scheduling, exponential full jitter, server pushback, and destination retry budget prevent a synchronized recovery wave.

### Example 9

A stream disconnects after acknowledged offset 9,200. Reconnect resumes from 9,201 with same subscription identity and deduplicates overlap; it does not replay from zero as a new business stream.

### Example 10

Third retries recover 0.01% of operations but add 7% dependency traffic and 400 ms tail latency. Evidence supports reducing attempts and investing in failover/capacity rather than calling every eventual success a win.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, ambiguity, clocks, idempotency, and failure detectors. [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies randomized algorithms, probability, queues, and control policies.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transaction retries, serialization/deadlock handling, uniqueness, and commit recovery. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies connection phases, routing, transport loss, congestion, and failover.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns SDK/mesh defaults, token budgets, telemetry, rollout, and load/fault tests. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes feedback-loop stability, margins, hazard analysis, and verification. [Security Engineering](../../25-security-engineering/ROADMAP.md) contributes authorization refresh, tenant fairness, pushback trust, and abuse controls.

## References

1. gRPC Authors. “Retry.” Retrieved 2026-09-02. <https://grpc.io/docs/guides/retry/>
2. Amazon Web Services. “Timeouts, Retries, and Backoff with Jitter.” Amazon Builders' Library. <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
3. Brooker, Marc. “Exponential Backoff and Jitter.” AWS Architecture Blog. Updated May 2023. <https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/>
4. Ulrich, Mike. “Addressing Cascading Failures.” *Site Reliability Engineering*. <https://sre.google/sre-book/addressing-cascading-failures/>
5. Beyer, Betsy, et al. “Reliable Product Launches at Scale.” *Site Reliability Engineering*. <https://sre.google/sre-book/reliable-product-launches/>
6. IETF. “RFC 9110: HTTP Semantics.” June 2022. <https://www.rfc-editor.org/rfc/rfc9110>

## Exercises

### Exercise 1

Create a retry decision table for GET, idempotency-keyed POST payment, conditional PATCH, batch create, webhook delivery, and stream resume across connection-before-send, timeout-after-send, `429`, `503`, validation, authorization, conflict, and domain rejection.

### Exercise 2

A policy allows five total attempts with base 80 ms, multiplier 2, cap 500 ms, and full jitter. Compute each jitter upper bound and total expected backoff. With 1.4 seconds remaining, 100 ms final reserve, and 220 ms minimum useful attempt, determine whether all attempts can be guaranteed to fit using worst-case delays (ignore prior attempt durations only for this bound).

### Exercise 3

Three layers allow three total attempts each. Compute worst deepest attempts. If each attempt independently fails retryably with probability 0.2 and one layer owns four total attempts, compute expected truncated attempts. Explain why outage planning cannot rely on independence.

### Exercise 4

Design a retry budget for 20,000 initial requests/s to one dependency with at most 8% additional retry traffic, per-tenant fairness, 200 client instances, autoscaling, server pushback, and circuit/load shedding. Include token semantics, scope, recovery, telemetry, and failure modes.

### Exercise 5

Design and verify retries for a cross-region order/payment API with SDK and mesh retries, ambiguous commits, failover, batches, asynchronous jobs, and streams. Include identity, deadlines, classification, backoff/jitter, ordering, authorization, outcome query, DLQ, observability, and synchronized recovery tests.

## Answers to the Exercises

### Answer 1

GET: retry proven pre-send/transient timeout/503/429 only within deadline, pushback, and budget; validation/auth/domain rejection no; 404/conflict only under explicit consistency/replan semantics. Idempotency-keyed payment POST: pre-send retry; after-send timeout first query/same-key retry under provider contract; 429/503 same key and pushback; validation/auth/domain decline terminal; conflict queries/replans rather than fresh key.

Conditional PATCH: retry transport only with same precondition when outcome is known absent/idempotent; on conflict fetch current state and create a new deliberate operation, not blind retry. Batch create: atomic batch uses one batch key/outcome; per-item batch retries only failed retryable IDs, never whole successes. Webhook reuses event/delivery identity, signs each attempt as specified, backs off on transient/429/503, treats durable recipient success as complete, and dead-letters after age/attempt policy. Stream resumes from acknowledged token/offset with overlap dedup; validation/auth may require correction/refresh, not position reset.

For every method, cancellation/expired deadline stops retries; authorization refresh is at most one defined credential path and does not override forbidden. Domain rejection is a normal final result. `Retry-After` and failure details are validated/clamped. Same ID with changed fingerprint is conflict/quarantine.

### Answer 2

Five total attempts imply four retry delays. Uncapped values are 80, 160, 320, and 640 ms; capped upper bounds are 80, 160, 320, and 500 ms. Full-jitter expected delays are half: 40+80+160+250=530 ms total.

Worst-case delays total 1,060 ms. Available after final reserve is 1,300 ms. One minimum useful retry attempt needs 220 ms, leaving only 20 ms if all worst delays occur; four useful retry attempts would need 880 ms. Therefore the full five-attempt sequence cannot be guaranteed to fit. Runtime must recompute after each attempt and delay; cap/skip later retries when delay+220 ms+100 ms response reserve does not fit. Expected delay is not a safety guarantee.

### Answer 3

Worst deepest calls with three layers and three total attempts each are $3^3=27$. With one owning layer, four total attempts, and independent retryable failure probability $p=0.2$, expected attempts are

$$
1+0.2+0.2^2+0.2^3=1.248.
$$

Outages, overload, configuration defects, and regional failures correlate attempts: conditional failure probability remains near one for all clients/attempts, so behavior approaches the maximum four (or 27 nested), and clients synchronize. Capacity/hazard planning uses worst/correlated scenarios plus measured dynamics, retry budgets, jitter, circuits, and pushback—not the independent expectation.

### Answer 4

Eight percent of 20,000/s is at most 1,600 retry attempts/s over a defined rolling window at this destination/method. Reserve budgets by tenant/tier while allowing unused share to a bounded common pool; one tenant cannot exhaust all. Initial requests never consume retry tokens and remain subject to normal admission.

Use conservative local token buckets on 200 instances totaling materially below 1,600/s (for drift/autoscaling), configured from a fleet coordinator/service policy; autoscaling divides/rebalances rather than granting every new instance a full independent bucket. Spend one token when a retry actually starts; no refund on cancellation/failure. Replenish based on qualified initial/success traffic up to cap slowly enough to avoid instant herd. Server pushback/circuit open can reduce allowed rate to zero regardless of tokens.

Track global/local tokens, configured/effective fleet capacity, initial/retry rates, tenant shares, attempts/operation, suppression reason, pushback, circuit/load-shed state, marginal success, dependency saturation, and autoscale membership. Fail closed/conservatively if coordinator/config is stale; validate clocks/windows. A token is permission only if operation safe, retryable, deadline-feasible, and endpoint valid.

Test 200→400 autoscale, instance restart/token reset, partitioned coordinator, hot tenant, synchronized 503/429, pushback do-not-retry, recovery, and region failover. Verify retries stay ≤1,600/s (or deliberately lower), initial capacity is protected, and budget recovery does not burst.

### Answer 5

Inventory/disable overlapping SDK/mesh/application policies; allow only proven transparent pre-application retries below one application owner. Assign order command/payment effect IDs and immutable fingerprints before first attempt; preserve across region, batch, job, and stream. One propagated deadline/business expiry bounds delays/attempts; authorization is rechecked per documented accepted-delegation policy.

Classify pre-send, unavailable/leader, overload/429/503+pushback, validation/auth/domain/conflict, deadline, and unknown-after-send. Payment/order commit timeout queries authoritative operation/effect state and retries same ID only when safe. Region failover requires authority/fencing and globally valid idempotency scope; otherwise pause rather than double-write. Conditional conflicts replan.

Use capped full/decorrelated jitter with independent seeds, total attempt/elapsed/fleet/tenant budgets, cancellable sleeps, and useful-work feasibility. Preserve order key/version; retry topic/job persists attempt/first-failure/next-time/deadline and dead-letters with case ownership. Batch retries failed item IDs only. Stream resumes acknowledged position with overlap dedup.

Observe logical operation and child attempts, layer/transparent retries, endpoint/region, failure class, requested/actual backoff, pushback, tokens/circuit/shedding, deadline suppression, same-ID outcome, batch items, queue age/DLQ, stream resume, final outcome and added load/latency. Reconcile order/payment ledgers.

Test every before/after-send/commit boundary, SDK+mesh configuration drift, 3-layer multiplication, cross-region partition/stale authority, synchronized client outage/recovery, autoscaling token multiplication, malformed pushback, RNG clone, deadline edge, partial batch, job restart counter persistence, DLQ/redrive, and stream overlap. Assert one business effect, bounded attempt/load, protected initial traffic, preserved order, and no herd on recovery.
