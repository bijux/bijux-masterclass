# Reference Answers — Module 07: Module 07 exercise answers — Caching, Freshness, and Invalidation

Read after attempting all twelve Caching, Freshness, and Invalidation exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Design a safe cache key for project metadata.

Include tenant or authorization partition, resource ID, durable resource version/ETag, API/representation version, and any projection or locale that changes the value. Enforce authorization before reuse unless the cached projection is proven safe.

## 2. Why are versioned keys robust against invalidation loss?

After a durable version increment, new reads use a new key, so the old entry is unreachable even if cleanup fails. Storage may retain stale entries until eviction, but correctness does not depend on immediate deletion.

## 3. When is a 60-second TTL unacceptable?

When any change within 60 seconds can create a forbidden state, such as revoked access still being granted. The tolerated stale behavior, not desired hit rate, determines TTL.

## 4. What should happen when a fill times out?

Do not publish a value or negative entry. Remove the in-flight marker, propagate the classified error, release waiters, and allow a later request to retry under reliability/admission policy.

## 5. Why can random TTL jitter be wrong?

Jitter can extend or shorten freshness beyond a strict policy. Use it only within an allowed stale interval and record the actual expiry. It is not a substitute for single-flight.

## 6. How can negative caching aid enumeration attacks?

Attackers can generate many unique missing IDs, filling the cache and observing timing differences. Bound keys, use short TTL, preserve existence concealment, and apply abuse controls.

## 7. A cache has 95% hit ratio. Miss cost is 100 ms, hit cost 1 ms. Estimate average service time.

`0.95×1 + 0.05×100 = 5.95 ms`. This average hides miss bursts and tail behavior; the origin must still handle miss concurrency.

## 8. What is stale-while-revalidate and when is it unsafe?

A stale value is served while one request refreshes it. It is unsafe when stale data can violate authorization, financial, or durable-state requirements. It requires explicit stale bounds and single-flight.

## 9. Why not cache list-run query results first?

Keys include tenant, filters, cursor, high-water, page size, and policy; mutations invalidate many combinations; cardinality can be high. Optimize SQL and response path first unless evidence shows reusable hot queries.

## 10. How does cache failure interact with admission?

Falling back every miss to origin can overload PostgreSQL. Origin calls need bounded concurrency and overload behavior. The cache outage is an expected dependency mode, not permission to bypass controls.

## 11. What metrics describe a cache better than hit ratio alone?

Hit/miss/stale/fill/fill-error counts, coalesced waiters, origin calls, origin latency, eviction reason, entries, bytes, miss burst, and latency/resource effect on critical workloads.

## 12. A cached value is correct but its response ETag differs from origin. Accept?

No. The selected public representation metadata is part of correctness. Cache the representation/validator consistently or regenerate both from the same durable version and representation policy.
