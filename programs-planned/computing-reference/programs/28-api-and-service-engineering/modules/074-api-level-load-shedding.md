---
module_id: API-074
program: API & Service Engineering
level: 2
module_number: 74
title: API-Level Load Shedding
status: complete
last_verified: 2026-09-02
---

# API-Level Load Shedding

## One-Page Review

### Governing question

When demand or per-request cost exceeds current safe capacity, which API work should be rejected, degraded, deferred, or admitted so the system maximizes useful completed work without violating fairness or truth?

### Essential definitions

- **offered load** is all work presented to a system; **admitted load** is the portion allowed to execute.
- **load shedding** deliberately rejects or stops excess work to keep the system inside a recoverable operating region.
- **goodput** is useful work completed correctly and before its usefulness/deadline expires.
- **brownout** is degraded service during overload, often preserving core functions while optional work is disabled.
- **admission control** decides whether a unit of work may consume a bounded resource.
- **criticality** is a trusted service-wide class describing the user/system consequence of not completing work.
- **cost** is the limiting resource demand of a request, such as CPU time, memory, database operations, bytes, or concurrency-time.
- **pushback** tells a caller not to retry immediately or how long to wait.

### Central model, mechanism, or theorem

For request classes $i$ with admitted rate $x_i$ and measured cost $c_i$, keep estimated demand inside safe capacity $B$:

$$
\sum_i x_i c_i\le B,\qquad 0\le x_i\le\lambda_i,
$$

where $\lambda_i$ is offered rate. Choose $x_i$ by authenticated entitlement, criticality, deadlines, fairness, and marginal user value—not arrival order alone. Reject before expensive work when safe, bound every queue, and continue admitted work only while it can still produce useful output.

### Critical invariants

The system knows its tested safe operating region and measures the resource that actually saturates. Admission happens before the scarce resource whenever possible. Rejection is cheaper than admitted execution, bounded in CPU/memory/logging/network cost, and does not claim that an unconfirmed write failed or succeeded.

Criticality is server-derived or authenticated, propagates consistently, and cannot be raised by an untrusted caller. Within a class, tenants receive defined fairness. Expired/cancelled work is not admitted or retained. Load-shed outcomes are distinct from quota, rate, authorization, validation, circuit, and dependency failures. Retry guidance reflects available capacity and the original deadline.

### Common failures

Scale only after overload; admit until every queue fills; shed based on CPU alone; count requests but ignore cost; reject after authentication/database/log work; emit expensive per-rejection logs; let callers self-declare “critical”; use inconsistent priorities across services; always sacrifice the same tenant; protect health checks while they bypass real dependencies; return generic `500`; send identical `Retry-After` to a fleet; allow retries to bypass admission; keep working after client deadline; drop committed writes ambiguously; autoscale multiplies local thresholds; fallback overloads; and tests stop at peak capacity instead of driving through collapse and recovery.

### Compact example

An API can safely complete 900 equal-cost requests/s but receives 1,200/s. Admitting all pushes latency beyond client deadlines and yields only 500 timely completions. An admission gate accepts 900/s and cheaply rejects 300/s, a 25% shed fraction. If the admitted 900 finish on time, goodput rises from 500 to 900 even though the raw error count increases. **Conclusion:** overload protection optimizes useful completion, not the appearance of accepting every request.

### Connections

[Rate Limits and Quotas](039-rate-limits-and-quotas.md) govern planned rate and entitlement. [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), [Retries and Backoff](072-retries-and-backoff.md), and [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md) bound time, amplification, dependency evidence, and occupancy. The next module carries capacity signals across service boundaries.

## Governing Question

At every API layer, how will current safe capacity, work cost, deadline, authenticated criticality, entitlement, and fairness determine admission—and how will rejection preserve goodput, truthful semantics, and fast recovery under demand well beyond capacity?

## Why This Matters

Overload is not merely high utilization. Beyond an inflection point, contention, context switching, garbage collection, cache churn, lock waits, I/O queues, and retries increase residence time. Clients time out while the server continues work whose result nobody will use. Those clients retry, adding more work, and overload becomes a self-reinforcing state. Throughput can fall even while offered traffic rises.

AWS's load-shedding guidance emphasizes preserving latency for accepted requests and testing beyond the point where goodput plateaus. Google SRE similarly recommends early, cheap rejection, graceful degradation, queue control, deadline propagation, and capacity testing to prevent cascading failures. The objective is not to make every arrival look accepted. It is to complete as much valuable work as the available system can finish.

Provisioning, autoscaling, caching, quotas, and capacity planning remain primary defenses. They cannot eliminate sudden traffic success, fleet loss, cache-miss shifts, dependency slowdown, attacks, or scaling delay. Load shedding is the fast safety layer that keeps a service recoverable while those slower mechanisms act.

API-level decisions can use semantics that a generic proxy cannot: operation cost, tenant entitlement, human versus batch origin, original deadline, idempotency state, and whether a cheaper response is honest. Edge layers are still essential against extreme volume because an overloaded application may lack capacity even to reject. A complete design uses layered protection with a single coherent priority model.

## Prerequisites and Retrieval

Retrieve [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md), [Rate Limits and Quotas](039-rate-limits-and-quotas.md), [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), [Retries and Backoff](072-retries-and-backoff.md), and [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md).

Retrieve the API operation and cost inventory; request sizes and fan-out; arrival, burst, tenant, and criticality distributions; original deadlines; concurrency and queue limits; CPU, memory, connection, event-loop, database, cache, and downstream capacity; autoscaling signals and lag; retry/client behavior; authentication cost; health-check topology; fallback/degradation contracts; idempotency/outcome protocols; edge/proxy rejection behavior; and overload/goodput telemetry.

## Learning Objectives

After completing this module, you can:

1. distinguish overload shedding from quotas, rate limiting, bulkheads, circuits, and backpressure;
2. identify the safe operating region and the resource/cost unit that constrains goodput;
3. place layered admission gates before expensive work without losing semantic authority;
4. reject expired, low-value, excess, or unaffordable work while finishing valuable admitted work;
5. define authenticated, end-to-end criticality and fair allocation among tenants and classes;
6. design bounded queues, concurrency gates, cost-aware admission, and stable adaptive controls;
7. express truthful HTTP/API overload outcomes and safe pushback;
8. coordinate shedding with retries, autoscaling, health checks, degradation, and writes;
9. observe offered load, admitted load, shed decisions, goodput, cost, fairness, and recovery; and
10. verify behavior far beyond capacity, during resource shifts, fleet loss, attack, and recovery.

## Core Exposition

### Distinguish planned limits from emergency capacity

A quota expresses entitlement over a scope and period. A rate limit shapes arrivals or enforces a contract. A bulkhead caps occupancy for a class or dependency. A circuit suppresses calls based on recent dependency outcomes. Load shedding responds to current or predicted inability to complete all offered work usefully. Backpressure tells upstream producers to slow rather than merely returning loss.

The same request can pass quota and rate checks yet be shed because half the fleet disappeared. Conversely, a tenant may exceed its quota while the service is idle. Use separate reason codes, metrics, policy owners, and client guidance. Do not call every rejection “throttling”; callers need to know whether waiting, changing input, reducing concurrency, or requesting entitlement can help.

Provisioned load should normally be protected before opportunistic burst. Load shedding is not permission to chronically underprovision promised traffic. Repeated shedding of within-contract demand is a capacity/SLO incident even when the mechanism prevents collapse.

### Find the goodput cliff

Measure offered rate, admitted rate, completed rate, timely successful rate, latency, and resource use while load increases past expected peak. Many systems have a region where throughput rises roughly with load, then a knee where latency accelerates, and finally a collapse region where useful completions fall.

The safe operating point needs headroom for bursts, uneven load balancing, garbage collection, dependency variance, and capacity loss. A threshold at 100% CPU is usually too late. CPU may not be limiting at all: memory allocation, event-loop lag, database connections, lock contention, I/O, network buffers, file descriptors, or a downstream quota can fail first.

Repeat tests with realistic request mixes. A cache-hit read and cache-miss report may differ by orders of magnitude. Average requests/s hides cost shifts. Test cold caches, large payloads, expensive authorization, fan-out, dependency slowdown, failures that trigger logs, and retries.

Goodput is contract-specific: a correct response after the caller's deadline is waste, a partial response may or may not be useful, and an accepted asynchronous command counts only under its durable lifecycle contract. Define usefulness before optimizing it.

### Place rejection early and cheaply

The cheapest safe layer should block clearly excess or abusive traffic: network protection, CDN/WAF, gateway rate policy, load balancer, proxy, framework admission, then operation-specific application control. Each inner layer has richer semantics but less spare capacity. Each outer layer has more leverage but less knowledge.

Before admission, avoid expensive body buffering, decompression, parsing, signature work, database lookup, tracing payload capture, or synchronous logging where the protocol/security model permits. Some authentication must occur before tenant priority or quota can be trusted; make that path bounded and protect it separately.

Rejection itself consumes sockets, TLS, CPU, bytes, and telemetry. Measure its cost beyond collapse. Aggregate metrics instead of writing one expensive log per rejected request. Bound error bodies. Under extreme attack, an upstream layer may need to drop connections or packets because the application cannot afford a semantic response.

Do not move nuanced admission solely to a proxy that cannot see cost, deadline, or criticality. Use coarse outer caps to preserve the application gate, then let the application make fine decisions from local resource information.

### Reject work that cannot be useful

Propagate an absolute deadline or remaining budget using a trusted contract. Reject before enqueue or execution if remaining time cannot fit estimated queue delay plus minimum useful service and response. Remove cancelled or expired work from queues immediately.

Once admitted work begins, continue it only while completion can still produce value. Check cancellation/deadline at bounded interruption points, especially before expensive fan-out or irreversible effects. A response computed after the client has abandoned it wastes scarce capacity and often provokes a retry.

Writes need semantic care. A shed decision before effect admission can be a clear temporary rejection. After an effect may have committed, the server cannot relabel it as shed. Preserve the operation/idempotency key, record authoritative state, return/recover the outcome, or report pending/unknown with reconciliation.

Bound work per request with pagination, maximum batch size, payload/complexity limits, fan-out limits, and asynchronous jobs. Admission is much easier when a unit's worst credible resource demand is known.

### Model cost, not only request count

Let each operation class have a conservative estimated cost in the limiting resource. A cheap cached lookup might cost one unit; an uncached aggregation might cost 20. Admit against a token or concurrency-time budget, updating estimates from telemetry. Separate budgets may be needed for CPU, memory, database, and external dependency capacity.

A single scalar cannot capture every bottleneck. Use a dominant-resource rule or sequential gates: payload memory, application concurrency, database permits, and response bandwidth. Avoid a complicated optimizer on the request hot path unless tests prove its reliability and cost.

Cost estimates can be manipulated by inputs. Validate declared sizes; derive complexity from bounded server-side features; charge the actual tenant; and stop work if cost grows beyond the admitted envelope. Record estimate versus actual to find systematic underpricing.

Static request caps are predictable. Adaptive limits can follow workload and capacity changes but may oscillate when every instance reacts to noisy latency. Use floors, ceilings, smoothing, hysteresis, bounded adjustment rate, and a stable fallback configuration. Verify aggregate behavior under autoscaling and synchronized controllers.

### Define trusted criticality

Criticality describes consequence, not caller impatience. Useful classes might be safety/control, interactive committed workflow, interactive optional enrichment, background maintenance, and deferrable batch. Keep the vocabulary small and consistent across services.

Derive priority from authenticated identity, operation, workflow state, and server policy. An external client must not gain protected capacity by setting `priority=critical`. Sign or reconstruct cross-service metadata; prevent a compromised upstream from promoting arbitrary traffic.

Criticality must propagate with causation. A low-priority crawler cannot call a downstream as high priority merely because the downstream operation is normally important. Conversely, a critical workflow should not be silently downgraded at one hop. Define rules for fan-out: child work normally cannot exceed parent criticality.

Reserve capacity for control-plane health only when it exercises what recovery requires. A shallow liveness ping that bypasses saturated dependencies can keep traffic routed to an unusable instance. Readiness and admission health should reflect ability to serve protected work without allowing probes to consume all reserve.

### Preserve fairness and avoid starvation

Priority says which consequences matter; fairness says how peers share capacity. Within a class, apply tenant quotas, weighted fair allocation, per-tenant concurrency, or probabilistic shedding so one noisy client cannot consume everything.

Do not always reject the same unlucky tenant or hash range unless deliberate cohort stability is a product choice. Random shedding spreads errors but can make every user experience intermittent failure. Consistent cohort shedding can preserve a complete experience for many users while denying a subset; rotate carefully and assess fairness, contractual, and abuse implications.

Strict priority can starve background work indefinitely and later cause maintenance, replication, expiration, or security failures. Reserve a small floor, age waiting work, or move deferrable work to durable scheduling with explicit lateness objectives. “Batch” is not synonymous with disposable.

Account for request cost: equal request counts are unfair if one tenant sends 100-times more expensive inputs. At the same time, do not let inaccurate cost estimates systematically exclude a valid workload. Publish limits and provide observability/recourse.

### Use bounded queues and concurrency

Queues absorb short mismatch between arrival and service, but they hide overload and spend deadlines. Bound both length and age. Reject before enqueue when full and again before execution when too old. Include queues in gateways, load balancers, runtimes, executors, connection pools, drivers, and brokers—not only application code.

First-in-first-out is simple but can leave fresh, useful work behind expired expensive calls. Deadline-aware queues, class queues, or controlled-delay approaches can improve goodput, but reordering may violate per-key/business order. Make order constraints explicit.

Concurrency admission often tracks overload better than raw request rate because slow work retains permits. It still needs cost/priority awareness: 100 cheap async waits differ from 100 CPU-bound reports. Use the bulkhead principles from API-073 and shed when permits or allowed wait expire.

Avoid large surge queues that deliver requests to a server after the client has timed out. A small spillover/fail-fast policy is often safer. If work must survive, accept it into a durable asynchronous contract with idempotency, expiry, position/status, and cancellation—not an invisible memory queue.

### Choose signals without chasing noise

Useful signals include in-flight work, queue age, event-loop lag, runnable threads, heap/GC pressure, memory, database/connection saturation, dependency latency, deadline miss rate, and recent goodput. Combine leading capacity indicators with direct user outcome.

CPU utilization alone is ambiguous: 90% may be healthy for compute work, while 30% can coexist with a saturated database pool. Tail latency alone can rise after queues are already dangerous and can be distorted by shedding cheap work. Queue length alone ignores service time.

Local signals enable fast instance admission. Fleet/global signals help account for capacity loss and uneven routing but arrive late or fail during incidents. Protect locally first, use global information for coarse allocation, and never require a remote metrics service to admit every request.

Use hysteresis so admission does not flap. Define recovery as a ramp: after pressure falls, gradually admit lower classes while checking goodput and queues. Autoscaling is slower and can fail; load shedding remains active until new capacity is ready and warmed.

### Express overload honestly in the API

HTTP `503 Service Unavailable` represents temporary inability to handle a request because of overload or maintenance and may include `Retry-After`. `429 Too Many Requests` conventionally represents rate limiting of the client/request scope. Apply the API's documented contract; do not use `500` for deliberate admission policy.

Return a stable machine-readable error code, whether the operation was admitted, retryability, the governing scope if safe to reveal, and correlation metadata. `Retry-After` is guidance, not permission to ignore the original deadline or retry budget. If every client receives the same instant, synchronized retries can recreate overload; use a window/jitter contract where possible.

For gRPC or other protocols, choose the documented overload/resource status and pushback semantics consistently across gateway translation. Avoid translating a server-capacity `503` into a tenant-quota error or vice versa.

Connection reset/drop is a last-resort outer protection because it obscures whether a request reached the application and can trigger aggressive retries. Semantic rejection is preferable when affordable. Large rejection bodies and synchronous audit calls can defeat the gate.

### Coordinate clients and retries

A shed response is a request to reduce offered work. Clients should stop immediate retries, use capped jitter and server pushback, spend a fleet retry budget, and abandon work that no longer fits its original deadline. Retrying another replica can spread overload.

The server should distinguish retryable temporary capacity from hard quota, invalid request, or non-retryable expensive operation. It may advertise asynchronous deferral or cheaper query forms. It must not promise a retry time unsupported by recovery evidence.

Initial useful requests generally outrank retries. Otherwise retry traffic consumes admission and prevents new operations. Retry attempts re-enter the same cost, fairness, criticality, circuit, bulkhead, and deadline gates; they do not carry automatic privilege.

Client-side throttling/backpressure reduces rejection cost and network load, but the server remains authoritative because clients can be stale, buggy, or hostile. The next module develops cross-service backpressure in detail.

### Degrade before discarding when honest

Some APIs can reduce cost: smaller search scope, fewer optional enrichments, stale cache with age, lower image resolution, partial fields, approximate aggregation, delayed consistency, or asynchronous completion. Define the degraded representation and client opt-in/expectation; do not silently change correctness.

Degradation itself needs a capacity model. A cache-miss storm can remove the cheap path; a fallback store can be smaller than the primary. Feature flags evaluated through a remote control plane may fail during overload. Keep safe local defaults and test combined degradation plus shedding.

Prefer a completed cheaper answer over starting a rich response that misses deadline. But preserve atomicity and security: partial authorization, partial financial effects, or incomplete policy evaluation are not graceful degradation.

Track quality alongside availability. A service that returns empty results quickly may look healthy while providing no user value. Goodput includes semantic usefulness.

### Layer protection and health behavior

Edge/WAF/CDN controls absorb attacks and obvious excess. Gateways enforce identity, quotas, maximum size, and coarse fleet capacity. Load balancers avoid unusable instances. Instance frameworks enforce local concurrency/deadline. Application operations apply semantic cost, criticality, and degradation. Downstream clients carry deadlines and backpressure.

Layers need consistent reasons and priorities. If the edge drops all traffic indiscriminately before protected workflows reach application reserve, fine-grained policy is useless. If only the application sheds, extreme traffic can exhaust sockets/TLS first. Allocate protective envelopes between layers and test their order.

Health checks receive protected but bounded capacity. Under brownout, failing every readiness check can remove capacity and concentrate load; always passing can route to a wedged instance. Design separate liveness, readiness, and overload signals with load-balancer behavior understood.

Operations such as configuration, credential refresh, leader lease, queue drain, and telemetry may be required for recovery. Reserve enough control capacity, but prevent it from becoming an unbounded bypass labeled “internal.”

### Observe decisions and goodput

Measure offered, authenticated, admitted, degraded, shed, cancelled, expired, completed, timely successful, and late-completed work. Segment by operation, cost class, trusted criticality, tenant cohort, instance/cell/region, reason, and policy version while bounding label cardinality.

Report shed fraction $S=(\lambda-a)/\lambda$ for offered rate $\lambda$ and admitted rate $a$, plus weighted admitted cost. Correlate with latency, queue age, concurrency, CPU, memory, dependencies, autoscaling, retries, fallback load, health changes, and SLO outcomes.

Watch fairness: within-entitlement rejection by tenant/class, starvation duration, reserve use, and cost-estimate error. Watch control quality: rejection cost, false shedding while capacity is idle, failure to shed before collapse, oscillation, and time to recover.

Dashboards must show goodput, not just success percentage among admitted calls. Excluding shed requests can make availability look perfect while most users are rejected; counting late useless work as success can hide collapse. Preserve both total-demand and admitted-service views.

### Verify overload as a state transition

Ramp realistic mixed load from idle through expected peak, safe limit, knee, severe overload, and back down. Hold each level long enough to expose queues, GC, thermal effects, autoscaling, retries, and dependency saturation. Verify that goodput plateaus rather than collapses and recovery is prompt.

Vary request cost without changing rate; remove fleet capacity; slow a dependency; force cache misses; create tenant skew; send huge/invalid inputs; expire deadlines in every queue; cancel clients; amplify retries; and attack priority metadata. Test control-plane and telemetry loss.

Test the cost of rejection itself at extreme volume. Confirm bounded CPU, memory, sockets, response bytes, logs, and metrics. Verify outer gates preserve inner semantic admission rather than masking it.

Check invariants: no class exceeds its effective resource envelope; untrusted callers cannot promote; expired work does not start; admitted effects retain truthful outcome; retries receive no bypass; health reserve is bounded; queues have length/age limits; and lowering offered load returns the system to normal without restart.

## Definitions and Notation

Let $\lambda_i$ be offered request rate for class $i$, $x_i$ admitted rate, $c_i$ estimated limiting-resource cost, and $B$ safe capacity per unit time. Let total offered rate be $\lambda=\sum_i\lambda_i$, admitted rate $a=\sum_i x_i$, and shed fraction $S=(\lambda-a)/\lambda$ for $\lambda>0$.

Let $G$ be useful, correct, timely completions per unit time. Goodput $G$ differs from raw throughput, which can include late, abandoned, duplicated, or semantically useless work. Let $D$ be original deadline, $t$ current time, $W_q$ estimated queue wait, and $W_s$ minimum useful service time. Work is temporally admissible only when $D-t>W_q+W_s$ plus response reserve.

An **admission envelope** is the tested set of resource/cost conditions under which the system remains recoverable. **priority inversion** occurs when lower-value work blocks protected work. **starvation** is indefinite denial to a class. **spillover** rejects excess instead of retaining it in a surge queue.

## Mechanisms, Invariants, or Proof Structure

**Capacity-bound argument.** If every admitted class-$i$ request spends $c_i$ tokens and admission atomically enforces $\sum_i x_i c_i\le B$ over the policy window, estimated admitted cost is bounded by $B$. The proof fails when cost is understated, work bypasses the gate, the window permits unsafe bursts, or a different resource becomes limiting.

**Goodput counterexample.** Suppose capacity is 900 equal-cost requests/s and demand is 1,200/s. Admit-all overload completes only 500 before deadline. Shedding 300 and completing 900 yields greater goodput despite more explicit rejections. Therefore acceptance rate alone is not an availability objective under overload.

**Deadline argument.** If remaining budget is no greater than queue wait plus minimum service and response reserve, admission cannot produce a timely result under those estimates. Rejecting now saves capacity without reducing estimated goodput. Estimates and clock/deadline trust remain empirical obligations.

**Fairness argument.** If protected tenant $j$ has a reserved non-borrowable envelope $b_j$ and other traffic cannot consume it, other tenants cannot remove that capacity. This does not guarantee tenant $j$ success if its own demand/cost exceeds $b_j$ or a shared ungated dependency fails.

Operational invariants are: rejection precedes scarce work where safe; every admitted unit is bounded; priority is trusted and monotone across fan-out; deadlines/cancellation remove worthless work; fairness is explicit; write outcomes remain truthful; retries respect admission; queues and reserve are bounded; recovery ramps; and all decisions expose reason and scope.

## Alternatives and Trade-Offs

Fixed admission thresholds are explainable and stable but drift as code, mix, and dependencies change. Adaptive controls follow capacity but can oscillate, synchronize, or reward a degraded signal. Bound adaptation with tested floors/ceilings and retain a static emergency mode.

Random shedding shares pain statistically. Stable cohort shedding gives unaffected users a coherent experience but may unfairly exclude the same group. Strict priority protects critical work but risks starvation; weighted/reserved capacity preserves some lower-class progress at the cost of protected headroom.

Edge shedding is cheap and attack-resistant but semantically coarse. Application shedding sees deadline, cost, and workflow but consumes more resources. Layer both with aligned envelopes.

Fail-fast protects latency and recovery. Small queues absorb bursts; durable queues defer work with explicit lifecycle; large hidden queues convert overload into stale work. Degradation preserves responses but can weaken quality and overload fallback.

Rate-based admission is simple for uniform work. Concurrency follows latency changes. Cost-weighted or multi-resource gates fit heterogeneous work but need robust estimates. Choose the least complex mechanism that bounds the observed failure mode.

## Failure Modes and Misconceptions

- “Autoscaling prevents overload.” Detection, provisioning, warmup, quota, dependency, and synchronized failure leave gaps.
- “High CPU means overload.” The limiting resource may be elsewhere, and high CPU can be healthy.
- “Requests per second measures load.” Work cost, residence, payload, cache state, and fan-out can change independently.
- “Accepting everything maximizes availability.” Late/abandoned work can collapse goodput.
- “A large queue absorbs the spike.” It spends deadlines and memory and prolongs recovery.
- “Reject at the edge only.” The edge lacks operation cost and current local resource knowledge.
- “Reject in application only.” Extreme traffic may exhaust network/TLS/framework capacity first.
- “Clients can label criticality.” Untrusted promotion defeats protection.
- “Internal traffic is always critical.” An unbounded bypass can consume the entire reserve.
- “Health checks should never be shed.” They need protected bounded capacity and representative semantics.
- “429 and 503 are interchangeable.” They communicate different scopes and remedies in a documented API.
- “Retry-After solves retries.” Synchronized clients, expired deadlines, and missing spare capacity still matter.
- “Rejected work is free.” Parsing, logging, metrics, response bytes, and connections can dominate.
- “All successful responses are goodput.” Late, stale beyond contract, empty, or duplicate results may be useless.
- “Degradation is always safe.” Some writes, authorization, and policy decisions cannot be approximated.
- “Priority eliminates fairness concerns.” Strict priority can starve tenants and essential background work.
- “The threshold is proven by one peak test.” Mix, fleet loss, cold state, attacks, and recovery change the envelope.

## Worked Examples

### Example 1

An equal-cost API receives 1,200 requests/s and has tested safe admission of 900/s. It sheds 300/s, so $S=(1200-900)/1200=25\%$. The admitted 900 finish before deadline. The dashboard reports both 75% demand admission and 900/s goodput instead of claiming 100% availability among admitted calls.

### Example 2

A cost gate has 1,000 units/s. Cached reads cost one unit and report generation costs 20. Offered work is 600 reads/s and 30 reports/s, totaling $600+30\times20=1{,}200$ units/s. After protecting 600 reads, only 20 reports/s fit; 10 reports/s are deferred or shed. Counting 630 requests would have hidden overload.

### Example 3

A request has 80 ms remaining. Estimated queue wait is 35 ms, minimum useful execution 40 ms, and response reserve 10 ms. Because $35+40+10=85$ ms exceeds the budget, admission cannot yield a timely result under the estimates. The API rejects before enqueue rather than doing late work.

### Example 4

A tenant is within its monthly quota but half the serving fleet was lost. The request passes quota and ordinary rate checks, then receives a temporary capacity `503` with bounded pushback. Metrics record `overload_capacity`, not `quota_exceeded`. The client reduces concurrency rather than requesting a larger entitlement.

### Example 5

An API trusts a public `X-Priority: critical` header. A scraper sets it and consumes the protected pool. The corrected gateway authenticates the caller, strips the public header, derives criticality from operation/workflow policy, and signs internal metadata. Child calls cannot exceed parent criticality.

### Example 6

Randomly shedding 20% causes nearly every interactive user to see occasional missing calls. A product chooses a stable, rotating 20% cohort for an optional personalization feature, preserving a consistent core experience for all and the feature for 80%. The rotation, accessibility impact, and tenant fairness are reviewed rather than assuming hashing is neutral.

### Example 7

A load balancer queues 50,000 requests during a 30-second incident. When servers recover, most requests have already exceeded their 2-second deadline and crowd out fresh work. Replacing the surge queue with a small deadline-aware spillover gate makes recovery immediate; durable tasks use an explicit job API instead.

### Example 8

The service sheds at 85% CPU, but database connections saturate at 40% CPU during cache misses. A multi-signal gate limits database concurrency and queue age while CPU remains a separate ceiling. A load test that changes only the cache-miss mix validates the new protection.

### Example 9

Every `503` response performs synchronous structured logging to a remote collector. At extreme traffic the rejection path costs more than a cached success and fails when the collector slows. The service switches to bounded counters and sampled local events with asynchronous export. Rejection cost is then included in overload tests.

### Example 10

A charge request passes admission and commits, but the response path becomes overloaded. The server cannot truthfully turn it into a pre-admission `503`. It records the outcome under the idempotency key; a retry with the same key retrieves that outcome. Load shedding prevents new effects while outcome reconciliation handles admitted writes.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains feedback, partial failure, deadlines, retry amplification, consistency, and why local admission signals cannot become global truth automatically.

[Operating Systems](../../22-operating-systems/ROADMAP.md) supplies scheduling, queues, memory, CPU, context-switch, event-loop, and resource-control mechanisms behind the goodput cliff.

[Network Engineering](../../24-network-engineering/ROADMAP.md) covers edge filtering, connections, load balancers, queues, health checks, resets, and protocol pushback.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns reusable admission libraries, gateway policies, criticality propagation, autoscaling, safe configuration rollout, and fleet observability.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes feedback-loop, bottleneck, capacity, fairness, graceful-degradation, and recovery analysis.

[Security Engineering](../../25-security-engineering/ROADMAP.md) addresses denial of service, trusted priority, tenant isolation, bounded authentication, override governance, and safe error disclosure.

## References

1. Amazon Web Services Builder Center, [Using load shedding to avoid overload](https://builder.aws.com/content/3Eun1EEyX6p2e3VYNyRLSJzLuMV/using-load-shedding-to-avoid-overload).
2. Google, *Site Reliability Engineering*, [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/).
3. Google, *Site Reliability Engineering*, [Handling Overload](https://sre.google/sre-book/handling-overload/).
4. Google, *The Site Reliability Workbook*, [Managing Load](https://sre.google/workbook/managing-load/).
5. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
6. Envoy Proxy, [Overload manager](https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager).

## Exercises

### Exercise 1

Given an API with cached reads, cache-miss reads, writes, and batch reports, design a cost-aware admission envelope. Identify resources, cost units, priority, fairness, deadlines, degradation, and validation evidence.

### Exercise 2

A fleet can safely admit 2,000 cost units/s. Interactive requests offer 1,200/s at one unit, background requests offer 300/s at four units, and a protected control class offers 100/s at one unit. Calculate offered cost and propose an allocation that preserves control and interactive work while giving background a nonzero floor.

### Exercise 3

Design the overload error contract for an HTTP API. Distinguish quota/rate rejection, temporary server overload, expired work, and ambiguous admitted writes. Include status, stable code, pushback, idempotency, and client behavior.

### Exercise 4

Create an overload test matrix that finds the goodput cliff and verifies recovery. Include mix shift, fleet loss, retry amplification, rejection cost, queue expiry, priority attack, fallback failure, health checks, autoscaling, and controller oscillation.

### Exercise 5

Audit layered shedding across WAF, gateway, load balancer, service framework, application, and downstream clients. Assign each layer's knowledge, limits, rejection behavior, metrics, and failure mode; resolve conflicting priority or retry policy.

## Answers to the Exercises

### Answer 1

Measure CPU time, memory/payload, database concurrency, downstream calls, response bytes, and residence time per class and input band. Gate maximum payload first, then authenticated tenant/rate, then local concurrency and database/downstream cost. Derive priority from workflow rather than headers; reserve critical capacity and use weighted per-tenant sharing. Reject work whose queue plus service cannot fit deadline. Cached reads may degrade to explicitly aged data; reports may become durable jobs; writes cannot fabricate success. Validate estimates versus actual cost under cache loss, large inputs, dependency slowdown, fleet loss, retries, and recovery beyond the goodput cliff.

### Answer 2

Offered cost is $1{,}200\times1+300\times4+100\times1=2{,}500$ units/s. Reserve 100 for control and admit all 1,200 interactive units, leaving 700. At four units each, at most 175 background requests/s fit. This sheds 125 background requests/s while preserving a substantial nonzero floor. A production policy would also apply tenant fairness, burst headroom, deadlines, and measured safe capacity; it would not assume the 2,000-unit envelope is exact under every mix.

### Answer 3

Use the documented rate-limit response, commonly `429`, with scope/reset for a caller exceeding quota/rate. Use `503` plus stable `overload_capacity` for temporary server inability and safe bounded `Retry-After` when known. Reject expired work with the API's deadline/cancellation code and no retry beyond original intent. State whether admission occurred. For a write that may have committed, return/retrieve the authoritative same-idempotency-key outcome or pending/unknown reconciliation; never relabel it as pre-admission shedding. Clients use capped jitter, original deadline, and retry budget, and do not change effect identity.

### Answer 4

Ramp realistic mixed load through idle, peak, knee, severe overload, sustained overload, and decline. Record offered/admitted/shed, weighted cost, goodput, tails, queues, resources, retries, and recovery. Repeat with cache-hit-to-miss shift, half fleet, slow dependency, synchronized clients, expensive rejection logging, deadlines expiring at every queue, forged criticality, saturated fallback, and health-check pressure. Exercise autoscaling lag/failure, process restart, telemetry/control-plane loss, and adaptive controllers across many instances. Pass criteria include bounded resources/queues, protected fairness, no priority promotion, cheap rejection, goodput plateau, truthful writes, and recovery without restart or oscillation.

### Answer 5

WAF handles attack signatures and coarse volume; gateway authenticates, strips untrusted priority, enforces quota/size, and applies fleet envelope; load balancer limits connections/queue and understands health; framework enforces deadline-aware local concurrency; application prices operation/input and selects honest degradation; downstream clients propagate deadline/criticality and obey pushback. Each emits a stable layer/reason metric. Outer limits must leave room for protected inner traffic, priorities must use one vocabulary and cannot rise on fan-out, and retries re-enter all gates. Test each layer unavailable or saturated and ensure no remote metrics/control service becomes a hot-path dependency.
