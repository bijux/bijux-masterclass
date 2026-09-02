---
module_id: API-080
program: API & Service Engineering
level: 2
module_number: 80
title: Preventing Failure Amplification Across Service Calls
status: complete
last_verified: 2026-09-02
---

# Preventing Failure Amplification Across Service Calls

## One-Page Review

### Governing question

How can one admitted user operation remain a bounded amount of downstream work when fan-out, retries, hedges, fallbacks, failover, caches, queues, health controls, and recovery all react to the same fault?

### Essential definitions

- A **logical operation** is the caller-visible intent whose identity and deadline survive all internal branches and attempts.
- **Amplification** occurs when one logical operation creates multiple downstream attempts, work units, resource holds, or failure signals.
- A **branch** is distinct required or optional subwork; an **attempt** is one execution of a branch.
- A **retry** follows a failed attempt; a **hedge** overlaps a slow attempt; **redelivery** repeats message delivery; a **fallback** takes an alternate path.
- **Orphan work** continues after its caller timed out, canceled, or accepted another result.
- A **retry owner** is the one layer authorized to create another sequential attempt for a logical boundary.
- An **amplification budget** bounds attempts, fan-out, concurrency, cost, age, and topology across the whole operation.

### Central model, mechanism, or theorem

For call-graph depth $d$, let $F_l$ be maximum fan-out per admitted branch and $A_l$ be maximum attempts per branch at layer $l$. The worst-case number of attempts reaching depth $d$ is

$$
N_d=\prod_{l=1}^{d}(F_lA_l).
$$

The bound is a warning, not a capacity target. The durable mechanism is budget conservation: child calls inherit one absolute deadline, operation/effect identity, criticality, and finite cost/attempt tokens; they can spend or subdivide those tokens but cannot mint more. The dependency still performs local admission from its actual capacity.

### Critical invariants

Every logical operation has stable identity and one end-to-end deadline. Every network, SDK, proxy, broker, and application attempt is counted. One layer owns retries for a boundary; hedges and failover consume the same attempt/cost budget. Fan-out cardinality and concurrency are bounded. Cancellation reaches descendants and results are ignored idempotently if work cannot stop.

Dependencies reject excess work early, preserve tenant/priority isolation, and do not trust clients to self-declare criticality. Fallbacks are simpler and independently capacitated. Circuits, bulkheads, shedding, backpressure, and retry policy share the same failure-domain model. Recovery ramps gradually while caches, connections, and capacity become ready.

### Common failures

An SDK, mesh, application, and workflow engine all retry; all-of fan-out waits for one straggler; a hedge is sent immediately to the same saturated shard; cancellation stops waiting but not work; timeout creates a new idempotency key; failover sends a full region's load to half its capacity; fallback calls another fragile service; cache loss multiplies origin traffic; redelivery and consumer retries multiply effects; health ejection shrinks capacity during overload; every client holds a private retry allowance; `200 after retry` hides the first-attempt collapse; and recovery releases every queued caller simultaneously.

### Compact example

Three layers each fan out to four branches and allow three total attempts per branch. One admitted operation can create $(4\times3)^3=1{,}728$ deepest-layer attempts. An end-to-end budget that permits only 20 cost tokens cannot make that graph cheap after the fact: each layer must reserve required work, reject optional branches, and spend attempts from the inherited 20. **Conclusion:** local limits do not compose unless the operation carries a conserved global bound.

### Connections

[Retries and Backoff](072-retries-and-backoff.md), [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), [API-Level Load Shedding](074-api-level-load-shedding.md), [Backpressure Across Service Boundaries](075-backpressure-across-service-boundaries.md), and [Fan-Out and Tail Latency](077-fan-out-and-tail-latency.md) provide individual controls. This module composes them into one call-graph safety policy before lifecycle governance begins.

## Governing Question

What invariant ensures that a failure or slowdown causes less optional work, not more total work, across every synchronous and asynchronous service boundary—and how is that invariant proved under overload, partial failure, cache loss, redelivery, failover, and recovery?

## Why This Matters

A service can be well within its steady-state request rate yet collapse after a dependency slows. Requests stay in flight longer, callers time out, retries create duplicates, queues grow, health checks eject slow replicas, and the remaining replicas receive more work. Positive feedback converts a local capacity shortfall into a system-wide outage.

Local resilience mechanisms can cause the cascade. A retry improves an isolated transient failure; a hedge trims an isolated tail; failover restores a lost endpoint; fallback preserves a feature; autoscaling replaces capacity. If several layers react independently, each can multiply traffic precisely when useful capacity is smallest. Google SRE documents this pattern as cascading failure and warns that retry counts multiply across layers. AWS likewise describes overload feedback from timeouts, wasted work, retries, and deep call graphs.

Request rate alone misses the real cost. One API call might scan one row or fan out to thousands of shards. A timed-out attempt can continue using CPU and database connections after the client has left. A cache normally absorbing 95% of traffic can disappear and place twenty times the usual request rate on its origin. An apparently successful retry can conceal deteriorating first-attempt health.

The design goal is not zero retries or zero redundancy. It is bounded, semantically safe work whose authority and observability compose across layers. The system must retain goodput—useful completed operations—while rejecting or degrading excess work cheaply, and it must recover without another synchronized surge.

## Prerequisites and Retrieval

Retrieve [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), [Idempotent Consumers](067-idempotent-consumers.md), [Dead-Letter Handling](068-dead-letter-handling.md), [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), [Retries and Backoff](072-retries-and-backoff.md), [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), [API-Level Load Shedding](074-api-level-load-shedding.md), [Backpressure Across Service Boundaries](075-backpressure-across-service-boundaries.md), [Fan-Out and Tail Latency](077-fan-out-and-tail-latency.md), [Partial Results and Graceful Degradation](078-partial-results-and-graceful-degradation.md), and [Consistency and Read-After-Write Expectations](079-consistency-and-read-after-write-expectations.md).

Retrieve the full synchronous call graph and asynchronous delivery graph; client, SDK, proxy, mesh, gateway, load-balancer, driver, broker, workflow-engine, and application retry settings; fan-out cardinality/concurrency; timeouts and cancellation; idempotency/effect identity; queues and executor pools; fallback/failover paths; cache hit ratios; health/ejection/autoscaling policies; per-tenant and priority controls; dependency capacity and quotas; regional recovery plans; and telemetry that distinguishes logical operations, branches, attempts, effects, and useful completions.

## Learning Objectives

After completing this module, you can:

1. distinguish logical operations, branches, attempts, retries, hedges, redeliveries, fallbacks, and effects;
2. calculate conservative call-graph amplification bounds and identify hidden attempt owners;
3. propagate deadlines, stable identity, causation, criticality, and conserved work budgets;
4. assign exactly one retry owner per logical boundary and coordinate mesh, SDK, and application behavior;
5. bound fan-out cardinality, concurrency, optional work, and orphan execution;
6. preserve downstream admission authority, tenant fairness, and goodput under overload;
7. design safe hedging, fallback, cache-loss, message-redelivery, and regional-failover behavior;
8. align circuits, bulkheads, load shedding, backpressure, and health controls to failure domains;
9. measure amplification, first-attempt health, wasted work, and recovery behavior directly; and
10. verify the graph beyond its breaking point with fault, load, replay, cancellation, and recovery tests.

## Core Exposition

### Define the unit before counting it

Start with one caller-visible logical operation: “place order,” “render page,” or “apply event.” Give it a stable operation ID, effect/idempotency identity where mutation is possible, absolute deadline, authenticated tenant, server-assigned priority, and causation ID. These survive internal retries and transport changes.

A branch represents distinct subwork: price, inventory, shipping, or fraud. An attempt is one execution of that branch. A retry starts after a failure or qualifying response. A hedge overlaps an outstanding slow attempt. Redelivery repeats a message that may already have caused work. A fallback invokes a cheaper or alternate implementation. Counting only HTTP requests erases these semantic distinctions.

Separate attempted work from committed effect. Ten attempts can safely converge on one effect only if idempotency and fencing cover the side effect. Conversely, one request can create thousands of effects through unbounded bulk input or fan-out. Both axes need bounds.

Inventory every place that can create work: browser/mobile client, generated SDK, gateway, service mesh, load balancer, application library, orchestration engine, database driver, broker, consumer framework, and recovery tool. Transparent behavior is still real load.

### Model amplification through the graph

At layer $l$, let maximum fan-out be $F_l$ and maximum total attempts per branch be $A_l$, including the original. Then deepest-layer attempts are bounded by $N_d=\prod(F_lA_l)$. For unequal branches, use a recursive cost instead: $C(v)=c_v+\sum_{u\in children(v)}A_{vu}C(u)$, with optional branches admitted only while budget remains.

This arithmetic is conservative. Short-circuiting, failed parents, and cancellation may reduce actual calls; simultaneous hedges, orphan work, and retrying hidden transports can raise concurrent resource use beyond what a sequential count suggests. Measure both total attempts and peak in-flight cost.

Local safety does not imply global safety. “At most three attempts” at each of three layers yields $3^3=27$ deepest attempts, not three. A fleet of 200 clients each holding 20 private retry tokens can still offer 4,000 retries at once. Budgets need an aggregation scope that matches the dependency's failure domain.

### Make work budgets conserved context

Propagate one absolute deadline rather than resetting a relative timeout at each hop. Also propagate operation/causation ID, attempt/branch metadata, trusted criticality, and a budget expressed in units meaningful enough to protect the system: attempt tokens, branch tokens, concurrency permits, estimated CPU/IO cost, result bytes, or a combination.

A child may subdivide a parent's remaining budget but cannot increase it. Required subwork reserves capacity first; optional enrichment, prefetch, hedges, and retries spend only the remainder. Reject requests whose minimum safe work cannot fit. Do not let an internal service upgrade criticality or replenish tokens because it “really needs” the result.

Budget propagation is not permission to trust arbitrary public headers. Authenticate the caller, overwrite untrusted priority, integrity-protect internal context, cap every value, and validate tenant and operation scope. Admission is always local too: a token authorizes at most an attempt; it does not prove current downstream capacity.

### Give the smaller dependency control

Large upstream fleets cannot infer the moment-to-moment capacity of a smaller dependency from their own health. Scale inversion is dangerous: thousands of callers can each behave reasonably and collectively overwhelm one control-plane or storage service. The dependency closest to the bottleneck must decide admission using local utilization, queue, concurrency, quota, and failure-domain state.

Reject excess work early and cheaply before expensive authentication extensions, deserialization, allocation, database access, or fan-out where security permits. Return a stable overload/pushback signal that distinguishes permanent invalidity from temporary capacity. Upstream clients honor “do not retry” and retry-after guidance, then apply jitter and their shared budget.

Client-side adaptive throttling can prevent even cheap rejections from consuming all server capacity. It complements rather than replaces server admission. Per-tenant quotas and server-assigned criticality stop one client or hostile tenant from converting expensive failures into everybody's outage.

### Assign one retry owner

For each logical boundary, document whether the caller, SDK, mesh, application, workflow, or broker owns retries. Disable or constrain the others. The owner knows semantic safety, original deadline, error classification, effect identity, and remaining graph budget; a transparent intermediary often lacks several of these.

Retry only evidence of transience, only while the operation remains useful, and only when another attempt can fit the original deadline. Use capped exponential backoff with jitter and honor server pushback. Preserve operation and idempotency identity. Spend from a dependency-scoped retry budget that shrinks as failures rise.

Never count a success after retry as an ordinary first-attempt success. Record initial failure, attempts, added latency, and recovered outcome separately. A high eventual-success rate can coexist with a dependency entering collapse.

### Hedge as a scarce speculative attempt

A hedge is a retry begun before the first attempt fails. It can reduce tail latency when latency variance is independent and spare capacity exists, but an immediate duplicate doubles load and correlated endpoints do not provide diversity. Delay the hedge using a measured tail threshold, choose a genuinely different eligible failure domain, and cap total attempts.

Only hedge operations whose effects are safe under duplication. The overall deadline governs the whole hedge group. On a winning response, cancel losers and propagate cancellation; if the remote side cannot stop, count that orphan work. Suppress hedging when the dependency signals overload, the retry/hedge token pool is depleted, or correlation means the extra attempt is unlikely to help.

The gRPC hedging guide reflects these mechanics: per-method maximum attempts and delay, one overall deadline, cancellation of outstanding calls, throttling, and server pushback. Those product controls still require application-level semantic and capacity review.

### Bound fan-out and tail coupling

Validate request cardinality before expansion. Put hard limits on items, shards, graph depth, recursion, pages, and resolver cost. Then cap concurrent branches with per-destination executors/semaphores and bounded queues. A cardinality bound without a concurrency bound can still create a destructive burst.

Distinguish required all-of, quorum, first-success, and optional branches. Cancel irrelevant work when quorum or first-success completes. Do not wait for optional recommendations after the response deadline reserve is gone. Partial results and degradation should remove work, not add another unbounded discovery path.

Budget estimates must reflect heterogeneous cost. Ten cache hits do not equal ten scans. Track predicted cost at admission and actual cost for learning, with conservative unknown-cost defaults. Restrict attacker-controlled query shapes and tenant fan-out so denial-of-wallet and denial-of-service cannot masquerade as normal API use.

### Propagate cancellation and contain orphan work

A timeout means the caller stopped waiting; it does not prove the server stopped. Cancellation must flow through request context, executors, drivers, and streaming loops. Check it before new subwork and at safe interruption points. Bound non-cancelable sections and make late completions harmless through stable effect identity.

Measure orphan rate and orphan resource time. If 30% of 10,000 attempts per second time out and 80% of their remote work continues, 2,400 attempts per second continue without a listener. Increasing the timeout might hide the symptom while making concurrency worse; fix admission, cancellation, and the slow dependency.

When cancellation races with commit, return/query an unknown outcome rather than retry with a new identity. For read-only work, discard late results. For mutations, idempotency, fencing, and outcome lookup determine whether the effect already happened.

### Design fallbacks that subtract work

A fallback is safe during overload only if it is simpler, bounded, and independently capacitated. Serving a local stale snapshot or omitting optional fields usually subtracts work. Calling a secondary region, recomputing a cache entry, or querying an alternate provider may add work and transfer the outage.

Give fallbacks their own bulkhead and admission limit, share the original deadline/effect identity, and prevent recursive fallback loops. Know the failover capacity before sending traffic: if the primary carries 10,000 requests per second and the fallback can handle 4,000, shed or degrade at least 6,000 rather than hoping autoscaling arrives.

Fallback correctness still matters. A stale authorization decision, duplicate payment, or inconsistent write may be worse than explicit failure. The degradation contract from API-078 decides what can be omitted, approximated, queued, or refused.

### Prepare for cache-loss amplification

A capacity cache is part of the origin's capacity model. With hit ratio $h$, total request rate $R$, and approximately one origin access per miss, ordinary origin rate is $R(1-h)$. Total cache loss sends roughly $R$, an amplification of $1/(1-h)$. At 95% hits, that is twentyfold.

Protect the origin with admission and reserved headroom, staggered TTLs, request coalescing, negative caching where correct, stale-while-revalidate, bounded refresh concurrency, and gradual cache warming. Do not let every miss retry or refresh independently. Separate correctness caches from capacity caches and test cold-start, eviction, key skew, and invalidation storms.

Recovery can be as dangerous as failure. If all instances restart empty and receive full traffic, the origin may never recover. Warm representative data, ramp traffic, and hold optional refreshes until origin goodput and tail latency stabilize.

### Bound asynchronous amplification

Message systems add publishers, broker delivery, consumers, downstream calls, dead-letter queues, and redrive tools. Publisher retries can duplicate records; broker redelivery can repeat them; consumer libraries can retry each delivery; a handler can fan out again. Preserve one event/effect ID across all of them.

Bound delivery attempts, event age, consumer attempts, handler fan-out, and redrive rate. Use idempotent consumers and transactional effect recording where required. A negative acknowledgment/requeue is another attempt, not a free pause. Poison events go to a quarantined dead-letter workflow rather than a hot requeue loop.

Redrive is production load. Admit it below live traffic, pace it by downstream capacity, and stop when failure/amplification rises. Monitor unique effects, deliveries, handler attempts, duplicate suppressions, and committed effects separately.

### Align containment mechanisms

Bulkheads isolate concurrency by destination, operation, tenant, and priority so one slow dependency cannot occupy every worker. Circuits should be scoped to the actual failure domain—endpoint, shard, zone, region, or operation—without routing all probes to the same survivor. Load shedding rejects excess new work; backpressure communicates sustainable pace; bounded queues prevent time from becoming hidden concurrency.

Decorator order is architecture, not syntax. A typical outbound sequence admits the logical operation, checks the dependency bulkhead/circuit, obtains an attempt token, performs one deadline-bounded attempt, classifies the result, releases resources, and lets the single retry owner decide whether another attempt is useful. Metrics surround all attempts so rejection is visible.

Health checks must not amplify overload. A slow replica ejected from serving may reduce capacity and overload survivors; restart loops spend warm-up capacity; active probes can become traffic. Separate liveness from readiness, protect control traffic, use hysteresis and minimum healthy capacity, and degrade before mass ejection where safe.

### Treat failover as load transfer

Failover does not create capacity. Confirm the target has data authority, consistency semantics, dependency capacity, warm caches, connection limits, quotas, and network paths for transferred work. Apply the same retry and fan-out budgets across regions; a regional error must not authorize every layer to try every region.

Avoid cyclic routing and concurrent ownership. Fence mutations, keep operation identity stable, and specify whether a cross-region attempt is a retry of the same effect. If the surviving region cannot carry the load, prioritize and shed. Failback waits for data/caches/capacity, then ramps gradually.

Control planes are often smaller than data planes. Keep the data plane able to serve last-known valid configuration when safe, and use pull, streaming updates, leases, or staged distribution so millions of workers do not poll a recovering control plane simultaneously.

### Observe amplification and goodput

Count admitted logical operations $L$, branches, total downstream attempts $D$, retries, hedges, fallback calls, deliveries, committed effects, cancellations, orphan work, rejections, and useful completions. A simple operation-level amplification ratio is

$$
\alpha=\frac{D}{L},
$$

segmented by route, dependency, tenant, priority, error class, topology, and software/config version. Report distributions because one expensive route can hide behind a fleet average.

Trace operation/causation ID, branch ID, attempt number/type, retry owner, remaining deadline/budget, chosen failure domain, and cancellation outcome. Do not log secrets or raw tenant-controlled metadata. Derive deepest-layer and cost-weighted amplification as well as raw request counts.

Graph offered load, admitted load, goodput, first-attempt success/latency, eventual success, retry recovery, shed load, queue/concurrency, and dependency saturation together. A falling error rate caused by rejecting most traffic early is not recovery; a high eventual-success rate with collapsing first attempts is not health.

### Change and recover safely

Timeout, retry, hedge, fan-out, connection-pool, health, circuit, cache, and failover configuration changes alter the stability boundary. Treat them like production code: review ownership, canary by dependency/failure domain, compare amplification and goodput, and retain a rapid rollback or server-side kill switch.

During an incident, stop optional/batch/redrive work, suppress retries/hedges, shed aggressively enough for goodput to recover, and fix the trigger. Add capacity only if it becomes usable without multiplying cold starts or control-plane pressure. Once stable, restore traffic gradually with jitter so caches and connections warm.

Do not declare recovery at the first green health check. Require bounded queue age, first-attempt health, amplification near baseline, orphan work drained, cache warmth, and stable goodput under a controlled ramp.

### Verify beyond the breaking point

Load testing must cross the capacity knee and show that accepted-request latency and useful completions remain bounded while excess work is rejected cheaply. Measure how much rejection itself costs. Exercise varied query cost, fan-out sizes, tenant skew, cache hit ratios, and client fleet sizes rather than one homogeneous QPS target.

Inject abrupt failure, slow responses, partial endpoint/shard loss, broker redelivery, cache loss, region loss, health flapping, hidden SDK/mesh retries, cancellation failure, fallback loss, and recovery. Combine faults: dependency slowdown plus autoscaling clients, cache cold start plus redrive, or region loss plus a rollout.

Prove invariants from traces and counters: attempts/effects stay within budget; only the designated owner retries; descendants never outlive deadline beyond a bounded cancellation interval; optional work falls as overload rises; tenants remain isolated; target capacity governs failover/redrive; goodput does not collapse before the tested safety envelope; and recovery does not create a second surge.

## Definitions and Notation

Let $L$ be admitted logical operations in a window, $F_l$ maximum fan-out at layer $l$, $A_l$ maximum total attempts per branch, $N_d$ deepest-layer attempts, $D$ observed downstream attempts, and $\alpha=D/L$ the raw amplification ratio. Let $c_v$ be local cost at graph node $v$ and $C(v)$ its recursive maximum cost.

Let $B$ be remaining end-to-end time budget, $K$ remaining cost/attempt tokens, $Q$ queue capacity, $I$ in-flight work, $G$ useful completion rate (goodput), $R$ total cache-fronted request rate, and $h$ cache hit ratio. Ordinary origin load is approximately $R(1-h)$; complete cache loss multiplies it by $1/(1-h)$ relative to that baseline.

A **retry budget** limits additional sequential attempts across an aggregation scope. A **hedge budget** limits speculative concurrent attempts and should share dependency capacity accounting. **Pushback** is downstream guidance to delay or suppress attempts. A **capacity cache** is required to keep origin load within capacity, not merely to improve latency. **Scale inversion** occurs when a much larger caller fleet drives a smaller dependency. **Goodput** counts useful work completed within its contract, not merely accepted attempts.

## Mechanisms, Invariants, or Proof Structure

**Multiplication argument.** If every branch at layer $l$ may independently create $F_l$ children and each child may receive $A_l$ attempts, induction gives $N_d=\prod_{l=1}^{d}(F_lA_l)$. Independence is a worst-case assumption; it proves why per-layer limits are insufficient, not that every operation realizes the bound.

**Conservation argument.** Suppose a parent admits remaining token budget $K$. If it allocates nonnegative child budgets $K_i$ with local spend $k_0+\sum K_i\le K$, and every child obeys the same rule, total descendant spend cannot exceed the root budget. This holds only if all attempt creators participate, units are not silently reset, and admission rejects work whose minimum cost cannot fit.

**Overload feedback.** A slowdown raises latency and in-flight work; deadline expiry wastes completed or continuing work; retries/hedges add offered load; added load raises queues and latency. Early shedding, cancellation, and bounded additional attempts break edges in that positive-feedback loop. Backoff alone spreads load in time but cannot make an overloaded dependency capable.

**Cache-loss derivation.** With hit ratio $h$, baseline origin load is $R(1-h)$. Cache loss produces $R$, so relative amplification is $R/[R(1-h)]=1/(1-h)$ for $h<1$. This simplified model excludes request coalescing, partial hits, fill cost, and different origin costs; those require measurement.

Operational invariants are: one operation identity and absolute deadline; one retry owner per boundary; no hidden uncounted attempts; conserved branch/attempt/cost budget; local downstream admission; bounded fan-out/concurrency/queues; propagated cancellation; one effect under duplicate execution; isolated tenants/failure domains; simpler bounded fallback; and gradual evidence-driven recovery.

## Alternatives and Trade-Offs

Retrying at the top preserves semantic context and avoids multiplication, but may repeat more high-level work. Retrying near the dependency can be efficient and hide a brief connection fault, but lacks business semantics. Choose one owner and expose enough result detail for it to decide.

Static attempt limits are simple but ignore current health and fleet size. Ratio- or token-based retry budgets adapt to successful traffic and contain storms, yet distributed enforcement can lag. Combine hard per-operation caps with dependency/fleet budgets and server pushback.

Hedging reduces tails without waiting for failure, at the price of concurrent duplicate work. Delayed hedges to diverse endpoints with cancellation and throttling can be worthwhile for safe reads; under correlated overload or expensive writes they are harmful.

Central global admission can coordinate capacity but adds latency, state, and a failure dependency. Local downstream admission reacts quickly and remains authoritative but can be unfair without tenant/priority policy. Hierarchical quotas and local protection usually compose better than either alone.

Fail-fast errors preserve goodput but reduce headline availability. Long queues may absorb small bursts but hide latency and consume memory; large queues turn overload into timeout and orphan work. Bounded queues with explicit backpressure make the trade visible.

Warm standby/failover capacity costs money. Depending on autoscaling is cheaper but often too slow for an abrupt transfer and can stress control planes. Degraded modes and priority shedding can reduce required reserve if the product contract explicitly permits them.

## Failure Modes and Misconceptions

- “Three retries means three attempts.” Three retries normally means four total attempts; configure and measure the same unit.
- “Each layer retries only a little.” Products of small local limits can be enormous.
- “The mesh handles resilience.” Transparent retries still need semantic safety, deadline, identity, and a single owner.
- “Backoff solves overload.” It desynchronizes attempts but does not add capacity or remove useless work.
- “A token means the dependency must accept.” Local admission remains authoritative.
- “Hedges are free when the loser is canceled.” Cancellation can arrive after expensive or committed work.
- “Different endpoints mean independent failures.” Same shard, zone, database, or control plane can correlate them.
- “A timeout stopped the request.” It stopped waiting unless cancellation is propagated and honored.
- “Fallback improves availability.” An unbounded alternate dependency can amplify and spread failure.
- “Failover restores capacity.” It transfers load to capacity that must already exist or shed it.
- “Circuit opening removes load.” Repeated probes, fallback, rerouting, and retries can move or multiply it.
- “Eject every unhealthy instance.” Overload-induced health failure can shrink capacity and overload survivors.
- “Cache is only an optimization.” A high-hit capacity cache can be part of the origin's survival envelope.
- “Redelivery is not retry.” It repeats handler and downstream work and must share effect identity/bounds.
- “Eventual success proves health.” Retries can hide first-attempt collapse and burn the remaining capacity.
- “Autoscaling will catch up.” Startup, caches, connections, quotas, and control planes can delay usable capacity.
- “Critical traffic can declare itself.” Publicly controlled priority lets an attacker bypass shedding.
- “Recovery means remove all throttles.” A synchronized release can recreate the incident.

## Worked Examples

### Example 1

Three layers each fan out to four branches and allow three total attempts per branch. The deepest bound is $(4\times3)^3=12^3=1{,}728$ attempts from one operation. The team replaces independent limits with a 20-token root budget, reserves required branches, and drops optional work that cannot fit.

### Example 2

An application, service, and database adapter each allow three total attempts. One top-level branch can cause $3^3=27$ database attempts. The application becomes retry owner; inner layers use one attempt except for a narrowly classified pre-send connection failure charged to the same budget.

### Example 3

An endpoint admits 1,000 logical requests per second, fans out to ten branches, and permits two attempts per branch. Worst-case downstream offer is $1{,}000\times10\times2=20{,}000$ attempts per second. A 12,000-attempt dependency limit requires lower fan-out, fewer attempts, degradation, or shedding before expansion.

### Example 4

A cache fronts 20,000 requests per second with a 95% hit ratio, so the origin normally sees $20{,}000(1-0.95)=1{,}000$ requests per second. Total cache loss sends 20,000—twenty times baseline. Origin admission, coalescing, stale serving, and gradual warming activate before the cache fleet restarts.

### Example 5

There are 5,000 one-branch logical operations per second and 500 retry attempts. Downstream attempts are 5,500, so $\alpha=5{,}500/5{,}000=1.1$ and the retry ratio is 10%. If first-attempt success falls while eventual success stays flat, the retry layer is masking deterioration.

### Example 6

At 10,000 attempts per second, 30% time out and 80% of timed-out remote work ignores cancellation. Orphan rate is $10{,}000\times0.30\times0.80=2{,}400$ attempts per second. The team fixes driver cancellation and admission rather than extending every timeout.

### Example 7

A primary region carried 10,000 requests per second; the surviving fallback region has 4,000 spare. Immediate full failover overloads it by 6,000. The gateway preserves top-priority operations up to admitted capacity, serves a cheaper mode where correct, and sheds the remainder while capacity warms.

### Example 8

Two hundred client instances each have 20 local retry tokens, exposing a synchronized allowance of 4,000 retries. A dependency-scoped shared budget and server pushback cap aggregate retries; small local buckets remain only to prevent one process from bursting its share.

### Example 9

A publisher allows two attempts, the broker delivers up to five times, and a consumer's provider call allows three attempts. One event can produce $2\times5\times3=30$ provider attempts. Stable event/effect identity, idempotent consumption, bounded age, and one paced redrive path prevent 30 committed effects.

### Example 10

One hundred recovering instances each launch five immediate health or cache-warm probes, producing 500 concurrent requests to a dependency that just restarted. Randomized ramp, readiness gates, and a fleet probe budget reduce the burst while first-attempt latency and goodput confirm recovery.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies failure models, partial failure, idempotency, replication, causality, and feedback analysis.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects stocks, flows, positive feedback, control stability, capacity constraints, and emergent risk.

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) governs call-graph boundaries, ownership, dependency direction, orchestration, and fallback composition.

[Network Engineering](../../24-network-engineering/ROADMAP.md) explains timeouts, connection pools, load balancing, topology correlation, cancellation limits, and regional routing.

[Security Engineering](../../25-security-engineering/ROADMAP.md) covers tenant isolation, authenticated priority, adversarial expensive requests, replay, and effect integrity.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns standard deadline/budget propagation, mesh and SDK retry defaults, admission controls, telemetry, canaries, and emergency kill switches.

## References

1. Google, [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/).
2. Google, [Handling Overload](https://sre.google/sre-book/handling-overload/).
3. Amazon Web Services, [Timeouts, Retries, and Backoff with Jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter).
4. Amazon Web Services, [Using Load Shedding to Avoid Overload](https://builder.aws.com/content/3Eun1EEyX6p2e3VYNyRLSJzLuMV/using-load-shedding-to-avoid-overload).
5. Amazon Web Services, [Avoiding Overload in Distributed Systems by Putting the Smaller Service in Control](https://d1.awsstatic.com/builderslibrary/pdfs/Avoiding%20overload%20in%20distributed%20systems%20by%20putting%20the%20smaller%20service%20in%20control-Joe%20Magerramov.pdf).
6. Envoy Project, [Circuit Breaking](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking).
7. gRPC Authors, [Request Hedging](https://grpc.io/docs/guides/request-hedging/).

## Exercises

### Exercise 1

An API fans out through three layers with $(F_1,A_1)=(5,2)$, $(F_2,A_2)=(3,3)$, and $(F_3,A_3)=(2,2)$. Compute the deepest bound and design a conserved budget that admits required work without treating that bound as acceptable capacity.

### Exercise 2

Audit a path where a mobile SDK, gateway, mesh, application, database driver, broker, and consumer can all repeat work. Assign retry ownership, identity, deadline, pushback, attempt accounting, cancellation, and effect protection.

### Exercise 3

A service receives 8,000 logical requests per second, normally fans out to four branches, has 25% retries during a fault, and loses a cache that normally absorbs 90% of one branch's origin calls. Estimate relevant amplification and define admission/degradation actions.

### Exercise 4

Design a hedging policy for an idempotent read with correlated zones, a 300 ms end-to-end deadline, and rising server overload. Cover delay, diversity, total attempts, cancellation, throttling, pushback, metrics, and suppression.

### Exercise 5

Create a fault/load/recovery verification plan for multi-tenant regional services with caches, fan-out, health ejection, failover, asynchronous redelivery, fallbacks, and hidden retries. State invariants and evidence required before removing incident throttles.

## Answers to the Exercises

### Answer 1

The deepest bound is $(5\times2)(3\times3)(2\times2)=10\times9\times4=360$ attempts per admitted operation. That is a hazard bound, not a provisioning goal. Classify mandatory branches and their worst safe cost, remove redundant expansion, cap concurrency per dependency, and give the root a finite cost budget based on tested capacity—perhaps far below 360. Each layer reserves mandatory work and subdivides remaining tokens; optional branches and extra attempts are skipped when they cannot fit. The dependency still performs local admission, and traces prove that every SDK/proxy/application attempt spends a token.

### Answer 2

Map the logical operation and effect ID end to end. Prefer the application/workflow as retry owner because it knows semantics; configure SDK, gateway, mesh, and driver to one attempt except explicitly reviewed pre-send transport recovery charged to the same budget. Preserve one absolute deadline and idempotency identity. The database driver propagates cancellation; uncertain commit uses outcome lookup rather than a new effect. Publisher retry preserves event ID; broker delivery count and consumer attempt consume bounded age/attempt budgets; the consumer records effects idempotently. Every layer honors permanent errors and downstream do-not-retry/retry-after signals. Telemetry records branch/attempt owner and exposes any hidden repeats.

### Answer 3

Normal branch offer is $8{,}000\times4=32{,}000$ attempts per second before retries. If 25% means 0.25 additional attempts per original branch, total becomes $32{,}000\times1.25=40{,}000$. For the cache-fronted branch, 90% hits mean 800 origin calls per second normally; full loss creates 8,000, a tenfold origin amplification and 7,200 additional origin calls. Do not merely accept 40,000 plus the miss storm. Shed before fan-out, omit optional branches, cap concurrency, suppress retries under overload, coalesce fills, serve safe stale data, reserve origin capacity, prioritize tenants, and warm/ramp the cache. Validate actual cost because branch and miss costs may differ.

### Answer 4

Use one original attempt and at most one delayed hedge only after a measured high-tail threshold that leaves execution and response reserve inside 300 ms. Choose an endpoint in a genuinely independent eligible failure domain, not merely another address backed by the same shard. Both attempts share operation ID, deadline, and dependency hedge/retry budget. Cancel the loser and measure whether remote work stopped. Honor negative or delayed server pushback and gRPC-style throttling. Suppress hedges when overload, correlated latency, insufficient diversity, low remaining deadline, or depleted tokens makes them harmful. Compare first-attempt tail, eventual latency, added attempts, orphan cost, and dependency goodput in canaries.

### Answer 5

Establish baselines for logical operations, cost-weighted amplification, first-attempt/effect success, goodput, queue/concurrency, cache origin load, tenant fairness, and orphan work. Drive beyond the capacity knee; inject slow/failed shards, cache loss, health flapping/ejection, hidden SDK/mesh retry, cancellation loss, fallback failure, region loss, broker redelivery, poison events, and paced/unpaced recovery in combinations. Assert one retry owner, bounded attempts/effects/age, conserved budgets, local admission, tenant isolation, optional-work reduction, no recursive fallback, target-capacity-limited failover, and idempotent redelivery. Keep throttles until queues and orphans drain, caches warm, first-attempt health and goodput stabilize, amplification returns near baseline, consistency/fencing checks pass, and a randomized staged ramp causes no second surge.
