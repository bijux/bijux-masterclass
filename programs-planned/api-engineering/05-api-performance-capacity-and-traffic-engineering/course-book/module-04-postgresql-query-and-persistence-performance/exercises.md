# Exercises — Module 04: PostgreSQL Query and Persistence Performance

Work through all twelve problems before opening the answers. In **PostgreSQL Query and Persistence Performance**, every response must settle this question: **Which query plan, index, lock, pool, or pagination behavior is the first persistence bottleneck for a declared workload?** For every answer, separate the authoritative boundary from convenient diagnostics, then explain which failing experiment would force you to revise the design.

## 1. Propose an index for owner, status, descending created_at/id pagination.


## 2. Why can an index-only scan still read heap pages?


## 3. Actual rows are 100,000 while estimated rows are 100. What does that suggest?


## 4. A query executes in 8 ms but request span shows 240 ms database time. What next?


## 5. Why is `EXPLAIN ANALYZE DELETE ...` dangerous?


## 6. For 8 API instances with pool max 20, 4 workers with pool max 5, and reserve 10, calculate possible connections.


## 7. Why may status be a poor leading index column?


## 8. What does a sort spill indicate?


## 9. How does high-water pagination affect the index query?


## 10. Why should exact planner cost not be a cross-version gate?


## 11. When is a partial index appropriate?


## 12. Design a read/write index decision.


## Submission format

Submit Module 04 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
