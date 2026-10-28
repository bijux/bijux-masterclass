# Module 07 — Caching, Freshness, and Invalidation

> **Program stage:** Course 5 of 10 — Sustain the promise under pressure.

> **Central question:** Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure?

## Where this module fits

Module 06 produced **Implement bounded admission, per-operation limits, queue accounting, permit release, and recovery after pressure**. This module extends that result by asking: **Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure?**

The new capstone increment is **Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics**. It becomes the prerequisite for **Traffic Shaping, Quotas, and Load Shedding**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish HTTP, process-local, shared application, database, and client caches.
- Classify values by mutability and authorization sensitivity.
- Define complete cache keys and value envelopes.
- Choose freshness and stale behavior explicitly.
- Implement invalidation from durable change rather than best-effort route code.
- Prevent cross-tenant and cross-policy reuse.
- Bound entries, bytes, and concurrent fills.
- Control cache stampedes and failure amplification.
- Measure hit, miss, fill, stale, eviction, and origin cost.
- Reject caches that improve latency while worsening correctness or tail load.

## Capstone increment

Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics.

## Core performance model

### 1. Cache is a stored answer to a question


Define the question completely. “Project 123” is not enough if the answer depends on tenant, principal permissions, API version, locale, representation encoding, projection, or security profile.

A cache entry contains more than a value:

```text
key
value
created time
fresh-until time
version/validator
authorization context
size
origin identity
negative/positive classification
```

The cache policy decides whether an answer remains valid for a later question. Omitting one selection dimension creates wrong reuse.


### 2. Cache layers are not interchangeable


The system can reuse work at several layers:

- client or HTTP private cache;
- shared HTTP intermediary;
- process-local application cache;
- distributed application cache;
- PostgreSQL buffer cache;
- operating-system page cache;
- storage or CDN cache.

Each has different visibility, failure, invalidation, and security semantics. Course 3 and Module 3 already constrain HTTP caching. Module 7 focuses on application reuse while preserving those boundaries.

A process-local cache is fast and simple but inconsistent across instances after mutation unless keys are immutable/versioned or invalidation is coordinated. A shared cache centralizes reuse but becomes a dependency and contention point.


### 3. Classify before caching


The capstone catalogue uses five classes:

1. **immutable content-addressed artifact metadata** — key includes checksum/version; long reuse possible;
2. **versioned project metadata** — key includes owner and version/ETag; old entries become unreachable after version change;
3. **mutable authorization decisions** — generally short-lived or uncached because roles/revocation change;
4. **list/query results** — high invalidation complexity and key cardinality; cache only with strong evidence;
5. **negative lookups** — can reduce repeated misses but may hide newly created data and amplify enumeration.

Not every expensive operation should be cached. If origin cost is low and mutation rate high, the cache can add more complexity than value.


### 4. Authorization-safe keys


At minimum, a protected object cache key may include:

```text
tenant_id
principal or policy partition
resource_id
resource_version
representation/profile version
```

If the cached value contains only tenant-neutral public data after a prior authorization check, the authorization decision may remain outside the cache. That must be proven, not assumed.

Never key solely by attacker-controlled identifiers and then return the value before policy enforcement. The safest pattern is authorization-aware query or policy first, then cache a projection partitioned by the required security context.


### 5. Freshness and stale policy


Freshness is a correctness budget. A TTL of 60 seconds means a value may be reused for that interval even if the origin changes, unless invalidation/versioning prevents it.

Options include:

- immutable/versioned keys: stale entries remain but are unreachable;
- explicit invalidation after durable commit;
- short TTL and validation;
- stale-while-revalidate for values where bounded stale reuse is acceptable;
- stale-if-error for carefully selected non-sensitive data.

For owner permissions, stale access may be unacceptable. A “fast” cache that grants revoked access for 60 seconds violates security profile 1.0. The policy catalogue records maximum staleness and forbidden stale states.


### 6. Invalidation from durable truth


Deleting a cache key in a route handler after a database update is vulnerable to process crash between commit and invalidation. Better strategies:

- versioned keys derived from durable row version;
- transactional outbox event that drives invalidation;
- read-through validation against a durable validator;
- short TTL where residual stale risk is accepted.

Course 2’s transactional outbox provides a durable mechanism. The capstone demonstrates versioned project metadata keys and uses an invalidation event as a secondary cleanup, not the only correctness mechanism.


### 7. Stampedes and single-flight


When a popular key expires, many concurrent misses can call the origin. This cache stampede raises database demand precisely when the cache is least useful.

Single-flight coalesces concurrent fills for the same complete key:

```text
first miss → owns fill
other misses → await same fill
fill succeeds → publish once
fill fails → all receive failure; no poisoned entry
```

Bound total concurrent fills and per-key wait. Single-flight does not justify an unbounded waiter list. Add jitter to TTLs only when it does not violate a strict freshness boundary.


### 8. Negative caching


Caching “not found” can reduce repeated misses, but it has risks:

- newly created resource remains hidden until expiry;
- ownership/existence concealment can be broken if negative states differ;
- attacker enumeration fills cache with arbitrary keys;
- transient origin failure may be miscached as absence.

Use short TTLs, bounded key spaces, and the same public error policy. Cache only authoritative absence, not timeout or 500. Partition by tenant/policy where needed.


### 9. Capacity and observability


A cache must be bounded by entries and preferably bytes. LRU-like eviction is a policy, not a guarantee of optimality. Large values can evict many useful entries. The cache reports:

- hit, miss, stale, fill, fill error;
- fill coalescing;
- eviction reason;
- entries and estimated bytes;
- origin latency saved;
- origin load under miss burst.

Hit ratio alone is misleading. A 99% hit ratio can coexist with a catastrophic 1% miss path if misses arrive in a burst or are the most expensive keys.


### 10. Cache failure policy


An application cache can fail open to origin, fail closed, or serve stale depending on data class. For metadata reads, origin fallback may be safe if admission protects the database. For security decisions, stale reuse may be forbidden and origin failure may require denial.

A distributed cache outage can create an origin stampede. Circuit and admission policies from Course 4 and Module 6 apply. The cache is an optimization, not a new source of business truth.

## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Catalogue before code | Every cached class has key, authorization, freshness, invalidation, bounds, and failure policy. | Cache library defaults define semantics. | Cache catalogue |
| Complete key | All value- and policy-selecting dimensions are key-bound. | Wrong representation or tenant reused. | Cross-context vectors |
| Security before reuse | Authorization or safe partition is enforced before returning protected value. | Fast cross-tenant leak. | Security tests |
| Staleness explicit | Maximum stale state and forbidden stale outcomes are documented. | TTL is chosen by intuition. | Policy review |
| Durable invalidation | Correctness does not depend on best-effort post-commit deletion. | Crash leaves stale grants/data. | Version/outbox proof |
| Fill bounded | Concurrent fills and waiters are capped and cancel-safe. | Stampede or waiter leak. | Burst tests |
| Failure not absence | Timeout/500 is never cached as authoritative not-found. | Outage becomes false 404. | Negative-cache vectors |
| Capacity bounded | Entries/bytes and eviction are observable. | Cache becomes memory leak. | Capacity tests |

## Worked failures

### Case 1 — The resource-ID-only key

**Initial condition.** Project metadata is cached under `project:{id}` after one authorized request.

**Analysis.** Another tenant guessing the same ID can hit the cached value before authorization.

**Correct response.** Enforce authorization first and partition key/value by tenant/policy, or cache only a safe tenant-neutral projection.

**Lesson.** Cache keys are security boundaries.

### Case 2 — The route invalidation crash

**Initial condition.** Database commit succeeds, process crashes before deleting the old cache entry.

**Analysis.** Best-effort invalidation is lost and stale data remains reachable.

**Correct response.** Use row-version keying or durable outbox invalidation; route deletion is cleanup only.

**Lesson.** Invalidation must follow durable truth.

### Case 3 — The 99% hit ratio outage

**Initial condition.** Cache expires a hot key; 2,000 concurrent misses hit PostgreSQL and exhaust the pool.

**Analysis.** Aggregate hit ratio hid synchronized miss behavior.

**Correct response.** Use single-flight, bounded fills, staggered freshness where allowed, and origin admission.

**Lesson.** Miss concurrency matters more than average hit ratio.

### Case 4 — The negative timeout

**Initial condition.** A database timeout is cached as not-found for five minutes.

**Analysis.** A transient dependency failure becomes durable false absence.

**Correct response.** Cache only authoritative absence; errors follow reliability policy.

**Lesson.** Error classification precedes caching.

## Python implementation

### Mechanism

The Python cache module provides an injected-clock bounded TTL/LRU store, authorization-aware keys, estimated byte accounting, and an async single-flight coordinator.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/cache.py`
- `capstone/tracks/python-fastapi/src/api_performance/singleflight.py`
- `capstone/tracks/python-fastapi/tests_performance/test_cache_singleflight.py`

### Focused example

```python
from api_performance.cache import AuthorizedCacheKey

key = AuthorizedCacheKey(
    tenant_id="tenant-a",
    policy_partition="owner",
    resource_type="project",
    resource_id="project-7",
    version="12",
    representation="api-1.2",
)
assert "tenant-a" in key.canonical
```

The canonical key uses length-prefixed fields rather than ambiguous delimiter concatenation. Values carry expiry and estimated size. The clock is injected, so expiry tests do not sleep.

### Python-specific failure to avoid

Do not hold an asyncio lock while calling the origin; it serializes unrelated keys. Lock only cache/in-flight state transitions and await the fill outside the global lock.

## TypeScript implementation

### Mechanism

The TypeScript cache uses a Map-based bounded store with explicit recency updates, bigint-safe byte counters, and abort-aware single-flight promises.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/cache.ts`
- `capstone/tracks/typescript-fastify/src/performance/singleflight.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/cache-singleflight.test.mjs`

### Focused example

```typescript
const key = createAuthorizedCacheKey({
  tenantId: "tenant-a",
  policyPartition: "owner",
  resourceType: "project",
  resourceId: "project-7",
  version: "12",
  representation: "api-1.2",
});
if (!key.canonical.includes("tenant-a")) throw new Error("bad key");
```

The key encoder rejects empty identity fields and prototype-sensitive objects. Single-flight removes settled promises in `finally` so failed fills do not poison later requests.

### TypeScript-specific failure to avoid

A plain JavaScript object is not a safe unbounded cache: inherited keys, accidental coercion, and no eviction semantics. Use Map and explicit bounds.

## Cross-language invariant

Both tracks agree on canonical keys, expiry boundaries, LRU order for deterministic vectors, negative-cache classification, and single-flight origin-call counts.

## Failure patterns

- **Product-first design.** Redis or memory cache is chosen before semantics. **Decisive check:** cache catalogue.
- **Incomplete key.** Tenant, version, projection, or encoding omitted. **Decisive check:** cross-context vector.
- **Best-effort invalidation.** Crash separates commit and deletion. **Decisive check:** versioned-key proof.
- **Stampede.** Concurrent misses multiply origin calls. **Decisive check:** single-flight count.
- **Negative error.** Timeout cached as absence. **Decisive check:** origin-classification vector.
- **Hit-ratio vanity.** Average hits hide expensive miss burst. **Decisive check:** origin load and tail report.

## Evidence and design review

Before accepting the module increment, answer:

1. What exact question does each cache key answer?
2. Can a caller with different policy context reuse the value?
3. What is the maximum permitted stale state?
4. Which durable event or version makes old data unreachable?
5. How many origin fills can run concurrently globally and per key?
6. What happens to database demand when the cache is unavailable?

## Module synthesis

You are ready to leave this module when you can **distinguish HTTP, process-local, shared application, database, and client caches, classify values by mutability and authorization sensitivity, and define complete cache keys and value envelopes** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Inject origin timeout and ensure it is not cached as not-found** and requiring the following oracle: **cross-tenant value is never reused; 100 concurrent misses produce one bounded origin fill per key; failed fill leaves no poisoned entry; post-commit version change makes old entry unreachable.**

The cumulative platform now includes **Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Traffic Shaping, Quotas, and Load Shedding](../module-08-traffic-shaping-quotas-and-load-shedding/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
