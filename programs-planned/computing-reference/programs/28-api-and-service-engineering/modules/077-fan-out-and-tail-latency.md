---
module_id: API-077
program: API & Service Engineering
level: 2
module_number: 77
title: Fan-Out and Tail Latency
status: complete
last_verified: 2026-09-02
---

# Fan-Out and Tail Latency

## One-Page Review

### Governing question

When one API operation expands into many branches, how should it bound branch count, concurrency, deadlines, completion criteria, cancellation, and duplicate attempts so tail latency and load remain predictable?

### Essential definitions

- **fan-out** expands one logical operation into multiple downstream branches; **fan-in** combines their outcomes.
- **tail latency** is latency in a high percentile or beyond a usefulness threshold, not the mean.
- A **straggler** is a branch whose completion is materially later than its peers.
- The **critical path** is the dependency sequence/order statistic that determines end-to-end completion.
- **all-of** completion requires every required branch; **quorum** requires a defined subset; **best-effort** permits omissions under an explicit contract.
- A **hedged request** starts an additional equivalent attempt before the first attempt fails and uses an acceptable first result.
- A **branch budget** bounds branch count, concurrent attempts, cost, retries/hedges, and deadline.
- **orphan work** continues after the parent can no longer use its result.

### Central model, mechanism, or theorem

For $n$ independent identically distributed branch latencies with cumulative distribution $F(t)$, all-of completion time $M_n=\max(X_1,\ldots,X_n)$ satisfies

$$
P(M_n\le t)=F(t)^n.
$$

If one branch exceeds $t$ with probability $p$, the request exceeds $t$ with probability $1-(1-p)^n$. Independence is an estimate, not a safety proof: shared queues, hosts, regions, deployments, data skew, and overload correlate tails. End-to-end control therefore needs both order-statistic analysis and correlated fault/load tests.

### Critical invariants

Every parent has one absolute deadline and bounded fan-out, concurrency, bytes, cost, retry, and hedge attempts. Child deadlines preserve time for scheduling, aggregation, serialization, and response. Required, optional, quorum, and substitutable branches are defined before execution; success criteria do not change opportunistically.

Cancellation propagates promptly and losers release permits, connections, CPU, and downstream work where possible. Retried/hedged effects are idempotent or read-only under stable operation identity. Hedging is delayed, load-budgeted, topology-diverse, and suppressed during overload. Metrics distinguish logical operations, branches, attempts, winners, losers, cancelled work, and completed-after-cancel work.

### Common failures

Measure only means; assume branch independence; launch unbounded work from list size; make every optional enrichment required; give each child the parent timeout; serialize “parallel” futures while awaiting; hide executor/connection queues; retry every slow branch; hedge immediately; send duplicates to the same failed host; treat cancellation as proof work stopped; let losers commit effects; use fastest response without consistency/version checks; quorum ignores membership/authority; merge waits after deadline; one hot shard dominates; and aggregate success hides branch tail and orphan load.

### Compact example

Each branch independently has a 1% chance of exceeding 200 ms. One branch meets 200 ms 99% of the time, but an all-of request over 100 branches meets it with probability $0.99^{100}\approx36.6\%$; about 63.4% exceed 200 ms. Reducing the per-branch tail, reducing required fan-out, or using a semantically valid quorum/partial result changes the end-to-end outcome. **Conclusion:** large all-of fan-out converts rare branch slowness into normal request slowness.

### Connections

[Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), [Retries and Backoff](072-retries-and-backoff.md), [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), [API-Level Load Shedding](074-api-level-load-shedding.md), and [Backpressure Across Service Boundaries](075-backpressure-across-service-boundaries.md) bound time and attempts. The next module formalizes partial/degraded responses.

## Governing Question

For each scatter/gather API, what branch set and completion rule are semantically necessary, what order statistic drives latency, and how will budgets, scheduling, cancellation, and topology prevent tail mitigation from becoming load amplification?

## Why This Matters

A request that consults one backend sees one latency distribution. A request that waits for 100 shards sees the maximum of 100 distributions. A rare 1% slow event becomes likely somewhere in the fan-out. Google Research's *The Tail at Scale* describes how temporary high-latency episodes that are minor at small scale dominate large interactive systems and surveys tail-tolerant techniques.

Fan-out is common: search shards, authorization plus profile plus inventory, replica reads, microservice aggregation, batch APIs, GraphQL fields, storage erasure sets, analytics partitions, and multi-region queries. It increases parallelism and coverage, but also multiplies attempts, connections, queue entries, logs, retries, and failure opportunities.

Tail latency is not only a probability problem. Branches share failure domains: a garbage collector pauses a process, a hot key targets one shard, a deployment affects every replica, a regional network slows, or overload lengthens all queues. Independent formulas help intuition; capacity and fault tests must include correlation.

Mitigations have costs. Higher concurrency can reduce wall time while increasing queueing. Hedging can outrun a straggler while duplicating work at the worst time. Quorum can lower latency but weaken completeness or consistency. Cancellation may arrive after a write commits. The API contract and resource model must constrain every technique.

## Prerequisites and Retrieval

Retrieve [Long-Running Operations](018-long-running-operations.md), [Bulk and Batch Operations](019-bulk-and-batch-operations.md), [Unary and Streaming gRPC](053-unary-and-streaming-grpc.md), [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), [Retries and Backoff](072-retries-and-backoff.md), [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), [API-Level Load Shedding](074-api-level-load-shedding.md), and [Backpressure Across Service Boundaries](075-backpressure-across-service-boundaries.md).

Retrieve the logical dependency graph; branch cardinality/cost/size distributions; required/optional/quorum semantics; per-branch and end-to-end latency distributions; correlations by host/shard/zone/region/version/tenant; queues and connection pools; deadline/cancellation propagation; retry/hedge/library/mesh policies; idempotency and consistency/replica rules; load-balancer topology; capacity under duplicate work; and traces for branch attempts and orphan completion.

## Learning Objectives

After completing this module, you can:

1. derive all-of and quorum tail behavior from branch latency distributions;
2. identify correlation and hidden queues that invalidate independent models;
3. bound branch cardinality, concurrency, cost, bytes, retries, and hedges;
4. allocate one end-to-end deadline across scheduling, execution, aggregation, and response;
5. define required, optional, quorum, and early-termination semantics;
6. propagate cancellation and account for work that cannot be stopped;
7. use delayed hedging only for safe operations under aggregate load budgets;
8. choose topology-diverse attempts without violating consistency or affinity;
9. observe critical paths, branch/attempt tails, wasted work, and user outcomes; and
10. verify tail controls under independent, correlated, overload, and recovery scenarios.

## Core Exposition

### Model the completion rule first

List branches and classify each as required, optional, substitutable, or conditional. Define success before implementation: all required branches, any one replica, $k$ of $n$, one per failure domain, a ranked top-$K$, or a base response plus bounded enrichments. A vague “best effort” creates unstable client semantics.

All-of latency is the maximum required branch completion plus scheduling/merge/response. Any-one latency is the minimum acceptable result, subject to correctness. A $k$-of-$n$ quorum uses the $k$th order statistic, but quorum membership and version/authority rules matter more than speed.

Do not wait for branches that cannot change the result. A top-$K$ search can terminate a shard only when remaining scores have a proven upper bound below the current cutoff. Majority voting can finish once no remaining votes can alter the decision. Early exit requires a correctness proof.

The next module covers response representation for missing components. Here the essential point is that completion policy is an API contract, not a timeout accident.

### Quantify order-statistic amplification

If branches are independent and each completes by $t$ with probability $q=F(t)$, all $n$ complete with $q^n$. At $q=0.99$ and $n=100$, $q^n\approx0.366$. At $n=10$, it is about $0.904$. Reducing required branches can matter as much as improving one percentile.

For non-identical independent branches, $P(M\le t)=\prod_iF_i(t)$. A single slow distribution can dominate. For a quorum, sum probabilities for at least $k$ completions (binomial only under identical independence). In production use traces/simulation for heterogeneous and correlated distributions.

Percentiles do not compose by addition. The sum of component p99s is not the request p99; parallel paths use maxima and sequential paths use sums with joint dependence. Histogram aggregation can also hide per-tenant/shard tails. Preserve distributions and trace critical paths.

Independence often understates risk. Perfectly correlated branches all slow together; their probability of any slow branch may equal the per-event probability rather than the independent union, but incident severity and inability to hedge are greater. Mixed common-mode plus idiosyncratic tails needs scenario modeling.

### Bound cardinality before launching

Never map an untrusted or unbounded list directly to asynchronous calls. Apply maximum items, pagination, query complexity, cost units, bytes, tenant quota, and deadline feasibility before scatter. Large work becomes a long-running/asynchronous job with explicit lifecycle.

Fan-out factor can change with data. A cache miss, wildcard, graph traversal, tenant with many accounts, or partition split can make nominal 10 become 10,000. Record actual and rejected fan-out; protect downstream with per-operation/tenant limits.

Collapse duplicate branches. Batch compatible requests when downstream supports authoritative per-item results and bounded batch cost. Cache/reuse safe results. Move joins to a service that owns the data when repeated network scatter is an architectural smell.

Bound recursive fan-out. If A calls 20 B instances and each B calls 20 C instances, one request can create 400 C calls before retries. Propagate a branch/cost budget, not merely local concurrency.

### Separate concurrency from total work

A semaphore of $C$ bounds in-flight branches, not total $n$. With service time $S$, $n$ branches run in roughly $\lceil n/C\rceil$ waves plus variability/queueing. Lower $C$ protects capacity but can make deadlines infeasible; higher $C$ can overload pools and worsen every tail.

Choose concurrency from downstream safe capacity, per-parent fairness, fleet amplification, cost, connection pool, and deadline. One parent must not occupy the entire shared bulkhead. Use per-parent cap inside a tenant/operation/destination pool.

Acquire permits deadline-aware. Do not enqueue branches whose estimated wait plus useful execution cannot fit. Release on success, failure, timeout, cancellation, and early completion. Avoid holding parent locks/resources while waiting for branch permits.

Parallel code can accidentally serialize by awaiting each future in creation order. Launch within the bound, consume completions as they arrive, and preserve deterministic output order separately where required.

### Allocate one deadline across the graph

Start with the caller's absolute deadline. Reserve time for admission, scheduling, merge/validation, serialization, network response, and cleanup. Child deadlines are no later than parent minus downstream reserves. Never give every branch a fresh copy of the full timeout.

Parallel branches share wall time but consume different resources. Sequential levels consume deadline additively. For a graph with two sequential fan-out layers, allocate explicit budgets and fail/degrade before launching a layer that cannot complete usefully.

Use per-branch timeouts based on distributions and importance, capped by remaining parent budget. A slow optional branch may have a shorter cutoff than a required branch. Dynamic budgets need floors and stable estimates so short recent samples do not create oscillation.

After the completion criterion is met, stop waiting. Return only after response correctness/metadata is assembled, then propagate cancellation. Track results that arrive during the response reserve without letting them extend the deadline unpredictably.

### Treat queues as part of branch latency

Latency begins before downstream execution: executor, connection pool, load balancer, transport, server admission, and storage queues all contribute. A 50 ms RPC timeout after 200 ms local queue wait cannot meet a 100 ms parent budget.

Measure queue wait separately from service time. Shed before enqueue when remaining time is inadequate. Use small bounded queues and fair scheduling; thousands of parent requests each holding partial fan-out can deadlock resources needed for their remaining branches.

Scatter/gather can create convoying. If every parent holds $C-1$ completed results and waits for one branch in a saturated shared pool, memory and upstream resources grow. Stream/aggregate incrementally and cap concurrent parents as well as branches.

Backpressure from downstream reduces new parent admission. It must not merely fill the aggregator's hidden queue.

### Find and reduce straggler causes

Common causes include queueing at high utilization, CPU scheduling, garbage collection, lock contention, cold cache/JIT, page faults, storage/network variability, load imbalance, hot shards/keys, large requests, noisy neighbors, retries, deployment skew, and failure recovery.

Segment branch latency by endpoint, shard, zone, version, payload/cost, cache state, tenant, and attempt. Avoid unbounded labels. Correct structural causes before adding speculative duplicates: balance load, split hot shards, bound work, isolate queues, prewarm, control GC/memory, and reduce synchronization.

Use percentile targets at branch and parent levels derived from the fan-out model. A branch p99 target may be insufficient for a 100-way all-of operation. Conversely, optimizing every branch p99 at great cost may be wasteful if quorum ignores the slow tail.

Tail behavior changes under utilization. Measure at realistic and overload levels; a policy learned at idle may amplify queues at peak.

### Define quorum and replica semantics

“First response wins” is safe only when replicas are equivalent for the operation. Reads may differ by version, consistency, session, region, authorization, or staleness. Validate result version/freshness and honor read-after-write/session tokens.

$k$-of-$n$ is not automatically a consistency quorum. Membership, overlapping read/write sets, epochs, leader authority, conflict resolution, and failure domains determine correctness. An API-level fastest-two policy cannot invent database quorum semantics.

For replicated reads, prefer one well-chosen attempt before hedging to a distinct eligible replica. Cross-region attempts affect residency, consistency, cost, and capacity. For writes, duplicate attempts need stable effect identity and provider idempotency; cancellation does not roll back a commit.

When branches return conflicting data, do not choose fastest silently. Apply authoritative version/order/reconciliation or fail with explicit inconsistency.

### Propagate cancellation and account for orphans

Cancel children when the caller cancels, parent deadline expires, a fatal required error makes success impossible, or an early completion criterion is reached. Cancellation flows through runtime, transport, executor, and downstream operation where supported.

Cancellation is a request, not proof. Work may already be executing or committed; a library may drop only the response; a server may ignore it. Preserve idempotency/outcome semantics and measure work completed after cancellation.

Remove queued-but-not-started branches and release permits immediately. For running CPU work, check cancellation at bounded points. For database/external calls, use protocol cancellation with separate cleanup deadline, but do not assume rollback.

Loser responses must not mutate shared result after winner selection. Use an atomic parent generation/state; late callbacks release resources and record outcome without overwriting response or double-completing.

### Use hedging as controlled speculation

A hedge launches another equivalent attempt after a delay while the original remains in flight. The first acceptable result wins and losers are cancelled. It differs from a retry because attempts overlap; it can reduce latency for isolated stragglers but increases concurrent load.

Hedge only read-only or strongly idempotent operations with stable identity, replayable body, equivalent eligible endpoints, one parent deadline, and cancellation. Configure delayed rather than immediate duplicates—often near a measured tail threshold—so most fast originals finish without extra work.

Let $H$ be the probability the original is unfinished at hedge delay. With at most one hedge, additional attempts per logical call are approximately $H$ before suppression/cancellation effects. At one million calls/s and $H=0.02$, hedging can add up to about 20,000 attempts/s. Spare capacity must be proved.

Use per-request and fleet/endpoint hedge budgets, tenant fairness, retry throttling, server pushback, circuits, and load shedding. Suppress hedges when overload/latency is common: correlated slowness makes duplicates consume the same constrained resource.

### Choose hedge destinations and results safely

The duplicate should avoid the suspected failure domain: different connection/endpoint/host, perhaps zone, while preserving shard ownership, affinity, consistency, residency, and authorization. A load balancer can otherwise select the same endpoint.

Hedging across replicated storage may read different versions. Define acceptable version and choose the first acceptable result, not first byte. Validate errors: a fast authorization or domain failure should usually terminate rather than be ignored for a slower success.

gRPC documents per-method hedging with maximum attempts, delay, nonfatal status codes, one overall deadline, loser cancellation, throttling, and server pushback. Treat those as product semantics; verify language support and actual configuration.

Hedges and retries share a total attempt budget. Do not hedge each retry or allow mesh, SDK, and application to speculate independently. Count transparent attempts.

### Avoid tied-request and cancellation hazards

Some tail-tolerance designs enqueue duplicate “tied” requests at multiple servers and arrange for one starting copy to cancel the other before execution. Correctness depends on fast cross-cancellation and queue semantics. If both start, load duplicates; if cancellation is lost, both complete.

Do not implement distributed locks merely to choose a hedge winner on the hot path. Use idempotent read/operation semantics and local winner selection, while downstream admission controls duplicate work.

For side effects, a winner response does not mean the loser effect vanished. Stable idempotency key and authoritative outcome merge are mandatory, or hedging is prohibited.

Security checks must be identical on every attempt. Do not hedge to a less trusted region/cache or treat fastest partial authorization as sufficient.

### Handle partial and incremental aggregation

Aggregate as branches finish to reduce memory and expose progress internally. Public partial/streaming results require stable item identity, completeness metadata, ordering, errors, continuation/resume, and a finalization contract—developed in API-078.

For all-of atomic responses, do not emit success until required set validates. For optional fields, distinguish absent-by-design, unavailable, timed out, unauthorized, and not found without leaking security state.

Bound merge CPU/memory and output size. A fan-in sorting one million branch items can dominate tail after every branch completes. Use top-$K$ algorithms, bounded heaps, streaming reductions, or asynchronous jobs.

Preserve deterministic ordering if clients depend on it, but do not wait in input order to process completions. Separate collection from final order.

### Observe logical calls, branches, and attempts

Measure parent latency/outcome/completion rule; requested/launched/completed/cancelled branches; branch queue/service/total distributions; critical path; fan-out and concurrency; deadline remaining; required/optional/quorum outcomes; merge time; result size; and branch errors by scoped cause.

For retries/hedges record logical operation ID, attempt, destination/failure domain, launch reason/delay, winner, loser cancellation latency, completed-after-cancel, duplicate CPU/bytes/effects, suppression, pushback, and token budget.

Report tail percentiles and SLO threshold fractions, not means alone. Avoid averaging percentiles across instances. Correlate parent tails with shard/host/zone/version, utilization, queues, GC, payload, cache, deployment, and incident.

Sample traces without losing slow requests: tail-based sampling is useful, but retain unbiased distributions. Bound labels and protect tenant/request data.

### Verify independent and correlated tails

Replay measured branch distributions and compare parent order statistics. Then inject correlation: one hot shard, one slow host, zone latency, shared database, fleet GC, deployment regression, cache miss storm, connection-pool exhaustion, and global overload.

Vary fan-out cardinality, concurrency, parent arrival rate, payload, required/optional mix, deadline, retries, and hedge delay. Drive beyond capacity and verify speculation suppresses before goodput collapses.

Test cancellation at queue, send, execution, response, and post-commit stages. Confirm permits release once, late callbacks cannot change response, and orphan work is bounded/visible. Test inconsistent replicas and fatal versus nonfatal hedge errors.

Check invariants automatically: no parent exceeds branch/attempt/cost budget; children never outlive useful deadline without explicit cleanup; completion matches declared rule; hedge losers cannot duplicate effects; destination diversity/consistency holds; and offered load returns to baseline after parent cancellation/recovery.

## Definitions and Notation

Let branch latencies be $X_i$ with CDFs $F_i(t)$, required count $n$, all-of latency $M_n=\max_iX_i$, and per-branch probability $p=P(X_i>t)$. Let $C$ be per-parent concurrency, $F$ fan-out factor, $A$ maximum total attempts, $D$ parent deadline, and $R$ response/merge reserve.

Let $H=P(X>d_h)$ be probability an original remains unfinished at hedge delay $d_h$. With one possible hedge, expected/average added attempts are bounded approximately by $H$ per logical call when all eligible calls launch it; correlated suppression and cancellation change realized work. Let $W_o$ be orphan work completed after parent interest ends.

An **order statistic** is a ranked sample value. A **quorum** is a contractually sufficient subset, not merely any fast $k$. **Speculation** spends extra work for latency. **Correlation** means branch latencies/outcomes are not independent.

## Mechanisms, Invariants, or Proof Structure

**All-of amplification.** Under independence, $P(M_n\le t)=\prod_iF_i(t)$; for identical $F$, this is $F(t)^n$. With per-branch exceedance $p$, request exceedance is $1-(1-p)^n$. The proof is not valid under correlation and says nothing about capacity feedback.

**Fan-out load bound.** If at most $P$ parents execute concurrently, each has at most $C$ branches in flight and every branch attempt acquires one shared permit, then parent-originated in-flight branches are at most $PC$ within that governed scope. Hidden retries/hedges or nested fan-out invalidate the bound.

**Hedge-load bound.** For call rate $\lambda$ and eligible unfinished fraction $H$, one hedge adds at most approximately $\lambda H$ attempts/s before fleet suppression. This is a rate estimate; a correlated pause can make instantaneous $H$ near one, so an absolute token/concurrency budget is required.

**Early-completion correctness.** Returning before all branches is correct only if unobserved branches cannot change the declared result or are explicitly optional/omitted. A latency benefit cannot substitute for that semantic proof.

Operational invariants are: bounded fan-out and attempts; one parent deadline; declared completion semantics; deadline-aware permits; prompt cancellation; authoritative winner selection; safe effects; topology eligibility; overload suppression; bounded aggregation; and branch/attempt observability.

## Alternatives and Trade-Offs

All-of preserves completeness but amplifies tails. Quorum/partial/approximate completion lowers latency only when semantics allow. Sequential calls reduce concurrency but add latency; full parallelism minimizes ideal wall time but maximizes instantaneous load; bounded waves balance them.

Reducing branch count through denormalization, indexing, ownership, caching, or precomputation simplifies runtime but increases write/storage complexity. Moving to asynchronous jobs changes interaction latency and lifecycle.

Delayed hedging adds modest average load when tails are rare; immediate duplication doubles load. Retries use less simultaneous capacity but wait for failure. Neither helps correlated overload without spare/diverse capacity.

Static timeouts/concurrency are predictable but drift. Adaptive policies can follow distributions yet oscillate or learn from already-shed traffic. Bound with floors, ceilings, hysteresis, and load tests.

Replica-first selection avoids duplicate work; power-of-two/adaptive balancing needs trustworthy signals. Cross-zone/region diversity improves independence but affects consistency, cost, and residency.

## Failure Modes and Misconceptions

- “Each dependency is p99 under 200 ms, so the parent is p99.” All-of order statistics amplify exceedance.
- “Multiply probabilities always.” Independence may be false; shared causes dominate incidents.
- “Parallel latency is the sum.” Parallel all-of uses a maximum plus overhead; sequential levels add.
- “Concurrency cap bounds total work.” It bounds in-flight work, not cardinality, retries, or duration.
- “The caller timeout covers every child.” Children need reserves and queue time within one deadline.
- “First response is correct.” Replicas may differ by version, authority, region, or error semantics.
- “Quorum means any fast majority.” Correct membership/epoch/intersection rules are domain-specific.
- “Cancellation stops work.” It may only stop waiting; effects and CPU can continue.
- “Hedging is a faster retry.” Attempts overlap and consume simultaneous capacity.
- “Hedge immediately for best latency.” It duplicates normal fast work and can double load.
- “Send hedge anywhere.” Same endpoint gives no diversity; another region may violate contracts.
- “Reads are always safe to duplicate.” Metering, leases, locks, and expensive computation can have effects.
- “Optional means silently missing.” Response completeness and error provenance must be explicit.
- “Branches finished, so response is fast.” Merge/serialization/output can dominate.
- “Average branch latency shows health.” Tail, correlation, queue, and critical-path distributions matter.
- “Autoscaling fixes fan-out.” Client/instance counts and attempts can scale faster than dependencies.

## Worked Examples

### Example 1

Each of 100 independent required branches exceeds 200 ms with probability 1%. Parent exceedance is $1-0.99^{100}\approx63.4\%$. A one-branch p99 becomes an approximately p36.6 all-of completion at the same threshold.

### Example 2

Ten independent branches each meet 100 ms with probability 0.99. All ten meet it with $0.99^{10}\approx90.4\%$, so about 9.6% of parents exceed. Reducing required branches from 100 to 10 materially changes the tail without changing branch code.

### Example 3

A parent has 120 branches, concurrency 20, and 40 ms mean service with negligible queue. At least six waves are needed, giving an idealized 240 ms before merge. A 200 ms deadline is infeasible even though each branch is “40 ms”; admission must reduce work or use another interaction.

### Example 4

Fifty concurrent parents each may hold 12 branch permits in a governed pool. The scoped in-flight bound is $50\times12=600$. If each branch library invisibly retries twice, deepest attempts can reach 1,800; attempt inventory and the same permit/budget must cover retries.

### Example 5

A 500 ms parent reserves 60 ms for merge/response and 20 ms for cleanup. Branches start after 40 ms admission, leaving at most 380 ms for useful child execution—not a new 500 ms each. An optional enrichment gets 150 ms; required storage gets the remaining bounded budget.

### Example 6

A replica read's original is unfinished at a 95th-percentile hedge delay for 5% of calls. At 100,000 calls/s, one hedge can add about 5,000 attempts/s. The team proves spare capacity, sets a 1,000/s fleet token cap during peak, and accepts less tail improvement rather than overload.

### Example 7

A hedge returns a fast replica value at version 41 while the original returns version 43 shortly afterward; the session requires at least version 42. The fastest response is unacceptable. The client validates the session token and waits within deadline for an eligible result.

### Example 8

A top-20 search has results from 30 of 40 shards. Each remaining shard declares a score upper bound below the current twentieth score. The aggregator can prove unseen results cannot change top 20, cancels the remaining branches, and returns complete—not merely partial—results.

### Example 9

A parent reaches quorum and cancels six losers. Four were queued and release permits; one stops mid-read; one external write already committed. Because all attempts share one idempotency/effect ID, the late commit resolves to the same outcome. Cancellation alone would not have protected correctness.

### Example 10

Independent replay predicts a 2% parent deadline miss, but a zone network delay makes 60% of branches slow together and observed misses reach 18%. Segmenting traces by zone reveals correlation. Hedging inside the same zone adds load; eligible cross-zone routing is capacity- and consistency-gated.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) provides replication, quorum, partial failure, correlation, deadlines, cancellation, and idempotency models.

[Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies distribution-aware measurement, experimental design, simulation, fault injection, and uncertainty analysis.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) contributes top-$K$, early termination, bounded heaps, parallel work/span, and aggregation costs.

[Operating Systems](../../22-operating-systems/ROADMAP.md) explains queues, schedulers, garbage collection, cache/page faults, locks, and resource cancellation.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns shared concurrency/hedge policies, topology-aware balancing, tracing, safe defaults, and load controls.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames common-mode failures, feedback, bottlenecks, capacity, and tail-tolerance trade-offs.

## References

1. Jeffrey Dean and Luiz André Barroso, Google Research, [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/).
2. Google, *Site Reliability Engineering*, [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/).
3. gRPC, [Request Hedging](https://grpc.io/docs/guides/request-hedging/).
4. gRPC, [Deadlines](https://grpc.io/docs/guides/deadlines/).
5. Amazon Web Services, [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/).
6. Envoy Proxy, [HTTP route components: HedgePolicy](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto.html).

## Exercises

### Exercise 1

For 40 independent required branches, each with a 2% chance of exceeding 300 ms, calculate parent exceedance. Recalculate for 10 branches and explain why both results are estimates rather than guarantees.

### Exercise 2

Design a bounded scatter/gather API for up to 500 items under a 1-second deadline. Specify admission, concurrency, waves, child budgets, aggregation, cancellation, and asynchronous fallback.

### Exercise 3

Design delayed hedging for a read replicated across zones. Include eligibility, delay, maximum attempts, topology, version consistency, deadline, load/throttle budget, pushback, cancellation, and observability.

### Exercise 4

Threat-model fan-out and tail controls for an authenticated multi-tenant aggregation API. Cover cardinality attacks, costly inputs, tenant fairness, forged priority, cross-region hedging, data leakage, orphan work, and metric cardinality.

### Exercise 5

Create a verification plan that tests independent-tail math and correlated reality. Include queues, hot shards, GC, zone fault, overload, retry/hedge interaction, inconsistent replicas, cancellation after commit, and recovery.

## Answers to the Exercises

### Answer 1

For 40 branches, exceedance is $1-0.98^{40}\approx55.4\%$. For 10, it is $1-0.98^{10}\approx18.3\%$. These assume identical independent branches, stable distributions, and no load feedback. Shared hosts, queues, keys, zones, deployments, or parent-induced concurrency create dependence; heterogeneous branches require $1-\prod_iF_i(300\text{ ms})$. Validate with segmented traces and correlated fault/load tests.

### Answer 2

Reject or convert requests above 500 items and price cost/bytes before scatter. Reserve perhaps 100 ms for response/merge and explicit cleanup, then test a child window inside the remaining budget. Use per-parent concurrency within tenant/destination bulkheads; derive feasible waves from measured tail service, not the mean. Skip/terminate branches that cannot fit remaining deadline. Aggregate incrementally with bounded memory and deterministic final order. Cancel queued/running work when failure is terminal or criterion completes; track orphans. If 500 items cannot meet one second under safe concurrency, return an accepted long-running operation or pagination rather than raise concurrency unboundedly.

### Answer 3

Allow only read-only/idempotent same-operation attempts to replicas meeting shard, authorization, residency, session-version, and health constraints. Send the original immediately; after a measured high-percentile delay, launch at most one attempt to a different eligible failure domain if parent deadline retains useful time and fleet/tenant/endpoint tokens permit. One original deadline governs both. Accept first semantically eligible version/status, treat fatal errors consistently, honor server pushback, suppress under overload/circuit, and cancel losers. Metrics separate call/attempt, destinations, delay, winner, version rejections, added load, suppression, cancellation latency, and completed-after-cancel.

### Answer 4

Authenticate before trusting tenant/priority and cap items, query complexity, bytes, recursive depth, and fan-out. Give each tenant per-parent and fleet cost/concurrency shares plus protected common capacity. Derive child criticality from parent; do not accept promotion headers. Restrict cross-region attempts by residency and authorization and avoid returning another tenant's cached/replica data. Preserve stable effect IDs, assume cancellation is non-rollback, and bound orphan cleanup. Redact/hash tenant and branch keys in bounded labels. Test huge lists, repeated/hot IDs, expensive filters, priority forgery, cancellation storms, region policy, and high-cardinality metrics.

### Answer 5

Replay measured per-branch distributions at multiple $n$ and compare simulated/observed parent order statistics. Then inject heterogeneous and correlated cases: one hot shard, shared executor/connection queue, synchronized GC, zone delay, cache miss, deployment regression, and global overload. Vary concurrency, parent rate, deadline, payload, and completion rule. Enable retries and hedges at all actual layers; verify total attempt/load budgets and suppression. Return conflicting replica versions and fatal/nonfatal statuses. Cancel at queue/send/execution/response/post-commit stages and assert one completion, released permits, safe effects, and visible orphans. Recovery must drain/cancel work and restore baseline offered load without a speculative herd.
