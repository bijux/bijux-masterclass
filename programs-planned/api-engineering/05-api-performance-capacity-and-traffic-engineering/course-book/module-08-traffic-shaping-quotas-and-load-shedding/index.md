# Module 08 — Traffic Shaping, Quotas, and Load Shedding

> **Program stage:** Course 5 of 10 — Sustain the promise under pressure.

> **Central question:** How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes?

## Where this module fits

Module 07 produced **Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics**. This module extends that result by asking: **How should quotas, priorities, cost budgets, and load shedding preserve fairness and truthful 429/503 outcomes?**

The new capstone increment is **Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations**. It becomes the prerequisite for **Capacity Modeling and Scaling Decisions**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish rate limits, quotas, concurrency limits, and capacity admission.
- Choose dimensions that reflect resource cost.
- Implement deterministic token-bucket arithmetic.
- Bind policy to principal, tenant, operation, and service class.
- Preserve fairness under skewed traffic.
- Calculate truthful retry guidance.
- Define a load-shedding ladder before overload.
- Protect admitted work and critical control operations.
- Measure offered, admitted, rejected, and completed traffic by reason.
- State local versus distributed enforcement limitations.

## Capstone increment

Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations.

## Core performance model

### 1. Four different controls


A **rate limit** controls how quickly work may arrive over a short horizon. A **quota** controls total consumption over a longer horizon. A **concurrency limit** bounds simultaneous active work. **Capacity admission** rejects when current downstream conditions cannot safely accept more work.

Examples:

```text
metadata reads:       100 tokens/s, burst 200
analysis submissions: 10 cost units/s, burst 20
active uploads:       4 per tenant
monthly storage:      2 TiB per tenant
global job depth:     50,000 durable jobs
```

These controls answer different questions. A client can be within rate but above concurrency, or below both but rejected because storage is unavailable.


### 2. Cost-weighted traffic


One request is not one unit of demand. Assign stable cost units from measured resource demand:

- project read: 1 unit;
- run list page: 2 units;
- analysis submission: 5 units;
- upload MiB: 1 unit per declared chunk/size band;
- artifact stream: concurrency permit plus byte quota.

Cost weights are policy approximations and must be versioned. Do not set them solely from intuition; use Modules 3–7 evidence. A large request cannot lie about its cost: size-dependent costs are charged incrementally or reserved from validated content length and adjusted safely.


### 3. Token bucket


A token bucket has capacity `B`, refill rate `r`, and current tokens. Time adds tokens up to capacity; each admitted action spends cost `c`.

```text
tokens(t) = min(B, tokens(t0) + r × (t - t0))
admit when tokens >= c
```

The capstone uses integer microtokens and integer nanoseconds to avoid cross-language floating-point drift. It computes a conservative wait time for the missing tokens.

Burst capacity permits short spikes while rate controls long-run average. A huge burst merely postpones overload; choose it from queue and dependency headroom.


### 4. Policy dimensions and cardinality


A decision may use:

```text
principal
tenant
operation
service class
cost
global state
```

Do not create unbounded limiter state from arbitrary attacker keys. Authenticate before principal-based allocation when possible, bound inactive entries, and retain an IP or anonymous edge policy separately.

Global, tenant, and principal buckets can all apply. Admission succeeds only when all required budgets can be consumed atomically. A rollback mechanism returns reservations when a later policy layer rejects before work begins.


### 5. Fairness and borrowing


Equal per-tenant limits are simple but may waste capacity. Weighted fairness may reflect purchased service tiers or workload value. Borrowing unused capacity can improve utilization but must not eliminate a minimum share for others.

A practical policy:

1. reserve a minimum tenant share;
2. apply global cap;
3. allow bounded borrowing when no protected demand waits;
4. age waiting work or bound wait;
5. report policy class, not sensitive tenant identity, in global metrics.

Fairness is evaluated through admission and completion distributions under skew, not by reading configuration.


### 6. Retry guidance


A rate limiter can compute when enough tokens will refill for a cost. A concurrency or downstream-capacity rejection may not know a precise recovery time. `Retry-After` should be:

- a conservative delay when token refill determines recovery;
- omitted or coarse when recovery depends on unknown dependency state;
- consistent with idempotency and retry budgets from Courses 2 and 4.

All clients retrying at the exact same second can create a herd. Client guidance should include jitter behavior in SDKs or documentation while the server remains truthful.


### 7. Load-shedding ladder


Define overload actions before the incident. Example:

1. reject optional diagnostics and expensive query variants;
2. reduce maximum non-critical page size within the public contract only if clients requested a lower acceptable size—never silently truncate;
3. deny new large uploads when storage/stream permits are exhausted;
4. reject new analysis submissions before durable acceptance;
5. preserve run status, cancellation, health, and already admitted artifact delivery;
6. enter explicit service-unavailable mode if durable dependencies cannot preserve correctness.

The ladder cannot violate the public contract. “Return less data with 200” is not graceful degradation unless contract semantics permit it.


### 8. Priority inversion and critical controls


A large stream can occupy all worker or connection capacity while a cancellation or status request waits. Reserve small, bounded control-plane capacity for:

- cancellation;
- run status;
- readiness/health;
- operational reconciliation;
- security revocation paths where applicable.

Reservation must be modest and measured; excessive reserved idle capacity lowers utilization. Ensure high-priority work does not depend on a lower-priority queue holding a lock or connection, a form of priority inversion.


### 9. Distributed enforcement boundary


An in-process token bucket is exact only for one process. With `N` independent instances, a per-instance limit can admit approximately `N` times the intended global rate and distribution may be uneven.

Options include:

- divide capacity conservatively per instance;
- route a tenant consistently;
- use a shared atomic limiter;
- enforce global quotas in durable storage;
- accept bounded approximation and monitor aggregate behavior.

Course 5 implements deterministic local policy and documents the distributed contract. It does not pretend that a local Map or dictionary is a global limiter.


### 10. Traffic evidence


A traffic report includes:

```text
offered cost units
admitted cost units
rejected cost units by reason
active concurrency
queue wait
completed outcomes
tenant/service-class distribution
resource utilization
```

Requests per second alone can improve while cost or bytes explode. Compare admitted work with completed work and service objectives. Rejection is acceptable only when policy selects it and the response is correct.

## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Control type explicit | Rate, quota, concurrency, and capacity decisions are separate. | One RPS number hides resource use. | Traffic policy schema |
| Cost versioned | Operation/size weights derive from evidence and carry profile version. | Policy changes silently alter capacity. | Cost catalogue |
| Atomic multi-budget decision | Global/tenant/principal reservations cannot partially leak. | Rejected request consumes some budgets. | State transition tests |
| State bounded | Limiter keys expire/evict under controlled rules. | Arbitrary identities create memory exhaustion. | Capacity tests |
| Retry truthful | Guidance derives from known refill or declared uncertainty. | Clients synchronize on invented delay. | Retry vectors |
| Critical journeys protected | Shedding order preserves admitted and control work. | Overload disables cancellation/status. | Mixed workload |
| Fairness measured | Skewed tenants cannot monopolize capacity or be starved silently. | Configuration is called fair without evidence. | Distribution report |
| Distributed scope declared | Local limiter is not called global. | Deployment multiplies limits unexpectedly. | Evidence boundary |

## Worked failures

### Case 1 — The one-RPS policy

**Initial condition.** All operations cost one token. A 1-byte metadata read and 5 GiB upload are treated equally.

**Analysis.** Request count is not resource demand. Large streams consume bandwidth, storage, memory, and concurrency far longer.

**Correct response.** Use operation and size/concurrency dimensions derived from measured service demand.

**Lesson.** Traffic units must reflect the limiting resource.

### Case 2 — The partial reservation leak

**Initial condition.** Global bucket is charged, then tenant bucket rejects. Global tokens are not returned.

**Analysis.** Repeated rejected requests drain global capacity and deny others.

**Correct response.** Evaluate atomically or reserve/rollback exactly on pre-admission failure.

**Lesson.** Multi-layer policy is a state machine.

### Case 3 — The synchronized Retry-After

**Initial condition.** Every rejected client receives `Retry-After: 1` and retries exactly one second later.

**Analysis.** The server creates a periodic herd.

**Correct response.** Return truthful minimum guidance and ensure clients apply bounded jitter; consider token-specific wait calculation.

**Lesson.** Retry policy is part of traffic control.

### Case 4 — The silent truncation

**Initial condition.** During overload, list endpoints return half the requested page with 200 but omit pagination metadata changes.

**Analysis.** The public response meaning changed to make latency look better.

**Correct response.** Reject, honor documented page semantics, or use a contract-versioned degradation option.

**Lesson.** Load shedding cannot invent a new API.

## Python implementation

### Mechanism

The Python traffic module implements integer-microtoken buckets, atomic multi-budget reservations, TTL-bounded key state, cost catalogues, and a deterministic shedding policy.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/traffic.py`
- `capstone/tracks/python-fastapi/src/api_performance/shedding.py`
- `capstone/tracks/python-fastapi/tests_performance/test_traffic_shedding.py`

### Focused example

```python
from api_performance.traffic import TokenBucket

bucket = TokenBucket(capacity=10_000_000, refill_per_second=2_000_000)
decision = bucket.consume(now_ns=0, cost=5_000_000)
assert decision.allowed
assert decision.remaining == 5_000_000
```

Values are integer microtokens. The injected monotonic timestamp makes refill deterministic. A reservation group commits all budgets or rolls back consumed tokens before application work starts.

### Python-specific failure to avoid

Protect shared bucket state with a bounded critical section, but do not hold the lock while executing the request. Use monotonic time and prevent backward clock input from minting tokens.

## TypeScript implementation

### Mechanism

The TypeScript implementation uses bigint microtokens/nanoseconds and explicit reservation objects. It avoids floating-point refill drift.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/traffic.ts`
- `capstone/tracks/typescript-fastify/src/performance/shedding.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/traffic-shedding.test.mjs`

### Focused example

```typescript
const bucket = new TokenBucket({
  capacity: 10_000_000n,
  refillPerSecond: 2_000_000n,
});
const decision = bucket.consume(0n, 5_000_000n);
if (!decision.allowed || decision.remaining !== 5_000_000n) {
  throw new Error("unexpected decision");
}
```

Bigint arithmetic gives identical boundary decisions. Serialized metrics convert microtokens to decimal strings or scaled units explicitly.

### TypeScript-specific failure to avoid

Do not mix bigint and number in arithmetic. Avoid timer callbacks as the source of refill; calculate refill lazily from monotonic elapsed time to prevent drift and timer storms.

## Cross-language invariant

Shared vectors assert identical allow/deny decisions, remaining budgets, wait estimates, rollback behavior, key eviction, and shedding-stage selection.

## Failure patterns

- **RPS monoculture.** Different cost operations share one unit. **Decisive check:** cost/service-demand catalogue.
- **Limiter state attack.** Unbounded identity keys consume memory. **Decisive check:** TTL/capacity proof.
- **Partial budget leak.** One layer charges before another rejects. **Decisive check:** atomic reservation test.
- **Priority starvation.** Critical class consumes all capacity forever. **Decisive check:** aging/minimum-share evidence.
- **Local-global confusion.** Per-process bucket is called tenant-global. **Decisive check:** deployment scope.
- **Semantic shedding.** Response body is silently changed. **Decisive check:** contract conformance.

## Evidence and design review

Before accepting the module increment, answer:

1. Which resource does each cost unit approximate?
2. Can a rejected request leak any reservation?
3. How are inactive limiter keys bounded?
4. Which journeys remain available at each shedding stage?
5. Can retry guidance be derived from known state?
6. What aggregate rate can multiple independent instances admit?

## Module synthesis

You are ready to leave this module when you can **distinguish rate limits, quotas, concurrency limits, and capacity admission, choose dimensions that reflect resource cost, and implement deterministic token-bucket arithmetic** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **offered/admitted/rejected/completed cost reconciles; no partial token leak occurs; tenant B retains the declared minimum service; status and cancellation remain available.**

The cumulative platform now includes **Implement multi-dimensional fixed-point budgets, tenant isolation, staged shedding, and rollback of partial reservations**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Capacity Modeling and Scaling Decisions](../module-09-capacity-modeling-and-scaling-decisions/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
