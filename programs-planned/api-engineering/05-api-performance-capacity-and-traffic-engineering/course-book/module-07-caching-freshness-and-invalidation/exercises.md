# Exercises — Module 07: Caching, Freshness, and Invalidation

Work through all twelve problems before opening the answers. In **Caching, Freshness, and Invalidation**, every response must settle this question: **Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure?** Each solution must survive delay, duplication, version skew, hostile input, or partial failure where relevant; happy-path intuition alone earns no credit.

## 1. Design a safe cache key for project metadata.


## 2. Why are versioned keys robust against invalidation loss?


## 3. When is a 60-second TTL unacceptable?


## 4. What should happen when a fill times out?


## 5. Why can random TTL jitter be wrong?


## 6. How can negative caching aid enumeration attacks?


## 7. A cache has 95% hit ratio. Miss cost is 100 ms, hit cost 1 ms. Estimate average service time.


## 8. What is stale-while-revalidate and when is it unsafe?


## 9. Why not cache list-run query results first?


## 10. How does cache failure interact with admission?


## 11. What metrics describe a cache better than hit ratio alone?


## 12. A cached value is correct but its response ETag differs from origin. Accept?


## Submission format

Submit Module 07 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
