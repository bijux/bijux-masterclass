---
module_id: SEPAT-085
program: Software Engineering: Patterns
level: 2
module_number: 85
title: Rate Limiter
status: complete
last_verified: 2026-08-29
---

# Rate Limiter

## One-Page Review

### Governing question

How can a service govern how much work an authenticated scope may offer over time— including legitimate bursts and weighted cost—without confusing rate with concurrency, capacity, quota, or correctness?

### Essential definitions

- A **rate limiter** is an admission policy that bounds admitted cost over time for a declared key and scope.
- A **limiter key** is the authenticated principal, tenant, route, resource, region or hierarchy whose usage shares state.
- A **token bucket** accumulates tokens at rate r up to capacity B and spends cost c per admitted operation.
- **burst capacity** B is the maximum stored allowance; it is not a concurrency limit.
- A **leaky-bucket meter/GCRA** constrains conformity against a theoretical arrival schedule; “leaky bucket” can also mean a finite draining queue, so implementations must name semantics.
- A **fixed window** counts usage in disjoint intervals and can allow boundary bursts.
- A **sliding log/window** evaluates recent usage without fixed-window reset artifacts, at greater state/approximation cost.
- A **weighted limiter** charges an operation-specific cost such as requests, bytes, compute units or estimated downstream work.
- A **quota** commonly limits total use over a longer accounting period; rate limits govern temporal admission and may coexist with quotas.
- A **throttle response** explicitly reports non-admission, usually with retry/policy advice that remains subordinate to the caller deadline.

### Central model, mechanism, or theorem

For token count T at last update t₀, current monotonic time t, refill rate r, capacity B and requested cost c:

\[
T'=\min(B,\;T+r\max(0,t-t_0)).
\]

Admit atomically iff T'≥c, then set T←T'−c; otherwise retain T' and reject/defer. Over any interval of length Δ, a single bucket can admit no more than B+rΔ cost under the ideal model, including allowance stored before the interval. Local buckets on n replicas can jointly admit roughly nB+nrΔ unless configured/coordinated to represent a global policy. Rate limiting does not bound concurrent residence: admitted rate λ combined with long service W can still produce L≈λW in-flight work.

### Critical invariants

- The limiter names its key, trust source, protected resource, algorithm, units, rate, burst, cost and enforcement location.
- Identity is authenticated and normalized before keying; attacker-controlled high-cardinality keys cannot allocate unbounded state.
- Refill and spend are one atomic decision; concurrent requests cannot overspend the same tokens.
- Elapsed-time accounting uses monotonic time locally and handles zero, backward, overflow and long-idle boundaries.
- Every hierarchy level that must hold—global, dependency, tenant, route, operation—authorizes the request without partial token loss.
- Rejection occurs before expensive/protected work where possible and is distinguishable from dependency/business failure.
- Queueing/defer is finite in count, bytes and age; a limiter never hides an unbounded waiting room.
- Rate, burst and weighted costs fit measured downstream capacity and compose with concurrency bulkheads.
- Distributed/local enforcement states its maximum overshoot, outage behavior, staleness and reconciliation model.
- Response metadata is informative, privacy-safe and not a promise that a future request must succeed.

### Common failures

Common failures include “100 requests per minute” without burst algorithm, fixed-window double bursts, one process-local bucket assumed global, per-IP keys punishing NAT users and evadable by botnets, trusting API-key headers before authentication, one key per arbitrary URL or user input, request count ignoring payload/compute cost, non-atomic read-modify-write, wall-clock refill, full buckets on every replica restart, refunding tokens after work already consumed, sequential hierarchical checks that burn some buckets before a later rejection, sleeping server threads instead of rejecting, returning `429` after the database call, rate limiting mistaken for concurrency isolation, `Retry-After` longer than the deadline, high-priority bypass with no cap, metrics keyed by raw tenant, and treating best-effort platform throttles as hard ceilings.

### Compact example

A document API gives each authenticated tenant a token bucket of 20 request-cost units/s with burst 40, inside a global dependency bucket. Metadata reads cost 1, searches 4, and exports are admitted through a separate durable workflow/quota rather than pretending one request costs 1. A tenant may burst 40 units after idle, then sustains 20/s. An additional database bulkhead caps concurrency because 20/s with slow queries could still accumulate many in flight. Rejects happen before request-body buffering beyond a small bounded envelope.

### Connections

[SEPAT-082](082-timeout-and-deadline.md) bounds any wait/retry advice, [SEPAT-083](083-circuit-breaker.md) suppresses likely failures, and [SEPAT-084](084-bulkhead.md) reserves concurrent resources. Rate Limiter prepares the forthcoming Load-Shedding and resilience-composition modules.

## Governing Question

Which temporal admission algorithm, hierarchy, identity and distribution model constrains offered work fairly and observably while preserving bursts that the system can actually absorb?

A rate number is incomplete. “Ten per second” could mean a fixed counter that resets each second, a token bucket with a ten-request burst, a strict 100 ms spacing rule, a rolling window, ten per instance, or ten across a fleet. These accept different traces. A production contract must make the trace language and enforcement error explicit.

## Why This Matters

Unbounded or unfair arrival can exhaust downstream quotas, create noisy-neighbor failure, increase cost, or enable denial of service. A limiter shapes admission before work enters expensive paths. But it is not a capacity oracle: service time changes, request costs vary, dependencies fail, and fleet topology scales. A stale limit can be too loose during impairment or needlessly restrictive after safe capacity increases.

Rate policy is also a product/security contract. It decides whose work is admitted and how rejection is communicated. Incorrect keys can merge unrelated customers, permit evasion, leak identifiers or allocate attacker-controlled state. Distributed enforcement trades coordination cost and availability against overshoot. These trade-offs deserve the same rigor as other correctness mechanisms.

## Prerequisites and Retrieval

Learners should retrieve:

- arrival/service rate, Little's Law, burstiness and queue stability;
- monotonic clocks, atomic read-modify-write and numeric precision;
- authentication, tenant identity, quotas and abuse resistance;
- hash partitioning, replication, consistency and failure modes;
- HTTP `429 Too Many Requests` and `Retry-After` semantics;
- finite queues, backpressure, bulkheads and load shedding;
- probability/distributions for testing randomized/client behavior.

Before proceeding, construct two arrival sequences that both average ten requests per second over a minute but impose very different instantaneous load.

## Learning Objectives

After this module, learners can:

1. specify token bucket, fixed/sliding window and GCRA-style admission precisely;
2. compute burst and interval bounds and distinguish them from concurrency;
3. choose authenticated limiter keys and bounded state lifecycles;
4. model weighted/multidimensional cost rather than only request counts;
5. compose global, dependency, tenant, route and operation policies atomically/fairly;
6. compare local, sharded, centrally coordinated and leased distributed enforcement;
7. define throttle response, client behavior, queue/defer and deadline semantics;
8. verify boundary traces, concurrency atomicity, fleet overshoot and security abuse;
9. calibrate policies against measured capacity, SLOs, economics and risk.

## Core Exposition

### State the policy contract

For each limiter define:

- protected capacity or fairness objective;
- enforcement point and work already spent before it;
- key source and trust boundary;
- cost unit and cost function;
- algorithm and exact boundary/equality behavior;
- sustained rate r and burst/window capacity B;
- state lifetime, idle eviction and cold-start behavior;
- hierarchy/composition order;
- local versus global scope and overshoot;
- reject, bounded wait, degrade or durable-defer outcome;
- response metadata and client expectations;
- fail-open/fail-closed/degraded behavior if limiter state/service fails.

Limits can protect an upstream service from clients, a caller from dependency quotas, tenants from one another, an expensive operation, a background consumer or a cost budget. One policy rarely serves every purpose. A global dependency limit plus per-tenant fairness shares are common; route-only limits can let many routes jointly exceed the downstream budget.

### Token bucket

Tokens accrue continuously or in discrete fills up to B. Each operation costs c. After idle, up to B cost can arrive immediately; thereafter average admitted cost is bounded by r under the ideal single-bucket model. B should reflect absorbable burst across queues, concurrency and downstream capacity—not marketing preference.

Use fixed-point/integer units or carefully specified numeric precision. Refill lazily at admission using monotonic elapsed time, then atomically test/spend. Clamp backward time to zero rather than minting tokens. Saturate multiplication/addition to avoid overflow after long idle. Decide whether c>B is always impossible, split across a durable workflow, or uses another policy.

The interval bound B+rΔ includes tokens stored before the interval. It is an upper bound, not a guarantee of service: other limits, failures and concurrency may reject. If the bucket starts empty, the initial B term is not available. Discrete refill creates microbursts at fill boundaries; continuous/fixed-point refill produces different traces.

Do not refund automatically on downstream error. Admission capacity may already have been consumed, and retries can exploit refunds. If the token represents a monetary quota rather than load, reservation/commit/refund may be appropriate—but it needs transactional ownership and differs from traffic shaping.

### Fixed and sliding windows

A fixed window counter permits at most N within named intervals, but N calls at the end of one window plus N at the beginning of the next can produce 2N in a short span. It is easy to distribute/operate and may be adequate for coarse quotas if this burst is acceptable.

A sliding log stores timestamps/costs and removes entries older than Δ, giving exact recent-window behavior within clock/atomicity assumptions but using state proportional to admitted events. A sliding-window counter combines adjacent buckets approximately, with defined error. Ringed time buckets bound memory and approximation. State exact algorithm and inclusion at the boundary: is an event exactly Δ old included?

GCRA/theoretical-arrival-time methods enforce conformance to a rate plus tolerance without storing every event. They can express burst tolerance and regular spacing. “Leaky bucket” must be disambiguated: a meter rejects nonconforming arrivals, while a queue drains at a fixed rate and adds latency/memory/failure ownership.

### Rate is not concurrency or quota

At admitted arrival λ and mean residence W, mean in-flight work at a stable boundary is L=λW. A limit of 100/s with W=10 s can imply around 1,000 residents. Use a bulkhead for in-flight resource bounds and deadlines/cancellation for residence. Rate limiting alone cannot protect a dependency whose service slows dramatically.

A daily quota of one million operations allows radically different bursts unless paired with a rate policy. Conversely, a rate bucket can permit unlimited total use over a day. Define both when economics/accounting and instantaneous capacity matter. Storage/compute/bytes may need separate budgets; one scalar token cost approximates a vector and can be gamed if estimates are poor.

Load shedding responds to current saturation/overload evidence, while a rate limiter applies a configured temporal policy even when idle capacity exists. Adaptive limits blur the boundary and require stable feedback design.

### Keys, identity and state cardinality

Key after authenticating and normalizing identity. API keys identify applications only if securely bound; user-supplied headers do not. Source IP is useful for coarse unauthenticated abuse defense but merges users behind NAT/proxies and is evadable through distributed sources. Respect trusted proxy chains only under explicit network configuration.

Choose bounded cardinality: tenant ID from an authorized registry, plan tier, route template—not raw path/query. Per-resource keys need admission/eviction quotas. Attackers can spray unique keys to exhaust limiter memory before being limited. Use a coarse pre-auth global/IP/network limiter plus authenticated fine-grained limit, each with privacy and false-positive analysis.

Idle eviction must not reset allowance into an exploitable fresh full bucket. Options include retaining state for at least the refill horizon, cold-starting empty/partially filled, durable summaries, or accepting/documenting reset risk. Configuration changes and deployments likewise require state migration or bounded ramp.

Metrics label by bounded policy/tier/route, not raw principal. Detailed per-tenant diagnosis belongs in controlled logs/traces with access/retention policy.

### Weighted and hierarchical limits

Cost may be request count, input/output bytes, database units, model tokens, CPU estimate, recipients, rows scanned or a composite. Charge known cost before expensive work. For unknown response/work cost, reserve a safe estimate, stream with incremental budget, cap output, or reconcile accounting—never accept unbounded cost behind a unit token.

A hierarchy can require global ∧ region ∧ dependency ∧ tenant ∧ route ∧ operation allowance. Naively checking/spending sequentially can deduct an early bucket then reject later. Use one atomic/transactional decision in a common store, a reservation/rollback protocol with failure handling, or conservative preordered design whose token loss is deliberate and bounded. Partial rollback under concurrency can mint allowance if wrong.

Hierarchical fairness gives tenants guarantees/shares while enforcing global capacity. Strict equal shares waste unused capacity; shared surplus improves utilization. Borrowing needs a bounded rule like bulkheads. Weighted fair scheduling can complement rate buckets when queued durable work exists. “Premium” or emergency bypass remains finite and authenticated.

### Distributed enforcement

**Per-instance local buckets** are fast and available but multiply the configured policy. With n replicas each configured r,B, aggregate allowance can approach nr,nB. Dividing by expected n fails during autoscaling/skew and load imbalance.

**Consistent-hash ownership** routes a key to one limiter shard, bounding per-key state without central coordination on every worker. Shard failure/remapping can reset/duplicate allowance; hot keys and availability require design.

**Central atomic store/service** can enforce a global decision, but adds latency, cost and a critical dependency. Define time source, atomic script/transaction, partitions, timeout and fail-open/closed behavior. Fail-open preserves availability but can exceed protected capacity; fail-closed protects capacity but can deny healthy work.

**Leased/local quotas** allocate token blocks to instances. Fast local decisions are bounded by total issued leases, while unused tokens strand temporarily and failure/lease expiry can create overshoot or underuse. Epochs and monotonic lease rules prevent old instances spending after reassignment.

**Approximate sketches/gossip** may suit abuse detection/analytics, not hard contractual ceilings, unless error bounds are acceptable and public claims reflect them.

Any “global limit” specifies overshoot from replication lag, concurrent partitions, clock/bucket granularity, leases and in-flight already admitted calls. Managed platform throttles may be best-effort targets; inspect exact guarantees.

### Response and client behavior

HTTP commonly uses `429 Too Many Requests`. `Retry-After` can communicate a delay/date under HTTP semantics, but the server should provide it only when meaningful and the client must still honor its own deadline/backoff/jitter. A retry at the exact same time from every client causes a herd; advice can include conservative randomized behavior in documentation.

Rate-limit information fields are evolving: as of the review date, the IETF HTTPAPI RateLimit header document is an active Internet-Draft, not a final RFC. Treat fields according to the exact protocol/version adopted. Metadata is advisory; another limit or traffic change can reject the next request. Avoid exposing sensitive partition keys or precise capacity that aids abuse.

Reject before expensive parsing/body buffering where feasible, but authenticate enough to select the correct key under bounded pre-auth resources. Return stable machine-readable reason/policy identifiers and distinguish global, tenant, quota and concurrency rejection without disclosing other tenants.

Server-side sleeping is rarely right for interactive requests: it retains connections/memory and can exceed deadlines. If bounded delay fits and the runtime owns a finite scheduler, it may shape trusted internal work. Otherwise reject. Durable defer changes the contract to accepted asynchronous work and needs queue/backlog/idempotency governance.

### Deterministic token-bucket trace

The following uses integer milli-tokens and milliseconds: capacity 5 tokens, refill 2 tokens/s, cost 1 token unless specified. It performs lazy refill and atomicity only because events are sequential.

<!-- bijux-verify: {"id":"sepat-085-token-bucket","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decisions=admit,admit,admit,admit,admit,reject,admit,reject,admit\nallowed=7\nrejected=2\nremaining_tokens=0\ninterval_bound_3s=11\n","stderr":""}} -->
```python
def decide(tokens, last_ms, now_ms, cost, capacity=5000, refill_per_ms=2):
    elapsed = max(0, now_ms - last_ms)
    available = min(capacity, tokens + elapsed * refill_per_ms)
    if available < cost:
        return available, now_ms, "reject"
    return available - cost, now_ms, "admit"


tokens = 5000
last = 0
decisions = []
events = [(0, 1000)] * 6 + [(500, 1000), (1000, 2000), (3000, 5000)]

for now, cost in events:
    tokens, last, result = decide(tokens, last, now, cost)
    decisions.append(result)

allowed = sum(1 for result in decisions if result == "admit")
print("decisions=" + ",".join(decisions))
print("allowed=" + str(allowed))
print("rejected=" + str(len(decisions) - allowed))
print("remaining_tokens=" + str(tokens // 1000))
print("interval_bound_3s=" + str(5 + 2 * 3))
```

This trace proves fixed integer arithmetic only. It omits threads/atomic storage, clock resolution, keys, hierarchy, state eviction, networking, distribution, retries, payload cost, queueing, authentication, failover and actual protected capacity.

### Observability and verification

Record policy/version, bounded scope/key class, algorithm, cost, decision, remaining/estimated reset where safe, enforcement point, reject/defer reason, state-store latency/error and effective replica/shard/lease. Metrics include offered/admitted/rejected cost and requests, burst utilization, bucket saturation duration, unique-state cardinality/eviction, hierarchy decision, fairness share, distributed overshoot estimate and downstream capacity/outcomes.

Verification covers:

- initial empty/full/partial state, exact token equality and cost>B;
- zero/backward/large elapsed time, precision and overflow;
- burst B plus refill interval bound;
- fixed/sliding exact window boundaries and approximation error;
- concurrent spend cannot oversubscribe;
- weighted bytes/compute and streaming/unknown cost;
- hierarchical rejection without token loss/minting;
- key spoofing, NAT/botnet, key spray, eviction/reset and privacy;
- local n-replica multiplication, scaling, skew, shard remap, store partition and lease expiry;
- fail-open/closed behavior under limiter outage;
- `429`/advice, client jitter/deadline and no server wait leak;
- simultaneous rate, concurrency, retry, dependency slowdown and recovery load.

Use controlled/virtual time for algorithm tests and real clocks/stores/proxies for integration. Load/fault tests must prove protected-resource behavior and fairness, not merely the count of rejections. Experiments remain within isolated owned systems.

## Definitions and Notation

Let key k, token state Tₖ, capacity Bₖ, refill rate rₖ, cost c(o), last-update t₀ and current monotonic t. Let Aₖ(Δ) be admitted cost in interval Δ. Ideal token-bucket bound is Aₖ(Δ)≤Bₖ+rₖΔ. Hierarchy H(o) is the set of buckets whose policies must all authorize operation o.

Let n be independent local replicas. Without coordination/partitioned ownership, aggregate bound scales with n. Let ε capture documented distributed overshoot/approximation. A public claim should be A≤configured bound+ε under named failures, not “exact” without proof.

## Mechanisms, Invariants, or Proof Structure

**Token conservation.** Lazy refill creates at most rΔ new tokens and clamps stored tokens at B; admission consumes c. Thus an initially full ideal bucket admits at most B+rΔ cost over any Δ, assuming one atomic state and nonnegative monotonic elapsed time.

**Concurrency counterexample.** Rate bound λ does not bound in-flight L when residence W can grow. For any fixed λ>0, unbounded W produces unbounded resident work absent cancellation/concurrency limits.

**Local multiplication.** n independent full buckets each satisfy B+rΔ locally, so their sum can admit n(B+rΔ). A local configuration is not a global bound.

**Hierarchical safety.** If admission atomically spends cost from every bucket in H(o) iff all have capacity, each hierarchy constraint remains valid. Sequential nontransactional checks can violate accounting through partial spend/rollback races.

**Cardinality bound.** If new limiter keys are admitted only under a finite state quota and idle states have safe eviction/cold-start semantics, memory is bounded at that layer. Per-key traffic limiting alone cannot bound number of keys.

**No capacity proof.** A correct limiter only enforces configured trace semantics. It does not prove r/B match current service/dependency capacity, fairness objectives or safety.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation |
|---|---|---|
| fixed window | coarse quota/simple distributed counter | boundary double burst |
| sliding log | exact recent-window rule and manageable volume | state/write cost proportional to events |
| bucketed sliding counter | bounded memory with acceptable error | approximation/boundary semantics |
| token bucket | sustained rate plus explicit burst | permits bursts; distributed state needed for global rule |
| GCRA/leaky-bucket meter | conformance/spacing with burst tolerance | less intuitive; exact time arithmetic required |
| finite shaping queue | trusted work should be smoothed, not rejected | latency/memory/deadline/ownership burden |
| concurrency bulkhead | resource residence is primary risk | no temporal/fair usage bound |
| load shedding | current saturation should drive rejection | reactive, not contractual temporal share |
| durable quota ledger | billable/long-period exact usage matters | latency/transactions; does not shape instantaneous rate alone |
| managed gateway limiter | platform provides operationally mature enforcement | scope/algorithm may be best-effort or per instance/region |

## Failure Modes and Misconceptions

- **Rate equals requests/second.** Burst/window/algorithm/key/location are part of the contract.
- **Burst B means B concurrent requests.** It is stored admission allowance.
- **Average below r always passes.** Bursty traces can be rejected.
- **Token bucket is exact across replicas.** Independent buckets multiply allowance.
- **429 proves no work occurred.** Place enforcement before protected work; intermediaries may differ.
- **IP identifies a user.** NAT, proxies, mobility and botnets violate that assumption.
- **Per-tenant keys bound memory.** Attackers can create/spray tenants/keys unless key admission is bounded.
- **One request has one cost.** Payload, fan-out, compute and result sizes vary.
- **Refund on failure is fair.** Capacity was often consumed and retries can game refunds.
- **Waiting is friendlier than rejection.** It can exhaust server resources and deadline.
- **Daily quota protects instantaneous capacity.** It permits concentration unless paired with rate/burst control.
- **Rate limiting replaces bulkheads.** Slow service can accumulate concurrency.
- **Local clocks can coordinate global windows.** Cross-node skew/state semantics matter.
- **Headers guarantee next admission.** They are advisory and other policies can reject.
- **A green limiter test proves safe capacity.** Calibration/load/failure evidence is separate.

## Worked Examples

### Example 1

A token bucket has B=100 cost units and r=20/s. After idle it can admit 100 immediately. During the next 10 seconds it can admit at most another 200 ideal cost, for interval upper bound 300 if full initially. A concurrency bulkhead still caps in-flight database work.

### Example 2

A fixed window permits 1,000/minute. A client sends 1,000 at 12:00:59.9 and 1,000 at 12:01:00.1: 2,000 in 0.2 seconds. If the dependency cannot absorb that, use token/sliding semantics or lower burst; the average quota statement was insufficient.

### Example 3

Four replicas each enforce 50/s with burst 100, intended as a global tenant limit. They can jointly offer about 200/s and initial burst 400. The system either configures the intended per-replica aggregate knowingly, hashes tenant ownership, coordinates state, or leases portions of the global budget.

### Example 4

A generative endpoint charges one token per HTTP request; one request emits a million model tokens. Weighted reservation uses declared/max input plus output budget, streams only while budget remains, and caps fan-out. Billing quota and instantaneous compute rate are separate policies.

### Example 5

Global check spends one token, then the tenant bucket rejects. Repeating this drains global allowance without admitted work. A transactional multi-bucket decision or bounded reservation protocol evaluates/spends all hierarchy levels atomically; failure tests cover store timeout and rollback races.

### Example 6

An unauthenticated endpoint keys solely by source IP. A university NAT is unfairly throttled while a botnet evades the policy. Layered defense uses coarse IP/network limits before authentication and authenticated account/device/tenant policies afterward, with abuse detection and privacy safeguards.

### Example 7

Idle key state is evicted after one minute, while a full refill needs ten minutes. An attacker alternates keys to regain full buckets. Retain state through refill horizon, cold-start conservatively, or store a durable summary; bound new-key allocation at a coarser scope.

### Example 8

A server receives no token and sleeps the request for eight seconds, holding a socket/body and missing a five-second deadline. It instead returns a machine-readable throttle response with bounded advice; the client applies deadline-aware jittered backoff. Durable internal jobs use a finite scheduler rather than interactive sleeping.

### Example 9

During limiter-store partition, fail-open would overload a scarce payment provider; fail-closed would block all checkout. The service uses short-lived preleased local tokens plus a small emergency authenticated reserve, then fails closed for new standard work. The bounded overshoot and degraded contract are tested.

### Example 10

An emergency-control platform separates noncritical telemetry rates from authenticated command reserve and also applies hard concurrency/communications bulkheads. Rate advice cannot extend command validity. Attackers cannot self-label priority. Hardware-in-loop tests combine key spray, telemetry flood, network impairment and urgent commands to prove the fail-safe path.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): policy placement, hierarchy and protected capacity.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): virtual time, concurrent atomicity, distribution and load/fault testing.
- [Network Engineering](../../24-network-engineering/ROADMAP.md): traffic shaping, source identity, proxies and protocol feedback.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): denial of service, key spoofing/spray, quotas, privacy and privileged reserve.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): sharded/coordinated state, leases, overshoot and partitions.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): gateway/mesh enforcement, autoscaling, configuration and fleet telemetry.

## References

1. Turner, Jonathan S. “New Directions in Communications (or Which Way to the Information Age?).” *IEEE Communications Magazine* 24(10), 1986. (Token-bucket traffic regulation context.)
2. ITU-T. “Traffic Control and Congestion Control in B-ISDN.” Recommendation I.371. (GCRA specification lineage.)
3. Amazon Web Services. “Throttle Requests to Your HTTP APIs for Better Throughput in API Gateway.” <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-throttling.html>
4. Envoy Authors. “Local Rate Limit Filter.” <https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/local_rate_limit_filter.html>
5. NGINX Authors. “Rate Limiting with NGINX.” <https://blog.nginx.org/blog/rate-limiting-nginx>
6. Polli, Roberto, Alex Martínez Ruiz, and Darrel Miller. “RateLimit Header Fields for HTTP.” IETF HTTPAPI active Internet-Draft, work in progress. <https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/>
7. Nottingham, Mark, and Roy T. Fielding. “Additional HTTP Status Codes.” RFC 6585, Section 4 (`429`); and Fielding, Roy T., Mark Nottingham, and Julian Reschke. “HTTP Semantics.” RFC 9110, Section 10.2.3 (`Retry-After`). <https://www.rfc-editor.org/rfc/rfc6585>
8. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013.
9. Jain, Raj. *The Art of Computer Systems Performance Analysis*. Wiley, 1991.
10. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018.
11. Beyer, Betsy, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds. *Site Reliability Engineering*. O'Reilly, 2016.
12. OpenTelemetry Authors. “Semantic Conventions.” <https://opentelemetry.io/docs/specs/semconv/>

The RateLimit header document is an active Internet-Draft as of 2026-08-29 and must not be represented as a final standard. Gateway/limiter algorithms and guarantees vary by version and deployment; verify exact behavior.

## Exercises

### Exercise 1

Specify a hierarchical rate policy for an authenticated analytics API with metadata reads, searches and exports. Include global/dependency/tenant scope, weighted costs, burst, concurrency, state lifecycle, distribution and response.

### Exercise 2

A full token bucket has B=30 units, r=6 units/s. Requests cost 4 units. Compute the maximum number of complete requests admitted immediately, unused tokens, and ideal upper bound on admitted cost over 10 seconds. Explain why the cost bound does not guarantee 22 complete requests.

### Exercise 3

Five independent replicas each have r=40/s and B=80 while product documentation claims a global 40/s, burst-80 policy. Compute local aggregate limits and propose three architectures with different consistency/availability trade-offs.

### Exercise 4

Diagnose a limiter keyed by raw URL and untrusted `X-User`, using wall-clock non-atomic fixed windows per replica, unit request cost, unbounded server waiting, token refunds on every 5xx, sequential hierarchy spend, full cold-start buckets and raw-user metric labels. Redesign and define tests.

### Exercise 5

Design rate policy for a safety-critical command/telemetry system under attack and network/limiter-store failure. Include priority authority, temporal validity, distribution/overshoot, fail-safe behavior, capacity, evidence and named review.

## Answers to the Exercises

### Answer 1

Authenticate under a coarse bounded pre-auth/IP/network policy, then map to bounded tenant/plan identity and route templates. Apply an atomic hierarchy: global service/dependency budget, tenant share, and operation cost. Metadata might cost 1, search cost from bounded query complexity/estimated DB units, and export is a separately rate/quota/concurrency-limited durable workflow with byte/row maximum and status identity.

Choose r/B from measured safe dependency throughput, burst headroom and fairness; add database/compute bulkheads because rate does not bound residence. Reserve premium/operational capacity only from authenticated policy with finite caps. Bound key cardinality and retain/cold-start state so eviction/deployment cannot mint bursts.

For a fleet, hash tenant to limiter shards, use a central atomic service, or lease global tokens to replicas with documented overshoot/outage behavior. Reject before expensive work with stable machine reason and deadline-compatible advice; do not promise next success. Observe offered/admitted/rejected weighted cost, fairness, key state, overshoot and downstream utilization without raw-tenant metric labels.

### Answer 2

At cost 4, the full bucket admits floor(30/4)=7 complete requests immediately and leaves 30−28=2 tokens. The ideal admitted-cost upper bound over ten seconds from a full bucket is

\[
B+r\Delta=30+6(10)=90\text{ units}.
\]

Although floor(90/4)=22, the interval cost bound does not guarantee 22 complete requests. Arrival timing, refill granularity, prior admissions at the interval boundary, other hierarchy/concurrency limits, failures and the rule for tokens stored before the interval affect individual admission. Ninety is an upper bound on cost under stated assumptions, not promised capacity.

### Answer 3

Five independent buckets can sustain about 5×40=200 requests/s and expose initial aggregate burst 5×80=400, rather than documented 40/s and 80.

Architecture one: consistent-hash each tenant/global key to one limiter shard; low per-decision coordination, but hot shard, remap/reset and shard availability need fencing/replication. Architecture two: central linearizable atomic bucket; closest exact global semantics, but every decision pays store/service latency and partitions require fail-open/closed policy. Architecture three: a coordinator leases portions of the global rate/burst to replicas; fast local admission and bounded issued-token sum, but unused capacity strands and failure/lease expiry creates quantified overshoot/underuse. An approximate gossip design is a fourth option only if a documented error bound is acceptable.

### Answer 4

Raw URL and untrusted identity enable key spray/evasion/cardinality exhaustion. Wall clock/reset windows create jumps and boundary bursts; non-atomic updates overspend; per-replica state multiplies policy. Unit cost ignores expensive payloads. Waiting retains resources. Blanket refund can be gamed and ignores consumed work. Sequential hierarchy loses/mints tokens under rollback races. Cold starts mint allowance. Raw-user labels expose data and explode metrics.

Authenticate/normalize bounded keys and route templates; add coarse new-key/pre-auth caps. Use monotonic fixed-point token/GCRA/sliding semantics with atomic state and exact equality; weighted known/reserved/incremental costs; finite rejection/defer; global distribution design; transactional multi-bucket decision; conservative restart/eviction; and no load-token refund after consumed work. Add concurrency bulkheads/deadlines and privacy-safe telemetry.

Tests cover exact algorithm/window boundaries, clock back/overflow, concurrent spend, weighted large/streaming requests, hierarchy store failures, key spoof/NAT/key spray/eviction, replica multiplication/scaling/remap/partition/lease expiry, cold deployment, refund abuse, queue/deadline, response metadata/client herd and actual downstream load/fairness.

### Answer 5

Separate authenticated command, emergency reserve, routine control and telemetry policies, plus hard communications/controller/actuator concurrency bulkheads. Command eligibility derives from cryptographic principal, authorized safety operation, device generation/fence, sequence and validity deadline—not a client priority flag. Telemetry source/device/tenant rate and byte cost cannot consume command capacity.

Use local leased command tokens whose globally issued sum and expiry bound overshoot during limiter-store/network failure. Standard traffic fails closed or degrades when authority is unknown; a small hazard-approved emergency reserve has replay protection, audit and finite capacity. No rate advice extends command validity. Cancellation/rejection before issue has no effect; issued actuation remains reconciled by durable identity.

Threats include distributed key evasion, forged priority, state-store denial, replay, clock manipulation, lease reuse and telemetry floods. Evidence includes formal timed quota/resource/effect model, overshoot proof, worst-case schedulability/capacity, model checking where feasible, hardware-in-loop burst/failure/failover tests, clock/network/store/power faults, adversarial/security tests, protected audit and fail-safe/recovery drills.

Approval requires named domain safety, controls, hardware, communications/real-time, distributed systems, security, reliability/operations, human-factors and regulatory reviewers with traceable hazards and acceptance criteria.
