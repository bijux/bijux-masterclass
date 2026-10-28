---
module_id: API-039
program: API & Service Engineering
level: 1
module_number: 39
title: Rate Limits and Quotas
status: complete
last_verified: 2026-09-01
---

# Rate Limits and Quotas

## One-Page Review

### Governing question

How should an API bound request rate, burst, concurrent work, and contractual consumption across identities and distributed enforcement points while preserving fairness, availability, and actionable client recovery?

### Essential definitions

- A **rate limit** bounds admitted cost per unit time for a named policy and partition key.
- A **burst allowance** permits short arrivals above the sustained rate up to bounded stored capacity.
- A **quota** bounds cumulative entitlement over a longer accounting period or finite allocation.
- A **concurrency limit** bounds in-flight work rather than arrivals.
- A **partition key** identifies the subject of accounting, such as tenant, principal, client, address, operation, or resource.
- A **request cost** is the number of accounting units charged for estimated or measured work.
- **admission control** decides whether work may enter a constrained component before scarce resources are consumed.

### Central model, mechanism, or theorem

For a token bucket with sustained refill rate $r$, capacity $B$, previous tokens $T$, and elapsed time $\Delta t$, available tokens are

$$
T'=\min(B,T+r\Delta t).
$$

A request of cost $c$ is admitted only if $T'\ge c$, after which the balance is $T'-c$. The algorithm is useful only after defining verified partition key, policy scope, cost, clock, distribution, and failure behavior. Multiple hierarchical limits compose by requiring every applicable policy—global, tenant, principal, operation, resource, and concurrency—to admit the request.

### Critical invariants

Policies name their purpose, key, scope, unit, sustained rate, burst, concurrency, window, and change rules. Authentication-derived keys are verified; pre-auth limits use separately threat-modeled network/device evidence. Rejected work is stopped before the protected scarce resource. Expensive requests cost more than cheap ones where material. Global capacity and per-tenant fairness compose. Distributed overshoot and outage behavior are bounded and documented. `429` identifies requester-specific excess; `503` identifies service unavailability independent of that requester's rate. Retry advice is safe, scoped, and non-guaranteeing. Limits never replace authorization, validation, budgets, or capacity planning.

### Common failures

One fixed requests-per-second value for every operation; keying authenticated traffic only by IP; trusting a body tenant; letting attackers rotate unbounded keys; counting only successful requests; parsing/uploading a huge body before limiting; applying a gateway counter after backend fan-out; using fixed windows that double bursts at boundaries; allowing every node a full global burst; storing counters only locally during failover; returning `429` for server-wide overload; promising success at reset; exposing sensitive account tier or exact defense capacity; using unbounded key labels in metrics; and treating paid quota as protection against computational abuse.

### Compact example

A tenant may sustain 100 cost units/s with burst 200, while each report request costs 20 and each lookup costs 1. A separate tenant concurrency limit allows four reports, and a global limiter protects the report cluster. The gateway authenticates before tenant accounting, reserves cost before dispatch, and returns `429 report-rate-limited` plus bounded retry advice when the tenant bucket denies. Global overload returns `503`. **Conclusion:** units, identity, concurrency, and capacity are separate controls that compose.

### Connections

[Authentication Context Propagation](033-authentication-context-propagation.md) supplies trustworthy subjects, [Idempotency Keys](037-idempotency-keys.md) protects logical retries, and [Error Translation](035-error-translation.md) supplies `429`, `503`, and retry semantics. [Implementing a Predictable Service Endpoint](../ROADMAP.md) next composes these controls into a complete endpoint.

## Governing Question

Which traffic dimension is constrained, for whose verified identity, in what unit and time/concurrency model, at which enforcement point, with what distributed error bound, and with which public policy and operational response?

## Why This Matters

An API has several scarce resources: request parsing, connections, worker slots, database pools, lock time, memory, CPU, downstream calls, bytes, and human or financial capacity. Average traffic below nominal capacity can still fail a service when synchronized bursts exhaust one of them. One expensive query can cost more than thousands of cache hits.

Limits also allocate fairness. Without per-tenant controls, one noisy customer can consume a shared pool. Without a global capacity guard, every tenant can remain below its individual allowance while their sum overloads the service. Without concurrency limits, slow requests accumulate even at a moderate arrival rate.

Rate limits and quotas answer different questions. A token bucket smooths work over seconds or minutes. A monthly quota expresses entitlement or cost governance. A concurrency limiter reacts to work duration. A circuit breaker responds to dependency health. Treating them as one counter yields wrong recovery: waiting one second cannot repair an exhausted annual allocation, and buying quota cannot make a saturated database safe.

The public contract matters because clients coordinate retries and pacing from it. Yet limits are also security controls, and exposing exact global headroom or stable cross-tenant identifiers can help attackers. Responses must provide enough safe guidance without promising reservation or disclosing defense topology.

## Prerequisites and Retrieval

Retrieve arrival rate, service time, concurrency, queueing, token/leaky buckets, fixed and sliding windows, authentication identity, tenant isolation, HTTP `429`, `503`, and `Retry-After`, retries/backoff/jitter, distributed counters and clock behavior, load shedding, quotas/billing, caching, streaming, asynchronous jobs, observability cardinality, and abuse threat modeling.

Before defining a policy, retrieve the protected bottleneck, steady and burst capacity, operation cost distribution, traffic identity and trust, anonymous/NAT/proxy behavior, fairness objective, entitlement plan, retry behavior, regional topology, allowable overshoot, counter-store latency and outage policy, enforcement location, body/stream size, downstream fan-out, long-running work, reset semantics, privacy constraints, customer communication, emergency override, and measured validation plan.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish rate, burst, quota, concurrency, capacity, and abuse controls;
2. select partition keys and hierarchical policies from trustworthy identity;
3. compare token bucket, leaky bucket, fixed window, and sliding window behavior;
4. price heterogeneous request work and place admission before the bottleneck;
5. reason about distributed counters, overshoot, clocks, and fail-open/closed choices;
6. design safe `429`, `503`, `Retry-After`, and policy metadata; and
7. test fairness, boundaries, retries, degradation, and operational control.

## Core Exposition

### Name the protected resource and objective

“Prevent too many requests” is not a policy. Name the resource and desired outcome:

- protect authentication CPU before credentials are verified;
- preserve database pool slots per tenant;
- cap expensive search fan-out;
- prevent one client from monopolizing a shared downstream provider;
- limit concurrent exports and retained artifacts;
- enforce purchased monthly ingestion units; or
- slow enumeration and credential attacks.

Each objective may need a different key, algorithm, and response. A pre-auth source-address limit can protect password hashing but groups users behind NAT and can be evaded by address rotation. A verified tenant limit is fairer after authentication but does not protect the work required to authenticate. Layer both without pretending either identity is perfect.

Capacity protection and commercial entitlement must remain separable. An unlimited paid tier still needs emergency/global admission control. A free-tier quota should not be marketed as DDoS protection. Document policy owners: platform capacity, security abuse, and product entitlement changes have different review and incident paths.

### Define the accounting tuple

A durable policy can be represented as

$$
P=(i,s,u,r,B,C,W,e),
$$

where $i$ is partition identity, $s$ scope/operation, $u$ accounting unit, $r$ sustained rate, $B$ burst capacity, $C$ concurrency cap, $W$ quota/window, and $e$ enforcement/distribution rule.

Define whether the unit is requests, bytes, rows scanned, predicted CPU milliseconds, downstream calls, tokens, or domain units. Request counts are understandable but often poor proxies. A report with `limit=10000`, complex joins, and five expansions should not cost the same as a cached health lookup.

Keep cost predictable enough for clients. Use route classes and bounded parameters rather than an opaque bill computed only after execution. If actual cost differs, reserve estimated maximum before admission and reconcile/refund under explicit rules. Never permit a caller-controlled “cost” field to lower accounting.

State when units are charged. Invalid and unauthorized requests still consume edge/security resources and should usually count against those policies. A business quota might charge only accepted domain work. Idempotent replay consumes transport and lookup capacity even when it should not repeat the business quota/effect. Maintain separate meters.

### Choose trustworthy partition keys

Post-authentication keys can include tenant/account, effective principal, client/workload, operation class, target resource, and purchased plan. Derive them from verified context, not query/body claims. Scope impersonation and delegation deliberately.

Pre-auth keys can use source prefix, connection, TLS/client evidence, device risk, cookie, or attempted account, but each can be shared, spoofed, rotated, or privacy-sensitive. Combine signals for abuse controls and avoid permanently punishing an entire carrier-grade NAT.

Hierarchical keys improve fairness:

- global service/region capacity;
- dependency or shard capacity;
- tenant entitlement and noisy-neighbor protection;
- principal/client protection;
- operation/resource hot-spot limits; and
- anonymous/source abuse limits.

Admission requires all applicable policies. Define which denial is publicly reported without exposing internal global headroom or another tenant. Do not create an unbounded counter for every attacker-supplied string; validate, hash/aggregate, expire, and cap cardinality.

### Understand window algorithms

**Fixed window** counts within aligned intervals. It is simple and cheap, but a client can spend a full allowance at the end of one window and again at the start of the next, producing roughly double the nominal burst near the boundary.

**Sliding log** retains request timestamps and counts those within the trailing interval. It is precise but storage and processing grow with traffic.

**Sliding-window counter** combines adjacent-window counts approximately. It smooths boundaries with bounded state but needs a documented approximation.

**Token bucket** accumulates tokens at rate $r$ up to capacity $B$ and spends cost $c$ on admission. It permits bounded bursts while enforcing long-run rate. Use monotonic elapsed time inside a process and carefully define distributed time.

**Leaky bucket/queue shaping** drains work at a steady rate. It can smooth downstream traffic but adds queue latency. A finite queue must reject or shed when full; an unbounded queue merely converts overload into timeouts and memory exhaustion.

Choose from product semantics and bottleneck behavior, not familiarity. A monthly quota often uses ledger/counter accounting rather than a token bucket. Concurrency needs acquire/release leases or permits and protection against leaked ownership.

### Add concurrency and queue bounds

Little's Law relates average in-flight work $L$, admitted arrival rate $\lambda$, and average time in system $W$ by $L=\lambda W$ in a stable system. If service time rises, fixed arrival rate produces more concurrency. Rate limiting alone can therefore miss slow-request saturation.

Acquire a concurrency permit before the scarce worker, database, or downstream call and release it on success, failure, cancellation, and timeout. Bound wait queues and queue time; reject early when the remaining deadline cannot cover service.

Partition concurrency for fairness while retaining a global cap. Pure per-tenant caps can sum beyond capacity. Pure global caps let one tenant occupy everything. Weighted fair queues or reserved shares with borrowable slack can improve utilization, but document starvation and priority rules.

Streams and subscriptions consume permits for duration and may also consume byte/message rates. A request that upgrades or starts a stream cannot be charged only once at establishment. Define idle, lifetime, message, and bandwidth limits plus cleanup on disconnect.

### Enforce before expensive amplification

Put coarse controls at the edge before large bodies, decompression, authentication work, and routing where possible. After verified identity and parsed bounded parameters, apply accurate tenant and cost policies. Before database or downstream dispatch, acquire their capacity/concurrency permits.

One gateway request can fan out to hundreds of backend calls. A gateway request counter alone does not protect the dependency. Propagate a trusted cost/budget context or enforce independently at the owning backend. Never trust a caller-supplied internal bypass header across an unauthenticated boundary.

Reject uploads before fully buffering where content length is known; enforce streaming byte rates and absolute size while reading. Compression ratios and multipart counts need separate bounds. If the server discovers over-limit only after material work, it still stops further amplification and accounts honestly.

Admission decisions race capacity changes. A successful rate check is not a reservation of database success unless it acquires an actual permit. Keep waits bounded and release reservations reliably.

### Compose rate and quota policy

A request might need all of:

- one edge-abuse token;
- ten tenant compute tokens;
- one monthly report unit;
- one of four tenant report concurrency slots; and
- one global report-worker slot.

Choose an acquisition order that avoids holding scarce global permits while waiting on slower policy stores. If partial reservation occurs, release or expire it. For financial quotas, use an auditable ledger/atomic conditional decrement rather than approximate caches. For capacity shaping, small approximation may be acceptable.

Quota reset can follow calendar, rolling, subscription, or purchased-allocation semantics. Define time zone, inclusivity, clock source, plan changes, refunds, reservations, cancellations, and delayed usage reports. A long-term exhausted quota may need upgrade/contact guidance rather than an automatic short retry loop.

Separate hard and soft limits. Soft thresholds warn, emit events, or require confirmation; hard limits reject. Emergency safety controls can override plan entitlement downward. Human overrides need narrow scope, expiry, audit, and rollback—not permanent hidden exceptions.

### Design distributed enforcement honestly

A centralized strongly consistent counter gives clear global accounting but adds latency and a dependency. Per-node buckets are fast and available but multiply burst capacity. With $N$ independent nodes each allowed burst $B_n$, worst-case aggregate burst can approach $N B_n$ before reconciliation.

Mitigations include:

- divide global budget among nodes and rebalance leases;
- use a strongly consistent conditional counter for strict quotas;
- route a partition key to a stable owner;
- allocate regional budgets plus a small emergency reserve;
- accept bounded overshoot and reconcile; or
- combine local fast admission with a slower global feedback loop.

State the error bound. “Distributed rate limit” is incomplete without maximum overshoot, convergence delay, failover behavior, and partition policy. Billing/contract quotas usually require stronger accounting than abuse shaping.

Counter-store outage needs policy-specific behavior. Failing open preserves availability but can overload the protected system or bypass entitlement. Failing closed protects capacity/revenue but can cause broad denial. Use local bounded emergency budgets, cached leases with expiry, degraded operation classes, or safe shedding. Never turn an old unlimited lease into permanent authority.

Use monotonic time for elapsed refill where possible. Wall-clock jumps can add or remove tokens. Distributed reset timestamps and leases require synchronized-enough clocks or server-relative durations with conservative margins.

### Translate denial by cause

RFC 6585 defines `429 Too Many Requests` for a requester that sent too many requests in a period and permits `Retry-After`. It deliberately does not standardize how the user is identified or requests counted. Return a stable Problem Details type that distinguishes safe policy classes without revealing sensitive internals.

Use `503 Service Unavailable` when the responding service is temporarily unable to handle valid work because of general overload or maintenance, rather than blaming one requester's rate. During attack, responding `429` to every packet can itself consume resources; RFC 6585 notes that dropping connections or other measures may be appropriate.

`Retry-After` is advice, not reservation. It can express seconds or a date under HTTP semantics. Compute it for the denied policy and request cost; cap precision if exact reset leaks information. Clients respect deadlines, apply jitter, and avoid retrying all queued work at one reset instant.

Long-term quota exhaustion can still use a documented `429` policy when the requester's allocation is the reason, but the problem type and recovery should say “wait for billing reset” or “obtain allocation,” not imply a seconds-scale transient. Avoid `402` unless an application-specific contract defines it; HTTP does not make it a generic quota code.

### Treat rate-limit fields as evolving contract

Many APIs expose proprietary `X-RateLimit-*` fields with inconsistent semantics. As of the review date, the IETF HTTPAPI working group's `RateLimit` response-field work is revision 11 of an Internet-Draft, not an RFC. It defines structured policy information, but an implementation must track its status and must not claim final standard conformance.

If exposing fields, document policy name, remaining units, reset/delay meaning, scope, cost, and whether values are exact or conservative. Clients must not assume remaining capacity is reserved: concurrent requests and other nodes can spend it before the next call.

Avoid exposing global service capacity, other tenants' activity, security thresholds, or stable identifiers. Fields may be omitted or coarsened on anonymous/attack paths. Generate them from the enforcement decision, not a stale unrelated counter.

Version incompatible policy semantics and give clients migration time. Lowering a limit can break correct automation even without changing a schema. Publish effective dates and offer discovery/configuration where appropriate.

### Make clients cooperative

Clients should pace proactively, bound concurrency, coalesce work, cache, paginate reasonably, batch within documented size, and honor server advice. On `429`, retry only similar denied work after the applicable delay, with jitter and a total budget. On `503`, use a separate service-availability backoff and circuit-breaking policy.

A client with many workers needs one shared limiter; independent retry loops can multiply load. Preserve idempotency keys across retries of unsafe operations. Do not treat a replayed idempotent result as free transport capacity, but avoid charging the business quota twice.

Adaptive concurrency can reduce load when latency/errors rise, but feedback needs damping and minimum samples. It supplements explicit server policy rather than inferring entitlement from latency.

### Observe policy without cardinality explosions

Measure admitted and denied cost, active concurrency, wait time, queue depth, limiter latency/error, token/lease utilization, approximate overshoot, retry traffic, top operation classes, fairness, and downstream saturation. Attribute by bounded tenant tier or hashed sampled identity under privacy policy—not raw keys as metric labels.

Correlate denial with protected-resource health. If `429` rises while the database remains idle, limits may be too strict or mis-keyed. If latency and pool exhaustion rise before denials, enforcement is late or cost is wrong. Track false sharing behind NAT and key-rotation abuse.

Changes need simulation or shadow mode, staged rollout, rollback, and alerts. Test time/window edges with a controllable clock, not wall-clock sleeps. Chaos-test counter-store loss, region partition, node scaling, lease expiry, and cleanup.

The executable token-bucket model below illustrates refill, burst, weighted cost, and retry delay. It does not model concurrency, distributed overshoot, clocks, or production fairness.

<!-- bijux-verify: {"id":"weighted-token-bucket","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"report_a=allow remaining:2.0\nreport_b=deny retry:1.0\nreport_c=allow remaining:0.0\nlookup=deny retry:1.0\n","stderr":""}} -->
```python
class Bucket:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = float(capacity)
        self.updated = 0.0

    def admit(self, now, cost):
        self.tokens = min(self.capacity, self.tokens + self.rate * (now - self.updated))
        self.updated = now
        if self.tokens >= cost:
            self.tokens -= cost
            return f"allow remaining:{self.tokens:.1f}"
        wait = (cost - self.tokens) / self.rate
        return f"deny retry:{wait:.1f}"

bucket = Bucket(rate=1, capacity=5)
print("report_a=" + bucket.admit(0, 3))
print("report_b=" + bucket.admit(0, 3))
print("report_c=" + bucket.admit(1, 3))
print("lookup=" + bucket.admit(1, 1))
```

## Definitions and Notation

Let arrival cost rate be $\lambda_c$, service capacity be $\mu_c$, average in-system work be $L$, and average time in system be $W$. Stable long-run operation requires admitted load below effective capacity with burst/concurrency margins; Little's Law gives $L=\lambda W$ for a stable observed system.

For token bucket state $(T,t)$, rate $r$, capacity $B$, and request cost $c$ at time $t'$, refill gives $T'=\min(B,T+r(t'-t))$. Admission requires $T'\ge c$. A **partition key** determines which bucket/ledger applies. **Overshoot** is admitted cost beyond intended aggregate policy before distributed enforcement converges.

A **hard quota** rejects consumption beyond entitlement. A **soft quota** warns or triggers workflow. A **lease budget** allocates bounded units to an enforcement node/region. **Load shedding** rejects work to preserve bounded service for admitted requests. **Retry horizon** bounds how long/ often a client retries one denied operation.

## Mechanisms, Invariants, or Proof Structure

1. Name the protected bottleneck, fairness goal, and entitlement requirement.
2. Define verified partition keys, operation scope, accounting unit, and cost.
3. Select sustained rate, burst, concurrency, queue, and long-term quota separately.
4. Place coarse and precise admission before their protected resources.
5. Compose global, dependency, tenant, principal, operation, and resource policies.
6. Choose algorithm, clock, storage, regional ownership, and acceptable overshoot.
7. Define counter-store outage, failover, lease expiry, and emergency behavior.
8. Translate requester excess, quota exhaustion, and global unavailability distinctly.
9. Publish only safe, current, non-guaranteeing retry and policy metadata.
10. Test boundaries, distribution, fairness, attacks, client retries, and operational feedback.

The rate-safety claim is bounded by cost accuracy, key integrity, enforcement placement, and distributed error. A finite algorithm example does not prove capacity, fairness, or attack resistance.

## Alternatives and Trade-Offs

Fixed windows are cheap and explainable but permit boundary bursts. Sliding logs are precise but expensive. Approximate sliding counters smooth traffic with error. Token buckets express sustained rate plus burst naturally. Choose per policy.

Central counters enforce strict global limits but add latency and dependence. Local buckets are fast and partition-tolerant but overshoot. Leased budgets combine both with rebalancing complexity and stranded capacity.

Request counts are predictable but ignore heterogeneous work. Weighted cost protects capacity better but must be stable, bounded, and understandable. Measured post-execution cost is accurate for billing but too late for admission; reserve then reconcile.

Hard rejection preserves service but can harm critical customers. Queuing absorbs small bursts but increases latency and can collapse if unbounded. Reserved shares guarantee priority but may waste idle capacity; borrowing improves utilization with revocation rules.

Exact remaining/reset data aids client pacing but exposes policy and can be stale immediately. Coarse advice is safer but less efficient. Tailor disclosure to authenticated trust and threat level.

Fail-open counter outages preserve requests but can destroy the protected service. Fail-closed preserves capacity/accounting but causes denial. Bounded local leases and degraded modes make the trade-off explicit.

## Failure Modes and Misconceptions

- **“Rate limit equals quota.”** One shapes time; the other accounts entitlement/allocation.
- **“Requests per second measures load.”** Request costs and service times differ.
- **“IP identifies a user.”** NAT, proxies, mobility, IPv6, and rotation break that assumption.
- **“Use the body tenant as key.”** Scope must come from verified context.
- **“Count only successes.”** Rejected and invalid traffic still consumes protected layers.
- **“The gateway protects everything.”** Backend fan-out and resource hot spots need owned controls.
- **“Rate limiting bounds concurrency.”** Slow work can accumulate; use concurrency/queue limits.
- **“Every node gets the full limit.”** Aggregate burst/overshoot multiplies.
- **“Reset means capacity is reserved.”** Concurrent clients can consume it first.
- **“429 means the service is overloaded.”** Requester excess and general `503` differ.
- **“Paid unlimited means safe unlimited.”** Capacity controls remain mandatory.
- **“Retry immediately at reset.”** Respect budget and add jitter.
- **“Idempotent replay is free.”** It still consumes transport/lookup resources.
- **“Expose exact remaining globally.”** It can leak defense or other-tenant activity.
- **“RateLimit is already an RFC.”** The checked IETF document remains work in progress.

## Worked Examples

### Example 1

**Situation:** One tenant sends cheap GETs and expensive graph searches. **Reasoning:** Equal request counts underprice search. Charge bounded route/parameter cost units and keep a separate global search concurrency cap. **Conclusion:** account the bottleneck, not only envelopes.

### Example 2

**Situation:** Thousands of users share a mobile carrier NAT. **Reasoning:** A strict per-IP account limit blocks unrelated users. Use a coarse pre-auth source policy, then verified tenant/principal policies after authentication, with abuse risk signals. **Conclusion:** identity quality changes across the pipeline.

### Example 3

**Situation:** Client sends 100 requests at 59.9 seconds and 100 at 60.1 under a 100/minute fixed window. **Reasoning:** Boundary alignment admits 200 nearly together. Use token/sliding behavior or an explicit burst capacity. **Conclusion:** window algorithm determines real burst.

### Example 4

**Situation:** Ten nodes each allow burst 100 for a “global” tenant limit. **Reasoning:** A distributed client can approach burst 1,000. Allocate node leases summing to the global budget or accept and document overshoot. **Conclusion:** local correctness is not global enforcement.

### Example 5

**Situation:** Four long reports occupy every database connection despite low request rate. **Reasoning:** Arrival shaping missed service duration. Acquire tenant and global report concurrency permits before database work and bound the wait queue. **Conclusion:** concurrency protects occupancy.

### Example 6

**Situation:** A 2 GB upload is rejected only after buffering. **Reasoning:** The limiter failed to protect memory/bandwidth. Check headers early, stream-enforce bytes and rate, and stop decompression/multipart amplification at bounds. **Conclusion:** placement is part of the policy.

### Example 7

**Situation:** One tenant exhausts monthly export allocation. **Reasoning:** Return a stable quota-exhausted problem with billing-period recovery, not a one-second retry loop; global safety limits still apply after upgrade. **Conclusion:** quota recovery differs from transient rate recovery.

### Example 8

**Situation:** The central limiter store fails. **Reasoning:** Unlimited fail-open could collapse the database; fail-closed blocks all users. Use short-lived regional leases, reserve critical traffic, reject expensive work, and expire stale authority. **Conclusion:** outage policy is a capacity decision.

### Example 9

**Situation:** Every worker retries a `429` exactly at the reset second. **Reasoning:** Synchronization creates another spike. Share a client limiter, honor the delay, add jitter, cap concurrency, and stop at deadline. **Conclusion:** retry advice requires cooperative pacing.

### Example 10

**Situation:** Anonymous responses reveal exact global remaining report slots. **Reasoning:** Attackers can measure service load and tune attacks. Omit/coarsen capacity metadata, expose only caller-scoped safe policy, and shed cheaply under attack. **Conclusion:** limit observability has a threat model.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies leases, partitions, clocks, feedback, and bounded inconsistency. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies abuse identity, enumeration, denial-of-service, and disclosure analysis. [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies capacity, load shedding, SLOs, rollout, and incident controls. [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies online algorithms and approximation analysis. This API module makes admission and entitlement visible at the service boundary.

## References

1. M. Nottingham and R. Fielding, [*RFC 6585: Additional HTTP Status Codes*](https://www.rfc-editor.org/rfc/rfc6585.html), especially `429 Too Many Requests` and its security considerations, April 2012. Checked 2026-09-01.
2. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially `Retry-After` and `503`, June 2022. Checked 2026-09-01.
3. R. Polli, A. Martínez Ruiz, and D. Miller, [*RateLimit Fields for HTTP, draft-ietf-httpapi-ratelimit-headers-11*](https://www.ietf.org/archive/id/draft-ietf-httpapi-ratelimit-headers-11.html), Internet-Draft, May 2026; work in progress, not an RFC. Status checked 2026-09-01.
4. Amazon Web Services, [*Using Load Shedding to Avoid Overload*](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/), Amazon Builders' Library. Checked 2026-09-01.
5. J. D. C. Little, “A Proof for the Queuing Formula: $L=\lambda W$,” *Operations Research*, vol. 9, no. 3, 1961, pp. 383–387.

## Exercises

### Exercise 1

Design layered limits for anonymous login, authenticated reads, expensive tenant searches, export jobs, and monthly export entitlement. Name key, unit, algorithm, enforcement point, and response for each.

### Exercise 2

Compare fixed window, sliding log, sliding counter, token bucket, and leaky queue for a webhook ingestion API with bursty senders and a steady downstream database.

### Exercise 3

Diagnose a global “1,000 requests/minute” limiter implemented independently on 20 pods after request-body parsing, keyed by `X-Tenant` from the body, returning `429 Retry-After: 1` for all database overload.

### Exercise 4

Design distributed enforcement for a strict paid quota and a best-effort abuse rate across three regions during normal operation, partition, counter-store outage, failover, and plan change.

### Exercise 5

Create a verification and rollout plan for weighted tenant rate plus concurrency limits protecting a report service with retries, idempotency, streams, NAT users, and adversarial key rotation.

## Answers to the Exercises

### Answer 1

Before authentication, apply coarse source-prefix/device-risk token buckets to bound login parsing and password work, plus per-attempted-account controls that avoid enumeration. After authentication, use verified principal/client and tenant buckets for reads, charging route cost. Searches use weighted tenant+principal tokens and global/shard concurrency before fan-out. Exports acquire tenant and global job slots and account bytes/runtime during asynchronous execution; retries preserve idempotency identity but still consume request lookup cost. Monthly export entitlement is a strongly accounted tenant ledger with soft warnings and hard rejection/problem guidance at exhaustion. Every path also passes global emergency capacity control; requester excess is `429`, general overload `503`, and advice is bounded and non-guaranteeing.

### Answer 2

Fixed windows are simplest but permit boundary double bursts that can swamp the steady database. Sliding logs precisely bound trailing traffic but store every arrival. Approximate sliding counters smooth boundaries with small state and quantifiable error. A token bucket is usually a good admission fit: per-sender sustained rate matches downstream share while capacity permits expected webhook bursts. A finite leaky queue after admission can smooth accepted work to database rate, but it adds latency and needs deadline/overflow rejection. Combine per-sender token buckets, global capacity/concurrency, a bounded durable queue, idempotent event identities, and backpressure; do not use an unbounded queue as the limiter.

### Answer 3

The nominal aggregate limit is up to 20,000/minute plus boundary bursts because each pod owns a full counter. Enforcement after body parsing fails to protect bandwidth, memory, and parser CPU. Body `X-Tenant` is unverified and lets callers evade or attack another tenant's key. One request count ignores cost. A universal `429` mislabels general database overload, and one-second synchronized retries amplify it. Move coarse limits before body processing; derive tenant from authentication; use weighted hierarchical policies; allocate pod/region leases that sum to an aggregate or use authoritative counters; add database concurrency/load shedding; return caller excess as `429`, general overload as `503`, and calculate scoped delay with jitter guidance.

### Answer 4

For paid quota, use an auditable strongly consistent conditional ledger or home-region owner per tenant, with reservation/commit/refund semantics and versioned plan changes. During partition, route to the owner or fail closed for consumption that cannot be accounted; do not create unlimited regional credit. Small preallocated leases can preserve bounded availability and define maximum overshoot. On failover, fence old owners before issuing new leases and reconcile usage. For abuse rate, use fast regional/local token buckets plus global feedback, accept a measured overshoot bound, and shed aggressively when stores fail. Cached leases expire quickly. Plan increase creates new signed/versioned allocation; decrease handles already reserved units explicitly. Public responses disclose tenant-scoped recovery, not global topology.

### Answer 5

Replay production traces in shadow mode with bounded tenant identifiers and a cost model, comparing predicted cost with CPU, database time, fan-out, bytes, and latency. Test token/window boundaries with a fake clock; orchestrate simultaneous arrivals across nodes; inject counter outage, partition, scaling, lease expiry, and cancellation; and measure overshoot. Verify tenant+global concurrency release on success, error, timeout, stream disconnect, and worker death. Preserve idempotency keys while charging retry lookup but not duplicate business quota. Simulate NAT sharing and rotating keys to test layered identity/abuse controls. Stage enforcement by operation/tier/region, publish policy changes, monitor denial/fairness/protected saturation, retain emergency rollback, and inspect metrics/logs for raw or unbounded identity labels.
