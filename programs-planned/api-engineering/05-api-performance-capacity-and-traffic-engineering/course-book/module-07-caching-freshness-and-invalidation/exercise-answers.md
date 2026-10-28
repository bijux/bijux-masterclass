# Worked Answers — Module 07: Caching, Freshness, and Invalidation

Use these solutions to audit your reasoning for **Caching, Freshness, and Invalidation**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Design a safe cache key for project metadata.

Include tenant or authorization partition, resource ID, durable resource version/ETag, API/representation version, and any projection or locale that changes the value. Enforce authorization before reuse unless the cached projection is proven safe.

The chapter’s decisive distinction is this: A process-local cache is fast and simple but inconsistent across instances after mutation unless keys are immutable/versioned or invalidation is coordinated. A shared cache centralizes reuse but becomes a dependency and contention point.

## 2. Why are versioned keys robust against invalidation loss?

After a durable version increment, new reads use a new key, so the old entry is unreachable even if cleanup fails. Storage may retain stale entries until eviction, but correctness does not depend on immediate deletion.

In the cumulative capstone, the rule becomes concrete: A distributed cache outage can create an origin stampede. Circuit and admission policies from Course 4 and Module 6 apply. The cache is an optimization, not a new source of business truth.

## 3. When is a 60-second TTL unacceptable?

When any change within 60 seconds can create a forbidden state, such as revoked access still being granted. The tolerated stale behavior, not desired hit rate, determines TTL.

A useful way to reason about the boundary is: For owner permissions, stale access may be unacceptable. A “fast” cache that grants revoked access for 60 seconds violates security profile 1.0. The policy catalogue records maximum staleness and forbidden stale states.

## 4. What should happen when a fill times out?

Do not publish a value or negative entry. Remove the in-flight marker, propagate the classified error, release waiters, and allow a later request to retry under reliability/admission policy.

The implementation consequence is: A distributed cache outage can create an origin stampede. Circuit and admission policies from Course 4 and Module 6 apply. The cache is an optimization, not a new source of business truth.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 5. Why can random TTL jitter be wrong?

Jitter can extend or shorten freshness beyond a strict policy. Use it only within an allowed stale interval and record the actual expiry. It is not a substitute for single-flight.

The important nuance is: For owner permissions, stale access may be unacceptable. A “fast” cache that grants revoked access for 60 seconds violates security profile 1.0. The policy catalogue records maximum staleness and forbidden stale states.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 6. How can negative caching aid enumeration attacks?

Attackers can generate many unique missing IDs, filling the cache and observing timing differences. Bound keys, use short TTL, preserve existence concealment, and apply abuse controls.

Under concurrency or failure, the distinction becomes: A process-local cache is fast and simple but inconsistent across instances after mutation unless keys are immutable/versioned or invalidation is coordinated. A shared cache centralizes reuse but becomes a dependency and contention point.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 7. A cache has 95% hit ratio. Miss cost is 100 ms, hit cost 1 ms. Estimate average service time.

`0.95×1 + 0.05×100 = 5.95 ms`. This average hides miss bursts and tail behavior; the origin must still handle miss concurrency.

The design remains honest only if: A distributed cache outage can create an origin stampede. Circuit and admission policies from Course 4 and Module 6 apply. The cache is an optimization, not a new source of business truth.

**Evidence.** Vary tenant, principal, representation, source version, mutation, concurrent miss, and cache failure while asserting correctness before hit rate.

## 8. What is stale-while-revalidate and when is it unsafe?

A stale value is served while one request refreshes it. It is unsafe when stale data can violate authorization, financial, or durable-state requirements. It requires explicit stale bounds and single-flight.

The consumer-facing consequence is: For owner permissions, stale access may be unacceptable. A “fast” cache that grants revoked access for 60 seconds violates security profile 1.0. The policy catalogue records maximum staleness and forbidden stale states.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 9. Why not cache list-run query results first?

Keys include tenant, filters, cursor, high-water, page size, and policy; mutations invalidate many combinations; cardinality can be high. Optimize SQL and response path first unless evidence shows reusable hot queries.

The operational consequence is: A process-local cache is fast and simple but inconsistent across instances after mutation unless keys are immutable/versioned or invalidation is coordinated. A shared cache centralizes reuse but becomes a dependency and contention point.

**Evidence.** Vary tenant, principal, representation, source version, mutation, concurrent miss, and cache failure while asserting correctness before hit rate.

## 10. How does cache failure interact with admission?

Falling back every miss to origin can overload PostgreSQL. Origin calls need bounded concurrency and overload behavior. The cache outage is an expected dependency mode, not permission to bypass controls.

The strongest engineering interpretation is: A distributed cache outage can create an origin stampede. Circuit and admission policies from Course 4 and Module 6 apply. The cache is an optimization, not a new source of business truth.

**Evidence.** Vary tenant, principal, representation, source version, mutation, concurrent miss, and cache failure while asserting correctness before hit rate.

## 11. What metrics describe a cache better than hit ratio alone?

Hit/miss/stale/fill/fill-error counts, coalesced waiters, origin calls, origin latency, eviction reason, entries, bytes, miss burst, and latency/resource effect on critical workloads.

The defect-oriented view is: For owner permissions, stale access may be unacceptable. A “fast” cache that grants revoked access for 60 seconds violates security profile 1.0. The policy catalogue records maximum staleness and forbidden stale states.

**Evidence.** Vary tenant, principal, representation, source version, mutation, concurrent miss, and cache failure while asserting correctness before hit rate.

## 12. A cached value is correct but its response ETag differs from origin. Accept?

No. The selected public representation metadata is part of correctness. Cache the representation/validator consistently or regenerate both from the same durable version and representation policy.

Across the Python and TypeScript tracks, the invariant is: A process-local cache is fast and simple but inconsistent across instances after mutation unless keys are immutable/versioned or invalidation is coordinated. A shared cache centralizes reuse but becomes a dependency and contention point.

**Evidence.** Vary tenant, principal, representation, source version, mutation, concurrent miss, and cache failure while asserting correctness before hit rate.
